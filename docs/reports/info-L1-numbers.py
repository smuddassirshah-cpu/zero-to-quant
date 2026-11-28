"""info level 1 (surprise, entropy, codes): every stated number computed twice and found in the JSON.
Method A uses math.log2; method B uses natural logs divided by ln 2, or a second algorithm where named.
Code widgets: each solution is run in CPython on its hidden tests (and each starter must fail one).
Run from the repo root or anywhere: <venv>/bin/python docs/reports/info-L1-numbers.py"""
import sys, os, math, heapq, zlib, json, shutil, tempfile, contextlib, io
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import Level

APP = os.path.join(HERE, '..', '..', 'app')
lv = Level('info', 1)
L2, LN2 = math.log2, math.log(2)


def two(a, b, places, label):
    """Two methods must agree to the stated places; returns the rounded value."""
    ok = round(a, places) == round(b, places)
    lv.claim(ok, f'{label}: {a!r} and {b!r} agree to {places} places')
    return round(a, places)


def s_bits(p):            # A
    return -L2(p)


def s_bits_b(p):          # B
    return -math.log(p) / LN2


def H(ps):                # A
    return -sum(p * L2(p) for p in ps if p > 0)


def H_b(ps):              # B: natural logs, converted
    return -sum(p * math.log(p) for p in ps if p > 0) / LN2


def huff_avg(ps):         # A: heap with lengths
    h = [(p, i, [i]) for i, p in enumerate(ps)]
    heapq.heapify(h)
    L = [0] * len(ps)
    c = len(ps)
    while len(h) > 1:
        a, b = heapq.heappop(h), heapq.heappop(h)
        for i in a[2] + b[2]:
            L[i] += 1
        heapq.heappush(h, (a[0] + b[0], c, a[2] + b[2]))
        c += 1
    return sum(p * l for p, l in zip(ps, L)), L


def huff_avg_b(ps):       # B: the average equals the sum of the merged weights
    q, tot = sorted(ps), 0.0
    while len(q) > 1:
        a, b = q[0], q[1]
        q = sorted(q[2:] + [a + b])
        tot += a + b
    return tot


# ---------------- l1 ----------------
lv.expect('l1', 'screens[0].widget.answer', two(L2(8), math.log(8) / LN2, 6, 'log2 8'))
lv.expect('l1', 'screens[2].widget.answer', two(s_bits(0.5), s_bits_b(0.5), 3, 'surprise 1/2'))
lv.expect('l1', 'screens[2].widget.wrong[1].value', two(-math.log(0.5), LN2, 3, 'nats of 1/2'))
v = two(s_bits(1 / 6), s_bits_b(1 / 6), 3, 'surprise 1/6')
lv.expect('l1', 'screens[3].widget.answer', v)
lv.expect('l1', 'screens[3].widget.wrong', two(math.log(6), -math.log(1 / 6), 3, 'ln 6'))
lv.expect('l1', 'screens[3].widget.wrong', two(math.log10(6), math.log(6) / math.log(10), 3, 'log10 6'))
lv.expect('l1', 'screens[3].explain.text', two(math.log(6), math.log(2) + math.log(3), 4, 'ln 6 to 4'))
lv.expect('l1', 'screens[3].explain.text', two(LN2, math.log1p(1), 4, 'ln 2'))
v = two(s_bits(0.9), s_bits_b(0.9), 3, 'surprise 0.9')
lv.expect('l1', 'screens[4].widget.answer', v)
lv.expect('l1', 'screens[4].widget.wrong[0].value', two(s_bits(0.1), s_bits_b(0.1), 3, 'surprise 0.1'))
lv.expect('l1', 'screens[4].widget.wrong[1].value', two(-math.log(0.9), -math.log1p(-0.1), 3, 'nats 0.9'))
lv.expect('l1', 'screens[4].explain.text', two(-math.log(0.9), -math.log1p(-0.1), 4, 'nats 0.9 4dp'))
v = two(s_bits(1 / 12), 1 + s_bits(1 / 6), 3, 'surprise 1/12 as 1 + 2.585')
lv.expect('l1', 'screens[5].widget.answer', v)
lv.expect('l1', 'screens[5].widget.wrong[0].value', two(1 * s_bits(1 / 6), s_bits_b(1 / 6), 3, 'multiplied surprises'))
lv.expect('l1', 'screens[5].widget.wrong[1].value', two(1 / 12, 0.5 / 6, 3, 'chance 1/12'))
lv.expect('l1', 'screens[5].widget.wrong[2].value', two(math.log(12), math.log(3) + 2 * LN2, 3, 'ln 12'))
lv.expect('l1', 'screens[6].explain.text', two(-math.log(0.5), LN2, 3, 'ln 0.5'))
lv.expect('l1', 'screens[7].explain.text', two(s_bits(0.001), s_bits_b(0.001), 2, 'surprise 0.001'))
lv.claim(round(s_bits(0.001)) == 10, 'chance 0.001 is about 10 bits')
lv.expect('l1', 'screens[8].widget.options', two(s_bits(1 / 32), s_bits_b(1 / 32), 0, 'surprise 1/32'))
lv.expect('l1', 'screens[8].widget.options', two(math.log(32), 5 * LN2, 3, 'ln 32'))
v = two(s_bits(0.0005), s_bits_b(0.0005), 2, 'halt')
lv.expect('l1', 'screens[10].widget.answer', v)
lv.expect('l1', 'screens[10].widget.wrong[0].value', two(-math.log(0.0005), math.log(2000), 2, 'halt nats'))
lv.expect('l1', 'screens[10].widget.wrong[1].value', two(-math.log10(0.0005), math.log(2000) / math.log(10), 2, 'halt log10'))
lv.expect('l1', 'screens[10].widget.wrong[2].value', two(s_bits(0.98), s_bits_b(0.98), 2, 'tick'))
lv.expect('l1', 'screens[10].explain.text', two(-math.log(0.0005), math.log(2000), 4, 'halt nats 4dp'))
lv.claim(abs(0.98 + 0.0195 + 0.0005 - 1) < 1e-12, 'feed chances add to 1')
lv.expect('l1', 'quiz[0].widget.options', two(math.log(4), 2 * LN2, 3, 'ln 4'))
v = two(s_bits(0.05), s_bits_b(0.05), 2, 'surprise 0.05')
lv.expect('l1', 'quiz[1].widget.answer', v)
lv.expect('l1', 'quiz[1].widget.wrong[0].value', two(-math.log(0.05), math.log(20), 2, 'nats 0.05'))
lv.expect('l1', 'quiz[1].widget.wrong[1].value', two(-math.log10(0.05), math.log(20) / math.log(10), 2, 'log10 0.05'))
lv.expect('l1', 'quiz[1].widget.wrong[2].value', two(s_bits(0.95), s_bits_b(0.95), 2, 'quiet day'))
lv.expect('l1', 'quiz[2].widget.options', two(s_bits(0.2), s_bits_b(0.2), 2, 'surprise 0.2'))
lv.expect('l1', 'quiz[3].widget.answer', two(math.log(8) / LN2, L2(8), 2, 'ln 8 in bits'))
lv.expect('l1', 'quiz[3].prose', two(math.log(8), 3 * LN2, 4, 'ln 8'))
lv.expect('l1', 'quiz[3].widget.wrong[0].value', two(math.log(8) * LN2, 3 * LN2 * LN2, 2, 'times ln2'))
lv.expect('l1', 'quiz[3].explain.text', two(1 / LN2, L2(math.e), 4, 'bits per nat'))
lv.claim(round((2 * 2 + 4 * 3) / 6, 3) == 2.667 and 2 < L2(6) < 3, 'die halving plan between 2 and 3 questions')

# ---------------- l2 ----------------
v = two(H([0.9, 0.1]), H_b([0.9, 0.1]), 3, 'H(0.9, 0.1)')
lv.expect('l2', 'screens[0].widget.answer', v)
lv.expect('l2', 'screens[0].prose', two(s_bits(0.9), s_bits_b(0.9), 3, 's 0.9'))
lv.expect('l2', 'screens[0].prose', two(s_bits(0.1), s_bits_b(0.1), 3, 's 0.1'))
lv.expect('l2', 'screens[0].widget.wrong[0].value', two((0.152 + 3.322) / 2, (s_bits(0.9) + s_bits(0.1)) / 2, 3, 'unweighted mean'))
lv.expect('l2', 'screens[0].widget.wrong[1].value', two(0.152 + 3.322, s_bits(0.9) + s_bits(0.1), 3, 'summed'))
lv.expect('l2', 'screens[0].explain.text', two(0.9 * 0.152, 0.9 * s_bits(0.9), 3, 'term 1'))
lv.expect('l2', 'screens[0].explain.text', two(0.1 * 3.322, 0.1 * s_bits(0.1), 3, 'term 2'))
v = two(H([.5, .25, .125, .125]), H_b([.5, .25, .125, .125]), 3, 'H weather')
lv.expect('l2', 'screens[2].widget.answer', v)
lv.expect('l2', 'screens[2].widget.wrong[0].value', two((1 + 2 + 3 + 3) / 4, sum(s_bits(p) for p in [.5, .25, .125, .125]) / 4, 3, 'unweighted weather'))
lv.expect('l2', 'screens[3].widget.answer', two(H([.25] * 4), L2(4), 3, 'H equal 4'))
lv.expect('l2', 'screens[4].widget.rows[1][2].answer', two(0.3 * s_bits(0.3), 0.3 * s_bits_b(0.3), 3, 'term 0.3'))
lv.expect('l2', 'screens[4].widget.rows[3][2].answer', two(0.1 * s_bits(0.1), 0.1 * s_bits_b(0.1), 3, 'term 0.1'))
lv.expect('l2', 'screens[4].widget.rows[4][2].answer', two(H([.4, .3, .2, .1]), H_b([.4, .3, .2, .1]), 3, 'H 0.4..0.1'))
lv.expect('l2', 'screens[4].widget.rows[4][2].wrong[0].value', two(sum(s_bits(p) for p in [.4, .3, .2, .1]) / 4, sum(s_bits_b(p) for p in [.4, .3, .2, .1]) / 4, 3, 'unweighted 0.4..0.1'))
for i, p in enumerate([.4, .3, .2, .1]):
    lv.expect('l2', f'screens[4].widget.rows[{i}][1]', two(s_bits(p), s_bits_b(p), 3, f'table surprise {p}'))
lv.expect('l2', 'screens[4].widget.rows[0][2]', two(0.4 * s_bits(0.4), 0.4 * s_bits_b(0.4), 3, 'term 0.4'))
lv.expect('l2', 'screens[4].widget.rows[2][2]', two(0.2 * s_bits(0.2), 0.2 * s_bits_b(0.2), 3, 'term 0.2'))
lv.expect('l2', 'screens[5].explain.text', two(H([.7, .1, .1, .1]), H_b([.7, .1, .1, .1]), 3, 'H 0.7 0.1 0.1 0.1'))
lv.expect('l2', 'screens[5].widget.options', two(H([.4, .3, .2, .1]), H_b([.4, .3, .2, .1]), 3, 'H C option'))
lv.expect('l2', 'screens[6].widget.options', two(L2(100), 2 * math.log(10) / LN2, 3, 'log2 100'))
lv.expect('l2', 'screens[7].widget.options', two(L2(3), math.log(3) / LN2, 3, 'log2 3'))
lv.expect('l2', 'screens[8].widget.options', two(H([.5, .25, .25]), H_b([.5, .25, .25]), 1, 'H 1/2 1/4 1/4'))
lv.expect('l2', 'screens[8].widget.options', two((1 + 2 + 2) / 3, sum(s_bits(p) for p in [.5, .25, .25]) / 3, 3, 'unweighted three-way'))
v = two(H([.6, .3, .1]), H_b([.6, .3, .1]), 3, 'H 0.6 0.3 0.1')
lv.expect('l2', 'screens[10].widget.answer', v)
lv.expect('l2', 'screens[10].widget.wrong[1].value', two(H([.6, .3, .1]) * LN2, -sum(p * math.log(p) for p in [.6, .3, .1]), 3, 'nats'))
lv.expect('l2', 'screens[10].widget.wrong[2].value', two(H([.6, .3, .1]) * math.log10(2), -sum(p * math.log10(p) for p in [.6, .3, .1]), 3, 'log10'))
for p in [.6, .3]:
    lv.expect('l2', 'screens[10].explain.text', two(p * s_bits(p), p * s_bits_b(p), 3, f'transfer term {p}'))
lv.expect('l2', 'quiz[0].widget.options', two(6 * s_bits(1 / 6), 6 * s_bits_b(1 / 6), 2, 'summed die'))
lv.expect('l2', 'quiz[0].widget.options', two(s_bits(1 / 6) / 6, s_bits_b(1 / 6) / 6, 3, 'one die term'))
v = two(H([.8, .2]), H_b([.8, .2]), 3, 'H 0.8 0.2')
lv.expect('l2', 'quiz[1].widget.answer', v)
lv.expect('l2', 'quiz[1].widget.wrong[0].value', two(H([.8, .2]) * LN2, -(0.8 * math.log(.8) + .2 * math.log(.2)), 3, 'nats 0.8'))
lv.expect('l2', 'quiz[1].widget.wrong[1].value', two(H([.8, .2]) * math.log10(2), -(0.8 * math.log10(.8) + .2 * math.log10(.2)), 3, 'log10 0.8'))
lv.expect('l2', 'quiz[1].widget.wrong[2].value', two((s_bits(.8) + s_bits(.2)) / 2, (s_bits_b(.8) + s_bits_b(.2)) / 2, 3, 'unweighted 0.8'))
lv.expect('l2', 'quiz[2].explain.text', two(H([.98, .01, .01]), H_b([.98, .01, .01]), 3, 'H 0.98'))
v = two(L2(5), math.log(5) / LN2, 3, 'log2 5')
lv.expect('l2', 'quiz[3].widget.answer', v)

# ---------------- l3 ----------------
lv.expect('l3', 'screens[0].widget.answer', two(4 * 1 + 2 * 2 + 3 + 3, sum(n * len(w) for n, w in [(4, '0'), (2, '10'), (1, '110'), (1, '111')]), 0, '8 reports'))
lv.expect('l3', 'screens[3].widget.answer', two(.5 + .5 + .375 + .375, sum(p * l for p, l in zip([.5, .25, .125, .125], [1, 2, 3, 3])), 3, 'weather average'))
a, Ls = huff_avg([.4, .3, .2, .1])
lv.claim(Ls == [1, 2, 3, 3], 'Huffman lengths 1, 2, 3, 3 for 0.4..0.1')
lv.expect('l3', 'screens[5].widget.answer', two(a, huff_avg_b([.4, .3, .2, .1]), 3, 'Huffman 0.4..0.1'))
lv.expect('l3', 'screens[5].widget.wrong[1].value', two(H([.4, .3, .2, .1]), H_b([.4, .3, .2, .1]), 3, 'entropy wrong'))
lv.expect('l3', 'screens[6].widget.options', two(.5 + .25 + .25 + .125, sum(2 ** -l for l in [1, 2, 2, 3]), 3, 'Kraft 1 2 2 3'))
lv.expect('l3', 'screens[7].prose', two(.5 * 1 + .25 * 1 + .125 * 2 + .125 * 2, sum(p * len(w) for p, w in zip([.5, .25, .125, .125], ['0', '1', '01', '10'])), 2, 'non-prefix average'))
a, _ = huff_avg([.7, .1, .1, .1])
lv.expect('l3', 'screens[8].widget.answer', two(a, huff_avg_b([.7, .1, .1, .1]), 3, 'Huffman ties'))
lv.claim(abs((.7 + .1 * 3 + .1 * 3 + .1 * 2) - 1.5) < 1e-12, 'other tie break also 1.5')
lv.expect('l3', 'screens[8].widget.wrong[0].value', two(H([.7, .1, .1, .1]), H_b([.7, .1, .1, .1]), 3, 'entropy ties'))
a, Ls = huff_avg([.5, .3, .15, .05])
lv.claim(Ls == [1, 2, 3, 3], 'feed lengths')
lv.expect('l3', 'screens[11].widget.answer', two(a, huff_avg_b([.5, .3, .15, .05]), 3, 'feed Huffman'))
lv.expect('l3', 'screens[11].widget.wrong[1].value', two(H([.5, .3, .15, .05]), H_b([.5, .3, .15, .05]), 3, 'feed entropy'))
lv.expect('l3', 'screens[11].feedback.correct', two((2 - a) * 1e6, (2 - huff_avg_b([.5, .3, .15, .05])) * 1e6, 0, 'saved on a million'))
lv.expect('l3', 'quiz[0].widget.answer', two(.6 + .4 + .3 + .3, sum(p * l for p, l in zip([.6, .2, .1, .1], [1, 2, 3, 3])), 3, 'quiz average'))
lv.expect('l3', 'quiz[2].explain.text', two(3 / 4 + 1 / 8, sum(2 ** -l for l in [2, 2, 2, 3]), 3, 'Kraft 2 2 2 3'))

# ---------------- l4 (the names file, read twice) ----------------
NAMES = os.path.join(APP, 'content', 'data', 'ai', 'names.txt')
raw = open(NAMES, 'rb').read()
words = raw.decode().splitlines()
seq = ''.join(w + '.' for w in words)
N = len(seq)
cnt = Counter(seq)
lv.expect('l4', 'screens[0].prose', two(len(words), raw.count(b'\n') + 1, 0, 'names'))
lv.expect('l4', 'screens[0].prose', two(N, len(raw) + 1, 0, 'symbols (bytes plus the final end mark)'))
lv.expect('l4', 'screens[0].prose', two(len(cnt), len(set(raw.decode().replace('\n', ''))) + 1, 0, 'distinct symbols'))
lv.expect('l4', 'screens[0].widget.answer', two(L2(27), math.log(27) / LN2, 3, 'log2 27'))
lv.expect('l4', 'screens[0].widget.wrong[1].value', two(math.log(27), 3 * math.log(3), 3, 'ln 27'))
lv.expect('l4', 'screens[0].widget.wrong[2].value', two(math.log10(27), 3 * math.log10(3), 3, 'log10 27'))
lv.expect('l4', 'screens[0].explain.text', two(math.log(27), 3 * math.log(3), 4, 'ln 27 4dp'))
lv.expect('l4', 'screens[1].feedback.correct', two(cnt['a'], seq.count('a'), 0, 'count of a'))
lv.expect('l4', 'screens[1].widget.options', two(100 * cnt['a'] / N, 100 * seq.count('a') / N, 1, 'share of a'))
lv.expect('l4', 'screens[1].widget.options', two(100 * cnt['.'] / N, 100 * len(words) / N, 1, 'share of end'))
lv.expect('l4', 'screens[1].widget.options', two(100 * cnt['e'] / N, 100 * seq.count('e') / N, 1, 'share of e'))
lv.expect('l4', 'screens[1].widget.options', two(100 / 27, 100 * (1 / 27), 1, 'equal share'))
lv.expect('l4', 'screens[1].explain.text', two(100 * cnt['q'] / N, 100 * seq.count('q') / N, 1, 'share of q'))
lv.claim(cnt.most_common(1)[0][0] == 'a', 'a is the most common symbol')
Huni = H([c / N for c in cnt.values()])
Huni_b = (N * L2(N) - sum(c * L2(c) for c in cnt.values())) / N
hu = two(Huni, Huni_b, 4, 'letter entropy')
lv.expect('l4', 'screens[2].widget.tests[0].expect', hu)
lv.expect('l4', 'screens[2].feedback.correct', two(L2(27) - Huni, L2(27) - Huni_b, 2, 'saving on equal'))
# bigram with add-one smoothing (the makemore model), counts by pairs (A) and by a 27 x 27 table (B)
pairs = Counter()
for w in words:
    ch = ['.'] + list(w) + ['.']
    pairs.update(zip(ch, ch[1:]))
first = Counter()
for (x, y), c in pairs.items():
    first[x] += c
nll = -sum(c * math.log((c + 1) / (first[x] + 27)) for (x, y), c in pairs.items()) / sum(pairs.values())
syms = sorted(cnt)
idx = {s: i for i, s in enumerate(syms)}
T = [[1] * 27 for _ in range(27)]
for (x, y), c in pairs.items():
    T[idx[x]][idx[y]] += c
nll_b, nb = 0.0, 0
for w in words:
    ch = ['.'] + list(w) + ['.']
    for x, y in zip(ch, ch[1:]):
        r = T[idx[x]]
        nll_b -= math.log(r[idx[y]] / sum(r))
        nb += 1
nll_b /= nb
big = two(nll / LN2, nll_b / LN2, 4, 'bigram bits')
lv.expect('l4', 'screens[3].prose', big)
kb = two(N * big / 8 / 1000, N * nll_b / LN2 / 8 / 1000, 0, 'bigram thousand bytes')
lv.expect('l4', 'screens[3].widget.answer', kb)
lv.expect('l4', 'screens[3].widget.wrong[0].value', two(N * big / 1000, N * nll / LN2 / 1000, 0, 'thousand bits'))
lv.expect('l4', 'screens[3].widget.wrong[1].value', two(N * hu / 8000, N * Huni_b / 8000, 0, 'letters KB'))
lv.claim(abs(N * L2(27) / 8000 - 136) < 0.5, 'equal chances about 136 thousand bytes')
lv.expect('l4', 'screens[3].explain.text', two(N * big, N * 3.5412, 0, 'bits at 3.5412'))
lv.expect('l4', 'screens[3].explain.text', two(N * big / 8, N * 3.5412 / 8, 0, 'bytes at 3.5412'))
z = len(zlib.compress(raw, 9))
lv.expect('l4', 'screens[4].feedback.correct', two(z, len(zlib.compress(bytes(raw), 9)), 0, 'zlib bytes'))
zb = two(z * 8 / len(raw), z * 8 / 228145, 4, 'zlib bits per byte')
lv.expect('l4', 'screens[4].widget.tests[0].expect', zb)
lv.expect('l4', 'screens[5].prose', zb)
lv.claim(big < zb < hu, 'zlib sits between the bigram and the letter counts')
lv.expect('l4', 'screens[6].explain.text', two(len(zlib.compress(b'a' * 1000, 9)), len(zlib.compress(bytes(1000 * [97]), 9)), 0, 'zlib of 1000 a'))
lv.expect('l4', 'screens[6].feedback.correct', two(L2(10000), 4 * math.log(10) / LN2, 1, 'log2 10000'))
lv.claim(math.ceil(L2(10000)) == 14, 'about 14 bits for the length')
up = 132 / 250
lv.expect('l4', 'screens[8].widget.answer', two(H([up, 1 - up]), H_b([up, 1 - up]), 3, 'sign entropy'))
lv.expect('l4', 'screens[8].explain.text', two(s_bits(up), s_bits_b(up), 3, 's up'))
lv.expect('l4', 'screens[8].explain.text', two(s_bits(1 - up), s_bits_b(1 - up), 3, 's down'))
lv.expect('l4', 'screens[8].widget.wrong[0].value', two(H([up, 1 - up]) * LN2, -(up * math.log(up) + (1 - up) * math.log(1 - up)), 3, 'sign nats'))
lv.expect('l4', 'quiz[1].widget.answer', two(2e6 * 2.5 / 8 / 1000, 2e6 / 8 * 2.5 / 1000, 0, 'log file KB'))
lv.expect('l4', 'quiz[0].widget.options', two(math.log(32), 5 * LN2, 3, 'ln 32'))

# ---------------- review ----------------
lv.expect('review', 'items[0].widget.answer', two(L2(64), math.log(64) / LN2, 3, 'log2 64'))
lv.expect('review', 'items[0].widget.wrong[1].value', two(math.log(64), 6 * LN2, 3, 'ln 64'))
lv.expect('review', 'items[0].widget.wrong[2].value', two(math.log10(64), 6 * math.log10(2), 3, 'log10 64'))
lv.expect('review', 'items[1].widget.answer', two(H([.5, .3, .2]), H_b([.5, .3, .2]), 3, 'H 0.5 0.3 0.2'))
lv.expect('review', 'items[1].widget.wrong[1].value', two(H([.5, .3, .2]) * LN2, -sum(p * math.log(p) for p in [.5, .3, .2]), 3, 'nats'))
lv.expect('review', 'items[1].widget.wrong[2].value', two(sum(s_bits(p) for p in [.5, .3, .2]) / 3, sum(s_bits_b(p) for p in [.5, .3, .2]) / 3, 3, 'unweighted'))
a, Ls = huff_avg([.45, .25, .2, .1])
lv.expect('review', 'items[3].widget.answer', two(a, huff_avg_b([.45, .25, .2, .1]), 2, 'Huffman 0.45'))
lv.expect('review', 'items[3].widget.wrong[1].value', two(H([.45, .25, .2, .1]), H_b([.45, .25, .2, .1]), 3, 'H 0.45'))
lv.expect('review', 'items[4].widget.answer', two(2 * s_bits(1 / 6), L2(36), 2, 'double six'))
lv.expect('review', 'items[4].widget.wrong[1].value', two(s_bits(1 / 6) ** 2, s_bits_b(1 / 6) ** 2, 2, 'multiplied'))
lv.expect('review', 'items[4].widget.wrong[2].value', two(math.log(36), 2 * math.log(6), 2, 'ln 36'))
lv.expect('review', 'items[5].widget.answer', two(.5 + 4 / 8, sum(2 ** -l for l in [1, 3, 3, 3, 3]), 3, 'Kraft 1 3 3 3 3'))
lv.expect('review', 'items[6].explain.text', two(L2(3), math.log(3) / LN2, 3, 'log2 3'))
lv.claim(max([(H(d), d) for d in ([.6, .2, .2], [.5, .5, 0], [.35, .3, .35], [.8, .1, .1])])[1] == [.35, .3, .35], 'flattest wins')
lv.expect('review', 'items[7].widget.answer', two(50000 * 3.2 / 8, 50000 / 8 * 3.2, 0, 'bytes floor'))
lv.expect('review', 'items[8].widget.answer', two(H([.6, .4, 0]), H_b([.6, .4]), 3, 'H 0.6 0.4 0'))
lv.expect('review', 'items[8].widget.wrong[1].value', two(H([.6, .4]) * LN2, -(.6 * math.log(.6) + .4 * math.log(.4)), 3, 'nats 0.6'))

# ---------------- homework ----------------
lv.expect('homework', 'items[0].widget.answer', two(s_bits(.5) + s_bits(.2) + s_bits(.8), s_bits_b(.5 * .2 * .8), 3, 'three days'))
lv.expect('homework', 'items[0].widget.wrong[1].value', two(-math.log(.08), -(math.log(.5) + math.log(.2) + math.log(.8)), 3, 'three days nats'))
a, Ls = huff_avg([.35, .25, .2, .15, .05])
lv.expect('homework', 'items[2].widget.lines', two(a, huff_avg_b([.35, .25, .2, .15, .05]), 1, 'five-symbol Huffman'))
lv.claim(sorted(Ls) == [2, 2, 2, 3, 3], 'five-symbol lengths 2, 2, 2, 3, 3')
lv.expect('homework', 'items[2].explain.text', two(H([.35, .25, .2, .15, .05]), H_b([.35, .25, .2, .15, .05]), 3, 'five-symbol entropy'))
lv.expect('homework', 'items[2].explain.text', two(a - H([.35, .25, .2, .15, .05]), huff_avg_b([.35, .25, .2, .15, .05]) - H_b([.35, .25, .2, .15, .05]), 3, 'five-symbol gap'))
k = 1 / 2 + 1 / 4 + 3 / 16
lv.expect('homework', 'items[3].widget.answer', two((1 - k) * 16, (1 - sum(2 ** -l for l in [1, 2, 4, 4, 4])) / 2 ** -4, 0, 'room for words of length 4'))
lv.expect('homework', 'items[4].widget.model', two(H([.4, .3, .2, .1]), H_b([.4, .3, .2, .1]), 3, 'model answer entropy'))
lv.expect('homework', 'items[7].widget.answer', two(L2(12), 2 + L2(3), 3, 'log2 12'))
lv.expect('homework', 'items[7].widget.wrong[1].value', two(math.log(12), math.log(3) + 2 * LN2, 3, 'ln 12'))
lv.expect('homework', 'items[7].widget.wrong[2].value', two(math.log10(12), math.log10(3) + 2 * math.log10(2), 3, 'log10 12'))

# ---------------- problem set ----------------
R5 = [.5, .2, .15, .1, .05]
h1 = two(H(R5), H_b(R5), 3, 'router entropy')
lv.expect('problems', 'items[0].parts[0].widget.answer', h1)
lv.expect('problems', 'items[0].parts[0].widget.wrong[0].value', two(L2(5), math.log(5) / LN2, 3, 'log2 5'))
lv.expect('problems', 'items[0].parts[0].widget.wrong[1].value', two(H(R5) * LN2, -sum(p * math.log(p) for p in R5), 3, 'router nats'))
a, Ls = huff_avg(R5)
h2 = two(a, huff_avg_b(R5), 2, 'router Huffman')
lv.claim(Ls == [1, 2, 3, 4, 4], 'router lengths')
lv.expect('problems', 'items[0].parts[1].widget.answer', h2)
lv.expect('problems', 'items[0].parts[1].widget.wrong[1].value', two(sum(Ls) / 5, (1 + 2 + 3 + 4 + 4) / 5, 1, 'router unweighted'))
lv.expect('problems', 'items[0].parts[2].widget.answer', two(h2 - h1, a - H_b(R5), 3, 'router gap'))
lv.expect('problems', 'items[0].parts[3].widget.answer', two((3 - h2) * 1000, (3 - huff_avg_b(R5)) * 1000, 0, 'bits saved'))
lv.expect('problems', 'items[0].parts[3].widget.wrong[0].value', two((3 - H(R5)) * 1000, (3 - H_b(R5)) * 1000, 0, 'vs entropy'))
for p in R5:
    lv.expect('problems', 'items[0].parts[0].explain.text', two(s_bits(p), s_bits_b(p), 3, f'router surprise {p}'))
M = [.45, .15, .4]
lv.expect('problems', 'items[1].parts[0].widget.answer', two(s_bits(.15), s_bits_b(.15), 3, 'flat'))
lv.expect('problems', 'items[1].parts[0].widget.wrong[0].value', two(-math.log(.15), math.log(20 / 3), 3, 'flat nats'))
lv.expect('problems', 'items[1].parts[1].widget.answer', two(s_bits(.15) + s_bits(.45), s_bits_b(.15 * .45), 3, 'flat then up'))
lv.expect('problems', 'items[1].parts[1].widget.wrong[0].value', two(s_bits(.15) * s_bits(.45), s_bits_b(.15) * s_bits_b(.45), 3, 'multiplied'))
hm = two(H(M), H_b(M), 3, 'move entropy')
lv.expect('problems', 'items[1].parts[2].widget.answer', hm)
lv.expect('problems', 'items[1].parts[3].widget.answer', two(H(M) * LN2, -sum(p * math.log(p) for p in M), 3, 'move nats'))
lv.expect('problems', 'items[1].parts[3].widget.wrong[0].value', two(H(M) / LN2, H_b(M) / LN2, 3, 'divided'))
S6, L6 = [.3, .25, .2, .1, .1, .05], [2, 2, 2, 3, 4, 4]
lv.expect('problems', 'items[2].parts[0].widget.answer', two(sum(2 ** -l for l in L6), 3 / 4 + 1 / 8 + 2 / 16, 3, 'Kraft six'))
avg6 = two(sum(p * l for p, l in zip(S6, L6)), .6 + .5 + .4 + .3 + .4 + .2, 1, 'six average')
lv.expect('problems', 'items[2].parts[1].widget.answer', avg6)
lv.expect('problems', 'items[2].parts[1].widget.wrong[0].value', two(sum(L6) / 6, 17 / 6, 3, 'six unweighted'))
h6 = two(H(S6), H_b(S6), 3, 'six entropy')
lv.expect('problems', 'items[2].parts[2].widget.answer', h6)
lv.expect('problems', 'items[2].parts[2].widget.wrong[1].value', two(H(S6) * LN2, -sum(p * math.log(p) for p in S6), 3, 'six nats'))
a, _ = huff_avg(S6)
lv.expect('problems', 'items[2].parts[3].widget.answer', two(sum(p * l for p, l in zip(S6, L6)) - a, avg6 - huff_avg_b(S6), 3, 'Huffman saves nothing'))
lv.expect('problems', 'items[2].parts[3].widget.wrong[0].value', two(avg6 - H(S6), 2.4 - H_b(S6), 3, 'six gap to entropy'))
lv.expect('problems', 'items[3].parts[0].widget.answer', two(L2(16), 4 * LN2 / LN2, 3, 'log2 16'))
lv.expect('problems', 'items[3].parts[1].widget.answer', two(4e5 * 3.1 / 8 / 1000, 4e5 / 8 * 3.1 / 1000, 0, 'log floor'))
lv.expect('problems', 'items[3].parts[2].widget.answer', two(1.6e5 * 8 / 4e5, 1.6e5 / 4e5 * 8, 1, 'zlib bits per char'))
lv.expect('problems', 'items[3].parts[3].widget.answer', two(160 - 4e5 * 3.1 / 8000, (1.6e5 * 8 - 4e5 * 3.1) / 8000, 0, 'zlib above floor'))


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
    try:
        return math.isclose(got, exp, rel_tol=tol.get('rel', 0 if 'abs' in tol else 1e-9), abs_tol=tol.get('abs', 1e-12))
    except TypeError:
        return False


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

# Table totals: every canvas table whose last row is "Total" must add up (rows, columns and the grand total).
import glob as _glob


def _num(s):
    try:
        return float(str(s).replace(',', '').strip())
    except ValueError:
        return None


def _tables(o, path):
    if isinstance(o, dict):
        p = o.get('params')
        if o.get('kind') == 'table' and isinstance(p, dict) and isinstance(p.get('rows'), list):
            yield path, p
        for k, v in o.items():
            yield from _tables(v, path + [k])
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _tables(v, path + [i])


def check_table_totals(names):
    for name in names:
        for fn in sorted(_glob.glob(os.path.join(APP, 'content', 'courses', 'info', name + '.json'))):
            d = json.load(open(fn))
            for path, p in _tables(d, []):
                rows = p['rows']
                if not rows or str(rows[-1][0]).strip().lower() != 'total':
                    continue
                grid = [[_num(c) for c in r[1:]] for r in rows]
                if any(v is None for r in grid for v in r):
                    continue
                where = f'{os.path.basename(fn)}{path}'
                body, tot = grid[:-1], grid[-1]
                for i, r in enumerate(body):
                    lv.claim(abs(sum(r[:-1]) - r[-1]) < 1e-9, f'{where}: row {i} total {r[-1]} is the sum of its cells {sum(r[:-1])}')
                for j in range(len(tot) - 1):
                    s = sum(r[j] for r in body)
                    lv.claim(abs(s - tot[j]) < 1e-9, f'{where}: column {j} total {tot[j]} is the sum of its cells {s}')
                s = sum(r[-1] for r in body)
                lv.claim(abs(s - tot[-1]) < 1e-9, f'{where}: grand total {tot[-1]} is the sum of the row totals {s}')


check_table_totals(['l1-*', 'l2-*', 'l3-*', 'l4-*', 'review-1', 'homework-1', 'problems-1'])

lv.check_wrongs()
lv.report()
