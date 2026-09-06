---
name: forge-product
description: Convert an active Forge project prompt and repository evidence into a compact, testable Product Contract. Use only for non-trivial Forge delivery.
---

# Forge Product

Create a Product Contract that is brief enough to guide implementation and concrete enough to verify. Derive it from the user's prompt, existing product behavior, repository instructions, and current constraints.

Include:

- outcome and target users;
- required user-visible flows or deliverables;
- acceptance criteria with observable evidence;
- confirmed constraints, reasonable inferences, and unresolved assumptions;
- explicit non-goals that prevent scope creep;
- external integrations, credentials, payment, deployment, or irreversible-action gates;
- relevant quality attributes such as accessibility, security, performance, reliability, or AI evaluation.

Do not invent features or metrics. Resolve cheap questions from the workspace. Make safe, reversible assumptions when they do not materially change the product, and flag them. Ask the user only when a missing decision materially changes the outcome and cannot be inferred safely.

For tiny work, return only a one-sentence outcome and a short done condition.
