# The post package: `post.json`

Write one `post.json` per post at `blog-sites/<site>/posts/<slug>/post.json`, then run:

`python3 <skill>/scripts/build_package.py blog-sites/<site>/posts/<slug>/post.json blog-sites/<site>/posts --zip --site-url <site url>`

The package is written into `blog-sites/<site>/posts/<slug>/` (next to `post.json`) and a `<slug>-package.zip` is placed in `posts/`. It cleans the HTML, runs the checks, and writes `post-preview.html`, `body.html`, `post.md`, `fields.txt`, `schema.jsonld.html`, `images.md`, `lint-report.txt`, `HOW-TO-PUBLISH.md`, and copies the owner's own image files. Fix every FAIL and think about every WARN, then rebuild.

## Fields

| Field | Required | Rules |
|---|---|---|
| `title` | yes | The headline. The site shows it as the H1. Includes the primary keyword. |
| `seo_title` | yes | 30 to 60 characters. Primary keyword near the start. |
| `meta_description` | yes | 70 to 160 characters. Primary keyword and a reason to click. |
| `slug` | yes | Lowercase letters, numbers, single dashes. Contains the primary keyword. |
| `primary_keyword` | yes | One phrase. |
| `cluster` | no | 5 to 10 related terms used naturally. |
| `excerpt` | yes | Up to 300 characters, for blog listings. |
| `tags` | yes | 1 to 8. |
| `category` | no | |
| `author` | no | Only a real name the owner gave. |
| `date` | no | Suggested publish date, `YYYY-MM-DD`. |
| `platform` | no | `shopify`, `wordpress`, `other` (opens the matching paste guide). |
| `target_words` | no | From the competitor research; the check allows 20 percent either way. |
| `featured_image` | no | Image object (below). |
| `images` | no | List of image objects, numbered from 1. |
| `brief` | no | `{ "voice": "what the user chose", "humor": "none/light/playful", "person": "I/we", "content_mode": "write/notes/exact", "original_file": "path (only for exact)" }`. In `exact` mode the builder compares the body with the original file word for word and FAILs on any difference. |
| `body_html` | yes | Clean HTML (rules below). |
| `faq` | no | List of `{ "q": "...", "a": "..." }`, 4 to 8. Appended as an H2 section, or placed where `[[FAQ]]` appears. |
| `faq_heading` | no | Default "Frequently asked questions". |
| `social` | no | Object of share texts, for example `{ "facebook": "...", "linkedin": "..." }`. |
| `canonical_url` | no | Only if known. |
| `site_url` | no | Used to tell internal from external links. |

### Image object
`mode` (`url` or `upload`), `alt` (required), `description` (what it shows), `placement` (where it goes), `caption`, `credit`, `width`, `height`, plus `url` (mode `url`) or `file` (mode `upload`).

- `mode: url`: the image is placed in the post as a linked image with its caption and credit.
- `mode: upload`: the post gets a clear marker `[IMAGE n: ...]`; the owner uploads the file and replaces the marker. The file is copied into the package.

## Body HTML rules (so it pastes well on any platform)

- **No H1.** Start with a short intro paragraph, then **H2** sections, **H3** only inside an H2. Do not skip levels.
- Allowed: `h2 h3 h4 p ul ol li a strong em blockquote img figure figcaption br hr table thead tbody tr th td`. Allowed attributes: `href` and `title` on links; `src`, `alt`, `width`, `height` on images. **Everything else is removed** (no classes, styles, scripts, iframes, divs).
- Put `[[IMAGE:1]]`, `[[IMAGE:2]]` where those images go. Put `[[FAQ]]` where the FAQ goes (optional).
- **Internal links:** use a real address from `site-pages.csv`. If the page is not on the list, use `href="[[INTERNAL:short description of the page]]"` so the owner knows to replace it. **Never invent a web address.**
- External links: only to reputable, real sources you can name; descriptive link text (never "click here").
- Short paragraphs (2 to 4 lines). Lists and tables only where they help.
- No text in capitals for emphasis; use `strong` sparingly.
- Anything unknown is `TODO(owner): what is needed`, never a guess.

## The checks (what the script tells you)

Search title and meta description length; clean slug; excerpt length; tag count; no H1 in the body; H2 sections present and no skipped levels; primary keyword in the first 100 words, title, search title, meta description and slug; alt text on every image; leftover `[[INTERNAL:...]]` and TODO notes; internal and external link counts; vague link text; FAQ count; anything removed to make the HTML safe. **FAIL** means fix before publishing. **WARN** means look at it and decide.
