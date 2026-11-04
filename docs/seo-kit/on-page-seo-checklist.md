# On-Page SEO Checklist (reconstructed, 80+ items)

The video says its checklist has "80+ signals" and shows only a few. This is a reconstruction.

- **[V]** means the video named it.
- All other items are **[Standard SEO]**, general best practice that fits the video's approach.

Use it as a pass/fail audit on **every blog post and service page**. Do not apply it at the cost of the voice and humor. Content quality comes first. [V]

Some items apply only to blogs (B) or only to service pages (S). Unmarked items apply to both.

---

## A. Keyword targeting (1–10)

1. One **primary keyword** chosen per page (from the keyword CSV).
2. A **keyword cluster** of 5 to 10 secondary and long-tail terms chosen. [V]
3. The primary keyword matches the page's **search intent**: informational for blogs, commercial for service pages. [V]
4. No two pages target the same primary keyword (no cannibalization). Check `content/published.json`.
5. Primary keyword in the **H1**.
6. Primary keyword in the **first 100 words**. [V]
7. Primary keyword in the **meta title**, ideally near the start.
8. Primary keyword in the **meta description**.
9. Primary keyword in the **URL slug**.
10. Primary keyword in the alt text of at least one image. Natural wording only.

## B. Title, description and URL (11–20)

11. Meta title is **≤ 60 characters**, unique across the site.
12. Meta title is compelling (a benefit, number or hook), not just keyword stuffing. [V: shown in search result]
13. Meta description is **≤ 160 characters**, unique, and has a reason to click. [V]
14. Meta title and description do not contain truncated or duplicated phrasing.
15. URL is lowercase, hyphen-separated and short (≤ 5 words where possible).
16. URL has no dates, IDs, parameters or stop-word padding.
17. A **canonical URL** tag is present and points to the page itself.
18. `<html lang="...">` is set correctly.
19. Page is **indexable**: no stray `noindex`.
20. Page is listed in `sitemap.xml` and not blocked by `robots.txt`.

## C. Headings and structure (21–30)

21. **Exactly one H1**. [V]
22. H1 is not identical to the meta title (a slight variation is fine).
23. Headings follow a logical order (H1 → H2 → H3). No skipped levels.
24. **H2 count** matches the average of the top 3 ranking pages for the keyword. [V: average of the top 3]
25. H2s and H3s include secondary keywords naturally.
26. At least one H2 phrased as a question that the page answers (B).
27. Short paragraphs (2 to 4 lines), scannable subheadings, no walls of text.
28. Lists or tables used where they make content clearer.
29. A short summary or answer near the top (B), for featured snippets and AI answers.
30. A clear call to action section at the end (B) / above the fold and repeated (S).

## D. Content quality (31–45)

31. **Word count** matches the average of the top 3 ranking pages. [V]
32. Covers every major topic the top 3 results cover, plus at least one thing they miss.
33. **Original voice**: reads like the owner, not generic AI. [V]
34. **Hook in the first 50 words** (joke, aside or vivid image, per the brand's tone). [V]
35. Uses real **stats** about the business where relevant. Never fabricated. [V]
36. Includes a real **story or anecdote** where relevant. Never fabricated. [V]
37. Includes a clear **opinion or recommendation**, not only neutral information.
38. Answers the search query directly and early.
39. Practical, specific, actionable detail (costs, timeframes, steps, warnings).
40. No filler openings ("In today's fast-paced world…"). [V]
41. No keyword stuffing. Keyword use reads naturally.
42. Facts are accurate and any claims are defensible.
43. Reading level suits the audience (generally Grade 7 to 9).
44. Author name / byline and "last updated" date shown (B).
45. Content is not duplicated from another page on the site or from competitors.

## E. Links (46–55)

46. **3 to 5 internal links** to relevant posts or pages (B). [V]
47. **2 to 3 external links** to reputable, relevant sources (B). [V]
48. Internal links use **descriptive anchor text**, not "click here".
49. At least one internal link points to a **relevant service page** (B), passing authority to money pages. [V: blogs lift service pages]
50. Service pages link to **related blog posts** and to the other relevant services (S).
51. No broken links (internal or external).
52. External links open normally, with `rel="noopener"` if `target="_blank"` is used.
53. Paid or affiliate links use `rel="sponsored"`.
54. No orphan pages: every page is reachable from at least one other page.
55. Breadcrumb navigation present and linked.

## F. Media (56–62)

56. At least one **relevant image** (count matches the competitor average). [V]
57. Every image has descriptive **alt text**.
58. Images have explicit width and height (prevents layout shift).
59. Images are compressed and served in modern formats (WebP or AVIF).
60. The above-the-fold hero image is prioritized, and others are lazy-loaded.
61. Descriptive image file names (`low-water-pressure-fix.webp`, not `IMG_123.webp`).
62. Photo credits included where the licence asks for them (for example Pexels).

## G. FAQ and rich results (63–67)

63. **4 to 8 FAQ questions** with concise answers (B). [V]
64. Questions come from real searches (Semrush questions tab, "People also ask"). [V: questions tab]
65. FAQ marked up with **FAQPage JSON-LD**. (Check current Google rich-result eligibility; the markup is still useful for AI parsing.)
66. **Article** JSON-LD on blog posts (headline, author, dates, image).
67. **Service / LocalBusiness** JSON-LD on service pages (name, area served, phone, address, opening hours).

## H. Social and sharing (68–71)

68. **Open Graph** tags: `og:title`, `og:description`, `og:image`, `og:url`, `og:type`. [V: OG tags seen in DevTools]
69. **Twitter card** tags.
70. OG image is correctly sized (about 1200×630).
71. Share image has legible text and branding.

## I. Technical and performance on the page (72–82)

72. **Mobile-friendly** layout with a correct viewport tag.
73. **Lighthouse: 100 on SEO, Accessibility, Best Practices and Performance** (target). [V]
74. **Largest Contentful Paint** under 2.5 s.
75. **Cumulative Layout Shift** under 0.1.
76. **Interaction to Next Paint** under 200 ms.
77. Page is rendered as **static HTML** (SSG). [V]
78. No render-blocking resources. Scripts are deferred or async. [V: render-blocking named]
79. Minimal JavaScript, no legacy polyfills. [V: legacy JavaScript named]
80. HTTPS only, no mixed content.
81. Page returns **200**, not a redirect chain.
82. Custom **404** page exists and links back into the site.

## J. Conversion and trust (83–90)

83. A clear **call to action** above the fold (S) and at the end (B).
84. A contact **form or click-to-call** that works and is accessible. [V: fill out the form]
85. **Social proof**: reviews, years in business, certifications, guarantees (S).
86. NAP (name, address, phone) is **consistent** with the Google Business Profile.
87. Local relevance: mentions the specific city, area or neighbourhoods served (S).
88. Trust pages are linked: about, contact, privacy.
89. Layout matches the best-**tested** landing page where one exists. [V: the 20% conversion page]
90. Forms have thank-you states and conversion tracking set up.

---

## Audit report format

When asked to audit a page, output:

```
PAGE: <url or file>   TYPE: blog | service   PRIMARY KEYWORD: <kw>
PASSED: n/90   FAILED: n   N/A: n
FAILED ITEMS:
  #<n> <item> → <what is wrong> → <fix>
VOICE CHECK: pass | fail  (hook in the first 50 words? No generic AI phrasing? Only true stats?)
```

Fix failing items without dulling the voice, then re-run the audit.
