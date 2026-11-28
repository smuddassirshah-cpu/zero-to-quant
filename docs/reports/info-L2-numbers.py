"""info level 2 (cross-entropy, KL, perplexity, likelihood): every stated number computed twice and found in the JSON.
Method A uses math.log2 sums; method B uses natural logs divided by ln 2, or the identity CE = H + KL, or a grid search.
Code widgets: each solution is run in CPython on its hidden tests (and each starter must fail one).
Run: <venv>/bin/python docs/reports/info-L2-numbers.py"""
import sys, os, math, json, shutil, tempfile, contextlib, io
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import Level

APP = os.path.join(HERE, '..', '..', 'app')
lv = Level('info', 2)
L2, LN2, ln = math.log2, math.log(2), math.log


def two(a, b, places, label):
    ok = round(a, places) == round(b, places)
    lv.claim(ok, f'{label}: {a!r} and {b!r} agree to {places} places')
    return round(a, places)


def H(p):
    return -sum(x * L2(x) for x in p if x > 0)


def Hn(p):                                   # B: natural logs, in bits
    return -sum(x * ln(x) for x in p if x > 0) / LN2


def CE(p, q):
    return -sum(a * L2(b) for a, b in zip(p, q) if a > 0)


def CEn(p, q):
    return -sum(a * ln(b) for a, b in zip(p, q) if a > 0) / LN2


def KL(p, q):                                # A: the direct sum
    return sum(a * L2(a / b) for a, b in zip(p, q) if a > 0)


def KLb(p, q):                               # B: cross-entropy minus entropy
    return CEn(p, q) - Hn(p)


E = lambda f, path, v: lv.expect(f, path, v)

# ---------------- l5 ----------------
P4, U4, R4 = [.5, .25, .125, .125], [.25] * 4, [.125, .125, .25, .5]
E('l5', 'screens[0].widget.answer', two(CE(U4, P4), sum([1, 2, 3, 3]) / 4, 3, 'old code in new town'))
E('l5', 'screens[1].widget.options', two(CE(P4, R4), CEn(P4, R4), 3, 'reversed model'))
E('l5', 'screens[1].canvas.controls[0].frames[2].caption', two(CE(P4, R4), CEn(P4, R4), 3, 'reversed caption'))
E('l5', 'screens[2].widget.answer', two(CE(P4, U4), L2(4), 3, 'p coded equal'))
E('l5', 'screens[2].widget.wrong[1].value', two(CE(U4, P4), CEn(U4, P4), 3, 'swapped'))
E('l5', 'screens[2].widget.wrong[2].value', two(CE(P4, U4) * LN2, 2 * LN2, 3, 'nats'))
T, M = [.7, .2, .1], [.5, .3, .2]
for i, (p, q) in enumerate(zip(T, M)):
    E('l5', f'screens[3].widget.rows[{i}][3]', two(-L2(q), -ln(q) / LN2, 3 if q != .5 else 0, f'length {q}'))
E('l5', 'screens[3].widget.rows[1][4].answer', two(.2 * -L2(.3), -.2 * ln(.3) / LN2, 3, 'rain term'))
E('l5', 'screens[3].widget.rows[1][4].wrong[0].value', two(.3 * -L2(.3), -.3 * ln(.3) / LN2, 3, 'rain q-weight'))
E('l5', 'screens[3].widget.rows[2][4].answer', two(.1 * -L2(.2), -.1 * ln(.2) / LN2, 3, 'snow term'))
E('l5', 'screens[3].widget.rows[2][4].wrong[0].value', two(.2 * -L2(.2), -.2 * ln(.2) / LN2, 3, 'snow q-weight'))
E('l5', 'screens[3].widget.rows[3][4].answer', two(CE(T, M), CEn(T, M), 3, 'weather CE'))
E('l5', 'screens[3].widget.rows[3][4].wrong[0].value', two(H(T), Hn(T), 3, 'weather H'))
E('l5', 'screens[4].widget.answer', two(KL(T, M), KLb(T, M), 3, 'weather KL'))
E('l5', 'screens[4].widget.wrong[2].value', two(KL(T, M) * LN2, sum(a * ln(a / b) for a, b in zip(T, M)), 3, 'weather KL nats'))
E('l5', 'screens[4].explain.text', two(CE(T, M), CEn(T, M), 4, 'CE 4dp'))
E('l5', 'screens[4].explain.text', two(H(T), Hn(T), 4, 'H 4dp'))
E('l5', 'screens[4].explain.text', two(KL(T, M) * 24 * 365, KLb(T, M) * 8760, 0, 'a year of hourly reports'))
E('l5', 'screens[5].prose', two(CE(M, T), CEn(M, T), 3, 'swapped weather'))
E('l5', 'screens[5].prose', two(CE(T, M) * LN2, -sum(a * ln(b) for a, b in zip(T, M)), 3, 'weather CE nats'))
RT, RB = [.9, .09, .01], [.95, .049, .001]
E('l5', 'screens[9].widget.answer', two(CE(RT, RB), CEn(RT, RB), 3, 'risk B CE'))
E('l5', 'screens[9].widget.wrong[0].value', two(H(RT), Hn(RT), 3, 'risk H'))
E('l5', 'screens[9].widget.wrong[1].value', two(CE(RT, RB) * LN2, -sum(a * ln(b) for a, b in zip(RT, RB)), 3, 'risk nats'))
E('l5', 'screens[9].widget.wrong[2].value', two(CE(RB, RT), CEn(RB, RT), 3, 'risk swapped'))
for q in RB:
    E('l5', 'screens[9].explain.text', two(-L2(q), -ln(q) / LN2, 3, f'risk length {q}'))
lv.claim(round(.01 * -L2(.001), 1) == 0.1, 'crash term about 0.1 bits')
E('l5', 'quiz[0].widget.answer', two(CE([.5, .5], [.25, .75]), CEn([.5, .5], [.25, .75]), 3, 'quiz CE'))
E('l5', 'quiz[0].widget.wrong[1].value', two(CE([.5, .5], [.25, .75]) * LN2, -(.5 * ln(.25) + .5 * ln(.75)), 3, 'quiz CE nats'))
E('l5', 'quiz[2].widget.options', two(CE([.5, .5], [.8, .2]), CEn([.5, .5], [.8, .2]), 3, 'H(q, p) order'))

# ---------------- l6 ----------------
for q, cap in [([1 / 3] * 3, 0), ([.5, .3, .2], 1), ([.8, .15, .05], 2), ([.6, .25, .15], 3)]:
    E('l6', f'screens[0].canvas.controls[0].frames[{cap}].caption', two(KL(T, q), KLb(T, q), 3, f'extra bits {q}'))
E('l6', 'screens[1].widget.rows[0][3]', two(.7 * L2(.7 / .5), .7 * ln(1.4) / LN2, 3, 'dry term'))
E('l6', 'screens[1].widget.rows[1][3].answer', two(.2 * L2(.2 / .3), .2 * ln(2 / 3) / LN2, 3, 'rain term'))
E('l6', 'screens[1].widget.rows[2][3].answer', two(.1 * L2(.1 / .2), -.1, 3, 'snow term'))
E('l6', 'screens[1].widget.rows[3][3].answer', two(KL(T, M), KLb(T, M), 3, 'KL table total'))
E('l6', 'screens[1].widget.rows[3][3].wrong[0].value', two(abs(.7 * L2(1.4)) + abs(.2 * L2(2 / 3)) + abs(.1 * L2(.5)), .340 + .117 + .1, 3, 'abs sum'))
a, b = [.9, .1], [.5, .5]
E('l6', 'screens[4].widget.answer', two(KL(a, b), KLb(a, b), 3, 'D(a||b)'))
E('l6', 'screens[4].widget.wrong[2].value', two(H(a), Hn(a), 3, 'H(a)'))
E('l6', 'screens[4].feedback.correct', two(L2(1.8), ln(1.8) / LN2, 3, 'log2 1.8'))
E('l6', 'screens[5].widget.answer', two(KL(b, a), KLb(b, a), 3, 'D(b||a)'))
E('l6', 'screens[5].widget.wrong[1].value', two(KL(b, a) * LN2, sum(x * ln(x / y) for x, y in zip(b, a)), 3, 'D(b||a) nats'))
E('l6', 'screens[5].widget.wrong[2].value', two(CE(b, a), CEn(b, a), 3, 'H(b, a)'))
E('l6', 'screens[6].widget.answer', two(KL(a, b) * LN2, .9 * ln(1.8) + .1 * ln(.2), 3, 'D(a||b) nats'))
E('l6', 'screens[6].widget.wrong[0].value', two(KL(a, b) / LN2, KLb(a, b) / LN2, 3, 'divided'))
E('l6', 'screens[6].explain.text', two(.9 * ln(1.8), .9 * (ln(9) - ln(5)), 3, '0.9 ln 1.8'))
E('l6', 'screens[6].explain.text', two(-.1 * ln(.2), .1 * ln(5), 3, '0.1 ln 5'))
E('l6', 'screens[7].prose', two(KL(P4, U4), KLb(P4, U4), 2, 'D(p||u)'))
lv.claim(abs(KL(P4, U4) - KL(U4, P4)) < 1e-12, 'the coincidence pair gives 0.25 both ways')
E('l6', 'screens[8].widget.options', two(KL([.5, .5, 0], [.25, .25, .5]), KLb([.5, .5, 0], [.25, .25, .5]), 0, 'edge D(p||q)'))
RL, MO = [.15, .35, .35, .15], [.1, .4, .4, .1]
E('l6', 'screens[10].widget.answer', two(KL(RL, MO), KLb(RL, MO), 3, 'buckets KL'))
E('l6', 'screens[10].widget.wrong[0].value', two(KL(MO, RL), KLb(MO, RL), 3, 'buckets reversed'))
E('l6', 'screens[10].widget.wrong[1].value', two(KL(RL, MO) * LN2, sum(x * ln(x / y) for x, y in zip(RL, MO)), 3, 'buckets nats'))
E('l6', 'screens[10].explain.text', two(250 * KL(RL, MO), 250 * KLb(RL, MO), 0, '250 days'))
E('l6', 'quiz[0].widget.answer', two(KL([.5, .5], [.25, .75]), KLb([.5, .5], [.25, .75]), 3, 'quiz KL'))
E('l6', 'quiz[2].widget.answer', two(.2 * LN2, .2 / (1 / LN2), 3, '0.2 bits in nats'))

# ---------------- l7 ----------------
E('l7', 'screens[0].prose', two(L2(6), ln(6) / LN2, 3, 'log2 6'))
E('l7', 'screens[2].widget.answer', two(math.exp(2.4), 2 ** (2.4 / LN2), 2, 'e^2.4'))
E('l7', 'screens[2].widget.wrong[0].value', two(2 ** 2.4, math.exp(2.4 * LN2), 2, '2^2.4'))
E('l7', 'screens[2].explain.text', two(2.4 / LN2, 2.4 * 1.4427, 3, '2.4 nats in bits'))
E('l7', 'screens[3].widget.answer', two(math.exp(2.4546), 2 ** (2.4546 / LN2), 2, 'bigram perplexity'))
E('l7', 'screens[3].widget.wrong[0].value', two(2 ** 2.4546, math.exp(2.4546 * LN2), 2, '2^2.4546'))
E('l7', 'screens[3].widget.wrong[1].value', two(2.4546 / LN2, 2.4546 * 1.4426950408889634, 2, 'bigram bits'))
E('l7', 'screens[4].widget.rows[0][2].answer', two(1 / LN2, L2(math.e), 3, 'bits per nat'))
E('l7', 'screens[4].widget.rows[0][2].wrong[0].value', two(LN2, 1 / L2(math.e), 3, 'ln 2'))
E('l7', 'screens[4].widget.rows[0][3]', two(math.e, 2 ** (1 / LN2), 3, 'e'))
E('l7', 'screens[4].widget.rows[1][1].answer', two(3 * LN2, ln(8), 3, '3 bits in nats'))
E('l7', 'screens[4].widget.rows[1][1].wrong[0].value', two(3 / LN2, 3 * L2(math.e), 3, '3 divided'))
E('l7', 'screens[4].widget.rows[1][3].wrong[0].value', two(math.exp(3), 2 ** (3 / LN2), 2, 'e^3'))
E('l7', 'screens[4].widget.rows[2][2]', two(2.4546 / LN2, 2.4546 * 1.4426950408889634, 3, 'row C bits'))
E('l7', 'screens[9].widget.answer', two(ln(11.6) - ln(8.7), ln(11.6 / 8.7), 2, 'fall in nats'))
E('l7', 'screens[9].widget.wrong[0].value', two(11.6 / 8.7, 4 / 3, 2, 'ratio'))
E('l7', 'screens[9].widget.wrong[1].value', two(L2(11.6 / 8.7), ln(11.6 / 8.7) / LN2, 2, 'fall in bits'))
E('l7', 'screens[9].feedback.correct', two(ln(11.6), ln(116) - ln(10), 3, 'ln 11.6'))
E('l7', 'screens[9].feedback.correct', two(ln(8.7), ln(87) - ln(10), 3, 'ln 8.7'))
lv.claim(round(math.exp(2.4514), 1) == 11.6 and round(math.exp(2.1609), 1) == 8.7, 'makemore dev losses 2.4514 and 2.1609 give 11.6 and 8.7')
E('l7', 'quiz[1].widget.answer', two(math.exp(3.2), 2 ** (3.2 / LN2), 1, 'e^3.2'))
E('l7', 'quiz[1].widget.wrong[0].value', two(2 ** 3.2, math.exp(3.2 * LN2), 1, '2^3.2'))
E('l7', 'quiz[3].widget.wrong[0].value', two(L2(27), ln(27) / LN2, 3, 'log2 27'))

# ---------------- l8 (coin 7 of 10) ----------------
Cn = [.7, .3]
grid = [k / 100 for k in range(1, 100)]
lossA = lambda th: CE(Cn, [th, 1 - th])
lossB = lambda th: -(7 * ln(th) + 3 * ln(1 - th)) / 10 / LN2      # B: the negative log-likelihood of the tosses, averaged
lv.claim(min(grid, key=lossA) == 0.7 and min(grid, key=lossB) == 0.7, 'grid minimum at 0.7 both ways')
E('l8', 'screens[1].widget.answer', two(lossA(.5), lossB(.5), 3, 'loss at 0.5'))
E('l8', 'screens[1].widget.wrong[2].value', two(lossA(.5) * LN2, ln(2), 3, 'nats at 0.5'))
E('l8', 'screens[2].widget.answer', two(lossA(.7), H(Cn), 3, 'loss at 0.7 = entropy'))
E('l8', 'screens[2].explain.text', two(-L2(.7), -ln(.7) / LN2, 3, 's 0.7'))
E('l8', 'screens[3].widget.answer', two(H(Cn) * LN2, -(.7 * ln(.7) + .3 * ln(.3)), 3, 'min nats'))
E('l8', 'screens[3].widget.wrong[1].value', two(H(Cn) / LN2, Hn(Cn) / LN2, 3, 'divided'))
E('l8', 'screens[6].prose', two(100 * lossA(.7), 10 * 10 * lossB(.7), 2, 'total on 100'))
E('l8', 'screens[6].prose', two(10 * lossA(.7), 10 * lossB(.7), 2, 'total on 10'))
E('l8', 'screens[7].widget.answer', two(KL(Cn, [.6, .4]), lossB(.6) - lossB(.7), 3, 'boundary gap'))
E('l8', 'screens[7].widget.wrong[0].value', two(lossA(.6), lossB(.6), 3, 'loss at 0.6'))
E('l8', 'screens[7].widget.wrong[1].value', two(KL([.6, .4], Cn), KLb([.6, .4], Cn), 3, 'reversed gap'))
E('l8', 'screens[7].feedback.correct', two(L2(7 / 6), ln(7 / 6) / LN2, 3, 'log2 7/6'))
E('l8', 'screens[9].widget.answer', two(H([.6, .4]) * LN2, -(.6 * ln(.6) + .4 * ln(.4)), 3, 'log loss 150 of 250'))
lv.claim(150 / 250 == 0.6, 'share of up days 0.6')
E('l8', 'quiz[2].widget.answer', two(H([.75, .25]), Hn([.75, .25]), 3, 'H 0.75'))
E('l8', 'quiz[2].widget.wrong[0].value', two(H([.75, .25]) * LN2, -(.75 * ln(.75) + .25 * ln(.25)), 3, 'H 0.75 nats'))

# ---------------- review ----------------
E('review', 'items[0].widget.wrong[0].value', two(H([.6, .4]), Hn([.6, .4]), 3, 'H 0.6'))
E('review', 'items[1].widget.answer', two(KL([.6, .4], [.8, .2]), KLb([.6, .4], [.8, .2]), 3, 'KL 0.6 vs 0.8'))
E('review', 'items[1].widget.wrong[0].value', two(KL([.6, .4], [.8, .2]) * LN2, .6 * ln(.75) + .4 * ln(2), 3, 'KL nats'))
E('review', 'items[3].widget.answer', two(2 ** 4.5, 16 * math.sqrt(2), 1, '2^4.5'))
E('review', 'items[3].widget.wrong[0].value', two(math.exp(4.5), 2 ** (4.5 / LN2), 1, 'e^4.5'))
E('review', 'items[4].widget.answer', two(math.exp(1.8), 2 ** (1.8 / LN2), 2, 'e^1.8'))
E('review', 'items[4].widget.wrong[0].value', two(2 ** 1.8, math.exp(1.8 * LN2), 2, '2^1.8'))
E('review', 'items[5].widget.answer', two(H([.55, .45]), Hn([.55, .45]), 3, 'H 0.55'))
E('review', 'items[5].widget.wrong[1].value', two(H([.55, .45]) * LN2, -(.55 * ln(.55) + .45 * ln(.45)), 3, 'H 0.55 nats'))
E('review', 'items[7].widget.options', two(.68 / LN2, .68 * 1.4426950408889634, 3, '0.68 nats in bits'))
E('review', 'items[8].widget.answer', two(.4 * LN2, .4 / L2(math.e), 3, '0.4 bits in nats'))
E('review', 'items[9].widget.options', two(412 / 500, 0.824, 3, 'per symbol full'))

# ---------------- homework ----------------
E('homework', 'items[4].widget.model', two(KL([.6, .3, .1], [.4, .4, .2]), KLb([.6, .3, .1], [.4, .4, .2]), 3, 'perf pair KL'))
E('homework', 'items[4].widget.model', two(KL([.6, .3, .1], [.4, .4, .2]) * LN2, sum(x * ln(x / y) for x, y in zip([.6, .3, .1], [.4, .4, .2])), 3, 'perf pair nats'))
E('homework', 'items[5].widget.answer', two(2 ** 2.2, math.exp(2.2 * LN2), 2, '2^2.2'))
E('homework', 'items[5].widget.wrong[0].value', two(math.exp(2.2), 2 ** (2.2 / LN2), 2, 'e^2.2'))
p6, q6 = [.5, .3, .2], [.6, .2, .2]
E('homework', 'items[6].widget.answer', two(CE(p6, q6), CEn(p6, q6), 3, 'fresh CE'))
E('homework', 'items[6].widget.wrong[0].value', two(H(p6), Hn(p6), 3, 'fresh H'))
E('homework', 'items[6].widget.wrong[1].value', two(CE(q6, p6), CEn(q6, p6), 3, 'fresh swapped'))
E('homework', 'items[6].widget.wrong[2].value', two(CE(p6, q6) * LN2, -sum(a * ln(b) for a, b in zip(p6, q6)), 3, 'fresh nats'))
E('homework', 'items[6].explain.text', two(KL(p6, q6), KLb(p6, q6), 3, 'fresh gap'))


def held(tr, te, a):                       # A: direct
    n, k, m = sum(tr), len(tr), sum(te)
    s = 0.0
    for c, d in zip(tr, te):
        if d == 0:
            continue
        q = (c + a) / (n + k * a)
        if q == 0:
            return math.inf
        s -= d / m * ln(q)
    return s


def held_b(tr, te, a):                     # B: as a cross-entropy of shares, via CEn
    n, k = sum(tr), len(tr)
    q = [(c + a) / (n + k * a) for c in tr]
    p = [d / sum(te) for d in te]
    if any(pi > 0 and qi == 0 for pi, qi in zip(p, q)):
        return math.inf
    return CEn(p, q) * LN2


AL = [0, 0.1, 0.5, 1, 2, 5, 20]
for tr, te, want in [([12, 30, 40, 18, 0], [3, 9, 10, 6, 2], 5), ([12, 30, 40, 18, 0], [3, 9, 12, 6, 0], 0), ([5, 0, 3, 2], [4, 1, 3, 2], 2), ([2, 9, 5], [3, 4, 3], 20)]:
    ba = min(AL, key=lambda a: (held(tr, te, a), a))
    bb = min(AL, key=lambda a: (held_b(tr, te, a), a))
    lv.claim(ba == bb == want, f'best smoothing {tr} {te} is {want}')

# ---------------- problem set ----------------
VT, VB = [.35, .3, .25, .1], [.4, .35, .15, .1]
E('problems', 'items[0].parts[0].widget.answer', two(H(VT), Hn(VT), 3, 'bands H'))
E('problems', 'items[0].parts[0].widget.wrong[1].value', two(H(VT) * LN2, -sum(x * ln(x) for x in VT), 3, 'bands nats'))
E('problems', 'items[0].parts[1].widget.answer', two(CE(VT, VB), CEn(VT, VB), 3, 'bands CE'))
E('problems', 'items[0].parts[1].widget.wrong[1].value', two(CE(VB, VT), CEn(VB, VT), 3, 'bands swapped'))
E('problems', 'items[0].parts[2].widget.answer', two(KL(VT, VB), KLb(VT, VB), 3, 'bands KL'))
E('problems', 'items[0].parts[2].widget.wrong[0].value', two(KL(VB, VT), KLb(VB, VT), 3, 'bands KL reversed'))
E('problems', 'items[0].parts[3].widget.answer', two(2 ** CE(VT, VB), math.exp(CE(VT, VB) * LN2), 2, 'bands perplexity'))
E('problems', 'items[0].parts[3].widget.wrong[0].value', two(math.exp(CE(VT, VB)), math.exp(CEn(VT, VB)), 2, 'e^bits'))
E('problems', 'items[0].parts[4].feedback.correct', two(KL(VT, [.25] * 4), 2 - Hn(VT), 3, 'A KL'))
for x in VT:
    E('problems', 'items[0].parts[0].explain.text', two(x * -L2(x), -x * ln(x) / LN2, 3, f'bands term {x}'))
for x in VB:
    E('problems', 'items[0].parts[1].explain.text', two(-L2(x), -ln(x) / LN2, 3, f'B length {x}'))
th = 21 / 60
nll = lambda t: -(th * ln(t) + (1 - th) * ln(1 - t))
nll_b = lambda t: -(21 * ln(t) + 39 * ln(1 - t)) / 60
lv.claim(min(grid, key=nll) == 0.35 == min(grid, key=nll_b), 'fills grid minimum at 0.35')
E('problems', 'items[1].parts[0].widget.answer', two(th, 0.35, 2, 'fills share'))
E('problems', 'items[1].parts[0].widget.wrong[0].value', two(21 / 39, 7 / 13, 2, 'fills odds'))
E('problems', 'items[1].parts[1].widget.answer', two(nll(th), nll_b(th), 3, 'fills loss'))
E('problems', 'items[1].parts[1].widget.wrong[0].value', two(nll(th) / LN2, H([th, 1 - th]), 3, 'fills bits'))
E('problems', 'items[1].parts[2].widget.answer', two(math.exp(nll(th)), 2 ** H([th, 1 - th]), 2, 'fills perplexity'))
E('problems', 'items[1].parts[2].widget.wrong[0].value', two(2 ** nll(th), 2 ** nll_b(th), 2, 'fills 2^nats'))
E('problems', 'items[1].parts[3].widget.answer', two(nll(.45) - nll(th), KL([th, 1 - th], [.45, .55]) * LN2, 3, 'fills gap'))
E('problems', 'items[1].parts[3].widget.wrong[0].value', two(nll(.45), nll_b(.45), 3, 'fills loss at 0.45'))
E('problems', 'items[1].parts[3].widget.wrong[1].value', two(KL([th, 1 - th], [.45, .55]), KLb([th, 1 - th], [.45, .55]), 3, 'fills gap in bits'))
E('problems', 'items[1].parts[1].explain.text', two(-ln(.35), ln(20 / 7), 3, '-ln 0.35'))
E('problems', 'items[1].parts[1].explain.text', two(-ln(.65), ln(20 / 13), 3, '-ln 0.65'))
q13 = [9 / 13, 3 / 13, 1 / 13]
te = [.6, .2, .2]
E('problems', 'items[2].parts[1].widget.answer', two(1 / 13, (0 + 1) / (10 + 3), 3, 'add-one down'))
E('problems', 'items[2].parts[1].widget.wrong[1].value', two(1 / 11, 1 / (10 + 1), 3, 'one over 11'))
E('problems', 'items[2].parts[2].widget.answer', two(CE(te, q13), CEn(te, q13), 3, 'smoothed CE'))
E('problems', 'items[2].parts[2].widget.wrong[0].value', two(H(te), Hn(te), 3, 'test H'))
E('problems', 'items[2].parts[2].widget.wrong[1].value', two(CE(q13, te), CEn(q13, te), 3, 'smoothed swapped'))
E('problems', 'items[2].parts[2].widget.wrong[2].value', two(CE(te, q13) * LN2, -sum(a * ln(b) for a, b in zip(te, q13)), 3, 'smoothed nats'))
for x in q13:
    E('problems', 'items[2].parts[2].explain.text', two(-L2(x), -ln(x) / LN2, 3, f'smoothed length {x}'))
E('problems', 'items[2].parts[3].widget.answer', two(KL(te, q13), KLb(te, q13), 3, 'smoothed KL'))
# ---------------- code widgets: solution passes, starter fails, in CPython ----------------
def code_widgets():
    for fid, doc in lv.files.items():
        def walk(n, p):
            if isinstance(n, dict):
                if n.get('kind') == 'code':
                    yield fid, p, n
                for k, v in n.items():
                    yield from walk(v, f'{p}.{k}')
            elif isinstance(n, list):
                for i, v in enumerate(n):
                    yield from walk(v, f'{p}[{i}]')
        yield from walk(doc, '')


def run(src, w, case):
    ns = {}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(w.get('prelude', ''), ns)
        exec(src, ns)
        exec(w.get('postlude', ''), ns)
        if case.get('setup'):
            exec(case['setup'], ns)
        if case.get('compare') == 'raises':
            try:
                eval(case['call'], ns)
            except Exception as e:
                return type(e).__name__ == case['expect'] or any(c.__name__ == case['expect'] for c in type(e).__mro__)
            return False
        got = eval(case['call'], ns)
    exp = eval(case['expect'])
    if case.get('compare') == 'equal':
        return got == exp
    tol = case.get('tol', {})

    def close(g, e):
        if isinstance(e, dict):
            return isinstance(g, dict) and set(g) == set(e) and all(close(g[k], e[k]) for k in e)
        if isinstance(e, (list, tuple)):
            return isinstance(g, (list, tuple)) and len(g) == len(e) and all(close(x, y) for x, y in zip(g, e))
        try:
            return math.isclose(g, e, rel_tol=tol.get('rel', 0 if 'abs' in tol else 1e-9), abs_tol=tol.get('abs', 1e-12))
        except TypeError:
            return False
    return close(got, exp)


cwd = os.getcwd()
tmp = tempfile.mkdtemp()
try:
    os.chdir(tmp)
    for fid, path, w in code_widgets():
        for name, src in w.get('data', {}).items():
            shutil.copy(os.path.join(APP, src), os.path.join(tmp, name))
        cases = w['tests'] + w.get('examples', [])
        res = []
        for c in cases:
            try:
                res.append(run(w['solution'], w, c))
            except Exception:
                res.append(False)
        lv.claim(all(res), f'{fid}{path}: solution passes {len(cases)} cases', f'failing cases {[i for i, r in enumerate(res) if not r]}')
        bad = []
        for c in w['tests']:
            try:
                bad.append(not run(w['starter'], w, c))
            except Exception:
                bad.append(True)
        lv.claim(any(bad), f'{fid}{path}: starter fails a hidden test')
finally:
    os.chdir(cwd)
    shutil.rmtree(tmp)

lv.check_wrongs()
lv.report()
