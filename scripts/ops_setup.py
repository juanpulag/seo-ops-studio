#!/usr/bin/env python3
"""SEO Ops Studio · credential onboarding.

Creates the credential templates in ~/.config/seo-ops-studio/ (never overwriting
anything) and shows which APIs are connected, what each is for and how to connect it.
Never prints keys or secrets: only whether they exist and, for the service account,
its email (which the user must share in Search Console and GA4).

Usage:
  seo-ops run ops_setup.py --init            # create missing templates
  seo-ops run ops_setup.py --status [--json] # status of each API
  seo-ops run ops_setup.py --open            # open the credentials folder
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = PLUGIN_ROOT / "templates" / "credentials"
CONFIG_DIR = Path(os.path.expanduser("~/.config/seo-ops-studio"))
CLAUDE_JSON = Path(os.path.expanduser("~/.claude.json"))

APIS = [
    {
        "id": "google_sa",
        "name": "Google · service account (Search Console, GA4, URL Inspection, GTM)",
        "why": "Real client data: clicks, impressions, positions, indexing, organic traffic and conversions. Without it, priorities are based on best practices rather than measured impact.",
        "cost": "Free",
        "how": "docs/guides/02-service-account.md → save the JSON path in google-api.json (service_account_path).",
    },
    {
        "id": "google_key",
        "name": "Google · API key (PageSpeed Insights and CrUX)",
        "why": "Real Core Web Vitals (LCP, INP, CLS) and Lighthouse without the public limit that returns 429 errors. Without a key, performance is an estimate.",
        "cost": "Free",
        "how": "Google Cloud → APIs & Services → Credentials → Create API key → google-api.json (api_key).",
    },
    {
        "id": "dataforseo",
        "name": "DataForSEO (MCP)",
        "why": "Real rankings by country and language, volumes, competitors, backlinks, Lighthouse at scale and LLM mentions.",
        "cost": "Pay as you go",
        "how": "Run it yourself in the terminal: bash extensions/dataforseo/install.sh (it asks for the API username and password; do not paste them in the chat).",
    },
    {
        "id": "bing",
        "name": "Bing Webmaster Tools",
        "why": "Indexing and backlinks in Bing, which feeds Copilot.",
        "cost": "Free",
        "how": "bing.com/webmasters → Settings → API access → backlinks-api.json (bing_api_key).",
    },
    {
        "id": "moz",
        "name": "Moz API (free tier)",
        "why": "Domain authority and links as a fallback when DataForSEO is not available.",
        "cost": "Free (monthly quota)",
        "how": "moz.com/products/api → backlinks-api.json (moz_api_key).",
    },
]


def _secure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    try:
        path.chmod(0o700)
    except OSError:
        pass


def init() -> list[str]:
    """Copy missing credential templates. Never overwrites existing files."""
    _secure_dir(CONFIG_DIR)
    created = []
    for template in sorted(TEMPLATES.glob("*.json")):
        target = CONFIG_DIR / template.name
        if target.exists():
            continue
        shutil.copyfile(template, target)
        try:
            target.chmod(stat.S_IRUSR | stat.S_IWUSR)
        except OSError:
            pass
        created.append(str(target))
    return created


def _load(name: str) -> dict:
    path = CONFIG_DIR / name
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"_error": f"{name} is not valid JSON"}


def _service_account_email(path_value: str | None) -> tuple[bool, str | None, str | None]:
    if not path_value:
        return False, None, "service_account_path is empty"
    sa_path = Path(os.path.expanduser(path_value))
    if not sa_path.is_file():
        return False, None, "the file set in service_account_path does not exist"
    try:
        data = json.loads(sa_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False, None, "the service account file is not valid JSON"
    if data.get("type") != "service_account" or not data.get("client_email"):
        return False, None, "the JSON is not a service account key"
    return True, data["client_email"], None


def _dataforseo_configured() -> bool:
    if not CLAUDE_JSON.is_file():
        return False
    try:
        data = json.loads(CLAUDE_JSON.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    servers = dict(data.get("mcpServers") or {})
    for project in (data.get("projects") or {}).values():
        servers.update(project.get("mcpServers") or {})
    return any("dataforseo" in name.lower() for name in servers)


def _google_live_check() -> dict | None:
    """Run the bundled google_auth check (no secrets in its output)."""
    script = PLUGIN_ROOT / "scripts" / "google_auth.py"
    try:
        proc = subprocess.run(
            [sys.executable, str(script), "--check", "--json"],
            capture_output=True, text=True, timeout=60,
        )
        return json.loads(proc.stdout) if proc.stdout.strip().startswith("{") else None
    except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError):
        return None


def status() -> dict:
    google = _load("google-api.json")
    backlinks = _load("backlinks-api.json")
    sa_ok, sa_email, sa_problem = _service_account_email(google.get("service_account_path"))
    results = {
        "google_sa": {"ok": sa_ok, "detail": sa_email and f"email to share: {sa_email}" or sa_problem},
        "google_key": {"ok": bool(google.get("api_key")), "detail": None if google.get("api_key") else "api_key is empty"},
        "dataforseo": {"ok": _dataforseo_configured(), "detail": None},
        "bing": {"ok": bool(backlinks.get("bing_api_key")), "detail": None},
        "moz": {"ok": bool(backlinks.get("moz_api_key")), "detail": None},
    }
    out = {
        "config_dir": str(CONFIG_DIR),
        "templates_present": sorted(p.name for p in CONFIG_DIR.glob("*.json")) if CONFIG_DIR.is_dir() else [],
        "apis": [],
    }
    for api in APIS:
        res = results[api["id"]]
        out["apis"].append({**api, "connected": res["ok"], "detail": res["detail"]})
    if sa_ok or google.get("api_key"):
        out["google_check"] = _google_live_check()
    return out


def _print_human(report: dict) -> None:
    print(f"Credentials folder: {report['config_dir']}\n")
    for api in report["apis"]:
        mark = "✅" if api["connected"] else "⬜"
        print(f"{mark} {api['name']}  [{api['cost']}]")
        print(f"   What for: {api['why']}")
        if api["detail"]:
            print(f"   Status: {api['detail']}")
        if not api["connected"]:
            print(f"   How to connect: {api['how']}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--init", action="store_true", help="create missing templates")
    parser.add_argument("--status", action="store_true", help="show the status of each API")
    parser.add_argument("--open", action="store_true", help="open the credentials folder")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()
    if not (args.init or args.status or args.open):
        args.init = args.status = True

    if args.init:
        created = init()
        if not args.json:
            print("Templates created: " + (", ".join(created) if created else "none (already present)") + "\n")
    if args.open:
        _secure_dir(CONFIG_DIR)
        opener = {"darwin": ["open"], "win32": ["explorer"]}.get(sys.platform, ["xdg-open"])
        subprocess.run(opener + [str(CONFIG_DIR)], check=False)
    if args.status:
        report = status()
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            _print_human(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
