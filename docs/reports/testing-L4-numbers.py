"""Number checks for testing level 4 (l13 to l18, review-4, homework-4, including the performance task h-cr-poisson).

Every stated number is computed twice: once from its closed form (exact fractions where it helps) and once by an
independent route (SciPy, SymPy, a seeded NumPy simulation, a second formula, or the content's own code solution run
on its hidden tests). `two(a, b, tol)` records that the routes agree; `E(file, path, value)` records that the value is
printed where it is stated (app/tools/numbers_lib.py). The code widgets' solutions and starters are run on their tests,
and the homework code item is run against planted wrong solutions. The performance rubric's passing tick sets are listed.
Run: <venv>/bin/python docs/reports/testing-L4-numbers.py   (NumPy, SciPy and SymPy needed; exits 1 on any failure)
"""
import itertools, json, math, os, sys
from fractions import Fraction as Fr
import numpy as np
import sympy as sp
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level('testing', 4)
E = lv.expect
C = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'testing')
J = lambda f: json.load(open(os.path.join(C, f + '.json'), encoding='utf8'))


def two(a, b, tol, label):
    lv.claim(abs(float(a) - float(b)) <= tol, f'two routes: {label} ({float(a):.6g} vs {float(b):.6g})')
    return float(a)


def r(x, k):
    return round(float(x), k)


Phi = stats.norm.cdf
chi2sf = stats.chi2.sf
rng = np.random.default_rng(20261111)

# ---------------------------------------------------------------- l13 matching moments
lam = two(1 / Fr(1, 2), 1 / 0.5, 0, 'exponential rate from mean 0.5'); E('l13', 'screens[0].widget.answer', 2); E('l13', 'screens[0].explain.text', 2)
X = rng.exponential(0.5, 200000); two(1 / X.mean(), 2, 0.01, 'simulated exponential rate')
lam_g = two(Fr(6, 12), 6 / 12, 0, 'Gamma rate 6/12'); a_g = two(Fr(36, 12), 0.5 * 6, 0, 'Gamma shape 36/12 = 6 x 0.5')
G = rng.gamma(3, 2, 400000); two(G.mean() / G.var(), 0.5, 0.01, 'simulated Gamma(3, rate 0.5): mean/var'); two(G.mean() ** 2 / G.var(), 3, 0.05, 'simulated shape')
E('l13', 'screens[2].widget.answer', 3); E('l13', 'screens[2].widget.wrong[0].value', r(Fr(12, 36), 4)); E('l13', 'screens[2].widget.wrong[1].value', 12)
E('l13', 'screens[7].explain.text', 0.5); E('l13', 'screens[7].explain.text', 3)
n = 10
mse_mom = two(Fr(1, 3 * n), 1 / 30, 1e-12, 'MSE of 2xbar'); mse_mle = two(Fr(2, (n + 1) * (n + 2)), 1 / 66, 1e-12, 'MSE of max')
U = rng.random((400000, 10)); two(((2 * U.mean(1) - 1) ** 2).mean(), mse_mom, 0.0005, 'simulated MSE 2xbar'); two(((U.max(1) - 1) ** 2).mean(), mse_mle, 0.0003, 'simulated MSE max')
ratio = two(Fr(66, 30), mse_mom / mse_mle, 1e-12, 'ratio 2.2')
E('l13', 'screens[4].widget.answer', 2.2); E('l13', 'screens[4].widget.wrong[0].value', r(1 / ratio, 4)); E('l13', 'screens[4].widget.wrong[1].value', 0.0333)
E('l13', 'screens[4].explain.text', 0.0333); E('l13', 'screens[4].explain.text', 0.0152); E('l13', 'screens[4].hints', 0.0152)
b = two(math.sqrt(2 / 2), 1, 0, 'Laplace b from 2b^2 = 2'); L = rng.laplace(0, 1, 400000); two((L ** 2).mean(), 2, 0.02, 'Laplace E[X^2] = 2b^2 at b = 1')
E('l13', 'screens[5].widget.answer', 1); E('l13', 'screens[5].widget.wrong[0].value', r(math.sqrt(2), 4))
two(2 * np.mean([1, 2, 9]), 8, 0, '2xbar of 1, 2, 9'); E('l13', 'screens[6].prose', 8); E('l13', 'screens[6].explain.text', 9)
m, v = 0.52, 0.0016
s = two(m * (1 - m) / v - 1, Fr(52, 100) * Fr(48, 100) / Fr(16, 10000) - 1, 1e-9, 'a + b = 155')
a_b = two(m * s, Fr(52, 100) * 155, 1e-9, 'a = 80.6'); b_b = two((1 - m) * s, 155 - 80.6, 1e-9, 'b = 74.4')
two(stats.beta(a_b, b_b).mean(), 0.52, 1e-12, 'Beta(80.6, 74.4) mean'); two(stats.beta(a_b, b_b).var(), 0.0016, 1e-12, 'Beta(80.6, 74.4) variance')
E('l13', 'screens[9].widget.answer', 80.6); E('l13', 'screens[9].widget.wrong[0].value', r(m * (s + 1), 2)); E('l13', 'screens[9].widget.wrong[1].value', 74.4)
E('l13', 'screens[9].explain.text', 155); E('l13', 'screens[9].explain.text', r(math.sqrt(v), 2))
two(1 / 4, 0.25, 0, 'quiz wait'); E('l13', 'quiz[0].widget.answer', 0.25)
two(Fr(100, 25), 10 * Fr(10, 25), 0, 'quiz Gamma shape 4'); E('l13', 'quiz[1].widget.answer', 4); E('l13', 'quiz[1].explain.text', 0.4)
two(2 * np.mean([2, 3, 4, 11]), 10, 0, 'quiz 2xbar = 10'); E('l13', 'quiz[2].widget.answer', 11)

# ---------------------------------------------------------------- l14 sufficiency
two(math.comb(10, 7), len([c for c in itertools.combinations(range(10), 7)]), 0, '120 orders'); E('l14', 'screens[1].prose', 120)
p = 0.7; one = p ** 7 * 0.3 ** 3
two(one, Fr(7, 10) ** 7 * Fr(3, 10) ** 3, 1e-15, 'one order at 0.7'); E('l14', 'screens[1].canvas.state.caption', 0.00222, fmt='0.00222'); E('l14', 'screens[1].canvas.state.caption', 0.2668, fmt='0.2668')
two(120 * one, stats.binom.pmf(7, 10, 0.7), 1e-12, '7 wins at 0.7'); two(120 * 0.5 ** 10, stats.binom.pmf(7, 10, 0.5), 1e-12, '7 wins at 0.5')
E('l14', 'screens[1].explain.canvas.caption', 0.1172, fmt='0.1172'); E('l14', 'screens[1].widget.options', 0.0083)
two(math.comb(10, 6), 210, 0, '210 orders'); E('l14', 'screens[2].widget.answer', 210)
var_rb = two(0.6 * 0.4 / 10, stats.binom.var(10, 0.6) / 100, 1e-15, 'Var(K/10) at 0.6')
K = rng.binomial(10, 0.6, 400000) / 10; two(K.var(), var_rb, 0.0003, 'simulated Var(K/10)')
E('l14', 'screens[6].widget.answer', 0.024); E('l14', 'screens[6].explain.text', 0.24); E('l14', 'screens[6].widget.wrong[1].value', 0.0024)
two(1.95 / 390, 0.005, 1e-12, 'Monday mean return'); E('l14', 'screens[9].explain.text', 0.005)
E('l14', 'quiz[1].widget.answer', 2); two(0.25 / 20, stats.binom.var(20, 0.5) / 400, 1e-15, 'quiz RB 0.0125'); E('l14', 'quiz[2].widget.answer', 0.0125)
# factorisation claims checked symbolically: the Poisson joint pmf depends on the data only through the total
lmb = sp.symbols('lambda', positive=True); xs = sp.symbols('x1:4', nonnegative=True, integer=True)
joint = sp.prod([sp.exp(-lmb) * lmb ** x / sp.factorial(x) for x in xs])
lv.claim(sp.simplify(joint / (sp.exp(-3 * lmb) * lmb ** sum(xs)) - 1 / sp.prod([sp.factorial(x) for x in xs])) == 0, 'Poisson factorisation g(sum x, lambda) h(x)')

# ---------------------------------------------------------------- l15 Fisher information
f1 = lambda q: 7 * math.log(q / 0.7) + 3 * math.log((1 - q) / 0.3)
two(f1(0.6), -0.216, 0.0005, 'fall of 7-in-10 at 0.6'); two(10 * f1(0.6), -2.160, 0.005, 'fall of 70-in-100 at 0.6')
E('l15', 'screens[0].hints', 0.216); E('l15', 'screens[0].hints', 2.16); E('l15', 'screens[0].explain.text', 2.16)
score = two(Fr(7, 1) / Fr(6, 10) - Fr(3, 1) / Fr(4, 10), (f1(0.6 + 1e-6) - f1(0.6 - 1e-6)) / 2e-6, 1e-5, 'score at 0.6')
E('l15', 'screens[1].widget.answer', r(score, 4)); E('l15', 'screens[1].widget.wrong[1].value', r(7 / 0.6 + 7.5, 4)); E('l15', 'screens[1].explain.text', 4.1667)
pp = sp.symbols('p', positive=True); xx = sp.symbols('x')
I_b = sp.simplify(-(xx * sp.diff(sp.log(pp), pp, 2) + (1 - xx) * sp.diff(sp.log(1 - pp), pp, 2)).subs(xx, pp))
lv.claim(sp.simplify(I_b - 1 / (pp * (1 - pp))) == 0, 'sympy: Bernoulli I(p) = 1/(p(1-p))')
I1 = two(1 / 0.21, float(I_b.subs(pp, sp.Rational(7, 10))), 1e-12, 'I(0.7) per trade'); I100 = 100 * I1
B = rng.binomial(1, 0.7, (200000, 1)); S1 = B[:, 0] / 0.7 - (1 - B[:, 0]) / 0.3; two(S1.var(), I1, 0.05, 'simulated Var(score) one trade')
E('l15', 'screens[2].widget.answer', r(I100, 2)); E('l15', 'screens[2].widget.wrong[0].value', r(I1, 4)); E('l15', 'screens[2].explain.text', 47.62); E('l15', 'screens[2].hints', 4.7619)
mu, sg, lm = sp.symbols('mu sigma lambda', positive=True)
lv.claim(sp.simplify(-sp.diff(-(xx - mu) ** 2 / (2 * sg ** 2), mu, 2) - 1 / sg ** 2) == 0, 'sympy: normal mean I = 1/sigma^2')
lv.claim(sp.simplify(-sp.diff(sp.log(lm) - lm * xx, lm, 2) - 1 / lm ** 2) == 0, 'sympy: exponential rate I = 1/lambda^2')
lv.claim(sp.simplify(-sp.diff(xx * sp.log(lm) - lm, lm, 2).subs(xx, lm) - 1 / lm) == 0, 'sympy: Poisson mean I = 1/lambda')
lv.claim(sp.simplify(-(sp.diff(-sp.log(sg) - xx ** 2 / (2 * sg ** 2), sg, 2)).subs(xx ** 2, sg ** 2) - 2 / sg ** 2) == 0, 'sympy: I(sigma) = 2/sigma^2')
for k, val in enumerate([0.25, 0.25, 0.5]):
    E('l15', f'screens[3].widget.rows[{k}][3].answer', val)
se_p = two(1 / math.sqrt(I100), math.sqrt(0.21 / 100), 1e-12, 'SE of phat'); E('l15', 'screens[4].widget.answer', r(se_p, 4))
E('l15', 'screens[4].explain.canvas.vlines[0].x', r(0.7 - se_p, 4)); E('l15', 'screens[4].explain.canvas.vlines[1].x', r(0.7 + se_p, 4)); E('l15', 'screens[4].widget.wrong[1].value', r(math.sqrt(0.21), 4))
se_s = two(1 / math.sqrt(2 * 252), 1 / math.sqrt(504), 1e-15, 'SE of sigma hat')
R = rng.standard_normal((20000, 252)); two(np.sqrt((R ** 2).mean(1)).std(), se_s, 0.001, 'simulated SE of sigma hat (mean 0 known)')
E('l15', 'screens[5].widget.answer', r(se_s, 4)); E('l15', 'screens[5].widget.wrong[0].value', r(1 / math.sqrt(252), 3)); E('l15', 'screens[5].feedback.correct', 4.45)
two(-1 / 2, -0.5, 0, 'uniform mean score at theta 2'); E('l15', 'screens[6].widget.answer', -0.5)
se_s2 = two(math.sqrt(2 / 252), 2 * se_s, 1e-12, 'SE of sigma^2 hat (delta method)'); two(((R ** 2).mean(1)).std(), se_s2, 0.002, 'simulated SE of sigma^2 hat')
E('l15', 'screens[7].widget.answer', r(se_s2, 4)); E('l15', 'screens[7].widget.wrong[1].value', r(se_s / 2, 4))
lv.claim(sp.simplify((2 / sg ** 2) / (2 * sg) ** 2 - 1 / (2 * sg ** 4)) == 0, 'chain rule I(sigma^2) = 1/(2 sigma^4)')
n200 = two(1 / (2 * 0.05 ** 2), Fr(1, 2) / Fr(1, 400), 1e-9, 'n = 200'); E('l15', 'screens[10].widget.answer', 200); E('l15', 'screens[10].widget.wrong[0].value', 400)
two(math.sqrt(4 / 25), 0.4, 1e-12, 'quiz Poisson SE'); E('l15', 'quiz[0].widget.answer', 0.4); E('l15', 'quiz[0].explain.text', 6.25)
two(2 / math.sqrt(100), 0.2, 1e-12, 'quiz exponential SE'); E('l15', 'quiz[2].widget.answer', 0.2); E('l15', 'quiz[2].widget.wrong[1].value', r(math.sqrt(2 / 100), 4))
# overlapping 5-day returns: SE ratio about sqrt 5
d = rng.standard_normal((4000, 254)); o5 = np.array([d[:, i:i + 5].sum(1) for i in range(250)]).T
naive = np.sqrt(5 / 250); true = o5.mean(1).std(); two(true / naive, math.sqrt(5), 0.25, 'overlap SE understated by about sqrt 5')

# ---------------------------------------------------------------- l16 Cramer-Rao
H = J('l16-best-possible-precision')['screens'][0]['canvas']['state']['values']
rg = np.random.default_rng(2016); Xn = rg.standard_normal((2000, 101))
lv.claim(all(abs(sum(H[g].values()) - 1) < 0.002 for g in H), 'hook histograms are shares summing to 1')
sds = [Xn.mean(1).std(), np.median(Xn, 1).std(), ((Xn[:, 0] + Xn[:, -1]) / 2).std()]
for k, (val, th) in enumerate(zip([0.100, 0.126, 0.715], [1 / math.sqrt(101), math.sqrt(math.pi / 2 / 101), math.sqrt(0.5)])):
    two(round(sds[k], 3), val, 0, f'hook sd {k}'); two(val, th, 0.015, f'hook sd {k} against theory')
E('l16', 'screens[0].explain.text', 0.715); E('l16', 'screens[0].explain.text', 0.126)
two(1 / math.sqrt(11), 0.30, 0.002, 'sd mean at 11'); E('l16', 'screens[1].hints', 0.71)
bound = two(1 / 101, Fr(1, 101), 1e-15, 'bound 1/101'); E('l16', 'screens[2].widget.answer', r(bound, 4)); E('l16', 'screens[2].widget.wrong[0].value', r(1 / math.sqrt(101), 4))
two(Xn.mean(1).var(), 0.0101, 0.00005, 'simulated var of mean'); two(np.median(Xn, 1).var(), 0.016, 0.00005, 'simulated var of median')
eff_med = two(2 / math.pi, float(sp.N(2 / sp.pi)), 1e-15, '2/pi'); E('l16', 'screens[3].prose', 0.6366); E('l16', 'screens[3].prose', 1.5708)
two(np.median(Xn, 1).var() / Xn.mean(1).var(), 1.59, 0.005, 'simulated median/mean variance ratio')
m159 = two(101 * math.pi / 2, 101 / eff_med, 1e-9, '101 pi/2'); E('l16', 'screens[3].widget.answer', r(m159, 1)); E('l16', 'screens[3].widget.wrong[0].value', r(101 * 2 / math.pi, 1))
Emle = two(Fr(10 * 2, 9), 20 / 9, 1e-15, 'E[1/xbar]'); Xe = rng.exponential(0.5, (400000, 10)); two((1 / Xe.mean(1)).mean(), Emle, 0.005, 'simulated E[1/xbar]')
E('l16', 'screens[4].widget.answer', r(Emle, 4)); E('l16', 'screens[4].widget.wrong[1].value', r(20 / 11, 4))
v_unb = two(Fr(4, 8), (9 / Xe.sum(1)).var(), 0.005, 'Var((n-1)/sum x) = lambda^2/(n-2)'); E('l16', 'screens[5].prose', 0.5); E('l16', 'screens[5].prose', 0.4)
two(Fr(4, 10) / Fr(1, 2), 0.8, 0, 'efficiency 0.8'); E('l16', 'screens[5].widget.answer', 0.8)
Xs = rng.standard_normal((400000, 10)); two(Xs.var(1, ddof=1).var(), 2 / 9, 0.003, 'simulated Var(s^2) = 2/9'); E('l16', 'screens[5].explain.text', Fr(2, 9))
two(Fr(2, 11), (Xs.var(1, ddof=0) * 10 / 11 - 1).__pow__(2).mean(), 0.003, 'MSE of SS/(n+1) = 2/11'); E('l16', 'screens[6].prose', r(2 / 11, 4)); E('l16', 'screens[6].canvas.state.values.nm1', r(2 / 9, 4))
nd = two((2 * 1 / 0.04) ** 2, 2500, 1e-9, '2,500 days'); E('l16', 'screens[9].widget.answer', 2500); two(2500 / 252, 9.9, 0.05, '9.9 years'); E('l16', 'screens[9].explain.text', 9.9)
E('l16', 'screens[9].widget.wrong[1].value', 625)
Uu = rng.random((400000, 10)).max(1) * 11 / 10; two(Uu.var(), Fr(1, 120), 0.0002, 'Var((n+1)/n max) = 1/120')
two(0.25 / 100, 0.0025, 1e-15, 'quiz hit bound'); E('l16', 'quiz[1].widget.answer', 0.0025); two(2 / 50, 0.04, 1e-15, 'quiz sigma^2 bound'); E('l16', 'quiz[2].widget.answer', 0.04)

# ---------------------------------------------------------------- l17 likelihood ratios
LR = lambda k: 1.2 ** k * 0.8 ** (20 - k)
two(LR(15), stats.binom.pmf(15, 20, 0.6) / stats.binom.pmf(15, 20, 0.5), 1e-12, 'LR(15)'); E('l17', 'screens[0].widget.answer', r(LR(15), 3))
two(LR(10), stats.binom.pmf(10, 20, 0.6) / stats.binom.pmf(10, 20, 0.5), 1e-12, 'LR(10)'); E('l17', 'screens[0].explain.text', 0.665); E('l17', 'screens[0].widget.wrong[0].value', r(1 / LR(15), 4))
E('l17', 'screens[1].canvas.state.points[0].y', r(LR(8), 4)); E('l17', 'screens[1].hints', r(LR(11), 3)); E('l17', 'screens[1].hints', r(LR(12), 3))
lv.claim(LR(11) < 1 < LR(12), 'ratio first exceeds 1 at 12 wins'); E('l17', 'screens[1].widget.answer', 12)
size15 = two(stats.binom.sf(14, 20, 0.5), Fr(sum(math.comb(20, k) for k in range(15, 21)), 2 ** 20), 1e-15, 'size of k >= 15')
size14 = two(stats.binom.sf(13, 20, 0.5), Fr(sum(math.comb(20, k) for k in range(14, 21)), 2 ** 20), 1e-15, 'size of k >= 14')
pow15 = two(stats.binom.sf(14, 20, 0.6), sum(math.comb(20, k) * Fr(6, 10) ** k * Fr(4, 10) ** (20 - k) for k in range(15, 21)), 1e-15, 'power of k >= 15')
E('l17', 'screens[2].prose', r(size15, 4)); E('l17', 'screens[2].prose', r(size14, 4)); E('l17', 'screens[2].widget.answer', r(pow15, 4)); E('l17', 'screens[2].widget.wrong[1].value', r(1 - pow15, 4))
E('l17', 'screens[2].widget.wrong[2].value', r(stats.binom.sf(13, 20, 0.6), 4))
two(stats.binom.cdf(5, 20, 0.5), size15, 1e-15, 'size of k <= 5 equals 0.0207'); E('l17', 'screens[3].prose', r(stats.binom.cdf(5, 20, 0.6), 4))
two(0.6 ** 6, Fr(6, 10) ** 6, 1e-15, 'first six power'); E('l17', 'screens[3].explain.text', r(0.6 ** 6, 4)); E('l17', 'screens[3].prose', r(0.5 ** 6, 4))
stat = two(2 * (120 * math.log(1.2) - 50 * 0.4), -2 * (stats.poisson.logpmf(120, 100) - stats.poisson.logpmf(120, 120)), 1e-9, 'Poisson LRT via the total')
E('l17', 'screens[4].widget.answer', r(stat, 3)); E('l17', 'screens[4].explain.text', r(chi2sf(stat, 1), 4)); two(chi2sf(stat, 1), 2 * (1 - Phi(math.sqrt(stat))), 1e-12, 'chi2_1 tail two ways')
two(stats.chi2.ppf(0.95, 1), 1.959964 ** 2, 1e-4, '3.841'); E('l17', 'screens[4].canvas.state.vlines[0].x', 3.841)
E('l17', 'screens[4].hints', r(120 * math.log(1.2), 3)); E('l17', 'screens[4].widget.wrong[0].value', r(stat / 2, 3))
z0 = two(0.4 / math.sqrt(2 / 50), 2.0, 1e-12, 'z null variance'); z1 = two(0.4 / math.sqrt(2.4 / 50), 1.826, 0.0005, 'z estimated variance')
E('l17', 'screens[5].prose', r(2 * stats.norm.sf(z0), 4)); E('l17', 'screens[5].prose', r(2 * stats.norm.sf(z1), 4)); E('l17', 'screens[5].prose', 1.826)
pool = two((1 + 1.69) / 2, Fr(269, 200), 1e-15, 'pooled variance')
vol = two(100 * math.log(pool / 1) + 100 * math.log(pool / 1.69), 200 * math.log(pool) - 100 * math.log(1) - 100 * math.log(1.69), 1e-9, 'two-regime LRT')
Rr = rng.standard_normal((4000, 200)); w = np.r_[np.ones(100), np.full(100, 1.0)]
sims = 100 * np.log((Rr ** 2).mean(1) / (Rr[:, :100] ** 2).mean(1)) + 100 * np.log((Rr ** 2).mean(1) / (Rr[:, 100:] ** 2).mean(1))
two(np.mean(sims > 3.841), 0.05, 0.012, 'simulated size of the two-regime test at 5%')
E('l17', 'screens[10].widget.answer', r(vol, 3)); E('l17', 'screens[10].explain.text', r(chi2sf(vol, 1), 4)); E('l17', 'screens[10].hints', r(100 * math.log(pool), 3)); E('l17', 'screens[10].hints', r(math.log(pool / 1.69), 4))
E('l17', 'screens[10].widget.wrong[0].value', r(100 * math.log(pool), 2)); E('l17', 'screens[10].explain.text', r(math.sqrt(1.69), 1))
two(0.2 / 1.2, 1 / 6, 1e-15, 'trap posterior chance'); E('l17', 'screens[7].explain.text', 0.167)
two(2 * (512.4 - 509.1), 6.6, 1e-9, 'quiz LR 6.6'); E('l17', 'quiz[3].widget.answer', 6.6)
two(stats.chi2.ppf(0.90, 1), 2.706, 0.001, 'boundary mixture 5% point equals chi2_1 10% point (claim: 3.841 too strict)')

# ---------------------------------------------------------------- l18 chi-squared
O = np.array([62, 45, 48, 41, 54]); Ee = 50
cont = (O - Ee) ** 2 / Ee; X2 = two(cont.sum(), stats.chisquare(O).statistic, 1e-12, 'weekday X^2')
for k, c in enumerate(cont):
    E('l18', f'screens[0].widget.rows[{k}][3].answer', r(c, 2))
E('l18', 'screens[0].widget.rows[5][3].answer', 5.4)
p54 = two(math.exp(-2.7) * 3.7, chi2sf(5.4, 4), 1e-12, 'chi2_4 tail at 5.4'); E('l18', 'screens[1].widget.answer', r(p54, 4)); E('l18', 'screens[1].widget.wrong[0].value', r(1 - p54, 4))
E('l18', 'screens[1].widget.wrong[1].value', r(chi2sf(5.4, 1), 4)); E('l18', 'screens[1].canvas.state.caption', r(chi2sf(9.5, 4), 4))
two(stats.chi2.ppf(0.95, 4), 9.488, 0.0005, 'cut-off 9.488'); E('l18', 'screens[1].explain.text', 9.488)
zmon = two(12 / math.sqrt(250 * 0.2 * 0.8), (62 - 50) / math.sqrt(40), 1e-12, 'Monday z'); E('l18', 'screens[2].prose', r(zmon, 3))
Gst = two(2 * (O * np.log(O / Ee)).sum(), stats.power_divergence(O, lambda_='log-likelihood').statistic, 1e-9, 'G statistic')
E('l18', 'screens[3].widget.answer', r(Gst, 3)); E('l18', 'screens[3].feedback.correct', r(chi2sf(Gst, 4), 4))
for k, o in enumerate(O):
    E('l18', f'screens[3].canvas.params.rows[{k}][3]', r(o * math.log(o / 50), 3))
T22 = np.array([[70, 50], [50, 70]]); res = stats.chi2_contingency(T22, correction=False)
x22 = two(4 * 100 / 60, res[0], 1e-12, '2x2 X^2'); E('l18', 'screens[4].widget.answer', r(x22, 3)); E('l18', 'screens[4].feedback.correct', r(res[1], 4))
zz = two((70 / 120 - 50 / 120) / math.sqrt(0.25 * 2 / 120), math.sqrt(x22), 1e-12, 'two-proportion z squared'); E('l18', 'screens[4].explain.text', r(zz, 3))
T32 = np.array([[45, 35], [60, 60], [15, 25]]); res = stats.chi2_contingency(T32, correction=False)
x32 = two(2 * 25 / 40 + 2 * 25 / 20, res[0], 1e-12, '3x2 X^2'); E('l18', 'screens[5].widget.answer', 3.75); E('l18', 'screens[5].explain.text', r(res[1], 4))
two(stats.chi2.ppf(0.95, 2), 5.991, 0.0005, 'cut-off 5.991'); two(math.exp(-3.75 / 2), res[1], 1e-12, 'chi2_2 tail by e^{-x/2}')
lamp = 1.8; pr = [stats.poisson.pmf(k, lamp) for k in range(4)]; pr.append(stats.poisson.sf(3, lamp))
Ep = [200 * x for x in pr]; Op = [30, 62, 56, 32, 20]
for k, e in enumerate(Ep):
    E('l18', 'screens[6].prose', r(e, 2))
xp = two(sum((o - e) ** 2 / e for o, e in zip(Op, Ep)), stats.chisquare(Op, Ep, ddof=1).statistic, 1e-9, 'Poisson GOF X^2')
E('l18', 'screens[6].prose', r(xp, 3)); E('l18', 'screens[6].widget.answer', 3); E('l18', 'screens[6].feedback.correct', r(chi2sf(xp, 3), 3))
two(stats.chisquare(Op, Ep, ddof=1).pvalue, chi2sf(xp, 3), 1e-12, 'GOF p on 3 df two ways')
x10 = two(stats.chi2_contingency(10 * T22, correction=False)[0], 10 * x22, 1e-9, 'ten times the table'); E('l18', 'screens[7].widget.options', r(x10, 2))
V = np.array([112, 95, 88, 120, 85]); xv = two(((V - 100) ** 2 / 100).sum(), stats.chisquare(V).statistic, 1e-12, 'venue evenness')
TV = np.array([[90, 22], [80, 15], [60, 28], [100, 20], [70, 15]]); rv = stats.chi2_contingency(TV, correction=False)
xi = two(rv[0], sum((TV[i, j] - TV[i].sum() * TV[:, j].sum() / 500) ** 2 / (TV[i].sum() * TV[:, j].sum() / 500) for i in range(5) for j in range(2)), 1e-9, 'venue x quality')
E('l18', 'screens[10].widget.rows[0][1].answer', r(xv, 2)); E('l18', 'screens[10].widget.rows[1][1].answer', r(xi, 2)); E('l18', 'screens[10].widget.rows[1][2].answer', rv[2])
E('l18', 'screens[10].explain.text', r(chi2sf(xv, 4), 3)); E('l18', 'screens[10].explain.text', r(rv[1], 3)); E('l18', 'screens[10].explain.text', round(28 / 88 * 100))
E('l18', 'screens[10].widget.rows[1][1].wrong[0].value', r(sum((TV[i, 1] - TV[i].sum() * 0.2) ** 2 / (TV[i].sum() * 0.2) for i in range(5)), 1))
yates = two(stats.chi2_contingency(T22, correction=True)[0], 4 * 9.5 ** 2 / 60, 1e-12, 'continuity-corrected 6.017'); E('l18', 'quiz[1].prose', r(yates, 3))
two(1240 / 20, 62, 0, 'non-overlapping windows'); E('l18', 'quiz[3].explain.text', 62)

# ---------------------------------------------------------------- review-4
two(Fr(16, 2), 2 * 4, 0, 'r-gamma shape 8'); E('review', 'items[0].widget.answer', 8)
se_r = two(math.sqrt(0.55 * 0.45 / 400), 1 / math.sqrt(400 / 0.2475), 1e-15, 'r-se-hit'); E('review', 'items[2].widget.answer', r(se_r, 4)); E('review', 'items[2].explain.text', r(1.96 * se_r, 3))
E('review', 'items[3].widget.answer', 0.8)
lr_r = two(2 * (60 * math.log(1.2) + 40 * math.log(0.8)), 2 * (stats.binom.logpmf(60, 100, 0.6) - stats.binom.logpmf(60, 100, 0.5)), 1e-9, 'r-lrt-coin')
E('review', 'items[4].widget.answer', r(lr_r, 3)); E('review', 'items[4].explain.text', r(chi2sf(lr_r, 1), 4))
T23 = np.array([[30, 50, 20], [20, 30, 50]]); r23 = stats.chi2_contingency(T23, correction=False)
two(r23[0], 2 * (25 / 25 + 100 / 40 + 225 / 35), 1e-9, 'r-chi-23'); E('review', 'items[5].widget.answer', r(r23[0], 3)); E('review', 'items[5].widget.wrong[0].value', r(r23[0] / 2, 3))
two(round(r23[1], 5), 0.00005, 0, 'r-chi-23 p'); two(((T23 - r23[3]) ** 2).sum(), 700, 1e-9, 'r-chi-23 sum of squares'); E('review', 'items[5].widget.wrong[1].value', 700)
two(4 / 8, 0.5, 0, 'r-rb-exp'); Xr = rng.exponential(2, (200000, 8)); two(Xr.mean(1).var(), 0.5, 0.01, 'simulated Var(xbar) exponential mean 2, n 8'); E('review', 'items[7].widget.answer', 0.5)
two(2 / math.sqrt(50), 0.2828, 0.00005, 'r-param'); E('review', 'items[8].widget.answer', 0.2828); E('review', 'items[8].widget.wrong[0].value', r(0.5 / math.sqrt(50), 4))

# ---------------------------------------------------------------- homework-4
rb = two(Fr(4, 5) ** 10, stats.binom.pmf(0, 10, 0.2), 1e-15, 'h-rb-zero'); E('homework', 'items[0].widget.answer', r(rb, 4)); E('homework', 'items[0].prose', r(math.exp(-2), 4))
Pz = rng.poisson(2, (400000, 5)); tot = Pz.sum(1); sel = Pz[tot == 10]; two((sel[:, 0] == 0).mean(), rb, 0.006, 'simulated P(X1 = 0 | T = 10)')
E('homework', 'items[0].widget.wrong[2].value', r(0.8 ** 5, 4))
two(1 - Fr(5, 4), -0.25, 0, 'h-mom-negative'); E('homework', 'items[1].widget.answer', -0.25); E('homework', 'items[1].explain.text', -16)
two(Fr(1, 20), 0.05, 0, 'h-eff-min'); Xm = rng.exponential(1, (200000, 20)); two((20 * Xm.min(1)).var(), 1, 0.02, 'simulated Var(n min) = theta^2'); E('homework', 'items[2].widget.answer', 0.05)
le = two(2 * (40 * math.log(2.6 / 2) + 60 * math.log(2.6 / 3)), 2 * ((-40 * math.log(2) - 40) + (-60 * math.log(3) - 60) - (-100 * math.log(2.6) - 100)), 1e-9, 'h-lrt-exp')
E('homework', 'items[3].widget.answer', r(le, 3)); E('homework', 'items[3].feedback.correct', r(chi2sf(le, 1), 4)); E('homework', 'items[3].widget.wrong[1].value', r(80 * math.log(1.3), 3))
pw = two(Phi(0.5 * 4 - 1.645), stats.norm.sf((1.645 / 4 - 0.5) / 0.25), 1e-12, 'h-np-normal power'); E('homework', 'items[6].widget.answer', r(pw, 4)); E('homework', 'items[6].widget.wrong[2].value', r(1.645 / 4, 4))
E('homework', 'items[7].model', r(math.pi / 2 * 1.44 / 250, 5)); E('homework', 'items[7].model', r(math.sqrt(math.pi / 2 * 1.44 / 250), 3)); E('homework', 'items[7].model', r(1.2 / math.sqrt(250), 3))
E('homework', 'items[7].model', r(1.2 / math.sqrt(500), 3)); E('homework', 'items[7].model', r(stats.chi2.ppf(0.95, 7), 3)); E('homework', 'items[7].prose' if False else 'items[7].prompt', 0.00576)
two(1.44 / 250, 0.00576, 1e-15, 'CR bound for the mean, sd 1.2, n 250')
# performance task: Poisson bound lambda/n, attained by xbar (symbolic and simulated)
xi_ = sp.symbols('x', nonnegative=True); nn = sp.symbols('n', positive=True)
ell = xi_ * sp.log(lm) - lm
lv.claim(sp.simplify(sp.diff(ell, lm).subs(xi_, lm)) == 0, 'perf: E[score] = 0 for one Poisson count')
lv.claim(sp.simplify(nn * (-sp.diff(ell, lm, 2)).subs(xi_, lm) - nn / lm) == 0, 'perf: nI(lambda) = n/lambda')
Pp = rng.poisson(3, (400000, 12)); two(Pp.mean(1).var(), 3 / 12, 0.003, 'perf: simulated Var(xbar) = lambda/n at 3, 12')
Sc = Pp.sum(1) / 3 - 12; two(np.cov(Pp.mean(1), Sc)[0, 1], 1, 0.02, 'perf: simulated Cov(xbar, S) = 1'); two(Sc.var(), 12 / 3, 0.05, 'perf: simulated Var(S) = n/lambda')
lv.claim(np.allclose(Pp.mean(1), 3 + (3 / 12) * Sc), 'perf: xbar = lambda + (lambda/n) S exactly')
hw = J('homework-4'); perf = [it for it in hw['items'] if it.get('performance')]
lv.claim(len(perf) == 1 and perf[0]['performance'] == 'derivation', 'one derivation performance task')
rub = perf[0]['rubric']; pts = [x['points'] for x in rub]; req = [bool(x.get('required')) for x in rub]
passing = [s for k in range(1, len(rub) + 1) for s in itertools.combinations(range(len(rub)), k) if sum(pts[i] for i in s) >= 7 and all(i in s for i in range(len(rub)) if req[i])]
print('perf rubric passing tick sets (rows 1-based):', [[i + 1 for i in s] for s in passing])
lv.claim(sum(pts) == 10 and len(passing) == 2 and all(set(range(4)) <= set(s) for s in passing), 'perf: every pass ticks score, information, bound and attainment')
lv.claim(not all(req), 'perf: not every row required')

# ---------------------------------------------------------------- code widgets: solution passes, starter fails, planted bugs fail
sys.path.insert(0, HERE)


def widgets(node):
    if isinstance(node, dict):
        if node.get('kind') == 'code':
            yield node
        for v_ in node.values():
            yield from widgets(v_)
    elif isinstance(node, list):
        for v_ in node:
            yield from widgets(v_)


def close(a_, b_, tol):
    if isinstance(b_, (list, tuple)):
        return isinstance(a_, (list, tuple)) and len(a_) == len(b_) and all(close(x, y, tol) for x, y in zip(a_, b_))
    if isinstance(b_, bool):
        return a_ == b_
    rel = (tol or {}).get('rel', 0 if tol else 1e-9); ab = (tol or {}).get('abs', 0 if tol else 1e-12)
    return math.isclose(float(a_), float(b_), rel_tol=rel, abs_tol=ab)


def fails(src, w):
    bad = 0
    for t in w['tests']:
        g = {}
        try:
            exec(src, g)
            if t.get('setup'):
                exec(t['setup'], g)
            ok = close(eval(t['call'], g), eval(t['expect'], g), t.get('tol'))
        except Exception:
            ok = False
        bad += not ok
    return bad


for f in ['l13-matching-moments', 'l15-sharpness-of-the-peak', 'l17-ratio-of-likelihoods', 'l18-counts-against-expectations', 'homework-4']:
    for w in widgets(J(f)):
        lv.claim(fails(w['solution'], w) == 0, f'{f}: solution passes all {len(w["tests"])} tests')
        lv.claim(fails(w['starter'], w) == len(w['tests']), f'{f}: starter fails every test')
gw = next(widgets(J('homework-4'))); sol = gw['solution']
planted = {
    'df cells minus 1': sol.replace('df = len(obs) - 2', 'df = len(obs) - 1'),
    'no merging': sol.replace('while len(obs) > 2 and exp_[-1] < 5:', 'while False:').replace('while len(obs) > 2 and exp_[0] < 5:', 'while False:'),
    'last cell P(X = m), not the tail': sol.replace('probs.append(1 - sum(probs))', 'probs.append(exp(-lam) * lam ** m / factorial(m))'),
    'front merge into the wrong cell': sol.replace('o, e = obs.pop(0), exp_.pop(0)\n        obs[0] += o\n        exp_[0] += e', 'obs[1] += obs.pop(0)\n        exp_[1] += exp_.pop(0)'),
    'sample variance as the Poisson mean': sol.replace('lam = sum(counts) / n', 'lam = sum((c - sum(counts) / n) ** 2 for c in counts) / n'),
}
for name, src in planted.items():
    lv.claim(src != sol and fails(src, gw) > 0, f'homework code catches planted bug: {name}')

lv.check_wrongs()
lv.report()
