# Completion Contract

Scout may claim completion only when the result proportionately satisfies all applicable conditions:

- the objective is answered or explicitly unresolved
- material claims have provenance
- current claims use current evidence
- primary or authoritative sources were preferred where available
- material contradictions were checked and exposed
- decision-reversing unknowns remain visible
- inference is labelled
- citations point to supporting pages, not search results
- accessible source pages were inspected rather than relying on snippets
- no quote, date, or URL was fabricated
- jurisdiction and access dates are recorded where needed
- the result does not overstate exhaustiveness
- the evidence pack matches the research contract
- the receiving authority has enough bounded context

Statuses:

- `COMPLETE`: all material checks pass and no material limitation is named or remains.
- `COMPLETE WITH LIMITATIONS`: the answer is usable and every material limitation is named.
- `PARTIAL`: some research questions or validation checks remain incomplete.
- `BLOCKED`: a required resource, permission, tool, or external condition is inaccessible.
- `INSUFFICIENT EVIDENCE`: available evidence cannot support a reliable answer and the missing evidence is identified.

Missing citations, stale current evidence, or unresolved material contradictions prevent unqualified `COMPLETE`.

Any non-empty material limitations field makes `COMPLETE` invalid. Use `COMPLETE WITH LIMITATIONS` only when the remaining limitation is explicit and the answer is still usable.
