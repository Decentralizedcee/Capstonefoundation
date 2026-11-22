# Une Femme Divine: handoff note

Status as of 22 Nov 2026. Branch: `ccr-80b17ffc-ti5gyr` (repo `decentralizedcee/capstonefoundation`). Everything below is committed on that branch.

## 1. What this project is
Une Femme Divine sells **Divine Elixir**, a daily collagen ritual for women (halal, made in Slovakia, EU). The webshop opened 29 Sep 2026 on Shopify (store `unefemmedivine.com`, admin domain `71w86d-dn.myshopify.com`, EUR, Netherlands). Markets: NL, BE, DE, ES, Dubai, UK.

We built a lead magnet: a free **Rhythm of the Body** planner (a gentle cycle and self-care planner) given in exchange for joining the email list. We also drafted Instagram posts and a WhatsApp community plan.

**Only the planner is in use.** The earlier "Your Divine Ritual" guide is built but parked.

## 2. Brand rules (always follow)
- Voice: calm, warm, short sentences, "you" and "we". Soft emojis, sparingly.
- **No health or beauty claims.** No cures, treats, prevents, "miracle", "all-in-one", no comparisons, nothing unprovable. EU/UK collagen claims are not allowed.
- Planner wording must stay lifestyle only: no hormones, fertility, pain, symptoms or pregnancy advice. It carries a "not medical advice" disclaimer.
- Palette (from Badar's Divine Elixir Welcome Guide PDF): aubergine `#3B1F2B`, cream `#F7F1EA`, sand `#EFE4D6`, champagne `#E2C994`, bronze `#7B5C47`, gold `#B8975A`. Fonts: Crimson Pro (serif, stands in for Palatino/TeX Gyre Pagella) and Poppins.
- Tagline in use: "Balance begins within" (brand book). Badar's PDF says "Beauty begins within". **Not yet decided by the owner.**
- Contact address used everywhere: `help@unefemmedivine.com` (the store's contact email). Badar's PDF used `info@`.
- Instagram: `@unefemmedivine`.

## 3. What is LIVE right now
- **Shopify live theme:** "UFD live copy 21 Nov - free planner page", id `gid://shopify/OnlineStoreTheme/200867611011` (role MAIN). Previous live theme "UFD live copy 20 Nov - review badge + SEO fixes" (`.../200846541187`) is unpublished and is the rollback.
- **Pages (both visible):**
  - `/pages/free-planner` (Page `gid://shopify/Page/713101803907`, template `free-planner`): landing page with the email sign-up and, after sign-up, "Open the planner" and "Download PDF".
  - `/pages/rhythm-planner` (Page `gid://shopify/Page/713101836675`, template `rhythm-planner`): the interactive planner. Visitors who have not signed up see a "Get the free planner" button.
- **PDF:** `Rhythm-of-the-Body.pdf` is uploaded in Shopify Files (READY, 374,015 bytes, new "you" wording). Pages link to it with `{{ 'Rhythm-of-the-Body.pdf' | file_url }}`, so the file name must stay exact.
- Not linked from the menu or homepage. Intended use: Instagram bio, ads, DM replies ("send us FREE PLANNER"), WhatsApp.

## 4. How the sign-up works
- The landing page uses Shopify's native customer form (`{% form 'customer' %}`), posting `contact[email]`, `contact[first_name]` and tags `free-planner,rhythm-of-the-body,newsletter`. A required consent checkbox is validated in JS.
- After a successful post, Shopify reloads the page with `form.posted_successfully?`; a small script stores `ufd:access` in localStorage (with the first name saved just before submit as `ufd:pendingName`), and the shared script `ufd-common.js` unlocks the thank-you card. The planner page reads the same `ufd:access` key.
- It is a **soft gate**: anyone with the planner URL can still open it only if the browser has that key; otherwise they see the join button. Fine for a lead magnet.
- **Not yet verified:** that a test sign-up creates a customer tagged correctly AND marked as subscribed to email marketing. The owner must test once with their own email (incognito) and check Customers.

## 5. The planner (features)
Month calendar with four colour-coded "inner seasons" (Rest, Rise, Bloom, Restore) from first day of last period, cycle length and period length; "today" card; daily log (energy 1 to 5, mood, note); cycle chart; "Your four seasons, explained" (days computed per cycle length); season playbooks with tickable ritual ideas; calendar export (all-day events, discreet titles toggle, `.ics` download, Google Calendar per-season links, device-aware emphasis: iPhone/Mac push the `.ics`, others push Google); "Keep your record" (CSV download and print/save-as-PDF summary); "clear my data". All planner data stays in the browser (localStorage); nothing is sent to us.
Season maths (in `planner.html`): rest = period days; rise ends at `max(period+1, floor(L*0.45))`; bloom is 4 more days (capped); restore is the rest. Seasons are estimates only.

## 6. Repo map (`guides/`)
- `src/` sources: `base.css`, `common.js` (storage, toast, ics, Google links, email gate), `planner.html`, `ritual.html` (parked), `landing.html` + `landing.css` + `landing.js` (static version of the landing page), `print.css`, `print-ritual.html`, `print-planner.html`, `print-whatsapp.html`, `assets/` (logo PNGs recoloured from the brand book, cover jpgs).
- `build.py`: builds the standalone web files (`divine-ritual-guide.html`, `rhythm-planner.html`, `free-planner.html`), `_preview/` (artifact-safe copies without download/print buttons) and `_print/` (A4 sheet HTML). Run: `python3 guides/build.py`.
- PDFs: `tools/render-pdf.js` (Playwright, needs `NODE_PATH=$(npm root -g)`) then `tools/add-fields.py` (reportlab + pypdf; adds real fillable form fields). Output in `pdf/`. `tools/render-plan.js` makes `whatsapp/WhatsApp-Community-Plan.pdf`.
- `shopify/build_shopify.py` generates the theme files in `shopify/theme/` from the same sources (`layout/ufd-guide.liquid`, `sections/ufd-free-planner.liquid`, `sections/ufd-rhythm-planner.liquid`, `templates/page.free-planner.liquid`, `templates/page.rhythm-planner.liquid`, `assets/ufd-*.css|js`). **Caution:** the generated `shopify/theme/` is NOT identical to the live theme in two ways: images. Live uses `assets/ufd-word-ink.svg` and `assets/ufd-mark-gold.svg` (SVG wrappers holding base64 PNGs); the build script still emits `.png`. Update the build script before relying on it.
- `social/`: Instagram posts (`posts.html`, 6 PNGs: 3 designs x DM and website call to action) and `whatsapp-copy.txt`.
- `whatsapp/`: WhatsApp community plan PDF.
- Previews (private Artifacts): planner https://claude.ai/artifact/RwQSLpT7toHzmj54c1Aaxy, landing https://claude.ai/artifact/Kq9pmCcbwLJ4S7j6Qv38uo, ritual guide https://claude.ai/artifact/XxiqtdEUhGEHNfkWekT6uY.

## 7. Hard-won lessons for the Shopify tooling
- Theme edits: `theme_bash` + `theme_commit` on the MAIN theme only stage changes ("awaitingPublish"). Run `theme_publish` (needs the owner's yes) to make them live. `theme_publish` initially refused an unpublished copy ("only agent-created themes"), so the owner published the copy in admin once.
- **Binary assets break**: PNGs uploaded through `themeFilesUpsert` (BASE64) were stored as text and rendered as broken images. Use SVG files (with the PNG embedded as a data URI) or inline data URIs, never raw PNG theme assets.
- Long base64 strings copied by hand can silently corrupt. Always verify size and `checksumMd5` via `theme(id){ files(filenames:[...]) { nodes { size checksumMd5 } } }`.
- Hidden (unpublished) pages cannot be previewed with `theme_screenshot`; they 404.
- The sandbox cannot reach the live storefront with curl.
- `theme_bash` has no python/node and its `sed` is limited; use `awk` and heredocs. Script size limit about 65 KB.
- Shopify Email is replaced by the messaging app in this store; Shopify Flow was being installed by the owner.

## 8. Open items (priority order)
1. **Owner test** of the live sign-up (see section 4). Confirm customer, tag and email-marketing consent.
2. **Welcome email.** Nothing is automated yet. Cannot be created through the API; the owner sets it up in the Shopify messaging app (Automations, Welcome) or Klaviyo. Draft: subject "Your Rhythm of the Body planner is ready"; body: warm welcome, button to `/pages/rhythm-planner`, sign-off "Balance begins within". The landing page's line "A link to your planner is also on its way to your inbox" is shown to everyone; keep it only once the email is live, otherwise remove it from `sections/ufd-free-planner.liquid`.
3. **Email deliverability / DNS.** The owner could not reach DNS (domain at one.com; an earlier note suggested Shopify might manage it). Step-by-step guidance was given for Shopify domain authentication on one.com. Plan agreed: start sending from Shopify's default sender (may land in spam; the guide opens instantly so nothing depends on email), fix DNS later. Klaviyo was discussed as a better long-term tool; its DNS records differ from Shopify's. Awaiting: who manages DNS (Settings, Domains).
4. **Instagram posts.** 3 designs x 2 versions are finished. Captions "to follow". DM keyword: "FREE PLANNER". The link in bio should be `unefemmedivine.com/pages/free-planner`. DM replies need a person or an auto-reply tool (e.g. ManyChat).
5. **WhatsApp community.** Plan PDF done (13 pages): two spaces (announcements plus chat), six weekly pillars (Mon growth, Tue mental wellbeing, Wed routines, Thu beauty and style, Fri lifestyle, Sun self-care), four first-month themes (Boundaries and rest; Confidence and ambition; Friendship and connection; Home and calm), monthly "brand moments" (You decide, Divine Voices, Ask the founders, Free guides). Only Week 1 messages are written; **Weeks 2 to 4 still to write.** Owner said they will return to it.
6. **Compliance review needed (owner or counsel):** (a) the "What's inside" copy copied from Badar's PDF (22 active ingredients, 5,000 mg collagen; the ritual guide only); (b) the live homepage lists "Hormonal Balance", "Reduced Bloating", "More Energy", which conflicts with the no-claims rule and EU/UK advertising rules; (c) privacy policy wording ("we never share your email").
7. **Decisions pending:** tagline (Balance vs Beauty begins within); customer contact email (`help@` vs `info@`); fonts (real Sharpe/Palatino files if the owner has them).
8. Optional: regenerate `Your-Divine-Ritual.pdf`, put the ritual guide on the site later, add a homepage link, update `shopify/build_shopify.py` (see section 6), add UTM links for ads.

## 9. Who does what
- The assistant can: edit and commit repo files, build PDFs and previews, edit theme files, create or update pages, read customers and files, take theme screenshots. It cannot: create automations or emails, touch DNS, preview hidden pages, send email.
- The owner must: test sign-up, set up the welcome email and DNS, approve publishing the theme, upload files from their device, decide tagline and contact email.
- Badar (design team) made the Divine Elixir Welcome Guide (palette source) and will use the WhatsApp plan and Instagram copy blocks.

## 10. Style of working with this owner
Wants step-by-step plain-English guidance, short answers, and copy ready to paste (WhatsApp-friendly formatting with `*bold*` and `_italic_`). Asks before outward actions: always confirm before publishing, making pages visible or sending anything. Corrects scope quickly ("cycle" not "period" on posts; one guide only; planner is evergreen, no ongoing content needed).
