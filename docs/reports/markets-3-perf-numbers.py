"""Recompute every number in markets/homework-3.json#h-carry-two-rates.

Route A: closed forms in floats.
Route B: an explicit cash-flow ledger per plan, in 50-digit Decimal arithmetic,
run over many share paths, with the bound found by bisection on F.
Then: every number printed in the prompt, model and rubric is matched to a
computed value; the funding alternatives are searched to show the cheapest
plan sets each bound; the rubric's passing tick sets are listed; the
homework-2 split is checked to leave its numbers unchanged.
Standard library only. Exits 1 on any failure.
"""
import json, re, sys, random, itertools
from decimal import Decimal as Dc, getcontext
from pathlib import Path

getcontext().prec = 50
ROOT = Path(__file__).resolve().parents[2]
HW3 = ROOT / "app/content/courses/markets/homework-3.json"
HW2 = ROOT / "app/content/courses/markets/homework-2.json"
fails = 0
checks = 0


def ok(cond, msg):
    global fails, checks
    checks += 1
    if not cond:
        fails += 1
        print("FAIL", msg)


def close(a, b, tol=1e-9):
    return abs(float(a) - float(b)) <= tol


# Inputs, as the prompt states them.
S0, D, t, T = 64.0, 1.20, 0.5, 1.0
rb, rd, fee = 0.07, 0.03, 0.50
r_one, quote = 0.05, 67.80

# ---------- Route A: closed forms ----------
A = {}
A["loan6"] = D * (1 + rb) ** -t
A["loan12"] = S0 - A["loan6"]
A["upper"] = (S0 - D * (1 + rb) ** -t) * (1 + rb) ** T
A["upper_dep"] = S0 * (1 + rb) ** T - D * (1 + rd) ** (T - t)  # dividend deposited at 3%
A["dep6"] = D * (1 + rd) ** -t
A["dep12"] = S0 - A["dep6"]
A["dep12_out"] = A["dep12"] * (1 + rd) ** T
A["lower"] = (S0 - D * (1 + rd) ** -t) * (1 + rd) ** T - fee
A["lower_bor"] = S0 * (1 + rd) ** T - D * (1 + rb) ** (T - t) - fee  # dividend borrowed at 7%
A["one"] = (S0 - D * (1 + r_one) ** -t) * (1 + r_one) ** T
A["one_term"] = D * (1 + r_one) ** (T - t)
A["S0grow5"] = S0 * (1 + r_one)
A["profit"] = quote - A["upper"]

# ---------- Route B: Decimal ledger ----------
def dpow(x, y):
    return (Dc(x).ln() * Dc(y)).exp()


S0d, Dd, td, Td = Dc("64"), Dc("1.20"), Dc("0.5"), Dc("1")
rbd, rdd, feed = Dc("0.07"), Dc("0.03"), Dc("0.50")


def cash_and_carry(F, ST, div_to="loan"):
    """Net cash today, at six months and at delivery. div_to: 'loan' or 'deposit'."""
    today = Dc(0)
    if div_to == "loan":
        l6 = Dd / dpow(1 + rbd, td)
    else:
        l6 = Dc(0)
    l12 = S0d - l6
    today += l6 + l12          # borrowed
    today -= S0d               # buy share
    six = Dd                   # dividend received as holder
    six -= l6 * dpow(1 + rbd, td)  # repay six-month loan
    dep = six                  # whatever is left goes on deposit
    six -= dep
    end = dep * dpow(1 + rdd, Td - td)
    end += F                   # deliver share, receive F
    end -= l12 * (1 + rbd) ** 1  # repay one-year loan
    # share held = share delivered, so ST never enters
    _ = ST
    return today, six, end


def reverse_cc(F, ST, div_from="deposit"):
    today = S0d                # short sale proceeds
    if div_from == "deposit":
        d6 = Dd / dpow(1 + rdd, td)
    else:
        d6 = Dc(0)
    d12 = S0d - d6
    today -= d6 + d12          # deposited
    six = d6 * dpow(1 + rdd, td)
    bor = Dd - six             # borrow any shortfall at 7%
    six += bor
    six -= Dd                  # pay dividend to lender
    end = d12 * (1 + rdd) - F - feed - bor * dpow(1 + rbd, Td - td)
    _ = ST
    return today, six, end


rng = random.Random(7)
paths = [Dc(str(round(rng.uniform(10, 150), 2))) for _ in range(200)]
for ST in paths:
    a, b, c = cash_and_carry(Dc("67"), ST)
    ok(abs(a) < Dc("1e-40") and abs(b) < Dc("1e-40"), "cash and carry not zero before delivery")
    a, b, c = reverse_cc(Dc("65"), ST)
    ok(abs(a) < Dc("1e-40") and abs(b) < Dc("1e-40"), "reverse not zero before delivery")
ok(len({cash_and_carry(Dc("67"), s)[2] for s in paths}) == 1, "cash and carry depends on S_T")
ok(len({reverse_cc(Dc("65"), s)[2] for s in paths}) == 1, "reverse depends on S_T")


def bisect(fun, lo, hi):
    """Root of a monotone function of F."""
    for _ in range(200):
        mid = (lo + hi) / 2
        if (fun(lo) > 0) == (fun(mid) > 0):
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


B = {}
B["upper"] = bisect(lambda F: cash_and_carry(F, S0d)[2], Dc(50), Dc(80))
B["upper_dep"] = bisect(lambda F: cash_and_carry(F, S0d, "deposit")[2], Dc(50), Dc(80))
B["lower"] = bisect(lambda F: reverse_cc(F, S0d)[2], Dc(50), Dc(80))
B["lower_bor"] = bisect(lambda F: reverse_cc(F, S0d, "borrow")[2], Dc(50), Dc(80))
B["loan6"] = Dd / dpow(Dc("1.07"), td)
B["loan12"] = S0d - B["loan6"]
B["dep6"] = Dd / dpow(Dc("1.03"), td)
B["dep12"] = S0d - B["dep6"]
B["dep12_out"] = B["dep12"] * Dc("1.03")
B["one_term"] = Dd * dpow(Dc("1.05"), td)
B["S0grow5"] = S0d * Dc("1.05")
B["one"] = B["S0grow5"] - B["one_term"]
B["profit"] = Dc("67.80") - B["upper"]

for k in A:
    ok(close(A[k], B[k], 1e-9), f"route A and B disagree on {k}: {A[k]} vs {B[k]}")

# One rate, no fee: the two ledgers meet at one price for many r.
for r in ["0.01", "0.03", "0.05", "0.08"]:
    def cc(F, r=Dc(r)):
        l6 = Dd / dpow(1 + r, td)
        return F - (S0d - l6) * (1 + r)
    def rv(F, r=Dc(r)):
        d6 = Dd / dpow(1 + r, td)
        return (S0d - d6) * (1 + r) - F
    up = bisect(cc, Dc(40), Dc(90))
    lo = bisect(rv, Dc(40), Dc(90))
    formula = (S0d - Dd / dpow(1 + Dc(r), td)) * (1 + Dc(r))
    ok(abs(up - lo) < Dc("1e-30") and abs(up - formula) < Dc("1e-30"), f"bounds do not meet at r={r}")

# The cheapest plan sets each bound: search the share of the dividend that repays
# debt (cash and carry) or is set aside today (reverse).
for w in [i / 20 for i in range(21)]:
    up_w = S0 * (1 + rb) - w * D * (1 + rb) ** (T - t) - (1 - w) * D * (1 + rd) ** (T - t)
    ok(up_w >= A["upper"] - 1e-12, f"a mix {w} gives a tighter upper bound")
    lo_w = S0 * (1 + rd) - w * D * (1 + rd) ** (T - t) - (1 - w) * D * (1 + rb) ** (T - t) - fee
    ok(lo_w <= A["lower"] + 1e-12, f"a mix {w} gives a tighter lower bound")
ok(A["lower"] < A["one"] < A["upper"], "frictionless price not inside the band")
ok(A["upper_dep"] > A["upper"] and A["lower_bor"] < A["lower"], "looser bounds on wrong side")
# The claims about quotes in the gaps.
ok(cash_and_carry(Dc("67.25"), S0d)[2] > 0 and cash_and_carry(Dc("67.25"), S0d, "deposit")[2] < 0,
   "67.25 should pay by the cheaper plan only")
ok(reverse_cc(Dc("64.19"), S0d)[2] > 0 and reverse_cc(Dc("64.19"), S0d, "borrow")[2] < 0,
   "64.19 should pay by the cheaper plan only")
ok(cash_and_carry(Dc("67.80"), S0d)[2] > 0 and reverse_cc(Dc("67.80"), S0d)[2] < 0, "67.80 trade")

# ---------- Every number the item prints ----------
values = {
    "64": S0, "1.20": D, "7": 7, "3": 3, "0.50": fee, "67.80": quote, "5": 5,
    "0.5": t, "1": T, "0.07": rb, "0.03": rd, "0": 0, "2": 2, "6": 6,
    "1.1601": A["loan6"], "62.8399": A["loan12"], "67.2387": A["upper"], "67.24": A["upper"],
    "67.2621": A["upper_dep"], "67.26": A["upper_dep"], "1.1824": A["dep6"],
    "62.8176": A["dep12"], "64.7021": A["dep12_out"], "64.2021": A["lower"], "64.20": A["lower"],
    "64.1787": A["lower_bor"], "64.18": A["lower_bor"], "64.19": 64.19, "67.20": A["S0grow5"],
    "1.2296": A["one_term"], "65.9704": A["one"], "65.97": A["one"], "0.5613": A["profit"],
    "0.56": A["profit"], "1.05": 1.05, "1.07": 1.07, "1.03": 1.03, "64.00": S0,
}
item = [i for i in json.loads(HW3.read_text())["items"] if i["id"] == "h-carry-two-rates"][0]
texts = [item["prompt"], item["model"]] + [r["text"] for r in item["rubric"]]
seen = set()
for txt in texts:
    for num in re.findall(r"(?<![\w.])-?\d+(?:\.\d+)?", txt.replace("£", " ")):
        n = num.lstrip("-")
        seen.add(n)
        ok(n in values, f"printed number {n} has no computed value")
        if n in values:
            dp = len(n.split(".")[1]) if "." in n else 0
            ok(abs(round(values[n], dp) - float(n)) < 1e-9 or n in ("7", "3", "5", "1", "0", "2", "6"),
               f"{n} is not {values[n]} at {dp} places")
# Shown arithmetic lines, recomputed from the printed figures.
ok(close(round(1.1601 * 1.07 ** 0.5, 2), 1.20), "1.1601 x 1.07^0.5")
ok(close(round(64 - 1.1601, 4), 62.8399), "64 - 1.1601")
ok(abs(62.8399 * 1.07 - 67.2387) < 6e-5, "62.8399 x 1.07")
ok(close(round(1.1824 * 1.03 ** 0.5, 2), 1.20), "1.1824 x 1.03^0.5")
ok(close(round(64 - 1.1824, 4), 62.8176), "64 - 1.1824")
ok(abs(62.8176 * 1.03 - 64.7021) < 6e-5, "62.8176 x 1.03")
ok(close(round(64.7021 - 0.50, 4), 64.2021), "64.7021 - 0.50")
ok(close(round(67.20 - 1.2296, 4), 65.9704), "67.20 - 1.2296")
ok(close(round(67.80 - 67.2387, 4), 0.5613), "67.80 - 67.2387")

# ---------- Rubric: every passing tick set ----------
rub = item["rubric"]
ok(sum(r["points"] for r in rub) == 10, "rubric does not sum to 10")
ok(3 <= len(rub) <= 5, "rubric rows")
named = {0, 1, 2}  # parts 1, 2 and 3; row 4 is the optional part
passing = []
for k in range(len(rub) + 1):
    for s in itertools.combinations(range(len(rub)), k):
        pts = sum(rub[i]["points"] for i in s)
        if pts >= 7 and all(i in s for i, r in enumerate(rub) if r.get("required")):
            passing.append(s)
print("passing tick sets:", [[i + 1 for i in s] for s in passing])
for s in passing:
    ok(named <= set(s), f"pass {s} skips a named part")
ok(not all(r.get("required") for r in rub), "every row required")
ok("Optional, one more point:" in item["prompt"], "optional part not marked")

# ---------- Homework limits ----------
hw = json.loads(HW3.read_text())
ok(6 <= len(hw["items"]) <= 12, "homework size")
ok(any(i.get("difficulty") == 5 for i in hw["items"]), "no difficulty 5")
ok(sum(1 for i in hw["items"] if i.get("performance")) == 1, "not exactly one performance task")

# ---------- homework-2 split: the display holds the same figures ----------
h2 = [i for i in json.loads(HW2.read_text())["items"] if i["id"] == "h-bond-and-share"][0]
ok("\\begin{aligned} P &=" in h2["model"], "h-bond-and-share not split")
p = 5 / 1.06 + 5 / 1.06 ** 2 + 5 / 1.06 ** 3 + 105 / 1.06 ** 4
terms = [round(5 / 1.06, 4), round(5 / 1.06 ** 2, 4), round(5 / 1.06 ** 3, 4), round(105 / 1.06 ** 4, 4)]
ok(terms == [4.7170, 4.4500, 4.1981, 83.1698] and round(p, 4) == 96.5349, "h-bond-and-share figures")

print(f"{checks} checks, {fails} failures")
print("upper", round(A["upper"], 6), "lower", round(A["lower"], 6), "one rate", round(A["one"], 6),
      "profit", round(A["profit"], 6))
sys.exit(1 if fails else 0)
