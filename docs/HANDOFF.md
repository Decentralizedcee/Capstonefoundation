# Handoff notes (read this first in a fresh session)

Branch: `claude/seo-video-guideline-0fl7qh`. Everything below is committed and pushed. Updated 12 Nov 2026.

## About the owner
Non-technical, works in Claude Code on their own computer (sometimes the regular chat). Wants plain-language, beginner-friendly output, short guides (PDF, interactive), and **never invented facts**. Never pastes passwords or keys into the chat (they go in `.env` or a browser login). Prefers Render for hosting.

**Capstone-only rules** (hopeful and openly Christian voice, NIV, the sparkle style, humor off, no Unsplash people-photos in work pages, and so on) live in `docs/capstone/` and apply **only** to the Capstone project. They must **never** be copied into `blog-anywhere`, `site-setup`, `blog` or any other general-purpose skill. Those skills are for any user.

## What exists (all in this repo)
| Item | Where | Status |
|---|---|---|
| SEO method from Jono Catliff's video, reconstructed | `docs/seo-with-claude-guideline.md`, `docs/seo-kit/` | Done |
| Step-by-step PDF guide (15 pages) | `docs/seo-step-by-step-guide.pdf` | Done |
| `blog` skill (static-site projects, Astro or Next.js) | `.claude/skills/blog/` | Built, **not run on a real site yet** |
| `service-page` skill (local service sites) | `.claude/skills/service-page/` | Built, not run |
| `site-setup` skill (Claude Code): folder-first, intake, CLAUDE.md, verify script, design direction, build prompt | `.claude/skills/site-setup/` | Built; verify script tested |
| `site-setup-chat` (regular chat edition, ZIP-based) | `chat-edition/site-setup-chat/` | Built; scripts tested; not run in claude.ai |
| `blog-anywhere` (any platform; copy-paste package + preview page) | `.claude/skills/blog-anywhere/` | Built; scripts and preview tested; skill not run end to end |
| Interactive user guide for site-setup (7 pages) | `docs/site-setup-user-guide.pdf` | Done |
| Capstone Foundation project files and start prompt | `docs/capstone/` | Done (owner is running it in their own folder) |
| Audit-skill requirements | `docs/seo-audit-skill-notes.md` | **Not built yet** |

## Pending edits to `blog-anywhere` (requested 12 Nov, not yet made)
1. **Per-post voice picker (voice-neutral).** The skill is for **any user**, so every user must be free to **pick their own voice type**. Each post, ask how this post should sound and offer a menu **as examples, not rules** (for example: friendly and conversational; professional and authoritative; warm and inspirational; calm and reassuring; bold and direct; playful and witty; educational and clear; premium and refined; **my own voice from my writing samples**; or **describe it yourself**), plus humor level, "I" or "we", angle and audience. Use the choice for that post. **No default, preset or example may come from the Capstone owner's rules.** Keep example wording neutral. The user's **own** site rules (their privacy, legal and off-limits topics from their own site profile) still apply, never anyone else's. Offer to save a choice as a named variant (and update the voice reference files only after the user approves).
2. **Keywords.** Ask for keywords before writing: if the owner supplied a list (`keywords.csv`), let them choose from it; if they have a specific keyword, take that one; if neither, ask. Flag unverified data. Then start.
3. **Images.** Ask which images the owner wants for this post (their own photos, stock, specific files, how many, where).
4. **Owner's own content.** Ask if they have their own content. Modes: write for me / build on my notes and add to them / **use mine exactly** (format, SEO fields and checks only; do not change their wording without permission; suggest, do not edit).
5. **Draft publishing when connected.** Ask whether the site is connected to Claude (WordPress, Wix, Shopify or another builder, through whatever connector tools exist in the session). If yes: create the post as a **draft only**, after the owner approves exactly what will be sent. **Never publish live.** If not connected: give the preview package to copy and paste.

## Next to build: SEO audit skill
See `docs/seo-audit-skill-notes.md`. First target is a Shopify client store; the owner will send a preview link after the skill exists. Lighthouse 13.6 was run successfully in the Claude Code environment (needs Node and Chrome). Google's keyless PageSpeed API was rate-limited.

## Rules that never change
Never invent facts. Never ask for, print or store keys or passwords. Never overwrite existing files or replace an existing `CLAUDE.md`. Never publish live or change a client's site without written permission (work on copies, preview first). Stop at gates and wait for "go".
