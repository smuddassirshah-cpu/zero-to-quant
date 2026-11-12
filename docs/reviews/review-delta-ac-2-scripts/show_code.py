#!/usr/bin/env python3
"""Reading aid: print a code item (bank coding task or ci drill) whole, tests numbered from 1.
Usage (repo root): python docs/reviews/review-delta-ac-2-scripts/show_code.py <id> [<id> ...]"""
import glob, json, sys


def walk(o, f, out):
    if isinstance(o, dict):
        if 'id' in o and isinstance(o.get('tests'), list):
            out[o['id']] = (f, o)
        elif 'id' in o and isinstance(o.get('widget'), dict) and o['widget'].get('kind') == 'code':
            out[o['id']] = (f, o)
        for v in o.values():
            walk(v, f, out)
    elif isinstance(o, list):
        for v in o:
            walk(v, f, out)


items = {}
for f in sorted(glob.glob('app/content/bank/coding-*.json') + glob.glob('app/content/drills/**/*.json', recursive=True)):
    walk(json.load(open(f)), f, items)
for i in sys.argv[1:]:
    if i not in items:
        print('MISSING', i)
        continue
    f, it = items[i]
    w = it.get('widget', it)
    print('=====', f, i)
    for k, v in it.items():
        if k in ('widget', 'tests', 'examples', 'solution', 'starter', 'planted'):
            continue
        print(f'{k}: {json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v}')
    for k in ('how', 'starter', 'solution'):
        if k in w:
            print(f'-- {k}\n{w[k]}')
    print('-- examples')
    for e in w.get('examples', []):
        print('  ', json.dumps(e, ensure_ascii=False)[:400])
    print('-- tests')
    for n, t in enumerate(w.get('tests', []), 1):
        print(f'  {n}', json.dumps(t, ensure_ascii=False)[:400])
    for n, p in enumerate(w.get('planted', it.get('planted', []))):
        print(f'-- planted[{n}]', json.dumps({k: v for k, v in p.items() if k != 'code' and k != 'solution'}, ensure_ascii=False)[:300])
