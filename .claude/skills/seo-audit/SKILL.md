---
name: seo-audit
description: Audit a website's SEO from a link, with optional theme code or admin access. Asks what access you have, never changes a site, and writes a plain-language report with every finding labelled.
---

# seo-audit

Audits a website's on-page and technical SEO and writes a **report** a client can read and a developer can act on. First target: a **Shopify** client store, but it works for any platform. It is **report-first**: it never changes a live site, and it works on copies when code or admin access exists.

Explain every step in plain words. The owner is not technical. **Stop at each gate** and wait for an answer.

## Hard rules
- **Never invent** facts, scores, rankings or traffic. Unknown or not checked means "not checked", with the reason.
- **Never ask for, print or store a password, token or key.** The owner connects the site themselves (a browser login, or a key in their own `.env`). If one is pasted into the chat, tell them to change it and do not repeat it.
- **Never change a client's site without written permission.** Even with permission: work on a **copy** of the theme, show every change first, keep a way to undo it, and never publish live.
- Never overwrite the owner's files. Reports go in `seo-audits/<site>/<date>/`.
- You can only report what you actually fetched. Never say you checked a page you did not fetch.

## Step 1: Ask what access they have (the gate)
Ask these five, one short list, "I don't know" allowed (`references/access-prompt.md` has the wording):
1. A **link** to the site (public address or a preview link).
2. Is it **password-protected**?
3. The site's **code** (for Shopify: the theme files).
4. **Admin access** (staff account, collaborator access or a token, connected by the owner, never pasted here).
5. Is the **client's permission** in writing?

Then say which mode applies and what each extra access unlocks:

| Access | Mode | What happens |
|---|---|---|
| Link only (**always offered**) | **Report only** | Audit through the link. Nothing is changed. The report can be used to work on the site separately. |
| Link + code | **Fix preview** | Also shows what can be fixed from our end in the theme, on a **copy**. |
| Link + code + admin | **Fix + admin prep** | Also prepares admin changes (titles, descriptions, alt text, redirects) for approval, with a preview and an undo path. |

Changes of any kind need written permission (question 5). Without it, stay in report-only mode.

**Preview links:** tell the owner a preview link can add the platform's own preview bar, can expire, and may score differently from the live site. A password-protected or expiring link may block the audit; say so rather than guess.

## Step 2: Pick pages
Audit these first: **home, about, one product page, contact**. Ask for the exact links. The blog is handled later with `blog-anywhere`. Add more only if asked.

## Step 3: Collect facts
Create `seo-audits/<site-slug>/<YYYY-MM-DD>/`. For each page run:

`python3 <skill>/scripts/audit_page.py <url-or-file> --out seo-audits/<site>/<date>/pages`

It fetches the page once (no logins, no forms) and records title, meta description, headings, canonical, robots tags, language, viewport, social tags, structured data, images and alt text, links, plus `robots.txt` and the sitemap for the site. If a page cannot be fetched (blocked, password page, error), the output says so; report that, do not work around it. Network access depends on the session's allowed hosts: if the site is blocked, tell the owner (see the environment documentation) rather than guessing.

**Speed:** run `python3 <skill>/scripts/run_lighthouse.py seo-audits/<site>/<date> <url> <url> ...` for the audited pages (needs Node and a Chrome browser; first run downloads Lighthouse, so the session's network must allow package downloads). It writes `lighthouse.json`, which `build_report.py` adds to the report. Say it is one lab test, that scores move between runs, that a preview link can differ from the live site, and that the SEO score is lowered while the site is blocked from search engines. Always run it; if it cannot run, say why, never skip it silently. Google's keyless PageSpeed API is rate-limited and needs a free key; never ask for one in the chat. If speed was not measured, say "not measured".

## Step 4: Judge and label
Read `references/checks.md` for what each check means and `references/platform-notes.md` for the platform. Turn the facts into findings (`findings.json`, format in `references/report-format.md`). Every finding has: page, what was found (quoted from the facts), why it matters in one plain sentence, what to do, severity, and exactly one label:

- **We fix**: can be done from our end in the theme/code (needs code access and permission).
- **Done in the admin**: done in the store/site admin, with the steps written out.
- **Platform limit**: the platform does not allow it, with the best workaround.
- **Client's decision**: needs a business choice or content only the client has.

Platform behaviour you have not confirmed in the platform's own documentation is marked **"to confirm"**. Do not present general knowledge as fact.

## Step 5: Write the report
`python3 <skill>/scripts/build_report.py seo-audits/<site>/<date>/findings.json` writes `report.md` and `report.html` next to it. The report has: a plain-language summary and top recommendations, the access mode used and its limits, the preview-link note if relevant, findings grouped by label, what was not checked, and next steps. Read it back to the owner and fix anything you cannot support from the facts.

## Step 5b: Client summary PDF (when the owner wants one for the client)
Write `client_summary.json` (format in the header of `scripts/build_client_summary.py`) in **plain English for a non-technical client**: what was looked at, the good news, the one big thing, numbered recommendations in order (only items the owner approved), who does what, what was not checked, and the preview-link note. Use only facts from the audit. **Show the text to the owner and wait for approval**, including any item they want removed, then run `python3 <skill>/scripts/build_client_summary.py <that file>` (needs `pip install reportlab`) and send the PDF. Never put it in the repo without the owner's say-so; audit folders hold a client's data and stay local unless the owner decides otherwise.

## Step 6: Fixes (only with code or admin access AND written permission)
Show each proposed change as a before and after, on a **copy** of the theme or as an admin change list. Wait for "go" per batch. Never push to the live theme or publish; the owner does that. Record what changed and how to undo it in `changes.md`.

## Bundled files
`references/access-prompt.md`, `references/checks.md`, `references/platform-notes.md`, `references/report-format.md`, `scripts/audit_page.py`, `scripts/run_lighthouse.py`, `scripts/build_report.py`, `scripts/build_client_summary.py`.
