# SEO With Claude Code: Website Creation and Optimization Guideline

**Source:** Jono Catliff, "Claude Code SEO: How I Got 50,000 Clicks Per Month (Steal This)" (1h 08m)
- YouTube: https://youtu.be/4IyJm1i__ag
- The Skool lesson you shared (`.../classroom/6ca29126?md=33b841283b354e589ef554a980cf7407`) is the free blueprint linked from this video's description.

**How this was built:** from the video's full transcript, the creator's chapter timestamps and the video description. Nothing here is paraphrased from a summary alone.

**Labels used below:**
- Plain text means the video said it.
- **[Note]** means my own addition or caution, not from the video.
- **[Not in video]** means the video points to a resource, but the content isn't shown.

---

## 0. What you are reading

The video teaches **one system** with two money-making tactics, built and optimized entirely through Claude Code:

1. **Blog posts at scale.** These build topical authority and raise trust in the whole domain.
2. **Service pages.** These are the pages meant to turn visitors into leads and customers.

Everything else (keywords, on-page SEO, technical SEO, off-page SEO, deployment, post-launch tools) supports those two tactics.

The creator's claimed results: $500K+ earned at a previous company, and ~50,000 clicks/month (~1,500/day) from one site. He says it took 4–6 years to learn. These are his claims and I haven't verified them.

---

## 1. Core principles

1. **Ranking position decides traffic.** The video cites ~40% of searchers clicking result #1 and ~20% clicking #2, then a steep drop-off.
2. **AI SEO is just SEO.** If you rank well in Google, you will be surfaced in ChatGPT, Perplexity, Claude and similar tools. Their first step is to search the web as a person would. Don't chase AI-search hype separately.
3. **Choose the right strategy early.** A wrong SEO strategy usually shows up 2–4 years later. Validate with data (keyword tool, Lighthouse, Search Console), not guesses.
4. **Google must be able to crawl your site.** If it can't find or fully read your pages, nothing else matters. Static generation, sitemap and robots.txt exist for this reason.
5. **SEO is a black box.** There are 200+ rumored ranking signals (dwell time, bounce rate, scroll depth, click-through rate, content quality and depth). Nobody outside Google knows the weights. The simple approach is to reverse-engineer what Google wants.
6. **What Google wants:** it makes money from ads, so it wants people to keep coming back. People come back for **high-quality content**, so content quality is the number one lever.
7. **Content must be enjoyable.** If people bounce, you won't climb. SEO is a balance: SEO markers *and* readable, entertaining content. Never let optimization turn a post dry.
8. **Your business is a funnel.** SEO gets clicks. Then the page must convert visitors into leads, and you must close leads into customers. Improve each stage separately.
9. **Pace yourself.** Claude can produce content far faster than is safe to publish. Dumping hundreds or thousands of pages at once risks Google flagging the spike.
10. **Don't buy cheap backlinks.** Off-page shortcuts are the riskiest part of SEO (see section 11).

---

## 2. The four SEO buckets

| Bucket | What it covers | Who normally does it |
|---|---|---|
| **Keyword research** | Finding keywords you can realistically win | You, with a keyword tool |
| **On-page SEO** | Everything you write and how you structure and publish it | Claude, via checklist |
| **Technical SEO** | How the site is built: load speed, Core Web Vitals, crawlability | Claude, via Lighthouse loop |
| **Off-page SEO** | What the rest of the internet says about you, which determines trust and authority | Outreach (optional, risky) |

His point: big competitors like Homestars likely have whole teams doing on-page and technical SEO daily. One person with Claude Code can reproduce that work.

---

## 3. Tooling and accounts

| Tool | Purpose | Notes |
|---|---|---|
| **Claude Code** | Builds the site and runs every prompt | The video runs it inside Antigravity. **Your plan: run Claude Code directly** in a terminal inside the project folder. No editor is required. |
| **Semrush** | Keyword research, competitor keywords, site audit, backlink data | Free trial. Creator has used it 4–5 years. The "Keyword Magic Tool" is the main feature. |
| **Dribbble** | Design reference screenshots | Free. Prevents "AI slop" design. |
| **Unsplash API** (or your own images) | Free images for posts | The video uses Pexels. **Your choice: Unsplash**, with an Access Key from a free developer app. Or skip the API and put your own images in an `images/` folder, chosen per run. |
| **GitHub** | Stores the code | Make the repo private. |
| **Render** | Free static hosting and deploy | **Your choice instead of the video's Vercel.** Deploy as a **Static Site** (build `npm install && npm run build`, publish directory `out`). Custom domains are added in the Render dashboard. |
| **Google Business Profile** (video says "Google My Business") | Free local listing | Described as the lowest-hanging fruit for clicks. |
| **Google Search Console** | Tracking, sitemap submission, request indexing | |
| **Google Analytics** | Visitor behaviour | |
| **Chrome DevTools, Lighthouse tab** | Performance audit | Built into Chrome. |
| **Make.com** | Optional automation | Appears in his related videos, not in this one. |

**[Decision]** You chose to work in Claude Code directly, so Antigravity is dropped. The video description notes Antigravity 2.0 removed extensions (including Claude Code) and recommends VS Code instead, but the workspace is only a window around Claude Code. Every step in this guideline works the same from the terminal. Where the video says "attach a screenshot" or "drag the file into Antigravity", drag the image into the Claude Code session or give it the file path.

---

## 4. Step 1: Set up the project

1. Open Claude Code directly in your terminal (no Antigravity or VS Code needed).
2. Create an **empty folder** for the project. Every Claude Code project lives in a folder. The video names it "SEO brief".
3. Add **one file: `CLAUDE.md`**. The video compares it to training a new employee: how to behave and the standard operating procedures.
   - The creator supplies a ready-made `CLAUDE.md` for web apps in the free Skool blueprint. **[Not in video]**: its contents aren't shown, only that it exists.
   - It tells Claude to build the site with **static site generation (SSG)**, which is a requirement.
4. Open Claude from the extension icon and send the site-building prompt.

### The site-building prompt (as described)

> Can you please build out a beautiful website for me with the following pages: a homepage, an index page for my blog posts, an index page for my service posts, and that's it. I'm going to attach a screenshot of the design I'm looking for. Please clone or copy that exact design when building out the website pages.

- Build **only three pages** to start: **homepage, blog index, service index**.
- A **blog index** lists all blog posts (1 post → 1 listing, 100 posts → 100 listings).
- **Always attach a design screenshot.** Claude output looks generic ("AI slop") without a reference. Find one on Dribbble (e.g., search "plumbing website" for your niche) and attach it with the **+** button, then upload from computer.
- The site previews at a **localhost link** shown in the tool.
- He claims this takes seconds, versus 4–5 hours on WordPress (hosting, DNS, editing).

---

## 5. Step 2: Make sure the site is built for crawling (rendering)

Three build types exist. The video's pizza analogy:

| Type | Analogy | SEO effect |
|---|---|---|
| **Static Site Generation (SSG)** | The pizza is already made. Hand over a slice instantly | **Wanted.** Google finds the finished page instantly. |
| **Server-Side Rendering (SSR)** | You order and wait for it to be cooked | Slower and not optimal. |
| **Client-Side Rendering (CSR)** | You make the pizza yourself | Google may get almost nothing back and can't rank it. |

- Google ranks only what it can crawl. "You can spend 10 years on SEO, it doesn't matter" if the site can't be crawled.
- The provided `CLAUDE.md` forces SSG. **If you write your own, state this as a hard requirement.**
- The video's stack is Next.js with static generation (it deploys on Vercel with the Next.js preset). **You deploy on Render instead**, so the site is built with `output: 'export'` and hosted as a Render Static Site.

---

## 6. Step 3: Keyword research (the foundation)

### Why not just ask Claude

Asking Claude "give me 20 keywords for plumbing" gives guesses. Claude doesn't know monthly search volume or keyword difficulty. Use a standalone SEO tool (Semrush) for real data.

### Procedure in Semrush

1. Go to **SEO → Keyword Magic Tool**.
2. Enter a **root keyword** (e.g., `plumber`). You get a huge list (~1 million in the example) of variations such as "plumber near me" and "emergency plumber".
3. Apply filters:
   - **Keyword difficulty ≤ 30.** A score around 2/10 can reach positions 1–3 very quickly; he says he has seen this "multiple times".
   - **Monthly volume ≥ 100.** Skip keywords with a handful of searches.
   - **Intent: informational** (for blog posts). The example filter took ~1M down to ~6,000.
4. **Hand-pick** from what's left. Skip:
   - Other people's businesses or brand names (his example: "Zeke the Plumber").
   - Terms for people who want to start their own company or become a plumber (competitors, not customers).
   - Irrelevant terms (his example: "plumb bob").
   - **Keep** terms where the searcher could become a paying customer, such as "plumbing installation", "plumber fix shower" and "plumber plumbing drain washing machine".
5. Add selected keywords to a **Keyword List** (his is called "plumbing keywords"). Target **a couple hundred to a couple thousand** keywords over time.

### Extra sources of keywords

- **Questions tab** in Keyword Magic Tool. Great blog topics.
  - "How much does a plumber cost?" is a good pick because the searcher is a potential customer.
  - "How long does it take to become a plumber?" is a competitor audience. Skip it, although you could target it.
- **Adjacent / top-of-funnel topics.** Same audience, earlier in the buying journey (e.g., "best water softener 2026", "tankless vs tank water heater", "signs you need a new water heater"). These capture prospects before they urgently need a plumber, so they remember you later.
- **Competitor keywords.** Enter a competitor domain in Semrush, see what they rank for, and add those keywords to your own list.

### Intent explained (from the video)

- **Informational**: wants to learn ("how much does a plumber cost").
- **Commercial / transactional**: wants to buy ("buy Nike shoes" returns e-commerce pages, not blogs).
- Blog posts target informational intent. Service pages target money keywords (section 8).
- "Niche difficulty varies. Winning keywords aren't always easy to find."

### Export to Claude Code

1. Open the keyword list → **Export as CSV**.
2. Drag the file into the project folder and **rename it `keywords.csv`**. Skills and prompts refer to this file by name.

---

## 7. Tactic 1: Blog posts at scale

### 7.1 First draft prompt

> Can you please create a blog post for me about [primary keyword]? That's the keyword I want you to use, and I also want you to create a keyword cluster. That keyword cluster can either be from common keywords in the keywords.csv file or you can just make it up. Please add in images (from Pexels in the video; in this kit: Unsplash via the API key in `.env`, or my own images from the `images/` folder, chosen per run).

**Rule of thumb: one keyword = one blog post.** Every keyword in `keywords.csv` becomes its own post.

### 7.2 Images (video: Pexels; this kit: Unsplash or your own images)

The video gets free images from the Pexels API and pastes the key into a **`.env` file**. This kit works two ways, chosen per run:

1. **Unsplash API.** Create a free Unsplash developer app, copy its **Access Key** (never the Secret Key), and put `UNSPLASH_ACCESS_KEY=your_key` in `.env`. Unsplash's rules: images are **hotlinked** from the URLs the API returns (not downloaded and self-hosted), a download ping is sent when an image is chosen, and a visible credit ("Photo by [name] on Unsplash", with UTM links) is shown. Demo apps are limited to 50 API requests per hour.
2. **Your own images.** Drop images into an `images/` folder in the project root. Claude looks at them, picks the fitting unused ones, and saves optimized copies (never touching your originals). No key and no attribution needed.

You tell Claude which one per run ("blog images=unsplash", "blog images=local", "blog images=none"), or set a default in `CLAUDE.md`.

**[Note]** Add `.env` to `.gitignore`. The video shows its own key on screen, and he jokes about it. If the repo is ever public or shared, the key leaks.

### 7.3 Keyword clusters

- Don't rank for one keyword per page. Rank for **a root keyword plus many secondary and tertiary related keywords** on the same page.
- His example: root "how to unclog a drain" with cluster terms like unclog kitchen sink, unclog bathroom sink, drain won't drain, slow drain sink, home remedy clogged drain, what dissolves hair in drain.
- A single post can rank for 50 to 100+ keywords, many you didn't know about.
- Clusters can come from `keywords.csv` or be generated.

### 7.4 The first draft is not enough

He calls it "crap" and warns that most people stop here and never get results. Typical AI output opens with: "In today's fast-paced world…". Nobody reads that, and bounce rate hurts you.

### 7.5 Fix 1: Teach Claude your voice (reference files)

Give Claude reference files so every post sounds like you. In the video these live in a **`references` folder** with separate files for:

| File | Contains |
|---|---|
| **Voice** | How you write and speak |
| **Tone** | Your overall feel |
| **Humor** | Your type of jokes, with examples |
| **Opinions** | Your stance on topics in your industry |
| **Stats** | Real numbers: drains unclogged, years in business, etc. |
| **Stories** | Anecdotes from real jobs and things you tell clients |

**How to fill them:**
- Collect your own writing: transcripts, phone calls, videos, emails (Gmail), LinkedIn posts, any passages you like.
- Paste them in and ask: *"Please create these files and update them from these LinkedIn posts."*
- No samples yet? Find a writing style you love online and add it as a **humor reference** (he used a blog written in a "99 problems, but humor ain't one" tone).

**His humor rules, quoted as he showed them:**
- "Plumbing is boring, your job is to make it more fun. Every blog post should be funny, this isn't optional."
- Opening rule: if the **first 50 words** don't land at least one **dad joke, self-aware wink or parenthetical aside**, rewrite them.
- Persona: "We are not a brochure, we are a guy at the pub who has had one beer and is now explaining how the toilet works."

Swap "plumbing" and the dad-joke persona for your own industry and brand voice. The principle is **personality is not optional.**

### 7.6 Fix 2: Steal the winning format from Google's top results

For the primary keyword:

1. Search it on Google.
2. Take the **top 3 organic blog results**, excluding Reddit and similar forums.
3. Have Claude analyze what they have in common: **page length, keyword usage, H2 count, images, topics covered, format**.
4. **Average the three** (word count, number of H2s, images, etc.) and use that as the target structure.
5. Write your own post to that structure, with your voice, humor, opinions, stats and stories.

The combined prompt does all of this at once: rewrite using the reference files, research the keyword on Google *before* writing, copy the format, length and topics that are winning, and still keep the humor. (**[Not in video]**: the exact prompt is in the Skool blueprint.)

**Before and after (his example):**
- Before: "In today's fast-paced world, maintaining a functional household…"
- After: "Your toilet has been hissing for longer than most celebrity marriages. It's 11:00 p.m., you're Googling…"

---

## 8. Tactic 2: Service pages

### 8.1 What they are

- Landing pages for **money keywords**: queries where the searcher wants to hire someone ("plumbing Toronto").
- Goal: **get the visitor to fill out the form** so you can call them and close the deal.
- Blog posts and service pages work together:
  - Blogs build **topical authority** and **domain trust**, and pass link equity to service pages.
  - His metaphor: **"a rising tide lifts all boats."** Blogs raise the tide and service pages are the boats that earn money.

### 8.2 The zipper method

Two sides of the zipper joined together:

- **Services:** emergency plumber, drain cleaning, hot water repair, leak detection…
- **Locations:** Vancouver, Toronto, Montreal, Edmonton… (**municipalities** work too. If you serve one metro area, use its municipalities).

Zip them: *emergency plumber Toronto, emergency plumber Vancouver, drain cleaning Toronto, drain cleaning Montreal*, and so on.

### 8.3 Don't overdo it

- Service pages have very similar content, unlike blogs, which are each different.
- **Too many near-duplicate pages can be a negative signal to Google.**
- No objective cap. His view: **never thousands, probably not even multiple hundreds.** Be tasteful.

### 8.4 Finding service keywords in Semrush

1. Keyword Magic Tool, root keyword (e.g., `plumbing`).
2. **Sort by cost per click (CPC).** High CPC means advertisers pay a lot for the click, which means these are money keywords.
3. Caveat: the very top CPC values (e.g., $700) are bad data. **Typical real CPC is about $3 to $20.**
4. Look for the **service + city** or **city + service** pattern. He noted many location terms in the results.
5. Add chosen keywords to a separate list (e.g., "service pages"), export CSV, drag into the project and rename it **`service-keywords.csv`**.
6. **[Not in video]** Which Semrush filters beyond CPC he applies for service keywords. He says you will probably already know the service keywords for your own business.

### 8.5 Service page prompt (as described)

> I want you to build out a page with the primary keyword from [service keywords file]. This is a landing page specifically for [city and service]. The landing page should look pretty much the same as the homepage.

### 8.6 Conversion rule: reuse your winning landing page

- Making the service page look like the homepage is **his habit, not a requirement.**
- The real principle: **test landing page variations and reuse the winner everywhere.**
  - He ran **Google Ads** to test 5–10 landing page variations.
  - His best page reached a **~20% conversion rate** (1 in 5 visitors).
  - Then he applied that winning layout across all service pages.
- A new site will find it hard to rank service pages at first. Blog posts, good on-page SEO and technical SEO help lift them.

---

## 9. On-page SEO (the checklist approach)

### 9.1 Concept

- He says on-page SEO has **80+ signals**, and doing it manually would take a team, or "6 to 12 hours" just to explain.
- The method: **paste the whole checklist into Claude Code once**, and have it update the page. The checklist and prompt are in the free Skool blueprint. **[Not in video]**: the full list isn't shown.

### 9.2 Items he explicitly mentioned or showed

| Item | Detail |
|---|---|
| **External links** | 2 to 3 per post, pointing to relevant outside sources |
| **Internal links** | 3 to 5 per post, linking to your other posts and pages. Claude finds relevant ones itself |
| **Primary keyword in the first 100 words** | He showed this being checked |
| **FAQ questions** | 4 to 8 questions per blog post |
| **Exactly one H1** | Headings can be H1, H2, H3, and so on, but only one H1 per page |
| **Meta title** | The blue clickable title in search results. Not visible on the page |
| **Meta description** | The gray text under the title in search results. Not visible on the page |
| **Open Graph (OG) tags** | Viewable in the page's HTML (DevTools → Elements, search for `og`) |

**How to see the meta title and description:** in Chrome, three-dot menu → More tools → Developer tools → Elements tab, then search for `og`.

### 9.3 The update prompt (as described)

> Can you please update the blog post with the on-page SEO checklist items from this [paste]. Add all the following items, but still maintain the voice and style of the blog post.

**Key instruction: "still maintain the voice and style."** Content is still king. Don't let optimization drain the humor and personality.

**Do this for every page**, both blog posts and service pages.

### 9.4 Verify, don't trust

His cross-check after the run:
- Internal and external links are present and relevant.
- Primary keyword appears in the first 100 words.
- Meta title and description exist and read well.

---

## 10. Technical SEO

Technical SEO is how the site is built. It used to require coding experience.

### 10.1 Three files and tools

1. **`sitemap.xml`**. Tells Google which pages exist so they can be indexed. If Google doesn't know a page exists, it can't rank.
2. **`robots.txt`**. Tells crawlers which pages they may or may not crawl.
   - Allow everything except pages you don't want ranked, such as an **admin login or dashboard**.
   - Add anything else you want excluded.
3. **Google Lighthouse**, the performance report. Scores four areas out of 100: **SEO, Accessibility, Best Practices, Performance (speed)**. Aim for **100/100 on all**.

### 10.2 The Lighthouse loop

1. In Chrome: three dots → More tools → Developer tools → click the double arrows `>>` → **Lighthouse** → analyze page load.
2. His first result: SEO 92, Best Practices 100, Accessibility 96, **Performance 53** (slow).
3. **Expand every failing section** in the report so all details are visible (do this for SEO too).
4. **Copy the whole report** and paste into Claude Code:

> Here's my Lighthouse report. Can you please optimize it so that I have a 100% score across all areas: performance, accessibility, best practices, SEO. Can you also generate the robots.txt file and the sitemap.xml file?

5. Re-run Lighthouse. His second result: **100 / 100 / 100 and 96**. He said a 96 is fine.
6. **If it isn't 100, paste the new report and repeat.** You can go back and forth until it's solved.

### 10.3 Notes

- Old-school fixes he lists (what you'd otherwise have to learn): render-blocking requests, legacy JavaScript, LCP request discovery, network dependency trees, reducing JavaScript execution time. Claude handles these.
- He also mentions **Core Web Vitals** and **load speed** as part of technical SEO.
- After the fix, check `/sitemap.xml` and `/robots.txt` on the site. **Sitemap** lists all pages. **Robots** shows what crawlers may scrape.
- **[Note]** Lighthouse scores vary by run and device (mobile vs desktop), so run it more than once and in both modes. Run it on the **deployed** site too, since localhost results differ.

---

## 11. Off-page SEO (optional and risky)

The creator says he **does not do this anymore** and isn't a full expert. It worked in about 2018 to 2020, but algorithm updates keep wiping out people who rely on it. He has seen businesses devastated.

### 11.1 What to avoid

- **Cheap backlink packages** ("100 backlinks for $5"). These are usually **PBNs (private blog networks)**: link farms, someone with thousands of websites linking to you for a fee.
  - Google detects them, penalties can be permanent, and you may be blacklisted from Google.
  - Even "legit-sounding" cheap SEO providers often do things that get you banned **about 3 years later**.
- **Hiring via Upwork "top 1%" backlinkers.** He asked for a past client's start and end dates, and the performance line **went down** between them. Always ask for before/after proof.

### 11.2 Four legitimate methods he lists

| # | Method | How it works |
|---|---|---|
| 1 | **Broken backlink swapping** | Use Semrush site audit on a competitor (e.g., Homestars). Find outgoing links on their pages that now return **404**. Contact them: "This link is broken. I have a page covering the same material. Want to swap?" Claude can build the replacement page. Takes time, no guarantee. |
| 2 | **Guest posting** | Search Google: `plumbing "write for us"` (with quotes for exact match). Write a post for them and include a link back to your site (a **backlink**). |
| 3 | **Journalist queries** | Journalists post questions, and you answer as the expert. They credit you with a backlink. The video calls it "Hero Journalism". See the note below. |
| 4 | **Paid quality backlinks** | Reputable domains that accept payment for a post or link. He names TechCrunch and Forbes but says he could be wrong about both. The value is "link juice": authority and trust passed to you. |

**[Note]** The service he's describing in #3 is **HARO (Help A Reporter Out)**. HARO has changed ownership and shut down at least once, so check what is currently available. Also, Google's guidance on paid links is that they should carry `rel="sponsored"` or `nofollow`. Paid backlinks carry risk. This conflicts with the video's own warning, so decide deliberately.

### 11.3 His bottom line

Off-page isn't required to succeed. His best advice: **find the golden-nugget keywords (low difficulty, decent volume, right intent) and rank for those.**

---

## 12. Bottling it into a reusable Claude Code skill

**Why:** the steps above take time. Package them so you type one word and get a fully optimized post.

### 12.1 The prompt used to create the skill

> Can you please create a skill for me called **blog**, where we automatically generate blog posts with all of the details that we just covered in this conversation:
> - Grab a keyword from `keywords.csv`
> - Create a keyword cluster
> - Publish the blog post and add pictures (Unsplash or the owner's own images)
> - Add in our writing style, voice, tone, humor
> - Optimize it for on-page SEO
> - For technical SEO, use the same standard template every time. Reuse the same page structure for every future blog post.

### 12.2 Using it

- **Refresh or start a new chat** so the skill is loaded, then type `blog`.
- The skill should **not reuse a keyword that was already used**.
- You can **schedule it to run automatically** (his example: 9:00 a.m. daily).
- Do the same for **service pages** (a second skill).
- His pitch: one person with this skill beats a 20-person team.

### 12.3 Publishing cadence (very important)

Do not publish in bulk. His suggested ramp:

| Day | Posts |
|---|---|
| 1 | 1 |
| 2 | 1 |
| 3 | maybe 2 |
| 5 | 3 |
| 8 | 4 |

Keep it reasonable. "Posting 1,000 blog posts a day is an easy way to get banned." Also: **"Don't dump 1,000 pages onto your website immediately."** He repeats this in the closing.

---

## 13. Deployment

Localhost means only you can see the site. To go live:

1. **GitHub** ("Google Drive for code"):
   - Create a **new repository**. Name it, set it **private**, create.
   - Copy the code shown, go back to Claude Code and say: *"Please upload my whole project here."*
2. **Render** (your choice; the video uses Vercel, and the steps are equivalent):
   - **New → Static Site**, connect GitHub, select the repo and branch.
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `out` (the folder Next.js writes when `output: 'export'` is set).
   - Click **Create Static Site**. Every push to the branch redeploys automatically.
3. **Domain (optional):** add a custom domain in the Render dashboard (Settings → Custom Domains) and set the DNS records Render shows, or buy one from a registrar such as Namecheap.

---

## 14. Post-launch checklist (his four remaining steps)

1. **Google Business Profile.** Free listing that appears in local results ("Toronto plumber"). He calls it the lowest-hanging fruit in 2026 for clicks and says it can bring thousands of clicks per month (his words: "I could be wrong"). This matters mainly for local, service-area businesses.
2. **Google Search Console.**
   - Add your Render URL (or custom domain) as a **URL prefix** property. Use the **full URL**, because a partial one throws an error.
   - **Verify ownership with the HTML tag method.** Copy the meta tag and tell Claude: *"Please add this meta tag to the website for Google Search Console verification, then deploy it live to GitHub and then Render."*
   - In the **Sitemaps** section, submit `sitemap.xml`.
   - **Request indexing:** paste a newly deployed page URL into the top search bar and request indexing. This can get a page indexed in about a day instead of weeks or months. It's limited to **roughly 10 requests per day**.
3. **Google Analytics.** Track visitor behavior.
4. **Test your landing pages.** Find what converts best, then apply the winning layout to all existing pages.

---

## 15. Master workflow (the video in 15 steps)

1. Open Claude Code in an empty project folder (no Antigravity needed).
2. Add `CLAUDE.md` (SSG required).
3. Find a Dribbble design reference, screenshot it and prompt Claude to build the homepage, blog index and service index.
4. Research keywords in Semrush (KD ≤ 30, volume ≥ 100, right intent). Export `keywords.csv`.
5. Build `references/` (voice, tone, humor, opinions, stats, stories) from your real writing.
6. Create a blog post per keyword, with a keyword cluster and images (Unsplash or your own).
7. Rewrite it with your voice and the **averaged format of the top 3 Google results**.
8. Find service keywords (sort by CPC, service + city). Export `service-keywords.csv` and build service pages.
9. Run the on-page SEO checklist over every blog post and service page, keeping the voice.
10. Add `sitemap.xml` and `robots.txt`. Run the Lighthouse loop until about 100 across the board.
11. Bottle the workflow into `blog` and service-page skills.
12. Publish at a gradual cadence.
13. Deploy through GitHub then Render (Static Site).
14. Set up Business Profile, Search Console (verify, submit sitemap, request indexing) and Analytics.
15. Test landing pages, apply the winner everywhere. Optionally do careful off-page work.

---

## 16. Quick-reference numbers

| Item | Value |
|---|---|
| Keyword difficulty | **≤ 30** (≈ 2/10 is ideal for fast wins) |
| Monthly search volume | **≥ 100** |
| Intent for blogs | Informational |
| Service keyword CPC (realistic) | About $3 to $20 |
| Blog internal links | 3 to 5 |
| Blog external links | 2 to 3 |
| Primary keyword placement | First 100 words |
| FAQ questions per blog | 4 to 8 |
| H1 per page | Exactly 1 |
| Humor hook | Within first 50 words |
| Competitor benchmark | Top 3 organic results, averaged (word count, H2s, images) |
| Lighthouse target | 100 on SEO, Accessibility, Best Practices, Performance |
| Request-indexing limit | About 10 per day |
| Publishing ramp | 1, 1, 2, 3, 4 per day, then keep reasonable |
| Service pages | Tasteful. Never thousands, probably not multiple hundreds |
| Click distribution | ~40% on #1, ~20% on #2 |
| Landing page conversion (his best) | ~20% |
| Deploy preset | Next.js |

---

## 17. Missing blueprint files: now reconstructed

The video points to five resources in the Skool blueprint, which you can't access. They have been **reconstructed** in `docs/seo-kit/`. Each is marked as [Video], [Reconstructed] or [Standard SEO]:

| Missing resource | Reconstructed in |
|---|---|
| The `CLAUDE.md` web-app file (SSG, stack, rules) | `docs/seo-kit/CLAUDE.md.template` |
| The 80+ item on-page checklist | `docs/seo-kit/on-page-seo-checklist.md` (90 items; the video named about a dozen, the rest are standard best practice) |
| The exact prompts (build, blog, rewrite, on-page, Lighthouse, service page, deploy, outreach) | `docs/seo-kit/prompts.md` |
| The reference templates (voice, tone, humor, opinions, stats, stories) | `docs/seo-kit/references/` |
| The `blog` and service-page skill definitions | **Installed:** `.claude/skills/blog/` and `.claude/skills/service-page/` |

These are my versions, not the creator's originals. They follow his method but the wording and the checklist's extra items are mine. If you ever get the real files, compare and merge.

---

## 18. My cautions (not from the video)

- **The video is plumbing-specific.** The dad-joke voice and "guy at the pub" persona are his brand fit. Define the right tone for your audience, but keep the principle of strong personality.
- **Claims are unverified.** The $500K and 50K clicks/month figures come from the creator, who also sells courses and affiliate tools (Semrush, etc.), so treat the numbers as marketing.
- **Fabricated experience risk.** The "stats" and "stories" reference files should contain **true** information. Don't let Claude invent anecdotes or numbers about a real business. This also matters for Google's expectations on experience and trustworthiness.
- **Scaled AI content carries risk.** Google has policies against low-value mass-produced content. His mitigations (voice, real stats, competitor-informed structure, slow cadence) help, but quality and originality still decide this. Review each post before publishing.
- **Keep secrets out of git.** `.env` should be git-ignored.
- **Re-check tool names and UIs.** Google My Business is now Google Business Profile, and Semrush's menus may differ from the video.
- **Local SEO.** The creator's other video covers local SEO in depth (Google Business Profile ranking fields, citations, reviews). That isn't part of this guideline.

---

## 19. Other stacks and non-service sites (the Capstone case)

The video builds a local service business on Next.js. Not every site matches that. A real example is the Capstone Foundation build spec (`docs/capstone/`), which differs in four ways:

| Difference | What to do |
|---|---|
| **Astro** (output folder `dist/`) or any other static framework, not Next.js (`out/`) | Describe the stack in the **Stack adapter** of `CLAUDE.md`. The skills read it. On Render, the Publish Directory is `dist` for Astro and `out` for a Next.js static export. |
| **No service + city pages** (a charity, a membership body, a portfolio) | Skip Phase 9 and the `service-page` skill. Set `service_pages: NOT USED`. The blog (here called "Stories") does the SEO work. |
| **No humor** (sensitive causes) | Set humor to "none" in `references/humor.md`. The first-50-words hook becomes an honest human moment, a direct question or a clear promise. |
| **Temporary address, indexing off** (`PUBLIC_INDEXABLE=false`) | Do **not** submit to Search Console or request indexing until the real domain is live and indexing is switched on. `PUBLIC_*` variables are read **at build time**, so redeploy after changing one. |

Also: the Lighthouse target in such a spec may be 95+ rather than 100. Use the spec's number. New posts may default to **draft** until the owner reviews them.

**Two more adjustments from the Capstone project**

| Topic | What to do |
|---|---|
| **Voice from a style reference** | An owner can supply a writing sample as a style reference (the Capstone project used a "sparkle text" article). Distil it into `references/<name>.md` (technique, where to use it, guardrails) and let the skill follow it. Never paste a whole third-party article into the repo. |
| **Images by context** | Some sites need rules by context: the owner's own photos for anything about the organisation's work, Unsplash for general-topic posts (including people), and Unsplash limited to no-people atmosphere on pages about the work. Put this in `CLAUDE.md`; the skill decides the context first. |
| **Scripture or other quoted text** | Set one translation in `CLAUDE.md`, verify every quotation exactly from an authoritative source, cite it, keep it short and add the publisher's notice. |

---

## 20. The `site-setup` skill (starting any new project)

`.claude/skills/site-setup/` automates the start of a project for **any** business, with checkpoints:

| Stage | What it does |
|---|---|
| 0 | Checks Node, npm, git and the skills. If a `CLAUDE.md` already exists it switches to **audit mode** and changes nothing. Reads a build spec if there is one. |
| 1 | Plain-language **intake** (about 40 questions in groups). "Unknown" is allowed and becomes a `TODO(owner)`. Nothing is invented. |
| 2 | Writes `CLAUDE.md` (with the **Stack adapter** for Astro or Next.js), the six `references/` files (only from the owner's answers), `keywords.csv` and the checklist. Never overwrites a file. |
| 3 | Creates the folder tree, `.gitignore`, `.env.example` and an empty `.env`. No framework scaffold. |
| 4 | Runs `scripts/verify-setup.sh` and shows the full output (files, folders, git-ignore proof, no secrets behind public prefixes, `.env` values never printed, stray video files). |
| 5 | **Stops** with a checklist for the owner: images, logos, keys, keyword export. |
| 6 | Checks what the owner uploaded, flags risky files, changes nothing. |
| 7 | Proposes the build plan and waits. It does **not** build the site. |

Type `site-setup` in a new chat in an empty project folder. For an existing project, type `site-setup audit`.
