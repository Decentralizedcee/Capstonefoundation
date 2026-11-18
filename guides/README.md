# Une Femme Divine guides

Two interactive lead-magnet guides, each a single self-contained HTML file.

| File | Guide |
| --- | --- |
| `divine-ritual-guide.html` | Your Divine Ritual (welcome guide, ritual builder, 7-day journal, moment cards, FAQ) |
| `rhythm-planner.html` | Rhythm of the Body (cycle planner, month view, daily log, calendar export) |

Edit `src/`, then run `python3 guides/build.py`. `_preview/` holds copies without download buttons, for viewers that block them.

## PDF editions (A4, fillable)
`pdf/Your-Divine-Ritual.pdf` and `pdf/Rhythm-of-the-Body.pdf` are designed paper layouts with real fillable form fields.
Rebuild them after editing `src/print-*.html` or `src/print.css`:

    python3 guides/build.py
    NODE_PATH=$(npm root -g) node guides/tools/render-pdf.js
    python3 guides/tools/add-fields.py

## Connect the email capture
Both pages have a `UFD_CONFIG` block near the bottom. Until you set `provider`, the form unlocks the guide but sends the email nowhere.

- `provider: 'shopify'` plus `shopDomain`: posts to your store's customer form and tags the contact. Works best when the page is hosted on the store's own domain.
- `provider: 'webhook'` plus `webhookUrl`: posts JSON `{email, name, tags, source, consent}` to Klaviyo, Mailchimp, Make or Zapier.

Also set `contactEmail`, `shopUrl` and `otherGuideUrl` (the two guides link to each other).

## Notes
- The email gate is client-side. It suits a lead magnet, not secret content.
- Planner data (dates, moods, notes) is stored only in the visitor's browser and never sent anywhere.
- Fonts: Bodoni Moda and DM Sans load from Google Fonts as stand-ins for Sharpe and DejaVu Sans. To use the real fonts, add `@font-face` rules named `Sharpe` and `DejaVu Sans` in `src/base.css`.
- No health claims appear in the copy, in line with the brand book.
