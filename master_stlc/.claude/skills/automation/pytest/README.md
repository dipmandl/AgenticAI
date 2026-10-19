# Pytest Automation Skill — Full Reference

## When to use
- Repository is Python-based or framework-agnostic.
- Test plan includes UI, API, integration, or unit scenarios.
- pytest or pytest-playwright is selected by the framework-selection-agent.

## Folder structure

```
automation/
├── conftest.py                        # session-scoped fixtures (server, browser, auth)
├── pytest.ini                         # markers only — no paths or plugins here
├── requirements.txt                   # pytest, pytest-playwright, pytest-html
├── pages/                             # Page Object Model
│   ├── base_page.py                   # shared navigation and wait helpers
│   └── release_form_page.py           # one file per page/component
├── tests/
│   ├── release_notes/                 # feature folder — one per user-facing area
│   │   ├── test_add_release_note.py   # all scenarios for adding a release note
│   │   ├── test_edit_release_note.py  # all scenarios for editing a release note
│   │   └── test_delete_release_note.py# all scenarios for deleting a release note
│   ├── release_list/
│   │   └── test_release_list.py
│   └── search/                        # another feature area
│       └── test_search_release_note.py
└── utils/
    ├── helpers.py                     # shared constants, localStorage keys, field lists
    └── test_data.py                   # reusable test data factories
```

**Rule**: test type (positive/negative/boundary) is expressed via markers, NOT folder names. Folders = features only.

## pytest.ini — marker declarations

```ini
[pytest]
markers =
    # Traceability — parametrized, no individual tc_NNN entries
    tc: test case identifier — usage: @pytest.mark.tc("TC-001")
    req: requirement identifier — usage: @pytest.mark.req("REQ-001")

    # Story tags — add one entry per story as stories are generated
    story_001: tests generated for STORY-001
    story_002: tests generated for STORY-002

    # Test type
    smoke:       fast sanity check, run on every build
    regression:  full suite, run pre-release
    sanity:      quick post-deploy smoke
    positive:    happy path / valid input scenarios
    negative:    invalid input / error path scenarios
    boundary:    edge case and limit value scenarios
    e2e:         multi-step end-to-end flows
    critical:    must-pass gate — blocks release if failing
    high:        high priority
    medium:      medium priority
    low:         low priority
    ui:          DOM and visual assertions
    api:         HTTP / API response assertions
    functional:  business behaviour verification
    manual_only: cannot be automated — excluded from automated run

base_url = http://localhost:3000
```

## Page Object Model pattern

```python
# pages/base_page.py
class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate(self, path=""):
        self.page.goto(f"http://localhost:3000/{path}")
```

```python
# pages/release_form_page.py
from playwright.sync_api import expect

class ReleaseFormPage:
    def __init__(self, page):
        self.page = page
        # Locators — defined once, used everywhere
        self.product     = page.locator("#product")
        self.version     = page.locator("#version")
        self.title       = page.locator("#title")
        self.description = page.locator("#description")
        self.date        = page.locator("#releaseDate")
        self.breaking    = page.locator("#breaking")
        self.submit_btn  = page.locator("button[type='submit']")

    def fill_all(self, product, version, title, description, date):
        self.product.fill(product)
        self.version.fill(version)
        self.title.fill(title)
        self.description.fill(description)
        self.date.fill(date)

    def submit(self):
        self.submit_btn.click()

    def get_error(self, field: str):
        return self.page.locator(f'.field-error[data-for="{field}"]')

    def error_visible(self, field: str):
        expect(self.get_error(field)).to_be_visible()

    def error_hidden(self, field: str):
        expect(self.get_error(field)).to_be_hidden()
```

## Test file pattern

```python
# tests/release_notes/test_add_release_note.py
import pytest
from pages.release_notes_page import ReleaseNotesPage

@pytest.mark.tc("TC-001")
@pytest.mark.req("REQ-001")
@pytest.mark.req("REQ-003")
@pytest.mark.story_002
@pytest.mark.smoke
@pytest.mark.critical
@pytest.mark.positive
@pytest.mark.ui
def test_successful_submission_all_fields_valid(page):
    form = ReleaseFormPage(page)
    form.fill_all("Product Alpha", "1.0.0", "Initial Release", "First release.", "2026-09-23")
    form.submit()
    # assertions ...
```

## utils/helpers.py pattern

```python
# utils/helpers.py
LS_KEY    = "releaseNotesDashboard.releases"
LS_READ   = f"JSON.parse(localStorage.getItem('{LS_KEY}') || '[]')"
FIELDS    = ["product", "version", "title", "description", "releaseDate"]
BASE_URL  = "http://localhost:3000"
```

## conftest.py conventions

- **Session-scoped**: HTTP server startup, browser launch, auth token generation
- **Function-scoped**: page creation, localStorage clear, test data seed
- Clear localStorage + reload before every test to ensure isolation
- Never share mutable state between tests via fixtures

## Execution commands

```bash
# By story — impacted area
pytest -m story_002
pytest -m "story_002 or story_003"

# By type — CI gates
pytest -m smoke
pytest -m "regression and critical"
pytest -m "negative and story_002"

# By feature folder
pytest tests/release_notes/ -v
pytest tests/release_notes/test_add_release_note.py -v

# Full suite with report
pytest automation/tests/ -v --html=automation/reports/report.html --self-contained-html
```

## Evidence on failure
- Screenshot: call `page.screenshot(path=f"reports/screenshots/{test_name}.png")` in a `conftest.py` finalizer
- Trace: enable with `--tracing=retain-on-failure`

## Safety
- Never hardcode credentials — use fixtures or environment variables.
- Never modify application code or test data outside designated test data utilities.
- Classify failures with the failure-analysis-agent before changing any assertion.
- `manual_only` tests must never be run in CI — gate them with the marker.
