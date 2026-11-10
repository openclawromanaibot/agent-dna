# Task: Export current agent instructions for DNA migration

**Execution mode: read-only.** This is a task document, not a persistent instruction or permission to change the host. Execute only when the human owner explicitly requests this export. Applies independently to OpenClaw (Windows) and Hermes (Debian).

## Objective

Produce a sanitized inventory and archive of the instructions currently used by your runtime. The output will be reviewed before any content is proposed for the public Agent DNA repository. Do not modify, install, reload, or publish active instructions.

## 1. Discover and classify

Identify, without modifying them:

- L0: root and startup instructions, such as `AGENTS.md`, `SOUL.md`, or equivalents.
- L1: indexes, routing tables, skill registries, and task-trigger mappings.
- L2: referenced skill procedures and supporting instruction files.
- Loading behavior: startup versus dynamic loading, precedence, missing-file handling, and dependencies.

Classify every item as **confirmed active**, **available but not confirmed active**, or **legacy/unused**. Cite the local evidence for each classification in the report; do not infer activation from file existence.

## 2. Build a sanitized export

Create a new output directory outside active instruction paths:

```text
agent-dna-export/
  manifest.md
  loading-map.md
  migration-notes.md
  L0/
  L1/
  L2/
```

Preserve safe relative filenames and hierarchy where possible. In `manifest.md`, list each exported file's relative path, sanitized original logical location, L0/L1/L2 level, activity classification, evidence, and referenced dependencies. Record excluded files by purpose only, without private details.

In `loading-map.md`, distinguish observed runtime loading from inference, including when a new session is required. In `migration-notes.md`, document duplicates, contradictions, oversized roots, obsolete references, missing dependencies, shared candidates, and host-only requirements. Do not silently reconcile or rewrite source rules.

## 3. Mandatory privacy and safety

Assume the export might later be shared publicly. Never include credentials, private keys, environment files, private memory, conversation history, user profiles, personal names, emails, phone numbers, chat identifiers, network addresses, absolute home paths, or host-specific secrets. Do not copy full configuration files when only a small instruction excerpt is needed.

Replace private values with clear placeholders such as `<USER>`, `<HOST>`, `<PRIVATE_PATH>`, and `<SECRET>`. Exclude any file that cannot be reliably sanitized. Do not follow symlinks outside the intended instruction scope.

Scan the final output, including filenames, manifest metadata, and archive entries, for sensitive content. If a safe scan cannot be completed, do not produce a shareable archive; report the blocker.

## 4. Package

Create `agent-dna-export-openclaw.zip` or `agent-dna-export-hermes.zip` as appropriate. Include only sanitized Markdown or plain text. No executables, binaries, symlinks, logs, databases, or unredacted originals. If archive creation is unavailable, provide the sanitized directory and say so.

## 5. Final report

Report the runtime name and verified version (if available), counts of exported L0/L1/L2 files, excluded file count, duplicates/conflicts, missing or unverified dependencies, output archive location, privacy scan outcome, and confirmation that active files were not modified.

## Boundaries

- Read-only discovery; write only to the new export output directory.
- No Git commits, pushes, PRs, or merges.
- No changes to active DNA, configuration, skills, memory, or runtime.
- No loader installation, synchronization, or scheduling.
- No publication of the archive to GitHub or another remote.
- Stop after the export and await human review.

Reference architecture: `common/instructions/dna-rollout.md` and `common/instructions/dna-phase1-hardening.md`.
