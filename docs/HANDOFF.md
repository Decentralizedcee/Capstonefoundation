# Handoff notes (read this first in a fresh session)

Branch: `claude/seo-video-guideline-0fl7qh`. Everything below is committed and pushed. Updated 12 Nov 2026.

## About the owner
Non-technical, works in Claude Code on their own computer (sometimes the regular chat). Wants plain-language, beginner-friendly output, short guides (PDF, interactive), and **never invented facts**. Never pastes passwords or keys into the chat (they go in `.env` or a browser login). Prefers Render for hosting.

**Capstone-only rules** (hopeful and openly Christian voice, NIV, the sparkle style, humor off, no Unsplash people-photos in work pages, and so on) live in `docs/capstone/` and apply **only** to the Capstone project. They must **never** be copied into `blog-anywhere`, `site-setup`, `blog` or any other general-purpose skill. Those skills are for any user.

## ORDER OF WORK
1. ~~Make the five pending edits to `blog-anywhere`.~~ **DONE 12 Nov 2026** (see below). Not yet run end to end in a real session.
2. ~~Build the SEO site audit skill (`seo-audit`).~~ **DONE 12 Nov 2026** (`.claude/skills/seo-audit/`, zip `dist/seo-audit.zip`). Update 12 Nov: first real run done on the client's Shopify preview link (report only; audit files kept LOCAL in `seo-audits/`, not committed, because they hold client data). Added `run_lighthouse.py` (works: Node + Chromium) and `build_client_summary.py` (plain-English client PDF via reportlab; owner approves the text first). Needed the session's network to allow the preview host.
3. ~~First audit on the Shopify preview~~ done (test run). **Next:** when the client's site is live, run `seo-audit` again on the live address (owner will ask). Open items from the test: confirm noindex/robots.txt are gone live, sitemap exists, 'Elixer/Elixir' spelling, headings, alt text, home page speed (LCP 8.9 s on preview). Reviews finding stays in the internal report only.

When a step is finished, update this note.

## What exists (all in this repo)
| Item | Where | Status |
|---|---|---|
| SEO method from Jono Catliff's video, reconstructed | `docs/seo-with-claude-guideline.md`, `docs/seo-kit/` | Done |
| Step-by-step PDF guide (15 pages) | `docs/seo-step-by-step-guide.pdf` | Done |
| `blog` skill (static-site projects, Astro or Next.js) | `.claude/skills/blog/` | Built, **not run on a real site yet** |
| `service-page` skill (local service sites) | `.claude/skills/service-page/` | Built, not run |
| `site-setup` skill (Claude Code): folder-first, intake, CLAUDE.md, verify script, design direction, build prompt | `.claude/skills/site-setup/` | Built; verify script tested |
| `site-setup-chat` (regular chat edition, ZIP-based) | `chat-edition/site-setup-chat/` | Built; scripts tested; not run in claude.ai |
| `blog-anywhere` (any platform; per-post brief, copy-paste package + preview page, draft if connected) | `.claude/skills/blog-anywhere/` | Built and edited 12 Nov; scripts tested; skill not run end to end. Zip: `dist/blog-anywhere.zip` |
| Interactive user guide for site-setup (7 pages) | `docs/site-setup-user-guide.pdf` | Done |
| Interactive user guide for blog-anywhere (7 pages: install, set up, per-post questions, package, publish, commands and fixes) | `docs/blog-anywhere-user-guide.pdf` | Done |
| Capstone Foundation project files and start prompt | `docs/capstone/` | Done (owner is running it in their own folder) |
| `seo-audit` (access prompt, 3 modes, labelled report) | `.claude/skills/seo-audit/` | Built 12 Nov; `audit_page.py` and `build_report.py` tested locally; not run on a real site |

## `blog-anywhere` edits (done 12 Nov 2026)
New file `references/post-brief.md` holds the questions asked before every post; `SKILL.md` Step 3 starts with it. Skill is voice-neutral (checked: no Capstone terms anywhere in the skill folder).
1. **Per-post voice picker:** menu of examples (friendly, professional, inspirational, calm, bold, playful, educational, premium, my own voice from samples, describe it yourself), plus humor, I/we, angle, audience. No defaults. Named variants saved only if the user approves. The old voice builder now applies only to the "my own voice" choice.
2. **Keywords:** choose from `keywords.csv`, give one, or be asked; unverified data flagged.
3. **Images:** asked per post (own photos, stock, files, how many, where).
4. **Own content:** three modes (write / build on notes / use mine exactly). `build_package.py` reads `brief` in `post.json`; in `exact` mode it compares the body with `brief.original_file` word for word and FAILs on any change (tested).
5. **Connected site:** ask which connector tools exist; if one can make drafts, show exactly what will be sent, get a yes, create a **draft only**, never live. Otherwise the copy-paste package.
Script changes (all tested): `build_package.py` (brief + exact check), `voice_tools.py check` (friendly note if no saved numbers), `new_site.py` (`connection` field in `site.json`). Skill description is 180 characters.

## seo-audit skill (built; requirements it follows)
See `docs/seo-audit-skill-notes.md` for the full requirements: the access prompt (link, password protection, code, admin access, written permission), the **link-only mode that is always offered** (report only), the fix/recommend labels, safety rules and the pages to audit first (home, about, a product page, contact). First target is a Shopify client store; the owner will send a preview link after the skill exists. Lighthouse 13.6 was run successfully in the Claude Code environment (needs Node and Chrome). Google's keyless PageSpeed API was rate-limited.

## Rules that never change
Never invent facts. Never ask for, print or store keys or passwords. Never overwrite existing files or replace an existing `CLAUDE.md`. Never publish live or change a client's site without written permission (work on copies, preview first). Stop at gates and wait for "go".
