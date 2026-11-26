#!/usr/bin/env python3
"""Concept audit series-1-3 (round 1): independent recomputation of the series course.

Run from the repo root or anywhere:  python docs/reports/series-L1-3-concepts.py
Standard library only (no version-dependent figures).

Parts
 A. Every numeric and slider widget in lessons, reviews, homework and problems:
    the key and every slip value recomputed from the named mistake.
 B. Every fluency family swept over its whole variable range: key recomputed by
    brute force (terms listed and added, brackets multiplied out), every wrong
    value checked against the mistake its line names, collisions counted.
 C. Stated facts in prose (exact values quoted in explains), recomputed.
 D. Empirical and convergence claims: Monte Carlo for the chance items, the
    harmonic series (terms shrink, sums do not settle), geometric partial sums.
 E. Text checks for the audit's findings. These FAIL while the content is as
    audited; they pass once the fix in docs/reviews/audit-series-1-3.md is applied.

Exit 0 only when every check passes.
"""
import json, math, os, random, re, sys
from fractions import Fraction as Fr
from math import comb

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CDIR = os.path.join(ROOT, 'app', 'content', 'courses', 'series')
fails, passes, finding_fails = [], 0, []


def ok(cond, label, finding=False):
    global passes
    if cond:
        passes += 1
    else:
        (finding_fails if finding else fails).append(label)


def load(name):
    return json.load(open(os.path.join(CDIR, name + '.json'), encoding='utf-8'))


def widgets(d):
    for key, tag in (('screens', 'S'), ('quiz', 'Q'), ('items', 'I')):
        for i, s in enumerate(d.get(key, [])):
            if 'parts' in s:
                for j, p in enumerate(s['parts']):
                    yield f'{tag}{i}p{j}', p
            else:
                yield f'{tag}{i}', s


def ann(C, r, n):  # n payments of C, first one period away
    return sum(C / (1 + r) ** t for t in range(1, n + 1))


def geo(a, r, n):
    return sum(a * r ** k for k in range(n))


def ari(a, d, n):
    return sum(a + k * d for k in range(n))


def rec(f, u, steps):
    for _ in range(steps):
        u = f(u)
    return u


def first(pred, start=1):
    n = start
    while not pred(n):
        n += 1
    return n


def coef(poly_terms, n, power):
    """coefficient of x^power in (sum of c*x^e)^n, by multiplying out."""
    cur = {0: Fr(1)}
    for _ in range(n):
        nxt = {}
        for e1, c1 in cur.items():
            for c2, e2 in poly_terms:
                nxt[e1 + e2] = nxt.get(e1 + e2, 0) + c1 * c2
        cur = nxt
    return cur.get(power, 0)


def binom_p(n, k, p):
    return comb(n, k) * p ** k * (1 - p) ** (n - k)


# ---------------------------------------------------------------- Part A
# file -> loc -> (key, [slips in file order]); every figure derived here, not copied.
A = {
 'l1-spotting-the-rule': {
  'S0': (17 + 4, [17 + 5, 17, 17 + 3]),
  'S1': (5, [6, 1]),
  'S2': (10 - 3 * 5, [10 - 3 * 4, 0, 5, 1 - 9]),
  'S3': (4 * 50 + 3, [4 * 50, 7 + 50 * 4, 50 + 4]),
  'S4': (12 * 12, [2 * 12, 11 * 11, 25 + 11]),
  'S7': (50 - 7 * .25, [50 - 8 * .25, 50 + 7 * .25, 50 + 8 * .25]),
  'S8': (2000 / 2, [2000 - 4000, 2000 - 2000, 2000 / 4]),
  'Q0': (23 + 7, [23 + 2, 7]),
  'Q2': (10 - 3 * 5, [(10 - 3) * 5, 5, 10 - 3 * 4]),
 },
 'l2-any-term': {
  'S0': ((19 - 4) / 3, [6, 19]),
  'S1': (4 + 39 * 3, [4 + 40 * 3, 40 * 3, 40 + 3]),
  'S2': (11 + 9 * 6, [11 + 10 * 6, 10 * 6, 6 + 9 * 11]),
  'S3': (50 + 14 * -4, [50 + 15 * -4, 50 + 14 * 4, 50 + 15 * 4, 6]),
  'S5': ((39 - 14) / (8 - 3), [39 - 14, 25 / 6, 25 / 8]),
  'S8': (1500 + 23 * 200, [1500 + 24 * 200, 24 * 200, 23 * 200]),
  'S9': (first(lambda n: 1500 + 200 * (n - 1) > 10000), [43, 10000 / 200, 42]),
  'Q1': (20 + 11 * -3, [20 + 12 * -3, 20 + 33, 13]),
  'Q2': ((50 - 30) / (9 - 5), [20, 20 / 5]),
  'Q3': ((102 - 2) / 5, [19, 21]),
 },
 'l3-multiplying-each-time': {
  'S0': (54 * 3, [54 + 36, 54 * 2]),
  'S3': (3 / 2, [3 - 2, 2 / 3]),
  'S4': (3 * 2 ** 7, [3 * 2 ** 8, 3 * 2 ** 6, 3 + 7 * 3]),
  'S5': (16 * (-.5) ** 5, [.5, 16 * (-.5) ** 4, -2 - 6 - 6, -2 * -2 * -2]),
  'S8': (1.2 * 1.05 ** 7, [1.2 * 1.05 ** 8, 1.2 + 7 * .06]),
  'S9': (20000 * 1.01 ** 12 - (20000 + 12 * 200), [0, 20000 * 1.01 ** 12 - 20000]),
  'Q0': (8000 * .5 ** 4, [8000 * .5 ** 3, 8000 * .5 ** 5, 8000 - 4 * 2000]),
  'Q1': (48 / 64, [48 - 64, 64 / 48]),
 },
 'l4-last-step': {
  'S1': (10 / (1 - .5), [10, 0, 50]),
  'S2': (rec(lambda u: 2 * u - 3, 5, 3), [rec(lambda u: 2 * u - 3, 5, 2), 2 * 3 - 3,
         rec(lambda u: 2 * (u - 3), 5, 3), rec(lambda u: 2 * u - 3, 5, 4)]),
  'S4': (12 / (1 - .6), [12, 12 / .6, rec(lambda u: .6 * u + 12, 0, 9)]),
  'S6': (rec(lambda u: 3 * u - 1, 4, 2), [3 * 2 - 1, 3 * 4 - 1, 3 * (3 * 4) - 1]),
  'S8': (rec(lambda b: 1.01 * b - 200, 5000, 2), [5000 - 400, 5000 + 2 * 50 - 400,
         rec(lambda b: 1.01 * (b - 200), 5000, 2), 1.01 * 5000 - 200]),
  'S9': (200 / .01, [12 * 200, 200 / .1, 200 / .001]),
  'Q0': (2 + 3 * 6, [2 + 4 * 6, 3 + 6]),
  'Q1': (4 / .5, [4, 4 / 2]),
  'Q2': (rec(lambda u: 2 * u + 1, 3, 2), [2 * 2 + 1, 7]),
 },
 'review-1': {
  'I0': (16 - 5, [16 + 5, 16 - 6]),
  'I3': (first(lambda n: 2 * 3 ** (n - 1) == 486), [5, 486 / 2]),
  'I4': (rec(lambda u: .5 * u + 6, 20, 2), [.5 * 2 + 6, 16]),
  'I5': (5 / .25, [5, 5 / .75]),
  'I6': (50 * (-.8) ** 3, [25.6, 50 * (-.8) ** 4]),
  'I7': (first(lambda n: 350 + 125 * (n - 1) > 2000), [14, 2000 / 125, 13]),
  'I8': (first(lambda n: .8 * 1.04 ** (n - 1) > 1), [6, first(lambda n: .8 + .032 * (n - 1) > 1)]),
 },
 'homework-1': {
  'I2': (22 + 10, [22 + 8, 22 * 2]),
  'I3': (2 + 9 * -3, [2 + 10 * -3, 2 + 8 * -3, 25]),
  'I4': (324 * 3 ** 2, [324 * 3 ** 3, 324 * 3, 324 + 2 * 104]),
  'I5': (rec(lambda b: 1.005 * b - 150, 12000, 3), [12000 - 450, 12000 + 3 * 60 - 450,
         rec(lambda b: 1.005 * b - 150, 12000, 2)]),
  'I7': (first(lambda n: 10000 * 1.02 ** n > 10000 + 300 * n),
         [first(lambda n: 10000 * 1.02 ** (n - 1) * .02 > 300), 39, 0]),
 },
 'problems-1': {
  'I0p0': (18 + 6 * 3, [18 + 7 * 3, 30]),
  'I0p2': (3 * 25 + 15, [18 + 3 * 25, 3 * 25]),
  'I0p3': (first(lambda n: 3 * n + 15 >= 45), [12.5, 45 / 3, 9]),
  'I1p2': (80 * .9 ** 5, [80 * .9 ** 6, 80 * .9 ** 4, 80 - 5 * 8]),
  'I1p3': (first(lambda n: 80 * .9 ** (n - 1) < 40), [7, 6]),
  'I2p0': (rec(lambda u: .4 * u + 240, 240, 2), [720, 336, rec(lambda u: .6 * u + 240, 240, 2)]),
  'I2p1': (240 / .6, [240 / .4, 240 / 1.4]),
  'I2p3': (first(lambda n: rec(lambda u: .4 * u + 240, 240, n - 1) > 395),
           [4, first(lambda n: rec(lambda u: .6 * u + 240, 240, n - 1) > 395)]),
  'I3p0': ((216 - 96) / 2, [120, 120 / 3]),
  'I3p1': (math.sqrt(216 / 96), [216 / 96, 216 / 96 / 2, math.sqrt(96 / 216)]),
  'I3p4': (first(lambda n: 64 * 1.5 ** (n - 1) > 1000), [7, first(lambda n: 60 * n - 24 > 1000)]),
 },
 'l5-sigma': {
  'S1': (3 + 5 + 7, [7, 3 * 7, 3 + 7, 3 + 5 + 7 + 9]),
  'S5': (sum(k * k for k in range(1, 5)), [10 ** 2, 16, 10, 20]),
  'S6': (5 * len(range(4, 13)), [5 * 8, 5 * 12, 5, 5 * 11]),
  'S7': (len(range(7, 21)), [13, 20]),
  'S9': (1200 - 450 + 800 - 1500, [-1500, 1200 + 450 + 800 + 1500, 1200 - 450 + 800 - 1500 + 350, 1550]),
  'Q0': (sum(10 - k for k in range(1, 5)), [sum(10 + k for k in range(1, 5)), 40, 9]),
  'Q3': (50 - 41, [91, 50, 50 / 6]),
 },
 'l6-gauss': {
  'S3': (1 + 6, [6, 21]),
  'S4': (sum(range(1, 101)), [100 * 101, 50 * 100, 51 * 100, 101]),
  'S5': (3 + 6 + 9 + 12 + 15, [18 + 18, 3 * 18, 5 * 18]),
  'S6': (sum(range(5, 51, 3)), [15 * 55 / 2, 16 * 55, 17 * 55 / 2, 15 * 55]),
  'S8': (ari(4, 3, 20), [10 * (8 + 20 * 3), 20 * (8 + 19 * 3), 4 + 19 * 3]),
  'S9': (ari(200, 150, 8), [7 / 2 * (200 + 1250), 8 * 1450, 4 * (200 + 200 + 8 * 150), 8 * 200]),
  'Q0': (sum(range(1, 51)), [50 * 51, 25 * 50]),
  'Q1': (sum(range(1, 20, 2)), [200, 9 * 20 / 2, sum(range(2, 21, 2))]),
  'Q3': (25 / 2 * (8 + 80), [25 * 88, 25 / 2 * (80 - 8)]),
 },
 'l7-shifted-copy': {
  'S0': (geo(1, 2, 8), [128, 256, geo(1, 2, 7), 8 * 128]),
  'S3': (2 + 6 + 18 + 54 + 162, [484, 486, 3 * 242]),
  'S4': (48 + 24 + 12 + 6 + 3, [46.5, 48 / .5, 48 + 1.5]),
  'S5': (geo(3, 2, 9), [geo(3, 2, 8), 2 * 768, geo(3, 2, 10), 768]),
  'S8': (ann(500, .04, 10), [5000, ann(500, .04, 10) * 1.04, ann(500, .04, 9), 5000 / 1.04 ** 10]),
  'Q0': (geo(1, 3, 6), [728, geo(1, 3, 7), 3 ** 6]),
  'Q2': (sum(2 ** k for k in range(10)), [geo(1, 2, 9), geo(1, 2, 11), 2 ** 10]),
  'Q3': (4 - 8 + 16 - 32 + 64, [4 + 8 + 16 + 32 + 64, 4 * ((-2) ** 5 - 1)]),
 },
 'l8-adding-forever': {
  'S2': (1 / (1 - 1 / 3), [1, 1 / (1 / 3), 2 / 3]),
  'S3': (6 / (1 - 1 / 3), [6 / (1 / 3), 6 / (1 + 1 / 3), 1.5]),
  'S4': (8 / 1.5, [8 / .5, 8, 8 - 4]),
  'S8': (5 / .04, [5 / .04 + 5, 5 / 1.04, 125 / 1.04]),
  'Q0': (12 / .5, [12 / 1.5, 12]),
  'Q3': (20 / 1.5, [20 / .5, 20, 10]),
 },
 'review-2': {
  'I0': (sum(k * k + 1 for k in range(2, 6)), [sum(k * k + 1 for k in range(1, 6)), 54, 55]),
  'I1': (len(range(5, 31)), [25, 30]),
  'I2': (sum(range(2, 201, 2)), [5050, 100 * 202, 100 * 100]),
  'I3': (sum(range(7, 103, 5)), [19 * 109 / 2, 20 * 109, 21 * 109 / 2]),
  'I4': (geo(5, 3, 7), [geo(5, 3, 6), 5 * 3 ** 7 - 5, geo(5, 3, 8)]),
  'I5': (geo(100, 1.01, 12), [1200, 10000 * 1.01 ** 12, geo(100, 1.01, 11)]),
  'I7': (2.5 / .4, [2.5 + 1.5, 2.5 / .6, 2.5 / 1.6]),
 },
 'homework-2': {
  'I1': (float(sum(Fr(1, k * (k + 1)) for k in range(1, 100))), [1, 1 - 1 / 101, .5]),
  'I2': (first(lambda n: ari(3, 4, n) > 1000), [22, first(lambda n: 3 + 4 * (n - 1) >= 999)]),
  'I3': (first(lambda n: geo(5, 2, n + 1) > 5000), [10, 5000 / 5, 8]),
  'I4': (10000 / ann(1, .005, 24), [10000 / 24, (10000 + 24 * 50) / 24, 10000 / ann(1, .005, 24) / 1.005]),
 },
 'problems-2': {
  'I0p0': (8 + 9 * 5, [8 + 10 * 5, 50]),
  'I0p1': (ari(8, 5, 10), [10 * 61, 5 * 53, 5 * (16 + 50)]),
  'I0p2': (len(range(4, 11)), [6, 10]),
  'I0p3': (sum(5 * k + 3 for k in range(4, 11)), [3 * 76, 305 - (8 + 13 + 18 + 23), 305]),
  'I1p0': (4 * 5 ** 5, [4 * 5 ** 6, 4 * 5 ** 4]),
  'I1p1': (geo(4, 5, 6), [4 * geo(4, 5, 6), 62500 / 4]),
  'I1p3': (first(lambda n: geo(4, 5, n) > 350000), [first(lambda n: 4 * 5 ** (n - 1) > 350000), 7]),
  'I2p0': (geo(3, .6, 9), [3 / .4, geo(3, .6, 10), geo(3, .6, 8)]),
  'I2p1': (5 + 2 * geo(3, .6, 9), [5 + 7.42, 2 * geo(3, .6, 9), 10 + 2 * geo(3, .6, 9)]),
  'I2p2': (3 / .4, [5 / .4, 3 / .6, 1.8 / .4]),
  'I2p3': (5 + 2 * 7.5, [5 + 7.5, 15, 10 + 15]),
  'I3p1': (first(lambda n: ari(50, 10, n) >= 3000), [20, 3000 / 50]),
  'I3p2': (200 / .1, [180 / .1, 200 / .9, 200 / 1.9]),
  'I3p3': (geo(200, .9, 21), [geo(200, .9, 20), 2000, 2000 * .9 ** 21]),
  'I3p4': (3000 - geo(200, .9, 21), [1000, 3000 - geo(200, .9, 20), geo(200, .9, 21)]),
 },
 'l9-pascal': {
  'S2': (comb(4, 2), [3, 3 * 3, comb(4, 1)]),
  'S4': (comb(6, 3), [10, comb(6, 2), 100]),
  'S8': (comb(4, 2), [2 ** 4, comb(4, 1), 2, 1]),
  'Q0': (comb(7, 2), [comb(6, 2), comb(7, 3), 6 * 15]),
 },
 'l10-counting-paths': {
  'S2': (comb(4, 2), [4 * 3, 16, 8, 4]),
  'S3': (math.factorial(3), [3, 9, 2]),
  'S4': (comb(5, 3), [60, 60 / 3, 60 / 2, 5 * 3]),
  'S8': (binom_p(5, 3, .5), [10, 3 / 5, .5 ** 3, .5 ** 5]),
  'Q0': (comb(7, 2), [7 * 6, 7 * 2, 7 * 7]),
  'Q3': (binom_p(4, 2, .5), [2 / 4, .5 ** 2, .5 ** 4]),
 },
 'l11-powers-of-a-bracket': {
  'S3': (coef([(2, 1), (1, 0)], 4, 2), [6 * 2, 4, 6 * 8, 6]),
  'S4': (coef([(1, 1), (-3, 0)], 4, 1), [108, 4 * 9, -27, -4 * 9]),
  'S5': (coef([(1, 1), (2, -1)], 4, 0), [6 * 2, 6, 2 ** 4, comb(4, 3) * 2 ** 3]),
  'S9': (1000 * 1.04 ** 3 - 1120, [1000 * 1.04 ** 3 - 1000, 1000 * 3 * .04 ** 2,
         1000 * (.04 ** 2 + .04 ** 3), 1000 * 1.04 ** 3]),
  'Q0': (coef([(1, 1), (2, 0)], 5, 3), [10, 10 * 2, 10 * 8]),
  'Q2': (coef([(2, 1), (1, -1)], 6, 0), [20, 20 * 2, 2 ** 6]),
  'Q3': (coef([(3, 0), (1, 1)], 5, 2), [10 * 9, 10 * 3, 10]),
 },
 'l12-small-x': {
  'S2': (1 + 4 * -.02, [1 + 4 * .02, .98, 4 * .98]),
  'S3': (1 + 10 * .02 + 45 * .02 ** 2, [1.2, 1.2 + 90 * .02 ** 2, 1.2 + 100 * .02 ** 2]),
  'S8': (10000 * comb(5, 2) * .04 ** 2, [10000 * .04 ** 2, 10000 * 25 * .04 ** 2, 10000 * 20 * .04 ** 2,
         10000 * 1.04 ** 5 - 10000]),
  'Q0': (50 * (1 + 10 * .002), [50 * 1.002, 50 * (1 + 10 * .02), 1]),
  'Q3': (1 + 8 * .03 + 28 * .03 ** 2, [1.24, 1.24 + 56 * .03 ** 2]),
 },
 'l13-stream-of-payments': {
  'S0': (100 / 1.05, [95, 105, 100]),
  'S3': (ann(100, .05, 5), [500, 500 / 1.05, 500 / 1.05 ** 5]),
  'S5': (100 / .05, [100 / .05 + 100, 100 / 5, ann(100, .05, 5)]),
  'S8': (ann(5, .04, 3) + 100 / 1.04 ** 3, [115, ann(5, .04, 3), 100 / 1.04 ** 3, 115 / 1.04 ** 3]),
  'Q0': (200 / 1.04 ** 2, [200 * .92, 200 / 1.04, 200 * 1.04 ** 2]),
  'Q1': (50 / .025, [50 * .025, 50 / 2.5, 50 / .025 + 50]),
  'Q2': (ann(250, .03, 4), [1000, 1000 / 1.03, 1000 / 1.03 ** 4]),
 },
 'review-3': {
  'I0': (comb(8, 3), [comb(7, 3), comb(8, 4), comb(8, 2)]),
  'I1': (comb(9, 4), [9 * 8 * 7 * 6, 9 * 4, 9 ** 4]),
  'I3': (1 + 25 * .004 + 300 * .004 ** 2, [1.1, 1.1 + 600 * .004 ** 2, 1.1 + 625 * .004 ** 2]),
  'I4': (ann(1200, .03, 20), [24000, 1200 / .03, 24000 / 1.03 ** 20]),
  'I5': (binom_p(6, 3, .5), [3 / 6, .5 ** 3, .5 ** 6]),
  'I8': (100 / .04 - 100 / .05, [1, 100 / 4 - 100 / 5, 100]),
 },
 'homework-3': {
  'I1': (coef([(1, 0), (2, 1)], 8, 5), [56, 56 * 8, 56 * 2]),
  'I2': (coef([(1, 2), (-2, -1)], 6, 0), [-240, 15 * 4, comb(6, 3) * (-2) ** 3]),
  'I3': (binom_p(5, 3, .6), [.6 ** 3 * .4 ** 2, binom_p(5, 3, .5), .6 ** 3, 3 / 5]),
  'I4': (80 * (1 + 21 * .001 + 210 * .001 ** 2), [80 * 1.021, 80 * (1.021 + 420e-6), 1.6968]),
  'I5': (sum(coef([(3, 1), (-1, 0)], 5, k) for k in range(6)), [3 ** 5, 4 ** 5, -32]),
  'I7': (10000 / ann(1, .06, 5), [10000 / 5, 2000 + 600, 2000 * 1.06]),
  'I8': (max(comb(10, k) * .5 ** k for k in range(11)), [comb(10, 5) * .5 ** 5, comb(10, 2) * .25,
         comb(10, 4) * .5 ** 4, comb(10, 5)]),
 },
 'problems-3': {
  'I0p0': (comb(18, 4), [18 * 17 * 16 * 15, 18 * 4, 18 * 17 * 16 * 15 / 6]),
  'I0p1': (comb(18, 4) + comb(18, 14), [comb(18, 4)]),
  'I0p2': (comb(19, 4), [3060 + 18, 2 * 3060, 19 * 18 * 17 * 16]),
  'I0p3': (sum(comb(19, k) for k in range(20)), [2 ** 19 - 1, 2 ** 18]),
  'I1p0': (coef([(1, 0), (-3, 1)], 7, 2), [21 * 3, -189, 9]),
  'I1p2': (1 - 21 * .01 + 189 * .01 ** 2, [.79, 1 - .21 - .0189, 1 - 21 * .03 + 189 * .03 ** 2, round(.97 ** 7, 4)]),
  'I1p3': (coef([(1, 0), (-3, 1)], 7, 3), [945, 35 * -3, -27]),
  'I1p4': (.8089 - 945e-6, [.97 ** 7, .8089 + 945e-6, .8089 - 945e-4]),
  'I2p0': (1 + 12 * .005 + 66 * .005 ** 2, [1.06, 1.005 ** 12, 1.06 + 132 * .005 ** 2]),
  'I2p1': (1 / 1.0617, [1.0617, 1 - .0617, 1 / 1.005]),
  'I2p2': (ann(100, .005, 12), [1200, 20000 * .9419, 94.19]),
  'I2p3': (ann(100, .005, 12) - 1150, [50, 1150 - ann(100, .005, 12)]),
  'I3p0': (11 ** 4, [10 ** 4 + 1, 11111]),
  'I3p1': (11 ** 5, [15101051, 14641 * 10, 10 ** 5 + 1]),
  'I3p2': (1.1 ** 5, [11 ** 5 / 1e4, 11 ** 5 / 1e6, 1.5]),
  'I3p3': (1.1 ** 5 - 1.5, [1.1 ** 5 - 1.6, comb(5, 2) * .01, 1.5 - 1.1 ** 5]),
 },
}


def close(a, b, tol):
    return abs(float(a) - float(b)) <= tol + 1e-9


seenA = 0
for fname, table in A.items():
    d = load(fname)
    ws = dict(widgets(d))
    numeric = [loc for loc, s in ws.items() if (s.get('widget') or {}).get('kind') in ('numeric', 'slider')]
    ok(set(numeric) == set(table), f'A coverage {fname}: content {sorted(numeric)} vs script {sorted(table)}')
    for loc, (key, slips) in table.items():
        w = ws[loc]['widget']
        seenA += 1
        tol = (w.get('tol') or {}).get('abs', 0) if isinstance(w.get('tol'), dict) else 0
        # the key must sit inside the widget's own tolerance of the recomputed value
        ok(close(w['answer'], key, max(tol, 5e-5)), f'A key {fname} {loc}: content {w["answer"]} recomputed {key}')
        wr = w.get('wrong', [])
        ok(len(wr) == len(slips), f'A slip count {fname} {loc}')
        for x, s in zip(wr, slips):
            v = x['value'] if 'value' in x else x['from']
            xt = (x.get('tol') or {}).get('abs', 0) if isinstance(x.get('tol'), dict) else 0
            ok(close(v, s, max(xt, 6e-3 if abs(s) > 1 else 6e-5)), f'A slip {fname} {loc} {x["id"]}: content {v} recomputed {s}')
            # a slip may never be accepted as the key
            ok(not close(v, w['answer'], tol), f'A slip equals key {fname} {loc} {x["id"]}')
print(f'A: {seenA} numeric widgets recomputed')

# ---------------------------------------------------------------- Part B fluency sweeps
def ev(expr, env):
    e = re.sub(r'(?<![\w.])(\d+\.\d+|\d+)', r'Fr("\1")', expr.replace('^', '**'))
    return eval(e, {'Fr': Fr, 'floor': lambda v: Fr(math.floor(v)), 'abs': abs,
                    'gcd': lambda a, b: Fr(math.gcd(int(a), int(b))),
                    'comb': lambda a, b: Fr(comb(int(a), int(b)))}, env)


def cases(fam):
    names = list(fam['vars'])
    doms = []
    for n in names:
        v = fam['vars'][n]
        if 'int' in v:
            dom = [Fr(i) for i in range(v['int'][0], v['int'][1] + 1)]
        else:
            dom = [x if isinstance(x, str) else Fr(str(x)) for x in v['pick']]
        dom = [x for x in dom if x not in [Fr(str(y)) for y in v.get('not', [])]] if 'not' in v else dom
        doms.append(dom)

    def recur(i, env):
        if i == len(names):
            e = dict(env)
            for k, x in fam.get('let', {}).items():
                e[k] = ev(x, e)
            if all(ev(c, e) for c in fam.get('where', [])):
                yield e
            return
        for x in doms[i]:
            env[names[i]] = x
            yield from recur(i + 1, env)
    yield from recur(0, {})


def tmpl(s, e):  # resolve a bare "{name}" value template
    m = re.fullmatch(r'\{(\w+)\}', s)
    return e[m.group(1)] if m else None


def terms_ar(a, d, n):
    return [a + i * d for i in range(n)]


def terms_ge(a, r, n):
    return [a * r ** i for i in range(n)]


B = {}  # (file, family) -> function(e) -> (key, {wrong id: value})
B['fluency-l2-any-term', 'term-from-list'] = lambda e: (terms_ar(e['a'], e['d'], int(e['k']))[-1], {
    'k-steps': e['a'] + e['k'] * e['d'], 'difference-sign': terms_ar(e['a'], -e['d'], int(e['k']))[-1]})
B['fluency-l2-any-term', 'difference-from-two-terms'] = lambda e: (e['d'], {
    'whole-rise': e['uq'] - e['up'], 'counted-terms': (e['uq'] - e['up']) / (e['q'] - e['p'] + 1)})
B['fluency-l2-any-term', 'which-term'] = lambda e: (
    Fr(terms_ar(e['a'], e['d'], 61).index(e['u']) + 1), {'steps-not-position': e['m'] - 1, 'one-too-many': e['m'] + 1})
B['fluency-l3-multiplying-each-time', 'geometric-term'] = lambda e: (terms_ge(e['a'], e['r'], int(e['k']))[-1], {
    'k-factors': e['a'] * e['r'] ** int(e['k']), 'added-the-step': terms_ar(e['a'], e['t2'] - e['a'], int(e['k']))[-1]})
B['fluency-l3-multiplying-each-time', 'common-ratio'] = lambda e: (e['t2'] / e['a'], {
    'upside-down': e['a'] / e['t2'], 'difference': e['t2'] - e['a']})
B['fluency-l6-gauss', 'one-to-n'] = lambda e: (Fr(sum(range(1, int(e['m']) + 1))), {
    'not-halved': e['m'] * (e['m'] + 1), 'one-term-short': e['m'] * (e['m'] - 1) / 2})
B['fluency-l6-gauss', 'first-n-terms'] = lambda e: (sum(terms_ar(e['a'], e['d'], int(e['k']))), {
    'not-halved': 2 * sum(terms_ar(e['a'], e['d'], int(e['k']))), 'k-steps': e['k'] * (2 * e['a'] + e['k'] * e['d']) / 2})
B['fluency-l6-gauss', 'up-to-last-term'] = lambda e: (sum(terms_ar(e['a'], e['d'], int(e['k']))), {
    'counted-steps': (e['k'] - 1) * (e['a'] + e['l']) / 2, 'not-halved': e['k'] * (e['a'] + e['l'])})
B['fluency-l7-shifted-copy', 'first-n-terms'] = lambda e: (sum(terms_ge(e['a'], e['r'], int(e['k']))), {
    'one-term-short': sum(terms_ge(e['a'], e['r'], int(e['k']) - 1)), 'sign-flipped': -sum(terms_ge(e['a'], e['r'], int(e['k'])))})
B['fluency-l7-shifted-copy', 'up-to-last-term'] = lambda e: (sum(terms_ge(e['a'], e['r'], int(e['k']))), {
    'counted-steps': sum(terms_ge(e['a'], e['r'], int(e['k']))) - e['l'], 'sign-flipped': -sum(terms_ge(e['a'], e['r'], int(e['k'])))})
B['fluency-l7-shifted-copy', 'sigma-powers'] = lambda e: (sum(e['r'] ** k for k in range(int(e['b']), int(e['t']) + 1)), {
    'stopped-early': sum(e['r'] ** k for k in range(int(e['b']), int(e['t']))),
    'one-term-extra': sum(e['r'] ** k for k in range(int(e['b']), int(e['t']) + 2))})
B['fluency-l8-adding-forever', 'from-the-terms'] = lambda e: (e['a'] / (1 - e['t2'] / e['a']), {
    'sign-of-r': e['a'] / (1 + e['t2'] / e['a']), 'first-term-left-out': 1 / (1 - e['t2'] / e['a'])})
B['fluency-l8-adding-forever', 'from-a-and-r'] = lambda e: (e['a'] / (1 - e['r']), {
    'sign-of-r': e['a'] / (1 + e['r']), 'first-term-left-out': 1 / (1 - e['r'])})
B['fluency-l8-adding-forever', 'perpetual-bond'] = lambda e: (e['c'] / (e['i'] / 100), {
    'payment-today': e['c'] / (e['i'] / 100) + e['c'], 'per-cent-not-decimal': e['c'] / e['i']})
B['fluency-l11-powers-of-a-bracket', 'x-plus-b'] = lambda e: (coef([(1, 1), (e['b'], 0)], int(e['n']), int(e['e'])), {
    'count-only': Fr(comb(int(e['n']), int(e['ne']))), 'power-swapped': comb(int(e['n']), int(e['ne'])) * e['b'] ** int(e['e'])})
B['fluency-l11-powers-of-a-bracket', 'ax-plus-b'] = lambda e: (coef([(e['a'], 1), (e['b'], 0)], int(e['n']), int(e['e'])), {
    'a-not-raised': comb(int(e['n']), int(e['ne'])) * e['a'] * e['b'] ** int(e['ne']),
    'a-left-out': comb(int(e['n']), int(e['ne'])) * e['b'] ** int(e['ne'])})
B['fluency-l11-powers-of-a-bracket', 'term-with-no-x'] = lambda e: (coef([(e['a'], 1), (e['s'] * e['m'], -1)], int(e['n']), 0), {
    'count-only': Fr(comb(int(e['n']), int(e['n']) // 2)), 'powers-only': (e['a'] * e['s'] * e['m']) ** (int(e['n']) // 2)})

# expression-answer families: checked by evaluating the intended rule at n = 1..6
EXPR = {
 ('fluency-l2-any-term', 'nth-term-formula'): lambda e, n: (
     e['d'] * n + e['c'], terms_ar(e['a'], e['d'], n)[-1],
     {'n-steps': e['d'] * n + e['a'], 'first-term-times-n': e['a'] * n + e['d']}),
 ('fluency-l3-multiplying-each-time', 'geometric-formula'): lambda e, n: (
     e['a'] * e['r'] ** (n - 1), terms_ge(e['a'], e['r'], n)[-1],
     {'n-factors': e['a'] * e['r'] ** n, 'ratio-and-first-swapped': e['r'] * e['a'] ** (n - 1),
      'arithmetic-rule': e['d'] * n + e['c']}),
}
collisions = {}
swept = 0
for fname in ['fluency-l2-any-term', 'fluency-l3-multiplying-each-time', 'fluency-l6-gauss',
              'fluency-l7-shifted-copy', 'fluency-l8-adding-forever', 'fluency-l11-powers-of-a-bracket']:
    d = load(fname)
    for fam in d['families']:
        fid = (fname, fam['id'])
        n_cases = bad = coll = same = 0
        for e in cases(fam):
            n_cases += 1
            if fid in EXPR:
                vals = [EXPR[fid](e, n) for n in range(1, 7)]
                if any(v[0] != v[1] for v in vals):
                    bad += 1
                for wid in vals[0][2]:
                    if all(v[2][wid] == v[0] for v in vals):
                        same += 1
                continue
            if fname == 'fluency-l8-adding-forever' and fam['id'] == 'recurring-decimal':
                key = e['key']
                # brute force: 60 repeating digits
                dec = Fr(int(('%d%d' % (e['t'], e['u'])) * 30), 10 ** 60)
                if abs(key - dec) > Fr(1, 10 ** 58) or e['first'] == key or e['plus'] == key:
                    bad += 1
                continue
            key, wrong = B[fid](e)
            content_key = tmpl(fam['widget']['answer'], e)
            if content_key != key:
                bad += 1
            wtol = Fr(str((fam['widget'].get('tol') or {}).get('abs', 0)))
            cw = {x['id']: tmpl(x['value'], e) for x in fam['wrong']}
            if set(cw) != set(wrong) or any(cw[k] != wrong[k] for k in wrong):
                bad += 1
            if any(abs(v - content_key) <= wtol for v in cw.values()):
                same += 1
            vs = list(cw.values())
            if len(set(vs)) < len(vs):
                coll += 1
        swept += n_cases
        ok(n_cases > 0, f'B {fid}: no admissible case')
        ok(bad == 0, f'B {fid}: {bad}/{n_cases} cases where key or a slip value is not the stated one')
        ok(same == 0, f'B {fid}: {same}/{n_cases} cases where a wrong value is accepted as the key')
        if coll:
            collisions[fid] = (coll, n_cases)
print(f'B: {swept} fluency cases swept; slip-slip collisions: {collisions}')
# Finding 7: two slips with one value (the second line can never show)
ok(not collisions, 'B slip-slip collision ' + str(collisions), finding=True)

# ---------------------------------------------------------------- Part C stated facts
def near(a, b, tol, label):
    ok(abs(a - b) <= tol, f'C {label}: {a} vs {b}')


near(1.01 ** 5, 1.05101, 5e-6, 'l12 S0 1.01^5')
near(.98 ** 4, .92237, 5e-6, 'l12 S2 0.98^4')
near(1.02 ** 10, 1.21899, 5e-6, 'l12 S3')
near(1.01 ** 100, 2.7048, 5e-5, 'l12 S5')
near(comb(100, 2) * 1e-4, .495, 1e-12, 'l12 S5 third term')
near(1.02 ** 5 - 1.1, .0041, 5e-5, 'l12 S6 error at 0.02')
near(1.01 ** 5 - 1.05, .0010, 5e-5, 'l12 S6 error at 0.01')
near(.98 ** 5, .90392, 5e-6, 'l12 S7')
near(10000 * 1.04 ** 5 - 12000, 166.53, 5e-3, 'l12 S8 exact gap')
near(1.3 ** 5 - 2.5, 1.21, 5e-3, 'l12 S1 gap right end')
near(.7 ** 5 + .5, .67, 5e-3, 'l12 S1 gap left end')
near(50 * 1.002 ** 10, 51.01, 5e-3, 'l12 Q0')
near(.97 ** 6, .8330, 5e-5, 'l12 Q1')
near(1.03 ** 8, 1.26677, 5e-6, 'l12 Q3')
near(1.004 ** 25, 1.10495, 5e-6, 'review-3 I3')
near(1.01 ** 200, 7.32, 5e-3, 'review-3 I7 long')
near(.9 ** 30, .042, 5e-4, 'review-3 I7 negative')
near(1.001 ** 50, 1.0512, 5e-5, 'review-3 I7 right')
near(ann(100, .05, 10), 772.17, 5e-3, 'l13 S4 key')
near(1000 / 1.05 ** 10, 613.91, 5e-3, 'l13 S4 last')
near(100 + ann(100, .05, 4), 454.60, 5e-3, 'l13 S6 annuity due')
near(1.05 * ann(100, .05, 5), 454.60, 5e-3, 'l13 S6 = 1.05 x ordinary')
near(ann(100, .06, 5), 421.24, 5e-3, 'l13 Q3')
near(500 / 1.06 ** 5, 373.63, 5e-3, 'l13 Q3 last')
near(ann(1000, .05, 30), 15372.45, 5e-3, 'hw2 I7 annuity A')
near(1000 / .05 - ann(1000, .05, 30), 4627.55, 5e-3, 'hw2 I7 difference')
near(24 * round(10000 / ann(1, .005, 24), 2), 10637.04, 5e-3, 'hw2 I4 total repaid')
near(5 * round(10000 / ann(1, .06, 5), 2), 11869.80, 5e-3, 'hw3 I7 total')
near(5000 * 1.03 ** 10 - 6500, 219.58, 5e-3, 'hw3 I9 ten-year gap')
near(5000 * 1.03 ** 40 - 11000, 5310.19, 5e-3, 'hw3 I9 forty-year gap')
near(5000 * comb(40, 3) * .03 ** 3, 1333.80, 5e-3, 'hw3 I9 fourth term')
near(5000 * comb(10, 3) * .03 ** 3, 16.20, 5e-3, 'hw3 I9 next term')
near(10000 * 1.02 ** 40, 22080.40, 5e-3, 'hw1 I7 month 40')
near(10000 * 1.02 ** 39, 21647.45, 5e-3, 'hw1 I7 month 39')
near(16600 - 10000 * 1.02 ** 22, 1140.20, 5e-3, 'hw1 I7 behind at month 22')
near(12000 - 2000 * 1.01 ** 12, 9746.35, 5e-3, 'hw1 I8 closed form B12')
near(rec(lambda b: 1.01 * b - 120, 10000, 12), 9746.35, 5e-3, 'hw1 I8 recurrence B12')
near(rec(lambda b: 1.01 * b - 120, 10000, 3), 9939.40, 5e-3, 'hw1 I8 B3')
near(20000 * 1.01 ** 12, 22536.50, 5e-3, 'l3 S9 plan B')
near(.97 ** 7, .80798, 5e-6, 'problems-3 calculator value')
near(1.005 ** 12, 1.06168, 5e-6, 'problems-3 gym')
near(sum(range(4, 20, 3)), 69, 0, 'l5 S4 six-week total')
near(10 / 1.9, 5.26, 5e-3, 'l8 S6 sum')
ok([comb(9, k) for k in range(10)] == [1, 9, 36, 84, 126, 126, 84, 36, 9, 1], 'C l9 row 9')
ok([comb(19, k) for k in range(5)] == [1, 19, 171, 969, 3876], 'C problems-3 row 19')
ok([coef([(1, 1), (-3, 0)], 4, k) for k in (4, 3, 2, 1, 0)] == [1, -12, 54, -108, 81], 'C l11 S4 expansion')
ok([coef([(2, 1), (-1, 0)], 4, k) for k in (4, 3, 2, 1, 0)] == [16, -32, 24, -8, 1], 'C hw3 I0 expansion')
ok([comb(10, k) * .5 ** k for k in range(5)] == [1, 5, 11.25, 15, 13.125], 'C hw3 I8 terms')
# recurrences: fixed point L = b/(1-a), and the gap is geometric with ratio a
for a_, b_, u1 in ((.5, 10, 100), (.6, 12, 0), (2, -10, 12), (1.01, -200, 15000), (.4, 240, 240)):
    L = b_ / (1 - a_)
    u, gaps = u1, []
    for _ in range(8):
        gaps.append(u - L)
        u = a_ * u + b_
    ok(all(abs(gaps[i + 1] - a_ * gaps[i]) < 1e-6 for i in range(7)), f'C gap ratio a={a_}')

# ---------------------------------------------------------------- Part D empirical / convergence
rng = random.Random(20261126)
N = 400_000


def mc(n, k, p):
    return sum(1 for _ in range(N) if sum(rng.random() < p for _ in range(n)) == k) / N


for n, k, p, claim, rival in ((5, 3, .5, .3125, .6), (4, 2, .5, .375, .5), (6, 3, .5, .3125, .5), (5, 3, .6, .3456, .3125)):
    est = mc(n, k, p)
    se = math.sqrt(claim * (1 - claim) / N)
    ok(abs(est - claim) < 4 * se, f'D MC {k} of {n} at p={p}: {est:.4f} vs {claim}')
    ok(abs(est - rival) > 10 * se, f'D MC separates {claim} from slip {rival}')
# most likely count in 6 flips is 3 (review-3 I5 explain)
ok(max(range(7), key=lambda k: comb(6, k)) == 3, 'D mode of row 6')
# geometric partial sums settle exactly when |r| < 1
for r in (-.9, -.5, .5, .9):
    ok(abs(geo(1, r, 2000) - 1 / (1 - r)) < 1e-9, f'D geometric settles r={r}')
ok(geo(1, 1, 1000) == 1000 and {geo(1, -1, n) for n in range(1, 9)} == {0, 1}, 'D r = 1 and r = -1 do not settle')
# harmonic series: the terms shrink to 0 but the partial sums pass every level
H, n = 0.0, 0
levels = {}
for target in (5, 10, 14):
    while H <= target:
        n += 1
        H += 1 / n
    levels[target] = n
ok(levels[5] == 83 and levels[10] == 12367 and 1 / levels[14] < 2e-6, f'D harmonic passes 5, 10, 14 at n = {levels}')
print('D: harmonic sum first passes 5, 10, 14 at n =', levels)
# perpetuity, rates 5% -> 4%: gain of the payment t years away (review-3 I8 explain)
gain = [100 / 1.04 ** t - 100 / 1.05 ** t for t in range(1, 400)]
tmax = gain.index(max(gain)) + 1
prop = [(1.05 / 1.04) ** t for t in range(1, 400)]
ok(all(prop[i] < prop[i + 1] for i in range(len(prop) - 1)), 'D proportional gain rises with t')
print(f'D: absolute gain per payment peaks at t = {tmax} (£{max(gain):.2f}), is £{gain[0]:.2f} at t = 1 and £{gain[199]:.2f} at t = 200')
# 1 + nx + C(n,2)x^2: does each kept term shrink the error? Not for negative x with |nx| large.
def errs(x, n, kmax):
    exact, s, out = (1 + x) ** n, 0, []
    for k in range(kmax + 1):
        s += comb(n, k) * x ** k
        out.append(abs(exact - s))
    return out
e_small, e_neg = errs(.02, 10, 3), errs(-.5, 10, 3)
ok(all(e_small[i + 1] < e_small[i] for i in range(3)), 'D kept terms shrink the error at x = 0.02')
print('D: errors of 1, 2, 3, 4 terms of (1 - 0.5)^10:', [round(v, 3) for v in e_neg])

# ---------------------------------------------------------------- Part E findings (fail until fixed)
def text(name):
    return json.dumps(load(name), ensure_ascii=False)


ok('because the terms shrink to 0' not in text('l13-stream-of-payments'),
   'E1 l13 summary: "finite value ... because the terms shrink to 0" (harmonic series: terms shrink, no sum)', finding=True)
ok('makes the terms shrink to nothing' not in text('l8-adding-forever'),
   'E2 l8 S1 feedback gives shrinking terms as the test for settling', finding=True)
ok('otherwise they run away' not in text('l4-last-step'),
   'E3 l4 summary: "otherwise they run away" (a = -1 flips for ever; a start at L stays)', finding=True)
ok(all(abs(rec(lambda u: -u + 6, 5, k)) < 10 for k in range(50)), 'E3 basis: a = -1 stays bounded')
ok('exactly when $-1 < a < 1$' not in text('homework-1'),
   'E4 homework-1 h-gap-proof: "shrinks to 0 exactly when -1 < a < 1" (also when u1 = L)', finding=True)
ok('Far-off payments gain the most from the cut' not in text('review-3'),
   'E5 review-3 I8: far-off payments gain most only in proportion (absolute gain peaks near year %d)' % tmax, finding=True)
ok(e_neg[1] < e_neg[0] or 'Each term we keep shrinks the error' not in text('l12-small-x'),
   'E6 l12 S3: "Each term we keep shrinks the error" fails for (1 - 0.5)^10', finding=True)
ok('only when solving for $n$ gives a whole number' not in text('l2-any-term'),
   'E8 l2 summary: needs a positive whole number (n = 0 or -1 is whole but no position)', finding=True)

print(f'passes {passes}; failing checks {len(fails)}; failing finding checks {len(finding_fails)}')
for f in fails:
    print('FAIL', f)
for f in finding_fails:
    print('FINDING', f)
sys.exit(1 if fails or finding_fails else 0)
