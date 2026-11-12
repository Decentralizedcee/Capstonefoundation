# What is checked (and what each means)

Severity: **High** blocks search visibility or is plainly broken; **Medium** loses opportunity; **Low** polish. Only report what the facts show.

| Check | Good looks like | Notes |
|---|---|---|
| Page loads | 200 OK, not a password or error page | If not, stop and report. |
| Title | 30 to 60 characters, unique, main topic near the start | Missing or duplicated is High. |
| Meta description | 70 to 160 characters, unique, a reason to click | Missing is Medium. |
| H1 | Exactly one, describes the page | None or several is Medium. |
| Heading order | H2 under H1, no skipped levels | Low. |
| Canonical | Present and points to the page's preferred address | Missing is Low; pointing elsewhere unexpectedly is High. |
| Robots tags | No unexpected `noindex` | `noindex` on a page meant to rank is High. A preview or password site may be noindex on purpose. |
| Language / viewport | `lang` set; mobile viewport tag present | Missing viewport is High for mobile. |
| Social tags | `og:title`, `og:description`, `og:image` | Low. |
| Structured data | Valid JSON-LD where it fits (Organization, Product, Article, LocalBusiness) | Report what exists; do not claim it is valid unless a validator was run. |
| Images | Every content image has descriptive alt text; sizes and formats sensible | Missing alt is Medium. Decorative images may have empty alt. |
| Links | Internal links exist; link text is descriptive; no obviously empty links | Do not claim broken links unless fetched and failed. |
| robots.txt | Exists; does not block the whole site; lists the sitemap | |
| Sitemap | Exists, lists the audited pages | |
| HTTPS | Page served over HTTPS | |
| Speed | Lighthouse numbers if measured | Otherwise "not measured". |
| Content | Page has enough real text to answer the visitor; product pages have unique descriptions | Judgement; quote the evidence. Client's decision. |
