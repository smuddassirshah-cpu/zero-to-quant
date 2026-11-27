"""Extra ai-papers numbers, each by two methods."""
import numpy as np, math
from scipy import stats, integrate
from toy import train, eval_loss
# log-log slope of a clean power law, and the bend from an irreducible term
f = lambda N: 10*N**-0.1
s1 = math.log10(f(1e10)/f(1e8))/2; s2 = np.polyfit(np.log10([1e8, 1e9, 1e10]), np.log10([f(1e8), f(1e9), f(1e10)]), 1)[0]
print('clean power law: L(1e8) %.4f L(1e10) %.4f slope %.4f (polyfit %.4f)' % (f(1e8), f(1e10), s1, s2))
g = lambda N: 1.69 + 406.4*N**-0.3392
n1 = math.log10(g(1e10)/g(1e8))/2; n2 = np.polyfit(np.log10([1e8, 1e10]), np.log10([g(1e8), g(1e10)]), 1)[0]
r1 = math.log10((g(1e10)-1.69)/(g(1e8)-1.69))/2
print('with E: L(1e8) %.4f L(1e10) %.4f naive slope %.4f (polyfit %.4f); slope of L - E %.4f' % (g(1e8), g(1e10), n1, n2, r1))
# compute parity
print('6ND: 1.25e8 x 2.5e9 = %.4g ; 1.25e8 x 1e9 = %.4g ; ratio %.3f' % (6*1.25e8*2.5e9, 6*1.25e8*1e9, 2.5))
# Chinchilla on Pyodide
secs = 5.76e23/2.1e9; print('5.76e23 FLOP at 2.1 GFLOP/s: %.4g s = %.4g years (%.4g by 365.25-day years)' % (secs, secs/3.156e7, secs/(365.25*86400)))
# toy grid time
print('phase grid 5 x 4 cells x 6 seeds x 0.85 s = %.1f s' % (5*4*6*0.85))
# short runs for two phase cells
for r_, S in [(1.5, 0.0), (1.0, 0.9), (0.1, 0.0)]:
    out = []
    for seed in range(4):
        W, b = train(2, 1, S, np.array([1.0, r_]), steps=1000, B=256, seed=seed); out.append(np.round(W[0], 3).tolist())
    print('short 1000x256 r=%.1f S=%.1f: %s' % (r_, S, out))
# seeds
a = np.array([71.2, 72.5, 70.8, 73.1, 71.9]); b = np.array([72.0, 73.6, 71.1, 74.0, 72.3]); d = b - a
print('sd A %.4f sd B %.4f sd diff %.4f (by hand %.4f)' % (a.std(ddof=1), b.std(ddof=1), d.std(ddof=1), math.sqrt(sum((x-d.mean())**2 for x in d)/4)))
sd = d.std(ddof=1)
for delta in [0.3, 0.5]:
    n = ((1.959964+0.841621)*sd/delta)**2
    # second method: smallest n with simulated power >= 0.8 using normal approx
    nn = next(k for k in range(2, 200) if stats.norm.sf(1.959964 - delta/(sd/math.sqrt(k))) >= 0.8)
    print('seeds for delta %.1f: formula %.2f, smallest n by power search %d' % (delta, n, nn))
# items: paired via discordant counts
bb, cc, n = 40, 60, 1000
se_pair = math.sqrt((bb+cc) - (cc-bb)**2/n)/n
dvec = np.r_[np.full(bb, -1.0), np.full(cc, 1.0), np.zeros(n-bb-cc)]
print('items: diff %.4f paired se %.6f (vector sd/sqrt(n) %.6f) unpaired se %.6f z paired %.3f unpaired %.3f' % (
    (cc-bb)/n, se_pair, dvec.std(ddof=0)/math.sqrt(n), math.sqrt(.72*.28/n + .74*.26/n), 0.02/se_pair, 0.02/math.sqrt(.72*.28/n + .74*.26/n)))
# expected max of 5 standard normals
em = integrate.quad(lambda x: x*5*stats.norm.pdf(x)*stats.norm.cdf(x)**4, -10, 10)[0]
mc = np.random.default_rng(0).standard_normal((400000, 5)).max(1).mean()
print('E max of 5 N(0,1): %.5f (simulation %.5f)' % (em, mc))
