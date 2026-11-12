#!/usr/bin/env python3
"""Create the workspace for one site. Standard library only.

  python3 new_site.py <site-slug> [--dir blog-sites] [--name "Display Name"] [--platform shopify] [--url https://example.com]

Creates <dir>/<site-slug>/ with site.json, references/ (voice, tone, humor, opinions, stats, stories),
site-pages.csv (real pages for internal links), keywords.csv, published.json, posts/, images-incoming/.
Never overwrites an existing site folder.
"""
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(HERE, "..", "references", "reference-templates")
SLUG = re.compile(r"^[a-z0-9][a-z0-9-]{0,60}$")


def arg(args, flag, default=""):
    if flag in args:
        i = args.index(flag)
        v = args[i + 1] if i + 1 < len(args) else default
        del args[i:i + 2]
        return v
    return default


def main(argv):
    args = argv[1:]
    base = arg(args, "--dir", "blog-sites")
    name = arg(args, "--name")
    platform = arg(args, "--platform", "other").lower()
    url = arg(args, "--url").rstrip("/")
    if not args:
        print(__doc__)
        return 2
    slug = args[0]
    if not SLUG.match(slug):
        print("ERROR: site-slug must be lowercase letters, digits and dashes, for example my-shop")
        return 1
    root = os.path.join(base, slug)
    if os.path.exists(root):
        print(f"ERROR: {root} already exists. Not overwriting. Pick another name or use the existing folder.")
        return 1
    for d in ("references", "posts", "images-incoming"):
        os.makedirs(os.path.join(root, d))
    open(os.path.join(root, "images-incoming", ".gitkeep"), "w").close()
    for f in sorted(os.listdir(TEMPLATES)):
        if f.endswith(".md"):
            shutil.copy2(os.path.join(TEMPLATES, f), os.path.join(root, "references", f))
    site = {"slug": slug, "name": name or slug, "url": url, "platform": platform,
            "author": "", "audience": "", "goal": "", "humor_level": "unknown",
            "image_source_default": "ask", "image_rules": "", "content_rules": "",
            "notes": "Fill from the site profile questions. Unknown items stay empty (never guessed)."}
    with open(os.path.join(root, "site.json"), "w", encoding="utf-8") as fh:
        json.dump(site, fh, indent=2)
    with open(os.path.join(root, "site-pages.csv"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("title,url,type,notes\n")
    with open(os.path.join(root, "keywords.csv"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("keyword,volume,difficulty,intent,status,notes\n")
    with open(os.path.join(root, "published.json"), "w", encoding="utf-8") as fh:
        fh.write("[]\n")
    with open(os.path.join(root, "README.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(f"# {name or slug}: blog workspace\n\n"
                 "- `site.json`: facts about the site (platform, audience, rules).\n"
                 "- `references/`: the voice files. Posts are written from these.\n"
                 "- `site-pages.csv`: the site's real pages, for internal links.\n"
                 "- `keywords.csv`: topics and keywords.\n"
                 "- `published.json`: posts already made, so none repeats.\n"
                 "- `posts/`: one folder per post (post.json and its package).\n"
                 "- `images-incoming/`: the owner's own photos.\n")
    print(json.dumps({"site_folder": root, "platform": platform,
                      "created": sorted(os.listdir(root)), "references": sorted(os.listdir(os.path.join(root, "references")))}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
