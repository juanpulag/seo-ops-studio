#!/usr/bin/env python3
"""SEO Ops Studio · onboarding de credenciales.

Crea las plantillas de credenciales en ~/.config/seo-ops-studio/ (sin sobrescribir
nada) y muestra qué APIs están conectadas, para qué sirve cada una y cómo conectarla.
Nunca imprime claves ni secretos: solo si existen y, para la cuenta de servicio,
su correo (que es lo que el usuario debe compartir en Search Console y GA4).

Uso:
  seo-ops run ops_setup.py --init            # crea plantillas que falten
  seo-ops run ops_setup.py --status [--json] # estado de cada API
  seo-ops run ops_setup.py --open            # abre la carpeta de credenciales
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
TEMPLATES = PLUGIN_ROOT / "templates" / "credenciales"
CONFIG_DIR = Path(os.path.expanduser("~/.config/seo-ops-studio"))
CLAUDE_JSON = Path(os.path.expanduser("~/.claude.json"))

APIS = [
    {
        "id": "google_sa",
        "nombre": "Google · cuenta de servicio (Search Console, GA4, URL Inspection, GTM)",
        "por_que": "Datos reales del cliente: clics, impresiones, posiciones, indexación, tráfico orgánico y conversiones. Sin esto las prioridades se basan en buenas prácticas, no en impacto medido.",
        "coste": "Gratis",
        "como": "docs/es/02-cuenta-de-servicio.md → guarda la ruta del JSON en google-api.json (service_account_path).",
    },
    {
        "id": "google_key",
        "nombre": "Google · clave de API (PageSpeed Insights y CrUX)",
        "por_que": "Core Web Vitals reales (LCP, INP, CLS) y Lighthouse sin el límite público que devuelve error 429. Sin clave, el rendimiento queda como estimación.",
        "coste": "Gratis",
        "como": "Google Cloud → APIs y servicios → Credenciales → Crear clave de API → google-api.json (api_key).",
    },
    {
        "id": "dataforseo",
        "nombre": "DataForSEO (MCP)",
        "por_que": "Posiciones reales por país e idioma, volúmenes, competencia, backlinks, Lighthouse a escala y menciones en LLMs.",
        "coste": "Pago por uso",
        "como": "Ejecuta tú en la terminal: bash extensions/dataforseo/install.sh (te pide usuario y contraseña de API; no los pegues en el chat).",
    },
    {
        "id": "bing",
        "nombre": "Bing Webmaster Tools",
        "por_que": "Indexación y backlinks en Bing, que alimenta a Copilot.",
        "coste": "Gratis",
        "como": "bing.com/webmasters → Configuración → Acceso a API → backlinks-api.json (bing_api_key).",
    },
    {
        "id": "moz",
        "nombre": "Moz API (nivel gratuito)",
        "por_que": "Autoridad de dominio y enlaces como respaldo cuando no hay DataForSEO.",
        "coste": "Gratis (cupo mensual)",
        "como": "moz.com/products/api → backlinks-api.json (moz_api_key).",
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
        return {"_error": f"{name} no es JSON válido"}


def _service_account_email(path_value: str | None) -> tuple[bool, str | None, str | None]:
    if not path_value:
        return False, None, "service_account_path vacío"
    sa_path = Path(os.path.expanduser(path_value))
    if not sa_path.is_file():
        return False, None, f"no existe el archivo indicado en service_account_path"
    try:
        data = json.loads(sa_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False, None, "el archivo de la cuenta de servicio no es JSON válido"
    if data.get("type") != "service_account" or not data.get("client_email"):
        return False, None, "el JSON no es una clave de cuenta de servicio"
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
        "google_sa": {"ok": sa_ok, "detalle": sa_email and f"correo a compartir: {sa_email}" or sa_problem},
        "google_key": {"ok": bool(google.get("api_key")), "detalle": None if google.get("api_key") else "api_key vacío"},
        "dataforseo": {"ok": _dataforseo_configured(), "detalle": None},
        "bing": {"ok": bool(backlinks.get("bing_api_key")), "detalle": None},
        "moz": {"ok": bool(backlinks.get("moz_api_key")), "detalle": None},
    }
    out = {
        "config_dir": str(CONFIG_DIR),
        "plantillas_presentes": sorted(p.name for p in CONFIG_DIR.glob("*.json")) if CONFIG_DIR.is_dir() else [],
        "apis": [],
    }
    for api in APIS:
        res = results[api["id"]]
        out["apis"].append({**api, "conectada": res["ok"], "detalle": res["detalle"]})
    if sa_ok or google.get("api_key"):
        out["verificacion_google"] = _google_live_check()
    return out


def _print_human(report: dict) -> None:
    print(f"Carpeta de credenciales: {report['config_dir']}\n")
    for api in report["apis"]:
        mark = "✅" if api["conectada"] else "⬜"
        print(f"{mark} {api['nombre']}  [{api['coste']}]")
        print(f"   Para qué: {api['por_que']}")
        if api["detalle"]:
            print(f"   Estado: {api['detalle']}")
        if not api["conectada"]:
            print(f"   Cómo conectarla: {api['como']}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--init", action="store_true", help="crea las plantillas que falten")
    parser.add_argument("--status", action="store_true", help="muestra el estado de cada API")
    parser.add_argument("--open", action="store_true", help="abre la carpeta de credenciales")
    parser.add_argument("--json", action="store_true", help="salida JSON")
    args = parser.parse_args()
    if not (args.init or args.status or args.open):
        args.init = args.status = True

    if args.init:
        created = init()
        if not args.json:
            print("Plantillas creadas: " + (", ".join(created) if created else "ninguna (ya existían)") + "\n")
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
