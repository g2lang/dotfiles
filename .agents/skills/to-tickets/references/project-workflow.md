# Project planning and delivery configuration

Read the project's own instructions and tracker configuration, such as `docs/agents/issue-tracker.md`, before planning or publishing. This is project configuration, not a requirement to install another setup skill.

Establish only the facts the task needs:

- The repository identity and tracker, or the chosen local document directory.
- The specification and ticket locations and their status vocabulary.
- Required checks, review ownership, and the rule for closing work.
- Authority to create or modify issues, commit, push, open PRs, or merge.

Use existing conventions. Do not invent labels or assume that GitHub is the tracker because the code has a Git remote. If configuration is absent, produce a local draft in an agreed path and ask only when publishing or delivery is requested. A safe default for nonsecret local drafts is `.scratch/<feature>/`; check repository policy before using it.

Reading tracker data and publishing to it are different permissions. A request to draft a spec does not authorize creating an issue. A request to publish the spec authorizes that publication, not unrelated labels, project settings, or issue closure.

For GitHub, use the project's tested helpers when available, otherwise `gh` help and API documentation. Read all relevant comments and pages. Keep CLI mechanics out of the specification itself.

A ticket records desired work and durable acceptance criteria. An Orca Task records a bounded execution responsibility. A Dispatch records one attempt. Record the mapping during implementation, but do not equate worker completion with integration, tracker closure, or PR merge. See the [workflow policy](../../orchestration/references/workflow-policy.md).
