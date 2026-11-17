"""Mechanical check of the 63 `[rounding-tie]` slip hits of engine pass 9.

For every flagged `wrong` value the hit message names the two roundings at the asked
places. A learner who makes the slip types the nearer one. This script asks which band
(key first, then the `wrong` list in order, as the grader does) takes each rounding.

Usage (from the repo root): python docs/reviews/review-pass9-hits-scripts/slip_bands.py
Prints one line per hit and a summary. `near` is the rounding nearer the stored value.
"""
import json, re, os

ROOT = os.path.join(os.path.dirname(__file__), '..', '..', '..')
EPS = 1e-9


def half(value, tol):
    h = 0.0
    if 'abs' in tol:
        h = max(h, tol['abs'])
    if 'rel' in tol:
        h = max(h, abs(value) * tol['rel'])
    return h


def taker(w, v):
    """Name of the band that takes a typed value v (already in stored units)."""
    if abs(v - w['answer']) <= half(w['answer'], w['tol']) + EPS * max(1, abs(v)):
        return 'KEY'
    for x in w.get('wrong', []):
        if isinstance(x.get('value'), (int, float)) and abs(v - x['value']) <= half(x['value'], x.get('tol', {'abs': 0})) + EPS * max(1, abs(v)):
            return x['id']
    return 'generic'


rows = []
for line in open(os.path.join(ROOT, 'docs/reports/engine-pass-9-hits.md'), encoding='utf-8'):
    m = re.match(r'- \[rounding-tie\] (courses/\S+) \| (\S+) \| part (\d+) \| wrong "([^"]+)" \(([-\d.e]+)\) .*roundings \(([-\d.e]+), ([-\d.e]+)\)', line)
    if not m:
        continue
    f, pid, part, wid, val, r1, r2 = m.groups()
    d = json.load(open(os.path.join(ROOT, 'app/content', f), encoding='utf-8'))
    it = [i for i in d['items'] if i.get('id') == pid][0]
    w = it['parts'][int(part) - 1]['widget']
    val, r1, r2 = float(val), float(r1), float(r2)
    near, far = (r1, r2) if abs(r1 - val) <= abs(r2 - val) else (r2, r1)
    tn, tf = taker(w, near), taker(w, far)
    rows.append((f[8:], pid, part, wid, val, near, tn, far, tf))
    flag = '' if tn == wid else '  <-- near rounding not on its own line'
    print(f'{f[8:]} | {pid} | part {part} | {wid} {val} | near {near} -> {tn} | far {far} -> {tf}{flag}')

print()
print('hits', len(rows))
print('near rounding on its own line:', sum(1 for r in rows if r[6] == r[3]))
print('near rounding elsewhere:', [(r[0], r[1], r[3], r[6]) for r in rows if r[6] != r[3]])
print('far rounding on its own line too:', sum(1 for r in rows if r[8] == r[3]))
print('far rounding taken by the key:', [(r[0], r[1], r[3]) for r in rows if r[8] == 'KEY'])
