"""Voice checks on the eight new items' learner-facing text (prose, question, prompt, model, rubric, feedback,
explain, how; code blocks and maths spans cut; a lesson cited by number is flagged). Run from this folder with any Python 3."""
import json, re, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[3] / "app" / "content" / "courses"
ITEMS = [("markets", 3, "h-carry-two-rates"), ("micro", 3, "h-derive-tilted-quotes"), ("sql", 1, "h-cash-bonds"), ("ds", 4, "h4-save-tree"),
         ("vectors", 3, "h-bond-curve"), ("random-vars", 1, "h-build-pmf"), ("algo-think", 2, "h-split-feed"), ("algo-think", 3, "h-ring-search")]
US = r"\b(color|behavior|center|favor|analyze|optimize|organize|recognize|minimize|maximize|modeling|labeled|traveled|program\b(?!me))"
bad = 0
def texts(it):
    out = [it.get(k, "") for k in ("prose", "question", "prompt", "model", "title")]
    out += [r["text"] for r in it.get("rubric", [])]
    w = it.get("widget", {})
    out.append(w.get("how", ""))
    fb = it.get("feedback", {})
    out += [fb.get("correct", ""), fb.get("generic", "")] + list(fb.get("byKey", {}).values())
    out.append((it.get("explain") or {}).get("text", ""))
    return [t for t in out if t]
def clean(t):
    t = re.sub(r"```.*?```", " ", t, flags=re.S)
    t = re.sub(r"\$\$.*?\$\$", " X ", t, flags=re.S)
    t = re.sub(r"\$[^$]*\$", " X ", t)
    t = re.sub(r"`[^`]*`", " X ", t)
    return t
for c, n, iid in ITEMS:
    it = next(x for x in json.loads((ROOT / c / f"homework-{n}.json").read_text())["items"] if x["id"] == iid)
    longest, flags = 0, []
    for t in texts(it):
        raw = t
        t = clean(t)
        if "!" in re.sub(r"!=", "", t): flags.append("exclamation")
        if "—" in raw or "–" in raw: flags.append("em or en dash")
        if re.search(US, t, re.I): flags.append("US spelling " + re.search(US, t, re.I).group(0))
        if "$" in it.get("title", ""): flags.append("$ in title")
        if re.search(r"\b[Ll]esson \d", raw): flags.append("lesson cited by number")
        for s in re.split(r"(?<=[.?:;])\s+|\n+", t):
            longest = max(longest, len(re.findall(r"[A-Za-z0-9£][\w'’,.£%-]*", s)))
    ex = clean((it.get("explain") or {}).get("text", ""))
    nsent = len([s for s in re.split(r"(?<=[.?])\s+", ex.strip()) if s.strip()]) if ex.strip() else 0
    print(f"{c} L{n} {iid}: longest sentence {longest} words, explain sentences {nsent}, flags {sorted(set(flags)) or 'none'}")
    if flags or longest > 35 or nsent > 3:
        bad += 1
sys.exit(1 if bad else 0)
