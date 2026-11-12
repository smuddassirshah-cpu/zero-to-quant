#!/usr/bin/env python3
"""Print bank items by id, whole. Usage: show.py <id> [<id> ...]   (from the repo root)"""
import json, glob, sys
items = {}
for f in sorted(glob.glob('app/content/bank/*.json')):
    d = json.load(open(f))
    for it in d.get('items', []):
        items[it['id']] = (f.split('/')[-1], it)
for i in sys.argv[1:]:
    if i not in items:
        print('MISSING', i); continue
    f, it = items[i]
    print('=====', f, i)
    print(json.dumps(it, indent=1, ensure_ascii=False))
