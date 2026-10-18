---
name: blast-radius
description: Investigate what a proposed change could break beyond its diff and test the assumptions that make it safe.
disable-model-invocation: true
---

# Assess change impact

Follow the [workflow policy](../orchestration/references/workflow-policy.md). This is an investigation, not permission to fix findings or publish anything.

1. Fix the scope and revision. State whether working-tree changes are included. Inspect the diff, callers, tests, relevant Git history, and project decisions directly.
2. Identify the assumptions on which safety depends. A change may depend on several independent conditions; do not force them into one explanation.
3. Follow dependencies that symbol search misses, including stored data, wire formats, configuration, another language reading the same bytes, and deployed consumer versions. Inspect the pinned dependency version rather than assuming current upstream behavior.
4. Test the important assumptions using the smallest safe executable check. Prefer a scratch directory or isolated test instance. Do not mutate a live service or shared checkout without permission. Distinguish code inspection from an executed check.
5. For an authorized independent review, use [interrogate](../interrogate/SKILL.md) with the fixed scope and identified risks. Otherwise complete the investigation directly.

Report what changed, each confirmed risk and its evidence, assumptions established or still unproven, and cases checked and cleared. Explain plausible failure paths and consequences without inventing numerical probabilities. Name the cheapest next check for each unresolved material risk. Keep unsupported speculation separate from findings.
