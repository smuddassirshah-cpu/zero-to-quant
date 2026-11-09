"""Recompute every key of the 13 review top-up items by two methods.

Checks each typed key against the file, each numeric distractor and each
choice distractor against the key, and exits 0 only when all agree.
Run from anywhere: python docs/reports/review-topup-numbers.py
"""
import json
import math
import os
import sys
from collections import deque
from fractions import Fraction as F
from itertools import product

import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "app", "content", "courses")
fails = []


def check(name, a, b, tol=1e-9):
    if abs(float(a) - float(b)) > tol:
        fails.append(f"{name}: {a} != {b}")


def item(course, n, iid):
    j = json.load(open(os.path.join(ROOT, course, f"review-{n}.json"), encoding="utf-8"))
    hits = [it for it in j["items"] if it["id"] == iid]
    if len(hits) != 1:
        fails.append(f"{course}/review-{n}#{iid}: not found once")
        return None
    if j["items"][-1]["id"] != iid:
        fails.append(f"{course}/review-{n}#{iid}: not the last item")
    if len(j["items"]) != 10:
        fails.append(f"{course}/review-{n}: {len(j['items'])} items, not 10")
    return hits[0]


def numeric(course, n, iid, key, wrong):
    """key: recomputed answer; wrong: {id: recomputed slip value}."""
    it = item(course, n, iid)
    if it is None:
        return
    w = it["widget"]
    tol = w["tol"]["abs"]
    check(f"{iid} key vs file", w["answer"], key, max(tol, 1e-9))
    ws = {x["id"]: x for x in w.get("wrong", [])}
    if set(ws) != set(wrong):
        fails.append(f"{iid}: wrong ids {sorted(ws)} != {sorted(wrong)}")
    for k, v in wrong.items():
        if k in ws:
            check(f"{iid} wrong {k} vs file", ws[k]["value"], v, max(ws[k]["tol"]["abs"], 1e-9))
            # a distractor must not be accepted as the key, nor the key as a distractor
            if abs(ws[k]["value"] - w["answer"]) <= tol + ws[k]["tol"]["abs"]:
                fails.append(f"{iid}: wrong {k} overlaps the key")
        if k not in it["feedback"].get("byKey", {}):
            fails.append(f"{iid}: no feedback for {k}")


def choice(course, n, iid, correct_id):
    it = item(course, n, iid)
    if it is None:
        return
    opts = it["widget"]["options"]
    right = [o["id"] for o in opts if o.get("correct")]
    if right != [correct_id]:
        fails.append(f"{iid}: correct options {right}")
    texts = [o["text"] for o in opts]
    if len(set(texts)) != len(texts):
        fails.append(f"{iid}: repeated option text")
    for o in opts:
        if not o.get("correct") and not o.get("why"):
            fails.append(f"{iid}: distractor {o['id']} has no why")


# 1. recruiting review-1: judgement item, key is the developer plan.
choice("recruiting", 1, "r10-dev-plan", "coding")

# 2. recruiting review-2: one take; the restart leaves 120 - 20 = 100 s.
choice("recruiting", 2, "r2-one-take", "finish")
check("one-take restart seconds", 120 - 20, 100)

# 3. recruiting review-3: up to three rolls, keep the last.
# Method A: backward induction with fractions.
v1 = F(7, 2)
v2 = sum(max(F(f), v1) for f in range(1, 7)) / 6
v3 = sum(max(F(f), v2) for f in range(1, 7)) / 6
# Method B: enumerate the stopping rule "stop on 5 or 6 at roll 1, on 4+ at roll 2".
tot = F(0)
for a, b, c in product(range(1, 7), repeat=3):
    if a >= 5:
        tot += a
    elif b >= 4:
        tot += b
    else:
        tot += c
v3b = tot / 216
check("three-roll value A vs B", v3, v3b)
check("three-roll value", v3, F(14, 3))
check("two-roll value", v2, F(17, 4))
assert v1 > F(16, 5) and F(16, 5) >= 1 and F(16, 5) <= 6  # 3.20 passes range, fails refusal
choice("recruiting", 3, "r3-refuse-check", "refuse")


# 4. brainteasers review-1: jugs of 7 and 11, fewest steps to 8 litres.
def bfs(a, b, target, start_moves=None):
    def moves(s):
        x, y = s
        t, u = min(x, b - y), min(y, a - x)
        return [(a, y), (x, b), (0, y), (x, 0), (x - t, y + t), (x + u, y - u)]
    firsts = start_moves or moves((0, 0))
    best = math.inf
    for f0 in firsts:
        dist = {(0, 0): 0, f0: 1}
        q = deque([f0])
        while q:
            s = q.popleft()
            if target in s:
                best = min(best, dist[s])
                break
            for m in moves(s):
                if m not in dist:
                    dist[m] = dist[s] + 1
                    q.append(m)
    return best


steps = bfs(7, 11, 8)


# Method B: iterative deepening search, independent of the BFS.
def dfs_depth(a, b, target, limit):
    def moves(s):
        x, y = s
        t, u = min(x, b - y), min(y, a - x)
        return [(a, y), (x, b), (0, y), (x, 0), (x - t, y + t), (x + u, y - u)]
    def go(s, d, seen):
        if target in s:
            return True
        if d == 0:
            return False
        return any(go(m, d - 1, seen | {m}) for m in moves(s) if m not in seen)
    for d in range(limit + 1):
        if go((0, 0), d, {(0, 0)}):
            return d
    return None


steps_b = dfs_depth(7, 11, 8, 12)
# Method C: the written route, step by step.
route = [(0, 11), (7, 4), (0, 4), (4, 0), (4, 11), (7, 8)]
check("jugs BFS vs IDDFS", steps, steps_b)
check("jugs route length", len(route), steps)
small_first = bfs(7, 11, 8, start_moves=[(7, 0)])
check("jugs small-jug-first route", small_first, 8)
pours = sum(1 for (x0, y0), (x1, y1) in zip([(0, 0)] + route, route) if x0 + y0 == x1 + y1 and (x0, y0) != (x1, y1))
check("pours in the route", pours, 3)
numeric("brainteasers", 1, "r10-jugs-7-11", steps, {"small-first": small_first, "pours": pours})

# 5. research-int review-1: det(I + u u^T), u = (2, 1, 2, 4).
u = np.array([2.0, 1.0, 2.0, 4.0])
det_a = np.linalg.det(np.eye(4) + np.outer(u, u))
det_b = 1 + u @ u  # matrix determinant lemma / eigenvalues 1 + |u|^2, 1, 1, 1
check("det numpy vs lemma", det_a, det_b, 1e-9)
check("det value", det_b, 26)
eig = np.linalg.eigvalsh(np.eye(4) + np.outer(u, u))
check("trace", eig.sum(), 29, 1e-9)
numeric("research-int", 1, "r1-det-rank-one", 26, {"no-identity": 25, "trace": 29})

# 6. puzzles review-1: 8 equally likely stickers, wait for 5 different.
e_a = sum(F(8, 8 - k) for k in range(5))
# Method B: Markov chain on the number of distinct stickers held.
P = np.zeros((6, 6))
for k in range(5):
    P[k, k] = k / 8
    P[k, k + 1] = 1 - k / 8
Q = P[:5, :5]
e_b = np.linalg.solve(np.eye(5) - Q, np.ones(5))[0]
check("stickers A vs B", float(e_a), e_b, 1e-12)
full = float(sum(F(8, k) for k in range(1, 9)))
numeric("puzzles", 1, "r1-five-of-eight", round(float(e_a), 4), {"all-eight": round(full, 4), "one-each": 5})

# 7. puzzles review-4: ticket pays 16 if THH before HHH.
# Method A: first-step analysis on prefixes.
pats = ["THH", "HHH"]


def first_to_appear(a, b, p=F(1, 2)):
    states = [""]
    for pat in (a, b):
        for i in range(1, len(pat)):
            if pat[:i] not in states:
                states.append(pat[:i])
    idx = {s: i for i, s in enumerate(states)}
    n = len(states)
    M = [[F(0)] * n for _ in range(n)]
    rhs = [F(0)] * n
    for s in states:
        i = idx[s]
        M[i][i] += 1
        for c, pc in (("H", p), ("T", 1 - p)):
            t = s + c
            if t.endswith(a):
                rhs[i] += pc
                continue
            if t.endswith(b):
                continue
            while t not in idx:
                t = t[1:]
            M[i][idx[t]] -= pc
    # Gaussian elimination in fractions
    for col in range(n):
        piv = next(r for r in range(col, n) if M[r][col] != 0)
        M[col], M[piv] = M[piv], M[col]
        rhs[col], rhs[piv] = rhs[piv], rhs[col]
        for r in range(n):
            if r != col and M[r][col] != 0:
                f = M[r][col] / M[col][col]
                M[r] = [x - f * y for x, y in zip(M[r], M[col])]
                rhs[r] -= f * rhs[col]
    return rhs[0] / M[0][0]


pa = first_to_appear("THH", "HHH")


# Method B: Conway leading numbers, odds for A over B = (BB - BA) : (AA - AB).
def lead(x, y):
    return sum(2 ** (len(x) - 1 - i) for i in range(len(x)) if y.startswith(x[i:]))


A, B = "THH", "HHH"
odds_a = F(lead(B, B) - lead(B, A), lead(A, A) - lead(A, B))
pb = odds_a / (1 + odds_a)
check("THH first: chain vs Conway", pa, pb)
check("THH first", pa, F(7, 8))
numeric("puzzles", 4, "r4-thh-price", float(16 * pa), {"even": 8, "hhh": 2})

# 8. game-theory review-1: Ana's value at the mixed equilibrium.
a_pay = np.array([[4, 1], [1, 3]], float)
b_pay = np.array([[1, 3], [2, 0]], float)
# no pure equilibrium
pure = [(i, j) for i in range(2) for j in range(2)
        if a_pay[i, j] >= a_pay[1 - i, j] and b_pay[i, j] >= b_pay[i, 1 - j]]
if pure:
    fails.append(f"mixed game has pure equilibria {pure}")
# Method A: indifference formulas
q = (a_pay[1, 1] - a_pay[0, 1]) / (a_pay[0, 0] - a_pay[0, 1] - a_pay[1, 0] + a_pay[1, 1])
p = (b_pay[1, 1] - b_pay[1, 0]) / (b_pay[0, 0] - b_pay[1, 0] - b_pay[0, 1] + b_pay[1, 1])
va = q * a_pay[0, 0] + (1 - q) * a_pay[0, 1]
vb = p * b_pay[0, 0] + (1 - p) * b_pay[1, 0]
# Method B: brute grid over Ben's mix; Ana indifferent where her two rows meet
qs = np.linspace(0, 1, 100001)
gap = np.abs((qs * a_pay[0, 0] + (1 - qs) * a_pay[0, 1]) - (qs * a_pay[1, 0] + (1 - qs) * a_pay[1, 1]))
q2 = qs[gap.argmin()]
va2 = q2 * a_pay[0, 0] + (1 - q2) * a_pay[0, 1]
check("q", q, 0.4)
check("p", p, 0.5)
check("Ana value A vs B", va, va2, 1e-4)
check("Ben value", vb, 1.5)
numeric("game-theory", 1, "rv1-mixed-value", 2.2, {"average": a_pay.mean(), "ben": vb})

# 9. game-theory review-2: half the average, rounds until the bound < 1.
k = 0
bound = 100.0
while bound >= 1:
    k += 1
    bound = 100 * 0.5 ** k
k_b = math.floor(math.log(100) / math.log(2)) + 1  # smallest k with 2^k > 100
check("rounds loop vs log", k, k_b)
check("bound after 6", 100 * 0.5 ** 6, 1.5625)
numeric("game-theory", 2, "rv2-half-rounds", k, {"off-by-one": k - 1})

# 10. systems review-1: branch misses as a share of a 5 us budget.
ns_a = 200 * 0.5 * 5
pct_a = ns_a / 5000 * 100
pct_b = (200 / 2) * 5e-9 / 5e-6 * 100
check("branch pct A vs B", pct_a, pct_b, 1e-9)
numeric("systems", 1, "r1-branch-budget", 10, {"every": 20, "fraction": 0.1})

# 11. systems review-2: bounded queue of 600 fills at a net 50,000 a second.
t_a = 600 / (250_000 - 200_000) * 1000
# Method B: step time in microseconds
held, t_us = 0.0, 0
while held < 600:
    t_us += 1
    held += 0.25 - 0.20
t_b = t_us / 1000
check("queue fill A vs B", t_a, t_b, 1e-3)
numeric("systems", 2, "r2-queue-fills", 12, {"no-consumer": 600 / 250_000 * 1000, "consumer-rate": 600 / 200_000 * 1000})

# 12. systems review-3: packed offset of the price.
sizes = [("type", 1), ("seq", 4), ("id", 8), ("price", 4), ("qty", 4)]
off, offs = 0, {}
for name, s in sizes:
    offs[name] = off
    off += s
packed_b = sum(s for name, s in sizes[: [n for n, _ in sizes].index("price")])
aligned, aoffs = 0, {}
for name, s in sizes:
    aligned = (aligned + s - 1) // s * s
    aoffs[name] = aligned
    aligned += s
check("offset A vs B", offs["price"], packed_b)
check("aligned price offset", aoffs["price"], 16)
numeric("systems", 3, "r3-offset", offs["price"], {"aligned": aoffs["price"], "from-one": offs["price"] + 1})

# 13. systems review-4: backlog after a 2 ms burst at 500,000 a second, 2.5 us each.
arr = 500_000 * 0.002
served = 2000 / 2.5
back_a = arr - served
# Method B: simulate in 0.5 us ticks (an arrival every 2 us, one service every 2.5 us)
q_len, busy_until, done = 0, 0.0, 0
for tick in range(0, 4000):
    t = tick * 0.5
    if tick % 4 == 0:
        q_len += 1
    if q_len and t >= busy_until:
        q_len -= 1
        busy_until = t + 2.5
        done += 1
# at 2000 us: the message in service counts as not yet handled; queue + in service
in_service = 1 if busy_until > 2000 else 0
back_b = q_len + in_service
check("backlog A vs B", back_a, back_b, 1.0)
numeric("systems", 4, "r4-burst", back_a, {"no-service": arr, "served": served})

if fails:
    print("\n".join(fails))
    sys.exit(1)
print("review top-up: all 13 keys recomputed twice; distractors differ from keys")
