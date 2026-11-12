"""Show where a regex hits in content files, with the JSON path and some text either side.
   python docs/reviews/review-delta-problems-ac-1-scripts/context.py '<glob under app/content>' '<regex>' [width]
The regex is matched against each string with whitespace removed (as fresh.py does)."""
import glob
import json
import re
import sys

pat, rx = sys.argv[1], re.compile(sys.argv[2], re.I)
width = int(sys.argv[3]) if len(sys.argv) > 3 else 160


def walk(o, path=""):
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            tag = v.get("id", i) if isinstance(v, dict) else i
            yield from walk(v, f"{path}[{tag}]")


for f in sorted(glob.glob("app/content/" + pat, recursive=True)):
    for path, s in walk(json.load(open(f, encoding="utf-8"))):
        t = re.sub(r"\s+", "", s)
        m = rx.search(t)
        if m:
            a = max(0, m.start() - width)
            print(f"{f.replace('app/content/', '')} {path}\n    ...{t[a:m.end() + width]}...")
