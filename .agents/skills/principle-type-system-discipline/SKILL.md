---
name: principle-type-system-discipline
description: Use when designing identifiers, units, result states, or typed interfaces, and when parsing external data. Prevent plausible mixups without wrapping every value.
---

# Type-system discipline

Use types to reject impossible combinations, mismatched identifiers or units, and unhandled result states. Follow the language's idioms and the project's contracts.

- Introduce a distinct type when confusing values would cause a plausible error. Avoid branding every argument merely because it has a different name.
- Represent mutually exclusive states explicitly instead of coordinating unrelated booleans or optional fields.
- Parse untrusted data at network, configuration, storage, and language boundaries. Reuse the validated representation internally rather than repeating the same parsing.
- Derive types from an authoritative schema where suitable tooling exists. When representations differ intentionally, make conversion and contract checks explicit.
- Keep checks for conditions that can change at runtime, such as authorization, lease ownership, concurrent state, and successful external persistence. A well-typed value does not establish those facts.

The test is whether the type prevents a real mistake or clarifies a contract. If it only adds conversions and indirection, prefer the simpler representation.
