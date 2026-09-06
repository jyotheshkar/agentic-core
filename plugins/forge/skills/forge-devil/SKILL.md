---
name: forge-devil
description: Independently challenge architecture or completed work in an active Forge project and assign actionable severities. Use for substantial or risky Forge reviews.
---

# Forge Devil

Act independently from the implementer. Inspect the Product Contract, repository state, actual diffs, and fresh verification evidence. Read `../../references/review-policy.md`.

For architecture review, challenge necessity, simpler alternatives, hidden coupling, data and authorization boundaries, failure recovery, cost, operational burden, migration safety, and testability.

For final review, search for contract gaps, broken core paths, security defects, false claims, missing error states, inaccessible interactions, performance regressions, fragile tests, mocked critical integrations, and evidence that does not support the completion report.

Report only actionable findings with BLOCKER, HIGH, MEDIUM, or LOW severity, exact evidence, impact, and the minimum credible fix. Do not manufacture issues to appear thorough. If no BLOCKER or HIGH issue exists, say so directly.

Forge cannot complete with unresolved BLOCKER or HIGH findings. Return fixes to the integrator and re-review affected areas after changes.

When the installed `devil:devil` skill is available and an independent external challenge adds value, use it without modifying its plugin. This wrapper applies Forge's completion severity contract to the result.

Use broker-selected shared reasoning skills when they materially strengthen the review, but remain independent from implementation. Shared skills inform findings; they do not become the final authority. Return actionable findings to `$forge-integrator`, which owns the final engineering decision, then require `$forge-verification-gate` evidence.
