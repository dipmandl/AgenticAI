---
name: Self-Healing Skill
description: Safe, bounded repair patterns for AUTOMATION_FAILURE issues without weakening assertions
trigger: "when fixing brittle test automation or addressing AUTOMATION_FAILURE failures"
category: repair
applies_to_phases: [self-healing]
---

# Self-Healing Skill

See [README.md](./README.md) for safe repair patterns and forbidden self-healing actions.

## Quick Reference
- Scope: AUTOMATION_FAILURE only (locator drift, timing, config, syntax)
- Forbidden: Changing assertions, loosening expectations, modifying app code
- Patterns: Locator update, wait/timing fix, setup correction, syntax fix
- Safety: Never weaken test expectations
