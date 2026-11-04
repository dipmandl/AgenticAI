# Framework Selection — COD-9: Export Release Notes to JSON File

**Story ID:** COD-9  
**Pipeline ID:** COD-9-20261103  
**Selection Date:** 2026-11-03  
**Framework:** Behave (Python/Gherkin)  
**Status:** CONFIRMED

---

## Decision Summary

| Field | Value |
|---|---|
| **Selected Framework** | Behave (Python BDD with Gherkin) |
| **Decision Basis** | EXISTING_CONFIRMED |
| **Evidence** | Gherkin feature files already generated and validated |
| **Test Runner** | behave (Python) |
| **Browser Driver** | Selenium WebDriver (Python) with ChromeDriver |
| **Configuration File** | automation/behave.ini |
| **Feature Root** | automation/features/ |
| **Step Definitions** | automation/steps/step_*.py |
| **Project Root** | product_release_dashboard |
| **Automation Root** | automation |
| **Test Root** | features |
| **Run From** | automation |
| **Execution Command** | behave |

---

## Discovery and Justification

### Existing Automation Signals Detected

The framework selection was based on the following concrete evidence:

1. **Gherkin Feature Files Present (Confirmed)**
   - Path: `product_release_dashboard/manual/json_export/export_release_note.feature`
   - Path: `product_release_dashboard/manual/json_export/release_notes_stability.feature`
   - Status: Already generated in prior test-generation phase
   - Scope: 29 total test scenarios across two feature files (TS-P-001 through TS-R-007)

2. **Test Scenarios Ready for Automation**
   - Positive scenarios: 8 (TS-P-001 to TS-P-008) — all suitable for automation
   - Negative scenarios: 6 (TS-N-001 to TS-N-006) — 4 automated, 2 manual
   - Boundary scenarios: 8 (TS-B-001 to TS-B-008) — 6 automated, 2 manual
   - Regression scenarios: 7 (TS-R-001 to TS-R-007) — 6 automated, 1 manual

3. **Gherkin Format Already Structured**
   - Feature: "Export Release Notes to JSON"
   - Feature: "Release Notes Stability (Regression)"
   - Steps follow Given/When/Then (BDD) convention
   - Tags: @story-001, @smoke, @positive, @negative, @boundary, @regression

### Why Behave?

**Best-fit rationale:**

- **Existing Gherkin investment:** 29 test scenarios already written in `.feature` format
- **Stakeholder alignment:** Gherkin is human-readable; non-technical stakeholders can validate test intent
- **BDD discipline:** The test plan used BDD language (preconditions, steps, expected results); Behave preserves that structure
- **Python ecosystem:** Matches target application stack (vanilla JavaScript SPA, tested via Python Selenium)
- **Step reusability:** Step definitions can be shared across multiple features and scenarios
- **Browser automation:** Integrates seamlessly with Selenium WebDriver for browser interaction
- **Traceability:** Scenario tags preserve TC and REQ IDs for audit trail

### Decision Override Rationale

This is **NOT an override** — the framework was confirmed to already exist. Behave is the natural choice because:
- The `.feature` files are already committed to the repository
- The test plan references them by scenario ID
- There is zero rework required to adopt Behave

---

## Feature Areas Identified

Derived from the test plan scenario groupings and `.feature` file organization:

| Feature Area | Automated Tests | Manual Tests | Test File(s) |
|---|---|---|---|
| Export Action | TS-P-001, TS-P-002, TS-P-003, TS-P-006 | None | export_release_note.feature |
| Export Output (JSON) | TS-P-004, TS-P-005, TS-P-007, TS-P-008 | None | export_release_note.feature |
| Empty State Handling | TS-P-006, TS-N-001, TS-B-001 | None | export_release_note.feature |
| Data Integrity | TS-N-002, TS-N-004, TS-N-006 | TS-N-003, TS-N-005 | export_release_note.feature |
| Boundary & Scale | TS-B-002 to TS-B-006 | TS-B-007, TS-B-008 | export_release_note.feature |
| Regression (Existing Features) | TS-R-001 to TS-R-006 | TS-R-007 | release_notes_stability.feature |

---

## File Structure

**Project Root:** `product_release_dashboard` (read from `artifacts/COD-9/discovery/repository-discovery.md`)

All paths are anchored inside `<project_root>` — the STLC artifact pipeline root is external.

```
product_release_dashboard/
├── manual/
│   └── json_export/
│       ├── export_release_note.feature       ← Manual test specs (TC-001 to TC-016)
│       ├── release_notes_stability.feature   ← Manual test specs (TC-017 to TC-029)
│       └── test-plan.md                      ← Reference only
│
└── automation/                                ← Framework working directory (cd here to run)
    ├── behave.ini                            ← Behave configuration
    ├── environment.py                        ← Browser setup/teardown fixtures
    ├── requirements.txt                      ← Python dependencies
    ├── conftest.py                           ← pytest fixtures (if running certain tests)
    ├── pages/
    │   └── release_notes_page.py             ← Page Object Model for release notes UI
    ├── steps/
    │   ├── step_export.py                    ← Export feature step definitions
    │   ├── step_json_export.py               ← JSON validation step definitions
    │   └── step_regression.py                ← Regression (existing features) steps
    ├── utils/
    │   ├── browser_utils.py                  ← Browser interaction helpers
    │   ├── file_utils.py                     ← Downloaded file inspection helpers
    │   └── schema_validator.py               ← JSON schema and data comparison
    └── features/                             ← Feature-based folder (MANDATORY)
        └── json_export/                      ← Feature area folder
            ├── export_release_note.feature   ← Export action + output tests
            └── release_notes_stability.feature ← Regression tests
```

### Mandatory Naming Rules

1. **Feature files** go into `automation/features/<feature_area>/` — never at the root
   - Each feature area gets its own subfolder (e.g., `json_export/`)
   - Feature names are **feature-based**, not category-based

2. **Step definitions** go into `automation/steps/step_<area>.py`
   - Example: `step_export.py` for export action steps
   - Example: `step_regression.py` for regression steps

3. **Manual test specs** go into `product_release_dashboard/manual/<feature_area>/`
   - These are reference-only; not executed by Behave
   - Provides audit trail and manual test case mapping

4. **Test data** is loaded via `environment.py` (global setup) or step fixtures
   - Avoid hardcoding; use parameterization where possible

5. **Traceability tags** are preserved in `.feature` file headers:
   - `@story-COD-9` — Story ownership
   - `@tc-001` through `@tc-029` — Test case IDs
   - `@req-001` through `@req-005` — Requirement traceability
   - `@smoke` / `@regression` — Test category

---

## Test Categories and Markers

### Behave Tag Strategy

Behave uses tags to select and filter scenarios during execution. The tag structure for this story:

```gherkin
@story-COD-9 @tc-001 @req-001 @smoke @positive
Scenario: Export button is visible on page load
  Given the user has the release notes app open
  When the page finishes loading
  Then the Export button is visible in the dashboard toolbar
```

**Marker meanings:**

| Tag | Meaning | Selection |
|---|---|---|
| `@story-COD-9` | Belongs to story COD-9 | `behave -t @story-COD-9` |
| `@tc-001` | Test case ID TC-001 | `behave -t @tc-001` |
| `@req-001` | Covers requirement REQ-001 | `behave -t @req-001` |
| `@smoke` | Smoke test (critical gate) | `behave -t @smoke` |
| `@positive` | Happy-path scenario | `behave -t @positive` |
| `@negative` | Error-path scenario | `behave -t @negative` |
| `@boundary` | Edge-case / boundary test | `behave -t @boundary` |
| `@regression` | Regression test (existing features) | `behave -t @regression` |

### Test Execution Commands

```bash
# Navigate to automation root
cd product_release_dashboard/automation

# Run all scenarios for story COD-9
behave -t @story-COD-9

# Run only smoke tests
behave -t @smoke

# Run only regression tests
behave -t @regression

# Run all features with detailed output
behave --no-capture

# Run specific feature file
behave features/json_export/export_release_note.feature

# Run with dry-run (print steps without execution)
behave --dry-run

# Generate HTML report
behave -f html -o reports/behave_report.html
```

---

## Dependencies and Setup

### Python Environment

**Required packages** (to be listed in `automation/requirements.txt`):

```
behave==1.2.6
selenium==4.15.0
webdriver-manager==4.0.1
jsonschema==4.20.0
python-dotenv==1.0.0
```

**Python version:** 3.8+

### Browser Driver Setup

The test automation will use **ChromeDriver** (Selenium WebDriver) managed via `webdriver-manager`:

```python
# In environment.py or conftest.py
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def before_all(context):
    """Setup browser before all scenarios"""
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Auto-download management
    prefs = {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False
    }
    options.add_experimental_option("prefs", prefs)
    
    service = Service(ChromeDriverManager().install())
    context.driver = webdriver.Chrome(service=service, options=options)

def after_all(context):
    """Teardown browser after all scenarios"""
    context.driver.quit()
```

### File Download Interception

Since the feature involves triggering file downloads, the browser must be configured to:
1. Allow automatic downloads (no user prompt)
2. Save to a known directory (checked by test helpers)
3. Preserve file extension and naming

**Implementation approach:**
- Chrome download directory: `automation/downloads/` (created per test run)
- Helper function: `utils/file_utils.py::get_latest_download()`
- Verification: JSON parsing + schema validation

### Selenium Integration with Behave

Step definitions access the Selenium driver via `context.driver`:

```python
# In steps/step_export.py
from behave import given, when, then

@when('the user clicks the Export button')
def step_click_export(context):
    button = context.driver.find_element("id", "export-btn")
    button.click()
    # Wait for download to complete (helper)
    context.file_path = wait_for_download(context)

@then('a JSON file is downloaded')
def step_json_downloaded(context):
    assert context.file_path is not None, "No file downloaded"
    assert context.file_path.endswith('.json'), "File is not JSON"
```

---

## Configuration File: behave.ini

Located at `automation/behave.ini`:

```ini
[behave]
# Feature file paths
paths = features

# Output format
format = progress
stdout_capture = false
stderr_capture = false

# Logging
logging_level = INFO
logging_format = %(levelname)s:%(name)s:%(message)s

# Tags
tags_require = story-COD-9

# Dry-run (set to 1 for dry-run by default)
dry_run = false

# Strict (fail on undefined steps)
strict = true

# Name of the environment.py module
userdata_define = --userdata
```

---

## Traceability Mapping

### Test Case to Feature Mapping

| TC ID | Scenario ID | Feature File | Feature | Status |
|---|---|---|---|---|
| TC-001 | TS-P-001 | export_release_note.feature | Export button is visible | AUTO |
| TC-002 | TS-P-002 | export_release_note.feature | Clicking Export triggers download | AUTO |
| TC-003 | TS-P-003 | export_release_note.feature | Downloaded file has .json extension | AUTO |
| TC-004 | TS-P-004 | export_release_note.feature | Downloaded file contains valid JSON | AUTO |
| TC-005 | TS-P-005 | export_release_note.feature | Exported JSON schema matches localStorage | AUTO |
| TC-006 | TS-P-006 | export_release_note.feature | Export with empty localStorage downloads [] | AUTO |
| TC-007 | TS-P-007 | export_release_note.feature | Export with single release entry | AUTO |
| TC-008 | TS-P-008 | export_release_note.feature | Export with multiple release entries | AUTO |
| TC-009 | TS-N-001 | export_release_note.feature | Empty storage does NOT skip download | AUTO |
| TC-010 | TS-N-002 | export_release_note.feature | Export does not mutate localStorage | AUTO |
| TC-011 | TS-N-003 | export_release_note.feature | Corrupted localStorage value (MANUAL) | MANUAL |
| TC-012 | TS-N-004 | export_release_note.feature | Export when localStorage key absent | AUTO |
| TC-013 | TS-N-005 | export_release_note.feature | Export does not break other buttons (MANUAL) | MANUAL |
| TC-014 | TS-N-006 | export_release_note.feature | Export button not duplicated on reload | AUTO |
| TC-015 | TS-B-001 | export_release_note.feature | Zero releases boundary | AUTO |
| TC-016 | TS-B-002 | export_release_note.feature | One release boundary | AUTO |
| TC-017 | TS-B-003 | export_release_note.feature | Large dataset (100 releases) | AUTO |
| TC-018 | TS-B-004 | export_release_note.feature | Stress boundary (1000 releases) | AUTO |
| TC-019 | TS-B-005 | export_release_note.feature | Special characters (quotes, newlines) | AUTO |
| TC-020 | TS-B-006 | export_release_note.feature | Unicode characters | AUTO |
| TC-021 | TS-B-007 | export_release_note.feature | Multiple rapid clicks (MANUAL) | MANUAL |
| TC-022 | TS-B-008 | export_release_note.feature | Max localStorage size (MANUAL) | MANUAL |
| TC-023 | TS-R-001 | release_notes_stability.feature | Release list rendering unaffected | AUTO |
| TC-024 | TS-R-002 | release_notes_stability.feature | Add release functionality unaffected | AUTO |
| TC-025 | TS-R-003 | release_notes_stability.feature | Edit release functionality unaffected | AUTO |
| TC-026 | TS-R-004 | release_notes_stability.feature | Delete release functionality unaffected | AUTO |
| TC-027 | TS-R-005 | release_notes_stability.feature | Page navigation unaffected | AUTO |
| TC-028 | TS-R-006 | release_notes_stability.feature | localStorage write operations unaffected | AUTO |
| TC-029 | TS-R-007 | release_notes_stability.feature | No console errors (MANUAL) | MANUAL |

### Requirement to Test Case Mapping

| REQ ID | Requirement | Covered By | Count |
|---|---|---|---|
| REQ-001 | Export button visible in UI | TC-001 | 1 |
| REQ-002 | Clicking Export triggers download | TC-002, TC-003, TC-007, TC-008, TC-017, TC-018 | 6 |
| REQ-003 | Exported JSON matches localStorage schema | TC-005, TC-007, TC-008, TC-016, TC-017, TC-018, TC-020 | 7 |
| REQ-004 | Empty storage downloads `[]` | TC-006, TC-009, TC-015 | 3 |
| REQ-005 | No impact on other code | TC-010 to TC-029 (all regression) | 17 |

---

## Browser and Environment Compatibility

### Supported Browsers

**Primary (tested):**
- Google Chrome (latest stable) ← ChromeDriver focus

**Secondary (cross-browser validation via manual tests):**
- Mozilla Firefox
- Microsoft Edge
- Apple Safari

### Platform Support

| OS | Status | Driver | Notes |
|---|---|---|---|
| Windows 11 | Primary | ChromeDriver | Current environment |
| macOS | Supported | ChromeDriver | Requires manual Safari testing |
| Linux | Supported | ChromeDriver | CI/CD environment |

### Selenium Version Compatibility

- **Selenium 4.15.0** — Supports modern WebDriver protocol
- **Python 3.8+** — Minimum version for feature compatibility
- **webdriver-manager 4.0.1** — Auto-manages driver binary (no manual download needed)

---

## Known Constraints and Mitigations

| Constraint | Impact | Mitigation |
|---|---|---|
| Browser download prompts may block automation | HIGH | Configure Chrome profile to auto-download; use webdriver-manager |
| File system inspection during test | MEDIUM | Use helper function `get_latest_download()` to locate downloaded file |
| Cross-browser API differences (Blob, URL.createObjectURL) | MEDIUM | Primary tests use Chrome; cross-browser tests marked as MANUAL or use feature detection |
| localStorage access from Selenium | LOW | Use `driver.execute_script("return localStorage.getItem(...)")` to read/write |
| Large dataset performance (1000 releases) | MEDIUM | Stress test marked as MANUAL; automation tests up to 100 releases |
| Race conditions on rapid clicks | LOW | Use explicit waits; document debounce requirements in defect if issue found |

---

## Execution Environment Details

### Pre-Execution Checklist

- [ ] Python 3.8+ installed
- [ ] pip dependencies installed from `automation/requirements.txt`
- [ ] ChromeDriver auto-installed via webdriver-manager
- [ ] `automation/downloads/` directory writable
- [ ] Browser sandbox disabled (Chrome options)
- [ ] `behave.ini` configured and present in `automation/`
- [ ] Feature files present in `automation/features/json_export/`
- [ ] Step definition files present in `automation/steps/`
- [ ] `environment.py` fixture configured for driver setup/teardown

### Resolved Execution Command

```bash
cd product_release_dashboard/automation && behave
```

**Breakdown:**
- `cd product_release_dashboard/automation` — Navigate to automation root (framework's working directory)
- `behave` — Run all scenarios in `features/` directory using configuration in `behave.ini`

**With options:**

```bash
# Smoke tests only
cd product_release_dashboard/automation && behave -t @smoke

# Generate HTML report
cd product_release_dashboard/automation && behave -f html -o reports/behave_report.html

# Specific feature file
cd product_release_dashboard/automation && behave features/json_export/export_release_note.feature
```

---

## Decision Record

| Field | Value |
|---|---|
| **Decision Date** | 2026-11-03 |
| **Decision Type** | Framework Selection |
| **Selected Framework** | Behave (Python BDD) |
| **Evidence** | Feature files already generated; test plan structured as BDD scenarios |
| **Basis** | EXISTING_CONFIRMED |
| **Approved By** | User (explicit confirmation) |
| **State** | FINALIZED |
| **Next Phase** | Automation Generation (develop step definitions and Page Object Model) |

---

## Summary

**Behave** is the confirmed framework for COD-9's Export Release Notes to JSON feature. The decision is based on:

1. **Pre-existing Gherkin feature files** that encode 29 test scenarios
2. **BDD alignment** with the structured test plan (Given/When/Then)
3. **Python + Selenium integration** for browser automation
4. **Zero rework** required — features are ready for step definition implementation
5. **Traceability preservation** — TC and REQ IDs are encoded as tags

**Next steps:**
- Automation generation agent will create step definitions in `automation/steps/`
- Page Object Model in `automation/pages/release_notes_page.py`
- Helper utilities in `automation/utils/` for file inspection and schema validation
- `environment.py` fixture for browser lifecycle management
- Execution agent will run `cd product_release_dashboard/automation && behave` to validate all scenarios

---

**Artifact Version:** 1.0  
**Created:** 2026-11-03T00:35:00Z  
**Framework Status:** CONFIRMED AND READY FOR AUTOMATION GENERATION
