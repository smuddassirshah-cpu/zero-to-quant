"""Delta read AC-1: reuse search for the six re-authored items, and a voice check of every changed item.

Every string of every JSON file under app/content is read with all whitespace removed (so `4 & 2 & 1` and `4&2&1` match, and
`[[5, 10], [10, 30]]` matches `[[5,10],[10,30]]`). Each needle is a plain string, or a regex when it starts with `re:`.
A hit in the item's own file is counted only when it lies outside the item itself.

Run from the repo root:  python docs/reviews/review-delta-problems-ac-1-scripts/fresh.py [--all]
(--all prints every hit; the default prints at most 12 files per needle.)"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from dump import ITEMS, find, load  # noqa: E402

ALL = "--all" in sys.argv


def squash(s):
    return re.sub(r"\s+", "", s)


NEEDLES = {
    "p-courier-rounds": [
        r"0&3&2\\4&1&1\\0&6&7", r"4&1&1\\0&3&2\\0&6&7", r"4&1&1\\0&3&2\\0&0&3", "[[0,3,2],[4,1,1],[0,6,7]]", "[[4,1,1],[0,3,2],[0,6,7]]",
        "0&3&2", "0&6&7", "4&1&1", "(18,15,45)", "(15,18,45)", "(15,18,9)", "(2,4,3)", "courier", "signed-for", "re:deliveryrounds?",
    ],
    "p-tilted-gantry": [
        "(1,0,2)", "(1,1,0)", "(0,2,k)", "(0,2,-4)", "(6,2,c)", "(6,2,8)", "(6,0,1)", "(4,2,0)", "(2,-2,1)", r"1&1&0\\0&1&2\\2&0&k", r"1&1&0\\0&1&2",
        "gantry", "3Dprinter", "re:motors?", "tilt",
    ],
    "p-futures-packages": [
        r"1&0&1\\-1&1&-2\\0&-1&1", r"1&0&1\\-1&1&-2", "(5,-2,c)", "(5,-2,-3)", "(5,3,0)", "(3,5,2)", "(-1,1,1)", "(7,1,2)", "(9,-10,1)",
        "butterfl", "re:Septemberfutures|futureson", "packages",
    ],
    "p-vinyl-cutter": [
        r"3&k\\2&4", r"3&2\\2&4", "[[3,2],[2,4]]", "[[3,k],[2,4]]", "12-2k", "12-4=8", "vinyl", "sign-maker", "re:logoofarea", "squashedflat",
    ],
    "p-gas-hubs": [
        "(0,1,2,3,4)", "(3.5,0,-0.5,-3,-5)", "(2,1,-2,-2,-4)", "(1.5,-1,1.5,-1,-1)", "[[5,10],[10,30]]", r"5&10\\10&30", "[-5,-30]", "[-5,-25]",
        "(3,-2)", "(2,-1.5)", "(1,-0.5)", "0+1+4+9+16", "5/7.5", "41.5", "re:gasprice|gashub", "therm", "temperatureanomaly", "re:hub[NS]\\b",
    ],
    "p-river-gauges": [
        r"4&2&1\\2&3&1\\1&1&c", r"4&2&1\\2&3&1", "4&2&1", "2&3&1", "[[4,2,1],[2,3,1]", "[[4,2],[2,3]]", r"4&2\\2&3", "8c-3", "c-0.375", "(-0.125,-0.25,1)", "(-1/8,-1/4,1)",
        "0.125z_A", "1.625", "straingauge", "bridgecable", "amplifier", "re:gauge[ABC]\\b",
    ],
}

files = sorted(glob.glob("app/content/**/*.json", recursive=True))


def strings_of(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings_of(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings_of(v)


def text_of(o):
    return squash(" | ".join(strings_of(o)))


texts = {f: text_of(json.load(open(f, encoding="utf-8"))) for f in files}
print(f"{len(files)} content files read")
total = 0
for path, pid in ITEMS:
    if pid not in NEEDLES:
        continue
    own = f"app/content/courses/{path}.json"
    it = find(load(path), pid)
    own_item = text_of(it)
    # the own file with this item's text taken out, so a hit in a sister item of the same set still shows
    raw = json.load(open(own, encoding="utf-8"))
    rest = text_of([x for x in raw["items"] if x["id"] != pid])
    print(f"\n== {pid} ({path})")
    for nd in NEEDLES[pid]:
        rx = re.compile(nd[3:] if nd.startswith("re:") else re.escape(nd), re.I)
        ok_own = bool(rx.search(own_item))
        hits = [f for f, t in texts.items() if f != own and rx.search(t)]
        if rx.search(rest):
            hits.append(own + " (another item of the same set)")
        total += len(hits)
        tag = "" if ok_own else "   [needle not in the item itself: check the spelling]"
        print(f"  {nd!r}: {len(hits)} other file(s){tag}")
        for h in hits if ALL else hits[:12]:
            print("      " + h.replace("app/content/", ""))
        if not ALL and len(hits) > 12:
            print(f"      ... and {len(hits) - 12} more (--all)")
print(f"\nfresh: {total} hits to judge")

# ---- voice of every changed item: no exclamation mark, no em-dash or en-dash, no dollar money, no American spelling
bad = 0
US = re.compile(r"\b(color|center|meter\b|liter|analyze|normalize|standardize|organize|modeling|modeled|labeled|traveled|neighbor|favor|behavior|gray)\w*", re.I)
for path, pid in ITEMS:
    it = find(load(path), pid)

    def strings(o):
        if isinstance(o, str):
            yield o
        elif isinstance(o, dict):
            for k, v in o.items():
                if k not in ("id", "tex", "answer", "accept", "skills", "kind", "keyboard"):
                    yield from strings(v)
        elif isinstance(o, list):
            for v in o:
                yield from strings(v)

    for s in strings(it):
        plain = re.sub(r"\$[^$]*\$", " MATH ", s.replace("$$", "$"))
        plain = re.sub(r"`[^`]*`", " CODE ", plain)
        for name, rx in (("exclamation mark", r"!"), ("dash", "[—–]"), ("dollar", r"\$\d|USD|dollars?")):
            if re.search(rx, plain):
                bad += 1
                print(f"VOICE {pid}: {name}: {s[:90]}")
        m = US.search(plain)
        if m:
            bad += 1
            print(f"VOICE {pid}: spelling {m.group(0)!r}: {s[:90]}")
print(f"voice: {bad} hits over {len(ITEMS)} items")
