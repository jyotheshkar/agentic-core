# Forge External Skill Reference

This is a maintained reference for useful installed publisher skills and known unavailable libraries. The AI OS registry at `<HOME>\.codex\ai-os\registry\skill-registry.json` is the source of truth for shared-skill discovery. Forge never vendors shared or external skills. Availability is checked at execution time because skills and plugins can be installed, removed, or updated.

| Skill or library | Publisher | Source | Category | Status | Default | Trigger and purpose | Compatibility notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `forge` suite | Jyothesh Karnam | Personal local plugin | Orchestration | Enabled | Primary | Explicit `@Forge` project delivery | Codex personal marketplace |
| `devil:devil` | Personal plugin | Installed personal marketplace | Review | Available | Conditional | Independent adversarial challenge | Preserve original plugin; do not edit |
| `openai-developers:agents-sdk` | OpenAI | Installed curated plugin | AI engineering | Available | Conditional | OpenAI Agents SDK project | Authoritative publisher |
| `openai-developers:build-chatgpt-app` | OpenAI | Installed curated plugin | Apps | Available | Conditional | ChatGPT App build | Authoritative publisher |
| `openai-developers:openai-api-troubleshooting` | OpenAI | Installed curated plugin | AI engineering | Available | Conditional | Existing OpenAI API failure | May involve paid APIs; free-first policy applies |
| `vercel:react-best-practices` | Vercel | Installed curated plugin | Frontend | Available | Conditional | React implementation or review | Authoritative framework host guidance |
| `vercel:nextjs` | Vercel | Installed curated plugin | Frontend | Available | Conditional | Next.js App Router project | Authoritative platform guidance |
| `vercel:shadcn` | Vercel curated | Installed curated plugin | UI | Available | Conditional | shadcn/ui implementation | Load only when shadcn is actually used |
| `vercel:agent-browser-verify` | Vercel | Installed curated plugin | QA | Available | Conditional | Browser-verifiable web flows | Use after implementation |
| `anthropic-skills:web-artifacts-builder` | Anthropic | Installed plugin | Frontend | Available | Conditional | Rich standalone web artifact | Do not combine with unrelated stacks |
| `anthropic-skills:anatomy-of-sde` | Anthropic | Installed plugin | Engineering | Available | Conditional | Production-grade software delivery | Use for substantial SDE work |
| `convex:convex-expert` | Convex | Installed curated plugin | Backend | Available | Conditional | Existing or chosen Convex backend | Do not select by default |
| `convex:convex-reviewer` | Convex | Installed curated plugin | Security review | Available | Conditional | Convex code review | Only for Convex projects |
| `nvidia:aiq-research` | NVIDIA | Installed curated plugin | AI research | Available | Conditional | NVIDIA AIQ deep research | Requires task relevance and configured tools |
| `spreadsheets:Spreadsheets` | OpenAI | Installed bundled plugin | Data | Available | Conditional | Spreadsheet creation or analysis | Format-specific |
| `documents:documents` | OpenAI | Installed bundled plugin | Documents | Available | Conditional | Word document creation or editing | Format-specific |
| `pdf:pdf` | OpenAI | Installed bundled plugin | Documents | Available | Conditional | PDF creation, inspection, or QA | Format-specific |
| Cloudflare plugin | Cloudflare | Recommended, not installed | Backend/deploy | Disabled | Never | Workers, D1, R2, KV, Durable Objects | Suggest installation only for an explicit Cloudflare task |
| Supabase skills | Supabase | Not currently installed | Backend/data | Disabled | Never | Supabase schema, RLS, migrations | Use only when discoverable from an authoritative source |
| Prisma skills | Prisma | Not currently installed | Data | Disabled | Never | Prisma ORM and migrations | Use only when discoverable from an authoritative source |
| Better Auth skills | Better Auth | Not currently installed | Authentication | Disabled | Never | Better Auth sessions and security | Use only when discoverable from an authoritative source |
| Hugging Face skills | Hugging Face | Not currently installed | AI/ML | Disabled | Never | Hub, models, datasets, inference | Use only when discoverable from an authoritative source |
| Expo skills | Expo | Not currently installed | Mobile | Disabled | Never | Expo and React Native | Use only when discoverable from an authoritative source |

## Selection rules

Prefer first-party publisher skills. Do not install or activate a skill because it appears in this registry. Confirm it is discoverable, compatible, relevant, and appropriately licensed before installation. Avoid overlapping skills unless each has a distinct role. The router records the chosen set and reason; all others remain inactive.
