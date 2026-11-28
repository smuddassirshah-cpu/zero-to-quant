"""Recompute every number stated in gpt level 1 (l1 to l4, review-1, homework-1, problems-1), each two ways, and check it
appears in the JSON where it is stated (app/tools/numbers_lib.py).

Method A and method B per kind of figure:
- UTF-8 lengths: Python's encoder (A) and the code-point rows of the UTF-8 table (B).
- BPE: a dict-order trainer with max(counts, key=counts.get) (A) and an independent trainer that scans positions, keeps
  first-occurrence indices explicitly and breaks ties by the smallest first index (B); both merge left to right.
- Encoding: replaying merges in order with list merges (A) and with byte strings and a vocabulary lookup (B).
- Duplicates: a set of seen lines (A) and collections.Counter (B). Jaccard: Python sets (A) and sorted lists merged by hand (B).
- Conversions: direct formulas (A) and math.log2 / an independent route (B).
The full Tiny Shakespeare figures (32,777 lines, 25,721 distinct, 7,056 repeats, 6,913 speaker tags, GLOUCESTER 229 ...) need
the 1,115,394-character text, which is not in the repository (data files stop at 256 KB). Set GPT_FULL_TEXT to its path to
recompute them both ways; without it they are checked against the planner's recorded values in docs/briefs/gpt.md only.
Run from the repository root: <venv>/bin/python docs/reports/gpt-L1-numbers.py   (exits 0 when every check passes)
"""
import os, sys, math, collections
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level('gpt', 1)
SLICE = open(os.path.join(HERE, '..', '..', 'app', 'content', 'data', 'ai', 'tiny-shakespeare.txt'), encoding='utf-8').read()
LN2 = math.log(2)


# ---------------- two UTF-8 length methods ----------------
def u8_a(s):
    return len(s.encode('utf-8'))


def u8_b(s):
    return sum(1 if ord(c) < 0x80 else 2 if ord(c) < 0x800 else 3 if ord(c) < 0x10000 else 4 for c in s)


def u8(s):
    a, b = u8_a(s), u8_b(s)
    lv.claim(a == b, f'UTF-8 length of {s!r}: encoder {a} = rows {b}')
    return a


# ---------------- two BPE trainers ----------------
def merge_a(ids, pair, new):
    out, i = [], 0
    while i < len(ids):
        if i + 1 < len(ids) and ids[i] == pair[0] and ids[i + 1] == pair[1]:
            out.append(new); i += 2
        else:
            out.append(ids[i]); i += 1
    return out


def train_a(text, n):
    ids, m = list(text.encode('utf-8')), []
    for k in range(n):
        c = {}
        for p in zip(ids, ids[1:]):
            c[p] = c.get(p, 0) + 1
        if not c:
            break
        p = max(c, key=c.get)
        if c[p] < 2:
            break
        ids = merge_a(ids, p, 256 + k); m.append(p)
    return m


def train_b(text, n):
    seq, m = list(text.encode('utf-8')), []
    for k in range(n):
        cnt, first = collections.Counter(), {}
        for i in range(len(seq) - 1):
            p = (seq[i], seq[i + 1]); cnt[p] += 1; first.setdefault(p, i)
        if not cnt:
            break
        top = max(cnt.values())
        if top < 2:
            break
        p = min((q for q in cnt if cnt[q] == top), key=lambda q: first[q])
        new, i, out = 256 + k, 0, []
        while i < len(seq):
            if seq[i:i + 2] == list(p):
                out.append(new); i += 2
            else:
                out.append(seq[i]); i += 1
        seq = out; m.append(p)
    return m


def train(text, n, label):
    a, b = train_a(text, n), train_b(text, n)
    lv.claim(a == b, f'two BPE trainers agree on {label}')
    return a


def enc_a(text, m):
    ids = list(text.encode('utf-8'))
    for k, p in enumerate(m):
        ids = merge_a(ids, p, 256 + k)
    return ids


def vocab(m):
    v = {i: bytes([i]) for i in range(256)}
    for k, (a, b) in enumerate(m):
        v[256 + k] = v[a] + v[b]
    return v


def enc_b(text, m):
    # greedy by rank over byte strings: at each step merge the lowest-rank adjacent pair everywhere (equivalent to replay)
    v = vocab(m); rank = {p: k for k, p in enumerate(m)}
    toks = list(text.encode('utf-8'))
    while True:
        cands = [rank[p] for p in zip(toks, toks[1:]) if p in rank]
        if not cands:
            break
        k = min(cands)
        toks = merge_a(toks, m[k], 256 + k)
    assert b''.join(v[t] for t in toks) == text.encode('utf-8')
    return toks


def enc(text, m, label):
    a, b = enc_a(text, m), enc_b(text, m)
    lv.claim(a == b, f'two encoders agree on {label}')
    return a


def jac_a(s, t, n):
    A = {s[i:i + n] for i in range(len(s) - n + 1)}; B = {t[i:i + n] for i in range(len(t) - n + 1)}
    return len(A & B), len(A | B), len(A), len(B)


def jac_b(s, t, n):
    A = sorted(set(s[i:i + n] for i in range(len(s) - n + 1))); B = sorted(set(t[i:i + n] for i in range(len(t) - n + 1)))
    i = j = shared = 0
    while i < len(A) and j < len(B):
        if A[i] == B[j]:
            shared += 1; i += 1; j += 1
        elif A[i] < B[j]:
            i += 1
        else:
            j += 1
    return shared, len(A) + len(B) - shared, len(A), len(B)


def jac(s, t, n, label):
    a, b = jac_a(s, t, n), jac_b(s, t, n)
    lv.claim(a == b, f'Jaccard counts agree for {label}: {a}')
    return a


def bpb(L, b):
    x, y = L / (b * LN2), (L / b) * math.log2(math.e)
    lv.claim(abs(x - y) < 1e-12, f'bits per byte {L}/{b}: two routes agree')
    return x


# ================= l1 =================
for s, n in [('A', 1), ('£', 2), ('é', 2), ('€', 3), ('日', 3), ('\U0001F4C8', 4)]:
    lv.claim(u8(s) == n, f'{s!r} is {n} bytes')
lv.claim(['%02x' % b for b in '£'.encode()] == ['c2', 'a3'] and (0b110 << 5 | 0b00010, 0b10 << 6 | 0b100011) == (0xc2, 0xa3), '£ is c2 a3 by encoder and by hand')
lv.claim(format(163, 'b') == '10100011' and format(163, '011b') == '00010100011', '163 is 10100011, padded 00010100011')
lv.claim('€'.encode().hex() == 'e282ac' and ord('€') == 8364 == 0x20AC, '€ is U+20AC = 8364, bytes e2 82 ac')
lv.claim(len('Price £5') == 8 and u8('Price £5') == 9, 'Price £5: 8 characters, 9 bytes')
lv.claim(len('naïve café') == 10 and u8('naïve café') == 12, 'naïve café: 10 characters, 12 bytes')
lv.claim(len('€5 日') == 4 and u8('€5 日') == 8 and u8('Up \U0001F4C8') == 7, 'explore frames: 4 chars 8 bytes; Up+emoji 7 bytes')
starts = [i for i, b in enumerate('naïve café'.encode()) if b & 0xC0 != 0x80]
lv.claim(starts == [0, 1, 2, 4, 5, 6, 7, 8, 9, 10] and len(starts) == len('naïve café'), 'naïve café: 10 start bytes, af and a9 continue')
lv.expect('l1', 'screens[0].feedback.correct', 'Nine bytes')
lv.expect('l1', 'screens[2].widget.answer', 3)
lv.expect('l1', 'screens[2].question', 8364)
lv.expect('l1', 'screens[4].feedback.correct', 'Ten starts')
lv.claim([u8(n) for n in ['Lloyds plc', 'naïve café', 'Price £5']] == [10, 12, 9] and len('Société Générale') == 16, 'trap table: 10, 12, 9 bytes; Société Générale len 16')
lv.claim(b'caf\xc3'.decode('utf-8', errors='replace') == 'caf�', 'b"caf\\xc3" with replace is caf + U+FFFD')
lv.claim(len(SLICE) == 250000 and u8_a(SLICE) == 250000 and u8_b(SLICE) == 250000, 'slice: 250,000 characters and bytes')
lv.expect('l1', 'quiz[0].widget.answer', 250000)
lv.claim(u8('€5') == 4 and u8('日本') == 6, '€5 is 4 bytes')
lv.expect('l1', 'quiz[1].widget.answer', 4)
lv.claim(int('9f', 16) >> 6 == 0b10, '9f is a continuation byte')
lv.claim(u8('Société G') == 11 and u8('Société Gé') == 13, 'safe_truncate: Société G fits 12, the next é ends at 13')
lv.claim(u8('Price ') == 6 and u8('Price £') == 8, 'Price £5 cut at 7 keeps Price ; at 8 keeps Price £')

# ================= l2 =================
TOY = 'bid bids bidder bidding'
tm = train(TOY, 10, 'the toy')
tv = vocab(tm)
lv.claim([tv[256 + i] for i in range(len(tm))] == [b'bi', b'bid', b' bid', b' bidd'], 'toy merges bi, bid, " bid", " bidd"')
lens = [len(enc_a(TOY, tm[:k])) for k in range(5)]
lv.claim(lens == [23, 19, 15, 12, 10], f'toy lengths {lens}')
c0 = collections.Counter(zip(TOY.encode(), TOY.encode()[1:]))
lv.claim(c0[(98, 105)] == 4 == c0[(105, 100)] and c0[(32, 98)] == 3 and c0[(100, 100)] == 2, 'hook: bi 4, id 4, space-b 3, dd 2')
r1 = enc_a(TOY, tm[:1]); c1 = collections.Counter(zip(r1, r1[1:]))
lv.claim(c1[(256, 100)] == 4 and c1[(32, 256)] == 3 and c1[(105, 100)] == 0, 'after merge 1: bi d 4, space bi 3, i d 0')
lv.expect('l2', 'screens[1].widget.answer', 10)
lv.claim(collections.Counter(zip(b'1000', b'1000'[1:]))[(48, 48)] == 2 and merge_a(list(b'1000'), (48, 48), 256) == [49, 256, 48], '1000: pair 00 counted twice, merge leaves 1 00 0')
lv.expect('l2', 'screens[3].widget.answer', 2)
lv.claim(train(('papa mama'), 1, 'papa mama') == [(112, 97)], 'papa mama: pa first')
t20 = SLICE[:20000]
m200 = train(t20, 200, 'the first 20,000 Shakespeare characters, 200 merges')
v200 = vocab(m200)
lv.claim([v200[256 + i] for i in range(8)] == [b'e ', b'th', b't ', b's ', b'ou', b', ', b'd ', b'r '], 'first eight Shakespeare merges')
counts = {n: len(enc(t20, m200[:n], f'20,000 characters with {n} merges')) for n in (0, 25, 50, 100, 150, 200)}
lv.claim(counts == {0: 20000, 25: 15240, 50: 13665, 100: 11886, 150: 10731, 200: 9940}, f'token counts {counts}')
lv.expect('l2', 'screens[5].widget.answer', round(20000 / 13665, 4))
lv.claim(round(20000 / 13665, 4) == round(float(Fr(20000, 13665)), 4) == 1.4636 and round(20000 / 9940, 4) == 2.0121, '1.4636 and 2.0121 bytes per token')
shrink = 1 - 9940 / 13665
lv.claim(abs(shrink - float(Fr(3725, 13665))) < 1e-12 and round(shrink, 4) == 0.2726, 'shrink 3725/13665 = 0.2726')
lv.expect('l2', 'screens[6].widget.answer', 0.2726)
lv.expect('l2', 'screens[6].explain.text', 3725)
lv.claim(256 + 50 == 306 and 256 + 200 == 456 and round(150 / 306, 4) == 0.4902, 'vocabulary 306 and 456; 150/306')
LOG = 'NEW BUY VOD 100\nNEW SELL BP 200\nNEW BUY BP 100\nCXL BUY VOD 100\n'
lm = train(LOG, 8, 'the order log')
lv.claim(len(LOG) == 63 and len(enc(LOG, lm, 'the order log')) == 35, 'order log: 63 bytes to 35 tokens')
lv.claim(collections.Counter(zip(b'see sea seen', b'see sea seen'[1:]))[(115, 101)] == 3 and train('see sea seen', 1, 'see sea seen') == [(115, 101)], 'quiz: se 3, merged first')
lv.claim(merge_a([5] * 5, (5, 5), 300) == [300, 300, 5], 'quiz: [300, 300, 5]')

# ================= l3 =================
lv.claim(enc('bidding bids', tm, 'bidding bids') == [257, 100, 105, 110, 103, 258, 115], 'bidding bids is 7 tokens')
lv.expect('l3', 'screens[0].widget.answer', 7)
lv.claim(len(tv[259]) == 5, 'token 259 is 5 bytes')
lv.expect('l3', 'screens[2].widget.answer', 5)
lv.claim(enc('€5', tm, '€5') == [226, 130, 172, 53], '€5 is 4 tokens')
val = SLICE[-25000:]
nval = len(enc(val, m200, 'the held-out 25,000 characters'))
lv.claim(nval == 13809 and round(25000 / nval, 4) == 1.8104, 'held out: 13,809 tokens, 1.8104 bytes per token')
lv.expect('l3', 'screens[4].widget.answer', 1.8104)
THE = [(101, 114), (116, 104), (257, 101)]
lv.claim(enc('the there', THE, 'the there') == [258, 32, 257, 256, 101], 'the there: there splits th er e')
x = bpb(4.20, 2.0121); y = bpb(2.4554, 1)
lv.claim(round(x, 4) == 3.0114 and round(y, 4) == 3.5424, f'4.20 nats/token at 2.0121 is {x:.4f}; bigram {y:.4f}')
lv.expect('l3', 'screens[6].widget.answer', 3.0114)
lv.expect('l3', 'screens[6].canvas.params.rows', 3.5424)
lv.claim(round(math.log2(65), 4) == 6.0224 == round(bpb(math.log(65), 1), 4), 'log2 65 = 6.0224')
a, b = bpb(3.10, 3.8), bpb(2.60, 3.0)
lv.claim(round(a, 2) == 1.18 and round(b, 2) == 1.25 and a < b, 'vendors: A 1.18 < B 1.25')
lv.claim(round(bpb(1.30, 1), 4) == 1.8755, 'quiz: 1.30 nats is 1.8755 bits')
lv.expect('l3', 'quiz[1].widget.answer', 1.8755)
lv.claim(round(bpb(2.9, 3.1), 2) == 1.35 and round(bpb(3.4, 3.9), 2) == 1.26, 'quiz: 1.35 then 1.26')
lv.claim(b''.join(tv[i] for i in [257, 115, 259, 101, 114]) == b'bids bidder', 'quiz: decode bids bidder')

# ================= l4 =================
L = [l for l in SLICE.split('\n') if l != '']
seen = set(); rep_a = 0
for l in L:
    if l in seen:
        rep_a += 1
    else:
        seen.add(l)
cnt = collections.Counter(L); rep_b = sum(v - 1 for v in cnt.values())
lv.claim(len(L) == 7606 and len(seen) == len(cnt) == 5920 and rep_a == rep_b == 1686, 'slice: 7,606 lines, 5,920 distinct, 1,686 removed')
lv.expect('l4', 'quiz[0].widget.answer', 1686)
lv.claim([(k, v) for k, v in cnt.most_common(5)] == [('MENENIUS:', 162), ('CORIOLANUS:', 149), ('GLOUCESTER:', 149), ('SICINIUS:', 117), ('BRUTUS:', 91)], 'slice top five lines')
lv.claim(SLICE.split('\n')[6] == 'First Citizen:' == SLICE.split('\n')[0] and SLICE.split('\n')[9] == 'All:' == SLICE.split('\n')[3], 'hook: lines 7 and 10 repeat 1 and 4')
FULL = {'lines': 32777, 'distinct': 25721, 'repeats': 7056, 'tags': 6913, 'top': [('GLOUCESTER:', 229), ('DUKE VINCENTIO:', 193), ('ROMEO:', 163), ('MENENIUS:', 162), ('PETRUCHIO:', 158)]}
fp = os.environ.get('GPT_FULL_TEXT')
if fp and os.path.exists(fp):
    full = open(fp, encoding='utf-8').read()
    lv.claim(len(full) == 1115394 and full.startswith(SLICE), 'full text: 1,115,394 characters, the slice is its start')
    FL = [l for l in full.split('\n') if l != '']
    fs, fr = set(), 0
    for l in FL:
        if l in fs:
            fr += 1
        else:
            fs.add(l)
    fc = collections.Counter(FL)
    lines = full.split('\n')
    tags = {l for i, l in enumerate(lines) if l.endswith(':') and (i == 0 or lines[i - 1] == '')}
    seen2, trep = set(), 0
    for l in FL:
        if l in seen2 and l in tags:
            trep += 1
        seen2.add(l)
    lv.claim((len(FL), len(fs), fr, sum(v - 1 for v in fc.values())) == (32777, 25721, 7056, 7056), 'full text lines, distinct, repeats both ways')
    lv.claim(trep == 6913 and fc.most_common(5) == FULL['top'], 'full text: 6,913 speaker-tag repeats; top five')
else:
    lv.claim(FULL['lines'] - FULL['distinct'] == FULL['repeats'], 'recorded full-text figures (docs/briefs/gpt.md): 32,777 - 25,721 = 7,056 (GPT_FULL_TEXT not set)')
lv.expect('l4', 'screens[2].widget.answer', 7056)
share = FULL['tags'] / FULL['repeats']
lv.claim(round(share, 4) == 0.9797 and round(float(Fr(6913, 7056)) * 100, 1) == 98.0 and 7056 - 6913 == 143, '6,913 / 7,056 = 98.0%; 143 others')
lv.expect('l4', 'screens[3].widget.answer', 0.9797)
lv.claim(round(6913 / 32777, 4) == 0.2109 and round(143 / 7056, 4) == 0.0203, 'trap slips 0.2109 and 0.0203')
S1 = 'Shell shares rose 2% to £27.10 on Tuesday after the oil major raised its quarterly dividend.'
S2 = S1.replace('£27.10', '£27.40')
sh_, un_, nA, nB = jac(S1, S2, 5, 'the two Shell stories')
lv.claim(len(S1) == 92 and nA == nB == 88 and sh_ == 83 and un_ == 93, 'story: 92 characters, 88 shingles, 83 shared, 93 in either')
lv.claim(round(sh_ / un_, 4) == 0.8925 == round(float(Fr(83, 93)), 4), 'J = 83/93 = 0.8925')
lv.expect('l4', 'screens[5].widget.answer', 88)
lv.expect('l4', 'screens[6].widget.answer', 0.8925)
lv.claim(round(83 / 88, 4) == 0.9432 and round(83 / 176, 4) == 0.4716, 'Jaccard slips 0.9432 and 0.4716')
NOTE = ('Hartley Lowe keeps its buy rating on Northgate Retail with a target price of 412p. '
        'Like-for-like sales grew 3.1% in the quarter and margins held at 6.4%.')
NOTE2 = ('Hartley Lowe cuts Fenwick Mining to hold with a target price of 188p. '
         'Copper output fell 7.5% in the quarter and costs rose faster than expected.')
D = {'A': 'Feed A | ' + NOTE, 'B': 'Feed B 07:02 | ' + NOTE, 'C': 'Feed C | ' + NOTE + ' Not for retail clients.', 'D': 'Feed A | ' + NOTE2}
pj = {}
for p, q in [('A', 'B'), ('A', 'C'), ('B', 'C'), ('A', 'D'), ('B', 'D'), ('C', 'D')]:
    s_, u_, _, _ = jac(D[p], D[q], 5, f'notes {p} and {q}')
    pj[p + q] = round(s_ / u_, 2)
lv.claim(pj == {'AB': 0.91, 'AC': 0.83, 'BC': 0.8, 'AD': 0.22, 'BD': 0.19, 'CD': 0.18} and min(jac_a(D[p], D[q], 5)[0] / jac_a(D[p], D[q], 5)[1] for p, q in ['AB', 'AC', 'BC']) >= 0.8, f'distributor table {pj}; B and C at 0.801, above 0.8')
lv.claim(len({'aaaa'[i:i + 3] for i in range(2)}) == 1, 'quiz: aaaa has 1 distinct 3-shingle')

# ================= review =================
lv.claim(u8('Zürich €') == 11, 'Zürich € is 11 bytes')
lv.expect('review', 'items[0].widget.answer', 11)
lv.claim(train('abab ab', 10, 'abab ab') == [(97, 98)] and len(enc_a('abab ab', [(97, 98)])) == 4, 'abab ab: 4 tokens')
lv.claim(train('xyxyz xyz', 10, 'xyxyz xyz') == [(120, 121), (256, 122)], 'xyxyz xyz: second merge xyz')
lv.claim(enc('banana', [(97, 110), (110, 97), (256, 97)], 'banana') == [98, 256, 258], 'banana: 3 tokens')
lv.claim(len(merge_a(list(b'banana'), (110, 97), 9)) == 4, 'banana na-first slip gives 4')
r = bpb(3.6, 4.1); lv.claim(round(r, 4) == 1.2668, f'3.6 at 4.1 bytes per token: {r:.4f}')
lv.expect('review', 'items[5].widget.answer', 1.2668)
lv.claim(len(enc_a('日本', train('the cat sat on the mat and the cat ran', 20, 'an English text'))) == 6, '日本 is 6 byte tokens')
lv.claim(Fr(30, 40 + 50 - 30) == Fr(1, 2), 'Jaccard 30/60 = 0.5')
H1 = 'Ashby Copper shares fall 4% after quarterly output misses forecasts'
sh_, un_, nA, _ = jac(H1, H1.replace('4%', '6%'), 5, 'the two headlines')
lv.claim((len(H1), nA, sh_, un_) == (67, 63, 58, 68) and round(sh_ / un_, 4) == 0.8529, 'headlines: 67 chars, 63 shingles, 58/68 = 0.8529')
lv.expect('review', 'items[9].widget.answer', 0.8529)

# ================= homework =================
lv.claim(train('toto koko', 10, 'toto koko') == [(116, 111), (107, 111)], 'toto koko: to before ko')
m50 = train(t20, 50, '20,000 characters, 50 merges')
h = SLICE[-5000:]
lv.claim(round(5000 / len(enc(h, m50, 'the last 5,000 characters')), 4) == 1.4434, 'held-out 5,000: 1.4434 bytes per token, above 1.4')
lv.claim([v200[i] for i in enc(' strawberry', m200, ' strawberry')] == [b' ', b'st', b'ra', b'w', b'b', b'er', b'r', b'y'], 'strawberry split in the model answer')
x = bpb(2.95, 2400000 / 800000)
lv.claim(2400000 / 800000 == 3 and round(x, 4) == 1.4187, f'filings: 3 bytes per token, {x:.4f}')
lv.expect('homework', 'items[4].widget.answer', 1.4187)

# ================= problems =================
M = [(111, 110), (256, 100), (98, 257), (32, 258), (117, 110)]
T = 'bonds fund bond'
pl = [len(enc(T, M[:k], f'bonds fund bond, {k} merges')) for k in range(6)]
lv.claim(pl == [15, 13, 11, 9, 8, 7], f'bond lengths {pl}')
lv.expect('problems', 'items[0].parts[0].widget.answer', 13)
lv.expect('problems', 'items[0].parts[1].widget.answer', 7)
lv.claim(round(15 / 7, 4) == 2.1429 and round(7 / 15, 4) == 0.4667, '15/7 = 2.1429')
x = bpb(4.1, 15 / 7)
lv.claim(round(x, 4) == 2.7604 and round(bpb(4.1, 2.1429), 4) == 2.7603, f'bond bits per byte {x:.4f}; carried 2.1429 gives 2.7603, inside the band')
lv.expect('problems', 'items[0].parts[3].widget.answer', 2.7604)
N = 'Lefèvre & Søn'
lv.claim(len(N) == 13 and u8(N) == 15, 'Lefèvre & Søn: 13 characters, 15 bytes')
lv.claim(N.encode()[:12].decode() == 'Lefèvre & S' and len(N.encode()[:13].decode('utf-8', errors='replace')) == 12, '12-byte cut keeps 11; raw 13 shows 12')
lv.claim(12400 - 9850 == 2550 and Fr(1100, 1200 + 1150 - 1100) == Fr(22, 25), 'transcripts: 2,550 removed; J = 0.88')
lv.claim(Fr(36, 400) == Fr(9, 100), '36 of 400 is 9%')
x = bpb(2.2, 4.0); lv.claim(round(x, 4) == 0.7935, f'2.2 at 4.0: {x:.4f}')
lv.expect('problems', 'items[2].parts[4].widget.answer', 0.7935)

lv.check_wrongs()
lv.check_slips()
lv.report()
