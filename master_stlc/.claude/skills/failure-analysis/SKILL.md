---
name: Failure Analysis Skill
description: Root cause classification of test failures into APPLICATION, AUTOMATION, ENVIRONMENT, and DATA failure types
trigger: "when analyzing test execution failures or classifying failure root causes"
category: analysis
applies_to_phases: [failure-analysis]
---

# Failure Analysis Skill

See [README.md](./README.md) for failure classification taxonomy and analysis patterns.

## Quick Reference
- Purpose: Classify test failures by root cause
- Categories: APPLICATION_FAILURE, AUTOMATION_FAILURE, ENVIRONMENT_FAILURE, TEST_DATA_FAILURE
- Output: failure-analysis.md with classified failures
- Determines: Whether self-healing or defect reporting is appropriate
