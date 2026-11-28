"""llm-apps level 2 (Language models in quant research): every stated number recomputed by a second route.

Route A is the content builder (NumPy vectorised P&L, pandas merge_asof, numpy statistics). Route B here: the seeded market is
regenerated from llm_apps_ops_l2.make_market, the as-of feature is rebuilt with bisect on publication strings (no pandas),
Sharpe ratios and standard errors come from the statistics module in plain loops, dates from datetime; every code widget's hidden
tests are rerun in CPython with its solution and an independent twin, and every mutant must fail its named test first. Strict coverage.
"""
import bisect, datetime as dt, json, math, os, re, statistics, sys
HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, '..', '..', 'app')
DATA = os.path.join(APP, 'content', 'data', 'ai')
sys.path.insert(0, os.path.join(APP, 'tools'))
sys.path.insert(0, DATA)
import numpy as np
from numbers_lib import Level, ZQ_LIB
import llm_apps_ops_l2 as o2

lv = Level("llm-apps", 2, coverage="strict")
F = lv.files


def close(a, b, t=1e-9):
    return abs(a - b) <= t


def sharpe(xs):
    return statistics.fmean(xs) / statistics.stdev(xs) * math.sqrt(252)


def asof_b(docs, dates, close_t='16:30'):
    ds = sorted(docs, key=lambda d: d['published'])
    ts = [d['published'] for d in ds]
    out = []
    for d in dates:
        i = bisect.bisect_right(ts, d + ' ' + close_t)
        out.append(ds[i - 1]['score'] if i else None)
    return out


def sgn(x):
    return 0 if x is None or x == 0 else (1 if x > 0 else -1)


# ------------------------------------------------------------------ the seeded market, by loops
M = o2.make_market()
dates, ret, docs = M['dates'], [float(x) for x in M['ret']], M['docs']
lv.claim(M['cutoff'] == '2021-10-01' and dates[0] == '2016-01-04' and dates[-1] == '2023-09-01' and len(dates) == 2000, 'market: 2,000 business days from 4 Jan 2016 to 1 Sep 2023, cut-off 1 Oct 2021 (day 1,500)', covers=[2000, 1500, 500])
f = asof_b(docs, dates)
pnl = [sgn(x) * r for x, r in zip(f, ret)]
CUT = 1500
sb, sa = sharpe(pnl[:CUT]), sharpe(pnl[CUT:])
fd = [d['score'] for d in docs]
pd_ = [sgn(x) * r for x, r in zip(fd, ret)]
sda = sharpe(pd_[CUT:])
hit_a = sum(1 for x in pnl[CUT:] if x > 0) / 500
hit_b = sum(1 for x in pnl[:CUT] if x > 0) / 1500
hit_d = sum(1 for x in pd_[CUT:] if x > 0) / 500
lv.claim(close(sb, 9.2165, 1e-3) and close(sa, 0.99598, 1e-4), f'Sharpe before {sb:.4f}, after {sa:.4f} (loop route)')
lv.claim(sum(1 for d in docs if d['published'][11:] > '16:30') / 2000 > 0.25, 'about 30% of documents come after the close')
pm, ps = statistics.fmean(pnl[CUT:]), statistics.stdev(pnl[CUT:])
bm, bs = statistics.fmean(pnl[:CUT]), statistics.stdev(pnl[:CUT])
l5 = 'l5-what-the-model-knows'
lv.expect(l5, 'screens[0].explain', round(sb, 1))
lv.expect(l5, 'screens[0].explain', round(sa, 1))
lv.expect(l5, 'screens[1].widget.answer', 500 / 2000)
lv.expect(l5, 'screens[2].prose', round(pm * 100, 4))
lv.expect(l5, 'screens[2].prose', round(ps * 100, 4))
lv.expect(l5, 'screens[2].widget.answer', round(sa, 2))
lv.expect(l5, 'screens[2].widget.wrong[0].value', round(pm / ps, 4))
lv.expect(l5, 'screens[2].widget.wrong[1].value', round(pm / ps * 252, 2))
lv.expect(l5, 'screens[2].explain', round(pm / ps, 4))
lv.expect(l5, 'screens[2].explain', round(sb, 2))
lv.expect(l5, 'screens[10].feedback.correct', round(sb, 3))
lv.expect(l5, 'screens[10].feedback.correct', round(sa, 3))
lv.claim(1250 - 1000 == 250, '250 clean days in the l5 quiz', covers=[250])
lv.literal('16:30, 16:29, 16:35, 16:40, 17:10, 18:05, 24 hours, 30 trading days', why='clock times and durations in the scenarios and test descriptions, givens')
lv.claim(close(math.log(4 / 3) + 1, 1.2876820724517808) and close((1 + 4) / (1 + 1), 5 / 2), 'fractions 4/3 (three training notes, df 2) and 5/2 (four notes, df 1)', covers=[4 / 3, 5 / 2])
lv.claim(close(math.sqrt(2 * math.log(20)) / 2, math.sqrt(2 * math.log(20)) / math.sqrt(4)), 'sqrt(2 ln 20)/2 is the noise best over 4 years', covers=[20 / 2, 20])
lv.claim(2016 - 1638 == 378 and 15 - 5 + 1 == 11, 'review: 378 clean days; 11 five-grams in 15 shared words', covers=[378, 15])
lv.literal('36, 30', why='given headline count and number of combinations in review scenarios')
lv.claim(close(round(math.sqrt(252), 3), 15.875) and round(0.0627 * 15.875, 2) == round(sa, 2), 'sqrt(252) = 15.875; 0.0627 x 15.875 = 1.00', covers=[15.875, 252])
lv.expect(l5, 'screens[3].prose', round(bm * 100, 4))
lv.expect(l5, 'screens[3].prose', round(bs * 100, 4))
lv.expect(l5, 'screens[3].widget.answer', round(sb, 1))
lv.expect(l5, 'screens[3].widget.wrong[0].value', round(bm / bs, 2))
lv.claim(sb / sa > 9, 'before is more than nine times the clean figure', covers=[9])
lv.claim(close(round(sb, 2), 9.22), 'printed 9.22')
lv.expect(l5, 'screens[3].explain', round(sb, 1))
DOC = "lenders to corran refused to extend the credit line on friday and the shares fell sharply"
CONT = "lenders to corran refused to extend the credit line on friday and its bonds fell"
def grams(t, n):
    w = t.split()
    return [tuple(w[i:i + n]) for i in range(len(w) - n + 1)]
o5 = sum(1 for g in grams(DOC, 5) if g in set(grams(CONT, 5))) / len(grams(DOC, 5))
o3 = sum(1 for g in grams(DOC, 3) if g in set(grams(CONT, 3))) / len(grams(DOC, 3))
shared = next(i for i, (a, b) in enumerate(zip(DOC.split(), CONT.split())) if a != b)
lv.claim(len(DOC.split()) == 16 and shared == 12, 'story of 16 words; the model repeats the first 12', covers=[16, 12])
lv.expect(l5, 'screens[4].widget.answer', round(o5, 4))
lv.expect(l5, 'screens[4].widget.wrong[0].value', round(o3, 4))
lv.expect(l5, 'screens[4].widget.wrong[1].value', round(12 / 16, 4))
lv.claim(len(grams(DOC, 5)) == 12 and 12 - 5 + 1 == 8 and close(o5, 2 / 3), "12 five-grams, 8 shared: two thirds", covers=[8, 2 / 3])
lv.claim(dates.index('2021-10-01') == 1499, '1 October 2021 is trading day 1,500 (index 1,499)', covers=[1499])
lv.claim(close((2023 + 8 / 12 - (2021 + 9 / 12)) / (2023 + 8 / 12 - 2016), 0.25, 0.01), 'calendar share 1.92/7.67 is close to 0.25', covers=[2023.67, 7.67, 2021.75])
lv.literal('2024.2', why='a stated cut-off position (March 2024) on the edge-case number line, a given')
# l5 quiz
lv.expect(l5, 'quiz[0].widget.answer', 250 / 1250)
lv.expect(l5, 'quiz[1].widget.answer', round(0.05 * math.sqrt(252), 2))
lv.expect(l5, 'quiz[1].widget.wrong[0].value', round(0.05 * 252, 2))
lv.expect(l5, 'quiz[2].widget.answer', round(6 / 8, 4))
lv.expect(l5, 'quiz[2].widget.wrong[0].value', round(10 / 12, 4))
lv.literal('1,250; 1,000', why='given lengths in the l5 quiz scenario')

# ------------------------------------------------------------------ l6
l6 = 'l6-text-as-a-feature'
DOCS8 = [("2023-03-06 09:15", 0.4), ("2023-03-06 16:35", -0.6), ("2023-03-07 11:00", 0.2), ("2023-03-07 15:50", 0.8),
         ("2023-03-07 18:05", -0.3), ("2023-03-08 08:40", 0.5), ("2023-03-08 16:29", 0.1), ("2023-03-09 07:55", -0.2)]
tue = [s for p, s in DOCS8 if "2023-03-06 16:30" < p <= "2023-03-07 16:30"]
wed = [s for p, s in DOCS8 if "2023-03-07 16:30" < p <= "2023-03-08 16:30"]
lv.expect(l6, 'screens[0].widget.answer', round(statistics.fmean(tue), 4))
lv.expect(l6, 'screens[0].widget.wrong[0].value', round(statistics.fmean([0.2, 0.8, -0.3]), 4))
lv.expect(l6, 'screens[0].widget.wrong[1].value', round(statistics.fmean([0.2, 0.8]), 4))
lv.claim(len([p for p, s in DOCS8 if p <= "2023-03-08 16:30"]) == 7, 'seven documents known at Wednesday 16:30', covers=[7])
lv.claim([s for p, s in DOCS8 if p <= "2023-03-08 16:30"][-1] == 0.1, 'as-of feature on Wednesday = 0.1 (d7)', covers=[0.1])
lv.expect(l6, 'screens[2].widget.answer', 0.1)
lv.expect(l6, 'screens[4].widget.answer', round(statistics.fmean(wed), 2))
lv.expect(l6, 'screens[4].widget.wrong[0].value', round((0.5 + 0.1) / 2, 2))
def agef(p, day):
    return (dt.datetime.fromisoformat(day + ' 16:30') - dt.datetime.fromisoformat(p)).total_seconds() / 86400
a1 = agef("2023-03-06 09:15", "2023-03-08")
lv.claim(close(a1, 2 + 7.25 / 24), 'd1 is 2 + 7.25/24 days old', covers=[7.25])
lv.expect(l6, 'screens[5].prose', round(a1, 4))
lv.expect(l6, 'screens[5].widget.answer', round(0.5 ** a1, 4))
lv.claim(close(0.5 ** a1, 0.2028, 1e-4), "about a fifth", covers=[1 / 5])
kn = [(p, s) for p, s in DOCS8 if p <= "2023-03-08 16:30"]
w = [0.5 ** agef(p, "2023-03-08") for p, s in kn]
decw = sum(wi * s for wi, (p, s) in zip(w, kn)) / sum(w)
lv.expect(l6, 'screens[5].explain', round(decw, 4))
lv.expect(l6, 'screens[10].feedback.correct', round(decw, 4))
lv.claim((dt.date(2023, 11, 8) - dt.date(2023, 9, 30)).days == 39, '30 September to 8 November = 39 days', covers=[39, 31, 8])
lv.claim(close(39 / 7, 5.57, 0.01), 'five and a half weeks', covers=[])
lv.literal('400', why='size of the share universe in the transfer scenario, a given')
lv.literal('12, 14, 16.5, 21.5, 40.5', why='hour positions on the transfer number line (call 14:00, close 16:30, publication 21:30, next close), givens')
lv.expect(l6, 'quiz[1].widget.answer', 0.3)
lv.expect(l6, 'quiz[2].widget.answer', round(0.5 ** 1.5, 4))
lv.claim(close((0.6 - 0.2 + 0.5) / 3, 0.3) and close(0.6 - 0.2 + 0.5, 0.9), 'quiz mean 0.30 of sum 0.9', covers=[0.9])
lv.claim(close(agef("2023-03-09 07:55", "2023-03-10"), 1 + (8 + 35 / 60) / 24), 'd8 at Friday close: 1 day 8 hours 35 minutes', covers=[35])
lv.claim(close(0.25 / 0.75, 1 / 3), 'two documents 1 and 2 days old: weights 0.5, 0.25; mean a third', covers=[0.25, 0.75, 1 / 3])

# ------------------------------------------------------------------ l7
l7 = 'l7-leaks-in-text'
train = ["corran margins steady as costs ease", "corran guidance raised on strong sales", "corran sales slip as demand cools"]
voc = {w for t in train for w in t.split()}
miss = [x for x in "zenvia orders lift corran guidance".split() if x not in voc]
lv.expect(l7, 'screens[0].widget.answer', len(miss))
lv.expect(l7, 'screens[2].widget.answer', round(math.log(4 / 3) + 1, 4))
lv.expect(l7, 'screens[2].widget.wrong[0].value', round(math.log(6 / 4) + 1, 4))
lv.expect(l7, 'screens[3].prose', round(hit_a * 100, 1))
lv.expect(l7, 'screens[3].prose', round(hit_d * 100, 1))
lv.expect(l7, 'screens[3].widget.answer', round((hit_d - hit_a) * 100, 1))
lv.expect(l7, 'screens[3].widget.wrong[0].value', round(hit_d / hit_a, 2))
lv.expect(l7, 'screens[3].explain', round(hit_b * 100, 1))
for v in (hit_a, hit_d, hit_b):
    lv.expect(l7, 'screens[3].canvas', round(v, 3))
RAW = [0.62, 0.35, -0.41, 0.80, 0.15, -0.22, 0.55, 0.40]
MSK = [0.30, 0.31, -0.45, 0.42, 0.12, -0.20, 0.18, 0.36]
D_ = [round(a - b, 2) for a, b in zip(RAW, MSK)]
md, sd_ = statistics.fmean(D_), statistics.stdev(D_)
se_ = sd_ / math.sqrt(8)
lv.claim(close(sum(D_), 1.2), 'changes add up to 1.20', covers=[1.2])
for v in D_:
    lv.expect(l7, 'screens[4].canvas', v)
lv.expect(l7, 'screens[4].widget.answer', round(md, 4))
lv.expect(l7, 'screens[5].prose', round(sd_, 4))
lv.expect(l7, 'screens[5].widget.answer', round(se_, 4))
lv.expect(l7, 'screens[5].widget.wrong[1].value', round(sd_ / 8, 4))
lv.expect(l7, 'screens[5].feedback.correct', round(md / se_, 1))
lv.expect(l7, 'screens[5].explain', round(math.sqrt(8), 4))
lv.claim(all(d > 0.3 for d in (D_[0], D_[3], D_[6])), 'h1, h4, h7 drop by more than 0.3', covers=[0.3])
R4, M4 = [0.5, -0.1, 0.3, 0.2], [0.42, 0.05, 0.31, 0.14]
D4_ = [round(a - b, 2) for a, b in zip(R4, M4)]
m4, s4 = statistics.fmean(D4_), statistics.stdev(D4_) / 2
lv.expect(l7, 'screens[6].prose', round(m4, 4))
lv.expect(l7, 'screens[6].prose', round(s4, 4))
lv.expect(l7, 'screens[6].feedback.correct', round(2 * s4, 2))
for v in D4_ + R4 + M4:
    lv.expect(l7, 'screens[6].canvas', v)
lv.claim(close(round(s4, 2), 0.05) and 2 * s4 > 0.1 - 0.01, 'standard error near 0.05: a change of 0.1 is about two standard errors away', covers=[0.05, 0.1])
for v in RAW + MSK:
    lv.expect(l7, 'screens[4].canvas', v)
lv.expect(l7, 'quiz[1].widget.answer', 0.2)
lv.claim(close((0.2 + 0.1 + 0.3 + 0.0 + 0.4) / 5, 0.2), 'quiz mean 0.20', covers=[1.0, 0.4])
lv.expect(l7, 'quiz[2].widget.answer', round(0.10 / 10, 2))
lv.claim(close(0.03 / 0.01, 3), 'three standard errors', covers=[0.03, 3])

# ------------------------------------------------------------------ l8
l8 = 'l8-an-honest-text-backtest'
k12 = math.sqrt(2 * math.log(12)) / math.sqrt(2)
lv.claim(close(round(math.sqrt(2 * math.log(12)), 4), 2.2293) and close(round(k12, 4), 1.5764) and close(round(math.sqrt(2), 4), 1.4142), 'sqrt(2 ln 12) = 2.2293, over sqrt 2 = 1.5764', covers=[2.2293, 1.5764, 1.4142])


def emax(n, grid=200001, lim=9.0):
    """Expected maximum of n standard normals by trapezoid integration of x n phi(x) Phi(x)^(n-1) (route two: simulation below)."""
    x = np.linspace(-lim, lim, grid)
    phi = np.exp(-x * x / 2) / math.sqrt(2 * math.pi)
    cdf = 0.5 * (1 + np.array([math.erf(v / math.sqrt(2)) for v in x]))
    return float(np.trapezoid(x * n * phi * cdf ** (n - 1), x))


sim = np.random.default_rng(5).standard_normal((200000, 12)).max(axis=1).mean()
e12 = emax(12)
lv.claim(close(e12, sim, 0.01) and close(e12 / math.sqrt(2), 1.15, 0.005) and e12 < math.sqrt(2 * math.log(12)),
         f'the noise best of 12 averages {e12:.4f}, so about 1.15 over two years, below the allowance 1.58', covers=[1.15])
lv.expect(l8, 'screens[0].widget.answer', round(2.1 - k12, 2))
lv.expect(l8, 'screens[0].widget.wrong[1].value', round(2.1 - math.sqrt(2 * math.log(12)), 2))
nmin = next(n for n in range(1, 1000) if math.sqrt(2 * math.log(n)) / math.sqrt(2) >= 2)
lv.expect(l8, 'screens[1].widget.answer', nmin)
lv.claim(close(round(math.exp(4), 1), 54.6), 'e^4 = 54.6', covers=[54.6])
lv.expect(l8, 'screens[2].widget.answer', 400)
cost = 0.0002
shc = (pm - cost) / ps * math.sqrt(252)
lv.expect(l8, 'screens[3].widget.answer', round(shc, 2))
lv.expect(l8, 'screens[3].widget.wrong[1].value', round((pm - cost) / ps * 252, 1))
lv.claim(close((sa - shc) / sa, 1 / 3, 0.02), 'costs take about a third of the clean Sharpe', covers=[1 / 3, 0.02])
# four designs by the loop route
fc = f[CUT:]
rc = ret[CUT:]
n = len(fc)
b = [round(i * n / 5) for i in range(6)]
wf = []
for k in range(1, 5):
    past = [x for x in fc[:b[k]] if x is not None]
    mu = sum(past) / len(past)
    wf += [sgn(None if x is None else x - mu) * r for x, r in zip(fc[b[k]:b[k + 1]], rc[b[k]:b[k + 1]])]
muf = statistics.fmean([x for x in fc if x is not None])
full = [sgn(None if x is None else x - muf) * r for x, r in zip(fc[b[1]:], rc[b[1]:])]
lv.claim(len(wf) == 400, 'walk-forward: 400 out-of-sample days')
lv.expect(l8, 'screens[10].feedback.correct', round(sharpe(wf), 3))
lv.expect(l8, 'screens[9].feedback.correct', round(2.1 - k12, 4))
for v in (sharpe(pnl), sda, sharpe(full), sharpe(wf)):
    lv.expect(l8, 'screens[4]', round(v, 2))
need6 = 1.96 / math.sqrt(0.5)
lv.expect(l8, 'screens[5].widget.answer', round(need6, 2))
lv.expect(l8, 'screens[5].widget.wrong[0].value', round(1.96 * math.sqrt(0.5), 2))
lv.expect(l8, 'screens[5].widget.wrong[1].value', round(1.96 / 0.5, 2))
lv.expect(l8, 'screens[6].widget.answer', round(1.9 - k12, 2))
lv.literal('0.5 and 2', why='a typical range of real signal Sharpe ratios, stated as context, not computed')
lv.expect(l8, 'quiz[0].widget.answer', round(1.6 - math.sqrt(2 * math.log(20)) / 2, 2))
lv.expect(l8, 'quiz[0].explain', round(math.sqrt(2 * math.log(20)), 4))
lv.expect(l8, 'quiz[0].explain', round(math.sqrt(2 * math.log(20)) / 2, 4))
lv.expect(l8, 'quiz[1].widget.answer', 500)
lv.literal('600', why='the clean-window length given in the l8 quiz')
lv.claim(close(round(need6, 1), 2.8), 'summary: six months needs about 2.8', covers=[2.8])

# ------------------------------------------------------------------ review
lv.expect('review', 'items[0].widget.answer', round(378 / 2016, 4))
lv.expect('review', 'items[1].widget.answer', round(0.08 / 1.2 * math.sqrt(252), 2))
lv.claim(close(round(0.08 / 1.2, 4), 0.0667), 'daily ratio 0.0667', covers=[0.0667])
lv.expect('review', 'items[2].widget.answer', round(11 / 16, 4))
lv.expect('review', 'items[4].widget.answer', round(0.5 ** 0.5, 4))
lv.claim((dt.date(2024, 2, 14) - dt.date(2023, 12, 31)).days == 45, '31 December to 14 February = 45 days', covers=[45, 14])
lv.expect('review', 'items[6].widget.answer', 0.04)
lv.claim(close(0.06 / 0.04, 1.5), '1.5 standard errors', covers=[1.5, 0.06, 0.24])
lv.expect('review', 'items[7].widget.answer', round(math.log(5 / 2) + 1, 4))
lv.expect('review', 'items[7].widget.wrong[0].value', round(math.log(11 / 7) + 1, 4))
hr = 1.8 - math.sqrt(2 * math.log(30)) / math.sqrt(3)
lv.expect('review', 'items[8].widget.answer', round(hr, 2))
lv.expect('review', 'items[8].feedback.correct', round(math.sqrt(2 * math.log(30)), 4))
lv.expect('review', 'items[8].feedback.correct', round(math.sqrt(3), 4))
lv.literal('2,016; 1,638', why='given lengths in the review scenario')

# ------------------------------------------------------------------ homework
lv.expect('homework', 'items[4].widget.answer', round((1764 - 1260 - 63) / 252, 2))
lv.claim(1764 - 1260 == 504 and 504 - 63 == 441, '504 days after the cut-off, 441 after the buffer', covers=[504, 441, 1764, 1260, 63])
lv.literal('2.4, 0.6, 6', why='a team\'s reported figures in the homework scenario, givens')
lv.literal('2012 to 2023, 3', why='the vendor pitch in the long-form item, givens')

# ------------------------------------------------------------------ problem set
nb = math.sqrt(2 * math.log(25)) / math.sqrt(2)
lv.expect('problems', 'items[0].parts[0].widget.answer', 504 / 2520)
lv.expect('problems', 'items[0].parts[1].widget.answer', 504 / 252)
lv.expect('problems', 'items[0].parts[2].widget.answer', round(nb, 4))
lv.claim(close(round(math.sqrt(2 * math.log(25)), 5), 2.53727) and close(round(math.sqrt(2), 5), 1.41421), 'printed 2.53727/1.41421', covers=[2.53727, 1.41421, round(math.sqrt(2 * math.log(25)), 4)])
lv.expect('problems', 'items[0].parts[3].widget.answer', round(2.4 - nb, 4))
lv.expect('problems', 'items[0].parts[4]', round(1.96 / math.sqrt(2), 2))
lv.literal('2,520; 2,016; 25', why='given backtest length, cut-off day and number of versions in the problem')
wa = (24 + 16.5 - (9 + 1 / 6)) / 24
lv.expect('problems', 'items[1].parts[2].widget.answer', round(0.5 ** wa, 4))
lv.expect('problems', 'items[1].parts[2].feedback.correct', round(wa, 4))
lv.expect('problems', 'items[1].parts[1].widget.answer', round((-0.4 + 0.3) / 2, 2))
lv.expect('problems', 'items[1].parts[1].widget.wrong[1].value', round((0.6 - 0.4 + 0.3) / 3, 2))
lv.claim(close(wa * 24, 31 + 20 / 60), '31 hours 20 minutes', covers=[31, 20])
DW = [0.22, -0.02, 0.02, 0.22, -0.01, 0.19]
lv.claim(DW == [round(a - b, 2) for a, b in zip([0.42, 0.10, -0.25, 0.33, 0.05, 0.28], [0.20, 0.12, -0.27, 0.11, 0.06, 0.09])], 'the six changes come from the raw and masked scores')
mw, sw = statistics.fmean(DW), statistics.stdev(DW)
lv.expect('problems', 'items[2].parts[0].widget.answer', round(mw, 4))
lv.expect('problems', 'items[2].parts[0].feedback.correct', round(sum(DW), 2))
lv.expect('problems', 'items[2].parts[1].question', round(sw, 4))
lv.expect('problems', 'items[2].parts[1].widget.answer', round(sw / math.sqrt(6), 4))
lv.expect('problems', 'items[2].parts[1].explain', round(math.sqrt(6), 4))
lv.expect('problems', 'items[2].parts[2].widget.answer', round(mw / (sw / math.sqrt(6)), 2))
lv.expect('problems', 'items[2].parts[2].widget.wrong[0].value', round((sw / math.sqrt(6)) / mw, 2))
lv.claim(close(1.96 / math.sqrt(2), 1.386, 1e-3), 'bar about 1.39', covers=[1.39])
lv.claim(all(abs(d - 0.2) < 0.03 for d in (0.22, 0.22, 0.19)), 'three headlines dropped by about 0.2', covers=[0.2])
lv.claim(close(round(mw, 1), 0.1) and close(mw / (sw / math.sqrt(6)), 2.14, 0.01), 'a mean change of about 0.1, about two standard errors', covers=[0.1, 2])

# ------------------------------------------------------------------ every code widget: solution, twin, starter and mutants in CPython
TWINS = {
    'clean_window': """
import datetime as _d
def clean_window(dates, cutoff, buffer_days):
    e = _d.date.fromisoformat(cutoff).toordinal() + buffer_days
    return [x for x in dates if _d.date.fromisoformat(x).toordinal() > e]
def share_after_cutoff(dates, cutoff):
    return len([x for x in dates if x > cutoff]) / len(dates)
""",
    'sharpe_by_period': """
import statistics, math
def sharpe_by_period(pnl, dates, cutoff):
    a = [float(p) for p, d in zip(pnl, dates) if d <= cutoff]
    b = [float(p) for p, d in zip(pnl, dates) if d > cutoff]
    sr = lambda x: statistics.fmean(x) / statistics.stdev(x) * math.sqrt(252)
    return sr(a), sr(b)
""",
    'known_by': """
import bisect
def known_by(docs, t):
    return sorted([d for d in docs if not d['published'] > t], key=lambda d: d['published'])
def asof_feature(docs, days, decision_time):
    ds = sorted(docs, key=lambda d: d['published']); ts = [d['published'] for d in ds]
    out = []
    for day in days:
        i = bisect.bisect_right(ts, day + ' ' + decision_time)
        out.append(ds[i - 1]['score'] if i else None)
    return out
""",
    'decayed_score': """
def _mins(s):
    import datetime as _d
    y, mo, da = int(s[:4]), int(s[5:7]), int(s[8:10])
    return _d.date(y, mo, da).toordinal() * 1440 + int(s[11:13]) * 60 + int(s[14:16])
def decayed_score(docs, day, half_life, decision_time='16:30'):
    t = _mins(day + ' ' + decision_time)
    ws = [(2 ** (-(t - _mins(d['published'])) / 1440 / half_life), d['score']) for d in docs if _mins(d['published']) <= t]
    if not ws:
        return None
    return sum(w * s for w, s in ws) / sum(w for w, s in ws)
""",
    'fit_vocab_in_fold': """
from sklearn.feature_extraction.text import TfidfVectorizer
def fit_vocab_in_fold(train_docs):
    v = TfidfVectorizer(token_pattern='[a-z]+').fit(train_docs)
    vocab = list(v.get_feature_names_out())
    return {'vocab': vocab, 'idf': dict(zip(vocab, (float(x) for x in v.idf_))), '_v': v}
def transform(test_docs, model):
    if '_v' in model:
        return model['_v'].transform(test_docs).toarray().tolist()
    raise ValueError
""",
    'mask_entities': """
import re, statistics, math
def mask_entities(text, names):
    for n in sorted(names, key=lambda s: -len(s)):
        text = re.sub('(?<![A-Za-z0-9_])' + re.escape(n) + '(?![A-Za-z0-9_])', 'NAME', text, flags=re.I)
    return text
def masking_effect(r, m):
    d = [a - b for a, b in zip(r, m)]
    return statistics.fmean(d), statistics.stdev(d) / math.sqrt(len(d))
""",
    'haircut': """
def haircut(best_sharpe, n_trials, years):
    import math
    return best_sharpe - (2 * math.log(n_trials) / years) ** 0.5
""",
    'honest_backtest': """
import numpy as np, pandas as pd
def honest_backtest(panel, docs, cutoff, folds, decision_time='16:30'):
    P = pd.DataFrame({'date': panel['dates'], 'ret': panel['ret']})
    P = P[P['date'] > cutoff].reset_index(drop=True)
    P['decision'] = pd.to_datetime(P['date'] + ' ' + decision_time)
    D = pd.DataFrame(docs); D['t'] = pd.to_datetime(D['published']); D = D.sort_values('t')
    J = pd.merge_asof(P, D[['t', 'score']], left_on='decision', right_on='t', direction='backward')
    f = J['score'].to_numpy(dtype=float); r = J['ret'].to_numpy(dtype=float)
    n = len(f); b = [round(i * n / folds) for i in range(folds + 1)]
    out = []
    for k in range(1, folds):
        mu = np.nanmean(f[:b[k]])
        out.append(np.nan_to_num(np.sign(f[b[k]:b[k + 1]] - mu)) * r[b[k]:b[k + 1]])
    x = np.concatenate(out)
    return float(x.mean() / x.std(ddof=1) * np.sqrt(252))
""",
    'text_signal_report': """
import numpy as np, pandas as pd, datetime as _d
def text_signal_report(panel, docs, cutoff, buffer_days, folds, n_trials, decision_time='16:30'):
    edge = str(_d.date.fromisoformat(cutoff) + _d.timedelta(days=buffer_days))
    P = pd.DataFrame({'date': panel['dates'], 'ret': panel['ret']})
    P = P[P['date'] > edge].reset_index(drop=True)
    P['decision'] = pd.to_datetime(P['date'] + ' ' + decision_time)
    D = pd.DataFrame(docs); D['t'] = pd.to_datetime(D['published']); D = D.sort_values('t')
    J = pd.merge_asof(P, D[['t', 'score']], left_on='decision', right_on='t', direction='backward')
    f = J['score'].to_numpy(dtype=float); r = J['ret'].to_numpy(dtype=float)
    n = len(f); b = [round(i * n / folds) for i in range(folds + 1)]
    out = []
    for k in range(1, folds):
        mu = np.nanmean(f[:b[k]])
        out.append(np.nan_to_num(np.sign(f[b[k]:b[k + 1]] - mu)) * r[b[k]:b[k + 1]])
    x = np.concatenate(out)
    s = float(x.mean() / x.std(ddof=1) * np.sqrt(252))
    return {'sharpe': s, 'haircut': s - np.sqrt(2 * np.log(n_trials)) / np.sqrt(len(x) / 252)}
""",
    'name_masking_test': """
import re, statistics, math
def name_masking_test(texts, names, score):
    def mk(t):
        for n in sorted(names, key=lambda s: -len(s)):
            t = re.sub('(?<![A-Za-z0-9_])' + re.escape(n) + '(?![A-Za-z0-9_])', 'NAME', t, flags=re.I)
        return t
    d = [score(t) - score(mk(t)) for t in texts]
    m = statistics.fmean(d); se = statistics.stdev(d) / math.sqrt(len(d))
    return m, se, (m / se if se else 0.0)
""",
}


def norm(v):
    if hasattr(v, 'tolist'):
        v = v.tolist()
    if isinstance(v, tuple):
        v = list(v)
    if isinstance(v, dict):
        return {k: norm(x) for k, x in v.items() if not k.startswith('_')}
    return [norm(x) for x in v] if isinstance(v, list) else v


def same(a, b, cmp, tol):
    a, b = norm(a), norm(b)
    if isinstance(a, dict) or isinstance(b, dict):
        return isinstance(a, dict) and isinstance(b, dict) and set(a) == set(b) and all(same(a[k], b[k], cmp, tol) for k in a)
    if isinstance(a, list) or isinstance(b, list):
        return isinstance(a, list) and isinstance(b, list) and len(a) == len(b) and all(same(x, y, cmp, tol) for x, y in zip(a, b))
    if cmp == 'isclose' and isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        rel = (tol or {}).get('rel', 1e-9 if not tol else 0) or 0
        ab = (tol or {}).get('abs', 1e-12 if not tol else 0) or 0
        return math.isclose(a, b, rel_tol=rel, abs_tol=ab)
    return a == b


def run(w, src):
    cwd = os.getcwd()
    os.chdir(DATA)
    res = []
    try:
        ns = {'__name__': '__zq__', '__learner_source__': src}
        exec(ZQ_LIB, ns)
        try:
            exec(w.get('prelude', ''), ns)
            exec(src, ns)
        except Exception:
            return [False] * len(w['tests'])
        for t in w['tests']:
            try:
                if t.get('setup'):
                    exec(t['setup'], ns)
                res.append(same(eval(t['call'], ns), eval(t['expect'], ns), t.get('compare', 'equal'), t.get('tol')))
            except Exception:
                res.append(False)
    finally:
        os.chdir(cwd)
    return res


n_code = 0
for fid, doc in F.items():
    for key in ('screens', 'items'):
        for i, s in enumerate(doc.get(key, [])):
            w = s.get('widget')
            if not (isinstance(w, dict) and w.get('kind') == 'code'):
                continue
            path, bk = f'{key}[{i}]', s.get('feedback', {}).get('byKey', {})
            n_code += 1
            r = run(w, w['solution'])
            lv.claim(all(r), f'{fid} {path}: the model solution passes all {len(r)} hidden tests in CPython')
            name = next(k for k in TWINS if f'def {k}(' in w['solution'])
            rt = run(w, TWINS[name])
            lv.claim(all(rt), f'{fid} {path}: an independent twin ({name}) passes them too' + ('' if all(rt) else f' (fails {[j + 1 for j, x in enumerate(rt) if not x]})'))
            lv.claim(not all(run(w, w['starter'])), f'{fid} {path}: the starter fails')
            ms = w.get('mutants', [])
            lv.claim(len(ms) >= 2, f'{fid} {path}: {len(ms)} mutants')
            for m in ms:
                rm = run(w, m['source'])
                first = next((j + 1 for j, x in enumerate(rm) if not x), None)
                lv.claim(first == m['test'] and f"test-{m['test']}" in bk, f"{fid} {path}: mutant '{m['symptom'][:40]}' first fails test {m['test']}, which has a byKey line")
            lv.claim(all(any(m['test'] == int(k.split('-')[1]) for m in ms) for k in bk if k.startswith('test-')), f'{fid} {path}: every byKey test line is reached by a mutant')
lv.claim(n_code == 10, f'{n_code} code widgets in the level')
# the seeded expects: walk-forward on seed 0 equals the table's figure, by the loop route above
hb = F['l8-an-honest-text-backtest']['screens'][10]['widget']['tests'][3]
lv.claim(close(eval(hb['expect']), sharpe(wf), 1e-9), 'honest_backtest seed 0, 5 folds: the stored expect equals the loop route')
lv.claim(close(eval(F['l5-what-the-model-knows']['screens'][10]['widget']['tests'][4]['expect'])[1], sa, 1e-9), 'sharpe_by_period seed 0: stored expect equals the loop route')
lv.literal('$10^{-9}$, $10^{-12}$, 0.0005, 0.002, $10^{-6}$', why='tolerances named in how lines are settings of the hidden tests, which this script runs')
lv.literal('90, 91, 60, 1,000, 8 trials, 12 trials', why='test settings named in how lines (buffers, half-lives, trial counts); the tests themselves are run above')
lv.check_wrongs()
lv.report()
