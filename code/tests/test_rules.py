"""One test per labelling rule (LABEL_CONVENTIONS R1-R17 + adopted hypotheses).

Every test builds a tiny synthetic world (conftest.World); none depends on dataset/. Each docstring names
the sample case that motivated the rule.
"""
from __future__ import annotations

from conftest import ops

from agent.intent import deterministic_intent
from engine.identity import Identity
from engine.rules import (OWNER, h4_legal_exists, r4_observe, r7_category, r8_treatment, r9_backup, r10_flow,
                          r11_tombstone, r12_system, r14_order, r15_attribute, r17_padded_account)

AUDIT = "2026-09-10T00:00:00Z"


def test_r1_intent_negation_and_multilingual():
    """R1, motivated by test case_534/537 (negated deletion) and S case_02 (Spanish deletion request)."""
    assert deterministic_intent("Please delete my account.")["authorizes_deletion"]
    assert deterministic_intent("Intenté eliminar mi cuenta, completen la eliminación.")["authorizes_deletion"]
    assert not deterministic_intent("Please stop the emails. I am not asking for deletion.")["authorizes_deletion"]
    assert not deterministic_intent("Correct my surname without removing any records.")["authorizes_deletion"]
    assert not deterministic_intent("Please remove me from marketing lists only.")["authorizes_deletion"]


def test_r2_identity_exact_case_insensitive_historical_never_fuzzy():
    """R2, motivated by S case_10 (historical email), S case_28 (decoy search_8168 with a '.jr' copy)."""
    from conftest import AUDIT as AUD, USERS
    idt = Identity(USERS, AUD)
    assert idt.resolve("ALICE@EX.COM") == ["user_1"]
    assert idt.resolve("old.alice@ex.com") == ["user_1"]
    assert idt.users_in('{"email": "alice.jr@ex.com"}') == set()
    assert idt.users_in('{"email": "alicee@ex.com"}') == set()
    assert idt.users_in('{"customer_reference": "user_2"}') == {"user_2"}


def test_r3_post_audit_file_is_not_admissible(world):
    """R3, motivated by S case_26/27: evidence_02 (captured after audit_at) shows the account ACTIVE again."""
    world.json_file("evidence_1", "2026-09-05T00:00:00Z", [{"resource_id": "search_11", "email": "alice@ex.com"}])
    world.json_file("evidence_2", "2026-09-20T00:00:00Z", [{"resource_id": "search_11", "email": "alice@ex.com",
                                                            "result": "NOT_FOUND"}])
    req = world.request("case_901", "alice@ex.com")
    res = world.engine().plan(req)
    assert ops(res, "search_11") == ["REPORT_REMAINING_RECORD", "DELETE_RECORD", "VERIFY_RECORD_ABSENT"]


def test_r4_latest_observation_beats_activity_claim(world):
    """R4, motivated by S case_05 (DELETE SUCCESS claim, but the failover replica row is ACTIVE)."""
    world.json_file("evidence_1", "2026-09-05T00:00:00Z", [{"resource_id": "account_12", "email": "alice@ex.com",
                                                            "account_status": "ACTIVE"}])
    world.act("DELETE_RECORD", "account_12", "2026-09-02T00:00:00Z", "SUCCESS")
    res = world.engine().plan(world.request("case_902", "alice@ex.com"))
    assert res["status"] == "INCOMPLETE"
    assert ops(res, "account_12")[0] == "REPORT_REMAINING_RECORD"


def test_r5_account_absent_verify_only(world):
    """R5, motivated by S case_06-15: a deleted account still gets VERIFY_RECORD_ABSENT."""
    world.json_file("evidence_1", "2026-09-05T00:00:00Z", [{"resource_id": "account_13", "customer_reference": "user_1",
                                                            "status_code": 404, "profile": None}])
    res = world.engine().plan(world.request("case_903", "alice@ex.com"))
    assert ops(res, "account_13") == ["VERIFY_RECORD_ABSENT"]
    assert res["status"] == "COMPLETE"


def test_r6_retained_audit_record_verify_present():
    """R6, motivated by S case_03/11-32: security audit records are RETAIN -> VERIFY_RECORD_PRESENT."""
    from engine.rules import ops_for
    assert ops_for("audit_record", {"present": True}, set()) == ["VERIFY_RECORD_PRESENT"]
    assert ops_for("legal_hold", {"present": True}, set()) == ["VERIFY_RECORD_PRESENT"]


def test_r7_category_from_record_content():
    """R7, motivated by S case_13 (SUPPORT_ATTACHMENT -> DELETE), S case_11 (SUPPORT_MESSAGE -> REDACT),
    S case_12 (analytics opt-in contact -> DELETE)."""
    assert r7_category("support", r4_observe({"record_type": "SUPPORT_ATTACHMENT"})["hints"]) == "DELETE"
    assert r7_category("support", r4_observe({"record_type": "SUPPORT_MESSAGE"})["hints"]) == "REDACT"
    assert r7_category("analytics", r4_observe({"event": "contact_lookup_completed", "email_opt_in": "true"})["hints"]) == "DELETE"
    assert r7_category("analytics", r4_observe({"email": "a@x.com"})["hints"]) == "ANONYMIZE"


def test_r8_treatment_chains_and_compliant_verify_only():
    """R8/I9, motivated by S case_11 (all three chains) and S case_26 (compliant -> verify only)."""
    present_exposed = r4_observe({"email": "a@x.com"})
    clean = r4_observe({"email": None, "customer_reference": None})
    assert r8_treatment("DELETE", present_exposed) == ["REPORT_REMAINING_RECORD", "DELETE_RECORD", "VERIFY_RECORD_ABSENT"]
    assert r8_treatment("REDACT", present_exposed) == ["REPORT_EXPOSED_PII", "REDACT_RECORD", "VERIFY_RECORD_REDACTED"]
    assert r8_treatment("ANONYMIZE", present_exposed)[0] == "REPORT_EXPOSED_PII"
    assert r8_treatment("REDACT", clean) == ["VERIFY_RECORD_REDACTED"]
    assert r8_treatment("ANONYMIZE", clean) == ["VERIFY_RECORD_ANONYMIZED"]


def test_r9_backups():
    """R9, motivated by S case_09 (restore_allowed=1 -> risk) vs S case_26 (restore_allowed false)."""
    assert r9_backup(r4_observe({"restore_allowed": 1}))[0] == "REPORT_RESTORE_RISK"
    assert r9_backup(r4_observe({"restore_allowed": False})) == ["VERIFY_RESTORE_BLOCKED"]
    assert r9_backup(r4_observe({"archive_key": "x"}))[0] == "REPORT_RESTORE_RISK"   # no flag at all -> risk


def test_r10_data_flows():
    """R10, motivated by S case_15 (enabled connector) vs S case_26 (enabled false)."""
    assert r10_flow(r4_observe({"enabled": "true"}))[0] == "REPORT_ACTIVE_DATA_FLOW"
    assert r10_flow(r4_observe({"enabled": False})) == ["VERIFY_DATA_FLOW_DISABLED"]


def test_r11_tombstone():
    """R11, motivated by S case_32 (tombstone keeps name/email) vs S case_31 (all null)."""
    assert r11_tombstone(r4_observe({"name": "A", "email": "a@x.com"}))[0] == "REPORT_EXPOSED_PII"
    assert r11_tombstone(r4_observe({"name": None, "email": None, "subject_reference": "user_1"})) == ["VERIFY_RECORD_REDACTED"]


def test_r12_owning_system():
    """R12, motivated by S case_05 (failover table -> account_service) and S case_10 (support_replica)."""
    assert r12_system("account_5") == "account_service"
    assert r12_system("support_2") == "support_platform"
    assert r12_system("audit_record_3") == "security_service"
    assert OWNER["export"] == "export_service"


def test_r13_evidence_latest_admissible_and_absence(world):
    """R13, motivated by S case_11-32 (latest admissible observing file) and S case_31 (absence proof)."""
    world.json_file("evidence_1", "2026-09-01T00:00:00Z", [{"resource_id": "audit_record_14", "subject_reference": "user_1"}])
    world.json_file("evidence_2", "2026-09-08T00:00:00Z", [{"resource_id": "audit_record_14", "subject_reference": "user_1"},
                                                            {"resource_id": "account_98", "customer_reference": "user_1",
                                                             "status_code": 404, "profile": None}])
    world.json_file("evidence_3", "2026-09-30T00:00:00Z", [{"resource_id": "audit_record_14", "subject_reference": "user_1"}])
    eng = world.engine()
    res = eng.plan(world.request("case_904", "alice@ex.com"))
    assert [s["evidence_id"] for s in res["steps"] if s["resource_id"] == "audit_record_14"] == ["evidence_2"]
    # absence proof: latest admissible file covering the account family and naming the subject
    assert eng.r13_evidence("account_99", "user_1", AUDIT) == "evidence_2"


def test_r14_ordering():
    """R14 (PS L126), motivated by S case_16/24: DELETE account sorts before DELETE search."""
    steps = [{"phase": "REMEDIATION", "operation": "DELETE_RECORD", "system_id": "search_service", "resource_id": "search_1"},
             {"phase": "REMEDIATION", "operation": "DELETE_RECORD", "system_id": "account_service", "resource_id": "account_2"},
             {"phase": "REMEDIATION", "operation": "DISABLE_DATA_FLOW", "system_id": "integration_service", "resource_id": "data_flow_3"},
             {"phase": "FINDING", "operation": "REPORT_REMAINING_RECORD", "system_id": "search_service", "resource_id": "search_1"}]
    out = r14_order(steps)
    assert [s["resource_id"] for s in out] == ["search_1", "data_flow_3", "account_2", "search_1"]
    assert [s["step_no"] for s in out] == [1, 2, 3, 4]


def test_r15_multi_request_attribution():
    """R15, motivated by S case_07 vs test case_61: object_19 (linked 02-13) belongs to the February request."""
    reqs = [{"case_id": "case_a", "requested_at": "2026-02-11T00:00:00Z"},
            {"case_id": "case_b", "requested_at": "2026-08-31T00:00:00Z"}]
    assert r15_attribute("2026-02-13T00:00:00Z", reqs, "case_a")
    assert not r15_attribute("2026-02-13T00:00:00Z", reqs, "case_b")
    assert r15_attribute("2026-09-15T00:00:00Z", reqs, "case_b")


def test_r16_file_content_beats_activity_claim(world):
    """R16, motivated by test case_63: evidence_60 shows marketing_001 with another person's email."""
    world.media_file("evidence_5", "2026-09-05T00:00:00Z")
    world.act("LINK_RESOURCE_IDENTITY", "marketing_15", "2026-09-05T01:00:00Z",
              details="Data catalog linked marketing_15 (marketing_15) to bob@ex.com and user_2.", source="data_catalog")
    media = {"evidence_5": {"path": "cache", "records": [{"resource_id": "marketing_15", "record_type": "MARKETING_PROFILE",
             "system_hint": "Audience", "identifiers": {"email": "someone.else@else.com", "phone": None, "email_hash": None,
             "user_id": None, "name": "Some One"}, "status_fields": [], "timestamps": [], "other_references": []}]}}
    res = world.engine(media=media).plan(world.request("case_905", "bob@ex.com"))
    assert ops(res, "marketing_15") == []
    assert any(f.startswith("R16_conflict") for f in res["report"]["flags"])


def test_r17_h7d_prime_padded_account():
    """R17/H7d', motivated by S case_01/02/07/08/10 (account_00N with an in-window DELETE row)."""
    assert r17_padded_account("user_7", {"account_007"}, {}) == "account_007"
    assert r17_padded_account("user_7", set(), {}) is None                                   # no DELETE row in window
    assert r17_padded_account("user_7", {"account_007"}, {"account_007": {"user_2"}}) is None  # attributed elsewhere


def test_h4_audit_record_known_only_post_audit(world):
    """H4, motivated by S case_09/23/24/29/30: audit record seen only in a post-audit file -> VERIFY_PRESENT."""
    world.json_file("evidence_1", "2026-09-05T00:00:00Z", [{"resource_id": "search_16", "email": "alice@ex.com"}])
    world.json_file("evidence_2", "2026-09-30T00:00:00Z", [{"resource_id": "audit_record_16", "subject_reference": "user_1"}])
    res = world.engine().plan(world.request("case_906", "alice@ex.com"))
    steps = [s for s in res["steps"] if s["resource_id"] == "audit_record_16"]
    assert [s["operation"] for s in steps] == ["VERIFY_RECORD_PRESENT"] and steps[0]["evidence_id"] == ""


def test_h4_legal_retain_activity_before_audit():
    """H4-legal (spec-inferred), motivated by test case_220/432 and deletion_rules rule_13 RETAIN."""
    acts = [{"resource_id": "legal_hold_1", "event_type": "RETAIN_RECORD", "reported_result": "SUCCESS",
             "event_time": "2026-06-08T00:00:00Z"}]
    assert h4_legal_exists("legal_hold_1", "2026-07-03T08:00:00Z", acts)
    assert not h4_legal_exists("legal_hold_1", "2026-06-01T00:00:00Z", acts)
    assert not h4_legal_exists("legal_hold_1", "2026-07-03T08:00:00Z", [{**acts[0], "reported_result": "FAILED"}])


def test_r3c_account_linked_only_post_audit(world):
    """R3c, motivated by S case_09/26/27: the account is linked only by a post-audit file -> VERIFY_ABSENT."""
    world.json_file("evidence_1", "2026-09-05T00:00:00Z", [{"resource_id": "account_17", "status_code": 404, "profile": None}])
    world.json_file("evidence_2", "2026-09-30T00:00:00Z", [{"resource_id": "account_17", "email": "alice@ex.com",
                                                            "account_status": "ACTIVE"}])
    req = world.request("case_907", "alice@ex.com")
    assert ops(world.engine(r3c={"account"}).plan(req), "account_17") == ["VERIFY_RECORD_ABSENT"]
    assert ops(world.engine(r3c=set()).plan(req), "account_17") == []


def test_media_own_row_linking(world):
    """Media own-row rule, motivated by test case_55: backup_9286 printed in backup_9287's activity panel
    must not be linked to backup_9287's owner."""
    world.media_file("evidence_6", "2026-09-05T00:00:00Z")
    media = {"evidence_6": {"path": "cache", "records": [{"resource_id": "backup_18", "record_type": "BACKUP_ARCHIVE",
             "system_hint": "Vault", "identifiers": {"email": "alice@ex.com", "phone": None, "email_hash": None, "user_id": None,
             "name": None}, "status_fields": [{"name": "Activity", "value": "backup_19 restored"}], "timestamps": [],
             "other_references": ["backup_19"]}]}}
    res = world.engine(media=media).plan(world.request("case_908", "alice@ex.com"))
    rids = {s["resource_id"] for s in res["steps"]}
    assert "backup_18" in rids and "backup_19" not in rids
