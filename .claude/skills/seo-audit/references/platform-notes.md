# Platform notes

Mark anything not confirmed in the platform's own documentation as **to confirm**.

## Shopify
- **Confirmed (Shopify docs):** Shopify generates `robots.txt` by default, and a `robots.txt.liquid` template can replace it.
- **To confirm in the first real audit (general knowledge only):** fixed URL prefixes (`/products/`, `/collections/`, `/pages/`, `/blogs/`) cannot be changed; the sitemap is generated at `/sitemap.xml` and cannot be edited directly; checkout pages are limited; title and description are set in the page's "Search engine listing" in the admin; image alt text is set per image in the admin; redirects are managed in the admin's URL redirects; theme code (Liquid) controls the HTML around them.
- **Preview links** may add Shopify's preview bar and expire; the store may also be password-protected until launch.
- Typical labels: titles, descriptions, alt text, redirects = **Done in the admin**; theme markup (headings, schema, missing tags) = **We fix** (needs theme code and permission); fixed URL structure = **Platform limit**; copy and product descriptions = **Client's decision**.

## Other platforms
Ask which platform; do not assume. Treat any platform behaviour as **to confirm** until checked in its documentation.
