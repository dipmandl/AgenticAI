# Test Case Inventory — COD-9: Export Release Notes to JSON File

## Metadata

| Field | Value |
|---|---|
| Story ID | COD-9 |
| Pipeline ID | COD-9-20261103 |
| Inventory Date | 2026-11-03 |
| Agent | manual-test-generation-agent (claude-sonnet-4-6[1m]) |
| Total Test Cases | 29 |
| Feature Files | 2 |

---

## Feature File Locations

| Feature File | Path |
|---|---|
| export_release_note.feature | `product_release_dashboard/manual/json_export/export_release_note.feature` |
| release_notes_stability.feature | `product_release_dashboard/manual/json_export/release_notes_stability.feature` |

---

## Feature: json_export — Export Release Note

Scenarios for the core export action: positive, negative, and boundary tests for the JSON export feature.

| TC-ID | REQ | Tags | Scenario Title | Feature File |
|---|---|---|---|---|
| TC-001 | REQ-001 | @positive @smoke @critical @ui | Export JSON button is visible on page load | `product_release_dashboard/manual/json_export/export_release_note.feature` |
| TC-002 | REQ-002 | @positive @smoke @critical @ui | Clicking Export JSON triggers a file download | `product_release_dashboard/manual/json_export/export_release_note.feature` |
| TC-003 | REQ-002 | @positive @regression @high @ui | Downloaded file has a .json extension | `product_release_dashboard/manual/json_export/export_release_note.feature` |
| TC-004 | REQ-002, REQ-003 | @positive @smoke @critical @ui | Downloaded file contains valid parseable JSON | `product_release_dashboard/manual/json_export/export_release_note.feature` |
| TC-005 | REQ-003 | @positive @smoke @critical @ui | Exported JSON schema matches the localStorage releases schema | `product_release_dashboard/manual/json_export/export_release_note.feature` |
| TC-006 | REQ-004 | @positive @smoke @critical @ui | Export with empty localStorage downloads an empty array | `product_release_dashboard/manual/json_export/export_release_note.feature` |
| TC-007 | REQ-002, REQ-003 | @positive @regression @high @ui | Export with a single release entry downloads a single-element array | `product_release_dashboard/manual/json_export/export_release_note.feature` |
| TC-008 | REQ-002, REQ-003 | @positive @regression @high @ui | Export with multiple release entries downloads all entries | `product_release_dashboard/manual/json_export/export_release_note.feature` |
| TC-009 | REQ-004 | @negative @smoke @critical @ui | Export with empty localStorage does not skip the download | `product_release_dashboard/manual/json_export/export_release_note.feature` |
| TC-010 | REQ-002, REQ-005 | @negative @regression @high @ui | Export does not mutate localStorage | `product_release_dashboard/manual/json_export/export_release_note.feature` |
| TC-011 | REQ-002, REQ-004 | @negative @regression @high @ui @manual_only | Export with corrupted localStorage value produces a valid or graceful result | `product_release_dashboard/manual/json_export/export_release_note.feature` |
| TC-012 | REQ-004 | @negative @regression @high @ui | Export does not break when the localStorage releases key is absent | `product_release_dashboard/manual/json_export/export_release_note.feature` |
| TC-013 | REQ-005 | @negative @regression @high @ui @manual_only | Export does not interfere with other UI button actions | `product_release_dashboard/manual/json_export/export_release_note.feature` |
| TC-014 | REQ-001 | @negative @regression @medium @ui | Export button is not duplicated after page reload | `product_release_dashboard/manual/json_export/export_release_note.feature` |
| TC-015 | REQ-004 | @boundary @smoke @critical @ui | Zero releases — lower bound boundary | `product_release_dashboard/manual/json_export/export_release_note.feature` |
| TC-016 | REQ-002, REQ-003 | @boundary @regression @high @ui | One release — single element boundary | `product_release_dashboard/manual/json_export/export_release_note.feature` |
| TC-017 | REQ-002, REQ-003 | @boundary @regression @high @ui | Large dataset — 100 release notes | `product_release_dashboard/manual/json_export/export_release_note.feature` |
| TC-018 | REQ-002, REQ-003 | @boundary @regression @medium @ui | Stress boundary — 1000 release notes | `product_release_dashboard/manual/json_export/export_release_note.feature` |
| TC-019 | REQ-003 | @boundary @regression @high @ui | Special characters in release content are correctly escaped | `product_release_dashboard/manual/json_export/export_release_note.feature` |
| TC-020 | REQ-003 | @boundary @regression @high @ui | Unicode characters in release content are preserved | `product_release_dashboard/manual/json_export/export_release_note.feature` |
| TC-021 | REQ-002 | @boundary @regression @medium @ui @manual_only | Multiple rapid clicks each trigger exactly one valid download | `product_release_dashboard/manual/json_export/export_release_note.feature` |
| TC-022 | REQ-002, REQ-003 | @boundary @regression @low @ui @manual_only | Export succeeds when localStorage is near the 5 MB browser storage limit | `product_release_dashboard/manual/json_export/export_release_note.feature` |

---

## Feature: json_export — Release Notes Stability After Export Feature

Regression scenarios verifying that existing release note operations are unaffected by the addition of the JSON export feature.

| TC-ID | REQ | Tags | Scenario Title | Feature File |
|---|---|---|---|---|
| TC-023 | REQ-005 | @regression @high @ui | Release notes list renders correctly after Export feature is added | `product_release_dashboard/manual/json_export/release_notes_stability.feature` |
| TC-024 | REQ-005 | @regression @high @ui | Add release functionality is unaffected by the Export feature | `product_release_dashboard/manual/json_export/release_notes_stability.feature` |
| TC-025 | REQ-005 | @regression @high @ui | Edit release functionality is unaffected by the Export feature | `product_release_dashboard/manual/json_export/release_notes_stability.feature` |
| TC-026 | REQ-005 | @regression @high @ui | Delete release functionality is unaffected by the Export feature | `product_release_dashboard/manual/json_export/release_notes_stability.feature` |
| TC-027 | REQ-005 | @regression @medium @ui | Page navigation and routing are unaffected by the Export feature | `product_release_dashboard/manual/json_export/release_notes_stability.feature` |
| TC-028 | REQ-005 | @regression @high @ui | localStorage write operations by existing code are unaffected | `product_release_dashboard/manual/json_export/release_notes_stability.feature` |
| TC-029 | REQ-005 | @regression @high @ui @manual_only | No new JavaScript console errors are introduced by the Export feature | `product_release_dashboard/manual/json_export/release_notes_stability.feature` |

---

## Coverage Summary

| Requirement | Covered By |
|---|---|
| REQ-001 | TC-001, TC-014 |
| REQ-002 | TC-002, TC-003, TC-004, TC-007, TC-008, TC-009, TC-010, TC-011, TC-016, TC-017, TC-018, TC-021, TC-022 |
| REQ-003 | TC-004, TC-005, TC-007, TC-008, TC-016, TC-017, TC-018, TC-019, TC-020, TC-022 |
| REQ-004 | TC-006, TC-009, TC-011, TC-012, TC-015 |
| REQ-005 | TC-010, TC-013, TC-023, TC-024, TC-025, TC-026, TC-027, TC-028, TC-029 |

### Acceptance Criteria Coverage

| AC | Description | Test Cases |
|---|---|---|
| AC-1 | Given release notes exist, clicking Export downloads a .json file | TC-002, TC-003, TC-007, TC-008 |
| AC-2 | Exported file contains a valid JSON array matching localStorage schema | TC-004, TC-005, TC-016, TC-019, TC-020 |
| AC-3 | Given no release notes exist, Export downloads a file with [] | TC-006, TC-009, TC-012, TC-015 |

---

## Test Type Breakdown

| Type | Count | TC-IDs |
|---|---|---|
| @smoke | 7 | TC-001, TC-002, TC-004, TC-005, TC-006, TC-009, TC-015 |
| @positive | 8 | TC-001 to TC-008 |
| @negative | 6 | TC-009 to TC-014 |
| @boundary | 8 | TC-015 to TC-022 |
| @regression | 14 | TC-010, TC-011, TC-012, TC-013, TC-014, TC-016, TC-017, TC-018, TC-019, TC-020, TC-021, TC-022, TC-023 to TC-029 |
| @manual_only | 5 | TC-011, TC-013, TC-021, TC-022, TC-029 |
| @critical | 7 | TC-001, TC-002, TC-004, TC-005, TC-006, TC-009, TC-015 |
| @high | 16 | TC-003, TC-007, TC-008, TC-010, TC-011, TC-012, TC-013, TC-016, TC-017, TC-019, TC-020, TC-023, TC-024, TC-025, TC-026, TC-028, TC-029 |
| @medium | 4 | TC-014, TC-018, TC-021, TC-027 |
| @low | 1 | TC-022 |

---

## Test Plan to TC Traceability

| Test Plan Scenario | TC-ID | Scenario Title |
|---|---|---|
| TS-P-001 | TC-001 | Export JSON button is visible on page load |
| TS-P-002 | TC-002 | Clicking Export JSON triggers a file download |
| TS-P-003 | TC-003 | Downloaded file has a .json extension |
| TS-P-004 | TC-004 | Downloaded file contains valid parseable JSON |
| TS-P-005 | TC-005 | Exported JSON schema matches the localStorage releases schema |
| TS-P-006 | TC-006 | Export with empty localStorage downloads an empty array |
| TS-P-007 | TC-007 | Export with a single release entry downloads a single-element array |
| TS-P-008 | TC-008 | Export with multiple release entries downloads all entries |
| TS-N-001 | TC-009 | Export with empty localStorage does not skip the download |
| TS-N-002 | TC-010 | Export does not mutate localStorage |
| TS-N-003 | TC-011 | Export with corrupted localStorage value produces a valid or graceful result |
| TS-N-004 | TC-012 | Export does not break when the localStorage releases key is absent |
| TS-N-005 | TC-013 | Export does not interfere with other UI button actions |
| TS-N-006 | TC-014 | Export button is not duplicated after page reload |
| TS-B-001 | TC-015 | Zero releases — lower bound boundary |
| TS-B-002 | TC-016 | One release — single element boundary |
| TS-B-003 | TC-017 | Large dataset — 100 release notes |
| TS-B-004 | TC-018 | Stress boundary — 1000 release notes |
| TS-B-005 | TC-019 | Special characters in release content are correctly escaped |
| TS-B-006 | TC-020 | Unicode characters in release content are preserved |
| TS-B-007 | TC-021 | Multiple rapid clicks each trigger exactly one valid download |
| TS-B-008 | TC-022 | Export succeeds when localStorage is near the 5 MB browser storage limit |
| TS-R-001 | TC-023 | Release notes list renders correctly after Export feature is added |
| TS-R-002 | TC-024 | Add release functionality is unaffected by the Export feature |
| TS-R-003 | TC-025 | Edit release functionality is unaffected by the Export feature |
| TS-R-004 | TC-026 | Delete release functionality is unaffected by the Export feature |
| TS-R-005 | TC-027 | Page navigation and routing are unaffected by the Export feature |
| TS-R-006 | TC-028 | localStorage write operations by existing code are unaffected |
| TS-R-007 | TC-029 | No new JavaScript console errors are introduced by the Export feature |
