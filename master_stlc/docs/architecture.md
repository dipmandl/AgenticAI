# Architecture Reference

Detail moved out of CLAUDE.md to keep the always-loaded context small. Read this file when you need architecture, layout, or configuration specifics.

## Layer separation

- **Orchestrator** (`stlc-orchestrator` agent / `scripts/stlc-orchestrator.py`) — sequences phases, manages state, enforces permission gates. Contains zero framework-specific logic.
- **Agents** (`.claude/agents/1-stlc-orchestrator.md` through `15-reporting-agent.md`) — numbered in pipeline order; each handles one STLC responsibility.
- **Skills** (`.claude/skills/`) — reusable domain knowledge loaded by agents. Framework-specific automation rules live under `.claude/skills/automation/{pytest,behave,playwright,selenium,cypress,api}/`.
- **Commands** (`.claude/commands/`) — user-facing entry points that invoke the orchestrator with a specific phase slice.
- **Templates** (`.claude/templates/`) — standardised Markdown schemas that every artifact-generating agent writes into.
- **Hooks** (`.claude/hooks/`) — deterministic lifecycle operations (pre-task validation, post-task artifact checks, safety guards, execution lifecycle).

## Artifact layout

Pipeline state is persisted in `artifacts/state/stlc-state.json` after every phase. The orchestrator reads this on startup and skips already-completed phases, making the pipeline resumable after interruption.

```
artifacts/
├── repository/        ← repository-discovery.md
├── requirements/      ← requirement-analysis.md
├── test-planning/     ← impact-analysis.md, test-plan.md
├── test-cases/        ← test-case-inventory.md
├── reviews/           ← test-case-review.md, automation-review.md
├── automation/        ← framework-selection.md, automation-plan.md
├── execution/         ← execution-summary.md, failure-analysis.md
├── self-healing/      ← self-healing-report.md
├── defects/           ← DEF-NNN.md (one per functional failure)
├── reports/           ← final-stlc-report.md, .json
├── metrics/           ← agent-metrics.md, .json
├── traceability/      ← traceability-matrix.md
└── state/             ← stlc-state.json
```

Artifacts are inputs to downstream agents via file paths — agents pass paths, not inline content, to keep context lean.

## Adding a new automation framework

Add a skill under `.claude/skills/automation/<framework>/README.md` and register the framework name in `.claude/config/frameworks.yaml`. The orchestrator discovers it through `framework-selection-agent` without requiring changes to the core pipeline.

## Configuration

`.claude/config/stlc-config.yaml` controls permissions, execution limits, and reporting:

```yaml
permissions:
  modify_existing_tests: false      # all false by default — change to enable
  modify_existing_automation: false
  modify_application_code: false
  install_dependencies: false
  create_external_defects: false

execution:
  default_scope: "impacted-tests"
  require_user_scope: true          # prompts before every run
  max_reruns: 2
  max_self_healing_iterations: 2
```

Model selection per phase is in `.claude/config/models.yaml`. Supported frameworks are listed in `.claude/config/frameworks.yaml`.

## Traceability

Every artifact links back through the chain: Requirement → Test Case → Automation → Execution → Defect. Stable identifiers follow the pattern `REQ-NNN` / `TC-NNN` and are preserved from Gherkin tags through to pytest marks (or framework equivalents). The traceability matrix at `artifacts/traceability/traceability-matrix.md` is the canonical cross-reference.

## Python orchestrator CLI

```bash
python scripts/stlc-orchestrator.py --help
python scripts/stlc-orchestrator.py                        # run full pipeline
python scripts/stlc-orchestrator.py --start-phase <name>  # resume from a phase
python scripts/stlc-orchestrator.py --dry-run             # propose workflow without writing
```

Valid `--start-phase` names: `repository-discovery`, `requirement-analysis`, `impact-analysis`, `test-plan`, `manual-test-generation`, `test-review`, `automation-generation`, `automation-review`, `execution`, `self-healing`, `reporting`.

## Token metrics

`python .claude\scripts\token-usage.py` computes per-phase and per-agent token usage from Claude Code transcripts and writes `artifacts/<story_id>/metrics/agent-metrics.md` + `.json`.

## Sliced pipeline runner (token-efficient full pipeline)

`python scripts/stlc-pipeline.py "<story>"` runs the whole STLC as four isolated slices (`/2-stlc-plan` → `/3-stlc-automate` → `/4-stlc-run` → `/6-stlc-report`), each in a fresh headless `claude` session — equivalent to `/clear` between slices, so no slice re-reads prior conversation history. Continuity comes from `artifacts/state/stlc-state.json`; approval gates are prompted by the script between slices. Flags: `--scope`, `--yes`, `--skip-permissions`. Token usage is computed automatically at the end.
