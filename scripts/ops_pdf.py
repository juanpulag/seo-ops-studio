#!/usr/bin/env python3
"""SEO Ops Studio · turn the HTML report into a PDF with the real data sources.

google_report.py generates the report's HTML. This script:
  1. Replaces the generic "Data Sources & Methodology" table with the sources
     actually used in the audit (so the report never claims data it did not have).
  2. Prints the HTML to an A4 PDF with Chromium (Playwright) or, if missing, with
     the installed Google Chrome. Does not depend on WeasyPrint.

Usage:
  seo-ops run ops_pdf.py --html report.html --pdf report.pdf \\
      [--sources sources.json] [--note "methodology text"]

sources.json: [["Source", "What it provided", "Date"], ...]
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
            print("Warning: the generic sources table was not found; the HTML was not changed at that point.", file=sys.stderr)
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
    raise RuntimeError("No browser available to print the PDF (" + "; ".join(errors) + "). Run /seo-ops-setup to prepare the runtime, or install Google Chrome.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--html", required=True)
    parser.add_argument("--pdf", required=True)
    parser.add_argument("--sources", help="JSON with rows [source, what it provided, date]")
    parser.add_argument("--note", help="text that replaces the generic methodology note")
    args = parser.parse_args()

    html_path = Path(args.html)
    text = html_path.read_text(encoding="utf-8")
    rows = json.loads(Path(args.sources).read_text(encoding="utf-8")) if args.sources else None
    patched = patch_sources(text, rows, args.note)
    if patched != text:
        html_path.write_text(patched, encoding="utf-8")
    engine = to_pdf(html_path, Path(args.pdf))
    print(json.dumps({"pdf": str(Path(args.pdf).resolve()), "engine": engine}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
