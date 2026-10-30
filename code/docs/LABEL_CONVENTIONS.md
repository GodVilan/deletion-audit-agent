# LABEL_CONVENTIONS: how sample gold labels are formed (binding, with SPEC_CARD.md)

Derived from the 32 public sample rows (`dataset/sample_output.csv`) traced back to participant evidence. Sources: `scratch/gold_trace.txt` (code/analysis/gold_trace.py), `scratch/p1_checks.txt` (code/analysis/p1_checks.py), `scratch/media_transcripts.md`. Nothing here is keyed on case_id; case ids are cited only as evidence for a rule.

Markers: **spec-backed** (problem_statement/AGENTS text), **sample-inferred** (only the samples show it), **OPEN** (unresolved, with the check that would settle it), **CONTRADICTED** (the samples disagree with the drafted wording; the revision is given). Step abbreviations: REM = REPORT_REMAINING_RECORD, PII = REPORT_EXPOSED_PII, FLOW = REPORT_ACTIVE_DATA_FLOW, RISK = REPORT_RESTORE_RISK, v* = VERIFY_* (vABS, vPRES, vRED, vANON, vDIS, vBLK).

## Part A: one row per sample case

| row | what's special in the input | gold (status + steps) | rule(s) shown | spec or sample | certainty |
|---|---|---|---|---|---|
| case_01 | reported COMPLETE; account_001 in no file; activity_3342 DELETE SUCCESS | COMPLETE: vABS account_001 (evidence_54) | R5, R13 absence proof | sample | likely (absence citation) |
| case_02 | Spanish text; reported PARTIALLY_COMPLETE; activity_3376 DELETE **PARTIAL** | COMPLETE: vABS account_002 (evidence_54) | R1 multilingual, R4 (a PARTIAL claim alone ≠ finding), R13 | sample | likely |
| case_03 | French; decoy l.fontaine02@ (another user, d=2) only in post-audit evidence_53 | COMPLETE: vABS account_7566, vPRES audit_record_2016, vANON analytics_9406 (all evidence_94) | R2, R6, R8 compliant-only verify, R13 | sample | certain |
| case_04 | "keep anonymous statistics"; account_004 appears nowhere in participant data | COMPLETE: vABS account_004 (evidence_54), vANON analytics_901 (evidence_56) | R8, R13 absence + two files per case, R17 | sample | likely; account id not derivable |
| case_05 | activity DELETE SUCCESS + SYNC to failover; evidence_54 failover table still ACTIVE | INCOMPLETE: REM/DELETE/vABS account_005 (evidence_54) | R4 file beats claim, R5, R12 replica → account_service | spec + sample | certain |
| case_06 | search_001 in evidence_57 (source_resource_id account_006); decoys jonas.berglund@/joana.berg@ | INCOMPLETE: REM/DELETE search_001; vABS account_006 + search_001 | R2, R5 (verify-only account), R8 | sample | certain |
| case_07 | PDF attachment, uploader customer; object_19 linked to the same user via activity_4007 (Feb) | INCOMPLETE: REM/DELETE/vABS support_001 (evidence_58); vABS account_007 | R7 attachment → DELETE, R15 (object_19 belongs to case_61) | sample | certain (R15 likely) |
| case_08 | export_001 download_available true (evidence_59) | INCOMPLETE: REM/DELETE/vABS export_001; vABS account_008 | R8 USER_EXPORT DELETE, R12 export_service | sample | certain |
| case_09 | backup_restore_entries restore_allowed=1 (evidence_93); audit_record_4902 only in post-audit evidence_06 | INCOMPLETE: RISK/BLOCK/vBLK backup_4978; vABS account_3960; vPRES audit_record_4902 | R9, R6 (CONTRADICTED), R3b | sample | certain for backup; R6 open |
| case_10 | request email is historical; support_replica log | INCOMPLETE: REM/DELETE/vABS support_002 (evidence_61); vABS account_010 | R2 historical, R7, R12 support_replica → support_platform | sample | certain |
| case_11 | handover TXT with record types; audit_at == file captured_at | INCOMPLETE: REM search_052; PII analytics_2034, support_864; FLOW data_flow_9522; DISABLE → DELETE → REDACT → ANONYMIZE; 6 verifies | R3 inclusive, R7 SUPPORT_MESSAGE, R8, R10, R14 | spec + sample | certain |
| case_12 | email changed; analytics_9914 is `contact_lookup_completed email_opt_in=true` keyed by the **historical email_hash** | INCOMPLETE: REM/DELETE/vABS analytics_9914 (evidence_01); vABS account_9797; vPRES audit_record_2945 | R2 hash, R7 opt-in contact → DELETE | sample | likely |
| case_13 | SUPPORT_ATTACHMENT FOUND; activity DELETE account FAILED but file NOT_FOUND | INCOMPLETE: REM search_1308 + support_4218 → DELETE; vABS ×3; vPRES | R4, R7 attachment, R14 | sample | certain |
| case_14 | Japanese; handover `BACKUP_ARCHIVE ACTIVE` | INCOMPLETE: RISK/BLOCK/vBLK backup_3870; vABS account_3677; vPRES audit_record_987 | R1, R9 | sample | certain |
| case_15 | connector still enabled (evidence_01) | INCOMPLETE: FLOW/DISABLE/vDIS data_flow_9846; vABS account_4745; vPRES | R10 | sample | certain |
| case_16 | account_994 present only in the read-replica table (replication drift) | INCOMPLETE: REM account_994 + search_1007 → DELETE (account before search); 3 verifies | R5, R12, R14 sort beats downstream-first | spec + sample | certain |
| case_17 | backup restore policy check ERROR (evidence_01); same user as test case_46 | INCOMPLETE: RISK/BLOCK/vBLK backup_3245; vABS account_4092; vPRES audit_record_1797 | R9, R15 (account_6523, tombstone_17 excluded) | sample | certain (R15 likely) |
| case_18 | full set in readback log evidence_94; audit_record_6645 appears in **no** participant text | INCOMPLETE: REM search_4013; PII analytics_037, support_5569; FLOW data_flow_4890; 6 verifies | R7, R8, R10, R6 CONTRADICTED, R17 | sample | certain except audit record |
| case_19 | message_pii_scan on a shared conversation | INCOMPLETE: REM search_6083; PII/REDACT/vRED support_9553; vABS ×2; vPRES | R7 message → REDACT | sample | certain |
| case_20 | audit_record_5569 appears in no participant text | INCOMPLETE: REM search_4262; FLOW data_flow_1770; DISABLE before DELETE | R10, R14, R6 CONTRADICTED, R17 | sample | certain except audit record |
| case_21 | all compliant in evidence_92; anonymized analytics carries no identifiers | COMPLETE: vABS account_6440, vPRES audit_record_3737, vANON analytics_5335 | R8 compliant → verify, R13 | sample | certain for steps; linking R17 |
| case_22 | analytics row in read replica still has user_51 email/phone/hash | INCOMPLETE: REM search_8911; PII/ANONYMIZE/vANON analytics_4440 | R8 ANONYMIZE | sample | certain |
| case_23 | text asks for export + search deletion | INCOMPLETE: REM export_7364 + search_898 → DELETE; verifies sorted export < search | R8, R14 | sample | certain |
| case_24 | "told deletion was complete"; account_5334 lookup 200 with email | INCOMPLETE: REM account_5334 + search_5577 → DELETE | R5, R4, R14 | sample | certain |
| case_25 | reported NOT_STARTED but evidence shows compliant | COMPLETE: vABS account_3136, vPRES audit_record_451, vANON analytics_1895 | R4 status is a claim | spec + sample | certain |
| case_26 | evidence_02 (manifest 09-17 > audit 09-15) shows the account ACTIVE again | COMPLETE: 6 verifies, all evidence_92 | R3 manifest time decides, R9/R10/R11-style compliant verifies | spec + sample | certain |
| case_27 | "audit as it stood"; same post-audit reactivation as case_26 | COMPLETE: 6 verifies, all evidence_92 | R3 | spec + sample | certain |
| case_28 | decoy search_8168 `smartinez6461.jr@` (evidence_02, post-audit); activity DELETE FAILED but file 404 | COMPLETE: 6 verifies, all evidence_92 | R2, R3, R4 | spec + sample | certain |
| case_29 | historical email; enabled bridge; requester_email still set | INCOMPLETE: REM search_1993; PII analytics_5208, support_5281; FLOW data_flow_3827 | R2, R7, R8, R10 | sample | certain |
| case_30 | historical email; same shape as case_29 | INCOMPLETE: same 14-step shape as case_29 | R2, R8, R10, R14 | sample | certain |
| case_31 | tombstone with all identifiers null; account_service collection empty in evidence_51 | COMPLETE: vABS account_4857, vPRES audit_record_6909, vRED tombstone_440 (all evidence_51) | R11, R13 absence proof | spec + sample | certain |
| case_32 | tombstone still holds name/email/phone/hash | INCOMPLETE: PII/REDACT/vRED tombstone_9178; vABS account_8858; vPRES audit_record_7068 | R11 | spec + sample | certain |

## Part B: rules

### R1 Intent: spec-backed
NOT_APPLICABLE iff request_text does not authorize deletion → `[]`. Negation-aware and multilingual. Test set: exactly case_533–542. CLASSIFY_REQUEST rows corroborate only.
- Spec: AG §6.5 "A request for access, correction, export, marketing opt-out, or another non-deletion action is `NOT_APPLICABLE`"; PS L91.
- Evidence: 0 NOT_APPLICABLE samples. All 32 sample texts (EN/ES/FR/JA) authorize deletion. A full scan of 375 distinct test texts finds exactly 10 non-deletion texts (case_533–542, all reported NOT_STARTED). The 10 CLASSIFY_REQUEST rows (activity_3486…3827) link one-to-one to those 10 users through evidence (scratch/audit_out.txt §e).
- Pitfall: case_538 "remove me from marketing lists only" contains a deletion verb but is an opt-out.

### R2 Identity: sample-inferred
Case-insensitive exact match on current+historical email, email_hash, phone, user_id. Never fuzzy. Evidence-only `<name>.jr@` and near-miss emails never match.
- Evidence: historical email in S case_10/29/30. Historical email_hash in S case_12: evidence_01 analytics_9914 `correlation_key` = audit_283 old_value for user_12. Decoys excluded from gold: S case_28 search_8168 `smartinez6461.jr@gmail.com` (evidence_02); evidence_09 search_1874 `g.silva76.jr@gmail.com`; S case_06 search_8814/4203 (jonas.berglund@/joana.berg@, evidence_57). 20 test request emails differ only by case.

### R3 Admissibility: spec-backed
A file counts iff its manifest captured_at ≤ audit_at (inclusive). In-file timestamps never override. An activity counts iff event_time ≤ audit_at.
- Spec: AG §6.2 "at or before `audit_at`"; AG §6.6 "Never cite … an evidence item captured after the case's `audit_at`."
- Evidence: S case_11/13/14/16/22/31/32 cite files captured exactly at audit_at. S case_26/27: evidence_02 (manifest 2026-09-17) has a section stamped 2026-09-15T12:00 (== audit_at) showing account_5684/3866 ACTIVE, but gold is COMPLETE from evidence_92. So the manifest time decides.
- Test-set stress cases: evidence_21 (legal_hold_4961, lines stamped 07-03 ≤ case_220 audit 07-03T08:00, but manifest 07-05) and evidence_40 (legal_hold_438, manifest 03-22 > case_432 audit 03-20).

### R3b Existence knowledge from post-audit evidence: OPEN (new)
Gold includes **verify-only** steps (evidence_id "") for resources that admissible text never shows:
- audit_record_4902 (case_09: evidence_06, 09-18 > audit 09-16)
- audit_record_4128 / 7095 / 3954 / 1707 (case_23/24/29/30: evidence_02, 09-17 > audit 09-15)
- audit_record_6645 (case_18) and audit_record_5569 (case_20): in **no** participant text at all

Candidate rule: post-audit evidence may establish that a resource *exists and belongs to the subject* (for an uncited verify step), never its state or a citation. It needs a decision because AG §6.2 reads strictly. It cannot explain 6645/5569 (R17).

### R4 State: spec-backed, sample-confirmed
The latest admissible file observation of a resource decides its state. Activity results are claims and are used only when no file observes the resource.
- Evidence: S case_05 (activity DELETE SUCCESS; evidence_54 failover row ACTIVE → REM). S case_28 (activity DELETE FAILED; evidence_92 404 → vABS). S case_13 (DELETE FAILED; evidence_03 NOT_FOUND → vABS).
- Refinement (sample-inferred): **activity results never create a finding.** When only activity rows exist, gold treats the resource as compliant. S case_02 account_002 PARTIAL → COMPLETE; S case_32 account_8858 PARTIAL → vABS only; S case_09 account_3960 FAILED with no admissible file → vABS only. All 75 cited gold evidence ids are files.

### R5 Account: sample-inferred (32/32)
Every authorized case has account_service VERIFY_RECORD_ABSENT for the subject's account. If the account is present → REM + DELETE.
- Evidence: I10 holds 32/32. Present → REM: S case_05 (failover replica), S case_16 (read replica), S case_24 (lookup 200 with email).
- **OPEN (R17):** the subject's account id is linked to the subject by admissible text in only 12/32 samples (20 accounts are unlinked or linked only after audit). See R17.

### R6 Security audit record: CONTRADICTED as drafted → revised OPEN
Drafted: "VERIFY_RECORD_PRESENT iff the subject has one in admissible evidence (S case_03, 09, 11-32; absent in 01, 02, 04-08, 10)."
- The case lists are right, but "in admissible evidence" is false for 7 of the 24: case_09, 18, 20, 23, 24, 29, 30 (see R3b). Only the remaining 17 have the audit record in an admissible file.
- Revised candidate: vPRES for every SECURITY_AUDIT_LOG record of the subject known from any participant evidence (pre- or post-audit), uncited in INCOMPLETE cases, cited from an admissible file in COMPLETE cases. Every COMPLETE case with an audit record (03, 21, 25-28, 31) has it in an admissible file.
- Why 01, 02, 04-08, 10 have none: no audit record for those users exists anywhere in participant data. Consistent.

- **UPDATE 2026-10-24 (R17 probe, scratch/r17_probe.txt): H4 ADOPTED.** A security_service audit record linked to the subject in ANY file (even one captured after audit_at) exists for the subject at audit_at → vPRES. It is cited only if an admissible file observes it, so it stays uncited in INCOMPLETE cases. Explains 5 gold rows (case_09 audit_record_4902, case_23 4128, case_24 7095, case_29 3954, case_30 1707), 0 false positives over 32 samples. audit_record_6645 (case_18) and 5569 (case_20) remain unexplained (R17).

### R7 Category from record content: sample-inferred
An explicit record_type or scan type decides the category:
- SUPPORT_ATTACHMENT → DELETE: evidence_03 `support_4218 | SUPPORT_ATTACHMENT | FOUND` (S case_13); evidence_58 PDF "uploader customer" (S case_07); support_replica contact index (S case_10, evidence_61).
- SUPPORT_MESSAGE → REDACT: evidence_03 `support_864 | SUPPORT_MESSAGE | IDENTIFIABLE` (S case_11); `event=message_pii_scan` (S case_19, evidence_01); conversation records with requester_* fields (S case_18, 29, 30).
- Analytics: an analytics record that is an `email_opt_in` contact keyed to the subject's identifiers → DELETE (S case_12, evidence_01 `contact_lookup_completed rows=1 email_opt_in=true`, keyed by user_12's historical email_hash). Every other attributable analytics profile → ANONYMIZE (S case_11, 18, 22, 29, 30).
- Status: likely. The opt-in contact rule rests on one sample (case_12), so it needs a custom eval case.

### R8 Treatment → steps (I9): sample-inferred
- DELETE → REM / DELETE_RECORD / vABS
- REDACT → PII / REDACT_RECORD / vRED
- ANONYMIZE → PII / ANONYMIZE_RECORD / vANON
- An already-compliant record gets only its VERIFY step, and only in COMPLETE cases.
- Evidence: 0 I9 violations across 22 INCOMPLETE rows. Compliant-only verifies appear in COMPLETE S case_03, 04, 21, 25-28, 31.
- **OPEN (A13):** whether an INCOMPLETE case also verifies already-compliant records. No sample shows one. Compliant analytics/support carry no identifiers, so the trace cannot tell "omitted" from "not linkable" (R17).

- **A13 settled:** an already-compliant record gets its VERIFY step regardless of case status. Sample-backed by analogy: accounts and audit records in INCOMPLETE samples (e.g. case_09 account_3960).

### R9 Backups: sample-inferred
- restore_allowed true → RISK / BLOCK_RESTORE / vBLK.
- restore_allowed false → vBLK only.
- Evidence (risk): S case_09 evidence_93 `restore_allowed: 1`; S case_14 evidence_03 `BACKUP_ARCHIVE | ACTIVE`; S case_17 evidence_01 `restore_policy_check` ERROR trace.
- Evidence (blocked): S case_26-28 evidence_92 `restore_allowed: false`.
- Never REM or vPRES for a backup.
- Note: evidence_32 (PNG) shows backup_9287 without any restore flag, and activity_3387 shows it actually restored data (search_4882), so the test set needs a decision there.

### R10 Data flows: sample-inferred
- enabled → FLOW / DISABLE_DATA_FLOW / vDIS.
- disabled → vDIS only.
- Evidence (active): S case_11 evidence_03 `DATA_FLOW | ACTIVE`; S case_15 evidence_01; S case_18/20 evidence_94 connector_config_read; S case_29/30 evidence_92 `enabled: true`.
- Evidence (disabled): S case_26-28 `enabled: false, last_delivery_status: stopped`.
- Remediation order is DISABLE first (R14).

### R11 Tombstone: spec-backed
- Any of name/email/phone/email_hash non-null → PII / REDACT / vRED.
- All null → vRED only.
- Spec: PS L13; AG §6.5.
- Evidence: S case_32 tombstone_9178 (all four populated); S case_31 tombstone_440 (all null). Both are in evidence_51.

### R12 system_id: sample-inferred
system_id = the owning system for the resource family, not the capture or replica.
- Mapping: account→account_service, search→search_service, analytics→analytics_platform, support→support_platform, export→export_service, data_flow→integration_service, backup→backup_service, audit_record→security_service, tombstone→identity_service.
- Evidence: evidence_54 failover table → account_service (S case_05); evidence_05 read-replica table → account_service (S case_16); evidence_61 `support_replica` → support_platform (S case_10); audit_record → security_service although 196/197 activity rows target archive_service; export → export_service although 155/189 rows target object_store.
- Unsampled families (proposed): object_N → object_storage, marketing_N → marketing_platform, legal_hold_N → legal_service, cache_N → cache_service, email_delivery_N → email_delivery_service. All are activity target systems.

### R13 evidence_id: sample-inferred; verdict 75/75
COMPLETE verifications and all findings cite the latest admissible file that observes the resource. Absence proofs cite the latest admissible capture of the owning system for that subject.
- Result (Task 2a, scratch/p1_checks.txt), over all 75 cited sample steps:

| rule | observed steps (71) | absence steps (4) |
|---|---|---|
| (i) latest admissible file observing the resource | **71/71** | 0/4 |
| (ii) latest admissible file covering the owning system **and** containing the subject's identifiers | 70/71 | 1/4 (case_31 evidence_51) |
| (iii) latest admissible file covering the owning system, any subject | 33/71 | 3/4 (fails case_04: picks evidence_08) |
| (iv) latest admissible file whose manifest origin names the family (`customer_account_*`) | 6/71 | 3/4 (fails case_31) |
| (v) latest admissible file mentioning the subject, any system | 70/71 | 1/4 |

- **Combined rule reproduces 75/75:** observed → (i); absence → (ii), else (iv).
- Caveat: the fallback rests on 3 rows (case_01/02/04 → evidence_54, the only `customer_account_*` origin before their audits). It stays **OPEN** until a custom case tests it; a plausible generic reading is "the most recent dedicated account-profile capture".

### R14 Ordering: spec-backed
Phase, then table operation order, then system_id, then resource_id (string ascending).
- Spec: PS L126.
- Evidence: 32/32 samples follow it (scratch/verify_card.py). S case_16/24 delete account before search (sort beats "downstream first"). S case_11/20/29/30 put DISABLE before DELETE.

### R15 Multi-request users: verdict = sample-consistent, OPEN for test
Resources belong to the request whose window contains their evidence.
- Proposed rule: for a user with several requests, a linked resource belongs to the **latest request whose requested_at ≤ the resource's earliest linking source time**. Admissibility (R3) then applies per case.
- Sample check: object_19 (activity_4007, 02-13) → case_61 (req 02-11), so it is not in case_07 gold ✓. account_6523 (evidence_67, 03-10) and tombstone_17 (activity_4011, 03-10) → case_46 (req 03-08), so they are not in case_17 gold ✓. account_4092, audit_record_1797, backup_3245 (evidence_01, 09-15) → case_17 (req 08-19) ✓.
- user_18 (test only): export_1260 (06-18) → case_52; export_1842 / evidence_18 PDF (07-18) → case_33. account_2373, audit_record_8486, search_2352 and export_1260's later sightings (evidence_01, 09-15; activity 08-19) fall after both audits, so they are inadmissible for both (but see R3b).
- Do not apply the window as a general filter. Over all 111 sample gold resources only 89 have an in-window file source. 14 accounts are activity-only and 8 resources are seen only out of window.

### R16 Ownership conflicts: OPEN (no sample)
File content beats an activity claim.
- evidence_60 shows marketing_001 = Soo-jin Park / sj.park@naver.com / +82 10-5837-9451. None of these match any user. activity_4008 claims marketing_001 belongs to user_09 (kwame-mensah, case_63).
- Proposal: exclude marketing_001 from case_63.

### R17 Gold resources with no admissible link to the subject: OPEN (new, affects the ship gate)
Over all 111 gold (case, resource) pairs, 77 are linked to the subject by an admissible file record. 8 are linked only by post-audit files (R3b). **26 are linked by no file record at all**:
- 17 accounts: case_01, 02, 04, 07, 08, 10, 18, 20, 21, 22, 23, 25, 28, 29, 30, 31, 32
- 7 anonymized analytics: case_03, 04, 21, 25, 26, 27, 28
- 2 audit records: case_18, 20

For accounts, the only participant trace is usually a deletion_worker `DELETE_RECORD "submitted primary profile account_X"` row near reported_at. These rows come in multi-case batches; cases 27, 28 and 29 share one batch with identical reported_at, so the batch alone cannot attribute them. account_004 appears nowhere. Anonymized analytics have every identifier null by construction.

**Consequence:** a headline of 32/32 exact-match is likely unreachable from participant data alone. Only case_05, 06, 11, 12, 13, 14, 15, 16, 17 and 19 have every gold resource admissibly linked. The SPEC_CARD §12 gate needs revisiting (participant decision).

- **UPDATE 2026-10-24 (R17 probe, code/analysis/r17_probe.py → scratch/r17_probe.txt), adopt only if explained ≥ 1 and FP = 0:**

| hypothesis | explained | FP | verdict |
|---|---|---|---|
| H1 unlinked account → account_{user_num:03d} | 6 (case_01, 02, 04, 07, 08, 10) | 14 (case_09, 18, 20, 21, 22, 23, 25-32) | REJECT |
| H2 shared non-identity key (ORD-/CS-/NST-/FIN-/segment-/trace ids) | 0 | 0 | REJECT |
| H3 activity per-row subject field | 0 | 2 (object_19, tombstone_17: R15 multi-request cases) | REJECT |
| H4 audit record seen in any file, even post-audit | 5 | 0 | **ADOPT** (see R6) |

  Engine v0 consequence: no resource is invented. Without an evidence path, the subject's account vABS and anonymized analytics vANON are omitted. Status is unaffected, because absence of evidence of presence is compliant (R4). Still unexplained: 17 accounts, 7 analytics, 2 audit records.

- **UPDATE 2026-10-24 (R17 probe 2, code/analysis/r17_probe2.py → scratch/r17_probe2.txt, dump scratch/r17_dump.txt):**

| hypothesis | explained | FP (samples) | test fires | verdict |
|---|---|---|---|---|
| H5 batch row carries a parallel subject list | 0 | 0 | 0 | REJECT: deletion_worker details are single-resource templates with no subject field |
| H6 elimination within a batch (accounts) | 0 | 0 | 3 | REJECT: batches always hold ≥2 unattributed accounts (case_28 vs case_29 share batch #187) |
| H7 conditional account_{num:03d} | 6 | 11 | 259 | REJECT |
| H7b … id exists in activity/evidence | 5 | 0 | 16 | REJECT: test fires collide with sample gold (account_410 = S case_23) |
| H7c … not attributed to another user | 5 | 0 | 9 | REJECT: same collisions (case_412→account_410, case_61→account_007 = S case_07) |
| **H7d** … user_num < 100 + deletion_worker DELETE of the padded id inside [requested_at, audit_at] | 5 | 0 | 0 | **ADOPT** (engine rule `r17_padded_account`) |
| H8 elimination (anonymized analytics) | 0 | 0 | 5 | REJECT: ANONYMIZE batches always hold ≥2 unattributed analytics ids |

  Decision: adopt H7d, because it explains 5 sample accounts with 0 FP and a principled evidence path (an in-window deletion_worker DELETE row). Rejected H5/H6/H8 because no batch carries subject information and elimination never leaves a unique candidate. Rejected H7/H7b/H7c because the unpadded form collides with real ids on the test set. **H7d fires on 0 test cases**: its gain is sample-only, and the test R17 count stays 342. Still unexplained: 15 accounts (incl. account_004, which has no row anywhere), 7 anonymized analytics, 2 audit records.

- **UPDATE 2026-10-24 (R17 probe 3, `r17_probe2.py probe3` → scratch/r17_probe3.txt).** Adopt only if explained ≥ 1, FP = 0, and no test collision with another case's sample gold resource.

| hypothesis | family | explained | FP | test fires | collisions | verdict |
|---|---|---|---|---|---|---|
| H7d' padded id, no <100 cutoff (in-window deletion_worker DELETE, not attributed elsewhere) | account | 5 | 0 | 0 | 0 | **ADOPT** (replaces H7d) |
| H7e padded id with no evidence path, iff no unattributed DELETE in window | account | 0 | 0 | 1 (case_63) | 0 | REJECT |
| H9a run membership, by activity_id / by event_time | account | 0 | 0 | 16 / 16 | 1 / 1 (case_51→account_5037 = S case_20) | REJECT |
| H9a run membership, by activity_id / by event_time | analytics | 0 | 0 | 21 / 21 | 0 | REJECT |
| H9b exact shared event_time / sub-batch id | account, analytics | 0 | 0 | 0 | 0 | REJECT: no deletion_worker row shares an exact event_time with any other row, and there is no sub-batch id field |

  Contiguity check: attributed rows form contiguous per-subject runs in only 35 of 132 batches that have ≥2 attributed subjects (identical by activity_id and by event_time), so run membership has no basis.
  Decision: adopt H7d', because it keeps 5 explained / 0 FP with no arbitrary cutoff and fires on no test case. Rejected H7e, H9a and H9b because they explain no sample (H9a also collides with S case_20's account). Decision: no step for a resource with 2+ candidate subjects, because a guess costs precision and can't be defended; rejected: a deterministic tie-break with no evidence basis. Test R17 coverage is unchanged (262 test subjects with no evidence-linked account, any-time linking).

- **262 vs 342:** the probe's 262 = test requests whose resolved user has no `account_*` id in any evidence record that names the user, at any capture time, nor in any LINK_RESOURCE_IDENTITY row. The run's 342 = authorized test cases for which the engine emitted no account step (flag `R17:no_account_evidence_path`). 342 = those 262 + 79 whose only linking record is captured after audit_at (excluded by R3) + 1 whose account R15 assigns to the user's other request. The 79 have the same shape as S case_09/26/27, whose gold does include the account. R17 is closed, so this was not probed (`scratch/run_report_before_p3.json`).
- **R17 CLOSED 2026-10-24:** no further account or analytics attribution probes. Known limitation recorded in code/evaluation/evaluation_report.md.

### R3c Ownership from any-time evidence, state from admissible evidence (adopted for accounts, 2026-10-24)
Which resources belong to the subject may use evidence captured at any time (still exact identity R2 + R15 request attribution). State and evidence_id use only admissible evidence (R3/R13). A resource linked only post-audit with no admissible observation gets its verify-only step; for accounts that is VERIFY_RECORD_ABSENT with the R13 absence citation. Engine: `r3c_post_audit_link` in code/engine/rules.py.

| family | explained | FP | evidence_id agree | status flips | test fires | verdict |
|---|---|---|---|---|---|---|
| account | 3 (S case_09 account_3960, S case_26 account_5684, S case_27 account_3866) | 0 | 3/3 | 0 | 79 | **ADOPT** |
| search | 0 | 0 | – | 0 | 14 | REJECT (no sample basis) |
| legal_hold | 0 | 0 | – | 0 | 2 (case_220, case_432) | REJECT (no sample basis) |
| analytics, support, export, data_flow, backup, tombstone, object, marketing | 0 | 0 | – | 0 | 0 | REJECT (no sample basis) |

For non-account families the samples contain no post-audit-only resource, so gold says nothing about them. Decision: adopt R3c for accounts, because it explains 3 gold accounts with 0 FP and 3/3 evidence agreement; rejected R3c for the other families, because they explain no sample (search would add steps to 14 test cases on no evidence). Effect: test R17 342 → 263; sample exact 16 → 17 (case_09); no status change on any test case (scratch/r3c_probe.txt).

### Settled 2026-10-24 (traps from scratch/trap_inventory.md)
- **case_45 media linking:** all six evidence_37 rows (audit_record_001..006) carry the subject in their own `identifiers.user_id` = user_03 (the Subject column of each row). case_45's oliver-bennett@gmail.com resolves to user_03. Each links through its own record (R2), not another record's panel. Decision: keep all six, no count cap, because each row is the subject's own record and capping without a ranking is unjustified; rejected a per-subject cap because no evidence orders the rows.
- **Legal holds:** deletion_rules.csv `rule_13,LEGAL_HOLD_RECORD,A supplied legal hold is active,RETAIN` and `rule_12,SECURITY_AUDIT_LOG,Record is within the supplied retention period,RETAIN` are both RETAIN, so legal_hold → VERIFY_RECORD_PRESENT on legal_service is **spec-backed** (same action as audit records).
  **H4-legal (spec-inferred, no sample):** a legal_hold seen in any file counts as existing at audit_at iff a RETAIN_RECORD SUCCESS activity for it has event_time ≤ audit_at; it is cited only from an admissible file (`h4_legal_exists` in rules.py). Effect: case_220 + legal_hold_4961 (activity_2264, 2026-06-08) and case_432 + legal_hold_438 (activity_801, 2026-03-02), each an uncited VERIFY_RECORD_PRESENT; no status change. Decision: adopt H4-legal, because rule_13 is RETAIN like rule_12 and an admissible RETAIN_RECORD SUCCESS row shows the hold was in force at audit_at; rejected leaving them out, because a retained record that must remain available would go unverified (PS L29).
- **R15 scope:** attribution already uses all 550 requests (32 sample + 518 test). user_18 has two test requests (case_52 2026-06-16..06-19, case_33 2026-07-16..07-19). account_2373 and audit_record_8486 are linked only by evidence_01 (2026-09-15), so they go to case_33. Decision: no change, because R15 already sees every request; the possibility of a third, unseen request of user_18 is noted but has no evidence.

