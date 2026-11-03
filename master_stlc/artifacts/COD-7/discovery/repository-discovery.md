# Repository Discovery Report

**Story ID**: COD-7  
**Generated**: 2026-11-03  
**Repository Root**: C:\Users\DipakMandlik\Desktop\AgenticAI\Final_implementation\AgenticAI\master_stlc  

---

## Project Overview

This is a **Generic Claude STLC (Software Testing Life Cycle) Orchestration System**—a reusable, project-agnostic framework for automating the end-to-end testing workflow. The framework includes a cloud-based master test orchestration system written in Python/Bash, complete with Claude AI agent integration, MCP (Model Context Protocol) connectors for Atlassian (Jira/Confluence), and built-in test automation skill libraries.

**Key Application Under Test**: Release Notes Dashboard (product_release_dashboard/) — a lightweight, dependency-free HTML/CSS/JavaScript web application for managing and viewing release notes.

**Primary Purpose**: This repository serves as a reusable test framework engine, NOT a specific application. It is designed to be integrated into target repositories to execute complete STLC pipelines.

---

## Technology Stack

### Core Framework & Language
- **Primary Language**: Python (orchestrator, scripts, hooks)
- **Secondary Languages**: JavaScript (Release Dashboard app), YAML (configuration), Markdown (templates & documentation), PowerShell (bootstrap scripts)
- **Python Version**: Not explicitly pinned (assumed 3.8+)
- **CLI**: Bash/PowerShell (Git Bash on Windows)

### Claude AI Integration
- **Claude Model**: Haiku 4.5 (primary agent model), Sonnet (orchestrator), as declared in agent frontmatter
- **MCP Integrations**: Atlassian (Jira/Confluence) via `mcp-atlassian` package
- **MCP Configuration**: `.mcp.json` (project-scoped, loaded by hooks)
- **Model Selection**: Per-phase model routing via `.claude/config/models.yaml` and agent frontmatter (`model:` field)

### Test Automation Frameworks (Configured & Available)
1. **Pytest** — Python unit/integration/API/UI testing (primary framework)
2. **Behave** — Python BDD framework with Gherkin scenarios
3. **Playwright** — Node.js/TypeScript browser automation (E2E/UI)
4. **Cypress** — JavaScript E2E testing framework
5. **Selenium** — Python WebDriver-based cross-browser UI automation
6. **API Automation** — Framework-agnostic API testing via pytest + requests/httpx

### Supporting Libraries & Tools
- **Test Configuration Format**: YAML/INI (pytest.ini, behave.ini, playwright.config.ts, cypress.config.js)
- **State Management**: JSON (stlc-state.json for pipeline resumability)
- **Artifact Format**: Markdown with JSON metadata
- **CI/CD Support**: GitHub Actions (.github/workflows/), GitLab CI, Jenkins, Azure Pipelines (detection only)
- **Package Managers**: 
  - Python: pip (inferred, not explicitly locked)
  - Node.js: npm (assumed for Playwright/Cypress)
  - Ruby: Bundler (Gemfile support detected)
  - Go: Go modules (go.mod support detected)
  - Java: Maven/Gradle (pom.xml, build.gradle support detected)

### External Integrations
- **Atlassian Jira**: Create tickets from defects; read/write work items
- **Atlassian Confluence**: Publish STLC reports
- **GitHub**: Create pull requests (permission-gated, currently disabled)
- **MCP Server**: mcp-atlassian (Python-based, credentials in .env)

---

## Directory Structure

### Repository Layout
```
master_stlc/
├── README.md                          # Project overview
├── CLAUDE.md                          # Main user-facing instructions
├── stlcplan.md                        # Master STLC architecture & implementation plan
│
├── .claude/                           # Claude AI framework configuration
│   ├── agents/                        # 16 numbered agent definitions (1-stlc-orchestrator through 15-reporting-agent)
│   │   ├── 1-stlc-orchestrator.md     # Main pipeline coordinator (Sonnet model)
│   │   ├── 2-repository-discovery-agent.md    # Scan target repository (Haiku model)
│   │   ├── 3-requirement-analysis-agent.md
│   │   ├── 4-impact-analysis-agent.md
│   │   ├── 5-test-planning-agent.md
│   │   ├── 6-manual-test-generation-agent.md
│   │   ├── 7-test-review-agent.md
│   │   ├── 8-framework-selection-agent.md
│   │   ├── 9-automation-generation-agent.md
│   │   ├── 10-automation-review-agent.md
│   │   ├── 11-execution-agent.md
│   │   ├── 12-failure-analysis-agent.md
│   │   ├── 13-self-healing-agent.md
│   │   ├── 14-defect-analysis-agent.md
│   │   ├── 15-reporting-agent.md
│   │   └── 16-pr-generation-agent.md
│   │
│   ├── commands/                      # User-facing command entry points
│   │   ├── 0-setup-mcp.md             # MCP initialization (one-time)
│   │   ├── 1-stlc.md                  # Full pipeline (/1-stlc <story>)
│   │   ├── 2-stlc-plan.md             # Planning only (/2-stlc-plan <story>)
│   │   ├── 3-stlc-automate.md         # Automation generation (/3-stlc-automate)
│   │   ├── 4-stlc-run.md              # Execution & analysis (/4-stlc-run [scope])
│   │   ├── 5-stlc-heal.md             # Self-healing (/5-stlc-heal)
│   │   └── 6-stlc-report.md           # Final reporting (/6-stlc-report)
│   │
│   ├── config/                        # Configuration files
│   │   ├── stlc-config.yaml           # Permission gates, execution limits, integrations
│   │   ├── frameworks.yaml            # Framework definitions (pytest, playwright, cypress, behave, selenium, api)
│   │   └── mcp_config.json            # MCP server configuration
│   │
│   ├── skills/                        # Reusable domain knowledge
│   │   ├── automation/                # Framework-specific automation skills
│   │   │   ├── pytest/SKILL.md
│   │   │   ├── behave/SKILL.md
│   │   │   ├── playwright/SKILL.md
│   │   │   ├── cypress/SKILL.md
│   │   │   ├── selenium/SKILL.md
│   │   │   └── api/SKILL.md
│   │   ├── defect-management/SKILL.md
│   │   ├── execution/SKILL.md
│   │   ├── failure-analysis/SKILL.md
│   │   ├── gherkin/SKILL.md
│   │   ├── impact-analysis/SKILL.md
│   │   ├── repository-analysis/SKILL.md
│   │   ├── requirements-analysis/SKILL.md
│   │   ├── test-planning/SKILL.md
│   │   ├── test-review/SKILL.md
│   │   ├── self-healing/SKILL.md
│   │   ├── reporting/SKILL.md
│   │   └── [more skills...]
│   │
│   ├── templates/                     # Standardized artifact schemas
│   │   ├── test-plan.md
│   │   ├── test-case-review.md
│   │   ├── automation-review.md
│   │   ├── requirement-analysis.md
│   │   ├── execution-report.md
│   │   ├── defect.md
│   │   ├── final-report.md
│   │   └── impact-analysis.md
│   │
│   ├── hooks/                         # Pipeline lifecycle hooks
│   │   ├── hooks.json                 # Hook definitions (pre-task, post-task, on-error)
│   │   ├── pre-task.md                # Pre-flight validation
│   │   ├── post-task.md               # Post-phase artifact validation
│   │   ├── safety.md                  # Safety constraint enforcement
│   │   └── execution.md               # Execution lifecycle hooks
│   │
│   ├── scripts/                       # Utility scripts (Python)
│   │   ├── pre-agent-check.py         # PreToolUse hook: validate state before agent invocation
│   │   ├── log-agent-model.py         # PostToolUse hook: record agent model usage
│   │   ├── token-usage.py             # Generate token metrics per phase and agent
│   │   ├── validate-artifacts.py      # Verify artifact structure
│   │   ├── validate-mcp.py            # MCP connectivity check
│   │   └── html-report-generator.py   # Generate interactive HTML report
│   │
│   ├── settings.json                  # Claude Code hook configuration (PreToolUse, PostToolUse, Stop)
│   ├── settings.local.json            # Local settings override (not tracked)
│   └── orchestrator.md                # Orchestration strategy & documentation
│
├── artifacts/                         # Generated artifacts & state (one folder per story_id)
│   ├── COD-7/                         # Current story artifacts
│   │   ├── state/
│   │   │   └── stlc-state.json        # Pipeline state, resumability marker
│   │   ├── discovery/                 # Repo analysis
│   │   ├── requirements/              # Requirement analysis
│   │   ├── test-planning/             # Impact analysis, test plan
│   │   ├── test-cases/                # Test case inventory & manual tests
│   │   ├── reviews/                   # Test reviews, automation reviews
│   │   ├── automation/                # Automation plan, framework selection
│   │   ├── execution/                 # Test execution results
│   │   ├── self-healing/              # Self-healing reports
│   │   ├── defects/                   # Defect records (DEF-NNN.md)
│   │   ├── traceability/              # Traceability matrix (REQ → TC → Execution)
│   │   ├── metrics/                   # Token usage, agent metrics
│   │   └── reports/                   # Final STLC report + HTML
│   │
│   ├── general/                       # Shared cross-story artifacts (future)
│   └── .mcp-validated                 # Marker file (MCP validation status)
│
├── product_release_dashboard/         # Application under test (sample)
│   ├── index.html                     # Main UI
│   ├── styles.css                     # Styling
│   ├── script.js                      # Business logic (main application)
│   └── README.md                      # Feature documentation
│
├── docs/                              # Documentation
│   ├── architecture.md                # Core architecture reference
│   ├── HOOKS-CONFIGURATION.md         # Hook setup guide
│   ├── HOOKS-ACTIVE-CONFIGURATION.md  # Current hook status
│   ├── ARCHITECTURE-COMPLIANCE-AUDIT.md
│   └── codemie/                       # CodeMie training docs
│
├── scripts/                           # Root-level utility scripts (if any)
├── .env.example                       # Template for MCP credentials
├── .env                               # Actual MCP credentials (git-ignored)
├── .mcp.json                          # MCP server configuration (Atlassian)
├── .gitignore                         # Git ignore rules
└── .vscode/                           # VS Code settings
```

### Key Artifact Generation Outputs (Per Story)
- `artifacts/<story_id>/discovery/repository-discovery.md` — Repository technical baseline
- `artifacts/<story_id>/requirements/requirement-analysis.md` — Requirement decomposition
- `artifacts/<story_id>/test-planning/impact-analysis.md` — Impact classification
- `artifacts/<story_id>/test-planning/test-plan.md` — Test strategy & scope
- `artifacts/<story_id>/test-cases/test-case-inventory.md` — Manual test case registry
- `artifacts/<story_id>/reviews/test-case-review.md` — QA review of manual tests
- `artifacts/<story_id>/automation/framework-selection.md` — Framework recommendation
- `artifacts/<story_id>/automation/automation-plan.md` — Automation strategy
- `artifacts/<story_id>/traceability/traceability-matrix.md` — REQ↔TC↔Execution mapping
- `artifacts/<story_id>/execution/execution-summary.md` — Test run results
- `artifacts/<story_id>/execution/failure-analysis.md` — Root cause analysis
- `artifacts/<story_id>/self-healing/self-healing-report.md` — Auto-fix attempts
- `artifacts/<story_id>/defects/DEF-NNN.md` — Defect records (created if `create_external_defects: true`)
- `artifacts/<story_id>/reports/final-stlc-report.md` — Consolidated final report
- `artifacts/<story_id>/reports/stlc-report.html` — Interactive HTML report (auto-generated)
- `artifacts/<story_id>/metrics/agent-metrics.json` — Token usage by phase & agent

---

## Test Infrastructure

### Existing Test Directories
- **Detected**: None in current repository (this is a framework, not a target application)
- **Framework Support**: `tests/`, `test/`, `spec/`, `features/`, `e2e/` are all scanned during discovery

### Existing Test Frameworks
- **None configured in master_stlc repo** (framework is a test generation tool, not a test suite)
- **Supported for target repositories**:
  1. **Pytest** (Python unit/integration/UI/API/E2E)
  2. **Behave** (BDD with Gherkin)
  3. **Playwright** (Node/TypeScript E2E)
  4. **Cypress** (JavaScript E2E)
  5. **Selenium** (Python/Java cross-browser UI)
  6. **Jest** (JavaScript unit tests, detected but not fully configured)

### Test Command Patterns (Configured in frameworks.yaml)
| Framework | Run Command | Config File |
|-----------|-------------|------------|
| Pytest | `pytest tests/ -v` | `pytest.ini` |
| Behave | `behave` | `behave.ini` |
| Playwright | `npx playwright test` | `playwright.config.ts` |
| Cypress | `npx cypress run` | `cypress.config.js` |
| Selenium | `pytest tests/ -v` | `pytest.ini` |
| API | `pytest tests/ -v` | `pytest.ini` |

### Test File Naming Conventions (Configured)
- **Pytest**: `test_*.py` or `*_test.py` (feature-based: `test_form_submission.py`)
- **Behave**: `*.feature` files under `features/<feature_area>/`
- **Playwright**: `*.spec.ts` under `tests/<feature_area>/`
- **Cypress**: `*.cy.js` under `cypress/e2e/<feature_area>/`
- **Selenium**: `test_*.py` under `tests/<feature_area>/`

### UI / API / E2E / Unit Test Support
- **UI Testing**: Playwright, Cypress, Selenium, Behave (with browser drivers)
- **API Testing**: Dedicated `api` framework (pytest + requests/httpx)
- **E2E Testing**: Playwright, Cypress, Behave
- **Unit Testing**: Pytest (primary)
- **Integration Testing**: Pytest, Behave
- **Contract Testing**: API framework

### Test Artifact Path Resolution (Per frameworks.yaml)
Test files are placed relative to `<project_root>/<automation_root>/<test_root>/<feature_area>/`:
- **project_root**: Read from discovered target repository
- **automation_root**: Typically `automation` (relative to project root)
- **test_root**: Framework-specific (pytest: `tests`, behave: `features`, playwright: `tests`)
- **feature_area**: Feature name extracted from requirement (e.g., `form_submission`, `billing_api`)

### CI/CD Pipeline Detection
- **Supported**: GitHub Actions, GitLab CI, Jenkins, Azure Pipelines
- **Detection Pattern**: Scans `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `azure-pipelines.yml`
- **Current Repository**: No active CI/CD pipeline (this is a framework, not a deployable app)

### Existing Reporting Setup
- **Built-in Report Formats**:
  - Markdown (`final-stlc-report.md`)
  - JSON (`final-stlc-report.json`)
  - Interactive HTML (`stlc-report.html` — auto-generated post-reporting)
- **Report Sections**: Test execution summary, test group breakdown, defects, agent metrics (token usage by phase)
- **Report Features**: Dark/light mode, responsive layout, pass/fail/xfail tallies, pass rate

---

## Automation Frameworks

### Framework Selection Strategy
The `framework-selection-agent` uses the following logic:
1. **Requirement Analysis**: Identify test type (UI, API, unit, integration, E2E, BDD)
2. **Repository Discovery**: Detect existing frameworks, package.json, requirements.txt, go.mod, etc.
3. **Match to Framework**:
   - If requirement is "UI/E2E" and Playwright/Cypress dependencies exist → select Playwright or Cypress
   - If requirement is "API" → select API framework
   - If requirement is "BDD" and Behave/cucumber dependencies exist → select Behave
   - If requirement is "unit" and Python detected → select Pytest
   - Fallback: Pytest (most versatile)

### Framework-Specific Skill Libraries
Located in `.claude/skills/automation/`:

1. **pytest** (SKILL.md)
   - Supports: unit, api, integration, ui, e2e
   - Config file: `pytest.ini`
   - Run from: `automation` directory
   - Naming: feature-based (`test_*.py`)

2. **behave** (SKILL.md)
   - Supports: gherkin, functional, bdd
   - Config file: `behave.ini`
   - Feature files: `features/<feature_area>/*.feature`
   - Step definitions: `features/steps/*.py`

3. **playwright** (SKILL.md)
   - Supports: ui, e2e, browser
   - Config file: `playwright.config.ts`
   - Test files: `tests/<feature_area>/*.spec.ts`
   - Language: TypeScript/JavaScript

4. **cypress** (SKILL.md)
   - Supports: ui, e2e, browser
   - Config file: `cypress.config.js`
   - Test files: `cypress/e2e/<feature_area>/*.cy.js`
   - Language: JavaScript

5. **selenium** (SKILL.md)
   - Supports: ui, browser
   - Config file: `pytest.ini`
   - Test files: `tests/<feature_area>/test_*.py`
   - Language: Python

6. **api** (SKILL.md)
   - Supports: api, contract, integration
   - Config file: `pytest.ini`
   - Test files: `tests/<resource_area>/test_*.py`
   - Language: Python
   - Libraries: requests, httpx

### Test Generation Patterns
- **Manual Tests** (generated by manual-test-generation-agent): `.feature` files in `<project_root>/manual/<feature_area>/`
- **Automated Tests** (generated by automation-generation-agent): Framework-specific files in `<project_root>/automation/<test_root>/<feature_area>/`
- **Traceability IDs**: All tests tagged with `REQ-NNN` (requirement → test case → execution mapping preserved end-to-end)

---

## Entry Points and Services

### STLC Pipeline Entry Points (Commands)
| Command | Purpose | User Input | Output |
|---------|---------|-----------|--------|
| `/0-setup-mcp` | Initialize MCP (Atlassian) | Credentials | `.env`, `.mcp.json` validated |
| `/1-stlc <story>` | Full pipeline | Story ID/requirement text | Complete STLC execution |
| `/2-stlc-plan <story>` | Planning only | Story ID | Test plan + manual tests |
| `/3-stlc-automate` | Automation generation | (uses previous state) | Automation framework files |
| `/4-stlc-run [scope]` | Execution + analysis | Test scope (smoke/regression/all) | Execution report + failure analysis |
| `/5-stlc-heal` | Self-healing retry | (uses previous failure data) | Self-healing report |
| `/6-stlc-report` | Final reporting | (uses all previous artifacts) | Final report + HTML + metrics |

### Application Entry Points (Release Dashboard)
- **Entry Point**: `product_release_dashboard/index.html` (opens in browser)
- **Application Type**: Single-page application (SPA), no server required
- **Key Features**:
  - Create release notes (form submission)
  - Display release list (read from localStorage)
  - Filter by product name
  - Filter by breaking/non-breaking changes
  - Search by title/description
  - Edit/delete releases
  - Export to CSV
  - Import from JSON
- **Data Persistence**: Browser localStorage (no backend API)

### Key Application Functions (from script.js)
- `addRelease()` — Form submission & validation
- `displayReleases()` — Render release list
- `filterReleases()` — Apply product/breaking filters
- `editRelease()` — Populate form for editing
- `deleteRelease()` — Remove release
- `exportCSV()` — Export releases as CSV
- `importJSON()` — Load releases from JSON file
- `updateProductFilter()` — Dynamically populate product selector

### Services & APIs
- **No backend services** — This is a pure frontend application
- **External API Integration**: None (localStorage only)
- **MCP Services** (for STLC pipeline):
  - Atlassian Jira API (via mcp-atlassian) — create defect tickets
  - Atlassian Confluence API (via mcp-atlassian) — publish reports

---

## Configuration Files

### Runtime Configuration

| File | Purpose | Location | Permissions Gate |
|------|---------|----------|------------------|
| `.claude/config/stlc-config.yaml` | Permissions, execution limits, integrations | Core config | All phases |
| `.claude/config/frameworks.yaml` | Framework definitions (pytest, playwright, etc.) | Core config | Framework selection |
| `.mcp.json` | MCP server endpoints & credentials | Project root | Pre-task hook |
| `.env` | MCP credentials (Jira/Confluence) | Project root (git-ignored) | PreToolUse hook |
| `.env.example` | Credential template | Project root (tracked) | Setup guide |

### stlc-config.yaml Sections
```yaml
stlc:
  project_name: "Generic Claude STLC Project"
  pipeline_version: "1.0.0"

permissions:
  create_external_defects: false   # Gate: Jira ticket creation
  create_pr: false                 # Gate: GitHub PR creation

integrations:
  github:
    create_pr: false               # Must match permissions.create_pr

execution:
  require_user_scope: true         # Prompt for test scope before /4-stlc-run
  max_reruns: 2
  max_self_healing_iterations: 2

state:
  file: "artifacts/{story_id}/state/stlc-state.json"
  auto_resume: true
```

### State File (stlc-state.json)
```json
{
  "story_id": "COD-7",
  "pipeline_id": "COD-7-2026-11-03",
  "created_at": "2026-11-03T00:00:00Z",
  "current_phase": "repository_discovery",
  "completed_phases": [],
  "failed_phases": [],
  "artifacts": {},
  "config": { ... }
}
```

### Hook Configuration (hooks.json & settings.json)
- **Pre-task hooks**: MCP bootstrap, state validation, safety checks
- **Post-task hooks**: Artifact validation, token metrics, HTML report generation, traceability validation
- **Stop hooks**: Final artifact validation, token usage report, HTML report generation
- **Pre-agent hooks** (settings.json): Run `pre-agent-check.py` before Agent tool invocation
- **Post-agent hooks** (settings.json): Log agent model usage via `log-agent-model.py`

### Release Dashboard Configuration
- **No external config files** — Configuration hardcoded in `script.js`
- **Configurable at runtime** (HTML form):
  - Product name, version, title, description, release date, breaking change flag

---

## Naming and Coding Conventions Observed

### Artifact Naming
- **Story ID**: `COD-NNN` (e.g., `COD-7`)
- **Requirement ID**: `REQ-NNN` (e.g., `REQ-001`)
- **Test Case ID**: `TC-NNN` (e.g., `TC-001`)
- **Defect ID**: `DEF-NNN` (e.g., `DEF-001`)
- **Agent Files**: `NN-descriptive-name.md` (numbered in pipeline order)
- **Skill Files**: `<domain>/SKILL.md` with README.md
- **Template Files**: `<purpose>.md`

### File Naming Patterns
- **Agents**: `<number>-<agent-name>.md` (e.g., `2-repository-discovery-agent.md`)
- **Commands**: `<number>-<command-name>.md` (e.g., `1-stlc.md`)
- **Artifact outputs**: `<phase>-<type>.md` (e.g., `test-plan.md`, `failure-analysis.md`)
- **Test files**: Framework-dependent (pytest: `test_*.py`, behave: `*.feature`, playwright: `*.spec.ts`)

### Directory Naming
- **Kebab-case** for multi-word directories (e.g., `product-release-dashboard`, `test-planning`, `failure-analysis`)
- **Underscore_case** for Python packages (e.g., `automation_root`, `test_root`)
- **Acronyms in caps** (e.g., `.claude`, `MCP`, `STLC`, `E2E`)

### Markdown Conventions
- **Frontmatter**: YAML frontmatter in agent/command definitions (name, description, tools, model)
- **Sections**: H2 headers for major sections, H3 for subsections
- **Code blocks**: Fence with triple backticks, specify language (bash, yaml, json, python)
- **Tables**: Markdown tables for structured data
- **Links**: Absolute paths to config files, relative to repo root

### Python Conventions
- **Script location**: `.claude/scripts/` for all utility scripts
- **Naming**: Snake_case (e.g., `pre-agent-check.py`, `token-usage.py`)
- **Imports**: Standard library first, then third-party (Claude tools), then local
- **Error handling**: Try/except with descriptive error messages

### JSON Conventions
- **State files**: camelCase keys (e.g., `story_id`, `current_phase`, `completed_phases`)
- **Config files**: snake_case or YAML (framework definitions use YAML)
- **Metrics files**: camelCase keys (e.g., `totalTokens`, `phaseBreakdown`)

---

## Risks and Unknowns

### Known Limitations
1. **No Active CI/CD**: This repository contains framework code only; no active CI/CD pipeline is configured for the framework itself.
2. **MCP Credentials Exposed**: `.mcp.json` contains plaintext Atlassian credentials (API token visible in git history). **Risk**: Credential compromise. **Mitigation**: Rotate API token, move to `.env` (partially done but `.mcp.json` still tracked).
3. **No Target Repository**: Framework is designed for integration into external repos; current `product_release_dashboard/` is a minimal sample app.
4. **Model Costs**: Full pipelines invoke multiple Claude models (Haiku, Sonnet, etc.); no token budget enforcement.
5. **Framework Selection**: Automated framework selection may not always match user intent; requires user confirmation when ambiguous.

### Unknowns & Assumptions
1. **Python Version**: No explicit Python version pinned; assuming 3.8+
2. **Node.js Version**: Playwright/Cypress assume Node.js 16+ available in target environment
3. **Browser Dependencies**: Playwright/Cypress require browser binaries (Chrome, Firefox, etc.); installation not automated
4. **Test Data**: No test data management strategy defined; each framework will need its own fixtures
5. **Parallel Execution**: Frameworks may support parallel test runs, but orchestrator does not yet implement concurrency
6. **Cross-Repository Integration**: Framework assumes target repo is a git clone; no support for monorepos or multi-repo strategies
7. **Artifact Retention**: No automated cleanup of old pipeline runs; `artifacts/` can grow unbounded
8. **Permission Model**: Permission gates are configuration-based (yaml) but not runtime-enforced with user prompts beyond initial gate
9. **Self-Healing Scope**: Self-healing is allowed for `AUTOMATION_FAILURE` only; unclear if this includes test code vs. test data vs. environment issues
10. **Defect Lifecycle**: Defects created in Jira have no backlink to STLC artifacts; manual tracking needed

### Technical Risks
1. **Agent Context Windows**: Large test suites may exceed Claude token limits; no automatic test batching
2. **State File Corruption**: If `stlc-state.json` is manually edited, pipeline resumption may fail silently
3. **Circular Dependencies**: If self-healing fixes introduce new failures, infinite retry loop risk (mitigated by `max_self_healing_iterations`)
4. **Framework Conflicts**: Target repo may have conflicting test frameworks; orchestrator doesn't validate
5. **Artifact Namespace Collisions**: Multiple concurrent pipelines with same `story_id` will overwrite artifacts

### Operational Risks
1. **First-Run Setup**: MCP setup is required (`/0-setup-mcp`); if skipped, all MCP-dependent phases will fail
2. **Credential Rotation**: Atlassian API token in `.mcp.json` requires periodic rotation; no automated refresh
3. **Manual Intervention**: Pipeline has multiple approval gates; requires user attention for prod-critical decisions
4. **Test Flakiness**: Generated tests may be flaky; self-healing does not address root causes (environmental, concurrency, etc.)
5. **Documentation Lag**: Framework configuration (frameworks.yaml) may drift from actual target repo capabilities

---

## Summary

This is a **Generic, Reusable STLC Orchestration System** built on Claude AI agents. It is NOT a traditional application repository but rather a test automation framework generator and executor.

**Key Characteristics**:
- **Framework Type**: Test orchestration & automation framework
- **Primary Languages**: Python, JavaScript, YAML, Markdown
- **Test Frameworks**: Pytest, Behave, Playwright, Cypress, Selenium, API (configurable per target repo)
- **AI Integration**: Claude Haiku/Sonnet models, MCP for Atlassian (Jira/Confluence)
- **Deployment Model**: Integrated into target repositories (not standalone)
- **State Management**: JSON-based state file with resumable pipeline
- **Entry Points**: 6 slash commands (`/1-stlc` through `/6-stlc-report`)
- **Artifact Output**: Markdown, JSON, HTML (interactive reports)
- **Safety Gates**: Permission-based (create_external_defects, create_pr), execution scope confirmation
- **Self-Healing**: Automatic retry for AUTOMATION_FAILURE (not APPLICATION_FAILURE)

**Target Application**: `product_release_dashboard/` (Release Notes Dashboard) — a lightweight HTML/CSS/JavaScript SPA with localStorage persistence.

**Readiness**: Framework is fully structured; ready for integration into external target repositories to execute complete STLC pipelines.
