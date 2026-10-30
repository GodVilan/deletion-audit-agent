# Run history

Raw sections appended by `code/evaluation/main.py` (and earlier by `score_sample.py`), oldest first. The current summary is in [evaluation_report.md](evaluation_report.md).

## Sample run 2026-10-24T14:29Z

```text
SAMPLE SCORE
  status_accuracy: 31/32
  exact_steps_json: 11/32
  step_P: 0.7267
  step_R: 0.6062
  step_F1: 0.661
  core_step_recall(6-field, ignoring evidence/step_no): 161/193
  evidence_id_acc_on_matched: 161/161
  sequence_exact(core order): 11/32
  intent_paths: {'fallback': 32}
  status confusion (gold -> pred): COMPLETE->COMPLETE: 10, INCOMPLETE->COMPLETE: 1, INCOMPLETE->INCOMPLETE: 21
  headline before: 31/32  after: 31/32  (no drop)
  flipped vs last run: none
MISSES (21 cases)
  case_01
     R5/R17 MISSING VERI account_service account_001 VERIFY_RECORD_ABSENT
  case_02
     R5/R17 MISSING VERI account_service account_002 VERIFY_RECORD_ABSENT
  case_03
     R7/R8 MISSING VERI analytics_platform analytics_9406 VERIFY_RECORD_ANONYMIZED
  case_04
     R5/R17 MISSING VERI account_service account_004 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_901 VERIFY_RECORD_ANONYMIZED
  case_07
     STATUS gold INCOMPLETE got COMPLETE
     R7/R8 MISSING FIND support_platform support_001 REPORT_REMAINING_RECORD
     R7/R8 MISSING REME support_platform support_001 DELETE_RECORD
     R5/R17 MISSING VERI account_service account_007 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI support_platform support_001 VERIFY_RECORD_ABSENT
  case_08
     R5/R17 MISSING VERI account_service account_008 VERIFY_RECORD_ABSENT
  case_09
     R5/R17 MISSING VERI account_service account_3960 VERIFY_RECORD_ABSENT
  case_10
     R5/R17 MISSING VERI account_service account_010 VERIFY_RECORD_ABSENT
  case_18
     R5/R17 MISSING VERI account_service account_5521 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_6645 VERIFY_RECORD_PRESENT
  case_20
     R5/R17 MISSING VERI account_service account_5037 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_5569 VERIFY_RECORD_PRESENT
  case_21
     R5/R17 MISSING VERI account_service account_6440 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_5335 VERIFY_RECORD_ANONYMIZED
  case_22
     R5/R17 MISSING VERI account_service account_4990 VERIFY_RECORD_ABSENT
  case_23
     R5/R17 MISSING VERI account_service account_410 VERIFY_RECORD_ABSENT
  case_25
     R5/R17 MISSING VERI account_service account_3136 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_1895 VERIFY_RECORD_ANONYMIZED
  case_26
     R5/R17 MISSING VERI account_service account_5684 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_4566 VERIFY_RECORD_ANONYMIZED
  case_27
     R5/R17 MISSING VERI account_service account_3866 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_4574 VERIFY_RECORD_ANONYMIZED
  case_28
     R5/R17 MISSING VERI account_service account_5482 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_6077 VERIFY_RECORD_ANONYMIZED
  case_29
     R5/R17 MISSING VERI account_service account_7012 VERIFY_RECORD_ABSENT
  case_30
     R5/R17 MISSING VERI account_service account_4163 VERIFY_RECORD_ABSENT
  case_31
     R5/R17 MISSING VERI account_service account_4857 VERIFY_RECORD_ABSENT
  case_32
     R5/R17 MISSING VERI account_service account_8858 VERIFY_RECORD_ABSENT
```

## Sample run 2026-10-24T14:30Z

```text
SAMPLE SCORE
  status_accuracy: 31/32
  exact_steps_json: 11/32
  step_P: 0.7267
  step_R: 0.6062
  step_F1: 0.661
  core_step_recall(6-field, ignoring evidence/step_no): 161/193
  evidence_id_acc_on_matched: 161/161
  sequence_exact(core order): 11/32
  intent_paths: {'fallback': 32}
  status confusion (gold -> pred): COMPLETE->COMPLETE: 10, INCOMPLETE->COMPLETE: 1, INCOMPLETE->INCOMPLETE: 21
  headline before: 31/32  after: 31/32  (no drop)
  flipped vs last run: none
MISSES (21 cases)
  case_01
     R5/R17 MISSING VERI account_service account_001 VERIFY_RECORD_ABSENT
  case_02
     R5/R17 MISSING VERI account_service account_002 VERIFY_RECORD_ABSENT
  case_03
     R7/R8 MISSING VERI analytics_platform analytics_9406 VERIFY_RECORD_ANONYMIZED
  case_04
     R5/R17 MISSING VERI account_service account_004 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_901 VERIFY_RECORD_ANONYMIZED
  case_07
     STATUS gold INCOMPLETE got COMPLETE
     R7/R8 MISSING FIND support_platform support_001 REPORT_REMAINING_RECORD
     R7/R8 MISSING REME support_platform support_001 DELETE_RECORD
     R5/R17 MISSING VERI account_service account_007 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI support_platform support_001 VERIFY_RECORD_ABSENT
  case_08
     R5/R17 MISSING VERI account_service account_008 VERIFY_RECORD_ABSENT
  case_09
     R5/R17 MISSING VERI account_service account_3960 VERIFY_RECORD_ABSENT
  case_10
     R5/R17 MISSING VERI account_service account_010 VERIFY_RECORD_ABSENT
  case_18
     R5/R17 MISSING VERI account_service account_5521 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_6645 VERIFY_RECORD_PRESENT
  case_20
     R5/R17 MISSING VERI account_service account_5037 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_5569 VERIFY_RECORD_PRESENT
  case_21
     R5/R17 MISSING VERI account_service account_6440 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_5335 VERIFY_RECORD_ANONYMIZED
  case_22
     R5/R17 MISSING VERI account_service account_4990 VERIFY_RECORD_ABSENT
  case_23
     R5/R17 MISSING VERI account_service account_410 VERIFY_RECORD_ABSENT
  case_25
     R5/R17 MISSING VERI account_service account_3136 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_1895 VERIFY_RECORD_ANONYMIZED
  case_26
     R5/R17 MISSING VERI account_service account_5684 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_4566 VERIFY_RECORD_ANONYMIZED
  case_27
     R5/R17 MISSING VERI account_service account_3866 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_4574 VERIFY_RECORD_ANONYMIZED
  case_28
     R5/R17 MISSING VERI account_service account_5482 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_6077 VERIFY_RECORD_ANONYMIZED
  case_29
     R5/R17 MISSING VERI account_service account_7012 VERIFY_RECORD_ABSENT
  case_30
     R5/R17 MISSING VERI account_service account_4163 VERIFY_RECORD_ABSENT
  case_31
     R5/R17 MISSING VERI account_service account_4857 VERIFY_RECORD_ABSENT
  case_32
     R5/R17 MISSING VERI account_service account_8858 VERIFY_RECORD_ABSENT
```

## Sample run 2026-10-24T14:44Z

```text
SAMPLE SCORE
  status_accuracy: 31/32
  exact_steps_json: 11/32
  step_P(7-field): 0.7267
  step_R(7-field): 0.6062
  step_F1(7-field): 0.661
  step_P(6-field, no step_no): 1.0
  step_R(6-field): 0.8342
  step_F1(6-field): 0.9096
  core_step_recall(6-field, ignoring evidence/step_no): 161/193
  evidence_id_acc_on_matched: 161/161
  sequence_exact(core order): 11/32
  intent_paths: {'fallback': 32}
  status confusion (gold -> pred): COMPLETE->COMPLETE: 10, INCOMPLETE->COMPLETE: 1, INCOMPLETE->INCOMPLETE: 21
  headline before: 31/32  after: 31/32  (no drop)
  flipped vs last run: none
MISSES (21 cases)
  case_01
     R5/R17 MISSING VERI account_service account_001 VERIFY_RECORD_ABSENT
  case_02
     R5/R17 MISSING VERI account_service account_002 VERIFY_RECORD_ABSENT
  case_03
     R7/R8 MISSING VERI analytics_platform analytics_9406 VERIFY_RECORD_ANONYMIZED
  case_04
     R5/R17 MISSING VERI account_service account_004 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_901 VERIFY_RECORD_ANONYMIZED
  case_07
     STATUS gold INCOMPLETE got COMPLETE
     R7/R8 MISSING FIND support_platform support_001 REPORT_REMAINING_RECORD
     R7/R8 MISSING REME support_platform support_001 DELETE_RECORD
     R5/R17 MISSING VERI account_service account_007 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI support_platform support_001 VERIFY_RECORD_ABSENT
  case_08
     R5/R17 MISSING VERI account_service account_008 VERIFY_RECORD_ABSENT
  case_09
     R5/R17 MISSING VERI account_service account_3960 VERIFY_RECORD_ABSENT
  case_10
     R5/R17 MISSING VERI account_service account_010 VERIFY_RECORD_ABSENT
  case_18
     R5/R17 MISSING VERI account_service account_5521 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_6645 VERIFY_RECORD_PRESENT
  case_20
     R5/R17 MISSING VERI account_service account_5037 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_5569 VERIFY_RECORD_PRESENT
  case_21
     R5/R17 MISSING VERI account_service account_6440 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_5335 VERIFY_RECORD_ANONYMIZED
  case_22
     R5/R17 MISSING VERI account_service account_4990 VERIFY_RECORD_ABSENT
  case_23
     R5/R17 MISSING VERI account_service account_410 VERIFY_RECORD_ABSENT
  case_25
     R5/R17 MISSING VERI account_service account_3136 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_1895 VERIFY_RECORD_ANONYMIZED
  case_26
     R5/R17 MISSING VERI account_service account_5684 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_4566 VERIFY_RECORD_ANONYMIZED
  case_27
     R5/R17 MISSING VERI account_service account_3866 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_4574 VERIFY_RECORD_ANONYMIZED
  case_28
     R5/R17 MISSING VERI account_service account_5482 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_6077 VERIFY_RECORD_ANONYMIZED
  case_29
     R5/R17 MISSING VERI account_service account_7012 VERIFY_RECORD_ABSENT
  case_30
     R5/R17 MISSING VERI account_service account_4163 VERIFY_RECORD_ABSENT
  case_31
     R5/R17 MISSING VERI account_service account_4857 VERIFY_RECORD_ABSENT
  case_32
     R5/R17 MISSING VERI account_service account_8858 VERIFY_RECORD_ABSENT
```

## Sample run 2026-10-24T14:44Z

```text
SAMPLE SCORE
  status_accuracy: 31/32
  exact_steps_json: 15/32
  step_P(7-field): 0.7425
  step_R(7-field): 0.6425
  step_F1(7-field): 0.6889
  step_P(6-field, no step_no): 0.988
  step_R(6-field): 0.8549
  step_F1(6-field): 0.9167
  core_step_recall(6-field, ignoring evidence/step_no): 166/193
  evidence_id_acc_on_matched: 165/166
  sequence_exact(core order): 15/32
  intent_paths: {'fallback': 32}
  status confusion (gold -> pred): COMPLETE->COMPLETE: 10, INCOMPLETE->COMPLETE: 1, INCOMPLETE->INCOMPLETE: 21
  headline before: 31/32  after: 31/32  (no drop)
  flipped vs last run: ['case_01: gold=COMPLETE before=COMPLETE after=COMPLETE(exact)', 'case_02: gold=COMPLETE before=COMPLETE after=COMPLETE(exact)', 'case_08: gold=INCOMPLETE before=INCOMPLETE after=INCOMPLETE(exact)', 'case_10: gold=INCOMPLETE before=INCOMPLETE after=INCOMPLETE(exact)']
MISSES (17 cases)
  case_03
     R7/R8 MISSING VERI analytics_platform analytics_9406 VERIFY_RECORD_ANONYMIZED
  case_04
     R5/R17 MISSING VERI account_service account_004 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_901 VERIFY_RECORD_ANONYMIZED
  case_07
     STATUS gold INCOMPLETE got COMPLETE
     R7/R8 MISSING FIND support_platform support_001 REPORT_REMAINING_RECORD
     R7/R8 MISSING REME support_platform support_001 DELETE_RECORD
     R13 evidence account_007 VERIFY_RECORD_ABSENT: gold '' got 'evidence_54'
     R7/R8 MISSING VERI support_platform support_001 VERIFY_RECORD_ABSENT
  case_09
     R5/R17 MISSING VERI account_service account_3960 VERIFY_RECORD_ABSENT
  case_18
     R5/R17 MISSING VERI account_service account_5521 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_6645 VERIFY_RECORD_PRESENT
     R5/R17 EXTRA VERI account_service account_050 VERIFY_RECORD_ABSENT
  case_20
     R5/R17 MISSING VERI account_service account_5037 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_5569 VERIFY_RECORD_PRESENT
  case_21
     R5/R17 MISSING VERI account_service account_6440 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_5335 VERIFY_RECORD_ANONYMIZED
  case_22
     R5/R17 MISSING VERI account_service account_4990 VERIFY_RECORD_ABSENT
  case_23
     R5/R17 MISSING VERI account_service account_410 VERIFY_RECORD_ABSENT
  case_25
     R5/R17 MISSING VERI account_service account_3136 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_1895 VERIFY_RECORD_ANONYMIZED
  case_26
     R5/R17 MISSING VERI account_service account_5684 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_4566 VERIFY_RECORD_ANONYMIZED
  case_27
     R5/R17 MISSING VERI account_service account_3866 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_4574 VERIFY_RECORD_ANONYMIZED
  case_28
     R5/R17 MISSING VERI account_service account_5482 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_6077 VERIFY_RECORD_ANONYMIZED
  case_29
     R5/R17 MISSING VERI account_service account_7012 VERIFY_RECORD_ABSENT
  case_30
     R5/R17 MISSING VERI account_service account_4163 VERIFY_RECORD_ABSENT
  case_31
     R5/R17 MISSING VERI account_service account_4857 VERIFY_RECORD_ABSENT
  case_32
     R5/R17 MISSING VERI account_service account_8858 VERIFY_RECORD_ABSENT
```

## Sample run 2026-10-24T14:44Z

```text
SAMPLE SCORE
  status_accuracy: 31/32
  exact_steps_json: 15/32
  step_P(7-field): 0.741
  step_R(7-field): 0.6373
  step_F1(7-field): 0.6852
  step_P(6-field, no step_no): 0.994
  step_R(6-field): 0.8549
  step_F1(6-field): 0.9192
  core_step_recall(6-field, ignoring evidence/step_no): 166/193
  evidence_id_acc_on_matched: 165/166
  sequence_exact(core order): 15/32
  intent_paths: {'fallback': 32}
  status confusion (gold -> pred): COMPLETE->COMPLETE: 10, INCOMPLETE->COMPLETE: 1, INCOMPLETE->INCOMPLETE: 21
  headline before: 31/32  after: 31/32  (no drop)
  flipped vs last run: none
MISSES (17 cases)
  case_03
     R7/R8 MISSING VERI analytics_platform analytics_9406 VERIFY_RECORD_ANONYMIZED
  case_04
     R5/R17 MISSING VERI account_service account_004 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_901 VERIFY_RECORD_ANONYMIZED
  case_07
     STATUS gold INCOMPLETE got COMPLETE
     R7/R8 MISSING FIND support_platform support_001 REPORT_REMAINING_RECORD
     R7/R8 MISSING REME support_platform support_001 DELETE_RECORD
     R13 evidence account_007 VERIFY_RECORD_ABSENT: gold '' got 'evidence_54'
     R7/R8 MISSING VERI support_platform support_001 VERIFY_RECORD_ABSENT
  case_09
     R5/R17 MISSING VERI account_service account_3960 VERIFY_RECORD_ABSENT
  case_18
     R5/R17 MISSING VERI account_service account_5521 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_6645 VERIFY_RECORD_PRESENT
  case_20
     R5/R17 MISSING VERI account_service account_5037 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_5569 VERIFY_RECORD_PRESENT
  case_21
     R5/R17 MISSING VERI account_service account_6440 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_5335 VERIFY_RECORD_ANONYMIZED
  case_22
     R5/R17 MISSING VERI account_service account_4990 VERIFY_RECORD_ABSENT
  case_23
     R5/R17 MISSING VERI account_service account_410 VERIFY_RECORD_ABSENT
  case_25
     R5/R17 MISSING VERI account_service account_3136 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_1895 VERIFY_RECORD_ANONYMIZED
  case_26
     R5/R17 MISSING VERI account_service account_5684 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_4566 VERIFY_RECORD_ANONYMIZED
  case_27
     R5/R17 MISSING VERI account_service account_3866 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_4574 VERIFY_RECORD_ANONYMIZED
  case_28
     R5/R17 MISSING VERI account_service account_5482 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_6077 VERIFY_RECORD_ANONYMIZED
  case_29
     R5/R17 MISSING VERI account_service account_7012 VERIFY_RECORD_ABSENT
  case_30
     R5/R17 MISSING VERI account_service account_4163 VERIFY_RECORD_ABSENT
  case_31
     R5/R17 MISSING VERI account_service account_4857 VERIFY_RECORD_ABSENT
  case_32
     R5/R17 MISSING VERI account_service account_8858 VERIFY_RECORD_ABSENT
```

## Sample run 2026-10-24T14:56Z

```text
SAMPLE SCORE
  status_accuracy: 31/32
  exact_steps_json: 15/32
  step_P(7-field): 0.741
  step_R(7-field): 0.6373
  step_F1(7-field): 0.6852
  step_P(6-field, no step_no): 0.994
  step_R(6-field): 0.8549
  step_F1(6-field): 0.9192
  core_step_recall(6-field, ignoring evidence/step_no): 166/193
  evidence_id_acc_on_matched: 165/166
  sequence_exact(core order): 15/32
  intent_paths: {'agent(cache)': 32}
  status confusion (gold -> pred): COMPLETE->COMPLETE: 10, INCOMPLETE->COMPLETE: 1, INCOMPLETE->INCOMPLETE: 21
  headline before: 31/32  after: 31/32  (no drop)
  flipped vs last run: none
MISSES (17 cases)
  case_03
     R7/R8 MISSING VERI analytics_platform analytics_9406 VERIFY_RECORD_ANONYMIZED
  case_04
     R5/R17 MISSING VERI account_service account_004 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_901 VERIFY_RECORD_ANONYMIZED
  case_07
     STATUS gold INCOMPLETE got COMPLETE
     R7/R8 MISSING FIND support_platform support_001 REPORT_REMAINING_RECORD
     R7/R8 MISSING REME support_platform support_001 DELETE_RECORD
     R13 evidence account_007 VERIFY_RECORD_ABSENT: gold '' got 'evidence_54'
     R7/R8 MISSING VERI support_platform support_001 VERIFY_RECORD_ABSENT
  case_09
     R5/R17 MISSING VERI account_service account_3960 VERIFY_RECORD_ABSENT
  case_18
     R5/R17 MISSING VERI account_service account_5521 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_6645 VERIFY_RECORD_PRESENT
  case_20
     R5/R17 MISSING VERI account_service account_5037 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_5569 VERIFY_RECORD_PRESENT
  case_21
     R5/R17 MISSING VERI account_service account_6440 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_5335 VERIFY_RECORD_ANONYMIZED
  case_22
     R5/R17 MISSING VERI account_service account_4990 VERIFY_RECORD_ABSENT
  case_23
     R5/R17 MISSING VERI account_service account_410 VERIFY_RECORD_ABSENT
  case_25
     R5/R17 MISSING VERI account_service account_3136 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_1895 VERIFY_RECORD_ANONYMIZED
  case_26
     R5/R17 MISSING VERI account_service account_5684 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_4566 VERIFY_RECORD_ANONYMIZED
  case_27
     R5/R17 MISSING VERI account_service account_3866 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_4574 VERIFY_RECORD_ANONYMIZED
  case_28
     R5/R17 MISSING VERI account_service account_5482 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_6077 VERIFY_RECORD_ANONYMIZED
  case_29
     R5/R17 MISSING VERI account_service account_7012 VERIFY_RECORD_ABSENT
  case_30
     R5/R17 MISSING VERI account_service account_4163 VERIFY_RECORD_ABSENT
  case_31
     R5/R17 MISSING VERI account_service account_4857 VERIFY_RECORD_ABSENT
  case_32
     R5/R17 MISSING VERI account_service account_8858 VERIFY_RECORD_ABSENT
```

## Sample run 2026-10-24T15:59Z

```text
SAMPLE SCORE
  status_accuracy: 32/32
  exact_steps_json: 16/32
  step_P(7-field): 0.7515
  step_R(7-field): 0.658
  step_F1(7-field): 0.7017
  step_P(6-field, no step_no): 1.0
  step_R(6-field): 0.8756
  step_F1(6-field): 0.9337
  core_step_recall(6-field, ignoring evidence/step_no): 169/193
  evidence_id_acc_on_matched: 169/169
  sequence_exact(core order): 16/32
  intent_paths: {'agent(cache)': 32}
  status confusion (gold -> pred): COMPLETE->COMPLETE: 10, INCOMPLETE->INCOMPLETE: 22
  headline before: 31/32  after: 32/32  (no drop)
  flipped vs last run: ['case_07: gold=INCOMPLETE before=COMPLETE after=INCOMPLETE(exact)']
MISSES (16 cases)
  case_03
     R7/R8 MISSING VERI analytics_platform analytics_9406 VERIFY_RECORD_ANONYMIZED
  case_04
     R5/R17 MISSING VERI account_service account_004 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_901 VERIFY_RECORD_ANONYMIZED
  case_09
     R5/R17 MISSING VERI account_service account_3960 VERIFY_RECORD_ABSENT
  case_18
     R5/R17 MISSING VERI account_service account_5521 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_6645 VERIFY_RECORD_PRESENT
  case_20
     R5/R17 MISSING VERI account_service account_5037 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_5569 VERIFY_RECORD_PRESENT
  case_21
     R5/R17 MISSING VERI account_service account_6440 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_5335 VERIFY_RECORD_ANONYMIZED
  case_22
     R5/R17 MISSING VERI account_service account_4990 VERIFY_RECORD_ABSENT
  case_23
     R5/R17 MISSING VERI account_service account_410 VERIFY_RECORD_ABSENT
  case_25
     R5/R17 MISSING VERI account_service account_3136 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_1895 VERIFY_RECORD_ANONYMIZED
  case_26
     R5/R17 MISSING VERI account_service account_5684 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_4566 VERIFY_RECORD_ANONYMIZED
  case_27
     R5/R17 MISSING VERI account_service account_3866 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_4574 VERIFY_RECORD_ANONYMIZED
  case_28
     R5/R17 MISSING VERI account_service account_5482 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_6077 VERIFY_RECORD_ANONYMIZED
  case_29
     R5/R17 MISSING VERI account_service account_7012 VERIFY_RECORD_ABSENT
  case_30
     R5/R17 MISSING VERI account_service account_4163 VERIFY_RECORD_ABSENT
  case_31
     R5/R17 MISSING VERI account_service account_4857 VERIFY_RECORD_ABSENT
  case_32
     R5/R17 MISSING VERI account_service account_8858 VERIFY_RECORD_ABSENT
```

## Sample run 2026-10-24T15:59Z

```text
SAMPLE SCORE
  status_accuracy: 32/32
  exact_steps_json: 16/32
  step_P(7-field): 0.7515
  step_R(7-field): 0.658
  step_F1(7-field): 0.7017
  step_P(6-field, no step_no): 1.0
  step_R(6-field): 0.8756
  step_F1(6-field): 0.9337
  core_step_recall(6-field, ignoring evidence/step_no): 169/193
  evidence_id_acc_on_matched: 169/169
  sequence_exact(core order): 16/32
  intent_paths: {'agent(cache)': 32}
  status confusion (gold -> pred): COMPLETE->COMPLETE: 10, INCOMPLETE->INCOMPLETE: 22
  headline before: 32/32  after: 32/32  (no drop)
  flipped vs last run: none
MISSES (16 cases)
  case_03
     R7/R8 MISSING VERI analytics_platform analytics_9406 VERIFY_RECORD_ANONYMIZED
  case_04
     R5/R17 MISSING VERI account_service account_004 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_901 VERIFY_RECORD_ANONYMIZED
  case_09
     R5/R17 MISSING VERI account_service account_3960 VERIFY_RECORD_ABSENT
  case_18
     R5/R17 MISSING VERI account_service account_5521 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_6645 VERIFY_RECORD_PRESENT
  case_20
     R5/R17 MISSING VERI account_service account_5037 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_5569 VERIFY_RECORD_PRESENT
  case_21
     R5/R17 MISSING VERI account_service account_6440 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_5335 VERIFY_RECORD_ANONYMIZED
  case_22
     R5/R17 MISSING VERI account_service account_4990 VERIFY_RECORD_ABSENT
  case_23
     R5/R17 MISSING VERI account_service account_410 VERIFY_RECORD_ABSENT
  case_25
     R5/R17 MISSING VERI account_service account_3136 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_1895 VERIFY_RECORD_ANONYMIZED
  case_26
     R5/R17 MISSING VERI account_service account_5684 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_4566 VERIFY_RECORD_ANONYMIZED
  case_27
     R5/R17 MISSING VERI account_service account_3866 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_4574 VERIFY_RECORD_ANONYMIZED
  case_28
     R5/R17 MISSING VERI account_service account_5482 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_6077 VERIFY_RECORD_ANONYMIZED
  case_29
     R5/R17 MISSING VERI account_service account_7012 VERIFY_RECORD_ABSENT
  case_30
     R5/R17 MISSING VERI account_service account_4163 VERIFY_RECORD_ABSENT
  case_31
     R5/R17 MISSING VERI account_service account_4857 VERIFY_RECORD_ABSENT
  case_32
     R5/R17 MISSING VERI account_service account_8858 VERIFY_RECORD_ABSENT
```

## Sample run 2026-10-24T16:00Z

```text
SAMPLE SCORE
  status_accuracy: 32/32
  exact_steps_json: 16/32
  step_P(7-field): 0.7515
  step_R(7-field): 0.658
  step_F1(7-field): 0.7017
  step_P(6-field, no step_no): 1.0
  step_R(6-field): 0.8756
  step_F1(6-field): 0.9337
  core_step_recall(6-field, ignoring evidence/step_no): 169/193
  evidence_id_acc_on_matched: 169/169
  sequence_exact(core order): 16/32
  intent_paths: {'agent(cache)': 32}
  status confusion (gold -> pred): COMPLETE->COMPLETE: 10, INCOMPLETE->INCOMPLETE: 22
  headline before: 32/32  after: 32/32  (no drop)
  flipped vs last run: none
MISSES (16 cases)
  case_03
     R7/R8 MISSING VERI analytics_platform analytics_9406 VERIFY_RECORD_ANONYMIZED
  case_04
     R5/R17 MISSING VERI account_service account_004 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_901 VERIFY_RECORD_ANONYMIZED
  case_09
     R5/R17 MISSING VERI account_service account_3960 VERIFY_RECORD_ABSENT
  case_18
     R5/R17 MISSING VERI account_service account_5521 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_6645 VERIFY_RECORD_PRESENT
  case_20
     R5/R17 MISSING VERI account_service account_5037 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_5569 VERIFY_RECORD_PRESENT
  case_21
     R5/R17 MISSING VERI account_service account_6440 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_5335 VERIFY_RECORD_ANONYMIZED
  case_22
     R5/R17 MISSING VERI account_service account_4990 VERIFY_RECORD_ABSENT
  case_23
     R5/R17 MISSING VERI account_service account_410 VERIFY_RECORD_ABSENT
  case_25
     R5/R17 MISSING VERI account_service account_3136 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_1895 VERIFY_RECORD_ANONYMIZED
  case_26
     R5/R17 MISSING VERI account_service account_5684 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_4566 VERIFY_RECORD_ANONYMIZED
  case_27
     R5/R17 MISSING VERI account_service account_3866 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_4574 VERIFY_RECORD_ANONYMIZED
  case_28
     R5/R17 MISSING VERI account_service account_5482 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_6077 VERIFY_RECORD_ANONYMIZED
  case_29
     R5/R17 MISSING VERI account_service account_7012 VERIFY_RECORD_ABSENT
  case_30
     R5/R17 MISSING VERI account_service account_4163 VERIFY_RECORD_ABSENT
  case_31
     R5/R17 MISSING VERI account_service account_4857 VERIFY_RECORD_ABSENT
  case_32
     R5/R17 MISSING VERI account_service account_8858 VERIFY_RECORD_ABSENT
```

## Sample run 2026-10-24T18:10Z

```text
SAMPLE SCORE
  status_accuracy: 32/32
  exact_steps_json: 17/32
  step_P(7-field): 0.7907
  step_R(7-field): 0.7047
  step_F1(7-field): 0.7452
  step_P(6-field, no step_no): 1.0
  step_R(6-field): 0.8912
  step_F1(6-field): 0.9425
  core_step_recall(6-field, ignoring evidence/step_no): 172/193
  evidence_id_acc_on_matched: 172/172
  sequence_exact(core order): 17/32
  intent_paths: {'agent(cache)': 32}
  status confusion (gold -> pred): COMPLETE->COMPLETE: 10, INCOMPLETE->INCOMPLETE: 22
  headline before: 32/32  after: 32/32  (no drop)
  flipped vs last run: ['case_09: gold=INCOMPLETE before=INCOMPLETE after=INCOMPLETE(exact)']
MISSES (15 cases)
  case_03
     R7/R8 MISSING VERI analytics_platform analytics_9406 VERIFY_RECORD_ANONYMIZED
  case_04
     R5/R17 MISSING VERI account_service account_004 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_901 VERIFY_RECORD_ANONYMIZED
  case_18
     R5/R17 MISSING VERI account_service account_5521 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_6645 VERIFY_RECORD_PRESENT
  case_20
     R5/R17 MISSING VERI account_service account_5037 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_5569 VERIFY_RECORD_PRESENT
  case_21
     R5/R17 MISSING VERI account_service account_6440 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_5335 VERIFY_RECORD_ANONYMIZED
  case_22
     R5/R17 MISSING VERI account_service account_4990 VERIFY_RECORD_ABSENT
  case_23
     R5/R17 MISSING VERI account_service account_410 VERIFY_RECORD_ABSENT
  case_25
     R5/R17 MISSING VERI account_service account_3136 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_1895 VERIFY_RECORD_ANONYMIZED
  case_26
     R7/R8 MISSING VERI analytics_platform analytics_4566 VERIFY_RECORD_ANONYMIZED
  case_27
     R7/R8 MISSING VERI analytics_platform analytics_4574 VERIFY_RECORD_ANONYMIZED
  case_28
     R5/R17 MISSING VERI account_service account_5482 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_6077 VERIFY_RECORD_ANONYMIZED
  case_29
     R5/R17 MISSING VERI account_service account_7012 VERIFY_RECORD_ABSENT
  case_30
     R5/R17 MISSING VERI account_service account_4163 VERIFY_RECORD_ABSENT
  case_31
     R5/R17 MISSING VERI account_service account_4857 VERIFY_RECORD_ABSENT
  case_32
     R5/R17 MISSING VERI account_service account_8858 VERIFY_RECORD_ABSENT
```

## Evaluation run 2026-10-24T18:19Z (code/evaluation/main.py)

```text
SAMPLE SCORE
  status_accuracy: 32/32
  exact_steps_json: 17/32
  step_P(7-field): 0.7907
  step_R(7-field): 0.7047
  step_F1(7-field): 0.7452
  step_P(6-field, no step_no): 1.0
  step_R(6-field): 0.8912
  step_F1(6-field): 0.9425
  core_step_recall(6-field, ignoring evidence/step_no): 172/193
  evidence_id_acc_on_matched: 172/172
  sequence_exact(core order): 17/32
  intent_paths: {'agent(cache)': 32}
  status confusion (gold -> pred): COMPLETE->COMPLETE: 10, INCOMPLETE->INCOMPLETE: 22
  headline before: 32/32  after: 32/32  (no drop)
  flipped vs last run: none
MISSES (15 cases)
  case_03
     R7/R8 MISSING VERI analytics_platform analytics_9406 VERIFY_RECORD_ANONYMIZED
  case_04
     R5/R17 MISSING VERI account_service account_004 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_901 VERIFY_RECORD_ANONYMIZED
  case_18
     R5/R17 MISSING VERI account_service account_5521 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_6645 VERIFY_RECORD_PRESENT
  case_20
     R5/R17 MISSING VERI account_service account_5037 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_5569 VERIFY_RECORD_PRESENT
  case_21
     R5/R17 MISSING VERI account_service account_6440 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_5335 VERIFY_RECORD_ANONYMIZED
  case_22
     R5/R17 MISSING VERI account_service account_4990 VERIFY_RECORD_ABSENT
  case_23
     R5/R17 MISSING VERI account_service account_410 VERIFY_RECORD_ABSENT
  case_25
     R5/R17 MISSING VERI account_service account_3136 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_1895 VERIFY_RECORD_ANONYMIZED
  case_26
     R7/R8 MISSING VERI analytics_platform analytics_4566 VERIFY_RECORD_ANONYMIZED
  case_27
     R7/R8 MISSING VERI analytics_platform analytics_4574 VERIFY_RECORD_ANONYMIZED
  case_28
     R5/R17 MISSING VERI account_service account_5482 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_6077 VERIFY_RECORD_ANONYMIZED
  case_29
     R5/R17 MISSING VERI account_service account_7012 VERIFY_RECORD_ABSENT
  case_30
     R5/R17 MISSING VERI account_service account_4163 VERIFY_RECORD_ABSENT
  case_31
     R5/R17 MISSING VERI account_service account_4857 VERIFY_RECORD_ABSENT
  case_32
     R5/R17 MISSING VERI account_service account_8858 VERIFY_RECORD_ABSENT

VALIDATOR output.csv: 0 errors, 264 warnings

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
    VERIFY_RECORD_PRESENT         15.2% /  12.4%
    VERIFY_RECORD_REDACTED         6.3% /   5.2%
    VERIFY_RESTORE_BLOCKED         2.1% /   3.1%

MEDIA CHECK (vs dev ground truth)
  evidence_09: records=2 resource_ids=EXACT identifiers=DIFF status_values_verbatim=2/2
     user_ids: missing=['user_9842'] extra=[]
  TOTAL (matched / union):
   resource_ids: 26/26 = 100.0%
   identifiers: 34/35 = 97.1%
   status: 201/234 = 85.9%

```

## Evaluation run 2026-10-24T18:25Z (code/evaluation/main.py)

```text
SAMPLE SCORE
  status_accuracy: 32/32
  exact_steps_json: 17/32
  step_P(7-field): 0.7907
  step_R(7-field): 0.7047
  step_F1(7-field): 0.7452
  step_P(6-field, no step_no): 1.0
  step_R(6-field): 0.8912
  step_F1(6-field): 0.9425
  core_step_recall(6-field, ignoring evidence/step_no): 172/193
  evidence_id_acc_on_matched: 172/172
  sequence_exact(core order): 17/32
  intent_paths: {'agent(cache)': 32}
  status confusion (gold -> pred): COMPLETE->COMPLETE: 10, INCOMPLETE->INCOMPLETE: 22
  headline before: 32/32  after: 32/32  (no drop)
  flipped vs last run: none
MISSES (15 cases)
  case_03
     R7/R8 MISSING VERI analytics_platform analytics_9406 VERIFY_RECORD_ANONYMIZED
  case_04
     R5/R17 MISSING VERI account_service account_004 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_901 VERIFY_RECORD_ANONYMIZED
  case_18
     R5/R17 MISSING VERI account_service account_5521 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_6645 VERIFY_RECORD_PRESENT
  case_20
     R5/R17 MISSING VERI account_service account_5037 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_5569 VERIFY_RECORD_PRESENT
  case_21
     R5/R17 MISSING VERI account_service account_6440 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_5335 VERIFY_RECORD_ANONYMIZED
  case_22
     R5/R17 MISSING VERI account_service account_4990 VERIFY_RECORD_ABSENT
  case_23
     R5/R17 MISSING VERI account_service account_410 VERIFY_RECORD_ABSENT
  case_25
     R5/R17 MISSING VERI account_service account_3136 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_1895 VERIFY_RECORD_ANONYMIZED
  case_26
     R7/R8 MISSING VERI analytics_platform analytics_4566 VERIFY_RECORD_ANONYMIZED
  case_27
     R7/R8 MISSING VERI analytics_platform analytics_4574 VERIFY_RECORD_ANONYMIZED
  case_28
     R5/R17 MISSING VERI account_service account_5482 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_6077 VERIFY_RECORD_ANONYMIZED
  case_29
     R5/R17 MISSING VERI account_service account_7012 VERIFY_RECORD_ABSENT
  case_30
     R5/R17 MISSING VERI account_service account_4163 VERIFY_RECORD_ABSENT
  case_31
     R5/R17 MISSING VERI account_service account_4857 VERIFY_RECORD_ABSENT
  case_32
     R5/R17 MISSING VERI account_service account_8858 VERIFY_RECORD_ABSENT

VALIDATOR output.csv: 0 errors, 264 warnings

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
    VERIFY_RECORD_PRESENT         15.2% /  12.4%
    VERIFY_RECORD_REDACTED         6.3% /   5.2%
    VERIFY_RESTORE_BLOCKED         2.1% /   3.1%

MEDIA CHECK (vs dev ground truth)
  evidence_09: records=2 resource_ids=EXACT identifiers=DIFF status_values_verbatim=2/2
     user_ids: missing=['user_9842'] extra=[]
  TOTAL (matched / union):
   resource_ids: 26/26 = 100.0%
   identifiers: 34/35 = 97.1%
   status: 201/234 = 85.9%

```

## Evaluation run 2026-10-24T18:25Z (code/evaluation/main.py)

```text
SAMPLE SCORE
  status_accuracy: 32/32
  exact_steps_json: 17/32
  step_P(7-field): 0.7907
  step_R(7-field): 0.7047
  step_F1(7-field): 0.7452
  step_P(6-field, no step_no): 1.0
  step_R(6-field): 0.8912
  step_F1(6-field): 0.9425
  core_step_recall(6-field, ignoring evidence/step_no): 172/193
  evidence_id_acc_on_matched: 172/172
  sequence_exact(core order): 17/32
  intent_paths: {'agent(cache)': 32}
  status confusion (gold -> pred): COMPLETE->COMPLETE: 10, INCOMPLETE->INCOMPLETE: 22
  headline before: 32/32  after: 32/32  (no drop)
  flipped vs last run: none
MISSES (15 cases)
  case_03
     R7/R8 MISSING VERI analytics_platform analytics_9406 VERIFY_RECORD_ANONYMIZED
  case_04
     R5/R17 MISSING VERI account_service account_004 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_901 VERIFY_RECORD_ANONYMIZED
  case_18
     R5/R17 MISSING VERI account_service account_5521 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_6645 VERIFY_RECORD_PRESENT
  case_20
     R5/R17 MISSING VERI account_service account_5037 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_5569 VERIFY_RECORD_PRESENT
  case_21
     R5/R17 MISSING VERI account_service account_6440 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_5335 VERIFY_RECORD_ANONYMIZED
  case_22
     R5/R17 MISSING VERI account_service account_4990 VERIFY_RECORD_ABSENT
  case_23
     R5/R17 MISSING VERI account_service account_410 VERIFY_RECORD_ABSENT
  case_25
     R5/R17 MISSING VERI account_service account_3136 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_1895 VERIFY_RECORD_ANONYMIZED
  case_26
     R7/R8 MISSING VERI analytics_platform analytics_4566 VERIFY_RECORD_ANONYMIZED
  case_27
     R7/R8 MISSING VERI analytics_platform analytics_4574 VERIFY_RECORD_ANONYMIZED
  case_28
     R5/R17 MISSING VERI account_service account_5482 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_6077 VERIFY_RECORD_ANONYMIZED
  case_29
     R5/R17 MISSING VERI account_service account_7012 VERIFY_RECORD_ABSENT
  case_30
     R5/R17 MISSING VERI account_service account_4163 VERIFY_RECORD_ABSENT
  case_31
     R5/R17 MISSING VERI account_service account_4857 VERIFY_RECORD_ABSENT
  case_32
     R5/R17 MISSING VERI account_service account_8858 VERIFY_RECORD_ABSENT

VALIDATOR output.csv: 0 errors, 264 warnings

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

MEDIA CHECK (vs dev ground truth)
  evidence_09: records=2 resource_ids=EXACT identifiers=DIFF status_values_verbatim=2/2
     user_ids: missing=['user_9842'] extra=[]
  TOTAL (matched / union):
   resource_ids: 26/26 = 100.0%
   identifiers: 34/35 = 97.1%
   status: 201/234 = 85.9%

```

## Evaluation run 2026-10-24T18:26Z (code/evaluation/main.py)

```text
SAMPLE SCORE
  status_accuracy: 32/32
  exact_steps_json: 17/32
  step_P(7-field): 0.7907
  step_R(7-field): 0.7047
  step_F1(7-field): 0.7452
  step_P(6-field, no step_no): 1.0
  step_R(6-field): 0.8912
  step_F1(6-field): 0.9425
  core_step_recall(6-field, ignoring evidence/step_no): 172/193
  evidence_id_acc_on_matched: 172/172
  sequence_exact(core order): 17/32
  intent_paths: {'agent(cache)': 32}
  status confusion (gold -> pred): COMPLETE->COMPLETE: 10, INCOMPLETE->INCOMPLETE: 22
  headline before: 32/32  after: 32/32  (no drop)
  flipped vs last run: none
MISSES (15 cases)
  case_03
     R7/R8 MISSING VERI analytics_platform analytics_9406 VERIFY_RECORD_ANONYMIZED
  case_04
     R5/R17 MISSING VERI account_service account_004 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_901 VERIFY_RECORD_ANONYMIZED
  case_18
     R5/R17 MISSING VERI account_service account_5521 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_6645 VERIFY_RECORD_PRESENT
  case_20
     R5/R17 MISSING VERI account_service account_5037 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_5569 VERIFY_RECORD_PRESENT
  case_21
     R5/R17 MISSING VERI account_service account_6440 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_5335 VERIFY_RECORD_ANONYMIZED
  case_22
     R5/R17 MISSING VERI account_service account_4990 VERIFY_RECORD_ABSENT
  case_23
     R5/R17 MISSING VERI account_service account_410 VERIFY_RECORD_ABSENT
  case_25
     R5/R17 MISSING VERI account_service account_3136 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_1895 VERIFY_RECORD_ANONYMIZED
  case_26
     R7/R8 MISSING VERI analytics_platform analytics_4566 VERIFY_RECORD_ANONYMIZED
  case_27
     R7/R8 MISSING VERI analytics_platform analytics_4574 VERIFY_RECORD_ANONYMIZED
  case_28
     R5/R17 MISSING VERI account_service account_5482 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_6077 VERIFY_RECORD_ANONYMIZED
  case_29
     R5/R17 MISSING VERI account_service account_7012 VERIFY_RECORD_ABSENT
  case_30
     R5/R17 MISSING VERI account_service account_4163 VERIFY_RECORD_ABSENT
  case_31
     R5/R17 MISSING VERI account_service account_4857 VERIFY_RECORD_ABSENT
  case_32
     R5/R17 MISSING VERI account_service account_8858 VERIFY_RECORD_ABSENT

VALIDATOR output.csv: 0 errors, 264 warnings

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

MEDIA CHECK (vs dev ground truth)
  evidence_09: records=2 resource_ids=EXACT identifiers=DIFF status_values_verbatim=2/2
     user_ids: missing=['user_9842'] extra=[]
  TOTAL (matched / union):
   resource_ids: 26/26 = 100.0%
   identifiers: 34/35 = 97.1%
   status: 201/234 = 85.9%

```

## Evaluation run 2026-10-24T18:36Z (code/evaluation/main.py)

```text
SAMPLE SCORE
  status_accuracy: 32/32
  exact_steps_json: 17/32
  step_P(7-field): 0.7907
  step_R(7-field): 0.7047
  step_F1(7-field): 0.7452
  step_P(6-field, no step_no): 1.0
  step_R(6-field): 0.8912
  step_F1(6-field): 0.9425
  core_step_recall(6-field, ignoring evidence/step_no): 172/193
  evidence_id_acc_on_matched: 172/172
  sequence_exact(core order): 17/32
  intent_paths: {'agent(cache)': 32}
  status confusion (gold -> pred): COMPLETE->COMPLETE: 10, INCOMPLETE->INCOMPLETE: 22
  headline before: 32/32  after: 32/32  (no drop)
  flipped vs last run: none
MISSES (15 cases)
  case_03
     R7/R8 MISSING VERI analytics_platform analytics_9406 VERIFY_RECORD_ANONYMIZED
  case_04
     R5/R17 MISSING VERI account_service account_004 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_901 VERIFY_RECORD_ANONYMIZED
  case_18
     R5/R17 MISSING VERI account_service account_5521 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_6645 VERIFY_RECORD_PRESENT
  case_20
     R5/R17 MISSING VERI account_service account_5037 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_5569 VERIFY_RECORD_PRESENT
  case_21
     R5/R17 MISSING VERI account_service account_6440 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_5335 VERIFY_RECORD_ANONYMIZED
  case_22
     R5/R17 MISSING VERI account_service account_4990 VERIFY_RECORD_ABSENT
  case_23
     R5/R17 MISSING VERI account_service account_410 VERIFY_RECORD_ABSENT
  case_25
     R5/R17 MISSING VERI account_service account_3136 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_1895 VERIFY_RECORD_ANONYMIZED
  case_26
     R7/R8 MISSING VERI analytics_platform analytics_4566 VERIFY_RECORD_ANONYMIZED
  case_27
     R7/R8 MISSING VERI analytics_platform analytics_4574 VERIFY_RECORD_ANONYMIZED
  case_28
     R5/R17 MISSING VERI account_service account_5482 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_6077 VERIFY_RECORD_ANONYMIZED
  case_29
     R5/R17 MISSING VERI account_service account_7012 VERIFY_RECORD_ABSENT
  case_30
     R5/R17 MISSING VERI account_service account_4163 VERIFY_RECORD_ABSENT
  case_31
     R5/R17 MISSING VERI account_service account_4857 VERIFY_RECORD_ABSENT
  case_32
     R5/R17 MISSING VERI account_service account_8858 VERIFY_RECORD_ABSENT

VALIDATOR output.csv: 0 errors, 264 warnings

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

MEDIA CHECK (vs dev ground truth)
  evidence_09: records=2 resource_ids=EXACT identifiers=DIFF status_values_verbatim=2/2
     user_ids: missing=['user_9842'] extra=[]
  TOTAL (matched / union):
   resource_ids: 26/26 = 100.0%
   identifiers: 34/35 = 97.1%
   status: 203/246 = 82.5%

```

## Evaluation run 2026-10-24T18:55Z (code/evaluation/main.py)

```text
SAMPLE SCORE
  status_accuracy: 32/32
  exact_steps_json: 17/32
  step_P(7-field): 0.7907
  step_R(7-field): 0.7047
  step_F1(7-field): 0.7452
  step_P(6-field, no step_no): 1.0
  step_R(6-field): 0.8912
  step_F1(6-field): 0.9425
  core_step_recall(6-field, ignoring evidence/step_no): 172/193
  evidence_id_acc_on_matched: 172/172
  sequence_exact(core order): 17/32
  intent_paths: {'agent(cache)': 32}
  status confusion (gold -> pred): COMPLETE->COMPLETE: 10, INCOMPLETE->INCOMPLETE: 22
  headline before: 32/32  after: 32/32  (no drop)
  flipped vs last run: none
MISSES (15 cases)
  case_03
     R7/R8 MISSING VERI analytics_platform analytics_9406 VERIFY_RECORD_ANONYMIZED
  case_04
     R5/R17 MISSING VERI account_service account_004 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_901 VERIFY_RECORD_ANONYMIZED
  case_18
     R5/R17 MISSING VERI account_service account_5521 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_6645 VERIFY_RECORD_PRESENT
  case_20
     R5/R17 MISSING VERI account_service account_5037 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_5569 VERIFY_RECORD_PRESENT
  case_21
     R5/R17 MISSING VERI account_service account_6440 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_5335 VERIFY_RECORD_ANONYMIZED
  case_22
     R5/R17 MISSING VERI account_service account_4990 VERIFY_RECORD_ABSENT
  case_23
     R5/R17 MISSING VERI account_service account_410 VERIFY_RECORD_ABSENT
  case_25
     R5/R17 MISSING VERI account_service account_3136 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_1895 VERIFY_RECORD_ANONYMIZED
  case_26
     R7/R8 MISSING VERI analytics_platform analytics_4566 VERIFY_RECORD_ANONYMIZED
  case_27
     R7/R8 MISSING VERI analytics_platform analytics_4574 VERIFY_RECORD_ANONYMIZED
  case_28
     R5/R17 MISSING VERI account_service account_5482 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_6077 VERIFY_RECORD_ANONYMIZED
  case_29
     R5/R17 MISSING VERI account_service account_7012 VERIFY_RECORD_ABSENT
  case_30
     R5/R17 MISSING VERI account_service account_4163 VERIFY_RECORD_ABSENT
  case_31
     R5/R17 MISSING VERI account_service account_4857 VERIFY_RECORD_ABSENT
  case_32
     R5/R17 MISSING VERI account_service account_8858 VERIFY_RECORD_ABSENT

VALIDATOR output.csv: 0 errors, 264 warnings

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

MEDIA CHECK (vs dev ground truth)
  evidence_09: records=2 resource_ids=EXACT identifiers=DIFF status_values_verbatim=2/2
     user_ids: missing=['user_9842'] extra=[]
  TOTAL (matched / union):
   resource_ids: 26/26 = 100.0%
   identifiers: 34/35 = 97.1%
   status: 203/246 = 82.5%

```

## Evaluation run 2026-10-24T19:02Z (code/evaluation/main.py)

```text
SAMPLE SCORE
  status_accuracy: 32/32
  exact_steps_json: 17/32
  step_P(7-field): 0.7907
  step_R(7-field): 0.7047
  step_F1(7-field): 0.7452
  step_P(6-field, no step_no): 1.0
  step_R(6-field): 0.8912
  step_F1(6-field): 0.9425
  core_step_recall(6-field, ignoring evidence/step_no): 172/193
  evidence_id_acc_on_matched: 172/172
  sequence_exact(core order): 17/32
  intent_paths: {'agent(cache)': 32}
  status confusion (gold -> pred): COMPLETE->COMPLETE: 10, INCOMPLETE->INCOMPLETE: 22
  headline before: 32/32  after: 32/32  (no drop)
  flipped vs last run: none
MISSES (15 cases)
  case_03
     R7/R8 MISSING VERI analytics_platform analytics_9406 VERIFY_RECORD_ANONYMIZED
  case_04
     R5/R17 MISSING VERI account_service account_004 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_901 VERIFY_RECORD_ANONYMIZED
  case_18
     R5/R17 MISSING VERI account_service account_5521 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_6645 VERIFY_RECORD_PRESENT
  case_20
     R5/R17 MISSING VERI account_service account_5037 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_5569 VERIFY_RECORD_PRESENT
  case_21
     R5/R17 MISSING VERI account_service account_6440 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_5335 VERIFY_RECORD_ANONYMIZED
  case_22
     R5/R17 MISSING VERI account_service account_4990 VERIFY_RECORD_ABSENT
  case_23
     R5/R17 MISSING VERI account_service account_410 VERIFY_RECORD_ABSENT
  case_25
     R5/R17 MISSING VERI account_service account_3136 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_1895 VERIFY_RECORD_ANONYMIZED
  case_26
     R7/R8 MISSING VERI analytics_platform analytics_4566 VERIFY_RECORD_ANONYMIZED
  case_27
     R7/R8 MISSING VERI analytics_platform analytics_4574 VERIFY_RECORD_ANONYMIZED
  case_28
     R5/R17 MISSING VERI account_service account_5482 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_6077 VERIFY_RECORD_ANONYMIZED
  case_29
     R5/R17 MISSING VERI account_service account_7012 VERIFY_RECORD_ABSENT
  case_30
     R5/R17 MISSING VERI account_service account_4163 VERIFY_RECORD_ABSENT
  case_31
     R5/R17 MISSING VERI account_service account_4857 VERIFY_RECORD_ABSENT
  case_32
     R5/R17 MISSING VERI account_service account_8858 VERIFY_RECORD_ABSENT

VALIDATOR output.csv: 0 errors, 264 warnings

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

MEDIA CHECK (vs dev ground truth)
  evidence_09: records=2 resource_ids=EXACT identifiers=DIFF status_values_verbatim=2/2
     user_ids: missing=['user_9842'] extra=[]
  TOTAL (matched / union):
   resource_ids: 26/26 = 100.0%
   identifiers: 34/35 = 97.1%
   status: 203/246 = 82.5%

```

## Evaluation run 2026-10-24T19:07Z (code/evaluation/main.py)

```text
SAMPLE SCORE
  status_accuracy: 32/32
  exact_steps_json: 17/32
  step_P(7-field): 0.7907
  step_R(7-field): 0.7047
  step_F1(7-field): 0.7452
  step_P(6-field, no step_no): 1.0
  step_R(6-field): 0.8912
  step_F1(6-field): 0.9425
  core_step_recall(6-field, ignoring evidence/step_no): 172/193
  evidence_id_acc_on_matched: 172/172
  sequence_exact(core order): 17/32
  field_accuracy (aligned by resource_id+operation; correct/gold steps): {'step_no': '136/193 (70.5%)', 'phase': '172/193 (89.1%)', 'system_id': '172/193 (89.1%)', 'resource_id': '172/193 (89.1%)', 'operation': '172/193 (89.1%)', 'state': '172/193 (89.1%)', 'evidence_id': '172/193 (89.1%)'}
  intent_paths: {'agent(cache)': 32}
  status_confusion: {'COMPLETE->COMPLETE': 10, 'INCOMPLETE->INCOMPLETE': 22}
  status confusion (gold -> pred): COMPLETE->COMPLETE: 10, INCOMPLETE->INCOMPLETE: 22
  headline before: 32/32  after: 32/32  (no drop)
  flipped vs last run: none
MISSES (15 cases)
  case_03
     R7/R8 MISSING VERI analytics_platform analytics_9406 VERIFY_RECORD_ANONYMIZED
  case_04
     R5/R17 MISSING VERI account_service account_004 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_901 VERIFY_RECORD_ANONYMIZED
  case_18
     R5/R17 MISSING VERI account_service account_5521 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_6645 VERIFY_RECORD_PRESENT
  case_20
     R5/R17 MISSING VERI account_service account_5037 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_5569 VERIFY_RECORD_PRESENT
  case_21
     R5/R17 MISSING VERI account_service account_6440 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_5335 VERIFY_RECORD_ANONYMIZED
  case_22
     R5/R17 MISSING VERI account_service account_4990 VERIFY_RECORD_ABSENT
  case_23
     R5/R17 MISSING VERI account_service account_410 VERIFY_RECORD_ABSENT
  case_25
     R5/R17 MISSING VERI account_service account_3136 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_1895 VERIFY_RECORD_ANONYMIZED
  case_26
     R7/R8 MISSING VERI analytics_platform analytics_4566 VERIFY_RECORD_ANONYMIZED
  case_27
     R7/R8 MISSING VERI analytics_platform analytics_4574 VERIFY_RECORD_ANONYMIZED
  case_28
     R5/R17 MISSING VERI account_service account_5482 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_6077 VERIFY_RECORD_ANONYMIZED
  case_29
     R5/R17 MISSING VERI account_service account_7012 VERIFY_RECORD_ABSENT
  case_30
     R5/R17 MISSING VERI account_service account_4163 VERIFY_RECORD_ABSENT
  case_31
     R5/R17 MISSING VERI account_service account_4857 VERIFY_RECORD_ABSENT
  case_32
     R5/R17 MISSING VERI account_service account_8858 VERIFY_RECORD_ABSENT

VALIDATOR output.csv: 0 errors, 264 warnings

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

MEDIA CHECK (vs dev ground truth)
  evidence_09: records=2 resource_ids=EXACT identifiers=DIFF status_values_verbatim=2/2
     user_ids: missing=['user_9842'] extra=[]
  TOTAL (matched / union):
   resource_ids: 26/26 = 100.0%
   identifiers: 34/35 = 97.1%
   status: 203/246 = 82.5%


CUSTOM CASES
| case | what it tests | rule | expected | got | pass |
|---|---|---|---|---|---|
| case_901 (c1_decoy_identity) | evidence holds '<name>.jr@' and a 1-edit near-miss email; neither may link | R2 | COMPLETE [] | COMPLETE [] (intent: fallback(agent_failed)) | PASS |
| case_902 (c2_post_audit_evidence) | account 404 before audit_at, ACTIVE in a file captured after it | R3 + R13 | COMPLETE ['VERIFY_RECORD_ABSENT'] | COMPLETE ['VERIFY_RECORD_ABSENT'] (intent: fallback(agent_failed)) | PASS |
| case_903 (c3_multilingual_negation) | Spanish: 'do not delete my account, only unsubscribe me from the newsletter' | R1 | NOT_APPLICABLE [] | NOT_APPLICABLE [] (intent: fallback(agent_failed)) | PASS |
| case_904 (c4_file_beats_claim) | activity DELETE SUCCESS, but the latest admissible file shows the account present | R4 + R5 | INCOMPLETE ['REPORT_REMAINING_RECORD', 'VERIFY_RECORD_ABSENT'] | INCOMPLETE ['REPORT_REMAINING_RECORD', 'VERIFY_RECORD_ABSENT'] (intent: fallback(agent_failed)) | PASS |
| case_905 (c5_multi_request_user) | two requests by one user; each resource belongs to the request its evidence falls under | R15 | INCOMPLETE ['REPORT_REMAINING_RECORD', 'VERIFY_RECORD_ABSENT'] | INCOMPLETE ['REPORT_REMAINING_RECORD', 'VERIFY_RECORD_ABSENT'] (intent: fallback(agent_failed)) | PASS |
| case_906 (c5_multi_request_user) | two requests by one user; each resource belongs to the request its evidence falls under | R15 | INCOMPLETE ['REPORT_REMAINING_RECORD', 'VERIFY_RECORD_ABSENT'] | INCOMPLETE ['REPORT_REMAINING_RECORD', 'VERIFY_RECORD_ABSENT'] (intent: fallback(agent_failed)) | PASS |
| case_907 (c6_backup_and_legal_hold) | restorable backup plus an active legal hold for the same subject | R9 + R6 (rule_13) | INCOMPLETE ['REPORT_RESTORE_RISK', 'VERIFY_RECORD_PRESENT', 'VERIFY_RESTORE_BLOCKED'] | INCOMPLETE ['REPORT_RESTORE_RISK', 'VERIFY_RECORD_PRESENT', 'VERIFY_RESTORE_BLOCKED'] (intent: fallback(agent_failed)) | PASS |

7/7 custom cases pass (status and full steps_json equal to the hand-written expected.csv; the operation lists above omit remediation for brevity).
```

## Evaluation run 2026-10-24T19:07Z (code/evaluation/main.py)

```text
SAMPLE SCORE
  status_accuracy: 32/32
  exact_steps_json: 17/32
  step_P(7-field): 0.7907
  step_R(7-field): 0.7047
  step_F1(7-field): 0.7452
  step_P(6-field, no step_no): 1.0
  step_R(6-field): 0.8912
  step_F1(6-field): 0.9425
  core_step_recall(6-field, ignoring evidence/step_no): 172/193
  evidence_id_acc_on_matched: 172/172
  sequence_exact(core order): 17/32
  field_accuracy (aligned by resource_id+operation; correct/gold steps): {'step_no': '136/193 (70.5%)', 'phase': '172/193 (89.1%)', 'system_id': '172/193 (89.1%)', 'resource_id': '172/193 (89.1%)', 'operation': '172/193 (89.1%)', 'state': '172/193 (89.1%)', 'evidence_id': '172/193 (89.1%)'}
  intent_paths: {'agent(cache)': 32}
  status_confusion: {'COMPLETE->COMPLETE': 10, 'INCOMPLETE->INCOMPLETE': 22}
  status confusion (gold -> pred): COMPLETE->COMPLETE: 10, INCOMPLETE->INCOMPLETE: 22
  headline before: 32/32  after: 32/32  (no drop)
  flipped vs last run: none
MISSES (15 cases)
  case_03
     R7/R8 MISSING VERI analytics_platform analytics_9406 VERIFY_RECORD_ANONYMIZED
  case_04
     R5/R17 MISSING VERI account_service account_004 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_901 VERIFY_RECORD_ANONYMIZED
  case_18
     R5/R17 MISSING VERI account_service account_5521 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_6645 VERIFY_RECORD_PRESENT
  case_20
     R5/R17 MISSING VERI account_service account_5037 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_5569 VERIFY_RECORD_PRESENT
  case_21
     R5/R17 MISSING VERI account_service account_6440 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_5335 VERIFY_RECORD_ANONYMIZED
  case_22
     R5/R17 MISSING VERI account_service account_4990 VERIFY_RECORD_ABSENT
  case_23
     R5/R17 MISSING VERI account_service account_410 VERIFY_RECORD_ABSENT
  case_25
     R5/R17 MISSING VERI account_service account_3136 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_1895 VERIFY_RECORD_ANONYMIZED
  case_26
     R7/R8 MISSING VERI analytics_platform analytics_4566 VERIFY_RECORD_ANONYMIZED
  case_27
     R7/R8 MISSING VERI analytics_platform analytics_4574 VERIFY_RECORD_ANONYMIZED
  case_28
     R5/R17 MISSING VERI account_service account_5482 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_6077 VERIFY_RECORD_ANONYMIZED
  case_29
     R5/R17 MISSING VERI account_service account_7012 VERIFY_RECORD_ABSENT
  case_30
     R5/R17 MISSING VERI account_service account_4163 VERIFY_RECORD_ABSENT
  case_31
     R5/R17 MISSING VERI account_service account_4857 VERIFY_RECORD_ABSENT
  case_32
     R5/R17 MISSING VERI account_service account_8858 VERIFY_RECORD_ABSENT

VALIDATOR output.csv: 0 errors, 264 warnings

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

MEDIA CHECK (vs dev ground truth)
  evidence_09: records=2 resource_ids=EXACT identifiers=DIFF status_values_verbatim=2/2
     user_ids: missing=['user_9842'] extra=[]
  TOTAL (matched / union):
   resource_ids: 26/26 = 100.0%
   identifiers: 34/35 = 97.1%
   status: 203/246 = 82.5%


CUSTOM CASES
| case | what it tests | rule | expected | got | pass |
|---|---|---|---|---|---|
| case_901 (c1_decoy_identity) | evidence holds '<name>.jr@' and a 1-edit near-miss email; neither may link | R2 | COMPLETE [] | COMPLETE [] (intent: agent) | PASS |
| case_902 (c2_post_audit_evidence) | account 404 before audit_at, ACTIVE in a file captured after it | R3 + R13 | COMPLETE ['VERIFY_RECORD_ABSENT'] | COMPLETE ['VERIFY_RECORD_ABSENT'] (intent: agent(cache)) | PASS |
| case_903 (c3_multilingual_negation) | Spanish: 'do not delete my account, only unsubscribe me from the newsletter' | R1 | NOT_APPLICABLE [] | NOT_APPLICABLE [] (intent: agent) | PASS |
| case_904 (c4_file_beats_claim) | activity DELETE SUCCESS, but the latest admissible file shows the account present | R4 + R5 | INCOMPLETE ['REPORT_REMAINING_RECORD', 'VERIFY_RECORD_ABSENT'] | INCOMPLETE ['REPORT_REMAINING_RECORD', 'VERIFY_RECORD_ABSENT'] (intent: agent(cache)) | PASS |
| case_905 (c5_multi_request_user) | two requests by one user; each resource belongs to the request its evidence falls under | R15 | INCOMPLETE ['REPORT_REMAINING_RECORD', 'VERIFY_RECORD_ABSENT'] | INCOMPLETE ['REPORT_REMAINING_RECORD', 'VERIFY_RECORD_ABSENT'] (intent: agent(cache)) | PASS |
| case_906 (c5_multi_request_user) | two requests by one user; each resource belongs to the request its evidence falls under | R15 | INCOMPLETE ['REPORT_REMAINING_RECORD', 'VERIFY_RECORD_ABSENT'] | INCOMPLETE ['REPORT_REMAINING_RECORD', 'VERIFY_RECORD_ABSENT'] (intent: agent(cache)) | PASS |
| case_907 (c6_backup_and_legal_hold) | restorable backup plus an active legal hold for the same subject | R9 + R6 (rule_13) | INCOMPLETE ['REPORT_RESTORE_RISK', 'VERIFY_RECORD_PRESENT', 'VERIFY_RESTORE_BLOCKED'] | INCOMPLETE ['REPORT_RESTORE_RISK', 'VERIFY_RECORD_PRESENT', 'VERIFY_RESTORE_BLOCKED'] (intent: agent(cache)) | PASS |

7/7 custom cases pass (status and full steps_json equal to the hand-written expected.csv; the operation lists above omit remediation for brevity).
```

## Evaluation run 2026-10-24T19:18Z (code/evaluation/main.py)

```text
SAMPLE SCORE
  status_accuracy: 32/32
  exact_steps_json: 17/32
  step_P(7-field): 0.7907
  step_R(7-field): 0.7047
  step_F1(7-field): 0.7452
  step_P(6-field, no step_no): 1.0
  step_R(6-field): 0.8912
  step_F1(6-field): 0.9425
  core_step_recall(6-field, ignoring evidence/step_no): 172/193
  evidence_id_acc_on_matched: 172/172
  sequence_exact(core order): 17/32
  field_accuracy (aligned by resource_id+operation; correct/gold steps): {'step_no': '136/193 (70.5%)', 'phase': '172/193 (89.1%)', 'system_id': '172/193 (89.1%)', 'resource_id': '172/193 (89.1%)', 'operation': '172/193 (89.1%)', 'state': '172/193 (89.1%)', 'evidence_id': '172/193 (89.1%)'}
  intent_paths: {'agent(cache)': 32}
  status_confusion: {'COMPLETE->COMPLETE': 10, 'INCOMPLETE->INCOMPLETE': 22}
  status confusion (gold -> pred): COMPLETE->COMPLETE: 10, INCOMPLETE->INCOMPLETE: 22
  headline before: 32/32  after: 32/32  (no drop)
  flipped vs last run: none
MISSES (15 cases)
  case_03
     R7/R8 MISSING VERI analytics_platform analytics_9406 VERIFY_RECORD_ANONYMIZED
  case_04
     R5/R17 MISSING VERI account_service account_004 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_901 VERIFY_RECORD_ANONYMIZED
  case_18
     R5/R17 MISSING VERI account_service account_5521 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_6645 VERIFY_RECORD_PRESENT
  case_20
     R5/R17 MISSING VERI account_service account_5037 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_5569 VERIFY_RECORD_PRESENT
  case_21
     R5/R17 MISSING VERI account_service account_6440 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_5335 VERIFY_RECORD_ANONYMIZED
  case_22
     R5/R17 MISSING VERI account_service account_4990 VERIFY_RECORD_ABSENT
  case_23
     R5/R17 MISSING VERI account_service account_410 VERIFY_RECORD_ABSENT
  case_25
     R5/R17 MISSING VERI account_service account_3136 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_1895 VERIFY_RECORD_ANONYMIZED
  case_26
     R7/R8 MISSING VERI analytics_platform analytics_4566 VERIFY_RECORD_ANONYMIZED
  case_27
     R7/R8 MISSING VERI analytics_platform analytics_4574 VERIFY_RECORD_ANONYMIZED
  case_28
     R5/R17 MISSING VERI account_service account_5482 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_6077 VERIFY_RECORD_ANONYMIZED
  case_29
     R5/R17 MISSING VERI account_service account_7012 VERIFY_RECORD_ABSENT
  case_30
     R5/R17 MISSING VERI account_service account_4163 VERIFY_RECORD_ABSENT
  case_31
     R5/R17 MISSING VERI account_service account_4857 VERIFY_RECORD_ABSENT
  case_32
     R5/R17 MISSING VERI account_service account_8858 VERIFY_RECORD_ABSENT

VALIDATOR output.csv: 0 errors, 264 warnings

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

MEDIA CHECK (vs dev ground truth)
  evidence_09: records=2 resource_ids=EXACT identifiers=DIFF status_values_verbatim=5/5
     user_ids: missing=['user_9842'] extra=[]
  evidence_32: records=4 resource_ids=DIFF identifiers=EXACT status_values_verbatim=18/18
     resource_ids: missing=['backup_9281'] extra=[]
  TOTAL (matched / union):
   resource_ids: 25/26 = 96.2%
   identifiers: 34/35 = 97.1%
   status: 201/243 = 82.7%


CUSTOM CASES
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
```

## Evaluation run 2026-10-24T19:20Z (code/evaluation/main.py)

```text
SAMPLE SCORE
  status_accuracy: 32/32
  exact_steps_json: 17/32
  step_P(7-field): 0.7907
  step_R(7-field): 0.7047
  step_F1(7-field): 0.7452
  step_P(6-field, no step_no): 1.0
  step_R(6-field): 0.8912
  step_F1(6-field): 0.9425
  core_step_recall(6-field, ignoring evidence/step_no): 172/193
  evidence_id_acc_on_matched: 172/172
  sequence_exact(core order): 17/32
  field_accuracy (aligned by resource_id+operation; correct/gold steps): {'step_no': '136/193 (70.5%)', 'phase': '172/193 (89.1%)', 'system_id': '172/193 (89.1%)', 'resource_id': '172/193 (89.1%)', 'operation': '172/193 (89.1%)', 'state': '172/193 (89.1%)', 'evidence_id': '172/193 (89.1%)'}
  intent_paths: {'agent(cache)': 32}
  status_confusion: {'COMPLETE->COMPLETE': 10, 'INCOMPLETE->INCOMPLETE': 22}
  status confusion (gold -> pred): COMPLETE->COMPLETE: 10, INCOMPLETE->INCOMPLETE: 22
  headline before: 32/32  after: 32/32  (no drop)
  flipped vs last run: none
MISSES (15 cases)
  case_03
     R7/R8 MISSING VERI analytics_platform analytics_9406 VERIFY_RECORD_ANONYMIZED
  case_04
     R5/R17 MISSING VERI account_service account_004 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_901 VERIFY_RECORD_ANONYMIZED
  case_18
     R5/R17 MISSING VERI account_service account_5521 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_6645 VERIFY_RECORD_PRESENT
  case_20
     R5/R17 MISSING VERI account_service account_5037 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_5569 VERIFY_RECORD_PRESENT
  case_21
     R5/R17 MISSING VERI account_service account_6440 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_5335 VERIFY_RECORD_ANONYMIZED
  case_22
     R5/R17 MISSING VERI account_service account_4990 VERIFY_RECORD_ABSENT
  case_23
     R5/R17 MISSING VERI account_service account_410 VERIFY_RECORD_ABSENT
  case_25
     R5/R17 MISSING VERI account_service account_3136 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_1895 VERIFY_RECORD_ANONYMIZED
  case_26
     R7/R8 MISSING VERI analytics_platform analytics_4566 VERIFY_RECORD_ANONYMIZED
  case_27
     R7/R8 MISSING VERI analytics_platform analytics_4574 VERIFY_RECORD_ANONYMIZED
  case_28
     R5/R17 MISSING VERI account_service account_5482 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_6077 VERIFY_RECORD_ANONYMIZED
  case_29
     R5/R17 MISSING VERI account_service account_7012 VERIFY_RECORD_ABSENT
  case_30
     R5/R17 MISSING VERI account_service account_4163 VERIFY_RECORD_ABSENT
  case_31
     R5/R17 MISSING VERI account_service account_4857 VERIFY_RECORD_ABSENT
  case_32
     R5/R17 MISSING VERI account_service account_8858 VERIFY_RECORD_ABSENT

VALIDATOR output.csv: 0 errors, 264 warnings

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

MEDIA CHECK (vs dev ground truth)
  evidence_09: records=2 resource_ids=EXACT identifiers=DIFF status_values_verbatim=5/5
     user_ids: missing=['user_9842'] extra=[]
  evidence_32: records=4 resource_ids=DIFF identifiers=EXACT status_values_verbatim=18/18
     resource_ids: missing=['backup_9281'] extra=[]
  TOTAL (matched / union):
   resource_ids: 25/26 = 96.2%
   identifiers: 34/35 = 97.1%
   status: 201/243 = 82.7%


CUSTOM CASES
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
```

## Evaluation run 2026-10-24T19:53Z (code/evaluation/main.py)

```text
SAMPLE SCORE
  status_accuracy: 32/32
  exact_steps_json: 17/32
  step_P(7-field): 0.7907
  step_R(7-field): 0.7047
  step_F1(7-field): 0.7452
  step_P(6-field, no step_no): 1.0
  step_R(6-field): 0.8912
  step_F1(6-field): 0.9425
  core_step_recall(6-field, ignoring evidence/step_no): 172/193
  evidence_id_acc_on_matched: 172/172
  sequence_exact(core order): 17/32
  field_accuracy (aligned by resource_id+operation; correct/gold steps): {'step_no': '136/193 (70.5%)', 'phase': '172/193 (89.1%)', 'system_id': '172/193 (89.1%)', 'resource_id': '172/193 (89.1%)', 'operation': '172/193 (89.1%)', 'state': '172/193 (89.1%)', 'evidence_id': '172/193 (89.1%)'}
  intent_paths: {'agent(cache)': 32}
  status_confusion: {'COMPLETE->COMPLETE': 10, 'INCOMPLETE->INCOMPLETE': 22}
  status confusion (gold -> pred): COMPLETE->COMPLETE: 10, INCOMPLETE->INCOMPLETE: 22
  headline before: 32/32  after: 32/32  (no drop)
  flipped vs last run: none
MISSES (15 cases)
  case_03
     R7/R8 MISSING VERI analytics_platform analytics_9406 VERIFY_RECORD_ANONYMIZED
  case_04
     R5/R17 MISSING VERI account_service account_004 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_901 VERIFY_RECORD_ANONYMIZED
  case_18
     R5/R17 MISSING VERI account_service account_5521 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_6645 VERIFY_RECORD_PRESENT
  case_20
     R5/R17 MISSING VERI account_service account_5037 VERIFY_RECORD_ABSENT
     R6/H4 MISSING VERI security_service audit_record_5569 VERIFY_RECORD_PRESENT
  case_21
     R5/R17 MISSING VERI account_service account_6440 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_5335 VERIFY_RECORD_ANONYMIZED
  case_22
     R5/R17 MISSING VERI account_service account_4990 VERIFY_RECORD_ABSENT
  case_23
     R5/R17 MISSING VERI account_service account_410 VERIFY_RECORD_ABSENT
  case_25
     R5/R17 MISSING VERI account_service account_3136 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_1895 VERIFY_RECORD_ANONYMIZED
  case_26
     R7/R8 MISSING VERI analytics_platform analytics_4566 VERIFY_RECORD_ANONYMIZED
  case_27
     R7/R8 MISSING VERI analytics_platform analytics_4574 VERIFY_RECORD_ANONYMIZED
  case_28
     R5/R17 MISSING VERI account_service account_5482 VERIFY_RECORD_ABSENT
     R7/R8 MISSING VERI analytics_platform analytics_6077 VERIFY_RECORD_ANONYMIZED
  case_29
     R5/R17 MISSING VERI account_service account_7012 VERIFY_RECORD_ABSENT
  case_30
     R5/R17 MISSING VERI account_service account_4163 VERIFY_RECORD_ABSENT
  case_31
     R5/R17 MISSING VERI account_service account_4857 VERIFY_RECORD_ABSENT
  case_32
     R5/R17 MISSING VERI account_service account_8858 VERIFY_RECORD_ABSENT

VALIDATOR output.csv: 0 errors, 264 warnings

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

MEDIA CHECK (vs dev ground truth)
  evidence_09: records=2 resource_ids=EXACT identifiers=DIFF status_values_verbatim=5/5
     user_ids: missing=['user_9842'] extra=[]
  evidence_32: records=4 resource_ids=DIFF identifiers=EXACT status_values_verbatim=18/18
     resource_ids: missing=['backup_9281'] extra=[]
  TOTAL (matched / union):
   resource_ids: 25/26 = 96.2%
   identifiers: 34/35 = 97.1%
   status: 201/243 = 82.7%


CUSTOM CASES
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
```
