# Image sources: how to get and use images

Pages (blog posts and service pages) can get images from **two sources**, chosen per run. Nothing here needs an API key except the Unsplash mode.

## 1. Choosing the mode

Resolve the mode in this order and stop at the first match:

1. **The user's instruction for this run.** Examples:
   - "use unsplash", "pull images from the API" → `unsplash`
   - "use my images", "use the images folder", "use the photos I uploaded" → `local`
   - "no images", "skip images" → `none`
   - "use my images and fill the gaps from unsplash" → `mixed`
2. **`image_source:` in the project `CLAUDE.md`** (`unsplash` | `local` | `mixed` | `none` | `ask`).
3. If still unknown → **ask the user once**: "Unsplash, your own images in `images/`, or none?" Do not guess.

A website may use Unsplash for every post, never use it, or switch per run. Never assume the previous run's mode.

## 2. Pre-flight checks (run before any other work)

| Mode | Check | If it fails |
|---|---|---|
| `unsplash` | `.env` in the project root contains `UNSPLASH_ACCESS_KEY` (check it is set; **never print, echo or paste its value**). `.env` is listed in `.gitignore`. | **Stop.** Tell the user to create a file named exactly `.env` in the project root (next to `CLAUDE.md`) containing `UNSPLASH_ACCESS_KEY=their_access_key`, and to add it themselves, not in chat. Offer `local` or `none` as alternatives. |
| `local` | `images/` exists in the project root and holds at least one image (`.jpg .jpeg .png .webp .avif`). | **Stop.** Tell the user to put their images in `images/` in the project root, or to switch mode. |
| `mixed` | Both of the above (unsplash part only needed if the folder has too few suitable images). | Same messages. |
| `none` | Nothing. | Continue and insert clearly marked image placeholders (see section 5). |

Only the **Access Key** is needed. Never ask for or use the Secret Key. Never name the variable with a `NEXT_PUBLIC_` prefix (it would publish the key to every visitor).

## 3. Mode `unsplash`

Rules come from Unsplash's API Guidelines. Follow all of them.

### 3.1 Search

Load the key without printing it, then search once per image topic:

```bash
set -a; . ./.env; set +a
curl -s -G "https://api.unsplash.com/search/photos" \
  -H "Authorization: Client-ID $UNSPLASH_ACCESS_KEY" \
  --data-urlencode "query=<specific visual topic>" \
  --data-urlencode "per_page=10" \
  --data-urlencode "orientation=landscape" \
  --data-urlencode "content_filter=high"
```

- Use specific visual queries (what the photo should show), not the SEO keyword itself.
- Read from each result: `id`, `alt_description`, `width`, `height`, `urls.raw`, `user.name`, `user.links.html`, `links.html`, `links.download_location`.
- Pick photos that truly match the topic and fit the brand. Prefer real, uncluttered scenes. Avoid photos with legible brand names, faces that imply a testimonial, or content that misrepresents the business.
- **Rate limit:** demo apps get 50 API requests per hour (1,000 after production approval). Check the `X-Ratelimit-Remaining` response header. Use as few requests as possible (one search per image topic), and stop and report if it runs out. Requests to `images.unsplash.com` do not count.
- Unsplash expects the API to be used for authentic, human-reviewed experiences. **Show the user the chosen photos (id, description, link) in your report** so they can approve or swap them. Do not bulk-pull images.

### 3.2 Hotlink (required)

All uses of the image must use the URLs returned by the API. **Do not download and self-host Unsplash photos.** Store `urls.raw` and add sizing parameters:

```
<urls.raw>&w=1200&q=75&fm=webp&fit=crop
```

- Provide a `srcset` (for example `w=480`, `w=800`, `w=1200`) and a `sizes` attribute.
- Always set explicit `width` and `height` (use the aspect ratio you crop to) so there is no layout shift.
- The hero / above-the-fold image gets `fetchpriority="high"` and no lazy loading. Everything else gets `loading="lazy"`.
- Add `<link rel="preconnect" href="https://images.unsplash.com">` in the page head.
- With a static export, use a plain `<img>` (or `next/image` with `unoptimized`). No `remotePatterns` setup is needed for `<img>`.

### 3.3 Trigger the download (required)

When a photo is chosen for a page, send one request to its `links.download_location`:

```bash
curl -s -o /dev/null -H "Authorization: Client-ID $UNSPLASH_ACCESS_KEY" "<links.download_location>"
```

Do this once per photo, at the moment it is chosen for the page, not on every page view. (The key is only used at writing time. The finished static site never needs it.)

### 3.4 Attribution (required)

Visible under or next to every Unsplash image:

> Photo by **[Photographer name]** on **Unsplash**

- The photographer name links to `user.links.html` + `?utm_source=<app>&utm_medium=referral`
- "Unsplash" links to `https://unsplash.com/?utm_source=<app>&utm_medium=referral`
- `<app>` is `unsplash_app_name` from `CLAUDE.md` (the name of the owner's Unsplash application). The name may not contain "Unsplash". If it is not set, ask.

### 3.5 Frontmatter to store

```yaml
images:
  - source: unsplash
    id: LBI7cgq3pbM
    src: https://images.unsplash.com/photo-...?ixid=...      # urls.raw, unmodified
    width: 1600
    height: 900
    alt: "Plumber tightening a pipe fitting under a kitchen sink"
    role: hero            # hero | inline
    credit:
      photographer: "Jane Doe"
      photographer_url: "https://unsplash.com/@janedoe?utm_source=<app>&utm_medium=referral"
      unsplash_url: "https://unsplash.com/?utm_source=<app>&utm_medium=referral"
```

## 4. Mode `local` (the user's own images)

The user drops images into `images/` in the project root. These are theirs, so no attribution is needed. (Assume the user has the rights to the images. If a file looks like stock with a watermark, flag it.)

### 4.1 Choose images

1. List `images/` (recursively). Subfolders and filenames are hints (`images/team/`, `images/projects/`).
2. **Look at the candidates** (open the image files) and match them to the post's topic. Do not choose from filenames alone.
3. Prefer images **not yet used** on other pages. Check `content/images-used.json`. Reuse an image only if there is no good alternative, and say so.
4. If there are not enough suitable images, **say so and ask**: use fewer, switch a few to Unsplash, or add placeholders. Never fall back to Unsplash without permission (unless the mode is `mixed`).

### 4.2 Optimize and place

- **Never modify or move the originals in `images/`.**
- Run the bundled optimizer (copy `scripts/optimize-image.mjs` into the project's `scripts/` folder if it is not there; it needs `sharp`, so `npm install --save-dev sharp` if missing):

  ```bash
  node scripts/optimize-image.mjs "images/<file>" "public/images/<blog|services>/<slug>" "<descriptive-name>"
  ```

  It writes `<name>-480.webp`, `-800.webp`, `-1200.webp` (never upscaled) and prints JSON with the paths and dimensions.
- Use **descriptive, hyphenated filenames** (`kitchen-sink-repair.webp`, not `IMG_4312.webp`).
- Write the `alt` text yourself **from what is actually in the image**. Never claim anything the image does not show (no invented names, places or results).
- Record each used file in `content/images-used.json` (`{ "images/<file>": ["<slug>"] }`).

### 4.3 Frontmatter to store

```yaml
images:
  - source: local
    original: images/team-on-site.jpg
    src: /images/blog/<slug>/team-on-site-1200.webp
    srcset: "/images/blog/<slug>/team-on-site-480.webp 480w, /images/blog/<slug>/team-on-site-800.webp 800w, /images/blog/<slug>/team-on-site-1200.webp 1200w"
    width: 1200
    height: 800
    alt: "Two technicians fitting a water heater in a utility room"
    role: hero
```

## 5. Mode `none` and gaps

If there are no images, or the user chose none, insert this where an image belongs and list each one in the report:

```
<!-- IMAGE PLACEHOLDER: <what the image should show> | alt: <suggested alt text> -->
```

Never leave a broken image link.

## 6. Mode `mixed`

Use local images first (section 4). For topics with no suitable local image, use Unsplash (section 3) and say which images came from where. Attribution applies only to the Unsplash ones.

## 7. Every image, every mode

- Descriptive `alt` text (what the image shows, naturally including the topic where it genuinely fits; no keyword stuffing).
- Explicit `width` and `height`.
- One hero image (eager, high priority), the rest lazy.
- Number of images should match the competitor average from the research step, within reason.
- An Open Graph image (`og:image`, about 1200x630) per page: the hero image, cropped. For Unsplash use `&w=1200&h=630&fit=crop&fm=jpg`.
