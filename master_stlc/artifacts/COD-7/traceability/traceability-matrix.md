# Traceability Matrix

## Metadata

| Field | Value |
|---|---|
| Story ID | COD-7 |
| Story Title | Edit an existing release note |
| Generated | 2026-11-03 |
| Total TCs | 42 |
| Automated | 39 |
| Manual | 3 |

---

## Matrix

| TC ID | Requirement(s) | Test File | Test Title | Status |
|-------|----------------|-----------|------------|--------|
| TC-001 | REQ-001, REQ-002, REQ-003, REQ-004, AC-1 | tests/edit_release_notes/positive.spec.ts | Edit button present and triggers form pre-fill | AUTOMATED |
| TC-002 | REQ-005, REQ-006, REQ-007, AC-2 | tests/edit_release_notes/positive.spec.ts | Save after modifying product field updates localStorage | AUTOMATED |
| TC-003 | REQ-005, REQ-006, REQ-007, AC-2 | tests/edit_release_notes/positive.spec.ts | Save after modifying version field updates localStorage | AUTOMATED |
| TC-004 | REQ-003, REQ-005, REQ-006, AC-2 | tests/edit_release_notes/positive.spec.ts | Save after modifying title and description updates both fields | AUTOMATED |
| TC-005 | REQ-003, REQ-005, REQ-006, AC-2 | tests/edit_release_notes/positive.spec.ts | Save after modifying releaseDate updates date in localStorage | AUTOMATED |
| TC-006 | REQ-003, REQ-005, REQ-006, AC-2 | tests/edit_release_notes/positive.spec.ts | Save after modifying teamName updates teamName in localStorage | AUTOMATED |
| TC-007 | REQ-003, REQ-005, REQ-006, AC-2 | tests/edit_release_notes/positive.spec.ts | Save with breaking flag toggled from false to true | AUTOMATED |
| TC-008 | REQ-003, REQ-005, REQ-006, AC-2 | tests/edit_release_notes/positive.spec.ts | Save with breaking flag toggled from true to false | AUTOMATED |
| TC-009 | REQ-003, REQ-005, REQ-006, REQ-007, AC-2 | tests/edit_release_notes/positive.spec.ts | Save after modifying all editable fields; id remains unchanged | AUTOMATED |
| TC-010 | REQ-008, AC-3 | tests/edit_release_notes/positive.spec.ts | Cancel after modifying fields discards all changes | AUTOMATED |
| TC-011 | REQ-004 | tests/edit_release_notes/positive.spec.ts | Form returns to create mode after Save | AUTOMATED |
| TC-012 | REQ-004 | tests/edit_release_notes/positive.spec.ts | Form returns to create mode after Cancel | AUTOMATED |
| TC-013 | REQ-009, AC-4, NFR-004 | tests/edit_release_notes/positive.spec.ts | Active product filter persists after Save | AUTOMATED |
| TC-014 | REQ-009, AC-4, NFR-004 | tests/edit_release_notes/positive.spec.ts | Active search filter persists after Cancel | AUTOMATED |
| TC-015 | N-001, REQ-003 | tests/edit_release_notes/negative.spec.ts | Save blocked when required field product is cleared | AUTOMATED |
| TC-016 | N-001, REQ-003 | tests/edit_release_notes/negative.spec.ts | Save blocked when required field version is cleared | AUTOMATED |
| TC-017 | N-001, REQ-003 | tests/edit_release_notes/negative.spec.ts | Save blocked when required field title is cleared | AUTOMATED |
| TC-018 | N-001, REQ-003 | tests/edit_release_notes/negative.spec.ts | Save blocked when required field description is cleared | AUTOMATED |
| TC-019 | N-001, REQ-003 | tests/edit_release_notes/negative.spec.ts | Save blocked when required field releaseDate is cleared | AUTOMATED |
| TC-020 | N-001, REQ-003 | tests/edit_release_notes/negative.spec.ts | Save blocked with custom error when teamName is cleared | AUTOMATED |
| TC-021 | N-002 | tests/edit_release_notes/negative.spec.ts | Save without modifying any field succeeds and preserves data | AUTOMATED |
| TC-022 | N-005, NFR-003 | — | localStorage full on Save — silent failure | MANUAL |
| TC-023 | B-001, REQ-007 | tests/edit_release_notes/boundary.spec.ts | Edit the only release note in the list | AUTOMATED |
| TC-024 | B-002, REQ-007 | tests/edit_release_notes/boundary.spec.ts | Edit with no active filters applied | AUTOMATED |
| TC-025 | B-003, REQ-007, REQ-009, AC-4 | tests/edit_release_notes/boundary.spec.ts | Edited entry disappears when it no longer matches active product filter | AUTOMATED |
| TC-026 | B-004, REQ-003, AC-1 | tests/edit_release_notes/boundary.spec.ts | Edit entry with isBreaking=true — checkbox pre-fills as checked | AUTOMATED |
| TC-027 | B-005, REQ-003, AC-1 | tests/edit_release_notes/boundary.spec.ts | Edit entry with releaseDate "1970-01-01" — date pre-fills correctly | AUTOMATED |
| TC-028 | B-005, REQ-003, AC-1 | tests/edit_release_notes/boundary.spec.ts | Edit entry with releaseDate = today's date — date pre-fills correctly | AUTOMATED |
| TC-029 | AC-4, REQ-009, NFR-004 | tests/edit_release_notes/boundary.spec.ts | All three filters active simultaneously — all persist after Save | AUTOMATED |
| TC-030 | B-006 | — | Edit one entry from a 100-entry dataset — no visible performance lag | MANUAL |
| TC-031 | NFR-003 | tests/edit_release_notes/regression.spec.ts | Create → Edit → Create: second create adds new entry with blank form | AUTOMATED |
| TC-032 | NFR-003 | tests/edit_release_notes/regression.spec.ts | Edit → Save → Delete: delete removes correct entry and list re-renders | AUTOMATED |
| TC-033 | NFR-003 | tests/edit_release_notes/regression.spec.ts | Edit → Save → Export: CSV export reflects updated values | AUTOMATED |
| TC-034 | NFR-003 | tests/edit_release_notes/regression.spec.ts | Edit → Cancel → Create: create form is blank and adds new entry | AUTOMATED |
| TC-035 | REQ-005, NFR-003 | tests/edit_release_notes/regression.spec.ts | Edit one entry — all other entries remain unchanged in localStorage | AUTOMATED |
| TC-036 | NFR-003 | tests/edit_release_notes/regression.spec.ts | Edit product value — product filter returns correct results afterward | AUTOMATED |
| TC-037 | REQ-002, REQ-003, AC-1 | tests/edit_release_notes/regression.spec.ts | Edit same entry twice — second edit pre-fills values from first save | AUTOMATED |
| TC-038 | NFR-003 | tests/edit_release_notes/regression.spec.ts | Seed data: edit one seed record — other seed record unchanged | AUTOMATED |
| TC-039 | NFR-003 | tests/edit_release_notes/regression.spec.ts | Edit entry to isBreaking=true — breaking filter shows it correctly | AUTOMATED |
| TC-040 | NFR-003 | tests/edit_release_notes/regression.spec.ts | Edit title to include search keyword — search returns updated entry | AUTOMATED |
| TC-041 | REQ-005, REQ-006 | tests/edit_release_notes/regression.spec.ts | Two sequential edits on different entries — both updated independently | AUTOMATED |
| TC-042 | NFR-003 | — | Edit → Save → Import CSV: import proceeds without crash | MANUAL |

---

## Summary

| Status | Count |
|--------|-------|
| AUTOMATED | 39 |
| MANUAL | 3 |
| **Total** | **42** |

## Manual-Only Cases

| TC ID | Reason |
|-------|--------|
| TC-022 | Filling localStorage to browser quota is unsafe to automate reliably |
| TC-030 | Performance judgment (visible rendering lag) requires human observation |
| TC-042 | CSV import involves `window.confirm` and OS-level file picker interaction |
