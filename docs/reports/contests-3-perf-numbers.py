"""Recompute every claim and number in contests homework-3 item hw3-due-order.

Problem L: one machine, every job ready at 0, job j takes p_j and is due d_j,
lateness max(0, C_j - d_j); minimise the worst lateness. The greedy runs the
jobs back to back in order of due time.

Size checked: every multiset of 1 to 5 jobs with times 1 to 3 and due times
0 to 8 (201,375 instances). Greedy, under every tie order, is compared with
two independent optima: route A tries every order, route B is a DP over
subsets (bitmasks). Idle time is checked never to help (n <= 3, every gap 0 to
3 before each job). The exchange step of the model is replayed on every best
order for n <= 4. The counterexamples are checked by orders (each job as
early as it may start) and by a grid of integer start times. Exits 0 only if
every check passes.
"""
import itertools
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ITEM_FILE = os.path.join(HERE, "..", "..", "app", "content", "courses", "contests", "homework-3.json")

fails = []
count = [0]


def check(name, ok, detail=""):
    count[0] += 1
    if not ok:
        fails.append(name)
        print("FAIL", name, detail)


def late(c, d):
    return max(0, c - d)


def worst_back_to_back(order, jobs):
    """jobs[j] = (p, d); run order back to back from 0."""
    t = 0
    w = 0
    for j in order:
        p, d = jobs[j]
        t += p
        w = max(w, late(t, d))
    return w


def finishes(order, jobs):
    t = 0
    out = {}
    for j in order:
        t += jobs[j][0]
        out[j] = t
    return out


def dp_opt(jobs):
    """Route B: f[S] = least worst lateness for running set S first; the last job of S ends at sum p(S)."""
    n = len(jobs)
    tot = [0] * (1 << n)
    for s in range(1, 1 << n):
        low = (s & -s).bit_length() - 1
        tot[s] = tot[s ^ (1 << low)] + jobs[low][0]
    f = [0] + [None] * ((1 << n) - 1)
    for s in range(1, 1 << n):
        best = None
        for j in range(n):
            if s >> j & 1:
                v = max(f[s ^ (1 << j)], late(tot[s], jobs[j][1]))
                if best is None or v < best:
                    best = v
        f[s] = best
    return f[(1 << n) - 1]


# 1. Greedy optimal on every small instance, by two routes
JOB_TYPES = [(p, d) for p in range(1, 4) for d in range(0, 9)]
instances = 0
greedy_orders_checked = 0
for n in range(1, 6):
    for jobs in itertools.combinations_with_replacement(JOB_TYPES, n):
        instances += 1
        perms = list(itertools.permutations(range(n)))
        vals = {o: worst_back_to_back(o, jobs) for o in perms}
        opt_a = min(vals.values())
        opt_b = dp_opt(jobs)
        check("route A = route B", opt_a == opt_b, (jobs, opt_a, opt_b))
        for o in perms:
            if all(jobs[o[i]][1] <= jobs[o[i + 1]][1] for i in range(n - 1)):
                greedy_orders_checked += 1
                check("greedy (any tie order) optimal", vals[o] == opt_a, (jobs, o, vals[o], opt_a))
check("instance count", instances == sum(
    len(list(itertools.combinations_with_replacement(JOB_TYPES, n))) for n in range(1, 6)))
check("instance count by formula", instances == sum(
    __import__("math").comb(27 + n - 1, n) for n in range(1, 6)), instances)
print("instances:", instances, "greedy orders checked:", greedy_orders_checked)


# 2. Idle never helps when every job is ready at 0 (closing the gaps)
def worst_with_gaps(order, gaps, jobs):
    t = 0
    w = 0
    for j, g in zip(order, gaps):
        t += g + jobs[j][0]
        w = max(w, late(t, jobs[j][1]))
    return w


for n in range(1, 4):
    for jobs in itertools.combinations_with_replacement(JOB_TYPES, n):
        no_gap = min(worst_back_to_back(o, jobs) for o in itertools.permutations(range(n)))
        with_gap = min(worst_with_gaps(o, g, jobs)
                       for o in itertools.permutations(range(n))
                       for g in itertools.product(range(4), repeat=n))
        check("idle never helps", with_gap == no_gap, jobs)
        # sliding a gapped schedule closed makes no job later
        for o in itertools.permutations(range(n)):
            for g in itertools.product(range(4), repeat=n):
                check("closing gaps makes no job later",
                      worst_back_to_back(o, jobs) <= worst_with_gaps(o, g, jobs))


# 3. The exchange step, replayed on every best order (n <= 4)
max_swaps = {n: 0 for n in range(1, 5)}
swaps_replayed = 0
for n in range(1, 5):
    for jobs in itertools.combinations_with_replacement(JOB_TYPES, n):
        G = tuple(sorted(range(n), key=lambda j: (jobs[j][1], j)))
        perms = list(itertools.permutations(range(n)))
        opt = min(worst_back_to_back(o, jobs) for o in perms)
        for O in perms:
            if worst_back_to_back(O, jobs) != opt:
                continue
            cur = list(O)
            swaps = 0
            while tuple(cur) != G:
                k = next(i for i in range(n) if cur[i] != G[i])
                g = G[k]
                m = cur.index(g)
                check("g sits later than k", m > k)
                check("prefix before k is g_1..g_{k-1}", cur[:k] == list(G[:k]))
                Lo = worst_back_to_back(cur, jobs)
                Co = finishes(cur, jobs)
                T = Co[g]
                check("T is the end of position m", T == sum(jobs[j][0] for j in cur[:m + 1]))
                new = cur[:]
                new[k], new[m] = new[m], new[k]
                check("swap keeps every job once", sorted(new) == list(range(n)))
                Cn = finishes(new, jobs)
                for i in range(n):
                    j = new[i]
                    if i < k or i > m:
                        check("outside the block unchanged", Cn[j] == Co[j])
                    else:
                        check("block job ends by T", Cn[j] <= T)
                        check("block job due no earlier than g", jobs[j][1] >= jobs[g][1])
                        check("block job lateness <= g's in O",
                              late(Cn[j], jobs[j][1]) <= late(T, jobs[g][1]) <= Lo)
                check("block still ends at T", Cn[new[m]] == T)
                Ln = worst_back_to_back(new, jobs)
                check("no worse", Ln <= Lo, (jobs, cur, new))
                check("still best", Ln == opt)
                agree_old = next((i for i in range(n) if cur[i] != G[i]), n)
                agree_new = next((i for i in range(n) if new[i] != G[i]), n)
                check("agreement grows by at least one", agree_new >= agree_old + 1)
                cur = new
                swaps += 1
                swaps_replayed += 1
            max_swaps[n] = max(max_swaps[n], swaps)
for n, s in max_swaps.items():
    check(f"at most n - 1 swaps, n = {n}", s <= n - 1, s)
check("n - 1 swaps reached at n = 4", max_swaps[4] == 3, max_swaps)
print("swaps replayed:", swaps_replayed, "max swaps by n:", max_swaps)


# 4. Ready times: the due-order greedy fails
def run_ready(order, jobs):
    """jobs[j] = (r, p, d); each job starts once ready and the machine is free. Returns worst, timeline."""
    t = 0
    w = 0
    line = []
    for j in order:
        r, p, d = jobs[j]
        s = max(t, r)
        t = s + p
        w = max(w, late(t, d))
        line.append((j, s, t, late(t, d)))
    return w, line


def grid_opt(jobs, horizon=20):
    """Route 2: every integer start time, no overlap, no start before ready."""
    n = len(jobs)
    best = None
    for starts in itertools.product(range(horizon), repeat=n):
        ok = all(starts[j] >= jobs[j][0] for j in range(n))
        iv = sorted((starts[j], starts[j] + jobs[j][1]) for j in range(n))
        ok = ok and all(iv[i][1] <= iv[i + 1][0] for i in range(n - 1))
        if ok:
            w = max(late(starts[j] + jobs[j][1], jobs[j][2]) for j in range(n))
            best = w if best is None else min(best, w)
    return best


A, B = 0, 1
ready = {A: (0, 5, 7), B: (5, 1, 6)}
due_order = sorted(ready, key=lambda j: ready[j][2])
check("due order is B, A", due_order == [B, A])
gw, gline = run_ready(due_order, ready)
check("greedy: B from 5 to 6", gline[0] == (B, 5, 6, 0), gline)
check("greedy: A from 6 to 11, 4 late", gline[1] == (A, 6, 11, 4), gline)
check("greedy worst 4", gw == 4)
aw, aline = run_ready([A, B], ready)
check("A then B: A 0 to 5, B 5 to 6, both on time", aline == [(A, 0, 5, 0), (B, 5, 6, 0)], aline)
check("best by orders is 0", min(run_ready(list(o), ready)[0] for o in itertools.permutations(ready)) == 0)
check("best by time grid is 0", grid_opt(ready) == 0)
check("swap would start B at 0, before ready 5", 0 < ready[B][0])


def never_wait(jobs):
    left = set(jobs)
    t = 0
    w = 0
    line = []
    while left:
        rd = [j for j in left if jobs[j][0] <= t]
        if not rd:
            t = min(jobs[j][0] for j in left)
            continue
        j = min(rd, key=lambda j: (jobs[j][2], j))
        left.remove(j)
        s = t
        t += jobs[j][1]
        w = max(w, late(t, jobs[j][2]))
        line.append((j, s, t, late(t, jobs[j][2])))
    return w, line


ready2 = {A: (0, 4, 10), B: (1, 1, 2)}
nw, nline = never_wait(ready2)
check("never-wait: A 0 to 4, B ends 5, 3 late", nline == [(A, 0, 4, 0), (B, 4, 5, 3)], nline)
check("never-wait worst 3", nw == 3)
ww, wline = run_ready([B, A], ready2)
check("waiting for B: B 1 to 2, A 2 to 6, worst 0", (ww, wline) == (0, [(B, 1, 2, 0), (A, 2, 6, 0)]), wline)
check("best by time grid is 0 (second instance)", grid_opt(ready2) == 0)
# The due-order rule happens to be right on the second instance, so both rules need their own instance.
check("due-order rule on the second instance", run_ready(sorted(ready2, key=lambda j: ready2[j][2]), ready2)[0] == 0)

# 5. Total lateness: the greedy fails, worst lateness it wins
tot = {A: (5, 1), B: (1, 2)}
def lates(order, jobs):
    C = finishes(order, jobs)
    return [late(C[j], jobs[j][1]) for j in order]
check("A, B late 4 and 4", lates([A, B], tot) == [4, 4])
check("B, A late 0 and 5", lates([B, A], tot) == [0, 5])
check("totals 8 and 5", (sum(lates([A, B], tot)), sum(lates([B, A], tot))) == (8, 5))
check("worst 4 against 5", (max(lates([A, B], tot)), max(lates([B, A], tot))) == (4, 5))
check("due order is A, B", sorted(tot, key=lambda j: tot[j][1]) == [A, B])
check("best total 5 by DP-free search", min(sum(lates(list(o), tot)) for o in itertools.permutations(tot)) == 5)

# 6. The item as shipped: rubric and the numbers in the model
data = json.load(open(ITEM_FILE))
item = next(i for i in data["items"] if i["id"] == "hw3-due-order")
w = item["widget"]
rub = w["rubric"]
pts = [r["points"] for r in rub]
req = [bool(r.get("required")) for r in rub]
check("rubric sums to 10", sum(pts) == 10, pts)
check("rubric pattern 1, 3, 2, 2, 2", pts == [1, 3, 2, 2, 2], pts)
check("rows 2 to 5 required, row 1 not", req == [False, True, True, True, True], req)
passing = [s for r in range(len(rub) + 1) for s in itertools.combinations(range(len(rub)), r)
           if sum(pts[i] for i in s) >= 7 and all(i in s for i in range(len(rub)) if req[i])]
check("passing tick sets", [tuple(i + 1 for i in s) for s in passing] == [(2, 3, 4, 5), (1, 2, 3, 4, 5)], passing)
for named, row in [("exchange", 1), ("feasibility", 2), ("repeat", 3), ("assumption", 4)]:
    check(f"no pass skips the {named} row", all(row in s for s in passing))
check("performance derivation", item.get("performance") == "derivation")
model = w["model"]
for s in ["from 6 to 11", "4 minutes late", "from 0 to 5 and B from 5 to 6", "The best is 0 against the greedy's 4",
          "B ends at 5, 3 minutes late", "total 8", "total 5", "The worst is 4 against 5", "$n - 1$ swaps", "$n!$"]:
    check(f"model says: {s}", s in model)
check("explain: 4 minutes late against 0", "4 minutes late against 0" in item["explain"]["text"])

print(f"checks: {count[0]}, failures: {len(fails)}")
sys.exit(1 if fails else 0)
