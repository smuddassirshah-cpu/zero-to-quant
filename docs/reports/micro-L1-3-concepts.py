#!/usr/bin/env python3
"""Concept checks for micro (topic 1.7), levels 1 to 3 (blind concept audit, 12 Nov 2026).

Run from the repo root: python3 -I docs/reports/micro-L1-3-concepts.py
Exit 0 when every check passes. A check that encodes a content claim the audit
found wrong or imprecise is named "FINDING n" and stays failing until the
content is fixed (brief step 4). Each FINDING check is tied to the wording it
tests: it passes once the sentence is reworded.

What it does
- Recomputes every numeric key and every numeric wrong[] value by the route its
  feedback names (KEYS), every table cell (TABLES), and proves coverage: a
  numeric widget or wrong id that is not in the registry fails the run.
- Runs every Python code widget: the solution passes all hidden tests and the
  untouched starter fails at least one.
- Checks the two expression widgets with sympy.
- Simulates the empirical and model claims (seeded): queue wait, the
  market-or-limit model, the race between the two best levels, microprice
  against mid as a forecast, the arrival-rate profit hump, the inventory skew,
  the Glosten-Milgrom update and zero-profit spread, the tilted-noise quotes of
  the performance task, the timing-risk figure of homework 2.
"""
import contextlib
import io
import json
import math
import pathlib
import random
import sys

import numpy as np
import sympy as sp

ROOT = pathlib.Path(__file__).resolve().parents[2]
COURSE = ROOT / 'app' / 'content' / 'courses' / 'micro'
DOCS = {p.stem: json.loads(p.read_text(encoding='utf-8')) for p in COURSE.glob('*.json') if p.stem != 'course'}
SHORT = {}
for stem in DOCS:
    k = stem.split('-')[0] if stem[0] == 'l' else stem.replace('review-', 'r').replace('homework-', 'h')
    SHORT[k] = stem
FAILS, COUNT = [], [0]


def check(name, ok):
    COUNT[0] += 1
    if not ok:
        FAILS.append(name)
        print('FAIL', name)


def node(f, loc):
    d = DOCS[SHORT[f]]
    kind = {'s': 'screens', 'q': 'quiz', 'i': 'items'}[loc[0]]
    return d[kind][int(loc[1:])]


def strings(x):
    if isinstance(x, str):
        return [x]
    if isinstance(x, dict):
        return [s for v in x.values() for s in strings(v)]
    if isinstance(x, list):
        return [s for v in x for s in strings(v)]
    return []


def text(f, loc=None):
    return '\n'.join(strings(node(f, loc) if loc else DOCS[SHORT[f]]))


def stated(f, loc, phrase, ok, label=None):
    """The phrase must be in the text and the claim true."""
    t = text(f, loc)
    check(label or f'{f} {loc} states "{phrase}"', phrase in t and ok)


def finding(n, f, loc, phrase, ok, label):
    """Fails while the phrase is in the text and the claim is false; passes once reworded."""
    present = phrase in text(f, loc)
    check(f'FINDING {n}: {f} {loc} {label}', (not present) or ok)


def tol_of(t, v):
    if not t:
        return 1e-9
    return max(t.get('abs', 0), abs(v) * t.get('rel', 0), 1e-9)


# ---------------------------------------------------------------- registry
A, B = 100.10, 100.14          # the course's standard touch
e = math.exp
KEYS = {
    # level 1 ------------------------------------------------------------
    ('l1', 's3'): ((B - A) * 100, {'lowest-bid': (B - 100.08) * 100, 'widest': (100.16 - 100.08) * 100, 'pounds': B - A}),
    ('l1', 's4'): ((A + B) / 2, {'half-spread': (B - A) / 2, 'sum': A + B, 'bid': A, 'ask': B}),
    ('l1', 's5'): ((B - A) / 100.12 * 1e4, {'percent': (B - A) / 100.12 * 100, 'fraction': (B - A) / 100.12, 'ten-times': (B - A) / 100.12 * 1e5}),
    ('l1', 's10'): (10000 / 10 * 0.06, {'per-pound': 10000 * 0.06, 'large': 10000 / 100 * 0.02, 'pence': 100 * 0.06}),
    ('l1', 'q0'): ((54.20 + 54.26) / 2, {'half': 0.03, 'spread': 0.06}),
    ('l1', 'q1'): (0.04 / 20 * 1e4, {'pence': 4, 'percent': 0.04 / 20 * 100}),
    ('l2', 's3'): (150238 / 1500, {'unweighted': (100.14 + 100.16 + 100.18) / 3, 'best': 100.14, 'last': 100.18}),
    ('l2', 's4'): ((150238 / 1500 - 100.14) * 100, {'last-level': (100.18 - 100.14) * 100, 'pounds': 150238 / 1500 - 100.14, 'total': 150238 - 1500 * 100.14}),
    ('l2', 's5'): (150238 - 1500 * 100.12, {'best-ask': 150238 - 1500 * 100.14, 'half-only': 1500 * 0.02, 'per-share': 150238 / 1500 - 100.12}),
    ('l2', 's10'): (2000 * .05 + 3000 * .10 + 3000 * .20 + 2000 * .40, {'half-spread': 10000 * .05, 'liquid': 10000 * .01, 'worst': 10000 * .40}),
    ('l2', 'q0'): (100.14, {'two-levels': (100.14 + 100.16) / 2}),
    ('l2', 'q1'): ((400 * 50 + 600 * 49.98) / 1000, {'unweighted': (50 + 49.98) / 2, 'best': 50.0}),
    ('l2', 'q2'): ((50 - 49.988) * 100, {'level-gap': (50 - 49.98) * 100, 'total': 1000 * (50 - 49.988)}),
    ('l3', 's2'): (300 + 600 + 400, {'next': 0, 'own': 200, 'with-own': 1500}),
    ('l3', 's3'): (300 + 400, {'unchanged': 1300, 'only-b': 600}),
    ('l3', 's6'): (100.14, {'limit': 100.20, 'bid': 100.10}),
    ('l3', 's8'): (20000 / 2000, {'inverse': 2000 / 20000, 'next': 1}),
    ('l3', 'q0'): (1200 - 1000, {'all': 500, 'none': 0, 'prorata': 1200 * 500 / 3500}),
    ('l3', 'q2'): (100.10, {'limit': 100.05}),
    ('l3', 'q3'): ((9000 - 3000) / 1500, {'no-cancel': 9000 / 1500}),
    ('l4', 's3'): (0.3 * -2 + 0.7 * 3, {'old': 0.6 * -2 + 0.4 * 3, 'fill-only': 0.3 * -2, 'miss-only': 0.7 * 3}),
    ('l4', 's4'): (1 / 5, {'half': 0.5, 'bid-chance': 0.6, 'third': 1 / 3}),
    ('l4', 'q0'): (0.8 * -2 + 0.2 * 3, {'fill-only': 0.8 * -2, 'sign': -(0.8 * -2 + 0.2 * 3)}),
    ('l4', 'q2'): (2 / (2 * 5 + 2), {'h-c': 2 / (5 + 2), 'over-h': 2 / 5}),
    ('r1', 'i1'): (0.04 / 7.50 * 1e4, {'pence': 4, 'bid': 0.04 / 7.48 * 1e4, 'percent': 0.04 / 7.50 * 100}),
    ('r1', 'i2'): (16010 / 800, {'unweighted': 20.01, 'best': 20.0}),
    ('r1', 'i3'): (16010 - 800 * 19.99, {'best-ask': 16010 - 800 * 20.0, 'half': 800 * 0.01}),
    ('r1', 'i4'): (1500 - 600, {'unchanged': 1500, 'filled': 0}),
    ('r1', 'i6'): (0.7 * -3 + 0.3 * 4, {'sign': 0.9, 'fill-only': 0.7 * -3, 'full-spread': -3}),
    ('r1', 'i7'): (900 - 400 - 300, {'all-fill': 0, 'none': 900, 'market': 300}),
    ('h1', 'i0'): (0.04 / 12.48 * 1e4, {'pence': 4, 'bid': 0.04 / 12.46 * 1e4, 'percent': 0.04 / 12.48 * 100, 'ask': 0.04 / 12.50 * 1e4}),
    ('h1', 'i1'): (2500 * 250.43 - 625880, {'best-bid': 2500 * 250.40 - 625880, 'half': 2500 * 0.03, 'all-levels': 3000 * 250.43 - (800 * 250.40 + 1000 * 250.35 + 1200 * 250.30)}),
    # h1 i3: 'no-rest' is FINDING 7 (its route gives 6, the value is 2); the registry holds the value's true route (rest at the fill price, 100.16 - 100.14)
    ('h1', 'i3'): ((100.16 - 100.15) * 100, {'old': 4, 'walked': (100.16 - 100.10) * 100, 'no-rest': (100.16 - 100.14) * 100}),
    ('h1', 'i4'): ((12000 - 4000) / 1600, {'no-cancel': 12000 / 1600, 'added': 16000 / 1600}),
    # level 2 ------------------------------------------------------------
    ('l5', 's1'): (100 * (B - A), {'half': 100 * 0.02, 'per-share': B - A, 'zero': 0, 'pence': 100 * (B - A) * 100}),
    ('l5', 's2'): (0.02 / 100.12 * 1e4, {'full': 0.04 / 100.12 * 1e4, 'percent': 0.02 / 100.12 * 100}),
    ('l5', 's3'): (50000 * 0.04 / 100.12, {'once': 50000 * 0.02 / 100.12, 'percent': 50000 * 0.04, 'per-share': 0.04}),
    ('l5', 's8'): (3 - 4, {'ignored': 3, 'half': 3 - 2, 'double': 3 - 2 * 4, 'added': 3 + 4}),
    ('l5', 's9'): (50000 * 0.0005 * 252, {'once': 25000 * 0.0005 * 252, 'full': 50000 * 0.0010 * 252, 'day': 50000 * 0.0005}),
    ('l5', 'q1'): (20000 * 0.04 / 5.00, {'once': 20000 * 0.02 / 5.00, 'pence': 20000 * 0.04}),
    ('l5', 'q2'): (0.10 / 200 * 1e4, {'full': 0.20 / 200 * 1e4, 'pence': 20}),
    ('l6', 's0'): ((1000 * 10.01 + 1500 * 10.02) / 2500, {'top': 10.01, 'simple': (10.01 + 10.02) / 2, 'last': 10.02}),
    ('l6', 's2'): ((1000 * 1 + 1500 * 2 + 2000 * 3) / 100, {'top': 4500 * 1 / 100, 'last': 4500 * 3 / 100, 'pence': 10000}),
    ('l6', 's3'): (0.01 / 10 * 1e4, {'none': 0, 'full': 0.02 / 10 * 1e4, 'pence': 1}),
    ('l6', 's4'): (0.02 * math.sqrt(0.01) * 1e4, {'no-root': 0.02 * 0.01 * 1e4, 'root-of-one': 0.02 * math.sqrt(1) * 1e4, 'percent': 0.02 * math.sqrt(0.01) * 100}),
    ('l6', 's6'): ((10.03 - 10.00) * 100, {'all': 6, 'none': 0}),
    ('l6', 's9'): (4000 * .02 + 3000 * .05 + 3000 * .12, {'filled-only': 4000 * .02 + 3000 * .05, 'missed-only': 3000 * .12, 'all-close': 10000 * .12}),
    ('l6', 's10'): (0.02 * math.sqrt(0.1) * 5e6, {'linear': 20e-4 * 10 * 5e6, 'no-root': 0.02 * 0.1 * 5e6, 'bp': 0.02 * math.sqrt(0.1) * 1e4}),
    ('l6', 'q0'): ((500 * 20 + 500 * 20.02 + 500 * 20.05) / 1500, {'top': 20.0, 'all-third': (500 * 20 + 500 * 20.02 + 800 * 20.05) / 1800}),
    ('l6', 'q3'): (0.02 / 40 * 1e4, {'none': 0, 'full': 0.04 / 40 * 1e4}),
    ('l7', 's2'): ((B * 5000 + A * 1000) / 6000, {'mid': 100.12, 'same-side': (A * 5000 + B * 1000) / 6000}),
    ('l7', 's3'): (1000 / 500, {'bid': 5000 / 500, 'both': 6000 / 500}),
    ('l7', 's4'): (100.12, {'bid': A, 'ask': B}),
    ('l7', 's5'): (4000 / 6000, {'reversed': -4000 / 6000, 'no-divide': 4000, 'ratio': 5}),
    ('l7', 'q0'): ((50.04 * 2000 + 50.00 * 6000) / 8000, {'mid': 50.02, 'own': (50.00 * 2000 + 50.04 * 6000) / 8000}),
    ('l8', 's1'): ((300 * .5 + 400 * 4.5 + 1300 * 9.5) / 100, {'spread': 2000 * .5 / 100, 'top-level': 300 * .5 / 100, 'pence': 14300}),
    ('l8', 's2'): (300 + 400, {'top': 300, 'all': 2700, 'both-sides': 700 + 300 + 200}),
    ('l8', 's4'): (1.2 / 30, {'negative': -1.2 / 30, 'inverse': 30 / 1.2, 'times': 1.2 * 30, 'decimal': 0.012 / 30}),
    ('l8', 's6'): (500000 * (12 - 3.2) / 1e4, {'half': 500000 * 4.4 / 1e4, 'open-only': 500000 * 12 / 1e4, 'bp': 8.8}),
    ('l8', 's7'): (1e6 * 40 / 1e4, {'calm': 1e6 * 4 / 1e4, 'half': 1e6 * 20 / 1e4}),
    ('l8', 's9'): (3 * 0.1 * 8, {'one-day': 0.8, 'no-p': 3 * 8, 'divide': 0.8 / 3}),
    ('l8', 'q1'): (0.6 / 15, {'negative': -0.04, 'inverse': 15 / 0.6, 'decimal': 0.006 / 15}),
    ('l8', 'q2'): (20 / (0.1 * 50), {'no-p': 20 / 50, 'times': 20 * 0.1 * 50}),
    ('r2', 'i0'): (25000 * 0.06 / 30, {'once': 25000 * 0.03 / 30, 'percent': 25000 * 0.20}),
    ('r2', 'i1'): ((20.02 * 800 + 20.00 * 3200) / 4000, {'mid': 20.01, 'own': (20.00 * 800 + 20.02 * 3200) / 4000}),
    ('r2', 'i2'): ((2000 * 2 + 3000 * 3 + 1000 * 5) / 6000 / 5000 * 1e4, {'top': 2 / 5000 * 1e4, 'last': 5 / 5000 * 1e4, 'simple': (2 + 3 + 5) / 3 / 5000 * 1e4}),
    ('r2', 'i3'): (0.015 * math.sqrt(0.04) * 2e6, {'no-root': 0.015 * 0.04 * 2e6, 'bp': 30}),
    ('r2', 'i4'): (5 * 8, {'once': 5 * 4, 'double': 5 * 2 * 8}),
    ('r2', 'i7'): (12 / (0.2 * 20), {'no-p': 12 / 20, 'ten': 12 / (0.1 * 20)}),
    ('r2', 'i8'): (3000 * 0.06 + 2000 * (39.90 - 40.00), {'filled-only': 180, 'sign': 180 + 200, 'sign2': 200 - 180}),
    ('h2', 'i3'): ((10000 * .03 + 15000 * .06 + 15000 * .20) / 1e6 * 1e4, {'filled-only': 1200 / (25000 * 25) * 1e4, 'fills-on-paper': 1200 / 1e6 * 1e4}),
    # level 3 ------------------------------------------------------------
    ('l9', 's1'): (100 * (5.02 - 4.98), {'one-side': 100 * 0.02, 'per-share': 0.04, 'half': 0.02}),
    ('l9', 's3'): (2 * 3 * 10 * e(-1.5), {'one-side': 3 * 10 * e(-1.5), 'full-spread': 2 * 6 * 10 * e(-1.5), 'per-share': 2 * 3 * 10 * e(-1.5) / 100, 'no-fall': 2 * 3 * 10}),
    ('l9', 's4'): (0, {'trades': 20, 'ten': 10}),
    ('l9', 's10'): (10000 * 1000 * 0.01, {'half': 10000 * 1000 * 0.005, 'no-shares': 10000 * 0.01, 'pence': 10000 * 1000}),
    ('l9', 'q0'): (500 * 0.06, {'one-side': 500 * 0.03, 'per-share': 0.06}),
    ('l9', 'q1'): (200 * 0.02, {'spread': 200 * 0.04, 'zero': 0}),
    ('l9', 'q3'): (2 * 1 * 10 * e(-0.5), {'one-side': 10 * e(-0.5), 'no-fall': 2 * 1 * 10}),
    ('l10', 's2'): (500 - 3 + 2, {'wrong-way': 500 + 3 + 2, 'no-skew': 502, 'mid': 497, 'bid': 495}),
    ('l10', 's3'): (500 + 2 - 2, {'wrong-way': 500 - 2 - 2, 'no-skew': 498, 'mid': 502}),
    ('l10', 's5'): (1400 * 5 / 100, {'lots': 14 * 5 / 100, 'pence': 7000, 'skewed': 0}),
    ('l10', 'q0'): (800 - 4 + 3, {'wrong-way': 800 + 4 + 3, 'no-skew': 803, 'gamma1': 800 - 2 + 3}),
    ('l10', 'q3'): (9, {'three': 3}),
    ('l11', 's0'): ((502 - 510) * 100 / 100, {'spread': (502 - 500) * 100 / 100, 'loss-sign': 8, 'per-share': -0.08}),
    ('l11', 's3'): (0.3 / 0.5, {'prior': 0.5, 'alpha': 0.2, 'joint': 0.3}),
    ('l11', 's4'): (0.6 * 510 + 0.4 * 490, {'prior': 500, 'high': 510, 'swapped': 0.4 * 510 + 0.6 * 490}),
    ('l11', 's7'): (0.2 * 30, {'old': 0.2 * 10, 'delta': 30}),
    ('l11', 'q0'): (0, {'delta': 10}),
    ('l11', 'q1'): (0.1 * 20, {'delta': 20, 'half': 1}),
    ('l11', 'q2'): (0.4 * 510 + 0.6 * 490, {'prior': 500, 'up': 502, 'low': 490}),
    ('l12', 's2'): (1500 - 1200, {'all': 1500, 'sell': 1200, 'zero': 0}),
    ('l12', 's4'): (250, {'p251': 251, 'p249': 249, 'mid': 252}),
    ('l12', 's6'): (20000 * 0.01, {'full': 20000 * 0.02, 'per-share': 0.01, 'pence': 20000}),
    ('l12', 'q1'): (101, {'p102': 102, 'p100': 100}),
    ('l12', 'q3'): ((12.40 + 12.44) / 2, {'ask': 12.44, 'bid': 12.40}),
    ('r3', 'i0'): (2000 * 0.02, {'one-side': 2000 * 0.01, 'per-share': 0.02}),
    ('r3', 'i1'): (1200 + 0.5 * 4 - 3, {'wrong-way': 1200 - 2 - 3, 'no-skew': 1197, 'gamma1': 1200 + 4 - 3}),
    ('r3', 'i3'): (102, {'p101': 101, 'p103': 103}),
    ('r3', 'i4'): (3, {'k': 1 / 3, 'lam': 6}),
    ('r3', 'i5'): (490 + 20 * 0.36 / 0.52, {'one-buy': 502, 'added': 504, 'prior': 500}),
    ('r3', 'i6'): (5000 * 0.03, {'full': 5000 * 0.06, 'per-share': 0.03}),
    ('r3', 'i7'): (4 / 2, {'one': 1, 'four': 4}),
    ('r3', 'i8'): (2 - 0.3 * 10, {'spread': 2, 'sign': 1, 'full': 4}),
    ('h3', 'i0'): (2 * 4 * 20 * e(-1), {'one-side': 4 * 20 * e(-1), 'no-fall': 2 * 4 * 20, 'old-k': 2 * 2 * 20 * e(-0.5)}),
    ('h3', 'i2'): (2000 - 9 + 4, {'bid': 2000 - 9 - 4, 'no-skew': 2004, 'wrong-way': 2000 + 9 + 4, 'mid': 1991}),
    ('h3', 'i3'): (490 + 20 * 0.216 / 0.280, {'linear': 506, 'two': 490 + 20 * 9 / 13, 'one': 502}),
    ('h3', 'i5'): (502, {'same': 501, 'p503': 503}),
}
TABLES = {
    ('l2', 's2'): [500, 500 * 100.14, 600, 600 * 100.16, 400, 400 * 100.18],
    ('l4', 's2'): [2, 3, 0.6 * -2 + 0.4 * 3],
    ('l5', 's5'): [0.04 / 100.12 * 1e4, 0.04 / 100.12 * 1e4, 40, 40, 8, 8],
    ('l10', 's9'): [1, 497, 501, 2, 496, 500, 1, 497, 501, 0, 498, 502, -1, 499, 503],
    ('l12', 's3'): [500, 2000, 800, 1400, 1200, 1000, 1800, 500, 2000, 200],
    ('h2', 'i0'): [2e6 * 3e-4, 0.02 * math.sqrt(2 / 50) * 2e6, 2e6 * 3e-4 + 0.02 * 0.2 * 2e6],
    ('h2', 'i4'): [6, 72 / 6 + 12],
}


def all_widgets():
    for f, stem in SHORT.items():
        d = DOCS[stem]
        for kind, pre in (('screens', 's'), ('quiz', 'q'), ('items', 'i')):
            for i, n in enumerate(d.get(kind, [])):
                if 'widget' in n:
                    yield f, f'{pre}{i}', n['widget']


for f, loc, w in all_widgets():
    if w['kind'] == 'numeric':
        reg = KEYS.get((f, loc))
        check(f'coverage: {f} {loc} numeric key is in the registry', reg is not None)
        if reg is None:
            continue
        ans, routes = reg
        label = f'{f} {loc} key {w["answer"]} = recomputed {ans:.6g}'
        if (f, loc) == ('l6', 'q0'):
            label = f'FINDING 8: l6 q0 key {w["answer"]} is not 30,035 / 1,500 = {ans:.4f}'
        check(label, abs(w['answer'] - ans) <= tol_of(w.get('tol'), ans) + 1e-12)
        ids = {x['id'] for x in w.get('wrong', [])}
        check(f'coverage: {f} {loc} wrong ids match the registry', ids == set(routes))
        for x in w.get('wrong', []):
            if x['id'] in routes:
                r = routes[x['id']]
                check(f'{f} {loc} wrong {x["id"]} {x["value"]} = route {r:.6g}', abs(x['value'] - r) <= tol_of(x.get('tol'), x['value']) + 1e-12)
                check(f'{f} {loc} wrong {x["id"]} lies outside the key tolerance', abs(x['value'] - w['answer']) > tol_of(w.get('tol'), w['answer']) + tol_of(x.get('tol'), x['value']) - 1e-12 or x['value'] != w['answer'])
    elif w['kind'] == 'table':
        cells = [c for row in w['rows'] for c in row if isinstance(c, dict) and 'answer' in c]
        if cells and all(isinstance(c['answer'], (int, float)) for c in cells):
            reg = TABLES.get((f, loc))
            check(f'coverage: {f} {loc} table is in the registry', reg is not None and len(reg) == len(cells))
            if reg and len(reg) == len(cells):
                for j, (c, r) in enumerate(zip(cells, reg)):
                    check(f'{f} {loc} table cell {j} {c["answer"]} = {r:.6g}', abs(c['answer'] - r) <= tol_of(c.get('tol'), r) + 1e-12)
    elif w['kind'] == 'slider':
        check(f'coverage: {f} {loc} slider is l6 s7', (f, loc) == ('l6', 's7'))

# FINDING 7: homework-1 h-limit-through, slip no-rest. Its feedback route (drop the unfilled 500) leaves bid 100.10, ask 100.16.
route_no_rest = round((100.16 - 100.10) * 100)
w = node('h1', 'i3')['widget']
val = [x['value'] for x in w['wrong'] if x['id'] == 'no-rest'][0]
finding(7, 'h1', 'i3', 'You dropped the unfilled 500 shares', route_no_rest == val, f'slip no-rest: "dropped the unfilled 500" gives {route_no_rest}p, the value is {val}p')

# ---------------------------------------------------------------- level 1: books and walks
BOOK2 = [(100.14, 500), (100.16, 600), (100.18, 700)]


def walk(levels, size):
    left, cost = size, 0.0
    for p, q in levels:
        t = min(left, q)
        cost += t * p
        left -= t
        if left == 0:
            return cost
    raise ValueError


stated('l2', 's1', '100.1622', abs(walk(BOOK2, 1800) / 1800 - 100.1622) < 5e-5)
stated('l2', 's2', '150,238', abs(walk(BOOK2, 1500) - 150238) < 1e-6)
stated('l2', 's5', '3.9 bp', abs(58 / 150180 * 1e4 - 3.9) < 0.05)
stated('l2', 's7', '100.1433', abs(walk(BOOK2, 600) / 600 - 100.1433) < 5e-5)
stated('l2', 's7', '0.67p', abs((100.15 - walk(BOOK2, 600) / 600) * 100 - 0.67) < 0.005)
thin = [(100.05, 2000), (100.10, 3000), (100.20, 3000), (100.40, 4000)]
stated('l2', 's10', '1,001,800', abs(walk(thin, 10000) - 1001800) < 1e-6)
stated('l2', 's10', '18 bp against 1 bp', abs(1800 / 1e6 * 1e4 - 18) < 1e-9 and abs(100 / 1e6 * 1e4 - 1) < 1e-9)
stated('l2', 'q3', 'saving £28', abs(walk(BOOK2, 1500) - 1500 * 100.14 - 28) < 1e-6)
stated('l1', 's8', '20', abs(0.10 / 50.05 * 1e4 - 20) < 0.05, 'l1 s8 explain: 10p on 50.05 is about 20 bp')
stated('l1', 's10', 'thirty times', 60 / 2 == 30)
stated('r1', 'i1', 'more than 13 times', 53.33 / 4 > 13)
stated('r1', 'i7', '200 rest at £20.00', 900 - 400 - 300 == 200)
stated('h1', 'i1', '250.352', abs(625880 / 2500 - 250.352) < 5e-4)
# homework 1 longform
la = [(20.02, 10000), (20.03, 15000), (20.05, 20000), (20.08, 25000)]
stated('h1', 'i8', '1,202,850', abs(walk(la, 60000) - 1202850) < 1e-6)
stated('h1', 'i8', '20.0475', abs(walk(la, 60000) / 60000 - 20.0475) < 1e-9)
stated('h1', 'i8', '23.75 bp', abs(2850 / 1.2e6 * 1e4 - 23.75) < 1e-9)
stated('h1', 'i8', 'more than twice the sliced cost', 2850 / 1200 > 2)
stated('h1', 'i8', '1{,}800', 60000 * 0.03 == 1800)
stated('h1', 'i7', '1/(4 + 1 - 2) = 1/3', abs(1 / (2 * 2 + 1 - 2) - 1 / 3) < 1e-12)

# l3 queue wait n ~ Q/v: trades of random size, mean v
rng = np.random.default_rng(7)
counts = []
for _ in range(20000):
    tot, n = 0.0, 0
    while tot < 20000:
        tot += rng.exponential(2000)
        n += 1
    counts.append(n - 1)                      # whole trades that pass before the one that reaches you
check('sim l3 s7/s8: trades before the first fill average about Q/v = 10', abs(np.mean(counts) - 10) < 0.2)

# l4 market-or-limit model, by formula on the slider grid and by simulation


def limit_cost(p, h=2, c=1):
    return -p * h + (1 - p) * (h + c)


grid = {k: (max(0, 1 - 0.1 * k)) * (2 - k) + (1 - max(0, 1 - 0.1 * k)) * 3 for k in range(0, 11)}
best = min(grid.values())
check('l4 s1: slider minimum is 0p at 100.10 and 100.09', abs(best) < 1e-12 and [k for k, v in grid.items() if abs(v - best) < 1e-12] == [4, 5])
stated('l4', 's1', '1.2p at £100.06', abs(grid[8] - 1.2) < 1e-12)
stated('l4', 's1', '3.0p at £100.04', abs(grid[10] - 3.0) < 1e-12)
rng = np.random.default_rng(11)
for p, miss, want in ((0.6, 3, 0.0), (0.3, 3, 1.5), (0.5, 8, 3.0), (0.2, 3, 2.0)):
    fills = rng.random(400000) < p
    sim = np.where(fills, -2, miss).mean()
    check(f'sim l4: limit cost at p={p}, miss {miss}p is {want}p', abs(sim - want) < 0.03)
h_, c_, p_ = sp.symbols('h c p', positive=True)
sol = sp.solve(sp.Eq(-p_ * h_ + (1 - p_) * (h_ + c_), h_), p_)
check('l4 s8: break-even p = c/(2h + c)', sp.simplify(sol[0] - c_ / (2 * h_ + c_)) == 0)
a_ = sp.symbols('a', positive=True)
sol = sp.solve(sp.Eq(p_ * (a_ - h_) + (1 - p_) * (h_ + c_), h_), p_)
check('h1 i7: with adverse selection p = c/(2h + c - a)', sp.simplify(sol[0] - c_ / (2 * h_ + c_ - a_)) == 0)
# expression widgets
exp_w = node('h1', 'i6')['widget']
target = -p_ * h_ + (1 - p_) * (h_ + c_)
for s_ in ['h + c - 2*p*h - p*c', 'c+h-2*h*p-c*p', 'h+c-p*(2*h+c)']:
    check(f'h1 i6 accepted form {s_} equals E[limit]', sp.simplify(sp.sympify(s_, locals={'h': h_, 'c': c_, 'p': p_}) - target) == 0)
check('h1 i6 wrong forms differ', sp.simplify((c_ - p_ * h_ - p_ * c_) - target) != 0 and sp.simplify((h_ + c_) - target) != 0)
aa, bb, qa = sp.symbols('a b Q', positive=True)
mp = (aa * 3 * qa + bb * qa) / (qa + 3 * qa)
check('h2 i2 microprice with Qb = 3Qa is (3a + b)/4', sp.simplify(mp - (3 * aa + bb) / 4) == 0)

# ---------------------------------------------------------------- level 2
stated('l5', 's3', '499', round(50000 / 100.12) == 499)
stated('l5', 's7', '60', 3 * 2 * 10 == 60)
stated('l5', 's9', '0.63%', abs(6300 / 1e6 - 0.0063) < 1e-12)
stated('l5', 'q3', '2.5 bp', abs(0.005 / 20.005 * 1e4 - 2.5) < 0.005)
stated('l5', 's8', '4.0 bp', abs(0.01 / 25.005 * 1e4 - 4.0) < 0.005)
# l6
curve = lambda x: 10 * (min(x, 1) + 2 * max(0, min(x, 2.5) - 1) + 3 * max(0, min(x, 4.5) - 2.5) + 4 * max(0, min(x, 7) - 4.5) + 5 * max(0, min(x, 10) - 7)) / x
check('l6 s1: the book curve gives 10 bp at 1,000 and 35 bp at 10,000', abs(curve(1) - 10) < 1e-9 and abs(curve(10) - 35) < 1e-9)
stated('l6', 's2', '22 bp', abs(100 / 45000 * 1e4 - 22) < 0.3)
stated('l6', 's5', 'eight times the £', abs(4 * 2 - 8) < 1e-12 and abs(4 ** 1.5 - 8) < 1e-12)
tot = {n: 50 / n + 2 * n for n in range(1, 13)}
check('l6 s7: 50/n + 2n is smallest at n = 5 (20 bp)', min(tot, key=tot.get) == 5 and abs(tot[5] - 20) < 1e-12 and node('l6', 's7')['widget']['answer'] == 5)
stated('l6', 's7', '52 bp for one block', tot[1] == 52)
stated('l6', 's9', '33 bp', abs(230 / 70000 * 1e4 - 33) < 0.5)
stated('l6', 's9', '59 bp', abs(590 / 1e5 * 1e4 - 59) < 1e-9)
finding(9, 'l6', 'q2', '30.5 bp', abs(3050 / 1e5 * 1e4 - 30.5) < 1e-9, f'£3,050 on £100,000 is {3050 / 1e5 * 1e4:.0f} bp, not 30.5 bp')
stated('l6', 'q0', '£30,035', 500 * 20 + 500 * 20.02 + 500 * 20.05 == 30035)
finding(8, 'l6', 'q0', '£20.030 each', abs(30035 / 1500 - 20.030) < 5e-4, f'explain: £30,035 / 1,500 is £{30035 / 1500:.4f}, not £20.030')
# FINDING 10: the slicing model contradicts the square-root rule two screens earlier unless it says so
sq = {n: 50 / math.sqrt(n) + 2 * n for n in range(1, 13)}
finding(10, 'l6', 's7', 'since smaller slices push less', abs(sq[5] - tot[5]) < 1, f'impact 50/n is not what the square-root rule gives for n slices (50/sqrt(n): {sq[5]:.1f} bp at n = 5 against {tot[5]:.0f})')
tot2 = {n: 72 / n + 2 * n for n in range(1, 20)}
check('h2 i4: 72/n + 2n is smallest at n = 6 (24 bp); 5 and 7 cost 24.4 and 24.3', min(tot2, key=tot2.get) == 6 and abs(tot2[5] - 24.4) < 1e-9 and abs(tot2[7] - 24.2857) < 1e-3)
# l7 microprice identity and lean
Qb_, Qa_, m_, s_sym = sp.symbols('Q_b Q_a m s', positive=True)
mu = ((m_ + s_sym / 2) * Qb_ + (m_ - s_sym / 2) * Qa_) / (Qa_ + Qb_)
check('l7 s7: microprice = m + I s/2', sp.simplify(mu - (m_ + (Qb_ - Qa_) / (Qa_ + Qb_) * s_sym / 2)) == 0)
stated('l7', 's10', '100.104', abs(100.12 - 0.8 * 0.02 - 100.104) < 1e-9)
stated('l7', 's3', '100.125', abs((100.10 + 100.15) / 2 - 100.125) < 1e-9)
cents = {'right': (100.11 + 100.15) / 2, 'mid': (100.10 + 100.14) / 2, 'far': (100.12 + 100.16) / 2, 'back': (100.09 + 100.13) / 2}
check('l7 s8: the 100.11/100.15 quote is centred closest to 100.1333', min(cents, key=lambda k: abs(cents[k] - 100.13333)) == 'right')


def race(qb, qa, rng, lot=100):
    """Equal-rate unit market orders; True if the ask empties first."""
    b, a = qb // lot, qa // lot
    while a > 0 and b > 0:
        if rng.random() < 0.5:
            a -= 1
        else:
            b -= 1
    return a == 0


rng = random.Random(5)
up = sum(race(5000, 1000, rng) for _ in range(20000)) / 20000
check('sim l7 s0: with equal flow the 1,000 ask empties before the 5,000 bid', up > 0.99)


def forecast_mse(width_ticks, rng, n=40000):
    """Random sizes at the touch, equal market-order flow, nobody adds; the next level sits one tick behind.
    Returns (mse of the mid, mse of the microprice) as forecasts of the next mid, in ticks squared."""
    em = eu = 0.0
    for _ in range(n):
        qb, qa = rng.randrange(1, 11), rng.randrange(1, 11)
        b, a = qb, qa
        while a > 0 and b > 0:
            if rng.random() < 0.5:
                a -= 1
            else:
                b -= 1
        move = 0.5 if a == 0 else -0.5           # the emptied side steps back one tick: the mid moves half a tick
        shift = (qb - qa) / (qb + qa) * width_ticks / 2
        em += move ** 2
        eu += (move - shift) ** 2
    return em / n, eu / n


rng = random.Random(21)
m1, u1 = forecast_mse(1, rng)
m4, u4 = forecast_mse(4, rng)
check('sim l7: in a book one tick wide the microprice beats the mid as a forecast of the next mid', u1 < m1)
# the lesson's own book: mid 100.12, microprice 100.1333, next mid 100.125
own_mid_err, own_mu_err = abs(100.125 - 100.12), abs(100.125 - 100.13333)
finding(11, 'l7', None, 'so the microprice predicts the next mid better than the mid does', u4 < m4 and own_mu_err < own_mid_err,
        f'unqualified claim: in the lesson\'s 4p-wide book the microprice misses the next mid by {own_mu_err * 100:.2f}p, the mid by {own_mid_err * 100:.2f}p (simulated MSE {u4:.3f} against {m4:.3f} ticks squared)')
# more stated figures
stated('l5', 'q1', '80 bp', abs(0.04 / 5 * 1e4 - 80) < 1e-9)
stated('l8', 's1', '1.5 bp', abs(30 / (2000 * 100.005) * 1e4 - 1.5) < 0.005)
stated('l8', 's6', '£600 against £160', 500000 * 12e-4 == 600 and abs(500000 * 3.2e-4 - 160) < 1e-9)
stated('r2', 'i2', '£180', 18000 / 100 == 180)
stated('h2', 'i3', '19 bp', abs(1200 / 625000 * 1e4 - 19.2) < 1e-9)
stated('l4', 'q3', '£40', 2000 * 0.02 == 40)
# FINDING 6: l4 q-urgent, 2,000 shares cannot hedge £500 a penny
finding(6, 'l4', 'q3', 'loses £500 for every 1p', 2000 * 0.01 == 500, f'a 2,000-share hedge offsets £{2000 * 0.01:.0f} per 1p, not £500 (that needs 50,000 shares)')
# l8
stated('l8', 's1', '7.1 bp', abs(143 / (2000 * 100.005) * 1e4 - 7.15) < 0.06)
x_cost = 0.02 * math.sqrt(1 / 5) * 1e4 + 1
y_cost = 0.02 * math.sqrt(1 / 200) * 1e4 + 3
check('l8 s3: X about 90 bp, Y about 17 bp', abs(x_cost - 90) < 1 and abs(y_cost - 17) < 0.5)
check('l8 s5: Amihud P 0.05, Q 0.025', abs(4 / 80 - 0.05) < 1e-12 and abs(1 / 40 - 0.025) < 1e-12)
stated('l8', 's9', '25 days', abs(20 / 0.8 - 25) < 1e-9)
stated('l8', 's8', '4$ days', abs(20 / (0.1 * 50) - 4) < 1e-9)
# FINDING 12: "adds little impact" at 10% of volume against the course's own rule
finding(12, 'l8', 's8', 'Then the order adds little impact', 0.02 * math.sqrt(0.1) * 1e4 < 10, f'10% of a day at sigma 2% costs {0.02 * math.sqrt(0.1) * 1e4:.0f} bp by the square-root rule of l6')
stated('r2', 'i5', '200 times', 3e6 / 15000 == 200)
stated('h2', 'i0', '43 bp', abs(8600 / 2e6 * 1e4 - 43) < 1e-9)
check('h2 i1: doubling Q multiplies sqrt-model cost by 2^1.5', abs(2 ** 1.5 - 2.83) < 0.005)
check('h2 i5: Amihud ranks R 0.020, S 0.030, T 0.060', (2 / 100, 0.6 / 20, 1.5 / 25) == (0.02, 0.03, 0.06))
# homework 2 longform
block = 0.018 * math.sqrt(10 / 40) * 10e6
three = 0.018 * math.sqrt(1 / 12) * 10e6
stated('h2', 'i8', '£90,000', abs(block - 90000) < 1e-6)
stated('h2', 'i8', '£52,000', abs(three - 52000) < 100)
stated('h2', 'i8', '£38,000', abs(block - three - 38000) < 100)
rng = np.random.default_rng(3)
r = rng.normal(0, 0.018, size=(400000, 2))
sd = (10e6 * (2 / 3 * r[:, 0] + 1 / 3 * r[:, 1])).std()
stated('h2', 'i8', '134{,}000', abs(sd - 134164) < 1500, 'sim h2 i8: timing-risk sd of the three-day plan is about £134,000')
stated('h2', 'i8', '24.994', abs(25.00 - 0.6 * 0.01 - 24.994) < 1e-9)
stated('h2', 'i6', '£94,000', abs(10e6 * (4e-4 + 0.018 * 0.5) - 94000) < 1e-6)

# ---------------------------------------------------------------- level 3
lam = lambda s, l0=10, k=0.5: l0 * e(-k * s)
for s_, txt in ((1, '12.13'), (2, '14.72'), (4, '10.83'), (10, '1.35')):
    stated('l9', 's2', txt, abs(2 * s_ * lam(s_) - float(txt)) < 0.006)
check('l9 s2 option whys: 1.35 and 0.07 trades a minute at 4p and 10p', abs(lam(4) - 1.35) < 0.005 and abs(lam(10) - 0.07) < 0.005)
s_s, k_s, l0_s = sp.symbols('s k lambda0', positive=True)
check('l9 s7: profit 2 s lam0 exp(-ks) peaks at s = 1/k', sp.solve(sp.diff(2 * s_s * l0_s * sp.exp(-k_s * s_s), s_s), s_s) == [1 / k_s])
rng = np.random.default_rng(9)
prof = {}
for s_ in (1, 2, 3, 4):
    minutes = 200000
    trades = rng.poisson(lam(s_), size=(minutes, 2)).sum(axis=1)
    prof[s_] = (trades * s_).mean()             # 100 shares at s pence is s pounds
check('sim l9: Poisson arrivals give 2 s lam(s) a minute and the hump peaks at 2p', all(abs(prof[s_] - 2 * s_ * lam(s_)) < 0.08 for s_ in prof) and max(prof, key=prof.get) == 2)
al_s, de_s = sp.symbols('alpha delta', positive=True)
check('h3 i1: with adverse selection the peak is alpha delta + 1/k', sp.solve(sp.diff(2 * l0_s * sp.exp(-k_s * s_s) * (s_s - al_s * de_s), s_s), s_s) == [al_s * de_s + 1 / k_s])
# l10 skew
check('l10 s1: moving down d pence makes a sale e^d times as likely', all(abs(lam(2 - d) / lam(2 + d) - e(d)) < 1e-9 for d in range(-4, 5)))
stated('l10', 's1', '7.39', abs(e(2) - 7.39) < 0.005)
stated('l10', 's1', 'about 55 times', abs(e(4) - 55) < 0.5)
ser = {s['id']: s['values'] for s in node('l10', 's5')['canvas']['params']['series']}
flat, skew = ser['flat'], ser['skew']
check('l10 s5 chart: both paths start at 0, move one lot a trade, 100 trades', len(flat) == len(skew) == 101 and all(abs(x - y) == 1 for v in (flat, skew) for x, y in zip(v, v[1:])))
check('l10 s5: the no-skew path ends at 14 and reaches 18', flat[-1] == 14 and max(map(abs, flat)) == 18)
check('l10 s5: the skewed path ends at 0 and stays within 3 lots', skew[-1] == 0 and max(map(abs, skew)) == 3)
rng = np.random.default_rng(3)
u = rng.random((20000, 100))
q0 = np.zeros(20000)
q1 = np.zeros(20000)
mx = np.zeros(20000)
for t in range(100):
    q0 += np.where(u[:, t] < 0.5, -1, 1)
    psale = 1 / (1 + np.exp(-q1))               # a sale is e^q times as likely as a purchase
    q1 += np.where(u[:, t] < psale, -1, 1)
    mx = np.maximum(mx, np.abs(q1))
check('sim l10 s5: without a skew inventory is a random walk (sd 10 after 100 trades)', abs(q0.std() - 10) < 0.3)
check('sim l10 s5: with the e^q skew inventory stays near zero (sd under 1.3; beyond 3 lots in under 15% of runs)', q1.std() < 1.3 and (mx > 3).mean() < 0.15)
stated('l10', 's10', '£200', abs(0.02 * 2000 * 5.00 - 200) < 1e-9)
# l11 Glosten-Milgrom


def gm(alpha, delta, n, rng, beta=0.5):
    high = rng.random(n) < 0.5
    informed = rng.random(n) < alpha
    buys = np.where(informed, high, rng.random(n) < beta)
    d = np.where(high, delta, -delta)
    return high, informed, buys, d


rng = np.random.default_rng(1)
high, informed, buys, d = gm(0.2, 10, 2_000_000, rng)
check('sim l11 s2: P(informed | buy) = alpha = 0.2', abs(informed[buys].mean() - 0.2) < 0.002)
check('sim l11 s3: P(510 | buy) = 0.6', abs(high[buys].mean() - 0.6) < 0.002)
check('sim l11 s4: E[V | buy] = 502', abs(500 + d[buys].mean() - 502) < 0.03)
check('sim l11 q2: E[V | sell] = 498', abs(500 + d[~buys].mean() - 498) < 0.03)
check('sim l11 s5: a 2p half-spread earns 0 on an average buy', abs((2 - d[buys]).mean()) < 0.03)
check('sim l11 s10: profit per trade tends to s - alpha delta = 1 at s = 3', abs(np.where(buys, 3 - d, 3 + d).mean() - 1) < 0.03)
check('sim r3 i8: 2 - 0.3 x 10 = -1 a trade', abs(np.where(*(lambda h, i, b, dd: (b, 2 - dd, 2 + dd))(*gm(0.3, 10, 2_000_000, rng))).mean() + 1) < 0.03)
# two and three independent buys given the value
n = 3_000_000
high = rng.random(n) < 0.5
bs = [np.where(rng.random(n) < 0.2, high, rng.random(n) < 0.5) for _ in range(3)]
two = bs[0] & bs[1]
thr = two & bs[2]
check('sim r3 i5: E[V | two buys] = 503.85', abs(490 + 20 * high[two].mean() - 503.846) < 0.05)
check('sim h3 i3: E[V | three buys] = 505.43', abs(490 + 20 * high[thr].mean() - 505.429) < 0.07)
stated('h3', 'i3', '1.58p', abs((505.4286 - 503.8462) - 1.58) < 0.005)
# homework 3 performance task: tilted noise
high, informed, buys, d = gm(0.2, 21, 4_000_000, rng, beta=0.75)
check('sim h3 i8: zero-profit ask is V + 3p', abs(d[buys].mean() - 3) < 0.05)
check('sim h3 i8: zero-profit bid is V - 7p', abs(-d[~buys].mean() - 7) < 0.08)
check('sim h3 i8: P(buy) = 0.7, P(informed | buy) = 1/7, P(informed | sell) = 1/3', abs(buys.mean() - 0.7) < 0.002 and abs(informed[buys].mean() - 1 / 7) < 0.002 and abs(informed[~buys].mean() - 1 / 3) < 0.003)
check('sim h3 i8 (d): symmetric quotes earn 1.2p on a buy, lose 2.8p on a sell, 0 overall', abs((4.2 - d[buys]).mean() - 1.2) < 0.05 and abs((4.2 + d[~buys]).mean() + 2.8) < 0.08 and abs(np.where(buys, 4.2 - d, 4.2 + d).mean()) < 0.05)
al, be, de = sp.symbols('alpha beta delta', positive=True)
a_closed = sp.Rational(1, 2) * al * de / (sp.Rational(1, 2) * al + (1 - al) * be)
check('h3 i8: a = alpha delta / (alpha + 2(1 - alpha) beta); at beta = 1/2 it is alpha delta', sp.simplify(a_closed - al * de / (al + 2 * (1 - al) * be)) == 0 and sp.simplify(a_closed.subs(be, sp.Rational(1, 2)) - al * de) == 0)
stated('h3', 'i7', '8p', 0.2 * 40 == 8)
# l12 auctions


def uncross_ref(buys, sells):
    best = None
    for p in sorted({p for p, _ in buys} | {p for p, _ in sells}):
        dmd = sum(q for l, q in buys if l >= p)
        sup = sum(q for l, q in sells if l <= p)
        v = min(dmd, sup)
        if v and (best is None or (v, -abs(dmd - sup)) > best[1]):
            best = ((p, v), (v, -abs(dmd - sup)))
    return best and best[0]


rows = node('l12', 's0')['canvas']['params']['rows']
t = [(int(r[0]), int(r[1].replace(',', '')), int(r[2].replace(',', ''))) for r in rows]
m = {p: min(dm, su) for p, dm, su in t}
check('l12 s0: 501p matches the most, 1,200', max(m, key=m.get) == 501 and m[501] == 1200 and node('l12', 's0')['widget']['answer'] == ['r2'])
check('l12 s2: bids above 501p total 1,000, so the 500 at 501p share the last 200', dict((p, dm) for p, dm, _ in t)[502] == 1000 and 1500 - 1000 == 500 and 1200 - 1000 == 200)
b2 = [(252, 500), (251, 300), (250, 400), (249, 600), (248, 200)]
s2 = [(252, 600), (251, 400), (250, 500), (249, 300), (248, 200)]
check('l12 s4: second auction uncrosses at 250p for 1,000', uncross_ref(b2, s2) == (250, 1000))
check('l12 s5: no overlap, no price', uncross_ref([(249, 500), (248, 300)], [(251, 400), (252, 200)]) is None)
m3 = {p: min(dm + 300, su) for p, dm, su in t}
check('h3 i5: a 300-share market buy moves the uncross to 502p, 1,300 matched', max(m3, key=m3.get) == 502 and m3[502] == 1300)
check('l12 s9: the bars add to £200m and £20m is 40% of the close', sum(node('l12', 's9')['canvas']['state']['values'].values()) == 200 and 20 / 50 == 0.4)
r3 = [(104, 200, 1500), (103, 500, 1200), (102, 900, 1000), (101, 1300, 700), (100, 1600, 400)]
check('r3 i3: opening auction uncrosses at 102p for 900', max(r3, key=lambda x: min(x[1], x[2]))[0] == 102)
check('l12 q1: uncross at 101p for 600', max([(100, 900, 300), (101, 700, 600), (102, 400, 1000)], key=lambda x: min(x[1], x[2]))[0] == 101)

# ---------------------------------------------------------------- code widgets


def close(a, b):
    if isinstance(a, tuple) or isinstance(b, tuple):
        return a == b
    try:
        return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)
    except TypeError:
        return a == b


def run_py(widget, code):
    ns = {}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(code, ns)
    except Exception:
        return [False] * len(widget['tests'])
    res = []
    for t_ in widget['tests']:
        try:
            if t_.get('setup'):
                exec(t_['setup'], ns)
            if t_.get('compare') == 'raises':
                try:
                    eval(t_['call'], ns)
                    res.append(False)
                except Exception as ex:
                    res.append(isinstance(ex, eval(t_['expect'], ns)))
                continue
            val, exp = eval(t_['call'], ns), eval(t_['expect'], ns)
            res.append(close(val, exp) if t_.get('compare') == 'isclose' else val == exp)
        except Exception:
            res.append(False)
    return res


ncode = 0
for f, loc, w in all_widgets():
    if w['kind'] == 'code':
        ncode += 1
        check(f'{f} {loc} code: the solution passes every hidden test', all(run_py(w, w['solution'])))
        check(f'{f} {loc} code: the untouched starter fails at least one test', not all(run_py(w, w['starter'])))
check('eight Python code widgets were run', ncode == 8)
ns = {}
exec(node('h3', 'i4')['widget']['solution'], ns)
rng = random.Random(8)
ok = True
for _ in range(3000):
    bq = [(rng.randrange(95, 106), rng.randrange(1, 9) * 100) for _ in range(rng.randrange(0, 6))]
    sq_ = [(rng.randrange(95, 106), rng.randrange(1, 9) * 100) for _ in range(rng.randrange(0, 6))]
    ok &= ns['uncross'](bq, sq_) == uncross_ref(bq, sq_)
check('h3 i4: the model uncross agrees with an independent reference on 3,000 random books', ok)
ns = {}
exec(node('l11', 's10')['widget']['solution'], ns)
check('l11 s10: seed 1 gives 0.9988 and the long run is 1p', abs(ns['maker_pnl'](100000, 0.2, 10, 3, 1) - 0.9988) < 1e-9 and abs(ns['maker_pnl'](400000, 0.2, 10, 3, 99) - 1) < 0.05)

print(f'{COUNT[0]} checks, {len(FAILS)} failed')
for name in FAILS:
    print(' -', name)
sys.exit(1 if FAILS else 0)
