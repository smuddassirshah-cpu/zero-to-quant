#!/usr/bin/env python3
"""Concept audit, integrals levels 1 to 3, round 3 (blind read at commit 73990629).

Recomputes, independently of the authored figures:
  A. every numeric key and every numeric slip (wrong[].value) of lessons l1 to l13, review-1..3, homework-1..3 and problems-1..3,
     each slip from the mistake its feedback line names;
  B. every decimal an `accept` line prints as the answer (it must be accepted by the widget's own tolerance), and the `x +- t` bands;
  C. the figures printed in prose, hints, feedback and explain lines that are not a key or a slip;
  D. the empirical and statistical claims, by Monte Carlo or by running the method (seeded; replications sized so that the claim
     and its negation are many standard errors apart);
  E. the fluency families (l6, l7, l9, l10): 60 seeded draws a family through tools/fluency-sample.mjs, each answer rederived from
     the prompt the learner sees, each wrong form shown wrong (needs node; skipped with a notice when node is missing);
  F. the hidden tests of the three Python code widgets, run in CPython on the authored solution.

Exit 0 when every check passes. A check that fails because the content is wrong stays failing and is a finding.
Checks tagged KNOWN are the findings of this audit (docs/reviews/audit-integrals-1-3-r3.md, findings 1 to 4). They fail the run
(exit 1) until the content is fixed. Pass --allow-known to count them apart and exit 0 when nothing else fails, which makes the
script a regression guard for everything else.
Fix pass: findings 1 to 4 are fixed in the content, so the KNOWN checks pass without --allow-known. No check was re-pointed;
section B gains one check that a "within t of" accept line states the widget's own absolute tolerance.

Python: NumPy, SciPy and SymPy (venv versions newer than CI's pins; no figure here depends on the version).
"""
import json, math, os, re, shutil, subprocess, sys
from math import e, exp, log, pi, sqrt, sin, cos, ceil
import numpy as np
from scipy import integrate, optimize, stats

import warnings
warnings.filterwarnings('ignore', category=integrate.IntegrationWarning)

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CDIR = os.path.join(ROOT, 'app', 'content', 'courses', 'integrals')
ALLOW_KNOWN = '--allow-known' in sys.argv
FAILS, KNOWN, N = [], [], [0]


def check(ok, label, known=False):
    N[0] += 1
    if not ok:
        (KNOWN if known else FAILS).append(label)
        print(('KNOWN ' if known else 'FAIL  ') + label)


def close(a, b, tol):
    return abs(a - b) <= tol + 1e-12


def load(name):
    with open(os.path.join(CDIR, name + '.json'), encoding='utf8') as fh:
        return json.load(fh)


FILES = {}
for _n in sorted(os.listdir(CDIR)):
    if re.match(r'l([1-9]|1[0-3])-', _n) or re.match(r'(review|homework|problems)-[123]\.json', _n):
        FILES[_n[:-5]] = load(_n[:-5])


def short(name):
    return name.split('-')[0] if name[0] == 'l' else name


def numeric_widgets():
    """(key, widget) for every numeric widget; key like 'l7 S[9]' or 'problems-2 I[1]P[2]'."""
    out = []

    def walk(o, p):
        if isinstance(o, dict):
            if o.get('kind') == 'numeric' and ('answer' in o or 'answers' in o):
                out.append((p, o))
            for k, v in o.items():
                walk(v, p + '.' + k)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, p + '[%d]' % i)

    res = []
    for name, d in FILES.items():
        out.clear()
        walk(d, '')
        for p, o in out:
            p = p.replace('.screens', 'S').replace('.items', 'I').replace('.quiz', 'Q').replace('.parts', 'P').replace('.widget', '')
            res.append((short(name) + ' ' + p, o))
    return res


def tol_of(w, value=None):
    t = w.get('tol') or {}
    if 'rel' in t:
        return abs(t['rel'] * (value if value is not None else w['answer']))
    return t.get('abs', 0)


# ---------- helpers ----------
def Lsum(f, a, b, n):
    h = (b - a) / n
    return h * sum(f(a + i * h) for i in range(n))


def Rsum(f, a, b, n):
    h = (b - a) / n
    return h * sum(f(a + (i + 1) * h) for i in range(n))


def Msum(f, a, b, n):
    h = (b - a) / n
    return h * sum(f(a + (i + 0.5) * h) for i in range(n))


def Trap(f, a, b, n):
    h = (b - a) / n
    return h * (f(a) / 2 + sum(f(a + i * h) for i in range(1, n)) + f(b) / 2)


def Int(f, a, b, **kw):
    return integrate.quad(f, a, b, epsabs=1e-13, epsrel=1e-13, limit=200, **kw)[0]


sq = lambda x: x * x
cube = lambda x: x ** 3
recip = lambda x: 1 / x
phi = lambda x: exp(-x * x / 2) / sqrt(2 * pi)
A5 = lambda x: 2 * x * x - x ** 3 / 3          # l5: area under t(4 - t) from 0
PV = lambda c, r, T: c * (1 - exp(-r * T)) / r
tri = lambda x: (10 - abs(x - 100)) / 100      # triangular density on [90, 110]
sig = lambda t: t * exp(-t * t / 8)            # problems-3 item 4
bars_hw1 = [2400, 1600, 1200, 1000, 900, 1100, 1500, 2800]
mid_heights = [0.3958, 0.3719, 0.3282, 0.2721]  # l1 screen 10, as printed

# ---------- A. keys and slips, each from the named mistake ----------
EXP = {
    # level 1 lessons
    'l1 S[1]': dict(ans=next(n for n in range(1, 50) if Rsum(sq, 0, 1, n) < 0.4), seven=7, nine=9, one=1),
    'l1 S[2]': dict(ans=Rsum(sq, 0, 1, 4), **{'no-width': 4 * Rsum(sq, 0, 1, 4), 'left': Lsum(sq, 0, 1, 4), 'guess': 1 / 3}),
    'l1 S[3]': dict(ans=Lsum(sq, 0, 1, 4), **{'right-ends': Rsum(sq, 0, 1, 4), 'no-width': 4 * Lsum(sq, 0, 1, 4), 'three': 4 * Lsum(sq, 0, 1, 4) / 3}),
    'l1 S[4]': dict(ans=Msum(sq, 0, 1, 4), **{'average-sums': (Lsum(sq, 0, 1, 4) + Rsum(sq, 0, 1, 4)) / 2, 'no-square': 0.25 * (1 / 8 + 3 / 8 + 5 / 8 + 7 / 8), 'no-width': 4 * Msum(sq, 0, 1, 4)}),
    'l1 S[6]': dict(ans=Lsum(sq, 1, 2, 4), **{'wrong-end': Rsum(sq, 1, 2, 4), 'old-points': Lsum(sq, 0, 1, 4), 'five': Lsum(sq, 1, 2, 4) + 0.25 * 4, 'no-width': 4 * Lsum(sq, 1, 2, 4)}),
    'l1 S[9]': dict(ans=0.25 * sum(mid_heights), **{'no-width': sum(mid_heights), 'percent': 25 * sum(mid_heights), 'one-height': mid_heights[0]}),
    'l1 Q[0]': dict(ans=Rsum(lambda x: 2 * x + 1, 0, 2, 4), **{'left': Lsum(lambda x: 2 * x + 1, 0, 2, 4), 'no-width': 2 * Rsum(lambda x: 2 * x + 1, 0, 2, 4), 'exact': Int(lambda x: 2 * x + 1, 0, 2)}),
    'l1 Q[2]': dict(ans=Msum(cube, 0, 2, 2), **{'average': (Lsum(cube, 0, 2, 2) + Rsum(cube, 0, 2, 2)) / 2, 'no-cube': 0.5 + 1.5, 'left': Lsum(cube, 0, 2, 2)}),
    'l2 S[0]': dict(ans=next(n for n in range(1, 100) if 1 / n <= 0.05 + 1e-15), nineteen=19, twentyone=21, ten=10),
    'l2 S[2]': dict(ans=Rsum(sq, 1, 3, 10) - Lsum(sq, 1, 3, 10), **{'no-height': 0.2, 'no-width': 9 - 1, 'unit-width': (9 - 1) / 10}),
    'l2 S[4]': dict(ans=Rsum(sq, 0, 1, 100), **{'limit': 1 / 3, 'left': Lsum(sq, 0, 1, 100), 'half-term': round(1 / 3 + 1 / 200, 5)}),
    'l2 S[8]': dict(ans=ceil(10 * (1 - exp(-0.5)) / 0.01), **{'round-down': math.floor(10 * (1 - exp(-0.5)) / 0.01), 'no-length': ceil((1 - exp(-0.5)) / 0.01), 'no-height': ceil(10 / 0.01 - 1e-9)}),
    'l2 Q[0]': dict(ans=Rsum(lambda x: 3 * x, 0, 2, 6) - Lsum(lambda x: 3 * x, 0, 2, 6), **{'no-height': 2 / 6, 'no-width': 6, 'unit': 6 / 6}),
    'l2 Q[1]': dict(ans=Lsum(sq, 0, 1, 10), **{'right': Rsum(sq, 0, 1, 10), 'limit': 1 / 3, 'dropped': 1 / 3 - 1 / 20}),
    'l3 S[0]': dict(ans=Msum(lambda x: x - 1, 0, 3, 6), **{'no-signs': Msum(lambda x: abs(x - 1), 0, 3, 6), 'no-width': 2 * Msum(lambda x: x - 1, 0, 3, 6), 'below-only': 0.5 * (-0.75 - 0.25)}),
    'l3 S[1]': dict(ans=optimize.brentq(lambda b: Int(lambda x: x - 1, 0, b), 0.5, 3), crossing=1, end=3),
    'l3 S[3]': dict(ans=Int(lambda x: 2 - x, 0, 5), area=Int(lambda x: abs(2 - x), 0, 5), flipped=-Int(lambda x: 2 - x, 0, 5), above=Int(lambda x: 2 - x, 0, 2), below=Int(lambda x: 2 - x, 2, 5)),
    'l3 S[4]': dict(ans=-Int(lambda x: x - 1, 0, 3), same=Int(lambda x: x - 1, 0, 3), zero=0, area=-Int(lambda x: abs(x - 1), 0, 3)),
    'l3 S[5]': dict(ans=Int(sin, 0, pi / 2), whole=Int(sin, 0, pi), box=pi / 2),
    'l3 S[6]': dict(ans=Int(lambda x: abs(sin(x)), 0, 2 * pi, points=[pi]), signed=Int(sin, 0, 2 * pi), one=2, negative=-4),
    'l3 S[9]': dict(ans=Int(lambda t: 400 - 100 * t, 0, 6), traded=Int(lambda t: abs(400 - 100 * t), 0, 6, points=[4]), stop=Int(lambda t: 400 - 100 * t, 0, 4), rate=400 - 600),
    'l3 Q[0]': dict(ans=Int(lambda x: x, -2, 2), area=Int(abs, -2, 2, points=[0]), half=2, neg=-2),
    'l3 Q[3]': dict(ans=Int(lambda x: abs(x - 1), 0, 3, points=[1]), signed=1.5, above=2, diff=-1.5),
    'l4 S[0]': dict(ans=120 + 80 + 150 + 60 + 90, average=(120 + 80 + 150 + 60 + 90) / 5, peak=150, **{'one-day': 120}),
    'l4 S[1]': dict(ans=sqrt(18), **{'half-time': 3, 'end': 6}),
    'l4 S[2]': dict(ans=Int(lambda t: 20 * t, 0, 5), rate=100, box=500, **{'half-rate': 50}),
    'l4 S[3]': dict(ans=Int(lambda t: min(2 * t, 20), 0, 30, points=[10]), **{'top-speed': 600, 'triangle': 0.5 * 30 * 20, 'cruise': 400}),
    'l4 S[4]': dict(ans=Int(lambda t: 400 - 200 * t, 0, 3), stop=Int(lambda t: 400 - 200 * t, 0, 2), area=Int(lambda t: abs(400 - 200 * t), 0, 3, points=[2]), rate=400 - 600),
    'l4 S[8]': dict(ans=1e7 * (0.04 * 30 + 0.045 * 60) / 365, average=1e7 * 0.0425 * 90 / 365, **{'first-rate': 1e7 * 0.04 * 90 / 365, 'second-rate': 1e7 * 0.045 * 90 / 365}),
    'l4 Q[0]': dict(ans=2000 * 15 + 500 * 30, rates=2500, average=1250 * 45, first=30000),
    'l4 Q[1]': dict(ans=Int(lambda t: 3 * t, 0, 4), final=12, box=48),
    'l4 Q[2]': dict(ans=-50 * 6 + 80 * 2, area=300 + 160, rates=-50 + 80, gain=160, sign=140),
    'l4 Q[3]': dict(ans=1e6 * 0.06 * 73 / 365, year=60000, days=60000 * 73, daily=60000 / 365),
    # level 2 lessons
    'l5 S[1]': dict(ans=3 * (4 - 3), area=A5(3), fprime=4 - 2 * 3),
    'l5 S[2]': dict(ans=A5(2.25) - A5(2), height=4, width=0.25, total=A5(2.25)),
    'l5 S[3]': dict(ans=4, zero=0, area=A5(2)),
    'l5 Q[0]': dict(ans=7, area=20),
    'l5 Q[3]': dict(ans=6 - 10, level=Int(lambda t: 6 - 2 * t, 0, 5), sign=4),
    'l6 S[9]': dict(ans=2 + Int(lambda t: 3 - t / 2, 0, 4), **{'no-c': Int(lambda t: 3 - t / 2, 0, 4), 'rate': 3 - 2, 'no-divide': 12 - 16 / 2 + 2}),
    'l6 Q[2]': dict(ans=5 + Int(lambda x: 6 * x * x, 1, 2), **{'no-c': 16, 'slope': 24}),
    'l7 S[0]': dict(ans=Int(lambda x: 2 * x, 1, 3), **{'from-zero': 9, 'tall-side': 12, 'short-side': 4}),
    'l7 S[2]': dict(ans=Int(lambda x: 3 * x * x, 1, 2), **{'forgot-fa': 8, 'order': -7, 'added': 9, 'height': 12}),
    'l7 S[3]': dict(ans=Int(sin, 0, pi), **{'cos': cos(pi) - cos(0), 'cos-pi': -1 - (-1), 'forgot-fa': -cos(pi)}),
    'l7 S[5]': dict(ans=-Int(lambda x: 2 * x, 1, 3), **{'positive': 8, 'forgot-fa': 1}),
    'l7 S[7]': dict(ans=Int(sq, -1, 2), **{'forgot-fa': 8 / 3, 'sign-slip': 8 / 3 - 1 / 3, 'order': -3}),
    'l7 S[9]': dict(ans=PV(10000, 0.04, 5), **{'undiscounted': 50000, 'forgot-fa': -250000 * exp(-0.2), 'order': -PV(10000, 0.04, 5), 'end-discount': 50000 * exp(-0.2)}),
    'l7 S[10]': dict(ans=Int(lambda s: max(s - 100, 0) / 20, 90, 110, points=[100]), **{'given-pays': 5, 'best': 10, 'at-mean': 0}),
    'l7 Q[0]': dict(ans=Int(exp, 0, 2), **{'forgot-fa': e ** 2}),
    'l7 Q[1]': dict(ans=-Int(lambda x: 3 * x * x, 0, 2), positive=8),
    'l7 Q[3]': dict(ans=PV(2000, 0.05, 10), **{'undiscounted': 20000, 'end-discount': 20000 * exp(-0.5)}),
    'l8 S[2]': dict(ans=Int(lambda x: x + 2 - x * x, -1, 2), **{'under-line': Int(lambda x: x + 2, -1, 2), 'upside': -4.5, 'under-para': Int(sq, -1, 2)}),
    'l8 S[4]': dict(ans=Int(lambda x: 8 - 2 * x * x, -2, 2), **{'cancel': Int(lambda x: 4 - x * x, -2, 2) + Int(lambda x: x * x - 4, -2, 2), 'top-only': Int(lambda x: 4 - x * x, -2, 2)}),
    'l8 S[5]': dict(ans=Int(lambda x: abs(x - x ** 3), -1, 1, points=[0]), **{'cancelled': Int(lambda x: x - x ** 3, -1, 1), 'one-piece': Int(lambda x: x - x ** 3, 0, 1)}),
    'l8 S[8]': dict(ans=Int(lambda t: 10 - 2 * t, 0, 12), **{'total-area': Int(lambda t: abs(10 - 2 * t), 0, 12, points=[5]), 'lead': Int(lambda t: 10 - 2 * t, 0, 5), 'sign': 24, 'lag': Int(lambda t: 10 - 2 * t, 5, 12)}),
    'l8 Q[0]': dict(ans=Int(lambda x: x - x * x, 0, 1), **{'upside': -1 / 6, 'under-line': 0.5}),
    'l8 Q[1]': dict(ans=Int(lambda x: 4 - x * x, -2, 2), **{'half': Int(lambda x: 4 - x * x, 0, 2), 'upside': -32 / 3}),
    'l8 Q[2]': dict(ans=Int(lambda x: abs(sin(x) - cos(x)), 0, pi, points=[pi / 4]), **{'no-split': Int(lambda x: sin(x) - cos(x), 0, pi), 'one-piece': Int(lambda x: sin(x) - cos(x), pi / 4, pi)}),
    # level 3 lessons
    'l9 S[6]': dict(ans=Int(lambda x: 2 * x * exp(x * x), 0, 2), **{'kept-limits': Int(exp, 0, 2), 'top-only': e ** 4}),
    'l9 S[8]': dict(ans=log(125 / 100), **{'simple': 0.25, 'no-lower': log(125)}),
    'l9 Q[1]': dict(ans=Int(lambda x: x * (x * x + 1) ** 3, 0, 1), **{'forgot-half': Int(cube, 1, 2), 'kept-limits': 0.5 * Int(cube, 0, 1)}),
    'l9 Q[2]': dict(ans=Int(lambda x: 2 * x * (x * x + 1) ** 2, 0, 1), **{'sams': 1 / 3, 'upper-only': 8 / 3}),
    'l10 S[4]': dict(ans=Int(lambda x: x * log(x), 1, e), **{'lower': e * e / 4, 'no-integral': e * e / 2}),
    'l10 S[9]': dict(ans=Int(lambda t: 10 * t * exp(-0.05 * t), 0, 2), **{'undiscounted': 20, 'end-discount': 20 * exp(-0.1), 'mid-discount': 20 * exp(-0.05)}),
    'l10 Q[2]': dict(ans=Int(lambda x: x * exp(x), 0, 2), **{'lower': e * e, 'no-integral': 2 * e * e}),
    'l10 Q[3]': dict(ans=Int(log, 1, e), **{'no-integral': e, 'top-only': e * 1 - e}),
    'l11 S[2]': dict(ans=Int(lambda x: x ** -3, 1, np.inf), **{'one-over-p': 1 / 3, 'same': Int(lambda x: x ** -2, 1, np.inf), 'sign': -0.5}),
    'l11 S[7]': dict(ans=Int(lambda t: exp(-0.04 * t), 0, np.inf), **{'times-rate': 0.04 * 100, 'rate': 0.04, 'sign': -25}),
    'l11 S[8]': dict(ans=Int(lambda t: exp(-0.02 * t), 0, np.inf), **{'no-growth': 25, 'added': 1 / 0.06}),
    'l11 Q[0]': dict(ans=Int(lambda x: 3 * x ** -4, 1, np.inf), **{'one-over-p': 3 / 4, 'no-three': 1 / 3}),
    'l11 Q[2]': dict(ans=Int(lambda t: 5 * exp(-0.1 * t), 0, np.inf), **{'times': 0.5, 'no-discount-factor': 5}),
    'l12 S[1]': dict(ans=Trap(sq, 0, 1, 2), **{'no-width': 0.125 + 0.625, 'left': Lsum(sq, 0, 1, 2), 'right-rect': Rsum(sq, 0, 1, 2)}),
    'l12 S[2]': dict(ans=5, strips=4, inside=3),
    'l12 S[4]': dict(ans=Trap(sq, 0, 1, 32) - 1 / 3, halved=0.000651 / 2, same=Trap(sq, 0, 1, 16) - 1 / 3),
    'l12 Q[0]': dict(ans=Trap(cube, 0, 2, 2), **{'no-halves': 0 + 1 + 8, 'half-h': 0.5 * 5}),
    'l12 Q[1]': dict(ans=0.008 / 4, halved=0.004),
    'l12 Q[2]': dict(ans=11, strips=10),
    'l13 S[1]': dict(ans=Int(lambda x: 6 * x * x, 0, 2) / 2, **{'no-divide': 16, 'mid-x': 6, 'midrange': 12}),
    'l13 S[2]': dict(ans=2 / pi, midrange=0.5, peak=1, **{'no-divide': 2}),
    'l13 S[3]': dict(ans=Int(lambda x: x / 20, 90, 110), total=1, **{'no-density': Int(lambda x: x, 90, 110)}),
    'l13 S[4]': dict(ans=Int(lambda x: x * x / 2, 0, 2), midpoint=1, **{'avg-density': 0.5 * Int(lambda x: x / 2, 0, 2), 'no-x': Int(sq, 0, 2)}),
    'l13 S[5]': dict(ans=Int(lambda x: (x - 100) / 20, 100, 110), **{'at-mean': 0, 'only-in-money': 5, 'no-density': 50}),
    'l13 S[7]': dict(ans=Int(lambda t: 100 + 4 * t - t * t, 0, 4) / 4, ends=100, peak=104, **{'no-divide': Int(lambda t: 100 + 4 * t - t * t, 0, 4)}),
    'l13 S[8]': dict(ans=Int(lambda x: (x - 100) * tri(x), 100, 110), uniform=2.5, **{'at-mean': 0, 'peak-density': Int(lambda x: (x - 100) / 10, 100, 110)}),
    'l13 Q[0]': dict(ans=Int(lambda x: 3 * x * x, 0, 2) / 2, ends=6, **{'no-divide': 8, 'mid-x': 3}),
    'l13 Q[2]': dict(ans=Int(lambda x: 3 * x ** 3, 0, 1), midpoint=0.5, total=1),
    'l13 Q[3]': dict(ans=Int(lambda x: (100 - x) / 20, 90, 100), **{'at-mean': 0, 'only-in-money': 5, 'no-density': 50}),
    # reviews
    'review-1 I[0]': dict(ans=Lsum(cube, 0, 2, 4), right=Rsum(cube, 0, 2, 4), exact=4, **{'no-width': 2 * Lsum(cube, 0, 2, 4)}),
    'review-1 I[1]': dict(ans=Int(lambda x: x, -1, 2), area=2.5, **{'right-part': 2, 'left-part': -0.5}),
    'review-1 I[2]': dict(ans=Rsum(cube, 0, 2, 40) - Lsum(cube, 0, 2, 40), unit=8 / 40, **{'no-height': 2 / 40, 'no-width': 8}),
    'review-1 I[3]': dict(ans=1200 * 30 + 400 * 60, rates=1600, average=800 * 90, first=36000),
    'review-1 I[4]': dict(ans=Int(sin, 0, 3 * pi), area=6, cancel=0, neg=-2),
    'review-1 I[6]': dict(ans=Int(lambda t: 300 - 100 * t, 0, 5), traded=450 + 200, stop=450, rate=300 - 500),
    'review-1 I[7]': dict(ans=Msum(sqrt, 0, 4, 2), left=Lsum(sqrt, 0, 4, 2), right=Rsum(sqrt, 0, 4, 2), **{'no-root': 2 * (1 + 3)}),
    'review-1 I[8]': dict(ans=Int(lambda t: -300 + 100 * t, 0, 3), rate=-300, end=Int(lambda t: -300 + 100 * t, 0, 6), double=-900, sign=450),
    'review-2 I[2]': dict(ans=Int(sqrt, 1, 4), heights=sqrt(4) - sqrt(1), order=-14 / 3, **{'forgot-fa': 16 / 3}),
    'review-2 I[3]': dict(ans=Int(lambda x: 2 * x - x * x, 0, 2), upside=-4 / 3, **{'under-line': 4, 'under-para': 8 / 3}),
    'review-2 I[4]': dict(ans=Int(lambda t: 5 - t, 0, 5), end=Int(lambda t: 5 - t, 0, 10), **{'max-rate': 5}),
    'review-2 I[6]': dict(ans=Int(cube, -2, 0), sign=4, **{'forgot-fa': 0}),
    'review-2 I[7]': dict(ans=Int(lambda x: abs(sin(x)), 0, 2 * pi, points=[pi]), **{'no-split': 0, 'one-hump': 2}),
    'review-2 I[8]': dict(ans=PV(5000, 0.06, 3), **{'undiscounted': 15000, 'end-discount': 15000 * exp(-0.18)}),
    'review-3 I[0]': dict(ans=Int(lambda x: x / (x * x + 1), 0, 2), **{'forgot-half': log(5)}),
    'review-3 I[2]': dict(ans=Int(lambda x: x ** -2, 2, np.inf), sign=-0.5, **{'from-one': 1}),
    'review-3 I[3]': dict(ans=Trap(recip, 1, 3, 2), exact=log(3), **{'no-halves': 1 + 1 / 2 + 1 / 3, 'half-h': 0.5 * (0.5 + 0.5 + 1 / 6)}),
    'review-3 I[4]': dict(ans=Int(sq, 0, 2) / 2, midrange=2, **{'no-divide': 8 / 3, 'mid-x': 1}),
    'review-3 I[5]': dict(ans=Int(lambda x: x * exp(-x * x), 0, np.inf), sign=-0.5, **{'forgot-half': 1}),
    'review-3 I[6]': dict(ans=Int(lambda t: t * exp(-t), 0, np.inf), sign=-1, **{'upper-only': 0}),
    'review-3 I[8]': dict(ans=Int(lambda x: (x - 105) / 20, 105, 110), **{'at-mean': 0, 'no-density': 12.5, 'only-in-money': 2.5}),
    # homework
    'homework-1 I[0]': dict(ans=Rsum(recip, 1, 3, 4), left=Lsum(recip, 1, 3, 4), exact=log(3), **{'no-width': 2 * Rsum(recip, 1, 3, 4)}),
    'homework-1 I[3]': dict(ans=Int(lambda x: abs(x) - 1, -3, 2, points=[0]), area=Int(lambda x: abs(abs(x) - 1), -3, 2, points=[-1, 0, 1]), above=2.5, below=-1),
    'homework-1 I[4]': dict(ans=-(8 - 10), added=18, **{'no-flip': -2, 'neg-added': -18}),
    'homework-1 I[5]': dict(ans=30 * sum(bars_hw1), hours=60 * sum(bars_hw1), quarter=15 * sum(bars_hw1), **{'no-minutes': sum(bars_hw1)}),
    'homework-1 I[6]': dict(ans=Int(lambda t: 300 * t * t, 0, 10), rate=30000, box=300000, triangle=150000),
    'homework-2 I[1]': dict(ans=Int(lambda x: x * x + 1, -2, 1), order=-6, **{'forgot-fa': 4 / 3, 'sign-slip': 4 / 3 - 14 / 3}),
    'homework-2 I[2]': dict(ans=sin(pi / 6) + 2, sign=-sin(pi / 6) + 2, **{'no-c': sin(pi / 6)}),
    'homework-2 I[4]': dict(ans=3 * e, value=e - 1, **{'no-chain': e}),
    'homework-2 I[5]': dict(ans=Int(lambda x: abs(4 * x - x ** 3), -2, 2, points=[0]), **{'no-split': Int(lambda x: 4 * x - x ** 3, -2, 2), 'one-piece': 4}),
    'homework-2 I[6]': dict(ans=Int(lambda s: (s - 100) * tri(s), 100, 110), uniform=2.5, **{'at-mean': 0, 'given-pays': 2 * Int(lambda s: (s - 100) * tri(s), 100, 110)}),
    'homework-2 I[7]': dict(ans=216 ** (1 / 3), **{'line-only': 72 ** (1 / 3), 'para-only': 108 ** (1 / 3)}),
    'homework-3 I[3]': dict(ans=Int(lambda t: t * exp(-0.05 * t), 0, np.inf), cube=1 / 0.05 ** 3, **{'one-over-r': 20}),
    'homework-3 I[5]': dict(ans=Int(lambda x: (x - 104) * tri(x), 104, 110), uniform=Int(lambda x: (x - 104) / 20, 104, 110), **{'at-mean': 0, 'peak-density': Int(lambda x: (x - 104) / 10, 104, 110)}),
    'homework-3 I[8]': dict(ans=Trap(lambda x: exp(-x * x), 0, 1, 4), exact=Int(lambda x: exp(-x * x), 0, 1), **{'no-halves': 0.25 * sum(exp(-(i / 4) ** 2) for i in range(5))}),
    # problem sets
    'problems-1 I[0]P[0]': dict(ans=Rsum(lambda x: 12 - 3 * x * x, 0, 2, 4), **{'left-ends': Lsum(lambda x: 12 - 3 * x * x, 0, 2, 4), 'no-width': 25.5}),
    'problems-1 I[0]P[1]': dict(ans=Lsum(lambda x: 12 - 3 * x * x, 0, 2, 4), subtracted=12.75 - 6, **{'no-length': 12.75 + 12 / 4}),
    'problems-1 I[0]P[2]': dict(ans=ceil(24 / 0.1 - 1e-9), strict=241, **{'no-length': 120}),
    'problems-1 I[0]P[4]': dict(ans=Int(lambda x: 12 - 3 * x * x, 0, 2), stopped=12.75, once=12 - 8, **{'no-squares': 24}),
    'problems-1 I[1]P[0]': dict(ans=3, **{'rate-highest': 0, 'zero-total': 6}),
    'problems-1 I[1]P[1]': dict(ans=Int(lambda t: 12 - 4 * t, 0, 3), rectangle=36, rate=12),
    'problems-1 I[1]P[2]': dict(ans=Int(lambda t: 12 - 4 * t, 0, 5), gross=18 + 8, peak=18, **{'only-outflow': Int(lambda t: 12 - 4 * t, 3, 5)}),
    'problems-1 I[1]P[3]': dict(ans=-10, gross=-26, **{'no-flip': 10}),
    'problems-1 I[1]P[4]': dict(ans=optimize.brentq(lambda T: Int(lambda t: 12 - 4 * t, 0, T), 4, 9), **{'no-half': 3 + sqrt(18 / 4), 'rate-zero': 3}),
    'problems-1 I[2]P[0]': dict(ans=Msum(lambda t: t * t - 4, 0, 3, 3), unsigned=3.75 + 1.75 + 2.25, sign=3.25, **{'right-ends': Rsum(lambda t: t * t - 4, 0, 3, 3), 'left-ends': Lsum(lambda t: t * t - 4, 0, 3, 3)}),
    'problems-1 I[2]P[1]': dict(ans=Int(lambda t: t * t - 4, 0, 3), once=9 - 4, sign=3, **{'squares-only': 9}),
    'problems-1 I[2]P[2]': dict(ans=2, end=3, **{'rate-lowest': 0}),
    'problems-1 I[2]P[3]': dict(ans=Int(lambda t: t * t - 4, 0, 2), sign=16 / 3, **{'squares-only': 8 / 3, 'rect-only': -8}),
    'problems-1 I[2]P[4]': dict(ans=Int(lambda t: t * t - 4, 2, 3), added=-3 - 16 / 3, reversed=-7 / 3, **{'rate-end': 5}),
    'problems-2 I[0]P[0]': dict(ans=9 - 18 + 8, area=Int(lambda t: t * t - 6 * t + 8, 0, 3), sign=1, **{'derivative-of-f': 2 * 3 - 6}),
    'problems-2 I[0]P[1]': dict(ans=2, min=4, vertex=3),
    'problems-2 I[0]P[3]': dict(ans=Int(lambda t: t * t - 6 * t + 8, 0, 2), **{'at-four': Int(lambda t: t * t - 6 * t + 8, 0, 4), 'at-three': 6, 'old-power': 8 / 2 - 6 * 4 + 16}),
    'problems-2 I[0]P[4]': dict(ans=Int(lambda t: t * t - 6 * t + 8, 0, 6), local=20 / 3, unsigned=Int(lambda t: abs(t * t - 6 * t + 8), 0, 6, points=[2, 4])),
    'problems-2 I[1]P[1]': dict(ans=16, zero=0, minus=-16),
    'problems-2 I[1]P[2]': dict(ans=Int(lambda t: 8 * exp(-0.5 * t), 0, 4), rate=8 * exp(-2), **{'no-c': -16 * exp(-2), 'times-k': 4 * (1 - exp(-2))}),
    'problems-2 I[1]P[3]': dict(ans=2 * log(4), divided=log(4) / 2, **{'wrong-share': 2 * log(4 / 3)}),
    'problems-2 I[2]P[1]': dict(ans=Int(lambda x: x + 3 - 2 * x * x, -1, 1.5), signs=Int(lambda x: x + 3 - 2 * x * x, -1.5, 1), **{'bottom-top': -125 / 24, 'line-only': Int(lambda x: x + 3, -1, 1.5)}),
    'problems-2 I[2]P[2]': dict(ans=Int(lambda x: 2 * x * x - x - 3, -2, -1), signed=-19 / 6, **{'parabola-only': Int(lambda x: 2 * x * x, -2, -1)}),
    'problems-2 I[2]P[3]': dict(ans=Int(lambda x: abs(x + 3 - 2 * x * x), -2, 1.5, points=[-1]), negative=-49 / 24, **{'one-integral': Int(lambda x: x + 3 - 2 * x * x, -2, 1.5)}),
    'problems-2 I[3]P[0]': dict(ans=24 - 12 - 9, value=Int(lambda t: 12 * t - 3 * t * t - 9, 0, 2), **{'no-redeem': 12}),
    'problems-2 I[3]P[2]': dict(ans=Int(lambda t: 12 * t - 3 * t * t - 9, 0, 1), sign=4, **{'no-redeem': Int(lambda t: 12 * t - 3 * t * t, 0, 1), 'at-three': Int(lambda t: 12 * t - 3 * t * t - 9, 0, 3)}),
    'problems-2 I[3]P[3]': dict(ans=Int(lambda t: 12 * t - 3 * t * t - 9, 0, 5), sign=20, level=0, **{'no-redeem': Int(lambda t: 12 * t - 3 * t * t, 0, 5)}),
    'problems-2 I[3]P[4]': dict(ans=Int(lambda t: abs(12 * t - 3 * t * t - 9), 0, 5, points=[1, 3]), net=-20, **{'unsigned-net': 20, 'missed-middle': 4 + 20}),
    'problems-3 I[0]P[1]': dict(ans=Int(lambda x: 2 * x / (1 + x * x) ** 2, 2, np.inf), below=Int(lambda x: 2 * x / (1 + x * x) ** 2, 0, 2), **{'x-limits': Int(lambda u: u ** -2, 2, np.inf)}),
    'problems-3 I[0]P[2]': dict(ans=1, **{'drop-one': sqrt(2)}),
    'problems-3 I[0]P[3]': dict(ans=sqrt(99), **{'drop-one': 10, 'no-root': 99, 'wrong-tail': sqrt(1 / 0.99 - 1)}),
    'problems-3 I[1]P[1]': dict(ans=Int(lambda x: x * exp(-x), 2, np.inf), complement=Int(lambda x: x * exp(-x), 0, 2), **{'dropped-x': exp(-2), 'dropped-one': 2 * exp(-2)}),
    'problems-3 I[1]P[2]': dict(ans=Int(lambda x: x * x * exp(-x), 0, np.inf), **{'no-factor': 1}),
    'problems-3 I[1]P[3]': dict(ans=100 * Int(lambda x: x * exp(-2 * x), 0, np.inf), half=50, one=100, **{'mean-wait': 100 * exp(-2)}),
    'problems-3 I[2]P[0]': dict(ans=Trap(log, 0.5, 1.5, 2), midpoint=Msum(log, 0.5, 1.5, 2), sign=0.5 * (0.34657 - 0.20273), **{'full-ends': 0.5 * (log(0.5) + log(1.5)), 'lost-strip': 0.5 * (log(0.5) + log(1)) / 2}),
    'problems-3 I[2]P[1]': dict(ans=Int(log, 0.5, 1.5), estimate=Trap(log, 0.5, 1.5, 2), sign=-Int(log, 0.5, 1.5), **{'plus-x': (1.5 * log(1.5) + 1.5) - (0.5 * log(0.5) + 0.5), 'uv-only': 1.5 * log(1.5) - 0.5 * log(0.5)}),
    'problems-3 I[2]P[2]': dict(ans=0.0267 / 16, linear=0.0267 / 4, **{'eight-squared': 0.0267 / 64}),
    'problems-3 I[3]P[1]': dict(ans=Int(sig, 0, 4), quarter=(1 - exp(-2)) / 4, sign=-Int(sig, 0, 4), **{'x-limits': 4 * (1 - exp(-4))}),
    'problems-3 I[3]P[2]': dict(ans=Int(sig, 0, 4) / 4, halved=Int(sig, 0, 4) / 2, **{'no-divide': Int(sig, 0, 4), 'x-limits': 1 - exp(-4)}),
    'problems-3 I[3]P[3]': dict(ans=Trap(sig, 0, 4, 2), midpoint=Msum(sig, 0, 4, 2), **{'full-ends': 2 * (sig(0) + sig(2) + sig(4)), 'no-h': Trap(sig, 0, 4, 2) / 2}),
    'problems-3 I[3]P[4]': dict(ans=next(2 * 2 ** k for k in range(20) if 0.49 / 4 ** k < 0.01), linear=next(2 * 2 ** k for k in range(20) if 0.49 / 2 ** k < 0.01), **{'one-short': 8}),
}

seen = set()
for key, w in numeric_widgets():
    if 'answers' in w:                     # problems-2 item 3 part 1: the two crossings
        roots = sorted(np.roots([2, -1, -3]).real)
        check(all(close(a, b, tol_of(w, 1)) for a, b in zip(sorted(w['answers']), roots)), f'A {key}: crossings {w["answers"]} vs {roots}')
        check(sorted(float(s) for s in w['wrong'][0]['value'].split(',')) == sorted(np.roots([2, 1, -3]).real.round(9).tolist()), f'A {key}: slip "signs" is the roots of 2x^2 + x - 3')
        seen.add(key)
        continue
    exp_ = EXP.get(key)
    check(exp_ is not None, f'A {key}: no recomputation in the table')
    if exp_ is None:
        continue
    seen.add(key)
    t = tol_of(w)
    check(close(w['answer'], exp_['ans'], t), f'A {key}: key {w["answer"]} vs recomputed {exp_["ans"]:.10g} (tol {t:g})')
    ids = [x['id'] for x in w.get('wrong', [])]
    check(sorted(ids) == sorted(k for k in exp_ if k != 'ans'), f'A {key}: slip ids {ids} vs table {sorted(k for k in exp_ if k != "ans")}')
    for x in w.get('wrong', []):
        if x['id'] not in exp_:
            continue
        tw = (x.get('tol') or {})
        tw = abs(tw['rel'] * x['value']) if 'rel' in tw else tw.get('abs', 0)
        check(close(x['value'], exp_[x['id']], tw), f'A {key}: slip {x["id"]} = {x["value"]} but the named mistake gives {exp_[x["id"]]:.10g} (band {tw:g})')
        check(abs(x['value'] - w['answer']) > t + tw, f'A {key}: slip {x["id"]} band overlaps the key band')
check(set(EXP) <= seen, f'A table keys without a widget: {sorted(set(EXP) - seen)}')

# ---------- B. accept lines ----------
NUM = re.compile(r'(?<![\w.{^_])[-−]?\d+(?:[.,]\d+)*(?:\.\d+)?')


def nums(s):
    s = s.replace('{,}', '').replace('−', '-')
    out = []
    for m in re.finditer(r'(?<![\w.^_{/])-?\d[\d,]*\.?\d*', s):
        tok = m.group(0).replace(',', '')
        try:
            out.append(float(tok))
        except ValueError:
            pass
    return out


accept_hits = 0
for key, w in numeric_widgets():
    acc = w.get('accept')
    if not isinstance(acc, str) or 'answers' in w:
        continue
    t = tol_of(w)
    # the figure printed as the answer is the first number of the line, or the one after an "approx" sign
    m = re.search(r'\\approx\s*(?:\\text\{£\})?\s*(-?[\d.{},]+)', acc.replace('−', '-'))
    if m:
        shown = float(m.group(1).replace('{,}', '').replace(',', '').rstrip('.'))
    else:
        m0 = re.match(r'\s*\$?(?:£|\\text\{£\})?(-?\d[\d,{}]*\.?\d*)', acc.replace('−', '-').replace('About ', '').replace('Exactly ', ''))
        shown = float(m0.group(1).replace('{,}', '').replace(',', '').rstrip('.')) if m0 else None
    mf = re.match(r'\s*\$?(-?)\\t?frac\{(\d+)\}\{(\d+)\}(?=\$|\s*\\approx|\s*=|\s*:|\s*$)', acc.replace('−', '-'))
    if mf:                                # a leading fraction is the exact answer
        accept_hits += 1
        fv = (-1 if mf.group(1) else 1) * int(mf.group(2)) / int(mf.group(3))
        check(close(fv, w['answer'], t), f'B {key}: accept line leads with {mf.group(0).strip()} = {fv:.6f}, refused by {w["answer"]} +- {t:g}')
    if shown is not None and not re.match(r'\s*Any value from', acc):
        accept_hits += 1
        check(close(shown, w['answer'], t), f'B {key}: accept line prints {shown} but the widget accepts {w["answer"]} +- {t:g}')
    # "x is accepted too"
    for m in re.finditer(r'\(\$?(-?[\d.]+)\$? is accepted too\)', acc.replace('−', '-')):
        check(close(float(m.group(1)), w['answer'], t), f'B {key}: "{m.group(1)} is accepted too" is refused')
    # "Any value from a to b"
    m = re.search(r'Any value from (\d+\.\d+) to (\d+\.\d+)', acc)
    if m:
        a, b = float(m.group(1)), float(m.group(2))
        check(close(a, w['answer'], t) and close(b, w['answer'], t) and not close(a - 0.011, w['answer'], t) and not close(b + 0.011, w['answer'], t), f'B {key}: range {a} to {b} is not the accepted range')
    # "x +- t" bands: both printed ends must be accepted (KNOWN: the band is centred on the unrounded key, not on x)
    m = re.search(r'(-?[\d.]+)\s*\\pm\s*([\d.]+)', acc.replace('−', '-'))
    if m:
        x, band = float(m.group(1)), float(m.group(2))
        check(close(x, w['answer'], t), f'B {key}: the centre {x} of the printed band is refused')
        ends_ok = close(x - band * 0.98, w['answer'], t) and close(x + band * 0.98, w['answer'], t)
        check(ends_ok, f'B {key}: accept line says "{m.group(0)}" but the accepted set is {w["answer"]:.6f} +- {t:g}; part of the printed band is refused', known=True)
    # "within t of ..." (the fix-pass wording of finding 4): t must be the widget's own absolute tolerance
    for mw in re.finditer(r'within ([\d.]+) of', acc):
        check(isinstance(w.get('tol'), dict) and 'abs' in w['tol'] and close(float(mw.group(1)), w['tol']['abs'], 1e-12),
              f'B {key}: accept line says "within {mw.group(1)}" but the widget tol is {w.get("tol")}')
check(accept_hits > 100, f'B only {accept_hits} accept figures were read')

# ---------- C. other printed figures ----------
R = lambda n: Rsum(sq, 0, 1, n)
Lq = lambda n: Lsum(sq, 0, 1, n)
C = [
    # lesson 1
    (round(R(7), 3) == 0.408 and round(R(8), 3) == 0.398, 'l1 S2: seven rectangles 0.408, eight 0.398'),
    (round(R(4), 3) == 0.469 and round(Lq(4), 3) == 0.219, 'l1: R4 = 0.469, L4 = 0.219'),
    (close(Rsum(sq, 1, 2, 4), 2.71875, 0) and round(7 / 3, 3) == 2.333, 'l1 S7: right sum 2.71875, area 7/3'),
    (all(round(phi(x), 4) == h for x, h in zip([0.125, 0.375, 0.625, 0.875], mid_heights)), 'l1 S10: the four printed heights are the normal density at the midpoints'),
    (round(sum(mid_heights), 3) == 1.368 and round(stats.norm.cdf(1) - 0.5, 4) == 0.3413 and abs(0.342 - 0.3413) < 0.001, 'l1 S10: heights add to 1.368; exact 0.3413; within 0.001'),
    (close(Rsum(sq, 0, 1, 2), 0.625, 0) and close(Lsum(sq, 0, 1, 2), 0.125, 0), 'l1 quiz: R2 = 0.625, L2 = 0.125'),
    (Lsum(cube, 0, 2, 2) == 1 and Rsum(cube, 0, 2, 2) == 9 and Int(cube, 0, 2) - 4 < 1e-12, 'l1 quiz: left 1, right 9, area 4'),
    # lesson 2
    (round(Lq(20), 3) == 0.309 and round(R(20), 3) == 0.359 and round(1 / 19, 4) == 0.0526, 'l2 S1: L20 0.309, R20 0.359, gap at 19 is 0.0526'),
    (all(close(R(n), v, 1e-9) for n, v in [(1, 1), (2, 0.625), (4, 0.46875), (10, 0.385)]), 'l2 table of R_n'),
    (all(close(R(n), 1 / 3 + 1 / (2 * n) + 1 / (6 * n * n), 1e-12) and close(Lq(n), 1 / 3 - 1 / (2 * n) + 1 / (6 * n * n), 1e-12) for n in range(1, 200)), 'l2: closed forms of R_n and L_n'),
    (all(close(R(n) - Lq(n), 1 / n, 1e-12) for n in range(1, 60)), 'l2: gap is 1/n'),
    (round(1 / 200, 3) == 0.005 and abs(1 / 60000 - 0.0000167) < 5e-8 and close(101 * 201 / 60000, 0.33835, 1e-9), 'l2 S5: 0.005, 0.0000167, 101 x 201 / 60000'),
    (close(Lsum(lambda x: 1 - x * x, 0, 1, 4), 0.78125, 0) and close(Rsum(lambda x: 1 - x * x, 0, 1, 4), 0.53125, 0), 'l2 S6: L4 = 0.78125, R4 = 0.53125 for 1 - x^2'),
    (close(Rsum(sqrt, 0, 4, 50) - Lsum(sqrt, 0, 4, 50), 0.16, 1e-12), 'l2 S7: gap 0.16 for sqrt on [0, 4], n = 50'),
    (round(exp(-0.5), 4) == 0.6065 and round(10 * (1 - 0.6065), 3) == 3.935 and round(10 * (1 - exp(-0.5)) / 393, 5) == 0.01001 and round(PV(1, 0.05, 10), 2) == 7.87, 'l2 S9: D(10), 3.935, gap at 393 strips, value 7.87'),
    (Lsum(lambda t: exp(-0.05 * t), 0, 10, 394) - Rsum(lambda t: exp(-0.05 * t), 0, 10, 394) <= 0.01 < Lsum(lambda t: exp(-0.05 * t), 0, 10, 393) - Rsum(lambda t: exp(-0.05 * t), 0, 10, 393), 'l2 S9: 394 strips is the first gap of at most 0.01'),
    (close(9 * 19 / 600, 0.285, 1e-12), 'l2 quiz: 9 x 19 / 600'),
    # lesson 3
    (abs(Msum(sin, 0, pi, 1000) - 2) < 5e-4, 'l3 S6: midpoint sum with n = 1000 gives 2.000'),
    (close(Int(lambda x: 2 * sin(pi * x / 2), 0, 8), 0, 1e-9), 'l3 S3: four equal humps on [0, 8] cancel'),
    # lesson 4
    (176 < 10 * 4.2 ** 2 < 180 < 10 * 4.25 ** 2 and 10 * 16 == 160 and 10 * 9 == 90 and 10 * 36 == 360, 'l4 S2: caption figures'),
    (round(400000 / 365, 2) == 1095.89 and round(450000 / 365, 2) == 1232.88 and round(30 * 400000 / 365, 2) == 32876.71 and round(60 * 450000 / 365, 2) == 73972.60, 'l4 S9: daily accruals and the two rectangles'),
    (close(30 * 1095.89 + 60 * 1232.88, 106849.32, 1), 'l4 S9: the rounded daily rates also land inside the tolerance'),
    (Int(lambda t: 400 - 200 * t, 0, 4) < 1e-9, 'l4 S6: P&L back to 0 by hour 4'),
    # lesson 5
    (round(A5(2) - A5(1.75), 2) == 0.99 and round(A5(4) - A5(3.75), 2) == 0.12, 'l5 S1: steps 0.99 and 0.12'),
    (round(A5(2.25) - A5(2), 3) == 0.995 and round(A5(2.25), 2) == 6.33 and round(A5(2), 2) == 5.33, 'l5 S3: 0.995, 6.33, 5.33'),
    (all(close((A5(2 + h) - A5(2)) / h, 4 - h * h / 3, 1e-9) for h in [0.5, 0.25, 0.1, 0.01]), 'l5 S4: rise over run is 4 - h^2/3'),
    (round(A5(4), 2) == 10.67 and round(A5(5), 2) == 8.33 and close(A5(1), 5 / 3, 1e-12), 'l5: A(4), A(5), A(1)'),
    (close(Int(lambda t: 4 - t, 0, 4), 8, 1e-9) and close(Int(lambda t: 4 - t, 0, 8), 0, 1e-9), 'l5 S9: peak 8, flat by the close'),
    # lesson 7
    (round(PV(10000, 0.04, 5)) == 45317 and round(50000 - PV(10000, 0.04, 5)) == 4683 and round(1 - exp(-0.2), 5) == 0.18127, 'l7 S10: 45,317; 4,683; 0.18127'),
    (close(Int(lambda x: 4 * x ** 3 - 2 * x, 0, 1 / sqrt(2)), -0.25, 1e-9) and close(Int(lambda x: 4 * x ** 3 - 2 * x, 1 / sqrt(2), 1), 0.25, 1e-9), 'l7 quiz: two parts of area 1/4'),
    (round(1 - exp(-0.5), 5) == 0.39347 and round(100 * PV(2000, 0.05, 10) / 20000) == 79, 'l7 quiz: 0.39347 and 79%'),
    # lesson 8
    (close(Int(lambda x: cos(x) - sin(x), 0, pi / 4), sqrt(2) - 1, 1e-9) and close(Int(lambda x: sin(x) - cos(x), pi / 4, pi), sqrt(2) + 1, 1e-9) and round(2 * sqrt(2), 2) == 2.83, 'l8 S7: the two pieces and 2.83'),
    # lesson 9
    (round(2 * e, 2) == 5.44 and round(e - 1, 3) == 1.718 and round(e ** 2 - 1, 3) == 6.389, 'l9: 5.44, 1.718, 6.389'),
    # lesson 10
    (round(e, 2) == 2.72 and round(-4400 * exp(-0.1), 3) == -3981.285 and round(1000 * Int(lambda t: 10 * t * exp(-0.05 * t), 0, 2)) == 18715, 'l10: slope 2.72, -3981.285, 18,715'),
    (close(2 ** 3 / 3, 8 / 3, 0) and close(8 / 3 + 16 / 3, 8, 1e-12), 'l10 S2: blue 8/3, orange 16/3'),
    # lesson 11
    ([round(1 - 1 / b, 4) for b in (10, 100, 1000)] == [0.9, 0.99, 0.999], 'l11 S1: 0.9, 0.99, 0.999'),
    (2 * sqrt(100) - 2 == 18 and 2 * sqrt(10000) - 2 == 198, 'l11 S4: 18 and 198'),
    (round(log(1000), 1) == 6.9 and round(log(1e6), 1) == 13.8 and round(log(1e12), 1) == 27.6, 'l11 S5: ln figures'),
    (close(Int(lambda x: x ** -1.01, 1, np.inf), 100, 1e-5), 'l11 quiz: p = 1.01 gives 100'),
    # lesson 12
    ([Trap(sq, 0, 1, n) for n in (1, 2, 4)] == [0.5, 0.375, 0.34375], 'l12 S1: sums 0.5, 0.375, 0.34375'),
    ([f'{Trap(sq, 0, 1, n):.6f}' for n in (4, 8, 16)] == ['0.343750', '0.335938', '0.333984'] and [f'{Trap(sq, 0, 1, n) - 1 / 3:.6f}' for n in (4, 8, 16)] == ['0.010417', '0.002604', '0.000651'], 'l12 S5: the table'),
    (all(close(Trap(sq, 0, 1, n) - 1 / 3, 1 / (6 * n * n), 1e-12) for n in range(1, 100)) and round(1 / 6144, 6) == 0.000163, 'l12 S5: error is exactly 1/(6 n^2)'),
    (round(0.25 * ((0 + 0.75 ** 2) / 2 + 0.25 ** 2 + 0.5 ** 2), 4) == 0.1484, 'l12 S6: Jo returns 0.1484'),
    (Trap(lambda x: 3 * x + 2, 0, 4, 1) == 32 == round(Int(lambda x: 3 * x + 2, 0, 4), 9), 'l12 quiz: T1 = 32 exactly'),
    (round(1 / sqrt(2 * pi), 5) == 0.39894, 'l12 S9: phi(0)'),
    (f'{Trap(phi, -1.96, 1.96, 1000):.6f}' == '0.950004' == f'{2 * stats.norm.cdf(1.96) - 1:.6f}' and round(Trap(phi, -1.96, 1.96, 10), 4) == 0.9471, 'l12 S9: 0.950004 both ways; 0.9471 with 10 strips'),
    # lesson 13
    (round(2 * 3 ** 1.5 / 3, 2) == 3.46 and close(9 - 9 + 2 * 3 ** 1.5 / 3, 2 * 3 ** 1.5 / 3, 0), 'l13 S1: both areas about 3.46 at height 3'),
    (round(Int(lambda t: 100 + 4 * t - t * t, 0, 4), 2) == 410.67, 'l13 S8: 410.67 pound-hours'),
    (close(Int(tri, 90, 110, points=[100]), 1, 1e-9), 'l13 S9: the triangular density integrates to 1'),
    # reviews and homework
    (round(Int(sqrt, 0, 4), 2) == 5.33 and round(2 * (1 + sqrt(3)), 2) == 5.46, 'review-1: 16/3 and M2'),
    (round(5000 / 0.06) == 83333 and round(1 - exp(-0.18), 5) == 0.16473, 'review-2: 83,333 and 0.16473'),
    (round(log(3), 4) == 1.0986, 'review-3: ln 3'),
    ([round(1 / x, 3) for x in (1.5, 2, 2.5, 3)] == [0.667, 0.5, 0.4, 0.333] and round(log(3), 3) == 1.099, 'homework-1: heights and 1.099'),
    (close(Rsum(cube, 0, 1, 2), 0.5625, 0), 'homework-1: cube check at n = 2'),
    (close(Rsum(sq, 0, 2, 1), 8, 0) and all(close(Rsum(sq, 0, 2, n), 4 * (n + 1) * (2 * n + 1) / (3 * n * n), 1e-9) for n in range(1, 50)), 'homework-1: R_n on [0, 2]'),
    (all(close(Rsum(lambda x: 9 - x * x, 1, 3, n), 28 / 3 - 8 / n - 4 / (3 * n * n), 1e-9) and close(Lsum(lambda x: 9 - x * x, 1, 3, n), 28 / 3 + 8 / n - 4 / (3 * n * n), 1e-9) for n in range(1, 60)), 'homework-1 derivation: R_n and L_n for 9 - x^2 on [1, 3]'),
    (Rsum(lambda x: 9 - x * x, 1, 3, 4) == 7.25 and Lsum(lambda x: 9 - x * x, 1, 3, 4) == 11.25, 'homework-1 derivation: R4 = 7.25, L4 = 11.25'),
    (Lsum(lambda t: 600 - 200 * t, 0, 5, 5) == 1000 and Rsum(lambda t: 600 - 200 * t, 0, 5, 5) == 0 and round(Int(lambda t: 600 - 200 * t, 0, 5)) == 500 and round(Int(lambda t: abs(600 - 200 * t), 0, 5, points=[3])) == 1300, 'homework-1 inventory: 1000, 0, 500, 1300'),
    (round(300000 * (1 - exp(-0.2))) == 54381 and round(60000 * exp(-0.2)) == 49124 and round(1 - exp(-0.2), 6) == 0.181269, 'homework-2 lease: 54,381; 49,124'),
    (round(sqrt(2 * log(2) / 3), 4) == 0.6798 and round(log(2), 4) == 0.6931 and round(2 * 0.6931 / 3, 4) == 0.4621, 'homework-2 window: 0.6798, 0.6931, 0.4621'),
    (abs(optimize.minimize_scalar(lambda x: -(stats.norm.cdf(2 * x) - stats.norm.cdf(x)), bounds=(0.01, 3), method='bounded', options={'xatol': 1e-10}).x - sqrt(2 * log(2) / 3)) < 1e-6, 'homework-2 window: the maximiser of P(x < Z < 2x) is sqrt(2 ln 2 / 3)'),
    ([round(exp(-(i / 4) ** 2), 4) for i in range(5)] == [1, 0.9394, 0.7788, 0.5698, 0.3679] and round(Trap(lambda x: exp(-x * x), 0, 1, 4) / 0.25, 4) == 2.9719 and round(Int(lambda x: exp(-x * x), 0, 1), 4) == 0.7468, 'homework-3: heights, 2.9719, 0.7468'),
    (round(1 / 0.041, 2) == 24.39 and round(100 * (1 - 0.04 / 0.041), 2) == 2.44, 'homework-3 duration: 24.39 and 2.44%'),
    (all(close(Int(lambda x: log(x) / x ** 3, 1, b), 0.25 - 1 / (4 * b * b) - log(b) / (2 * b * b), 1e-9) for b in (2, 5, 30)), 'homework-3 log tail: the finite-range formula'),
    (round(1 / (6 * 32 ** 2), 6) == 0.000163 and round(1 / (6 * 64 ** 2), 6) == 0.000041, 'homework-3 code item: errors at n = 32 and 64'),
    # problem sets
    (all(close(Rsum(lambda x: 12 - 3 * x * x, 0, 2, n), 16 - 12 / n - 4 / (n * n), 1e-9) for n in range(1, 60)), 'problems-1: R_n = 16 - 12/n - 4/n^2'),
    (round(16 - 16 * exp(-2), 2) == 13.83 and round(16 * exp(-2), 2) == 2.17 and close(13.84, 16 - 16 * exp(-2), 0.01), 'problems-2: 13.83, 2.17, and 13.84 accepted'),
    (close(Int(lambda x: x + 3 - 2 * x * x, -2, 1.5), 49 / 24, 1e-9), 'problems-2: one integral gives 49/24'),
    (round(stats.gamma(2).median(), 2) == 1.68 and round(100 * exp(-stats.gamma(2).median()), 2) == 18.67 and round(100 * exp(-2), 2) == 13.53, 'problems-3: median 1.68 gives 18.67; mean wait gives 13.53'),
    (round(0.5 * log(0.5), 5) == -0.34657 and round(0.5 * log(1.5), 5) == 0.20273 and round(1.5 * log(1.5) - 1.5, 4) == -0.8918 and round(0.5 * log(0.5) - 0.5, 4) == -0.8466, 'problems-3: the four log figures'),
    (round(Trap(log, 0.5, 1.5, 2) - Int(log, 0.5, 1.5), 4) == -0.0267, 'problems-3: T2 is out by 0.0267'),
    (round(sig(2), 4) == 1.2131 and round(sig(4), 4) == 0.5413 and round(Int(sig, 0, 4) - Trap(sig, 0, 4, 2), 2) == 0.49, 'problems-3: s(2), s(4), error 0.49'),
    ([round(0.49 / 4 ** k, 4) for k in (1, 2, 3)] == [0.1225, 0.0306, 0.0077], 'problems-3: predicted errors 0.12, 0.031, 0.0077'),
]
for ok, label in C:
    check(bool(ok), 'C ' + label)

# cross-references between lessons (KNOWN: two "last lesson" lines point one lesson too near)
l4, l7 = FILES['l4-accumulating-a-rate'], FILES['l7-evaluating']
check('last lesson' not in l4['screens'][7]['explain']['text'], 'C l4 screens[7].explain: "the same squeeze as last lesson", but the squeeze is in l2 (l3 has none)', known=True)
check('Last lesson' not in l7['screens'][8]['prose'], 'C l7 screens[8].prose: "Last lesson ... A\' = f", but that is lesson 5 (lesson 6 is antiderivatives)', known=True)

q3 = FILES['l10-undo-product']['quiz'][3]['feedback']['byKey']['no-integral']
check('Subtract the $-x$ part' not in q3, 'C l10 quiz[3] byKey no-integral: "Subtract the -x part" read literally gives e + (e - 1) = %.3f, not 1; the piece [-x] is added' % (e + e - 1), known=True)
check(close(e + (-(e - 1)), 1, 1e-12), 'C l10 quiz[3]: [x ln x] + [-x] between 1 and e is 1')

# ---------- D. empirical and statistical claims ----------
rng = np.random.default_rng(20261126)
z = rng.standard_normal(4_000_000)
p = np.mean(np.abs(z) <= 1.96)                       # s.e. 0.00011
check(abs(p - 0.95) < 0.0006, f'D l12 S9: P(|Z| <= 1.96) = {p:.5f}, the familiar 95% (about 1 day in 20 outside)')
p = np.mean((z > 0) & (z < 1))                       # s.e. 0.00024
check(abs(p - 0.3413) < 0.0012 and abs(p - 0.342) < 0.002, f'D l1 S10: P(0 < Z < 1) = {p:.5f}')
u = rng.uniform(90, 110, 4_000_000)
c = np.maximum(u - 100, 0)
check(abs(c.mean() - 2.5) < 0.01 and abs(np.maximum(100 - u, 0).mean() - 2.5) < 0.01, f'D l7/l13: uniform call and put worth 2.50 ({c.mean():.4f})')
check(abs(np.mean(c[c > 0]) - 5) < 0.02 and max(u.mean() - 100, 0) < 0.02, 'D l13: average payoff 5 when it pays; payoff at the mean price is 0')
check(abs(np.maximum(u - 105, 0).mean() - 0.625) < 0.006, 'D review-3: call struck at 105 worth 0.625')
tr = 90 + 10 * (rng.random(4_000_000) + rng.random(4_000_000))   # triangular on [90, 110]
check(abs(np.maximum(tr - 100, 0).mean() - 5 / 3) < 0.008, f'D l13 S9 / homework-2: triangular call worth 1.67 ({np.maximum(tr - 100, 0).mean():.4f})')
check(abs(np.maximum(tr - 104, 0).mean() - 0.36) < 0.004, 'D homework-3: triangular call struck at 104 worth 0.36')
check(np.maximum(tr - 100, 0).mean() < c.mean() - 0.7, 'D l13 S9: the wider uniform model prices the call higher')
g = rng.gamma(2.0, 1.0, 4_000_000)                    # density x e^-x
check(abs(np.mean(g > 2) - 3 * exp(-2)) < 0.0012 and abs(g.mean() - 2) < 0.004 and abs(np.mean(100 * np.exp(-g)) - 25) < 0.06, 'D problems-3 item 2: P(X > 2), E[X] = 2, E[100 e^-X] = 25')
check(np.mean(100 * np.exp(-g)) > 100 * exp(-g.mean()) + 10, 'D problems-3 item 2: the expected value is above the value at the mean wait (convex payoff)')
uu = rng.random(4_000_000)
xs = np.sqrt(1 / (1 - uu) - 1)                         # inverse of F(x) = 1 - 1/(1 + x^2)
check(abs(np.mean(xs > 2) - 0.2) < 0.001 and abs(np.median(xs) - 1) < 0.003 and abs(np.mean(xs > sqrt(99)) - 0.01) < 0.0003, 'D problems-3 item 1: tail 0.2, median 1, 1% size sqrt(99)')
check(close(Int(lambda x: 2 * x / (1 + x * x) ** 2, 0, np.inf), 1, 1e-9), 'D problems-3 item 1: the density integrates to 1 (quadrature, independent of the sampler)')
w = rng.uniform(0.5, 1.5, (400_000, 10))
lw = np.log(w)
wealth = w.prod(axis=1)
check(abs(lw.mean() - (-0.0452)) < 0.0005 and abs(w.mean() - 1) < 0.001, f'D problems-3 item 3: E[ln X] = {lw.mean():.4f} with E[X] = 1')
check(np.median(wealth) < 0.70 and abs(wealth.mean() - 1) < 0.012, f'D problems-3 item 3: over 10 independent years the typical path shrinks (median {np.median(wealth):.3f}) while the mean stays at 1 ({wealth.mean():.3f})')
# rising curve: left sums below, right sums above, for every n; falling curve the reverse
check(all(Lsum(sq, 0, 1, n) < 1 / 3 < Rsum(sq, 0, 1, n) for n in range(1, 400)), 'D l1/l2: on a rising curve L_n < area < R_n for every n')
check(all(Rsum(recip, 1, 2, n) < log(2) < Lsum(recip, 1, 2, n) for n in range(1, 400)), 'D l2 quiz: on a falling curve R_n < area < L_n for every n')
check(all(Rsum(sq, 0, 1, 2 * n) < Rsum(sq, 0, 1, n) and Lsum(sq, 0, 1, 2 * n) > Lsum(sq, 0, 1, n) for n in range(1, 200)), 'D l1 quiz: thinner right rectangles overshoot less')
# trapezium rule: error ratio about 4 per doubling for smooth integrands; exact for lines; sign follows the curvature
for name, f, a, b in [('x^2', sq, 0, 1), ('1/x', recip, 1, 2), ('ln x', log, 0.5, 1.5), ('exp', exp, 0, 1), ('signal', sig, 0, 4), ('phi', phi, -1.96, 1.96)]:
    ex = Int(f, a, b)
    ratios = [(Trap(f, a, b, n) - ex) / (Trap(f, a, b, 2 * n) - ex) for n in (16, 32, 64, 128)]
    check(all(3.9 < r < 4.1 for r in ratios), f'D l12: trapezium error quarters on doubling for {name} ({ratios[0]:.3f})')
check(abs((Trap(sq, 0, 1, 100) - 1 / 3) / (Trap(sq, 0, 1, 300) - 1 / 3) - 9) < 1e-6 and abs((Trap(exp, 0, 1, 20) - (e - 1)) / (Trap(exp, 0, 1, 80) - (e - 1)) - 16) < 0.05, 'D l12 S7 / review-3: factors 9 and 16')
check(Trap(cube, 0, 2, 2) > 4 and Trap(recip, 1, 3, 2) > log(3) and Trap(sq, 0, 1, 7) > 1 / 3, 'D l12: chords lie above a curve that bends upwards')
check(Trap(lambda x: exp(-x * x), 0, 1, 4) < Int(lambda x: exp(-x * x), 0, 1) and 1 / sqrt(2) > 0.5, 'D homework-3: T4 is low for exp(-x^2), concave on [0, 0.707]')
check(abs(Trap(log, 0.5, 1.5, 8) - Int(log, 0.5, 1.5)) < 0.0019 and abs(abs(Trap(log, 0.5, 1.5, 8) - Int(log, 0.5, 1.5)) - 0.0017) < 0.0002, 'D problems-3 item 3: the predicted error 0.0017 at n = 8 is what the rule gives')
err = lambda n: abs(Trap(sig, 0, 4, n) - Int(sig, 0, 4))
check(err(16) < 0.01 < err(8), f'D problems-3 item 4: the error is really below 0.01 first at n = 16 ({err(8):.4f}, {err(16):.4f})')
# improper integrals: p-test at the boundary
check(all(Int(lambda x: x ** -pp, 1, 1e6) > 10 for pp in (0.5, 0.99, 1.0)) and close(Int(lambda x: x ** -2, 1, np.inf), 1, 1e-9), 'D l11: p <= 1 grows without limit, p = 2 gives 1')
check(all(close(Int(lambda x: log(x) / x, 1, b), 0.5 * log(b) ** 2, 1e-8) for b in (10, 1e3, 1e5)), 'D homework-3: integral of ln x / x to b is (ln b)^2 / 2')
# fundamental theorem checks by finite differences
G = lambda x: Int(lambda t: exp(t), 0, x ** 3)
check(abs((G(1 + 1e-5) - G(1 - 1e-5)) / 2e-5 - 3 * e) < 1e-4, 'D homework-2: G\'(1) = 3e for the moving limit x^3')
H = lambda x: Int(lambda t: cos(t * t), 0, x)
check(abs((H(1.3 + 1e-5) - H(1.3 - 1e-5)) / 2e-5 - cos(1.69)) < 1e-6, 'D review-2: derivative of the accumulation function is the integrand')
check(abs(Int(lambda t: 1 / (100 * exp(0.3 * sin(9 * t) + log(1.25) * t)) * (100 * exp(0.3 * sin(9 * t) + log(1.25) * t) * (2.7 * cos(9 * t) + log(1.25))), 0, 1) - (0.3 * sin(9) + log(1.25))) < 1e-8, 'D l9 S9: the integral of S\'/S depends only on the end prices (a wiggly path)')

# ---------- F. code widgets in CPython ----------
def run_tests(widget):
    ns = {}
    exec(widget['solution'], ns)
    out = []
    for t in widget['tests']:
        if t.get('setup'):
            exec(t['setup'], ns)
        got, want = eval(t['call'], ns), eval(t['expect'], ns)
        out.append(math.isclose(got, want, rel_tol=1e-9) if t['compare'] == 'isclose' else got == want)
    return out


for name, w in [('l12 S4 trapezium', FILES['l12-no-formula']['screens'][3]['widget']), ('l12 S9 phi', FILES['l12-no-formula']['screens'][8]['widget']), ('homework-3 n_needed', FILES['homework-3']['items'][4]['widget'])]:
    res = run_tests(w)
    check(all(res), f'F {name}: solution passes its hidden tests in CPython {res}')
ns = {}
exec(FILES['homework-3']['items'][4]['widget']['solution'], ns)
check(ns['n_needed'](sq, 0, 1, 1 / 3, 1e-4) == 64 == next(2 ** k for k in range(20) if 1 / (6 * 4 ** k) < 1e-4), 'F homework-3: 64 is the first power of 2 with error below 1e-4')

# ---------- E. fluency families ----------
def tex_to_sympy(s, var):
    import sympy as sp
    from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
    s = s.replace('\\,', '').replace('\\displaystyle', '').replace('\\left', '').replace('\\right', '').replace('\\dfrac', '\\frac').replace('\\tfrac', '\\frac')
    for _ in range(8):
        s2 = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', s)
        if s2 == s:
            break
        s = s2
    for _ in range(4):
        s = re.sub(r'e\^\{([^{}]*)\}', r' exp(\1)', s)
        s = re.sub(r'\^\{([^{}]*)\}', r'**(\1)', s)
    s = re.sub(r'\\ln\s*\(', ' log(', s)
    s = re.sub(r'\\ln\s*([a-z])', r' log(\1)', s)
    s = s.replace('\\sin', ' sin').replace('\\cos', ' cos').replace('{', '(').replace('}', ')')
    v = sp.Symbol(var, positive=True)
    return parse_expr(s, local_dict={var: v, 'exp': sp.exp, 'log': sp.log, 'sin': sp.sin, 'cos': sp.cos}, transformations=standard_transformations + (implicit_multiplication_application, convert_xor)), v


def fluency():
    import sympy as sp
    node = shutil.which('node')
    if not node:
        print('SKIP  E: node not found, fluency families not sampled')
        return
    tool = os.path.join(ROOT, 'app', 'tools', 'fluency-sample.mjs')
    drawn = 0
    for name in ('fluency-l6-working-backwards', 'fluency-l7-evaluating', 'fluency-l9-undo-chain', 'fluency-l10-undo-product'):
        fams = [f['id'] for f in load(name)['families']]
        for fam in fams:
            r = subprocess.run([node, tool, '--set', 'integrals/' + name, '--family', fam, '--n', '60', '--json'], capture_output=True, text=True, cwd=os.path.join(ROOT, 'app'))
            check(r.returncode == 0, f'E {name}/{fam}: sampler exit {r.returncode}')
            if r.returncode:
                continue
            for it in json.loads(r.stdout)['items']:
                drawn += 1
                tag = f'E {name}/{fam} seed {it["seed"]}'
                pr = it['prompt']
                if fam == 'fix-constant':
                    m = re.search(r"F'\(x\) = (.+?)\$ and \$F\((-?\d+)\) = (-?\d+)\$\. Work out \$F\((-?\d+)\)", pr)
                    f, x = tex_to_sympy(m.group(1), 'x')
                    x = sp.Symbol('x')
                    f = f.subs({s: x for s in f.free_symbols})
                    true = int(m.group(3)) + sp.integrate(f, (x, int(m.group(2)), int(m.group(4))))
                    check(sp.nsimplify(it['answer']) == true, f'{tag}: key {it["answer"]} vs {true}')
                    F0 = sp.integrate(f, x)
                    named = {'no-constant': F0.subs(x, int(m.group(4))), 'no-divide': int(m.group(3)) + (sp.degree(f, x) + 1) * sp.integrate(f, (x, int(m.group(2)), int(m.group(4))))}
                    for wv in it['wrong']:
                        check(sp.nsimplify(wv['value']) == named[wv['id']] and wv['value'] != it['answer'], f'{tag}: slip {wv["id"]} = {wv["value"]} vs {named[wv["id"]]}')
                    continue
                m = re.search(r'\\int(?:_\{(-?[\d.]+)\}\^\{(-?[\d.]+)\})?\s*(.+?)\\,d([xt])', pr)
                check(m is not None, f'{tag}: prompt not read: {pr}')
                if not m:
                    continue
                var = m.group(4)
                f, v = tex_to_sympy(m.group(3), var)
                if it['kind'] == 'expression':
                    F, _ = tex_to_sympy(it['answer'], var)
                    check(sp.simplify(sp.diff(F, v) - f) == 0, f'{tag}: d/d{var} of the key is not the integrand ({pr})')
                    for wv in it['wrong']:
                        Fw, _ = tex_to_sympy(wv['tex'], var)
                        check(sp.simplify(sp.diff(Fw, v) - f) != 0, f'{tag}: wrong form {wv["id"]} is a correct antiderivative')
                    for line in it['solution']:
                        mm = re.search(r'^So (?:the answer is )?\$(?:uv - \\int v\\,du = )?(.+?) \+ C\$', line) or re.search(r'^Put \$u\$ back: \$(.+?) \+ C\$', line) or re.search(r'so the answer is \$(.+?) \+ C\$', line)
                        if mm and '\\int' not in mm.group(1):
                            Fs, _ = tex_to_sympy(mm.group(1), var)
                            check(sp.simplify(sp.diff(Fs, v) - f) == 0, f'{tag}: solution line ends on a form that is not an antiderivative: {line}')
                else:
                    a, b = sp.nsimplify(m.group(1)), sp.nsimplify(m.group(2))
                    vv = sp.Symbol(var)
                    fr = f.subs(v, vv)
                    true = float(sp.integrate(fr, (vv, a, b)))
                    t = it['tol']['abs']
                    check(close(it['answer'], true, max(t, 1e-9)), f'{tag}: key {it["answer"]} vs {true}')
                    for wv in it['wrong']:
                        check(abs(wv['value'] - true) > 2 * t + 1e-9, f'{tag}: slip {wv["id"]} = {wv["value"]} sits inside the key band ({true})')
                    F0 = sp.integrate(fr, vv)
                    named = {'limits-swapped': -true, 'sign-lost': -true, 'lower-limit-zero': float(F0.subs(vv, b))}
                    if fam == 'reciprocal-square':
                        named['power-lowered'] = float((sp.integrate(fr * vv ** 2, vv) / vv ** 2 * 0 + (fr * vv ** 2) * vv ** -3 / -3).subs(vv, b) - ((fr * vv ** 2) * vv ** -3 / -3).subs(vv, a))
                    if fam == 'definite-power':
                        named['limits-kept'] = None
                    for wv in it['wrong']:
                        if named.get(wv['id']) is not None:
                            check(close(wv['value'], named[wv['id']], 1e-6), f'{tag}: slip {wv["id"]} = {wv["value"]} vs the named mistake {named[wv["id"]]}')
                    acc = it.get('accept') or ''
                    mm = re.search(r'\\approx\s*(-?[\d.]+)', acc)
                    if mm:
                        check(close(float(mm.group(1).rstrip('.')), it['answer'], t), f'{tag}: accept line prints {mm.group(1)}, refused by tol {t}')
                    mm = re.match(r'\$(.+?)\$, or a decimal', acc)
                    if mm:
                        fr_, _ = tex_to_sympy(mm.group(1), 'x')
                        check(close(float(fr_), true, 1e-9), f'{tag}: accept line fraction {mm.group(1)} is not the value {true}')
    check(drawn >= 16 * 60, f'E drew {drawn} fluency items')
    print(f'E fluency items checked: {drawn}')


fluency()

print(f'{N[0]} checks, {len(FAILS)} failed, {len(KNOWN)} failed as known findings of this audit')
sys.exit(1 if FAILS or (KNOWN and not ALLOW_KNOWN) else 0)
