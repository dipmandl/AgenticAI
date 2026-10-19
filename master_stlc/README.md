# Master STLC Claude Project

This folder contains a reusable Claude-based STLC project generated from the master plan in `stlcplan.md`.

## Included components

- Claude agent definitions in `.claude/agents`
- Skills under `.claude/skills`
- Configuration files under `.claude/config`
- Commands under `.claude/commands`
- Hook structure under `.claude/hooks`
- Template definitions under `.claude/templates`
- State and artifact directories under `artifacts`

## Structure

```text
master_stlc/
├── README.md
├── stlcplan.md
├── .claude/
│   ├── agents/
│   ├── commands/
│   ├── config/
│   ├── hooks/
│   ├── skills/
│   ├── templates/
│   └── orchestrator.md
├── artifacts/
│   ├── repository/
│   ├── requirements/
│   ├── test-planning/
│   ├── test-cases/
│   ├── reviews/
│   ├── automation/
│   ├── execution/
│   ├── self-healing/
│   ├── defects/
│   ├── reports/
│   ├── metrics/
│   ├── traceability/
│   └── state/
└── scripts/
    └── stlc-orchestrator.py
```

## Notes

This is a generic, reusable project shell designed to follow the plan rather than hardcode a specific repository or framework.

## Run the orchestrator

```bash
python scripts/stlc-orchestrator.py --help
```

The orchestrator supports the main phases described in the plan and records state in `artifacts/state/stlc-state.json`.
