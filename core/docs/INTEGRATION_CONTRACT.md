# Future Plugin Integration Contract v0.1

1. Keep agent identity, private routing, integration ownership, and verification gates inside the plugin.
2. Keep reusable domain knowledge in user-scoped shared skills.
3. When outside expertise is required, consult `skill-broker` or the registry and request explicit capabilities.
4. Select the minimum sufficient set of enabled, available, compatible skills.
5. Prefer AUTHORITATIVE, then VERIFIED, unless a documented compatibility or relevance issue applies.
6. Never route to DISABLED skills or required dependencies that are disabled or unavailable.
7. Do not execute untrusted scripts automatically.
8. Report missing capability instead of inventing an installed skill.
9. Load full skill content and references only after selection.
10. Preserve normal user approval, credential, payment, and irreversible-action boundaries.
