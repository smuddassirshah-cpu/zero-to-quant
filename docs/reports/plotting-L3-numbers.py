"""Number recompute for plotting level 3 (Clear and honest): l9 to l13, review-3, homework-3. Second reader, session V.

Every graded key, every numeric wrong[] value and the numbers stated in prose, hints, feedback and explanations are
recomputed from the lesson data with the standard library. Checks tied to a sentence (lv.stated) fail while a false
sentence is still in the text and pass once a fix rewords it. Code behaviour was checked in CPython with matplotlib 3.8.4,
numpy 2.0.2 and pandas 2.2.3 (the Pyodide 0.27.7 versions); the behaviour facts used below are constants from that run:
  - set_yscale("log") defaults to nonpositive="clip": a zero or negative point is drawn off the bottom edge, not masked;
    a series with no positive value raises UserWarning "Data has no positive values, and therefore cannot be log-scaled."
  - plt.subplots(2, 2, sharex="col") with imshow(3 x 12) above a 250-day line gives the heat map's column x limits
    (-0.5, 261.5): the heat map collapses to a sliver.
Run from anywhere:  python3 docs/reports/plotting-L3-numbers.py
Failing checks on the current content are findings in docs/reviews/review-plotting-1-3.md.
"""
import sys, os, re, math, statistics as st, datetime as dt
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("plotting", 3)
r2 = lambda x: round(x, 2)
R252 = math.sqrt(252)
LOG_CLIPS = True            # matplotlib 3.8.4: LogTransform(nonpositive="clip") is the default
NO_POSITIVE_WARNS = True    # UserWarning when every value is <= 0
SHAREX_COL_SPLITS_HEATMAP = True
LOG_TICKS = ['$\\mathdefault{10^{2}}$', '$\\mathdefault{10^{3}}$']   # set_yscale('log') on £100 to £1,640: the only labelled ticks
NPLOG_TICKS = [4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5]                   # plot(np.log(closes)): the default ticks


def rets(p):
    return [b / a - 1 for a, b in zip(p, p[1:])]


def corr(x, y):
    mx, my = st.mean(x), st.mean(y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    return sxy / math.sqrt(sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y))


# ---------- l9 ----------
l9 = lv.files['l9-log-axis']
p9 = l9['screens'][0]['canvas']['params']
v9, d9 = p9['series'][0]['values'], p9['dates']
yr = [int(x[:4]) for x in d9]
for peak_y, trough_y, pct in ((2000, 2002, 50), (2007, 2008, 35), (2019, 2020, 20)):
    a, z = v9[yr.index(peak_y)], v9[yr.index(trough_y)]
    lv.claim(round(100 * (1 - z / a)) == pct, f'l9 screens[0]: {peak_y} to {trough_y} falls {pct}%')
    lv.expect('l9', 'screens[0].explain.text', pct)
lv.expect('l9', 'screens[0].feedback.byKey.t08', 900.0 - 585.0)
lv.expect('l9', 'screens[2].widget.answer', 2 * math.log2(800 / 200))
lv.expect('l9', 'screens[2].widget.wrong[0].value', 2 * (800 - 200) / 100)
lv.expect('l9', 'screens[2].widget.wrong[1].value', 2 * 800 / 200)
lv.claim(round(math.log(100), 1) == 4.6 and round(math.log(1640), 1) == 7.4, 'l9 screens[3]: the logs of the data run 4.6 to 7.4')
lv.claim_text('l9', 'screens[3].widget.options[1].why', 'reads 4.5 to 7.5', NPLOG_TICKS[0] == 4.5 and NPLOG_TICKS[-1] == 7.5)
lv.stated('l9', 'screens[3].widget.options[1].why', 'the ticks read 4.6 and 7.4', 4.6 in NPLOG_TICKS and 7.4 in NPLOG_TICKS)
lv.stated('l9', 'screens[3].explain.text', 'tick labels still read in pounds', all('£' in t for t in LOG_TICKS))
lv.stated('l9', 'summary.ideas[1]', 'keeps the tick labels in pounds', all('£' in t for t in LOG_TICKS))
lv.expect('l9', 'screens[4].widget.answer', sum(x > 0 for x in [0.00, 120.50, -80.25, 310.00, 450.75]))
lv.stated('l9', 'screens[4].explain.text', 'the line simply breaks', not LOG_CLIPS)
lv.stated('l9', 'quiz[2].widget.options[1].why', 'It masks values', not LOG_CLIPS)
lv.stated('l9', 'quiz[2].explain.text', 'masks the', not LOG_CLIPS)
lv.expect('l9', 'screens[6].explain.text', 'eight times')
lv.claim((1600 - 800) / (200 - 100) == 8, 'l9 screens[6]: B made eight times what A made')
lv.expect('l9', 'quiz[0].widget.answer', 1.5 * math.log2(160 / 40))
lv.expect('l9', 'quiz[0].widget.wrong[0].value', 1.5 * (160 - 40) / 20)
lv.expect('l9', 'quiz[0].widget.wrong[1].value', 1.5 * 160 / 40)
lv.expect('l9', 'quiz[1].widget.options[0].text', 400 * 50 / 40)
lv.claim(450 / 400 - 1 == 0.125, 'l9 quiz[1] plus100 why: £450 is 12.5%')
lv.check_wrongs('l9')

# ---------- l10 ----------
l10 = lv.files['l10-panels']
eq = l10['screens'][0]['canvas']['left']['params']['series'][0]['values']
pk = [max(eq[:i + 1]) for i in range(len(eq))]
dd = [a / m - 1 for a, m in zip(eq, pk)]
it = dd.index(min(dd))
lv.claim(it == 33 and pk[it] == eq[18], 'l10 screens[0]: deepest drawdown on day 33, from the day 18 peak')
lv.expect('l10', 'screens[0].widget.answer', eq[it])
lv.expect('l10', 'screens[0].widget.wrong[0].value', eq[18])
lv.expect('l10', 'screens[0].feedback.correct', round(100 * dd[it], 1), fmt='{:.1f}%')
dcan = l10['screens'][0]['canvas']['right']['params']['series'][0]['values']
lv.claim(all(abs(a - b) < 2e-6 for a, b in zip(dd, dcan)), 'l10 screens[0]: drawdown panel recomputes')
lv.expect('l10', 'screens[2].widget.options[1].text', -0.05 * 59)
lv.expect('l10', 'screens[2].widget.options[1].text', 59 + 0.05 * 59)
c3 = [100.0, 104.0, 101.4, 97.0, 99.0, 106.0]
lv.expect('l10', 'screens[3].explain.text', round(c3[3] / c3[1] - 1, 4))
lv.claim(round(c3[1] / c3[0] - 1, 4) == 0.04, 'l10 screens[3] explain: the day 1 return is 4%')
lv.expect('l10', 'screens[5].widget.answer', 8 * 150)
lv.expect('l10', 'screens[5].widget.wrong[0].value', 8 * 100)
lv.expect('l10', 'screens[5].widget.wrong[1].value', 4.5 * 150)
a6, b6 = (l10['screens'][6]['canvas'][k]['params']['series'][0]['values'] for k in ('left', 'right'))
lv.expect('l10', 'screens[6].widget.options[0].text', round(100 * (b6[-1] / b6[0] - 1)), fmt='{:.0f}%')
lv.expect('l10', 'screens[6].widget.options[0].text', round(100 * (a6[-1] / a6[0] - 1)), fmt='{:.0f}%')
lv.claim(all(abs((b6[i] - 100) - 15 * (a6[i] - 100)) < 1e-6 for i in range(len(a6))), 'l10 screens[6]: the two lines have the same shape')
lv.stated('l10', 'screens[7].explain.text', 'ties each column', not SHAREX_COL_SPLITS_HEATMAP)
e8 = [10000.0, 10250.0, 10120.0, 9840.0, 10010.0, 10400.0, 10330.0, 10710.0]
dd8 = [a / max(e8[:i + 1]) - 1 for i, a in enumerate(e8)]
lv.expect('l10', 'screens[8].explain.text', round(min(dd8), 4))
lv.expect('l10', 'quiz[1].widget.answer', 4 * 200)
lv.expect('l10', 'quiz[1].widget.wrong[0].value', 6 * 200)
lv.expect('l10', 'quiz[3].widget.wrong[1].value', 5 * 12)
lv.check_wrongs('l10')

# ---------- l11 ----------
l11 = lv.files['l11-two-variables']
pts = l11['screens'][0]['canvas']['params']['points']
sxy, sxx = sum(x * y for x, y in pts), sum(x * x for x, y in pts)
lv.expect('l11', 'screens[1].explain.text', round(sxy, 2))
lv.expect('l11', 'screens[1].explain.text', round(sxx, 2))
lv.expect('l11', 'screens[1].explain.text', r2(sxy / sxx))
lv.claim(min(pts, key=lambda p: p[0]) == pts[0] and min(pts, key=lambda p: p[1]) == pts[1], 'l11 screens[0]: p0 is the market low, p1 the ACME low')
lv.expect('l11', 'screens[2].widget.answer', 1.3 * -0.02)
lv.expect('l11', 'screens[2].widget.wrong[2].value', round(-0.02 / 1.3, 4))
pr = l11['screens'][3]['canvas']['left']['params']['points']
ra, rb = rets([p[0] for p in pr]), rets([p[1] for p in pr])
lv.claim([[r2(100 * a), r2(100 * b)] for a, b in zip(ra, rb)] == l11['screens'][3]['canvas']['right']['params']['points'], 'l11 screens[3]: the returns plot comes from the price plot')
# price correlation is 0.9445: the text's 0.95 should read 0.94 (finding)
lv.stated('l11', 'screens[3].explain.text', 'correlation is 0.95', r2(corr([p[0] for p in pr], [p[1] for p in pr])) == 0.95)
lv.expect('l11', 'screens[3].explain.text', r2(corr(ra, rb)))
# screens[6]: BETA's real closes are the rebased line on screens[8] times £48.00 / 100
beta = [48.0 * x / 100 for x in l11['screens'][8]['canvas']['params']['series'][1]['values']]
lv.claim(abs(beta[0] - 48.0) < 1e-9 and abs(beta[-1] - 52.8) < 1e-9, 'l11: BETA runs £48.00 to £52.80')
for side, cap in (('left', '£44 to £52'), ('right', '£47 to £53')):
    drawn = l11['screens'][6]['canvas'][side]['params']['series'][1]['values']
    slope = (drawn[-1] - drawn[0]) / (beta[-1] - beta[0])            # panel units per £ on BETA's right axis
    lo = beta[0] - (drawn[0] - 95) / slope
    hi = lo + 50 / slope                                              # the left axis runs 95 to 145
    lv.claim(all(abs(d - (95 + (b - lo) * slope)) < 0.06 for d, b in zip(drawn, beta)), f'l11 screens[6] {side}: drawn BETA is a linear map of the closes')
    a_, b_ = [float(x) for x in cap.replace('£', '').split(' to ')]
    lv.stated('l11', f'screens[6].canvas.{side}.state.caption', cap, abs(lo - a_) < 0.05 and abs(hi - b_) < 0.05)
    print(f'     ({side} panel: BETA axis implied £{lo:.2f} to £{hi:.2f})')
acme = l11['screens'][6]['canvas']['left']['params']['series'][0]['values']
top_b = l11['screens'][6]['canvas']['left']['params']['series'][1]['values']
bot_b = l11['screens'][6]['canvas']['right']['params']['series'][1]['values']
first_above = lambda bb: next(i + 1 for i in range(len(acme)) if bb[i] > acme[i] and all(bb[j] > acme[j] for j in range(i, len(acme))))
lv.claim(first_above(top_b) == 2 and first_above(bot_b) == 8, 'l11 screens[6]: crossings in month 2 (top) and month 8 (bottom)')
lv.expect('l11', 'screens[7].widget.answer', 100 * 52.80 / 48.00)
lv.expect('l11', 'screens[7].widget.wrong[0].value', 100 + 52.80 - 48.00)
lv.expect('l11', 'screens[7].explain.text', r2(100 * acme[-1] / acme[0]))
lv.expect('l11', 'screens[7].explain.text', round(100 * (acme[-1] / acme[0] - 1), 1), fmt='{:.1f}%')
lv.expect('l11', 'screens[8].explain.text', round(100 * (123 / 120 - 1), 1), fmt='+{:.1f}%')
a_, b_ = [float(x.replace(',', '')) for x in re.findall(r'£([\d,]+\.\d\d)', lv.text('l11', 'quiz[1].prose'))]   # read from the prose (a fix may change them)
lv.expect('l11', 'quiz[1].widget.answer', round(100 * b_ / a_, 4))
lv.expect('l11', 'quiz[1].widget.wrong[0].value', round(100 - (a_ - b_), 4))
lv.expect('l11', 'quiz[1].widget.wrong[1].value', round(b_ / a_, 4))
lv.expect('l11', 'quiz[1].explain.text', round(100 * b_ / a_, 4))
lv.check_wrongs('l11')

# ---------- l12 ----------
l12 = lv.files['l12-charts-that-mislead']
nav = l12['screens'][0]['canvas']['params']['series'][0]['values']
win = [round(100 * (nav[k + 12] / nav[k] - 1), 2) for k in range(24)]
cap = l12['screens'][0]['canvas']['derive']['caption']
lst = [float(x) for x in cap.split('{{fixed([')[1].split('][k]')[0].split(', ')]
lv.claim(win == lst, 'l12 screens[0]: the caption list is every 12-month return')
best = max(range(24), key=lambda k: win[k])
lv.claim(best == 14, 'l12 screens[0]: best window starts in month 14')
lv.expect('l12', 'screens[0].widget.answer', round(nav[26] / nav[14] - 1, 4))
lv.expect('l12', 'screens[0].widget.wrong[0].value', round(nav[12] / nav[0] - 1, 3))
lv.expect('l12', 'screens[1].widget.answer', round(nav[-1] / nav[0] - 1, 4))
lv.expect('l12', 'screens[1].explain.text', round(100 * (1 - min(nav) / nav[0])), fmt='{:.0f}%')
tall = l12['screens'][2]['canvas']['left']['params']['series'][0]['values']
lv.expect('l12', 'screens[2].prose', round(100 * (tall[-1] / tall[0] - 1)), fmt='{:.0f}%')
lv.claim(abs((98.00 - 95) / (96.04 - 95) - 3) < 0.2, 'l12 screens[4]: Friday bar is about a third of Monday\'s')
app = (96.04 - 95) / (98.00 - 95) - 1
lv.expect('l12', 'screens[5].widget.options[0].text', round(100 * app))
lv.expect('l12', 'screens[5].hints[2].text', round(app, 3))
lv.claim(app / (96.04 / 98.00 - 1) > 30, 'l12 screens[5] explain: exaggerated more than thirtyfold')
lv.expect('l12', 'quiz[0].widget.answer', (57 - 50) / (60 - 50) - 1)
lv.expect('l12', 'quiz[0].widget.wrong[0].value', 57 / 60 - 1)
lv.claim(abs(((57 - 50) / (60 - 50) - 1) / (57 / 60 - 1) - 6) < 1e-9, 'l12 quiz[0]: six times smaller')
years_since = (dt.date(2026, 11, 7) - dt.date(2020, 3, 23)).days / 365.25
lv.stated('l12', 'quiz[1].widget.options[1].text', 'Four years', abs(years_since - 4) < 0.5)
lv.claim(41 - 23 == 18, 'l12 quiz[3]: 18 days from day 23 to day 41')
lv.check_wrongs('l12')

# ---------- l13 ----------
c = [50.0, 52.0, 51.0, 54.0, 49.5, 48.6, 50.4, 53.1]


def mdd(p):
    return min(a / max(p[:i + 1]) - 1 for i, a in enumerate(p))


lv.expect('l13', 'screens[0].feedback.correct', round(-100 * mdd(c)), fmt='{:.0f}%')
lv.expect('l13', 'screens[3].widget.answer', round(0.012 * R252, 4))
lv.expect('l13', 'screens[3].widget.wrong[0].value', 0.012 * 252)
lv.expect('l13', 'screens[3].widget.wrong[1].value', round(0.012 * math.sqrt(12), 4))
for test, closes in ((0, c), (1, [40.0, 44.0, 52.0, 60.0, 57.0, 54.0, 58.0]), (2, [100.0, 101.0, 102.5, 103.0])):
    got = [round(st.stdev(rets(closes)) * R252, 4), round(mdd(closes), 4)]
    want = lv.files['l13-exit-project']['screens'][4]['widget']['tests'][test]['expect']
    lv.claim(str(got).replace('-0.0]', '0.0]') == want, f'l13 screens[4] test-{test + 1}: {got}')
s5 = [40.0, 44.0, 52.0, 60.0, 57.0, 54.0, 58.0]
lv.expect('l13', 'screens[5].widget.options[0].text', round(100 * mdd(s5), 2))
lv.expect('l13', 'screens[5].widget.options[1].text', -r2(100 * (60 - 40) / 60))
lv.expect('l13', 'screens[5].widget.options[2].text', -r2(100 * (60 - 40) / 40))
lv.expect('l13', 'screens[5].widget.options[3].text', -r2(100 * (1 - 54 / 57)))
lv.expect('l13', 'screens[6].explain.text', round(100 * (1 - 58 / 60), 1), fmt='{:.1f}%')
lv.expect('l13', 'quiz[0].widget.answer', round(0.008 * R252, 3))
lv.expect('l13', 'quiz[0].widget.wrong[0].value', 0.008 * 252)
q = [80.0, 100.0, 90.0, 120.0, 96.0, 110.0]
lv.expect('l13', 'quiz[1].widget.answer', mdd(q))
lv.expect('l13', 'quiz[1].widget.wrong[0].value', round((80 - 120) / 120, 4))
lv.expect('l13', 'quiz[1].widget.wrong[1].value', 90 / 100 - 1)
lv.check_wrongs('l13')

# ---------- review-3 ----------
lv.expect('review', 'items[0].widget.answer', math.log2(800 / 100))
lv.expect('review', 'items[0].widget.wrong[0].value', (800 - 100) / 50)
lv.stated('review', 'items[1].explain.text', 'masks them', not LOG_CLIPS)
lv.expect('review', 'items[3].widget.answer', 6 * 150)
lv.expect('review', 'items[3].widget.wrong[0].value', 10 * 150)
lv.expect('review', 'items[5].widget.answer', 100 * 72 / 64)
lv.expect('review', 'items[6].widget.answer', (96 - 90) / (100 - 90) - 1)
lv.expect('review', 'items[7].explain.text', round(0.8 * 1.3, 2))
q3 = [30.0, 45.0, 36.0, 50.0, 42.5, 55.0]
lv.expect('review', 'items[8].widget.answer', mdd(q3))
lv.expect('review', 'items[8].widget.wrong[0].value', round((30 - 55) / 55, 4))
lv.expect('review', 'items[8].widget.wrong[1].value', 42.5 / 50 - 1)
sd9 = float(re.search(r'(\d+\.\d+)%', lv.text('review', 'items[9].prose')).group(1)) / 100    # read from the prose
lv.expect('review', 'items[9].widget.answer', round(sd9 * R252, 4))
lv.expect('review', 'items[9].widget.wrong[0].value', round(sd9 * 252, 4))
lv.claim(abs(lv.files['review-3']['items'][9]['widget']['wrong'][1]['value'] - sd9 * math.sqrt(12)) < 5e-4, 'review items[9]: the months slip is sd x sqrt(12)')
lv.expect('review', 'items[9].feedback.correct', round(sd9 * 100 * R252, 2), fmt='{:.2f}%')
lv.check_wrongs('review')

# ---------- homework-3 ----------
lv.expect('homework', 'items[0].widget.answer', r2(1.2 * math.log2(10)))
lv.expect('homework', 'items[0].widget.accept', round(math.log2(10), 4))
lv.expect('homework', 'items[2].widget.answer', 1280 / 6.4)
lv.expect('homework', 'items[2].widget.wrong[0].value', 1280 / 4)
lv.expect('homework', 'items[2].widget.wrong[1].value', 1280 * 6.4)
lv.expect('homework', 'items[3].widget.answer', ((190 - 180) / (200 - 180) - 1) / (190 / 200 - 1))
eqh = [10000.0, 10092.26, 10313.74, 10253.64, 10444.14, 10817.88, 11037.91, 11643.47, 11427.46, 11541.98, 11390.13, 11213.5, 11241.36, 11405.92, 11640.53, 11911.1, 12804.57, 13238.35, 12710.99, 12890.61, 12752.8, 12657.51, 13254.78, 13272.17, 12601.42]
rh = rets(eqh)
sh = st.mean(rh[18:24]) / st.stdev(rh[18:24]) * math.sqrt(12)
lv.expect('homework', 'items[5].explain.text', round(sh, 4))
lv.expect('homework', 'items[5].explain.text', round(100 * mdd(eqh), 1), fmt='{:.1f}%')
lv.claim(eqh.index(max(eqh)) == 23 and mdd(eqh) == eqh[-1] / eqh[23] - 1, 'homework items[5]: the worst fall is the last month from £13,272.17')
m6 = [0.01, -0.005, 0.02, 0.005, 0.015, -0.01]
lv.expect('homework', 'items[7].prose', round(100 * st.mean(m6), 4))
lv.expect('homework', 'items[7].prose', round(100 * st.stdev(m6), 4))
lv.expect('homework', 'items[7].widget.answer', r2(st.mean(m6) / st.stdev(m6) * math.sqrt(12)))
lv.expect('homework', 'items[7].widget.wrong[0].value', round(st.mean(m6) / st.stdev(m6), 1))
lv.expect('homework', 'items[7].widget.wrong[1].value', r2(st.mean(m6) / st.stdev(m6) * 12))
m8 = re.search(r'\(£([\d.]+)\) and 31 December \(£([\d.]+)\)\. Its y axis runs from £(\d+)', lv.text('homework', 'items[8].prompt'))
hi8, lo8, base8 = (float(x) for x in m8.groups())                                     # read from the prompt
app8, real8 = (lo8 - base8) / (hi8 - base8) - 1, lo8 / hi8 - 1
lv.expect('homework', 'items[8].model', round(100 * app8))
lv.expect('homework', 'items[8].model', round(100 * real8))
lv.expect('homework', 'items[8].model', '{:.2f} and {:.2f}'.format(hi8 - base8, lo8 - base8))
lv.expect('homework', 'items[8].rubric[0].text', round(100 * app8))
lv.expect('homework', 'items[8].model', round(app8 / real8), fmt='about {} times')
lv.expect('homework', 'items[1].explain.text', hi8)
lv.expect('homework', 'items[1].explain.text', lo8)
lv.stated('homework', 'items[8].model', 'drops every value silently', not NO_POSITIVE_WARNS)
lv.stated('homework', 'items[8].rubric[3].text', 'drops them silently', not NO_POSITIVE_WARNS)
lv.claim(sum(r['points'] for r in lv.files['homework-3']['items'][8]['rubric']) == 10, 'homework items[8]: rubric sums to 10')
lv.claim((8 / 4) / (4 / 12) == 6, 'homework items[9] explain: six times steeper')
lv.check_wrongs('homework')

lv.report()
