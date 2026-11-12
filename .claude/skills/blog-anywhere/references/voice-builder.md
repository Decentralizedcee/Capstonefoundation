# Voice builder

Goal: capture **how this site's owner sounds** once, write it down, and use the same voice in **every** post. A voice is only real if it is built from real evidence. Never invent a voice, a catchphrase, a story or a fact about the owner.

All files live in `blog-sites/<site>/references/`.

---

## 1. Gather evidence

Ask for, in this order of value:
1. **3 to 5 samples of their own writing or speech**: emails, posts, product descriptions, a transcript, voice-note text. **About 500 words in total** or more gives steadier numbers.
2. **A style reference** if they have one ("I want it to sound like this"). Follow `style-reference-template.md`: distil the technique, never paste a third-party article into the files.
3. Their own words about the voice: tone words (warm, direct, formal, playful, gentle...), humor level (**none**, **light**, **playful**), formal or casual, "I" or "we", how they address the reader.
4. **Off-limits:** words, phrases, topics, claims they never want.

If they have no samples, build the voice from (3) and (4) plus two calibration rounds (section 4), and say plainly that it is a first draft that gets better as they approve more writing.

## 2. Measure it

Run: `python3 <skill>/scripts/voice_tools.py stats <sample files> --out blog-sites/<site>/voice-metrics.json`

This records measurable habits: sentence length, long sentences, contractions, "I", "we" and "you" rates, questions, exclamations and reading ease. Show the owner the numbers in plain words ("You write short sentences, about 8 words on average, and you often ask the reader a question"). Under 500 words of samples means rough numbers; say so.

## 3. Write the voice files

Fill the six templates in `references/` **only from evidence**:

| File | What goes in it |
|---|---|
| `voice.md` | Who is speaking; person ("I" or "we"); how they address the reader; sentence habits; **signature phrases that actually appear in their samples** (quote them); words they never use. |
| `tone.md` | Tone words and when each applies (educational posts, announcements, sensitive topics). |
| `humor.md` | The chosen level (none, light or playful) with its rules. Keep only the matching section of the template. |
| `opinions.md` | Convictions they actually stated. Nothing else. |
| `stats.md` | Real numbers they gave, with source and date. Nothing else. |
| `stories.md` | True, permitted stories only. Anonymous unless they gave a name with permission. |

Unknown items stay as clearly marked placeholders. Never fill a gap to make the file look complete.

## 4. Calibrate (this is what makes it consistent)

1. Write a **sample paragraph (about 120 words)** on a topic from their world, in the voice you captured.
2. Ask: *"Does this sound like you? What would you change?"* Adjust the files, not just the paragraph.
3. Repeat up to **3 rounds**.
4. When they approve, save it as `references/anchor-sample.md` with a header: *"Approved voice anchor. Style reference only. Never reuse this text in posts."*
5. Re-run the stats on the **approved** paragraph plus their real samples if it helps, and update `voice-metrics.json`.

## 5. Use it in every post

Before writing: read **all** files in `references/` and `anchor-sample.md`.
While writing: use signature phrases **sparingly** (at most one per post, only where natural); never repeat the anchor text; keep to the humor level; never invent facts or stories.
After writing: run `python3 <skill>/scripts/voice_tools.py check <draft.md> blog-sites/<site>/voice-metrics.json` and fix real drift. The check is **a nudge, not a verdict**: topic and post type can legitimately move the numbers (a how-to may ask more questions). Tell the owner what drifted and why you did or did not change it.
Then read the draft against `voice.md` and `humor.md` and state the **VOICE CHECK** in the report (hook fits the tone? no generic AI phrasing? only true facts? signature phrases not overused?).

## 6. Update the voice

When the owner shares new writing or says "that does not sound like me":
- add the new samples, re-run the stats, update the files, and note the change in a short **version log** at the bottom of `voice.md` (date, what changed, why);
- never silently rewrite an approved voice.

## 7. Guardrails

- **Dignity and honesty over style.** Style never overrides truth, privacy or the owner's content rules.
- Third-party style references are for technique only.
- A voice is not a persona to hide behind. Do not write as if the owner has experiences they never described.
