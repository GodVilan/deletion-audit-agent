"""Audit log.txt against AGENTS.md §5 (read-only).

Counts entries; entries missing an exact tool=/model= line; turn entries whose prompt field is empty,
abbreviated (bracketed placeholder) or path-only; and whether a later correction entry covers them.

    python3 code/analysis/log_audit.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL, MODEL = "tool=Claude Code", "model=claude-opus-5-5"


def main():
    text = (ROOT / "log.txt").read_text(encoding="utf-8")
    entries = re.split(r"(?m)^(?=## \[\d{4}-\d\d-\d\dT[\d:]+Z\] )", text)
    entries = [e for e in entries if e.startswith("## [")]
    starts = [e for e in entries if " SESSION START" in e.splitlines()[0]]
    turns = [e for e in entries if e not in starts]
    bad_tm = [e.splitlines()[0] for e in entries
              if e.count(f"\n{TOOL}\n") + e.count(f"\n{TOOL}") != 1 and not re.search(rf"(?m)^{re.escape(TOOL)}$", e)
              or len(re.findall(r"(?m)^tool=", e)) != 1 or len(re.findall(r"(?m)^model=", e)) != 1
              or not re.search(rf"(?m)^{re.escape(TOOL)}$", e) or not re.search(rf"(?m)^{re.escape(MODEL)}$", e)]
    problems = []
    for e in turns:
        head = e.splitlines()[0]
        m = re.search(r"User Prompt \(verbatim[^)]*\):\n(.*?)\n\nAgent Response Summary:", e, re.S)
        if not m:
            problems.append((head, "no prompt field"))
            continue
        p = m.group(1).strip()
        if not p:
            problems.append((head, "empty"))
        elif re.match(r"^\[.*(abbreviat|verbatim in|Full text is in|preserved in|not duplicated).*\]$", p, re.S) or \
                re.search(r"\[(The participant's full SPEC_CARD draft|Two pasted blocks)[^\]]*\]", p):
            problems.append((head, "abbreviated/path-only"))
    print(f"log.txt entries: {len(entries)} (SESSION START {len(starts)}, turn entries {len(turns)})")
    print(f"entries missing/duplicating an exact '{TOOL}' or '{MODEL}' line: {len(bad_tm)}")
    for h in bad_tm:
        print(f"   {h}")
    print(f"turn entries with an empty / abbreviated / path-only prompt: {len(problems)}")
    corrections = [e.splitlines()[0] for e in turns if "CORRECTION" in e.splitlines()[0]]
    for h, why in problems:
        stamp = re.search(r"\[(.*?)\]", h).group(1)
        covered = [c for c in corrections if stamp in c or ("P4" in c and "P4:" in h)]
        print(f"   {h}  [{why}]  -> corrected by: {covered or 'NONE'}")
    print(f"correction entries: {len(corrections)}")
    sys.exit(1 if bad_tm or any(not [c for c in corrections if re.search(r'\[(.*?)\]', h).group(1) in c or ('P4' in c and 'P4:' in h)] for h, _ in problems) else 0)


if __name__ == "__main__":
    main()
