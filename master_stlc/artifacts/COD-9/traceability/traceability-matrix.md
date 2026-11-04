# Traceability Matrix — COD-9: Export Release Notes to JSON File

**Story ID:** COD-9
**Pipeline ID:** COD-9-20261103
**Generated:** 2026-11-03T00:40:00Z

---

## Matrix

| TC-ID | REQ-ID | Scenario | Automation File | Status |
|---|---|---|---|---|
| TC-001 | REQ-001 | Export JSON button is visible on page load | steps/step_json_export.py | AUTOMATED |
| TC-002 | REQ-002 | Clicking Export JSON triggers a file download | steps/step_json_export.py | AUTOMATED |
| TC-003 | REQ-002 | Downloaded file has a .json extension | steps/step_json_export.py | AUTOMATED |
| TC-004 | REQ-002, REQ-003 | Downloaded file contains valid parseable JSON | steps/step_json_export.py | AUTOMATED |
| TC-005 | REQ-003 | Exported JSON schema matches localStorage releases schema | steps/step_json_export.py | AUTOMATED |
| TC-006 | REQ-004 | Export with empty localStorage downloads an empty array | steps/step_json_export.py | AUTOMATED |
| TC-007 | REQ-002, REQ-003 | Export with a single release entry downloads a single-element array | steps/step_json_export.py | AUTOMATED |
| TC-008 | REQ-002, REQ-003 | Export with multiple release entries downloads all entries | steps/step_json_export.py | AUTOMATED |
| TC-009 | REQ-004 | Export with empty localStorage does not skip the download | steps/step_json_export.py | AUTOMATED |
| TC-010 | REQ-002, REQ-005 | Export does not mutate localStorage | steps/step_json_export.py | AUTOMATED |
| TC-011 | REQ-002, REQ-004 | Export with corrupted localStorage value produces graceful result | — | MANUAL ONLY |
| TC-012 | REQ-004 | Export does not break when localStorage releases key is absent | steps/step_json_export.py | AUTOMATED |
| TC-013 | REQ-005 | Export does not interfere with other UI button actions | — | MANUAL ONLY |
| TC-014 | REQ-001 | Export button is not duplicated after page reload | steps/step_json_export.py | AUTOMATED |
| TC-015 | REQ-004 | Zero releases — lower bound boundary | steps/step_json_export.py | AUTOMATED |
| TC-016 | REQ-002, REQ-003 | One release — single element boundary | steps/step_json_export.py | AUTOMATED |
| TC-017 | REQ-002, REQ-003 | Large dataset — 100 release notes | steps/step_json_export.py | AUTOMATED |
| TC-018 | REQ-002, REQ-003 | Stress boundary — 1000 release notes | steps/step_json_export.py | AUTOMATED |
| TC-019 | REQ-003 | Special characters in release content are correctly escaped | steps/step_json_export.py | AUTOMATED |
| TC-020 | REQ-003 | Unicode characters in release content are preserved | steps/step_json_export.py | AUTOMATED |
| TC-021 | REQ-002 | Multiple rapid clicks each trigger exactly one valid download | — | MANUAL ONLY |
| TC-022 | REQ-002, REQ-003 | Export succeeds when localStorage is near the 5 MB limit | — | MANUAL ONLY |
| TC-023 | REQ-005 | Release notes list renders correctly after Export feature is added | steps/step_regression.py | AUTOMATED |
| TC-024 | REQ-005 | Add release functionality is unaffected by the Export feature | steps/step_regression.py | AUTOMATED |
| TC-025 | REQ-005 | Edit release functionality is unaffected by the Export feature | steps/step_regression.py | AUTOMATED |
| TC-026 | REQ-005 | Delete release functionality is unaffected by the Export feature | steps/step_regression.py | AUTOMATED |
| TC-027 | REQ-005 | Page navigation and routing are unaffected by the Export feature | steps/step_regression.py | AUTOMATED |
| TC-028 | REQ-005 | localStorage write operations by existing code are unaffected | steps/step_regression.py | AUTOMATED |
| TC-029 | REQ-005 | No new JavaScript console errors are introduced | — | MANUAL ONLY |

---

## Coverage Summary

| Requirement | Description | TC-IDs Automated | TC-IDs Manual | Coverage |
|---|---|---|---|---|
| REQ-001 | Export button visible in UI | TC-001, TC-014 | — | 100% |
| REQ-002 | Clicking Export triggers download | TC-002, TC-003, TC-007, TC-008, TC-016, TC-017, TC-018 | TC-021, TC-022 | 78% |
| REQ-003 | Exported JSON matches localStorage schema | TC-004, TC-005, TC-007, TC-008, TC-016, TC-017, TC-018, TC-019, TC-020 | TC-022 | 90% |
| REQ-004 | Empty storage downloads `[]` | TC-006, TC-009, TC-012, TC-015 | TC-011 | 80% |
| REQ-005 | No impact on other code | TC-010, TC-023, TC-024, TC-025, TC-026, TC-027, TC-028 | TC-013, TC-029 | 78% |

---

## Statistics

| Metric | Count |
|---|---|
| Total test cases | 29 |
| Automated | 24 |
| Manual only | 5 |
| Automation coverage | 82.8% |
| Feature files | 2 |
| Step definition files | 2 |
| Requirements covered | 5/5 |

---

**Artifact Version:** 1.0
**Created:** 2026-11-03T00:40:00Z
