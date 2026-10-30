"""Media extraction agent (P4): the model transcribes PNG screenshots and PDF pages into records;
code owns everything after extraction (R2-R16).

Per file: one bounded tool loop (step cap 3) ending in the strict tool submit_media_records.
First attempt: forced tool_choice {"type":"tool"} with thinking disabled. Current models reject that
with HTTP 400, so the extractor switches once to tool_choice "auto" + strict schema + a submit nudge and
records which mode worked (self.mode).
Cache: code/cache/media/<sha256(file)>_<prompt_hash>.json (shipped). A prompt change invalidates it.
No key and no cache hit -> the file is skipped and reported as media_unread.
"""
from __future__ import annotations

import base64
import hashlib
import json
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))
from agent.llm import LLM, prompt_hash  # noqa: E402
from prompts import MEDIA_PROMPT_VERSION, MEDIA_SUBMIT_NUDGE, MEDIA_SYSTEM  # noqa: E402

CACHE_DIR = ROOT / "code" / "cache" / "media"
MAX_STEPS = 3
RECORD_TYPES = ["USER_PROFILE", "SEARCH_INDEX_ENTRY", "ANALYTICS_PROFILE", "SUPPORT_MESSAGE", "SUPPORT_ATTACHMENT",
                "USER_EXPORT", "DATA_FLOW", "BACKUP_ARCHIVE", "SECURITY_AUDIT_LOG", "ACCOUNT_TOMBSTONE",
                "LEGAL_HOLD_RECORD", "MARKETING_PROFILE", "ORDER_OR_FINANCE_RECORD", "OTHER"]
NSTR = {"type": ["string", "null"]}
SUBMIT_TOOL = {
    "name": "submit_media_records", "strict": True,
    "description": "Submit every record transcribed from the artefact. Call exactly once.",
    "input_schema": {
        "type": "object", "additionalProperties": False, "required": ["records", "unreadable_fields"],
        "properties": {
            "unreadable_fields": {"type": "array", "items": {"type": "string"}},
            "records": {"type": "array", "items": {
                "type": "object", "additionalProperties": False,
                "required": ["resource_id", "record_type", "system_hint", "identifiers", "status_fields",
                             "timestamps", "other_references"],
                "properties": {
                    "resource_id": NSTR,
                    "record_type": {"type": "string", "enum": RECORD_TYPES},
                    "system_hint": {"type": "string"},
                    "identifiers": {"type": "object", "additionalProperties": False,
                                    "required": ["email", "phone", "email_hash", "user_id", "name"],
                                    "properties": {k: NSTR for k in ("email", "phone", "email_hash", "user_id", "name")}},
                    "status_fields": {"type": "array", "items": {
                        "type": "object", "additionalProperties": False, "required": ["name", "value"],
                        "properties": {"name": {"type": "string"}, "value": {"type": "string"}}}},
                    "timestamps": {"type": "array", "items": {"type": "string"}},
                    "other_references": {"type": "array", "items": {"type": "string"}},
                }}},
        }}}
PROMPT_HASH = prompt_hash(MEDIA_PROMPT_VERSION, MEDIA_SYSTEM, SUBMIT_TOOL, MEDIA_SUBMIT_NUDGE)


def _pdf_blocks(path: Path):
    import fitz  # PyMuPDF: text layer + page renders
    doc = fitz.open(str(path))
    text = "\n".join(p.get_text() for p in doc)
    blocks = [{"type": "text", "text": f"PDF text layer ({doc.page_count} pages):\n{text}"}]
    has_table = sum("|" in ln for ln in text.splitlines()) >= 2
    if not has_table:   # key/value layouts lose their structure in the text layer: add page images
        for page in doc:
            png = page.get_pixmap(dpi=110).tobytes("png")
            blocks.append({"type": "image", "source": {"type": "base64", "media_type": "image/png",
                                                       "data": base64.b64encode(png).decode()}})
    return blocks


class MediaExtractor:
    def __init__(self, llm: LLM):
        self.llm = llm
        self.mode = None          # "forced_tool" | "auto_strict_nudge", decided by the first live call
        self.lock = threading.Lock()
        self.stats = {"cache": 0, "live": 0, "unread": 0, "failed": 0}

    def cache_path(self, path: Path) -> Path:
        return CACHE_DIR / f"{hashlib.sha256(path.read_bytes()).hexdigest()}_{PROMPT_HASH}.json"

    def extract(self, fid: str, path: Path, kind: str, refresh: bool = False) -> dict:
        """refresh=True (--refresh-media) skips the cache read and re-extracts live (still writes the cache)."""
        cp = self.cache_path(path)
        if cp.exists() and not (refresh and self.llm.live):
            with self.lock:
                self.stats["cache"] += 1
            return {**json.loads(cp.read_text(encoding="utf-8")), "path": "cache"}
        if not self.llm.live:
            with self.lock:
                self.stats["unread"] += 1
            return {"records": [], "unreadable_fields": [], "path": "media_unread"}
        try:
            out = self._run(path, kind)
        except Exception as exc:
            print(f"[media] {fid} failed: {exc.__class__.__name__}", file=sys.stderr)
            out = None
        if out is None:
            with self.lock:
                self.stats["failed"] += 1
            return {"records": [], "unreadable_fields": [], "path": "media_unread"}
        out["file"] = path.name
        out["mode"] = self.mode
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cp.write_text(json.dumps(out, indent=1, ensure_ascii=False, sort_keys=True), encoding="utf-8")
        with self.lock:
            self.stats["live"] += 1
        return {**out, "path": "live"}

    def _content(self, path, kind):
        if kind == "png":
            return [{"type": "image", "source": {"type": "base64", "media_type": "image/png",
                                                 "data": base64.b64encode(path.read_bytes()).decode()}}]
        return _pdf_blocks(path)

    def _call(self, messages):
        if self.mode in (None, "forced_tool"):
            try:
                resp = self.llm.create(role="media", max_tokens=8000, system=MEDIA_SYSTEM, tools=[SUBMIT_TOOL],
                                       tool_choice={"type": "tool", "name": "submit_media_records"},
                                       thinking={"type": "disabled"}, messages=messages)
                with self.lock:
                    self.mode = "forced_tool"
                return resp
            except self.llm.anthropic.BadRequestError:
                with self.lock:
                    self.mode = "auto_strict_nudge"
        return self.llm.create(role="media", max_tokens=16000, system=MEDIA_SYSTEM, tools=[SUBMIT_TOOL],
                               tool_choice={"type": "auto"}, messages=messages)

    def _run(self, path, kind):
        messages = [{"role": "user", "content": self._content(path, kind) + [
            {"type": "text", "text": f"Artefact file: {path.name}. {MEDIA_SUBMIT_NUDGE}"}]}]
        for _ in range(MAX_STEPS):
            resp = self._call(messages)
            if resp.stop_reason == "refusal":
                return None
            for b in resp.content:
                if b.type == "tool_use" and b.name == "submit_media_records":
                    inp = b.input if isinstance(b.input, dict) else json.loads(b.input)
                    return {"records": inp["records"], "unreadable_fields": inp["unreadable_fields"]}
            messages.append({"role": "assistant", "content": resp.content})
            messages.append({"role": "user", "content": MEDIA_SUBMIT_NUDGE})
        return None
