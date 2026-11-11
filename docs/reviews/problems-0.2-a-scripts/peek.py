"""Show every string of a content file that matches a regex, with its JSON path and some context.

Usage: python3 docs/reviews/problems-0.2-a-scripts/peek.py <file.json> <regex> [width] [--full]
"""
import json
import re
import sys


def texts(o, path=''):
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from texts(v, path + '/' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from texts(v, path + f'[{i}]')


f, rx = sys.argv[1], re.compile(sys.argv[2])
w = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else 200
for p, t in texts(json.load(open(f))):
    for m in rx.finditer(t):
        print(f'{p} :: ' + (t if '--full' in sys.argv else t[max(0, m.start() - w):m.end() + w]).replace('\n', ' '))
        if '--full' in sys.argv:
            break
