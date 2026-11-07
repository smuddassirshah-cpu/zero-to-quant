"""Recompute every number in brainteasers homework-2 item hw9-circle-hats.

Runs the item's own solution, starter and planted wrong plans through its
postlude and every hidden test and example, as the code widget does (expect
read as Python, compare equal). Then checks the claims in the prose, feedback
and explain by a second route that does not use the postlude.
Exits 0 only if every check passes.
"""
import json, os, sys
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
HW = os.path.join(HERE, "..", "..", "app", "content", "courses", "brainteasers", "homework-2.json")
item = next(i for i in json.load(open(HW))["items"] if i["id"] == "hw9-circle-hats")
w = item["widget"]
fails = []


def check(name, got, want):
    ok = got == want
    print(("ok  " if ok else "FAIL"), name, got, "" if ok else f"(want {want})")
    if not ok:
        fails.append(name)


def run(code, cases):
    """Results of each case: True if it passes."""
    out = []
    for case in cases:
        ns = {}
        try:
            exec(code, ns)
            exec(w["postlude"], ns)
            out.append(eval(case["call"], ns) == eval(case["expect"]))
        except Exception:
            out.append(False)
    return out


tests, examples = w["tests"], w["examples"]
check("tests >= 3", len(tests) >= 3, True)
check("more tests than examples", len(tests) > len(examples), True)
check("test expectations are floor(n/2)",
      all(int(t["expect"]) == int(t["call"][11:-1]) // 2 for t in tests + examples), True)
check("solution passes every test", run(w["solution"], tests), [True] * len(tests))
check("solution passes every example", run(w["solution"], examples), [True] * len(examples))
check("starter fails at least one test", all(run(w["starter"], tests)), False)

# Planted wrong plans, each one a plausible slip
P = "def guess(i, n, left, right):\n    "
planted = {
    "whole-circle parity, as in the line puzzles": P + "return (i - left - right) % 2\n",
    "copy the left neighbour": P + "return left\n",
    "bet the opposite of the left neighbour": P + "return 1 - left\n",
    "both partners bet the hats match": P + "return right if i % 2 == 0 else left\n",
    "odd person bets on the wrong neighbour": P + "return right if i % 2 == 0 else 1 - right\n",
    "say a colour only when both neighbours agree": P + "return left if left == right else 0\n",
    "odd person picks a neighbour by i % 3": P + "return 1 - right if i % 2 == 0 else left if i % 3 else right\n",
}
caught = 0
for name, code in planted.items():
    res = run(code, tests)
    ok = not all(res)
    caught += ok
    check(f"planted '{name}' fails a test (first fail: test {res.index(False) + 1 if not all(res) else '-'})", ok, True)
check("planted plans caught", caught, len(planted))


# Second route: count right guesses directly, colouring by colouring, no shuffle
def sol(i, n, left, right):
    if i % 2 == 0:
        return right if i + 1 < n else 0
    return 1 - left


for n in range(2, 13):
    counts = []
    for h in product((0, 1), repeat=n):
        counts.append(sum(sol(i, n, h[(i - 1) % n], h[(i + 1) % n]) == h[i] for i in range(n)))
    check(f"n = {n}: fewest right is floor(n/2)", min(counts), n // 2)
    # each pair has exactly one right guess, so even n gives exactly n/2 every time
    if n % 2 == 0:
        check(f"n = {n}: every colouring gives exactly n/2", set(counts), {n // 2})
    # each guess is right on exactly half the colourings: average n/2
    check(f"n = {n}: total right over all colourings is n 2^(n-1)", sum(counts), n * 2 ** (n - 1))

# Optimality by brute force on small circles: every plan, every person
# A person's plan is a function of (left, right): 16 choices. For n = 2, 3 try all.
for n in (2, 3):
    best = 0
    for plan in product(range(16), repeat=n):
        f = lambda i, l, r: (plan[i] >> (2 * l + r)) & 1
        worst = min(sum(f(i, h[(i - 1) % n], h[(i + 1) % n]) == h[i] for i in range(n))
                    for h in product((0, 1), repeat=n))
        best = max(best, worst)
    check(f"n = {n}: best guarantee over every plan", best, n // 2)
# n = 4: 16^4 = 65,536 plans
n = 4
cols = list(product((0, 1), repeat=n))
best = 0
for plan in product(range(16), repeat=n):
    worst = n
    for h in cols:
        s = 0
        for i in range(n):
            s += ((plan[i] >> (2 * h[(i - 1) % n] + h[(i + 1) % n])) & 1) == h[i]
        if s < worst:
            worst = s
            if worst <= best:
                break
    best = max(best, worst)
check("n = 4: best guarantee over every plan", best, 2)

# Number of colourings the largest test plays
check("colourings at n = 12", len(list(product((0, 1), repeat=12))), 2 ** 12)

if fails:
    print(len(fails), "checks failed")
    sys.exit(1)
print("all checks passed")
