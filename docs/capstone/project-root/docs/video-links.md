# Videos to embed: Capstone Foundation

Source of truth for every video on the site. Titles, lengths and channel were read from YouTube on 6 Nov 2026. All four are on Capstone Foundation's own YouTube channel. They are **embedded** from YouTube, never downloaded and never committed.

## The videos

Video ID = the part after `/shorts/` (ignore the `?si=` tracking part of any link). Watch URL pattern: `https://www.youtube.com/shorts/<ID>`

| # | Video ID | Title (hashtags removed) | Length | What it is (per YouTube) | Suggested home (owner approves) |
|---|---|---|---|---|---|
| 1 | `Rw5ewqXteY8` | Capstone Foundation: Changing Lives Through Education | 0:30 | Overview of the Scholarship Scheme | Programs > Scholarships (could also be the one featured video on Home) |
| 2 | `jSiSsNCmEkc` | Life as a Widow in Nigeria Today: Their Stories, in Their Own Words | 2:45 | Voice of the Widows Forum members speaking | Programs > Widows Empowerment |
| 3 | `MGx__JGb-wY` | "My Daughter Got a Scholarship" \| A Widow's Story of Hope | 1:10 | A widow's testimony about the Scholarship Scheme | Programs > Scholarships and/or the Testimonials section |
| 4 | `6ah3juz598Y` | Voice of the Widows Forum: Monthly Review & Impact Update | 0:36 | Highlights from a monthly forum meeting | Programs > Widows Empowerment |

Original links the owner supplied:
- https://youtube.com/shorts/Rw5ewqXteY8
- https://youtube.com/shorts/jSiSsNCmEkc
- https://youtube.com/shorts/MGx__JGb-wY
- https://youtube.com/shorts/6ah3juz598Y

## How to embed (one reusable `VideoEmbed` component)

- **Data:** `src/data/videos.ts` with `id`, `title`, `caption`, `page`, `slot` and `approved` (**`false` by default**; a video renders only when `approved` is `true`).
- **Shape:** vertical 9:16, centred, maximum width about 360px, inside a fixed aspect-ratio box so there is **no layout shift**.
- **Click to load.** On page load show only a flat poster card (12px radius, 1px `#EBEBEB` border) with a large flat brand-green play button (at least 56px) and the video title below as text. Only when the visitor clicks does the card swap for an iframe:
  `https://www.youtube-nocookie.com/embed/<ID>?autoplay=1&rel=0&playsinline=1`
  with a `title` attribute (the video title), `allow="encrypted-media; picture-in-picture; fullscreen"`, `allowfullscreen`, `referrerpolicy="strict-origin-when-cross-origin"`. No YouTube code or cookies load before the click. This protects Lighthouse 95+ and visitor privacy.
- **Works without JavaScript.** The play button is a normal link to `https://www.youtube.com/shorts/<ID>` (new tab, `rel="noopener"`), and a visible "Watch on YouTube" text link is always present. Keyboard accessible, visible focus, accessible name "Play video: <title>". Respect `prefers-reduced-motion`.
- **Poster:** do **not** hotlink YouTube thumbnails. Use a flat `#EBEBEB` poster, or a still from the owner's own photos (`images-incoming/`, named `video-<ID>.jpg`) processed by the normal image pipeline.
- **No video files** in the repository.
- **Placement:** propose a **video slot map** (page, position, which video, caption) together with the photo slot map and **wait for approval**. Default: each video appears once. Videos may also be embedded in Stories (MDX) when relevant and approved.
- **Consent and privacy:** these videos show real people. Before any video goes live, ask the owner, for each one: who appears; that they consented to appear on this website; that no money amounts, children's surnames, diagnoses or case details are shown or spoken. Keep `approved: false` until the owner says yes.
- **Copy rule:** do **not** copy text from the YouTube titles or descriptions into page copy (they contain wording and claims that are not in the build spec). Page copy stays word for word from the spec. Use a title only as the accessible title and as a caption the owner approves.
- **Optional:** ask whether to add `VideoObject` structured data. Only with the real title, upload date and duration.
