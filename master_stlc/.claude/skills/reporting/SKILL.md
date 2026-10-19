---
name: Reporting Skill
description: Final STLC report assembly from all phase artifacts into unified HTML and JSON artifacts
trigger: "when generating final STLC report or consolidating execution evidence"
category: reporting
applies_to_phases: [reporting]
---

# Reporting Skill

See [README.md](./README.md) for report structure and artifact consolidation patterns.

## Quick Reference
- Purpose: Assemble final report from all phase artifacts
- Output: final-stlc-report.md/json, agent-metrics.json, stlc-report.html
- Scope: Read-only aggregation of existing artifacts
- Includes: Requirement summary, test results, defects, metrics, traceability matrix
