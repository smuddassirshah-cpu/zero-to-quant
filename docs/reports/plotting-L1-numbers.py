"""Number recompute for plotting level 1 (First charts): l1 to l4, review-1, homework-1. Second reader, session V.

Every graded key, every numeric wrong[] value and the numbers stated in prose, hints, feedback and explanations are
recomputed here from the lesson data (pure standard library; histograms rebuilt with numpy's bin rule by hand).
Checks tied to a sentence (lv.stated) fail while a false sentence is still in the text and pass once a fix rewords it.
matplotlib behaviour (current axes, AttributeError text, legend entries, category ticks, DateFormatter, autofmt_xdate)
was checked separately in CPython with matplotlib 3.8.4, numpy 2.0.2 and pandas 2.2.3 (the Pyodide 0.27.7 versions).
Run from anywhere:  python3 docs/reports/plotting-L1-numbers.py
Failing checks on the current content are findings in docs/reviews/review-plotting-1-3.md.
"""
import sys, os, math, datetime as dt
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("plotting", 1)
r2 = lambda x: round(x, 2)


def hist(values, bins):
    """numpy.histogram with an integer bin count: equal bins from min to max, the last bin closed."""
    lo, hi = min(values), max(values)
    w = (hi - lo) / bins
    counts = [0] * bins
    for v in values:
        i = min(int((v - lo) / w), bins - 1)
        counts[i] += 1
    return counts, lo, w


def rets(p):
    return [b / a - 1 for a, b in zip(p, p[1:])]


# ---------- l1 ----------
l1 = lv.files['l1-figure-and-axes']
closes = l1['screens'][0]['canvas']['params']['series'][0]['values']
top = max(closes)
lv.claim(closes.index(top) == 8 and l1['screens'][0]['widget']['answer'] == ['m8'], 'l1 screens[0]: the highest close is day 9 (marker m8)')
lv.expect('l1', 'screens[0].hints[2].text', top)
lv.expect('l1', 'screens[0].feedback.byKey.m9', closes[9])
lv.expect('l1', 'screens[0].feedback.byKey.m5', closes[5])
lv.expect('l1', 'screens[0].feedback.byKey.m7', closes[7])
lv.claim(closes[5] == max(closes[:6]), 'l1 byKey.m5: day 6 was a high at the time')
lv.claim(closes[2] < min(closes[:2]), 'l1 screens[1] avg why: day 3 sits below both earlier closes')
lv.expect('l1', 'screens[1].widget.options[3].why', closes[2])
lv.expect('l1', 'screens[5].widget.answer', 2)       # two ax.plot calls
lv.expect('l1', 'quiz[1].widget.answer', 2)
lv.check_wrongs('l1')

# ---------- l2 ----------
lv.expect('l2', 'screens[3].widget.options[1].text', 1000 * 404.10 / 100)    # pence: £4,041
lv.expect('l2', 'screens[3].widget.options[0].text', 1000 * 404.10)          # pounds: £404,100
lv.expect('l2', 'screens[3].hints[2].text', 404.10 / 100)
lv.expect('l2', 'screens[3].explain.text', 4041)
lv.expect('l2', 'screens[4].widget.answer', 1)       # one labelled line
lv.expect('l2', 'screens[5].widget.options[0].text', "£{:,.2f}".format(1250))
lv.expect('l2', 'quiz[2].widget.options[0].text', "£{:,.2f}".format(18.5))
lv.check_wrongs('l2')

# ---------- l3 ----------
l3 = lv.files['l3-price-chart']
p3 = l3['screens'][0]['canvas']['params']
v3, d3 = p3['series'][0]['values'], p3['dates']
falls = sorted(((v3[i - 1] - v3[i], i) for i in range(1, len(v3))), reverse=True)
big, ib = falls[0]
lv.claim(ib == 16 and d3[ib] == '2024-03-25' and l3['screens'][0]['widget']['answer'] == ['d16'], 'l3 screens[0]: the largest fall ends on 25 March (d16)')
lv.expect('l3', 'screens[0].feedback.correct', r2(big))
lv.expect('l3', 'screens[0].explain.text', r2(100 * big / v3[15]), fmt='{:.1f}%')
lv.expect('l3', 'screens[0].feedback.byKey.d2', r2(v3[1] - v3[2]))
lv.expect('l3', 'screens[0].feedback.byKey.d6', r2(v3[5] - v3[6]))
lv.expect('l3', 'screens[0].feedback.byKey.d14', max(v3))
lv.claim(v3.index(max(v3)) == 14 and ib - 14 == 2, 'l3 byKey.d14: the month high is 21 March, two trading days before the fall')
# hint 1: "the last full week of the month". The data end Thursday 28 March (29 March 2024 was Good Friday), so the
# week of 25 March holds four trading days; the last full week is 18 to 22 March, and the drop lands on 25 March.
week = [x for x in d3 if dt.date.fromisoformat(x).isocalendar()[1] == dt.date(2024, 3, 25).isocalendar()[1]]
lv.stated('l3', 'screens[0].hints[1].text', 'last full week', len(week) == 5)
lv.expect('l3', 'screens[5].widget.answer', len(v3) - 1)
r3 = rets(v3)
cnt, lo, w = hist(r3, 20)
lv.claim(cnt == [l3['screens'][6]['canvas']['state']['values'][f'b{i}'] for i in range(20)], 'l3 screens[6]: canvas bars equal numpy histogram of the 19 March returns')
lv.expect('l3', 'screens[6].canvas.state.caption', cnt.count(0))
lv.expect('l3', 'screens[6].explain.text', cnt.count(0))
lv.claim(sum(cnt) == 19, 'l3 screens[6] explain: heights add to 19')
b4 = l3['screens'][4]['canvas']['state']['values']
b4 = [b4[f'b{i}'] for i in range(16)]
lv.claim(sum(b4) == 100, 'l3 screens[4]: 100 days in the histogram')
lv.expect('l3', 'screens[4].explain.text', sum(b4[:8]))
lv.expect('l3', 'screens[4].explain.text', sum(b4[8:]))
lv.claim(b4[1] == 0 and b4[14] == 0, 'l3 screens[4] explain: at 0.5% empty bins sit in the tails')
lv.expect('l3', 'screens[8].feedback.byKey.test-3', min(rets([100.0, 102.0, 100.98, 103.0])))
lv.claim(abs(round(max(rets([412.30, 415.10, 409.80, 411.25])), 6) - 0.006791) < 1e-12, 'l3 screens[8] test-4 expects 0.006791, the largest return')
lv.expect('l3', 'quiz[1].widget.answer', 253 - 1)
lv.expect('l3', 'screens[3].widget.options[0].text', dt.date(2024, 3, 8).strftime('%d %b'))
lv.expect('l3', 'quiz[3].widget.options[0].text', dt.date(2024, 1, 15).strftime('%b %Y'))
lv.check_wrongs('l3')

# ---------- l4 ----------
l4 = lv.files['l4-rebasing']
hb, kr = (s['values'] for s in l4['screens'][0]['canvas']['params']['series'])
g_h, g_k = hb[-1] / hb[0] - 1, kr[-1] / kr[0] - 1
lv.expect('l4', 'screens[0].hints[2].text', round(100 * g_k, 1), fmt='{:.1f}%')
lv.expect('l4', 'screens[0].hints[2].text', round(100 * g_h, 1), fmt='{:.1f}%')
lv.expect('l4', 'screens[0].widget.options[0].why', r2(hb[-1] - hb[0]))
lv.expect('l4', 'screens[0].explain.text', r2(kr[-1] - kr[0]))
lv.claim(3.5 <= g_k / g_h <= 4.5, f'l4 screens[0] explain: "four times" ({g_k / g_h:.2f})')
reb = [[r2(p / s[0] * 100) for p in s] for s in (hb, kr)]
lv.claim(reb == [s['values'] for s in l4['screens'][1]['canvas']['params']['series']], 'l4 screens[1]: rebased canvas values recompute')
lv.expect('l4', 'screens[1].question', round(kr[8] / kr[0] * 100, 1))
lv.expect('l4', 'screens[1].widget.options[2].why', round(kr[7] / kr[0] * 100, 1))
lv.expect('l4', 'screens[1].widget.options[2].why', round(100 * (kr[8] / kr[7] - 1), 1), fmt='{:.1f}%')
lv.expect('l4', 'screens[1].explain.text', round(hb[8] / hb[0] * 100, 1))
lv.expect('l4', 'screens[1].widget.options[1].why', kr[8])
lv.expect('l4', 'screens[2].widget.answer', round(kr[5] / kr[0] * 100, 6))
lv.expect('l4', 'screens[2].widget.wrong[0].value', r2(kr[0] / kr[5] * 100))
lv.expect('l4', 'screens[2].widget.wrong[1].value', r2(kr[5] - kr[0]))
lv.expect('l4', 'screens[2].widget.wrong[2].value', round(kr[5] / kr[0], 2))
lv.expect('l4', 'screens[4].prose', round(reb[1][-1], 1))
lv.expect('l4', 'screens[4].prose', round(reb[0][-1], 1))
reb6 = [[r2(p / s[5] * 100) for p in s] for s in (hb, kr)]
lv.claim(reb6 == [s['values'] for s in l4['screens'][5]['canvas']['params']['series']], 'l4 screens[5]: canvas rebased to day 6 recomputes')
lv.expect('l4', 'screens[5].widget.answer', r2(hb[-1] / hb[5] * 100))
lv.expect('l4', 'screens[5].widget.wrong[1].value', r2(hb[0] / hb[5] * 100))
lv.expect('l4', 'screens[5].widget.wrong[0].value', round(hb[-1] / hb[0] * 100, 1))
lv.expect('l4', 'screens[5].explain.text', r2(100 * (1 - hb[-1] / hb[5])), fmt='{:.2f}%')
lv.expect('l4', 'screens[5].explain.text', r2(100 * (kr[-1] / kr[5] - 1)), fmt='{:.2f}%')
pts = [[r2(100 * a), r2(100 * b)] for a, b in zip(rets(hb), rets(kr))]
lv.claim(pts == l4['screens'][6]['canvas']['params']['points'], 'l4 screens[6]: scatter points are the daily returns in %')
both = ['p%d' % i for i, (x, y) in enumerate(pts) if x < 0 and y < 0]
lv.claim(both == l4['screens'][6]['widget']['answer'], f'l4 screens[6]: days both fell are {both}')
lv.expect('l4', 'screens[6].feedback.byKey.p11', abs(pts[11][0]))
lv.expect('l4', 'screens[6].feedback.byKey.p11', pts[11][1])
above = sum(y > x for x, y in pts)
lv.expect('l4', 'screens[7].widget.answer', above)
lv.expect('l4', 'screens[7].widget.wrong[0].value', len(pts) - above)
lv.claim(all(x < 0 and y < 0 for x, y in pts if y < x), 'l4 screens[7] explain: every day below the line is a fall')
lv.expect('l4', 'quiz[0].widget.answer', 230 / 250 * 100)
lv.expect('l4', 'quiz[0].widget.wrong[0].value', round(250 / 230 * 100, 1))
lv.check_wrongs('l4')

# ---------- review-1 ----------
lv.expect('review', 'items[2].widget.options[0].text', 25 * 1000)
lv.expect('review', 'items[3].widget.answer', (dt.date(2024, 3, 25) - dt.date(2024, 3, 22)).days)
lv.expect('review', 'items[4].widget.options[0].text', 61 - 1)
lv.expect('review', 'items[5].widget.answer', 1932 / 1840 * 100)
lv.expect('review', 'items[5].widget.wrong[0].value', r2(1840 / 1932 * 100))
lv.expect('review', 'items[5].widget.wrong[1].value', 1932 - 1840)
lv.claim(-2.4 < -1.5, 'review items[6]: (-1.5, -2.4) lies below y = x')
lv.check_wrongs('review')

# ---------- homework-1 ----------
hr = [100 * x for x in rets([412.30, 415.10, 409.80, 411.25, 418.60])]
lv.expect('homework', 'items[1].feedback.byKey.test-3', round(min(hr), 6))
lv.expect('homework', 'items[1].explain.text', r2(min(hr)), fmt='{:.2f}%')
ra, rb = rets([100.0, 101.5, 99.47, 100.46]), rets([40.0, 40.8, 39.58, 39.98])
lv.expect('homework', 'items[2].feedback.byKey.test-3', round(min(ra + rb), 6))
lv.expect('homework', 'items[2].feedback.byKey.test-3', round(max(ra + rb), 6))
lv.expect('homework', 'items[5].widget.answer', 90 / 100 * 100)
lv.expect('homework', 'items[5].widget.wrong[0].value', 90 / 80 * 100)
lv.expect('homework', 'items[5].feedback.byKey.day1', round(100 * (90 / 80 - 1), 1), fmt='{:.1f}%')
lv.claim(sum(c['points'] for c in lv.files['homework-1']['items'][6]['widget']['rubric']) == 10, 'homework items[6]: rubric sums to 10')
lv.claim(dt.date(2024, 1, 2).weekday() == 1, 'homework items[6] model: 2 Jan 2024, the first day of the data, is a Tuesday')
# items[7] explain: "Sixty bins for 30 returns leaves at most one day per bar" is not forced. 30 returns can share a bar:
cnt60, _, _ = hist([0.0, 0.0001] + [0.001 * k for k in range(1, 29)], 60)
lv.stated('homework', 'items[7].explain.text', 'leaves at most one day per bar', max(cnt60) <= 1)
lv.check_wrongs('homework')

lv.report()
