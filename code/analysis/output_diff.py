"""Diff two output.csv files: list every case whose status or steps changed (dev aid).

    python3 code/analysis/output_diff.py scratch/output_before.csv output.csv
"""
import csv
import json
import sys


def load(p):
    return {r["case_id"]: (r["deletion_status"], json.loads(r["steps_json"])) for r in csv.DictReader(open(p, encoding="utf-8"))}


def key(s):
    return (s["phase"], s["system_id"], s["resource_id"], s["operation"], s["state"], s["evidence_id"])


a, b = load(sys.argv[1]), load(sys.argv[2])
changed = [c for c in a if a[c] != b[c]]
print(f"test cases whose status/steps changed: {len(changed)}")
for c in sorted(changed, key=lambda x: int(x.split("_")[1])):
    ka, kb = set(map(key, a[c][1])), set(map(key, b[c][1]))
    st = f"{a[c][0]} -> {b[c][0]}" if a[c][0] != b[c][0] else a[c][0]
    print(f"  {c} [{st}]")
    for k in sorted(ka - kb):
        print(f"     - {' '.join(k[:5])} ev={k[5]!r}")
    for k in sorted(kb - ka):
        print(f"     + {' '.join(k[:5])} ev={k[5]!r}")
