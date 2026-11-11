# SEO Ops Studio: Multi-Platform Agent Instructions

> For **Cursor**, **Cursor Cloud Agents**, **Google Antigravity**, **Gemini CLI**,
> **Grok Build**,
> **OpenAI Codex CLI**, **Cline**, **Aider**, and any other agent harness that
> reads project-root agent instructions.
>
> Claude Code users: see `CLAUDE.md` instead.

## Cross-platform portability (v2.0.0)

Every skill in `skills/*/SKILL.md` is authored to a portable subset of the
Claude Code skill spec. Validate compatibility with your harness via:

```bash
./scripts/seo-ops run portability_check.py
```

The check confirms each `SKILL.md` has the minimum frontmatter every harness
expects (`name`, `description`, optional `model`, optional `tools`) and warns
on Claude-Code-specific features (`maxTurns`, multi-line tool list with
descriptive comments) that other harnesses may ignore but do not reject.

### Per-harness notes

| Harness | How to load seo-ops-studio |
|---|---|
| **Cursor** | Symlink or copy `skills/` and `agents/` into `.cursor/rules/`. Commands are invoked as text prompts; the harness reads `SKILL.md` body as system context. |
| **Cursor Cloud Agents** | Push the repo; Cloud Agents read `AGENTS.md` automatically at session start. |
| **Google Antigravity** | Point the workspace at this repo root; Antigravity reads `AGENTS.md` first, falls back to `skills/`. |
| **Gemini CLI** | `gemini init` in this repo loads `AGENTS.md`. Skills are activated via `activate_skill <name>` in conversation. |
| **Grok Build** | Open this repository in Grok Build. It reads `AGENTS.md` and Claude Code compatible plugins and skills without a separate layout. Use `grok inspect` to verify discovery. See the [official compatibility guide](https://docs.x.ai/build/features/skills-plugins-marketplaces). |
| **OpenAI Codex CLI** | Reads `AGENTS.md` from project root. Bash tools work as documented; some Claude-specific tool names (Read/Write/Edit) are aliased to Codex equivalents transparently. |
| **Cline** | Loads `AGENTS.md` from project root. Skills appear as system messages; subagent delegation falls back to in-context expansion. |
| **Aider** | Reads `AGENTS.md` if present; otherwise falls back to README. Aider does not support sub-agent dispatch; the seo-* skills run inline. |

### Tool-name compatibility

Where seo-ops-studio skills mention Claude Code tools (`Read`, `Write`, `Edit`,
`Bash`, `Glob`, `Grep`, `WebFetch`), each harness typically has an equivalent:

| Claude Code | Codex | Cline | Aider | Cursor / Antigravity |
|---|---|---|---|---|
| Read       | read_file        | read_file       | (inline)        | read |
| Write      | write_file       | write_file      | /add then edit  | write |
| Edit       | apply_diff       | replace_in_file | /edit           | edit |
| Bash       | bash             | execute_command | /run            | shell |
| Glob       | glob             | search_files    | (inline)        | find |
| Grep       | grep             | search_files    | /grep           | grep |
| WebFetch   | fetch / browse   | (browser tool)  | (n/a)           | fetch |

These mappings are automatic in most harnesses; we list them for transparency
in case a recipe needs a specific call.

## Overview

SEO Ops Studio is a Tier 4 SEO analysis skill with 28 sub-skills (2 SEO Ops skills + 22 core + 1 orchestrator +
1 framework integration + 2 extension mirrors), 19 sub-agents (16 core + 1 framework
integration + 2 extension mirrors), and 62 Python execution scripts.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/seo-ops-analyze audit <url>` | Full website audit with parallel subagent delegation |
| `/seo-ops-analyze page <url>` | Deep single-page analysis |
| `/seo-ops-analyze technical <url>` | Technical SEO audit (9 categories) |
| `/seo-ops-analyze content <url>` | E-E-A-T and content quality analysis |
| `/seo-ops-analyze content-brief <topic>` | Generate a content brief for a topic |
| `/seo-ops-analyze schema <url>` | Schema.org detection, validation, generation |
| `/seo-ops-analyze sitemap <url>` | XML sitemap analysis or generation |
| `/seo-ops-analyze images <url>` | Image SEO: on-page audit, SERP analysis, file optimization |
| `/seo-ops-analyze geo <url>` | AI Overviews / Generative Engine Optimization |
| `/seo-ops-analyze plan <type>` | Strategic SEO planning |
| `/seo-ops-analyze cluster <keyword>` | SERP-based semantic clustering and content architecture |
| `/seo-ops-analyze sxo <url>` | Search Experience Optimization: page-type analysis, personas |
| `/seo-ops-analyze drift baseline <url>` | Capture SEO baseline for change monitoring |
| `/seo-ops-analyze drift compare <url>` | Compare current state to stored baseline |
| `/seo-ops-analyze drift history <url>` | Show drift history over time |
| `/seo-ops-analyze ecommerce <url>` | E-commerce SEO: product schema, marketplace intelligence |
| `/seo-ops-analyze programmatic [url]` | Programmatic SEO at scale |
| `/seo-ops-analyze competitor-pages [url]` | Competitor comparison pages |
| `/seo-ops-analyze flow [stage]` | FLOW framework prompts (Find, Leverage, Optimize, Win, Local; prompts/sync utilities.) |
| `/seo-ops-analyze local <url>` | Local SEO analysis (GBP, citations, reviews) |
| `/seo-ops-analyze maps [cmd] [args]` | Maps intelligence (geo-grid, GBP audit, competitors) |
| `/seo-ops-analyze hreflang <url>` | Hreflang/i18n SEO audit, cultural profiles, content parity |
| `/seo-ops-analyze google [cmd] [url]` | Google SEO APIs (GSC, PageSpeed, CrUX, Indexing, GA4) |
| `/seo-ops-analyze backlinks <url>` | Backlink profile analysis |
| `/seo-ops-analyze backlinks setup` | Setup free backlink APIs |
| `/seo-ops-analyze backlinks verify <url>` | Verify known backlinks still exist |
| `/seo-ops-analyze dataforseo [cmd]` | Live SEO data via DataForSEO (extension) |
| `/seo-ops-analyze image-gen [use-case]` | AI image generation for SEO assets (extension) |
| `/seo-ops-analyze firecrawl [cmd] <url>` | Full-site crawling and site mapping (extension) |
| `/seo-ops-analyze ahrefs [cmd] <target>` | Ahrefs backlink and keyword data (extension) |
| `/seo-ops-analyze bing [cmd] <url>` | Bing Webmaster data and IndexNow (extension) |
| `/seo-ops-analyze profound [cmd]` | LLM brand-citation tracking (extension) |
| `/seo-ops-analyze seranking [cmd]` | AI share-of-voice tracking (extension) |
| `/seo-ops-analyze matomo [cmd] [args]` | Matomo Reporting API: GA4 alternative or supplement (extension) |
| `/seo-ops-analyze unlighthouse <url>` | Multi-page Lighthouse audits (extension) |

## Using with Cursor / Cursor Cloud

Cursor reads this file automatically. All SKILL.md files contain the full
analysis logic as natural language instructions. Python scripts in `scripts/`
provide execution capabilities.

**Running scripts directly** (Cursor doesn't have MCP):
```bash
# Page fetching with SSRF protection
./scripts/seo-ops run fetch_page.py https://example.com

# HTML parsing for SEO elements
./scripts/seo-ops run parse_html.py https://example.com

# PageSpeed Insights
./scripts/seo-ops run pagespeed_check.py https://example.com --json

# Drift baseline
./scripts/seo-ops run drift_baseline.py https://example.com

# DataForSEO (requires credentials)
DATAFORSEO_USERNAME=user DATAFORSEO_PASSWORD=pass ./scripts/seo-ops run dataforseo_merchant.py search "keyword"
```

**Cursor Cloud gotchas:**
- SSL certificates may not resolve for some domains. Investigate the certificate issue rather than disabling verification.
- Run bundled tools through `seo-ops-studio`; never call the venv interpreter directly.
- Screenshots save to `/tmp/` not CWD. Check absolute paths.

## Using with Google Antigravity

Antigravity discovers this project via `.claude-plugin/plugin.json`.
Place the repo in `~/.gemini/antigravity/plugins/seo-ops-studio/` or install via:

```bash
bash install.sh
```

## Architecture

```
skills/                    # 28 sub-skills (auto-discovered; includes the 2 SEO Ops skills)
  seo/SKILL.md            # Main orchestrator + routing
  seo-ops-cluster/            # Semantic clustering (v1.9.0)
  seo-ops-sxo/                # Search Experience Optimization (v1.9.0)
  seo-ops-drift/              # SEO drift monitoring (v1.9.0)
  seo-ops-ecommerce/          # E-commerce SEO (v1.9.0)
  seo-ops-audit/              # Full site audit
  seo-ops-page/               # Single-page analysis
  seo-ops-technical/          # Technical SEO
  seo-ops-content/            # E-E-A-T quality
  seo-ops-content-brief/      # Content brief generation
  seo-ops-schema/             # Schema.org markup
  seo-ops-sitemap/            # XML sitemaps
  seo-ops-images/             # Image optimization
  seo-ops-geo/                # AI search / GEO
  seo-ops-agentic/            # Agent readiness (Lighthouse Agentic Browsing, WebMCP)
  seo-ops-local/              # Local SEO
  seo-ops-maps/               # Maps intelligence
  seo-ops-plan/               # Strategic planning
  seo-ops-hreflang/           # International SEO
  seo-ops-google/             # Google APIs
  seo-ops-backlinks/          # Backlink analysis
  seo-ops-programmatic/       # Programmatic SEO
  seo-ops-competitor-pages/   # Competitor pages
  seo-ops-flow/               # FLOW framework integration
  seo-ops-dataforseo/         # DataForSEO (extension)
  seo-ops-image-gen/          # AI images (extension)
agents/                    # 19 subagents
scripts/                   # 62 Python scripts, including the managed runtime
schema/                    # JSON-LD templates
extensions/                # 9 MCP extensions: DataForSEO, Firecrawl, Banana, Ahrefs, SE Ranking, Profound, Bing Webmaster, Matomo, Unlighthouse
```

## Key Principles

1. **Progressive Disclosure**: Read SKILL.md for routing, load references on demand
2. **Industry Detection**: Auto-detect SaaS, e-commerce, local, publisher, agency
3. **Security**: All scripts call `validate_url()` for SSRF protection
4. **Config location**: `~/.config/seo-ops-studio/` for API credentials

## Credits

Created by [@AgriciDaniel](https://github.com/AgriciDaniel).
v1.9.0 community contributions by Lutfiya Miller, Chris Muller, Florian Schmitz,
Dan Colta, and Matej Marjanovic. See [CONTRIBUTORS.md](CONTRIBUTORS.md).
