---
name: moa
description: Orchestrate an explicit @MOA request by framing the real outcome, requiring adaptive Minister judgment, selecting the minimum sufficient installed agents and shared skills, coordinating execution, and governing completion. Use for @MOA tasks and MOA diagnostics.
---

# MOA

Answer: which available agents, skills, tools, and workflows should solve the user's actual problem completely?

## Diagnostics

For `agents`, `skills`, `health`, or `explain routing <task>`, run `python ../../scripts/moa_core.py <command>` from this skill directory and report the result. Diagnostics inspect live registries and paths. They do not imply that every installed capability plugin is an autonomous agent.

## Workflow

1. Invoke `$moa-intent-psychology` and `$moa-problem-framing` to separate the request, real problem, and desired outcome.
2. Invoke `$minister` for every substantive task. Use MOA participation levels LIGHT, STANDARD, DEEP, or CRITICAL. For compatibility with the current Minister plugin, pass DEEP as Minister COUNCIL and label the MOA level DEEP.
3. Invoke `$moa-capability-discovery` and `$moa-agent-router`. Consult the AI OS Agent Registry and `$skill-broker`; select the minimum sufficient enabled mixture. Never invent a plugin or select a disabled record.
4. Use `$scout` for current research, source or claim verification, contradiction analysis, and research completeness. Pure research does not select Forge. When research must precede implementation, route Scout before `$forge` and preserve verified facts, versions, constraints, and unknowns in the Forge handoff.
5. For multi-step work, invoke `$moa-task-decomposition` and `$moa-orchestration`. Pass bounded handoffs. Use `$forge` for implementation, repair, or engineering work without reproducing Forge internals. Select `$audit` as the standalone assurance agent for supplied-artifact audits, release readiness, and completion claims; do not ask Audit to replace Scout, Forge, Minister, or MOA.
6. Preserve material Minister conditions. Resolve disagreements with `$moa-conflict-arbitration`, based on domain authority rather than votes.
7. After execution, obtain Minister final judgment at appropriate depth and invoke `$moa-completion-governance`. A returned artifact is not proof that the user outcome is achieved.

Keep ordinary user output simple. Show a short MOA plan only when it helps. Direct plugin-to-plugin process invocation is not exposed by Codex, so compose installed skills in the current task and never claim separate autonomous plugin execution.

Read `../../references/architecture.md` for substantive workflows, `../../references/handoff-contract.md` before delegating, `../../references/completion-contract.md` before a completion claim, and `../../references/safety-policy.md` when cost, credentials, publishing, deletion, or production actions matter.
