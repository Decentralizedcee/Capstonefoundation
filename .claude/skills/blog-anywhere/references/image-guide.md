# Images for copy-paste posts

The post package must tell the owner **exactly which images the post uses, where each goes, its alt text, and any credit**. Choose the source **per post**, following the site's rules in `site.json` (`image_rules`). If the owner says "use my own photos" or "use Unsplash" for this post, that wins.

## 1. Which source

| Source | When | What you produce |
|---|---|---|
| **The owner's own photos** (best) | Anything about their own products, team, work, premises, results. Always when `image_rules` says so. | Look at the files, pick the ones that fit, write honest alt text, optimise copies, list them in `images.md`. The owner uploads them on their site. |
| **Unsplash, by hand** | General-topic posts when the owner has no suitable photo and does not want to use an API key. | Search terms and a description of the photo wanted. The owner downloads it from Unsplash's website (its licence allows free use; a credit is appreciated). The owner uploads it. |
| **Unsplash, through the API** | General-topic posts, the owner has an Access Key in `.env` and wants it done for them. | Search, pick, and put the photo in the post as a **linked image** (see 3), with a visible credit. |
| **None** | The owner wants no images or none fit. | Image briefs (what each image should show) so they can add their own later. |

**Never present a stock photo as the owner's own people, products, team, results or testimonials.** For those, only the owner's own photos.

## 2. The owner's own photos

1. List the files in `images-incoming/`. Open and **look at each candidate**; do not choose from filenames.
2. Skip, and tell the owner you skipped, anything that looks like a receipt, bank screenshot, ID, chat screenshot, medical document, or that shows an account number or private details.
3. Prefer photos not already used (check `published.json`).
4. Write **alt text from what is actually visible**. No names, claims or results the photo does not show.
5. Optimise copies (the original is never touched): `python3 <skill>/scripts/optimize_image.py <file> <out_dir> <descriptive-name> [--og]` (needs Pillow). It fixes rotation, limits width to 1600, converts to WebP and removes location data. `--og` adds a 1200 by 630 crop for the featured image.
6. In `post.json` use `"mode": "upload"` with the file path. The package puts a clear marker where the image goes, and lists the file in `images.md`.

## 3. Unsplash through the API (only if the owner wants it)

Rules from Unsplash's API guidelines. Follow all of them.

- Key: `UNSPLASH_ACCESS_KEY` in `.env` (Access Key only, never the Secret Key). **Check it is set without printing it.** If missing, stop and tell the owner how to add it themselves. Never ask for the key in the chat.
- Search once per image topic; read `id`, `alt_description`, `urls.raw`, `user.name`, `user.links.html`, `links.html`, `links.download_location`. Demo apps are limited to 50 requests an hour.
- **Hotlink** the URL the API returns, with size parameters: `<urls.raw>&w=1200&q=75&fm=webp&fit=crop`. Do not download and self-host photos taken through the API.
- Send one request to `links.download_location` when a photo is chosen for the post.
- Show a visible credit: "Photo by [name] on Unsplash", with the photographer's link and Unsplash's link, both carrying `?utm_source=<app name>&utm_medium=referral`. The app name is the owner's Unsplash application name (it may not contain the word "Unsplash").
- In `post.json` use `"mode": "url"` with the full URL and the credit line.
- **Tell the owner**: some platforms copy pasted images onto their own servers. If they do, the "linked" requirement is no longer met, so for those platforms use the hand-download route or their own photos.
- Show the owner every photo you picked (id, description, link) in the report. Do not bulk-pull images.

## 4. For every image

- **Alt text:** describes what is visible, in plain words, naturally including the topic where it truly fits. No keyword stuffing, no "image of".
- **One featured image** per post, about **1200 by 630 pixels** (also used when the post is shared). Other images no wider than 1600 pixels.
- **Format and weight:** WebP or JPEG, ideally under 200 KB.
- **Filename:** short, descriptive, lowercase, with dashes (`reusable-bottle-lids.webp`), never `IMG_4312`.
- **How many:** about the competitor average from the research step, with a sensible minimum of the featured image plus one inline image for a long post.
- **Caption and credit** where useful or required.
- **People:** only with consent. Never imply a real person endorses the business.
