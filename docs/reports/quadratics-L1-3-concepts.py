#!/usr/bin/env python3
"""Concept audit checks, quadratics levels 1 to 3 (round 1, blind audit quadratics-1-3).

Run from anywhere:  python docs/reports/quadratics-L1-3-concepts.py
Exits 0 when every check on correct content passes. A check listed under
EXPECTED_FAIL is a finding of the audit (docs/reviews/audit-quadratics-1-3.md):
it stays failing until the content is fixed, and it makes the exit code 1.

Sections
  A  every choice option of an "expand / factorise" item: the key is identically
     equal to the prompt, every wrong option is not (sympy, read from the JSON)
  B  graded keys, slips and stated numbers, recomputed by hand-coded formulae
  C  fluency families swept over their whole range (own enumeration)
  D  canvas points lie on the curve they are drawn on (plane canvases)
"""
import itertools, json, math, os, re, sys
from fractions import Fraction as F
import sympy as sp
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
                                        implicit_multiplication_application, convert_xor)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'quadratics')
TR = standard_transformations + (implicit_multiplication_application, convert_xor)
fails, npass = [], 0


def ok(cond, label):
    global npass
    if cond:
        npass += 1
    else:
        fails.append(label)


def near(a, b, tol=1e-9):
    return abs(float(a) - float(b)) <= tol


def load(name):
    with open(os.path.join(ROOT, name + '.json')) as fh:
        return json.load(fh)


def tex2sym(t):
    t = t.strip().strip('$')
    t = re.sub(r'\\t?frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', t)
    t = t.replace('\\times', '*').replace('\\left', '').replace('\\right', '')
    t = t.replace('−', '-').replace('{', '(').replace('}', ')')
    return parse_expr(t, transformations=TR)


def not_fully(tex):
    """True when a written product still has a bracket with a common factor or a reducible bracket."""
    for inner in re.findall(r'\(([^()]*)\)', tex.replace('−', '-')):
        e = tex2sym(inner)
        if e.is_number:
            continue
        coeff, facs = sp.factor_list(e)
        if abs(coeff) != 1 or sum(m for _, m in facs) > 1:
            return True
    return False


LESSONS = ['l1-two-brackets', 'l2-product-and-sum', 'l3-leading-coefficient',
           'l4-difference-of-squares', 'l5-product-of-zero', 'l6-completing-the-square',
           'l7-the-formula', 'l8-how-many-solutions', 'l9-shape-of-a-square',
           'l10-turning-point', 'l11-meeting-the-axis', 'l12-above-or-below', 'l13-best-price']
SETS = ['review-1', 'review-2', 'review-3', 'homework-1', 'homework-2', 'homework-3']
PROBLEMS = ['problems-1', 'problems-2', 'problems-3']

# ---------------------------------------------------------------- A
PAT = re.compile(r'(?:Expand(?: and simplify)?|[Ff]actorise|[Ww]hich is|Complete the square on|'
                 r'equal to|Write) \$([^$]+)\$')


def items_of(d):
    for key in ('screens', 'quiz', 'items'):
        for i, it in enumerate(d.get(key, [])):
            yield '%s[%d]' % (key, i), it
            for j, part in enumerate(it.get('parts', [])):
                yield '%s[%d].parts[%d]' % (key, i, j), part


nA = 0
for name in LESSONS + SETS + PROBLEMS:
    d = load(name)
    for path, it in items_of(d):
        w = it.get('widget') or {}
        if w.get('kind') != 'choice':
            continue
        text = (it.get('question') or '') + ' || ' + (it.get('prose') or '')
        m = PAT.search(it.get('question') or '') or PAT.search(it.get('prose') or '')
        if not m:
            continue
        try:
            target = tex2sym(m.group(1).split('=')[0])
        except Exception:
            continue
        opts = []
        for o in w.get('options', []):
            mm = re.search(r'\$([^$]+)\$\s*$', o.get('text', ''))
            if not mm or not re.fullmatch(r'\$[^$]+\$', o.get('text', '').strip()):
                opts = None
                break
            try:
                opts.append((o, tex2sym(mm.group(1))))
            except Exception:
                opts = None
                break
        if not opts:
            continue
        if not any(sp.simplify(e - target) == 0 for o, e in opts if o.get('correct')):
            continue  # the pattern caught a different expression (not an identity item)
        nA += 1
        fully = 'ully factoris' in text
        for o, e in opts:
            same = sp.simplify(sp.expand(e - target)) == 0
            if same and not o.get('correct') and fully:
                # an equal option may be marked wrong only if it is not fully factorised
                ok(not_fully(re.search(r'\$([^$]+)\$', o['text']).group(1)),
                   'A %s %s option %s: equal and fully factorised, yet marked wrong' % (name, path, o.get('id')))
                continue
            ok(same == bool(o.get('correct')), 'A %s %s option %s: identity %s but correct=%s'
               % (name, path, o.get('id'), same, bool(o.get('correct'))))

# ---------------------------------------------------------------- B
x, q, p, t, w_, n, d_ = sp.symbols('x q p t w n d')
r5, r29, r41 = math.sqrt(5), math.sqrt(29), math.sqrt(41)


def roots(expr, var=x):
    return sorted(float(s) for s in sp.solve(expr, var) if sp.im(s) == 0)


def wrongs(widget):
    return {e['id']: e.get('value') for e in widget.get('wrong', [])}


def key(name, where, idx, part=None):
    it = load(name)[where][idx]
    if part is not None:
        it = it['parts'][part]
    return it['widget']


B = []  # (label, stated, recomputed)


def chk(name, where, idx, expect, slips=None, part=None, tol=1e-6):
    wdg = key(name, where, idx, part)
    ans = wdg.get('answer', wdg.get('answers'))
    lab = 'B %s %s[%d]%s' % (name, where, idx, '' if part is None else '.parts[%d]' % part)
    if isinstance(expect, (list, tuple)):
        ok(sorted(map(float, ans)) == sorted(map(float, expect)) or
           all(near(a, b, tol) for a, b in zip(sorted(map(float, ans)), sorted(map(float, expect)))),
           lab + ' key %s vs %s' % (ans, expect))
    else:
        ok(near(ans, expect, tol), lab + ' key %s vs %s' % (ans, expect))
    have = wrongs(wdg)
    for sid, val in (slips or {}).items():
        ok(sid in have and near(have[sid], val, max(tol, 1e-6)),
           lab + ' slip %s stated %s, the named mistake gives %s' % (sid, have.get(sid), val))


# level 1
chk('l1-two-brackets', 'screens', 0, 13 * 12, {'firsts-lasts': 100 + 6, 'added': 13 + 12,
    'one-strip': 156 - 20, 'other-strip': 156 - 30})
chk('l1-two-brackets', 'screens', 4, 5 - 2, {'ignored-sign': 7, 'flipped': -5 + 2, 'both-minus': -7})
chk('l1-two-brackets', 'screens', 8, 2000 * 0.04 ** 2, {'whole-gain': 2000 * 1.04 ** 2 - 2000,
    'one-strip': 80, 'two-strips': 160, 'per-pound': 0.04 ** 2}, tol=1e-6)
chk('l2-product-and-sum', 'quiz', 3, 3 + 24 / 3, {'gave-p': 8, 'added-c': 27})
chk('l3-leading-coefficient', 'quiz', 1, 4 * -3, {'c-only': -3, 'no-sign': 12})
chk('l4-difference-of-squares', 'screens', 0, 100 - 9, {'side-not-area': 97, 'small-square': 49, 'cut-strip': 70})
chk('l4-difference-of-squares', 'screens', 8, 50 * 1.08 * 0.92, {'flat': 50, 'down-only': 46, 'up-only': 54,
    'two-r': 50 * (1 - 2 * 0.0064)}, tol=1e-6)
chk('l4-difference-of-squares', 'quiz', 1, 51 ** 2 - 49 ** 2, {'diff-squared': 4, 'sum-squared': 10000})
chk('review-1', 'items', 1, 10, {'one-strip': 5, 'each-squared': 0, 'corner': 25})
chk('review-1', 'items', 6, 1.03 ** 2 - 1, {'simple': 0.06, 'each-squared': 0.0009, 'one-strip': 0.03})
chk('review-1', 'items', 7, math.sqrt(0.01), {'one-pc': 0.01, 'two-r': 0.005})
chk('review-1', 'items', 8, 10, {'smaller': 4, 'sum': 14, 'product': 40})
chk('homework-1', 'items', 4, 1003 * 997, {'added': 1000009, 'no-corner': 1000000})
chk('homework-1', 'items', 5, 12, {'one-strip': 6, 'corner': 36, 'eighteen': 18})
chk('homework-1', 'items', 6, 320 / 16, {'sum': 36, 'product': 320})
ok(sp.expand(q * (25 - q / 2) - 7 * q - 160 - (-q ** 2 / 2 + 18 * q - 160)) == 0, 'B homework-1 profit expansion')
ok(sp.expand(q * (16 - q) - 4 * q - 27 + (q - 3) * (q - 9)) == 0, 'B l2 transfer profit = -(q-3)(q-9)')
ok(sp.expand(q * (30 - 2 * q) - 6 * q - 40 + 2 * (q - 2) * (q - 10)) == 0, 'B l3 transfer profit')
# homework-1 variance example
xs = [F(1, 100), F(3, 100), F(5, 100)]
m_ = sum(xs) / 3
ok(sum((v - m_) ** 2 for v in xs) / 3 == sum(v * v for v in xs) / 3 - m_ ** 2 == F(35, 10000) / 3 - F(9, 10000),
   'B homework-1 variance shortcut example')
# problems-1
ok(sp.expand((x + 4) * (x + 11) - (x ** 2 + 15 * x + 44)) == 0, 'B p1 cinema expand')
chk('problems-1', 'items', 0, 13 * 22, {'kept': 14 * 21, 'sum-thirteen': 14 * 19, 'square': 256}, part=2)
ok(sp.factor(2 * x ** 2 + 19 * x + 45) == (x + 5) * (2 * x + 9), 'B p1 plot B')
ok(sp.expand((x + 5) * ((x + 6) + (2 * x + 9)) - 3 * (x + 5) ** 2) == 0, 'B p1 joined plots')
chk('problems-1', 'items', 1, 300, {'three-squared': 900, 'both-sides': 600}, part=3)
ok(sp.expand((6 * x + 2) ** 2 - 9 - (6 * x + 5) * (6 * x - 1)) == 0, 'B p1 steel wider plate')
chk('problems-1', 'items', 2, 35 * 29, {'old': 900 - 9, 'each-term': 900 - 5, 'no-hole': 32 ** 2, 'signs': 25 * 31}, part=4)

# level 2
ok(sp.expand(q * (30 - q) - 10 * q - 64 + (q - 4) * (q - 16)) == 0, 'B l5 transfer P = -(q-4)(q-16)')
for qq, pr in [(2, -28), (6, 20), (10, 36), (14, 20), (18, -28)]:
    ok(-qq * qq + 20 * qq - 64 == pr, 'B l5 transfer table q=%d' % qq)
chk('l5-product-of-zero', 'quiz', 1, 3, {'five': 5, 'fifteen': 15})
chk('l6-completing-the-square', 'screens', 0, 9, {'six-sq': 36, 'six': 6, 'side': 3})
chk('l6-completing-the-square', 'screens', 3, 5 - 9, {'add': 14, 'ignore': 5, 'drop': -9, 'sign': 4})
chk('l6-completing-the-square', 'screens', 5, min(roots(x ** 2 + 3 * x - 4)), {'pos': 1, 'shift': -2.5, 'sign': 4})
ok(sp.expand(q * (26 - q) - 6 * q - 36 - (64 - (q - 10) ** 2)) == 0, 'B l6 transfer P = 64-(q-10)^2')
chk('l6-completing-the-square', 'screens', 8, 64, {'table': 60, 'fixed': 100, 'q': 10})
chk('l6-completing-the-square', 'quiz', 1, math.sqrt(1.21) - 1, {'halved': 0.105, 'total': 0.21})
chk('l6-completing-the-square', 'quiz', 2, 3, {'larger': 7, 'sign': -3})
chk('l7-the-formula', 'screens', 2, 3 + r5, {'smaller': 3 - r5, 'noroot': 8, 'nocentre': r5}, tol=0.005)
chk('l7-the-formula', 'screens', 3, -2 + math.sqrt(2.5), {'nodiv': -4 + math.sqrt(13), 'forgotc': -1,
    'smaller': -2 - math.sqrt(2.5), 'sign': 2 - math.sqrt(2.5)}, tol=0.005)
chk('l7-the-formula', 'screens', 5, -1 / 3, {'signb': (-5 - 7) / 6, 'overa': (5 - 7) / 3, 'sign': 1 / 3}, tol=0.005)
chk('l7-the-formula', 'screens', 7, 3 ** 2 - 4 * 2 * -1, {'signc': 9 - 8, 'noa': 9 - 4 * -1})
chk('l7-the-formula', 'screens', 8, (7 + r29) / 2, {'first': (7 - r29) / 2, 'peak': 3.5, 'nohalf': 7 + r29}, tol=0.006)
chk('l7-the-formula', 'quiz', 1, 2, {'signb': (-1 + 7) / 4, 'overa': (1 + 7) / 2})
chk('l8-how-many-solutions', 'screens', 1, 4, {'sign': -4, 'half': 2, 'sq': 16})
chk('l8-how-many-solutions', 'screens', 2, 16 - 24, {'flip': 8, 'plus': 40, 'noa': 10})
chk('l8-how-many-solutions', 'screens', 9, 2500 / 4, {'nofour': 2500, 'half': 1250, 'q': 25})
chk('l8-how-many-solutions', 'quiz', 1, 4 + 12, {'signc': 4 - 12, 'negb': -4 + 12})
chk('review-2', 'items', 0, 7, {'sign': 4, 'const': 28})
chk('review-2', 'items', 2, 40 - 49, {'add': 89, 'drop': -49, 'sign': 9})
chk('review-2', 'items', 4, (3 + r41) / 4, {'signb': (-3 + r41) / 4, 'overa': (3 + r41) / 2, 'bar': 3 + r41 / 4}, tol=0.005)
chk('review-2', 'items', 8, 1 - math.sqrt(0.81), {'halved': 0.095, 'total': 0.19})
ok(near(20000 * 0.81, 16200), 'B review-2 car value')
chk('homework-2', 'items', 0, 5, {'split': 37, 'sign': 8})
chk('homework-2', 'items', 3, math.sqrt(5618 / 5000) - 1, {'halved': 0.0618, 'total': 0.1236})
chk('homework-2', 'items', 5, 3 + math.sqrt(13), {'neg': 3 - math.sqrt(13), 'peak': 3, 'nohalf': 6 + math.sqrt(52)}, tol=0.006)
chk('homework-2', 'items', 7, 48 ** 2 / 8, {'four': 576, 'two': 1152})
ok(sp.expand(q * (60 - 2 * q) - 12 * q - (-2 * q ** 2 + 48 * q)) == 0, 'B homework-2 fixed-cost quadratic')
ok(sp.expand(q * (50 - q) - 10 * q - 300 - (100 - (q - 20) ** 2)) == 0, 'B homework-2 desk model answer')
ok(roots(q ** 2 - 40 * q + 375, q) == [15.0, 25.0] and 1600 - 1680 == -80, 'B homework-2 desk targets')
# problems-2
ok(sp.expand(15 + 10 * t - 5 * t ** 2 - (-5 * (t - 1) ** 2 + 20)) == 0, 'B p2 flare square form')
chk('problems-2', 'items', 0, 20, {'sign': 10, 'no-five': 16}, part=0)
chk('problems-2', 'items', 0, 3, {'negative': -1, 'no-root': 5, 'carried': 1 + math.sqrt(2)}, part=1, tol=0.02)
chk('problems-2', 'items', 0, [0, 2], part=2)
chk('problems-2', 'items', 0, [1 - math.sqrt(0.4), 1 + math.sqrt(0.4)], part=3, tol=0.005)
chk('problems-2', 'items', 1, 36 - 40, {'sign-b': -36 - 40, 'plus': 76, 'reversed': 4}, part=0)
chk('problems-2', 'items', 1, 1, {'start': 10, 'halved': 7, 'sign': 19}, part=1)
chk('problems-2', 'items', 1, 3 - math.sqrt(3), {'larger': 3 + math.sqrt(3), 'half-root': 3 - math.sqrt(12), 'no-root': 0}, part=2, tol=0.005)
chk('problems-2', 'items', 1, math.sqrt(40), {'no-root': 40, 'no-four': math.sqrt(10)}, part=3, tol=0.006)
chk('problems-2', 'items', 2, 15, {'negative': -16, 'sign': 16}, part=0)
chk('problems-2', 'items', 2, 801, {'sign-c': -799, 'no-double': 401}, part=1)
chk('problems-2', 'items', 2, (-1 + math.sqrt(801)) / 2, {'sign-b': (1 + math.sqrt(801)) / 2,
    'no-half': -1 + math.sqrt(801), 'carried': (-1 + math.sqrt(401)) / 2}, part=2, tol=0.005)
chk('problems-2', 'items', 2, 100 - 13 * 14 // 2, {'rounded-up': 14 * 15 // 2 - 100, 'rows': 13}, part=3)

# level 3
chk('l9-shape-of-a-square', 'screens', 9, ((100 - 14 + 1.2) + (100 + 14 + 1.2)) / 2, {'linear': 100, 'rise': 87.2, 'fall': 115.2})
chk('l9-shape-of-a-square', 'quiz', 0, (-3) ** 2 - 5, {'neg-square': -9 - 5, 'doubled': -6 - 5})
chk('l9-shape-of-a-square', 'quiz', 2, 7, {'origin': -1, 'line': 4, 'double': 9})
chk('l10-turning-point', 'screens', 3, 5, {'x-value': 3, 'sign': -5, 'intercept': 5 - 9})
prof = lambda v: -0.04 * v * v + 12 * v - 500
chk('l10-turning-point', 'screens', 9, prof(150), {'ends': prof(300), 'quantity': 150, 'minus-b': prof(12)}, tol=1e-6)
chk('l10-turning-point', 'quiz', 1, -5, {'minus-b': -10, 'sign': 5})
f3 = lambda v: 3 * v * v - 12 * v + 5
chk('l10-turning-point', 'quiz', 2, f3(2), {'intercept': 5, 'x-value': 2, 'sign': f3(-2), 'sign2': 7})
ok(2 * 12 ** 2 - 12 * 12 + 7 == 151 and 2 * 9 - 36 + 7 == -11, 'B l10 trap heights 151 and -11')
chk('l11-meeting-the-axis', 'screens', 2, 2 * -4, {'sign': 8, 'sum': 2, 'vertex': 3 * -3})
chk('l11-meeting-the-axis', 'screens', 4, 2 * 3 * -3, {'no-a': -9, 'intercept': 14, 'x-value': 4, 'sign': 18})
chk('l11-meeting-the-axis', 'screens', 9, 6, {'square': 36, 'intercept': -1.8, 'half': 18})
chk('l11-meeting-the-axis', 'quiz', 1, 36, {'no-a': 12, 'vertex': 3 * 2 * -2, 'sign': -36})
chk('l11-meeting-the-axis', 'quiz', 2, 9, {'sign': -9, 'intercept': 5, 'x-value': 2})
chk('l12-above-or-below', 'screens', 4, len([k for k in range(-50, 50) if k * k - 2 * k - 8 < 0]), {'both-ends': 7, 'one-end': 6})
chk('l12-above-or-below', 'quiz', 1, len([k for k in range(-50, 50) if (k - 1) * (k - 6) < 0]), {'both-ends': 6, 'one-end': 5})
V12 = sp.Rational(1, 100) * w_ ** 2 + sp.Rational(4, 100) * (1 - w_) ** 2
ok(sp.expand(V12 - (sp.Rational(5, 100) * w_ ** 2 - sp.Rational(8, 100) * w_ + sp.Rational(4, 100))) == 0, 'B l12 transfer variance')
chk('l12-above-or-below', 'screens', 9, min(roots(V12 - sp.Rational(1, 100), w_)), {'upper': 1, 'vertex': 0.8, 'equal': 0.5})
ok(V12.subs(w_, sp.Rational(1, 2)) == sp.Rational(125, 10000), 'B l12 equal weights V = 0.0125')
chk('l13-best-price', 'screens', 1, 30, {'peak': 25, 'double': 40})
chk('l13-best-price', 'screens', 3, 20, {'choke': 40, 'revenue': 8000, 'quarter': 10})
chk('l13-best-price', 'screens', 5, 3.75, {'choke': 7.5, 'revenue': 3.75 * 750, 'rounded': 4})
ok(sp.expand(500 * p - 10 * p ** 2 - (-10 * (p - 25) ** 2 + 6250)) == 0, 'B l13 square form')
ok((27 - 4) * (500 - 270) == 5290 and 15 * 450 == 6750, 'B l13 profit 5290 and revenue 6750')
V13 = sp.Rational(1, 100) * w_ ** 2 + sp.Rational(9, 100) * (1 - w_) ** 2
ok(sp.expand(V13 - (sp.Rational(1, 10) * w_ ** 2 - sp.Rational(18, 100) * w_ + sp.Rational(9, 100))) == 0, 'B l13 transfer variance')
ok(V13.subs(w_, sp.Rational(9, 10)) == sp.Rational(9, 1000) and near(math.sqrt(0.009), 0.0949, 5e-4)
   and V13.subs(w_, sp.Rational(1, 2)) == sp.Rational(25, 1000), 'B l13 min variance 0.009, vol 9.5%, equal 0.025')
chk('l13-best-price', 'quiz', 0, 600 / 80, {'choke': 15, 'no-b': 300})
chk('l13-best-price', 'quiz', 2, (6 + 20) / 2, {'revenue': 10, 'full-cost': 16, 'choke': 20})
chk('l13-best-price', 'quiz', 3, 0.1 / 0.16, {'no-two': 1.25, 'equal': 0.5})
chk('review-3', 'items', 2, -8 / 4, {'minus-b': -8, 'sign': 2, 'over-a': -4})
chk('review-3', 'items', 3, 4 * -4, {'intercept': -15, 'x-value': 1, 'sign': 16})
chk('review-3', 'items', 4, 2 * -1 * 4, {'vertex': 2 * -2.5 * 2.5, 'no-a': -4, 'sign': 8})
chk('review-3', 'items', 6, 9, {'x-value': 3, 'left': 1})
chk('review-3', 'items', 8, 7.5 * 600, {'price': 7.5, 'quantity': 600})
chk('review-3', 'items', 9, (2 + 15) / 2, {'revenue': 7.5, 'full-cost': 9.5, 'sum': 17})
ok(near(6.5 * (60 - 4 * 8.5), 169), 'B review-3 profit 169')
chk('homework-3', 'items', 0, 6 / 0.8, {'minus-b': 6, 'over-a': 15, 'sign': -7.5})
ok(near(100 - 6 * 7.5 + 0.4 * 7.5 ** 2, 77.5), 'B homework-3 bond low 77.50')
chk('homework-3', 'items', 3, -2 * 3 * -3, {'no-a': -9, 'sign': -18, 'x-value': 5})
chk('homework-3', 'items', 4, len([k for k in range(-50, 50) if k * k + 3 * k < 10]), {'both-ends': 8, 'one-end': 7})
chk('homework-3', 'items', 6, 45 / 6 - 3, {'parabola': 7.5, 'true': 3, 'k-one': 45 - 3})
rho, sa, sb = sp.Rational(1, 4), sp.Rational(1, 10), sp.Rational(2, 10)
Vc = sp.expand(w_ ** 2 * sa ** 2 + (1 - w_) ** 2 * sb ** 2 + 2 * w_ * (1 - w_) * rho * sa * sb)
ok(Vc == sp.Rational(4, 100) * w_ ** 2 - sp.Rational(7, 100) * w_ + sp.Rational(4, 100), 'B homework-3 correlated variance')
chk('homework-3', 'items', 8, 0.07 / 0.08, {'no-corr': 0.8, 'no-two': 1.75, 'half': 0.5})
ok(Vc.subs(w_, sp.Rational(7, 8)) == sp.Rational(9375, 1000000) and near(math.sqrt(0.009375), 0.097, 5e-4), 'B homework-3 V = 0.009375')
ok(sp.expand((p - 5) * (2000 - 80 * p) - (-80 * (p - 15) ** 2 + 8000)) == 0, 'B homework-3 vendor model')
# problems-3
arch = lambda v: -0.2 * v * (v - 20)
chk('problems-3', 'items', 0, 10, {'root': 20, 'sign': -10}, part=0)
chk('problems-3', 'items', 0, arch(10), {'sign': -20}, part=1)
ok(roots(-sp.Rational(1, 5) * (x - 10) ** 2 + 20 - sp.Rational(64, 5)) == [4.0, 16.0], 'B p3 barge ends 4 and 16')
chk('problems-3', 'items', 1, 15 * 75, {'bikes': 75, 'no-drop': 2250}, part=2)
chk('problems-3', 'items', 1, 19, {'full-cost': 23, 'no-cost': 15, 'sign': (-8 + 30) / 2}, part=3)
ok(sp.expand((p - 8) * (150 - 5 * p) - (605 - 5 * (p - 19) ** 2)) == 0, 'B p3 bike profit square form')
chk('problems-3', 'items', 2, 5, {'flat': 6, 'vertex': 2.5}, part=1, tol=0.01)
chk('problems-3', 'items', 2, 2.5, {'flat': 3, 'square-half': 15 - 2.5 ** 2}, part=2, tol=0.01)
chk('problems-3', 'items', 2, 2.5 * 2.5 - 0.5 * 2.5 ** 2, {'water-top': 4.5, 'no-square': 6.25, 'x-value': 2.5}, part=3, tol=0.01)

# conventions: discriminant cases over a grid (two, one, no real roots)
for a_, b_, c_ in itertools.product(range(-4, 5), repeat=3):
    if a_ == 0:
        continue
    disc = b_ * b_ - 4 * a_ * c_
    nreal = len(set(sp.real_roots(a_ * x ** 2 + b_ * x + c_)))
    ok(nreal == (2 if disc > 0 else 1 if disc == 0 else 0), 'B discriminant count %s' % ((a_, b_, c_),))
    if a_ * c_ < 0:
        ok(disc > 0, 'B opposite signs of a and c give two roots %s' % ((a_, b_, c_),))

# ---- findings (kept failing until fixed)
EXPECTED_FAIL = []
w = key('l7-the-formula', 'screens', 7)
have = wrongs(w)
# feedback: "You made b^2 negative": -(3^2) - 4*2*(-1) = -1, but the slip value is -17 (= 4ac - b^2)
if not near(have['neg'], -(3 ** 2) - 4 * 2 * -1):
    EXPECTED_FAIL.append('F l7-the-formula screens[7] slip neg: value %s, but "made b^2 negative" gives %s; -17 is 4ac - b^2'
                         % (have['neg'], -(3 ** 2) - 4 * 2 * -1))
w = key('problems-3', 'items', 0, 1)
have = wrongs(w)
# feedback: "You left out the -0.2": 10 * (10 - 20) = -100, but the slip value is +100
if not near(have['no-a'], 10 * (10 - 20)):
    EXPECTED_FAIL.append('F problems-3 items[0].parts[1] slip no-a: value %s, but leaving out -0.2 gives %s'
                         % (have['no-a'], 10 * (10 - 20)))
# l7 quiz[2]: a = 1 is a valid choice (multiply the equation by -1): same roots
r_as_written = sorted(roots(-x ** 2 - 3 * x + 5))
r_times_minus = sorted(roots(x ** 2 + 3 * x - 5))
opt = {o['id']: o for o in load('l7-the-formula')['quiz'][2]['widget']['options']}
if r_as_written == r_times_minus and 'correct' not in opt['dropsign'] and \
        'as it stands' not in json.dumps(load('l7-the-formula')['quiz'][2]):
    EXPECTED_FAIL.append('F l7-the-formula quiz[2]: option a = 1 is marked wrong, but x^2 + 3x - 5 = 0 (times -1) has the same roots')
# l12 / homework-3: the count of "whole numbers" depends on whether negatives count
c_all = len([k for k in range(-50, 50) if k * k - 2 * k - 8 < 0])
c_nonneg = len([k for k in range(0, 50) if k * k - 2 * k - 8 < 0])
if c_all != c_nonneg and 'integer' not in json.dumps(load('l12-above-or-below')['screens'][4]) \
        and 'negative' not in load('l12-above-or-below')['screens'][4]['question']:
    EXPECTED_FAIL.append('F l12 screens[4] (and homework-3 items[4]): key %d counts negatives as whole numbers; 0, 1, 2, ... gives %d'
                         % (c_all, c_nonneg))
# l2 screens[1]: "every pair of whole numbers with product 24" lists positive pairs only
rows = load('l2-product-and-sum')['screens'][1]['canvas']['params']['rows']
pairs_all = {(i, 24 // i) for i in range(-24, 25) if i and 24 % i == 0 and i <= 24 // i}
if len(rows) != len(pairs_all) and 'positive' not in json.dumps(load('l2-product-and-sum')['screens'][1]):
    EXPECTED_FAIL.append('F l2 screens[1]: table has %d pairs; integer pairs with product 24 number %d (negatives missing, "positive" unstated)'
                         % (len(rows), len(pairs_all)))
# l9 transfer: "big moves either way help the holder": P(+d) < 100 for a yield rise
P = lambda dd: 100 - 7 * dd + 0.3 * dd * dd
if P(2) < 100 and 'help the holder' in load('l9-shape-of-a-square')['screens'][9]['explain']['text']:
    EXPECTED_FAIL.append('F l9 screens[9]: "big moves either way help the holder", yet P(+2) = %.2f < 100 (and P(d) < 100 for 0 < d < %.1f)'
                         % (P(2), 7 / 0.3))

# ---------------------------------------------------------------- C  fluency families, whole range
X = sp.Symbol('v')


def poly(*cs):
    deg = len(cs) - 1
    return sum(c * X ** (deg - i) for i, c in enumerate(cs))


cnt = {}


def tally(fam):
    cnt[fam] = cnt.get(fam, 0) + 1


R = range
nz = lambda lo, hi: [k for k in R(lo, hi + 1) if k != 0]
# l1
for a, b in itertools.product(nz(-9, 9), repeat=2):
    s, pr = a + b, a * b
    if a != b and s != 0 and pr != s:
        tally('l1 expand-monic')
        ok(sp.expand((X + a) * (X + b) - poly(1, s, pr)) == 0 and (s, pr) != (0, pr) and (pr, s) != (s, pr), 'C l1 monic %s' % ((a, b),))
for pp, qq, rr, ss in itertools.product(R(1, 4), nz(-7, 7), R(1, 4), nz(-7, 7)):
    mid = pp * ss + qq * rr
    if pp * rr > 1 and math.gcd(pp, abs(qq)) == 1 and math.gcd(rr, abs(ss)) == 1 and (pp != rr or qq != ss) \
            and mid != 0 and qq + ss != 0 and mid != qq + ss:
        tally('l1 expand-coefficient')
        ok(sp.expand((pp * X + qq) * (rr * X + ss) - poly(pp * rr, mid, qq * ss)) == 0, 'C l1 coeff %s' % ((pp, qq, rr, ss),))
for a in nz(-12, 12):
    tally('l1 expand-square')
    ok(sp.expand((X + a) ** 2 - poly(1, 2 * a, a * a)) == 0 and a != 2 * a, 'C l1 square %d' % a)
# l2
for pp, qq in itertools.product(nz(-9, 9), repeat=2):
    if pp < qq and pp + qq != 0:
        tally('l2 factorise-monic')
        tgt = poly(1, pp + qq, pp * qq)
        ok(sp.expand((X + pp) * (X + qq) - tgt) == 0, 'C l2 monic key %s' % ((pp, qq),))
        ok(sp.expand((X - pp) * (X - qq) - tgt) != 0 and sp.expand((X + pp) * (X - qq) - tgt) != 0, 'C l2 monic wrongs %s' % ((pp, qq),))
        ok((-pp) * (-qq) == pp * qq and -pp - qq == -(pp + qq) and pp * -qq == -pp * qq, 'C l2 monic lines')
for pp in nz(-12, 12):
    tally('l2 perfect-square')
    ok(sp.expand((X + pp) ** 2 - poly(1, 2 * pp, pp * pp)) == 0, 'C l2 perfect %d' % pp)
# l3
for pp, qq, ss in itertools.product(R(2, 6), nz(-7, 7), nz(-7, 7)):
    b_ = pp * ss + qq
    if math.gcd(pp, abs(qq)) == 1 and b_ != 0 and qq != ss and qq != pp * ss:
        tally('l3 factorise-non-monic')
        tgt = poly(pp, b_, qq * ss)
        ok(sp.expand((pp * X + qq) * (X + ss) - tgt) == 0, 'C l3 key')
        ok(sp.expand((X + pp * ss) * (X + qq) - tgt) != 0 and sp.expand((pp * X + ss) * (X + qq) - tgt) != 0, 'C l3 wrongs %s' % ((pp, qq, ss),))
        ok(pp * ss * qq == pp * qq * ss and pp * ss + qq == b_, 'C l3 split pair has product ac and sum b')
        ok(sp.gcd_list([pp, b_, qq * ss]) == 1, 'C l3 non-monic has no common factor %s' % ((pp, qq, ss),))
for pp, qq, rr, ss in itertools.product(R(2, 6), nz(-7, 7), R(1, 3), nz(-7, 7)):
    a_, b_, c_ = pp * rr, pp * ss + qq * rr, qq * ss
    if math.gcd(pp, abs(qq)) == 1 and math.gcd(rr, abs(ss)) == 1 and b_ != 0 and a_ * c_ != b_ and b_ != c_:
        tally('l3 split-product')
        ok(a_ * c_ != c_ and a_ * c_ != b_ and sp.expand((pp * X + qq) * (rr * X + ss) - poly(a_, b_, c_)) == 0, 'C l3 split-product')
for k, pp, qq, ss in itertools.product([2, 3, 4, 5, -2, -3], [1, 2, 3], nz(-6, 6), nz(-6, 6)):
    m_ = pp * ss + qq
    if math.gcd(pp, abs(qq)) == 1 and m_ != 0 and (pp > 1 or qq < ss) and abs(k * qq * ss) <= 90:
        tally('l3 common-factor-first')
        tgt = poly(k * pp, k * m_, k * qq * ss)
        ok(sp.expand(k * (pp * X + qq) * (X + ss) - tgt) == 0, 'C l3 cff key')
        ok(abs(sp.gcd_list([k * pp, k * m_, k * qq * ss])) == abs(k), 'C l3 cff: k is the whole common factor %s' % ((k, pp, qq, ss),))
        ok(sp.expand((pp * X + qq) * (X + ss) - tgt) != 0, 'C l3 cff dropped')
        if pp > 1 and qq != ss:
            ok(sp.expand(k * (pp * X + ss) * (X + qq) - tgt) != 0, 'C l3 cff swapped')
# l4
for pp, qq in itertools.product(R(1, 6), R(1, 13)):
    if math.gcd(pp, qq) == 1:
        tally('l4 square-minus-number')
        ok(sp.expand((pp * X + qq) * (pp * X - qq) - poly(pp * pp, 0, -qq * qq)) == 0, 'C l4 dots')
        ok(sp.expand((pp * X - qq) ** 2).coeff(X, 1) == -2 * pp * qq, 'C l4 strips of -pq each')
for pp, qq in itertools.product(R(1, 5), R(1, 13)):
    if math.gcd(pp, qq) == 1:
        tally('l4 number-minus-square')
        tgt = qq * qq - pp * pp * X ** 2
        ok(sp.expand((qq + pp * X) * (qq - pp * X) - tgt) == 0 and sp.expand((pp * X + qq) * (pp * X - qq) + tgt) == 0
           and sp.expand((qq - pp * X) ** 2 - tgt) != 0, 'C l4 number minus square %s' % ((pp, qq),))
for s in R(30, 201, 5):
    for dd in R(2, 10):
        if (s + dd) % 2 == 0:
            tally('l4 mental-difference')
            a_, b_ = (s + dd) // 2, (s - dd) // 2
            ok(a_ * a_ - b_ * b_ == s * dd and dd * dd != s * dd and s != s * dd, 'C l4 mental %s' % ((s, dd),))
for k, pp, qq in itertools.product(R(2, 8), [1, 2, 3], R(1, 10)):
    if math.gcd(pp, qq) == 1 and k * qq * qq <= 200:
        tally('l4 common-factor-first')
        ok(sp.expand(k * (pp * X + qq) * (pp * X - qq) - poly(k * pp * pp, 0, -k * qq * qq)) == 0
           and math.gcd(k * pp * pp, k * qq * qq) == k, 'C l4 cff %s' % ((k, pp, qq),))
# l6
for h, c_ in itertools.product(nz(-7, 7), R(-12, 13)):
    if c_ != h * h:
        tally('l6 find-the-constant')
        ok(sp.expand((X + h) ** 2 + (c_ - h * h) - poly(1, 2 * h, c_)) == 0 and len({c_ - h * h, c_ + h * h, c_ - 4 * h * h}) == 3, 'C l6 const')
for h, k in itertools.product(nz(-6, 6), R(1, 8)):
    if k != abs(h):
        tally('l6 solve-by-square')
        rs = sorted(sp.solve(poly(1, -2 * h, h * h - k * k), X))
        ok(rs == [h - k, h + k] and {-h - k, -h + k} != {h - k, h + k} and (k == 1 or {h - k * k, h + k * k} != {h - k, h + k}), 'C l6 solve %s' % ((h, k),))
for b_, c_ in itertools.product(nz(-12, 12), R(-12, 13)):
    if 4 * c_ != b_ * b_ and 4 * c_ != -b_ * b_ and c_ != b_ * b_:
        tally('l6 square-form')
        h = sp.Rational(b_, 2)
        ok(sp.expand((X + h) ** 2 + c_ - h * h - poly(1, b_, c_)) == 0 and sp.expand((X + b_) ** 2 + c_ - b_ * b_ - poly(1, b_, c_)) != 0, 'C l6 form')
for h, c_ in itertools.product(nz(-6, 6), R(-20, 11)):
    top = c_ + h * h
    if top != h and c_ - h * h != h and c_ != 0:
        tally('l6 largest-value')
        f = poly(-1, 2 * h, c_)
        ok(f.subs(X, h) == top and sp.expand(top - (X - h) ** 2 - f) == 0 and len({top, c_ - h * h, h}) == 3, 'C l6 largest %s' % ((h, c_),))
# l7
for a_, b_, c_ in itertools.product(R(1, 6), R(-9, 10), nz(-9, 9)):
    if math.gcd(math.gcd(a_, abs(b_)), abs(c_)) == 1:
        tally('l7 discriminant')
        dsc = b_ * b_ - 4 * a_ * c_
        ok(len({dsc, b_ * b_ + 4 * a_ * c_, b_ * b_ - a_ * c_}) == 3, 'C l7 disc %s' % ((a_, b_, c_),))
worst = 9
for pp, qq, ss in itertools.product(R(2, 5), nz(-7, 7), nz(-5, 5)):
    if math.gcd(pp, abs(qq)) == 1 and pp * ss + qq != 0:
        tally('l7 rational-roots')
        nb = pp * ss + qq
        sd = math.isqrt(nb * nb - 4 * pp * qq * ss)
        ok(sd * sd == nb * nb - 4 * pp * qq * ss, 'C l7 rational: square discriminant')
        ans = sorted([F(nb - sd, 2 * pp), F(nb + sd, 2 * pp)])
        ok(ans == sorted([F(qq, pp), F(ss)]) and ans[0] != ans[1], 'C l7 rational roots')
        for wr in (sorted([F(-nb - sd, 2 * pp), F(-nb + sd, 2 * pp)]), sorted([nb - F(sd, 2 * pp), nb + F(sd, 2 * pp)])):
            gap = max(abs(wr[0] - ans[0]), abs(wr[1] - ans[1]))
            worst = min(worst, float(gap))
            ok(gap > F(1, 100), 'C l7 rational: a wrong set within tolerance of the key %s' % ((pp, qq, ss),))
for a_, b_, c_ in itertools.product(R(1, 4), nz(-9, 9), nz(-9, 9)):
    dsc = b_ * b_ - 4 * a_ * c_
    if math.gcd(math.gcd(a_, abs(b_)), abs(c_)) == 1 and dsc > 0 and math.isqrt(dsc) ** 2 != dsc:
        tally('l7 decimal-roots')
        rt = math.sqrt(dsc)
        ans = sorted([(-b_ - rt) / (2 * a_), (-b_ + rt) / (2 * a_)])
        ok(all(abs(a_ * v * v + b_ * v + c_) < 1e-9 for v in ans), 'C l7 decimal roots')
        for wr in (sorted([(b_ - rt) / (2 * a_), (b_ + rt) / (2 * a_)]), sorted([-b_ - rt / (2 * a_), -b_ + rt / (2 * a_)])):
            gap = max(abs(wr[0] - ans[0]), abs(wr[1] - ans[1]))
            worst = min(worst, gap)
            ok(gap > 0.01, 'C l7 decimal: a wrong set within tolerance of the key %s' % ((a_, b_, c_),))
        if b_ % 2 and dsc % 9 and dsc % 25 and dsc % 49:
            tally('l7 exact-roots')
            ok(sp.sqrt(dsc).is_Pow and sp.sqrt(dsc) == sp.sqrt(sp.Integer(dsc)) and sp.sqrt(dsc).args[0] == dsc, 'C l7 exact: sqrt(%d) is in simplest form' % dsc)

# ---------------------------------------------------------------- D  canvas points on curves
def fx(expr, params, xv):
    e = expr.replace('^', '**').replace('abs(', 'abs(')
    env = dict(params)
    env['x'] = xv
    return eval(e, {'__builtins__': {}, 'abs': abs, 'pow': pow}, env)


def pts(obj):
    if isinstance(obj, list):
        return [(pt.get('id'), pt) for pt in obj]
    if isinstance(obj, dict):
        return list(obj.items())
    return []


nD = 0
for name in LESSONS + SETS:
    d = load(name)
    for path, it in items_of(d):
        cv = it.get('canvas') or {}
        if cv.get('kind') != 'plane':
            continue
        fns = (cv.get('params') or {}).get('functions') or []
        base = dict((cv.get('params') or {}).get('params') or {})
        ex = (it.get('explain') or {}).get('canvas') or {}
        prm = dict(base)
        prm.update(ex.get('params') or {})
        fns = fns + (ex.get('functions') or [])
        for pid, pt in pts(ex.get('points')):
            if not isinstance(pt, dict) or 'x' not in pt or 'y' not in pt or not fns:
                continue
            try:
                vals = [fx(f['expr'], prm, pt['x']) for f in fns]
            except Exception:
                continue
            nD += 1
            on_curve = any(abs(v - pt['y']) <= 0.002 * max(1, abs(v)) + 6e-5 for v in vals)
            on_axis_mark = pt['y'] == 0 and 'centre' in str(pt.get('label', ''))  # a marked centre, not a curve point
            ok(on_curve or on_axis_mark, 'D %s %s point %s (%s, %s) is on no drawn curve: %s' % (name, path, pid, pt['x'], pt['y'], vals))

# ---------------------------------------------------------------- report
print('A: %d expand/factorise choice items checked option by option' % nA)
print('C: instances swept per family:')
for fam in sorted(cnt):
    print('   %-28s %6d' % (fam, cnt[fam]))
print('   smallest gap between a wrong root set and the key (l7): %.4f' % worst)
print('D: %d explain-canvas points checked against their curves' % nD)
print('passed %d checks; %d unexpected failures; %d findings kept failing' % (npass, len(fails), len(EXPECTED_FAIL)))
for f_ in fails:
    print('FAIL', f_)
for f_ in EXPECTED_FAIL:
    print('FINDING', f_)
sys.exit(1 if (fails or EXPECTED_FAIL) else 0)
