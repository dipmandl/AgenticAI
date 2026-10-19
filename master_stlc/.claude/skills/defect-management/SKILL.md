---
name: Defect Analysis Skill
description: Structured formatting of APPLICATION_FAILURE evidence into formal defect artifacts
trigger: "when creating defect records from test failure evidence"
category: defect-management
applies_to_phases: [defect-analysis]
---

# Defect Analysis Skill

See [README.md](./README.md) for defect structure and external defect integration patterns.

## Quick Reference
- Purpose: Document functional failures as formal defects
- Scope: APPLICATION_FAILURE failures only
- Output: DEF-### defect files with severity, impact, root cause
- Integration: Optional external defect system (if configured)
