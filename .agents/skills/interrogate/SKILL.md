---
name: interrogate
description: Review a fixed change with independent reviewers, verify their findings, and report defects separately from optional improvements. Does not apply fixes.
disable-model-invocation: true
---

# Interrogate

Follow the [workflow policy](../orchestration/references/workflow-policy.md). An explicit independent-review request authorizes bounded review workers, not edits or publication.

## 1. Fix the review scope

Record the base and head commit IDs, the exact diff command, and the intended behavior. Resolve names to immutable revisions before workers start. Include the originating specification and relevant project standards when available. Report a missing specification rather than inventing one.

Decide explicitly whether the review includes staged, unstaged, and untracked changes. A committed branch diff alone excludes them. If reviewing working changes, capture a private snapshot or patch with the relevant untracked contents and record its identity. Keep that snapshot stable while reviewers work. Never include credentials or private unrelated files.

## 2. Dispatch independent reviewers

Read [orchestration](../orchestration/SKILL.md) and use its installed guide. Start two reviewers by default, with the same scope, intent, specification, and standards. Give each a unique report path and an explicit prohibition on product edits, commits, publication, and further delegation. Read-only review may share the checkout; use the frozen inputs rather than a moving branch tip.

Use configured agent defaults unless the user requests specific available agents or models. Record effective settings when known. If independent workers cannot run, report the limitation and obtain permission before substituting a direct review. Do not claim a multi-model review unless the effective settings establish it.

Construct briefs from [reviewer-prompt.md](references/reviewer-prompt.md), [rubric.md](references/rubric.md), and [code-quality-review.md](references/code-quality-review.md).

## 3. Evaluate the evidence

Process worker questions and completion through Orca. Read every report and inspect the cited code. Deduplicate findings, but do not decide correctness by vote. One demonstrated failure can outweigh several clean reviews. Distinguish missing requirements, wrong behavior, scope expansion, and optional restructuring.

Use [lead-judgment.md](references/lead-judgment.md). Put each finding in one of four groups:

- Act on: a supported defect or requirement violation.
- Consider: a concrete improvement whose cost or priority needs a decision.
- Noted: relevant context with no current action.
- Dismissed: an unsupported or incorrect claim, with a reason.

Review does not authorize fixes. Route accepted fixes to the assigned owner. If a fix changes the reviewed revision, recheck the affected findings and run relevant tests against the new revision before reporting them resolved. A report for an older revision is not approval of a newer one.

## Result

Report intent, exact reviewed inputs, specification coverage, actual reviewers, findings with evidence, unresolved disagreements, and checks performed. An empty review is valid. Complete worker accounting under the installed Orca guide before ending the supervised run.
