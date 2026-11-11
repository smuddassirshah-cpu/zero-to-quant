#!/usr/bin/env python3
"""Concept checks for conditional levels 4 and 5 (blind audit, round 1).

Run from the repo root with no arguments:  python3 docs/reports/conditional-L4-5-concepts.py
Exit 0 only when every check passes. Checks tagged [F<n>] test a content
string named in docs/reviews/audit-conditional-4-5.md and stay failing until
that finding's fix is applied. Values come from exact enumeration (fractions)
or seeded Monte Carlo (CPython `random`, Mersenne Twister, the same generator
Pyodide uses). Run with CPython 3.13; no NumPy is needed.
"""
import contextlib
import io
import json
import math
import os
import random
import sys
from fractions import Fraction as Fr
from itertools import product
from statistics import NormalDist

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
CDIR = os.path.join(ROOT, 'app', 'content', 'courses', 'conditional')
FAILS = []
COUNT = [0]


def load(name):
    with open(os.path.join(CDIR, name + '.json'), encoding='utf-8') as fh:
        return json.load(fh)


def check(name, cond, detail=''):
    COUNT[0] += 1
    if not cond:
        FAILS.append(name)
    print(('ok   ' if cond else 'FAIL ') + name + ((' | ' + str(detail)) if detail != '' else ''))


def near(a, b, tol):
    return abs(a - b) <= tol


def by_id(seq, key):
    return next(x for x in seq if x.get('id') == key)


L18, L19, L20, L21 = load('l18-monty-hall'), load('l19-bertrands-box'), load('l20-two-children'), load('l21-tuesday-boy')
L22, L23, L24, L25, L26 = (load('l22-gamblers-fallacy'), load('l23-prosecutors-fallacy'),
                           load('l24-simpsons-paradox'), load('l25-survivorship'), load('l26-trading-signal'))
R4, R5, H4, H5, P4, P5 = (load('review-4'), load('review-5'), load('homework-4'), load('homework-5'),
                          load('problems-4'), load('problems-5'))
rng = random.Random(20261111)

# ---------------------------------------------------------------- Monty Hall
print('--- Monty Hall')


def monty_exact(q3):
    """Knowing host, you pick door 1. With the car behind 1 he opens door 3 with
    chance q3. Returns P(car at 1 | opens 3), P(car at 2 | opens 3)."""
    paths = {1: Fr(1, 3) * q3, 2: Fr(1, 3) * 1, 3: Fr(0)}
    tot = sum(paths.values())
    return paths[1] / tot, paths[2] / tot


c1, c2 = monty_exact(Fr(1, 2))
check('monty: fair knowing host, P(car 2 | opens 3) = 2/3', c2 == Fr(2, 3) and c1 == Fr(1, 3))
c1, c2 = monty_exact(Fr(1))
check('monty: lazy host (always 3 when free), door 1 moves to 1/2', c1 == Fr(1, 2) and c2 == Fr(1, 2),
      'so "he can never open door 1, so door 1 cannot move" is not a valid inference')
for q in (Fr(0), Fr(1, 4), Fr(1, 2), Fr(3, 4), Fr(1)):
    assert monty_exact(q)[1] == 1 / (1 + q)
check('monty: homework formula 1/(1+q) holds for q in {0,1/4,1/2,3/4,1}', True)
# random host, conditional on door 3 opened and a goat shown
paths = {c: Fr(1, 3) * Fr(1, 2) * (0 if c == 3 else 1) for c in (1, 2, 3)}
check('monty: random host who happens to show a goat gives 1/2', paths[2] / sum(paths.values()) == Fr(1, 2))
# simulation of both hosts
n_k = w_k = n_r = w_r = 0
for _ in range(200000):
    car = rng.randrange(3)
    opened = rng.choice([d for d in (1, 2) if d != car])     # knowing, pick = 0
    if opened == 2:
        n_k += 1
        w_k += (car == 1)
    opened = rng.choice((1, 2))                               # random host
    if opened == 2 and car != 2:
        n_r += 1
        w_r += (car == 1)
check('monty MC: knowing host switch wins about 2/3', near(w_k / n_k, 2 / 3, 0.01), round(w_k / n_k, 4))
check('monty MC: random host switch wins about 1/2', near(w_r / n_r, 1 / 2, 0.01), round(w_r / n_r, 4))
check('monty: four doors, one goat opened, random switch = 3/8', Fr(3, 4) * Fr(1, 2) == Fr(3, 8))
check('monty: 100 doors 99/100; homework four doors 3/4', 1 - Fr(1, 100) == Fr(99, 100) and 1 - Fr(1, 4) == Fr(3, 4))
ps, pn = Fr(3, 10) + Fr(7, 10) * Fr(1, 2), Fr(7, 10) * Fr(1, 2)
check('monty transfer: P(99 | sell) = 0.65', ps / (ps + pn) == Fr(13, 20))
pb, pb2 = Fr(2, 10) + Fr(8, 10) * Fr(1, 2), Fr(8, 10) * Fr(1, 2)
check('homework-4 ask price 100.20', pb / (pb + pb2) * 101 + pb2 / (pb + pb2) * 99 == Fr(1002, 10))
why = by_id(L18['screens'][7]['widget']['options'], 'door-one')['why']
check('[F1] l18 trap why does not argue "could never open door 1, so ... nothing new"',
      'so his move says nothing new' not in why, why)
check('[F1] l18 first problem states the host always opens a goat door',
      'always' in L18['screens'][1]['prose'], L18['screens'][1]['prose'])
it = by_id(R4['items'], 'r-monty-stay')
check('[F2] review-4 r-monty-stay states the tie-break (at random)', 'at random' in it['prose'], it['prose'])

# ---------------------------------------------------------------- Bertrand
print('--- Bertrand box')
boxes = ['GG', 'SS', 'GS']
draw = {b: Fr(b.count('G'), 2) for b in boxes}
check('bertrand: drawn gold gives GG 2/3', draw['GG'] / sum(draw.values()) == Fr(2, 3))
yes = {b: Fr(1 if 'G' in b else 0) for b in boxes}
check('bertrand: clerk answering "any gold?" gives GG 1/2', yes['GG'] / sum(yes.values()) == Fr(1, 2))
# a clerk who names the colour of a coin he looks at (random coin) and says "at least one <colour>"
vol = {b: Fr(b.count('G'), 2) for b in boxes}
check('bertrand: clerk who reports a random coin\'s colour gives GG 2/3 (the option marked wrong)',
      vol['GG'] / sum(vol.values()) == Fr(2, 3))
check('[F3] l19 clerk screen states the clerk\'s rule', 'His rule' in L19['screens'][7]['prose'], L19['screens'][7]['prose'])
four = {'GG': Fr(1), 'GS1': Fr(1, 2), 'GS2': Fr(1, 2), 'SS': Fr(0)}
check('bertrand: second GS box gives 1/2', four['GG'] / sum(four.values()) == Fr(1, 2))
check('bertrand: fund classes 6/8, three-coin boxes 3/4', Fr(6, 8) == Fr(3, 4) and Fr(3, 3 + 1) == Fr(3, 4))
w = [Fr(3, 3), Fr(2, 3), Fr(1, 3), Fr(0)]
post = [x / sum(w) for x in w]
check('homework-4 second draw 2/3', post[0] * 1 + post[1] * Fr(1, 2) + post[2] * 0 == Fr(2, 3))
check('problems-4 marble bags: 0.5, 0.4, 1/(1+3h) at h=1/2 is 0.4, h=1 is 1/4',
      Fr(1, 5) + Fr(3, 5) * Fr(1, 2) == Fr(1, 2) and Fr(1, 5) / Fr(1, 2) == Fr(2, 5)
      and 1 / (1 + 3 * Fr(1, 2)) == Fr(2, 5) and 1 / (1 + 3 * Fr(1)) == Fr(1, 4))
check('problems-4 two strategies: 0.91, 0.455, 7/13, 7/22',
      1 - Fr(9, 100) == Fr(91, 100) and Fr(21, 100) + Fr(49, 200) == Fr(455, 1000)
      and Fr(245, 455) == Fr(7, 13) == Fr(49, 91) and Fr(98, 98 + 210) == Fr(7, 22))
check('problems-4 dated coins: 0.8, 0.19, 19/24, limit 0.8',
      Fr(4, 5) == Fr(8, 10) and 1 - Fr(9, 10) ** 2 == Fr(19, 100)
      and Fr(1, 2) * Fr(19, 100) / (Fr(1, 2) * Fr(19, 100) + Fr(1, 4) * Fr(1, 10)) == Fr(19, 24)
      and Fr(4, 5) == Fr(2 * 2, 2 * 2 + 1))

# ---------------------------------------------------------------- Two children
print('--- two children and the Tuesday boy')
fams = [a + b for a in 'BG' for b in 'BG']
check('children: filter "at least one boy" gives 1/3', Fr(1, sum('B' in f for f in fams)) == Fr(1, 3))
meet = {f: Fr(f.count('B'), 2) for f in fams}
check('children: meet a random child, a boy, gives 1/2', meet['BB'] / sum(meet.values()) == Fr(1, 2))
check('children: a parent who mentions the sex of a random child and says "at least one is a boy" gives 1/2',
      meet['BB'] / sum(meet.values()) == Fr(1, 2), 'same words, different procedure: the option marked wrong')
check('[F4] l20 "at least one" screen states how the fact was learnt (a question asked)',
      'ask' in L20['screens'][2]['prose'].lower(), L20['screens'][2]['prose'])
check('children: three children 1/7; trader 3/7; trader random pick 0.6; homework 121/319',
      Fr(1, 7) == Fr(1, 8) / Fr(7, 8) and Fr(36, 84) == Fr(3, 7)
      and Fr(36, 100) / (Fr(36, 100) + Fr(48, 100) * Fr(1, 2)) == Fr(6, 10)
      and Fr(3025, 7975) == Fr(121, 319))


def detail_formula(k):
    kids = [(s, d) for s in 'BG' for d in range(k)]
    fit = [(a, b) for a in kids for b in kids if ('B', 0) in (a, b)]
    bb = [f for f in fit if f[0][0] == 'B' and f[1][0] == 'B']
    return len(fit), Fr(len(bb), len(fit))


check('tuesday: k=2 gives 7 and 3/7; k=7 gives 27 and 13/27', detail_formula(2) == (7, Fr(3, 7)) and detail_formula(7) == (27, Fr(13, 27)))
check('tuesday: (2k-1)/(4k-1) for k = 1,3,4,6,12,365',
      all(detail_formula(k)[1] == Fr(2 * k - 1, 4 * k - 1) for k in (1, 3, 4, 6, 12, 365)),
      [str(detail_formula(k)[1]) for k in (1, 3, 4, 6, 12)])
check('tuesday: smallest k within 0.01 of 1/2 is 13',
      min(k for k in range(1, 100) if Fr(1, 2) - Fr(2 * k - 1, 4 * k - 1) <= Fr(1, 100)) == 13)
# procedures (b) and (c) of the homework long-form, by enumeration
kids = [(s, d) for s in 'BG' for d in range(7)]
num_b = den_b = num_c = den_c = Fr(0)
for a in kids:
    for b in kids:
        pr = Fr(1, 196)
        both = a[0] == 'B' and b[0] == 'B'
        for child in (a, b):                       # (b) random child reported
            if child == ('B', 1):
                den_b += pr / 2
                num_b += pr / 2 * both
        sons = [c for c in (a, b) if c[0] == 'B']  # (c) random son's weekday
        for s in sons:
            if s[1] == 1:
                den_c += pr / len(sons)
                num_c += pr / len(sons) * both
check('tuesday: random child reported gives 1/2; random son\'s weekday gives 1/3',
      num_b / den_b == Fr(1, 2) and num_c / den_c == Fr(1, 3))
q = Fr(6, 10) / 390
filt = Fr(36, 100) * (1 - (1 - Fr(1, 390)) ** 2) / (1 - (1 - q) ** 2)
check('tuesday transfer: yes/no filter "a winner at 10:17" gives 779/1299', filt == Fr(779, 1299), float(filt))
# the report names the minute of a winning trade (a random winner if two): the minute carries no information
lik_both, lik_one = Fr(1, 390), Fr(1, 390)
named = Fr(36, 100) * lik_both / (Fr(36, 100) * lik_both + Fr(48, 100) * lik_one)
check('tuesday transfer: a report that names a winner\'s minute gives 3/7 (the option marked wrong)', named == Fr(3, 7))
check('[F5] l21 transfer states the procedure behind the report (a yes/no question)',
      '?' in L21['screens'][9]['prose'], L21['screens'][9]['prose'])
check('homework-4 left-handed boy 19/39 and (2-q)/(4-q)',
      Fr(19, 100) / (Fr(19, 100) + 2 * Fr(1, 10)) == Fr(19, 39)
      and all((2 * x - x * x) / ((2 * x - x * x) + 2 * x) == (2 - x) / (4 - x) for x in (Fr(1, 7), Fr(1, 10), Fr(1))))

# ---------------------------------------------------------------- code widgets
print('--- code widgets (CPython 3.13)')


def run_code(widget, which):
    ns = {}
    with contextlib.redirect_stdout(io.StringIO()) as out:
        try:
            exec(widget[which], ns)
        except Exception as exc:                    # starter may stop with an error
            return ns, out.getvalue(), exc
    return ns, out.getvalue(), None


def close(a, b):
    if a is None or b is None:
        return a is b
    if isinstance(b, (list, tuple)):
        return isinstance(a, (list, tuple)) and len(a) == len(b) and all(close(x, y) for x, y in zip(a, b))
    return isinstance(a, (int, float)) and math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)


def passes(widget, which):
    ns, _, _ = run_code(widget, which)
    n = 0
    for t in widget['tests']:
        try:
            env = dict(ns)
            if t.get('setup'):
                exec(t['setup'], env)
            got = eval(t['call'], env)
            exp = t['expect']
            exp = eval(exp, {}) if isinstance(exp, str) else exp
            n += close(got, exp)
        except Exception:
            pass
    return n, len(widget['tests'])


for label, wd, stated in (('l20 filters', L20['screens'][7]['widget'], 9),
                          ('homework-4 hosts', by_id(H4['items'], 'h-host-rules-code')['widget'], 11),
                          ('homework-5 share_after_run', by_id(H5['items'], 'h-share-after-run')['widget'], 5)):
    ok, tot = passes(wd, 'solution')
    sk, _ = passes(wd, 'starter')
    check(f'{label}: solution passes {tot}/{tot} hidden tests, starter passes none, stated count {stated}',
          ok == tot and sk == 0 and tot == stated, f'solution {ok}/{tot}, starter {sk}/{tot}')
_, out, _ = run_code(L20['screens'][7]['widget'], 'solution')
vals = [float(x) for x in out.split()]
check('l20 code prints 0.330 and 0.492 with seed 4', [round(v, 3) for v in vals] == [0.33, 0.492], vals)
ns, _, _ = run_code(by_id(H5['items'], 'h-share-after-run')['widget'], 'solution')
r7 = random.Random(7)
seq = ''.join(r7.choice('HT') for _ in range(200000))
check('homework-5 seeded share 0.513', round(ns['share_after_run'](seq, 5), 3) == 0.513, ns['share_after_run'](seq, 5))

# ---------------------------------------------------------------- gambler's fallacy
print('--- gambler\'s fallacy')
kept = heads = 0
for _ in range(400000):
    t = [rng.random() < 0.5 for _ in range(6)]
    if not any(t[:5]):
        kept += 1
        heads += t[5]
check('gambler MC: sixth toss after five tails is a head about half the time',
      near(heads / kept, 0.5, 0.02) and near(kept / 400000, 1 / 32, 0.002), (kept, round(heads / kept, 4)))
vals = L22['screens'][3]['canvas']['left']['params']['series'][0]['values']
share = lambda n: (n + vals[n]) / 2 / n
check('gambler: stored walk has gap -6, share 0.470 at 100 and gap -24, share 0.488 at 1,000',
      vals[100] == -6 and vals[1000] == -24 and round(share(100), 3) == 0.47 and round(share(1000), 3) == 0.488)
check('gambler: stored share stays within 0.03 of 0.5 after 300 tosses', max(abs(share(n) - 0.5) for n in range(300, 1001)) < 0.03)
# dilution, not compensation: after 5 tails the expected gap stays 5; share -> 1/2
gap_sum = sh_sum = 0
for _ in range(20000):
    h = sum(rng.random() < 0.5 for _ in range(95))
    gap_sum += (5 + 95 - h) - h
    sh_sum += h / 100
check('gambler MC: five tails then 95 fair tosses, mean tails-heads about 5 and share about 0.475',
      near(gap_sum / 20000, 5, 0.3) and near(sh_sum / 20000, 0.475, 0.002), (round(gap_sum / 20000, 3), round(sh_sum / 20000, 4)))
# the gap of a fair coin: it is not pulled back, but it does come back to 0 and often shrinks
shr = ret = 0
a100 = a1000 = 0
for _ in range(4000):
    s = 0
    s100 = None
    back = False
    for i in range(1, 1001):
        s += 1 if rng.random() < 0.5 else -1
        if i == 100:
            s100 = s
        if i > 100 and s == 0:
            back = True
    shr += abs(s) < abs(s100)
    ret += back
    a100 += abs(s100)
    a1000 += abs(s)
check('gambler MC: mean |gap| grows from 100 to 1,000 tosses (about 8 to about 25)',
      a1000 / 4000 > 2.5 * a100 / 4000, (round(a100 / 4000, 2), round(a1000 / 4000, 2)))
check('gambler MC: yet in a sizeable share of paths the gap is smaller at 1,000 than at 100, and most paths revisit 0',
      shr / 4000 > 0.15 and ret / 4000 > 0.5, (round(shr / 4000, 3), round(ret / 4000, 3)))
check('[F9] l22 summary does not say the gap "does not shrink back" as a rule',
      'does not shrink back' not in L22['summary']['ideas'][1], L22['summary']['ideas'][1])
check('gambler: cards 21/47, two coins 243/275, next tail about 0.72',
      round(21 / 47, 4) == 0.4468 and Fr(243, 243 + 32) == Fr(243, 275)
      and near(float(Fr(243, 275) * Fr(3, 4) + Fr(32, 275) * Fr(1, 2)), 0.72, 0.002))
check('gambler: doubling EV 0 for caps 4,5,6,10; unfair cap 3 is -0.331',
      all(Fr(2 ** k - 1, 2 ** k) - Fr(1, 2 ** k) * (2 ** k - 1) == 0 for k in (4, 5, 6, 10))
      and near((1 - 0.55 ** 3) - 7 * 0.55 ** 3, -0.331, 0.0005))
q0 = by_id(L22['quiz'], 'q-roulette')
left = by_id(q0['widget']['wrong'], 'left')
check('[F8] l22 roulette slip value matches its feedback (eight blacks removed is 18/29 = 0.6207; 0.4737 is 18/38)',
      near(left['value'], 18 / 29, 0.001) or '38' in q0['feedback']['byKey']['left'],
      (left['value'], round(18 / 29, 4), round(18 / 38, 4)))
p20 = (31 / 32) ** 20
check('problems-5 doubling desk: (31/32)^20 = 0.5299, quitters average -22.55',
      round(p20, 4) == 0.5299 and near(-p20 * 20 / (1 - p20), -22.55, 0.005), (p20, -p20 * 20 / (1 - p20)))
tot = quitn = quits = 0
for _ in range(200000):
    profit = 0
    quit_ = False
    for _r in range(20):
        if rng.random() < 1 / 32:
            profit -= 31
            quit_ = True
            break
        profit += 1
    tot += profit
    if quit_:
        quitn += 1
        quits += profit
check('problems-5 MC: all traders average about 0, quitters about -22.5',
      near(tot / 200000, 0, 0.15) and near(quits / quitn, -22.55, 0.15), (round(tot / 200000, 3), round(quits / quitn, 3)))
pg = 0.4096 / 1.4096
check('problems-5 signal streak: 0.4096, 0.2906, 0.5291, 0.0582',
      near(0.8 ** 4, 0.4096, 1e-9) and round(pg, 4) == 0.2906 and round(pg * 0.6 + (1 - pg) * 0.5, 4) == 0.5291
      and round(2 * 0.5291 - 1, 4) == 0.0582 and near(2 * (pg * 0.6 + (1 - pg) * 0.5) - 1, 0.0582, 0.0005))
ph = 1.4 ** 4 / (1 + 1.4 ** 4)
check('homework-5 heavy coin 0.6587', near(ph * 0.7 + (1 - ph) * 0.5, 0.6587, 0.0005))

# ---------------------------------------------------------------- prosecutor
print('--- prosecutor\'s fallacy')
inn = Fr(4999999, 10 ** 6)
check('prosecutor: city of 5m, P(innocent | match) about 5/6, P(guilty) about 1/6',
      near(float(inn / (1 + inn)), 5 / 6, 1e-6))
check('prosecutor: 10 suspects 0.99999; 1 in 10m test 2/3; quiz 1/3; homework 1/7; review 1/51',
      near(1 / 1.000009, 0.99999, 2e-6) and near(1 / (1 + 4999999 / 1e7), 2 / 3, 1e-6)
      and near(1 / (1 + 199999 / 1e5), 1 / 3, 1e-5) and near(1 / (1 + 299999 / 5e4), 1 / 7, 1e-5)
      and Fr(1, 51) == Fr(1, 1 + 50))
# p-values under the null are uniform: a one-sided z test on 100 normal returns
nd = NormalDist()
hits = 0
N = 20000
for _ in range(N):
    m = sum(rng.gauss(0, 1) for _ in range(100)) / 100
    hits += (1 - nd.cdf(m * 10)) < 0.01
check('prosecutor MC: with no edge, P(p < 0.01) is about 0.01', near(hits / N, 0.01, 0.003), hits / N)
false = true = 0
for _ in range(400):                      # 400 batches of 1,000 strategies, 20 with an edge and power 0.5
    false += sum(rng.random() < 0.01 for _ in range(980))
    true += sum(rng.random() < 0.5 for _ in range(20))
check('prosecutor MC: 20 real edges in 1,000, about half the passes are false',
      near(false / (false + true), 9.8 / 19.8, 0.02), round(false / (false + true), 4))
check('prosecutor: homework long-form 6/10.9 = 0.55; posterior does not depend on the number tried at a fixed share',
      near(6 / 10.9, 0.55, 0.001)
      and all(near((n * 0.02 * 0.6) / (n * 0.02 * 0.6 + n * 0.98 * 0.01), 6 / 10.9, 1e-12) for n in (50, 500, 5000)))
model = by_id(H5['items'], 'h-long-pvalue')['model']
check('[F11] homework-5 model answer does not list "fewer designs are tried" as raising the posterior',
      'fewer designs are tried' not in model)
check('[F10] l23 summary states the p-value as a result at least this good',
      'this good' in L23['summary']['ideas'][2] or 'at least' in L23['summary']['ideas'][2], L23['summary']['ideas'][2])
check('problems-5 warning screen: 0.3125, 0.6875, 40/51, 29/51',
      Fr(90, 288) == Fr(5, 16) and Fr(198, 288) == Fr(11, 16) and Fr(5, 11) * 8 / (1 + Fr(5, 11) * 8) == Fr(40, 51)
      and 2 * Fr(40, 51) - 1 == Fr(29, 51))

# ---------------------------------------------------------------- Simpson
print('--- Simpson\'s paradox')
check('simpson: hospital 0.6875 v 0.80; crossover at 3/7 severe; same mix 0.60',
      Fr(275, 400) == Fr(11, 16) and Fr(320, 400) == Fr(4, 5)
      and (Fr(95, 100) - Fr(8, 10)) / Fr(35, 100) == Fr(3, 7) and Fr(1, 4) * Fr(9, 10) + Fr(3, 4) * Fr(1, 2) == Fr(6, 10))
check('simpson: X/Y, traders, funds, desk, strategy M/N, houses',
      (Fr(860, 1000), Fr(790, 1000)) == (Fr(86, 100), Fr(79, 100))
      and Fr(46, 100) < Fr(59, 100) and Fr(55, 100) > Fr(50, 100)
      and Fr(120, 250) < Fr(130, 250) and Fr(250, 400) > Fr(244, 400)
      and Fr(65, 100) < Fr(150, 225) and Fr(5, 8) > Fr(55, 100)
      and Fr(220, 50) == Fr(44, 10) and Fr(1, 2) * 8 - Fr(1, 2) * 2 == 3 and Fr(64, 100) * 8 - Fr(36, 100) * 2 == Fr(44, 10))
# which table answers the causal question depends on what the third variable is
# (a) confounder: severity is fixed first and drives the choice of treatment. A truly helps (+0.07 within each group).
# (b) mediator: the treatment itself changes the third variable. T truly helps overall, yet looks worse in each stratum.
N = 200000
pool = {0: [0, 0], 1: [0, 0]}
strat = {(t, z): [0, 0] for t in (0, 1) for z in (0, 1)}
do_ = {0: 0, 1: 0}
for _ in range(N):
    z = rng.random() < 0.5                              # severe
    t = rng.random() < (0.8 if z else 0.2)              # A given mostly to severe cases
    py = lambda tt: (0.5 if z else 0.9) + (0.07 if tt else 0.0)
    y = rng.random() < py(t)
    pool[t][0] += y
    pool[t][1] += 1
    strat[(t, z)][0] += y
    strat[(t, z)][1] += 1
    do_[1] += py(1)
    do_[0] += py(0)
r = lambda c: c[0] / c[1]
true_eff = (do_[1] - do_[0]) / N
check('simpson MC (confounder): pooled table has the wrong sign, each stratum has the true +0.07',
      r(pool[1]) < r(pool[0]) and all(near(r(strat[(1, z)]) - r(strat[(0, z)]), true_eff, 0.02) for z in (0, 1)),
      (round(r(pool[1]) - r(pool[0]), 3), round(true_eff, 3)))
pool = {0: [0, 0], 1: [0, 0]}
strat = {(t, m): [0, 0] for t in (0, 1) for m in (0, 1)}
for _ in range(N):
    t = rng.random() < 0.5                              # randomised treatment
    u = rng.random() < 0.5                              # unseen frailty
    m = rng.random() < ((0.9 if t else 0.3) if not u else (0.5 if t else 0.05))   # treatment improves a marker
    y = rng.random() < (0.3 + 0.4 * m + (0.0 if u else 0.25))
    pool[t][0] += y
    pool[t][1] += 1
    strat[(t, m)][0] += y
    strat[(t, m)][1] += 1
check('simpson MC (third variable changed by the treatment): pooled table is right (T helps), every stratum says T is worse',
      r(pool[1]) > r(pool[0]) + 0.05 and all(r(strat[(1, m)]) < r(strat[(0, m)]) for m in (0, 1)),
      (round(r(pool[1]) - r(pool[0]), 3), [round(r(strat[(1, m)]) - r(strat[(0, m)]), 3) for m in (0, 1)]))
txt = ' '.join(L24['summary']['ideas']) + ' ' + L24['screens'][5]['explain']['text']
check('[F6] l24 says when to split: by a variable fixed before the choice', 'fixed before' in txt, L24['screens'][5]['explain']['text'])

# ---------------------------------------------------------------- survivorship
print('--- survivorship')
rets = [8, 6, -12, 9, 5, -8, 7, 4, -5, 10]
surv = [x for x in rets if x > 0]
check('survivorship: 7, 2.4, -8.33, gap -4.6', Fr(sum(surv), 7) == 7 and Fr(sum(rets), 10) == Fr(24, 10)
      and Fr(3, 10) * (Fr(-25, 3) - 7) == Fr(-46, 10))
acc = 0
for _ in range(50000):
    keep = rng.sample(rets, 7)
    acc += sum(keep) / 7
check('survivorship MC: random closure of 3 of the 10 funds leaves the survivors\' mean at about 2.4', near(acc / 50000, 2.4, 0.06), round(acc / 50000, 3))
up = down = alln = 0.0
ku = kd = 0
for _ in range(200000):
    x = rng.gauss(3, 8)
    alln += x
    if rng.random() < (0.9 if x > 0 else 0.4):          # losers close more often
        up += x
        ku += 1
    if rng.random() < (0.4 if x > 10 else 0.9):         # winners leave the sample more often (bought out, closed to new money)
        down += x
        kd += 1
check('survivorship MC: when losers drop out the survivors overstate; when winners drop out they understate',
      up / ku > alln / 200000 + 0.5 and down / kd < alln / 200000 - 0.5,
      (round(alln / 200000, 2), round(up / ku, 2), round(down / kd, 2)))
check('[F7] l25 summary ties the direction of the bias to failures doing worse',
      'worse' in L25['summary']['ideas'][1].split('.')[0], L25['summary']['ideas'][1])
check('survivorship: index 6 v 11.2 v 8.33; strategies -0.25; hedge funds 4.2; review 2; homework gap 5.2',
      Fr(8, 10) * 9 - Fr(2, 10) * 6 == 6 and Fr(8, 10) * 9 + Fr(2, 10) * 20 == Fr(112, 10) and Fr(720 - 120 + 400, 120) == Fr(25, 3)
      and Fr(40 - 45, 20) == Fr(-1, 4) and Fr(6, 10) * 9 - Fr(4, 10) * 3 == Fr(42, 10)
      and Fr(72 - 32, 20) == 2 and Fr(4, 10) * 13 == Fr(52, 10))

# ---------------------------------------------------------------- trading signal
print('--- trading signal')


def post(prior, *lrs):
    o = prior / (1 - prior)
    for x in lrs:
        o *= x
    return o / (1 + o)


check('signal: 0.6, 11/17, 9/13, 0.55, 77/95, 0.5, 6/13, homework 0.661',
      post(Fr(1, 2), Fr(3, 2)) == Fr(3, 5) and post(Fr(55, 100), Fr(3, 2)) == Fr(11, 17)
      and post(Fr(1, 2), Fr(3, 2), Fr(3, 2)) == Fr(9, 13) and post(Fr(55, 100), Fr(1)) == Fr(55, 100)
      and post(Fr(55, 100), Fr(3, 2), Fr(7, 3)) == Fr(77, 95) and post(Fr(4, 10), Fr(3, 2)) == Fr(1, 2)
      and post(Fr(3, 10), Fr(2)) == Fr(6, 13) and round(float(post(Fr(52, 100), Fr(3, 2), Fr(6, 5))), 3) == 0.661)
check('signal: hit rate equals detection rate at a 50% prior only when detection + false alarm = 1',
      post(Fr(1, 2), Fr(6, 4)) == Fr(6, 10) and post(Fr(1, 2), Fr(6, 3)) != Fr(6, 10) and post(Fr(55, 100), Fr(6, 4)) != Fr(6, 10))
check('signal: flashes needed for 80% from even odds is 4 (0.771 then 0.835)',
      math.ceil(math.log(4) / math.log(1.5)) == 4 and round(float(post(Fr(1, 2), Fr(27, 8))), 3) == 0.771
      and round(float(post(Fr(1, 2), Fr(81, 16))), 3) == 0.835)
# conditional independence: MC of two signals, independent given the day, and of a copied signal
n2 = u2 = nc = uc = 0
for _ in range(400000):
    upd = rng.random() < 0.5
    f1 = rng.random() < (0.6 if upd else 0.4)
    f2 = rng.random() < (0.6 if upd else 0.4)
    if f1 and f2:
        n2 += 1
        u2 += upd
    if f1:                                              # the copy flashes exactly when the first does
        nc += 1
        uc += upd
check('signal MC: two independent flashes about 0.692; a signal and its copy about 0.600',
      near(u2 / n2, 9 / 13, 0.01) and near(uc / nc, 0.6, 0.01), (round(u2 / n2, 4), round(uc / nc, 4)))


def growth(f, p):
    return p * math.log(1 + f) + (1 - p) * math.log(1 - f)


best = {p: max((x / 1000 for x in range(0, 999)), key=lambda f: growth(f, p)) for p in (0.55, 0.6, 0.7843)}
check('signal: the stake that maximises expected log growth at even money is 2p - 1',
      all(near(best[p], 2 * p - 1, 0.0011) for p in best), best)
# best of 200 designs with the same true detection rate: in-sample winner regresses on new data
ins = oos = 0
T = 300
for _ in range(T):
    true_rate = 0.55
    days = 1250                                         # up days in ten years
    scores = [sum(rng.random() < true_rate for _ in range(days)) / days for _ in range(40)]
    ins += max(scores)
    oos += sum(rng.random() < true_rate for _ in range(days)) / days
check('signal MC: the best of many equal designs scores higher in sample than on new data',
      ins / T > oos / T + 0.015, (round(ins / T, 4), round(oos / T, 4)))

print()
print(f'{COUNT[0]} checks, {len(FAILS)} failing')
for f in FAILS:
    print('  failing:', f)
sys.exit(1 if FAILS else 0)
