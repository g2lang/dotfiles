---
name: implement-spec
description: Implement an approved specification through supervised Orca tasks, serial integration, and independent review. Establish delivery permissions before starting.
disable-model-invocation: true
---

# Implement a specification

Read the [workflow policy](../orchestration/references/workflow-policy.md), [project workflow](../to-tickets/references/project-workflow.md), and [orchestration](../orchestration/SKILL.md). Fetch the installed Orca guide and its coordinator, placement, and messaging references as needed. Do not copy a remembered command sequence over the installed guide.

## 1. Establish scope and authority

Read the approved specification, tickets, comments, project requirements, and working-tree status. Identify dependencies and acceptance checks. Stop for missing consequential decisions rather than guessing them during parallel implementation.

State the integration branch, its exact base revision, worker ownership, and delivery endpoint. This workflow needs permission to create branches, make task-scoped commits, and integrate them locally. If that authority is absent or expressly withheld, ask once before starting. Pushes, tracker writes, PR publication, target-branch merges, and worktree deletion are separate permissions. A request to run this workflow authorizes its bounded supervised workers unless the user restricts delegation.

Preserve existing work. Never reset a checkout onto a preferred base. Create an appropriate Orca-managed checkout when authorized, or ask its owner to resolve an unsuitable one.

## 2. Build the execution graph

Use one coordinator-owned Orca Run. Map each ticket to an implementation Task and an integration-and-verification Task. Record the issue reference, Task IDs, active Dispatch, branch, base revision, and resulting commit in the run's working notes.

The dependency pattern is:

- `build-A` produces a reviewed implementation candidate on its own branch.
- `integrate-A` depends on `build-A`, incorporates its exact commit, and verifies the integration branch.
- `build-B`, when it needs A, depends on `integrate-A`, not merely on `build-A`.

An accepted worker completion automatically settles its Orca Task. Do not mark a build complete and then assume dependent work waits for a later merge. Encode that wait in the graph. If a candidate needs fixes, complete the correction before integration, or create an explicit correction prerequisite. Do not let an integration task report success while its acceptance checks fail.

Only one integration owner may write the integration branch at a time. Add ordering dependencies between integration tasks or dispatch them serially. Keep the common implementation base current only after successful integration. Other implementation tasks may run concurrently when their inputs and ownership allow it.

## 3. Dispatch implementation tasks

Create isolated Orca worktrees when concurrent code, index, or build writes would conflict. Pass an explicit base ref at creation and verify the resolved revision before work begins. A new child workspace relationship alone does not prove its Git base.

Each brief contains the ticket, approved contracts, exact base, allowed files, relevant skills, checks, report path, and Git permissions. Workers use [tdd](../tdd/SKILL.md). They do not run this coordinator workflow, open local approval dialogs, start more workers, or merge into the integration branch.

Each successful worker returns its exact commit, changed files, test commands and results, unresolved concerns, and report path. It follows the live Orca preamble for questions, follow-ups, and completion. Preserve failed attempts and their evidence; retry only through the installed recovery procedure.

## 4. Integrate and verify serially

The integration owner reads the candidate diff and tests, confirms the expected integration tip, incorporates the authorized commit, and runs relevant checks. Resolve conflicts within scope; ask before choosing between conflicting product contracts.

Report the resulting integration commit and actual check results. Only successful integration-and-verification unlocks dependent builds. If incorporation succeeds but checks fail, record that state and repair or explicitly undo it within granted authority before accepting integration. Do not start dependents from a broken tip.

## 5. Review the integrated result

Use [interrogate](../interrogate/SKILL.md) against a fixed integration revision and the approved specification. Check missing requirements as well as defects and scope expansion.

The coordinator evaluates findings before assigning fixes. Dispatch accepted fixes to the implementation owner; a review report alone does not authorize coordinator edits. Integrate fixes serially, rerun checks, and recheck affected findings against the new revision. Do not apply all reviewer suggestions indiscriminately.

## 6. Deliver and settle

Without publication permission, stop at an integrated and verified local branch. With permission, publish using the configured project workflow and [pr](../pr/SKILL.md). Mark review readiness only after the checks required for that state pass. Close tickets only at the project's agreed completion point. Never infer permission to merge the target branch from permission to open a PR.

Process every expected Dispatch through accepted success or failure and the installed reuse, retention, or release procedure. Unknown liveness is not completion. Release archives the worker output and handles its owned execution resource; it does not authorize deleting a worktree. Preserve branches and unique work unless separate cleanup permission covers them.

Report per ticket whether it is implemented, integrated and verified, published, or blocked. Include exact revisions, checks, unresolved issues, evidence locations, and worker disposition. A failed or blocked run is a valid outcome when reported accurately.
