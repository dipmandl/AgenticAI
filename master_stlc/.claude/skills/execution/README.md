# Execution Skill

## Purpose
Provide reusable patterns for executing automated tests across supported frameworks in both local and CI/CD environments.

## Pre-execution checklist
Before running any tests, verify:
- [ ] Environment variables are set (BASE_URL, credentials, DB connection)
- [ ] Required services are running
- [ ] Test data and fixtures are available
- [ ] Configuration matches the target environment
- [ ] Dependencies are installed

## Execution scope resolution
| Scope | Description | Filter mechanism |
|-------|-------------|-----------------|
| `impacted-tests` | Run only TC-IDs from the current story | Markers/tags matching TC identifiers |
| `smoke` | Run smoke test subset | `@smoke` tag |
| `regression` | Run regression suite | `@regression` tag |
| `all` | Run entire suite | No filter |
| `specific` | Named TC-IDs or tags | User-provided list |

## Framework execution commands
| Framework | Local command | CI headless |
|-----------|--------------|-------------|
| pytest | `pytest -q --tb=short` | `pytest -q --tb=short --no-header` |
| playwright | `pytest -q --browser=chromium` | `pytest -q --browser=chromium --headed=false` |
| selenium | `pytest -q` | `pytest -q` (headless via fixture) |
| behave | `behave` | `behave --no-capture` |
| cypress | `npx cypress run` | `npx cypress run --headless` |

## Exit codes
| Code | Meaning |
|------|---------|
| 0 | All tests passed |
| 1 | At least one test failed |
| 2 | Execution interrupted or error |
| 3 | No tests collected |
| 5 | No tests matched the filter |

## Artifact collection after execution
Always collect to `artifacts/execution/raw-results/<ISO-timestamp>/`:
- Framework-generated XML/JSON report
- Log output
- Screenshots (if any)
- Video or trace files (if configured)

## CI/CD environment variables
Expose the following in CI pipeline config (never hardcode):
```
BASE_URL
TEST_USER
TEST_PASS
DB_URL
API_KEY
```

## Parallel execution
If the framework supports parallel execution and the suite is large, use:
- pytest: `pytest-xdist` with `-n auto`
- Cypress: Cypress Cloud parallel or `--parallel` with recorded run
- Playwright: built-in parallel with `--workers N`
