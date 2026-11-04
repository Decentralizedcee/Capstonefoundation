---
name: service-page
description: Generate one SEO-optimized, conversion-focused service landing page for any business (a service plus a location, the "zipper" method). Picks an unused row from service-keywords.csv or uses the one given, researches the top 3 results, builds the page on the site's winning landing-page layout with unique local copy, adds images from Unsplash or the owner's own images folder (chosen per run), applies the on-page SEO checklist, and publishes through the standard static template. Use when the user types "service", asks for a new service page, a service + city page, or a landing page for a money keyword.
---

# service-page

Creates **one** service landing page per run for a statically generated website (Next.js static export, hosted on Render). A service page targets a **money keyword** (someone wants to hire), unlike a blog post, which targets someone who wants to learn. The goal is to get the visitor to fill out the form or call.

Method from Jono Catliff's "Claude Code SEO" video: the zipper (service + location), CPC-sorted money keywords, a layout that already converts, and restraint (never thousands of near-identical pages).

## Invocation

| What the user types | Meaning |
|---|---|
| `service` | Next unused row from `service-keywords.csv`, image mode from `CLAUDE.md` (or ask) |
| `service <service> <city>` | Build exactly this pair (must be unused) |
| `service images=unsplash` / `local` / `none` / `mixed` | Choose the image source for this run |

Image modes work exactly as in the `blog` skill. Details: `references/image-sources.md` (in this skill's folder). Free-text such as "use the photos I uploaded" also works.

## Terms

- **Project files**: `CLAUDE.md`, `.env`, `service-keywords.csv`, `images/`, `references/` (voice, tone, humor, opinions, stats, stories), `content/`, `docs/`.
- **Bundled files**: `references/image-sources.md`, `references/on-page-seo-checklist.md`, `scripts/optimize-image.mjs`.

## Step 0: Project and image pre-flight

1. Confirm `CLAUDE.md`, `service-keywords.csv` and `content/services/` (or a service page template) exist. If core pieces are missing, **stop** and name the missing setup step.
2. Resolve the image mode and run its pre-flight per `references/image-sources.md`. Missing `UNSPLASH_ACCESS_KEY` or an empty `images/` folder means **stop** and tell the user how to fix it, or offer another mode. Never ask for a key in chat.
3. Read `CLAUDE.md` for: business facts, services, locations, phone/email/NAP, the primary conversion goal, and the layout rules.

## Step 1: Restraint check

Count pages in `content/services/`. The guidance: be tasteful. **Never thousands, probably not hundreds.** If the total reaches the cap in `CLAUDE.md` (default **50**), **stop** and ask the user before adding more. Also respect the publishing cadence in `CLAUDE.md` (a service page counts as a post for the day's limit).

## Step 2: Pick the keyword

- Use the user's pair if given; otherwise the next row in `service-keywords.csv` not in `content/published.json`.
- It should follow the zipper pattern: **service + location** (or location + service) for a service and place the business actually serves (check `CLAUDE.md`). Prefer commercial intent and a meaningful CPC.
- Reject other companies' brand names, places the business does not serve, and services it does not offer.
- Check **overlap**: if the page would be near-identical to an existing one, tell the user and do not create a duplicate-looking page.
- Show the choice and why.

## Step 3: Research the top 3 results

Search Google for the keyword. Take the top 3 organic results (skip big directories like Yelp or Homestars for the benchmark, but note them separately). Record: sections included, calls to action, trust signals, form placement, length, FAQ presence, images, and how the keyword is used. Compute average length and section list, note gaps. Show a short table.

## Step 4: Read the facts and voice

Read `CLAUDE.md` and every file in the project `references/`. Service pages use a **confident, clear, reassuring** tone, with lighter humor than blog posts (follow `tone.md`). Use only real proof from `stats.md` and `stories.md`. Anything unknown is `TODO(owner): <what is needed>`. **Never invent** prices, licences, addresses, reviews, response times, guarantees or service areas.

## Step 5: Build the page

Use the site's **winning landing-page layout** (the homepage's conversion layout unless a tested variant exists in `CLAUDE.md`). Sections:

1. **Hero:** H1 containing the keyword, a one-line promise, and the call to action with the form or click-to-call **above the fold**.
2. **Why choose us:** real proof (years, jobs, rating, certifications, guarantees).
3. **The service explained:** what it includes, who it's for, how it works.
4. **Process / what to expect.**
5. **Pricing guidance:** only if the owner has given it, otherwise `TODO(owner)`.
6. **Local section for the location:** areas or neighbourhoods served, local conditions or rules, **only if accurate**, otherwise `TODO(owner)`.
7. **Reviews / trust signals** (real ones only).
8. **FAQ (4 to 6)** specific to this service and place, with FAQPage JSON-LD.
9. **Related blog posts (3)** and **related service pages (1 to 2)**.
10. **Final call to action** repeating the form or phone number.

The copy must be **genuinely unique** to this service and place. Not the same page with a swapped city name: different local detail, different FAQs, different examples.

## Step 6: Images

Follow `references/image-sources.md` for the chosen mode (Unsplash: hotlink, download ping, attribution, show picks in the report; local: look at the images, pick unused ones, optimize copies into `public/images/services/<slug>/`, honest alt text, never touch originals; none: placeholders). Hero image eager, the rest lazy. Every image has `alt`, `width` and `height`. Do not use stock photos that imply real staff, customers or work done by the business unless the owner confirms (prefer the owner's own photos in local mode for "our team" and "our work" sections).

## Step 7: On-page checklist

Use the project's `docs/on-page-seo-checklist.md` if present, otherwise the bundled one. Apply the service-page (S) and general items: one H1, meta title ≤ 60 and description ≤ 160, `Service` or `LocalBusiness` and `BreadcrumbList` and `FAQPage` JSON-LD, canonical, Open Graph and Twitter tags, clean slug like `emergency-plumber-toronto`, descriptive alt text, consistent NAP, working form or click-to-call, and internal links to related content. Keep the tone consistent with the brand.

## Step 8: Publish through the standard template

Save to `content/services/<slug>.md` using the project's standard frontmatter so it renders through the **same static template** as the other service pages. Make sure the services index and the sitemap include it. Add internal links **to** this page from 2 to 3 relevant blog posts where natural.

## Step 9: Bookkeeping

Append to `content/published.json`: `{ "keyword": ..., "slug": ..., "type": "service", "date": ... }`.

## Step 10: Verify

Run `npm run build` and fix errors (the site must stay a static export). Print the audit report:

```
PAGE: content/services/<slug>.md   TYPE: service   PRIMARY KEYWORD: <kw>
PASSED: n/90   FAILED: n   N/A: n
FAILED ITEMS: #<n> <item> -> <what is wrong> -> <fix>
VOICE CHECK: pass | fail (consistent with tone.md? only true proof? unique local content?)
```

Fix failures and re-run. Confirm the form or call button is present in the HTML.

## Step 11: Report

Give the user: the keyword and why; page count vs the cap; the image mode used and each image (source, description, link); every `TODO(owner)`; the file path; and cadence status. **Do not deploy, push or commit unless asked.** After deploying, request indexing in Search Console (about 10 a day).

## Conversion rule (from the video)

Making service pages look like the homepage is a habit, not a law. The real principle: **test landing-page variants** (the video used Google Ads to test 5 to 10, with a best page at about 20% conversion), then **reuse the winning layout on every service page**. If the user gives test results or a winning variant, update the layout in `CLAUDE.md` and apply it.

## Hard rules

- One service + location keyword = one page. Never reuse a pair.
- Never create near-duplicate pages. Content must be genuinely different per page.
- Never invent addresses, licences, prices, reviews, results or service areas.
- Never print, log, commit or paste an API key. Never use a `NEXT_PUBLIC_` prefix for a key.
- Unsplash images are hotlinked with attribution and a download ping; never self-host them. Own images: never modify the originals.
- Respect the page cap and the cadence.
