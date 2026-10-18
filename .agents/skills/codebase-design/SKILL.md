---
name: codebase-design
description: Design interfaces that hide implementation complexity, make state ownership clear, and support useful behavioral tests. Use for module design, refactoring, or interface tradeoffs.
---

# Codebase design

A useful module lets callers perform meaningful work without coordinating its implementation. Design from realistic call sites, errors, and invariants before choosing internal structure.

## Vocabulary

A module is code with an interface and an implementation. Its interface includes the types, ordering rules, failure behavior, assumptions, and resource costs a caller must understand. A deep module provides substantial behavior through a small understandable interface.

A seam is a place where behavior can be substituted. An adapter connects a concrete external system or representation at that interface. Use the project's vocabulary, including API, service, component, or boundary when those words are accurate. Consistency should clarify the design, not prohibit ordinary terminology.

## Design questions

- Can the caller accomplish its task without coordinating internal stages?
- Does the interface hide storage and transport details while preserving meaningful domain assumptions?
- Is there one clear owner of each mutable state or invariant?
- Would deleting this layer remove unnecessary forwarding, or force callers to repeat real decisions?
- Can tests exercise the promised behavior without depending on private call order?
- Does the extra abstraction serve a demonstrated need?

One caller or implementation does not automatically make a boundary unnecessary. A wrapper can isolate an external dependency, enforce a contract, or manage a resource lifetime. Explain what it protects. Avoid speculative interfaces that add no such value.

## Testability and state

Accept dependencies where their variation matters. Prefer pure transformations for computation and explicit resource ownership for I/O. Keep mutation local when it is appropriate; do not add indirection just to remove every mutation.

Use [reader load](../principle-minimize-reader-load/SKILL.md) to assess indirection and hidden state. Use [type discipline](../principle-type-system-discipline/SKILL.md) for representations and [behavioral testing](../principle-test-behavior-not-implementation/SKILL.md) for tests. Public interfaces at several module levels can each deserve tests. No single end-to-end test replaces every lower-level property.

## Further work

Read [DEEPENING.md](DEEPENING.md) when consolidating existing modules. For an explicitly requested comparison of competing designs, follow [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md), which uses [architect](../architect/SKILL.md). Merely reading this reference does not start workers or authorize implementation.
