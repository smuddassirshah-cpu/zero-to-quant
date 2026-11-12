#!/usr/bin/env python3
"""Freshness search: every string of the content files matching a glob that matches a regex, with its JSON path.
   find.py '<glob under app/content>' '<regex>' [width]      (from the repo root)
   e.g. find.py 'courses/testing/*.json' '0\\.95\\^\\{?18|Šidák' 160"""
import json, glob, re, sys
pat = re.compile(sys.argv[2])
width = int(sys.argv[3]) if len(sys.argv) > 3 else 150


def walk(o, path):
    if isinstance(o, str):
        m = pat.search(o)
        if m:
            a = max(0, m.start() - width // 2)
            yield path, o[a:a + width].replace('\n', ' ')
    elif isinstance(o, dict):
        ident = o.get('id')
        for k, v in o.items():
            yield from walk(v, f'{path}.{k}' if not ident or k == 'id' else f'{path}[{ident}].{k}')
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, f'{path}[{i}]')


n = 0
for f in sorted(glob.glob('app/content/' + sys.argv[1])):
    try:
        d = json.load(open(f))
    except Exception:
        continue
    for path, snip in walk(d, ''):
        n += 1
        print(f"{f.replace('app/content/', '')} {path}: ...{snip}...")
print(f'{n} hits')
