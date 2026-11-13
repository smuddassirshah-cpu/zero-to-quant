"""Grep every string (and stored number) of every content file for regexes.
   python docs/reviews/review-delta-ac-4-scripts/grepc.py [--in <path-substring>] [--not <path-substring>] [--n <max>] <regex> [<regex> ...]
   Prints file, JSON path and 70 characters each side."""
import glob
import json
import re
import sys

args = sys.argv[1:]
inc, exc, mx = None, None, 8
while args and args[0].startswith("--"):
    if args[0] == "--in":
        inc = args[1]
    elif args[0] == "--not":
        exc = args[1]
    elif args[0] == "--n":
        mx = int(args[1])
    args = args[2:]


def strings(d, path=""):
    if isinstance(d, (str, int, float)) and not isinstance(d, bool):
        yield path, str(d)
    elif isinstance(d, dict):
        for k, v in d.items():
            yield from strings(v, f"{path}.{k}" if path else k)
    elif isinstance(d, list):
        for i, v in enumerate(d):
            yield from strings(v, f"{path}[{i}]")


DOCS = {}
for f in sorted(glob.glob("app/content/**/*.json", recursive=True)):
    if f.endswith("manifest.json") or (inc and inc not in f) or (exc and exc in f):
        continue
    try:
        DOCS[f] = json.load(open(f))
    except Exception:
        pass

for pat in args:
    rx = re.compile(pat)
    hits = []
    for f, d in DOCS.items():
        for path, s in strings(d):
            m = rx.search(s)
            if m:
                hits.append((f.replace("app/content/", ""), path, s[max(0, m.start() - 70):m.end() + 70].replace("\n", " ")))
    print(f"/{pat}/ : {len(hits)} hit(s) in {len({h[0] for h in hits})} file(s)")
    for h in hits[:mx]:
        print("    ", h[0], h[1], "...", h[2])
