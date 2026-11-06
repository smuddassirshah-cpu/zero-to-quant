"""Second-reader number checks for coint level 1 (l1 to l4, review-1, homework-1).

Every number is recomputed from the course generators (copied from the lesson preludes) with NumPy and statsmodels
in CPython, or from its closed form, then looked up where it is stated (app/tools/numbers_lib.py). statsmodels values
are compared after rounding to the places shown. Claims that are not single numbers use `claim_text(...)`: such a check
fails only while the faulty phrase is still in the content and the fact is false.
A failing check means the content is wrong (see docs/reviews/review-coint.md) and stays failing until fixed.
Run: python3 docs/reports/coint-L1-numbers.py   (about two minutes)
"""
import math, os, sys, warnings
import numpy as np
warnings.filterwarnings('ignore')
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, coint
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level('coint', 1)


def claim(ok, label, note=''):
    return lv._rec(bool(ok), 'claim: ' + label, note)


def claim_text(ref, path, phrase, ok, label, note=''):
    present = phrase in lv.text(ref, path)
    return lv._rec(bool(ok) or not present, f'claim: {ref} {path}: {label}', note + ('' if present else ' (phrase gone)'))


def r(v, k=0):
    return round(float(v), k)


def make_two_walks(seed, n=500):
    z = np.random.default_rng(seed).standard_normal((n, 2))
    return np.cumsum(z[:, 0]), np.cumsum(z[:, 1])


def make_pair(seed, n=1000, alpha=5.0, beta=1.5, phi=0.95, sd_u=0.5, x0=40.0, vol=0.015):
    z = np.random.default_rng(seed).standard_normal((n, 2))
    x = x0 * np.exp(np.cumsum(vol * z[:, 0]))
    u = np.empty(n); u[0] = sd_u * z[0, 1]
    for t in range(1, n):
        u[t] = phi * u[t - 1] + sd_u * z[t, 1]
    return x, alpha + beta * x + u


def make_broken_pair(seed, n=1500, break_at=1000, sd_break=1.0, **kw):
    x, y = make_pair(seed, n, **kw)
    z = np.random.default_rng(seed + 1000).standard_normal(n)
    return x, y + np.concatenate([np.zeros(break_at), np.cumsum(sd_break * z[break_at:])])


def make_case(name, n=1000):
    if name == 'A':
        e = np.random.default_rng(1).standard_normal((n, 2))
        return np.cumsum(e[:, 0]), np.cumsum(0.8 * e[:, 0] + 0.6 * e[:, 1])
    if name == 'B':
        e = np.random.default_rng(2).standard_normal((n, 2))
        x = np.cumsum(e[:, 0]); u = np.empty(n); u[0] = 3 * e[0, 1]
        for t in range(1, n):
            u[t] = 0.5 * u[t - 1] + 3 * e[t, 1]
        return x, x + u
    if name == 'C':
        return make_pair(3, n)
    return make_two_walks(4, n)


def ar_pair(seed, n, phi):
    z = np.random.default_rng(seed).standard_normal((n, 2)); a = np.empty((n, 2)); a[0] = z[0]
    for t in range(1, n):
        a[t] = phi * a[t - 1] + z[t]
    return a[:, 0], a[:, 1]


def abst(x, y):
    q = np.corrcoef(x, y)[0, 1]; n = len(x)
    return abs(q) * math.sqrt((n - 2) / (1 - q * q)), q * q


def ols(y, x):
    return sm.OLS(y, sm.add_constant(x)).fit()


def eg_stat(y, x):
    b, a = np.polyfit(x, y, 1)
    return adfuller(y - a - b * x, maxlag=0, regression='n', autolag=None)[0]


# ---------------- l1 ----------------
A, B = make_two_walks(103)
m = ols(B, A)
lv.expect('l1', 'screens[0].prose', r(m.params[1], 2))
lv.expect('l1', 'screens[0].prose', r(m.rsquared, 2))
lv.expect('l1', 'screens[0].prose', r(m.tvalues[1], 1))
lv.expect('l1', 'screens[4].feedback.correct', r(m.params[1], 4))
lv.expect('l1', 'screens[4].feedback.correct', r(m.tvalues[1], 4))
lv.expect('l1', 'screens[4].feedback.correct', r(m.rsquared, 4))
claim(abs(ols(A, B).rsquared - m.rsquared) < 1e-12, 'l1 swapped regression has the same R^2')
res = m.resid
lv.expect('l1', 'screens[6].prose', r(np.corrcoef(res[1:], res[:-1])[0, 1], 2))
lv.expect('l1', 'screens[6].explain.text', r(np.sum(np.diff(res) ** 2) / np.sum(res ** 2), 2))
md = ols(np.diff(B), np.diff(A))
lv.expect('l1', 'screens[5].feedback.correct', r(md.params[1], 4))
lv.expect('l1', 'screens[5].feedback.correct', r(md.tvalues[1], 2))
lv.expect('l1', 'screens[5].feedback.correct', r(md.rsquared, 4))
lv.expect('l1', 'quiz[3].prose', r(md.tvalues[1], 2))
claim(1e-135 < m.pvalues[1] < 1e-133, 'l1 statsmodels p-value about 1e-134', f'{m.pvalues[1]:.2e}')
T, R2, S = [], [], []
for s in range(1000):
    x, y = make_two_walks(s); t, q2 = abst(x, y); T.append(t); R2.append(q2)
    q = np.corrcoef(x, y)[0, 1]; S.append(q * math.sqrt(498 / (1 - q * q)))
T, R2 = np.array(T), np.array(R2)
lv.expect('l1', 'screens[2].hints[2].text', int((R2 >= 0.7).sum()))
lv.expect('l1', 'screens[2].explain.text', r(np.median(R2), 2))
lv.expect('l1', 'screens[2].explain.text', r(R2.mean(), 2))
lv.expect('l1', 'screens[2].explain.text', r(100 * (R2 > 0.5).mean(), 1))
lv.expect('l1', 'screens[2].widget.options[2].why', r(np.quantile(R2, 0.75), 2))
lv.expect('l1', 'screens[3].explain.text', r(100 * (T > 1.96).mean(), 1))
claim(abs((T > 10).mean() - 0.5) < 0.02, 'l1 half the pairs have |t| > 10', f'{(T > 10).mean()}')
lv.expect('l1', 'screens[8].hints[2].text', int((T >= 34.59).sum()))
lv.expect('l1', 'screens[8].explain.text', int((T >= 34.59).sum()))
lv.expect('l1', 'screens[8].canvas.state.overlay[0].params.sigma', r(np.std(S, ddof=1), 2))
wn = np.mean([abst(*np.random.default_rng(s).standard_normal((500, 2)).T)[0] > 1.96 for s in range(1000)])
lv.expect('l1', 'screens[3].explain.text', r(100 * wn, 1))
lv.expect('l1', 'screens[9].widget.options[2].why', r(100 * wn, 1))
share, medr2 = {}, {}
for n, sims in [(100, 500), (250, 500), (500, 1000), (2000, 500)]:
    tt = [abst(*make_two_walks(s, n)) for s in range(sims)]
    share[n] = np.mean([a > 1.96 for a, _ in tt]); medr2[n] = np.median([b for _, b in tt])
    if n == 2000:
        lv.expect('l1', 'screens[11].canvas.params.rows[1]', r(medr2[n], 2))
        lv.expect('l1', 'screens[11].canvas.params.rows[1]', int(round(np.median([a for a, _ in tt]))))
for n in (100, 250, 500):
    lv.expect('l1', 'quiz[2].explain.text', r(100 * share[n], 1))
lv.expect('l1', 'screens[7].explain.text', r(100 * share[2000], 1))
lv.expect('l1', 'quiz[1].widget.options[2].why', r(100 * share[2000], 1))
note = f'median R^2 {medr2[500]:.3f} at 500 days, {medr2[2000]:.3f} at 2,000'
claim_text('l1', 'screens[7].explain.text', 'so they fit better', medr2[2000] > medr2[500] + 0.05, 'longer walks fit better', note)
claim_text('l1', 'quiz[2].widget.options[1].why', 'so they fit better', medr2[2000] > medr2[500] + 0.05, 'longer walks fit better', note)
xc, yc = make_pair(3, 1000)
lv.expect('l1', 'screens[5].explain.text', int(round(ols(np.diff(yc), np.diff(xc)).tvalues[1])))
lv.expect('l1', 'screens[9].widget.options[3].why', int(round(ols(yc, xc).tvalues[1])))
lv.expect('l1', 'screens[9].hints[1].text', int(round(math.log(0.5) / math.log(0.98))))
lv.expect('l1', 'screens[9].explain.text', r(100 * np.mean([abst(*ar_pair(s, 250, 0.98))[0] > 1.96 for s in range(1000)]), 1))
lv.expect('l1', 'quiz[0].widget.answer', r(0.5 * math.sqrt(498 / 0.75), 2))
lv.expect('l1', 'quiz[0].widget.wrong[0].value', r(0.25 * math.sqrt(664), 2))
lv.expect('l1', 'quiz[0].widget.wrong[1].value', 332)
lv.expect('l1', 'quiz[0].explain.text', r(math.sqrt(664), 2))

# ---------------- l2 ----------------
cases = {k: make_case(k) for k in 'ABCD'}
rc = {k: np.corrcoef(np.diff(x), np.diff(y))[0, 1] for k, (x, y) in cases.items()}
cp = {k: coint(y, x) for k, (x, y) in cases.items()}
for k in 'ABCD':
    lv.expect('l2', 'screens[10].canvas.params.rows', r(rc[k], 4))
lv.expect('l2', 'screens[10].canvas.params.rows', r(cp['A'][1], 2))
lv.expect('l2', 'screens[10].canvas.params.rows', r(cp['C'][1], 4))
lv.expect('l2', 'screens[10].canvas.params.rows', r(cp['D'][1], 2))
claim(r(cp['B'][1], 4) == 0, 'l2 B coint p = 0.0000')
lv.expect('l2', 'screens[10].explain.text', r(cp['A'][1], 2))
lv.expect('l2', 'screens[0].prose', r(rc['A'], 2)); lv.expect('l2', 'screens[0].prose', r(rc['B'], 2))
lv.expect('l2', 'screens[1].canvas.controls[0].frames[2].caption', r(rc['C'], 2))
lv.expect('l2', 'screens[1].canvas.controls[0].frames[3].caption', r(rc['D'], 2))
xa, ya = cases['A']; gA = ya - 0.8 * xa
lv.expect('l2', 'screens[0].widget.options[0].why', int(round(gA.min())))
xd, yd = cases['D']
lv.expect('l2', 'screens[1].widget.options[3].why', int(round((yd - xd).max())))
xb, yb = cases['B']; ub = yb - xb
lv.expect('l2', 'screens[3].explain.text', r(np.std(ub), 2))
lv.expect('l2', 'screens[3].widget.answer', r(3 / math.sqrt(0.75), 2))
lv.expect('l2', 'screens[3].explain.text', r(2 * math.sqrt(12), 2))
lv.expect('l2', 'screens[3].widget.wrong[2].value', 3 / 0.5)
lv.expect('l2', 'screens[4].widget.answer', r(1 / math.sqrt(13), 3))
lv.expect('l2', 'screens[4].widget.wrong[0].value', r(1 / 13, 4))
lv.expect('l2', 'screens[4].widget.wrong[1].value', r(1 / math.sqrt(12), 4))
lv.expect('l2', 'screens[4].feedback.correct', r(rc['B'], 3))


def roll_corr(x, y, w=20):
    dx, dy = np.diff(x), np.diff(y)
    return np.array([np.corrcoef(dx[i:i + w], dy[i:i + w])[0, 1] for i in range(len(dx) - w + 1)])


for k in 'CA':
    rr = roll_corr(*cases[k])
    lv.expect('l2', 'screens[5].prose', r(rr.min(), 2)); lv.expect('l2', 'screens[5].prose', r(rr.max(), 2))


def drift_apart(x, y, beta):
    s = y - beta * x; q = len(s) // 4
    return np.std(s[:q]), np.std(s[-q:])


for k, b in (('A', 0.8), ('C', 1.5), ('B', 1.0)):
    f, l = drift_apart(*cases[k], b)
    lv.expect('l2', 'screens[6].explain.text', r(f, 2)); lv.expect('l2', 'screens[6].explain.text', r(l, 2))
lv.expect('l2', 'screens[8].widget.lines[3].text', r(0.6 * math.sqrt(1000), 2))
lv.expect('l2', 'screens[11].prose', 500 * 499 // 2)
lv.expect('l2', 'screens[11].widget.wrong[1].value', 124750 * 0.05)
lv.expect('l2', 'quiz[3].widget.answer', 300 * 299 // 2)
lv.expect('l2', 'quiz[3].feedback.correct', int(44850 * 0.05))
lv.expect('l2', 'quiz[0].widget.answer', 0.6 * 20)

# ---------------- l3 ----------------
pa = lambda s: adfuller(s, autolag='AIC')
lv.expect('l3', 'screens[2].widget.rows[0][1]', r(pa(xc)[1], 4))
lv.expect('l3', 'screens[2].widget.rows[1][1]', r(pa(yc)[1], 4))
g = yc - 1.5 * xc - 5
lv.expect('l3', 'screens[2].widget.rows[2][1]', r(pa(g)[1], 5))
lv.expect('l3', 'screens[2].explain.text', r(pa(g)[0], 2))
grid = np.round(np.arange(0, 3.0001, 0.01), 2)
st = np.array([pa(yc - b * xc)[0] for b in grid])
lv.expect('l3', 'screens[3].explain.text', r(grid[st.argmin()], 2))
lv.expect('l3', 'screens[3].explain.text', r(st.min(), 2))
below = grid[st < -2.86]
lv.expect('l3', 'screens[3].explain.text', r(below.min(), 2))
claim(abs(below.max() - 1.61) <= 0.011, 'l3 the 0.01 grid falls below -2.86 up to about 1.61', f'last grid point {below.max():.2f}')
lv.expect('l3', 'screens[3].explain.text', r(st[0], 2))
lv.expect('l3', 'quiz[0].explain.text', r(st.min(), 2))
lv.expect('l3', 'screens[0].explain.text', int(round(np.std(yc, ddof=1))))
claim(abs(np.std(yc - 1.4744 * xc, ddof=1) - 1.59) < 0.01 and abs(np.std(g, ddof=1) - 1.64) < 0.01, 'l3 gap sd about £1.60 near 1.5')
claim(np.abs(g - g.mean()).max() < 4.6, 'l3 gap stays within about £4 of its average at beta 1.5', f'max {np.abs(g - g.mean()).max():.2f}')
lv.expect('l3', 'screens[1].widget.options[2].why', int(round(min(xc.min(), yc.min()))))
lv.expect('l3', 'screens[1].widget.options[2].why', int(round(max(xc.max(), yc.max()))))
lv.expect('l3', 'screens[4].explain.text', r(pa(cases['A'][1] - 0.8 * cases['A'][0])[1], 2))
lv.expect('l3', 'screens[4].explain.text', r(pa(cases['D'][1] - cases['D'][0])[1], 2))
lv.expect('l3', 'screens[6].widget.options[0].text', r(pa(cases['A'][1] - 0.8 * cases['A'][0])[1], 2))
lv.expect('l3', 'screens[6].prose', r(pa(np.diff(cases['A'][1]) - 0.8 * np.diff(cases['A'][0]))[0], 2))
g05 = np.round(np.arange(1, 2.0001, 0.05), 2)
lv.expect('l3', 'screens[7].feedback.correct', r(g05[np.argmin([pa(yc - b * xc)[0] for b in g05])], 2))
lv.expect('l3', 'screens[7].feedback.correct', r(grid[st.argmin()], 2))
claim_text('l3', 'screens[7].explain.text', 'a smaller variance looks more stationary', abs(pa(10 * g)[0] - pa(g)[0]) > 1e-6,
           'ADF statistic depends on scale', 'adfuller is scale-invariant: the same statistic for g and 10 g')
lv.expect('l3', 'screens[8].explain.text', r(pa(np.cumsum(np.random.default_rng(5).standard_normal(500)))[1], 2))

# ---------------- l4 ----------------
b1, a1 = np.polyfit(A, B, 1); res = B - a1 - b1 * A
lv.expect('l4', 'screens[0].prose', r(adfuller(res)[0], 2))
lv.expect('l4', 'screens[0].prose', r(adfuller(res)[1], 3))
c103 = coint(B, A)
lv.expect('l4', 'screens[2].explain.text', r(c103[0], 4)); lv.expect('l4', 'screens[2].explain.text', r(c103[1], 4))
lv.expect('l4', 'screens[6].explain.text', r(c103[1], 4))
lv.expect('l4', 'screens[5].feedback.correct', r(eg_stat(B, A), 4))
for v, nm, shown in zip(c103[2], ('1%', '5%', '10%'), (-3.90, -3.34, -3.04)):
    claim_text('l4', 'screens[2].prose', 'with a constant and 500 days', abs(r(v, 2) - shown) < 0.005,
               f'500-day EG {nm} critical value shown as {shown}', f'coint on 500 days gives {v:.4f}')
stats0 = np.array([eg_stat(*make_two_walks(s)[::-1]) for s in range(1000)])
lv.expect('l4', 'screens[1].explain.text', r(100 * (stats0 < -2.86).mean(), 1))
lv.expect('l4', 'screens[1].explain.text', r(100 * (stats0 <= eg_stat(B, A)).mean(), 1))
lv.expect('l4', 'screens[1].explain.text', r(100 * (stats0 < -3.35).mean(), 1))
lv.expect('l4', 'screens[1].widget.answer', r(np.quantile(stats0, 0.05), 2))
lv.expect('l4', 'summary.trap', r(100 * (stats0 < -2.86).mean(), 1))
lv.expect('l4', 'screens[8].explain.text', r(100 * (stats0 < -3.34).mean(), 1))
lv.expect('l4', 'screens[11].widget.options[3].why', r(100 * (stats0 < -3.34).mean(), 1))
lv.expect('l4', 'screens[11].canvas.params.rows', r(100 * (stats0 < -3.34).mean(), 1))
lv.expect('review', 'items[7].prose', r(100 * (stats0 < -3.34).mean(), 1))
bc, ac = np.polyfit(xc, yc, 1); rc_ = yc - ac - bc * xc
lv.expect('l4', 'screens[3].prose', r(bc, 4)); lv.expect('l4', 'screens[3].prose', r(ac, 4))
lv.expect('l4', 'screens[3].prose', r(xc[500], 2)); lv.expect('l4', 'screens[3].prose', r(yc[500], 2))
lv.expect('l4', 'screens[3].widget.answer', r(r(yc[500], 2) - r(ac, 4) - r(bc, 4) * r(xc[500], 2), 2))
lv.expect('l4', 'screens[3].widget.wrong[0].value', r(r(yc[500], 2) - 5 - 1.5 * r(xc[500], 2), 2))
lv.expect('l4', 'screens[3].widget.wrong[1].value', r(r(yc[500], 2) - r(bc, 4) * r(xc[500], 2), 2))
lv.expect('l4', 'screens[3].explain.text', r(np.std(rc_, ddof=1), 2))
lv.expect('l4', 'screens[4].prose', r(eg_stat(yc, xc), 4))
cc = coint(yc, xc)
lv.expect('l4', 'screens[4].explain.text', r(cc[0], 4)); lv.expect('l4', 'screens[4].explain.text', r(cc[1], 4))
claim(abs(cc[0] - eg_stat(yc, xc)) < 1e-9, 'l4 coint chose no lags on pair C')
lv.expect('l4', 'screens[5].explain.text', r(adfuller(rc_, maxlag=0, regression='c', autolag=None)[0], 4))
lv.expect('l4', 'screens[5].explain.text', r(eg_stat(*cases['B'][::-1]), 2))
lv.expect('l4', 'screens[6].prose', r(adfuller(rc_)[1], 6))
lv.expect('l4', 'screens[6].prose', r(cc[1], 6))
lv.expect('l4', 'screens[10].question', r(coint(xc, yc)[0], 3))


def wrong_dec(y, x):
    b, a = np.polyfit(x, y, 1)
    return adfuller(y - a - b * x, autolag='AIC')[1] < 0.05


r200 = [(coint(*make_two_walks(s)[::-1])[1] < 0.05, wrong_dec(*make_two_walks(s)[::-1])) for s in range(200)]
claim(sum(a for a, _ in r200[:40]) == 1, 'l4 coint rejects once on seeds 0 to 39')
lv.expect('l4', 'screens[7].feedback.correct', int(sum(b for _, b in r200[:40])))
lv.expect('l4', 'screens[7].explain.text', int(sum(a for a, _ in r200)))
lv.expect('l4', 'screens[7].explain.text', int(sum(b for _, b in r200)))
xb_, yb_ = make_broken_pair(3)
lv.expect('l4', 'screens[9].prose', r(coint(yb_[:1000], xb_[:1000])[1], 4))
lv.expect('l4', 'screens[9].prose', r(coint(yb_, xb_)[1], 2))
gb = yb_ - 1.5 * xb_ - 5
claim(45 <= -gb[1000:].min() <= 55, 'l4 gap wanders by up to £50 after the break', f'min {gb[1000:].min():.1f}')
lv.expect('l4', 'quiz[1].prose', int(sum(coint(*make_pair(s, 250)[::-1])[1] < 0.05 for s in range(100))))
claim(sum(coint(*make_pair(s, 1000)[::-1])[1] < 0.05 for s in range(100)) == 100, 'l4 1,000-day power 100 of 100')

# ---------------- review-1 ----------------
lv.expect('review', 'items[0].widget.answer', r(0.3 * math.sqrt(248 / 0.91), 2))
lv.expect('review', 'items[0].widget.wrong[0].value', r(0.09 * math.sqrt(248 / 0.91), 2))
lv.expect('review', 'items[0].widget.wrong[1].value', r(0.3 * math.sqrt(250 / 0.91), 2))
lv.expect('review', 'items[0].explain.text', r(math.sqrt(248 / 0.91), 2))
lv.expect('review', 'items[0].explain.text', r(100 * share[250]))
lv.expect('review', 'items[3].widget.answer', 0.8 * math.sqrt(100))
s286, s334 = r(100 * (stats0 < -2.86).mean(), 1), r(100 * (stats0 < -3.34).mean(), 1)
lv.expect('review', 'items[7].widget.answer', round(2000 * (s286 - s334) / 100))
lv.expect('review', 'items[7].widget.wrong[0].value', round(2000 * s286 / 100))
lv.expect('review', 'items[7].widget.wrong[1].value', round(2000 * s334 / 100))
lv.expect('review', 'items[7].explain.text', round(2000 * s286 / 100)); lv.expect('review', 'items[7].explain.text', round(2000 * s334 / 100))
lv.expect('review', 'items[7].feedback.correct', round(2000 * s334 / 100)); lv.expect('review', 'items[7].widget.accept', round(2000 * (s286 - s334) / 100))
claim(s334 == 5.1 and round(2000 * (s286 - s334) / 100) == 190, 'review-1 items[7] keys use 5.1% and 190', f'{s334}, {round(2000 * (s286 - s334) / 100)}')
mk = coint(B, A)[2]; adf1 = adfuller(res, regression='c')  # placeholder to keep names defined
from statsmodels.tsa.adfvalues import mackinnoncrit
adf1pc = mackinnoncrit(N=1, regression='c', nobs=500)[0]
claim(abs(adf1pc - (-3.44)) < 0.005 and mk[0] < -3.60 < mk[1], 'review-1 items[6]: -3.60 is between EG 1% and 5% (500 days) and below ADF 1% -3.44', f'{mk}, ADF 1% {adf1pc:.4f}')
claim(-3.60 > mk[0] and -3.60 < mk[1] and -3.60 < mk[2], 'review-1 items[6]: rejects at 5% and 10% but not 1%')
claim_text('review', 'items[1].explain.text', '500 residuals', '500' in lv.text('review', 'items[1].prose'),
           'explanation names a sample of 500', 'the prose gives no sample length')

# ---------------- homework-1 ----------------
u = 52.85 - 3.10 - 0.92 * 54.20
lv.expect('homework', 'items[1].widget.answer', r(u, 2))
lv.expect('homework', 'items[1].widget.wrong[0].value', r(52.85 - 0.92 * 54.20, 2))
lv.expect('homework', 'items[1].explain.text', r(u, 3))
vu = 4 / 0.36; vdu = 2 * vu * 0.2
lv.expect('homework', 'items[3].widget.answer', r(1 / math.sqrt(1 + vdu), 3))
lv.expect('homework', 'items[3].widget.wrong[0].value', r(1 / (1 + vdu), 3))
lv.expect('homework', 'items[3].widget.wrong[1].value', r(1 / math.sqrt(vdu), 3))
lv.expect('homework', 'items[3].explain.text', r(vu, 2)); lv.expect('homework', 'items[3].explain.text', r(vdu, 2))
lv.expect('homework', 'items[3].explain.text', r(1 + vdu, 2))
for phi in (0.98, 0.9, 0.5, 0.0):
    lv.expect('homework', 'items[5].explain.text', r(100 * np.mean([abst(*ar_pair(s, 250, phi))[0] > 1.96 for s in range(1000)]), 1))
lv.expect('homework', 'items[5].explain.text', r(100 * np.mean([abst(*ar_pair(s, 250, 1.0))[0] > 1.96 for s in range(500)]), 1))
lv.expect('homework', 'items[6].explain.text', 6 * 5 // 2); lv.expect('homework', 'items[6].explain.text', 8 * 7 // 2)

lv.check_wrongs()
lv.report()
