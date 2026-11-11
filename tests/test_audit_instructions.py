"""Static instruction guards for full audit persistence and SPA wiring."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_seo_audit_starts_with_render_page_auto() -> None:
    text = (REPO_ROOT / "skills" / "seo-ops-audit" / "SKILL.md").read_text(encoding="utf-8")
    process = text[text.index("## Process"):text.index("## Crawl Configuration")]
    assert '"${CLAUDE_PLUGIN_ROOT}/scripts/seo-ops" run render_page.py' in process
    assert "python3 scripts/render_page.py" not in process
    assert "--mode auto" in process
    assert "scripts/fetch_page.py` to retrieve HTML" not in process


def test_seo_audit_requires_persistent_artifacts() -> None:
    text = (REPO_ROOT / "skills" / "seo-ops-audit" / "SKILL.md").read_text(encoding="utf-8")
    for artifact in (
        "FULL-AUDIT-REPORT.md",
        "ACTION-PLAN.md",
        "audit-data.json",
        "findings/",
        "screenshots/",
    ):
        assert artifact in text
    assert "{domain}-audit" in text


def test_audit_agents_use_renderer_or_capture_script() -> None:
    expectations = {
        "seo-ops-performance.md": "render_page.py",
        "seo-ops-visual.md": "capture_screenshot.py",
        "seo-ops-technical.md": "render_page.py",
        "seo-ops-content.md": "render_page.py",
        "seo-ops-schema.md": "render_page.py",
    }
    for filename, marker in expectations.items():
        text = (REPO_ROOT / "agents" / filename).read_text(encoding="utf-8")
        assert marker in text, f"{filename} must mention {marker}"


def test_audit_agents_document_output_dir_findings_contract() -> None:
    for filename in (
        "seo-ops-performance.md",
        "seo-ops-visual.md",
        "seo-ops-technical.md",
        "seo-ops-content.md",
        "seo-ops-schema.md",
        "seo-ops-sitemap.md",
        "seo-ops-geo.md",
        "seo-ops-local.md",
        "seo-ops-maps.md",
        "seo-ops-google.md",
        "seo-ops-backlinks.md",
        "seo-ops-cluster.md",
        "seo-ops-sxo.md",
        "seo-ops-drift.md",
        "seo-ops-ecommerce.md",
        "seo-ops-agentic.md",
    ):
        text = (REPO_ROOT / "agents" / filename).read_text(encoding="utf-8")
        assert "output_dir" in text
        assert "findings/" in text


def test_seo_audit_report_command_keeps_outputs_in_audit_dir() -> None:
    text = (REPO_ROOT / "skills" / "seo-ops-audit" / "SKILL.md").read_text(encoding="utf-8")
    assert "--output-dir {domain}-audit/" in text
