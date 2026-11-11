"""Concept audit, recruiting level 3 (l11 to l15, review-3, homework-3).
Recomputes the game values, day plans, offer dates, rates and model word counts,
with exact enumeration and a Monte Carlo cross-check for each game.
Exits 0 when the content is right.
Run: python3 docs/reports/recruiting-L3-concepts.py
"""
import json, os, sys
from datetime import date, timedelta
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
WPM = 130
rng = np.random.default_rng(3)
N = 400000

# ---- l11 ----
l11 = J('l11-stories-that-answer')
check('l11 budget 15+10+60+20+15 = 120', 15 + 10 + 60 + 20 + 15 == 120)
check('l11 s9 action words key 130', l11['screens'][9]['widget']['answer'] == WPM * 60 / 60)
check('l11 s9 S and T, 25 s, about 54 words', near(WPM * 25 / 60, 54, 0.5))

# ---- l12: games ----
faces = range(1, 7)
v0 = F(sum(faces), 6)                                   # no reroll
v1 = sum(F(max(F(f), v0), 6) for f in faces)            # one reroll, optimal
v2 = sum(F(max(F(f), v1), 6) for f in faces)            # two rerolls, optimal
check('l12 s0 one reroll worth 4.25', v1 == F(17, 4))
check('l12 s0 keep part 2.5 and reroll part 1.75', F(4 + 5 + 6, 6) == F(5, 2) and F(1, 2) * v0 == F(7, 4))
check('l12 s10 two rerolls worth 14/3', v2 == F(14, 3) and F(5 + 6, 6) + F(4, 6) * v1 == F(14, 3))
a = rng.integers(1, 7, N); b = rng.integers(1, 7, N); c = rng.integers(1, 7, N)
mc1 = np.where(a >= 4, a, b).mean()
mc2 = np.where(a >= 5, a, np.where(b >= 4, b, c)).mean()
check('l12 Monte Carlo one reroll', near(mc1, 4.25, 0.02), '%.3f' % mc1)
check('l12 Monte Carlo two rerolls', near(mc2, 14 / 3, 0.02), '%.3f' % mc2)
check('l12 s2 flips to first head: E = 1 + E/2 gives 2', near(rng.geometric(0.5, N).mean(), 2, 0.02))
check('l12 s3 rolls to first six: E = 1 + 5E/6 gives 6', near(rng.geometric(1 / 6, N).mean(), 6, 0.05))
cc = sum(F(6, k) for k in range(1, 7))
check('l12 s5 all six faces: 14.7 rolls', near(float(cc), 14.7, 0.005), str(float(cc)))
check('l12 s6 two reds from 3 red 2 blue: 3/10', F(3, 5) * F(2, 4) == F(3, 10))
check('l12 s7 total of 7 with two dice: 6/36',
      sum(1 for i in faces for j in faces if i + j == 7) == 6)
check('l12 s9 coin +2/-1 worth 0.5', F(1, 2) * 2 - F(1, 2) * 1 == F(1, 2))
l12 = J('l12-reasoning-aloud')
check('l12 quiz1 coin +3/-2 key 0.5', l12['quiz'][1]['widget']['answer'] == 0.5)
check('l12 s11 300 x 300 = 90,000, inside 70,000 to 110,000', 300 * 300 == 90000)

# ---- l13 ----
l13 = J('l13-the-final-round')
check('l13 s3 two aces 1/221, about 0.45%', F(4, 52) * F(3, 51) == F(1, 221) and near(100 / 221, 0.45, 0.005))
u = np.sort(rng.random((N, 2)), axis=1)
p1, p2, p3 = u[:, 0], u[:, 1] - u[:, 0], 1 - u[:, 1]
tri = ((p1 < 0.5) & (p2 < 0.5) & (p3 < 0.5)).mean()
check('l13 s7 broken stick makes a triangle with chance 1/4', near(tri, 0.25, 0.004), '%.4f' % tri)
check('l13 s8 1 - 0.8^4 = 0.59', near(1 - 0.8 ** 4, 0.59, 0.005))
check('l13 s8 five rounds key 0.672', near(l13['screens'][8]['widget']['answer'], 1 - 0.8 ** 5, 0.0005))
check('l13 quiz2 key 0.271', near(l13['quiz'][2]['widget']['answer'], 1 - 0.9 ** 3, 0.0005))
p = l13['screens'][0]['widget']['points'][0]
check('l13 s0 key is the 10:30 to 11:15 round', p['target'] - p['tol'] == 10.5 and p['target'] + p['tol'] == 11.25)
check('l13 four 45-minute rounds end at 14:15', 13.5 + 0.75 == 14.25)

# ---- l14 ----
l14 = J('l14-offers-and-deadlines')
d0 = date(2027, 3, 2)
check('l14 s2 day 14 is 16 March, day 18 is 20 March',
      d0 + timedelta(14) == date(2027, 3, 16) and d0 + timedelta(18) == date(2027, 3, 20))
check('l14 s3 pay key 43,500', l14['screens'][3]['widget']['rows'][0][1]['answer'] == 4350 * 10)
check('l14 s9 60,000 x 9/52 key', near(l14['screens'][9]['widget']['answer'], 60000 * 9 / 52, 0.1))
check('l14 s11 29/55 key', near(l14['screens'][11]['widget']['answer'], 29 / 55, 0.0005))
check('l14 s11 slips 26/55 and 55/29', near(26 / 55, 0.473, 0.0005) and near(55 / 29, 1.897, 0.0005))
check('l14 quiz0 3 May to 13 May is ten days; 9 May leaves four', 13 - 3 == 10 and 13 - 9 == 4)
check('l14 quiz1 3,200 x 12 key', l14['quiz'][1]['widget']['answer'] == 3200 * 12)
check('l14 s5 ten weeks is 50 working days', 10 * 5 == 50)

# ---- l15 ----
l15 = J('l15-after-a-rejection')
mdiff = lambda y1, m1, y2, m2: (y2 - y1) * 12 + (m2 - m1)
check('l15 s3 Nov 2026 to Jul 2027 key 8', l15['screens'][3]['widget']['answer'] == mdiff(2026, 11, 2027, 7))
check('l15 s8 0.95^20 key 0.358', near(l15['screens'][8]['widget']['answer'], 0.95 ** 20, 0.0005))
check('l15 s8 0.9^20 = 0.12; cut of about two thirds',
      near(0.9 ** 20, 0.12, 0.005) and near(1 - 0.9 ** 20 / 0.95 ** 20, 2 / 3, 0.02))
check('l15 quiz1 Oct 2026 to Jul 2027 key 9', l15['quiz'][1]['widget']['answer'] == mdiff(2026, 10, 2027, 7))

# ---- review-3 ----
r3 = {i['id']: i for i in J('review-3')['items']}
check('review-3 18/24 key', r3['r3-return-rate']['widget']['answer'] == 18 / 24)
check('review-3 Dec 2026 to Jul 2027 key 7', r3['r3-months-retry']['widget']['answer'] == mdiff(2026, 12, 2027, 7))
check('review-3 1 - 0.75^3 key', near(r3['r3-bad-round']['widget']['answer'], 1 - 0.75 ** 3, 0.0005))
check('review-3 up to three rolls worth 14/3, above 3.5', v2 == F(14, 3) and v2 > v0)
check('review-3 tell-day: nine days from day 1, four from day 6', 10 - 1 == 9 and 10 - 6 == 4)

# ---- homework-3 ----
h3 = {i['id']: i for i in J('homework-3')['items']}
claims = {'hw3-story-project': (178, 82), 'hw3-story-failure': (150, 69), 'hw3-story-decision': (168, 78),
          'hw3-story-team': (155, 72), 'hw3-story-disagreement': (170, 78), 'hw3-story-pressure': (155, 72)}
for k, (w, s) in claims.items():
    n = len(h3[k]['widget']['model'].split('\n\n')[1].split())
    check('%s model is about %d words, about %d s' % (k, w, s), abs(n - w) <= 5 and near(w / WPM * 60, s, 1),
          'counted %d, %.1f s' % (n, w / WPM * 60))
check('hw3 failure story: module mark 0.25 x 52 + 0.75 x 71 = 66', near(0.25 * 52 + 0.75 * 71, 66, 0.5))
check('hw3 decision story: 100 x 30 = 3,000; 50 x 15 = 750; 100 x 15 = 1,500; 15% off 100 is 85',
      100 * 30 == 3000 and 50 * 15 == 750 and 100 * 15 == 1500 and 100 * 0.85 == 85)
check('hw3 reasoning: E = 1 + 2E/3 gives 3', near(rng.geometric(1 / 3, N).mean(), 3, 0.03))

print('\n%d failing' % len(fails))
sys.exit(1 if fails else 0)
