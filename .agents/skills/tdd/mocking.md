# External dependencies in tests

Use real local implementations where practical, including isolated test databases when persistence semantics matter. Mock or fake external providers, clocks, randomness, or unavailable services at their actual interface.

Pass dependencies explicitly when that makes behavior testable. Do not add a generic dependency framework solely to satisfy a testing convention.

A fake establishes behavior only for the guarantees it models. An in-memory store does not prove a production database's transaction, concurrency, or durability behavior. Use integration tests for those guarantees.

Avoid mocks of private collaborators that pin internal call structure. Assertions about a real external contract, such as the request a provider receives, are valid under [behavioral testing](../principle-test-behavior-not-implementation/SKILL.md).

Keep default tests deterministic and isolated. Live provider calls, paid services, production data, and destructive fixtures require explicit project support and authorization. Use synthetic or sanitized fixtures without credentials or proprietary payloads.
