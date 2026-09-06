# Job Search Learning Agent

## Decision

This is a rules-first, **shadow-only** learning layer. It reads the existing queue, exports, run logs and preparation records as evidence. It writes only under `learning_agent/`. It cannot write to `data/jobs.sqlite3`, change a queue status, send an application, contact an employer, or approve a submission.

The non-ML baseline is the current deterministic queue: hard gates first, then existing score descending, then earliest observation. The learning layer may only emit a next-day `PRIORITIZE_RESEARCH`, `KEEP_BASELINE`, or `NO_ACTION` suggestion. It never produces a live ranking change. `NO_ACTION` is mandatory if evidence is incomplete, data are insufficient, a record has any failing hard gate, or its proposed action is outside the action mask.

## Non-negotiable controls

- Deterministic gate results remain authoritative: live vacancy, deduplication, exact sponsor entity, role-level sponsorship, qualifying salary, occupation eligibility, and mandatory eligibility.
- Unknown is not a pass. The system never creates a training label from missing evidence.
- Only explicit queue records, Jyo-confirmed submissions, and later explicit outcome labels are counted. It never infers applications, offers, interviews, rejections, or outcomes.
- The policy is shadow-only. Any possible promotion needs a frozen evidence ledger, baseline comparison, regression tests, rollback plan, and explicit written Jyo approval.
- No paid APIs, credit purchases, employer contact, or automatic applications are in scope.

## Nightly operation

At 00:00 Europe/London, run:

```powershell
python -B learning_agent/review.py
```

By default it analyses the completed prior London day, writes a dated JSON review and Markdown report, and appends a hash-chained evidence-ledger event. It reports data sufficiency honestly. `--date YYYY-MM-DD` is for a completed historical day only. `--dry-run` prints the report without writing it.

## DQN readiness

The model contract is deliberately present but inactive: state features and allowable actions are in `schema.json`; transitions require an explicit later outcome label and immutable evidence references. Training is blocked until the review finds at least 100 explicitly-labelled eligible transitions, at least 20 positive and 20 negative labels, and a temporally held-out comparison that beats the deterministic baseline without safety regressions. These thresholds are conservative operating gates, not evidence that 100 records would be sufficient for a deployable DQN.

## Rollback and approval

`build-status.json` records the release state. A policy release can only move from `SHADOW_BASELINE` to `PROPOSAL_PENDING_JYO_APPROVAL`; this implementation has no code path to make a proposal live. To roll back, set the release to `ROLLED_BACK`, preserve the ledger, and continue using the deterministic baseline.
