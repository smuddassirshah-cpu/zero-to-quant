"""Recompute every Fluency answer and every named slip in the exp-log sets from the drawn variable values alone, with
sympy, and compare with what the engine resolved (tools/fluency-sample.mjs --json).
Method 1 is the engine's own arithmetic in gen.js (exact fractions, and since the widening pass the evaluator's own
`ln`; the first wave used the let formula 50000*(y^(1/100000) - y^(-1/100000)), which is 100000*sinh(ln y / 100000));
method 2 is this script: sympy evaluates the powers exactly and the logarithms with its own log, from the vars only.
It checks the key, that each wrong is the slip it names, that each wrong lies outside the key's tolerance, and that
an exact (expression) key equals the sympy value. Run with the sympy venv:
    <scratchpad>/venv/bin/python docs/reports/fluency-exp-log-numbers.py      (exit 0 = pass)
"""
import json, os, subprocess, sys
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

APP = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app')
N = int(os.environ.get('FLUENCY_N', '60'))
lv = Level("exp-log", 1)
count = 0


def draws(ref, fam):
    out = subprocess.run(['node', 'tools/fluency-sample.mjs', '--set', ref, '--family', fam, '--n', str(N), '--json'],
                         cwd=APP, capture_output=True, text=True, check=True).stdout
    return json.loads(out)['items']


def R(x):
    if isinstance(x, float):
        return sp.nsimplify(repr(x), rational=True)
    if isinstance(x, int):
        return sp.Integer(x)
    if isinstance(x, str):
        try:
            return sp.Rational(x)
        except (TypeError, ValueError):
            return x
    return x


def check(ok, label):
    global count
    count += 1
    lv.claim(bool(ok), label)


def tol_of(spec, key):
    t = spec or {'abs': 0}
    return float(t['abs']) if 'abs' in t else float(t['rel']) * abs(float(key))


def num_item(it, key, wrongs, close=1e-9):
    """key and wrongs from the vars only; close: how near the engine's key must be to sympy's (1e-9 for exact work)."""
    fam, seed = it['family'], it['seed']
    a = float(R(it['answer']))
    check(abs(a - float(key)) <= close * max(1, abs(float(key))), f"{fam} seed {seed}: key {a} equals {float(key)}")
    t = tol_of(it.get('tol'), key)
    for w in it['wrong']:
        val = float(R(w['value']))
        wt = tol_of(w.get('tol'), val)
        check(abs(val - float(key)) > t + wt, f"{fam} seed {seed}: wrong {w['id']} outside the key tolerance")
        check(abs(val - float(wrongs[w['id']])) <= close * max(1, abs(float(wrongs[w['id']]))),
              f"{fam} seed {seed}: wrong {w['id']} = {val} is the named slip {float(wrongs[w['id']])}")


def run(ref, fam, fn):
    for it in draws(ref, fam):
        V = {k: R(x) for k, x in it['vars'].items()}
        fn(it, V)


L3 = 'exp-log/fluency-l3-strange-powers'


# ---- l3-strange-powers ---------------------------------------------------------------------------
def l3_negative(it, V):
    a, n = V['a'], V['n']
    check(f"${a}^{{-{n}}}$" in it['prompt'], f"negative-power seed {it['seed']}: prompt shows {a}^-{n}")
    num_item(it, sp.Pow(a, -n), {'dropped-minus': a**n, 'times-the-power': -a*n})


def l3_fractional(it, V):
    r, n, m, g = V['r'], V['n'], V['m'], V['g']
    a = r**n
    s = sp.Rational(g*m, n)
    key = sp.Pow(a, s)                       # sympy evaluates the fractional power itself
    check(key == r**(g*m), f"fractional-power seed {it['seed']}: {a}^({s}) = {r}^{g*m}")
    num_item(it, key, {'times-the-power': a*s, 'flipped': 1/key})


def l3_laws(it, V):
    a, m, n, k = V['a'], V['m'], V['n'], V['k']
    p = m + n - k
    x = sp.Symbol('x', positive=True)
    key = sp.simplify((sp.Integer(a)**m * sp.Integer(a)**n) / sp.Integer(a)**p)
    check(f"{a}^{{{p}}}" in it['prompt'], f"laws-then-evaluate seed {it['seed']}: prompt divides by {a}^{p}")
    num_item(it, key, {'added-the-bottom': sp.Integer(a)**(m + n + p), 'multiplied-the-top': sp.Integer(a)**(m*n - p)})


def l3_power(it, V):
    m, n, p, v = V['m'], V['n'], V['p'], V['v']
    x = sp.Symbol('x', positive=True)
    e = sp.powsimp((x**m)**n / x**p)
    k = sp.simplify(sp.log(e.subs(x, 2), 2))        # the single power k, read back from 2^k
    num_item(it, k, {'added-the-powers': m + n - p, 'sign-of-divide': m*n + p})


# ---- LaTeX of the expression keys, read into sympy (only the shapes these sets write) -------------
TR = standard_transformations + (implicit_multiplication_application, convert_xor)


def tex(s, symbols=()):
    s = s.replace('\\dfrac', '\\frac').replace('\\left', '').replace('\\right', '')
    while '\\frac{' in s:                                   # innermost-first is not needed: our fracs do not nest
        i = s.index('\\frac{')
        j, depth = i + 6, 1
        while depth:
            depth += {'{': 1, '}': -1}.get(s[j], 0); j += 1
        k, depth = j + 1, 1
        while depth:
            depth += {'{': 1, '}': -1}.get(s[k], 0); k += 1
        s = s[:i] + '((' + s[i + 6:j - 1] + ')/(' + s[j + 1:k - 1] + '))' + s[k:]
    s = s.replace('\\ln', ' log').replace('\\log', ' log').replace('{', '(').replace('}', ')')
    loc = {c: sp.Symbol(c) for c in symbols}
    loc['log'] = sp.log
    return parse_expr(s, local_dict=loc, transformations=TR)


def expr_item(it, key, wrongs, symbols=()):
    fam, seed = it['family'], it['seed']
    got = tex(it['answer'], symbols)
    check(sp.simplify(got - key) == 0, f"{fam} seed {seed}: key {it['answer']} equals {key}")
    for w in it['wrong']:
        e = tex(w['tex'], symbols)
        check(sp.simplify(e - key) != 0 and (symbols or abs(float(e) - float(key)) > 1e-6),
              f"{fam} seed {seed}: wrong {w['id']} differs from the key")
        check(sp.simplify(e - wrongs[w['id']]) == 0, f"{fam} seed {seed}: wrong {w['id']} is the named slip")


# ---- l6-products-into-sums -----------------------------------------------------------------------
L6 = 'exp-log/fluency-l6-products-into-sums'
X, Y, B = sp.symbols('x y b', positive=True)
P, Qs = sp.symbols('p q')


def in_pq(e):
    return sp.expand(sp.expand_log(e, force=True)).subs({sp.log(X): P * sp.log(B), sp.log(Y): Qs * sp.log(B)}) / sp.log(B)


def l6_product(it, V):
    m, n = V['m'], V['n']
    key = sp.simplify(in_pq(sp.log(X**m * Y**n)))
    expr_item(it, key, {'powers-left-behind': P + Qs, 'multiplied-the-logs': m*n*P*Qs}, ('p', 'q'))


def l6_quotient(it, V):
    m, n = V['m'], V['n']
    key = sp.simplify(in_pq(sp.log(X**m / Y**n)))
    expr_item(it, key, {'added-for-divide': m*P + n*Qs, 'divided-the-logs': m*P / (n*Qs)}, ('p', 'q'))


def l6_sum(it, V):
    b, n, h, d = V['b'], V['n'], V['h'], V['d']
    u = 2 if b % 2 == 0 else 3
    w = b // u
    i = h % (n + 1)
    j = (i + 1 + d % n) % (n + 1)
    x, y = u**i * w**j, u**(n - i) * w**(n - j)
    check(f"$\\log_{{{b}}} {x} + \\log_{{{b}}} {y}$" in it['prompt'], f"combine-a-sum seed {it['seed']}: prompt shows {x} and {y}")
    key = sp.simplify(sp.log(x * y) / sp.log(b))
    check(key == n and i != j, f"combine-a-sum seed {it['seed']}: log_{b} {x*y} = {n}, and neither number is a power of {b}")
    num_item(it, key, {'log-of-the-sum': sp.log(x + y) / sp.log(b), 'multiplied-the-logs': sp.log(x) * sp.log(y) / sp.log(b)**2}, 1e-6)


def l6_difference(it, V):
    b, c, n = V['b'], V['c'], V['n']
    top = c * b**n
    check(f"$\\log_{{{b}}} {top} - \\log_{{{b}}} {c}$" in it['prompt'], f"combine-a-difference seed {it['seed']}: prompt")
    key = sp.simplify(sp.log(sp.Rational(top, c)) / sp.log(b))
    num_item(it, key, {'divided-the-logs': sp.log(top) / sp.log(c), 'subtracted-inside': sp.log(top - c) / sp.log(b)}, 1e-6)


# ---- l8-solving-for-the-power --------------------------------------------------------------------
L8 = 'exp-log/fluency-l8-solving-for-the-power'


def l8_exact(it, V):
    a, b = V['a'], V['b']
    x = sp.Symbol('x', real=True)
    root = sp.solve(sp.Eq(sp.Integer(a)**x, b), x)[0]          # sympy solves a^x = b itself
    check(not sp.nsimplify(root).is_integer, f"exact-power seed {it['seed']}: {b} is not a power of {a}")
    expr_item(it, root, {'upside-down': sp.log(a) / sp.log(b), 'divided-the-numbers': sp.Rational(b, a)})


def sf3(it, r):
    """Widening pass (sfN format): the shown answer is r to 3 significant figures, worked with Decimal at 40 digits from
    sympy's value; the tolerance is 0.51 of a unit in the third figure; r is not a whole number of those units."""
    import decimal
    decimal.getcontext().prec = 40
    v = decimal.Decimal(str(sp.N(r, 40)))
    unit = decimal.Decimal(1).scaleb(v.adjusted() - 2)
    shown = v.quantize(unit, rounding=decimal.ROUND_HALF_UP)
    text = format(shown, 'f')
    fam, seed = it['family'], it['seed']
    check(text == it['accept'], f"{fam} seed {seed}: accept {it['accept']} is {text} (3 sf)")
    check(len(text.replace('.', '').lstrip('0')) == 3, f"{fam} seed {seed}: {text} has 3 figures")
    check(abs(tol_of(it.get('tol'), r) - 0.51 * float(unit)) < 1e-12, f"{fam} seed {seed}: tol is 0.51 of a unit")
    check(f"{shown}" in ''.join(it['solution']), f"{fam} seed {seed}: solution states {text}")
    check(abs(float(v / unit) - round(float(v / unit))) > 0.01, f"{fam} seed {seed}: not an exact 3 sf value")


def l8_sf(it, V):
    a, b = V['a'], V['b']
    r = sp.log(b) / sp.log(a)
    sf3(it, r)
    num_item(it, r, {'upside-down': 1 / r, 'divided-the-numbers': sp.Rational(b) / a}, 1e-6)


def l8_alone(it, V):
    c, a, n = V['c'], V['a'], V['n']
    d = c * a**n
    x = sp.Symbol('x', real=True)
    root = sp.solve(sp.Eq(c * sp.Integer(a)**x, d), x)[0]
    num_item(it, sp.nsimplify(root), {'stopped-early': a**n, 'joined-the-base': sp.log(d) / sp.log(c * a)}, 1e-6)


def l8_money(it, V):
    p, g, q = V['p'], V['g'], V['q']
    t = p * q
    r = sp.log(sp.Rational(t) / p) / sp.log(g)
    sf3(it, r)
    num_item(it, r, {'joined-the-base': sp.log(t) / sp.log(p * g), 'logs-too-soon': sp.log(t) / sp.log(g)}, 1e-6)


# ---- l10-natural-log -----------------------------------------------------------------------------
L10 = 'exp-log/fluency-l10-natural-log'


def l10_exact(it, V):
    k, b = V['k'], V['b']
    x = sp.Symbol('x', real=True)
    root = sp.solve(sp.Eq(sp.exp(k * x), b), x)[0]
    expr_item(it, root, {'multiplied-by-k': k * sp.log(b), 'divided-inside': sp.log(sp.Rational(b, k))})


def l10_growth(it, V):
    p, r, q = V['p'], V['r'], V['q']
    t = sp.Symbol('t', real=True)
    root = sp.solve(sp.Eq(p * sp.exp(sp.Rational(r, 100) * t), p * q), t)[0]
    check(f"{float(root):.2f}" == it['accept'], f"continuous-growth seed {it['seed']}: accept shows {float(root):.2f}")
    num_item(it, root, {'logs-too-soon': sp.log(p * q) / sp.Rational(r, 100), 'rate-as-whole-number': sp.log(q) / r}, 1e-6)


def l10_two(it, V):
    f, g, i, j = V['f'], V['g'], V['i'], V['j']
    lf, lg = sp.Rational(str(round(float(sp.log(f)), 4))), sp.Rational(str(round(float(sp.log(g)), 4)))
    check(f"$\\ln {f} = {float(lf):.4f}$ and $\\ln {g} = {float(lg):.4f}$" in it['prompt'], f"ln-from-two-values seed {it['seed']}: given values are ln to 4 dp")
    x = sp.Integer(f)**i * sp.Integer(g)**j
    key = i * lf + j * lg
    check(abs(float(key) - float(sp.log(x))) < 0.0005, f"ln-from-two-values seed {it['seed']}: the true ln {x} is inside the tolerance")
    num_item(it, key, {'powers-left-behind': sp.sign(i) * lf + sp.sign(j) * lg, 'swapped-the-values': i * lg + j * lf})


def l10_base(it, V):
    b = V['b']
    k = sp.Symbol('k')
    x = sp.Symbol('x', positive=True)
    root = sp.solve(sp.Eq(sp.log(sp.Integer(b)**x), k * x), k)[0]     # b^x = e^(kx)  <=>  x ln b = k x
    root = sp.expand_log(root, force=True)
    num_item(it, root, {'used-log': sp.log(b, 10), 'one-over': 1 / sp.log(b)}, 1e-6)


JOBS = [
    (L3, 'negative-power', l3_negative),
    (L3, 'fractional-power', l3_fractional),
    (L3, 'laws-then-evaluate', l3_laws),
    (L3, 'power-of-a-power', l3_power),
    (L6, 'split-a-product', l6_product),
    (L6, 'split-a-quotient', l6_quotient),
    (L6, 'combine-a-sum', l6_sum),
    (L6, 'combine-a-difference', l6_difference),
    (L8, 'exact-power', l8_exact),
    (L8, 'power-to-3-sf', l8_sf),
    (L8, 'power-alone-first', l8_alone),
    (L8, 'money-target', l8_money),
    (L10, 'exact-with-ln', l10_exact),
    (L10, 'continuous-growth', l10_growth),
    (L10, 'ln-from-two-values', l10_two),
    (L10, 'any-base-as-e', l10_base),
]

for ref, fam, fn in JOBS:
    run(ref, fam, fn)
print(f"{len(JOBS)} families, {N} draws each, {count} checks")
lv.report()
