#!/usr/bin/env python3
"""Concept checks for systems L1 (l1 to l5, review-1, homework-1): exact simulations of the
cache, page-table, struct-layout and branch-predictor claims, g++ runs of every C++ code item
(solution must pass every hidden test, the starter must fail at least one) and a few compiled
checks (sizeof, cmov at -O1). Run from the repo root: python3 -I docs/reports/systems-L1-concepts.py
Each assert names the ledger row (file: JSON path) in docs/reports/audit-systems-1-3-ledger.md."""
import json, math, os, random, shutil, subprocess, sys, tempfile
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COURSE = os.path.join(ROOT, 'app', 'content', 'courses', 'systems')
PASSED = []

def load(name):
    with open(os.path.join(COURSE, name + '.json')) as f:
        return json.load(f)

def check(name, cond, msg):
    assert cond, f'{name}: {msg}'
    PASSED.append(name)

# ---------------------------------------------------------------- C++ runner for code widgets
CXX = shutil.which('g++') or shutil.which('clang++')

def cpp_lit(v, typ=None):
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, int):
        return f'{v}LL' if abs(v) > 2**31 - 1 else str(v)
    if isinstance(v, float):
        return repr(v)
    if isinstance(v, str):
        return 'std::string("' + v.replace('\\', '\\\\').replace('"', '\\"') + '")'
    if isinstance(v, list):
        if typ is None:
            if v and all(isinstance(x, str) for x in v):
                typ = 'std::vector<std::string>'
            elif v and all(isinstance(x, list) for x in v):
                typ = 'std::vector<std::vector<double>>'
            else:
                typ = 'std::vector<int>'
        return typ + '{' + ', '.join(cpp_lit(x) for x in v) + '}'
    raise TypeError(repr(v))

def canon(v):
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, list):
        return '[' + ','.join(canon(x) for x in v) + ']'
    if isinstance(v, float):
        return repr(v)
    return str(v)

HARNESS_HEAD = '#include <iostream>\n#include <string>\n#include <vector>\n'
HARNESS_SHOW = '''
template <class T> void show(const T& v) { std::cout << v; }
void show(bool v) { std::cout << (v ? "true" : "false"); }
void show(const std::string& s) { std::cout << s; }
template <class T> void show(const std::vector<T>& v) {
    std::cout << '['; for (size_t i = 0; i < v.size(); ++i) { if (i) std::cout << ','; show(v[i]); } std::cout << ']'; }
'''

def run_cpp(widget, code):
    """Compile prelude + code + a main that prints every test result; return (ok_compile, lines)."""
    tests = widget['tests']
    body = []
    for t in tests:
        setup = t.get('setup', '')
        if 'args' in t:
            types = t.get('types') or [None] * len(t['args'])
            call = t['call'] + '(' + ', '.join(cpp_lit(a, ty) for a, ty in zip(t['args'], types)) + ')'
        else:
            call = t['call']
        body.append('    { ' + setup + ' show(' + call + '); std::cout << "\\n"; }')
    src = (HARNESS_HEAD + widget.get('prelude', '') + '\n' + code + '\n' + HARNESS_SHOW
           + 'int main() {\n' + '\n'.join(body) + '\n    return 0;\n}\n')
    d = tempfile.mkdtemp()
    path = os.path.join(d, 'main.cpp')
    with open(path, 'w') as f:
        f.write(src)
    exe = os.path.join(d, 'a.out')
    r = subprocess.run([CXX, '-std=c++17', '-O1', '-w', '-o', exe, path], capture_output=True, text=True)
    if r.returncode != 0:
        return False, r.stderr
    out = subprocess.run([exe], capture_output=True, text=True, timeout=120).stdout
    return True, out.splitlines()

def code_item(name, widget):
    tests = widget['tests']
    expected = [canon(t.get('expect', [])) for t in tests]
    ok, lines = run_cpp(widget, widget['solution'])
    check(name + ':solution_compiles', ok, f'solution does not compile: {lines[:600]}')
    bad = [(i, e, l) for i, (e, l) in enumerate(zip(expected, lines)) if e != l]
    check(name + ':solution_passes', len(lines) == len(tests) and not bad,
          f'solution fails tests {bad[:3]}')
    ok2, lines2 = run_cpp(widget, widget['starter'])
    fails = (not ok2) or any(e != l for e, l in zip(expected, lines2)) or len(lines2) != len(tests)
    check(name + ':starter_fails', fails, 'the starter passes every hidden test')

# ---------------------------------------------------------------- L1 lesson 1: latency numbers
def haversine(a, b):
    R = 6371.0
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))

def l1_latency():
    table = {'reg': 0.3e-9, 'l1': 1e-9, 'l2': 4e-9, 'l3': 20e-9, 'dram': 100e-9, 'nvme': 100e-6,
             'dc': 500e-6, 'seek': 10e-3, 'ny': 60e-3}
    order = ['reg', 'l1', 'dram', 'nvme', 'seek', 'ny']
    check('L1:order', order == sorted(order, key=table.get), 'l1 screens[0] order')
    order2 = ['reg', 'l2', 'dram', 'nvme', 'dc', 'seek']
    check('L1:order_review', order2 == sorted(order2, key=table.get), 'review-1 items[0] order')
    # Dean's table (2009 values) within a factor of 3 of each round figure that it lists
    dean = {'l1': 0.5e-9, 'l2': 7e-9, 'dram': 100e-9, 'nvme': 150e-6, 'dc': 500e-6, 'seek': 10e-3}
    for k, v in dean.items():
        check(f'L1:dean_{k}', 1 / 3 <= table[k] / v <= 3, f'l1 figure {k} off Dean by more than 3x')
    lon, nyc, fra = (51.5074, -0.1278), (40.7128, -74.0060), (50.1109, 8.6821)
    check('L1:greatcircle', abs(haversine(lon, nyc) - 5570) < 30 and abs(haversine(lon, fra) - 640) < 15,
          'l1 distances 5,570 km and 640 km')
    check('L1:powers', math.log10(10e-3 / 1e-9) == 7, 'l1 screens[1] seven powers of ten')
    check('L1:stretch', 100_000 == 86400 + 3 * 3600 + 46 * 60 + 40 and abs(1e7 / 86400 - 115.7) < 0.05
          and abs(6e7 / 86400 / 365.25 - 1.9) < 0.05, 'l1 screens[2] explain')
    check('L1:fibre', abs(1280 / 200000 * 1e3 - 6.4) < 1e-9 and abs(1280 / 299792 * 1e3 - 4.27) < 0.005
          and abs(11140 / 200000 * 1e3 - 55.7) < 1e-9 and abs(5570 / 299792 * 1e3 - 18.58) < 0.005,
          'l1 screens[4], [6], [10] times')
    check('L1:drill', [5000 // 100, 1000 // 1, round(math.log10(100_000)), 60000 // 500, 10_000 // 100]
          == [50, 1000, 5, 120, 100], 'l1 screens[8] drill')
    check('L1:hw1_follow', (100_000 // 20, 60_000_000 // 100, 3 * 100 + 100_000 // 1000) == (5000, 600_000, 400),
          'homework-1 items[0]')

# ---------------------------------------------------------------- L1 lesson 2: caches
def misses(addresses, lines, ways, line_bytes=64):
    """LRU set-associative cache; addresses in bytes; returns miss count (no prefetcher)."""
    sets = lines // ways
    cache = [OrderedDict() for _ in range(sets)]
    m = 0
    for a in addresses:
        line = a // line_bytes
        s = cache[line % sets]
        if line in s:
            s.move_to_end(line)
        else:
            m += 1
            if len(s) == ways:
                s.popitem(last=False)
            s[line] = True
    return m

def l2_caches():
    check('L2:seq', misses([8 * i for i in range(32)], 512, 8) == 4, 'l2 screens[0]: 4 misses')
    sweep5 = [64 * i for i in range(5)] * 3
    check('L2:lru_5_in_4', misses(sweep5, 4, 4) == 15, 'l2 screens[1], [4]: 15 misses')
    check('L2:lru_fits', misses([64 * i for i in range(4)] * 3, 4, 4) == 4 and misses([64 * i for i in range(3)] * 4, 4, 4) == 3,
          'l2 screens[7] row 3 and quiz[3]')
    ab = [x for i in range(8) for x in (8 * i, 256 + 8 * i)]
    ab320 = [x for i in range(8) for x in (8 * i, 320 + 8 * i)]
    check('L2:conflict', (misses(ab, 4, 1), misses(ab, 4, 2), misses(ab320, 4, 1)) == (16, 2, 2), 'l2 screens[2]')
    seq = [0, 256, 512, 0]
    check('L2:ways', [misses(seq, 8, w) for w in (1, 2, 4, 8)] == [4, 4, 3, 3], 'l2 screens[3]')
    # 64 x 64 doubles, column walk, 512-line 8-way cache
    col64 = [8 * (i * 64 + j) for j in range(64) for i in range(64)]
    check('L2:matrix64', misses(col64, 512, 8) == 512, 'l2 screens[5]: 512 misses by columns')
    check('L2:set', (4160 // 64) % 64 == 1 and (448 // 64) % 4 == 3, 'l2 screens[6], quiz[1]')
    drill = [misses([8 * 4 * i for i in range(16)], 512, 8), misses([8 * 3 * i for i in range(32)], 512, 8),
             misses(sweep5, 4, 4), misses([64 * i for i in range(4)] * 3, 4, 4), misses(seq, 8, 2), misses(seq, 8, 4)]
    check('L2:drill', drill == [8, 12, 15, 4, 4, 3], f'l2 screens[7]: {drill}')
    check('L2:ints', misses([4 * i for i in range(64)], 512, 8) == 4, 'l2 quiz[0]')
    # 1000 x 1000 doubles row-outer and column-outer (L1 only: 512 lines, 8 ways)
    n = 1000
    rows = (8 * (i * n + j) for i in range(n) for j in range(n))
    cols = (8 * (i * n + j) for j in range(n) for i in range(n))
    check('L2:column_walk', misses(rows, 512, 8) == 125_000 and misses(cols, 512, 8) == 1_000_000,
          'l2 screens[8]: 125,000 and 1,000,000 L1 misses')

def l1_review_hw_caches():
    check('L1:drill_review', misses([8 * 5 * i for i in range(24)], 512, 8) == 15, 'review-1 items[2]')
    n = 1200
    rows = (8 * (i * n + j) for i in range(n) for j in range(n))
    cols = (8 * (i * n + j) for j in range(n) for i in range(n))
    check('L1:matrix_1200', misses(rows, 512, 8) == 180_000 and misses(cols, 512, 8) == 1_440_000,
          'homework-1 items[3] parts 0 and 1')
    col = [8 * (i * 64 + j) for j in range(64) for i in range(32)]
    check('L1:matrix_32x64', misses(col, 512, 8) == 256, 'homework-1 items[3] part 4')

def l1_tlb_random():
    rng = random.Random(7)
    def hit_rate(pages, entries, n=200_000):
        tlb = OrderedDict(); hits = 0
        for _ in range(n):
            p = rng.randrange(pages)
            if p in tlb:
                hits += 1; tlb.move_to_end(p)
            else:
                if len(tlb) == entries: tlb.popitem(last=False)
                tlb[p] = True
        return hits / n
    h4k, h2m = hit_rate(65536, 64), hit_rate(128, 64)
    check('L1:tlb_random', abs(h4k - 64 / 65536) < 0.0005 and abs(h2m - 0.5) < 0.01,
          f'homework-1 items[5]: hit rates {h4k:.5f} and {h2m:.3f}')
    cost4k = 100 + (1 - 64 / 65536) * 30
    check('L1:tlb_cost', abs(cost4k - 129.97) < 0.005 and abs((cost4k - 115) / cost4k - 0.1152) < 0.0005,
          'homework-1 items[5] parts 1 to 3')

# ---------------------------------------------------------------- L1 lesson 3: virtual memory
def translate(frames, v):
    p, o = divmod(v, 4096)
    if p >= len(frames) or frames[p] is None or frames[p] < 0:
        return -1
    return frames[p] * 4096 + o

def l3_vm():
    check('L3:translate', translate([7, -1, 9], 0x2A7C) == 39548 and translate([7, -1, 9], 8195) == 36867
          and translate([5, 2, -1, 8], 15120) == 35600 and translate([5, 2, -1, 8], 8192) == -1
          and translate([3, 6], 4100) == 24580 and translate([7, 3, 12, -1], 10812) == 51772,
          'l3 screens[0], [8], [9], quiz[1]; review-1 items[4]')
    v = 0x00007F3A1C2D5E48
    fields = [(v >> 39) & 0x1FF, (v >> 30) & 0x1FF, (v >> 21) & 0x1FF, (v >> 12) & 0x1FF, v & 0xFFF]
    check('L3:bits', fields == [254, 232, 225, 213, 3656], f'l3 screens[2]: {fields}')
    check('L3:tlb', (64 * 4, 2**26 // 2**12, 64 / 16384, 2**26 // 2**21) == (256, 16384, 0.00390625, 32)
          and abs(64 / 16384 - 0.0039) < 0.0001, 'l3 screens[3]')
    check('L3:drill', (1536 * 4 // 1024, 3 * 2**30 // 2**12, 3 * 2**30 // 2**12 / 1000, 3072 // 2)
          == (6, 786432, 786.432, 1536), 'l3 screens[9], [10]')
    check('L3:faults', (2**30 // 2**12, 2**29 // 2**12, 2**31 // 2**12) == (262144, 131072, 524288),
          'l3 screens[5], quiz[3]; review-1 items[5]')
    check('L3:tib', 2**48 // 2**40 == 256, 'l3 screens[6]')

# ---------------------------------------------------------------- L1 lesson 4: object layout (g++)
LAYOUT_SRC = r'''
#include <cstddef>
#include <cstdint>
#include <cstdio>
struct S { uint8_t a; double b; uint8_t c; };
struct S2 { double b; uint8_t a; uint8_t c; };
struct S3 { uint8_t a; uint8_t c; double b; };
struct Order { uint8_t type; uint32_t seq; uint8_t side; uint32_t id; uint16_t instrument; uint32_t qty; int32_t price; uint32_t time; };
struct OrderS { uint32_t seq; uint32_t id; uint32_t qty; int32_t price; uint32_t time; uint16_t instrument; uint8_t type; uint8_t side; };
struct OrderF { uint32_t seq; uint32_t id; uint32_t qty; int32_t price; uint32_t time; uint16_t instrument; uint8_t type; uint8_t side; uint16_t flags; };
struct T { char a; double b; char c; };
struct A { uint8_t a; uint16_t b; uint32_t c; double d; uint8_t e; uint16_t f; uint32_t g; double h; };
struct AS { double d; double h; uint32_t c; uint32_t g; uint16_t b; uint16_t f; uint8_t a; uint8_t e; };
struct U { uint16_t a; uint8_t b; };
struct G { uint32_t a; uint16_t b; double c; };
struct D1 { uint8_t a; uint16_t b; uint8_t c; uint32_t d; uint8_t e; };
struct D1S { uint32_t d; uint16_t b; uint8_t a; uint8_t c; uint8_t e; };
struct D2 { uint8_t a; double b; uint8_t c; double d; uint8_t e; double f; };
struct D2S { double b; double d; double f; uint8_t a; uint8_t c; uint8_t e; };
struct D4 { double a; uint32_t b; };
struct Q { uint8_t a; uint32_t b; uint16_t c; };
struct QS { uint32_t b; uint16_t c; uint8_t a; };
struct P { uint8_t a; uint64_t b; uint8_t c; uint16_t d; };
struct PS { uint64_t b; uint16_t d; uint8_t a; uint8_t c; };
struct E {};
int main() {
    std::printf("%zu %zu %zu %zu %zu %zu %zu %zu %zu %zu %zu %zu %zu %zu %zu %zu %zu %zu %zu %zu %zu %zu\n",
        sizeof(S), sizeof(S2), sizeof(S3), sizeof(Order), sizeof(OrderS), sizeof(OrderF), sizeof(T), sizeof(A), sizeof(AS),
        sizeof(U), sizeof(G), sizeof(D1), sizeof(D1S), sizeof(D2), sizeof(D2S), sizeof(D4), sizeof(Q), sizeof(QS),
        sizeof(P), sizeof(PS), sizeof(E), (size_t)0);
    std::printf("%zu %zu %zu\n", offsetof(S, a), offsetof(S, b), offsetof(S, c));
    std::printf("%zu %zu %zu %zu %zu %zu %zu %zu\n", offsetof(Order, type), offsetof(Order, seq), offsetof(Order, side), offsetof(Order, id),
        offsetof(Order, instrument), offsetof(Order, qty), offsetof(Order, price), offsetof(Order, time));
    std::printf("%zu %zu %zu %zu %zu %zu %zu %zu\n", offsetof(OrderS, seq), offsetof(OrderS, id), offsetof(OrderS, qty), offsetof(OrderS, price),
        offsetof(OrderS, time), offsetof(OrderS, instrument), offsetof(OrderS, type), offsetof(OrderS, side));
    std::printf("%zu %zu %zu %zu %zu %zu %zu %zu\n", offsetof(P, a), offsetof(P, b), offsetof(P, c), offsetof(P, d),
        offsetof(PS, b), offsetof(PS, d), offsetof(PS, a), offsetof(PS, c));
    std::printf("%zu %zu %zu\n", offsetof(G, a), offsetof(G, b), offsetof(G, c));
    return 0;
}
'''

def l4_layout():
    d = tempfile.mkdtemp()
    src = os.path.join(d, 'layout.cpp')
    with open(src, 'w') as f:
        f.write(LAYOUT_SRC)
    exe = os.path.join(d, 'layout')
    r = subprocess.run([CXX, '-std=c++17', '-O0', '-w', '-o', exe, src], capture_output=True, text=True)
    check('L1:sizeof_compiles', r.returncode == 0, r.stderr[:500])
    out = subprocess.run([exe], capture_output=True, text=True).stdout.splitlines()
    sizes = list(map(int, out[0].split()))
    want = [24, 16, 16, 32, 24, 28, 24, 32, 32, 4, 16, 16, 12, 48, 32, 16, 12, 8, 24, 16, 1, 0]
    check('L1:sizeof', sizes == want, f'l4 sizeof claims: got {sizes}, lesson says {want}')
    check('L1:offsets_S', out[1] == '0 8 16', f'l4 screens[2]: {out[1]}')
    check('L1:offsets_Order', out[2] == '0 4 8 12 16 20 24 28' and out[3] == '0 4 8 12 16 20 22 23',
          f'l4 screens[3], [4]: {out[2]} / {out[3]}')
    check('L1:offsets_P', out[4] == '0 8 16 18 0 8 10 11', f'homework-1 items[4]: {out[4]}')
    check('L1:offsets_G', out[5] == '0 4 8', f'l4 screens[8]: {out[5]}')
    # model rule: offset = a*ceil(e/a), size = amax*ceil(end/amax); sorted descending is optimal for powers of two
    def struct_size(sizes):
        off, widest = 0, 1
        for s in sizes:
            off = (off + s - 1) // s * s + s
            widest = max(widest, s)
        return (off + widest - 1) // widest * widest
    import itertools
    for sz in ([1, 8, 1], [1, 4, 1, 4, 2, 4, 4, 4], [1, 2, 1, 4, 1], [4, 1, 2, 1, 8], [1, 2, 4, 8, 1, 2, 4, 8]):
        best = min(struct_size(p) for p in set(itertools.permutations(sz)))
        check('L1:sort_optimal', struct_size(sorted(sz, reverse=True)) == best, f'l4 screens[8]: sorting is not optimal for {sz}')

def l4_straddle():
    def crossing(size, count, line=64):
        return [k for k in range(count) if (k * size) // line != (k * size + size - 1) // line]
    check('L1:straddle', crossing(24, 8) == [2, 5] and crossing(32, 8) == [] and crossing(40, 8) == [1, 3, 4, 6],
          'l4 screens[10]; review-1 items[8]')

# ---------------------------------------------------------------- L1 lesson 5: branches
def twobit(history, start=1):
    c, wrong = start, 0
    for ch in history:
        t = ch == 'T'
        if (c >= 2) != t:
            wrong += 1
        c = min(3, c + 1) if t else max(0, c - 1)
    return wrong

def onebit(history):
    last, wrong = False, 0
    for ch in history:
        t = ch == 'T'
        if last != t:
            wrong += 1
        last = t
    return wrong

def l5_branches():
    check('L1:twobit', (twobit('TTTNNN'), twobit('TTTNTTTN'), twobit('TTTTTTTN' * 2), twobit('TTN' * 10), twobit('NTTT'),
                        twobit('TNTNTNTN'), twobit('TTN' * 3), twobit('NNNT'), twobit('TTTN' * 4)) == (3, 3, 3, 11, 2, 8, 4, 1, 5),
          'l5 screens[0], [1], [8], quiz[0]; review-1 items[7]')
    check('L1:onebit', onebit('TTN' * 3) == 6 and onebit('TTTN' * 4) == 8, 'l5 screens[8] row 4; review-1 items[7] slip')
    rng = random.Random(1)
    hist = ''.join('T' if rng.randrange(256) >= 128 else 'N' for _ in range(10_000))
    w = twobit(hist)
    check('L1:random_branch', 0.45 * 10_000 < w < 0.55 * 10_000 and twobit(''.join(sorted(hist))) == 2,
          f'l5 screens[2]: {w} wrong of 10,000; sorted gives {twobit("".join(sorted(hist)))}')
    check('L1:mask', (-(200 >= 128)) == -1 and (200 & -1) == 200 and (-(100 >= 128)) == 0, 'l5 screens[3]')
    check('L1:costs', abs(1e6 * 0.5 * 5e-9 - 2.5e-3) < 1e-12 and abs(1e6 * 0.1 * 5e-9 - 0.5e-3) < 1e-12
          and abs(0.3 * 5 - 1.5) < 1e-12 and abs(1e7 * 0.5 * 5e-9 - 25e-3) < 1e-12 and abs(0.001 * 5 - 0.005) < 1e-12,
          'l5 screens[2], [7], [9], quiz[1], quiz[3]')
    # cmov at -O1 in both compilers (l5 screens[5])
    src = ('#include <cstdint>\nlong sum_branch(const uint8_t* a, int n) { long s = 0; '
           'for (int i = 0; i < n; ++i) if (a[i] >= 128) s += a[i]; return s; }\n')
    d = tempfile.mkdtemp()
    p = os.path.join(d, 'b.cpp')
    with open(p, 'w') as f:
        f.write(src)
    for cc in ('g++', 'clang++'):
        if shutil.which(cc):
            asm = subprocess.run([cc, '-std=c++17', '-O1', '-S', '-o', '-', p], capture_output=True, text=True).stdout
            check(f'L1:cmov_{cc}', 'cmov' in asm, f'l5 screens[5]: {cc} -O1 emits no cmov')

def l1_code_items():
    code_item('L3:code_translate', load('l3-virtual-memory')['screens'][4]['widget'])
    code_item('L1:code_struct_size', load('l4-object-layout')['screens'][5]['widget'])
    code_item('L1:code_mispredicts', load('l5-branches')['screens'][6]['widget'])
    code_item('L1:code_count_misses', load('homework-1')['items'][1]['widget'])

if __name__ == '__main__':
    assert CXX, 'no C++ compiler found (g++ or clang++)'
    l1_latency()
    l2_caches()
    l1_review_hw_caches()
    l1_tlb_random()
    l3_vm()
    l4_layout()
    l4_straddle()
    l5_branches()
    l1_code_items()
    print(f'systems L1 concepts: {len(PASSED)} checks passed')
