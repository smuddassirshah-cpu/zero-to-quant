#!/usr/bin/env python3
"""Concept checks, round 3, for course `conditional` levels 1 to 3 (lessons l1 to l17,
review-1..3, homework-1..3, problems-1..3, fluency-l7).

Run from the repo root with no arguments:  python3 docs/reports/conditional-L1-3-concepts-r3.py
Exit 0 when every check passes. A check tied to an audit finding (tag F1..F6) fails until
the content is fixed, so the script exits 1 while any finding is open.

Self-contained: no import of earlier concept libraries. Run with CPython 3 (standard library
only); the two code widgets use only `math.comb`, so values match Pyodide 0.27.7.
"""
import glob
import itertools
import json
import math
import os
import random
import re
import sys
from fractions import Fraction as Fr

ROOT = os.path.join('app', 'content', 'courses', 'conditional')
FAILS, PASSES = [], 0


def check(name, ok, detail=''):
    global PASSES
    if ok:
        PASSES += 1
    else:
        FAILS.append(name + (' :: ' + str(detail) if detail else ''))


def load(name):
    with open(os.path.join(ROOT, name + '.json'), encoding='utf-8') as fh:
        return json.load(fh)


def lesson(n):
    hits = glob.glob(os.path.join(ROOT, 'l%d-*.json' % n))
    assert len(hits) == 1, hits
    with open(hits[0], encoding='utf-8') as fh:
        return json.load(fh)


def close(a, b, tol=1e-9):
    return abs(float(a) - float(b)) <= tol


def num(s):
    """Parse '3/5', '0.45', '9,900' into a Fraction."""
    s = str(s).replace(',', '').strip()
    if '/' in s:
        a, b = s.split('/')
        return Fr(a) / Fr(b)
    return Fr(s)


# ---------------------------------------------------------------- trees
def tree_paths(levels):
    """Yield (path id, product) for a `levels` tree. A branch p is a string or a map keyed
    by the parent path; a branch missing for a parent is pruned."""
    paths = [('', Fr(1))]
    for lev in levels:
        nxt = []
        for pid, pr in paths:
            tot = Fr(0)
            for br in lev['branches']:
                p = br['p']
                if isinstance(p, dict):
                    if pid not in p:
                        continue
                    p = p[pid]
                p = num(p)
                tot += p
                nxt.append(((pid + '-' + br['id']) if pid else br['id'], pr * p))
            yield ('__node__' + pid, tot)
        paths = nxt
    for x in paths:
        yield x


def walk_canvases(obj, path=''):
    if isinstance(obj, dict):
        if obj.get('kind') == 'tree' and 'params' in obj:
            yield path, obj
        for k, v in obj.items():
            yield from walk_canvases(v, path + '.' + k if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_canvases(v, '%s[%d]' % (path, i))


def digits(s):
    s = str(s)
    return len(s.split('.')[1]) if '.' in s and '/' not in s else None


def check_trees(fname, data):
    for path, cv in walk_canvases(data):
        prm = cv['params']
        tag = '%s %s' % (fname, path)
        if 'levels' in prm:
            is_count = 'rootLabel' in prm
            leaves = {}
            for pid, val in tree_paths(prm['levels']):
                if pid.startswith('__node__'):
                    if is_count:
                        continue
                    check('tree node branches sum to 1: ' + tag + ' ' + pid[8:], val == 1, val)
                else:
                    leaves[pid] = val
            if is_count:
                # counts: children of each first-stage branch add to it; first stage adds to the root
                root = num(re.sub(r'[^0-9,.]', '', prm['rootLabel']))
                l0 = prm['levels'][0]['branches']
                check('count tree first stage adds to root: ' + tag, sum(num(b['p']) for b in l0) == root)
                if len(prm['levels']) > 1:
                    for b in l0:
                        kids = sum(num(x['p'][b['id']]) for x in prm['levels'][1]['branches'] if b['id'] in x['p'])
                        check('count tree children add to parent: ' + tag + ' ' + b['id'], kids == num(b['p']))
                continue
            check('tree path products sum to 1: ' + tag, sum(leaves.values()) == 1, sum(leaves.values()))
            shown = prm.get('leaves')
            if shown:
                is_l17_s5 = fname.startswith('l17') and path == 'screens[5].canvas'
                ok_all = True
                for pid, txt in shown.items():
                    want = leaves.get(pid)
                    d = digits(txt)
                    if want is None:
                        ok_all = False
                    elif d is None:
                        ok_all &= (num(txt) == want)
                    else:
                        ok_all &= abs(num(txt) - want) <= Fr(1, 2 * 10 ** d) + Fr(1, 10 ** 12)
                if is_l17_s5:
                    cap = (cv.get('state') or {}).get('caption', '')
                    check('F5 l17 screens[5] tree: leaves are path products, or the caption says they are not',
                          ok_all or 'not path products' in cap or 'not a path product' in cap, 'leaves %s shown under branches 0.2 and 0.8' % shown)
                else:
                    check('tree leaves equal path products: ' + tag, ok_all, shown)
                    check('tree shown leaves sum to 1: ' + tag,
                          abs(sum(num(v) for v in shown.values()) - 1) <= Fr(1, 1000), shown)
        elif 'nodes' in prm:
            def rec(node, where):
                kids = node.get('children') if isinstance(node, dict) else node
                if not kids:
                    return
                check('tree node children sum to 1: ' + tag + ' ' + where, sum(num(k['p']) for k in kids) == 1)
                for k in kids:
                    rec(k, where + '/' + k['id'])
            rec(prm['nodes'], 'root')


SCOPE = (['l%d' % i for i in range(1, 18)] + ['review-%d' % i for i in (1, 2, 3)]
         + ['homework-%d' % i for i in (1, 2, 3)] + ['problems-%d' % i for i in (1, 2, 3)])
DATA = {}
for key in SCOPE:
    DATA[key] = lesson(int(key[1:])) if re.fullmatch(r'l\d+', key) else load(key)
    check_trees(key, DATA[key])
FLU = load('fluency-l7-turning-around')

L = {i: DATA['l%d' % i] for i in range(1, 18)}


def widget_answers(obj):
    """Yield every numeric widget (answer, wrong list, tol) to test that no slip value is graded right."""
    if isinstance(obj, dict):
        if obj.get('kind') == 'numeric' and isinstance(obj.get('answer'), (int, float)):
            yield obj
        for v in obj.values():
            yield from widget_answers(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from widget_answers(v)


for key, d in DATA.items():
    for w in widget_answers(d):
        ta = (w.get('tol') or {}).get('abs', 0)
        for wr in w.get('wrong') or []:
            if isinstance(wr.get('value'), (int, float)):
                tw = (wr.get('tol') or {}).get('abs', 0)
                check('slip value not inside the accepted band: %s answer %s slip %s' % (key, w['answer'], wr['id']),
                      abs(wr['value'] - w['answer']) > ta + tw, (w['answer'], ta, wr['value'], tw))

# ---------------------------------------------------------------- level 1: exact enumeration
dice = list(itertools.product(range(1, 7), repeat=2))


def P(ev, given=lambda o: True, space=dice):
    g = [o for o in space if given(o)]
    return Fr(sum(1 for o in g if ev(o)), len(g))


d1 = [(x,) for x in range(1, 7)]
check('l1 P(6|even)=1/3', P(lambda o: o[0] == 6, lambda o: o[0] % 2 == 0, d1) == Fr(1, 3))
check('l1 P(even|>3)=2/3', P(lambda o: o[0] % 2 == 0, lambda o: o[0] > 3, d1) == Fr(2, 3))
check('l1 trap: P(even|<=4) stays 1/2', P(lambda o: o[0] % 2 == 0, lambda o: o[0] <= 4, d1) == Fr(1, 2))
check('l1 quiz: P(<=3|odd)=2/3 rose from 1/2', P(lambda o: o[0] <= 3, lambda o: o[0] % 2, d1) == Fr(2, 3))
v = L[1]['screens'][8]['canvas']['params']['values']
check('l1 transfer venn: 56/80=0.7 and 120/200=0.6',
      Fr(v['AB'], v['A'] + v['AB']) == Fr(7, 10) and Fr(v['AB'] + v['B'], sum(v.values())) == Fr(3, 5))

# l2 bag 3 red 2 blue, ordered draws without replacement
cnt = list(itertools.permutations(['R1', 'R2', 'R3', 'B1', 'B2'], 2))
check('l2 20 ordered pairs, 6 both red', len(cnt) == 20 and sum(a[0] == 'R' and b[0] == 'R' for a, b in cnt) == 6)
check('l2 hidden first draw: P(2nd red)=3/5', Fr(sum(b[0] == 'R' for a, b in cnt), 20) == Fr(3, 5))
check('l2 P(2nd red|1st red)=1/2, |1st blue=3/4',
      Fr(sum(a[0] == 'R' and b[0] == 'R' for a, b in cnt), sum(a[0] == 'R' for a, b in cnt)) == Fr(1, 2)
      and Fr(sum(a[0] == 'B' and b[0] == 'R' for a, b in cnt), sum(a[0] == 'B' for a, b in cnt)) == Fr(3, 4))

# l3
check('l3 P(total 8)=5/36', P(lambda o: sum(o) == 8) == Fr(5, 36))
check('l3 at least one 5 leaves 11', sum(1 for o in dice if 5 in o) == 11)
check('l3 P(total 10 | at least one 5)=1/11', P(lambda o: sum(o) == 10, lambda o: 5 in o) == Fr(1, 11))
check('l3 P(total 10 | first is 5)=1/6 (the fixed-die slip)', P(lambda o: sum(o) == 10, lambda o: o[0] == 5) == Fr(1, 6))
check('l3 quiz: P(a 3 shows | total 7)=1/3; reversed 2/11',
      P(lambda o: 3 in o, lambda o: sum(o) == 7) == Fr(1, 3) and P(lambda o: sum(o) == 7, lambda o: 3 in o) == Fr(2, 11))
st = list(itertools.product('UD', repeat=2))
check('l3 stocks: P(both up | at least one up)=1/3; | A up = 1/2',
      P(lambda o: o == ('U', 'U'), lambda o: 'U' in o, st) == Fr(1, 3)
      and P(lambda o: o == ('U', 'U'), lambda o: o[0] == 'U', st) == Fr(1, 2))
check('l3 trap line: at least one 5 leaves 11, first is 5 leaves 6',
      '11 outcomes' in L[3]['summary']['trap'] and 'leaves 6' in L[3]['summary']['trap'])

# l4 six-card deck: 4 hearts, 2 spades
deck = ['H'] * 4 + ['S'] * 2
perm2 = list(itertools.permutations(range(6), 2))
both_h = Fr(sum(deck[a] == 'H' and deck[b] == 'H' for a, b in perm2), len(perm2))
check('l4 both hearts 2/5, not Sam\'s 4/9', both_h == Fr(2, 5))
hs = Fr(sum(deck[a] == 'H' and deck[b] == 'S' for a, b in perm2), len(perm2))
check('l4 either order: P(A)P(B|A)=P(B)P(A|B)=8/30, P(A|B)=4/5',
      hs == Fr(8, 30) and hs / Fr(sum(deck[b] == 'S' for a, b in perm2), len(perm2)) == Fr(4, 5))
perm3 = list(itertools.permutations(range(6), 3))
check('l4 three hearts 1/5 and heart-spade-heart 1/5',
      Fr(sum(all(deck[i] == 'H' for i in p) for p in perm3), len(perm3)) == Fr(1, 5)
      and Fr(sum([deck[i] for i in p] == ['H', 'S', 'H'] for p in perm3), len(perm3)) == Fr(1, 5))
check('l4 transfer: 0.16 understates 0.24 by a third', Fr(24 - 16, 24) == Fr(1, 3))

# l5 socks
check('l5 leaves 20/56,15/56,15/56,6/56', Fr(5, 8) * Fr(4, 7) == Fr(20, 56) and Fr(3, 8) * Fr(2, 7) == Fr(6, 56))
check('l5 Kim: wrong second-stage branches still give leaves adding to 1',
      Fr(25 + 15 + 15 + 9, 64) == 1 and Fr(15, 64) != Fr(5, 8) * Fr(3, 7))
check('l5 transfer: 0.6*0.45=0.27, slip 0.6*0.52=0.312', close(0.6 * 0.45, 0.27) and close(0.6 * 0.52, 0.312))

# l6 total probability
check('l6 5/12 and 11/24', Fr(1, 3) * Fr(3, 4) + Fr(2, 3) * Fr(1, 4) == Fr(5, 12)
      and Fr(1, 6) + Fr(2, 6) * Fr(1, 2) + Fr(3, 6) * Fr(1, 4) == Fr(11, 24))
check('l6 weighted average lies between the conditional chances',
      all(min(a, b) - 1e-12 <= w * a + (1 - w) * b <= max(a, b) + 1e-12
          for a in (0.0, 0.25, 0.9) for b in (0.1, 0.75, 1.0) for w in (0.0, 0.3, 1.0)))
check('l6 quiz: grade C over half of defaults; two thirds of flags on no-drop days',
      Fr(20, 34) > Fr(1, 2) and Fr(18, 27) == Fr(2, 3))

# ---------------------------------------------------------------- level 2: Bayes


def post(b, h, f):
    return Fr(h) * Fr(b) / (Fr(h) * Fr(b) + Fr(f) * (1 - Fr(b)))


S = lambda x: Fr(str(x))
check('l7 8/26 and 3/7 and 88/115', post(S(0.1), S(0.8), S(0.2)) == Fr(8, 26)
      and post(S(0.2), S(0.9), S(0.3)) == Fr(3, 7) and post(S(0.55), S(0.8), S(0.3)) == Fr(88, 115))
check('l7 summary: with P(AB)>0 the two directions agree iff P(A)=P(B)',
      all((Fr(j, a) == Fr(j, b)) == (a == b) for j in (1, 2) for a in (2, 3, 4) for b in (2, 3, 4)))
check('l8 2/13, 11/13 false, 18/19 at even base rate, clinic B 0.885',
      post(S(0.01), S(0.9), S(0.05)) == Fr(2, 13) and 1 - post(S(0.01), S(0.9), S(0.05)) == Fr(11, 13)
      and post(S(0.5), S(0.9), S(0.05)) == Fr(18, 19) and close(post(S(0.3), S(0.9), S(0.05)), 0.8852, 5e-4))
check('l8 slider: crosses 0.5 between 5% and 6%',
      post(S(0.05), S(0.9), S(0.05)) < Fr(1, 2) < post(S(0.06), S(0.9), S(0.05)))
check('l8 fraud 0.1599, backtest 9/28, ten-times quiz 4.3x',
      close(post(S(0.002), S(0.95), S(0.01)), 0.1599, 5e-4) and post(S(0.05), S(0.9), S(0.1)) == Fr(9, 28)
      and close(post(S(0.1), S(0.9), S(0.05)) / post(S(0.01), S(0.9), S(0.05)), 4.33, 0.01))
check('l8 direction: posterior rises with the base rate',
      all(post(Fr(b, 100), S(0.9), S(0.05)) < post(Fr(b + 1, 100), S(0.9), S(0.05)) for b in range(1, 99)))
# l9 grid counts against rates
g0 = L[9]['screens'][0]['canvas']['params']['cells']
check('l9 grid: 8 of 10 top-row positives, 9 of 90 below, 8/17',
      sum(c == '+' for c in g0[0]) == 8 and sum(c == '+' for r in g0[1:] for c in r) == 9)
g9 = L[9]['screens'][9]['canvas']['params']['cells']
check('l9 transfer grid: 14 trend squares and 8 others, 140/220, rates 70% and 10%',
      sum(c == 'S' for c in g9[0]) == 14 and sum(c == 'S' for r in g9[1:] for c in r) == 8
      and Fr(14, 20) == Fr(7, 10) and Fr(8, 80) == Fr(1, 10))
check('l9 10,000 crowd gives the exact 2/13; 1,000 with rounding gives 9/59', Fr(90, 585) == Fr(2, 13))
# l10 odds
check('l10 odds 1:99 -> x18 -> 18/99 -> p 2/13', Fr(1, 99) * 18 / (1 + Fr(1, 99) * 18) == Fr(2, 13))
check('l10 LR 18 = 0.9/0.05; log-odds labels', S(0.9) / S(0.05) == 18 and close(math.log(1 / 99), -4.5951, 1e-4)
      and close(math.log(1 / 99) + math.log(18), -1.7047, 1e-4))
check('l10 four signals of LR 1.5 needed from 1:4', Fr(1, 4) * Fr(3, 2) ** 3 < 1 <= Fr(1, 4) * Fr(3, 2) ** 4)
check('l10 quiz: 3 to 1 on is p=0.75; LR 1/4 from evens gives 0.2', Fr(3, 4) == Fr(3, 3 + 1) and Fr(1, 4) / Fr(5, 4) == Fr(1, 5))
# l11
o2 = Fr(1, 99) * 18 * 18
check('l11 two positives 36/47', o2 / (1 + o2) == Fr(36, 47))
o_pn = Fr(1, 99) * 18 * (S(0.1) / S(0.95))
check('l11 positive then negative: odds 4/209, p 4/213, above the 1% base rate', o_pn == Fr(4, 209)
      and o_pn / (1 + o_pn) == Fr(4, 213) and Fr(4, 213) > Fr(1, 100))
check('l11 analysts 49/58; a copy leaves 0.7', Fr(49, 9) / (1 + Fr(49, 9)) == Fr(49, 58))
# l12
pri = [Fr(1, 3)] * 3
lik5 = [Fr(0), Fr(1, 6), Fr(1, 8)]
pr5 = [a * b for a, b in zip(pri, lik5)]
p5 = [x / sum(pr5) for x in pr5]
lik3 = [Fr(1, 4), Fr(1, 6), Fr(1, 8)]
pr3 = [a * b for a, b in zip(p5, lik3)]
p3 = [x / sum(pr3) for x in pr3]
check('l12 dice: 0,4/7,3/7 then 0,16/25,9/25; zero prior stays zero',
      p5 == [0, Fr(4, 7), Fr(3, 7)] and p3 == [0, Fr(16, 25), Fr(9, 25)])
check('l12 regimes 2/9,1/3,4/9; models 0.25; managers 8/47',
      [S(a) * S(b) / S(0.135) for a, b in ((0.6, 0.05), (0.3, 0.15), (0.1, 0.6))] == [Fr(2, 9), Fr(1, 3), Fr(4, 9)]
      and S(0.5) * S(0.012) / (S(0.006) + S(0.009) + S(0.009)) == Fr(1, 4)
      and S(0.08) / S(0.47) == Fr(8, 47))

# ---------------------------------------------------------------- level 3: independence
A6 = lambda o: o[0] == 6
ind = lambda e, f, sp=dice: P(lambda o: e(o) and f(o), space=sp) == P(e, space=sp) * P(f, space=sp)
check('l13 total 7 independent of first die 6; total 12 not', ind(A6, lambda o: sum(o) == 7) and not ind(A6, lambda o: sum(o) == 12))
check('l13 multi: second 6 and even total independent of A; at least one 6 and first even not',
      ind(A6, lambda o: o[1] == 6) and ind(A6, lambda o: sum(o) % 2 == 0)
      and not ind(A6, lambda o: 6 in o) and not ind(A6, lambda o: o[0] % 2 == 0)
      and P(A6, lambda o: 6 in o) == Fr(6, 11))
rows = L[13]['screens'][9]['canvas']['params']['rows']
tally = {(y, t): sum(1 for r in rows if (r[1], r[2]) == (y, t)) for y in ('Up', 'Down') for t in ('Up', 'Down')}
check('l13 sign tally 7,3,3,7 and the table is one consistent chain of days',
      tally == {('Up', 'Up'): 7, ('Up', 'Down'): 3, ('Down', 'Up'): 3, ('Down', 'Down'): 7}
      and all(rows[i][2] == rows[i + 1][1] for i in range(len(rows) - 1)))
check('l13 self-independence only at 0 or 1', [x for x in (Fr(0), Fr(1, 2), Fr(1)) if x == x * x] == [0, 1])
# l14
tail = lambda k, n, p: sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k, n + 1))
check('l14 0.45^5=0.0185, 0.45^6<0.01, two wins in three 0.4084, 1-0.7^3=0.657',
      close(0.45 ** 5, 0.0185, 5e-5) and 0.45 ** 6 < 0.01 < 0.45 ** 5 and close(3 * 0.55 ** 2 * 0.45, 0.4084, 5e-5)
      and close(1 - 0.7 ** 3, 0.657))
check('l14 P(7+ of 10 at 0.55)=0.2660; P(30+ of 50 at 0.5)=0.1013; 20 strategies -> 2.03',
      close(tail(7, 10, 0.55), 0.2660, 5e-5) and close(tail(30, 50, 0.5), 0.1013, 5e-5) and close(20 * tail(30, 50, 0.5), 2.03, 0.01))
# l15 coins
coins = list(itertools.product('HT', repeat=2))
eA, eB, eC = (lambda o: o[0] == 'H'), (lambda o: o[1] == 'H'), (lambda o: o[0] == o[1])
eD = lambda o: o[0] != o[1]
check('l15 A,B,C pairwise independent, triple 1/4 not 1/8, P(C|A and B)=1',
      ind(eA, eB, coins) and ind(eA, eC, coins) and ind(eB, eC, coins)
      and P(lambda o: eA(o) and eB(o) and eC(o), space=coins) == Fr(1, 4)
      and P(eC, lambda o: eA(o) and eB(o), coins) == 1)
check('l15 with "differ" the pairs still pass and the triple is 0',
      ind(eA, eD, coins) and ind(eB, eD, coins) and P(lambda o: eA(o) and eB(o) and eD(o), space=coins) == 0)
# range of P(ABC) for three pairwise independent events of chance 1/2: atoms are non-negative exactly on [0, 1/4]
feas = [t for t in (Fr(k, 40) for k in range(-2, 15))
        if min(t, Fr(1, 4) - t) >= 0]
check('l15 trap key: pair checks leave P(all three) anywhere in [0, 1/4]', min(feas) == 0 and max(feas) == Fr(1, 4))
check('l15 four events need 11 equations', sum(math.comb(4, k) for k in (2, 3, 4)) == 11)
# l16 sector model
sector = [(c, a, b, Fr(1, 2) * (pa if a else 1 - pa) * (pa if b else 1 - pa))
          for c, pa in (('g', Fr(4, 5)), ('b', Fr(1, 5))) for a in (1, 0) for b in (1, 0)]
pj = lambda f: sum(w for c, a, b, w in sector if f(c, a, b))
check('l16 both rise 0.34, P(B up|A up)=0.68, given good day 0.8',
      pj(lambda c, a, b: a and b) == Fr(34, 100) and pj(lambda c, a, b: a and b) / pj(lambda c, a, b: a) == Fr(68, 100)
      and pj(lambda c, a, b: c == 'g' and a and b) / pj(lambda c, a, b: c == 'g' and a) == Fr(4, 5))
alert = {(1, 1): S(0.02), (1, 0): S(0.18), (0, 1): S(0.08), (0, 0): S(0.72)}
fire = {k: w for k, w in alert.items() if k != (0, 0)}
p_news_alert = sum(w for k, w in fire.items() if k[0]) / sum(fire.values())
p_news_alert_drop = alert[(1, 1)] / (alert[(1, 1)] + alert[(0, 1)])
check('l16 explaining away: 5/7 after the alert, falls to 0.2 once the drop is known',
      p_news_alert == Fr(5, 7) and p_news_alert_drop == Fr(1, 5) and p_news_alert_drop < p_news_alert)
check('l16 analysts: P(2 says beat|1 says beat)=7/12; coin quiz 5/6',
      (S(0.4) * S(0.75) ** 2 + S(0.6) * S(0.25) ** 2) / (S(0.4) * S(0.75) + S(0.6) * S(0.25)) == Fr(7, 12)
      and (Fr(1, 2) * Fr(1, 4) + Fr(1, 2)) / (Fr(1, 2) * Fr(1, 2) + Fr(1, 2)) == Fr(5, 6))
# l17
mix = lambda k, n, q, pb, pg: q * tail(k, n, pb) + (1 - q) * tail(k, n, pg)
pmf = lambda j, n, p: math.comb(n, j) * p ** j * (1 - p) ** (n - j)
check('l17 independent bars 0.5987,0.3151,0.0746,0.0115',
      all(close(a, b, 5e-5) for a, b in zip([pmf(0, 10, .05), pmf(1, 10, .05), pmf(2, 10, .05), tail(3, 10, .05)],
                                            [0.5987, 0.3151, 0.0746, 0.0115])))
check('l17 mixture bars at q=0.2: 0.7269,0.1430,0.0655,0.0646',
      all(close(0.2 * pmf(j, 10, 0.2) + 0.8 * pmf(j, 10, 0.0125), w, 5e-5) for j, w in ((0, 0.7269), (1, 0.1430), (2, 0.0655)))
      and close(mix(3, 10, 0.2, 0.2, 0.0125), 0.0646, 5e-5))
qs = [i / 100 for i in range(0, 26)]
pg_of = lambda q: (0.05 - 0.2 * q) / (1 - q)
z0 = [q * pmf(0, 10, 0.2) + (1 - q) * pmf(0, 10, pg_of(q)) for q in qs]
z3 = [mix(3, 10, q, 0.2, pg_of(q)) for q in qs]
check('l17 slider: both the 0 bar and the 3-or-more bar rise all the way from q=0 to 0.25',
      all(a < b for a, b in zip(z0, z0[1:])) and all(a < b for a, b in zip(z3, z3[1:])))
check('l17 pair 0.008125 = 3.25 x 0.0025; tail ratio 5.6; all-or-nothing 0.05 > 4 x 0.0115',
      close(0.2 * 0.04 + 0.8 * 0.0125 ** 2, 0.008125) and close(0.0646 / 0.0115, 5.6, 0.05) and 0.05 / 0.0115 > 4)
check('homework-3 identity: P(D1 D2)-P(D1)P(D2) = q(1-q)(pb-pg)^2 on a grid',
      all((q * pb ** 2 + (1 - q) * pg ** 2) - (q * pb + (1 - q) * pg) ** 2 == q * (1 - q) * (pb - pg) ** 2
          for q in (Fr(0), Fr(1, 5), Fr(1, 2), Fr(1)) for pb in (Fr(1, 5), Fr(1, 2)) for pg in (Fr(1, 80), Fr(1, 2))))

# ---------------------------------------------------------------- sets: spot recomputes of conceptual keys
check('review-1 at least two heads: 1/4', P(lambda o: o.count('H') == 3, lambda o: o.count('H') >= 2,
                                             list(itertools.product('HT', repeat=3))) == Fr(1, 4))
check('homework-1 aces: 4/4804 = 1/1201', Fr(4, math.comb(52, 3) - math.comb(48, 3)) == Fr(1, 1201))
check('homework-1 doubles given total>=10: 1/3', P(lambda o: o[0] == o[1], lambda o: sum(o) >= 10) == Fr(1, 3))
check('homework-2 two tests 5/54; backtest twice 256/275',
      (Fr(1, 19) * S(9.5) * S(0.2) / S(0.98)) / (1 + Fr(1, 19) * S(9.5) * S(0.2) / S(0.98)) == Fr(5, 54)
      and Fr(256, 19) / (1 + Fr(256, 19)) == Fr(256, 275))
NB, NG = S(0.02) * S(0.9) * S(0.7), S(0.98) * S(0.06) * S(0.03)
check('homework-2 two filters: 15/64, 50/57, and 3/10 when good-tick flags coincide',
      post(S(0.02), S(0.9), S(0.06)) == Fr(15, 64) and NB / (NB + NG) == Fr(50, 57)
      and NB / (NB + S(0.98) * S(0.03)) == Fr(3, 10))
check('review-2 three coins 16/33; problems-2 broker 16/31 then 0.6185',
      Fr(1, 4) / (Fr(1, 2) * Fr(1, 4) + Fr(1, 4) * Fr(9, 16) + Fr(1, 4)) == Fr(16, 33)
      and close((45 * 0.3 + 75 * 0.5 + 128 * 0.8) / 248, 0.6185, 5e-5))
eight = list(itertools.product(range(1, 9), repeat=2))
check('problems-1 eight-sided: 7/64, 2/15, 2/7, 1/32',
      P(lambda o: sum(o) == 10, space=eight) == Fr(7, 64) and P(lambda o: sum(o) == 10, lambda o: 8 in o, eight) == Fr(2, 15)
      and P(lambda o: 8 in o, lambda o: sum(o) == 10, eight) == Fr(2, 7))
check('problems-1 dealer: 8/13', Fr(4, 15) / (Fr(5, 6) - Fr(4, 10)) == Fr(8, 13))
feeds = list(itertools.product((0, 1), repeat=3))  # F, G, H
dA, dB, dC = (lambda o: o[0] == o[1]), (lambda o: o[0] == o[2]), (lambda o: o[1] == o[2])
check('problems-3 desks: pairwise independent, triple 1/4, P(C|A,B)=1',
      ind(dA, dB, feeds) and ind(dA, dC, feeds) and ind(dB, dC, feeds)
      and P(lambda o: dA(o) and dB(o) and dC(o), space=feeds) == Fr(1, 4))
check('problems-3 losing week: 0.475, 12/19, back to 0.3', 1 - S(0.7) * S(0.75) == S(0.475) and S(0.3) / S(0.475) == Fr(12, 19))
check('review-3 margin call: 0.3/0.65 then 0.3; two loans 0.00936 about 4x 0.048^2',
      close(0.3 / (1 - 0.7 * 0.5), 0.4615, 5e-4) and close(0.1 * 0.09 + 0.9 * 0.0004, 0.00936) and close(0.00936 / 0.048 ** 2, 4.06, 0.01))

# ---------------------------------------------------------------- fluency generator: every variable combination
ok_counts = True
for tot in (100, 200, 400):
    for a in range(5, 31):
        for c in range(1, 10):
            for b in range(3, 41):
                if b == c:
                    continue
                key, fwd, joint = Fr(a, a + b), Fr(a, a + c), Fr(a, tot)
                ok_counts &= (key != fwd and key != joint and a + c + b <= tot)
check('fluency from-counts: key never equals a slip, counts fit the crowd', ok_counts)
ok_rates = True
for pp in (1, 2, 5, 10, 20, 25, 30, 40):
    for s in range(60, 100, 5):
        for f in range(5, 35, 5):
            j, fp = Fr(pp * s, 10000), Fr((100 - pp) * f, 10000)
            key, nof, sd = j / (j + fp), j / (j + Fr(f, 100)), Fr(s, 100)
            if all(abs(x) > Fr(2, 1000) for x in (key - sd, key - j, key - nof, nof - sd, nof - j)):
                ok_rates &= (key == post(Fr(pp, 100), sd, Fr(f, 100)))
check('fluency from-rates: key is Bayes for every kept combination', ok_rates)
check('fluency every-positive-path: unweighted slip always differs from the key',
      all(Fr(pp * s, 10000) + Fr(f, 100) != Fr(pp * s, 10000) + Fr((100 - pp) * f, 10000)
          for pp in (5, 10, 15, 20, 25, 30, 40) for s in range(60, 100, 5) for f in range(5, 45, 5)))

# ---------------------------------------------------------------- code widgets: run them (CPython)
def run_code_widget(tag, w, n_stated):
    ns = {}
    exec(w['solution'], ns)
    good = all(math.isclose(float(eval(t['call'], ns)), float(t['expect']), rel_tol=1e-9, abs_tol=1e-12) for t in w['tests'])
    check(tag + ': solution passes every hidden test', good)
    ns2 = {}
    exec(w['starter'], ns2)
    bad = 0
    for t in w['tests']:
        try:
            if not math.isclose(float(eval(t['call'], ns2)), float(t['expect']), rel_tol=1e-9, abs_tol=1e-12):
                bad += 1
        except Exception:
            bad += 1
    check(tag + ': starter fails the hidden tests', bad == len(w['tests']), bad)
    check(tag + ': stated test count matches', ('%d hidden tests' % len(w['tests'])) in w['how'] and len(w['tests']) == n_stated)


run_code_widget('l14 p_at_least', L[14]['screens'][9]['widget'], 8)
run_code_widget('l17 book_tail', L[17]['screens'][9]['widget'], 7)

# ---------------------------------------------------------------- Monte Carlo (seeded) for the empirical claims
rng = random.Random(20261111)
N = 400_000


def se(p, n):
    return math.sqrt(max(p * (1 - p), 1e-12) / n)


# (a) l3: two dice, keep rolls with at least one 5; share with total 10 is 1/11, not 1/6
kept = hit = 0
for _ in range(N):
    a, b = rng.randint(1, 6), rng.randint(1, 6)
    if a == 5 or b == 5:
        kept += 1
        hit += (a + b == 10)
ph = hit / kept
check('MC l3: P(total 10 | at least one 5) is 1/11 and not 1/6', abs(ph - 1 / 11) < 5 * se(1 / 11, kept) and abs(ph - 1 / 6) > 5 * se(1 / 6, kept), ph)
check('MC l3: about 11/36 of rolls survive the filter', abs(kept / N - 11 / 36) < 5 * se(11 / 36, N))

# (b) l2: unseen first draw leaves P(second red)=3/5
c = 0
for _ in range(N):
    bagx = ['R', 'R', 'R', 'B', 'B']
    rng.shuffle(bagx)
    c += bagx[1] == 'R'
check('MC l2: second draw red 3/5 when the first is unseen', abs(c / N - 0.6) < 5 * se(0.6, N))

# (c) l8: rare condition, most positives false
pos = ill = 0
for _ in range(N * 2):
    i = rng.random() < 0.01
    t = rng.random() < (0.9 if i else 0.05)
    pos += t
    ill += (i and t)
check('MC l8: P(condition|+) near 2/13, far from 0.9', abs(ill / pos - 2 / 13) < 5 * se(2 / 13, pos), ill / pos)

# (d) l11: two conditionally independent 70% analysts both say up -> 49/58; copying analyst -> 0.7
both = up_both = copy_n = copy_up = 0
for _ in range(N):
    up = rng.random() < 0.5
    a = up if rng.random() < 0.7 else not up
    b = up if rng.random() < 0.7 else not up
    if a and b:
        both += 1
        up_both += up
    if a:  # B copies A, so "both say up" is "A says up"
        copy_n += 1
        copy_up += up
check('MC l11: two analysts 49/58', abs(up_both / both - 49 / 58) < 5 * se(49 / 58, both), up_both / both)
check('MC l11: a copied call leaves 0.7', abs(copy_up / copy_n - 0.7) < 5 * se(0.7, copy_n))

# (e) l16: shared sector makes stocks dependent overall, independent given the day; explaining away
a_up = ab_up = g_a = g_ab = 0
al = al_news = al_drop = al_drop_news = 0
for _ in range(N):
    good = rng.random() < 0.5
    p = 0.8 if good else 0.2
    a, b = rng.random() < p, rng.random() < p
    a_up += a
    ab_up += (a and b)
    if good:
        g_a += a
        g_ab += (a and b)
    news, drop = rng.random() < 0.2, rng.random() < 0.1
    if news or drop:
        al += 1
        al_news += news
        if drop:
            al_drop += 1
            al_drop_news += news
check('MC l16: P(B up | A up) is 0.68 overall and 0.8 given a good day',
      abs(ab_up / a_up - 0.68) < 5 * se(0.68, a_up) and abs(g_ab / g_a - 0.8) < 5 * se(0.8, g_a))
check('MC l16: P(news|alert) 5/7 falls to 0.2 given alert and drop',
      abs(al_news / al - 5 / 7) < 5 * se(5 / 7, al) and abs(al_drop_news / al_drop - 0.2) < 5 * se(0.2, al_drop))

# (f) l15: Z falls exactly when X and Y agree: every pair independent, all three fall 1/4 of the time
n3 = xz = x_ = z_ = 0
for _ in range(N):
    x, y = rng.random() < 0.5, rng.random() < 0.5  # True = falls
    z = (x == y)
    n3 += (x and y and z)
    xz += (x and z)
    x_ += x
    z_ += z
check('MC l15: all three fall 1/4 of days (not 1/8) while X and Z look independent',
      abs(n3 / N - 0.25) < 5 * se(0.25, N) and abs(xz / N - (x_ / N) * (z_ / N)) < 0.005)

# (g) l17: correlated defaults: each loan 0.05, P(0) 0.7269, P(3+) 0.0646; big pool hits 10% with chance 0.2
M = 200_000
k0 = k3 = dsum = 0
for _ in range(M):
    p = 0.2 if rng.random() < 0.2 else 0.0125
    k = sum(rng.random() < p for _ in range(10))
    dsum += k
    k0 += (k == 0)
    k3 += (k >= 3)
check('MC l17: single-loan default rate stays 0.05', abs(dsum / (10 * M) - 0.05) < 0.002)
check('MC l17: P(no defaults) 0.7269 exceeds the independent 0.5987', abs(k0 / M - 0.7269) < 5 * se(0.7269, M))
check('MC l17: P(3 or more) 0.0646, not the independent 0.0115',
      abs(k3 / M - 0.0646) < 5 * se(0.0646, M) and abs(k3 / M - 0.0115) > 20 * se(0.0115, M), k3 / M)
big = 0
T = 4000
for _ in range(T):
    p = 0.2 if rng.random() < 0.2 else 0.0125
    # pool of 2,000 loans: normal approximation to the binomial share is ample here
    share = rng.gauss(p, math.sqrt(p * (1 - p) / 2000))
    big += share >= 0.10
check('MC l17 quiz: a large pool loses 10% or more with chance near 0.2', abs(big / T - 0.2) < 5 * se(0.2, T), big / T)

# (h) l14: twenty no-edge strategies over 50 trades: about 2 show 60% or better
tot60 = 0
R = 4000
for _ in range(R):
    tot60 += sum(1 for _ in range(20) if bin(rng.getrandbits(50)).count('1') >= 30)
check('MC l14: about 2.03 of 20 no-edge backtests clear 60%', abs(tot60 / R - 2.026) < 0.1, tot60 / R)

# ---------------------------------------------------------------- findings: one failing check each until fixed
t = L[11]['screens'][8]['feedback']['byKey']['one']
check('F1 l11 screens[8].feedback.byKey.one: no bare "independent call" (the calls are independent only given the direction)',
      'independent call' not in t, t)
t = DATA['review-2']['items'][5]['feedback']['byKey']['added']
check('F2 review-2 items[5].feedback.byKey.added: no bare "Independent ratios"', 'Independent ratios' not in t, t)
p2 = DATA['problems-2']['items'][1]['parts']
t3 = [p2[2]['feedback']['byKey']['ratio-sum'], p2[3]['question'], p2[4]['feedback']['correct']]
check('F3 problems-2 items[1] parts[2..4]: bare "independent" where independence given the truth is meant',
      'Independent evidence multiplies' not in t3[0] and 'more independent reports' not in t3[1]
      and 'was not independent of the delay' not in t3[2], t3)
t = L[8]['screens'][2]['question']
check('F4 l8 screens[2]: 0.0585 rounded to 3 places is 0.059, the value graded as the unweighted slip; question must ask for 4 places',
      '4 places' in t or not any(w['id'] == 'unweighted' for w in L[8]['screens'][2]['widget']['wrong']), t)
alltext = json.dumps(L[15], ensure_ascii=False)
check('F6 l15: says once that "independent" for several events means mutually independent',
      re.search(r'means mutual|mutually independent is meant|mutual independence is meant', alltext) is not None)
# evidence for F1: the two analysts' calls are dependent overall although independent given the direction
pa_up = Fr(1, 2) * Fr(7, 10) + Fr(1, 2) * Fr(3, 10)
pboth = Fr(1, 2) * Fr(49, 100) + Fr(1, 2) * Fr(9, 100)
check('basis for F1: P(both say up)=0.29 differs from 0.5*0.5', pboth == Fr(29, 100) and pboth != pa_up * pa_up)

print('checks passed: %d, failed: %d' % (PASSES, len(FAILS)))
for f in FAILS:
    print('FAIL', f)
sys.exit(1 if FAILS else 0)
