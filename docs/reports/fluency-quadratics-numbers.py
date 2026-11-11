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

# ==== Level 4 (fluency and problems quadratics 4) ===================================================
# Method 2: sympy works each key from the vars alone (sqrt and its square factor, cancel and factor on the
# rational expressions, solve on the cleared equation, rem and div on the polynomials) and each slip from the
# step the learner got wrong; a second route (trial division, substitution, numeric evaluation) is checked too.
SETS4 = {}


def wtol4(ref, fam, wid):
    if ref not in SETS4:
        SETS4[ref] = json.load(open(os.path.join(APP, 'content', 'courses', *ref.split('/')) + '.json'))
    f = next(z for z in SETS4[ref]['families'] if z['id'] == fam)
    w = next(z for z in f['wrong'] if z['id'] == wid)
    return float((w.get('tol') or {}).get('abs', 0))


def num4(it, ref, key, slips, tol=0.0):
    tag = f"{it['family']} seed {it['seed']}"
    check(abs(float(it['answer']) - float(key)) <= 1e-9, f"{tag}: key {it['answer']} is {key}")
    want = {k for k, v in slips.items() if v is not None}
    got = {w['id']: float(w['value']) for w in it['wrong']}
    check(set(got) == want, f"{tag}: slips offered {sorted(got)} are {sorted(want)}")
    for wid, val in got.items():
        if wid in want:
            check(abs(val - float(slips[wid])) <= 1e-6, f"{tag}: slip {wid} {val} is {float(slips[wid])}")
        check(abs(val - float(key)) > tol + wtol4(ref, it['family'], wid), f"{tag}: slip {wid} outside the key band")
    vals = list(got.items())
    for i in range(len(vals)):
        for j in range(i + 1, len(vals)):
            check(abs(vals[i][1] - vals[j][1]) > wtol4(ref, it['family'], vals[i][0]) + wtol4(ref, it['family'], vals[j][0]),
                  f"{tag}: slips {vals[i][0]} and {vals[j][0]} apart")


def expr4(it, key, slips, v, form=None):
    """key, slips: sympy expressions (None = slip not offered); every wrong offered must be its slip and differ from the key
    and from every other wrong."""
    x = sp.Symbol(v)
    tag = f"{it['family']} seed {it['seed']}"
    got = tval(it['answer'], x)
    check(sp.simplify(got - key) == 0, f"{tag}: key {it['answer']} equals {key}")
    if form == 'expanded':
        check('(' not in it['answer'], f"{tag}: key has no bracket")
    if form in ('factorised', 'factorised-fully'):
        outside = re.sub(r'\([^()]*\)', '()', it['answer'])
        check('()' in outside and not re.search(r'(?<!^)[+-]', outside), f"{tag}: key {it['answer']} is a product")
    want = {k for k, e in slips.items() if e is not None}
    offered = {w['id']: tval(w['tex'], x) for w in it['wrong']}
    check(set(offered) == want, f"{tag}: slips offered {sorted(offered)} are {sorted(want)}")
    for wid, e in offered.items():
        check(sp.simplify(e - key) != 0, f"{tag}: wrong {wid} differs from the key")
        if wid in want:
            check(sp.simplify(e - slips[wid]) == 0, f"{tag}: wrong {wid} is the slip {slips[wid]}")
    ids = list(offered)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            check(sp.simplify(offered[ids[i]] - offered[ids[j]]) != 0, f"{tag}: wrongs {ids[i]} and {ids[j]} differ")


Q14 = 'quadratics/fluency-l14-roots-that-stay'
Q15 = 'quadratics/fluency-l15-fractions-with-letters'
Q16 = 'quadratics/fluency-l16-adding-and-solving'
Q17 = 'quadratics/fluency-l17-dividing-polynomials'


def q14_simplest(it, V):
    n = int(re.search(r'\\sqrt\{(\d+)\}', it['prompt']).group(1))
    s = sp.sqrt(n)                      # sympy writes it as a*sqrt(b) with b square-free
    a = s.as_coeff_Mul()[0]
    big = max(d for d in range(1, n + 1) if n % (d * d) == 0)
    check(a == big and sp.factorint(n // big ** 2) and all(e == 1 for e in sp.factorint(n // big ** 2).values()),
          f"simplest {n}: largest square factor {big}^2, rest square-free")
    k = int(V['k'])
    j = int(V['j'])
    early = min(p for p in sp.factorint(k)) if not sp.isprime(k) else None
    check((early or 0) == j, f"simplest {n}: the smallest prime of {k} is the early stop {j}")
    num4(it, Q14, a, {'stopped-early': early, 'square-not-root': a * a})


def q14_collect(it, V):
    m = re.search(r'\\sqrt\{(\d+)\} ([+-]) \\sqrt\{(\d+)\}\$ to \$k\\sqrt\{(\d+)\}', it['prompt'])
    A, op, B, r = int(m.group(1)), m.group(2), int(m.group(3)), int(m.group(4))
    sgn = 1 if op == '+' else -1
    tot = sp.sqrt(A) + sgn * sp.sqrt(B)
    key = sp.simplify(tot / sp.sqrt(r))
    check(key.is_integer, f"collect {A} {op} {B}: a whole number of sqrt({r})")
    check(abs(float(tot) - float(key) * r ** 0.5) < 1e-9, f"collect {A} {op} {B}: decimal check")
    p, q = sp.sqrt(sp.Rational(A, r)), sp.sqrt(sp.Rational(B, r))
    nr = p * p + sgn * q * q
    num4(it, Q14, key, {'no-roots': nr, 'sign': (p + q) if sgn < 0 and nr != p + q else None})


def q14_conj(it, V):
    m = re.search(r'\\dfrac\{(\d+)\}\{(\d+) ([+-]) \\sqrt\{(\d+)\}\}', it['prompt'])
    c, p, op, q = int(m.group(1)), int(m.group(2)), m.group(3), int(m.group(4))
    sgn = 1 if op == '+' else -1
    bottom = sp.expand((p + sgn * sp.sqrt(q)) * (p - sgn * sp.sqrt(q)))
    check(bottom.is_integer, f"conj {p} {op} sqrt{q}: the bottom is rational")
    check(bottom >= 1 and p * p > q, f"conj {p} {op} sqrt{q}: the new bottom {bottom} is a whole number of at least 1")
    check(f"{p} {'-' if sgn > 0 else '+'} \\sqrt{{{q}}}" in it['prompt'], f"conj {p}: the conjugate named is the right one")
    check(abs(float(c / (p + sgn * q ** 0.5)) - float(c * (p - sgn * q ** 0.5) / bottom)) < 1e-9, f"conj {p}: same value after rationalising")
    num4(it, Q14, bottom, {'added': p * p + q, 'squared-q': p * p - q * q})


def q15_cancel(it, V):
    a, b, c, v = int(V['a']), int(V['b']), int(V['c']), V['v']
    x = sp.Symbol(v)
    top, bot = sp.expand((x + a) * (x + b)), sp.expand((x + a) * (x + c))
    q = sp.cancel(top / bot)
    check(sp.simplify(q - (x + b) / (x + c)) == 0, f"cancel {a},{b},{c}: cancels to (x+b)/(x+c)")
    check(abs(float((top / bot).subs(x, sp.Rational(7, 3))) - float(((x + b) / (x + c)).subs(x, sp.Rational(7, 3)))) < 1e-12, f"cancel: value at 7/3")
    check(sp.denom(sp.together(q)) == x + c, f"cancel {a},{b},{c}: the bottom left is x + c")
    expr4(it, sp.numer(sp.together(q)),
          {'shared-bracket': x + a, 'sign-slip': x - b, 'whole': (x + b) / (x + c)}, v, 'expanded')


def q15_mult(it, V):
    a, b, k, v = int(V['a']), int(V['b']), int(V['k']), V['v']
    x = sp.Symbol(v)
    e = (x ** 2 - a * a) / (x + b) * (k * x + k * b) / (x - a)
    key = sp.factor(sp.cancel(e))
    check(sp.simplify(key - k * (x + a)) == 0, f"mult {a},{b},{k}: {key}")
    expr4(it, key, {'sign': k * (x - a), 'number-lost': x + a}, v, 'factorised')


def q15_div(it, V):
    a, b, v = int(V['a']), int(V['b']), V['v']
    x = sp.Symbol(v)
    e = ((x ** 2 + a * x) / (x - b)) / ((x + a) / (x ** 2 - b * b))
    key = sp.factor(sp.cancel(e))
    check(sp.simplify(key - x * (x + b)) == 0, f"div {a},{b}: {key}")
    expr4(it, key, {'sign': x * (x - b), 'letter-lost': x + b}, v, 'factorised')


def q16_add(it, V, sign=1):
    p, q, a, b, v = int(V['p']), int(V['q']), int(V['a']), int(V['b']), V['v']
    x = sp.Symbol(v)
    total = sp.together(p / (x + a) + sign * q / (x + b))
    top = sp.expand(sp.cancel(total * (x + a) * (x + b)))
    check(sp.expand(top - (p * (x + b) + sign * q * (x + a))) == 0, f"add {p},{q}: cross-multiplied top")
    return x, top, p, q, a, b, v


def q16_addtops(it, V):
    x, top, p, q, a, b, v = q16_add(it, V)
    check(it['prompt'].endswith('Type the top, simplified, with no brackets.'), f"add-tops seed {it['seed']}: the prompt rules out a bracketed top")
    expr4(it, top, {'own-bottoms': sp.expand(p * (x + a) + q * (x + b)), 'tops-added': sp.Integer(p + q),
                          'whole': top / ((x + a) * (x + b))}, v, 'simplified')


def q16_subtops(it, V):
    x, top, p, q, a, b, v = q16_add(it, V, -1)
    check(it['prompt'].endswith('Type the top, simplified, with no brackets.'), f"subtract-tops seed {it['seed']}: the prompt rules out a bracketed top")
    own = sp.expand(p * (x + a) - q * (x + b))
    lost = sp.expand(p * (x + b) - q * x + q * a)
    expr4(it, top, {'sign-lost': lost, 'own-bottoms': own if sp.expand(own - lost) != 0 else None,
                          'whole': top / ((x + a) * (x + b))}, v, 'simplified')


def q16_roots(it, V):
    A, B, k = int(V['aa']), int(V['bb']), int(V['k'])
    x = sp.Symbol('x')
    sols = sp.solve(sp.Eq(A / x + B / (x + k), 1), x)
    sols = sorted(sols)
    tag = f"roots seed {it['seed']}"
    check(sorted(float(z) for z in it['answers']) == [float(z) for z in sols], f"{tag}: answers {it['answers']} are {sols}")
    for z in sols:
        check(abs(A / float(z) + B / (float(z) + k) - 1) < 1e-12, f"{tag}: {z} satisfies the equation")
    w = it['wrong'][0]
    check(w['id'] == 'signs' and sorted(float(t) for t in w['value'].split(',')) == sorted(-float(z) for z in sols), f"{tag}: signs slip")
    check(sorted(-float(z) for z in sols) != [float(z) for z in sols], f"{tag}: signs slip is not the key set")


def q16_reject(it, V):
    a, b = int(V['a']), int(V['b'])
    x = sp.Symbol('x')
    sols = sp.solve(sp.Eq(b * x / (x - a), a * b / (x - a) + x), x)
    check(sols == [b], f"reject {a},{b}: sympy keeps only {sols}")
    cleared = sp.solve(sp.Eq(b * x, a * b + x * (x - a)), x)
    check(sorted(cleared) == sorted({a, b}), f"reject {a},{b}: clearing gives {cleared}")
    num4(it, Q16, b, {'kept-bad': a, 'sign': -b})


def q17_rem(it, V):
    lc, b, c, d, a = (int(V[z]) for z in ('lc', 'b', 'c', 'd', 'a'))
    x = sp.Symbol('x')
    f = lc * x ** 3 + b * x ** 2 + c * x + d
    r = sp.rem(f, x - a, x)
    check(r == f.subs(x, a), f"rem {f} by x-{a}: long division agrees with f(a)")
    num4(it, Q17, r, {'sign': f.subs(x, -a), 'no-constant': f.subs(x, a) - d})


def q17_k(it, V):
    a, k, c = int(V['a']), int(V['k']), int(V['c'])
    x, K = sp.symbols('x K')
    d = -(a ** 3 + k * a * a + c * a)
    check(f"{'+' if d > 0 else '-'}{abs(d)}$" in it['prompt'].replace(' ', ''), f"k {a}: the constant {d} is shown")
    f = x ** 3 + K * x ** 2 + c * x + d
    key = sp.solve(f.subs(x, a), K)[0]
    check(sp.rem(f.subs(K, key), x - a, x) == 0, f"k {a}: (x - {a}) divides with k = {key}")
    neg = sp.solve(f.subs(x, -a), K)[0]
    lin = sp.solve(a ** 3 + K * a + c * a + d, K)[0]
    num4(it, Q17, key, {'sign': neg if abs(neg - key) > 0.02 else None,
                       'power-dropped': lin if abs(lin - key) > 0.02 and abs(lin - neg) > 0.02 and a != 1 else None})


def q17_quot(it, V):
    a, p, q, v = int(V['a']), int(V['p']), int(V['q']), V['v']
    x = sp.Symbol(v)
    f = sp.expand((x - a) * (x ** 2 + p * x + q))
    quo, r = sp.div(f, x - a, x)
    check(r == 0 and sp.expand(quo - (x ** 2 + p * x + q)) == 0, f"quot {f}: exact, quotient {quo}")
    # the slip: synthetic division run with -a in place of a
    co = sp.Poly(f, x).all_coeffs()
    s1 = co[1] + (-a) * co[0]
    s0 = co[2] + (-a) * s1
    check('multiplied out' in it['prompt'], f"quot seed {it['seed']}: the prompt asks for the quotient multiplied out")
    expr4(it, quo, {'sign': x ** 2 + s1 * x + s0, 'constant-sign': x ** 2 + p * x - q}, v, 'expanded')


def q17_cubic(it, V):
    r, s, u, v = int(V['r']), int(V['s']), int(V['u']), V['v']
    x = sp.Symbol(v)
    f = sp.expand((x - r) * (x - s) * (x - u))
    fl = sp.factor_list(f)
    check(fl[0] == 1 and len(fl[1]) == 3 and all(sp.Poly(g, x).degree() == 1 for g, _ in fl[1]), f"cubic {f}: three linear factors")
    trial = [z for z in sp.divisors(abs(int(f.subs(x, 0)))) for z in (z, -z) if f.subs(x, z) == 0]
    check(sorted(set(trial)) == sorted([r, s, u]), f"cubic {f}: trial of the constant's factors finds {sorted(set(trial))}")
    expr4(it, sp.factor(f), {'signs': (x + r) * (x + s) * (x + u),
                             'one-sign': (x + r) * (x - s) * (x - u) if s + u != 0 else None}, v, 'factorised-fully')


JOBS += [
    (Q14, 'simplest-surd', q14_simplest), (Q14, 'collect-surds', q14_collect), (Q14, 'conjugate-bottom', q14_conj),
    (Q15, 'cancel-common-bracket', q15_cancel), (Q15, 'multiply-and-cancel', q15_mult), (Q15, 'divide-and-cancel', q15_div),
    (Q16, 'add-tops', q16_addtops), (Q16, 'subtract-tops', q16_subtops), (Q16, 'solve-two-roots', q16_roots), (Q16, 'reject-root', q16_reject),
    (Q17, 'remainder', q17_rem), (Q17, 'find-k', q17_k), (Q17, 'quotient', q17_quot), (Q17, 'factorise-cubic', q17_cubic),
]

for ref, fam, fn in JOBS:
    run(ref, fam, fn)
print(f"{len(JOBS)} families, {N} draws each, {count} checks")
lv.report()
