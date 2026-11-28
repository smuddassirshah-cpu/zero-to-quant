"""Recompute every number stated in ai-use level 3 (l9 to l12, review-3, homework-3, problems-3), each two ways,
and check it appears in the JSON where it is stated (app/tools/numbers_lib.py).
Method A divides counts as floats; method B uses exact fractions and counts the toy tables' rows or days one by one.
The transcripts, settings pages and messages of this level hold invented figures (30 days, £49.99, £250,000) that
are data, not results, so nothing is computed from them.
Run from the repository root: python3 docs/reports/ai-use-L3-numbers.py   (exits 0 when every check passes)
"""
import os, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level('ai-use', 3)


def rate(k, n, label):
    a, b = k / n, F(k, n)
    lv.claim(abs(a - float(b)) < 1e-12, f'{label}: {k}/{n} = {float(b)} (float and exact)')
    return b


def points(r1, r2, label):
    """Gap in percentage points, by subtraction of exact rates and by counting hundredths."""
    gap = (r1 - r2) * 100
    gap_b = F(round(r1 * 10000) - round(r2 * 10000), 100)
    lv.claim(gap == gap_b, f'{label}: gap {float(gap)} points both ways')
    return float(gap)


# ---------------- l10 ----------------
rows = lv.files['l10-bias-from-data']['screens'][0]['canvas']['params']['rows']
lv.claim(sum(1 for r in rows if r[1] == 'A') == 9 and len(rows) == 10, 'l10 hook: 9 of 10 past hires from Group A')
pa, pb = rate(30, 100, 'past A'), rate(10, 100, 'past B')
ma, mb = rate(33, 100, 'model A'), rate(9, 100, 'model B')
fr = lv.files['l10-bias-from-data']['screens'][1]['canvas']['controls'][0]['frames']
lv.claim(fr[0]['values'] == {'ga': float(pa), 'gb': float(pb)} and fr[1]['values'] == {'ga': float(ma), 'gb': float(mb)}, 'l10 explore frames match the toy table rates')
g_model, g_past = points(ma, mb, 'model'), points(pa, pb, 'past')
lv.expect('l10', 'screens[2].widget.answer', g_model)
lv.expect('l10', 'screens[2].widget.wrong[0].value', g_past)
lv.expect('l10', 'screens[2].widget.wrong[1].value', round(33 / 9, 2))
lv.expect('l10', 'screens[2].widget.wrong[2].value', 33 + 9)
lv.expect('l10', 'screens[2].explain.text', 24); lv.expect('l10', 'screens[2].explain.text', 20)
lv.expect('l10', 'screens[1].explain.text', 33); lv.expect('l10', 'screens[1].explain.text', 9)
ta, tb = rate(140, 200, 'lender A'), rate(104, 200, 'lender B')
lv.claim(ta == F(7, 10) and tb == F(52, 100), 'lender rates 70% and 52%')
lv.expect('l10', 'screens[9].widget.answer', points(ta, tb, 'lender'))
lv.expect('l10', 'screens[9].widget.wrong[0].value', 140 - 104)
lv.expect('l10', 'screens[9].widget.wrong[1].value', round(140 / 104, 2))
lv.expect('l10', 'screens[9].widget.wrong[2].value', float(ta - tb))
lv.expect('l10', 'screens[9].explain.text', 70); lv.expect('l10', 'screens[9].explain.text', 52)
qa, qb = rate(45, 150, 'quiz A'), rate(15, 100, 'quiz B')
lv.expect('l10', 'quiz[1].widget.answer', points(qa, qb, 'quiz'))
lv.expect('l10', 'quiz[1].widget.wrong[0].value', 45 - 15)
lv.expect('l10', 'quiz[1].widget.wrong[1].value', float(qa / qb))

# ---------------- l12 ----------------
pnl = [lv.files['l12-what-alignment-means']['screens'][8]['canvas']['state']['values'][str(d)] for d in range(1, 21)]
tot_a = sum(pnl); tot_b = 0
for v in pnl:
    tot_b += v
lv.claim(tot_a == tot_b == 19 * 2 - 60 == -22 and sum(1 for v in pnl if v > 0) == 19, 'l12: 19 days of +2 and one of -60 total -22')
lv.expect('l12', 'screens[8].widget.answer', -22)
lv.expect('l12', 'screens[8].widget.wrong[0].value', 19 * 2)
lv.expect('l12', 'screens[8].widget.wrong[1].value', 22)
lv.expect('l12', 'screens[8].widget.wrong[2].value', 20 * 2)
lv.expect('l12', 'screens[8].explain.text', 38); lv.expect('l12', 'screens[8].explain.text', 60)

# ---------------- review-3 ----------------
r5a, r5b = rate(54, 120, 'r5 A'), rate(18, 80, 'r5 B')
lv.claim(r5a == F(45, 100) and r5b == F(225, 1000), 'r5 rates 45% and 22.5%')
lv.expect('review', 'items[4].widget.answer', points(r5a, r5b, 'r5'))
lv.expect('review', 'items[4].widget.wrong[0].value', 54 - 18)
lv.expect('review', 'items[4].widget.wrong[1].value', float(r5a / r5b))

# ---------------- homework-3 ----------------
h6a, h6b = rate(168, 240, 'h6 A'), rate(99, 180, 'h6 B')
lv.claim(h6a == F(70, 100) and h6b == F(55, 100), 'h6 rates 70% and 55%')
lv.expect('homework', 'items[5].widget.answer', points(h6a, h6b, 'h6'))
lv.expect('homework', 'items[5].widget.wrong[0].value', 168 - 99)
lv.expect('homework', 'items[5].widget.wrong[1].value', round(float(h6a / h6b), 2))

# ---------------- problems-3 ----------------
c, d = rate(56, 160, 'p1 C'), rate(6, 40, 'p1 D')
lv.expect('problems', 'items[0].parts[0].widget.answer', float(c))
lv.expect('problems', 'items[0].parts[0].widget.wrong[0].value', float(rate(56, 200, 'C over all 200')))
lv.expect('problems', 'items[0].parts[0].widget.wrong[1].value', 0.56)
lv.expect('problems', 'items[0].parts[1].widget.answer', float(d))
lv.expect('problems', 'items[0].parts[1].widget.wrong[0].value', float(rate(6, 200, 'D over all 200')))
lv.expect('problems', 'items[0].parts[1].widget.wrong[1].value', 0.06)
g1 = points(c, d, 'p1')
lv.expect('problems', 'items[0].parts[2].widget.answer', g1)
lv.expect('problems', 'items[0].parts[2].widget.wrong[0].value', 56 - 6)
lv.expect('problems', 'items[0].parts[2].widget.wrong[1].value', round(float(c / d), 2))
lv.claim(160 + 40 == 200, 'p1: 200 applicants in all')
d2 = rate(13, 40, 'p2 D after retraining')
lv.expect('problems', 'items[1].parts[0].widget.answer', float(d2))
lv.expect('problems', 'items[1].parts[0].widget.wrong[1].value', float(d))
g2 = points(c, d2, 'p2')
lv.claim(g2 == 2.5 and g1 == 20, 'gap falls from 20 to 2.5 points')
lv.expect('problems', 'items[1].parts[1].widget.answer', g2)
lv.expect('problems', 'items[1].parts[1].widget.wrong[0].value', g1)
lv.expect('problems', 'items[1].parts[1].widget.wrong[1].value', 56 - 13)
lv.expect('problems', 'items[1].prose', 35)
# the qualified pool: 40% of each group meet the requirements, and every shortlist sits inside it
qc, qd = F(40, 100) * 160, F(40, 100) * 40
lv.claim(qc == 64 == 0.4 * 160 and qd == 16 == 0.4 * 40, 'p1/p2: 40% of 160 is 64 and 40% of 40 is 16 meet the requirements')
lv.claim(56 <= qc and 6 <= qd and 13 <= qd, 'p1/p2: 56 of 64 (C), 6 and 13 of 16 (D): no shortlist exceeds those who meet the requirements')
lv.claim(F(13, 40) < F(40, 100) and F(56, 160) < F(40, 100) and F(6, 40) < F(40, 100), 'p2: every shortlist rate (35%, 32.5%, 15%) is below the 40% who meet the requirements')
lv.expect('problems', 'items[0].canvas.params.rows[1]', '40%')
lv.claim_text('problems', 'items[0].canvas.params.rows[1]', '25%', False, 'p1: the old 25% cell (below the shortlist counts) is gone')

lv.check_wrongs()
lv.report()
