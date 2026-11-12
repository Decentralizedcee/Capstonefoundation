#!/usr/bin/env python3
"""Voice tools for the blog-anywhere skill. Standard library only.

  python3 voice_tools.py stats <file> [<file> ...] [--out voice-metrics.json]
      Measures how the person writes (from their samples) and prints the numbers.
      With --out, saves them as the site's voice metrics (with a default tolerance).

  python3 voice_tools.py check <draft> <voice-metrics.json> [--strict]
      Compares a draft with the saved metrics and says where it drifts.
      Advisory only: a nudge, not a judge. Exit code is 0 unless --strict and something drifted.

Text may be plain text, Markdown or HTML. Tags and Markdown marks are ignored.
"""
import json
import re
import sys

CONTRACTION = re.compile(
    r"\b(?:\w+n['’]t|\w+['’](?:re|ll|ve|m|d)|(?:it|that|he|she|there|here|what|who|where|let)['’]s)\b", re.I)
FIRST_SING = {"i", "i'm", "i’m", "i've", "i’ve", "i'll", "i’ll", "i'd", "i’d", "my", "me", "mine", "myself"}
FIRST_PLUR = {"we", "we're", "we’re", "we've", "we’ve", "we'll", "we’ll", "we'd", "we’d", "our", "us", "ours", "ourselves"}
SECOND = {"you", "your", "yours", "you're", "you’re", "you've", "you’ve", "you'll", "you’ll", "you'd", "you’d", "yourself"}


def clean(text):
    text = re.sub(r"<(script|style)\b.*?</\1>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"^---\n.*?\n---\n", " ", text, flags=re.S)           # front matter
    text = re.sub(r"```.*?```", " ", text, flags=re.S)                   # code blocks
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)                    # images
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)                 # links keep text
    text = re.sub(r"^\s{0,3}#{1,6}\s+", "", text, flags=re.M)            # headings marks
    text = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", text, flags=re.M)     # list marks
    text = re.sub(r"[*_`>]+", "", text)
    return text


def split_sentences(text):
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    out = []
    for p in paras:
        p = re.sub(r"\s+", " ", p).strip()
        parts = re.split(r"(?<=[.!?])[\"')\]]*\s+(?=[A-Z0-9\"'(\[])", p)
        out += [s.strip() for s in parts if re.search(r"[A-Za-z]", s)]
    return out


def tokens(sentence):
    return re.findall(r"[A-Za-z]+(?:['’][A-Za-z]+)*", sentence)


def syllables(word):
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups)
    if w.endswith("e") and not w.endswith(("le", "ee")) and n > 1:
        n -= 1
    return max(n, 1)


def measure(raw):
    text = clean(raw)
    sents = split_sentences(text)
    words_all = []
    lens = []
    for s in sents:
        t = tokens(s)
        lens.append(len(t))
        words_all += t
    nw, ns = len(words_all), len(sents)
    if nw < 30 or ns < 3:
        raise ValueError("Not enough text to measure (need at least about 30 words and 3 sentences).")
    low = [w.lower() for w in words_all]
    per100 = lambda c: round(100.0 * c / nw, 2)
    pct = lambda c: round(100.0 * c / ns, 2)
    syl = sum(syllables(w) for w in words_all)
    flesch = 206.835 - 1.015 * (nw / ns) - 84.6 * (syl / nw)
    return {
        "words": nw,
        "sentences": ns,
        "avg_sentence_len": round(nw / ns, 2),
        "long_sentence_pct": pct(sum(1 for n in lens if n > 25)),
        "avg_word_len": round(sum(len(w) for w in words_all) / nw, 2),
        "contractions_per100": per100(len(CONTRACTION.findall(text))),
        "first_person_singular_per100": per100(sum(1 for w in low if w in FIRST_SING)),
        "first_person_plural_per100": per100(sum(1 for w in low if w in FIRST_PLUR)),
        "second_person_per100": per100(sum(1 for w in low if w in SECOND)),
        "question_pct": pct(sum(1 for s in sents if s.endswith("?"))),
        "exclamation_pct": pct(sum(1 for s in sents if s.endswith("!"))),
        "reading_ease": round(flesch, 1),
    }


# (key, label, kind, floor)   kind: rel = relative tolerance with floor, abs = absolute points
RULES = [
    ("avg_sentence_len", "Average sentence length (words)", "rel", 5.0),
    ("long_sentence_pct", "Long sentences (over 25 words), % of sentences", "rel", 5.0),
    ("contractions_per100", "Contractions per 100 words", "rel", 1.0),
    ("first_person_singular_per100", "'I / my' per 100 words", "rel", 1.0),
    ("first_person_plural_per100", "'we / our' per 100 words", "rel", 1.0),
    ("second_person_per100", "'you / your' per 100 words", "rel", 1.0),
    ("question_pct", "Questions, % of sentences", "rel", 4.0),
    ("exclamation_pct", "Exclamations, % of sentences", "rel", 3.0),
    ("reading_ease", "Reading ease (higher is easier)", "abs", 10.0),
]


def cmd_stats(args):
    out = None
    if "--out" in args:
        i = args.index("--out")
        out = args[i + 1]
        args = args[:i] + args[i + 2:]
    if not args:
        print(__doc__)
        sys.exit(2)
    text = ""
    for p in args:
        with open(p, encoding="utf-8", errors="replace") as fh:
            text += "\n\n" + fh.read()
    try:
        m = measure(text)
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    for k, label, *_ in RULES:
        print(f"{label}: {m[k]}")
    print(f"(measured from {m['words']} words in {m['sentences']} sentences)")
    if m["words"] < 500:
        print("NOTE: under 500 words is a thin sample, so these numbers are rough. Add more of the person's writing for steadier checks.")
    if out:
        with open(out, "w", encoding="utf-8") as fh:
            json.dump({"tolerance": 0.3, "metrics": m}, fh, indent=2)
        print(f"Saved: {out}")


def cmd_check(args):
    strict = "--strict" in args
    args = [a for a in args if a != "--strict"]
    if len(args) < 2:
        print(__doc__)
        sys.exit(2)
    try:
        with open(args[1], encoding="utf-8") as fh:
            saved = json.load(fh)
    except FileNotFoundError:
        print("NOTE: no saved voice numbers at that path (the voice for this post came from a menu choice or a description, "
              "not from writing samples), so there is nothing to compare. Judge the draft against the voice brief instead.")
        return
    base, tol = saved["metrics"], float(saved.get("tolerance", 0.3))
    with open(args[0], encoding="utf-8", errors="replace") as fh:
        try:
            d = measure(fh.read())
        except ValueError as e:
            print(f"ERROR: {e}")
            sys.exit(1)
    if d["words"] < 300:
        print(f"NOTE: the draft has only {d['words']} words, so these results are rough. Longer drafts give steadier results.")
    drift = 0
    for key, label, kind, floor in RULES:
        b, v = base[key], d[key]
        if kind == "abs":
            ok = abs(v - b) <= floor
        else:
            ok = abs(v - b) <= tol * max(b, floor)
        if not ok:
            drift += 1
        direction = "higher" if v > b else "lower"
        note = "" if ok else f"   <- drifts ({direction} than usual)"
        print(f"{'OK   ' if ok else 'DRIFT'}  {label}: draft {v} vs your usual {b}{note}")
    print(f"Summary: {len(RULES) - drift} in range, {drift} drifting. This is a nudge, not a verdict.")
    if strict and drift:
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "stats":
        cmd_stats(sys.argv[2:])
    elif len(sys.argv) >= 2 and sys.argv[1] == "check":
        cmd_check(sys.argv[2:])
    else:
        print(__doc__)
        sys.exit(2)
