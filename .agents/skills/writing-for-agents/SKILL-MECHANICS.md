# Skill mechanics

This is the skill-specific reference for [writing-for-agents](SKILL.md).

## Discovery, loading, and authority

These are separate decisions:

- Automatic discovery lets an agent select a skill when its description matches the task.
- Explicit loading reads a requested skill or a file referenced by an authorized workflow.
- Authority comes from the current request and applicable instructions, not from reading a skill.

For automatically selectable guidance, omit `disable-model-invocation` and write a concrete description of the situations it handles. Selection is not guaranteed. Keep essential project requirements in the project's standing instructions and executable checks.

For substantial user-initiated procedures, set `disable-model-invocation: true`. In clients that honor it, the skill is excluded from automatic selection but remains explicitly available. When `agents/openai.yaml` is present, keep `policy.allow_implicit_invocation` consistent with that choice. Client behavior can differ; verify discovery and explicit commands in the actual client after activation.

This flag is not filesystem access control. An authorized workflow can explicitly read a referenced file. That read must not accidentally start the referenced skill's entire procedure or broaden permissions. Separate coordinator instructions from worker references so a candidate worker does not launch another candidate set.

## Portable references

Link local dependencies with relative Markdown paths from the containing file. Say to read and follow the relevant file instead of assuming an invocation tool exists. Keep required support files in the managed collection. Every local link must resolve after installation.

Use [the shared workflow policy](../orchestration/references/workflow-policy.md) for permissions and delegation. Load Orca's installed guide through the [orchestration stub](../orchestration/SKILL.md) or [CLI stub](../orca-cli/SKILL.md); do not duplicate its version-specific command catalog.

## Scope and invocation

A description should identify when the skill adds useful guidance, without matching every coding request. A reference skill should not secretly launch workers, rewrite files, or commit. State the side effects of a procedural skill and check that the caller authorized them.

Explicit command names, directory names, frontmatter names, and client metadata should agree. Renaming a command must also update links and user documentation. Avoid duplicate names in different discovery locations.

## Composition

Use shared reference files for repeated guidance. One workflow should own each multi-step procedure. Other skills may link to that procedure, but reading a design or review reference must not recursively execute its coordinator.

A router can recommend a command or read an explicitly authorized reference. It does not acquire permission to run every procedure it can name. Keep a clear stopping point and a concrete completion condition for each workflow.
