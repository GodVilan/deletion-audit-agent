# Evaluation report

Generated 2026-10-24T19:53Z by `python3 code/evaluation/main.py` (do not edit by hand). `output.csv` sha256 `c140419a317d70ecd5d0daf1106154180c0cc5f6a7eaa703d726e3af5c476490`. VALIDATOR output.csv: 0 errors, 264 warnings. Raw runs: [run_history.md](run_history.md).

## Case-level status accuracy

- **32/32** on the 32 public samples (`deletion_status` equal to gold). Confusion (gold → predicted): COMPLETE->COMPLETE: 10, INCOMPLETE->INCOMPLETE: 22.
- Test-set status distribution vs sample gold:

```text
DISTRIBUTION (test output vs sample gold)
  rows: 518 (expected 518) OK
  NOT_APPLICABLE: 10 (expected exactly 10) OK
  COMPLETE        test  153 ( 29.5%)   sample gold  10 ( 31.2%)
  INCOMPLETE      test  355 ( 68.5%)   sample gold  22 ( 68.8%)
  NOT_APPLICABLE  test   10 (  1.9%)   sample gold   0 (  0.0%)
  steps per authorized case: test 5.63   sample gold 6.03
  operation mix (test % / gold %):
    ANONYMIZE_RECORD               2.6% /   2.6%
    BLOCK_RESTORE                  0.9% /   1.6%
    DELETE_RECORD                 13.0% /  10.9%
    DISABLE_DATA_FLOW              4.0% /   3.1%
    REDACT_RECORD                  4.1% /   3.1%
    REPORT_ACTIVE_DATA_FLOW        4.0% /   3.1%
    REPORT_EXPOSED_PII             6.7% /   5.7%
    REPORT_REMAINING_RECORD       13.0% /  10.9%
    REPORT_RESTORE_RISK            0.9% /   1.6%
    VERIFY_DATA_FLOW_DISABLED      5.1% /   4.7%
    VERIFY_RECORD_ABSENT          19.6% /  25.9%
    VERIFY_RECORD_ANONYMIZED       2.6% /   6.2%
    VERIFY_RECORD_PRESENT         15.3% /  12.4%
    VERIFY_RECORD_REDACTED         6.3% /   5.2%
    VERIFY_RESTORE_BLOCKED         2.1% /   3.1%
```

## Step-level and field-level accuracy

| metric (32 samples, 193 gold steps) | value | definition |
|---|---|---|
| exact_steps_json | 17/32 | the whole parsed steps_json array equal to gold |
| step_P(7-field) | 0.7907 | precision on all seven step fields, step_no included |
| step_R(7-field) | 0.7047 | recall on all seven step fields |
| step_F1(7-field) | 0.7452 | F1 on all seven fields (a missing step shifts every later step_no) |
| step_P(6-field, no step_no) | 1.0 | precision ignoring step_no (gate 1.0: no wrong step emitted) |
| step_R(6-field) | 0.8912 | recall ignoring step_no |
| step_F1(6-field) | 0.9425 | F1 ignoring step_no |
| core_step_recall(6-field, ignoring evidence/step_no) | 172/193 | gold steps matched on phase/system/resource/operation/state |
| evidence_id_acc_on_matched | 172/172 | evidence_id agreement on matched steps |

Field-level accuracy: each gold step is aligned to the predicted step with the same (resource_id, operation); per field, correct / gold steps, where an unaligned gold step counts wrong for every field.

| field | correct / gold steps |
|---|---|
| step_no | 136/193 (70.5%) |
| phase | 172/193 (89.1%) |
| system_id | 172/193 (89.1%) |
| resource_id | 172/193 (89.1%) |
| operation | 172/193 (89.1%) |
| state | 172/193 (89.1%) |
| evidence_id | 172/193 (89.1%) |

Media extraction vs the dev hand transcription:

```text
MEDIA CHECK (vs dev ground truth)
  evidence_09: records=2 resource_ids=EXACT identifiers=DIFF status_values_verbatim=5/5
     user_ids: missing=['user_9842'] extra=[]
  evidence_32: records=4 resource_ids=DIFF identifiers=EXACT status_values_verbatim=18/18
     resource_ids: missing=['backup_9281'] extra=[]
  TOTAL (matched / union):
   resource_ids: 25/26 = 96.2%
   identifiers: 34/35 = 97.1%
   status: 201/243 = 82.7%

```

## Sequence accuracy

- **17/32** cases have gold and predicted steps in identical order (phase/system/resource/operation/state sequence). Every predicted case satisfies the PS L126 ordering (validator I6). All sequence misses are missing steps (R17), never mis-ordered ones: 6-field precision is 1.0.
- step_no field accuracy 136/193 (70.5%): a missing earlier step shifts the step_no of every later step.

## Custom evaluation cases

Synthetic datasets with the `dataset/` schemas (`code/evaluation/custom_cases/`, built by `build.py` with the test fixtures). The expected outputs are written by hand from the rules.

| case | what it tests | rule | expected | got | pass |
|---|---|---|---|---|---|
| case_901 (c1_decoy_identity) | evidence holds '<name>.jr@' and a 1-edit near-miss email; neither may link | R2 | COMPLETE [] | COMPLETE [] (intent: agent(cache)) | PASS |
| case_902 (c2_post_audit_evidence) | account 404 before audit_at, ACTIVE in a file captured after it | R3 + R13 | COMPLETE ['VERIFY_RECORD_ABSENT'] | COMPLETE ['VERIFY_RECORD_ABSENT'] (intent: agent(cache)) | PASS |
| case_903 (c3_multilingual_negation) | Spanish: 'do not delete my account, only unsubscribe me from the newsletter' | R1 | NOT_APPLICABLE [] | NOT_APPLICABLE [] (intent: agent(cache)) | PASS |
| case_904 (c4_file_beats_claim) | activity DELETE SUCCESS, but the latest admissible file shows the account present | R4 + R5 | INCOMPLETE ['REPORT_REMAINING_RECORD', 'VERIFY_RECORD_ABSENT'] | INCOMPLETE ['REPORT_REMAINING_RECORD', 'VERIFY_RECORD_ABSENT'] (intent: agent(cache)) | PASS |
| case_905 (c5_multi_request_user) | two requests by one user; each resource belongs to the request its evidence falls under | R15 | INCOMPLETE ['REPORT_REMAINING_RECORD', 'VERIFY_RECORD_ABSENT'] | INCOMPLETE ['REPORT_REMAINING_RECORD', 'VERIFY_RECORD_ABSENT'] (intent: agent(cache)) | PASS |
| case_906 (c5_multi_request_user) | two requests by one user; each resource belongs to the request its evidence falls under | R15 | INCOMPLETE ['REPORT_REMAINING_RECORD', 'VERIFY_RECORD_ABSENT'] | INCOMPLETE ['REPORT_REMAINING_RECORD', 'VERIFY_RECORD_ABSENT'] (intent: agent(cache)) | PASS |
| case_907 (c6_backup_and_legal_hold) | restorable backup plus an active legal hold for the same subject | R9 + R6 (rule_13) | INCOMPLETE ['REPORT_RESTORE_RISK', 'VERIFY_RECORD_PRESENT', 'VERIFY_RESTORE_BLOCKED'] | INCOMPLETE ['REPORT_RESTORE_RISK', 'VERIFY_RECORD_PRESENT', 'VERIFY_RESTORE_BLOCKED'] (intent: agent(cache)) | PASS |

7/7 custom cases pass (status and full steps_json equal to the hand-written expected.csv; the operation lists above omit remediation for brevity).

## Failures found and improvements made

One row per adopted or rejected rule, in the order decided. Metrics are on the 32 public samples unless marked *test*. 6F1 is the 6-field step F1; R17 is the number of *test* cases with no account step. Full reasoning is in [LABEL_CONVENTIONS.md](../docs/LABEL_CONVENTIONS.md); raw runs are in [run_history.md](run_history.md).

| # | rule | decision | evidence | metric before → after |
|---|---|---|---|---|
| 1 | Engine v0 (R2–R16 in code; R1 deterministic fallback) | adopted | gold is generated by fixed rules (AGENTS.md §7) | – → status 31/32, exact 11/32, 7F1 0.661 |
| 2 | R1 fallback: "profile is gone / cannot identify me" counts as a deletion request | adopted | S case_26 misread as NOT_APPLICABLE | status 30/32 → 31/32 |
| 3 | R7: a support-ticket read is a SUPPORT_MESSAGE (REDACT) | adopted | S case_18 support_5569 | core recall 158/193 → 161/193 |
| 4 | R16 v0: a resource with no admissible text observation is skipped and flagged (H4 audit records exempt) | adopted | S case_24 regression while H4 records were skipped | exact 10/32 → 11/32 |
| 5 | Uncitable verify in a COMPLETE case is dropped (PS L127) | adopted | test case_45/53/55 (later resolved by media) | validator 3 errors → 0 |
| 6 | H4: an audit record seen only in post-audit files exists at audit_at | adopted | 5 explained / 0 FP (S case_09, 23, 24, 29, 30) | gold rows recoverable +5 |
| 7 | H1 (account_{user_num:03d}), H2 (shared keys), H3 (activity subject field) | rejected | H1 6 explained / 14 FP; H2 0 / 0; H3 0 explained / 2 FP | – |
| 8 | H7d: padded account id, user_num < 100, in-window DELETE row | adopted | 5 explained / 0 FP (S case_01/02/07/08/10) | exact 11/32 → 15/32; 6F1 0.9096 → 0.9192 |
| 9 | H5 (batch subject list), H6 (batch elimination), H7/H7b/H7c, H8 (analytics elimination) | rejected | no subject field in batches; H7b/H7c collide with S case_23/S case_07 gold | – |
| 10 | H7d': padded account id without the < 100 cutoff | adopted (replaces 8) | 5 explained / 0 FP / 0 test collisions | no metric change |
| 11 | H7e, H9a (run membership), H9b (exact event_time) | rejected | 0 explained; H9a collides with S case_20 | – |
| 12 | Media extraction by the agent + media records in the evidence graph | adopted | case_07 needs evidence_58 (PDF) | status 31/32 → **32/32**; exact 15/32 → 16/32; 6F1 0.9192 → 0.9337; *test* media_needed 10 → 0 |
| 13 | Media own-row linking (ids inside another record's panel never link) | adopted | *test* case_55 picked up backup_9286/9281 | *test* case_55 −2 backups |
| 14 | Media reference binding by whole token ("statement NST-…") | adopted | *test* case_33 export_1842 | *test* case_33 COMPLETE → INCOMPLETE |
| 15 | R16 content beats claim (marketing_001 shows another person) | adopted | evidence_60 vs activity_4008 | *test* case_63 marketing_001 dropped |
| 16 | R3c: account ownership from post-audit evidence | adopted for account; rejected for the other families | 3 explained / 0 FP (S case_09/26/27); other families 0 explained | exact 16/32 → 17/32; 6F1 0.9337 → 0.9425; R17 342 → 263 |
| 17 | H4-legal: legal hold exists iff a RETAIN_RECORD SUCCESS row ≤ audit_at | adopted (spec-inferred) | rule_13 RETAIN = rule_12 RETAIN; no sample | *test* case_220/432 +1 verify each |
| 18 | Per-subject cap on audit records (case_45) | rejected | all six evidence_37 rows carry user_03 themselves | no change |
| 19 | A13: compliant records get their verify step in INCOMPLETE cases too | settled (include) | accounts/audit records in INCOMPLETE samples (S case_09) | no change |
| 20 | R2 token-boundary matching in the R13 absence check | adopted (bug fix) | unit test: user_12 matched inside user_123 | 0 output rows changed |
| 21 | Media prompt media-v2 (example `user_123` was a real id) | adopted (hygiene) | literal grep | 0 output rows changed |

### Bugs found by tests, grep and dev diffs (all fixed)

| bug | found by | fix | metric before → after |
|---|---|---|---|
| R13 absence check matched subject tokens by substring (`user_12` inside `user_123`, `alice@` inside `malice@`); a length filter only hid it | unit test `test_r13_evidence_latest_admissible_and_absence` | token-boundary matching (`_has_token`) | 0 output rows changed |
| Media prompt used `user_123`, a real user id, as an example | literal grep of code/ for ids | `user_<digits>` (prompt media-v2), cache re-extracted | 0 output rows changed |
| Ids printed inside another record's panel were linked (case_55 picked up backup_9286/9281) | dev diff of test output | media records link only their own resource id | *test* −2 wrong steps |
| Label-prefixed references ("statement NST-…") did not bind to their LINK rows | media_needed flag on test case_33 | whole-token reference binding | *test* case_33 COMPLETE → INCOMPLETE |
| A COMPLETE case emitted verify steps with no citable evidence | validator (I3) | drop and flag uncitable verifies (PS L127) | validator 3 errors → 0 |
| Keyword fallback missed "confirm the profile is gone" | sample scorer (case_26) | added verification phrasing | status 30/32 → 31/32 |
| Unused import and dead constant | ruff | removed | – |

## Known limitations

- **R17: 263 test cases have no account step.** Deletion-worker activity rows carry no subject field. Every deletion batch holds two or more unattributed accounts whose request windows overlap (S case_28 and case_29 share batch #187), and no evidence file names these accounts with an identifier. H1–H3 and H5–H9 were probed and rejected (`code/analysis/r17_probe2.py`); H7d' and R3c recovered part of the gap (342 → 263). In the samples, 12 subject accounts, 7 anonymized analytics records and 2 audit records (in no participant text) remain unattributable.
- **case_63** is COMPLETE with no steps: its only candidate resource (marketing_001) shows another person on screen (R16).
- **Spec-inferred, no sample example:** H4-legal (legal hold exists iff a RETAIN_RECORD SUCCESS row ≤ audit_at); the R12 owning systems for legal_service, object_storage and marketing_platform; and the **R9 inference** that a present archive with no restore flag at all is restorable (RESTORE_RISK). The basis for R9 is PS L27: "no active sync, import, or restore path can recreate the data" (COMPLETE needs proof that restore is blocked).
- **Agent vs fallback:** the final live run answered all 518 intents with the agent (0 fallback). The deterministic fallback used without a key agrees with the agent on 518/518, so keyless runs reproduce `output.csv` byte for byte.
