#!/usr/bin/env python3
"""Turn findings.json into report.md and report.html next to it. Standard library only.

  python3 build_report.py <findings.json>

Refuses a finding that has no valid label or severity, so nothing goes out unlabelled.
"""
import html
import json
import os
import sys

LABELS = ["We fix", "Done in the admin", "Platform limit", "Client's decision"]
LABEL_HELP = {
    "We fix": "Can be fixed from our end in the theme/code (needs code access and written permission; done on a copy first).",
    "Done in the admin": "Done in the site's admin, with the steps below.",
    "Platform limit": "The platform does not allow it directly. A workaround is given.",
    "Client's decision": "Needs a business choice or content only the client has.",
}
SEV = ["High", "Medium", "Low"]
MODES = {"report-only": "Report only. Nothing was or will be changed.",
         "fix-preview": "Link plus code. Fixes are shown on a copy, never on the live site.",
         "fix-admin-prep": "Link, code and admin. Admin changes are prepared for approval, with a preview and an undo path."}


def validate(d):
    errs = []
    for i, f in enumerate(d.get("findings", []), 1):
        if f.get("label") not in LABELS: errs.append(f"Finding {i} ({f.get('check')}): label must be one of {LABELS}")
        if f.get("severity") not in SEV: errs.append(f"Finding {i} ({f.get('check')}): severity must be one of {SEV}")
        for k in ("page", "check", "found", "action"):
            if not f.get(k): errs.append(f"Finding {i}: missing '{k}'")
    if d.get("mode") not in MODES: errs.append(f"mode must be one of {list(MODES)}")
    return errs


def build_md(d):
    L = [f"# SEO audit: {d.get('site', '')}", "", f"Site: {d.get('url', '')}  |  Date: {d.get('date', '')}  |  Platform: {d.get('platform', 'not stated')}", "",
         "## Summary", "", d.get("summary") or "TODO: write the summary.", ""]
    if d.get("recommendations"):
        L += ["## Top recommendations", ""] + [f"{n}. {r}" for n, r in enumerate(d["recommendations"], 1)] + [""]
    a = d.get("access", {})
    L += ["## How this audit was done", "", f"**Mode:** {MODES.get(d.get('mode'), d.get('mode'))}", "",
          "Access: " + ", ".join(f"{k.replace('_', ' ')} {'yes' if v else 'no'}" for k, v in a.items()), ""]
    if d.get("preview_link"):
        L += ["> **Preview link:** this audit used a preview link. It can add the platform's own preview bar and can expire, so results (especially speed) may differ from the live site.", ""]
    L += ["Pages audited:"] + [f"- {p}" for p in d.get("pages_audited", [])] + [""]
    n = len(d.get("findings", []))
    L += [f"## Findings ({n})", ""]
    for lab in LABELS:
        items = [f for f in d.get("findings", []) if f["label"] == lab]
        if not items: continue
        L += [f"### {lab} ({len(items)})", "", f"_{LABEL_HELP[lab]}_", ""]
        for f in sorted(items, key=lambda x: SEV.index(x["severity"])):
            L += [f"**[{f['severity']}] {f['check']}** on {f['page']}" + (" _(platform behaviour to confirm)_" if f.get("to_confirm") else ""),
                  f"- Found: {f['found']}", f"- Why it matters: {f.get('why', '')}", f"- What to do: {f['action']}"]
            if f.get("workaround"): L.append(f"- Workaround: {f['workaround']}")
            for s in f.get("steps", []): L.append(f"  - {s}")
            L.append("")
    L += ["## Not checked", ""] + ([f"- {x}" for x in d.get("not_checked", [])] or ["- Nothing listed."]) + [""]
    L += ["## Next steps", "", "1. The client reviews the findings marked Client's decision.", "2. Nothing is changed on the site without written permission.", "3. Fixes are prepared on a copy and shown before any change.", ""]
    return "\n".join(L)


def build_html(md):
    out, in_ul = [], False
    for line in md.split("\n"):
        e = html.escape(line)
        e = __import__("re").sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", e)
        e = __import__("re").sub(r"(?<![\w])_(.+?)_(?![\w])", r"<em>\1</em>", e)
        if line.startswith("- ") or line.startswith("  - "):
            if not in_ul: out.append("<ul>"); in_ul = True
            out.append(f"<li>{e.strip()[2:]}</li>"); continue
        if in_ul: out.append("</ul>"); in_ul = False
        if line.startswith("### "): out.append(f"<h3>{e[4:]}</h3>")
        elif line.startswith("## "): out.append(f"<h2>{e[3:]}</h2>")
        elif line.startswith("# "): out.append(f"<h1>{e[2:]}</h1>")
        elif line.startswith("&gt;") or line.startswith("> "): out.append(f"<blockquote>{e[4:] if e.startswith('&gt;') else e}</blockquote>")
        elif line.strip(): out.append(f"<p>{e}</p>")
    if in_ul: out.append("</ul>")
    css = "body{font-family:system-ui,sans-serif;max-width:46rem;margin:2rem auto;padding:0 1rem;line-height:1.55;color:#1c1c1c}blockquote{background:#fff7e0;margin:1rem 0;padding:.6rem 1rem;border-left:4px solid #e0a800}h3{margin-top:2rem}"
    return f"<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>SEO audit report</title><style>{css}</style>" + "\n".join(out)


def main(argv):
    if len(argv) != 2:
        print(__doc__); return 2
    with open(argv[1], encoding="utf-8") as fh: d = json.load(fh)
    errs = validate(d)
    if errs:
        print("Cannot build the report:\n" + "\n".join("- " + e for e in errs)); return 1
    md = build_md(d); folder = os.path.dirname(os.path.abspath(argv[1]))
    for name, text in (("report.md", md), ("report.html", build_html(md))):
        with open(os.path.join(folder, name), "w", encoding="utf-8", newline="\n") as fh: fh.write(text + "\n")
    print(f"Wrote {folder}/report.md and report.html ({len(d.get('findings', []))} findings)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
