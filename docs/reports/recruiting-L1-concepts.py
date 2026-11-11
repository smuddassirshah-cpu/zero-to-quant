"""Concept audit, recruiting level 1 (l1 to l5, review-1, homework-1).
Recomputes every date count, pay figure and probability the level states,
reading graded keys from the content JSON where a key is involved.
Exits 0 when the content is right; a failing line is a finding in
docs/reviews/audit-recruiting-1-3.md.
Run: python3 docs/reports/recruiting-L1-concepts.py
"""
import json, os, sys
from datetime import date, timedelta

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
C = os.path.join(ROOT, 'app', 'content', 'courses', 'recruiting')
J = lambda n: json.load(open(os.path.join(C, n + '.json')))
fails = []


def check(name, ok, detail=''):
    print(('ok   ' if ok else 'FAIL ') + name + (' | ' + detail if detail else ''))
    if not ok:
        fails.append(name)


def near(a, b, tol):
    return abs(a - b) <= tol


def add_months(d, m):
    y, mo = divmod(d.month - 1 + m, 12)
    return date(d.year + y, mo + 1, d.day)


TODAY = date(2026, 11, 2)  # the date the level states as "today"
days = lambda d: (d - TODAY).days

# ---- l2: pay ----
l2 = J('l2-kinds-of-firm')
check('l2 s2 4350 x 10 = key', l2['screens'][2]['widget']['answer'] == 4350 * 10)
check('l2 s3 65000 x 10/52 = key', near(l2['screens'][3]['widget']['answer'], 65000 * 10 / 52, 0.5))
check('l2 s3 slip 10 months', near(65000 * 10 / 12, 54166.67, 0.01))
m = 120 / 52
check('l2 s8 10 weeks = 2.31 months', near(m, 2.31, 0.005))
check('l2 s8 range 23,077 to 32,308', near(10000 * m, 23077, 1) and near(14000 * m, 32308, 1))
check('l2 s4 70-80% leaves 20-30%, about 1 in 4', 0.20 <= 0.25 <= 0.30)
check('l2 quiz0 4000 x 9', l2['quiz'][0]['widget']['answer'] == 36000)
check('l2 quiz1 60000 x 10/52', near(l2['quiz'][1]['widget']['answer'], 60000 * 10 / 52, 1))

# ---- l3: calendar ----
l3 = J('l3-the-calendar')
rows = l3['screens'][4]['widget']['rows']
check('l3 s4 8 Nov is 6 days', days(date(2026, 11, 8)) == 6)
check('l3 s4 15 Nov is 13 days', days(date(2026, 11, 15)) == 13)
check('l3 s4 6 Dec key', rows[3][2]['answer'] == days(date(2026, 12, 6)), str(days(date(2026, 12, 6))))
check('l3 s4 3 Jan key', rows[4][2]['answer'] == days(date(2027, 1, 3)), str(days(date(2027, 1, 3))))
d241 = days(date(2027, 7, 1))
check('l3 s10 2 Nov to 1 Jul 2027 is 241 days', d241 == 241)
check('l3 s10 full weeks key', l3['screens'][10]['widget']['answer'] == d241 // 7 and d241 % 7 == 3)
check('l3 s10 2 Nov + 238 d = 28 Jun 2027', TODAY + timedelta(238) == date(2027, 6, 28))
check('l3 s10 slip from 29 Oct is 35 weeks', (date(2027, 7, 1) - date(2026, 10, 29)).days == 245)
check('l3 quiz0 1 Dec key', l3['quiz'][0]['widget']['answer'] == days(date(2026, 12, 1)))
# month axis: month 0 = July 2026
mi = lambda y, mth: (y - 2026) * 12 + (mth - 7)
pts = l3['screens'][0]['widget']['points']
check('l3 s0 apply target = July 2027', pts[0]['target'] == mi(2027, 7))
check('l3 s0 offers key inside late Oct to mid Dec 2027',
      pts[3]['target'] - pts[3]['tol'] >= mi(2027, 10) and pts[3]['target'] + pts[3]['tol'] <= mi(2027, 12) + 0.5)
check('l3 s0 internship key = Jun to Aug 2028',
      pts[4]['target'] - pts[4]['tol'] == mi(2028, 6) and pts[4]['target'] + pts[4]['tol'] == mi(2028, 8))
check('l3 s9 key = July 2027', l3['screens'][9]['widget']['points'][0]['target'] == mi(2027, 7))
# stated programme dates: weekday sanity (a note, not a failure: the dates are reported)
for a, b, lab in [(date(2026, 3, 23), date(2026, 3, 27), 'New York run'), (date(2026, 4, 7), date(2026, 4, 11), 'London run')]:
    print('note l3 s8 %s %s to %s: %s to %s' % (lab, a, b, a.strftime('%A'), b.strftime('%A')))

# ---- l4: retake rule ----
check('l4 quiz1 1 Dec 2026 + 8 months = 1 Aug 2027', add_months(date(2026, 12, 1), 8) == date(2027, 8, 1))

# ---- l5: spread ----
l5 = J('l5-a-target-list')
check('l5 s3 0.95^30 key', near(l5['screens'][3]['widget']['answer'], 0.95 ** 30, 0.01), '%.4f' % 0.95 ** 30)
check('l5 s3 0.95^15 = 0.4633', near(0.95 ** 15, 0.4633, 0.0001))
check('l5 s7 np = 1.5 and 0.75', l5['screens'][7]['widget']['answer'] == 30 * 0.05 and 15 * 0.05 == 0.75)
check('l5 quiz1 0.9^10 key', near(l5['quiz'][1]['widget']['answer'], 0.9 ** 10, 0.01), '%.4f' % 0.9 ** 10)
check('l5 s1 14 days on is 16 Nov', TODAY + timedelta(14) == date(2026, 11, 16))
# linked failures raise P(no offer): one shared pass/fail factor
import random
random.seed(7)
N = 200000
none_ind = sum(all(random.random() > 0.05 for _ in range(30)) for _ in range(N // 10)) / (N // 10)
none_link = 0
for _ in range(N // 10):
    weak = random.random() < 0.5            # half the candidates carry a weakness
    p = 0.0 if weak else 0.10               # average p stays 0.05
    none_link += all(random.random() > p for _ in range(30))
none_link /= (N // 10)
check('l5 s5 linked failures give a higher chance of no offer', none_link > none_ind + 0.1,
      'independent %.3f, linked %.3f' % (none_ind, none_link))

# ---- review-1 ----
r1 = J('review-1')
it = {i['id']: i for i in r1['items']}
check('review-1 pay key', it['r3-pay']['widget']['answer'] == 30000)
check('review-1 days key', it['r5-days']['widget']['answer'] == days(date(2026, 11, 15)))
check('review-1 0.9^20 key', near(it['r7-spread']['widget']['answer'], 0.9 ** 20, 0.005), '%.4f' % 0.9 ** 20)
p = it['r4-spring']['widget']['points'][0]
lo, hi = p['target'] - p['tol'], p['target'] + p['tol']
check('review-1 r4-spring key accepts all of March and April 2027 (months 8 to 10)',
      lo <= mi(2027, 3) and hi >= mi(2027, 5), 'accepts %.2f to %.2f' % (lo, hi))

# ---- homework-1 ----
h1 = J('homework-1')
it = {i['id']: i for i in h1['items']}
check('hw1 15 Jul 2027 + 8 months = 15 Mar 2028', add_months(date(2027, 7, 15), 8) == date(2028, 3, 15))
check('hw1 0.92^25 key', near(it['hw1-spread']['widget']['answer'], 0.92 ** 25, 0.002), '%.4f' % 0.92 ** 25)
d = days(date(2027, 6, 28))
check('hw1 28 Jun 2027 key', it['hw1-imc-days']['widget']['answer'] == d and d == 7 * 34, str(d))

print('\n%d failing' % len(fails))
sys.exit(1 if fails else 0)
