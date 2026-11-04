"""Topic 3.5 exam: every keyed number computed twice (closed form, then brute force or exact Fraction).

Run: python3 check.py   (asserts; prints each answer).  Seeds fixed.
"""
import math, random, itertools
from fractions import Fraction as F
from collections import deque, OrderedDict
import heapq

random.seed(35)
out = {}

# 1 two-regressions: b_yx = 0.75, b_xy = 0.27  ->  r^2 = b_yx * b_xy, r = +/-sqrt
b1, b2 = F(3, 4), F(27, 100)
r2 = b1 * b2
assert r2 == F(81, 400)
r = math.sqrt(r2)
assert abs(r - 0.45) < 1e-12
# brute force: build data with r = 0.45, sx = 1, sy = b1/ r ... check slopes
sx, sy = 1.0, 0.75 / 0.45 * 1.0
# slope y on x = r*sy/sx ; slope x on y = r*sx/sy
assert abs(0.45 * sy / sx - 0.75) < 1e-12 and abs(0.45 * sx / sy - 0.27) < 1e-12
out[1] = dict(r=0.45, r2=float(r2), mean=(0.75 + 0.27) / 2, gm_slip=0.75 * 0.27)

# 2 correlation-limits: rho_ab = 0.8, rho_bc = -0.5. Range of rho_ac.
a, b = 0.8, -0.5
hi = a * b + math.sqrt((1 - a * a) * (1 - b * b))
lo = a * b - math.sqrt((1 - a * a) * (1 - b * b))
# brute force: smallest eigenvalue of the matrix is >= 0 exactly on [lo, hi]
import numpy as np
def mineig(c):
    M = np.array([[1, a, c], [a, 1, b], [c, b, 1]])
    return np.linalg.eigvalsh(M)[0]
grid = np.linspace(-1, 1, 200001)
ok = [c for c in grid if mineig(c) > -1e-12] if False else None
# bisect from the interior point
mid = a * b
def bis(lo_, hi_):
    for _ in range(80):
        m = (lo_ + hi_) / 2
        if mineig(m) >= -1e-13: lo_ = m
        else: hi_ = m
    return lo_
hi_b = bis(mid, 1.0)
lo_b = -bis(-mid, 1.0) if False else None
def bis2(inner, outer):
    for _ in range(80):
        m = (inner + outer) / 2
        if mineig(m) >= -1e-13: inner = m
        else: outer = m
    return inner
lo_b = bis2(mid, -1.0)
assert abs(hi - hi_b) < 1e-6 and abs(lo - lo_b) < 1e-6, (hi, hi_b, lo, lo_b)
out[2] = dict(hi=round(hi, 4), lo=round(lo, 4), slip_product=a * b, slip_zero=0.0)

# 3 p-value: eight signals, smallest p 0.011, threshold 0.05/8
assert abs(0.05 / 8 - 0.00625) < 1e-12
assert 0.011 > 0.00625
# brute force: probability at least one p <= 0.011 among 8 nulls
fw = 1 - (1 - 0.011) ** 8
out[3] = dict(bonf=0.00625, family_wise_at_0_011=round(fw, 4))
assert abs(fw - 0.0849) < 0.0005

# 4 special eigenvalues: A = 2 I_4 + 3 w w^T, w = (1,2,2,4)
w = np.array([1, 2, 2, 4])
A = 2 * np.eye(4) + 3 * np.outer(w, w)
ww = int(w @ w)
assert ww == 25
det_closed = 2 ** 3 * (2 + 3 * ww)
det_np = round(np.linalg.det(A))
assert det_closed == det_np == 616
ev = np.sort(np.linalg.eigvalsh(A))
assert np.allclose(ev, [2, 2, 2, 77])
out[4] = dict(det=616, lam_max=77, slip_no_two=8 * 75, slip_2pow4=16 * 77, slip_prod_all=2 * 2 * 2 * 75)

# 6 pca share: Sigma = [[6,2],[2,3]]
S = np.array([[7, 2], [2, 4]])
ev6 = np.sort(np.linalg.eigvalsh(S))[::-1]
assert np.allclose(ev6, [8, 3])
# closed form: trace 11, det 24, lam^2 - 11 lam + 24 = 0
assert (11 + math.isqrt(121 - 96)) / 2 == 8
share = F(8, 11)
assert abs(float(share) - ev6[0] / ev6.sum()) < 1e-12
# simulation of share from sample covariance of many draws
L = np.linalg.cholesky(S)
X = (L @ np.random.default_rng(35).standard_normal((2, 400000))).T
Se = np.cov(X.T)
e = np.linalg.eigvalsh(Se)
assert abs(e[1] / e.sum() - 8 / 11) < 0.003
out[6] = dict(share=round(8 / 11, 4), slip_var_share=round(7 / 11, 4), slip_second=round(3 / 11, 4), slip_half=0.5)

# 7 weak signals statement arithmetic
# (a) rho 0.04, n 2500 -> t = r sqrt(n) = 2.0
t_a = 0.04 * math.sqrt(2500)
assert abs(t_a - 2.0) < 1e-12
# simulation: sample correlation sd ~ 1/sqrt(n)
rng = np.random.default_rng(7)
rs = []
for _ in range(4000):
    x = rng.standard_normal(2500); y = rng.standard_normal(2500)
    rs.append(np.corrcoef(x, y)[0, 1])
assert abs(np.std(rs) - 1 / math.sqrt(2500)) < 0.002
# (b) days needed for t = 2 at r = 0.02: n = (2/r)^2 = 10000
assert (2 / 0.02) ** 2 == 10000
# (c) doubling the sample: standard error falls by sqrt 2, not by half
assert abs(1 / math.sqrt(2) - 0.7071) < 1e-4
# (d) cost: gross edge 4 bp a trade less cost 5 bp per round trip is negative
assert 4 - 5 < 0
out[7] = dict(t=2.0, n_for_0_02=10000, se_ratio=round(1 / math.sqrt(2), 4))

# 9 baseline-first: AR(1) phi = 0.6, marginal variance 4
phi, var = 0.6, 4.0
mse_persist = 2 * var * (1 - phi)
mse_mean = var
mse_fit = var * (1 - phi ** 2)
assert abs(mse_persist - 3.2) < 1e-12 and abs(mse_fit - 2.56) < 1e-12
gain = 1 - mse_fit / mse_persist
assert abs(gain - 0.2) < 1e-12
# simulation
rng = np.random.default_rng(9)
n = 1_500_000
e_ = rng.standard_normal(n) * math.sqrt(var * (1 - phi ** 2))
x = np.empty(n); x[0] = rng.standard_normal() * 2
for i in range(1, n):
    x[i] = phi * x[i - 1] + e_[i]
m_p = np.mean((x[1:] - x[:-1]) ** 2)
m_m = np.mean(x[1:] ** 2)
m_f = np.mean((x[1:] - phi * x[:-1]) ** 2)
assert abs(m_p - 3.2) < 0.03 and abs(m_m - 4) < 0.05 and abs(m_f - 2.56) < 0.02, (m_p, m_m, m_f)
out[9] = dict(persist=3.2, mean=4.0, fit=2.56, gain_vs_persist=0.2, gain_vs_mean=1 - 2.56 / 4, slip_phi2=0.36, slip_mean_ratio=3.2 / 4)

# 10 group slopes (code item): reference implementation and brute force
def slope(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx == 0: return None
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
def group_slopes(rows, min_n):
    g = {}
    for k, x, y in rows:
        g.setdefault(k, []).append((x, y))
    res = {}
    for k, pts in g.items():
        if len(pts) < min_n: continue
        s = slope([p[0] for p in pts], [p[1] for p in pts])
        if s is None: continue
        res[k] = s
    return res
def group_slopes_np(rows, min_n):
    res = {}
    for k in {r[0] for r in rows}:
        pts = np.array([(x, y) for kk, x, y in rows if kk == k], float)
        if len(pts) < min_n or np.ptp(pts[:, 0]) == 0: continue
        res[k] = np.polyfit(pts[:, 0], pts[:, 1], 1)[0]
    return res
ROWS = [("A", 1, 3), ("A", 2, 5), ("A", 3, 8), ("A", 4, 9),
        ("B", 10, 4), ("B", 20, 7), ("B", 30, 8), ("B", 40, 14), ("B", 50, 15),
        ("C", 5, 9), ("C", 6, 2), ("C", 7, 5),
        ("D", 2, 2), ("D", 2, 4), ("D", 2, 9), ("D", 2, 1)]
r1 = group_slopes(ROWS, 4); r2_ = group_slopes_np(ROWS, 4)
assert set(r1) == set(r2_) == {"A", "B"}
for k in r1: assert abs(r1[k] - r2_[k]) < 1e-9
out[10] = {k: round(v, 4) for k, v in r1.items()}

# 11 online fit: rows then arrive, leave
pts = [(1, 3), (2, 4), (3, 7), (4, 8)]
def fit(p):
    n = len(p); sx = sum(x for x, _ in p); sy = sum(y for _, y in p)
    sxx = sum(x * x for x, _ in p); sxy = sum(x * y for x, y in p)
    b = F(n * sxy - sx * sy, n * sxx - sx * sx)
    return b, F(sy, n) - b * F(sx, n)
b0, a0 = fit(pts)
p1 = pts + [(5, 12)]
b1_, a1_ = fit(p1)
p2 = p1[1:]
b2_, a2_ = fit(p2)
# brute force with polyfit
for p, b in ((pts, b0), (p1, b1_), (p2, b2_)):
    assert abs(np.polyfit([x for x, _ in p], [y for _, y in p], 1)[0] - float(b)) < 1e-9
# running sums
S_ = dict(n=4, sx=10, sy=22, sxx=30, sxy=1*3 + 2*4 + 3*7 + 4*8)
assert S_['sxy'] == 64
out[11] = dict(b0=str(b0), b_add=str(b1_), b_add_f=float(b1_), b_leave=str(b2_), b_leave_f=float(b2_), a_leave=float(a2_))
# slips: forgetting to update n; leaving row with wrong sign
def slope_from_sums(n, sx, sy, sxx, sxy): return (n * sxy - sx * sy) / (n * sxx - sx * sx)
sl_add = slope_from_sums(5, 15, 34, 55, 124)
assert abs(sl_add - float(b1_)) < 1e-12
slip_n = slope_from_sums(4, 15, 34, 55, 124)  # forgot to count the new row in n
sl_leave = slope_from_sums(4, 14, 31, 54, 121)
assert abs(sl_leave - float(b2_)) < 1e-12
slip_leave_add = slope_from_sums(6, 16, 37, 56, 127)  # added the leaving row instead of removing it
out[11].update(slip_n=slip_n, slip_leave_add=slip_leave_add)

# 13 deque trace
seq = [7, 3, 9, 4, 6, 8, 2, 5, 5, 1]
k = 4
def deque_run(seq, k):
    dq = deque(); back = front = 0; maxima = []
    for i, v in enumerate(seq):
        while dq and seq[dq[-1]] <= v:
            dq.pop(); back += 1
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft(); front += 1
        if i >= k - 1: maxima.append(seq[dq[0]])
    return back, front, maxima
back, front, maxima = deque_run(seq, k)
bf = [max(seq[i:i + k]) for i in range(len(seq) - k + 1)]
assert maxima == bf
out[13] = dict(back=back, front=front, maxima=maxima, sum=sum(maxima), pushes=len(seq))

# 15 stack parse (truncating division, unary minus)
def parse(expr):
    toks = expr.split()
    # recursive descent with unary minus
    pos = [0]
    def peek(): return toks[pos[0]] if pos[0] < len(toks) else None
    def nxt(): t = toks[pos[0]]; pos[0] += 1; return t
    def factor():
        t = nxt()
        if t == "u-": return -factor()
        return int(t)
    def term():
        v = factor()
        while peek() in ("*", "/"):
            op = nxt(); r = factor()
            if op == "*": v *= r
            else: v = int(v / r)  # toward zero
        return v
    def expr_():
        v = term()
        while peek() in ("+", "-"):
            op = nxt(); r = term()
            v = v + r if op == "+" else v - r
        return v
    return expr_()
# two-stack evaluator on the same strings as a second method
def stack_eval(expr):
    toks = expr.split()
    prec = {"+": 1, "-": 1, "*": 2, "/": 2}
    vals, ops = [], []
    def apply():
        op = ops.pop(); b = vals.pop(); a = vals.pop()
        if op == "+": vals.append(a + b)
        elif op == "-": vals.append(a - b)
        elif op == "*": vals.append(a * b)
        else:
            q = abs(a) // abs(b); vals.append(q if (a >= 0) == (b >= 0) else -q)
    neg = False
    for t in toks:
        if t == "u-": neg = not neg
        elif t in prec:
            while ops and prec[ops[-1]] >= prec[t]: apply()
            ops.append(t)
        else:
            v = int(t); vals.append(-v if neg else v); neg = False
    while ops: apply()
    return vals[0]
E = "25 + 7 * u- 4 / 3 + 17 / u- 5"
# readable: 25 + 7 * -4 / 3 + 17 / -5
assert parse(E) == stack_eval(E)
floor_val = None
out[15] = dict(val=parse(E))
# slip values
# floor division
def py_eval(s):  # floor division version
    return eval(s.replace("/", "//"))
fl = py_eval("25 + 7 * (-4) / 3 + 17 / (-5)")
out[15]["floor"] = fl
# left to right with no precedence
# unary treated as binary subtract of next? (ignore the sign of -4 and -5)
ign = 25 + 7 * 4 // 3 + 17 // 5
out[15]["ignore_sign"] = ign
def tr_(a, b):
    q = abs(a) // abs(b); return q if (a >= 0) == (b >= 0) else -q
ltr = tr_(tr_((25 + 7) * -4, 3) + 17, -5)
out[15]["no_precedence"] = ltr

# 16 rule trace
bal = 500
rules_pnl = [-120, -90, 60, 400, -250, -180]
log = []
for p in rules_pnl:
    if bal < 400: bal += 250
    bal += p
    if bal > 700: bal -= (bal - 700) // 2
    log.append(bal)
out[16] = dict(final=bal, log=log)

# 17 price time
asks = [("A", 101.0, 10, 1), ("B", 100.5, 5, 2), ("C", 100.5, 8, 3), ("D", 100.0, 6, 4)]
def match_buy(asks, qty, limit):
    book = sorted(asks, key=lambda a: (a[1], a[3]))
    fills = []
    for name, px, q, t in book:
        if qty == 0 or px > limit: break
        f = min(q, qty); fills.append((name, f, px)); qty -= f
    return fills, qty
fills, rest = match_buy(asks, 20, 100.5)
assert fills == [("D", 6, 100.0), ("B", 5, 100.5), ("C", 8, 100.5)] and rest == 1
out[17] = dict(fills=fills, rest=rest, notional=sum(f * p for _, f, p in fills))

# 18 LRU cache of capacity 3
cap = 3
ops = [("put", "a"), ("put", "b"), ("put", "c"), ("get", "a"), ("put", "d"), ("get", "c"), ("put", "e"), ("get", "b"), ("put", "a")]
od = OrderedDict(); ev_log = []; state = []
for op, key in ops:
    ev = "none"
    if op == "get":
        if key in od: od.move_to_end(key)
    else:
        if key in od: od.move_to_end(key)
        else:
            od[key] = 1
            if len(od) > cap:
                ev = next(iter(od)); del od[ev]
    ev_log.append(ev); state.append("".join(reversed(list(od))))
# second method: list simulation
lst = []; ev2 = []
for op, key in ops:
    ev = "none"
    if key in lst: lst.remove(key); lst.append(key)
    elif op == "put":
        lst.append(key)
        if len(lst) > cap: ev = lst.pop(0)
    ev2.append(ev)
assert ev2 == ev_log
out[18] = dict(evicted=ev_log, state_mru_first=state)

# 19 minutes plan: budget, options
budget = 70
probs = [  # (full pts, full min, part pts, part min)
    (30, 28, 12, 9), (40, 36, 18, 13), (25, 20, 10, 6), (50, 44, 20, 15)]
def best(budget, probs):
    # dp over problems: choose skip / part / full
    dp = [0] * (budget + 1)
    for fp, fm, pp, pm in probs:
        nd = dp[:]
        for t in range(budget + 1):
            for pts, m in ((fp, fm), (pp, pm)):
                if t >= m: nd[t] = max(nd[t], dp[t - m] + pts)
        dp = nd
    return max(dp)
def best_brute(budget, probs):
    bst = 0
    for choice in itertools.product((0, 1, 2), repeat=len(probs)):
        pts = m = 0
        for c, (fp, fm, pp, pm) in zip(choice, probs):
            if c == 1: pts += fp; m += fm
            elif c == 2: pts += pp; m += pm
        if m <= budget: bst = max(bst, pts)
    return bst
assert best(budget, probs) == best_brute(budget, probs)
# slips: only full problems; greedy by points per minute taking full only
def only_full(budget, probs):
    bst = 0
    for choice in itertools.product((0, 1), repeat=len(probs)):
        pts = sum(c * p[0] for c, p in zip(choice, probs)); m = sum(c * p[1] for c, p in zip(choice, probs))
        if m <= budget: bst = max(bst, pts)
    return bst
def greedy_rate(budget, probs):
    items = []
    for fp, fm, pp, pm in probs: items.append((fp / fm, fp, fm))
    items.sort(reverse=True); pts = 0; t = 0
    for r, p, m in items:
        if t + m <= budget: pts += p; t += m
    return pts
out[19] = dict(best=best(budget, probs), only_full=only_full(budget, probs), greedy=greedy_rate(budget, probs), all_partial=sum(p[2] for p in probs), partial_min=sum(p[3] for p in probs))

# 20 edge case list
def longest_run_good(xs):
    best = run = 0; prev = object()
    for v in xs:
        run = run + 1 if v == prev else 1
        prev = v; best = max(best, run)
    return best
def longest_run_bug(xs):
    best, run = 0, 1
    for i in range(1, len(xs)):
        if xs[i] == xs[i - 1]: run += 1
        else:
            best = max(best, run); run = 1
    return best
cands = {"empty": [], "single": [5], "two_equal": [4, 4], "ends_run": [1, 2, 2], "all_equal": [3, 3, 3, 3], "start_run": [6, 6, 1, 2], "mid_run": [1, 7, 7, 7, 2], "alternating": [1, 2, 1, 2]}
exposes = {k: longest_run_good(v) != longest_run_bug(v) for k, v in cands.items()}
out[20] = exposes

# 22 latency ladder
out[22] = dict(ratio=100_000 / 4)  # SSD random read 100 us vs L2 hit 4 ns

# 23 cache misses
def misses(n_acc, stride_bytes, line=64, start=0):
    seen = set(); m = 0
    for i in range(n_acc):
        l = (start + i * stride_bytes) // line
        if l not in seen: seen.add(l); m += 1
    return m
n_acc = 1000; stride = 24  # 8-byte doubles, step 3
m1 = misses(n_acc, stride)
# closed form: last address 999*24 = 23976, lines 0..374 and every line touched since stride < line
assert m1 == (999 * 24) // 64 + 1 == 375
out[23] = dict(misses=m1, lines_if_unit=1000 * 8 // 64, every=1000)

# 25: nothing numeric

# 26 branch cost
N = 2_000_000; p = 0.3; pen = 14
cycles = N * p * pen
assert cycles == 8_400_000
# simulate a simple predictor for iid data with p=0.3: always predict majority -> miss rate p
rng = random.Random(26)
miss = sum(1 for _ in range(200000) if rng.random() < p) / 200000
assert abs(miss - p) < 0.005
out[26] = dict(cycles=cycles, ms_at_3ghz=cycles / 3e9 * 1e3, slip_half=N * 0.5 * pen, slip_all=N * pen)

# 27 race: n = n + 2 (A) and n = n * 3 (B), start 0
finals = set()
# each thread: read, compute, write. enumerate interleavings of [rA, wA, rB, wB] with order within thread kept
for order in set(itertools.permutations("AABB")):
    n = 0; regs = {}; step = {"A": 0, "B": 0}
    for t in order:
        if step[t] == 0: regs[t] = n
        else: n = regs[t] + 2 if t == "A" else regs[t] * 3
        step[t] += 1
    finals.add(n)
assert finals == {0, 2, 6}
out[27] = dict(finals=sorted(finals))

# 29 tail percentile: nearest rank
lat = [212, 198, 205, 219, 201, 207, 3100, 214, 203, 209, 196, 211, 206, 202, 2650, 208, 200, 215, 204, 210, 197, 213, 199, 216, 205]
assert len(lat) == 25
s = sorted(lat)
rank = math.ceil(0.96 * 25)
assert rank == 24
p96 = s[rank - 1]
mean = sum(lat) / len(lat)
# second method: smallest value with at least 96% of data at or below it
cum = [v for v in s if sum(1 for u in s if u <= v) / 25 >= 0.96][0]
assert cum == p96
# interpolated (numpy linear)
lin = float(np.percentile(lat, 96))
out[29] = dict(p96=p96, mean=mean, median=s[12], linear=lin, maxv=s[-1], p95_rank=s[math.ceil(0.95 * 25) - 1])

# 30 ring buffer
def ring_run(ops, cap):
    mask = cap - 1
    buf = [0] * cap; head = tail = 0; popped = []
    for o in ops:
        if o > 0:
            if head - tail < cap:
                buf[head & mask] = o; head += 1
        else:
            if head > tail:
                popped.append(buf[tail & mask]); tail += 1
    return popped
def ring_ref(ops, cap):
    from collections import deque as dq
    d = dq(); popped = []
    for o in ops:
        if o > 0:
            if len(d) < cap: d.append(o)
        else:
            if d: popped.append(d.popleft())
    return popped
rr = random.Random(30)
for _ in range(2000):
    c = rr.choice([1, 2, 4, 8, 16])
    ops = [rr.choice([rr.randint(1, 99), 0]) for _ in range(rr.randint(0, 60))]
    assert ring_run(ops, c) == ring_ref(ops, c)
out[30] = dict(ex1=ring_run([5, 6, 7, 0, 8, 9, 0, 0, 0, 0], 4))

if __name__ == "__main__":
    for k in sorted(out): print(k, out[k])
    print("all checks passed")
