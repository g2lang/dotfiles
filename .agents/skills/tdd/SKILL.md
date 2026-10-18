---
name: tdd
description: Build features or fix bugs through small test-first increments. Use when implementing specified behavior, regression tests, or integration tests.
---

# Test-driven development

Use [behavioral testing](../principle-test-behavior-not-implementation/SKILL.md) as the definition of a useful test. This skill defines the implementation sequence. Read [tests.md](tests.md) and [mocking.md](mocking.md) when choosing assertions or dependencies.

## Establish the contract

Read the task, relevant project requirements, and existing tests. Identify the behavior and the interface through which it can be exercised. Use [codebase-design](../codebase-design/SKILL.md) if the interface itself needs design.

Confirm consequential new behavior or public contracts before implementing them. Reuse already approved decisions; do not ask for permission before every routine test. A dispatched worker routes unresolved decisions through its live Orca ask mechanism under the [workflow policy](../orchestration/references/workflow-policy.md), rather than opening a separate user interview.

Choose the testing levels needed for the behavior. Focused property or numerical tests, persistence tests, and client tests can prove different requirements. Tests must exercise real behavior at the relevant interface; they need not all start at the application's outermost entry point.

## Work in verified increments

1. Choose one concrete behavior and an expected result independent of the implementation.
2. Add the smallest useful test and run it before changing the implementation. Confirm that it fails for the intended reason, not an unrelated setup failure.
3. Implement enough behavior to satisfy the test and the established contract.
4. Run the focused test and relevant nearby checks.
5. Refactor while tests pass when it improves the implementation without changing behavior. Keep unrelated cleanup out of scope.
6. Repeat, then run the broader project checks before reporting completion.

Do not write a large batch of speculative tests before learning from the first working increment. Do not weaken an assertion merely to make the current implementation pass.

When a regression requires integration infrastructure, use the project's isolated setup or establish the missing test capability within authorized scope. If a useful failing check cannot be run, report the reason and the closest executable evidence. Do not call an unexecuted test a demonstrated regression test.

## Result

Report the failing-before evidence, passing-after checks, broader checks, and remaining limitations. A passing worker-local test does not prove integration with other branches. Follow the assigned task's completion contract and do not commit, merge, or publish unless authorized.
