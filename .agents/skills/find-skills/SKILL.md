---
name: find-skills
description: Find and assess skills when the user asks for an installable capability or a skill recommendation. Do not search for skills instead of doing an ordinary task.
---

# Find and assess skills

Clarify the capability the user needs and check the existing collection first. Search upstream repositories or the Skills CLI catalog when external material would help. Search results and popularity are leads, not evidence of safety or suitability.

Before recommending a skill, read its instructions and relevant scripts. Check its source, license, dependencies, permissions, invocation behavior, tool assumptions, and overlap with installed skills. Compare the actual procedure with the user's tools and project needs. Report required adaptations and limitations.

## Managed installation

For this user's shared collection, installation means reviewed vendoring into `~/Projects/dotfiles/.agents/skills/`, not running a global installer over `~/.agents/skills/`.

With approval:

1. Obtain a pinned upstream revision in a temporary download location.
2. Inspect the complete skill directory and required support files. Exclude credentials, private state, and external symlinks.
3. Copy reviewed sources into the dotfiles checkout without overwriting unrelated work. Preserve licenses and record the upstream URL, revision, and local adaptations in `UPSTREAM.md`.
4. Resolve dependencies, naming collisions, tool assumptions, and invocation metadata.
5. Run the repository's agent tests and configuration checks. Report the diff and remaining activation step.

Do not run an installer or blanket update against Nix-managed skill names. Leave unrelated installer-managed skills and lock files untouched. Activation requires separate authorization under the [workflow policy](../orchestration/references/workflow-policy.md).

For another repository or installation system, inspect its documented ownership rules instead of assuming this personal layout. If no suitable skill exists, explain why direct execution or a small local reference may be better than installing a framework.
