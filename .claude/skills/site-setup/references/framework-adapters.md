# Framework adapters

Use the block for the framework the owner chose (or that their build spec names). Copy its values into the `## Stack adapter` section of the project `CLAUDE.md`, paste its technical-rules block into `CLAUDE.md`, create its folder tree, and create `.env` with only its keys (empty values).

If the owner's build spec uses a different layout, **the spec wins**: adapt these values to match it and say so.

Both frameworks are used as **static sites** hosted as a **Render Static Site**: Build Command `npm install && npm run build`, Publish Directory as below. Values that start with the framework's public prefix are baked into the HTML **at build time**, so redeploy after changing one.

---

## 1. Astro (static)

**Good for:** content-led sites (blogs, nonprofits, portfolios, local business sites). Ships little JavaScript by default. Content collections suit the blog.

### Stack adapter values
```
framework:            astro
build_command:        npm install && npm run build
output_dir:           dist
blog_collection:      src/content/blog              (or the name the owner wants, for example src/content/stories)
blog_format:          mdx                           (or md)
blog_route:           /blog/<slug>
blog_index:           /blog
service_pages:        src/content/services          (or NOT USED)
published_log:        src/data/published.json
new_posts_as:         published                     (or draft if the owner reviews before publishing)
local_images_dir:     images                        (or images-incoming)
image_pipeline:       scripts/optimize-image.mjs    (bundled sharp script) or the project's own pipeline
image_registry:       none                          (or src/data/images.ts if the project keeps one)
processed_images_dir: src/assets/images
image_source:         <owner's choice>
unsplash_app_name:    <owner's Unsplash app name, only if using Unsplash>
```

### Folder tree
```
(project root)
├── CLAUDE.md  README.md  keywords.csv  .gitignore  .env  .env.example
├── docs/                      checklist, intake, any build spec
├── references/                voice, tone, humor, opinions, stats, stories
├── <local_images_dir>/        owner's own photos (git-ignored contents)
├── public/                    static files (brand/, favicon)
├── scripts/                   image scripts
└── src/
    ├── assets/images/         processed images (astro:assets)
    ├── components/  layouts/  pages/  styles/
    ├── content/<blog>/        posts (+ <services>/ if used)
    └── data/                  published.json (and images.ts if used)
```

### Technical rules (paste into CLAUDE.md)
- Static output only (`output: 'static'`). No server rendering for content pages.
- Use Astro integrations for the sitemap, RSS and MDX; never hand-edit generated files.
- Set `site` from the public site URL variable so canonical links, the sitemap and Open Graph tags use it.
- Define content collections with a schema that includes `title`, `description`, `date`, `primary_keyword`, `cluster`, `draft` and `images`.
- Own images go through `astro:assets` (optimised). **Unsplash images are hotlinked with a plain `<img>`, never through `astro:assets`** (remote optimisation re-hosts them, which Unsplash does not allow).
- Self-host fonts. Minimise client JavaScript. No layout shift (explicit width and height).
- `PUBLIC_` variables are visible to every visitor. **Never** put a secret behind that prefix.

### `.env` keys (empty values; owner types their own)
```
PUBLIC_SITE_URL=
PUBLIC_INDEXABLE=true        # set to false on a temporary address (adds noindex and blocks crawlers) until the real domain is live
UNSPLASH_ACCESS_KEY=         # only if using Unsplash (Access Key only)
```

### `.gitignore` essentials
`.env`, `node_modules/`, `dist/`, `.astro/`, `<local_images_dir>/*` (keep its `.gitkeep`), `.DS_Store`

### Render
Static Site, Build Command `npm install && npm run build`, Publish Directory **`dist`**.

---

## 2. Next.js (static export)

**Good for:** sites that may later grow app-like features. A static export has no server features.

### Stack adapter values
```
framework:            nextjs
build_command:        npm install && npm run build
output_dir:           out
blog_collection:      content/blog
blog_format:          md
blog_route:           /blog/<slug>
blog_index:           /blog
service_pages:        content/services              (or NOT USED)
published_log:        content/published.json
new_posts_as:         published                     (or draft)
local_images_dir:     images
image_pipeline:       scripts/optimize-image.mjs    (bundled sharp script)
image_registry:       none
processed_images_dir: public/images/<blog|services>/<slug>
image_source:         <owner's choice>
unsplash_app_name:    <owner's Unsplash app name, only if using Unsplash>
```

### Folder tree
```
(project root)
├── CLAUDE.md  README.md  keywords.csv  .gitignore  .env  .env.example  next.config.*
├── docs/  references/  <local_images_dir>/  scripts/
├── public/                    static files and processed images (public/images/...)
├── content/
│   ├── blog/                  one .md per post
│   ├── services/              one .md per service page (if used)
│   └── published.json
└── app/ (or src/app/)         routes, layouts, components
```

### Technical rules (paste into CLAUDE.md)
- Set `output: 'export'` in `next.config` so `npm run build` writes plain HTML to `out/`.
- Generate blog and service routes with `generateStaticParams` and `dynamicParams = false`.
- Static export means **no server features**: no API routes, no middleware, no on-request rendering, no image optimisation server. Set `images: { unoptimized: true }` and ship **pre-compressed WebP or AVIF** at the right sizes (this keeps Lighthouse Performance high).
- Sitemap and robots must be static (`export const dynamic = 'force-static'`). Set `trailingSlash: true` if Render's static routing needs it, and confirm a `404.html` is produced.
- Self-host fonts with `next/font`. No layout shift (explicit width and height).
- `NEXT_PUBLIC_` variables are visible to every visitor. **Never** put a secret behind that prefix.

### `.env` keys (empty values; owner types their own)
```
NEXT_PUBLIC_SITE_URL=
NEXT_PUBLIC_INDEXABLE=true   # set to false on a temporary address until the real domain is live
UNSPLASH_ACCESS_KEY=         # only if using Unsplash (Access Key only)
```

### `.gitignore` essentials
`.env`, `node_modules/`, `out/`, `.next/`, `<local_images_dir>/*` (keep its `.gitkeep`), `.DS_Store`

### Render
Static Site, Build Command `npm install && npm run build`, Publish Directory **`out`**.

---

## 3. Another static framework

Ask the owner (or the spec) for: build command, output folder, content folder and format, the public env prefix, the cache folder to ignore. Fill the Stack adapter from those answers. Keep the same safety rules: static output, no secrets behind a public prefix, own images optimised, Unsplash hotlinked.

Not supported: sites that must render on a server for every request (for example WordPress or server-rendered apps).
