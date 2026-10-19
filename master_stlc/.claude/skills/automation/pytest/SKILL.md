---
name: Pytest Automation Skill
description: Python-based test automation with feature-based structure, Page Object Model, and 2-category marker strategy
trigger: "when selecting pytest for test automation or implementing pytest test structure"
category: automation
frameworks: [pytest]
languages: [python]
applies_to_phases: [automation-generation, automation-review, execution]
---

# Pytest Automation Skill

See [README.md](./README.md) for full patterns, examples, and conventions.

## Quick Reference

- **Framework**: pytest + pytest-playwright (UI) or requests/httpx (API)
- **Language**: Python 3.8+
- **Best for**: UI, API, integration, unit testing

## Folder structure

```
automation/
├── conftest.py               # server + browser fixtures (session-scoped)
├── pytest.ini                # markers declaration
├── requirements.txt
├── pages/                    # Page Object Model — one file per page/component
│   ├── base_page.py
│   └── <feature>_page.py
├── tests/
│   └── <feature>/            # one folder per feature (login/, release_form/, search/)
│       └── test_<scenario>.py
└── utils/
    └── helpers.py            # shared constants, test data, reusable assertions
```

## Marker strategy — 2 categories

**Category 1 — Test type** (what kind of test):
`smoke` · `regression` · `sanity` · `positive` · `negative` · `boundary` · `e2e` · `critical` · `high` · `medium` · `low` · `ui` · `api` · `functional` · `manual_only`

**Category 2 — Story tag** (which story owns this test):
`story_001` · `story_002` · `story_NNN` — one tag per story, added to pytest.ini per story

**Traceability** (for reports, not for filtering — parametrized):
`@pytest.mark.tc("TC-001")` · `@pytest.mark.req("REQ-001")`

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
pytest -m story_002                        # all tests for one story
pytest -m "story_002 or story_003"         # impacted area run
pytest -m smoke                            # build gate
pytest -m "negative and critical"          # release gate
pytest tests/release_form/                 # all tests for one feature
```
