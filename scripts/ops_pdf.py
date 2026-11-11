#!/usr/bin/env python3
"""SEO Ops Studio · convertir el informe HTML en PDF con las fuentes reales.

google_report.py genera el HTML del informe. Este script:
  1. Sustituye la tabla genérica de «Data Sources & Methodology» por las fuentes
     que realmente se usaron en la auditoría (para no afirmar datos que no hubo).
  2. Imprime el HTML a PDF A4 con Chromium (Playwright) y, si no está, con
     Google Chrome instalado. No depende de WeasyPrint.

Uso:
  seo-ops run ops_pdf.py --html informe.html --pdf informe.pdf \
      [--fuentes fuentes.json] [--nota "texto de metodología"]

fuentes.json: [["Fuente", "Qué aportó", "Fecha"], ...]
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

TABLE_RE = re.compile(r"<table[^>]*>(?:(?!</table>).)*PageSpeed Insights API(?:(?!</table>).)*</table>", re.S)
GENERIC_NOTE = "Methodology based on Google Web Vitals thresholds, Search Console documentation, and Lighthouse scoring algorithms."


def patch_sources(text: str, rows: list[list[str]] | None, note: str | None) -> str:
    if rows:
        body = "".join(
            "<tr>" + "".join(f"<td>{html.escape(str(cell))}</td>" for cell in row[:3]) + "</tr>"
            for row in rows
        )
        table = f"<table><thead><tr><th>Source</th><th>What it provided</th><th>Date</th></tr></thead><tbody>{body}</tbody></table>"
        text, n = TABLE_RE.subn(table, text, count=1)
        if not n:
            print("Aviso: no se encontró la tabla de fuentes genérica; el HTML no se modificó en ese punto.", file=sys.stderr)
    if note:
        text = text.replace(GENERIC_NOTE, html.escape(note))
    return text


def to_pdf(html_path: Path, pdf_path: Path) -> str:
    from playwright.sync_api import sync_playwright

    errors = []
    with sync_playwright() as p:
        for label, kwargs in (("chromium", {}), ("chrome", {"channel": "chrome"})):
            try:
                browser = p.chromium.launch(**kwargs)
            except Exception as exc:  # browser binary missing: try the next one
                errors.append(f"{label}: {exc.__class__.__name__}")
                continue
            page = browser.new_page()
            page.goto(html_path.resolve().as_uri(), wait_until="networkidle")
            page.pdf(path=str(pdf_path), format="A4", print_background=True,
                     margin={"top": "12mm", "bottom": "12mm", "left": "10mm", "right": "10mm"})
            browser.close()
            return label
    raise RuntimeError("No hay navegador disponible para imprimir el PDF (" + "; ".join(errors) + "). Ejecuta /seo-ops-configurar para preparar el entorno, o instala Google Chrome.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--html", required=True)
    parser.add_argument("--pdf", required=True)
    parser.add_argument("--fuentes", help="JSON con filas [fuente, qué aportó, fecha]")
    parser.add_argument("--nota", help="texto que sustituye la nota de metodología genérica")
    args = parser.parse_args()

    html_path = Path(args.html)
    text = html_path.read_text(encoding="utf-8")
    rows = json.loads(Path(args.fuentes).read_text(encoding="utf-8")) if args.fuentes else None
    patched = patch_sources(text, rows, args.nota)
    if patched != text:
        html_path.write_text(patched, encoding="utf-8")
    engine = to_pdf(html_path, Path(args.pdf))
    print(json.dumps({"pdf": str(Path(args.pdf).resolve()), "motor": engine}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
