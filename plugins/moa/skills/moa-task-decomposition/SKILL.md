---
name: moa-task-decomposition
description: Convert a multi-step MOA outcome into a dependency-aware execution graph with bounded agent assignments and verification requirements. Use only inside an MOA workflow.
---

# MOA Task Decomposition

Create nodes only when work is genuinely separable. Each node contains: task, assigned agent, required skills, inputs, dependencies, parallelizable, expected output, verification requirement, and status.

Sequence dependent work. Parallelize independent bounded work only when it reduces latency without creating merge, safety, or context risks. A common substantive pattern is framing, Minister initial review, execution, verification, Minister final review, then completion governance.

Do not expose a large graph for trivial requests and do not create fake multi-agent complexity.
