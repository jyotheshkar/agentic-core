# Minister and AI OS Shared Skills

Minister owns identity, routing, conflict resolution, and final judgment. Skill Broker owns trusted shared-skill selection. The AI OS registry owns shared capability metadata.

`decision -> minister-router -> required capabilities -> skill-broker -> registry -> shared specialists -> executive-judgment`

The router passes capability IDs and task context, so future registered skills can participate without a permanent Minister skill-name list. Full skill instructions load only after selection; deep references load only when their skill requires them.

## Ownership audit

| Skill | Classification | Reason |
| --- | --- | --- |
| `minister` | MINISTER-PRIVATE | Owns Minister identity and decision workflow. |
| `minister-router` | MINISTER-PRIVATE | Owns depth and capability routing. |
| `executive-judgment` | MINISTER-PRIVATE | Sole final decision authority. |
| All nine reasoning skills | SHARED VERIFIED | User-scoped AI OS skills, not Minister-local copies or personal authoritative claims. |

No pre-existing Minister implementation was found. No private duplicates or obsolete Minister skills existed to migrate.

If the broker is unavailable, Minister may continue with private framing and judgment when safe, but must mark specialist support unavailable and reduce confidence. Missing capabilities remain explicit. Neither failure path permits invented or silently substituted skills.
