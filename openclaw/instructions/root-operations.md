# OpenClaw operational guardrails

## Infrastructure and execution
- Correct syntax errors and local command mistakes independently within the authorized task.
- On access, authentication, connection or infrastructure failure: report exactly what failed and why, then wait. Do not try alternate endpoints, guess credentials or bypass restrictions.
- After two failed infrastructure attempts involving disk search, git or hooks, stop and report: "Done and verified: <what>. Blocked on: <X>. Tried: <A>, <B>. Options: <1 recommended>, <2>."

## Git workspace hygiene
- Never leave browser profiles, cookies, sessions, logins, keys, tokens, secrets, personal reports, contacts, messages, memory/instruction backups, scratch files or service files in the repo root or tracked folders.
- Exclude sensitive files immediately, preferably using `.git/info/exclude`, or move them outside the repository.
- After creating files or directories, check whether `git add -A` would include sensitive content; fix exclusions before staging.
- Secrets and keys must never live in the workspace, even when ignored; keep them in the designated external secrets store.
- Make `git add -A` safe by default. Treat any unignored sensitive content as a critical failure.
- Never commit personal names, email addresses, phone numbers, profile links, credentials or tokens; follow the code-class privacy rules.

## Learning
- AGENTS.md is read-only to the agent. Never append lessons, examples or temporary details.
- First search for an existing rule and refine it instead of adding a duplicate.
- Work-class rule: `instructions/<class>/index.md`.
- Commands or ordered steps: the appropriate skill and its normal editing mechanism.
- Facts, IDs, dates and incidents: local learnings or shared memory.
- Principle, red line or routing change: propose exact wording to the owner before changing cloud DNA.
- If no class fits, use `instructions/ops/index.md` or ask.

## Related
- The OpenClaw workspace contract: `/concepts/agent-workspace`.
- Private host identifiers, paths and endpoints: `instructions/FACTS.md`.
