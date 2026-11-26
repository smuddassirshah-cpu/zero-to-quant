#!/usr/bin/env python3
"""Blind concept audit, round 2: quadratics levels 1 to 3 (audit name quadratics-1-3-r2).

Run from the repository root or from app/:  python docs/reports/quadratics-L1-3-concepts-r2.py
Exits 0 when every check passes. A check that fails because the content is wrong stays failing.

Parts
  A  every numeric key and every numeric slip: the key recomputed from the item, each slip
     recomputed as the value that the mistake its feedback line names would give
  B  every expand / factorise choice item: sympy says exactly one option is right
  C  every expression widget: key equals the task, accept forms equal the key, slips differ
  D  hand-written sympy checks of the solving, discriminant, inequality, vertex and model items
  E  canvas: every labelled plane function against its label over the whole x range; tables
  F  fluency families (l1, l2, l3, l4, l6, l7): every draw in the whole range, templates rendered
     here independently of the engine, key recomputed from the vars, each slip recomputed
  G  a randomised identity sweep (20,000 draws) of the stated rules (no claim here is empirical,
     so this is a guard on the rules, not a Monte Carlo estimate)
"""
import itertools, json, math, os, random, re, sys
from fractions import Fraction as Fr
import sympy as sp
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
                                        implicit_multiplication_application, convert_xor)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get('QUAD_ROOT') or os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'quadratics')
TR = standard_transformations + (implicit_multiplication_application, convert_xor)
SYM = {c: sp.Symbol(c) for c in 'xytrqpwdnABvhkabc'}
fails, passed = [], 0


def ok(cond, what):
    global passed
    if cond:
        passed += 1
    else:
        fails.append(what)


def load(name):
    return json.load(open(os.path.join(ROOT, name + '.json'), encoding='utf-8'))


def get(doc, path):
    o = doc
    for part in re.findall(r'\.([A-Za-z_]+)|\[(\d+)\]', path):
        o = o[part[0]] if part[0] else o[int(part[1])]
    return o


def tex2sym(s):
    s = s.strip().strip('$').replace('−', '-').replace('\\left', '').replace('\\right', '')
    s = s.replace('\\big', '').replace('\\,', '').replace('\\;', '').replace('\\times', '*').replace('\\cdot', '*')
    s = s.replace('\\dfrac', '\\frac').replace('\\tfrac', '\\frac')
    for _ in range(20):
        n = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', s)
        n = re.sub(r'\\sqrt\{([^{}]*)\}', r'sqrt(\1)', n)
        n = re.sub(r'\^\{([^{}]*)\}', r'^(\1)', n)
        if n == s:
            break
        s = n
    s = s.replace('[', '(').replace(']', ')').replace('{', '(').replace('}', ')')
    return parse_expr(s, local_dict=dict(SYM, sqrt=sp.sqrt), transformations=TR)


def same(a, b):
    return sp.simplify(sp.expand(a - b)) == 0


def maths(text):
    return re.findall(r'\$([^$]+)\$', text or '')


def widgets(doc):
    def walk(o, p):
        if isinstance(o, dict):
            if isinstance(o.get('widget'), dict):
                yield p, o
            for k, v in o.items():
                yield from walk(v, p + '.' + k)
        elif isinstance(o, list):
            for i, x in enumerate(o):
                yield from walk(x, p + '[%d]' % i)
    yield from walk(doc, '')


FILES = ['l1-two-brackets', 'l2-product-and-sum', 'l3-leading-coefficient', 'l4-difference-of-squares',
         'l5-product-of-zero', 'l6-completing-the-square', 'l7-the-formula', 'l8-how-many-solutions',
         'l9-shape-of-a-square', 'l10-turning-point', 'l11-meeting-the-axis', 'l12-above-or-below',
         'l13-best-price', 'review-1', 'review-2', 'review-3', 'homework-1', 'homework-2', 'homework-3',
         'problems-1', 'problems-2', 'problems-3']
DOC = {f: load(f) for f in FILES}
s5, s13, s29, s41, s40, s801, s401 = (math.sqrt(v) for v in (5, 13, 29, 41, 40, 801, 401))


def roots(a, b, c):
    d = math.sqrt(b * b - 4 * a * c)
    return sorted([(-b - d) / (2 * a), (-b + d) / (2 * a)])


# ---------------------------------------------------------------- A: numeric keys and slips
# (file, path): (key, {slip id: value the named mistake gives})
P10 = lambda q: -0.04 * q * q + 12 * q - 500
NUM = {
 ('l1-two-brackets', '.screens[0]'): (13 * 12, {'firsts-lasts': 10 * 10 + 3 * 2, 'added': 13 + 12, 'one-strip': 156 - 2 * 10, 'other-strip': 156 - 3 * 10}),
 ('l1-two-brackets', '.screens[4]'): (5 - 2, {'ignored-sign': 5 + 2, 'flipped': -5 + 2, 'both-minus': -5 - 2}),
 ('l1-two-brackets', '.screens[8]'): (2000 * 0.04 ** 2, {'whole-gain': 2000 * 1.04 ** 2 - 2000, 'one-strip': 2000 * 0.04, 'two-strips': 2 * 2000 * 0.04, 'per-pound': 0.04 ** 2}),
 ('l2-product-and-sum', '.quiz[3]'): (3 + 24 / 3, {'gave-p': 24 / 3, 'added-c': 3 + 24}),
 ('l3-leading-coefficient', '.quiz[1]'): (4 * -3, {'c-only': -3, 'no-sign': 4 * 3}),
 ('l4-difference-of-squares', '.screens[0]'): (100 - 9, {'side-not-area': 100 - 3, 'small-square': 7 * 7, 'cut-strip': 100 - 3 * 10}),
 ('l4-difference-of-squares', '.screens[8]'): (50 * 1.08 * 0.92, {'flat': 50, 'down-only': 50 * 0.92, 'up-only': 50 * 1.08, 'two-r': 50 * (1 - 2 * 0.08 ** 2)}),
 ('l4-difference-of-squares', '.quiz[1]'): (51 ** 2 - 49 ** 2, {'diff-squared': (51 - 49) ** 2, 'sum-squared': (51 + 49) ** 2}),
 ('l5-product-of-zero', '.quiz[1]'): (roots(1, 2, -15)[1], {'five': 5, 'fifteen': 15}),
 ('l6-completing-the-square', '.screens[0]'): (3 * 3, {'six-sq': 6 * 6, 'six': 6, 'side': 3}),
 ('l6-completing-the-square', '.screens[3]'): (5 - 9, {'add': 9 + 5, 'ignore': 5, 'drop': -9, 'sign': 9 - 5}),
 ('l6-completing-the-square', '.screens[5]'): (roots(1, 3, -4)[0], {'pos': roots(1, 3, -4)[1], 'shift': -2.5, 'flip': -roots(1, 3, -4)[1], 'sign': 2.5 + 1.5}),
 ('l6-completing-the-square', '.screens[8]'): (100 - 36, {'table': max(-q * q + 20 * q - 36 for q in (4, 8, 12, 16)), 'fixed': 100, 'q': 10}),
 ('l6-completing-the-square', '.quiz[1]'): (math.sqrt(1.21) - 1, {'halved': 0.21 / 2, 'total': 0.21}),
 ('l6-completing-the-square', '.quiz[2]'): (roots(1, -10, 21)[0], {'larger': roots(1, -10, 21)[1], 'sign': -3}),
 ('l7-the-formula', '.screens[2]'): (3 + s5, {'smaller': 3 - s5, 'noroot': 3 + 5, 'nocentre': s5}),
 ('l7-the-formula', '.screens[3]'): (roots(2, 8, 3)[1], {'nodiv': roots(1, 8, 3)[1], 'forgotc': roots(1, 4, 3)[1], 'smaller': roots(2, 8, 3)[0], 'sign': -roots(2, 8, 3)[1]}),
 ('l7-the-formula', '.screens[5]'): (roots(3, -5, -2)[0], {'signb': (-5 - 7) / 6, 'overa': (5 - 7) / 3, 'sign': (7 - 5) / 6}),
 ('l7-the-formula', '.screens[7]'): (9 - 4 * 2 * -1, {'signc': 9 - 4 * 2 * 1, 'neg': 4 * 2 * -1 - 9, 'noa': 9 - 4 * -1}),
 ('l7-the-formula', '.screens[8]'): (roots(-20, 140, -100)[1] if roots(-20, 140, -100)[1] > 3.5 else roots(-20, 140, -100)[0], {'first': (7 - s29) / 2, 'peak': 3.5, 'nohalf': 7 + s29}),
 ('l7-the-formula', '.quiz[1]'): (roots(2, -1, -6)[1], {'signb': (-1 + 7) / 4, 'overa': (1 + 7) / 2}),
 ('l8-how-many-solutions', '.screens[1]'): (16 / 4, {'sign': -4, 'half': 4 / 2, 'sq': 4 ** 2}),
 ('l8-how-many-solutions', '.screens[2]'): (16 - 24, {'flip': 24 - 16, 'plus': 16 + 24, 'noa': 16 - 6}),
 ('l8-how-many-solutions', '.screens[9]'): (2500 / 4, {'nofour': 2500, 'half': 2500 / 2, 'q': 25}),
 ('l8-how-many-solutions', '.quiz[1]'): (4 - 4 * 3 * -1, {'signc': 4 - 4 * 3 * 1, 'negb': -4 + 12}),
 ('l9-shape-of-a-square', '.screens[9]'): ((87.2 + 115.2) / 2, {'linear': 100, 'rise': 100 - 14 + 1.2, 'fall': 100 + 14 + 1.2}),
 ('l9-shape-of-a-square', '.quiz[0]'): ((-3) ** 2 - 5, {'neg-square': -9 - 5, 'doubled': 2 * -3 - 5}),
 ('l9-shape-of-a-square', '.quiz[2]'): (2 * 4 - 1, {'origin': -1, 'line': 4, 'double': 4 + 5}),
 ('l10-turning-point', '.screens[3]'): (5, {'x-value': 3, 'sign': -5, 'intercept': 5 - 9}),
 ('l10-turning-point', '.screens[9]'): (P10(150), {'ends': P10(300), 'quantity': 150, 'minus-b': P10(12)}),
 ('l10-turning-point', '.quiz[1]'): (-10 / 2, {'minus-b': -10, 'sign': 10 / 2}),
 ('l10-turning-point', '.quiz[2]'): (3 * 4 - 24 + 5, {'intercept': 5, 'x-value': 2, 'sign': 3 * 4 + 24 + 5, 'sign2': 7}),
 ('l11-meeting-the-axis', '.screens[2]'): (2 * -4, {'sign': 8, 'sum': -2 + 4, 'vertex': (1 + 2) * (1 - 4)}),
 ('l11-meeting-the-axis', '.screens[4]'): (2 * 3 * -3, {'no-a': 3 * -3, 'intercept': 2 * -1 * -7, 'x-value': 4, 'sign': 2 * 3 * 3}),
 ('l11-meeting-the-axis', '.screens[9]'): (math.sqrt(1.8 / 0.05), {'square': 1.8 / 0.05, 'intercept': -1.8, 'half': 36 / 2}),
 ('l11-meeting-the-axis', '.quiz[1]'): (3 * -2 * -6, {'no-a': -2 * -6, 'vertex': 3 * (4 - 2) * (4 - 6), 'sign': -36}),
 ('l11-meeting-the-axis', '.quiz[2]'): (-(2 + 1) * (2 - 5), {'sign': (2 + 1) * (2 - 5), 'intercept': -(1) * (-5), 'x-value': 2}),
 ('l12-above-or-below', '.screens[4]'): (sum(1 for x in range(-50, 50) if x * x - 2 * x - 8 < 0), {'both-ends': sum(1 for x in range(-50, 50) if x * x - 2 * x - 8 <= 0), 'one-end': 6}),
 ('l12-above-or-below', '.screens[9]'): (0.6, {'upper': 1, 'vertex': 0.08 / 0.1, 'equal': 0.5}),
 ('l12-above-or-below', '.quiz[1]'): (sum(1 for x in range(-50, 50) if (x - 1) * (x - 6) < 0), {'both-ends': sum(1 for x in range(-50, 50) if (x - 1) * (x - 6) <= 0), 'one-end': 5}),
 ('l13-best-price', '.screens[1]'): (50 - 20, {'peak': 25, 'double': 2 * 20}),
 ('l13-best-price', '.screens[3]'): (40 / 2, {'choke': 40, 'revenue': 20 * 400, 'quarter': 40 / 4}),
 ('l13-best-price', '.screens[5]'): (7.5 / 2, {'choke': 7.5, 'revenue': 3.75 * 750, 'rounded': 4}),
 ('l13-best-price', '.quiz[0]'): (600 / 80, {'choke': 15, 'no-b': 600 / 2}),
 ('l13-best-price', '.quiz[2]'): ((6 + 20) / 2, {'revenue': 10, 'full-cost': 10 + 6, 'choke': 20}),
 ('l13-best-price', '.quiz[3]'): (0.1 / 0.16, {'no-two': 0.1 / 0.08, 'equal': 0.5}),
 ('review-1', '.items[1]'): (2 * 5, {'one-strip': 5, 'each-squared': 0, 'corner': 25}),
 ('review-1', '.items[6]'): (1.03 ** 2 - 1, {'simple': 2 * 0.03, 'each-squared': 0.03 ** 2, 'one-strip': 0.03}),
 ('review-1', '.items[7]'): (math.sqrt(0.01), {'one-pc': 0.01, 'two-r': 0.01 / 2}),
 ('review-1', '.items[8]'): (roots(1, -14, 40)[1], {'smaller': roots(1, -14, 40)[0], 'sum': 14, 'product': 40}),
 ('review-2', '.items[0]'): (roots(1, -3, -28)[1], {'sign': -roots(1, -3, -28)[0], 'const': 28}),
 ('review-2', '.items[2]'): (40 - 49, {'add': 40 + 49, 'drop': -49, 'sign': 49 - 40}),
 ('review-2', '.items[4]'): ((3 + s41) / 4, {'signb': (-3 + s41) / 4, 'overa': (3 + s41) / 2, 'bar': 3 + s41 / 4}),
 ('review-2', '.items[8]'): (1 - math.sqrt(16200 / 20000), {'halved': (1 - 0.81) / 2, 'total': 1 - 0.81}),
 ('review-3', '.items[2]'): (-8 / 4, {'minus-b': -8, 'sign': 2, 'over-a': -8 / 2}),
 ('review-3', '.items[3]'): ((1 + 3) * (1 - 5), {'intercept': 3 * -5, 'x-value': 1, 'sign': 16}),
 ('review-3', '.items[4]'): (2 * -1 * 4, {'vertex': 2 * (-1.5 - 1) * (-1.5 + 4), 'no-a': -1 * 4, 'sign': 8}),
 ('review-3', '.items[6]'): (3 ** 2, {'x-value': 3, 'left': (-1) ** 2}),
 ('review-3', '.items[8]'): (7.5 * (1200 - 80 * 7.5), {'price': 7.5, 'quantity': 1200 - 80 * 7.5}),
 ('review-3', '.items[9]'): ((2 + 15) / 2, {'revenue': 15 / 2, 'full-cost': 7.5 + 2, 'sum': 2 + 15}),
 ('homework-1', '.items[4]'): (1003 * 997, {'added': 1000 ** 2 + 9, 'no-corner': 1000 ** 2}),
 ('homework-1', '.items[5]'): (2 * 6, {'one-strip': 6, 'corner': 36, 'eighteen': 36 / 2}),
 ('homework-1', '.items[6]'): (320 / 16, {'sum': 36, 'product': 320}),
 ('homework-2', '.items[0]'): (roots(1, 3, -40)[1], {'split': 40 - 3, 'sign': 8}),
 ('homework-2', '.items[3]'): (math.sqrt(5618 / 5000) - 1, {'halved': (5618 / 5000 - 1) / 2, 'total': 5618 / 5000 - 1}),
 ('homework-2', '.items[5]'): (3 + s13, {'neg': 3 - s13, 'peak': 3, 'nohalf': 6 + math.sqrt(52)}),
 ('homework-2', '.items[7]'): (48 ** 2 / 8, {'four': 48 ** 2 / 4, 'two': 48 ** 2 / 2}),
 ('homework-3', '.items[0]'): (6 / 0.8, {'minus-b': 6, 'over-a': 6 / 0.4, 'sign': -7.5}),
 ('homework-3', '.items[3]'): (-2 * 3 * -3, {'no-a': 3 * -3, 'sign': -18, 'x-value': 5}),
 ('homework-3', '.items[4]'): (sum(1 for x in range(-50, 50) if x * x + 3 * x < 10), {'both-ends': sum(1 for x in range(-50, 50) if x * x + 3 * x <= 10), 'one-end': 7}),
 ('homework-3', '.items[6]'): ((81 - 36) / 6 - (9 - 6), {'parabola': 45 / 6, 'true': 3, 'k-one': 45 - 3}),
 ('homework-3', '.items[8]'): (0.07 / 0.08, {'no-corr': 0.04 / 0.05, 'no-two': 0.07 / 0.04, 'half': 0.5}),
 ('problems-1', '.items[0].parts[2]'): (13 * 22, {'kept': 14 * 21, 'sum-thirteen': 14 * 19, 'square': 16 ** 2}),
 ('problems-1', '.items[1].parts[3]'): (3 * 10 ** 2, {'three-squared': 30 ** 2, 'both-sides': 6 * 10 ** 2}),
 ('problems-1', '.items[2].parts[4]'): (35 * 29, {'old': 36 * 25 - 9, 'each-term': 36 * 25 - 5, 'no-hole': 32 ** 2, 'signs': 25 * 31}),
 ('problems-2', '.items[0].parts[0]'): (15 + 5, {'sign': 15 - 5, 'no-five': 15 + 1}),
 ('problems-2', '.items[0].parts[1]'): (1 + 2, {'negative': 1 - 2, 'no-root': 1 + 4, 'carried': 1 + math.sqrt(2)}),
 ('problems-2', '.items[1].parts[0]'): (36 - 40, {'sign-b': -36 - 40, 'plus': 36 + 40, 'reversed': 40 - 36}),
 ('problems-2', '.items[1].parts[1]'): (10 - 9, {'start': 10, 'halved': 10 - 3, 'sign': 10 + 9}),
 ('problems-2', '.items[1].parts[2]'): (3 - math.sqrt(3), {'larger': 3 + math.sqrt(3), 'half-root': 3 - math.sqrt(12), 'no-root': 3 - 3}),
 ('problems-2', '.items[1].parts[3]'): (s40, {'no-root': 40, 'no-four': math.sqrt(10)}),
 ('problems-2', '.items[2].parts[0]'): (roots(1, 1, -240)[1], {'negative': roots(1, 1, -240)[0], 'sign': 16}),
 ('problems-2', '.items[2].parts[1]'): (1 + 800, {'sign-c': 1 - 800, 'no-double': 1 + 400}),
 ('problems-2', '.items[2].parts[2]'): ((-1 + s801) / 2, {'sign-b': (1 + s801) / 2, 'no-half': -1 + s801, 'carried': (-1 + s401) / 2}),
 ('problems-2', '.items[2].parts[3]'): (100 - 13 * 14 // 2, {'rounded-up': 14 * 15 // 2 - 100, 'rows': 13}),
 ('problems-3', '.items[0].parts[0]'): (10, {'root': 20, 'sign': -10}),
 ('problems-3', '.items[0].parts[1]'): (-0.2 * 10 * -10, {'sign': -20, 'no-a': -1 * 10 * -10}),
 ('problems-3', '.items[0].parts[3]'): (16 - 4, {'half': 6, 'right-end': 16, 'left-end': 4}),
 ('problems-3', '.items[1].parts[0]'): (150 / 5, {'no-divide': 150}),
 ('problems-3', '.items[1].parts[1]'): (30 / 2, {'zero': 30}),
 ('problems-3', '.items[1].parts[2]'): (15 * 75, {'bikes': 75, 'no-drop': 15 * 150}),
 ('problems-3', '.items[1].parts[3]'): ((8 + 30) / 2, {'full-cost': 15 + 8, 'no-cost': 15, 'sign': (-8 + 30) / 2}),
 ('problems-3', '.items[2].parts[1]'): (5, {'flat': 6, 'vertex': 2.5}),
 ('problems-3', '.items[2].parts[2]'): (0.5 * 5, {'flat': 0.5 * 6, 'square-half': 15 - (0.5 * 5) ** 2}),
 ('problems-3', '.items[2].parts[3]'): (2.5 * 2.5 - 0.5 * 2.5 ** 2, {'water-top': 3 * 3 - 0.5 * 9, 'no-square': 2.5 * 2.5, 'x-value': 2.5}),
}
SETS = {
 ('problems-2', '.items[0].parts[2]'): ([0, 2], {'sign': [0, -2]}),
 ('problems-2', '.items[0].parts[3]'): ([1 - math.sqrt(0.4), 1 + math.sqrt(0.4)], {'no-root': [0.6, 1.4], 'times-five': [1 - math.sqrt(10), 1 + math.sqrt(10)]}),
}
seen_numeric = 0
for f in FILES:
    for p, o in widgets(DOC[f]):
        w = o['widget']
        if w['kind'] != 'numeric':
            continue
        seen_numeric += 1
        if 'answers' in w:
            key, slips = SETS.get((f, p), (None, None))
            ok(key is not None, f'{f}{p}: numeric set not in the audit table')
            if key is None:
                continue
            ok(all(abs(a - b) < 0.006 for a, b in zip(sorted(w['answers']), sorted(key))), f'{f}{p}: key set {w["answers"]} vs {key}')
            for x in w.get('wrong', []):
                got = sorted(float(v) for v in x['value'].split(','))
                ok(x['id'] in slips and all(abs(a - b) < 0.006 for a, b in zip(got, sorted(slips[x['id']]))), f'{f}{p}: slip {x["id"]} {got}')
                ok(any(abs(a - b) > 0.01 for a, b in zip(got, sorted(key))), f'{f}{p}: slip {x["id"]} equals the key')
            continue
        key, slips = NUM.get((f, p), (None, None))
        ok(key is not None, f'{f}{p}: numeric widget not in the audit table')
        if key is None:
            continue
        tol = w.get('tol', {}).get('abs', 0) + 1e-12
        ok(abs(w['answer'] - key) <= 0.0051, f'{f}{p}: key {w["answer"]} but recomputed {key}')
        vals = []
        for x in w.get('wrong', []):
            ok(x['id'] in slips, f'{f}{p}: slip {x["id"]} not in the audit table')
            if x['id'] in slips:
                ok(abs(x['value'] - slips[x['id']]) <= 0.0051 + x.get('tol', {}).get('abs', 0) * 0, f'{f}{p}: slip {x["id"]} stored {x["value"]} but the named mistake gives {slips[x["id"]]}')
            ok(abs(x['value'] - w['answer']) > tol + x.get('tol', {}).get('abs', 0), f'{f}{p}: slip {x["id"]} is inside the key band')
            vals.append(x['value'])
            fb = o.get('feedback', {}).get('byKey', {})
            ok(x['id'] in fb, f'{f}{p}: slip {x["id"]} has no feedback line')
        ok(len(set(vals)) == len(vals), f'{f}{p}: two slips share a value')
ok(seen_numeric == len(NUM) + len(SETS), f'numeric widgets seen {seen_numeric} vs table {len(NUM) + len(SETS)}')

# ---------------------------------------------------------------- B: expand / factorise choices
def content_gt1(text):
    """True when some bracket of the typed product still has a whole-number common factor."""
    for inner in re.findall(r'\(([^()]*)\)', text.replace('$', '')):
        e = tex2sym(inner)
        if e.is_Add:
            c, _ = sp.Poly(e, *sorted(e.free_symbols, key=str)).primitive()
            if abs(c) != 1:
                return True
            if all(sp.Poly(e, z).terms()[-1][0][0] > 0 for z in e.free_symbols):
                return True  # every term still holds the letter
    return False


covered_B = 0
for f in FILES:
    for p, o in widgets(DOC[f]):
        w = o['widget']
        if w['kind'] != 'choice':
            continue
        text = (o.get('prose') or '') + ' ' + (o.get('question') or '')
        if not re.search(r'[Ee]xpand|[Ff]actoris', text):
            continue
        opts = w['options']
        if not all(re.fullmatch(r'\$[^$=]+\$', x['text']) and 'pm' not in x['text'] for x in opts):
            continue
        cands = [m for m in maths(o.get('question', '')) + maths(o.get('prose', ''))[::-1] if re.search(r'\^|\(', m) and '=' not in m]
        if not cands:
            continue
        target = tex2sym(cands[0])
        full = 'ully' in text
        covered_B += 1
        right = 0
        for x in opts:
            e = tex2sym(x['text'])
            eq = same(e, target)
            if x.get('correct'):
                right += 1
                ok(eq, f'{f}{p}: key {x["text"]} is not equal to {cands[0]}')
                if full:
                    ok(not content_gt1(x['text']), f'{f}{p}: key {x["text"]} is not fully factorised')
            else:
                if eq:
                    ok(full and content_gt1(x['text']), f'{f}{p}: wrong option {x["text"]} is equal to the task and fully factorised')
                else:
                    ok(True, '')
        ok(right == 1, f'{f}{p}: {right} options marked correct')
ok(covered_B >= 30, f'part B covered only {covered_B} items')

# every "That expands to ..." / "That gives ..." claim in a choice why-line
for f in FILES:
    for p, o in widgets(DOC[f]):
        w = o['widget']
        if w['kind'] != 'choice':
            continue
        for x in w['options']:
            why = x.get('why', '')
            m = re.search(r'(?:That expands to|These multiply out to|That gives|That is) \$([^$=]+?)(?:= ([^$]+))?\$', why)
            if m and re.fullmatch(r'\$[^$]+\$', x['text']) and re.search(r'\(', x['text']) and re.search(r'x|q', m.group(1)):
                try:
                    lhs = tex2sym(x['text'])
                    rhs = tex2sym(m.group(2) or m.group(1))
                    if '^' in (m.group(2) or m.group(1)) and lhs.free_symbols == rhs.free_symbols:
                        ok(same(lhs, rhs), f'{f}{p}: option {x["text"]} does not expand to {m.group(0)}')
                except Exception:
                    pass

# ---------------------------------------------------------------- C: expression widgets
EXPR_TASK = {
 ('problems-1', '.items[0].parts[0]'): '(x+4)(x+11)', ('problems-1', '.items[0].parts[1]'): 'x^2+15x+36',
 ('problems-1', '.items[1].parts[0]'): 'x^2+11x+30', ('problems-1', '.items[1].parts[1]'): '2x^2+19x+45',
 ('problems-1', '.items[1].parts[2]'): '(x+5)(x+6)+(x+5)(2x+9)', ('problems-1', '.items[2].parts[0]'): '(6x)^2-3^2',
 ('problems-1', '.items[2].parts[1]'): '36x^2-9', ('problems-1', '.items[2].parts[2]'): '(6x+2)^2-9',
 ('problems-1', '.items[2].parts[3]'): '36x^2+24x-5', ('l13-best-price', '.screens[2]'): 'p(800-20p)',
 ('l13-best-price', '.screens[7]'): 'A/(2B)', ('problems-3', '.items[0].parts[2]'): '-0.2x(x-20)',
 ('problems-3', '.items[2].parts[0]'): '(3x-0.5x^2)-0.5x',
}
seen_expr = 0
for f in FILES:
    for p, o in widgets(DOC[f]):
        w = o['widget']
        if w['kind'] != 'expression':
            continue
        seen_expr += 1
        task = EXPR_TASK.get((f, p))
        ok(task is not None, f'{f}{p}: expression widget not in the audit table')
        if task is None:
            continue
        t, a = tex2sym(task), tex2sym(w['answer'])
        ok(same(sp.nsimplify(t, rational=True), sp.nsimplify(a, rational=True)), f'{f}{p}: key {w["answer"]} is not the task {task}')
        for acc in w.get('accept', []):
            ok(same(sp.nsimplify(tex2sym(acc.replace('*', ' ')), rational=True), sp.nsimplify(a, rational=True)), f'{f}{p}: accept {acc} differs from the key')
        for x in w.get('wrong', []):
            ok(not same(sp.nsimplify(tex2sym(x['tex']), rational=True), sp.nsimplify(a, rational=True)), f'{f}{p}: slip {x["id"]} equals the key')
ok(seen_expr == len(EXPR_TASK), f'expression widgets seen {seen_expr} vs table {len(EXPR_TASK)}')
x, q, t, p_, w_, n = sp.symbols('x q t p w n', real=True)
ok(same(sp.expand((6 * x - 5) * (6 * x + 1)), 36 * x ** 2 - 24 * x - 5), 'problems-1 steel: signs slip expansion')
ok(same(sp.expand(9 * (2 * x + 3) * (2 * x - 3)), 36 * x ** 2 - 81), 'problems-1 steel: inside slip expansion')
ok(same(sp.expand((2 * x + 5) * (x + 9)), 2 * x ** 2 + 23 * x + 45), 'problems-1 plot B wrong-pair expansion')

# ---------------------------------------------------------------- D: hand-written sympy checks
def key_of(f, path):
    o = get(DOC[f], path)
    return [z for z in o['widget']['options'] if z.get('correct')][0]['text']


def nums(s):
    s = s.replace('−', '-')
    out = set()
    for m in re.finditer(r'-?\\tfrac\{(\d+)\}\{(\d+)\}|-?\d+(?:\.\d+)?', s):
        g = m.group(0)
        if 'tfrac' in g:
            v = sp.Rational(int(m.group(1)), int(m.group(2)))
            out.add(-v if g.startswith('-') else v)
        else:
            out.add(sp.nsimplify(g))
    return out


def solset(expr, var=x):
    return set(sp.solve(expr, var))


D_ROOTS = [  # (file, path, equation = 0, variable): the key lists exactly the roots
 ('l5-product-of-zero', '.screens[4]', x * (x - 1) - 12, x), ('l5-product-of-zero', '.screens[6]', x ** 2 - 5 * x, x),
 ('l5-product-of-zero', '.screens[9]', -q ** 2 + 20 * q - 64, q), ('l5-product-of-zero', '.quiz[0]', (2 * x - 3) * (x + 4), x),
 ('l5-product-of-zero', '.quiz[3]', (x - 1) * (x - 6) - 6, x), ('l6-completing-the-square', '.screens[6]', (x - 2) ** 2 - 9, x),
 ('l7-the-formula', '.screens[6]', x ** 2 - 4 * x - 5, x), ('l8-how-many-solutions', '.screens[5]', x ** 2 - 36, x),
 ('review-2', '.items[1]', 4 * x ** 2 - 12 * x, x), ('review-2', '.items[3]', (x + 1) ** 2 - 16, x),
 ('homework-2', '.items[1]', x * (x - 3) - 4 * x, x), ('l11-meeting-the-axis', '.quiz[0]', (x + 4) * (x - 1), x),
]
for f, path, eq, var in D_ROOTS:
    k = key_of(f, path)
    ok(nums(k) == {sp.nsimplify(r) for r in solset(eq, var)}, f'{f}{path}: key "{k}" vs roots {solset(eq, var)}')
    o = get(DOC[f], path)
    for z in o['widget']['options']:
        if not z.get('correct'):
            ok(nums(z['text']) != {sp.nsimplify(r) for r in solset(eq, var)} or not nums(z['text']), f'{f}{path}: wrong option "{z["text"]}" lists the true roots')

D_COUNT = [  # number of real roots
 ('l5-product-of-zero', '.screens[5]', x ** 2 - 6 * x + 9, 'One'), ('l5-product-of-zero', '.quiz[2]', 3 * x ** 2 - 12 * x, 'Two'),
 ('l6-completing-the-square', '.quiz[3]', x ** 2 + 4 * x + 7, 'None'), ('l8-how-many-solutions', '.screens[0]', (x - 2) ** 2 + 1, 'None'),
 ('l8-how-many-solutions', '.screens[3]', 2 * x ** 2 + 3 * x + 5, 'None'), ('l8-how-many-solutions', '.screens[4]', 9 * x ** 2 - 12 * x + 4, 'One'),
 ('l8-how-many-solutions', '.screens[7]', x ** 2 - 6 * x - 7, 'Two'), ('l8-how-many-solutions', '.screens[8]', x ** 2 + 5 * x - 1000, 'Two'),
 ('l8-how-many-solutions', '.quiz[0]', x ** 2 + 6 * x + 10, 'None'), ('l8-how-many-solutions', '.quiz[3]', x * (10 - x) - 26, 'None'),
 ('review-2', '.items[6]', 4 * x ** 2 - 4 * x + 1, 'One'),
]
WORD = {0: 'None', 1: 'One', 2: 'Two'}
for f, path, eq, word in D_COUNT:
    cnt = len(sp.real_roots(sp.Poly(sp.expand(eq), x), multiple=False))
    ok(WORD[cnt] == word and key_of(f, path).startswith(word), f'{f}{path}: {cnt} real roots, key "{key_of(f, path)}"')

D_INEQ = [  # (file, path, inequality, key text must equal)
 ('l12-above-or-below', '.screens[0]', x ** 2 - 4 < 0, sp.Interval.open(-2, 2)),
 ('l12-above-or-below', '.screens[3]', x ** 2 < x + 2, sp.Interval.open(-1, 2)),
 ('l12-above-or-below', '.screens[6]', x ** 2 > 9, sp.Union(sp.Interval.open(-sp.oo, -3), sp.Interval.open(3, sp.oo))),
 ('l12-above-or-below', '.screens[8]', -x ** 2 + 4 * x > 0, sp.Interval.open(0, 4)),
 ('l12-above-or-below', '.quiz[0]', x ** 2 - 16 >= 0, sp.Union(sp.Interval(-sp.oo, -4), sp.Interval(4, sp.oo))),
 ('review-3', '.items[5]', x ** 2 - x - 12 > 0, sp.Union(sp.Interval.open(-sp.oo, -3), sp.Interval.open(4, sp.oo))),
 ('l8-how-many-solutions', '.quiz[2]', 64 - 4 * x > 0, sp.Interval.open(-sp.oo, 16)),
 ('review-2', '.items[7]', 36 - 12 * x > 0, sp.Interval.open(-sp.oo, 3)),
 ('problems-3', '.items[1].parts[4]', 605 - 5 * (x - 19) ** 2 >= 525, sp.Interval(15, 23)),
]


def opt_set(text):
    s = text.replace('−', '-').replace('\\le', '<=').replace('\\ge', '>=').replace('$', '')
    s = re.sub(r'<=q?', '<=', s)
    parts = [z.strip() for z in s.split(' or ')]
    sets = []
    for z in parts:
        m = re.fullmatch(r'(-?[\d.]+) (<=?) [xcpy] (<=?) (-?[\d.]+)', z)
        if m:
            sets.append(sp.Interval(sp.nsimplify(m.group(1)), sp.nsimplify(m.group(4)), m.group(2) == '<', m.group(3) == '<'))
            continue
        m = re.fullmatch(r'[xcpy] (<=?|>=?) (-?[\d.]+)', z)
        if not m:
            return None
        v = sp.nsimplify(m.group(2))
        sets.append(sp.Interval(-sp.oo, v, True, m.group(1) == '<') if m.group(1)[0] == '<' else sp.Interval(v, sp.oo, m.group(1) == '>', True))
    return sp.Union(*sets)


for f, path, ineq, truth in D_INEQ:
    ok(sp.solve_univariate_inequality(ineq, x, relational=False) == truth, f'{f}{path}: audit truth set wrong')
    o = get(DOC[f], path)
    hits = 0
    for z in o['widget']['options']:
        s_ = opt_set(z['text'])
        if s_ is not None and s_ == truth:
            hits += 1
            ok(z.get('correct') is True, f'{f}{path}: option "{z["text"]}" is the true set but not the key')
        elif z.get('correct'):
            ok(False, f'{f}{path}: key "{z["text"]}" is not the true set {truth}')
    ok(hits == 1, f'{f}{path}: {hits} options equal the true set')

# single facts
facts = [
 (sp.expand((x + 2) ** 2 - 5) == x ** 2 + 4 * x - 1, 'l7 s0 square form'),
 (solset(x ** 2 + 4 * x - 1) == {-2 + sp.sqrt(5), -2 - sp.sqrt(5)} and '-2 + \\sqrt{5}' in key_of('l7-the-formula', '.screens[0]'), 'l7 s0 key'),
 (solset(x ** 2 + 2 * x - 2) == {-1 + sp.sqrt(3), -1 - sp.sqrt(3)} and key_of('l7-the-formula', '.quiz[0]') == '$-1 \\pm \\sqrt{3}$', 'l7 quiz exact roots'),
 (solset(x ** 2 - 6 * x + 7) == {3 + sp.sqrt(2), 3 - sp.sqrt(2)} and key_of('l7-the-formula', '.quiz[3]') == '$3 \\pm \\sqrt{2}$', 'l7 quiz surd'),
 (solset(x ** 2 - 2 * x - 1) == {1 + sp.sqrt(2), 1 - sp.sqrt(2)} and key_of('review-2', '.items[5]') == '$1 \\pm \\sqrt{2}$', 'review-2 exact'),
 (sp.Poly(5 - 3 * x - x ** 2, x).all_coeffs()[0] == -1 and key_of('l7-the-formula', '.quiz[2]') == '$-1$', 'l7 which a'),
 (sp.expand(2 * (x + 3) ** 2 - 11) == 2 * x ** 2 + 12 * x + 7 and key_of('homework-2', '.items[2]') == '$2(x + 3)^2 - 11$', 'homework-2 leading'),
 (sp.expand((x + 5) ** 2 - 25) == x ** 2 + 10 * x and '(x + 5)^2 - 25' in key_of('l6-completing-the-square', '.screens[2]'), 'l6 s2'),
 (sp.expand((x + 6) ** 2 - 36) == x ** 2 + 12 * x and '(x + 6)^2 - 36' in key_of('l6-completing-the-square', '.quiz[0]'), 'l6 quiz'),
 (key_of('l6-completing-the-square', '.screens[7]') == '$49$', 'l6 s7 corner'),
 (sp.expand(-(x - 2) ** 2 + 5) == -x ** 2 + 4 * x + 1 and key_of('l10-turning-point', '.screens[8]').startswith('A maximum of 5 at $x = 2$'), 'l10 s8'),
 (sp.expand(2 * (x - 3) ** 2 - 11) == 2 * x ** 2 - 12 * x + 7 and key_of('l10-turning-point', '.screens[6]') == '$x = 3$', 'l10 s6'),
 ((2 * 144 - 144 + 7) == 151, 'l10 s6 height at 12'),
 (sp.expand(-2 * (x - 3) ** 2 + 8) == -2 * x ** 2 + 12 * x - 10 and key_of('homework-3', '.items[1]').startswith('A maximum of 8 at $x = 3$'), 'homework-3 max point'),
 (key_of('l10-turning-point', '.screens[2]') == '$(-1, -3)$' and key_of('l10-turning-point', '.quiz[0]').startswith('$(1, 8)$, a maximum'), 'l10 read vertex'),
 (key_of('l10-turning-point', '.quiz[3]') == '$(0, 5)$' and key_of('review-3', '.items[1]').startswith('$(2, -5)$, a minimum'), 'vertex reads'),
 (sp.expand((x - 2) * (x - 4)) == x ** 2 - 6 * x + 8 and key_of('l11-meeting-the-axis', '.screens[6]') == '$(3, -1)$', 'l11 s6 vertex'),
 (sp.Rational(-3 + 5, 2) == 1 and key_of('l11-meeting-the-axis', '.screens[8]') == '$x = 1$', 'l11 s8 axis'),
 (solset(x ** 2 - (3 * x - 2)) == {1, 2} and key_of('l12-above-or-below', '.quiz[2]') == '$(1, 1)$ and $(2, 4)$', 'l12 meet'),
 (solset(x ** 2 - 4 * x + 7 - (2 * x - 2)) == {3} and key_of('homework-3', '.items[5]') == 'Once, at $(3, 4)$', 'homework-3 tangent'),
 (solset(x ** 2 - x + sp.Rational(1, 4)) == {sp.Rational(1, 2)}, 'l12 s1 touching at c = -0.25'),
 (sp.expand((p_ - 4) * (500 - 10 * p_)).subs(p_, 27) == 5290 and sp.solve(sp.diff((p_ - 4) * (500 - 10 * p_), p_), p_) == [27] and key_of('l13-best-price', '.screens[6]') == '£27.00', 'l13 s6 profit price'),
 (sp.solve(sp.diff(p_ * (900 - 30 * p_), p_), p_) == [15] and key_of('l13-best-price', '.screens[8]') == '£15.00', 'l13 s8'),
 (sp.expand(sp.Rational(1, 100) * w_ ** 2 + sp.Rational(9, 100) * (1 - w_) ** 2 - (sp.Rational(1, 10) * w_ ** 2 - sp.Rational(18, 100) * w_ + sp.Rational(9, 100))) == 0, 'l13 s9 variance'),
 (sp.expand(sp.Rational(1, 100) * w_ ** 2 + sp.Rational(4, 100) * (1 - w_) ** 2 - (sp.Rational(5, 100) * w_ ** 2 - sp.Rational(8, 100) * w_ + sp.Rational(4, 100))) == 0, 'l12 s9 variance'),
 (solset(sp.Rational(5, 100) * w_ ** 2 - sp.Rational(8, 100) * w_ + sp.Rational(3, 100), w_) == {sp.Rational(3, 5), 1}, 'l12 s9 roots'),
 (sp.expand(sp.Rational(1, 100) * w_ ** 2 + sp.Rational(4, 100) * (1 - w_) ** 2 + 2 * w_ * (1 - w_) * sp.Rational(1, 4) * sp.Rational(2, 100) - (sp.Rational(4, 100) * w_ ** 2 - sp.Rational(7, 100) * w_ + sp.Rational(4, 100))) == 0, 'homework-3 correlated variance'),
 ((sp.Rational(4, 100) * w_ ** 2 - sp.Rational(7, 100) * w_ + sp.Rational(4, 100)).subs(w_, sp.Rational(7, 8)) == sp.Rational(9375, 1000000), 'homework-3 least variance 0.009375'),
 (sp.expand((p_ - 5) * (2000 - 80 * p_) - (-80 * (p_ - 15) ** 2 + 8000)) == 0, 'homework-3 vendor square form'),
 (sp.expand(q * (50 - q) - 10 * q - 300 - (100 - (q - 20) ** 2)) == 0 and solset(q ** 2 - 40 * q + 375, q) == {15, 25}, 'homework-2 desk'),
 (sp.expand(q * (60 - 2 * q) - 12 * q - (-2 * q ** 2 + 48 * q)) == 0, 'homework-2 fixed cost profit'),
 (sp.expand(q * (25 - q / 2) - 7 * q - 160 - (-(q - 16) * (q - 20) / 2)) == 0, 'homework-1 profit'),
 (sp.expand(q * (16 - q) - 4 * q - 27 + (q - 3) * (q - 9)) == 0, 'l2 s8 profit'),
 (sp.expand(q * (30 - 2 * q) - 6 * q - 40 + 2 * (q - 2) * (q - 10)) == 0, 'l3 s8 profit'),
 (sp.expand(q * (30 - q) - 10 * q - 64 + (q - 4) * (q - 16)) == 0, 'l5 s9 profit'),
 (sp.expand(q * (26 - q) - 6 * q - 36 - (64 - (q - 10) ** 2)) == 0, 'l6 s8 profit'),
 (sp.expand(15 + 10 * t - 5 * t ** 2 - (-5 * (t - 1) ** 2 + 20)) == 0 and solset(15 + 10 * t - 5 * t ** 2, t) == {-1, 3}, 'problems-2 flare'),
 (sp.expand(t ** 2 - (6 * t - 10) - ((t - 3) ** 2 + 1)) == 0 and sp.expand(t ** 2 - 6 * t + 6 - ((t - 3) ** 2 - 3)) == 0, 'problems-2 bus'),
 (sp.expand((p_ - 8) * (150 - 5 * p_) - (605 - 5 * (p_ - 19) ** 2)) == 0, 'problems-3 bike square form'),
 (sp.expand(-sp.Rational(1, 5) * x * (x - 20) - (-sp.Rational(1, 5) * (x - 10) ** 2 + 20)) == 0, 'problems-3 arch'),
 (sp.expand(x ** 2 + 6 * x + 5 - ((x + 3) ** 2 - 4)) == 0 and solset(x ** 2 + 6 * x + 5) == {-1, -5}, 'l6 s3/s4'),
 (sp.expand(2 * x ** 2 + 8 * x + 1 - (2 * (x + 2) ** 2 - 7)) == 0 and sp.expand(x ** 2 + 10 * x + 18 - ((x + 5) ** 2 - 7)) == 0, 'square-form checks in review-3 and l10 quiz'),
 ((0.01 + 0.03 + 0.05) / 3 == 0.03 and abs(((0.01 ** 2 + 0.03 ** 2 + 0.05 ** 2) / 3 - 0.03 ** 2) - (0.0004 + 0 + 0.0004) / 3) < 1e-15, 'homework-1 variance example'),
 (abs(math.sqrt(0.009) - 0.0949) < 1e-4 and abs(math.sqrt(0.009375) - 0.0968) < 1e-4, 'stated volatilities'),
 (100 - 6 * 7.5 + 0.4 * 7.5 ** 2 == 77.5, 'homework-3 bond low point'),
]
for cond, what in facts:
    ok(bool(cond), 'fact: ' + what)

# multi item and the one reasoned option the audit calls true
m = get(DOC['l4-difference-of-squares'], '.quiz[3]')['widget']['options']
ok([z['text'] for z in m if z.get('correct')] == ['$x^2 - 36$', '$9x^2 - 1$', '$100 - x^2$'], 'l4 multi key')

# ---------------------------------------------------------------- E: canvases
def js2sym(expr, params):
    e = expr.replace('pow(', 'Pow(')
    return parse_expr(e, local_dict=dict(SYM, **{k: sp.nsimplify(v) for k, v in params.items()}, abs=sp.Abs, Pow=sp.Pow), transformations=TR)


canvas_fns = 0
for f in FILES:
    def walk(o, p):
        global canvas_fns
        if isinstance(o, dict):
            if o.get('kind') == 'plane' and isinstance(o.get('params'), dict):
                par = o['params'].get('params', {})
                xr = o['params'].get('x', [-5, 5])
                for fn in o['params'].get('functions', []):
                    lab = fn.get('label', '')
                    mm = re.fullmatch(r'\$y = ([^$]+)\$', lab)
                    if not mm:
                        continue
                    canvas_fns += 1
                    try:
                        lhs = js2sym(fn['expr'], {})
                        rhs = tex2sym(mm.group(1))
                    except Exception as ex:
                        ok(False, f'{f}{p}: cannot parse {fn["expr"]} / {lab}: {ex}')
                        continue
                    for i in range(201):
                        xv = sp.nsimplify(xr[0]) + (sp.nsimplify(xr[1]) - sp.nsimplify(xr[0])) * i / 200
                        d = (lhs - rhs).subs(SYM['x'], xv)
                        if d.free_symbols:
                            d = d.subs({s_: 1 for s_ in d.free_symbols})
                        if abs(float(d)) > 1e-9:
                            ok(False, f'{f}{p}: canvas {fn["expr"]} differs from label {lab} at x = {xv}')
                            break
                    else:
                        ok(True, '')
            for k, v in o.items():
                walk(v, p + '.' + k)
        elif isinstance(o, list):
            for i, z in enumerate(o):
                walk(z, p + '[%d]' % i)
    walk(DOC[f], '')
ok(canvas_fns >= 25, f'only {canvas_fns} labelled canvas functions checked')


def num(s):
    return float(s.replace('−', '-').replace('£', '').replace('$', ''))


TAB = [
 ('l5-product-of-zero', '.screens[0]', lambda r: (r[1] == r[0] - 2, r[2] == r[0] - 5, r[3] == (r[0] - 2) * (r[0] - 5))),
 ('l5-product-of-zero', '.screens[9]', lambda r: (r[1] == 30 - r[0], r[2] == r[0] * (30 - r[0]) - 10 * r[0] - 64)),
 ('l6-completing-the-square', '.screens[8]', lambda r: (r[1] == 26 - r[0], r[2] == -r[0] ** 2 + 20 * r[0] - 36)),
 ('l2-product-and-sum', '.screens[8]', lambda r: (r[1] == 16 - r[0], r[2] == r[0] * (16 - r[0]) - 4 * r[0] - 27)),
 ('l3-leading-coefficient', '.screens[8]', lambda r: (r[1] == 30 - 2 * r[0], r[2] == r[0] * (30 - 2 * r[0]) - 6 * r[0] - 40)),
]
for f, path, rule in TAB:
    for row in get(DOC[f], path)['canvas']['params']['rows']:
        r = [num(c) for c in row]
        ok(all(rule(r)), f'{f}{path}: table row {row}')
for f, path, cols in [('l2-product-and-sum', '.screens[1]', None), ('l3-leading-coefficient', '.screens[2]', None)]:
    rows = get(DOC[f], path)['canvas']['params']['rows']
    pairs = {tuple(int(v) for v in re.findall(r'-?\d+', r[0])) for r in rows}
    ok(pairs == {(a, 24 // a) for a in range(1, 5) if 24 % a == 0}, f'{f}{path}: pairs for 24 {pairs}')
rows = get(DOC['l2-product-and-sum'], '.screens[3]')['canvas']['params']['rows']
ok({tuple(int(v) for v in re.findall(r'-?\d+', r[0])) for r in rows} == {(1, -15), (-1, 15), (3, -5), (-3, 5)}, 'l2 s3 pairs for -15')
rows = get(DOC['l2-product-and-sum'], '.screens[4]')['canvas']['params']['rows']
ok({tuple(int(v) for v in re.findall(r'-?\d+', r[0])) for r in rows} == {(a, 20 // a) for a in (1, 2, 4, -1, -2, -4)}, 'l2 s4 pairs for 20')
# drag targets, sliders and sketches against their curves
ok(get(DOC['l9-shape-of-a-square'], '.screens[0]')['widget']['points'][0]['target'] == [3, 9], 'l9 s0 target')
ok(get(DOC['l9-shape-of-a-square'], '.screens[2]')['widget']['points'][0]['target'] == [4, 4], 'l9 s2 mirror')
ok(get(DOC['l9-shape-of-a-square'], '.screens[3]')['widget']['answer'] == 1 - 2 ** 2, 'l9 s3 slider k')
ok(get(DOC['l9-shape-of-a-square'], '.screens[4]')['widget']['answer'] == -2 / 4, 'l9 s4 slider a')
ok(get(DOC['l10-turning-point'], '.screens[0]')['widget']['points'][0]['target'] == [2, 1], 'l10 s0 vertex')
ok(get(DOC['l10-turning-point'], '.screens[5]')['widget']['answer'] == -2 * 3, 'l10 s5 slider b')
ok([z['target'] for z in get(DOC['l11-meeting-the-axis'], '.screens[0]')['widget']['points']] == [[1, 0], [5, 0]], 'l11 s0 roots')
ok(get(DOC['l11-meeting-the-axis'], '.screens[5]')['widget']['answer'] == 4, 'l11 s5 slider c')
ok([z['target'] for z in get(DOC['l12-above-or-below'], '.screens[2]')['widget']['points']] == [[-1, 1], [2, 4]], 'l12 s2 intersections')
ok(get(DOC['l13-best-price'], '.screens[0]')['widget']['answer'] == 25, 'l13 s0 slider')
tg = get(DOC['l13-best-price'], '.screens[9]')['widget']['points'][0]['target']
ok(tg[0] == 0.9 and abs(tg[1] - (0.1 * 0.81 - 0.18 * 0.9 + 0.09)) < 1e-12, 'l13 s9 vertex target')
for f, path, heights, xs in [('l9-shape-of-a-square', '.screens[5]', [-5, 0, 3, 4, 3, 0, -5], range(-3, 4)),
                             ('l11-meeting-the-axis', '.screens[3]', [5, 0, -3, -4, -3, 0, 5], range(-2, 5)),
                             ('review-3', '.items[7]', [-5, 0, 3, 4, 3, 0, -5], range(0, 7)),
                             ('homework-3', '.items[2]', [3.5, 0, -2.5, -4, -4.5, -4, -2.5, 0, 3.5], range(-3, 6))]:
    tgt = js2sym(get(DOC[f], path)['widget']['target'], {})
    ok([float(tgt.subs(SYM['x'], v)) for v in xs] == heights, f'{f}{path}: sketch heights')

# ---------------------------------------------------------------- F: fluency families, whole range
def fnum(v):
    return Fr(v).limit_denominator(10 ** 9) if not isinstance(v, str) else v


def ev(expr, env):
    e = expr.replace('^', '**')

    def _gcd(*a):
        return Fr(math.gcd(*[int(z) for z in a]))

    def _sqrt(a):
        a = Fr(a)
        rn, rd = math.isqrt(a.numerator), math.isqrt(a.denominator)
        if a >= 0 and rn * rn == a.numerator and rd * rd == a.denominator:
            return Fr(rn, rd)
        return math.sqrt(a)

    def _floor(a):
        return Fr(math.floor(a))
    return eval(e, {'__builtins__': {}}, dict(env, gcd=_gcd, abs=abs, sqrt=_sqrt, floor=_floor))


def polytex(v, cs):
    out = ''
    n_ = len(cs) - 1
    for i, c in enumerate(cs):
        c = Fr(c)
        if c == 0:
            continue
        k = n_ - i
        mag = abs(c)
        co = ('' if (mag == 1 and k > 0) else (str(mag.numerator) if mag.denominator == 1 else str(float(mag))))
        term = co + (v if k >= 1 else '') + ('^%d' % k if k >= 2 else '')
        out += ('-' if c < 0 else ('+' if out else '')) + term
    return out or '0'


def fmt(val, f_):
    if isinstance(val, str):
        return val
    if isinstance(val, float):
        if f_ and f_.startswith('dp'):
            return ('%.' + f_[2:] + 'f') % val
        return repr(val)
    val = Fr(val)
    plain = str(val.numerator) if val.denominator == 1 else (repr(float(val)) if (val.denominator & (val.denominator - 1) == 0 or val.denominator % 5 == 0 and set(sp.factorint(val.denominator)) <= {2, 5}) else '\\frac{%d}{%d}' % (val.numerator, val.denominator))
    if f_ is None:
        return plain
    if f_ == '+':
        return ('+' if val >= 0 else '') + plain
    if f_ == 'c':
        return '' if val == 1 else ('-' if val == -1 else plain)
    if f_ == '+c':
        return '+' if val == 1 else ('-' if val == -1 else (('+' if val >= 0 else '') + plain))
    if f_ == '()':
        return plain if val >= 0 else '(' + plain + ')'
    if f_ == 'frac':
        return str(val.numerator) if val.denominator == 1 else ('-' if val < 0 else '') + '\\frac{%d}{%d}' % (abs(val.numerator), val.denominator)
    if f_.startswith('dp'):
        return ('%.' + f_[2:] + 'f') % float(val)
    raise ValueError(f_)


def render(tpl, env):
    out, i = '', 0
    while i < len(tpl):
        ch = tpl[i]
        if tpl.startswith('{{', i):
            out += '{'; i += 2; continue
        if tpl.startswith('}}', i) and not tpl.startswith('}}}', i + 0) or (tpl.startswith('}}', i)):
            out += '}'; i += 2; continue
        if ch == '{':
            j = tpl.index('}', i)
            body = tpl[i + 1:j]
            if body.startswith('poly('):
                args = body[5:-1].split(';')
                v = env.get(args[0].strip(), args[0].strip())
                out += polytex(v, [ev(a, env) for a in args[1].split(',')])
            else:
                mm = re.fullmatch(r'(.*?)(?::(\+c|\+|c|\(\)|frac|dp\d+))?', body)
                out += fmt(ev(mm.group(1), env), mm.group(2))
            i = j + 1
            continue
        out += ch; i += 1
    return out


def draws(fam):
    names, pools = [], []
    for k, spec in fam['vars'].items():
        if 'int' in spec:
            pool = list(range(spec['int'][0], spec['int'][1] + 1, spec.get('step', 1)))
        else:
            pool = list(dict.fromkeys(spec['pick']))
        pool = [z for z in pool if z not in spec.get('not', [])]
        names.append(k); pools.append(pool)
    # the variable letter never changes the mathematics except by renaming: keep the first letter and,
    # for families whose letter list holds the name of a numeric var, also that letter
    for combo in itertools.product(*pools):
        env = {k: (Fr(z) if not isinstance(z, str) else z) for k, z in zip(names, combo)}
        try:
            good = True
            pre = [c for c in fam.get('where', []) if not any(re.search(r'\b%s\b' % l, c) for l in fam.get('let', {}))]
            for c in pre:
                if not ev(c, env):
                    good = False; break
            if not good:
                continue
            for k, e in fam.get('let', {}).items():
                env[k] = ev(e, env)
            if all(ev(c, env) for c in fam.get('where', [])):
                yield env
        except ZeroDivisionError:
            continue


def V(env):
    return sp.Symbol(env['v']) if 'v' in env else sp.Symbol('x')


def psym(s, env):
    """Parse rendered tex in the family's letter (which may clash with a numeric var name)."""
    return tex2sym(s)


def I(z):
    return sp.Rational(Fr(z).numerator, Fr(z).denominator)


def roots_of(e, v):
    return sorted(sp.solve(e, v), key=lambda z: float(z))


def close_sets(a, b, tol=0.005):
    a, b = sorted(float(z) for z in a), sorted(float(z) for z in b)
    return len(a) == len(b) and all(abs(u - w2) <= tol for u, w2 in zip(a, b))


def truth(fid, env):
    """Independent key and slips from the vars alone: (key, {slip id: value})."""
    v = V(env)
    g = lambda k: I(env[k])
    if fid == 'fluency-l1-two-brackets/expand-monic':
        a_, b_ = g('a'), g('b')
        return sp.expand((v + a_) * (v + b_)), {'firsts-lasts': v ** 2 + a_ * b_, 'swapped': v ** 2 + a_ * b_ * v + a_ + b_}
    if fid == 'fluency-l1-two-brackets/expand-coefficient':
        P, Q, R_, S_ = g('p'), g('q'), g('r'), g('s')
        return sp.expand((P * v + Q) * (R_ * v + S_)), {'firsts-lasts': P * R_ * v ** 2 + Q * S_, 'added-numbers': P * R_ * v ** 2 + (Q + S_) * v + Q * S_}
    if fid == 'fluency-l1-two-brackets/expand-square':
        a_ = g('a')
        return sp.expand((v + a_) ** 2), {'squares-only': v ** 2 + a_ ** 2, 'one-strip': v ** 2 + a_ * v + a_ ** 2}
    if fid == 'fluency-l2-product-and-sum/factorise-monic':
        P, Q = g('p'), g('q')
        return (v + P) * (v + Q), {'signs-swapped': (v - P) * (v - Q), 'one-sign': (v + P) * (v - Q)}
    if fid == 'fluency-l2-product-and-sum/perfect-square':
        P = g('p')
        return (v + P) ** 2, {'wrong-sign': (v - P) ** 2, 'difference': (v + P) * (v - P)}
    if fid == 'fluency-l3-leading-coefficient/factorise-non-monic':
        P, Q, S_ = g('p'), g('q'), g('s')
        return (P * v + Q) * (v + S_), {'skipped-grouping': (v + P * S_) * (v + Q), 'numbers-swapped': (P * v + S_) * (v + Q)}
    if fid == 'fluency-l3-leading-coefficient/split-product':
        P, Q, R_, S_ = g('p'), g('q'), g('r'), g('s')
        co = sp.Poly(sp.expand((P * v + Q) * (R_ * v + S_)), v).all_coeffs()
        return co[0] * co[2], {'last-term-only': co[2], 'the-sum': co[1]}
    if fid == 'fluency-l3-leading-coefficient/common-factor-first':
        K, P, Q, S_ = g('k'), g('p'), g('q'), g('s')
        return K * (P * v + Q) * (v + S_), {'factor-dropped': (P * v + Q) * (v + S_), 'factor-sign': -K * (P * v + Q) * (v + S_), 'numbers-swapped': K * (P * v + S_) * (v + Q)}
    if fid == 'fluency-l4-difference-of-squares/square-minus-number':
        P, Q = g('p'), g('q')
        return (P * v + Q) * (P * v - Q), {'squared-difference': (P * v - Q) ** 2, 'squared-sum': (P * v + Q) ** 2}
    if fid == 'fluency-l4-difference-of-squares/number-minus-square':
        P, Q = g('p'), g('q')
        return (Q + P * v) * (Q - P * v), {'order-swapped': (P * v + Q) * (P * v - Q), 'squared-difference': (Q - P * v) ** 2}
    if fid == 'fluency-l4-difference-of-squares/mental-difference':
        A_, B_ = (g('s') + g('d')) / 2, (g('s') - g('d')) / 2
        return A_ ** 2 - B_ ** 2, {'difference-squared': (A_ - B_) ** 2, 'sum-only': A_ + B_}
    if fid == 'fluency-l4-difference-of-squares/common-factor-first':
        K, P, Q = g('k'), g('p'), g('q')
        return K * (P * v + Q) * (P * v - Q), {'factor-dropped': (P * v + Q) * (P * v - Q), 'squared-difference': K * (P * v - Q) ** 2}
    if fid == 'fluency-l6-completing-the-square/find-the-constant':
        H, C = g('h'), g('c')
        return C - H ** 2, {'added-corner': C + H ** 2, 'b-not-halved': C - (2 * H) ** 2}
    if fid == 'fluency-l6-completing-the-square/solve-by-square':
        H, K = g('h'), g('k')
        return roots_of(v ** 2 - 2 * H * v + H ** 2 - K ** 2, v), {'centre-sign': [-H - K, -H + K], 'no-square-root': [H - K ** 2, H + K ** 2]}
    if fid == 'fluency-l6-completing-the-square/square-form':
        B_, C = g('b'), g('c')
        return v ** 2 + B_ * v + C, {'added-corner': (v + B_ / 2) ** 2 + C + B_ ** 2 / 4, 'b-not-halved': (v + B_) ** 2 + C - B_ ** 2}
    if fid == 'fluency-l6-completing-the-square/largest-value':
        H, C = g('h'), g('c')
        e = -v ** 2 + 2 * H * v + C
        vx = sp.solve(sp.diff(e, v), v)[0]
        return e.subs(v, vx), {'corner-sign': C - H ** 2, 'gave-the-input': vx}
    if fid == 'fluency-l7-the-formula/discriminant':
        A_, B_, C = g('a'), g('b'), g('c')
        return B_ ** 2 - 4 * A_ * C, {'sign-of-4ac': B_ ** 2 + 4 * A_ * C, 'dropped-four': B_ ** 2 - A_ * C}
    if fid == 'fluency-l7-the-formula/rational-roots':
        P, Q, S_ = g('p'), g('q'), g('s')
        A_, B_, C = P, -(P * S_ + Q), Q * S_
        sd = sp.sqrt(B_ ** 2 - 4 * A_ * C)
        return roots_of(A_ * v ** 2 + B_ * v + C, v), {'b-for-minus-b': [(B_ - sd) / (2 * A_), (B_ + sd) / (2 * A_)], 'halved-root-only': [-B_ - sd / (2 * A_), -B_ + sd / (2 * A_)]}
    if fid in ('fluency-l7-the-formula/decimal-roots', 'fluency-l7-the-formula/exact-roots'):
        A_, B_, C = g('a'), g('b'), g('c')
        sd = sp.sqrt(B_ ** 2 - 4 * A_ * C)
        sl = {'b-for-minus-b': [(B_ - sd) / (2 * A_), (B_ + sd) / (2 * A_)], 'halved-root-only': [-B_ - sd / (2 * A_), -B_ + sd / (2 * A_)],
              'over-a': [(-B_ - sd) / A_, (-B_ + sd) / A_]}
        return roots_of(A_ * v ** 2 + B_ * v + C, v), sl
    raise KeyError(fid)


FLU = ['fluency-l1-two-brackets', 'fluency-l2-product-and-sum', 'fluency-l3-leading-coefficient',
       'fluency-l4-difference-of-squares', 'fluency-l6-completing-the-square', 'fluency-l7-the-formula']
fam_counts = {}
for fl in FLU:
    doc = load(fl)
    for fam in doc['families']:
        fid = fl + '/' + fam['id']
        seen = set()
        cnt = bad = 0
        for env in draws(fam):
            # one letter is enough: the letter only renames the variable
            sig = tuple((k, str(z)) for k, z in env.items() if k != 'v' and k in fam['vars'])
            if sig in seen:
                continue
            seen.add(sig)
            if 'v' in env:
                env = dict(env, v='x')
            cnt += 1
            key, slips = truth(fid, env)
            w = fam['widget']
            v = V(env)
            try:
                prompt = render(fam['prompt'], env)
                # the prompt states the task the key answers
                pm = maths(prompt)
                if w['kind'] == 'expression' and 'answers' not in w:
                    ans = tex2sym(render(w['answer'], env))
                    good = same(ans, key)
                    # the prompt's own expression is the same polynomial (first maths, before any '=')
                    task = tex2sym(pm[0].split('=')[0])
                    good = good and same(task, key)
                    if w.get('form') == 'factorised-fully':
                        good = good and not content_gt1(render(w['answer'], env))
                    if w.get('form') == 'completed-square':
                        good = good and same(sp.Poly(ans, v).all_coeffs()[1] / 2, sp.Rational(Fr(env['b']).numerator, Fr(env['b']).denominator) / 2)
                    for acc in w.get('accept', []):
                        good = good and same(tex2sym(render(acc, env)), key)
                elif w['kind'] == 'expression':
                    ans = [tex2sym(render(a_, env)) for a_ in w['answers']]
                    good = close_sets(ans, key, 1e-9) and all(same(a_, b_) for a_, b_ in zip(sorted(ans, key=float), key))
                    task = tex2sym(pm[0].split('=')[0])
                    good = good and all(sp.simplify(task.subs(v, r_)) == 0 for r_ in key)
                elif 'answers' in w:
                    ans = [ev(a_.strip('{}'), env) for a_ in w['answers']]
                    good = close_sets(ans, key, 1e-9)
                    task = tex2sym(pm[0].split('=')[0])
                    good = good and all(abs(float(task.subs(v, r_))) < 1e-9 for r_ in key)
                else:
                    ans = ev(render(w['answer'], env), {}) if False else ev(w['answer'].strip('{}'), env)
                    good = abs(float(ans) - float(key)) < 1e-9
                    if fid.endswith('find-the-constant'):
                        task = tex2sym(pm[0].split('=')[0]); form = tex2sym(pm[0].split('=')[1].replace('+ q', ''))
                        good = good and same(task - form, key)
                    if fid.endswith('largest-value'):
                        task = tex2sym(pm[0])
                        good = good and sp.maximum(task, v) == key
                    if fid.endswith('discriminant'):
                        co = sp.Poly(tex2sym(pm[0].split('=')[0]), v).all_coeffs()
                        co = [0] * (3 - len(co)) + co
                        good = good and (len(co) == 3 and co[1] ** 2 - 4 * co[0] * co[2] == key)
                    if fid.endswith('split-product'):
                        co = sp.Poly(tex2sym(pm[0]), v).all_coeffs()
                        good = good and co[0] * co[2] == key
                    if fid.endswith('mental-difference'):
                        good = good and tex2sym(pm[0]) == key
                if not good:
                    bad += 1
                    if bad <= 2:
                        fails.append(f'{fid}: key wrong for {dict((k, str(z)) for k, z in env.items() if k in fam["vars"])}: {prompt}')
                offered = []
                for x_ in fam.get('wrong', []):
                    if 'when' in x_ and not ev(x_['when'], env):
                        continue
                    exp = slips[x_['id']]
                    if 'tex' in x_:
                        r_ = render(x_['tex'], env)
                        if isinstance(exp, list):
                            got = [tex2sym(z) for z in r_.split(', ')]
                            g2 = close_sets(got, exp, 1e-9); neq = not close_sets(got, key, 1e-9)
                        else:
                            got = tex2sym(r_); g2 = same(got, exp); neq = not same(got, key)
                        offered.append(sp.srepr(sp.expand(got)) if not isinstance(got, list) else str(sorted(float(z) for z in got)))
                    else:
                        r_ = render(x_['value'], env)
                        if isinstance(exp, list):
                            got = [float(z) for z in r_.split(', ')]
                            g2 = close_sets(got, exp, 2e-6); neq = not close_sets(got, key, w.get('tol', {}).get('abs', 0) + 1e-9)
                        else:
                            got = float(ev(x_['value'].strip('{}'), env)); g2 = abs(got - float(exp)) < 1e-9; neq = abs(got - float(key)) > w.get('tol', {}).get('abs', 0) + 1e-9
                        offered.append(str(got))
                    if not (g2 and neq):
                        bad += 1
                        if bad <= 3:
                            fails.append(f'{fid}: slip {x_["id"]} {"is not what its line names" if not g2 else "equals the key"} for {dict((k, str(z)) for k, z in env.items() if k in fam["vars"])}: {r_}')
                    render(x_['line'], env)
                if len(set(offered)) != len(offered):
                    bad += 1
                    if bad <= 3:
                        fails.append(f'{fid}: two slips coincide for {dict((k, str(z)) for k, z in env.items() if k in fam["vars"])}')
                for line in fam.get('solution', []):
                    render(line, env)
            except Exception as ex:
                bad += 1
                if bad <= 2:
                    fails.append(f'{fid}: {type(ex).__name__} {ex} for {dict((k, str(z)) for k, z in env.items() if k in fam["vars"])}')
        fam_counts[fid] = (cnt, bad)
        ok(cnt > 0, f'{fid}: no draws')
        if bad == 0:
            passed += cnt
        else:
            fails.append(f'{fid}: {bad} of {cnt} draws fail')
ok(len(fam_counts) == 20, f'fluency families checked {len(fam_counts)}')

# ---------------------------------------------------------------- G: randomised sweep of the rules
random.seed(20261126)
for _ in range(20000):
    a_, b_, c_ = (random.choice([z for z in range(-9, 10) if z]) for _ in range(3))
    xv = random.uniform(-10, 10)
    h_, k_ = -b_ / (2 * a_), c_ - b_ * b_ / (4 * a_)
    if abs(a_ * xv * xv + b_ * xv + c_ - (a_ * (xv - h_) ** 2 + k_)) > 1e-7:
        fails.append('vertex form identity'); break
    val = a_ * xv * xv + b_ * xv + c_
    if (a_ > 0 and val < k_ - 1e-9) or (a_ < 0 and val > k_ + 1e-9):
        fails.append('vertex is not the extreme value'); break
    disc = b_ * b_ - 4 * a_ * c_
    n_real = 2 if disc > 0 else (1 if disc == 0 else 0)
    if n_real != len(set(sp.Poly(a_ * x ** 2 + b_ * x + c_, x).real_roots())) and _ < 400:
        fails.append('discriminant count'); break
    if a_ * c_ < 0 and disc <= 0:
        fails.append('opposite signs of a and c must give two roots'); break
    p0, q0 = sorted((b_, c_))
    inside = p0 < xv < q0
    if ((xv - p0) * (xv - q0) < 0) != inside:
        fails.append('sign of a factorised quadratic'); break
    r_ = random.uniform(0, 0.5)
    if abs((1 + r_) * (1 - r_) - (1 - r_ * r_)) > 1e-12:
        fails.append('up then down'); break
else:
    passed += 20000

print(f'quadratics L1-3 concepts r2: {passed} checks passed, {len(fails)} failed')
print('numeric widgets', seen_numeric, '| expand/factorise choices', covered_B, '| expression widgets', seen_expr, '| labelled canvas functions', canvas_fns)
for k_, (c_, b_) in fam_counts.items():
    print(f'  {k_}: {c_} draws, {b_} bad')
for z in fails[:60]:
    print('FAIL', z)
sys.exit(1 if fails else 0)
