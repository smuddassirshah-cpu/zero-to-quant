"""Numbers used in the proposed fixes of review-bank-2-a.md, each by two routes. Exit 0 when all hold."""
from fractions import Fraction as F
from math import sqrt, isclose
from statistics import NormalDist
import json, os, collections
ok = True
def chk(name, a, b, tol=1e-9):
    global ok; good = abs(float(a) - float(b)) <= tol; ok = ok and good
    print('ok  ' if good else 'FAIL', name, float(a), float(b))
# finding 2: Beta(3, 1) prior, 7 of 10
chk('posterior mean 5/7', F(3 + 7, 4 + 10), 0.714286, 5e-7); chk('no prior', F(7, 10), 0.7); chk('one of each', F(8, 12), 0.6667, 5e-5)
# finding 3: k = 4, n = 65, R2 = 0.2
chk('F', (F(1, 5) / 4) / (F(4, 5) / 60), 3.75); chk('F again from sums', (0.2 * 100 / 4) / (0.8 * 100 / 60), 3.75)
chk('df 61', 0.05 / (0.8 / 61), 3.81, 0.005); chk('no df', 0.2 / 0.8, 0.25)
# finding 4: n = 625
chk('band', 1.96 / sqrt(625), 0.0784); chk('band again', 1.96 / 25, 0.0784); chk('no multiplier', 1 / 25, 0.04); chk('by n', 1.96 / 625, 0.0031, 5e-5); chk('rule of two', 2 / 25, 0.08)
# finding 5: t to 2 places
chk('t', sqrt(0.2 * 100 / 0.8), 5.00); chk('used n', sqrt(0.2 * 102 / 0.8), 5.05, 0.005); chk('no one-minus', sqrt(0.2 * 100), 4.47, 0.005)
# finding 6: Phi(0.355)
chk('Phi(0.355)', NormalDist().cdf(0.355), 0.6387, 5e-5)
# finding 13: VIF at r = 0.6
chk('VIF', 1 / (1 - 0.36), 1.5625); chk('VIF again', F(25, 16), 1.5625); chk('1 - r', 1 / 0.4, 2.5); chk('root', sqrt(1.5625), 1.25)
# finding 14: slope 1.4, variance 7, noise 3
chk('attenuated', 1.4 * 7 / 10, 0.98); chk('cov over var', (1.4 * 7) / (7 + 3), 0.98); chk('wrong way', 1.4 * 10 / 7, 2.0)
# finding 15: t of 3 at Sharpe 0.7
chk('years', (3 / 0.7) ** 2, 18.37, 0.005); chk('years again', F(900, 49), 18.37, 0.005); chk('no square', 3 / 0.7, 4.3, 0.05); chk('aimed at 2', (2 / 0.7) ** 2, 8.2, 0.05)
# finding 21: dropout model
chk('se of 80% on 400', sqrt(0.8 * 0.2 / 400), 0.02); chk('edge in se', (0.83 - 0.80) / 0.02, 1.5); chk('edges', 91 - 80, 11); chk('edges', 84 - 80, 4)
# question lines of the 32 behavioural items are distinct, and distinct from part 1
HERE = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'bank')
q = collections.Counter(); p = collections.Counter()
for n in range(1, 9):
    for it in json.load(open(os.path.join(B, 'behavioural-%d.json' % n)))['items']:
        if n >= 5: q[it['question']] += 1
        p[it['widget']['prompt']] += 1
good = len(q) == 32 and max(q.values()) == 1 and max(p.values()) == 1 and len(p) == 62
ok = ok and good; print('ok  ' if good else 'FAIL', '32 distinct question lines, 62 distinct prompts')
raise SystemExit(0 if ok else 1)
