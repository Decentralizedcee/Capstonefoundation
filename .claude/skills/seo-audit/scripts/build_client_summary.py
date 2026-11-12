#!/usr/bin/env python3
"""Make the client-friendly summary PDF from client_summary.json. Needs reportlab (pip install reportlab).

  python3 build_client_summary.py <client_summary.json>   ->  writes client-summary.pdf next to it

client_summary.json (plain English, no jargon, written from the real findings only):
  {"title": "...", "subtitle": "Website check, 12 November 2026", "sections": [
     {"heading": "What we looked at", "text": "paragraph"},
     {"heading": "What we recommend", "numbered": ["item", "item"]},
     {"heading": "Speed test", "table": [["Page","Score","Main image shows after"], ...], "text": "optional note"}],
   "footer": "short line"}
Shown to the owner for approval BEFORE it is built. Never include anything not in the audit.
"""
import json, os, sys
from xml.sax.saxutils import escape


def main(argv):
    if len(argv) != 2:
        print(__doc__); return 2
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import mm
        from reportlab.platypus import ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    except ImportError:
        print("reportlab is missing. Run: pip install reportlab"); return 1
    d = json.load(open(argv[1], encoding="utf-8"))
    out = os.path.join(os.path.dirname(os.path.abspath(argv[1])), "client-summary.pdf")
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["BodyText"], fontSize=10.5, leading=15, spaceAfter=6)
    h = ParagraphStyle("h", parent=ss["Heading2"], fontSize=13, spaceBefore=12, spaceAfter=4, textColor=colors.HexColor("#222222"))
    t = ParagraphStyle("t", parent=ss["Title"], fontSize=20, leading=24, alignment=0, spaceAfter=2)
    sub = ParagraphStyle("s", parent=body, textColor=colors.HexColor("#555555"))
    doc = SimpleDocTemplate(out, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=18*mm, bottomMargin=18*mm, title=d.get("title", "Website check"))
    story = [Paragraph(escape(d.get("title", "")), t), Paragraph(escape(d.get("subtitle", "")), sub)]
    for s in d.get("sections", []):
        story.append(Paragraph(escape(s["heading"]), h))
        if s.get("text"): story.append(Paragraph(escape(s["text"]), body))
        if s.get("numbered"):
            story.append(ListFlowable([ListItem(Paragraph(escape(x), body)) for x in s["numbered"]], bulletType="1", leftIndent=14))
        if s.get("bullets"):
            story.append(ListFlowable([ListItem(Paragraph(escape(x), body)) for x in s["bullets"]], bulletType="bullet", leftIndent=14))
        if s.get("table"):
            rows = [[Paragraph(escape(str(c)), body) for c in r] for r in s["table"]]
            tb = Table(rows, hAlign="LEFT"); tb.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#bbbbbb")), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eeeeee")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            story += [Spacer(1, 3), tb]
    if d.get("footer"): story += [Spacer(1, 10), Paragraph(escape(d["footer"]), sub)]
    doc.build(story); print("Wrote", out); return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
