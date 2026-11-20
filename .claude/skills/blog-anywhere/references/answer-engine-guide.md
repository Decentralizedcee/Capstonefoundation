# Writing so AI answers can find, understand and quote the post

Read this before outlining and again before writing the FAQ. It is about one thing: **being specific about the answers to the questions buyers actually ask**, so that a search engine's AI answer (Google AI Overviews / AI Mode, Gemini, ChatGPT and similar) can pull a clear, correct, quotable passage from the post.

## Where this comes from (and how far to trust each part)

- **The video:** Neil Patel, "Google's New Rules for Getting Customers" (NP Digital, 19 Nov 2026, 15:43). Studied from its full transcript. Rules 1, 2, 3 and 6 matter for blog writing; rules 4 and 5 are about Google Ads and conversion tracking and are not used here.
- **Google's own page, checked on 20 Nov 2026:** "Optimizing your website for generative AI features on Google Search" (developers.google.com/search/docs/fundamentals/ai-optimization-guide, last updated 10 Jul 2026). Points that Google states itself are marked **[Google]**.
- **Practitioner research** (the video names Mike King, Cyrus Shepard, Dan Petrovic) is marked **[practitioner]**. It matches what Google describes but is not Google's formula. Never present it as a Google rule.
- Treat all of this as guidance that can change. If it matters for a client, re-check Google's page.

## 1. Cover the related questions a buyer needs answered (query fan-out)

When someone asks a complex question, the AI can run several related searches behind the scenes and build one answer from all of them. **[Google]** Google's own example: for "how to fix a lawn that's full of weeds", the related searches might be best herbicides, removing weeds without chemicals, and preventing weeds.

What to do for each post:
1. Take the post's main buying or reader question.
2. List the **related questions a reader needs answered before they can say yes** (aim for 5 to 10). Sources: the top 3 results, the "People also ask" style questions you find while researching, the owner's own customer questions, and free question tools such as AnswerThePublic (the video's suggestion).
3. Check the post (and `site-pages.csv`) for a **specific answer to each**. If the answer is nowhere on the site, that is a gap: answer it in this post's sections or FAQ, or note it as a future post.
4. **Do not spin up a thin page or post for every sub-question.** **[Google]** Doing that mainly to gain AI answers violates its scaled-content-abuse spam policy, and a high page count does not make a site better. Fewer pieces with real answers beat many with nothing in them.

## 2. Make every answer survive being copied out of the page

The AI pulls relevant pages, then reviews the specific information on them. **[Google]** In practice the unit that gets quoted is often **one passage, not the whole article**. **[practitioner]** Self-contained, specific passages get used more.

So every paragraph that answers a question (the first paragraph under each H2, and every FAQ answer) must pass the **copy test**: paste it alone into a blank document. Is it still accurate, clear and useful? If it needs the paragraph above it to make sense, rewrite it.

How to write it (the video's weak versus strong example):
- **Weak:** "It also comes with these features, which makes it perfect for cafes like yours." Pasted alone it means nothing: which product, which features, perfect for whom?
- **Strong:** "The Neuro Duo is a dual boiler espresso machine that holds temperature across back-to-back shots. It is built for cafes doing 150 to 300 drinks a day, and it needs a dedicated 20 amp circuit."
- The recipe: **name the subject, say who it is for, and put the limit right next to the claim.**
- Open with the answer, then add detail. Do not start an answer with "It", "This", "That", "They", "These", "Also" or "As mentioned above".
- Use the actual names (the product, the ingredient, the phase, the place), not pronouns, in the sentence that makes the claim.
- State the numbers, conditions, exceptions and who it does not suit **in the same paragraph** as the claim. Facts only from the owner's materials or named sources; anything unknown is `TODO(owner)`.

## 3. FAQ answers: the rules

The FAQ is where this matters most. For every FAQ question:
1. Use a real question a reader or buyer asks, in their words. Prefer questions that map to the fan-out list in section 1.
2. **First sentence answers the question directly** (yes, no, or the answer), and **repeats the subject** so it works alone.
3. Then one to three sentences of specifics: numbers, conditions, exceptions, who it is for, and the limit. About 30 to 90 words. Shorter than about 15 words is too thin to be useful; longer than about 150 means it belongs in a section.
4. No pronoun openings, no "see above", no "click here". Never rely on the question being shown next to the answer.
5. Every answer must be true on its own and consistent with the rest of the post and the owner's other pages (same numbers, same names).
6. Do not pad the FAQ with questions nobody asks just to add pages or keywords.

## 4. Be specific, and be the real thing

- **[Google]** Content that people find unique, helpful and reliable influences AI visibility more than any other tip. Prefer a real point of view and first-hand detail over a summary of what is already everywhere. "Commodity" lists that restate common knowledge add little.
- **Proof that people and AI both use:** named customers, numbers and specific results (the video cites a survey of 100 businesses where social proof ranked highest in influence on purchase decisions, 4.7 out of 5, and price lowest, 3.4; treat it as the video's data). Only use proof the owner can show. Never invent a customer, a number or a result.
- **Keep it current.** Remove or fix claims that are out of date, discontinued, not approved by the owner or not true in every region they sell to. The video's point: a site's pages can now be turned into ad copy and answers, so an old claim can be repeated back to buyers.

## 5. What not to do (do not sell the owner these)

- **[Google]** No `llms.txt` file or special AI markup is needed for Google Search. The video makes the same point: anyone selling "AI schema for Google" is selling air.
- **[Google]** You do not need to chop content into tiny chunks or rewrite it only for AI. Write for the reader. Keep normal headings, short paragraphs and clear sections.
- **[Google]** Structured data is not required for AI search. Keep the existing Article and FAQ markup because it is useful for normal SEO, but never promise it will win AI answers.
- **[Google]** Do not chase inauthentic mentions around the web.
- Do not stuff keywords, and do not write one thin page per question.

## 6. Check and measure (tell the owner, do not claim results)

Being quoted is not the same as being chosen. **[video]** Track three separate things: (1) was a page **cited**, (2) was the brand **recommended**, (3) did a **valuable action** follow (a sale, a booking, a quote request). A post can be cited and still lose the sale.

Give the owner these checks after publishing (this skill cannot run them):
- **Search Console:** the "Generative AI performance report" shows how pages appear in Google's AI features. **[Google]**
- **A test set:** 10 questions a real buyer asks, run in AI Mode, Gemini and ChatGPT. Write down whether the brand appears, which customer it is assigned to, what strengths and weaknesses are attributed, and which sources are cited. Repeat monthly, because answers move. It is a diagnosis, not proof that one edit changed an answer.
- If a bad description of the brand is cited, trace it to its source (an old page, a directory profile) and fix what the owner controls.
- Report on customers and revenue, with citations and traffic as leading indicators, not the scoreboard.

## 7. Quick audit to run on every post (the skill does this before the report)

1. List the 5 to 10 buyer questions the post answers. Is each one answered **specifically** somewhere in it? Mark gaps.
2. Copy the first paragraph under each H2 and every FAQ answer into a blank space. Does each one still make sense alone? Rewrite the ones that do not.
3. Does each answer name its subject, say who it is for and put the limit beside the claim?
4. Are all facts true, current and consistent with the site? Is any proof invented? (It must not be.)
5. Did any section exist only to catch a keyword? Remove it.
