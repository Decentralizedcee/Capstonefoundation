"""Adds the 'Your buyer questions' page to docs/blog-anywhere-user-guide.pdf.

The original guide was generated with ReportLab and its generator was not kept, so this script edits the
existing PDF instead of rebuilding it: it inserts one new page after page 4, changes "five" to "six" on page 4,
adds a pointer box at the bottom of page 4 and moves the footer page numbers of the later pages up by one.
Run once on the 12 Nov 2026 version of the guide. Usage: python3 add_buyer_questions_page.py IN.pdf OUT.pdf
"""
import io
import sys

from pypdf import PdfReader, PdfWriter
from pypdf.generic import DecodedStreamObject, NameObject
from reportlab.lib.colors import Color, HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", FONT_DIR + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DV-B", FONT_DIR + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DV-M", FONT_DIR + "DejaVuSansMono.ttf"))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DV-B", italic="DV", boldItalic="DV-B")

NAVY = Color(.078431, .129412, .239216)
INK = Color(.2, .254902, .333333)
MUTED = Color(.392157, .454902, .545098)
LINE = HexColor("#cbd2dc")
TINT = HexColor("#eef2f9")
TIPBG = HexColor("#e6edfb")
TIPBAR = HexColor("#2f5bd1")
MINT = HexColor("#e6f4f1")

H1 = ParagraphStyle("h1", fontName="DV-B", fontSize=19, leading=24, textColor=NAVY, spaceAfter=6)
H2 = ParagraphStyle("h2", fontName="DV-B", fontSize=12, leading=16, textColor=NAVY, spaceBefore=10, spaceAfter=4)
P = ParagraphStyle("p", fontName="DV", fontSize=9.3, leading=13.2, textColor=INK, spaceAfter=3)
CELL = ParagraphStyle("c", parent=P, fontSize=8.8, leading=12, spaceAfter=0)
CELLB = ParagraphStyle("cb", parent=CELL, fontName="DV-B")
HEAD = ParagraphStyle("hd", parent=CELL, fontName="DV-B", textColor=HexColor("#ffffff"))
MONO = ParagraphStyle("m", fontName="DV-M", fontSize=8.4, leading=12, textColor=INK)
NUM = ParagraphStyle("n", parent=P, leftIndent=14, firstLineIndent=-14, spaceAfter=2)


def footer(canvas, doc, page_no):
    canvas.saveState()
    canvas.setFillColor(MUTED)
    canvas.setFont("DV", 8)
    canvas.drawString(50.4, 32.4, "Blog-Anywhere skill: your simple guide")
    canvas.drawString(534.2, 32.4, f"Page {page_no}")
    canvas.restoreState()


def build_new_page(new_page_no):
    buf = io.BytesIO()
    doc = BaseDocTemplate(buf, pagesize=(612, 792), leftMargin=50.4, rightMargin=50.4, topMargin=50, bottomMargin=50)
    frame = Frame(50.4, 50, 511.2, 792 - 100, leftPadding=6, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=lambda c, d: footer(c, d, new_page_no))])

    def table(rows, widths, header=None):
        data = [[Paragraph(x, st) for x, st in r] for r in rows]
        style = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("GRID", (0, 0), (-1, -1), .5, LINE),
                 ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                 ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                 ("BACKGROUND", (0, 0), (0, -1), TINT)]
        t = Table(data, colWidths=widths)
        t.setStyle(TableStyle(style))
        return t

    story = [
        Paragraph("3b. Your buyer questions (Claude can suggest them)", H1),
        Paragraph("A good post answers the questions a buyer asks <b>before</b> they say yes. Search engines and AI answers look for "
                  "clear, specific answers to exactly those questions. <b>You do not have to know them.</b> Claude can suggest "
                  "them and you pick. Pick one way:", P),
        Spacer(1, 2),
        table([[("I have my questions", CELLB), ("Type up to 10, in your own words. Claude uses them as you wrote them.", CELL)],
               [("Suggest some for me", CELLB), ("Claude asks a few basic questions, does some research, and shows a numbered list to pick from.", CELL)],
               [("A mix", CELLB), ("You give some. Claude suggests more to fill the gaps.", CELL)],
               [("Skip for now", CELLB), ("Claude still looks for gaps and shows them in the outline for your OK.", CELL)]],
              [130, 369]),
        Paragraph("If you choose &quot;suggest&quot;, Claude first asks (answer what you can)", H2),
        Paragraph("1.&nbsp;&nbsp;What is the post about, and what should the reader do afterwards (buy, book, subscribe, learn)?", NUM),
        Paragraph("2.&nbsp;&nbsp;Who is the reader, and what decision are they making?", NUM),
        Paragraph("3.&nbsp;&nbsp;What do customers usually ask you before they buy or book? Even two or three real ones help.", NUM),
        Paragraph("4.&nbsp;&nbsp;Is there anything the post must never claim or say?", NUM),
        Paragraph("&quot;I don't know&quot; is a fine answer to any of them.", P),
        Paragraph("Then Claude researches and gives you a pick-list", H2),
        Paragraph("It looks at what the top results answer, the &quot;people also ask&quot; style questions, a free question tool such as "
                  "AnswerThePublic where it can, your own pages and FAQs, and what a first-time buyer worries about (price, who it "
                  "suits, how to use it, what it does not do, delivery, returns).", P),
        Paragraph("You get <b>8 to 12 numbered suggestions</b>. Each says why a reader asks it and where the idea came from, and each is "
                  "marked as a suggestion. <b>Claude never invents numbers, customers or quotes.</b>", P),
        Paragraph("You reply with the numbers you want (5 to 10 is plenty), change any wording, or add your own. If you say "
                  "&quot;you choose&quot;, Claude picks 6 to 8 and tells you why.", P),
        Spacer(1, 3),
        Table([[Paragraph("Suggest the buyer questions for me. The post is about [your topic]. My reader is [who]. "
                          "Show me a numbered list I can pick from.", MONO)],
               [Paragraph("Use 1, 3, 4, 6 and 9. Change 3 to: [your wording]. Add: [your own question].", MONO)]],
              colWidths=[499],
              style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), HexColor("#f1f3f6")), ("GRID", (0, 0), (-1, -1), .5, LINE),
                                ("LEFTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 6),
                                ("BOTTOMPADDING", (0, 0), (-1, -1), 6)])),
        Paragraph("What happens next", H2),
        Paragraph("Your picks become the sections and the FAQ. Each one is answered in a short paragraph that still makes sense if it is "
                  "copied out on its own (it names the product or topic, says who it is for, and puts any limit next to the claim). "
                  "A question Claude has no facts for gets a note for you to fill in, <b>never a guess</b>.", P),
        Spacer(1, 4),
        Table([[Paragraph("<b>TIP</b> Do not make a separate page for every question. Google says creating pages for every possible "
                          "question just to win AI answers breaks its spam policy. A few real, specific answers beat many empty pages. "
                          "You also do not need an llms.txt file or special AI markup: Google says Search does not use them.", CELL)]],
              colWidths=[499],
              style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), TIPBG), ("LINEBEFORE", (0, 0), (0, -1), 3, TIPBAR),
                                ("LEFTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 7),
                                ("BOTTOMPADDING", (0, 0), (-1, -1), 7)])),
        Spacer(1, 4),
        Paragraph("Added 20 Nov 2026. Based on Neil Patel's video &quot;Google's New Rules for Getting Customers&quot; and Google's guide "
                  "&quot;Optimizing your website for generative AI features on Google Search&quot;.", ParagraphStyle("s", parent=P, fontSize=7.6, leading=10, textColor=MUTED)),
    ]
    doc.build(story)
    buf.seek(0)
    return PdfReader(buf)


def page4_overlay():
    buf = io.BytesIO()
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(buf, pagesize=(612, 792))
    # pointer box in the free space under the TIP box (page bottom area)
    x, y, w, h = 50.4, 60, 511.2, 50
    c.setFillColor(MINT)
    c.rect(x, y, w, h, stroke=0, fill=1)
    c.setFillColor(HexColor("#0f766e"))
    c.rect(x, y, 3, h, stroke=0, fill=1)
    c.setFillColor(INK)
    c.setFont("DV-B", 9.3)
    c.drawString(x + 14, y + h - 17, "6. Your buyer questions (new)")
    c.setFont("DV", 8.8)
    c.drawString(x + 14, y + h - 31, "Claude also asks what a buyer needs answered before they say yes, and it can suggest")
    c.drawString(x + 14, y + h - 43, "the questions for you to pick from. See the next page.")
    c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]


def set_stream(writer, page, data):
    s = DecodedStreamObject()
    s.set_data(data)
    page[NameObject("/Contents")] = writer._add_object(s)


def main(src, dst):
    writer = PdfWriter(clone_from=src)
    pages = writer.pages
    assert len(pages) == 7, "expected the 7-page 12 Nov 2026 guide"
    # footers of pages 5-7 become 6-8 (do the highest first so numbers never collide)
    for old in (7, 6, 5):
        pg = pages[old - 1]
        data = pg.get_contents().get_data()
        a, b = f"(Page {old})".encode(), f"(Page {old + 1})".encode()
        assert data.count(a) == 1, (old, data.count(a))
        set_stream(writer, pg, data.replace(a, b))
    # page 4: "five" -> "six" and the pointer box
    p4 = pages[3]
    data = p4.get_contents().get_data()
    a = b"asks five short things."
    assert data.count(a) == 1
    set_stream(writer, p4, data.replace(a, b"asks six short things."))
    p4.merge_page(page4_overlay())
    # new page 5
    new = build_new_page(5).pages[0]
    writer.insert_page(new, 4)
    # register any form widgets of the new page (there are none) and set metadata
    writer.add_metadata({"/Title": "Blog-Anywhere skill: your simple guide",
                         "/Subject": "A short interactive guide to using the blog-anywhere skill (updated 20 Nov 2026)",
                         "/Author": "Prepared with Claude Code"})
    with open(dst, "wb") as f:
        writer.write(f)
    print("written", dst, "pages:", len(writer.pages))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
