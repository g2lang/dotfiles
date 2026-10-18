---
name: principle-guard-the-context-window
description: Use during large investigations, long command output, repeated file reads, or multi-stage work. Bound inputs and preserve decisions and evidence without dropping necessary context.
---

# Guard the context window

Read enough to answer the current question, then expand when the evidence requires it. Context management must not hide correctness-critical details.

- Inventory paths and search for relevant symbols before opening whole directories.
- Read the implementation, callers, and tests needed for the decision. Use bounded ranges for large files, then follow missing context when necessary.
- Save large logs or generated results to private files. Bring relevant excerpts, commands, and artifact paths into the conversation.
- Avoid rereading unchanged material already available in context.
- Before changing phases, record approved decisions, exact revisions, evidence paths, unresolved questions, and ownership of active work. Distinguish facts from inference.
- Delegate independent investigations only when authorized under the [workflow policy](../orchestration/references/workflow-policy.md). Require source references and inspect important evidence rather than trusting summaries alone.
- Verify that a handoff's paths are accessible to its recipient. A summary cannot preserve evidence that was deleted or exists only on another host.

A file or turn budget is a planning aid, not a reason to skip relevant code or stop accounting for active workers. Use [handoff-note](../handoff-note/SKILL.md) for an explicitly requested transfer document, not as a substitute for completing supervised work.
