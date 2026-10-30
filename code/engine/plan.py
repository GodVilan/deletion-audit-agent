"""Per-case planner: identity -> linked resources -> admissible state -> steps, evidence ids, status."""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

from .identity import Identity
from .loaders import EMAIL_RE, HASH_RE, PHONE_RE, Evidence, add_media, read_csv
from .rules import (OPS, family, merge_states, ops_for, r4_observe, r12_system, r14_order, r15_attribute,
                    r16_media_only, r17_padded_account, r3c_post_audit_link, h4_legal_exists)



def _has_token(text: str, token: str) -> bool:
    """R2 exact match inside raw text: the token must not be part of a longer identifier
    (user_12 must not match user_123; alice@ex.com must not match malice@ex.com)."""
    return re.search(rf"(?<![A-Za-z0-9._%+\-]){re.escape(token)}(?![A-Za-z0-9])", text) is not None


class Engine:
    def __init__(self, data_dir: Path, media: dict | None = None):
        """media: {file_id: {"records": [...], "path": "cache"|"live"|"media_unread"}} from agent.media."""
        self.data_dir = data_dir
        self.activity = read_csv(data_dir / "system_activity.csv")
        self.identity = Identity(read_csv(data_dir / "user_identities.csv"), read_csv(data_dir / "user_audit_log.csv"))
        self.ev = Evidence(data_dir, sorted({a["resource_id"].rsplit("_", 1)[0] for a in self.activity}))
        self.r3c_families = None   # None -> rules.R3C_FAMILIES; probes pass an explicit set
        self.trace_on = False      # --trace: record per-resource links/observations/state in the report
        self.media_status = {fid: "not_extracted" for fid, _ in self.ev.media_files()}
        for fid, res in (media or {}).items():
            self.media_status[fid] = res.get("path", "?")
            add_media(self.ev, fid, res.get("records") or [])
        self._bind_media_refs()
        self.all_requests = []
        for name in ("sample_deletion_requests.csv", "deletion_requests.csv"):
            if (data_dir / name).exists():
                self.all_requests += read_csv(data_dir / name)
        # indexes
        self.rec_users = [self.identity.users_in(rc.text) for rc in self.ev.records]
        self.user_records = defaultdict(list)
        for i, us in enumerate(self.rec_users):
            for u in us:
                self.user_records[u].append(i)
        self.primary_obs = defaultdict(list)          # rid -> [(captured_at, file_id, fields)]
        self.mentions = defaultdict(list)             # rid -> [(captured_at, file_id)]
        for rc in self.ev.records:
            for rid, f in rc.primary.items():
                self.primary_obs[rid].append((rc.captured_at, rc.file_id, f))
            for rid in rc.rids:
                self.mentions[rid].append((rc.captured_at, rc.file_id))
        self.link_acts = defaultdict(list)            # uid -> [(event_time, rid, activity_id)]
        for a in self.activity:
            if a["event_type"] != "LINK_RESOURCE_IDENTITY":
                continue
            us = self.identity.users_in(a["details"])
            rids = {a["resource_id"]} | set(self.ev.rid_re.findall(a["details"]))
            for u in us:
                for r in rids:
                    self.link_acts[u].append((a["event_time"], r, a["activity_id"]))
        # R17/H7d support: ids known anywhere, who evidence attributes them to, and when first seen
        self.first_seen = {}
        for a in self.activity:
            self.first_seen[a["resource_id"]] = min(self.first_seen.get(a["resource_id"], "9999"), a["event_time"])
        for rc in self.ev.records:
            for rid in rc.rids:
                self.first_seen[rid] = min(self.first_seen.get(rid, "9999"), rc.captured_at)
        self.attributed = defaultdict(set)
        for i, us in enumerate(self.rec_users):
            for rid in self.ev.records[i].rids:
                self.attributed[rid] |= us
        for u, items in self.link_acts.items():
            for _, rid, _ in items:
                self.attributed[rid].add(u)
        self.requests_by_user = defaultdict(list)
        for r in self.all_requests:
            for u in self.identity.resolve(r["email"]):
                self.requests_by_user[u].append(r)

    def _bind_media_refs(self):
        """A media record that prints no resource id (a file name, a statement number, a bare user_id) is
        bound to the resource a LINK_RESOURCE_IDENTITY row names next to that reference, e.g.
        "object_19 (delivery_confirmation_19.pdf)", "export_1842 (NST-2026-0718-1842)". The reference must
        appear as a whole token inside the printed reference (e.g. "statement NST-2026-0718-1842")."""
        ref_to_rid = {}
        for a in self.activity:
            if a["event_type"] == "LINK_RESOURCE_IDENTITY":
                for rid, ref in re.findall(r"\b(\w+_\d+) \(([^)]+)\)", a["details"]):
                    if ref != rid:
                        ref_to_rid[ref.lower()] = rid
        for rc in self.ev.records:
            if rc.kind != "media" or rc.primary:
                continue
            for ref in getattr(rc, "refs", ()):
                low = str(ref).lower()
                rid = ref_to_rid.get(low) or next(
                    (r for key, r in ref_to_rid.items() if re.search(rf"(?<![\w-]){re.escape(key)}(?![\w-])", low)), None)
                if rid:
                    rc.primary[rid] = rc.media_fields
                    rc.rids = sorted(set(rc.rids) | {rid})
                    self.ev.coverage[rc.file_id].add(rid.rsplit("_", 1)[0])

    def r16_conflict(self, rid, uid, audit_at, sources):
        """R16: a resource tied to the subject only by an activity claim, whose admissible file/media
        content shows direct identifiers of someone else, is not the subject's (evidence_60
        marketing_001 shows sj.park@naver.com while activity_4008 claims user_09)."""
        if any(not str(s).startswith("activity_") for s in sources):
            return False
        for rc in self.ev.records:
            if rid in rc.primary and rc.captured_at <= audit_at:
                direct = EMAIL_RE.search(rc.text) or PHONE_RE.search(rc.text) or HASH_RE.search(rc.text)
                if direct and uid not in self.identity.users_in(rc.text):
                    return True
        return False

    # ------------------------------------------------------------------ helpers
    def subject_tokens(self, uid):
        return set(self.identity.emails[uid]) | set(self.identity.hashes[uid]) | {uid}

    def r13_evidence(self, rid, uid, audit_at):
        """R13 combined rule (75/75 on samples): observed -> latest admissible file mentioning the
        resource; absence -> latest admissible file covering the owning system and containing the
        subject, else latest admissible file whose origin names the family."""
        obs = [(t, f) for t, f in self.mentions.get(rid, []) if t <= audit_at]
        if obs:
            return max(obs)[1]
        fam = family(rid)
        sysname = r12_system(rid)
        toks = self.subject_tokens(uid)
        cands = []
        for fid, m in self.ev.meta.items():
            if m["captured_at"] > audit_at:
                continue
            cov = self.ev.coverage[fid]
            if (fam in cov or f"system:{sysname}" in cov) and any(_has_token(self.ev.raw[fid], t) for t in toks):
                cands.append((m["captured_at"], fid))
        if cands:
            return max(cands)[1]
        cands = [(m["captured_at"], fid) for fid, m in self.ev.meta.items()
                 if m["captured_at"] <= audit_at and fam in m["origin"] and m["kind"] not in ("pdf", "png")]
        return max(cands)[1] if cands else ""

    # ------------------------------------------------------------------ main
    def plan(self, req: dict) -> dict:
        cid, audit_at = req["case_id"], req["audit_at"]
        uids = self.identity.resolve(req["email"])
        report = {"case_id": cid, "uids": uids, "flags": [], "resources": {}}
        if not uids:
            report["flags"].append("identity_unresolved")
            return {"status": "COMPLETE", "steps": [], "report": report}
        uid = uids[0]
        own_reqs = self.requests_by_user[uid]

        # linked resources with their earliest link time and admissible-link flag
        link = {}  # rid -> {"first": t, "admissible": bool, "sources": [...]}

        def add(rid, t, src):
            e = link.setdefault(rid, {"first": t, "admissible": False, "sources": []})
            e["first"] = min(e["first"], t)
            e["admissible"] |= t <= audit_at
            e["sources"].append(src)

        for i in self.user_records.get(uid, []):
            rc = self.ev.records[i]
            for rid in rc.rids:
                add(rid, rc.captured_at, rc.file_id)
        for t, rid, aid in self.link_acts.get(uid, []):
            add(rid, t, aid)

        if not any(r.startswith("account_") and e["admissible"] for r, e in link.items()):
            deleted_in_window = {a["resource_id"] for a in self.activity
                                 if a["source_system"] == "deletion_worker" and a["event_type"] == "DELETE_RECORD"
                                 and req["requested_at"] <= a["event_time"] <= audit_at}
            rid = r17_padded_account(uid, deleted_in_window, self.attributed)
            if rid:
                add(rid, self.first_seen[rid], "R17/H7d")
                report["flags"].append(f"R17_H7d:{rid}")

        steps = []
        if self.trace_on:   # instrumentation for --trace (no effect on decisions)
            report["trace"] = {rid: {"first_link": e["first"], "admissible_link": e["admissible"],
                                     "sources": sorted(set(map(str, e["sources"]))),
                                     "observations": [{"file_id": f, "captured_at": t,
                                                       "admissible": t <= audit_at}
                                                      for t, f, _ in sorted(self.primary_obs.get(rid, []))]}
                               for rid, e in link.items()}
        for rid, e in sorted(link.items()):
            fam = family(rid)
            if fam not in ("account", "search", "analytics", "support", "export", "data_flow", "backup",
                           "audit_record", "tombstone", "legal_hold", "object", "marketing"):
                continue
            if not r15_attribute(e["first"], own_reqs, cid):
                report["resources"][rid] = "R15: belongs to another request of this user"
                continue
            if not e["admissible"] and fam != "audit_record" and not r3c_post_audit_link(fam, self.r3c_families) \
                    and not (fam == "legal_hold" and h4_legal_exists(rid, audit_at, self.activity)):
                # R3; H4 exception for audit records; R3c for adopted families
                report["resources"][rid] = "R3: linked only by post-audit evidence"
                continue
            if self.r16_conflict(rid, uid, audit_at, e["sources"]):
                report["flags"].append(f"R16_conflict:{rid}")
                report["resources"][rid] = "R16: file content names another person than the activity claim"
                continue
            prim = [(t, f, fl) for t, f, fl in self.primary_obs.get(rid, []) if t <= audit_at]
            has_text = any(t <= audit_at for t, _ in self.mentions.get(rid, []))
            if fam != "audit_record" and "R17/H7d" not in e["sources"] and e["admissible"] and \
                    r16_media_only(rid, has_text):
                # H4 audit records and H7d accounts (evidence path = activity row) are exempt
                report["flags"].append(f"media_needed:{rid}")
                report["resources"][rid] = "R16: activity-linked, observed only in media (v0 skips)"
                continue
            if prim:
                latest = max(t for t, _, _ in prim)
                st = merge_states([r4_observe(fl) for t, _, fl in prim if t == latest])
                hints = set().union(*(r4_observe(fl)["hints"] for _, _, fl in prim))
            else:
                st, hints = None, set()
            if fam in ("audit_record", "legal_hold") and st is not None and not st["present"]:
                report["flags"].append(f"retained_record_missing:{rid}")
                continue
            ops = ops_for(fam, st, hints)
            report["resources"][rid] = ops
            if self.trace_on:
                report["trace"][rid]["state"] = None if st is None else {k: (sorted(v) if isinstance(v, set) else v)
                                                                         for k, v in st.items()}
                report["trace"][rid]["category_hints"] = sorted(hints)
            for op in ops:
                phase, state = OPS[op]
                steps.append({"step_no": 0, "phase": phase, "system_id": r12_system(rid), "resource_id": rid,
                              "operation": op, "state": state, "evidence_id": ""})

        if not any(s["resource_id"].startswith("account_") for s in steps):
            report["flags"].append("R17:no_account_evidence_path")
        # media that could not be read (no key, no cache) and falls inside this request's window
        for fid, m in self.ev.media_files():
            if self.media_status.get(fid) in ("media_unread", "not_extracted") and \
                    req["requested_at"] <= m["captured_at"] <= audit_at:
                report["flags"].append(f"media_unread:{fid}")

        status = "INCOMPLETE" if any(s["phase"] == "FINDING" for s in steps) else "COMPLETE"
        for s in steps:
            if s["phase"] == "FINDING" or (status == "COMPLETE"):
                s["evidence_id"] = self.r13_evidence(s["resource_id"], uid, audit_at)
        if status == "COMPLETE":
            # PS L127: COMPLETE verifications must cite evidence; an H4 record known only from post-audit
            # files cannot be cited at audit_at, so it is dropped and flagged (all COMPLETE samples cite theirs).
            for s in [s for s in steps if not s["evidence_id"]]:
                report["flags"].append(f"uncitable_verify_dropped:{s['resource_id']}")
            steps = [s for s in steps if s["evidence_id"]]
        return {"status": status, "steps": r14_order(steps), "report": report}
