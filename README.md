# agent-dna

A public, reusable **universal agent constitution**. DNA is the top abstraction:
it defines the structural laws and boundaries of an agent system, not the
preferences, role, host configuration, procedures or memories of an individual
agent.

Read [the layer contract](common/instructions/dna-layer-contract.md) before
editing or deploying DNA.

## Target layering

| Layer | Owner | Contents |
| --- | --- | --- |
| L0 DNA | This reviewed public repository | Universal invariants, hierarchy and safe change rules |
| L1 Agent | Each agent | Role, capabilities, runtime and routing |
| L2 Skills | Each agent / approved skill library | Procedures and workflows |
| L3 Profile | Private/local profile | User preferences, response language, host settings |
| L4 Memory | Memory store | Facts, history and lessons |

The runtime may compose one active `AGENTS.md` from several layers; this is
not permission to store every layer in the public DNA repository.

## Current migration state

The existing `L0-core.md`, `openclaw/L0-local.md`,
`openclaw/instructions/root-operations.md` and
`common/instructions/user-communication.md` are **legacy inputs** to the
current OpenClaw installer. Some contain agent-specific or profile-level rules.
They are retained temporarily to avoid breaking that installer. The migration
plan and restrictions are recorded in
[the layer contract](common/instructions/dna-layer-contract.md).

Do **not** run the existing cloud-root replacement as the final architecture.
Update the installer to compose verified DNA plus private agent/profile layers
first, and verify that no behavior or local configuration is lost.

## Never publish

Never commit personal data, identifiers, secrets, keys, tokens, passwords,
addresses, host paths, individual preferences or private profile/memory records.
All instructions in this public repository must be in English.

## Change flow

1. Create an owned feature branch from fresh `dev`, never write to `dev` directly.
2. Open a PR to `dev`; require the `gate` checks (paths, secrets, hidden text,
   size budgets) and review.
3. Publish only reviewed structural rules; do not treat publication as proof of
   successful local activation.
4. Apply changes through a verified loader with backup, drift protection and
   rollback, then confirm the active runtime actually loaded them.
