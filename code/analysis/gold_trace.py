"""Trace every sample gold step back to the evidence and activity that mention it.

Read-only, stdout only, no model calls. Uses the participant-facing sample files
(sample_deletion_requests.csv, sample_output.csv) as the public gold reference.

    python3 code/analysis/gold_trace.py > scratch/gold_trace.txt
"""
from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from data_audit import (EMAIL_RE, USER_RE, build_index, load_identity, read_csv,  # noqa: E402
                        record_links, resolve_email)


def snippet(rec, rid: str, limit: int = 300) -> str:
    if rec.kind == "log":
        lines = [ln for ln in rec.text.splitlines()
                 if rid in ln or EMAIL_RE.search(ln) or USER_RE.search(ln)]
        s = " ⏎ ".join(lines)
    elif rec.kind == "pdf":
        i = rec.text.find(rid)
        s = rec.text[max(0, i - 150): i + 150] if i >= 0 else rec.text
    else:
        s = rec.text
    s = re.sub(r"\s+", " ", s)
    return s if len(s) <= limit else s[: limit - 3] + "..."


def act_line(a) -> str:
    return (f"{a['activity_id']} {a['event_time']} {a['event_type']} {a['source_system']}->{a['target_system']} "
            f"{a['resource_id']} {a['reported_result']} | {a['details'][:160]}")


def main():
    P = print
    ident = load_identity()
    acts = read_csv("system_activity.csv")
    recs, meta, rid_re = build_index(sorted({a["resource_id"].rsplit("_", 1)[0] for a in acts}))
    by_rid = collections.defaultdict(list)
    for rc in recs:
        for r in rc.rids:
            by_rid[r].append(rc)
    act_by_rid = collections.defaultdict(list)
    for a in acts:
        act_by_rid[a["resource_id"]].append(a)
        for r in set(rid_re.findall(a["details"])) - {a["resource_id"]}:
            act_by_rid[r].append(a)

    reqs = {r["case_id"]: r for r in read_csv("sample_deletion_requests.csv")}
    gold = {r["case_id"]: r for r in read_csv("sample_output.csv")}
    flags_all = []

    for cid, req in reqs.items():
        g = gold[cid]
        steps = json.loads(g["steps_json"])
        audit_at = req["audit_at"]
        how, uids = resolve_email(ident, req["email"])
        uid = uids[0] if uids else None
        P("#" * 110)
        P(f"{cid}  gold={g['deletion_status']}  steps={len(steps)}")
        P(f"   email={req['email']} -> {how} {uids}")
        if uid:
            em = ", ".join(f"{e}[{'/'.join(sorted(t))}]" for e, t in sorted(ident.emails[uid].items()))
            P(f"   identifiers: emails={em} phones={sorted(ident.phones[uid])} hashes={len(ident.hashes[uid])}")
        P(f"   requested_at={req['requested_at']} reported={req['reported_status']}@{req['reported_at']} audit_at={audit_at}")
        P(f"   request_text: {req['request_text']}")
        gold_rids = set()
        for s in steps:
            rid, ev = s["resource_id"], s["evidence_id"]
            gold_rids.add(rid)
            P(f"   STEP {s['step_no']:2d} {s['phase']:12s} {s['system_id']:20s} {rid:20s} {s['operation']:26s} {s['state']:10s} ev={ev!r}")
            cited_systems = set()
            for rc in by_rid.get(rid, []):
                when = "<=audit" if rc.captured_at <= audit_at else "AFTER "
                mark = " *CITED*" if rc.file_id == ev else ""
                sysname = rc.rid_system.get(rid) or rc.system
                if rc.file_id == ev:
                    cited_systems.add(sysname)
                rt = f" rec_time={rc.rec_time}" if rc.rec_time else ""
                P(f"        [{when}] {rc.file_id} cap={rc.captured_at}{rt} sys={sysname}{mark}")
                P(f"                 {snippet(rc, rid)}")
            for a in act_by_rid.get(rid, []):
                when = "<=audit" if a["event_time"] <= audit_at else "AFTER "
                mark = " *CITED*" if a["activity_id"] == ev else ""
                P(f"        [{when}] ACT {act_line(a)}{mark}")
            if not by_rid.get(rid) and not act_by_rid.get(rid):
                P("        (resource_id appears in no parsed evidence record and no activity row)")
            if ev and ev.startswith("evidence_"):
                if not cited_systems:
                    f = f"{cid} step {s['step_no']} {rid}: NOT FOUND in cited {ev} (kind={meta[ev]['kind']})"
                    P(f"        !! {f}")
                    flags_all.append(f)
                elif s["system_id"] not in cited_systems:
                    kind = ("names no system (only table/source)" if all(c.startswith(("table:", "source:")) for c in cited_systems)
                            else "names a DIFFERENT system")
                    f = f"{cid} step {s['step_no']} {rid}: gold system_id={s['system_id']}; cited {ev} {kind}: {sorted(cited_systems)}"
                    P(f"        !! {f}")
                    flags_all.append(f)

        # resources linked to the same user but absent from gold
        P(f"   --- resources linked to {uid} in evidence/activity but NOT in gold")
        linked = collections.defaultdict(list)
        if uid:
            for rc in recs:
                links = record_links(rc, ident).get(uid)
                if links:
                    for r in rc.rids:
                        if r not in gold_rids:
                            linked[r].append((rc, sorted(links)))
            user_tokens = set(ident.emails[uid]) | {uid}
            for a in acts:
                toks = {e.lower() for e in EMAIL_RE.findall(a["details"])} | set(USER_RE.findall(a["details"]))
                if toks & user_tokens:
                    for r in {a["resource_id"]} | set(rid_re.findall(a["details"])):
                        if r not in gold_rids:
                            linked[r].append((a, ["activity details"]))
        if not linked:
            P("        none")
        for r in sorted(linked):
            P(f"     {r}")
            for src, links in linked[r]:
                if isinstance(src, dict):
                    when = "<=audit" if src["event_time"] <= audit_at else "AFTER "
                    P(f"        [{when}] ACT {act_line(src)}")
                else:
                    when = "<=audit" if src.captured_at <= audit_at else "AFTER "
                    P(f"        [{when}] {src.file_id} cap={src.captured_at} sys={src.rid_system.get(r) or src.system} via={links}")
                    P(f"                 {snippet(src, r)}")
            n_act = len(act_by_rid.get(r, []))
            if n_act:
                P(f"        activity rows for {r}: {n_act}")
                for a in act_by_rid[r]:
                    when = "<=audit" if a["event_time"] <= audit_at else "AFTER "
                    P(f"          [{when}] {act_line(a)}")
        P()

    P("#" * 110)
    P(f"SUMMARY: {len(flags_all)} system/citation flags")
    for f in flags_all:
        P(f"   {f}")


if __name__ == "__main__":
    main()
