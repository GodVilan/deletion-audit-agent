"""R1 intent agent: a bounded tool-using Claude agent with a deterministic fallback.

Tools are read-only (get_request_text, get_classify_rows) plus submit_intent. Current Claude models reject
forced tool_choice ("any"/"tool"), so submission is enforced with tool_choice "auto", strict tool schemas,
an explicit instruction, and a final-turn nudge; a run that never submits falls back to the deterministic
classifier. Step cap 4. Model from ANTHROPIC_MODEL (default claude-opus-5-5). Results are cached in
scratch/intent_cache.json (not shipped) keyed by (sha256(request text), prompt_hash, model).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))
from agent.llm import LLM, prompt_hash  # noqa: E402
from prompts import FINAL_TURN_NUDGE, INTENT_SYSTEM, PROMPT_VERSION  # noqa: E402

CACHE_PATH = Path(os.environ.get("INTENT_CACHE_PATH") or ROOT / "scratch" / "intent_cache.json")
MAX_STEPS = 4

DELETE_KW = re.compile(
    r"delet|eras|remov|close (?:my|this|the) account|close this account|permanent|erasure|forget|"
    r"profile is gone|account is gone|cannot identify me|can no longer identify|"
    r"supprim|suppression|eliminar|eliminación|borrar|lösch|entfern|cancellare|eliminare|"
    r"excluir|exclusão|apagar|verwijder|usuń|削除|삭제|删除|注销|退会|탈퇴|удал", re.I)
NEGATION = re.compile(
    r"\bnot\b[^.]{0,40}\b(?:delet|eras|remov|clos)|don't (?:delete|close|remove|erase)|do not (?:delete|close|remove|erase)|"
    r"without (?:delet|remov|eras)|no deletion|marketing[^.]{0,20}\bonly\b|keep the account|leave (?:the|my) "
    r"(?:account|profile)|continue using|still (?:need|use|want)", re.I)


def deterministic_intent(text: str) -> dict:
    """Negation-aware keyword classifier (fallback path). Full scan of 375 distinct test texts: it flags
    exactly the 10 non-deletion texts and no deletion request (scratch/audit_out.txt §e)."""
    has_del = bool(DELETE_KW.search(text))
    neg = bool(NEGATION.search(text))
    ok = has_del and not neg
    return {"authorizes_deletion": ok, "scope": "account" if ok else "none",
            "rationale": f"deletion_keyword={has_del} negation_or_keep={neg}", "path": "fallback"}


TOOLS = [
    {"name": "get_request_text", "description": "Return the request_text of the case being classified.",
     "strict": True, "input_schema": {"type": "object", "properties": {}, "required": [], "additionalProperties": False}},
    {"name": "get_classify_rows", "description": "Return CLASSIFY_REQUEST activity rows linked to this requester (intake claims).",
     "strict": True, "input_schema": {"type": "object", "properties": {}, "required": [], "additionalProperties": False}},
    {"name": "submit_intent", "description": "Submit the final decision. Call exactly once.", "strict": True,
     "input_schema": {"type": "object", "additionalProperties": False,
                      "required": ["authorizes_deletion", "scope", "rationale"],
                      "properties": {"authorizes_deletion": {"type": "boolean"},
                                     "scope": {"type": "string", "enum": ["account", "partial", "none"]},
                                     "rationale": {"type": "string"}}}},
]


class IntentClassifier:
    """Thread-safe. Cache key = (sha256(request text), prompt_hash, model); legacy keys are migrated on read."""

    PROMPT_HASH = prompt_hash(INTENT_SYSTEM, TOOLS, FINAL_TURN_NUDGE)

    def __init__(self, llm: LLM | None = None):
        self.llm = llm or LLM()
        self.model = self.llm.model
        self.client = self.llm.client
        self.lock = threading.Lock()
        self.stats = {"cache_hits": 0, "live": 0, "fallback": 0, "agent_failed": 0}
        try:
            self.cache = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            self.cache = {}

    @property
    def usage(self):
        return self.llm.usage

    def _key(self, text):
        return f"{hashlib.sha256(text.encode()).hexdigest()}:{self.PROMPT_HASH}:{self.model}"

    def _legacy_key(self, text):
        return hashlib.sha256(f"{PROMPT_VERSION}|{self.model}|{text}".encode()).hexdigest()

    def classify(self, text: str, classify_rows: list[dict], force_live: bool = False, trace: list | None = None) -> dict:
        """force_live bypasses the cache (used by --trace); trace collects the tool calls for the golden trace."""
        fb = deterministic_intent(text)
        if self.client is None:
            with self.lock:
                self.stats["fallback"] += 1
            return {**fb, "fallback": fb}
        k = self._key(text)
        with self.lock:
            hit = None if force_live else (self.cache.get(k) or self.cache.get(self._legacy_key(text)))
            if hit is not None:
                self.cache[k] = hit
                self.stats["cache_hits"] += 1
                return {**hit, "path": "agent(cache)", "fallback": fb}
        try:
            out = self._run_agent(text, classify_rows, trace)
        except Exception as exc:
            out = None
            print(f"[intent] agent error {exc.__class__.__name__}: falling back", file=sys.stderr)
        if out is None:
            with self.lock:
                self.stats["agent_failed"] += 1
            return {**fb, "path": "fallback(agent_failed)", "fallback": fb}
        with self.lock:
            self.cache[k] = out
            self.stats["live"] += 1
        return {**out, "path": "agent", "fallback": fb}

    def _run_agent(self, text, classify_rows, trace=None):
        messages = [{"role": "user", "content": "Classify the current case's request."}]
        for step in range(MAX_STEPS):
            resp = self.llm.create(role="intent", max_tokens=2048, system=INTENT_SYSTEM, tools=TOOLS,
                                   tool_choice={"type": "auto"}, output_config={"effort": "low"}, messages=messages)
            if resp.stop_reason == "refusal":
                return None
            messages.append({"role": "assistant", "content": resp.content})
            results = []
            for b in resp.content:
                if b.type != "tool_use":
                    continue
                if trace is not None:
                    trace.append({"step": step + 1, "tool": b.name, "input": b.input})
                if b.name == "submit_intent":
                    inp = b.input if isinstance(b.input, dict) else json.loads(b.input)
                    return {"authorizes_deletion": bool(inp["authorizes_deletion"]), "scope": inp["scope"],
                            "rationale": inp["rationale"][:300]}
                payload = text if b.name == "get_request_text" else json.dumps(classify_rows)
                results.append({"type": "tool_result", "tool_use_id": b.id, "content": payload})
            if results:
                content = results + ([{"type": "text", "text": FINAL_TURN_NUDGE}] if step >= MAX_STEPS - 2 else [])
                messages.append({"role": "user", "content": content})
            else:
                messages.append({"role": "user", "content": FINAL_TURN_NUDGE})
        return None

    def save(self):
        if self.client is None:
            return
        try:
            CACHE_PATH.parent.mkdir(exist_ok=True)
            with self.lock:
                CACHE_PATH.write_text(json.dumps(self.cache, indent=0, sort_keys=True), encoding="utf-8")
        except OSError:
            pass
