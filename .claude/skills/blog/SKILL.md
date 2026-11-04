---
name: blog
description: Generate one fully SEO-optimized blog post for any business, in the owner's own voice. Picks an unused keyword from keywords.csv (or uses the one given), builds a keyword cluster, researches the top 3 Google results and matches their averaged format, adds images from Unsplash or from the owner's own images folder (chosen per run), applies the on-page SEO checklist, and publishes through the site's standard static template. Use when the user types "blog", asks for a new blog post, the next post, a post for a keyword, or says "blog images=local" / "blog images=unsplash".
---

# blog

Creates **one** SEO blog post per run for a statically generated website (Next.js static export, hosted on Render). It follows the method from Jono Catliff's "Claude Code SEO" video: real keyword data, a keyword cluster, the averaged format of the top 3 Google results, the owner's voice, an on-page checklist, and the same technical template every time.

## Invocation

| What the user types | Meaning |
|---|---|
| `blog` | Next unused keyword, image mode from `CLAUDE.md` (or ask) |
| `blog <keyword>` | Use this exact keyword (must still be unused) |
| `blog images=unsplash` / `blog use unsplash` | Pull images from the Unsplash API |
| `blog images=local` / `blog use my images` | Choose from the `images/` folder in the project root |
| `blog images=none` | No images; insert marked placeholders |
| `blog images=mixed` | Own images first, Unsplash to fill gaps |

Free-text instructions such as "use the photos I uploaded" mean the same. Details are in `references/image-sources.md` (in this skill's folder).

## Terms

- **Project files** are in the website project root: `CLAUDE.md`, `.env`, `keywords.csv`, `images/`, `references/` (voice, tone, humor, opinions, stats, stories), `content/`, `docs/`.
- **Bundled files** are in this skill's folder: `references/image-sources.md`, `references/on-page-seo-checklist.md`, `scripts/optimize-image.mjs`.

## Step 0: Project and image pre-flight (before any other work)

1. Confirm this is a site project: `CLAUDE.md`, `keywords.csv`, and `content/blog/` exist (or a blog template to build on). If something core is missing, **stop** and say which setup step is missing. Do not improvise a site.
2. Resolve the **image mode** and run its pre-flight, exactly as `references/image-sources.md` sections 1 and 2 say. In particular:
   - `unsplash`: confirm `UNSPLASH_ACCESS_KEY` is in `.env` (never print it) and that `.env` is in `.gitignore`. If missing, **stop** and tell the user how to add it themselves; offer `local` or `none`.
   - `local`: confirm `images/` exists and has images. If not, stop and say so.
3. Never ask the user to paste a key into the chat.

## Step 1: Cadence check

Read the publishing ramp in `CLAUDE.md` and `content/published.json` (each entry has `date`). If today's count already meets the stage limit, **stop** and tell the user. Default is **1 post per run**. Ramp: day 1 → 1, day 2 → 1, day 3 → 2, day 5 → 3, day 8 → 4, then keep it reasonable. Never exceed the limit without the user saying so.

## Step 2: Pick the keyword

- If the user gave a keyword, use it if it is not in `content/published.json`.
- Otherwise take the next qualifying row in `keywords.csv` not in `published.json`, preferring: difficulty ≤ 30, volume ≥ 100, informational intent, and a searcher who could become a customer.
- Skip other companies' brand names, "how to become a [profession]" queries, and anything off-topic for the business.
- Show the keyword and why you chose it. If nothing qualifies, say so and stop.

## Step 3: Keyword cluster

Build **5 to 10 related terms** (from `keywords.csv` where possible: same stem, questions, long-tail variants; supplement with close variations only if needed). Mark which become H2/H3 headings, which are FAQ questions, and which are used in the body. The post ranks for the whole cluster, not just the primary keyword.

## Step 4: Research the top 3 results

Search Google (web search) for the primary keyword. Take the **top 3 organic results**, skipping Reddit, Quora, forums, video and big directories. For each, record: word count, H2 count, H3 count, image count, FAQ presence, topics covered, format (guide, list, how-to), and how the keyword is used. Then:

- Compute the **averages**: word count, H2s, images. These are the targets.
- List topics all three cover (must include) and topics none cover (your angle).
- Show this as a short table before writing.

## Step 5: Read the voice files

Read **every** file in the project `references/`: voice, tone, humor, opinions, stats, stories. Use only real stats and stories from them. If a useful stat or story is missing, write `TODO(owner): <what is needed>` in the draft. **Never invent** numbers, quotes, customers, results or anecdotes.

## Step 6: Write the post

To the averaged targets, in the owner's voice:

- **Hook in the first 50 words** per `references/humor.md` (joke, self-aware aside or vivid image; adjust to the brand's tone). Serious or emergency topics get less humor, per `tone.md`.
- Primary keyword in the H1 and in the first 100 words; cluster terms placed naturally; no stuffing.
- Answer the query directly and early, then go deeper. Be specific and practical (costs, timeframes, steps, warnings), only where the facts are known.
- Include a clear opinion or recommendation where the owner has one (`opinions.md`).
- End with a call to action linking to the most relevant service page.
- **No generic AI openings** ("In today's fast-paced world", "In this comprehensive guide", "Delve into").

## Step 7: Images

Follow `references/image-sources.md` for the chosen mode. Summary:

- `unsplash`: search, pick, **hotlink** the API's URLs with size parameters, send the download ping, add visible attribution with UTM links, store the credit in frontmatter. Show the user the chosen photos in the report.
- `local`: look at the images in `images/`, pick the ones that fit and are unused, optimize copies into `public/images/blog/<slug>/` with `scripts/optimize-image.mjs`, write honest alt text, never touch the originals. Update `content/images-used.json`.
- `none`: insert marked placeholders.
- `mixed`: local first, Unsplash only for gaps.

Match the **image count** to the competitor average, with one hero image and the rest lazy-loaded. Every image gets `alt`, `width` and `height`.

## Step 8: On-page checklist

Use the project's `docs/on-page-seo-checklist.md` if present, otherwise the bundled `references/on-page-seo-checklist.md`. Apply every applicable item: exactly one H1, meta title ≤ 60 and description ≤ 160, 3 to 5 internal links (to real, existing pages and at least one service page), 2 to 3 external links to reputable sources, 4 to 8 FAQ questions with FAQPage JSON-LD, Article and BreadcrumbList JSON-LD, Open Graph and Twitter tags, canonical URL, clean slug, alt text.

**Keep the humor and voice intact.** If a checklist item would damage the post, flag it in the report instead of forcing it.

## Step 9: Publish through the standard template

Save to `content/blog/<slug>.md` with the project's standard frontmatter (title, description, slug, primary_keyword, cluster, date, images, faq) so it renders through the **same static page template** as every earlier post. Do not alter the template's technical SEO per post. Make sure the blog index, sitemap and internal links will pick the post up. Add links **to** the new post from 2 to 3 relevant existing posts or pages where natural.

## Step 10: Bookkeeping

Append to `content/published.json`: `{ "keyword": ..., "slug": ..., "type": "blog", "date": ... }`. Never reuse a keyword.

## Step 11: Verify

Run `npm run build` and fix errors (the site must stay a static export). Then print the **audit report**:

```
PAGE: content/blog/<slug>.md   TYPE: blog   PRIMARY KEYWORD: <kw>
PASSED: n/90   FAILED: n   N/A: n
FAILED ITEMS: #<n> <item> -> <what is wrong> -> <fix>
VOICE CHECK: pass | fail (hook in first 50 words? no generic AI phrasing? only true stats and stories?)
```

Fix failures and re-run the audit. Check that the page contains real HTML text (static), not content that only appears with JavaScript.

## Step 12: Report

Give the user: the keyword and why; the cluster; targets vs actuals (words, H2s, images); the image mode used and each image (source, description, link); every `TODO(owner)`; the file path; and the cadence status ("posts today: n of limit"). **Do not deploy, push or commit unless the user asks.** Remind them to request indexing in Search Console after deploying (about 10 a day).

## Hard rules

- One keyword = one post. Never reuse a keyword.
- Never fabricate stats, stories, quotes, customers, prices, locations or what an image shows.
- Never print, log, commit or paste any API key. Never use a `NEXT_PUBLIC_` prefix for a key.
- Unsplash images are hotlinked with attribution and a download ping. Never self-host them.
- Own images: never modify the originals in `images/`.
- Never bulk-publish. Respect the cadence ramp.
- Content quality beats checklist compliance.
