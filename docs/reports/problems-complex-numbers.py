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
    c.expr(1, 3, sp.arg(w), cmath.phase(nr), {'inverted': sp.atan(sp.re(w) / sp.im(w)), 'carried-minus-b': sp.arg(-sp.conjugate(w))})
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
    c.expr(2, 2, sp.arg(cc), cmath.phase(cn), {'arctan': sp.atan(sp.im(cc) / sp.re(cc)), 'reference': pi / 3, 'swapped': pi - sp.atan(-sp.re(cc) / sp.im(cc))})
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
    c.num(3, 1, sp.im(B), nB.imag, {'swapped': 6, 'unscaled': sp.sin(2 * pi / 3), 'degrees': 12 * math.sin(math.radians(2 * math.pi / 3))})
    c.expr(3, 2, C, nC, {'sin-sign': sp.conjugate(C), 'swapped': -R(7, 2) * sqrt(3) - R(7, 2) * I})
    N = sp.expand(A + B + C)
    nN = 12 + nB + nC
    c.expr(3, 3, N, nN, {'no-first': N - 12, 'carried-sin-sign': sp.expand(A + B + sp.conjugate(C))})
    c.lv.claim(sp.simplify(sp.expand_complex(N + 5 * om ** 2)) == 0, 'item 4: N = -5 omega^2 (1 + omega + omega^2 = 0)')
    c.num(3, 4, sp.Abs(N), abs(nN), {'added': sp.re(N) + sp.im(N), 'squared': 25, 'carried-sin-sign': sp.Abs(sp.expand(A + B + sp.conjugate(C)))})
    c.num(3, 5, sp.arg(N) * 180 / pi, deg(cmath.phase(nN)), {'inverted': 30, 'omega-squared': 240, 'radians': pi / 3})
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
    c.expr(0, 1, sp.expand(f(z0)), f(n0), {'square-parts': R(25, 4) + 9 * I - 4 * z0, 'i-squared': R(25, 4) + 9 + 15 * I - 4 * z0})
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

    # ---- item 3: logarithm branches at w = -4 sqrt3 + 4i
    w = -4 * sqrt(3) + 4 * I
    wn = complex(sp.N(w))
    c.num(2, 1, sp.Abs(w), abs(wn), {'added': 4 * sqrt(3) + 4, 'no-root': 64})
    c.expr(2, 2, sp.arg(w), cmath.phase(wn), {'arctan': sp.atan(sp.im(w) / sp.re(w)), 'reference': pi / 6, 'inverted': pi - sp.atan(-sp.re(w) / sp.im(w))})
    sol = sp.log(8) + I * (sp.arg(w) - 2 * pi)
    nsol = cmath.log(wn) - 2j * math.pi
    c.lv.claim(abs(cmath.exp(nsol) - wn) < 1e-12 and -2 * math.pi < nsol.imag <= 0, 'item 3: e^z = w and the imaginary part is in (-2 pi, 0]')
    c.expr(2, 3, sol, nsol, {'principal': sp.log(8) + 5 * pi * I / 6, 'no-log': 8 - 7 * pi * I / 6, 'dropped-turn': sp.log(8) - 5 * pi * I / 6})
    dl = (cmath.log(wn + 1e-5) - cmath.log(wn - 1e-5)) / 2e-5
    c.num(2, 4, 1 / sp.Abs(w), abs(dl), {'no-inverse': 8, 'log-of-modulus': sp.log(8), 'squared': R(1, 64)})
    c.num(2, 5, sp.exp(-5 * pi / 6), abs(wn ** 1j), {'sign': sp.exp(5 * pi / 6), 'carried-branch': sp.exp(7 * pi / 6), 'unit': 1})
    c.vocab(2, [wn, 48, 16, 64, 4 * 3 ** 0.5, 5 * math.pi / 6, 1 / 64, 2 * math.pi])

    # ---- item 4: f = |z|^2 + z
    uu = x ** 2 + y ** 2 + x
    vv = y
    fz = lambda q: abs(q) ** 2 + q
    c.expr(3, 1, uu, lambda X, Y, Z, T, Uu: fz(complex(X, Y)).real, {'square': x ** 2 - y ** 2 + x, 'no-x': x ** 2 + y ** 2})
    e1 = sp.diff(uu, x) - sp.diff(vv, y)
    e2 = sp.diff(uu, y) + sp.diff(vv, x)
    def cr(X, Y, which):
        U_ = lambda a, b: fz(complex(a, b)).real
        V_ = lambda a, b: fz(complex(a, b)).imag
        if which == 1:
            return (U_(X + h, Y) - U_(X - h, Y)) / (2 * h) - (V_(X, Y + h) - V_(X, Y - h)) / (2 * h)
        return (U_(X, Y + h) - U_(X, Y - h)) / (2 * h) + (V_(X + h, Y) - V_(X - h, Y)) / (2 * h)
    c.expr(3, 2, e1, lambda X, Y, Z, T, Uu: cr(X, Y, 1), {'no-v': 2 * x + 1, 'swapped': 2 * y - 1})
    c.expr(3, 3, e2, lambda X, Y, Z, T, Uu: cr(X, Y, 2), {'carried-square': -2 * y, 'no-u': 0})
    hh = R(1, 100) * I
    q = sp.expand(sp.simplify(((hh * sp.conjugate(hh)) + hh) / hh))
    c.expr(3, 4, q, (fz(0.01j) - fz(0)) / 0.01j, {'sign': 1 + R(1, 100) * I, 'no-modulus': 1})
    quot = [(fz(1e-6 * cmath.exp(1j * a)) - fz(0)) / (1e-6 * cmath.exp(1j * a)) for a in np.linspace(0, 2 * math.pi, 9)]
    c.lv.claim(max(abs(qq - 1) for qq in quot) < 1e-5, 'item 4: the quotient at 0 tends to 1 from every direction')
    off = [(fz(0.5 + 1e-6 * cmath.exp(1j * a)) - fz(0.5)) / (1e-6 * cmath.exp(1j * a)) for a in (0, math.pi / 2)]
    c.lv.claim(abs(off[0] - off[1]) > 0.5, 'item 4: at z = 0.5 the quotient depends on direction, so no derivative there')
    c.pick(3, 5, 'a')
    c.vocab(3, [0.01j, 0.0001, 0.01])
    return c


if __name__ == '__main__':
    done = []
    for f in (level1, level2):
        ch = f()
        ch.finish()
        done.append(ch)
    bad = sum(1 for ch in done for r in ch.lv.results if not r[0])
    total = sum(len(ch.lv.results) for ch in done)
    print(f'complex problem sets: {total - bad} of {total} checks passed')
    sys.exit(1 if bad else 0)
