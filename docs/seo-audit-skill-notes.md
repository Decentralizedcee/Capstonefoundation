# SEO audit skill: requirements noted (to build after `blog-anywhere`)

Recorded from the owner's instructions. Not built yet.

## Access prompt (the skill asks first)
The skill must **ask the person which of these they have**, so nobody has to guess:
1. A **link** to the site: a public URL or a **preview link**.
2. Whether the store/site is **password-protected**.
3. The site's **code** (for Shopify: the theme).
4. **Admin access** (a staff account, collaborator access or an access token).
5. Whether the client's **permission** exists in writing.

## Modes (set by the answers)
- **Link only (always offered):** the skill audits through the link and produces a **report that can be used to work on the site separately**. Report only. Nothing is changed.
- **Link + code:** also shows what the skill can **fix from our end** in the theme/code (on a copy, never the live site).
- **Link + code + admin:** also prepares admin-side changes (titles, descriptions, alt text, redirects) for approval, with a preview and an undo path.

Every extra access lets us see what the skill can fix from our end.

## Report
- Every finding labelled: **We fix** / **Done in the admin** (with steps) / **Platform limit** (with workaround) / **Client's decision**.
- A plain-language summary with recommendations for the client.
- Pages to audit first: **home, about, a product page, contact**. The blog is handled later by the blog skill.
- Note when a **preview link** is used: it can add the platform's own preview bar and can expire, so scores may differ from the live site.

## Credentials (the owner's rule)
- The owner connects the site **themselves**. **No password is ever pasted into the Claude chat.** Keys and passwords go in `.env` or are typed in a browser login window.

## Safety
- Never change a client's site without written permission.
- Work on a copy of the theme, never the live one. Show every change first. Keep a way to undo it.

## Context
- First target: a **Shopify** client store. Owner has been given the code and admin access by the client and will send the preview link after the skill is built.
- Platform notes: Shopify generates `robots.txt` by default and `robots.txt.liquid` can replace it (confirmed in Shopify's docs). Other Shopify details (fixed URL structure, generated sitemap, checkout limits) are from general knowledge and must be confirmed in the first real audit.
- Lighthouse was run successfully in the Claude Code environment (v13.6). Google's keyless PageSpeed API was rate-limited, so it would need a free key.
