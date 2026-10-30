"""Labelling rules R4-R16 (code/docs/LABEL_CONVENTIONS.md). One function per rule.

Every function is keyed on record content and family only, never on case_id or literal ids.
"""
from __future__ import annotations

OWNER = {  # R12 resource family -> owning system
    "account": "account_service", "search": "search_service", "analytics": "analytics_platform",
    "support": "support_platform", "export": "export_service", "data_flow": "integration_service",
    "backup": "backup_service", "audit_record": "security_service", "tombstone": "identity_service",
    "legal_hold": "legal_service", "object": "object_storage", "marketing": "marketing_platform",
    "cache": "cache_service", "email_delivery": "email_delivery_service",
}
IDENT_KEYS = {"email", "phone", "email_hash", "full_name", "name", "display_name", "requester_email",
              "requester_name", "requester_phone", "owner_email", "owner_phone", "customer_email",
              "matched_value", "uploaded_by"}
TRUE = {True, 1, "1", "true", "True"}
FALSE = {False, 0, "0", "false", "False"}

OP_ORDER = ["REPORT_REMAINING_RECORD", "REPORT_EXPOSED_PII", "REPORT_ACTIVE_DATA_FLOW", "REPORT_RESTORE_RISK",
            "DISABLE_DATA_FLOW", "BLOCK_RESTORE", "DELETE_RECORD", "REDACT_RECORD", "ANONYMIZE_RECORD",
            "VERIFY_RECORD_ABSENT", "VERIFY_RECORD_PRESENT", "VERIFY_RECORD_REDACTED", "VERIFY_RECORD_ANONYMIZED",
            "VERIFY_DATA_FLOW_DISABLED", "VERIFY_RESTORE_BLOCKED"]
OPS = {  # operation -> (phase, state), PS L105-119
    "REPORT_REMAINING_RECORD": ("FINDING", "PRESENT"), "REPORT_EXPOSED_PII": ("FINDING", "PRESENT"),
    "REPORT_ACTIVE_DATA_FLOW": ("FINDING", "ACTIVE"), "REPORT_RESTORE_RISK": ("FINDING", "ACTIVE"),
    "DISABLE_DATA_FLOW": ("REMEDIATION", "DISABLED"), "BLOCK_RESTORE": ("REMEDIATION", "BLOCKED"),
    "DELETE_RECORD": ("REMEDIATION", "ABSENT"), "REDACT_RECORD": ("REMEDIATION", "REDACTED"),
    "ANONYMIZE_RECORD": ("REMEDIATION", "ANONYMIZED"), "VERIFY_RECORD_ABSENT": ("VERIFICATION", "ABSENT"),
    "VERIFY_RECORD_PRESENT": ("VERIFICATION", "PRESENT"), "VERIFY_RECORD_REDACTED": ("VERIFICATION", "REDACTED"),
    "VERIFY_RECORD_ANONYMIZED": ("VERIFICATION", "ANONYMIZED"),
    "VERIFY_DATA_FLOW_DISABLED": ("VERIFICATION", "DISABLED"), "VERIFY_RESTORE_BLOCKED": ("VERIFICATION", "BLOCKED"),
}
PHASE_RANK = {"FINDING": 0, "REMEDIATION": 1, "VERIFICATION": 2}


def family(rid: str) -> str:
    return rid.rsplit("_", 1)[0]


# ----------------------------------------------------------------------------- R4 state
def r4_observe(f: dict) -> dict:
    """R4: read one primary observation of a resource into a state dict.

    Activity results are never read here; only file content. Absence markers: NOT_FOUND, 404, rows=0,
    result=miss, account_status DELETED on an account. S case_05 (failover row ACTIVE beats a SUCCESS
    claim), S case_28 (404 beats a FAILED claim), S case_13 (NOT_FOUND beats a FAILED claim).
    """
    res = str(f.get("result") or "").upper()
    st = {"present": True, "exposed": False, "attributable": False, "active": None, "restorable": None,
          "hints": set()}
    if res == "NOT_FOUND" or str(f.get("http_status") or f.get("status_code") or "") == "404" \
            or str(f.get("rows")) == "0" or res == "MISS" or str(f.get("total_hits")) == "0":
        st["present"] = False
    if "profile" in f and f["profile"] is None and "status_code" in f:
        st["present"] = False
    exposed = any(f.get(k) not in (None, "", "[REDACTED]") for k in IDENT_KEYS)
    if str(f.get("direct_identifiers")) == "1":
        exposed = True
    if str(f.get("direct_identifiers")) == "0":
        exposed = False
    if res == "IDENTIFIABLE":
        exposed = True
    if res in ("ANONYMIZED", "REDACTED"):
        exposed = False
    st["exposed"] = exposed and st["present"]
    st["attributable"] = st["exposed"] or (st["present"] and res not in ("ANONYMIZED", "REDACTED") and any(
        f.get(k) not in (None, "") for k in ("user_id", "customer_reference")))
    en = f.get("enabled")
    if en in TRUE or res == "ACTIVE":
        st["active"] = True
    if en in FALSE or res == "DISABLED":
        st["active"] = False
    ra = f.get("restore_allowed")
    if ra in TRUE or res == "ACTIVE" or f.get("decision") == "allow" or (
            f.get("eligible") in TRUE and f.get("deletion_block") in FALSE):
        st["restorable"] = True
    if ra in FALSE or res == "BLOCKED" or f.get("decision") == "deny" or f.get("deletion_block") in TRUE:
        st["restorable"] = False
    if f.get("_media") and res != "NOT_FOUND":
        st["present"] = True
    ev = str(f.get("event") or "")
    rt = str(f.get("record_type") or "")
    if rt == "SUPPORT_ATTACHMENT" or "attachment" in ev or any(k in f for k in ("file_name", "uploaded_by", "file")):
        st["hints"].add("attachment")
    if rt == "SUPPORT_MESSAGE" or "message" in ev or "ticket" in ev or any(
            k in f for k in ("message_text", "message_excerpt", "requester_email", "requester_name")):
        st["hints"].add("message")
    if "contact_lookup" in ev or "email_opt_in" in f:
        st["hints"].add("optin_contact")
    if str(f.get("account_status") or "").upper() == "DELETED" and "name" not in f:
        st["present"] = False
    return st


def merge_states(states: list[dict]) -> dict:
    """Combine observations from the same (latest) capture: any presence / exposure wins."""
    out = {"present": any(s["present"] for s in states), "exposed": any(s["exposed"] for s in states),
           "attributable": any(s["attributable"] for s in states), "active": None, "restorable": None,
           "hints": set().union(*(s["hints"] for s in states))}
    for key in ("active", "restorable"):
        vals = [s[key] for s in states if s[key] is not None]
        if vals:
            out[key] = any(vals)
    return out


# ----------------------------------------------------------------------------- R5-R11 treatments
def r5_account(st: dict | None) -> list[str]:
    """R5: the subject's account. Present -> REMAINING/DELETE/VERIFY_ABSENT, else VERIFY_ABSENT only.

    S case_05 (failover replica), S case_16 (read replica), S case_24 (lookup 200 with email); all 32
    samples verify the account ABSENT.
    """
    if st and st["present"]:
        return ["REPORT_REMAINING_RECORD", "DELETE_RECORD", "VERIFY_RECORD_ABSENT"]
    return ["VERIFY_RECORD_ABSENT"]


def r6_retained(st: dict | None) -> list[str]:
    """R6 (+H4): security audit records and legal holds are retained -> VERIFY_RECORD_PRESENT.

    S case_03, 09, 11-32. Existence may come from post-audit files (H4, S case_09/23/24/29/30); the
    citation still needs an admissible file (handled in R13).
    """
    return ["VERIFY_RECORD_PRESENT"]


def r7_category(fam: str, hints: set) -> str:
    """R7: deletion_rules category from record content -> DELETE | REDACT | ANONYMIZE.

    Support: SUPPORT_ATTACHMENT / attachment scan / file fields -> DELETE (S case_07, 13); a message
    conversation or support-ticket read -> REDACT (S case_11, 18, 19, 29, 30); a bare contact-index
    record -> DELETE (S case_10).
    Analytics: an email_opt_in contact -> DELETE (S case_12); a profile -> ANONYMIZE (S case_11, 22).
    """
    if fam == "support":
        if "attachment" in hints:
            return "DELETE"
        return "REDACT" if "message" in hints else "DELETE"
    if fam == "analytics":
        return "DELETE" if "optin_contact" in hints else "ANONYMIZE"
    if fam == "tombstone":
        return "REDACT"
    return "DELETE"


def r8_treatment(category: str, st: dict | None) -> list[str]:
    """R8 (I9): treatment -> finding/remediation/verify chain; compliant -> verify only.

    DELETE: S case_06, 08, 13, 23. REDACT: S case_11, 19 (compliant: S case_26-28). ANONYMIZE:
    S case_11, 22 (compliant: S case_03, 21, 25-28).
    """
    if category == "DELETE":
        if st and st["present"]:
            return ["REPORT_REMAINING_RECORD", "DELETE_RECORD", "VERIFY_RECORD_ABSENT"]
        return ["VERIFY_RECORD_ABSENT"]
    if category == "REDACT":
        if st and st["present"] and st["exposed"]:
            return ["REPORT_EXPOSED_PII", "REDACT_RECORD", "VERIFY_RECORD_REDACTED"]
        return ["VERIFY_RECORD_REDACTED"] if (st is None or st["present"]) else ["VERIFY_RECORD_ABSENT"]
    if category == "ANONYMIZE":
        if st and st["present"] and st["attributable"]:
            return ["REPORT_EXPOSED_PII", "ANONYMIZE_RECORD", "VERIFY_RECORD_ANONYMIZED"]
        return ["VERIFY_RECORD_ANONYMIZED"] if (st is None or st["present"]) else ["VERIFY_RECORD_ABSENT"]
    raise ValueError(category)


def r9_backup(st: dict | None) -> list[str]:
    """R9: restore allowed -> RESTORE_RISK/BLOCK/VERIFY_BLOCKED; blocked -> VERIFY_BLOCKED.

    S case_09 (restore_allowed=1), 14 (BACKUP_ARCHIVE ACTIVE), 17 (eligible, no deletion block)
    vs S case_26-28 (restore_allowed false). A present archive with no restore flag at all (e.g. the
    evidence_32 screenshot) counts as restorable: COMPLETE needs proof that restore is blocked (PS L27).
    """
    if st and (st["restorable"] or (st["present"] and st["restorable"] is None)):
        return ["REPORT_RESTORE_RISK", "BLOCK_RESTORE", "VERIFY_RESTORE_BLOCKED"]
    return ["VERIFY_RESTORE_BLOCKED"]


def r10_flow(st: dict | None) -> list[str]:
    """R10: enabled connector -> ACTIVE_DATA_FLOW/DISABLE/VERIFY_DISABLED; disabled -> verify only.

    S case_11, 15, 18, 20, 29, 30 vs S case_26-28.
    """
    if st and st["active"]:
        return ["REPORT_ACTIVE_DATA_FLOW", "DISABLE_DATA_FLOW", "VERIFY_DATA_FLOW_DISABLED"]
    return ["VERIFY_DATA_FLOW_DISABLED"]


def r11_tombstone(st: dict | None) -> list[str]:
    """R11: tombstone with any direct identifier -> EXPOSED_PII/REDACT/VERIFY_REDACTED, else verify.

    S case_32 (tombstone_9178 populated) vs S case_31 (tombstone_440 all null).
    """
    if st and st["exposed"]:
        return ["REPORT_EXPOSED_PII", "REDACT_RECORD", "VERIFY_RECORD_REDACTED"]
    return ["VERIFY_RECORD_REDACTED"]


def ops_for(fam: str, st: dict | None, hints: set) -> list[str]:
    if fam == "account":
        return r5_account(st)
    if fam in ("audit_record", "legal_hold"):
        return r6_retained(st)
    if fam == "backup":
        return r9_backup(st)
    if fam == "data_flow":
        return r10_flow(st)
    if fam == "tombstone":
        return r11_tombstone(st)
    return r8_treatment(r7_category(fam, hints), st)


# ----------------------------------------------------------------------------- R12, R14
def r12_system(rid: str) -> str:
    """R12: system_id is the owning system of the resource family, never the replica/capture.

    evidence_54 failover table -> account_service (S case_05); evidence_61 support_replica ->
    support_platform (S case_10); audit_record -> security_service; export -> export_service.
    """
    return OWNER[family(rid)]


def r14_order(steps: list[dict]) -> list[dict]:
    """R14: phase, then table operation order, then system_id, then resource_id (string). PS L126."""
    steps = sorted(steps, key=lambda s: (PHASE_RANK[s["phase"]], OP_ORDER.index(s["operation"]),
                                         s["system_id"], s["resource_id"]))
    for i, s in enumerate(steps, 1):
        s["step_no"] = i
    return steps


# ----------------------------------------------------------------------------- R15, R16
def r15_attribute(link_time: str, own_requests: list[dict], this_case: str) -> bool:
    """R15: with several requests from one user, a resource belongs to the latest request whose
    requested_at <= its earliest linking source; before every request -> the earliest request.

    Samples: object_19 -> the Feb request, not S case_07; account_6523 / tombstone_17 -> the Mar
    request, not S case_17.
    """
    if len(own_requests) <= 1:
        return True
    reqs = sorted(own_requests, key=lambda r: r["requested_at"])
    owner = reqs[0]
    for r in reqs:
        if r["requested_at"] <= link_time:
            owner = r
    return owner["case_id"] == this_case


def r16_media_only(rid: str, has_text_observation: bool) -> bool:
    """R16 (v0): a resource with no ADMISSIBLE text observation (seen only in media, or in text captured
    after audit_at) and tied to the subject only by an activity claim or post-audit text
    (e.g. marketing_001 in evidence_60, object_19 in evidence_46) is not emitted in v0; the case is
    flagged for media extraction instead of guessing ownership or state.
    """
    return not has_text_observation


# ----------------------------------------------------------------------------- R17 linking (adopted H7d)
def r17_padded_account(user_id: str, known_ids: set, attributed: dict) -> str | None:
    """R17/H7d': a subject with no evidence-linked account may use the zero-padded account id
    account_{user_num:03d}, but only when (a) a deletion_worker DELETE_RECORD row for that id falls
    inside the request's [requested_at, audit_at] window (passed in as known_ids; a stray profile UPDATE
    months earlier, as for account_050, does not count); and (b) no evidence attributes it to another
    user. Explains S case_01/02/07/08/10 with 0 FP; fires on 0 test cases and collides with no sample
    gold resource (probe3, scratch/r17_probe3.txt). Replaces H7d's user_num < 100 cutoff, which the
    in-window DELETE condition makes redundant. account_004 has no DELETE row, so it stays R17.
    """
    rid = f"account_{int(user_id.rsplit('_', 1)[1]):03d}"
    if rid not in known_ids or (attributed.get(rid, set()) - {user_id}):
        return None
    return rid


# ----------------------------------------------------------------------------- R3c (ownership vs state)
R3C_FAMILIES: set = {"account"}   # adopted 2026-10-24: 3 explained / 0 FP (scratch/r3c_probe.txt)


def r3c_post_audit_link(fam: str, families: set | None = None) -> bool:
    """R3c: ownership (which resources belong to the subject) may use evidence captured at ANY time,
    still exact identity (R2) and R15 request attribution; state and evidence_id use only admissible
    evidence (R3, R13). A resource linked only post-audit with no admissible observation gets its
    verify-only step (accounts: VERIFY_RECORD_ABSENT with the R13 absence citation).
    Sample basis: S case_09 account_3960 (linked only by evidence_06, captured after audit_at), S case_26
    account_5684 and S case_27 account_3866 (linked only by evidence_02, after audit_at); all three are in
    gold as VERIFY_RECORD_ABSENT. Applies only to the families in `families` (default R3C_FAMILIES).
    """
    return fam in (R3C_FAMILIES if families is None else families)


def h4_legal_exists(rid: str, audit_at: str, activity: list[dict]) -> bool:
    """H4-legal (spec-inferred, no sample): a legal_hold record seen in any file (even one captured after
    audit_at) counts as existing for the subject at audit_at iff a RETAIN_RECORD activity row with
    reported_result SUCCESS exists for it with event_time <= audit_at. Its VERIFY_RECORD_PRESENT step cites
    only an admissible file (R13). Basis: deletion_rules.csv rule_13 "LEGAL_HOLD_RECORD,A supplied legal
    hold is active,RETAIN", the same action as rule_12 SECURITY_AUDIT_LOG (H4). No sample case; see
    LABEL_CONVENTIONS "Settled 2026-10-24" for the test rows it affects.
    """
    return any(a["resource_id"] == rid and a["event_type"] == "RETAIN_RECORD" and a["reported_result"] == "SUCCESS"
               and a["event_time"] <= audit_at for a in activity)
