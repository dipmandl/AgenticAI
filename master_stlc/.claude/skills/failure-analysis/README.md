# Failure Analysis Skill

## Purpose
Guide the failure analysis agent through systematic root cause classification using available evidence.

## Evidence priority order
Read evidence in this order (stop when sufficient to classify):
1. Test framework exit message / summary line
2. Assertion error message (expected vs actual)
3. Stack trace (first 5–10 lines)
4. Screenshot (if available — look for visual mismatch)
5. Application or server logs (if accessible)
6. Network/API response (for API test failures)

## Classification decision tree

```
Did the test fail with an assertion error?
│
├── Yes: Is the expected value correct per the requirement?
│         ├── Yes → APPLICATION_FAILURE (functionality mismatch)
│         └── No  → AUTOMATION_FAILURE (wrong assertion in test code)
│
├── No: Did execution crash before the assertion?
│         ├── Locator / selector not found → AUTOMATION_FAILURE
│         ├── Timeout waiting for element  → AUTOMATION_FAILURE (timing)
│         ├── Connection refused / 503     → ENVIRONMENT_FAILURE
│         ├── Test data missing/null       → TEST_DATA_FAILURE
│         ├── Import / dependency error    → DEPENDENCY_FAILURE
│         ├── Config key missing           → CONFIGURATION_FAILURE
│         └── Unknown exception            → UNKNOWN
```

## Classification rules
- `AUTOMATION_FAILURE`: test code issue — locator, wait, setup, syntax, assertion mismatch due to coding error
- `APPLICATION_FAILURE`: application does not behave as the requirement specifies — confirmed by evidence
- `TEST_DATA_FAILURE`: required data is missing, stale, or in wrong state
- `ENVIRONMENT_FAILURE`: service down, port unreachable, wrong base URL
- `CONFIGURATION_FAILURE`: missing config key, wrong environment variable, misconfigured framework
- `DEPENDENCY_FAILURE`: import error, version mismatch, missing package
- `UNKNOWN`: insufficient evidence; list specifically what evidence would resolve the classification

## What NOT to do
- Never classify as APPLICATION_FAILURE based on assertion values alone without verifying the requirement.
- Never recommend application code changes in this agent.
- Never merge multiple distinct failures into one record.

## Output format per failure
```
TC-ID: TC-NNN
Scenario: <title>
Classification: <one of the 7 categories>
Evidence:
  <log snippet ≤10 lines>
Recommended action: HEAL / DEFECT / INVESTIGATE
```
