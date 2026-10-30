# Test Case Inventory: COD-7 — Edit Existing Release Note

**Story**: COD-7  
**Feature File**: `product_release_dashboard/manual/release_notes/edit_release_note.feature`  
**Total Test Cases**: 51

---

## Feature: release_notes / edit_release_note

| TC-ID  | Tags                                              | Scenario Title                                                                      | Feature File |
|--------|---------------------------------------------------|-------------------------------------------------------------------------------------|--------------|
| TC-001 | @positive @high @functional @ui                   | Edit button is visible on every rendered release card                               | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-002 | @positive @critical @functional @ui               | Clicking Edit pre-fills all 7 form fields with the release data                     | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-003 | @positive @high @functional @ui                   | isBreaking checkbox pre-fills as checked for a breaking release                     | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-004 | @positive @high @functional @ui                   | isBreaking checkbox pre-fills as unchecked for a non-breaking release               | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-005 | @positive @high @functional @ui                   | Submit button label changes to "Update Release Note" in edit mode                   | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-006 | @positive @high @functional @ui                   | Cancel Edit button becomes visible when edit mode is active                         | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-007 | @positive @critical @functional @ui               | Save updates the specific release by its id                                         | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-008 | @positive @critical @functional @ui               | Save does not create a duplicate entry                                              | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-009 | @positive @high @functional @ui                   | Save does not modify any other release entries                                      | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-010 | @positive @critical @functional @ui               | Updated release is persisted to localStorage after Save                             | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-011 | @positive @high @functional @ui                   | Release list re-renders immediately with updated values after Save                  | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-012 | @positive @critical @functional @ui               | Cancel discards in-progress changes and the rendered list is unchanged              | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-013 | @positive @high @functional @ui                   | Cancel leaves localStorage unchanged                                                | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-014 | @positive @critical @functional @ui               | All active filters remain applied after Save                                        | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-015 | @positive @high @functional @ui                   | All active filters remain applied after Cancel                                      | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-016 | @positive @medium @functional @ui                 | Edit operates correctly on the first card in the list                               | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-017 | @positive @medium @functional @ui                 | Edit operates correctly on the last card in the list                                | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-018 | @positive @medium @functional @ui                 | Edit operates correctly on a middle card in the list                                | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-019 | @negative @high @functional @ui                   | Cancel without modifying any field leaves list and localStorage unchanged            | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-020 | @negative @high @functional @ui                   | Save with teamName cleared shows validation error and preserves edit state           | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-021 | @negative @high @functional @ui                   | Save with title cleared shows validation error                                      | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-022 | @negative @high @functional @ui                   | Save with product cleared shows validation error                                    | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-023 | @negative @high @functional @ui                   | Save with version cleared shows validation error                                    | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-024 | @negative @high @functional @ui                   | Save with releaseDate cleared shows validation error                                | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-025 | @negative @high @functional @manual_only          | Calling startEdit with a non-existent id does not crash the application             | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-026 | @negative @medium @functional @ui                 | Clicking Edit on card B while card A is in edit mode replaces form with card B      | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-027 | @negative @high @functional @ui                   | Cancel after a validation failure exits edit mode cleanly                           | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-028 | @boundary @high @functional @ui                   | Edit with all 7 fields modified then Save persists every change                     | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-029 | @boundary @medium @functional @ui                 | Edit with exactly one field changed leaves all other fields intact                  | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-030 | @boundary @medium @functional @ui                 | Edit with teamName cleared to empty — outcome observed and recorded per AMB-001     | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-031 | @boundary @medium @functional @ui                 | Edit with minimum single-character values in all mandatory fields succeeds          | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-032 | @boundary @high @functional @ui                   | Edit then Cancel then re-Edit same card shows original unchanged values             | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-033 | @boundary @high @functional @ui                   | Edit card A then Cancel then Edit card B shows only card B's values                 | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-034 | @boundary @low @functional @ui @manual_only       | Edit title and description with 500-character text does not crash the application   | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-035 | @boundary @low @functional @ui @manual_only       | Edit text fields with special characters are stored and rendered safely             | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-036 | @boundary @high @functional @ui                   | Toggle isBreaking from true to false and Save persists the change                   | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-037 | @boundary @high @functional @ui                   | Toggle isBreaking from false to true and Save persists the change                   | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-038 | @boundary @medium @functional @ui                 | Edit operates correctly when the list contains exactly one entry                    | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-039 | @boundary @medium @functional @ui                 | Edit with no filters active leaves all filter controls cleared after Save           | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-040 | @regression @high @functional @ui                 | Create new release still works after Edit and Save                                  | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-041 | @regression @high @functional @ui                 | Create new release still works after Edit and Cancel                                | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-042 | @regression @high @functional @ui                 | Delete a different release still works after Edit and Save                          | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-043 | @regression @high @functional @ui                 | Deleting the release currently in edit mode resets edit state                       | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-044 | @regression @high @functional @ui                 | Product filter functions correctly before and after Edit and Save                   | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-045 | @regression @high @functional @ui                 | Breaking-change filter functions correctly after Edit and Save                      | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-046 | @regression @high @functional @ui                 | Keyword search filter functions correctly after Edit and Save                       | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-047 | @regression @high @functional @ui                 | Multi-filter combination persists correctly after Edit and Save                     | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-048 | @regression @high @functional @ui                 | Edited values persist after a full page reload                                      | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-049 | @regression @medium @functional @ui @manual_only  | Export CSV contains updated values after Edit and Save                              | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-050 | @regression @medium @functional @ui @manual_only  | Importing JSON while in edit mode resets edit state                                 | product_release_dashboard/manual/release_notes/edit_release_note.feature |
| TC-051 | @regression @high @functional @ui                 | Form in create mode creates a new entry and does not trigger an update              | product_release_dashboard/manual/release_notes/edit_release_note.feature |
