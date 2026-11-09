"""Numbers in momentum-rep homework-1 item h-ivol-plan (performance task, L1).

Every stated number is computed twice by independent routes, and the rubric's
passing tick sets are enumerated. Run from the repository root or anywhere:
    python3 docs/reports/momentum-rep-1-perf-numbers.py
Exits 0 when every check passes.
"""
import itertools
import json
import math
import os
import statistics
from datetime import date
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
HW = os.path.join(HERE, "..", "..", "app", "content", "courses", "momentum-rep", "homework-1.json")
hw = json.load(open(HW, encoding="utf-8"))
item = next(i for i in hw["items"] if i["id"] == "h-ivol-plan")
w = item["widget"]
model, prompt = w["model"], w["prompt"]
fails = []


def check(name, ok):
    print(("ok   " if ok else "FAIL ") + name)
    if not ok:
        fails.append(name)


# 1. Holding months: rankings at the ends of July 1963 .. November 2000,
#    held August 1963 .. December 2000.
# Route A: walk the calendar month by month.
y, m, n_a = 1963, 8, 0
while (y, m) <= (2000, 12):
    n_a += 1
    m += 1
    if m == 13:
        y, m = y + 1, 1
# Route B: arithmetic, 5 months of 1963 plus 37 whole years.
n_b = 5 + 12 * (2000 - 1964 + 1)
# Route C: formation months July 1963 .. November 2000 by month index.
n_c = (2000 * 12 + 11) - (1963 * 12 + 7) + 1
check("449 holding months (calendar walk %d, arithmetic %d, index %d)" % (n_a, n_b, n_c), n_a == n_b == n_c == 449)
check("model states 449", "449 months" in model and "holding months August 1963 to December 2000" in model and "\\sqrt{449}" in model)
check("sample is 37.5 years of formation months", Fraction(n_a + 1, 12) == Fraction(75, 2))

# 2. Standard error of the mean at sd 6.0% a month over 449 months.
se_a = 6.0 / math.sqrt(449)
se_b = math.exp(math.log(6.0) - 0.5 * math.log(449))
# Route C: Newton's method on x^2 = 36/449 in exact fractions.
target = Fraction(36, 449)
x = Fraction(3, 10)
for _ in range(8):
    x = (x + target / x) / 2
se_c = float(x)
check("se = %.5f%% (sqrt %.5f, logs %.5f, newton %.5f)" % (se_a, se_a, se_b, se_c),
      abs(se_a - se_b) < 1e-12 and abs(se_a - se_c) < 1e-12 and round(se_a, 2) == 0.28)
check("model states 0.28%", "= 0.28\\%" in model)

# 3. Tolerance band: -1.06 +- 2 se.
lo_a, hi_a = -1.06 - 2 * se_a, -1.06 + 2 * se_a
lo_b = float(Fraction(-106, 100) - 2 * Fraction(6) / Fraction(math.isqrt(449 * 10**12), 10**6))
hi_b = float(Fraction(-106, 100) + 2 * Fraction(6) / Fraction(math.isqrt(449 * 10**12), 10**6))
check("band %.4f to %.4f (float) vs %.4f to %.4f (fractions)" % (lo_a, hi_a, lo_b, hi_b),
      abs(lo_a - lo_b) < 1e-5 and abs(hi_a - hi_b) < 1e-5)
check("band rounds to -1.63 and -0.49", round(lo_a, 2) == -1.63 and round(hi_a, 2) == -0.49)
check("model states the band", "−1.63% to −0.49%" in model)
check("band holds the target strictly inside", lo_a < -1.06 < hi_a)

# 4. The target and its sign: high minus low, 1.06% less.
check("prompt says 1.06% less", "1.06% a month less than the lowest" in prompt)
check("model and rubric give -1.06%", "−1.06% a month" in model and any("−1.06% a month" in r["text"] for r in w["rubric"]))

# 5. Minimum days: 15 of about 21 trading days. Two routes for the month's days.
days_a = 252 / 12
d = date(1999, 1, 1)
weekdays_1999 = sum(1 for k in range(365) if date.fromordinal(d.toordinal() + k).weekday() < 5)
days_b = (weekdays_1999 - 9) / 12  # about nine US market holidays a year
check("about 21 trading days a month (%.2f, %.2f)" % (days_a, days_b), round(days_a) == 21 and abs(days_b - 21) < 0.6)
check("15 days is most of a month (between half and all)", 21 / 2 < 15 < 21)
check("model states at least 15 days", model.count("15") >= 3)

# 6. Rubric: points, required rows, and every passing tick set.
rub = w["rubric"]
pts = [r["points"] for r in rub]
req = [bool(r.get("required")) for r in rub]
check("rubric has 3 to 5 rows summing to 10 (%s)" % pts, 3 <= len(rub) <= 5 and sum(pts) == 10)
check("not every row required", not all(req))
passes = []
for k in range(len(rub) + 1):
    for s in itertools.combinations(range(len(rub)), k):
        if sum(pts[i] for i in s) >= 7 and all(i in s for i in range(len(rub)) if req[i]):
            passes.append(s)
print("passing tick sets (rows from 1):", [[i + 1 for i in s] for s in passes])
named = {0: "data", 1: "steps", 2: "checks"}
for i, part in named.items():
    check("no pass skips row %d (%s)" % (i + 1, part), all(i in s for s in passes))
# Route B: brute force over bit masks agrees.
passes_b = [mask for mask in range(1 << len(rub))
            if sum(pts[i] for i in range(len(rub)) if mask >> i & 1) >= 7
            and all(mask >> i & 1 for i in range(len(rub)) if req[i])]
check("bit-mask count agrees (%d)" % len(passes_b), len(passes_b) == len(passes) == 2)
check("rows 1 to 3 name data, steps, checks",
      rub[0]["text"].startswith("The data") and rub[1]["text"].startswith("The steps") and rub[2]["text"].startswith("The checks"))

# 7. Shape and homework limits.
check("performance derivation, longform, no starter/steps/hints/parts",
      item.get("performance") == "derivation" and w["kind"] == "longform"
      and not any(k in item or k in w for k in ("starter", "steps", "order", "derive", "hints", "parts")))
check("homework 6 to 12 items (%d)" % len(hw["items"]), 6 <= len(hw["items"]) <= 12)
check("one performance task in the homework", sum(1 for i in hw["items"] if i.get("performance")) == 1)
check("a difficulty 5 present", any(i.get("difficulty") == 5 for i in hw["items"]))
check("a code item present", any(i.get("widget", {}).get("kind") == "code" for i in hw["items"]))
check("no exclamation, em-dash or en-dash", not any(c in json.dumps(item, ensure_ascii=False) for c in "!—–"))

print()
print("failures:", len(fails))
raise SystemExit(1 if fails else 0)
