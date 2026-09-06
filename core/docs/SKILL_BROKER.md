# Skill Broker v0.1

The broker converts a task into capability signals, considers only enabled and available compatible records, ranks relevance and trust, resolves equivalent candidates, and returns the minimum sufficient set plus rejections and missing capabilities.

Typical targets are 1 to 2 skills for tiny work, 2 to 5 for normal work, and 3 to 8 for complex work. These are context-efficiency expectations, not fixed quotas. The broker does not load every skill, install missing skills, execute untrusted scripts, or invent missing capabilities.

Use the deterministic CLI for inspectable routing. The shared `skill-broker` Agent Skill adds semantic judgment and can correct deterministic matches when the task context provides clear evidence.
