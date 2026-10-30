"""Synthetic fixtures for the rule tests. Nothing here reads dataset/: each test builds a tiny world."""
from __future__ import annotations

import csv
import json
import os
import sys
from pathlib import Path

import pytest

CODE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE))
os.environ["ANTHROPIC_API_KEY"] = ""   # tests never call the API (load_dotenv does not override this)

USERS = [
    {"user_id": "user_1", "name": "Alice Ark", "email": "alice@ex.com", "phone": "+1 555 0100 001",
     "email_hash": "a" * 64, "updated_at": "2026-01-01T00:00:00Z"},
    {"user_id": "user_2", "name": "Bob Bay", "email": "bob@ex.com", "phone": "+1 555 0100 002",
     "email_hash": "b" * 64, "updated_at": "2026-01-01T00:00:00Z"},
    {"user_id": "user_7", "name": "Gina Gold", "email": "gina@ex.com", "phone": "+1 555 0100 007",
     "email_hash": "c" * 64, "updated_at": "2026-01-01T00:00:00Z"},
]
AUDIT = [{"audit_id": "audit_1", "user_id": "user_1", "event_time": "2025-12-01T00:00:00Z", "field_name": "email",
          "old_value": "old.alice@ex.com", "new_value": "alice@ex.com"}]
FAMILIES = ["account", "search", "analytics", "support", "export", "data_flow", "backup", "audit_record",
            "tombstone", "legal_hold", "object", "marketing"]


def _write_csv(path: Path, rows: list[dict], header: list[str]):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=header)
        w.writeheader()
        w.writerows(rows)


class World:
    """Builds a minimal dataset directory: identities, activity, a manifest and evidence files."""

    def __init__(self, root: Path):
        self.root = root
        (root / "evidence" / "records").mkdir(parents=True)
        self.files, self.activity, self.requests = [], [], []
        # one placeholder activity row per family, so the resource-id regex knows every prefix
        for i, f in enumerate(FAMILIES):
            self.act("UPDATE_RECORD", f"{f}_9{i}90", "2025-01-01T00:00:00Z", source="profile_service")

    def act(self, event_type, rid, t, result="SUCCESS", details=None, source="deletion_worker"):
        self.activity.append({"activity_id": f"activity_{len(self.activity) + 1}", "event_time": t,
                              "event_type": event_type, "source_system": source, "target_system": "x",
                              "resource_id": rid, "reported_result": result,
                              "details": details or f"Policy action completed for {rid}."})

    def json_file(self, fid, captured_at, records: list[dict]):
        p = self.root / "evidence" / "records" / f"{fid}.json"
        p.write_text(json.dumps({"captured_at": captured_at, "records": records}), encoding="utf-8")
        self.files.append({"file_id": fid, "file_path": f"evidence/records/{fid}.json", "origin": "test_origin",
                           "captured_at": captured_at})

    def media_file(self, fid, captured_at, origin="test_screen"):
        p = self.root / "evidence" / "records" / f"{fid}.png"
        p.write_bytes(b"\x89PNG\r\n\x1a\n" + b"0" * 32)
        self.files.append({"file_id": fid, "file_path": f"evidence/records/{fid}.png", "origin": origin,
                           "captured_at": captured_at})

    def request(self, cid, email, requested_at="2026-09-01T00:00:00Z", audit_at="2026-09-10T00:00:00Z", text="Please delete my account."):
        r = {"case_id": cid, "email": email, "requested_at": requested_at, "reported_status": "COMPLETE",
             "reported_at": requested_at, "audit_at": audit_at, "request_text": text}
        self.requests.append(r)
        return r

    def write(self):
        """Write every dataset CSV for this world (used by engine() and by the custom evaluation cases)."""
        _write_csv(self.root / "user_identities.csv", USERS, list(USERS[0]))
        _write_csv(self.root / "user_audit_log.csv", AUDIT, list(AUDIT[0]))
        _write_csv(self.root / "system_activity.csv", self.activity, list(self.activity[0]))
        _write_csv(self.root / "evidence_files.csv", self.files, ["file_id", "file_path", "origin", "captured_at"])
        _write_csv(self.root / "deletion_requests.csv", self.requests or [self.request("case_900", "x@ex.com")],
                   list((self.requests or self.requests)[0]))

    def engine(self, media=None, r3c=None):
        self.write()
        from engine.plan import Engine
        eng = Engine(self.root, media=media)
        if r3c is not None:
            eng.r3c_families = r3c
        return eng


@pytest.fixture
def world(tmp_path):
    return World(tmp_path)


def ops(result, rid=None):
    return [s["operation"] for s in result["steps"] if rid is None or s["resource_id"] == rid]
