# Changelog

All notable changes to SEO Ops Studio are recorded here. Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [SemVer](https://semver.org/).

## [0.2.0] - 2026-11-11

### Changed
- Everything is now in English: commands, guides, templates, script flags and output, and the Notion schema. Claude still works in whatever language the user asks for.
- Renamed commands: `/seo-ops-configurar` is now `/seo-ops-setup` and the engine's `/seo-ops-analisis` is now `/seo-ops-analyze`.
- Audits are saved in `audits/<domain>/`. `ops_pdf.py` flags are now `--sources` and `--note`.

## [0.1.0] - 2026-11-10

First release (basic edition).

### Added
- `/seo-ops`: menu, first-use detection and full site audit with report and PDF (`/seo-ops audit <url>`).
- `/seo-ops-setup`: API onboarding (Google, DataForSEO, Bing, Moz) with credential templates that are never overwritten and verification that never prints secrets.
- `scripts/ops_setup.py` (templates and API status) and `scripts/ops_pdf.py` (PDF with the real data sources, no WeasyPrint dependency).
- Guides: `docs/guides/01-apis.md` and `docs/guides/02-service-account.md`.

### Changed from claude-seo v2.5.0
- Every command uses the `/seo-ops` prefix: the `/seo` orchestrator was renamed and each skill and agent `seo-X` became `seo-ops-X`, so it can live alongside the original plugin.
- Launcher `scripts/seo-ops`, `SEO_OPS_*` variables and configuration in `~/.config/seo-ops-studio/`.

The audit engine's earlier history is in the [claude-seo CHANGELOG](https://github.com/AgriciDaniel/claude-seo/blob/main/CHANGELOG.md).
