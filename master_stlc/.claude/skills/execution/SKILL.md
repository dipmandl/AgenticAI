---
name: Test Execution Skill
description: Orchestration of test execution, result capture, and evidence collection
trigger: "when preparing to execute automated tests or setting up test execution"
category: execution
applies_to_phases: [execution]
---

# Test Execution Skill

See [README.md](./README.md) for execution patterns, scope definitions, and evidence capture.

## Quick Reference
- Purpose: Execute approved automation and capture timestamped results
- Scopes: smoke, regression, impacted, all, or specific TC-IDs
- Output: execution-summary.md, metadata.json, raw logs
- Evidence: Timestamped logs, screenshots, execution metadata for analysis
