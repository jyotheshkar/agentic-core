# Security Policy

## Protected assets

Credentials, authentication state, private job records, CVs, correspondence, local databases, and confidential employer information must remain outside Git.

## Controls

- Allowlist-only source imports with dry-run and hash manifests.
- Owner-only Site access for Job Searching Agent.
- D1 runtime data is separate from repository fixtures.
- Prepared statements and server-side authorization protect writes.
- CI uses synthetic data and cannot send email, contact employers, or submit applications.

## Reporting

Record suspected exposure privately. Revoke affected credentials before repository cleanup. Do not place secret values in issues or logs.
