"""info level 3 (mutual information): every stated number computed twice and found in the JSON.
Method A: I = H(X) + H(Y) - H(X, Y); method B: I = D(p_XY || p_X p_Y) (or H(Y) - H(Y | X) where named).
The l12 simulation is rerun with numpy's default_rng(2026), 2,000 runs per sample size, null and signal drawn in turn (as in
docs/briefs/ai-s0s1-scripts/info3.py); its bias figures are checked against the first-order formula.
Code widgets: each solution is run in CPython on its hidden tests (and each starter must fail one).
Run: <venv>/bin/python docs/reports/info-L3-numbers.py"""
import sys, os, math, json, shutil, tempfile, contextlib, io
from collections import Counter
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import Level

APP = os.path.join(HERE, '..', '..', 'app')
lv = Level('info', 3)
LN2, ln, L2 = math.log(2), math.log, math.log2
E = lambda f, path, v: lv.expect(f, path, v)


def two(a, b, places, label):
    ok = round(a, places) == round(b, places)
    lv.claim(ok, f'{label}: {a!r} and {b!r} agree to {places} places')
    return round(a, places)


def H(p):
    p = np.asarray(p, float).ravel(); p = p[p > 0]; return float(-(p * np.log2(p)).sum())


def miA(J):
    J = np.asarray(J, float); J = J / J.sum(); return H(J.sum(1)) + H(J.sum(0)) - H(J)


def miB(J):
    J = np.asarray(J, float); J = J / J.sum(); px = J.sum(1, keepdims=True); py = J.sum(0, keepdims=True)
    m = J > 0; return float((J[m] * np.log2(J[m] / (px * py)[m])).sum())


h2 = lambda p: H([p, 1 - p])
CT = [[.3, .2], [.2, .3]]
# ---------------- l9 ----------------
E('l9', 'screens[0].widget.answer', two(h2(.6), -(.6 * ln(.6) + .4 * ln(.4)) / LN2, 3, 'H(0.6)'))
E('l9', 'screens[0].widget.wrong[1].value', two(h2(.6) * LN2, -(.6 * ln(.6) + .4 * ln(.4)), 3, 'H(0.6) nats'))
for J, cap, left in [([[.25, .25], [.25, .25]], 0, 1), (CT, 1, h2(.6)), ([[.4, .1], [.1, .4]], 2, h2(.8)), ([[.5, 0], [0, .5]], 3, 0)]:
    E('l9', f'screens[1].canvas.controls[0].frames[{cap}].caption', two(1 - miA(J), left, 3, f'doubt left {cap}'))
E('l9', 'screens[2].widget.answer', two(H(CT), -(0.6 * ln(.3) + .4 * ln(.2)) / LN2, 3, 'H(X,Y) course'))
E('l9', 'screens[2].widget.wrong[2].value', two(H(CT) * LN2, -(0.6 * ln(.3) + .4 * ln(.2)), 3, 'H(X,Y) nats'))
E('l9', 'screens[3].widget.answer', two(miA(CT), miB(CT), 3, 'course MI'))
E('l9', 'screens[4].widget.rows[2][4]', two(miA(CT), 1 - h2(.6), 3, 'course MI row'))
E('l9', 'screens[5].widget.answer', two(miA([[.4, .1], [.1, .4]]), 1 - h2(.8), 3, '80% MI'))
E('l9', 'screens[5].prose', two(h2(.8), -(.8 * ln(.8) + .2 * ln(.2)) / LN2, 3, 'H(0.8)'))
E('l9', 'screens[7].prose', two(L2(6), ln(6) / LN2, 3, 'log2 6'))
J55 = [[.275, .225], [.225, .275]]
E('l9', 'screens[10].widget.answer', two(miA(J55), 1 - h2(.55), 3, '55% MI'))
E('l9', 'screens[10].widget.wrong[2].value', two(h2(.55), -(.55 * ln(.55) + .45 * ln(.45)) / LN2, 3, 'H(0.55)'))
E('l9', 'screens[10].feedback.correct', two(250 * miA(J55), 250 * miB(J55), 1, 'bits a year at 55%'))
lv.claim(3.9 < miA(CT) / miA(J55) < 4.1, 'half the edge gives about a quarter of the bits')
E('l9', 'screens[9].widget.tests[4].expect', two(miA([[0, 1 / 3], [1 / 3, 0], [0, 1 / 3]]), H([1 / 3, 2 / 3]), 10, 'Y = X^2 in code test'))
E('l9', 'screens[9].widget.tests[5].expect', two(miA([[40, 5], [30, 25], [5, 45]]), miB([[40, 5], [30, 25], [5, 45]]), 10, 'links in code test'))
# ---------------- l10 ----------------
SQ = [[0, 1 / 3], [1 / 3, 0], [0, 1 / 3]]
E('l10', 'screens[0].widget.rows[0][1].answer', two(1 / 9, (1 / 3) * (1 / 3), 3, '1/9'))
E('l10', 'screens[0].widget.rows[0][2].answer', two(2 / 9, (1 / 3) * (2 / 3), 3, '2/9'))
xs, ys = np.array([-1, 0, 1]), np.array([0, 1])
Jsq = np.array(SQ)
cov = (Jsq * np.outer(xs, ys)).sum() - (Jsq.sum(1) * xs).sum() * (Jsq.sum(0) * ys).sum()
lv.claim(abs(cov) < 1e-15, 'Y = X^2 has covariance 0')
E('l10', 'screens[3].widget.answer', two(miB(CT), .6 * L2(1.2) + .4 * L2(.8), 3, 'course as KL'))
E('l10', 'screens[3].widget.wrong[0].value', two(.6 * L2(1.2) - .4 * L2(.8), .6 * ln(1.2) / LN2 + .4 * -ln(.8) / LN2, 3, 'abs sum'))
E('l10', 'screens[3].widget.wrong[1].value', two(.3 * L2(1.2), .3 * ln(1.2) / LN2, 3, 'one cell'))
E('l10', 'screens[3].widget.wrong[2].value', two(miB(CT) * LN2, .6 * ln(1.2) + .4 * ln(.8), 3, 'course nats'))
E('l10', 'screens[3].feedback.correct', two(L2(1.2), ln(1.2) / LN2, 3, 'log2 1.2'))
E('l10', 'screens[4].widget.answer', two(miB(SQ), 2 / 3 * L2(1.5) + 1 / 3 * L2(3), 3, 'Y = X^2 as KL'))
E('l10', 'screens[4].widget.wrong[1].value', two(L2(3), ln(3) / LN2, 3, 'H(X) log2 3'))
E('l10', 'screens[4].widget.wrong[2].value', two(miA(SQ) * LN2, 2 / 3 * ln(1.5) + 1 / 3 * ln(3), 3, 'Y=X^2 nats'))
VOL = [[.05, .4, .05], [.15, .2, .15]]
E('l10', 'screens[9].widget.answer', two(miA(VOL), miB(VOL), 3, 'vol MI'))
E('l10', 'screens[9].widget.wrong[1].value', two(miA(VOL) * LN2, miB(VOL) * LN2, 3, 'vol nats'))
E('l10', 'screens[9].explain.text', two(H([.2, .6, .2]), -(.4 * ln(.2) + .6 * ln(.6)) / LN2, 3, 'H(Y) vol'))
E('l10', 'screens[9].explain.text', two(H(VOL), -(.1 * ln(.05) + .4 * ln(.4) + .3 * ln(.15) + .2 * ln(.2)) / LN2, 3, 'H(X,Y) vol'))
cv = sum(VOL[i][j] * i * r for i in range(2) for j, r in enumerate([-1, 0, 1])) - 0.5 * sum(sum(VOL[i][j] for i in range(2)) * r for j, r in enumerate([-1, 0, 1]))
lv.claim(abs(cv) < 1e-15, 'volatility signal uncorrelated with the return')
E('l10', 'quiz[2].widget.answer', two(.1 * L2(.1 / (.5 * .4)), -.1, 3, 'negative cell'))
# ---------------- l11 ----------------
LK = [[40, 5], [30, 25], [5, 45]]
rows = [h2(a / (a + b)) for a, b in LK]
for v in rows:
    E('l11', 'screens[1].prose', two(v, v, 3, 'row entropy'))
lv.claim([round(v, 3) for v in rows] == [0.503, 0.994, 0.469], 'row entropies 0.503, 0.994, 0.469')
cond = sum((a + b) / 150 * v for (a, b), v in zip(LK, rows))
E('l11', 'screens[1].widget.answer', two(miA(LK), 1 - cond, 3, 'links MI'))
E('l11', 'screens[1].widget.wrong[0].value', two(cond, 1 - miB(LK), 3, 'links conditional'))
E('l11', 'screens[1].widget.wrong[1].value', two(1 - sum(rows) / 3, 1 - (rows[0] + rows[1] + rows[2]) / 3, 3, 'unweighted'))
E('l11', 'screens[0].explain.text', two(miA([[55, 20], [20, 55]]), miB([[55, 20], [20, 55]]), 3, 'contacts MI'))
E('l11', 'screens[0].explain.text', two(miA([[25, 30], [50, 45]]), miB([[25, 30], [50, 45]]), 3, 'attachment MI'))
MG = [[70, 30], [5, 45]]
E('l11', 'screens[2].widget.answer', two(miA(MG), 1 - (2 / 3 * h2(.7) + 1 / 3 * h2(.1)), 3, 'merged MI'))
E('l11', 'screens[2].widget.wrong[1].value', two(miA(MG) * LN2, miB(MG) * LN2, 3, 'merged nats'))
E('l11', 'screens[2].feedback.correct', two(miA(LK) - miA(MG), miB(LK) - miB(MG), 3, 'lost by merging'))
E('l11', 'screens[3].widget.answer', two(1 - h2(.1), miB([[.45, .05], [.05, .45]]), 3, 'I(X;Y) chain'))
E('l11', 'screens[3].widget.wrong[2].value', two((1 - h2(.1)) * LN2, miB([[.45, .05], [.05, .45]]) * LN2, 3, 'chain nats'))
lv.claim(abs(0.1 * 0.9 + 0.9 * 0.1 - 0.18) < 1e-12, 'combined flip 0.18')
E('l11', 'screens[4].widget.answer', two(1 - h2(.18), miB([[.41, .09], [.09, .41]]), 3, 'I(X;Z) chain'))
E('l11', 'screens[4].widget.wrong[0].value', two((1 - h2(.1)) ** 2, miB([[.45, .05], [.05, .45]]) ** 2, 3, 'squared'))
E('l11', 'screens[4].feedback.correct', two(h2(.18), -(.18 * ln(.18) + .82 * ln(.82)) / LN2, 3, 'H(0.18)'))
SG = [[30, 45], [48, 52], [52, 48], [45, 30]]
E('l11', 'screens[9].prose', two(miA(SG), miB(SG), 4, 'four bins'))
E('l11', 'screens[9].widget.answer', two(miA([[78, 97], [97, 78]]), miB([[78, 97], [97, 78]]), 4, 'low against high'))
lv.claim(abs(miA([[75, 75], [100, 100]])) < 1e-12, 'extreme against middle keeps 0')
E('l11', 'screens[9].widget.wrong[2].value', two(miA([[78, 97], [97, 78]]) * LN2, miB([[78, 97], [97, 78]]) * LN2, 4, 'low-high nats'))
E('l11', 'quiz[1].widget.answer', two(1 - h2(.2), miB([[.4, .1], [.1, .4]]), 3, 'flip 0.2'))
# ---------------- l12: the simulation ----------------
pu = np.array([0.47, 0.50, 0.53]); Js = np.stack([(1 - pu) / 3, pu / 3], axis=1)
true = two(miA(Js), miB(Js), 5, 'weak signal true MI')
lv.claim(round(miA(Js) * LN2, 6) == 0.001201, 'true MI in nats 0.001201')


def plug(s, y, kx=3, ky=2):
    J = np.zeros((kx, ky)); np.add.at(J, (s, y), 1); return miA(J)


rng = np.random.default_rng(2026)
sim = {}
for n in (250, 1000, 5000):
    en, es = [], []
    for _ in range(2000):
        s = rng.integers(0, 3, n)
        y0 = (rng.random(n) < 0.5).astype(int); en.append(plug(s, y0))
        y1 = (rng.random(n) < pu[s]).astype(int); es.append(plug(s, y1))
    sim[n] = (np.array(en), np.array(es))
bias = lambda n, kx=3, ky=2: (kx - 1) * (ky - 1) / (2 * n * LN2)
NS = lv.files['l12-a-signal-and-tomorrow']['screens'][1]['canvas']['controls'][0]['frames'][1]['values']
for n, key in [(250, 'x250'), (1000, 'x1000'), (5000, 'x5000')]:
    en, es = sim[n]
    lv.claim(round(float(en.mean()), 5) == round(NS['null'][key], 5), f'null mean {n} = {NS["null"][key]}')
    lv.claim(round(float(es.mean()), 5) == round(NS['weak'][key], 5), f'signal mean {n} = {NS["weak"][key]}')
    lv.claim(abs(en.mean() - bias(n)) < 0.15 * bias(n), f'null mean {n} near the formula {bias(n):.5f}')
E('l12', 'screens[2].widget.answer', two(bias(250), 2 / (500 * LN2), 5, 'bias 250'))
E('l12', 'screens[2].widget.wrong[0].value', two(bias(250) * LN2, 2 / 500, 3, 'bias nats'))
E('l12', 'screens[2].widget.wrong[1].value', two(6 / (500 * LN2), 3 * bias(250), 5, 'k product'))
E('l12', 'screens[2].feedback.correct', two(float(sim[250][0].mean()), float(np.mean(sim[250][0])), 4, 'simulated null 250'))
E('l12', 'screens[3].widget.answer', two(float(sim[250][1].mean()) - bias(250), 0.00763 - 0.00577, 5, 'corrected 250'))
E('l12', 'screens[3].explain.text', two(float(sim[1000][1].mean()) - bias(1000), 0.00314 - 0.00144, 5, 'corrected 1000'))
E('l12', 'screens[3].explain.text', two(float(sim[5000][1].mean()) - bias(5000), float(np.sum(sim[5000][1])) / 2000 - 1 / (5000 * LN2), 5, 'corrected 5000'))
E('l12', 'screens[3].widget.wrong[1].value', two(0.00763 + 0.00577, float(sim[250][1].mean()) + bias(250), 4, 'added'))
E('l12', 'screens[4].widget.answer', two(bias(5000), bias(250) / 20, 5, 'bias 5000'))
E('l12', 'screens[4].widget.wrong[1].value', two(2 / 10000, bias(5000) * LN2, 4, 'bias 5000 nats'))
E('l12', 'screens[4].feedback.correct', two(float(sim[5000][1].mean()) - bias(5000), float(np.sum(sim[5000][1])) / 2000 - 1 / (5000 * LN2), 5, 'corrected 5000 in feedback'))
for n, txt in [(250, 73.7), (1000, 30)]:
    E('l12', 'screens[5].explain.text', two(100 * float((sim[n][0] > miA(Js)).mean()), 100 * float(np.sum(sim[n][0] > miB(Js)) / 2000), 1 if n == 250 else 0, f'share above truth {n}'))
lv.claim(int(np.sum(sim[5000][0] > miA(Js))) == 5, '5 runs of 2,000 on 5,000 days')
E('l12', 'screens[5].hints[2].text', two(float(np.sum(sim[250][0] > miA(Js))), 0.7365 * 2000, 0, '1,473 runs'))
NULL = lv.files['l12-a-signal-and-tomorrow']['screens'][5]['canvas']['params']['data']
lv.claim(len(NULL) == 2000 and max(abs(a - b) for a, b in zip(NULL, sim[250][0])) < 1e-6, 'histogram data are the 250-day null runs')
E('l12', 'screens[6].widget.options', two(3 / (1000 * LN2), bias(500, 4), 5, 'k4 n500'))
E('l12', 'screens[6].widget.options', two(1 / (1000 * LN2), bias(500, 2), 5, 'k2 n500'))
E('l12', 'screens[6].widget.options', two(3 / (500 * LN2), bias(250, 4), 5, 'k4 n250'))
E('l12', 'screens[7].widget.options', two(0.004 - bias(250, 2), 0.004 - 1 / (500 * LN2), 4, 'A corrected'))
E('l12', 'screens[7].widget.options', two(0.012 - bias(250, 6), 0.012 - 5 / (500 * LN2), 4, 'B corrected'))
E('l12', 'screens[7].explain.text', two(bias(250, 6), 5 / (500 * LN2), 4, 'B bias'))
E('l12', 'screens[10].widget.answer', two(bias(250, 4), 3 / (500 * LN2), 4, 'backtest bias'))
E('l12', 'screens[10].feedback.correct', two(0.011 - bias(250, 4), 0.011 - 3 / (500 * LN2), 4, 'backtest left'))
E('l12', 'quiz[0].widget.answer', two(bias(1000, 2), 1 / (2000 * LN2), 5, 'quiz bias'))
import random
r = random.Random(11); s11 = [r.randrange(3) for _ in range(250)]; y11 = [r.randrange(2) for _ in range(250)]
J11 = np.zeros((3, 2)); np.add.at(J11, (s11, y11), 1)
E('l12', 'screens[9].explain.text', two(miA(J11), miB(J11), 4, 'seed 11 plug-in'))
E('l12', 'screens[9].explain.text', two(miA(J11) - bias(250), miB(J11) - bias(250), 4, 'seed 11 corrected'))
# ---------------- review ----------------
E('review', 'items[2].widget.answer', two(1 - h2(.7), miB([[.35, .15], [.15, .35]]), 3, '70% MI'))
E('review', 'items[3].widget.answer', two(.15 * L2(.15 / (.3 * .25)), .15 * ln(2) / LN2, 2, 'KL cell'))
E('review', 'items[5].widget.answer', two(bias(400, 6), 5 / (800 * LN2), 4, 'six-state bias'))
E('review', 'items[5].widget.wrong[0].value', two(6 / (800 * LN2), 1.2 * bias(400, 6), 4, 'k slip'))
E('review', 'items[6].explain.text', two(H([2 / 3, 1 / 3]), miA(SQ), 3, 'size info'))
E('review', 'items[8].widget.answer', two(0.010 - bias(300, 4), 0.010 - 3 / (600 * LN2), 4, 'corrected 300'))
E('review', 'items[8].widget.wrong[2].value', two(0.010 - bias(300, 3), 0.010 - 2 / (600 * LN2), 4, 'three-state slip'))
lv.claim(all(abs(a - b) < 1e-12 for a, b in zip([.12, .28, .18, .42], [.4 * .3, .4 * .7, .6 * .3, .6 * .7])), 'review table is a product')
# ---------------- homework ----------------
E('homework', 'items[4].widget.answer', two(1 - h2(.26), miB([[.37, .13], [.13, .37]]), 3, 'two flips'))
E('homework', 'items[4].widget.wrong[0].value', two(1 - h2(.2), miB([[.4, .1], [.1, .4]]), 3, 'first copy'))
E('homework', 'items[4].widget.wrong[1].value', two(1 - h2(.3), 1 - h2(.7), 3, 'flips added'))
J6 = [[.2, .1], [.1, .6]]
E('homework', 'items[5].widget.answer', two(miA(J6), miB(J6), 3, 'fresh table'))
E('homework', 'items[5].widget.wrong[0].value', two(H(J6), -(.2 * ln(.2) + .2 * ln(.1) + .6 * ln(.6)) / LN2, 3, 'fresh joint'))
E('homework', 'items[5].explain.text', two(h2(.3), h2(.7), 3, 'fresh margins'))
lv.claim(0.017 < np.quantile(sim[250][0], 0.95) < 0.019, '250-day null 95th percentile near 0.018 (model answer)')
# ---------------- problem set ----------------
OF = [[30, 40, 30], [10, 40, 50]]
E('problems', 'items[0].parts[0].widget.answer', two(80 / 200, np.array(OF).sum(0)[2] / 200, 1, 'share rose'))
E('problems', 'items[0].parts[1].widget.answer', two(H([.2, .4, .4]), -(.2 * ln(.2) + .8 * ln(.4)) / LN2, 3, 'H outcome'))
E('problems', 'items[0].parts[1].widget.wrong[1].value', two(H([.2, .4, .4]) * LN2, -(.2 * ln(.2) + .8 * ln(.4)), 3, 'H outcome nats'))
E('problems', 'items[0].parts[2].widget.answer', two(H(np.array(OF) / 200), -(2 * .15 * ln(.15) + 2 * .2 * ln(.2) + .05 * ln(.05) + .25 * ln(.25)) / LN2, 3, 'H cells'))
E('problems', 'items[0].parts[3].widget.answer', two(miA(OF), miB(OF), 3, 'order-flow MI'))
MF = [[70, 30], [50, 50]]
E('problems', 'items[1].parts[0].widget.answer', two(miA(MF), miB(MF), 3, 'merged MI'))
E('problems', 'items[1].parts[0].widget.wrong[1].value', two(miA(MF) * LN2, miB(MF) * LN2, 3, 'merged nats'))
E('problems', 'items[1].parts[0].explain.text', two(H(np.array(MF) / 200), -(.35 * ln(.35) + .15 * ln(.15) + .5 * ln(.25)) / LN2, 3, 'merged cells'))
E('problems', 'items[1].parts[1].widget.answer', two(bias(200, 2, 3), 2 / (400 * LN2), 4, 'bias 2x3'))
E('problems', 'items[1].parts[1].widget.wrong[0].value', two(bias(200, 2, 2), 1 / (400 * LN2), 4, 'bias 2x2'))
E('problems', 'items[1].parts[2].widget.answer', two(miA(OF) - bias(200, 2, 3), miB(OF) - 2 / (400 * LN2), 3, 'corrected 2x3'))
E('problems', 'items[1].parts[3].widget.answer', two(miA(MF) - bias(200, 2, 2), miB(MF) - 1 / (400 * LN2), 3, 'corrected 2x2'))
E('problems', 'items[2].parts[0].widget.answer', two(1 - h2(.05), miB([[.475, .025], [.025, .475]]), 3, 'relay 1'))
E('problems', 'items[2].parts[1].widget.answer', two(.05 * .8 + .95 * .2, 1 - (.05 * .2 + .95 * .8), 2, 'relay flip'))
E('problems', 'items[2].parts[2].widget.answer', two(1 - h2(.23), miB([[.385, .115], [.115, .385]]), 3, 'relay 2'))
E('problems', 'items[2].parts[2].widget.wrong[1].value', two(1 - h2(.2), miB([[.4, .1], [.1, .4]]), 3, 'second relay only'))
# ---------------- code widgets: solution passes, starter fails, in CPython ----------------
def code_widgets():
    for fid, doc in lv.files.items():
        def walk(n, p):
            if isinstance(n, dict):
                if n.get('kind') == 'code':
                    yield fid, p, n
                for k, v in n.items():
                    yield from walk(v, f'{p}.{k}')
            elif isinstance(n, list):
                for i, v in enumerate(n):
                    yield from walk(v, f'{p}[{i}]')
        yield from walk(doc, '')


def run(src, w, case):
    ns = {}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(w.get('prelude', ''), ns)
        exec(src, ns)
        exec(w.get('postlude', ''), ns)
        if case.get('setup'):
            exec(case['setup'], ns)
        if case.get('compare') == 'raises':
            try:
                eval(case['call'], ns)
            except Exception as e:
                return type(e).__name__ == case['expect'] or any(c.__name__ == case['expect'] for c in type(e).__mro__)
            return False
        got = eval(case['call'], ns)
    exp = eval(case['expect'])
    if case.get('compare') == 'equal':
        return got == exp
    tol = case.get('tol', {})

    def close(g, e):
        if isinstance(e, dict):
            return isinstance(g, dict) and set(g) == set(e) and all(close(g[k], e[k]) for k in e)
        if isinstance(e, (list, tuple)):
            return isinstance(g, (list, tuple)) and len(g) == len(e) and all(close(x, y) for x, y in zip(g, e))
        try:
            return math.isclose(g, e, rel_tol=tol.get('rel', 0 if 'abs' in tol else 1e-9), abs_tol=tol.get('abs', 1e-12))
        except TypeError:
            return False
    return close(got, exp)


cwd = os.getcwd()
tmp = tempfile.mkdtemp()
try:
    os.chdir(tmp)
    for fid, path, w in code_widgets():
        for name, src in w.get('data', {}).items():
            shutil.copy(os.path.join(APP, src), os.path.join(tmp, name))
        cases = w['tests'] + w.get('examples', [])
        res = []
        for c in cases:
            try:
                res.append(run(w['solution'], w, c))
            except Exception:
                res.append(False)
        lv.claim(all(res), f'{fid}{path}: solution passes {len(cases)} cases', f'failing cases {[i for i, r in enumerate(res) if not r]}')
        bad = []
        for c in w['tests']:
            try:
                bad.append(not run(w['starter'], w, c))
            except Exception:
                bad.append(True)
        lv.claim(any(bad), f'{fid}{path}: starter fails a hidden test')
finally:
    os.chdir(cwd)
    shutil.rmtree(tmp)

# Table totals: every canvas table whose last row is "Total" must add up (rows, columns and the grand total).
import glob as _glob


def _num(s):
    try:
        return float(str(s).replace(',', '').strip())
    except ValueError:
        return None


def _tables(o, path):
    if isinstance(o, dict):
        p = o.get('params')
        if o.get('kind') == 'table' and isinstance(p, dict) and isinstance(p.get('rows'), list):
            yield path, p
        for k, v in o.items():
            yield from _tables(v, path + [k])
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _tables(v, path + [i])


def check_table_totals(names):
    for name in names:
        for fn in sorted(_glob.glob(os.path.join(APP, 'content', 'courses', 'info', name + '.json'))):
            d = json.load(open(fn))
            for path, p in _tables(d, []):
                rows = p['rows']
                if not rows or str(rows[-1][0]).strip().lower() != 'total':
                    continue
                grid = [[_num(c) for c in r[1:]] for r in rows]
                if any(v is None for r in grid for v in r):
                    continue
                where = f'{os.path.basename(fn)}{path}'
                body, tot = grid[:-1], grid[-1]
                for i, r in enumerate(body):
                    lv.claim(abs(sum(r[:-1]) - r[-1]) < 1e-9, f'{where}: row {i} total {r[-1]} is the sum of its cells {sum(r[:-1])}')
                for j in range(len(tot) - 1):
                    s = sum(r[j] for r in body)
                    lv.claim(abs(s - tot[j]) < 1e-9, f'{where}: column {j} total {tot[j]} is the sum of its cells {s}')
                s = sum(r[-1] for r in body)
                lv.claim(abs(s - tot[-1]) < 1e-9, f'{where}: grand total {tot[-1]} is the sum of the row totals {s}')


check_table_totals(['l9-*', 'l10-*', 'l11-*', 'l12-*', 'review-3', 'homework-3', 'problems-3'])

lv.check_wrongs()
lv.report()
