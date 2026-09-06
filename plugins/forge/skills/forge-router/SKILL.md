---
name: forge-router
description: Route an active Forge request to the minimum sufficient execution mode, private roles, shared AI OS skills, and installed external skills. Use only inside a Forge workflow.
---

# Forge Router

Classify the request as QUICK, STANDARD, or DEEP using `../../references/execution-policy.md`. Identify domains such as frontend, backend, data, auth, AI, mobile, infrastructure, documents, research, deployment, and security.

For a deterministic baseline, run `python ../../scripts/route_forge.py "<prompt>"` from this skill directory when available. Correct its output when repository evidence or semantic context warrants it, and state the reason briefly.

Select Forge roles based on actual need:

- Always: `forge`, `forge-router`, and `forge-verification-gate` for project execution.
- Product: STANDARD or DEEP work with meaningful requirements.
- Architect: multi-domain, risky, ambiguous, or durable architecture.
- Devil: architecture challenge, security-sensitive work, or substantial final review.
- Integrator: multiple workstreams, subsystems, or contributors.

Identify reusable engineering or reasoning capabilities separately from Forge-private orchestration. Invoke `$skill-broker`, using the helper's capability IDs as a baseline, and let the AI OS registry select the minimum sufficient enabled, compatible skills. Prefer AUTHORITATIVE, then VERIFIED. Load selected skill instructions only after selection and load deeper references only when needed. Never invent a matching skill or copy it into Forge.

Inspect `../../references/skill-registry.md` and the current available skill catalog for installed external publisher skills that are not yet in the AI OS registry. Activate only relevant, discoverable skills. Do not select database, backend, cloud, AI, or deployment expertise without a task signal. Do not install a missing skill automatically unless the user's task explicitly requires that provider and installation is necessary.

Tiny tasks normally need 0 to 2 shared skills, normal features 2 to 5, and complex applications 3 to 8. These are limits for relevance, not quotas. The total may be higher once mandatory Forge roles are included.

If the broker or registry is unavailable, continue with Forge-private capabilities where safe, set broker status accurately, and expose the missing shared-capability layer in the final limitations. If one capability is missing, use another broker-selected compatible skill, proceed with internal reasoning only when safe, or report the exact missing capability. Never claim the broker was used when it was not.

Return a compact route record with mode, domains, active private roles, required shared capabilities, selected shared skills, active external skills, broker status, missing capabilities, and exclusions that prevent likely overengineering. Keep it internal unless the user requests `explain routing` or a limitation changes the result.
