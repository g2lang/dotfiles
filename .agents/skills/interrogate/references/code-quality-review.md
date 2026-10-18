# Code-quality review

Assess the changed code against project requirements and the cost of understanding and maintaining it. Read enough surrounding code to establish each finding. Review is not permission to restructure the project.

Use [reader load](../../principle-minimize-reader-load/SKILL.md) and [codebase-design](../../codebase-design/SKILL.md) when evaluating ownership or interfaces.

Look for:

- Duplicated decisions that can diverge and change observable behavior.
- Mutable state with unclear ownership or unsafe concurrent updates.
- Interfaces that make callers coordinate internal implementation steps.
- Type escapes or ambiguous result states that permit plausible mistakes.
- Added dependencies or abstractions with no demonstrated need.
- Repeated special cases that indicate a missing representation or invariant.

File length, caller counts, and the number of layers are clues, not approval thresholds. A small wrapper may isolate a dependency. A large cohesive module may be easier to understand than several forwarding layers. Explain the concrete cost before recommending a change.

Treat a reachable correctness or safety problem as a defect. Treat an alternative structure as optional unless it violates a documented requirement or causes a demonstrated maintenance problem. Keep unrelated improvements outside the change's acceptance criteria.

Prefer a correction proportional to the problem. Broader redesign requires a separate decision. An unchanged behavior and a cleaner-looking diff are not enough to justify expanding the task.
