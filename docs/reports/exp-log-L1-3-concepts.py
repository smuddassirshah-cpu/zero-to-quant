#!/usr/bin/env python3
"""Concept audit exp-log L1-3 (round 1): independent recomputation of every graded key, slip value and stated
number the audit ledger relies on, a full-range sweep of the four fluency sets, and a Monte Carlo check of the one
statistical claim (homework-3 h-annual-vol). Exits 0 on correct content; a check that fails because the content is
wrong stays failing (see docs/reviews/audit-exp-log-1-3.md)."""
import json, math, os, sys, itertools
from fractions import Fraction
import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'exp-log')
L = lambda f: json.load(open(os.path.join(ROOT, f + '.json')))
fails, n = [], 0
def ck(label, cond):
    global n
    n += 1
    if not cond: fails.append(label)
def near(a, b, tol): return abs(a - b) <= tol + 1e-12
ln, exp, log10, log2 = math.log, math.exp, math.log10, math.log2

def widgets(doc):
    """(path, widget) for every graded widget in a file."""
    out = []
    for key in ('screens', 'quiz', 'items'):
        for i, s in enumerate(doc.get(key, [])):
            sid = s.get('id', i)
            if 'widget' in s: out.append((f'{key}[{sid}]', s['widget']))
            for j, p in enumerate(s.get('parts', [])):
                if 'widget' in p: out.append((f'{key}[{sid}].parts[{j}]', p['widget']))
    return out
def W(f, sid, part=None):
    d = L(f)
    for key in ('screens', 'quiz', 'items'):
        for i, s in enumerate(d.get(key, [])):
            if s.get('id') == sid or (isinstance(sid, int) and key == 'screens' and i == sid):
                return (s['parts'][part] if part is not None else s)['widget']
    raise KeyError((f, sid))
def key_is(f, sid, val, tol=None, part=None):
    w = W(f, sid, part)
    t = tol if tol is not None else w['tol']['abs'] if isinstance(w.get('tol'), dict) else w.get('tol', 0)
    ck(f'{f} {sid} {part} key {w["answer"]} vs {val}', near(w['answer'], val, t))
def slip_is(f, sid, wid, val, part=None):
    w = W(f, sid, part)
    e = [x for x in w['wrong'] if x['id'] == wid][0]
    ck(f'{f} {sid} {part} slip {wid} {e["value"]} vs {val}', near(e['value'], val, max(e.get('tol', {}).get('abs', 0), 1e-9)))

# ---------- every numeric key band is clear of every slip band; every choice has one key ----------
for f in sorted(os.listdir(ROOT)):
    if not f.endswith('.json') or f.startswith('fluency') or f == 'course.json': continue
    for path, w in widgets(json.load(open(os.path.join(ROOT, f)))):
        if w.get('kind') == 'numeric' and isinstance(w.get('answer'), (int, float)):
            ta = w.get('tol', {}).get('abs', 0)
            for e in w.get('wrong', []):
                tw = e.get('tol', {}).get('abs', 0)
                ck(f'{f} {path} slip {e["id"]} band meets key band', abs(e['value'] - w['answer']) > ta + tw)
        if w.get('kind') == 'choice':
            ck(f'{f} {path} one correct option', sum(1 for o in w['options'] if o.get('correct')) == 1)

# ---------- Level 1 ----------
key_is('l1-doubling', 1, 6); ck('l1 day 6', 2**6 > 1 + 60 and 2**5 < 51)
key_is('l1-doubling', 9, 2**10); ck('l1 losses 1023', sum(2**k for k in range(10)) == 1023)
ck('l1 pond day 25', 100 / 2**5 == 3.125)
ck('l1 q-race first step B ahead after step 0 is 10', min(k for k in range(1, 30) if 2**k > 100 * k) == 10)
key_is('l2-growth-factors', 4, 2000 * 0.8**3); slip_is('l2-growth-factors', 4, 'sum', 2000 * 0.4); slip_is('l2-growth-factors', 4, 'rate', 2000 * 0.2**3)
key_is('l2-growth-factors', 9, 1000 * 1.05**20)
slip_is('l2-growth-factors', 9, 'double10', 2 * round(1000 * 1.05**10, 2)); slip_is('l2-growth-factors', 9, 'gain2', 1000 + 2 * (round(1000 * 1.05**10, 2) - 1000))
ck("l2 second ten years gain 1024.41 (difference of the displayed balances; exact 1024.40)", near(1000 * 1.05**20 - 1000 * 1.05**10, 1024.41, 0.01))
ck('l2 trap 34.87', near(100 * 0.9**10, 34.87, 0.005)); ck('l2 penny', 100 * 0.1**10 < 0.01)
key_is('l2-growth-factors', 'q-car', 20000 * 0.85**2)
key_is('l3-strange-powers', 9, 1.21**0.5); slip_is('l3-strange-powers', 9, 'halved', 1.105); ck('l3 1.105^2', near(1.105**2, 1.221, 0.0005))
ck('l3 27^(2/3)', near(27**(2/3), 9, 1e-9) and 9**3 == 27**2)
ck('l3 quiz: a negative power of a NEGATIVE number below 1 is not above 1 (note for FINDING 7)', (-2.0)**-1 < 1)
key_is('l4-exponential-curves', 5, 7); ck('l4 unwind', round(10000 * 0.9**6) == 5314 and round(10000 * 0.9**7) == 4783 and near(ln(.5) / ln(.9), 6.6, 0.05))
ck('l4 trap crossing between 9 and 10', 2**9 < 900 and 2**10 > 1000)
ck('l4 0.8 half-life a little over 3', 3 < ln(.5) / ln(.8) < 3.2 and near(0.8**3, 0.512, 1e-12))
key_is('l4-exponential-curves', 9, 10000 * 1.01**60); slip_is('l4-exponential-curves', 9, 'yearly', 10000 * 1.12**5)
ck('l4 ten-year lead over 11,000', 10000 * 1.01**120 - 22000 > 11000)
ck('l4 rule of 72 at 8%', near(1.08**9, 1.999, 0.0005)); key_is('l4-exponential-curves', 10, 1000 * 1.06**12); ck('l4 simple 16.7', near(100 / 6, 16.7, 0.05))
ck('l4 q-eventually first x with 1.01^x > 1000x is 1424', min(x for x in range(2, 5000) if 1.01**x > 1000 * x) == 1424)
key_is('review-1', 'r-savings', 5000 * 1.04**3 - 5000); slip_is('review-1', 'r-savings', 'two', 5000 * 1.04**2 - 5000)
key_is('review-1', 'r-losing-strategy', min(k for k in range(1, 99) if 0.98**k < 0.5)); ck('r1 0.98', near(0.98**34, .503, 5e-4) and near(0.98**35, .493, 5e-4))
key_is('review-1', 'r-years-ago', 27 / 1.5**3); slip_is('review-1', 'r-years-ago', 'forward', 27 * 1.5**3)
key_is('review-1', 'r-three-fifths', 32**0.6, 1e-9)
key_is('homework-1', 'h-rule-72-check', 1.09**8); key_is('homework-1', 'h-monthly-rate', 1.1268**(1/12) - 1)
key_is('homework-1', 'h-unwind-twenty', min(k for k in range(1, 99) if 0.8**k < 0.5))
A = lambda m: 10000 * 1.01**m
key_is('homework-1', 'h-overtake', min(m for m in range(1, 999) if A(m) > 10000 + 150 * m))
ck('hw1 overtake figures', near(A(78), 21730.37, .005) and near(A(77), 21515.22, .005) and near(10000 + 150 * 41 - A(41), 1112.48, .005))
ck('hw1 balance passes 15,000 at month 41', min(m for m in range(1, 999) if A(m) > 15000) == 41)
ck('hw1 longform', near(5000 * 1.05**10, 8144.47, .005) and near(5000 * 1.05**20, 13266.49, .005) and near(5000 * 1.05**14, 9899.66, .005) and near(5000 * 1.05**15, 10394.64, .005))
key_is('problems-1', 'p-yeast-culture', 3000 * 2**0.5, part=2); slip_is('problems-1', 'p-yeast-culture', 'base-times', 6000**0.5, part=2)
key_is('problems-1', 'p-laptop-value', 1200 * 0.75**4, part=2); key_is('problems-1', 'p-laptop-value', 1 - 0.75**4, part=3); slip_is('problems-1', 'p-laptop-value', 'one-short', 1 - 0.75**3, part=3)
key_is('problems-1', 'p-rare-coin', 3936.60 / 1600, part=0); key_is('problems-1', 'p-rare-coin', 2.460375**(1/3), part=1)
key_is('problems-1', 'p-rare-coin', 1600 * 1.35**1.5, part=3); slip_is('problems-1', 'p-rare-coin', 'carried', 1600 * 1.486792**1.5, part=3); slip_is('problems-1', 'p-rare-coin', 'forward', 3936.60 * 1.35**1.5, part=3)
key_is('problems-1', 'p-curve-point', ln(2048) / ln(4), part=2)

# ---------- Level 2 ----------
ck('l5 logs', near(log2(100), 6.64, .005) and near(log2(5000), 12.29, .005) and near(log2(50), 5.64, .005) and near(1000 / 64, 15.63, .0051) and near(1000 / 128, 7.81, .005))
ck('l5 summary note: with base 1/2 a number below 1 has a POSITIVE log (note for FINDING 6)', ln(1 / 8) / ln(1 / 2) > 0)
key_is('l5-how-many-doublings', 9, min(k for k in range(99) if 1000 / 2**k < 10))
key_is('l6-products-into-sums', 5, log2(12)); key_is('l6-products-into-sums', 10, log2(1.5 * .8 * 1.25))
slip_is('l6-products-into-sums', 10, 'mult-logs', 0.5850 * -0.3219 * 0.3219); slip_is('l6-products-into-sums', 10, 'sign', 0.5850 + 2 * 0.3219)
key_is('l6-products-into-sums', 'q-log2-40', log2(40))
ck('l7 ruler', near(10**.11, 1.29, .005) and near(10**.2, 1.58, .005) and near(10**.5, 3.16, .005) and near(10**-.5, .32, .005) and near(log10(2), .301, 5e-4))
key_is('l7-changing-base', 5, log2(1e6)); key_is('l7-changing-base', 9, 12 * 25 / 20); ck('l7 log5 200', near(ln(200) / ln(5), 3.29, .005))
key_is('l7-changing-base', 'q-log2-3', log2(3)); slip_is('l7-changing-base', 'q-log2-3', 'quot', log10(1.5))
ck('l8 table', near(500 * 1.1**4, 732.05, .005) and near(500 * 1.1**5, 805.26, .0051) and near(500 * 1.1**4.9, 798, .5))
key_is('l8-solving-for-the-power', 2, ln(1.6) / ln(1.1)); key_is('l8-solving-for-the-power', 3, ln(50) / ln(3)); slip_is('l8-solving-for-the-power', 3, 'log-quot', log10(50 / 3))
ck('l8 manipulate', near(ln(1.5) / ln(1.05), 8.31, .005) and near(1.5 / 1.05, 1.4286, 5e-5))
ck('l8 trap options', near(ln(800) / ln(550), 1.06, .005) and near(ln(800) / ln(1.1), 70.14, .005))
key_is('l8-solving-for-the-power', 9, ln(2) / ln(1.07)); ck('l8 balances', near(1000 * 1.07**10, 1967.15, .005) and near(1000 * 1.07**11, 2104.85, .005))
key_is('l8-solving-for-the-power', 'q-coefficient', ln(202.5 / 40) / ln(1.5)); slip_is('l8-solving-for-the-power', 'q-coefficient', 'merge', ln(202.5) / ln(60))
key_is('l8-solving-for-the-power', 'q-halvings', min(k for k in range(99) if 2500 / 2**k < 10)); key_is('l8-solving-for-the-power', 'q-decay', ln(.5) / ln(.8))
key_is('review-2', 'r-change-base', ln(20) / ln(4)); key_is('review-2', 'r-solve', ln(3) / ln(1.2))
key_is('review-2', 'r-fund-target', min(k for k in range(99) if 5000 * 1.06**k > 8000)); ck('r2 fund', near(5000 * 1.06**8, 7969.24, .005) and near(5000 * 1.06**9, 8447.39, .005))
key_is('review-2', 'r-decibel', 10**((63 - 43) / 10)); ck('r2 colony', near(ln(200) / ln(3), 4.82, .005))
key_is('homework-2', 'h-drawdown', min(k for k in range(99) if 12000 * .85**k < 3000)); ck('hw2 drawdown', near(12000 * .85**8, 3269.89, .005) and near(ln(.25) / ln(.85), 8.53, .005))
B = lambda k: (400 * 1.09**k, 1000 * 1.03**k)
key_is('homework-2', 'h-overtake', min(k for k in range(99) if B(k)[0] > B(k)[1]))
ck('hw2 overtake figures', near(B(16)[0], 1588.12, .005) and near(B(16)[1], 1604.71, .005) and near(B(17)[0], 1731.05, .005) and near(B(17)[1], 1652.85, .005) and near(ln(2.5) / ln(1.09 / 1.03), 16.18, .005))
ck('hw2 longform 14%', near(ln(2) / ln(1.14), 5.29, .005) and near(ln(2) / ln(1.07) / 2, 5.12, .005) and 1.07**2 > 1.14)
ck('p2 fault search', 2**11 == 2048 and math.ceil(log2(32 * 2048)) == 16 and math.ceil(log2(5 * 65536)) == 19)
key_is('problems-2', 'p-forty-doublings', 10**(40 * log10(2) - 12), part=2); key_is('problems-2', 'p-forty-doublings', min(k for k in range(99) if 2**(40 + k) > 10**16), part=3)
key_is('problems-2', 'p-drawdown-recovery', ln(1.5625) / ln(1.11), part=2); ck('p2 recovery', near(32000 * 1.11**4, 48578, .5) and near(32000 * 1.11**5, 53922, .5))
key_is('problems-2', 'p-app-users', ln(25) / ln(1.3), part=2); ck('p2 users', round(2000 * 1.3**12) == 46596 and round(2000 * 1.3**13) == 60575)
slip_is('problems-2', 'p-app-users', 'joined', ln(50000) / ln(2600), part=2); slip_is('problems-2', 'p-app-users', 'rate-only', ln(25) / ln(.3), part=2)

# ---------- Level 3 ----------
f = lambda k: (1 + 1 / k)**k
ck('l9 e as a limit: increasing and below e', all(f(k) < f(k + 1) < math.e for k in range(1, 5000)))
ck('l9 table', near(f(4), 2.4414, 5e-5) and near(f(12), 2.6130, 5e-5) and near(f(365), 2.7146, 5e-5) and near(f(10**6), 2.7183, 5e-5) and near(1.0833**12, 2.6121, 5e-5) and near(f(1000), 2.71692, 5e-6))
ck('l9 n = 52 text 2.69', round(f(52), 2) == 2.69)
P52 = [p for p in L('l9-compounding-more-often')['screens'][2]['explain']['canvas']['points'] if p['id'] == 'P'][0]['y']
ck(f'l9 screens[2].explain.canvas P.y {P52} is not (1+1/52)^52 = {f(52):.4f}  [FINDING 1]', near(P52, f(52), 5e-5))
ck('l9 10%', near(100 * (1 + .1 / 12)**12, 110.47, .005) and near(100 * (1 + .1 / 365)**365, 110.52, .005) and near(100 * exp(.1), 110.52, .005))
key_is('l9-compounding-more-often', 5, 1000 * exp(.5)); ck('l9 bars', near(1000 * (1 + .05 / 12)**120, 1647.01, .005) and near(1000 * (1 + .05 / 365)**3650, 1648.66, .005))
ck('l9 trap', near(10000 * exp(.06), 10618.37, .005) and near(10620 - 10000 * exp(.06), 1.63, .005))
key_is('l9-compounding-more-often', 9, exp(.05) - 1); ck('l9 interest on two million', near(2e6 * (exp(.05) - 1), 102542.19, .005))
key_is('l9-compounding-more-often', 'q-continuous-three', 2500 * exp(.12)); key_is('l9-compounding-more-often', 'q-negative-rate', 5000 * exp(-.01))
ck('l9 quarterly', 1.02**4 > exp(.079) > 1.08 and near(1.02**4, 1.08243, 5e-6) and near(exp(.079), 1.08220, 5e-6))
ck('l10 values', near(ln(5), 1.609, 5e-4) and near(1.5 / math.e, .5518, 5e-5) and near(ln(1500) / 40, .18, .005) and near(ln(1.5) / .04, 10.14, .005) and near(exp(3), 20.1, .05))
ck('l10 e^1.0986 is 3 only to 4 dp (note for FINDING 5)', abs(exp(1.0986) - 3) < 1e-4 and exp(1.0986) != 3)
key_is('l10-natural-log', 10, ln(100 / 92.31) / 2); slip_is('l10-natural-log', 10, 'yearly', (100 / 92.31)**.5 - 1); slip_is('l10-natural-log', 10, 'simple', (100 / 92.31 - 1) / 2)
key_is('l10-natural-log', 'q-solve-twenty', ln(20)); key_is('l10-natural-log', 'q-reach-ten-thousand', ln(2.5) / .06); slip_is('l10-natural-log', 'q-reach-ten-thousand', 'ln-gain', ln(6000) / .06)
ck('l11 explore', near(ln(1.21), .1906, 5e-5) and near(.4 + 121 / 140 - 1, .2643, 5e-5) and near(-.2 + 121 / 80 - 1, .3125, 5e-5) and near(ln(1.4), .3365, 5e-5) and near(ln(121 / 140), -.1459, 5e-5))
ck('l11 simple sum equals 21% only at 100 or 121', sorted(b for b in range(60, 200) if abs(b / 100 + 121 / b - 2.21) < 1e-12) == [100, 121])
key_is('l11-log-returns', 3, ln(1.05)); key_is('l11-log-returns', 4, ln(83.1 / 80)); key_is('l11-log-returns', 5, exp(.08) - 1)
px = [80.0, 81.2, 79.9, 82.3, 83.1]; lr = [round(ln(b / a), 4) for a, b in zip(px, px[1:])]
ck('l11 daily log returns', lr == [0.0149, -0.0161, 0.0296, 0.0097] and near(sum(lr), .0381, 1e-9))
ck('l11 ln(1+r) < r for r != 0, r > -1', all(ln(1 + r) < r for r in np.linspace(-.99, 5, 600) if abs(r) > 1e-9))
ck('l11 trap', near(ln(1.5), .4055, 5e-5) and near(log10(1.5), .1761, 5e-5) and near(ln(1.01), .00995, 5e-6) and near(exp(-.03), .9704, 5e-5))
key_is('l11-log-returns', 10, 1e6 * exp(sum([0.0124, -0.0131, 0.0222, 0.0136, -0.0106])))
key_is('l11-log-returns', 'q-up-down-twenty', ln(.96)); key_is('l11-log-returns', 'q-year-log', exp(.25) - 1); key_is('l11-log-returns', 'q-small-fall', ln(.95))
key_is('l12-doubling-time', 3, ln(2) / .05); key_is('l12-doubling-time', 4, ln(2) / .03); key_is('l12-doubling-time', 9, ln(2) / .15)
rows = W('l12-doubling-time', 5)['rows']
for row, r in zip(rows, (.02, .08, .24)):
    ck(f'l12 exact T at {r}', near(row[2]['answer'], ln(2) / ln(1 + r), 0.005))
err = lambda x: 72 / x - ln(2) / ln(1 + x / 100)
ck('l12 rule of 72 error: sign change near 8%, +1.0 at 2%, negative at 24%', err(7.5) > 0 > err(8.5) and near(err(2), .9972, 5e-5) and near(err(8), -.0065, 5e-5) and near(err(24), -.2223, 5e-5))
key_is('l12-doubling-time', 'q-rate-from-doubling', ln(2) / 12); key_is('l12-doubling-time', 'q-one-percent', ln(2) / ln(1.01))
ck('l13 15%', near(1.15**5, 2.01, .005) and near(10 * 1.15**15, 81.37, .005) and near(10 * 1.15**20, 163.67, .005) and near(ln(1.15**5), .70, .005))
key_is('l13-log-scale', 5, 100 * 2**.5); key_is('l13-log-scale', 9, ln(4) / 10); slip_is('l13-log-scale', 9, 'yearly', 4**.1 - 1); slip_is('l13-log-scale', 9, 'log10', log10(4) / 10)
t6 = W('l13-log-scale', 6); ck('l13 trap target', near(t6['points'][0]['target'][1], ln(300), 5e-5) and near(ln(1.5) / ln(2), .58, .005) and near(exp((ln(200) + ln(400)) / 2), 282.84, .005))
key_is('l13-log-scale', 'q-halfway-ten', 10**1.5); key_is('l13-log-scale', 'q-slope-rate', ln(4) / 4)
key_is('review-3', 'r-continuous-eight', 6000 * exp(.28) - 6000 * 1.035**8); key_is('review-3', 'r-solve-three-x', ln(40) / 3); key_is('review-3', 'r-log-path', ln(1.25))
key_is('review-3', 'r-signal-half-life', ln(2) / .2); key_is('review-3', 'r-log-midpoint', 20 * 16**.25); key_is('review-3', 'r-crash-log', ln(.6)); key_is('review-3', 'r-fund-rate', ln(1.64) / 6)
slip_is('review-3', 'r-fund-rate', 'yearly', 1.64**(1/6) - 1); ck('r3 quote', exp(.05) > 1.051)
key_is('homework-3', 'h-bond-yield', 1000 * exp(-.21)); slip_is('homework-3', 'h-bond-yield', 'yearly', 1000 / 1.042**5)
key_is('homework-3', 'h-eight-days', 45 * exp(.025)); ck('hw3 eight days sum', near(sum([0.012, -0.004, 0.009, -0.015, 0.006, 0.011, -0.002, 0.008]), .025, 1e-12))
key_is('homework-3', 'h-annual-vol', .012 * 252**.5); slip_is('homework-3', 'h-annual-vol', 'compound', 1.012**252 - 1)
key_is('homework-3', 'h-unwind-rate', ln(2) / 3); key_is('homework-3', 'h-crash-month', ln(.91)); key_is('homework-3', 'h-log-read', 100 * 10**.3)
ya, yb = ln(100 / 88) / 3, ln(1.043)
key_is('homework-3', 'h-two-bonds', (ya - yb) * 1e4); slip_is('homework-3', 'h-two-bonds', 'yearly', ((100 / 88)**(1/3) - 1.043) * 1e4)
r6 = [.12, -.08, .05, -.10, .15, .02]; s6 = sum(ln(1 + r) for r in r6)
ck('hw3 longform', near(s6, .13294, 5e-6) and near(exp(s6) - 1, .1422, 5e-5) and near(np.prod([1 + r for r in r6]), 1.1422, 5e-5) and near(ln(2) / (s6 / 6), 31.28, .005) and near(2 * s6, .2659, 5e-5) and near(exp(2 * s6) - 1, .3046, 5e-5))
ck('hw3 unwind: one day at k = ln2/3 sells 20.6% of the holding, not 23.1% (note for FINDING 4)', near(1 - exp(-ln(2) / 3), .2063, 5e-5))
key_is('problems-3', 'p-savings-doubling', ln(2) / .055, part=1); key_is('problems-3', 'p-savings-doubling', 3 * ln(2) / .055, part=2); key_is('problems-3', 'p-savings-doubling', 2400 * 2**1.5, part=3)
key_is('problems-3', 'p-weekly-target', 40 * exp(.043), part=1); key_is('problems-3', 'p-weekly-target', ln(45 / 41.76), part=2); key_is('problems-3', 'p-weekly-target', exp(.0249) - 1, part=4)
key_is('problems-3', 'p-log-chart-line', ln(9) / 8, part=0); key_is('problems-3', 'p-log-chart-line', ln(2) / (ln(9) / 8), part=1); key_is('problems-3', 'p-log-chart-line', (15 * 135)**.5, part=2); key_is('problems-3', 'p-log-chart-line', 12 * ln(3) / ln(9), part=3)
key_is('problems-3', 'p-monthly-deposit', 1.004**12, part=0); key_is('problems-3', 'p-monthly-deposit', 12 * ln(1.004), part=1); key_is('problems-3', 'p-monthly-deposit', 60 * ln(1.004), part=2); key_is('problems-3', 'p-monthly-deposit', 6000 * 1.004**60, part=3)

# ---------- Monte Carlo: sd of a sum of 252 independent daily log returns (homework-3 h-annual-vol) ----------
rng = np.random.default_rng(20261126)
for name, draw in (('normal', lambda s: rng.normal(0, .012, s)), ('fat-tailed t5', lambda s: rng.standard_t(5, s) * .012 / math.sqrt(5 / 3))):
    ann = draw((40000, 252)).sum(axis=1)
    sd = ann.std(ddof=1)            # standard error about 0.19 / sqrt(2 * 40000) = 0.0007 (wider for t5)
    ck(f'MC {name}: annual sd {sd:.4f} is 0.012*sqrt(252) = 0.1905, not 0.012*252 = 3.024', abs(sd - .012 * 252**.5) < 0.004 and abs(sd - 3.024) > 2)
x = rng.normal(0, .012, (40000, 252))
simple_sum, true_simple = (np.exp(x) - 1).sum(axis=1), np.exp(x.sum(axis=1)) - 1
ck('MC: daily simple returns do not sum to the yearly simple return, daily log returns do', np.abs(simple_sum - true_simple).mean() > 0.005)

# ---------- fluency: every family over its whole range ----------
counts = {}
def sweep(label, combos, body):
    c = 0
    for v in combos:
        r = body(*v)
        if r is None: continue
        c += 1
        ck(f'fluency {label} {v}', r)
    ck(f'fluency {label} has draws', c > 0)
    counts[label] = c
rel = lambda a, b, t=.002: abs(a - b) <= t * abs(b)
sweep('negative-power', itertools.product(range(2, 31), (1, 2, 3)),
      lambda a, m: None if a**m > 1000 else (not rel(a**m, Fraction(1, a**m)) and not rel(-a * m, Fraction(1, a**m))))
def fp(r, m_, k, g):
    if math.gcd(k, m_) != 1: return None
    a, key, times, flip = r**m_, Fraction(r)**(g * k), Fraction(r**m_ * g * k, m_), Fraction(r)**(-g * k)
    if times == key: return None
    return near(float(a)**(g * k / m_), float(key), 1e-9 * max(1, float(key))) and not rel(times, key) and not rel(flip, key) and not rel(times, flip)
sweep('fractional-power', itertools.product(range(2, 11), (2, 3), (1, 2, 3), (1, -1)), fp)
def lte(a, m, k_, kk):
    if m in (0, 1) or k_ in (0, 1): return None
    p = m + k_ - kk
    if p in (0, 1) or abs(p) > 9 or a**(-kk) > 125 or m * k_ == m + k_ or m + k_ + p == m * k_ - p or abs(m * k_ - p) > 40 or abs(m + k_ + p) > 40: return None
    key = Fraction(a)**m * Fraction(a)**k_ / Fraction(a)**p
    return key == Fraction(a)**kk and not rel(Fraction(a)**(m + k_ + p), key) and not rel(Fraction(a)**(m * k_ - p), key)
sweep('laws-then-evaluate', itertools.product(range(2, 6), range(-4, 8), range(-4, 8), range(-3, 1)), lte)
def pop(m, k_, p):
    if 0 in (m, k_, p) or 1 in (m, k_, p) or m + k_ == m * k_ or m * k_ == 1 or m + k_ - p == m * k_ + p: return None
    key = m * k_ - p            # (v^m)^n / v^p = v^(mn - p)
    return key != m + k_ - p and key != m * k_ + p
sweep('power-of-a-power', itertools.product(range(-5, 7), range(-3, 5), range(-6, 7)), pop)
def cs(b, k, h, d):
    if b**k > 1000: return None
    u = 2 + b % 2; w = b // u; i = h % (k + 1); j = (i + 1 + d % k) % (k + 1)
    x, y = u**i * w**j, u**(k - i) * w**(k - j)
    ofsum, times = ln(x + y) / ln(b), ln(x) * ln(y) / ln(b)**2
    if not (abs(ofsum - k) > .05 and abs(times - k) > .05 and abs(ofsum - times) > .05): return None
    return u * w == b and x > 1 and y > 1 and x * y == b**k and near(log10(x) / log10(b) + log10(y) / log10(b), k, 1e-9)
sweep('combine-a-sum', itertools.product([6, 10, 14, 15, 21, 22, 26], (1, 2, 3), range(4), (1, 2, 3)), cs)
def cd(b, c, k):
    top = c * b**k
    if c in (b, b**2, b**3) or top > 1000: return None
    div, ins = ln(top) / ln(c), ln(top - c) / ln(b)
    if not (abs(div - k) > .05 and abs(ins - k) > .05 and abs(div - ins) > .05): return None
    return near(ln(top) / ln(b) - ln(c) / ln(b), k, 1e-9)
sweep('combine-a-difference', itertools.product((2, 3, 5, 10), range(2, 13), (1, 2, 3)), cd)
def ep(a, b):
    r = ln(b) / ln(a)
    if not (abs(r - round(r)) > .001 and b > a and abs(b / a - r) > .01): return None
    return near(a**r, b, 1e-9 * b) and abs(1 / r - r) > .01
sweep('exact-power', itertools.product(range(2, 10), range(3, 100)), ep)
def p3(a, b):
    r = ln(b) / ln(a); e = math.floor(log10(r)) - 2; m = r / 10**e
    if not (abs(m - round(m)) > .01 and abs(b / a - r) > .02 and abs(1 / r - r) > .02): return None
    tol = .51 * 10**e
    return near(a**r, b, 1e-9 * b) and abs(1 / r - r) > 2 * tol and abs(b / a - r) > 2 * tol and abs(float(f'{r:.3g}') - r) <= tol
sweep('power-to-3-sf', itertools.product([1.5, 2, 2.5, 3, 4, 5, 6, 7], range(3, 201)), p3)
def paf(c, a, k):
    d = c * a**k; joined = ln(d) / ln(c * a)
    if a**k > 625 or c == a or abs(joined - k) <= .05: return None
    return a**k != k and near(ln(d / c) / ln(a), k, 1e-9)
sweep('power-alone-first', itertools.product(range(2, 10), range(2, 6), range(2, 7)), paf)
dropped = []
def mt(p, g, q):
    t = p * q; r = ln(q) / ln(g); joined = ln(t) / ln(p * g); early = ln(t) / ln(g); e = math.floor(log10(r)) - 2; m = r / 10**e
    if not (abs(m - round(m)) > .01 and abs(joined - r) > .2): return None
    tol = .51 * 10**e
    # logs taken first, done correctly, give the key; the slip value is what dropping p gives (FINDING 2)
    dropped.append(near((ln(t) - ln(p)) / ln(g), r, 1e-9) and near(g**early, t, 1e-6 * t) and not near(p * g**early, t, 1))
    return near(p * g**r, t, 1e-9 * t) and abs(joined - r) > 2 * tol and abs(early - r) > 2 * tol
sweep('money-target', itertools.product(range(100, 901, 100), [1.02, 1.03, 1.04, 1.05, 1.06, 1.08], [1.5, 2, 2.5, 3, 4]), mt)
ck('note FINDING 2: in every money-target draw, logs-first gives the key and the slip value solves g^v = t', all(dropped))
def el(k, b):
    if b == k or abs(ln(b / k) - ln(b) / k) <= .01 or abs(ln(b / k) - k * ln(b)) <= .01: return None
    return near(exp(k * ln(b) / k), b, 1e-9 * b) and abs(k * ln(b) - ln(b) / k) > .01
sweep('exact-with-ln', itertools.product(range(2, 10), range(2, 41)), el)
def cg(p, r, q):
    years = ln(q) / (r / 100)
    if years >= 100: return None
    return near(p * exp(r / 100 * years), p * q, 1e-9 * p * q) and abs(ln(p * q) / (r / 100) - years) > .012 and abs(ln(q) / r - years) > .012
sweep('continuous-growth', itertools.product([200, 500, 800, 1000, 2000, 4000, 5000], range(1, 10), [1.5, 2, 2.5, 3, 4]), cg)
def l2v(f_, g, i, j):
    if 0 in (i, j) or not f_ < g or max(abs(i), abs(j)) < 2 or i == j: return None
    x = Fraction(f_)**i * Fraction(g)**j
    lf, lg = round(ln(f_), 4), round(ln(g), 4)
    sg = lambda z: (z > 0) - (z < 0)
    flat, sw, key = sg(i) * lf + sg(j) * lg, i * lg + j * lf, i * lf + j * lg
    if x > 200 or x < Fraction(1, 50) or flat == sw: return None
    return near(round(ln(x), 4), key, .0005) and abs(flat - key) > .001 and abs(sw - key) > .001
sweep('ln-from-two-values', itertools.product((2, 3), (3, 5, 7), range(-3, 5), range(-2, 4)), l2v)
def abe(b):
    lb = ln(b)
    if abs(lb / ln(10) - lb) <= .001 or abs(1 / lb - lb) <= .001: return None
    return near(exp(lb), b, 1e-9 * b) and abs(lb / ln(10) - lb) > .0002 and abs(1 / lb - lb) > .0002
sweep('any-base-as-e', [(b,) for b in range(2, 61)], abe)

print(f'{n} checks, {len(fails)} failing; fluency draws swept:', counts)
for x in fails: print('FAIL', x)
sys.exit(1 if fails else 0)
