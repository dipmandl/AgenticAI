# Test Review: COD-7 — Edit Existing Release Note

**Reviewer**: Test Review Agent  
**Review Date**: 2026-10-30  
**Artifacts Reviewed**:
- `artifacts/COD-7/manual-tests/test-cases.md` (primary)
- `product_release_dashboard/manual/release_notes/edit_release_note.feature`
- `artifacts/COD-7/test-cases/test-case-inventory.md`
- `artifacts/COD-7/requirements/requirement-analysis.md`
- `artifacts/COD-7/test-plans/test-plan.md`

---

## Review Summary

| Metric | Value |
|---|---|
| Total test cases reviewed | 51 (TC-001 to TC-051) |
| PASS items | 33 |
| FAIL items | 3 |
| WARN items | 4 |
| Critical scenarios present | 6 / 6 |
| AC coverage | 4 / 4 |
| REQ coverage | 12 / 12 |
| Test plan scenario coverage | 51 / 51 (note: test-plan metadata says 48 — counted 51 in body) |
| **Verdict** | **APPROVED_WITH_AMENDMENTS** |

---

## Coverage Matrix

### Acceptance Criteria → TC Mapping

| AC | Description | Covering TCs | Status |
|---|---|---|---|
| AC-1 | Edit opens release pre-filled | TC-002, TC-003, TC-004, TC-026, TC-028, TC-032, TC-033, TC-036, TC-037 | PASS |
| AC-2 | Save updates by id in localStorage | TC-007, TC-008, TC-009, TC-010, TC-011, TC-028, TC-029, TC-040, TC-042, TC-048, TC-049, TC-051 | PASS |
| AC-3 | Cancel discards changes | TC-012, TC-013, TC-019, TC-027, TC-032, TC-041, TC-043, TC-050 | PASS |
| AC-4 | Filters remain applied after Save/Cancel | TC-014, TC-015, TC-039, TC-044, TC-045, TC-046, TC-047 | PASS |

### Requirements → TC Mapping

| REQ | Description (abbrev.) | Covering TCs | Status |
|---|---|---|---|
| REQ-001 | Edit button on every card | TC-001 | PASS |
| REQ-002 | Clicking Edit pre-fills all 7 fields | TC-002 – TC-004, TC-026, TC-028, TC-030 – TC-033, TC-036, TC-037 | PASS |
| REQ-003 | All pre-filled fields are editable | TC-030 (traceability), TC-034, TC-035 | PASS |
| REQ-004 | Save action available | TC-005, TC-020 – TC-024 | PASS |
| REQ-005 | Cancel action available | TC-006, TC-027 | PASS |
| REQ-006 | Save updates by id; no new/modified entries | TC-007 – TC-009, TC-025, TC-028, TC-029, TC-031, TC-036, TC-037, TC-040, TC-042, TC-051 | PASS |
| REQ-007 | Save persists to localStorage | TC-010, TC-048, TC-049 | PASS |
| REQ-008 | List re-renders after Save | TC-011 | PASS |
| REQ-009 | Cancel leaves list/localStorage unchanged | TC-012, TC-013, TC-019, TC-027, TC-032, TC-041, TC-043, TC-050 | PASS |
| REQ-010 | Filters remain after Save | TC-014, TC-039, TC-044 – TC-047 | PASS |
| REQ-011 | Filters remain after Cancel | TC-015 | PASS |
| REQ-012 | Edit works at any list position | TC-016 – TC-018, TC-038 | PASS |

---

## Findings

### F-001 — FAIL | TC-030 | Weakened assertion: no binary pass/fail outcome

**Severity**: FAIL  
**Affected TC**: TC-030 (TS-B-003)  
**Location**: `test-cases.md` lines 346-350; `edit_release_note.feature` lines 292-294

**Description**: The Then block reads:
```
Then the tester records whether Save is blocked with a validation error OR succeeds with empty teamName
And the actual outcome is documented against AMB-001 resolution
```
This step accepts both a pass and a fail outcome with the conjunction "OR". It is an observation directive, not a testable assertion. A test case must have a deterministic expected result; a dual-outcome step makes it impossible to produce a PASS or FAIL verdict. AMB-001 is flagged as unresolved in the test plan, but the correct response is to park the test case (mark it `@pending`) rather than write an assertion that can never fail.

**Recommendation**: Replace the Then block with:
```gherkin
# AMB-001 PENDING — expected result to be confirmed before execution
# If teamName is required: Then a validation error is displayed and the form remains in edit mode
# If teamName is optional: Then the release card shows an empty team name and localStorage is updated
```
Until AMB-001 is resolved, add tag `@pending @manual_only` and document the expected result clearly as one of the two alternatives above. Remove the "OR" construction from any Then step.

---

### F-002 — FAIL | TC-027, TC-028, TC-030, TC-031, TC-032, TC-036, TC-037 | Missing secondary @REQ tags

**Severity**: FAIL  
**Affected TCs**: 7 test cases  
**Location**: Both `test-cases.md` and `edit_release_note.feature`

**Description**: The traceability summary table at the end of `test-cases.md` correctly maps each TC to multiple REQs. The Gherkin scenario tags in both files only carry one @REQ tag each, omitting the secondary REQs. This breaks automated traceability queries that filter by tag.

| TC | Declared REQs (table) | Tagged REQs (Gherkin) | Missing Tag |
|---|---|---|---|
| TC-027 | REQ-005, REQ-009 | @REQ-005 | @REQ-009 |
| TC-028 | REQ-002, REQ-006 | @REQ-002 | @REQ-006 |
| TC-030 | REQ-002, REQ-003 | @REQ-002 | @REQ-003 |
| TC-031 | REQ-002, REQ-006 | @REQ-002 | @REQ-006 |
| TC-032 | REQ-002, REQ-009 | @REQ-002 | @REQ-009 |
| TC-036 | REQ-002, REQ-006 | @REQ-002 | @REQ-006 |
| TC-037 | REQ-002, REQ-006 | @REQ-002 | @REQ-006 |

**Recommendation**: Add the missing @REQ-NNN tags to the scenario tag line in both `edit_release_note.feature` and the Gherkin blocks in `test-cases.md`. For example, TC-027 tag line should read:
```
@TC-027 @REQ-005 @REQ-009 @story_COD-7 @negative @high @functional @ui
```

---

### F-003 — FAIL | TC-001 to TC-039 | Missing scope tags (@smoke / @sanity)

**Severity**: FAIL  
**Affected TCs**: TC-001 through TC-039 (39 of 51 scenarios)

**Description**: The STLC tag strategy requires every scenario to carry at least one scope tag: `@smoke`, `@regression`, or `@sanity`. TC-040 to TC-051 carry `@regression`. TC-001 to TC-039 carry only type and priority tags with no scope tag. This means filter-by-scope execution (e.g., `--tags @regression`) will silently exclude 39 test cases.

The test plan explicitly excludes smoke testing for this story. However, the 6 CRITICAL scenarios (TC-002, TC-007, TC-008, TC-010, TC-012, TC-014) and high-priority ACs should carry at minimum a `@sanity` or `@regression` scope tag.

**Recommendation**: Add `@sanity` to all CRITICAL and HIGH priority non-regression scenarios (TC-001 to TC-039). As an alternative strategy, add `@regression` to all scenarios (positive, negative, boundary, regression) since this story is entirely a regression-eligible functional feature. The simpler rule: add `@regression` to TC-001 through TC-039.

---

### W-001 — WARN | TC-034 | Observational step is not a hard assertion

**Severity**: WARN  
**Affected TC**: TC-034 (TS-B-007)  
**Location**: `test-cases.md` lines 396-398; `edit_release_note.feature` lines 336-339

**Description**: The second Then step reads:
```
And the tester records whether the text is saved as-is or truncated with a visible message
```
This is an observation instruction, not a pass/fail assertion. The first and third Then steps are hard assertions (no crash; no JSON parse errors), so the scenario is not fully broken, but the middle step contributes no automatable exit criterion.

**Recommendation**: Change to a conditional hard assertion with a note:
```gherkin
# Expected: text is saved as-is (no max-length defined — see test plan MISSING item)
And the release card title displays the full 500-character string without truncation
```
Or, if truncation is possible, split this into two mutually exclusive scenarios once the maximum-length constraint is specified.

---

### W-002 — WARN | TC-040, TC-041, TC-044, TC-045, TC-046, TC-048, TC-049 | Compound multi-action When steps

**Severity**: WARN  
**Affected TCs**: 7 regression scenarios

**Description**: Several regression scenario When steps combine multiple user actions into a single step using comma-separated clauses:
```
When the user clicks "Edit" on "Billing API v1.4.0", changes title to "Edited Billing Title", and clicks "Update Release Note"
```
This violates the single-responsibility principle for Gherkin steps, makes the step definition unusable for reuse, and reduces failure localization (a tester cannot determine which sub-action failed).

TC-041 additionally uses a vague modifier: "changes a field value" — this does not specify which field or to what value, making the step non-reproducible.

**Recommendation**: Decompose each compound step into discrete atomic steps. For example:
```gherkin
When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
And the user clears "#title-input" and types "Edited Billing Title"
And the user clicks "Update Release Note"
```

---

### W-003 — WARN | TC-026, TC-043 | Assertion (Then) logic placed inside When block

**Severity**: WARN  
**Affected TCs**: TC-026, TC-043

**Description**:
- TC-026 (line 282-285 in `edit_release_note.feature`): `And the form is pre-filled with "Billing API" values` appears inside the When block. This is a verification of state, which belongs in a Given (precondition) or an intermediate Then.
- TC-043 (line 429): `And the form is pre-filled with "Billing API v1.4.0" values` similarly appears in the When block after the action step.

Placing state-verification steps inside When breaks the Given/When/Then contract and can obscure which step boundary a failure crosses.

**Recommendation**: Move these verification steps to Given (as a precondition assertion) or restructure the step as `Given the form has been pre-filled` to indicate it is a setup validation.

---

### W-004 — WARN | TC-025, TC-034, TC-035, TC-049, TC-050 | @manual_only scenarios lack automation-exclusion rationale

**Severity**: WARN  
**Affected TCs**: TC-025, TC-034, TC-035, TC-049, TC-050

**Description**: All five `@manual_only` scenarios lack an inline comment or note explaining why the scenario cannot or should not be automated. Per the tag strategy, a WARN is issued when this note is absent.

- TC-025: Requires direct JS console call — automatable with DevTools Protocol or Playwright evaluate(); the `@manual_only` classification needs justification.
- TC-034: Pasting long text is fully automatable; `@manual_only` appears incorrect.
- TC-035: Special character input is fully automatable; `@manual_only` appears incorrect.
- TC-049: CSV download inspection is automatable; `@manual_only` appears incorrect.
- TC-050: JSON import dialog is automatable; `@manual_only` appears incorrect.

**Recommendation**: Either remove `@manual_only` from TC-034, TC-035, TC-049, TC-050 (they are automatable), or add a `# Manual only: <reason>` comment above each scenario tag line. For TC-025, document why DevTools console invocation is preferred over a programmatic automation approach.

---

## Critical Scenario Verification

| TC | Title | Present | Priority Tag | REQ Tag | TS-ID Mapped |
|---|---|---|---|---|---|
| TC-002 | Clicking Edit pre-fills all 7 form fields | YES | @critical | @REQ-002 | TS-P-002 |
| TC-007 | Save updates the specific release by its id | YES | @critical | @REQ-006 | TS-P-007 |
| TC-008 | Save does not create a duplicate entry | YES | @critical | @REQ-006 | TS-P-008 |
| TC-010 | Updated release is persisted to localStorage after Save | YES | @critical | @REQ-007 | TS-P-010 |
| TC-012 | Cancel discards in-progress changes | YES | @critical | @REQ-009 | TS-P-012 |
| TC-014 | All active filters remain applied after Save | YES | @critical | @REQ-010 | TS-P-014 |

All 6 mandated critical scenarios are present, correctly tagged @critical, carry the right REQ tag, and map to the correct TS-* plan scenario. **PASS.**

---

## Additional Observations (non-blocking)

1. **Test plan metadata count error**: `test-plan.md` Artifact Metadata section states "Total Scenarios: 48" but the body contains 51 enumerated scenarios (TS-P-001–018 = 18, TS-N-001–009 = 9, TS-B-001–012 = 12, TS-R-001–012 = 12; total = 51). The test cases correctly produce 51 TCs. This is a test-plan copy-edit error only; no correction required in test cases.

2. **Background state conflict in TC-038**: The feature file has a single Background that seeds 2 releases. TC-038 immediately overrides this with `Given localStorage "releaseNotesDashboard.releases" is set to contain exactly one release`. In automated execution this would work, but in manual execution the tester must know to clear the Background-seeded state first. Consider adding a Background-clear note to the step.

3. **Feature block naming in test-cases.md**: The markdown documentation in `test-cases.md` groups Gherkin blocks under section headings "Feature: Edit Release Note (Positive)", "(Negative)", "(Boundary)", "(Regression)". These headings are markdown prose, not actual Gherkin Feature declarations. The actual feature file correctly uses a single `Feature: Edit Release Note` declaration. No action required; the documentation grouping is for human readability.

4. **TC-027 alignment with test plan**: The test plan's requirement mapping lists REQ-005 and REQ-009 for TS-N-009 (TC-027). The Gherkin only tags @REQ-005. This is subsumed under F-002 above.

---

## Recommended Amendments

### Mandatory (address before marking APPROVED)

1. **TC-030**: Replace the dual-outcome "OR" Then assertion with a single definitive expected result, or park the test with `@pending` and a clear note referencing AMB-001. The current step makes test execution verdict impossible to determine.

2. **TC-027, TC-028, TC-030, TC-031, TC-032, TC-036, TC-037**: Add missing secondary @REQ tags to scenario tag lines in both `edit_release_note.feature` and `test-cases.md` Gherkin blocks. Exact tags listed in F-002.

3. **TC-001 to TC-039**: Add `@regression` (or `@sanity` for the 6 CRITICAL scenarios) scope tag to all 39 scenarios that currently lack a scope tag.

### Optional (improve quality, not blockers)

4. **TC-034**: Replace observational "records whether" step with a definitive assertion once max-length constraint is known.

5. **TC-040, TC-041, TC-044, TC-045, TC-046, TC-048, TC-049**: Decompose compound multi-action When steps into atomic steps.

6. **TC-026, TC-043**: Move state-verification And steps out of the When block into Given.

7. **TC-025, TC-034, TC-035, TC-049, TC-050**: Evaluate whether `@manual_only` is correct; add inline rationale comment if it is.

---

## Review Verdict

```
APPROVED_WITH_AMENDMENTS
```

**Rationale**: The test suite is comprehensive and well-structured. All 4 acceptance criteria are covered, all 12 requirements map to at least one test case, all 51 test plan scenarios are represented, and all 6 mandatory critical scenarios are present with correct tags. Coverage of negative, boundary, and regression paths is thorough.

The three FAIL items (TC-030 weakened assertion; 7 TCs missing secondary REQ tags; 39 TCs missing scope tags) are correctable tag and assertion amendments that do not invalidate the functional coverage. None of the 6 critical scenarios are affected. The suite should not be executed against a production build until the mandatory amendments (items 1–3 above) are applied.
