# Registry Maintenance Workflow v0.1

All commands use `python <HOME>\.codex\ai-os\bin\aios_skills.py`.

- List: `list`
- Search: `search --capability first-principles-analysis`
- Route: `broker --task "Challenge the assumptions behind this plan"`
- Find duplicates: `duplicates`
- Validate: `validate`
- Add: `add --entry-file <one-entry.json>`
- Update: `update --entry-file <one-entry.json>`
- Disable: `disable --id <skill-id>`
- Enable after review: `enable --id <skill-id> --trust-level VERIFIED`
- Remove registry record: `remove --id <skill-id>`

Add and update validate the candidate registry before atomic replacement. Disable does not delete source. Remove deletes only registry metadata and reports `source_deleted: false`. Review current dependents before disabling, enabling, or removing. Run full validation and relevant behavioral tests after every mutation.
