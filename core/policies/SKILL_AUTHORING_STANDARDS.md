# Shared Skill Authoring Standards v0.1

## Ownership boundary

Shared skills contain reusable domain knowledge. Plugin-private skills contain agent identity, routing, integration, and completion behavior. Do not duplicate shared domain knowledge inside plugins.

## Required structure

Each shared skill lives directly under `<HOME>\.codex\skills\<skill-id>` and contains a valid `SKILL.md` whose folder name, frontmatter name, and registry ID match. Use lowercase hyphenated semantic versions. Add `agents/openai.yaml` for clear UI metadata. Add references or scripts only when they materially improve the skill.

Keep `SKILL.md` focused on purpose, activation, workflow, output, boundaries, and reference routing. Put conditional depth in linked references. Do not create empty resources or copied manuals.

## Versioning

Use semantic versioning. Patch for compatible corrections, minor for backward-compatible capability additions, major for incompatible behavior or registry contracts. The registry holds the active version and source. Preserve prior source outside the active skill root only when rollback is genuinely needed; this is not a package manager.

## Lifecycle

1. Author or revise the skill and registry entry.
2. Run the official `quick_validate.py` against the skill.
3. Run `aios_skills.py validate` and relevant behavioral tests.
4. Review provenance, license, scripts, network, secrets, destructive behavior, and prompt-injection exposure.
5. Assign EXPERIMENTAL until evidence supports VERIFIED or authoritative provenance is confirmed.
6. Update `last_validated` and version only after successful validation.

Disabling changes registry state and trust to DISABLED; it does not delete source. Removal deletes the registry record only. Delete source separately only with explicit, scoped authorization.
