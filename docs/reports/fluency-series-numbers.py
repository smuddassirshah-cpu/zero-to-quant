"""Recompute every Fluency family of the series course from the drawn variables alone (docs/briefs/fluency.md check 1).

Run from anywhere with a Python that has sympy:
    <scratchpad>/venv/bin/python docs/reports/fluency-series-numbers.py [--n 200]
For each family it reads `node tools/fluency-sample.mjs --set series/<set> --family <id> --n N --json`, derives the key
again from `vars` only (never from the printed answer) with sympy (sums by `summation`, coefficients by `expand`),
checks it equals the engine's resolved answer, and checks each `wrong` equals the slip recomputed from the vars and
differs from the key (numeric: outside the key's tolerance). It also scans the drawn text for `1x`, `+-`, `--`,
`x^{1}` and `+0`. Exit 0 when all agree.
"""
import json
import os
import re
import subprocess
import sys

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

APP = os.environ.get('FLUENCY_APP') or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app')
N = int(sys.argv[sys.argv.index('--n') + 1]) if '--n' in sys.argv else int(os.environ.get('FLUENCY_N', '60'))
n, x, k = sp.symbols('n x k')
R = sp.Rational
fails = []
checked = 0
BAD = [r'(?<![\d.])1[a-z]', r'\+-', r'--', r'\^\{1\}', r'\+0(?![.\d])', r'(?<![\d.])0[a-z]', r'\+\s*-']


def tex2py(s):
    s = s.replace('\\times', '*').replace('\\left', '').replace('\\right', '')
    s = re.sub(r'\\d?frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', s)
    s = s.replace('^', '**').replace('{', '(').replace('}', ')')
    return s


def parse(s):
    return parse_expr(tex2py(s), local_dict={'n': n, 'x': x},
                      transformations=standard_transformations + (implicit_multiplication_application,))


def rat(v):
    return sp.nsimplify(v, rational=True) if isinstance(v, float) else sp.Integer(v) if isinstance(v, int) else sp.Rational(str(v))


def sample(set_id, fam):
    out = subprocess.run(['node', 'tools/fluency-sample.mjs', '--set', 'series/' + set_id, '--family', fam,
                          '--n', str(N), '--json'], cwd=APP, capture_output=True, text=True, check=True).stdout
    return json.loads(out)['items']


def scan(label, texts):
    for t in texts:
        plain = re.sub(r"\\[a-zA-Z]+", " ", str(t))
        for pat in BAD:
            if re.search(pat, plain):
                fails.append('%s: pattern %s in %r' % (label, pat, t))


def check(set_id, fam, derive):
    """derive(V) -> (key, {wrong_id: value}); expression keys are sympy expressions in n, numeric keys Rationals."""
    global checked
    for it in sample(set_id, fam):
        V = {kk: (rat(v) if isinstance(v, (int, float)) else v) for kk, v in it['vars'].items()}
        key, wrongs = derive(V)
        label = '%s/%s seed %s' % (set_id, fam, it['seed'])
        scan(label, [it['prompt'], it['answer']] + it['solution'] + [w['line'] for w in it['wrong']]
             + [w.get('tex', '') for w in it['wrong']])
        if it['kind'] == 'numeric':
            got = rat(it['answer']) if not isinstance(it['answer'], str) else sp.Rational(it['answer'])
            tol = (it.get('tol') or {}).get('abs', 0)
            ok = abs(float(got - key)) <= max(tol, 1e-9)
        else:
            got = parse(it['answer'])
            ok = sp.simplify(got - key) == 0
        checked += 1
        if not ok:
            fails.append('%s: key %s, engine %s' % (label, key, it['answer']))
        if set(w['id'] for w in it['wrong']) != set(wrongs):
            fails.append('%s: wrong ids %s' % (label, [w['id'] for w in it['wrong']]))
        for w in it['wrong']:
            want = wrongs.get(w['id'])
            if it['kind'] == 'numeric':
                wv = sp.Rational(str(w['value']))
                okw = want is not None and abs(float(wv - want)) <= 1e-6 and abs(float(wv - key)) > tol
            else:
                wv = parse(w['tex'])
                okw = want is not None and sp.simplify(wv - want) == 0 and sp.simplify(wv - key) != 0
            checked += 1
            if not okw:
                fails.append('%s: wrong %s, expected %s, engine %s' % (label, w['id'], want, w.get('tex', w.get('value'))))
        vals = [w['value'] if 'value' in w else w['tex'] for w in it['wrong']]
        if len(set(map(str, vals))) != len(vals):
            fails.append('%s: two wrongs coincide %s' % (label, vals))


def arith_term(a, d, m):
    """u_m by summing m - 1 steps of d onto a (not the closed formula)."""
    return a + sp.summation(d, (k, 1, m - 1))


# ---- fluency-l2-any-term ----
def l2_term(V):
    a, d, kk = V['a'], V['d'], V['k']
    seq = [a + i * d for i in range(int(kk))]
    return seq[-1], {'k-steps': seq[-1] + d, 'difference-sign': a - (kk - 1) * d}


def l2_formula(V):
    a, d = V['a'], V['d']
    u = sp.expand(a + (n - 1) * d)
    assert all(u.subs(n, i) == a + (i - 1) * d for i in range(1, 6))
    return u, {'n-steps': a + d * n, 'first-term-times-n': a * n + d}


def l2_difference(V):
    p, g, d, a = V['p'], V['g'], V['d'], V['a']
    up, uq = arith_term(a, d, p), arith_term(a, d, p + g)
    dd = sp.Rational(uq - up, g)
    return dd, {'whole-rise': uq - up, 'counted-terms': sp.Rational(uq - up, g + 1)}


def l2_which(V):
    a, d, m = V['a'], V['d'], V['m']
    u = arith_term(a, d, m)
    sol = sp.solve(sp.Eq(a + (n - 1) * d, u), n)
    assert len(sol) == 1
    return sol[0], {'steps-not-position': sol[0] - 1, 'one-too-many': sol[0] + 1}


# ---- fluency-l3-multiplying-each-time ----
def l3_first_term(V):
    """the drawn first term: s * m * (2 when r = +-1/2, else 1)^(k - 1), rebuilt from the vars."""
    den = 2 if abs(V['r']) < 1 else 1
    return V['s'] * V['m'] * den ** (V['k'] - 1)


def l3_term(V):
    a, r, kk = l3_first_term(V), V['r'], V['k']
    seq = [a]
    for _ in range(int(kk) - 1):
        seq.append(seq[-1] * r)
    step = seq[1] - seq[0]
    return seq[-1], {'k-factors': seq[-1] * r, 'added-the-step': a + (kk - 1) * step}


def l3_ratio(V):
    a = V['s'] * V['m'] * V['q'] ** 2
    t2 = V['s'] * V['m'] * V['p'] * V['q']
    t3 = V['s'] * V['m'] * V['p'] ** 2
    r = sp.Rational(t2, a)
    assert sp.Rational(t3, t2) == r
    return r, {'upside-down': sp.Rational(a, t2), 'difference': t2 - a}


def l3_formula(V):
    a, r = V['a'], V['r']
    u = a * r ** (n - 1)
    assert [u.subs(n, i) for i in (1, 2, 3)] == [a, a * r, a * r * r]
    return u, {'n-factors': a * r ** n, 'ratio-and-first-swapped': r * a ** (n - 1),
               'arithmetic-rule': sp.expand(a + (n - 1) * (a * r - a))}


# ---- fluency-l6-gauss ----
def l6_one_to_n(V):
    m = V['m']
    s = sp.summation(k, (k, 1, m))
    return s, {'not-halved': 2 * s, 'one-term-short': sp.summation(k, (k, 1, m - 1))}


def l6_first_n(V):
    a, d, kk = V['a'], V['d'], V['k']
    s = sp.summation(a + (k - 1) * d, (k, 1, kk))
    return s, {'not-halved': 2 * s, 'k-steps': sp.Rational(kk, 2) * (2 * a + kk * d)}


def l6_to_last(V):
    a, d, kk = V['a'], V['d'], V['k']
    last = a + (kk - 1) * d
    count = sp.Rational(last - a, d) + 1
    assert count == kk
    s = sp.summation(a + (k - 1) * d, (k, 1, count))
    return s, {'counted-steps': sp.Rational(count - 1, 2) * (a + last), 'not-halved': 2 * s}


# ---- fluency-l7-shifted-copy ----
def l7_first_term(V):
    return V.get('s', 1) * V['m'] * (2 if abs(V['r']) < 1 else 1) ** (V['k'] - 1)


def geo_sum(a, r, cnt):
    return sp.summation(a * r ** k, (k, 0, cnt - 1))


def l7_first_n(V):
    a, r, kk = l7_first_term(V), V['r'], V['k']
    s = geo_sum(a, r, kk)
    return s, {'one-term-short': geo_sum(a, r, kk - 1), 'sign-flipped': -s}


def l7_to_last(V):
    a, r, kk = l7_first_term(V), V['r'], V['k']
    last = a * r ** (kk - 1)
    cnt = [j for j in range(1, 20) if a * r ** (j - 1) == last]
    assert cnt == [kk]
    s = geo_sum(a, r, cnt[0])
    return s, {'counted-steps': s - last, 'sign-flipped': -s}


def l7_sigma(V):
    r, b, t = V['r'], V['b'], V['t']
    s = sp.summation(r ** k, (k, b, t))
    return s, {'stopped-early': s - r ** t, 'one-term-extra': s + r ** (t + 1)}


# ---- fluency-l8-adding-forever ----
def s_inf(a, r):
    assert abs(r) < 1
    return sp.summation(a * r ** k, (k, 0, sp.oo))


def l8_terms(V):
    q = V['p'] + V['j']
    r = V['g'] * sp.Rational(V['p'], q)
    a = V['s'] * V['m'] * q ** 2
    s = s_inf(a, r)
    return s, {'sign-of-r': a / (1 + r), 'first-term-left-out': s_inf(1, r)}


def l8_a_r(V):
    r = V['g'] * sp.Rational(V['p'], V['p'] + V['j'])
    s = s_inf(V['a'], r)
    return s, {'sign-of-r': V['a'] / (1 + r), 'first-term-left-out': s_inf(1, r)}


def l8_bond(V):
    c, i = V['c'], V['i']
    g = 1 + i / 100
    pv = sp.summation(c / g ** k, (k, 1, sp.oo))
    return pv, {'payment-today': pv + c, 'per-cent-not-decimal': c / i}


def l8_recurring(V):
    """Widening pass: 0.tututu... summed as a geometric series of the digit pair, cross-checked against 40 places."""
    pair = 10 * V['t'] + V['u']
    s = s_inf(sp.Rational(pair, 100), sp.Rational(1, 100))
    places = sum(sp.Rational(int(c), 10 ** (i + 1)) for i, c in enumerate(('%d%d' % (V['t'], V['u'])) * 20))
    assert 0 <= s - places < sp.Rational(1, 10 ** 39) and 0 < s < 1
    return s, {'first-term-only': sp.Rational(pair, 100), 'sign-of-r': sp.Rational(pair, 100) / (1 + sp.Rational(1, 100))}


# ---- fluency-l11-powers-of-a-bracket ----
def coeff(expr, e):
    return sp.Poly(sp.expand(expr), x).coeff_monomial(x ** e)


def l11_plain(V):
    e, ne, b = V['e'], V['ne'], V['b']
    c = coeff((x + b) ** (e + ne), e)
    return c, {'count-only': sp.binomial(e + ne, e), 'power-swapped': sp.binomial(e + ne, e) * b ** e}


def l11_scaled(V):
    a, b, e, ne = V['a'], V['b'], V['e'], V['ne']
    c = coeff((a * x + b) ** (e + ne), e)
    cn = sp.binomial(e + ne, e)
    return c, {'a-not-raised': cn * a * b ** ne, 'a-left-out': cn * b ** ne}


def l11_no_x(V):
    nn, a, b = V['n'], V['a'], V['s'] * V['m']
    c = sp.Poly(sp.expand((a * x + b / x) ** nn * x ** nn), x).coeff_monomial(x ** nn)  # x^0 term of the bracket
    h = nn // 2
    return c, {'count-only': sp.binomial(nn, h), 'powers-only': (a * b) ** h}


FAMILIES = [
    ('fluency-l8-adding-forever', 'from-the-terms', l8_terms),
    ('fluency-l8-adding-forever', 'from-a-and-r', l8_a_r),
    ('fluency-l8-adding-forever', 'perpetual-bond', l8_bond),
    ('fluency-l8-adding-forever', 'recurring-decimal', l8_recurring),
    ('fluency-l11-powers-of-a-bracket', 'x-plus-b', l11_plain),
    ('fluency-l11-powers-of-a-bracket', 'ax-plus-b', l11_scaled),
    ('fluency-l11-powers-of-a-bracket', 'term-with-no-x', l11_no_x),
    ('fluency-l6-gauss', 'one-to-n', l6_one_to_n),
    ('fluency-l6-gauss', 'first-n-terms', l6_first_n),
    ('fluency-l6-gauss', 'up-to-last-term', l6_to_last),
    ('fluency-l7-shifted-copy', 'first-n-terms', l7_first_n),
    ('fluency-l7-shifted-copy', 'up-to-last-term', l7_to_last),
    ('fluency-l7-shifted-copy', 'sigma-powers', l7_sigma),
    ('fluency-l3-multiplying-each-time', 'geometric-term', l3_term),
    ('fluency-l3-multiplying-each-time', 'common-ratio', l3_ratio),
    ('fluency-l3-multiplying-each-time', 'geometric-formula', l3_formula),
    ('fluency-l2-any-term', 'term-from-list', l2_term),
    ('fluency-l2-any-term', 'nth-term-formula', l2_formula),
    ('fluency-l2-any-term', 'difference-from-two-terms', l2_difference),
    ('fluency-l2-any-term', 'which-term', l2_which),
]

if __name__ == '__main__':
    for set_id, fam, fn in FAMILIES:
        check(set_id, fam, fn)
    print('%d checks over %d families, %d failures' % (checked, len(FAMILIES), len(fails)))
    for f in fails[:30]:
        print('FAIL', f)
    sys.exit(1 if fails else 0)
