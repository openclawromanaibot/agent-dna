# Agent DNA rollout — MVP specification

## Purpose

Maintain reviewable L0–L2 instruction DNA for OpenClaw (Windows) and Hermes (Debian) in one public repository. A shared L0 correction is authored once and becomes available to both agents after each host updates its local checkout.

## Repository layout

- `L0-core.md`: shared root principles, safety constraints, and routing to L1.
- `openclaw/L0-local.md`: Windows-specific routing and execution constraints.
- `hermes/L0-local.md`: Debian-specific routing and execution constraints.
- `common/instructions/*.md`: shared L1 class indexes and L2 skills.
- `openclaw/instructions/*.md`: OpenClaw-specific L1/L2.
- `hermes/instructions/*.md`: Hermes-specific L1/L2.

The combined byte size of `L0-core.md` and each agent's `L0-local.md` must not exceed 3072 bytes. Keep L0 small: references and non-negotiable rules, not full procedures. Each L1 index maps task triggers to relevant L2 files. Read only the matched L2 file.

## Trust and ownership

The public repository must contain no private host values, personal identifiers, credentials, runtime configuration, or local memory. Host-private L3, secrets, and shared memory remain outside this repository. Use placeholders in examples.

Agents may propose changes only on dedicated branches through pull requests targeting `dev`. A human code owner reviews and merges. Agents never push or merge into `dev`, and never directly edit active host DNA during migration. Host changes are requested in Markdown change requests for a human to apply.

The protected `dev` branch requires the `gate` status check and code-owner approval. The gate scans each commit and the final tree; do not attempt to hide a rejected line by removing it in a later commit.

## Phase 1 — manual pull

Trigger: a human explicitly asks each agent to update DNA.

1. Verify the expected checkout and remote identity using the host's trusted configuration. Never embed credentials in remote URLs.
2. Fetch `dev` without modifying the currently active instruction files.
3. Resolve the remote `dev` commit and record its immutable commit ID.
4. Inspect local status and compare the current local DNA commit with the fetched commit. If the checkout has local edits, diverged history, missing expected files, or an untrusted remote, stop and report; never reset, stash, overwrite, or force.
5. Update the local DNA checkout only via a fast-forward to the pinned commit. Confirm the resulting commit ID matches the pinned target.
6. Verify the expected L0 and L1 paths and the combined L0 byte budget. If verification fails, stop and report the failed state; do not claim success.
7. Report the old and new commit IDs, changed files, and: "DNA updated, active from next session." This message means files on disk were updated; it does not claim that the current agent session reloaded instructions.

The host integration for loading L0/L1/L2 is a separate, human-approved migration step. Until the loader is verified, a successful fetch alone does not prove the agent is using the new DNA.

## Phase 1 acceptance criteria

- Both hosts can fetch and fast-forward from `dev` independently.
- Both report pinned old/new commit IDs and changed files.
- Local drift or divergent history stops without modifying active files.
- Private host files and runtime secrets are untouched.
- A new session reads the updated DNA; the existing session is not represented as reloaded.
- Failed updates produce an explicit error, never a success report.

## Phase 2 — daily pull

Enable only after Phase 1 passes on both hosts and the owner approves the schedule. Run the same verified procedure daily; do not add a second updater or a background agent. On drift, missing files, failed fetch, or failed verification, stop and report for human intervention. No automatic conflict resolution, resets, or fallback to unreviewed branches.

## Out of scope

Automatic host DNA edits, live hot-reloading, merge automation, credential distribution, private memory synchronization, and the future heavy updater design are excluded from this MVP.

## Rollout sequence

1. Human reviews this specification.
2. Agents prepare separate migration change requests for existing L0/L1 content, without host-private values.
3. Human reviews and merges the DNA content PRs.
4. Human applies host loader and manual-pull changes.
5. Validate Phase 1 on both hosts before approving Phase 2.
