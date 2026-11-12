"""Numbers stated inside the behavioural model answers of behavioural-5 to -8, recomputed. Exit 0 when all hold."""
from fractions import Fraction as F
from math import sqrt
ok = True
def chk(name, cond):
    global ok; ok = ok and cond; print('ok  ' if cond else 'FAIL', name)
def run_prob(n, k, p):
    st = [1.0] + [0.0] * k
    for _ in range(n):
        nw = [0.0] * (k + 1)
        for r in range(k): nw[0] += st[r] * (1 - p); nw[r + 1] += st[r] * p
        nw[k] += st[k]; st = nw
    return st[k]
chk('b6 five-losses: 0.45^5 is about 1.8 per cent (%.4f)' % 0.45 ** 5, abs(0.45 ** 5 - 0.018) < 0.0006)
chk('b6 five-losses: a run of five losses in 40 trades in about one game in three (%.3f)' % run_prob(40, 5, 0.45), abs(run_prob(40, 5, 0.45) - 1 / 3) < 0.03)
chk('b6 too-good (dropout story): standard error of 83 per cent over 400 students is about 2 points (%.4f)' % sqrt(0.83 * 0.17 / 400), abs(sqrt(0.83 * 0.17 / 400) - 0.02) < 0.002)
chk('b6 too-good: edges 91-80 = 11 points before, 84-80 = 4 after; 3 points are 1.5 standard errors of 2', 91 - 80 == 11 and 84 - 80 == 4 and abs(3 / 2 - 1.5) < 1e-9)
chk('b6 too-much-to-do: placed fourth of eleven, 30 hours against 42 (no arithmetic to check)', True)
chk('b7 are-you-sure: E = 1 + (5/6)E gives 6', 1 / (1 - F(5, 6)) == 6)
chk('b7 chose-to-stop: 3 weeks + 8 working days (23 days sunk) + "the last three weeks" fits an eight-week placement (7.6 weeks)', 3 * 5 + 8 == 23 and 3 + 8 / 5 + 3 <= 8)   # fix pass: eight weeks, 23 working days
chk('b8 coin: five heads 1/32; 64 sequences of six, two start with five heads', F(1, 2) ** 5 == F(1, 32) and 2 ** 6 == 64)
chk('b8 earlier-answer: three heads in a row takes 14 flips on average', 2 + 4 + 8 == 14)
chk('b8 dull-task: twenty sheets on each of three Fridays is sixty', 20 * 3 == 60)
chk('b8 one-number: 3.1 against 4.6 is about a third less error (%.3f)' % (1 - 3.1 / 4.6), abs((1 - 3.1 / 4.6) - 1 / 3) < 0.02)
chk('b5 teach: low to the north gives westerlies on its southern side; low to the south gives easterlies (anticlockwise, northern hemisphere)', True)
raise SystemExit(0 if ok else 1)
