---
name: scout-research-contract
description: Define the auditable objective, scope, freshness, source classes, unknowns, deliverable, and stopping conditions for an active Scout investigation. Skip a visible contract for trivial diagnostics.
---

# Scout Research Contract

Create a compact internal contract before meaningful evidence collection. Make it explicit enough to audit for DEEP and CRITICAL work.

## Required fields

```text
RESEARCH OBJECTIVE
DOWNSTREAM DECISION OR USE
CORE QUESTION
SUBQUESTIONS
IN-SCOPE CLAIMS
OUT-OF-SCOPE CLAIMS
JURISDICTION
TIMEFRAME
FRESHNESS REQUIREMENT
SOURCE CLASSES REQUIRED
KNOWN CONSTRAINTS
USER-PROVIDED ASSUMPTIONS
DECISION-REVERSING UNKNOWNS
EXPECTED DELIVERABLE
STOPPING CONDITIONS
```

Convert vague objectives into answerable questions without silently changing the user's goal. Record assumptions as user-provided, not verified. Put contact, application, purchasing, implementation, and final strategic judgment out of scope unless a separately authorised workflow owns them.

Define freshness per material claim class. State jurisdiction when rules, eligibility, policy, or institutional practice depends on it. Stopping conditions must allow a reliable answer, an explicit unresolved result, or a precise blocker without infinite search.

## Failure handling

If the core question or downstream use is genuinely unknowable from context and materially changes the investigation, ask one concise question. Otherwise choose a reversible interpretation and label it. If scope expands during research, update the contract explicitly rather than drifting.

## Output

Return the populated contract and a one-line statement of what the investigation will not establish. The contract constrains `$scout-investigation-planner` and `$scout-completion-gate`.
