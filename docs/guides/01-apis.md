# SEO Ops Studio APIs: what to connect and why

Without APIs, SEO Ops Studio audits what it can see from the outside: HTML, headers, sitemaps and web searches. With them, every audit uses **real data** and the backlog is prioritized by measured impact. Connect them **once**: they work for all your clients.

## 1. Google: essential and free

All of these come from **one Google Cloud project with a service account** (guide: `02-service-account.md`).

| API | What it is for | Credential |
|---|---|---|
| Google Search Console API | Clicks, impressions, CTR, positions, sitemaps and indexing (about 16 months of history) | Service account, added as a user on each property |
| URL Inspection API (part of Search Console) | How Google sees each URL: indexing, chosen canonical, rendering. About 2,000 queries per day per property | Same service account |
| Google Analytics Data API (GA4) | Organic traffic, landing pages, conversions | Service account with the Viewer role on each GA4 property |
| Google Analytics Admin API | List properties and review GA4 configuration | Same service account |
| Tag Manager API (read) | Audit GTM containers: tags, triggers, Consent Mode | Service account with read access on each container |
| Chrome UX Report (CrUX) API | Real Core Web Vitals (LCP, INP, CLS) | API key |
| PageSpeed Insights API | Lighthouse without the public limit (429 errors) | API key (same as CrUX) |

**Do not use the Google Indexing API for normal pages.** Google only supports it for job postings and livestreams.

## 2. Free and complementary

| API | What it is for | Where it is stored |
|---|---|---|
| Bing Webmaster Tools API | Indexing and backlinks in Bing (which feeds Copilot) | `backlinks-api.json` → `bing_api_key` |
| Moz API (free tier) | Domain authority and links, as a fallback | `backlinks-api.json` → `moz_api_key` |
| Notion (Claude connector, Premium only) | Create and update each client's backlog | Notion connector in the Claude app |

## 3. Paid: external data

| API | What it is for | Note |
|---|---|---|
| **DataForSEO** | Real rankings by country and language, volumes, competitors, backlinks, Lighthouse at scale, LLM mentions | Pay as you go. Recommended: an account with a **business email** (higher limits, priority support, no phone verification). API credentials are not the web login |
| Semrush API | Bring Semrush data into Claude | Usually requires the Business plan plus separate API units. If you only use Semrush through its interface, you do not need it |

## 4. Optional

Firecrawl (JavaScript crawling), Ahrefs or SE Ranking (alternatives to DataForSEO: pick one), Profound (AI visibility), Gemini (image extension only). Install them from `extensions/`.

## The minimum to get started

1. A Google Cloud project with: Search Console, Analytics Data, Analytics Admin, Tag Manager, CrUX and PageSpeed.
2. A service account (its JSON file) and an API key for CrUX and PageSpeed.
3. DataForSEO.
4. Bing Webmaster Tools.

## Security

- Credentials live in `~/.config/seo-ops-studio/` (only your user can read them) or in the DataForSEO installer. Never in a client folder or in Git.
- **Do not paste keys in the chat.** If you do by mistake, regenerate the key.
- If you work with corporate clients' data, confirm with their IT team that they can grant read access to your service account, and check whether your Claude plan meets their privacy requirements.
