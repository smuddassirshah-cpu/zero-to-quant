"""Recompute every number in app/content/courses/complex/problems-1.json to problems-3.json twice.

Route 1 is exact: sympy (complex arithmetic, solve, arg, residues, symbolic integrals and derivatives).
Route 2 is a different method in floating point: Python complex numbers and cmath, numpy.roots,
scipy.integrate.quad on the real line, the trapezium rule round contours, a Monte Carlo check where a
distribution is involved, and Black-Scholes call prices integrated over log strikes for the Carr-Madan value.

Per part:
- numeric: the two routes agree; the key lies within its band of the value; the question names a form when
  the key is not whole; every wrong value equals its named slip (recomputed here) to the rounding asked, lies
  outside the key band, and no two wrong bands overlap; the key is printed in feedback.correct and explain.
- expression: the answer and every accept form equal the exact value; every wrong form equals its named slip
  and differs from the key and from the other slips.
- choice: the keyed option, and every distractor has a why.
Per item: `vocab` (every number printed anywhere in the item is a given, a computed value or a slip value).
numbers_lib (Level, expect, check_wrongs, report) records every check. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-complex-numbers.py [--verbose]
"""
import cmath
import itertools
import math
import os
import re
import sys

import numpy as np
import sympy as sp
from scipy import integrate
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import Level, _numbers  # noqa: E402

TR = standard_transformations + (implicit_multiplication_application,)
I, pi, sqrt, E = sp.I, sp.pi, sp.sqrt, sp.E
R = sp.Rational
x, y, z, t, u = sp.symbols('x y z t u', real=True)
SYM = {'x': x, 'y': y, 'z': z, 't': t, 'u': u, 'I': I, 'pi': pi, 'E': E, 'sqrt': sp.sqrt, 'log': sp.log, 'exp': sp.exp}
FORM = re.compile(r'decimal|places?\b|fraction|whole number|nearest|in pounds|per cent|%|exact', re.I)


# ------------------------------------------------------------------ tex to sympy
def _group(s, k):
    """s[k] == '{': return (content, index after the closing brace)."""
    depth = 0
    for j in range(k, len(s)):
        depth += s[j] == '{'
        depth -= s[j] == '}'
        if depth == 0:
            return s[k + 1:j], j + 1
    raise ValueError(s)


def tex2py(s):
    s = s.replace('\\left', '').replace('\\right', '').replace('\\,', '').replace(' ', '')
    out, k = '', 0
    while k < len(s):
        if s.startswith('\\frac', k) or s.startswith('\\tfrac', k) or s.startswith('\\dfrac', k):
            k = s.index('{', k)
            a, k = _group(s, k)
            b, k = _group(s, k)
            out += f'(({tex2py(a)})/({tex2py(b)}))'
        elif s.startswith('\\sqrt', k):
            k += 5
            if s[k] == '{':
                a, k = _group(s, k)
            else:
                a, k = s[k], k + 1
            out += f'sqrt({tex2py(a)})'
        elif s.startswith('\\pi', k):
            out += '(pi)'
            k += 3
        elif s.startswith('\\ln', k):
            k += 3
            m = re.match(r'\d+', s[k:])
            if m:
                out += f'log({m.group(0)})'
                k += len(m.group(0))
            else:
                out += 'log'
        elif s[k] == '^':
            k += 1
            if s[k] == '{':
                a, k = _group(s, k)
            else:
                a, k = s[k], k + 1
            out += f'**({tex2py(a)})'
        elif s[k] == 'i':
            out += '(I)'
            k += 1
        elif s[k] == 'e' and (k + 1 < len(s) and s[k + 1] == '^'):
            out += '(E)'
            k += 1
        else:
            out += s[k]
            k += 1
    return out


def val(s):
    return parse_expr(tex2py(s), local_dict=SYM, transformations=TR)


def eq(a, b):
    d = sp.simplify(sp.expand(sp.sympify(a) - sp.sympify(b)))
    if d == 0:
        return True
    pts = [{x: 0.7, y: 1.3, z: 0.9, t: 0.45, u: 0.35}, {x: 1.9, y: -0.6, z: 2.2, t: 0.8, u: -0.4}]
    return all(abs(complex(sp.N(d.subs(p)))) < 1e-9 for p in pts)


# ------------------------------------------------------------------ checks
class Checker:
    def __init__(self, n):
        self.n = n
        self.lv = Level('complex', n)
        self.items = self.lv.files[f'problems-{n}']['items']
        self.allowed = {i: set() for i in range(len(self.items))}

    def part(self, i, k):
        return self.items[i]['parts'][k - 1]

    def allow(self, i, *vals):
        for v in vals:
            v = complex(v)
            for w in (v.real, v.imag, abs(v)):
                self.allowed[i].add(round(w, 9))

    def num(self, i, k, exact, alt, slips):
        p, lv = self.part(i, k), self.lv
        w, tag = p['widget'], f'problems-{self.n} item {i + 1} part {k}'
        e = float(sp.N(exact)) if not isinstance(exact, (int, float)) else float(exact)
        lv.claim(math.isclose(e, float(alt), rel_tol=1e-9, abs_tol=1e-9), f'{tag}: two routes agree on {e:.6g} ({float(alt):.6g})')
        tol = w['tol']['abs']
        lv.claim(w['kind'] == 'numeric' and abs(w['answer'] - e) <= tol + 1e-12, f'{tag}: key {w["answer"]} within {tol} of {e:.6g}')
        if float(w['answer']) != int(w['answer']):
            lv.claim(bool(FORM.search(p['question'])), f'{tag}: question names the form')
        got = {x_['id']: x_ for x_ in w.get('wrong', [])}
        lv.claim(set(got) == set(slips), f'{tag}: wrong ids {sorted(got)} are the slips {sorted(slips)}')
        lv.claim(set(got) <= set(p['feedback'].get('byKey', {})), f'{tag}: every wrong id has a byKey line')
        for wid, sv in slips.items():
            if wid in got:
                g = got[wid]
                sv = float(sp.N(sv)) if not isinstance(sv, (int, float)) else float(sv)
                lv.claim(abs(g['value'] - sv) <= max(g['tol']['abs'], 0.0005) + 1e-9,
                         f'{tag}: wrong {wid} = {g["value"]} is the slip {sv:.6g}')
                lv.claim(abs(g['value'] - w['answer']) > tol + g['tol']['abs'], f'{tag}: wrong {wid} outside the key band')
                self.allow(i, sv, g['value'])
        for a, b in itertools.combinations(got, 2):
            lv.claim(abs(got[a]['value'] - got[b]['value']) > got[a]['tol']['abs'] + got[b]['tol']['abs'], f'{tag}: wrongs {a} and {b} do not overlap')
        base = f'items[{i}].parts[{k - 1}]'
        lv.expect('problems', f'{base}.feedback.correct', w['answer'])
        lv.expect('problems', f'{base}.explain.text', w['answer'])
        self.allow(i, e, w['answer'])
        return e

    def expr(self, i, k, exact, alt, slips):
        p, lv = self.part(i, k), self.lv
        w, tag = p['widget'], f'problems-{self.n} item {i + 1} part {k}'
        lv.claim(w['kind'] == 'expression', f'{tag}: expression widget')
        if alt is not None:
            pt = {x: 0.7, y: 1.3, z: 0.9, t: 0.45, u: 0.35}
            ev = complex(sp.N(sp.sympify(exact).subs(pt)))
            av = complex(alt(*[pt[s_] for s_ in (x, y, z, t, u)])) if callable(alt) else complex(alt)
            lv.claim(abs(ev - av) < 1e-9, f'{tag}: two routes agree ({ev:.6g} vs {av:.6g})')
        for form in [w['answer']] + w.get('accept', []):
            lv.claim(eq(val(form), exact), f'{tag}: form {form} equals {exact}')
        got = {x_['id']: x_['tex'] for x_ in w.get('wrong', [])}
        lv.claim(set(got) == set(slips), f'{tag}: wrong ids {sorted(got)} are the slips {sorted(slips)}')
        lv.claim(set(got) <= set(p['feedback'].get('byKey', {})), f'{tag}: every wrong id has a byKey line')
        for wid, sv in slips.items():
            if wid in got:
                g = val(got[wid])
                lv.claim(eq(g, sv), f'{tag}: wrong {wid} {got[wid]} is the slip {sv}')
                lv.claim(not eq(g, exact), f'{tag}: wrong {wid} differs from the key')
                if not g.free_symbols:
                    self.allow(i, complex(sp.N(g)))
        for a, b in itertools.combinations(got, 2):
            lv.claim(not eq(val(got[a]), val(got[b])), f'{tag}: wrongs {a} and {b} differ')
        if not sp.sympify(exact).free_symbols:
            self.allow(i, complex(sp.N(exact)))

    def pick(self, i, k, cid):
        opts = self.part(i, k)['widget']['options']
        keyed = [o['id'] for o in opts if o.get('correct')]
        self.lv.claim(keyed == [cid], f'problems-{self.n} item {i + 1} part {k}: keyed option {keyed} is {cid}')
        self.lv.claim(all(o.get('why') for o in opts if not o.get('correct')), f'problems-{self.n} item {i + 1} part {k}: every distractor has a why')

    def vocab(self, i, givens, small=12):
        """Every number printed in item i is a given, a computed value, a slip, or a whole number up to `small`."""
        self.allow(i, *givens)
        ok_vals = self.allowed[i]
        it = self.items[i]

        def strings(o):
            if isinstance(o, str):
                yield o
            elif isinstance(o, dict):
                for kk, v in o.items():
                    if kk not in ('id', 'kind', 'keyboard', 'form', 'skills', 'answer', 'tex', 'value', 'tol', 'wrong', 'accept'):
                        yield from strings(v)
                    elif kk == 'accept' and isinstance(v, str):
                        yield v
            elif isinstance(o, list):
                for v in o:
                    yield from strings(v)
        bad = set()
        for s in strings(it):
            for v in _numbers(s):
                if abs(v) <= small and float(v).is_integer():
                    continue
                if not any(abs(abs(v) - abs(a)) <= 0.5 * 10 ** (-self._places(v)) + 1e-9 for a in ok_vals):
                    bad.add(v)
        self.lv.claim(not bad, f'problems-{self.n} item {i + 1} vocab: every printed number is given or computed', f'unexplained: {sorted(bad)}')

    @staticmethod
    def _places(v):
        s = repr(float(v))
        if 'e' in s:
            return 10
        return len(s.split('.')[1].rstrip('0')) if '.' in s else 0

    def finish(self):
        self.lv.check_wrongs(file='problems')


def deg(a):
    return float(a) * 180 / math.pi


# ================================================================== level 1
def level1():
    c = Checker(1)
    # ---- item 1: two impedances in parallel
    Z1, Z2 = 2 + 5 * I, 4 - 3 * I
    z1, z2 = 2 + 5j, 4 - 3j
    P = sp.expand(Z1 * Z2)
    c.expr(0, 1, P, z1 * z2, {'i-squared': -7 + 14 * I, 'parts-only': 8 - 15 * I})
    S = Z1 + Z2
    Z = sp.expand(sp.simplify(P / S))
    zz = z1 * z2 / (z1 + z2)
    c.expr(0, 2, Z, zz, {'split': R(23, 6) + 7 * I, 'minus-squares': sp.expand((23 + 14 * I) * (6 - 2 * I)) / 32,
                         'wrong-factor': sp.expand((23 + 14 * I) * (6 + 2 * I)) / 40})
    c.lv.claim(sp.simplify((23 + 14 * I) * (6 + 2 * I) / ((6 + 2 * I) * (6 + 2 * I)) - Z) == 0, 'item 1 part 2: top and bottom both times 6 + 2i gives the right Z, so wrong-factor keeps 40 below')
    modZ = sp.sqrt(sp.re(Z) ** 2 + sp.im(Z) ** 2)
    c.num(0, 3, modZ, abs(zz), {'no-root': sp.re(Z) ** 2 + sp.im(Z) ** 2, 'added': sp.re(Z) + sp.im(Z),
                                'carried-split': abs(23 / 6 + 7j)})
    c.num(0, 4, sp.Rational(12000, 4257), 12 / round(abs(zz), 3), {'times': 12 * 4.257, 'squared': 12 / 18.125, 'carried-split': 12 / 7.981})
    c.lv.claim(round(12 / abs(zz), 3) == round(12 / 4.257, 3), 'item 1 part 4: the exact and the restated |Z| give the same 3-place current')
    c.num(0, 5, sp.atan(sp.im(Z) / sp.re(Z)) * 180 / pi, deg(cmath.phase(zz)),
          {'inverted': sp.atan(sp.re(Z) / sp.im(Z)) * 180 / pi, 'radians': cmath.phase(zz)})
    c.vocab(0, [z1, z2, 18.125, 17.2225, 0.9025, 166 + 38j, 138, 46, 84, 28, 36, 40, 15, 6 - 2j, 180, 0.32, 36, 32, 0.95 / 4.15, 20, 83 / 20, 19 / 20])

    # ---- item 2: animation frames
    zc = sp.Symbol('zc')
    roots = sp.solve(zc ** 2 - 3 * zc + 3, zc)
    w = [r for r in roots if sp.im(r) > 0][0]
    nr = [r for r in np.roots([1, -3, 3]) if r.imag > 0][0]
    c.expr(1, 1, w, nr, {'minus-b': -sp.conjugate(w), 'no-half': R(3, 2) + sqrt(3) * I, 'lower': sp.conjugate(w)})
    c.num(1, 2, sp.Abs(w), abs(nr), {'no-root': sp.Abs(w) ** 2, 'added': 1.5 + 0.866, 'carried-no-half': abs(1.5 + math.sqrt(3) * 1j)})
    c.lv.claim(sp.simplify(sp.Abs(w) ** 2 - 3) == 0, 'item 2: |w|^2 = 9/4 + 3/4 = 3')
    c.expr(1, 3, sp.arg(w), cmath.phase(nr), {'inverted': sp.atan(sp.re(w) / sp.im(w)), 'carried-minus-b': sp.arg(-sp.conjugate(w)), 'degrees': 30})
    w6 = sp.expand(w ** 6)
    c.num(1, 4, w6, (nr ** 6).real, {'sign': 27, 'angle-only': -1, 'carried-modulus-3': -(3 ** 6)})
    n_first = next(n for n in range(1, 50) if sp.im(sp.expand(w ** n)) == 0 and sp.re(sp.expand(w ** n)) > 0)
    c.lv.claim(n_first == 12, 'item 2 part 5: first n with w^n positive real is 12')
    c.num(1, 5, sp.expand(w ** n_first), (nr ** 12).real, {'half-turn': 27, 'frames': 12, 'carried-modulus-3': 3 ** 12})
    c.vocab(1, [9, 12, -3, 1.5, 0.866, 3 / 4, 9 / 4, 2.25, 5.25, 729, 27, 30, 531441])

    # ---- item 3: four lamps, w^4 = c
    cc = R(-81, 2) + R(81, 2) * sqrt(3) * I
    cn = complex(sp.N(cc))
    c.num(2, 1, sp.Abs(cc), abs(cn), {'added': R(81, 2) + R(81, 2) * sqrt(3), 'no-root': 6561, 'no-root3': abs(-40.5 + 40.5j)})
    c.expr(2, 2, sp.arg(cc), cmath.phase(cn), {'arctan': sp.atan(sp.im(cc) / sp.re(cc)), 'reference': pi / 3, 'swapped': pi - sp.atan(-sp.re(cc) / sp.im(cc)), 'degrees': 120})
    zc = sp.Symbol('zc')
    lamps = [sp.nsimplify(sp.expand_complex(L)) for L in sp.solve(zc ** 4 - cc, zc)]
    c.lv.claim(len(lamps) == 4, 'item 3: sympy finds four lamps')
    nl = np.roots([1, 0, 0, 0, -cn])
    for L in lamps:
        c.lv.claim(sp.simplify(sp.expand(L ** 4) - cc) == 0, f'item 3: {L} is a fourth root of c')
        c.lv.claim(min(abs(complex(sp.N(L)) - q) for q in nl) < 1e-9, f'item 3: numpy.roots has {L}')
        c.lv.claim(abs(abs(complex(sp.N(L))) - 3) < 1e-12, f'item 3: {L} is 3 m from the centre')
    q1 = [L for L in lamps if sp.re(L) > 0 and sp.im(L) > 0]
    q4 = [L for L in lamps if sp.re(L) > 0 and sp.im(L) < 0]
    c.lv.claim(len(q1) == 1 and len(q4) == 1, 'item 3: one lamp in each of quadrants 1 and 4')
    nq1 = [q for q in nl if q.real > 0 and q.imag > 0][0]
    nq4 = [q for q in nl if q.real > 0 and q.imag < 0][0]
    c.expr(2, 3, q1[0], nq1, {'modulus-9': 9 * sp.exp(I * pi / 6), 'quadrant': 3 * sp.exp(2 * pi * I / 3), 'half-angle': 3 * sp.exp(I * pi / 3)})
    c.lv.claim(sp.simplify(sp.expand_complex((3 * sp.exp(2 * pi * I / 3)) ** 4) - cc) == 0, 'item 3: the quadrant slip is a lamp, just not in quadrant 1')
    c.expr(2, 4, q4[0], nq4, {'times-i': sp.expand(I * q1[0]), 'conjugate': sp.conjugate(q1[0]), 'opposite': -q1[0]})
    c.lv.claim(sp.simplify(sp.expand(-I * q1[0]) - q4[0]) == 0, 'item 3: -i times the first lamp is the fourth-quadrant lamp')
    c.lv.claim(sp.simplify(sp.expand(sp.conjugate(q1[0]) ** 4) - sp.conjugate(cc)) == 0, 'item 3: the conjugate lamp has fourth power conj(c)')
    nb = sp.expand(I * q1[0])
    c.lv.claim(sp.simplify(nb - (R(-3, 2) + R(3, 2) * sqrt(3) * I)) == 0, 'item 3: the neighbour named in part 5 is i times the first lamp')
    dist = sp.sqrt(sp.expand((sp.re(q1[0] - nb)) ** 2 + (sp.im(q1[0] - nb)) ** 2))
    c.lv.claim(sp.simplify(dist ** 2 - 18) == 0, 'item 3: the parts of the difference squared add to 18')
    c.num(2, 5, dist, abs(nq1 - complex(sp.N(nb))), {'radius': 3, 'arc': 3 * pi / 2, 'opposite': 6})
    c.vocab(2, [cn, 6561 / 4, 6561, 81, 1.5, 3 * 3 ** 0.5 / 2, 18, 3 * 2 ** 0.5, 9 * 3 ** 0.5 / 2, 4.5, 3 ** 0.5, 81 / 4, 0.5])

    # ---- item 4: three-phase neutral current
    om = sp.exp(2 * pi * I / 3)
    A, B, C = 12, sp.expand_complex(12 * om), sp.expand_complex(7 * om ** 2)
    nB, nC = 12 * cmath.exp(2j * math.pi / 3), 7 * cmath.exp(4j * math.pi / 3)
    c.num(3, 1, sp.im(B), nB.imag, {'swapped': 12 * math.cos(2 * math.pi / 3), 'real-size': abs(12 * math.cos(2 * math.pi / 3)), 'unscaled': sp.sin(2 * pi / 3), 'degrees': 12 * math.sin(math.radians(2 * math.pi / 3))})
    c.expr(3, 2, C, nC, {'sin-sign': sp.conjugate(C), 'swapped': -R(7, 2) * sqrt(3) - R(7, 2) * I})
    N = sp.expand(A + B + C)
    nN = 12 + nB + nC
    c.expr(3, 3, N, nN, {'no-first': N - 12, 'carried-sin-sign': sp.expand(A + B + sp.conjugate(C))})
    c.lv.claim(sp.simplify(sp.expand_complex(N + 5 * om ** 2)) == 0, 'item 4: N = -5 omega^2 (1 + omega + omega^2 = 0)')
    c.num(3, 4, sp.Abs(N), abs(nN), {'added': sp.re(N) + sp.im(N), 'squared': 25, 'carried-sin-sign': sp.Abs(sp.expand(A + B + sp.conjugate(C)))})
    c.num(3, 5, sp.arg(N) * 180 / pi, deg(cmath.phase(nN)), {'inverted': 30, 'omega-squared': 240, 'radians': pi / 3})
    # fix pass: units and the wording that asks for an exact answer
    for (i_, k_, un) in ((0, 4, 'A'), (2, 5, 'm'), (3, 4, 'A')):
        c.lv.claim(c.part(i_, k_)['widget'].get('unit') == un, f'item {i_ + 1} part {k_}: unit {un} on the widget')
    for (i_, k_) in ((1, 1), (2, 3), (2, 4), (3, 2), (3, 3)):
        c.lv.claim('exactly as $p + qi$' in c.part(i_, k_)['question'], f'item {i_ + 1} part {k_}: the question asks exactly')
    for (i_, k_) in ((2, 4), (3, 2), (3, 3)):
        c.lv.claim('one fraction times $i$' in c.part(i_, k_)['question'], f'item {i_ + 1} part {k_}: the question names the form of the imaginary part')
    c.vocab(3, [nB, nC, 7 / 2, 25 / 4, 75 / 4, 120, 240, 2.094, 180, 2 * math.pi / 3, 19 / 2, 6 * 3 ** 0.5, 0.5, 75])
    return c


def cdiff(F, z0, h=1e-4):
    """Central difference along the real axis: exact for quadratics up to rounding."""
    return (F(z0 + h) - F(z0 - h)) / (2 * h)


# ================================================================== level 2
def level2():
    c = Checker(2)
    # ---- item 1: the mesh map f(z) = z^2 - 4z near 3 + 2i
    f = lambda q: q ** 2 - 4 * q
    z0, n0 = R(5, 2) + 3 * I, 2.5 + 3j
    c.expr(0, 1, sp.expand(f(z0)), f(n0), {'square-parts': R(25, 4) + 9 * I - 4 * z0, 'no-cross': R(25, 4) - 9 - 4 * z0, 'i-squared': R(25, 4) + 9 + 15 * I - 4 * z0})
    zs = sp.Symbol('zs')
    d0 = sp.diff(f(zs), zs).subs(zs, z0)
    nd = cdiff(f, n0)
    c.expr(0, 2, sp.expand(d0), nd, {'no-four': 2 * z0, 'not-doubled': z0 - 4})
    c.lv.claim(abs(cdiff(f, n0) - (f(n0 + 1e-4j) - f(n0 - 1e-4j)) / 2e-4j) < 1e-8, 'item 1: the quotient agrees along the real and imaginary directions')
    c.num(0, 3, sp.Abs(d0), abs(nd), {'no-root': 37, 'added': 7, 'carried-no-four': abs(5 + 6j)})
    c.num(0, 4, sp.atan2(sp.im(d0), sp.re(d0)) * 180 / pi, deg(cmath.phase(nd)),
          {'inverted': deg(math.atan(1 / 6)), 'radians': cmath.phase(nd), 'carried-no-four': deg(math.atan(6 / 5))})
    U = lambda X, Y: f(complex(X, Y)).real
    V = lambda X, Y: f(complex(X, Y)).imag
    h = 1e-4
    ux, uy = (U(2.5 + h, 3) - U(2.5 - h, 3)) / (2 * h), (U(2.5, 3 + h) - U(2.5, 3 - h)) / (2 * h)
    vx, vy = (V(2.5 + h, 3) - V(2.5 - h, 3)) / (2 * h), (V(2.5, 3 + h) - V(2.5, 3 - h)) / (2 * h)
    c.num(0, 5, sp.Abs(d0) ** 2 * R(1, 10000), (ux * vy - uy * vx) * 1e-4,
          {'not-squared': sp.sqrt(37) * R(1, 10000), 'side-only': sp.sqrt(37) / 100, 'unchanged': R(1, 10000)})
    c.vocab(0, [n0, -2.75 + 15j, 10 + 12j, 6.25, 9, 15, 36, 37, 0.0001, 0.01, 180, 1.406, 80.5])

    # ---- item 2: the plate, u = 2xy + 3x
    u_ = 2 * x * y + 3 * x
    v_ = sp.integrate(sp.diff(u_, x), y)
    v_ = v_ + sp.integrate(-sp.diff(u_, y) - sp.diff(v_, x), x)
    c.lv.claim(sp.simplify(sp.diff(u_, x) - sp.diff(v_, y)) == 0 and sp.simplify(sp.diff(u_, y) + sp.diff(v_, x)) == 0, 'item 2: u + iv meets both Cauchy-Riemann equations')
    c.lv.claim(sp.diff(u_, x, 2) + sp.diff(u_, y, 2) == 0, 'item 2: u is harmonic')

    def v_line(X, Y, Z, T, Uu):          # route 2: integrate (-u_y, u_x) along the straight path from 0 to (X, Y)
        fx = lambda s_: -(2 * (s_ * X)) * X + (2 * (s_ * Y) + 3) * Y
        return integrate.quad(fx, 0, 1, epsabs=1e-13)[0]
    c.expr(1, 1, v_, v_line, {'signs': -v_, 'no-g': y ** 2 + 3 * y, 'no-y-part': -x ** 2})
    F = 3 * z - I * z ** 2
    c.lv.claim(sp.simplify(sp.expand(F.subs(z, x + I * y)) - (u_ + I * v_)) == 0, 'item 2: 3z - iz^2 expands to u + iv')
    c.expr(1, 2, F, lambda X, Y, Z, T, Uu: complex(float(u_.subs({x: Z, y: 0})), float(v_.subs({x: Z, y: 0}))),
           {'plus': 3 * z + I * z ** 2, 'no-i': 3 * z - z ** 2, 'only-square': -I * z ** 2})
    Fn = lambda q: 3 * q - 1j * q ** 2
    d1 = sp.expand(sp.diff(F, z).subs(z, 1 + I))
    un = sp.lambdify((x, y), u_)
    vn = sp.lambdify((x, y), v_)
    nux, nvx = (un(1 + h, 1) - un(1 - h, 1)) / (2 * h), (vn(1 + h, 1) - vn(1 - h, 1)) / (2 * h)
    nuy = (un(1, 1 + h) - un(1, 1 - h)) / (2 * h)
    c.expr(1, 3, d1, complex(nux, nvx), {'i-squared': 1 - 2 * I, 'carried-plus': sp.expand((3 + 2 * I * z).subs(z, 1 + I)),
                                       'no-chain': sp.expand((3 - I * z).subs(z, 1 + I))})
    c.lv.claim(abs(cdiff(Fn, 1 + 1j) - complex(sp.N(d1))) < 1e-8, 'item 2: a difference quotient of 3z - iz^2 at 1 + i gives 5 - 2i')
    c.num(1, 4, -sp.im(d1), nuy, {'sign': -2, 'real-part': 5})
    c.num(1, 5, sp.Abs(d1), math.hypot(nux, nuy), {'no-root': 29, 'added': 7, 'carried-i-squared': abs(1 - 2j)})
    c.vocab(1, [25, 4, 29, 5 - 2j, 2 - 2j])

    # ---- item 3: logarithm branches at w = -8 + 15i
    w = -8 + 15 * I
    wn = complex(sp.N(w))
    c.num(2, 1, sp.Abs(w), abs(wn), {'added': 8 + 15, 'no-root': 289})
    c.num(2, 2, sp.N(sp.arg(w), 15), cmath.phase(wn),
          {'arctan': math.atan(15 / -8), 'reference': math.atan(15 / 8), 'inverted': math.pi - math.atan(8 / 15), 'degrees': deg(cmath.phase(wn))})
    c.lv.claim(round(float(sp.N(sp.arg(w))), 4) == 2.0608 and abs(float(sp.N(sp.arg(w))) - (math.pi - math.atan(15 / 8))) < 1e-12, 'item 3 part 2: Arg w = pi - arctan(15/8) = 2.0608')
    c.lv.claim(sp.re(w) < 0 < sp.im(w), 'item 3: w is in the second quadrant')
    sol = sp.log(17) + I * (sp.arg(w) - 2 * pi)
    nsol = cmath.log(wn) - 2j * math.pi
    c.lv.claim(abs(cmath.exp(nsol) - wn) < 1e-12 and -2 * math.pi < nsol.imag <= 0, 'item 3: e^z = w and the imaginary part is in (-2 pi, 0]')
    c.lv.claim(abs(math.exp(math.log(17)) - 17) < 1e-12 and abs(sp.N(sp.re(sol)) - math.log(17)) < 1e-12, 'item 3: Re z = ln 17')
    c.num(2, 3, sp.N(sp.im(sol), 15), nsol.imag,
          {'sign': -nsol.imag, 'principal': cmath.phase(wn), 'dropped-turn': -cmath.phase(wn)})
    c.lv.claim(round(2.0608 - 2 * math.pi, 4) == -4.2224 and round(nsol.imag, 4) == -4.2224, 'item 3 part 3: the restated Arg w and the exact one both give -4.2224')
    dl = (cmath.log(wn + 1e-6) - cmath.log(wn - 1e-6)) / 2e-6
    c.num(2, 4, 1 / sp.Abs(w), abs(dl), {'no-inverse': 17, 'log-of-modulus': sp.log(17), 'squared': R(1, 289)})
    c.lv.claim(wn.imag > 0 or wn.real < 0, 'item 3 part 4: w is off the cut (the negative real axis)')
    c.num(2, 5, sp.exp(-sp.arg(w)), abs(wn ** 1j), {'sign': math.exp(2.0608), 'carried-branch': math.exp(4.2224), 'unit': 1})
    c.lv.claim(round(abs(wn ** 1j), 4) == 0.1274 and round(math.exp(-2.0608), 4) == 0.1274, 'item 3 part 5: restated and exact Arg w both give 0.1274')
    c.vocab(2, [wn, 64, 225, 289, 17, 1.0808, 2.0608, 0.49, 2.6516, 118.07, 4.2224, 6.2832, 2.8332, 1 / 17, 1 / 289, 0.0588, 0.1274, 2 * math.pi, 15 / 8, -15 / 8, 8 / 15])

    # ---- item 4: f = z^2 + 2|z|^2 + 4z
    fz = lambda q: q ** 2 + 2 * abs(q) ** 2 + 4 * q
    zz_ = x + I * y
    fexp = sp.expand(zz_ ** 2 + 2 * (x ** 2 + y ** 2) + 4 * zz_)
    uu, vv = sp.re(fexp), sp.im(fexp)
    c.lv.claim(sp.simplify(vv - (2 * x * y + 4 * y)) == 0, 'item 4: v = 2xy + 4y as the prose says')
    c.expr(3, 1, uu, lambda X, Y, Z, T, Uu: fz(complex(X, Y)).real,
           {'no-mod': x ** 2 - y ** 2 + 4 * x, 'one-copy': 2 * x ** 2 + 4 * x, 'no-linear': 3 * x ** 2 + y ** 2})
    e1 = sp.diff(uu, x) - sp.diff(vv, y)
    e2 = sp.diff(uu, y) + sp.diff(vv, x)

    def cr(X, Y, which):
        U_ = lambda a_, b_: fz(complex(a_, b_)).real
        V_ = lambda a_, b_: fz(complex(a_, b_)).imag
        if which == 1:
            return (U_(X + h, Y) - U_(X - h, Y)) / (2 * h) - (V_(X, Y + h) - V_(X, Y - h)) / (2 * h)
        return (U_(X, Y + h) - U_(X, Y - h)) / (2 * h) + (V_(X + h, Y) - V_(X - h, Y)) / (2 * h)
    c.expr(3, 2, e1, lambda X, Y, Z, T, Uu: cr(X, Y, 1), {'no-v': sp.diff(uu, x), 'short-v': sp.diff(uu, x) - 2 * x})
    c.expr(3, 3, e2, lambda X, Y, Z, T, Uu: cr(X, Y, 2), {'minus': sp.diff(uu, y) - sp.diff(vv, x), 'no-v': sp.diff(uu, y)})
    c.lv.claim(sp.simplify(e1 - 4 * x) == 0 and sp.simplify(e2 - 4 * y) == 0, 'item 4: the two equations leave 4x and 4y')
    hh = R(1, 100) * I
    q = sp.expand(sp.simplify((hh ** 2 + 2 * hh * sp.conjugate(hh) + 4 * hh) / hh))
    c.expr(3, 4, q, (fz(0.01j) - fz(0)) / 0.01j,
           {'sign': 4 + R(1, 100) * I, 'mod-as-square': sp.expand((3 * hh ** 2 + 4 * hh) / hh), 'no-linear': sp.expand((hh ** 2 + 2 * hh * sp.conjugate(hh)) / hh)})
    quot = [(fz(1e-6 * cmath.exp(1j * a_)) - fz(0)) / (1e-6 * cmath.exp(1j * a_)) for a_ in np.linspace(0, 2 * math.pi, 9)]
    c.lv.claim(max(abs(qq - 4) for qq in quot) < 1e-5, 'item 4: the quotient at 0 tends to 4 from every direction')
    off = [(fz(0.5 + 1e-6 * cmath.exp(1j * a_)) - fz(0.5)) / (1e-6 * cmath.exp(1j * a_)) for a_ in (0, math.pi / 2)]
    c.lv.claim(abs(off[0] - off[1]) > 0.5, 'item 4: at z = 0.5 the quotient depends on direction, so no derivative there')
    c.lv.claim(sp.simplify(sp.diff(uu, x).subs({x: 0, y: 0}) + I * sp.diff(vv, x).subs({x: 0, y: 0}) - 4) == 0, 'item 4: f\'(0) = u_x + i v_x = 4 at 0')
    c.pick(3, 5, 'a')
    c.vocab(3, [0.01j, 0.0001, 0.0002, 0.0003, 0.04, 0.02, 0.01, 4 - 0.01j, 6, 4])
    return c


def trap_loop(F, centre, radius, n=4000):
    """Trapezium rule round |z - centre| = radius, anticlockwise: spectrally accurate for analytic F."""
    ts = np.linspace(0, 2 * math.pi, n, endpoint=False)
    zs_ = centre + radius * np.exp(1j * ts)
    return complex(np.sum(F(zs_) * 1j * radius * np.exp(1j * ts)) * (2 * math.pi / n))


def cquad(F, a, b):
    re_ = integrate.quad(lambda s_: F(s_).real, a, b, epsabs=1e-13, epsrel=1e-12, limit=200)[0]
    im_ = integrate.quad(lambda s_: F(s_).imag, a, b, epsabs=1e-13, epsrel=1e-12, limit=200)[0]
    return complex(re_, im_)


# ================================================================== level 3
def level3():
    c = Checker(3)
    # ---- item 1: the flower bed
    g = 3 * t + I * t ** 2
    integrand = sp.expand(sp.conjugate(g) * sp.diff(g, t))
    gn = lambda s_: 3 * s_ + 1j * s_ ** 2
    dgn = lambda s_: 3 + 2j * s_
    c.expr(0, 1, integrand, lambda X, Y, Z, T, Uu: gn(T).conjugate() * dgn(T),
           {'used-z': sp.expand(g * sp.diff(g, t)), 'i-squared': 9 * t - 2 * t ** 3 + 3 * I * t ** 2, 'no-dgamma': sp.conjugate(g)})
    curve = sp.integrate(integrand, (t, 0, 1))
    ncurve = cquad(lambda s_: gn(s_).conjugate() * dgn(s_), 0, 1)
    c.expr(0, 2, curve, ncurve, {'carried-i-squared': sp.integrate(9 * t - 2 * t ** 3 + 3 * I * t ** 2, (t, 0, 1)), 'antiderivative': sp.expand((3 + I) ** 2 / 2)})
    seg = sp.integrate(sp.expand(sp.conjugate((3 + I) * t) * (3 + I)), (t, 0, 1))
    nseg = cquad(lambda s_: ((3 + 1j) * s_).conjugate() * (3 + 1j), 0, 1)
    c.num(0, 3, seg, nseg.real, {'no-half': 10, 'used-z': sp.re(sp.expand((3 + I) ** 2 / 2))})
    loop_z2 = cquad(lambda s_: gn(s_) ** 2 * dgn(s_), 0, 1) - cquad(lambda s_: ((3 + 1j) * s_) ** 2 * (3 + 1j), 0, 1)
    c.lv.claim(abs(loop_z2) < 1e-10, 'item 1 part 4: the loop integral of z^2 is 0 numerically')
    c.pick(0, 4, 'a')
    area = sp.simplify((curve - seg) / (2 * I))
    narea = integrate.quad(lambda X: X / 3 - X ** 2 / 9, 0, 3)[0]
    c.num(0, 5, area, narea, {'no-two': 1, 'sign': -area})
    c.vocab(0, [3 + 1j, 4.5, 0.5, 1.5, 10, 2 / 4, 9 / 2, 4 + 3j])

    # ---- item 2: lighthouse flashes, Cauchy(location 0.5, scale 2.5): density c / (2x^2 - 2x + 13)
    zc = sp.Symbol('zc')
    q = 2 * zc ** 2 - 2 * zc + 13
    poles = sp.solve(q, zc)
    up = [pp for pp in poles if sp.im(pp) > 0][0]
    nup = [pp for pp in np.roots([2, -2, 13]) if pp.imag > 0][0]
    c.lv.claim(sp.simplify(up - (R(1, 2) + R(5, 2) * I)) == 0, 'item 2: the upper pole is 1/2 + 5i/2 (location 0.5, scale 2.5)')
    c.expr(1, 1, up, nup, {'lower': sp.conjugate(up), 'minus-b': -sp.conjugate(up), 'no-four': (2 + 10 * I) / 2})
    res = sp.residue(1 / q, zc, up)
    nres = 1e-7 / (2 * (nup + 1e-7) ** 2 - 2 * (nup + 1e-7) + 13)
    c.lv.claim(abs(complex(sp.N(res)) - nres) < 1e-6, 'item 2: (z - a)/q(z) near the pole tends to the residue')
    c.lv.claim(sp.simplify(sp.diff(q, zc).subs(zc, up) - 10 * I) == 0, "item 2: q'(a) = 10i")
    c.expr(1, 2, res, complex(sp.N(1 / sp.diff(q, zc).subs(zc, up))), {'no-i': R(1, 10), 'plus': I / 10, 'q-prime': 1 / (4 * up)})
    integral = sp.simplify(2 * pi * I * res)
    nint = integrate.quad(lambda X: 1 / (2 * X * X - 2 * X + 13), -np.inf, np.inf)[0]
    cc = 1 / integral
    c.num(1, 3, cc, 1 / nint, {'integral': integral, 'both-poles': 1 / (2 * integral), 'no-two': 2 / integral})
    phi = lambda uu: sp.simplify(cc * 2 * pi * I * sp.residue(sp.exp(I * uu * zc) / q, zc, up))
    phi1 = phi(1)
    cn = float(sp.N(cc))
    c.lv.claim(sp.simplify(phi1 - sp.exp(I / 2 - R(5, 2))) == 0, 'item 2: phi(1) = e^{i/2 - 5/2} by residues')
    # route 2 for phi: Y = X - 0.5 has density (c/2)/(y^2 + 6.25), symmetric, so E[e^{iuY}] = 2 int_0^inf (c/2) cos(uy)/(y^2 + 6.25) dy
    ny = lambda uu: 2 * integrate.quad(lambda Y: (cn / 2) / (Y * Y + 6.25), 0, np.inf, weight='cos', wvar=uu)[0]
    c.num(1, 4, sp.Abs(phi1), abs(ny(1.0)), {'sign': sp.exp(R(5, 2)), 'no-c': sp.exp(-R(5, 2)) * integral, 'standard': sp.exp(-1)})
    phiM = sp.simplify(phi(R(1, 2)) ** 2)
    rng = np.random.default_rng(11)
    xs = 0.5 + 2.5 * np.tan(math.pi * (rng.random((2, 400000)) - 0.5))
    mc = abs(np.mean(np.exp(1j * xs.mean(axis=0))))
    c.lv.claim(abs(mc - math.exp(-2.5)) < 0.004, f'item 2: Monte Carlo |E e^(iM)| for the mean of two flashes is {mc:.4f}, near e^-2.5')
    c.num(1, 5, sp.Abs(phiM), abs(ny(0.5)) ** 2, {'no-half': sp.exp(-5), 'one-factor': sp.exp(-R(5, 4))})
    c.lv.claim(round(float(sp.N(sp.Abs(phi1))), 4) == 0.0821, 'item 2: 0.0821 is |phi(1)| and |phi_M(1)|')
    c.vocab(1, [0.5 + 2.5j, 0.5, 2.5, 4, 104, 100, 10, 2, 13, 1, 5, 52, 6.25, 0.1, 5 / math.pi, math.pi / 5, 2 * math.pi / 5, math.pi / 10, 1.25, 0.25,
                12.1825, 0.0516, 0.3679, 0.0067, 0.2865, 0.0821, 1.592, 0.628, 0.796, 3.183, 1 / 52, 5 / 52, 1.5,
                210, 1004, 1044])   # token reader joins fractions when it drops braces: sqrt{-100}}{4}, sqrt{4 - 104}}{4}

    # ---- item 3: share moments from phi at complex points
    S0, r, sg, T = 64, R(5, 100), R(25, 100), R(8, 10)
    drift = (r - sg ** 2 / 2) * T
    s2 = sg ** 2 * T
    mu = sp.log(S0) + drift
    c.num(2, 1, drift, (0.05 - 0.25 ** 2 / 2) * 0.8, {'sign': -drift, 'no-half': (r - sg ** 2) * T, 'no-sigma': r * T})
    phi_s = lambda uu: sp.exp(I * mu * uu - s2 * uu ** 2 / 2)
    ES = sp.simplify(phi_s(-I))
    dens = lambda Lx: math.exp(-(Lx - float(mu)) ** 2 / (2 * float(s2))) / math.sqrt(2 * math.pi * float(s2))
    nES = integrate.quad(lambda Lx: math.exp(Lx) * dens(Lx), float(mu) - 12, float(mu) + 12, epsabs=1e-12, epsrel=1e-13)[0]
    c.lv.claim(abs(float(sp.N(ES)) - nES) < 1e-6 and round(nES, 3) == 66.612, 'item 3: E[S_T] = 66.612 by both routes (it is handed to part 4)')
    nphi3 = abs(integrate.quad(lambda Lx: math.cos(3 * Lx) * dens(Lx), float(mu) - 12, float(mu) + 12, epsabs=1e-13, limit=400)[0]
                + 1j * integrate.quad(lambda Lx: math.sin(3 * Lx) * dens(Lx), float(mu) - 12, float(mu) + 12, epsabs=1e-13, limit=400)[0])
    c.lv.claim(abs(abs(complex(sp.N(phi_s(3)))) - float(sp.N(sp.exp(-s2 * 9 / 2)))) < 1e-12, 'item 3 part 2: |phi(3)| from the closed form equals e^{-0.225}')
    c.num(2, 2, sp.exp(-s2 * 9 / 2), nphi3, {'no-square': sp.exp(-s2 * 3 / 2), 'no-half': sp.exp(-s2 * 9), 'sign': sp.exp(s2 * 9 / 2)})
    c.lv.claim(sp.simplify(sp.exp(-r * T) * ES - S0) == 0, 'item 3: e^{-rT} E[S_T] = S_0')
    ES2 = sp.simplify(phi_s(-2 * I))
    nES2 = integrate.quad(lambda Lx: math.exp(2 * Lx) * dens(Lx), float(mu) - 12, float(mu) + 12, epsabs=1e-10, epsrel=1e-13)[0]
    c.num(2, 3, ES2, nES2, {'mean-squared': ES ** 2, 'minus': sp.exp(2 * mu - 2 * s2)})
    E1, E2 = sp.Float('66.612'), sp.Float('4664.6')
    c.lv.claim(round(float(sp.N(ES)), 3) == 66.612 and round(float(sp.N(ES2)), 1) == 4664.6, 'item 3: the restated moments are the computed ones rounded')
    c.num(2, 4, sp.sqrt(E2 - E1 ** 2), math.sqrt(4664.6 - 66.612 ** 2),
          {'variance': E2 - E1 ** 2, 'not-squared': sp.sqrt(E2 - E1), 'log-sd': 64 * 0.25 * math.sqrt(0.8), 'own-rounding': math.sqrt(4665 - 66.61 ** 2)})
    c.lv.claim(abs(float(sp.N(ES2 - ES ** 2)) - 227.47) <= 0.08 and abs(float(E2 - E1 ** 2) - 227.47) <= 0.08 and round(float(sp.N(ES2 - ES ** 2)), 1) == 227.5, 'item 3 part 4: the variance band 227.47 +- 0.08 takes the variance from rounded and from unrounded moments')
    c.lv.claim(abs(float(E2 - E1 ** 2) - 227.44) < 0.005 and abs(math.sqrt(4665 - 66.61 ** 2) - 15.1) < 0.005, 'item 3 part 4: 227.44 from the handed moments; own-rounding 15.10 from 66.61 and 4665')
    c.lv.claim(round(float(sp.N(sp.sqrt(ES2 - ES ** 2))), 2) == 15.08, 'item 3: unrounded moments give the same 15.08')
    psi0 = sp.exp(-r * T) * E2 / 2
    from scipy.stats import norm
    def call(K):
        if K <= 0:
            return 64.0
        d1 = (math.log(64 / K) + (0.05 + 0.25 ** 2 / 2) * 0.8) / (0.25 * math.sqrt(0.8))
        return 64 * norm.cdf(d1) - K * math.exp(-0.04) * norm.cdf(d1 - 0.25 * math.sqrt(0.8))
    area_c = integrate.quad(call, 0, 64, limit=200)[0] + integrate.quad(call, 64, 2000, limit=400)[0]   # int e^k C dk = int C(K) dK
    c.lv.claim(abs(area_c - float(sp.N(sp.exp(-r * T) * ES2 / 2))) < 1e-5, f'item 3: the area under Black-Scholes call prices, {area_c:.4f}, is e^(-rT) E[S^2]/2')
    c.num(2, 5, psi0, math.exp(-0.04) * 4664.6 / 2, {'no-discount': E2 / 2, 'no-two': sp.exp(-r * T) * E2, 'wrong-sign': sp.exp(r * T) * E2 / 2})
    c.lv.claim(round(area_c) == 2241, 'item 3: the unrounded second moment gives the same 2241')
    c.vocab(2, [64, 0.05, 0.25, 0.8, 0.0625, 0.03125, 0.01875, 0.015, 0.025, 0.04, 0.03, 0.1, 0.13, 0.08, 4096, 66.612, 4664.6, 4437.2, 227.44, 227.4, 25, 30, 0.5, 2, 1 / 2,
                 4664.62, 0.9277, 0.6376, 1.2523, 0.7985, 0.225, 0.45, 0.075, 9, 66.61, 4665, 15.1, 15.08])   # 4664.62: the token reader joins 4664.6}{2} when it drops braces

    # ---- item 4: print stages
    phX = 1 / (1 - 2 * I * u) ** 2
    c.expr(3, 1, phX, lambda X, Y, Z, T_, Uu: (1 / (1 - 2j * Uu)) * (1 / (1 - 2j * Uu)),
           {'added': 2 / (1 - 2 * I * u), 'doubled-u': 1 / (1 - 4 * I * u)})
    zp = sp.solve(1 - 2 * I * zc, zc)[0]
    c.expr(3, 2, zp, np.roots([-2j, 1])[0], {'sign': -zp, 'real': R(1, 2)})
    d1_ = sp.diff(1 / (1 - 2 * I * zc) ** 2, zc).subs(zc, 0)
    d2_ = sp.diff(1 / (1 - 2 * I * zc) ** 2, zc, 2).subs(zc, 0)
    Fx = lambda w_: 1 / (1 - 2j * w_) ** 2
    I2 = trap_loop(lambda w_: Fx(w_) / w_ ** 2, 0, 0.25)
    I3 = trap_loop(lambda w_: Fx(w_) / w_ ** 3, 0, 0.25)
    c.lv.claim(abs(I2.imag) < 1e-10 and abs(I3.real) < 1e-10, 'item 4: the z^2 loop integral is real and the z^3 one imaginary')
    c.num(3, 3, sp.simplify(2 * pi * I * d1_), I2.real, {'sign': 8 * pi, 'one-stage': 2 * pi * I * sp.diff(1 / (1 - 2 * I * zc), zc).subs(zc, 0)})
    c.lv.claim(sp.simplify(pi * I * d2_ + 24 * pi * I) == 0 and abs(I3 - (-24j * math.pi)) < 1e-9, 'item 4: the z^3 loop integral is -24 pi i (both routes)')
    c.num(3, 4, sp.simplify(d1_ / I), (I2 / (2j * math.pi) / 1j).real, {'sign': -4, 'one-stage': 2})
    EX2 = -d2_
    c.num(3, 5, EX2 - (d1_ / I) ** 2, (-(I3 / (2j * math.pi)) * 2).real - 16, {'no-factorial': -d2_ / 2 - 16, 'second-moment': EX2, 'mean-not-squared': EX2 - 4})
    c.lv.claim(abs(np.var(rng.exponential(2, (2, 400000)).sum(axis=0)) - 8) < 0.15, 'item 4: Monte Carlo variance of two exponential stages of mean 2 is near 8')
    c.vocab(3, [0.25, 0.5, 24, 16, 12, 8, 25.13, 2 * math.pi])
    return c


if __name__ == '__main__':
    done = []
    for f in (level1, level2, level3):
        ch = f()
        ch.finish()
        done.append(ch)
    bad = sum(1 for ch in done for r in ch.lv.results if not r[0])
    total = sum(len(ch.lv.results) for ch in done)
    print(f'complex problem sets: {total - bad} of {total} checks passed')
    sys.exit(1 if bad else 0)
