# Phase 2.002: Role Qualification Contract

## Status

VERIFIED WITH LIMITATIONS

## Goal

Implement an explicit, manual-only qualification gate that separates role fit from confidence to prepare an application. Preserve the existing `APPLY`, `VERIFY_FIRST`, and `SKIP` workflow.

## Scope

- Add `application_confidence` to the operational job-evidence contract.
- Require an explicit `APPLY` decision and confidence of at least 80 before a role is package-eligible.
- Keep imports idempotent, preserve application status, and retain the required dedupe order.
- Add focused unit and contract tests.
- Correct CI package discovery for the imported site layout.

## Acceptance Criteria

1. A confidence value is validated as an integer from 0 through 100.
2. The package-eligibility result is deterministic and fail-closed for `VERIFY_FIRST`, `SKIP`, unknown sponsorship, or confidence below 80.
3. The qualification logic never submits, contacts, monitors, or automates an external system.
4. Existing import and application-status behavior remains intact.
5. Tests demonstrate the confidence boundary, country preservation, and manual-only constraints.

## Current Evidence

- Phase 2.001 imported 165 source files into the task worktree, excluding dependency directories, runtime state, databases, environment files, logs, and credential-like file names.
- The existing product validates `fit_score`, decision, sponsorship, and UK country, but has no `application_confidence` field or package-eligibility helper.
- Existing application events and audit events already support a later user-supplied status timeline.

## Affected Paths

- `products/job-searching-agent/site/lib/domain.ts`
- `products/job-searching-agent/site/lib/server/ingestion.ts`
- `products/job-searching-agent/site/db/schema.ts`
- `products/job-searching-agent/site/drizzle/**`
- `products/job-searching-agent/site/tests/**`
- `.github/workflows/ci.yml`

## Rollback and Recovery

- Revert only the files listed above and this phase record from the task worktree.
- Do not alter the primary source worktree.
- If interrupted, rerun the relevant product tests before changing the contract again.

## Verification Evidence

- `npm run test`: PASS, 19 tests across four files.
- `npm run lint`: PASS.
- `npm run build -- --outDir dist-phase-2-verification`: PASS.
- Drizzle generated `0001_misty_aqueduct.sql`, adding the non-null `application_confidence` field.
- Shared-library regression: PASS, 11 tests.
- Repository contract regressions: PASS, 3 tests.
- Limitation: `scripts/validate-repository.py` correctly rejects local `node_modules` and generated directories after dependency installation/build. CI runs that validation before product installation; local final validation must use a clean worktree or a future isolated build directory.
