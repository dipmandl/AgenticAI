# Playwright Automation Skill — Full Reference

## When to use
- Test plan includes UI / E2E / browser testing.
- Repository uses Playwright (Python or JavaScript/TypeScript).

## Folder structure (Python / pytest-playwright)

```
automation/
├── conftest.py                        # session-scoped: server, browser; function-scoped: page
├── pytest.ini                         # markers declaration
├── requirements.txt
├── pages/                             # Page Object Model
│   ├── base_page.py                   # navigate, wait helpers
│   └── release_form_page.py           # one file per page/component
├── tests/
│   ├── release_notes/                 # feature folder — one per user-facing area
│   │   ├── test_add_release_note.py
│   │   ├── test_edit_release_note.py
│   │   └── test_delete_release_note.py
│   ├── release_list/
│   │   └── test_release_list.py
│   └── search/
│       └── test_search_release_note.py
└── utils/
    └── helpers.py
```

**Rule**: folders = features. Test type (positive/negative/boundary) = markers only.

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
    positive:    happy path scenarios
    negative:    invalid input / error paths
    boundary:    edge cases and limits
    e2e:         multi-step end-to-end
    critical:    must-pass release gate
    high:        high priority
    medium:      medium priority
    low:         low priority
    ui:          DOM and visual assertions
    functional:  business behaviour
    manual_only: excluded from automated run

base_url = http://localhost:3000
```

## Page Object pattern

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
from playwright.sync_api import Page, expect

class ReleaseFormPage:
    def __init__(self, page: Page):
        self.page        = page
        self.product     = page.locator("#product")
        self.version     = page.locator("#version")
        self.title_field = page.locator("#title")
        self.description = page.locator("#description")
        self.date        = page.locator("#releaseDate")
        self.breaking    = page.locator("#breaking")
        self.submit_btn  = page.locator("button[type='submit']")

    def fill_all(self, product, version, title, description, date):
        self.product.fill(product)
        self.version.fill(version)
        self.title_field.fill(title)
        self.description.fill(description)
        self.date.fill(date)

    def submit(self):
        self.submit_btn.click()

    def error_locator(self, field: str):
        return self.page.locator(f'.field-error[data-for="{field}"]')

    def assert_error_visible(self, field: str):
        expect(self.error_locator(field)).to_be_visible()

    def assert_error_hidden(self, field: str):
        expect(self.error_locator(field)).to_be_hidden()
```

## Test file pattern

```python
# tests/release_notes/test_add_release_note.py
import pytest
from pages.release_notes_page import ReleaseNotesPage

@pytest.mark.tc("TC-007")
@pytest.mark.req("REQ-002")
@pytest.mark.story_002
@pytest.mark.negative
@pytest.mark.critical
@pytest.mark.smoke
@pytest.mark.ui
def test_submit_empty_product_shows_inline_error(page):
    form = ReleaseFormPage(page)
    form.submit()
    form.assert_error_visible("product")
```

## conftest.py conventions

```python
# conftest.py
import pytest, subprocess, sys, time

@pytest.fixture(scope="session")
def base_url():
    server = subprocess.Popen([sys.executable, "-m", "http.server", "3000", "--directory", "app"])
    time.sleep(1)
    yield "http://localhost:3000"
    server.terminate()

@pytest.fixture
def page(browser, base_url):
    context = browser.new_context()
    pg = context.new_page()
    pg.goto(base_url)
    pg.evaluate("localStorage.clear()")
    pg.reload()
    yield pg
    context.close()
```

## Execution commands

```bash
pytest -m story_002 --browser=chromium
pytest -m "story_002 or story_003" --browser=chromium
pytest -m smoke --browser=chromium
pytest -m "negative and critical" --browser=chromium
pytest tests/release_notes/ --browser=chromium -v
pytest --browser=chromium --headed                   # headed mode for debugging
pytest --tracing=retain-on-failure                   # save trace on failure
```

## Evidence collection
- Screenshot on failure: add `pytest_runtest_makereport` hook in conftest.py
- Trace: `--tracing=retain-on-failure` → saved to `test-results/`
- Video: `record_video_dir="reports/videos/"` in browser context args

## Locator priority (most stable → least stable)
1. `data-testid` attributes — `page.locator('[data-testid="submit"]')`
2. ARIA role — `page.get_by_role("button", name="Submit")`
3. CSS ID — `page.locator("#product")`
4. CSS class with `data-for` attribute — `.field-error[data-for="product"]`
5. ⚠️ Avoid positional CSS (`nth-child`) and full XPath

## Safety
- Never hardcode credentials — use fixtures or environment variables.
- Always use `expect()` for assertions, never bare `assert locator.count() == 1`.
- Classify failures with failure-analysis-agent before changing any assertion or locator.
