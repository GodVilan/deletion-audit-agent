"""Build the custom evaluation cases (synthetic datasets with the dataset/ schemas) and their expected output.

Each case directory holds a complete tiny dataset (user_identities.csv, user_audit_log.csv,
system_activity.csv, evidence_files.csv, evidence/, deletion_requests.csv), plus expected.csv and case.json.
The expected outputs are written out by hand from the rules (LABEL_CONVENTIONS), never produced by the engine.

    python3 code/evaluation/custom_cases/build.py
"""
from __future__ import annotations

import csv
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tests"))
sys.path.insert(0, str(HERE.parents[1]))
from conftest import World  # noqa: E402


def step(n, phase, system, rid, op, state, ev=""):
    return {"step_no": n, "phase": phase, "system_id": system, "resource_id": rid, "operation": op,
            "state": state, "evidence_id": ev}


def build_case(name, what, rule, make, expected):
    d = HERE / name
    if d.exists():
        shutil.rmtree(d)
    d.mkdir()
    w = World(d)
    make(w)
    w.write()
    with open(d / "expected.csv", "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh)
        wr.writerow(["case_id", "deletion_status", "steps_json"])
        for cid, status, steps in expected:
            wr.writerow([cid, status, json.dumps(steps, separators=(",", ":"))])
    (d / "case.json").write_text(json.dumps({"what": what, "rule": rule}, indent=1), encoding="utf-8")


def c1(w):
    w.json_file("evidence_1", "2026-09-05T00:00:00Z", [
        {"resource_id": "search_21", "email": "alice.jr@ex.com", "display_name": "Alice Ark"},
        {"resource_id": "search_22", "email": "alicf@ex.com"}])
    w.request("case_901", "alice@ex.com")


def c2(w):
    w.json_file("evidence_1", "2026-09-05T00:00:00Z", [{"resource_id": "account_31", "customer_reference": "user_1",
                                                       "status_code": 404, "profile": None}])
    w.json_file("evidence_2", "2026-09-20T00:00:00Z", [{"resource_id": "account_31", "email": "alice@ex.com",
                                                       "full_name": "Alice Ark", "account_status": "ACTIVE"}])
    w.request("case_902", "alice@ex.com")


def c3(w):
    w.json_file("evidence_1", "2026-09-05T00:00:00Z", [{"resource_id": "account_33", "email": "alice@ex.com",
                                                       "account_status": "ACTIVE"}])
    w.request("case_903", "alice@ex.com",
              text="No borren mi cuenta, por favor; solo quiero darme de baja del boletín.")


def c4(w):
    w.json_file("evidence_1", "2026-09-05T00:00:00Z", [{"resource_id": "account_41", "email": "bob@ex.com",
                                                       "account_status": "ACTIVE"}])
    w.act("DELETE_RECORD", "account_41", "2026-09-06T00:00:00Z", "SUCCESS",
          details="Deletion worker reported the requested operation as completed. Target resource: account_41.")
    w.request("case_904", "bob@ex.com")


def c5(w):
    w.json_file("evidence_1", "2026-03-03T00:00:00Z", [{"resource_id": "search_51", "email": "bob@ex.com"}])
    w.json_file("evidence_2", "2026-09-05T00:00:00Z", [{"resource_id": "export_52", "owner_email": "bob@ex.com",
                                                       "download_available": True}])
    w.request("case_905", "bob@ex.com", requested_at="2026-03-01T00:00:00Z", audit_at="2026-03-05T00:00:00Z")
    w.request("case_906", "bob@ex.com", requested_at="2026-09-01T00:00:00Z", audit_at="2026-09-10T00:00:00Z")


def c6(w):
    w.json_file("evidence_1", "2026-09-05T00:00:00Z", [
        {"resource_id": "backup_61", "customer_reference": "user_7", "restore_allowed": True,
         "archive_key": "archive/customer-data/backup_61.tar.zst"},
        {"resource_id": "legal_hold_62", "subject_reference": "user_7", "order_reference": "ORD-1",
         "retention_reason": "payment_dispute_and_tax_record", "retained_until": "2033-12-31T23:59:59Z"}])
    w.request("case_907", "gina@ex.com")


CASES = [
    ("c1_decoy_identity", "evidence holds '<name>.jr@' and a 1-edit near-miss email; neither may link", "R2",
     c1, [("case_901", "COMPLETE", [])]),
    ("c2_post_audit_evidence", "account 404 before audit_at, ACTIVE in a file captured after it", "R3 + R13",
     c2, [("case_902", "COMPLETE", [step(1, "VERIFICATION", "account_service", "account_31", "VERIFY_RECORD_ABSENT", "ABSENT", "evidence_1")])]),
    ("c3_multilingual_negation", "Spanish: 'do not delete my account, only unsubscribe me from the newsletter'", "R1",
     c3, [("case_903", "NOT_APPLICABLE", [])]),
    ("c4_file_beats_claim", "activity DELETE SUCCESS, but the latest admissible file shows the account present", "R4 + R5",
     c4, [("case_904", "INCOMPLETE", [
         step(1, "FINDING", "account_service", "account_41", "REPORT_REMAINING_RECORD", "PRESENT", "evidence_1"),
         step(2, "REMEDIATION", "account_service", "account_41", "DELETE_RECORD", "ABSENT"),
         step(3, "VERIFICATION", "account_service", "account_41", "VERIFY_RECORD_ABSENT", "ABSENT")])]),
    ("c5_multi_request_user", "two requests by one user; each resource belongs to the request its evidence falls under", "R15",
     c5, [("case_905", "INCOMPLETE", [
         step(1, "FINDING", "search_service", "search_51", "REPORT_REMAINING_RECORD", "PRESENT", "evidence_1"),
         step(2, "REMEDIATION", "search_service", "search_51", "DELETE_RECORD", "ABSENT"),
         step(3, "VERIFICATION", "search_service", "search_51", "VERIFY_RECORD_ABSENT", "ABSENT")]),
          ("case_906", "INCOMPLETE", [
         step(1, "FINDING", "export_service", "export_52", "REPORT_REMAINING_RECORD", "PRESENT", "evidence_2"),
         step(2, "REMEDIATION", "export_service", "export_52", "DELETE_RECORD", "ABSENT"),
         step(3, "VERIFICATION", "export_service", "export_52", "VERIFY_RECORD_ABSENT", "ABSENT")])]),
    ("c6_backup_and_legal_hold", "restorable backup plus an active legal hold for the same subject", "R9 + R6 (rule_13)",
     c6, [("case_907", "INCOMPLETE", [
         step(1, "FINDING", "backup_service", "backup_61", "REPORT_RESTORE_RISK", "ACTIVE", "evidence_1"),
         step(2, "REMEDIATION", "backup_service", "backup_61", "BLOCK_RESTORE", "BLOCKED"),
         step(3, "VERIFICATION", "legal_service", "legal_hold_62", "VERIFY_RECORD_PRESENT", "PRESENT"),
         step(4, "VERIFICATION", "backup_service", "backup_61", "VERIFY_RESTORE_BLOCKED", "BLOCKED")])]),
]

if __name__ == "__main__":
    for name, what, rule, make, expected in CASES:
        build_case(name, what, rule, make, expected)
        print("built", name)
