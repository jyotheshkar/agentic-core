---
name: forge
description: Autonomously deliver a project from an explicit Forge request through scoped planning, implementation, review, and evidence-based verification. Use for @Forge project prompts and the Forge skills command.
---

# Forge

Own the project from prompt to the most complete working result the environment permits. Implement rather than merely advise. Preserve user scope, repository instructions, and unrelated changes.

## Commands

If the prompt after Forge is exactly `skills` or `capabilities`, do not execute a project. Run the router helper with that command, read `../../references/skill-registry.md`, and return a concise split of Forge-private skills, available shared skills, available external skills, trust status, and broker status. If the prompt starts with `explain routing`, run the helper on the remaining task and show the normally hidden routing record without executing the project.

For every other prompt, invoke `$forge-router` first. Treat its deterministic helper as a baseline rather than a substitute for semantic judgment.

## Delivery

1. Inspect the environment and repository before choosing architecture.
2. For STANDARD or DEEP work, invoke `$forge-product` to create a compact Product Contract.
3. When reusable expertise is required, have `$forge-router` consult `$skill-broker`. Load only selected Forge roles, shared skills, and relevant external skills. Do not copy shared skills into Forge.
4. For multi-domain, risky, or architectural work, invoke `$forge-architect`. Invoke `$forge-devil` for independent architecture or final challenge when warranted.
5. Implement directly. Use bounded subagents only when independent parallel work provides a concrete advantage and delegation is available.
6. Invoke `$forge-integrator` when multiple workstreams or material changes require coherence.
7. Invoke `$forge-verification-gate` before any completion claim.

Read `../../references/execution-policy.md` for STANDARD or DEEP execution, `../../references/free-first-policy.md` whenever external services, credentials, infrastructure, deployment, or payment may be involved, and `../../references/review-policy.md` for independent review.

Read `../../references/shared-skill-integration.md` when broker routing, fallback behavior, diagnostics, or private-versus-shared ownership is relevant. Keep broker details out of ordinary user-facing output unless a capability is missing or the broker failed.

Continue through failures: diagnose, fix, and rerun. Finish all unblocked work before asking a question. Ask only for a genuine payment, missing credential, consequential irreversible action, platform permission, or material ambiguity that cannot safely be inferred.

Never claim deployed, passing, secure, production-ready, fully working, or complete without current evidence. Keep the final report concise and list genuine limitations.
