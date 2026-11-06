"""Recompute every number stated in stat-models level 4 and check it at its JSON path.

Run: python3 docs/reports/stat-models-L4-numbers.py   (NumPy, SciPy and the standard library; exits 0 when all pass, about 1 min)

Each figure is computed twice: a conjugate closed form (scipy.stats) against a grid or seeded draws, two optimisers,
or a formula against an enumeration. It also checks (a) every numeric `wrong[]` value lies outside the answer's band
(validator rule 581: |wrong - answer| > tol_answer + tol_wrong), (b) every code solution passes every hidden test and
every starter fails every hidden test, with a harness that mirrors code.js (setup, call, expect, isclose/equal, tol).
Seeded streams (default_rng 11, 61, 97, 102, 101, 5, 3, 9) are identical in local NumPy and Pyodide's 0.27.7 (NumPy 2.0.2):
the playthrough runs these solutions in Pyodide against exact expected values and passes.
The l17 series caption values come from the engine's own rng (app/js/engine/sim.js) via node, below.
"""
import json
import math
import os
import subprocess
import sys

import numpy as np
from scipy import optimize, special, stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level("stat-models", 4)
E = lv.expect
BAD = []


def agree(a, b, tol, what):
    a, b = np.atleast_1d(np.asarray(a, float)), np.atleast_1d(np.asarray(b, float))
    ok = bool(np.all(np.abs(a - b) <= tol))
    print(('ok ' if ok else 'BAD') + f' agree {what}: {a.tolist()} vs {b.tolist()} (tol {tol})')
    if not ok:
        BAD.append(what)


def two(v1, v2, tol, what, dp):
    agree(v1, v2, tol, what)
    return round(float(v1), dp)


# ---------------------------------------------------------------- l14 conjugate priors
b = stats.beta(15, 35)
rng = np.random.default_rng(1); d = rng.beta(15, 35, 2_000_000)
mean = two(b.mean(), d.mean(), 1e-3, 'beta mean', 2)
sd = two(b.std(), d.std(), 1e-3, 'beta sd', 4)
lo, hi = b.ppf([0.025, 0.975]); qlo, qhi = np.quantile(d, [0.025, 0.975])
agree([lo, hi], [qlo, qhi], 2e-3, 'beta interval')
sf = two(b.sf(0.25), (d > 0.25).mean(), 2e-3, 'P(p>0.25)', 4)
mc_sf = round(float((d > 0.25).mean()), 4)
E('l14', 'screens[0].widget.answer', mean); E('l14', 'screens[0].explain.text', 0.30); E('l14', 'screens[0].explain.text', 0.325)
E('l14', 'screens[0].widget.wrong[0].value', 13 / 40); E('l14', 'screens[0].widget.wrong[1].value', 0.2)
agree(40 / 50, (15 / 50 - 0.2) / (13 / 40 - 0.2), 1e-12, 'weight on data')
E('l14', 'screens[1].widget.answer', 0.8); E('l14', 'screens[1].widget.wrong[0].value', 0.2); E('l14', 'screens[1].widget.wrong[1].value', 0.25)
E('l14', 'screens[2].prose', sd); E('l14', 'screens[2].prose', round(14 / 48, 4)); E('l14', 'screens[2].prose', round(lo, 4)); E('l14', 'screens[2].prose', round(hi, 4))
E('l14', 'screens[2].widget.answer', sf); E('l14', 'screens[2].widget.wrong[0].value', round(1 - sf, 4))
prior_sf = round(stats.beta(2, 8).sf(0.25), 4); agree(prior_sf, (np.random.default_rng(2).beta(2, 8, 1_000_000) > 0.25).mean(), 2e-3, 'prior P>.25')
E('l14', 'screens[2].widget.wrong[1].value', prior_sf); E('l14', 'screens[2].explain.text', mc_sf); E('l14', 'screens[2].explain.text', prior_sf)
mode_grid = np.linspace(0.001, 0.999, 99801)[np.argmax(b.pdf(np.linspace(0.001, 0.999, 99801)))]; agree(mode_grid, 14 / 48, 1e-4, 'beta mode')
# Gamma-Poisson
g = stats.gamma(17, scale=1 / 6); dg = np.random.default_rng(3).gamma(17, 1 / 6, 2_000_000)
gmean = two(g.mean(), dg.mean(), 2e-3, 'gamma mean', 4); gsd = two(g.std(), dg.std(), 2e-3, 'gamma sd', 4)
glo, ghi = g.ppf([0.025, 0.975]); agree([glo, ghi], np.quantile(dg, [0.025, 0.975]), 5e-3, 'gamma interval')
agree((2 + 15) / (1 + 5), 5 / 6 * 3 + 1 / 6 * 2, 1e-12, 'gamma mean as weighted average')
E('l14', 'screens[3].widget.answer', round(5 / 6, 4)); E('l14', 'screens[3].question', gmean); E('l14', 'screens[3].widget.wrong[0].value', round(1 / 6, 4)); E('l14', 'screens[3].widget.wrong[1].value', 0.8)
E('l14', 'screens[3].explain.text', gmean); E('l14', 'screens[3].explain.text', gsd); E('l14', 'screens[3].explain.text', round(glo, 4)); E('l14', 'screens[3].explain.text', round(ghi, 4))
E('l14', 'screens[5].explain.text', 17); E('l14', 'screens[5].explain.text', 6); E('l14', 'screens[5].explain.text', round(7 / 16, 2))
# normal-normal
prec = 1 / 4 + 1 / 16; pm = (6 / 16) / prec; ps = prec ** -0.5
x = np.linspace(-20, 20, 400001); w = np.exp(-x ** 2 / 8 - (6 - x) ** 2 / 32); w /= w.sum()
agree(pm, (w * x).sum(), 1e-6, 'normal post mean grid'); agree(ps, math.sqrt((w * (x - pm) ** 2).sum()), 1e-6, 'normal post sd grid')
p0 = two(stats.norm(pm, ps).sf(0), w[x > 0].sum(), 1e-4, 'P(alpha>0)', 4)
nlo, nhi = stats.norm(pm, ps).interval(0.95); c = np.cumsum(w); agree([nlo, nhi], [x[np.searchsorted(c, .025)], x[np.searchsorted(c, .975)]], 1e-3, 'normal interval')
E('l14', 'screens[6].prose', 0.3125); E('l14', 'screens[6].prose', round(ps, 4)); E('l14', 'screens[6].prose', '\\sqrt{3.2}'); agree(1 / prec, 3.2, 1e-12, 'posterior variance 3.2')
E('l14', 'screens[6].widget.answer', round(pm, 4)); E('l14', 'screens[6].widget.wrong[2].value', 0.8 * 6); E('l14', 'screens[6].widget.wrong[1].value', 3)
E('l14', 'screens[6].explain.text', 0.8); E('l14', 'screens[6].explain.text', round(nlo, 3)); E('l14', 'screens[6].explain.text', round(nhi, 3)); E('l14', 'screens[6].explain.text', p0)
# trap
agree(stats.gamma(17, scale=6).mean(), 17 * 6, 1e-9, 'scale-6 mean'); agree(stats.gamma(17, 6).mean(), 17 + 6, 1e-9, 'loc-6 mean')
E('l14', 'screens[7].prose', 102); E('l14', 'screens[7].widget.options[2].why', 23); E('l14', 'screens[7].explain.text', gmean)
# flat prior
E('l14', 'screens[8].widget.answer', round(1 / 42, 4)); E('l14', 'screens[8].widget.wrong[1].value', round(1 / 40, 4))
f05 = two(stats.beta(1, 41).sf(0.05), (1 - 0.05) ** 41, 1e-12, 'flat P(p>.05)', 2); E('l14', 'screens[8].explain.text', f05)
# transfer
agree((15 + 6) / (50 + 30), (2 + 19) / (10 + 70), 1e-12, 'sequential = batch')
E('l14', 'screens[10].widget.answer', 21 / 80); E('l14', 'screens[10].widget.wrong[0].value', round(23 / 90, 4)); E('l14', 'screens[10].widget.wrong[1].value', 0.2)
# code screen outputs
E('l14', 'screens[9].explain.text', round(lo, 6)); E('l14', 'screens[9].explain.text', round(ghi, 6))
# quiz
E('l14', 'quiz[1].widget.answer', sd); E('l14', 'quiz[1].widget.wrong[0].value', round(b.var(), 4)); E('l14', 'quiz[1].widget.wrong[1].value', round(math.sqrt(0.3 * 0.7 / 40), 4))
E('l14', 'quiz[2].widget.answer', 2 / 4); E('l14', 'quiz[2].widget.wrong[2].value', round(2 / 3, 4))
agree(stats.norm(*(lambda p: ((6 / 9) / p, p ** -.5))(1 / 9 + 1 / 9)).mean(), 3, 1e-12, 'quiz shrink 3')

# ---------------------------------------------------------------- l15 posterior predictive
bb = stats.betabinom(10, 15, 35)
pmf_f = np.array([math.comb(10, j) * math.exp(special.betaln(j + 15, 45 - j) - special.betaln(15, 35)) for j in range(11)])
agree(bb.pmf(np.arange(11)), pmf_f, 1e-12, 'betabinom pmf formula')
rng = np.random.default_rng(2); kk = rng.binomial(10, rng.beta(15, 35, 2_000_000))
bbt = two(bb.sf(4), (kk >= 5).mean(), 2e-3, 'bb P>=5', 4); bbv = two(bb.var(), kk.var(), 5e-3, 'bb var', 4)
pl = two(stats.binom(10, .3).sf(4), sum(math.comb(10, j) * .3 ** j * .7 ** (10 - j) for j in range(5, 11)), 1e-12, 'binom P>=5', 4)
E('l15', 'screens[0].widget.answer', pl); E('l15', 'screens[0].widget.wrong[0].value', bbt); E('l15', 'screens[0].widget.wrong[1].value', round(stats.binom(10, .3).pmf(5), 4))
E('l15', 'screens[0].explain.text', pl); E('l15', 'screens[0].explain.text', bbt)
E('l15', 'screens[1].widget.answer', bbv); agree(bbv, 2.1 * 60 / 51, 1e-4, 'bb var formula'); E('l15', 'screens[1].widget.wrong[1].value', round(math.sqrt(bb.var()), 4)); E('l15', 'screens[1].explain.text', 2.1)
for j in range(11):
    E('l15', f'screens[2].canvas.params.rows[{j}]', f'{bb.pmf(j):.6f}'); E('l15', f'screens[2].canvas.params.rows[{j}]', f'{stats.binom(10, .3).pmf(j):.6f}')
E('l15', 'screens[2].widget.answer', bbt); E('l15', 'screens[2].widget.wrong[0].value', round(bb.sf(3), 4))
nb = stats.nbinom(17, 6 / 7); rng = np.random.default_rng(2); yy = rng.poisson(rng.gamma(17, 1 / 6, 2_000_000))
nbv = two(nb.var(), yy.var(), 2e-2, 'nb var', 4); nbt = two(nb.sf(5), (yy >= 6).mean(), 2e-3, 'nb P>=6', 4); pot = round(stats.poisson(17 / 6).sf(5), 4)
agree(nb.var(), 17 / 6 + 17 / 36, 1e-12, 'nb var decomposition')
E('l15', 'screens[3].widget.answer', nbv); E('l15', 'screens[3].widget.wrong[0].value', round(17 / 6, 4)); E('l15', 'screens[3].widget.wrong[1].value', round(17 / 6 / (7 / 6), 4))
E('l15', 'screens[3].explain.text', nbt); E('l15', 'screens[3].explain.text', pot)
E('l15', 'screens[4].prose', pot); E('l15', 'screens[4].prose', nbt); E('l15', 'screens[4].widget.options[2].text', round((pot + nbt) / 2, 4))
E('l15', 'screens[4].explain.text', pl); E('l15', 'screens[4].explain.text', bbt)
# D3 check
rng = np.random.default_rng(61); xx = rng.normal(0, 1, 200); zz = rng.normal(0, 1, 200); mu = np.exp(1.5 + 0.4 * xx); lam = rng.gamma(2.0, 0.5 * mu); yd = rng.poisson(lam)
agree([yd.sum(), (yd == 0).sum(), yd.max()], [881, 28, 23], 0, 'D3 sum, zeros, max')
ez = 200 * (200.1 / 201.1) ** 882
rng = np.random.default_rng(3); Lr = rng.gamma(882, 1 / 200.1, 200000); zs = []; vs = []
for i in range(0, 200000, 20000):
    Yc = rng.poisson(Lr[i:i + 20000][:, None] * np.ones((1, 200))); zs.append((Yc == 0).sum(1)); vs.append(Yc.var(1, ddof=1))
zs = np.concatenate(zs); vs = np.concatenate(vs)
agree(ez, zs.mean(), 0.02, 'E zeros integral vs sim')
E('l15', 'screens[5].widget.answer', round(ez, 2)); E('l15', 'screens[5].widget.accept', round(ez, 3)); E('l15', 'screens[5].widget.wrong[1].value', round(200 * math.exp(-882 / 200.1), 3))
E('l15', 'screens[5].explain.text', int(zs.max())); agree((vs >= yd.var(ddof=1)).sum(), 0, 0, 'no replicate variance reaches D3')
E('l15', 'screens[6].prose', round(882 / 200.1, 4)); E('l15', 'screens[6].prose', yd.mean()); E('l15', 'screens[6].widget.options[2].why', round(yd.var(ddof=1), 1))
E('l15', 'screens[9].prose', round(ez, 2)); E('l15', 'screens[9].explain.text', round(28 / ez))
E('l15', 'quiz[3].widget.answer', round((6 / 7) ** 17, 4)); agree(nb.pmf(0), (6 / 7) ** 17, 1e-12, 'nb pmf 0'); E('l15', 'quiz[3].widget.wrong[0].value', round(math.exp(-17 / 6), 4))
E('l15', 'quiz[1].prose', nbt); E('l15', 'quiz[1].prose', pot)
share = [round(float(np.mean(zs == j)), 4) for j in range(31)]
agree([lv.files['l15-posterior-predictive']['screens'][5]['canvas']['state']['values'][str(j)] for j in range(31)], share, 0, 'replicate histogram')

# ---------------------------------------------------------------- l16 MCMC
lpb = lambda x: 14 * math.log(x) + 34 * math.log(1 - x)
xs, z, u, chain = 0.5, [-1.2, 0.4, -0.9, 2.1], [0.3, 0.8, 0.05, 0.6], []
for zi, ui in zip(z, u):
    xp = round(xs + 0.1 * zi, 10); r1 = math.exp(lpb(xp) - lpb(xs)); r2 = stats.beta(15, 35).pdf(xp) / stats.beta(15, 35).pdf(xs)
    agree(r1, r2, 1e-9 * r1, f'hand ratio {xp}'); chain.append((xp, r1, xp if ui < r1 else xs)); xs = xp if ui < r1 else xs
rows = lv.files['l16-fitting-by-mcmc']['screens'][1]['widget']['rows']
for i, (xp, r1, nx) in enumerate(chain):
    agree([rows[i][1]['answer'], rows[i][4]['answer']], [xp, nx], 1e-9, f'hand row {i + 1}')
    E('l16', f'screens[1].widget.rows[{i}][2]', [round(r1, 2), round(r1, 4), round(r1, 4), round(r1, 5)][i])
E('l16', 'screens[0].widget.answer', round(chain[0][1], 2)); E('l16', 'screens[0].widget.wrong[0].value', round(1 / chain[0][1], 4))
agree(chain[-1][2], 0.29, 1e-12, 'chain ends at 0.29')
# D1s
rng = np.random.default_rng(11); L = rng.uniform(0, 1, 300); y = rng.binomial(1, 1 / (1 + np.exp(6 - 10 * L))); L, y = L[:100], y[:100]
X = np.column_stack([np.ones(100), L]); agree(y.sum(), 33, 0, '33 defaults')
bI = np.zeros(2)
for _ in range(60):
    e = X @ bI; m_ = 1 / (1 + np.exp(-e)); bI = bI + np.linalg.solve((X.T * (m_ * (1 - m_))) @ X, X.T @ (y - m_))
bB = optimize.minimize(lambda bb_: np.sum(np.logaddexp(0, X @ bb_) - y * (X @ bb_)), [0, 0], method='BFGS', options={'gtol': 1e-10}).x
agree(bI, bB, 1e-5, 'MLE IRLS vs BFGS'); m_ = 1 / (1 + np.exp(-X @ bI)); C = np.linalg.inv((X.T * (m_ * (1 - m_))) @ X); se_ = np.sqrt(np.diag(C))
for j, (v, sv) in enumerate([('−8.0481', '1.7795'), ('12.8287', '2.7886')]):
    E('l16', f'screens[3].canvas.params.rows[0][{j + 1}]', v); E('l16', f'screens[3].canvas.params.rows[1][{j + 1}]', sv)
agree([round(bI[0], 4), round(bI[1], 4), round(se_[0], 4), round(se_[1], 4)], [-8.0481, 12.8287, 1.7795, 2.7886], 1e-9, 'MLE and SE as shown')


def grid(xs_, ys_, Lx):
    G0, G1 = np.meshgrid(xs_, ys_, indexing='ij'); LP = np.empty(G0.shape)
    for i in range(len(xs_)):
        e = G0[i][:, None] + G1[i][:, None] * Lx; LP[i] = -(np.logaddexp(0, e) - y * e).sum(-1) - (G0[i] ** 2 + G1[i] ** 2) / 200
    W = np.exp(LP - LP.max()); W /= W.sum(); m0, m1 = (W * G0).sum(), (W * G1).sum(); s0, s1 = np.sqrt((W * (G0 - m0) ** 2).sum()), np.sqrt((W * (G1 - m1) ** 2).sum())
    return m0, m1, s0, s1, (W * (G0 - m0) * (G1 - m1)).sum() / s0 / s1, (W / (1 + np.exp(-(G0 + 0.5 * G1)))).sum()


gu = grid(np.linspace(-18, 2, 1101), np.linspace(-2, 28, 1361), L)
gu2 = grid(np.linspace(-20, 3, 1601), np.linspace(-4, 30, 1601), L)
agree(gu[:6], gu2[:6], 2e-3, 'uncentred grid, two meshes')
for path in ['screens[3].canvas.params.rows', 'screens[4].canvas.params.rows']:
    E('l16', path + '[2][1]', '−7.861'); E('l16', path + '[2][2]', '12.537'); E('l16', path + '[3][1]', '1.591'); E('l16', path + '[3][2]', '2.492')
agree([round(gu[0], 3), round(gu[1], 3), round(gu[2], 3), round(gu[3], 3), round(gu[4], 3)], [-7.861, 12.537, 1.591, 2.492, -0.971], 1e-9, 'grid moments as shown')
E('l16', 'screens[3].canvas.state.caption', -0.971)


def metropolis(log_post, start, step, n, seed):
    rr = np.random.default_rng(seed); x_ = np.array(start, float); dd = len(x_); out = np.empty((n, dd)); l_ = log_post(x_); acc = 0
    for t in range(n):
        zq = rr.standard_normal(dd); uq = rr.uniform(); xp = x_ + step * zq; ln_ = log_post(xp)
        if np.log(uq) < ln_ - l_:
            x_, l_, acc = xp, ln_, acc + 1
        out[t] = x_
    return out, acc / n


lpl = lambda bb_, XX=X: float(np.sum(y * (XX @ bb_) - np.logaddexp(0, XX @ bb_)) - bb_ @ bb_ / 200)
ch1, ar1_ = metropolis(lpl, [0, 0], 1.0, 20000, 1); pm1 = ch1[2000:].mean(0)
agree(pm1, gu[:2], [0.25, 0.25], 'chain vs grid means (test tolerance)')
E('l16', 'screens[3].canvas.params.rows[4][1]', '−7.869'); E('l16', 'screens[3].canvas.params.rows[4][2]', '12.545'); agree(np.round(pm1, 3), [-7.869, 12.545], 1e-9, 'chain means as shown')
E('l16', 'screens[9].explain.text', -7.869); E('l16', 'screens[9].explain.text', 12.545)
for s_, txt in [(0.05, '0.952'), (0.5, '0.579'), (1.0, '0.351'), (1.5, '0.24'), (5, '0.053')]:
    a_ = metropolis(lpl, [-8, 12.8], s_, 20000, 1)[1]; agree(round(a_, 3), float(txt), 1e-9, f'acceptance step {s_}')
for s_, ans in [(2.4, 0.4423), (1, 0.7048), (5, 0.2422)]:
    th = 2 / math.pi * math.atan(2 / s_); agree(round(th, 4), ans, 1e-9, f'arctan rate {s_}')
sim24 = metropolis(lambda v: -0.5 * float(v @ v), [0.0], 2.4, 20000, 1)[1]
agree(sim24, 2 / math.pi * math.atan(2 / 2.4), 0.02, 'sim vs theory acceptance')
E('l16', 'screens[5].widget.answer', 0.4423); E('l16', 'screens[5].widget.wrong[0].value', 0.7048); E('l16', 'screens[5].widget.wrong[1].value', round(math.atan(2 / 2.4), 4)); E('l16', 'screens[5].hints[1].text', round(math.atan(2 / 2.4), 4))
E('l16', 'screens[5].explain.text', round(sim24, 4)); E('l16', 'screens[5].explain.text', 0.2422); E('l16', 'screens[8].canvas.params.lines[2]', round(sim24, 4))
# accepted-only trap
rr = np.random.default_rng(1); xq = 0.0; lq = 0.0; full = np.empty(200000); accd = []
for t in range(200000):
    zq = rr.standard_normal(1)[0]; uq = rr.uniform(); xp = xq + 5 * zq; ln_ = -0.5 * xp * xp
    if np.log(uq) < ln_ - lq:
        xq, lq = xp, ln_; accd.append(xq)
    full[t] = xq
accd = np.array(accd)
E('l16', 'screens[6].canvas.params.lines[1]', f'{full.std():.3f}'); E('l16', 'screens[6].canvas.params.lines[1]', f'{(np.abs(full) > 2).mean():.4f}')
E('l16', 'screens[6].canvas.params.lines[2]', f'{accd.std():.3f}'); E('l16', 'screens[6].canvas.params.lines[2]', f'{(np.abs(accd) > 2).mean():.4f}')
E('l16', 'screens[6].prose', round(2 * stats.norm.sf(2) * 100, 2))
ll_mle = float(np.sum(y * (X @ bI) - np.logaddexp(0, X @ bI))); agree(round(ll_mle), -22, 0, 'loglik at MLE about -22')
E('l16', 'screens[7].prose', -22); E('l16', 'screens[7].prose', -2200)
pd_post = gu[5]; pd_chain = (1 / (1 + np.exp(-(ch1[2000:, 0] + 0.5 * ch1[2000:, 1])))).mean(); pd_plug = 1 / (1 + np.exp(-(bI[0] + 0.5 * bI[1])))
agree(pd_post, pd_chain, 0.003, 'PD grid vs chain'); E('l16', 'screens[10].prose', round(pd_post, 4)); E('l16', 'screens[10].prose', round(pd_chain, 4))
E('l16', 'screens[10].widget.answer', round(pd_plug, 4)); E('l16', 'screens[10].widget.wrong[1].value', round(bI[0] + 0.5 * bI[1], 4)); E('l16', 'screens[11].widget.options[2].why', round(pd_plug, 4))
E('l16', 'screens[4].explain.text', 2.7886); agree(round(bI[1] - gu[1], 2), 0.29, 1e-9, 'slope moves 0.29')
E('l16', 'quiz[1].prose', -0.02)
agree(math.log(sys.float_info.min * sys.float_info.epsilon), -744.4, 0.1, 'smallest double near e^-745')

# ---------------------------------------------------------------- l17 convergence


def rhat(c_):
    c_ = np.asarray(c_, float); m, n = c_.shape; W = c_.var(1, ddof=1).mean(); B = n * c_.mean(1).var(ddof=1); return math.sqrt(((n - 1) / n * W + B / n) / W)


def split_rhat(c_):
    c_ = np.asarray(c_, float); h = c_.shape[1] // 2; return rhat(np.vstack([c_[:, :h], c_[:, -h:]]))


def ess_ar1(c_):
    dd = np.asarray(c_, float) - np.mean(c_); ph = (dd[:-1] @ dd[1:]) / (dd @ dd); return len(c_) * (1 - ph) / (1 + ph)


hand = np.array([[1, 2, 3, 4], [3, 4, 5, 6.]])
Wh, Bh = hand.var(1, ddof=1).mean(), 4 * hand.mean(1).var(ddof=1); vp = 0.75 * Wh + Bh / 4
agree(vp, 3.25, 1e-12, 'var+ 3.25')
agree(hand.ravel().var(ddof=1), 6 / 7 * Wh + Bh / 7, 1e-12, 'total variance split')
rows = lv.files['l17-has-it-converged']['screens'][2]['widget']['rows']
agree([rows[0][1]['answer'], rows[1][1]['answer'], rows[2][1]['answer'], rows[3][1]['answer']], [round(Wh, 4), Bh, vp, round(rhat(hand), 4)], 1e-9, 'hand table')
agree(rhat(hand), math.sqrt(1.95), 1e-12, 'sqrt 1.95'); E('l17', 'screens[2].explain.text', round(hand.ravel().var(ddof=1), 4))
agree([rows[0][1]['wrong'][0]['value'], rows[1][1]['wrong'][0]['value'], rows[3][1]['wrong'][0]['value']], [hand.var(1).mean(), hand.mean(1).var(ddof=1), 1.95], 1e-9, 'hand table wrongs')
for phi, ans in [(0.9, 105.3), (0.5, 667), (0.9409, 61)]:
    agree(round(2000 * (1 - phi) / (1 + phi), 1 if phi == 0.9 else 0), ans, 1e-9, f'ESS phi {phi}')
E('l17', 'screens[4].widget.answer', 105.26); E('l17', 'screens[4].widget.wrong[0].value', 200); E('l17', 'screens[4].widget.wrong[1].value', round(2000 / 1.9, 1))
E('l17', 'screens[4].explain.text', 667); E('l17', 'screens[4].explain.text', 61); E('l17', 'screens[4].explain.text', 0.9409)
rr = np.random.default_rng(4); R_, n_ = 4000, 2000; Xa = np.empty((R_, n_)); Xa[:, 0] = rr.standard_normal(R_); Zs = rr.standard_normal((R_, n_))
for t in range(1, n_):
    Xa[:, t] = 0.9 * Xa[:, t - 1] + math.sqrt(0.19) * Zs[:, t]
infl = Xa.mean(1).var() * n_; agree(infl, 19 - 2 * 0.9 * (1 - 0.9 ** n_) / (n_ * 0.01), 0.7, 'inflation sim vs finite-n exact'); E('l17', 'screens[4].prose', round(infl, 1))
# centring
Lc = L - L.mean(); Xc = np.column_stack([np.ones(100), Lc])
gc = grid(np.linspace(-6, 2, 1201), np.linspace(-2, 28, 1361), Lc); gc2 = grid(np.linspace(-7, 3, 1001), np.linspace(-4, 30, 1201), Lc)
agree(gc[:5], gc2[:5], 3e-3, 'centred grid, two meshes'); E('l17', 'screens[5].prose', round(gc[4], 3)); E('l17', 'screens[5].prose', round(L.mean(), 4))
mc = np.linalg.inv((Xc.T * (m_ * (1 - m_))) @ Xc); E('l17', 'screens[5].prose', round(mc[0, 1] / math.sqrt(mc[0, 0] * mc[1, 1]), 3)); E('l17', 'screens[5].prose', round(C[0, 1] / math.sqrt(C[0, 0] * C[1, 1]), 3))
starts = [(-10, 0), (5, 25), (-10, 25), (5, 0)]
rows_out = {}
for name, XX, step in [('uncentred', X, 1.0), ('centred', Xc, np.array([0.8, 3.5]))]:
    chs = np.array([metropolis(lambda bb_, XX=XX: lpl(bb_, XX), s0, step, 5000, k_ + 1)[0][1000:] for k_, s0 in enumerate(starts)])
    rows_out[name] = ([rhat(chs[:, :, j]) for j in range(2)], [split_rhat(chs[:, :, j]) for j in range(2)], [sum(ess_ar1(cc[:, j]) for cc in chs) for j in range(2)], chs.reshape(-1, 2).mean(0))
    line = lv.text('l17', 'screens[5].canvas.params.lines[1]' if name == 'uncentred' else 'screens[5].canvas.params.lines[2]')
    for v in rows_out[name][0] + rows_out[name][1]:
        E('l17', 'screens[5].canvas.params.lines[1]' if name == 'uncentred' else 'screens[5].canvas.params.lines[2]', f'{v:.4f}')
    for v in rows_out[name][2]:
        E('l17', 'screens[5].canvas.params.lines[1]' if name == 'uncentred' else 'screens[5].canvas.params.lines[2]', str(int(round(v))))
ratio = round(rows_out['centred'][2][1]) / round(rows_out['uncentred'][2][1])
E('l17', 'screens[5].widget.answer', round(ratio, 2)); E('l17', 'screens[5].widget.wrong[0].value', round(round(rows_out['centred'][2][0]) / round(rows_out['uncentred'][2][0]), 2)); E('l17', 'screens[5].widget.wrong[1].value', round(1 / ratio, 3))
E('l17', 'screens[5].explain.text', round(rows_out['uncentred'][1][0], 4)); E('l17', 'screens[5].explain.text', round(rows_out['centred'][1][0], 4))
E('l17', 'screens[9].explain.text', f"{rows_out['centred'][0][0]:.4f}"); E('l17', 'screens[9].explain.text', f"{rows_out['centred'][0][1]:.4f}")
agree(rows_out['centred'][3], gc[:2], 0.25, 'centred chain means vs grid (test tolerance)')
agree(np.abs(rows_out['centred'][3] - np.array(gc[:2])).max(), 0.08, 0.005, 'within 0.08 of grid')
E('l17', 'screens[9].widget.tests[3].expect', round(gc[0], 3)); E('l17', 'screens[9].widget.tests[3].expect', round(gc[1], 3))
# trend case and planted chains
rr = np.random.default_rng(3); tr = np.linspace(0, 3, 1000) + rr.standard_normal((4, 1000))
E('l17', 'screens[6].prose', round(rhat(tr), 4)); E('l17', 'screens[6].prose', round(split_rhat(tr), 4)); E('l17', 'summary.trap', round(split_rhat(tr), 4))
c5 = np.random.default_rng(5).standard_normal((4, 1000)); E('l17', 'screens[8].explain.text', round(rhat(c5), 6)); c5[0] -= 1; c5[3] += 1; E('l17', 'screens[8].explain.text', round(rhat(c5), 6))
E('l17', 'quiz[0].widget.answer', round(math.sqrt((0.998 * 2 + 0.1) / 2), 4)); E('l17', 'quiz[0].widget.wrong[0].value', round((0.998 * 2 + 0.1) / 2, 4))
E('l17', 'quiz[2].widget.answer', 4000 * 0.4 / 1.6)
# series caption via the engine's rng
js = r"""
const fs=require('fs');global.window={};eval(fs.readFileSync(process.argv[1]+'/app/js/engine/sim.js','utf8'));const Z=window.ZQ;
const N=(n,s)=>{const r=Z.sim.rng(s),o=[];for(let i=0;i<n;i++){let u=0;while(u<=1e-12)u=r();o.push(Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*r()));}return o;};
const A=(p,n,s,g,x0)=>{let x=x0;return N(n,s).map(z=>(x=p*x+g*z));};
const R=(rho,w)=>{const p=rho*rho,g=Math.sqrt(1-p*p);const c=[[11,-4],[12,-1],[13,2],[14,5]].map(([s,x0])=>A(p,200,s,g,x0).slice(200-w));
const m=c.map(a=>a.reduce((s,x)=>s+x,0)/w),v=c.map((a,k)=>a.reduce((s,x)=>s+(x-m[k])**2,0)/(w-1));const W=v.reduce((s,x)=>s+x,0)/4,mb=m.reduce((s,x)=>s+x,0)/4;
const B=w*m.reduce((s,x)=>s+(x-mb)**2,0)/3;return Math.sqrt(((w-1)/w*W+B/w)/W);};
console.log(JSON.stringify([R(0.97,100),R(0.3,100),R(0.3,200),R(0.97,200)]));
"""
root = os.path.join(HERE, '..', '..')
cap = json.loads(subprocess.run(['node', '-e', js, os.path.abspath(root)], capture_output=True, text=True, check=True).stdout)
E('l17', 'screens[0].widget.answer', round(cap[0], 4)); E('l17', 'screens[0].widget.wrong[0].value', round(cap[1], 3)); E('l17', 'screens[0].explain.text', round(cap[1], 3))
print('series caption R-hat: rho 0.97 w 100 =', round(cap[0], 4), '; rho 0.3 w 100 =', round(cap[1], 4), '; rho 0.3 w 200 =', round(cap[2], 4), '; rho 0.97 w 200 =', round(cap[3], 4))

# ---------------------------------------------------------------- l18 hierarchical
n = np.array([20, 35, 50, 60, 80, 100, 120, 150, 200, 250, 300, 400]); rr = np.random.default_rng(97); p = rr.beta(52, 48, 12); k = rr.binomial(n, p)
agree(k, [12, 16, 35, 34, 39, 45, 60, 60, 117, 142, 206, 205], 0, 'hit-rate wins')
nll = lambda t: -np.sum(special.betaln(k + np.exp(t[0]), n - k + np.exp(t[1])) - special.betaln(np.exp(t[0]), np.exp(t[1])))
r1 = np.exp(optimize.minimize(nll, [0, 0], method='Nelder-Mead', options={'xatol': 1e-10, 'fatol': 1e-12, 'maxiter': 20000}).x)
r2 = np.exp(optimize.minimize(lambda t: -stats.betabinom.logpmf(k, n, *np.exp(t)).sum(), [0, 0], method='L-BFGS-B').x)
agree(r1, r2, 5e-3, 'EB two optimisers'); a_, b_ = r1; kap = a_ + b_
E('l18', 'screens[1].prose', round(a_, 2)); E('l18', 'screens[1].prose', round(b_, 2)); E('l18', 'screens[1].prose', round(kap, 2))
E('l18', 'screens[1].widget.answer', round(20 / (20 + kap), 3)); E('l18', 'screens[1].widget.wrong[0].value', round(kap / (20 + kap), 3)); E('l18', 'screens[1].widget.wrong[1].value', round(20 / (20 + a_), 4))
E('l18', 'screens[1].explain.text', round(400 / (400 + kap), 3))
E('l18', 'screens[2].prose', round(a_ / kap, 4)); E('l18', 'screens[2].prose', round(k.sum() / n.sum(), 4))
sh = (k + a_) / (n + kap); E('l18', 'screens[2].widget.answer', round(sh[2], 4)); E('l18', 'screens[2].explain.text', round((35 + 23.31) / 93.02, 3)); E('l18', 'screens[2].widget.wrong[1].value', round((35 + k.sum() / n.sum() * kap) / (50 + kap), 4))
agree(sh[2], (50 / (50 + kap)) * 0.7 + (kap / (50 + kap)) * a_ / kap, 1e-12, 'shrunk as weighted average'); E('l18', 'screens[2].explain.text', round(50 / (50 + kap), 4)); E('l18', 'screens[2].explain.text', round(kap / (50 + kap), 4))
mr, ms = np.mean((k / n - p) ** 2), np.mean((sh - p) ** 2)
E('l18', 'screens[3].prose', round(mr, 5)); E('l18', 'screens[3].prose', round(ms, 5)); E('l18', 'screens[3].widget.answer', round(mr / ms, 2)); E('l18', 'screens[3].widget.wrong[0].value', round(ms / mr, 2))
k43 = lambda j: (k[j] + 0.5417 * 43) / (n[j] + 43)
E('l18', 'screens[0].widget.options[0].text', round(k43(10), 3)); E('l18', 'screens[0].widget.options[1].why', round(k43(2), 3)); E('l18', 'screens[0].widget.options[2].why', round(k43(0), 3))
E('l18', 'screens[0].widget.options[2].why', round(20 / 63, 2)); E('l18', 'screens[0].explain.text', round(k[10] / n[10], 3))
# alphas
se = np.array([1.5, 2.0, 2.0, 2.5, 3.0, 3.0, 3.5, 4.0, 4.5, 5.0]); rr = np.random.default_rng(102); at = rr.normal(1.0, 2.0, 10); ah = np.round(at + se * rr.standard_normal(10), 2)
agree(ah, [5.08, 2.43, 2.32, -2.67, -1.29, 5.71, -0.79, -0.17, 0.52, 12.26], 1e-9, 'a_hat')
nlN = lambda t, a=ah: 0.5 * np.sum(np.log(se ** 2 + np.exp(2 * t[1])) + (a - t[0]) ** 2 / (se ** 2 + np.exp(2 * t[1])))
rN = optimize.minimize(nlN, [0, 0], method='Nelder-Mead', options={'xatol': 1e-10, 'fatol': 1e-12, 'maxiter': 20000}); mu_, tau_ = rN.x[0], math.exp(rN.x[1])
ts = np.linspace(0, 10, 100001); prof = []
for t in ts:
    v = se ** 2 + t * t; mm = np.sum(ah / v) / np.sum(1 / v); prof.append((0.5 * np.sum(np.log(v) + (ah - mm) ** 2 / v), t, mm))
best = min(prof); agree([mu_, tau_], [best[2], best[1]], 2e-4, 'mu tau NM vs profile')
B = se ** 2 / (se ** 2 + tau_ ** 2); post = mu_ + (1 - B) * (ah - mu_)
E('l18', 'screens[4].prose', round(mu_, 4)); E('l18', 'screens[4].prose', round(tau_, 4)); E('l18', 'screens[4].widget.answer', round(post[9], 2)); E('l18', 'screens[4].widget.wrong[1].value', round(mu_ + B[9] * (ah[9] - mu_), 2))
E('l18', 'screens[4].explain.text', round(B[9], 4)); E('l18', 'screens[4].explain.text', round(B[0], 4)); E('l18', 'screens[4].explain.text', round(post[0], 2)); E('l18', 'screens[4].explain.text', round(ah[9] - mu_, 2))
E('l18', 'screens[4].widget.accept', round(1 - B[9], 3)); E('l18', 'screens[4].hints[0].text', round(tau_ ** 2, 4)); E('l15', 'screens[5].widget.wrong[1].value', round(200 * math.exp(-882 / 200.1), 3)); E('l18', 'screens[4].hints[2].text', round((1 - B[9]) * (ah[9] - mu_), 3))
E('l18', 'screens[5].explain.text', round(post[9], 2)); E('l18', 'screens[5].explain.text', round(post[0], 2)); E('l18', 'screens[5].explain.text', round(np.mean((ah - at) ** 2), 2)); E('l18', 'screens[5].explain.text', round(np.mean((post - at) ** 2), 2))
agree(int(np.argmax(post)), 0, 0, 'fund 1 tops after shrinkage')
E('l18', 'screens[6].explain.text', round(B[0], 4)); E('l18', 'screens[6].explain.text', round(B[9], 4)); E('l18', 'screens[7].explain.text', round(25 + tau_ ** 2, 2)); E('l18', 'screens[7].explain.text', round(B[9], 3))
rr = np.random.default_rng(101); at2 = rr.normal(0.5, 1.0, 10); ah2 = np.round(at2 + se * rr.standard_normal(10), 2)
r101 = optimize.minimize(nlN, [0, 0], args=(ah2,), method='Nelder-Mead', options={'xatol': 1e-10, 'fatol': 1e-12, 'maxiter': 20000})
pool101 = np.sum(ah2 / se ** 2) / np.sum(1 / se ** 2); agree(r101.x[0], pool101, 1e-4, 'seed 101 mu = precision-weighted mean'); agree(math.exp(r101.x[1]) < 0.01, True, 0, 'seed 101 tau to 0')
E('l18', 'screens[8].prose', round(pool101, 2)); E('l18', 'screens[9].explain.text', round(pool101, 2))
E('l18', 'quiz[0].widget.answer', round(9 / 13, 4)); E('l18', 'quiz[0].widget.wrong[0].value', round(4 / 13, 4)); E('l18', 'quiz[1].widget.answer', round((30 + 23.31) / (50 + 43.02), 4)); agree((30 + a_) / (50 + kap), 0.5731, 0.0005, 'quiz shrunk unrounded')
E('l18', 'quiz[2].explain.text', round((12 + a_) / (20 + kap), 3)); E('l18', 'quiz[2].explain.text', round((240 + a_) / (400 + kap), 3))

# ---------------------------------------------------------------- review-4 and homework-4
E('review', 'items[0].widget.answer', 15 / 40); E('review', 'items[1].widget.answer', 22 / 5); E('review', 'items[1].widget.wrong[1].value', 22 / 2)
E('review', 'items[2].widget.answer', round(10 * .3 * .7 * (1 + 9 / 101), 4)); agree(stats.betabinom(10, 30, 70).var(), 2.1 * 110 / 101, 1e-12, 'review bb var')
ratio = math.exp(-(1.4 ** 2 - 1) / 2); agree(ratio, stats.norm.pdf(1.4) / stats.norm.pdf(1.0), 1e-12, 'review ratio'); E('review', 'items[3].widget.accept', round(ratio, 4))
vr = 0.999 * 1.5 + 12 / 1000; E('review', 'items[4].widget.answer', round(math.sqrt(vr / 1.5), 4)); E('review', 'items[4].widget.wrong[0].value', round(vr / 1.5, 3)); E('review', 'items[4].widget.wrong[1].value', round(math.sqrt(12 / 1.5), 4))
E('review', 'items[5].widget.answer', 9000 * 0.2 / 1.8); E('review', 'items[6].widget.answer', round(1 + (1 - 16 / 25) * 8, 2)); E('review', 'items[6].widget.wrong[0].value', round(1 + 0.64 * 8, 2))
E('review', 'items[8].explain.text', round((14 + a_) / (20 + kap), 3)); E('review', 'items[8].explain.text', round((270 + a_) / (400 + kap), 3)); E('review', 'items[8].widget.options[0].text', round((270 + a_) / (400 + kap), 3))
e3 = 15 * 16 * 17 / (50 * 51 * 52); agree(e3, (np.random.default_rng(5).beta(15, 35, 2_000_000) ** 3).mean(), 2e-4, 'E p^3'); E('homework', 'items[2].widget.answer', round(e3, 5))
mm3 = np.array([0.1, 0.3, -0.4]); Wt = np.mean([1.0, 1.2, 0.8]); Bt = 200 * mm3.var(ddof=1); vt = 199 / 200 * Wt + Bt / 200
E('homework', 'items[3].widget.answer', round(math.sqrt(vt / Wt), 4)); E('homework', 'items[3].widget.wrong[0].value', round(vt / Wt, 4)); E('homework', 'items[3].widget.wrong[1].value', round(math.sqrt((199 / 200 * Wt + 200 * mm3.var() / 200) / Wt), 4))
nmin = next(m for m in range(1, 1000) if (0.7 * m + 23.31) / (m + 43.02) > 0.65); E('homework', 'items[4].widget.answer', nmin); E('homework', 'items[4].feedback.byKey.floor', round((0.7 * 93 + 23.31) / (93 + 43.02), 5))
psd = (1 / 25 + 1 / 1.6943 ** 2) ** -0.5; agree(psd, (1 / 25 + 1 / tau_ ** 2) ** -0.5, 1e-4, 'post sd rounded tau'); E('homework', 'items[6].widget.answer', round(psd, 4)); E('homework', 'items[6].widget.wrong[0].value', round(psd ** 2, 3)); E('homework', 'items[6].explain.text', round(1 / 25 + 1 / 1.6943 ** 2, 5)); E('homework', 'items[6].explain.text', round(1 / 1.6943 ** 2, 5))
sys.path.insert(0, HERE)

# ---------------------------------------------------------------- wrong-value bands (rule 581) and code widgets


def walk(o):
    if isinstance(o, dict):
        yield o
        for v in o.values():
            yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)


nb_w = 0
for fid, doc in lv.files.items():
    for node in walk(doc):
        if node.get('kind') == 'numeric' and 'answer' in node:
            ta = node['tol'].get('abs', 0)
            for wr in node.get('wrong', []):
                nb_w += 1
                if not abs(wr['value'] - node['answer']) > ta + wr['tol'].get('abs', 0):
                    BAD.append(f'{fid} wrong {wr["id"]} inside band'); print('BAD band', fid, wr)
        if node.get('edit') and 'answer' in node:
            for wr in node.get('wrong', []):
                nb_w += 1
                if not abs(wr['value'] - node['answer']) > node['tol']['abs'] + wr['tol']['abs']:
                    BAD.append(f'{fid} cell wrong {wr["id"]} inside band')
print(f'ok  {nb_w} wrong values checked against their answer bands')


def close(a, b, tol):
    if isinstance(a, np.ndarray):
        a = a.tolist()
    if isinstance(b, np.ndarray):
        b = b.tolist()
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(close(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, bool) or isinstance(b, bool):
        return a == b
    ra, aa = (tol or {}).get('rel', 0 if tol else 1e-9), (tol or {}).get('abs', 0 if tol else 1e-12)
    return math.isclose(float(a), float(b), rel_tol=ra, abs_tol=aa)


def run_case(src, t):
    ns = {}
    try:
        exec(src, ns)
        exec('import numpy as np', ns)
        if t.get('setup'):
            exec(t['setup'], ns)
        got = eval(t['call'], ns); want = eval(t['expect'], ns)
        if t.get('compare') == 'equal':
            return got == want if not isinstance(got, np.ndarray) else got.tolist() == want
        return close(got, want, t.get('tol'))
    except Exception:
        return False


# ---------------------------------------------------------------- fix pass (second reader's rulings)
def geyer_ess(x_):
    """Effective sample size by Geyer's initial positive sequence (pairs of autocorrelations while positive)."""
    x_ = np.asarray(x_, float) - np.mean(x_); n0 = len(x_); f_ = np.fft.rfft(x_, 2 * n0); ac = np.fft.irfft(f_ * np.conj(f_))[:n0]; ac /= ac[0]; tot = -1.0
    for k_ in range(0, n0 - 1, 2):
        g_ = ac[k_] + ac[k_ + 1]
        if g_ < 0:
            break
        tot += 2 * g_
    return n0 / tot


# l16 quiz[2]: beta1 ESS by step, six seeds, 18,000 draws after 2,000 burn-in, start (-8, 12.8)
mean_ess = {}
for s_ in (0.05, 0.5, 1.0, 5.0, 2.5):
    mean_ess[s_] = float(np.mean([geyer_ess(metropolis(lpl, [-8, 12.8], s_, 20000, sd_)[0][2000:, 1]) for sd_ in range(1, 7)]))
print('mean beta1 ESS by step (Geyer):', {k_: round(v_) for k_, v_ in mean_ess.items()})
agree([mean_ess[0.05], mean_ess[1.0], mean_ess[5.0], mean_ess[2.5]], [7, 152, 291, 338], [3, 15, 15, 15], 'l16 quiz[2] ESS by step')
agree(mean_ess[0.5], 65, 8, 'l16 quiz[2] ESS at 0.5')
if not (mean_ess[0.05] < mean_ess[0.5] < mean_ess[1.0] < mean_ess[5.0] < mean_ess[2.5]):
    BAD.append('l16 step ranking')
for txt_ in ('about 7 effective', '65 at 0.5', '150 at 1.0', '290 at 5'):
    assert txt_ in lv.text('l16', 'quiz[2].explain.text'), txt_
E('l16', 'quiz[2].widget.options[1].why', 7); E('l16', 'quiz[2].widget.options[2].why', 290); E('l16', 'quiz[2].widget.options[2].why', 340)
# l16 screens[9]: Monte Carlo standard errors of the seed-1 chain by Geyer (0.15 and 0.23)
mcse = [float(ch1[2000:, j_].std() / math.sqrt(geyer_ess(ch1[2000:, j_]))) for j_ in range(2)]
agree(np.round(mcse, 2), [0.15, 0.23], 1e-9, 'l16 MCSE by Geyer')
E('l16', 'screens[9].widget.how', 0.15); E('l16', 'screens[9].widget.how', 0.23)
# l17: centring alone at step 1.0 (starts and seeds as the screen) gives beta1 ESS 217 by the lag-1 rule
chc = np.array([metropolis(lambda bb_: lpl(bb_, Xc), s0, 1.0, 5000, k_ + 1)[0][1000:] for k_, s0 in enumerate(starts)])
agree(round(sum(ess_ar1(cc[:, 1]) for cc in chc)), 217, 1, 'l17 centred at step 1.0, beta1 ESS (lag-1)')
E('l17', 'screens[5].feedback.correct', 217)
# l17 quiz[0] nob: leaving out B gives sqrt(0.998 * 2 / 2) = 0.9990
agree(round(math.sqrt(0.998), 4), 0.999, 1e-9, 'nob'); E('l17', 'quiz[0].widget.wrong[1].value', 0.999)
# l18 quiz[1] and hint
agree([round(53.31 / 93.02, 4), round((206 + 0.5417 * 43) / 343, 3)], [0.5731, 0.668], 1e-9, 'l18 0.5731 and 0.668')
E('l18', 'quiz[1].feedback.correct', 0.5731); E('l18', 'screens[0].hints[2].text', 0.668)


ncode = 0
for fid, doc in lv.files.items():
    for node in walk(doc):
        if node.get('kind') == 'code':
            ncode += 1
            for i, t in enumerate(node['tests'] + node.get('examples', [])):
                if not run_case(node['solution'], t):
                    BAD.append(f'{fid} solution fails test {i}'); print('BAD solution', fid, i, t['call'][:60])
            for i, t in enumerate(node['tests']):
                if run_case(node['starter'], t):
                    BAD.append(f'{fid} starter passes test {i}'); print('BAD starter passes', fid, i, t['call'][:60])
print(f'ok  {ncode} code widgets: every solution passes, every starter fails' if not [b_ for b_ in BAD if 'solution' in b_ or 'starter' in b_] else 'BAD code widgets')

if BAD:
    print('agreement or harness failures:', BAD)
lv.report() if not BAD else (lv.report(), sys.exit(1))
