# Minister

Minister is the decision authority of the Personal AI OS. It frames a choice, routes the minimum sufficient shared reasoning skills through Skill Broker, resolves disagreement, and recommends what to do.

```text
@Minister Should I accept this offer or stay in my current role?
```

Inspect available capabilities with `@Minister skills`. Inspect a route without deciding with `@Minister explain routing: <decision>`.

Minister contains only three private skills: `minister`, `minister-router`, and `executive-judgment`. Reusable reasoning remains under the user-level AI OS skill root.
