# Consolidate behavior behind useful interfaces

Start with a demonstrated problem: callers repeat coordination, one invariant is enforced in several places, or a change requires tracing unrelated layers. Describe the behavior to preserve before restructuring.

## Dependencies

- In-process computation can be tested through its own public interface. Consolidate it when doing so clarifies ownership, not simply because it has no I/O.
- Local test implementations can make development cheaper, but establish which production guarantees they do not model.
- Owned services and external providers may warrant an explicit adapter when transport or provider behavior needs isolation.
- A single concrete adapter can justify a boundary if it protects a real contract. Do not invent more implementations to justify an abstraction.

Keep storage, transport, and framework representations private unless exposing them is an intentional part of the caller's contract. Derived domain facts should have clear ownership rather than several hand-synchronized copies.

## Preserve verification

Use [behavioral testing](../principle-test-behavior-not-implementation/SKILL.md). Retain tests of numerical properties, serialization, persistence, and recovery when they establish distinct guarantees. Remove tests only when they are redundant, no longer relevant, or depend on obsolete private structure.

A fake database does not establish the real database's durability or isolation. Preserve suitable integration checks while moving code. Use small, passing refactors rather than a broad structural rewrite without intermediate evidence.

## Stop condition

The refactor is complete when the required behavior still passes its checks and the named ownership or caller-coordination problem is resolved. Further aesthetic cleanup is a separate task.
