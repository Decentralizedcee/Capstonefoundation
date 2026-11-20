# Build prompt template

Used in **Stage 8** to write `docs/BUILD-PROMPT.md`. The finished prompt must be **self-contained**: a brand-new chat that has only the project folder must be able to follow it from top to bottom.

## 1. How to fill it

- **Sources, in priority order:** the owner's build spec (if any) → `CLAUDE.md` → `docs/intake.md` → the approved plan (`docs/build-plan.md`) → the chosen design direction (`docs/design-direction.md`).
- **Never invent.** Anything unknown becomes `TODO(owner)` plus the placeholder behaviour in section 4. Never guess a fact, number, name, price, licence, address, testimonial or quote.
- **Copy status for each page** (state it in the prompt):
  - **FIXED**: the owner supplied the text (or the spec has it). Use it word for word, included verbatim or by file path.
  - **DRAFT**: Claude drafts it **only from intake facts** and the owner approves it before it is final. Mark every gap `TODO(owner)`.
  - **PLACEHOLDER**: nothing supplied yet. The section stays hidden (see the placeholder system).
- **Remove** sections that do not apply (service pages when `service_pages: NOT USED`; videos when there are none; the indexable flag when the site goes straight to its real domain).
- Plain words. Short sentences. No jargon the owner has to decode.
- After writing, **show the full text in the chat in a code block** (so it can be copied) and say where the file is saved.

## 2. Minimum needed before the prompt is written

If any of these is missing, **ask for it; do not write the prompt yet.**

1. Business or organisation name
2. One sentence on what it does and for whom
3. What it offers, or which pages are needed
4. How people should contact or act (phone, email, form, WhatsApp, booking, donation)
5. The main goal of the site
6. The framework (the owner chose, or accepted the recommendation)
7. Voice basics (tone words and humor level)
8. A **design direction** (a build spec, a reference screenshot or link, or one chosen from the fallback in section 3)

Everything else is optional. Missing optional items follow section 4.

## 3. Design direction fallback

Needed when the owner has **no** build spec, reference screenshot or link.

1. From the owner's mood words (for example "calm, warm, practical") propose **two or three simple directions**. For each give: a name; a one-line feel; colour tokens (ink for text, paper for the page, a light band colour, a hairline colour, a muted-text colour, **one** brand or accent colour); a single typeface family (self-hosted); radius and surface style (flat or soft); and a contrast note.
2. **Compute contrast; do not guess.** Normal text needs 4.5:1 against its background. If the accent fails against white for small text, say so and restrict it to large text and buttons, with a darker shade for links.
3. Recommend one and say why. The owner **picks or tweaks**. Save the decision to `docs/design-direction.md`.
4. If the owner gave a **reference screenshot or link**, describe its system in words (tokens, scale, spacing, component shapes) and say "based on, copy the system only". **Never copy** a third party's logo, wordmark, copy, photos or fonts.

## 4. The placeholder system (include in every build prompt)

- One config file (`{{site config path, for example src/config/site.ts}}`) is the **single source of truth** for contact details, social links and these flags: {{one flag per unknown item, for example showAddress, showRegistration, showTeam, bankDetails}}. All `false` or `null` until the owner supplies the item.
- Any section that depends on a missing item is **hidden**, with a `TODO` comment where it will go.
- Exception, if the owner wants it: a clearly styled "coming soon" card for a page that must exist (for example a donate or booking page).
- Never show an empty box, a lorem-ipsum block or a fake testimonial.

## 5. The prompt skeleton (fill every `{{...}}`, delete what does not apply)

````
You are building the website for {{name}} in this folder (the project root). I am not technical, so explain each step in plain words before you do it. Work in STEPS. After each step run the build and tell me in 2 to 3 sentences what is done and what is next. Stop at every STOP POINT and wait for my approval.

READ FIRST, IN THIS ORDER
1. CLAUDE.md (rules, Stack adapter, decisions)
2. {{docs/<build spec file>, if any}} (canonical for copy, design and routes)
3. docs/intake.md (my answers)
4. docs/build-plan.md (the plan I approved) and docs/design-direction.md
5. references/ (voice, tone, humor, opinions, stats, stories) and docs/on-page-seo-checklist.md

GOAL AND GROUND RULES
- This is a {{type}} for {{audience}}. The main goal is {{goal}}. Voice: {{tone words}}; humor: {{none | light | playful}}.
- Use only the facts in these files. Never invent statistics, names, dates, addresses, prices, licences, testimonials, quotes or partners{{, or quoted texts}}. If something is missing, use the placeholder system below.
- {{Privacy rules}}
- {{Faith, legal, medical or financial wording rules}}
- Placeholder system: {{section 4 text, filled}}
- Do not build {{payments, accounts, database, back end}} unless the plan says so. {{Prepare for them only as the plan describes.}}
- Never put a secret in the repository or the browser. If you need anything not covered here, ask me.

STACK AND STRUCTURE
- {{framework}}, static output. Build command {{build_command}}, publish directory {{output_dir}}. Hosted as a Render Static Site. Add a render.yaml and a README with install, dev and build commands and how to edit copy, add a post and connect the domain.
- Routes: {{list}}
- Components: {{list}}
- Actions and forms: {{how visitors contact or act: mailto, phone, WhatsApp, a form service later, and so on}}
- Environment keys: {{list from the Stack adapter}}. {{If the site starts on a temporary address: the indexable flag is false (every page noindex, robots disallows everything) until the real domain is live. Public values are baked in at build time, so redeploy after changing one.}}

DESIGN SYSTEM
{{Colour token table. Type scale (desktop and mobile). Layout widths and spacing. Component shapes (radius, borders, surfaces). Button styles. Motion rules (respect reduced motion). Logo and imagery rules. A "based on {{reference}}, copy the system only" note if there is a reference.}}

PAGES AND COPY
{{For each page: purpose, sections in order, copy status (FIXED, DRAFT or PLACEHOLDER) and the fixed copy included verbatim or by file path.}}

SEO AND TECHNICAL
- Unique title and meta description for every page, canonical URLs, Open Graph and Twitter tags, sitemap.xml and robots.txt (generated), {{RSS for the blog}}, JSON-LD ({{Organization or LocalBusiness}} site-wide, Article on posts, BreadcrumbList).
- Exactly one H1 per page. Descriptive alt text. Semantic HTML. No layout shift.
- {{Place and location words to include naturally in titles and headings, so the location is always clear.}}

QUALITY BAR
- Lighthouse {{target}} or higher on mobile for performance, accessibility, best practices and SEO, checked on the built site.
- WCAG AA contrast, full keyboard navigation, a layout that works at 360px wide, reduced-motion respected, all content works without JavaScript.

IMAGES AND VIDEO
- Default image source: {{unsplash | local | mixed | none | ask}}. Rules by context: {{rules}}.
- My own photos are in {{local_images_dir}} (never committed). Process them with {{image_pipeline}}. Skip and report anything that looks like a receipt, bank screenshot, ID, chat screenshot, medical document or anything showing an account number. Write alt text that describes only what is visible. STOP POINT: propose a slot map (which image goes where) and wait for my approval before placing any image.
- {{Unsplash rules, if used: Access Key only in .env and a local script, hotlinked URLs with size parameters, download ping when a photo is chosen, visible credit beside the image.}}
- {{Videos: embed from YouTube or Vimeo only, click to load, never committed. Links: ...}}

HOW TO WORK
1. Scaffold and config.
2. Design tokens and layout.
3. Pages, one at a time, in this order: {{page order}}.
4. {{Blog index and post template, tags, feed.}}
5. SEO and structured data.
6. Final checks against DONE MEANS.
STOP POINTS: the image slot map; any decision that is not covered; before anything is deployed.

DONE MEANS
- Every page in the route list exists and uses the copy as stated (FIXED word for word).
- No invented facts. Hidden sections are controlled only by the config file.
- The design matches the tokens above and looks right at 360, 768 and 1280px wide.
- Lighthouse target met on the built site, with proof.
- Sitemap, robots, canonical tags, Open Graph tags and JSON-LD present.
- README and render.yaml present and correct.

WHAT I WILL SUPPLY LATER
{{every TODO(owner) item}}

RULES THAT NEVER CHANGE
- Never invent facts. Never publish {{private items}}. Never put a secret in the repository or the browser. If something is not covered, ask me before adding it.

Begin with step 1 now.
````
