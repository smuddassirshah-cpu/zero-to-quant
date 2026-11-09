"""Recompute every Fluency family of the equations course (docs/briefs/fluency.md check 1).

Run from anywhere with a Python that has sympy:
    <scratchpad>/venv/bin/python docs/reports/fluency-equations-numbers.py [--n 200]
For every family it reads `node tools/fluency-sample.mjs --set equations/<set> --family <id> --n N --json`,
derives the key again from the drawn `vars` alone (never from the printed answer), and checks:
  - the prompt's maths is the expression or equation the vars describe;
  - the engine's answer equals the key derived here (exactly, with sympy);
  - every `wrong` equals the slip derived here and differs from the key;
  - for a solve family, the key really satisfies the prompt's equation.
Exits 1 on any failure.
"""
import json
import os
import re
import string
import subprocess
import sys
from fractions import Fraction

import sympy as sp
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
                                        implicit_multiplication_application, split_symbols, convert_xor)

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, '..', '..', 'app')
N = int(sys.argv[sys.argv.index('--n') + 1]) if '--n' in sys.argv else 200
LOCAL = {c: sp.Symbol(c) for c in string.ascii_letters}
TRANS = standard_transformations + (split_symbols, implicit_multiplication_application, convert_xor)
R = sp.Rational
failures = []
checked = 0


def fail(msg):
    failures.append(msg)


# ---------- LaTeX to sympy (the small subset the sets use) ----------

def _group(s, i):
    """s[i] == '{': return (inner, index after the closing brace)."""
    assert s[i] == '{', s
    depth, j = 0, i
    while True:
        if s[j] == '{':
            depth += 1
        elif s[j] == '}':
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1


def tex2py(s):
    s = s.replace('\\dfrac', '\\frac').replace('\\tfrac', '\\frac').replace('\u2212', '-')
    s = s.replace('\\left', '').replace('\\right', '').replace('\\times', '*').replace('\\cdot', '*')
    out, i = '', 0
    while i < len(s):
        if s.startswith('\\frac', i):
            a, i = _group(s, i + 5)
            b, i = _group(s, i)
            out += '((' + tex2py(a) + ')/(' + tex2py(b) + '))'
        elif s[i] == '{':
            a, i = _group(s, i)
            out += '(' + tex2py(a) + ')'
        else:
            out += s[i]
            i += 1
    return out


def P(tex):
    """Parse an expression, an equation (a single '='), or a vector '(a, b)'."""
    t = tex2py(tex).replace(' ', '')
    if '=' in t:
        lhs, rhs = t.split('=')
        return sp.Eq(P(lhs), P(rhs), evaluate=False)
    m = re.fullmatch(r'\((.*),(.*)\)', t)
    if m and m.group(1).count('(') == m.group(1).count(')'):
        return (P(m.group(1)), P(m.group(2)))
    return parse_expr(t, local_dict=LOCAL, transformations=TRANS)


def same(a, b):
    if isinstance(a, tuple) or isinstance(b, tuple):
        return isinstance(a, tuple) and isinstance(b, tuple) and len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    if isinstance(a, sp.Equality) or isinstance(b, sp.Equality):
        if not (isinstance(a, sp.Equality) and isinstance(b, sp.Equality)):
            return False
        da, db = sp.expand(a.lhs - a.rhs), sp.expand(b.lhs - b.rhs)
        return sp.simplify(da - db) == 0 or sp.simplify(da + db) == 0
    return sp.simplify(sp.sympify(a) - sp.sympify(b)) == 0


def num(s):
    return sp.nsimplify(sp.sympify(str(s)), rational=True)


def maths(prompt):
    return re.findall(r'\$([^$]+)\$', prompt)


def S(v):
    return LOCAL[v]


# ---------- the families ----------
# Each returns (prompt, key, {wrong id: value}, check): prompt is a list of (index of the $...$ block, the expression or
# equation it must show), key is recomputed from the vars, and check is None or (equations, unknowns) the key must solve.

def solve1(eq, v):
    sol = sp.solve(eq, v, dict=True)
    assert len(sol) == 1, (eq, sol)
    return sol[0][v]


def collect_one_letter(V):
    a, b, c, d, v = V['a'], V['b'], V['c'], V['d'], S(V['v'])
    prompt = sp.Add(a * v, b, c * v, d, evaluate=False)
    key = (a + c) * v + (b + d)
    return [(0, prompt)], key, {'flipped-sign': (a - c) * v + (b + d), 'combined-all': (a + b + c + d) * v}, None


def expand_one_bracket(V):
    a, p, b, v = V['a'], V['p'], V['b'], S(V['v'])
    prompt = sp.Mul(a, p * v + b, evaluate=False)
    return [(0, prompt)], sp.expand(a * (p * v + b)), {'first-term-only': a * p * v + b, 'sign-slip': a * p * v - a * b}, None


def expand_two_and_collect(V):
    a, b, c, d, v = V['a'], V['b'], V['c'], V['d'], S(V['v'])
    prompt = sp.Add(sp.Mul(a, v + b, evaluate=False), sp.Mul(c, v + d, evaluate=False), evaluate=False)
    key = sp.expand(a * (v + b) + c * (v + d))
    return [(0, prompt)], key, {'second-constant-kept': (a + c) * v + a * b + d, 'second-sign-slip': (a + c) * v + a * b - c * d}, None


def common_factor(V):
    h, p, q, v = V['h'], V['p'], V['q'], S(V['v'])
    if sp.gcd(h * p, h * q) != h:
        fail(f'common-factor: highest common factor of {h*p} and {h*q} is not {h}')
    return [(0, h * p * v + h * q)], h * (p * v + q), {'constant-not-divided': h * (p * v + h * q), 'letter-taken-out': h * v * (p + q)}, None


def multiply_then_add(V):
    a, x0, b, v = V['a'], V['x0'], V['b'], S(V['v'])
    c = a * x0 + b
    eq = sp.Eq(a * v + b, c)
    return [(0, eq)], solve1(eq, v), {'divided-first': solve1(sp.Eq(v + b, R(c, a)), v), 'sign-of-number': solve1(sp.Eq(a * v, c + b), v)}, ([eq], [v])


def divide_then_add(V):
    a, m, b, v = V['a'], V['m'], V['b'], S(V['v'])
    c = m + b
    eq = sp.Eq(v / a + b, c)
    return [(0, eq)], solve1(eq, v), {'multiplied-first': solve1(sp.Eq(v + b, a * c), v), 'divided-instead': solve1(sp.Eq(v * a, c - b), v)}, ([eq], [v])


def bracket_one_side(V):
    c, k, b, x0, v = V['c'], V['k'], V['b'], V['x0'], S(V['v'])
    a = c + k
    d = a * (x0 + b) - c * x0
    eq = sp.Eq(sp.Mul(a, v + b, evaluate=False), c * v + d)
    return [(0, eq)], solve1(eq, v), {'bracket-first-term': solve1(sp.Eq(a * v + b, c * v + d), v),
                                      'added-unknown': solve1(sp.Eq(a * v + a * b + c * v, d), v)}, ([eq], [v])


def brackets_both_sides(V):
    a, k, m, x0, v = V['a'], V['k'], V['m'], V['x0'], S(V['v'])
    c = a + k
    b, d = c * m - x0, a * m - x0
    eq = sp.Eq(sp.Mul(a, v + b, evaluate=False), sp.Mul(c, v + d, evaluate=False))
    return [(0, eq)], solve1(eq, v), {'bracket-first-term': solve1(sp.Eq(a * v + b, c * v + d), v),
                                      'number-sign-kept': solve1(sp.Eq(a * b + c * d, (c - a) * v), v)}, ([eq], [v])


def two_fractions_sum(V):
    p, q, k, v = V['p'], V['q'], V['k'], S(V['v'])
    L = sp.ilcm(p, q)
    r = R(k * L, p) + R(k * L, q)
    eq = sp.Eq(v / p + v / q, r)
    return [(0, eq)], solve1(eq, v), {'right-side-missed': solve1(sp.Eq((L // p) * v + (L // q) * v, r), v),
                                      'added-bottoms': solve1(sp.Eq(v / (p + q), r), v)}, ([eq], [v])


def whole_tops(V):
    p, k, m, x0, v = V['p'], V['k'], V['m'], V['x0'], S(V['v'])
    q = p + k
    b, d = p * m - x0, q * m - x0
    eq = sp.Eq((v + b) / p, (v + d) / q)
    return [(0, eq)], solve1(eq, v), {'lost-bracket': solve1(sp.Eq(q * v + b, p * v + d), v),
                                      'own-bottom': solve1(sp.Eq(p * (v + b), q * (v + d)), v)}, ([eq], [v])


def subject_from_linear(V):
    a, b, u, v = V['a'], V['b'], S(V['u']), S(V['v'])
    eq = sp.Eq(u, a * v + b)
    return [(0, v), (1, eq)], solve1(eq, v), {'divided-one-term': u / a - b, 'sign-kept': (u + b) / a}, ([eq], [v])


def subject_from_product(V):
    a, u, v, w = V['a'], S(V['u']), S(V['v']), S(V['w'])
    eq = sp.Eq(u, a * v * w)
    return [(0, w), (1, eq)], solve1(eq, w), {'upside-down': a * v / u, 'number-left': u / v}, ([eq], [w])


def subject_from_bottom(V):
    a, u, v, w = V['a'], S(V['u']), S(V['v']), S(V['w'])
    eq = sp.Eq(u, a * v / w)
    return [(0, w), (1, eq)], solve1(eq, w), {'upside-down': u / (a * v), 'multiplied': a * u * v}, ([eq], [w])


def substitute_linear_pair(V):
    x0, m, c, a, b = V['x0'], V['m'], V['c'], V['a'], V['b']
    x, y = S('x'), S('y')
    e = a * x0 + b * (m * x0 + c)
    e1, e2 = sp.Eq(y, m * x + c), sp.Eq(a * x + b * y, e)
    sol = sp.solve([e1, e2], [x, y], dict=True)
    assert len(sol) == 1
    key = (sol[0][x], sol[0][y])
    xs = solve1(sp.Eq(a * x + b * m * x + c, e), x)     # the slip: b multiplies m x but not c
    return [(0, e1), (1, e2)], key, {'bracket-dropped': (xs, m * xs + c), 'swapped-order': (key[1], key[0])}, ([e1, e2], [x, y])


FAMILIES = {
    'fluency-l2-like-terms': {'collect-one-letter': collect_one_letter},
    'fluency-l3-opening-brackets': {'expand-one-bracket': expand_one_bracket, 'expand-two-and-collect': expand_two_and_collect},
    'fluency-l4-putting-brackets-back': {'common-factor': common_factor},
    'fluency-l6-undoing-in-reverse': {'multiply-then-add': multiply_then_add, 'divide-then-add': divide_then_add},
    'fluency-l7-unknowns-both-sides': {'bracket-one-side': bracket_one_side, 'brackets-both-sides': brackets_both_sides},
    'fluency-l8-clearing-fractions': {'two-fractions-sum': two_fractions_sum, 'whole-tops': whole_tops},
    'fluency-l13-changing-the-subject': {'subject-from-linear': subject_from_linear, 'subject-from-product': subject_from_product,
                                         'subject-from-bottom': subject_from_bottom},
    # 'fluency-l15-swapping-in': {'substitute-linear-pair': substitute_linear_pair},   # skipped: see fluency-equations.md
}

# The shape the key must be written in, checked on the engine's key text.
SHAPES = {
    'common-factor': re.compile(r'^\d+\((\d*)?[a-z][+-]\d+\)$'),
}


def run_family(set_id, fam, fn):
    global checked
    cmd = ['node', 'tools/fluency-sample.mjs', '--set', f'equations/{set_id}', '--family', fam, '--n', str(N), '--json']
    out = subprocess.run(cmd, cwd=APP, capture_output=True, text=True)
    if out.returncode != 0:
        fail(f'{set_id}/{fam}: sampler failed: {out.stderr[-300:]}')
        return
    items = json.loads(out.stdout)['items']
    if len(items) < N:
        fail(f'{set_id}/{fam}: only {len(items)} draws')
    for it in items:
        tag = f"{set_id}/{fam} seed {it['seed']}"
        prompt, key, wrongs, eq = fn(it['vars'])
        shown = maths(it['prompt'])
        for idx, want in prompt:
            if len(shown) <= idx or not same(P(shown[idx]), want):
                fail(f'{tag}: prompt block {idx} {shown[idx:idx + 1]} is not {want}')
        if eq is not None:
            sub = dict(zip(eq[1], key if isinstance(key, tuple) else (key,)))
            for e in eq[0]:
                if sp.simplify((e.lhs - e.rhs).subs(sub)) != 0:
                    fail(f'{tag}: key {key} does not satisfy {e}')
        if fam in SHAPES and not SHAPES[fam].match(it['answer']):
            fail(f"{tag}: key text {it['answer']} is not in the asked shape")
        got = num(it['answer']) if it['kind'] == 'numeric' else P(it['answer'])
        if not same(got, key):
            fail(f"{tag}: engine answer {it['answer']} but recomputed {key}")
        ids = {w['id'] for w in it['wrong']}
        if ids != set(wrongs):
            fail(f'{tag}: wrong ids {ids} != {set(wrongs)}')
        for w in it['wrong']:
            wv = num(w['value']) if 'value' in w else P(w['tex'])
            if w['id'] in wrongs and not same(wv, wrongs[w['id']]):
                fail(f"{tag}: wrong {w['id']} {w.get('tex', w.get('value'))} but recomputed {wrongs[w['id']]}")
            if same(wv, key):
                fail(f"{tag}: wrong {w['id']} equals the key")
            if it['kind'] == 'numeric':
                tol = (w.get('tol') or {}).get('abs', 1e-9)
                ktol = (it.get('tol') or {}).get('abs', 0)
                if abs(float(wv) - float(key)) <= max(tol, ktol):
                    fail(f"{tag}: wrong {w['id']} lies within tolerance of the key")
        checked += 1


def main():
    only = [a for a in sys.argv[1:] if a.startswith('fluency-')]
    for set_id, fams in FAMILIES.items():
        if only and set_id not in only:
            continue
        doc = json.load(open(os.path.join(APP, 'content', 'courses', 'equations', set_id + '.json')))
        listed = {f['id'] for f in doc['families']}
        if listed != set(fams):
            fail(f'{set_id}: families in file {sorted(listed)} but recomputed {sorted(fams)}')
        for fam, fn in fams.items():
            run_family(set_id, fam, fn)
    print(f'fluency-equations-numbers: {checked} draws checked, {len(failures)} failures')
    for f in failures[:30]:
        print('  FAIL', f)
    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    main()
