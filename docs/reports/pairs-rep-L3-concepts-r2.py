"""pairs-rep level 3, concept audit round 2: exact and Monte Carlo checks of the claims in the ledger
(docs/reports/audit-pairs-rep-1-3-r2-ledger.md). Run from the repo root with `python3 -I`. Exit 0 when the
content is correct; a check the content fails is marked EXPECTED_FAIL, keeps running, and fails the script at
the end, with the corrected assert in a comment beside it. Messages name the ledger row by (file, path, check)."""
import json
import os
import time
import warnings

import numpy as np

warnings.filterwarnings('ignore')
T0 = time.time()
FAILS = []


def expected_fail(cond, msg):
    if not cond:
        FAILS.append(msg); print('FAIL', msg)


ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'pairs-rep')
FILES = ['l11-why-profits-fell', 'l12-cointegration-selection', 'l13-just-a-factor', 'l14-out-of-sample', 'l15-pairs-note', 'review-3', 'homework-3']
DOC = {f: json.load(open(os.path.join(ROOT, f + '.json'))) for f in FILES}

ns = {}
exec(DOC['homework-3']['items'][0]['widget']['prelude'], ns)   # generator and every helper up to trade_coint and eg_decision
pairs_panel, normalise, top_pairs, trade_pair, trade_trips, cycle_return, run, eg_decision, hedge_ratio, trade_coint = (
    ns[k] for k in ('pairs_panel', 'normalise', 'top_pairs', 'trade_pair', 'trade_trips', 'cycle_return', 'run', 'eg_decision', 'hedge_ratio', 'trade_coint'))
CLOSE, MID, IND, BROKEN = ns['close'], ns['mid'], ns['ind'], ns['broken']
from statsmodels.tsa.stattools import coint  # noqa: E402

rng = np.random.default_rng(2006)
PHI = 0.5 ** (1 / 8)


def ou(n, phi, sd, r):
    e = sd * r.standard_normal(n); s = np.zeros(n)
    for t in range(1, n):
        s[t] = phi * s[t - 1] + e[t]
    return s


def bounce(n, r, half=0.005):
    return np.where(r.random(n) < 0.5, 1 + half, 1 - half)


# ---- 1. size of the Engle-Granger test on one year with a bounce (l12 screens[4].explain) [eg-size]
reps = 600; rej_b = rej_nb = 0
for _ in range(reps):
    m = np.cumsum(0.010 * rng.standard_normal(252))
    x = np.exp(m + np.cumsum(0.015 * rng.standard_normal(252))); y = np.exp(m + np.cumsum(0.015 * rng.standard_normal(252)))
    rej_nb += coint(np.log(y), np.log(x))[1] < 0.05
    rej_b += coint(np.log(y * bounce(252, rng)), np.log(x * bounce(252, rng)))[1] < 0.05
print(f'[eg-size] independent random walks, n = 252, {reps} reps: rejection at 5% without bounce {rej_nb / reps:.3f}, with bounce {rej_b / reps:.3f}')
assert 0.04 < rej_b / reps < 0.13, 'l12 screens[4].explain [eg-size] false-alarm rate "about 7%" on one year with a bounce'

# ---- 2. power on a planted pair (l12 screens[1].explain; review-3 items[5].options[2].why) [eg-power]
reps = 400; rej = 0
for _ in range(reps):
    m = np.cumsum(0.010 * rng.standard_normal(252)); c = np.cumsum(0.015 * rng.standard_normal(252))
    x = np.exp(m + c + ou(252, PHI, 0.008, rng)) * bounce(252, rng); y = np.exp(m + c + ou(252, PHI, 0.008, rng)) * bounce(252, rng)
    rej += coint(np.log(y), np.log(x))[1] < 0.05
print(f'[eg-power] planted pairs (half-life 8, bounce), n = 252, {reps} reps: rejection at 5% {rej / reps:.3f}')
assert 0.45 < rej / reps < 0.97, 'l12 screens[1].explain [eg-power] a real relationship can fail the test on one year; most planted pairs pass'

# ---- 3. selection on closeness inflates the pass rate (l12 screens[8].explain, screens[9].explain; review-3 items[5]) [eg-select]
F0 = normalise(CLOSE[:252]); L0 = np.log(F0)
cand = top_pairs(F0, 50)
chance = [(i, j) for i, j in cand if not (j == i + 1 and i % 2 == 0 and i < 40)]
passes = sum(1 for i, j in chance if eg_decision(L0[:, i], L0[:, j])[1] < 0.05)
print(f'[eg-select] course panel, start 0: {passes} of the {len(chance)} chance pairs among the 50 closest pass at 5%')
assert len(chance) == 30 and passes == 18, 'l12 screens[8].explain [eg-select] 18 of 30'
fresh = []
for seed in range(3):
    c_, m_, i_, b_ = pairs_panel(seed=900 + seed, days=252, break_frac=0.0)
    F = normalise(c_); L = np.log(F); cd = top_pairs(F, 50)
    ch = [(i, j) for i, j in cd if not (j == i + 1 and i % 2 == 0 and i < 40)]
    fresh.append(sum(1 for i, j in ch if eg_decision(L[:, i], L[:, j])[1] < 0.05) / max(1, len(ch)))
print(f'[eg-select] fresh panels, pass rate of chance pairs among the 50 closest: {np.round(fresh, 2)}')
assert min(fresh) > 0.2, 'review-3 items[5].options[0] [eg-select] shortlisting on closeness makes chance pairs look stationary'

# ---- 4. scaling a price leaves the p-value unchanged (l12 screens[7].explain) [eg-scale]
p1 = coint(np.log(F0[:, 2]), np.log(F0[:, 3]))[1]; p2 = coint(np.log(5 * F0[:, 2]), np.log(0.3 * F0[:, 3]))[1]
assert abs(p1 - p2) < 1e-10, 'l12 screens[7].explain [eg-scale] the intercept absorbs a log scale'

# ---- 5. a hedge ratio of 2 and of 0.5 (l12 screens[6], quiz[1]; review-3 items[4]) [hedge-2]
A = F0[:, 2]; u = ou(252, PHI, 0.008, rng)
L2 = np.exp(2 * np.log(A) + u); B = np.exp(0.5 * np.log(A) + u)
assert abs(hedge_ratio(np.log(L2), np.log(A))[0] - 2) < 0.05 and abs(hedge_ratio(np.log(B), np.log(A))[0] - 0.5) < 0.05, 'l12 screens[6], quiz[1] [hedge-2] slopes 2 and 0.5'
assert coint(np.log(L2), np.log(A))[1] < 0.05, 'l12 screens[6] [hedge-2] Engle-Granger finds the pair'
ssd_L = ((normalise(L2) - normalise(A)) ** 2).sum(); ssd_B = ((normalise(B) - normalise(A)) ** 2).sum()
G = F0.T @ F0; d = np.diag(G); D = d[:, None] + d[None, :] - 2 * G; iu, ju = np.triu_indices(100, 1); cut20 = np.sort(D[iu, ju])[19]
print(f'[hedge-2] on share 2\'s first year: SSD of the hedge-2 pair {ssd_L:.2f}, of the hedge-0.5 pair {ssd_B:.2f}, 20th closest overall {cut20:.2f}')
assert ssd_L > cut20, 'l12 screens[6].explain, review-3 items[4] [hedge-2] a hedge of 2 is outside the distance top 20 here'
# Does a hedge far from 1 put a pair outside the top 20 "in any year" (review-3 items[4].options[1].why) and do halved moves
# "make them drift apart" (l12 quiz[1].options[1].why)? In normalised-price space a hedge b shows up as p^b against p, a gap
# that only grows as p leaves 1. Monte Carlo over the 100 shares' first-year paths with fresh stationary gaps:
inside2 = inside05 = 0
for col in range(100):
    Ap = F0[:, col]
    for _ in range(3):
        uu = ou(252, PHI, 0.008, rng)
        inside2 += ((normalise(np.exp(2 * np.log(Ap) + uu)) - Ap) ** 2).sum() < cut20
        inside05 += ((normalise(np.exp(0.5 * np.log(Ap) + uu)) - Ap) ** 2).sum() < cut20
print(f'[hedge-2] share of constructed pairs inside the distance top-20 cut: hedge 2 {inside2 / 300:.2f}, hedge 0.5 {inside05 / 300:.2f}')
# EXPECTED_FAIL (finding): a hedge of 0.5 often leaves the pair inside the top 20, so distance can select it; the keyed
# "why" lines state the opposite as a rule.
expected_fail(inside05 / 300 < 0.1, 'EXPECTED_FAIL l12 quiz[1].options[1].why [hedge-2] "halved moves make them drift apart": a hedge of 0.5 keeps the pair inside the distance top 20 in a large share of years')
expected_fail(inside2 / 300 < 0.1, 'EXPECTED_FAIL review-3 items[4].options[1].why [hedge-2] "in any year": a hedge of 2 can sit inside the distance top 20 in a quiet year')
# corrected asserts, ready to enable once the lines say distance misses such a pair only when the path moves far from 1:
# assert inside05 / 300 > 0.1, 'l12 quiz[1].options[1].why [hedge-2] distance can select a 0.5-hedge pair in a quiet year'
# assert 0 <= inside2 / 300, 'review-3 items[4].options[1].why [hedge-2] stated with its condition'

# ---- 6. the market cancels in a £1 long £1 short pair (l13 screens[2]) [beta]
rA, rB, mkt = 0.10, 0.04, 0.15
with_m = ((1 + mkt) * (1 + rA) - 1) - ((1 + mkt) * (1 + rB) - 1); without = rA - rB
assert abs(with_m - (1 + mkt) * without) < 1e-12 and abs(with_m - without) <= abs(mkt * without), 'l13 screens[2].options[0] [beta] a common market move cancels up to second order'
M = ns['market_level']() if 'market_level' in ns else None
Y22 = [r for _, r in run(CLOSE, 20, 0, 126)]
rng_m = np.random.default_rng(2006); Mlev = np.exp(np.cumsum(0.0003 + 0.010 * rng_m.standard_normal(3024)))
X22 = [Mlev[s + 377] / Mlev[s + 252] - 1 for s in range(0, 2647, 126)]
import statsmodels.api as sm  # noqa: E402

fit = sm.OLS(np.array(Y22), sm.add_constant(np.array(X22))).fit()
print(f'[beta] 22 cycles: alpha {fit.params[0]:.4f} (t {fit.tvalues[0]:.2f}), beta {fit.params[1]:.4f} (t {fit.tvalues[1]:.2f}), R^2 {fit.rsquared:.3f}')
assert abs(fit.params[1] - 0.0529) < 5e-4 and abs(fit.params[0] - 0.0623) < 5e-4 and abs(fit.tvalues[0] - 7.11) < 0.02, 'l13 screens[1].explain [beta]'
assert abs(fit.rsquared - 0.02) < 0.01, 'l13 screens[1].explain [beta] the market explains about 2% of the variation'
Yall = [r for _, r in run(CLOSE, 20, 0, 21)]; Xall = [Mlev[s + 377] / Mlev[s + 252] - 1 for s in range(0, 2647, 21)]
t_all = sm.OLS(np.array(Yall), sm.add_constant(np.array(Xall))).fit().tvalues[0]
assert abs(t_all - 13.48) < 0.05, 'l13 screens[4].prose [beta] plain OLS on 127 overlapping cycles gives 13.48'

# ---- 7. convergence share tells crowding from broken pairs (l11 screens[5], screens[9]; review-3 items[1]) [conv-mc]


def conv_share(spread_fn, reps=400):
    conv = opened = 0
    for _ in range(reps):
        s = spread_fn(); sd = s[:252].std(); x = s[252:]; n = len(x); t = 0
        while t < n:
            if abs(x[t]) > 2 * sd and t < n - 1:
                side = 1 if x[t] > 0 else -1
                tc = next((u for u in range(t + 1, n) if x[u] * side <= 0), None)
                opened += 1; conv += tc is not None; t = (n - 1 if tc is None else tc) + 1; continue
            t += 1
    return conv / opened


base = conv_share(lambda: ou(378, PHI, 0.008, rng))
crowd = conv_share(lambda: np.concatenate([ou(252, PHI, 0.008, rng), ou(127, 0.5 ** (1 / 4), 0.008 * np.sqrt((1 - 0.5 ** 0.5) / (1 - PHI ** 2)), rng)[1:]]))
broken = conv_share(lambda: (lambda s: np.concatenate([s[:252], s[251] + np.cumsum(0.008 * rng.standard_normal(126))]))(ou(378, PHI, 0.008, rng)))
print(f'[conv-mc] crossing share: baseline {base:.2f}, crowding (half-life 4 in trading) {crowd:.2f}, broken (random walk in trading) {broken:.2f}')
assert crowd >= base - 0.03 and broken < base - 0.2, 'l11 screens[5].options[0] [conv-mc] faster reversion keeps the crossing share; a break cuts it'
se_bin = np.sqrt(0.65 * 0.35 / 2000)
assert (0.77 - 0.54) > 6 * se_bin, 'l11 quiz[1].options[2].why [conv-mc] 77% to 54% over 2,000 trades is far outside chance'

# ---- 8. the best of many in-sample cells is partly the luckiest (l14 screens[2], screens[3], screens[5]) [best-of]
reps = 4000; ratio = {}
for cells in (2, 12):
    r_ = []
    for _ in range(reps):
        true = 0.01 + 0.002 * rng.standard_normal(cells)
        ins = true + 0.004 * rng.standard_normal(cells); oos = true + 0.004 * rng.standard_normal(cells)
        b = int(np.argmax(ins)); r_.append(oos[b] / ins[b])
    ratio[cells] = np.mean(r_)
print(f'[best-of] mean out/in of the best in-sample cell, no true decline: 2 cells {ratio[2]:.2f}, 12 cells {ratio[12]:.2f}')
assert ratio[12] < ratio[2] < 1.0, 'l14 screens[3].explain, screens[5].options[2].why [best-of] the best of more cells loses more out of sample'

# ---- 9. selection against trading rule: the cointegration arm changes both (l12 screens[2].explain, summary.ideas[1]; homework-3 items[0]) [confound]
P = normalise(CLOSE[:378]); form, trade = P[:252], P[252:]
cand = top_pairs(form, 50); Lf = np.log(form)
p = [eg_decision(Lf[:, i], Lf[:, j])[1] for i, j in cand]
eg = [cand[o] for o in np.argsort(p, kind='stable')[:20]]; dist = cand[:20]
r_dist = sum(trade_pair(form, trade, i, j)[0] for i, j in dist) / 20
r_eg_coint = sum(trade_coint(form, trade, i, j)[0] for i, j in eg) / 20
r_eg_pair = sum(trade_pair(form, trade, i, j)[0] for i, j in eg) / 20
r_dist_coint = sum(trade_coint(form, trade, i, j)[0] for i, j in dist) / 20
print(f'[confound] start 0, k = 20: distance picks {r_dist:.4f} (trade_pair) {r_dist_coint:.4f} (trade_coint); '
      f'EG picks {r_eg_pair:.4f} (trade_pair) {r_eg_coint:.4f} (trade_coint)')
assert abs(r_dist - 0.1424) < 5e-4 and abs(r_eg_coint - 0.1283) < 5e-4, 'homework-3 items[0] [confound] the stated cells'
# the stated gap (0.1424 against 0.1283) is attributed to selection; holding the trading rule fixed changes the gap materially
gap_stated = r_dist - r_eg_coint; gap_selection_only = r_dist - r_eg_pair
print(f'[confound] gap as stated {gap_stated:+.4f}; gap with the trading rule held at trade_pair {gap_selection_only:+.4f}; '
      f'trading-rule effect on the same EG picks {r_eg_coint - r_eg_pair:+.4f}')
# EXPECTED_FAIL (finding): l12 screens[2].explain reports the two-rule difference as "cointegration selection" against "distance"
expected_fail(abs(r_eg_coint - r_eg_pair) < 0.25 * abs(gap_stated),
              'EXPECTED_FAIL l12 screens[2].explain [confound] the trading rule moves the EG arm by more than a quarter of the gap attributed to selection')
# corrected assert, ready to enable once the sentence attributes the gap to selection and trading rule together (or trades both arms with trade_pair):
# assert True, 'l12 screens[2].explain [confound] attribution stated'

# ---- 10. pooled shares and exposures (review-3 items[2], items[7]; l13 screens[7]; homework-3 items[3], items[4]) [exact]
assert abs(51 / 90 - 0.5667) < 5e-5 and abs((26 / 40 + 25 / 50) / 2 - 0.575) < 1e-12, 'review-3 items[2] [exact] pooled against averaged'
assert abs((3 * 0.1045 + 17 * 0.0237) / 20 - 0.0358) < 5e-5, 'homework-3 items[3] [exact]'
assert 10 * (10 * 9 // 2) * 0.05 == 22.5 and 4950 / 450 == 11, 'homework-3 items[4] [exact]'
assert 1 - 0.6 == 0.4 and abs(1 - 1.25 + 0.25) < 1e-12, 'l13 screens[7], review-3 items[7] [exact]'
assert 5000 * 4999 // 2 == 12497500 and round(12497500 / 4950) == 2525, 'l15 screens[4].prose [exact]'
starts126 = list(range(0, 2647, 126))
assert sum(1 for s in starts126 if s + 378 <= 1512) == 10 and sum(1 for s in starts126 if s + 252 >= 1512) == 12, 'l14 screens[0] [exact]'
starts21 = list(range(0, 2647, 21))
assert sum(1 for s in starts21 if s + 378 <= 1512) == 55 and sum(1 for s in starts21 if s + 252 >= 1512) == 67, 'l11 screens[1].prose [exact] 55 before, 67 after'

# ---- 11. every code widget of the level: solution passes, starter fails [code]


def close_enough(got, exp, rel, ab):
    if isinstance(exp, dict):
        return isinstance(got, dict) and got.keys() == exp.keys() and all(close_enough(got[k], exp[k], rel, ab) for k in exp)
    if isinstance(exp, (list, tuple)):
        got = list(got.tolist()) if hasattr(got, 'tolist') else list(got)
        return len(got) == len(exp) and all(close_enough(g, e, rel, ab) for g, e in zip(got, exp))
    if isinstance(exp, (int, float)) and not isinstance(exp, bool):
        return abs(float(got) - float(exp)) <= ab + rel * abs(float(exp))
    return got == exp


def run_tests(w, src):
    ns_ = {'__learner_source__': src}
    exec(w.get('prelude', ''), ns_); exec(src, ns_)
    fails = 0
    for t in w['tests']:
        try:
            if t.get('setup'):
                exec(t['setup'], ns_)
            if t.get('compare') == 'raises':
                try:
                    eval(t['call'], ns_); ok = False
                except Exception as e:
                    ok = type(e).__name__ == t['expect']
            else:
                got = eval(t['call'], ns_); exp = eval(t['expect'], ns_)
                if t.get('compare', 'equal') == 'isclose':
                    tol = t.get('tol', {}); ok = close_enough(got, exp, tol.get('rel', 0 if 'abs' in tol else 1e-9), tol.get('abs', 0 if 'rel' in tol else 1e-12))
                else:
                    ok = (got.tolist() if hasattr(got, 'tolist') else got) == exp
        except Exception:
            ok = False
        fails += not ok
    return fails


def widgets(node, path=''):
    if isinstance(node, dict):
        if node.get('kind') == 'code' and 'tests' in node:
            yield path, node
        for k, v in node.items():
            yield from widgets(v, f'{path}.{k}')
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from widgets(v, f'{path}[{i}]')


n_code = 0
for fid in FILES:
    for path, w in widgets(DOC[fid]):
        n_code += 1
        assert run_tests(w, w['solution']) == 0, f'{fid}{path} [code] solution passes its tests'
        try:
            st = run_tests(w, w['starter'])
        except Exception:
            st = len(w['tests'])
        assert st > 0, f'{fid}{path} [code] starter fails at least one test'
print(f'[code] {n_code} code widgets: solution passes, starter fails')

print(f'pairs-rep L3 concepts r2: done in {time.time() - T0:.0f}s, {len(FAILS)} expected failure(s)')
assert not FAILS, 'content findings: ' + '; '.join(FAILS)
