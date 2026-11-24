"""Adds real, fillable PDF form fields (text boxes and tick boxes) on top of the Chrome-rendered pages.
usage: python3 guides/tools/add-fields.py
"""
import json, io
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color

ROOT = Path(__file__).resolve().parents[1]
PX = 0.75            # css px -> pt
PAGE_H = 841.89      # A4 height in pt
INK = Color(0x3B / 255, 0x1F / 255, 0x2B / 255)

def build(name, src):
    fields = json.loads((ROOT / "_print" / f"{src}.fields.json").read_text())
    base = PdfReader(str(ROOT / "_print" / f"{name}.base.pdf"))
    n = len(base.pages)
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(595.28, PAGE_H))
    for page in range(n):
        for f in (x for x in fields if x["page"] == page):
            x, w, h = f["x"] * PX, f["w"] * PX, f["h"] * PX
            y = PAGE_H - (f["y"] * PX) - h
            nm = f["name"]
            if f["type"] == "check":
                c.acroForm.checkbox(name=nm, x=x, y=y, size=min(w, h), buttonStyle="check", borderWidth=0, borderColor=None, fillColor=None, textColor=INK, forceBorder=False, tooltip=nm.replace("_", " "))
            else:
                c.acroForm.textfield(name=nm, x=x, y=y, width=w, height=h, borderWidth=0, borderColor=None, fillColor=None, textColor=INK, fontName="Helvetica", fontSize=min(10, max(7, h - 3)), forceBorder=False, tooltip=nm.replace("_", " "))
        c.showPage()
    c.save(); buf.seek(0)
    overlay = PdfReader(buf)
    w = PdfWriter(clone_from=overlay)          # keeps the form (AcroForm) of the overlay
    for i, pg in enumerate(w.pages):
        pg.merge_page(base.pages[i], over=False)   # put the designed page underneath the fields
    out = ROOT / "pdf" / f"{name}.pdf"
    out.parent.mkdir(exist_ok=True)
    w.write(str(out))
    print(out.name, n, "pages,", len(fields), "fields,", round(out.stat().st_size / 1024), "KB")

build("Your-Divine-Ritual", "ritual")
build("Rhythm-of-the-Body", "planner")
build("Divine-Ritual-Pack-Partner", "partner")
build("Une-Femme-Divine-Partner-Pitch", "pitch")
