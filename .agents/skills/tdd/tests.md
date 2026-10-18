# Choosing test assertions

The [behavioral-testing principle](../principle-test-behavior-not-implementation/SKILL.md) is the shared reference. Assert the contract at the interface whose behavior matters.

Good examples include:

- Retrieving a record after creating it when retrieval is the user's contract.
- Checking durable rows after restarting a writer when durability is the contract.
- Asserting that a cached request sends no additional request to an external provider. Pair it with a case that does send a request so the test proves it can observe one.
- Checking that an interval operation preserves a mathematical property across generated inputs.
- Checking a calculated value against an independently worked example, not the same calculation copied into the test.
- Checking a stable error category that callers branch on.

A test is coupled to implementation when it asserts which private helper ran, observes intermediate state no consumer can see, or breaks after a refactor that preserves every promised behavior.

The syntax of an assertion does not decide its value. A provider-call count can establish behavior; an internal-helper-call count usually does not. Database inspection can establish a persistence guarantee; inspecting an incidental private schema in a client-ergonomics test usually does not.

Keep lower-level tests when they establish properties the higher-level tests do not. Replace or delete redundant tests based on what they prove, not their position in the module hierarchy.

Use precise assertions. An empty result is correct when the contract requires no observations, but is a weak assertion if the test was supposed to prove successful retrieval. Derive expected values from requirements or independent fixtures.
