"""R17 probe 2: batch structure, elimination and conditional-format hypotheses for unlinked accounts/analytics.

Read-only, stdout only, no model calls. Reads sample_output.csv only to SCORE hypotheses (dev analysis).

    python3 code/analysis/r17_probe2.py dump  > scratch/r17_dump.txt
    python3 code/analysis/r17_probe2.py probe > scratch/r17_probe2.txt
"""
from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))
from engine.loaders import read_csv  # noqa: E402
from engine.plan import Engine  # noqa: E402

DATA = ROOT / "dataset"
BATCH_GAP_H = 1.5


def hours(a, b):
    from datetime import datetime
    f = "%Y-%m-%dT%H:%M:%SZ"
    return abs((datetime.strptime(b, f) - datetime.strptime(a, f)).total_seconds()) / 3600


class Ctx:
    def __init__(self):
        self.e = Engine(DATA)
        self.acts = self.e.activity
        self.reqs = read_csv(DATA / "sample_deletion_requests.csv") + read_csv(DATA / "deletion_requests.csv")
        self.req = {r["case_id"]: r for r in self.reqs}
        self.gold = {r["case_id"]: json.loads(r["steps_json"]) for r in read_csv(DATA / "sample_output.csv")}
        # rid -> users attributable via evidence (any file record, any time) or LINK activity
        self.attr = defaultdict(set)
        for i, us in enumerate(self.e.rec_users):
            for rid in self.e.ev.records[i].rids:
                self.attr[rid] |= us
        for u, items in self.e.link_acts.items():
            for _, rid, _ in items:
                self.attr[rid].add(u)
        # batches: deletion_worker rows in time order, split where the gap exceeds BATCH_GAP_H
        # (rows from other sources interleave and must not split a run)
        dw = sorted((a for a in self.acts if a["source_system"] == "deletion_worker"), key=lambda a: a["event_time"])
        self.batches, cur = [], []
        for a in dw:
            if cur and hours(cur[-1]["event_time"], a["event_time"]) > BATCH_GAP_H:
                self.batches.append(cur)
                cur = []
            cur.append(a)
        if cur:
            self.batches.append(cur)
        self.batch_of = {a["activity_id"]: bi for bi, b in enumerate(self.batches) for a in b}

    def uid(self, cid):
        u = self.e.identity.resolve(self.req[cid]["email"])
        return u[0] if u else None

    def linked_family(self, uid, fam):
        return {rid for i in self.e.user_records.get(uid, []) for rid in self.e.ev.records[i].rids
                if rid.startswith(fam + "_")} | {rid for _, rid, _ in self.e.link_acts.get(uid, []) if rid.startswith(fam + "_")}

    def who(self, rid):
        us = sorted(self.attr.get(rid, ()))
        out = []
        for u in us:
            cs = [r["case_id"] for r in self.reqs if u in self.e.identity.resolve(r["email"])]
            out.append(f"{u}({','.join(cs) or 'no request'})")
        return ", ".join(out) or "UNATTRIBUTED"


def dump(c: Ctx, cases):
    P = print
    hdr_a = list(c.acts[0].keys())
    for cid in cases:
        r = c.req[cid]
        gold_ids = sorted({s["resource_id"] for s in c.gold[cid]
                           if s["resource_id"].startswith(("account_", "analytics_"))})
        P("#" * 110)
        P(f"{cid} uid={c.uid(cid)} gold account/analytics ids: {gold_ids}")
        P("REQUEST ROW: " + ",".join(r[k] for k in r))
        for rid in gold_ids:
            P(f"\n== {rid}  (attributable via evidence to: {c.who(rid)})")
            for a in c.acts:
                if a["resource_id"] == rid or rid in a["details"]:
                    P("  ACTIVITY: " + ",".join(a[k] for k in hdr_a))
                    bi = c.batch_of.get(a["activity_id"])
                    if bi is not None:
                        b = c.batches[bi]
                        P(f"  BATCH #{bi}: {len(b)} rows {b[0]['event_time']} .. {b[-1]['event_time']}")
                        for x in b:
                            P(f"     {','.join(x[k] for k in hdr_a)}   -> {x['resource_id']}: {c.who(x['resource_id'])}")
            for a in read_csv(DATA / "user_audit_log.csv"):
                if rid in ",".join(a.values()):
                    P("  AUDIT: " + ",".join(a.values()))
            for rc in c.e.ev.records:
                if rid in rc.rids:
                    P(f"  EVIDENCE {rc.file_id} (captured {rc.captured_at}, {rc.kind}): {rc.text[:600]}")
            for fid, m in c.e.ev.meta.items():
                if m["kind"] in ("pdf", "png"):
                    continue
                if rid in c.e.ev.raw[fid] and not any(rid in rc.rids for rc in c.e.ev.records if rc.file_id == fid):
                    P(f"  EVIDENCE {fid}: raw text contains {rid} outside parsed records")
        P()


def probe(c: Ctx):
    P = print
    acct_rows = defaultdict(list)    # account rid -> DELETE rows
    anon_rows = defaultdict(list)    # analytics rid -> ANONYMIZE rows
    for a in c.acts:
        if a["event_type"] == "DELETE_RECORD" and a["resource_id"].startswith("account_"):
            acct_rows[a["resource_id"]].append(a)
        if a["event_type"] == "ANONYMIZE_RECORD" and a["resource_id"].startswith("analytics_"):
            anon_rows[a["resource_id"]].append(a)

    # H5: does any deletion_worker row carry a list / subject field?
    h5_rows = [a for b in c.batches for a in b
               if any(tok in a["details"] for tok in ("user_", "@", "subjects", "requests", "[", ";"))]
    P(f"H5 deletion_worker rows whose details carry any subject/user/list token: {len(h5_rows)}")
    for a in h5_rows[:5]:
        P("   " + ",".join(a.values()))
    P(f"   distinct deletion_worker detail templates: "
      f"{sorted({a['details'].replace(a['resource_id'], '<rid>') for b in c.batches for a in b})}")

    def elimination(fam, rows_by_rid):
        """subject -> attributed rid under H6/H8 elimination, plus conflicts."""
        out, why = {}, {}
        for cid, r in c.req.items():
            u = c.uid(cid)
            if not u or c.linked_family(u, fam):
                continue
            picks = set()
            for bi, b in enumerate(c.batches):
                fam_rows = [a for a in b if a["resource_id"].startswith(fam + "_") and a["resource_id"] in rows_by_rid]
                in_win = [a for a in fam_rows if r["requested_at"] <= a["event_time"] <= r["audit_at"]]
                if not in_win:
                    continue
                unattr = sorted({a["resource_id"] for a in fam_rows if not c.attr.get(a["resource_id"])})
                if len(unattr) == 1 and any(a["resource_id"] == unattr[0] for a in in_win):
                    picks.add(unattr[0])
                    why[cid] = f"batch#{bi} unique unattributed of {len(fam_rows)}"
            if len(picks) == 1:
                out[cid] = picks.pop()
        # the same rid picked for two subjects -> keep neither (ambiguous)
        cnt = defaultdict(list)
        for cid, rid in out.items():
            cnt[rid].append(cid)
        dup = {rid: cs for rid, cs in cnt.items() if len(cs) > 1}
        for rid, cs in dup.items():
            for cid in cs:
                out.pop(cid)
        return out, why, dup

    def score(name, fam, picks, extra_note=""):
        expl, fp = [], []
        for cid, rid in sorted(picks.items()):
            if cid not in c.gold:
                continue
            gold_rids = {s["resource_id"] for s in c.gold[cid] if s["resource_id"].startswith(fam + "_")}
            (expl if rid in gold_rids else fp).append(f"{cid}:{rid}" + ("" if rid in gold_rids else f" (gold {sorted(gold_rids)})"))
        test_fires = sum(1 for cid in picks if cid not in c.gold)
        return name, expl, fp, test_fires

    rows = []
    h6, why6, dup6 = elimination("account", acct_rows)
    rows.append(score("H6 elimination (accounts)", "account", h6))
    # H7: conditional H1 for subjects still without an account
    h7 = {}
    for cid in c.req:
        u = c.uid(cid)
        if not u or c.linked_family(u, "account") or cid in h6:
            continue
        h7[cid] = f"account_{int(u.split('_')[1]):03d}"
    rows.append(score("H7 conditional account_{num:03d}", "account", h7))
    # H7' restricted: only when that id has an evidence/activity path
    known = set(acct_rows) | {rid for rc in c.e.ev.records for rid in rc.rids}
    h7b = {cid: rid for cid, rid in h7.items() if rid in known}
    rows.append(score("H7b  ...and id exists in activity/evidence", "account", h7b))
    h7c = {cid: rid for cid, rid in h7b.items() if not (c.attr.get(rid, set()) - {c.uid(cid)})}
    rows.append(score("H7c  ...and not attributed to another user", "account", h7c))
    from engine.rules import r15_attribute
    first_seen = defaultdict(lambda: "9999")
    for a in c.acts:
        for rid in {a["resource_id"]}:
            first_seen[rid] = min(first_seen[rid], a["event_time"])
    for rc in c.e.ev.records:
        for rid in rc.rids:
            first_seen[rid] = min(first_seen[rid], rc.captured_at)
    h7d = {}
    for cid, rid in h7c.items():
        u = c.uid(cid)
        if int(u.split("_")[1]) >= 100:      # zero-padding distinguishes the format only below 100
            continue
        own = [r for r in c.reqs if u in c.e.identity.resolve(r["email"])]
        if r15_attribute(first_seen[rid], own, cid):
            h7d[cid] = rid
    rows.append(score("H7d  ...user_num<100 (padded form) + R15", "account", h7d))
    P("H7d test fires: " + (", ".join(f"{cid}:{rid}" for cid, rid in sorted(h7d.items()) if cid not in c.gold) or "none"))
    P("H7c test fires: " + ", ".join(f"{cid}:{rid}" for cid, rid in sorted(h7c.items()) if cid not in c.gold))
    P("H7b-only (dropped by H7c): " + ", ".join(f"{cid}:{rid}->{c.who(rid)}" for cid, rid in sorted(h7b.items()) if cid not in h7c))
    h8, why8, dup8 = elimination("analytics", anon_rows)
    rows.append(score("H8 elimination (anonymized analytics)", "analytics", h8))

    P()
    P(f"{'hypothesis':44s} {'explained':>9s} {'FP':>4s} {'test fires':>10s}  verdict")
    for name, e, f, t in rows:
        P(f"{name:44s} {len(e):9d} {len(f):4d} {t:10d}  {'ADOPT' if e and not f else 'REJECT'}")
    P(f"{'H5 batch row carries a parallel subject list':44s} {0:9d} {0:4d} {0:10d}  REJECT (no such field)")
    for name, e, f, t in rows:
        P(f"\n{name}\n   explained: {e or '-'}\n   FP: {f or '-'}")
    P(f"\nH6 ambiguous (same account picked for several subjects, dropped): {dup6}")
    P(f"H8 ambiguous: {dup8}")

    # R17 still flagged on test: subjects with no account after each adopted hypothesis
    test = [cid for cid in c.req if cid not in c.gold]
    base = [cid for cid in test if c.uid(cid) and not c.linked_family(c.uid(cid), "account")]
    after6 = [cid for cid in base if cid not in h6]
    P(f"\nTest cases with no evidence-linked account (R17 basis): {len(base)}; after H6: {len(after6)}; "
      f"after H6+H7: {len([x for x in after6 if x not in h7])}; after H6+H7c: {len([x for x in after6 if x not in h7c])}")
    P("Sample detail per unlinked-account case: gold account | H6 pick | H7 pick | DELETE rows of gold account")
    for cid in sorted(c.gold):
        u = c.uid(cid)
        if c.linked_family(u, "account"):
            continue
        g = next(s["resource_id"] for s in c.gold[cid] if s["resource_id"].startswith("account_"))
        P(f"   {cid} {u}: gold {g} | H6 {h6.get(cid, '-')} ({why6.get(cid, '')}) | H7 {h7.get(cid, '-')} | "
          f"{[(a['activity_id'], a['event_time'], 'batch#' + str(c.batch_of.get(a['activity_id']))) for a in acct_rows.get(g, [])]} "
          f"window {c.req[cid]['requested_at']}..{c.req[cid]['audit_at']}")


if __name__ == "__main__":
    ctx = Ctx()
    if sys.argv[1:2] == ["dump"]:
        dump(ctx, ["case_09", "case_18", "case_26", "case_28"])
    elif sys.argv[1:2] in (["probe"], []):
        probe(ctx)


# ============================================================================ probe 3 (test coverage)
def probe3(c: Ctx):
    """H7d', H7e, H9a, H9b over samples; test fires, collisions with sample gold, R17 remaining."""
    P = print
    num = lambda aid: int(aid.split("_")[1])  # noqa: E731
    gold_res = {cid: {s["resource_id"] for s in st} for cid, st in c.gold.items()}
    gold_owner = defaultdict(set)
    for cid, rs in gold_res.items():
        for r in rs:
            gold_owner[r].add(cid)
    dw_del = [a for a in c.acts if a["source_system"] == "deletion_worker"]

    def in_win(cid, t):
        r = c.req[cid]
        return r["requested_at"] <= t <= r["audit_at"]

    def case_of(uid, t):
        """the request of uid whose window contains t (unique), else None"""
        cs = [r["case_id"] for r in c.reqs if uid in c.e.identity.resolve(r["email"]) and in_win(r["case_id"], t)]
        return cs[0] if len(cs) == 1 else None

    def evaluate(name, picks, fam):
        expl, fp, test, coll = [], [], [], []
        for cid, rid in sorted(picks.items()):
            if cid in c.gold:
                (expl if rid in gold_res[cid] else fp).append(f"{cid}:{rid}")
            else:
                test.append(f"{cid}:{rid}")
                others = gold_owner.get(rid, set()) - {cid}
                if others:
                    coll.append(f"{cid}:{rid} (gold of {sorted(others)})")
        verdict = "ADOPT" if expl and not fp and not coll else "REJECT"
        return [name, fam, expl, fp, test, coll, verdict]

    no_acct = [cid for cid in c.req if c.uid(cid) and not c.linked_family(c.uid(cid), "account")]
    rows = []

    # H7d'
    picks = {}
    for cid in no_acct:
        u = c.uid(cid)
        rid = f"account_{int(u.split('_')[1]):03d}"
        rows_in = [a for a in dw_del if a["event_type"] == "DELETE_RECORD" and a["resource_id"] == rid and in_win(cid, a["event_time"])]
        if rows_in and not (c.attr.get(rid, set()) - {u}):
            picks[cid] = rid
    rows.append(evaluate("H7d' padded id, no <100 cutoff", picks, "account"))

    # H7e
    picks = {}
    for cid in no_acct:
        u = c.uid(cid)
        unattr = [a for a in dw_del if a["event_type"] == "DELETE_RECORD" and a["resource_id"].startswith("account_")
                  and in_win(cid, a["event_time"]) and not c.attr.get(a["resource_id"])]
        if not unattr:
            picks[cid] = f"account_{int(u.split('_')[1]):03d}"
    rows.append(evaluate("H7e padded id, no unattributed DELETE in window", picks, "account"))

    # H9a contiguity
    P("H9a contiguity of attributed rows per batch (by activity_id / by event_time):")
    contig = {"activity_id": [0, 0], "event_time": [0, 0]}
    for key in ("activity_id", "event_time"):
        for b in c.batches:
            seq = sorted(b, key=(lambda a: num(a["activity_id"])) if key == "activity_id" else (lambda a: a["event_time"]))
            subj = [next(iter(c.attr[a["resource_id"]])) for a in seq if len(c.attr.get(a["resource_id"], ())) == 1]
            if len(set(subj)) < 2:
                continue
            runs = [s for i, s in enumerate(subj) if i == 0 or s != subj[i - 1]]
            ok = len(runs) == len(set(runs))
            contig[key][0 if ok else 1] += 1
    P(f"   batches with >=2 attributed subjects: by activity_id contiguous={contig['activity_id'][0]} "
      f"NOT={contig['activity_id'][1]}; by event_time contiguous={contig['event_time'][0]} NOT={contig['event_time'][1]}")
    for fam in ("account", "analytics"):
        for key in ("activity_id", "event_time"):
            picks, amb = {}, defaultdict(set)
            for b in c.batches:
                seq = sorted(b, key=(lambda a: num(a["activity_id"])) if key == "activity_id" else (lambda a: a["event_time"]))
                for i, a in enumerate(seq):
                    rid = a["resource_id"]
                    if not rid.startswith(fam + "_") or c.attr.get(rid):
                        continue
                    prev = next((x for x in reversed(seq[:i]) if len(c.attr.get(x["resource_id"], ())) == 1), None)
                    nxt = next((x for x in seq[i + 1:] if len(c.attr.get(x["resource_id"], ())) == 1), None)
                    if prev and nxt and c.attr[prev["resource_id"]] == c.attr[nxt["resource_id"]]:
                        u = next(iter(c.attr[prev["resource_id"]]))
                        cid = case_of(u, a["event_time"])
                        if cid:
                            amb[rid].add(cid)
            picks = {next(iter(cs)): rid for rid, cs in amb.items() if len(cs) == 1}
            rows.append(evaluate(f"H9a run membership ({key})", picks, fam))

    # H9b exact event_time
    by_time = defaultdict(list)
    for a in c.acts:
        by_time[a["event_time"]].append(a)
    for fam in ("account", "analytics"):
        amb = defaultdict(set)
        for a in dw_del:
            rid = a["resource_id"]
            if not rid.startswith(fam + "_") or c.attr.get(rid):
                continue
            subs = {u for x in by_time[a["event_time"]] if x is not a for u in c.attr.get(x["resource_id"], ())}
            if len(subs) == 1:
                cid = case_of(next(iter(subs)), a["event_time"])
                if cid:
                    amb[rid].add(cid)
        picks = {next(iter(cs)): rid for rid, cs in amb.items() if len(cs) == 1}
        shared = sum(1 for a in dw_del if len(by_time[a["event_time"]]) > 1)
        P(f"H9b ({fam}): deletion_worker rows sharing an exact event_time with any other row: {shared}")
        rows.append(evaluate("H9b exact event_time", picks, fam))
    sub_ids = [a for a in dw_del if any(t in a["details"].lower() for t in ("batch", "run_id", "job", "sub-batch"))]
    P(f"H9b deletion-worker sub-batch id field present in details: {len(sub_ids)} rows")

    P()
    P(f"{'hypothesis':48s} {'fam':9s} {'expl':>4s} {'FP':>3s} {'test':>5s} {'coll':>4s}  verdict")
    for name, fam, e, f, t, col, v in rows:
        P(f"{name:48s} {fam:9s} {len(e):4d} {len(f):3d} {len(t):5d} {len(col):4d}  {v}")
    for name, fam, e, f, t, col, v in rows:
        P(f"\n{name} [{fam}]\n   explained: {e or '-'}\n   FP: {f or '-'}\n   test fires: {t or '-'}\n   collisions: {col or '-'}")
    test_no_acct = [cid for cid in no_acct if cid not in c.gold]
    P(f"\nTest cases with no evidence-linked account (R17 basis, any-time linking): {len(test_no_acct)}")
    for name, fam, e, f, t, col, v in rows:
        if v == "ADOPT" and fam == "account":
            fired = {x.split(":")[0] for x in t}
            P(f"   after {name}: {len([x for x in test_no_acct if x not in fired])}")


if __name__ == "__main__" and sys.argv[1:2] == ["probe3"]:
    probe3(ctx)
