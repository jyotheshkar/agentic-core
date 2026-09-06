# Scout Architecture

Scout is Agentic Core's research and evidence authority. It is selected by MOA from the Agent Registry and consumes canonical shared methods through the Skill Broker.

`user -> MOA -> Minister initial judgment when required -> Scout -> evidence pack -> Minister or Forge -> MOA completion governance`

## Authority boundaries

| Component | Owns | Does not own |
|---|---|---|
| MOA | scope, routing, sequencing, rework, completion governance | research findings or engineering internals |
| Minister | strategic judgment, option selection, risk acceptance | evidence gathering or implementation |
| Scout | research contract, investigation, provenance, freshness, contradictions, evidence completeness | final strategic verdict or software architecture |
| Forge | technical architecture, implementation, engineering verification | source truth outside its verified implementation evidence |
| Skill Broker | minimum sufficient reusable expertise | agent authority |

Scout's eight private skills coordinate research state and handoffs. Shared `research-planning`, `source-discovery`, `source-verification`, `evidence-epistemics`, and `research-synthesis` remain under `<HOME>\.codex\skills` and are never copied into this plugin.

Direct plugin-to-plugin process invocation is not exposed by the current platform. MOA composes installed skills inside one Codex task, so runtime orchestration is recorded as `EMULATED`.

## Maintenance

Keep private orchestration in this plugin and reusable methodology in the canonical Shared Skill Library. After a Scout source change, validate all private skills and the plugin, run `scripts/test_scout.py`, update only the Codex cachebuster with the plugin-creator helper, reinstall `scout@personal` through the desktop runtime, then verify native discovery, Agent Registry version agreement, current-cache parity, and the complete regression set. Do not hand-edit marketplace records during an update.

When routing or authority changes, update the narrow MOA contract, use a separate MOA cachebuster, reinstall MOA, and rerun its full suite. Do not modify Minister or Forge merely to document a handoff.
