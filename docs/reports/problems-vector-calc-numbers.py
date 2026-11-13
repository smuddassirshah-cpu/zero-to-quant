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
    return integrate.quad(lambda s: float(np.dot(F(*r(s)), d1(r, s))), a0, b0, limit=200, epsabs=1e-10, epsrel=1e-10)[0]


def scalar(f, r, a0, b0):
    return integrate.quad(lambda s: f(*r(s)) * float(np.linalg.norm(d1(r, s))), a0, b0, limit=200, epsabs=1e-10, epsrel=1e-10)[0]


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

# ---------------------------------------------------------------- level 2
def loop_work(F, verts):
    """work of F anticlockwise round a polygon, by quad along each straight edge"""
    tot = 0.0
    for A, B in zip(verts, verts[1:] + verts[:1]):
        tot += work(F, lambda s, A=A, B=B: (A[0] + s * (B[0] - A[0]), A[1] + s * (B[1] - A[1])), 0, 1)
    return tot


def edge_flux(F, A, B):
    """outward flux across a straight edge of an anticlockwise boundary: integral of P dy - Q dx"""
    r = lambda s: (A[0] + s * (B[0] - A[0]), A[1] + s * (B[1] - A[1]))
    def g(s):
        X, Y = r(s); d = d1(r, s); P, Q = F(X, Y)
        return P * d[1] - Q * d[0]
    return integrate.quad(g, 0, 1, epsabs=1e-10, epsrel=1e-10)[0]


if 2 in SETS:
    # Q1 rectangle [0,3]x[0,1], F = (y^3 - 4y, xy^2 + 2x)
    P, Q = y**3 - 4 * y, x * y**2 + 2 * x
    Fn = lambda X, Y: (Y**3 - 4 * Y, X * Y**2 + 2 * X)
    curl = sp.expand(sp.diff(Q, x) - sp.diff(P, y))
    expr(2, 'p-rectangle-edges', 1, curl, {'reversed': -curl, 'div': sp.diff(P, x) + sp.diff(Q, y)})
    circ = sp.integrate(curl, (y, 0, 1), (x, 0, 3))
    circn = loop_work(Fn, [(0, 0), (3, 0), (3, 1), (0, 1)])
    num(2, 'p-rectangle-edges', 2, circ, circn, {'reversed': -circ, 'axes': sp.integrate(curl, (y, 0, 3), (x, 0, 1)), 'const': 6 * 3})
    right = sp.integrate(Q.subs(x, 3), (y, 0, 1))
    rightn = work(Fn, lambda s: (3, s), 0, 1)
    num(2, 'p-rectangle-edges', 3, right, rightn, {'drop-2x': sp.integrate((x * y**2).subs(x, 3), (y, 0, 1))})
    bottom = work(Fn, lambda s: (3 * s, 0), 0, 1); left = work(Fn, lambda s: (0, 1 - s), 0, 1)
    ok(abs(bottom) < 1e-12 and abs(left) < 1e-12, 'L2 Q1 bottom and left edges give 0')
    top = circ - right
    topn = work(Fn, lambda s: (3 - 3 * s, 1), 0, 1)
    num(2, 'p-rectangle-edges', 4, top, topn, {'direction': -top, 'added': circ + right})
    text(2, 'p-rectangle-edges', 2, '3\\left(6 - \\tfrac23\\right) = 16')
    text(2, 'p-rectangle-edges', 4, '16 - 0 - 7 - 0 = 9', '\\int_3^0 (-3)\\,dx = 9')

    # Q2 cycloid arch (t - sin t, 1 - cos t)
    X_, Y_ = t - sp.sin(t), 1 - sp.cos(t)
    g = sp.expand(Y_ * sp.diff(X_, t))
    expr(2, 'p-cycloid-arch', 1, g, {'no-derivative': Y_ * X_, 'sign': -g})
    A = -(0 + sp.integrate(g, (t, 2 * sp.pi, 0)))          # -oint y dx: axis gives 0, arch run backwards
    rc = lambda s: (s - np.sin(s), 1 - np.cos(s))
    # second method: area by a direct double integral, x as a function of y is awkward, so integrate y over the arch in x
    An = integrate.quad(lambda s: (1 - np.cos(s)) * (1 - np.cos(s)), 0, 2 * PI)[0]   # integral of y dx with x' taken from the curve
    An2 = integrate.quad(lambda s: rc(s)[1] * d1(rc, s)[0], 0, 2 * PI)[0]
    ok(abs(An - An2) < 1e-6, 'L2 Q2 area two quads agree')
    ok(sp.simplify(A - 3 * sp.pi) == 0, 'L2 Q2 area 3 pi')
    num(2, 'p-cycloid-arch', 2, A, An2, {'sign': -A, 'cos-sq': 2 * sp.pi, 'square': sp.integrate(1 - sp.cos(t)**2, (t, 0, 2 * sp.pi))}, rounded=9.42)
    Pm = -y**2 / 2
    ok(sp.simplify(-sp.diff(Pm, y) - y) == 0, 'L2 Q2 -P_y = y')
    expr(2, 'p-cycloid-arch', 3, Pm, {'sign': -Pm, 'no-half': -y**2})
    My = sp.integrate(Pm.subs(y, Y_) * sp.diff(X_, t), (t, 2 * sp.pi, 0))
    # second method: double integral of y under the arch, as integral over the arch of y^2/2 dx
    Myn = integrate.quad(lambda s: 0.5 * rc(s)[1]**2 * d1(rc, s)[0], 0, 2 * PI)[0]
    ok(sp.simplify(My - 5 * sp.pi / 2) == 0, 'L2 Q2 moment 5 pi / 2')
    num(2, 'p-cycloid-arch', 4, My, Myn, {'no-half': 2 * My, 'sign': -My}, rounded=7.85)
    ybar = My / A
    num(2, 'p-cycloid-arch', 5, ybar, Myn / An2, {'inverse': A / My, 'no-half': 2 * My / A}, rounded=0.833)
    text(2, 'p-cycloid-arch', 2, '3\\pi \\approx 9.42')
    text(2, 'p-cycloid-arch', 4, '\\tfrac{5\\pi}{2} \\approx 7.85')

    # Q3 triangle (0,0),(4,0),(0,2), F = (x^2 + y, 2xy)
    P, Q = x**2 + y, 2 * x * y
    Fn = lambda X, Y: (X**2 + Y, 2 * X * Y)
    div = sp.diff(P, x) + sp.diff(Q, y)
    expr(2, 'p-triangle-flux', 1, div, {'curl': sp.diff(Q, x) - sp.diff(P, y), 'only-p': sp.diff(P, x)})
    flux = sp.integrate(div, (y, 0, 2 - x / 2), (x, 0, 4))
    V = [(0, 0), (4, 0), (0, 2)]
    fluxn = sum(edge_flux(Fn, A_, B_) for A_, B_ in zip(V, V[1:] + V[:1]))
    curl = sp.diff(Q, x) - sp.diff(P, y)
    num(2, 'p-triangle-flux', 2, flux, fluxn, {'curl': sp.integrate(curl, (y, 0, 2 - x / 2), (x, 0, 4)),
                                               'rectangle': sp.integrate(div, (y, 0, 2), (x, 0, 4)),
                                               'only-p': sp.integrate(2 * x, (y, 0, 2 - x / 2), (x, 0, 4))}, rounded=21.33)
    leftf = sp.integrate(-P.subs(x, 0), (y, 0, 2))
    num(2, 'p-triangle-flux', 3, leftf, edge_flux(Fn, (0, 2), (0, 0)), {'sign': -leftf, 'tangent': 0})
    ok(abs(edge_flux(Fn, (0, 0), (4, 0))) < 1e-12, 'L2 Q3 bottom edge flux 0')
    longf = flux - leftf
    num(2, 'p-triangle-flux', 4, longf, edge_flux(Fn, (4, 0), (0, 2)), {'add-edge': flux + leftf, 'all-out': flux}, rounded=23.33)
    text(2, 'p-triangle-flux', 2, '64 - \\tfrac{128}{3} = \\tfrac{64}{3}', '\\tfrac{64}{3} \\approx 21.33')
    text(2, 'p-triangle-flux', 4, '\\tfrac{70}{3} \\approx 23.33')

    # Q4 quadrilateral (0,0),(5,1),(4,5),(1,3), F = (2x - 4y, x + y)
    V = [(0, 0), (5, 1), (4, 5), (1, 3)]
    edges = [x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(V, V[1:] + V[:1])]
    plus = [x1 * y2 + x2 * y1 for (x1, y1), (x2, y2) in zip(V, V[1:] + V[:1])]
    xdy = lambda A_, B_: work(lambda X, Y: (-Y, X), lambda s: (A_[0] + s * (B_[0] - A_[0]), A_[1] + s * (B_[1] - A_[1])), 0, 1)
    num(2, 'p-quadrilateral-plot', 1, edges[1], xdy(V[1], V[2]), {'swap': -edges[1], 'plus': plus[1]})
    area = sp.Rational(sum(edges), 2)
    arean = 0.5 * loop_work(lambda X, Y: (-Y, X), V)
    ok(all(e > 0 for e in [5 * 4 - 1 * (-1), (-1) * (-2) - 4 * (-3), (-3) * (-3) - (-2) * (-1), (-1) * 1 - (-3) * 5]), 'L2 Q4 convex and anticlockwise')
    num(2, 'p-quadrilateral-plot', 2, area, arean, {'no-half': 2 * area, 'plus': sp.Rational(sum(plus), 2)})
    Fn = lambda X, Y: (2 * X - 4 * Y, X + Y)
    P, Q = 2 * x - 4 * y, x + y
    div, curl = sp.diff(P, x) + sp.diff(Q, y), sp.diff(Q, x) - sp.diff(P, y)
    fluxn = sum(edge_flux(Fn, A_, B_) for A_, B_ in zip(V, V[1:] + V[:1]))
    num(2, 'p-quadrilateral-plot', 3, div * area, fluxn, {'curl': curl * area, 'no-half': div * 2 * area})
    num(2, 'p-quadrilateral-plot', 4, curl * area, loop_work(Fn, V), {'div': div * area, 'reversed': -curl * area,
                                                                       'plus': (sp.diff(Q, x) + sp.diff(P, y)) * area})
    text(2, 'p-quadrilateral-plot', 2, '0 + 21 + 7 + 0 = 28', '4 \\times 3 - 1 \\times 5 = 7')

    L = Level('vector-calc', 2)
    L.check_wrongs('problems')
    bad = [r for r in L.results if not r[0]]
    ok(not bad, f'L2 numbers_lib check_wrongs: {len(bad)} failures')

# ---------------------------------------------------------------- level 3
def surf_flux(F, r, u0, u1, v0, v1):
    """flux of F through r(u, v) with normal r_u x r_v, both partials by central differences, by dblquad"""
    h = 1e-6
    def g(vv, uu):
        ru = (np.array(r(uu + h, vv)) - np.array(r(uu - h, vv))) / (2 * h)
        rv = (np.array(r(uu, vv + h)) - np.array(r(uu, vv - h))) / (2 * h)
        return float(np.dot(F(*r(uu, vv)), np.cross(ru, rv)))
    return integrate.dblquad(g, u0, u1, v0, v1, epsabs=1e-9, epsrel=1e-9)[0]


def surf_area(r, u0, u1, v0, v1):
    h = 1e-6
    def g(vv, uu):
        ru = (np.array(r(uu + h, vv)) - np.array(r(uu - h, vv))) / (2 * h)
        rv = (np.array(r(uu, vv + h)) - np.array(r(uu, vv - h))) / (2 * h)
        return float(np.linalg.norm(np.cross(ru, rv)))
    return integrate.dblquad(g, u0, u1, v0, v1, epsabs=1e-9, epsrel=1e-9)[0]


def curl3(F):
    P, Q, R = F
    return sp.Matrix([sp.diff(R, y) - sp.diff(Q, z), sp.diff(P, z) - sp.diff(R, x), sp.diff(Q, x) - sp.diff(P, y)])


def div3(F):
    return sp.diff(F[0], x) + sp.diff(F[1], y) + sp.diff(F[2], z)


def work3(F, r, a0, b0):
    return integrate.quad(lambda s: float(np.dot(F(*r(s)), d1(r, s))), a0, b0, limit=200, epsabs=1e-10, epsrel=1e-10)[0]


if 3 in SETS:
    # R1 saddle z = xy over x^2 + y^2 <= 3, polar parameters (rho, theta)
    rr, th = sp.symbols('rr th', positive=True)
    R = sp.Matrix([x, y, x * y])
    N = R.diff(x).cross(R.diff(y))
    expr(3, 'p-saddle-roof', 1, tuple(N), {'sign': (y, x, sp.Integer(1)), 'swap': (-x, -y, sp.Integer(1))})
    nN = sp.sqrt(sp.expand(N.dot(N)))
    expr(3, 'p-saddle-roof', 2, nN, {'no-root': sp.expand(N.dot(N)), 'no-one': sp.sqrt(x**2 + y**2)})
    pol = {x: rr * sp.cos(th), y: rr * sp.sin(th)}
    area = sp.integrate(sp.integrate(sp.simplify(nN.subs(pol)) * rr, (rr, 0, sp.sqrt(3))), (th, 0, 2 * sp.pi))
    rp = lambda q, w: (q * np.cos(w), q * np.sin(w), q * np.cos(w) * q * np.sin(w))
    arean = surf_area(rp, 0, np.sqrt(3), 0, 2 * PI)
    no_r = 2 * sp.pi * sp.integrate(sp.sqrt(1 + rr**2), (rr, 0, sp.sqrt(3)))
    ok(sp.simplify(area - 14 * sp.pi / 3) == 0, 'L3 R1 area 14 pi / 3')
    num(3, 'p-saddle-roof', 3, area, arean, {'no-r': no_r, 'flat': 3 * sp.pi}, rounded=14.66, agree=1e-6)
    Fv = sp.Matrix([y, x, 5])
    fl = sp.integrate(sp.integrate(sp.expand(Fv.dot(N)).subs(pol) * rr, (rr, 0, sp.sqrt(3))), (th, 0, 2 * sp.pi))
    fln = surf_flux(lambda X, Y, Z: (Y, X, 5), rp, 0, np.sqrt(3), 0, 2 * PI)
    zonly = 5 * 3 * sp.pi
    signn = sp.integrate(sp.integrate(sp.expand(Fv.dot(sp.Matrix([y, x, 1]))).subs(pol) * rr, (rr, 0, sp.sqrt(3))), (th, 0, 2 * sp.pi))
    num(3, 'p-saddle-roof', 4, fl, fln, {'down': -fl, 'z-only': zonly, 'sign-normal': signn}, rounded=32.99, agree=1e-6)
    text(3, 'p-saddle-roof', 3, '\\tfrac{14\\pi}{3} \\approx 14.66', '\\tfrac73')
    text(3, 'p-saddle-roof', 4, '\\tfrac{21\\pi}{2} \\approx 32.99', '\\tfrac{9\\pi}{2}')

    # R2 open tank [0,4]x[0,1]x[0,2], F = (xz, y^2, 3z)
    F = sp.Matrix([x * z, y**2, 3 * z]); Fn = lambda X, Y, Z: (X * Z, Y**2, 3 * Z)
    dv = div3(F)
    expr(3, 'p-open-tank', 1, dv, {'wrong-var': x + 2 * y + 3, 'drop-const': z + 2 * y})
    box = lambda e: sp.integrate(e, (x, 0, 4), (y, 0, 1), (z, 0, 2))
    tot = box(dv)
    totn = integrate.tplquad(lambda Z, Y, X: Z + 2 * Y + 3, 0, 4, 0, 1, 0, 2)[0]
    # third method: the six faces one by one with dblquad of F . n
    faces = {
        'x0': integrate.dblquad(lambda Z, Y: -Fn(0, Y, Z)[0], 0, 1, 0, 2)[0], 'x4': integrate.dblquad(lambda Z, Y: Fn(4, Y, Z)[0], 0, 1, 0, 2)[0],
        'y0': integrate.dblquad(lambda Z, X: -Fn(X, 0, Z)[1], 0, 4, 0, 2)[0], 'y1': integrate.dblquad(lambda Z, X: Fn(X, 1, Z)[1], 0, 4, 0, 2)[0],
        'z0': integrate.dblquad(lambda Y, X: -Fn(X, Y, 0)[2], 0, 4, 0, 1)[0], 'z2': integrate.dblquad(lambda Y, X: Fn(X, Y, 2)[2], 0, 4, 0, 1)[0]}
    ok(abs(sum(faces.values()) - float(tot)) < 1e-8, 'L3 R2 six faces add to the divergence integral')
    num(3, 'p-open-tank', 2, tot, totn, {'drop-const': box(z + 2 * y), 'wrong-var': box(x + 2 * y + 3)})
    lid = F[2].subs(z, 2) * 4
    num(3, 'p-open-tank', 3, lid, faces['z2'], {'wrong-area': F[2].subs(z, 2) * 8, 'no-z': 3 * 4})
    walls = tot - lid
    num(3, 'p-open-tank', 4, walls, sum(v for kf, v in faces.items() if kf != 'z2'), {'added': tot + lid, 'from-16': box(z + 2 * y) - lid})
    ok(abs(faces['x4'] - 8) < 1e-9 and abs(faces['y1'] - 8) < 1e-9, 'L3 R2 walls x = 4 and y = 1 give 8 each')
    text(3, 'p-open-tank', 2, '8 + 8 + 24 = 40')
    text(3, 'p-open-tank', 4, '40 - 24 = 16')

    # R3 plane z = 2 - x inside x^2 + y^2 = 4, F = (-yz, xz, xy + 3y)
    F = sp.Matrix([-y * z, x * z, x * y + 3 * y])
    cF = curl3(F)
    expr(3, 'p-slanted-ellipse', 1, tuple(cF), {'reversed': tuple(-cF), 'half': (sp.Integer(3), -y, z)})
    S = sp.Matrix([x, y, 2 - x]); N = S.diff(x).cross(S.diff(y))
    expr(3, 'p-slanted-ellipse', 2, tuple(N), {'fx': (sp.Integer(-1), sp.Integer(0), sp.Integer(1)), 'down': (sp.Integer(-1), sp.Integer(0), sp.Integer(-1))})
    integrand = sp.expand(cF.dot(N).subs(z, 2 - x))
    expr(3, 'p-slanted-ellipse', 3, integrand, {'z-left': 3 + 2 * z, 'fx': sp.expand(cF.dot(sp.Matrix([-1, 0, 1])).subs(z, 2 - x))})
    disc = lambda e, rad=2: sp.integrate(sp.integrate(sp.expand(e).subs(pol) * rr, (rr, 0, rad)), (th, 0, 2 * sp.pi))
    circ = disc(integrand)
    Fn = lambda X, Y, Z: (-Y * Z, X * Z, X * Y + 3 * Y)
    circn = work3(Fn, lambda s: (2 * np.cos(s), 2 * np.sin(s), 2 - 2 * np.cos(s)), 0, 2 * PI)
    ok(sp.simplify(circ - 28 * sp.pi) == 0, 'L3 R3 circulation 28 pi')
    num(3, 'p-slanted-ellipse', 4, circ, circn, {'fx': disc(1 - 2 * x), 'unit-disc': disc(integrand, 1), 'extra-root': circ * sp.sqrt(2)}, rounded=87.96)
    c = sp.Symbol('c')
    Fc = sp.Matrix([-y * z, x * z, x * y + c * y])
    circ_c = disc(curl3(Fc).dot(N).subs(z, 2 - x))
    cs = sp.solve(sp.Eq(circ_c, 0), c)
    ok(cs == [-4], f'L3 R3 c = {cs}')
    cn = work3(lambda X, Y, Z: (-Y * Z, X * Z, X * Y - 4 * Y), lambda s: (2 * np.cos(s), 2 * np.sin(s), 2 - 2 * np.cos(s)), 0, 2 * PI)
    num(3, 'p-slanted-ellipse', 5, cs[0], -4 + cn, {'sign': -cs[0]}, agree=1e-6)
    ok(sp.simplify(circ_c - 4 * sp.pi * (c + 4)) == 0, 'L3 R3 circulation 4 pi (c + 4)')
    text(3, 'p-slanted-ellipse', 4, '28\\pi \\approx 87.96')

    # R4 can x^2 + y^2 = 16, 0 <= z <= 2, F = (2y - z^2, x + xz + 3z, xy)
    F = sp.Matrix([2 * y - z**2, x + x * z + 3 * z, x * y])
    Fn = lambda X, Y, Z: (2 * Y - Z**2, X + X * Z + 3 * Z, X * Y)
    cF = curl3(F)
    slipF = sp.Matrix([cF[0] + x, cF[1], cF[2]])                    # Q_z taken as 3, not x + 3
    expr(3, 'p-can-curl', 1, tuple(cF), {'reversed': tuple(-cF), 'qz-slip': tuple(slipF)})
    dc = sp.simplify(div3(cF))
    num(3, 'p-can-curl', 2, dc, 0, {'qz-slip': div3(slipF)})
    base = work3(Fn, lambda s: (4 * np.cos(s), 4 * np.sin(s), 0), 0, 2 * PI)
    base_s = disc(cF[2].subs(z, 0), 4)
    num(3, 'p-can-curl', 3, base_s, base, {'sign': -base_s, 'radius': cF[2].subs(z, 0) * 4 * sp.pi}, rounded=-50.27)
    cFn = sp.lambdify((x, y, z), list(cF), 'numpy')
    lid_s = disc(cF[2].subs(z, 2), 4)
    lidn = surf_flux(lambda X, Y, Z: cFn(X, Y, Z), lambda q, w: (q * np.cos(w), q * np.sin(w), 2.0), 0, 4, 0, 2 * PI)
    num(3, 'p-can-curl', 4, lid_s, lidn, {'z0': -lid_s, 'radius': 4 * sp.pi}, rounded=50.27, agree=1e-6)
    side = 0 - lid_s - (-base_s)        # total 0 = side + lid + base(outward, normal down) with base outward = -base_s
    # independent: the side by dblquad on (4cos w, 4sin w, h), outward normal r_w x r_h
    siden = surf_flux(lambda X, Y, Z: cFn(X, Y, Z), lambda w, hh: (4 * np.cos(w), 4 * np.sin(w), hh), 0, 2 * PI, 0, 2)
    num(3, 'p-can-curl', 5, side, siden, {'added': 0 - lid_s - base_s, 'sign': -side, 'no-base': -lid_s}, rounded=-100.53, agree=1e-6)
    ok(sp.simplify(side + 32 * sp.pi) == 0, 'L3 R4 side -32 pi')
    text(3, 'p-can-curl', 3, '-16\\pi \\approx -50.27', '-32\\sin^2 t + 16\\cos^2 t')
    text(3, 'p-can-curl', 5, '-32\\pi \\approx -100.53')

    L = Level('vector-calc', 3)
    L.check_wrongs('problems')
    bad = [r_ for r_ in L.results if not r_[0]]
    ok(not bad, f'L3 numbers_lib check_wrongs: {len(bad)} failures')

print(f'{checks - len(fails)} of {checks} checks passed')
sys.exit(1 if fails else 0)
