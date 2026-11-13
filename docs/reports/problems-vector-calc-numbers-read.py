#!/usr/bin/env python3
"""Second reader's recompute for vector-calc problems-1 to -3 (docs/reviews/review-problems-vector-calc-1-3.md).

Imports nothing from the author's script. Every field, curve, region and surface is typed here from the prose.
Each line, surface and flux integral is done twice, exactly, with sympy:
  route 1  directly: parametrise the curve or surface and integrate;
  route 2  through the theorem the problem uses (Green, flux form, divergence, Stokes), or a second boundary form.
Every potential is checked by differentiation, every "conservative" claim by its curl on the whole plane.
Every wrong[] value is rebuilt from the slip its line names, shown outside the key band and clear of the other bands.
Every number after an "approx" sign in a feedback or explain string of a numeric part is checked against the key.

Run: <scratchpad>/venv/bin/python docs/reports/problems-vector-calc-numbers-read.py   (from the repo root; exit 0)
"""
import json, os, re, sys
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, split_symbols, convert_xor

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'vector-calc')
x, y, z, t, k, c, r, th, u = sp.symbols('x y z t k c r theta u', real=True)
pi, sqrt, sin, cos, Rat, integrate = sp.pi, sp.sqrt, sp.sin, sp.cos, sp.Rational, sp.integrate
n_ok = n_bad = 0


def chk(name, cond):
    global n_ok, n_bad
    if cond:
        n_ok += 1
    else:
        n_bad += 1
        print('FAIL  ' + name)


def same(a, b):
    return sp.simplify(sp.sympify(a) - sp.sympify(b)) == 0


SETS = {n: json.load(open(os.path.join(ROOT, 'problems-%d.json' % n))) for n in (1, 2, 3)}


def part(n, item, kpart):
    for it in SETS[n]['items']:
        if it['id'] == item:
            return it['parts'][kpart - 1]
    raise KeyError(item)


TR = standard_transformations + (split_symbols, implicit_multiplication_application, convert_xor)


def tex(s):
    """Small LaTeX reader for the keys of these three sets."""
    s = s.replace('\\left', '').replace('\\right', '').replace('\\cdot', '*').replace('\\,', '')
    s = re.sub(r'\\t?frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', s)
    s = re.sub(r'\\sqrt\{([^{}]*)\}', r'sqrt(\1)', s)
    s = re.sub(r'\\(sin|cos)\^2\(([^()]*)\)', r'(\1(\2))**2', s)
    s = re.sub(r'\\(sin|cos)\(([^()]*)\)\^2', r'(\1(\2))**2', s)
    s = re.sub(r'\\(sin|cos) t', r'\1(t)', s)
    s = s.replace('\\sin', 'sin').replace('\\cos', 'cos').replace('\\pi', ' pi ')
    return parse_expr(s, transformations=TR, local_dict={'x': x, 'y': y, 'z': z, 't': t, 'k': k, 'pi': pi, 'sqrt': sp.sqrt, 'sin': sp.sin, 'cos': sp.cos})


def vec(s):
    s = s.strip()
    assert s[0] == '(' and s[-1] == ')'
    return [tex(p) for p in s[1:-1].split(',')]


def expr_key(n, item, kp, truth, wrongs=None, vector=False):
    """truth: my expression (or list). Key and every accept form equal it; every wrong form differs and equals my slip."""
    w = part(n, item, kp)['widget']
    chk('%d %s %d is an expression part' % (n, item, kp), w['kind'] == 'expression')
    rd = vec if vector else tex
    eq = (lambda a, b: len(a) == len(b) and all(same(p, q) for p, q in zip(a, b))) if vector else same
    for form in [w['answer']] + list(w.get('accept', [])):
        chk('%d %s %d key/accept "%s" equals mine' % (n, item, kp, form), eq(rd(form), truth))
    got = {e['id']: e['tex'] for e in w.get('wrong', [])}
    wrongs = wrongs or {}
    chk('%d %s %d wrong ids %s are the ones I rebuilt %s' % (n, item, kp, sorted(got), sorted(wrongs)), set(got) == set(wrongs))
    for wid, mine in wrongs.items():
        if wid in got:
            chk('%d %s %d wrong "%s" %s equals my slip' % (n, item, kp, wid, got[wid]), eq(rd(got[wid]), mine))
            chk('%d %s %d wrong "%s" differs from the key' % (n, item, kp, wid), not eq(rd(got[wid]), truth))
            chk('%d %s %d wrong "%s" has a byKey line' % (n, item, kp, wid), wid in part(n, item, kp)['feedback'].get('byKey', {}))


def num_key(n, item, kp, truth, wrongs=None, places=None):
    """truth: my exact value. The key is within its own tolerance of it; the rounding the part asks for is taken;
    each wrong value equals my slip, is refused by the key band and overlaps no other band."""
    p = part(n, item, kp)
    w = p['widget']
    chk('%d %s %d is a numeric part' % (n, item, kp), w['kind'] == 'numeric')
    tv = float(sp.N(truth, 30))
    tol = w['tol']['abs']
    chk('%d %s %d key %s is my value %.6f' % (n, item, kp, w['answer'], tv), abs(w['answer'] - tv) <= max(6e-5 * max(1, abs(tv)) / 10, 5e-5))
    if places is not None:
        shown = round(tv, places)
        chk('%d %s %d the value to %d places (%s) is inside the band' % (n, item, kp, places, shown), abs(shown - w['answer']) <= tol + 1e-12)
        coarse = round(tv, places - 1)
        if abs(coarse - tv) > 1e-9:
            chk('%d %s %d the value to %d places (%s) is outside the band' % (n, item, kp, places - 1, coarse), abs(coarse - w['answer']) > tol)
        chk('%d %s %d the question names the form' % (n, item, kp), ('%d decimal places' % places in p['question']) or ('to %d place' % places in p['question']))
    else:
        chk('%d %s %d whole-number key with zero tolerance' % (n, item, kp), tol == 0 and float(w['answer']).is_integer() and 'whole number' in p['question'])
    got = {e['id']: e for e in w.get('wrong', [])}
    wrongs = wrongs or {}
    chk('%d %s %d wrong ids %s are the ones I rebuilt %s' % (n, item, kp, sorted(got), sorted(wrongs)), set(got) == set(wrongs))
    bands = [(w['answer'] - tol, w['answer'] + tol, 'key')]
    for wid, mine in wrongs.items():
        if wid not in got:
            continue
        e = got[wid]
        mv = float(sp.N(mine, 30))
        chk('%d %s %d wrong "%s" %s equals my slip %.6f' % (n, item, kp, wid, e['value'], mv), abs(e['value'] - mv) <= 6e-5 * max(1, abs(mv)))
        chk('%d %s %d wrong "%s" has a byKey line' % (n, item, kp, wid), wid in p['feedback'].get('byKey', {}))
        bands.append((e['value'] - e['tol']['abs'], e['value'] + e['tol']['abs'], wid))
    for i in range(len(bands)):
        for j in range(i + 1, len(bands)):
            a, b = bands[i], bands[j]
            chk('%d %s %d bands "%s" and "%s" do not overlap' % (n, item, kp, a[2], b[2]), a[1] < b[0] or b[1] < a[0])
    # numbers printed after an approx sign in this part
    for where, s in (('correct', p['feedback']['correct']), ('explain', p['explain']['text'])):
        m = re.findall(r'\\approx (-?[0-9.]+[0-9])', s)
        if m:
            last = float(m[-1])
            chk('%d %s %d %s prints %s, inside the key band' % (n, item, kp, where, m[-1]), abs(last - w['answer']) <= tol + 1e-12)
            dp = len(m[-1].split('.')[1]) if '.' in m[-1] else 0
            chk('%d %s %d %s prints %s, my value to %d places' % (n, item, kp, where, m[-1], dp), abs(round(tv, dp) - last) < 1e-9)


def says(n, item, kp, field, text):
    p = part(n, item, kp)
    s = p['question'] if field == 'question' else p['explain']['text'] if field == 'explain' else json.dumps(p['feedback'], ensure_ascii=False).replace('\\\\', '\\')
    chk('%d %s %d %s holds "%s"' % (n, item, kp, field, text), text in s)


def line(F, curve, a, b):
    """Work of the plane or space field F along curve(t), t from a to b."""
    sub = dict(zip((x, y, z), curve))
    return sp.simplify(integrate(sum(Fi.subs(sub) * sp.diff(ci, t) for Fi, ci in zip(F, curve)), (t, a, b)))


def seg(p0, p1):
    return [p0[i] + t * (p1[i] - p0[i]) for i in range(len(p0))]


def flux2(F, curve, a, b):
    """Flux across a plane curve, normal to the right of travel: int P dy - Q dx."""
    sub = {x: curve[0], y: curve[1]}
    return sp.simplify(integrate(F[0].subs(sub) * sp.diff(curve[1], t) - F[1].subs(sub) * sp.diff(curve[0], t), (t, a, b)))


def curl3(F):
    P, Q, R = F
    return [sp.diff(R, y) - sp.diff(Q, z), sp.diff(P, z) - sp.diff(R, x), sp.diff(Q, x) - sp.diff(P, y)]


def div(F):
    return sum(sp.diff(Fi, v) for Fi, v in zip(F, (x, y, z)))


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def polar(f, R):
    return sp.simplify(integrate(integrate(f.subs({x: r * cos(th), y: r * sin(th)}) * r, (r, 0, R)), (th, 0, 2 * pi)))


# =====================================================================================================================
# Level 1
# =====================================================================================================================
I = 'p-bead-semicircle'
F = [2 * x - y, x + 2 * y]
circ = [6 * cos(t), 6 * sin(t)]
F13 = [Fi.subs({x: 1, y: 3}) for Fi in F]
chk('bead: F(1, 3) = (-1, 7)', F13 == [-1, 7])
num_key(1, I, 1, sqrt(F13[0] ** 2 + F13[1] ** 2), {'sum': F13[0] + F13[1], 'no-root': F13[0] ** 2 + F13[1] ** 2, 'abs-sum': abs(F13[0]) + abs(F13[1])}, places=3)
F2 = sp.expand(F[0] ** 2 + F[1] ** 2)
expr_key(1, I, 2, F2, {'no-square': F[0] + F[1], 'coef': 3 * x ** 2 + 3 * y ** 2})
onc = {x: circ[0], y: circ[1]}
size = sqrt(sp.simplify(F2.subs(onc)))
speed = sp.simplify(sqrt(sp.diff(circ[0], t) ** 2 + sp.diff(circ[1], t) ** 2))
chk('bead: |F| = 6 sqrt5 on the circle, speed 6', same(size, 6 * sqrt(5)) and speed == 6)
S = integrate(size * speed, (t, 0, pi))
chk('bead: scalar integral 36 sqrt5 pi, also |F| times the arc length 6 pi', same(S, 36 * sqrt(5) * pi) and same(S, size * 6 * pi))
num_key(1, I, 3, S, {'no-speed': integrate(size, (t, 0, pi)), 'squared': integrate(size ** 2 * speed, (t, 0, pi)), 'full-circle': integrate(size * speed, (t, 0, 2 * pi))}, places=2)
dot = sp.simplify(sum(Fi.subs(onc) * sp.diff(ci, t) for Fi, ci in zip(F, circ)))
num_key(1, I, 4, dot, {'position': sp.simplify(sum(Fi.subs(onc) * ci for Fi, ci in zip(F, circ))), 'magnitude': size ** 2})
W = line(F, circ, 0, pi)
# route 2: close the path with the diameter and use Green. Curl 2 over the half disc of area 9 pi / 2; the diameter gives 0.
curlF = sp.diff(F[1], x) - sp.diff(F[0], y)
diam = line(F, seg((-6, 0), (6, 0)), 0, 1)
chk('bead: work 36 pi directly and by Green on the closed half disc (area 18 pi)', same(W, 36 * pi) and same(curlF * 18 * pi - diam, W) and diam == 0)
num_key(1, I, 5, W / S, {'inverse': S / W, 'no-integral': dot / S, 'full-circle': line(F, circ, 0, 2 * pi) / S}, places=3)
says(1, I, 5, 'explain', '113.10')
chk('bead: 36 pi = 113.10', round(float(36 * pi), 2) == 113.10)
chk('bead: not review-1 r4-clockwise (radius 3): the prose has radius 6', 'x^2 + y^2 = 36' in SETS[1]['items'][0]['prose'] and 'x^2 + y^2 = 9' not in json.dumps(SETS[1]['items'][0]))
# the claim in the last explanation: the tangential share is the same at every point
chk('bead: tangential part / |F| = 1/sqrt5 at every t', same(dot / speed / size, 1 / sqrt(5)))

I = 'p-two-routes-cubic'
F = [x * y, x + y]
A, B = [t, t ** 3], [t, 4 * t]
intA = sp.expand(sum(Fi.subs({x: A[0], y: A[1]}) * sp.diff(ci, t) for Fi, ci in zip(F, A)))
expr_key(1, I, 1, intA, {'no-dot': t ** 4 + t + t ** 3, 'no-chain': t ** 4 + (t + t ** 3) * t ** 2})
WA, WB = line(F, A, 0, 2), line(F, B, 0, 2)
num_key(1, I, 2, WA, {'no-dot': integrate(t ** 4 + t + t ** 3, (t, 0, 2)), 'no-chain': integrate(t ** 4 + (t + t ** 3) * t ** 2, (t, 0, 2))}, places=1)
chk('routes: W_A = 252/5', WA == Rat(252, 5))
num_key(1, I, 3, WB, {'ds': WB * sqrt(17), 'p-only': integrate(4 * t ** 2, (t, 0, 2)), 'q-only': integrate(20 * t, (t, 0, 2)), 'no-four': integrate(4 * t ** 2 + 5 * t, (t, 0, 2))}, places=3)
chk('routes: W_B = 152/3', WB == Rat(152, 3))
loop = WA - WB
# route 2: Green. Out along the lower curve y = x^3 and back along y = 4x is anticlockwise (x^3 < 4x on 0 < x < 2).
green = integrate(integrate(sp.diff(F[1], x) - sp.diff(F[0], y), (y, x ** 3, 4 * x)), (x, 0, 2))
chk('routes: loop work -4/15 directly and by Green', loop == Rat(-4, 15) and green == loop)
num_key(1, I, 4, loop, {'added': WA + WB, 'sign': WB - WA}, places=4)
ch = part(1, I, 5)['widget']
chk('routes: the choice key is the "not conservative" option', [o['id'] for o in ch['options'] if o.get('correct')] == ['a'])
chk('routes: P_y = x and Q_x = 1 differ', sp.diff(F[0], y) == x and sp.diff(F[1], x) == 1)
chk('routes: not the frame of homework-1 h1-two-paths (end point (1, 1), second route (t, t))', '(2, 8)' in SETS[1]['items'][1]['prose'] and '(t, 4t)' in SETS[1]['items'][1]['prose'])

I = 'p-cubic-potential'
F = [4 * x ** 3 + 3 * y ** 2, 6 * x * y]
expr_key(1, I, 1, [Fi.subs({x: 1, y: 2}) for Fi in F], {'y-not-squared': [4 + 3 * 2, 12], 'swap': [12, 16]}, vector=True)
expr_key(1, I, 2, sp.diff(F[0], y), {'px': sp.diff(F[0], x), 'qy': sp.diff(F[1], y)})
chk('cubic: curl 0 on the whole plane (polynomial field, no hole)', sp.diff(F[1], x) - sp.diff(F[0], y) == 0)
f = x ** 4 + 3 * x * y ** 2
chk('cubic: grad f = F and f(0, 0) = 0', same(sp.diff(f, x), F[0]) and same(sp.diff(f, y), F[1]) and f.subs({x: 0, y: 0}) == 0)
fd = integrate(F[0], x) + integrate(F[1], y)
expr_key(1, I, 3, f, {'double': fd, 'wrong-var': x ** 4 + integrate(F[1], x)})
Wp = f.subs({x: 2, y: 3}) - f.subs({x: 1, y: 0})
straight = line(F, seg((1, 0), (2, 3)), 0, 1)
bent = line(F, seg((1, 0), (1, 3)), 0, 1) + line(F, seg((1, 3), (2, 3)), 0, 1)
chk('cubic: work 69 by the potential, on the straight path and on a bent path', Wp == 69 and straight == 69 and bent == 69)
num_key(1, I, 4, Wp, {'end-only': f.subs({x: 2, y: 3}), 'double': fd.subs({x: 2, y: 3}) - fd.subs({x: 1, y: 0})})

I = 'p-ellipse-family'
F = [y ** 2 + k * y, 2 * x * y + 3 * x]
ks = sp.solve(sp.Eq(sp.diff(F[0], y), sp.diff(F[1], x)), k)
num_key(1, I, 1, ks[0], {'sign': -ks[0]})
f = x * y ** 2 + 3 * x * y
F3 = [Fi.subs(k, 3) for Fi in F]
chk('family: grad f = F at k = 3 and f(0, 0) = 0', same(sp.diff(f, x), F3[0]) and same(sp.diff(f, y), F3[1]))
expr_key(1, I, 2, f, {'double': integrate(F3[0], x) + integrate(F3[1], y), 'missing': x * y ** 2})
ell = [2 * cos(t), 5 * sin(t)]
one = {x: ell[0], y: ell[1]}
G = [sp.simplify(F[0].subs(k, 1) - sp.diff(f, x)), sp.simplify(F[1].subs(k, 1) - sp.diff(f, y))]
chk('family: G = (-2y, 0) at k = 1', G == [-2 * y, 0])
gdot = sp.simplify(sum(Gi.subs(one) * sp.diff(ci, t) for Gi, ci in zip(G, ell)))
expr_key(1, I, 3, gdot, {'sign': -gdot, 'position': sp.simplify(G[0].subs(one) * ell[0])})
W1 = line([Fi.subs(k, 1) for Fi in F], ell, 0, 2 * pi)          # route 1: the whole field, no splitting
area = pi * 2 * 5
Wk = line(F, ell, 0, 2 * pi)
chk('family: work 20 pi at k = 1 directly and by Green (curl 2, area 10 pi)', same(W1, 20 * pi) and same((sp.diff(F[1], x) - sp.diff(F[0], y)).subs(k, 1) * area, W1))
num_key(1, I, 4, W1, {'sign': -W1, 'sin-sq': 20 * 2 * pi}, places=2)
chk('family: work 10 pi (3 - k) directly and by Green', same(Wk, 10 * pi * (3 - k)) and same(sp.simplify(sp.diff(F[1], x) - sp.diff(F[0], y)) * area, Wk))
expr_key(1, I, 5, Wk, {'sign': -Wk, 'constant': 20 * pi})

# =====================================================================================================================
# Level 2
# =====================================================================================================================
I = 'p-rectangle-edges'
F = [y ** 3 - 4 * y, x * y ** 2 + 2 * x]
cu = sp.expand(sp.diff(F[1], x) - sp.diff(F[0], y))
expr_key(2, I, 1, cu, {'reversed': -cu, 'div': sp.diff(F[0], x) + sp.diff(F[1], y)})
gr = integrate(integrate(cu, (y, 0, 1)), (x, 0, 3))
corners = [(0, 0), (3, 0), (3, 1), (0, 1)]
edges = [line(F, seg(corners[i], corners[(i + 1) % 4]), 0, 1) for i in range(4)]   # bottom, right, top, left
chk('rectangle: Green gives 16 and the four edges give 0, 7, 9, 0', gr == 16 and edges == [0, 7, 9, 0] and sum(edges) == gr)
num_key(2, I, 2, gr, {'reversed': -gr, 'axes': integrate(integrate(cu, (y, 0, 3)), (x, 0, 1)), 'const': integrate(integrate(6, (y, 0, 1)), (x, 0, 3))})
num_key(2, I, 3, edges[1], {'drop-2x': integrate((x * y ** 2).subs(x, 3), (y, 0, 1))})
num_key(2, I, 4, gr - edges[0] - edges[1] - edges[3], {'direction': -edges[2], 'added': gr + edges[1]})
chk('rectangle: P(x, 1) = -3', F[0].subs(y, 1) == -3)

I = 'p-cycloid-arch'
cyc = [t - sin(t), 1 - cos(t)]
yx = sp.simplify(cyc[1] * sp.diff(cyc[0], t))
expr_key(2, I, 1, (1 - cos(t)) ** 2, {'no-derivative': cyc[1] * cyc[0], 'sign': -(1 - cos(t)) ** 2})
chk('cycloid: y x\' = (1 - cos t)^2', same(yx, (1 - cos(t)) ** 2))
# boundary anticlockwise: axis left to right (y = 0, dy = 0), then the arch from t = 2 pi back to 0
A1 = -integrate(cyc[1] * sp.diff(cyc[0], t), (t, 2 * pi, 0))                      # A = -oint y dx
A2 = integrate(cyc[0] * sp.diff(cyc[1], t), (t, 2 * pi, 0))                       # A = oint x dy, the other form
chk('cycloid: area 3 pi by -oint y dx and by oint x dy', same(A1, 3 * pi) and same(A2, 3 * pi))
num_key(2, I, 2, A1, {'sign': -A1, 'cos-sq': integrate(1 - 2 * cos(t), (t, 0, 2 * pi)), 'square': integrate(1 - cos(t) ** 2, (t, 0, 2 * pi))}, places=2)
Pm = -y ** 2 / 2
chk('cycloid: Q_x - P_y = y for P = -y^2/2, Q = 0', sp.diff(0, x) - sp.diff(Pm, y) == y)
expr_key(2, I, 3, Pm, {'sign': -Pm, 'no-half': -y ** 2, 'x-term': Pm + x, 'constant': Pm + 1})
# the part now fixes P: a function of y alone, 0 on the axis. Every P with -P_y = y is -y^2/2 + g(x); the wording leaves only g = 0.
chk('cycloid: P = -y^2/2 depends on y alone and is 0 at y = 0', Pm.free_symbols == {y} and Pm.subs(y, 0) == 0)
chk('cycloid: the x-term and constant slips satisfy -P_y = y but not the stated conditions', all(sp.diff(0, x) - sp.diff(g, y) == y for g in (Pm + x, Pm + 1)) and (Pm + x).free_symbols != {y} and (Pm + 1).subs(y, 0) != 0)
says(2, I, 3, 'question', 'a function of $y$ alone with $P = 0$ on the axis $y = 0$')
chk('cycloid: "centroid" is gone, "mean height" is used', 'centroid' not in json.dumps(SETS[2]['items'][1]) and 'mean height' in json.dumps(SETS[2]['items'][1]))
M1 = integrate(Pm.subs(y, cyc[1]) * sp.diff(cyc[0], t), (t, 2 * pi, 0))          # oint P dx
M2 = integrate((cyc[0] * cyc[1]) * sp.diff(cyc[1], t), (t, 2 * pi, 0))           # oint xy dy: Q = xy has Q_x = y
chk('cycloid: moment 5 pi / 2 by oint P dx and by oint xy dy', same(M1, 5 * pi / 2) and same(M2, 5 * pi / 2))
chk('cycloid: int (1 - cos t)^3 = 5 pi', same(integrate((1 - cos(t)) ** 3, (t, 0, 2 * pi)), 5 * pi))
num_key(2, I, 4, M1, {'no-half': 2 * M1, 'sign': -M1}, places=2)
num_key(2, I, 5, M1 / A1, {'inverse': A1 / M1, 'no-half': 2 * M1 / A1}, places=3)
chk('cycloid: mean height 5/6, below half the height 2', M1 / A1 == Rat(5, 6))
above = integrate((cyc[1] - 1) * sp.diff(cyc[0], t), (t, pi / 2, 3 * pi / 2))
chk('cycloid: "most of the area is low down": the part below y = 1 is over half', float(1 - above / A1) > 0.5)

I = 'p-triangle-flux'
F = [x ** 2 + y, 2 * x * y]
dv = sp.diff(F[0], x) + sp.diff(F[1], y)
cu = sp.diff(F[1], x) - sp.diff(F[0], y)
expr_key(2, I, 1, dv, {'curl': cu, 'only-p': sp.diff(F[0], x)})
tri = lambda g: integrate(integrate(g, (y, 0, 6 - 2 * x)), (x, 0, 3))
tot = tri(dv)
cs = [(0, 0), (3, 0), (0, 6)]
fl = [flux2(F, seg(cs[i], cs[(i + 1) % 3]), 0, 1) for i in range(3)]             # bottom, long, left; anticlockwise so normal is outward
chk('triangle: flux 36 by the divergence and 0, 54, -18 edge by edge', tot == 36 and fl == [0, 54, -18] and sum(fl) == tot)
num_key(2, I, 2, tot, {'curl': tri(cu), 'rectangle': integrate(integrate(dv, (y, 0, 6)), (x, 0, 3)), 'only-p': tri(sp.diff(F[0], x))})
num_key(2, I, 3, fl[2], {'sign': -fl[2], 'tangent': integrate(F[1].subs(x, 0), (y, 0, 6))})
num_key(2, I, 4, tot - fl[0] - fl[2], {'add-edge': tot + fl[2], 'all-out': tot})

I = 'p-quadrilateral-plot'
F = [2 * x - 4 * y, x + y]
q = [(0, 0), (5, 1), (4, 5), (1, 3)]
edge = lambda a, b: a[0] * b[1] - b[0] * a[1]
es = [edge(q[i], q[(i + 1) % 4]) for i in range(4)]
ed = [line([-y, x], seg(q[i], q[(i + 1) % 4]), 0, 1) for i in range(4)]         # int x dy - y dx by parametrising
chk('plot: edges 0, 21, 7, 0 by the formula and by parametrising', es == [0, 21, 7, 0] and ed == es)
num_key(2, I, 1, es[1], {'swap': -es[1], 'plus': 5 * 5 + 4 * 1})
Aq = Rat(sum(es), 2)
fan = Rat(edge(q[1], q[2]) + edge(q[2], q[3]), 2)                                 # two triangles from the corner at the origin
chk('plot: area 14 by the edges and by two triangles; corners anticlockwise and convex', Aq == 14 and fan == 14 and all(
    (q[(i + 1) % 4][0] - q[i][0]) * (q[(i + 2) % 4][1] - q[(i + 1) % 4][1]) - (q[(i + 1) % 4][1] - q[i][1]) * (q[(i + 2) % 4][0] - q[(i + 1) % 4][0]) > 0 for i in range(4)))
plus = [a[0] * b[1] + b[0] * a[1] for a, b in ((q[i], q[(i + 1) % 4]) for i in range(4))]
num_key(2, I, 2, Aq, {'no-half': sum(es), 'plus': Rat(sum(plus), 2)})
dv = sp.diff(F[0], x) + sp.diff(F[1], y)
cu = sp.diff(F[1], x) - sp.diff(F[0], y)
fx = sum(flux2(F, seg(q[i], q[(i + 1) % 4]), 0, 1) for i in range(4))
ci = sum(line(F, seg(q[i], q[(i + 1) % 4]), 0, 1) for i in range(4))
chk('plot: flux 42 and circulation 70, each by Green and edge by edge', dv * Aq == 42 and fx == 42 and cu * Aq == 70 and ci == 70)
num_key(2, I, 3, fx, {'curl': cu * Aq, 'no-half': dv * sum(es)})
num_key(2, I, 4, ci, {'div': dv * Aq, 'reversed': -cu * Aq, 'plus': (sp.diff(F[1], x) + sp.diff(F[0], y)) * Aq})

# =====================================================================================================================
# Level 3
# =====================================================================================================================
I = 'p-saddle-roof'
surf = [x, y, x * y]
nrm = cross([sp.diff(s, x) for s in surf], [sp.diff(s, y) for s in surf])
expr_key(3, I, 1, nrm, {'sign': [y, x, 1], 'swap': [-x, -y, 1]}, vector=True)
ln = sqrt(sum(c_ ** 2 for c_ in nrm))
expr_key(3, I, 2, ln, {'no-root': ln ** 2, 'no-one': sqrt(x ** 2 + y ** 2)})
Ar = polar(ln, sqrt(3))
Ar2 = integrate(pi * sqrt(1 + u), (u, 0, 3))                                      # route 2: rings, u = r^2, dA = pi du
chk('roof: area 14 pi / 3 in polar form and by rings in u = r^2', same(Ar, 14 * pi / 3) and same(Ar2, Ar))
num_key(3, I, 3, Ar, {'no-r': 2 * pi * integrate(sqrt(1 + r ** 2), (r, 0, sqrt(3))), 'flat': pi * 3}, places=2)
F = [y, x, 5]
fdot = sp.expand(sum(a * b for a, b in zip(F, nrm)))
up = polar(fdot, sqrt(3))
# route 2: div F = 0. Close the roof with the wall below its rim down to z = -10 and the disc there.
chk('roof: div F = 0', div(F) == 0)
rim = {x: sqrt(3) * cos(th), y: sqrt(3) * sin(th)}
wall = integrate(integrate((F[0] * cos(th) + F[1] * sin(th)).subs(rim) * sqrt(3), (z, -10, (x * y).subs(rim))), (th, 0, 2 * pi))
floor_up = 5 * 3 * pi
chk('roof: upward flux 21 pi / 2 directly and by the divergence theorem (floor 15 pi, wall 9 pi / 2)', same(up, 21 * pi / 2) and same(floor_up - wall, up) and same(wall, 9 * pi / 2))
num_key(3, I, 4, up, {'down': -up, 'z-only': polar(sp.Integer(5), sqrt(3)), 'sign-normal': polar(sum(a * b for a, b in zip(F, [y, x, 1])), sqrt(3))}, places=2)
chk('roof: the r^2 term is 9 pi / 2', same(polar(x ** 2 + y ** 2, sqrt(3)), 9 * pi / 2))

I = 'p-open-tank'
F = [x * z, y ** 2, 3 * z]
box = lambda g: integrate(integrate(integrate(g, (x, 0, 4)), (y, 0, 1)), (z, 0, 2))
dv = div(F)
expr_key(3, I, 1, dv, {'wrong-var': x + 2 * y + 3, 'drop-const': z + 2 * y})
faces = {
    'x=4': integrate(integrate(F[0].subs(x, 4), (y, 0, 1)), (z, 0, 2)), 'x=0': -integrate(integrate(F[0].subs(x, 0), (y, 0, 1)), (z, 0, 2)),
    'y=1': integrate(integrate(F[1].subs(y, 1), (x, 0, 4)), (z, 0, 2)), 'y=0': -integrate(integrate(F[1].subs(y, 0), (x, 0, 4)), (z, 0, 2)),
    'z=2': integrate(integrate(F[2].subs(z, 2), (x, 0, 4)), (y, 0, 1)), 'z=0': -integrate(integrate(F[2].subs(z, 0), (x, 0, 4)), (y, 0, 1))}
chk('tank: 40 by the divergence theorem and face by face (8, 0, 8, 0, lid 24, floor 0)', box(dv) == 40 and sum(faces.values()) == 40 and
    [faces[f_] for f_ in ('x=4', 'x=0', 'y=1', 'y=0', 'z=2', 'z=0')] == [8, 0, 8, 0, 24, 0])
num_key(3, I, 2, box(dv), {'drop-const': box(z + 2 * y), 'wrong-var': box(x + 2 * y + 3)})
num_key(3, I, 3, faces['z=2'], {'wrong-area': 6 * 8, 'no-z': 3 * 4})
num_key(3, I, 4, sum(v for f_, v in faces.items() if f_ != 'z=2'), {'added': box(dv) + faces['z=2'], 'from-16': box(z + 2 * y) - faces['z=2']})

I = 'p-slanted-ellipse'
Fc = [-y * z, x * z, x * y + c * y]
F = [g.subs(c, 3) for g in Fc]
cu = curl3(F)
expr_key(3, I, 1, cu, {'reversed': [-g for g in cu], 'half': [3, -y, z]}, vector=True)
pl = [x, y, 2 - x]
nrm = cross([sp.diff(s, x) for s in pl], [sp.diff(s, y) for s in pl])
expr_key(3, I, 2, nrm, {'fx': [-1, 0, 1], 'down': [-g for g in nrm]}, vector=True)
integrand = sp.expand(sum(a * b for a, b in zip(cu, nrm)).subs(z, 2 - x))
expr_key(3, I, 3, integrand, {'z-left': 3 + 2 * z, 'fx': sp.expand(sum(a * b for a, b in zip(cu, [-1, 0, 1])).subs(z, 2 - x))})
stokes = polar(integrand, 2)
C = [2 * cos(t), 2 * sin(t), 2 - 2 * cos(t)]                                     # anticlockwise seen from above
direct = line(F, C, 0, 2 * pi)
chk('ellipse: circulation 28 pi by Stokes and by the line integral round C', same(stokes, 28 * pi) and same(direct, stokes))
num_key(3, I, 4, stokes, {'fx': polar(1 - 2 * x, 2), 'unit-disc': polar(integrand, 1), 'extra-root': stokes * sqrt(2)}, places=2)
cuc = curl3(Fc)
gen = polar(sp.expand(sum(a * b for a, b in zip(cuc, nrm)).subs(z, 2 - x)), 2)
chk('ellipse: with cy the circulation is 4 pi (c + 4), by Stokes and directly', same(gen, 4 * pi * (c + 4)) and same(line(Fc, C, 0, 2 * pi), gen) and cuc[0] == c)
num_key(3, I, 5, sp.solve(gen, c)[0], {'sign': 4})

I = 'p-can-curl'
F = [2 * y - z ** 2, x + x * z + 3 * z, x * y]
cu = curl3(F)
expr_key(3, I, 1, cu, {'reversed': [-g for g in cu], 'qz-slip': [x - 3, -y - 2 * z, z - 1]}, vector=True)
num_key(3, I, 2, div(cu), {'qz-slip': div([x - 3, -y - 2 * z, z - 1])})
base = line(F, [4 * cos(t), 4 * sin(t), 0], 0, 2 * pi)
base_s = polar(cu[2].subs(z, 0), 4)
chk('can: bottom circle -16 pi directly and by Stokes on the base disc', same(base, -16 * pi) and same(base_s, base))
bdot = sp.simplify(sum(g.subs({x: 4 * cos(t), y: 4 * sin(t), z: 0}) * d for g, d in zip(F, [-4 * sin(t), 4 * cos(t), 0])))
chk('can: F . r\' = -32 sin^2 t + 16 cos^2 t on the bottom circle', same(bdot, -32 * sin(t) ** 2 + 16 * cos(t) ** 2))
num_key(3, I, 3, base, {'sign': -base, 'radius': -4 * pi}, places=2)
lid = polar(cu[2].subs(z, 2), 4)
num_key(3, I, 4, lid, {'z0': polar(cu[2].subs(z, 0), 4), 'radius': 4 * pi}, places=2)
side_n = {x: 4 * cos(th), y: 4 * sin(th)}
side = integrate(integrate((cu[0] * cos(th) + cu[1] * sin(th)).subs(side_n) * 4, (z, 0, 2)), (th, 0, 2 * pi))   # route 1: parametrise the side
closed = -lid - (-base_s)                                                         # route 2: side + lid + base (normal down) = 0
stokes_side = base - lid                                                          # route 3: Stokes on side + lid, bounded by the bottom circle
chk('can: side flux -32 pi by parametrising, by the closed surface and by Stokes', same(side, -32 * pi) and same(closed, side) and same(stokes_side, side))
num_key(3, I, 5, side, {'added': -(lid + base_s), 'sign': -side, 'no-base': -lid}, places=2)

# =====================================================================================================================
# Shape of the sets (docs/briefs/chained.md)
# =====================================================================================================================
course = json.load(open(os.path.join(ROOT, 'course.json')))
for n, d in SETS.items():
    parts = [p for it in d['items'] for p in it['parts']]
    typed = sum(p['widget']['kind'] in ('numeric', 'expression') for p in parts)
    chk('set %d: 3 to 5 items, each of 3 to 5 parts' % n, 3 <= len(d['items']) <= 5 and all(3 <= len(it['parts']) <= 5 for it in d['items']))
    chk('set %d: at least two thirds typed (%d of %d)' % (n, typed, len(parts)), 3 * typed >= 2 * len(parts))
    chk('set %d: difficulty 3 to 5 with a 5' % n, all(3 <= it['difficulty'] <= 5 for it in d['items']) and any(it['difficulty'] == 5 for it in d['items']))
    for it in d['items']:
        for i, p in enumerate(it['parts']):
            sents = [s for s in re.split(r'(?<=[.?])\s+(?=[A-Z$])', p['explain']['text']) if s]
            chk('set %d %s %d: explain of at most three sentences' % (n, it['id'], i + 1), len(sents) <= 3)

print('%d checks, %d failed' % (n_ok + n_bad, n_bad))
sys.exit(1 if n_bad else 0)
