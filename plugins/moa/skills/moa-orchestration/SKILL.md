---
name: moa-orchestration
description: Coordinate execution graph nodes and bounded handoffs across Minister, Forge, shared skills, tools, and any other enabled agents in an active MOA workflow.
---

# MOA Orchestration

Execute ready graph nodes in dependency order. Use the handoff contract in `../../references/handoff-contract.md`. Give each recipient only relevant context, constraints, required output, acceptance criteria, authority, and known risks.

Minister decides strategic direction and outcome fit. Scout owns research evidence and research completeness. Forge owns engineering implementation. MOA owns scope, sequencing, handoffs, and orchestration. Verification owns evidence of completion.

Track node status as PENDING, RUNNING, BLOCKED, FAILED, or COMPLETE. A node is COMPLETE only when its output and verification requirement are satisfied. Surface genuine blockers and continue all other safe work.
