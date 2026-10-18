# Compare alternative interfaces

When the user requests competing designs, use [architect](../architect/SKILL.md). It owns the common brief, bounded Orca candidate tasks, comparison, and approval checkpoint. Do not start an additional set of workers from this reference.

Use [codebase-design](SKILL.md) to compare what callers must know, where state belongs, and how behavior can be tested. Give candidates genuinely different constraints when those alternatives matter, such as prioritizing the common caller versus supporting several proven use cases.

A worker assigned one candidate returns that candidate only. It does not invoke architect's coordinator phases. A routine local design choice can be compared directly without delegation under the [workflow policy](../orchestration/references/workflow-policy.md).
