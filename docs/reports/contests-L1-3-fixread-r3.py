#!/usr/bin/env python3
"""Fix-pass read, contests levels 1 to 3, round 3 (diff of commit ce87d1b0).

Run from the repo root with no arguments. Exits 0 when the changed content is correct.
Every number is computed from the item's own givens, not copied from the content.
Lines printed as "note" are the imprecise rows of the read: true figures that show where a sentence over-reaches.
The Pyodide runs of l12 screens[4] and homework-3 items[1] (reversed(), .copy() and other variants through
app/tools/code-runner.mjs) are recorded in docs/reviews/audit-contests-1-3-r3.md; the harness is repeated here in CPython.
"""
import json
import math
import random
import sys

ROOT = "app/content/courses/contests/"
fails = []


def check(name, ok, detail=""):
    print(("ok   " if ok else "FAIL ") + name + (" | " + str(detail) if detail and not ok else ""))
    if not ok:
        fails.append(name)


def note(text):
    print("note " + text)


def load(name):
    with open(ROOT + name, encoding="utf-8") as fh:
        return json.load(fh)


def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


# ---- l3 quiz[2]: the `lines` slip, from each mistake its feedback names
q = load("l3-fast-io.json")["quiz"][2]
text = "2\n\n5 -3"
check("l3 prose gives the text used here", '"2\\n\\n5 -3"' in q["prose"])
check("l3 key 3 = len(text.split())", len(text.split()) == q["widget"]["answer"] == 3)
slips = {w["id"]: w["value"] for w in q["widget"]["wrong"]}
lines_with_text = sum(1 for ln in text.split("\n") if ln.strip())
last_line_numbers = len(text.split("\n")[-1].split())
check("l3 slip lines = lines with text", lines_with_text == slips["lines"], lines_with_text)
check("l3 slip lines = numbers on the last line", last_line_numbers == slips["lines"], last_line_numbers)
check("l3 slip blank = the three numbers plus the blank line", len(text.split()) + 1 == slips["blank"])
note("l3 old wording 'words on the first line only' gives %d, not the slip %d" % (len(text.split("\n")[0].split()), slips["lines"]))

# ---- l2 screens[2]: figures in the changed feedback, and the open point
BUDGET = 10 ** 8
check("l2 2^20 is about 10^6", 2 ** 20 == 1048576)
check("l2 2^20 fits", 2 ** 20 <= BUDGET)
check("l2 counting to 10^18 does not fit", 10 ** 18 > BUDGET)
check("l2 log2(10^18) is about 60 and fits", 59 < math.log2(10 ** 18) < 60)
note("l2 n<=20: n*2^n = %d fits 10^8 and grows faster than 2^n; n^2*2^n = %d does not fit" % (20 * 2 ** 20, 400 * 2 ** 20))
note("l2 10^18: cube root = %d steps and log2^2 = %d both fit and grow faster than log n" % (round(1e18 ** (1 / 3)), round(math.log2(1e18) ** 2)))
note("l2 n<=2*10^5 (given row): n*sqrt(n) = %.2e fits and grows faster than n log n = %.2e" % (2e5 ** 1.5, 2e5 * math.log2(2e5)))
check("l2 n<=500: n^3 fits near, n^3 log n does not", 500 ** 3 == 125000000 and 500 ** 3 * math.log2(500) > 5 * BUDGET)
check("l2 n<=5000: n^2 fits, n^2 log n does not", 5000 ** 2 == 25000000 and 5000 ** 2 * math.log2(5000) > BUDGET)

# ---- l6 screens[9]: which of the three large tests a loop without the sqrt stop cannot finish
check("l6 999983, 1000003 and 999999999989 are prime", is_prime(999983) and is_prime(1000003) and is_prime(999999999989))
tests = [t["call"] for t in load("l6-gcd-and-primes.json")["screens"][9]["widget"]["tests"]]
check("l6 nine tests, the last is the large prime", len(tests) == 9 and tests[-1] == "factorise(999999999989)")
# without the stop the loop runs d up to the largest prime factor
largest = {"999983^2": 999983, "999983*1000003": 1000003, "10^12": 5, "2^40": 2, "prime": 999999999989}
check("l6 only the large prime needs more than 2*10^6 trial divisors", [k for k, v in largest.items() if v > 2 * 10 ** 6] == ["prime"])

# ---- l12 screens[4] and homework-3 items[1]: what the counting list counts
l12 = load("l12-difference-arrays.json")["screens"][4]["widget"]
hw3 = load("homework-3.json")["items"][1]["widget"]
ns = {}
exec(l12["prelude"], ns)
Counted = ns["_Counted"]


def reads(fn):
    Counted.reads = 0
    fn(Counted([(0, 1, 2)] * 500))
    return Counted.reads


def by_index(xs):
    for k in range(len(xs)):
        xs[k]


def by_for(xs):
    for _ in xs:
        pass


check("l12 indexing is counted, one per read", reads(by_index) == 500)
check("l12 a for loop is counted, len per loop", reads(by_for) == 500)
check("l12 reversed() is not counted", reads(lambda xs: [u for u in reversed(xs)]) == 0)
check("l12 .copy() is not counted", reads(lambda xs: [u for u in xs.copy()]) == 0)
note("l12 also uncounted: pop() gives %d, xs + [] gives %d; counted: list(xs) gives %d, xs[::-1] gives %d"
     % (reads(lambda xs: [xs.pop() for _ in range(500)]), reads(lambda xs: xs + []), reads(lambda xs: list(xs)), reads(lambda xs: xs[::-1])))
t7 = l12["tests"][6]["call"]
check("l12 test 7 passes from 1 to 2,500 reads", t7 == "0 < update_reads(1000, ups) <= 2500")
env = ns
exec(l12["solution"], env)
exec(l12["tests"][6]["setup"], env)
check("l12 solution reads the 500 updates once", env["update_reads"](1000, env["ups"]) == 500)
note("l12 six reads per update is 3,000: over 2,500 but not 'far more'; scanning every update per day is %d" % (1000 * 500))

ns3 = {}
exec(hw3["prelude"], ns3)
exec(hw3["solution"], ns3)
check("hw3 test 7 passes from 1 to 10,000 reads", hw3["tests"][6]["call"] == "0 < reads_for(spans, list(range(1000))) <= 10000")
r_sol = ns3["reads_for"](ns3["spans"], list(range(1000)))
check("hw3 solution reads within 1 to 10,000", 0 < r_sol <= 10000, r_sol)


def spans_copy(closes):
    return ns3["spans"](closes.copy())


def spans_rev(closes):
    n = len(closes)
    out, stack, i = [0] * n, [], n - 1
    for c in reversed(closes):
        while stack and stack[-1][0] < c:
            j = stack.pop()[1]
            out[j] = j - i
        stack.append((c, i))
        i -= 1
    for _, j in stack:
        out[j] = j + 1
    return out


check("hw3 .copy() first gives 0 reads", ns3["reads_for"](spans_copy, list(range(1000))) == 0)
check("hw3 reversed() gives 0 reads", ns3["reads_for"](spans_rev, list(range(1000))) == 0)
rnd = random.Random(5)
cl = [rnd.randint(1, 50) for _ in range(300)]
check("hw3 the reversed() and .copy() variants are correct solutions", spans_rev(cl) == ns3["spans"](cl) == spans_copy(cl))

print()
print("FAILED: " + ", ".join(fails) if fails else "all checks pass")
sys.exit(1 if fails else 0)
