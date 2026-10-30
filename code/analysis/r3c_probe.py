"""R3c probe: per resource family, what does post-audit ownership linking add on the 32 samples?

Read-only; reads sample_output.csv only to score the hypothesis (dev analysis). No API calls (media cache).

    python3 code/analysis/r3c_probe.py > scratch/r3c_probe.txt
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))
import main  # noqa: E402,F401  (loads .env; never prints it)
from agent.intent import deterministic_intent  # noqa: E402
from agent.llm import LLM  # noqa: E402
from engine.loaders import read_csv  # noqa: E402

DATA = ROOT / "dataset"
FAMILIES = ["account", "search", "analytics", "support", "export", "data_flow", "backup", "tombstone",
            "legal_hold", "object", "marketing"]


def core(s):
    return (s["phase"], s["system_id"], s["resource_id"], s["operation"], s["state"])


def main_():
    P = print
    eng, _, _ = main.build_engine(DATA, LLM(), 4)
    samples = read_csv(DATA / "sample_deletion_requests.csv")
    tests = [r for r in read_csv(DATA / "deletion_requests.csv") if deterministic_intent(r["request_text"])["authorizes_deletion"]]
    gold = {r["case_id"]: (r["deletion_status"], json.loads(r["steps_json"])) for r in read_csv(DATA / "sample_output.csv")}

    def run(reqs, fams):
        eng.r3c_families = fams
        return {r["case_id"]: eng.plan(r) for r in reqs}

    base_s, base_t = run(samples, set()), run(tests, set())
    no_acct = lambda res: sum(1 for v in res.values() if not any(s["resource_id"].startswith("account_") for s in v["steps"]))  # noqa: E731
    P(f"{'family':11s} {'explained':>9s} {'FP':>4s} {'ev_agree':>9s} {'status_flips':>12s} {'test_fires':>10s}  verdict")
    detail = []
    adopted = []
    for fam in FAMILIES:
        res_s, res_t = run(samples, {fam}), run(tests, {fam})
        expl, fp, ev_ok, ev_n, flips = [], [], 0, 0, []
        for cid in gold:
            added = {s["resource_id"] for s in res_s[cid]["steps"]} - {s["resource_id"] for s in base_s[cid]["steps"]}
            gst, gsteps = gold[cid]
            gcore = {core(s): s for s in gsteps}
            for rid in sorted(added):
                if rid in {s["resource_id"] for s in gsteps}:
                    expl.append(f"{cid}:{rid}")
                    for s in res_s[cid]["steps"]:
                        if s["resource_id"] == rid and core(s) in gcore:
                            ev_n += 1
                            ev_ok += s["evidence_id"] == gcore[core(s)]["evidence_id"]
                else:
                    fp.append(f"{cid}:{rid}")
            if res_s[cid]["status"] != base_s[cid]["status"]:
                flips.append(f"{cid}:{base_s[cid]['status']}->{res_s[cid]['status']} (gold {gst})")
        fires = [cid for cid in res_t if {s["resource_id"] for s in res_t[cid]["steps"]} != {s["resource_id"] for s in base_t[cid]["steps"]}]
        verdict = "ADOPT" if expl and not fp and not [f for f in flips if not f.endswith(f"(gold {f.split('->')[1].split(' ')[0]})")] else "REJECT"
        if verdict == "ADOPT":
            adopted.append(fam)
        P(f"{fam:11s} {len(expl):9d} {len(fp):4d} {f'{ev_ok}/{ev_n}':>9s} {len(flips):12d} {len(fires):10d}  {verdict}")
        detail.append((fam, expl, fp, flips, fires))
    for fam, expl, fp, flips, fires in detail:
        if expl or fp or flips or fires:
            P(f"\n{fam}\n   explained: {expl or '-'}\n   FP: {fp or '-'}\n   status flips: {flips or '-'}\n   test fires ({len(fires)}): {fires[:25]}")
    P(f"\nadopted families: {adopted}")
    res_t_all = run(tests, set(adopted))
    P(f"R17 test (authorized test cases with no account step): before {no_acct(base_t)} after {no_acct(res_t_all)}")
    res_s_all = run(samples, set(adopted))
    for cid in ("case_09", "case_26", "case_27"):
        acc = [s for s in res_s_all[cid]["steps"] if s["resource_id"].startswith("account_")]
        gacc = [s for s in gold[cid][1] if s["resource_id"].startswith("account_")]
        P(f"   {cid}: predicted {[(s['resource_id'], s['operation'], s['evidence_id']) for s in acc]} | "
          f"gold {[(s['resource_id'], s['operation'], s['evidence_id']) for s in gacc]}")


if __name__ == "__main__":
    main_()
