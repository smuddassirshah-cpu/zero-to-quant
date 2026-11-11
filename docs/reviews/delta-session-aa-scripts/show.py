"""Print a problem item or a drill compactly.

show.py <json file> [item id ...]      (problem set: only the named items)
show.py <drill json> [--skip key,...]  (drill: every field but the skipped ones)
"""
import json
import sys


def walk(o, ind=0):
    pad = '  ' * ind
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, (dict, list)):
                print(f'{pad}{k}:')
                walk(v, ind + 1)
            else:
                print(f'{pad}{k}: {v}')
    elif isinstance(o, list):
        for i, v in enumerate(o):
            if isinstance(v, (dict, list)):
                print(f'{pad}[{i}]')
                walk(v, ind + 1)
            else:
                print(f'{pad}- {v}')


args = sys.argv[1:]
skip = []
if '--skip' in args:
    i = args.index('--skip')
    skip = args[i + 1].split(',')
    del args[i:i + 2]
d = json.load(open(args[0]))
ids = args[1:]
for k in skip:
    d.pop(k, None)
if not ids:
    walk(d)
else:
    for p in d.get('problems', d.get('items', [])):
        if p.get('id') in ids:
            print('=' * 30, p['id'])
            walk(p)
