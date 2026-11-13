# Universal Agent DNA: constitution and layer contract

## Definition

Agent DNA is the highest, reusable abstraction: the laws of an agent system, not a description of any individual agent. Like physical laws, DNA constrains how components interact without prescribing the particulars of any one component.

DNA must be portable across hosts, models, roles, users and operating systems. It defines **structure and invariants**, not task choices, runtime settings or personal preferences.

## Layer boundaries

| Layer | Responsibility | Examples | Authority |
| --- | --- | --- | --- |
| L0 — DNA | Universal invariants, hierarchy, boundaries and change protocol | Lower levels cannot override higher levels; changes need validation; unknown state fails safely | Shared, reviewed constitution |
| L1 — Agent | Agent identity, role, environment capabilities and task routing | OpenClaw or Hermes adapter, available classes, host-specific instruction entry points | Agent-local configuration |
| L2 — Skills | Reusable procedures and executable workflows | Git workflow, review checks, deployment and recovery | Agent-owned skills |
| L3 — Profile | User and host preferences and local settings | Preferred language, response style, file paths, runtime schedules | Local/private profile |
| L4 — Memory | Observations, factual history and lessons | Previous incidents, evidence, dates, learned constraints | Memory store |

Layers are conceptual, not required filenames or physical directories. Profile and memory are different concerns even if a product stores them in one database.

## DNA invariants

1. Higher layers establish constraints; lower layers can refine but never override them.
2. Each instruction has one owning layer; route changes to that layer instead of copying text across layers.
3. A task is routed through the applicable agent's capabilities and procedures before acting; the universal DNA does not enumerate those capabilities.
4. An agent must distinguish known facts, verified state and unknown state; report failures rather than invent results.
5. Side effects must respect authorization, data boundaries and the host's own security model.
6. Changes to active instructions require provenance, validation, rollback and protection against accidental overwrites.
7. Agent-specific choices and user preferences belong below DNA, even when they are widely shared by current deployments.
8. DNA must not contain personal identities, credentials, host paths, OS commands, concrete job-search classes or preferred languages.

## Composition and runtime

Each runtime may expose one active root document such as `AGENTS.md`. **One runtime file does not mean one source layer.** A trusted installer may compose it from the universal constitution plus the agent's approved lower-layer inputs.

The loader must identify the provenance of each section and protect agent-owned content from destructive replacements. Cloud DNA revisions are not authority to overwrite unrelated local profile or memory.

The universal constitution should be small and stable. Application procedures and templates are extensions, not mandatory DNA.

## Compatibility and required migration

The current `L0-core.md`, `openclaw/L0-local.md`, `openclaw/instructions/root-operations.md` and `common/instructions/user-communication.md` reflect an earlier combined-root design. They include agent routing and communication preferences, so **they do not yet satisfy this contract**.

The existing `job-search-automation` installer composes those four files into one active `AGENTS.md`. Do not delete, rename or substantially rewrite its required inputs before updating that installer and verifying the migration path.

Migration order:
1. Establish this universal layer contract and identify which current rules are structural versus agent/profile/skill content.
2. Update the installer and self-healing checks to separate trusted universal DNA from local, approved agent/profile inputs.
3. Test complete composition, local drift detection, backups, rollback and fresh-session injection.
4. Move the existing agent rules and communication policy to their owning layers without losing behavior.
5. Retire the legacy cloud paths in a separately reviewed transition.

Until the migration is complete, **do not activate the old cloud root on a new agent solely because its files pass SHA verification**. Content integrity is not architectural validity.
