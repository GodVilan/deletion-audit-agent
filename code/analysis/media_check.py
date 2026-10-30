"""Dev check: model media extraction (code/cache/media) vs the hand transcription in scratch/media_transcripts.md.

Dev only. The pipeline never reads the transcripts. Compares, per file:
  resource_ids  - every resource id in the model output vs the transcript (exact)
  identifiers   - emails, phones, 64-hex hashes, user_ids (exact strings as printed)
  status fields - each model status value must appear verbatim in the transcript section
Transcript lines that are my analysis (Links / State flags / Internal oddity) are excluded.

    python3 code/analysis/media_check.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))
from agent.media import CACHE_DIR, PROMPT_HASH  # noqa: E402
from engine.loaders import EMAIL_RE, HASH_RE, read_csv  # noqa: E402

RID_RE = re.compile(r"\b(?:account|search|analytics|support|export|data_flow|backup|audit_record|tombstone|"
                    r"legal_hold|object|marketing)_\d+\b")
PHONE_RE = re.compile(r"\+\d[\d \-]{6,}\d")
USER_RE = re.compile(r"\buser_\d+\b")
ANALYSIS = ("- Links", "- State flags", "- Internal oddity", "- No resource_id")


def sections(md: str) -> dict:
    out, cur = {}, None
    for line in md.splitlines():
        m = re.match(r"^### (evidence_\d+)", line)
        if m:
            cur = m.group(1)
            out[cur] = []
            continue
        if line.startswith("## "):
            cur = None
        if cur and not line.strip().startswith(ANALYSIS):
            out[cur].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def ids(text: str) -> dict:
    return {"resource_ids": set(RID_RE.findall(text)), "emails": set(EMAIL_RE.findall(text)),
            "phones": {p.strip() for p in PHONE_RE.findall(text)}, "hashes": set(HASH_RE.findall(text)),
            "user_ids": set(USER_RE.findall(text))}


def main():
    md = (ROOT / "scratch" / "media_transcripts.md").read_text(encoding="utf-8")
    secs = sections(md)
    manifest = {m["file_id"]: ROOT / "dataset" / m["file_path"] for m in read_csv(ROOT / "dataset" / "evidence_files.csv")}
    import hashlib
    tot = {"resource_ids": [0, 0], "identifiers": [0, 0], "status": [0, 0]}
    for fid in sorted(secs):
        cp = CACHE_DIR / f"{hashlib.sha256(manifest[fid].read_bytes()).hexdigest()}_{PROMPT_HASH}.json"
        if not cp.exists():
            print(f"{fid}: NO CACHE ENTRY")
            continue
        out = json.loads(cp.read_text(encoding="utf-8"))
        model_text = json.dumps(out["records"], ensure_ascii=False)
        t, mdl = ids(secs[fid]), ids(model_text)
        lines = []
        for k in ("resource_ids", "emails", "phones", "hashes", "user_ids"):
            miss, extra = t[k] - mdl[k], mdl[k] - t[k]
            bucket = "resource_ids" if k == "resource_ids" else "identifiers"
            tot[bucket][0] += len(t[k] & mdl[k])
            tot[bucket][1] += len(t[k] | mdl[k])
            if miss or extra:
                lines.append(f"   {k}: missing={sorted(miss)} extra={sorted(extra)}")
        sv = [(sf["name"], sf["value"]) for r in out["records"] for sf in r["status_fields"]]
        bad = [f"{n}={v}" for n, v in sv if v not in secs[fid]]
        tot["status"][0] += len(sv) - len(bad)
        tot["status"][1] += len(sv)
        ok_ids = not any("resource_ids" in ln for ln in lines)
        ok_idf = not any(k in ln for ln in lines for k in ("emails", "phones", "hashes", "user_ids"))
        print(f"{fid}: records={len(out['records'])} resource_ids={'EXACT' if ok_ids else 'DIFF'} "
              f"identifiers={'EXACT' if ok_idf else 'DIFF'} status_values_verbatim={len(sv) - len(bad)}/{len(sv)}")
        for ln in lines:
            print(ln)
        for b in bad:
            print(f"   status not verbatim in transcript: {b}")
    print("\nTOTAL (matched / union):")
    for k, (a, b) in tot.items():
        print(f"   {k}: {a}/{b} = {a / b:.1%}" if b else f"   {k}: n/a")


if __name__ == "__main__":
    main()
