#!/usr/bin/env python3
"""Blind concept audit, number-sense problems-1 to problems-3 (chained problem sets).

Recomputes every graded key, every wrong[] slip and every wrong choice option in exact
fractions, independently of the author's number script, and checks that
  * the stored key equals the recomputed value (to the 6 d.p. the JSON stores),
  * every slip equals the value its named mistake gives,
  * no slip window touches the answer window (a slip can never be marked right, and no
    right answer can be caught by a slip), and no slip equals the key under a valid
    alternative convention listed in ALT,
  * every chained part uses the value its question tells the learner to carry forward,
  * each rule or comparison stated in feedback or an explanation holds (CLAIMS).
Nothing here is empirical, so there is no Monte Carlo. Exit 0 when the content is correct.
`--ledger <path>` writes the claim ledger from the same table.
"""
import json, math, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'number-sense')
D = lambda s: F(str(s))


def rnd(x, dp):
    """Round half up at dp decimal places, exactly."""
    q = F(10) ** dp
    return F(math.floor(x * q + F(1, 2)), 1) / q


def sf1(x):
    e = math.floor(math.log10(float(x)))
    return rnd(F(x) / F(10) ** e, 0) * F(10) ** e


# ---------- problems-1 ----------
beans = F(1, 4) * 20
pb = F(2, 5) + F(1, 4)
flowers = 1 - pb
roses = F(1, 2) * flowers
fifths = F(5, 6) / F(1, 5)
loaves = math.floor(fifths)
left = F(5, 6) - loaves * F(1, 5)
share_left = left / F(5, 6)
hour1 = F(3, 8) + F(1, 3)
rest = 1 - hour1
a_alone = rest / F(3, 8)
total_min = 60 + a_alone * 60
a36 = F(4, 9) * 36
cordA = F(4, 9) * F(3, 4)
cordB = F(5, 12) * F(3, 4)
cord = cordA + cordB
bowl = cord / F(3, 2)

P1 = {
    (0, 0): (beans, '1/4 of 20', {
        'flipped': (F(20) * 4, '20 x 4'),
        'three-quarters': (F(3, 4) * 20, '3/4 of 20')}),
    (0, 1): (pb, '2/5 + 1/4 = 8/20 + 5/20', {
        'tops-bottoms': (F(2 + 1, 5 + 4), '(2+1)/(5+4) = 3/9'),
        'tops-kept': (F(2, 20) + F(1, 20), '2/20 + 1/20')}),
    (0, 2): (1 - F(13, 20), '1 - 13/20 (carried value)', {
        'carried': (1 - F(3, 9), '1 - 3/9, the part 2 slip'),
        'beds': (flowers * 20, '7/20 of 20 beds')}),
    (0, 3): (F(1, 2) * F(7, 20), '1/2 x 7/20 (carried value)', {
        'doubled': (2 * F(7, 20), '2 x 7/20'),
        'added-half': (F(1, 2) + F(7, 20), '1/2 + 7/20'),
        'carried': (F(1, 2) * F(2, 3), '1/2 x 2/3, the carried slip')}),
    (1, 0): (fifths, '5/6 / 1/5 = 25/6', {
        'multiplied': (F(5, 6) * F(1, 5), '5/6 x 1/5'),
        'wrong-flip': (F(6, 5) * F(1, 5), '6/5 x 1/5')}),
    (1, 1): (F(math.floor(F(25, 6))), 'floor(4 1/6)', {
        'rounded-up': (F(math.ceil(F(25, 6))), 'ceil(4 1/6)'),
        'carried': (F(math.floor(F(1, 6))), 'floor(1/6); floor(6/25) is 0 too')}),
    (1, 2): (F(5, 6) - 4 * F(1, 5), '5/6 - 4/5 = 1/30', {
        'one-loaf': (F(5, 6) - F(1, 5), '5/6 - 1/5'),
        'tops-bottoms': (F(5 - 4, 6 - 5), '(5-4)/(6-5)'),
        'loaf-sixth': (fifths - loaves, 'fraction part of 4 1/6')}),
    (1, 3): (F(1, 30) / F(5, 6), '1/30 / 5/6 = 1/25', {
        'multiplied': (F(1, 30) * F(5, 6), '1/30 x 5/6'),
        'flipped': (F(5, 6) / F(1, 30), '5/6 / 1/30'),
        'carried': (F(19, 30) / F(5, 6), '19/30 / 5/6, the one-loaf slip')}),
    (2, 0): (hour1, '3/8 + 1/3 = 9/24 + 8/24', {
        'tops-bottoms': (F(3 + 1, 8 + 3), '(3+1)/(8+3)'),
        'multiplied': (F(3, 8) * F(1, 3), '3/8 x 1/3')}),
    (2, 1): (1 - F(17, 24), '1 - 17/24', {
        'carried': (1 - F(4, 11), '1 - 4/11, the part 1 slip'),
        'count': (rest * 24, 'number of twenty-fourths')}),
    (2, 2): (F(7, 24) / F(3, 8), '7/24 / 3/8 = 7/9 h', {
        'multiplied': (F(7, 24) * F(3, 8), '7/24 x 3/8'),
        'flipped': (F(3, 8) / F(7, 24), '3/8 / 7/24'),
        'printer-b': (F(7, 24) / F(1, 3), '7/24 / 1/3'),
        'minutes': (a_alone * 60, '7/9 h in minutes')}),
    (2, 3): (60 + F(7, 9) * 60, '60 + 7/9 x 60 = 320/3 min', {
        'rest-only': (F(7, 9) * 60, '7/9 x 60'),
        'hundred': (100 + F(7, 9) * 100, '100 + 7/9 x 100'),
        'carried-flipped': (60 + F(9, 7) * 60, '60 + 9/7 x 60'),
        'hours': (1 + F(7, 9), '1 7/9 h')}),
    (3, 0): (a36, '4/9 = 16/36', {
        'top-kept': (F(4), 'top left at 4'),
        'added': (F(4 + (36 - 9)), '4 + 27'),
        'whole-fraction': (F(16, 36), '16/36 typed whole')}),
    (3, 1): ('choice', 'a', {
        'b-top': (F(5, 12) < F(4, 9), '15/36 < 16/36, so B is weaker'),
        'same': (F(5, 12) != F(4, 9), '15/36 != 16/36')}),
    (3, 2): (cordA, '4/9 x 3/4 = 1/3 l', {
        'added': (F(4, 9) + F(3, 4), '4/9 + 3/4 = 43/36'),
        'divided': (F(4, 9) / F(3, 4), '4/9 / 3/4 = 16/27')}),
    (3, 3): (F(1, 3) + F(5, 16), '1/3 + 5/16 = 31/48 l', {
        'tops-bottoms': (F(1 + 5, 3 + 16), '(1+5)/(3+16)'),
        'carried': (F(43, 36) + F(5, 16), '43/36 + 5/16, the part 3 slip')}),
    (3, 4): (F(31, 48) / F(3, 2), '31/48 / 3/2 = 31/72', {
        'multiplied': (F(31, 48) * F(3, 2), '31/48 x 3/2'),
        'shares-added': (F(4, 9) + F(5, 12), '4/9 + 5/12 = 31/36')}),
}

# ---------- problems-2 ----------
t6, t14, t23 = D('-3.6'), D('-3.6') + D('4.9'), F(-5)
chg = t23 - D('1.3')
rate = D('-6.3') / 9
t3 = t23 + 4 * D('-0.7')
card = 4 * -1 + 1 * -2 + 3 * 1 + 1 * 2 + 9 * 0
week = [-1, 2, -6, -3]
share = F(17, 6)

P2 = {
    (0, 0): (t14, '-3.6 + 4.9', {
        'subtracted': (t6 - D('4.9'), '-3.6 - 4.9'),
        'start-sign': (D('3.6') + D('4.9'), '3.6 + 4.9')}),
    (0, 1): (chg, '-5 - 1.3 (end minus start)', {
        'sign': (-chg, 'size without the minus'),
        'added': (t23 + D('1.3'), '-5 + 1.3'),
        'carried': (t23 - D('-8.5'), '-5 - (-8.5), the part 1 slip')}),
    (0, 2): (rate, '-6.3 / 9', {
        'sign': (-rate, 'sign dropped'),
        'times': (D('-6.3') * 9, '-6.3 x 9')}),
    (0, 3): (t3, '-5 + 4 x (-0.7)', {
        'sign': (-t3, 'sign dropped'),
        'minus-minus': (t23 - 4 * D('-0.7'), '-5 - (-2.8)'),
        'change-only': (4 * D('-0.7'), '4 x (-0.7)')}),
    (1, 0): (F(card), '4(-1) + (-2) + 3(1) + 2', {
        'sign': (F(-card), 'sign flipped'),
        'eagle-one': (F(4 * -1 + -1 + 3 + 2), 'eagle counted as -1'),
        'no-signs': (F(4 + 2 + 3 + 2), 'sizes added')}),
    (1, 1): (F(sum(week), 4), '(-1 + 2 - 6 - 3) / 4', {
        'sign': (F(-sum(week), 4), 'sign dropped'),
        'plus-as-minus': (F(-1 - 2 - 6 - 3, 4), '+2 read as -2'),
        'total': (F(sum(week)), 'total, not shared')}),
    (1, 2): (rnd(F(5, 18), 3), '5/18 = 0.2777.. to 3 d.p.', {
        'unrounded': (rnd(F(5, 18), 6), '5/18 to 6 d.p.'),
        'truncated': (F(math.floor(F(5, 18) * 1000), 1000), 'cut at 3 d.p.'),
        'flipped': (F(18, 5), '18 / 5')}),
    (1, 3): ('choice', 'rival', {
        'golfer': (F(5, 18) < D('0.28'), '5/18 < 0.28 (gap 1/450)'),
        'same': (F(5, 18) != D('0.28'), '5/18 != 7/25')}),
    (2, 0): (rnd(share, 4), '17/6 to 4 d.p.', {
        'flipped': (rnd(F(6, 17), 4), '6/17 to 4 d.p.'),
        'remainder': (D('2.5'), '2 r 5 read as 2.5')}),
    (2, 1): (rnd(D('2.8333'), 2), '2.8333 to 2 d.p.', {
        'unrounded': (D('2.8333'), 'not rounded'),
        'rounded-up': (F(math.ceil(D('2.8333') * 100), 100), 'rounded up'),
        'one-dp': (rnd(D('2.8333'), 1), '1 d.p.'),
        'pence': (rnd(D('2.8333'), 2) * 100, 'in pence')}),
    (2, 2): (6 * 283 - F(1700), '6 x 283 - 1700 pence', {
        'sign': (1700 - F(6 * 283), 'fare minus collected'),
        'pounds': (6 * D('2.83') - 17, 'in pounds'),
        'carried-up': (F(6 * 284 - 1700), '6 x 284 - 1700, the 2.84 slip')}),
    (2, 3): (17 - 5 * D('2.83'), '17 - 5 x 2.83', {
        'same': (D('2.83'), 'a plain share'),
        'wrong-way': (D('2.83') - D('0.02'), '2.83 - 0.02'),
        'shortfall': (D('0.02'), 'the gap alone'),
        'pence': ((17 - 5 * D('2.83')) * 100, 'in pence')}),
}

# ---------- problems-3 ----------
N = 2169
edge = max(n for n in range(1, 50) if n ** 3 <= N)
paper = 38 * D('4.85')
bill = paper + D('19.50')
est = sf1(38) * sf1(D('4.85')) + sf1(D('19.50'))
hours = F(12, 10) * 10 ** 9 / (4 * 10 ** 4)

P3 = {
    (0, 0): (F(edge), 'largest n with n^3 <= 2169', {
        'rounded-up': (F(edge + 1), '13, but 13^3 = 2197 > 2169'),
        'square-root': (F(math.isqrt(N)), 'sqrt(2169) = 46.57; window 45 to 47'),
        'thirds': (F(N, 3), '2169 / 3')}),
    (0, 1): (F(N - 12 ** 3), '2169 - 1728', {
        'squared': (F(N - 12 ** 2), '2169 - 144'),
        'carried-up': (F(N - 13 ** 3), '2169 - 2197'),
        'times-three': (F(N - 12 * 3), '2169 - 36')}),
    (0, 2): (F(math.isqrt(441)), 'sqrt(441)', {
        'halved': (F(441, 2), '441 / 2'),
        'quartered': (F(441, 4), '441 / 4')}),
    (1, 0): (est, '40 x 5 + 20', {
        'bracket-first': (sf1(38) * (sf1(D('4.85')) + sf1(D('19.50'))), '40 x (5 + 20)'),
        'no-delivery': (sf1(38) * sf1(D('4.85')), '40 x 5')}),
    (1, 1): (bill, '38 x 4.85 + 19.50', {
        'bracket': (38 * (D('4.85') + D('19.50')), '38 x (4.85 + 19.50)'),
        'boxes-only': (paper, '38 x 4.85')}),
    (1, 2): (paper + D('19.50') / 3, '38 x 4.85 + (19.50 / 3)', {
        'intended': (rnd(bill / 3, 2), '(bill) / 3 to the penny'),
        'delivery-share': (D('19.50') / 3, '19.50 / 3')}),
    (1, 3): (rnd(D('203.80') / 3, 2), '203.80 / 3 to the penny', {
        'calculator': (paper + D('19.50') / 3, 'the part 3 display'),
        'carried-bracket': (rnd(D('925.30') / 3, 2), '925.30 / 3'),
        'estimate': (rnd(F(220, 3), 2), '220 / 3')}),
    (2, 0): (hours, '1.2e9 / 4e4', {
        'kept-point': (F(3 * 10 ** 5), '3 x 10^5'),
        'added-indices': (F(3, 10) * 10 ** 13, '0.3 x 10^(9+4)'),
        'short': (F(3 * 10 ** 3), '3 x 10^3')}),
    (2, 1): (sf1(24 * 365), '8760 to 1 s.f.', {
        'truncated': (F(8000), 'digits cut'),
        'two-sf': (F(8800), '2 s.f.')}),
    (2, 2): (sf1(F(30000, 9000)), '30000 / 9000 to 1 s.f.', {
        'inverted': (F(9000, 30000), '9000 / 30000'),
        'carried': (sf1(F(30000, 8000)), '30000 / 8000 = 3.75 to 1 s.f.'),
        'unrounded': (rnd(F(30000, 9000), 2), '3.33, not rounded')}),
    (2, 3): (rnd(F(30000, 8760), 1), '30000 / 8760 to 1 d.p.', {
        'nine-thousand': (rnd(F(30000, 9000), 1), '30000 / 9000'),
        'carried': (rnd(F(300000, 8760), 1), '300000 / 8760'),
        'days': (F(30000, 24), '30000 / 24')}),
}

# Valid alternative conventions: values a careful learner could defend. None may hit a slip,
# and each must land in the answer window (or be ruled out by the item's own wording).
ALT = {
    ('problems-2', 1, 2): [(F(math.floor(F(5, 18) * 1000 + F(1, 2)), 1000), 'half-even or half-up, same 0.278')],
    ('problems-2', 2, 3): [(D('2.83') + D('0.02'), 'share plus shortfall')],
    ('problems-3', 1, 0): [(sf1(sf1(38) * sf1(D('4.85'))) + sf1(D('19.50')), 'product rounded again')],
    ('problems-3', 1, 2): [(rnd(paper + D('19.50') / 3, 2), 'left to right gives the same, x before +')],
    ('problems-3', 2, 2): [(sf1(F(30000, 8760)), 'unrounded year, still 3'), (sf1(F(30000, 8800)), '2 s.f. year, still 3')],
    ('problems-3', 2, 3): [(rnd(F(30000, 24) / D('365.25'), 1), '365.25-day year, still 3.4')],
}

# Rules and comparisons stated in prose: (file, path, claim, holds, basis)
CLAIMS = [
    ('problems-1', 'items[0].parts[3].explain', '7/40 of 20 beds is three and a half beds', F(7, 40) * 20 == F(7, 2), '7/40 x 20'),
    ('problems-1', 'items[1].parts[0].explain', 'dividing by 1/5 is multiplying by 5', F(5, 6) / F(1, 5) == F(5, 6) * 5, 'reciprocal'),
    ('problems-1', 'items[1].parts[1].feedback.byKey.rounded-up', 'the flour left is a sixth of a loaf', left / F(1, 5) == F(1, 6), '1/30 / 1/5'),
    ('problems-1', 'items[1].parts[2].feedback.byKey.loaf-sixth', 'a sixth of 1/5 kg is 1/30 kg', F(1, 6) * F(1, 5) == F(1, 30), 'product'),
    ('problems-1', 'items[1].parts[3].explain', 'a fraction of the start is leftover divided by start', left / F(5, 6) == F(1, 25), 'definition of a share'),
    ('problems-1', 'items[2].parts[0].feedback.byKey.tops-bottoms', '4/11 is less than A prints alone', F(4, 11) < F(3, 8), '32/88 < 33/88'),
    ('problems-1', 'items[2].parts[1].explain', '7/24 is a little under a third', F(7, 24) < F(1, 3) and F(1, 3) - F(7, 24) == F(1, 24), '7/24 < 8/24'),
    ('problems-1', 'items[2].parts[2].explain', '7/24 is 7 of the 9 pieces A does in an hour', F(3, 8) == F(9, 24), '3/8 = 9/24'),
    ('problems-1', 'items[2].parts[3].feedback.correct', '7/9 of 60 min is 420/9 = 46 2/3', F(7, 9) * 60 == F(420, 9) == 46 + F(2, 3), 'exact'),
    ('problems-1', 'items[3].parts[1].widget.options[1].why', 'ninths are bigger than twelfths', F(1, 9) > F(1, 12), '1/9 > 1/12'),
    ('problems-1', 'items[3].parts[1].widget.options[2].why', 'both shares are under a half', F(4, 9) < F(1, 2) and F(5, 12) < F(1, 2), '16, 15 < 18 thirty-sixths'),
    ('problems-1', 'items[3].parts[2].explain', '1/3 is less than either fraction multiplied', cordA < F(4, 9) and cordA < F(3, 4), 'product of proper fractions'),
    ('problems-1', 'items[3].parts[3].question', '5/12 x 3/4 = 5/16', cordB == F(5, 16), '15/48'),
    ('problems-1', 'items[3].parts[3].feedback.byKey.tops-bottoms', '6/19 is less than jug A alone', F(6, 19) < F(1, 3), '18/57 < 19/57'),
    ('problems-1', 'items[3].parts[4].question', 'two 3/4 l jugs make 3/2 l', 2 * F(3, 4) == F(3, 2), 'sum'),
    ('problems-1', 'items[3].parts[4].feedback.byKey.shares-added', 'bowl share is half the sum of the shares (equal jugs)', bowl == (F(4, 9) + F(5, 12)) / 2, 'equal volumes, so the mean'),
    ('problems-1', 'items[3].parts[4].explain', 'the mix sits between the two jug shares', F(5, 12) < bowl < F(4, 9), '30/72 < 31/72 < 32/72'),
    ('problems-2', 'items[0].parts[0].explain', '3.6 up to zero, then 1.3 more', D('4.9') - D('3.6') == D('1.3'), 'number line'),
    ('problems-2', 'items[0].parts[1].question', '2 pm to 11 pm is 9 hours', 23 - 14 == 9, 'clock'),
    ('problems-2', 'items[0].parts[2].explain', 'negative divided by positive is negative', rate < 0, 'sign rule'),
    ('problems-2', 'items[0].parts[3].question', '4 hours after 11 pm is 3 am', (23 + 4) % 24 == 3, 'clock'),
    ('problems-2', 'items[1].prose', 'the card has 18 holes', 4 + 1 + 3 + 1 + 9 == 18, 'count'),
    ('problems-2', 'items[1].parts[0].feedback.byKey.sign', '6 shots under and 5 over', 4 * 1 + 2 == 6 and 3 + 2 == 5, 'count'),
    ('problems-2', 'items[1].parts[2].question', 'under par on 5 of 18 holes', 4 + 1 == 5, '4 birdies and 1 eagle'),
    ('problems-2', 'items[1].parts[3].widget.options[2].why', '0.2777.. is below 0.28 by about 0.002', rnd(D('0.28') - F(5, 18), 3) == D('0.002'), '1/450 = 0.00222'),
    ('problems-2', 'items[2].parts[0].explain', '17/6: 2 r 5, 50 -> 8 r 2, 20 -> 3 r 2 recurring', divmod(17, 6) == (2, 5) and divmod(50, 6) == (8, 2) and divmod(20, 6) == (3, 2), 'long division'),
    ('problems-2', 'items[2].parts[2].feedback.byKey.sign', 'six pay 16.98', 6 * D('2.83') == D('16.98'), 'product'),
    ('problems-2', 'items[2].parts[3].explain', '5 x 2.83 = 14.15 and 2.85 = 2.83 + 0.02', 5 * D('2.83') == D('14.15') and D('2.85') == D('2.83') + D('0.02'), 'exact'),
    ('problems-3', 'items[0].parts[0].explain', '12^3 = 1728 < 2169 < 2197 = 13^3', 12 ** 3 == 1728 and 13 ** 3 == 2197 and 1728 < N < 2197, 'cubes'),
    ('problems-3', 'items[0].parts[2].explain', '20^2 = 400, 22^2 = 484, 21^2 = 441', (400, 441, 484) == (20 ** 2, 21 ** 2, 22 ** 2), 'squares'),
    ('problems-3', 'items[1].parts[0].feedback.correct', '38 -> 40, 4.85 -> 5, 19.50 -> 20 at 1 s.f.', (sf1(38), sf1(D('4.85')), sf1(D('19.50'))) == (40, 5, 20), 'rounding'),
    ('problems-3', 'items[1].parts[1].feedback.correct', '38 x 4.85 = 184.30', paper == D('184.30'), 'product'),
    ('problems-3', 'items[1].parts[2].explain', 'x and / before +; a share is about 73', rnd(F(220, 3), 0) == 73, 'order of operations (stated convention)'),
    ('problems-3', 'items[1].parts[3].explain', '203.80 / 3 = 67.9333.., third decimal 3', math.floor(D('203.80') / 3 * 1000) % 10 == 3, 'division'),
    ('problems-3', 'items[2].parts[0].feedback.correct', '0.3 x 10^5 = 3 x 10^4; dividing powers subtracts indices', F(3, 10) * 10 ** 5 == 3 * 10 ** 4 and F(10 ** 9, 10 ** 4) == 10 ** 5, 'index law'),
    ('problems-3', 'items[2].parts[1].question', '24 x 365 = 8760', 24 * 365 == 8760, 'product; 365-day year stated'),
    ('problems-3', 'items[2].parts[3].explain', '3.42.. exceeds 3.33.. because 8760 < 9000', F(30000, 8760) > F(30000, 9000) > 3, 'smaller divisor, larger quotient'),
    ('problems-3', 'items[2].parts[3].feedback.byKey.days', '30000 / 24 = 1250 days', F(30000, 24) == 1250, 'division'),
]

# Findings: ledger rows whose verdict is not `correct` (see docs/reviews/audit-number-sense-problems-1-3.md).
FINDINGS = {
    ('problems-2', 'items[1].parts[3].question'): ('imprecise', 'finding 1: 0.28 of an 18-hole round is not a whole number of holes, and 5/18 is 0.28 to 2 d.p.'),
}
EXACT_FORM = [  # finding 2: "exact fraction" asked, 3 d.p. accepted, 2 d.p. sent to a method line
    ('problems-1', 1, 0), ('problems-1', 1, 2), ('problems-1', 2, 0), ('problems-1', 2, 1), ('problems-1', 2, 2),
    ('problems-1', 2, 3), ('problems-1', 3, 2), ('problems-1', 3, 3), ('problems-1', 3, 4)]


def main():
    fails, rows = [], []

    def row(f, path, claim, ok, basis, verdict=None):
        v = verdict or ('correct' if ok else 'wrong')
        rows.append((f, path, claim, v, basis))
        if not ok:
            fails.append(f'{f} {path}: {claim} [{basis}]')

    for name, spec in (('problems-1', P1), ('problems-2', P2), ('problems-3', P3)):
        data = json.load(open(os.path.join(COURSE, name + '.json')))
        seen = set()
        for i, it in enumerate(data['items']):
            for j, part in enumerate(it['parts']):
                w = part['widget']
                p = f'items[{i}].parts[{j}].widget'
                assert (i, j) in spec, f'{name} {p} not in the audit table'
                seen.add((i, j))
                want, basis, wrongs = spec[(i, j)]
                if w['kind'] == 'choice':
                    right = [o['id'] for o in w['options'] if o.get('correct')]
                    row(name, p + '.options (key)', f'correct option is {basis}', right == [basis], 'recomputed comparison')
                    others = {o['id'] for o in w['options'] if not o.get('correct')}
                    row(name, p + '.options (set)', 'every wrong option is in the audit table', others == set(wrongs), 'coverage')
                    for oid, (is_wrong, b) in wrongs.items():
                        row(name, f'{p}.options.{oid}', 'option is wrong under every reading', bool(is_wrong), b)
                    continue
                ans, tol = F(str(w['answer'])), F(str(w['tol']['abs']))
                key_ok = abs(ans - want) <= F(1, 10 ** 6)
                verdict = None
                if (name, i, j) in EXACT_FORM and key_ok:
                    verdict = 'imprecise'
                    basis += '; finding 2: exact form asked, window takes 3 d.p. and rejects 2 d.p.'
                row(name, p + '.answer', f'key {w["answer"]} = {want}', key_ok, basis, verdict)
                ids = {x['id'] for x in w.get('wrong', [])}
                row(name, p + '.wrong (set)', 'every slip is in the audit table', ids == set(wrongs), 'coverage')
                for x in w.get('wrong', []):
                    if x['id'] not in wrongs:
                        continue
                    val, b = wrongs[x['id']]
                    xv, xt = F(str(x['value'])), F(str(x['tol']['abs']))
                    hit = abs(xv - val) <= max(xt, F(1, 10 ** 6))
                    apart = abs(xv - want) > tol + xt
                    row(name, f'{p}.wrong.{x["id"]}', f'slip {x["value"]} is the named mistake ({val}) and never the key',
                        hit and apart, b)
                    bk = part['feedback'].get('byKey', {})
                    if x['id'] not in bk:
                        fails.append(f'{name} {p}: slip {x["id"]} has no feedback line')
                for alt, b in ALT.get((name, i, j), []):
                    in_key = abs(alt - ans) <= tol
                    in_slip = any(abs(alt - F(str(x['value']))) <= F(str(x['tol']['abs'])) for x in w.get('wrong', []))
                    row(name, p + '.answer (convention)', f'alternative {float(alt):g} is marked right, not caught by a slip',
                        in_key and not in_slip, b)
        assert seen == set(spec), f'{name}: audit table has parts the file lacks'

    for f, path, claim, ok, basis in CLAIMS:
        verdict, note = FINDINGS.get((f, path), (None, None))
        row(f, path, claim, bool(ok), basis)
    for (f, path), (verdict, note) in FINDINGS.items():
        rows.append((f, path, note, verdict, 'see audit file'))

    # Chain values quoted in later questions equal the value the earlier part keys.
    chain = [
        (pb, F(13, 20)), (flowers, F(7, 20)), (fifths, 4 + F(1, 6)), (F(loaves), F(4)), (left, F(1, 30)),
        (hour1, F(17, 24)), (rest, F(7, 24)), (a_alone, F(7, 9)), (a36, F(16)), (cordA, F(1, 3)), (cord, F(31, 48)),
        (t14, D('1.3')), (chg, D('-6.3')), (rate, D('-0.7')), (F(card), F(-1)), (rnd(share, 4), D('2.8333')),
        (rnd(share, 2), D('2.83')), (6 * 283 - F(1700), F(-2)), (F(edge), F(12)), (F(N - edge ** 3), F(441)),
        (bill, D('203.80')), (hours, F(30000)), (sf1(8760), F(9000)),
    ]
    for k, (got, quoted) in enumerate(chain):
        row('chain', f'carry[{k}]', f'value carried forward {quoted} equals the earlier key', got == quoted, 'recomputed')

    if '--ledger' in sys.argv:
        out = sys.argv[sys.argv.index('--ledger') + 1]
        counts = {}
        for r in rows:
            counts[r[3]] = counts.get(r[3], 0) + 1
        with open(out, 'w') as fh:
            fh.write('# Claim ledger: number-sense problems-1 to problems-3 (blind concept audit)\n\n')
            fh.write('Stage 0 depth: every graded key, wrong option and slip, each stated rule or comparison, and each value carried between parts. ')
            fh.write('Written by `docs/reports/number-sense-problems-concepts.py --ledger`; the basis column is the exact-fraction derivation the script asserts.\n\n')
            fh.write(f'Rows: {len(rows)}. ' + ', '.join(f'{k} {v}' for k, v in sorted(counts.items())) + '.\n\n')
            fh.write('| file | JSON path | claim | verdict | basis |\n|---|---|---|---|---|\n')
            for r in rows:
                fh.write('| ' + ' | '.join(str(c).replace('|', '/') for c in r) + ' |\n')
    print(f'rows {len(rows)}, failures {len(fails)}')
    for f in fails:
        print('FAIL', f)
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
