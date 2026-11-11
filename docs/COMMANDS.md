# Commands Reference

## Overview

All SEO Ops Studio commands start with `/seo-ops-analisis` followed by a subcommand.

## Page-fetching script

Use `"${CLAUDE_PLUGIN_ROOT}/scripts/seo-ops" run fetch_page.py https://example.com --json` for structured
retrieval. Both the raw path (default, `--render never`) and the rendered path
(`--render auto` or `--render always`) emit JSON through the same
`render_page._json_summary` contract, so the two share one key set: `url`,
`status_code`, `content`, `raw_content`, `is_spa`, `extracted_text`,
`publication_date`, `accessibility_tree`, `accessibility_error`,
`accessibility_partial`, `headers`, `redirect_chain`, `console_errors`,
`render_diagnostics`, `render_engine`, `render_ms`, `mode_used`, `error`,
`structured_data`, and `truncation`. The raw path fills renderer-only fields
(`is_spa`, `extracted_text`, `render_engine`, ...) with `None`/empty defaults.
Fetch errors still emit JSON and exit 1; successful fetches exit 0. HTTP status
codes are reported without changing this behavior.

Pass `--max-text N` to cap the `content`, `raw_content`, and `extracted_text`
fields at N characters each; `truncation.fields` reports the original and
returned character counts per field. `--max-text 0` (default) keeps full text.

Combine `--json --output page.html` to save successful HTML while keeping JSON
on stdout. `output_written` indicates whether HTML was saved. On fetch errors,
the output file is left untouched. Without `--json`, existing text output is
unchanged.

## Command List

### `/seo-ops-analisis setup`

Explicitly create or refresh the isolated Python runtime and Playwright Chromium.
This is required once after a marketplace plugin install. Manual installers run
the same setup automatically. It never installs packages globally.

### `/seo-ops-analisis doctor`

Check runtime, dependency, and Chromium readiness without changing the system.
Diagnostic output omits absolute paths and environment values.

### `/seo-ops-analisis audit <url>`

Full website SEO audit with parallel analysis.

**Example:**
```
/seo-ops-analisis audit https://example.com
```

**What it does:**
1. Crawls up to 500 pages
2. Detects business type
3. Delegates to up to 17 specialist subagents in parallel (9 always-on + 8 conditional)
4. Generates SEO Health Score (0-100)
5. Creates prioritized action plan

**Output:**
- `FULL-AUDIT-REPORT.md`
- `ACTION-PLAN.md`
- `screenshots/` (if Playwright available)

---

### `/seo-ops-analisis page <url>`

Deep single-page analysis.

**Example:**
```
/seo-ops-analisis page https://example.com/about
```

**What it analyzes:**
- On-page SEO (title, meta, headings, URLs)
- Content quality (word count, readability, E-E-A-T)
- Technical elements (canonical, robots, Open Graph)
- Schema markup
- Images (alt text, sizes, formats)
- Core Web Vitals potential issues

---

### `/seo-ops-analisis technical <url>`

Technical SEO audit across 9 categories.

**Example:**
```
/seo-ops-analisis technical https://example.com
```

**Categories:**
1. Crawlability
2. Indexability
3. Security
4. URL Structure
5. Mobile Optimization
6. Core Web Vitals (LCP, INP, CLS)
7. Structured Data
8. JavaScript Rendering
9. IndexNow Protocol

---

### `/seo-ops-analisis content <url>`

E-E-A-T and content quality analysis.

**Example:**
```
/seo-ops-analisis content https://example.com/blog/post
```

**What it evaluates:**
- Experience signals (first-hand knowledge)
- Expertise (author credentials)
- Authoritativeness (external recognition)
- Trustworthiness (transparency, security)
- AI citation readiness
- Content freshness

---

### `/seo-ops-analisis content-brief <topic or url>`

Generate a detailed SEO content brief: target keywords, search intent, heading outline, internal link targets, and competitor angle.

**Example:**
```
/seo-ops-analisis content-brief "best running shoes for flat feet"
```

**What it produces:**
- Primary and secondary target keywords
- Search intent and audience
- Section-by-section heading outline
- Internal link recommendations
- Competitor content angles to beat

---

### `/seo-ops-analisis schema <url>`

Schema markup detection, validation, and generation.

**Example:**
```
/seo-ops-analisis schema https://example.com
```

**What it does:**
- Detects existing schema (JSON-LD, Microdata, RDFa)
- Validates against Google's requirements
- Identifies missing opportunities
- Generates ready-to-use JSON-LD

---

### `/seo-ops-analisis geo <url>`

AI Overviews / Generative Engine Optimization.

**Example:**
```
/seo-ops-analisis geo https://example.com/blog/guide
```

**What it analyzes:**
- Citability score (quotable facts, statistics)
- Structural readability (headings, lists, tables)
- Entity clarity (definitions, context)
- Authority signals (credentials, sources)
- Structured data support

---

### `/seo-ops-analisis agentic [audit|fix|lighthouse|refresh] <url>`

Agent readiness: how well AI agents that browse and act for people can read and use the site.

**Examples:**
```
/seo-ops-analisis agentic https://example.com
/seo-ops-analisis agentic lighthouse https://example.com
/seo-ops-analisis agentic fix https://example.com
```

**What it analyzes:**
- Lighthouse Agentic Browsing result as Lighthouse computes it (X of N, N/A and informative audits excluded)
- Accessibility tree for agents (the 33 axe rules Lighthouse uses, plus the local Agent-UX heuristic)
- robots.txt groups per AI purpose (training, search, user-triggered) and Content-Signal
- llms.txt, Markdown delivery (`Accept: text/markdown`, `.md` alternates), ai-catalog.json, `/.well-known` files
- WebMCP tools and form annotations, labelled as a W3C Community Group draft

`fix` drafts robots.txt Content-Signal lines, llms.txt, ai-catalog.json and WebMCP scaffolds for review; nothing is deployed.

---

### `/seo-ops-analisis images <url>`

Image optimization analysis. Subcommands: `serp <keyword>` (image SERP / visual-search analysis), `optimize <path>` (local file optimization + IPTC AI labeling).

**Examples:**
```
/seo-ops-analisis images https://example.com
/seo-ops-analisis images serp "running shoes"
/seo-ops-analisis images optimize ./hero.webp
```

**What it checks:**
- Alt text presence and quality
- File sizes (flag >200KB)
- Formats (WebP/AVIF recommendations)
- Responsive images (srcset, sizes)
- Lazy loading
- CLS prevention (dimensions)

---

### `/seo-ops-analisis sitemap <url>`

Analyze existing XML sitemap.

**Example:**
```
/seo-ops-analisis sitemap https://example.com/sitemap.xml
```

**What it validates:**
- XML format
- URL count (<50k per file)
- URL status codes
- lastmod accuracy
- Deprecated tags (priority, changefreq)
- Coverage vs crawled pages

---

### `/seo-ops-analisis sitemap generate`

Generate new sitemap with industry templates.

**Example:**
```
/seo-ops-analisis sitemap generate
```

**Process:**
1. Select or auto-detect business type
2. Interactive structure planning
3. Apply quality gates (30/50 location page limits)
4. Generate valid XML
5. Create documentation

---

### `/seo-ops-analisis plan <type>`

Strategic SEO planning.

**Types:** `saas`, `local`, `ecommerce`, `publisher`, `agency`

**Example:**
```
/seo-ops-analisis plan saas
```

**What it creates:**
- Complete SEO strategy
- Competitive analysis
- Content calendar
- Implementation roadmap (4 phases)
- Site architecture design

---

### `/seo-ops-analisis competitor-pages [url|generate]`

Competitor comparison page generation.

**Examples:**
```
/seo-ops-analisis competitor-pages https://example.com/vs/competitor
/seo-ops-analisis competitor-pages generate
```

**Capabilities:**
- Generate "X vs Y" comparison page layouts
- Create "Alternatives to X" page structures
- Build feature comparison matrices with scoring
- Generate Product + AggregateRating schema markup
- Apply conversion-optimized CTA placement
- Enforce fairness guidelines (accurate data, source citations)

---

### `/seo-ops-analisis hreflang [url]`

Hreflang and international SEO audit and generation. Subcommand: `audit <directory-or-url>` (audit hreflang across a local build directory or a live URL set).

**Examples:**
```
/seo-ops-analisis hreflang https://example.com
/seo-ops-analisis hreflang audit ./dist
```

**Capabilities:**
- Validate self-referencing hreflang tags
- Check return tag reciprocity (A→B requires B→A)
- Verify x-default tag presence
- Validate ISO 639-1 language and ISO 3166-1 region codes
- Check canonical URL alignment with hreflang
- Detect protocol mismatches (HTTP vs HTTPS)
- Generate correct hreflang link tags and sitemap XML

---

### `/seo-ops-analisis programmatic [url|plan]`

Programmatic SEO analysis and planning for pages generated at scale.

**Examples:**
```
/seo-ops-analisis programmatic https://example.com/tools/
/seo-ops-analisis programmatic plan
```

**Capabilities:**
- Assess data source quality (CSV, JSON, API, database)
- Plan template engines with unique content per page
- Design URL pattern strategies (`/tools/[tool-name]`, `/[city]/[service]`)
- Automate internal linking (hub/spoke, related items, breadcrumbs)
- Enforce thin content safeguards (quality gates, word count thresholds)
- Prevent index bloat (noindex low-value, pagination, faceted nav)

---

### `/seo-ops-analisis local <url>`

Local SEO analysis covering Google Business Profile, citations, reviews, and the map pack.

**Example:**
```
/seo-ops-analisis local https://example.com
```

**What it analyzes:**
- Google Business Profile signals (categories, hours, photos, posts)
- NAP (Name, Address, Phone) consistency across the page and external citations
- Review velocity, response rate, and sentiment
- Local schema markup (LocalBusiness, Restaurant, Service-specific types)
- Industry-specific local factors (brick-and-mortar, SAB, hybrid)
- Map pack visibility signals

---

### `/seo-ops-analisis maps [command] [args]`

Maps intelligence: geo-grid rank tracking, GBP profile audits, review intelligence, cross-platform NAP verification, competitor radius mapping.

**Examples:**
```
/seo-ops-analisis maps "Joe's Coffee" "austin tx"
/seo-ops-analisis maps grid "coffee shop" "austin tx"
/seo-ops-analisis maps gbp "Joe's Coffee" "austin tx"
/seo-ops-analisis maps reviews "Joe's Coffee" "austin tx"
/seo-ops-analisis maps competitors "auto repair" "denver"
/seo-ops-analisis maps nap "Joe's Coffee" "austin tx"
/seo-ops-analisis maps schema "Joe's Coffee" "austin tx"
```

**Capabilities:**
- Rank tracking on a geographic grid (typically 49 points)
- GBP profile audit with completeness scoring
- Review aggregation across Google, Yelp, Facebook, Bing
- Competitor discovery within a configurable radius

---

### `/seo-ops-analisis backlinks <url>`

Backlink profile analysis with a 3-tier data cascade: free (Common Crawl + verification), free with signup (Moz, Bing Webmaster Tools), paid (DataForSEO).

**Examples:**
```
/seo-ops-analisis backlinks https://example.com
/seo-ops-analisis backlinks gap https://example.com https://competitor.com
/seo-ops-analisis backlinks toxic https://example.com
/seo-ops-analisis backlinks new https://example.com
/seo-ops-analisis backlinks verify https://example.com --links known-links.txt
/seo-ops-analisis backlinks setup
```

**What it analyzes:**
- Domain Authority and Page Authority (Moz)
- Referring domain count and growth
- Anchor text distribution (branded, exact, partial, naked URL)
- Toxic / spammy backlink detection
- Lost backlinks
- Competitor link gap

---

### `/seo-ops-analisis cluster [command] <seed-keyword>`

SERP-based semantic topic clustering for content architecture planning. Built on the Pro Hub Challenge Semantic Cluster Engine. Subcommands: `plan <seed>` (full planning workflow; also `plan --from strategy` to import a `/seo-ops-analisis plan` output), `execute` (create content via claude-blog or output briefs), `map` (regenerate the interactive visualization). Bare `/seo-ops-analisis cluster <seed>` is shorthand for `plan`.

**Examples:**
```
/seo-ops-analisis cluster plan "claude code skills"
/seo-ops-analisis cluster plan --from strategy
/seo-ops-analisis cluster execute
/seo-ops-analisis cluster map
```

**What it produces:**
- Keyword expansion from the seed (50-200 candidates)
- Pairwise SERP overlap comparison to detect semantic clusters
- Intent classification per cluster (informational, commercial, transactional, navigational)
- Hub-and-spoke content architecture proposal
- Internal link matrix between cluster pages
- Interactive `cluster-map.html` visualization

---

### `/seo-ops-analisis sxo <url>`

Search Experience Optimization: SERP backwards analysis, page-type mismatch detection, persona scoring. Subcommands: `<url> <keyword>` (analyze for a specific keyword), `wireframe <url>` (IST/SOLL wireframe), `personas <url>` (persona-only scoring, skips SERP).

**Examples:**
```
/seo-ops-analisis sxo https://example.com/blog/how-to-x
/seo-ops-analisis sxo https://example.com/page "target keyword"
/seo-ops-analisis sxo wireframe https://example.com/page
/seo-ops-analisis sxo personas https://example.com/page
```

**What it produces:**
- Page-type taxonomy classification (article, landing, product, tool, listing)
- SERP intent vs page-type alignment check
- User stories derived from SERP signals
- Multi-persona scoring (researcher, buyer, expert, casual visitor)
- Wireframe-level recommendations for fixing mismatches

---

### `/seo-ops-analisis drift baseline|compare|history <url>`

SEO drift monitoring. Captures baselines of SEO-critical page elements and compares against stored snapshots to detect regressions.

**Examples:**
```
/seo-ops-analisis drift baseline https://example.com
/seo-ops-analisis drift compare https://example.com
/seo-ops-analisis drift history https://example.com
```

**What it tracks:** title, meta description, canonical, hreflang, Open Graph, schema, headings, internal links, robots, sitemap entry, indexability, Core Web Vitals, response status, redirect chain.

**17 comparison rules** classify changes by severity (CRITICAL, HIGH, MEDIUM). SQLite-backed baselines.

---

### `/seo-ops-analisis ecommerce <url>`

E-commerce SEO covering product schema, marketplace intelligence, and pricing gap analysis. Subcommands: `products <keyword>` (Google Shopping competitive analysis), `gaps <domain>` (organic-vs-Shopping visibility gap), `schema <url>` (product schema validation + enhancement).

**Examples:**
```
/seo-ops-analisis ecommerce https://shop.example.com/product/x
/seo-ops-analisis ecommerce products "running shoes"
/seo-ops-analisis ecommerce gaps shop.example.com
/seo-ops-analisis ecommerce schema https://shop.example.com/product/x
```

**What it analyzes:**
- Product schema (Product, Offer, AggregateRating, Review)
- Google Shopping visibility
- Amazon marketplace presence
- Pricing gap vs competitors
- Out-of-stock and availability signals
- Faceted navigation crawl traps

---

### `/seo-ops-analisis flow [stage] [url|topic]`

FLOW framework integration: evidence-led prompts for the Find, Leverage, Optimize, Win, and Local stages of a content campaign.

**Examples:**
```
/seo-ops-analisis flow find "topic"
/seo-ops-analisis flow leverage https://example.com
/seo-ops-analisis flow optimize https://example.com/page
/seo-ops-analisis flow win https://example.com/page
/seo-ops-analisis flow local https://example.com
/seo-ops-analisis flow prompts
/seo-ops-analisis flow sync
```

**41 prompts** sourced from FLOW (CC BY 4.0). Each prompt is grounded in a specific evidence source (SERP data, GSC, GA4, customer interviews) with attribution preserved.

---

### `/seo-ops-analisis google [command] [url]`

Google SEO APIs. 4-tier credential system covering PageSpeed Insights, CrUX, CrUX History, Search Console, URL Inspection, Indexing API, GA4, and Keyword Planner.

**Setup & reporting:**
```
/seo-ops-analisis google setup                      # Configure/check credentials
/seo-ops-analisis google quotas                     # Show per-API quota usage
/seo-ops-analisis google report full                # Generate full PDF/HTML report
/seo-ops-analisis google report cwv-audit           # CWV-focused report
/seo-ops-analisis google report gsc-performance     # Search performance report
/seo-ops-analisis google report indexation          # Indexation status report
```

**PageSpeed / CrUX (Tier 0):**
```
/seo-ops-analisis google pagespeed <url>            # PageSpeed Insights (lab) + CWV
/seo-ops-analisis google crux <url>                 # CrUX field data
/seo-ops-analisis google crux-history <url>         # 25-week CrUX history
```

**Search Console / Indexing (Tier 1):**
```
/seo-ops-analisis google gsc <property>             # Search Analytics (clicks/impressions/CTR/position)
/seo-ops-analisis google inspect <url>              # URL Inspection (indexation status)
/seo-ops-analisis google inspect-batch <file>       # Batch URL inspection
/seo-ops-analisis google sitemaps <property>        # List submitted sitemaps + status
/seo-ops-analisis google index <url>                # Indexing API notify
/seo-ops-analisis google index-batch <file>         # Batch indexing notify
```
Use Indexing API commands only for pages with JobPosting or BroadcastEvent embedded in VideoObject. Route ordinary URLs to URL Inspection or sitemaps; `URL_UPDATED` does not guarantee indexing.

**GA4 (Tier 2):**
```
/seo-ops-analisis google ga4 [property-id]          # Organic traffic report
/seo-ops-analisis google ga4-pages [property-id]    # Top organic landing pages
```

**NLP / Keywords / YouTube:**
```
/seo-ops-analisis google nlp <url-or-text>          # NLP content analysis
/seo-ops-analisis google entities <url-or-text>     # Entity extraction
/seo-ops-analisis google entity <query>             # Entity lookup
/seo-ops-analisis google keywords <seed>            # Keyword Planner ideas (Tier 3)
/seo-ops-analisis google volume <keywords>          # Keyword search volume (Tier 3)
/seo-ops-analisis google youtube <query>            # YouTube search
/seo-ops-analisis google youtube-video <video_id>   # YouTube video analysis
/seo-ops-analisis google safety <url>               # Safe Browsing check
```

**Tiers:**
- Tier 0 (API key only): PSI, CrUX, CrUX History
- Tier 1 (+ OAuth or Service Account): GSC, URL Inspection, Indexing API
- Tier 2 (+ GA4 property config): GA4 organic traffic
- Tier 3 (+ Google Ads developer token): Keyword Planner

PDF and HTML reports generated via WeasyPrint and matplotlib.

---

### `/seo-ops-analisis image-gen [use-case] <description>`

AI image generation for SEO assets (extension). Powered by Gemini via nanobanana-mcp.

**Prerequisites:** Banana extension installed (`./extensions/banana/install.sh`)

**Use Cases:**
```
/seo-ops-analisis image-gen og <description>          # OG/social preview image (16:9, 1K)
/seo-ops-analisis image-gen hero <description>        # Blog hero image (16:9, 2K)
/seo-ops-analisis image-gen product <description>     # Product photography (4:3, 2K)
/seo-ops-analisis image-gen infographic <description> # Infographic visual (2:3, 4K)
/seo-ops-analisis image-gen custom <description>      # Custom with full Creative Director pipeline
/seo-ops-analisis image-gen batch <description> [N]   # Generate N variations (default: 3)
```

**What it does:**
1. Maps SEO use case to optimized domain mode, aspect ratio, and resolution
2. Constructs 6-component Reasoning Brief (Creative Director pipeline)
3. Generates image via Gemini API
4. Provides SEO checklist (alt text, file naming, WebP, schema markup)

---

### `/seo-ops-analisis firecrawl [command] <url>`

Full-site crawling and URL discovery via Firecrawl MCP (extension).

**Prerequisites:** Firecrawl extension installed (`./extensions/firecrawl/install.sh`)

**Examples:**
```
/seo-ops-analisis firecrawl crawl https://example.com
/seo-ops-analisis firecrawl map https://example.com
/seo-ops-analisis firecrawl scrape https://example.com/page
/seo-ops-analisis firecrawl search "query" https://example.com
```

**What it does:**
- `crawl` walks the site discovering URLs and capturing content
- `map` returns the full URL inventory for a domain
- `scrape` extracts a single page in a model-friendly format
- `search` searches within a crawled site for a query

---

### `/seo-ops-analisis dataforseo [command]`

Live SEO data via DataForSEO MCP server (extension). 23 data commands across 9 API modules, plus cost-tracking commands.

**Prerequisites:** DataForSEO extension installed (`./extensions/dataforseo/install.sh`)

**SERP Analysis:**
```
/seo-ops-analisis dataforseo serp <keyword>              # Google organic results (also Bing/Yahoo)
/seo-ops-analisis dataforseo serp-images <keyword>       # Image elements in the organic SERP (no Images tool on the pinned server)
/seo-ops-analisis dataforseo serp-youtube <keyword>      # YouTube search results
/seo-ops-analisis dataforseo youtube <video_id>          # YouTube video deep analysis
```

**Keyword Research:**
```
/seo-ops-analisis dataforseo keywords <seed>             # Keyword ideas and suggestions
/seo-ops-analisis dataforseo volume <keywords>           # Search volume metrics
/seo-ops-analisis dataforseo difficulty <keywords>       # Keyword difficulty scores
/seo-ops-analisis dataforseo intent <keywords>           # Search intent classification
/seo-ops-analisis dataforseo trends <keyword>            # Google Trends data
```

**Domain & Competitors:**
```
/seo-ops-analisis dataforseo backlinks <domain>          # Full backlink profile
/seo-ops-analisis dataforseo competitors <domain>        # Competitor analysis
/seo-ops-analisis dataforseo ranked <domain>             # Ranked keywords
/seo-ops-analisis dataforseo intersection <domains>      # Keyword/backlink overlap
/seo-ops-analisis dataforseo traffic <domains>           # Traffic estimation
/seo-ops-analisis dataforseo subdomains <domain>         # Subdomains with ranking data
/seo-ops-analisis dataforseo top-searches <domain>       # Top queries mentioning domain
```

**Technical / On-Page:**
```
/seo-ops-analisis dataforseo onpage <url>                # On-page analysis (Lighthouse)
/seo-ops-analisis dataforseo tech <domain>               # Technology detection
/seo-ops-analisis dataforseo whois <domain>              # WHOIS data
```

**Content & Business Data:**
```
/seo-ops-analisis dataforseo content <keyword/url>       # Content analysis and trends
/seo-ops-analisis dataforseo listings <keyword>          # Business listings search
```

**AI Visibility / GEO:**
```
/seo-ops-analisis dataforseo ai-scrape <query>           # ChatGPT web scraper for GEO
/seo-ops-analisis dataforseo ai-mentions <keyword>       # LLM mention tracking
```

**Cost Tracking:**
```
/seo-ops-analisis dataforseo costs today                            # Today's DataForSEO spend
/seo-ops-analisis dataforseo costs summary                          # Spend summary across periods
/seo-ops-analisis dataforseo costs config --mode threshold --threshold 0.50   # Set cost-control mode/threshold
```

---

### `/seo-ops-analisis ahrefs [command] <url|topic>`

Ahrefs API metrics (extension). **Prerequisites:** Ahrefs extension installed (`./extensions/ahrefs/install.sh`).
```
/seo-ops-analisis ahrefs metrics <url>       # DR/UR, referring-domain count, organic traffic estimate
/seo-ops-analisis ahrefs backlinks <url>     # Top referring domains, anchor distribution, follow/nofollow ratio
/seo-ops-analisis ahrefs organic <url>       # Organic keywords, ranking distribution, traffic by country
/seo-ops-analisis ahrefs content <topic>     # Content Explorer top results, social shares, referring domains
```

---

### `/seo-ops-analisis bing [command]`

Bing Webmaster Tools + IndexNow (extension). **Prerequisites:** Bing extension installed (`./extensions/bing-webmaster/install.sh`).
```
/seo-ops-analisis bing links <url>                 # Inbound links from Bing Webmaster
/seo-ops-analisis bing compare <urlA> <urlB>       # Compare two URLs' Bing link profiles
/seo-ops-analisis bing submit <url> --host <host>                # IndexNow single-URL submit (requires key)
/seo-ops-analisis bing submit-batch <file> --host <host>         # IndexNow batch submit (requires key)
/seo-ops-analisis bing verify-indexnow --host <host>             # Verify the IndexNow key is published
```

---

### `/seo-ops-analisis matomo [command] [site-id]`

Matomo Reporting API (extension). **Prerequisites:** Matomo extension installed (`./extensions/matomo/install.sh`), which writes the instance URL, API token, and optional default site ID to `~/.config/seo-ops-studio/matomo.json` (0600). `MATOMO_URL`, `MATOMO_API_TOKEN`, and `MATOMO_SITE_ID` in the environment override the file. Works against self-hosted Matomo or Matomo Cloud; an instance on a private address must be named in `SEO_OPS_LOCAL_TARGETS`.

Use as a GA4 alternative or supplement when you want full data ownership, no Google dependency, or privacy-first analytics.
```
/seo-ops-analisis matomo check                  # Probe credentials and confirm Matomo version
/seo-ops-analisis matomo organic [site-id]      # Organic traffic trend (28d) + top landing pages
/seo-ops-analisis matomo top-pages              # Top organic landing pages only
/seo-ops-analisis matomo device                 # Visits by device type
/seo-ops-analisis matomo country                # Visits by country
/seo-ops-analisis matomo referrers              # Channel + search-engine breakdown
/seo-ops-analisis matomo keywords               # Organic search keywords (often "(not provided)")
```

All commands accept `--days` (default 28), `--limit` (default 50),
`--site-id`, and `--json`. The audit orchestrator spawns the
`seo-ops-matomo` agent automatically when credentials are present.

---

### `/seo-ops-analisis profound [command] <brand>`

LLM brand-citation tracking via Profound (extension). **Prerequisites:** Profound extension installed.
```
/seo-ops-analisis profound citations <brand>     # Citation rate per LLM + 30-day trend
/seo-ops-analisis profound prompts <brand>       # Top prompts that surface (or miss) the brand
/seo-ops-analisis profound competitors <brand>   # Brands cited alongside yours for the same prompts
/seo-ops-analisis profound alerts <brand>        # Spike/drop alerts vs 7-day baseline
```

---

### `/seo-ops-analisis seranking [command] <brand|keyword|url>`

AI-visibility + SERP via SE Ranking (extension). **Prerequisites:** SE Ranking extension installed.
```
/seo-ops-analisis seranking ai-visibility <brand>   # Share-of-voice across ChatGPT/Gemini/Perplexity/AI Overviews/AI Mode
/seo-ops-analisis seranking serp <keyword>          # Top 100 organic positions + SERP features
/seo-ops-analisis seranking backlinks <url>         # Backlink profile (free-tier alternative to Ahrefs/DataForSEO)
/seo-ops-analisis seranking competitors <url>       # Top 10 organic competitors + shared-keyword gaps
```

---

### `/seo-ops-analisis unlighthouse <url>`

Multi-page Lighthouse audit via Unlighthouse (extension, MIT, no API quota). **Prerequisites:** Node 18+ and the unlighthouse npm package (`./extensions/unlighthouse/install.sh`).
```
/seo-ops-analisis unlighthouse https://example.com
/seo-ops-analisis unlighthouse https://example.com --device desktop
/seo-ops-analisis unlighthouse https://example.com --max-routes 50 --output-dir ./reports
```

---

## Quick Reference

| Command | Use Case |
|---------|----------|
| `/seo-ops-analisis audit <url>` | Full website audit with parallel subagents |
| `/seo-ops-analisis page <url>` | Single page analysis |
| `/seo-ops-analisis technical <url>` | Technical SEO across 9 categories |
| `/seo-ops-analisis content <url>` | E-E-A-T and content quality |
| `/seo-ops-analisis content-brief <topic>` | Detailed content brief: keywords, outline, internal links |
| `/seo-ops-analisis schema <url>` | Schema markup detection, validation, generation |
| `/seo-ops-analisis sitemap <url>` | Sitemap validation |
| `/seo-ops-analisis sitemap generate` | Create new sitemap with industry templates |
| `/seo-ops-analisis images <url>` | Image optimization |
| `/seo-ops-analisis geo <url>` | AI search optimization (GEO) |
| `/seo-ops-analisis agentic <url>` | Agent readiness (Lighthouse Agentic Browsing, AI agent access, WebMCP) |
| `/seo-ops-analisis local <url>` | Local SEO (GBP, citations, reviews) |
| `/seo-ops-analisis maps [command]` | Maps intelligence (geo-grid, GBP audit, competitors) |
| `/seo-ops-analisis backlinks <url>` | Backlink profile analysis |
| `/seo-ops-analisis cluster <seed>` | SERP-based semantic clustering |
| `/seo-ops-analisis sxo <url>` | Search Experience Optimization |
| `/seo-ops-analisis drift baseline\|compare\|history <url>` | SEO drift monitoring |
| `/seo-ops-analisis ecommerce <url>` | E-commerce SEO |
| `/seo-ops-analisis hreflang [url]` | Hreflang and international SEO |
| `/seo-ops-analisis plan <type>` | Strategic planning by industry |
| `/seo-ops-analisis programmatic [url\|plan]` | Programmatic SEO analysis |
| `/seo-ops-analisis competitor-pages [url\|generate]` | Competitor comparison pages |
| `/seo-ops-analisis flow [stage] [url\|topic]` | FLOW framework prompts |
| `/seo-ops-analisis google [command] [url]` | Google SEO APIs (GSC, PSI, CrUX, GA4) |
| `/seo-ops-analisis dataforseo [command]` | Live SEO data (extension) |
| `/seo-ops-analisis image-gen [use-case] <desc>` | AI image generation (extension) |
| `/seo-ops-analisis firecrawl [command] <url>` | Full-site crawling (extension) |
| `/seo-ops-analisis ahrefs [command] <url>` | Backlinks, organic keywords, and content data via the official Ahrefs MCP (extension) |
| `/seo-ops-analisis seranking [command]` | AI Share-of-Voice across ChatGPT, Gemini, Perplexity, AI Overviews, AI Mode (extension) |
| `/seo-ops-analisis profound [command]` | LLM citation tracking with time-series data (extension) |
| `/seo-ops-analisis bing [command] <url>` | Bing Webmaster Tools + IndexNow URL submission (extension) |
| `/seo-ops-analisis matomo [command] [args]` | Matomo Reporting API: GA4 alternative or complement (extension) |
| `/seo-ops-analisis unlighthouse <url>` | Multi-page Lighthouse runner, runs locally (extension) |
