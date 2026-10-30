"""Shared Claude client: one client, bounded retries with exponential backoff + jitter, usage accounting.

Secrets: the key is read by the SDK from ANTHROPIC_API_KEY; it is never printed or logged.
"""
from __future__ import annotations

import hashlib
import json
import os
import random
import threading
import time

MAX_RETRIES = 5


def prompt_hash(*parts) -> str:
    """Stable hash of every prompt artefact (system text, tool schemas, nudges): part of each cache key."""
    return hashlib.sha256(json.dumps(parts, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]


class LLM:
    """Usage is counted overall and per role ("intent", "media", ...): calls, input/output tokens, retries,
    rejected (HTTP 4xx, not retried, not billed) and errors (retries exhausted)."""

    def __init__(self):
        self.model = os.environ.get("ANTHROPIC_MODEL") or "claude-opus-5-5"
        self.client = None
        self.lock = threading.Lock()
        self.usage = self._blank()
        self.by_role: dict[str, dict] = {}
        if os.environ.get("ANTHROPIC_API_KEY"):
            try:
                import anthropic
                self.anthropic = anthropic
                self.client = anthropic.Anthropic(max_retries=0)   # retries are ours (counted, jittered)
            except Exception as exc:
                print(f"[llm] anthropic SDK unavailable ({exc.__class__.__name__}); fallback paths only")

    @staticmethod
    def _blank():
        return {"calls": 0, "input_tokens": 0, "output_tokens": 0, "retries": 0, "rejected": 0, "errors": 0}

    def _count(self, role: str, key: str, n: int = 1):
        with self.lock:
            self.usage[key] += n
            self.by_role.setdefault(role, self._blank())[key] += n

    @property
    def live(self) -> bool:
        return self.client is not None

    def create(self, role: str = "other", **kwargs):
        """messages.create with up to MAX_RETRIES retries on 429 / 5xx / overloaded / connection errors."""
        a = self.anthropic
        for attempt in range(MAX_RETRIES + 1):
            try:
                resp = self.client.messages.create(model=self.model, **kwargs)
                self._count(role, "calls")
                self._count(role, "input_tokens", resp.usage.input_tokens)
                self._count(role, "output_tokens", resp.usage.output_tokens)
                return resp
            except (a.RateLimitError, a.InternalServerError, a.APIConnectionError) as exc:
                err = exc
            except a.APIStatusError as exc:
                if exc.status_code not in (408, 409, 429, 529) and exc.status_code < 500:
                    self._count(role, "rejected")
                    raise
                err = exc
            if attempt == MAX_RETRIES:
                self._count(role, "errors")
                raise err
            self._count(role, "retries")
            time.sleep(min(30.0, 2 ** attempt) * (0.5 + random.random()))
