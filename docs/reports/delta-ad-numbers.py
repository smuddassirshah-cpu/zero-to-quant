#!/usr/bin/env python3
"""Delta read AD-1: recompute, by two routes, every key, wrong value and printed number of the problems
that three fix passes re-authored or re-keyed (analysis/problems-4, -5; odes/problems-4; vector-calc/problems-1..3).
Run from the repo root with the scratchpad venv Python (sympy, scipy, numpy).
Exit 0 on correct content. A check that fails on wrong content stays failing and is a finding of
docs/reviews/review-delta-ad-1.md (rows marked FINDING name the finding number)."""
import json, re, sys, glob, math
import sympy as sp
from scipy import integrate, optimize
import numpy as np

C = 'app/content/courses/'
fails = []; n = 0


def chk(name, cond, finding=None):
    global n
    n += 1
    if not cond:
        fails.append((name, finding))
        print(('FINDING %s: ' % finding if finding else 'FAIL: ') + name)


def close(a, b, t=1e-6):
    return abs(float(a) - float(b)) <= t


def load(path):
    return {i['id']: i for i in json.load(open(C + path))['items']}


def text(o):
    """Every learner-facing string of an item, joined."""
    out = []
    def w(x, k=None):
        if isinstance(x, dict):
            for kk, v in x.items():
                w(v, kk)
        elif isinstance(x, list):
            for v in x:
                w(v, k)
        elif isinstance(x, str) and k not in ('id', 'kind', 'keyboard', 'layout'):
            out.append(x)
    w(o)
    return ' '.join(out)


def nrm(s):
    for a in ('\\,', '\\ ', '\\;', '\\left', '\\right', '\\big', '\\Big'):
        s = s.replace(a, '')
    s = s.replace('\\tfrac', '\\frac').replace('\\dfrac', '\\frac')
    return re.sub(r'\s+', '', s)


def decimals(s):
    return set(re.findall(r'(?<![\d.])\d+\.\d+(?![\d])', s))


def bands(item, k, key, printed, wrongs):
    """Part k (1-based): key band takes key and the printed value(s), refuses each wrong, wrong bands clear of key."""
    w = item['parts'][k - 1]['widget']
    tol = w['tol']['abs']
    chk(f"{item['id']} part {k} stored key {w['answer']} = recomputed {key}", close(w['answer'], key, max(tol, 1e-9) * 0.2 + 1e-7))
    for p in printed:
        chk(f"{item['id']} part {k} key band takes printed {p}", abs(p - w['answer']) <= tol + 1e-9)
    got = {x['id']: x for x in w.get('wrong', [])}
    chk(f"{item['id']} part {k} wrong ids {sorted(got)} = {sorted(wrongs)}", set(got) == set(wrongs))
    by = item['parts'][k - 1]['feedback'].get('byKey', {})
    for wid, val in wrongs.items():
        if wid not in got:
            continue
        x = got[wid]
        chk(f"{item['id']} part {k} wrong {wid} {x['value']} = recomputed {val}", close(x['value'], val, x['tol']['abs'] * 0.2 + 1e-7))
        chk(f"{item['id']} part {k} wrong {wid} clear of key band", abs(x['value'] - w['answer']) > tol + x['tol']['abs'] + 1e-9)
        chk(f"{item['id']} part {k} wrong {wid} has a byKey line", wid in by)
    vals = [x['value'] for x in w.get('wrong', [])]
    tl = [x['tol']['abs'] for x in w.get('wrong', [])]
    for i in range(len(vals)):
        for j in range(i):
            chk(f"{item['id']} part {k} wrong bands {i},{j} disjoint", abs(vals[i] - vals[j]) > tl[i] + tl[j])


def expr_eq(tex_map, sym, target):
    """Parse a stored tex answer through a tiny hand map and compare with the recomputed expression."""
    return sp.simplify(tex_map - target) == 0


def has(item, *subs):
    t = nrm(text(item))
    for s in subs:
        chk(f"{item['id']} prints {s}", nrm(s) in t)


def gone(item, *subs):
    t = nrm(text(item))
    for s in subs:
        chk(f"{item['id']} holds no old-version {s}", nrm(s) not in t)


def only_decimals(item, allowed):
    d = decimals(text(item)) | {repr(x['value']) for p in item['parts'] for x in p['widget'].get('wrong', []) if isinstance(x.get('value'), float)}
    extra = sorted(x for x in d if x not in allowed)
    chk(f"{item['id']} every printed decimal is a recomputed one (unexplained: {extra})", not extra)


def restates(item, k, *subs):
    q = nrm(item['parts'][k - 1]['question'])
    for s in subs:
        chk(f"{item['id']} part {k} question restates {s}", nrm(s) in q)


x, y, t, s, u, nn = sp.symbols('x y t s u n', real=True)

# ====================================================================== analysis/problems-5
A5 = load('analysis/problems-5.json')

# ---- p-root-sums: sqrt x on [0, 9]
it = A5['p-root-sums']
U9 = sum(sp.sqrt(k) for k in range(1, 10)); L9 = sum(sp.sqrt(k) for k in range(0, 9))
U9n = float(np.sum(np.sqrt(np.arange(1, 10)))); L9n = float(np.sum(np.sqrt(np.arange(0, 9))))
chk('root: U9 two routes', close(U9, U9n, 1e-12) and close(L9, L9n, 1e-12))
chk('root: printed roots add to 19.3060', close(1 + 1.41421 + 1.73205 + 2 + 2.23607 + 2.44949 + 2.64575 + 2.82843 + 3, 19.3060, 5e-5))
for k_, v in zip(range(2, 9), (1.41421, 1.73205, 2, 2.23607, 2.44949, 2.64575, 2.82843)):
    chk(f'root: sqrt{k_} printed {v}', close(math.sqrt(k_), v, 5.1e-6))
chk('root: U9 - L9 = 3', sp.simplify(U9 - L9 - 3) == 0)
bands(it, 1, U9n, [19.3060], {'lower': L9n, 'ninth': U9n / 9})
# part 2: gap for n equal pieces, by telescoping and by brute force for several n
gap = sp.Rational(9) / nn * (sp.sqrt(9) - sp.sqrt(0))
chk('root: gap formula 27/n', sp.simplify(gap - 27 / nn) == 0)
for m in (9, 50, 541):
    xs = np.linspace(0, 9, m + 1); g = (9 / m) * (np.sqrt(xs[1:]).sum() - np.sqrt(xs[:-1]).sum())
    chk(f'root: brute gap at n={m}', close(g, 27 / m, 1e-9))
w = it['parts'][1]['widget']
chk('root: part 2 key and accept', w['answer'] == '\\frac{27}{n}' and set(w['accept']) == {'27/n', '27n^{-1}'})
chk('root: part 2 wrong tex', {x['id']: x['tex'] for x in w['wrong']} == {'unit-width': '\\frac{3}{n}', 'no-height': '\\frac{9}{n}'})
I = sp.integrate(sp.sqrt(x), (x, 0, 9)); In = integrate.quad(lambda z: math.sqrt(z), 0, 9)[0]
chk('root: integral 18 two routes', I == 18 and close(In, 18, 1e-8))
chk('root: G(x) = 2/3 x^(3/2) differentiates to sqrt x', sp.simplify(sp.diff(sp.Rational(2, 3) * x ** sp.Rational(3, 2), x) - sp.sqrt(x)) == 0)
bands(it, 3, 18, [18], {'no-coeff': 27, 'flip': 1.5 * 27})
bands(it, 4, U9n - 18, [1.3060, 19.3060 - 18], {'gap': 3, 'lower': 18 - L9n})
smallest = next(m for m in range(1, 5000) if sp.Rational(27, m) < sp.Rational(5, 100))
chk('root: smallest n two routes', smallest == 541 and math.floor(27 / 0.05 + 1e-9) + 1 == 541)
chk('root: 27/540 is 0.05 itself', sp.Rational(27, 540) == sp.Rational(1, 20))
bands(it, 5, 541, [541], {'equal': 540,
                         'unit-width': next(m for m in range(1, 5000) if sp.Rational(3, m) < sp.Rational(1, 20)),
                         'no-height': next(m for m in range(1, 5000) if sp.Rational(9, m) < sp.Rational(1, 20))})
chk('root: L9 <= 18 <= U9', L9n < 18 < U9n)
has(it, '[0, 9]', 'nine pieces of width 1', 'U_9', '\\sqrt9 - \\sqrt0 = 3', '\\frac{27}{n}', '\\frac23 \\cdot 9^{3/2} - 0 = \\frac23 \\cdot 27 = 18',
    '19.3060 - 18 = 1.3060', 'L_9 \\approx 16.3060', 'n > 540', '\\frac{27}{540}')
restates(it, 4, '19.3060', '18'); restates(it, 5, '\\frac{27}{n}', '18')
gone(it, '[0, 4]', 'U_4', 'L_4', '\\frac{16}{3}', '\\frac8n', '\\frac{8}{n}', '6.146', '0.02', '401', 'four pieces', 'quarter', '0.8129', '\\frac4n')
only_decimals(it, {'19.3060', '19.30600', '19.3060005', '16.3060', '16.3060005', '2.1451112', '1.3060', '1.30600', '1.3060005',
                   '1.6939995', '40.5', '0.05', '1.41421', '1.73205', '2.23607', '2.44949', '2.64575', '2.82843'})

# ---- p-diamond-ball: p = (0.15, -0.4)
it = A5['p-diamond-ball']
p = (sp.Rational(15, 100), sp.Rational(-4, 10))
d1 = abs(p[0]) + abs(p[1]); r = 1 - d1
chk('diamond: d1 = 0.55, r = 0.45', d1 == sp.Rational(55, 100) and r == sp.Rational(45, 100))
straight = math.hypot(0.15, 0.4)
chk('diamond: straight-line distance is sqrt 0.1825', close(straight ** 2, 0.1825, 1e-12))
bands(it, 1, 0.55, [0.55], {'signs': 0.15 - 0.4, 'signs-size': abs(0.15 - 0.4), 'straight': straight, 'largest': 0.4})
bands(it, 2, 0.45, [0.45], {'whole': 0.55, 'straight': 1 - straight})
# r is the largest radius: the edge point is at d1 distance exactly r from p and on the edge of U
e = (sp.Rational(375, 1000), sp.Rational(-625, 1000))
chk('diamond: edge point at d1 distance 0.45 from p, on the edge', abs(e[0] - p[0]) + abs(e[1] - p[1]) == r and abs(e[0]) + abs(e[1]) == 1)
# brute force: largest d1 ball round p inside U
rng = np.random.default_rng(1); worst = 1.0
ang = np.linspace(0, 2 * np.pi, 20001)
# d1 sphere of radius rho round p: points p + rho*(a, b), |a|+|b| = 1; sup of d1(0, .) over it is 0.55 + rho
for rho in (0.44, 0.45, 0.46):
    a = np.linspace(-1, 1, 4001); b = 1 - np.abs(a)
    sup = max(np.max(np.abs(0.15 + rho * a) + np.abs(-0.4 + rho * b)), np.max(np.abs(0.15 + rho * a) + np.abs(-0.4 - rho * b)))
    chk(f'diamond: sup of d1(0, y) on the d1 sphere of radius {rho} is 0.55 + rho', close(sup, 0.55 + rho, 1e-9))
s_key = 0.45 / math.sqrt(2)
bands(it, 3, s_key, [0.3182, 0.45 / 1.414], {'times': 0.45 * math.sqrt(2), 'same': 0.45, 'half': 0.225})
# true largest disc round p inside U: distance from p to the line x - y = 1 (and the foot is the edge point)
chk('diamond: largest disc is the distance to the edge x - y = 1', close(abs(0.15 + 0.4 - 1) / math.sqrt(2), s_key, 1e-12))
chk('diamond: disc of radius 0.45 pokes out', 0.45 > s_key)
chk('diamond: d1 <= sqrt2 d2 and d1 <= 2 dinf on a sample', all(
    abs(a_) + abs(b_) <= math.sqrt(2) * math.hypot(a_, b_) + 1e-12 and abs(a_) + abs(b_) <= 2 * max(abs(a_), abs(b_)) + 1e-12
    for a_, b_ in rng.normal(size=(2000, 2))))
bands(it, 4, 0.225, [0.225], {'times': 0.9, 'root-two': s_key, 'same': 0.45})
chk('diamond: square corner (0.375, -0.625) = p + (0.225, -0.225)', (p[0] + sp.Rational(225, 1000), p[1] - sp.Rational(225, 1000)) == e)
chk('diamond: square of half-side 0.45 has corners at taxicab 0.9', close(2 * 0.45, 0.9, 1e-12))
has(it, 'p = (0.15, -0.4)', '|0.15| + |-0.4| = 0.15 + 0.4 = 0.55', '0.55 + 0.45 = 1', '(0.375, -0.625)', '\\frac{0.45}{\\sqrt2} \\approx 0.3182',
    '\\frac{0.45}{2} = 0.225', 'half-side 0.225', '\\sqrt{0.1825}', '1 - 0.55 = 0.45')
restates(it, 2, '0.55'); restates(it, 3, '0.45'); restates(it, 4, '0.45')
gone(it, '(0.2', '0.7', '0.2121', '0.35', '0.65', '0.4243')   # the rest of the old decimals: only_decimals below
only_decimals(it, {'0.15', '0.4', '0.55', '0.45', '0.25', '-0.25', '0.4272002', '0.1825', '0.5727998', '0.375', '0.625', '0.3181981',
                   '0.3182', '0.6363961', '0.225', '0.9'})
ch = it['parts'][4]['widget']['options']
chk('diamond: part 5 one correct option, all', [o['id'] for o in ch if o.get('correct')] == ['all'])

# ---- p-accumulated-cubic: t^2 - 12t + 27 on [0, 15]
it = A5['p-accumulated-cubic']
f = t ** 2 - 12 * t + 27
chk('cubic: f factorises', sp.expand((t - 3) * (t - 9) - f) == 0)
F = sp.integrate(f.subs(t, u), (u, 0, x))
chk('cubic: F polynomial and factorised', sp.expand(F - (x ** 3 / 3 - 6 * x ** 2 + 27 * x)) == 0 and sp.expand(F - x * (x - 9) ** 2 / 3) == 0)
Fn = lambda b: integrate.quad(lambda z: z * z - 12 * z + 27, 0, b)[0]
for b, v in ((0, 0), (3, 36), (9, 0), (15, 180), (14.5, 146.2083333)):
    chk(f'cubic: F({b}) = {v} two routes', close(F.subs(x, sp.nsimplify(b)), v, 1e-6) and close(Fn(b), v, 1e-6))
chk('cubic: zeros of F prime in (0, 15)', sorted(sp.solve(sp.diff(F, x), x)) == [3, 9] and it['parts'][1]['widget']['answers'] == [3, 9])
chk('cubic: zeros-of-big-f slip is 0, 9', sorted(set(sp.solve(F, x))) == [0, 9] and it['parts'][1]['widget']['wrong'][0]['value'] == '0, 9')
grid = np.linspace(0, 15, 150001); Fg = grid ** 3 / 3 - 6 * grid ** 2 + 27 * grid
chk('cubic: max of F on [0, 15] is 180 at 15 only (grid)', close(Fg.max(), 180, 1e-9) and Fg.argmax() == len(grid) - 1 and Fg[:-1].max() < 180)
chk('cubic: F(15) arithmetic 3375/3 - 1350 + 405', sp.Rational(3375, 3) - 1350 + 405 == 180 and 15 ** 3 == 3375 and 6 * 225 == 1350 and 27 * 15 == 405)
bands(it, 3, 180, [180], {'critical': 36, 'no-third': 15 ** 3 - 6 * 225 + 405})
fg = grid ** 2 - 12 * grid + 27
chk('cubic: sup |f| on [0, 15] is 72 at 15; f(0) = 27', close(np.abs(fg).max(), 72, 1e-9) and np.abs(fg).argmax() == len(grid) - 1 and f.subs(t, 0) == 27 and f.subs(t, 15) == 72)
sm = next(m for m in range(1, 5000) if sp.Rational(72, m) < sp.Rational(7, 100))
chk('cubic: smallest n 1029 two routes', sm == 1029 and math.floor(72 / 0.07) + 1 == 1029)
chk('cubic: 72/0.07 is about 1028.6 and 72/1028 about 0.07004', round(72 / 0.07, 1) == 1028.6 and round(72 / 1028, 5) == 0.07004)
bands(it, 5, 1029, [1029], {'round-down': 1028, 'left-end': next(m for m in range(1, 5000) if sp.Rational(27, m) < sp.Rational(7, 100)),
                           'no-bound': next(m for m in range(1, 5000) if sp.Rational(1, m) < sp.Rational(7, 100))})
chk('cubic: true gap at n = 1029 is below 0.07, and F(x_n) < 180', 0 < 180 - float(F.subs(x, 15 - sp.Rational(1, 1029))) < 0.07)
w = it['parts'][0]['widget']
chk('cubic: part 1 key, accept, wrong tex', w['answer'] == '\\frac{x^3}{3}-6x^2+27x' and set(w['accept']) == {'x^3/3-6x^2+27x', '\\frac{x(x-9)^2}{3}'}
    and {q['id']: q['tex'] for q in w['wrong']} == {'no-third': 'x^3-6x^2+27x', 'no-half': '\\frac{x^3}{3}-12x^2+27x', 'derivative': '2x-12'})
chk('cubic: derivative slip is f prime', sp.diff(f, t) == 2 * t - 12)
ch = it['parts'][3]['widget']['options']
chk('cubic: part 4 one correct option, not-closed', [o['id'] for o in ch if o.get('correct')] == ['not-closed'])
has(it, '[0, 15]', 't^2 - 12t + 27 = (t - 3)(t - 9)', 'F(3) = 36', 'F(15) = 180', '\\frac{72}{n}', 'F(14.5) \\approx 146.21', '15 - \\frac1n',
    '[0, 15)', 'f(0) = 27', '180 - 0.07')
restates(it, 3, '3 and 9'); restates(it, 4, '180'); restates(it, 5, '180', '72')
gone(it, '[0, 5]', '[0, 5)', 't^2 - 4t + 3', '(t - 1)(t - 3)', '(x - 1)(x - 3)', '\\frac{20}{3}', '\\frac8n', '0.003', '2667', '2666', '-2x^2')
only_decimals(it, {'0.07', '1028.6', '0.07004', '14.5', '146.21'})
# reuse guard: the integrand must not be a quadratic another course factorises (the fix pass's own rule for (t-2)(t-6))
qs = nrm(open(C + 'quadratics/l2-product-and-sum.json').read().replace('\\\\', '\\'))
# Main session ruling (finding 1 of review-delta-ad-1.md, not applied): a simple quadratic with small whole roots, shared with a
# factorising exercise of another topic that asks a different task, stands, like the single common fraction of the session AC
# ruling. The check asserts the item is still the ruled one, so the script fails if the function or keys change.
chk('cubic: ruling, t^2 - 12t + 27 stands (shared with quadratics/l2-product-and-sum, a different task)',
    'q^2-12q+27' in qs and '(q-3)(q-9)' in qs and 't^2 - 12t + 27 = (t - 3)(t - 9)' in it['prose'] and it['parts'][0]['widget']['answer'] == '\\frac{x^3}{3}-6x^2+27x'
    and it['parts'][1]['widget']['answers'] == [3, 9] and it['parts'][2]['widget']['answer'] == 180 and it['parts'][4]['widget']['answer'] == 1029)
# the proposed replacement of finding 1: f = t^2 - 24t + 108 = (t - 6)(t - 18) on [0, 27], epsilon 0.11
f2 = t ** 2 - 24 * t + 108; F2 = sp.integrate(f2.subs(t, u), (u, 0, x))
chk('proposal: factorisations', sp.expand((t - 6) * (t - 18) - f2) == 0 and sp.expand(F2 - x * (x - 18) ** 2 / 3) == 0 and sp.expand(F2 - (x ** 3 / 3 - 12 * x ** 2 + 108 * x)) == 0)
chk('proposal: F at 0, 6, 18, 27, 26.5', [F2.subs(x, v) for v in (0, 6, 18, 27)] == [0, 288, 0, 729] and close(F2.subs(x, sp.Rational(53, 2)), 638.2083333, 1e-6))
chk('proposal: F(27) arithmetic', sp.Rational(27 ** 3, 3) == 6561 and 12 * 27 ** 2 == 8748 and 108 * 27 == 2916 and 6561 - 8748 + 2916 == 729 and 27 ** 3 - 8748 + 2916 == 13851)
g2 = np.linspace(0, 27, 270001)
chk('proposal: max of F at 27 only; sup |f| = 189 at 27; f(0) = 108', (g2 ** 3 / 3 - 12 * g2 ** 2 + 108 * g2).argmax() == len(g2) - 1 and close(np.abs(g2 ** 2 - 24 * g2 + 108).max(), 189, 1e-9) and np.abs(g2 ** 2 - 24 * g2 + 108).argmax() == len(g2) - 1)
E = sp.Rational(11, 100)
chk('proposal: smallest n 1719, slips 1718, 982, 10; 189/0.11 = 1718.2; 189/1718 = 0.11001',
    [next(m for m in range(1, 9000) if sp.Rational(k_, m) < E) for k_ in (189, 108, 1)] == [1719, 982, 10] and round(189 / 0.11, 1) == 1718.2 and round(189 / 1718, 5) == 0.11001)
allc = ' '.join(nrm(open(p_).read().replace('\\\\', '\\')) for p_ in glob.glob('app/content/**/*.json', recursive=True) if not p_.endswith('manifest.json'))
chk('proposal: (.-6)(.-18) and .^2-24.+108 appear nowhere in app/content', not re.search(r'\(.-6\)\(.-18\)|.\^2-24.\+108', allc))

# ====================================================================== analysis/problems-4 (root renamed r)
A4 = load('analysis/problems-4.json')
it = A4['p-cubic-bracket']
q4, q5 = it['parts'][3], it['parts'][4]
chk('bracket: parts 4 and 5 call the root r, never c', '$c$' not in text(q4) + text(q5) and 'f(c)' not in text(q4) + text(q5) and 'root $r$' in q4['question'] and 'root $r$' in q5['question'])
chk('bracket: parts 1 and 2 keep c for the mean value point', "f'(c)" in it['parts'][0]['question'] and "f'(c)" in it['parts'][1]['question'])
chk('bracket: 12 halvings, 2/2^12 = 1/2048 <= 0.0005 < 2/2^11; bound 18/4096 = 9/2048 = 0.0043945', sp.Rational(2, 2 ** 12) == sp.Rational(1, 2048) and 1 / 2048 <= 0.0005 < 1 / 1024
    and sp.Rational(18, 4096) == sp.Rational(9, 2048) and close(9 / 2048, q5['widget']['answer'], 5e-8) and q4['widget']['answer'] == 12)

# ====================================================================== odes/problems-4 p-test-rig
O4 = load('odes/problems-4.json')
it = O4['p-test-rig']
tp = sp.symbols('t', positive=True); sv = sp.symbols('s')
yf = sp.Function('y')
sol = sp.dsolve(yf(tp).diff(tp, 2) + 6 * yf(tp).diff(tp) + 8 * yf(tp) - 24 * sp.exp(-8 * tp), yf(tp), ics={yf(0): 0, yf(tp).diff(tp).subs(tp, 0): 0}).rhs
ykey = 2 * sp.exp(-2 * tp) - 3 * sp.exp(-4 * tp) + sp.exp(-8 * tp)
chk('rig: dsolve gives the key y', sp.simplify(sol - ykey) == 0)
num = integrate.solve_ivp(lambda tt, z: [z[1], 24 * math.exp(-8 * tt) - 6 * z[1] - 8 * z[0]], (0, 3), [0, 0], rtol=1e-10, atol=1e-12, dense_output=True)
chk('rig: numerical solution agrees with the key y', all(close(num.sol(tt)[0], float(ykey.subs(tp, tt)), 1e-7) for tt in (0.1, 0.5, 0.5025, 1, 2)))
Y = 24 / ((sv + 2) * (sv + 4) * (sv + 8))
chk('rig: transform of forcing', sp.simplify(sp.laplace_transform(24 * sp.exp(-8 * tp), tp, sv, noconds=True) - 24 / (sv + 8)) == 0)
chk('rig: Y from the equation', sp.simplify(24 / (sv + 8) / (sv ** 2 + 6 * sv + 8) - Y) == 0 and sp.expand((sv + 2) * (sv + 4) - (sv ** 2 + 6 * sv + 8)) == 0)
res = {p_: sp.residue(Y, sv, p_) for p_ in (-2, -4, -8)}
cover = {-2: sp.Rational(24, (2) * (6)), -4: sp.Rational(24, (-2) * (4)), -8: sp.Rational(24, (-6) * (-4))}
chk('rig: residues 2, -3, 1 two routes, adding to 0', res == {-2: 2, -4: -3, -8: 1} and cover == res and sum(res.values()) == 0)
chk('rig: partial fractions', sp.simplify(sp.apart(Y, sv) - (2 / (sv + 2) - 3 / (sv + 4) + 1 / (sv + 8))) == 0)
chk('rig: y(0) = 0, y prime(0) = 0 as printed (2 - 3 + 1, -4 + 12 - 8)', ykey.subs(tp, 0) == 0 and sp.diff(ykey, tp).subs(tp, 0) == 0 and -4 + 12 - 8 == 0)
yu = 2 * u - 3 * u ** 2 + u ** 4
chk('rig: y in u and its factorisations', sp.simplify(ykey.subs(tp, -sp.log(u) / 2) - yu) == 0 and sp.expand(u * (1 - u) ** 2 * (u + 2) - yu) == 0
    and sp.expand(2 * (u - 1) * (2 * u ** 2 + 2 * u - 1) - sp.diff(yu, u)) == 0)
ustar = (sp.sqrt(3) - 1) / 2
chk('rig: u* root of 2u^2 + 2u - 1 in (0, 1)', sp.simplify(2 * ustar ** 2 + 2 * ustar - 1) == 0 and 0 < float(ustar) < 1 and round(float(ustar), 4) == 0.3660)
peak = sp.simplify(yu.subs(u, ustar)); tstar = -sp.log(ustar) / 2
chk('rig: peak (6 sqrt3 - 9)/4 = 0.34808 at t = ln(1 + sqrt3)/2 = 0.5025', close(peak, (6 * math.sqrt(3) - 9) / 4, 1e-12) and close(peak, 0.34808, 5e-6)
    and close(tstar, math.log(1 + math.sqrt(3)) / 2, 1e-12) and close(tstar, 0.5025, 5e-5) and round(float(tstar), 3) == 0.503)
opt = optimize.minimize_scalar(lambda tt: -(2 * math.exp(-2 * tt) - 3 * math.exp(-4 * tt) + math.exp(-8 * tt)), bounds=(0, 5), method='bounded', options={'xatol': 1e-10})
chk('rig: numerical peak agrees', close(-opt.fun, float(peak), 1e-8) and close(opt.x, float(tstar), 1e-5))
tg = np.linspace(0, 10, 100001); yg = 2 * np.exp(-2 * tg) - 3 * np.exp(-4 * tg) + np.exp(-8 * tg)
chk('rig: y never negative (grid), so no overshoot past rest', yg.min() > -1e-12)
y1 = float(ykey.subs(tp, 1))
bands(it, 3, -3, [-3], {'sign': 3, 'other-pole': 2})
bands(it, 5, float(peak), [0.348, 0.3481], {'u-value': float(ustar), 'time': float(tstar), 'at-one': y1})
w = [p_['widget'] for p_ in it['parts']]
chk('rig: expression keys', w[0]['answer'] == '\\frac{24}{s+8}' and w[1]['answer'] == '\\frac{24}{(s+2)(s+4)(s+8)}' and w[3]['answer'] == '2e^{-2t}-3e^{-4t}+e^{-8t}')
chk('rig: expression wrong tex', {q['id']: q['tex'] for q in w[0]['wrong']} == {'sign': '\\frac{24}{s-8}', 'no-factor': '\\frac{1}{s+8}'}
    and {q['id']: q['tex'] for q in w[1]['wrong']} == {'carried-sign': '\\frac{24}{(s-8)(s+2)(s+4)}', 'root-signs': '\\frac{24}{(s+8)(s-2)(s-4)}'}
    and {q['id']: q['tex'] for q in w[3]['wrong']} == {'exp-sign': '2e^{2t}-3e^{4t}+e^{8t}', 'carried-sign': '2e^{-2t}+3e^{-4t}+e^{-8t}'})
chk('rig: carried-sign y has y(0) = 6', 2 + 3 + 1 == 6)
has(it, "y'' + 6y' + 8y = 24e^{-8t}", '\\frac{24}{s + 8}', '\\frac{24}{(-2)(4)} = -3', '\\frac{24}{(2)(6)} = 2', '\\frac{24}{(-6)(-4)} = 1',
    'u(1 - u)^2(u + 2)', '\\frac{6\\sqrt3 - 9}{4} \\approx 0.348', '\\frac12\\ln(1 + \\sqrt3) \\approx 0.503', '\\frac{\\sqrt3 - 1}{2} \\approx 0.3660')
restates(it, 2, '\\frac{24}{s + 8}'); restates(it, 3, '\\frac{24}{(s + 2)(s + 4)(s + 8)}'); restates(it, 4, '2, $-3$ and 1'); restates(it, 5, '2e^{-2t} - 3e^{-4t} + e^{-8t}')
gone(it, '8e^{-3t}', 's + 3', 's+3', '4e^{-2t}', 'e^{-3t}', '0.25', '0.0625', '0.693', 'parabola', '(1 - e^{-t})', 'residues 4')
only_decimals(it, {'0.3481', '0.348', '0.366', '0.3660', '0.5025', '0.503', '0.2161'})

# ====================================================================== vector-calc/problems-1
V1 = load('vector-calc/problems-1.json')

# ---- p-bead-semicircle: radius 6
it = V1['p-bead-semicircle']
Px, Qx = 2 * x - y, x + 2 * y
rx, ry = 6 * sp.cos(t), 6 * sp.sin(t)
mag2 = sp.expand(Px ** 2 + Qx ** 2)
chk('bead: |F|^2 = 5x^2 + 5y^2; |F(1,3)| = sqrt 50', mag2 == 5 * x ** 2 + 5 * y ** 2 and (Px.subs({x: 1, y: 3}), Qx.subs({x: 1, y: 3})) == (-1, 7))
speed = sp.simplify(sp.sqrt(sp.diff(rx, t) ** 2 + sp.diff(ry, t) ** 2))
Fm = sp.simplify(sp.sqrt(mag2.subs({x: rx, y: ry})))
chk('bead: speed 6, |F| = 6 sqrt5 on the circle', speed == 6 and sp.simplify(Fm - 6 * sp.sqrt(5)) == 0)
I3 = sp.integrate(Fm * speed, (t, 0, sp.pi))
I3n = integrate.quad(lambda z: math.hypot(12 * math.cos(z) - 6 * math.sin(z), 6 * math.cos(z) + 12 * math.sin(z)) * 6, 0, math.pi)[0]
chk('bead: int |F| ds = 36 sqrt5 pi two routes', sp.simplify(I3 - 36 * sp.sqrt(5) * sp.pi) == 0 and close(I3n, 36 * math.sqrt(5) * math.pi, 1e-8))
bands(it, 1, math.sqrt(50), [7.071], {'sum': 6, 'no-root': 50, 'abs-sum': 8})
bands(it, 3, I3n, [252.89], {'no-speed': I3n / 6, 'squared': 180 * 6 * math.pi, 'full-circle': 2 * I3n})
dot = sp.simplify(Px.subs({x: rx, y: ry}) * sp.diff(rx, t) + Qx.subs({x: rx, y: ry}) * sp.diff(ry, t))
dotn = [(12 * math.cos(z) - 6 * math.sin(z)) * (-6 * math.sin(z)) + (6 * math.cos(z) + 12 * math.sin(z)) * 6 * math.cos(z) for z in (0.3, 1.1, 2.9)]
chk('bead: F.r prime = 36 two routes', dot == 36 and all(close(v, 36, 1e-9) for v in dotn))
pos = sp.simplify(Px.subs({x: rx, y: ry}) * rx + Qx.subs({x: rx, y: ry}) * ry)
bands(it, 4, 36, [36], {'position': int(pos), 'magnitude': int(sp.simplify(mag2.subs({x: rx, y: ry})))})
W = sp.integrate(dot, (t, 0, sp.pi))
# Green on the closed half disc: curl 2, area 18 pi, the diameter from (-6,0) to (6,0) contributes int 2x dx = 0
chk('bead: work 36 pi, also by Green (curl 2 times area 18 pi, diameter 0)', W == 36 * sp.pi and sp.diff(Qx, x) - sp.diff(Px, y) == 2 and sp.integrate(2 * x, (x, -6, 6)) == 0 and 2 * 18 == 36)
frac = float(W / I3)
bands(it, 5, frac, [0.447], {'inverse': 1 / frac, 'no-integral': 36 / I3n, 'full-circle': 2 * frac})
has(it, 'x^2 + y^2 = 36', '(6, 0)', '(-6, 0)', '(6\\cos t, 6\\sin t)', '6\\sqrt5', '36\\sqrt5\\pi \\approx 252.89', '36\\sin^2 t + 36\\cos^2 t = 36',
    '(12\\cos t - 6\\sin t)(-6\\sin t) + (6\\cos t + 12\\sin t)(6\\cos t)', '36\\pi \\approx 113.10', '|\\mathbf F|^2 = 180', '\\sqrt{180} = 6\\sqrt5', 'which gives 72')
restates(it, 3, '5(x^2 + y^2)'); restates(it, 5, '36', '36\\sqrt5\\pi')
gone(it, '= 9$', '(3, 0)', '(-3, 0)', '3\\cos t', '3\\sin t', '3\\sqrt5', '9\\sqrt5', '63.22', '28.27', '9\\pi', '= 45', '\\sqrt{45}', '9\\sin^2')
only_decimals(it, {'7.0711', '7.071', '252.8933', '252.89', '42.1489', '3392.92', '505.7867', '0.4472', '0.447', '2.2361', '0.1424', '0.8944', '113.10'})
chk('bead: 36 pi = 113.10', round(36 * math.pi, 2) == 113.10)

# ---- p-two-routes-cubic: (0,0) to (2,8)
it = V1['p-two-routes-cubic']
P2_, Q2_ = x * y, x + y
def work(rx_, ry_, a, b):
    return sp.integrate(P2_.subs({x: rx_, y: ry_}) * sp.diff(rx_, t) + Q2_.subs({x: rx_, y: ry_}) * sp.diff(ry_, t), (t, a, b))
integrandA = sp.expand(P2_.subs({x: t, y: t ** 3}) * 1 + Q2_.subs({x: t, y: t ** 3}) * 3 * t ** 2)
chk('routes: integrand on A', integrandA == t ** 4 + 3 * t ** 3 + 3 * t ** 5)
WA, WB = work(t, t ** 3, 0, 2), work(t, 4 * t, 0, 2)
WAn = integrate.quad(lambda z: z * z ** 3 + (z + z ** 3) * 3 * z * z, 0, 2)[0]; WBn = integrate.quad(lambda z: z * 4 * z + (z + 4 * z) * 4, 0, 2)[0]
chk('routes: W_A = 252/5, W_B = 152/3 two routes; both routes end at (2, 8)', WA == sp.Rational(252, 5) and WB == sp.Rational(152, 3) and close(WAn, 50.4, 1e-9) and close(WBn, 152 / 3, 1e-9) and 2 ** 3 == 8 and 4 * 2 == 8)
chk('routes: pieces 32/5, 12, 32 and 32/3, 40', [sp.integrate(e_, (t, 0, 2)) for e_ in (t ** 4, 3 * t ** 3, 3 * t ** 5, 4 * t ** 2, 20 * t)] == [sp.Rational(32, 5), 12, 32, sp.Rational(32, 3), 40])
bands(it, 2, 50.4, [50.4], {'no-dot': float(sp.integrate(t ** 4 + t ** 3 + t, (t, 0, 2))), 'no-chain': float(sp.integrate(t ** 4 + t ** 3 + t ** 5, (t, 0, 2)))})
bands(it, 3, 152 / 3, [50.667], {'ds': 152 / 3 * math.sqrt(17), 'p-only': 32 / 3, 'q-only': 40, 'no-four': float(sp.integrate(4 * t ** 2 + 5 * t, (t, 0, 2)))})
loop = WA - WB
green = sp.integrate(sp.integrate(sp.diff(Q2_, x) - sp.diff(P2_, y), (y, x ** 3, 4 * x)), (x, 0, 2))   # A below B, so out on A and back on B is anticlockwise
chk('routes: loop -4/15 two routes (difference, Green); 756 - 760', loop == sp.Rational(-4, 15) and green == loop and 252 * 3 == 756 and 152 * 5 == 760)
bands(it, 4, -4 / 15, [-0.2667], {'added': float(WA + WB), 'sign': 4 / 15})
chk('routes: P_y = x, Q_x = 1', sp.diff(P2_, y) == x and sp.diff(Q2_, x) == 1)
ch = it['parts'][4]['widget']['options']
chk('routes: part 5 one correct option a', [o['id'] for o in ch if o.get('correct')] == ['a'])
w = it['parts'][0]['widget']
chk('routes: part 1 key and wrong tex', w['answer'] == 't^4+3t^3+3t^5' and {q['id']: q['tex'] for q in w['wrong']} == {'no-dot': 't^4+t^3+t', 'no-chain': 't^4+t^3+t^5'})
has(it, '(2, 8)', '(t, 4t)', '0 \\le t \\le 2', '\\frac{32}{5} + 12 + 32 = \\frac{252}{5} = 50.4', '(4t^2, 5t)', '\\frac{152}{3} \\approx 50.667', '\\frac{756 - 760}{15} = -\\frac{4}{15} \\approx -0.2667',
    '\\sqrt{17}', '\\frac{32}{3} + 40 = \\frac{152}{3}')
restates(it, 2, 't^4 + 3t^3 + 3t^5'); restates(it, 4, '\\frac{252}{5}', '\\frac{152}{3}'); restates(it, 5, '-\\frac{4}{15}')
gone(it, 'to $(1, 1)$', '(t, t)$', '0 \\le t \\le 1', '\\frac{29}{20}', '\\frac43', '\\frac{7}{60}', '1.45', '1.333', '0.1167', '\\sqrt2', 'int_0^1')
only_decimals(it, {'50.4', '12.4', '21.0667', '50.66667', '50.667', '208.904', '10.6667', '20.6667', '101.0667', '0.266667', '-0.266667', '0.2667'})

# ---- p-cubic-potential: F = (4x^3 + 3y^2, 6xy)
it = V1['p-cubic-potential']
P3_, Q3_ = 4 * x ** 3 + 3 * y ** 2, 6 * x * y
fpot = x ** 4 + 3 * x * y ** 2
chk('potential: F(1,2) = (16, 12); slips (10, 12)', (P3_.subs({x: 1, y: 2}), Q3_.subs({x: 1, y: 2})) == (16, 12) and 4 + 3 * 2 == 10)
chk('potential: P_y = Q_x = 6y; P_x = 12x^2; Q_y = 6x', sp.diff(P3_, y) == 6 * y == sp.diff(Q3_, x) and sp.diff(P3_, x) == 12 * x ** 2 and sp.diff(Q3_, y) == 6 * x)
chk('potential: grad f = F and f(0,0) = 0', sp.diff(fpot, x) == P3_ and sp.diff(fpot, y) == Q3_ and fpot.subs({x: 0, y: 0}) == 0)
chk('potential: slips are int P dx + int Q dy and int 6xy dx', sp.expand(sp.integrate(P3_, x) + sp.integrate(Q3_, y) - (x ** 4 + 6 * x * y ** 2)) == 0 and sp.integrate(Q3_, x) == 3 * x ** 2 * y)
Wp = fpot.subs({x: 2, y: 3}) - fpot.subs({x: 1, y: 0})
line = sp.integrate((P3_ * 1 + Q3_ * 3).subs({x: 1 + t, y: 3 * t}), (t, 0, 1))
bent = sp.integrate(P3_.subs(y, 0), (x, 1, 2)) + sp.integrate(Q3_.subs(x, 2), (y, 0, 3))
chk('potential: work 69 three routes; f(2,3) = 70 = 16 + 54, f(1,0) = 1', Wp == 69 == line == bent and fpot.subs({x: 2, y: 3}) == 70 and 2 ** 4 == 16 and 3 * 2 * 9 == 54)
bands(it, 4, 69, [69], {'end-only': 70, 'double': int((x ** 4 + 6 * x * y ** 2).subs({x: 2, y: 3}) - 1)})
w = [p_['widget'] for p_ in it['parts']]
chk('potential: expression keys and wrong tex', w[0]['answer'] == '(16, 12)' and w[1]['answer'] == '6y' and w[2]['answer'] == 'x^4+3xy^2'
    and {q['id']: q['tex'] for q in w[0]['wrong']} == {'y-not-squared': '(10, 12)', 'swap': '(12, 16)'}
    and {q['id']: q['tex'] for q in w[1]['wrong']} == {'px': '12x^2', 'qy': '6x'}
    and {q['id']: q['tex'] for q in w[2]['wrong']} == {'double': 'x^4+6xy^2', 'wrong-var': 'x^4+3x^2y'})
has(it, '(4x^3 + 3y^2, 6xy)', '4 + 12 = 16', '6 \\times 1 \\times 2 = 12', '(16 + 54) - 1 = 69', 'x^4 + 3xy^2 + g(y)', 'f(2, 3) = 16 + 54 = 70')
restates(it, 3, '6y'); restates(it, 4, 'x^4 + 3xy^2')
gone(it, '3x^2 + y^2', '(2xy', 'x^3 + xy^2', '(7, 4)', '= 2y', '= 25', '6x^2')
only_decimals(it, set())

# ====================================================================== vector-calc/problems-2
V2 = load('vector-calc/problems-2.json')

# ---- p-triangle-flux: (0,0), (3,0), (0,6)
it = V2['p-triangle-flux']
P4_, Q4_ = x ** 2 + y, 2 * x * y
div = sp.diff(P4_, x) + sp.diff(Q4_, y); curl = sp.diff(Q4_, x) - sp.diff(P4_, y)
chk('triangle: div 4x, curl 2y - 1', div == 4 * x and curl == 2 * y - 1)
tri = lambda g: sp.integrate(sp.integrate(g, (y, 0, 6 - 2 * x)), (x, 0, 3))
tot = tri(div)
totn = integrate.dblquad(lambda yy, xx: 4 * xx, 0, 3, lambda xx: 0, lambda xx: 6 - 2 * xx)[0]
chk('triangle: total flux 36 two routes; 108 - 72', tot == 36 and close(totn, 36, 1e-9) and sp.integrate(24 * x, (x, 0, 3)) == 108 and sp.integrate(8 * x ** 2, (x, 0, 3)) == 72)
bands(it, 2, 36, [36], {'curl': int(tri(curl)), 'rectangle': int(sp.integrate(sp.integrate(div, (y, 0, 6)), (x, 0, 3))), 'only-p': int(tri(2 * x))})
left = sp.integrate((-P4_).subs(x, 0), (y, 0, 6)); bottom = sp.integrate((-Q4_).subs(y, 0), (x, 0, 3))
rx_, ry_ = 3 - 3 * t, 6 * t
longe = sp.integrate((P4_.subs({x: rx_, y: ry_}) * sp.diff(ry_, t) - Q4_.subs({x: rx_, y: ry_}) * sp.diff(rx_, t)), (t, 0, 1))
chk('triangle: edges -18, 0, 54 add to 36 (direct edge integrals against the divergence)', left == -18 and bottom == 0 and longe == 54 and left + bottom + longe == tot)
bands(it, 3, -18, [-18], {'sign': 18, 'tangent': int(sp.integrate(Q4_.subs(x, 0), (y, 0, 6)))})
bands(it, 4, 54, [54], {'add-edge': 36 + (-18), 'all-out': 36})
chk('triangle: part 1 key and wrong tex', it['parts'][0]['widget']['answer'] == '4x' and {q['id']: q['tex'] for q in it['parts'][0]['widget']['wrong']} == {'curl': '2y-1', 'only-p': '2x'})
has(it, '(3, 0)', '(0, 6)', '6 - 2x', '\\int_0^3 4x(6 - 2x)dx = 108 - 72 = 36', '(24x - 8x^2)', '[0, 3] \\times [0, 6]', '\\int_0^6 (-y)dy = -18', '36 - 0 - (-18) = 54', '36 + 18 = 54', '(3 - 3t, 6t)', 'The normal form of Green')
restates(it, 2, '4x'); restates(it, 4, '36', '-18')
gone(it, '(4, 0)', '(0, 2)', '\\frac{64}{3}', '21.33', '23.33', '\\frac{70}{3}', '-2$', '2 - \\frac', 'int_0^4', 'int_0^2', 'fraction', 'decimal', 'flux form', 'divergence form')
only_decimals(it, set())

# ---- p-cycloid-arch: wording (mean height), uniqueness of P, two new wrong entries
it = V2['p-cycloid-arch']
yt, xt = 1 - sp.cos(t), t - sp.sin(t)
Aarch = sp.integrate(yt * sp.diff(xt, t), (t, 0, 2 * sp.pi)); M = sp.Rational(1, 2) * sp.integrate(yt ** 2 * sp.diff(xt, t), (t, 0, 2 * sp.pi))
Mn = integrate.quad(lambda z: 0.5 * (1 - math.cos(z)) ** 3, 0, 2 * math.pi)[0]
chk('cycloid: area 3 pi, int y dA = 5 pi/2, mean height 5/6 (two routes)', Aarch == 3 * sp.pi and M == sp.Rational(5, 2) * sp.pi and close(Mn, 2.5 * math.pi, 1e-9) and M / Aarch == sp.Rational(5, 6))
# share of the area below y = 1: on the arch y < 1 for t in (0, pi/2) and (3pi/2, 2pi); width at height y by t(y)
below = (sp.integrate(yt * sp.diff(xt, t), (t, 0, sp.pi / 2)) * 2 + 1 * (xt.subs(t, 3 * sp.pi / 2) - xt.subs(t, sp.pi / 2))) / Aarch
chk('cycloid: more than half the area lies below half height (about 62%)', 0.61 < float(below) < 0.63 and sp.Rational(5, 6) < 1)
w = it['parts'][2]['widget']
wr = {q['id']: q['tex'] for q in w['wrong']}
chk('cycloid: part 3 key and four wrong entries', w['answer'] == '-\\frac{y^2}{2}' and wr == {'sign': '\\frac{y^2}{2}', 'no-half': '-y^2', 'x-term': '-\\frac{y^2}{2}+x', 'constant': '-\\frac{y^2}{2}+1'})
for nm, Pc, alone, zero in (('key', -y ** 2 / 2, True, True), ('x-term', -y ** 2 / 2 + x, False, False), ('constant', -y ** 2 / 2 + 1, True, False)):
    chk(f'cycloid: {nm} has -P_y = y; function of y alone {alone}; zero on the axis {zero}', -sp.diff(Pc, y) == y and (sp.diff(Pc, x) == 0) == alone and (Pc.subs(y, 0) == 0) == zero)
chk('cycloid: the stated conditions pin P down (-P_y = y, P(0) = 0, y alone)', sp.dsolve(sp.Function('P')(y).diff(y) + y, ics={sp.Function('P')(0): 0}).rhs == -y ** 2 / 2)
chk('cycloid: byKey lines for both new entries', all(k_ in it['parts'][2]['feedback']['byKey'] for k_ in ('x-term', 'constant')))
bands(it, 4, 2.5 * math.pi, [7.85], {'no-half': 5 * math.pi, 'sign': -2.5 * math.pi})
bands(it, 5, 5 / 6, [0.833], {'inverse': 1.2, 'no-half': 5 / 3})
has(it, 'mean height', '\\bar y = \\frac{1}{A}\\iint_D ydA', 'a function of $y$ alone with $P = 0$ on the axis $y = 0$', 'below half way')
gone(it, 'centroid', 'well below')
chk('cycloid: no undefined "moment" left from the centroid wording', 'moment' not in text(it))
bk = it['parts'][4]['feedback']['byKey']
chk('cycloid: part 5 inverse and no-half name the integral, not "the moment"',
    bk['inverse'] == 'You divided the area by $\\iint_D y\\,dA$. $\\bar y = \\iint_D y\\,dA \\div A$.'
    and bk['no-half'] == 'That uses $5\\pi$ for $\\iint_D y\\,dA$, without the $\\tfrac12$ from part 3.')

# ---- finding 10 wording in the quadrilateral problem
chk('quadrilateral: "normal form of Green\'s theorem" in the explain', "The normal form of Green's theorem" in text(V2['p-quadrilateral-plot']))

# ====================================================================== vector-calc/problems-3
V3 = load('vector-calc/problems-3.json')
it = V3['p-saddle-roof']
rr, th = sp.symbols('r theta', positive=True)
area = sp.integrate(sp.integrate(sp.sqrt(1 + rr ** 2) * rr, (rr, 0, sp.sqrt(3))), (th, 0, 2 * sp.pi))
flux = sp.integrate(sp.integrate((5 - rr ** 2) * rr, (rr, 0, sp.sqrt(3))), (th, 0, 2 * sp.pi))
fluxn = integrate.dblquad(lambda b_, a_: (5 - a_ * a_ - b_ * b_), -math.sqrt(3), math.sqrt(3), lambda a_: -math.sqrt(3 - a_ * a_), lambda a_: math.sqrt(3 - a_ * a_))[0]
chk('canopy: area 14 pi/3 and flux 21 pi/2 unchanged, keys agree', sp.simplify(area - sp.Rational(14, 3) * sp.pi) == 0 and flux == sp.Rational(21, 2) * sp.pi and close(fluxn, 10.5 * math.pi, 1e-6)
    and close(it['parts'][2]['widget']['answer'], 14 * math.pi / 3, 1e-4) and close(it['parts'][3]['widget']['answer'], 10.5 * math.pi, 1e-4))
has(it, 'A canopy', 'the wind', 'area of the canopy', 'up through the canopy', 'The canopy slopes')
gone(it, 'roof', 'air flow', 'tilted')
it = V3['p-open-tank']
X, Yv, Z = sp.symbols('X Y Z')
dv = sp.diff(X * Z, X) + sp.diff(Yv ** 2, Yv) + sp.diff(3 * Z, Z)
box = sp.integrate(dv, (X, 0, 4), (Yv, 0, 1), (Z, 0, 2))
faces = {'lid': sp.integrate(3 * 2, (X, 0, 4), (Yv, 0, 1)), 'floor': sp.integrate(-3 * 0, (X, 0, 4), (Yv, 0, 1)), 'x4': sp.integrate(4 * Z, (Yv, 0, 1), (Z, 0, 2)),
         'x0': 0, 'y1': sp.integrate(1, (X, 0, 4), (Z, 0, 2)), 'y0': 0}
chk('tank: box 40, lid 24, walls and floor 16 = 8 + 8 + 0 (faces against divergence)', box == 40 and faces['lid'] == 24 and faces['x4'] == 8 and faces['y1'] == 8 and faces['floor'] == 0 and sum(faces.values()) == 40
    and it['parts'][3]['widget']['answer'] == 16)
has(it, 'the four walls and the floor', 'floor included')
gone(it, 'five walls')
chk('tank: part 4 explain has at most three sentences', len(re.findall(r'[.](?:\s|$)', it['parts'][3]['explain']['text'])) <= 3)

findings = [f_ for f_ in fails if f_[1]]
plain = [f_ for f_ in fails if not f_[1]]
print(f'{n} checks, {len(plain)} failures, {len(findings)} FINDING rows')
sys.exit(1 if fails else 0)
