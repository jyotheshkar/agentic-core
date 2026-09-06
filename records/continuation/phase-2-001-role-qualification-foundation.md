# Phase 2.001: Role Qualification Foundation

## Status

IN PROGRESS

## Goal

Create a safe, testable foundation for the Job Searching Agent role-qualification workflow. The workflow must remain manual-application only and must preserve evidence, deduplication, user-managed application state, and UK country reporting.

## Scope

- Import the approved, sanitised Job Searching Agent source into this task worktree without altering the primary worktree.
- Add the smallest justified contract changes for role qualification and application confidence.
- Correct test discovery so the product test suite is exercised by repository CI once the product is tracked.
- Add deterministic and adverse-case tests for the new contract.

## Acceptance Criteria

1. The task worktree contains no credentials, private job records, CVs, application documents, browser data, or Amazon confidential information.
2. Role records distinguish `fit_score` from `application_confidence`.
3. Only an explicit `APPLY` decision with confidence at least 80 can be eligible for manual package preparation. No code may submit an application or contact an employer.
4. Dedupe follows official job ID, then official URL, then normalised company, role, location, and source.
5. Imports cannot overwrite user-managed application status.
6. CI discovers the actual product package and executes its check suite when the product exists.
7. Relevant deterministic, adverse-case, and repository checks pass, or any blocker is recorded precisely.

## Current Evidence

- 2026-09-06 read-only inventory: MOA live health PASS; Scout live health PASS with 29/29 source/cache parity; live shared Skill Broker PASS with 39 available skills.
- Committed baseline reports 75/75 deterministic tests. This is inherited evidence only and must be revalidated after changes.
- The primary worktree contains untracked Job Searching Agent source under `products/job-searching-agent`; it is reference material and will not be modified by this phase.
- Existing product ingestion uses canonical identity in the required order, but its payload does not yet distinguish application confidence from fit score.
- Existing repository CI points at `products/job-searching-agent/package.json`; the current product package is under `products/job-searching-agent/site/package.json`.

## Affected Paths

- `records/continuation/phase-2-001-role-qualification-foundation.md`
- `products/job-searching-agent/**` after allowlist import into this task worktree
- `.github/workflows/ci.yml`
- `records/imports/job-searching-agent-protected-reference.json`
- `scripts/import-job-searching-agent/**`

## Constraints

- No automatic application, browser automation, CAPTCHA handling, employer/recruiter contact, email sending, portal monitoring, payment, or deployment.
- Database is the future operational source of truth. CSV and Google Sheets are import, export, and audit formats.
- Use only synthetic data in tests and reports.
- Do not change the primary worktree or overwrite user-owned untracked source.

## Rollback and Recovery

- All changes are local and uncommitted until verification is complete.
- Revert only files created or modified by this phase in this task worktree.
- The primary worktree remains an untouched reference source.
- If work stops, resume by reading this record, checking `git status`, and rerunning the recorded deterministic checks before the next change.
