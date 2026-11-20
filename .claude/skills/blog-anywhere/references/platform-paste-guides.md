# Where to paste: platform guides

The preview page contains a short version of these. Give the owner the guide for **their** platform, one step at a time if they are a beginner. **Menu names change between versions**, so say "look for the closest match" and never claim a menu is exactly there. The steps below are from general knowledge of these platforms, not checked against each platform's current documentation.

## Two ways to paste the post body
- **Formatted:** in the preview page press **Copy formatted post**, then paste into the platform's normal (visual) editor. Headings, lists and links should carry over. This is the easiest way.
- **HTML:** press **Copy HTML code**, switch the editor to its **HTML**, **code** or **custom HTML** view, and paste there. Use this if formatting looks wrong when pasted.
After pasting, check the preview on the platform, because each editor handles pasted text a little differently.

## Shopify
1. Shopify admin → **Online Store** → **Blog posts** → **Create blog post**.
2. Paste the **Title**. In **Content**, paste the formatted post, or click the **<>** (Show HTML) button and paste the HTML code.
3. Fill **Excerpt**, choose the **Blog**, add **Tags**, and set the **Featured image** with its alt text.
4. Under **Search engine listing**, choose **Edit**, then paste the **Page title** (the SEO title), **Meta description** and **URL handle** (the slug).
5. Save as **Hidden** first, preview, then set to **Visible**.
- **Structured data:** many Shopify themes already add article data. Check the page with Google's Rich Results Test before pasting ours, so it is not duplicated. Most of the time, skip it.
- **Images:** upload them in the editor or in **Content → Files**, then insert them where the markers are.

## WordPress
1. **Posts** → **Add New**. Paste the **Title**.
2. Paste the formatted post into the editor, or add a **Custom HTML** block and paste the HTML code.
3. In the post settings set the **URL slug**, **Excerpt**, **Categories**, **Tags** and the **Featured image** with alt text.
4. Paste the **SEO title** and **Meta description** into your SEO plugin's boxes (for example Yoast or Rank Math).
5. Save as a draft, preview, then publish.
- **Structured data:** SEO plugins usually add it. Check before pasting ours.

## Wix, Squarespace, Webflow, Ghost, others
1. Create a new blog post. Paste the **Title**.
2. Paste the formatted post into the visual editor. If there is an HTML, code or embed block, paste the HTML code there. **Ghost** also accepts Markdown (use **Copy Markdown**).
3. Find the post's **SEO** or **search** settings for the title, description and URL slug, and the fields for excerpt, tags and featured image.
4. Save as a draft, preview, then publish.

## Always
- Replace every image marker and every `[[INTERNAL:...]]` link, and remove any `TODO` note, **before** publishing.
- Publish as **draft or hidden first**, look at it on a phone-sized window, then make it live.
- After it is live, request indexing in Google Search Console if the site is set up there.
