# AI OS Shared Skill Architecture v0.1

Codex native user skill discovery remains the runtime. Shared skills live directly under `<HOME>\.codex\skills`; plugin-private skills remain under their plugin. The AI OS registry adds capability, trust, status, compatibility, and lifecycle metadata without replacing Codex.

Flow:

`task -> skill-broker -> registry metadata -> minimum sufficient skill set -> native skill loading`

The broker reads metadata before full skill content. Full `SKILL.md` and conditional references are loaded only for selected skills. The current Windows host cannot create symbolic links without administrator privileges, so v0.1 uses direct native paths. No database, service, API, dashboard, or package manager is required.
