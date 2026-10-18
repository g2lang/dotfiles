# Design candidate worker brief

The coordinator supplies the requirements, approved decisions, source snapshot, design emphasis, allowed experiments, and a unique report path.

You produce one candidate design only. Do not run the coordinator's workflow, delegate, implement product code, commit, publish, or change shared files. Follow the live Orca preamble for questions and completion.

Read [codebase-design](../../codebase-design/SKILL.md) and [design-red-flags.md](design-red-flags.md). Use [domain-modeling](../../domain-modeling/SKILL.md) as a reference if terminology is unresolved, but propose glossary changes in your report rather than editing shared documents.

Your report contains:

1. Realistic caller examples before types or signatures.
2. The proposed data types, operations, errors, and invariants.
3. Ownership of mutable state and behavior under concurrent use.
4. External dependencies and how to test the relevant behavior.
5. What the interface hides and what callers must still know.
6. Costs, rejected alternatives, open questions, and evidence for factual claims.

Use [type discipline](../../principle-type-system-discipline/SKILL.md), [idempotency](../../principle-make-operations-idempotent/SKILL.md), and [reader load](../../principle-minimize-reader-load/SKILL.md) where relevant. Types do not prove that a lease is current or that an external operation succeeded. Keep runtime checks for conditions that can change.

Sketches are illustrative, not compiled implementations, unless an authorized experiment actually compiled them. Record any experiment and its result. Return the artifact path and explicit task outcome through the live worker completion protocol.
