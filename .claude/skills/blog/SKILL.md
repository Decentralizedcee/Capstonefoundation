---
name: blog
description: Generate one fully SEO-optimized blog post (or "story") for any business or organisation, in the owner's own voice and within the project's content rules. Picks an unused keyword from keywords.csv (or uses the one given), builds a keyword cluster, researches the top 3 Google results and matches their averaged format, adds images from Unsplash or the owner's own images folder (chosen per run), applies the on-page SEO checklist, and publishes through the site's standard static template, reading folders, format and framework from the Stack adapter in CLAUDE.md. Use when the user types "blog", asks for a new blog post or story, the next post, a post for a keyword, or says "blog images=local" / "blog images=unsplash".
---

# blog

Creates **one** SEO post per run for a statically generated website. It follows the method from Jono Catliff's "Claude Code SEO" video: real keyword data, a keyword cluster, the averaged format of the top 3 Google results, the owner's voice, an on-page checklist, and the same technical template every time.

The skill is **stack-neutral**. It works on Next.js, Astro or any static site, as long as the project's `CLAUDE.md` describes it in a **Stack adapter** section (see below).

## Invocation

| What the user types | Meaning |
|---|---|
| `blog` | Next unused keyword, image mode from `CLAUDE.md` (or ask) |
| `blog <keyword>` | Use this exact keyword (must still be unused) |
| `blog images=unsplash` / `blog use unsplash` | Pull images from the Unsplash API |
| `blog images=local` / `blog use my images` | Choose from the owner's local images folder |
| `blog images=none` | No images; insert marked placeholders |
| `blog images=mixed` | Own images first, Unsplash to fill gaps |

Free-text instructions such as "use the photos I uploaded" mean the same. Details: `references/image-sources.md` (in this skill's folder).

## Terms

- **Project files** are in the website project root: `CLAUDE.md`, `.env`, `keywords.csv`, `references/` (voice, tone, humor, opinions, stats, stories), `docs/`, the content folders and the local images folder.
- **Bundled files** are in this skill's folder: `references/image-sources.md`, `references/on-page-seo-checklist.md`, `scripts/optimize-image.mjs`.

## Stack adapter

Read the `## Stack adapter` section of the project `CLAUDE.md`. It tells you where things live. Use **its values** for every path and command below. If a key is missing, use the default.

| Key | Meaning | Default (Next.js layout) |
|---|---|---|
| `framework` | `nextjs`, `astro`, ... | `nextjs` |
| `build_command` / `output_dir` | how to build, where output goes | `npm run build` / `out` |
| `blog_collection` | folder for posts | `content/blog` |
| `blog_format` | `md` or `mdx` | `md` |
| `blog_route` / `blog_index` | public URL pattern and index | `/blog/<slug>` / `/blog` |
| `service_pages` | where service pages live, or `NOT USED` | `content/services` |
| `published_log` | JSON list of used keywords | `content/published.json` |
| `new_posts_as` | `draft` or `published` | `published` |
| `local_images_dir` | where the owner drops photos | `images` |
| `image_pipeline` | project command that processes local images | the bundled `scripts/optimize-image.mjs` |
| `image_registry` | file that records every image | none |
| `processed_images_dir` | where processed images go | `public/images/blog/<slug>` |
| `image_source` | default image mode | `ask` |
| `unsplash_app_name` | name used in Unsplash credit links | ask |

**Project rules win.** `CLAUDE.md` may add content rules (tone, privacy, faith, no-go topics, image restrictions, Scripture handling). Follow them over any default in this skill.

## Step 0: Project and image pre-flight (before any other work)

1. Confirm this is a site project: `CLAUDE.md` (with a Stack adapter or a recognisable default layout), `keywords.csv`, and the blog folder or a blog template exist. If something core is missing, **stop** and say which setup step is missing. Do not improvise a site.
2. Resolve the **image mode** and run its pre-flight, exactly as `references/image-sources.md` sections 1 and 2 say:
   - `unsplash`: confirm `UNSPLASH_ACCESS_KEY` is in `.env` (never print it) and `.env` is git-ignored. If missing, **stop** and tell the user how to add it themselves; offer `local` or `none`.
   - `local`: confirm the `local_images_dir` exists and has images. If not, stop and say so.
3. Never ask the user to paste a key into the chat.

## Step 1: Cadence check

Read the publishing ramp in `CLAUDE.md` and the dates in `published_log`. If today's count already meets the stage limit, **stop** and tell the user. Default is **1 post per run**. Ramp: day 1 → 1, day 2 → 1, day 3 → 2, day 5 → 3, day 8 → 4, then keep it reasonable. Never exceed the limit without the user saying so.

## Step 2: Pick the keyword

- If the user gave a keyword, use it if it is not in `published_log`.
- Otherwise take the next qualifying row in `keywords.csv` not in `published_log`, preferring: difficulty ≤ 30, volume ≥ 100, informational intent, and a searcher who could become a customer, donor or member.
- **If volume or difficulty are blank** (unverified data), say so plainly, show the keyword, and ask the user to approve it or provide Semrush numbers. Do not pretend the data exists.
- Skip other organisations' brand names, off-topic queries, and anything `CLAUDE.md` rules out.
- If a **stub** for this keyword or story title already exists in the blog folder (front matter only), plan to **fill that file**, not create a duplicate.
- Show the keyword and why you chose it. If nothing qualifies, say so and stop.

## Step 3: Keyword cluster

Build **5 to 10 related terms** (from `keywords.csv` where possible: same stem, questions, long-tail variants; supplement with close variations only if needed). Mark which become H2/H3 headings, which are FAQ questions, and which are used in the body. The post ranks for the whole cluster, not just the primary keyword.

## Step 4: Research the top 3 results

Search Google (web search) for the primary keyword. Take the **top 3 organic results**, skipping Reddit, Quora, forums, video and big directories. For each, record: word count, H2 count, H3 count, image count, FAQ presence, topics covered, format (guide, list, how-to), and how the keyword is used. Then:

- Compute the **averages**: word count, H2s, images. These are the targets.
- List topics all three cover (must include) and topics none cover (your angle).
- Show this as a short table before writing.
- Use the competitors for **structure only**. Never copy their wording or facts.

## Step 5: Read the voice files and the project rules

Read **every** file in the project `references/` (voice, tone, humor, opinions, stats, stories) and the content rules in `CLAUDE.md`. Use only real stats and stories from them. If a useful stat, story, opinion or quotation is missing, write `TODO(owner): <what is needed>` in the draft. **Never invent** numbers, quotes, people, results, anecdotes or (where relevant) Scripture or legal/medical claims. A fact from outside the project (a statistic, a date, a verse) needs a named, checkable source the owner can verify, otherwise mark it `TODO(owner): verify`.

## Step 6: Write the post

To the averaged targets, in the owner's voice and tone:

- **Hook in the first 50 words**, matching the brand's tone in `humor.md` and `tone.md`:
  - If the brand uses humor: a joke, self-aware aside or vivid image.
  - If humor is **off** (for example a charity, healthcare or any sensitive topic): open with an honest human moment, a direct reader question, or a clear promise of what the reader will learn. No jokes.
- Primary keyword in the H1 and in the first 100 words; cluster terms placed naturally; no stuffing.
- Answer the query directly and early, then go deeper. Be specific and practical, only where the facts are known.
- Include a clear opinion or recommendation where the owner has one (`opinions.md`).
- End with a call to action that fits the site (donate, volunteer, contact, book, buy) and link to the most relevant page.
- **No generic AI openings** ("In today's fast-paced world", "In this comprehensive guide", "Delve into").
- Respect any privacy and faith rules in `CLAUDE.md` (for example no amounts, no children's surnames, Scripture only as allowed).

## Step 7: Images

Follow `references/image-sources.md` for the chosen mode and **the project's image rules in `CLAUDE.md`** (for example "Unsplash only for scenes with no people"). Summary:

- `unsplash`: search, pick, **hotlink** the API's URLs with size parameters, send the download ping, add visible attribution with UTM links, store the credit. Show the user the chosen photos in the report.
- `local`: look at the images in `local_images_dir`, pick the ones that fit and are unused, run the project's `image_pipeline` (or the bundled optimizer if none), write honest alt text, record in `image_registry` if defined, never touch the originals.
- `none`: insert marked placeholders.
- `mixed`: local first, Unsplash only for gaps.

Match the **image count** to the competitor average within reason, with one hero image and the rest lazy-loaded. Every image gets `alt`, `width` and `height`.

## Step 8: On-page checklist

Use the project's `docs/on-page-seo-checklist.md` if present, otherwise the bundled `references/on-page-seo-checklist.md`. Apply every applicable item (mark service-page items N/A when the site has no service pages): exactly one H1, meta title ≤ 60 and description ≤ 160, 3 to 5 internal links (to real, existing pages), 2 to 3 external links to reputable sources, 4 to 8 FAQ questions with FAQPage JSON-LD, Article and BreadcrumbList JSON-LD, Open Graph and Twitter tags, canonical URL, clean slug, alt text.

**Keep the voice intact.** If a checklist item would damage the post, flag it in the report instead of forcing it.

## Step 9: Publish through the standard template

Save to `blog_collection` in `blog_format`, using the project's **existing frontmatter schema** (read an earlier post or the collection schema; do not invent fields), so it renders through the same static template as every other post. Do not alter the template's technical SEO per post.

- Set the publish state from `new_posts_as`. When it is `draft`, write `draft: true`. **Never flip a post to published yourself.**
- Make sure the blog index, sitemap and RSS will pick the post up when it is published (framework integrations normally do this; do not hand-edit generated files).
- Add links **to** the new post from 2 to 3 relevant existing posts or pages where natural, but only edit pages the project lets you edit (not fixed-copy pages).

## Step 10: Bookkeeping

Append to `published_log`: `{ "keyword": ..., "slug": ..., "type": "blog", "date": ..., "status": "draft|published" }`. Never reuse a keyword.

## Step 11: Verify

Run `build_command` and fix errors (the site must stay static). Then print the **audit report**:

```
PAGE: <file>   TYPE: blog   PRIMARY KEYWORD: <kw>
PASSED: n/90   FAILED: n   N/A: n
FAILED ITEMS: #<n> <item> -> <what is wrong> -> <fix>
VOICE CHECK: pass | fail (hook fits the tone? no generic AI phrasing? only true stats, stories and quotations? project rules respected?)
```

Fix failures and re-run the audit. Check that the page's text is in the built HTML (static), not only produced by JavaScript.

## Step 12: Report

Give the user: the keyword and why; the cluster; targets vs actuals (words, H2s, images); the image mode used and each image (source, description, link); every `TODO(owner)`; the file path and draft/published state; and cadence status ("posts today: n of limit"). **Do not deploy, push or commit unless the user asks.** If the site is still `noindex` (a temporary address), say that indexing requests wait until the real domain is live.

## Hard rules

- One keyword = one post. Never reuse a keyword.
- Never fabricate stats, stories, quotes, people, results, anecdotes, Scripture, prices, locations or what an image shows.
- Never print, log, commit or paste any API key. Never use a `NEXT_PUBLIC_` or `PUBLIC_` prefix for a secret.
- Unsplash images are hotlinked with attribution and a download ping. Never self-host them.
- Own images: never modify the originals.
- Never bulk-publish. Respect the cadence ramp.
- Project content rules in `CLAUDE.md` override this skill's defaults.
- Content quality beats checklist compliance.
