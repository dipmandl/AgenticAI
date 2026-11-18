# Test Case Inventory — COD-8

**Story ID**: COD-8
**Story Title**: Delete a release note with confirmation
**Author**: Manual Test Generation Agent
**Date**: 2026-11-05
**Total Test Cases**: 24 (TC-001 to TC-024)

---

## Coverage Summary

| Category   | TC Range       | Count | Priority              |
|------------|----------------|-------|-----------------------|
| Positive   | TC-001 – TC-008 | 8    | CRITICAL (5), HIGH (3) |
| Negative   | TC-009 – TC-013 | 5    | HIGH (3), MEDIUM (1), LOW (1) |
| Boundary   | TC-014 – TC-018 | 5    | HIGH (4), MEDIUM (1)  |
| Regression | TC-019 – TC-024 | 6    | HIGH (3), MEDIUM (3)  |

---

## Feature: delete_release

| TC-ID  | REQ(s)                    | Tags                                                        | Scenario Title                                                                      | Feature File |
|--------|---------------------------|-------------------------------------------------------------|-------------------------------------------------------------------------------------|--------------|
| TC-001 | REQ-001                   | @positive @smoke @critical @ui                              | TC-001 Delete button is visible on every rendered release card                      | product_release_dashboard/manual/delete_release/delete_release.feature |
| TC-002 | REQ-002                   | @positive @smoke @critical @ui                              | TC-002 Clicking Delete shows a browser confirmation dialog                          | product_release_dashboard/manual/delete_release/delete_release.feature |
| TC-003 | REQ-003, REQ-005          | @positive @smoke @critical @ui                              | TC-003 Confirmed deletion removes the targeted release card from the DOM            | product_release_dashboard/manual/delete_release/delete_release.feature |
| TC-004 | REQ-004                   | @positive @smoke @critical @ui                              | TC-004 Confirmed deletion removes the release from localStorage                     | product_release_dashboard/manual/delete_release/delete_release.feature |
| TC-005 | REQ-003, REQ-005          | @positive @smoke @critical @ui                              | TC-005 Release card count decreases by exactly one after a confirmed deletion       | product_release_dashboard/manual/delete_release/delete_release.feature |
| TC-006 | REQ-003, REQ-005          | @positive @regression @high @ui                             | TC-006 Other releases are unaffected after a single confirmed deletion              | product_release_dashboard/manual/delete_release/delete_release.feature |
| TC-007 | REQ-004                   | @positive @regression @high @ui                             | TC-007 Deleted release does not reappear after a page reload                        | product_release_dashboard/manual/delete_release/delete_release.feature |
| TC-008 | REQ-003, REQ-004, REQ-005 | @positive @regression @high @ui                             | TC-008 Deleting a release that is open in edit mode resets the form and removes the card | product_release_dashboard/manual/delete_release/delete_release.feature |
| TC-009 | REQ-006                   | @negative @smoke @high @ui                                  | TC-009 Cancelling the confirmation dialog keeps the release visible in the UI       | product_release_dashboard/manual/delete_release/delete_release.feature |
| TC-010 | REQ-006                   | @negative @regression @high @ui                             | TC-010 Cancelling the confirmation dialog leaves localStorage unchanged             | product_release_dashboard/manual/delete_release/delete_release.feature |
| TC-011 | REQ-006                   | @negative @regression @high @ui                             | TC-011 Dismissing the confirmation dialog without confirming has the same effect as cancelling | product_release_dashboard/manual/delete_release/delete_release.feature |
| TC-012 | REQ-003, REQ-004          | @negative @regression @medium @ui @manual_only              | TC-012 Invoking deleteRelease with a non-existent ID does not corrupt state         | product_release_dashboard/manual/delete_release/delete_release.feature |
| TC-013 | REQ-003, REQ-004          | @negative @regression @low @ui                              | TC-013 Rapid successive deletions do not corrupt the releases state                 | product_release_dashboard/manual/delete_release/delete_release.feature |
| TC-014 | REQ-003, REQ-004, REQ-005 | @boundary @smoke @high @ui                                  | TC-014 Deleting the only remaining release renders the empty state                  | product_release_dashboard/manual/delete_release/delete_release.feature |
| TC-015 | REQ-003, REQ-005          | @boundary @regression @high @ui                             | TC-015 Deleting the first release in the list leaves the remaining releases intact  | product_release_dashboard/manual/delete_release/delete_release.feature |
| TC-016 | REQ-003, REQ-005          | @boundary @regression @high @ui                             | TC-016 Deleting the last release in the list leaves the remaining releases intact   | product_release_dashboard/manual/delete_release/delete_release.feature |
| TC-017 | REQ-005                   | @boundary @regression @medium @ui                           | TC-017 Active product filter is preserved after a deletion triggers re-render       | product_release_dashboard/manual/delete_release/delete_release.feature |
| TC-018 | REQ-004                   | @boundary @regression @high @ui                             | TC-018 Deleted release remains absent after multiple consecutive page reloads       | product_release_dashboard/manual/delete_release/delete_release.feature |
| TC-019 | REQ-004                   | @regression @high @ui                                       | TC-019 Add release still persists correctly after delete code changes               | product_release_dashboard/manual/delete_release/delete_release.feature |
| TC-020 | REQ-003, REQ-005          | @regression @medium @ui                                     | TC-020 Edit form for release A is unaffected when a different release B is deleted  | product_release_dashboard/manual/delete_release/delete_release.feature |
| TC-021 | REQ-005                   | @regression @high @ui                                       | TC-021 Filter and search results are correct after a release is deleted             | product_release_dashboard/manual/delete_release/delete_release.feature |
| TC-022 | REQ-004                   | @regression @high @ui                                       | TC-022 JSON export does not include a release that has been deleted                 | product_release_dashboard/manual/delete_release/delete_release.feature |
| TC-023 | REQ-004, REQ-005          | @regression @medium @ui                                     | TC-023 Application shows correct state when all releases are deleted and page is reloaded | product_release_dashboard/manual/delete_release/delete_release.feature |
| TC-024 | REQ-004                   | @regression @medium @ui @manual_only                        | TC-024 Deletion in one tab is reflected after a reload of a second tab              | product_release_dashboard/manual/delete_release/delete_release.feature |

---

## Requirement Coverage

| REQ ID  | Requirement Summary                        | Covered By |
|---------|--------------------------------------------|------------|
| REQ-001 | Delete button present on each release card | TC-001 |
| REQ-002 | Confirmation prompt shown before deletion  | TC-002 |
| REQ-003 | In-memory state updated on confirm         | TC-003, TC-005, TC-006, TC-008, TC-012, TC-013, TC-014, TC-015, TC-016, TC-020 |
| REQ-004 | localStorage updated on confirm            | TC-004, TC-007, TC-008, TC-012, TC-013, TC-014, TC-018, TC-019, TC-022, TC-023, TC-024 |
| REQ-005 | UI re-rendered after deletion              | TC-003, TC-005, TC-006, TC-008, TC-014, TC-015, TC-016, TC-017, TC-020, TC-021, TC-023 |
| REQ-006 | No changes on cancellation                 | TC-009, TC-010, TC-011 |

---

## Manual-Only Test Cases

The following scenarios are marked `@manual_only` and are excluded from automated Behave runs (tag filter `~@manual_only`):

| TC-ID  | Reason |
|--------|--------|
| TC-012 | Requires direct JS executor invocation via browser console — not a standard UI path |
| TC-024 | Multi-tab testing requires a second browser window not supported by the current single-driver POM setup |

---

## Notes

- All scenarios in this inventory map 1:1 to the test plan entries in `artifacts/COD-8/test-plans/test-plan.md`.
- Every scenario carries `@story_8` and its `@TC-NNN` / `@REQ-NNN` traceability tags in the feature file.
- TC-023 behaviour on reload after delete-all depends on whether the application re-applies seed data; the expected result is intentionally stated as "empty or deterministic seed data" pending clarification (RISK-004 in test plan).
