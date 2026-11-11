"""Tests for the SEO Ops Studio product layer (ops skills, scripts and templates).

These are offline tests: they never touch the network or real credentials.
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
OPS_SKILLS = ["seo-ops", "seo-ops-configurar"]
OPS_SCRIPTS = ["ops_setup.py", "ops_pdf.py"]


def _load(name):
    spec = importlib.util.spec_from_file_location(name.removesuffix(".py"), SCRIPTS / name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _frontmatter(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert match, f"{path} has no frontmatter"
    return match.group(1)


@pytest.mark.parametrize("skill", OPS_SKILLS)
def test_ops_skill_exists_with_frontmatter(skill):
    skill_md = REPO_ROOT / "skills" / skill / "SKILL.md"
    assert skill_md.is_file()
    fm = _frontmatter(skill_md)
    assert re.search(rf"^name: {re.escape(skill)}$", fm, re.M)
    assert "description:" in fm
    assert (REPO_ROOT / "skills" / skill / "LICENSE.txt").is_file()


def test_ops_menu_lists_every_ops_command():
    menu = (REPO_ROOT / "skills" / "seo-ops" / "SKILL.md").read_text(encoding="utf-8")
    for skill in OPS_SKILLS[1:]:
        assert f"/{skill}" in menu, f"/seo-ops menu does not mention /{skill}"


def test_ops_scripts_are_allowlisted():
    sys.path.insert(0, str(SCRIPTS))
    try:
        runtime = _load("runtime.py")
    finally:
        sys.path.pop(0)
    for script in OPS_SCRIPTS:
        assert (SCRIPTS / script).is_file()
        assert script in runtime.ALLOWED_CORE_SCRIPTS


def test_templates_exist():
    for rel in [
        "templates/credenciales/google-api.json",
        "templates/credenciales/backlinks-api.json",
    ]:
        assert (REPO_ROOT / rel).is_file(), rel
    for rel in ["templates/credenciales/google-api.json", "templates/credenciales/backlinks-api.json"]:
        json.loads((REPO_ROOT / rel).read_text(encoding="utf-8"))


def test_credential_templates_hold_no_secrets():
    for name in ["google-api.json", "backlinks-api.json"]:
        data = json.loads((REPO_ROOT / "templates" / "credenciales" / name).read_text(encoding="utf-8"))
        for key, value in data.items():
            if not key.startswith("_"):
                assert value is None, f"{name}:{key} must ship empty"


def test_ops_setup_init_never_overwrites(tmp_path, monkeypatch):
    setup = _load("ops_setup.py")
    monkeypatch.setattr(setup, "CONFIG_DIR", tmp_path / "cfg")
    monkeypatch.setattr(setup, "CLAUDE_JSON", tmp_path / "claude.json")
    created = setup.init()
    assert len(created) == 2
    existing = tmp_path / "cfg" / "google-api.json"
    existing.write_text('{"api_key": "keep-me"}', encoding="utf-8")
    assert setup.init() == []
    assert "keep-me" in existing.read_text(encoding="utf-8")


def test_ops_setup_status_never_prints_secrets(tmp_path, monkeypatch):
    setup = _load("ops_setup.py")
    cfg = tmp_path / "cfg"
    cfg.mkdir()
    sa = tmp_path / "sa.json"
    sa.write_text(json.dumps({"type": "service_account", "client_email": "bot@proj.iam.gserviceaccount.com", "private_key": "-----SECRET-----"}), encoding="utf-8")
    (cfg / "google-api.json").write_text(json.dumps({"service_account_path": str(sa), "api_key": "AIza-SECRET"}), encoding="utf-8")
    (cfg / "backlinks-api.json").write_text(json.dumps({"moz_api_key": "MOZ-SECRET"}), encoding="utf-8")
    monkeypatch.setattr(setup, "CONFIG_DIR", cfg)
    monkeypatch.setattr(setup, "CLAUDE_JSON", tmp_path / "claude.json")
    monkeypatch.setattr(setup, "_google_live_check", lambda: None)
    report = json.dumps(setup.status(), ensure_ascii=False)
    assert "SECRET" not in report
    assert "bot@proj.iam.gserviceaccount.com" in report



def test_ops_pdf_patches_sources_and_escapes():
    pdf = _load("ops_pdf.py")
    html = "<table><tr><td>PageSpeed Insights API</td></tr></table><p>" + pdf.GENERIC_NOTE + "</p>"
    out = pdf.patch_sources(html, [["Raw crawl", "<b>all</b> URLs", "2026-11-05"]], "Estimates & weights")
    assert "PageSpeed Insights API" not in out
    assert "&lt;b&gt;all&lt;/b&gt;" in out
    assert "Estimates &amp; weights" in out



def test_credits_and_license_keep_upstream_attribution():
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    assert "agricidaniel" in license_text.lower()
    credits = (REPO_ROOT / "CREDITS.md").read_text(encoding="utf-8")
    assert "github.com/AgriciDaniel/claude-seo" in credits
    assert "CC BY 4.0" in credits


def test_basic_edition_ships_no_premium_layer():
    for skill in ["seo-ops-cliente", "seo-ops-auditoria", "seo-ops-backlog", "seo-ops-tablero"]:
        assert not (REPO_ROOT / "skills" / skill).exists(), skill
    for script in ["ops_cliente.py", "ops_export.py"]:
        assert not (SCRIPTS / script).exists(), script
