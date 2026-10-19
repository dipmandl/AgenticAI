# API Automation Skill — Full Reference

## When to use
- Test plan includes API / contract / integration testing.
- The project exposes HTTP endpoints to be validated.

## Folder structure (Python / pytest + requests)

```
automation/
├── conftest.py                        # session: base_url, auth token, http session
├── pytest.ini                         # markers declaration
├── requirements.txt
├── clients/                           # API client layer — equivalent of POM for APIs
│   ├── base_client.py                 # shared headers, auth, error handling
│   └── releases_client.py             # one client per resource group
├── tests/
│   ├── releases/                      # resource/feature folder
│   │   ├── test_create_release.py     # positive + valid flows
│   │   ├── test_create_validation.py  # negative + error responses
│   │   └── test_create_boundary.py    # boundary values
│   ├── auth/
│   │   └── test_auth.py
│   └── regression/
│       └── test_integration.py        # cross-resource flows
├── schemas/                           # JSON Schema files for contract validation
│   └── release_schema.json
└── utils/
    └── helpers.py                     # shared constants, test data factories
```

**Rule**: folders = API resource or feature area. Test type = markers.

## pytest.ini — marker declarations

```ini
[pytest]
markers =
    tc:          test case ID — @pytest.mark.tc("TC-001")
    req:         requirement ID — @pytest.mark.req("REQ-001")
    story_001:   tests for STORY-001
    story_002:   tests for STORY-002
    smoke:       fast build sanity
    regression:  full pre-release suite
    sanity:      quick post-deploy check
    positive:    valid input / success response scenarios
    negative:    invalid input / error response scenarios
    boundary:    edge case values and limits
    contract:    schema / contract validation tests
    e2e:         multi-step integration flows
    critical:    must-pass release gate
    high:        high priority
    medium:      medium priority
    low:         low priority
    api:         HTTP / API response assertions
    manual_only: excluded from automated run
```

## API Client pattern

```python
# clients/base_client.py
import requests

class BaseClient:
    def __init__(self, base_url: str, session: requests.Session = None):
        self.base_url = base_url
        self.session  = session or requests.Session()

    def get(self, path: str, **kwargs):
        return self.session.get(f"{self.base_url}{path}", **kwargs)

    def post(self, path: str, **kwargs):
        return self.session.post(f"{self.base_url}{path}", **kwargs)
```

```python
# clients/releases_client.py
from clients.base_client import BaseClient

class ReleasesClient(BaseClient):
    PATH = "/api/releases"

    def create(self, payload: dict):
        return self.post(self.PATH, json=payload)

    def list_all(self):
        return self.get(self.PATH)

    def get_by_id(self, release_id: str):
        return self.get(f"{self.PATH}/{release_id}")
```

## Test file pattern

```python
# tests/releases/test_create_validation.py
import pytest

@pytest.mark.tc("TC-007")
@pytest.mark.req("REQ-002")
@pytest.mark.story_002
@pytest.mark.negative
@pytest.mark.critical
@pytest.mark.smoke
@pytest.mark.api
def test_create_release_missing_product_returns_400(releases_client):
    payload = {"version": "1.0.0", "title": "Test", "description": "Desc", "releaseDate": "2026-09-23"}
    resp = releases_client.create(payload)
    assert resp.status_code == 400
    body = resp.json()
    assert "product" in body.get("errors", {}), "Expected field error for 'product'"
```

## Schema validation pattern

```python
# tests/releases/test_create_release.py
import jsonschema, json, pytest

@pytest.mark.tc("TC-001")
@pytest.mark.req("REQ-001")
@pytest.mark.story_002
@pytest.mark.positive
@pytest.mark.contract
@pytest.mark.smoke
def test_create_release_response_matches_schema(releases_client, release_schema):
    payload = {"product": "Alpha", "version": "1.0.0", "title": "Release",
               "description": "Desc", "releaseDate": "2026-09-23"}
    resp = releases_client.create(payload)
    assert resp.status_code == 201
    jsonschema.validate(resp.json(), release_schema)
```

## conftest.py conventions

```python
# conftest.py
import json, pytest, requests
from clients.releases_client import ReleasesClient

@pytest.fixture(scope="session")
def base_url():
    return "http://localhost:3000"

@pytest.fixture(scope="session")
def http_session(base_url):
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s

@pytest.fixture(scope="session")
def releases_client(base_url, http_session):
    return ReleasesClient(base_url, http_session)

@pytest.fixture(scope="session")
def release_schema():
    with open("schemas/release_schema.json") as f:
        return json.load(f)
```

## Execution commands

```bash
# By story
pytest -m story_002
pytest -m "story_002 or story_003"

# By type
pytest -m smoke
pytest -m "negative and critical"
pytest -m contract

# By resource folder
pytest tests/releases/ -v
pytest tests/auth/ -v

# Full suite with report
pytest -v --html=reports/report.html --self-contained-html
```

## Evidence on failure
- Log full request + response in a pytest fixture finalizer:
  ```python
  # URL, method, status code, response body (truncated to 500 chars)
  # Never log auth headers or tokens
  ```
- Write to `reports/api-failures/<timestamp>-<tc_id>.log`

## Authentication patterns
- Bearer token: obtain via a session-scoped login fixture; set in `Authorization` header
- API key: read from `os.environ["API_KEY"]`, never hardcode
- Refresh if the session token expires mid-run

## Safety
- Always test against a designated test environment — never production.
- Do not create, update, or delete production data.
- Classify failures with failure-analysis-agent before modifying client code or assertions.
- `manual_only` tests must be excluded from CI with `-m "not manual_only"`.
