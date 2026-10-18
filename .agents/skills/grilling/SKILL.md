---
name: grilling
description: Interview the user to resolve meaningful open decisions in a plan or design. Use when the user asks to be grilled or to stress-test an idea.
---

# Clarify a design through questions

Identify the decisions that must be settled and which depend on others. Work in rounds. Ask only questions whose prerequisites are settled, then wait for the user's answers before proceeding to dependent decisions.

Number each question, state why it matters when that is not obvious, and offer a reasoned recommendation where possible. Use plain text and short paragraphs. Do not force a yes/no answer when the alternatives need explanation.

Look up facts yourself through focused source inspection or documentation. A routine lookup does not need a worker. Use supervised research only when authorized under the [workflow policy](../orchestration/references/workflow-policy.md). Do not ask the user for facts you can inspect safely, and do not invent facts to keep the interview moving.

Keep the discussion within the requested scope. Reuse prior decisions instead of asking them again. Stop when the decisions needed for the next step are resolved or the remaining blockers are explicit. Summarize the agreement and ask for confirmation before implementing behavior that has not already been authorized.

A dispatched worker must not start a separate interview. Send unresolved decisions to its coordinator using the live Orca preamble. The coordinator answers within approved scope or asks the user.
