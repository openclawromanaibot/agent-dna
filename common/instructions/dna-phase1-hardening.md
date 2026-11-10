# Phase 1 hardening — pre-implementation acceptance contract

Status: proposed addendum to `common/instructions/dna-rollout.md`. This document does not authorize installation, activation, or scheduling on either host.

## 1. Exact target identity

The updater must read the fetched `refs/remotes/origin/dev` commit ID and pin that exact SHA. The validated tree, the staged checkout HEAD after fast-forward, and the reported target must refer to the same SHA. Checking only that a commit is reachable from `dev` is insufficient: an older ancestor is not the pinned target.

## 2. Byte accounting and line endings

Measure the exact Git blob bytes of `L0-core.md` and `<host>/L0-local.md` in the pinned target tree, as UTF-8, separately for both hosts. Each pair must total at most 3072 bytes. Reject non-UTF-8, unexpected byte-order marks, and ambiguous encodings. Define and test a single line-ending policy: LF in Git blobs; verify that Windows checkout conversion cannot cause the loader to read a different byte representation without detection. The measured object is the committed blob, not a platform-dependent text string.

## 3. Validate before moving HEAD

Use read-only tree inspection or an isolated temporary worktree to validate the pinned target's complete required file set, types, encoding, path routing, and L0 budgets. Do not mutate the staging checkout until all checks pass. Never run scripts from the candidate tree as part of validation.

## 4. Fast-forward invariants

Require a clean staging checkout and prove the current staging HEAD is an ancestor of the pinned target. Reject detached HEAD, unexpected branches, divergence, untracked collisions, and local modifications. Only fast-forward to the pinned SHA; confirm exact SHA equality after the operation. No reset, force, stash, merge commit, or automatic rebase.

## 5. Crash and recovery

Record the intended transition (old SHA, pinned target SHA, validation result) outside the active loader path before moving staging HEAD. After a crash or partial failure, inspect the actual staging HEAD and journal; reconcile only known states (old SHA or exact target SHA). For any other state, stop and request human intervention. Never claim success based solely on the journal. Active loader revision remains unchanged regardless of staging recovery.

## 6. Remote and tool trust boundary

Keep the allowlisted Git host, owner/repo identity, transport, and trusted updater executable/configuration outside the public DNA checkout, in host-private owner-controlled locations. Verify the remote against that policy before fetch; reject unexpected redirects and changed origin URLs. The updater must not source executable code, hooks, aliases, or configuration from the fetched tree. Pin the updater implementation separately and restrict its permissions.

## 7. Active loader isolation

The staging checkout and the active loader path must be physically and logically separate. A staging update may not modify symlinks, junctions, mounts, or paths used by the active loader. Activation requires a separate explicit human-approved operation with an independently validated target and a documented rollback to the prior active revision.

## 8. Activation evidence

A staging report must say `staged`, never `active`. After authorized activation, start a fresh agent session and capture non-sensitive evidence that its loader read the expected pinned revision (for example, a loader-produced revision marker plus an observable routing smoke test). A Git HEAD check alone does not prove the agent used the instructions. Do not include private host paths or user identifiers in published evidence.

## 9. Failure matrix and regression tests

Before Phase 1 rollout, exercise at least: invalid UTF-8, CRLF conversion mismatch, missing L0/L1, oversized L0, unexpected remote, non-descendant target, dirty checkout, unexpected HEAD, target changed between fetch and use, validation failure, crash before/after FF, and loader activation failure. For every negative case, assert no active loader change and an explicit failure status. For the positive case, assert exact target SHA and next-session activation evidence only after separately approved activation.

## Review boundary

These are nine proposed acceptance areas synthesized from the review summary, **not** a verbatim reconstruction of an unpublished numbered review. The owner/reviewer must confirm whether any intended requirements are missing before authorizing Phase 1.
