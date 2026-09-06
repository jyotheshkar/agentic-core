# Forge and AI OS Shared Skills

Forge owns project orchestration. Skill Broker owns trusted shared-skill selection. The AI OS registry owns current shared capability metadata. Selected shared skills provide reusable methods; they do not replace Forge Architect, Forge Integrator, or Forge Verification Gate authority.

## Routing contract

`task -> forge-router -> required capabilities -> skill-broker -> AI OS registry -> minimum sufficient shared skills -> Forge execution -> forge-devil -> forge-integrator -> forge-verification-gate`

The router passes capability IDs and the task to the broker. Selection is registry-driven, so a future enabled skill becomes discoverable without a permanent Forge skill-name list. Full shared instructions are loaded only after selection. Supporting references are loaded only when their skill says they are needed.

If the broker is unavailable or invalid, Forge continues with private capabilities when safe, records that the broker was not used, and reports the unavailable shared-capability layer. A missing capability is reported by ID. Forge must not invent, enable, install, or privately copy a skill to hide the gap.

## Ownership audit

| Current skill | Classification | Reason |
| --- | --- | --- |
| `forge` | FORGE-PRIVATE | Owns end-to-end Forge delivery and commands. |
| `forge-router` | FORGE-PRIVATE | Owns Forge execution mode and orchestration routing. |
| `forge-product` | FORGE-PRIVATE | Produces the Forge Product Contract. |
| `forge-architect` | FORGE-PRIVATE | Chooses project architecture and reconciles domain advice. |
| `forge-devil` | FORGE-PRIVATE | Applies Forge-specific independent review and completion severity. |
| `forge-integrator` | FORGE-PRIVATE | Owns final engineering coherence and decisions. |
| `forge-verification-gate` | FORGE-PRIVATE | Enforces Forge completion claims. |
| `first-principles` | EXTERNAL/AUTHORITATIVE | Verified shared AI OS reasoning skill outside the plugin. |
| `evidence-epistemics` | EXTERNAL/AUTHORITATIVE | Verified shared AI OS evidence skill outside the plugin. |
| `systems-thinking` | EXTERNAL/AUTHORITATIVE | Verified shared AI OS systems skill outside the plugin. |

No current Forge skill is DUPLICATE, OBSOLETE, or a SHARED-CANDIDATE. The private skills contain orchestration contracts, not generic reusable domain manuals.

## Diagnostics

`@Forge skills` and `@Forge capabilities` show Forge-private skills, shared skills, installed external skills, trust state, and broker status. `@Forge explain routing: <task>` shows the route and selection reasons without executing the task. Ordinary responses omit these diagnostics unless a missing capability or broker failure affects the result.
