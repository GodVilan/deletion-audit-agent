"""Output validator: SPEC_CARD §3/§4 invariants I1-I10. Fails loudly (non-zero exit) on any violation.

    python3 code/engine/validate.py output.csv [--input dataset/deletion_requests.csv] [--evidence-dir dataset]
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine.rules import OP_ORDER, OPS, PHASE_RANK  # noqa: E402

FIELDS = {"step_no", "phase", "system_id", "resource_id", "operation", "state", "evidence_id"}
STATUSES = {"COMPLETE", "INCOMPLETE", "NOT_APPLICABLE"}


def validate(out_path: Path, input_path: Path, data_dir: Path) -> list[str]:
    errs = []
    with open(out_path, newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        header = next(reader)
        rows = [dict(zip(header, r)) for r in reader]
    if header != ["case_id", "deletion_status", "steps_json"]:
        errs.append(f"I1 header {header}")
    inputs = [r["case_id"] for r in csv.DictReader(open(input_path, newline="", encoding="utf-8"))]
    got = [r["case_id"] for r in rows]
    if sorted(got) != sorted(inputs) or len(set(got)) != len(got):
        errs.append(f"I1 case ids: {len(got)} rows vs {len(inputs)} inputs")
    if got != sorted(got, key=lambda c: int(c.rsplit("_", 1)[1])):
        errs.append("I1 rows not sorted by numeric case_id (SPEC_CARD A1)")
    req = {r["case_id"]: r for r in csv.DictReader(open(input_path, newline="", encoding="utf-8"))}
    ids = {r["file_id"]: r["captured_at"] for r in csv.DictReader(open(data_dir / "evidence_files.csv", encoding="utf-8"))}
    ids.update({r["activity_id"]: r["event_time"] for r in csv.DictReader(open(data_dir / "system_activity.csv", encoding="utf-8"))})
    ids.update({r["audit_id"]: r["event_time"] for r in csv.DictReader(open(data_dir / "user_audit_log.csv", encoding="utf-8"))})
    for r in rows:
        c, st = r["case_id"], r["deletion_status"]
        try:
            steps = json.loads(r["steps_json"])
        except ValueError:
            errs.append(f"{c}: steps_json not JSON")
            continue
        if st not in STATUSES:
            errs.append(f"{c}: status {st}")
        if not isinstance(steps, list):
            errs.append(f"{c}: steps not a list")
            continue
        if st == "NOT_APPLICABLE" and steps != []:
            errs.append(f"{c}: I2 NOT_APPLICABLE => []")
        if st != "NOT_APPLICABLE" and steps == []:
            errs.append(f"{c}: I2 (warning) authorized case with no steps (sample-inferred direction; R17)")
        for i, s in enumerate(steps, 1):
            if set(s) != FIELDS:
                errs.append(f"{c} step {i}: fields {sorted(s)}")
                continue
            if s["step_no"] != i:
                errs.append(f"{c} step {i}: I5 step_no {s['step_no']}")
            if s["operation"] not in OPS or OPS[s["operation"]] != (s["phase"], s["state"]):
                errs.append(f"{c} step {i}: I7 op/phase/state {s['operation']}/{s['phase']}/{s['state']}")
            ev = s["evidence_id"]
            if st == "COMPLETE" and (s["phase"] != "VERIFICATION" or ev not in ids):
                errs.append(f"{c} step {i}: I3 COMPLETE step must be VERIFICATION citing a valid id ({ev!r})")
            if st == "INCOMPLETE":
                if s["phase"] == "FINDING" and ev not in ids:
                    errs.append(f"{c} step {i}: I4 finding without valid evidence ({ev!r})")
                if s["phase"] != "FINDING" and ev != "":
                    errs.append(f"{c} step {i}: I4 future step must have empty evidence")
            if ev and ev in ids and ids[ev] > req[c]["audit_at"]:
                errs.append(f"{c} step {i}: I8 cites {ev} after audit_at")
        if st == "INCOMPLETE" and not any(s.get("phase") == "FINDING" for s in steps):
            errs.append(f"{c}: I4 INCOMPLETE without a finding")
        keys = [(PHASE_RANK.get(s.get("phase"), 9), OP_ORDER.index(s["operation"]) if s.get("operation") in OP_ORDER else 99,
                 s.get("system_id"), s.get("resource_id")) for s in steps]
        if keys != sorted(keys):
            errs.append(f"{c}: I6 ordering")
        if st != "NOT_APPLICABLE" and not any(s.get("operation") == "VERIFY_RECORD_ABSENT"
                                              and s.get("system_id") == "account_service" for s in steps):
            errs.append(f"{c}: I10 (warning) no account VERIFY_RECORD_ABSENT")
    return errs


def main(argv=None):
    root = Path(__file__).resolve().parents[2]
    ap = argparse.ArgumentParser()
    ap.add_argument("output", nargs="?", default=str(root / "output.csv"))
    ap.add_argument("--input", default=str(root / "dataset" / "deletion_requests.csv"))
    ap.add_argument("--data-dir", default=str(root / "dataset"))
    a = ap.parse_args(argv)
    errs = validate(Path(a.output), Path(a.input), Path(a.data_dir))
    hard = [e for e in errs if "(warning)" not in e]
    warn = [e for e in errs if "(warning)" in e]
    print(f"validator: {len(hard)} errors, {len(warn)} warnings")
    for e in hard[:50]:
        print("  ERROR", e)
    if warn:
        print(f"  WARN  {len(warn)} warnings (I10 no account verify / I2 empty authorized case; LABEL_CONVENTIONS R17)")
    sys.exit(1 if hard else 0)


if __name__ == "__main__":
    main()
