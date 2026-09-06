---
name: scout-synthesis
description: Convert a validated Scout evidence ledger into a decision-ready research answer while preserving fact, support, inference, contradiction, freshness, and unknowns. Do not issue Minister's strategic verdict.
---

# Scout Synthesis

Synthesize only after material claims are in the ledger and contradiction checks are complete. Use [evidence-model.md](../../references/evidence-model.md) to preserve status language.

## Required result

```text
RESEARCH ANSWER
EXECUTIVE SUMMARY
CONFIRMED FACTS
SUPPORTED FINDINGS
CONDITIONAL OR INFERRED FINDINGS
CONTRADICTORY EVIDENCE
UNRESOLVED QUESTIONS
DECISION-REVERSING UNKNOWNS
SOURCE AND FRESHNESS NOTES
IMPLICATIONS FOR MINISTER OR FORGE
RECOMMENDED NEXT EVIDENCE ACTION
```

Add a compact Claim, Status, Best source, Freshness, Limitation table when several claims matter. Keep citations beside the claims they support and follow [citation-contract.md](../../references/citation-contract.md).

## Decision rules

- State what the evidence establishes before interpretation.
- Label every inference and preserve its evidence premises.
- Explain how unresolved contradiction or stale evidence could change the downstream decision.
- Distinguish programme or company facts from user eligibility, official policy from practice, and general capability from version-specific support.
- Give Minister evidence and unknowns, not a final option choice.
- Give Forge verified technical facts and constraints, not a final architecture.

## Failure handling

If the ledger is incomplete, return it to `$scout-evidence-ledger`. If a material contradiction was not analyzed, invoke `$scout-contradiction-resolution`. If evidence cannot support the requested answer, synthesize an honest `INSUFFICIENT EVIDENCE` result and state what would reverse it.

## Output boundary

Do not overstate exhaustiveness, hide limitations, or use source volume as a proxy for certainty. The synthesis remains subject to `$scout-completion-gate`.
