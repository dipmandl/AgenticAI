# Traceability Matrix: COD-7 — Edit Existing Release Note

**Story**: COD-7
**Framework**: Playwright (TypeScript)
**Total TCs**: 51 | **Automated**: 46 | **Manual Only**: 5

| TC-ID | REQ-ID | Scenario | Automation File | Status |
|-------|--------|----------|-----------------|--------|
| TC-001 | REQ-001 | Edit button is visible on every rendered release card | tests/positive/edit-positive.spec.ts | AUTOMATED |
| TC-002 | REQ-002 | Clicking Edit pre-fills all 7 form fields with the release data | tests/positive/edit-positive.spec.ts | AUTOMATED |
| TC-003 | REQ-002 | isBreaking checkbox pre-fills as checked for a breaking release | tests/positive/edit-positive.spec.ts | AUTOMATED |
| TC-004 | REQ-002 | isBreaking checkbox pre-fills as unchecked for a non-breaking release | tests/positive/edit-positive.spec.ts | AUTOMATED |
| TC-005 | REQ-004 | Submit button label changes to "Update Release Note" in edit mode | tests/positive/edit-positive.spec.ts | AUTOMATED |
| TC-006 | REQ-005 | Cancel Edit button becomes visible when edit mode is active | tests/positive/edit-positive.spec.ts | AUTOMATED |
| TC-007 | REQ-006 | Save updates the specific release by its id | tests/positive/edit-positive.spec.ts | AUTOMATED |
| TC-008 | REQ-006 | Save does not create a duplicate entry | tests/positive/edit-positive.spec.ts | AUTOMATED |
| TC-009 | REQ-006 | Save does not modify any other release entries | tests/positive/edit-positive.spec.ts | AUTOMATED |
| TC-010 | REQ-007 | Updated release is persisted to localStorage after Save | tests/positive/edit-positive.spec.ts | AUTOMATED |
| TC-011 | REQ-008 | Release list re-renders immediately with updated values after Save | tests/positive/edit-positive.spec.ts | AUTOMATED |
| TC-012 | REQ-009 | Cancel discards in-progress changes; rendered list unchanged | tests/positive/edit-positive.spec.ts | AUTOMATED |
| TC-013 | REQ-009 | Cancel leaves localStorage unchanged | tests/positive/edit-positive.spec.ts | AUTOMATED |
| TC-014 | REQ-010 | All active filters remain applied after Save | tests/positive/edit-positive.spec.ts | AUTOMATED |
| TC-015 | REQ-011 | All active filters remain applied after Cancel | tests/positive/edit-positive.spec.ts | AUTOMATED |
| TC-016 | REQ-012 | Edit operates correctly on the first card in the list | tests/positive/edit-positive.spec.ts | AUTOMATED |
| TC-017 | REQ-012 | Edit operates correctly on the last card in the list | tests/positive/edit-positive.spec.ts | AUTOMATED |
| TC-018 | REQ-012 | Edit operates correctly on a middle card in the list | tests/positive/edit-positive.spec.ts | AUTOMATED |
| TC-019 | REQ-009 | Cancel without modifying any field leaves list and localStorage unchanged | tests/negative/edit-negative.spec.ts | AUTOMATED |
| TC-020 | REQ-004 | Save with teamName cleared shows validation error and preserves edit state | tests/negative/edit-negative.spec.ts | AUTOMATED |
| TC-021 | REQ-004 | Save with title cleared shows validation error | tests/negative/edit-negative.spec.ts | AUTOMATED |
| TC-022 | REQ-004 | Save with product cleared shows validation error | tests/negative/edit-negative.spec.ts | AUTOMATED |
| TC-023 | REQ-004 | Save with version cleared shows validation error | tests/negative/edit-negative.spec.ts | AUTOMATED |
| TC-024 | REQ-004 | Save with releaseDate cleared shows validation error | tests/negative/edit-negative.spec.ts | AUTOMATED |
| TC-025 | REQ-006 | Calling startEdit with a non-existent id does not crash the application | tests/negative/edit-negative.spec.ts | SKIPPED (manual_only) |
| TC-026 | REQ-002 | Clicking Edit on card B while card A is in edit mode replaces form with card B values | tests/negative/edit-negative.spec.ts | AUTOMATED |
| TC-027 | REQ-005, REQ-009 | Cancel after a validation failure exits edit mode cleanly | tests/negative/edit-negative.spec.ts | AUTOMATED |
| TC-028 | REQ-002, REQ-006 | Edit all 7 fields then Save persists every change | tests/boundary/edit-boundary.spec.ts | AUTOMATED |
| TC-029 | REQ-006 | Edit exactly one field; all others remain intact | tests/boundary/edit-boundary.spec.ts | AUTOMATED |
| TC-030 | REQ-002, REQ-003 | Edit with teamName cleared shows validation error; does not save | tests/boundary/edit-boundary.spec.ts | AUTOMATED |
| TC-031 | REQ-002, REQ-006 | Edit with minimum single-character values in all mandatory fields succeeds | tests/boundary/edit-boundary.spec.ts | AUTOMATED |
| TC-032 | REQ-002, REQ-009 | Edit then Cancel then re-Edit same card shows original unchanged values | tests/boundary/edit-boundary.spec.ts | AUTOMATED |
| TC-033 | REQ-002 | Edit card A then Cancel then Edit card B shows only card B values | tests/boundary/edit-boundary.spec.ts | AUTOMATED |
| TC-034 | REQ-003 | Edit title and description with 500-character text does not crash | tests/boundary/edit-boundary.spec.ts | SKIPPED (manual_only) |
| TC-035 | REQ-003 | Edit text fields with special characters are stored and rendered safely | tests/boundary/edit-boundary.spec.ts | SKIPPED (manual_only) |
| TC-036 | REQ-002, REQ-006 | Toggle isBreaking from true to false and Save persists the change | tests/boundary/edit-boundary.spec.ts | AUTOMATED |
| TC-037 | REQ-002, REQ-006 | Toggle isBreaking from false to true and Save persists the change | tests/boundary/edit-boundary.spec.ts | AUTOMATED |
| TC-038 | REQ-012 | Edit operates correctly when the list contains exactly one entry | tests/boundary/edit-boundary.spec.ts | AUTOMATED |
| TC-039 | REQ-010 | Edit with no filters active leaves filter controls cleared after Save | tests/boundary/edit-boundary.spec.ts | AUTOMATED |
| TC-040 | REQ-006 | Create new release still works after Edit and Save | tests/regression/edit-regression.spec.ts | AUTOMATED |
| TC-041 | REQ-009 | Create new release still works after Edit and Cancel | tests/regression/edit-regression.spec.ts | AUTOMATED |
| TC-042 | REQ-006 | Delete a different release still works after Edit and Save | tests/regression/edit-regression.spec.ts | AUTOMATED |
| TC-043 | REQ-009 | Deleting the release currently in edit mode resets edit state | tests/regression/edit-regression.spec.ts | AUTOMATED |
| TC-044 | REQ-010 | Product filter functions correctly before and after Edit and Save | tests/regression/edit-regression.spec.ts | AUTOMATED |
| TC-045 | REQ-010 | Breaking-change filter functions correctly after Edit and Save | tests/regression/edit-regression.spec.ts | AUTOMATED |
| TC-046 | REQ-010 | Keyword search filter functions correctly after Edit and Save | tests/regression/edit-regression.spec.ts | AUTOMATED |
| TC-047 | REQ-010 | Multi-filter combination persists correctly after Edit and Save | tests/regression/edit-regression.spec.ts | AUTOMATED |
| TC-048 | REQ-007 | Edited values persist after a full page reload | tests/regression/edit-regression.spec.ts | AUTOMATED |
| TC-049 | REQ-007 | Export CSV contains updated values after Edit and Save | tests/regression/edit-regression.spec.ts | SKIPPED (manual_only) |
| TC-050 | REQ-009 | Importing JSON while in edit mode resets edit state | tests/regression/edit-regression.spec.ts | SKIPPED (manual_only) |
| TC-051 | REQ-006 | Form in create mode creates a new entry and does not trigger an update | tests/regression/edit-regression.spec.ts | AUTOMATED |
