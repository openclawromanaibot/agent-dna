# Agent DNA rollout — MVP specification

## Purpose

Maintain reviewed L0–L2 instructions for OpenClaw (Windows) and Hermes (Debian) in a public repository. Delivery of new files does not by itself prove that an agent loaded or obeyed them.

## Repository layout

- `L0-core.md`: shared root principles and routing.
- `openclaw/L0-local.md`: Windows-specific root instructions.
- `hermes/L0-local.md`: Debian-specific root instructions.
- `common/instructions/*.md`: shared L1 indexes and L2 procedures.
- `openclaw/instructions/*.md`: OpenClaw-specific L1/L2.
- `hermes/instructions/*.md`: Hermes-specific L1/L2.

For each host, count UTF-8 bytes in the *contents* of `L0-core.md` plus `<host>/L0-local.md`; the sum must be at most 3072 bytes. L0 routes to relevant L1 indexes; L1 selects only the L2 procedures matching a task.

## Trust, permissions, and boundaries

Never publish secrets, personal identifiers, host-specific private values, runtime configuration, or local memory. Keep private L3 and credentials outside this repository.

Agents with explicitly authorized GitHub write access may publish changes to their own feature branches and open PRs targeting `dev`. Agents without that access prepare a local diff or Markdown change request; a trusted human or authorized publisher opens the PR. No agent directly pushes to `dev` or merges a PR. A human code owner reviews and merges.

The protected `dev` branch requires `gate` and code-owner approval. The gate checks every commit as well as the final tree.

Each host keeps the expected Git host, repository owner/name, and allowed remote transport in **host-private configuration**. Before fetching, compare the configured identity against the actual remote and reject mismatches or unapproved redirects. Do not embed credentials in URLs. Never publish the private trust configuration.

## Deployment paths and activation

- **Staging checkout**: isolated, non-active Git working directory used for fetch, inspection, and validation.
- **Active loader path**: the instruction source actually read by the agent at session startup, managed separately from staging.

A staging fast-forward must never change the active loader path. Activation is a separate, human-approved host integration operation, with its own verification and rollback procedure. Until that integration is implemented and tested, the MVP only stages a verified revision; it must not report that active instructions changed.

## Phase 1 — manual staging update

Trigger: a human explicitly requests an update on each host.

1. Verify the staging checkout, host-private trusted remote identity, and absence of uncommitted changes. Stop on unexpected files, local drift, or untrusted remote.
2. Fetch `dev` into staging without modifying active loader files. Pin the fetched commit ID (`target SHA`); record the current staging commit (`old SHA`).
3. Verify that `old SHA` is an ancestor of `target SHA` and that the target is reachable from the trusted fetched `dev`. Otherwise stop: no rebase, reset, force, or automatic conflict resolution.
4. **Before changing the staging checkout**, inspect the pinned target tree in an isolated temporary worktree or equivalent read-only Git tree inspection. Validate expected L0 and L1 paths, file types, and both per-host UTF-8 L0 byte totals. Fail closed on missing or malformed content.
5. Only after successful target-tree validation, fast-forward the staging checkout to exactly `target SHA`. Confirm its HEAD matches the pinned SHA. If this operation fails, report failure; do not touch the active loader path.
6. Report old SHA, target SHA, changed files, staging validation results, and the explicit state: "DNA staged at <target SHA>; active loader unchanged."

The active loader remains on its previous approved revision throughout this staging procedure, including any validation or update failure. A verified host integration may later activate a pinned staged revision for **the next session**, after separate approval and checks. Never claim the current session has hot-reloaded instructions.

## Phase 1 acceptance criteria

- Both hosts independently stage the same reviewed `dev` revision and report pinned commit IDs.
- A clean ancestor relationship is required; divergent or dirty staging state stops safely.
- Invalid target-tree content is rejected **before** staging checkout changes.
- Failures leave the active loader revision unchanged.
- Secrets, host configuration, and local memory remain untouched.
- Once the separately approved loader integration exists, a new session demonstrably reads the activated revision; staging alone is not accepted as proof of activation.
- Every failure has an explicit status, never a success message.

## Phase 2 — daily staging update

Enable only after Phase 1 is validated on both hosts and a human approves the schedule. Reuse exactly the same pinned-target validation and staging procedure. Do not introduce another updater, silent fallback, automatic activation, or conflict resolution. Stop and report any drift or failure.

## Out of scope

Direct edits to active host DNA, live hot-reloading, automated merges, automatic activation, secret distribution, private memory synchronization, and the separate behavioral error-correction workflow are not part of this delivery MVP.

## Rollout sequence

1. Human reviews and approves this specification.
2. Agents prepare migration change requests for existing L0/L1 content without private host values.
3. Authorized contributors publish content PRs; human code owner reviews and merges.
4. Human separately approves and implements host staging and loader integration.
5. Validate Phase 1 on both hosts, including next-session loader behavior, before considering Phase 2.
