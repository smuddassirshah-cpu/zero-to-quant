"""Recompute every Fluency answer and every named slip in the trig sets from the drawn variable values alone, with
sympy, and compare with what the engine resolved (tools/fluency-sample.mjs --json).
Method 1 is the engine's own arithmetic in gen.js (exact fractions; since the widening pass the sines, cosines and
tangents of l3 come from the evaluator's own `sin`, `cos`, `tan` and `pi`, rounded to 4 dp); method 2 is this script: sympy's exact sin, cos, tan and pi,
and Pythagoras from the vars only. It checks the key, that each wrong is the slip it names, that each wrong lies
outside the key's tolerance, that the values a prompt gives are the true ratios to 4 dp, and that an exact key equals
sympy's exact value. Run with the sympy venv:
    <scratchpad>/venv/bin/python docs/reports/fluency-trig-numbers.py      (exit 0 = pass)
"""
import json, os, re, subprocess, sys
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

APP = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app')
N = int(os.environ.get('FLUENCY_N', '60'))
lv = Level("trig", 1)
count = 0
TR = standard_transformations + (implicit_multiplication_application, convert_xor)
DEG = sp.pi / 180


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


def num_item(it, key, wrongs, close=1e-6):
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


def tex(s):
    s = s.replace('\\dfrac', '\\frac')
    while '\\frac{' in s:
        i = s.index('\\frac{')
        j, depth = i + 6, 1
        while depth:
            depth += {'{': 1, '}': -1}.get(s[j], 0); j += 1
        k, depth = j + 1, 1
        while depth:
            depth += {'{': 1, '}': -1}.get(s[k], 0); k += 1
        s = s[:i] + '((' + s[i + 6:j - 1] + ')/(' + s[j + 1:k - 1] + '))' + s[k:]
    s = s.replace('\\sqrt', ' sqrt').replace('\\pi', ' pi ').replace('{', '(').replace('}', ')')
    return parse_expr(s, local_dict={'sqrt': sp.sqrt, 'pi': sp.pi}, transformations=TR)


def expr_item(it, key, wrongs):
    fam, seed = it['family'], it['seed']
    got = tex(it['answer'])
    check(sp.simplify(got - key) == 0, f"{fam} seed {seed}: key {it['answer']} equals {key}")
    check('.' not in it['answer'], f"{fam} seed {seed}: key {it['answer']} has no decimal")
    for w in it['wrong']:
        e = tex(w['tex'])
        check(abs(float(e - key)) > 1e-6, f"{fam} seed {seed}: wrong {w['id']} differs from the key")
        check(sp.simplify(e - wrongs[w['id']]) == 0, f"{fam} seed {seed}: wrong {w['id']} is the named slip")


def run(ref, fam, fn):
    for it in draws(ref, fam):
        V = {k: R(x) for k, x in it['vars'].items()}
        fn(it, V)


# ---- l1-squares-on-sides -------------------------------------------------------------------------
L1 = 'trig/fluency-l1-squares-on-sides'
A, B, C = sp.symbols('a b c', positive=True)


def triple(V):
    m, n = V['mn'] // 10, V['mn'] % 10
    k = 1 + V['h'] % (100 // (m**2 + n**2))
    p, q = k * (m**2 - n**2), 2 * k * m * n
    a, b = (p, q) if V['o'] == 1 else (q, p)
    return a, b


def l1_hyp(it, V):
    a, b = triple(V)
    check(f"short sides {a} and {b}." in it['prompt'], f"hypotenuse-whole seed {it['seed']}: prompt sides {a}, {b}")
    c = sp.solve(sp.Eq(C**2, a**2 + b**2), C)[0]
    check(c.is_integer and c <= 100, f"hypotenuse-whole seed {it['seed']}: c = {c} whole and at most 100")
    num_item(it, c, {'forgot-the-root': a**2 + b**2, 'added-the-sides': a + b})


def l1_short(it, V):
    a, b = triple(V)
    c = sp.sqrt(a**2 + b**2)
    check(f"hypotenuse {c} and one short side {a}." in it['prompt'], f"short-side-whole seed {it['seed']}: prompt")
    other = sp.solve(sp.Eq(a**2 + B**2, c**2), B)[0]
    num_item(it, other, {'added-the-squares': sp.sqrt(c**2 + a**2), 'took-away-sides': c - a})


def l1_hyp_dp(it, V):
    a, b = V['a'], V['b']
    c = sp.solve(sp.Eq(C**2, a**2 + b**2), C)[0]
    check(not c.is_integer and f"{float(c):.2f}" == it['accept'], f"hypotenuse-2-dp seed {it['seed']}: not whole, accept {float(c):.2f}")
    num_item(it, c, {'forgot-the-root': a**2 + b**2, 'added-the-sides': a + b})


def l1_short_dp(it, V):
    c, h = V['c'], V['h']
    a = 2 + h % (c - 2)
    check(f"hypotenuse {c} and one short side {a}." in it['prompt'], f"short-side-2-dp seed {it['seed']}: prompt")
    b = sp.solve(sp.Eq(a**2 + B**2, c**2), B)[0]
    check(not b.is_integer and f"{float(b):.2f}" == it['accept'], f"short-side-2-dp seed {it['seed']}: accept {float(b):.2f}")
    num_item(it, b, {'added-the-squares': sp.sqrt(c**2 + a**2), 'forgot-the-root': c**2 - a**2})


# ---- l3-sides-and-angles -------------------------------------------------------------------------
L3 = 'trig/fluency-l3-sides-and-angles'


def r4(x):
    return sp.Rational(str(round(float(x), 4)))


def given(it, t, names):
    vals = {'sin': r4(sp.sin(t * DEG)), 'cos': r4(sp.cos(t * DEG)), 'tan': r4(sp.tan(t * DEG))}
    for nm in names:
        check(f"$\\{nm} {t}^\\circ \\approx {float(vals[nm]):.4f}$" in it['prompt'], f"{it['family']} seed {it['seed']}: {nm} {t} given to 4 dp")
    return vals


def l3_side(it, V):
    h, t, w = V['h'], V['t'], V['w']
    g = given(it, t, ['sin', 'cos'])
    use, other = ('sin', 'cos') if w == 'opposite' else ('cos', 'sin')
    key = h * g[use]
    check(abs(float(h * getattr(sp, use)(t * DEG)) - float(key)) < 0.01, f"side-from-hypotenuse seed {it['seed']}: true side inside tolerance")
    num_item(it, key, {'other-ratio': h * g[other], 'divided-by-ratio': h / g[use]})


def l3_hyp(it, V):
    d, t, w = V['d'], V['t'], V['w']
    g = given(it, t, ['sin', 'cos'])
    use, other = ('sin', 'cos') if w == 'opposite' else ('cos', 'sin')
    key = d / g[use]
    check(abs(float(d / getattr(sp, use)(t * DEG)) - float(key)) < 0.01, f"hypotenuse-from-side seed {it['seed']}: true hypotenuse inside tolerance")
    num_item(it, key, {'multiplied-by-ratio': d * g[use], 'other-ratio': d / g[other]})


def l3_tan(it, V):
    a, t = V['a'], V['t']
    g = given(it, t, ['sin', 'tan'])
    key = a * g['tan']
    check(abs(float(a * sp.tan(t * DEG)) - float(key)) < 0.02, f"height-with-tan seed {it['seed']}: true height inside tolerance")
    num_item(it, key, {'used-sine': a * g['sin'], 'divided-by-tan': a / g['tan']})


# ---- l4-exact-values -----------------------------------------------------------------------------
L4 = 'trig/fluency-l4-exact-values'


def l4_side(it, V):
    c, t, w = V['c'], V['t'], V['w']
    h = 2 * c
    check(f"hypotenuse {h} and an angle of ${t}^\\circ$" in it['prompt'], f"side-from-hypotenuse seed {it['seed']}: prompt")
    f, g = (sp.sin, sp.cos) if w == 'opposite' else (sp.cos, sp.sin)
    key = h * f(t * DEG)
    expr_item(it, key, {'other-ratio': h * g(t * DEG), 'divided-by-ratio': h / f(t * DEG)})


def l4_tan(it, V):
    a, t = V['a'], V['t']
    key = a * sp.tan(t * DEG)
    expr_item(it, key, {'used-sine': a * sp.sin(t * DEG), 'divided-by-tan': a / sp.tan(t * DEG)})


def l4_45(it, V):
    c, e = V['c'], V['e']
    hyp = c * sp.sqrt(2) if e == 1 else sp.Integer(c)
    shown = f"\\sqrt{{2}}" if (e == 1 and c == 1) else (f"{c}\\sqrt{{2}}" if e == 1 else f"{c}")
    check(f"hypotenuse ${shown}$" in it['prompt'], f"forty-five-triangle seed {it['seed']}: prompt shows {hyp}")
    leg = sp.solve(sp.Eq(2 * A**2, hyp**2), A)[0]
    check(sp.simplify(leg - hyp * sp.cos(45 * DEG)) == 0, f"forty-five-triangle seed {it['seed']}: leg = hyp cos 45")
    expr_item(it, leg, {'halved': hyp / 2, 'times-root-two': hyp * sp.sqrt(2)})


def l4_combine(it, V):
    p, q, t = V['p'], V['q'], V['t']
    a, b = 2 * p, 2 * q
    key = a * sp.sin(t * DEG) + b * sp.cos(t * DEG)
    swapped = a * sp.cos(t * DEG) + b * sp.sin(t * DEG)
    expr_item(it, key, {'swapped-values': swapped, 'dropped-halves': 2 * key})


# ---- l7-arc-length -------------------------------------------------------------------------------
L7 = 'trig/fluency-l7-arc-length'


def l7_d2r(it, V):
    d = V['d']
    k = sp.nsimplify(d * DEG / sp.pi)
    num_item(it, k, {'upside-down': 1 / k, 'used-a-full-turn': sp.Rational(d, 360)})


def l7_d2r_exact(it, V):
    """Widening pass: the exact radian measure, a multiple of pi in lowest terms."""
    d = V['d']
    theta = sp.nsimplify(d * DEG)
    k = theta / sp.pi
    p, q = sp.fraction(k)
    check(f"${d}^\\circ$ in radians, exactly" in it['prompt'], f"degrees-to-radians-exact seed {it['seed']}: prompt")
    check(it['answer'] == (f"\\frac{{\\pi}}{{{q}}}" if p == 1 else f"\\frac{{{p}\\pi}}{{{q}}}") and q > 1 and sp.gcd(p, q) == 1,
          f"degrees-to-radians-exact seed {it['seed']}: key {it['answer']} is {theta} in lowest terms")
    expr_item(it, theta, {'upside-down': sp.pi / k, 'used-a-full-turn': sp.Rational(d, 360) * sp.pi})


def l7_r2d(it, V):
    q, h = V['q'], V['h']
    p = 1 + h % (2 * q - 1)
    theta = sp.Rational(p, q) * sp.pi
    shown = f"\\frac{{\\pi}}{{{q}}}" if p == 1 else f"\\frac{{{p}\\pi}}{{{q}}}"
    check(shown in it['prompt'] and sp.gcd(p, q) == 1, f"radians-to-degrees seed {it['seed']}: prompt shows {theta}")
    deg = sp.nsimplify(theta / DEG)
    num_item(it, deg, {'used-a-full-turn': 2 * deg, 'dropped-pi': sp.Rational(p, q) / DEG})


def l7_r2d_dp(it, V):
    x = sp.Rational(V['j'], 20)
    deg = x / DEG
    check(f"{float(deg):.1f}" == it['accept'], f"radians-to-degrees-1-dp seed {it['seed']}: accept {float(deg):.1f}")
    num_item(it, deg, {'wrong-way-round': x * DEG, 'used-a-full-turn': 2 * deg})


def l7_arc(it, V):
    r, d = V['r'], V['d']
    s = r * d * DEG
    check(f"{float(s):.2f}" == it['accept'], f"arc-length seed {it['seed']}: accept {float(s):.2f}")
    num_item(it, s, {'used-degrees': r * d, 'wrong-way-round': r * d / DEG})


JOBS = [
    (L1, 'hypotenuse-whole', l1_hyp), (L1, 'short-side-whole', l1_short),
    (L1, 'hypotenuse-2-dp', l1_hyp_dp), (L1, 'short-side-2-dp', l1_short_dp),
    (L3, 'side-from-hypotenuse', l3_side), (L3, 'hypotenuse-from-side', l3_hyp), (L3, 'height-with-tan', l3_tan),
    (L4, 'side-from-hypotenuse', l4_side), (L4, 'height-with-tan', l4_tan),
    (L4, 'forty-five-triangle', l4_45), (L4, 'combine-values', l4_combine),
    (L7, 'degrees-to-radians', l7_d2r), (L7, 'degrees-to-radians-exact', l7_d2r_exact), (L7, 'radians-to-degrees', l7_r2d),
    (L7, 'radians-to-degrees-1-dp', l7_r2d_dp), (L7, 'arc-length', l7_arc),
]

for ref, fam, fn in JOBS:
    run(ref, fam, fn)
print(f"{len(JOBS)} families, {N} draws each, {count} checks")
lv.report()
