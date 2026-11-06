#!/usr/bin/env python3
"""Concept checks for systems L3 (l11 to l14, review-3, homework-3): exact checks of the system-call,
stream-framing, sequence-gap and wire-format claims (Python struct), a Monte Carlo of the A/B feed
loss figure, a g++ check of the host struct sizes, g++ runs of the C++ code items and a Python run of
the feed.hex homework item (solution passes every hidden test, the starter fails at least one).
Run from the repo root: python3 -I docs/reports/systems-L3-concepts.py
Each assert names the ledger row (file: JSON path) in docs/reports/audit-systems-1-3-ledger.md."""
import json, math, os, random, shutil, struct, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COURSE = os.path.join(ROOT, 'app', 'content', 'courses', 'systems')
PASSED = []

def load(name):
    with open(os.path.join(COURSE, name + '.json')) as f:
        return json.load(f)

def check(name, cond, msg):
    assert cond, f'{name}: {msg}'
    PASSED.append(name)

# ---------------------------------------------------------------- C++ runner (as in the L1 and L2 scripts)
CXX = shutil.which('g++') or shutil.which('clang++')

def cpp_lit(v, typ=None):
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, int):
        return f'{v}LL' if abs(v) > 2**31 - 1 else str(v)
    if isinstance(v, str):
        return 'std::string("' + v.replace('\\', '\\\\').replace('"', '\\"') + '")'
    if isinstance(v, list):
        typ = typ or ('std::vector<std::string>' if v and all(isinstance(x, str) for x in v) else 'std::vector<int>')
        return typ + '{' + ', '.join(cpp_lit(x) for x in v) + '}'
    raise TypeError(repr(v))

def canon(v):
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, list):
        return '[' + ','.join(canon(x) for x in v) + ']'
    return str(v)

HARNESS_SHOW = '''
template <class T> void show(const T& v) { std::cout << v; }
void show(bool v) { std::cout << (v ? "true" : "false"); }
void show(const std::string& s) { std::cout << s; }
template <class T> void show(const std::vector<T>& v) {
    std::cout << '['; for (size_t i = 0; i < v.size(); ++i) { if (i) std::cout << ','; show(v[i]); } std::cout << ']'; }
'''

def run_cpp(widget, code):
    body = []
    for t in widget['tests']:
        if 'args' in t:
            types = t.get('types') or [None] * len(t['args'])
            call = t['call'] + '(' + ', '.join(cpp_lit(a, ty) for a, ty in zip(t['args'], types)) + ')'
        else:
            call = t['call']
        body.append('    { ' + t.get('setup', '') + ' show(' + call + '); std::cout << "\\n"; }')
    src = ('#include <iostream>\n#include <string>\n#include <vector>\n' + widget.get('prelude', '') + '\n' + code
           + '\n' + HARNESS_SHOW + 'int main() {\n' + '\n'.join(body) + '\n    return 0;\n}\n')
    d = tempfile.mkdtemp()
    path = os.path.join(d, 'main.cpp')
    with open(path, 'w') as f:
        f.write(src)
    exe = os.path.join(d, 'a.out')
    r = subprocess.run([CXX, '-std=c++17', '-O1', '-w', '-o', exe, path], capture_output=True, text=True)
    if r.returncode != 0:
        return False, r.stderr
    return True, subprocess.run([exe], capture_output=True, text=True, timeout=120).stdout.splitlines()

def code_item(name, widget):
    expected = [canon(t.get('expect', [])) for t in widget['tests']]
    ok, lines = run_cpp(widget, widget['solution'])
    check(name + ':solution_compiles', ok, f'solution does not compile: {str(lines)[:600]}')
    bad = [(i, e, l) for i, (e, l) in enumerate(zip(expected, lines)) if e != l]
    check(name + ':solution_passes', len(lines) == len(expected) and not bad, f'solution fails {bad[:3]}')
    ok2, lines2 = run_cpp(widget, widget['starter'])
    fails = (not ok2) or len(lines2) != len(expected) or any(e != l for e, l in zip(expected, lines2))
    check(name + ':starter_fails', fails, 'the starter passes every hidden test')

# ---------------------------------------------------------------- l11: system calls and switches
def syscalls():
    MiB, KiB = 2**20, 2**10
    check('L3:syscalls', (MiB // 64, MiB // (4 * KiB), MiB // (64 * KiB)) == (16384, 256, 16)
          and abs(16384 * 0.2 - 3276.8) < 1e-9 and abs(256 * 0.2 - 51.2) < 1e-9
          and (4 * MiB // (4 * KiB), 8 * MiB // (64 * KiB)) == (1024, 128) and abs(1024 * 0.2 - 204.8) < 1e-9
          and (2 * MiB // (32 * KiB)) * 0.2 == 12.8 and abs((6 * MiB // (8 * KiB)) * 0.2 - 153.6) < 1e-9
          and abs((5 * MiB // (2 * KiB)) * 0.2 - (5 * MiB // (160 * KiB)) * 0.2 - 505.6) < 1e-9,
          'l11 screens[1], [2], [8], quiz[0]; review-3 items[0]; homework-3 items[6]')
    check('L3:wakes', abs(100_000 * 5e-6 - 0.5) < 1e-12 and abs(250_000 * 5e-6 - 1.25) < 1e-12 and abs(50_000 * 5e-6 - 0.25) < 1e-12
          and 500_000 * 20e-9 == 0.01, 'l11 screens[3], [6], [8], quiz[3]')
    check('L3:datagram', 1500 - 20 - 8 == 1472 and 1472 // 24 == 61 and 1472 - 61 * 24 == 8 and math.ceil(200_000 / 61) == 3279
          and abs(200_000 * 0.2e-6 - 0.04) < 1e-12, 'l11 screens[9]; l14 screens[3]')
    check('L3:kernel_budget', (1_000_000 // 12, 1_000_000 // 3, 300_000 * 12e-6, 300_000 // 40, 7500 * 90e-6)
          == (83333, 333333, 3.6, 7500, 0.675), 'homework-3 items[4]')

# ---------------------------------------------------------------- l12: streams and framing
def carry(chunks, frame=24):
    held, parsed, per = 0, 0, []
    for c in chunks:
        held += c
        n, held = divmod(held, frame)
        parsed += n
        per.append(n)
    return parsed, held, per

def chunks():
    check('L3:chunks', carry([100]) == (4, 4, [4]) and carry([1000]) == (41, 16, [41])
          and carry([100, 50, 24, 23, 1]) == (8, 6, [4, 2, 1, 1, 0]) and carry([50, 50, 50]) == (6, 6, [2, 2, 2])
          and carry([250]) == (10, 10, [10]) and carry([60, 50, 60]) == (7, 2, [2, 2, 3]) and carry([3000]) == (125, 0, [125])
          and 1400 // 24 == 58 and 1400 - 58 * 24 == 8,
          'l12 screens[2], [7], quiz[0]; l14 screens[8], quiz[3]; review-3 items[2]')
    check('L3:polling', 50 / 0.2 == 250 and 1000 / 0.2 == 5000 and 10 / 5 == 2 and 1 / 5 == 0.2, 'l12 screens[1], [3], quiz[2]')

# ---------------------------------------------------------------- l13: TCP, UDP, gaps
def missing(seqs):
    seen = set(seqs)
    return sorted(set(range(1, max(seen) + 1)) - seen) if seen else []

def gaps():
    check('L3:gaps', missing([2, 1, 4, 4, 5]) == [3] and missing([1, 2, 4, 5]) == [3] and missing([1, 5]) == [2, 3, 4]
          and missing([3, 1, 2, 6, 5]) == [4] and missing([1, 2, 3, 7, 8, 10]) == [4, 5, 6, 9] and missing([2, 4, 5]) == [1, 3]
          and missing([2, 3, 6, 9, 4, 8]) == [1, 5, 7] and missing([1, 3, 2]) == [],
          'l13 screens[6], [8], quiz[2]; review-3 items[5]')
    check('L3:handshake', (3 * 30, 3 * 50, 3 * 18, 3 * 40 - 40) == (90, 150, 54, 80), 'l13 screens[2], quiz[0]; review-3 items[4]; homework-3 items[0]')
    check('L3:hol', (100_000 * 0.2, 100_000 * 0.0005, 40_000 * 0.0025, 40_000 * 0.2, 30_000 * 0.2) == (20000, 50, 100, 8000, 6000),
          'l13 screens[1]; homework-3 items[0], [2]')
    check('L3:multicast', (50 * 1000 * 100, 1000 * 100, 10 * 1000 * 200, 20 * 2000 * 150, 2000 * 150, 100 * 500 * 200)
          == (5_000_000, 100_000, 2_000_000, 6_000_000, 300_000, 10_000_000) and 5_000_000 * 8 / 1e6 == 40,
          'l13 screens[3], quiz[3]; homework-3 items[0], [2]')
    # A/B arbitration loss: the lesson's 100 (and 400, 25) are expectations of a binomial, not exact counts
    rng = random.Random(11)
    def both_lost(n, p, reps):
        out = []
        for _ in range(reps):
            # binomial(n, p*p) by inversion on the Poisson approximation is good enough at these sizes; use exact sampling
            lam = n * p * p
            k, s, u = 0, math.exp(-lam), rng.random()
            cdf = s
            while u > cdf:
                k += 1; s *= lam / k; cdf += s
            out.append(k)
        return out
    a = both_lost(1_000_000, 0.01, 400)
    mean, sd = sum(a) / len(a), (sum((x - sum(a) / len(a)) ** 2 for x in a) / len(a)) ** 0.5
    check('L3:ab_loss', abs(mean - 100) < 2 and 7 < sd < 13 and len(set(a)) > 20,
          f'l13 screens[4]: both-feed loss has mean {mean:.1f} and sd {sd:.1f}, so 100 is an expectation, not a count')
    b = both_lost(1_000_000, 0.02, 400)
    check('L3:ab_loss_review', abs(sum(b) / len(b) - 400) < 4, f'review-3 items[8]: mean {sum(b)/len(b):.1f}')
    check('L3:ab_loss_hw', 1_000_000 * 0.005 ** 2 == 25 and 1_000_000 * 0.005 == 5000, 'homework-3 items[2] model')

# ---------------------------------------------------------------- l14: wire bytes
def wire_bytes():
    check('L3:seq70000', struct.pack('>I', 70000) == bytes([0, 1, 0x11, 0x70]) and struct.pack('<I', 70000) == bytes([0x70, 0x11, 1, 0])
          and struct.pack('>I', 123456789) == bytes.fromhex('075bcd15'), 'l14 screens[0], [4]')
    check('L3:endian258', int.from_bytes(bytes([2, 1]), 'little') == 258 and int.from_bytes(bytes([2, 1]), 'big') == 513, 'l14 screens[1]')
    p = struct.pack('>i', 10275)
    check('L3:price_bytes', p == bytes.fromhex('00002823') and p[2] == 40 and p[3] == 35 and struct.pack('>i', -25)[3] == 231
          and struct.pack('>I', 36_000_000) == bytes.fromhex('02255100') and struct.pack('>I', 36_000_000)[1] == 37
          and struct.unpack('>i', bytes.fromhex('80000000'))[0] == -2**31 and struct.unpack('>I', bytes.fromhex('80000000'))[0] == 2**31
          and struct.unpack('>i', b'\xff' * 4)[0] == -1 and struct.unpack('>I', b'\xff' * 4)[0] == 4294967295,
          'l14 screens[2], [5]')
    check('L3:drill_bytes', struct.unpack('>I', bytes.fromhex('00000100'))[0] == 256 and struct.unpack('<I', bytes.fromhex('00000100'))[0] == 65536
          and struct.unpack('>i', bytes.fromhex('ffffff38'))[0] == -200 and struct.unpack('>i', bytes.fromhex('00002ee0'))[0] == 12000
          and struct.unpack('>I', bytes.fromhex('00000bb8'))[0] == 3000 and struct.unpack('<I', bytes.fromhex('00000bb8'))[0] == 3087728640
          and struct.pack('>i', -1000) == bytes.fromhex('fffffc18') and struct.pack('>i', -1000)[3] == 24
          and struct.unpack('>I', bytes.fromhex('000007d0'))[0] == 2000 and struct.unpack('<I', bytes.fromhex('000007d0'))[0] == 3490119680
          and struct.pack('>i', -100) == bytes.fromhex('ffffff9c') and struct.pack('>i', -100)[3] == 156,
          'l14 screens[8], quiz[0], quiz[1]; review-3 items[6], [7]')
    frame = struct.pack('>BBHIIIiI', 84, 83, 12, 300, 99, 1000, -5, 43_200_000)
    check('L3:hw3_frame', frame.hex() == '5453000c0000012c00000063000003e8fffffffb02932e00' and len(frame) == 24
          and [frame[3], frame[7], frame[11], frame[15], frame[19], frame[23]] == [12, 44, 99, 232, 251, 0],
          f'homework-3 items[3]: {frame.hex()}')
    check('L3:frame_l14', struct.pack('>BBHIIIiI', 65, 66, 258, 70000, 123456789, 100, 10275, 36_000_000).hex()
          == '4142010200011170075bcd150000006400002823' + '02255100', 'l14 screens[0] canvas frame')
    check('L3:double_tenth', 0.1 + 0.2 != 0.3 and float.fromhex('0x1.999999999999ap-4') == 0.1, 'l14 quiz[2]: 0.1 is not exact in binary')
    check('L3:flags', (24 + 2, (26 + 3) // 4 * 4, 1472 // 26, 1472 - 56 * 26) == (26, 28, 56, 16), 'l14 screens[9]')

def sizeof_msg():
    src = ('#include <cstdint>\n#include <cstdio>\n'
           'struct Msg { uint8_t type, side; uint16_t instrument; uint32_t seq, id, qty; int32_t price; uint32_t time; };\n'
           'struct MsgF { uint8_t type, side; uint16_t instrument; uint32_t seq, id, qty; int32_t price; uint32_t time; uint16_t flags; };\n'
           'int main() { std::printf("%zu %zu\\n", sizeof(Msg), sizeof(MsgF)); return 0; }\n')
    d = tempfile.mkdtemp()
    p = os.path.join(d, 'm.cpp')
    with open(p, 'w') as f:
        f.write(src)
    exe = os.path.join(d, 'm')
    r = subprocess.run([CXX, '-std=c++17', '-w', '-o', exe, p], capture_output=True, text=True)
    out = subprocess.run([exe], capture_output=True, text=True).stdout.split()
    check('L3:sizeof_msg', r.returncode == 0 and out == ['24', '28'], f'l14 screens[4], [9]: sizeof {out}')

# ---------------------------------------------------------------- code items
def code_summarise():
    item = load('homework-3')['items'][1]['widget']
    data = os.path.join(ROOT, 'app', item['data']['feed.hex'])
    check('L3:feed_exists', os.path.exists(data), f'homework-3 items[1]: {data} missing')
    d = tempfile.mkdtemp()
    shutil.copy(data, os.path.join(d, 'feed.hex'))
    def run(code):
        ns = {}
        cwd = os.getcwd()
        os.chdir(d)
        try:
            exec(code, ns)
            return [eval(t['call'], ns) for t in item['tests']]
        finally:
            os.chdir(cwd)
    expected = [eval(t['expect']) for t in item['tests']]
    got = run(item['solution'])
    ok = all((abs(g - e) <= 1e-9 * abs(e)) if isinstance(e, float) else g == e for g, e in zip(got, expected))
    check('L3:code_summarise:solution_passes', ok, f'homework-3 items[1]: solution gives {got}, expected {expected}')
    got2 = run(item['starter'])
    check('L3:code_summarise:starter_fails', got2 != expected, 'homework-3 items[1]: the starter passes')
    # independent recomputation of the four figures from the raw file
    rows, seen = [], set()
    for line in open(data):
        line = line.strip()
        if not line:
            continue
        rec = struct.unpack('>BBHIIIiI', bytes.fromhex(line))
        if rec[3] in seen:
            continue
        seen.add(rec[3]); rows.append(rec)
    trades = [(r[5], r[6]) for r in rows if r[0] == ord('T')]
    vwap = sum(q * p for q, p in trades) / sum(q for q, _ in trades)
    check('L3:feed_recompute', len(seen) == 200 and missing(seen) == [17, 18, 90, 150, 151, 152] and len(trades) == 31
          and abs(vwap - 10001.412844036697) < 1e-9, f'homework-3 items[1]: {len(seen)} {missing(seen)} {len(trades)} {vwap}')

def code_items():
    code_item('L3:code_find_gaps', load('l13-tcp-and-udp')['screens'][9]['widget'])
    code_item('L3:code_encode', load('l14-messages-on-the-wire')['screens'][7]['widget'])

if __name__ == '__main__':
    assert CXX, 'no C++ compiler found'
    syscalls()
    chunks()
    gaps()
    wire_bytes()
    sizeof_msg()
    code_summarise()
    code_items()
    print(f'systems L3 concepts: {len(PASSED)} checks passed')
