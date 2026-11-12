---
name: site-setup-chat
description: Start a website project from chat: a gentle intake, a downloadable starter folder ZIP, project files and a ready-to-paste build prompt. For beginners. Cannot see your computer.
---

# site-setup-chat (chat edition)

Gets a new website project ready, for **any** business or organisation, from the regular Claude chat. It is the chat version of the `site-setup` skill that runs in Claude Code.

## What this edition can and cannot do

- **Cannot:** see, create or change anything on the owner's computer; check their folders, Node, git or `.env`; run their build. This chat works in its own sandbox.
- **Can:** ask the questions, write every project file, **pack the starter project as a ZIP they download**, check the files it made, design a look, and write a ready-to-paste **build prompt**.
- **Building the site happens elsewhere** (Claude Code, or a developer). This skill prepares everything and never builds the site.

Never say you created, opened or checked anything **on the owner's computer**. Say "I made this file here. You download it."

The owner is often a complete beginner. Explain every step in plain words **before** doing it. Work in **stages**, **stop at each gate**, and wait for "go".

## Needs

Code execution must be on (Settings → Capabilities). If you cannot run code or offer downloads, use the **fallback**: show each file in a code block with its full path, and tell the owner to create each one by hand (give the beginner steps). Say plainly that this is slower.

## Bundled files (in this skill's folder)

- `references/beginner-walkthroughs-chat.md`: folder, ZIP, hidden files, `.env`, the `_incoming` folder, in plain words.
- `references/intake-sheet.md`: the questions, by group.
- `references/framework-adapters.md`: Stack adapter values and rules for Astro and Next.js.
- `references/claude-md.template.md`: the project `CLAUDE.md` template.
- `references/reference-templates/`: voice, tone, humor, opinions, stats, stories templates.
- `references/style-reference-template.md`: turn a writing sample into a style guide.
- `references/build-prompt-template.md`: minimum needed, design fallback, placeholder system, prompt skeleton.
- `references/on-page-seo-checklist.md`: the 90-item checklist.
- `scripts/site_tools.py`: builds the starter ZIP and packs ZIPs.
- `scripts/verify-setup.sh`: checks a project folder (used on a copy here in the sandbox).

To run a script, find it first: `find / -type d -name site-setup-chat 2>/dev/null | head -1`, then use `<that folder>/scripts/...`.

## Stage 0: Check (questions, not commands)

1. Explain in two plain sentences what this skill does and that **you cannot see their computer** (you make files, they download them).
2. Ask: **Mac, Windows or Linux?** And: **how comfortable are you with folders and files?** (*brand new*, *a little*, *comfortable*). Brand new means explain every term, one step at a time.
3. Ask: **new project, or do you already have one?** If they already have a project with a `CLAUDE.md`, say this edition is for new projects and suggest **Claude Code's `site-setup audit`** instead. Do not generate files over an existing project.
4. Ask: **do you have a build spec or design document?** If yes, ask them to upload it. Read it fully. It is canonical for copy, design and routes; note conflicts as **open decisions for the owner**.

## Stage 1: Folder first (before the business questions)

Goal: the owner **has a real project folder on their computer, understands it, and has met `.env`**, before you ask anything else.

1. Ask only what the starter needs:
   - the project folder name (suggest a short lowercase name with dashes, for example `my-business-site`)
   - the business type in a few words
   - the **framework**: offer **Astro** (static, content-focused, light) or **Next.js** (static export, more app-like), a one-line trade-off, and a recommendation that fits the business (follow the spec if it names one)
   - the **image plan**: free Unsplash photos, their own photos, both, or none; and a name for their own-photos folder (default `images`)
   - whether the site starts on a temporary address (then the indexable flag starts `false`)
   - whether they need service + location pages (a nonprofit or portfolio usually does not)
2. Write a small config file and run `python3 <skill>/scripts/site_tools.py starter config.json out`. See the script's header for the keys. It writes the folders, `.gitignore`, `.env`, `.env.example` and `README.md`, and zips them as `<name>-starter.zip` whose top folder is the project name.
3. **Offer the ZIP as a download** and say, in plain words, what is inside (use the table in `references/beginner-walkthroughs-chat.md` section 2).
4. Walk them through `references/beginner-walkthroughs-chat.md` sections 1 and 3: download, unzip, move to Documents, see hidden files.
5. **Offer the `.env` walkthrough now** (section 4), only if they want it and have a key. **Never ask for the key in the chat.** You cannot see their file; give them the self-check.
6. **Checkpoint:** "Do you have the folder, and can you see inside? Say go and I will start asking about your business."

## Stage 2: Questions

Ask `references/intake-sheet.md` **one group at a time**. Skip what Stage 0 and 1 or the spec answered. Rules:

- "I don't know" or "later" is fine: record `unknown` and carry it as a `TODO(owner)`. **Never guess or invent** a fact, number, name, price, licence, address, testimonial or quote.
- Never ask for a key or password in the chat.
- The owner may upload writing samples or a style reference. Follow `references/style-reference-template.md` (distil, never paste a whole third-party article).
- Decide and note: business type; blog yes/no; service pages yes/no (`service_pages: NOT USED` for a nonprofit or portfolio); voice and **humor level** (none, light, playful); image source default and rules by context; special content rules; hosting (Render Static Site by default).
- At the end, read back a summary (every `unknown` listed) and ask them to confirm or correct.

## Stage 3: Project files (written here, not yet downloaded)

Work in a folder in the sandbox named `incoming/`. Create, **only from the owner's answers or spec**:

- `incoming/CLAUDE.md` from `references/claude-md.template.md`, with the **Stack adapter** filled from `references/framework-adapters.md` for the chosen framework (the values must match the starter you already made: images folder, blog folder, output folder). Leave `{{placeholder}}` only where the answer was `unknown`.
- `incoming/references/` : the six files from `references/reference-templates/` (humor from the chosen level), filled only from what the owner supplied; plus any style guide.
- `incoming/keywords.csv` : header only (`keyword,volume,difficulty,intent,status,notes`) or seeded from their list with `status: unverified`.
- `incoming/docs/intake.md` (answers only, no secrets) and `incoming/docs/on-page-seo-checklist.md` (copy from `references/`).

Then show a **plain-language summary** of each file and the list of `TODO(owner)` items. Offer to show or change any file. **Never overwrite** what the owner has agreed without asking.

## Stage 4: Safety check (on a copy, here)

Assemble a **copy**: the starter folder from Stage 1 plus the contents of `incoming/` placed in their right spots. Run `git init` in that copy (it is in the sandbox) and `bash <skill>/scripts/verify-setup.sh <copy> <astro|nextjs>`. Show the full output. Fix every FAIL and explain every WARN in plain words.

Say clearly: **this checks the files I made, not your computer.** Their real folder can be checked later with Claude Code's `site-setup audit`. The script never prints key values.

## Stage 5: STOP. What the owner does now

Give a plain checklist:

- Put **logos and brand files** and approved **photos** in the right folders of their project folder (no receipts, bank screenshots, ID cards, chat screenshots or medical documents; no videos, which are embedded from YouTube or Vimeo instead).
- Type **keys** into their `.env` themselves (section 4 of the walkthroughs).
- Add the **keyword export** to `keywords.csv` if they have one.
- Tell you when done ("go").

**Wait for "go".**

## Stage 6: Photo check (optional, by upload)

Offer: "If you would like, upload your photos here and I will look for anything private (receipts, IDs, screenshots, medical papers, account numbers) and tell you which to leave out." Look at each one, report, **keep nothing**, change nothing. Remind them photos need consent from everyone who appears.

## Stage 7: Design direction and build plan

1. **Design direction.** Use the spec or a reference screenshot or link if there is one (describe its system in words; never copy a third party's logo, copy, photos or fonts). If not, follow the **design fallback** in `references/build-prompt-template.md` section 3: two or three simple directions from their mood words, contrast computed, one recommended, owner picks or tweaks. Save to `incoming/docs/design-direction.md`.
2. **Build plan** in plain words: file tree, pages with copy status (FIXED, DRAFT or PLACEHOLDER), components, how visitors contact or act, open questions. Save the **approved** plan to `incoming/docs/build-plan.md`.
3. **Stop and wait for approval.**

## Stage 8: Build prompt and the final download

1. Check the **minimum** in `references/build-prompt-template.md` section 2. If something is missing, ask.
2. Fill the skeleton in section 5 of that template from the spec, `CLAUDE.md`, `docs/intake.md`, the plan and the design direction. Never invent. Unknowns become `TODO(owner)` with the placeholder system.
3. **Put this block at the very top of the prompt, before READ FIRST** (the project files arrive in an `_incoming` folder):

   > STEP 0: MOVE THE INCOMING FILES. This project folder contains a folder called `_incoming/`. Move its contents into place: `_incoming/CLAUDE.md` to `CLAUDE.md`; `_incoming/keywords.csv` to `keywords.csv`; `_incoming/references/*` to `references/`; `_incoming/docs/*` to `docs/`. If a file already exists in the destination, do NOT overwrite it: tell me and keep both. Show me the final folder tree, and delete `_incoming/` only after I confirm.

4. Save the prompt as `incoming/docs/BUILD-PROMPT.md`. Also write `incoming/MOVE-ME.md`: a short table (file, where it goes) and "If you are not using Claude Code, drag each file to its place yourself."
5. **Verify once more** (Stage 4 method) on a fresh assembled copy that includes everything.
6. **Pack:** `python3 <skill>/scripts/site_tools.py pack incoming <project>-project-files.zip _incoming`. The ZIP contains **no `.env` and no `.gitignore`**, so it cannot touch the owner's keys.
7. **Offer the ZIP as a download** and **show the full build prompt in a code block** so it can be copied.
8. Explain, plainly: unzip it; **drag the whole `_incoming` folder into the project folder** (`references/beginner-walkthroughs-chat.md` section 5); then open the project folder in **Claude Code** in a new chat and paste the build prompt. If they do not use Claude Code, `MOVE-ME.md` shows where the files go, and a developer can use the prompt.
9. Show the list of `TODO(owner)` items still needing their input.

The skill ends here.

## Hard rules

- Never invent facts, statistics, names, dates, addresses, prices, licences, testimonials, quotes, partners or Scripture.
- Never ask for, print, store or repeat an API key or password. Never put a secret behind a `NEXT_PUBLIC_` or `PUBLIC_` name. Never include a filled `.env` in any ZIP; only the Stage 1 starter holds an **empty** `.env`.
- Never claim to have created, opened, moved or checked anything on the owner's computer.
- The final project-files ZIP unpacks to `_incoming/` only. Never design a ZIP that would replace the owner's existing folders.
- Follow the owner's build spec over this skill's defaults. If they conflict, ask.
- Never write the build prompt before the owner has approved the design direction and plan.
- Stop at every gate and wait for "go".
