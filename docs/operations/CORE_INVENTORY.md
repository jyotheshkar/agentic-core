# Core Inventory

Status: current local evidence, 2026-09-06. The authoritative sanitised records are [Agent Registry](../../core/registry/agent-registry.json) and [Skill Registry](../../core/registry/skill-registry.json).

## Authority-bearing plugins and workflows

| Record | State | Version or implementation | Scope |
| --- | --- | --- | --- |
| MOA | Installed, enabled, verified | `0.1.0+codex.20260906142235`, 9 private skills | Host-mediated orchestration, routing, handoffs, completion governance |
| Minister | Installed, enabled, verified | `0.1.0+codex.20260831230702`, 3 private skills | Strategic and final judgment |
| Scout | Installed, enabled, verified | `1.0.0+codex.20260902030631`, 8 private skills | Current evidence, provenance, freshness, contradiction, completeness |
| Forge | Installed, enabled, verified | `1.1.0+codex.20260831144017`, 7 private skills | Engineering, integration, technical verification |
| Devil | Legacy, installed but non-routable | `0.1.0`, 1 private skill | Retained compatibility plugin, deliberately disabled in the Agent Registry and replaced by shared adversarial review and Forge review |
| Audit | Composed independent workflow, not a plugin | Control-plane and shared-skill contracts | Evidence quality, policy conformance, release claims, residual risks |
| Fix, Design, Launch, Lab | Composed workflows, not plugins | MOA routes Minister, Scout, Forge, Verification, and Audit as needed | See [capability-family decisions](../architecture/CAPABILITY_FAMILY_DECISIONS.md) |

Private skills: MOA: `moa`, `moa-intent-psychology`, `moa-problem-framing`, `moa-capability-discovery`, `moa-agent-router`, `moa-task-decomposition`, `moa-orchestration`, `moa-conflict-arbitration`, `moa-completion-governance`. Minister: `minister`, `minister-router`, `executive-judgment`. Scout: `scout`, `scout-router`, `scout-research-contract`, `scout-investigation-planner`, `scout-evidence-ledger`, `scout-contradiction-resolution`, `scout-synthesis`, `scout-completion-gate`. Forge: `forge`, `forge-router`, `forge-product`, `forge-architect`, `forge-devil`, `forge-integrator`, `forge-verification-gate`. Legacy Devil: `devil`.

Shared skills, all 39 enabled and registered: `skill-broker`, `first-principles`, `evidence-epistemics`, `systems-thinking`, `behavioral-psychology`, `decision-science`, `strategic-foresight`, `game-theory-incentives`, `risk-premortem`, `adversarial-red-team`, `research-planning`, `source-discovery`, `source-verification`, `research-synthesis`, `product-discovery`, `requirements-engineering`, `user-research`, `experience-design`, `product-prioritization`, `software-architecture`, `frontend-engineering`, `backend-engineering`, `api-design`, `database-engineering`, `cloud-infrastructure`, `security-engineering`, `test-engineering`, `performance-engineering`, `ml-problem-framing`, `data-quality-engineering`, `model-evaluation`, `llm-engineering`, `retrieval-augmented-generation`, `responsible-ai-safety`, `project-delivery`, `release-readiness`, `incident-response`, `observability`, `quality-assurance`.

All routable records use free-first policy. None receive authority for paid, credentialed, destructive, public, or other consequential external actions.
