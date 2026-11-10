---
name: site-setup
description: Start a new SEO-ready website project for any business or organisation, in clear stages with checkpoints. Checks the environment, runs a plain-language intake (or reads the owner's build spec), writes the project's CLAUDE.md with a Stack adapter, fills the voice and facts reference files only from what the owner said, creates the folder tree, .gitignore and .env skeleton, verifies everything with a script, then stops so the owner can upload images, logos and keys, agrees a design direction and a build plan, and finishes with a build prompt. Use when the user says "set up a new site", "start a website project", "site setup", "new project", "intake", or opens an empty folder to begin a website. Ends by writing a ready-to-paste build prompt (docs/BUILD-PROMPT.md) from the owner's own answers, and prepares the project for the blog and service-page skills. It does not build the site itself.
---

# site-setup

Prepares a project folder so a static, SEO-ready website can be designed and then fed by the `blog` and `service-page` skills. It is **business-neutral**: everything specific to one business comes from the owner's answers (or their build spec), never from this skill.

It does the first half of the owner's workflow (environment, intake, project files, folders, verification, uploads, design direction, build plan) and finishes by **writing a ready-to-paste build prompt**. It **does not scaffold or build the site itself**. The owner pastes the build prompt into a new chat for that.

The owner is usually **not technical**. Explain every step in plain words **before** doing it. Work in **stages** and **stop at each gate**. Never move on until the owner says "go".

## Invocation

| What the user types | Meaning |
|---|---|
| `site-setup` or "set up a new site" | Full flow from Stage 0 |
| `site-setup audit` | Existing project: check it and report, change nothing |
| `site-setup <path-to-build-spec>` | Use the owner's build spec as the source of truth for copy and design |
| `site-setup build-prompt` | Skip to Stage 7 and 8 on an existing project: agree the design direction and plan, then write `docs/BUILD-PROMPT.md` |

## Bundled files (in this skill's folder)

- `references/intake-sheet.md`: the questions, by group.
- `references/framework-adapters.md`: Stack adapter values and technical rules for Next.js and Astro, plus Render settings.
- `references/claude-md.template.md`: the project `CLAUDE.md` template.
- `references/reference-templates/`: voice, tone, humor, opinions, stats, stories templates.
- `references/style-reference-template.md`: how to turn an owner-supplied writing sample into a style guide.
- `references/build-prompt-template.md`: the minimum needed, the design fallback, the placeholder system and the prompt skeleton (Stage 8).
- `scripts/verify-setup.sh`: the verification script (Stage 4).

## Stage 0: Look before you touch anything

1. **Check and report** in a short table: Node.js version (20 or higher) and npm; git installed, and whether this folder is a git repository (**ask before running `git init`**); which skills are visible (`blog`, `service-page`); whether the folder is empty or already a project.
2. **If a `CLAUDE.md` already exists, this is an existing project.** Do not overwrite anything. Switch to **audit mode**: run `scripts/verify-setup.sh` (Stage 4), report findings, and offer fixes one at a time. Never replace the owner's `CLAUDE.md`, references, keywords or content.
3. **If the owner supplied a build spec** (PDF, markdown, document) read it fully. It is **canonical for copy, design, routes and acceptance criteria**. The intake then only fills gaps. Note anything in the spec that conflicts with the SEO method and list it as an **open decision for the owner** (do not decide it yourself).
4. Stop and tell the owner if something is missing or wrong (for example Node too old).

## Stage 1: Intake (plain-language questions)

Ask the questions in `references/intake-sheet.md`, **one group at a time**, and wait for answers. Rules:

- "I don't know" or "later" is a valid answer. Record it as `unknown` and carry it forward as a `TODO(owner)`. **Never guess or invent** a fact, number, name, price, licence, address, testimonial or quote.
- Never ask the owner to paste an API key or password into the chat.
- Keep a record in `docs/intake.md` (answers only, no secrets).
- Decide, and write down, these things the rest of the skills depend on:
  1. **Business type:** local service business, nonprofit or organisation, professional services or portfolio, or other.
  2. **Page types needed:** blog yes/no; service + location pages yes/no (a nonprofit or portfolio usually says no, so set `service_pages: NOT USED`).
  3. **Framework:** offer Astro (static, content-focused, light) or Next.js (static export, more app-like). Both work with the skills. Give a one-line trade-off and a recommendation that fits the business, then let the owner choose. If a build spec names a framework, use it.
  4. **Voice:** warmth, formality, **humor level** (none, light or playful), and any topics or wording that are off limits.
  5. **Image source default:** Unsplash, the owner's own images, mixed, none, or ask each time, plus any rules by context (for example "own photos for anything about our work").
  6. **Special content rules:** privacy, faith or legal wording, quoted texts (for example a Bible translation), medical or financial claims.
  7. **Hosting:** Render Static Site by default; note a domain if the owner has one.

## Stage 2: Write the project files

Show the owner what you are about to create, then create it. **Never overwrite an existing file**; if one exists, write the new version next to it as `<name>.new` and tell the owner.

1. **`CLAUDE.md`** from `references/claude-md.template.md`:
   - Fill the business facts and rules **only from the intake or build spec**.
   - Fill the **Stack adapter** block from `references/framework-adapters.md` for the chosen framework, and append that framework's technical-rules block.
   - Leave `{{placeholder}}` only where the owner said `unknown`, and list each one in your report.
2. **`references/`**: create the six files from `references/reference-templates/` (humor from the chosen level) and fill them **only from what the owner supplied**: voice and tone from intake answers; real numbers into `stats.md`; true, consented stories into `stories.md`; stated beliefs into `opinions.md`. Unknowns stay as clearly marked placeholders.
   - If the owner gave a **writing sample as a style reference**, follow `references/style-reference-template.md` (distil the technique and guardrails; never paste a whole third-party article).
3. **`keywords.csv`**: header only (`keyword,volume,difficulty,intent,status,notes`), or seeded from the owner's own list with `status: unverified` and blank volume and difficulty. Tell the owner keyword data comes from a tool such as Semrush.
4. **`docs/`**: copy the on-page checklist (from either `blog` or `service-page` skill's `references/on-page-seo-checklist.md`) to `docs/on-page-seo-checklist.md`, if it is not there.

## Stage 3: Folders and starter files (no framework scaffold)

1. Print the folder tree for the chosen framework (`references/framework-adapters.md`), explain each folder in **one plain line**, then create the missing ones. Put an empty `.gitkeep` in each empty folder.
2. Create:
   - `.gitignore` (at least `.env`, `node_modules/`, the build output folder, the framework cache folder, the local images folder contents, `.DS_Store`). Keep the images folder's `.gitkeep` tracked.
   - `.env.example` and `.env` with the same keys and **empty values** (the owner types their own keys). Only the keys the project needs (see the adapter file).
   - `README.md` placeholder (completed when the site is built).
3. **Do not** run `npm init`, install packages, or scaffold the framework. Scaffolding belongs to the build step.

## Stage 4: Verify and show proof

Run `bash <this skill>/scripts/verify-setup.sh <project-root> <nextjs|astro>` and show the **full output** to the owner. It checks required files and folders, that `.env`, the images folder, `node_modules` and the build output are git-ignored, that no secret uses a browser-exposed prefix, that `.env` values are never printed, placeholders left in `CLAUDE.md` and references, and stray video files. Fix every FAIL, explain every WARN in plain words, re-run until there are no FAILs.

## Stage 5: STOP. Tell the owner exactly what to do now

Give a plain checklist, adapted to the intake:

- Put **logos and brand files** where the plan says (and which file is which).
- Put approved **photos** in the local images folder. Not receipts, bank screenshots, ID cards, chat screenshots, medical documents; no videos (videos are embedded from YouTube or Vimeo instead).
- Type **API keys** into `.env` themselves (for example `UNSPLASH_ACCESS_KEY`). Access key only, never a secret key.
- Add the **keyword export** to `keywords.csv`, or say they will do it later.
- Fill any **`TODO(owner)`** items listed in your report.
- Tell the owner what to type when done ("go").

**Wait for "go".**

## Stage 6: Check what arrived (no processing)

List files in the brand and images folders with sizes. Look at each photo. Flag anything that looks like a receipt, bank screenshot, ID, chat screenshot, medical document, fee slip, or anything showing an account number, and say it will be skipped. Flag very large files, duplicates and unreadable files. Do **not** move, edit or delete anything. Report how many look usable.

## Stage 7: Design direction and build plan

1. **Design direction.** If the owner has a build spec, a reference screenshot or link, use it (describe its system in words; never copy a third party's logo, copy, photos or fonts). If not, follow the **design fallback** in `references/build-prompt-template.md` section 3: propose two or three simple directions from the owner's mood words, compute contrast honestly, recommend one, and let the owner pick or tweak. Save the decision to `docs/design-direction.md`.
2. **Build plan.** Propose the plan in plain words: the file tree, the pages and their copy status (FIXED, DRAFT or PLACEHOLDER), the component list, how visitors contact or act (forms, mailto, WhatsApp, booking, donations later), and any open questions (including conflicts found in a build spec). Save the **approved** plan to `docs/build-plan.md`.
3. **STOP and wait for approval** of the design direction and the plan. Do not start building.

## Stage 8: Write the build prompt

1. Check the **minimum** in `references/build-prompt-template.md` section 2. If something is missing, ask for it. Do not write the prompt yet.
2. Fill the skeleton in `references/build-prompt-template.md` section 5 from the sources in section 1 (spec, `CLAUDE.md`, `docs/intake.md`, `docs/build-plan.md`, `docs/design-direction.md`). Never invent. Unknowns become `TODO(owner)` with the **placeholder system** (hidden sections, never empty boxes or fake content).
3. Save it to `docs/BUILD-PROMPT.md` (never overwrite an existing one; write `.new` instead) and **show the full text in the chat in a code block** so the owner can copy it.
4. Give the owner plain instructions: open a **new chat** in this project folder, paste the prompt, and answer its questions. Explain the stop points (image slot map, anything not covered, before deploying). Tell them that when the site is built and approved, the `blog` skill (and `service-page`, if the business needs it) can run.
5. Show the **list of `TODO(owner)` items** that will still need their input.

The skill ends here. **Building happens in the new chat** that uses the build prompt, not in this skill.

## Hard rules

- Never invent facts, statistics, names, dates, addresses, prices, licences, testimonials, quotes, partners or Scripture.
- Never ask for, print, log, commit or paste an API key or password. Never give a secret a `NEXT_PUBLIC_` or `PUBLIC_` prefix.
- Never overwrite an existing file. Never replace an existing `CLAUDE.md`.
- Never run `git init`, commit or push without asking. Never deploy.
- Never scaffold or build the site as part of this skill. Writing `docs/BUILD-PROMPT.md` is the last thing it does.
- Follow the owner's build spec and existing `CLAUDE.md` over this skill's defaults. If they conflict, ask.
- Never write the build prompt before the owner has approved the design direction and plan, and never put an invented fact in it.
- Stop at every gate and wait for "go".
