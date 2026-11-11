# SEO Ops Studio

**Full SEO audits, with real data and a client-ready PDF, from Claude Code.**

Type `/seo-ops audit https://yoursite.com` and get a report with a Health Score, prioritized issues, an action plan and a PDF that lists the data sources used (and the ones that were not).

> 28 sub-skills and 19 sub-agents. MIT licensed. Based on [claude-seo](https://github.com/AgriciDaniel/claude-seo) by Daniel Agrici (see `CREDITS.md`).

---

## What's included

- **Guided API onboarding** (`/seo-ops-setup`): creates the credential templates, explains what each API is for and what it costs, walks you through the Google service account and verifies the connection. It never asks for keys in the chat.
- **Full audit with PDF** (`/seo-ops audit <url>`): parallel specialists (technical, content, schema, performance, GEO, images, sitemap…), a weighted Health Score and a PDF with the real sources.
- **One-off analyses** (`/seo-ops-analyze …`): technical, content (E-E-A-T), schema, sitemap, Core Web Vitals, GEO for AI search, hreflang, local SEO, e-commerce, backlinks, keyword clusters and more.
- **Connected APIs**: Search Console, GA4, CrUX and PageSpeed (free), DataForSEO (pay as you go), Bing Webmaster and Moz (free).

## Commands

| Command | What it does |
|---|---|
| `/seo-ops` | Menu. Launches onboarding on first use |
| `/seo-ops-setup` | Connects and verifies the APIs |
| `/seo-ops audit <url>` | Full audit: report + PDF in `audits/<domain>/` |
| `/seo-ops status` | Which APIs are connected and what is missing |
| `/seo-ops-analyze …` | One-off engine analyses (`technical`, `content`, `schema`, `geo`, `hreflang`, `local`, `page`…) |

## Installation

Requires [Claude Code](https://claude.com/claude-code) and Python 3.11 to 3.14 (the plugin creates its own isolated environment).

```bash
/plugin marketplace add juanpulag/seo-ops-studio
/plugin install seo-ops-studio@seo-ops-studio
```

Restart Claude Code and, in any folder, type `/seo-ops`.

> Every command starts with `/seo-ops`, so SEO Ops Studio can live alongside the original claude-seo.

To update:

```bash
/plugin marketplace update seo-ops-studio
/plugin update seo-ops-studio@seo-ops-studio
```

## Getting started

1. `/seo-ops-setup`: connect at least Google (service account + API key). It also works with no APIs, but performance and traffic data will be estimates.
2. Open Claude Code in the folder where you want to keep your audits.
3. `/seo-ops audit https://yoursite.com`.

Guides in `docs/guides/`:
- `01-apis.md`: which APIs to connect and why.
- `02-service-account.md`: create the Google service account step by step.

## Other languages

The plugin is in English, and Claude works in whatever language you use. Just ask: "write the report and the PDF in Spanish".

## SEO Ops Studio Premium

For consultants and agencies managing **multiple clients and many sites**. Adds the operating methodology:

| Basic (this repo) | Premium |
|---|---|
| Audit + PDF for one site | Per-client audit, compared against the client's other sites |
| Report with findings | Each finding becomes a task in a **Notion backlog**, with evidence, acceptance criteria and how to validate, without duplicates |
| Not included | Detection of **platform** issues that repeat across sites (one task, not thirty) |
| Not included | One folder, one memory and one Notion **per client** |
| Not included | **Re-audits** that test each task on the live site, propose closing or reopening it, and produce a progress report for the client |
| Not included | Calculated priority (impact × severity × scope ÷ effort) and a panel of open tasks by country and severity |

Interested? Open an [issue](https://github.com/juanpulag/seo-ops-studio/issues) titled "Premium".

## Security

- Credentials live only in `~/.config/seo-ops-studio/` and in the DataForSEO connector. Never in your project or in Git.
- The plugin never asks for keys in the chat and never prints them.
- Details in `SECURITY.md` and `PRIVACY.md`.

## Credits

The audit engine comes from **claude-seo** (MIT) by Daniel Agrici, and the FLOW framework (CC BY 4.0) is by the same author. Details in `CREDITS.md` and `LICENSE`.
