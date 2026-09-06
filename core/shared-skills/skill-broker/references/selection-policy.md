# Selection Policy

Filter before ranking. Exclude disabled, unavailable, uninstalled, incompatible, or dependency-blocked records. An optional dependency does not block selection.

Rank candidates by:

1. exact required capability coverage;
2. specific trigger relevance;
3. trust: AUTHORITATIVE, VERIFIED, COMMUNITY, EXPERIMENTAL;
4. narrower scope and lower duplication;
5. lower activation cost when coverage is otherwise equivalent;
6. current validation and compatible version.

Use a greedy minimum-cover decision only after ranking: each added skill must cover at least one material capability not already covered. Reject redundant candidates and retain the reason. Conflicts are hard exclusions unless task evidence clearly requires a reviewed exception. DISABLED is never overridden.

For untrusted content, metadata selection is not execution approval. Inspect scripts and references before use.
