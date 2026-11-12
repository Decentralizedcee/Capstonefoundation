#!/usr/bin/env python3
"""Build a copy-paste blog post package. Standard library only.

  python3 build_package.py <post.json> <out_dir> [--zip] [--site-url https://example.com]

Reads one post (see references/post-package-spec.md), cleans the HTML so it pastes well,
checks the post, and writes <out_dir>/<slug>/ with:
  post-preview.html   interactive page: copy buttons, preview, where-to-paste guide, checks
  body.html           the clean HTML body only
  post.md             the same post as Markdown
  fields.txt          every field as plain text
  schema.jsonld.html  optional structured data (Article and FAQ)
  images.md           every image: alt text, caption, credit, where it goes
  lint-report.txt     the checks, in plain words
  HOW-TO-PUBLISH.md   short steps
  images/             copies of the owner's own image files, if given

Exit code 1 if any check FAILS, otherwise 0.
"""
import html
import json
import os
import re
import shutil
import sys
import zipfile
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "assets", "preview-template.html")

ALLOWED = {"h2", "h3", "h4", "p", "ul", "ol", "li", "a", "strong", "em", "blockquote", "img", "figure",
           "figcaption", "br", "hr", "table", "thead", "tbody", "tr", "th", "td"}
VOID = {"img", "br", "hr"}
ATTRS = {"a": {"href", "title"}, "img": {"src", "alt", "width", "height"}}
DROP_WITH_CONTENT = {"script", "style", "iframe", "object", "embed", "noscript", "template"}
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
GENERIC_LINK = {"click here", "here", "read more", "this link", "link", "more", "this"}


# ---------------------------------------------------------------- cleaning
class Sanitizer(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.removed, self.skip = [], [], 0

    def handle_starttag(self, tag, attrs):
        if tag in DROP_WITH_CONTENT:
            self.skip += 1
            self.removed.append(f"<{tag}> and its content")
            return
        if self.skip:
            return
        if tag not in ALLOWED:
            self.removed.append(f"<{tag}> tag")
            return
        keep = []
        for k, v in attrs:
            v = v or ""
            if k not in ATTRS.get(tag, ()):
                self.removed.append(f'"{k}" attribute on <{tag}>')
                continue
            if k in ("href", "src") and re.match(r"\s*(javascript|vbscript|data):", v, re.I):
                self.removed.append(f'unsafe {k} on <{tag}>')
                continue
            keep.append((k, v))
        attr_txt = "".join(f' {k}="{html.escape(v, quote=True)}"' for k, v in keep)
        self.out.append(f"<{tag}{attr_txt}>")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag in DROP_WITH_CONTENT:
            self.skip = max(0, self.skip - 1)
            return
        if self.skip or tag not in ALLOWED or tag in VOID:
            return
        self.out.append(f"</{tag}>")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(html.escape(data, quote=False))


def sanitize(body):
    s = Sanitizer()
    s.feed(body)
    s.close()
    cleaned = "".join(s.out)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
    return cleaned, sorted(set(s.removed))


class Analyzer(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.headings, self.links, self.imgs, self.text = [], [], [], []
        self._cur = None
        self._link = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("h1", "h2", "h3", "h4"):
            self._cur = [int(tag[1]), ""]
        elif tag == "a":
            self._link = [a.get("href", ""), ""]
        elif tag == "img":
            self.imgs.append(a)

    def handle_endtag(self, tag):
        if tag in ("h1", "h2", "h3", "h4") and self._cur:
            self.headings.append(tuple(self._cur))
            self._cur = None
        elif tag == "a" and self._link:
            self.links.append(tuple(self._link))
            self._link = None

    def handle_data(self, d):
        self.text.append(d)
        if self._cur is not None:
            self._cur[1] += d
        if self._link is not None:
            self._link[1] += d


# ---------------------------------------------------------------- markdown
class ToMarkdown(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.buf = ""
        self.lists = []
        self.marks = []
        self.rows, self.row, self.cell, self.in_cell = [], None, "", False

    def _blank(self):
        self.buf = self.buf.rstrip(" ")
        if self.buf and not self.buf.endswith("\n\n"):
            self.buf += "\n" if self.buf.endswith("\n") else "\n\n"

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("h2", "h3", "h4"):
            self._blank(); self.buf += "#" * int(tag[1]) + " "
        elif tag == "p":
            self._blank()
        elif tag in ("ul", "ol"):
            if not self.lists: self._blank()
            self.lists.append([tag, 0])
        elif tag == "li":
            if not self.buf.endswith("\n"): self.buf += "\n"
            top = self.lists[-1] if self.lists else ["ul", 0]
            top[1] += 1
            self.buf += "  " * (len(self.lists) - 1) + ("- " if top[0] == "ul" else f"{top[1]}. ")
        elif tag == "a":
            self.marks.append(("a", len(self.buf), a.get("href", "")))
        elif tag in ("strong", "em"):
            self.buf += "**" if tag == "strong" else "*"
        elif tag == "blockquote":
            self._blank(); self.marks.append(("q", len(self.buf), ""))
        elif tag == "img":
            self.buf += f"![{a.get('alt', '')}]({a.get('src', '')})"
        elif tag == "figcaption":
            self.buf += "\n*"
        elif tag == "br":
            self.buf += "  \n"
        elif tag == "hr":
            self._blank(); self.buf += "---\n\n"
        elif tag == "figure":
            self._blank()
        elif tag == "table":
            self._blank(); self.rows = []
        elif tag == "tr":
            self.row = []
        elif tag in ("td", "th"):
            self.in_cell, self.cell = True, ""

    def handle_endtag(self, tag):
        if tag in ("h2", "h3", "h4", "p", "figure"):
            self.buf += "\n\n"
        elif tag in ("ul", "ol"):
            self.lists.pop()
            self.buf += "\n"
        elif tag == "li":
            self.buf += "\n"
        elif tag == "a" and self.marks:
            kind, pos, href = self.marks.pop()
            text = self.buf[pos:]
            self.buf = self.buf[:pos] + f"[{text}]({href})"
        elif tag in ("strong", "em"):
            self.buf += "**" if tag == "strong" else "*"
        elif tag == "blockquote" and self.marks:
            kind, pos, _ = self.marks.pop()
            text = self.buf[pos:].strip()
            self.buf = self.buf[:pos] + "\n".join("> " + l for l in text.splitlines()) + "\n\n"
        elif tag == "figcaption":
            self.buf += "*\n"
        elif tag in ("td", "th") and self.row is not None:
            self.row.append(self.cell.strip().replace("|", "\\|")); self.in_cell = False
        elif tag == "tr" and self.row is not None:
            self.rows.append(self.row); self.row = None
        elif tag == "table" and self.rows:
            width = max(len(r) for r in self.rows)
            rows = [r + [""] * (width - len(r)) for r in self.rows]
            lines = ["| " + " | ".join(rows[0]) + " |", "| " + " | ".join(["---"] * width) + " |"]
            lines += ["| " + " | ".join(r) + " |" for r in rows[1:]]
            self.buf += "\n".join(lines) + "\n\n"

    def handle_data(self, d):
        if self.in_cell:
            self.cell += d
        else:
            self.buf += re.sub(r"\s+", " ", d) if d.strip() else (" " if d else "")


def to_markdown(body):
    p = ToMarkdown()
    p.feed(body)
    p.close()
    return re.sub(r"\n{3,}", "\n\n", p.buf).strip() + "\n"


# ---------------------------------------------------------------- building
def image_block(n, img):
    alt = html.escape(img.get("alt", ""), quote=True)
    if img.get("mode") == "url" and img.get("url"):
        size = ""
        if img.get("width") and img.get("height"):
            size = f' width="{int(img["width"])}" height="{int(img["height"])}"'
        cap = img.get("caption", "")
        credit = img.get("credit", "")
        line = " ".join(x for x in (cap, credit) if x).strip()
        figcap = f"<figcaption>{line}</figcaption>" if line else ""
        return f'<figure><img src="{html.escape(img["url"], quote=True)}" alt="{alt}"{size}>{figcap}</figure>'
    what = img.get("description") or img.get("alt") or "image"
    return f"<p><strong>[IMAGE {n}: {html.escape(what)}. Insert it from images.md using your editor's image button, then delete this line.]</strong></p>"


def faq_html(faq, heading):
    parts = [f"<h2>{html.escape(heading)}</h2>"]
    for item in faq:
        parts.append(f"<h3>{html.escape(item['q'])}</h3>")
        parts.append(f"<p>{item['a_html'] if 'a_html' in item else html.escape(item['a'])}</p>")
    return "\n".join(parts)


def assemble_body(post):
    body = post.get("body_html", "")
    images = post.get("images", [])
    for n, img in enumerate(images, 1):
        body = body.replace(f"[[IMAGE:{n}]]", image_block(n, img))
    if post.get("faq"):
        block = faq_html(post["faq"], post.get("faq_heading", "Frequently asked questions"))
        body = body.replace("[[FAQ]]", block) if "[[FAQ]]" in body else body.rstrip() + "\n" + block
    return body


def words_of(text):
    """Plain word list used to compare two texts (ignores case, punctuation, tags and Markdown marks)."""
    text = re.sub(r"\[\[(?:IMAGE:\d+|FAQ)\]\]", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"(?m)^\s*(?:#+|>|[-*+]|\d+[.)])\s+", " ", text)
    text = html.unescape(text).replace("\u2019", "'")
    return re.findall(r"[\w']+", text.lower())


def exact_check(post, add):
    """Mode 'use mine exactly': the post body must hold the owner's words unchanged."""
    brief = post.get("brief") or {}
    path = brief.get("original_file", "")
    if not path or not os.path.isfile(path):
        add("FAIL", "Content mode is 'use mine exactly' but brief.original_file is missing or not found, so the owner's wording cannot be checked.")
        return
    with open(path, encoding="utf-8", errors="replace") as fh:
        original = fh.read()
    original = re.sub(r"\A\s*(?:# [^\n]*\n|<h1[^>]*>.*?</h1>)", "", original, flags=re.S | re.I)  # the title is a separate field
    a = words_of(original)
    b = words_of(post.get("body_html", ""))
    if a == b:
        add("PASS", f"Owner's wording unchanged ({len(a)} words match their original exactly).")
        return
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]:
        i += 1
    ctx = lambda w: " ".join(w[max(0, i - 4):i + 6])
    add("FAIL", f"Owner's wording was changed (original {len(a)} words, post {len(b)} words). First difference near word {i + 1}: "
                f"original says '{ctx(a)}' but the post says '{ctx(b)}'. Restore their words or get their permission.")


def lint(post, body, removed, site_url, had_h1=False):
    res = []
    add = lambda lvl, msg: res.append((lvl, msg))
    kw = (post.get("primary_keyword") or "").strip().lower()
    brief = post.get("brief") or {}
    if brief:
        add("INFO", f"Brief: voice = {brief.get('voice') or 'not recorded'}; content = {brief.get('content_mode') or 'write it for me'}.")
        if brief.get("content_mode") == "exact":
            exact_check(post, add)

    def need(key, label):
        if not str(post.get(key, "")).strip():
            add("FAIL", f"Missing {label}.")
            return False
        return True

    need("title", "title"); need("body_html", "post body")
    if need("seo_title", "search title (SEO title)"):
        n = len(post["seo_title"])
        add("PASS" if 30 <= n <= 60 else "WARN", f"Search title is {n} characters (aim for 30 to 60).")
    if need("meta_description", "meta description"):
        n = len(post["meta_description"])
        add("PASS" if 70 <= n <= 160 else "WARN", f"Meta description is {n} characters (aim for 70 to 160).")
    slug = post.get("slug", "")
    if not slug:
        add("FAIL", "Missing URL slug.")
    elif not SLUG_RE.match(slug):
        add("FAIL", "URL slug must be lowercase letters, numbers and single dashes (for example how-to-fix-a-leaky-tap).")
    else:
        add("PASS", "URL slug is clean.")
    ex = len(post.get("excerpt", ""))
    if ex == 0:
        add("WARN", "No excerpt (the short summary shown on blog listings).")
    elif ex > 300:
        add("WARN", f"Excerpt is {ex} characters (aim for 300 or fewer).")
    tags = post.get("tags", [])
    add("PASS" if 1 <= len(tags) <= 8 else "WARN", f"{len(tags)} tag(s) (aim for 1 to 8).")

    an = Analyzer(); an.feed(body); an.close()
    words = re.findall(r"[A-Za-z0-9’']+", " ".join(an.text))
    add("INFO", f"Post body has about {len(words)} words.")
    tw = post.get("target_words")
    if tw:
        add("PASS" if 0.8 * tw <= len(words) <= 1.2 * tw else "WARN", f"Target length was {tw} words (within 20 percent is fine).")
    if had_h1 or any(h[0] == 1 for h in an.headings):
        add("FAIL", "The body contains an H1. Your site shows the title as the H1, so the body must start with H2 headings.")
    h2 = [h for h in an.headings if h[0] == 2]
    add("PASS" if h2 else "WARN", f"{len(h2)} H2 section heading(s)." if h2 else "No H2 headings. Break the post into sections.")
    prev = 1
    skipped = False
    for lvl, _ in an.headings:
        if lvl > prev + 1: skipped = True
        prev = lvl
    if skipped:
        add("WARN", "Heading levels skip (for example H2 straight to H4).")

    if kw:
        first100 = " ".join(" ".join(an.text).split()[:100]).lower()
        add("PASS" if kw in first100 else "WARN", f'Primary keyword "{kw}" in the first 100 words.' if kw in first100 else f'Primary keyword "{kw}" is not in the first 100 words.')
        for key, label in (("title", "title"), ("seo_title", "search title"), ("meta_description", "meta description")):
            ok = kw in str(post.get(key, "")).lower()
            add("PASS" if ok else "WARN", f"Primary keyword in the {label}." if ok else f"Primary keyword is not in the {label}.")
        slugkw = re.sub(r"[^a-z0-9]+", "-", kw).strip("-")
        add("PASS" if slugkw and slugkw in slug else "WARN", "Primary keyword in the URL slug." if slugkw in slug else "Primary keyword is not in the URL slug.")
    else:
        add("WARN", "No primary keyword set, so keyword checks were skipped.")

    missing_alt = [i for i in an.imgs if not (i.get("alt") or "").strip()]
    if missing_alt:
        add("FAIL", f"{len(missing_alt)} image(s) in the body have no alt text.")
    for n, img in enumerate(post.get("images", []), 1):
        if not (img.get("alt") or "").strip():
            add("FAIL", f"Image {n} has no alt text.")
    if post.get("featured_image") and not (post["featured_image"].get("alt") or "").strip():
        add("FAIL", "The featured image has no alt text.")

    ph = len(re.findall(r"\[\[INTERNAL:[^\]]*\]\]", body))
    if ph:
        add("WARN", f"{ph} internal link placeholder(s) [[INTERNAL:...]] still to replace with real page links.")
    internal = external = 0
    generic = []
    for href, text in an.links:
        if href.startswith("[["):
            continue
        is_internal = href.startswith("/") or href.startswith("#") or (site_url and href.startswith(site_url))
        internal += bool(is_internal); external += (not is_internal) and href.startswith("http")
        if text.strip().lower() in GENERIC_LINK:
            generic.append(text.strip())
    add("PASS" if internal + ph >= 3 else "WARN", f"{internal} real internal link(s) plus {ph} placeholder(s) (aim for 3 to 5).")
    add("PASS" if 2 <= external <= 4 else "WARN", f"{external} external link(s) (aim for 2 to 3 reputable sources).")
    if generic:
        add("WARN", f"Vague link text found ({', '.join(sorted(set(generic)))}). Use descriptive words.")
    todo = re.findall(r"TODO\(owner\)[^<]{0,60}|\bTBD\b", body)
    if todo:
        add("WARN", f"{len(todo)} TODO or TBD note(s) left in the text.")
    markers = len(re.findall(r"\[IMAGE \d+:", body))
    if markers:
        add("INFO", f"{markers} image marker(s) to replace with uploaded images.")
    faq = post.get("faq", [])
    add("PASS" if 4 <= len(faq) <= 8 else "WARN", f"{len(faq)} FAQ question(s) (aim for 4 to 8)." )
    if removed:
        add("WARN", "Removed so the post pastes cleanly: " + "; ".join(removed) + ".")
    return res


def schema_block(post, site_url):
    art = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": post.get("title", ""),
           "description": post.get("meta_description", "")}
    if post.get("date"): art["datePublished"] = post["date"]
    if post.get("author"): art["author"] = {"@type": "Person", "name": post["author"]}
    fi = post.get("featured_image") or {}
    if fi.get("url"): art["image"] = [fi["url"]]
    if post.get("canonical_url"): art["mainEntityOfPage"] = post["canonical_url"]
    graph = [art]
    if post.get("faq"):
        graph.append({"@context": "https://schema.org", "@type": "FAQPage",
                      "mainEntity": [{"@type": "Question", "name": q["q"],
                                      "acceptedAnswer": {"@type": "Answer", "text": q["a"]}} for q in post["faq"]]})
    out = []
    for g in graph:
        js = json.dumps(g, indent=2, ensure_ascii=False).replace("</", "<\\/")
        out.append(f'<script type="application/ld+json">\n{js}\n</script>')
    return "\n".join(out)


def field_row(fid, label, hint, value, multi=False, count=None):
    v = html.escape(value or "", quote=True)
    ctl = (f'<textarea id="{fid}" readonly>{html.escape(value or "")}</textarea>' if multi
           else f'<input id="{fid}" type="text" readonly value="{v}">')
    cnt = ""
    if count:
        cnt = f'<div class="count" data-count-for="{fid}" data-min="{count[0]}" data-max="{count[1]}"></div>'
    return (f'<div class="field"><label for="{fid}">{html.escape(label)}<span class="hint">{html.escape(hint)}</span></label>'
            f'<div>{ctl}{cnt}</div><button type="button" data-copy="{fid}" data-label="{html.escape(label, quote=True)}">Copy</button></div>')


def images_html(post):
    items = []
    fi = post.get("featured_image")
    if fi: items.append(("Featured image", fi))
    for n, im in enumerate(post.get("images", []), 1):
        items.append((f"Image {n}", im))
    if not items:
        return '<p class="sub">This post has no images.</p>'
    rows = []
    for label, im in items:
        src = im.get("url") or im.get("file") or ""
        how = "Already in the text (linked from its source)" if im.get("mode") == "url" and label != "Featured image" else "Upload it on your site, then insert it where noted" if im.get("mode") != "url" else "Use this link as the featured image, or download and upload it (check the licence)"
        rows.append(f"<tr><td><b>{label}</b></td><td>{html.escape(str(src))}<br><small>{html.escape(how)}</small></td>"
                    f"<td>{html.escape(im.get('alt', ''))}</td><td>{html.escape(im.get('placement', ''))}"
                    f"{('<br><small>' + html.escape(im['credit']) + '</small>') if im.get('credit') else ''}</td></tr>")
    return ('<table class="t"><thead><tr><th>Image</th><th>File or link</th><th>Alt text</th><th>Where / credit</th></tr></thead><tbody>'
            + "".join(rows) + "</tbody></table>")


def build(post_path, out_dir, make_zip=False, site_url=""):
    with open(post_path, encoding="utf-8") as fh:
        post = json.load(fh)
    slug = post.get("slug") or "post"
    if not SLUG_RE.match(slug):
        slug = re.sub(r"[^a-z0-9]+", "-", slug.lower()).strip("-") or "post"
    site_url = (site_url or post.get("site_url") or "").rstrip("/")

    assembled = assemble_body(post)
    body, removed = sanitize(assembled)
    results = lint(post, body, removed, site_url, had_h1=bool(re.search(r"<h1\b", assembled, re.I)))
    fails = [m for l, m in results if l == "FAIL"]

    pkg = os.path.join(out_dir, slug)
    os.makedirs(pkg, exist_ok=True)

    def write(name, text):
        with open(os.path.join(pkg, name), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)

    md = to_markdown(body)
    schema = schema_block(post, site_url)
    write("body.html", body + "\n")
    write("post.md", f"# {post.get('title', '')}\n\n{md}")
    write("schema.jsonld.html", schema + "\n")

    fields = [("Title", post.get("title", "")), ("SEO title", post.get("seo_title", "")),
              ("Meta description", post.get("meta_description", "")), ("URL slug", post.get("slug", slug)),
              ("Excerpt", post.get("excerpt", "")), ("Tags", ", ".join(post.get("tags", []))),
              ("Category", post.get("category", "")), ("Author", post.get("author", "")),
              ("Suggested publish date", post.get("date", "")),
              ("Featured image alt text", (post.get("featured_image") or {}).get("alt", ""))]
    soc = post.get("social") or {}
    for k, v in soc.items(): fields.append((f"Social post ({k})", v))
    write("fields.txt", "\n".join(f"{k}: {v}" for k, v in fields) + "\n")

    imgs = []
    allimgs = ([("Featured image", post["featured_image"])] if post.get("featured_image") else []) + \
              [(f"Image {n}", im) for n, im in enumerate(post.get("images", []), 1)]
    img_dir = os.path.join(pkg, "images")
    for label, im in allimgs:
        f = im.get("file")
        if f and im.get("mode") != "url":
            if os.path.isfile(f):
                os.makedirs(img_dir, exist_ok=True)
                shutil.copy2(f, os.path.join(img_dir, os.path.basename(f)))
            else:
                results.append(("WARN", f"{label}: file not found ({f}), so it was not copied into the package."))
        imgs.append(f"## {label}\n- Source: {im.get('url') or im.get('file') or 'not set'}\n- Alt text: {im.get('alt', '')}\n"
                    f"- Caption: {im.get('caption', '')}\n- Credit line: {im.get('credit', '') or 'none needed'}\n"
                    f"- Where it goes: {im.get('placement', '')}\n- Description: {im.get('description', '')}\n")
    write("images.md", "# Images for this post\n\nRecommended: about 1200 by 630 pixels for the featured image, no wider than 1600 pixels for others, WebP or JPEG, ideally under 200 KB.\n\n" + ("\n".join(imgs) or "No images.\n"))

    lint_txt = "\n".join(f"{l:5} {m}" for l, m in results)
    counts = {k: sum(1 for l, _ in results if l == k) for k in ("PASS", "WARN", "FAIL")}
    write("lint-report.txt", lint_txt + f"\n\nSummary: {counts['PASS']} passed, {counts['WARN']} warning(s), {counts['FAIL']} failed\n")

    platform = (post.get("platform") or "").lower()
    write("HOW-TO-PUBLISH.md",
          "# How to publish this post\n\n1. Open `post-preview.html` in your browser.\n2. Use the **Copy** buttons to paste each field into your site.\n"
          "3. Paste the post body (formatted, or as HTML code in the HTML/code view).\n4. Upload the images and replace the image markers.\n"
          "5. Replace any `[[INTERNAL:...]]` or TODO notes, save as a draft, check the preview, then publish.\n"
          "The preview page has a short guide for Shopify, WordPress and other platforms.\n")

    with open(TEMPLATE, encoding="utf-8") as fh:
        page = fh.read()
    rendered = re.sub(r"\[\[INTERNAL:([^\]]*)\]\]", r"<mark>[link: \1]</mark>", body)
    lint_html = "<ul>" + "".join(f'<li class="{l}"><b>{l}</b> {html.escape(m)}</li>' for l, m in results) + "</ul>"
    fields_html = "".join([
        field_row("f-title", "Title", "The post's headline. Your site shows it as the main heading.", post.get("title", "")),
        field_row("f-seo", "SEO title", "Shown in Google results.", post.get("seo_title", ""), count=(30, 60)),
        field_row("f-meta", "Meta description", "The text under the title in Google results.", post.get("meta_description", ""), multi=True, count=(70, 160)),
        field_row("f-slug", "URL slug", "The last part of the web address.", post.get("slug", slug)),
        field_row("f-excerpt", "Excerpt", "Short summary for blog listings.", post.get("excerpt", ""), multi=True, count=(0, 300)),
        field_row("f-tags", "Tags", "Separated by commas.", ", ".join(post.get("tags", []))),
        field_row("f-alt", "Featured image alt text", "Describes the main image for screen readers and search.", (post.get("featured_image") or {}).get("alt", "")),
    ] + ([field_row("f-cat", "Category", "", post["category"])] if post.get("category") else [])
      + ([field_row("f-author", "Author", "", post["author"])] if post.get("author") else [])
      + [field_row(f"f-soc{i}", f"Social post ({k})", "Optional share text.", v, multi=True) for i, (k, v) in enumerate(soc.items())])
    repl = {
        "{{PAGE_TITLE}}": html.escape(post.get("title", "")), "{{TITLE_ESC}}": html.escape(post.get("title", "")),
        "{{FIELDS_HTML}}": fields_html, "{{BODY_RENDERED}}": rendered, "{{BODY_RAW_ESC}}": html.escape(body),
        "{{MD_ESC}}": html.escape(md), "{{SCHEMA_ESC}}": html.escape(schema), "{{IMAGES_HTML}}": images_html(post),
        "{{LINT_HTML}}": lint_html,
        "{{OPEN_SHOPIFY}}": "open" if platform == "shopify" else "", "{{OPEN_WORDPRESS}}": "open" if platform == "wordpress" else "",
        "{{OPEN_OTHER}}": "open" if platform not in ("shopify", "wordpress") else "",
    }
    for k, v in repl.items():
        page = page.replace(k, v)
    write("post-preview.html", page)

    zip_path = None
    if make_zip:
        zip_path = os.path.join(out_dir, f"{slug}-package.zip")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for d, subs, fs in os.walk(pkg):
                subs.sort()
                for f in sorted(fs):
                    if f == "post.json":
                        continue
                    full = os.path.join(d, f)
                    z.write(full, os.path.join(slug, os.path.relpath(full, pkg)))

    print(lint_txt)
    print(f"\nSummary: {counts['PASS']} passed, {counts['WARN']} warning(s), {counts['FAIL']} failed")
    print(f"Package folder: {pkg}" + (f"\nZIP: {zip_path}" if zip_path else ""))
    return 1 if fails else 0


def main(argv):
    args = [a for a in argv[1:] if a != "--zip"]
    make_zip = "--zip" in argv
    site_url = ""
    if "--site-url" in args:
        i = args.index("--site-url"); site_url = args[i + 1]; args = args[:i] + args[i + 2:]
    if len(args) < 2:
        print(__doc__); return 2
    return build(args[0], args[1], make_zip, site_url)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
