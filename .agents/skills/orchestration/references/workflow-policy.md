# Shared workflow policy

Read this policy before a skill delegates work, publishes an artifact, or changes Git or tracker state. It defines local permissions and ownership. The installed Orca guide remains authoritative for commands and lifecycle recovery.

## Scope and permissions

- Work directly by default. Task complexity alone does not authorize delegation.
- An explicit request to run a multi-worker workflow such as architect's design comparison, interrogate, or implement-spec authorizes its bounded workers. An automatically selected reference skill does not. Follow narrower user or project restrictions.
- Permission to investigate, design, review, or write a plan does not authorize product implementation. Permission to implement does not by itself authorize commits, pushes, publishing issues or PRs, merging, or deleting worktrees. Establish those permissions once at the relevant phase, not before every routine edit.
- Confirm consequential public contracts, financial semantics, and architectural choices unless the user has already approved them. Routine choices within that scope remain autonomous.
- Never reset or discard existing work to make a workflow fit. Inspect the checkout first. A wrong or dirty base requires another checkout or a decision from its owner.
- Deployment, destructive operations, public artifact sharing, and Nix activation need explicit authorization. A skill cannot expand its caller's authority.

## Choose the execution path

For supervised delegation, read [orchestration](../SKILL.md) and fetch its version-matched guide. For a transfer of ownership without waiting, read [orca-cli](../../orca-cli/SKILL.md). Do not silently replace an unavailable Orca runtime with native subagents or ad hoc terminals. Report the limitation; perform authorized direct work where possible, or ask before changing the execution method.

A note prepared by [handoff-note](../../handoff-note/SKILL.md) transfers no ownership and starts no worker. An Orca handoff ends after verified prompt delivery and reporting the recipient. A supervised workflow remains responsible for results, questions, and cleanup decisions.

Use configured agent defaults. Pass model and effort overrides only when the user names them and the installed CLI supports them. Record effective launch settings when available. Two agents are not proof of two different models. If a requested model is unavailable, report it and seek an authorized alternative rather than guessing a substitute.

## Worker contract

Before dispatch, give each worker:

- The task, its allowed outputs, and explicit exclusions.
- The exact checkout or source snapshot, base revision, and any relevant dirty changes.
- Its write ownership, or an explicit instruction to leave product files unchanged.
- Relevant skill and evidence paths, with versions or revisions where needed.
- Acceptance checks, report destination, and authorized Git operations.

A worker performs only that task. Reading a parent workflow does not authorize recursive delegation, running the coordinator's phases, or starting implementation from a review brief. Only the coordinator may expand the task or assign another worker.

Dispatched workers follow their live Orca preamble. They route blockers through its ask/reply mechanism, check follow-ups at checkpoints, and report the explicit success or failure outcome. They do not open a local interview that the coordinator cannot answer. The coordinator escalates decisions reserved for the user.

## Isolation and artifacts

Use the current or an exact existing workspace for read-only review. Give each report writer a separate output path. Use separate Orca-managed worktrees for concurrent edits when shared files, the index, builds, or generated output could conflict. Set the Git base explicitly; Orca parentage is not a substitute for a base revision. One owner writes each shared integration branch.

Verify that every worker can read its brief and skill files on its execution host. A local temporary path is not automatically available remotely. Transfer reviewed files privately or use accessible committed references. Check returned artifacts on the execution host before relying on them. Do not upload proprietary data or transcripts as public artifacts to solve a path problem.

Keep evidence outside the checkout unless it belongs in the deliverable and is safe to commit. Preserve evidence through cleanup. Never store credentials or private run logs in this dotfiles repository or any other source included by a Nix path flake.

## Settlement and acceptance

Follow the installed guide's Run, Task, Dispatch, inbox acknowledgment, retry, and release rules. A timeout, idle display, or missing message is not proof of exit or completion. Do not launch a duplicate editor because a worker went quiet.

An accepted worker completion settles its Orca task. It does not prove that the code is integrated, that a review accepted the result, or that a GitHub issue should close. Express integration and verification as separate tasks when dependent work needs those results. Check the artifact and acceptance evidence independently.

Process questions and completion messages before acknowledging their delivery. Give each settled worker the next ownership decision required by the installed guide. Release does not delete a worktree. Worktree deletion requires separate permission and verification that no unique work remains.

A review-only task authorizes findings, not fixes. Route accepted fixes to the assigned implementation owner, or obtain permission before the coordinator edits code.

## Completion report

Report the actual result, checks run, artifact or revision references, remaining blockers, and worker disposition. Distinguish implementation complete, integrated and verified, published, and merged. Do not imply a later state from an earlier one.
