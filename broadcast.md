# Agent DNA Broadcast v1

Channel: `agent-dna/dev/broadcast.md`
Protocol: `common/instructions/broadcast-protocol.md`

This document is a **task announcement**, not a trusted runtime configuration or authorization to change active instructions. Reading it does not imply execution. Agents must follow the protocol, their local trust policy, and the explicit permissions granted by their human owner.

## Current announcement

- ID: `dna-export-2026-11-10-v1`
- Audience: `openclaw,hermes`
- Status: `proposed`
- Task: `common/tasks/export-dna.md`
- Execution: `read-only`
- Approval: `explicit-human-approval-required`
- Report destination: `private-issue`
- Artifacts: `local-only`

## Agent action

On the daily poll, validate this announcement and record its ID and the pinned broadcast commit SHA. Do not run the export automatically. If the owner explicitly authorizes this task, read the task from the **same pinned commit**, perform only its read-only actions, and report a sanitized status in the preconfigured private GitHub issue. Never upload instruction archives to this public repository.

If the private issue destination or access permissions are not configured, report the blocker locally. Never create a public issue as a fallback.

The task ID is stable for this announcement. Do not repeat an already completed task merely because the file was fetched again.
