# How Plugins Use Shared Skills

Shared skills live in `<HOME>\.codex\skills` and are discovered by Codex independently of any plugin. Forge, Minister, future MOA, and other plugins should keep identity and orchestration private while requesting shared expertise by skill name or through `skill-broker`.

Integration rule:

> When expertise outside plugin-private skills is required, consult the AI OS Skill Broker and shared registry. Select the minimum sufficient enabled trusted skills. Do not duplicate shared domain expertise inside the plugin.

The plugin should describe required capabilities, consult registry metadata, invoke selected user skills, and load their deeper references only when needed. A skill remains private when it encodes agent identity, private routing, integration ownership, or completion gates.

To add or update a shared skill, follow `policies/SKILL_AUTHORING_STANDARDS.md`, validate it, then add or update its registry record. Disable through the registry to stop broker routing without deleting source. Before creating a plugin skill, search capabilities and IDs to avoid duplication.

No Forge or Devil modification is required for discovery. A fresh Codex task loads newly added user skills. Future plugin revisions may copy the one-paragraph integration rule above into their private orchestration instructions.
