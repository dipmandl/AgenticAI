# Behave Automation Skill — Full Reference

## When to use
- Test plan categories include BDD / Gherkin / acceptance scenarios.
- Stakeholders need business-readable test documentation.
- Repository is Python-based.

## Folder structure

```
automation/
├── features/
│   ├── release_form/              # feature folder — one per user-facing area
│   │   ├── form_submission.feature
│   │   ├── form_validation.feature
│   │   └── form_boundary.feature
│   ├── release_list/
│   │   └── release_list.feature
│   └── environment.py             # browser setup, hooks, teardown
├── steps/
│   ├── release_form_steps.py      # one step file per feature area
│   └── release_list_steps.py
├── pages/                         # Page Object Model
│   ├── base_page.py
│   └── release_form_page.py
├── utils/
│   └── helpers.py                 # shared constants, test data
├── behave.ini
└── requirements.txt
```

**Rule**: Feature files organised by feature area, NOT by test type. Test type (positive/negative/boundary) is expressed via Gherkin tags.

## Tag strategy

```
@TC-001        — traceability: test case ID (always present)
@REQ-001       — traceability: requirement ID (always present)
@story_002     — story ownership (always present)
@smoke         — execution scope: build gate
@regression    — execution scope: pre-release suite
@positive      — test type: happy path
@negative      — test type: invalid input / error paths
@boundary      — test type: edge cases and limits
@e2e           — test type: multi-step end-to-end
@critical      — priority: must-pass gate
@high          — priority
@medium        — priority
@low           — priority
@manual_only   — excluded from automated run
```

## Feature file pattern

```gherkin
# features/release_form/form_validation.feature
Feature: Release form inline validation errors

  @TC-007 @REQ-002 @story_002 @negative @critical @smoke
  Scenario: Submit with empty product field shows inline error
    Given the release form is open with empty fields
    When the user clicks the Submit button
    Then an inline error is visible for the "product" field
    And the release list remains empty

  @TC-008 @REQ-002 @story_002 @negative @high
  Scenario: Submit with empty version field shows inline error
    Given the release form is open with empty fields
    When the user clicks the Submit button
    Then an inline error is visible for the "version" field
```

## Step file pattern

```python
# steps/release_form_steps.py
from behave import given, when, then
from pages.release_form_page import ReleaseFormPage

@given('the release form is open with empty fields')
def step_open_form(context):
    context.form = ReleaseFormPage(context.browser)
    context.form.navigate()

@when('the user clicks the Submit button')
def step_click_submit(context):
    context.form.submit()

@then('an inline error is visible for the "{field}" field')
def step_error_visible(context, field):
    assert context.form.get_error(field).is_displayed(), \
        f"Expected inline error for field '{field}' to be visible"
```

## Page Object pattern

```python
# pages/release_form_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ReleaseFormPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 10)

    def navigate(self):
        self.driver.get(self.driver.base_url)

    def submit(self):
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    def get_error(self, field: str):
        return self.driver.find_element(By.CSS_SELECTOR, f'.field-error[data-for="{field}"]')
```

## environment.py conventions

```python
# features/environment.py
from selenium import webdriver

def before_all(context):
    context.browser = webdriver.Chrome()
    context.browser.base_url = "http://localhost:3000"

def after_step(context, step):
    if step.status == "failed":
        name = context.scenario.name.replace(" ", "_")
        context.browser.save_screenshot(f"reports/screenshots/{name}.png")

def after_all(context):
    context.browser.quit()
```

## behave.ini

```ini
[behave]
format   = pretty
outdir   = reports/allure-results
```

## Execution commands

```bash
# By story
behave --tags=@story_002
behave --tags="@story_002 or @story_003"

# By type
behave --tags=@smoke
behave --tags="@negative and @critical"

# By feature folder
behave features/release_form/

# All tests
behave
```

## Safety
- Never hardcode credentials in step files — use `context.config.userdata` or environment variables.
- Classify failures with the failure-analysis-agent before modifying steps.
- `@manual_only` scenarios must be excluded from CI with `--tags="not @manual_only"`.
