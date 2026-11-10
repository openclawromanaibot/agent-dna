# agent-dna

Instruction DNA (L0–L2) for the OpenClaw and Hermes agents. This repository is **public**:
publish only what is safe for anyone to read.

## Layout

```
L0-core.md              # shared root: principles, red lines, routing table
openclaw/L0-local.md    # host-specific routing rows (Windows)
hermes/L0-local.md      # host-specific routing rows (Debian)
common/instructions/    # L1/L2 shared by both agents
openclaw/instructions/  # L1/L2 specific to the OpenClaw host
hermes/instructions/    # L1/L2 specific to the Hermes host
```

Per agent, `L0-core.md` + its `L0-local.md` must stay within 3072 bytes.

## Never publish

Tokens, passwords, keys, IP addresses, e-mail, phone numbers, real user names and home paths,
chat IDs, personal data. Private values live in the agent's secrets store, `sharedMemory`
and local L3 — never here. Use placeholders such as `<user>`.

## Change flow

1. Branch from `dev`; never push to `dev`.
2. Open a PR into `dev`. The `gate` check must pass (allowlisted paths, secret/PII/hidden-text
   scan over every commit, L0 size budget).
3. The code owner approves. Protected-branch rules forbid direct pushes and force-pushes.
4. Agents pull `dev` and report "DNA updated, active from the next session".
