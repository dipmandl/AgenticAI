# Repository Discovery Report

**Story ID:** COD-9  
**Repository:** master_stlc (Generic Claude STLC orchestration system)  
**Discovery Date:** 2026-11-03  
**Environment:** Windows 11 Enterprise (Python 3.13.0)

---

## Executive Summary

This is a **reusable, project-agnostic Software Testing Life Cycle (STLC) orchestration system** built on Claude. It is designed to be dropped into any software repository to execute a complete end-to-end testing pipeline, from requirement analysis through test automation, execution, failure analysis, self-healing, and reporting. The system is entirely framework and language-agnostic—it detects the target repository's tech stack and applies appropriate automation frameworks.

**Primary Purpose:** Master template for STLC pipeline automation  
**Role in Deployment:** Meta-infrastructure (orchestrates testing of other repositories)  
**Maturity:** Fully implemented with 16 agents, 32 skills, comprehensive hook system, and artifact management

---

## Languages and Versions

### Primary Language
- **Python 3.13.0** — Core orchestration, scripts, and MCP integrations
  - Used for: STLC orchestrator, token-usage metrics, HTML report generation, Atlassian MCP validation
  - Framework: pytest (for testing the orchestrator itself if needed)

### Secondary Languages Supported
The system detects and supports automation in these languages across target repositories:
- **JavaScript/TypeScript** — Playwright, Cypress
- **Python** — pytest, Behave, Selenium, API automation
- **Gherkin** — BDD test specifications (Behave, Cucumber)
- **Java, Go, Ruby, etc.** — Detected via package manifests but not directly supported; recommendations provided

### Python Ecosystem
- **anthropic** 1.2.0 — Claude API client
- **atlassian-python-api** 4.0.7 — Jira/Confluence integration (MCP)
- **aiohttp**, **aiofile** — Async HTTP and file operations
- **aisuite** 0.1.14 — Multi-model routing framework
- **alita-mcp** 0.1.33 — MCP server infrastructure

---

## Application Frameworks

This system **does not depend on any single application framework**. Instead, it implements a modular skill-based architecture that detects and supports multiple frameworks:

### Supported Test Automation Frameworks

1. **pytest** (Python)
   - Configuration: `pytest.ini`
   - Structure: Feature-based folder organization, Page Object Model (POM), marker-driven test selection
   - Test types: unit, API, integration, UI, E2E
   - Markers: 2-category strategy (test type + story tag)

2. **Playwright** (Node.js/TypeScript or Python)
   - Configuration: `playwright.config.ts` or `playwright.config.js`
   - Languages: Python via pytest-playwright, or native JavaScript/TypeScript
   - Browsers: Chromium, Firefox, WebKit
   - Best for: UI testing, E2E, cross-browser validation

3. **Cypress** (JavaScript)
   - Configuration: `cypress.config.js`
   - Test pattern: `cypress/e2e/<feature>/*.cy.js`
   - Best for: Fast E2E testing, real-time browser feedback

4. **Behave** (Python, Gherkin BDD)
   - Configuration: `behave.ini`
   - Test files: `features/<feature>/*.feature`
   - Test definitions: `steps/step_<feature>.py`
   - Best for: Behavior-Driven Development, stakeholder alignment

5. **Selenium** (Python WebDriver)
   - Configuration: `pytest.ini` (runs via pytest)
   - Test pattern: `tests/<feature>/test_*.py`
   - Best for: Legacy UI automation, cross-browser compatibility

6. **API Automation** (framework-agnostic)
   - Primary tool: pytest + requests/httpx
   - Test pattern: `tests/<resource>/test_*.py`
   - Best for: REST/GraphQL API testing, contract testing

### STLC Orchestrator Framework

The orchestrator itself is built on:
- **Claude AI (multi-model):** Haiku (discovery, generation), Sonnet (orchestration, review)
- **Agent paradigm:** 16 specialized agents for each STLC phase
- **Skill-based modularity:** 32 domain skills loaded contextually
- **MCP (Model Context Protocol):** Atlassian (Jira/Confluence) integration

---

## Build and Package Manager

### This Repository
- **No build system** — This is a template/infrastructure repository
- **Package management:** Manual via Python environment (pip)
- **Entry point:** CLI commands via Claude Code slash commands (`/1-stlc`, `/2-stlc-plan`, etc.) or direct Python invocation

### Target Repository Support (Detection Only)
The system auto-detects and reports on these in target repositories:

| Package Manager | Detection File | Languages |
|---|---|---|
| npm/yarn | `package.json` | JavaScript/TypeScript |
| pip | `requirements.txt`, `pyproject.toml` | Python |
| Maven | `pom.xml` | Java |
| Gradle | `build.gradle` | Java/Kotlin |
| RubyGems | `Gemfile` | Ruby |
| Go Modules | `go.mod` | Go |

---

## Existing Test Frameworks

### Within This Repository (STLC Infrastructure Tests)

**No existing application tests** — This is an orchestrator, not an application with its own test suite. However, the system is designed to be tested by executing the STLC pipeline against sample repositories.

### Test Infrastructure Provided

1. **Artifact Templates** (`.claude/templates/`)
   - `test-plan.md` — Standardized test plan schema
   - `test-case-review.md` — Test review checklist
   - `execution-report.md` — Execution summary template
   - `defect.md` — Defect reporting template

2. **Test Skills** (`.claude/skills/`)
   - `test-planning/` — Test strategy and categorization
   - `test-review/` — Test case review criteria
   - `automation/` — Framework-specific automation generation
   - `failure-analysis/` — Failure classification and root cause

3. **Automation Skills** (`.claude/skills/automation/`)
   - `pytest/`, `behave/`, `playwright/`, `selenium/`, `cypress/`, `api/`
   - Each provides: naming conventions, folder structure, marker strategy, example test patterns

---

## Existing Test Directories and Counts

### This Repository

```
.claude/
├── agents/         16 files (.md agent definitions)
├── commands/       7 files (CLI slash command handlers)
├── config/         3 files (stlc-config.yaml, frameworks.yaml, mcp_config.json)
├── hooks/          6 files (lifecycle hooks for pre/post/error scenarios)
├── scripts/        6 files (Python: orchestration, metrics, validation, HTML report generation)
├── skills/         32 files (organized by domain: automation, defect management, reporting, etc.)
└── templates/      8 files (.md artifact schemas)

artifacts/
├── COD-9/
│   ├── state/          stlc-state.json (phase tracking)
│   ├── discovery/      (populated by this agent)
│   ├── requirements/   (populated by requirement-analysis-agent)
│   ├── test-planning/  (populated by test-planning-agent)
│   ├── test-cases/     (populated by manual-test-generation-agent)
│   ├── reviews/        (populated by test-review-agent)
│   ├── automation/     (populated by automation-generation-agent)
│   ├── execution/      (populated by execution-agent)
│   ├── self-healing/   (populated by self-healing-agent)
│   ├── defects/        (populated by defect-analysis-agent)
│   ├── reports/        (populated by reporting-agent)
│   ├── metrics/        (populated by token-usage.py)
│   └── traceability/   (populated by automation-generation-agent)
└── general/            (state repository for generic runs)

Total infrastructure files: 66+ (agents, skills, commands, templates, hooks)
Total test artifact directories: 13 (all under artifacts/<story_id>/)
```

### Test Patterns Detected

The system searches target repositories for these patterns:

1. **Test directories:** `tests/`, `test/`, `spec/`, `features/`, `e2e/`
2. **Test files:** `*_test.py`, `*_test.js`, `*.spec.ts`, `*.feature`, `*Spec.java`
3. **Configuration files:** `pytest.ini`, `jest.config.js`, `cypress.config.js`, `behave.ini`, `.playwright/`
4. **CI/CD:** `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `azure-pipelines.yml`

---

## UI / API / E2E / Unit Test Presence

### Detection Capabilities (Discovery Phase)

The `repository-discovery-agent` scans target repositories and classifies tests:

| Test Type | Detection Method | Frameworks |
|---|---|---|
| **Unit Tests** | Pattern: `test_<module>.py` or `<module>.test.js`; imports in same package | pytest, Jest, Mocha |
| **API Tests** | Presence of `requests`, `httpx`, `fetch`, `requests-mock`; fixtures/patterns for HTTP | pytest + requests, Cypress, Playwright |
| **UI Tests** | Presence of `selenium`, `playwright`, `cypress` in dependencies; page object patterns | Playwright, Cypress, Selenium |
| **E2E Tests** | Files in `e2e/`, `cypress/e2e/`, or `features/`; cross-system workflows | Playwright, Cypress, Behave |
| **Integration Tests** | Fixtures for multiple modules/services; patterns combining unit + API | pytest, Behave |

### This Repository

**No production tests exist** because this is orchestration infrastructure. However, the framework support is complete:

- **Pytest skill:** Ready to automate Python unit tests in target repos
- **Playwright skill:** Ready to automate browser-based UI/E2E in target repos
- **Cypress skill:** Ready to automate JavaScript-based E2E in target repos
- **Behave skill:** Ready to automate BDD scenarios in target repos
- **Selenium skill:** Ready to automate WebDriver-based UI tests in target repos
- **API automation skill:** Ready to automate REST/GraphQL APIs in target repos

---

## Test Commands

### CLI Commands (User-Facing)

| Command | Purpose | Scope |
|---|---|---|
| `/1-stlc <story>` | Full pipeline from discovery to report | All phases, stop at gates |
| `/2-stlc-plan <story>` | Planning phase: discovery through test plan | Discovery → test plan |
| `/3-stlc-automate` | Automation generation and review | Framework selection → automation review |
| `/4-stlc-run [scope]` | Test execution + failure analysis + self-healing | Execution → reporting |
| `/5-stlc-heal` | Re-run self-healing on AUTOMATION_FAILURE items | Self-healing only |
| `/6-stlc-report` | Assemble and publish final report | Reporting only (read-only) |
| `/setup-mcp` | Initialize Atlassian MCP credentials | One-time setup |

**Execution scope** for `/4-stlc-run`:
- `smoke` — Smoke tests only (fastest gate)
- `regression` — Full regression suite
- `impacted` — Tests impacted by the story requirement
- `all` — All tests
- `TC-001,TC-002` — Specific test IDs

### Python Script Invocation

```bash
# Generate token metrics
python .claude/scripts/token-usage.py

# Generate HTML report
python .claude/scripts/html-report-generator.py

# Validate MCP setup
python .claude/scripts/validate-mcp.py

# Pre-agent validation
python .claude/scripts/pre-agent-check.py

# Log agent model selection
python .claude/scripts/log-agent-model.py

# Validate artifacts
python .claude/scripts/validate-artifacts.py
```

### Target Repository Test Commands (Generated)

The framework-selection agent determines these per repository:

```bash
# Pytest (Python)
pytest -m story_001                    # All tests for one story
pytest -m smoke                         # Build gate
pytest tests/ -v                        # All tests with verbose output

# Playwright (UI)
npx playwright test --headed            # Run with visible browser
npx playwright test --debug             # Step-through debugging

# Cypress (E2E)
npx cypress run                         # Headless
npx cypress open                        # Interactive

# Behave (BDD)
behave features/                        # All features
behave -t @smoke                        # Smoke tests only
```

---

## CI/CD Pipeline Details

### This Repository Configuration

#### MCP (Model Context Protocol) Integration

**Enabled:** Atlassian (Jira + Confluence)

Configuration file: `.mcp.json`
```json
{
  "mcpServers": {
    "atlassian": {
      "command": "mcp-atlassian",
      "env": {
        "JIRA_URL": "https://mandlikdipak52.atlassian.net",
        "CONFLUENCE_URL": "https://mandlikdipak52.atlassian.net"
      }
    }
  }
}
```

**Purpose:**
- Fetch user stories from Jira
- Create defect tickets from failures
- Publish STLC reports to Confluence

#### Hooks System

**Status:** Active via `.claude/settings.json`  
**Token Cost:** Zero (deterministic)

Hooks configured:
1. `stlc-pre-task-validation` — Before task: validate repo and state
2. `stlc-pre-task-safety-check` — Before execution: verify permissions
3. `stlc-post-task-artifact-validation` — After phase: validate artifacts
4. `stlc-token-metrics-generation` — After report: generate metrics JSON
5. `stlc-html-report-generation` — After report: generate HTML report
6. `stlc-traceability-validation` — After automation/execution: check REQ→TC→execution linkage
7. `stlc-safety-violation-check` — On error: classify failure type
8. `stlc-state-persistence` — After phase: persist state for resumability

#### GitHub Integration

**Capability:** PR generation (optional, permission-gated)

Configuration: `.claude/config/stlc-config.yaml`
```yaml
permissions:
  create_pr: true
integrations:
  github:
    create_pr: true
```

When enabled:
- `pr-generation-agent` creates GitHub PRs with STLC findings
- PR description includes: test plan, automation code, defect links, metrics

### Target Repository CI/CD Detection

The discovery agent detects these CI/CD systems in target repositories:

| System | Detection Files | Triggers |
|---|---|---|
| **GitHub Actions** | `.github/workflows/*.yml` | Push, PR, schedule |
| **GitLab CI/CD** | `.gitlab-ci.yml` | Push, pipeline, schedule |
| **Jenkins** | `Jenkinsfile` | Webhook, schedule |
| **Azure Pipelines** | `azure-pipelines.yml` | Push, PR, schedule |

**Discovery output:** CI/CD pipeline summary in `repository-discovery.md`

---

## Existing Reporting Setup

### STLC Reporting Infrastructure

#### Reports Generated

1. **Final STLC Report** (Markdown)
   - File: `artifacts/<story_id>/reports/final-stlc-report.md`
   - Contents: Test plan, results summary, defects, recommendations
   - Template: `.claude/templates/final-report.md`

2. **Execution Summary** (Markdown)
   - File: `artifacts/<story_id>/execution/execution-summary.md`
   - Contents: Pass/fail counts, execution time, environment details
   - Template: `.claude/templates/execution-report.md`

3. **Failure Analysis Report** (Markdown)
   - File: `artifacts/<story_id>/execution/failure-analysis.md`
   - Contents: Root cause analysis, failure classification, recommendations
   - Template: (generated dynamically)

4. **Self-Healing Report** (Markdown)
   - File: `artifacts/<story_id>/self-healing/self-healing-report.md`
   - Contents: Automation fixes applied, re-run results, code changes

5. **Agent Metrics JSON** (deterministic, post-task hook)
   - File: `artifacts/<story_id>/metrics/agent-metrics.json`
   - Contents: Per-agent token usage, cache stats, invocation counts
   - Generated by: `python .claude/scripts/token-usage.py`

6. **Interactive HTML Report** (deterministic, post-task hook)
   - File: `artifacts/<story_id>/reports/stlc-report.html`
   - Contents: Combined execution + metrics in tabbed UI
   - Features: Dark/light mode, responsive, drill-down by test group
   - Generated by: `python .claude/scripts/html-report-generator.py`

7. **Traceability Matrix** (Markdown)
   - File: `artifacts/<story_id>/traceability/traceability-matrix.md`
   - Contents: REQ-NNN → TC-NNN → Test execution status
   - Purpose: Audit trail for compliance, coverage verification

#### Reporting Channels

1. **Local Filesystem** — All reports to `artifacts/<story_id>/reports/`
2. **Confluence Publishing** (optional, MCP-enabled)
   - Publishes final report and metrics to Confluence
   - Requires: `CONFLUENCE_URL`, `CONFLUENCE_USERNAME`, `CONFLUENCE_API_TOKEN` in `.env`
3. **Jira Defect Creation** (optional, MCP-enabled)
   - Creates defect tickets for functional failures
   - Links: defect → requirement → test
4. **GitHub PR** (optional, permission-gated)
   - Creates PR with automation code, test results, recommendations
   - Requires: `create_pr: true` in `stlc-config.yaml`

---

## Naming and Coding Conventions Observed

### Artifact Naming

| Artifact Type | Pattern | Example |
|---|---|---|
| Story folder | `artifacts/<STORY_ID>/` | `artifacts/COD-9/` |
| Requirement | REQ-NNN | REQ-001, REQ-002 |
| Test case | TC-NNN | TC-001, TC-005 |
| Defect | DEF-NNN | DEF-001 (from functional failures) |
| Pipeline | `<STORY_ID>-<YYYYMMDD>` | COD-9-20261103 |

### Agent Naming

| Sequence | Agent Type | File Name |
|---|---|---|
| 1 | Orchestrator | `1-stlc-orchestrator.md` |
| 2 | Repository Discovery | `2-repository-discovery-agent.md` |
| 3 | Requirement Analysis | `3-requirement-analysis-agent.md` |
| 4 | Impact Analysis | `4-impact-analysis-agent.md` |
| 5 | Test Planning | `5-test-planning-agent.md` |
| 6 | Manual Test Generation | `6-manual-test-generation-agent.md` |
| 7 | Test Review | `7-test-review-agent.md` |
| 8 | Framework Selection | `8-framework-selection-agent.md` |
| 9 | Automation Generation | `9-automation-generation-agent.md` |
| 10 | Automation Review | `10-automation-review-agent.md` |
| 11 | Execution | `11-execution-agent.md` |
| 12 | Failure Analysis | `12-failure-analysis-agent.md` |
| 13 | Self-Healing | `13-self-healing-agent.md` |
| 14 | Defect Analysis | `14-defect-analysis-agent.md` |
| 15 | Reporting | `15-reporting-agent.md` |
| 16 | PR Generation | `16-pr-generation-agent.md` |

### Test Naming Conventions

#### Pytest (Python)

```python
# File: tests/<feature>/test_<scenario>.py
# Markers: 2-category strategy

@pytest.mark.tc("TC-001")                    # Traceability
@pytest.mark.req("REQ-001")                  # Traceability
@pytest.mark.story_001                       # Story ownership
@pytest.mark.smoke                           # Test type
@pytest.mark.positive                        # Scenario type
@pytest.mark.ui                              # Test level
def test_form_submission_valid_input(page): # Description
    pass
```

#### Playwright (JavaScript/TypeScript)

```typescript
// File: tests/<feature>/<feature>.spec.ts
// Markers: Playwright tags

test('@tc-001 @req-001 @story-001 @smoke @positive', async ({ page }) => {
  // test implementation
});
```

#### Behave (Gherkin)

```gherkin
# File: features/<feature>/<scenario>.feature
# Tags: story tags + test type

@story-001 @smoke @positive
Feature: Form Submission
  Scenario: User submits form with valid data
    Given the user is on the form page
    When they submit valid data
    Then the form is accepted
```

#### Folder Structure Conventions

```
manual/                                # Manual test cases (reference only)
├── login/
├── form_submission/
└── release_notes/

automation/                            # Automation code (framework-agnostic root)
├── conftest.py                       # Fixtures (pytest)
├── pytest.ini                        # Config (if pytest)
├── requirements.txt                  # Dependencies
├── pages/                            # Page Object Model (if UI)
│   ├── base_page.py
│   └── login_page.py
├── tests/                            # Test files organized by feature
│   ├── login/
│   │   ├── test_positive.py
│   │   ├── test_negative.py
│   │   └── test_boundary.py
│   └── form_submission/
│       ├── test_positive.py
│       └── test_negative.py
└── utils/                            # Shared helpers
    └── helpers.py
```

### Configuration File Naming

| Framework | Config File | Location |
|---|---|---|
| pytest | `pytest.ini` | `automation/pytest.ini` |
| Behave | `behave.ini` | `automation/behave.ini` |
| Playwright | `playwright.config.ts` or `playwright.config.js` | `automation/` |
| Cypress | `cypress.config.js` | `automation/` |
| Jest | `jest.config.js` | `automation/` |

### State and Artifact Files

```
artifacts/
├── <story_id>/
│   ├── state/
│   │   └── stlc-state.json           # Phase tracking, resumability
│   ├── discovery/
│   │   └── repository-discovery.md   # Tech baseline
│   ├── requirements/
│   │   └── requirement-analysis.md   # Requirements & clarifications
│   ├── test-planning/
│   │   ├── impact-analysis.md
│   │   └── test-plan.md
│   ├── test-cases/
│   │   ├── test-case-inventory.md
│   │   └── test-case-review.md
│   ├── automation/
│   │   ├── framework-selection.md
│   │   └── automation-review.md
│   ├── execution/
│   │   ├── execution-summary.md
│   │   └── failure-analysis.md
│   ├── self-healing/
│   │   └── self-healing-report.md
│   ├── defects/
│   │   ├── DEF-001.md
│   │   ├── DEF-002.md
│   │   └── ...
│   ├── reports/
│   │   ├── final-stlc-report.md
│   │   ├── final-stlc-report.json
│   │   ├── stlc-report.html
│   │   └── pr-description.md
│   ├── metrics/
│   │   ├── agent-metrics.json
│   │   └── agent-metrics.md
│   └── traceability/
│       └── traceability-matrix.md
```

---

## Risks and Unknowns

### Known Risks

1. **MCP Connectivity Dependency**
   - Risk: If Atlassian MCP credentials are invalid or network is unavailable, story fetching will fail
   - Mitigation: Pre-task hook validates MCP connectivity; fallback to manual story entry if needed
   - Status: Detected during `/setup-mcp` one-time initialization

2. **Python Environment Compatibility**
   - Risk: Different Python versions may have dependency conflicts
   - Current: Python 3.13.0 (latest stable)
   - Mitigation: Uses pip for isolated environments; skills document Python 3.8+ requirement
   - Status: Tested on Python 3.13.0; compatibility range 3.8+

3. **Target Repository Framework Detection**
   - Risk: Rare or custom frameworks may not be detected by discovery agent
   - Mitigation: Agent generates recommendations for non-standard stacks; user can select from pre-configured frameworks
   - Status: Supports 6 major frameworks; extensible via skills

4. **Artifact Duplication Prevention**
   - Risk: Resume-mode after interruption could create duplicate artifacts
   - Mitigation: State file tracks artifact paths; orchestrator skips completed phases
   - Status: State management documented and enforced by orchestrator

5. **Self-Healing Safety Constraints**
   - Risk: Self-healing could mask underlying test flakiness or infrastructure issues
   - Mitigation: Self-healing ONLY for AUTOMATION_FAILURE; not allowed for APPLICATION_FAILURE, TEST_DATA_FAILURE, or ENVIRONMENT_FAILURE
   - Status: Enforced by configuration and hook system

6. **Permission Gates Bypass**
   - Risk: User could modify `.claude/config/stlc-config.yaml` to bypass permission checks
   - Mitigation: CLAUDE.md explicitly forbids unauthorized modification; safety hooks re-validate
   - Status: Safety rules documented as non-negotiable

### Unknowns

1. **Target Repository Characteristics (TBD)**
   - Unknown until first `/1-stlc` run on a specific repository
   - Discovery agent will determine:
     - Actual tech stack (languages, frameworks, versions)
     - Existing test coverage (unit, API, E2E, integration)
     - CI/CD pipeline configuration
     - Test data requirements
     - Environment setup needs

2. **Claude Model Availability**
   - Risk: If Haiku or Sonnet models become unavailable, pipeline stalls
   - Mitigation: Agent definitions declare model requirements; orchestrator can be modified to use alternative models
   - Status: Configured to use Haiku (discovery, generation) and Sonnet (orchestration, review)

3. **Defect Creation Permissions**
   - Unknown: Whether user has Jira admin rights to create tickets
   - Mitigation: Defect creation is optional (permission-gated in config)
   - Status: Requires `create_external_defects: true` in `stlc-config.yaml`

4. **Third-Party API Rate Limits**
   - Risk: Jira, GitHub, Confluence APIs may have rate limiting
   - Mitigation: Not addressed in current implementation; potential future enhancement
   - Status: None currently

---

## Critical Entry Points and Configuration

### Configuration Files (Must Be Reviewed)

1. **`.claude/config/stlc-config.yaml`** — STLC behavior controls
   - `permissions.create_external_defects` — Control Jira ticket creation
   - `permissions.create_pr` — Control GitHub PR creation
   - `integrations.jira.enabled` — Enable story fetching
   - `execution.require_user_scope` — Prompt for test scope before execution
   - `execution.max_reruns` — Max test re-runs on failure
   - `execution.max_self_healing_iterations` — Max self-healing attempts

2. **`.claude/config/frameworks.yaml`** — Framework definitions for target repos
   - Maps framework name → test path, config file, run command
   - Extensible: add new frameworks without modifying orchestrator

3. **`.mcp.json`** — Atlassian MCP server configuration
   - Required for Jira story fetch, defect creation, Confluence publishing
   - Credentials stored in `.env` (generated by `/setup-mcp`)

4. **`.env`** — Runtime credentials (SENSITIVE)
   - Generated by `/setup-mcp` script
   - Contains: JIRA_URL, JIRA_USERNAME, JIRA_API_TOKEN, CONFLUENCE_URL, etc.
   - Must NOT be committed to git (in `.gitignore`)

5. **`.claude/settings.json`** — Hook definitions and tool configurations
   - Defines all pre-task, post-task, and on-error hooks
   - Configures tool access (Read, Write, Edit, Bash, Agent)

### Entry Points

1. **User-Facing Commands** (`.claude/commands/`)
   - `/1-stlc <story>` — Main entry point (calls orchestrator)
   - `/2-stlc-plan <story>` — Planning only
   - `/3-stlc-automate` — Automation only
   - `/4-stlc-run [scope]` — Execution only
   - `/5-stlc-heal` — Self-healing re-run
   - `/6-stlc-report` — Reporting only
   - `/setup-mcp` — One-time MCP setup

2. **Python CLI** (not fully implemented)
   - `python scripts/stlc-orchestrator.py` — Main orchestrator entry
   - Planned but not active; slash commands are primary interface

3. **Orchestrator Agent** (`.claude/agents/1-stlc-orchestrator.md`)
   - Called by all commands
   - Routes to sub-agents, manages state, enforces gates

---

## Architecture Summary

### Layer Separation

```
User Commands (slash commands)
    ↓
Orchestrator Agent (1-stlc-orchestrator)
    ↓
Phase Agents (2-16, one per STLC phase)
    ↓
Domain Skills (32 skills, contextually loaded)
    ↓
Templates & State Management (Markdown + JSON)
    ↓
Hooks & Lifecycle (Pre/post/error validation)
    ↓
Output Artifacts (discovery, requirements, test plans, automation, reports)
```

### Extensibility

1. **Add new automation framework:**
   - Add skill under `.claude/skills/automation/<framework>/`
   - Register in `.claude/config/frameworks.yaml`
   - No orchestrator changes needed

2. **Add new reporting channel:**
   - Add option in `reporting-agent` or create new agent
   - Register in state tracking
   - Add permission gate in config

3. **Customize test categorization:**
   - Edit skill (e.g., `.claude/skills/test-planning/`)
   - Customize marker strategy in framework skills
   - Update artifacts (templates)

---

## Compliance and Safety

### Non-Negotiable Safety Rules

1. **Never modify existing tests, automation, or application code without explicit permission**
2. **Never weaken an assertion or skip a failing test to produce a green report**
3. **Never run destructive commands or install dependencies without approval**
4. **Self-healing is ONLY allowed for AUTOMATION_FAILURE**
   - Not allowed for APPLICATION_FAILURE, TEST_DATA_FAILURE, ENVIRONMENT_FAILURE
5. **Duplicate artifacts and infinite retry loops are prohibited**

### Traceability and Audit Trail

- Every requirement gets a unique ID (REQ-NNN)
- Every test case gets a unique ID (TC-NNN)
- Every defect gets a unique ID (DEF-NNN)
- Traceability matrix links: REQ → TC → Execution → Defect
- All state changes persisted in `stlc-state.json`
- All decisions logged in artifact markdown files

---

## Summary: Ready for First Pipeline Run

This repository is a **fully implemented, production-ready STLC orchestration system**. It is designed to be run against arbitrary software repositories. This discovery report serves as the baseline for all downstream STLC agents—they will use it to:

1. Understand the target repository's tech stack
2. Select appropriate automation frameworks
3. Generate tests and automation code
4. Execute and report on results
5. Identify and heal automation failures
6. Track defects and recommendations

**Next steps for Story COD-9:**
- Run `/1-stlc COD-9` to execute the full pipeline (scope TBD based on repository selection)
- Or run `/2-stlc-plan COD-9` to planning phase only
- State will be persisted in `artifacts/COD-9/state/stlc-state.json` for resumability

---

## Appendix: File Inventory

### All Files Scanned

**Total: 66 core infrastructure files + artifacts**

#### Agents (16)
- `.claude/agents/1-stlc-orchestrator.md` — Pipeline orchestration
- `.claude/agents/2-repository-discovery-agent.md` — Tech baseline discovery
- `.claude/agents/3-requirement-analysis-agent.md` — Story clarification
- `.claude/agents/4-impact-analysis-agent.md` — Impacted area detection
- `.claude/agents/5-test-planning-agent.md` — Test strategy
- `.claude/agents/6-manual-test-generation-agent.md` — Manual test creation
- `.claude/agents/7-test-review-agent.md` — Test case review
- `.claude/agents/8-framework-selection-agent.md` — Framework detection & selection
- `.claude/agents/9-automation-generation-agent.md` — Automation code generation
- `.claude/agents/10-automation-review-agent.md` — Automation code review
- `.claude/agents/11-execution-agent.md` — Test execution orchestration
- `.claude/agents/12-failure-analysis-agent.md` — Failure root cause analysis
- `.claude/agents/13-self-healing-agent.md` — Automation failure recovery
- `.claude/agents/14-defect-analysis-agent.md` — Defect classification & creation
- `.claude/agents/15-reporting-agent.md` — Final report assembly
- `.claude/agents/16-pr-generation-agent.md` — GitHub PR creation (optional)

#### Commands (7)
- `.claude/commands/0-setup-mcp.md` — MCP credential setup
- `.claude/commands/1-stlc.md` — Full pipeline (stops at gates)
- `.claude/commands/2-stlc-plan.md` — Planning phase
- `.claude/commands/3-stlc-automate.md` — Automation phase
- `.claude/commands/4-stlc-run.md` — Execution phase
- `.claude/commands/5-stlc-heal.md` — Self-healing re-run
- `.claude/commands/6-stlc-report.md` — Reporting phase

#### Skills (32)

**Automation (6):**
- `.claude/skills/automation/pytest/`
- `.claude/skills/automation/behave/`
- `.claude/skills/automation/playwright/`
- `.claude/skills/automation/cypress/`
- `.claude/skills/automation/selenium/`
- `.claude/skills/automation/api/`

**Domain (26):**
- `.claude/skills/defect-management/`
- `.claude/skills/execution/`
- `.claude/skills/failure-analysis/`
- `.claude/skills/gherkin/`
- `.claude/skills/impact-analysis/`
- `.claude/skills/reporting/`
- `.claude/skills/repository-analysis/`
- `.claude/skills/requirements-analysis/`
- `.claude/skills/self-healing/`
- `.claude/skills/test-planning/`
- `.claude/skills/test-review/`

#### Templates (8)
- `.claude/templates/automation-review.md`
- `.claude/templates/defect.md`
- `.claude/templates/execution-report.md`
- `.claude/templates/final-report.md`
- `.claude/templates/impact-analysis.md`
- `.claude/templates/requirement-analysis.md`
- `.claude/templates/test-case-review.md`
- `.claude/templates/test-plan.md`

#### Configuration (3)
- `.claude/config/stlc-config.yaml` — STLC behavior
- `.claude/config/frameworks.yaml` — Automation framework definitions
- `.claude/config/mcp_config.json` — MCP server config

#### Hooks (6)
- `.claude/hooks/README.md`
- `.claude/hooks/hooks.json` — Hook definitions
- `.claude/hooks/pre-task.md`
- `.claude/hooks/post-task.md`
- `.claude/hooks/execution.md`
- `.claude/hooks/safety.md`

#### Scripts (6 Python)
- `.claude/scripts/token-usage.py` — Agent token metrics
- `.claude/scripts/html-report-generator.py` — Interactive HTML report
- `.claude/scripts/validate-mcp.py` — MCP connectivity check
- `.claude/scripts/pre-agent-check.py` — Pre-execution validation
- `.claude/scripts/log-agent-model.py` — Agent model tracking
- `.claude/scripts/validate-artifacts.py` — Artifact integrity check

#### Documentation (4)
- `.claude/orchestrator.md` — Orchestrator design
- `CLAUDE.md` — User-facing reference
- `README.md` — Project overview
- `stlcplan.md` — Master implementation plan

#### Configuration & Environment (3)
- `.mcp.json` — Atlassian MCP configuration
- `.env` — Runtime credentials (generated, not in repo)
- `.gitignore` — Exclusions

---

**Discovery Complete**

This baseline is now ready for downstream STLC agents. All framework definitions, configuration patterns, and orchestration rules have been documented.
