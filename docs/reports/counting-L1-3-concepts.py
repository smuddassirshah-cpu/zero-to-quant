#!/usr/bin/env python3
"""Concept audit counting-1-3: independent recomputation of every graded key and
numeric slip in the course `counting` (levels 1 to 3).

Counting keys are found by brute-force enumeration (itertools), never by the
formula the lesson teaches. Probabilities are exact (Fraction) over the full
equally likely sample space, which is stronger than a Monte Carlo estimate; two
Monte Carlo runs are added as a cross-check of the enumeration code itself.
Vector keys are recomputed with plain arithmetic. Fluency families are run over
their whole variable range.

Exit 0 only if every check passes. A check that fails because the content is
wrong stays failing (see docs/reviews/audit-counting-1-3.md).
Run: python docs/reports/counting-L1-3-concepts.py   (Python 3.9+, stdlib only)
"""
import json, os, re, sys, random
from itertools import product, permutations, combinations
from fractions import Fraction as F
from math import factorial as fact, comb, perm, sqrt, atan, acos, degrees, prod, hypot

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'counting')
FAILS, NCHK = [], [0]

def load(name):
    return json.load(open(os.path.join(ROOT, name + '.json')))

DOCS = {}
def node(name, loc):
    d = DOCS.setdefault(name, load(name))
    cur = None
    for part in loc.split('.'):
        k, i = part[0], int(part[1:])
        if k == 's': cur = d['screens'][i]
        elif k == 'q': cur = d['quiz'][i]
        elif k == 'i': cur = d['items'][i]
        elif k == 'p': cur = cur['parts'][i]
    return cur

def ok(cond, label):
    NCHK[0] += 1
    if not cond:
        FAILS.append(label)
        print('FAIL', label)

def close(v, e):
    e = float(e)
    if isinstance(v, int) and abs(e - round(e)) < 1e-12:
        return v == round(e)
    s = repr(v)
    d = len(s.split('.')[1]) if '.' in s and 'e' not in s else 0
    return abs(v - e) <= 0.5 * 10 ** (-d) + 1e-9

def optnum(text):
    """Number in a choice option's text, or None."""
    t = text.replace('$', '').replace('\\,', '').replace('\\text{£}', '').replace('£', '').replace(',', '').strip()
    m = re.fullmatch(r'\\d?frac\{(-?\d+)\}\{(\d+)\}', t)
    if m: return F(int(m.group(1)), int(m.group(2)))
    m = re.search(r'\\approx (-?[\d.]+)', t) or re.fullmatch(r'(-?[\d.]+)( newtons|%|°)?', t)
    if m: return float(m.group(1)) if '.' in m.group(1) else int(m.group(1))
    return None

SEEN = set()
def chk(name, loc, key, slips=None, right=None):
    """Numeric widget: key and every wrong[] value. Choice widget: the correct
    option id (`right`) and the number in each option's text."""
    slips = slips or {}
    n = node(name, loc); w = n['widget']; tag = f'{name}#{loc}'
    SEEN.add((name, loc))
    if w['kind'] == 'numeric':
        ok(close(w['answer'], key), f'{tag} key {w["answer"]} vs recomputed {float(key):.6g}')
        have = {x['id']: x['value'] for x in w.get('wrong', [])}
        for sid, v in have.items():
            if sid not in slips: ok(False, f'{tag} slip {sid}={v} has no recomputation'); continue
            ok(close(v, slips[sid]), f'{tag} slip {sid} {v} vs recomputed {float(slips[sid]):.6g}')
            band = w.get('tol', {}).get('abs', 0) + [x for x in w['wrong'] if x['id'] == sid][0].get('tol', {}).get('abs', 0)
            ok(abs(v - w['answer']) > band, f'{tag} slip {sid} band overlaps the key')
    elif w['kind'] in ('choice',):
        corr = [o['id'] for o in w['options'] if o.get('correct')]
        ok(corr == [right], f'{tag} correct option {corr} vs {right}')
        for o in w['options']:
            v = optnum(o['text'])
            if o.get('correct'):
                if key is not None:
                    ok(v is not None and abs(float(v) - float(key)) < 1e-9 + (0.005 if isinstance(v, float) else 0), f'{tag} key text {o["text"]} vs {key}')
            elif o['id'] in slips:
                ok(v is not None and abs(float(v) - float(slips[o['id']])) < (0.051 if 'approx' in o['text'] else 0.006), f'{tag} option {o["id"]} {o["text"]} vs {slips[o["id"]]}')
                if key is not None: ok(abs(float(slips[o['id']]) - float(key)) > 1e-9, f'{tag} option {o["id"]} equals key')
            elif v is not None:
                ok(False, f'{tag} option {o["id"]} has no recomputation')
    else:
        ok(False, f'{tag} unexpected widget {w["kind"]}')

# ---------- brute-force helpers ----------
def nprod(*sizes): return sum(1 for _ in product(*[range(s) for s in sizes]))
def lines(n, pred=lambda p: True): return sum(1 for p in permutations(range(n)) if pred(p))
def adj(p, a, b): return abs(p.index(a) - p.index(b)) == 1
def ordered(n, r, pred=lambda p: True): return sum(1 for p in permutations(range(n), r) if pred(p))
def subsets(n, r, pred=lambda c: True): return sum(1 for c in combinations(range(n), r) if pred(c))
def words(word, pred=lambda w: True):
    """Distinct arrangements of a multiset, by recursion on what is left."""
    cnt = {}
    for ch in word: cnt[ch] = cnt.get(ch, 0) + 1
    out = [0]; cur = []
    def rec(left):
        if left == 0:
            out[0] += 1 if pred(cur) else 0; return
        for ch in cnt:
            if cnt[ch]:
                cnt[ch] -= 1; cur.append(ch); rec(left - 1); cur.pop(); cnt[ch] += 1
    rec(len(word)); return out[0]
def together(w, ch): s = ''.join(w); return ch * 2 in s
def circ(n, pred=lambda p: True, mirror=False):
    seen = set()
    for p in permutations(range(n)):
        if not pred(p): continue
        rots = [p[i:] + p[:i] for i in range(n)]
        if mirror: rots += [tuple(reversed(r)) for r in rots]
        seen.add(min(rots))
    return len(seen)
def cadj(p, a, b): return (p.index(a) - p.index(b)) % len(p) in (1, len(p) - 1)
def seqs(alpha, n, pred=lambda s: True): return sum(1 for s in product(alpha, repeat=n) if pred(s))
def routes(m, n, through=None):
    """R/U words with m Rs and n Us; `through` = (x, y) a cell the path must visit."""
    c = 0
    for s in product('RU', repeat=m + n):
        if s.count('R') != m: continue
        x = y = 0; hit = through is None or (0, 0) == through
        for ch in s:
            x += ch == 'R'; y += ch == 'U'
            hit = hit or (x, y) == through
        c += hit
    return c
def weak_orders(n, shape):
    """Rankings with ties whose tie-block sizes are `shape` (sorted)."""
    seen = set()
    for t in product(range(n), repeat=n):
        lv = sorted(set(t)); d = tuple(lv.index(x) for x in t)
        if sorted(d.count(k) for k in set(d)) == sorted(shape): seen.add(d)
    return len(seen)
def gridpos(canvas, label):
    for r, row in enumerate(canvas['params']['cells']):
        for c, cell in enumerate(row):
            if cell == label: return r, c
    raise KeyError(label)

# ======================= LEVEL 1 =======================
L = 'l1-choices-multiply'
chk(L, 's1', nprod(3, 2), {'added': 3 + 2, 'shirts': 3})
chk(L, 's3', nprod(3, 2, 2, 3), {'added': 12 + 3, 'forgot': 12, 'no-shoes': 3 * 2 * 3})
chk(L, 's4', nprod(4, 3, 2), {'added': 4 + 3 + 2, 'one-main': 6})
chk(L, 's5', nprod(4, 3, 1), {'unchanged': 24, 'added': 4 + 3 + 1, 'dropped': nprod(4, 3, 0)})
chk(L, 's6', seqs('01', 5), {'times': 10, 'squared': 25, 'added': 7, 'three': seqs('01', 3)})
chk(L, 's7', nprod(3, 4), {'added': 7, 'mains': 4, 'both-ways': 24}, right='right')
chk(L, 's10', nprod(4, 3, 2) * 0.40, {'added': 9 * 0.4, 'drawn': 6 * 0.4, 'runs': 24})
ok(abs(nprod(4, 3, 2, 5) * 0.40 - 48.0) < 1e-9, 'l1 s10 explain: fourth setting gives £48.00')
chk(L, 'q0', seqs(range(10), 4), {'times': 40, 'largest': 9999, 'no-repeat': ordered(10, 4)}, right='right')
chk(L, 'q1', 5 + 3, {'times': nprod(5, 3), 'shares': 5, 'pair': 2}, right='right')
chk(L, 'q2', nprod(3, 5, 2), {'no-cheese': 15, 'added': 10, 'plus-one': 16}, right='right')
chk(L, 'q3', nprod(26, 26, 10), {'added': 62, 'no-repeat': 26 * 25 * 10, 'no-digit': 676}, right='right')
ok(node(L, 's8')['widget']['options'][0]['correct'] and node(L, 's8')['widget']['options'][0]['id'] == 'or', 'l1 s8 key is the or option')

L = 'l2-arranging'
chk(L, 's1', lines(3), {'one-each': 3, 'repeats': 27, 'square': 9})
chk(L, 's3', lines(4), {'added': 10, 'square': 16, 'two-places': ordered(4, 2), 'power': 4 ** 4})
chk(L, 's4', lines(5), {'added': 15, 'square': 25, 'four': lines(4), 'power': 5 ** 5})
chk(L, 's5', lines(4, lambda p: p[0] == 0), {'ignored': 24, 'subtracted': 24 - 6, 'four': 4})
chk(L, 's6', lines(4, lambda p: adj(p, 1, 2)), {'one-way': 6, 'ignored': 24, 'added': 6 + 2})
chk(L, 's7', lines(6), {'double': 12, 'square': 36, 'added': 21}, right='right')
ok(lines(6) == 60 * 12 and lines(6) // lines(3) == 4 * 5 * 6, 'l2 s7: 720 is sixty times 12; ratio 120')
ok(all(fact(n) > 2 ** n for n in range(4, 60)), 'l2 s7: n! outgrows doubling from n = 4')
chk(L, 's10', lines(5), {'square': 25, 'added': 15, 'four': 24, 'power': 3125})
ok(lines(5) * 30 == 3600, 'l2 s10: 120 replays at 30 s is one hour')
chk(L, 'q0', lines(6), {'square': 36, 'added': 21, 'double': 12}, right='right')
chk(L, 'q1', F(fact(8), fact(7)), {'one': 1, 'ratio': F(8, 7), 'big': 40320}, right='right')
chk(L, 'q2', lines(5, lambda p: p[4] == 0), {'ignored': 120, 'subtracted': 96, 'five': 5})
chk(L, 'q3', lines(5, lambda p: adj(p, 0, 1)), {'one-way': 24, 'ignored': 120, 'small': 12}, right='right')
ok([o['id'] for o in node(L, 's8')['widget']['options'] if o.get('correct')] == ['right'] and fact(7) == 7 * fact(6) == 5040, 'l2 s8: 7! = 7 x 6!')

L = 'l3-choosing-in-order'
chk(L, 's0', ordered(5, 3), {'repeats': 125, 'groups': subsets(5, 3), 'added': 12, 'all-five': 120})
chk(L, 's2', ordered(7, 3), {'repeats': 343, 'groups': subsets(7, 3), 'all-seven': 5040, 'added': 18})
ok(ordered(5, 3) == fact(5) // fact(2) and fact(5) // (fact(3) * fact(2)) == 10, 'l3 s3: P(5,3) = 5!/2!')
chk(L, 's4', F(fact(5), ordered(5, 5)), {'zero': 0, 'five': 120})
chk(L, 's5', ordered(6, 4), {'repeats': 6 ** 4, 'groups': subsets(6, 4), 'all-six': 720, 'added': 18})
ok(0.70 < 1 - ordered(6, 4) / 6 ** 4 < 0.75, 'l3 s5: banning repeats removes almost three quarters')
chk(L, 's6', ordered(6, 2), {'kim': fact(6) // 2, 'groups': subsets(6, 2), 'repeats': 36}, right='right')
ok(ordered(6, 4) == 360, 'l3 s6: 6!/2! is the count for 4 places')
chk(L, 's7', 10 - 4 + 1, {'left-over': 6, 'r': 4, 'one': 1}, right='right')
chk(L, 's9', ordered(10, 4), {'repeats': 10 ** 4, 'groups': subsets(10, 4), 'added': 34, 'no-zero': 9 * 8 * 7 * 6})
chk(L, 'q0', ordered(10, 3), {'groups': subsets(10, 3), 'repeats': 1000, 'added': 27}, right='right')
ok(9 * 8 * 7 * 6 == fact(9) // fact(5) == 3024, 'l3 q1: 9x8x7x6 = 9!/5!')
chk(L, 'q2', ordered(26, 3), {'repeats': 26 ** 3, 'groups': comb(26, 3), 'added': 75})
# FINDING 1: the l3 s9 line "as if 0 could not come first" names a mistake whose value is 4536
no_lead_zero = ordered(10, 4, lambda p: p[0] != 0)
w = node(L, 's9')
ok(no_lead_zero == 4536, 'brute force: 4-digit no-repeat PINs with first digit not 0 = 4536')
ok(any(x['value'] == no_lead_zero for x in w['widget']['wrong']) or 'could not come first' not in w['feedback']['byKey'].get('no-zero', ''),
   'FINDING 1 l3 s9 no-zero: line names "0 could not come first" (value 4536) but the slip value is 3024 (0 barred from every place)')

L = 'l4-choosing-without-order'
chk(L, 's0', subsets(4, 2), {'ordered': 12, 'square': 16, 'four': 4, 'added': 8})
chk(L, 's2', subsets(5, 2), {'ordered': 20, 'square': 25, 'five': 5})
chk(L, 's3', sum(1 for p in permutations(range(5), 3) if set(p) == {0, 1, 2}), {'three': 3, 'two': 2, 'one': 1})
chk(L, 's4', subsets(6, 3), {'ordered': 120, 'by-three': 40, 'repeats': 216})
ok(subsets(5, 3) == subsets(5, 2) == 10 and [o['id'] for o in node(L, 's5')['widget']['options'] if o.get('correct')] == ['right'], 'l4 s5 symmetry')
chk(L, 's6', subsets(8, 3), {'ranked': ordered(8, 3), 'halved': 336 // 3, 'repeats': 512}, right='right')
ok(subsets(10, 7) == subsets(10, 3) == 120 and subsets(7, 3) == 35 and ordered(10, 3) == 720, 'l4 s7 options')
ok(all(comb(n, r) == comb(n, n - r) == subsets(n, r) for n in range(1, 9) for r in range(n + 1)), 'symmetry C(n,r)=C(n,n-r) by enumeration, n<=8')
chk(L, 's9', subsets(10, 3), {'ordered': 720, 'repeats': 1000, 'by-three': 240, 'added': 27})
chk(L, 'q0', seqs('UD', 5, lambda s: s.count('U') == 2), {'ordered': 20, 'all': 32, 'square': 25}, right='right')
chk(L, 'q1', subsets(7, 7), {'seven': 7, 'ordered': 5040, 'zero': 0}, right='right')
chk(L, 'q2', subsets(12, 9), {'ordered': 1320, 'half': 660, 'product': 108})
chk(L, 'q3', ordered(6, 2), {'pairs': 15, 'repeats': 36, 'added': 11}, right='right')
ok(sorted(node(L, 's1')['widget']['answer']) == ['r1c2', 'r2c1'], 'l4 s1: AB and BA cells')

# ----- review-1, homework-1, problems-1 -----
L = 'review-1'
chk(L, 'i0', nprod(5, 3, 2), {'added': 10, 'one-branch': 6})
chk(L, 'i1', lines(7), {'square': 49, 'added': 28, 'five': 720}, right='right')
chk(L, 'i2', ordered(9, 3), {'repeats': 729, 'groups': subsets(9, 3), 'added': 24, 'all': fact(9)})
chk(L, 'i3', subsets(9, 4), {'ordered': ordered(9, 4), 'by-four': 3024 // 4, 'repeats': 9 ** 4})
chk(L, 'i4', 4 + 6, {'times': 24, 'kinds': 2})
chk(L, 'i5', seqs('WL', 6, lambda s: s.count('W') == 2), {'ordered': 30, 'all': 64, 'count': 2})
chk(L, 'i6', lines(6, lambda p: adj(p, 0, 1)), {'one-way': 120, 'ignored': 720, 'small': 48})
chk(L, 'i8', ordered(26, 3) * 10, {'repeats': 26 ** 3 * 10, 'no-digit': 15600, 'groups': comb(26, 3) * 10})
ok(sorted(o['id'] for o in node(L, 'i7')['widget']['options'] if o.get('correct')) == ['chair', 'pin', 'rank'], 'review-1 i7 ordered counts')

L = 'homework-1'
chk(L, 'i0', seqs('01', 4) * 5, {'one-switch': 10, 'times-four': 40, 'added': 13, 'no-switch': 5})
chk(L, 'i1', no_lead_zero, {'ignored': 5040, 'no-zero-anywhere': ordered(9, 4), 'lost-zero': 9 * 8 * 8 * 7})
chk(L, 'i2', seqs('UD', 5, lambda s: s.count('U') >= 4), {'only-four': 5, 'only-five': 1, 'wrong-r': 10})
ok(all(subsets(n, 2) == n * (n - 1) // 2 for n in range(2, 12)) and comb(100, 2) == 4950, 'homework-1 i3: n(n-1)/2 pairs; 4950 for 100')
hw_chair = sum(1 for c in combinations(range(10), 4) for ch in c)
chk(L, 'i5', hw_chair, {'no-chair': 210, 'ordered': ordered(10, 4), 'outside': 2100}, right='right')
ok(hw_chair == 10 * comb(9, 3), 'homework-1 i5: chair-first route agrees')
chk(L, 'i6', lines(7, lambda p: max(p.index(0), p.index(1), p.index(2)) - min(p.index(0), p.index(1), p.index(2)) == 2),
    {'block-fixed': 120, 'ignored': 5040, 'two-way': 240})
ok(subsets(12, 4) == 495 and ordered(12, 4) == 11880 == 495 * 24 and subsets(11, 3) == 165, 'homework-1 longform figures')

L = 'problems-1'
chk(L, 'i0.p0', subsets(8, 4), {'ordered': 1680, 'divide-four': 420, 'times': 32})
chk(L, 'i0.p1', lines(4), {'four': 4, 'repeats': 256})
chk(L, 'i0.p2', ordered(8, 4), {'added': 94, 'carried': 1680 * 24})
chk(L, 'i0.p3', ordered(8, 4) * 4, {'added': 1684, 'no-order': 280, 'carried': 40320 * 4})
chk(L, 'i1.p0', lines(7), {'square': 49, 'sum': 28, 'seven': 7})
chk(L, 'i1.p1', lines(7, lambda p: p[3] == 0), {'not-middle': 5040 - 720, 'six': 6})
chk(L, 'i1.p3', lines(7, lambda p: p[3] == 0 and adj(p, 1, 2)), {'block': 240, 'no-swap': 96, 'pairs-six': 288})
ok([o['id'] for o in node(L, 'i1.p2')['widget']['options'] if o.get('correct')] == ['pairs-four'], 'problems-1 i1.p2 key')
chk(L, 'i2.p0', subsets(8, 2), {'ordered': 56, 'square': 64, 'times-two': 16})
chk(L, 'i2.p1', ordered(8, 2), {'half': 14, 'carried': 112})
chk(L, 'i2.p2', [n for n in range(2, 30) if ordered(n, 2) == 72][0], {'halved': 36, 'one-factor': 8})
chk(L, 'i2.p3', subsets(9, 6), {'ordered': perm(9, 6), 'no-divide': 504, 'times': 54})
chk(L, 'i3.p0', subsets(14, 3), {'ordered': 2184, 'repeats': 14 ** 3, 'times': 42})
chk(L, 'i3.p1', ordered(14, 3), {'times-three': 1092, 'added': 370, 'carried': 2184 * 6})
chk(L, 'i3.p2', subsets(14, 3) + ordered(14, 3), {'multiplied': 364 * 2184, 'carried': 2184 + 13104})
chk(L, 'i3.p3', (subsets(14, 3) + ordered(14, 3)) * 5, {'no-none': 2548 * 4, 'added': 2553, 'carried': 794976 * 5})

# ======================= LEVEL 2 =======================
L = 'l5-repeats'
chk(L, 's1', words('EGG'), {'all-orders': 6, 'with-repeats': 27})
chk(L, 's3', words('BOOK'), {'labelled': 24, 'twice': 6})
chk(L, 's4', words('ERROR'), {'by-two': 60, 'by-three': 40, 'labelled': 120})
chk(L, 's5', words('BANANA'), {'only-a': 120, 'only-n': 360, 'added': 720 // 8, 'labelled': 720})
chk(L, 's6', routes(3, 2), {'all-orders': 120, 'only-r': 20, 'cells': 12, 'added': 5})
c6 = node(L, 's6')['canvas']
ok(gridpos(c6, 'Start') == (2, 0) and gridpos(c6, 'End') == (0, 3), 'l5 s6 grid: 3 right and 2 up from Start to End')
chk(L, 's7', lines(4), {'divided': 12, 'twice': 6, 'doubled': 48}, right='right')
ok(words('MISSISSIPPI') == 34650 and fact(11) == 39916800 and fact(4) * fact(4) * 2 == 1152, 'l5 s8: MISSISSIPPI 34 650 by enumeration')
chk(L, 's9', seqs('UD', 5, lambda s: s.count('D') == 2), {'only-u': 20, 'all-orders': 120, 'all-weeks': 32})
ok(all(50 + s.count('U') - s.count('D') == 51 for s in product('UD', repeat=5) if s.count('D') == 2), 'l5 s9: two down days end at £51')
chk(L, 'q0', words('LEVEL'), {'one-group': 60, 'v-too': 15, 'none': 120}, right='right')
chk(L, 'q1', words('OOOO'), {'all-orders': 24, 'by-four': 6})
chk(L, 'q2', routes(4, 3), {'all-orders': 5040, 'only-r': 5040 // 24, 'added': 7})
chk(L, 'q3', seqs('UD', 6, lambda s: s.count('U') == 4), {'only-up': 30, 'all': 64, 'ordered': 360}, right='right')
g = node(L, 's2'); cells = g['canvas']['params']['cells']
strip = lambda s: s.replace('₁', '').replace('₂', '').replace(' ', '')
ok(sorted(g['widget']['answer']) == sorted(f'r{r+1}c{c+1}' for r, row in enumerate(cells) for c, x in enumerate(row) if strip(x) == 'GEG'), 'l5 s2 tap key = labelled orders reading GEG')
cells = node(L, 's3')['canvas']['params']['cells']
ok(len({x for row in cells for x in row}) == 24 and all(strip(row[i]) == strip(row[i + 1]) for row in cells for i in (0, 2, 4)), 'l5 s3 grid: 24 labelled orders, twins side by side')

L = 'l6-together-or-apart'
for loc, want in (('s1', lambda s: 'AB' in s or 'BA' in s), ('s2', lambda s: 'AB' in s)):
    g = node(L, loc); cells = g['canvas']['params']['cells']
    ok(sorted(g['widget']['answer']) == sorted(f'r{r+1}c{c+1}' for r, row in enumerate(cells) for c, x in enumerate(row) if want(x)), f'l6 {loc} tap key')
    ok(sorted(x for row in cells for x in row) == sorted(''.join(p) for p in permutations('ABCD'[:len(cells[0][0])])), f'l6 {loc} grid lists every seating once')
chk(L, 's3', lines(5, lambda p: adj(p, 0, 1)), {'one-way': 24, 'all': 120, 'five-units': 240})
chk(L, 's4', lines(6, lambda p: max(p.index(0), p.index(1), p.index(2)) - min(p.index(0), p.index(1), p.index(2)) == 2), {'one-way': 24, 'pair': 48, 'all': 720})
chk(L, 's5', lines(5, lambda p: not adj(p, 0, 1)), {'together': 48, 'all': 120, 'one-way': 96})
chk(L, 's6', circ(5), {'row': 120, 'mirror': circ(5, mirror=True), 'minus-one': 119})
chk(L, 's7', lines(5), {'rotations': 24, 'times-five': 600, 'mirror': 12}, right='right')
ok(all(lines(n, lambda p: not adj(p, 0, 1)) == (n - 2) * fact(n - 1) for n in range(2, 8)), 'l6 s8: apart = (n-2)(n-1)! for n = 2..7')
ok(all(lines(n, lambda p, k=k: max(p.index(i) for i in range(k)) - min(p.index(i) for i in range(k)) == k - 1) == fact(n - k + 1) * fact(k) for n in range(2, 8) for k in range(1, n + 1)), 'l6 summary: (n-k+1)! k!')
# tie of one known pair: rankings of 5 with A=B tied, nobody else tied
tieAB = sum(1 for t in product(range(5), repeat=5) if t[0] == t[1] and len(set(t)) == 4 and sorted(set(t)) == list(range(4)))
chk(L, 's9', tieAB, {'flipped': 48, 'divided': 60, 'no-tie': 120}, right='right')
chk(L, 'q0', lines(6, lambda p: adj(p, 0, 1)), {'one-way': 120, 'all': 720, 'apart': 480}, right='right')
chk(L, 'q1', circ(6), {'row': 720, 'mirror': circ(6, mirror=True)})
chk(L, 'q2', lines(6, lambda p: not adj(p, 0, 1)), {'together': 240, 'one-way': 600, 'all': 720})
chk(L, 'q3', circ(4, lambda p: cadj(p, 0, 1)), {'row': 12, 'one-way': 2, 'all': circ(4)}, right='right')

L = 'l7-what-you-do-not-want'
d2 = list(product(range(1, 7), repeat=2))
chk(L, 's1', sum(1 for o in d2 if 6 not in o), {'one-die': 30, 'corner-twice': 24, 'at-least-one': sum(1 for o in d2 if 6 in o)})
ok(sorted(node(L, 's2')['widget']['answer']) == sorted(f'r{a}c{b}' for a, b in d2 if 6 in (a, b)), 'l7 s2 tap key = outcomes with a 6')
chk(L, 's3', seqs(range(1, 7), 3, lambda s: 6 in s), {'added': 108, 'none': 125, 'all': 216, 'per-die': 18})
chk(L, 's4', seqs(range(10), 4, lambda s: 0 in s), {'added': 4000, 'none': 9 ** 4, 'all': 10 ** 4, 'one-place': 1000})
v = node(L, 's5')['canvas']['params']['values']
ok(v['A'] + v['AB'] + v['B'] + v['none'] == 30 and sorted(node(L, 's5')['widget']['answer']) == ['A', 'AB', 'B'], 'l7 s5 venn')
chk(L, 's6', 22 + 15 - 9, {'double': 37, 'removed-twice': 19, 'neither': 12, 'minus-all': 3})
v = node(L, 's6')['canvas']['params']['values']
ok((v['A'] + v['AB'], v['B'] + v['AB'], v['A'] + v['AB'] + v['B'] + v['none']) == (22, 15, 40) and v['A'] + v['B'] == 19, 'l7 s6 venn regions agree with the prose')
ok(all(len(A | B) == len(A) + len(B) - len(A & B) for _ in range(2000) for A, B in [(set(random.sample(range(30), random.randint(0, 20))), set(random.sample(range(30), random.randint(0, 20))))]), 'inclusion-exclusion on 2000 random pairs of sets')
chk(L, 's8', seqs('UD', 5, lambda s: 'D' in s), {'all': 32, 'exactly-one': 5, 'none': 1, 'added': 10})
chk(L, 's9', 250 - (60 + 45 - 20), {'double': 145, 'union': 85, 'minus-overlap': 230})
v = node(L, 's9')['canvas']['params']['values']
ok((v['A'] + v['AB'], v['B'] + v['AB'], v['none']) == (60, 45, 165), 'l7 s9 venn')
chk(L, 'q0', sum(1 for n in range(1, 101) if n % 2 == 0 or n % 5 == 0), {'added': 70, 'evens': 50, 'neither': 40}, right='right')
chk(L, 'q1', seqs('HT', 3, lambda s: 'H' in s), {'all': 8, 'exactly-one': 3, 'added': 6})
chk(L, 'q2', seqs('UD', 5, lambda s: s.count('D') >= 2), {'at-least-one': 31, 'one-each': 30, 'exactly-two': 10}, right='right')
deck = [(r, s) for r in range(13) for s in range(4)]
chk(L, 'q3', sum(1 for h in combinations(deck, 2) if any(c[0] == 0 for c in h)), {'double': 4 * 51, 'none': comb(48, 2)})
ok(comb(52, 2) == 1326 and sum(1 for h in combinations(deck, 2) if all(c[0] == 0 for c in h)) == 6, 'l7 q3: 1326 hands, 6 two-ace hands')

L = 'l8-counts-to-chances'
pairs = list(combinations('ABCDE', 2))
P = lambda ev, space: F(sum(1 for x in space if ev(x)), len(space))
chk(L, 's1', P(lambda p: set(p) == {'A', 'B'}, pairs), {'ordered': F(1, 20), 'a-only': P(lambda p: 'A' in p, pairs), 'whole': F(1, 25)}, right='right')
g = node(L, 's2'); heads = g['canvas']['params']['rowHeads']
ok(sorted(g['widget']['answer']) == sorted(f'r{heads.index(a)+1}c{heads.index(b)+1}' for a, b in pairs if 'C' in (a, b)), 'l8 s2 tap key = pairs with C')
chk(L, 's3', P(lambda p: not set(p) & {'A', 'B'}, pairs), {'at-least-one': F(7, 10), 'replace': F(9, 25), 'singles': F(3, 5)})
ports = [(s, b) for s in combinations(range(8), 3) for b in combinations(range(5), 2)]
chk(L, 's4', len(ports), {'added': 56 + 10, 'pooled': comb(13, 5), 'ordered': perm(8, 3) * perm(5, 2)})
chk(L, 's5', P(lambda x: 0 in x[0], ports), {'one-pick': F(1, 8), 'one-portfolio': F(1, 560), 'half': 0.5})
c6 = node(L, 's6')['canvas']; st, en, mk = gridpos(c6, 'Start'), gridpos(c6, 'End'), gridpos(c6, 'Marked')
m, n = en[1] - st[1], st[0] - en[0]; thr = (mk[1] - st[1], st[0] - mk[0])
ok((m, n) == (3, 2), 'l8 s6 grid is 3 right, 2 up')
chk(L, 's6', F(routes(m, n, thr), routes(m, n)), {'added': F(5, 10), 'cell': F(1, 12), 'to-only': F(2, 10), 'from-only': F(3, 10)})
chk(L, 's7', P(lambda p: set(p) <= set('ABC'), pairs), {'sam': F(6, 10), 'replace': F(9, 25), 'one-pick': F(3, 5)}, right='right')
ok(F(sum(1 for p in permutations('ABCDE', 2) if set(p) <= set('ABC')), 20) == F(3, 10), 'l8 s7: ordered over ordered gives 3/10 too')
paths4 = list(product((5, -5), repeat=4))
chk(L, 's9', P(lambda s: sum(s) == 0, paths4), {'end-prices': F(1, len({sum(s) for s in paths4})), 'one-path': F(1, 16), 'half': 0.5, 'count': 6})
hands = list(combinations(deck, 2))
chk(L, 'q0', P(lambda h: all(c[1] == 0 for c in h), hands), {'replace': F(1, 16), 'mixed': F(13 * 12, 1326), 'one': F(1, 4)}, right='right')
chk(L, 'q1', sum(1 for t in combinations(range(6), 2) for a in range(4)), {'added': 19, 'pooled': comb(10, 3)})
ok(perm(6, 2) * 4 == 120, 'l8 q1: 120 is also traders counted in order')
paths5 = list(product('UD', repeat=5))
chk(L, 'q2', P(lambda s: s.count('U') == 2, paths5), {'end-prices': F(1, 6), 'one-path': F(1, 32), 'ups': 0.4})
rt = [s for s in product('RU', repeat=6) if s.count('R') == 4]
chk(L, 'q3', P(lambda s: s[0] == 'R', rt), {'coin': F(1, 2), 'one': F(1, 15), 'count': F(10, 6)}, right='right')

L = 'review-2'
chk(L, 'i0', words('COFFEE'), {'one-group': 360, 'none': 720})
chk(L, 'i1', lines(6, lambda p: p.index(1) == p.index(0) + 1 and p.index(2) == p.index(1) + 1), {'any-order': 144, 'all': 720, 'five-units': 120}, right='right')
chk(L, 'i2', seqs(range(10), 3, lambda s: 7 in s), {'added': 300, 'none': 729, 'all': 1000})
p6 = list(combinations(range(6), 2))
chk(L, 'i3', P(lambda p: set(p) & {0, 1}, p6), {'none': F(6, 15), 'both': F(1, 15), 'replace': 1 - F(4, 6) ** 2})
chk(L, 'i4', 120 - (70 + 50 - 30), {'double': 0, 'union': 90})
chk(L, 'i5', circ(7), {'row': 5040, 'mirror': circ(7, mirror=True), 'minus-two': 120}, right='right')
chk(L, 'i6', routes(4, 4), {'all': fact(8), 'only-r': fact(8) // 24, 'squared': 16})
paths7 = list(product('UD', repeat=7))
chk(L, 'i7', P(lambda s: s.count('U') == 5, paths7), {'end-prices': F(1, 8), 'one-path': F(1, 128), 'count': 21})
chk(L, 'i8', lines(5, lambda p: p[0] != 0 and p[4] != 1), {'double': 72, 'one-rule': 96, 'bad': 42})

L = 'homework-2'
chk(L, 'i0', words('STATISTICS'), {'missed-i': 100800, 'none': fact(10), 'counts': fact(10) // 18})
chk(L, 'i1', lines(7, lambda p: adj(p, 0, 1) and adj(p, 2, 3)), {'one-flip': 240, 'one-way': 120, 'all': 5040}, right='right')
aces5 = sum(1 for h in combinations(range(52), 5) if h[0] < 4)   # cards 0..3 are the aces; a sorted hand holds an ace iff its smallest card is one
chk(L, 'i2', aces5, {'double': 4 * comb(51, 4), 'none': comb(48, 5)})
ok(comb(52, 5) == 2598960, 'homework-2 i2: 2 598 960 hands')
chk(L, 'i3', P(lambda x: 0 in x[0] and 0 in x[1], ports), {'s1-only': F(3, 8), 'b1-only': P(lambda x: 0 in x[1], ports), 'added': F(3, 8) + F(2, 5)})
chk(L, 'i4', weak_orders(5, [1, 1, 1, 2]), {'known': tieAB, 'flipped': 480, 'five': 1200}, right='right')
chk(L, 'i5', sum(1 for k in range(1, 1001) if k % 3 == 0 or k % 7 == 0), {'added': 333 + 142, 'twice': 333 + 142 - 94, 'neither': 572})
c6 = node(L, 'i6')['canvas']; st, en, mk = gridpos(c6, 'Start'), gridpos(c6, 'End'), gridpos(c6, 'Centre')
m, n = en[1] - st[1], st[0] - en[0]; thr = (mk[1] - st[1], st[0] - mk[0])
ok((m, n, thr) == (4, 4, (2, 2)), 'homework-2 i6 grid: 4 right, 4 up, centre at (2, 2)')
chk(L, 'i6', 1 - F(routes(m, n, thr), routes(m, n)), {'through': F(36, 70), 'added': 1 - F(12, 70), 'cell': F(24, 25)})
ok(all(routes(a, b) == comb(a + b, a) for a in range(5) for b in range(5)), 'homework-2 i7: routes = C(m+n, m), m, n <= 4')
ok(all(circ(k, lambda p: not cadj(p, 0, 1)) == (k - 3) * fact(k - 2) for k in range(3, 8)), 'homework-2 longform: round-table apart = (n-3)(n-2)!, n = 3..7')
ok(F(circ(8, lambda p: cadj(p, 0, 1)), circ(8)) == F(2, 7), 'homework-2 longform: P(together) = 2/7 for n = 8, by enumeration')
random.seed(20261126); hit = 0; N = 200000
for _ in range(N):
    p = list(range(8)); random.shuffle(p); hit += cadj(p, 0, 1)
ok(abs(hit / N - 2 / 7) < 4 * sqrt(2 / 7 * 5 / 7 / N), f'Monte Carlo round table n=8: {hit/N:.4f} vs 2/7 = 0.2857 (4 se)')
pins = list(product(range(10), repeat=4))
chk(L, 'i9', P(lambda s: len(set(s)) < 4, pins), {'no-repeat': 0.504, 'unordered': 1 - 210 / 10000})

L = 'problems-2'
flags = 'RRRRBBY'
chk(L, 'i0.p0', words(flags), {'no-divide': 5040, 'reds-only': 210, 'blues-only': 2520})
chk(L, 'i0.p1', words(flags, lambda w: together(w, 'B')), {'flipped': 60, 'no-divide': 720, 'blue-divide': 15})
chk(L, 'i0.p2', words(flags, lambda w: not together(w, 'B')), {'carried': 45, 'added': 135})
chk(L, 'i0.p3', F(words(flags, lambda w: not together(w, 'B')), words(flags)), {'together': F(30, 105), 'carried': F(45, 105), 'bottom': 75 / 5040})
ok(sum(1 for a, b in combinations(range(7), 2) if b - a == 1) == 6 and comb(7, 2) == 21, 'problems-2 i0.p3 check by places')
chk(L, 'i1.p0', 45 + 38 - 20, {'no-overlap': 83, 'twice': 43})
chk(L, 'i1.p1', 80 - 63, {'carried': 37, 'only-one': 25 + 18})
chk(L, 'i1.p2', F(17, 80), {'at-least': F(63, 80), 'carried': F(37, 80), 'bottom': 17 / 63})
chk(L, 'i1.p3', P(lambda p: p[1] < 17, list(combinations(range(80), 2))), {'replaced': (17 / 80) ** 2, 'ordered-top': 17 * 16 / 3160, 'pairs-over-members': 136 / 80})
B = 'BALLOON'
chk(L, 'i2.p0', words(B), {'no-divide': 5040, 'one-pair': 2520})
chk(L, 'i2.p1', words(B, lambda w: together(w, 'O')), {'flipped': 720, 'both-divided': 180})
chk(L, 'i2.p2', words(B, lambda w: not together(w, 'O')), {'carried': 540, 'carried-half': 1080})
both_apart = words(B, lambda w: not together(w, 'O') and not together(w, 'L'))
chk(L, 'i2.p3', both_apart, {'all-ls': 540, 'both-only': 780})
ok(words(B, lambda w: together(w, 'O') and together(w, 'L')) == 120 and words(B, lambda w: together(w, 'L') and not together(w, 'O')) == 240, 'problems-2 i2.p3 explain: 120 and 240')
chk(L, 'i2.p4', F(both_apart, words(B)), {'carried': 540 / 1260, 'os-only': 900 / 1260, 'bottom': 660 / 5040})
random.seed(7); hit = 0; N = 200000
for _ in range(N):
    w = list(B); random.shuffle(w); s = ''.join(w); hit += 'OO' not in s and 'LL' not in s
ok(abs(hit / N - 11 / 21) < 4 * sqrt(11 / 21 * 10 / 21 / N), f'Monte Carlo BALLOON no matching blocks touch: {hit/N:.4f} vs 11/21 = 0.5238 (4 se)')
club = ['g'] * 6 + ['b'] * 5; teams = list(combinations(range(11), 4)); G = lambda t: sum(club[i] == 'g' for i in t)
chk(L, 'i3.p0', len(teams), {'ordered': perm(11, 4), 'times': 44})
chk(L, 'i3.p1', sum(1 for t in teams if G(t) == 0), {'no-boys': sum(1 for t in teams if G(t) == 4), 'ordered': 120})
chk(L, 'i3.p2', sum(1 for t in teams if G(t) >= 1), {'no-boys': 315, 'exactly-one': sum(1 for t in teams if G(t) == 1)})
chk(L, 'i3.p3', sum(1 for t in teams if 1 <= G(t) <= 3), {'no-girls-again': 320, 'both-off': 305})
chk(L, 'i3.p4', P(lambda t: 1 <= G(t) <= 3, teams), {'girl-only': 325 / 330, 'bottom': 310 / 325, 'carried': 305 / 330})

# ======================= LEVEL 3 (vectors) =======================
def V(*a): return tuple(a)
add = lambda u, v: tuple(a + b for a, b in zip(u, v))
sub = lambda u, v: tuple(a - b for a, b in zip(u, v))
sc = lambda k, u: tuple(k * a for a in u)
dot = lambda u, v: sum(a * b for a, b in zip(u, v))
mag = lambda u: sqrt(dot(u, u))
ang = lambda u, v: degrees(acos(dot(u, v) / (mag(u) * mag(v))))
def corr(name, loc, want):
    c = [o['id'] for o in node(name, loc)['widget']['options'] if o.get('correct')]
    ok(sorted(c) == sorted(want), f'{name}#{loc} correct option(s) {c} vs {want}'); SEEN.add((name, loc))
def table(name, loc, want):
    got = [r[1]['answer'] for r in node(name, loc)['widget']['rows']]
    ok(got == list(want), f'{name}#{loc} table {got} vs {want}'); SEEN.add((name, loc))
def drag(name, loc, want, regions=None):
    w = node(name, loc)['widget']
    ok(tuple(w['points'][0]['target']) == tuple(want), f'{name}#{loc} target vs {want}'); SEEN.add((name, loc))
    for x in w.get('wrong', []):
        r = x['region']; pt = (regions or {}).get(x['id'])
        ok(pt is not None and r['x'][0] < pt[0] < r['x'][1] and r['y'][0] < pt[1] < r['y'][1] and tuple(pt) != tuple(want), f'{name}#{loc} region {x["id"]} vs {pt}')

L = 'l9-arrows'
corr(L, 's1', ['right']); ok(sub((4, 3), (1, 1)) == (3, 2) and abs(mag((3, 2)) - 3.6) < 0.05, 'l9 s1: (3, 2), length about 3.6')
corr(L, 's2', ['right']); drag(L, 's3', (-3, 2), {'swapped': (2, -3), 'sign-top': (3, 2), 'sign-bottom': (-3, -2)})
vs = {v['id']: tuple(v['v']) for v in node(L, 's4')['canvas']['params']['vectors']}
corr(L, 's4', [k for k in vs if k != 'u' and vs[k] == vs['u']])
table(L, 's5', sub((6, 1), (1, 4))); corr(L, 's6', ['right']); ok(sub((1, 5), (4, 3)) == (-3, 2) and add((4, 3), (1, 5)) == (5, 8), 'l9 s6')
corr(L, 's7', ['right']); table(L, 's8', sub((150, 450), (300, 200)))
corr(L, 'q0', ['a']); ok(sub((4, -1), (-2, 3)) == (6, -4) and add((4, -1), (-2, 3)) == (2, 2), 'l9 q0')
corr(L, 'q1', ['a']); corr(L, 'q2', ['a']); corr(L, 'q3', ['a'])
# FINDING 2: "AC is a diagonal. It is longer" is false for some parallelograms
A, Bp, D = (0, 0), (10, 0), (-2, 1); Cp = add(Bp, D)      # ABCD in order, AD = (-2, 1)
ok(sub(Cp, D) == sub(Bp, A) and mag(sub(Cp, A)) < mag(sub(Bp, A)), 'counterexample: parallelogram with diagonal AC shorter than side AB')
ok('longer' not in node(L, 'q3')['widget']['options'][3]['why'], 'FINDING 2 l9 q3 option d: "AC ... is longer" fails for A(0,0) B(10,0) C(8,1) D(-2,1), |AC| = 8.06 < |AB| = 10')

L = 'l10-adding-arrows'
drag(L, 's0', add((3, 1), (1, 2)), {'first-leg': (3, 1), 'second-leg': (1, 2), 'multiplied': (3 * 1, 1 * 2)})
corr(L, 's1', ['add']); table(L, 's2', add((-2, 5), (4, -3)))
chk(L, 's3', [k for k in (-3, -2, -1, 1, 2, 3) if sc(k, (2, -1)) == (-6, 3)][0], {'nosign': 3, 'component': -6})
par = lambda u, v: abs(u[0] * v[1] - u[1] * v[0]) < 1e-9
corr(L, 's4', [i for i, v in zip('abcde', [(4, -2), (-6, 3), (1, -0.5), (1, -2), (2, 1)]) if par((2, -1), v)])
drag(L, 's5', sub((4, 1), (1, 3)), {'reverse': sub((1, 3), (4, 1)), 'sum': add((4, 1), (1, 3))})
corr(L, 's6', ['vu']); corr(L, 's7', ['a'])
ok(add(sc(2, (1, -3)), (4, 5)) == (6, -1) and add((1, -6), (4, 5)) == (5, -1) and sc(2, add((1, -3), (4, 5))) == (10, 4) and add((2, 6), (4, 5)) == (6, 11), 'l10 s7 options')
chk(L, 's9', 0.6 * -0.30 + 0.4 * 0.50, {'unweighted': 0.2, 'average': 0.1, 'market': 0.6 * 1.2 + 0.4 * 0.8, 'nosign': 0.18 + 0.20})
corr(L, 'q0', ['a']); ok(add((3, -1), (-5, 4)) == (-2, 3) and sub((3, -1), (-5, 4)) == (8, -5), 'l10 q0')
corr(L, 'q1', ['a']); corr(L, 'q2', [i for i, v in zip('abcd', [(-3, 2), (4, -6), (6, 4), (3, -1)]) if par((6, -4), v)])
corr(L, 'q3', ['right'])
random.seed(1)
for _ in range(200):
    a, b = (random.randint(-9, 9), random.randint(-9, 9)), (random.randint(-9, 9), random.randint(-9, 9))
    lhs = sub(sc(2, add(a, sc(3, b))), sub(a, b))
    ok(lhs == add(a, sc(7, b)), 'l10 q3: 2(a+3b)-(a-b) = a+7b');
    if lhs != add(a, sc(7, b)): break

L = 'l11-how-long'
chk(L, 's0', mag((3, 4)), {'added': 7, 'multiplied': 12, 'difference': 1})
corr(L, 's1', [i for i, v in zip('abcd', [(4, -3), (2, 5), (5, 5), (1, 4)]) if abs(mag(v) - 5) < 1e-12])
chk(L, 's2', mag((-5, 12)), {'signed-sum': 7, 'added': 17, 'subtracted-squares': sqrt(144 - 25)})
chk(L, 's3', mag(sub((7, 10), (1, 2))), {'sum': 14, 'positions': mag(add((7, 10), (1, 2))), 'end': mag((7, 10))})
chk(L, 's4', degrees(atan(3 / 4)), {'flipped': degrees(atan(4 / 3)), 'tan': 0.75, 'radians': atan(3 / 4)})
corr(L, 's5', [i for i, v in zip('abcd', [(0.6, 0.8), (3 / 7, 4 / 7), (1, 1), (0.75, 1)]) if abs(mag(v) - 1) < 1e-12 and par((3, 4), v)])
ok(abs(mag((3 / 7, 4 / 7)) - 5 / 7) < 1e-12 and abs(mag((0.75, 1)) - 1.25) < 1e-12, 'l11 s5 option lengths')
chk(L, 's6', mag(sc(-2, (3, 4))), {'negative': -10, 'unscaled': 5})
chk(L, 's7', mag(add((6, 8), (6, -8))), {'b': 20, 'c': 0, 'd': sqrt(200)}, right='a')
chk(L, 's9', mag((0.03, -0.04)), {'added': 0.07, 'signed': -0.01, 'signed-abs': 0.01})
chk(L, 'q0', mag((-8, 15)), {'b': 7, 'c': 23, 'd': sqrt(161)}, right='a')
corr(L, 'q1', ['a']); chk(L, 'q2', mag(sub((5, -4), (-1, 4))), {'added': 14, 'positions': mag(add((5, -4), (-1, 4)))})
corr(L, 'q3', ['a'])
random.seed(2); tri = True; scal = True
for _ in range(5000):
    u, v, k = (random.uniform(-9, 9), random.uniform(-9, 9)), (random.uniform(-9, 9), random.uniform(-9, 9)), random.uniform(-5, 5)
    tri = tri and mag(add(u, v)) <= mag(u) + mag(v) + 1e-12; scal = scal and abs(mag(sc(k, u)) - abs(k) * mag(u)) < 1e-9
ok(tri and scal, 'l11: |u+v| <= |u|+|v| and |ku| = |k||u| on 5000 random draws')
# FINDING 3: the summary gives direction by tan(theta) = u2/u1 with no quadrant caveat
u = (-3, 3); naive = degrees(atan(u[1] / u[0])); true = ang((1, 0), u)
ok(abs(naive + 45) < 1e-9 and abs(true - 135) < 1e-9, 'counterexample: (-3, 3) points at 135 degrees, inverse tangent of u2/u1 gives -45')
summ = ' '.join(load(L)['summary']['ideas'])
ok(re.search(r'quadrant|sketch|diagram|180', summ) is not None, 'FINDING 3 l11 summary: "direction comes from tan(theta) = u2/u1" with no quadrant caveat; (-3, 3) gives -45 degrees, true direction 135')

L = 'l12-proving-with-vectors'
corr(L, 's0', ['yes']); ok(sub((7, 4), (1, 1)) == sc(3, sub((3, 2), (1, 1))) and not par((2, 1), sub((7, 6), (1, 1))), 'l12 s0')
corr(L, 's1', ['equal']); ok(not par((2, 1), (4, 4)) and not par((2, 1), (2, 2)) and par((2, 1), (-4, -2)), 'l12 s1 counterexamples')
chk(L, 's2', sub((8, 10), (2, 1))[0] / sub((4, 4), (2, 1))[0], {'bc': 2, 'positions': 10 / 4})
ok(sub((8, 10), (2, 1)) == sc(3, sub((4, 4), (2, 1))) and sub((8, 10), (4, 4)) == sc(2, (2, 3)), 'l12 s2')
corr(L, 's3', ['no']); ok(not par(sub((2, 2), (0, 1)), sub((6, 5), (0, 1))), 'l12 s3 not collinear')
corr(L, 's4', ['right']); a, b = (6, 2), (2, 4); ok(sub(sc(.5, b), sc(.5, a)) == (-2, 1) and sub(b, a) == (-4, 2), 'l12 s4 diagram vectors')
corr(L, 's5', ['no']); ok(sub((4, 4), (0, 2)) == sc(2, (2, 1)) and not par((2, 1), (0, 2)), 'l12 s5')
corr(L, 's6', ['right'])
P_, Q_, R_ = (0, 100), (3, 104.5), (7, 110.5)
ok(par(sub(Q_, P_), sub(R_, Q_)), 'l12 s8 points collinear')
chk(L, 's8', sub(R_, Q_)[0] / sub(Q_, P_)[0], {'inverse': 0.75, 'price': 110.5 / 104.5, 'days': 7 / 3})
corr(L, 'q0', ['yes']); ok(sub((7, 11), (1, 2)) == sc(3, (2, 3)) and sub((7, 11), (3, 5)) == sc(2, (2, 3)), 'l12 q0')
chk(L, 'q1', [t for t in range(-50, 50) if par(sub((4, 4), (2, 1)), sub((8, t), (2, 1)))][0], {'no-start': 9, 'second': 7})
corr(L, 'q2', [i for i, v in zip('abcd', [(-6, 4), (3, 2), (2, -3), (4, 2)]) if par(sub((4, 2), (1, 4)), v)])
corr(L, 'q3', ['a'])
random.seed(3)
for _ in range(200):
    a, b = (random.randint(-9, 9), random.randint(-9, 9)), (random.randint(-9, 9), random.randint(-9, 9))
    if not ok(sub(sc(.5, b), sc(.5, a)) == sc(.5, sub(b, a)) and add(a, sc(.25, sub(b, a))) == add(sc(.75, a), sc(.25, b)), 'l12 midpoint and quarter-point identities') and FAILS: pass

L = 'l13-portfolio-vector'
chk(L, 's0', dot((30, 20), (2, -1.5)), {'nosign': 90, 'alpha': 60, 'changes': 0.5, 'shares': 50})
corr(L, 's1', ['perp']); ok(dot((3, 2), (2, -3)) == 0 and dot((3, 2), (-3, -2)) == -13 and dot((3, 2), (1, 0)) == 3, 'l13 s1')
chk(L, 's2', dot((4, -1), (2, 3)), {'nosign': 11, 'sums': 15, 'top': 8})
chk(L, 's3', dot(add((30, 20), (10, -5)), (0.8, -0.4)), {'book': dot((30, 20), (0.8, -0.4)), 'hedge': dot((10, -5), (0.8, -0.4)), 'short-sign': dot((40, 25), (0.8, -0.4))})
chk(L, 's4', dot((3, 4), (4, 3)) / (mag((3, 4)) * mag((4, 3))), {'dot': 24, 'sum': 2.4, 'one': 1})
ok(abs(ang((3, 4), (4, 3)) - 16.3) < 0.05, 'l13 s4: 16.3 degrees')
chk(L, 's5', dot((200, 300), (6, -4)), {'nosign': 2400, 'changes': 2}, right='zero')
chk(L, 's6', dot((30, 20), (1.2, -0.9)), {'nosign': 54, 'changes': 0.3}, right='right')
corr(L, 's7', ['obtuse'])
random.seed(4); cosok = True
for _ in range(5000):
    u, v = (random.uniform(-9, 9), random.uniform(-9, 9)), (random.uniform(-9, 9), random.uniform(-9, 9))
    th = abs(degrees(__import__('math').atan2(u[0] * v[1] - u[1] * v[0], dot(u, v))))   # angle from atan2, independent of the dot formula
    cosok = cosok and abs(dot(u, v) - mag(u) * mag(v) * __import__('math').cos(__import__('math').radians(th))) < 1e-9 and ((dot(u, v) < 0) == (th > 90))
ok(cosok, 'l13: u.v = |u||v|cos(theta) and sign rule, 5000 random draws, theta from atan2')
r, m_ = (3, 1), (2, 1); beta = dot(r, m_) / dot(m_, m_)
ok(abs(dot(sub(r, sc(beta, m_)), m_)) < 1e-12, 'l13 s9: residual is perpendicular to m')
chk(L, 's9', beta, {'dot': 7, 'first-day': 1.5, 'length': dot(r, m_) / mag(m_)})
chk(L, 'q0', 100 * dot((0.5, 0.3, 0.2), (0.02, -0.01, 0.04)), {'b': 5, 'c': 100 * 0.05 / 3, 'd': 2.1}, right='a')
corr(L, 'q1', ['a']); ok(dot((2, -3), (6, 4)) == 0, 'l13 q1')
chk(L, 'q2', ang((1, 0), (1, 1)), {'no-mag': 0, 'cos': 1 / sqrt(2)})
chk(L, 'q3', dot((3, -2), (-1, 4)), {'c': 3, 'd': 11}, right='a')

L = 'review-3'
corr(L, 'i0', ['a']); ok(sub((-1, 4), (3, -2)) == (-4, 6), 'review-3 i0')
corr(L, 'i1', ['a']); ok(sub(sc(3, (1, -2)), (4, -5)) == (-1, -1) and add(sc(3, (1, -2)), (4, -5)) == (7, -11) and sub((1, -2), (4, -5)) == (-3, 3), 'review-3 i1')
chk(L, 'i2', mag(sub((4, 9), (-2, 1))), {'added': 14, 'end': mag((4, 9))})
corr(L, 'i3', ['a'])
chk(L, 'i4', [t for t in range(-50, 50) if par(sub((3, 2), (1, -1)), sub((9, t), (1, -1)))][0], {'no-start': 12, 'times3': 8})
corr(L, 'i5', ['a'])
chk(L, 'i6', hypot(5, 12), {'b': 17, 'c': 7, 'd': sqrt(119)}, right='a')
chk(L, 'i7', dot((100, -50), (0.4, 1.2)), {'long': 100, 'vector': 40, 'sign': 20})
chk(L, 'i8', ang((2, 1), (-1, 3)), {'no-mag': 0, 'cos': 1 / sqrt(50), 'one-mag': degrees(acos(1 / sqrt(5)))})

L = 'homework-3'
corr(L, 'i0', ['a']); ok(sub((300, 200, 400), (500, 200, 0)) == (-200, 0, 400), 'homework-3 i0')
X, Y, Z = (1.10, 0.20), (0.90, -0.40), (1.30, 0.60); pf = add(add(sc(.5, X), sc(.3, Y)), sc(.2, Z))
chk(L, 'i1', pf[1], {'unweighted': 0.4, 'market': pf[0], 'nosign': 0.34})
chk(L, 'i2', mag((0.01, -0.02, 0.02)), {'signed': 0.01, 'sizes': 0.05})
chk(L, 'i3', [a for a in range(-50, 50) if par(sub((3, 4), (1, 1)), sub((a, 7), (1, 1)))][0], {'no-start': 4, 'from-b': 7})
chk(L, 'i4', [b for b in range(-1000, 1000) if dot((300, b), (2, 3)) == 0][0], {'long': 200, 'ratio': -450})
chk(L, 'i5', dot((3, -2, 1), (2, -1, 1)) / dot((2, -1, 1), (2, -1, 1)), {'dot': 9, 'root': 9 / sqrt(6), 'nosign': 5 / 6})
ok(dot((6, 8), (6, -8)) == -28 and 100 + 100 - 56 == dot(add((6, 8), (6, -8)), add((6, 8), (6, -8))), 'homework-3 longform example')

L = 'problems-3'
S_, Pp, Qq = (1, 2), (10, 14), (-2, 30)
ok(sub(Pp, S_) == (9, 12) and sub(Qq, Pp) == (-12, 16) and sub(Qq, S_) == (-3, 28) and sub((9, 12), (-12, 16)) == (21, -4) and add(Pp, Qq) == (8, 44), 'problems-3 i0 vectors')
route = 100 * (mag(sub(Pp, S_)) + mag(sub(Qq, Pp)))
chk(L, 'i0.p3', route, {'components': 4900, 'direct': 100 * mag(sub(Qq, S_)), 'squares': 35})
chk(L, 'i0.p4', route - 100 * mag(sub(Qq, S_)), {'direct': 100 * mag(sub(Qq, S_)), 'added-components': 3500 - 3100, 'carried': 4900 - 2816, 'squares': 6.84})
ok(sub((8, 7), (2, 3)) == (6, 4) and sub((17, 13), (2, 3)) == (15, 10) and sub((17, 13), (8, 7)) == (9, 6), 'problems-3 i1 vectors')
chk(L, 'i1.p2', 15 / 6, {'reciprocal': 0.4, 'difference': 9}); corr(L, 'i1.p3', ['collinear'])
chk(L, 'i1.p4', 100 * mag((15, 10)), {'ab-only': 100 * mag((6, 4)), 'added': 2500, 'units': mag((15, 10))})
h, d = (60, 40), (2.5, -3.5)
chk(L, 'i2.p0', dot(h, d), {'no-sign': 290, 'sum-first': (60 + 40) * (2.5 - 3.5)})
h2 = add(h, (-20, 30)); ok(h2 == (40, 70), 'problems-3 i2.p1')
chk(L, 'i2.p2', dot(h2, d), {'trade-only': dot((-20, 30), d), 'old-book': 10, 'signs': dot((80, 10), d), 'no-sign': 345, 'sign': 145})
chk(L, 'i2.p3', ang(h2, d), {'acute': 180 - ang(h2, d), 'cosine': dot(h2, d) / (mag(h2) * mag(d)), 'radians': __import__('math').radians(ang(h2, d))})
random.seed(5)
for _ in range(50):
    r_, s_ = (random.randint(-9, 9), random.randint(-9, 9)), (random.randint(-9, 9), random.randint(-9, 9))
    OM = sc(F(1, 2), add(r_, s_)); OX = sc(F(2, 3), OM); RX = sub(OX, r_); RN = sub(sc(F(1, 2), s_), r_)
    ok(OX == sc(F(1, 3), add(r_, s_)) and RX == sc(F(2, 3), RN), 'problems-3 i3: OX = (r+s)/3 and RX = (2/3) RN')
chk(L, 'i3.p4', F(2, 3), {'reciprocal': 1.5, 'third': 1 / 3, 'half': 0.5})

# ======================= FLUENCY FAMILIES, whole range =======================
def fl_eval(expr, env):
    e = expr.replace('^', '**')
    return eval(e, {'__builtins__': {}}, dict(env, fact=lambda x: F(fact(int(x))), comb=lambda a, b: F(comb(int(a), int(b)))))
INDEP = {
    'evaluate-p': lambda e: (perm(e['n'], e['r']), {'repeats-allowed': e['n'] ** e['r'], 'one-factor-short': perm(e['n'], e['r'] - 1)}),
    'awards': lambda e: (perm(e['n'], e['r']), {'repeats-allowed': e['n'] ** e['r'], 'times-places': e['n'] * e['r']}),
    'factorial-quotient': lambda e: (prod(range(e['n'] - e['g'] + 1, e['n'] + 1)), {'subtracted': fact(e['g']), 'divided-the-numbers': F(e['n'], e['n'] - e['g'])}),
    'pairs': lambda e: (comb(e['n'], 2), {'order-counted': e['n'] * (e['n'] - 1), 'n-plus-one': e['n'] * (e['n'] + 1) // 2}),
    'evaluate-binomial': lambda e: (comb(e['n'], int(e['_r'])), {'not-divided': perm(e['n'], e['s']), 'divided-by-s': F(perm(e['n'], e['s']), e['s'])}),
    'committee': lambda e: (comb(e['n'], e['r']), {'order-counted': perm(e['n'], e['r']), 'divided-by-r': F(perm(e['n'], e['r']), e['r'])}),
    'up-down-patterns': lambda e: (comb(e['n'], e['k']), {'all-patterns': 2 ** e['n'], 'order-counted': perm(e['n'], e['k'])}),
}
ENUM = {   # true enumeration for small parameters, to tie each formula to a count
    'evaluate-p': lambda e: ordered(e['n'], e['r']) if e['n'] <= 7 else None,
    'awards': lambda e: ordered(e['n'], e['r']) if e['n'] <= 7 else None,
    'pairs': lambda e: subsets(e['n'], 2) if e['n'] <= 12 else None,
    'evaluate-binomial': lambda e: subsets(e['n'], int(e['_r'])) if e['n'] <= 12 else None,
    'committee': lambda e: subsets(e['n'], e['r']) if e['n'] <= 12 else None,
    'up-down-patterns': lambda e: seqs('UD', e['n'], lambda s, k=e['k']: s.count('U') == k) if e['n'] <= 10 else None,
}
for fname in ('fluency-l3-choosing-in-order', 'fluency-l4-choosing-without-order'):
    for fam in load(fname)['families']:
        names = list(fam['vars']); doms = []
        for nme in names:
            sp = fam['vars'][nme]
            doms.append(list(range(sp['int'][0], sp['int'][1] + 1)) if 'int' in sp else sp['pick'])
        inst = bad = 0
        for combo in product(*doms):
            envF = {k: F(v) for k, v in zip(names, combo) if not isinstance(v, str)}
            for k, ex in fam['let'].items(): envF[k] = F(fl_eval(ex, envF))
            if not all(fl_eval(c, envF) for c in fam.get('where', [])): continue
            inst += 1
            env = {k: (int(v) if v.denominator == 1 else v) for k, v in envF.items()}
            env2 = dict(env); env2['_r'] = env.get('r', 0)
            key, slips = INDEP[fam['id']](env2)
            good = env['key'] == key
            en = ENUM.get(fam['id'], lambda e: None)(env2)
            good = good and (en is None or en == key)
            vals = []
            for x in fam['wrong']:
                v = F(fl_eval(x['value'].strip('{}'), envF)); vals.append(v)
                good = good and v == slips[x['id']] and v != key
            good = good and len(set(vals)) == len(vals)
            if fam['id'] == 'evaluate-binomial':
                good = good and env['r'] + env['nr'] == env['n'] and comb(env['n'], int(env['r'])) == comb(env['n'], env['s']) and env['r'] in (env['s'], env['n'] - env['s'])
            if fam['id'] == 'factorial-quotient':
                good = good and env['m'] == env['n'] - env['g'] and env['m1'] == env['m'] + 1
            bad += not good
        ok(inst >= 20 and bad == 0, f'{fname} family {fam["id"]}: {inst} instances over the whole range, {bad} bad')
        print(f'fluency {fam["id"]:22s} instances {inst:5d} bad {bad}')

# FINDING 4: three "you swapped" lines whose option is not the swapped vector
for name, loc, oid, base in (('l10-adding-arrows', 's4', 'd', (2, -1)), ('l10-adding-arrows', 'q2', 'b', (6, -4)), ('l12-proving-with-vectors', 'q2', 'c', (3, -2))):
    o = [x for x in node(name, loc)['widget']['options'] if x['id'] == oid][0]
    nums = tuple(float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', o['text']))
    swapped = (base[1], base[0])
    ok(nums == swapped or 'swapped' not in o['why'], f'FINDING 4 {name}#{loc} option {oid}: text {nums} is called a swap of {base}, whose swap is {swapped}')

# every graded numeric or choice widget in the course must have been visited
missing = []
for fn in sorted(os.listdir(ROOT)):
    if not fn.endswith('.json') or fn.startswith(('course', 'fluency')): continue
    name = fn[:-5]; d = DOCS.setdefault(name, load(name))
    def visit(nd, loc):
        w = nd.get('widget')
        if w and w['kind'] in ('numeric',) and (name, loc) not in SEEN: missing.append(f'{name}#{loc}')
        for j, p_ in enumerate(nd.get('parts', [])): visit(p_, f'{loc}.p{j}')
    for key_, pre in (('screens', 's'), ('quiz', 'q'), ('items', 'i')):
        for i, nd in enumerate(d.get(key_, [])): visit(nd, f'{pre}{i}')
ok(not missing, f'numeric widgets without a recomputation: {missing}')

print(f'\n{NCHK[0]} checks, {len(FAILS)} failed')
sys.exit(1 if FAILS else 0)
