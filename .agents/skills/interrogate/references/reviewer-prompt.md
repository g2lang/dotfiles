# Reviewer task brief

The coordinator supplies fixed review inputs, intent, specification, project standards, relevant source paths, and your unique report destination.

Review those inputs only. Do not edit product files, commit, publish, apply fixes, or delegate. You may write only your assigned report. Follow the live Orca preamble for questions and completion. If the inputs changed or cannot be read, report the limitation instead of reviewing an unknown revision.

Read [rubric.md](rubric.md) and [code-quality-review.md](code-quality-review.md). Check both implementation correctness and specification coverage. Project requirements take precedence over generic design preferences.

For each finding, give:

- Severity: critical, warning, or nit.
- Exact location in the reviewed revision or snapshot.
- The requirement, observable behavior, or concrete maintenance problem involved.
- Evidence, including a reachable failure path or executable check where practical.
- A proposed correction only when you have a supported one.

Separate missing requirements, incorrect behavior, scope expansion, and optional improvements. Do not inflate style preferences into blockers. Do not rewrite the intended product behavior, but flag ambiguous or contradictory requirements for the coordinator.

Tests and inspection commands must stay within the task's permissions. A read-only brief does not permit altering fixtures in a shared checkout or running destructive integration tests. Report unexecuted checks honestly.

Return no findings when that is the evidence. Include the reviewed input identity and any limitations, then send the required worker completion with your report path.
