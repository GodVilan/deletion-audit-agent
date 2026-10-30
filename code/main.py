"""Ghost Data Still Exists: deletion-audit agent, engine v0.

    python3 code/main.py                                   # dataset/deletion_requests.csv -> output.csv
    python3 code/main.py --input dataset/sample_deletion_requests.csv --out scratch/sample_pred.csv

Architecture A (SPEC_CARD §12): the deterministic evidence engine (code/engine) owns status and steps_json;
the intent agent (code/agent) owns R1. Runs with or without ANTHROPIC_API_KEY (no key -> deterministic
intent fallback). Writes a run report next to the output (<out>.report.json) and validates the output.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))


def load_dotenv(path: Path = ROOT / ".env") -> None:
    """Load KEY=VALUE lines from the repo-root .env if it exists; never override variables already set.
    Values are never printed or logged (only key presence is reported)."""
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.removeprefix("export ").partition("=")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


load_dotenv()
from concurrent.futures import ThreadPoolExecutor  # noqa: E402

from agent.intent import IntentClassifier  # noqa: E402
from agent.llm import LLM  # noqa: E402
from agent.media import MediaExtractor  # noqa: E402
from engine.plan import Engine  # noqa: E402
from engine.validate import validate  # noqa: E402


def case_num(cid: str) -> int:
    return int(cid.rsplit("_", 1)[1])


def build_engine(data_dir: Path, llm: LLM, workers: int, refresh_media: bool = False) -> tuple[Engine, MediaExtractor, dict]:
    """Extract media (model, cached) in parallel, then build the evidence engine over text + media."""
    from engine.loaders import read_csv as _rc, sniff
    manifest = _rc(data_dir / "evidence_files.csv")
    media_files = [(m["file_id"], data_dir / m["file_path"]) for m in manifest
                   if sniff(data_dir / m["file_path"]) in ("pdf", "png")]
    mx = MediaExtractor(llm)
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futs = {fid: pool.submit(mx.extract, fid, path, sniff(path), refresh_media) for fid, path in media_files}
        media = {fid: f.result() for fid, f in futs.items()}
    mx.seconds = round(time.time() - t0, 1)
    return Engine(data_dir, media=media), mx, media


def run(input_path: Path, out_path: Path, data_dir: Path, engine: Engine | None = None, quiet=False,
        refresh_media: bool = False) -> dict:
    t0 = time.time()
    workers = int(os.environ.get("MAX_WORKERS") or 8)
    llm = LLM()
    engine, mx, media = build_engine(data_dir, llm, workers, refresh_media) if engine is None else (engine, None, {})
    intent = IntentClassifier(llm)
    with open(input_path, newline="", encoding="utf-8") as fh:
        reqs = sorted(csv.DictReader(fh), key=lambda r: case_num(r["case_id"]))

    def classify(req):
        uids = engine.identity.resolve(req["email"])
        rows = [a for a in engine.activity if a["event_type"] == "CLASSIFY_REQUEST"
                and any(a["resource_id"] in engine.ev.records[i].rids for u in uids for i in engine.user_records.get(u, []))]
        return intent.classify(req["request_text"], rows)

    t_int = time.time()
    with ThreadPoolExecutor(max_workers=workers) as pool:          # results joined in case_id order below
        intents = list(pool.map(classify, reqs))
    intent_seconds = round(time.time() - t_int, 1)

    rows, report = [], {"cases": {}, "intent_paths": Counter(), "status": Counter(), "flags": Counter(),
                        "disagreements": []}
    for req, it in zip(reqs, intents):
        fb = it.pop("fallback", None)
        report["intent_paths"][it["path"]] += 1
        if fb is not None and it["path"].startswith("agent") and fb["authorizes_deletion"] != it["authorizes_deletion"]:
            report["disagreements"].append({"case_id": req["case_id"], "agent": it["authorizes_deletion"],
                                            "fallback": fb["authorizes_deletion"], "rationale": it["rationale"]})
        if not it["authorizes_deletion"]:
            status, steps, crep = "NOT_APPLICABLE", [], {"flags": []}
        else:
            res = engine.plan(req)
            status, steps, crep = res["status"], res["steps"], res["report"]
        crep["intent"] = it
        report["cases"][req["case_id"]] = {"status": status, **crep}
        report["status"][status] += 1
        for f in crep.get("flags", []):
            report["flags"][f.split(":")[0]] += 1
        rows.append((req["case_id"], status, json.dumps(steps, separators=(",", ":"), ensure_ascii=False)))
    intent.save()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["case_id", "deletion_status", "steps_json"])
        w.writerows(rows)
    report["usage"] = dict(llm.usage)
    report["usage_by_role"] = {k: dict(v) for k, v in llm.by_role.items()}
    report["media_seconds"] = getattr(mx, "seconds", None)
    report["model"] = llm.model if llm.live else None
    report["workers"] = workers
    report["intent_stats"] = intent.stats
    report["intent_seconds"] = intent_seconds
    report["media"] = {"stats": mx.stats if mx else None, "mode": mx.mode if mx else None,
                       "seconds": getattr(mx, "seconds", None),
                       "files": {fid: {"path": r.get("path"), "records": len(r.get("records") or [])} for fid, r in media.items()}}
    report["seconds"] = round(time.time() - t0, 1)
    rep_path = out_path.with_suffix(out_path.suffix + ".report.json")
    if out_path.resolve() == (ROOT / "output.csv").resolve():
        rep_path = ROOT / "scratch" / "run_report.json"
    rep_path.parent.mkdir(parents=True, exist_ok=True)
    rep_path.write_text(json.dumps(report, indent=1, default=list), encoding="utf-8")
    errs = validate(out_path, input_path, data_dir)
    hard = [e for e in errs if "(warning)" not in e]
    if not quiet:
        print(f"key_present={llm.live} model={report['model']} workers={workers}")
        print(f"wrote {out_path} ({len(rows)} rows) in {report['seconds']}s (intent {intent_seconds}s); report {rep_path}")
        print(f"status: {dict(report['status'])}")
        print(f"intent paths: {dict(report['intent_paths'])}; disagreements agent vs fallback: {len(report['disagreements'])}")
        print(f"media: {report['media']['stats']} mode={report['media']['mode']}")
        print(f"usage: {report['usage']}")
        print(f"usage by role: {report['usage_by_role']}")
        print(f"flags: {dict(report['flags'])}")
        print(f"validator: {len(hard)} errors, {len(errs) - len(hard)} warnings")
    if hard:
        for e in hard[:30]:
            print("VALIDATION ERROR", e, file=sys.stderr)
        raise SystemExit(f"validation failed with {len(hard)} errors")
    return report


RULE_OF = {"account": "R5", "audit_record": "R6", "legal_hold": "R6", "backup": "R9", "data_flow": "R10",
           "tombstone": "R11"}


def rule_fired(fam: str, decision, tr: dict) -> str:
    if isinstance(decision, str):
        return decision.split(":")[0]
    r = RULE_OF.get(fam, "R7+R8")
    if "R17/H7d" in tr.get("sources", []):
        r += " via R17/H7d'"
    elif not tr.get("admissible_link"):
        r += {"account": " via R3c", "audit_record": " via H4", "legal_hold": " via H4-legal"}.get(fam, "")
    return r + " + R12 + R13 + R14"


def write_trace(case_ids: list[str], out_md: Path, data_dir: Path) -> None:
    """Golden trace (ITEM 2): runs the real pipeline on the given cases and writes a readable trace."""
    import tempfile
    sys.path.insert(0, str(ROOT / "code" / "evaluation"))
    import score_sample
    llm = LLM()
    engine, mx, media = build_engine(data_dir, llm, 4)
    engine.trace_on = True
    intent = IntentClassifier(llm)
    reqs = {r["case_id"]: (r, name) for name in ("sample_deletion_requests.csv", "deletion_requests.csv")
            for r in csv.DictReader(open(data_dir / name, encoding="utf-8"))}
    L = [f"# Golden trace\n\nGenerated by `python3 code/main.py --trace {' '.join(case_ids)}` on "
         f"{time.strftime('%Y-%m-%dT%H:%MZ', time.gmtime())} (model {llm.model if llm.live else 'none: fallback'}). "
         "Do not edit by hand.\n"]
    for cid in case_ids:
        req, src = reqs[cid]
        L.append(f"\n## {cid} ({'sample' if src.startswith('sample') else 'test'})\n")
        L.append("### 1. Request\n")
        for k in ("email", "requested_at", "reported_status", "reported_at", "audit_at"):
            L.append(f"- {k}: `{req[k]}`")
        L.append(f"- request_text: \"{req['request_text']}\"")
        uids = engine.identity.resolve(req["email"])
        rows = [a for a in engine.activity if a["event_type"] == "CLASSIFY_REQUEST"
                and any(a["resource_id"] in engine.ev.records[i].rids for u in uids for i in engine.user_records.get(u, []))]
        calls: list = []
        it = intent.classify(req["request_text"], rows, force_live=True, trace=calls)
        L.append("\n### 2. Intent agent (R1)\n")
        if it["path"].startswith("fallback(agent_failed)"):
            cached = intent.classify(req["request_text"], rows)        # cache read (no API call)
            if cached["path"] == "agent(cache)":
                L.append("- live agent call failed (HTTP 400, e.g. API credit exhausted); showing the cached agent "
                         "answer from the last successful run. Tool calls were not re-recorded: re-run "
                         "`python3 code/main.py --trace ...` with a working key to refresh them.")
                it = cached
        L.append(f"- path: `{it['path']}` (cache bypassed for the trace when the API is reachable)")
        for c in calls:
            L.append(f"- step {c['step']}: tool `{c['tool']}` input `{json.dumps(c['input'], ensure_ascii=False)}`")
        L.append(f"- submitted: authorizes_deletion=`{it['authorizes_deletion']}`, scope=`{it['scope']}`, "
                 f"rationale: \"{it['rationale']}\"")
        fb = it.get("fallback") or {}
        L.append(f"- deterministic fallback agrees: `{fb.get('authorizes_deletion') == it['authorizes_deletion']}`")
        L.append("\n### 3. Identity resolution (R2)\n")
        if uids:
            u = uids[0]
            cur = engine.identity.users[u]["email"].lower() == req["email"].lower()
            L.append(f"- `{req['email']}` → `{u}` ({'current' if cur else 'historical'} email, exact case-insensitive match)")
            L.append(f"- identifiers searched: emails {sorted(engine.identity.emails[u])}, "
                     f"{len(engine.identity.hashes[u])} email hash(es), {len(engine.identity.phones[u])} phone(s), user_id `{u}`")
        if not it["authorizes_deletion"]:
            status, steps, crep = "NOT_APPLICABLE", [], {"resources": {}, "trace": {}}
            L.append("\n### 4-5. Evidence, state, rules\n\nNot evaluated: the request does not authorize deletion "
                     "(R1 → NOT_APPLICABLE with `[]`).")
        else:
            res = engine.plan(req)
            status, steps, crep = res["status"], res["steps"], res["report"]
            L.append("\n### 4. Evidence linked to the subject (R3 admissibility by manifest captured_at)\n")
            L.append("| resource | linking sources | first link | linked ≤ audit_at | observations (captured_at, admissible) |")
            L.append("|---|---|---|---|---|")
            for rid, tr in sorted(crep.get("trace", {}).items()):
                obs = "; ".join(f"{o['file_id']} {o['captured_at']} {'✓' if o['admissible'] else '✗ excluded'}"
                                for o in tr["observations"]) or "–"
                L.append(f"| {rid} | {', '.join(tr['sources'])} | {tr['first_link']} | {tr['admissible_link']} | {obs} |")
            L.append("\n### 5. Per-resource state (R4) and rule fired\n")
            L.append("| resource | state at audit_at | decision | rule |")
            L.append("|---|---|---|---|")
            for rid, dec in sorted(crep["resources"].items()):
                tr = crep.get("trace", {}).get(rid, {})
                st = tr.get("state")
                if isinstance(dec, str):        # skipped before state evaluation (R15 / R3 / R16)
                    sdesc = f"not evaluated ({dec.split(':')[0]})"
                else:
                    sdesc = None
                sdesc = sdesc or ("no admissible observation" if st is None else ", ".join(
                    f"{k}={v}" for k, v in st.items() if k != "hints" and v not in (None, [], False)) or "present=False")
                d = dec if isinstance(dec, str) else " → ".join(dec)
                L.append(f"| {rid} | {sdesc} | {d} | {rule_fired(rid.rsplit('_', 1)[0], dec, tr)} |")
        L.append(f"\n### 6. Output: `{status}`\n")
        L.append("| step | phase | system_id | resource_id | operation | state | evidence_id |")
        L.append("|---|---|---|---|---|---|---|")
        for x in steps:
            L.append(f"| {x['step_no']} | {x['phase']} | {x['system_id']} | {x['resource_id']} | {x['operation']} | "
                     f"{x['state']} | {x['evidence_id'] or '\"\"'} |")
        if not steps:
            L.append("| – | | | | `[]` | | |")
        with tempfile.TemporaryDirectory() as td:
            inp, out = Path(td) / "in.csv", Path(td) / "out.csv"
            with open(inp, "w", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=list(req))
                w.writeheader()
                w.writerow(req)
            with open(out, "w", newline="", encoding="utf-8") as fh:
                csv.writer(fh).writerows([["case_id", "deletion_status", "steps_json"],
                                          [cid, status, json.dumps(steps, separators=(",", ":"))]])
            errs = validate(out, inp, data_dir)
        hard = [e for e in errs if "(warning)" not in e]
        L.append(f"\n### 7. Validator\n\n- {len(hard)} errors, {len(errs) - len(hard)} warnings"
                 + "".join(f"\n- {e}" for e in errs))
        gold = score_sample.gold_case(cid)
        if gold is not None:
            key = lambda x: (x["step_no"], x["phase"], x["system_id"], x["resource_id"], x["operation"], x["state"], x["evidence_id"])  # noqa: E731
            gk, pk = set(map(key, gold[1])), set(map(key, steps))
            L.append(f"\n### 8. Diff vs gold\n\n- status: gold `{gold[0]}`, predicted `{status}`")
            L.append(f"- steps: {'identical (all 7 fields, same order)' if gold[1] == steps else 'DIFFERENT'}")
            for k in sorted(gk - pk):
                L.append(f"  - missing: {k}")
            for k in sorted(pk - gk):
                L.append(f"  - extra: {k}")
    # the trace never writes the intent cache (force_live answers are not saved)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {out_md} (calls {llm.usage['calls']}, input {llm.usage['input_tokens']}, output {llm.usage['output_tokens']})")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--input", default=str(ROOT / "dataset" / "deletion_requests.csv"))
    ap.add_argument("--out", default=str(ROOT / "output.csv"))
    ap.add_argument("--data-dir", default=str(ROOT / "dataset"))
    ap.add_argument("--refresh-media", action="store_true", help="re-extract media live (needs a key), rewriting the cache")
    ap.add_argument("--trace", nargs="+", metavar="CASE_ID", help="write a golden trace for these cases instead of a run")
    ap.add_argument("--trace-out", default=str(ROOT / "code" / "docs" / "GOLDEN_TRACE.md"))
    a = ap.parse_args()
    if a.trace:
        write_trace(a.trace, Path(a.trace_out), Path(a.data_dir))
        return
    run(Path(a.input), Path(a.out), Path(a.data_dir), refresh_media=a.refresh_media)


if __name__ == "__main__":
    main()
