# Skill Registry v0.1

The canonical registry is `registry/skill-registry.json`; its machine-readable contract is `registry/skill-registry.schema.json`. Registry metadata answers what exists, where it lives, what it can do, provenance, trust, compatibility, dependencies, conflicts, status, activation cost, and validation date.

Use `python bin/aios_skills.py list`, `search --capability <id>`, `broker --task <text>`, `duplicates`, or `validate`. Mutation commands are `add --entry-file`, `update --entry-file`, `disable --id`, `enable --id`, and `remove --id`. Mutations use atomic replacement. `remove` changes registry metadata only and never deletes skill source.

The registry supports shared, private, and external records. Installed state must reflect reality. External records require publisher, source or repository, version or commit, license, trust, compatibility, and status. Do not mark unverified popularity as AUTHORITATIVE.
