#!/usr/bin/env python3
"""Builds the two Une Femme Divine guides into standalone, upload-ready HTML files.

  python3 guides/build.py

Reads  guides/src/{ritual,planner}.html + base.css + common.js + assets/*.png
Writes guides/divine-ritual-guide.html and guides/rhythm-planner.html   (host these)
       guides/_preview/*.html                                           (artifact-safe copies: no print/download buttons)
"""
import base64, io, re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"


def data_uri(name: str) -> str:
    im = Image.open(SRC / "assets" / name).convert("RGBA")
    q = im.quantize(colors=48, method=Image.Quantize.FASTOCTREE)  # keeps alpha, shrinks the file a lot
    buf = io.BytesIO()
    q.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def assemble(page: str) -> str:
    html = (SRC / page).read_text()
    html = html.replace("/*@BASE_CSS*/", (SRC / "base.css").read_text())
    html = html.replace("/*@COMMON_JS*/", (SRC / "common.js").read_text())
    for token, asset in (("@@MARK_LIGHT@@", "mark-gold.png"), ("@@MARK_INK@@", "mark-ink.png"), ("@@MARK@@", "mark-gold.png"),
                         ("@@WORD_GOLD@@", "word-gold.png"), ("@@WORD@@", "word-ink.png")):
        if token in html:
            html = html.replace(token, data_uri(asset))
    return html


def preview_variant(html: str) -> str:
    """The Artifact viewer blocks downloads and printing, so drop those buttons and the document wrapper."""
    html = re.sub(r"<!--hosted-->.*?<!--/hosted-->", "", html, flags=re.S)
    html = re.sub(r"<!doctype html>\s*", "", html, flags=re.I)
    html = re.sub(r"</?(html|head|body)[^>]*>\s*", "", html)
    html = re.sub(r'<meta charset="utf-8">\s*', "", html)
    html = re.sub(r'<meta name="viewport"[^>]*>\s*', "", html)
    return html


def keep_hosted(html: str) -> str:
    return html.replace("<!--hosted-->", "").replace("<!--/hosted-->", "")


def assemble_print(page: str) -> str:
    html = (SRC / page).read_text()
    html = html.replace("/*@PRINT_CSS*/", (SRC / "print.css").read_text())
    return html.replace("@@MARK@@", data_uri("mark-gold.png"))


if __name__ == "__main__":
    (ROOT / "_print").mkdir(exist_ok=True)
    for page, out in (("print-ritual.html", "ritual.html"), ("print-planner.html", "planner.html")):
        (ROOT / "_print" / out).write_text(assemble_print(page))
    (ROOT / "_preview").mkdir(exist_ok=True)
    for page, out in (("ritual.html", "divine-ritual-guide.html"), ("planner.html", "rhythm-planner.html")):
        full = assemble(page)
        (ROOT / out).write_text(keep_hosted(full))
        (ROOT / "_preview" / out).write_text(preview_variant(full))
        print(f"{out}: {(ROOT / out).stat().st_size / 1024:.0f} KB")
