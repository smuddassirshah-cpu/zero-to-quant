#!/usr/bin/env python3
"""Freshness search by numbers and words, not by wording (fresh-check compares wording only).
For each probe (own item id, list of regexes) print every smallest JSON object in app/content
(a screen, a part, an item) whose joined strings match ALL the regexes, other than the item itself.
Usage: find.py [probe-file.json]     (from the repo root; default probes are the re-authored items)
       find.py -e '<re>' -e '<re>' ... (ad hoc)"""
import json, glob, re, sys, os

def strings(o):
    if isinstance(o, str): yield o
    elif isinstance(o, (int, float)) and not isinstance(o, bool): yield repr(o)
    elif isinstance(o, list):
        for x in o: yield from strings(x)
    elif isinstance(o, dict):
        for x in o.values(): yield from strings(x)

def walk(o, path, out, res):
    """smallest dicts matching all regexes"""
    if isinstance(o, dict):
        txt = ' | '.join(strings(o))
        if not all(r.search(txt) for r in res): return False
        hit_child = False
        for k, v in o.items():
            if walk(v, path + [o.get('id', k) if isinstance(v, dict) else k], out, res): hit_child = True
        if not hit_child and len(txt) <= LIMIT: out.append(('/'.join(str(p) for p in path) + ':' + str(o.get('id', '')), txt[:230]))
        return True
    if isinstance(o, list):
        h = False
        for i, x in enumerate(o):
            if walk(x, path + [x.get('id', i) if isinstance(x, dict) else i], out, res): h = True
        return h
    return False

LIMIT = 2500   # a whole lesson or file that happens to hold every number somewhere is not a shared item
FILES = [f for f in glob.glob('app/content/**/*.json', recursive=True) if not f.endswith('manifest.json')]
DOCS = {}
def docs():
    if not DOCS:
        for f in FILES:
            try: DOCS[f] = json.load(open(f))
            except Exception: pass
    return DOCS

def probe(own, regexes, show=True):
    res = [re.compile(r) for r in regexes]
    hits = []
    for f, d in docs().items():
        out = []
        walk(d, [], out, res)
        for p, t in out:
            if own and p.endswith(':' + own): continue
            if own and ('/' + own + '/') in ('/' + p + '/'): continue
            hits.append((f.replace('app/content/', ''), p, t))
    if show:
        print(f'## {own or "ad hoc"}  {regexes}  -> {len(hits)} hit(s)')
        for h in hits[:12]: print('   ', h[0], '|', h[1], '|', h[2][:200].replace('\n', ' '))
    return hits

if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == '-e':
        probe(None, a[1::2])
    else:
        for own, regs in json.load(open(a[0] if a else os.path.join(os.path.dirname(__file__), 'fresh-probes.json'))):
            probe(own, regs)
