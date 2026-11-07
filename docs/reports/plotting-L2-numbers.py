"""Number recompute for plotting level 2 (Returns and risk): l5 to l8, review-2, homework-2. Second reader, session V.

Every graded key, every numeric wrong[] value and the numbers stated in prose, hints, feedback and explanations are
recomputed from the lesson data with the standard library (statistics.stdev is the sample sd that pandas' rolling std
uses; the t(4) model in l6 uses its closed-form CDF). Checks tied to a sentence (lv.stated) fail while a false sentence is
still in the text and pass once a fix rewords it. Code behaviour and the seeded test data (numpy default_rng) were checked
in CPython with matplotlib 3.8.4, numpy 2.0.2 and pandas 2.2.3 (the Pyodide 0.27.7 versions).
Run from anywhere:  python3 docs/reports/plotting-L2-numbers.py
Failing checks on the current content are findings in docs/reviews/review-plotting-1-3.md.
"""
import sys, os, math, statistics as st, datetime as dt
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("plotting", 2)
r2 = lambda x: round(x, 2)
R252 = math.sqrt(252)


def rets(p):
    return [b / a - 1 for a, b in zip(p, p[1:])]


def roll_sd(x, n):
    return [None] * (n - 1) + [st.stdev(x[i - n + 1:i + 1]) for i in range(n - 1, len(x))]


# ---------- l5 ----------
l5 = lv.files['l5-returns-chart']
p5 = l5['screens'][0]['canvas']['params']['series'][0]['values']
r5 = rets(p5)
big = max(range(len(r5)), key=lambda i: abs(r5[i]))
lv.claim(big + 2 == 6 and l5['screens'][0]['widget']['answer'] == ['d6'], 'l5 screens[0]: the largest move is day 6')
lv.expect('l5', 'screens[0].feedback.correct', r2(-100 * r5[4]), fmt='{:.2f}%')
lv.expect('l5', 'screens[0].feedback.byKey.d10', r2(-100 * r5[8]), fmt='{:.2f}%')
lv.expect('l5', 'screens[0].feedback.byKey.d8', r2(-100 * r5[6]), fmt='{:.2f}%')
lv.expect('l5', 'screens[0].feedback.byKey.d4', r2(100 * r5[2]), fmt='{:.2f}%')
for i, d in ((2, 4), (4, 6), (6, 8)):
    lv.expect('l5', 'screens[0].hints[2].text', r2(abs(p5[d - 1] - p5[d - 2])))
canvas_r = l5['screens'][1]['canvas']['right']['params']['series'][0]['values'][1:]
lv.claim(all(abs(a - round(b, 5)) < 1e-9 for a, b in zip(canvas_r, r5)), 'l5 screens[1]: lower panel values are the daily returns')
lv.expect('l5', 'screens[2].widget.answer', round(r5[4], 6))
lv.expect('l5', 'screens[2].widget.wrong[0].value', -(p5[4] - p5[5]) / 100)        # £2.80 typed as 2.80%
lv.expect('l5', 'screens[2].widget.wrong[2].value', round(-(p5[4] - p5[5]) / p5[5], 4))
# x positions: days start at 1, so the first return belongs at x = 2; plot(rets) puts it at x = 0
shift = 2 - 0
lv.stated('l5', 'screens[3].explain.text', 'slide every return a day to the left', shift == 1)
lv.stated('l5', 'screens[3].feedback.byKey.test-3', 'one day early', shift == 1)
lv.stated('l5', 'quiz[1].widget.options[3].why', 'each one place to the left', shift == 1)
lv.claim_text('l5', 'quiz[1].explain.text', 'two places left', shift == 2)
v = l5['screens'][4]['canvas']['state']['values']
b = [v[str(i)] for i in range(1, 41)]
lv.expect('l5', 'screens[4].widget.options[3].why', round(sum(b[20:]), 2), fmt='+{:.2f}%')
lv.expect('l5', 'screens[4].hints[2].text', sum(abs(x) > 1 for x in b[20:]))
lv.claim(sum(abs(x) > 1 for x in b[:20]) == 1 and abs(b[8]) > 1, 'l5 hints: days 1 to 20 have one bar over 1%, day 9')
lv.claim(sum(abs(x) < 0.6 for x in b[:20]) >= 17, 'l5 explain: days 1 to 20 mostly move under 0.6%')
# screens[6]: £ changes on a £20 and an £80 share
for start, keys, off in ((20.0, [str(k) for k in range(1, 7)], 0), (80.0, [str(k) for k in range(501, 507)], 6)):
    ch = [l5['screens'][6]['canvas']['left']['state']['values'][k] for k in keys]
    price, out = start, []
    for c in ch:
        out.append(round(100 * c / price, 2))
        price += c
    shown = [l5['screens'][6]['explain']['canvas']['right']['values'][k] for k in keys]
    lv.claim(all(abs(a - b_) <= 0.011 for a, b_ in zip(out, shown)), f'l5 screens[6]: returns from £{start:.0f} recompute {out}')
lv.claim(abs(0.30 / 20.12 - 1.21 / 80.47) < 0.0005, 'l5 screens[6] early why: £0.30 off £20 and £1.21 off £80 are both 1.5%')
lv.expect('l5', 'quiz[0].widget.answer', round(81.90 / 84.00 - 1, 6))
lv.expect('l5', 'quiz[0].widget.wrong[0].value', -(84.00 - 81.90) / 100)
lv.expect('l5', 'quiz[0].widget.wrong[2].value', round(-(84.00 - 81.90) / 81.90, 5))
closes8 = [21.24, 21.51, 20.99, 21.13, 20.68]
lv.claim([round(x, 4) for x in rets(closes8)] == [0.0127, -0.0242, 0.0067, -0.0213], 'l5 screens[8] test-3 heights recompute')
lv.check_wrongs('l5')

# ---------- l6 ----------
l6 = lv.files['l6-shape-of-returns']
rows = [float(r[1].replace('−', '-')) for r in l6['screens'][0]['canvas']['params']['rows']]
edges = [-3, -2, -1, 0, 1, 2]
counts = [sum(edges[i] <= x < edges[i + 1] or (i == 4 and x == 2) for x in rows) for i in range(5)]
lv.expect('l6', 'screens[0].explain.text', '1, 1, 4, 5 and 1')
lv.claim(counts == [1, 1, 4, 5, 1], f'l6 screens[0]: 1% bin counts are {counts}')
neg = [x for x in rows if x < 0]
lv.stated('l6', 'screens[0].hints[1].text', 'There are five negative returns', len(neg) == 5)
lv.stated('l6', 'screens[0].hints[1].text', 'One of them is below', sum(x < -1 for x in neg) == 1)
lv.claim_text('l6', 'screens[0].hints[1].text', 'six negative returns', len(neg) == 6)
lv.claim_text('l6', 'screens[0].hints[1].text', 'Two of them are below', sum(x < -1 for x in neg) == 2)
T4 = lambda t: 0.5 + t * (t * t + 6) / (2 * (t * t + 4) ** 1.5)      # t(4) CDF; the model is t(4) scaled to sd 1
s = math.sqrt(2)
within1 = 2 * T4(1 * s) - 1
tail3 = 2 * (1 - T4(3 * s))
Phi = lambda z: 0.5 * (1 + math.erf(z / math.sqrt(2)))
lv.expect('l6', 'screens[1].explain.text', round(100 * within1, 1), fmt='{:.1f}%')
lv.expect('l6', 'screens[1].explain.text', round(100 * (2 * Phi(1) - 1), 1), fmt='{:.1f}%')
mv = l6['screens'][4]['canvas']['state']['values']
model = [round(T4((x + 0.25) * s) - T4((x - 0.25) * s), 4) for x in [k / 2 - 3.75 for k in range(16)]]
lv.claim(all(abs(a - mv[k]) < 2e-4 for a, k in zip(model, sorted(mv, key=float))), 'l6 screens[4]: bin shares are the t(4) model scaled to sd 1')
lv.expect('l6', 'screens[4].canvas.state.caption', round(100 * tail3, 2), fmt='{:.2f}%')
lv.expect('l6', 'screens[4].canvas.state.caption', round(100 * 2 * (1 - Phi(3)), 2), fmt='{:.2f}%')
lv.claim(4.5 <= tail3 / (2 * (1 - Phi(3))) <= 5.5, 'l6 screens[4] explain: five times the normal beyond 3 sd')
lv.claim(abs(mv['0.25'] / 0.1915 - 1.25) < 0.02, 'l6 screens[4]: centre bars about a quarter above the marks')
lv.expect('l6', 'screens[3].widget.answer', round(2520 * 0.0027, 1))
lv.expect('l6', 'screens[3].widget.wrong[0].value', round(2520 * 0.0027 / 2, 1))
lv.expect('l6', 'screens[3].widget.wrong[1].value', 2520 * 0.05)
lv.expect('l6', 'screens[3].widget.wrong[2].value', round(2520 * 0.9973, 1))
lv.expect('l6', 'screens[3].explain.text', round(2520 * tail3, 1))
lv.claim(abs(120 / (2520 * 0.0027) - 18) < 0.5, 'l6 screens[3] correct: one every 18 months')
pdf = lambda x: math.exp(-x * x / (2 * 1e-4)) / (0.01 * math.sqrt(2 * math.pi))
ex = l6['screens'][5]['canvas']['params']['exact']
lv.claim(all(abs(e['y'] - round(pdf(e['x']), 1)) < 0.06 for e in ex), 'l6 screens[5]: marks are the N(0, 0.01) pdf at the bin centres')
lv.expect('l6', 'screens[5].hints[2].text', 2520 * 0.005)
dens = l6['screens'][5]['explain']['canvas']['values']
cts = l6['screens'][5]['canvas']['state']['values']
lv.claim(all(abs(dens[k] - round(cts[k] / 12.6, 1)) < 0.051 for k in cts), 'l6 screens[5] explain: density bars are count / 12.6')
lv.expect('l6', 'screens[5].explain.text', max(cts.values()))
lv.expect('l6', 'screens[7].widget.options[0].text', 40 * 0.002 * 1000)
lv.expect('l6', 'screens[7].widget.options[3].text', 40 / 0.002)
lv.expect('l6', 'quiz[0].widget.answer', 24 * 0.0025 * 1000)
lv.expect('l6', 'quiz[0].widget.wrong[1].value', 24 * 0.0025)
lv.expect('l6', 'quiz[3].widget.answer', round(1260 * 0.0027, 1))
lv.expect('l6', 'quiz[3].widget.wrong[0].value', round(1260 * 0.0027 / 2, 1))
lv.expect('l6', 'quiz[3].widget.wrong[1].value', 1260 * 0.27)
lv.check_wrongs('l6')

# ---------- l7 ----------
l7 = lv.files['l7-drawing-drawdown']
f7, pk7 = (x['values'] for x in l7['screens'][0]['canvas']['params']['series'])
run = [max(f7[:i + 1]) for i in range(len(f7))]
lv.claim(run == pk7, 'l7 screens[0]: the dashed series is the running peak')
highs = ['d%d' % (i + 1) for i in range(1, len(f7)) if f7[i] > max(f7[:i])]
lv.claim(highs == l7['screens'][0]['widget']['answer'], f'l7 screens[0]: new highs on {highs}')
dd = [p / m - 1 for p, m in zip(f7, run)]
lv.claim(min(range(12), key=lambda i: dd[i]) == 7, 'l7 screens[1]: day 8 is the deepest')
lv.expect('l7', 'screens[1].feedback.correct', round(-100 * dd[7]), fmt='{:.0f}%')
lv.expect('l7', 'screens[1].feedback.byKey.d3', round(-100 * dd[2]), fmt='{:.0f}%')
lv.expect('l7', 'screens[1].feedback.byKey.d7', round(-100 * dd[6], 1), fmt='{:.1f}%')
lv.expect('l7', 'screens[1].feedback.byKey.d9', round(-100 * dd[8], 1), fmt='{:.1f}%')
lv.expect('l7', 'screens[1].explain.text', r2(run[7] - f7[7]))
lv.expect('l7', 'screens[2].widget.answer', round(dd[7], 4))
lv.expect('l7', 'screens[2].widget.wrong[0].value', -(run[7] - f7[7]) / 100)
lv.expect('l7', 'screens[2].widget.wrong[2].value', round(-(run[7] - f7[7]) / f7[7], 4))
lv.expect('l7', 'screens[2].widget.wrong[3].value', round(f7[7] / f7[6] - 1, 4))
w = [1.0]
for r in (0.5, -0.5, 0.5, -0.5):
    w.append(w[-1] * (1 + r))
lv.expect('l7', 'screens[3].widget.answer', w[-1])
lv.expect('l7', 'screens[3].widget.wrong[1].value', 0.5 ** 4)
lv.expect('l7', 'screens[3].widget.wrong[2].value', w[2])
lv.claim(w == l7['screens'][3]['canvas']['params']['series'][0]['values'], 'l7 screens[3]: the wealth canvas recomputes')
lv.claim([round(x, 4) for x in dd] == l7['screens'][4]['canvas']['params']['series'][0]['values'], 'l7 screens[4]: drawdown canvas recomputes')
lv.expect('l7', 'screens[6].widget.options[1].why', round(100 * (1 - 1280 / 1600)), fmt='{:.0f}%')
lv.expect('l7', 'screens[6].widget.options[1].why', round(100 * (1 - 200 / 400)), fmt='{:.0f}%')
lv.expect('l7', 'screens[6].widget.options[3].text', 1600 - 1280)
rr = [0.03, -0.09, 0.12, 0.04, -0.07, -0.06, 0.02]
W = [1 + rr[0]]
for r in rr[1:]:
    W.append(W[-1] * (1 + r))
M = [max(W[:i + 1]) for i in range(len(W))]
D = [a / m - 1 for a, m in zip(W, M)]
it = min(range(7), key=lambda i: D[i])
lv.claim(it == 5 and M[it] == W[3], 'l7 screens[8]: trough on day 6 below the day 4 peak')
lv.expect('l7', 'screens[8].feedback.correct', round(100 * D[it], 1), fmt='{:.1f}%')
lv.expect('l7', 'screens[8].explain.text', round(-100 * D[1], 1), fmt='{:.1f}%')
lv.expect('l7', 'screens[8].explain.text', r2(W[3]))
lv.expect('l7', 'screens[8].explain.text', r2(W[5]))
lv.expect('l7', 'screens[8].explain.text', r2(W[1]))
lv.expect('l7', 'quiz[0].widget.answer', round(125.80 / 148.00 - 1, 4))
lv.expect('l7', 'quiz[0].widget.wrong[0].value', -(148.00 - 125.80) / 100)
lv.expect('l7', 'quiz[0].widget.wrong[1].value', round(-(148.00 - 125.80) / 125.80, 4))
lv.expect('l7', 'quiz[1].explain.text', round(1.1 * 0.9, 2))
ratio = math.log(0.7) / math.log(0.9)
lv.stated('l7', 'quiz[2].explain.text', 'looks three times the depth', abs(ratio - 3) < 0.15)
lv.claim_text('l7', 'quiz[2].explain.text', 'more than three times', ratio > 3)
lv.check_wrongs('l7')

# ---------- l8 ----------
l8 = lv.files['l8-vol-over-time']
v8 = l8['screens'][0]['canvas']['state']['values']
b8 = [v8[str(i)] for i in range(1, 41)]
lv.claim(b8 == b, 'l8 screens[0]: the same 40 returns as l5 "Calm and storm"')
lv.expect('l8', 'screens[0].widget.options[0].text', r2(st.stdev(b8[20:])), fmt='{:.2f}%')
lv.expect('l8', 'screens[0].widget.options[1].text', r2(st.stdev(b8)), fmt='{:.2f}%')
lv.expect('l8', 'screens[0].widget.options[2].text', r2(st.stdev(b8[:20])), fmt='{:.2f}%')
lv.expect('l8', 'screens[0].widget.options[3].text', r2(max(abs(x) for x in b8)), fmt='{:.2f}%')
lv.expect('l8', 'screens[2].widget.answer', round(0.012 * R252, 6))
lv.expect('l8', 'screens[2].widget.wrong[0].value', 0.012 * 252)
lv.expect('l8', 'screens[2].widget.wrong[1].value', round(0.012 * math.sqrt(12), 4))
lv.expect('l8', 'screens[2].widget.wrong[2].value', round(0.012 * math.sqrt(20), 4))
lv.expect('l8', 'screens[2].hints[1].text', r2(R252))
t2 = [0.01, -0.01] * 15
lv.claim(round(roll_sd(t2, 20)[-1] * R252, 4) == 0.1629, 'l8 screens[3] test-2: 0.1629')
t3 = [0.02, -0.02] * 10 + [0.005, -0.005] * 10
rv = [x * R252 for x in roll_sd(t3, 20) if x is not None]
lv.claim(round(rv[-1], 4) == 0.0814, 'l8 screens[3] test-3: 0.0814')
lv.expect('l8', 'screens[4].explain.text', round(st.stdev(t3) * R252, 4))
lv.expect('l8', 'screens[4].explain.text', round(st.mean(rv), 4))
lv.expect('l8', 'screens[4].feedback.byKey.test-3', round(st.mean(rv), 4))
s5 = l8['screens'][5]['canvas']['params']['series']
vv = s5[0]['values']
seg = {k: [x for x in vv[a:z + 1] if x is not None] for k, a, z in (('A', 0, 149), ('B', 150, 259), ('C', 260, 399), ('D', 400, 499))}
mean = {k: st.mean(x) for k, x in seg.items()}
lr = s5[1]['values'][0]
lv.expect('l8', 'screens[5].prose', round(100 * lr, 1), fmt='{:.1f}%')
lv.claim(max(mean, key=mean.get) == 'B' and min(mean, key=mean.get) == 'A', f'l8 screens[5]: B highest, A lowest ({ {k: round(v, 3) for k, v in mean.items()} })')
lv.claim(abs(st.median(seg['B']) - 0.27) < 0.01 and abs(mean['A'] - 0.11) < 0.01, 'l8 screens[5]: B near 27%, A near 11%')
lv.claim(mean['C'] < lr < mean['D'] < mean['B'], 'l8 screens[5]: C below the line, D above but below B')
lv.expect('l8', 'screens[5].explain.text', r2(15 / 27))
calm = [0.005 if i % 2 == 0 else -0.005 for i in range(60)]
crash = calm[:]
crash[24] = -0.06
g = [None if x is None else round(x * R252, 4) for x in roll_sd(crash, 20)]
lv.claim(g[23] == 0.0814 and g[24] == 0.2264 and g[43] == 0.2264 and g[44] == 0.0814, 'l8 screens[6]: echo in and out on days 25 and 45')
lv.claim(g == l8['screens'][6]['canvas']['params']['series'][0]['values'], 'l8 screens[6]: the canvas line recomputes')
lv.expect('l8', 'quiz[0].widget.answer', round(0.009 * R252, 6))
lv.expect('l8', 'quiz[0].widget.wrong[0].value', 0.009 * 252)
lv.expect('l8', 'quiz[0].widget.wrong[1].value', round(0.009 * math.sqrt(12), 4))
lv.expect('l8', 'quiz[1].widget.answer', 60 - 1)
lv.expect('l8', 'quiz[2].widget.options[0].text', round(100 * math.sqrt((0.1 ** 2 + 0.3 ** 2) / 2), 1), fmt='{:.1f}%')
lv.expect('l8', 'quiz[3].widget.options[0].text', 100 + 60)
lv.check_wrongs('l8')

# ---------- review-2 ----------
lv.expect('review', 'items[0].widget.answer', round(53.71 / 52.40 - 1, 4))
lv.expect('review', 'items[0].widget.wrong[1].value', round((53.71 - 52.40) / 53.71, 4))
lv.expect('review', 'items[1].widget.answer', round(118.44 / 126.00 - 1, 4))
lv.expect('review', 'items[1].widget.wrong[0].value', round(118.44 / 120.00 - 1, 4))
lv.expect('review', 'items[1].widget.wrong[1].value', -(126.00 - 118.44) / 100)
lv.expect('review', 'items[2].widget.answer', 2520 * 0.0025 * 40)
lv.expect('review', 'items[2].widget.wrong[1].value', 2520 * 40)
lv.expect('review', 'items[3].widget.answer', round(0.015 * R252, 6))
lv.expect('review', 'items[3].widget.wrong[0].value', 0.015 * 252)
lv.expect('review', 'items[3].widget.wrong[1].value', round(0.015 * math.sqrt(20), 4))
lv.expect('review', 'items[5].widget.options[0].text', 37 + 20)
lv.expect('review', 'items[6].widget.answer', round((1.1 * 0.9) ** 2, 4))
lv.expect('review', 'items[6].widget.wrong[1].value', round(0.1 * 0.1 * 0.1 * 0.1, 4))
lv.check_wrongs('review')

# ---------- homework-2 ----------
h = lv.files['homework-2']
p = [250.0, 238.0, 247.35, 252.3, 260.1, 249.7, 243.45, 251.0, 258.8, 266.4]
pk = [max(p[:i + 1]) for i in range(len(p))]
dd2 = [a / m - 1 for a, m in zip(p, pk)]
lv.expect('homework', 'items[0].feedback.correct', round(100 * min(dd2), 1), fmt='{:.1f}%')
lv.claim(dd2.index(min(dd2)) == 6, 'homework items[0]: trough on day 7')
lv.expect('homework', 'items[0].explain.text', round(-100 * (p[1] / p[0] - 1), 1), fmt='{:.1f}%')
yrs = h['items'][1]['widget']['tests'][0]['setup']
px = [float(x) for x in yrs.split('], [')[1].rstrip('])').split(', ')]
crash = 1 - px[22] / px[21]
lv.claim(round(px[-1], 1) > 2800, 'homework items[1]: rises to over £2,800')
lv.stated('homework', 'items[1].prose', 'a 38% crash', abs(crash - 0.38) < 0.005)
c4 = [380.0, 362.1, 385.0, 409.95, 426.1, 401.2, 388.05, 392.6, 405.85, 431.2, 425.0]
days4 = [dt.date(2025, 9, 1) + dt.timedelta(k) for k in range(5)] + [dt.date(2025, 9, 8) + dt.timedelta(k) for k in range(5)] + [dt.date(2025, 9, 15)]
pk4 = [max(c4[:i + 1]) for i in range(11)]
dd4 = [a / m - 1 for a, m in zip(c4, pk4)]
i4 = dd4.index(min(dd4))
lv.claim(days4[i4] == dt.date(2025, 9, 9) and days4[c4.index(426.1)] == dt.date(2025, 9, 5), 'homework items[3]: peak 5 Sep, trough 9 Sep')
lv.expect('homework', 'items[3].feedback.correct', round(-100 * min(dd4), 1), fmt='{:.1f}%')
lv.claim(c4[1] / c4[0] - 1 > min(dd4), 'homework items[3]: the 2 September low is a shallower fall')
sig = 0.015 * R252
lv.expect('homework', 'items[5].widget.answer', round(0.15 / sig * 1_000_000))
lv.expect('homework', 'items[5].widget.wrong[0].value', 0.15 / 0.015 * 1_000_000)
lv.expect('homework', 'items[5].widget.wrong[1].value', round(0.15 / (0.015 * 252) * 1_000_000))
lv.expect('homework', 'items[5].explain.text', round(sig, 4))
lv.claim(sum(c['points'] for c in h['items'][6]['widget']['rubric']) == 10, 'homework items[6]: rubric sums to 10')
lv.check_wrongs('homework')

lv.report()
