"""Fix-pass read of commit 35ecf9f8 (markov L4 and L5 concept-audit fix pass).

Recomputes every changed slip two ways and simulates each empirical claim in
the changed strings. Exits 0 when all checks agree with the content. A check
marked EXPECTED-NOTE documents an imprecise sentence and does not fail the run.

Run from the repo root with the venv Python (NumPy needed).
"""
import json
import math
import os
import sys
from fractions import Fraction as F

import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
MK = os.path.join(ROOT, "app", "content", "courses", "markov")
rng = np.random.default_rng(20261126)
fails = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ("  " + detail if detail else ""))
    if not ok:
        fails.append(name)


def load(f):
    return json.load(open(os.path.join(MK, f)))


def walk(o):
    if isinstance(o, dict):
        yield o
        for v in o.values():
            yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)


def stationary(P):
    w, v = np.linalg.eig(P.T)
    k = np.argmin(abs(w - 1))
    p = np.real(v[:, k])
    return p / p.sum()


# ---------------------------------------------------------------- review-4
r4 = load("review-4.json")
acc = next(i for i in r4["items"] if i["id"] == "r-acceptance-share")
spl = next(i for i in r4["items"] if i["id"] == "r-split-joint")

# r-acceptance-share: Metropolis on weights 1, 2, 4.
w = [F(1), F(2), F(4)]
pi = [x / sum(w) for x in w]
move = []
for i in range(3):
    m = F(0)
    for j in (i - 1, i + 1):
        if 0 <= j < 3:
            m += F(1, 2) * min(F(1), w[j] / w[i])
    move.append(m)
share = sum(p * m for p, m in zip(pi, move))
check("r4 key 3/7 (exact)", share == F(3, 7), str(share))
# second way: build P, stationary by eigenvector, 1 - sum pi_i P_ii; plus a run.
P = np.zeros((3, 3))
for i in range(3):
    for j in (i - 1, i + 1):
        if 0 <= j < 3:
            P[i, j] = 0.5 * min(1.0, float(w[j] / w[i]))
    P[i, i] = 1 - P[i].sum()
pin = stationary(P)
check("r4 key 3/7 (matrix)", abs(1 - pin @ np.diag(P) - 3 / 7) < 1e-12)
n = 2_000_000
x, moves = 0, 0
u = rng.random(n)
cum = np.cumsum(P, axis=1)
for t in range(n):
    y = int(np.searchsorted(cum[x], u[t]))
    moves += y != x
    x = y
se = math.sqrt(3 / 7 * 4 / 7 / n) * 3  # generous for autocorrelation
check("r4 key 3/7 (simulated)", abs(moves / n - 3 / 7) < 5 * se, f"{moves/n:.4f}")

wrong = {s["id"]: s for s in acc["widget"]["wrong"]}
stay_a = 1 - share                       # complement of the key
stay_b = sum(p * (1 - m) for p, m in zip(pi, move))  # weighted stay chances
check("r4 slip stay = 4/7 two ways", stay_a == stay_b == F(4, 7)
      and abs(wrong["stay"]["value"] - 4 / 7) < 5e-5)
half_a = F(1, 2)                         # proposal chance
half_b = sum(move) / 3                   # unweighted mean of move chances
check("r4 slip half = 0.5 both named mistakes", half_a == half_b == F(1, 2))
check("r4 accept-top = middle move chance 3/4", move[1] == F(3, 4))


def bands_clear(widget):
    iv = [(widget["answer"] - widget["tol"]["abs"], widget["answer"] + widget["tol"]["abs"])]
    iv += [(s["value"] - s["tol"]["abs"], s["value"] + s["tol"]["abs"]) for s in widget["wrong"]]
    iv.sort()
    return all(iv[k][1] < iv[k + 1][0] for k in range(len(iv) - 1))


check("r4 acceptance bands disjoint", bands_clear(acc["widget"]))


# r-split-joint
def pois(k, m):
    return math.exp(-m) * m ** k / math.factorial(k)


key = pois(2, 6) * pois(1, 4)
check("r4 split key 0.00327", abs(key - spl["widget"]["answer"]) < 5e-6, f"{key:.6f}")
sw = {s["id"]: s for s in spl["widget"]["wrong"]}
om_a = pois(2, 3) * pois(1, 2)
om_b = math.exp(-5) * 9  # e^-3 * 9/2 * e^-2 * 2
check("r4 slip one-minute 0.0606 two ways", abs(om_a - om_b) < 1e-15
      and abs(om_a - sw["one-minute"]["value"]) < 5e-5, f"{om_a:.5f}")
sum_a = pois(2, 6) + pois(1, 4)
sum_b = 18 * math.exp(-6) + 4 * math.exp(-4)
check("r4 slip sum 0.1179 two ways", abs(sum_a - sum_b) < 1e-15
      and abs(sum_a - sw["sum"]["value"]) < 5e-5, f"{sum_a:.5f}")
check("r4 slip merged 0.0076", abs(pois(3, 10) - sw["merged"]["value"]) < 5e-5)
check("r4 split bands disjoint", bands_clear(spl["widget"]))
# compound slips that might land in a band: one-minute AND added
check("r4 one-minute-and-sum not in any band",
      all(abs(pois(2, 3) + pois(1, 2) - s["value"]) > s["tol"]["abs"] for s in sw.values()))
N = 4_000_000
b = rng.poisson(6, N)
s_ = rng.poisson(4, N)
hit = np.mean((b == 2) & (s_ == 1))
check("r4 split key simulated", abs(hit - key) < 5 * math.sqrt(key / N), f"{hit:.5f}")

# -------------------------------------------------------------- homework-4
h4 = load("homework-4.json")
Pc = np.array([[0, .8, .2], [.2, 0, .8], [.8, .2, 0]])
pc = stationary(Pc)
back = pc[0] * Pc[0, 1] / pc[1]
check("h4 yesterday A given today B = 0.8", abs(back - 0.8) < 1e-12)
flow_a, flow_c = F(1, 3) * F(4, 5), F(1, 3) * F(1, 5)
check("h4 half feedback flows 1/3*0.8 and 1/3*0.2 give 0.8",
      flow_a / (flow_a + flow_c) == F(4, 5))
# simulate
n = 1_000_000
u = rng.random(n)
xs = np.empty(n, dtype=np.int8)
x = 1
for t in range(n):
    x = (x + 1) % 3 if u[t] < 0.8 else (x - 1) % 3
    xs[t] = x
atB = xs[1:] == 1
est = np.mean(xs[:-1][atB] == 0)
check("h4 0.8 simulated (not 0.2, 0.5)", abs(est - 0.8) < 0.005, f"{est:.4f}")
# EXPECTED-NOTE: "right only for a reversible chain". A four-state chain where
# the A-B pair balances but the chain is not reversible: P(A|next B) = P_BA.
Q = np.array([[.5, .5, 0, 0],      # A talks only to B
              [.2, 0, .7, .1],     # B, C, D circulate
              [0, .1, .2, .7],
              [0, .7, .1, .2]])
q = stationary(Q)
pair_bal = abs(q[0] * Q[0, 1] - q[1] * Q[1, 0]) < 1e-12
rev = np.allclose(q[:, None] * Q, (q[:, None] * Q).T)
print(f"NOTE h4 forward: pair A-B balanced={pair_bal}, chain reversible={rev}, "
      f"P(A yesterday|B today)={q[0]*Q[0,1]/q[1]:.4f} equals P_BA={Q[1,0]}")
check("h4 counterexample to 'only for a reversible chain' exists", pair_bal and not rev)

# --------------------------------------------------- l13 birth-death claims
ok = True
for _ in range(2000):
    m = int(rng.integers(2, 9))
    up = rng.uniform(0.02, 0.6, m)
    dn = rng.uniform(0.02, 0.4, m)
    B = np.zeros((m, m))
    for i in range(m - 1):
        B[i, i + 1] = up[i]
        B[i + 1, i] = dn[i]
    B += np.diag(1 - B.sum(1))
    p = np.ones(m)
    for i in range(m - 1):
        p[i + 1] = p[i] * B[i, i + 1] / B[i + 1, i]
    p /= p.sum()
    ok &= np.allclose(p @ B, p) and np.allclose(p[:, None] * B, (p[:, None] * B).T)
check("l13 birth-death with both-way steps: ratio formula gives reversible pi (2000 chains)", ok)
B = np.zeros((6, 6))
for i in range(5):
    B[i, i + 1], B[i + 1, i] = 0.6, 0.1
B += np.diag(1 - B.sum(1))
p = stationary(B)
check("l13 walker 0..5: pi_{i+1} = 6 pi_i", np.allclose(p[1:] / p[:-1], 6))

# ----------------------------------------------------------- l14 dealers
l14 = load("l14-walks-on-networks.json")
found = False
for d in walk(l14):
    e = d.get("edges")
    if isinstance(e, list) and any(isinstance(x, dict) and x.get("to") == "D5" for x in e):
        nb = {}
        for x in e:
            nb.setdefault(x["from"], set()).add(x["to"])
            nb.setdefault(x["to"], set()).add(x["from"])
        if sorted(len(v) for v in nb.values()) == [1, 2, 2, 3, 4]:
            found = True
            check("l14 D5's only link is D1", nb["D5"] == {"D1"})
            rest = {k: v - {"D1"} for k, v in nb.items() if k != "D1"}
            seen, todo = {"D2"}, ["D2"]
            while todo:
                for y in rest[todo.pop()]:
                    if y not in seen:
                        seen.add(y)
                        todo.append(y)
            check("l14 without D1 only D5 is cut off", seen == {"D2", "D3", "D4"})
            break
check("l14 dealer network found", found)

# ------------------------------------------------------- l15 grid chain
l15 = load("l15-sampling-by-chain.json")
PM = None
for d in walk(l15):
    if isinstance(d.get("P"), list) and len(d["P"]) == 7:
        PM = np.array(d["P"], float)
        break
check("l15 matrix found, rows add to 1", PM is not None and np.allclose(PM.sum(1), 1, atol=2e-4))
stay = np.diag(PM)
check("l15 a step is most likely to be rejected at the two ends (P_ii)",
      min(stay[0], stay[-1]) > max(stay[1:-1]), str(np.round(stay, 3).tolist()))
pg = stationary(PM)
# EXPECTED-NOTE: per visit the ends reject most, but as a share of all flat
# steps in a long run (pi_i P_ii) the low end 0.40 is not above the middle.
cnt = pg * stay
print("NOTE l15 share of all steps that are flat, by state:", np.round(cnt, 4).tolist())
check("l15 count reading: flat steps at 0.40 are NOT the most common (sentence needs 'per visit')",
      cnt[0] < max(cnt[1:-1]) and cnt[-1] > max(cnt[:-1]))
d0 = np.zeros(7)
d0[0] = 1
traj = [d0]
for k in range(60):
    traj.append(traj[-1] @ PM)
traj = np.array(traj)
first = next(k for k in range(61) if traj[k, 0] < 0.06)
check("l15 first below 0.06 at k = 18 (give or take 1)", abs(first - 18) <= 1, str(first))
ev = np.sort(np.abs(np.linalg.eigvals(PM)))[::-1]
half_life = math.log(0.5) / math.log(ev[1])
check("l15 pull halves about every five steps (eigenvalue)", 4 <= half_life <= 6,
      f"lambda2={ev[1]:.4f}, half-life={half_life:.2f}")
tv = 0.5 * np.abs(traj - pg).sum(1)
hl2 = [k2 - k1 for k1 in (10, 15, 20) for k2 in range(k1, 60) if tv[k2] <= tv[k1] / 2][:1]
ratio5 = [tv[k + 5] / tv[k] for k in (10, 15, 20, 25)]
check("l15 pull halves about every five steps (TV distance)", all(0.4 < r < 0.6 for r in ratio5),
      str(np.round(ratio5, 3).tolist()))
check("l15 pull never vanishes exactly (TV > 0 at k = 60)", tv[60] > 0)
check("l15/h4 'most of the pull gone' by 18 to 20 steps", tv[18] < 0.5 * tv[0] and tv[20] < 0.1,
      f"TV(18)={tv[18]:.3f}, TV(20)={tv[20]:.3f}, excess at 0.40 after 18: {traj[18,0]-pg[0]:.4f}")

# ---------------------------------------------------------- l16 arrivals
lam, T, reps = 2.0, 40.0, 400_000   # 40 minutes = 80 mean gaps: "a long while"
# gap containing the fixed time T/2 ... use time t0 = 30
t0 = 30.0
gaps = rng.exponential(1 / lam, (reps, 140))
arr = np.cumsum(gaps, axis=1)
check("l16 enough arrivals simulated", arr[:, -1].min() > t0)
idx = (arr <= t0).sum(1)                    # arrivals before t0
nxt = arr[np.arange(reps), idx]
prev = np.where(idx > 0, arr[np.arange(reps), np.maximum(idx - 1, 0)], 0.0)
ahead, since, cover = nxt - t0, t0 - prev, nxt - prev
se = 1 / math.sqrt(reps)
check("l16 wait ahead mean 0.5", abs(ahead.mean() - 0.5) < 5 * 0.5 * se, f"{ahead.mean():.4f}")
check("l16 time since last trade mean 0.5", abs(since.mean() - 0.5) < 5 * 0.5 * se, f"{since.mean():.4f}")
check("l16 time since last is exponential (sd 0.5, P(>0.5)=e^-1)",
      abs(since.std() - 0.5) < 0.005 and abs(np.mean(since > 0.5) - math.exp(-1)) < 0.004)
check("l16 covering gap mean 1, not 0.5", abs(cover.mean() - 1) < 5 * math.sqrt(0.5) * se,
      f"{cover.mean():.4f}")
# conditional uniform: exactly one trade in 10 minutes at 2 a minute. The event
# has chance 20 e^-20, too rare to sample directly, so check the claim "the rate
# plays no part" exactly and by simulation at lower rates.
for lm in (0.05, 0.2, 2.0):
    exact = (pois(1, lm * 2) * pois(0, lm * 8)) / pois(1, lm * 10)
    check(f"l16 P(first 2 min | one in 10) = 0.2 at rate {lm} (exact)", abs(exact - 0.2) < 1e-12)
for lm in (0.05, 0.2):
    Nn = 3_000_000
    a, bb = rng.poisson(lm * 2, Nn), rng.poisson(lm * 8, Nn)
    one = (a + bb) == 1
    e = np.mean(a[one] == 1)
    check(f"l16 conditional uniform simulated at rate {lm}", abs(e - 0.2) < 5 * math.sqrt(0.16 / one.sum()),
          f"{e:.4f} on {one.sum()} windows")
check("l16 slip values use rate 2: 1-e^-4, e^-2",
      abs(1 - math.exp(-4) - 0.9817) < 5e-5 and abs(math.exp(-2) - 0.1353) < 5e-5)

# --------------------------------------------------------- l17 fair bets
p = F(100 - 80, 125 - 80)
check("l17 p = 4/9", p == F(4, 9) and 125 * p + 80 * (1 - p) == 100)
r = F(1, 20)   # with a rate the discounted price is the fair game
q_ = (100 * (1 + r) - 80) / 45
check("l17 with a rate: E[S1]/(1+r) = S0 under q, and q differs from 4/9",
      (125 * q_ + 80 * (1 - q_)) / (1 + r) == 100 and q_ != p)
check("l17 slip five solves 0.2x = 1", F(1) / F(1, 5) == 5 and F(3, 2) + F(3, 10) == F(9, 5))
check("l17 key x = 1", F(1, 2) * 3 + F(3, 10) * 1 + F(1, 5) * 1 == 2)

# ------------------------------------------------- l21 fair odds, patterns
# A £1 bet that returns £26 with chance 1/26 has zero expected profit.
check("l21 return £26 on £1 at chance 1/26 is fair; '26 to 1' is not",
      F(1, 26) * 26 - 1 == 0 and F(1, 26) * 27 - 1 != 0)


def wait(pattern, k):
    return sum(k ** j for j in range(1, len(pattern) + 1) if pattern[:j] == pattern[-j:])


check("l21 ABRACADABRA wait = 26^11 + 26^4 + 26", wait("ABRACADABRA", 26) == 26 ** 11 + 26 ** 4 + 26)
# simulate the same rule on a 3-letter alphabet, pattern ABA: 27 + 3 = 30 (vs 27).
reps3, tot = 200_000, 0
seq = rng.integers(0, 3, (reps3, 400))
hitm = (seq[:, :-2] == 0) & (seq[:, 1:-1] == 1) & (seq[:, 2:] == 0)
check("l21 sim: every run hits", hitm.any(1).all())
tt = hitm.argmax(1) + 3
check("l21 sim: ABA on 3 letters waits 30, not 27", abs(tt.mean() - 30) < 5 * tt.std() / math.sqrt(reps3),
      f"{tt.mean():.3f}")

# ------------------------------------------------------ l22 compound Poisson
sizes, ch = np.array([100, 200, 500]), np.array([0.5, 0.3, 0.2])
EY = float(sizes @ ch)
EY2 = float(sizes ** 2 @ ch)
check("l22 E[Y] = 210, E[S10] = 4200", EY == 210 and 20 * EY == 4200)
R = 400_000
Nc = rng.poisson(20, R)
S10 = rng.multinomial(Nc, ch) @ sizes
sd = math.sqrt(20 * EY2)
check("l22 E[S10] simulated 4200", abs(S10.mean() - 4200) < 5 * sd / math.sqrt(R), f"{S10.mean():.1f}")
# martingale: the increment over (10, 15] has mean 420*5 whatever S10 was.
N2 = rng.poisson(10, R)
inc = rng.multinomial(N2, ch) @ sizes - 420 * 5
lo, hi = S10 < np.quantile(S10, 0.25), S10 > np.quantile(S10, 0.75)
sdi = math.sqrt(10 * EY2)
check("l22 S_t - 420t: later increment has mean 0 given a low or a high past",
      abs(inc[lo].mean()) < 5 * sdi / math.sqrt(lo.sum()) and abs(inc[hi].mean()) < 5 * sdi / math.sqrt(hi.sum()),
      f"{inc[lo].mean():.2f}, {inc[hi].mean():.2f}")
# the hypothesis matters: a count that depends on the sizes breaks E[N]E[Y].
# Stop BEFORE the first 500 lot (N = number of trades before it): not a
# stopping time, not independent of the sizes.
draw = rng.choice(sizes, (R, 80), p=ch)
check("l22 dep. count: every row has a 500", (draw == 500).any(1).all())
Nd = (draw == 500).argmax(1)
Sd = np.where(np.arange(80)[None, :] < Nd[:, None], draw, 0).sum(1)
check("l22 dependent count: E[S] differs from E[N]E[Y] (so independence is needed)",
      abs(Sd.mean() - Nd.mean() * EY) > 100, f"E[S]={Sd.mean():.1f}, E[N]E[Y]={Nd.mean()*EY:.1f}")

print()
print("failed:", fails if fails else "none")
sys.exit(1 if fails else 0)
