"""pairs-rep level 1, concept audit round 2: exact and Monte Carlo checks of the claims in the ledger
(docs/reports/audit-pairs-rep-1-3-r2-ledger.md). Run from the repo root with `python3 -I`. Exit 0 when the
content is correct; a check that fails because the content is wrong is marked EXPECTED_FAIL and has the
corrected assert in a comment beside it. Each assert message names its ledger row by (file, path, check)."""
import json
import os
import sys
import time

import numpy as np

T0 = time.time()
FAILS = []


def expected_fail(cond, msg):
    """A check the content fails: record it, keep running, and fail the script at the end."""
    if not cond:
        FAILS.append(msg); print('FAIL', msg)


ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'pairs-rep')
FILES = ['l1-ggr-design', 'l2-normalised-paths', 'l3-closest-pairs', 'l4-main-results', 'l5-plan', 'review-1', 'homework-1']
DOC = {f: json.load(open(os.path.join(ROOT, f + '.json'))) for f in FILES}

# ---- the course's own generator and helpers, taken from the content so the check runs what learners run
ns = {}
exec(DOC['l5-plan']['screens'][6]['widget']['prelude'], ns)        # pairs_panel, normalise, trade_pair, close, mid
exec(DOC['l2-normalised-paths']['screens'][5]['widget']['solution'], ns)  # ssd_matrix
exec(DOC['l3-closest-pairs']['screens'][3]['widget']['solution'], ns)  # top_pairs
pairs_panel, normalise, trade_pair, top_pairs = ns['pairs_panel'], ns['normalise'], ns['trade_pair'], ns['top_pairs']
CLOSE, MID, IND, BROKEN = ns['close'], ns['mid'], ns['ind'], ns['broken']


def cycle(px, start, k, wait=0):
    Pn = normalise(px[start:start + 378])
    form, trade = Pn[:252], Pn[252:]
    return [(p, trade_pair(form, trade, i, j, wait)) for p, (i, j) in [(q, q) for q in top_pairs(form, k)]]


# ---- 1. calendar (l1 screens[1], screens[7], review-1 items[1]) [live]
live = lambda month, K=6: list(range(max(0, month - K + 1), month + 1))
assert 126 // 21 == 6 and len(live(100)) == 6 and len(live(2)) == 3 and live(9) == [4, 5, 6, 7, 8, 9], 'l1 screens[1] [live]'
assert sum(1 for m in range(6) if 21 * m + 252 <= 360 <= 21 * m + 377) == 6, 'l1 screens[1].widget.answer [live]'

# ---- 2. the mirror trade loses what the right one gains (l1 screens[0].options[1].why, l6 screens[5]) [sign]
P0 = normalise(CLOSE[:378]); F0, T0_ = P0[:252], P0[252:]
pay23 = trade_pair(F0, T0_, 2, 3)[0]
# flipping the sides is the same as negating every trip's payoff: build it from the code's own loop
a, b = T0_[:, 2], T0_[:, 3]
sd23 = float(np.std(F0[:, 2] - F0[:, 3]))
assert abs(pay23 - 0.221762) < 1e-6, 'l1 screens[0] [sign] pair (2,3) payoff'
# the trip booked on days 28 to 43: long A short B earns rA - rB; the flipped trade earns rB - rA
rA, rB = a[43] / a[28] - 1, b[43] / b[28] - 1
assert abs((rA - rB) - 0.0574) < 5e-4 and abs((rB - rA) + 0.0574) < 5e-4, 'l6 screens[5] [sign] mirror trade = -0.0574'

# ---- 3. look-ahead threshold (l1 screens[5], quiz[0]; l5 screens[0]) [lookahead]
sdT = float(np.std(T0_[:, 2] - T0_[:, 3]))
assert round(sd23, 4) == 0.0210 and round(sdT, 4) == 0.0300, 'l1 screens[5].prose [lookahead] formation 0.0210, trading 0.0300'


def cycle_mean(px, start, k, sd_source):
    """Committed return of one cycle with the 2 sd trigger from the formation sd ('form') or the trading sd ('trade')."""
    Pn = normalise(px[start:start + 378])
    form, trade = Pn[:252], Pn[252:]
    tot = 0.0
    for i, j in top_pairs(form, k):
        src = form if sd_source == 'form' else trade
        tot += trade_pair(src, trade, i, j)[0]   # trade_pair reads the sd from its first argument only
    return tot / k


# does a trading-period sd "flatter the backtest"? Monte Carlo on fresh panels: it is not a general law
flat_form, flat_trade = [], []
for seed in range(30):
    c_, m_, i_, b_ = pairs_panel(seed=100 + seed, days=378, break_frac=0.0)
    flat_form.append(cycle_mean(c_, 0, 20, 'form'))
    flat_trade.append(cycle_mean(c_, 0, 20, 'trade'))
d = np.array(flat_trade) - np.array(flat_form)
print(f'[lookahead] trading-sd threshold minus formation-sd threshold, 30 fresh first cycles: mean {d.mean():+.4f}, se {d.std(ddof=1)/np.sqrt(len(d)):.4f}')
# after the third-read fix pass the content says look-ahead is invalid whatever its effect, that it flatters on average
# on this course's simulated prices, and that on the screen's pair (2, 3) it earns less. This 30-cycle check is
# underpowered for the sign; the asserts live in pairs-rep-L1-lookahead-third-read.py. Print only, no assert on its sign.

# ---- 4. open share of pair-days (l1 screens[8].explain "most will be waiting" against l13 screens[2] "open most of the time") [open-share]
open_days, all_days = 0, 0
for s in range(0, CLOSE.shape[0] - 378 + 1, 21):
    Pn = normalise(CLOSE[s:s + 378]); form, trade = Pn[:252], Pn[252:]
    for i, j in top_pairs(form, 20):
        sd = float(np.std(form[:, i] - form[:, j]))
        a_, b_ = trade[:, i].tolist(), trade[:, j].tolist(); n = len(a_); t = 0
        while t < n:
            s_ = a_[t] - b_[t]
            if sd > 0 and abs(s_) > 2 * sd and t < n - 1:
                side = 1 if s_ > 0 else -1
                tc = next((u for u in range(t + 1, n) if (a_[u] - b_[u]) * side <= 0), None)
                tx = n - 1 if tc is None else tc
                open_days += tx - t
                t = tx + 1
                continue
            t += 1
        all_days += n
share_open = open_days / all_days
print(f'[open-share] top-20 pair-days open, 127 cycles, same day: {share_open:.3f}')
# l1 screens[8].explain says most of the 120 live pairs are waiting (open share under 0.5); l13 screens[2].options[2].why
# says "our pairs are open most of the time" (over 0.5). Exactly one of them can hold on this panel.
# l1 screens[8].explain "Most will be waiting for a 2 sd gap" needs an open share under 0.5. It is 0.533 on this panel.
# Fix pass: the explain now reads "About half are open at any time; the rest wait for a 2 sd gap."
# Second computation (fix pass): a position counts as held on day t when it was held overnight into t, using the
# course's trade_pair rule with the one-day wait; the same 127 cycles give 0.528 (0.533 same day, 0.534 on mids).
held_days, n_days = 0, 0
for s in range(0, CLOSE.shape[0] - 378 + 1, 21):
    Pn = normalise(CLOSE[s:s + 378]); form, trade = Pn[:252], Pn[252:]
    for i, j in top_pairs(form, 20):
        sd = float(np.std(form[:, i] - form[:, j])); a_, b_ = trade[:, i], trade[:, j]; n = len(a_); h = np.zeros(n, bool); t = 0
        while t < n:
            s_ = a_[t] - b_[t]
            if sd > 0 and abs(s_) > 2 * sd and t + 1 < n - 1:
                side = np.sign(s_); tc = next((u for u in range(t + 1, n) if (a_[u] - b_[u]) * side <= 0), None)
                tx = n - 1 if tc is None else min(tc + 1, n - 1); h[t + 2:tx + 1] = True; t = tx + 1; continue
            t += 1
        held_days += int(h.sum()); n_days += n
print(f'[open-share] second count, held overnight, one-day wait: {held_days / n_days:.3f}')
assert abs(share_open - 0.5) < 0.1 and abs(held_days / n_days - 0.5) < 0.1 and 'About half are open' in DOC['l1-ggr-design']['screens'][8]['explain']['text'], \
    'l1 screens[8].explain [open-share] about half of the pairs are open at any time (corrected claim, fix pass)'
assert share_open > 0.5, 'l13 screens[2].options[2].why [open-share] our pairs are open most of the time'

# ---- 5. SSD and sd toys (l2 screens[2], screens[3]; review-1 items[2], items[3]) [ssd-toy] [sd-toy]
ta = np.array([1, 1.02, 1.05, 1.03, 1.06, 1.08]); tb = np.array([1, 1.01, 1.03, 1.05, 1.04, 1.07])
assert abs(((ta - tb) ** 2).sum() - 0.0014) < 1e-12, 'l2 screens[2] [ssd-toy]'
assert abs((ta - tb).sum() - 0.04) < 1e-12 and abs(np.abs(ta - tb).sum() - 0.08) < 1e-12, 'l2 screens[2].wrong [ssd-toy] unsquared 0.04, absolute 0.08'
sp = ta - tb
assert abs(np.std(sp) - 0.0137) < 5e-5, 'l2 screens[3] [sd-toy] np.std divides by n'
assert abs(np.std(sp, ddof=1) - 0.0151) < 5e-5 and abs(np.sqrt((sp ** 2).mean()) - 0.0153) < 5e-5, 'l2 screens[3].wrong [sd-toy] ddof1 0.0151, rms 0.0153'
assert abs(np.std([0, 0.03, -0.03, 0]) - 0.0212) < 5e-5, 'review-1 items[3] [sd-toy]'
assert abs(np.std(F0[:, 2] - F0[:, 3], ddof=1) / np.std(F0[:, 2] - F0[:, 3]) - 1) < 0.003, 'l2 screens[3] [sd-toy] n against n-1 differs by 0.2% at n=252'

# ---- 6. the Gram identity and its exact zero diagonal (l2 screens[5], screens[9]) [gram]
G = F0.T @ F0; dg = np.diag(G); D = dg[:, None] + dg[None, :] - 2 * G
loop = np.array([[((F0[:, i] - F0[:, j]) ** 2).sum() for j in range(100)] for i in range(100)])
assert np.allclose(D, loop, atol=1e-9) and np.abs(np.diag(D)).max() == 0.0, 'l2 screens[5] [gram] identity and exactly zero diagonal'
assert abs(D[2, 3] - 0.1117) < 5e-5, 'l2 screens[1].widget.answer [gram] close pair SSD 0.1117'
x = np.array([0.1, -0.1, 0.0]); assert (x ** 2).sum() != x.sum() ** 2, 'l2 screens[9].lines[4].why [gram] squaring the sum differs'

# ---- 7. NaN and 0/0 behaviour (l2 screens[7], l4 screens[6], l5 screens[5]) [nan]
with np.errstate(all='ignore'):
    q = np.float64(0.0) / np.float64(0.0)
assert np.isnan(q) and not (q > 2) and not (np.nan > 0), 'l2 screens[7].options[2].why [nan] 0/0 is NaN and NaN > 2 is False'
try:
    0 / 0; raised = False
except ZeroDivisionError:
    raised = True
assert raised, 'l4 screens[6].options[2].why [nan] 0/0 raises in Python'
assert not bool((np.array([10.0, np.nan]) > 0).all()), 'l5 screens[5].explain [nan] NaN fails the positive check'

# ---- 8. distance is not correlation (l2 screens[8]) [corr-vs-dist]
rng = np.random.default_rng(7)
ra = 0.012 * rng.standard_normal(252); rg = 2 * ra
pa = np.exp(np.concatenate([[0], np.cumsum(ra)])); pg = np.exp(np.concatenate([[0], np.cumsum(rg)]))
assert abs(np.corrcoef(ra, rg)[0, 1] - 1) < 1e-12, 'l2 screens[8].prose [corr-vs-dist] return correlation 1'
ssd_ag = ((pa - pg) ** 2).sum()
assert ssd_ag > 10 * 0.1117, 'l2 screens[8].options[0] [corr-vs-dist] correlated returns, far apart levels'
A = np.round(F0[:, 2], 4); assert abs(((A - np.round(A * A, 4)) ** 2).sum() - 2.73) < 0.01, 'l2 screens[8].explain [corr-vs-dist] SSD 2.73 on the panel'

# ---- 9. nomination under the paper's nearest-partner rule in the toys (l3 screens[4], review-1 items[4]) [nominate-toy]
toy = {('A', 'B'): 3.00, ('A', 'C'): 6.75, ('B', 'C'): 0.75, ('A', 'D'): 300, ('B', 'D'): 243, ('C', 'D'): 216.75, ('D', 'E'): 27,
       ('A', 'E'): 507, ('B', 'E'): 432, ('C', 'E'): 396.75, ('A', 'F'): 2700, ('B', 'F'): 2523, ('C', 'F'): 2436.75, ('D', 'F'): 1200, ('E', 'F'): 867}


def nominated(order):
    """Pairs the paper's rule nominates: (i, j) is i's or j's nearest partner, i.e. the first listed pair holding i or j."""
    seen, out = set(), []
    for p in order:
        if p[0] not in seen or p[1] not in seen:
            out.append(p)
        seen |= set(p)
    return out


order = sorted(toy, key=toy.get)
assert order[:2] == [('B', 'C'), ('A', 'B')] and ('A', 'B') in nominated(order), 'l3 screens[4].options[1].why [nominate-toy] A-B is A\'s nearest partner'


def one_partner(order, k):
    used, out = set(), []
    for p in order:
        if p[0] in used or p[1] in used:
            continue
        out.append(p); used |= set(p)
        if len(out) == k:
            break
    return out


assert one_partner(order, 2) == [('B', 'C'), ('D', 'E')], 'l3 screens[4].options[0] [nominate-toy]'
r1 = [(3, 8), (3, 5), (5, 9), (1, 2)]
assert nominated(r1) == r1 and one_partner(r1, 3) == [(3, 8), (5, 9), (1, 2)], 'review-1 items[4] [nominate-toy] (3,5) nominated by 5; variant skips it'
# on the course panel at start 1512 the closest-overall top 20 is not the paper's nominated list either (informational)
P1512 = normalise(CLOSE[1512:1764]); G2 = P1512.T @ P1512; d2 = np.diag(G2); D2 = d2[:, None] + d2[None, :] - 2 * G2
iu, ju = np.triu_indices(100, 1); full_order = [(int(iu[o]), int(ju[o])) for o in np.argsort(D2[iu, ju], kind='stable')]
nom = set(nominated(full_order)); t20 = full_order[:20]
print(f'[nominate] start 1512: {sum(1 for p in t20 if p in nom)} of the 20 closest overall are nominated under the paper\'s rule; '
      f'{sum(1 for s in range(100) if sum(1 for p in nominated(full_order) if s in p) >= 2)} shares are the nearest partner of two or more others')

# ---- 10. chance pairs: unrelated random walks can stay close for a year (l3 screens[8], review-1 items[5]) [chance-close]
planted_late = []
for seed in range(12):
    c_, m_, i_, b_ = pairs_panel(seed=300 + seed)
    tp = top_pairs(normalise(c_[2016:2268]), 20)
    planted_late.append(sum(1 for i, j in tp if j == i + 1 and i % 2 == 0 and i < 40))
print(f'[chance-close] planted pairs in the top 20 at start 2016 over 12 fresh seeds: {planted_late}')
assert np.mean(planted_late) < 20 and min(planted_late) < 20, 'l3 screens[8] [chance-close] chance pairs fill the top 20 after the break'
t2016 = top_pairs(normalise(CLOSE[2016:2268]), 20)
assert sum(1 for i, j in t2016 if j == i + 1 and i % 2 == 0 and i < 40) == 3, 'l3 screens[8].widget.answer [chance-close] 3 planted on the course panel'

# ---- 11. the placebo: random pairs on fresh panels, mids and closes (l5 screens[6], screens[7], quiz[0]) [placebo]
pm, pc = [], []
for seed in range(200):
    c_, m_, i_, b_ = pairs_panel(seed=500 + seed, days=378, break_frac=0.0)
    Pc = normalise(c_); Pm = normalise(m_)
    r = np.random.default_rng(seed)
    for _ in range(20):
        i, j = r.choice(100, 2, replace=False)
        pm.append(trade_pair(Pm[:252], Pm[252:], int(i), int(j))[0])
        pc.append(trade_pair(Pc[:252], Pc[252:], int(i), int(j))[0])
pm, pc = np.array(pm), np.array(pc)
se_m = pm.std(ddof=1) / np.sqrt(len(pm)); se_c = pc.std(ddof=1) / np.sqrt(len(pc))
print(f'[placebo] 4000 random pairs on 200 fresh panels: mids mean {pm.mean():+.4f} (se {se_m:.4f}); closes mean {pc.mean():+.4f} (se {se_c:.4f}); closes minus mids {(pc - pm).mean():+.4f}')
assert abs(pm.mean()) < 2.5 * se_m, 'l5 screens[6].explain [placebo] random pairs on mids average within noise of 0'
assert (pc - pm).mean() > 0 and (pc - pm).mean() > 2 * (pc - pm).std(ddof=1) / np.sqrt(len(pc)), 'l5 screens[7].explain [placebo] the bounce lifts even random pairs'

# ---- 12. shorter half-life, more round trips (review-1 items[8].explain) [halflife]
assert abs(0.5 ** (1 / 8) - 0.9170) < 5e-5 and abs(0.5 ** 0.25 - 0.8409) < 5e-5, 'l5 screens[3], review-1 items[8] [halflife] phi'
r = np.random.default_rng(11); trips = {}
for hl in (4.0, 8.0):
    phi = 0.5 ** (1 / hl); counts = []
    for _ in range(300):
        e = 0.008 * r.standard_normal(378); s = np.zeros(378)
        for t in range(1, 378):
            s[t] = phi * s[t - 1] + e[t]
        sd = s[:252].std(); x = s[252:]; n = len(x); t = 0; c = 0
        while t < n:
            if abs(x[t]) > 2 * sd and t < n - 1:
                side = 1 if x[t] > 0 else -1
                tc = next((u for u in range(t + 1, n) if x[u] * side <= 0), None)
                c += 1; t = (n - 1 if tc is None else tc) + 1; continue
            t += 1
        counts.append(c)
    trips[hl] = np.mean(counts)
print(f'[halflife] round trips per 126-day period: half-life 4: {trips[4.0]:.2f}, half-life 8: {trips[8.0]:.2f}')
assert trips[4.0] > trips[8.0], 'review-1 items[8].explain [halflife] shorter half-life gives more round trips'

# ---- 13. k/n identity (l5 screens[9], homework-1 items[4]) [kn]
res = cycle(CLOSE, 0, 20); tot = sum(p for _, (p, o) in res); n = sum(1 for _, (p, o) in res if o)
assert n == 19 and abs((tot / n) / (tot / 20) - 20 / 19) < 1e-12, 'l5 screens[9] [kn] employed/committed = k/n'
assert abs(14.20 / 11.36 - 1.25) < 0.01, 'homework-1 items[4] [kn] 5/4'

# ---- 14. every code widget of the level: solution passes, starter fails (ledger rows "[code]") [code]


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

print(f'pairs-rep L1 concepts r2: done in {time.time() - T0:.0f}s, {len(FAILS)} expected failure(s)')
assert not FAILS, 'content findings: ' + '; '.join(FAILS)
