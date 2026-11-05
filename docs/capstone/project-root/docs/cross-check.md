# Cross-check: Capstone Build Spec vs. the SEO guide

Compared: `docs/capstone-build-spec.pdf` (the build spec) against `docs/seo-step-by-step-guide.pdf`, `docs/seo-with-claude-guideline.md`, `docs/seo-kit/` and the two skills.

**Rule of precedence:** the build spec wins for copy, design and content. The SEO guide supplies the *method* for content and optimization only.

---

## 1. What matched (no change needed)

| Topic | Both agree |
|---|---|
| Static site, fast, crawlable | Static output; no server rendering |
| Host | Render Static Site, build `npm install && npm run build` |
| Render + domain flow | Temporary onrender.com first, custom domain later, DNS records in the registrar |
| Secrets | Keys only in `.env` / Render env vars, never in the repo or browser |
| Unsplash rules | API URLs, download endpoint, photographer + Unsplash credit with links, Access Key only |
| Own photos first | Own images are preferred; the pipeline processes copies and keeps originals |
| Sitemap, robots.txt, canonical, Open Graph, JSON-LD | Required by both |
| Meta title / description per page | Required by both |
| Alt text on images, no layout shift | Required by both |
| Lighthouse | Spec: 95+ on mobile (all four). Guide said 100. **Use the spec's 95+.** |
| Never invent facts / stats | Both |
| Approval gates | Spec: plan first, then build. Guide: checkpoints per phase |

## 2. What was different, and what was corrected

| # | Spec | Guide / skills said | Correction made |
|---|---|---|---|
| 1 | **Astro** (static), Tailwind v4, TypeScript; output folder **`dist/`** | Next.js with `output: 'export'`, folder `out/` | Kit and skills are now **stack-aware** through a "Stack adapter" block in `CLAUDE.md`. For this site: Astro, `dist`. |
| 2 | Blog is an **MDX collection** at `src/content/stories`, route `/stories` | `content/blog/*.md` | Skill reads the content folder, format and route from the Stack adapter. |
| 3 | **Charity** with Programs, Donate, Get involved, Stories. No service + city pages. | Service pages (zipper), CPC-sorted money keywords, Google Business Profile | `service-page` skill is **not used** on this site and says so. Stories carry the SEO. Business Profile is not relevant unless the owner later wants a listing. |
| 4 | Voice: **hopeful, openly Christian, no humor** | Humor rule: dad joke in the first 50 words | Voice and humor files rewritten for Capstone (humor: none). The skill's hook rule now fits the brand's tone (human moment, question or clear promise when humor is off). |
| 5 | Photos live in **`images-incoming/`** (git-ignored); a **sharp pipeline** converts to AVIF and WebP, strips EXIF/GPS, skips receipts, IDs and similar, records each image in `src/data/images.ts`, and needs a **slot map approval** | `images/` folder and a generic optimizer | `CLAUDE.md` sets `local_images_dir: images-incoming` and the project's pipeline. The skill uses the project pipeline (not its bundled script) when one is defined. |
| 6 | **`PUBLIC_INDEXABLE=false`** until the domain is live: `noindex` on every page and robots disallows everything | Guide's Phase 13 said to submit to Search Console and request indexing straight after deploy | Guide now says: **do not** submit or request indexing until the real domain is live and `PUBLIC_INDEXABLE=true`. Also: `PUBLIC_*` values are read **at build time**, so redeploy after changing one. |
| 7 | Quality bar includes **WCAG AA, keyboard navigation, 360 px, reduced motion, works without JavaScript** | Guide mentioned accessibility only through Lighthouse | Added to the acceptance step in the start prompt. |
| 8 | Strict **privacy rules** (no amounts, receipts, diagnoses, children's surnames) and **no invented Scripture** | Guide had a general "no invention" rule | Added to `CLAUDE.md`, the references and the skill's hard rules. |
| 9 | Seeded stories are **drafts** and "do not publish drafts" | Skill published posts | New posts are written with `draft: true`; an existing stub for the keyword is **filled in**, not duplicated. |
| 10 | No keyword data | Skill needs keywords with volume and difficulty | `keywords.csv` seeded from the 8 story titles, marked **unverified**. Fill volume and difficulty from Semrush (free trial) before leaning on it. |

## 3. Conflicts inside the spec itself (owner decisions)

These are in the spec as written. I applied the "Resolution" so work is not blocked. Please confirm or change.

| # | Issue | Resolution applied | Your decision |
|---|---|---|---|
| A | **Images:** the spec wants optimisation through `astro:assets` **and** Unsplash's returned URLs. Unsplash requires hotlinking; Astro's remote-image optimisation downloads and re-hosts the photo. | Own photos via `astro:assets`; Unsplash photos hotlinked with plain `<img>` and size parameters. | ☐ OK  ☐ Change |
| B | **Testimonial 2** (healing from leg pain) vs the rule "never publish diagnoses or case details". | Included as written because consent is stated. | ☐ Keep  ☐ Remove  ☐ Soften wording |
| C | **Testimonial 1** shows the mother's surname with the child's first name; the rule says children's surnames are never published. | Included as written because she agreed to be quoted. | ☐ Keep  ☐ Use first name only |
| D | **`DonationPanel`** is described but missing from the component list. | Built as part of the component list. | ☐ OK |
| E | **Unsplash credit** only in the footer. Unsplash's rules ask for credit where the photo is displayed. | Footer line **and** a credit beside each Unsplash image. | ☐ OK  ☐ Footer only |
| F | **Scripture in stories:** the spec allows only the verses it quotes, but two seeded stories are about Bible verses. | Any other verse is flagged `TODO(owner)` to verify text and translation. Tell me the translation you prefer (for example NIV, ESV, KJV). | Translation: ________ |
| G | **Spelling:** "programs" in page copy, "programmes" in Values. | New copy uses "programs". | ☐ OK  ☐ UK spelling ("programmes") |
| H | **Sport Development Program** is "backed by Capstone Foundation" and may have its own site. | Button appears only when `sportProgramUrl` is set. | ☐ OK |

## 4. What the SEO method gives this site (and what it does not)

| Guide idea | Used on Capstone? |
|---|---|
| Static, crawlable site | Yes (Astro static) |
| Keyword research with Semrush (KD ≤ 30, volume ≥ 100, intent) | **Yes, for Stories.** Fill `keywords.csv`. |
| Blog posts at scale, keyword clusters, top-3 competitor format | **Yes**, through the `blog` skill |
| Voice, stats and stories reference files | **Yes**, written from the spec (`references/`) |
| On-page checklist (90 items) | **Yes**, with the "humor" and "service page" items marked not applicable |
| Technical SEO, sitemap, robots, Lighthouse loop | **Yes** (Astro integrations produce the files) |
| Service pages (service + city) | **No** |
| Google Business Profile | Not unless the owner chooses a local listing later |
| Off-page backlinks | Optional, later. Church and ministry directories, partner churches and genuine guest posts are the natural fit. Avoid paid link packages. |
| Publishing cadence (1, 1, 2, 3, 4 per day) | Yes. Stories start as drafts and are published slowly after owner review. |
| Request indexing | **Only after the domain is live and `PUBLIC_INDEXABLE=true`** |

## 5. Still needed from the owner (from the spec's own list)

SVG or transparent PNG logo; consented photos in `images-incoming/`; bank account details; founding story and trustees; CAC number; office address; more testimonials; Unsplash Access Key and app name (if using Unsplash); Semrush data for `keywords.csv`.
