"""R17 probe: can the gold resources that no admissible record links to the subject be explained?

Read-only, stdout only, no model calls. Hypotheses:
  H1 unlinked subject account -> account_{user_num:03d}
  H2 a shared non-identity key (order / ticket / statement / archive / trace id ...) links a
     null-identifier record to a record already linked to the subject
  H3 activity rows carry an explicit per-row user / subject field naming the subject
  H4 a security_service audit record seen in ANY file (even after audit_at) exists for the subject

    python3 code/analysis/r17_probe.py > scratch/r17_probe.txt
"""
from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from data_audit import EMAIL_RE, USER_RE, build_index, load_identity, read_csv, record_links, resolve_email  # noqa: E402

KEY_RE = re.compile(r"\b(?:ORD-\d+|CS-\d+|NST-[\d-]+|FIN-\d+|SWF-\d+|segment-\d+(?:-\d+)?|(?:tr|rb)-[A-Za-z0-9-]+)\b")


def main():
    P = print
    ident = load_identity()
    acts = read_csv("system_activity.csv")
    recs, meta, rid_re = build_index(sorted({a["resource_id"].rsplit("_", 1)[0] for a in acts}))
    reqs = {r["case_id"]: r for r in read_csv("sample_deletion_requests.csv")}
    gold = {r["case_id"]: json.loads(r["steps_json"]) for r in read_csv("sample_output.csv")}

    def uid_of(cid):
        return resolve_email(ident, reqs[cid]["email"])[1][0]

    def linked(rid, uid, audit_at, admissible_only=True):
        return [rc for rc in recs if rid in rc.rids and uid in record_links(rc, ident)
                and (not admissible_only or rc.captured_at <= audit_at)]

    # the 26 unlinked (case, rid) pairs
    unlinked = []
    for cid, st in gold.items():
        uid, a = uid_of(cid), reqs[cid]["audit_at"]
        for rid in sorted({s["resource_id"] for s in st}):
            if not any(rid in rc.rids and uid in record_links(rc, ident) for rc in recs):
                unlinked.append((cid, rid))
    P(f"unlinked gold (case, resource) pairs: {len(unlinked)}")
    P("   " + ", ".join(f"{c}:{r}" for c, r in unlinked))

    results = {}

    # H1
    expl, fp, notes = [], [], []
    for cid, st in gold.items():
        uid, a = uid_of(cid), reqs[cid]["audit_at"]
        gold_acc = next(s["resource_id"] for s in st if s["resource_id"].startswith("account_"))
        has_linked_acc = any(r.startswith("account_") and r in rc.rids
                             for rc in recs if rc.captured_at <= a and uid in record_links(rc, ident) for r in rc.rids)
        if has_linked_acc:
            continue
        pred = f"account_{int(uid.split('_')[1]):03d}"
        (expl if pred == gold_acc else fp).append(f"{cid}:{pred}{'' if pred == gold_acc else ' (gold ' + gold_acc + ')'}")
    results["H1 account_{user_num:03d}"] = (expl, fp)

    # H2 shared non-identity keys
    expl, fp = [], []
    gold_rids = {c: {s["resource_id"] for s in st} for c, st in gold.items()}
    for cid in gold:
        uid, a = uid_of(cid), reqs[cid]["audit_at"]
        subj_keys = set()
        for rc in recs:
            if rc.captured_at <= a and uid in record_links(rc, ident):
                subj_keys |= set(KEY_RE.findall(rc.text))
        cands = set()
        for rc in recs:
            if rc.captured_at > a or uid in record_links(rc, ident):
                continue
            if record_links(rc, ident):      # record already belongs to someone else
                continue
            shared = set(KEY_RE.findall(rc.text)) & subj_keys
            if shared:
                cands |= {r for r in rc.rids}
        for r in sorted(cands):
            (expl if (cid, r) in unlinked else (None if r in gold_rids[cid] else fp)).append(f"{cid}:{r}") if \
                ((cid, r) in unlinked or r not in gold_rids[cid]) else None
    results["H2 shared non-identity key"] = (expl, fp)

    # H3 activity per-row subject field
    expl, fp = [], []
    for cid in gold:
        uid = uid_of(cid)
        toks = set(ident.emails[uid]) | {uid}
        for x in acts:
            if x["event_time"] > reqs[cid]["audit_at"]:
                continue
            found = {e.lower() for e in EMAIL_RE.findall(x["details"])} | set(USER_RE.findall(x["details"]))
            if found & toks:
                r = x["resource_id"]
                if (cid, r) in unlinked:
                    expl.append(f"{cid}:{r}")
                elif r not in gold_rids[cid]:
                    fp.append(f"{cid}:{r}({x['activity_id']})")
    results["H3 activity per-row subject field"] = (expl, fp)

    # H4 audit record in any file, even post-audit
    expl, fp = [], []
    for cid in gold:
        uid, a = uid_of(cid), reqs[cid]["audit_at"]
        seen = {r for rc in recs if uid in record_links(rc, ident) for r in rc.rids if r.startswith("audit_record_")}
        for r in sorted(seen):
            if (cid, r) in unlinked or (r in gold_rids[cid] and not linked(r, uid, a)):
                expl.append(f"{cid}:{r}")
            elif r not in gold_rids[cid]:
                fp.append(f"{cid}:{r}")
    results["H4 audit record in any file"] = (expl, fp)

    P()
    P(f"{'hypothesis':38s} {'explained':>9s} {'FP':>4s}  verdict")
    for h, (e, f) in results.items():
        verdict = "ADOPT" if e and not f else "REJECT"
        P(f"{h:38s} {len(e):9d} {len(f):4d}  {verdict}")
    for h, (e, f) in results.items():
        P(f"\n{h}\n   explained: {e or '-'}\n   false positives: {f or '-'}")
    P("\nNote: H4 'explained' counts gold audit records not linked by any ADMISSIBLE file "
      "(post-audit-only) plus any of the 26 fully unlinked pairs.")


if __name__ == "__main__":
    main()
