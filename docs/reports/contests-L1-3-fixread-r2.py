"""Fix-pass read, contests levels 1 to 3 round 2 (commit 15f568f7). Written blind, before the audit file was opened.
Checks: l9 gaps, l6 divisor bound, l4 seed replay, l12 stress-test rate. Exits 0 when the content holds."""
import math
import random
import sys

fails = []


def check(name, ok, detail=""):
    print(("ok   " if ok else "FAIL ") + name + (" | " + detail if detail else ""))
    if not ok:
        fails.append(name)


# l9 screens[1] option odd: gaps of 2 4 1 3 5
p = [2, 4, 1, 3, 5]
gaps = [abs(a - b) for a, b in zip(p, p[1:])]
check("l9 gaps of 2 4 1 3 5 are 2, 3, 2, 2", gaps == [2, 3, 2, 2], str(gaps))
check("l9 pattern is evens then odds for n = 5", p == [x for x in range(1, 6) if x % 2 == 0] + [x for x in range(1, 6) if x % 2])

# l6: every composite n has a divisor d with 2 <= d <= sqrt(n); floor(sqrt(1,000,003)) = 1000
bad = [n for n in range(4, 200001)
       if any(n % d == 0 for d in range(2, math.isqrt(n) + 1)) != any(n % d == 0 for d in range(2, n))]
check("l6 composite n <= 200,000 has a divisor in [2, isqrt(n)], primes have none", not bad, str(bad[:3]))
check("l6 floor(sqrt(1,000,003)) = 1000", math.isqrt(1000003) == 1000 and 1000 ** 2 <= 1000003 < 1001 ** 2)
check("l6 without the lower bound the claim is empty (d = 1 divides a prime)", 7 % 1 == 0 and 1 <= math.sqrt(7))

# l4 quiz[1] option time: seed 4 replays the cases, another seed does not
def gen_pairs(rng):  # the lesson's own generator (l4 code widget prelude)
    n = rng.randint(1, 6)
    xs = [rng.randint(1, 10) for _ in range(n)]
    return xs, rng.randint(2, 20)


def run(seed, k=50):
    rng = random.Random(seed)
    return [gen_pairs(rng) for _ in range(k)]


check("l4 seed 4 gives the same 50 cases twice", run(4) == run(4))
same = sum(run(4) == run(s) for s in range(1000, 3000))
check("l4 none of 2,000 other seeds repeats seed 4's 50 cases", same == 0, f"{same} repeats")


# l12 screens[5] explain: a stress test finds the missing -v within ten random cases almost every time
def good(n, ups):
    d = [0] * (n + 1)
    for l, r, v in ups:
        d[l] += v
        d[r + 1] -= v
    out, run_ = [], 0
    for i in range(n):
        run_ += d[i]
        out.append(run_)
    return out


def buggy(n, ups):  # the trap screen's code
    d = [0] * (n + 1)
    for l, r, v in ups:
        d[l] += v
    out, run_ = [], 0
    for i in range(n):
        run_ += d[i]
        out.append(run_)
    return out


def brute(n, ups):
    out = [0] * n
    for l, r, v in ups:
        for i in range(l, r + 1):
            out[i] += v
    return out


def make_gen(nmax, qmax, vlo, vhi):
    # updates drawn as the l12 code widget's hidden tests draw them: l uniform, r uniform on [l, n - 1], v uniform
    def gen(rng):
        n = rng.randint(1, nmax)
        ups = []
        for _ in range(rng.randint(1, qmax)):
            l = rng.randint(0, n - 1)
            ups.append((l, rng.randint(l, n - 1), rng.randint(vlo, vhi)))
        return n, ups
    return gen


REPS = 20000
rng0 = random.Random(1)
for _ in range(2000):
    n, ups = make_gen(8, 6, -9, 9)(rng0)
    assert good(n, ups) == brute(n, ups)
worst10 = 1.0
for label, g in [("n 1..6, q 1..6, v -9..9 (lesson 4 sizes)", make_gen(6, 6, -9, 9)),
                 ("n 1..8, q 1..5, v -9..9", make_gen(8, 5, -9, 9)),
                 ("n 1..10, q 1..10, v -9..9", make_gen(10, 10, -9, 9)),
                 ("n 1..5, q 1..3, v 1..9 (very small)", make_gen(5, 3, 1, 9)),
                 ("n 1..3, q 1..2, v -9..9 (tiny)", make_gen(3, 2, -9, 9))]:
    first = within10 = 0
    for rep in range(REPS):
        rng = random.Random(rep)
        for t in range(10):
            n, ups = g(rng)
            if buggy(n, ups) != brute(n, ups):
                first += t == 0
                within10 += 1
                break
    p1, p10 = first / REPS, within10 / REPS
    worst10 = min(worst10, p10)
    print(f"     l12 {label}: first case {p1:.3f}, within ten {p10:.4f}")
    if "tiny" not in label and "very small" not in label:
        check(f"l12 within ten >= 0.99 for {label}", p10 >= 0.99, f"{p10:.4f}")
        check(f"l12 first-case rate is well under 'almost every time' for {label}", p1 < 0.9, f"{p1:.3f}")
check("l12 even the tiny generator finds it within ten in over 95% of runs", worst10 >= 0.95, f"{worst10:.4f}")

# l12 same explain, unchanged clause used by the changed sentence: (1, 4, +3) on 8 days leaves days 5 to 7 at 3
check("l12 (1, 4, +3), n = 8: buggy days 5 to 7 are 3", buggy(8, [(1, 4, 3)])[5:] == [3, 3, 3] and good(8, [(1, 4, 3)])[5:] == [0, 0, 0])

print("FAILS:", fails)
sys.exit(1 if fails else 0)
