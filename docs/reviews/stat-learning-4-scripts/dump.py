"""Compact text dump of a lesson or set JSON for reading.
Usage: dump.py <file> [start] [end]   (screen or item range; quiz and summary print when no end is given)."""
import json, sys


def show(v, ind=0, key=''):
    pad = ' ' * ind
    if isinstance(v, (dict, list)) and v and len(json.dumps(v, ensure_ascii=False)) < 150:
        print(f'{pad}{key}: {json.dumps(v, ensure_ascii=False)}')
    elif isinstance(v, dict):
        if key:
            print(f'{pad}{key}:')
        for k, x in v.items():
            show(x, ind + (1 if key else 0), k)
    elif isinstance(v, list) and len(v) > 14 and all(isinstance(x, str) for x in v):
        print(f'{pad}{key}: [{len(v)} strings] {" ".join(v[:4])} ...')
    elif isinstance(v, list) and len(v) > 12 and key in ('points','grid','data','pts','values','ys','xs'):
        print(f'{pad}{key}: [{len(v)} entries] {json.dumps(v[:3], ensure_ascii=False)} ...')
    elif isinstance(v, list) and len(v) == 10 and key == 'cells':
        print(f'{pad}{key}: [10 rows]')
    elif isinstance(v, list):
        if all(not isinstance(x, (dict, list)) for x in v) or len(json.dumps(v, ensure_ascii=False)) < 110:
            print(f'{pad}{key}: {json.dumps(v, ensure_ascii=False)}')
        else:
            for i, x in enumerate(v):
                show(x, ind + 1, f'{key}[{i}]')
    else:
        print(f'{pad}{key}: {v}')


d = json.load(open(sys.argv[1]))
a = int(sys.argv[2]) if len(sys.argv) > 2 else 0
b = int(sys.argv[3]) if len(sys.argv) > 3 else 999
for k, v in d.items():
    if k in ('screens', 'items', 'quiz'):
        for i, x in enumerate(v):
            if k != 'quiz' and not (a <= i < b):
                continue
            if k == 'quiz' and b < 999:
                continue
            print(f'=== {k}[{i}]')
            show(x, 0, '')
    elif b >= 999 or a == 0:
        show(v, 0, k)
