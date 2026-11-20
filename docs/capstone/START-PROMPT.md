# Start prompt: paste this into a NEW chat in the project folder

(Everything inside the box below is the prompt. Before you paste it, make sure these are in your project folder: `CLAUDE.md`, `references/`, `keywords.csv`, `docs/capstone-build-spec.pdf`, `.claude/skills/`. They are all in `seo-skills-kit.zip`.)

````
You are helping me build the Capstone Foundation website in this folder (the project root). I am not technical, so explain each step in plain words before you do it. Work in STAGES. Do not start the next stage until I say "go".

READ FIRST, IN THIS ORDER
1. CLAUDE.md (project rules, stack, folder map, gates, and the conflicts already resolved)
2. docs/capstone-build-spec.pdf (the full build specification: all copy, routes, design tokens and acceptance criteria; it is canonical for copy and design)
3. docs/cross-check.md (open decisions I still need to confirm; do not decide these yourself)
4. references/ (voice.md, tone.md, humor.md, sparkle-text.md, opinions.md, stats.md, stories.md: the voice, the sparkle writing style and the approved facts) and keywords.csv. They are used later by the SEO skill.
5. docs/video-links.md (the videos to embed; you will create it in step 1C from the VIDEOS TO EMBED section below)
Do not write any site code yet.

=== VIDEOS TO EMBED ===
These four YouTube Shorts are on Capstone Foundation's own YouTube channel. They must be EMBEDDED in the site where they fit. Never download them and never commit video files. The video ID is the part after /shorts/ (ignore the ?si= tracking part of my links). Watch URL pattern: https://www.youtube.com/shorts/<ID>

 1. Rw5ewqXteY8 - "Capstone Foundation: Changing Lives Through Education" - 0:30 - Scholarship Scheme overview. Suggested home: Programs > Scholarships (could also be the one featured video on Home).
 2. jSiSsNCmEkc - "Life as a Widow in Nigeria Today: Their Stories, in Their Own Words" - 2:45 - Voice of the Widows Forum members speaking. Suggested home: Programs > Widows Empowerment.
 3. MGx__JGb-wY - “My Daughter Got a Scholarship” | A Widow's Story of Hope - 1:10 - a widow's testimony about the Scholarship Scheme. Suggested home: Programs > Scholarships and/or the Testimonials section.
 4. 6ah3juz598Y - "Voice of the Widows Forum: Monthly Review & Impact Update" - 0:36 - highlights from a monthly forum meeting. Suggested home: Programs > Widows Empowerment.
(My original links: youtube.com/shorts/Rw5ewqXteY8, youtube.com/shorts/jSiSsNCmEkc, youtube.com/shorts/MGx__JGb-wY, youtube.com/shorts/6ah3juz598Y)

How to embed them (build ONE reusable VideoEmbed component):
- Data lives in src/data/videos.ts: id, title, caption, page, slot, approved. approved is false by default, and a video renders only when it is true.
- Vertical 9:16, centred, maximum width about 360px, inside a fixed aspect-ratio box so there is no layout shift.
- Click to load. On page load show only a flat poster card (12px radius, 1px #EBEBEB border) with a large flat brand-green play button (at least 56px) and the video title as text below. Only when the visitor clicks does it swap for an iframe from https://www.youtube-nocookie.com/embed/<ID>?autoplay=1&rel=0&playsinline=1 with a title attribute (the video title), allow="encrypted-media; picture-in-picture; fullscreen", allowfullscreen, and referrerpolicy="strict-origin-when-cross-origin". No YouTube code or cookies may load before the click. This protects Lighthouse 95+ and visitor privacy.
- It must work without JavaScript: the play button is a normal link to https://www.youtube.com/shorts/<ID> (new tab, rel="noopener"), and a visible "Watch on YouTube" text link is always there. Keyboard accessible, visible focus, accessible name "Play video: <title>".
- Poster: do NOT hotlink YouTube thumbnails. Use a flat #EBEBEB poster, or a still from my own photos (images-incoming/, named video-<ID>.jpg) through the normal image pipeline.
- Placement: propose a video slot map (page, position, which video, caption) together with the photo slot map, and WAIT for my approval. Default: each video appears once. Videos may also be embedded in Stories (MDX) when relevant and approved.
- Consent and privacy: these videos show real people. Before any video goes live, ask me for each one: who appears, that they consented to appear on this website, and that no money amounts, children's surnames, diagnoses or case details are shown or spoken. Keep approved false until I say yes.
- Copy rule: do NOT copy text from the YouTube titles or descriptions into page copy (they contain wording and claims that are not in the spec). Page copy stays word for word from the spec. Use a title only as the accessible title and as a caption I approve.
- Ask me whether to add VideoObject structured data (optional, only with the real title, upload date and duration).

=== STAGE 1: CHECK, THEN CREATE THE FOLDERS (no site code) ===

1A. Check and report back to me in a short table:
   - Node.js version (need 20 or higher) and npm version
   - git installed, and whether this folder is already a git repository (ask before running git init)
   - Which skills you can see (I expect: blog, service-page)
   - That these exist: CLAUDE.md, docs/capstone-build-spec.pdf, docs/cross-check.md, references/ (7 files, including sparkle-text.md), keywords.csv
   - Whether any logo files, photos or video files are already in this folder, and where (video files must not be in the project; the videos are embedded from YouTube)
   Stop and tell me if anything is missing or wrong.

1B. Show me the folder tree below, explain in ONE line what each folder is for, then create the ones that do not exist yet. Put an empty .gitkeep file in each empty folder so it is not lost.

   (project root)
   ├── docs/                        spec PDF, cross-check, video-links.md, SEO guide and kit
   ├── references/                  voice, tone, humor, opinions, stats, stories
   ├── images-incoming/             I drop my approved photos here (never committed)
   ├── public/
   │   └── brand/                   the two logo files
   ├── scripts/                     process-images.mjs and fetch-unsplash.mjs (written later)
   ├── server/                      README only: the future donation back end plan, no code
   ├── src/
   │   ├── assets/images/           processed images (created by the pipeline)
   │   ├── components/              Header, Footer, Hero, Band, MediaBlock, ProgramCard, StatStrip,
   │   │                            Testimonial, CtaBand, PlaceholderCard, Seo, DonationPanel, VideoEmbed
   │   ├── config/                  site.ts (contact, social links, the hidden-section flags)
   │   ├── content/stories/         the blog (MDX)
   │   ├── data/                    images.ts, testimonials.ts, videos.ts, published.json
   │   ├── layouts/
   │   ├── pages/                   (routes are created in Stage 4)
   │   └── styles/                  global.css
   └── .claude/skills/              already provided (blog, service-page)

   Do NOT scaffold Astro yet (no package.json, no npm install). Only folders and the small files below.

1C. Create these files:
   - .gitignore containing at least: .env, node_modules/, dist/, .astro/, images-incoming/*, and a .DS_Store line. Keep images-incoming/.gitkeep tracked.
   - .env.example listing: PUBLIC_SITE_URL=   PUBLIC_INDEXABLE=false   PUBLIC_API_URL=   UNSPLASH_ACCESS_KEY=
   - .env with the same keys and EMPTY values, except PUBLIC_INDEXABLE=false. I will type my own Unsplash key into .env myself. NEVER ask me to paste a key into this chat.
   - server/README.md with one short paragraph: "Phase 2 donation back end plan. No code yet." plus the planned endpoints from the spec.
   - A short README.md placeholder (it is completed in Stage 4).
   - docs/video-links.md containing the VIDEOS TO EMBED section above, exactly as written (if the file already exists, keep it and tell me if it differs).
   - Add a short "Videos" section to CLAUDE.md that points to docs/video-links.md as the source of truth (only if CLAUDE.md does not already have one).

1D. VERIFY everything and show me the proof:
   - Print the final folder tree.
   - Run `git check-ignore -v` on .env, images-incoming/test.jpg, node_modules and dist to prove they are ignored.
   - Confirm every folder in the tree above exists, and list anything that does not.
   - Confirm .env exists, is ignored by git, and contains no secret.

1E. STOP. Then give me a plain checklist of exactly what I must do now:
   - Put the two logo files in public/brand/ and rename them to capstone-logo-green-on-white.jpg and capstone-logo-white-on-green.jpg (tell me which of my files is which if you can see them).
   - Put the photos I have approved into images-incoming/ (not straight from Google Drive; no receipts, bank screenshots, ID cards, chat screenshots, medical documents or school-fee slips; no videos). These are my own photos of Capstone's work, and they are the ONLY source for anything about Capstone's work, testimonials and projects.
   - Optional: add my Unsplash Access Key to .env (UNSPLASH_ACCESS_KEY=...). Access Key only, never the Secret Key.
   - Tell me what to type when I am done.
   Wait for me to say "go".

=== STAGE 2: CHECK WHAT I UPLOADED (no processing yet) ===
   - List every file in public/brand/ and images-incoming/ with its size. Check that the logos are 960 x 540 and the names are right.
   - Look at each photo. Flag anything that looks like a receipt, bank screenshot, ID, chat screenshot, medical document, school-fee slip, or anything showing an account number, and tell me those will be skipped. Flag very large files, duplicates and unreadable files.
   - Tell me how many photos look usable. Do not move, edit or delete anything.
   - Videos: for each of the 4 videos, ask me (a) who appears, (b) whether they consented to appear on this website, (c) whether any money amounts, children's surnames, diagnoses or case details are shown or spoken, and (d) which page I want it on (use the suggested homes as a starting point). Record my answers in docs/video-links.md. Keep every video unapproved until I say yes.
   Wait for "go".

=== STAGE 3: PLAN (the spec's "How to work", step 1) ===
   Reply with: the full file tree you plan to create, the component list (including DonationPanel and VideoEmbed), a proposed VIDEO SLOT MAP (page, position, which video, caption) and any questions you have. You MUST include question K from docs/cross-check.md (the spec's Psalm 68:5 and James 1:27 lines are not NIV wording; ask me whether to switch them to the NIV text or keep the spec wording). Do not change any fixed spec copy until I answer. Wait for my approval.

=== STAGE 4: BUILD ===
   Follow the spec's build order: scaffold and config; design tokens and layout; Home; About; Programs; Get involved; Donate and Contact; Stories; SEO and structured data; final checks. After EACH step run the build and tell me in 2 to 3 sentences what is done and what is next. When the image pipeline is ready, process my photos, then propose the slot map (home hero, About, one per program page, Get involved) and WAIT for my approval before placing any photo or video. Build the VideoEmbed component and src/data/videos.ts as described in VIDEOS TO EMBED, and place only the videos I have approved. Use the copy in the spec word for word. Use no invented facts.

=== STAGE 5: ACCEPTANCE ===
   Check the build against the spec's "Done means" list and report pass or fail for each item with proof (Lighthouse 95+ on mobile for all four categories on the built site; 360, 768 and 1280 px widths). For videos also prove: no iframe and no request to youtube.com or youtube-nocookie.com before a click; the 9:16 box causes no layout shift; the play link and the "Watch on YouTube" link work with JavaScript off; every embedded video is one I approved.

=== STAGE 6: SEO (ONLY WHEN I SAY SO) ===
   Do not run anything from the SEO skill until I ask. When I do, run the `blog` skill for the Stories section as set out in CLAUDE.md (stack adapter, new posts as drafts, humor none, the sparkle style in references/sparkle-text.md, Scripture in the NIV verified exactly). Show me every Unsplash photo you pick. Do not run `service-page` on this site.

RULES THAT NEVER CHANGE
- Never invent facts, statistics, names, dates, addresses, quotes, testimonials, partners or Scripture. Quote Scripture only in the NIV, copied exactly from a verified source and cited.
- Images: my own photos (images-incoming/) are required for anything about Capstone's work, testimonials and projects. Unsplash may be used elsewhere when needed (people are allowed in general-topic Stories). In pages or stories about Capstone's work, Unsplash is for atmosphere with no people only. Never present an Unsplash photo as Capstone's own people, work or testimonial.
- Voice: the spec voice (hopeful, openly Christian, inspirational, short sentences, plain words) plus the sparkle style for Stories and new copy only. Fixed spec copy is never sparkled. No humor.
- Videos are only embedded from YouTube (click to load, youtube-nocookie.com), never downloaded or committed, and only the ones I have approved. Never use YouTube title or description wording as page copy.
- Never publish money amounts, receipts, bank screenshots, diagnoses, case details or children's surnames.
- Never put a secret in the repository or the browser.
- If something is not covered, ask me before adding it.

Begin with Stage 1A now.
````
