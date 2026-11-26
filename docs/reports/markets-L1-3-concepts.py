#!/usr/bin/env python3
"""Concept audit checks: markets L1 to L3 (blind audit markets-1-3, round 1).

Run from the repository root or anywhere: python docs/reports/markets-L1-3-concepts.py
Each check prints `ok <name>` or `FAIL <name>`; exit 0 only when every check passes.
A check that fails because the content is wrong stays failing (it is a finding in
docs/reviews/audit-markets-1-3.md).

Fix pass (Opus fixer, round 1): checks re-pointed to the new wording, as the audit allowed.
- L3.hw.3 slip `end`: the line now names checking the 2-contract balance against one contract's
  4,500.00; the check recomputes that mistake and asserts it gives the slip value 0.
- code l5 bond_price test-2 and test-3: the lines now name a yield fixed at the example's 5% and a
  face discounted over a fixed 5 years; the checks submit those codings, and a new check asserts the
  discount-at-coupon and wrong-period codings fail test 1, where the new test-1 line names them.
- code l8 annualised test-2: the line now names a root fixed at 3; averaging codings are checked
  against the new test-1 line, and the mean-log-return codings against the new test-6 line.
- run_tests now returns N, not 'error', for an exception raised inside test N, as widgets/code.js does.
- New: L2.l5.s3 half-yearly equals an annual bond paying 4.05 at 5.0625% (the new explanation).

Sources: Hull, Options, Futures and Other Derivatives (ch. 2 futures mechanics, ch. 4
interest rates, duration, convexity, ch. 5 forward and futures prices); Fabozzi, Bond Markets,
Analysis and Strategies (ch. 2 to 4); Bodie, Kane and Marcus, Investments (ch. 3 margin and
short sales, ch. 5 returns, ch. 14 and 16 bonds and duration, ch. 18 dividend discount model).
"""
import json, math, os, sys, re, signal
import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'markets')
def load(name):
    with open(os.path.join(ROOT, name + '.json'), encoding='utf-8') as f:
        return json.load(f)

FAILS = []
def check(name, cond, detail=''):
    if cond:
        print('ok', name)
    else:
        print('FAIL', name, detail)
        FAILS.append(name)
def close(a, b, tol):
    return abs(a - b) <= tol

L = {n: load(n) for n in [
    'l1-interest-on-interest', 'l2-present-value', 'l3-comparing-rates', 'l4-npv', 'l5-pricing-a-bond', 'l6-yield',
    'l7-shares', 'l8-measuring-returns', 'l9-agreeing-today', 'l10-cost-of-carry', 'l11-margin',
    'l12-selling-what-you-do-not-own', 'l13-leverage', 'review-1', 'review-2', 'review-3', 'homework-1', 'homework-2', 'homework-3']}
def W(f, kind, i):
    return L[f][kind][i]['widget']
def key_and_wrongs(name, f, kind, i, answer, wrongs, tol=None):
    """The key equals `answer`; each named slip equals the stated wrong value (within the entry's own band)."""
    w = W(f, kind, i)
    t = tol if tol is not None else w['tol']['abs'] + 1e-9
    ok = close(w['answer'], answer, t)
    bad = []
    got = {x['id']: x for x in w.get('wrong', [])}
    for k, v in wrongs.items():
        if k not in got or not close(got[k]['value'], v, got[k]['tol']['abs'] + 1e-9):
            bad.append((k, v, got.get(k, {}).get('value')))
    check(name, ok and not bad, f'key {w["answer"]} vs {answer}; slips {bad}')

# ---------------------------------------------------------------- bond helpers
def bond(c, y, T, F=100.0, f=1):
    n = int(round(T * f))
    return sum(F * c / f / (1 + y / f) ** k for k in range(1, n + 1)) + F / (1 + y / f) ** n
def mod_dur(c, y, T, F=100.0):
    P = bond(c, y, T, F)
    mac = (sum(k * F * c / (1 + y) ** k for k in range(1, T + 1)) + T * F / (1 + y) ** T) / P
    return mac / (1 + y)
def convexity(c, y, T, F=100.0):
    P = bond(c, y, T, F)
    cf = [F * c] * T; cf[-1] += F
    return sum(k * (k + 1) * cf[k - 1] / (1 + y) ** (k + 2) for k in range(1, T + 1)) / P
def bisect(fn, lo, hi, n=200):
    for _ in range(n):
        mid = (lo + hi) / 2
        if fn(mid) > 0: lo = mid
        else: hi = mid
    return (lo + hi) / 2
def npv(r, flows):
    return sum(c / (1 + r) ** t for t, c in enumerate(flows))

# ================================================================ LEVEL 1
f = 'l1-interest-on-interest'
key_and_wrongs('L1.l1.s0 gap at 10 years', f, 'screens', 0, 1000 * 1.05 ** 10 - 1500, {'balance': 1000 * 1.05 ** 10, 'simple-int': 500, 'comp-int': 1000 * 1.05 ** 10 - 1000})
check('L1.l1.s0 gap at 20 years 653.30', close(1000 * 1.05 ** 20 - 2000, 653.30, 0.005))
check('L1.l1.s3 first year above 2000 is 15', 1000 * 1.05 ** 14 < 2000 < 1000 * 1.05 ** 15 and close(math.log(2) / math.log(1.05), 14.21, 0.005))
check('L1.l1.s4 -5% ten years 598.74 v 500', close(1000 * 0.95 ** 10, 598.74, 0.005))
key_and_wrongs('L1.l1.s5 2000 at 6% 5y', f, 'screens', 5, 2000 * 1.06 ** 5, {'simple': 2600, 'times': 2000 * 1.06 * 5, 'once': 2120, 'interest': 2000 * 1.06 ** 5 - 2000})
key_and_wrongs('L1.l1.s7 doubling at 20%', f, 'screens', 7, math.log(2) / math.log(1.2), {'simple': 5, 'rule72': 3.6, 'savings': math.log(2) / math.log(1.04)})
check('L1.l1.s7 rule of 72 short at high rates, close near 8%', 72 / 20 < math.log(2) / math.log(1.2) and abs(72 / 8 - math.log(2) / math.log(1.08)) < 0.01)
key_and_wrongs('L1.l1.s8 1% a month', f, 'screens', 8, 1.01 ** 12 - 1, {'twelve': 0.12, 'month': 0.01})
key_and_wrongs('L1.l1.q0', f, 'quiz', 0, 1000 * 0.98 ** 10, {'simple': 800, 'grew': 1000 * 1.02 ** 10})
check('L1.l1.q2 A 3000 v B 5604.41', close(1000 * 1.09 ** 20, 5604.41, 0.005))
key_and_wrongs('L1.l1.q3', f, 'quiz', 3, 500 * 1.04 ** 3 - 500, {'simple': 60, 'balance': 500 * 1.04 ** 3})

f = 'l2-present-value'
check('L1.l2.s0 900 grows to 1041.86', close(900 * 1.05 ** 3, 1041.86, 0.005))
key_and_wrongs('L1.l2.s1 rate for 750', f, 'screens', 1, (1000 / 750) ** (1 / 3) - 1, {'simple': (1000 / 750 - 1) / 3, 'split': 0.25 / 3})
key_and_wrongs('L1.l2.s2', f, 'screens', 2, 1000 / 1.05 ** 3, {'once': 1000 / 1.05, 'simple': 1000 / 1.15, 'minus': 850, 'grow': 1000 * 1.05 ** 3})
pv3 = 400 / 1.05 + 500 / 1.05 ** 2 + 600 / 1.05 ** 3
check('L1.l2.s3 stream 1352.77', close(pv3, 1352.77, 0.005))
key_and_wrongs('L1.l2.s4', f, 'screens', 4, 250 + pv3, {'once': 250 / 1.05 + pv3, 'ignored': pv3, 'plain': 1750})
key_and_wrongs('L1.l2.s5 perpetuity', f, 'screens', 5, 30 / 0.04, {'pct': 7.5, 'due': 780, 'once': 30 / 1.04, 'times': 1.2})
check('L1.l2.s5 perpetuity = limit of partial sums', close(sum(30 / 1.04 ** k for k in range(1, 2000)), 750, 1e-6))
key_and_wrongs('L1.l2.s6', f, 'screens', 6, 5000 / 1.06 ** 3, {'simple': 5000 / 1.18, 'once': 5000 / 1.06, 'minus': 4100, 'grow': 5000 * 1.06 ** 3})
key_and_wrongs('L1.l2.s8', f, 'screens', 8, 500 / 1.07 ** 2, {'simple': 500 / 1.14, 'once': 500 / 1.07, 'minus': 430, 'grow': 500 * 1.07 ** 2})
ann = 50000 * (1 - 1.04 ** -20) / 0.04
check('L1.l2.s9 lottery 679516.32 and distractors', close(ann, 679516.32, 0.01) and close(1e6 / 1.04, 961538.46, 0.01) and close(1e6 / 1.04 ** 20, 456386.95, 0.01))
key_and_wrongs('L1.l2.q1', f, 'quiz', 1, 1000 / 1.03 ** 10 - 1000 / 1.06 ** 10, {'simple': 1000 / 1.3 - 1000 / 1.6, 'pv6': 1000 / 1.06 ** 10})

f = 'l3-comparing-rates'
check('L1.l3.s0 banks 1126.83 v 1126.00', close(1000 * 1.01 ** 12, 1126.83, 0.005))
eff = lambda r, m: (1 + r / m) ** m - 1
check('L1.l3.s1 effective rate rises in m and stays under e^r - 1', all(eff(0.12, m) < eff(0.12, m + 1) < math.exp(0.12) - 1 for m in range(1, 400)))
key_and_wrongs('L1.l3.s2', f, 'screens', 2, eff(0.08, 4), {'nominal': 0.08, 'quarter': 0.02})
check('L1.l3.s3 6% three ways', close(1000 * 1.03 ** 2, 1060.90, 0.005) and close(1000 * 1.005 ** 12, 1061.68, 0.005) and close(1000 * (1 + 0.06 / 365) ** 365, 1061.83, 0.005))
key_and_wrongs('L1.l3.s4 continuous', f, 'screens', 4, math.exp(0.12) - 1, {'quad': 0.12 + 0.0072, 'monthly': eff(0.12, 12)})
check('L1.l3.s4 daily 12.747%, within 0.003 points', close(eff(0.12, 365), 0.12747, 5e-6) and (math.exp(0.12) - 1 - eff(0.12, 365)) * 100 < 0.003)
key_and_wrongs('L1.l3.s6 monthly rate', f, 'screens', 6, 1.12 ** (1 / 12) - 1, {'div': 0.01})
check('L1.l3.s7 AER 4.91% and 4.92% continuous', round(eff(0.048, 12) * 100, 2) == 4.91 and round((math.exp(0.048) - 1) * 100, 2) == 4.92)
check('L1.l3.s8 X 6.06%, 124.38 more', round(eff(0.059, 12) * 100, 2) == 6.06 and close(200000 * (eff(0.059, 12) - 0.06), 124.38, 0.01))
key_and_wrongs('L1.l3.s9 daily cash', f, 'screens', 9, 20000 * eff(0.045, 365), {'simple': 900, 'cont': 20000 * (math.exp(0.045) - 1)})
key_and_wrongs('L1.l3.q3 nominal for 10% AER', f, 'quiz', 3, 4 * (1.1 ** 0.25 - 1), {'quarter': 1.1 ** 0.25 - 1})
check('L1.l3.q1 5% quarterly 5.09% < 5.1%', round(eff(0.05, 4) * 100, 2) == 5.09)

f = 'l4-npv'
check('L1.l4.s0 payments worth 954.55', close(550 / 1.1 + 550 / 1.21, 954.55, 0.005))
irr1 = bisect(lambda r: npv(r, [-1000, 550, 550]), 0, 1)
check('L1.l4.s1 crosses zero between 6% and 7% (6.60%)', 0.06 < irr1 < 0.07 and close(irr1, 0.065965, 1e-6))
check('L1.l4.s2 NPV 154.19; s3 IRR 9.70%', close(npv(0.08, [-5000, 2000, 2000, 2000]), 154.19, 0.005) and close(bisect(lambda r: npv(r, [-5000, 2000, 2000, 2000]), 0, 1), 0.09701, 1e-5))
A, B = [-1000, 0, 0, 1331], [-1000, 800, 300, 100]
xs = np.linspace(0, 0.15, 15001); d = np.array([npv(x, A) - npv(x, B) for x in xs])
cross = xs[np.where(np.sign(d[:-1]) != np.sign(d[1:]))[0]]
check('L1.l4.s4 A v B: one crossing near 6.7%, values at 4% and 8%', len(cross) == 1 and close(cross[0], 0.067, 0.001) and close(npv(0.04, A), 183.25, 0.005) and close(npv(0.04, B), 135.50, 0.005) and close(npv(0.08, A), 56.59, 0.005) and close(npv(0.08, B), 77.33, 0.005))
key_and_wrongs('L1.l4.s5', f, 'screens', 5, npv(0.07, [-1100, 300, 300, 300, 300]), {'undisc': 100, 'no-cost': npv(0.07, [0, 300, 300, 300, 300]), 'once': 1200 / 1.07 - 1100, 'last': 1200 / 1.07 ** 4 - 1100})
key_and_wrongs('L1.l4.s8', f, 'screens', 8, npv(0.05, [-95, 4, 4, 104]), {'undisc': 17, 'no-cost': npv(0.05, [0, 4, 4, 104]), 'no-principal': npv(0.05, [-95, 4, 4, 4])})
check('L1.l4.s8 IRR 5.87%; s9 IRR 7.51%', round(bisect(lambda r: npv(r, [-95, 4, 4, 104]), 0, 1) * 100, 2) == 5.87 and round(bisect(lambda r: npv(r, [-130000, 50000, 50000, 50000]), 0, 1) * 100, 2) == 7.51)
key_and_wrongs('L1.l4.s9', f, 'screens', 9, npv(0.07, [-130000] + [50000] * 3), {'undisc': 20000, 'at8': npv(0.08, [-130000] + [50000] * 3)})
# Finding 1: "NPV falls as the rate rises" needs an outlay followed by inflows. Counter-example (a loan-shaped stream, and a stream with two IRRs).
loan = [1000, -550, -550]
check('L1.l4 NPV falls in r for outlay-then-inflow streams (the lesson\'s own)', all(npv(r, [-5000, 2000, 2000, 2000]) > npv(r + 0.01, [-5000, 2000, 2000, 2000]) for r in np.arange(0, 0.5, 0.01)))
print('   note (finding 1): loan-shaped stream NPV at 5%% %.2f, at 10%% %.2f (rises with r); [-100, 230, -132] has IRRs 10%% and 20%%: %.4f %.4f'
      % (npv(0.05, loan), npv(0.10, loan), npv(0.10, [-100, 230, -132]), npv(0.20, [-100, 230, -132])))
check('L1.l4.summary "NPV falls as the rate rises" states its hypothesis (outlay then inflows)',
      bool(re.search(r'outlay|first|inflow|comes back|conventional', L[f]['summary']['ideas'][2])), L[f]['summary']['ideas'][2])

f = 'review-1'
def item_kw(name, file, i, ans, wr):
    key_and_wrongs(name, file, 'items', i, ans, wr)
item_kw('L1.rev.0', f, 0, 5000 * 1.03 ** 6, {'simple': 5900, 'interest': 5000 * 1.03 ** 6 - 5000})
item_kw('L1.rev.1', f, 1, 2500 / 1.06 ** 4, {'simple': 2500 / 1.24, 'once': 2500 / 1.06})
item_kw('L1.rev.2', f, 2, eff(0.09, 12), {'month': 0.0075})
item_kw('L1.rev.3', f, 3, npv(0.06, [-800, 300, 300, 300]), {'undisc': 100})
item_kw('L1.rev.5', f, 5, 10000 / 1.005 ** 24, {'annual': 10000 / 1.06 ** 2, 'simple': 10000 / 1.12})
item_kw('L1.rev.6', f, 6, 1.08 ** 0.25 - 1, {'div': 0.02})
check('L1.rev.7 A v B at 5% and 10%, equal near 7.7%', close(npv(0.05, [-2000, 0, 2600]), 358.28, 0.005) and close(npv(0.05, [-2000, 1300, 1200]), 326.53, 0.005) and close(npv(0.10, [-2000, 0, 2600]), 148.76, 0.005) and close(npv(0.10, [-2000, 1300, 1200]), 173.55, 0.005) and close(1400 / 1300 - 1, 0.077, 0.0005))
f = 'homework-1'
item_kw('L1.hw.0', f, 0, 3000 * 1.018 ** 24, {'simple': 3000 * (1 + 0.018 * 24), 'annual': 3000 * 1.216 ** 2, 'interest': 3000 * 1.018 ** 24 - 3000})
item_kw('L1.hw.1', f, 1, 1000 / 1.05 + 2000 / 1.05 ** 3 + 3000 / 1.05 ** 5, {'plain': 6000, 'all-five': 6000 / 1.05 ** 5, 'all-three': 6000 / 1.05 ** 3})
aers = [eff(0.046, 12), 0.047, math.exp(0.0455) - 1, eff(0.0465, 4)]
check('L1.hw.2 AERs 4.698, 4.700, 4.655, 4.732; quarterly highest', [round(a * 100, 3) for a in aers] == [4.698, 4.7, 4.655, 4.732] and max(aers) == aers[3])
check('L1.hw.3 r = 12((1+a)^(1/12) - 1) = 4.89% at a = 5%', round(12 * (1.05 ** (1 / 12) - 1) * 100, 2) == 4.89)
item_kw('L1.hw.6 quadratic IRR', f, 6, (550 + math.sqrt(550 ** 2 + 4 * 1000 * 550)) / 2000 - 1, {'simple': 0.0667, 'u': 1.065965, 'neg': (550 - math.sqrt(550 ** 2 + 4 * 1000 * 550)) / 2000 - 1})
af = lambda r, n: (1 - (1 + r) ** -n) / r
check('L1.hw.7 model: 611564.69, 560799.47, 600875.25, 595634.83, break-even 4.22%, last payment 20537.41',
      close(45000 * af(0.04, 20), 611564.69, 0.01) and close(45000 * af(0.05, 20), 560799.47, 0.01) and close(45000 * af(0.042, 20), 600875.25, 0.01)
      and close(45000 * af(0.043, 20), 595634.83, 0.01) and round(bisect(lambda r: 45000 * af(r, 20) - 600000, 0.01, 0.2) * 100, 2) == 4.22 and close(45000 / 1.04 ** 20, 20537.41, 0.01))

# ================================================================ LEVEL 2
f = 'l5-pricing-a-bond'
key_and_wrongs('L2.l5.s1 price 95.67', f, 'screens', 1, bond(0.04, 0.05, 5), {'no-discount': 120, 'par': 100, 'last-only': 104 / 1.05 ** 5, 'coupons-only': 4 * af(0.05, 5)})
key_and_wrongs('L2.l5.s3 half-yearly 95.62', f, 'screens', 3, bond(0.04, 0.05, 5, f=2), {'annual': bond(0.04, 0.05, 5), 'full-coupon': 4 * af(0.025, 10) + 100 / 1.025 ** 10, 'full-rate': 2 * af(0.05, 10) + 100 / 1.05 ** 10, 'five-periods': 2 * af(0.025, 5) + 100 / 1.025 ** 5})
# Finding 4: the half-yearly price is not always lower; it moves further from par (premium bonds price higher, as the lesson's own quiz 3 shows).
check('L2.l5 half-yearly pricing moves away from par: discount lower, premium higher, par unchanged',
      bond(0.04, 0.05, 5, f=2) < bond(0.04, 0.05, 5) and bond(0.06, 0.04, 2, f=2) > bond(0.06, 0.04, 2) and close(bond(0.05, 0.05, 7, f=2), 100, 1e-9))
check('L2.l5.s3 half-yearly price equals an annual bond paying 2 x 1.025 + 2 = 4.05 at 1.025^2 - 1 = 5.0625% (the explanation)',
      close(2 * 1.025 + 2, 4.05, 1e-12) and close(4.05 * af(0.050625, 5) + 100 / 1.050625 ** 5, bond(0.04, 0.05, 5, f=2), 1e-9) and round(0.050625 * 100, 2) == 5.06)
check('L2.l5.s3.explain gives a reason that also covers a premium bond (not only "compounds to 5.06%")',
      not re.search(r'because 2\.5% a half compounds to 5\.06% a year', L[f]['screens'][3]['explain']['text']), L[f]['screens'][3]['explain']['text'][-90:])
key_and_wrongs('L2.l5.s5 zero', f, 'screens', 5, 100 / 1.05 ** 5, {'coupon-bond': bond(0.04, 0.05, 5), 'with-coupon': 104 / 1.05 ** 5, 'simple': 80})
check('L2.l5.s7 102.72 and swapped 97.33', close(bond(0.06, 0.05, 3), 102.72, 0.005) and close(bond(0.05, 0.06, 3), 97.33, 0.005))
check('L2.l5.s8 closed form C/y (1 - v^T) + F v^T', all(close(4 / y * (1 - (1 + y) ** -T) + 100 * (1 + y) ** -T, bond(0.04, y, T), 1e-9) for y in (0.01, 0.05, 0.09) for T in (1, 5, 30)))
key_and_wrongs('L2.l5.s10 dirty price', f, 'screens', 10, 98.50 * 100 + 0.5 * 200, {'clean': 9850, 'per-pound': 985000, 'whole-coupon': 10050, 'full-year': 10250})
key_and_wrongs('L2.l5.q1', f, 'quiz', 1, bond(0.06, 0.04, 2), {'undiscounted': 112, 'coupon-rate': 100, 'principal': 100 / 1.04 ** 2})
key_and_wrongs('L2.l5.q2', f, 'quiz', 2, 100 / 1.05 ** 10, {'simple': 100 / 1.5, 'ten-off': 50})
key_and_wrongs('L2.l5.q3', f, 'quiz', 3, bond(0.06, 0.04, 2, f=2), {'annual': bond(0.06, 0.04, 2), 'full-coupon': 6 * af(0.02, 4) + 100 / 1.02 ** 4, 'two-periods': 3 * af(0.02, 2) + 100 / 1.02 ** 2})

f = 'l6-yield'
y92 = bisect(lambda y: bond(0.04, y, 5) - 92, 0, 1)
check('L2.l6.s2 YTM at 92 is 5.894%; 92.18 at 5.85%, 91.97 at 5.90%', close(y92, 0.05894, 5e-6) and close(bond(0.04, 0.0585, 5), 92.18, 0.005) and close(bond(0.04, 0.059, 5), 91.97, 0.005))
check('L2.l6.s3 bisection table 91.58, 95.67, 93.59, 92.58, 92.07', [round(bond(0.04, y, 5), 2) for y in (0.06, 0.05, 0.055, 0.0575, 0.05875)] == [91.58, 95.67, 93.59, 92.58, 92.07])
def newton(y0, steps):
    y = y0
    for _ in range(steps):
        h = 1e-7; g = (bond(0.04, y + h, 5) - bond(0.04, y - h, 5)) / (2 * h)
        y -= (bond(0.04, y, 5) - 92) / g
    return y
check('L2.l6.s3 20 halvings of [4%, 8%] give 0.000004 points; Newton from either end is as close in 3 steps',
      close(4 / 2 ** 20, 0.0000038, 1e-7) and all(abs(newton(s, 3) - y92) * 100 < 4 / 2 ** 20 for s in (0.04, 0.06, 0.08)))
D5, C5 = mod_dur(0.04, 0.05, 5), convexity(0.04, 0.05, 5)
check('L2.l6.s4 modified duration 4.40, slope 4.2098 per point, convexity 24.47', close(D5, 4.40, 0.005) and close(D5 * bond(0.04, 0.05, 5) / 100, 4.2098, 5e-5) and close(C5, 24.47, 0.005))
key_and_wrongs('L2.l6.s4 tangent fall', f, 'screens', 4, 4.40 * 95.67 * 0.01, {'no-price': 4.4, 'pct': 0.044, 'true': bond(0.04, 0.05, 5) - bond(0.04, 0.06, 5)})
check('L2.l6.s5 2y and 10y: prices, changes -1.84% and -7.58%, durations 1.87 and 7.96',
      [round(bond(0.04, y, T), 2) for T in (2, 10) for y in (0.05, 0.06)] == [98.14, 96.33, 92.28, 85.28] and close((96.33 / 98.14 - 1) * 100, -1.84, 0.006)
      and close((85.28 / 92.28 - 1) * 100, -7.58, 0.006) and close(mod_dur(0.04, 0.05, 2), 1.87, 0.005) and close(mod_dur(0.04, 0.05, 10), 7.96, 0.005))
key_and_wrongs('L2.l6.s6 zero duration', f, 'screens', 6, 5 / 1.05, {'macaulay': 5, 'coupon': 4.4, 'times': 5.25})
check('L2.l6.s6 zero: Macaulay = T and numerical -P\'/P = T/(1+y)', close(-(100 / 1.0501 ** 5 - 100 / 1.0499 ** 5) / 0.0002 / (100 / 1.05 ** 5), 5 / 1.05, 1e-4))
key_and_wrongs('L2.l6.s8 current yield', f, 'screens', 8, 4 / 95.67, {'ytm': 0.05, 'coupon': 0.04, 'inverse': 4.33 / 95.67})
durs = {'zero10': 10 / 1.05, 'coupon10': mod_dur(0.08, 0.05, 10), 'short': mod_dur(0.04, 0.05, 2), 'zero2': 2 / 1.05}
check('L2.l6.s9 10y zero has the largest duration (9.52); both 2y under 2', max(durs, key=durs.get) == 'zero10' and close(durs['zero10'], 9.52, 0.005) and durs['short'] < 2 and durs['zero2'] < 2)
check('L2.l6.s10 428,058 on the 5y 4% bond', close(1e7 * (1 - bond(0.04, 0.06, 5) / bond(0.04, 0.05, 5)), 428058, 1))
p8 = bond(0.04, 0.08, 5); p5 = bond(0.04, 0.05, 5)
check('L2.l6.q3 84.03, -12.2%, tangent 83.04, convexity closes most of the gap', close(p8, 84.03, 0.005) and close((p8 / p5 - 1) * 100, -12.2, 0.05) and close(p5 - 3 * 4.2098, 83.04, 0.005)
      and abs((-D5 * 0.03 + 0.5 * C5 * 0.03 ** 2) - (p8 / p5 - 1)) < 0.2 * abs(-D5 * 0.03 - (p8 / p5 - 1)))
# Finding 5: holding to maturity earns the purchase yield only if coupons are reinvested at it.
fv6 = sum(4 * 1.06 ** (5 - k) for k in range(1, 6)) + 100; fv5 = sum(4 * 1.05 ** (5 - k) for k in range(1, 6)) + 100
print('   note (finding 5): realised 5-year return on 95.67 with coupons reinvested at 6%%: %.3f%%; at 5%%: %.3f%%' % (((fv6 / p5) ** 0.2 - 1) * 100, ((fv5 / p5) ** 0.2 - 1) * 100))
check('L2.l6.s7 held to maturity earns 5% when coupons are reinvested at 5% (and more at 6%)', close((fv5 / p5) ** 0.2 - 1, 0.05, 1e-9) and (fv6 / p5) ** 0.2 - 1 > 0.05)

f = 'l7-shares'
check('L2.l7.s5 DDM 40, 39.97 after 150 years, first ten 15.10', close(2 / 0.05, 40, 1e-9) and close(sum(2 * 1.03 ** (k - 1) / 1.08 ** k for k in range(1, 151)), 39.97, 0.005) and close(sum(2 * 1.03 ** (k - 1) / 1.08 ** k for k in range(1, 11)), 15.10, 0.005))
check('L2.l7.s6 D/(r-g) equals the series (several g, r)', all(close(sum(D * (1 + g) ** (k - 1) / (1 + r) ** k for k in range(1, 6000)), D / (r - g), 1e-6) for D, g, r in ((2, 0.03, 0.08), (1.5, 0.04, 0.09), (3, 0.02, 0.09))))
check('L2.l7.s7 28.57, down 29%; s8 each dividend worth 1.85', close(2 / 0.07, 28.57, 0.005) and round((1 - (2 / 0.07) / 40) * 100) == 29 and close(2 / 1.08, 1.85, 0.005))
check('L2.l7.s11 rights issue 4.60; hw 5.43', close((4 * 5 + 3) / 5, 4.60, 1e-9) and close((5 * 6 + 2 * 4) / 7, 5.43, 0.005))

f = 'l8-measuring-returns'
key_and_wrongs('L2.l8.s0 total return', f, 'screens', 0, (53 + 1.5 - 50) / 50, {'price-only': 0.06, 'div-only': 0.03})
key_and_wrongs('L2.l8.s3 annualised', f, 'screens', 3, 1.134 ** (1 / 3) - 1, {'divide': 0.134 / 3, 'average': 0.05})
key_and_wrongs('L2.l8.s4 log returns', f, 'screens', 4, math.log(1.134), {'simple': 0.15})
check('L2.l8.s2 -3.00% and 12.00%', close((40.42 + 1.29 - 43) / 43, -0.03, 1e-4) and close((44.06 + 1.21 - 40.42) / 40.42, 0.12, 1e-4))
check('L2.l8.s5 -13.4%; s6 9.38% and 26.82%; s9 18.50, 5.82, 6.33', close(0.75 ** 0.5 - 1, -0.134, 5e-4) and close(1.0075 ** 12 - 1, 0.0938, 5e-5) and close(1.02 ** 12 - 1, 0.2682, 5e-5)
      and close(1.12 * 0.92 * 1.15, 1.18496, 1e-9) and close(1.18496 ** (1 / 3) - 1, 0.0582, 5e-5))
rng = np.random.default_rng(20261126)
# "The annualised return sits below the average because the returns varied" / "averaging overstates growth": AM >= GM, strict when returns vary.
R = rng.normal(0.06, 0.18, size=(200000, 5)).clip(-0.95)
gm = np.prod(1 + R, axis=1) ** 0.2 - 1; am = R.mean(axis=1)
check('L2.l8 arithmetic average >= annualised return in every one of 200,000 random 5-year paths', bool(np.all(am >= gm - 1e-12)))
# "A few years of data could not tell [Sharpe 0.42 and 0.40] apart": Monte Carlo of the sample Sharpe ratio.
def sharpe_wrong_rate(T, n=200000):
    a = rng.normal(0.09, 0.12, size=(n, T)); b = rng.normal(0.12, 0.20, size=(n, T))
    sa = (a.mean(1) - 0.04) / a.std(1, ddof=1); sb = (b.mean(1) - 0.04) / b.std(1, ddof=1)
    return float(np.mean(sb > sa)), float(sa.std())
w5, se5 = sharpe_wrong_rate(5); w10, se10 = sharpe_wrong_rate(10)
print('   Sharpe MC: 5 years: B ranks above A in %.1f%% of samples, sd of estimate %.2f; 10 years: %.1f%%, sd %.2f' % (w5 * 100, se5, w10 * 100, se10))
check('L2.l8.s11 a few years cannot separate Sharpe 0.42 from 0.40 (wrong ranking in over 45% of 5- and 10-year samples)', w5 > 0.45 and w10 > 0.45 and se5 > 10 * 0.02)
key_and_wrongs('L2.l8.q2', f, 'quiz', 2, math.exp(0.04) - 1, {'sum': 0.04})

f = 'review-2'
item_kw('L2.rev.0', f, 0, bond(0.05, 0.06, 3, f=2), {'annual': bond(0.05, 0.06, 3), 'full-coupon': 5 * af(0.03, 6) + 100 / 1.03 ** 6, 'full-rate': 2.5 * af(0.06, 6) + 100 / 1.06 ** 6})
check('L2.rev.1 2y 8% duration 1.84 is the smallest of the four; rev.4 price 94.00; rev.7 98.17, 97.27, YTM 6.09%',
      close(mod_dur(0.08, 0.05, 2), 1.84, 0.005) and mod_dur(0.08, 0.05, 2) < min(2 / 1.05, mod_dur(0.08, 0.05, 10), 10 / 1.05) and close(bond(0.03, 0.04, 7), 94.00, 0.005)
      and close(bond(0.05, 0.06, 2), 98.17, 0.005) and close(bond(0.05, 0.065, 2), 97.27, 0.005) and round(bisect(lambda y: bond(0.05, y, 2) - 98, 0, 1) * 100, 2) == 6.09)
f = 'homework-2'
item_kw('L2.hw.1 YTM', f, 1, bisect(lambda y: bond(0.05, y, 3) - 97, 0, 1), {'current': 5 / 97, 'coupon': 0.05})
p4 = bond(0.04, 0.06, 4)
item_kw('L2.hw.7 one-year return', f, 7, (p4 + 4 - 95.67) / 95.67, {'unchanged': 0.05, 'no-coupon': (p4 - 95.67) / 95.67, 'five-year': (bond(0.04, 0.06, 5) + 4 - 95.67) / 95.67})
P = bond(0.05, 0.06, 4); slope = sum(t * c / 1.06 ** (t + 1) for t, c in ((1, 5), (2, 5), (3, 5), (4, 105)))
check('L2.hw.8 model: 96.5349, current yield 5.18%, slope 338.58, D 3.51, 94.86 at 6.5%, 97.33 and 6.00% after a year, share 50.00 to 42.86 (-14.3%), 1/(r-g) = 16.7',
      close(P, 96.5349, 5e-5) and round(5 / 96.53 * 100, 2) == 5.18 and close(slope, 338.58, 0.005) and close(slope / P, 3.51, 0.005) and close(bond(0.05, 0.065, 4), 94.86, 0.005)
      and close(bond(0.05, 0.06, 3), 97.33, 0.005) and close((bond(0.05, 0.06, 3) + 5 - P) / P, 0.06, 1e-9) and close(3 / 0.07, 42.86, 0.005) and close(1 - (3 / 0.07) / 50, 0.143, 5e-4) and close(1 / 0.06, 16.7, 0.05))

# ================================================================ LEVEL 3
f = 'l10-cost-of-carry'
F_div = (100 - 2 / 1.05 ** 0.5) * 1.05
key_and_wrongs('L3.l10.s7 forward with dividend', f, 'screens', 7, F_div, {'ignored': 105, 'not-grown': 103, 'not-disc': 98 * 1.05, 'added': 107})
check('L3.l10.s7 two routes agree: (S - PV(D))(1+r) = S(1+r) - D(1+r)^0.5', close(F_div, 105 - 2 * 1.05 ** 0.5, 1e-12) and close(100 * math.exp(0.05), 105.13, 0.005))
# No-arbitrage by replication under random terminal prices: cash-and-carry profit is F_quote - F_fair whatever S_T is.
ST = rng.lognormal(math.log(100), 0.4, 100000)
cc = (104 - ST) + ST + 2 * 1.05 ** 0.5 - 100 * 1.05          # short forward at 104 + share + reinvested dividend - loan
rcc = (ST - 102) - ST + 100 * 1.05 - 0                        # no-dividend case: long forward at 102, short share, lend
check('L3.l10 cash and carry / reverse profits are riskless: 1.05 (hw item 2) and 3.00 (s4) for every S_T', np.ptp(cc) < 1e-9 and close(cc[0], 1.05, 0.006) and np.ptp(rcc) < 1e-9 and close(rcc[0], 3.0, 1e-9))
key_and_wrongs('L3.l10.s8 covered interest parity', f, 'screens', 8, 1.25 * 1.05 / 1.04, {'inverted': 1.25 * 1.04 / 1.05, 'spot': 1.25, 'dollars': 1.3125})
w = W(f, 'screens', 9)
check('L3.l10.s9 index forward: key band holds the linear (7920), exact (7923.8) and continuous (7920.4) values; slips outside',
      all(abs(v - w['answer']) <= w['tol']['abs'] for v in (8000 * 0.99, 8000 * 1.04 / 1.05, 8000 * math.exp(-0.01))) and all(abs(x['value'] - w['answer']) > w['tol']['abs'] + x['tol']['abs'] for x in w['wrong']))
key_and_wrongs('L3.l10.q0', f, 'quiz', 0, 50 * 1.04 ** 2, {'simple': 54, 'one-year': 52})
key_and_wrongs('L3.l10.q2 gold with storage', f, 'quiz', 2, (2000 + 10 / 1.05) * 1.05, {'no-storage': 2100, 'minus': 2090})

f = 'l11-margin'
def margin_calls(prices, contracts, pv, initial, maint):
    n = abs(contracts); bal = initial * n; calls = []; bals = []
    for a, b in zip(prices, prices[1:]):
        bal += contracts * pv * (b - a); bals.append(bal)
        c = initial * n - bal if bal < maint * n else 0
        calls.append(c); bal += c
    return calls, bals
c, b = margin_calls([8000, 7960, 7900, 7830, 7830, 7880], 1, 10, 6000, 4500)
check('L3.l11.s3 table: balances 5600, 5000, 4300, 6000, 6500; one call 1700', b == [5600, 5000, 4300, 6000, 6500] and c == [0, 0, 1700, 0, 0])
c, b = margin_calls([8000, 7930, 7840, 7900, 7880], 1, 10, 6000, 4500)
check('L3.l11.s5 trap week: call 1600 after day 2 only; colleague\'s end-of-week sum leaves 4800 and no call', c == [0, 1600, 0, 0] and 6000 - 1200 == 4800 > 4500)
check('L3.l11.s8 pension fund call 25000 on a 250-point rally; shares gain 25000', margin_calls([8000, 8250], -10, 10, 6000, 4500)[0] == [25000] and close(800000 * 250 / 8000, 25000, 1e-9))
check('L3.rev.3 three contracts call 6000', margin_calls([8000, 7800], 3, 10, 6000, 4500)[0] == [6000])
c, b = margin_calls([8000, 7900, 7820, 7850, 7700, 7640], 2, 10, 6000, 4500)
check('L3.hw.3 two calls of 3600, total 7200; balances 10000, 8400, 12600, 9600, 8400', c == [0, 3600, 0, 0, 3600] and b == [10000, 8400, 12600, 9600, 8400])
# Finding 10: the slip `end` (value 0) is described as "You settled the week at once", but settling the week at once gives a call of 7200.
once_bal = 12000 - 2 * 10 * (8000 - 7640)
once_call = 12000 - once_bal if once_bal < 9000 else 0
hw3 = L['homework-3']['items'][3]
end_val = [x['value'] for x in hw3['widget']['wrong'] if x['id'] == 'end'][0]
check('L3.hw.3 slip `end`: the line no longer names "settled the week at once" (that gives the key, 7200)',
      not ('settled the week at once' in hw3['feedback']['byKey']['end'] and once_call != end_val), f'settling once gives a call of {once_call}, the slip value is {end_val}')
c4500, _ = margin_calls([8000, 7900, 7820, 7850, 7700, 7640], 2, 10, 6000, 2250)   # 2 contracts against 4500 in all: per-contract level 2250
check('L3.hw.3 slip `end`: the mistake it now names (2-contract balance against one contract\'s 4,500) gives the slip value',
      '£4,500.00' in hw3['feedback']['byKey']['end'] and sum(c4500) == end_val == 0, f'calls {c4500}, slip {end_val}')

f = 'l12-selling-what-you-do-not-own'
check('L3.l12.s3 profit 7025; s4 -15975; s9 -52000; q0 985; q2 -550; hw.5 -7180; rev.4 -920',
      1000 * 8 - 50000 * 0.03 * 0.25 - 600 == 7025 and -15000 - 975 == -15975 and 100000 - 150000 - 2000 == -52000 and 200 * 5 - 15 == 985 and -500 - 50 == -550 and -6000 - 1000 - 180 == -7180 and 300 * (15 - 18) - 20 == -920)
# Finding 8: a dividend is a cash flow the short pays, but the share goes ex-dividend by about the same amount, so it is not a net cost.
print('   note (finding 8): short 1 share at 50, dividend 0.60, nothing else changes: ex-dividend price 49.40; P&L = 50 - 49.40 - 0.60 = %.2f' % (50 - 49.40 - 0.60))
check('L3.l12.s2.explain says the ex-dividend price fall offsets the dividend the short pays',
      bool(re.search(r'ex-dividend|falls by|drops by|offset', L[f]['screens'][2]['explain']['text'])), L[f]['screens'][2]['explain']['text'][-80:])

f = 'l13-leverage'
RE = lambda Lv, ra, r: Lv * ra - (Lv - 1) * r
check('L3.l13 R_E = L R_A - (L-1) r: 15%, 25% and -55% at L=4, -65%, 14% and -34%, 20%', close(RE(2, 0.1, 0.05), 0.15, 1e-12) and close(RE(4, 0.1, 0.05), 0.25, 1e-12) and close(RE(4, -0.1, 0.05), -0.55, 1e-12)
      and close(RE(2, -0.3, 0.05), -0.65, 1e-12) and close(RE(3, 0.08, 0.05), 0.14, 1e-12) and close(RE(3, -0.08, 0.05), -0.34, 1e-12) and close(RE(2, 0.12, 0.04), 0.20, 1e-12))
check('L3.l13 formula equals the cash accounting for random L, R_A, r', all(close((Lv * (1 + ra) - (Lv - 1) * (1 + r)) - 1, RE(Lv, ra, r), 1e-12) for Lv, ra, r in rng.uniform([1, -0.9, 0], [6, 0.9, 0.2], size=(1000, 3))))
check('L3.l13.s7 margin trigger 13333.33 (fall of a third); rev.8 25714.29 (14.3%, 2.5x); hw.6 fall of 1/9; hw.7 short call at 15.38%',
      close(10000 / 0.75, 13333.33, 0.005) and close(1 - 10000 / 0.75 / 20000, 1 / 3, 1e-9) and close(18000 / 0.7, 25714.29, 0.005) and close(1 - 18000 / 0.7 / 30000, 0.143, 5e-4)
      and close(1 - (8 / 3) / 3, 1 / 9, 1e-12) and close(10000 / 65000, 0.1538, 5e-5) and close((75000 - 50000 * (1 + 10 / 65)) / (50000 * (1 + 10 / 65)), 0.30, 1e-9))
check('L3.l13.s8 equity falls 63%; a further fall of about 15% wipes it out', close((0.2 * 300000 + 200000 * 0.06 * 0.25) / 100000, 0.63, 1e-12) and close(37000 / 240000, 0.154, 0.001))
# "Volatility scales with L" and "leverage makes 50% losses far more likely": Monte Carlo, annual asset return N(7%, 15%), r = 5%.
ra = rng.normal(0.07, 0.15, 2_000_000)
sd1, sd3 = ra.std(), RE(3, ra, 0.05).std()
p1, p3 = np.mean(ra <= -0.5), np.mean(RE(3, ra, 0.05) <= -0.5)
print('   leverage MC: sd unlevered %.3f, at L=3 %.3f; P(lose half) unlevered %.2e, at L=3 %.4f' % (sd1, sd3, p1, p3))
check('L3.l13 volatility scales with L (15% -> 45%); a 50% loss is far more likely at L = 3', close(sd3 / sd1, 3, 1e-9) and p3 > 100 * max(p1, 1e-7))

f = 'review-3'
item_kw('L3.rev.1', f, 1, 80 * 1.03 ** 2, {'simple': 84.8, 'one': 82.4})
item_kw('L3.rev.7', f, 7, (60 - 1.5 / 1.04 ** 0.25) * 1.04, {'ignored': 62.4, 'not-grown': 60.9, 'not-disc': 58.5 * 1.04})
f = 'homework-3'
item_kw('L3.hw.2', f, 2, 104 - F_div, {'no-div': -1, 'vs-spot': 4, 'not-grown': 1})
up = (64 - 1.2 * 1.07 ** -0.5) * 1.07; lo = (64 - 1.2 * 1.03 ** -0.5) * 1.03 - 0.5
check('L3.hw.9 band: upper 67.2387 (67.2621 if the dividend is deposited), lower 64.2021 (64.1787 if the dividend is borrowed), one-rate price 65.9704, profit 0.5613 at 67.80',
      close(up, 67.2387, 5e-5) and close(64 * 1.07 - 1.2 * 1.03 ** 0.5, 67.2621, 5e-5) and close(lo, 64.2021, 5e-5) and close(64 * 1.03 - 1.2 * 1.07 ** 0.5 - 0.5, 64.1787, 5e-5)
      and close((64 - 1.2 * 1.05 ** -0.5) * 1.05, 65.9704, 5e-5) and close(67.80 - up, 0.5613, 5e-5) and close(1.2 * 1.07 ** -0.5, 1.1601, 5e-5) and close(1.2 * 1.03 ** -0.5, 1.1824, 5e-5))
check('L3.hw.8 jet fuel: 642, payoffs -720000 and +580000, total 6,420,000 both ways, 18 a tonne at a 660 quote',
      600 * 1.05 + 12 == 642 and 10000 * (570 - 642) == -720000 and 10000 * (700 - 642) == 580000 and 5700000 + 720000 == 7000000 - 580000 == 6420000 and 660 - 630 - 12 == 18)
# Finding 11: for a commodity held for use the carry price is an upper limit, not an equality (Hull 5.11, consumption assets).
check('L3.hw.8 model says the carry price is an upper limit for a commodity held for use (convenience yield)',
      bool(re.search(r'upper|at most|convenience|cannot be sold short|limit', L[f]['items'][8]['model'].split('**2.')[0])), 'part 1 states an equality for jet fuel')

# ================================================================ CODE WIDGETS (rule 6 sweeps)
def run_tests(src, fname, tests):
    """Index (1-based) of the first failing hidden test, 0 if all pass, 'error' on an exception. Mirrors widgets/code.js: isclose rel 1e-9, or equality."""
    env = {}
    try:
        exec(src, env)
    except Exception:
        return 'error'
    def _alarm(*_):
        raise TimeoutError
    signal.signal(signal.SIGALRM, _alarm)
    for i, t in enumerate(tests, 1):
        try:
            signal.alarm(3)          # the page stops a run that takes too long; a loop that never ends is an error there too
            got = eval(t['call'], env); exp = eval(t['expect'], {})
        except Exception:
            return i                 # the page gives test-N for an exception inside test N (AUTHORING, engine pass 7)
        finally:
            signal.alarm(0)
        if t.get('compare') == 'isclose':
            seq = lambda v: v if isinstance(v, (list, tuple)) else [v]
            ok = len(seq(got)) == len(seq(exp)) and all(isinstance(a, (int, float)) and math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12) for a, b in zip(seq(got), seq(exp)))
        else:
            ok = got == exp
        if not ok:
            return i
    return 0
def code_widget(fkey, kind, i):
    w = L[fkey][kind][i]['widget']; fb = L[fkey][kind][i].get('feedback', {}).get('byKey', {})
    return w, fb
codes = [('l4-npv', 'screens', 7), ('l5-pricing-a-bond', 'screens', 9), ('l8-measuring-returns', 'screens', 10), ('homework-1', 'items', 5), ('homework-2', 'items', 3), ('homework-3', 'items', 4)]
for fk, kind, i in codes:
    w, fb = code_widget(fk, kind, i)
    s, st = run_tests(w['solution'], None, w['tests']), run_tests(w['starter'], None, w['tests'])
    check(f'code {fk}[{i}]: solution passes all {len(w["tests"])} hidden tests and the starter does not', s == 0 and st != 0, f'solution {s}, starter {st}')

def mutants_first_fail(fk, kind, i, mutants):
    w, _ = code_widget(fk, kind, i)
    return {name: run_tests(src, None, w['tests']) for name, src in mutants.items()}

# l4 npv: obvious wrong programs must fail some test.
m = mutants_first_fail('l4-npv', 'screens', 7, {
    'discount t+1': "def npv(rate, flows):\n    return sum(c / (1 + rate) ** (t + 1) for t, c in enumerate(flows))",
    'simple interest': "def npv(rate, flows):\n    return sum(c / (1 + rate * t) for t, c in enumerate(flows))",
    'no discount': "def npv(rate, flows):\n    return sum(flows)",
    'multiply': "def npv(rate, flows):\n    return sum(c * (1 + rate) ** t for t, c in enumerate(flows))"})
check('code l4 npv: four wrong programs each fail a hidden test', all(v != 0 for v in m.values()), str(m))

# l5 bond_price: byKey test-2 names "discount at coupon, not yld"; test-3 names "face not discounted over years".
bp = "def bond_price(face, coupon, years, yld):\n    price = 0.0\n    for t in range(1, years + 1):\n        price += %s\n    price += %s\n    return price"
m2 = mutants_first_fail('l5-pricing-a-bond', 'screens', 9, {
    'coupons and face discounted at coupon': bp % ('face * coupon / (1 + coupon) ** t', 'face / (1 + coupon) ** years'),
    'coupons discounted at coupon, face at yld': bp % ('face * coupon / (1 + coupon) ** t', 'face / (1 + yld) ** years'),
    'face discounted at coupon only': bp % ('face * coupon / (1 + yld) ** t', 'face / (1 + coupon) ** years')})
m3 = mutants_first_fail('l5-pricing-a-bond', 'screens', 9, {
    'face not discounted': bp % ('face * coupon / (1 + yld) ** t', 'face'),
    'face discounted one year': bp % ('face * coupon / (1 + yld) ** t', 'face / (1 + yld)'),
    'face discounted years - 1': bp % ('face * coupon / (1 + yld) ** t', 'face / (1 + yld) ** (years - 1)'),
    'face left out': bp % ('face * coupon / (1 + yld) ** t', '0')})
print('   l5 bond_price first failing test: discount-at-coupon codings', m2, '; face-discount codings', m3)
fb5 = code_widget('l5-pricing-a-bond', 'screens', 9)[1]
check('code l5 bond_price byKey test-1 (discount at `yld`, face over `years`): the discount-at-coupon and wrong-period codings all fail test 1 first',
      'test-1' in fb5 and all(v == 1 for v in list(m2.values()) + list(m3.values())), str(m2) + str(m3))
m2b = mutants_first_fail('l5-pricing-a-bond', 'screens', 9, {
    'both at 1.05': bp % ('face * coupon / 1.05 ** t', 'face / 1.05 ** years'),
    'coupons at 0.05': bp % ('face * coupon / (1 + 0.05) ** t', 'face / (1 + yld) ** years'),
    'face at 1.05': bp % ('face * coupon / (1 + yld) ** t', 'face / 1.05 ** years')})
m3b = mutants_first_fail('l5-pricing-a-bond', 'screens', 9, {
    'face ** 5': bp % ('face * coupon / (1 + yld) ** t', 'face / (1 + yld) ** 5'),
    'loop and face at 5': bp.replace('range(1, years + 1)', 'range(1, 6)') % ('face * coupon / (1 + yld) ** t', 'face / (1 + yld) ** 5'),
    'face * v ** -5': bp % ('face * coupon / (1 + yld) ** t', 'face * (1 + yld) ** -5')})
check('code l5 bond_price byKey test-2 (yield fixed at the example\'s 5%): every such coding fails test 2 first', 'fixed 5%' in fb5.get('test-2', '') and all(v == 2 for v in m2b.values()), str(m2b))
check('code l5 bond_price byKey test-3 (face over a fixed 5 years): every such coding fails test 3 first', 'fixed 5 years' in fb5.get('test-3', '') and all(v == 3 for v in m3b.values()), str(m3b))

# l8 annualised: byKey test-2 names "compound rather than average".
an = "def annualised(returns):\n    %s"
m8 = mutants_first_fail('l8-measuring-returns', 'screens', 10, {
    'arithmetic mean': an % 'return sum(returns) / len(returns)',
    'total return over T': an % "growth = 1.0\n    for r in returns:\n        growth *= 1 + r\n    return (growth - 1) / len(returns)",
    'mean of growth factors': an % 'return sum(1 + r for r in returns) / len(returns) - 1'})
print('   l8 annualised first failing test for averaging codings', m8)
fb8 = code_widget('l8-measuring-returns', 'screens', 10)[1]
check('code l8 annualised byKey test-1 ("not the 6.33% average"): every averaging coding fails test 1 first', 'average' in fb8.get('test-1', '') and all(v == 1 for v in m8.values()), str(m8))
m8r = mutants_first_fail('l8-measuring-returns', 'screens', 10, {
    'root 1/3': an % "growth = 1.0\n    for r in returns:\n        growth *= 1 + r\n    return growth ** (1 / 3) - 1",
    'root 1/3.0': an % "growth = 1.0\n    for r in returns:\n        growth *= 1 + r\n    return growth ** (1 / 3.0) - 1",
    'math.pow 1/3': "import math\n" + an % "growth = 1.0\n    for r in returns:\n        growth *= 1 + r\n    return math.pow(growth, 1 / 3) - 1"})
check('code l8 annualised byKey test-2 (root uses len(returns)): every fixed-root coding fails test 2 first', 'len(returns)' in fb8.get('test-2', '') and all(v == 2 for v in m8r.values()), str(m8r))
m8l = mutants_first_fail('l8-measuring-returns', 'screens', 10, {
    'mean log': "import math\n" + an % "return math.exp(sum(math.log(1 + r) for r in returns) / len(returns)) - 1",
    'mean log1p': "import math\n" + an % "return math.exp(sum(math.log1p(r) for r in returns) / len(returns)) - 1",
    'log loop': "import math\n" + an % "total = 0.0\n    for r in returns:\n        total += math.log(1 + r)\n    return math.exp(total / len(returns)) - 1"})
check('code l8 annualised byKey test-6 (math.log(0)): every mean-log-return coding first fails test 6', 'test-6' in fb8 and all(v == 6 for v in m8l.values()), str(m8l))
m8b = mutants_first_fail('l8-measuring-returns', 'screens', 10, {
    'no root': an % "growth = 1.0\n    for r in returns:\n        growth *= 1 + r\n    return growth - 1",
    'sum not product': an % "growth = 1.0\n    for r in returns:\n        growth += r\n    return growth ** (1 / len(returns)) - 1"})
check('code l8 annualised: no-root and sum-for-product programs fail a hidden test', all(v != 0 for v in m8b.values()), str(m8b))

# homework-1 irr and homework-2 ytm: reversed bisection must fail; ytm byKey test-1 names the direction.
w, _ = code_widget('homework-1', 'items', 5)
m = {'reversed': run_tests(w['solution'].replace('> 0', '< 0'), None, w['tests']), 'never moves hi': run_tests(w['solution'].replace('hi = mid', 'lo = mid'), None, w['tests'])}
check('code hw1 irr: reversed and one-sided bisections fail a hidden test', all(v != 0 for v in m.values()), str(m))
w, _ = code_widget('homework-2', 'items', 3)
my = {'reversed >': run_tests(w['solution'].replace('> price', '< price'), None, w['tests']),
      'reversed operands': run_tests(w['solution'].replace('bond_price(face, coupon, years, mid) > price', 'price > bond_price(face, coupon, years, mid)'), None, w['tests']),
      'swapped branches': run_tests(w['solution'].replace('            lo = mid\n        else:\n            hi = mid', '            hi = mid\n        else:\n            lo = mid'), None, w['tests'])}
check('code hw2 ytm byKey test-1 ("check the direction"): every reversed-direction coding fails test 1 first', all(v == 1 for v in my.values()), str(my))

# homework-3 margin_calls: obvious wrong programs must fail some test.
base = L['homework-3']['items'][4]['widget']['solution']
mm = {'<= maintenance': base.replace('balance < maintenance * n', 'balance <= maintenance * n'),
      'top up to maintenance': base.replace('call = initial * n - balance', 'call = maintenance * n - balance'),
      'call not added back': base.replace('        balance += call\n', ''),
      'short treated as long': base.replace('side = 1 if contracts > 0 else -1', 'side = 1'),
      'one contract margin': base.replace('balance = initial * n', 'balance = initial').replace('initial * n - balance', 'initial - balance').replace('maintenance * n', 'maintenance'),
      'settle once at the end': "def margin_calls(prices, contracts, point_value, initial, maintenance):\n    n = abs(contracts)\n    bal = initial * n + contracts * point_value * (prices[-1] - prices[0])\n    c = initial * n - bal if bal < maintenance * n else 0\n    return [0] * (len(prices) - 2) + ([c] if len(prices) > 1 else [])"}
res = {k: run_tests(v, None, L['homework-3']['items'][4]['widget']['tests']) for k, v in mm.items()}
check('code hw3 margin_calls: six wrong programs each fail a hidden test', all(v != 0 for v in res.values()), str(res))

print()
print('%d failing check(s): %s' % (len(FAILS), '; '.join(FAILS)) if FAILS else 'all checks pass')
sys.exit(1 if FAILS else 0)
