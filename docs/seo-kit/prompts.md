# Prompt Library (reconstructed)

The video shows these prompts, mostly in short form. Prompts marked **[Video]** follow the wording shown. The longer versions are **[Reconstructed]**: they include the steps the video describes but doesn't display in full.

Replace `{{placeholders}}`. Run everything in Claude Code from inside the project folder.

---

## 1. Build the starter site [Video]

Attach a Dribbble screenshot first (drag the image in, or give its file path).

```
Build a beautiful website for {{business}} with these pages only:
1. A homepage
2. An index page for my blog posts
3. An index page for my service pages

I've attached a screenshot of the design I want. Copy that design closely
(layout, spacing, typography feel, colour mood), adapted to {{business}}.

Follow CLAUDE.md. Static site generation is required. Use Next.js.
Make it fast, accessible and mobile-first. When done, run the build and
tell me how to preview it locally.
```

---

## 2. Keyword export hand-off [Video]

After exporting from Semrush, drop the CSV into the project and run:

```
I added my Semrush export. Rename it to keywords.csv at the project root.
Show me the columns, the row count, and the 20 rows with the lowest
keyword difficulty and a volume of at least 100. Flag any keyword that
looks like another company's brand or a "how to become a {{profession}}"
query so I can remove it.
```

Use the same pattern for `service-keywords.csv`.

---

## 3. First-draft blog post [Video]

```
Create a blog post for me about "{{primary keyword}}".
That is the primary keyword.

Also create a keyword cluster of 5 to 10 related terms. Take them from
keywords.csv where they fit, or generate close variations if not.

Add images from Pexels. My API key is in .env as PEXELS_API_KEY.
Save the post to content/blog/{{slug}}.md with frontmatter
(title, description, slug, primary_keyword, cluster, date, images).
```

---

## 4. Fill the reference files from your own writing [Video]

```
I'm pasting examples of my own writing below (LinkedIn posts, emails,
transcripts). Create or update every file in references/:
voice.md, tone.md, humor.md, opinions.md, stats.md, stories.md.

Rules:
- Extract only what is actually in my text. Do not invent facts, numbers
  or anecdotes.
- Quote short representative phrases in voice.md and humor.md.
- Put every real number in stats.md and every real anecdote in stories.md.
- If a file has nothing to draw on, leave the template placeholders and
  list what I need to provide.

<paste writing here>
```

If you have no samples, add a humor/tone reference you admire:

```
Please add the following passage as a humor and tone reference in
references/humor.md. Describe what makes it work (rhythm, self-deprecation,
asides) so you can imitate the technique without copying the text.

<paste passage>
```

---

## 5. Rewrite with voice and "steal the winning format" [Reconstructed]

The video describes this combined step: rewrite using the reference files, research the top 3 results first, and copy the length, structure and topics.

```
Rewrite content/blog/{{slug}}.md.

STEP 1: RESEARCH (before writing anything)
Search Google for the primary keyword "{{primary keyword}}". Take the top 3
organic results. Skip Reddit, Quora, forums and video results.
For each, record: word count, number of H2s, number of H3s, number of images,
whether it has a FAQ, the topics covered, the format (guide, list, how-to),
and how the keyword is used.
Then compute the AVERAGE word count, H2s and images. Those are my targets.
List what all three cover (must include) and what none cover (my angle).
Show me this table before writing.

STEP 2: WRITE
Rewrite the post to those averaged targets. Use my references/ files:
voice, tone, humor, opinions, stats, stories. Read all of them first.
- The first 50 words must land a joke, self-aware aside, or vivid image.
- Use real stats and stories from the references only. If a useful one is
  missing, insert a line starting with "TODO(owner):" instead of inventing it.
- No generic AI openings ("In today's fast-paced world", "In this
  comprehensive guide").
- Keep it genuinely helpful. Answer the question directly and early.

STEP 3: COMPARE
Show the old opening and the new opening side by side.
```

---

## 6. On-page SEO pass [Reconstructed from the video's description]

```
Update content/blog/{{slug}}.md using every applicable item in
docs/on-page-seo-checklist.md.

Critical constraint: keep the voice, style and humor of the post.
Do not turn it into a dry, corporate post. People who bounce will not
rank. Content is king; the checklist is the seasoning.

Make sure of at least:
- exactly one H1 with the primary keyword
- the primary keyword in the first 100 words
- 3 to 5 internal links (find relevant existing posts and services yourself)
- 2 to 3 external links to reputable sources
- 4 to 8 FAQ questions with FAQPage JSON-LD
- meta title (<= 60 chars) and meta description (<= 160 chars)
- Open Graph and Twitter tags, canonical URL, Article JSON-LD
- alt text on all images

When done, print the audit report in the format at the bottom of the
checklist, and fix anything that failed.
```

Use the same prompt for service pages, changing the file path to `content/services/{{slug}}.md`.

---

## 7. Service page [Video, expanded]

```
Build a service landing page. Use the first row of service-keywords.csv
that is not already in content/published.json.

The keyword is "{{service}} {{city}}". This is a landing page for that
specific service in that city.

It should look like the homepage (same design system and conversion layout).
Include: a headline with the keyword, a call to action and form above the
fold, why choose us, the process, pricing guidance if known, local details
for {{city}} (neighbourhoods, local regulations or conditions, only if
you're sure they're accurate, otherwise TODO(owner)), reviews/trust
signals, a short FAQ, and links to 3 related blog posts.

The copy must be unique to this service and city, not the same page with a
swapped word. Save to content/services/{{slug}}.md and record the keyword
in content/published.json. Then run the on-page checklist.
```

---

## 8. Lighthouse loop [Video]

Run Lighthouse in Chrome (DevTools → Lighthouse). Expand every failing section first, then paste:

```
Here is my Lighthouse report:

<paste the full report, including expanded failing audits>

Optimize the site so I get 100 across Performance, Accessibility,
Best Practices and SEO. Also generate the robots.txt and sitemap.xml
if they are missing, following CLAUDE.md.
Run the build afterward and list what you changed.
```

If any score is below 100:

```
Re-tested. These are the new results. Here is the report: <paste>.
We're not at 100 yet. Fix the remaining issues.
```

Repeat until solved or until the remaining items are acceptable.

---

## 9. Create the reusable skills [Video, expanded]

Draft definitions are in `skills-draft/`. When approved, create them from them:

```
Create a skill called "blog" from docs/seo-kit/skills-draft/blog.md.
Install it in .claude/skills/blog/SKILL.md and verify its frontmatter.
```

Original wording from the video:

```
Please create a skill called blog where we automatically generate blog posts
with all the details we just covered: grab a keyword from keywords.csv,
create a keyword cluster, publish the blog post, pull in pictures from
Pexels, add our writing style, voice, tone and humor, optimize for on-page
SEO, and reuse the same standard technical-SEO page template every time.
```

---

## 10. Deploy [Video]

```
Initialize git, make the first commit, and push this project to my
GitHub repository: {{repo url}}. Do not commit .env.
```

Then in Vercel: create a free account, **Add New Project**, connect GitHub, import the repo, set the preset to **Next.js**, and deploy.

---

## 11. Search Console verification [Video]

```
Add this meta tag to the website for Google Search Console verification,
then deploy it live to GitHub and then Vercel:

<paste the HTML tag from Search Console>
```

Then in Search Console: submit `sitemap.xml` under Sitemaps, and use the top search bar → **Request indexing** for each new page (roughly 10 a day).

---

## 12. Backlink outreach helpers [Reconstructed, from the video's four legitimate methods]

Broken-link swap:
```
Here is a list of broken outbound links from a competitor audit:
<paste>
For each, find which page of mine covers the same topic (or tell me what
page I need to write). Draft a short, friendly outreach email: point out
the broken link, offer my page as a replacement, no pressure.
```

Guest post sourcing:
```
Draft a pitch for sites that accept guest posts in the {{niche}} space
(I searched: {{niche}} "write for us"). Give 3 headline ideas that fit my
expertise, and keep it short and specific. One backlink to my site only,
in the bio or naturally within the content.
```

Journalist queries:
```
Here is a journalist's question: <paste>.
Write a clear, quotable, expert answer in my voice (references/voice.md),
with one real example from references/stories.md or a TODO(owner) if none.
```

---

## 13. Cadence guard [Video]

Add this to the top of any bulk task:

```
Do not create more than {{N}} posts in this run. Our current stage of the
publishing ramp is: {{stage}}. Stop and ask before exceeding it.
```

Ramp from the video: day 1 → 1, day 2 → 1, day 3 → 2, day 5 → 3, day 8 → 4. Keep it reasonable after that.
