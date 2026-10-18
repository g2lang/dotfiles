---
name: principle-minimize-reader-load
description: Use when designing or reviewing module boundaries, tracing data ownership, or changing mutable state. Reduce unnecessary indirection and hidden state while preserving useful boundaries.
---

# Minimize reader load

Assess how many places a reader must inspect to explain a behavior and how much mutable state they must remember. Line count and caller count are clues, not goals.

- Remove forwarding layers that add no policy, adaptation, ownership, or useful abstraction.
- Preserve wrappers that isolate external dependencies, enforce contracts, or manage resource lifetimes, even with one caller or implementation.
- Keep related decisions with the code that owns them. An interface should save callers from learning implementation details without hiding assumptions they need to interpret the result.
- Prefer locals over broader mutable state, and derive values instead of maintaining synchronized copies when practical.
- State an invariant where it is established and enforced rather than repeating it in every caller.

Ask where a value comes from, who can change it, and what must remain true. If those answers require unnecessary traversal or hidden state, improve the structure. Inherently difficult behavior may still need careful explanation and tests; do not flatten useful boundaries to meet an arbitrary time or file-count limit.
