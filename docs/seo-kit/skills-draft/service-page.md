---
name: service-page
description: Generate one SEO-optimized, conversion-focused service landing page for a service + location pair. Picks an unused row from service-keywords.csv, builds the page using the site's winning landing-page layout, writes unique local content, applies the on-page SEO checklist, and publishes using the standard template. Use when the user types "service", asks for a new service page, or a service + city page.
---

# service-page (DRAFT, not installed)

Reconstructed. The video says to "do the same thing for service pages", and describes the zipper method and the conversion rules. Install to `.claude/skills/service-page/SKILL.md` only after approval.

## Inputs
- `service-keywords.csv`: Semrush export, sorted by CPC (service + city keywords)
- `content/published.json`: keywords already used
- `references/`, `docs/on-page-seo-checklist.md`, `CLAUDE.md`
- The homepage / best-tested landing page layout

## Procedure

1. **Restraint check.** Count existing pages in `content/services/`. The video's guidance: be tasteful, never thousands, probably not even multiple hundreds. If the total is already over the cap in `CLAUDE.md` (default: 50), stop and ask.
2. **Pick the keyword.** Take the next row in `service-keywords.csv` not in `content/published.json`. It should follow the zipper pattern (service + city / city + service). Prefer commercial-intent keywords with a meaningful CPC. Reject brand names and irrelevant locations. Show the choice.
3. **Check overlap.** Make sure it's not near-identical to an existing service page. If it is, tell the user rather than creating a duplicate-looking page.
4. **Research the top 3 results** for the keyword (exclude directories like Homestars/Yelp, or analyze them separately). Record the sections they include, their calls to action, trust signals and length. Use the averages as targets and find the gaps.
5. **Build the page** with the **winning landing-page layout**: the same conversion structure as the homepage unless a tested variant exists.
   - Headline containing the keyword
   - Call to action and form above the fold
   - Why choose us (real proof from `references/stats.md`)
   - Process, what to expect
   - Pricing guidance (only if known, else `TODO(owner)`)
   - Local section for the city (neighbourhoods, local conditions, only if accurate, else `TODO(owner)`)
   - Reviews and trust signals
   - Short FAQ (4 to 6) with FAQPage JSON-LD
   - Links to 3 related blog posts and 1 to 2 related service pages
   - Final call to action
6. **Write unique copy.** Not a template with a swapped city. Use the owner's voice (tone adjusted to confident and clear for service pages, with lighter humor than blogs).
7. **Apply the on-page checklist** (service-page items), including `Service` / `LocalBusiness` and `BreadcrumbList` JSON-LD, canonical, OG tags, a slug like `emergency-plumber-toronto`.
8. **Publish** to `content/services/<slug>.md` through the standard static template.
9. **Bookkeeping.** Append to `content/published.json`. Make sure the services index and sitemap include it. Add internal links to it from 2 to 3 relevant blog posts.
10. **Verify.** `npm run build`, then print the audit report.
11. **Report.** Keyword, page count vs cap, `TODO(owner)` items, file path. Do not deploy unless asked.

## Hard rules
- Never create near-duplicate pages. Content must be genuinely different per page.
- Never invent addresses, licences, prices, reviews or service areas.
- After deploying, request indexing in Search Console (roughly 10 per day).
- Test landing page variants over time (the video's best page hit ~20% conversion), then roll the winner out to all service pages.
