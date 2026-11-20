#!/usr/bin/env python3
"""Run Lighthouse (a free speed and quality test) on pages and save a short summary. Read-only.

  python3 run_lighthouse.py <out-dir> <url> [<url> ...]

Needs Node (npx) and a Chrome/Chromium browser. Uses CHROME_PATH if set, else /opt/pw-browsers/chromium*/ if present.
Writes <out-dir>/lighthouse.json with, for each page: scores out of 100 (performance, accessibility, best practices, SEO)
and key timings. Each page is one 'lab test' on a mobile profile: scores move between runs, and a preview link can differ
from the live site. If it cannot run, it says why; never invent numbers.
"""
import glob, json, os, re, subprocess, sys, tempfile

METRICS = {"first-contentful-paint": "First Contentful Paint", "largest-contentful-paint": "Largest Contentful Paint",
           "total-blocking-time": "Total Blocking Time", "cumulative-layout-shift": "Cumulative Layout Shift", "speed-index": "Speed Index"}


def find_chrome():
    if os.environ.get("CHROME_PATH"): return os.environ["CHROME_PATH"]
    for pat in ("/opt/pw-browsers/chromium-*/chrome-linux*/chrome", "/opt/pw-browsers/chromium/chrome"):
        hits = sorted(glob.glob(pat))
        if hits: return hits[-1]
    return None


def run(url, chrome):
    out = tempfile.mktemp(suffix=".json")
    env = dict(os.environ)
    if chrome: env["CHROME_PATH"] = chrome
    cmd = ["npx", "-y", "lighthouse@12", url, "--output=json", f"--output-path={out}", "--quiet",
           "--only-categories=performance,accessibility,best-practices,seo", "--chrome-flags=--headless --no-sandbox"]
    try:
        p = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=240)
    except Exception as e:
        return {"url": url, "error": f"{type(e).__name__}: {e}"}
    if not os.path.isfile(out):
        return {"url": url, "error": "Lighthouse did not produce a result: " + (p.stderr or p.stdout)[-300:]}
    d = json.load(open(out)); os.remove(out)
    if d.get("runtimeError"): return {"url": url, "error": d["runtimeError"].get("message", "runtime error")}
    cats = {k: round((v.get("score") or 0) * 100) for k, v in d["categories"].items()}
    met = {label: d["audits"][k].get("displayValue", "n/a") for k, label in METRICS.items() if k in d["audits"]}
    return {"url": d.get("finalDisplayedUrl", url), "scores": cats, "metrics": met, "lighthouse_version": d.get("lighthouseVersion")}


def main(argv):
    if len(argv) < 3:
        print(__doc__); return 2
    outdir, urls = argv[1], argv[2:]
    os.makedirs(outdir, exist_ok=True); chrome = find_chrome()
    results = [run(u, chrome) for u in urls]
    with open(os.path.join(outdir, "lighthouse.json"), "w") as fh: json.dump(results, fh, indent=2)
    for r in results:
        print(r["url"], r.get("error") or r["scores"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
