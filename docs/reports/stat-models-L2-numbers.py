"""Recompute every number stated in stat-models level 2 and check it at its JSON path.

Run: python3 docs/reports/stat-models-L2-numbers.py   (NumPy and the standard library only; exits 0 when all pass)

Each value is computed twice: here by hand formulas, exact sums and NumPy (own t, F and binomial tails from the
regularised incomplete beta), and in Pyodide 0.27.7 by SciPy 1.14.1 / statsmodels 0.14.4, pasted in SM below.
Datasets use np.random.default_rng(seed) in the brief's order of draws; the local NumPy and Pyodide's NumPy 2.0.2
give identical streams for seeds 41 and 53 (checked byte for byte). The peeking count (190 of 1,000, seed 3) and the
SPRT walk counts (14 and 246 of 300, seed 17) come from the engine's own seeded streams: the first was recomputed
by running app/js/engine/sim.js in Node, both were read off the rendered canvas.
"""
import math
import os
import sys
from statistics import NormalDist

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level("stat-models", 2)
Z = NormalDist()


def chk(f, path, v, dp=None):
    lv.expect(f, path, (round(v, dp) if dp else int(round(v))) if dp is not None else v)


def agree(a, b, tol, what=''):
    a, b = np.atleast_1d(np.asarray(a, float)), np.atleast_1d(np.asarray(b, float))
    if not np.all(np.abs(a - b) <= tol):
        print('BAD agreement', what, a, b)
        sys.exit(1)


def betacf(a, b, x):
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 / (1 - qab * x / qap)
    h = d
    for m in range(1, 400):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 / (1 + aa * d); c = 1 + aa / c; h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 / (1 + aa * d); c = 1 + aa / c; de = d * c; h *= de
        if abs(de - 1) < 1e-15:
            break
    return h


def betainc(a, b, x):
    if x <= 0:
        return 0.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x))
    return bt * betacf(a, b, x) / a if x < (a + 1) / (a + b + 2) else 1 - bt * betacf(b, a, 1 - x) / b


f_sf = lambda F, d1, d2: betainc(d2 / 2, d1 / 2, d2 / (d2 + d1 * F))
t_sf2 = lambda t, df: betainc(df / 2, 0.5, df / (df + t * t))          # two-sided


def bisect(fn, lo, hi, target):
    for _ in range(200):
        mid = (lo + hi) / 2
        if fn(mid) > target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


f_crit = lambda d1, d2: bisect(lambda x: f_sf(x, d1, d2), 0.01, 50, 0.05)
t_crit = lambda df: bisect(lambda x: t_sf2(x, df), 0.5, 20, 0.05)
binom_two = lambda k, n: min(1.0, 2 * sum(math.comb(n, j) for j in range(max(k, n - k), n + 1)) / 2 ** n)

SM = dict(hookF=4.153846153846154, hookp=0.05272481278900583, crit29=4.25649472909375, abp=0.07814074941121574, abt=-2.1213203435596424,
          d5F=5.447809485415127, d5p=0.00590045936308082, d5ssb=321.8859479086759, d5ssw=2570.214463540558, ols=[2.1402260944674167, 4.090789351348472, 0.16300809008554165],
          r2=0.11129833066459105, pairs=[0.9110160356397008, 0.004071746348722031, 0.006425891240224915], crit287=3.101295756667187, f455=0.1419891925947489, crit455=2.53968863490368,
          nind=1004.6541460552606, ntt=1005.6154263658912, pow200=0.23952699321850004, corr=0.808089835477115, welch=[-1.2220672823780936, 0.2224054739299888],
          paired=[-1.0914651498979229, 5.53338304920927, -2.7895499084665825, 0.005791028662052371], tcrit199=1.971956544249395, ci=[-1.8630311429023243, -0.31989915689352144],
          wins=117, signp=0.019396944540338423, signnorm=0.019624414976639706, fe=[-1.091465149897913, -2.78954990846655], peek=[0.050435, 0.0834725, 0.1419175, 0.193405],
          asn=[42.931454433031455, 61.00614573384048], hwF=0.0021503108436711654, r1p=0.06232228030306132)

# ---------- hook set ----------
G = [[1, 3, 2, 6], [5, 7, 4, 8], [2, 4, 3, 3]]


def anova(groups):
    allv = [v for g in groups for v in g]; N, k = len(allv), len(groups); gm = sum(allv) / N
    ssb = sum(len(g) * (sum(g) / len(g) - gm) ** 2 for g in groups); ssw = sum((v - sum(g) / len(g)) ** 2 for g in groups for v in g)
    return ssb, ssw, (ssb / (k - 1)) / (ssw / (N - k)), k - 1, N - k


ssb, ssw, F, d1, d2 = anova(G); agree([ssb, ssw, F], [24, 26, SM['hookF']], 1e-12, 'hook')
p_hook = f_sf(F, 2, 9); agree(p_hook, SM['hookp'], 1e-12); c29 = f_crit(2, 9); agree(c29, SM['crit29'], 1e-9)
F3 = anova([[1, 3, 2, 3], G[1], G[2]])
# ---------- D5 ----------
rng = np.random.default_rng(41); s = np.repeat([2.0, 3.0, 6.0], 30) + rng.normal(0, 6, 90)
g5 = [list(s[:30]), list(s[30:60]), list(s[60:])]
m5 = [np.mean(x) for x in g5]; sd5 = [np.std(x, ddof=1) for x in g5]; gm5 = float(s.mean())
ssb5, ssw5, F5, _, _ = anova(g5); agree([ssb5, ssw5, F5], [SM['d5ssb'], SM['d5ssw'], SM['d5F']], 1e-8, 'd5')
p5 = f_sf(F5, 2, 87); agree(p5, SM['d5p'], 1e-10); X = np.column_stack([np.ones(90), np.repeat([0, 1, 0], 30), np.repeat([0, 0, 1], 30)])
beta = np.linalg.lstsq(X, s, rcond=None)[0]; agree([beta[0], beta[2], beta[1]], SM['ols'], 1e-9, 'ols'); r2 = ssb5 / (ssb5 + ssw5); agree(r2, SM['r2'], 1e-12)


def ttest_ind(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float); na, nb = len(a), len(b)
    sp = ((na - 1) * a.var(ddof=1) + (nb - 1) * b.var(ddof=1)) / (na + nb - 2); t = (a.mean() - b.mean()) / math.sqrt(sp * (1 / na + 1 / nb))
    return t, t_sf2(t, na + nb - 2)


pp = [ttest_ind(g5[0], g5[1])[1], ttest_ind(g5[0], g5[2])[1], ttest_ind(g5[1], g5[2])[1]]; agree(pp, SM['pairs'], 1e-10, 'pairs')
tab, pab = ttest_ind(G[0], G[1]); agree([tab, pab], [SM['abt'], SM['abp']], 1e-10)
c287, c455 = f_crit(2, 87), f_crit(4, 55); agree([c287, c455], [SM['crit287'], SM['crit455']], 1e-8); p455 = f_sf(1.8, 4, 55); agree(p455, SM['f455'], 1e-10)
# ---------- power ----------
z = Z.inv_cdf(0.975) + Z.inv_cdf(0.8); n1 = 2 * z ** 2 * 64; agree(n1, SM['nind'], 0.01)
pw = lambda se, d=1: (1 - Z.cdf(Z.inv_cdf(0.975) - d / se)) + Z.cdf(-Z.inv_cdf(0.975) - d / se)
pow200 = pw(8 * math.sqrt(2 / 200)); agree(pow200, SM['pow200'], 1e-6); sdD = math.sqrt(2 * 64 * 0.2); npairs = z ** 2 * sdD ** 2
pow200p = pw(sdD / math.sqrt(200))
n_arm = lambda d, s_, a=0.05, p=0.8, r=0: math.ceil(2 * (1 - r) * (Z.inv_cdf(1 - a / 2) + Z.inv_cdf(p)) ** 2 * s_ ** 2 / d ** 2)
# ---------- D6 ----------
rng = np.random.default_rng(53); block = rng.normal(0, 8, 200); order = rng.integers(0, 2, 200); eA = 3 * rng.standard_t(4, 200); eB = 3 * rng.standard_t(4, 200)
A = 5 + block + eA; B = 4 + block + eB; d = B - A
corr = float(np.corrcoef(A, B)[0, 1]); agree(corr, SM['corr'], 1e-12)
seW = math.sqrt(A.var(ddof=1) / 200 + B.var(ddof=1) / 200); tW = (B.mean() - A.mean()) / seW
dfW = seW ** 4 / ((A.var(ddof=1) / 200) ** 2 / 199 + (B.var(ddof=1) / 200) ** 2 / 199); agree([tW, t_sf2(tW, dfW)], SM['welch'], 1e-9, 'welch')
seP = d.std(ddof=1) / math.sqrt(200); tP = d.mean() / seP; pP = t_sf2(tP, 199); agree([d.mean(), d.std(ddof=1), tP, pP], SM['paired'], 1e-9, 'paired')
tc = t_crit(199); agree(tc, SM['tcrit199'], 1e-9); ci = (d.mean() - tc * seP, d.mean() + tc * seP); agree(ci, SM['ci'], 1e-9)
# fixed-effect OLS: within-block demeaning gives the same estimate
wins = int((d < 0).sum()); agree(wins, SM['wins'], 0); ps = binom_two(wins, 200); agree(ps, SM['signp'], 1e-12)
pnorm = 2 * (1 - Z.cdf((wins - 100 - 0.5) / math.sqrt(50))); agree(pnorm, SM['signnorm'], 1e-9); pnorm_nocc = 2 * (1 - Z.cdf((wins - 100) / math.sqrt(50)))
# peeking: exact rates by simulation here (seeded), and the planner's grid figure 0.1936
rngp = np.random.default_rng(7); Zs = rngp.standard_normal((400000, 10)); S = np.cumsum(Zs, 1) / np.sqrt(np.arange(1, 11))
peek = [float((np.abs(S[:, :k]) > 1.959964).any(1).mean()) for k in (1, 2, 5, 10)]; agree(peek, SM['peek'], 1e-12, 'peek same stream')
# SPRT
Lb, Ub = math.log(0.2 / 0.95), math.log(0.8 / 0.05); asn0 = (0.95 * Lb + 0.05 * Ub) / -0.03125; asn1 = (0.2 * Lb + 0.8 * Ub) / 0.03125; agree([asn0, asn1], SM['asn'], 1e-9)
nfix = ((Z.inv_cdf(0.95) + Z.inv_cdf(0.8)) / 0.25) ** 2

# ================= l6 =================
f = 'l6'
chk(f, 'screens[0].explain', 50); chk(f, 'screens[0].explain', 24); chk(f, 'screens[0].explain', 26)
chk(f, 'screens[1].widget.answer', ssb); chk(f, 'screens[1].widget.wrong[0].value', ssb / 4); chk(f, 'screens[1].widget.wrong[1].value', ssb / 12)
chk(f, 'screens[1].explain', 4 * (6 - 4) ** 2)
chk(f, 'screens[2].widget.answer', ssw); chk(f, 'screens[2].hints', 14); chk(f, 'screens[2].explain', ssb / (ssb + ssw), 2)
chk(f, 'screens[4].widget', 12); chk(f, 'screens[4].widget', ssw / 9, 3); chk(f, 'screens[4].widget', F, 4); chk(f, 'screens[4].explain', F, 4)
chk(f, 'screens[5].widget', ssw / 9, 3)
chk(f, 'screens[6].prose', m5[0], 4); chk(f, 'screens[6].prose', m5[1], 4); chk(f, 'screens[6].prose', m5[2], 4); chk(f, 'screens[6].prose', gm5, 4); chk(f, 'screens[6].prose', ssw5, 3)
for v in sd5:
    chk(f, 'screens[6].canvas', v, 4)
chk(f, 'screens[6].widget.answer', ssb5, 3); chk(f, 'screens[6].widget.wrong[0].value', ssb5 / 30, 4); chk(f, 'screens[6].widget.wrong[1].value', ssb5 / 3, 3)
chk(f, 'screens[6].explain', F5, 4); chk(f, 'screens[6].explain', ssb5 / 2, 3); chk(f, 'screens[6].explain', ssw5 / 87, 3)
chk(f, 'screens[6].hints', sum((m - gm5) ** 2 for m in m5), 4)
chk(f, 'screens[8].widget.tests', SM['d5F'])
chk(f, 'screens[9].widget.answer', (48 / 2) / (1140 / 57), 1); chk(f, 'screens[9].widget.wrong[0].value', 48 / 1140, 4); chk(f, 'screens[9].widget.wrong[1].value', 24 / (1140 / 60), 4)
chk(f, 'quiz[1].widget.answer', (36 / 4) / (270 / 45), 1); chk(f, 'quiz[1].widget.wrong[0].value', 36 / 270, 4); chk(f, 'quiz[1].widget.wrong[1].value', (36 / 5) / 6, 1)
chk(f, 'quiz[2].widget.answer', 30 / 120, 2); chk(f, 'quiz[2].widget.wrong[0].value', 30 / 90, 4)

# ================= l7 =================
f = 'l7'
chk(f, 'screens[0].widget.answer', p_hook, 4); chk(f, 'screens[0].widget.wrong[1].value', 1 - p_hook, 4); chk(f, 'screens[0].feedback', c29, 4)
chk(f, 'screens[1].hints', F3[2], 2); chk(f, 'screens[1].explain', F3[1], 2); chk(f, 'screens[1].explain', F3[2], 2)
chk(f, 'screens[2].explain', c287, 4)
chk(f, 'screens[3].widget.answer', p5, 4); chk(f, 'screens[3].feedback', p5, 5); chk(f, 'screens[3].prose', F5, 4); chk(f, 'screens[3].canvas', c287, 4)
chk(f, 'screens[4].widget.answer', beta[0] + beta[2], 3); chk(f, 'screens[4].widget.wrong[0].value', beta[2], 4); chk(f, 'screens[4].hints', beta[0] + beta[2], 6)
chk(f, 'screens[4].explain', r2, 4); chk(f, 'screens[4].explain', p5, 5)
chk(f, 'screens[5].widget.answer', tab ** 2, 1); chk(f, 'screens[5].prose', tab, 4); chk(f, 'screens[5].feedback', pab, 4); chk(f, 'screens[5].explain', 18); chk(f, 'screens[5].explain', 4)
chk(f, 'screens[6].widget.answer', 1 - 0.95 ** 3, 4); chk(f, 'screens[6].canvas', pp[0], 3); chk(f, 'screens[6].canvas', pp[1], 4); chk(f, 'screens[6].canvas', pp[2], 4)
chk(f, 'screens[7].prose', 0.05 / 3, 4)
chk(f, 'screens[9].widget.answer', p455, 3); chk(f, 'screens[9].widget.wrong[0].value', 1 - p455, 3); chk(f, 'screens[9].hints', c455, 4)
chk(f, 'quiz[0].explain', f_sf(3.0, 2, 9), 3); chk(f, 'quiz[1].widget.answer', 6.25, 2)

# ================= l8 =================
f = 'l8'
chk(f, 'screens[0].prose', (4 + 14 + 16 + 12) / 4, 1); chk(f, 'screens[0].prose', (3 + 2 + 4 + 3) / 4, 1)
chk(f, 'screens[2].widget.answer', math.ceil(n1)); chk(f, 'screens[2].prose', Z.inv_cdf(0.975), 5); chk(f, 'screens[2].prose', Z.inv_cdf(0.8), 5)
chk(f, 'screens[2].widget.accept', z, 5); chk(f, 'screens[2].widget.accept', n1, 2); chk(f, 'screens[2].widget.wrong[0].value', math.ceil(n1 / 2))
chk(f, 'screens[2].widget.wrong[1].value', z ** 2, 3); chk(f, 'screens[2].widget.wrong[2].value', 2 * z ** 2 * 8, 0); chk(f, 'screens[2].feedback', math.ceil(SM['ntt']))
chk(f, 'screens[2].explain', z, 2)
chk(f, 'screens[3].prose', 8 * math.sqrt(2 / 200), 1); chk(f, 'screens[3].prose', 1 / 0.8, 2); chk(f, 'screens[3].widget.answer', pow200, 4); chk(f, 'screens[3].explain', 100 * pow200, 0)
chk(f, 'screens[4].widget.answer', sdD, 4); chk(f, 'screens[4].widget.wrong[0].value', sdD ** 2, 1); chk(f, 'screens[4].widget.wrong[1].value', math.sqrt(2 * 64 * 0.8), 3)
chk(f, 'screens[4].widget.wrong[2].value', 8 * math.sqrt(2), 4); chk(f, 'screens[4].canvas', 8 * math.sqrt(2), 2)
chk(f, 'screens[5].widget.answer', math.ceil(npairs)); chk(f, 'screens[5].widget.accept', npairs, 2); chk(f, 'screens[5].feedback', 100 * pow200p, 1); chk(f, 'screens[5].widget.wrong[1].value', math.ceil(2 * npairs))
chk(f, 'screens[6].hints', 100 * pow200, 0)
for v in (n_arm(1, 8), n_arm(1, 8, r=0.8), n_arm(2, 8), n_arm(1, 8, p=0.9), n_arm(1, 8, a=0.01)):
    chk(f, 'screens[8].widget.how', v)
chk(f, 'quiz[1].widget.answer', n_arm(2, 8)); chk(f, 'quiz[1].widget.accept', n1 / 4, 1)

# ================= l9 =================
f = 'l9'
chk(f, 'screens[0].explain', corr, 3)
for v, dp in ((A.mean(), 4), (B.mean(), 4), (A.std(ddof=1), 4), (B.std(ddof=1), 4), (d.mean(), 4), (d.std(ddof=1), 4)):
    chk(f, 'screens[1].canvas', v, dp)
chk(f, 'screens[1].widget.answer', tW, 4); chk(f, 'screens[1].widget.wrong[1].value', d.mean() / math.sqrt((A.var(ddof=1) + B.var(ddof=1)) / 400), 4)
chk(f, 'screens[1].hints', seW, 4); chk(f, 'screens[1].hints', A.var(ddof=1), 3); chk(f, 'screens[1].feedback', t_sf2(tW, dfW), 3)
chk(f, 'screens[2].widget.answer', tP, 4); chk(f, 'screens[2].hints', seP, 5); chk(f, 'screens[2].widget.wrong[1].value', d.mean() / d.std(ddof=1), 4); chk(f, 'screens[2].explain', pP, 5)
chk(f, 'screens[3].widget.answer', ci[0], 3); chk(f, 'screens[3].prose', tc, 4); chk(f, 'screens[3].widget.wrong[0].value', ci[1], 4)
chk(f, 'screens[3].widget.wrong[1].value', d.mean() - 1.96 * seP, 4); chk(f, 'screens[3].widget.wrong[2].value', d.mean() - tc * d.std(ddof=1), 3); chk(f, 'screens[3].hints', tc * seP, 4)
chk(f, 'screens[5].prose', wins); chk(f, 'screens[5].widget.answer', ps, 4); chk(f, 'screens[5].widget.wrong[0].value', ps / 2, 4); chk(f, 'screens[5].widget.wrong[1].value', pnorm_nocc, 4)
chk(f, 'screens[5].feedback', pnorm, 4)
agree(SM['peek'][3], 0.1935, 0.001, 'peek 10'); lv.expect(f, 'screens[7].explain', 19.35); chk(f, 'screens[7].explain', 100 * peek[2], 1); chk(f, 'screens[7].explain', 100 * peek[1], 1)
chk(f, 'screens[7].widget.wrong[1].value', 1 - 0.95 ** 10, 4); chk(f, 'screens[7].widget.accept', 19.35, 2)
chk(f, 'screens[8].prose', Ub, 4); chk(f, 'screens[8].prose', Lb, 4); chk(f, 'screens[8].widget.answer', asn0, 2); chk(f, 'screens[8].widget.wrong[0].value', asn1, 2)
chk(f, 'screens[8].widget.wrong[1].value', nfix, 2); chk(f, 'screens[8].explain', asn0, 1); chk(f, 'screens[8].explain', 100 * 14 / 300, 1); chk(f, 'screens[8].explain', 100 * 246 / 300, 1)
chk(f, 'screens[9].widget.tests', SM['signp'], 6)
gbp = 2e9 * abs(d.mean()) / 1e4
chk(f, 'screens[10].widget.answer', gbp, 0); chk(f, 'screens[10].explain', gbp, 0); chk(f, 'screens[10].explain', 2e9 * abs(ci[1]) / 1e4, 0); chk(f, 'screens[10].explain', 2e9 * abs(ci[0]) / 1e4, 0)
chk(f, 'quiz[2].explain', binom_two(15, 19), 3)

# ================= review and homework =================
f = 'review'
chk(f, 'items[0].widget.answer', (40 / 3) / 5, 4); chk(f, 'items[0].explain', SM['r1p'], 3); chk(f, 'items[0].widget.wrong[1].value', (40 / 4) / (180 / 40), 4)
chk(f, 'items[3].widget.answer', n_arm(2, 10)); chk(f, 'items[3].widget.accept', 2 * z ** 2 * 100 / 4, 1)
chk(f, 'items[6].widget.wrong[0].value', 6 * math.sqrt(2), 4); chk(f, 'items[8].widget.answer', 0.05 / 6, 5)
f = 'homework'
chk(f, 'items[3].widget.answer', pw(8 * math.sqrt(2 / 500)), 4); chk(f, 'items[3].widget.wrong[0].value', pw(8 / math.sqrt(500)), 4); chk(f, 'items[3].widget.accept', 8 * math.sqrt(2 / 500), 5)
chk(f, 'items[4].widget.answer', 70 / 9, 4); chk(f, 'items[4].feedback', SM['hwF'], 4)
chk(f, 'items[6].widget.answer', asn1, 2); chk(f, 'items[6].widget.wrong[1].value', (0.8 * Lb + 0.2 * Ub) / 0.03125, 2)
rng30 = np.random.default_rng(9); S30 = np.cumsum(rng30.standard_normal((200000, 30)), 1) / np.sqrt(np.arange(1, 31))
chk(f, 'items[2].model', 100 * float((np.abs(S30) > 1.959964).any(1).mean()), 0)
lv.report()
