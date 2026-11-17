"""Recompute every number in app/content/courses/measure-prob/problems-4.json twice.

Method 1 is exact (fractions, sympy integrals, closed forms). Method 2 is independent: numerical quadrature,
enumeration of every coin path or trade sequence, or a seeded simulation. Each numeric part's key equals
both values at the asked rounding and lies in its band; every `wrong` value is rebuilt from its named slip,
lies outside the key's band and the other slips and has a byKey line. Expression keys, accept forms and
slips are compared with sympy at sample points; choice parts check the keyed option. Printed working
figures are checked against the exact values.
Run: <scratchpad>/venv/bin/python docs/reports/problems-measure-prob-4-numbers.py   (exit 0 when all pass)
Helpers are copied from problems-measure-prob-numbers.py (levels 1 to 3), which this script does not import.
"""
import json, os, re, sys, math, itertools, random
from fractions import Fraction as F
import sympy as sp
import numpy as np
from scipy import integrate

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'measure-prob')
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

fails, checks = [], 0


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)
        print('FAIL', msg)


def close(a, b, eps=1e-9):
    return abs(float(a) - float(b)) <= eps * max(1, abs(float(b)))


def load(n):
    p = os.path.join(COURSE, f'problems-{n}.json')
    return {it['id']: it for it in json.load(open(p))['items']} if os.path.exists(p) else None


FORM = re.compile(r'decimal|place|fraction|whole number|nearest|exact', re.I)


def structural(items, n):
    for iid, it in items.items():
        ok(3 <= len(it['parts']) <= 5, f'{iid}: 3 to 5 parts')
        for k, p in enumerate(it['parts']):
            w, fb = p['widget'], p['feedback']
            tag = f'L{n} {iid} part {k + 1}'
            if w['kind'] == 'numeric':
                key, tol = w['answer'], w['tol']['abs']
                ok(FORM.search(p['question']) is not None, f'{tag}: names its form')
                seen = []
                for wr in w.get('wrong', []):
                    v, t = wr['value'], wr['tol']['abs']
                    ok(abs(v - key) > tol + t, f'{tag}: wrong {wr["id"]} clear of the key band')
                    ok(wr['id'] in fb.get('byKey', {}), f'{tag}: wrong {wr["id"]} has a byKey line')
                    for (v2, t2, i2) in seen:
                        ok(abs(v - v2) > t + t2, f'{tag}: wrong {wr["id"]} and {i2} do not overlap')
                    seen.append((v, t, wr['id']))
            elif w['kind'] == 'expression':
                for wr in w.get('wrong', []):
                    ok(wr['id'] in fb.get('byKey', {}), f'{tag}: wrong {wr["id"]} has a byKey line')
            elif w['kind'] == 'choice':
                ok(sum(1 for o in w['options'] if o.get('correct')) == 1, f'{tag}: one correct option')
                ok(all(o.get('why') for o in w['options'] if not o.get('correct')), f'{tag}: every distractor has a why')


def key(items, iid, k):
    return items[iid]['parts'][k - 1]['widget']


def num_part(items, iid, k, v1, v2, places=None, eps=1e-9):
    """Both methods agree, the key is in its band, and the value at the asked rounding is taken."""
    w = key(items, iid, k)
    tag = f'{iid} part {k}'
    ok(abs(v1 - v2) <= eps * max(1, abs(v1)), f'{tag}: methods agree ({v1} vs {v2})')
    ok(abs(w['answer'] - v1) <= w['tol']['abs'] + 1e-12, f'{tag}: key {w["answer"]} within band of {v1}')
    if places is not None:
        r = round(v1, places)
        ok(abs(r - w['answer']) <= w['tol']['abs'] + 1e-12, f'{tag}: rounded {r} accepted')


def wrong_is(items, iid, k, wid, value, places=None):
    w = key(items, iid, k)
    e = [x for x in w['wrong'] if x['id'] == wid]
    ok(len(e) == 1, f'{iid} part {k}: wrong {wid} exists')
    if e:
        v = round(value, places) if places is not None else value
        ok(abs(e[0]['value'] - v) <= e[0]['tol']['abs'] + 1e-12, f'{iid} part {k}: wrong {wid} = {e[0]["value"]} is slip value {value}')


def choice_key(items, iid, k, oid):
    w = key(items, iid, k)
    ok([o['id'] for o in w['options'] if o.get('correct')] == [oid], f'{iid} part {k}: keyed option is {oid}')


SYM = {s: sp.Symbol(s) for s in ('n', 'h', 's', 'm', 'k', 'x')}


def tex(s):
    s = s.replace('\\left', '').replace('\\right', '').replace(' ', '').replace('\\tfrac', '\\frac').replace('\\dfrac', '\\frac')
    while '\\frac' in s:
        i = s.index('\\frac')

        def grab(j):
            depth, kk = 0, j
            while True:
                if s[kk] == '{':
                    depth += 1
                elif s[kk] == '}':
                    depth -= 1
                    if depth == 0:
                        return s[j + 1:kk], kk + 1
                kk += 1
        a, j = grab(i + 5)
        b, j = grab(j)
        s = s[:i] + f'(({a})/({b}))' + s[j:]
    s = s.replace('\\cdot', '*').replace('\\times', '*').replace('{', '(').replace('}', ')').replace('^', '**').replace('e**', 'E**')
    from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
    return parse_expr(s, local_dict=dict(SYM, E=sp.E), transformations=standard_transformations + (implicit_multiplication_application,))


def same(e1, e2, pts=(1, 2, 3, 5, 0.5, 2.5)):
    for v in pts:
        sub = {x: v for x in SYM.values()}
        a, b = complex(e1.subs(sub).evalf()), complex(e2.subs(sub).evalf())
        if abs(a - b) > 1e-9 * max(1, abs(b)):
            return False
    return True


def expr_part(items, iid, k, truth):
    w = key(items, iid, k)
    ok(same(tex(w['answer']), truth), f'{iid} part {k}: answer equals the truth')
    for a in w.get('accept', []):
        ok(same(tex(a), truth), f'{iid} part {k}: accept {a} equals the truth')
    for wr in w.get('wrong', []):
        ok(not same(tex(wr['tex']), truth), f'{iid} part {k}: wrong {wr["id"]} differs')




def text_has(items, iid, k, field, phrase):
    p = items[iid]['parts'][k - 1]
    t = p['feedback']['correct'] if field == 'correct' else p['explain']['text']
    ok(phrase in t, f'{iid} part {k}: {field} prints {phrase!r}')


# ---------------------------------------------------------------- level 4
def level4():
    it = load(4)
    structural(it, 4)
    x = sp.Symbol('x', positive=True)

    # p-recovery-reweight: P density 2x, Q density 4x^3 on [0, 1]
    I = 'p-recovery-reweight'
    fP, fQ = 2 * x, 4 * x ** 3
    Z = sp.simplify(fQ / fP)
    ok(sp.simplify(Z - 2 * x ** 2) == 0, 'recovery: Z = 2x^2 exactly')
    ok(sp.integrate(Z * fP, (x, 0, 1)) == 1, 'recovery: E_P[Z] = 1')
    expr_part(it, I, 1, 2 * SYM['x'] ** 2)
    zf = lambda t: 2 * t * t
    q8 = sp.integrate(Z * fP, (x, sp.Rational(4, 5), 1))
    q8n = integrate.quad(lambda t: zf(t) * 2 * t, 0.8, 1)[0]
    num_part(it, I, 2, float(q8), q8n, 4)
    ok(q8 == sp.Rational(5904, 10000), 'recovery: Q(X > 0.8) = 0.5904 exactly')
    wrong_is(it, I, 2, 'no-weight', float(sp.integrate(fP, (x, sp.Rational(4, 5), 1))))
    wrong_is(it, I, 2, 'frozen', float(2 * sp.Rational(16, 25) * sp.integrate(fP, (x, sp.Rational(4, 5), 1))))
    wrong_is(it, I, 2, 'complement', float(sp.integrate(fQ, (x, 0, sp.Rational(4, 5)))))
    ok(close(1 - 0.8 ** 2, 0.36) and close(1 - 0.8 ** 4, 0.5904), 'recovery: printed 0.36 and 0.5904')
    v = sp.integrate(Z ** 2 * fP, (x, 0, 1)) - 1
    rng = np.random.default_rng(4)
    xs = np.sqrt(rng.random(2_000_000))           # inverse of F_P(x) = x^2
    vs = np.var(2 * xs ** 2)
    ok(abs(vs - 1 / 3) < 0.003, f'recovery: simulated Var_P(Z) {vs:.4f} near 1/3')
    num_part(it, I, 3, float(v), integrate.quad(lambda t: zf(t) ** 2 * 2 * t, 0, 1)[0] - 1, 4)
    ok(v == sp.Rational(1, 3) and sp.integrate(8 * x ** 5, (x, 0, 1)) == sp.Rational(8, 6), 'recovery: Var = 1/3, E_P[Z^2] = 8/6')
    wrong_is(it, I, 3, 'second-moment', float(v + 1), 6)
    wrong_is(it, I, 3, 'under-q', float(sp.integrate(Z ** 2 * fQ, (x, 0, 1)) - 1))
    ok(sp.integrate(Z ** 2 * fQ, (x, 0, 1)) == 2, 'recovery: E_Q[Z^2] = 2 (printed in the under-q line)')
    eps = sp.Symbol('eps', positive=True)
    m2 = sp.integrate((1 / (2 * x ** 2)) ** 2 * fQ, (x, eps, 1))
    ok(sp.limit(m2, eps, 0) == sp.oo and sp.simplify(m2 + sp.log(eps)) == 0, 'recovery: E_Q[(dP/dQ)^2] = int dx/x diverges')
    ok(sp.integrate((1 / (2 * x ** 2)) * fQ, (x, 0, 1)) == 1, 'recovery: E_Q[dP/dQ] = 1 (the "one" distractor is the mean)')
    choice_key(it, I, 4, 'infinite')

    # p-share-numeraire: S0 48, u 1.25, d 0.85, cash 1.02, three steps
    I = 'p-share-numeraire'
    S0, u, d, R = F(48), F(5, 4), F(17, 20), F(51, 50)
    q = (R - d) / (u - d)
    ok(q == F(17, 40), 'numeraire: q = 0.425 from u, d and cash')
    paths = list(itertools.product('UD', repeat=3))
    S3 = {pth: S0 * u ** pth.count('U') * d ** pth.count('D') for pth in paths}
    Qp = {pth: q ** pth.count('U') * (1 - q) ** pth.count('D') for pth in paths}
    Z3 = {pth: S3[pth] / (S0 * R ** 3) for pth in paths}
    ok(sum(Qp[p_] * Z3[p_] for p_ in paths) == 1, 'numeraire: E_Q[Z_3] = 1 by enumeration')
    ok(all(z > 0 for z in Z3.values()) and max(Z3.values()) < 2, "numeraire: 0 < Z_3 < 2 on all eight paths")
    pud = ('U', 'D', 'D')
    ok(S3[pud] == F(4335, 100), 'numeraire: S_3 = 43.35 on U, D, D')
    num_part(it, I, 1, float(Z3[pud]), 43.35 / (48 * 1.02 ** 3), 4)
    ok(close(1.02 ** 3, 1.061208) and abs(48 * 1.061208 - 50.938) < 5e-4 and close(0.85 ** 2, 0.7225), 'numeraire: printed 1.061208, 50.938, 0.7225')
    wrong_is(it, I, 1, 'no-discount', float(S3[pud] / S0))
    wrong_is(it, I, 1, 'one-discount', float(S3[pud] / (S0 * R)), 6)
    choice_key(it, I, 2, 'mart')
    qs = q * u / R
    qs_down = (1 - q) * d / R
    ok(qs == F(25, 48) and qs_down == F(23, 48) and qs + qs_down == 1, 'numeraire: q^S = 25/48, down 23/48')
    QS = {pth: qs ** pth.count('U') * qs_down ** pth.count('D') for pth in paths}
    ok(all(QS[p_] == Qp[p_] * Z3[p_] for p_ in paths), 'numeraire: Q^S path chances equal Q chance times Z_3')
    num_part(it, I, 3, float(qs), 0.425 * 1.25 / 1.02, 4)
    wrong_is(it, I, 3, 'no-cash', float(q * u))
    wrong_is(it, I, 3, 'down-factor', float(q * d / R), 6)
    wrong_is(it, I, 3, 'down-chance', float(qs_down), 6)
    choice_key(it, I, 4, 'qs')
    A = [p_ for p_ in paths if S3[p_] > 50]
    ok(sorted({float(S3[p_]) for p_ in paths}) == [29.478, 43.35, 63.75, 93.75], 'numeraire: S_3 values 29.478, 43.35, 63.75, 93.75')
    ok(all(p_.count('U') >= 2 for p_ in A) and len(A) == 4, 'numeraire: S_3 > 50 exactly with two or three ups')
    qsA = sum(QS[p_] for p_ in A)
    ok(qsA == F(58750, 110592) and qsA == 3 * qs ** 2 * qs_down + qs ** 3, 'numeraire: Q^S(S_3 > 50) = 58750/110592')
    price1 = S0 * qsA
    price2 = sum(Qp[p_] * S3[p_] for p_ in A) / R ** 3
    ok(price1 == price2, 'numeraire: 48 Q^S(A) equals the Q price exactly')
    rng = np.random.default_rng(44)
    ups = (rng.random((1_000_000, 3)) < 0.425).sum(axis=1)
    sim = np.mean(np.where(ups >= 2, 48 * 1.25 ** ups * 0.85 ** (3 - ups), 0)) / 1.02 ** 3
    ok(abs(sim - float(price1)) < 0.05, f'numeraire: simulated Q price {sim:.3f} near {float(price1):.4f}')
    num_part(it, I, 5, float(price1), float(price2), 2)
    ok(abs(float(qsA) - 0.531232) < 5e-7 and abs(48 * 0.531232 - 25.50) < 0.005, 'numeraire: printed 0.531232 and 25.50')
    wrong_is(it, I, 5, 'q-chance', float(S0 * sum(Qp[p_] for p_ in A)), 6)
    wrong_is(it, I, 5, 'top-only', float(S0 * qs ** 3), 6)
    wrong_is(it, I, 5, 'discount', float(price1 / R ** 3), 6)

    # p-ten-trades: ten trades, win 0.5 under P, 0.8 under Q, A = at least 8 wins
    I = 'p-ten-trades'
    pw, qw = F(1, 2), F(4, 5)
    w = lambda k: (pw / qw) ** k * ((1 - pw) / (1 - qw)) ** (10 - k)
    PA = sum(math.comb(10, k) for k in (8, 9, 10)) * F(1, 1024)
    ok(PA == F(7, 128), 'trades: P(A) = 56/1024 = 7/128')
    seqs = list(itertools.product((0, 1), repeat=10))
    PA2 = sum(F(1, 1024) for s_ in seqs if sum(s_) >= 8)
    ok(PA2 == PA, 'trades: P(A) by enumerating 1024 sequences')
    num_part(it, I, 1, float(w(8)), 0.625 ** 8 * 2.5 ** 2, 4)
    ok(abs(0.625 ** 8 * 6.25 - 0.1455) < 5e-5, 'trades: printed 0.1455')
    wrong_is(it, I, 1, 'reversed', float(1 / w(8)), 6)
    wrong_is(it, I, 1, 'wins-only', float((pw / qw) ** 8), 6)
    m2 = sum(math.comb(10, k) * F(1, 1024) * w(k) for k in (8, 9, 10))
    m2b = 0.0
    for s_ in seqs:                                    # E_Q[Y^2] summed over Q-chances
        k = sum(s_)
        if k >= 8:
            m2b += 0.8 ** k * 0.2 ** (10 - k) * float(w(k)) ** 2
    num_part(it, I, 2, float(m2), m2b, 5)
    ok([round(float(w(k)), 5) for k in (8, 9, 10)] == [0.14552, 0.03638, 0.00909], 'trades: printed weights 0.14552, 0.03638, 0.00909')
    ok(round(float(m2), 5) == 0.00676, 'trades: E_Q[Y^2] rounds to 0.00676')
    ok(round((45 * 0.1455 + 10 * float(w(9)) + float(w(10))) / 1024, 5) == 0.00676, 'trades: the rounded weight 0.1455 also gives 0.00676')
    wrong_is(it, I, 2, 'no-weight', float(PA))
    wrong_is(it, I, 2, 'eight-only', float(45 * w(8) / 1024), 6)
    rng = np.random.default_rng(21)
    k_ = rng.binomial(10, 0.8, 2_000_000)
    wts = 0.625 ** k_ * 2.5 ** (10 - k_)
    Y = np.where(k_ >= 8, wts, 0)
    ok(abs(Y.mean() - 7 / 128) < 2e-4 and abs((Y ** 2).mean() - float(m2)) < 1e-4, 'trades: simulated mean and mean square of Y')
    m2r = F(676, 100000)
    var = m2r - PA ** 2
    rel = math.sqrt(float(var)) / float(PA)
    rel_exact = math.sqrt(float(m2 - PA ** 2)) / float(PA)
    num_part(it, I, 3, rel, float(sp.sqrt(sp.Rational(676, 100000) - sp.Rational(49, 16384)) / sp.Rational(7, 128)), 2)
    ok(round(rel_exact, 2) == 1.12, 'trades: unrounded E_Q[Y^2] also gives 1.12')
    ok(round(float(var), 6) == 0.003769 and round(float(PA) ** 2, 7) == 0.0029907 and round(0.00676 - 0.0029907, 7) == 0.0037693, 'trades: printed 0.003769, 0.0029907, 0.0037693')
    ok(abs(math.sqrt(0.003769) - 0.06139) < 5e-6 and round(0.06139 / 0.0546875, 2) == 1.12, 'trades: printed 0.06139 over 0.0546875')
    wrong_is(it, I, 3, 'no-mean', math.sqrt(float(m2r)) / float(PA), None)
    wrong_is(it, I, 3, 'no-root', float(var / PA ** 2), None)
    plain2 = (1 - PA) / PA
    ok(plain2 == F(121, 7), 'trades: plain square 121/7')
    ratio = float(plain2) / 1.12 ** 2
    ratio_exact = float(plain2) / rel_exact ** 2
    ok(round(ratio) == 14 and round(ratio_exact) == 14, f'trades: ratio {ratio:.2f} ({ratio_exact:.2f} unrounded) is 14 to the nearest whole')
    num_part(it, I, 4, 14, round(ratio), 0)
    ok(abs(17.29 / 1.2544 - 13.78) < 0.01 and round(float(plain2), 2) == 17.29, 'trades: printed 17.29 and 1.2544')
    wrong_is(it, I, 4, 'not-squared', round(math.sqrt(float(plain2)) / 1.12))
    wrong_is(it, I, 4, 'plain-only', round(float(plain2)))
    ok(round(math.sqrt(float(plain2)), 2) == 4.16, 'trades: printed 4.16')

    # p-premium-weight: 40 to 48 or 34, cash 1.01, p 0.6
    I = 'p-premium-weight'
    S0, Su, Sd, R, p = F(40), F(48), F(34), F(101, 100), F(3, 5)
    q = (S0 * R - Sd) / (Su - Sd)
    qq = sp.solve(sp.Eq(48 * sp.Symbol('q') + 34 * (1 - sp.Symbol('q')), sp.Rational(404, 10)))[0]
    ok(q == F(16, 35) and qq == sp.Rational(16, 35), 'premium: q = 16/35 two ways')
    num_part(it, I, 1, float(q), float(qq), 4)
    wrong_is(it, I, 1, 'no-cash', float((S0 - Sd) / (Su - Sd)), 6)
    wrong_is(it, I, 1, 'down', float(1 - q), 6)
    zu, zd = q / p, (1 - q) / (1 - p)
    ok(zu == F(16, 21) and zd == F(19, 14), 'premium: weights 16/21 and 19/14')
    num_part(it, I, 2, float(zd), float(sp.Rational(19, 35) / sp.Rational(2, 5)), 4)
    wrong_is(it, I, 2, 'up', float(zu), 6)
    wrong_is(it, I, 2, 'inverse', float(1 / zd), 6)
    wrong_is(it, I, 2, 'no-cash', float((1 - F(3, 7)) / (1 - p)), 6)
    EZS = p * zu * Su + (1 - p) * zd * Sd
    ES = p * Su + (1 - p) * Sd
    ok(EZS == F(404, 10) and ES == F(424, 10) and p * zu + (1 - p) * zd == 1, 'premium: E_P[ZS] 40.4, E_P[S] 42.4, E_P[Z] 1')
    cov1 = EZS - ES
    cov1b = float(np.cov([float(zu), float(zd)], [48, 34], aweights=[0.6, 0.4], bias=True)[0, 1])
    num_part(it, I, 3, float(cov1), cov1b, 2)
    wrong_is(it, I, 3, 'sign', float(-cov1))
    wrong_is(it, I, 3, 'no-mean', float(EZS))
    EZ2 = p * zu ** 2 + (1 - p) * zd ** 2
    ok(round(float(EZ2), 3) == 1.085, 'premium: E_Q[Z_1] = E_P[Z_1^2] = 1.085 (printed)')
    choice_key(it, I, 4, 'any')
    EZS2 = ES2 = EZ_2 = F(0)
    for pth in itertools.product('UD', repeat=2):        # enumerate the four two-step paths
        pr, z, s_ = F(1), F(1), S0
        for m in pth:
            pr *= p if m == 'U' else 1 - p
            z *= zu if m == 'U' else zd
            s_ *= Su / S0 if m == 'U' else Sd / S0
        EZS2 += pr * z * s_
        ES2 += pr * s_
        EZ_2 += pr * z
    ok(EZ_2 == 1 and EZS2 == S0 * R ** 2 and ES2 == S0 * (ES / S0) ** 2, 'premium: two-step means by enumeration')
    cov2 = EZS2 - ES2
    num_part(it, I, 5, float(cov2), 40 * 1.01 ** 2 - 40 * 1.06 ** 2, 2)
    ok(EZS2 == F(40804, 1000) and ES2 == F(44944, 1000) and ES / S0 == F(106, 100), 'premium: printed 40.804, 44.944, 1.06')
    wrong_is(it, I, 5, 'doubled', float(2 * cov1))
    wrong_is(it, I, 5, 'sign', float(-cov2))
    wrong_is(it, I, 5, 'cash-once', float(S0 * R - ES2))

    lv = Level('measure-prob', 4)
    lv.check_wrongs('problems')
    ok(all(r_[0] for r_ in lv.results), 'level 4: numbers_lib check_wrongs')


level4()
print(f'{checks} checks, {len(fails)} failures')
sys.exit(1 if fails else 0)
