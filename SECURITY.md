# Security Policy

## Protected assets

Credentials, authentication state, private records, correspondence, local databases, and confidential employer information must remain outside Git.

## Controls

- Allowlist-only source imports with dry-run and hash manifests.
- External consumer systems retain their own access controls and runtime data. They are not imported or exercised by this core repository.
- CI uses synthetic data and cannot send messages, submit forms, or perform external actions.

## Reporting

Record suspected exposure privately. Revoke affected credentials before repository cleanup. Do not place secret values in issues or logs.
