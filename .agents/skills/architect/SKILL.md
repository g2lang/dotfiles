---
name: architect
description: Compare caller-first interface designs for a substantial change. Produce a recommendation and stop before implementation unless it is explicitly authorized.
disable-model-invocation: true
---

# Architect

Use [codebase-design](../codebase-design/SKILL.md) for interface guidance and the [workflow policy](../orchestration/references/workflow-policy.md) for delegation and permissions.

## 1. Establish the design question

State the behavior to support, constraints, affected callers, and decisions already approved. Inspect the relevant implementation and tests directly. Read focused Git history or project decisions when the existing shape needs explanation. Greenfield work needs no invented history.

Produce a short common brief. Mark unknown facts separately from product choices. Resolve facts with inspection or a bounded experiment; ask the user about consequential choices that evidence cannot settle.

## 2. Compare candidates

For an explicitly requested design comparison, use [orchestration](../orchestration/SKILL.md) to dispatch two candidate workers by default. Honor narrower delegation restrictions. Without authorization or a usable runtime, explain the limitation and offer direct comparison rather than silently changing execution methods.

Give each worker the same requirements, a different design emphasis, and a separate report path. Use [runner-prompt.md](references/runner-prompt.md). They produce design documents, not product edits, commits, or more workers. Read-only candidates can share a source checkout. Isolate any authorized runnable experiments that write files.

Compare candidates against the actual caller examples, invariants, failure behavior, ownership, testing options, and implementation cost. Screen them with [design-red-flags.md](references/design-red-flags.md), treating its findings as questions to justify rather than automatic demands to restructure.

Use effective agent settings from launch receipts when available. A second model is useful when available and requested; never claim model diversity without evidence.

## 3. Recommend and checkpoint

Read both artifacts and verify their claims against the source. Select a design or explain a coherent combination. Record the decision using [rationale-template.md](references/rationale-template.md).

By default, stop here. An architecture request is not permission to implement. If implementation was explicitly requested and the relevant contracts are approved, continue within that scope. Ask before changing public semantics or an approved architecture.

## 4. Implement only within approved scope

Use [tdd](../tdd/SKILL.md) to build verified increments. Keep illustrative sketches outside production source until they can become a working increment. Do not commit incomplete placeholder implementations merely to preserve the sketch.

When implementation exposes a missed requirement, state which assumption changed. Revise the design locally when the change is routine. Return to the user for a material contract change. Repeated workarounds justify reconsidering the design, not deleting unrelated code.

## Result

Return caller examples, the candidates considered, the recommendation and tradeoffs, acceptance checks, unresolved decisions, and paths to the artifacts. State whether implementation was authorized and performed. Complete Orca worker accounting before ending the supervised run.
