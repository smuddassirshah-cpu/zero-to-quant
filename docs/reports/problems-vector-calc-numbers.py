"""Recompute every number in app/content/courses/vector-calc/problems-1.json to problems-3.json twice.

Method 1 is exact: sympy integrates the integrand worked out by hand (or the field along the curve), solves and
simplifies. Method 2 is independent: scipy quad (or dblquad / tplquad) integrates the field itself along the
parametrised curve or surface, with the derivative taken by a central difference, never by the hand formula.
For each numeric part: the two methods agree, the JSON key lies within its tol of the value, the rounding the question
asks for is accepted, every `wrong` value equals its named slip recomputed here, has a byKey line and lies outside the
key's band (and outside every other slip's band). Expression parts: the key and every accepted form equal the sympy
truth at random points and every wrong form differs. Choice parts: the keyed option is the expected one. Stated
figures in feedback and explain are checked as text. numbers_lib.Level.check_wrongs runs over each set as well.
Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-vector-calc-numbers.py
"""
import json, os, re, sys, random
import sympy as sp
import numpy as np
from scipy import integrate

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
COURSE = os.path.join(ROOT, 'app', 'content', 'courses', 'vector-calc')
sys.path.insert(0, os.path.join(ROOT, 'app', 'tools'))
from numbers_lib import Level  # noqa: E402
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,  # noqa: E402
                                        implicit_multiplication_application, convert_xor)

fails, checks = [], 0
x, y, z, t, k, u, v, a = sp.symbols('x y z t k u v a', real=True)
LEVELS = [n for n in (1, 2, 3) if os.path.exists(os.path.join(COURSE, f'problems-{n}.json'))]


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)
        print('BAD', msg)


SETS = {}
for lv in LEVELS:
    d = json.load(open(os.path.join(COURSE, f'problems-{lv}.json'), encoding='utf8'))
    SETS[lv] = {it['id']: it for it in d['items']}


def part(lv, iid, p):
    return SETS[lv][iid]['parts'][p - 1]


def band(w):
    return w['tol']['abs']


def num(lv, iid, p, exact, alt, slips, rounded=None, agree=1e-7):
    """exact, alt: the value two ways. slips: {wrong id: recomputed value}. rounded: the figure the asked rounding gives."""
    pt = part(lv, iid, p)
    w, tag = pt['widget'], f'L{lv} {iid} p{p}'
    ok(w['kind'] == 'numeric', f'{tag} is numeric')
    exact, alt = float(exact), float(alt)
    ok(abs(exact - alt) <= agree * max(1, abs(exact)), f'{tag} methods agree {exact} vs {alt}')
    tol = band(w)
    ok(abs(w['answer'] - exact) <= tol, f'{tag} key {w["answer"]} within {tol} of {exact}')
    if rounded is not None:
        ok(abs(rounded - w['answer']) <= tol + 1e-12, f'{tag} rounded {rounded} accepted')
    ids = {e['id']: e for e in w.get('wrong', [])}
    ok(set(ids) == set(slips), f'{tag} wrong ids {sorted(ids)} match slips {sorted(slips)}')
    byk = pt['feedback'].get('byKey', {})
    for wid, val in slips.items():
        if wid not in ids:
            continue
        e = ids[wid]
        val = float(val)
        ok(abs(e['value'] - val) <= e['tol']['abs'], f'{tag} wrong {wid} {e["value"]} matches slip {val}')
        ok(abs(e['value'] - w['answer']) > tol + e['tol']['abs'], f'{tag} wrong {wid} outside key band')
        ok(wid in byk, f'{tag} wrong {wid} has a byKey line')
        for oid, o in ids.items():
            if oid != wid:
                ok(abs(e['value'] - o['value']) > e['tol']['abs'] + o['tol']['abs'], f'{tag} wrong {wid} band clear of {oid}')
    return exact


def tex2sym(s):
    s = s.replace('\\left', '').replace('\\right', '').replace('\\,', '')
    s = re.sub(r'\\(sin|cos)\^(\d)\((\w)\)', r'(\\\1(\3))^\2', s)
    s = re.sub(r'\\(sin|cos)\^(\d) (\w)', r'(\\\1(\3))^\2', s)
    s = re.sub(r'\\(sin|cos) (\w)', r'\\\1(\2)', s)
    while '\\frac' in s:
        s = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', s)
    while '\\sqrt' in s:
        s = re.sub(r'\\sqrt\{([^{}]*)\}', r'sqrt(\1)', s)
    s = s.replace('\\pi', ' pi ').replace('\\sin', ' sin').replace('\\cos', ' cos').replace('\\cdot', '*')
    s = s.replace('\\theta', ' theta ').replace('\\phi', ' phi ')
    s = s.replace('{', '(').replace('}', ')')
    tr = standard_transformations + (implicit_multiplication_application, convert_xor)
    loc = {'x': x, 'y': y, 'z': z, 't': t, 'k': k, 'u': u, 'v': v, 'a': a, 'pi': sp.pi,
           'theta': sp.Symbol('theta', real=True), 'phi': sp.Symbol('phi', real=True)}
    s = s.strip()
    if s.startswith('(') and ',' in s and s.endswith(')') and s.count('(') == 1:
        return tuple(parse_expr(c, local_dict=loc, transformations=tr) for c in s[1:-1].split(','))
    return parse_expr(s, local_dict=loc, transformations=tr)


def same(e1, e2):
    if isinstance(e1, tuple) or isinstance(e2, tuple):
        return isinstance(e1, tuple) and isinstance(e2, tuple) and len(e1) == len(e2) and all(same(p, q) for p, q in zip(e1, e2))
    d = sp.simplify(e1 - e2)
    if d == 0:
        return True
    syms = sorted(d.free_symbols, key=str)
    rnd = random.Random(7)
    for _ in range(6):
        val = complex(d.subs({s: rnd.uniform(0.3, 3) for s in syms}).evalf())
        if abs(val) > 1e-9:
            return False
    return True


def expr(lv, iid, p, truth, slips):
    """truth: sympy value; slips: {wrong id: sympy value of the slip}."""
    pt = part(lv, iid, p)
    w, tag = pt['widget'], f'L{lv} {iid} p{p}'
    ok(w['kind'] == 'expression', f'{tag} is expression')
    for form in [w['answer']] + list(w.get('accept') or []):
        ok(same(tex2sym(form), truth), f'{tag} form {form!r} equals truth')
    ids = {e['id']: e for e in w.get('wrong', [])}
    ok(set(ids) == set(slips), f'{tag} wrong ids {sorted(ids)} match slips {sorted(slips)}')
    byk = pt['feedback'].get('byKey', {})
    for wid, val in slips.items():
        if wid in ids:
            e = tex2sym(ids[wid]['tex'])
            ok(same(e, val), f'{tag} wrong {wid} equals its slip')
            ok(not same(e, truth), f'{tag} wrong {wid} differs from the key')
            ok(wid in byk, f'{tag} wrong {wid} has a byKey line')


def choice(lv, iid, p, key_id, n_opts):
    pt = part(lv, iid, p)
    w, tag = pt['widget'], f'L{lv} {iid} p{p}'
    corr = [o['id'] for o in w['options'] if o.get('correct')]
    ok(corr == [key_id], f'{tag} keyed option {corr} is {key_id}')
    ok(len(w['options']) == n_opts and all(o.get('correct') or o.get('why') for o in w['options']), f'{tag} options have why')


def text(lv, iid, p, *phrases):
    pt = part(lv, iid, p)
    blob = json.dumps(pt, ensure_ascii=False).replace('\\\\', '\\')
    for ph in phrases:
        ok(ph in blob, f'L{lv} {iid} p{p} states {ph!r}')


def d1(f, s, h=1e-6):
    """central difference derivative of a vector function of one variable"""
    return (np.array(f(s + h)) - np.array(f(s - h))) / (2 * h)


def work(F, r, a0, b0):
    """quad of F(r(s)) . r'(s) with r' by central difference"""
    return integrate.quad(lambda s: float(np.dot(F(*r(s)), d1(r, s))), a0, b0, limit=200, epsabs=1e-11, epsrel=1e-11)[0]


def scalar(f, r, a0, b0):
    return integrate.quad(lambda s: f(*r(s)) * float(np.linalg.norm(d1(r, s))), a0, b0, limit=200, epsabs=1e-11, epsrel=1e-11)[0]


PI = float(sp.pi)

# ---------------------------------------------------------------- level 1
if 1 in SETS:
    # P1 bead on a semicircle, F = (2x - y, x + 2y), r = (3cos t, 3sin t), 0..pi
    F1 = lambda X, Y: (2 * X - Y, X + 2 * Y)
    r1 = lambda s: (3 * np.cos(s), 3 * np.sin(s))
    Fs = sp.Matrix([2 * x - y, x + 2 * y])
    mag = sp.sqrt(Fs.dot(Fs).subs({x: 1, y: 3}))
    num(1, 'p-bead-semicircle', 1, mag, np.hypot(*F1(1, 3)), {'sum': -1 + 7, 'no-root': 50, 'abs-sum': 8}, rounded=7.071)
    expr(1, 'p-bead-semicircle', 2, sp.expand(Fs.dot(Fs)), {'no-square': sp.expand(sum(Fs)), 'coef': 3 * x**2 + 3 * y**2})
    rs = sp.Matrix([3 * sp.cos(t), 3 * sp.sin(t)])
    Fr = Fs.subs({x: rs[0], y: rs[1]})
    speed = sp.sqrt(sp.simplify(rs.diff(t).dot(rs.diff(t))))
    I3 = sp.integrate(sp.sqrt(sp.simplify(Fr.dot(Fr))) * speed, (t, 0, sp.pi))
    I3n = scalar(lambda X, Y: np.hypot(*F1(X, Y)), r1, 0, PI)
    ok(sp.simplify(I3 - 9 * sp.sqrt(5) * sp.pi) == 0, 'L1 P1 p3 exact is 9 sqrt5 pi')
    num(1, 'p-bead-semicircle', 3, I3, I3n, {'no-speed': 3 * sp.sqrt(5) * sp.pi, 'squared': 45 * 3 * sp.pi, 'full-circle': 18 * sp.sqrt(5) * sp.pi}, rounded=63.22)
    dot = sp.simplify(Fr.dot(rs.diff(t)))
    ok(dot == 9, f'L1 P1 p4 dot is constant 9 ({dot})')
    num(1, 'p-bead-semicircle', 4, dot, np.dot(F1(*r1(0.7)), d1(r1, 0.7)), {'position': sp.simplify(Fr.dot(rs)), 'magnitude': sp.simplify(Fr.dot(Fr))}, agree=1e-6)
    W = sp.integrate(dot, (t, 0, sp.pi))
    Wn = work(F1, r1, 0, PI)
    num(1, 'p-bead-semicircle', 5, W / I3, Wn / I3n, {'inverse': I3 / W, 'no-integral': 9 / I3, 'full-circle': 2 * W / I3}, rounded=0.447)
    text(1, 'p-bead-semicircle', 1, '(-1, 7)', '\\sqrt{50} \\approx 7.071')
    text(1, 'p-bead-semicircle', 3, '9\\sqrt5\\,\\pi \\approx 63.22')
    text(1, 'p-bead-semicircle', 5, '9\\pi \\approx 28.27', '\\tfrac{1}{\\sqrt5} \\approx 0.447')
    ok(abs(float(W) - 28.27) < 0.005, 'L1 P1 9 pi rounds to 28.27')

    # P2 two routes, F = (xy, x + y), A: (t, t^3), B: (t, t)
    F2 = lambda X, Y: (X * Y, X + Y)
    Fs = sp.Matrix([x * y, x + y])
    rA = sp.Matrix([t, t**3]); rB = sp.Matrix([t, t])
    gA = sp.expand(Fs.subs({x: rA[0], y: rA[1]}).dot(rA.diff(t)))
    expr(1, 'p-two-routes-cubic', 1, gA, {'no-dot': sp.expand(sum(Fs.subs({x: t, y: t**3}))),
                                         'no-chain': sp.expand(Fs.subs({x: t, y: t**3}).dot(sp.Matrix([1, t**2])))})
    WA = sp.integrate(gA, (t, 0, 1)); WAn = work(F2, lambda s: (s, s**3), 0, 1)
    ok(WA == sp.Rational(29, 20), 'L1 P2 WA = 29/20')
    num(1, 'p-two-routes-cubic', 2, WA, WAn, {'no-dot': sp.integrate(t**4 + t**3 + t, (t, 0, 1)),
                                             'no-chain': sp.integrate(t**4 + t**3 + t**5, (t, 0, 1))}, rounded=1.45)
    gB = sp.expand(Fs.subs({x: t, y: t}).dot(rB.diff(t)))
    WB = sp.integrate(gB, (t, 0, 1)); WBn = work(F2, lambda s: (s, s), 0, 1)
    num(1, 'p-two-routes-cubic', 3, WB, WBn, {'ds': WB * sp.sqrt(2), 'p-only': sp.integrate(t**2, (t, 0, 1)), 'q-only': sp.integrate(2 * t, (t, 0, 1))}, rounded=1.333)
    loop = WA - WB
    loopn = work(F2, lambda s: (s, s**3), 0, 1) + work(F2, lambda s: (1 - s, 1 - s), 0, 1)
    ok(loop == sp.Rational(7, 60), 'L1 P2 loop = 7/60')
    num(1, 'p-two-routes-cubic', 4, loop, loopn, {'added': WA + WB, 'sign': -loop}, rounded=0.1167)
    ok(sp.diff(Fs[0], y) != sp.diff(Fs[1], x), 'L1 P2 P_y = x differs from Q_x = 1')
    choice(1, 'p-two-routes-cubic', 5, 'a', 4)
    text(1, 'p-two-routes-cubic', 2, '\\tfrac{29}{20} = 1.45')
    text(1, 'p-two-routes-cubic', 4, '\\tfrac{87 - 80}{60} = \\tfrac{7}{60} \\approx 0.1167')

    # P3 F = (3x^2 + y^2, 2xy), potential x^3 + xy^2
    Fs = sp.Matrix([3 * x**2 + y**2, 2 * x * y])
    expr(1, 'p-cubic-potential', 1, tuple(Fs.subs({x: 1, y: 2})), {'y-not-squared': (sp.Integer(5), sp.Integer(4)), 'swap': (sp.Integer(4), sp.Integer(7))})
    expr(1, 'p-cubic-potential', 2, sp.diff(Fs[0], y), {'px': sp.diff(Fs[0], x), 'qy': sp.diff(Fs[1], y)})
    ok(sp.diff(Fs[0], y) == sp.diff(Fs[1], x), 'L1 P3 P_y = Q_x')
    f = x**3 + x * y**2
    ok(sp.simplify(sp.Matrix([f.diff(x), f.diff(y)]) - Fs) == sp.zeros(2, 1), 'L1 P3 grad f = F')
    expr(1, 'p-cubic-potential', 3, f, {'double': x**3 + 2 * x * y**2, 'wrong-var': x**3 + x**2 * y})
    Wf = f.subs({x: 2, y: 3}) - f.subs({x: 1, y: 0})
    Wn = work(lambda X, Y: (3 * X**2 + Y**2, 2 * X * Y), lambda s: (1 + s, 3 * s**2), 0, 1)   # a curved path from (1,0) to (2,3)
    g2 = x**3 + 2 * x * y**2
    num(1, 'p-cubic-potential', 4, Wf, Wn, {'end-only': f.subs({x: 2, y: 3}), 'double': g2.subs({x: 2, y: 3}) - g2.subs({x: 1, y: 0})})
    text(1, 'p-cubic-potential', 4, '(8 + 18) - 1 = 25')

    # P4 family (y^2 + ky, 2xy + 3x), ellipse (2cos t, 5sin t)
    Fk = sp.Matrix([y**2 + k * y, 2 * x * y + 3 * x])
    ks = sp.solve(sp.Eq(sp.diff(Fk[0], y), sp.diff(Fk[1], x)), k)
    ok(ks == [3], f'L1 P4 k = {ks}')
    num(1, 'p-ellipse-family', 1, ks[0], 3, {'sign': -3})
    f = x * y**2 + 3 * x * y
    ok(sp.simplify(sp.Matrix([f.diff(x), f.diff(y)]) - Fk.subs(k, 3)) == sp.zeros(2, 1), 'L1 P4 grad f = F at k = 3')
    expr(1, 'p-ellipse-family', 2, f, {'double': 2 * f, 'missing': x * y**2})
    re_ = sp.Matrix([2 * sp.cos(t), 5 * sp.sin(t)])
    G = (Fk - sp.Matrix([f.diff(x), f.diff(y)])).subs(k, 1)
    gG = sp.simplify(G.subs({x: re_[0], y: re_[1]}).dot(re_.diff(t)))
    expr(1, 'p-ellipse-family', 3, gG, {'sign': -gG, 'position': sp.simplify(G.subs({x: re_[0], y: re_[1]}).dot(re_))})
    C1 = sp.integrate(gG, (t, 0, 2 * sp.pi))
    C1n = work(lambda X, Y: (Y**2 + Y, 2 * X * Y + 3 * X), lambda s: (2 * np.cos(s), 5 * np.sin(s)), 0, 2 * PI)
    num(1, 'p-ellipse-family', 4, C1, C1n, {'sign': -C1, 'sin-sq': 2 * C1}, rounded=62.83)
    Gk = (Fk - sp.Matrix([f.diff(x), f.diff(y)]))
    Ck = sp.simplify(sp.integrate(Gk.subs({x: re_[0], y: re_[1]}).dot(re_.diff(t)), (t, 0, 2 * sp.pi)))
    for kv in (-2, 0, 1, 3, 4.5):
        cn = work(lambda X, Y: (Y**2 + kv * Y, 2 * X * Y + 3 * X), lambda s: (2 * np.cos(s), 5 * np.sin(s)), 0, 2 * PI)
        ok(abs(float(Ck.subs(k, kv)) - cn) < 1e-6, f'L1 P4 p5 general k agrees with quad at k = {kv}')
    expr(1, 'p-ellipse-family', 5, Ck, {'sign': -Ck, 'constant': 20 * sp.pi})
    text(1, 'p-ellipse-family', 4, '20\\pi \\approx 62.83')

    L = Level('vector-calc', 1)
    L.check_wrongs('problems')
    bad = [r for r in L.results if not r[0]]
    ok(not bad, f'L1 numbers_lib check_wrongs: {len(bad)} failures')

print(f'{checks - len(fails)} of {checks} checks passed')
sys.exit(1 if fails else 0)
