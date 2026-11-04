"""Voice check for learner-facing text specified in a brief (CLAUDE.md voice): sentences under 20 words, no exclamation
marks, no em-dashes.  A code span or a formula counts as one word.

Usage: python3 -I voice.py            checks the problem statements in oa_code_tests.json and the section text of
                                      mocks.md written for the three new mocks (prose lines only: not tables, not code).
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def words(sentence):
    s = re.sub(r"`[^`]*`", "X", sentence)
    s = re.sub(r"\$[^$]*\$", "X", s)
    return len(s.split())


def sentences(text):
    text = re.sub(r"\s+", " ", text)
    # a full stop, question mark, colon or semicolon followed by a space ends a unit; a list joined by semicolons is read unit by unit
    return [x for x in re.split(r"(?<=[.?!:;][\"')])\s+|(?<=[.?!:;])\s+", text) if x.strip()]


def check_text(label, text, bad):
    if "!" in text:
        bad.append((label, "exclamation mark"))
    if "—" in text or "–" in text:
        bad.append((label, "dash"))
    for s in sentences(text):
        if words(s) >= 20:
            bad.append((label, f"{words(s)} words: {s[:90]}"))


def prose_of(md, start, end):
    out, fence = [], False
    for line in md.splitlines():
        if line.startswith("```"):
            fence = not fence
            continue
        if fence or line.startswith("|") or line.startswith("#"):
            continue
        out.append(line)
    return "\n".join(out)


def main():
    bad = []
    d = json.load(open(os.path.join(HERE, "oa_code_tests.json")))
    for k, v in d.items():
        check_text(k + " statement", v["statement"], bad)
    md = open(os.path.join(HERE, "..", "mocks.md")).read()
    for name in ("## mock-oa-code", "## mock-superday-research", "## mock-oa-quant-data"):
        i = md.find(name)
        if i < 0:
            continue
        j = md.find("\n## ", i + 5)
        text = prose_of(md[i:j if j > 0 else len(md)], 0, 0)
        for para in text.split("\n"):
            check_text(name, para, bad)
    for b in bad:
        print("VOICE", b)
    print("VOICE: clean" if not bad else f"{len(bad)} voice problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
