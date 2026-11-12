"""Recompute every number in app/content/courses/estimation/problems-<n>.json twice.

Method 1 is exact (fractions.Fraction, sympy, closed forms). Method 2 takes a different
route: NumPy on the raw data, SciPy optimisers and fits (norm.fit, minimize_scalar,
brentq), numerical integration of an MSE over the estimator's density, a fixed-seed
simulation, an enumeration of all 27 bootstrap resamples, statsmodels' normal interval.
For each numeric part: both methods agree; the key matches them within its tol; each
`wrong` value matches its named slip and lies outside the key's band; no two wrong bands
overlap; a non-whole key's question states its form. Expression parts: the key and every
accept form equal the exact expression, and every wrong form differs. Choice parts: the
keyed option. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-estimation-numbers.py
"""
import json, os, re, sys, itertools
from fractions import Fraction as F
from math import isclose, sqrt, exp, log, ceil, floor
import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from scipy import stats, optimize, integrate
from statsmodels.stats.proportion import proportion_confint

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'estimation')
fails, checks = [], 0
FORM = re.compile(r'decimal|places?\b|fraction|whole number|nearest|per cent|%', re.I)


def derived_slips(slips, wrongs, e, text=''):
    """Slips the script derives itself for the `sign` / `sign2` and `decimal` wrong entries.

    sign: the absolute value of the computed key (the sign-dropped answer).
    decimal: the computed key over 100 (over 10,000 where the part is in %^2).
    Each is then compared with the content value inside its tolerance, and must lie
    outside the key band, by the ordinary slip checks below."""
    s = dict(slips or {})
    for wid in wrongs:
        if wid in s:
            continue
        if re.fullmatch(r'sign\d*', wid):
            s[wid] = abs(e)
        elif wid == 'decimal':
            s[wid] = e / (10000 if '%²' in text else 100)
    return s


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def load(n):
    p = os.path.join(COURSE, f'problems-{n}.json')
    if not os.path.exists(p):
        return None
    d = json.load(open(p))
    ok(d['id'] == f'problems-{n}' and d['level'] == n and d['course'] == 'estimation', f'set {n}: header')
    ok(3 <= len(d['items']) <= 5, f'set {n}: item count')
    ok(any(it['difficulty'] == 5 for it in d['items']), f'set {n}: no difficulty 5')
    return {it['id']: it for it in d['items']}


def part(items, iid, k):
    return items[iid]['parts'][k - 1]


def num(items, iid, k, exact, alt, slips=None, rel=1e-9, pct=False):
    """exact: method 1; alt: method 2; slips: {wrong id: value the slip gives}.
    pct: the part has unit "%", so the key, its band and every wrong value are the fraction (value / 100)."""
    if items is None:
        return
    p = part(items, iid, k)
    w, tag = p['widget'], f'{iid} p{k}'
    ok(w['kind'] == 'numeric', f'{tag}: not numeric')
    ok((w.get('unit') == '%') == bool(pct), f'{tag}: unit {w.get("unit")!r} against pct={pct}')
    sc = 0.01 if pct else 1
    e = float(exact)
    ok(isclose(e, float(alt), rel_tol=rel, abs_tol=1e-9), f'{tag}: methods differ {e} vs {float(alt)}')
    e *= sc
    tol = w['tol']['abs']
    ok(abs(w['answer'] - e) <= tol + 1e-12, f'{tag}: key {w["answer"]} vs computed {e} (tol {tol})')
    if float(w['answer']) != int(w['answer']) or tol > 0:
        ok(bool(FORM.search(p['question'])), f'{tag}: question states no form')
    else:
        ok(bool(re.search(r'whole number', p['question'])), f'{tag}: integer key, question does not say whole number')
    if re.search(r'whole number', p['question']):
        ok(w.get('placeholder') != 'decimal', f'{tag}: whole-number part with the placeholder "decimal"')
    slips = slips or {}
    wrongs = {x['id']: x for x in w.get('wrong', [])}
    slips = derived_slips(slips, wrongs, e / sc, json.dumps(p, ensure_ascii=False))
    ok(set(wrongs) == set(slips), f'{tag}: wrong ids {sorted(wrongs)} vs slips {sorted(slips)}')
    ok(set(wrongs) <= set(p['feedback'].get('byKey', {})), f'{tag}: byKey lines missing')
    ok(set(p['feedback'].get('byKey', {})) <= set(wrongs), f'{tag}: byKey line with no wrong entry')
    for wid, val in slips.items():
        if wid not in wrongs:
            continue
        x = wrongs[wid]
        wt = x['tol']['abs']
        val = float(val) * sc
        ok(abs(x['value'] - val) <= max(wt, 1e-9) + 1e-12, f'{tag}: wrong {wid} {x["value"]} vs slip {val}')
        ok(abs(x['value'] - w['answer']) > tol + wt, f'{tag}: wrong {wid} {x["value"]} inside the key band')
        ok(abs(val - e) > tol, f'{tag}: slip {wid} equals the answer')
    for a, b in itertools.combinations(list(wrongs), 2):
        A, B = wrongs[a], wrongs[b]
        ok(abs(A['value'] - B['value']) > A['tol']['abs'] + B['tol']['abs'], f'{tag}: wrongs {a} and {b} overlap')


def band_takes(items, iid, k, wid, values, msg, pct=False):
    """a wrong entry (or the key, wid=None) whose band takes every value a learner reaches by a rounded route"""
    if items is None:
        return
    w = part(items, iid, k)['widget']
    sc = 0.01 if pct else 1
    if wid is None:
        v0, t0 = w['answer'], w['tol']['abs']
    else:
        x = next(y for y in w['wrong'] if y['id'] == wid)
        v0, t0 = x['value'], x['tol']['abs']
    for v in values:
        ok(abs(float(v) * sc - v0) <= t0 + 1e-12, f'{iid} p{k} {wid or "key"}: {msg} ({float(v)}) outside {v0} +- {t0}')


def has_text(items, iid, k, needle, msg):
    ok(needle in json.dumps(part(items, iid, k), ensure_ascii=False), f'{iid} p{k}: {msg}')


def lacks_text(items, iid, k, needle, msg):
    ok(needle not in json.dumps(part(items, iid, k), ensure_ascii=False), f'{iid} p{k}: stale value ({msg})')


TR = standard_transformations + (implicit_multiplication_application,)


def tex(s):
    s = re.sub(r'\\ln\s*\\lambda', 'log(lam)', s)
    s = s.replace('\\lambda', 'lam').replace('\\ln', 'log')
    while '\\frac' in s:
        s = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', s)
    s = s.replace('{', '(').replace('}', ')').replace('^', '**')
    return parse_expr(s, transformations=TR, local_dict={'e': sp.E, 'lam': sp.Symbol('lam', positive=True), 'w': sp.Symbol('w'), 'p': sp.Symbol('p')})


def expr(items, iid, k, exact, wrong_exact):
    if items is None:
        return
    w, tag = part(items, iid, k)['widget'], f'{iid} p{k}'
    ok(w['kind'] == 'expression', f'{tag}: not expression')
    for form in [w['answer']] + w.get('accept', []):
        ok(sp.simplify(tex(form) - exact) == 0, f'{tag}: form {form} differs from the key')
    got = {x['id']: x['tex'] for x in w.get('wrong', [])}
    ok(set(got) == set(wrong_exact), f'{tag}: wrong ids')
    for wid, ex in wrong_exact.items():
        ok(sp.simplify(tex(got[wid]) - ex) == 0, f'{tag}: wrong {wid} tex differs from its slip')
        ok(sp.simplify(tex(got[wid]) - exact) != 0, f'{tag}: wrong {wid} equals the key')


def pick(items, iid, k, cid):
    if items is None:
        return
    keyed = [o['id'] for o in part(items, iid, k)['widget']['options'] if o.get('correct')]
    ok(keyed == [cid], f'{iid} p{k}: keyed {keyed}, expected {cid}')


def stated(text_value, exact, msg, tol=1e-9):
    ok(abs(float(text_value) - float(exact)) <= tol, f'stated {msg}: {text_value} vs {float(exact)}')


def mse_by_integration(c, mean, var, target):
    """E[(c X - target)^2] for X ~ N(mean, var), by quadrature."""
    f = lambda x: (c * x - target) ** 2 * stats.norm.pdf(x, mean, sqrt(var))
    return integrate.quad(f, mean - 40 * sqrt(var), mean + 40 * sqrt(var))[0]


def qform(n, var):
    """Var of an equal-weight mean as w' S w, with S = var * I."""
    wv = np.full(n, 1 / n)
    return float(wv @ (var * np.eye(n)) @ wv)


# ======================================================== level 1: estimators
I = load(1)
if I:
    # p-ping-latency
    x = [304, 318, 296, 322, 310]
    xb = F(sum(x), 5)
    ss = sum((F(v) - xb) ** 2 for v in x)
    s2 = ss / 4
    num(I, 'p-ping-latency', 1, xb, np.mean(x), {'by-four': F(1550, 4), 'range': max(x) - min(x)})
    num(I, 'p-ping-latency', 2, s2, np.var(x, ddof=1), {'by-n': ss / 5, 'no-divide': ss, 'abs': F(sum(abs(v - 310) for v in x), 4)})
    se = sqrt(s2 / 5)
    num(I, 'p-ping-latency', 3, se, np.std(x, ddof=1) / np.sqrt(5),
        {'carried': sqrt(ss / 5 / 5), 'root-of-n': sqrt(s2) / 5, 'sd': sqrt(s2), 'variance': s2 / 5}, rel=1e-12)
    # part 4 asks for a standard error of at most 2 microseconds (finding 8): exact ceiling, then a search over n
    n_exact = ceil(s2 / 4)
    n_search = next(n for n in range(1, 1000) if sqrt(110 / n) <= 2)
    n_root = optimize.brentq(lambda n: sqrt(110 / n) - 2, 1, 1000)
    ok(abs(n_root - 27.5) < 1e-9 and n_exact == n_search == 28, 'ping p4: root 27.5, 28 pings')
    ok(sqrt(110 / 28) <= 2 < sqrt(110 / 27), 'ping p4: 28 pings are enough, 27 are not')
    stated(2.02, sqrt(110 / 27), 'ping p4 round-down line: 27 pings give 2.02', 0.005)
    stated(5.2, sqrt(110) / 2, 'ping p4 unsquared line: n = s / 2', 0.05)
    num(I, 'p-ping-latency', 4, n_exact, n_search,
        {'carried': ceil(ss / 5 / 4), 'no-square': s2 / 2, 'unsquared': sqrt(s2) / 2, 'round-down': 27})
    lacks_text(I, 'p-ping-latency', 4, '1 microsecond', 'old target of 1 microsecond')
    ok(part(I, 'p-ping-latency', 4)['widget']['answer'] != s2, 'ping p4: the answer is no longer the s^2 printed in part 2')
    ok(isclose(5 * 4.69 ** 2, 110, rel_tol=0.001), 'ping p4 explain check 5 x 4.69^2')

    # p-route-delays
    v = F(36, 16)
    num(I, 'p-route-delays', 1, v, qform(16, 36), {'se': sqrt(v), 'sd-over-n': F(6, 16), 'root-n': F(36, 4)})
    bias = F(1, 2) * 3 - 3
    num(I, 'p-route-delays', 2, bias, integrate.quad(lambda t: (0.5 * t - 3) * stats.norm.pdf(t, 3, 1.5), -60, 66)[0],
        {'mean-not-bias': F(3, 2), 'unbiased': 3}, rel=1e-7)
    mse_half = F(1, 4) * v + bias ** 2
    num(I, 'p-route-delays', 3, mse_half, mse_by_integration(0.5, 3, 2.25, 3),
        {'unquartered': v + bias ** 2, 'bias-unsquared': F(1, 4) * v + abs(bias), 'carried': F(1, 4) * F(3, 2) + bias ** 2, 'variance-only': F(1, 4) * v}, rel=1e-7)
    cut = sqrt(3 * v)
    cut2 = optimize.brentq(lambda m: mse_by_integration(0.5, m, 2.25, m) - 2.25, 0.1, 6)
    num(I, 'p-route-delays', 4, cut, cut2,
        {'no-root': 3 * v, 'bias-unquartered': sqrt(F(3, 4) * v), 'carried': sqrt(3 * F(3, 2))}, rel=1e-7)

    # p-sulphur-labs
    va, vb, bb = F(36, 9), F(9, 36), F(1, 2)
    mb = vb + bb ** 2
    num(I, 'p-sulphur-labs', 1, va, qform(9, 36), {'se': 2, 'root-n': 12})
    num(I, 'p-sulphur-labs', 2, mb, mse_by_integration(1, 10.5, 0.25, 10), {'variance-only': vb, 'bias-unsquared': vb + bb}, rel=1e-7)
    W = sp.Symbol('w')
    mse_w = mb * W ** 2 + va * (1 - W) ** 2
    expr(I, 'p-sulphur-labs', 3, sp.Rational(1, 2) * W ** 2 + 4 * (1 - W) ** 2,
         {'unsquared-weights': sp.Rational(1, 2) * W + 4 * (1 - W), 'no-bias': sp.Rational(1, 4) * W ** 2 + 4 * (1 - W) ** 2,
          'swapped': 4 * W ** 2 + sp.Rational(1, 2) * (1 - W) ** 2})
    # simulation check of the blend formula at w = 0.3 (fixed seed)
    rng = np.random.default_rng(16)
    A = rng.normal(0, 6, (200000, 9)).mean(1)
    B = rng.normal(0.5, 3, (200000, 36)).mean(1)
    ok(abs(np.mean((0.3 * B + 0.7 * A) ** 2) - float(mse_w.subs(W, 0.3))) < 0.03, 'sulphur blend MSE by simulation')
    wstar = sp.solve(sp.diff(mse_w, W), W)[0]
    wnum = optimize.minimize_scalar(lambda t: float(mb) * t * t + float(va) * (1 - t) ** 2, bounds=(0, 1), method='bounded', options={'xatol': 1e-12}).x
    best = lambda m: F(int(va), 1) / (va + m)          # weight on B for MSE(B) = m
    num(I, 'p-sulphur-labs', 4, wstar, wnum,
        {'swapped': 1 - best(mb), 'no-bias': best(vb), 'carried': best(vb + bb), 'half': F(1, 2)}, rel=1e-6)
    msestar = mse_w.subs(W, wstar)
    hm = lambda m: m * va / (m + va)
    num(I, 'p-sulphur-labs', 5, msestar, float(mb) * wnum ** 2 + float(va) * (1 - wnum) ** 2,
        {'half-half': mse_w.subs(W, sp.Rational(1, 2)), 'no-bias': hm(vb), 'carried': hm(vb + bb),
         'swapped': mse_w.subs(W, 1 - wstar), 'b-alone': mb}, rel=1e-9)

    # p-reference-mass
    r = [12, -6, 6, -10, 8]
    rb = F(sum(r), 5)
    ssr = sum((F(t) - rb) ** 2 for t in r)
    sq = sum(F(t) ** 2 for t in r)
    # part 1 asks for the sampling error xbar - mu with mu = 0 (finding 10)
    num(I, 'p-reference-mass', 1, rb - 0, np.mean(r) - 0, {'by-four': F(10, 4), 'sizes': F(sum(abs(t) for t in r), 5)})
    ok('sampling error' in part(I, 'p-reference-mass', 1)['question'] and 'mu = 0' in part(I, 'p-reference-mass', 1)['question'], 'reference p1 asks for the sampling error')
    num(I, 'p-reference-mass', 2, ssr, np.var(r) * 5, {'from-zero': sq, 's-squared': ssr / 4, 'by-n': ssr / 5})
    ok(sq == ssr + 5 * rb ** 2, 'reference identity sum x^2 = SS + n xbar^2')
    num(I, 'p-reference-mass', 3, (ssr + 5 * rb ** 2) / 5, np.mean(np.square(r)),
        {'ss-by-n': ssr / 5, 's-squared': ssr / 4, 'by-four': sq / 4, 'subtracted': (ssr - 5 * rb ** 2) / 5})
    pick(I, 'p-reference-mass', 4, 'known')
    # part 5 asks how many standard errors of a five-reading mean the 2 mg is (finding 8): exact, then from the raw readings
    se5 = sqrt(F(76, 5))
    z5 = 2 / se5
    z5_data = (np.mean(r) - 0) / np.sqrt(np.mean(np.square(r)) / len(r))
    stated(3.90, se5, 'reference p5 SE of a five-reading mean', 0.005)
    stated(0.513, z5, 'reference p5 key', 0.0005)
    num(I, 'p-reference-mass', 5, z5, z5_data,
        {'carried-90': 2 / sqrt(F(90, 5)), 'carried-72': 2 / sqrt(F(72, 5)), 'no-root': 2 / F(76, 5), 'sd-not-se': 2 / sqrt(76), 'inverted': se5 / 2})
    # the stale items are gone: the old key 19 and the old unsquared slip
    lacks_text(I, 'p-reference-mass', 5, 'readings must the lab average', 'the old sample-size question')
    ok(part(I, 'p-reference-mass', 5)['widget']['answer'] != 19 and 'unsquared' not in {x['id'] for x in part(I, 'p-reference-mass', 5)['widget']['wrong']}, 'reference p5: old key 19 and unsquared slip gone')
    ok(part(I, 'p-reference-mass', 5)['widget']['tol']['abs'] >= abs(2 / sqrt(15.2) - 0.513), 'reference p5: key band takes the exact value')
    # the unsbiasedness claim of part 4, by simulation: mean of sum x^2 / 5 against sigma^2 = 9
    sim = rng.normal(0, 3, (200000, 5))
    ok(abs(np.mean(np.sum(sim ** 2, 1) / 5) - 9) < 0.05, 'reference: known-mean estimator unbiased by simulation')

# ======================================================== level 2: likelihood
I = load(2)
if I:
    P = sp.Symbol('p')
    expr(I, 'p-robot-deliveries', 1, P ** 9 * (1 - P) ** 3,
         {'swapped': P ** 3 * (1 - P) ** 9, 'added': 9 * P + 3 * (1 - P), 'one-failure': P ** 9 * (1 - P), 'any-order': sp.binomial(12, 9) * P ** 9 * (1 - P) ** 3})
    ph = sp.solve(sp.diff(9 * sp.log(P) + 3 * sp.log(1 - P), P), P)[0]
    phn = optimize.minimize_scalar(lambda q: -stats.binom.logpmf(9, 12, q), bounds=(0.01, 0.99), method='bounded', options={'xatol': 1e-10}).x
    num(I, 'p-robot-deliveries', 2, ph, phn, {'failure-share': F(1, 4), 'odds': 3}, rel=1e-6)
    pr = optimize.minimize_scalar(lambda q: -(9 * log(q) + 3 * log(1 - q)), bounds=(0.9, 1 - 1e-12), method='bounded', options={'xatol': 1e-10}).x
    num(I, 'p-robot-deliveries', 3, F(9, 10), pr, {'unrestricted': F(3, 4), 'top': 1, 'middle': F(19, 20)}, rel=1e-6)
    # finding 1: only the edge value and its roundings pass; the middle of the range (0.95) and 0.85 are refused
    kb = part(I, 'p-robot-deliveries', 3)['widget']
    ok(kb['tol']['abs'] <= 0.005, 'robot p3: key band is at most 0.005')
    for v in (0.95, 0.85, 0.75, 1.0):
        ok(abs(v - kb['answer']) > kb['tol']['abs'], f'robot p3: {v} is refused as the answer')
    for v in (0.9, 0.90, round(pr, 2), round(pr, 4)):
        ok(abs(v - kb['answer']) <= kb['tol']['abs'], f'robot p3: {v} is accepted')
    # the middle of [0.9, 1] is a worse likelihood than the edge, and the slip is a real one: L falls across the range
    Lq = lambda q: F(q) ** 9 * (1 - F(q)) ** 3
    ok(Lq(F(9, 10)) > Lq(F(19, 20)) > Lq(1) == 0, 'robot p3: L falls from 0.9 to 1')
    ok('2 decimal places' in part(I, 'p-robot-deliveries', 3)['question'], 'robot p3: asks for 2 decimal places')
    L = lambda q: F(q) ** 9 * (1 - F(q)) ** 3
    ratio = L(F(3, 4)) / L(F(9, 10))
    num(I, 'p-robot-deliveries', 4, ratio, exp(stats.binom.logpmf(9, 12, 0.75) - stats.binom.logpmf(9, 12, 0.9)),
        {'inverted': 1 / ratio, 'no-failures': (F(3, 4) / F(9, 10)) ** 9, 'same': 1}, rel=1e-9)
    stated(0.1938, (F(3, 4) / F(9, 10)) ** 9, 'robot (0.75/0.9)^9', 5e-5)
    stated(5.2, (F(9, 10) / F(3, 4)) ** 9, 'robot (0.9/0.75)^9', 0.05)
    stated(15.6, F(5, 2) ** 3, 'robot 2.5^3', 0.05)

    x = [52, 47, 55, 50]
    mh = F(sum(x), 4)
    # finding 4: 52.5 is the mean of the LAST two readings (55, 50); the middle two (50, 52 sorted) average the key
    ok(F(sum(x[2:]), 2) == F(105, 2) and F(sum(sorted(x)[1:3]), 2) == mh, 'tank: 52.5 is the last-two mean; the middle two average to 51')
    num(I, 'p-tank-sensor', 1, mh, stats.norm.fit(x, fscale=4)[0], {'by-three': F(204, 3), 'last-two': F(sum(x[2:]), 2)}, rel=1e-6)
    s51 = sum((t - 51) ** 2 for t in x); s48 = sum((t - 48) ** 2 for t in x)
    stated(34, s51, 'tank sum about 51'); stated(70, s48, 'tank sum about 48')
    d = F(s48 - s51, 32)
    dn = stats.norm.logpdf(x, 51, 4).sum() - stats.norm.logpdf(x, 48, 4).sum()
    num(I, 'p-tank-sensor', 2, d, dn, {'no-two': F(s48 - s51, 16), 'sd-not-squared': F(s48 - s51, 8), 'reversed': -d})
    num(I, 'p-tank-sensor', 3, exp(d), np.prod(stats.norm.pdf(x, 51, 4)) / np.prod(stats.norm.pdf(x, 48, 4)),
        {'carried': exp(2 * d), 'no-exp': d, 'inverted': exp(-d)})
    top = 51 + sqrt(8 * log(10))
    topn = optimize.brentq(lambda m: stats.norm.logpdf(x, 51, 4).sum() - stats.norm.logpdf(x, m, 4).sum() - log(10), 51.001, 70)
    num(I, 'p-tank-sensor', 4, top, topn,
        {'log-ten': 51 + sqrt(8), 'no-root': 51 + 8 * log(10), 'sd-not-squared': 51 + sqrt(2 * log(10)), 'no-n': 51 + sqrt(32 * log(10))}, rel=1e-9)
    ok(all(sum((t - m) ** 2 for t in x) == 34 + 4 * (m - 51) ** 2 for m in range(40, 60)), 'tank identity')
    # finding 11: part 4 opens with part 3's result
    stated(3.08, exp(d), 'tank p3 ratio quoted at the start of part 4', 0.005)
    ok(part(I, 'p-tank-sensor', 4)['question'].startswith('Part 3 found the readings 3.08 times as likely at 51 as at 48.'), 'tank p4 opens with part 3 result')

    r = [F(t) for t in ['1.4', '-0.6', '0.7', '-1.3', '1.1', '-0.1', '1.8', '-1.0']]
    rf = np.array([float(t) for t in r])
    stated(9.96, sum(t * t for t in r), 'fx squares add to 9.96')
    mu = sum(r) / 8
    mu_fit, sd_fit = stats.norm.fit(rf)
    num(I, 'p-currency-vol', 1, mu, mu_fit, {'by-seven': sum(r) / 7, 'sizes': sum(abs(t) for t in r) / 8}, rel=1e-9, pct=True)
    ss = sum((t - mu) ** 2 for t in r)
    stated(9.46, ss, 'fx SS'); stated(1.1825, ss / 8, 'fx sigma^2')
    sig = sqrt(ss / 8)
    num(I, 'p-currency-vol', 2, sig, sd_fit,
        {'n-minus-one': sqrt(ss / 7), 'zero-mean': sqrt(sum(t * t for t in r) / 8), 'variance': ss / 8}, rel=1e-9, pct=True)
    stated(1.0874, sig, 'fx sigma 4dp', 5e-5)
    ann = 1.0874 * sqrt(52)
    num(I, 'p-currency-vol', 3, ann, np.sqrt(52 * 1.0874 ** 2),
        {'times-52': 1.0874 * 52, 'trading-days': 1.0874 * sqrt(252), 'carried': sqrt(ss / 7) * sqrt(52), 'variance': 52 * float(ss / 8)}, rel=1e-12, pct=True)
    # finding 5: the slip bands take the value from the exact sigma-hat and from the 1.09 / 1.16 part 2 hands over at 2 places
    s_ex, s_r = float(sig), 1.09
    nm1, nm1_r = float(sqrt(ss / 7)), 1.16
    band_takes(I, 'p-currency-vol', 3, 'times-52', [s_ex * 52, s_r * 52, 1.0874 * 52], 'times 52 from exact, 1.09, 1.0874', pct=True)
    band_takes(I, 'p-currency-vol', 3, 'trading-days', [s_ex * sqrt(252), s_r * sqrt(252), 1.0874 * sqrt(252)], 'times sqrt 252', pct=True)
    band_takes(I, 'p-currency-vol', 3, 'carried', [nm1 * sqrt(52), nm1_r * sqrt(52), 1.1625 * sqrt(52)], 'n - 1 slip', pct=True)
    band_takes(I, 'p-currency-vol', 3, 'variance', [52 * float(ss / 8), 52 * s_r ** 2, 52 * 1.1825], 'annual variance', pct=True)
    band_takes(I, 'p-currency-vol', 3, None, [s_ex * sqrt(52), s_r * sqrt(52), 1.0874 * sqrt(52), 7.84], 'annual vol, exact and rounded routes', pct=True)
    ok(abs(sig * sqrt(52) - 7.84) < 0.005 and abs(1.09 * sqrt(52) - ann) < 0.02, 'fx annual: exact and 1.09 both inside band')
    num(I, 'p-currency-vol', 4, F(784, 100) / 4, 7.84 / np.sqrt(2 * 8), {'no-two': 7.84 / sqrt(8), 'weeks-in-year': 7.84 / sqrt(104), 'no-root': F(784, 1600)}, pct=True)
    nw = next(n for n in range(1, 1000) if 7.84 / sqrt(2 * n) <= 0.5)
    num(I, 'p-currency-vol', 5, ceil((7.84 / 0.5) ** 2 / 2), nw, {'no-two': round((7.84 / 0.5) ** 2), 'unsquared': 7.84, 'no-two-unsquared': 15.68, 'round-down': floor((7.84 / 0.5) ** 2 / 2)})
    # finding 6: 122 weeks leave the standard error above 0.5, 123 do not
    ok(7.84 / sqrt(2 * 122) > 0.5 >= 7.84 / sqrt(2 * 123), 'fx p5: 122 weeks are not enough, 123 are')
    stated(0.5019, 7.84 / sqrt(2 * 122), 'fx p5 122 weeks leave 0.502 (just above 0.5)', 5e-5)
    ok(ceil((sig * sqrt(52) / 0.5) ** 2 / 2) == 123 and ceil(8 * (1.96 / 0.5) ** 2) == 123, 'fx weeks robust to rounding')

    waits = [2, 7, 4, 1, 6]
    lam = sp.Symbol('lam', positive=True)
    expr(I, 'p-ride-waits', 1, 5 * sp.log(lam) - 20 * lam,
         {'likelihood': lam ** 5 * sp.exp(-20 * lam), 'sign': 5 * sp.log(lam) + 20 * lam, 'one-log': sp.log(lam) - 20 * lam})
    l1 = sp.solve(sp.diff(5 * sp.log(lam) - 20 * lam, lam), lam)[0]
    l1n = 1 / stats.expon.fit(waits, floc=0)[1]
    num(I, 'p-ride-waits', 2, l1, l1n, {'mean-wait': 4, 'one-log': F(1, 20)}, rel=1e-9)
    l2 = sp.solve(sp.diff(5 * sp.log(lam) - 28 * lam, lam), lam)[0]
    cen = lambda t: -(stats.expon.logpdf(waits, scale=1 / t).sum() + stats.expon.logsf(8, scale=1 / t))
    l2n = optimize.minimize_scalar(cen, bounds=(0.01, 2), method='bounded', options={'xatol': 1e-12}).x
    num(I, 'p-ride-waits', 3, l2, l2n, {'as-complete': F(6, 28), 'dropped': F(1, 4), 'no-time': F(6, 20)}, rel=1e-6)
    num(I, 'p-ride-waits', 4, sp.exp(-10 * l2), stats.expon.sf(10, scale=1 / l2n),
        {'old-rate': exp(-2.5), 'as-complete': exp(-60 / 28), 'complement': 1 - exp(-50 / 28)}, rel=1e-6)

# ======================================================== level 3: uncertainty
I = load(3)
if I:
    ph = F(96, 600)
    num(I, 'p-email-clicks', 1, ph, np.mean([1] * 96 + [0] * 504), {'non-clicks': 1 - ph, 'count': 96})
    se = sqrt(ph * (1 - ph) / 600)
    num(I, 'p-email-clicks', 2, se, np.std([1] * 96 + [0] * 504) / np.sqrt(600),
        {'no-root': ph * (1 - ph) / 600, 'no-n': sqrt(ph * (1 - ph)), 'root-n-only': float(ph * (1 - ph)) / sqrt(600)}, rel=1e-9)
    lo, hi = proportion_confint(96, 600, alpha=0.05, method='normal')
    z = stats.norm.ppf(0.975)
    num(I, 'p-email-clicks', 3, 0.16 - 1.96 * se, lo,
        {'ninety': 0.16 - 1.645 * se, 'one-se': 0.16 - se, 'upper': 0.16 + 1.96 * se}, rel=1e-4)
    ok(abs((0.16 - 1.96 * 0.0150) - 0.1307) <= 0.0006, 'clicks: rounded SE route inside band')
    pick(I, 'p-email-clicks', 4, 'excluded')
    ok(lo > 0.12, 'clicks: 12% below the interval')

    data = [2, 4, 9]
    m = F(sum(data), 3)
    ss = sum((F(t) - m) ** 2 for t in data)
    stated(5, m, 'fund mean'); stated(26, ss, 'fund squared deviations')
    num(I, 'p-three-month-fund', 1, sqrt(ss / 2 / 3), np.std(data, ddof=1) / np.sqrt(3),
        {'sd': sqrt(ss / 2), 'by-n': sqrt(ss / 3 / 3), 'no-root': ss / 2 / 3}, rel=1e-12, pct=True)
    means = [F(sum(c), 3) for c in itertools.product(data, repeat=3)]       # all 27 resamples
    draws = [F(t) for t in data]
    vdraw = sum((t - m) ** 2 for t in draws) / 3
    num(I, 'p-three-month-fund', 2, ss / 3, vdraw, {'s-squared': ss / 2, 'no-divide': ss, 'sd': sqrt(ss / 3)})
    boot_var = sum((b - m) ** 2 for b in means) / 27
    num(I, 'p-three-month-fund', 3, sqrt(ss / 9), sqrt(boot_var), {'carried': sqrt(ss / 2 / 3), 'no-root': ss / 9, 'one-draw': sqrt(ss / 3)}, rel=1e-12, pct=True)
    num(I, 'p-three-month-fund', 4, sqrt(F(2, 3)), sqrt(boot_var) / (np.std(data, ddof=1) / np.sqrt(3)),
        {'inverted': sqrt(F(3, 2)), 'squared': F(2, 3), 'same': 1}, rel=1e-12)
    ok(abs(1.70 / 2.08 - 0.8165) <= 0.001, 'fund: rounded ratio inside band')
    # finding 3: the explanation prints 0.817 from the rounded SEs and 0.816 from the unrounded ones
    stated(0.817, round(1.70 / 2.08, 3), 'fund 1.70 / 2.08 at 3 places', 5e-4)
    stated(0.816, sqrt(F(2, 3)), 'fund sqrt(2/3) at 3 places', 5e-4)
    ok(round(float(sqrt(F(2, 3))), 3) == 0.816 and round(1.70 / 2.08, 3) == 0.817, 'fund: 0.817 and 0.816 are the two roundings')
    # finding 5: the slip bands take the value from the rounded 2.08 and 1.70 the question hands over
    band_takes(I, 'p-three-month-fund', 4, 'inverted', [float(sqrt(F(3, 2))), 2.08 / 1.70, round(2.08 / 1.70, 3)], 'inverted ratio, exact and from 2.08 / 1.70')
    band_takes(I, 'p-three-month-fund', 4, 'squared', [2 / 3, (1.70 / 2.08) ** 2, round((1.70 / 2.08) ** 2, 3)], 'squared ratio, exact and from 1.70 / 2.08')
    band_takes(I, 'p-three-month-fund', 4, None, [float(sqrt(F(2, 3))), 1.70 / 2.08, 0.817, 0.816], 'ratio, exact and rounded')

    a, b, k, n = 8, 12, 21, 30
    pm = F(a + k, a + b + n)
    num(I, 'p-ticket-bot', 1, pm, stats.beta.mean(a + k, b + n - k), {'mle': F(k, n), 'prior': F(a, a + b), 'swapped': F(a + n - k, a + b + n)}, rel=1e-12)
    wgt = (pm - F(a, a + b)) / (F(k, n) - F(a, a + b))
    num(I, 'p-ticket-bot', 2, wgt, n / (n + a + b), {'prior-weight': 1 - wgt, 'ratio': F(n, a + b)}, rel=1e-12)
    nn = next(t for t in range(1, 5000) if F(20, t + 20) * F(3, 10) <= F(1, 100))
    nbeta = next(t for t in range(10, 5000, 10)
                 if abs(stats.beta.mean(a + 0.7 * t, b + 0.3 * t) - 0.7) <= 0.01 + 1e-12)
    num(I, 'p-ticket-bot', 3, nn, nbeta, {'no-prior-size': 600, 'wrong-gap': next(t for t in range(1, 5000) if F(20, t + 20) * F(7, 10) <= F(1, 100)),
                                          'prior-mean': next(t for t in range(1, 5000) if F(20, t + 20) * F(4, 10) <= F(1, 100))})
    stated(0.69, F(8 + 406, 600), 'bot posterior mean at 580')
    # finding 5: no-root band takes 27.6 as well as 27.62; finding 7: part 3 is a whole-number part
    band_takes(I, 'p-ticket-bot', 4, 'no-root', [0.01 / (0.21 / 580), 27.6, 27.62], 'no-root slip, exact and rounded')
    se580 = sqrt(0.21 / 580)
    num(I, 'p-ticket-bot', 4, 0.01 / se580, 0.01 / np.sqrt(stats.binom.var(580, 0.7)) * 580,
        {'inverted': se580 / 0.01, 'se': se580, 'no-root': 0.01 / (0.21 / 580)}, rel=1e-9)

    sa, sb = F(3, 10), F(42, 10) / 12
    num(I, 'p-routing-test', 1, sa, 3.0 / np.sqrt(100), {'by-n': F(3, 100), 'variance': sa ** 2})
    stated(0.35, sb, 'routing SE_B')
    sd_ = sqrt(sa ** 2 + sb ** 2)
    num(I, 'p-routing-test', 2, sd_, np.hypot(0.3, 0.35), {'added': sa + sb, 'no-root': sa ** 2 + sb ** 2, 'subtracted': sb - sa}, rel=1e-12)
    lo2 = 0.8 - 1.96 * sd_
    num(I, 'p-routing-test', 3, lo2, 0.8 - z * 0.4609772, {'added-se': 0.8 - 1.96 * 0.65, 'no-root': 0.8 - 1.96 * 0.2125,
                                                          'upper': 0.8 + 1.96 * sd_, 'ninety': 0.8 - 1.645 * sd_, 'no-sign': abs(lo2)}, rel=1e-3)
    # finding 6: the dropped minus sign gives 0.10, and 1.96 x 0.461 = 0.904 > 0.8 puts the lower end below 0
    stated(0.904, 1.96 * 0.461, 'routing 1.96 x 0.461', 5e-4)
    band_takes(I, 'p-routing-test', 3, 'no-sign', [abs(lo2), 0.10, 0.1035, 0.104], 'no-sign slip')
    ok(abs((0.8 - 1.96 * 0.461) - (-0.1035)) <= 0.01, 'routing: rounded SE route inside band')
    pick(I, 'p-routing-test', 4, 'no-proof')
    stated(1.7, 0.8 / sd_, 'routing z of the difference', 0.05)
    ok(lo2 < 0 < 0.8 + 1.96 * sd_, 'routing interval holds 0')

print(f'{checks} checks, {len(fails)} failures')
for f in fails:
    print('FAIL', f)
sys.exit(1 if fails else 0)
