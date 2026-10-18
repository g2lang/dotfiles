---
name: correct
description: "Find the mistakes agents keep repeating in this repo and make each one impossible. Try architecture first, then types, then a lint whose error names the fix, then a test, and write docs last. Prove each check fails on a real past mistake. Repeat this each time the operator corrects you. Use for /correct."
disable-model-invocation: true
---

# Correct

Identify recurring mistakes and propose enforceable corrections. Follow the [workflow policy](../orchestration/references/workflow-policy.md). Diagnose first, present the proposed scope, and implement only the corrections the user authorizes. Reading this skill after a correction does not authorize an unrelated repository cleanup.

Assume every contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles. Design the repo so a change that looks right from one file is right for the whole repo.

## Find the mistake classes

First, read recent commits, reverts, review comments, agent instruction files, and comments that explain workarounds. Group the mistakes into classes. A class counts once it has happened twice.

## Fix each class at the highest level that works

1. **Eliminate it with architecture.** Give each piece of state one owner and each task one supported way. Hide internals so the wrong import fails. Replace hand-synced lists with one source of truth. Delete old ways and dead code an agent would copy.
2. **Enforce it with types so the bad state can't be written.** If bad code still compiles, add a lint or CI check whose error names the file, type, or function to use instead. If the pattern is already common, fail only when a change adds more.
3. **Test the behavior.** Fix or delete any test that still passes when the behavior it checks breaks, or that fails when only the internals change.
4. **Write docs or agent rules last, only for judgment calls.** Nothing fails when an agent skips them.

## Fix and prove

Implement the approved corrections in focused increments. Prove each new check fails on a real past mistake or a documented equivalent reproduction, then passes on the correction. Run local checks and report whether CI has actually run; do not imply that adding CI configuration means it passed. Commit only when requested. Exceptions need an explicit reason and an owner; use expiry dates where the project requires them.

## Keep the rule table

Record necessary judgment rules in the project's existing guidance. Prefer linking to the enforcing check over duplicating its implementation. A repeated correction is evidence for a proposed enforcement change, not permission to expand the current task. Remove obsolete guidance when the approved fix makes it unnecessary.

**Reply:** each class with its evidence, the level you picked, and why a higher level didn't work.
