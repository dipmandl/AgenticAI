# Test Case Review — COD-9: Export Release Notes to JSON File

## Metadata

| Field | Value |
|---|---|
| Story ID | COD-9 |
| Pipeline ID | COD-9-20261103 |
| Review Date | 2026-11-03 |
| Reviewer Agent | test-review-agent (claude-sonnet-4-6[1m]) |
| Total Test Cases Reviewed | 29 |
| Feature Files Reviewed | 2 |
| Artifacts Reviewed | requirement-analysis.md, test-plan.md, test-case-inventory.md, export_release_note.feature, release_notes_stability.feature |

---

## Review Checklist

### Coverage

| # | Check | Result | Notes |
|---|---|---|---|
| C-1 | All acceptance criteria have at least one scenario | PASS | AC-1 → TC-002, TC-003, TC-007, TC-008; AC-2 → TC-004, TC-005, TC-016, TC-019, TC-020; AC-3 → TC-006, TC-009, TC-012, TC-015 |
| C-2 | All test plan scenario IDs are covered | PASS | All 29 plan scenarios (TS-P-001..008, TS-N-001..006, TS-B-001..008, TS-R-001..007) map 1-to-1 to TC-001..TC-029 |
| C-3 | No duplicate scenarios | PASS | TC-006, TC-009, TC-015 share the same precondition (empty localStorage) but assert distinct behaviors: positive content assertion, negative download-not-suppressed assertion, and lower-bound boundary respectively — intentionally distinct |
| C-4 | No scenarios outside defined scope | PASS | All scenarios map to REQ-001 through REQ-005; none address CSV/PDF export, server-side behavior, auth, or other out-of-scope items |
| C-5 | Negative scenarios exist where required | PASS | 6 negative scenarios: TC-009 through TC-014 |
| C-6 | Boundary scenarios exist where required | PASS | 8 boundary scenarios: TC-015 through TC-022; covers zero, one, 100, 1000 records, special chars, Unicode, rapid clicks, storage limit |
| C-7 | Regression scenarios exist where required | PASS | 7 regression scenarios: TC-023 through TC-029; covers list rendering, add, edit, delete, navigation, localStorage writes, console errors |

---

### Gherkin Validity

| # | Check | Result | Notes |
|---|---|---|---|
| G-1 | Gherkin syntax is valid (Feature, Scenario, Background, Given/When/Then/And) | PASS | Both files have Feature header, Background block, and well-formed Scenario blocks with correct keyword ordering |
| G-2 | Steps are concrete and specific | WARN | TC-023 step "the rendering matches the pre-Export-feature baseline" and TC-027 step "navigation behavior matches the pre-Export-feature baseline" are vague — "baseline" is not defined with a concrete expected value or reference dataset |
| G-3 | Background is used only for prerequisites shared by all scenarios in the file | PASS | export_release_note.feature Background: app open + storage key — shared by all 22 scenarios; release_notes_stability.feature Background: app loaded with Export feature present + storage key — shared by all 7 scenarios |

---

### Folder Structure

| # | Check | Result | Notes |
|---|---|---|---|
| F-1 | Feature files are organised by feature area: `features/<feature_area>/<scenario_group>.feature` | WARN | Files are at `product_release_dashboard/manual/json_export/*.feature`. The `json_export` folder is correctly feature-area based, but the path root uses `manual/` rather than the `features/` prefix convention. Not a structural failure, but deviates from the canonical path template. |
| F-2 | No type-based folders present (`features/positive/`, `features/negative/`, etc.) | PASS | No type-based folder names are used; `json_export` is a feature-area name |

---

### Tag Strategy

| # | Check | Result | Notes |
|---|---|---|---|
| T-1 | Every scenario has `@TC-NNN` | PASS | All 29 scenarios carry `@TC-001` through `@TC-029` |
| T-2 | Every scenario has `@REQ-NNN` | PASS | All 29 scenarios carry at least one `@REQ-NNN` tag |
| T-3 | Every scenario has `@story_NNN` | PASS | All 29 scenarios carry `@story_9` in the feature files |
| T-4 | Every scenario has at least one type tag | PASS | TC-001..008: `@positive`; TC-009..014: `@negative`; TC-015..022: `@boundary`; TC-023..029: `@regression` |
| T-5 | Every scenario has at least one scope tag | PASS | TC-001/002/004/005/006/009/015: `@smoke`; all remaining: `@regression` |
| T-6 | Every scenario has at least one priority tag | PASS | All 29 scenarios carry exactly one of `@critical`, `@high`, `@medium`, or `@low` |
| T-7 | No old-style underscore tags (`@tc_001`, `@req_001`) | PASS | All traceability tags use hyphen format: `@TC-NNN`, `@REQ-NNN` |
| T-8 | `@manual_only` scenarios have an inline note explaining why automation is not feasible | WARN | TC-011, TC-013, TC-021, TC-022, TC-029 carry `@manual_only` but the feature files contain no inline comment (e.g., `# Automation note:`) explaining the automation exclusion reason — see Findings section |
| T-9 | Inventory Tags column completeness | WARN | The Tags column in test-case-inventory.md omits `@story_9` from all rows; it is present in the actual feature files but invisible in the inventory table, reducing inventory traceability |

---

### Traceability

| # | Check | Result | Notes |
|---|---|---|---|
| TR-1 | Every TC-NNN maps to at least one REQ-NNN | PASS | All 29 TC-IDs map to at least one REQ; TC-004/007/008/010/011/016/017/018/022 map to two REQs |
| TR-2 | Every REQ-NNN from the requirement artifact is covered by at least one TC-NNN | PASS | REQ-001: TC-001, TC-014; REQ-002: 13 TCs; REQ-003: 10 TCs; REQ-004: TC-006, TC-009, TC-011, TC-012, TC-015; REQ-005: TC-010, TC-013, TC-023–TC-029 |

---

### Artifact Structure

| # | Check | Result | Notes |
|---|---|---|---|
| A-1 | test-case-inventory.md groups scenarios by feature area, not by test type | PASS | Two sections: "json_export — Export Release Note" and "json_export — Release Notes Stability After Export Feature" — both are feature-area labels |
| A-2 | No sections named "Positive Scenarios", "Negative Scenarios", "Boundary Scenarios", etc. | PASS | No type-based section headings exist at the inventory feature-group level; test type breakdown is a summary table only, not a structural grouping |

---

## Findings

### WARN-001 — TC-023, TC-027: Vague assertion steps (Gherkin validity G-2)

- TC-ID: TC-023, TC-027
- Finding type: Gherkin validity — vague step
- File: `release_notes_stability.feature`
- Specific correction required:
  - TC-023 line 17: Replace `And the rendering matches the pre-Export-feature baseline` with a concrete assertion, for example: `And the release notes list displays the same number of cards and card content as before the Export feature was added`
  - TC-027 line 47: Replace `And navigation behavior matches the pre-Export-feature baseline` with: `And each application view loads without JavaScript errors and displays its expected content`

---

### WARN-002 — TC-011, TC-013, TC-021, TC-022, TC-029: @manual_only missing automation exclusion notes (Tag strategy T-8)

- TC-IDs: TC-011, TC-013, TC-021, TC-022, TC-029
- Finding type: Tag strategy — missing `@manual_only` justification comment
- Files: `export_release_note.feature` (TC-011, TC-013, TC-021, TC-022), `release_notes_stability.feature` (TC-029)
- Specific correction required: Add an inline `# Automation note:` comment immediately above each `@manual_only` scenario explaining why it cannot be automated. Suggested notes:
  - TC-011: `# Automation note: browser behavior for corrupted localStorage is undefined in requirements; outcome must be visually confirmed and documented before an assertion can be codified`
  - TC-013: `# Automation note: requires human judgment to verify parity of all existing UI actions against pre-Export behavior; cannot be fully expressed as deterministic assertions without a complete action-by-action baseline spec`
  - TC-021: `# Automation note: rapid-click timing relies on OS scheduler and browser download queue behavior; deterministic assertion on download count is unreliable in headless automation`
  - TC-022: `# Automation note: populating localStorage near the 5 MB limit is environment-dependent; exact limit varies by browser and test environment, making the precondition non-reproducible in CI`
  - TC-029: `# Automation note: browser console error detection requires a live browser devtools session; headless frameworks intercept console output inconsistently across browsers`

---

### WARN-003 — All scenarios: Inventory Tags column omits @story_9 (Tag strategy T-9)

- TC-IDs: TC-001 through TC-029
- Finding type: Inventory completeness — Tags column incomplete
- File: `artifacts/COD-9/test-cases/test-case-inventory.md`
- Specific correction required: Add `@story_9` to the Tags cell of every row in both inventory tables, or add a separate "Story Tag" column. The tag exists in the feature files but is absent from the inventory table, making inventory-level story ownership non-auditable without opening feature files.

---

### WARN-004 — Feature file path deviates from `features/<feature_area>/<scenario_group>.feature` convention (Folder structure F-1)

- TC-IDs: All 29
- Finding type: Folder structure — path convention deviation
- Current path: `product_release_dashboard/manual/json_export/*.feature`
- Expected path pattern: `features/json_export/*.feature`
- Specific correction required: If the project adopts the standard pipeline path convention, move files to `product_release_dashboard/features/json_export/export_release_note.feature` and `product_release_dashboard/features/json_export/release_notes_stability.feature` and update the inventory file paths accordingly. This is a WARN, not a FAIL, because the folder name `json_export` is feature-area based (not type-based) and no type-based folder names are present.

---

## No-Weakened-Assertion Verification

All 29 scenarios were checked for weakened or skipped validations:

- TC-011: "does not throw an unhandled JavaScript exception visible to the user AND the downloaded file either contains '[]' or is otherwise handled gracefully" — the disjunctive assertion ("or is otherwise handled gracefully") is intentional given undefined corrupted-localStorage behavior documented in RISK-006 of the test plan; not a weakened assertion but a reflection of an unspecified requirement. The scenario is correctly tagged `@manual_only`.
- All other scenarios carry specific, verifiable assertions. No assertion was found to be weakened or replaced with a no-op. PASS.

---

## Summary

| Metric | Value |
|---|---|
| Total test cases reviewed | 29 |
| Feature files reviewed | 2 |
| Checklist items evaluated | 19 |
| PASS | 15 |
| FAIL | 0 |
| WARN | 4 (covering 8 individual scenario-level findings) |
| Acceptance criteria covered | 3 / 3 |
| Test plan scenario IDs covered | 29 / 29 |
| REQs covered | 5 / 5 |

**Recommended action: APPROVE**

The test case set is complete, correctly structured, and free of blocking defects. All acceptance criteria, test plan scenarios, and requirements are fully traced. The four warnings are minor quality improvements (vague baseline assertions in two regression scenarios, missing @manual_only justification comments, incomplete Tags column in the inventory) and do not block progression to framework selection. Warnings WARN-001 and WARN-002 should be resolved before the automation phase begins so that the @manual_only rationale is on record and the two vague regression assertions are made concrete.

---

**Review Version:** 1.0
**Completed:** 2026-11-03T00:30:00Z
**Next Phase:** framework_selection
