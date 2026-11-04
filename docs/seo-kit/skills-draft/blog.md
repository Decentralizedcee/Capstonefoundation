---
name: blog
description: Generate one fully SEO-optimized blog post in the owner's own voice. Picks an unused keyword from keywords.csv, builds a keyword cluster, researches the top 3 Google results, writes to the averaged format, adds Pexels images, applies the on-page SEO checklist, and publishes using the standard page template. Use when the user types "blog", asks for a new blog post, or asks to publish the next post.
---

# blog (DRAFT, not installed)

Reconstructed from the video's description of the `blog` skill. Install to `.claude/skills/blog/SKILL.md` only after approval.

## Inputs
- `keywords.csv`: Semrush export (keyword, volume, KD, intent…)
- `content/published.json`: keywords already used
- `references/`: voice, tone, humor, opinions, stats, stories
- `docs/on-page-seo-checklist.md`
- `.env`: `PEXELS_API_KEY`
- `CLAUDE.md`: project rules (SSG, stack, cadence)

## Procedure

0. **Pre-flight: Pexels key.** Before anything else, check that `.env` in the project root contains `PEXELS_API_KEY` (check that it is set; never print or echo the value). If it is missing, **stop** and tell the user: create a file named exactly `.env` in the project root (next to `CLAUDE.md`) containing `PEXELS_API_KEY=their_key`, and add it themselves, not in chat. Offer to continue without images (marked image placeholders) only if the user says so. Also confirm `.env` is listed in `.gitignore`.
1. **Cadence check.** Read the current publishing stage in `CLAUDE.md` / `content/published.json`. If today's post count already meets the stage limit, stop and tell the user. Default is 1 post per run. Never exceed the limit without asking.
2. **Pick the keyword.** Take the next row in `keywords.csv` that is not in `content/published.json`, preferring (a) KD ≤ 30, (b) volume ≥ 100, (c) informational intent, (d) a searcher who could become a customer. Skip other companies' brand names and "how to become a …" queries. Show the chosen keyword before continuing. If none qualify, say so.
3. **Build the keyword cluster.** 5 to 10 related terms from `keywords.csv` (similar stems, questions, long-tail variants). Supplement with close variations only if needed. Note which are H2/H3 candidates and which belong in the FAQ.
4. **Research the top 3 results.** Search the primary keyword. Take the top 3 organic results, excluding Reddit, Quora, forums and video. Record each page's word count, H2 count, H3 count, image count, FAQ presence, topics and format. Compute the **averages** and list topics all three cover plus gaps. Show a short table.
5. **Read the references.** Read every file in `references/`. Use only real stats and stories from them. If something useful is missing, write `TODO(owner):` and never invent it.
6. **Write the post** to the averaged targets, in the owner's voice.
   - The hook in the first 50 words follows `references/humor.md`.
   - Primary keyword in the H1 and first 100 words.
   - Cluster terms placed naturally.
   - Answer the query early. Be specific and practical.
   - No generic AI openings.
7. **Images.** Fetch relevant photos from Pexels via the API, using the number matching the competitor average. **Download and compress them into the project** (WebP, sensible dimensions, descriptive file names) instead of hotlinking, so the deployed static site does not depend on the key. Add descriptive alt text and the photographer/Pexels credit where Pexels requires it. Never print the API key.
8. **Apply the on-page checklist.** Work through `docs/on-page-seo-checklist.md`: one H1, meta title ≤ 60 and description ≤ 160, 3 to 5 internal links (find real existing pages), 2 to 3 external links, 4 to 8 FAQs with FAQPage JSON-LD, Article JSON-LD, OG/Twitter tags, canonical, slug. **Keep the humor and voice intact.**
9. **Publish using the standard template.** Save as `content/blog/<slug>.md` with the project's standard frontmatter, so it renders through the same static page template as every earlier post. Do not change the technical-SEO template per post.
10. **Update bookkeeping.** Append the keyword to `content/published.json` with the slug and date. Make sure the blog index and sitemap will include it.
11. **Verify.** Run `npm run build`. Fix errors. Print the audit report (passed/failed items and the voice check).
12. **Report.** Give the keyword, cluster, targets vs actuals, anything marked `TODO(owner)`, and the file path. Do not deploy or push unless asked.

## Hard rules
- One keyword = one post. Never reuse a keyword.
- Never fabricate stats, quotes, customers or stories.
- Never bulk-publish. Respect the cadence ramp (day 1 → 1, day 2 → 1, day 3 → 2, day 5 → 3, day 8 → 4).
- Content quality beats checklist compliance. If a checklist item would ruin the post, flag it instead of forcing it.
