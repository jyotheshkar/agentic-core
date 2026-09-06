---
name: scout-evidence-ledger
description: Maintain claim-level provenance, direct support, freshness, contradiction, limitation, and evidence status during an active Scout investigation. Do not use a source list without claim alignment as a substitute.
---

# Scout Evidence Ledger

Create one entry for each material claim. Split compound claims when evidence supports only part.

## Required fields

```text
CLAIM ID
CLAIM
CLAIM TYPE
SOURCE
SOURCE OWNER
SOURCE TYPE
SOURCE URL OR LOCAL PATH
PUBLICATION DATE
LAST UPDATED DATE
ACCESS DATE
JURISDICTION
DIRECT SUPPORT
LIMITATIONS
CONTRADICTING SOURCES
FRESHNESS STATUS
CONFIDENCE
EVIDENCE STATUS
NOTES
```

Apply the status definitions in [evidence-model.md](../../references/evidence-model.md). `VERIFIED` requires suitable current Level 1 evidence that directly establishes the claim. `INFERRED` requires an explicit inference label and citations to its premises. A search result, snippet, copied listing, or inaccessible page cannot be final direct support.

Use [freshness-policy.md](../../references/freshness-policy.md) for current claims and [citation-contract.md](../../references/citation-contract.md) before adding provenance. Record unavailable dates as unknown, never invent them. Confidence must explain its basis rather than provide artificial precision.

## Decision rules

- Downgrade a claim when the source supports only part of it.
- Mark credible disagreement `DISPUTED` until `$scout-contradiction-resolution` resolves it.
- Mark a once-valid but stale current source `OUTDATED`.
- Keep unavailable material `UNKNOWN` or `UNVERIFIED` rather than filling gaps by inference.
- Preserve user-provided claims as claims until independently established.

## Output and failure handling

Return the ledger plus validation errors. Duplicate claim IDs, missing provenance, invalid status, unlabelled inference, or `VERIFIED` without direct Level 1 support blocks completion. Do not remove an adverse source because it weakens the preferred conclusion.
