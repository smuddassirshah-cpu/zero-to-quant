"""Recompute every Fluency family of the limits course from the drawn variables alone (docs/briefs/fluency.md check 1).

Run from anywhere with a Python that has sympy:
    <scratchpad>/venv/bin/python docs/reports/fluency-limits-numbers.py [--n 200]
For each family it reads `node tools/fluency-sample.mjs --set limits/<set> --family <id> --n N --json`, derives the key
again with sympy from `vars` only (never from the printed answer), checks it equals the engine's resolved answer,
and checks each `wrong` equals the slip recomputed from the vars and differs from the key. Exit 0 when all agree.
"""
import json
import os
import subprocess
import sys

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

APP = os.environ.get('FLUENCY_APP') or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app')
N = int(sys.argv[sys.argv.index('--n') + 1]) if '--n' in sys.argv else int(os.environ.get('FLUENCY_N', '60'))
x, t, h = sp.symbols('x t h')
SYM = {'x': x, 't': t, 'h': h}
R = sp.Rational
fails = []
checked = 0


# ---- a small LaTeX reader for the shapes these sets print ----
def _group(s, i):
    """s[i] == '{': return (inner, index after the closing brace)."""
    assert s[i] == '{', (s, i)
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
    out, i = [], 0
    while i < len(s):
        if s.startswith('\\dfrac', i) or s.startswith('\\frac', i):
            i += 6 if s.startswith('\\dfrac', i) else 5
            a, i = _group(s, i)
            b, i = _group(s, i)
            out.append(' ((%s)/(%s)) ' % (tex2py(a), tex2py(b)))
        elif s.startswith('\\sqrt', i):
            a, i = _group(s, i + 5)
            out.append(' sqrt(%s) ' % tex2py(a))
        elif s.startswith('e^', i):
            i += 2
            if s[i] == '{':
                a, i = _group(s, i)
            else:
                a, i = s[i], i + 1
            out.append(' exp(%s) ' % tex2py(a))
        elif s[i] == '^':
            i += 1
            if s[i] == '{':
                a, i = _group(s, i)
            else:
                a, i = s[i], i + 1
            out.append('**(%s) ' % tex2py(a))
        elif s.startswith('\\sin', i) or s.startswith('\\cos', i):
            out.append(' %s' % s[i + 1:i + 4])
            i += 4
        elif s.startswith('\\ln', i):
            out.append(' log')
            i += 3
        elif s.startswith('\\left', i):
            i += 5
        elif s.startswith('\\right', i):
            i += 6
        elif s.startswith('\\,', i):
            i += 2
        elif s[i] == '{':
            a, i = _group(s, i)
            out.append('(%s)' % tex2py(a))
        else:
            c = s[i]
            out.append(' %s ' % c if c.isalpha() else c)
            i += 1
    return ''.join(out)


def parse(s):
    return parse_expr(tex2py(s), local_dict=dict(SYM, exp=sp.exp, sqrt=sp.sqrt, sin=sp.sin, cos=sp.cos, log=sp.log),
                      transformations=standard_transformations + (implicit_multiplication_application,))


def same(a, b):
    d = sp.simplify(sp.expand(a - b))
    if d == 0:
        return True
    # numeric fallback at a few points (log/sqrt shapes)
    free = sorted(d.free_symbols, key=str)
    for pt in (0.37, 0.81, 1.3, 2.2):
        v = complex(d.subs({s_: pt for s_ in free}).evalf())
        if abs(v) > 1e-9:
            return False
    return True


def num(v):
    return sp.nsimplify(v, rational=True) if isinstance(v, float) else sp.Integer(v) if isinstance(v, int) else parse(str(v))


def sample(set_id, fam):
    out = subprocess.run(['node', 'tools/fluency-sample.mjs', '--set', 'limits/' + set_id, '--family', fam,
                          '--n', str(N), '--json'], cwd=APP, capture_output=True, text=True, check=True).stdout
    return json.loads(out)['items']


def check(set_id, fam, derive):
    """derive(vars) -> (key, {wrong_id: value}); expression keys are sympy expressions, numeric keys are Rationals."""
    global checked
    for it in sample(set_id, fam):
        V = {k: (sp.nsimplify(v, rational=True) if isinstance(v, (int, float)) else v) for k, v in it['vars'].items()}
        key, wrongs = derive(V)
        label = '%s/%s seed %s' % (set_id, fam, it['seed'])
        if it['kind'] == 'numeric':
            got = sp.Rational(str(it['answer']))
            tol = (it.get('tol') or {}).get('abs', 0)
            ok = abs(float(got - key)) <= 1e-9
        else:
            got = parse(it['answer'])
            ok = same(got, key)
        checked += 1
        if not ok:
            fails.append('%s: key %s, engine %s' % (label, key, it['answer']))
        if set(wrongs) != {w['id'] for w in it['wrong']}:
            fails.append('%s: offered %s, expected %s' % (label, [w['id'] for w in it['wrong']], sorted(wrongs)))
            continue
        for w in it['wrong']:
            want = wrongs[w['id']]
            if it['kind'] == 'numeric':
                wv = sp.Rational(str(w['value']))
                okw = abs(float(wv - want)) <= 1e-9 and abs(float(wv - key)) > tol
            else:
                wv = parse(w['tex'])
                okw = same(wv, want) and not same(wv, key)
            checked += 1
            if not okw:
                fails.append('%s: wrong %s, expected %s, engine %s' % (label, w['id'], want, w.get('tex', w.get('value'))))


# ---- fluency-l7-power-rule ----
def poly(v, *cs):
    n = len(cs) - 1
    return sum(c * v ** (n - i) for i, c in enumerate(cs))


def l7_polynomial(V):
    v = SYM[V['v']]
    f = poly(v, V['a'], V['b'], V['c'], V['d'])
    d = sp.diff(f, v)
    return d, {'power-not-lowered': sp.expand(d * v), 'constant-kept': d + V['d']}


def l7_negative(V):
    f = V['s'] * V['a'] / x ** V['n']
    d = sp.diff(f, x)
    return d, {'bottom-differentiated': V['s'] * V['a'] / sp.diff(x ** V['n'], x),
               'power-raised': -V['n'] * V['s'] * V['a'] * x ** (1 - V['n'])}


def l7_fractional(V):
    k = V['s'] * V['m'] * V['q']
    e = V['p'] / V['q']
    d = sp.diff(k * x ** e, x)
    return d, {'power-raised': k * e * x ** (e + 1), 'power-not-brought-down': k * x ** (e - 1)}


def l7_point(V):
    f = poly(x, V['a'], V['b'], V['c'], V['d'])
    fp = sp.diff(f, x)
    k = V['k']
    return fp.subs(x, k), {'value-not-slope': f.subs(x, k), 'power-not-lowered': (fp * x).subs(x, k)}


# ---- fluency-l2-computing-limits: sympy's limit of the drawn fraction ----
def l2_linear(V):
    a, b = V['a'], V['b']
    top = sp.expand((x - a) * (x + b))
    return sp.limit(top / (x - a), x, a), {'zero-over-zero-is-zero': 0, 'zero-over-zero-is-one': 1,
                                           'sign-of-factor': sp.limit(sp.expand((x - a) * (x - b)) / (x - a), x, a)}


def l2_quadratics(V):
    a, b, c = V['a'], V['b'], V['c']
    f = sp.expand((x - a) * (x + b)) / sp.expand((x - a) * (x + c))
    L = sp.limit(f, x, a)
    return L, {'upside-down': 1 / L, 'zero-over-zero-is-one': 1}


def l2_quotient(V):
    k, a = V['k'], V['a']
    L = sp.limit((k * (a + h) ** 2 - k * a ** 2) / h, h, 0)
    return L, {'square-split': sp.limit((k * (a ** 2 + h ** 2) - k * a ** 2) / h, h, 0),
               'factor-dropped': sp.limit(((a + h) ** 2 - a ** 2) / h, h, 0)}


# ---- fluency-l9-products-quotients ----
def l9_product(V):
    n, a, b = V['n'], V['a'], V['b']
    u, v = x ** n, a * x + b
    return sp.diff(u * v, x), {'product-of-derivatives': sp.diff(u, x) * sp.diff(v, x), 'one-term-only': sp.diff(u, x) * v}


def l9_quotient(V):
    a, b, c, d = V['a'], V['b'], V['c'], V['d']
    u, v = a * x + b, c * x + d
    return sp.diff(u / v, x), {'sign-reversed': (u * sp.diff(v, x) - sp.diff(u, x) * v) / v ** 2,
                               'not-squared': (sp.diff(u, x) * v - u * sp.diff(v, x)) / v}


def l9_point(V):
    p, q, r, k = V['p'], V['q'], V['r'], V['k']
    u, v = x ** 2 + p, q * x + r
    at = lambda e: e.subs(x, k)
    return at(sp.diff(u * v, x)), {'product-of-derivatives': at(sp.diff(u, x) * sp.diff(v, x)),
                                   'one-term-only': at(sp.diff(u, x) * v)}


# ---- fluency-l10-inside-function ----
def l10_linear(V):
    a, b, n = V['a'], V['b'], V['n']
    g = a * x + b
    slips = {'power-not-lowered': n * a * g ** n}
    if a != 1:   # widening pass: a = 1 is drawn, and the slip is switched off there by `when`
        slips['inside-forgotten'] = n * g ** (n - 1)
    return sp.diff(g ** n, x), slips


def l10_square(V):
    a, b, n = V['a'], V['b'], V['n']
    g = a * x ** 2 + b
    return sp.diff(g ** n, x), {'inside-forgotten': n * g ** (n - 1), 'x-dropped': n * 2 * a * g ** (n - 1)}


def l10_root(V):
    a, b = V['a'], V['b']
    g = a * x ** 2 + b
    return sp.diff(sp.sqrt(g), x), {'inside-forgotten': 1 / (2 * sp.sqrt(g)), 'half-dropped': 2 * a * x / sp.sqrt(g)}


# ---- fluency-l11-standard-derivatives ----
def l11_exp(V):
    v = SYM[V['v']]
    a, k = V['a'], V['k']
    return sp.diff(a * sp.exp(k * v), v), {'inside-forgotten': a * sp.exp(k * v),
                                            'power-rule-used': a * k * v * sp.exp(k * v - 1)}


def l11_log(V):
    a, b, m = V['a'], V['b'], V['m']
    return sp.diff(m * sp.log(a * x + b), x), {'inside-forgotten': m / (a * x + b), 'one-over-x': m / x}


def l11_sin(V):
    v = SYM[V['v']]
    a, k = V['a'], V['k']
    d = sp.diff(a * sp.sin(k * v), v)
    return d, {'inside-forgotten': a * sp.cos(k * v), 'sign-flipped': -d}


def l11_cos(V):
    v = SYM[V['v']]
    a, k = V['a'], V['k']
    d = sp.diff(a * sp.cos(k * v), v)
    return d, {'sign-lost': -d, 'inside-forgotten': -a * sp.sin(k * v)}


# ---- fluency-l12-implicit: sympy's idiff at the point, after checking the point is on the curve ----
Y = sp.Symbol('y')


def on_curve(F, p, q):
    assert F.subs({x: p, Y: q}) == 0, (F, p, q)


def l12_ellipse(V):
    a, b, p, q = V['a'], V['b'], V['p'], V['q']
    c = a * p ** 2 + b * q ** 2
    F = a * x ** 2 + b * Y ** 2 - c
    on_curve(F, p, q)
    s = sp.idiff(F, Y, x).subs({x: p, Y: q})
    return s, {'sign-lost': -s, 'upside-down': 1 / s}


def l12_extra(V):
    k, p, q = V['k'], V['p'], V['q']
    c = p ** 2 + q ** 2 + k * q
    F = x ** 2 + Y ** 2 + k * Y - c
    on_curve(F, p, q)
    s = sp.idiff(F, Y, x).subs({x: p, Y: q})
    # slips: k*y differentiated as k (no y'), or dropped
    return s, {'y-term-missed': -(2 * p + k) / (2 * q), 'y-term-dropped': -p / q}


def l12_product(V):
    k, p, q = V['k'], V['p'], V['q']
    c = p ** 2 + k * p * q + q ** 2
    F = x ** 2 + k * x * Y + Y ** 2 - c
    on_curve(F, p, q)
    s = sp.idiff(F, Y, x).subs({x: p, Y: q})
    return s, {'xy-as-y-only': -(2 * p + k * q) / (2 * q), 'xy-as-xy-prime-only': -(2 * p) / (k * p + 2 * q)}


# ---- fluency-l13-peaks-and-troughs: rebuild f from its stationary points, solve f' = 0, classify by f'' ----
def l13_cubic(V):
    A, r, g, d = V['A'], V['r'], V['g'], V['d']
    s = r + g
    f = sp.integrate(3 * A * (x - r) * (x - s), x) + d
    roots = sp.solve(sp.diff(f, x), x)
    mx = [z for z in roots if sp.diff(f, x, 2).subs(x, z) < 0][0]
    mn = [z for z in roots if sp.diff(f, x, 2).subs(x, z) > 0][0]
    return f, mx, mn


def l13_max(V):
    f, mx, mn = l13_cubic(dict(V, A=V['ka']))
    return mx, {'trough-given': mn, 'sign-slip': -mx}


def l13_min(V):
    f, mx, mn = l13_cubic(dict(V, A=V['ka']))
    return mn, {'peak-given': mx, 'sign-slip': -mn}


def l13_value(V):
    f, mx, mn = l13_cubic(dict(V, A=V['ka']))
    return f.subs(x, mn), {'x-not-value': mn, 'peak-value': f.subs(x, mx)}


def l13_closed(V):
    """Widening pass: the largest value of the cubic on [lo, hi], from f' = 0 and the two ends, compared by sympy."""
    A, r, g, d, e1, e2 = V['ka'], V['r'], V['g'], V['d'], V['e1'], V['e2']
    f, mx, mn = l13_cubic(dict(V, A=A))
    lo, hi = min(mx, mn) - e1, max(mx, mn) + e2
    crit = [z for z in sp.solve(sp.diff(f, x), x) if lo <= z <= hi]
    assert len(crit) == 2
    cands = [lo] + sorted(crit) + [hi]
    vals = {z: f.subs(x, z) for z in cands}
    top = max(vals.values())
    arg = [z for z in cands if vals[z] == top]
    xa = hi if hi in arg else lo if lo in arg else mx
    slips = {'smallest': min(vals.values())}
    if f.subs(x, mx) != top:
        slips['local-max'] = f.subs(x, mx)
    if xa != top:
        slips['x-not-value'] = xa
    return top, slips


FAMILIES = [
    ('fluency-l13-peaks-and-troughs', 'closed-interval-maximum', l13_closed),
    ('fluency-l2-computing-limits', 'cancel-linear-bottom', l2_linear),
    ('fluency-l2-computing-limits', 'cancel-two-quadratics', l2_quadratics),
    ('fluency-l2-computing-limits', 'difference-quotient', l2_quotient),
    ('fluency-l9-products-quotients', 'product-rule', l9_product),
    ('fluency-l9-products-quotients', 'quotient-rule', l9_quotient),
    ('fluency-l9-products-quotients', 'product-at-a-point', l9_point),
    ('fluency-l10-inside-function', 'linear-inside', l10_linear),
    ('fluency-l10-inside-function', 'square-inside', l10_square),
    ('fluency-l10-inside-function', 'root-inside', l10_root),
    ('fluency-l11-standard-derivatives', 'exponential-chain', l11_exp),
    ('fluency-l11-standard-derivatives', 'log-chain', l11_log),
    ('fluency-l11-standard-derivatives', 'sine-chain', l11_sin),
    ('fluency-l11-standard-derivatives', 'cosine-chain', l11_cos),
    ('fluency-l12-implicit', 'ellipse', l12_ellipse),
    ('fluency-l12-implicit', 'extra-y-term', l12_extra),
    ('fluency-l12-implicit', 'product-term', l12_product),
    ('fluency-l13-peaks-and-troughs', 'local-maximum', l13_max),
    ('fluency-l13-peaks-and-troughs', 'local-minimum', l13_min),
    ('fluency-l13-peaks-and-troughs', 'minimum-value', l13_value),
    ('fluency-l7-power-rule', 'polynomial', l7_polynomial),
    ('fluency-l7-power-rule', 'negative-power', l7_negative),
    ('fluency-l7-power-rule', 'fractional-power', l7_fractional),
    ('fluency-l7-power-rule', 'slope-at-a-point', l7_point),
]

if __name__ == '__main__':
    for set_id, fam, fn in FAMILIES:
        check(set_id, fam, fn)
    for f in fails[:30]:
        print('FAIL', f)
    print('%d checks over %d families, %d failures' % (checked, len(FAMILIES), len(fails)))
    sys.exit(1 if fails else 0)
