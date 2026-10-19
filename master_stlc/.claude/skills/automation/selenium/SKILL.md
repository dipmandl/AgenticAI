---
name: Selenium Browser Automation Skill
description: WebDriver-based UI automation with feature-based structure, POM, and 2-category marker strategy
trigger: "when selecting selenium for browser automation or legacy test migration"
category: automation
frameworks: [selenium]
languages: [python, javascript, java]
applies_to_phases: [automation-generation, automation-review, execution]
---

# Selenium Browser Automation Skill

See [README.md](./README.md) for full patterns, examples, and conventions.

## Quick Reference

- **Framework**: Selenium WebDriver + pytest
- **Languages**: Python, JavaScript, Java
- **Best for**: Cross-browser UI automation, legacy test migration
- **Browsers**: Chrome, Firefox, Safari, Edge

## Folder structure

```
automation/
├── conftest.py               # driver fixture, base_url, auth
├── pytest.ini                # markers declaration
├── requirements.txt
├── pages/                    # Page Object Model
│   ├── base_page.py
│   └── <feature>_page.py
├── tests/
│   └── <feature>/            # feature folders (login/, release_form/)
│       └── test_<scenario>.py
└── utils/
    └── helpers.py
```

## Marker strategy — 2 categories

**Category 1 — Test type**: `smoke` · `regression` · `positive` · `negative` · `boundary` · `e2e` · `critical` · `high` · `medium` · `low` · `ui` · `manual_only`

**Category 2 — Story tag**: `story_NNN` — one per story

**Traceability** (parametrized): `@pytest.mark.tc("TC-001")` · `@pytest.mark.req("REQ-001")`

## Test marker template

```python
@pytest.mark.tc("TC-001")
@pytest.mark.req("REQ-001")
@pytest.mark.story_002
@pytest.mark.smoke
@pytest.mark.critical
@pytest.mark.positive
@pytest.mark.ui
def test_<scenario>(driver):
```

## Key run commands

```bash
pytest -m story_002
pytest -m "story_002 or story_003"
pytest -m smoke
pytest -m "negative and critical"
pytest tests/release_form/ -v
```
