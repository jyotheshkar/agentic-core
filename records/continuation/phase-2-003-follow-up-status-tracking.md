# Phase 2.003: Follow-Up and Status Tracking

## Status

VERIFIED WITH LIMITATIONS

## Goal

Complete the existing manual application-status feature with read-only timeline and follow-up views. All status changes remain explicitly user supplied through the authenticated application update route.

## Scope

- Read the append-only application event history.
- Surface follow-up work from persisted `follow_up_at` values.
- Preserve existing rejection and interview status values.
- Do not add portal monitoring, account login, email delivery, recruiter contact, or automated status changes.

## Acceptance Criteria

1. Timeline reads are ordered, bounded, and contain only persisted application events.
2. Follow-up reads return only due or scheduled manual work, with no external action.
3. Interview and rejection statuses remain visible in the same application lifecycle.
4. Route reads do not mutate data; updates keep the existing owner-authentication requirement.
5. Tests cover timeline ordering, no-follow-up cases, and adverse lifecycle status cases.

## Current Evidence

- Existing `updateApplication` writes `application_events` and `audit_events` for every status update.
- Applications already contain `follow_up_at`, `outcome`, `notes`, and lifecycle statuses including `INTERVIEW` and `REJECTED`.
- No route currently exposes a timeline or a follow-up queue.

## Affected Paths

- `products/job-searching-agent/site/lib/server/repository.ts`
- `products/job-searching-agent/site/app/api/**`
- `products/job-searching-agent/site/tests/**`

## Rollback and Recovery

- Revert only this phase's files in the task worktree.
- Existing write behavior stays unchanged; the phase adds read-only projections only.
- Resume by checking this record, then running the relevant product tests.

## Verification Evidence

- `npm run test`: PASS, 21 tests across five files.
- `npm run lint`: PASS.
- `npm run build -- --outDir dist-phase-2-followup-verification`: PASS.
- Limitation: API behavior is build-verified and unit-tested at the pure-projection layer. It has not been exercised against a live D1 database or authenticated deployment, which remain outside the approved scope.
