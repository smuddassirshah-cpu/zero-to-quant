"""Print every string of the content files matching a glob that matches a regex, with context, for reading.

Run from the repo root: python docs/reviews/delta-problems-aa-3-scripts/context.py '<glob under app/content>' '<regex>' [width]
Example: context.py 'courses/trig/l13*.json' '-0\\.5|7\\\\pi\\}\\{6\\}'
"""
import glob
import json
import re
import sys

pat = re.compile(sys.argv[2])
width = int(sys.argv[3]) if len(sys.argv) > 3 else 110


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)


for f in sorted(glob.glob('app/content/' + sys.argv[1], recursive=True)):
    seen = set()
    for s in strings(json.load(open(f))):
        for m in pat.finditer(s):
            snip = s[max(0, m.start() - width):m.end() + width].replace('\n', ' ')
            if snip[:50] in seen:
                continue
            seen.add(snip[:50])
            print(f.split('app/content/')[1][:40], '|', snip)
