"""Recompute every Fluency answer and every named slip in the quadratics sets (and functions l8) from the drawn
variable values alone, with sympy, and compare with what the engine resolved (tools/fluency-sample.mjs --json).
Method 1 is the engine's own arithmetic in gen.js; method 2 is this script: sympy builds each expression from the
vars (expanding, factorising or solving), then checks that the engine's key equals it, that an expand key has no
bracket and a factorise key is a product, and that each wrong differs from the key and equals the slip it names.
Run with the sympy venv:  <scratchpad>/venv/bin/python docs/reports/fluency-quadratics-numbers.py   (exit 0 = pass)
"""
import json, os, subprocess, sys
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

APP = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app')
N = int(os.environ.get('FLUENCY_N', '200'))
TR = standard_transformations + (implicit_multiplication_application, convert_xor)
lv = Level("quadratics", 1)
count = 0


def draws(ref, fam):
    out = subprocess.run(['node', 'tools/fluency-sample.mjs', '--set', ref, '--family', fam, '--n', str(N), '--json'],
                         cwd=APP, capture_output=True, text=True, check=True).stdout
    return json.loads(out)['items']


def tex(s, v):
    sym = {v: sp.Symbol(v)}
    return parse_expr(s.replace('\\left', '').replace('\\right', ''), local_dict=sym, transformations=TR)


def R(x):
    return sp.nsimplify(x, rational=True) if isinstance(x, float) else sp.Integer(x) if isinstance(x, int) else x


def check(ok, label):
    global count
    count += 1
    lv.claim(bool(ok), label)


def expr_item(it, key, form, wrongs, v):
    """key: sympy expr; wrongs: {id: sympy expr}"""
    got = tex(it['answer'], v)
    check(sp.expand(got - key) == 0, f"{it['family']} seed {it['seed']}: key {it['answer']} equals {key}")
    if form == 'expanded':
        check('(' not in it['answer'], f"{it['family']} seed {it['seed']}: key has no bracket")
    if form == 'factorised':
        check(it['answer'].startswith('(') and (')(' in it['answer'] or it['answer'].endswith('^2')),
              f"{it['family']} seed {it['seed']}: key is a product")
    for w in it['wrong']:
        e = tex(w['tex'], v)
        check(sp.expand(e - key) != 0, f"{it['family']} seed {it['seed']}: wrong {w['id']} differs from key")
        check(sp.expand(e - wrongs[w['id']]) == 0, f"{it['family']} seed {it['seed']}: wrong {w['id']} is the named slip")


def num_item(it, key, wrongs, tol=0, wtol=0):
    a = it['answer']
    check(abs(float(a) - float(key)) <= 1e-9, f"{it['family']} seed {it['seed']}: key {a} equals {key}")
    for w in it['wrong']:
        val = float(w['value'])
        check(abs(val - float(key)) > tol + wtol, f"{it['family']} seed {it['seed']}: wrong {w['id']} outside the key tolerance")
        check(abs(val - float(wrongs[w['id']])) <= 1e-9, f"{it['family']} seed {it['seed']}: wrong {w['id']} is the named slip")
    vals = [float(w['value']) for w in it['wrong']]
    for i in range(len(vals)):
        for j in range(i + 1, len(vals)):
            check(abs(vals[i] - vals[j]) > 2 * wtol, f"{it['family']} seed {it['seed']}: wrongs {i} and {j} apart")


def run(ref, fam, fn):
    for it in draws(ref, fam):
        V = {k: (R(x) if not isinstance(x, str) else x) for k, x in it['vars'].items()}
        fn(it, V)


# ---- l1-two-brackets --------------------------------------------------------------------------------
def l1_monic(it, V):
    x = sp.Symbol(V['v']); a, b = V['a'], V['b']
    key = sp.expand((x + a) * (x + b))
    expr_item(it, key, 'expanded', {'firsts-lasts': x**2 + a*b, 'swapped': x**2 + a*b*x + (a + b)}, V['v'])


def l1_coef(it, V):
    x = sp.Symbol(V['v']); p, q, r, s = V['p'], V['q'], V['r'], V['s']
    key = sp.expand((p*x + q) * (r*x + s))
    expr_item(it, key, 'expanded', {'firsts-lasts': p*r*x**2 + q*s, 'added-numbers': p*r*x**2 + (q + s)*x + q*s}, V['v'])


def l1_square(it, V):
    x = sp.Symbol(V['v']); a = V['a']
    key = sp.expand((x + a)**2)
    expr_item(it, key, 'expanded', {'squares-only': x**2 + a**2, 'one-strip': x**2 + a*x + a**2}, V['v'])


# ---- l2-product-and-sum -----------------------------------------------------------------------------
def l2_monic(it, V):
    x = sp.Symbol(V['v']); p, q = V['p'], V['q']
    quad = sp.expand((x + p) * (x + q))
    check(sp.Poly(quad, x).all_coeffs() == [1, p + q, p*q], f"factorise-monic seed {it['seed']}: prompt coefficients")
    check(sp.factor(quad) == sp.factor((x + p) * (x + q)), f"factorise-monic seed {it['seed']}: sympy factor agrees")
    expr_item(it, quad, 'factorised', {'signs-swapped': (x - p)*(x - q), 'one-sign': (x + p)*(x - q)}, V['v'])


def l2_square(it, V):
    x = sp.Symbol(V['v']); p = V['p']
    expr_item(it, sp.expand((x + p)**2), 'factorised', {'wrong-sign': (x - p)**2, 'difference': (x + p)*(x - p)}, V['v'])


# ---- l3-leading-coefficient -------------------------------------------------------------------------
def l3_nonmonic(it, V):
    x = sp.Symbol(V['v']); p, q, s = V['p'], V['q'], V['s']
    quad = sp.expand((p*x + q) * (x + s))
    f = sp.factor_list(quad)
    check(f[0] in (1, -1), f"factorise-non-monic seed {it['seed']}: no common number factor")
    # the split numbers multiply to ac and add to b
    a, b, c = sp.Poly(quad, x).all_coeffs()
    check(p*s * q == a*c and p*s + q == b, f"factorise-non-monic seed {it['seed']}: split {p*s}, {q}")
    expr_item(it, quad, 'factorised', {'skipped-grouping': (x + p*s)*(x + q), 'numbers-swapped': (p*x + s)*(x + q)}, V['v'])


def l3_split(it, V):
    x = sp.Symbol(V['v']); p, q, r, s = V['p'], V['q'], V['r'], V['s']
    a, b, c = sp.Poly(sp.expand((p*x + q)*(r*x + s)), x).all_coeffs()
    num_item(it, a*c, {'last-term-only': c, 'the-sum': b})


# ---- l4-difference-of-squares -----------------------------------------------------------------------
def l4_sq(it, V):
    x = sp.Symbol(V['v']); p, q = V['p'], V['q']
    expr_item(it, p**2*x**2 - q**2, 'factorised', {'squared-difference': (p*x - q)**2, 'squared-sum': (p*x + q)**2}, V['v'])


def l4_rev(it, V):
    x = sp.Symbol(V['v']); p, q = V['p'], V['q']
    expr_item(it, q**2 - p**2*x**2, 'factorised', {'order-swapped': (p*x + q)*(p*x - q), 'squared-difference': (q - p*x)**2}, V['v'])


def l4_mental(it, V):
    s, d = V['s'], V['d']
    a, b = (s + d) / 2, (s - d) / 2
    check(a.is_integer and b.is_integer, f"mental-difference seed {it['seed']}: whole numbers")
    check(f"${a}^2 - {b}^2$" in it['prompt'], f"mental-difference seed {it['seed']}: prompt shows {a} and {b}")
    num_item(it, a**2 - b**2, {'difference-squared': (a - b)**2, 'sum-only': a + b})


# ---- l6-completing-the-square -----------------------------------------------------------------------
def l6_const(it, V):
    x = sp.Symbol(V['v']); h, c = V['h'], V['c']
    q = sp.Symbol('q')
    sol = sp.solve(sp.Eq(sp.expand((x + h)**2 + q), x**2 + 2*h*x + c), q)
    check(len(sol) == 1, f"find-the-constant seed {it['seed']}: one q")
    num_item(it, sol[0], {'added-corner': c + h**2, 'b-not-halved': c - (2*h)**2})


def roots_of(quad, x):
    rs = sorted(sp.solve(quad, x), key=lambda z: float(z))
    return rs


def l6_solve(it, V):
    x = sp.Symbol(V['v']); h, k, w = V['h'], V['k'], V['w']
    quad = x**2 - 2*h*x + h**2 - k**2
    lo, hi = roots_of(quad, x)
    key = hi if w == 'larger' else lo
    other = lo if w == 'larger' else hi
    # centre-sign: the same spread about -h
    lo2, hi2 = roots_of(x**2 + 2*h*x + h**2 - k**2, x)
    slip = hi2 if w == 'larger' else lo2
    num_item(it, key, {'other-root': other, 'centre-sign': slip})


def l6_max(it, V):
    x = sp.Symbol(V['v']); h, c = V['h'], V['c']
    f = -x**2 + 2*h*x + c
    xs = sp.solve(sp.diff(f, x), x)[0]
    top = f.subs(x, xs)
    num_item(it, top, {'corner-sign': c - h**2, 'gave-the-input': xs})


# ---- l7-the-formula ---------------------------------------------------------------------------------
def l7_disc(it, V):
    x = sp.Symbol(V['v']); a, b, c = V['a'], V['b'], V['c']
    num_item(it, sp.discriminant(a*x**2 + b*x + c, x), {'sign-of-4ac': b**2 + 4*a*c, 'dropped-four': b**2 - a*c})


def formula_slips(a, b, c, w):
    D = b**2 - 4*a*c
    g = 1 if w == 'larger' else -1
    return {'other-root': (-b - g*sp.sqrt(D)) / (2*a), 'b-for-minus-b': (b + g*sp.sqrt(D)) / (2*a),
            'halved-root-only': -b + g*sp.sqrt(D) / (2*a)}


def l7_rational(it, V):
    x = sp.Symbol(V['v']); p, q, s, w = V['p'], V['q'], V['s'], V['w']
    quad = sp.expand((p*x - q) * (x - s))
    a, b, c = sp.Poly(quad, x).all_coeffs()
    lo, hi = roots_of(quad, x)
    check(lo.is_rational and hi.is_rational, f"rational-roots seed {it['seed']}: rational roots")
    key = hi if w == 'larger' else lo
    num_item(it, key, formula_slips(a, b, c, w), tol=0.005, wtol=0.005)


def l7_decimal(it, V):
    x = sp.Symbol(V['v']); a, b, c, w = V['a'], V['b'], V['c'], V['w']
    lo, hi = roots_of(a*x**2 + b*x + c, x)
    check(not lo.is_rational, f"decimal-roots seed {it['seed']}: irrational roots")
    key = hi if w == 'larger' else lo
    check(it['accept'] == f"{float(key):.2f}" or abs(float(it['accept']) - float(key)) <= 0.005,
          f"decimal-roots seed {it['seed']}: accept {it['accept']} is the root to 2 dp")
    num_item(it, sp.N(key, 30), {k: sp.N(v, 30) for k, v in formula_slips(a, b, c, w).items()}, tol=0.005, wtol=0.005)


# ---- functions l8-line-through-two-points -----------------------------------------------------------
def f8_grad(it, V):
    x1, run, y1, m = V['x1'], V['run'], V['y1'], V['m']
    x2, y2 = x1 + run, y1 + m*run
    check(f"$A({x1}, {y1})$ and $B({x2}, {y2})$" in it['prompt'], f"gradient seed {it['seed']}: points in prompt")
    grad = sp.Rational(y2 - y1, x2 - x1)
    num_item(it, grad, {'run-over-rise': 1 / grad, 'sign-slip': (y2 - y1) / (x1 - x2)}, wtol=0.005)


def f8_line(it, V):
    X, Y = sp.symbols('x y'); mm, cc = sp.symbols('mm cc')
    x1, run, y1, m = V['x1'], V['run'], V['y1'], V['m']
    x2, y2 = x1 + run, y1 + m*run
    sol = sp.solve([sp.Eq(y1, mm*x1 + cc), sp.Eq(y2, mm*x2 + cc)], [mm, cc])
    key = sol[mm]*X + sol[cc]
    check(f"$A({x1}, {y1})$ and $B({x2}, {y2})$" in it['prompt'], f"line-equation seed {it['seed']}: points in prompt")
    expr_item(it, key, None, {'first-point-height': sol[mm]*X + y1, 'sign-of-c': sol[mm]*X + y1 + sol[mm]*x1}, 'x')


JOBS = [
    ('quadratics/fluency-l1-two-brackets', 'expand-monic', l1_monic),
    ('quadratics/fluency-l1-two-brackets', 'expand-coefficient', l1_coef),
    ('quadratics/fluency-l1-two-brackets', 'expand-square', l1_square),
    ('quadratics/fluency-l2-product-and-sum', 'factorise-monic', l2_monic),
    ('quadratics/fluency-l2-product-and-sum', 'perfect-square', l2_square),
    ('quadratics/fluency-l3-leading-coefficient', 'factorise-non-monic', l3_nonmonic),
    ('quadratics/fluency-l3-leading-coefficient', 'split-product', l3_split),
    ('quadratics/fluency-l4-difference-of-squares', 'square-minus-number', l4_sq),
    ('quadratics/fluency-l4-difference-of-squares', 'number-minus-square', l4_rev),
    ('quadratics/fluency-l4-difference-of-squares', 'mental-difference', l4_mental),
    ('quadratics/fluency-l6-completing-the-square', 'find-the-constant', l6_const),
    ('quadratics/fluency-l6-completing-the-square', 'solve-by-square', l6_solve),
    ('quadratics/fluency-l6-completing-the-square', 'largest-value', l6_max),
    ('quadratics/fluency-l7-the-formula', 'discriminant', l7_disc),
    ('quadratics/fluency-l7-the-formula', 'rational-roots', l7_rational),
    ('quadratics/fluency-l7-the-formula', 'decimal-roots', l7_decimal),
    ('functions/fluency-l8-line-through-two-points', 'gradient', f8_grad),
    ('functions/fluency-l8-line-through-two-points', 'line-equation', f8_line),
]

for ref, fam, fn in JOBS:
    run(ref, fam, fn)
print(f"{len(JOBS)} families, {N} draws each, {count} checks")
lv.report()
