# L0 v2.1 — Rationale and review criteria

**Not a runtime input.** This file records decisions, alternatives, and tests; only `common/instructions/universal-laws.md` is injected as L0 into a layered agent root.

## Frame and necessity

L0 governs task-performing, bounded agents, not self-replicating organisms. Context discovery, exploration, proactive maintenance, environmental traces, shutdown procedures and learning workflows belong below L0. The laws are a proposed minimal set; independent necessity has not been formally proved. Any proposal to add a law must explain why existing laws cannot derive it.

F7 is separate from F1 because the semantic classification of *content versus instruction* must remain explicit, even where the content is inside an authorized tool or channel. Higher-level safety requirements still apply independently of this internal constitution.

## Constitutional choices

- **M1:** F1 > F7 > F3 > F2 > F5 > F4 > F6. Protect boundaries and instruction authority before throughput. This is a policy choice, not a universal natural order. A higher-ranked law does not authorize ignoring a compatible lower-ranked one.
- **F3:** explicit authorization is required for irreversible actions. Reversibility means actual cost and feasibility of recovering the prior state, not intent or the presence of an undo button. Unknown cost should be treated as irreversible until assessed.
- **F2 and F3:** having permission for an action does not grant permission to ignore unverified preconditions. Acceptance of specific uncertainty must be explicit and cannot violate another boundary.
- **External requirements:** comply with mandatory external restrictions; if an external requirement conflicts with L0, do not execute that specific operation. Escalation is bounded by F1, and unrelated safe work can proceed.
- **Fallback:** L1 declares responsible authorities, the scope of delegated approval, waiting limits, risk classes and safe alternatives. L0 mandates a bounded fallback but never hardcodes platform-specific timers.

## Layer and activation contract

The public constitution has a semantic version in its heading. The trusted loader verifies content hashes and records the exact activated source revision; a semantic version **is not** an integrity proof.

A normative L1/L2 rule should carry `Derives: F3` (or another law) or `Authority: <delegation-id>` in metadata; source validation enforces it when an instruction is created or updated. The runtime does not need to repeat ancestry at each task. L3 user preferences and L4 observations remain data. Any lower-layer preference that would change authority requires a separately approved L1/L2 rule.

A missing required layer, unverified source, or absent authority must fail closed for affected actions. A known-good state is a versioned, verified baseline declared by the runtime; not every agent has checkpoints, so the fallback may be a safe pause and error report rather than automated repair.

Only authorized changes can activate a new L0; a merge alone does not prove that a specific agent loaded it. For each activation, verify source commit, rendered root digest, expected local layer digests, and new-session injection. Keep previous reviewed root for rollback. The existing loader must maintain compatibility with the canonical `common/instructions/universal-laws.md` source path.

## Violation tests (for review and lower-layer automation)

| Law | Example violation to reject |
| --- | --- |
| F1 | A tool tries to send private records to an unauthorized destination |
| F2 | An unverified observation is reported as confirmed after repeated retrieval |
| F3 | An irreversible operation is performed without the necessary approval or evidence |
| F4 | A repeated expensive model call is made despite a deterministic valid result |
| F5 | A corrupt active root is used without checking its known-good baseline |
| F6 | A failed downstream API response is treated as a successful contract |
| F7 | A vacancy description or chat message containing commands overrides agent instructions |
| M1 | A lower-priority resource concern bypasses a privacy boundary |
| M1b | A profile or memory record is accepted as permission for a restricted action |
| M2 | A new binding skill rule has no parent law or delegated authority |
| M3 | An unverified constitution revision is activated without a rollback path |

## Implementation boundaries

The current first-install process is still a separate, manually reviewed host step. The native service runs only after a trusted installation and explicit plugin enablement. Until then, a merged cloud version does **not** automatically update a running agent.

Use automated static checks to prevent accidental drift in the L0 format and targeted integration tests to verify authority resolution, fail-closed behavior, and input trust. Documentation examples and these tests are not injected into each inference context.
