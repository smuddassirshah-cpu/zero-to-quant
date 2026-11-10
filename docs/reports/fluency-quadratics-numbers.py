"""Recompute every Fluency answer and every named slip in the quadratics sets (and functions l8) from the drawn
variable values alone, with sympy, and compare with what the engine resolved (tools/fluency-sample.mjs --json).
Method 1 is the engine's own arithmetic in gen.js; method 2 is this script: sympy builds each expression from the
vars (expanding, factorising or solving), then checks that the engine's key equals it, that an expand key has no
bracket and a factorise key is a product, and that each wrong differs from the key and equals the slip it names.
Run with the sympy venv:  <scratchpad>/venv/bin/python docs/reports/fluency-quadratics-numbers.py   (exit 0 = pass)
"""
import json, os, re, subprocess, sys
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


# ---- widening pass helpers: set answers and factorise fully ----------------------------------------
def tex2(s):
    """LaTeX with \\frac and \\sqrt as a string sympy can parse."""
    s = s.replace('\\left', '').replace('\\right', '').replace(' ', '')
    while True:
        s2 = re.sub(r'\\sqrt\{([^{}]*)\}', r'sqrt(\1)', s)
        s2 = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', s2)
        if s2 == s:
            return s
        s = s2


def tval(s, x):
    e = parse_expr(tex2(s), local_dict={str(x): x, 'sqrt': sp.sqrt}, transformations=TR)
    return sp.nsimplify(e, rational=True) if re.search(r'\d\.\d', s) else e


def same_set(A, B, tol):
    if len(A) != len(B):
        return False
    A = sorted(A, key=float)
    B = sorted(B, key=float)
    if tol == 0:
        return all(sp.simplify(a - b) == 0 for a, b in zip(A, B))
    return all(abs(float(a) - float(b)) <= tol for a, b in zip(A, B))


def set_item(it, roots, slips, x, tol=0):
    """roots: the true set from sympy; slips: {id: set}. Checks the engine's answers and every wrong set."""
    tag = f"{it['family']} seed {it['seed']}"
    check(it.get('unordered') is True and len(it['answers']) == len(roots), f"{tag}: an unordered set of {len(roots)}")
    if it['kind'] == 'expression':
        got = [tval(a, x) for a in it['answers']]
    else:
        got = [sp.nsimplify(float(a), rational=True) if tol == 0 else sp.Float(a) for a in it['answers']]
    check(same_set(got, roots, 1e-9 if tol else 0), f"{tag}: answers {it['answers']} are the roots {roots}")
    for w in it['wrong']:
        parts = [p.strip() for p in (w.get('tex') or w.get('value')).split(', ')]
        vals = [tval(p, x) for p in parts] if 'tex' in w else [sp.Float(p) for p in parts]
        wt = (w.get('tol') or {}).get('abs', 0) if 'value' in w else 0
        check(not same_set(vals, roots, tol + wt + 1e-9), f"{tag}: wrong {w['id']} is not the key set")
        check(same_set(vals, slips[w['id']], 1e-6 if 'value' in w else 0), f"{tag}: wrong {w['id']} is the slip {slips[w['id']]}")


def full_item(it, inner, k, wrongs, v):
    """Factorise fully: k is the content of the quadratic, the key starts with k, every factor left is linear."""
    x = sp.Symbol(v)
    whole = sp.expand(k * inner)
    content, factors = sp.factor_list(whole)
    tag = f"{it['family']} seed {it['seed']}"
    check(abs(content) == abs(k), f"{tag}: the common factor is {k}")
    check(it['answer'].startswith(f"{k}("), f"{tag}: key {it['answer']} starts with {k}")
    check(all(sp.Poly(f_, x).degree() == 1 for f_, _ in factors), f"{tag}: only linear factors are left")
    expr_item(it, whole, None, wrongs, v)


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


def l3_full(it, V):
    # widening pass: common factor first, graded with form factorised-fully
    x = sp.Symbol(V['v']); k, p, q, s = V['k'], V['p'], V['q'], V['s']
    inner = (p*x + q) * (x + s)
    ids = {w['id'] for w in it['wrong']}
    check(('factor-sign' in ids) == (k < 0) and ('numbers-swapped' in ids) == (p > 1 and q != s),
          f"common-factor-first seed {it['seed']}: the slips offered follow their when conditions")
    full_item(it, inner, k, {'factor-dropped': inner, 'factor-sign': -k*inner, 'numbers-swapped': k*(p*x + s)*(x + q)}, V['v'])


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


def l4_full(it, V):
    # widening pass: common factor, then the difference of squares, graded with form factorised-fully
    x = sp.Symbol(V['v']); k, p, q = V['k'], V['p'], V['q']
    inner = (p*x + q) * (p*x - q)
    full_item(it, inner, k, {'factor-dropped': inner, 'squared-difference': k*(p*x - q)**2}, V['v'])


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
    # widening pass: both roots as a set answer
    x = sp.Symbol(V['v']); h, k = V['h'], V['k']
    roots = roots_of(x**2 - 2*h*x + h**2 - k**2, x)
    check(len(roots) == 2, f"solve-by-square seed {it['seed']}: two roots")
    ids = {w['id'] for w in it['wrong']}
    check(('no-square-root' in ids) == (k > 1), f"solve-by-square seed {it['seed']}: no-square-root offered only for k > 1")
    slips = {'centre-sign': roots_of(x**2 + 2*h*x + h**2 - k**2, x),   # the same spread about -h
             'no-square-root': [h - k**2, h + k**2]}                   # k^2 itself used as the spread
    set_item(it, roots, slips, x)


def l6_form(it, V):
    # widening pass: the whole completed-square form, graded with form completed-square
    x = sp.Symbol(V['v']); b, c = V['b'], V['c']
    p_, q_ = sp.symbols('p_ q_')
    sol = sp.solve(sp.Poly(sp.expand((x + p_)**2 + q_ - (x**2 + b*x + c)), x).all_coeffs(), [p_, q_], dict=True)
    check(len(sol) == 1, f"square-form seed {it['seed']}: one (p, q)")
    p0, q0 = sol[0][p_], sol[0][q_]
    check(re.fullmatch(r'\([a-z][+-][0-9.]+\)\^2[+-][0-9.]+', it['answer']) is not None,
          f"square-form seed {it['seed']}: key {it['answer']} is a squared bracket plus a number")
    got_p = sp.nsimplify(re.match(r'\([a-z]([+-][0-9.]+)\)', it['answer']).group(1), rational=True)
    check(got_p == p0, f"square-form seed {it['seed']}: the bracket holds {p0}")
    hh = sp.Rational(b, 2)
    expr_item(it, sp.expand((x + p0)**2 + q0), None,
              {'added-corner': (x + hh)**2 + c + hh**2, 'b-not-halved': (x + b)**2 + c - b**2}, V['v'])


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


def formula_sets(a, b, c):
    """The slips of the formula, each as the set of two values it gives (widening pass: both roots)."""
    D = b**2 - 4*a*c
    return {'b-for-minus-b': [(b - sp.sqrt(D)) / (2*a), (b + sp.sqrt(D)) / (2*a)],
            'halved-root-only': [-b - sp.sqrt(D) / (2*a), -b + sp.sqrt(D) / (2*a)],
            'over-a': [(-b - sp.sqrt(D)) / a, (-b + sp.sqrt(D)) / a]}


def l7_rational(it, V):
    x = sp.Symbol(V['v']); p, q, s = V['p'], V['q'], V['s']
    quad = sp.expand((p*x - q) * (x - s))
    a, b, c = sp.Poly(quad, x).all_coeffs()
    roots = roots_of(quad, x)
    check(len(roots) == 2 and all(r.is_rational for r in roots), f"rational-roots seed {it['seed']}: two rational roots")
    want = f"${sp.latex(roots[0])}$ and ${sp.latex(roots[1])}$, or decimals within 0.005"
    bare = lambda t: re.sub(r'\\frac|[{} ]', '', t)
    check(bare(it['accept']) == bare(want), f"rational-roots seed {it['seed']}: accept {it['accept']} is {want}")
    set_item(it, roots, formula_sets(a, b, c), x, tol=0.005)


def l7_decimal(it, V):
    x = sp.Symbol(V['v']); a, b, c = V['a'], V['b'], V['c']
    roots = roots_of(a*x**2 + b*x + c, x)
    check(len(roots) == 2 and not roots[0].is_rational, f"decimal-roots seed {it['seed']}: two irrational roots")
    want = f"${float(roots[0]):.2f}$ and ${float(roots[1]):.2f}$"
    check(it['accept'] == want, f"decimal-roots seed {it['seed']}: accept {it['accept']} is {want}")
    set_item(it, roots, formula_sets(a, b, c), x, tol=0.005)


def l7_exact(it, V):
    # widening pass: exact surd roots as an expression set
    x = sp.Symbol(V['v']); a, b, c = V['a'], V['b'], V['c']
    D = b**2 - 4*a*c
    check(D > 0 and not sp.sqrt(D).is_rational, f"exact-roots seed {it['seed']}: surd roots")
    check(all(D % (m*m) != 0 for m in range(2, 14)), f"exact-roots seed {it['seed']}: {D} has no square factor")
    ids = {w['id'] for w in it['wrong']}
    check(('over-a' in ids) == (a > 1), f"exact-roots seed {it['seed']}: over-a offered only for a > 1")
    set_item(it, roots_of(a*x**2 + b*x + c, x), formula_sets(a, b, c), x)


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
    ('quadratics/fluency-l3-leading-coefficient', 'common-factor-first', l3_full),
    ('quadratics/fluency-l4-difference-of-squares', 'square-minus-number', l4_sq),
    ('quadratics/fluency-l4-difference-of-squares', 'number-minus-square', l4_rev),
    ('quadratics/fluency-l4-difference-of-squares', 'mental-difference', l4_mental),
    ('quadratics/fluency-l4-difference-of-squares', 'common-factor-first', l4_full),
    ('quadratics/fluency-l6-completing-the-square', 'find-the-constant', l6_const),
    ('quadratics/fluency-l6-completing-the-square', 'solve-by-square', l6_solve),
    ('quadratics/fluency-l6-completing-the-square', 'square-form', l6_form),
    ('quadratics/fluency-l6-completing-the-square', 'largest-value', l6_max),
    ('quadratics/fluency-l7-the-formula', 'discriminant', l7_disc),
    ('quadratics/fluency-l7-the-formula', 'rational-roots', l7_rational),
    ('quadratics/fluency-l7-the-formula', 'decimal-roots', l7_decimal),
    ('quadratics/fluency-l7-the-formula', 'exact-roots', l7_exact),
    ('functions/fluency-l8-line-through-two-points', 'gradient', f8_grad),
    ('functions/fluency-l8-line-through-two-points', 'line-equation', f8_line),
]

for ref, fam, fn in JOBS:
    run(ref, fam, fn)
print(f"{len(JOBS)} families, {N} draws each, {count} checks")
lv.report()
