"""P1 read-only checks: evidence_id citation rules (R13) and multi-request users (R15).

Stdout only, no model calls. Uses the sample files as the public gold reference.

    python3 code/analysis/p1_checks.py > scratch/p1_checks.txt
"""
from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from data_audit import (DATA, EMAIL_RE, USER_RE, build_index, load_identity,  # noqa: E402
                        read_csv, record_links, resolve_email, sniff)

FAMILY_SYSTEM = {  # resource prefix -> owning system (R12, sample-backed)
    "account": "account_service", "search": "search_service", "analytics": "analytics_platform",
    "support": "support_platform", "export": "export_service", "data_flow": "integration_service",
    "backup": "backup_service", "audit_record": "security_service", "tombstone": "identity_service",
}


def file_coverage(meta, recs_by_file):
    """file_id -> set of owning systems the capture covers (records, data_store/system fields, snapshot_scope)."""
    cov = collections.defaultdict(set)
    for fid, m in meta.items():
        for rc in recs_by_file.get(fid, []):
            for r in rc.rids:
                fam = r.rsplit("_", 1)[0]
                if fam in FAMILY_SYSTEM:
                    cov[fid].add(FAMILY_SYSTEM[fam])
        p = DATA / m["path"]
        if m["kind"] == "json":
            def walk(o):
                if isinstance(o, dict):
                    for k in ("data_store", "system", "origin_system"):
                        if isinstance(o.get(k), str):
                            cov[fid].add(o[k])
                    for k, v in o.items():
                        if k.endswith(("_service", "_platform")):
                            cov[fid].add(k)
                        walk(v)
                elif isinstance(o, list):
                    for v in o:
                        walk(v)
            walk(json.loads(p.read_text(encoding="utf-8")))
        elif m["kind"] == "sql-text":
            import sqlite3
            con = sqlite3.connect(":memory:")
            con.executescript(p.read_text(encoding="utf-8"))
            names = {r[0] for r in con.execute("select name from sqlite_master where type='table'")}
            if "snapshot_scope" in names:
                cov[fid] |= {r[0] for r in con.execute("select origin_system from snapshot_scope")}
            con.close()
    return cov


def raw_text(meta, fid, recs_by_file):
    m = meta[fid]
    if m["kind"] in ("png",):
        return ""
    if m["kind"] == "pdf":
        return " ".join(rc.text for rc in recs_by_file.get(fid, []))
    return (DATA / m["path"]).read_text(encoding="utf-8")


def main():
    P = print
    ident = load_identity()
    acts = read_csv("system_activity.csv")
    recs, meta, rid_re = build_index(sorted({a["resource_id"].rsplit("_", 1)[0] for a in acts}))
    by_file = collections.defaultdict(list)
    for rc in recs:
        by_file[rc.file_id].append(rc)
    observes = collections.defaultdict(set)  # rid -> {file_id}
    for rc in recs:
        for r in rc.rids:
            observes[r].add(rc.file_id)
    cap = {fid: m["captured_at"] for fid, m in meta.items()}
    origin = {fid: m["origin"] for fid, m in meta.items()}
    cov = file_coverage(meta, by_file)
    texts = {fid: raw_text(meta, fid, by_file).lower() for fid in meta}

    def subject_in(fid, uid):
        t = texts[fid]
        toks = set(ident.emails[uid]) | {uid} | set(ident.hashes[uid])
        if any(tok in t for tok in toks if tok != uid):
            return True
        return uid in set(USER_RE.findall(t))

    def latest(cands, audit_at):
        c = sorted((cap[f], f) for f in cands if cap[f] <= audit_at)
        return c[-1][1] if c else None

    reqs = {r["case_id"]: r for r in read_csv("sample_deletion_requests.csv")}
    gold = {r["case_id"]: json.loads(r["steps_json"]) for r in read_csv("sample_output.csv")}

    # ------------------------------------------------------------- R13
    P("=" * 100)
    P("TASK 2a  R13 evidence_id rules over every cited sample step")
    P("=" * 100)
    rules = {
        "i_latest_observing": lambda rid, sysn, uid, a, case_cites: latest(observes[rid], a),
        "ii_latest_cover_owner+subject": lambda rid, sysn, uid, a, cc: latest(
            [f for f in meta if sysn in cov[f] and subject_in(f, uid)], a),
        "iii_latest_cover_owner_any_subject": lambda rid, sysn, uid, a, cc: latest(
            [f for f in meta if sysn in cov[f]], a),
        "iv_latest_origin_names_family": lambda rid, sysn, uid, a, cc: latest(
            [f for f in meta if rid.rsplit("_", 1)[0] in origin[f]], a),
        "v_latest_with_subject_any_system": lambda rid, sysn, uid, a, cc: latest(
            [f for f in meta if subject_in(f, uid)], a),
    }
    hits = collections.Counter()
    total = collections.Counter()
    rows = []
    for cid, steps in gold.items():
        req = reqs[cid]
        a = req["audit_at"]
        uid = resolve_email(ident, req["email"])[1][0]
        case_cites = {s["evidence_id"] for s in steps if s["evidence_id"]}
        for s in steps:
            ev = s["evidence_id"]
            if not ev:
                continue
            rid = s["resource_id"]
            kind = "observed" if any(cap[f] <= a for f in observes[rid]) else "ABSENCE"
            preds = {name: fn(rid, s["system_id"], uid, a, case_cites) for name, fn in rules.items()}
            for name, p in preds.items():
                total[(kind, name)] += 1
                hits[(kind, name)] += p == ev
            rows.append((cid, s["step_no"], rid, kind, ev, preds))
    names = list(rules)
    P(f"{'case':8s} {'st':>2s} {'resource':18s} {'kind':8s} {'gold':12s} " + " ".join(f"{n[:22]:>22s}" for n in names))
    for cid, st, rid, kind, ev, preds in rows:
        P(f"{cid:8s} {st:2d} {rid:18s} {kind:8s} {ev:12s} " +
          " ".join(f"{(str(preds[n]) + ('' if preds[n] == ev else '*')):>22s}" for n in names))
    P("\n(* = differs from gold)")
    for kind in ("observed", "ABSENCE"):
        P(f"\n{kind} steps:")
        for n in names:
            if total[(kind, n)]:
                P(f"   {n:36s} {hits[(kind, n)]}/{total[(kind, n)]}")
    # combined rule
    comb_ok, comb_bad = 0, []
    for cid, st, rid, kind, ev, preds in rows:
        p = preds["i_latest_observing"] if kind == "observed" else (
            preds["ii_latest_cover_owner+subject"] or preds["iv_latest_origin_names_family"])
        if p == ev:
            comb_ok += 1
        else:
            comb_bad.append((cid, st, rid, ev, p))
    P(f"\nCOMBINED (observed -> i; absence -> ii, fallback iv): {comb_ok}/{len(rows)}; exceptions: {comb_bad}")

    P("\nAbsence-step detail: admissible files covering the owning system, newest first (cover/subject flags)")
    for cid, st, rid, kind, ev, preds in rows:
        if kind != "ABSENCE":
            continue
        req = reqs[cid]
        uid = resolve_email(ident, req["email"])[1][0]
        sysn = FAMILY_SYSTEM[rid.rsplit("_", 1)[0]]
        P(f"  {cid} {rid} audit_at={req['audit_at']} gold={ev} uid={uid}")
        c = sorted(((cap[f], f) for f in meta if cap[f] <= req["audit_at"] and sysn in cov[f]), reverse=True)[:8]
        for t, f in c:
            P(f"     {f} cap={t} origin={origin[f]} subject_in_file={subject_in(f, uid)}{'  <-- gold' if f == ev else ''}")
        acts_rid = [x for x in acts if x["resource_id"] == rid]
        P(f"     activity rows for {rid}: " + "; ".join(f"{x['activity_id']} {x['event_time']} {x['event_type']} {x['reported_result']}" for x in acts_rid) or "none")

    # ------------------------------------------------------------- R15
    P()
    P("=" * 100)
    P("TASK 2b  R15 multi-request users")
    P("=" * 100)
    all_reqs = [("sample", r) for r in read_csv("sample_deletion_requests.csv")] + [("test", r) for r in read_csv("deletion_requests.csv")]
    for uid in ("user_07", "user_17", "user_18"):
        cases = [(sp, r) for sp, r in all_reqs if uid in resolve_email(ident, r["email"])[1]]
        P(f"\n### {uid}  emails={sorted(ident.emails[uid])}")
        for sp, r in cases:
            g = ""
            if r["case_id"] in gold:
                g = " gold rids=" + ",".join(sorted({s['resource_id'] for s in gold[r['case_id']]}))
            P(f"   {sp:6s} {r['case_id']:9s} requested_at={r['requested_at']} reported_at={r['reported_at']} audit_at={r['audit_at']} "
              f"reported={r['reported_status']}{g}")
        linked = collections.defaultdict(list)
        for rc in recs:
            if uid in record_links(rc, ident):
                for rid in rc.rids:
                    linked[rid].append(f"{rc.file_id}@{rc.captured_at}" + (f"(rec {rc.rec_time})" if rc.rec_time else ""))
        toks = set(ident.emails[uid]) | {uid}
        for x in acts:
            found = {e.lower() for e in EMAIL_RE.findall(x["details"])} | set(USER_RE.findall(x["details"]))
            if found & toks:
                for rid in {x["resource_id"]} | set(rid_re.findall(x["details"])):
                    linked[rid].append(f"{x['activity_id']}@{x['event_time']} {x['event_type']}")
        for rid in sorted(linked):
            P(f"   {rid}")
            for src in sorted(set(linked[rid]), key=lambda s: s.split("@")[1]):
                P(f"       src  {src}")
            for x in sorted((x for x in acts if x["resource_id"] == rid), key=lambda x: x["event_time"]):
                P(f"       act  {x['activity_id']}@{x['event_time']} {x['event_type']} {x['reported_result']} | {x['details'][:90]}")


if __name__ == "__main__":
    main()


def window_check():
    """R15 candidate: a gold resource has a file observation or activity row inside [requested_at, audit_at]."""
    P = print
    ident = load_identity()
    acts = read_csv("system_activity.csv")
    recs, meta, rid_re = build_index(sorted({a["resource_id"].rsplit("_", 1)[0] for a in acts}))
    obs = collections.defaultdict(list)
    for rc in recs:
        for r in rc.rids:
            obs[r].append(("file", rc.file_id, rc.captured_at))
    for x in acts:
        for r in {x["resource_id"]} | set(rid_re.findall(x["details"])):
            obs[r].append(("act", x["activity_id"], x["event_time"]))
    reqs = {r["case_id"]: r for r in read_csv("sample_deletion_requests.csv")}
    P()
    P("=" * 100)
    P("TASK 2b-ii  window test over all sample gold resources: any source with requested_at <= t <= audit_at?")
    P("=" * 100)
    stats = collections.Counter()
    for r in read_csv("sample_output.csv"):
        q = reqs[r["case_id"]]
        for rid in sorted({s["resource_id"] for s in json.loads(r["steps_json"])}):
            srcs = obs.get(rid, [])
            inwin = [s for s in srcs if q["requested_at"] <= s[2] <= q["audit_at"]]
            files_in = [s for s in inwin if s[0] == "file"]
            before = [s for s in srcs if s[2] < q["requested_at"]]
            tag = "file-in-window" if files_in else ("act-only-in-window" if inwin else ("NONE" if not srcs else "OUTSIDE"))
            stats[tag] += 1
            if tag != "file-in-window":
                P(f"   {r['case_id']} {rid:18s} {tag:20s} req={q['requested_at']} audit={q['audit_at']} "
                  f"in={[s[1] for s in inwin]} before={[s[1] + '@' + s[2][:10] for s in before][:4]}")
    P(f"   totals: {dict(stats)}")


if __name__ == "__main__":
    window_check()


def batch_check():
    """Deletion-worker batches: activity rows from the same worker run as the subject's account DELETE."""
    P = print
    acts = read_csv("system_activity.csv")
    by_id = {a["activity_id"]: a for a in acts}
    order = [a["activity_id"] for a in acts]
    reqs = {r["case_id"]: r for r in read_csv("sample_deletion_requests.csv")}
    P()
    P("=" * 100)
    P("BATCH  deletion_worker rows adjacent (by activity_id) to the gold account's DELETE_RECORD row")
    P("=" * 100)
    for r in read_csv("sample_output.csv"):
        st = json.loads(r["steps_json"])
        gold_rids = {s["resource_id"] for s in st}
        acc = next(s["resource_id"] for s in st if s["resource_id"].startswith("account_"))
        hits = [a for a in acts if a["resource_id"] == acc and a["event_type"] == "DELETE_RECORD"]
        if not hits:
            P(f"{r['case_id']} {acc}: no DELETE_RECORD activity")
            continue
        i = order.index(hits[0]["activity_id"])
        batch = []
        for j in range(i, min(i + 12, len(order))):
            a = by_id[order[j]]
            if j > i and a["source_system"] != "deletion_worker":
                break
            batch.append(a)
        P(f"{r['case_id']} {r['deletion_status']:10s} reported_at={reqs[r['case_id']]['reported_at']} audit={reqs[r['case_id']]['audit_at']}")
        for a in batch:
            mark = "GOLD" if a["resource_id"] in gold_rids else "----"
            P(f"    {mark} {a['activity_id']} {a['event_time']} {a['event_type']:18s} {a['resource_id']:18s} {a['reported_result']}")
        missing = gold_rids - {a["resource_id"] for a in batch}
        P(f"    gold rids not in batch: {sorted(missing)}")


if __name__ == "__main__":
    batch_check()


def link_history_check():
    """Is every gold resource tied to the subject by SOME file record (any time), and when?"""
    P = print
    ident = load_identity()
    acts = read_csv("system_activity.csv")
    recs, meta, rid_re = build_index(sorted({a["resource_id"].rsplit("_", 1)[0] for a in acts}))
    reqs = {r["case_id"]: r for r in read_csv("sample_deletion_requests.csv")}
    P()
    P("=" * 100)
    P("LINK-HISTORY  per gold resource: files whose record links it to the subject (<=audit / AFTER)")
    P("=" * 100)
    cnt = collections.Counter()
    for r in read_csv("sample_output.csv"):
        q = reqs[r["case_id"]]
        uid = resolve_email(ident, q["email"])[1][0]
        for rid in sorted({s["resource_id"] for s in json.loads(r["steps_json"])}):
            links = sorted({(rc.captured_at, rc.file_id) for rc in recs if rid in rc.rids and uid in record_links(rc, ident)})
            adm = [f for t, f in links if t <= q["audit_at"]]
            aft = [f for t, f in links if t > q["audit_at"]]
            tag = "linked<=audit" if adm else ("linked-AFTER-only" if aft else "NOT-LINKED")
            cnt[tag] += 1
            if tag != "linked<=audit":
                P(f"   {r['case_id']} {rid:18s} {tag:18s} after={aft}")
    P(f"   totals: {dict(cnt)}")


if __name__ == "__main__":
    link_history_check()
