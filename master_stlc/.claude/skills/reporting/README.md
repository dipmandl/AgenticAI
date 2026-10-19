# Reporting Skill

## Purpose
Guide structured assembly of the final STLC report from existing phase artifacts.

## Reporting principles
- Aggregate only — never re-analyze or re-interpret evidence.
- Use exact counts from `execution-metadata.json`, not re-parsed logs.
- Report only what the artifacts contain; note gaps explicitly rather than omitting them.

## Report sections and artifact sources
| Section | Source artifact |
|---------|----------------|
| Requirement summary | `requirements/requirement-analysis.md` |
| Repository analysis | `repository/repository-discovery.md` |
| Test planning | `test-planning/test-plan.md` |
| Manual test cases | `test-cases/test-case-inventory.md` |
| Test review | `reviews/test-case-review.md` |
| Automation plan | `automation/automation-plan.md` |
| Automation review | `reviews/automation-review.md` |
| Execution results | `execution/execution-metadata.json` |
| Failure analysis | `execution/failure-analysis.md` |
| Self-healing | `self-healing/self-healing-report.md` |
| Defects | `defects/DEF-*.md` |
| Traceability | `traceability/traceability-matrix.md` |

## Metrics collection
For each agent phase, record in `metrics/agent-metrics.json`:
```json
{
  "agent": "<agent name>",
  "phase": "<phase name>",
  "status": "SUCCESS | PARTIAL_SUCCESS | FAILED | SKIPPED",
  "files_read": [],
  "files_created": [],
  "files_modified": [],
  "duration_seconds": 0
}
```

## JSON report schema stability
The `final-stlc-report.json` schema must remain stable across projects:
```json
{
  "pipeline_id": "",
  "story_id": "",
  "requirements": 0,
  "test_cases_existing": 0,
  "test_cases_created": 0,
  "tests_automated": 0,
  "tests_executed": 0,
  "passed": 0,
  "failed": 0,
  "skipped": 0,
  "healed": 0,
  "defects": 0
}
```

## Secret masking
Before writing any report, replace the following with `***MASKED***`:
- Values matching patterns: `password`, `secret`, `token`, `api_key`, `auth`
- Any value from environment variables known to contain credentials
