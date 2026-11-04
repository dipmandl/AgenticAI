# Automation Review Input — COD-9: Export Release Notes to JSON File

**Story ID:** COD-9
**Pipeline ID:** COD-9-20261103
**Generated:** 2026-11-03T00:40:00Z
**Framework:** Behave + Selenium (Python BDD)
**Status:** READY FOR REVIEW

---

## Generated Files

All paths are relative to the repository root (`AgenticAI/`).

### Configuration

| File | Purpose |
|---|---|
| `product_release_dashboard/automation/behave.ini` | Behave configuration — feature paths, format, tag exclusion of `@manual_only` |
| `product_release_dashboard/automation/requirements.txt` | Python dependencies: behave, selenium, webdriver-manager, jsonschema, python-dotenv |
| `product_release_dashboard/automation/environment.py` | Browser lifecycle hooks: `before_all`, `before_scenario`, `after_step`, `after_all` |

### Page Object Model

| File | Purpose |
|---|---|
| `product_release_dashboard/automation/pages/release_dashboard_page.py` | Full POM for the Release Notes Dashboard SPA — export button, form, release cards, edit/delete |

### Utilities

| File | Purpose |
|---|---|
| `product_release_dashboard/automation/utils/helpers.py` | localStorage helpers, download polling, JSON schema validation, test data factories |

### Step Definitions

| File | Covers | TC-IDs |
|---|---|---|
| `product_release_dashboard/automation/steps/step_json_export.py` | `export_release_note.feature` — all automated scenarios | TC-001 to TC-010, TC-012, TC-014 to TC-020 |
| `product_release_dashboard/automation/steps/step_regression.py` | `release_notes_stability.feature` — all automated regression scenarios | TC-023 to TC-028 |

### Feature Files (copied from manual/)

| File | Source |
|---|---|
| `product_release_dashboard/automation/features/json_export/export_release_note.feature` | Copied from `product_release_dashboard/manual/json_export/` |
| `product_release_dashboard/automation/features/json_export/release_notes_stability.feature` | Copied from `product_release_dashboard/manual/json_export/` |

---

## TC → File Mapping

| TC-ID | REQ-ID | Feature File | Step File | Status |
|---|---|---|---|---|
| TC-001 | REQ-001 | export_release_note.feature | step_json_export.py | AUTOMATED |
| TC-002 | REQ-002 | export_release_note.feature | step_json_export.py | AUTOMATED |
| TC-003 | REQ-002 | export_release_note.feature | step_json_export.py | AUTOMATED |
| TC-004 | REQ-002, REQ-003 | export_release_note.feature | step_json_export.py | AUTOMATED |
| TC-005 | REQ-003 | export_release_note.feature | step_json_export.py | AUTOMATED |
| TC-006 | REQ-004 | export_release_note.feature | step_json_export.py | AUTOMATED |
| TC-007 | REQ-002, REQ-003 | export_release_note.feature | step_json_export.py | AUTOMATED |
| TC-008 | REQ-002, REQ-003 | export_release_note.feature | step_json_export.py | AUTOMATED |
| TC-009 | REQ-004 | export_release_note.feature | step_json_export.py | AUTOMATED |
| TC-010 | REQ-002, REQ-005 | export_release_note.feature | step_json_export.py | AUTOMATED |
| TC-011 | REQ-002, REQ-004 | export_release_note.feature | — | SKIPPED (manual_only) |
| TC-012 | REQ-004 | export_release_note.feature | step_json_export.py | AUTOMATED |
| TC-013 | REQ-005 | export_release_note.feature | — | SKIPPED (manual_only) |
| TC-014 | REQ-001 | export_release_note.feature | step_json_export.py | AUTOMATED |
| TC-015 | REQ-004 | export_release_note.feature | step_json_export.py | AUTOMATED |
| TC-016 | REQ-002, REQ-003 | export_release_note.feature | step_json_export.py | AUTOMATED |
| TC-017 | REQ-002, REQ-003 | export_release_note.feature | step_json_export.py | AUTOMATED |
| TC-018 | REQ-002, REQ-003 | export_release_note.feature | step_json_export.py | AUTOMATED |
| TC-019 | REQ-003 | export_release_note.feature | step_json_export.py | AUTOMATED |
| TC-020 | REQ-003 | export_release_note.feature | step_json_export.py | AUTOMATED |
| TC-021 | REQ-002 | export_release_note.feature | — | SKIPPED (manual_only) |
| TC-022 | REQ-002, REQ-003 | export_release_note.feature | — | SKIPPED (manual_only) |
| TC-023 | REQ-005 | release_notes_stability.feature | step_regression.py | AUTOMATED |
| TC-024 | REQ-005 | release_notes_stability.feature | step_regression.py | AUTOMATED |
| TC-025 | REQ-005 | release_notes_stability.feature | step_regression.py | AUTOMATED |
| TC-026 | REQ-005 | release_notes_stability.feature | step_regression.py | AUTOMATED |
| TC-027 | REQ-005 | release_notes_stability.feature | step_regression.py | AUTOMATED |
| TC-028 | REQ-005 | release_notes_stability.feature | step_regression.py | AUTOMATED |
| TC-029 | REQ-005 | release_notes_stability.feature | — | SKIPPED (manual_only) |

**Totals:** 24 automated, 5 skipped (manual_only)

---

## Skipped Test Cases

The following 5 test cases carry `@manual_only` and have **no step definitions generated**. They are excluded from automated runs via `behave.ini` tag filter `~@manual_only`.

| TC-ID | Reason |
|---|---|
| TC-011 | Corrupted localStorage — browser behaviour is non-deterministic; requires manual observation |
| TC-013 | UI button interaction isolation — requires human judgment on side-effects |
| TC-021 | Rapid-click race conditions — timing-sensitive; not reliably automatable |
| TC-022 | Near-5 MB localStorage limit — environment-specific browser storage behaviour |
| TC-029 | Console error monitoring — requires browser DevTools open; no Selenium API |

---

## Key Implementation Notes

1. **App URL**: `file:///C:/Users/DipakMandlik/Desktop/AgenticAI/Final_implementation/AgenticAI/product_release_dashboard/index.html`
   The app has no HTTP server; all tests use the `file://` protocol.

2. **Export button ID**: `export-json-button` — this is the new button added by the COD-9 implementation. The existing CSV export button is `export-csv-button`.

3. **localStorage seed pattern**: Each `before_scenario` hook clears localStorage and reloads the app, then individual `Given` steps seed the required state via `driver.execute_script`.

4. **Download verification**: Chrome is configured with a known download directory (`automation/reports/downloads/`). `utils/helpers.wait_for_download()` polls for `.json` files with a 15-second timeout.

5. **Schema validation**: `utils/helpers.validate_release_schema()` uses `jsonschema` to validate each downloaded array against the documented release object schema.

---

## Execution Command

```bash
cd product_release_dashboard/automation

# Install dependencies (first run only)
pip install -r requirements.txt

# Run all automated tests (excludes @manual_only)
behave

# Smoke tests only
behave --tags=@smoke

# Regression tests only
behave --tags=@regression

# Specific feature
behave features/json_export/export_release_note.feature

# Full run with HTML report
behave -f html -o reports/behave_report.html
```

---

**Artifact Version:** 1.0
**Created:** 2026-11-03T00:40:00Z
**Phase:** automation_generation → automation_review
