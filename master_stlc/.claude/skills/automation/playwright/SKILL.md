---
name: Playwright Browser Automation Skill
description: Cross-browser UI automation with feature-based structure, POM, and 2-category marker strategy
trigger: "when selecting playwright for browser automation or E2E testing"
category: automation
frameworks: [playwright]
languages: [python, javascript]
applies_to_phases: [automation-generation, automation-review, execution]
---

# Playwright Browser Automation Skill

See [README.md](./README.md) for full patterns, examples, and conventions.

## Quick Reference

- **Framework**: Playwright (Python via pytest-playwright, or JS/TS)
- **Browsers**: Chromium, Firefox, WebKit
- **Best for**: UI testing, E2E, browser automation

## Folder structure

```
automation/
├── conftest.py               # browser, page, auth fixtures
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

#Example Folder Structure
```
automation/
├── conftest.py               # browser, page, auth fixtures
├── pytest.ini                # markers declaration
├── requirements.txt
├── pages/                    # Page Object Model
│   ├── base_page.py
│   └── login_page.py
│   └── release_form_page.py
├── tests/
│   └── login/            # feature folders (login/, release_form/)
│       └── test_login.py
│   └── release_form/            # feature folders (login/, release_form/)
│       └── test_release_form.py
└── utils/
    └── helpers.py
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
def test_<scenario>(page):
```

## Key run commands

```bash
pytest -m story_002
pytest -m "story_002 or story_003"
pytest -m smoke --browser=chromium
pytest -m "negative and critical"
pytest tests/release_form/ --browser=chromium
```
