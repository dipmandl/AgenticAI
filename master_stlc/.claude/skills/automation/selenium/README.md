# Selenium Automation Skill — Full Reference

## When to use
- Repository already uses Selenium WebDriver.
- Test plan includes cross-browser UI testing.
- Migrating legacy Selenium tests into the STLC pipeline.

## Folder structure

```
automation/
├── conftest.py                        # driver fixture, base_url, credentials
├── pytest.ini                         # markers declaration
├── requirements.txt
├── pages/                             # Page Object Model
│   ├── base_page.py                   # shared driver helpers, explicit wait wrappers
│   └── release_form_page.py           # one file per page/component
├── tests/
│   ├── release_form/                  # feature folder
│   │   ├── test_form_submission.py
│   │   ├── test_form_validation.py
│   │   └── test_form_boundary.py
│   ├── release_list/
│   │   └── test_release_list.py
│   └── regression/
│       └── test_end_to_end.py
└── utils/
    └── helpers.py                     # shared constants, test data
```

**Rule**: folders = features. Test type = markers.

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
```

## Page Object pattern

```python
# pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 10)

    def navigate(self, path=""):
        self.driver.get(self.driver.base_url + path)

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()
```

```python
# pages/release_form_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ReleaseFormPage(BasePage):
    PRODUCT     = (By.ID, "product")
    VERSION     = (By.ID, "version")
    TITLE       = (By.ID, "title")
    DESCRIPTION = (By.ID, "description")
    DATE        = (By.ID, "releaseDate")
    SUBMIT      = (By.CSS_SELECTOR, "button[type='submit']")

    def fill_all(self, product, version, title, description, date):
        self.find(self.PRODUCT).send_keys(product)
        self.find(self.VERSION).send_keys(version)
        self.find(self.TITLE).send_keys(title)
        self.find(self.DESCRIPTION).send_keys(description)
        self.find(self.DATE).send_keys(date)

    def submit(self):
        self.click(self.SUBMIT)

    def get_error(self, field: str):
        return self.find((By.CSS_SELECTOR, f'.field-error[data-for="{field}"]'))

    def is_error_visible(self, field: str) -> bool:
        return self.get_error(field).is_displayed()
```

## Test file pattern

```python
# tests/release_form/test_form_validation.py
import pytest
from pages.release_form_page import ReleaseFormPage

@pytest.mark.tc("TC-007")
@pytest.mark.req("REQ-002")
@pytest.mark.story_002
@pytest.mark.negative
@pytest.mark.critical
@pytest.mark.smoke
@pytest.mark.ui
def test_submit_empty_product_shows_inline_error(driver):
    form = ReleaseFormPage(driver)
    form.navigate()
    form.submit()
    assert form.is_error_visible("product"), "Expected inline error for product field"
```

## conftest.py conventions

```python
# conftest.py
import pytest
from selenium import webdriver

@pytest.fixture(scope="session")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    d = webdriver.Chrome(options=options)
    d.base_url = "http://localhost:3000"
    d.implicitly_wait(0)          # use explicit waits only — never implicit
    yield d
    d.quit()
```

## Execution commands

```bash
pytest -m story_002
pytest -m "story_002 or story_003"
pytest -m smoke
pytest -m "negative and critical"
pytest tests/release_form/ -v
```

## Evidence on failure

```python
# conftest.py — automatic screenshot on failure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report  = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            name = item.name.replace(" ", "_")
            driver.save_screenshot(f"reports/screenshots/{name}.png")
```

## Locator priority (most stable → least stable)
1. `By.ID` — `(By.ID, "product")`
2. `By.CSS_SELECTOR` with `data-testid` — `[data-testid="submit"]`
3. `By.CSS_SELECTOR` with stable class + attribute
4. ⚠️ Avoid `By.XPATH` with positional indices (`//div[2]/span[1]`)
5. ⚠️ Never use `By.CLASS_NAME` alone for interactive elements

## Safety
- Always use explicit waits (`WebDriverWait`) — never `time.sleep` or implicit waits.
- Never hardcode credentials — use conftest fixtures and environment variables.
- Classify failures with failure-analysis-agent before changing locators or assertions.
