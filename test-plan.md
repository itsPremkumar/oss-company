# Meta-RSI v9 Stage 7 — Test Plan (t_e78d3ecf)

≥45 tests across 4 modules. All must pass.

## evolution_governance.py — 12 tests

| # | Test | Assertion |
|---|------|-----------|
| EG.1 | Propose evolution | Proposal created with PROPOSED status |
| EG.2 | Duplicate proposal rejected | ValueError on duplicate proposal_id |
| EG.3 | Assign reviewer | Reviewer added, status → REVIEWING |
| EG.4 | Approve with min approvals | Status → APPROVED after 2 approvals |
| EG.5 | Reject proposal | Status → REJECTED, reason recorded |
| EG.6 | Deploy approved | Status → DEPLOYED |
| EG.7 | Deploy unapproved rejected | ValueError on deploying non-approved |
| EG.8 | Rollback deployed | Status → ROLLED_BACK |
| EG.9 | Rollback non-deployed rejected | ValueError on rolling back non-deployed |
| EG.10 | Audit trail | All actions recorded in order |
| EG.11 | Non-reviewer cannot approve | ValueError for unassigned reviewer |
| EG.12 | Get status | Returns correct EvolutionStatus |

## benchmark_contamination_defense.py — 11 tests

| # | Test | Assertion |
|---|------|-----------|
| BC.1 | Register training data | DataSegment created with hash |
| BC.2 | Register benchmark | DataSegment created with hash |
| BC.3 | Check clean benchmark | ContaminationLevel.NONE |
| BC.4 | Check contaminated benchmark | ContaminationLevel.HIGH/CRITICAL |
| BC.5 | Validate integrity (clean) | Returns True |
| BC.6 | Validate integrity (contaminated) | Returns False |
| BC.7 | Get reports filtered | Returns only matching benchmark reports |
| BC.8 | Similarity identical hashes | Returns 1.0 |
| BC.9 | Similarity different hashes | Returns < 1.0 |
| BC.10 | Classify contamination (0 matches) | NONE |
| BC.11 | Classify contamination (many matches) | CRITICAL |

## self_experiment_manager.py — 12 tests

| # | Test | Assertion |
|---|------|-----------|
| SE.1 | Design experiment | Experiment created with DESIGNED status |
| SE.2 | Duplicate experiment rejected | ValueError on duplicate experiment_id |
| SE.3 | Run experiment | Status → COMPLETED, result present |
| SE.4 | Run non-designed rejected | ValueError on running non-designed |
| SE.5 | Max concurrent rejected | RuntimeError when max concurrent reached |
| SE.6 | Abort running | Status → ABORTED |
| SE.7 | Abort non-running rejected | ValueError on aborting non-running |
| SE.8 | Get experiment | Returns correct experiment |
| SE.9 | Get results | Returns ExperimentResult |
| SE.10 | List by status | Returns only matching experiments |
| SE.11 | Capability probe result | success=True, capability_score present |
| SE.12 | Safety boundary result | success=True, safety_score present |

## control_group_enforcement.py — 10 tests

| # | Test | Assertion |
|---|------|-----------|
| CG.1 | Assign treatment | Subject created with treatment group |
| CG.2 | Assign control | Subject created with control group |
| CG.3 | Invalid group rejected | ValueError for non treatment/control |
| CG.4 | Random assignment | Subjects split ~50/50 |
| CG.5 | Check contamination (clean) | Status → INTACT |
| CG.6 | Check contamination (overlap) | Status → CONTAMINATED |
| CG.7 | Validate random assignment | Returns True for balanced split |
| CG.8 | Validate (unbalanced) | Returns False for unbalanced |
| CG.9 | Get subjects by group | Returns only matching subjects |
| CG.10 | Selection bias score | Returns 0.0 for balanced, >0 for unbalanced |

## Total: 45 tests (12 + 11 + 12 + 10)

All tests runnable via `pytest`. Each module independently testable.

Author: @cto
