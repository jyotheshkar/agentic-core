# Manual Resume Procedure

This project does not assume automatic continuation after a Codex usage reset, interruption, or closed session.

1. Read the newest file under `records/continuation/`.
2. Inspect `git status --short` and preserve all unrelated user changes.
3. Read `docs/phase-2/PHASE_2_COMPLETION.md` for the last verified evidence and open limitations.
4. If product work resumes, install dependencies only inside `products/job-searching-agent/site/node_modules`, which remains ignored.
5. Run `npm run test`, `npm run lint`, and a fresh-output `npm run build -- --outDir <ignored-local-directory>`.
6. Run shared-library and repository contract tests. Run the repository validator before installing dependencies, or in a clean source-only worktree, because it intentionally rejects generated directories.
7. Create a new continuation record before the next implementation phase. Record scope, acceptance criteria, current evidence, affected paths, rollback, and recovery.
8. Stop for credentials, payment, deployment, D1 promotion, live personal data, external communication, public release, destructive action, or any unresolved critical/high risk.
