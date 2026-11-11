"""Concept audit, recruiting level 2 (l6 to l10, review-2, homework-2).
Recomputes speaking budgets, guess values, retake dates and model word counts,
and simulates the two empirical claims (best of 200 Sharpe; survivorship).
Exits 0 when the content is right.
Run: python3 docs/reports/recruiting-L2-concepts.py
"""
import json, os, re, sys
from datetime import date
from fractions import Fraction as F
import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
C = os.path.join(ROOT, 'app', 'content', 'courses', 'recruiting')
J = lambda n: json.load(open(os.path.join(C, n + '.json')))
fails = []


def check(name, ok, detail=''):
    print(('ok   ' if ok else 'FAIL ') + name + (' | ' + detail if detail else ''))
    if not ok:
        fails.append(name)


near = lambda a, b, tol: abs(a - b) <= tol


def add_months(d, m):
    y, mo = divmod(d.month - 1 + m, 12)
    return date(d.year + y, mo + 1, d.day)


WPM = 130
words = lambda secs: WPM * secs / 60

# ---- l6 ----
check('l6 s2 40/6 = 6.7 times', near(40 / 6, 6.7, 0.05))

# ---- l7 ----
l7 = J('l7-projects-that-count')
check('l7 budget 15+30+45+30 = 120', 15 + 30 + 45 + 30 == 120)
pts = [p['target'] for p in l7['screens'][3]['widget']['points']]
check('l7 s3 boundaries 15, 45, 90', pts == [15, 45, 90])
check('l7 s4 260 words key', l7['screens'][4]['widget']['answer'] == words(120))
check('l7 s9 45 s = 97.5 words', words(45) == 97.5 and 260 - 65 - 65 - 32.5 == 97.5)
check('l7 quiz2 90 s = 195 words', l7['quiz'][2]['widget']['answer'] == words(90))
# Empirical: best of 200 no-edge strategies over 3 years has expected Sharpe near 1.6
rng = np.random.default_rng(11)
reps, n, T = 2000, 200, 36
r = rng.standard_normal((reps, n, T))
sh = r.mean(axis=2) / r.std(axis=2, ddof=1) * np.sqrt(12)
best = sh.max(axis=1).mean()
check('l7 s7 expected best-of-200 Sharpe, 3 years of monthly data, near 1.6', 1.45 <= best <= 1.8, '%.2f' % best)
# Empirical: does leaving out delisted shares flatter a long-short momentum result?
# Toy market with no true momentum; a share delists (final return -100%) when its price falls below a floor.
rng = np.random.default_rng(5)
S, M = 3000, 240
ret = rng.normal(0.005, 0.10, (S, M))
price = np.ones(S); alive = np.ones(S, bool); dead_at = np.full(S, M)
for t in range(M):
    price *= 1 + ret[:, t]
    hit = alive & (price < 0.25)
    ret[hit, t] = -1.0
    dead_at[hit] = t
    alive &= ~hit


def momentum(mask_universe):
    longs, shorts = [], []
    for t in range(12, M - 1):
        live = mask_universe & (dead_at > t)        # tradable at the end of month t
        idx = np.where(live)[0]
        past = np.prod(1 + ret[idx, t - 11:t + 1], axis=1)
        k = len(idx) // 10
        order = np.argsort(past)
        longs.append(ret[idx[order[-k:]], t + 1].mean())
        shorts.append(ret[idx[order[:k]], t + 1].mean())
    return np.mean(longs), np.mean(shorts)


L_all, S_all = momentum(np.ones(S, bool))
L_sur, S_sur = momentum(dead_at == M)                # today's list only
print('info l7 s10 / hw2: long leg  monthly mean, all shares %.4f, survivors only %.4f' % (L_all, L_sur))
print('info l7 s10 / hw2: short leg monthly mean, all shares %.4f, survivors only %.4f' % (S_all, S_sur))
print('info l7 s10 / hw2: long minus short,      all shares %.4f, survivors only %.4f' % (L_all - S_all, L_sur - S_sur))
check('survivorship flatters the long leg (the claim as taught holds for long positions)', L_sur > L_all)
print('info: the long-short figure can move either way, because the losers that go bust are profits for the short leg')


# Fix pass (audit): the sign of the long-short bias depends on why shares leave the data.
# Three toy markets, no true momentum in returns. 'floor': bankruptcy after a long fall (-100%).
# 'takeover': recent winners bought out at a +30% premium. 'crash': recent winners collapse (-100%).
def ls_bias(scenario, seed=8, S=2000, M=240):
    g = np.random.default_rng(seed)
    rr = g.normal(0.005, 0.10, (S, M))
    dead = np.full(S, M); live_now = np.ones(S, bool); px = np.ones(S)
    for t in range(M):
        px *= 1 + rr[:, t]
        past = np.prod(1 + rr[:, max(0, t - 11):t + 1], axis=1)
        if scenario == 'floor':
            hit = live_now & (px < 0.25); rr[hit, t] = -1.0
        elif scenario == 'crash':
            hit = live_now & (past > 1.6) & (g.random(S) < 0.03); rr[hit, t] = -1.0
        else:
            hit = live_now & (past > 1.6) & (g.random(S) < 0.08); rr[hit, t] += 0.30
        dead[hit] = t; live_now &= ~hit

    def ls(univ):
        out = []
        for t in range(12, M - 1):
            idx = np.where(univ & (dead > t))[0]
            o = np.argsort(np.prod(1 + rr[idx, t - 11:t + 1], axis=1)); k = len(idx) // 10
            out.append(rr[idx[o[-k:]], t + 1].mean() - rr[idx[o[:k]], t + 1].mean())
        return np.mean(out)
    return ls(dead == M) - ls(np.ones(S, bool))   # survivors only minus all shares


biases = {sc: ls_bias(sc) for sc in ('floor', 'takeover', 'crash')}
print('info fix pass: survivors-only minus all shares, long-short monthly: ' +
      ', '.join('%s %+.4f' % kv for kv in biases.items()))
check('fix pass: long-short survivorship bias takes both signs across plausible markets',
      min(biases.values()) < -0.002 and max(biases.values()) > 0.002)
key = [o for o in l7['screens'][10]['widget']['options'] if o.get('correct')][0]['text']
texts = [key, l7['screens'][10]['hints'][2]['text'], l7['screens'][10]['explain']['text'],
         J('homework-2')['items'][4]['widget']['model']]
check('fix pass: l7 s10 key, hint, explain and hw2 model assert no direction for the long-short bias',
      not any(re.search(r'overstat|flatter|looks better', t) for t in texts) and 'delisted' in key)

# ---- l8 ----
l8 = J('l8-why-this-firm')
check('l8 s4 45 s = 97.5 words key', l8['screens'][4]['widget']['answer'] == words(45))
check('l8 quiz2 250 words = 115 s key', near(l8['quiz'][2]['widget']['answer'], 250 / WPM * 60, 3), '%.1f' % (250 / WPM * 60))

# ---- l9 ----
l9 = J('l9-sitting-an-assessment')
ev = lambda k, pen=1: F(1, k) - F(k - 1, k) * pen
check('l9 s3 blind guess key -0.5', F(l9['screens'][3]['widget']['answer']).limit_denominator(100) == ev(4))
check('l9 s4 values -1/2, -1/3, 0, +1', [ev(k) for k in (4, 3, 2, 1)] == [F(-1, 2), F(-1, 3), 0, 1])
check('l9 summary E = 2p - 1', all(ev(k) == 2 * F(1, k) - 1 for k in (1, 2, 3, 4)))
check('l9 s5 60/17 key', near(l9['screens'][5]['widget']['answer'], 60 / 17, 0.02))
check('l9 s5 480/80 = 6 s', 480 / 80 == 6 and l9['quiz'][0]['widget']['answer'] == 6)
check('l9 s2 15 Nov 2026 + 8 months = 15 Jul 2027', add_months(date(2026, 11, 15), 8) == date(2027, 7, 15))
check('l9 s10 five options, -0.25: blind guess 0', ev(5, F(1, 4)) == 0 and l9['screens'][10]['widget']['answer'] == 0)
check('l9 s10 one ruled out: 1/16', ev(4, F(1, 4)) == F(1, 16))
check('l9 quiz3 1 Dec 2026 + 8 months = 1 Aug 2027', add_months(date(2026, 12, 1), 8) == date(2027, 8, 1))

# ---- l10 ----
l10 = J('l10-recorded-video')
check('l10 s1 30/120 key', l10['screens'][1]['widget']['answer'] == 30 / 120)
check('l10 budget 10+80+30 = 120', 10 + 80 + 30 == 120)
check('l10 s3 80 s = 173.3 words key', near(l10['screens'][3]['widget']['answer'], words(80), 0.1))

# ---- review-2 ----
r2 = {i['id']: i for i in J('review-2')['items']}
check('review-2 90 s result share key 33.75', r2['r2-budget-90']['widget']['answer'] == 45 / 120 * 90)
check('review-2 33.75 s is about 73 words', near(words(33.75), 73, 0.5))
check('review-2 one ruled out key -1/3', near(r2['r2-one-out']['widget']['answer'], float(ev(3)), 0.001))
check('review-2 15 items in 25 min key 100 s', r2['r2-sequence-pace']['widget']['answer'] == 25 * 60 / 15)
d = add_months(date(2026, 11, 20), 8)
check('review-2 20 Nov 2026 + 8 months = 20 Jul 2027, about three weeks after 1 Jul',
      d == date(2027, 7, 20) and (d - date(2027, 7, 1)).days == 19)

# ---- homework-2 ----
h2 = {i['id']: i for i in J('homework-2')['items']}
check('hw2 net score key 48', h2['hw2-net-score']['widget']['answer'] == 60 * (0.9 - 0.1) + 10 * 0 and 54 - 6 == 48)


def body_words(model, start, stop):
    t = model.split(start, 1)[1].split(stop, 1)[0]
    t = re.sub(r'\*[^*\n]*\*', ' ', t) if start != '\n\n' else t
    return len(t.split())


for key, claim in [('hw2-why-1', 85), ('hw2-why-2', 81), ('hw2-why-3', 85)]:
    m = h2[key]['widget']['model']
    para = m.split('\n\n')[1]
    n = len(para.split())
    check('%s model is about %d words' % (key, claim), abs(n - claim) <= 6, 'counted %d' % n)
check('hw2-why-1 85 words is under 40 s', 85 / WPM * 60 < 40)
m = h2['hw2-project-account']['widget']['model']
paras = [p for p in m.split('\n\n') if re.match(r'^\*[^*]+\(about \d+ s\)\.\*', p)]
n = sum(len(re.sub(r'^\*[^*]*\*', '', p).split()) for p in paras)
check('hw2 project account is about 210 words', abs(n - 210) <= 12, 'counted %d' % n)
check('hw2 210 words is 1 min 36 s to 1 min 37 s', 96 <= 210 / WPM * 60 <= 97.5, '%.1f s' % (210 / WPM * 60))
check('hw2 section times 12+25+34+25 = 96 s', 12 + 25 + 34 + 25 == 96)
cv = h2['hw2-cv']['widget']['model']
dates = re.findall(r'(?:[A-Z][a-z]{2} )?20\d\d to (?:[A-Z][a-z]{2} )?(?:20\d\d|now)', cv)
month_style = [bool(re.match(r'[A-Z][a-z]{2} ', d)) for d in dates]
check('hw2 CV model keeps one date format, as its own rubric asks', len(set(month_style)) == 1, '; '.join(dates))

print('\n%d failing' % len(fails))
sys.exit(1 if fails else 0)
