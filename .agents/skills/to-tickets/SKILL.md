---
name: to-tickets
description: Divide an approved specification or discussion into verifiable implementation tickets with explicit dependencies. Publish only when authorized.
disable-model-invocation: true
---

# Divide work into tickets

Read the [project workflow](references/project-workflow.md) and [workflow policy](../orchestration/references/workflow-policy.md).

## Gather the requirements

Read the source specification and relevant comments. Inspect enough code to establish the current behavior and likely integration points. Preserve unresolved decisions instead of filling them in silently.

## Propose verifiable increments

Each ticket should deliver a useful behavior or establish a necessary independently checkable prerequisite. Prefer a narrow end-to-end capability over completing every file in one layer first. Do not invent a UI for a library or a database for a pure transformation.

State only real dependencies. Explain the observable result, scope, constraints, and acceptance checks for each ticket. Keep tickets small enough for a fresh worker to understand from their references.

Wide mechanical migrations may use an expand, migrate, contract sequence. Name the temporary compatibility behavior and its removal condition. If changes cannot remain independently usable, name the integration checkpoint where they must work together.

Present the proposed breakdown and dependencies for approval unless the user already approved them. Ask about unresolved scope or meaningful granularity choices, not facts available in the repository.

## Record the tickets

Use one local file per ticket, or the configured tracker when publication is authorized. Preserve the parent specification. Do not close or rewrite parent issues as a side effect of ticket creation. Use configured labels and native blocking relationships where supported; otherwise record dependencies explicitly.

Each ticket contains:

- Title and source specification reference.
- Behavior or prerequisite to deliver.
- Constraints and exclusions.
- Acceptance checks.
- Blocking tickets and why they block it.
- Agreed status.

Paths and code examples are allowed when they clarify a contract; include revisions for claims about existing code. Do not copy entire source files into tickets.

## Execution handoff

Ticket dependencies describe when a result is available, not merely when an agent has finished writing it. [implement-spec](../implement-spec/SKILL.md) translates them into Orca implementation and integration-and-verification tasks. Dependent code must wait for successful integration when it needs another ticket's implementation.

This command creates planning artifacts, not Orca Runs or workers. Report the approved breakdown, artifact references, and any remaining decisions.
