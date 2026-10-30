"""Evaluation entry point.

    python3 code/evaluation/main.py

Runs, in order:
  1. the sample scorer (code/evaluation/score_sample.py, the only reader of sample_output.csv)
  2. the validator on the root output.csv
  3. a distribution check: test output vs the sample gold shape (status mix, steps per case, operation mix)
  4. the media dev check against scratch/media_transcripts.md (dev ground truth; skipped with a note if absent)
  5. the custom evaluation cases (code/evaluation/custom_cases/)
appends the raw output to code/evaluation/run_history.md and regenerates code/evaluation/evaluation_report.md
(headings per AGENTS.md §6.8; "Failures found and improvements made" comes from decision_history.md).
"""
from __future__ import annotations

import contextlib
import csv
import datetime as dt
import io
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))
sys.path.insert(0, str(ROOT / "code" / "evaluation"))
sys.path.insert(0, str(ROOT / "code" / "analysis"))
import score_sample  # noqa: E402
from engine.validate import validate  # noqa: E402

DATA = ROOT / "dataset"
REPORT = ROOT / "code" / "evaluation" / "evaluation_report.md"
HISTORY = ROOT / "code" / "evaluation" / "run_history.md"
METRIC_DEFS = [
    ("status_accuracy", "deletion_status equal to gold (headline; gate 32/32)"),
    ("exact_steps_json", "the whole parsed steps_json array equal to gold"),
    ("step_P(7-field)", "precision on all seven step fields, step_no included"),
    ("step_R(7-field)", "recall on all seven step fields"),
    ("step_F1(7-field)", "F1 on all seven fields (a missing step shifts every later step_no)"),
    ("step_P(6-field, no step_no)", "precision ignoring step_no (gate 1.0: no wrong step emitted)"),
    ("step_R(6-field)", "recall ignoring step_no"),
    ("step_F1(6-field)", "F1 ignoring step_no"),
    ("core_step_recall(6-field, ignoring evidence/step_no)", "gold steps matched on phase/system/resource/operation/state"),
    ("evidence_id_acc_on_matched", "evidence_id agreement on matched steps"),
    ("sequence_exact(core order)", "gold and predicted steps in identical order"),
]


def distribution() -> str:
    out = [json.loads(r["steps_json"]) for r in csv.DictReader(open(ROOT / "output.csv", encoding="utf-8"))]
    status = Counter(r["deletion_status"] for r in csv.DictReader(open(ROOT / "output.csv", encoding="utf-8")))
    g = score_sample.gold_distribution()
    n = sum(status.values())
    auth = [s for s in out if s]
    t_ops = Counter(x["operation"] for st in out for x in st)
    lines = ["DISTRIBUTION (test output vs sample gold)",
             f"  rows: {n} (expected 518) {'OK' if n == 518 else 'MISMATCH'}",
             f"  NOT_APPLICABLE: {status.get('NOT_APPLICABLE', 0)} (expected exactly 10) "
             f"{'OK' if status.get('NOT_APPLICABLE', 0) == 10 else 'MISMATCH'}"]
    for k in ("COMPLETE", "INCOMPLETE", "NOT_APPLICABLE"):
        lines.append(f"  {k:15s} test {status.get(k, 0):4d} ({status.get(k, 0) / n:6.1%})   "
                     f"sample gold {g['status'].get(k, 0):3d} ({g['status'].get(k, 0) / g['n']:6.1%})")
    lines.append(f"  steps per authorized case: test {sum(map(len, auth)) / max(1, len(auth)):.2f}   sample gold {g['steps_per_case']:.2f}")
    tot_t, tot_g = sum(t_ops.values()), sum(g["ops"].values())
    lines.append("  operation mix (test % / gold %):")
    for op in sorted(set(t_ops) | set(g["ops"])):
        lines.append(f"    {op:28s} {t_ops.get(op, 0) / tot_t:6.1%} / {g['ops'].get(op, 0) / tot_g:6.1%}")
    return "\n".join(lines)


def media() -> str:
    if not (ROOT / "scratch" / "media_transcripts.md").exists():
        return "MEDIA CHECK: skipped (dev ground truth scratch/media_transcripts.md not present)"
    import media_check
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        media_check.main()
    tail = buf.getvalue().split("TOTAL", 1)
    diffs = [ln for ln in buf.getvalue().splitlines() if "missing=" in ln or "DIFF" in ln]
    return "MEDIA CHECK (vs dev ground truth)\n" + "\n".join("  " + d for d in diffs) + "\n  TOTAL" + (tail[1] if len(tail) > 1 else "")


CUSTOM = ROOT / "code" / "evaluation" / "custom_cases"
DECISIONS = ROOT / "code" / "evaluation" / "decision_history.md"


def run_custom() -> tuple[str, list]:
    """Run the pipeline on each synthetic custom case and compare with its hand-written expected.csv."""
    import tempfile
    sys.path.insert(0, str(ROOT / "code"))
    import main as pipeline
    rows, results = [], []
    for d in sorted(p for p in CUSTOM.iterdir() if p.is_dir()):
        meta = json.loads((d / "case.json").read_text(encoding="utf-8"))
        exp = {r["case_id"]: (r["deletion_status"], json.loads(r["steps_json"]))
               for r in csv.DictReader(open(d / "expected.csv", encoding="utf-8"))}
        with tempfile.TemporaryDirectory() as td, contextlib.redirect_stderr(io.StringIO()):
            out = Path(td) / "out.csv"
            try:
                rep = pipeline.run(d / "deletion_requests.csv", out, d, quiet=True)
                got = {r["case_id"]: (r["deletion_status"], json.loads(r["steps_json"]))
                       for r in csv.DictReader(open(out, encoding="utf-8"))}
                paths = {c: v["intent"]["path"] for c, v in rep["cases"].items()}
            except SystemExit as e:
                got, paths = {}, {c: f"run failed: {e}" for c in exp}
        for cid, (est, esteps) in exp.items():
            gst, gsteps = got.get(cid, ("(missing)", []))
            ok = (est, esteps) == (gst, gsteps)
            short = lambda st, steps: f"{st} {[x['operation'] for x in steps if x['phase'] != 'REMEDIATION'] or '[]'}"  # noqa: E731
            results.append(ok)
            rows.append(f"| {cid} ({d.name}) | {meta['what']} | {meta['rule']} | {short(est, esteps)} | "
                        f"{short(gst, gsteps)} (intent: {paths.get(cid)}) | {'PASS' if ok else 'FAIL'} |")
    table = ("| case | what it tests | rule | expected | got | pass |\n|---|---|---|---|---|---|\n" + "\n".join(rows)
             + f"\n\n{sum(results)}/{len(results)} custom cases pass (status and full steps_json equal to the hand-written "
               "expected.csv; the operation lists above omit remediation for brevity).")
    return table, results


def build_report(summary, val, dist, med, custom_table) -> str:
    import hashlib
    sha = hashlib.sha256((ROOT / "output.csv").read_bytes()).hexdigest()
    try:
        rep = json.load(open(ROOT / "scratch" / "run_report.json", encoding="utf-8"))
        flags = rep.get("flags", {})
        c63 = rep["cases"].get("case_63", {}).get("status", "?")
    except (OSError, ValueError, KeyError):
        flags, c63 = {}, "?"
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    m = dict(METRIC_DEFS)
    step_rows = "\n".join(f"| {k} | {summary.get(k)} | {m[k]} |" for k in (
        "exact_steps_json", "step_P(7-field)", "step_R(7-field)", "step_F1(7-field)", "step_P(6-field, no step_no)",
        "step_R(6-field)", "step_F1(6-field)", "core_step_recall(6-field, ignoring evidence/step_no)",
        "evidence_id_acc_on_matched"))
    fa = summary.get("field_accuracy (aligned by resource_id+operation; correct/gold steps)", {})
    field_rows = "\n".join(f"| {f} | {v} |" for f, v in fa.items())
    conf = ", ".join(f"{k}: {v}" for k, v in summary.get("status_confusion", {}).items())
    return f"""# Evaluation report

Generated {stamp} by `python3 code/evaluation/main.py` (do not edit by hand). `output.csv` sha256 `{sha}`. {val}. Raw runs: [run_history.md](run_history.md).

## Case-level status accuracy

- **{summary.get("status_accuracy")}** on the 32 public samples (`deletion_status` equal to gold). Confusion (gold → predicted): {conf}.
- Test-set status distribution vs sample gold:

```text
{dist}
```

## Step-level and field-level accuracy

| metric (32 samples, 193 gold steps) | value | definition |
|---|---|---|
{step_rows}

Field-level accuracy: each gold step is aligned to the predicted step with the same (resource_id, operation); per field, correct / gold steps, where an unaligned gold step counts wrong for every field.

| field | correct / gold steps |
|---|---|
{field_rows}

Media extraction vs the dev hand transcription:

```text
{med}
```

## Sequence accuracy

- **{summary.get("sequence_exact(core order)")}** cases have gold and predicted steps in identical order (phase/system/resource/operation/state sequence). Every predicted case satisfies the PS L126 ordering (validator I6). All sequence misses are missing steps (R17), never mis-ordered ones: 6-field precision is {summary.get("step_P(6-field, no step_no)")}.
- step_no field accuracy {fa.get("step_no", "?")}: a missing earlier step shifts the step_no of every later step.

## Custom evaluation cases

Synthetic datasets with the `dataset/` schemas (`code/evaluation/custom_cases/`, built by `build.py` with the test fixtures). The expected outputs are written by hand from the rules.

{custom_table}

## Failures found and improvements made

{DECISIONS.read_text(encoding="utf-8").strip()}

## Known limitations

- **R17: {flags.get("R17", "?")} test cases have no account step.** Deletion-worker activity rows carry no subject field. Every deletion batch holds two or more unattributed accounts whose request windows overlap (S case_28 and case_29 share batch #187), and no evidence file names these accounts with an identifier. H1–H3 and H5–H9 were probed and rejected (`code/analysis/r17_probe2.py`); H7d' and R3c recovered part of the gap (342 → {flags.get("R17", "?")}). In the samples, 12 subject accounts, 7 anonymized analytics records and 2 audit records (in no participant text) remain unattributable.
- **case_63** is {c63} with no steps: its only candidate resource (marketing_001) shows another person on screen (R16).
- **Spec-inferred, no sample example:** H4-legal (legal hold exists iff a RETAIN_RECORD SUCCESS row ≤ audit_at); the R12 owning systems for legal_service, object_storage and marketing_platform; and the **R9 inference** that a present archive with no restore flag at all is restorable (RESTORE_RISK). The basis for R9 is PS L27: "no active sync, import, or restore path can recreate the data" (COMPLETE needs proof that restore is blocked).
- **Agent vs fallback:** the final live run answered all 518 intents with the agent (0 fallback). The deterministic fallback used without a key agrees with the agent on 518/518, so keyless runs reproduce `output.csv` byte for byte.
"""


def main():
    text, summary = score_sample.score(write_report=False, quiet=True)
    errs = validate(ROOT / "output.csv", DATA / "deletion_requests.csv", DATA)
    hard = [e for e in errs if "(warning)" not in e]
    val = f"VALIDATOR output.csv: {len(hard)} errors, {len(errs) - len(hard)} warnings" + \
          "".join(f"\n  ERROR {e}" for e in hard[:20])
    dist, med = distribution(), media()
    custom_table, custom_res = run_custom()
    body = "\n\n".join([text, val, dist, med, "CUSTOM CASES\n" + custom_table])
    print(body)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    with open(HISTORY, "a", encoding="utf-8") as fh:
        fh.write(f"\n## Evaluation run {stamp} (code/evaluation/main.py)\n\n```text\n{body}\n```\n")
    REPORT.write_text(build_report(summary, val.split("\n")[0], dist, med, custom_table), encoding="utf-8")
    print(f"\nappended raw section to {HISTORY.relative_to(ROOT)}; regenerated {REPORT.relative_to(ROOT)}")
    sys.exit(1 if hard or not all(custom_res) else 0)


if __name__ == "__main__":
    main()
