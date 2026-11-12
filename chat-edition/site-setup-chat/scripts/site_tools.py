#!/usr/bin/env python3
"""Helpers for the site-setup-chat skill. Standard library only.

Usage:
  python3 site_tools.py starter <config.json> <out_dir>
      Builds the starter project (folders, .gitignore, .env, .env.example, README)
      and zips it to <out_dir>/<project_name>-starter.zip. Prints a JSON summary.

  python3 site_tools.py pack <src_dir> <zip_path> <root_name>
      Zips the contents of <src_dir> under a single top-level folder <root_name>/.

Config keys for `starter` (all optional except framework):
  project_name   lowercase letters, digits and dashes (default "my-website")
  framework      "astro" or "nextjs"
  images_dir     folder for the owner's own photos (default "images")
  blog_dir       blog folder (default: astro "src/content/blog", nextjs "content/blog")
  service_pages  true/false (default false)
  services_dir   service pages folder (default: astro "src/content/services", nextjs "content/services")
  use_unsplash   true/false (default false) -> adds an empty UNSPLASH_ACCESS_KEY line
  indexable      true/false (default true)  -> value of the public indexable flag
"""
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile

SLUG = re.compile(r"^[a-z0-9][a-z0-9-]{0,60}$")


def fail(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def safe_rel(path, label):
    if not isinstance(path, str) or not path or path.startswith(("/", "\\")) or ".." in path.replace("\\", "/").split("/") or ":" in path:
        fail(f"{label} must be a simple relative folder path (got {path!r})")
    return path.strip("/")


def starter(cfg_path, out_dir):
    with open(cfg_path, encoding="utf-8") as fh:
        cfg = json.load(fh)
    fw = cfg.get("framework")
    if fw not in ("astro", "nextjs"):
        fail('framework must be "astro" or "nextjs"')
    name = cfg.get("project_name", "my-website")
    if not SLUG.match(name):
        fail("project_name must be lowercase letters, digits and dashes, for example my-business-site")
    images = safe_rel(cfg.get("images_dir", "images"), "images_dir")
    blog = safe_rel(cfg.get("blog_dir") or ("src/content/blog" if fw == "astro" else "content/blog"), "blog_dir")
    services_on = bool(cfg.get("service_pages", False))
    services = safe_rel(cfg.get("services_dir") or ("src/content/services" if fw == "astro" else "content/services"), "services_dir")
    unsplash = bool(cfg.get("use_unsplash", False))
    indexable = "true" if cfg.get("indexable", True) else "false"

    dirs = ["docs", "references", "public", "scripts", images, blog]
    if services_on:
        dirs.append(services)
    if fw == "astro":
        dirs += ["src/assets/images", "src/components", "src/layouts", "src/pages", "src/styles", "src/data"]
        out_folder, cache_folder = "dist", ".astro"
        prefix = "PUBLIC_"
    else:
        dirs += ["app"]
        out_folder, cache_folder = "out", ".next"
        prefix = "NEXT_PUBLIC_"

    env_lines = [
        "# Private notes file. Type your own keys after the = sign.",
        "# No spaces and no quotes. Never share this file or paste it into a chat.",
        f"{prefix}SITE_URL=",
        f"{prefix}INDEXABLE={indexable}",
    ]
    if unsplash:
        env_lines.append("UNSPLASH_ACCESS_KEY=")
    env_text = "\n".join(env_lines) + "\n"

    gitignore = "\n".join([
        "# Private keys (never upload)", ".env", "",
        "# Installed packages and build output", "node_modules/", f"{out_folder}/", f"{cache_folder}/", "",
        "# Your own photos stay on your computer (the folder itself is kept)",
        f"{images}/*", f"!{images}/.gitkeep", "",
        "# Computer clutter", ".DS_Store", "",
    ])
    readme = (
        f"# {name}\n\n"
        "Starter folder created by the site-setup-chat skill.\n\n"
        "- `.env` is your private notes file (keys go here, never shared).\n"
        f"- `{images}/` is where you put your own photos.\n"
        "- `docs/` and `references/` get filled in as you go.\n\n"
        "This README is completed when the website is built.\n"
    )

    os.makedirs(out_dir, exist_ok=True)
    work = tempfile.mkdtemp()
    root = os.path.join(work, name)
    os.makedirs(root)
    made = []
    for d in dirs:
        p = os.path.join(root, d)
        os.makedirs(p, exist_ok=True)
        open(os.path.join(p, ".gitkeep"), "w").close()
        made.append(d + "/")
    files = {".gitignore": gitignore, ".env": env_text, ".env.example": env_text, "README.md": readme}
    for fn, text in files.items():
        with open(os.path.join(root, fn), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)

    zip_path = os.path.join(out_dir, f"{name}-starter.zip")
    pack_dir(root, zip_path, name)
    # also leave the unzipped folder next to the zip, so it can be inspected or verified
    dest = os.path.join(out_dir, name)
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(root, dest)
    shutil.rmtree(work)
    print(json.dumps({"zip": zip_path, "folder": dest, "framework": fw, "folders": sorted(made),
                      "files": sorted(files), "env_keys": [l.split("=")[0] for l in env_lines if "=" in l and not l.startswith("#")]},
                     indent=2))


def pack_dir(src, zip_path, root_name):
    if not os.path.isdir(src):
        fail(f"not a folder: {src}")
    if not SLUG.match(root_name.lstrip("_")) and not root_name.startswith("_"):
        fail("root_name must be a simple folder name")
    entries = []
    for d, subdirs, fs in os.walk(src):
        subdirs.sort()
        for f in sorted(fs):
            full = os.path.join(d, f)
            entries.append((full, os.path.join(root_name, os.path.relpath(full, src)).replace(os.sep, "/")))
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for full, arc in entries:
            z.write(full, arc)
    return len(entries)


def main(argv):
    if len(argv) >= 4 and argv[1] == "starter":
        starter(argv[2], argv[3])
    elif len(argv) >= 5 and argv[1] == "pack":
        n = pack_dir(argv[2], argv[3], argv[4])
        print(json.dumps({"zip": argv[3], "files": n, "root": argv[4]}))
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv)
