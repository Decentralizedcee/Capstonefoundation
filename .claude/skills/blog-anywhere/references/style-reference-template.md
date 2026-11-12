# Turning a writing sample into a style guide

Use this when the owner gives a writing sample, an article or a description of a style they love ("this is how I would like most of the content to sound").

## Rules
- **Distil, never copy.** The result is a short guide of technique, not a pasted article. Third-party text is not stored in the project. Keep at most three short example lines, labelled "for study only, never reuse", and name the source.
- The style **sits on top of** the owner's stated voice and tone. It never replaces them.
- It must obey the project's content rules (privacy, quoted texts, no invented facts, humor level).

## Create `references/<style-name>.md` with these sections
1. **Status and source:** owner-approved; where the sample came from; the owner's own words about it.
2. **Where it applies:** a table (for example blog posts: yes, moderate; new short copy: light; fixed copy from a build spec: never; quoted texts such as laws or standards: never).
3. **What the style is:** the marks of the style in 3 to 5 bullets (for example vivid imagery, emotional resonance, rhythm, originality, specificity).
4. **How to write it:** the techniques, each in one or two sentences.
5. **Where to place it:** for example the opening line, a turning point, a key idea, the closing line. Give a working number per post (for example 2 to 4 moments) and say the owner can change it.
6. **Guardrails for this business** (these override the technique): plain words and short sentences if the voice says so; an imagery palette that fits the brand and avoids the opposite mood; **honesty** (imagery never smuggles in an invented fact, person, event or result); **dignity** (never make a real person's suffering decorative); humor rules from `humor.md`; never alter fixed or quoted texts; never reuse the sample lines.
7. **Plain to styled samples:** a small table of "plain" and "styled" lines written fresh for this business, labelled "style samples, not facts, not to be reused".
8. **Quick check before a post is finished:** a short checkbox list.

## Then
- Add the file name to the Stack adapter's or CLAUDE.md's voice list, so the `blog` skill reads it.
- Tell the owner where the file is and ask them to read and correct it.
