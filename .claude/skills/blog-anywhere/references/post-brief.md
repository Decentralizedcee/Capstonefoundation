# The post brief (ask before every post)

Ask these as a short, friendly sequence, **one group at a time**, in plain words. Record the answers in the `brief` object of `post.json` (see `post-package-spec.md`) and read a one-paragraph summary back before researching or writing. "I don't know" is fine: offer a sensible option and say it is only a suggestion.

**Nothing here has a built-in default.** Every user chooses for every post. The examples below are a menu of ideas, never rules, and never anyone else's house style. The only rules that always apply are the user's **own** (their privacy, legal and off-limits topics from their own `site.json` and `content_rules`) and the hard rules in `SKILL.md`.

## 1. Voice for this post
Show this menu and let the user pick **one, or mix two**, or describe their own:

- Friendly and conversational
- Professional and authoritative
- Warm and inspirational
- Calm and reassuring
- Bold and direct
- Playful and witty
- Educational and clear
- Premium and refined
- **My own voice, from my writing samples** (use the site's saved voice files and measured numbers, or collect samples now)
- **Describe it yourself** (they say it in their own words; repeat it back as two or three short rules)

Then ask:
- **Humor:** none, light, or playful? Any part of this post where there must be none?
- **Person:** "I" (one person) or "we" (a team or company)?
- **Angle:** what is the main point or promise of this post, in one sentence?
- **Audience:** who is this post for, and what do they want or worry about?

How to use the answer:
- The choice applies to **this post only**. A different post may use a different voice.
- If they picked **my own voice**, read every file in `references/` and `anchor-sample.md`, and run the voice check afterwards.
- If they picked a menu voice or described one, write a **voice brief** (five to eight bullet rules: sentence length, how the reader is addressed, humor level, words to favor and avoid). Show it, get an OK, and write the post from it. There are no measured numbers for these, so the voice check script has nothing to compare; judge the draft against the brief and say so in the report.
- Do not mix in the site's saved voice files for a menu or described voice unless the user asks.
- Offer once, after the post: *"Want to save this voice as a named variant for future posts?"* Only if they say yes, save it as `references/voice-variants/<name>.md`. Never change the approved site voice files without their approval and a version-log note.

## 2. Keywords
Before writing anything:
1. If `keywords.csv` has rows, offer the next few unused ones (not in `published.json`) and let them **choose**.
2. If they already have **a specific keyword** in mind, take that one.
3. If there is no list and no keyword, **ask** for one, or offer to suggest a few topics clearly marked as unverified ideas.

Flag data you cannot verify (blank volume or difficulty means unverified; say so). Never invent search volumes. Then go to research.

## 3. Images for this post
Ask: *"Which images do you want in this post?"* Offer: their own photos (where are they?), free stock photos (by hand or through their key, per `image-guide.md`), specific files they name, or no images yet (you write image briefs). Also ask **how many** and **where** (top image, in the middle, near the end) if they have a view; otherwise suggest the competitor average. Their answer for this post wins over the site's default.

## 4. Their own content
Ask: *"Do you already have content for this post: a draft, notes, or finished text?"*

| Mode | What it means | What you may do |
|---|---|---|
| **Write it for me** | They have nothing, or only a topic. | Write the whole post. |
| **Build on my notes** | They have notes, bullets or a rough draft. | Keep their facts and ideas, turn them into a full post, add the SEO structure. Mark everything you added so they can see it. |
| **Use mine exactly** | They have finished text. | Change **nothing** in their wording. Only add the SEO fields, the format (headings, if they already exist), images, alt text and the checks. Anything you would change is a **suggestion** shown separately; apply it only if they say yes to that exact change. |

For **use mine exactly**: save their text as a file in the post folder, set `brief.content_mode` to `exact` and `brief.original_file` to that file. The package builder then compares the post with their file word for word and reports a **FAIL** if anything differs. Their title is a separate field; a first-line `# Title` in the file is ignored by the comparison. Facts you cannot verify in their text are flagged as questions, not edited.

## 5. Is the site connected to Claude?
Ask: *"Is your site connected to Claude through a connector (WordPress, Wix, Shopify or another builder)?"* Check which connector tools exist in this session (look at the tools you have; do not guess and never ask for a password, token or key). The user connects the site themselves.

- **Connected, and the tools can create a post:** after the package is built and checked, show the user **exactly** what will be sent: title, body, SEO fields, tags, image list, and that it will be a **draft**. Get a clear "yes, send it as a draft". Then create **a draft only**, never published, never scheduled. Report what the tool answered. Tell the user to open the draft on their site, check it, and press publish themselves. If the tool cannot make a draft (it can only publish), do **not** use it; give the copy-paste package instead and say why.
- **Not connected, or unsure:** give the copy-paste package and the paste guide for their platform.
- Never claim you saw the live site. Never edit an existing live post.

Record the answer in `site.json` (`connection`) so you do not have to ask every time, but ask again if the session has different tools.
