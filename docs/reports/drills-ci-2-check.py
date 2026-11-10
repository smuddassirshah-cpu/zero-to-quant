"""Check for drill pack ci, pack 2 (two-pointers, windows): 15 drills.

For every drill it:
- runs the model solution on every example and hidden test and compares with `expect`;
- runs an independent method written here (brute force on small inputs; on large inputs a
  different algorithm: counting, a stable sort, bisect on prefix sums, numpy, a sparse table,
  a binary search on the answer, occurrence lists) and compares with `expect`;
- checks the starter fails at least one test;
- runs every planted solution on all hidden tests in its own CPython process and asserts it
  fails at least one and finishes inside 2.5 s (a planted run must never time out in the browser);
- runs each slow method in SLOW (the obvious method, kept out of `planted`) one test at a time
  and asserts some hidden test takes it past 5 s;
- times the model solution over all tests (must be under 1.5 s in CPython, so Pyodide keeps
  a margin inside its shared 5 s);
- checks the pack mix: 3/5/5/2 by difficulty 2/3/4/5, two stdin drills, pace 900 to 2,700,
  10 to 15 hidden tests, 2 or 3 examples with a note, `pack-2` first in tags, two or more planted.
Exit 0 on success.
Run: <scratchpad>/venv/bin/python docs/reports/drills-ci-2-check.py
"""
import json, os, re, subprocess, sys, time
from bisect import bisect_left, bisect_right, insort
from collections import Counter, defaultdict
from itertools import combinations, accumulate
import heapq

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DRILLS = os.path.join(HERE, "..", "..", "app", "content", "drills")
IDS = ["ci-reference-split", "ci-late-fills-merge", "ci-two-desk-matches", "ci-widest-banner",
       "ci-van-pairs", "ci-three-leg-nets", "ci-frame-triples", "ci-excused-outages",
       "ci-capped-repeats", "ci-rota-swaps", "ci-basket-cover", "ci-ends-to-target",
       "ci-paired-signals", "ci-exact-venue-runs", "ci-hop-score"]
SMALL = 60

# ---------------- independent methods ----------------

def split_by_reference(sizes, ref):
    small = [x for x in sizes if x < ref]
    equal = [x for x in sizes if x == ref]
    big = [x for x in sizes if x > ref]
    sizes[:] = small + equal + big
    return (len(small), len(small) + len(equal))

def merge_late_fills(log, m, late):
    log[:] = sorted(log[:m] + list(late), key=lambda f: f[0])   # stable: log entries first on a tie

def count_matching_pairs(a, b, target):
    cb = Counter(b)
    return sum(cb[target - x] for x in a)

def widest_banner(posts):
    n = len(posts)
    if n <= 400:
        best = (0, 0)
        for i in range(n):
            for j in range(i + 1, n):
                a = min(posts[i], posts[j]) * (j - i)
                if a > 0 and (a, j - i) > best:
                    best = (a, j - i)
        return list(best)
    # tallest first: for each post as the shorter end, the partner is the farthest post at least as tall
    order = sorted(range(n), key=lambda i: -posts[i])
    lo = hi = order[0]
    best = (0, 0)
    for i in order[1:]:
        lo, hi = min(lo, i), max(hi, i)
        w = max(i - lo, hi - i)
        a = posts[i] * w
        if a > 0 and (a, w) > best:
            best = (a, w)
    return list(best)

def ints(text):
    return [int(v) for v in re.findall(r"-?\d+", text)]

def vans_brute(w, cap):
    if not w:
        return 0
    first, rest = w[0], w[1:]
    best = 1 + vans_brute(rest, cap)
    for k in range(len(rest)):
        if first + rest[k] <= cap:
            best = min(best, 1 + vans_brute(rest[:k] + rest[k + 1:], cap))
    return best

def solve_van_pairs(text):
    v = ints(text)
    n, cap, w = v[0], v[1], sorted(v[2:2 + v[0]])
    if n <= 9:
        return str(vans_brute(w, cap))
    # p pairs are possible iff the 2p lightest, paired outside-in, all fit; feasibility falls with p
    def ok(p):
        return all(w[i] + w[2 * p - 1 - i] <= cap for i in range(p))
    lo, hi = 0, n // 2
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if ok(mid):
            lo = mid
        else:
            hi = mid - 1
    return str(n - lo)

def netting_triples(sizes, target):
    if len(sizes) <= SMALL:
        return sorted({tuple(sorted(c)) for c in combinations(sizes, 3) if sum(c) == target})
    cnt = Counter(sizes)
    vals = sorted(cnt)
    out = []
    for ai, a in enumerate(vals):
        for b in vals[ai:]:
            c = target - a - b
            if c < b:
                break
            need = Counter([a, b, c])
            if all(cnt.get(x, 0) >= k for x, k in need.items()):
                out.append((a, b, c))
    return out

def count_frames(rods):
    n = len(rods)
    if n <= SMALL:
        return sum(1 for c in combinations(sorted(rods), 3) if c[0] + c[1] > c[2])
    a = np.sort(np.array(rods, dtype=np.int64))
    total = 0
    for j in range(1, n - 1):
        s = a[:j] + a[j]                     # pairs (i, j), i < j
        total += int((np.searchsorted(a, s, side="left") - (j + 1)).clip(min=0).sum())
    return total

def solve_excused_outages(text):
    tok = text.split()
    n, k = int(tok[0]), int(tok[1])
    days = tok[2] if n else ""
    P = [0] + list(accumulate(1 if c == "D" else 0 for c in days))
    best = 0
    for r in range(n):
        l = bisect_left(P, P[r + 1] - k, 0, r + 1)
        best = max(best, r + 1 - l)
    return str(best)

def longest_capped_run(log, m):
    n = len(log)
    if n <= SMALL:
        best = 0
        for i in range(n):
            for j in range(i, n):
                if max(Counter(log[i:j + 1]).values()) <= m:
                    best = max(best, j - i + 1)
        return best
    pos = defaultdict(list)
    L = best = 0
    for r, x in enumerate(log):
        pos[x].append(r)
        if len(pos[x]) > m:
            L = max(L, pos[x][-(m + 1)] + 1)
        best = max(best, r - L + 1)
    return best

def longest_after_swaps(rota, k):
    n = len(rota)
    if n <= SMALL:
        best = 0
        for i in range(n):
            for j in range(i, n):
                s = rota[i:j + 1]
                if len(s) - max(Counter(s).values()) <= k:
                    best = max(best, len(s))
        return best
    best = 0
    for c in set(rota):
        P = [0] + list(accumulate(0 if ch == c else 1 for ch in rota))
        for r in range(n):
            l = bisect_left(P, P[r + 1] - k, 0, r + 1)
            best = max(best, r + 1 - l)
    return best

def shortest_basket_cover(tape, basket):
    want = Counter(basket)
    n = len(tape)
    if n <= SMALL:
        best = None
        for i in range(n):
            for j in range(i, n):
                c = Counter(tape[i:j + 1])
                if all(c[t] >= k for t, k in want.items()):
                    if best is None or j - i < best[1] - best[0]:
                        best = (i, j)
                    break
        return best
    def first_start(L):           # fixed window of length L: first start that covers, or None
        have = Counter()
        short = sum(want.values())
        for r, t in enumerate(tape):
            if t in want:
                have[t] += 1
                if have[t] <= want[t]:
                    short -= 1
            if r >= L:
                u = tape[r - L]
                if u in want:
                    have[u] -= 1
                    if have[u] < want[u]:
                        short += 1
            if r >= L - 1 and short == 0:
                return r - L + 1
        return None
    if first_start(n) is None:
        return None
    lo, hi = len(basket), n
    while lo < hi:
        mid = (lo + hi) // 2
        if first_start(mid) is not None:
            hi = mid
        else:
            lo = mid + 1
    s = first_start(lo)
    return (s, s + lo - 1)

def fewest_end_lots(lots, x):
    n = len(lots)
    P = [0] + list(accumulate(lots))
    if n <= SMALL:
        best = -1
        for a in range(n + 1):
            for b in range(n - a + 1):
                if P[a] + (P[n] - P[n - b]) == x and (best < 0 or a + b < best):
                    best = a + b
        return best
    suffix_at = {}                  # suffix sum -> fewest lots from the back giving it
    for b in range(n, -1, -1):
        suffix_at[P[n] - P[n - b]] = b
    best = -1
    for a in range(n + 1):
        b = suffix_at.get(x - P[a])
        if b is not None and a + b <= n and (best < 0 or a + b < best):
            best = a + b
    return best

def best_signal_pair(signals, k):
    n = len(signals)
    if n <= SMALL:
        s = [signals[i][1] + signals[j][1] + signals[j][0] - signals[i][0]
             for i in range(n) for j in range(i + 1, n) if signals[j][0] - signals[i][0] <= k]
        return max(s) if s else None
    t = [p[0] for p in signals]
    a = [p[1] - p[0] for p in signals]
    table = [a[:]]                   # sparse table of range maxima
    w = 1
    while 2 * w <= n:
        prev = table[-1]
        table.append([max(prev[i], prev[i + w]) for i in range(n - 2 * w + 1)])
        w *= 2
    def rmq(l, r):                   # max of a[l..r]
        lev = (r - l + 1).bit_length() - 1
        return max(table[lev][l], table[lev][r - (1 << lev) + 1])
    best = None
    for j in range(1, n):
        l = bisect_left(t, t[j] - k, 0, j)
        if l < j:
            sc = rmq(l, j - 1) + signals[j][1] + t[j]
            best = sc if best is None or sc > best else best
    return best

def count_exact_venue_runs(venues, k):
    n = len(venues)
    if n <= SMALL:
        return sum(1 for i in range(n) for j in range(i, n) if len(set(venues[i:j + 1])) == k)
    # from each start, the sorted first positions of each venue at or after it
    nxt = {}
    firsts = []
    total = 0
    for i in range(n - 1, -1, -1):
        v = venues[i]
        if v in nxt:
            firsts.pop(bisect_left(firsts, nxt[v]))
        nxt[v] = i
        insort(firsts, i)
        if len(firsts) >= k:
            end = firsts[k] if len(firsts) > k else n
            total += end - firsts[k - 1]
    return total

def best_hop_total(gains, k):
    n = len(gains)
    if n <= 12:
        best = None
        for mask in range(1 << (n - 2) if n >= 2 else 1):
            stops = [0] + [i + 1 for i in range(n - 2) if mask >> i & 1] + ([n - 1] if n > 1 else [])
            if all(b - a <= k for a, b in zip(stops, stops[1:])):
                s = sum(gains[i] for i in stops)
                best = s if best is None or s > best else best
        return best
    best = [0] * n
    best[0] = gains[0]
    heap = [(-best[0], 0)]
    for i in range(1, n):
        while heap[0][1] < i - k:
            heapq.heappop(heap)
        best[i] = gains[i] - heap[0][0]
        heapq.heappush(heap, (-best[i], i))
    return best[-1]

INDEP = {
    "ci-reference-split": split_by_reference, "ci-late-fills-merge": merge_late_fills,
    "ci-two-desk-matches": count_matching_pairs, "ci-widest-banner": widest_banner,
    "ci-van-pairs": solve_van_pairs, "ci-three-leg-nets": netting_triples,
    "ci-frame-triples": count_frames, "ci-excused-outages": solve_excused_outages,
    "ci-capped-repeats": longest_capped_run, "ci-rota-swaps": longest_after_swaps,
    "ci-basket-cover": shortest_basket_cover, "ci-ends-to-target": fewest_end_lots,
    "ci-paired-signals": best_signal_pair, "ci-exact-venue-runs": count_exact_venue_runs,
    "ci-hop-score": best_hop_total,
}

# ---------------- running ----------------

# The slow methods a candidate writes first (the obvious method, or the right idea at the wrong
# complexity). They are not in `planted`: a planted run that times out on the drill page restarts
# Python, and the playthrough then reads the stale results of that run for the next submits
# (BACKLOG-INBOX, drills ci 2). Here each must run past 5 s on one hidden test in CPython, which is
# faster than Pyodide, so it also fails the browser's limit.
SLOW = {
    'ci-reference-split': [
        'def split_by_reference(sizes, ref):\n    lo = 0\n    for i in range(len(sizes)):\n        if sizes[i] < ref:\n            sizes.insert(lo, sizes.pop(i))\n            lo += 1\n    hi = lo\n    for i in range(lo, len(sizes)):\n        if sizes[i] == ref:\n            sizes.insert(hi, sizes.pop(i))\n            hi += 1\n    return (lo, hi)\n',
    ],
    'ci-two-desk-matches': [
        'def count_matching_pairs(a, b, target):\n    count = 0\n    for x in a:\n        for y in b:\n            if x + y == target:\n                count += 1\n    return count\n',
    ],
    'ci-widest-banner': [
        'def widest_banner(posts):\n    best, width = 0, 0\n    for i in range(len(posts)):\n        for j in range(i + 1, len(posts)):\n            area = min(posts[i], posts[j]) * (j - i)\n            if area > best or (area == best and area > 0 and j - i > width):\n                best, width = area, j - i\n    return [best, width]\n',
    ],
    'ci-three-leg-nets': [
        'from itertools import combinations\n\ndef netting_triples(sizes, target):\n    found = set()\n    for c in combinations(sorted(sizes), 3):\n        if sum(c) == target:\n            found.add(c)\n    return sorted(found)\n',
    ],
    'ci-frame-triples': [
        'def count_frames(rods):\n    a = sorted(rods)\n    n = len(a)\n    count = 0\n    for i in range(n):\n        for j in range(i + 1, n):\n            for k in range(j + 1, n):\n                if a[i] + a[j] > a[k]:\n                    count += 1\n    return count\n',
    ],
    'ci-excused-outages': [
        "def solve_excused_outages(text):\n    tokens = text.split()\n    n, k = int(tokens[0]), int(tokens[1])\n    days = tokens[2] if n else ''\n    best = 0\n    for i in range(n):\n        down = 0\n        for j in range(i, n):\n            down += days[j] == 'D'\n            if down > k:\n                break\n            best = max(best, j - i + 1)\n    return str(best)\n",
    ],
    'ci-capped-repeats': [
        'def longest_capped_run(log, m):\n    best = 0\n    for i in range(len(log)):\n        count = {}\n        for j in range(i, len(log)):\n            count[log[j]] = count.get(log[j], 0) + 1\n            if count[log[j]] > m:\n                break\n            best = max(best, j - i + 1)\n    return best\n',
    ],
    'ci-rota-swaps': [
        'def longest_after_swaps(rota, k):\n    best = 0\n    for i in range(len(rota)):\n        count = {}\n        for j in range(i, len(rota)):\n            count[rota[j]] = count.get(rota[j], 0) + 1\n            if j - i + 1 - max(count.values()) <= k:\n                best = max(best, j - i + 1)\n    return best\n',
    ],
    'ci-basket-cover': [
        'def shortest_basket_cover(tape, basket):\n    want = {}\n    for t in basket:\n        want[t] = want.get(t, 0) + 1\n    best = None\n    for i in range(len(tape)):\n        have = {}\n        got = 0\n        for j in range(i, len(tape)):\n            t = tape[j]\n            if t in want:\n                have[t] = have.get(t, 0) + 1\n                if have[t] <= want[t]:\n                    got += 1\n            if got == len(basket):\n                if best is None or j - i < best[1] - best[0]:\n                    best = (i, j)\n                break\n    return best\n',
    ],
    'ci-ends-to-target': [
        'def fewest_end_lots(lots, x):\n    n = len(lots)\n    best = -1\n    front = 0\n    for a in range(n + 1):\n        if a:\n            front += lots[a - 1]\n        if front > x:\n            break\n        back = 0\n        for b in range(n - a + 1):\n            if front + back == x:\n                if best < 0 or a + b < best:\n                    best = a + b\n                break\n            if b < n - a:\n                back += lots[n - 1 - b]\n    return best\n',
    ],
    'ci-paired-signals': [
        'def best_signal_pair(signals, k):\n    best = None\n    for j, (t, v) in enumerate(signals):\n        i = j - 1\n        while i >= 0 and t - signals[i][0] <= k:\n            ti, vi = signals[i]\n            score = vi + v + t - ti\n            if best is None or score > best:\n                best = score\n            i -= 1\n    return best\n',
    ],
    'ci-exact-venue-runs': [
        'def count_exact_venue_runs(venues, k):\n    total = 0\n    for i in range(len(venues)):\n        seen = set()\n        for j in range(i, len(venues)):\n            seen.add(venues[j])\n            if len(seen) > k:\n                break\n            if len(seen) == k:\n                total += 1\n    return total\n',
    ],
    'ci-hop-score': [
        'def best_hop_total(gains, k):\n    best = [0] * len(gains)\n    best[0] = gains[0]\n    for i in range(1, len(gains)):\n        best[i] = gains[i] + max(best[max(0, i - k):i])\n    return best[-1]\n',
    ],
}

RUNNER = r"""
import json, sys, time
spec = json.load(sys.stdin)
ns = {}
exec(spec["code"], ns)
first = None
t0 = time.time()
for i, c in enumerate(spec["cases"]):
    try:
        ok = eval(c["call"], ns) == eval(c["expect"])
    except Exception as e:
        ok = False
    if not ok and first is None:
        first = i
    if spec.get("stop") and first is not None:
        break
print(json.dumps({"failed": first, "s": round(time.time() - t0, 2)}))
"""

def run_isolated(code, cases, limit=10, stop=False):
    try:
        r = subprocess.run([sys.executable, "-c", RUNNER], input=json.dumps({"code": code, "cases": cases, "stop": stop}),
                           capture_output=True, text=True, timeout=limit)
    except subprocess.TimeoutExpired:
        return {"failed": "timeout", "s": limit}
    return json.loads(r.stdout.strip().splitlines()[-1])

errors = []
def err(m):
    errors.append(m)
    print("ERROR", m)

diffs = Counter()
stdin = 0
for did in IDS:
    d = json.load(open(os.path.join(DRILLS, did + ".json")))
    cases = d["examples"] + d["tests"]
    fn = d["fn"]
    # model
    ns = {}
    exec(d["solution"], ns)
    t0 = time.time()
    for c in cases:
        if eval(c["call"], ns) != eval(c["expect"]):
            err(f"{did}: model fails {c['call'][:60]}")
    dt = time.time() - t0
    if dt > 1.5:
        err(f"{did}: model took {dt:.2f} s")
    # independent
    ins = {fn: INDEP[did]}
    for c in cases:
        if eval(c["call"], ins) != eval(c["expect"]):
            err(f"{did}: independent method disagrees on {c['call'][:60]}")
    # starter
    sres = run_isolated(d["starter"], d["tests"])
    if sres["failed"] is None:
        err(f"{did}: starter passes every test")
    # planted
    pl = d.get("planted", [])
    if len(pl) < 2:
        err(f"{did}: fewer than two planted")
    caught = []
    for k, p in enumerate(pl):
        # every hidden test, no early stop, as the drill page runs them; must finish well inside 5 s
        r = run_isolated(p["code"], d["tests"], limit=2.5)
        if r["failed"] == "timeout":
            err(f"{did}: planted[{k}] runs past 2.5 s in CPython, so it could time out in the browser")
        elif r["failed"] is None:
            err(f"{did}: planted[{k}] passes every hidden test ({p['slip']})")
        caught.append(f"test {r['failed']} in {r['s']} s")
    slow_out = []
    for k, code in enumerate(SLOW.get(did, [])):
        hit = None
        for i, c in enumerate(d["tests"]):
            r = run_isolated(code, [c], limit=5)
            if r["failed"] == "timeout":
                hit = i
                break
        if hit is None:
            err(f"{did}: slow method {k} finishes every hidden test inside 5 s")
        slow_out.append(hit)
    # shape
    diffs[d["difficulty"]] += 1
    stdin += "stdin" in d["tags"]
    if d["tags"][0] != "pack-2": err(f"{did}: tags must start pack-2")
    if not 900 <= d["pace"] <= 2700: err(f"{did}: pace {d['pace']}")
    if not 10 <= len(d["tests"]) <= 15: err(f"{did}: {len(d['tests'])} tests")
    if not 2 <= len(d["examples"]) <= 3 or not all(e.get("note") for e in d["examples"]): err(f"{did}: examples")
    if len(d["notes"]) != 3: err(f"{did}: notes")
    if d["pack"] != "ci" or d["course"] != "coding-int": err(f"{did}: pack or course")
    if any("setup" in c for c in cases): err(f"{did}: a case uses setup")
    print(f"{did}: d{d['difficulty']} {len(d['tests'])} tests ok, model {dt:.2f} s, starter fails at {sres['failed']}, planted fail at {caught}, slow methods time out at {slow_out}")

if dict(diffs) != {2: 3, 3: 5, 4: 5, 5: 2}: err(f"difficulty mix {dict(diffs)}")
if stdin != 2: err(f"{stdin} stdin drills")
print(f"{len(IDS)} drills, {len(errors)} errors")
sys.exit(1 if errors else 0)
