"""systems level 1 performance task h1-branch-aloud: every number in the
prompt, model, rubric and explain, computed twice.

Route A: the closed-form products (n x p_wrong x 5 ns) and the exact
stationary mispredict rate of a two-bit counter (a birth-death chain).
Route B: a seeded simulation of 1,000,000 random prices through the best
fixed guess and through a two-bit counter, scaled to 10,000,000, plus a
native run of both loops to show they keep the same prices.
"""
import json, os, random, re, shutil, subprocess, sys, tempfile
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
HW = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'systems', 'homework-1.json')
item = next(i for i in json.load(open(HW))['items'] if i['id'] == 'h1-branch-aloud')
W = item['widget']
text = W['prompt'] + W['model'] + json.dumps(W['rubric']) + item['explain']['text'] + json.dumps(W['followUps'])
fails = []
def check(c, m):
    if not c:
        fails.append(m); print('FAIL', m)

n, p, miss_ns, body_ns = 10_000_000, F(3, 10), 5, 1

# ---- route A -----------------------------------------------------------
wrong = n * min(p, 1 - p)                       # best fixed guess: the majority
check(wrong == 3_000_000, 'wrong guesses 3,000,000')
miss_ms = wrong * miss_ns / F(10**6)
body_ms = n * body_ns / F(10**6)
check(miss_ms == 15 and body_ms == 10, '15 ms and 10 ms')
check(miss_ms + body_ms == 25 and miss_ms / (miss_ms + body_ms) == F(3, 5), '25 ms, 60%')
check((miss_ms + body_ms) / body_ms == F(5, 2), '2.5 times faster')
# two-bit counter: states 0..3, up with prob p, down with 1-p; guess taken at 2, 3
r = p / (1 - p)
w = [r**i for i in range(4)]; Z = sum(w); pi = [x / Z for x in w]
rate2 = (pi[0] + pi[1]) * p + (pi[2] + pi[3]) * (1 - p)
check(rate2 == F(210, 580), 'two-bit rate 210/580')
check(round(float(rate2) * 100) == 36, 'about 36%')
check(round(float(n * rate2 * miss_ns / 10**6)) == 18, 'about 18 ms')
half = n * F(1, 2) * miss_ns / F(10**6)
check(half == 25, 'half pass 25 ms')
ninety9 = n * F(1, 100) * miss_ns / F(10**6)
check(ninety9 == F(1, 2), '99% pass 0.5 ms')
check(1 - p == F(7, 10), 'keep guess wrong 70%')

# ---- route B: simulation ------------------------------------------------
rng = random.Random(2026)
m = 1_000_000
keep = [rng.random() < 0.3 for _ in range(m)]
fixed_wrong = sum(keep)                         # always guess skip
c, two_wrong = 1, 0
for k in keep:
    guess = c >= 2
    two_wrong += guess != k
    c = min(3, c + 1) if k else max(0, c - 1)
scale = n / m
print('simulated: fixed %.4f, two-bit %.4f' % (fixed_wrong / m, two_wrong / m))
check(abs(fixed_wrong / m - 0.3) < 0.002, 'sim fixed about 30%')
check(abs(two_wrong / m - float(rate2)) < 0.002, 'sim two-bit about 36.2%')
check(abs(fixed_wrong * scale * 5e-6 - 15) < 0.1, 'sim 15 ms')
check(abs(two_wrong * scale * 5e-6 - 18.1) < 0.1, 'sim 18 ms')
half_keep = [rng.random() < 0.5 for _ in range(m)]
check(abs(min(sum(half_keep), m - sum(half_keep)) * scale * 5e-6 - 25) < 0.15, 'sim half 25 ms')
k99 = [rng.random() < 0.99 for _ in range(m)]
check(abs((m - sum(k99)) * scale * 5e-6 - 0.5) < 0.02, 'sim 99% 0.5 ms')
srt = sorted(rng.random() for _ in range(m)); lim = 0.3
c, sw = 1, 0
for x in srt:
    k = x <= lim; sw += (c >= 2) != k; c = min(3, c + 1) if k else max(0, c - 1)
check(sw <= 3, 'sorted prices fool the predictor about once (%d)' % sw)

# ---- the rewrite keeps the same prices (native) ------------------------
cxx = shutil.which('g++') or shutil.which('clang++')
code = r'''
#include <cstdio>
#include <vector>
#include <random>
int main() {
    std::mt19937 g(7); std::vector<int> p(100000), a(100000), b(100000);
    for (auto& x : p) x = static_cast<int>(g() % 1000);
    int limit = 299, ka = 0, kb = 0, n = 100000;
    for (int i = 0; i < n; ++i)
        if (p[i] <= limit) a[ka++] = p[i];
    for (int i = 0; i < n; ++i) {
        b[kb] = p[i];
        kb += (p[i] <= limit);
    }
    bool same = ka == kb;
    for (int i = 0; same && i < ka; ++i) same = a[i] == b[i];
    std::printf("%d %d\n", same ? 1 : 0, ka);
}
'''
if cxx:
    d = tempfile.mkdtemp(); s = os.path.join(d, 'm.cpp'); open(s, 'w').write(code)
    subprocess.run([cxx, '-std=c++20', '-O1', '-fno-exceptions', s, '-o', os.path.join(d, 'a')], check=True)
    out = subprocess.run([os.path.join(d, 'a')], capture_output=True, text=True).stdout.split()
    print('native: same output', out)
    check(out[0] == '1' and abs(int(out[1]) / 100000 - 0.3) < 0.01, 'rewrite keeps the same prices')
    shutil.rmtree(d)
else:
    print('no compiler: skipped the native run')

# ---- every figure in the text is accounted for -------------------------
for fig in ['10,000,000', '30%', '1 ns', '5 ns', '3,000,000', '15 ms', '10 ms', '25 ms', '60%',
            '36%', '18 ms', '2.5 times', '99%', '1%', '0.5 ms', '70%']:
    check(fig in text, 'figure present: ' + fig)
nums = set(x.rstrip(',') for x in re.findall(r'\d[\d,]*(?:\.\d+)?', text.replace('{,}', ',')))
known = {'10,000,000', '30', '1', '5', '3,000,000', '0.3', '15', '10', '25', '60', '36', '18', '2.5',
         '99', '0.01', '0.5', '70', '2', '3', '0', '120', '30', '000', '000,000'}
check(nums <= known, 'no unchecked figure: %s' % sorted(nums - known))
check(sum(r['points'] for r in W['rubric']) == 10, 'rubric sums to 10')
check(0 < sum(1 for r in W['rubric'] if r.get('required')) < len(W['rubric']), 'some rows required, not all')
check(15 <= W['seconds'] <= 1800 and 1 <= len(W['followUps']) <= 5, 'aloud shape')
print('FAILURES:', len(fails))
sys.exit(1 if fails else 0)
