---
name: handoff-note
description: Write a private continuation note for another session. Does not launch an agent, transfer ownership, or wait for work.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

# Prepare a handoff note

Write a concise continuation document in a private temporary directory, outside the checkout. Tailor it to the next session's task. Follow the [workflow policy](../orchestration/references/workflow-policy.md).

Include the goal, approved decisions, exact source revisions and relevant working changes, checks performed, unresolved questions, permissions, and current ownership of any active work. Reference existing specifications, issues, commits, and reports rather than copying them. List useful skills by name and readable path, not by an assumed invocation tool.

Redact credentials, sensitive payloads, and unrelated personal information. Verify that referenced artifacts still exist. State which paths are local to this host and what must be transferred privately if the recipient runs elsewhere.

Creating this note starts no worker and changes no ownership. For a requested full transfer, use [orca-cli](../orca-cli/SKILL.md) separately. For an ongoing supervised task, use [orchestration](../orchestration/SKILL.md) and preserve live ownership and completion accounting. A saved note is not a worker completion message.

Return the note's path and any inaccessible dependencies. Do not publish or commit it without authorization.
