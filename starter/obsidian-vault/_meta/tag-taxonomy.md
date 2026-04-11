# Tag Taxonomy

> **Rule:** Every doc gets 3-7 tags from this taxonomy. Use nested `/` syntax.
> Project-specific identifiers belong in `project:` frontmatter, not tags.
> Extend this file as your vault grows — keep it as the single source of truth.

## Domains

### `ai/`
| Tag | Use for |
|-----|---------|
| `ai/agents` | Agentic workflows, agent frameworks, subagents |
| `ai/architecture` | Agent system design, multi-agent patterns |
| `ai/ml` | Machine learning, models, training |

### `tech/`
| Tag | Use for |
|-----|---------|
| `tech/web` | Web dev, APIs, frontend, backend |
| `tech/mobile` | iOS, Android, mobile dev |
| `tech/infra` | Cloud, deployment, databases, networking |
| `tech/security` | Cybersecurity, auth patterns, pen testing |
| `tech/devtools` | Developer tools, SDKs, CLI, DX |
| `tech/mcp` | Model Context Protocol servers and tools |

### `product/`
| Tag | Use for |
|-----|---------|
| `product/design` | UX, UI, gamification, animation |
| `product/growth` | User acquisition, retention, funnels |
| `product/pkm` | Personal knowledge management, Obsidian |

### `business/`
| Tag | Use for |
|-----|---------|
| `business/strategy` | Market analysis, competitive intelligence |
| `business/model` | Revenue models, pricing, moats |
| `business/finance` | Financial models, investment, valuation |
| `business/legal` | Contracts, corporate law, compliance |

### `personal/`
| Tag | Use for |
|-----|---------|
| `personal/career` | Career development, skills, growth |
| `personal/health` | Health tracking, protocols |
| `personal/strategy` | Life strategy, financial independence |

### `research/`
| Tag | Use for |
|-----|---------|
| `research/pattern` | Reusable patterns and mental models |
| `research/decision` | Decision records and rationale |

---

## Guidelines

- Tags describe what the document **is about**, not what it mentions in passing
- Avoid single-word generic tags: `code`, `notes`, `misc`
- Vendor/company names go in content, not tags
- Feature-level tags (`ooda`, `spaced-repetition`) are covered by parent domain tags
- Status tags (`decision`, `meeting`) belong in the `type:` frontmatter field
