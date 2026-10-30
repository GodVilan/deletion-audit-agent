# SPEC_CARD: Ghost Data Still Exists (HackerRank Orchestrate, Oct 2026) — v2 (verified against repo files 08:20 CDT; line-checked 2026-10-24T14:05Z)
Citations: PS = problem_statement.md line, RD = original challenge README line (preserved verbatim at code/docs/CHALLENGE_README.md; the root README.md is now the solution README), AG = AGENTS.md section, ATI = agent_trace_instructions.md line, S = sample_output.csv case. "sample-inferred" = not in spec text.

Verification notation: under each line, `> ✓` quotes the spec sentence or sample row that supports it; `> ✗ CORRECTED` marks a fixed line number, count or claim (original wording shown struck through); `> ? UNSUPPORTED` marks a line with no support in the files. Counts come from `code/analysis/data_audit.py` (full output `scratch/audit_out.txt`) and sample traces from `code/analysis/gold_trace.py` (`scratch/gold_trace.txt`). §11 interpretations are the participant's and are left unchanged.

## 1. Task in one sentence
For each of 518 requests, decide whether deletion was authorized and, if so, whether it is truly COMPLETE at audit_at, then emit the ordered findings / remediation / verification steps (PS L9-11, L17-22; AG §1).
> ✓ PS L9 "For deletion requests, the agent must investigate the supplied records, determine the user's current and historical identifiers, reconstruct what happened across systems, and decide whether the deletion is actually complete." PS L19 "whether the deletion is `COMPLETE`, `INCOMPLETE`, or `NOT_APPLICABLE` because the person did not request deletion". AG §1 "For every request in `dataset/deletion_requests.csv`, the agent first determines whether the person actually requested deletion."

## 2. Inputs
| file | rows | key columns | joins / notes |
|---|---|---|---|
| deletion_requests.csv | 518 (case_33..case_550, contiguous, numeric order) | case_id,email,requested_at,reported_status,reported_at,audit_at,request_text | email = current OR historical (AG §6.2): 403 current exact, 15 current only case-insensitively, 100 historical, 0 unmatched; reported_status is a claim (PS L57): COMPLETE 254, PARTIALLY_COMPLETE 152, NOT_STARTED 112 |
| sample_deletion_requests.csv / sample_output.csv | 32 / 32 | same / case_id,deletion_status,steps_json | gold format reference (RD L73); 10 COMPLETE, 22 INCOMPLETE, 0 NOT_APPLICABLE; 29 current + 3 historical emails |
| user_identities.csv | 850 | user_id,name,email,phone,email_hash,updated_at | current snapshot (AG §6.1) |
| user_audit_log.csv | 306 | audit_id,user_id,event_time,field_name,old_value,new_value | field_name: email 107, email_hash 107, phone 92 (AG §6.1) |
| system_activity.csv | 4011 | activity_id,event_time,event_type,source_system,target_system,resource_id,reported_result,details | global, unrelated people; results are claims (AG §6.1). Includes 12 LINK_RESOURCE_IDENTITY, 10 CLASSIFY_REQUEST, 1 RESTORE_BACKUP |
| deletion_rules.csv | 15 | rule_id,data_category,condition,required_action | policy (PS L26) |
| evidence_files.csv | 94 | file_id,file_path,origin,captured_at | manifest does not identify case/user (AG §6.1, §6.6) |
| evidence/ | 24 .sql, 26 .log, 28 .json, 1 .txt, 11 .png, 4 .pdf | multi-user point-in-time snapshots | SQL = primary/regional/reporting/failover replicas, compare for drift (RD L59, AG §6.6) |

- deletion_requests.csv
  > ✓ audit a: rows=518, unique_ids=518, no blanks; range case_33..case_550, contiguous=True, input_order==numeric_order=True, ==lexicographic=False. Audit b: current_exact 403, current_case_insensitive 15, historical_exact 95 + historical_case_insensitive 5 = 100, unmatched 0, ambiguous 0. reported_status COMPLETE 254 / NOT_STARTED 112 / PARTIALLY_COMPLETE 152. AG §6.2 "It may be a current or historical email address." PS L57 "It is a claim from the existing deletion workflow, not proof of the true state."
- sample files
  > ✓ 32/32 rows; gold COMPLETE 10 / INCOMPLETE 22; resolution current_exact 29, historical_exact 3 (case_10, case_29, case_30). RD L73 "Use `dataset/sample_output.csv` as the format reference." Note: sample case_ids are zero-padded (case_01..case_32), test ids are not.
- user_identities.csv
  > ✓ rows=850, unique user_id, no blanks. AG §6.1 "`user_identities.csv` contains the current identity snapshot for each user".
- user_audit_log.csv
  > ✓ rows=306; field_name {'email': 107, 'email_hash': 107, 'phone': 92}. AG §6.1 "records historical changes to identity fields".
- system_activity.csv
  > ✓ rows=4011; LINK_RESOURCE_IDENTITY 12, CLASSIFY_REQUEST 10, RESTORE_BACKUP 1. AG §6.1 "Its rows may describe unrelated people. Determine resource state from the available evidence rather than trusting workflow or operation results alone." Extra fact: activity rows are not in event_time order (activity_4000..4011 are back-dated LINK rows).
- deletion_rules.csv
  > ✓ rows=15. PS L26 "every relevant copy has received the treatment required by `deletion_rules.csv`".
- evidence_files.csv
  > ✓ rows=94. AG §6.1 "The manifest does not identify which case or user a file concerns; the solution must connect evidence through its contents and identifiers." AG §6.6 "Do not infer case membership from the manifest alone."
- evidence/
  > ✓ extensions {.log 26, .json 28, .txt 1, .png 11, .sql 24, .pdf 4}; byte-sniff agrees (no binary SQLite). All 4 PDFs have a text layer (pypdf). RD L59 "SQL captures may contain a primary database, regional replicas, a reporting replica, or a failover replica so replication drift can be investigated directly." AG §6.6 "SQL evidence can contain primary, regional, reporting, or failover replicas." Extra fact: the 11 `customer_data_inventory_*.sql` files are not replica pairs; they hold one table per data family plus a `snapshot_scope` table.

## 3. Output contract
| column | type | allowed | format | source |
|---|---|---|---|---|
| case_id | str | ids from deletion_requests.csv | exactly 518 rows, sorted by case_id (see A1) | PS L61, L73 |
| deletion_status | enum | COMPLETE, INCOMPLETE, NOT_APPLICABLE | uppercase | PS L70 |
| steps_json | JSON array string | objects with exactly: step_no (int), phase, system_id, resource_id, operation, state, evidence_id (str) | NOT_APPLICABLE -> []; future steps -> ""; sample serializes compact; key order varies (8 rows sorted keys, 24 rows schema order) — cosmetic, PS L99 | PS L75-91, AG §6.3 |
Allowed (phase, operation, state) = the 15 rows of PS L105-119; the operation fixes the state. Do not invent others (AG §6.4).

- case_id
  > ✓ PS L61 "Produce exactly one row in `output.csv` for every case in `deletion_requests.csv`". PS L73 "The final file must contain exactly 518 data rows, sorted by `case_id`."
- deletion_status
  > ✓ PS L70 "| `deletion_status` | `COMPLETE`, `INCOMPLETE`, or `NOT_APPLICABLE` |".
- steps_json
  > ✓ PS L75 "Each object in `steps_json` must contain:" (L77-87 schema); PS L91 "For `NOT_APPLICABLE`, use an empty JSON array (`[]`)"; AG §6.3 "Each step contains exactly these fields". PS L99 "JSON object-key order and whitespace are ignored; array order is not."
  > ✗ CORRECTED: ~~sample serializes compact with sorted keys~~ → only 8/32 sample rows use sorted keys (case_01, 02, 04, 05, 06, 07, 08, 10); 24/32 use schema order (step_no first). Both compact `(",", ":")`. Cosmetic either way.
- 15 (phase, operation, state) rows
  > ✓ PS L103-119 table has exactly 15 data rows (L105-L119). AG §6.4 "Do not invent additional phases, operations, or states."

## 4. Cross-field invariants (testable)
- I1 header == case_id,deletion_status,steps_json; 518 unique case_ids == input ids (PS L73).
  > ✓ PS L64 `case_id,deletion_status,steps_json`; PS L73 "exactly 518 data rows". AG §6.3 "these exact columns, in this order".
- I2 NOT_APPLICABLE <=> steps == [] (PS L91).
  > ✓ PS L91 "For `NOT_APPLICABLE`, use an empty JSON array (`[]`) because no deletion or deletion verification is authorized." The <= direction (authorized => non-empty) holds in all 32 samples (I10).
- I3 COMPLETE => every step phase == VERIFICATION, evidence_id non-empty and a valid file_id/activity_id/audit_id (PS L91, L127).
  > ✓ PS L91 "For `COMPLETE`, include only verification steps proving the current state." PS L127 "Findings and verification steps for `COMPLETE` cases must cite a `file_id`, `activity_id`, or `audit_id`." Holds on 10/10 COMPLETE samples (scratch/verify_card.py: 0 violations).
- I4 INCOMPLETE => >=1 FINDING; every FINDING evidence_id non-empty; every REMEDIATION and VERIFICATION evidence_id == "" (PS L127, AG §6.6).
  > ✓ PS L127 "Proposed remediation and future verification steps for `INCOMPLETE` cases use an empty `evidence_id`." AG §6.6 "A finding must use the participant-visible `file_id`, `activity_id`, or `audit_id` that proves it." Holds on 22/22 INCOMPLETE samples.
- I5 step_no == position (1-based, consecutive) (PS L89).
  > ✓ PS L89 "Step numbers start at `1` and increase consecutively." 32/32 samples.
- I6 order key = (phase rank, operation rank in table, system_id, resource_id) (PS L126).
  > ✓ PS L126 "Within each phase, follow the operation order in the table above, followed by `system_id` and `resource_id` in ascending order." 32/32 samples are sorted by this key.
- I7 state == the table state for the operation (PS L105-119).
  > ✓ PS L105-119; 0 violations in samples.
- I8 every cited file has captured_at <= audit_at; cited activity/audit ids have event_time <= audit_at (AG §6.2, §6.6).
  > ✓ AG §6.6 "Never cite organizer-only truth or an evidence item captured after the case's `audit_at`." AG §6.2 "Use only information available at or before `audit_at`". Audit z: 0 sample citations after audit_at (manifest captured_at).
- I9 finding->remediation->verification pairing: REMAINING->DELETE->VERIFY_ABSENT; EXPOSED_PII->REDACT/ANONYMIZE->VERIFY_REDACTED/ANONYMIZED; ACTIVE_DATA_FLOW->DISABLE->VERIFY_FLOW_DISABLED; RESTORE_RISK->BLOCK->VERIFY_RESTORE_BLOCKED (sample-inferred: all 22 INCOMPLETE rows).
  > ✓ sample-inferred: 0 violations in 22 INCOMPLETE rows, and no remediation step lacks a matching finding. Spec support is partial: AG §6.5 "Verification must cover the required final state for each remediated record or process."
- I10 every authorized case (32/32 samples) contains VERIFY_RECORD_ABSENT for the subject's account on account_service, even when the account itself needs no remediation (sample-inferred, S all).
  > ✓ sample-inferred: 32/32. 19 INCOMPLETE samples verify the account ABSENT without remediating it (case_06-15, 17-20, 22, 23, 29, 30, 32).

## 5. Decision rules stated in the spec
- D1 Decide first whether request_text authorizes deletion. Access, correction, export, marketing opt-out or other non-deletion -> NOT_APPLICABLE "even if other fields resemble a deletion case". Text may be multilingual (AG §6.5, §6.2).
  > ✓ AG §6.5 "A request for access, correction, export, marketing opt-out, or another non-deletion action is `NOT_APPLICABLE`, even if other fields resemble a deletion case." AG §6.2 "`request_text` contains the person's request and may be written in different languages."
- D2 Resolve current and historical identifiers; request email may be either (AG §6.5).
  > ✓ AG §6.5 "Resolve both current and historical identifiers for the subject. The request email may match either form." Also PS L123.
- D3 State at audit_at only; later evidence must not change the answer; reported_status/reported_result are claims (PS L124, AG §6.2, §6.5).
  > ✓ PS L124 "Determine the resource state at `audit_at` using the available evidence. Reported workflow statuses and operation results are claims." AG §6.2 "Evidence created later must not change the answer for that case." AG §6.5 "Ignore later evidence and do not accept `reported_status` or `reported_result` as proof."
- D4 COMPLETE only if: every relevant copy has the deletion_rules treatment; no active sync/import/restore path; retained records hold only permitted identifiers; must-retain records remain available (PS L24-29).
  > ✓ PS L24-29 (four bullets, verbatim content). AG §6.5 restates it.
- D5 deletion_rules.csv: USER_PROFILE, SECONDARY_IDENTIFIER, SEARCH_INDEX_ENTRY, CACHE_ENTRY, USER_EXPORT, MARKETING_PROFILE -> DELETE (always); SUPPORT_MESSAGE with shared customer/agent/order context -> REDACT; SUPPORT_ATTACHMENT belonging only to subject -> DELETE; ANALYTICS_PROFILE, PRODUCT_TELEMETRY still attributable -> ANONYMIZE; EMAIL_DELIVERY_LOG containing an email -> REDACT; SECURITY_AUDIT_LOG within retention -> RETAIN; LEGAL_HOLD_RECORD with active hold -> RETAIN; BACKUP_ARCHIVE whose restore can be blocked -> RETAIN; ACCOUNT_TOMBSTONE -> REDACT (rule_01..rule_15).
  > ✓ deletion_rules.csv rule_01..rule_15 match one-for-one (rule_01/02/03/04/09/10 "Always,DELETE"; rule_05 REDACT; rule_06 DELETE; rule_07/08 ANONYMIZE; rule_11 REDACT; rule_12/13/14 RETAIN; rule_15 REDACT).
- D6 ACCOUNT_TOMBSTONE keeps the stable user_id; name, email, phone, email_hash removed (PS L13, AG §6.5).
  > ✓ PS L13 "the stable user reference may remain, but direct identifiers such as name, email, phone, and email hash must be removed." AG §6.5 "preserve the stable subject reference and remove the name, email, phone, email hash". S case_31/32 (tombstone_440 nulls -> VERIFY_REDACTED; tombstone_9178 still has name/email/phone/hash -> EXPOSED_PII+REDACT).
- D7 INCOMPLETE reports every violation and recreation risk supported by participant-visible evidence (AG §6.5).
  > ✓ AG §6.5 "For an incomplete case, report every relevant policy violation and recreation risk supported by participant-visible evidence."
- D8 Verification covers the required final state of each remediated record or process (AG §6.5).
  > ✓ AG §6.5 "Verification must cover the required final state for each remediated record or process."

## 6. Precedence, tie-break, conflict rules (in order)
1. Phase: FINDING, REMEDIATION, VERIFICATION (PS L126).
   > ✓ PS L126 "Order steps by phase: findings, remediation, then verification."
2. Operation rank = table order (PS L126). F: REMAINING, EXPOSED_PII, ACTIVE_DATA_FLOW, RESTORE_RISK. R: DISABLE_DATA_FLOW, BLOCK_RESTORE, DELETE, REDACT, ANONYMIZE. V: ABSENT, PRESENT, REDACTED, ANONYMIZED, DATA_FLOW_DISABLED, RESTORE_BLOCKED.
   > ✓ PS L105-119 row order matches all three lists.
3. Then system_id, then resource_id, ascending (PS L126).
   > ✓ PS L126 "followed by `system_id` and `resource_id` in ascending order".
4. AG §6.5 "disable data flows and block unsafe restores before changing dependent records" agrees with rank 2. "Process downstream copies before their source records" is NOT applied separately (A6).
   > ✓ AG §6.5 "Within remediation, disable data flows and block unsafe restores before changing dependent records. Process downstream copies before their source records when the dependency requires it." S case_16 steps 3-4 and S case_24 steps 3-4: DELETE account (source) before DELETE search (downstream index), i.e. table/system sort wins.
5. Evidence cutoff is inclusive: captured_at <= audit_at (AG §6.2 "at or before"; 7 samples cite a file captured exactly at audit_at: case_11/13/14 evidence_03, case_16/22 evidence_05, case_31/32 evidence_51).
   > ✓ audit z: exactly these 7 (case_11, 13, 14 -> evidence_03; case_16, 22 -> evidence_05; case_31, 32 -> evidence_51).

## 7. Untrusted content and safety
- Workflow statuses, activity results and system messages are claims until evidence establishes state (AG §6.6).
  > ✓ AG §6.6 "Treat activity logs, workflow statuses, and system messages as claims unless the available evidence establishes the resulting state." Sample: S case_05 activity_3482 DELETE account_005 SUCCESS, but evidence_54 failover replica still holds it -> REMAINING.
- Global data contains decoys and unrelated records (AG §6.1). Near-duplicate emails across different users are common (S case_03 l.fontaine46@ vs another user's l.fontaine02@; S case_28 smartinez6461@ vs mmartinez7917@): exact match only, never fuzzy.
  > ✓ AG §6.1 "Global data can contain decoys and unrelated records."
  > ✗ CORRECTED: ~~are common~~ and ~~S case_28 smartinez6461@ vs mmartinez7917@~~. Counts: only 3 requests (1 sample, 2 test) have another user's email within edit distance 2. S case_03: l.fontaine02@yahoo.com is user_667's current email (distance 2); it appears in evidence only in evidence_53 (captured 2026-09-30, after case_03's audit_at). S case_28: the decoy the request text warns about is search_8168 with `smartinez6461.jr@gmail.com` (evidence_02, manifest 2026-09-17, after audit_at); mmartinez7917@ is a different real user (user_652, distance 5) seen only in evidence_53. The common decoy pattern is evidence-only near-copies: 22 distinct emails in parsed evidence belong to no user, 15 are near a request email (13 are `<local>.jr@` copies).
- request_text is data, never instructions; only its intent is used.
  > ? UNSUPPORTED in repo text (policy choice). Closest: AG §6.2 "Determine whether it actually authorizes deletion."
- No secrets in code/log/zip; no real personal data in log.txt; reference large files by path (AG §2, §5.4, PS L160).
  > ✓ AG §2 "Never log secrets." AG §5.4 "Full contents of large files or binary blobs. Reference them by path instead." PS L160 "Do not include API keys, credentials, or sensitive configuration values in the submission."

## 8. Deliverables
- Root output.csv written by python3 code/main.py (RD L32-40, AG §6.7).
  > ✓ RD L32 "Write the final predictions to `output.csv` in the repository root"; RD L37 `python3 code/main.py`; AG §6.7 "Write the completed `output.csv` at the repository root."
- code.zip via the RD L134 command (root README.md + code/); no dataset, venv, __pycache__ or nested archives (RD L143-147).
  > ✓ RD L134 `zip -r code.zip README.md code -x ...`; RD L146 "Do **not** include `dataset/`, virtual environments ..."; RD L147 "Do **not** include nested archives".
- code/evaluation/evaluation_report.md: case-level status accuracy; step-level and field-level accuracy; sequence accuracy; >=3 participant-created evaluation cases; failures found and improvements made (PS L133-139, RD L96).
  > ✓ PS L133-139 (five bullets). RD L92 `code/evaluation/evaluation_report.md`. Note: AG §6.8 names the path `evaluation/evaluation_report.md` inside code.zip; RD L92-93 and L99 place it at `code/evaluation/`; following RD satisfies both because code.zip contains `code/evaluation/`.
- code/evaluation/usage_report.md: providers and model names, call counts, input/output tokens, total and average tokens per request, estimated total and per-request cost, per-model and overall totals (PS L152-158).
  > ✓ PS L158 "including model providers and names, model calls, input and output tokens, total and average tokens per request, and estimated total and per-request cost. If multiple models are used, include both per-model and overall totals".
- All metrics and prompts in .md/.py: the code judge and AI interviewer ignore .csv/.tsv/.json/.jsonl/.sql/.log (RD L99).
  > ✓ RD L99 "Automated code evaluation ignores raw data files (`.csv`, `.tsv`, `.json`, `.jsonl`, `.sql`, `.log`), so content stored only in those formats will not be visible to the code judge or AI interviewer."
- chat_transcript = root log.txt per AG §5 (RD L105-113). Every SESSION START and per-turn entry needs exact, non-placeholder tool= and model= lines or it is invalid (AG §5.2 mandatory rules, §9).
  > ✓ RD L113 "Upload `log.txt` directly as your `chat_transcript` submission on HackerRank." AG §5.2 "The entry is invalid if `tool=` is missing, blank, still contains a placeholder ..."
- agent-trace.zip of every session used, including planning sessions; Claude Code: ~/.claude/projects/ JSONL + /export; claude.ai chats: Settings → Privacy → Export data, relevant conversations only (ATI L3-5, L19-36). Request the claude.ai export early: it arrives by email.
  > ✓ ATI L3 "submit the complete agent trace ... as a **ZIP file**"; ATI L5 "Include every session you used ... including sessions in which you planned, coded, debugged, or reviewed"; ATI L21 `~/.claude/projects/`; ATI L31 `/export`; ATI L36 "use **Settings → Privacy → Export data**". "arrives by email" is ? UNSUPPORTED in repo text (external knowledge; ATI L36 says only "follow the download instructions").
- Deadline (supplied by participant, AG §3.3): Sun 2026-10-25 07:30 CDT = 12:30 UTC. Confirm against the challenge email.
  > ✓ AG §3 item 3 "If a higher-priority instruction or an official repository update supplies the end time, calculate and display the time remaining." The time itself is participant-supplied (not in repo).
- AG §4.1 submission URL contains a typo ("wwww.hackerrank.com"); use the link from the official email.
  > ✓ AG §4.1 "https://wwww.hackerrank.com/contests/hackerrank-orchestrate-october26/challenges/ghost-data-still-exists" (four w's). Note AG §4.1 also requires quoting that exact URL whenever asked for the submission link.

## 9. How output is scored
Hidden canonical answers; considers deletion_status, identity resolution, discovered records and risks, cited evidence, policy decisions, completeness and order of steps_json (PS L131, RD L81-87). No weights stated. JSON is parsed: key order and whitespace ignored, array order significant (PS L99).
> ✓ PS L131 "Scoring will consider the correctness of `deletion_status`, identity resolution, discovered records and risks, cited evidence, policy decisions, and the completeness and order of `steps_json`." RD L81-87 (five bullets). No weights anywhere in PS/RD/AG.

## 10. Forbidden
Organizer-only files (e.g. generator/, golden answers; anything outside dataset/ used for predictions) (AG §4 rule 3, §6.1); hardcoded labels or case-family shortcuts (AG §6.7); keying logic on case_id; citing evidence captured after audit_at (AG §6.6); inferring case membership from the manifest alone (AG §6.6); inventing phases, operations or states (AG §6.4); secrets (PS L160).
> ✓ AG §4 rule 3 "Organizer-only truth, golden answers, review files, and generator internals must never be used for predictions." AG §6.7 "Do not use organizer-only files, hardcoded golden labels, or case-family shortcuts." AG §6.6 (two quotes above). AG §6.4. PS L160. "keying logic on case_id" is ? UNSUPPORTED as literal text (project rule in CLAUDE.md; consistent with AG §6.7 "case-family shortcuts").

## 11. Ambiguities
| # | question | spec text | sample evidence | chosen interpretation | basis |
|---|---|---|---|---|---|
| A1 | case_id sort | "sorted by case_id" PS L73 | samples case_01..32; test case_33..case_550 unpadded, contiguous, input in numeric order; lexicographic sort would differ (case_100 < case_33) | numeric order (= input order) | inferred; low risk if grader joins on id |
| A2 | resource_id tie-break | "ascending" PS L126 | no sample has two resources with same op+system | plain string ascending (search_1007 < search_898) | spec literal, unverified |
| A3 | verification scope in INCOMPLETE | "each remediated record or process" AG §6.5 | S case_06/07/08/10 verify account ABSENT without remediating it (I10); audit_record VERIFY_PRESENT in S case_03, 09, 11-32 | verify the required final state of every relevant subject resource: account (always), retained audit record, every remediated resource | sample-inferred |
| A4 | backup handling | rule_14 RETAIN | S case_09/14/17: RESTORE_RISK -> BLOCK_RESTORE -> VERIFY_RESTORE_BLOCKED, never REMAINING or VERIFY_PRESENT; S case_26-28 COMPLETE verify RESTORE_BLOCKED | as samples | sample-inferred |
| A5 | retained security audit record | rule_12 RETAIN; "must remain available" PS L29 | only ever VERIFY_RECORD_PRESENT; absent in S case_01,02,04-08,10 | include iff subject has one at audit_at; missing-but-required: open (no restore op) | open, audit must count |
| A6 | downstream-before-source vs table sort | AG §6.5 vs PS L126 | S case_16 and case_24 delete account before search (sort wins) | PS L126 ordering only | sample-backed |
| A7 | analytics DELETE vs ANONYMIZE | rule_07 ANONYMIZE | S case_11/18/22/29/30 EXPOSED_PII+ANONYMIZE; S case_12 analytics_9914 REMAINING+DELETE (cites evidence_01) | open: find what makes analytics_9914 a DELETE category in evidence_01 | open |
| A8 | support REDACT vs DELETE | rule_05 vs rule_06 | REDACT S case_11/18/19/29/30; DELETE S case_07/10/13 | decided by record content (shared context vs subject-only attachment); deciding field TBD | sample-backed, mechanism open |
| A9 | which evidence id per step | "the id that proves it" AG §6.6 | S case_04 cites evidence_54 (account) + evidence_56 (analytics); case_11-32 cite one file per case; samples never cite activity/audit ids | latest file captured <= audit_at that observes that resource; activity/audit id only when no file observes it | sample-inferred, tie rule unverified |
| A10 | cutoff inclusive? | "at or before" AG §6.2 | S case_11/13/14/16/22/31/32 (cited file captured == audit_at) | inclusive | spec + sample |
| A11 | identifier matching | AG §6.6 | 20 test request emails contain uppercase (all 20 resolve only case-insensitively: 15 current, 5 historical); S case_28 decoy | case-insensitive exact match on email/email_hash/phone/user_id/resource_id; never fuzzy | sample-backed + inferred |
| A12 | NOT_APPLICABLE | AG §6.5 | 0 of 32 samples; exactly 10 test texts are non-deletion: case_533-542 (all reported NOT_STARTED); 5 contain negated deletion words (534, 536, 537, 539, 542); 10 CLASSIFY_REQUEST rows say "classified ... as non-deletion" | classify intent from request_text only (model, multilingual, negation-aware); CLASSIFY_REQUEST = corroborating claim only | spec-backed; no sample -> custom eval cases |
| A13 | already-disabled flow / already-blocked backup inside an INCOMPLETE case | - | none | include their VERIFY step (A3) | open |
| A14 | README in code.zip | RD L134 zips root README.md | - | our README replaces root README.md | decision |
| A15 | two sample families | AG §7 "never hand-edit golden output" | S case_01-10 cite evidence_54-61/93/94 (system-named origins, 4 of 8 undated filenames: 55, 58, 60, 61) and mostly lack audit records; S case_11-32 cite bundles evidence_01/03/05/51/92/94 | both are generated gold conventions; never "noisy" | playbook rule 3 |
| A16 | rule categories and systems with no sample | D5 | none for CACHE_ENTRY (cache_service, 284 activity rows), EMAIL_DELIVERY_LOG (email_delivery_service, 368), LEGAL_HOLD_RECORD (legal_service, 10), MARKETING_PROFILE (marketing_platform; evidence_60 PNG uncited), PRODUCT_TELEMETRY, SECONDARY_IDENTIFIER, object storage | apply D5 + I9: DELETE categories -> REMAINING/DELETE/VERIFY_ABSENT; REDACT -> EXPOSED_PII/REDACT/VERIFY_REDACTED; ANONYMIZE -> EXPOSED_PII/ANONYMIZE/VERIFY_ANONYMIZED; legal hold -> VERIFY_RECORD_PRESENT like audit records | spec + sample-inferred; custom eval case per category |
| A17 | system_id when a resource appears in several systems | PS L126 | gold uses the owning system: account_service for account_005 found in evidence_54 (failover replica); security_service for audit records although 196/197 activity rows target archive_service; export_service although 155/189 export rows target object_store | canonical owning system per resource family, not the capture or activity target | sample-backed; confirm in gold trace |
| A18 | identity-link and recreation activity | AG §6.6 | 12 LINK_RESOURCE_IDENTITY rows (data_catalog links resource -> email + user_id); 1 RESTORE_BACKUP (backup_9287 repopulated search_4882) | use as linking/recreation evidence when <= audit_at; corroborate with files when possible; citable as activity_id | spec-backed, usage open |

Row-level checks (interpretations unchanged; disagreements and new evidence are in the session reply, not here):
- A1 > ✓ audit a: test ids unpadded case_33..case_550, input order == numeric order, != lexicographic; sample ids zero-padded so the sample cannot disambiguate.
- A2 > ✓ scratch/verify_card.py: no sample has two steps with the same (operation, system_id). `"search_1007" < "search_898"` under plain string compare.
- A3 > ✓ the four cited cases are correct; the full set is 19 INCOMPLETE samples (see I10). audit_record VERIFY_PRESENT appears in exactly case_03, 09, 11-32 (24 cases).
- A4 > ✓ S case_09 backup_4978, case_14 backup_3870, case_17 backup_3245: REPORT_RESTORE_RISK -> BLOCK_RESTORE -> VERIFY_RESTORE_BLOCKED; S case_26/27/28 VERIFY_RESTORE_BLOCKED (evidence_92 `"restore_allowed": false`). No backup ever gets REMAINING or VERIFY_PRESENT.
- A5 > ✓ complement of A3's list: case_01, 02, 04, 05, 06, 07, 08, 10.
- A6 > ✓ see §6.4.
- A7 > ✓ samples as stated (analytics EXPOSED_PII+ANONYMIZE in case_11, 18, 22, 29, 30; case_12 REMAINING+DELETE from evidence_01).
- A8 > ✓ REDACT case_11, 18, 19, 29, 30; DELETE case_07, 10, 13.
- A9 > ✓ case_04 cites evidence_54 + evidence_56; case_11-32 each cite one file; 0 activity/audit ids cited. Tested: for every cited step whose resource appears in some parsed file <= audit_at, the cited file is the latest such file (0 exceptions). The rule does not cover absence proofs: case_01/02/04 cite evidence_54 and case_31 cites evidence_51 although the account id does not appear in that file.
- A10 > ✓ see §6.5.
- A11 > ✗ CORRECTED: ~~(15 resolve only case-insensitively)~~ → all 20 uppercase emails resolve only case-insensitively (15 current, 5 historical). S case_28 decoy is search_8168 `smartinez6461.jr@gmail.com` (see §7).
- A12 > ✓ case_533-542 all NOT_STARTED; full scan of 375 distinct test texts finds no other non-deletion text; the 10 CLASSIFY_REQUEST accounts link one-to-one to case_533..542's users through evidence. ✗ CORRECTED: negated list ~~534, 536, 538, 539, 542~~ → 534, 536, 537 ("without removing"), 539, 542; case_538 is a scoped opt-out ("remove me from marketing lists only"), not a negation.
- A13 > ? no sample (as stated).
- A14 > ✓ RD L134 includes root `README.md`.
- A15 > ✓ case_01-10 cite evidence_54, 56-59, 61, 93, 94 (case_03 -> evidence_94, case_09 -> evidence_93). ✗ CORRECTED: ~~undated filenames~~ → only evidence_55, 58, 60, 61 have undated filenames; 54, 56, 57, 59 are dated. Audit records present only in case_03 and case_09 of the first family.
- A16 > ✓ REFRESH_CACHE 284 (cache_* -> cache_service); SEND_EMAIL 368 (email_delivery_* -> email_delivery_service); RETAIN_RECORD 10 (legal_hold_* -> legal_service); marketing_001 only in evidence_60 (PNG) and activity_4008. Literal SECONDARY_IDENTIFIER, CACHE_ENTRY, PRODUCT_TELEMETRY, MARKETING_PROFILE, EMAIL_DELIVERY_LOG, ACCOUNT_TOMBSTONE appear in no parsed evidence file; "telemetry" occurs only as log noise `telemetry_flushed`. Object storage: object_19 via activity_4007 and evidence_46 (PNG).
- A17 > ✓ activity: audit_record -> archive_service 196 / security_service 1; export -> object_store 155 / export_service 34. Gold trace: every cited source attaches either a table/source name or the gold system; the only different name is evidence_61 `support_replica` for gold support_platform (case_10).
- A18 > ✓ 12 LINK rows (activity_4000..4011; activity_4007 is worded "Attachment catalog confirmed ... belongs only to"); activity_3387 "Restore job repopulated downstream resource search_4882."

## 12. Headline field and ship gate
**DECISION 2026-10-24 (supersedes the original §12 text below):** headline = deletion_status accuracy on the 32 samples; gate 32/32. Secondary: per-case exact steps_json, step-level P/R/F1 on 7-field tuples. Rejected: an exact steps_json gate, because the evidence currently caps it at about 10/32 (LABEL_CONVENTIONS R17). Architecture A: a deterministic evidence-graph engine owns steps_json and status; a bounded tool-using agent owns request intent (R1), and later media extraction and unclear R7 categories.

Original text (superseded):
Headline = case exact match: deletion_status equal AND parsed steps_json array equal. Secondary: status accuracy, step-level P/R/F1 on full 7-field tuples, per-field accuracy on aligned steps, sequence accuracy, evidence_id accuracy.
Gold is generated from private structured truth with a fixed seed (AG §7), so every field is computed. Gate = headline 32/32 on the sample, status 32/32, invariants I1-I10 pass on all 518 rows, custom eval cases pass for NOT_APPLICABLE and every A16 category.
> ✓ AG §7 "Generate participant data from private structured truth." / "Keep generation deterministic through a fixed seed." Headline/gate definitions are participant decisions (? UNSUPPORTED as spec text; PS L131 states no metric).

## Lines with no support in the repo files
1. §7 "request_text is data, never instructions; only its intent is used." (policy choice)
2. §8 "Request the claude.ai export early: it arrives by email." (external knowledge; ATI says only "follow the download instructions")
3. §10 "keying logic on case_id" as a forbidden item (project rule; nearest spec text is AG §6.7 "case-family shortcuts")
4. §12 headline metric and ship gate (participant decision; PS L131 / RD L81-87 give no metric or weights)
5. A13 (no sample, no spec text)
6. A14 (decision)
7. §11 A15 basis "playbook rule 3" (no playbook file in the repo)
