#!/usr/bin/env python3
"""Concept audit, equations levels 1 to 3 (audit name equations-1-3, round 1).

Recomputes, from each item's own givens, every graded numeric key, every numeric slip
value, every drag target, every table cell, the algebra of the expression and choice
items, the solution set of every inequality item, and each fluency family over its whole
variable range. Nothing here is copied from the author's scripts.

Run from anywhere:  python docs/reports/equations-L1-3-concepts.py [--rows]
Exit 0 when every check passes. A check that fails because the content is wrong stays
failing. `--rows` prints one ledger row per check (used to build the ledger).

There is no empirical or statistical claim in these levels, so there is no Monte Carlo
part; the one "testing" claim (a wrong simplification can pass at one test value) is
checked exactly in check_test_value().
"""
import json, math, os, re, sys, itertools
from fractions import Fraction as Fr
import sympy as sp
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
                                        implicit_multiplication, split_symbols, convert_xor, rationalize)

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'equations')
ROWS = '--rows' in sys.argv
fails, rows, nchecks = [], [], 0


def load(f):
    return json.load(open(os.path.join(BASE, f + '.json')))


def at(doc, loc):
    o = doc
    for tok in re.findall(r'[A-Za-z_]+|\[\d+\]', loc):
        o = o[int(tok[1:-1])] if tok[0] == '[' else o[tok]
    return o


def check(ok, f, path, claim, basis):
    global nchecks
    nchecks += 1
    rows.append((f, path, claim, 'correct' if ok else 'wrong', basis))
    if not ok:
        fails.append(f'{f} | {path} | {claim} | {basis}')


def close(a, b, tol=0.006):
    return abs(float(a) - float(b)) <= tol


# ---------------------------------------------------------------- numeric keys and slips
# file -> { locator: (key, {slip id: value}) }, each value worked from the item's givens.
NUM = {
 'l1-letters-for-numbers': {
  'screens[0]': (3*5+4, {'added': 3+5+4, 'all-envelopes': (3+4)*5, 'coins-inside': 3*(5+4), 'one-envelope': 5+4}),
  'screens[1]': (3*6+4, {'added': 3+6+4, 'one-envelope': 6+4, 'coins-inside': 3*(6+4), 'old': 3*5+4}),
  'screens[4]': (3+2*50, {'side-by-side': 3+250, 'plus-first': (3+2)*50, 'added': 3+2+50}),
  'quiz[1]': (4+3*0, {'three': 4+3, 'side-by-side': 4+30, 'all-zero': (4+3)*0}),
  'quiz[3]': (5*6-4, {'side-by-side': 56-4, 'subtract-first': (5-4)*6, 'added': 5+6-4}),
 },
 'l2-like-terms': {
  'screens[1]': (2*4+3+4+5, {'lost-one': 2*4+8, 'times': 3*4+3*5, 'tray-a': 2*4+3}),
  'screens[5]': (4*2+7+2*2+3, {'sams': 16*2, 'old': 4+7+2+3}),
 },
 'l3-opening-brackets': {
  'screens[0]': (3*(5+2), {'first-only': 3*5+2, 'added': 3+5+2, 'left-only': 3*5}),
  'quiz[2]': (7*(6+4), {'first-only': 7*6+4, 'added': 7+6+4}),
 },
 'l4-putting-brackets-back': {
  'screens[7]': (math.gcd(8, 20), {'two': 2, 'eight': 8, 'twenty': 20}),
  'screens[9]': (600/15, {'subtract': 600-15, 'times': 600*15, 'add': 600+15}),
 },
 'l5-keeping-the-balance': {
  'screens[5]': (8+3, {'subtracted': 8-3}),
  'screens[9]': (1286/40, {'times': 1286*40, 'minus': 1286-40, 'flipped': 40/1286}),
  'quiz[0]': (9.1-2.75, {'added': 9.1+2.75}),
  'quiz[1]': (27/6, {'multiplied': 27*6, 'subtracted': 27-6, 'flipped': 6/27}),
  'quiz[2]': (3*4.2, {'divided': 4.2/3}),
 },
 'l6-undoing-in-reverse': {
  'screens[3]': ((30-6)/4, {'half-divided': 30/4-6, 'added': (30+6)/4, 'multiplied': (30-6)*4}),
  'screens[4]': (9*3-2, {'wrong-order': (9-2)*3, 'divided': 9/3-2, 'plus': 9*3+2}),
  'screens[5]': ((7-15)/2, {'sign': (15-7)/2, 'added': (7+15)/2}),
  'screens[8]': ((1287.5-12.5)/4.25, {'added-fee': (1287.5+12.5)/4.25, 'no-fee': 1287.5/4.25, 'divide-first': 1287.5/4.25-12.5}),
  'quiz[0]': ((50-11)/6, {'added': (50+11)/6, 'half-divided': 50/6-11}),
  'quiz[1]': ((4+3)*5, {'subtracted': (4-3)*5, 'divided': (4+3)/5}),
  'quiz[2]': ((9+7)/4, {'subtracted': (9-7)/4}),
  'quiz[3]': (3*2+4, {'wrong-order': (3+4)*2, 'divided': 3/2+4}),
 },
 'l7-unknowns-both-sides': {
  'screens[3]': ((18-3)/(7-2), {'kept-sign': (18-3)/(7+2), 'added-three': (18+3)/(7-2), 'two-slips': (18+3)/(7+2)}),
  'screens[8]': ((300*13.1+200*12.4)/500, {'short-as-long': (300*13.1-200*12.4)/100, 'average': (12.4+13.1)/2}),
  'quiz[0]': ((12+3)/(8-5), {'kept-sign': (12+3)/(8+5), 'constant-sign': (12-3)/(8-5)}),
  'quiz[1]': ((14+6)/(4-2), {'bracket': (7+6)/(4-2)}),
  'quiz[3]': ((9.2-4)/(1.5-0.5), {'kept-sign': (9.2-4)/(1.5+0.5)}),
 },
 'l8-clearing-fractions': {
  'screens[0]': (10/(1/2+1/3), {'times-six': 10*6, 'one-sixth': 10/5, 'added-denoms': 10*5}),
  'screens[2]': ((3+8)/(4-3), {'lost-bracket': (1+2)/(4-3), 'swapped': (-6-4)/(4-3)}),
  'screens[3]': ((6+24)/(4-1), {'fractions-only': (1+4)/3, 'missed-one': (1+24)/3, 'missed-four': (6+4)/3}),
  'screens[4]': ((15+3)/(5-2), {'missed-term': (15+0.3)/3, 'sign': (15-3)/3}),
  'screens[7]': (8750/(1-1/3-1/4), {'invested': 8750/(1/3+1/4), 'stopped': 8750*12, 'times': 8750*(1/3+1/4)}),
  'quiz[0]': (2/(1/4+1/12), {'added-denoms': 2*16}),
  'quiz[1]': (2/(1/3-1/5), {'missed-two': 2/(5-3)}),
  'quiz[2]': ((6+12)/(4-1), {'sign': (6-12)/(4-1)}),
 },
 'l9-story-to-equation': {
  'screens[2]': (1800/(6+2*4.5), {'no-double': 1800/(6+4.5), 'other-batch': 2*1800/15, 'all': 3*1800/15}),
  'screens[3]': ((17+5)/2, {'reversed': (5-17)/2, 'bracket': 17/2+5, 'subtracted': (17-5)/2}),
  'screens[5]': ((1613-5)/(8*1.005), {'no-commission': (1613-5)/8, 'percent-as-whole': (1613-5)/(8*1.5)}),
  'screens[6]': (math.floor((1500-5)/8.04), {'rounded-up': math.ceil((1500-5)/8.04), 'unrounded': (1500-5)/8.04}),
  'screens[8]': (math.ceil(150/(100*0.06-2*100*0.01)), {'one-way': 150/(6-1), 'rounded-down': math.floor(150/4), 'unrounded': 150/4, 'no-fees': 150/6}),
  'quiz[1]': ((257.5-7.5)/2.5, {'added-fee': (257.5+7.5)/2.5, 'no-fee': 257.5/2.5}),
  'quiz[2]': (20/(8-3), {'no-per-user': 20/8, 'added': 20/(8+3)}),
  'quiz[3]': ((15-3)*2, {'added': (15+3)*2, 'halved': (15-3)/2}),
 },
 'l10-ranges-of-answers': {
  'screens[4]': (math.ceil(-2.5), {'outside': -3, 'not-whole': -2.5}),
  'screens[8]': (22.00-0.01, {'included': 22.00, 'tenth': 22.00-0.10}),
 },
 'l11-one-twist': {
  'quiz[3]': (math.floor((10-4)/3)+1, {'boundary': (10-4)/3, 'kept': (10-4)/3-1}),
 },
 'l12-trapped': {
  'screens[4]': (4-(-1), {'both-ends': 6, 'no-ends': 4, 'subtract': 4-1}),
  'screens[7]': (120-(-200), {'to-zero': 120, 'limit-only': 200, 'flipped': 200-120}),
  'screens[8]': (math.floor((5000-800)/450), {'not-whole': (5000-800)/450, 'no-buffer': math.floor(5000/450), 'added-buffer': math.floor((5000+800)/450), 'rounded-up': math.ceil((5000-800)/450)}),
  'quiz[1]': (len(range(-3, 2)), {'both': 6, 'neither': 4}),
 },
 'l13-changing-the-subject': {
  'screens[1]': (250/(2000*0.05), {'principal': 250/2000, 'rate': 250/0.05}),
  'screens[4]': (1200/(9.5-5.5), {'price-only': 1200/9.5, 'cost-only': 1200/5.5, 'added': 1200/(9.5+5.5)}),
  'screens[8]': (6000/(0.25*48), {'no-rate': 6000/48, 'times-rate': 6000*0.25/48, 'all-times': 6000*0.25*48}),
  'quiz[2]': (66/1.10, {'off-exit': 66*0.90, 'times': 66*1.10}),
 },
 'review-1': {
  'items[4]': (4+3*2**2, {'square-3n': 4+(3*2)**2, 'add-first': (4+3)*2**2}),
  'items[8]': (90/(4.5-2.25), {'no-unit-cost': 90/4.5, 'added-cost': 90/(4.5+2.25)}),
 },
 'review-2': {
  'items[0]': (12.3+4.65, {'subtracted': 12.3-4.65}),
  'items[1]': ((19+8)/3, {'subtracted': (19-8)/3, 'half-divided': 19/3+8}),
  'items[3]': ((18+4)/(9-5), {'kept-sign': (18+4)/(9+5)}),
  'items[4]': (14/(1/3+1/4), {'added-denoms': 14*7, 'no-right': 14/7}),
  'items[5]': ((2150-400)/2, {'asha': (2150-400)/2+400, 'half': 2150/2}),
  'items[7]': ((24-8-3)/(4-3), {'minus-slip': (24-8+3)/(4-3), 'lost-bracket': (24-2+1)/(4-3)}),
  'items[8]': ((6-1.5)/(0.025-0.01), {'added': (6-1.5)/(0.025+0.01), 'one-rate': (6-1.5)/0.025, 'pence': (6-1.5)/(2.5-1)}),
  'items[9]': (math.ceil(500/(7.5-1.1)), {'rounded-down': math.floor(500/6.4), 'unrounded': 500/6.4, 'no-cost': 500/7.5}),
 },
 'review-3': {
  'items[3]': (len([x for x in range(-20, 20) if -2 <= 3*x+1 < 10]), {'took-three': 5, 'dropped-low': 3}),
  'items[5]': (45.60/0.95, {'times': 45.60*1.05, 'off-exit': 45.60*0.95}),
  'items[6]': ((100-80)/4, {'smallest': (100-92)/4, 'sign': -(100-92)/4}),
  'items[7]': (math.floor(2000/8)+1, {'break-even': 2000/8}),
 },
 'homework-1': {
  'items[1]': (2.25+0.03*1250, {'fee-each': (2.25+0.03)*1250, 'pence': 2.25+3*1250, 'no-fee': 0.03*1250}),
  'items[5]': (120/0.04, {'four': 120/4, 'point-four': 120/0.4, 'times': 120*0.04}),
  'items[7]': (2.5/(0.12-0.02), {'no-share-cost': 2.5/0.12, 'added-cost': 2.5/(0.12+0.02), 'fee-only': 2.5/0.02}),
 },
 'homework-2': {
  'items[0]': ((22-7)/-3, {'sign': (22-7)/3, 'added': (22+7)/-3}),
  'items[1]': ((35+3)/(9-5), {'lost-bracket': (7+1)/(9-5), 'swapped': (21+5)/(15-3)}),
  'items[3]': (math.ceil((500*3.84+6+6)/500*100)/100, {'short': math.floor((500*3.84+12)/500*100)/100, 'unrounded': (500*3.84+12)/500, 'no-fees': 3.84}),
  'items[4]': (math.ceil((5000+7.95)/(16*(1-0.0025))), {'under': math.floor(5007.95/15.96), 'unrounded': 5007.95/15.96, 'percent-as-whole': math.ceil(5007.95/(16*0.75))}),
  'items[5]': ((26000-20000)/(350+150), {'one-fund': 6000/150, 'other-fund': 6000/350, 'kept-sign': 6000/(350-150)}),
  'items[7]': ((1380-120)/3, {'monday': 2*(1380-120)/3+120, 'half': (1380-120)/2, 'added': (1380+120)/3}),
 },
 'homework-3': {
  'items[1]': (52*(1-0.06), {'pounds': 52-6, 'above': 52*1.06, 'drop': 52*0.06}),
  'items[2]': (len([x for x in range(-50, 50) if 2*x-3 < 9 and 5-x <= 7]), {'took-six': 9, 'dropped-low': 7}),
  'items[3]': (len([n for n in range(0, 50) if 12000-1500*n >= 0.25*12000 and n >= 2]), {'no-buffer': len([n for n in range(2, 50) if 1500*n <= 12000]), 'subtract': 6-2, 'from-one': 6}),
  'items[6]': (max(x for x in range(-50, 50) if Fr(2*x-1, 3) < Fr(x+4, -2)), {'rounded': round(-10/7), 'dropped-minus': max(x for x in range(-50, 50) if Fr(2*x-1, 3) < Fr(x+4, 2)), 'boundary': -10/7, 'sign': 2}),
 },
 'problems-1': {
  'items[0].parts[3]': (2*18+3*(18-5), {'five-off': 5*18-5, 'sign': 5*(18+3), 'no-child': 5*18}),
  'items[1].parts[3]': ((6.5-2.3)*90-45+(6.5-2.3)*70-45, {'carried': 8.4*90-110, 'one-pitch': 8.4*90-129, 'sunday': 8.4*70-174}),
  'items[2].parts[2]': (5*(7+4)-3*(7-2), {'sign': 2*7+14, 'one-term': 2*(7+26), 'letter': 2*7*14, 'half': 2*7+13}),
  'items[3].parts[3]': (4*16+3*4*6, {'squared-last': (7*4)**2+6*4, 'doubled': 7*(2*4)+6*4, 'three-reach': 7*16+2*4}),
 },
 'problems-2': {
  'items[0].parts[1]': ((213-45)/8, {'no-fee': 213/8, 'add-fee': (213+45)/8}),
  'items[0].parts[2]': (math.floor((300-45)/8), {'rounded-up': round((300-45)/8), 'no-fee': math.floor(300/8)}),
  'items[0].parts[3]': (math.floor((300-45)/35*100)/100, {'rounded-up': round((300-45)/35, 2), 'no-fee': 300/35, 'pence': 728}),
  'items[1].parts[1]': ((150+600)/(6-5), {'lone-twenty': (150+20)/(6-5), 'top': (30+600)/(6-5), 'carried-plus': (150-600)/(6-5)}),
  'items[1].parts[2]': ((750+30)/6, {'no-bed': 750/6, 'old-share': 750/5}),
  'items[1].parts[3]': ((780+30)/7, {'no-bed': 780/7, 'six': 810/6}),
  'items[2].parts[0]': (216/30, {'times': 216*30, 'minus': 216-30}),
  'items[2].parts[1]': (45/(30-24), {'one-rate': 45/24, 'added': 45/(30+24), 'sign': -45/6}),
  'items[2].parts[3]': ((30*9)-(45+24*9), {'unit-gap': 9-7.5, 'no-charge': 30*9-24*9}),
  'items[3].parts[2]': ((0.065*12000-660)/(0.065-0.04), {'sign': -4800, 'bracket-sign': (660000-780000)/(40+65), 'rhs': (660-780000)/(40-65)}),
  'items[3].parts[3]': ((780-720)/0.025, {'sign': -2400, 'added': (780+720)/0.025, 'old': 4800}),
 },
 'problems-3': {
  'items[0].parts[3]': (len([h for h in range(0, 50) if h > 4 and 240-18*h >= 60]), {'with-four': 7, 'no-ten': 5}),
  'items[1].parts[1]': ((41-32)/1.8, {'order': 41/1.8-32, 'sign': (41+32)/1.8, 'times': (41-32)*1.8}),
  'items[1].parts[3]': (len([F for F in range(-200, 200) if -25 <= (F-32)/1.8 <= -15]), {'gap': 5-(-13), 'celsius': len(range(-25, -14)), 'both-out': 17}),
  'items[2].parts[1]': ((24000-9600)/2400, {'value-only': 9600/2400, 'sign': -6, 'added': (24000+9600)/2400}),
  'items[2].parts[4]': (len([t for t in range(0, 50) if 6000 < 24000-2400*t <= 19200]), {'no-two': 5, 'rounded-up': 7}),
  'items[3].parts[1]': (0.4*6000/(1-0.4), {'dropped': 0.4*6000, 'sign': 0.4*6000/1.4}),
  'items[3].parts[2]': (0.25*6000/0.75, {'dropped': 0.25*6000, 'sign': 0.25*6000/1.25}),
  'items[3].parts[3]': (len([n for n in range(0, 100) if 2000 <= 250*n <= 4000]), {'gap': 16-8, 'both-out': 7}),
 },
}
# table widgets: locator -> list of answers in row order
TAB = {
 'l6-undoing-in-reverse': {'screens[1]': [25+7, (25+7)/4]},
 'l7-unknowns-both-sides': {'screens[7]': [5*(5-1), 2*5+13, 5*(6-1), 2*6+13]},
 'l9-story-to-equation': {'screens[0]': [3.2+1.85*5, 3.2+1.85*6, 3.2+1.85*7]},
 'l13-changing-the-subject': {'screens[0]': [2000*0.05*3, 1500*0.04*2, 800*0.025*4], 'screens[7]': [52.5/1.05, 38.4/0.96, 121/1.10]},
 'homework-3': {'items[5]': [900/(12-7), 2400/(15.5-9.5), 750/(4.25-2.75)]},
}
FILES = ['l1-letters-for-numbers', 'l2-like-terms', 'l3-opening-brackets', 'l4-putting-brackets-back',
         'l5-keeping-the-balance', 'l6-undoing-in-reverse', 'l7-unknowns-both-sides', 'l8-clearing-fractions',
         'l9-story-to-equation', 'l10-ranges-of-answers', 'l11-one-twist', 'l12-trapped', 'l13-changing-the-subject',
         'review-1', 'review-2', 'review-3', 'homework-1', 'homework-2', 'homework-3',
         'problems-1', 'problems-2', 'problems-3']


def widgets(doc):
    """Yield (locator, item) for every item carrying a widget."""
    for key in ('screens', 'quiz', 'items'):
        for i, it in enumerate(doc.get(key, [])):
            if 'widget' in it:
                yield f'{key}[{i}]', it
            for j, p in enumerate(it.get('parts', [])):
                if 'widget' in p:
                    yield f'{key}[{i}].parts[{j}]', p


def check_numeric():
    for f in FILES:
        doc = load(f)
        for loc, it in widgets(doc):
            w = it['widget']
            kind = w['kind']
            if kind == 'numeric':
                if loc not in NUM.get(f, {}):
                    check(False, f, loc + '.widget.answer', 'numeric key not recomputed', 'no entry in NUM'); continue
                key, slips = NUM[f][loc]
                check(close(w['answer'], key, 0.0051), f, loc + '.widget.answer', f"key {w['answer']}", f'recomputed {round(float(key), 4)}')
                for wr in w.get('wrong', []):
                    if wr['id'] not in slips:
                        check(False, f, f"{loc}.widget.wrong[{wr['id']}]", 'slip not recomputed', 'no entry'); continue
                    v = slips[wr['id']]
                    tol = max(wr.get('tol', {}).get('abs', 0), 0.0051)
                    check(close(wr['value'], v, tol) and not close(v, key, 1e-9), f, f"{loc}.widget.wrong[{wr['id']}]",
                          f"slip {wr['id']} = {wr['value']}", f'named slip gives {round(float(v), 4)}; differs from key')
            elif kind == 'drag-point' and loc in NUM.get(f, {}):
                key, slips = NUM[f][loc]
                check(close(w['points'][0]['target'][0], key), f, loc + '.widget.points[0].target', f"target {w['points'][0]['target'][0]}", f'recomputed {key}')
                for wr in w.get('wrong', []):
                    if wr['id'] in slips:
                        lo, hi = wr['region']['x']
                        check(lo <= slips[wr['id']] <= hi and not lo <= key <= hi, f, f"{loc}.widget.wrong[{wr['id']}]",
                              f"slip region {lo} to {hi}", f"named slip gives {slips[wr['id']]}; key outside the region")
            elif kind == 'table' and any(isinstance(c, dict) for r in w['rows'] for c in r):
                cells = [c for r in w['rows'] for c in r if isinstance(c, dict) and c.get('edit')]
                exp = TAB.get(f, {}).get(loc)
                if exp is None or len(exp) != len(cells):
                    check(False, f, loc + '.widget.rows', 'table not recomputed', 'no entry in TAB'); continue
                for k, (c, e) in enumerate(zip(cells, exp)):
                    check(close(c['answer'], e, 0.0051), f, f'{loc}.widget.rows cell {k}', f"cell key {c['answer']}", f'recomputed {round(float(e), 4)}')


# ---------------------------------------------------------------- algebra of expression and choice items
LETTERS = {ch: sp.Symbol(ch) for ch in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'}
TR = standard_transformations + (split_symbols, implicit_multiplication, convert_xor, rationalize)


def tex2(s):
    s = s.strip().strip('$').replace('\\dfrac', '\\frac').replace('\\tfrac', '\\frac')
    s = s.replace('\\times', '*').replace('\\ge', '>=').replace('\\le', '<=').replace('{,}', '')
    while '\\frac' in s:
        s2 = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', s)
        if s2 == s:
            raise ValueError(s)
        s = s2
    return s.replace('{', '(').replace('}', ')')


def P(s):
    return parse_expr(re.sub(r'(\d)\s*\(', r'\1*(', tex2(s)), local_dict=LETTERS, transformations=TR)


def same(a, b):
    return sp.simplify(sp.nsimplify(a - b, rational=True)) == 0


# (file, locator, source expression, ids that are equal in value but refused for form)
ALG = [
 ('l1-letters-for-numbers', 'screens[2]', '2n+5', []), ('l1-letters-for-numbers', 'screens[3]', '3+2n', []),
 ('l1-letters-for-numbers', 'screens[8]', '25+12m', []), ('l1-letters-for-numbers', 'screens[9]', '1.5+0.02n', []),
 ('l1-letters-for-numbers', 'quiz[0]', '9t+2', []), ('l1-letters-for-numbers', 'quiz[2]', '12.4q+150', []),
 ('l2-like-terms', 'screens[0]', '2n+3+n+5', []), ('l2-like-terms', 'screens[4]', '5n+6-2n-4', []),
 ('l2-like-terms', 'screens[9]', '-12.5n-4+13.1n-4', []), ('l2-like-terms', 'quiz[0]', '5a+3+2a+6', []),
 ('l2-like-terms', 'quiz[1]', 'n+n+n', []), ('l2-like-terms', 'quiz[2]', '8x-3-5x+7', []), ('l2-like-terms', 'quiz[3]', '6n-6n+5', []),
 ('l3-opening-brackets', 'screens[2]', '3(n+2)', []), ('l3-opening-brackets', 'screens[4]', '5(2n+1)', []),
 ('l3-opening-brackets', 'screens[5]', '-2(n-4)', []), ('l3-opening-brackets', 'screens[7]', '6(n-2)', []),
 ('l3-opening-brackets', 'screens[9]', '40(n+6.25)', []), ('l3-opening-brackets', 'quiz[0]', '5(n+3)', []),
 ('l3-opening-brackets', 'quiz[1]', '4(2n-1)', []), ('l3-opening-brackets', 'quiz[3]', 'n(n+3)', []),
 ('l4-putting-brackets-back', 'screens[0]', '(4n+12)/4', []), ('l4-putting-brackets-back', 'screens[3]', '6n+9', []),
 ('l4-putting-brackets-back', 'screens[4]', '12n+18', ['two', 'three']), ('l4-putting-brackets-back', 'screens[5]', '7n+7', []),
 ('l4-putting-brackets-back', 'quiz[0]', '6n+15', []), ('l4-putting-brackets-back', 'quiz[1]', '20n-30', ['not-fully']),
 ('l4-putting-brackets-back', 'quiz[2]', '9n+9', []), ('l4-putting-brackets-back', 'quiz[3]', 'n^2+4n', []),
 ('review-1', 'items[0]', '2.8+1.6m', []), ('review-1', 'items[1]', '6(n+4)', []), ('review-1', 'items[2]', '7n+4-3n+2n-9', []),
 ('review-1', 'items[3]', '18n+24', ['two', 'three']), ('review-1', 'items[5]', '-3(2n-5)', []),
 ('review-1', 'items[6]', '2(n+3)+5(n-2)', []), ('review-1', 'items[7]', '300(p+0.45)', []),
 ('homework-1', 'items[0]', '3.2n+5', []), ('homework-1', 'items[2]', '3(2n-1)-2(n-4)', []),
 ('homework-1', 'items[3]', '5(3-2n)', []), ('homework-1', 'items[6]', '6n^2+9n', ['no-n', 'no-three']),
 ('problems-1', 'items[0].parts[0]', 'a-5', []), ('problems-1', 'items[0].parts[1]', '2a+3(a-5)', []),
 ('problems-1', 'items[0].parts[2]', '5a-15', []), ('problems-1', 'items[1].parts[0]', '6.5n-2.3n-45', []),
 ('problems-1', 'items[1].parts[1]', '4.2(n-20)-45', []), ('problems-1', 'items[1].parts[2]', '4.2n-45+4.2(n-20)-45', []),
 ('problems-1', 'items[2].parts[0]', '5(n+4)-3(n-2)', []), ('problems-1', 'items[2].parts[1]', '2n+26', []),
 ('problems-1', 'items[3].parts[0]', 's(s+2)', []), ('problems-1', 'items[3].parts[1]', '3s(s+2)+4s^2', []),
 ('problems-1', 'items[3].parts[2]', '7s^2+6s', []), ('problems-2', 'items[3].parts[0]', '12000-s', []),
 # formulae: source is the solved form, worked below with sympy.solve before use
 ('l13-changing-the-subject', 'screens[5]', sp.solve(sp.Eq(LETTERS['C'], 5+2*LETTERS['n']), LETTERS['n'])[0], []),
 ('l13-changing-the-subject', 'quiz[0]', sp.solve(sp.Eq(LETTERS['I'], LETTERS['P']*LETTERS['r']*LETTERS['t']), LETTERS['r'])[0], []),
 ('l13-changing-the-subject', 'quiz[1]', sp.solve(sp.Eq(LETTERS['v'], LETTERS['u']+LETTERS['a']*LETTERS['t']), LETTERS['a'])[0], []),
 ('l13-changing-the-subject', 'quiz[3]', sp.solve(sp.Eq(LETTERS['q'], LETTERS['F']/(LETTERS['p']-LETTERS['c'])), LETTERS['p'])[0], []),
 ('review-3', 'items[2]', sp.solve(sp.Eq(LETTERS['P'], 2*(LETTERS['l']+LETTERS['w'])), LETTERS['w'])[0], []),
 ('problems-3', 'items[1].parts[0]', sp.solve(sp.Eq(LETTERS['F'], sp.Rational(9, 5)*LETTERS['C']+32), LETTERS['C'])[0], []),
 ('problems-3', 'items[2].parts[0]', sp.solve(sp.Eq(LETTERS['V'], LETTERS['P']-LETTERS['k']*LETTERS['t']), LETTERS['t'])[0], []),
 ('problems-3', 'items[3].parts[0]', sp.solve(sp.Eq(LETTERS['w'], LETTERS['a']/(LETTERS['a']+LETTERS['b'])), LETTERS['a'])[0], []),
]


def check_algebra():
    for f, loc, src, formonly in ALG:
        w = at(load(f), loc)['widget']
        s = P(src) if isinstance(src, str) else src
        if w['kind'] == 'expression':
            forms = [('answer', w['answer'], True)] + [(f'accept[{k}]', a, True) for k, a in enumerate(w.get('accept', []))] \
                    + [(f"wrong[{x['id']}]", x['tex'], False) for x in w.get('wrong', [])]
        else:
            forms = [(f"options[{o['id']}]", o['text'].split('=')[-1] if '=' in o['text'] else o['text'], bool(o.get('correct')) or o['id'] in formonly)
                     for o in w['options'] if o['text'].count('$') == 2 and o['text'].strip().startswith('$')]
            if w['kind'] == 'choice':
                check(sum(bool(o.get('correct')) for o in w['options']) == 1, f, loc + '.widget.options', 'exactly one correct option', 'count')
        for name, tex, want in forms:
            try:
                eq = same(P(tex), s)
            except Exception as e:  # an option that is words, not algebra
                check(False, f, f'{loc}.widget.{name}', f'could not parse {tex}', str(e)); continue
            what = 'equals' if want else 'differs from'
            note = ' (equal in value, refused for form: not fully factorised)' if name.split('[')[-1].rstrip(']') in formonly else ''
            check(eq == want, f, f'{loc}.widget.{name}', f'{tex} {what} the source expression{note}', f'sympy identity test against {sp.sstr(s)}')


# equations typed whole, and the equations behind worded items: root of the key, roots of the slips
def root(tex, var):
    l, r = tex2(tex).split('=')
    sol = sp.solve(sp.Eq(P(l), P(r)), LETTERS[var])
    return sol[0] if sol else None


EQN = [('problems-2', 'items[0].parts[0]', 'c', 21), ('problems-2', 'items[1].parts[0]', 'x', 750), ('problems-2', 'items[3].parts[1]', 's', 4800)]


def check_equations():
    for f, loc, var, want in EQN:
        w = at(load(f), loc)['widget']
        for name, tex in [('answer', w['answer'])] + [(f'accept[{k}]', a) for k, a in enumerate(w.get('accept', []))]:
            check(same(root(tex, var), sp.Integer(want)), f, f'{loc}.widget.{name}', f'{tex} has the root {want}', 'sympy.solve')
        for x in w.get('wrong', []):
            check(not same(root(x['tex'], var), sp.Integer(want)), f, f"{loc}.widget.wrong[{x['id']}]", f"{x['tex']} is a different equation", 'sympy.solve: different root')


# ---------------------------------------------------------------- inequalities: solution sets
x, n, h, F, t, y, pp = sp.symbols('x n h F t y p', real=True)
I = sp.Interval
oo = sp.oo
R = sp.S.Reals


def sol(rel, v):
    return sp.solveset(rel, v, R)


INEQ = [
 ('l11-one-twist', 'screens[0]', 'x + 4 > 9 is x > 5', sol(x+4 > 9, x), I.open(5, oo)),
 ('l11-one-twist', 'screens[1]', '3x - 2 >= 10 is x >= 4', sol(3*x-2 >= 10, x), I(4, oo)),
 ('l11-one-twist', 'screens[4]', '-3x > 12 is x < -4', sol(-3*x > 12, x), I.open(-oo, -4)),
 ('l11-one-twist', 'screens[5]', '2x + 5 < 1 is x < -2', sol(2*x+5 < 1, x), I.open(-oo, -2)),
 ('l11-one-twist', 'screens[6]', '5 - x/2 >= 3 is x <= 4', sol(5-x/2 >= 3, x), I(-oo, 4)),
 ('l11-one-twist', 'screens[7]', '7 - 2x <= 1 is x >= 3', sol(7-2*x <= 1, x), I(3, oo)),
 ('l11-one-twist', 'screens[8]', '-2.5n >= -600 is n <= 240', sol(-sp.Rational(5, 2)*n >= -600, n), I(-oo, 240)),
 ('l11-one-twist', 'quiz[0]', '4x + 1 > 13 is x > 3', sol(4*x+1 > 13, x), I.open(3, oo)),
 ('l11-one-twist', 'quiz[1]', '-5x <= 20 is x >= -4', sol(-5*x <= 20, x), I(-4, oo)),
 ('l11-one-twist', 'quiz[3]', '10 - 3x < 4 is x > 2', sol(10-3*x < 4, x), I.open(2, oo)),
 ('l12-trapped', 'screens[3]', '1 < 2x + 3 <= 11 is -1 < x <= 4', sol(1 < 2*x+3, x) & sol(2*x+3 <= 11, x), I.Lopen(-1, 4)),
 ('l12-trapped', 'screens[5]', '-3 <= 1 - 2x < 7 is -3 < x <= 2', sol(-3 <= 1-2*x, x) & sol(1-2*x < 7, x), I.Lopen(-3, 2)),
 ('l12-trapped', 'screens[7]', '-200 <= 120 - n <= 200 is -80 <= n <= 320', sol(-200 <= 120-n, n) & sol(120-n <= 200, n), I(-80, 320)),
 ('l12-trapped', 'screens[8]', '5000 - 450n >= 800 is n <= 28/3', sol(5000-450*n >= 800, n), I(-oo, sp.Rational(28, 3))),
 ('l12-trapped', 'quiz[0]', '5 <= x + 3 < 9 is 2 <= x < 6', sol(5 <= x+3, x) & sol(x+3 < 9, x), I.Ropen(2, 6)),
 ('l12-trapped', 'quiz[2]', '-1 < -x <= 4 is -4 <= x < 1', sol(-1 < -x, x) & sol(-x <= 4, x), I.Ropen(-4, 1)),
 ('l12-trapped', 'quiz[3]', '5 < x < 2 is empty', sol(5 < x, x) & sol(x < 2, x), sp.S.EmptySet),
 ('review-3', 'items[1]', '6 - 2x > 14 is x < -4', sol(6-2*x > 14, x), I.open(-oo, -4)),
 ('review-3', 'items[3]', '-2 <= 3x + 1 < 10 is -1 <= x < 3', sol(-2 <= 3*x+1, x) & sol(3*x+1 < 10, x), I.Ropen(-1, 3)),
 ('review-3', 'items[6]', '80 <= 100 - 4y <= 92 is 2 <= y <= 5', sol(80 <= 100-4*y, y) & sol(100-4*y <= 92, y), I(2, 5)),
 ('review-3', 'items[7]', '8q - 2000 > 0 is q > 250', sol(8*x-2000 > 0, x), I.open(250, oo)),
 ('homework-3', 'items[0]', '(3 - x)/4 >= -2 is x <= 11', sol((3-x)/4 >= -2, x), I(-oo, 11)),
 ('homework-3', 'items[2]', '2x - 3 < 9 and 5 - x <= 7 is -2 <= x < 6', sol(2*x-3 < 9, x) & sol(5-x <= 7, x), I.Ropen(-2, 6)),
 ('homework-3', 'items[3]', '12000 - 1500n >= 3000 is n <= 6', sol(12000-1500*n >= 3000, n), I(-oo, 6)),
 ('homework-3', 'items[6]', '(2x - 1)/3 < (x + 4)/(-2) is x < -10/7', sol((2*x-1)/3 < (x+4)/(-2), x), I.open(-oo, sp.Rational(-10, 7))),
 ('homework-3', 'items[7]', '40(75 - p) >= -400 is p <= 85', sol(40*(75-pp) >= -400, pp), I(-oo, 85)),
 ('problems-3', 'items[0].parts[1]', '240 - 18h >= 60 is h <= 10', sol(240-18*h >= 60, h), I(-oo, 10)),
 ('problems-3', 'items[1].parts[2]', '(F - 32)/1.8 <= 5 is F <= 41', sol((F-32)/sp.Rational(9, 5) <= 5, F), I(-oo, 41)),
 ('problems-3', 'items[1].parts[3]', '-25 <= (F - 32)/1.8 <= -15 is -13 <= F <= 5', sol(-25 <= (F-32)/sp.Rational(9, 5), F) & sol((F-32)/sp.Rational(9, 5) <= -15, F), I(-13, 5)),
 ('problems-3', 'items[2].parts[2]', '24000 - 2400t > 6000 is t < 7.5', sol(24000-2400*t > 6000, t), I.open(-oo, sp.Rational(15, 2))),
 ('problems-3', 'items[2].parts[3]', '6000 < 24000 - 2400t <= 19200 is 2 <= t < 7.5', sol(6000 < 24000-2400*t, t) & sol(24000-2400*t <= 19200, t), I.Ropen(2, sp.Rational(15, 2))),
]


def check_inequalities():
    for f, loc, claim, got, want in INEQ:
        check(got == want, f, loc, claim, f'sympy.solveset gives {sp.sstr(got)}')
    # the one twist itself, exhaustively on a grid: a < b and k < 0 give ka > kb; k > 0 keeps the order
    grid = [Fr(i, 2) for i in range(-12, 13)]
    ok = all((k*a > k*b) if k < 0 else (k*a < k*b) for a in grid for b in grid if a < b for k in grid if k != 0)
    check(ok, 'l11-one-twist', 'screens[3].explain.text / summary.formula.tex', 'a < b gives ka > kb for k < 0, and ka < kb for k > 0', 'exhaustive on a grid of 25 values each; follows from b - a > 0 times k')
    ok = all((a+c < b+c) and (a-c < b-c) for a in grid for b in grid if a < b for c in grid)
    check(ok, 'l11-one-twist', 'screens[7].prose', 'adding or subtracting the same number keeps the sign', 'exhaustive on the same grid')
    # counting integers: a < x <= b holds b - a, both closed b - a + 1, both open b - a - 1 (l12 screens[6])
    ok = all(len([z for z in range(-30, 31) if a < z <= b]) == b-a and len([z for z in range(-30, 31) if a <= z <= b]) == b-a+1
             and len([z for z in range(-30, 31) if a < z < b]) == b-a-1 for a in range(-10, 10) for b in range(a+1, 11))
    check(ok, 'l12-trapped', 'screens[6].widget and explain.text', 'integers in a < x <= b number b - a; closed both ends b - a + 1; open both b - a - 1', 'exhaustive for -10 <= a < b <= 10')


# ---------------------------------------------------------------- the "test with a number" claim (l2 screens[5])
def check_test_value():
    # Sam's 16n agrees with 4n+7+2n+3 at exactly one n; so one lucky test value can pass a wrong answer.
    agree = [k for k in range(-100, 101) if 4*k+7+2*k+3 == 16*k]
    check(agree == [1], 'l2-like-terms', 'screens[5].explain.text', "Sam's 16n matches the expression only at n = 1", 'two different linear expressions agree at one n at most: 6n + 10 = 16n only at n = 1')
    check(4*0+7+2*0+3 != 16*0, 'l2-like-terms', 'screens[5].explain.text', 'n = 0 would in fact expose this particular slip (10 against 0); the advice is a rule of thumb', 'direct substitution')


# ---------------------------------------------------------------- fluency families, whole ranges
def rng(lo, hi, no=()):
    return [v for v in range(lo, hi+1) if v not in no]


def check_fluency():
    bad = {}

    def need(cond, fam):
        if not cond:
            bad[fam] = bad.get(fam, 0) + 1
    cnt = {}

    def seen(fam):
        cnt[fam] = cnt.get(fam, 0) + 1
    v = sp.Symbol('v')
    # l2: a v + b + c v + d
    for a, b, c, d in itertools.product(rng(1, 9), rng(-9, 9, [0]), rng(-9, 9, [0]), rng(-9, 9, [0])):
        k, r, al = a+c, b+d, a+b+c+d
        if k == 0 or r == 0 or al == 0:
            continue
        seen('l2/0')
        need((a-c, r) != (k, r), 'l2/0')          # sign slip differs from the key
        need((al, 0) != (k, r), 'l2/0')           # everything-onto-v slip differs from the key
    # l3 family 0: a(p v + b); family 1: a(v + b) + c(v + d)
    for a, p, b in itertools.product(rng(-9, 9, [-1, 0, 1]), rng(1, 5), rng(-9, 9, [0])):
        seen('l3/0')
        need(sp.expand(a*(p*v+b)) == a*p*v+a*b, 'l3/0')
        need(b != a*b and -a*b != a*b, 'l3/0')
    for a, b, c, d in itertools.product(rng(2, 6), rng(-6, 6, [0]), rng(-6, 6, [-1, 0, 1]), rng(-6, 6, [0])):
        k, r = a+c, a*b+c*d
        if k == 0 or r == 0:
            continue
        seen('l3/1')
        need(a*b+d != r and a*b-c*d != r, 'l3/1')
    # l4: h(p v + q) with gcd(p, |q|) = 1: h is then the highest common factor of hp and h|q|
    for fam, hs, ps, qs in (('l4/0', [2, 3, 5, 7], rng(1, 6), rng(-9, 9, [0])), ('l4/1', [4, 6, 8, 9, 10, 12], rng(1, 5), rng(-7, 7, [0]))):
        for hh, p, q in itertools.product(hs, ps, qs):
            if math.gcd(p, abs(q)) != 1 or p+q == 0:
                continue
            seen(fam)
            need(math.gcd(hh*p, abs(hh*q)) == hh, fam)      # the factor taken out is the HCF
            need(hh*q != q, fam)                            # undivided-second-term slip differs
            need(not (p+q == p and q == 0), fam)
    # l6 family 0: a v + b = c; family 1: v/a + b = c
    for a, x0, b in itertools.product(rng(2, 9), rng(-9, 9, [0]), rng(-15, 15, [0])):
        c = a*x0+b
        seen('l6/0')
        need(Fr(c-b, a) == x0, 'l6/0')
        need(Fr(c, a)-b != x0 and Fr(c+b, a) != x0, 'l6/0')
    for a, m, b in itertools.product(rng(2, 6), rng(-9, 9, [0]), rng(-9, 9, [0])):
        x0, c = a*m, m+b
        seen('l6/1')
        need(Fr(x0, a)+b == c, 'l6/1')
        need(a*c-b != x0 and Fr(c-b, a) != x0, 'l6/1')
    # l7 family 0: a(v + b) = c v + d; family 1: a(v + b) = c(v + d)
    for c, k, b, x0 in itertools.product(rng(1, 4), rng(2, 4), rng(-6, 6, [0]), rng(-6, 6, [0])):
        a = c+k
        d = a*(x0+b)-c*x0
        if d == 0 or abs(d) > 40:
            continue
        seen('l7/0')
        need(a*(x0+b) == c*x0+d, 'l7/0')
        need(Fr(d-b, a-c) != x0 and Fr(d-a*b, a+c) != x0, 'l7/0')
    for a, k, m, x0 in itertools.product(rng(2, 4), rng(2, 3), [-1, 1, 2], rng(-5, 6, [0])):
        c = a+k
        b, d = c*m-x0, a*m-x0
        if b == 0 or d == 0 or abs(b) > 12 or abs(d) > 12 or b-d == a*b-c*d or b-d == a*b+c*d:
            continue
        seen('l7/1')
        need(a*(x0+b) == c*(x0+d), 'l7/1')
        need(Fr(b-d, c-a) != x0 and Fr(a*b+c*d, c-a) != x0, 'l7/1')
        need(Fr(a*b-c*d, k) == x0, 'l7/1')                 # the worked solution's line
    # l8 family 0: v/p + v/q = r; family 1: (v + b)/p = (v + d)/q
    for p, q, k in itertools.product(rng(2, 5), rng(3, 6), rng(-4, 5, [0])):
        if not p < q:
            continue
        L = p*q//math.gcd(p, q)
        x0 = k*L
        r = Fr(x0, p)+Fr(x0, q)
        u, w = L//p, L//q
        seen('l8/0')
        need(r.denominator == 1, 'l8/0')                    # the right side shown is a whole number
        need(L*r == (u+w)*x0, 'l8/0')
        need(r/(u+w) != x0 and r*(p+q) != x0, 'l8/0')
    for p, k, m, x0 in itertools.product(rng(2, 4), rng(2, 3), [-2, -1, 1, 2], rng(-6, 9, [0])):
        q = p+k
        b, d = p*m-x0, q*m-x0
        if q > 6 or b == 0 or d == 0 or abs(b) > 12 or abs(d) > 12 or m == x0 or x0 == (p+q+1)*m:
            continue
        seen('l8/1')
        need(Fr(x0+b, p) == Fr(x0+d, q), 'l8/1')
        need(Fr(d-b, q-p) == m and m != x0, 'l8/1')                         # lost-bracket slip q v + b = p v + d gives m
        need(Fr(p*b-q*d, q-p) == x0-(p+q)*m != x0, 'l8/1')                  # own-bottom slip p(v+b) = q(v+d)
        need(Fr(p*d-q*b, k) == x0, 'l8/1')
    # l13: rearrangements, symbolic
    u_, a_, b_, w_ = sp.symbols('u a b w', nonzero=True)
    ok13 = [sp.simplify(sp.solve(sp.Eq(u_, a_*v+b_), v)[0]-(u_-b_)/a_) == 0,
            sp.simplify(sp.solve(sp.Eq(u_, a_*b_*v), v)[0]-u_/(a_*b_)) == 0,
            sp.simplify(sp.solve(sp.Eq(u_, a_*b_/v), v)[0]-a_*b_/u_) == 0]
    names = {'l2/0': 'fluency-l2-like-terms', 'l3/0': 'fluency-l3-opening-brackets', 'l3/1': 'fluency-l3-opening-brackets',
             'l4/0': 'fluency-l4-putting-brackets-back', 'l4/1': 'fluency-l4-putting-brackets-back',
             'l6/0': 'fluency-l6-undoing-in-reverse', 'l6/1': 'fluency-l6-undoing-in-reverse',
             'l7/0': 'fluency-l7-unknowns-both-sides', 'l7/1': 'fluency-l7-unknowns-both-sides',
             'l8/0': 'fluency-l8-clearing-fractions', 'l8/1': 'fluency-l8-clearing-fractions'}
    for fam, f in names.items():
        check(bad.get(fam, 0) == 0 and cnt.get(fam, 0) > 0, f, f'families[{fam[-1]}]',
              f'key solves the item and both slips differ from the key, all {cnt.get(fam, 0)} draws',
              'own enumeration of the whole variable range (not the engine templates)')
    for k, ok in enumerate(ok13):
        check(ok, 'fluency-l13-changing-the-subject', f'families[{k}]', 'key is the rearrangement; slips are different expressions for a >= 2, b != 0', 'sympy.solve with symbols; u/a - b = (u - b)/a only if a = 1 or b = 0')
    # the templates in the files still have the ranges enumerated above
    spec = {('fluency-l6-undoing-in-reverse', 0): {'a': [2, 9], 'x0': [-9, 9], 'b': [-15, 15]},
            ('fluency-l8-clearing-fractions', 0): {'p': [2, 5], 'q': [3, 6], 'k': [-4, 5]},
            ('fluency-l7-unknowns-both-sides', 1): {'a': [2, 4], 'k': [2, 3], 'x0': [-5, 6]},
            ('fluency-l4-putting-brackets-back', 1): {'p': [1, 5], 'q': [-7, 7]},
            ('fluency-l3-opening-brackets', 1): {'a': [2, 6], 'b': [-6, 6], 'c': [-6, 6], 'd': [-6, 6]},
            ('fluency-l2-like-terms', 0): {'a': [1, 9], 'b': [-9, 9], 'c': [-9, 9], 'd': [-9, 9]}}
    for (f, k), want in spec.items():
        vs = load(f)['families'][k]['vars']
        check(all(vs[name]['int'] == r for name, r in want.items()), f, f'families[{k}].vars', 'ranges in the file match the ranges enumerated', 'read from the file')


check_numeric(); check_algebra(); check_equations(); check_inequalities(); check_test_value(); check_fluency()
if ROWS:
    for r in rows:
        print('\t'.join(str(c).replace('\t', ' ').replace('\n', ' ') for c in r))
else:
    print(f'{nchecks} checks, {len(fails)} failed')
    for m in fails:
        print('FAIL', m)
sys.exit(1 if fails else 0)
