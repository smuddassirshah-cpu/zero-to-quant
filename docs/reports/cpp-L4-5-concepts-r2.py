#!/usr/bin/env python3
"""Concept checks for cpp levels 4 and 5, blind audit round 2 (docs/reviews/audit-cpp-4-5-r2.md).

Part A (pure Python): every stated figure of the two levels recomputed, and read against the content JSON where the figure is a key.
Part B (C++): docs/reports/cpp-L4-5-concepts-r2-run.mjs compiles and runs, with the page's own unit builder and worker code and the
YoWASP clang 21 of the local CDN (wasm32, -O1, libc++ hardening, no exceptions): every solution, example and starter; 165 natural wrong
or alternative codings against the feedback line they should reach; 34 claim programs (sizes, growth, moves, special members, what
undefined snippets do here); and the proposed new hidden tests.

Exit 0 on correct content. A check tagged FINDING fails because the content is wrong (see the audit file) and stays failing until fixed.

Fix pass (Opus fixer): only checks that encoded the old content were re-pointed. The six wrong programs tagged FINDING in
-mutants.mjs now name the new test-N they must reach; the PROPOSED-FIX jobs run on the content as it stands (the tests are in it);
-programs.mjs reads the l21 screen 9 listing from the content instead of a copy; and a block of FP codings sweeps each test-N line
the fix pass wrote. The part A text checks are unchanged.

  python3 docs/reports/cpp-L4-5-concepts-r2.py [--pkgs <local cdn folder>] [--no-cpp] [--jobs 3]
The local CDN folder is --pkgs, else $ZQ_LOCAL_CDN (the folder the playthrough takes as --local-cdn). Part B takes about four minutes.
"""
import json, math, os, re, subprocess, sys
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
APP = os.path.join(ROOT, 'app')
C = os.path.join(APP, 'content', 'courses', 'cpp')
bad = []
n_ok = 0


def J(name):
    with open(os.path.join(C, name + '.json'), encoding='utf-8') as f:
        return json.load(f)


def check(tag, ok, text):
    global n_ok
    if ok:
        n_ok += 1
    else:
        bad.append((tag, text))
        print(f'FAIL {tag} {text}')


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def texts(o):
    """every string in a JSON value"""
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from texts(v)
    elif isinstance(o, list):
        for v in o:
            yield from texts(v)


L14, L15, L16, L17, L18 = J('l14-vector'), J('l15-maps'), J('l16-algorithms'), J('l17-cmake'), J('l18-unit-tests')
L19, L20, L21, L22, L23 = J('l19-moving-not-copying'), J('l20-rule-of-five'), J('l21-virtual-dispatch'), J('l22-undefined-behaviour'), J('l23-own-smart-pointer')
R4, R5, H4, H5 = J('review-4'), J('review-5'), J('homework-4'), J('homework-5')
item = lambda d, i: next(x for x in d['items'] if x['id'] == i)
quiz = lambda d, i: next(x for x in d['quiz'] if x['id'] == i)

# ---------------------------------------------------------------- l14 vector
def doubling(n_push, start=0):
    """capacity model of libc++ and libstdc++: max(2 * cap, size + 1)"""
    cap, size, allocs, moves, copied = start, 0, 0, 0, 0
    for _ in range(n_push):
        if size == cap:
            new = max(2 * cap, size + 1)
            allocs += 1
            if size:
                moves += 1
                copied += size
            cap = new
        size += 1
    return cap, allocs, moves, copied

check('l14', doubling(5)[0] == 8 == L14['screens'][1]['widget']['answer'], 's1 five pushes give capacity 8')
cap, allocs, moves, copied = doubling(600)
check('l14', (cap, allocs, moves, copied) == (1024, 11, 10, 1023), 's2 600 pushes without reserve: 11 allocations, 10 moves, 1,023 copies')
check('l14', L14['screens'][2]['widget']['answer'] == 0 and [w['value'] for w in L14['screens'][2]['widget']['wrong']] == [10, 11, 1], 's2 key 0, slips 10, 11, 1')
check('l14', all(doubling(n)[3] < 2 * n for n in range(1, 5000)), 'summary: copies for n pushes < 2n under doubling')
def mov(xs, n):
    return [] if n < 1 or n > len(xs) else [sum(xs[i:i + n]) / n for i in range(len(xs) - n + 1)]
for t in L14['screens'][3]['widget']['tests']:
    got, want = mov(*t['args']), t['expect']
    check('l14', len(got) == len(want) and all(close(a, b) for a, b in zip(got, want)), f's3 test {t["args"]}')
for t in L14['screens'][4]['widget']['tests']:
    if 'args' in t:
        px = t['args'][0]
        got = [px[i] / px[i - 1] - 1 for i in range(1, len(px))]
        check('l14', len(got) == len(t['expect']) and all(close(a, b) for a, b in zip(got, t['expect'])), f's4 test {px}')
check('l14', 2 ** 32 - 1 == 4294967295 and close(2 ** 64 - 1, 1.8e19, 0.03), 's4 largest size_t: 4.3 billion here, 1.8e19 on 64 bits')
check('l14', close(101.5 + 99.8 + 102.3, 303.6) and close(100.0 + 101.5 + 99.8 + 102.3, 403.6) and close(101.5 + 99.8, 201.3), 's5 303.6, slips 403.6 and 201.3')
def lattice(s0, u, d, steps):
    return [[s0 * u ** (i - j) * d ** j for j in range(i + 1)] for i in range(steps + 1)]
t = lattice(100, 1.25, 0.8, 50)
check('l14', all(close(a, b) for a, b in zip(lattice(100, 1.25, 0.8, 3)[3], [195.3125, 125.0, 80.0, 51.2])) and len(t[50]) == 51 and close(t[50][25], 100.0), 's10 row 3 and the middle of row 50')
check('l14', 64 // 8 == 8, 'quiz: eight doubles to a 64-byte cache line')

# ---------------------------------------------------------------- l15 maps
check('l15', sorted(['VOD', 'BARC', 'AZN']) == ['AZN', 'BARC', 'VOD'], 's0 key order')
check('l15', math.ceil(math.log2(7 + 1)) == 3 and math.ceil(math.log2(1e6 + 1)) == 20 and 2 * math.log2(1e6 + 1) <= 40, 's1 3 steps for 7 keys; 20 to 40 for a million (red-black height <= 2 log2(n + 1))')
check('l15', close(1000 * 0.72 - 500 * 2.10, -330.0) and close(20 * 118.5 - 300 * 6.42, 444.0), 's5 exposures -330 and 444')
check('l15', 100.1 + 0.1 != 100.2 and repr(100.1 + 0.1) == '100.19999999999999' and L15['screens'][9]['widget']['answer'] == 3, 's9 three double keys')
check('l15', 15 <= math.log2(40000) <= 16, 'quiz: about 16 comparisons for 40,000 keys')

# ---------------------------------------------------------------- l16 algorithms
pnl = [120.5, -40.25, 75.0, -10.5, 30.25]
check('l16', close(sum(pnl), 175.0) and close(sum(pnl[:4]), 144.75) and L16['screens'][1]['widget']['answer'] == 175, 's1 175, slips 120.5 and 144.75')
tot, chain = 0, []
for x in pnl:
    tot = int(tot + x)  # int total: truncation towards zero after every step
    chain.append(tot)
check('l16', chain == [120, 79, 154, 143, 173] and L16['screens'][7]['widget']['answer'] == 173, 's7 int total 120, 79, 154, 143, 173')
rets = [0.01, -0.03, 0.025, -0.005, 0.04]
check('l16', sum(abs(r) > 0.02 for r in rets) == 3 and sum(r > 0.02 for r in rets) == 2 and sum(abs(r) > 0.05 for r in rets) == 0, 's2 and h4-capture: 3 counted, 2 without abs, 0 at 0.05')
for t in L16['screens'][3]['widget']['tests']:
    px, q = t['args']
    got = 0.0 if sum(q) == 0 else sum(a * b for a, b in zip(px, q)) / sum(q)
    check('l16', close(got, t['expect']), f's3 vwap test {px} {q}')
check('l16', close((100 + 101 + 102) / 3, 101.0) and int(int(0 + 10.25 * 3) + 10.75 * 1) / 4.0 == 10.0 and (int(int(int(0 + 100 * 200) + 101 * 100) + 102 * 100)) // 400 == 100, 's3 slips: 101 unweighted, 10 with an int value total, 100 with both totals int')
def dd(daily):
    cum, s = [], 0.0
    for x in daily:
        s += x
        cum.append(s)
    peak = worst = 0.0
    for c in cum:
        peak = max(peak, c)
        worst = max(worst, peak - c)
    return worst
for t in L16['screens'][9]['widget']['tests']:
    check('l16', close(dd(t['args'][0]), t['expect']), f's9 drawdown {t["args"][0]}')
check('l16', [50, 30, 65] == [50, 50 - 20, 50 - 20 + 35], 'quiz partial sums 50, 30, 65')

# ---------------------------------------------------------------- l17 cmake
check('l17', close(math.exp(-0.1), 0.9048374180359595) and close(100 * math.exp(0.05), 105.12710963760242) and close(5 * math.exp(-0.04) + 5 * math.exp(-0.08) + 105 * math.exp(-0.12), 102.54617478299633) and close(100 * math.exp(-0.015), 98.51119396030627), 's4 discount factor, forward and present values')
check('l17', close(90 / 360, 0.25) and close(73 / 365, 0.2) and close(5.0 * 182 / 365, 2.493150684931507) and close(4.5 * 180 / 360, 2.25) and round(90 / 365, 4) == 0.2466 and round(73 / 360, 4) == 0.2028 and 90 // 360 == 0, 's5 year fractions and the three slips')
check('l17', close(1.28 / 0.16, 8) and close(0.16 / 1.28, 0.125) and close(1.28 - 0.16, 1.12), 's6 speed-up 8, slips 0.125 and 1.12')
check('l17', round(4.1 / 0.16) == 26 and round(4.1 / 1.3) == 3, 'quiz 26 times and 3 times')

# ---------------------------------------------------------------- l18 tests
N = lambda x: 0.5 * math.erfc(-x / math.sqrt(2.0))
def bs(S, K, r, s, T, half=0.5, df=None):
    d1 = (math.log(S / K) + (r + half * s * s) * T) / (s * math.sqrt(T))
    d2 = d1 - s * math.sqrt(T)
    return S * N(d1) - K * (math.exp(-r * T) if df is None else df) * N(d2)
def binom(S, K, r, s, T, n, disc=None):
    dt = T / n
    u = math.exp(s * math.sqrt(dt)); d = 1 / u
    dc = math.exp(-r * dt) if disc is None else disc
    p = (math.exp(r * dt) - d) / (u - d)
    val = [max(S * u ** (n - j) * d ** j - K, 0.0) for j in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(i + 1):
            val[j] = dc * (p * val[j] + (1 - p) * val[j + 1])
    return val[0]
v = bs(100, 100, 0.05, 0.2, 1.0)
check('l18', round(v, 6) == 10.450584 and round(v, 4) == 10.4506 and round(abs(v - 10.4506), 6) == 0.000016 and 1e-5 < abs(v - 10.4506) < 1e-4, 's3 the pin 10.4506 is 0.000016 from 10.450584')
check('l18', abs(bs(100, 100, 0.05, 0.2, 1.0, half=1.0) - 10.4506) > 1e-2 and abs(bs(100, 100, 0.05, 0.2, 1.0, df=1.0) - 10.4506) > 1e-2, 's3 planted bugs 1 and 3 move the at-the-money value by more than 0.01')
b100, b99, b2000, b1999 = (binom(100, 100, 0.05, 0.2, 1.0, n) for n in (100, 99, 2000, 1999))
check('l18', round(b100, 6) == 10.430612 and abs(b100 - 10.430612) < 1e-6 and abs(b100 - 10.430612) > 1e-7, 's9 100 steps: 10.430612 to six places; 1e-6 holds and 1e-7 does not')
check('l18', round(b99, 4) == 10.4683 and abs(b2000 - 10.450584) < 0.002 and abs(b1999 - 10.450584) < 0.002, 's9 99 steps give 10.4683; 2,000 and 1,999 steps both sit within 0.002 of Black-Scholes')
check('l18', abs(binom(100, 100, 0.05, 0.2, 1.0, 100, disc=1.0) - 10.430612) > 0.1 and abs(binom(100, 100, 0.05, 0.2, 1.0, 100) - 10.450584) > 0.002, 's9 the no-discount bug is far off; 100 steps is 0.02 from Black-Scholes')
check('l18', repr(110.0 / 100.0 - 1) == '0.10000000000000009' and 110.0 / 100.0 - 1 != 0.1 and Decimal(1.1) > Decimal('1.1'), 's7 110.0 / 100.0 - 1 is 0.10000000000000009')
check('l18', round(10 / 110, 4) == 0.0909 and abs(10 / 110 - 0.1) > 0.005, 's4 the shipped code gives 0.0909')
check('l18', close((100 * 100 + 102 * 300) / 400, 101.5) and round(10.430612 - 10.430598, 6) == 0.000014, 'quiz 101.5 and 0.000014')
check('l18', close(1.1920929e-7 * 100, 1.2e-5, 0.01), 'Catch2 Approx default epsilon: 100 * FLT_EPSILON = 1.19e-5')
# FINDING 1: the key of screen 7 holds only for one of the two correct ways to write the fix
s7 = L18['screens'][7]
names_formula = bool(re.search(r'px\[i\] / px\[i - 1\] - 1', s7.get('prose', '')))
check('FINDING', (110.0 - 100.0) / 100.0 != 0.1 or names_formula, 'l18 s7: with the fix `(px[i] - px[i - 1]) / px[i - 1]` (the starter of screen 5 with its divisor changed) the result is exactly 0.1 and the test passes, yet the key is FAIL; the screen must say which formula the fixed code uses')

# ---------------------------------------------------------------- l19 moves
check('l19', close(8_000_000 / 10e9 * 1e3, 0.8), 's1 8,000,000 bytes at 10 GB/s is 0.8 ms')
def pushes(n, noexcept=True):
    cap = size = copies = moves = 0
    for _ in range(n):
        if size == cap:
            cap = max(2 * cap, size + 1)
            if noexcept:
                moves += size
            else:
                copies += size
        moves += 1
        size += 1
    return copies, moves
check('l19', pushes(4) == (0, 7) and pushes(2, False) == (1, 2) and pushes(8) == (0, 15) and pushes(8, False) == (7, 8), 's3 0 copies 7 moves; s4 1 copy 2 moves; h5-vec 15 moves, and 7 copies 8 moves for Wobbly')
t3 = L19['screens'][3]['widget']['rows'][0]
check('l19', (t3[0]['answer'], t3[1]['answer']) == (0, 7), 's3 keys 0 and 7')
r9 = L19['screens'][9]['widget']['rows']
check('l19', [r[1]['answer'] for r in r9] == [1000000, 0, 0], 's9 sink keys')
txt = L19['screens'][1]['explain']['text']
check('FINDING', '16 on a desktop' not in txt, 'l19 s1 explain: `Buffer` holds an `int` and a pointer, so a desktop move writes 12 bytes of fields (the object is 16 with padding), not "a pointer and a size: 16"')
nrvo = [L19['summary']['trap']] + [o['text'] for o in quiz(L19, 'q-return-move')['widget']['options'] if o.get('correct')]
check('FINDING', all('would run none' not in s for s in nrvo), 'l19 summary.trap and q-return-move: eliding a named local (NRVO) is permitted, not required ([class.copy.elision]/1), so `return t;` "would run none" needs "usually"')

# ---------------------------------------------------------------- l21 sizes (Itanium ABI layout; MSVC noted)
def layout(fields, ptr):
    """size of a struct with a vptr first; fields are (size, align)"""
    off, al = ptr, ptr
    for s, a in fields:
        off = (off + a - 1) // a * a + s
        al = max(al, a)
    return (off + al - 1) // al * al
I, Dbl, Ch = (4, 4), (8, 8), (1, 1)
check('l21', layout([I], 4) == 8 and layout([I], 8) == 16, 's0 and quiz: VTick and W are 8 here, 16 on a desktop')
check('l21', layout([I, I], 4) == 12 and layout([I, I], 8) == 16 and layout([I], 8) + 8 == 24, 's2 D is 12 here, 16 under the Itanium ABI (y reuses the tail padding of B), 24 under MSVC (y after the 16-byte B)')
check('l21', layout([Dbl, Dbl], 4) == 24 and layout([Dbl, Dbl], 8) == 24 and 4 + 16 == 20, 's3 Quote is 24 here and on a desktop; slip 20')
check('l21', layout([Ch], 4) == 8 and layout([Ch], 8) == 16 and layout([Dbl], 4) == 16, 'r5 S is 8 (16 desktop); h5 B with a double is 16')
check('l21', [L21['screens'][2]['widget']['answer'], L21['screens'][3]['widget']['answer'], quiz(L21, 'q-sizeof-virtual')['widget']['answer']] == [12, 24, 8], 'size keys 12, 24, 8')

# ---------------------------------------------------------------- l22 undefined behaviour
check('l22', (0 - 1) % 2 ** 32 == 4294967295 == L22['screens'][6]['widget']['answer'] and (0 - 1) % 2 ** 64 == 18446744073709551615, 's6 size() - 1 on an empty vector')
check('l22', int(-7 / 2) == -3 and (2 ** 32 - 1 + 1) % 2 ** 32 == 0 and 1 << 31 == 2147483648, 's2 -7 / 2 is -3; UINT_MAX + 1u is 0; 1u << 31')
check('l22', 5000 * 5000 == 25_000_000 and 25_000_000 * 100 == 2_500_000_000 > 2 ** 31 - 1, 's10 2,500,000,000 pence passes INT_MAX')
check('l22', (2 ** 31 - 1) / 100 == 21474836.47 and (2 ** 32 - 1) / 100 == 42949672.95 and quiz(L22, 'q-int-max-pounds')['widget']['answer'] == 21474836.47, 's10 and quiz: 21,474,836.47 and 42,949,672.95 pounds')
check('l22', 2 ** 53 > 2_500_000_000, 's10 a double holds whole pence exactly up to 2^53')
INT_MAX, INT_MIN = 2 ** 31 - 1, -2 ** 31
def add_overflows(a, b):
    return a > INT_MAX - b if b > 0 else a < INT_MIN - b
ok = True
for t in L22['screens'][4]['widget']['tests']:
    if 'call' in t:
        a, b = (eval(x, {'INT_MAX': INT_MAX, 'INT_MIN': INT_MIN}) for x in re.match(r'add_overflows\((.+), (.+)\)', t['call']).groups())
        ok &= add_overflows(a, b) == t['expect'] == (not INT_MIN <= a + b <= INT_MAX)
        ok &= INT_MIN <= (INT_MAX - b if b > 0 else INT_MIN - b) <= INT_MAX  # the check itself stays in range
check('l22', ok, 's4 every hidden case: the key matches exact arithmetic and the check never leaves int')

# ---------------------------------------------------------------- l23 smart pointers
r = L23['screens'][9]['widget']['rows']
check('l23', [x[1]['answer'] for x in r] == [400000, 200000, 10] and close(200000 * 50e-9 * 1e3, 10), 's9 400,000 and 200,000 allocations, 10 ms saved')
check('l23', L23['screens'][0]['widget']['answer'] == 2 and L23['screens'][1]['widget']['answer'] == 1 and L23['screens'][7]['widget']['answer'] == 1, 's0 two news, s1 one counter, s7 count 1 after the move')

# ---------------------------------------------------------------- reviews and homework
check('r4', item(R4, 'r4-capacity')['widget']['answer'] == 8 and item(R4, 'r4-acc-int')['widget']['answer'] == 8, 'r4 capacity 8; int total of four 2.5s is 8')
tot = 0
for x in [2.5] * 4:
    tot = int(tot + x)
check('r4', tot == 8 and repr((10.1 + 10.2) / 2) == '10.149999999999999' and (10.1 + 10.2) / 2 != 10.15 and 11 <= math.log2(4000) <= 12, 'r4 2, 4, 6, 8; 10.149999999999999; a dozen comparisons for a few thousand symbols')
check('r5', 2_500_000_000 - (2 ** 31 - 1) == 352516353 == item(R5, 'r5-count-and-money')['parts'][1]['widget']['answer'], 'r5 352,516,353 pence over')
def book(lines):
    d = {}
    for ln in lines:
        s, p, q = ln.split()
        d.setdefault(s, []).append((float(p), int(q)))
    out = ''
    for s in sorted(d):
        tr = d[s]
        vw = sum(p * q for p, q in tr) / sum(q for _, q in tr)
        out += f'{s} {len(tr)} {vw:.4f} {min(p for p, _ in tr):.4f} {max(p for p, _ in tr):.4f}\n'
    return out
for t in item(H4, 'h4-vwap-book')['widget']['tests']:
    toks = t['stdin'].split()
    lines = [' '.join(toks[i:i + 3]) for i in range(0, len(toks), 3)]
    check('h4', book(lines) == t['expect'], f'h4-vwap-book {toks[:3]}')
check('h4', close((72.1 + 72.5 + 72.3) / 3, 72.3) and close((4.75 * 1000 + 4.80 * 3000 + 4.70 * 1000) / 5000, 4.77), 'h4 unweighted 72.3; BP 4.77')
px = [100.0, 120.0, 90.0, 130.0, 104.0]
def mdd(px, v=0):
    peak, worst = px[0], 0.0
    for p in px:
        if v != 1:
            peak = max(peak, p)
        fall = peak - p if v == 2 else (peak - p) / peak
        worst = fall if v == 4 else max(worst, fall)
    return worst
check('h4', close(mdd(px), 0.25) and close(mdd(px, 4), 0.2) and close(mdd(px, 2), 30.0) and close(mdd(px, 1), 0.1), 'h4 drawdown 0.25; the planted versions give 0.2, 30 and 0.1')
check('h4', doubling(150, 100)[0] == 200 == item(H4, 'h4-reserve-grow')['widget']['answer'], 'h4 reserve(100) then 150 pushes: capacity 200')
check('h4', sorted([700, 100, 400, 301])[1:3] == [301, 400] and (301 + 400) / 2 == 350.5 and (2000000000 + 1999999999) / 2 == 1999999999.5 and 2000000000 + 1999999999 > 2 ** 31 - 1, 'h4 medians 350.5 and 1999999999.5; the int sum overflows')
check('h5', 1000 * 1000 * 8 == 8_000_000 and doubling(1000)[1] == 11 and doubling(1000)[0] == 1024, 'h5 8 MB; 1,000 pushes allocate 11 times, capacity 1,024')
ex = item(H5, 'h5-members-table')['explain']['text']
check('FINDING', 'leaves the constructors deleted' not in ex, 'h5-members-table explain: after a lone move assignment the copy constructor is deleted and no move constructor is declared (the default constructor is untouched); "leaves the constructors deleted" contradicts "deleted, not absent"')
fb = L16['screens'][3]['feedback']['byKey']['test-1']
check('FINDING', '100,' in fb or 'got 100 ' in fb or 'got 100,' in fb, 'l16 s3 feedback test-1: both totals started at the int 0 (the commonest form of the slip) fail test 1 with 100, which the line does not name')

print(f'part A: {n_ok} checks passed, {len(bad)} failed')

# ---------------------------------------------------------------- part B: C++ through the page's own grader
def cpp_part(pkgs, jobs):
    run = os.path.join(HERE, 'cpp-L4-5-concepts-r2-run.mjs')
    procs = [subprocess.Popen(['node', run, '--app', APP, '--pkgs', pkgs, '--shard', f'{i}/{jobs}'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) for i in range(jobs)]
    okc = 0
    for p in procs:
        out, _ = p.communicate()
        for ln in out.splitlines():
            if ln.startswith('ok  '):
                okc += 1
            elif ln.startswith('FAIL'):
                tag = ln.split()[1]
                bad.append((tag, ln[5:]))
                print(ln)
            elif ln.startswith('shard') or ln.startswith('note') or 'yowasp' in ln:
                continue
            elif ln.strip():
                bad.append(('RUNNER', ln))
                print('FAIL RUNNER ' + ln)
        if p.returncode not in (0, 1):
            bad.append(('RUNNER', f'node exited {p.returncode}'))
    print(f'part B: {okc} checks passed')


if '--no-cpp' not in sys.argv:
    pkgs = sys.argv[sys.argv.index('--pkgs') + 1] if '--pkgs' in sys.argv else os.environ.get('ZQ_LOCAL_CDN', '')
    jobs = int(sys.argv[sys.argv.index('--jobs') + 1]) if '--jobs' in sys.argv else 3
    if not pkgs or not os.path.isdir(os.path.join(pkgs, 'yowasp-clang-21.1.4-3')):
        print('setup: no local CDN with yowasp-clang-21.1.4-3 (give --pkgs or ZQ_LOCAL_CDN, or --no-cpp for part A alone)')
        sys.exit(2)
    cpp_part(pkgs, jobs)

findings = [b for b in bad if b[0] == 'FINDING']
others = [b for b in bad if b[0] != 'FINDING']
print(f'{len(findings)} FINDING checks failing (content defects, see docs/reviews/audit-cpp-4-5-r2.md); {len(others)} other failures')
sys.exit(1 if bad else 0)
