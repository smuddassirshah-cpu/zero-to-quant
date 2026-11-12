#!/usr/bin/env python3
"""What each fix-pass commit really changed, part by part, to hold against its "every graded answer, band or item that
   changed" list. For each problems file touched by a commit it prints, per item and part, the leaf paths that differ.
   difflist.py <commit> [--values]      (from the repo root)"""
import json, subprocess, sys
rev = sys.argv[1]
VALUES = '--values' in sys.argv


def git(*a):
    return subprocess.run(['git', *a], capture_output=True, text=True, check=True).stdout


def flat(o, p=''):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from flat(v, f'{p}.{k}' if p else k)
    elif isinstance(o, list):
        ids = all(isinstance(v, dict) and 'id' in v for v in o) and o
        for i, v in enumerate(o):
            yield from flat(v, f'{p}[{v["id"] if ids else i}]')
    else:
        yield p, o


files = [f for f in git('show', '--name-only', '--format=', rev).split() if '/problems-' in f and f.endswith('.json')]
for f in files:
    old = json.loads(git('show', f'{rev}^:{f}'))
    new = json.loads(git('show', f'{rev}:{f}'))
    oi = {i['id']: i for i in old['items']}
    for it in new['items']:
        o = oi.get(it['id'])
        if o is None:
            print(f'{f} {it["id"]}: NEW ITEM')
            continue
        top_o = dict(flat({k: v for k, v in o.items() if k != 'parts'}))
        top_n = dict(flat({k: v for k, v in it.items() if k != 'parts'}))
        ch = sorted(k for k in set(top_o) | set(top_n) if top_o.get(k) != top_n.get(k))
        if ch:
            print(f'{f.split("/")[-2]} {it["id"]} item: {", ".join(ch)}')
        if len(o['parts']) != len(it['parts']):
            print(f'{f.split("/")[-2]} {it["id"]}: parts {len(o["parts"])} -> {len(it["parts"])}')
        for k, p in enumerate(it['parts']):
            q = o['parts'][k] if k < len(o['parts']) else {}
            a, b = dict(flat(q)), dict(flat(p))
            ch = sorted(x for x in set(a) | set(b) if a.get(x) != b.get(x))
            if ch:
                print(f'{f.split("/")[-2]} {it["id"]} part {k + 1}: {", ".join(ch)}')
                if VALUES:
                    for x in ch:
                        if 'widget' in x:
                            print(f'      {x}: {a.get(x)!r} -> {b.get(x)!r}')
