"""Second read of bank part 2, statistics-1 to statistics-4: every key and every wrong value recomputed
independently of docs/reports/bank-2-s*-numbers.py (which this file does not import or read).
For each numeric item: MINE[id] = (key, {wrong id: value the named slip gives}, [(typed text, wanted outcome)]).
The script compares the stored key and wrong values with mine, checks band hygiene, and writes probes.json for
probe.mjs (the real grader). Exit 0 when content agrees; a line starting FAIL is a finding.
Run: <venv>/bin/python stats_recompute.py   then   node probe.mjs probes.json"""
import json, math, os, sys
from fractions import Fraction as F
from math import comb, sqrt, log, pi
from statistics import NormalDist

N = NormalDist()
Phi = N.cdf
HERE = os.path.dirname(os.path.abspath(__file__))
BANK = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'bank')

M = {}
# ---------- statistics-1 ----------
gaps = [4, 9, 2, 7, 5, 3]
M['es-mle-waits-between-trades'] = (F(len(gaps), sum(gaps)), {'mean-wait': F(sum(gaps), len(gaps)), 'five-gaps': F(5, sum(gaps))},
    [('1/5', 'ok'), ('0.2', 'ok'), ('0.20', 'ok'), ('.2', 'ok'), ('20%', 'ok'), ('5', 'mean-wait'), ('0.17', 'no'), ('0.167', 'five-gaps'), ('1/6', 'five-gaps')])
c = [4, 7, 9, 12]; mu = F(sum(c), 4); ss = sum((x - mu) ** 2 for x in c)
M['es-biasvar-four-closes'] = (ss / 3, {'divide-by-n': ss / 4, 'gave-sd': sqrt(ss / 3)},
    [('34/3', 'ok'), ('11.33', 'ok'), ('11.3', 'no'), ('11.333', 'ok'), ('8.5', 'divide-by-n'), ('3.37', 'gave-sd'), ('34', 'no'), ('2.92', 'no')])
M['es-intervals-halve-the-width'] = (64 * (2.94 / 1.47) ** 2, {'doubled-n': 128, 'halved-n': 32}, [('256', 'ok'), ('256 observations', 'ok'), ('128', 'doubled-n'), ('192', 'no')])
M['es-bayes-seven-in-ten'] = (F(2 + 7, 4 + 10), {'no-prior': F(7, 10), 'one-each': F(8, 12)},
    [('9/14', 'ok'), ('0.6429', 'ok'), ('0.643', 'ok'), ('0.64', 'no'), ('64.29%', 'ok'), ('0.7', 'no-prior'), ('2/3', 'one-each'), ('0.6667', 'one-each')])
tail = F(sum(comb(16, k) for k in range(13, 17)), 2 ** 16)
assert tail == F(697, 65536)
zc = (13 - 8) / 2
M['ht-pvalue-thirteen-of-sixteen'] = (2 * tail, {'one-tail': tail, 'normal-curve': 2 * (1 - Phi(zc))},
    [('697/32768', 'ok'), ('0.0213', 'ok'), ('0.021', 'ok'), ('2.13%', 'ok'), ('0.0106', 'one-tail'), ('697/65536', 'one-tail'), ('0.0124', 'normal-curve'),
     ('%.4f' % (2 * (1 - Phi((12.5 - 8) / 2))), 'no')])  # continuity-corrected normal, 0.0244
se = 12 / sqrt(36); crit = 1.645 * se
M['power-one-sided-shift'] = (1 - Phi((crit - 4) / se), {'miss-rate': Phi((crit - 4) / se), 'two-sided': 1 - Phi((1.96 * se - 4) / se)},
    [('0.6387', 'ok'), ('0.639', 'ok'), ('63.87%', 'ok'), ('0.64', 'no'), ('0.6406', 'no'), ('0.6368', 'no'), ('0.3613', 'miss-rate'), ('0.516', 'two-sided'), ('0.5160', 'two-sided')])
p32 = 2 * (1 - Phi(3.2))
assert abs(p32 - 0.001374) < 5e-7
M['multiple-testing-how-many-tests'] = (math.floor(0.05 / 0.001374), {'rounded-up': math.ceil(0.05 / 0.001374), 'one-sided': math.floor(0.05 / (0.001374 / 2))},
    [('36', 'ok'), ('37', 'rounded-up'), ('72', 'one-sided'), ('36.39', 'no'), ('73', 'no')])
M['two-regressions-two-slopes'] = (sqrt(2.5 * 0.1), {'no-root': 2.5 * 0.1, 'ratio': 0.1 / 2.5}, [('0.5', 'ok'), ('1/2', 'ok'), ('.5', 'ok'), ('0.25', 'no-root'), ('0.04', 'ratio'), ('25', 'no'), ('-0.5', 'no')])
M['rg-inference-t-from-r-squared'] = (sqrt(0.2 * 100 / 0.8), {'no-one-minus': sqrt(0.2 * 100), 'no-root': 0.2 * 100 / 0.8},
    [('5', 'ok'), ('5.0', 'ok'), ('25', 'no-root'), ('4.5', 'no-one-minus'), ('4.47', 'no-one-minus'),
     ('%.2f' % sqrt(0.2 * 102 / 0.8), 'any-no'), ('%.1f' % sqrt(0.2 * 102 / 0.8), 'ok')])  # used n, not n - 2: 5.05 refused, but 5.0 at the asked place
M['rg-multiple-left-out-factor'] = (1.5 + (-2) * 0.4, {'no-bias': 1.5, 'added-bias': 1.5 + 2 * 0.4}, [('0.7', 'ok'), ('7/10', 'ok'), ('0.70', 'ok'), ('1.5', 'no-bias'), ('2.3', 'added-bias'), ('-0.8', 'no')])
M['ts-models-ar1-long-run-variance'] = (16 / (1 - 0.6 ** 2), {'unsquared': 16 / (1 - 0.6), 'noise-only': 16}, [('25', 'ok'), ('25.0', 'ok'), ('40', 'unsquared'), ('16', 'noise-only'), ('5', 'no')])
M['ts-acf-ma1-first-lag'] = (0.75 / (1 + 0.75 ** 2), {'coefficient': 0.75, 'unsquared': 0.75 / 1.75}, [('0.48', 'ok'), ('12/25', 'ok'), ('0.75', 'coefficient'), ('0.43', 'unsquared'), ('0.4286', 'unsquared')])
M['sample-size-for-signal-sharpe-years'] = ((2 / 0.7) ** 2, {'no-square': 2 / 0.7, 'used-1-96': (1.96 / 0.7) ** 2},
    [('8.2', 'ok'), ('8.16', 'ok'), ('8.163', 'ok'), ('8.2 years', 'ok'), ('400/49', 'ok'), ('8', 'no'), ('2.9', 'no-square'), ('2.86', 'no-square'), ('7.8', 'used-1-96'), ('7.84', 'used-1-96')])
a, b = 0.28, 0.96
M['correlation-bounds-highest-third'] = (a * b + sqrt((1 - a * a) * (1 - b * b)), {'product-only': a * b, 'no-limit': 1}, [('0.5376', 'ok'), ('0.538', 'ok'), ('0.2688', 'product-only'), ('1', 'no-limit'), ('0', 'no')])
assert abs(a * b - sqrt((1 - a * a) * (1 - b * b))) < 1e-12  # floor is 0, as the explanation says
M['es-estimators-median-standard-error'] = (2 * sqrt(pi / 2) / sqrt(100), {'mean-se': 2 / sqrt(100), 'no-root': 0.2 * pi / 2},
    [('0.251', 'ok'), ('0.2507', 'ok'), ('0.25', 'ok'), ('0.2', 'mean-se'), ('0.314', 'no-root'), ('0.3142', 'no-root')])
# ---------- statistics-2 ----------
l8 = 0.8 ** 4 * 0.2; lf = 0.5 ** 5
M['es-mle-two-coins-ratio'] = (l8 / lf, {'upside-down': lf / l8, 'all-heads': 0.8 ** 5 / lf}, [('2.62', 'ok'), ('2.6214', 'ok'), ('2.6', 'no'), ('0.38', 'upside-down'), ('10.49', 'all-heads'), ('0.08192', 'no')])
M['shrinkage-mse-best-multiplier'] = (F(9, 12), {'unbiased': 1, 'equal-split': F(3, 6)}, [('0.75', 'ok'), ('3/4', 'ok'), ('1', 'unbiased'), ('0.5', 'equal-split'), ('2.25', 'no')])
sep = sqrt(0.6 * 0.4 / 400)
M['es-intervals-poll-margin'] = (196 * sep, {'used-half': 196 * sqrt(0.25 / 400), 'no-multiplier': 100 * sep},
    [('4.8', 'ok'), ('4.80', 'ok'), ('4.801', 'ok'), ('4.8 points', 'ok'), ('4.9', 'used-half'), ('2.4', 'no-multiplier'), ('2.45', 'no-multiplier'), ('0.048', 'no'), ('4.8%', 'ok'),
     ('%.1f' % (200 * sep), 'used-half')])  # multiplier 2 gives 4.9 and is told "you used p = 0.5"
pm = (0 * 0.25 + 3 * 1) / 1.25
M['es-bayes-prior-and-sample'] = (pm / 100, {'plain-average': 1.5 / 100, 'weights-swapped': (3 * 0.25) / 1.25 / 100}, [('2.4', 'ok'), ('2.4%', 'ok'), ('2.40', 'ok'), ('12/5', 'ok'), ('0.024', 'no'), ('1.5', 'plain-average'), ('0.6', 'weights-swapped'), ('2', 'no')])
M['ht-setup-ten-paired-days'] = (1.2 / (1.5 / sqrt(10)), {'no-root': 1.2 / 1.5, 'root-nine': 1.2 / (1.5 / 3)}, [('2.53', 'ok'), ('2.530', 'ok'), ('2.5', 'no'), ('0.8', 'no-root'), ('2.4', 'root-nine'), ('2.40', 'root-nine')])
M['ht-pvalue-bigger-sample'] = (2.4 * sqrt(2.25), {'times-n': 2.4 * 2.25, 'divided': 2.4 / 1.5}, [('3.6', 'ok'), ('3.60', 'ok'), ('5.4', 'times-n'), ('1.6', 'divided'), ('2.4', 'no')])
M['ht-errors-equal-error-cutoff'] = (1 - Phi(1.5), {'added-both': 2 * (1 - Phi(1.5)), 'cutoff-at-three': 1 - Phi(3)},
    [('0.0668', 'ok'), ('6.68%', 'ok'), ('0.06681', 'ok'), ('0.067', 'no'), ('0.1336', 'added-both'), ('0.0013', 'cutoff-at-three'), ('0.00135', 'cutoff-at-three'), ('0.0014', 'cutoff-at-three'), ('1.5', 'no')])
M['collinear-features-inflation-factor'] = (1 / (1 - 0.81), {'one-minus-r': 1 / (1 - 0.9), 'standard-error-factor': sqrt(1 / 0.19)}, [('5.26', 'ok'), ('100/19', 'ok'), ('5.263', 'ok'), ('5.3', 'no'), ('10', 'one-minus-r'), ('2.29', 'standard-error-factor')])
M['ts-forecast-two-steps-ahead'] = (10 + 0.36 * 5, {'one-step': 10 + 0.6 * 5, 'no-mean': 0.36 * 15}, [('11.8', 'ok'), ('11.80', 'ok'), ('13', 'one-step'), ('5.4', 'no-mean'), ('1.8', 'no'), ('15.4', 'no')])
M['ts-acf-two-day-variance-ratio'] = (1 - 0.15, {'independent': 1, 'sign': 1.15}, [('0.85', 'ok'), ('17/20', 'ok'), ('85%', 'ok'), ('1', 'independent'), ('1.15', 'sign'), ('1.7', 'no'), ('0.7', 'no')])
M['measurement-error-noisy-regressor'] = (1.2 * 5 / 8, {'no-attenuation': 1.2, 'wrong-way': 1.2 * 8 / 5}, [('0.75', 'ok'), ('3/4', 'ok'), ('1.2', 'no-attenuation'), ('1.92', 'wrong-way'), ('0.625', 'no')])
M['dl-clt-mean-of-hundred'] = (1 - Phi(2), {'no-root': 1 - Phi(0.2), 'both-tails': 2 * (1 - Phi(2))},
    [('0.0228', 'ok'), ('2.28%', 'ok'), ('0.02275', 'ok'), ('0.023', 'no'), ('0.025', 'no'), ('0.4207', 'no-root'), ('0.0455', 'both-tails'), ('0.9772', 'no')])
# ---------- statistics-3 ----------
M['es-estimators-pool-two-estimates'] = (1 / (F(1, 4) + F(1, 12)), {'equal-weights': F(4 + 12, 4), 'average-variances': 8, 'total-precision': F(1, 4) + F(1, 12)},
    [('3', 'ok'), ('3.0', 'ok'), ('4', 'equal-weights'), ('8', 'average-variances'), ('1/3', 'total-precision'), ('0.3333', 'total-precision'), ('0.33', 'no')])
M['estimator-bias-divide-by-n'] = (F(4, 5) * 10, {'no-bias': 10, 'wrong-way': F(5, 4) * 10}, [('8', 'ok'), ('8.0', 'ok'), ('10', 'no-bias'), ('12.5', 'wrong-way'), ('2', 'no')])
M['es-intervals-wider-confidence'] = (6 + 4 * 2.576 / 1.96, {'added-gap': 10 + (2.576 - 1.96), 'scaled-end': 10 * 2.576 / 1.96},
    [('11.26', 'ok'), ('11.257', 'ok'), ('11.3', 'no'), ('10.62', 'added-gap'), ('13.14', 'scaled-end'), ('5.26', 'no'), ('0.74', 'no')])
M['es-bayes-arrivals-per-day'] = (F(3 + 12, 1 + 5), {'data-only': F(12, 5), 'prior-only': 3}, [('2.5', 'ok'), ('5/2', 'ok'), ('15/6', 'ok'), ('2.4', 'data-only'), ('3', 'prior-only'), ('2.50', 'ok')])
cnt = [5, 8, 9, 8, 10, 20]
M['ht-setup-die-sixty-rolls'] = (sum((x - 10) ** 2 for x in cnt) / 10, {'not-divided': sum((x - 10) ** 2 for x in cnt), 'absolute-gaps': sum(abs(x - 10) for x in cnt) / 10},
    [('13.4', 'ok'), ('134/10', 'ok'), ('13.40', 'ok'), ('134', 'not-divided'), ('2', 'absolute-gaps'), ('20', 'no')])
M['weak-signal-daily-edge'] = (0.05 / (1 / sqrt(400)), {'no-root': 0.05 / 1, 'annual-sharpe': 0.05 / 1 * sqrt(252)}, [('1', 'ok'), ('1.00', 'ok'), ('1.0', 'ok'), ('0.05', 'no-root'), ('0.79', 'annual-sharpe'), ('0.8', 'no'), ('20', 'no')])
nn = ((1.96 + 0.8416) * 10 / 2) ** 2
M['ht-errors-sample-for-power'] = (math.ceil(nn), {'no-power': math.ceil((1.96 * 5) ** 2), 'one-sided': math.ceil(((1.645 + 0.8416) * 5) ** 2), 'rounded-down': math.floor(nn)},
    [('197', 'ok'), ('196', 'rounded-down'), ('196.2', 'no'), ('97', 'no-power'), ('155', 'one-sided'), ('393', 'no'), ('394', 'no')])
assert abs(Phi(sqrt(196) * 0.2 - 1.96) - 0.7995) < 5e-5 and Phi(sqrt(197) * 0.2 - 1.96) > 0.8
M['ht-multiple-share-false'] = (F(2, 14), {'gave-level': 0.01, 'pass-rate': F(14, 200)}, [('14.3', 'ok'), ('14.3%', 'ok'), ('14.29', 'ok'), ('1/7', 'no'), ('14', 'no'), ('1', 'gave-level'), ('7', 'pass-rate'), ('0.143', 'no'), ('85.7', 'no')])
M['rg-fit-correlation-from-sums'] = (-sqrt(1 - 50 / 200), {'sign': sqrt(0.75), 'no-root': -0.75, 'residual-share': -sqrt(50 / 200)},
    [('-0.866', 'ok'), ('−0.866', 'ok'), ('-0.8660', 'ok'), ('-0.87', 'no'), ('0.866', 'sign'), ('-0.75', 'no-root'), ('-0.5', 'residual-share'), ('0.75', 'no'), ('0.5', 'no')])
M['rg-inference-new-observation'] = (2 * sqrt(1 + 1 / 25), {'fitted-mean': 2 / 5, 'noise-only': 2}, [('2.04', 'ok'), ('2.040', 'ok'), ('2.0', 'noise-only'), ('2', 'noise-only'), ('0.4', 'fitted-mean'), ('4.16', 'no')])
M['ts-forecast-half-life'] = (log(0.5) / log(0.75), {'linear-decay': 0.5 / 0.25, 'time-scale': 1 / 0.25},
    [('2.4', 'ok'), ('2.41', 'ok'), ('2.409', 'ok'), ('2.4 days', 'ok'), ('2', 'linear-decay'), ('4', 'time-scale'), ('3', 'no'), ('%.1f' % (log(2) / 0.25), 'no')])
M['ts-acf-noise-band'] = (1.96 / sqrt(400), {'no-multiplier': 1 / 20, 'divided-by-n': 1.96 / 400},
    [('0.098', 'ok'), ('0.0980', 'ok'), ('0.1', 'no'), ('0.100', 'no'), ('0.05', 'no-multiplier'), ('0.005', 'divided-by-n'), ('0.0049', 'divided-by-n'), ('0.196', 'no')])
v = 0.2 ** 2 * (1 / 25 + (1 - 1 / 25) * 0.25)
M['equicorrelation-many-assets-vol'] = (sqrt(v), {'independent': 0.2 / 5, 'many-asset-limit': 0.2 * sqrt(0.25)}, [('10.6', 'ok'), ('10.6%', 'ok'), ('10.58', 'ok'), ('0.106', 'no'), ('4', 'independent'), ('10', 'many-asset-limit'), ('1.12', 'no'), ('11', 'no')])
# ---------- statistics-4 ----------
M['es-estimators-error-of-the-vol'] = (0.012 / sqrt(100), {'root-of-n': 0.012 / sqrt(50), 'divided-by-n': 0.012 / 50},
    [('0.12', 'ok'), ('0.12%', 'ok'), ('0.120', 'ok'), ('0.17', 'root-of-n'), ('0.1697', 'root-of-n'), ('0.02', 'divided-by-n'), ('0.024', 'divided-by-n'), ('0.0012', 'no'), ('0.1', 'no')])
M['es-mle-best-precision-rate'] = (sqrt(0.2 * 0.8 / 100), {'gave-variance': 0.2 * 0.8 / 100, 'one-trial': sqrt(0.16)}, [('0.04', 'ok'), ('1/25', 'ok'), ('4%', 'ok'), ('0.040', 'ok'), ('0.0016', 'gave-variance'), ('0.4', 'one-trial'), ('625', 'no'), ('0.02', 'no')])
seg = sqrt(4 / 50 + 4 / 50)
M['es-intervals-two-desk-gap'] = (0.8 - 1.96 * seg, {'one-mean': 0.8 - 1.96 * 2 / sqrt(50), 'upper-end': 0.8 + 1.96 * seg},
    [('0.016', 'ok'), ('£0.016', 'ok'), ('0.0160', 'ok'), ('0.02', 'no'), ('16', 'no'), ('0.246', 'one-mean'), ('1.584', 'upper-end'), ('0', 'no'), ('0.4', 'no')])
M['es-bayes-three-from-three'] = (F(1 + 3, 2 + 3), {'no-prior': 1, 'one-failure': F(3, 4)}, [('0.8', 'ok'), ('4/5', 'ok'), ('80%', 'ok'), ('1', 'no-prior'), ('0.75', 'one-failure'), ('3/4', 'one-failure')])
import itertools
vals = [8, 9, 1, 2, 3]
obs = (8 + 9) / 2 - (1 + 2 + 3) / 3
ext = sum(1 for s in itertools.combinations(range(5), 2) if (sum(vals[i] for i in s) / 2 - sum(vals[i] for i in range(5) if i not in s) / 3) >= obs - 1e-12)
assert abs(obs - 6.5) < 1e-12 and ext == 1
M['sm-nonpar-shuffled-labels'] = (F(ext, comb(5, 2)), {'ordered-pairs': F(1, 20), 'two-sided': F(2, 10)}, [('0.1', 'ok'), ('1/10', 'ok'), ('10%', 'ok'), ('0.05', 'ordered-pairs'), ('1/20', 'ordered-pairs'), ('0.2', 'two-sided'), ('1/120', 'no')])
M['ht-multiple-better-of-two'] = (1 / sqrt(pi), {'no-selection': 0, 'one-size': sqrt(2 / pi)}, [('0.564', 'ok'), ('0.5642', 'ok'), ('0.56', 'no'), ('0', 'no-selection'), ('0.798', 'one-size'), ('1.128', 'no')])
M['power-half-the-effect'] = (150 * 4, {'doubled': 300, 'root-two': 150 * sqrt(2)}, [('600', 'ok'), ('300', 'doubled'), ('212', 'root-two'), ('213', 'root-two'), ('75', 'no')])
M['rg-fit-next-year-return'] = ((6 + 0.5 * (10 / 10) * (26 - 6)) / 100, {'no-pull': 0.26, 'halved-return': 0.13}, [('16', 'ok'), ('16%', 'ok'), ('16.0', 'ok'), ('0.16', 'no'), ('26', 'no-pull'), ('13', 'halved-return'), ('19', 'no'), ('10', 'no')])
M['rg-inference-overall-f'] = (F(3, 10) / 3 / (F(7, 10) / 40), {'df-41': 0.1 / (0.7 / 41), 'no-df': 0.3 / 0.7}, [('5.71', 'ok'), ('40/7', 'ok'), ('5.714', 'ok'), ('5.7', 'no'), ('5.86', 'df-41'), ('0.43', 'no-df'), ('%.2f' % (0.1 / (0.7 / 44)), 'no')])
M['rg-multiple-dummy-and-slope'] = (3 + 2 * 2 + 4 + 1.5 * 2, {'no-interaction': 3 + 4 + 4, 'other-group': 3 + 4}, [('14', 'ok'), ('14.0', 'ok'), ('11', 'no-interaction'), ('7', 'other-group'), ('10', 'no')])
M['gv-models-ewma-after-a-shock'] = (sqrt(0.94 * 1 + 0.06 * 9) / 100, {'averaged-vols': (0.94 + 0.18) / 100, 'weights-swapped': sqrt(0.06 + 0.94 * 9) / 100},
    [('1.22', 'ok'), ('1.22%', 'ok'), ('1.217', 'ok'), ('1.2', 'no'), ('1.48', 'no'), ('1.12', 'averaged-vols'), ('2.92', 'weights-swapped'), ('0.0122', 'no')])
lr = 0.0000045 / (1 - 0.10 - 0.88)
M['gv-forecast-long-run-vol'] = (sqrt(lr), {'annualised': sqrt(lr) * sqrt(252), 'one-minus-beta': sqrt(0.0000045 / 0.12)},
    [('1.5', 'ok'), ('1.5%', 'ok'), ('1.50', 'ok'), ('0.015', 'no'), ('23.8', 'annualised'), ('0.6', 'one-minus-beta'), ('0.61', 'one-minus-beta'), ('0.0225', 'no'), ('0.02', 'no')])

# ---------- compare with content ----------
fails = 0; probes = []; seen = set()
def fail(msg):
    global fails; fails += 1; print('FAIL', msg)
for n in (1, 2, 3, 4):
    fid = 'statistics-%d' % n
    for it in json.load(open(os.path.join(BANK, fid + '.json')))['items']:
        w = it['widget']
        if w['kind'] != 'numeric': continue
        if it['id'] not in M: fail('no independent value for ' + it['id']); continue
        seen.add(it['id'])
        key, wr, pr = M[it['id']]
        tol = w['tol'].get('abs', 0)
        if abs(float(key) - w['answer']) > 1e-4 * max(1, abs(float(key))) and abs(float(key) - w['answer']) > tol / 10 + 1e-12:
            fail('%s key stored %r, mine %r' % (it['id'], w['answer'], float(key)))
        ids = {x['id'] for x in w.get('wrong', [])}
        if ids != set(wr): fail('%s wrong ids %s, mine %s' % (it['id'], sorted(ids), sorted(wr)))
        bands = [(w['answer'] - tol, w['answer'] + tol, 'key')]
        for x in w.get('wrong', []):
            t = x['tol'].get('abs', 0)
            if x['id'] in wr and abs(float(wr[x['id']]) - x['value']) > t + 1e-9:
                fail('%s wrong %s stored %r but the named slip gives %r (band %r)' % (it['id'], x['id'], x['value'], float(wr[x['id']]), t))
            if x['id'] not in it['feedback'].get('byKey', {}): fail('%s wrong %s has no byKey line' % (it['id'], x['id']))
            bands.append((x['value'] - t, x['value'] + t, x['id']))
        bands.sort()
        for (lo1, hi1, a1), (lo2, hi2, a2) in zip(bands, bands[1:]):
            if hi1 >= lo2 - 1e-12: fail('%s bands touch: %s and %s' % (it['id'], a1, a2))
        for text, want in pr: probes.append({'file': fid, 'id': it['id'], 'text': text, 'want': want})
for k in M:
    if k not in seen: fail('item not found in content: ' + k)
json.dump(probes, open(os.path.join(HERE, 'probes.json'), 'w'), indent=0)
print('%d numeric items compared, %d probes written, %d failed' % (len(seen), len(probes), fails))
sys.exit(1 if fails else 0)
