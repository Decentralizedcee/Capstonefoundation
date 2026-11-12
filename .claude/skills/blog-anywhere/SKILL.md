---
name: blog-anywhere
description: Write SEO blog posts in a site's own voice for any platform (Shopify, WordPress, Wix...). Builds a voice profile once, then gives a copy-paste post package with SEO fields, images and a preview.
---

# blog-anywhere

Writes a blog post for **any website, on any platform**, in the site owner's own voice, and hands it over as a **copy-paste package** they can publish on their own site. Use it when you cannot or should not publish for them: Shopify, WordPress, Wix, Squarespace, Webflow, Ghost, a client's site, or a site that is not built yet.

It is **not** the same as the `blog` skill. `blog` is for a static-site project in this folder (it has a `CLAUDE.md` with a Stack adapter) and publishes the post file straight into that project. If the folder is such a project, say so and suggest `blog`, unless the owner wants a copy-paste package anyway.

## What you produce

For each post, a **package** (`post-preview.html` and files): every SEO field with a Copy button and a character count, the post as clean HTML, Markdown and a formatted copy, the image list with alt text and credits, optional structured data, a "where to paste it" guide for their platform, and a plain-language check report. The owner copies, pastes and publishes. **You never publish anything yourself**, and never say you did.

## Workspace

One folder per site: `blog-sites/<site-slug>/`, made by `scripts/new_site.py`. It holds `site.json`, `references/` (the voice files), `site-pages.csv`, `keywords.csv`, `published.json`, `posts/` and `images-incoming/`. Keep it **outside** the skill folder. To run a script, find this skill's folder first: `find / -type d -name blog-anywhere 2>/dev/null | head -1`.

## Invocation

| What the user types | Meaning |
|---|---|
| `blog-anywhere` | Start, or continue: set up the site if needed, then write the next post |
| `blog-anywhere new-site` | Make a workspace and site profile for a new site |
| `blog-anywhere voice` | Build or refresh the site's voice |
| `blog-anywhere post <topic or keyword>` | Write a post on this topic |
| `blog-anywhere package <slug>` | Rebuild a post's package after edits |

## Bundled files

- `references/site-profile-questions.md`: the questions for a new site.
- `references/voice-builder.md`: how to capture and keep a consistent voice.
- `references/reference-templates/`: voice, tone, humor, opinions, stats, stories templates.
- `references/style-reference-template.md`: turn a writing sample into a style guide.
- `references/post-anatomy.md`: what a proper post contains, in order.
- `references/post-package-spec.md`: the `post.json` fields, HTML rules and checks.
- `references/image-guide.md`: image sources and rules.
- `references/platform-paste-guides.md`: Shopify, WordPress and others.
- `references/on-page-seo-checklist.md`: the 90-item checklist (platform items are N/A here).
- `scripts/new_site.py`, `scripts/voice_tools.py`, `scripts/build_package.py`, `scripts/optimize_image.py`, `assets/preview-template.html`.

The owner is often a beginner. Explain each step in plain words before you do it, and **stop at each gate**.

## Step 0: Orient

1. Is there a `blog-sites/<site>/` workspace for this site? If not, go to Step 1. If yes, read `site.json`, every file in `references/`, `anchor-sample.md` and `published.json`.
2. If the folder is a static-site project with a `CLAUDE.md` Stack adapter, mention `blog` (see above).
3. Ask which site this post is for, if more than one workspace exists.

## Step 1: Site profile (first time for a site)

Ask `references/site-profile-questions.md` **one group at a time**. "I don't know" is fine: leave it empty and carry a `TODO(owner)`. **Never guess**, never ask for a password or key. Run `python3 <skill>/scripts/new_site.py <site-slug> --name "..." --platform <platform> --url <url>` and save the answers into `site.json`, `site-pages.csv` and `keywords.csv`. Read back a summary and get a "go".

## Step 2: Voice (before the first post)

Follow `references/voice-builder.md`: collect samples, **measure** them (`voice_tools.py stats`), write the six voice files only from evidence, **calibrate** a ~120-word sample until the owner approves, save it as `anchor-sample.md`. **Do not write a post until the voice is approved.** Say how you will keep it consistent: every post is written from these files and checked against the measured numbers.

## Step 3: Each post

1. **Topic and keyword.** Use the owner's topic, or the next unused row in `keywords.csv`. If volume or difficulty are blank, say the data is unverified and ask. Never reuse a keyword in `published.json`.
2. **Cluster.** 5 to 10 related terms, used naturally.
3. **Research.** Search the web for the primary keyword. Take the **top 3 organic results** (skip forums, directories and video). Record word count, number of H2s, images, FAQ presence, topics and format; average them for targets; list what all three cover and what none cover. Use them for **structure only**, never copy wording or facts. Show a short table.
4. **Outline** following `references/post-anatomy.md`. Show it and **wait for the owner's OK** (skip only if they say "just write it").
5. **Write** in the voice: read every voice file and `anchor-sample.md` first. Hook per the humor level (a joke only if allowed; otherwise an honest human moment, a direct question or a clear promise). Primary keyword in the first 100 words. Answer early, then go deeper. **Only true facts** from the profile, `stats.md`, `stories.md` or sources you can name; everything else is `TODO(owner)`. Quoted texts follow the owner's rule (one translation, verified exactly, cited). Signature phrases sparingly. No generic AI openings. Internal links **only** to pages in `site-pages.csv`, otherwise `[[INTERNAL:description]]`. Never invent a web address.
6. **Images.** Follow `references/image-guide.md` and the site's image rules. Decide the source for this post (own photos, Unsplash by hand, Unsplash by API, or none) and ask if unsure. Look at the owner's photos before choosing; write honest alt text; optimise copies with `optimize_image.py`. Show every stock photo you pick.
7. **Build the package.** Write `blog-sites/<site>/posts/<slug>/post.json` per `references/post-package-spec.md`, then run `build_package.py <that file> blog-sites/<site>/posts --zip`. Fix every **FAIL**, weigh every **WARN**, rebuild.
8. **Voice check.** Run `voice_tools.py check blog-sites/<site>/posts/<slug>/post.md blog-sites/<site>/voice-metrics.json`. Fix real drift; if you keep a difference, say why (topic or post type can move the numbers). Read the draft against `voice.md` and `humor.md`.
9. **On-page checklist.** Walk `references/on-page-seo-checklist.md`. Mark site-platform items (sitemap, robots, speed, templates) **N/A** and say they belong to the site.
10. **Report** (below). Update `published.json` with keyword, slug, date and status `package built`.

## Step 4: Help them publish (if they want it)

Give the platform guide for **their** platform from `references/platform-paste-guides.md`, one step at a time for a beginner. Remind them: replace image markers and `[[INTERNAL:...]]` links, remove `TODO` notes, publish as **draft or hidden first**, check the preview, then go live. **You cannot see their site**, so never say you checked it there.

## The report (every post)

```
POST: <title>   SITE: <site>   PLATFORM: <platform>
KEYWORD: <primary>   CLUSTER: <terms>   LENGTH: <words> (target <n>)
PACKAGE: <folder and zip>   Open post-preview.html in a browser.
CHECKS: <passed> passed, <warnings> warning(s), <fails> failed   (list each warning in plain words)
VOICE CHECK: <hook fits tone? no AI phrasing? only true facts? signature phrases ok?>   METRICS: <in range / drifting and why>
IMAGES: <each: source, what it shows, who uploads it, credit>
STILL NEEDED FROM YOU: <every TODO(owner), every [[INTERNAL:...]] link, every image to upload>
WHERE TO PASTE: <their platform's steps, short>
```

## Hard rules

- **Never invent** facts, statistics, quotes, customers, stories, prices, results, web addresses or licences. Unknown means `TODO(owner)`.
- **Never publish** or claim to have published. Never claim to have checked the owner's live site.
- Never ask for, print, store or repeat a password or API key. A key lives only in the owner's `.env`.
- Never write a post before the voice is approved. Never reuse the anchor sample or the owner's signature phrases heavily.
- Never present a stock photo as the owner's own people, products, team, results or testimonials.
- Posts link only to real pages the owner listed; everything else is a marked placeholder.
- Follow the owner's content rules (privacy, faith, legal, medical or financial wording) over any default here.
- Content quality and truth beat checklist scores.
