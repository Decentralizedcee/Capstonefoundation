#!/usr/bin/env python3
"""Collect SEO facts from one page. Standard library only. Read-only: one GET request, no logins, no forms.

  python3 audit_page.py <url-or-local-html-file> [--out DIR]

Prints a JSON summary and, with --out, saves it as DIR/<name>.json. For a URL it also fetches /robots.txt
and the sitemap(s) it names (or /sitemap.xml). Nothing is changed on the site. It records facts only;
the judging happens afterwards (see references/checks.md).
"""
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

UA = "seo-audit/1.0 (read-only page check)"


def fetch(url, limit=2_000_000):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            body = r.read(limit).decode(r.headers.get_content_charset() or "utf-8", errors="replace")
            return {"status": r.status, "final_url": r.geturl(), "headers": dict(r.headers), "body": body}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "final_url": url, "headers": dict(e.headers or {}), "body": "", "error": f"HTTP {e.code}"}
    except Exception as e:  # network blocked, DNS, timeout...
        return {"status": None, "final_url": url, "headers": {}, "body": "", "error": f"{type(e).__name__}: {e}"}


class Facts(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""; self.in_title = False
        self.meta = {}; self.links = []; self.headings = []; self.imgs = []; self.anchors = []
        self.jsonld = []; self.lang = ""; self.canonical = ""; self.hreflang = []
        self._h = None; self._a = None; self._ld = False; self._ldbuf = ""; self.text = []; self._skip = 0

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag == "html": self.lang = a.get("lang", "")
        elif tag == "title": self.in_title = True
        elif tag == "meta":
            key = (a.get("name") or a.get("property") or a.get("http-equiv") or "").lower()
            if key: self.meta[key] = a.get("content", "")
        elif tag == "link":
            rel = a.get("rel", "").lower()
            if "canonical" in rel: self.canonical = a.get("href", "")
            if "alternate" in rel and a.get("hreflang"): self.hreflang.append(a["hreflang"])
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"): self._h = [int(tag[1]), ""]
        elif tag == "img": self.imgs.append({"src": a.get("src") or a.get("data-src", ""), "alt": a.get("alt"), "width": a.get("width"), "height": a.get("height"), "loading": a.get("loading")})
        elif tag == "a": self._a = [a.get("href", ""), ""]
        elif tag == "script":
            self._skip += 1
            if "ld+json" in a.get("type", "").lower(): self._ld = True; self._ldbuf = ""
        elif tag == "style": self._skip += 1

    def handle_endtag(self, tag):
        if tag == "title": self.in_title = False
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6") and self._h:
            self.headings.append({"level": self._h[0], "text": " ".join(self._h[1].split())}); self._h = None
        elif tag == "a" and self._a:
            self.anchors.append({"href": self._a[0], "text": " ".join(self._a[1].split())}); self._a = None
        elif tag == "script":
            self._skip = max(0, self._skip - 1)
            if self._ld:
                self._ld = False
                try: self.jsonld.append(json.loads(self._ldbuf))
                except ValueError: self.jsonld.append({"_invalid_json": True})
        elif tag == "style": self._skip = max(0, self._skip - 1)

    def handle_data(self, d):
        if self.in_title: self.title += d
        if self._h is not None: self._h[1] += d
        if self._a is not None: self._a[1] += d
        if self._ld: self._ldbuf += d
        if not self._skip: self.text.append(d)


def jsonld_types(items):
    out = []
    def walk(x):
        if isinstance(x, dict):
            t = x.get("@type")
            if t: out.extend(t if isinstance(t, list) else [t])
            for v in x.values(): walk(v)
        elif isinstance(x, list):
            for v in x: walk(v)
    walk(items)
    return sorted(set(map(str, out)))


def analyse(html_text, page_url=""):
    f = Facts(); f.feed(html_text)
    words = re.findall(r"\w+", " ".join(f.text))
    base = urllib.parse.urlparse(page_url).netloc
    internal = external = 0
    for a in f.anchors:
        h = a["href"]
        if not h or h.startswith(("#", "mailto:", "tel:", "javascript:")): continue
        host = urllib.parse.urlparse(urllib.parse.urljoin(page_url, h)).netloc
        if not base or host == base: internal += 1
        else: external += 1
    vague = sorted({a["text"] for a in f.anchors if a["text"].lower() in ("click here", "here", "read more", "learn more", "more")})
    return {
        "title": " ".join(f.title.split()), "title_length": len(" ".join(f.title.split())),
        "meta_description": f.meta.get("description"), "meta_description_length": len(f.meta.get("description") or ""),
        "robots_meta": f.meta.get("robots"), "viewport": f.meta.get("viewport"), "lang": f.lang,
        "canonical": f.canonical, "hreflang": f.hreflang,
        "open_graph": {k: v for k, v in f.meta.items() if k.startswith("og:")},
        "twitter_card": f.meta.get("twitter:card"),
        "h1_count": sum(1 for h in f.headings if h["level"] == 1), "headings": f.headings,
        "heading_order_skips": any(b["level"] - a["level"] > 1 for a, b in zip(f.headings, f.headings[1:])),
        "images_total": len(f.imgs), "images_missing_alt": sum(1 for i in f.imgs if i["alt"] is None),
        "images_empty_alt": sum(1 for i in f.imgs if i["alt"] == ""),
        "images_missing_dimensions": sum(1 for i in f.imgs if not (i["width"] and i["height"])),
        "images": f.imgs[:60],
        "internal_links": internal, "external_links": external, "vague_link_text": vague,
        "structured_data_types": jsonld_types(f.jsonld), "structured_data_invalid_blocks": sum(1 for x in f.jsonld if isinstance(x, dict) and x.get("_invalid_json")),
        "word_count": len(words),
    }


def site_files(url):
    p = urllib.parse.urlparse(url); root = f"{p.scheme}://{p.netloc}"
    out = {"https": p.scheme == "https"}
    r = fetch(root + "/robots.txt", 300_000)
    txt = r["body"] if r["status"] == 200 else ""
    out["robots_txt"] = {"status": r["status"], "error": r.get("error"), "blocks_everything": bool(re.search(r"(?im)^user-agent:\s*\*\s*\n(?:\s*(?:#.*)?\n)*\s*disallow:\s*/\s*$", txt)),
                         "sitemaps": re.findall(r"(?im)^sitemap:\s*(\S+)", txt), "first_lines": txt.splitlines()[:25]}
    sm_url = (out["robots_txt"]["sitemaps"] or [root + "/sitemap.xml"])[0]
    s = fetch(sm_url, 1_000_000)
    out["sitemap"] = {"url": sm_url, "status": s["status"], "error": s.get("error"), "url_entries": len(re.findall(r"<loc>", s["body"])) if s["status"] == 200 else None}
    return out


def main(argv):
    args = argv[1:]; outdir = None
    if "--out" in args:
        i = args.index("--out"); outdir = args[i + 1]; args = args[:i] + args[i + 2:]
    if len(args) != 1:
        print(__doc__); return 2
    target = args[0]; is_url = re.match(r"https?://", target, re.I) is not None
    result = {"target": target}
    if is_url:
        r = fetch(target)
        result.update(status=r["status"], final_url=r["final_url"], redirected=r["final_url"].rstrip("/") != target.rstrip("/"),
                      error=r.get("error"), x_robots_tag=r["headers"].get("X-Robots-Tag"))
        html_text = r["body"]
        if r["status"] == 200: result["site"] = site_files(r["final_url"])
    else:
        with open(target, encoding="utf-8", errors="replace") as fh: html_text = fh.read()
        result.update(status="local file", final_url=target)
    if html_text:
        result["facts"] = analyse(html_text, result["final_url"] if is_url else "")
        if re.search(r"(?i)enter using password|password-page|storefront.password", html_text) and result["facts"]["word_count"] < 150:
            result["warning"] = "This looks like a password page, not the real site. Facts below describe the password page only."
    else:
        result["warning"] = "No page content was collected (" + str(result.get("error") or "empty page") + "). Report this; do not guess."
    text = json.dumps(result, indent=2)
    if outdir:
        os.makedirs(outdir, exist_ok=True)
        name = re.sub(r"[^a-z0-9]+", "-", re.sub(r"^https?://", "", target.lower())).strip("-")[:80] or "page"
        with open(os.path.join(outdir, name + ".json"), "w", encoding="utf-8") as fh: fh.write(text)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
