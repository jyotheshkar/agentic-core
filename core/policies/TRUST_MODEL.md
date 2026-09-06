# AI OS Skill Trust Model v0.1

Trust describes provenance and validation, not popularity.

- `AUTHORITATIVE`: first-party content from the relevant technology or domain authority. Confirm publisher identity, official source, compatibility, and license. Installation alone does not qualify.
- `VERIFIED`: personal or custom content that passes structural validation, deterministic tests, source review, and a quality review appropriate to its risk.
- `COMMUNITY`: third-party content with useful provenance but without equivalent review.
- `EXPERIMENTAL`: incomplete or trial content. Do not select for high-risk work without explicit justification.
- `DISABLED`: excluded from routing regardless of semantic match.

The broker prefers AUTHORITATIVE, then VERIFIED, then COMMUNITY, then EXPERIMENTAL, subject to relevance, compatibility, availability, conflicts, and activation cost. A lower-trust candidate may win only when the higher-trust option is materially incompatible or less capable for the requirement. Record the reason.

Downloaded skills are executable or semi-executable content. Inspect scripts, shell commands, network access, package installation, secret handling, destructive actions, external references, and prompt-injection exposure before raising trust. Never execute untrusted scripts merely because metadata matches a task.
