"""pairs-rep level 2, concept audit round 2: exact and Monte Carlo checks of the claims in the ledger
(docs/reports/audit-pairs-rep-1-3-r2-ledger.md). Run from the repo root with `python3 -I`. Exit 0 when the
content is correct; a check the content fails is marked EXPECTED_FAIL, keeps running, and fails the script at
the end, with the corrected assert in a comment beside it. Messages name the ledger row by (file, path, check)."""
import json
import os
import time

import numpy as np

T0 = time.time()
FAILS = []


def expected_fail(cond, msg):
    if not cond:
        FAILS.append(msg); print('FAIL', msg)


ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'pairs-rep')
FILES = ['l6-two-standard-deviations', 'l7-closing', 'l8-committed-capital', 'l9-bid-ask-bounce', 'l10-matching-results', 'review-2', 'homework-2']
DOC = {f: json.load(open(os.path.join(ROOT, f + '.json'))) for f in FILES}

ns = {}
exec(DOC['l10-matching-results']['screens'][7]['widget']['prelude'], ns)   # generator, normalise, ssd_matrix, top_pairs, trade_pair, cycle_return, run
pairs_panel, normalise, top_pairs, trade_pair, cycle_return, run = (ns[k] for k in ('pairs_panel', 'normalise', 'top_pairs', 'trade_pair', 'cycle_return', 'run'))
CLOSE, MID, IND, BROKEN = ns['close'], ns['mid'], ns['ind'], ns['broken']


def trips(form, trade, i, j, wait=0, open_at=2.0):
    """Every round trip as (open, exit, converged, payoff), the course's loop."""
    sd = float(np.std(form[:, i] - form[:, j])); a, b = trade[:, i].tolist(), trade[:, j].tolist(); n = len(a); out = []; t = 0
    while t < n:
        s = a[t] - b[t]
        if sd > 0 and abs(s) > open_at * sd and t + wait < n - 1:
            side = 1 if s > 0 else -1; to = t + wait
            tc = next((u for u in range(t + 1, n) if (a[u] - b[u]) * side <= 0), None)
            tx = n - 1 if tc is None else min(tc + wait, n - 1)
            out.append((to, tx, tc is not None, side * ((b[tx] - b[to]) / b[to] - (a[tx] - a[to]) / a[to]))); t = tx + 1; continue
        t += 1
    return out


# ---- 1. the full 127-cycle run, naive and Newey-West t (l8 screens[4], review-2 items[5]) [nw]
import statsmodels.api as sm  # noqa: E402

starts = range(0, CLOSE.shape[0] - 378 + 1, 21)
R0 = np.array([cycle_return(CLOSE, s, 20, 0)[0] for s in starts]) / 6
R1 = np.array([cycle_return(CLOSE, s, 20, 1)[0] for s in starts]) / 6
assert len(R0) == 127 and abs(R0.mean() - 0.0100) < 5e-4 and abs(R1.mean() - 0.0075) < 5e-4, 'l8 screens[4].prose [nw] 127 monthly figures, mean 1.00% and 0.75%'
X = np.ones((127, 1))
t_naive0 = sm.OLS(R0, X).fit().tvalues[0]; t_nw0 = sm.OLS(R0, X).fit(cov_type='HAC', cov_kwds={'maxlags': 5}).tvalues[0]
t_naive1 = sm.OLS(R1, X).fit().tvalues[0]; t_nw1 = sm.OLS(R1, X).fit(cov_type='HAC', cov_kwds={'maxlags': 5}).tvalues[0]
print(f'[nw] naive t {t_naive0:.2f} NW(5) t {t_nw0:.2f}; with the wait {t_naive1:.2f} and {t_nw1:.2f}')
assert abs(t_naive0 - 13.55) < 0.05 and abs(t_nw0 - 8.09) < 0.05, 'l8 screens[4] [nw] 13.55 and 8.09'
assert abs(t_naive1 - 11.09) < 0.05 and abs(t_nw1 - 6.91) < 0.05, 'l8 screens[4].explain [nw] 11.09 and 6.91 with the wait'
ac = [np.corrcoef(R0[:-k], R0[k:])[0, 1] for k in range(1, 7)]
print(f'[nw] autocorrelations of the 127 cycle returns, lags 1 to 6: {np.round(ac, 2)}')
assert all(r > 0 for r in ac[:5]), 'l8 screens[4].prose [nw] overlapping cycles are positively correlated up to lag 5'
assert np.mean(R0) == np.mean(R0), 'l8 screens[4].options[1].why [nw] the mean does not change'

# ---- 2. Monte Carlo: overlap inflates the naive t; NW(5) is the right lag (l8 screens[4], summary.ideas[2], quiz[1]) [nw-mc]
rng = np.random.default_rng(2006); rej_naive = rej_nw = 0; reps = 1500
for _ in range(reps):
    m = rng.standard_normal(132)                       # iid monthly returns, mean 0
    y = np.array([m[k:k + 6].sum() for k in range(127)])  # 127 overlapping six-month sums, one a month
    f = sm.OLS(y, np.ones((127, 1)))
    rej_naive += abs(f.fit().tvalues[0]) > 1.96
    rej_nw += abs(f.fit(cov_type='HAC', cov_kwds={'maxlags': 5}).tvalues[0]) > 1.96
print(f'[nw-mc] size at nominal 5% under H0 with 6-month overlap, {reps} reps: naive {rej_naive / reps:.3f}, NW(5) {rej_nw / reps:.3f}')
assert rej_naive / reps > 0.25 and rej_nw / reps < 0.15, 'l8 summary.ideas[2] [nw-mc] the naive t over-rejects badly under overlap; NW(5) is far closer to 5%'

# ---- 3. the bounce and the one-day wait on fresh panels (l9 screens[2], screens[3]; homework-2 items[3]) [bounce]
same_c, same_m, wait_c, wait_m = [], [], [], []
for seed in range(60):
    c_, m_, i_, b_ = pairs_panel(seed=700 + seed, days=378, break_frac=0.0)
    Pc, Pm = normalise(c_), normalise(m_)
    pairs = top_pairs(Pc[:252], 20)                     # the same pairs for all four runs
    for i, j in pairs:
        same_c.append(trade_pair(Pc[:252], Pc[252:], i, j, 0)[0]); same_m.append(trade_pair(Pm[:252], Pm[252:], i, j, 0)[0])
        wait_c.append(trade_pair(Pc[:252], Pc[252:], i, j, 1)[0]); wait_m.append(trade_pair(Pm[:252], Pm[252:], i, j, 1)[0])
same_c, same_m, wait_c, wait_m = map(np.array, (same_c, same_m, wait_c, wait_m))
d_same = same_c - same_m; d_wait = wait_c - wait_m
se = lambda x: x.std(ddof=1) / np.sqrt(len(x))
print(f'[bounce] 1200 top-20 pairs on 60 fresh panels, payoff per cycle: same day closes {same_c.mean():.4f} mids {same_m.mean():.4f} '
      f'(gap {d_same.mean():+.4f}, se {se(d_same):.4f}); with the wait closes {wait_c.mean():.4f} mids {wait_m.mean():.4f} (gap {d_wait.mean():+.4f}, se {se(d_wait):.4f})')
assert d_same.mean() > 3 * se(d_same), 'l9 screens[1].explain [bounce] a same-day trade on closes books the bounce'
assert abs(d_wait.mean()) < 3 * se(d_wait) and d_wait.mean() < d_same.mean() / 3, 'l9 screens[3].options[0] [bounce] with the wait the bounce gain is gone'
assert wait_m.mean() < same_m.mean(), 'l9 screens[3].explain [bounce] the wait also gives up a day of convergence (mids)'

# ---- 4. forced closes: who loses (l7 screens[4].explain) [forced]
n_trips = n_forced = 0; forced_loss_chance = forced_loss_all = 0
for s in starts:
    Pn = normalise(CLOSE[s:s + 378]); form, trade = Pn[:252], Pn[252:]
    for i, j in top_pairs(form, 20):
        planted_live = (j == i + 1 and i % 2 == 0 and i < 40) and not (BROKEN[i // 2] and s + 252 + 125 >= 1512)
        for to, tx, conv, pay in trips(form, trade, i, j):
            n_trips += 1
            if not conv:
                n_forced += 1
                if pay < 0:
                    forced_loss_all += 1; forced_loss_chance += not planted_live
print(f'[forced] {n_forced} of {n_trips} top-20 trades end in a forced close ({n_forced / n_trips:.2f}); of the {forced_loss_all} losing ones, '
      f'{forced_loss_chance} come from chance or broken pairs ({forced_loss_chance / forced_loss_all:.2f})')
assert abs(n_forced / n_trips - 0.35) < 0.02, 'l7 screens[4].explain [forced] 35% of trades end in a forced close'
assert forced_loss_chance / forced_loss_all > 0.5, 'l7 screens[4].explain [forced] most forced-close losses come from pairs that are not live planted pairs'

# ---- 5. re-basing at the trading start (l2 quiz[1], l10 screens[3], homework-2 items[6]) [rebase]
P = normalise(CLOSE[:378]); form, trade = P[:252], P[252:]
trade_rb = trade / trade[0]                                   # re-based: every trading path starts at 1 on day 0
t_a = trips(form, trade, 2, 3); t_b = trips(form, trade_rb, 2, 3)
print(f'[rebase] pair (2,3): {len(t_a)} trips carried through, {len(t_b)} trips re-based; opens {[t[0] for t in t_a]} against {[t[0] for t in t_b]}')
# for a fixed trade the payoff is base-invariant (each leg's return is p_out/p_in)
to, tx = t_a[0][0], t_a[0][1]
pay_a = (trade[tx, 2] / trade[to, 2] - 1) - (trade[tx, 3] / trade[to, 3] - 1)
pay_b = (trade_rb[tx, 2] / trade_rb[to, 2] - 1) - (trade_rb[tx, 3] / trade_rb[to, 3] - 1)
assert abs(pay_a - pay_b) < 1e-12, 'homework-2 items[6].options[1].why [rebase] the base cancels in each leg\'s return'
assert [t[0] for t in t_a] != [t[0] for t in t_b], 'homework-2 items[6].options[1].why [rebase] re-basing changes which trades open'
assert abs(trade_rb[0, 2] - trade_rb[0, 3]) == 0.0, 'l2 quiz[1].options[1].why [rebase] re-basing resets the day-0 gap to 0'
# l2 quiz[1] grades re-basing as "what goes wrong", while l10 screens[3] lists "normalise once and carry through" as the
# course's own departure from the paper (Krauss 2017 and Rad, Low and Faff 2016 describe GGR as re-normalising at the
# trading start). The two screens cannot both be right about the paper. EXPECTED_FAIL (finding): the course states both.
q = DOC['l6-two-standard-deviations']  # placeholder to keep the namespace tidy
l2 = json.load(open(os.path.join(ROOT, 'l2-normalised-paths.json')))
l10 = DOC['l10-matching-results']
rebase_is_error = l2['quiz'][1]['question'].startswith('What goes wrong')
norm_is_gap = l10['screens'][3]['widget']['options'][1].get('correct', False)
# Fix pass: l2 quiz[1] now states that the paper re-bases (Krauss 2015 FAU discussion paper 09/2015, Siy-Yap 2009,
# Rubesam 2021, Rad, Low and Faff 2016) and keys "which trades open" as what re-basing changes.
# Second computation (fix pass): over all 127 cycles, top 20, re-basing changes the payoff of 2,414 of 2,540 pair-cycles
# (the trades differ) while a fixed trade pays the same on either base; the committed month moves 1.00% to 0.99%.
q2 = l2['quiz'][1]; key = next(o for o in q2['widget']['options'] if o.get('correct'))
n_diff = n_all = 0
for s0 in range(0, CLOSE.shape[0] - 378 + 1, 21):
    Pc = normalise(CLOSE[s0:s0 + 378]); fc, tc_ = Pc[:252], Pc[252:]
    for i, j in top_pairs(fc, 20):
        n_all += 1; n_diff += abs(trade_pair(fc, tc_, i, j)[0] - trade_pair(fc, tc_ / tc_[0], i, j)[0]) > 1e-12
print(f'[rebase] second count: re-basing changes the payoff of {n_diff} of {n_all} top-20 pair-cycles')
assert norm_is_gap and not rebase_is_error and 're-normalises' in q2['prose'] and key['text'].startswith('Which trades open') \
    and n_diff > n_all / 2, 'l2 quiz[1] / l10 screens[3] [rebase] consistent about the paper (corrected claim, fix pass)'

# ---- 6. which paper cell is "up to 11%" (l10 screens[0], quiz[0]) [fair-cell]
paper = {'top20_employed_wait': 0.00895, 'top20_committed_wait': 0.00520, 'top5_employed_wait': 0.00745, 'top5_committed_wait': 0.00463}  # Table 1 transcription
ann = {k: (1 + v) ** 12 - 1 for k, v in paper.items()}
print('[fair-cell] paper cells annualised: ' + ', '.join(f'{k} {v:.1%}' for k, v in ann.items()))
closest_cell = min(ann, key=lambda k: abs(ann[k] - 0.11))
assert closest_cell == 'top20_employed_wait', 'l10 screens[0] [fair-cell] the paper\'s 11% is the fully invested (employed) top-20 one-day-wait cell'
ours_committed_wait = R1.mean(); ours_employed_wait = np.mean([cycle_return(CLOSE, s, 20, 1)[1] for s in starts]) / 6
print(f'[fair-cell] course: committed wait {(1 + ours_committed_wait) ** 12 - 1:.1%}, employed wait {(1 + ours_employed_wait) ** 12 - 1:.1%}')
# Fix pass: l10 screens[0] and quiz[0] now key employed capital with the wait as the like-for-like cell.
# Second computation (fix pass): the paper's top-20 employed one-day-wait month, 0.895% (Table 1 as transcribed in the
# Skiena lecture 23 slides), compounds to 11.3% and is 10.7% simple; the committed one, 0.520%, gives 6.4%. Ours: 0.84% a
# month employed with the wait compounds to 10.6%, committed 0.75% to 9.4%.
assert abs(1.00895 ** 12 - 1 - 0.113) < 5e-4 and abs(12 * 0.00895 - 0.107) < 5e-4 and abs(1.0052 ** 12 - 1 - 0.064) < 5e-4
assert round(ours_employed_wait * 100, 2) == 0.84 and round(((1 + ours_employed_wait) ** 12 - 1) * 100, 1) == 10.6
l10s0 = DOC['l10-matching-results']['screens'][0]; l10q0 = DOC['l10-matching-results']['quiz'][0]
k0 = next(o for o in l10s0['widget']['options'] if o.get('correct')); kq = next(o for o in l10q0['widget']['options'] if o.get('correct'))
assert all('employed' in k['text'] and 'wait' in k['text'] for k in (k0, kq)) and '10.6%' in l10s0['explain']['text'], \
    'l10 screens[0], quiz[0] [fair-cell] the like-for-like cell is employed with the wait (corrected claim, fix pass)'

# ---- 7. costs and k/n identities (l9 screens[4] to [6], review-2 items[6]; l8 screens[6]) [cost] [kn]
assert abs(4 * 0.001 * 1.6886 - 0.00675) < 5e-6 and abs(0.0452 / (4 * 1.6886) - 0.00669) < 5e-6, 'l9 screens[4], screens[5] [cost]'
assert abs(0.036 / (4 * 1.5) - 0.006) < 1e-12 and abs(0.06 / (4 * 2.5) - 0.006) < 1e-12, 'review-2 items[6], l9 quiz[2] [cost]'
c21 = cycle_return(CLOSE, 21, 20, 0)
assert c21[2] == 20 and abs(c21[0] - c21[1]) < 1e-12, 'l8 screens[6] [kn] all 20 open: committed equals employed'
assert sum(1 for s in starts if cycle_return(CLOSE, s, 20, 0)[2] == 20) == 46, 'l8 screens[6].explain [kn] 46 of 127 cycles'

# ---- 8. every code widget of the level: solution passes, starter fails [code]


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

print(f'pairs-rep L2 concepts r2: done in {time.time() - T0:.0f}s, {len(FAILS)} expected failure(s)')
assert not FAILS, 'content findings: ' + '; '.join(FAILS)
