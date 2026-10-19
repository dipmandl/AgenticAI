---
name: API Test Automation Skill
description: Framework-agnostic API testing with feature-based structure and 2-category marker strategy
trigger: "when automating API tests or building contract-driven test suites"
category: automation
frameworks: [pytest, behave, rest-assured]
languages: [python, javascript, java]
applies_to_phases: [automation-generation, automation-review, execution]
---

# API Test Automation Skill

See [README.md](./README.md) for full patterns, examples, and conventions.

## Quick Reference

- **Type**: API, contract, integration testing
- **Frameworks**: pytest + requests/httpx (Python), Jest + axios (JS), REST Assured (Java)
- **Best for**: Backend validation, contract testing, integration verification

## Folder structure

```
automation/
├── conftest.py               # session-scoped: base_url, auth token, http client
├── pytest.ini                # markers declaration
├── requirements.txt
├── clients/                  # API client layer (replaces POM for API tests)
│   └── <resource>_client.py  # one client per API resource group
├── tests/
│   └── <resource>/           # feature/resource folders (auth/, releases/, users/)
│       └── test_<scenario>.py
├── schemas/                  # JSON schemas for response validation
│   └── <resource>_schema.json
└── utils/
    └── helpers.py
```

## Marker strategy — 2 categories

**Category 1 — Test type**: `smoke` · `regression` · `positive` · `negative` · `boundary` · `contract` · `critical` · `high` · `medium` · `low` · `api` · `manual_only`

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
@pytest.mark.api
def test_<scenario>(api_client):
```

## Key run commands

```bash
pytest -m story_002
pytest -m "story_002 or story_003"
pytest -m smoke
pytest -m "negative and critical"
pytest tests/releases/ -v
```
