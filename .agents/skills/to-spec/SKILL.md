---
name: to-spec
description: Turn an established discussion into a concise specification. Draft locally unless publication is requested and configured.
disable-model-invocation: true
---

# Write a specification

Read the [project workflow](../to-tickets/references/project-workflow.md) and [workflow policy](../orchestration/references/workflow-policy.md).

Synthesize the current discussion and relevant code. Use agreed domain vocabulary and existing decisions. Do not run another interview or invent answers. Mark unresolved questions and request a decision only when it blocks the requested deliverable.

Describe testing at the levels needed to establish the contract. Prefer existing interfaces, but do not force all checks through one highest-level interface. A property test, a persistence test, and a client test may establish different requirements. Use the [behavioral-testing principle](../principle-test-behavior-not-implementation/SKILL.md).

Write a proportionate specification with these sections:

- Problem and intended users.
- Observable behavior, with concrete caller examples where useful.
- Invariants and data semantics.
- Failure, retry, cancellation, and recovery behavior where applicable.
- Approved implementation decisions and their reasons.
- Acceptance criteria and verification strategy.
- Exclusions and unresolved decisions.

Include paths, revisions, or small type sketches when they make a decision precise. Label illustrative code and avoid duplicating implementation details that do not constrain the feature. Use only as many scenarios as the feature needs.

Draft in the project's document location. Publish only when requested and the tracker is configured. Apply only agreed statuses or labels, and do not label unresolved work ready for implementation. Report the path or issue reference and any decisions still needed. Do not start implementation from this command.
