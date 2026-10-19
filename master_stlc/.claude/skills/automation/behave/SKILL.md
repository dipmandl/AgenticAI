---
name: Behave BDD Skill
description: Python BDD framework with feature-based Gherkin structure and 2-category tag strategy
trigger: "when selecting behave for BDD-style test automation"
category: automation
frameworks: [behave]
languages: [python]
applies_to_phases: [automation-generation, automation-review, execution]
---

# Behave BDD Skill

See [README.md](./README.md) for full patterns, examples, and conventions.

## Quick Reference

- **Framework**: Behave (Python Cucumber)
- **Language**: Python + Gherkin
- **Best for**: Acceptance testing, BDD, business-readable scenarios

## Folder structure

```
automation/
├── features/
│   ├── <feature>/              # one folder per feature (login/, release_form/)
│   │   └── <scenario>.feature
│   └── environment.py          # browser/driver setup and hooks
├── steps/
│   └── <feature>_steps.py      # one step file per feature
├── pages/                      # Page Object Model
│   └── <feature>_page.py
├── utils/
│   └── helpers.py
├── behave.ini
└── requirements.txt
```

## Tag strategy — 2 categories

**Category 1 — Test type**: `@smoke` · `@regression` · `@positive` · `@negative` · `@boundary` · `@e2e` · `@critical` · `@high` · `@medium` · `@low` · `@manual_only`

**Category 2 — Story tag**: `@story_002` · `@story_NNN`

**Traceability**: `@TC-001` · `@REQ-001` — on every scenario for reports

## Scenario tag template

```gherkin
@TC-001 @REQ-001 @story_002 @smoke @critical @positive
Scenario: Successful form submission with all fields valid
```

## Key run commands

```bash
behave --tags=@story_002
behave --tags="@story_002 or @story_003"
behave --tags=@smoke
behave --tags="@negative and @critical"
behave features/release_form/
```
