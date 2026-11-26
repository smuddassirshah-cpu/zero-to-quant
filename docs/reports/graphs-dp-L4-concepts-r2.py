#!/usr/bin/env python3
"""Concept audit, round 2: graphs-dp level 4 (l14 to l17, review-4, homework-4).

Recomputes every stated value and slip by exact enumeration, brute force, exact value
iteration (fractions) and Monte Carlo, independently of the author's scripts. Runs every
Python code widget's solution, starter and mutants in CPython against the hidden tests.

Exit 0 when every check passes. A check that fails because the content is deficient stays
failing: those are the findings of docs/reviews/audit-graphs-dp-4-r2.md (each is tagged
FINDING n in its name; each passes once the audit's fix for it is applied). Run from the repository root or anywhere:
    python docs/reports/graphs-dp-L4-concepts-r2.py

Fix pass (re-pointed, old text only): the mutant total check now counts 100, the 85
read here plus the 15 mutants the fix pass added for findings 1, 2, 3 and 9. No other
check was changed.
"""
import itertools, json, math, os, re, sys, time, heapq
from collections import Counter, deque
from fractions import Fraction as F
from functools import lru_cache

import numpy as np

sys.setrecursionlimit(20000)
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "app", "content", "courses", "graphs-dp")
L = {n: json.load(open(os.path.join(ROOT, n + ".json"), encoding="utf-8"))
     for n in ["l14-knapsack", "l15-common-subsequence", "l16-grid-paths", "l17-dice-stopping", "review-4", "homework-4"]}
l14, l15, l16, l17, rev, hw = (L[k] for k in L)
rng = np.random.default_rng(20261126)
FAILS, N = [], [0]


def chk(name, cond, detail=""):
    N[0] += 1
    if not cond:
        FAILS.append(name)
    print(("ok   " if cond else "FAIL ") + name + (("  [" + str(detail) + "]") if detail != "" else ""))


def note(msg):
    print("note " + msg)


def close(a, b, tol=5e-5):
    return abs(float(a) - float(b)) <= tol


# ------------------------------------------------------------------ helpers (independent implementations)
def knap_brute(ws, vs, cap):
    best, packs = 0, []
    for mask in range(1 << len(ws)):
        idx = [i for i in range(len(ws)) if mask >> i & 1]
        if sum(ws[i] for i in idx) <= cap:
            v = sum(vs[i] for i in idx)
            if v > best:
                best, packs = v, [idx]
            elif v == best:
                packs.append(idx)
    return best, packs


def knap_by_value(ws, vs, cap):
    """Independent of the lesson's table: least weight for each exact value (K&T 11.8 table)."""
    V = sum(vs)
    INF = float("inf")
    least = [0] + [INF] * V
    for w, v in zip(ws, vs):
        for t in range(V, v - 1, -1):
            if least[t - v] + w < least[t]:
                least[t] = least[t - v] + w
    return max(t for t in range(V + 1) if least[t] <= cap)


def knap_table(ws, vs, cap):
    n = len(ws)
    b = [[0] * (cap + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(cap + 1):
            b[i][w] = b[i - 1][w]
            if ws[i - 1] <= w:
                b[i][w] = max(b[i][w], b[i - 1][w - ws[i - 1]] + vs[i - 1])
    return b


def rule_pack(ws, vs, cap):
    """The pack the lesson's tie rule defines, by brute force: among optimal packs, leave out the
    last item if any optimal pack does, then the one before it, and so on."""
    _, packs = knap_brute(ws, vs, cap)
    n = len(ws)
    return sorted(min(packs, key=lambda p: tuple(1 if i in p else 0 for i in range(n - 1, -1, -1))))


def lcs_brute(a, b):
    """Longest common subsequence by listing subsequences of the shorter string (small inputs)."""
    if len(a) > len(b):
        a, b = b, a

    def is_sub(s, t):
        it = iter(t)
        return all(c in it for c in s)
    for k in range(len(a), -1, -1):
        found = {tuple(a[i] for i in c) for c in itertools.combinations(range(len(a)), k)}
        found = {s for s in found if is_sub(s, b)}
        if found:
            return k, found
    return 0, {()}


def lcs_memo(a, b):
    @lru_cache(None)
    def go(i, j):
        if i == len(a) or j == len(b):
            return 0
        if a[i] == b[j]:
            return 1 + go(i + 1, j + 1)
        return max(go(i + 1, j), go(i, j + 1))
    return go(0, 0)


def edit_bfs(a, b, alphabet=None):
    """Edit distance by breadth-first search over strings (insert, delete, replace): no table."""
    alphabet = alphabet or sorted(set(a) | set(b))
    seen, q = {a}, deque([(a, 0)])
    lim = max(len(a), len(b))
    while q:
        s, d = q.popleft()
        if s == b:
            return d
        nxt = set()
        for i in range(len(s) + 1):
            for c in alphabet:
                nxt.add(s[:i] + c + s[i:])
            if i < len(s):
                nxt.add(s[:i] + s[i + 1:])
                for c in alphabet:
                    nxt.add(s[:i] + c + s[i + 1:])
        for t in nxt:
            if t not in seen and len(t) <= lim:
                seen.add(t)
                q.append((t, d + 1))


def edit_memo(a, b):
    @lru_cache(None)
    def go(i, j):
        if i == len(a):
            return len(b) - j
        if j == len(b):
            return len(a) - i
        if a[i] == b[j]:
            return go(i + 1, j + 1)
        return 1 + min(go(i + 1, j), go(i, j + 1), go(i + 1, j + 1))
    return go(0, 0)


def routes(grid):
    """Every right/down route through open cells, by enumeration."""
    R, Cc = len(grid), len(grid[0])
    out = []

    def go(i, j, path):
        if i >= R or j >= Cc or grid[i][j] == 1:
            return
        path = path + [(i, j)]
        if (i, j) == (R - 1, Cc - 1):
            out.append(path)
            return
        go(i + 1, j, path)
        go(i, j + 1, path)
    go(0, 0, [])
    return out


def min_cost_dag(costs):
    """Cheapest right/down route by a heap search on the DAG (not the lesson's table)."""
    R, Cc = len(costs), len(costs[0])
    heap, done = [(costs[0][0], 0, 0)], set()
    while heap:
        d, i, j = heapq.heappop(heap)
        if (i, j) in done:
            continue
        done.add((i, j))
        if (i, j) == (R - 1, Cc - 1):
            return d
        for a, b in ((i + 1, j), (i, j + 1)):
            if a < R and b < Cc:
                heapq.heappush(heap, (d + costs[a][b], a, b))


def stop_exact(n, quotes):
    qs = [F(str(q)) for q in quotes]
    v = sum(qs) / len(qs)
    vals = [v]
    for _ in range(n - 1):
        v = sum(max(q, v) for q in qs) / len(qs)
        vals.append(v)
    return vals


def best_policy_enum(n, quotes):
    """Largest expected payoff over ALL stop-set policies (a set of accepted quotes per stage)."""
    qs = [F(str(q)) for q in quotes]
    k = len(qs)
    best = None
    stages = [list(itertools.product([0, 1], repeat=k)) for _ in range(n - 1)]
    for pol in itertools.product(*stages):
        v = sum(qs) / k
        for acc in reversed(pol):          # acc for the stage just before the tail already valued
            v = sum(q if a else v for q, a in zip(qs, acc)) / k
        if best is None or v > best[0]:
            best = (v, pol)
    return best


def ex(t):
    """A test's expected value: the JSON holds it as Python source."""
    return eval(t["expect"]) if isinstance(t["expect"], str) else t["expect"]


def widget(doc, i):
    return (doc.get("screens") or doc.get("items"))[i]["widget"]


def cells(doc, i):
    return (doc.get("screens") or doc.get("items"))[i]["canvas"]["params"]["cells"]


# ================================================================== l14 knapsack
print("\n== l14 knapsack")
W4, V4 = [1, 3, 4, 5], [10, 40, 50, 70]
best, packs = knap_brute(W4, V4, 7)
chk("l14 s0: best pack is B and C, £90, unique", best == 90 and packs == [[1, 2]], (best, packs))
chk("l14 s0: greedy by £/kg takes D then A for £80", knap_brute([5, 1], [70, 10], 7)[0] == 80 and 70 / 5 > 40 / 3 > 50 / 4 > 10)
chk("l14 s0: A+B+C weigh 8 kg; any pack with D tops out at £80", sum(W4[:3]) == 8 and max(sum(V4[i] for i in p) for m in range(16) for p in [[i for i in range(4) if m >> i & 1]] if 3 in p and sum(W4[i] for i in p) <= 7) == 80)
chk("l14 s0: 16 packs for 4 items, 2^40 over a trillion", 2 ** 4 == 16 and 2 ** 40 > 10 ** 12, 2 ** 40)
tab = knap_table(W4, V4, 7)
chk("l14: full table shown on screens 5, 6, 9 equals the DP", all([[str(x) for x in r] for r in tab] == cells(l14, s) for s in (5, 6, 9)))
chk("l14 s1: best[2][4] = 50; slips 40 (B alone), 90 (needs C)", tab[2][4] == 50 == widget(l14, 1)["answer"] and V4[1] == 40 and tab[3][7] == 90)
chk("l14 s2: best[3][7] = max(best[2][7], best[2][3] + 50) = max(50, 90)", (tab[2][7], tab[2][3] + 50, tab[3][7]) == (50, 90, 90))
chk("l14 s3: row ABC answers", [r[1]["answer"] for r in widget(l14, 3)["rows"]] == tab[3][1:])
chk("l14 s4: row ABCD answers 70, 80, 90", [c["answer"] for c in widget(l14, 4)["rows"][0][1:]] == tab[4][5:])
# walk back
w, path, took = 7, ["r5c8"], []
for i in range(4, 0, -1):
    if tab[i][w] != tab[i - 1][w]:
        took.append(i - 1)
        w -= W4[i - 1]
    path.append("r%dc%d" % (i, w + 1))
chk("l14 s5: walk visits the keyed cells and takes C and B", path == widget(l14, 5)["answer"] and sorted(took) == [1, 2], path)
w, path = 7 - 5, ["r5c8", "r4c3"]            # the 'took-d' slip: take D at the corner, then walk properly
for i in range(3, 0, -1):
    if tab[i][w] != tab[i - 1][w]:
        w -= W4[i - 1]
    path.append("r%dc%d" % (i, w + 1))
chk("l14 s5: slip took-d is the walk after wrongly taking D", path == widget(l14, 5)["wrong"][0]["set"], path)


def knapsack_1d(weights, values, cap):
    dp = [0] * (cap + 1)
    trace = []
    for wt, val in zip(weights, values):
        for w_ in range(wt, cap + 1):
            dp[w_] = max(dp[w_], dp[w_ - wt] + val)
        trace.append(list(dp))
    return dp[cap], trace


r, tr = knapsack_1d([2, 3], [30, 40], 6)
chk("l14 s7: upward one-row returns 90; after item 1 the row is 0,0,30,30,60,60,90", r == 90 and tr[0] == [0, 0, 30, 30, 60, 60, 90])
chk("l14 s7: true 0/1 answer 70; 80 = two of item 2; 60 = two of item 1", knap_brute([2, 3], [30, 40], 6)[0] == 70 and 2 * 40 == 80 and 2 * 30 == 60)
chk("l14 s8: grams table 5 x 7001 cells against 5 x 8: about 1,000 times", 800 < 5 * 7001 / 40 < 1100, 5 * 7001 / 40)
TW, TP = [4, 3, 5, 2, 6], [18, 11, 21, 6, 25]
best, packs = knap_brute(TW, TP, 10)
chk("l14 s10: best plan A and E, 43, unique", best == 43 and packs == [[0, 4]], (best, packs))
order = sorted(range(5), key=lambda i: -TP[i] / TW[i])
room, g = 10, 0
for i in order:
    if TW[i] <= room:
        room -= TW[i]
        g += TP[i]
chk("l14 s10: greedy by ratio takes A then C: 39 with one unit unused; B+C+D = 38 on 10 units", order[:2] == [0, 2] and g == 39 and room == 1 and TP[1] + TP[2] + TP[3] == 38 and TW[1] + TW[2] + TW[3] == 10)
chk("l14 s10: ratios in the table", ["%.2f" % (p / w_) for p, w_ in zip(TP, TW)] == ["4.50", "3.67", "4.20", "3.00", "4.17"])
pence = [w_ * 12345 for w_ in TW]          # the same trades with risk in a fine unit: capacity is huge
chk("l14 s10 (basis of finding 6): a table indexed by profit (6 x 82 cells) solves the fine-unit case exactly",
    knap_by_value(pence, TP, 10 * 12345) == 43 and sum(TP) + 1 == 82)
chk("FINDING 6: l14 s10 explain does not say that no table works once the budget is in pence", "no table trick saves us" not in l14["screens"][10]["explain"]["text"],
    "the profit-indexed table above solves it exactly with 6 x 82 cells")
chk("l14 quiz: capacity 0 -> 0; all fit -> 18 (slips 7, 13); greedy 60 against 90; X+Y = 11 kg",
    knap_brute([3, 4], [20, 30], 0)[0] == 0 and knap_brute([1, 2, 3], [5, 6, 7], 10)[0] == 18 and knap_brute([6, 5, 5], [60, 45, 45], 10)[0] == 90 and 60 / 6 > 45 / 5)
t0 = time.time()
row = [0] * 50001
for _ in range(20):                       # 20 of 200 rows, timed, then scaled
    for w_ in range(50000, 99, -1):
        if row[w_ - 100] + 7 > row[w_]:
            row[w_] = row[w_ - 100] + 7
t = (time.time() - t0) * 10
note("timing-dependent: l14 quiz 3 '10^7 cells in a few seconds': CPython here about %.1f s for 200 rows of 50,000" % t)
chk("l14 quiz 3: 200 x 50,000 = 10^7", 200 * 50000 == 10 ** 7)

# ================================================================== l15 LCS and edit distance
print("\n== l15 common subsequence")
k, subs = lcs_brute("HEDGE", "EDGY")
chk("l15 s0: LCS of HEDGE and EDGY is EDG, length 3, unique", k == 3 and subs == {tuple("EDG")}, subs)
chk("l15 s0: 2^20 subsequences is over a million; 21 x 21 cells is about 400", 2 ** 20 > 10 ** 6 and 21 * 21 == 441)


def lcs_tab(a, b):
    t = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            t[i][j] = t[i - 1][j - 1] + 1 if a[i - 1] == b[j - 1] else max(t[i - 1][j], t[i][j - 1])
    return t


T = lcs_tab("HEDGE", "EDGY")
chk("l15: every prefix cell equals brute force", all(T[i][j] == lcs_brute("HEDGE"[:i], "EDGY"[:j])[0] for i in range(6) for j in range(5)))
chk("l15: full table on screens 5, 6, 7 equals the DP", all([[str(x) for x in r] for r in T] == cells(l15, s) for s in (5, 6, 7)))
chk("l15 s1-s4: keyed cells", T[2][1] == 1 and T[3][2] == 2 and [c["answer"] for c in widget(l15, 3)["rows"][0][1:]] == T[3][1:]
    and [[c["answer"] for c in r[1:]] for r in widget(l15, 4)["rows"]] == [T[4][1:], T[5][1:]])
i, j, kept, path = 5, 4, [], ["r6c5"]
while i and j:
    if "HEDGE"[i - 1] == "EDGY"[j - 1]:
        kept.append("r%dc%d" % (i + 1, j + 1))
        i, j = i - 1, j - 1
    elif T[i - 1][j] >= T[i][j - 1]:
        i -= 1
    else:
        j -= 1
    path.append("r%dc%d" % (i + 1, j + 1))
chk("l15 s5: walk (up on a tie) keeps G, D, E at the keyed cells; path as drawn",
    kept == widget(l15, 5)["answer"] and path == l15["screens"][5]["explain"]["canvas"]["paths"][0]["cells"], path)
try:
    a, b = "HEDGE", "EDGY"
    m, n = 5, 4
    t = [[0] * (n + 1) for _ in range(m + 1)]
    where = None
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            where = (i, j)
            if a[i] == b[j]:
                t[i][j] = t[i - 1][j - 1] + 1
            else:
                t[i][j] = max(t[i - 1][j], t[i][j - 1])
    err = None
except IndexError as e:
    err = str(e)
chk("l15 s7: the a[i], b[j] version raises IndexError at i = 1, j = 4", err == "string index out of range" and where == (1, 4), (err, where))
chk("l15 s8: edit distance HEDGE -> EDGY is 2 (BFS over edits, and memo recursion)", edit_bfs("HEDGE", "EDGY") == 2 == edit_memo("HEDGE", "EDGY"))
chk("l15 s8: insert/delete-only distance is 5 + 4 - 2*3 = 3; one delete gives EDGE, not EDGY", 5 + 4 - 2 * 3 == 3 and "HEDGE"[1:] == "EDGE")
pos = sum(x != y for x, y in zip("HEDGE", "EDGY")) + 1
why4 = [o for o in widget(l15, 8)["options"] if o["id"] == "four"][0]["why"]
chk("FINDING 5: l15 s8 option 'four': the mistake its `why` names gives 4", pos == 4 or "outside a matching position" not in why4,
    "changing every letter outside a matching position costs %d (4 replaces and a delete), not 4" % pos)


def edit_tab(a, b):
    d = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1):
        d[i][0] = i
    for j in range(len(b) + 1):
        d[0][j] = j
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            d[i][j] = d[i - 1][j - 1] if a[i - 1] == b[j - 1] else 1 + min(d[i - 1][j], d[i][j - 1], d[i - 1][j - 1])
    return d


ED = edit_tab("HEDGE", "EDGY")
note("edit-distance table for HEDGE/EDGY (for the fix of finding 8): " + "; ".join(" ".join(map(str, r)) for r in ED))
chk("FINDING 8: l15 s9 canvas: the grid on the edit-distance screen is the edit-distance table",
    cells(l15, 9) == [[str(x) for x in r] for r in ED] or bool(l15["screens"][9]["canvas"].get("state", {}).get("caption")),
    "it shows the LCS table (first row and column 0) with no caption, beside prose saying they count up")
ours = ["B100", "S50", "B100", "B200", "S100", "S50"]
brok = ["B100", "B100", "S50", "B200", "S75", "S100", "S50"]
k, subs = lcs_brute(ours, brok)
chk("l15 s10: logs' LCS has length 5, so 2 broker fills and 1 of ours are unmatched", k == 5 and len(brok) - k == 2 and len(ours) - k == 1)
un = set()
for ci in itertools.combinations(range(6), 5):
    for cj in itertools.combinations(range(7), 5):
        if all(ours[x] == brok[y] for x, y in zip(ci, cj)):
            un.add(tuple(brok[y] for y in range(7) if y not in cj))
s10 = l15["screens"][10]
said = " ".join([s10["feedback"]["correct"], s10["feedback"]["byKey"]["one"], s10["explain"]["text"]])
chk("FINDING 7: l15 s10: the unmatched broker fills the feedback names (a Buy 100 and the Sell 75) are the same under every longest match",
    un == {("B100", "S75")} or "Buy 100" not in said, "longest matches leave %s" % sorted(un))
chk("l15 s10: slip 1 = matching by counts (7 - 6, or the multiset difference)", 7 - 6 == 1 and sum((Counter(brok) - Counter(ours)).values()) == 1)
t = [[0] * 3 for _ in range(3)]
for i in (1, 2):
    for j in (1, 2):
        t[i][j] = max(t[i - 1][j - 1] + 1, t[i - 1][j], t[i][j - 1])
chk("l15 quiz: buggy diagonal returns 2 for AB/CD; RDS.A/RDSA = 1; 10^4 x 10^4 = 10^8",
    t[2][2] == 2 and edit_bfs("RDS.A", "RDSA") == 1 and 10 ** 4 * 10 ** 4 == 10 ** 8)

# ================================================================== l16 grid paths
print("\n== l16 grid paths")
open_ = lambda r, c: [[0] * c for _ in range(r)]
chk("l16 s0: 3 x 3 grid has 6 routes; slips 9 cells, 2^4 = 16", len(routes(open_(3, 3))) == 6)
chk("l16 s0: 20 x 20 grid has over 35 billion routes", math.comb(38, 19) > 35 * 10 ** 9, math.comb(38, 19))
g2 = [[0, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 0]]


def ways_tab(grid):
    R, Cc = len(grid), len(grid[0])
    return [[sum(1 for p in routes([row[:j + 1] for row in grid[:i + 1]])) for j in range(Cc)] for i in range(R)]


wt2 = ways_tab(g2)
chk("l16 s1: 3 x 3 table 2, 3, 3, 6 by enumeration", [[c["answer"] for c in r[1:]] for r in widget(l16, 1)["rows"]] == [x[1:] for x in ways_tab(open_(3, 3))[1:]])
keyed = [[c["answer"] if isinstance(c, dict) else 0 for c in r[1:]] for r in widget(l16, 2)["rows"]]
chk("l16 s2: blocked-grid counts by enumeration; corner 7; open grid 35", keyed == [x[1:] for x in wt2[1:]] and wt2[3][4] == 7 and math.comb(7, 3) == 35, wt2)
g3 = [[0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
ones = [[1] * 5 for _ in range(3)]
for i in (1, 2):
    for j in range(1, 5):
        ones[i][j] = ones[i - 1][j] + ones[i][j - 1]
zb = [[1, 1, 0, 1, 1], [1, 0, 0, 0, 0], [1, 0, 0, 0, 0]]
for i in (1, 2):
    for j in range(1, 5):
        zb[i][j] = zb[i - 1][j] + zb[i][j - 1]
chk("l16 s3: truly 9 routes; all-ones edges give 15; zeroing only the block gives 12",
    len(routes(g3)) == 9 and ones[2][4] == 15 and zb[2][4] == 12 and ways_tab(g3) == [[1, 1, 0, 0, 0], [1, 2, 2, 2, 2], [1, 3, 5, 7, 9]])
FEES = [[3, 1, 4, 2], [2, 5, 1, 3], [6, 2, 2, 1]]
allr = routes(open_(3, 4))
cost = lambda p, c=FEES: sum(c[i][j] for i, j in p)
cheapest = sorted(allr, key=cost)
tot = [[min(cost(p) for p in routes(open_(i + 1, j + 1))) for j in range(4)] for i in range(3)]
chk("l16 s4: cheapest totals by enumeration match the table", tot == [[3, 4, 8, 10], [5, 9, 9, 12], [11, 11, 11, 12]]
    and [[c["answer"] if isinstance(c, dict) else int(c) for c in r[1:]] for r in widget(l16, 4)["rows"]] == tot)
chk("l16 s5: the £12 route is unique and is the keyed route", cost(cheapest[0]) == 12 and cost(cheapest[1]) > 12
    and ["r%dc%d" % (i + 1, j + 1) for i, j in cheapest[0]] == widget(l16, 5)["answer"])
via = [(int(s[1]) - 1, int(s[3]) - 1) for s in widget(l16, 5)["wrong"][0]["set"]]
chk("l16 s5: slip route costs 13; every route through the £5 cell costs at least 13", cost(via) == 13 and min(cost(p) for p in allr if (1, 1) in p) == 13)
chk("l16 s6/s8: C(32,16) = 601,080,390; C(10,5) = 252; C(8,4) = 70; 6 x 6 by enumeration", math.comb(32, 16) == 601080390 and math.comb(10, 5) == 252 == len(routes(open_(6, 6))) and math.comb(8, 4) == 70)
pas = [[math.comb(i + j, i) for j in range(5)] for i in range(5)]
chk("l16 s8: Pascal grid shown; shaded anti-diagonal is 1 4 6 4 1", [[str(x) for x in r] for r in pas] == cells(l16, 8) and [pas[i][4 - i] for i in range(5)] == [1, 4, 6, 4, 1])
p3 = math.comb(4, 3) * 0.55 ** 3 * 0.45
ups = (rng.random((2_000_000, 4)) < 0.55).sum(axis=1)
mc = (ups == 3).mean()
chk("l16 s9: P(3 ups in 4) = 0.299475 -> 0.2995; Monte Carlo agrees", close(p3, 0.2995, 5e-4) and abs(mc - p3) < 4 * math.sqrt(p3 * (1 - p3) / 2e6), "exact %.6f mc %.6f" % (p3, mc))
chk("l16 s9: slips 0.0749 (one path), 0.1664 (0.55^3)", close(0.55 ** 3 * 0.45, 0.0749) and close(0.55 ** 3, 0.1664))


def del_routes(r, c):
    @lru_cache(None)
    def go(i, j):
        if i < 0 or j < 0:
            return 0
        if i == 0 and j == 0:
            return 1
        return go(i - 1, j) + go(i, j - 1) + go(i - 1, j - 1)
    return go(r - 1, c - 1)


chk("l16 quiz: with a diagonal step a 2 x 2 grid has 3 routes, not 2; blocked start 0", del_routes(2, 2) == 3 and len(routes(open_(2, 2))) == 2 and len(routes([[1, 0, 0], [0, 0, 0], [0, 0, 0]])) == 0)

# ================================================================== l17 dice stopping
print("\n== l17 dice stopping")
V = stop_exact(200, range(1, 7))            # V[n-1] = V_n, exact fractions
chk("l17: V1..V4 = 7/2, 17/4, 14/3, 89/18", V[:4] == [F(7, 2), F(17, 4), F(14, 3), F(89, 18)], [str(x) for x in V[:5]])
thr = [1] + [min(f for f in range(1, 7) if f >= V[n - 2]) for n in range(2, 201)]
chk("l17: thresholds 1, 4, 5, 5, 5, then 6 from six rolls on", thr[:6] == [1, 4, 5, 5, 5, 6] and set(thr[5:]) == {6})
chk("l17 s5: keyed table 5 / 4.6667 and 5 / 4.9444", [(r[1]["answer"], r[2]["answer"]) for r in widget(l17, 5)["rows"][2:]] == [(5, 4.6667), (5, 4.9444)] and close(V[2], 4.6667) and close(V[3], 4.9444))
chk("l17 s2/s4 slips: 2.5, 5, 3.5; 4.25; 4.1667 = 11/6 + 4/6 x 3.5", F(15, 6) == F(5, 2) and F(4 + 5 + 6, 3) == 5 and close(F(11, 6) + F(4, 6) * F(7, 2), 4.1667))
bv, bpol = best_policy_enum(3, range(1, 7))
chk("l17: over all 64 x 64 stop-set policies the 3-roll optimum is 14/3, stopping on {5,6} then {4,5,6}",
    bv == F(14, 3) and bpol == ((0, 0, 0, 0, 1, 1), (0, 0, 0, 1, 1, 1)), (str(bv), bpol))
chk("l17 s5/s6: increments shrink; V_n rises and stays below 6; V10 = 5.6502; V50 = 5.9998", all(V[i + 1] - V[i] < V[i] - V[i - 1] for i in range(1, 60))
    and all(V[i] < V[i + 1] < 6 for i in range(199)) and close(V[9], 5.650218, 5e-7) and close(V[49], 5.9998))
chk("l17 s7: dice_value(200) rounds to 6.0 at 6 places", round(float(V[199]), 6) == 6.0)
chk("l17 s8: threshold 4 at the first of three rolls is worth 4.625", F(15, 6) + F(3, 6) * F(17, 4) == F(37, 8) and float(F(37, 8)) == 4.625)


def play(n, thresholds, reps):
    rolls = rng.integers(1, 7, size=(reps, n))
    out = rolls[:, n - 1].astype(float)
    for s in range(n - 2, -1, -1):        # stage s has n - s rolls left
        out = np.where(rolls[:, s] >= thresholds[s], rolls[:, s], out)
    return out


for n, th in ((2, [4]), (3, [5, 4]), (4, [5, 5, 4])):
    x = play(n, th, 3_000_000)
    se = x.std() / math.sqrt(len(x))
    chk("l17 MC: %d-roll game played with thresholds %s is worth %.4f" % (n, th, float(V[n - 1])), abs(x.mean() - float(V[n - 1])) < 4 * se, "mc %.4f se %.4f" % (x.mean(), se))
x = play(3, [4, 4], 3_000_000)
se = x.std() / math.sqrt(len(x))
chk("l17 MC: comparing every roll with 3.5 in the 3-roll game gives 4.625, below 4.6667", abs(x.mean() - 4.625) < 4 * se and x.mean() + 6 * se < 14 / 3, "mc %.4f se %.4f" % (x.mean(), se))
BIDS = [99.0, 99.2, 99.5, 99.9]
bvals = stop_exact(3, BIDS)
bv, bpol = best_policy_enum(3, BIDS)
chk("l17 s9: dealers 99.4, 99.55, 99.6375; best over all accept-set policies; accept 99.9 only, then 99.5 or better",
    [float(v) for v in bvals] == [99.4, 99.55, 99.6375] and bv == bvals[2] and bpol == ((0, 0, 0, 1), (0, 0, 1, 1)), [str(v) for v in bvals])
chk("l17 s9: slip first-best = 99.625 (accept 99.5 and 99.9 first)", (F("99.5") + F("99.9")) / 4 + F(1, 2) * bvals[1] == F("99.625"))
bids = rng.choice(BIDS, size=(3_000_000, 3))
px = np.where(bids[:, 0] >= 99.9, bids[:, 0], np.where(bids[:, 1] >= 99.5, bids[:, 1], bids[:, 2]))
px2 = np.where(bids[:, 0] >= 99.5, bids[:, 0], np.where(bids[:, 1] >= 99.5, bids[:, 1], bids[:, 2]))
se = px.std() / math.sqrt(len(px))
chk("l17 s9 MC: best policy 99.6375 beats the first-best slip 99.625", abs(px.mean() - 99.6375) < 4 * se and abs(px2.mean() - 99.625) < 4 * se and (px - px2).mean() > 6 * (px - px2).std() / math.sqrt(len(px)),
    "mc %.5f and %.5f, se %.5f" % (px.mean(), px2.mean(), se))
chk("l17 s10: node value max(8.00, 7.40) = 8.00; average 7.70; holding gives up 0.60", max(8.0, 7.4) == 8.0 and (8.0 + 7.4) / 2 == 7.7 and round(8.0 - 7.4, 2) == 0.6)


def sec(n, r):
    return 1 / n if r == 1 else (r - 1) / n * sum(1 / (i - 1) for i in range(r, n + 1))


best_r = max(range(1, 11), key=lambda r: sec(10, r))
chk("secretary n = 10: best r = 4 gives 0.3987; r = 5 gives 0.3983; 1/e = 0.3679", best_r == 4 and close(sec(10, 4), 0.3987) and close(sec(10, 5), 0.3983) and close(1 / math.e, 0.3679))
perms = np.array(list(itertools.permutations(range(10))), dtype=np.int8)     # all 10! orders, exact
for r in (4, 5):
    pre = perms[:, :r - 1].max(axis=1)
    rest = perms[:, r - 1:]
    hit = rest > pre[:, None]
    first = hit.argmax(axis=1)
    win = hit.any(axis=1) & (rest[np.arange(len(rest)), first] == 9)
    chk("secretary n = 10, r = %d: exact count over all 10! orders equals the formula" % r, abs(win.mean() - sec(10, r)) < 1e-12, "%.6f" % win.mean())


def sec_optimal(n):
    """Optimal stopping by backward induction on 'is the current candidate the best so far'."""
    v = F(0)                                  # value of continuing past candidate n
    for i in range(n, 0, -1):
        stop = F(i, n)                        # P(best overall | best so far at i)
        v = F(1, i) * max(stop, v) + F(i - 1, i) * v
    return v


chk("secretary n = 10: the optimal stopping value (backward induction) is the rule's 0.3987", close(sec_optimal(10), sec(10, 4), 1e-12))
opt = [float(sec_optimal(n)) for n in range(1, 301)]
chk("secretary: n = 100 wins about 0.371; the optimum never rises with n and stays above 1/e", close(opt[99], 0.371, 5e-4) and all(a >= b - 1e-15 for a, b in zip(opt, opt[1:])) and min(opt) > 1 / math.e, "n=100 %.5f" % opt[99])
sim = rng.random((2_000_000, 10)).argsort(axis=1)
pre = sim[:, :3].max(axis=1)
hit = sim[:, 3:] > pre[:, None]
win = hit.any(axis=1) & (sim[:, 3:][np.arange(len(sim)), hit.argmax(axis=1)] == 9)
se = math.sqrt(0.24 / 2e6)
chk("h4-secretary MC: simulation converges to 0.3987, not to 1/e", abs(win.mean() - sec(10, 4)) < 4 * se and win.mean() - 1 / math.e > 20 * se, "mc %.5f se %.5f" % (win.mean(), se))

# ================================================================== review-4 and homework-4
print("\n== review-4, homework-4")
chk("r4-knap-cell: 60; slips 50, 100", max(tab[2][6], tab[2][2] + 50) == 60 and tab[2][6] == 50 and tab[2][6] + 50 == 100 and tab[2] == [0, 10, 10, 40, 50, 50, 50, 50])
k, subs = lcs_brute("TRADE", "TREAD")
chk("r4-lcs-trade: 4, and TRAD is one", k == 4 and tuple("TRAD") in subs, subs)
gr = [[0, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]]
chk("r4-paths-edge: 6 routes; open grid 10", len(routes(gr)) == 6 and len(routes(open_(3, 4))) == 10)
d4 = stop_exact(2, range(1, 5))
x = rng.integers(1, 5, size=(2_000_000, 2))
pay = np.where(x[:, 0] >= 3, x[:, 0], x[:, 1])
chk("r4-d4: value 3 (exact, all policies, Monte Carlo); slips 2.5, 3.5", d4 == [F(5, 2), F(3)] and best_policy_enum(2, range(1, 5))[0] == 3 and abs(pay.mean() - 3) < 4 * pay.std() / math.sqrt(2e6), "mc %.4f" % pay.mean())
chk("r4-edit: BUY -> BYE is 2 by BFS", edit_bfs("BUY", "BYE") == 2)
MC2 = [[4, 2, 7], [1, 8, 1]]
rc = sorted(cost(p, MC2) for p in routes(open_(2, 3)))
chk("r4-mincost: 14, two routes tie; right-down-right is 15; without the start fee 10", rc == [14, 14, 15] and 14 - 4 == 10)
chk("r4-dealers: 99.75", stop_exact(2, [99.0, 100.0])[1] == F("99.75") and best_policy_enum(2, [99.0, 100.0])[0] == F("99.75"))
bh, ph = knap_brute([2, 3, 4, 5], [3, 4, 5, 6], 5)
chk("h4-knap: 7 with the 2 kg and 3 kg items; slips 6, 3", bh == 7 and ph == [[0, 1]])
hv = stop_exact(3, [99.0, 99.4, 100.0])
chk("h4-dealers-order: 99.4667, 99.6444, 99.7630; 100.0 the only bid above each", all(close(a, b) for a, b in zip(hv, [99.4667, 99.6444, 99.7630])) and F("99.4") < hv[0] < hv[1] < 100
    and best_policy_enum(3, [99.0, 99.4, 100.0])[0] == hv[2])
gh = [[0, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 1, 0], [1, 0, 0, 0, 0], [0, 0, 1, 0, 0]]
gh2 = [r[:] for r in gh]
gh2[3][0] = 0
chk("h4-paths: 9 routes; 11 if the first-column block is counted open; rows as explained", len(routes(gh)) == 9 and len(routes(gh2)) == 11
    and ways_tab(gh) == [[1, 1, 1, 1, 1], [1, 0, 1, 2, 3], [1, 1, 2, 0, 3], [0, 1, 3, 3, 6], [0, 1, 0, 3, 9]])
chk("h4-edit: SATURDAY -> SUNDAY is 3; LCS 5 so insert/delete-only is 4", edit_memo("SATURDAY", "SUNDAY") == 3 == edit_bfs("SATURDAY", "SUNDAY") and lcs_memo("SATURDAY", "SUNDAY") == 5)
chk("h4-risk-design model: 41 x 201 cells about 8,000; 2^40 about 10^12; £2,000,000 in pence is 2 x 10^8 columns", 41 * 201 == 8241 and 0.9e12 < 2 ** 40 < 1.2e12 and 2_000_000 * 100 == 2 * 10 ** 8
    and knap_brute([4, 5, 6], [18, 21, 25], 10)[0] == 43)

# ================================================================== code widgets in CPython
print("\n== code widgets: solutions, starters, mutants, expected values")


def run_tests(src, w, limit=None, budget=None):
    """Return (index of first failing test (1-based) or None, actual of that test)."""
    ns = {}
    try:
        exec(src, ns)
    except Exception as e:
        return 1, "load " + type(e).__name__
    for i, t in enumerate(w["tests"] if limit is None else w["tests"][:limit], 1):
        env = dict(ns)
        try:
            if t.get("setup"):
                exec(t["setup"], env)
            got = eval(t["call"], env)
        except Exception as e:
            return i, type(e).__name__
        if not got == ex(t):
            return i, got
    return None, None


code = []
for name, doc in L.items():
    for i, s in enumerate(doc.get("screens") or doc.get("items")):
        if s.get("widget", {}).get("kind") == "code":
            code.append((name, i, s))
n_mut = 0
for name, i, s in code:
    w = s["widget"]
    f, got = run_tests(w["solution"], w)
    chk("%s[%d]: solution passes its %d tests" % (name, i, len(w["tests"])), f is None, (f, got))
    f, got = run_tests(w["starter"], w)
    chk("%s[%d]: starter fails" % (name, i), f is not None)
    m = re.search(r"Check runs (\d+) hidden tests", w["how"])
    chk("%s[%d]: `how` count equals the number of tests" % (name, i), m and int(m.group(1)) == len(w["tests"]))
    keys = [int(k.split("-")[1]) for k in s["feedback"].get("byKey", {}) if k.startswith("test-")]
    chk("%s[%d]: every test-N line names an existing test" % (name, i), all(1 <= k <= len(w["tests"]) for k in keys), keys)
    bad = []
    for mi, mu in enumerate(w.get("mutants", [])):
        n_mut += 1
        if mu.get("timeout"):
            f, got = run_tests(mu["source"], w, limit=mu["test"] - 1)     # must pass everything before its test
            if f is not None:
                bad.append((mi, "fails early at", f))
            continue
        f, got = run_tests(mu["source"], w)
        sym = mu.get("symptom", "")
        if f != mu["test"]:
            bad.append((mi, "first fails", f, "stated", mu["test"]))
        elif "IndexError" not in sym and not re.search(r"(?<![\d.])" + re.escape(repr(got)) + r"(?![\d.])", sym):
            bad.append((mi, "symptom", sym, "got", got))
        elif "IndexError" in sym and got != "IndexError":
            bad.append((mi, "symptom IndexError, got", got))
    chk("%s[%d]: %d mutants first fail at their stated test with the stated symptom" % (name, i, len(w.get("mutants", []))), not bad, bad)
chk("100 mutants across the nine code widgets (85, plus 15 added by the fix pass)", n_mut == 100, n_mut)

# expected values recomputed by other methods
ws = [(i * 37) % 23 + 1 for i in range(60)]
vs = [(i * 53) % 41 + 5 for i in range(60)]
ws2 = [(i * 7) % 31 + 5 for i in range(120)]
vs2 = [(i * 11) % 47 + 1 for i in range(120)]
chk("l14 s6: 877 and 2054 by the value-indexed table (a different DP)", knap_by_value(ws, vs, 200) == 877 and knap_by_value(ws2, vs2, 1000) == 2054)
w6, w9 = widget(l14, 6), widget(l14, 9)
chk("l14 s6: small tests equal brute force", all(knap_brute(*eval(t["call"][len("knapsack"):]))[0] == ex(t) for t in w6["tests"][:8]))
chk("l14 s9: item tests equal the tie rule applied to brute-force optimal packs", all(rule_pack(*eval(t["call"][len("knapsack_items"):])) == ex(t) for t in w9["tests"][:9]))
wl, we = widget(l15, 6), widget(l15, 9)
chk("l15 s6: LCS tests equal memo recursion (and brute force when short)", all(lcs_memo(*map(tuple, eval(t["call"][len("lcs_length"):]))) == ex(t) for t in wl["tests"])
    and all(lcs_brute(*eval(t["call"][len("lcs_length"):]))[0] == ex(t) for t in wl["tests"][:9]))
chk("l15 s9: edit tests equal memo recursion (and BFS when short)", all(edit_memo(*eval(t["call"][len("edit_distance"):])) == ex(t) for t in we["tests"])
    and all(edit_bfs(*eval(t["call"][len("edit_distance"):])) == ex(t) for t in we["tests"][:7] + we["tests"][8:9]))
wc, wm = widget(l16, 6), widget(l16, 7)
chk("l16 s6: path-count tests equal route enumeration (17 x 17 by the binomial)", all(len(routes(eval(t["call"][len("count_paths"):]))) == ex(t) for t in wc["tests"][:9]))
cs = [[(i * 7 + j * 13) % 10 for j in range(40)] for i in range(30)]
chk("l16 s7: cost tests equal route enumeration; 30 x 40 = 132 by heap search", all(min(cost(p, g) for p in routes(open_(len(g), len(g[0])))) == ex(t)
    for t in wm["tests"][:8] for g in [eval(t["call"][len("min_path_cost"):])]) and min_cost_dag(cs) == 132)
wd = widget(l17, 7)
chk("l17 s7: value tests equal exact fractions; threshold tests equal the exact thresholds",
    all(round(float(V[int(re.search(r"\((\d+)\)", t["call"]).group(1)) - 1]), 6) == ex(t) for t in wd["tests"] if "dice_value" in t["call"])
    and all(thr[int(re.search(r"\((\d+)\)", t["call"]).group(1)) - 1] == ex(t) for t in wd["tests"] if "dice_threshold" in t["call"]))
wsv, wub = widget(hw, 4), widget(hw, 5)
ok = True
for t in wsv["tests"]:
    n_, q_ = eval(re.search(r"stop_value(\(.*?\]\))", t["call"]).group(1))
    ok &= round(float(stop_exact(n_, q_)[-1]), 6) == ex(t)
    if n_ <= 3 and len(q_) <= 4:
        ok &= best_policy_enum(n_, q_)[0] == stop_exact(n_, q_)[-1]
chk("h4-stop-value: tests equal exact fractions (and the best of all policies when small)", ok)


def unb(ws_, vs_, cap):            # capacity-outer formulation
    dp = [0] * (cap + 1)
    for c in range(1, cap + 1):
        dp[c] = max([dp[c - w_] + v_ for w_, v_ in zip(ws_, vs_) if w_ <= c], default=0)
    return dp[cap]


def unb_brute(ws_, vs_, cap):
    best = 0
    for counts in itertools.product(*[range(cap // w_ + 1) for w_ in ws_]):
        if sum(c * w_ for c, w_ in zip(counts, ws_)) <= cap:
            best = max(best, sum(c * v_ for c, v_ in zip(counts, vs_)))
    return best


ok = True
for t in wub["tests"]:
    env = {}
    if t.get("setup"):
        exec(t["setup"], env)
    a = eval(t["call"][len("unbounded_knapsack"):], env)
    ok &= unb(*a) == ex(t)
    if a[2] <= 13:
        ok &= unb_brute(*a) == ex(t)
chk("h4-unbounded: tests equal a capacity-outer table (and brute force when small)", ok)

# ------------------------------------------------------------------ wrong or correct programs the tests misjudge (findings)
print("\n== programs the hidden tests misjudge")
COST_ON_ALL = '''
def edit_distance(a, b):
    m, n = len(a), len(b)
    d = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        d[i][0] = i
    for j in range(n + 1):
        d[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            d[i][j] = min(d[i - 1][j], d[i][j - 1], d[i - 1][j - 1]) + cost
    return d[m][n]
'''
ns = {}
exec(COST_ON_ALL, ns)
chk("the 'min of three, plus cost' edit distance is wrong: it gives 0 for ('aa', 'a'), true 1", ns["edit_distance"]("aa", "a") == 0 and edit_bfs("aa", "a") == 1)
f, got = run_tests(COST_ON_ALL, we)
chk("FINDING 1: l15 screens[9] hidden tests reject 'min(up, left, diagonal) + cost'", f is not None, "it passes all %d tests" % len(we["tests"]))

DIJK4 = '''
import heapq
def min_path_cost(costs):
    rows, cols = len(costs), len(costs[0])
    dist = {(0, 0): costs[0][0]}
    heap = [(costs[0][0], 0, 0)]
    while heap:
        d, i, j = heapq.heappop(heap)
        if (i, j) == (rows - 1, cols - 1):
            return d
        if d > dist[(i, j)]:
            continue
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < rows and 0 <= b < cols:
                nd = d + costs[a][b]
                if nd < dist.get((a, b), float("inf")):
                    dist[(a, b)] = nd
                    heapq.heappush(heap, (nd, a, b))
'''
SNAKE = [[1, 1, 1], [9, 9, 1], [1, 1, 1], [1, 9, 9], [1, 1, 1]]
ns = {}
exec(DIJK4, ns)
chk("a four-direction shortest path is a different problem: snake grid gives 11, right/down optimum is 15",
    ns["min_path_cost"](SNAKE) == 11 and min(cost(p, SNAKE) for p in routes(open_(5, 3))) == 15 == min_cost_dag(SNAKE))
f, got = run_tests(DIJK4, wm)
chk("FINDING 2: l16 screens[7] hidden tests reject Dijkstra with moves in all four directions", f is not None, "it passes all %d tests" % len(wm["tests"]))

GUARD = '''
def knapsack_items(weights, values, cap):
    n = len(weights)
    best = [[0] * (cap + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        wt, val = weights[i - 1], values[i - 1]
        if wt > cap:
            continue
        for w in range(cap + 1):
            best[i][w] = best[i - 1][w]
            if wt <= w:
                best[i][w] = max(best[i][w], best[i - 1][w - wt] + val)
    chosen, w = [], cap
    for i in range(n, 0, -1):
        if weights[i - 1] <= w and best[i][w] != best[i - 1][w]:
            chosen.append(i - 1)
            w -= weights[i - 1]
    return sorted(chosen)
'''
ns = {}
exec(GUARD, ns)
chk("a zero row for a too-heavy item, patched by a weight guard in the walk, is wrong: ([1, 9, 1], [7, 100, 5], 1) gives [2], true [0]",
    ns["knapsack_items"]([1, 9, 1], [7, 100, 5], 1) == [2] and rule_pack([1, 9, 1], [7, 100, 5], 1) == [0])
f, got = run_tests(GUARD, w9)
chk("FINDING 3: l14 screens[9] hidden tests reject the zero-row table with a guarded walk", f is not None, "it passes all %d tests" % len(w9["tests"]))

FRAC = '''
from fractions import Fraction
def dice_value(n):
    value = Fraction(7, 2)
    for _ in range(n - 1):
        value = sum(max(Fraction(face), value) for face in range(1, 7)) / 6
    return value

def dice_threshold(n):
    if n == 1:
        return 1
    later = dice_value(n - 1)
    return next(face for face in range(1, 7) if face >= later)
'''
ns = {}
exec(FRAC, ns)
bad = [i for i, t in enumerate(wd["tests"], 1) if not eval(t["call"], dict(ns)) == ex(t)]
chk("FINDING 4: l17 screens[7] hidden tests accept an exact Fraction solution (14/3 kept as a fraction)", not bad,
    "fails tests %s: round(Fraction(14, 3), 6) is Fraction(2333333, 500000), which is not == the float 4.666667" % bad)
chk("  the fix works: round(float(Fraction(14, 3)), 6) == 4.666667", round(float(F(14, 3)), 6) == 4.666667)

calls = [0]


def lcs_plain(a, b):
    def go(i, j):
        calls[0] += 1
        if calls[0] > 3_000_000:
            raise OverflowError
        if i == 0 or j == 0:
            return 0
        if a[i - 1] == b[j - 1]:
            return go(i - 1, j - 1) + 1
        return max(go(i - 1, j), go(i, j - 1))
    return go(len(a), len(b))


worst = 0
for t in wl["tests"]:
    calls[0] = 0
    try:
        lcs_plain(*eval(t["call"][len("lcs_length"):]))
        worst = max(worst, calls[0])
    except OverflowError:
        worst = float("inf")
chk("FINDING 9: some l15 screens[6] hidden test needs more than 3 million calls of the plain recursion (so the table is enforced)",
    worst == float("inf"), "largest call count over the 10 tests is %s: the two 200-letter strings match on alternate diagonals" % worst)
calls[0] = 0
try:
    lcs_plain("ACGT" * 50, "TGCA" * 50)
    slow = False
except OverflowError:
    slow = True
chk("  a replacement large test: ('ACGT' * 50, 'TGCA' * 50) defeats plain recursion; its LCS is %d" % lcs_memo("ACGT" * 50, "TGCA" * 50), slow)

print("\n%d checks, %d failing" % (N[0], len(FAILS)))
for f in FAILS:
    print("  FAIL " + f)
sys.exit(1 if FAILS else 0)
