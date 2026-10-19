# Self-Healing Skill

## Purpose
Define safe, bounded repair patterns for AUTOMATION_FAILURE classified issues.

## Scope
Self-healing applies only to failures classified as `AUTOMATION_FAILURE` by the failure analysis agent.

## Safe repair patterns

### 1. Broken locator
**Symptom**: `ElementNotFound`, `NoSuchElement`, `Unable to locate element`
**Fix**: Update the locator to a stable attribute (prefer `data-testid`, `id`, `name`).
**Forbidden**: Changing what the test is asserting about the located element.

### 2. Timing / wait issue
**Symptom**: `ElementNotInteractable`, `StaleElementReference`, timeout
**Fix**: Add or increase `WebDriverWait`, `page.wait_for_selector`, or `cy.get(timeout)`.
**Forbidden**: Adding `time.sleep` as a permanent fix.

### 3. Incorrect test setup
**Symptom**: Precondition not met, fixture data missing, test DB in wrong state
**Fix**: Correct the `setup` / `before` block or fixture to put the system in the correct precondition.
**Forbidden**: Removing the precondition check.

### 4. Framework syntax error
**Symptom**: `SyntaxError`, `AttributeError` on framework object, import error
**Fix**: Correct the syntax, update the import path, or align with the installed framework version.
**Forbidden**: Disabling the test to hide the syntax error.

### 5. Configuration drift
**Symptom**: `ConnectionRefused`, wrong `base_url`, missing environment variable
**Fix**: Update the config path or environment variable reference in the test config.
**Forbidden**: Hardcoding production values into the test.

## Forbidden self-healing actions
- Removing or loosening an assertion
- Changing an expected value to match a wrong actual value
- Adding `try/except` to swallow assertion errors
- Using `pytest.skip` or `xit` to suppress failure
- Modifying application source code

## Change record format (required before applying any fix)
```
TC-ID: TC-NNN
Failure: <one-line failure description>
Root cause: <specific cause>
File: <path>
Line: <line number if known>
Change: <exact change to be made>
Previous code: <before>
New code: <after>
Business behavior changed: No
```

## Post-healing validation
After each repair, re-run the specific TC identifier using the framework command.
Record result as `HEALED` or `STILL_FAILING`.
If `STILL_FAILING` after `max_self_healing_iterations`, stop and reclassify.

## Iteration limit
Read `max_self_healing_iterations` from `.claude/config/stlc-config.yaml`.
Default: 2. Never exceed this limit for the same failure.
