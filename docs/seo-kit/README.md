# SEO Kit (reconstructed)

The video's free Skool blueprint wasn't accessible, so these files are **reconstructions**. They are built from (a) what the video shows and says, and (b) standard, widely accepted SEO practice where the video only gestures at something (mainly the "80+ signals" checklist).

Every file marks its confidence:

- **[Video]** means the video stated or showed it.
- **[Reconstructed]** means I wrote it to match what the video describes, as the original's exact text isn't available.
- **[Standard SEO]** means it comes from general SEO best practice, not the video.

## Contents

| File | What it is |
|---|---|
| `CLAUDE.md.template` | The project instruction file. Copy it to the root of the website project as `CLAUDE.md` and fill in the `{{placeholders}}`. |
| `on-page-seo-checklist.md` | The "80+ signals" checklist, reconstructed. Paste or reference it in the on-page prompt. |
| `prompts.md` | Every prompt from the video, written out in full and ready to copy. |
| `references/` | Templates for the voice, tone, humor, opinions, stats and stories files. |
| `.claude/skills/blog/` and `.claude/skills/service-page/` | **The installed skills** (at the repo root, not in this folder). Each bundles the image-source rules, the checklist and the image optimizer script. |

## Project layout the kit assumes

```
my-site/
├── CLAUDE.md
├── .env                    # UNSPLASH_ACCESS_KEY=...   (git-ignored; only if using Unsplash)
├── images/                 # your own images (only if using local images)
├── .gitignore
├── keywords.csv            # blog keywords, exported from Semrush
├── service-keywords.csv    # service + city keywords, exported from Semrush
├── references/             # voice.md tone.md humor.md opinions.md stats.md stories.md
├── content/
│   ├── blog/               # one .md file per post, with frontmatter
│   ├── services/           # one .md file per service page
│   └── published.json      # keywords already used, so none is reused
├── docs/
│   └── on-page-seo-checklist.md
└── src/ or app/            # Next.js (static generation)
```

## Work directly in Claude Code

The video used Antigravity, and its update note recommends VS Code. You don't need either. Run Claude Code in a terminal inside the project folder. Everything in this kit works the same way. When a prompt says "attach a screenshot", reference the image file's path or drag the image into the Claude Code session.
