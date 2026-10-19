---
description: Bootstrap the local Atlassian MCP connection for this project. IMPORTANT: Invoke ONLY when the user explicitly types this slash command.
---

# setup-mcp Command

## Purpose
Install the Atlassian MCP server, collect Jira and Confluence credentials into a local `.env` file, and verify that Claude can discover the project MCP entry.

## What this command should do
1. Run `./scripts/setup-mcp.ps1` from the repository root.
2. Tell the user that the script creates a gitignored `.env` file in the repo root.
3. After the script finishes, tell the user to restart Claude Code or open a fresh terminal.
4. Ask the user to run `claude` once in this project and approve the `atlassian` MCP server if it is shown as pending.
5. Run `claude mcp list` and report whether `atlassian` is `Connected`, `Pending approval`, or failed.

## Usage
```
/setup-mcp
```

## Output
- Local `.env` file with Jira and Confluence credentials
- Installed `mcp-atlassian` user package
- `claude mcp list` status summary

## Safety
- Do not print or echo secrets back to the chat.
- Do not write credentials into tracked project files.
- Stop and tell the user if the script prompts for secrets that must be entered directly.