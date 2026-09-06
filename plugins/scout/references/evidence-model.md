# Evidence Model

Each material claim belongs in the evidence ledger with a unique claim ID and direct provenance.

## Statuses

- `VERIFIED`: current suitable Level 1 evidence directly establishes the material claim.
- `SUPPORTED`: good evidence supports the claim but is not dispositive.
- `PARTIALLY SUPPORTED`: only part is established or material conditions remain.
- `DISPUTED`: credible evidence materially disagrees.
- `UNVERIFIED`: available evidence does not establish the claim.
- `OUTDATED`: evidence may once have been correct but cannot establish current truth.
- `INFERRED`: a reasonable conclusion from cited evidence that is not directly stated.
- `UNKNOWN`: required information is unavailable or inaccessible.

Do not use numeric confidence as decoration. If confidence is reported, state the evidence basis, such as direct regulator text, independent corroboration, or unresolved version ambiguity.

## Claim discipline

Split compound claims when different sources support different parts. A source supports a claim only if the inspected page directly bears on it. Record limitations, contradicting sources, jurisdiction, publication or update date where available, and access date. An inference retains citations to its premises and must be labelled.
