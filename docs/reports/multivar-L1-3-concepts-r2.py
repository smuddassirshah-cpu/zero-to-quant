"""Blind concept audit, multivar levels 1 to 3, round 2 (multivar-1-3-r2).

Independent recomputation of the claims in the ledger docs/reports/audit-multivar-1-3-r2-ledger.md.
Exits 0 only if every CONTENT check passes. A content check that fails is a finding and stays failing.
SUPPORT checks establish the auditor's own counter-examples; they must pass for a finding to stand.
Run: python docs/reports/multivar-L1-3-concepts-r2.py   (NumPy and SciPy; no version-dependent figure)
Fix pass (Opus fixer): the review-3 item 8 note was re-pointed to fire only on the old question wording, since the
question now asks what the second derivative test shows (key unchanged). No content or support check was changed.
"""
import json, math, os, sys, warnings
warnings.filterwarnings("ignore")
import numpy as np
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'multivar')
J = lambda f: json.load(open(os.path.join(C, f + '.json'), encoding='utf-8'))
fails, notes, n = [], [], 0
rng = np.random.default_rng(20261126)


def check(name, ok, content=True):
    global n
    n += 1
    if not ok:
        fails.append(('CONTENT ' if content else 'SUPPORT ') + name)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def grad(f, p, h=1e-6):
    p = np.asarray(p, float)
    return np.array([(f(*(p + h * e)) - f(*(p - h * e))) / (2 * h) for e in np.eye(len(p))])


def hess(f, p, h=1e-4):
    p = np.asarray(p, float); k = len(p); H = np.zeros((k, k))
    for i in range(k):
        for j in range(k):
            ei, ej = np.eye(k)[i] * h, np.eye(k)[j] * h
            H[i, j] = (f(*(p + ei + ej)) - f(*(p + ei - ej)) - f(*(p - ei + ej)) + f(*(p - ei - ej))) / (4 * h * h)
    return H


# ---------------------------------------------------------------- level 1
# l1: contours, P&L surface
check('l1 s4 rises 0.75 and 2.75', close(1 - 0.25, 0.75) and close(9 - 6.25, 2.75))
check('l1 s8 flat book', close(300 * 2 + 200 * (-3), 0) and close(-300 / 200 * 2, -3))
check('l1 s8 slip ratio-flipped', close(-200 / 300 * 2, -1.3333, 1e-4))
# l2: partials by finite differences
f = lambda x, y: x * x * y + 3 * y
check('l2 f_x=2xy, f_y=x^2+3', np.allclose(grad(f, (2, 2)), (8, 7), atol=1e-5))
check('l2 e^{xy} f_x at (0,.5)', close(grad(lambda x, y: math.exp(x * y), (0, .5))[0], .5, 1e-6))
check('l2 ln f_y, f_x at (1,2)', np.allclose(grad(lambda x, y: math.log(x * x + y * y), (1, 2)), (.4, .8), atol=1e-6))
check('l2 quiz x/y f_y at (2,4)', close(grad(lambda x, y: x / y, (2, 4))[1], -0.125, 1e-6))
V = lambda y1, y2: 5e5 * math.exp(-2 * y1) + 3e5 * math.exp(-10 * y2)
g = grad(V, (.03, .04), 1e-7)
check('l2 quiz pv01 201.10 and slip 94.18', abs(-g[1] * 1e-4 - 201.10) < .01 and abs(-g[0] * 1e-4 - 94.18) < .01)
check('review-1 bond rate 12.74', abs(g[0] * 2e-4 + g[1] * (-1e-4) - 12.74) < .01)


# Black-Scholes tables (r = 0, T = 0.5, K = 100) behind l2 s8, review-1 item 3 and l3 s8
def bs(S, s, K=100., T=.5):
    d1 = (math.log(S / K) + .5 * s * s * T) / (s * math.sqrt(T)); d2 = d1 - s * math.sqrt(T)
    return S * norm.cdf(d1) - K * norm.cdf(d2), norm.cdf(d1)


t2 = J('l2-slicing')['screens'][8]['canvas']['params']['rows']
ok = all(abs(bs(S, s)[0] - float(t2[i][j + 1])) < .006 for i, S in enumerate((99, 100, 101)) for j, s in enumerate((.19, .20, .21)))
check('l2 s8 call table is Black-Scholes at r=0', ok)
check('l2 s8 delta .53, diagonal .81, vega .28', close((6.18 - 5.12) / 2, .53) and close((6.46 - 4.84) / 2, .81) and close((5.92 - 5.36) / 2, .28))
t3 = J('l3-second-partials')['screens'][8]['canvas']['params']['rows']
ok = all(abs(bs(S, s)[1] - float(t3[i][j + 1])) < .0006 for i, S in enumerate((95, 100, 105)) for j, s in enumerate((.15, .20, .25)))
check('l3 s8 delta table is Black-Scholes at r=0', ok)
check('l3 s8 vanna -0.54 at 105, +0.87 at 95, gamma slip .0276',
      close((.642 - .696) / .1, -.54) and close((.420 - .333) / .1, .87) and close((.661 - .385) / 10, .0276))
# exact vanna has the estimated signs
vanna = lambda S, s, h=1e-4: (bs(S, s + h)[1] - bs(S, s - h)[1]) / (2 * h)
check('l3 s8 vanna sign: negative at 105, positive at 95', vanna(105, .2) < 0 < vanna(95, .2))

# l3: second partials
f = lambda x, y: x ** 3 * y ** 2
H = hess(f, (1, 3)); check('l3 s3 table 54, 18, 18, 2', np.allclose(H, [[54, 18], [18, 2]], atol=1e-3))
f = lambda x, y: math.exp(x * y)
check('l3 s4 f_xy=(1+xy)e^{xy}', all(close(hess(f, p)[0, 1], (1 + p[0] * p[1]) * math.exp(p[0] * p[1]), 1e-4) for p in rng.uniform(-1, 1, (20, 2))))
check('review-1 f_xy x^3e^{2y} = 24', close(hess(lambda x, y: x ** 3 * math.exp(2 * y), (2, 0))[0, 1], 24, 1e-4))
f = lambda x, y: x * math.exp(x * y)
check('homework-1 f_xy=(2x+x^2y)e^{xy}', all(close(hess(f, p)[0, 1], (2 * p[0] + p[0] ** 2 * p[1]) * math.exp(p[0] * p[1]), 1e-4) for p in rng.uniform(-1, 1, (20, 2))))


# SUPPORT (finding 1): a function whose FIRST partials are continuous but whose mixed partials differ at the origin.
# So "smooth = partial derivatives continuous", read as first partials, does not give Clairaut (Apostol II 8.23 needs the mixed second partials continuous).
def P(x, y):
    return 0.0 if x == 0 and y == 0 else x * y * (x * x - y * y) / (x * x + y * y)


def Px(x, y, h=1e-7): return (P(x + h, y) - P(x - h, y)) / (2 * h)
def Py(x, y, h=1e-7): return (P(x, y + h) - P(x, y - h)) / (2 * h)


pts = rng.normal(size=(20000, 2)); pts = pts / np.linalg.norm(pts, axis=1)[:, None]
cont = max(max(abs(Px(*(r * u))), abs(Py(*(r * u)))) / r for r in (1e-2, 1e-3) for u in pts[:3000])
check('support: first partials of xy(x^2-y^2)/(x^2+y^2) are O(r), so continuous at 0', cont < 2.5, content=False)
k = 1e-3
fxy0 = (Px(0, k) - Px(0, -k)) / (2 * k); fyx0 = (Py(k, 0) - Py(-k, 0)) / (2 * k)
check('support: f_xy(0,0) = -1 but f_yx(0,0) = +1', abs(fxy0 + 1) < 1e-3 and abs(fyx0 - 1) < 1e-3, content=False)

# l4 chain rule
check('l4 s1-s3 -3 + 1 = -2', close(4 * .5 - 4, -2) and close(3 * -1 + 1 * 1, -2))
check('l4 s4 rate 11', close(((1 + 2e-6) ** 2 * (2 + 3e-6) - (1 - 2e-6) ** 2 * (2 - 3e-6)) / 2e-6, 11, 1e-5))
check('l4 s8 140 and slips', close(1000 * (.56 * .5 + .28 * -.5), 140) and close(1000 * (.56 * .5 + .28 * .5), 420) and close(.5 - .5, 0))
check('l4 quiz 80, 10', close(8 * 4 + 4 * 12, 80) and close(200 * .3 - 500 * .1, 10))
check('homework-1 item 6 -sqrt2', close(1 * -math.sqrt(.5) + (-1) * math.sqrt(.5), -1.4142, 1e-4))
check('homework-1 item 3 0.12, 0.07, 0.0475, 0.105',
      close(2 * .5 * .09 + 2 * .5 * .5 * .2 * .3, .12) and close(2 * .5 * .04 + .03, .07) and close(.25 * .04 + .25 * .09 + 2 * .25 * .03, .0475) and close(.09 + .015, .105))
Vb = lambda S, s: 1000 * (.5 * (S - 100) + .02 * (S - 100) ** 2 + 30 * (s - .2) - 2 * (S - 100) * (s - .2))
r = lambda t: (Vb(100 + 2 * (t + 1e-6), .2 - .01 * (t + 1e-6)) - Vb(100 + 2 * (t - 1e-6), .2 - .01 * (t - 1e-6))) / 2e-6
check('homework-1 long form 700, 940, vanna -2000, gamma 40', abs(r(0) - 700) < 1e-3 and abs(r(1) - 940) < 1e-3 and np.allclose(hess(Vb, (100, .2), 1e-3), [[40, -2000], [-2000, 0]], atol=1e-2))
# problems-1
check('problems-1 item 0 exact -0.0303, slip -0.015', abs(math.sqrt(18 - 9 * 1.01 ** 2) - 3 + .0303) < 5e-5 and abs(math.sqrt(18 - 9.09) - 3 + .015) < 5e-4)
f = lambda x, y: x ** 3 * y - 2 * x * y * y
check('problems-1 item 1 f_xy=8, f_x=10, 10.78', close(hess(f, (2, 1))[0, 1], 8, 1e-4) and close(grad(f, (2, 1))[0], 10, 1e-6) and close(grad(f, (2, 1.1))[0], 10.78, 1e-6))
VF = lambda p, x: 2000 * p / x
gg = grad(VF, (50, 1.25)); HH = hess(VF, (50, 1.25), 1e-3)
check('problems-1 item 2 1600, -64000, 160, -1280, -12.8', np.allclose(gg, (1600, -64000), atol=1e-2) and close(gg @ (.5, .01), 160, 1e-6) and abs(HH[0, 1] + 1280) < .1 and close(-1280 * .01, -12.8))

# ---------------------------------------------------------------- level 2
f = lambda x, y: x * x + 2 * y * y
gP = grad(f, (2, 1))
check('l5 s0 slopes 5.66, 5.37, 4, 0', np.allclose([gP @ np.array(u) / np.hypot(*u) for u in ((4, 4), (2, 1), (0, 1), (1, -1))], (5.657, 5.367, 4, 0), atol=2e-3))
check('l5 s4 |grad| 6.32 at A, 8.94 at B', close(np.linalg.norm(grad(f, (math.sqrt(10), 0))), 6.3246, 1e-4) and close(np.linalg.norm(grad(f, (0, math.sqrt(5)))), 8.9443, 1e-4))
check('l5 s6 grad g = (-4,-8); (8,-4) along contour', np.allclose(grad(lambda x, y: 20 - x * x - 4 * y * y, (2, 1)), (-4, -8), atol=1e-6) and close(8 * -4 + -4 * -8, 0))
Sg = np.array([[.04, .01], [.01, .01]]); w = np.array([.5, .5])
check('l5 s9 Sigma from 20%, 10%, rho .5; grad V = 2 Sigma w = (.05,.02); slip .025', close(.5 * .2 * .1, .01) and np.allclose(2 * Sg @ w, (.05, .02)) and close((Sg @ w)[0], .025))
# gradient is the direction of steepest climb: Monte Carlo over directions
th = rng.uniform(0, 2 * np.pi, 200000); U = np.c_[np.cos(th), np.sin(th)]
best = U[np.argmax(U @ gP)]
check('l5/l6 MC: best of 200,000 unit arrows is grad/|grad| and its slope is |grad|', np.allclose(best, gP / np.linalg.norm(gP), atol=1e-4) and (U @ gP).max() <= np.linalg.norm(gP) + 1e-12)
check('l6 values 5.6, 0.8, -5.66, slips 4, 2.828', close(4 * .6 + 4 * .8, 5.6) and close(4 * -.6 + 4 * .8, .8) and close(4 * -3 + 4 * 4, 4) and close(4 / math.sqrt(2), 2.828, 1e-3))
check('l6 s8 210, 1710, 123.5', close(1200 * .8 - 500 * 1.5, 210) and close(1200 * .8 + 500 * 1.5, 1710) and abs(210 / math.hypot(.8, 1.5) - 123.5) < .05)
check('l6 quiz 4.95, -0.8, 13', close(7 / math.sqrt(2), 4.95, 1e-3) and close(4 * .6 - 4 * .8, -.8) and close(math.hypot(5, 12), 13))
check('homework-2 item 1 -4.025, 4.243', close(-9 / math.sqrt(5), -4.025, 1e-4) and close(math.sqrt(18), 4.243, 1e-4))
S2 = np.array([[.09, -.009], [-.009, .0225]]); w2 = np.array([.6, .4])
check('homework-2 item 0 0.1008, 0.0072, slips', np.allclose(2 * S2 @ w2, (.1008, .0072)) and close(2 * .09 * .6, .108) and close(-.2 * .3 * .15, -.009))
# l7 tangent planes
plane = lambda x, y: 6 + 4 * (x - 2) + 4 * (y - 1)
check('l7 6.6 vs 6.615; 6.04 vs 6.0422; error 3h^2; Jo', close(plane(2.1, 1.05), 6.6) and close(f(2.1, 1.05), 6.615) and close(plane(1.98, 1.03), 6.04) and abs(f(1.98, 1.03) - 6.0422) < 1e-4
      and all(close(f(2 + h, 1 + h) - plane(2 + h, 1 + h), 3 * h * h) for h in (.1, .05, .01)) and close(6 + 5 * .5 + 6 * .5, 11.5) and close(f(2.5, 1.5), 10.75) and close(plane(2.5, 1.5), 10))
check('l7 s8 0.825, 1.575, 1.196', close(.6 * 2 + .25 * -1.5, .825) and close(.6 * 2 + .25 * 1.5, 1.575) and abs(1.2 + .25 * -.015 - 1.196) < 5e-4)
check('review-2 values', np.allclose(grad(lambda x, y: 3 * x * x - x * y + y * y, (1, 2)), (4, 3), atol=1e-6) and close(2 + .1 - .4, 1.7) and close(2.1 * .81, 1.701) and close(.55 * -3 + .18 * 4, -.93))
sg = lambda x, y: math.hypot(x, y)
check('problems-2 item 1 4.88, 0.0118, 0.1156, 0.0029', close(.6 * 3.2 + .8 * 3.7, 4.88) and abs(sg(3.2, 3.7) - 4.88 - .0118) < 5e-5 and close(23.93 - 4.88 ** 2, .1156) and abs(sg(3.1, 3.85) - 4.94 - .0029) < 5e-5)
check('problems-2 item 0 (12,9), 15, -4.2, 60 degrees', close(12 * -.8 + 9 * .6, -4.2) and close(math.hypot(12, 9), 15) and close(math.degrees(math.acos(.5)), 60) and close(12 * .6 - 9 * .8, 0))
# SUPPORT (finding 3): the tangent line's error is quadratic only with continuous second derivatives.
# f(x) = |x|^1.5 has a continuous first derivative; at 0 its tangent error is h^1.5, so halving the step divides it by 2.83, not 4.
e = lambda h: abs(h) ** 1.5
check('support: C1 but not C2 example, halving the step divides the tangent error by 2^1.5', close(e(.2) / e(.1), 2 ** 1.5), content=False)


# l8 gradient descent
def descend(gr, x, y, s, k):
    for _ in range(k):
        gx, gy = gr(x, y); x, y = x - s * gx, y - s * gy
    return x, y


gb = lambda x, y: (2 * x, 4 * y)
check('l8 s0 one step (3.2,1.8), f=16.72; step 2 (2.56,1.08)', np.allclose(descend(gb, 4, 3, .1, 1), (3.2, 1.8)) and close(f(3.2, 1.8), 16.72) and np.allclose(descend(gb, 4, 3, .1, 2), (2.56, 1.08)))
a = descend(gb, 4, 3, .05, 10); b = descend(gb, 4, 3, .45, 10); c = descend(gb, 4, 3, .3, 10)
check('l8 s1 ends: 0.05 at (1.39,0.32) f 2.15; 0.45 f 0.21; 0.3 nearly 0', np.allclose(a, (1.39, .32), atol=6e-3) and abs(f(*a) - 2.15) < 6e-3 and abs(f(*b) - .21) < 6e-3 and f(*c) < 1e-6)
tw = J('l8-walking-downhill')['screens'][3]['widget']['tests']
check('l8 s3 expected values of the 7 tests', np.allclose(descend(gb, 4, 3, .1, 10), (0.4294967296, 0.0181398528)) and np.allclose(descend(gb, 4, 3, .6, 10), (4.096e-07, 86.7763964928)) and len(tw) == 7)
check('l8 s4 limit 0.5: y flips 3,-3', np.allclose([descend(gb, 4, 3, .5, k)[1] for k in (1, 2, 3)], (-3, 3, -3)))
# settle iff 0 < s < 0.5 on x^2 + 2y^2; iff 0 < s < 1/3 on 3x^2 + y^2 (sweep of step sizes, 2,000 steps)
sw = np.round(np.arange(.01, .7, .01), 2)
settles = lambda gr, s: f(*descend(gr, 4, 3, s, 2000)) < 1e-12
check('l8 sweep: x^2+2y^2 settles exactly for s < 0.5', all(settles(gb, s) == (s < .5 - 1e-9) for s in sw))
check('l8 s7 sweep: 3x^2+y^2 settles exactly for s < 1/3', all(settles(lambda x, y: (6 * x, 2 * y), s) == (s < 1 / 3) for s in sw))
check('review-2 item 6 sweep: 2x^2+5y^2 settles exactly for s < 0.2', all(settles(lambda x, y: (4 * x, 10 * y), s) == (s < .2 - 1e-9) for s in sw))
check('homework-2 best step 1/3 on x^2+2y^2', close(min(np.linspace(.01, .49, 4801), key=lambda s: max(abs(1 - 2 * s), abs(1 - 4 * s))), 1 / 3, 1e-3))


def fit(xs, ys, s, k):
    a = b = 0.0; m = len(xs)
    for _ in range(k):
        r = [a + b * x - y for x, y in zip(xs, ys)]
        ga = 2 / m * sum(r); gb_ = 2 / m * sum(ri * x for ri, x in zip(r, xs)); a, b = a - s * ga, b - s * gb_
    return a, b


for xs, ys, s in (([-1.2, .4, 1., -.6, 1.8, .2], [-1.5, .7, 1.1, -.4, 2.3, 0.], .1), ([0, 1, 2, 3], [.5, 2.5, 4.5, 6.5], .05), ([-2., -1., .5, 1.5, 2.5], [1.1, .4, -.2, -.5, -1.4], .05)):
    bb, aa = np.polyfit(xs, ys, 1); got = fit(xs, ys, s, 3000)
    check('l8 s8 3,000 steps reach the least-squares line to rel 1e-9', math.isclose(got[0], aa, rel_tol=1e-9, abs_tol=1e-12) and math.isclose(got[1], bb, rel_tol=1e-9))
check('l8 s8 one step (0.0733, 0.252); beta 1.20, alpha 0.047', np.allclose(fit([-1.2, .4, 1., -.6, 1.8, .2], [-1.5, .7, 1.1, -.4, 2.3, 0.], .1, 1), (0.0733333, 0.252)) and np.allclose(fit([-1.2, .4, 1., -.6, 1.8, .2], [-1.5, .7, 1.1, -.4, 2.3, 0.], .1, 3000), (.047, 1.200), atol=6e-4))


def steps_needed(gr, x, y, s, tol, mx):
    for k in range(mx):
        gx, gy = gr(x, y)
        if math.hypot(gx, gy) < tol: return k
        x, y = x - s * gx, y - s * gy
    return mx


check('homework-2 code counts 41, 10, 445, 0, 50, 200, 77', [steps_needed(gb, 4, 3, .1, 1e-3, 1000), steps_needed(gb, 4, 3, .3, 1e-3, 1000), steps_needed(gb, 4, 3, .01, 1e-3, 10000), steps_needed(gb, 0, 0, .1, 1e-3, 100),
      steps_needed(gb, 4, 3, .6, 1e-3, 50), steps_needed(gb, 4, 3, .5, 1e-3, 200), steps_needed(lambda x, y: (2 * x, 18 * y), 9, 1, .1, 1e-6, 1000)] == [41, 10, 445, 0, 50, 200, 77])
check('homework-2 long form: s=0.1, factor 0.8, 41 steps', close(max(abs(1 - .2), abs(1 - 1.8)), .8) and 9 * .8 ** 41 < 1e-3 < 9 * .8 ** 40)
check('problems-2 item 2: -0.72, limit .25, 24 steps, slips 3, 21', close(-2 + .8 * 1.6, -.72) and 2 * .8 ** 24 < .01 < 2 * .8 ** 23 and .2 ** 3 < .01 < .2 ** 2 and .8 ** 21 < .01 < .8 ** 20)
# homework-2 item 6: the slip named "signs" (a short gains when its price falls) must give that slip's value
hw6 = J('homework-2')['items'][6]['widget']
key = 800 * 1.2 + (-300) * (-.5) + 150 * 2
slip_b_sign = 800 * 1.2 - 300 * .5 + 150 * 2          # B's term taken as -150: the mistake the feedback names
check('homework-2 item 6 key 1410 and noB 1260', close(key, hw6['answer']) and close(960 + 300, 1260))
check('homework-2 item 6 slip "signs" value equals the named mistake (1110, content has %s)' % hw6['wrong'][0]['value'], close(hw6['wrong'][0]['value'], slip_b_sign))

# ---------------------------------------------------------------- level 3
def classify(fn, p):
    H = hess(fn, p); D = H[0, 0] * H[1, 1] - H[0, 1] ** 2
    return 'saddle' if D < -1e-6 else ('none' if abs(D) <= 1e-6 else ('pit' if H[0, 0] > 0 else 'peak')), D


def mc_type(fn, p, r=1e-2, m=40000):
    """Monte Carlo classification from f itself: sample a small disc round p."""
    d = rng.normal(size=(m, 2)); d = d / np.linalg.norm(d, axis=1)[:, None] * rng.uniform(.2 * r, r, (m, 1))
    v = np.array([fn(p[0] + a, p[1] + b) for a, b in d]) - fn(*p)
    return 'pit' if v.min() >= -1e-14 else ('peak' if v.max() <= 1e-14 else 'saddle')


cases = [(lambda x, y: x ** 3 - 3 * x + y * y, (1, 0), 'pit', 12), (lambda x, y: x ** 3 - 3 * x + y * y, (-1, 0), 'saddle', -12),
         (lambda x, y: x * x + y * y - 2 * x + 4 * y, (1, -2), 'pit', 4), (lambda x, y: x * x - y * y, (0, 0), 'saddle', -4),
         (lambda x, y: 6 * x - x * x + x * y - y * y, (4, 2), 'peak', 3), (lambda x, y: x * x + 4 * x * y + y * y, (0, 0), 'saddle', -12),
         (lambda x, y: 10 * x + 8 * y - x * x - y * y - x * y, (4, 2), 'peak', 3), (lambda x, y: x * x + 3 * x * y + y * y, (0, 0), 'saddle', -5),
         (lambda x, y: x * x + 2 * y * y - 4 * x + 4 * y, (2, -1), 'pit', 8), (lambda x, y: x ** 3 + y ** 3 - 3 * x - 12 * y, (-1, -2), 'peak', 72),
         (lambda x, y: x ** 3 + y ** 3 - 3 * x - 12 * y, (1, 2), 'pit', 72), (lambda x, y: x ** 3 + y ** 3 - 3 * x - 12 * y, (1, -2), 'saddle', -72),
         (lambda x, y: x ** 3 + y ** 3 - 3 * x * y, (0, 0), 'saddle', -9), (lambda x, y: x ** 3 + y ** 3 - 3 * x * y, (1, 1), 'pit', 27),
         (lambda x, y: x ** 4 + y ** 4 - 4 * x * y, (0, 0), 'saddle', -16), (lambda x, y: x ** 4 + y ** 4 - 4 * x * y, (1, 1), 'pit', 128),
         (lambda x, y: 2 * x ** 3 - 6 * x * y + 3 * y * y, (0, 0), 'saddle', -36), (lambda x, y: 2 * x ** 3 - 6 * x * y + 3 * y * y, (1, 1), 'pit', 36),
         (lambda x, y: 14 * x + 6 * y - x * x - y * y, (7, 3), 'peak', 4), (lambda x, y: -.4 * x * x + .5 * x * y - .1 * y * y, (0, 0), 'saddle', -.09)]
for fn, p, typ, D in cases:
    t, d = classify(fn, p)
    check('L3 stationary, D and type at %s' % (p,), np.allclose(grad(fn, p), 0, atol=1e-5) and abs(d - D) < 1e-3 * max(1, abs(D)) and t == typ and mc_type(fn, p) == typ)
# D = 0 gives no verdict: both behaviours occur
check('l10 D=0: x^4+y^4 pit, x^4-y^4 saddle, (x-y)^2 lowest along y=x', mc_type(lambda x, y: x ** 4 + y ** 4, (0, 0)) == 'pit' and mc_type(lambda x, y: x ** 4 - y ** 4, (0, 0)) == 'saddle'
      and classify(lambda x, y: (x - y) ** 2, (2, 2))[0] == 'none' and mc_type(lambda x, y: (x - y) ** 2, (2, 2)) == 'pit')
# review-3 item 8: at |k| = 2 the origin is still a lowest point (not strict). NOTE only: imprecise, finding 4.
if mc_type(lambda x, y: x * x + 2 * x * y + y * y, (0, 0)) == 'pit' and J('review-3')['items'][8]['widget']['options'][0]['text'] == '$-2 < k < 2$' \
        and 'derivative test' not in J('review-3')['items'][8]['question']:
    notes.append('review-3 item 8: at k = +-2 the origin is a (non-strict) lowest point, which l10 s6 calls a pit; the key -2 < k < 2 leaves it out')
check('l9 values: 28 at (4,2); quiz 2 points', close(40 + 16 - 16 - 4 - 8, 28) and np.allclose(grad(lambda x, y: x * x - y ** 3 + 3 * y, (0, -1)), 0, atol=1e-6))
check('homework-3 item 6 global minimum -2 (grid search on [-3,3]^2, f > 0 outside)', abs(min(x ** 4 + y ** 4 - 4 * x * y for x in np.linspace(-3, 3, 601) for y in np.linspace(-3, 3, 601)) + 2) < 1e-6)
check('problems-3 item 0: -1 is a local pit only', 2 * (-10) ** 3 < -1)


# Lagrange: brute force on the constraint curve
def best_on_line(fn, a, b, c, lo=-50, hi=50, m=2000001, mode=max):  # ax + by = c, parametrised by x
    xs = np.linspace(lo, hi, m); ys = (c - a * xs) / b; v = fn(xs, ys); i = v.argmax() if mode is max else v.argmin()
    return v[i], xs[i], ys[i]


def best_on_circle(fn, R2, mode=max, m=2000001):
    t = np.linspace(0, 2 * np.pi, m); xs, ys = math.sqrt(R2) * np.cos(t), math.sqrt(R2) * np.sin(t); v = fn(xs, ys); i = v.argmax() if mode is max else v.argmin()
    return v[i], xs[i], ys[i]


xy = lambda x, y: x * y
check('l11 xy on x+y=10: 25 at (5,5); no smallest value', np.allclose(best_on_line(xy, 1, 1, 10), (25, 5, 5), atol=1e-3) and best_on_line(xy, 1, 1, 10, mode=min)[0] < -1000)
check('l11 shadow price: best on x+y=10.2 is 26.01, estimate 26', close(best_on_line(xy, 1, 1, 10.2)[0], 26.01, 1e-6) and close(25 + 5 * .2, 26))
check('l11 s2 x+2y on circle 5: 5 at (1,2), -5 at (-1,-2)', np.allclose(best_on_circle(lambda x, y: x + 2 * y, 5), (5, 1, 2), atol=1e-3) and np.allclose(best_on_circle(lambda x, y: x + 2 * y, 5, min), (-5, -1, -2), atol=1e-3))
check('l11 s3 lambda 0; s5 4 at (2,2), lambda 1/4', np.allclose(best_on_line(lambda x, y: (x - 1) ** 2 + (y - 1) ** 2, 1, 1, 2, mode=min), (0, 1, 1), atol=1e-3) and np.allclose(best_on_circle(lambda x, y: x + y, 8), (4, 2, 2), atol=1e-3) and close(1 / (2 * 2), .25))
pr = lambda x, y: 3 * x + 4 * y
check('l11 s8 25 at (3,4), lambda .5 = d/dR 5 sqrt R; slips', np.allclose(best_on_circle(pr, 25), (25, 3, 4), atol=1e-3) and close((best_on_circle(pr, 25.01)[0] - best_on_circle(pr, 24.99)[0]) / .02, .5, 1e-4) and abs(7 * math.sqrt(12.5) - 24.75) < .01)
check('l11 quiz 9, 8, 25.98; homework-3 30, 30.5, 20', close(best_on_line(xy, 1, 1, 6)[0], 9, 1e-6) and close(best_on_line(lambda x, y: x * x + y * y, 1, 1, 4, mode=min)[0], 8, 1e-6) and abs(best_on_circle(pr, 27)[0] - 25.98) < 5e-3
      and close(best_on_circle(pr, 36)[0], 30, 1e-9) and close(25 + .5 * 11, 30.5) and close(best_on_line(lambda x, y: x * x + y * y, 1, 2, 10, mode=min)[0], 20, 1e-6))
check('review-3 18 at (3,6); 5 at (2,1)', np.allclose(best_on_line(xy, 2, 1, 12), (18, 3, 6), atol=1e-3) and np.allclose(best_on_circle(lambda x, y: 2 * x + y, 5), (5, 2, 1), atol=1e-3))
Pf = lambda x, y: 14 * x + 6 * y - x * x - y * y
check('problems-3 item 1: 50 at (5,1), lambda 4, exact 51.875, estimate 52', np.allclose(best_on_line(Pf, 1, 1, 6), (50, 5, 1), atol=1e-3) and close(best_on_line(Pf, 1, 1, 6.5)[0], 51.875, 1e-6) and close(14 - 10, 4))
# Monte Carlo: lambda = d(best value)/dc for random concave quadratics on random lines (sign and size of the shadow price, max and min alike)
ok = True
for _ in range(300):
    A = rng.normal(size=(2, 2)); Q = -(A @ A.T + .1 * np.eye(2)); q = rng.normal(size=2); a = rng.normal(size=2); c = rng.normal()
    sol = lambda c: np.linalg.solve(np.block([[2 * Q, -a[:, None]], [a[None, :], np.zeros((1, 1))]]), np.r_[-q, c])
    val = lambda c: (lambda z: z[:2] @ Q @ z[:2] + q @ z[:2])(sol(c))
    ok &= close((val(c + 1e-5) - val(c - 1e-5)) / 2e-5, sol(c)[2], 1e-5)
check('MC 300 random problems: lambda equals the slope of the best value in c', ok)


# l12 minimum variance
def mv(s1, s2, r):
    return (s2 * s2 - r * s1 * s2) / (s1 * s1 + s2 * s2 - 2 * r * s1 * s2)


var = lambda w, s1, s2, r: w * w * s1 * s1 + (1 - w) ** 2 * s2 * s2 + 2 * w * (1 - w) * r * s1 * s2
w = mv(.2, .1, .3)
check('l12 w1 .10526, sigma 9.79%, coefficients, lambda .01916 = 2 var', abs(w - .10526) < 1e-5 and abs(math.sqrt(var(w, .2, .1, .3)) - .09787) < 1e-5 and close(.04 + .01 - .012, .038) and close(-.02 + .012, -.008)
      and abs(.08 * w + .012 * (1 - w) - .01916) < 1e-5 and close(.08 * w + .012 * (1 - w), 2 * var(w, .2, .1, .3)))
check('l12 half 12.45%; rho -1 third; rho 1 formula -1 hedges', abs(math.sqrt(var(.5, .2, .1, .3)) - .1245) < 5e-5 and close(mv(.2, .1, -1), 1 / 3) and close(var(1 / 3, .2, .1, -1), 0, 1e-12) and close(mv(.2, .1, 1), -1) and abs(var(-1, .2, .1, 1)) < 1e-15)
check('l12 s6 13.4% at 20%, 16.8% half; s9 1.3 and 19%', close(mv(.3, .15, 0), .2) and abs(math.sqrt(var(.2, .3, .15, 0)) - .1342) < 1e-4 and abs(math.sqrt(var(.5, .3, .15, 0)) - .1677) < 1e-4 and close(mv(.15, .25, .8), 1.3) and abs(math.sqrt(var(.5, .15, .25, .8)) - .1904) < 1e-4)
check('review-3 .8, 14.14%; homework-3 .21429, .26471', close(mv(.1, .2, 0), .8) and close(math.sqrt(var(.5, .2, .2, 0)), .1414, 1e-3) and abs(mv(.25, .15, .2) - .21429) < 1e-5 and abs(.0225 / .085 - .26471) < 1e-5)
w = mv(.3, .2, .4)
check('homework-3 long form .1951, 19.20%, lambda .07376, rho -1 .4, rho .9 -.636', abs(w - .1951) < 1e-4 and abs(math.sqrt(var(w, .3, .2, .4)) - .1920) < 1e-4 and abs(.18 * w + .048 * (1 - w) - .07376) < 1e-5 and close(mv(.3, .2, -1), .4) and abs(mv(.3, .2, .9) + .636) < 1e-3)
w = mv(.4, .25, .3)
check('problems-3 item 2 .2, .2366, .112, .05826 exact against .05824', close(w, .2) and abs(math.sqrt(var(.2, .4, .25, .3)) - .2366) < 1e-4 and close(.32 * .2 + .06 * .8, .112) and abs(.056 * 1.02 ** 2 - .05826) < 1e-5 and close(.056 + .112 * .02, .05824))
# Monte Carlo over 100,000 random pairs: the general claims of l12
s1 = rng.uniform(.02, .6, 100000); s2 = rng.uniform(.02, .6, 100000); r = rng.uniform(-.999, .999, 100000)
ws = (s2 * s2 - r * s1 * s2) / (s1 * s1 + s2 * s2 - 2 * r * s1 * s2)
grid = np.linspace(0, 1, 2001)[:, None]
vg = grid ** 2 * s1 ** 2 + (1 - grid) ** 2 * s2 ** 2 + 2 * grid * (1 - grid) * r * s1 * s2
check('l12 MC: denominator Var(RA-RB) > 0', (s1 * s1 + s2 * s2 - 2 * r * s1 * s2 > 0).all())
check('l12 MC: clipping w* to [0,1] gives the long-only minimum', np.abs(grid[vg.argmin(0), 0] - np.clip(ws, 0, 1)).max() <= 5.1e-4)
calm2 = s2 < s1
check('l12 quiz MC: long-only minimum is all in the calmer asset exactly when rho >= s_calm/s_risky', ((np.clip(ws, 0, 1) == 0)[calm2] == (r >= s2 / s1)[calm2]).all())
check('l12 quiz MC: never more of the riskier asset; never riskier than the calmer asset alone', (np.clip(ws, 0, 1)[calm2] < .5).all() and (vg.min(0) <= np.minimum(s1, s2) ** 2 + 1e-15).all())
check('l12 MC: lambda = 2 sigma_p^2 at the unconstrained minimum', np.allclose(2 * ws * s1 ** 2 + 2 * (1 - ws) * r * s1 * s2, 2 * (ws ** 2 * s1 ** 2 + (1 - ws) ** 2 * s2 ** 2 + 2 * ws * (1 - ws) * r * s1 * s2)))

print('%d checks, %d failing' % (n, len(fails)))
for x in fails: print('FAIL', x)
for x in notes: print('NOTE', x)
sys.exit(1 if fails else 0)
