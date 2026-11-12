#!/usr/bin/env python3
"""Round 2 concept audit, py-found L1 to L3: executed code-behaviour claims.

Run: python3 docs/reports/py-found-L1-3-r2-concepts.py
Exits 0 when every claim the content makes holds. A check that fails because
the content is wrong stays failing: the last section reads the six strings of
audit findings 1 to 6 and fails while each still holds its flawed wording, so
the script exits 1 until the fix pass lands (447 behaviour checks pass today).

Written on CPython 3.13; the app runs Pyodide 0.27.7 (CPython 3.12). Where the
two could differ (error-message wording) the check matches the stable prefix
and says so.
"""
import csv
import math
import os
import random
import statistics
import subprocess
import sys
import tempfile
import textwrap
from collections import Counter
from datetime import datetime
from decimal import Decimal
from fractions import Fraction

FAILS = []
N = 0


def check(label, cond):
    global N
    N += 1
    if not cond:
        FAILS.append(label)
        print("FAIL", label)


def raises(exc, fn, *a, **k):
    try:
        fn(*a, **k)
    except exc as e:
        return str(e) or True
    except Exception:
        return False
    return False


def run_src(src, files=None, name="main.py"):
    """Run a script in a fresh folder; return (stdout, last stderr line)."""
    with tempfile.TemporaryDirectory() as d:
        for fn, body in (files or {}).items():
            with open(os.path.join(d, fn), "w") as fh:
                fh.write(textwrap.dedent(body))
        with open(os.path.join(d, name), "w") as fh:
            fh.write(textwrap.dedent(src))
        p = subprocess.run([sys.executable, name], cwd=d, capture_output=True, text=True)
        err = p.stderr.strip().splitlines()
        return p.stdout, (err[-1] if err else "")


# ---------------------------------------------------------------- l1 floats
check("l1 0.1+0.2 != 0.3", (0.1 + 0.2 == 0.3) is False)
check("l1 repr sum", repr(0.1 + 0.2) == "0.30000000000000004")
check("l1 0.3 to 17 dp", f"{0.3:.17f}" == "0.29999999999999999")
check("l1 gap 5.6e-17", abs((0.1 + 0.2) - 0.3) == 2 ** -54 and round(2 ** -54 * 1e18) == 56)
check("l1 stored 0.1", f"{Decimal(0.1):.20f}" == "0.10000000000000000555")
check("l1 stored 0.2", f"{Decimal(0.2):.20f}" == "0.20000000000000001110")
check("l1 stored 0.3", f"{Decimal(0.3):.20f}" == "0.29999999999999998890")
check("l1 0.1 and 0.2 high, 0.3 low", Fraction(0.1) > Fraction(1, 10) and Fraction(0.2) > Fraction(2, 10) and Fraction(0.3) < Fraction(3, 10))
# binary expansion of 1/10 starts 0.000110011
bits, x = "", Fraction(1, 10)
for _ in range(9):
    x *= 2
    bits += "1" if x >= 1 else "0"
    x -= int(x)
check("l1 0.1 binary 0.000110011", bits == "000110011")
check("l1 53 bits", sys.float_info.mant_dig == 53)
check("l1 17 digits identify a double", sys.float_info.dig == 15 and len(repr(0.1 + 0.2).replace("0.", "")) == 17)
check("l1 s3 exact checks", (0.5 + 0.25 == 0.75) and (0.25 * 4 == 1.0) and (1.5 + 2.5 == 4.0))
check("l1 s3 tenth checks False", not (0.1 * 3 == 0.3) and not (0.7 + 0.1 == 0.8))
check("l1 0.1*3", repr(0.1 * 3) == "0.30000000000000004")
check("l1 0.7+0.1", repr(0.7 + 0.1) == "0.7999999999999999")
check("l1 isclose pair", math.isclose(0.1 + 0.2, 0.3) and not math.isclose(0.1 + 0.2 - 0.3, 0.0))
check("l1 isclose allowance 3e-10", abs(1e-9 * max(0.1 + 0.2, 0.3) - 3e-10) < 1e-16)
check("l1 isclose allowance 6e-26", 5.5e-26 < 1e-9 * abs(0.1 + 0.2 - 0.3) < 5.6e-26)
check("l1 isclose abs_tol", math.isclose(0.1 + 0.2 - 0.3, 0.0, abs_tol=1e-9))
check("l1 isclose(x,0) acts like ==", not math.isclose(1e-300, 0.0) and math.isclose(0.0, 0.0))
check("l1 same_price no abs slip", (10.00 - 10.01 < 0.005) is True and (abs(10.00 - 10.01) < 0.005) is False)
check("l1 same_price row 1", abs(10.00 - 10.003) < 0.005)
t, run = 0.0, []
for _ in range(10):
    t += 0.1
    run.append(repr(t))
check("l1 ten deposits", run[-1] == "0.9999999999999999" and t != 1.0)
check("l1 running totals", run == ["0.1", "0.2", "0.30000000000000004", "0.4", "0.5", "0.6", "0.7", "0.7999999999999999", "0.8999999999999999", "0.9999999999999999"])
check("l1 0.29*100", repr(0.29 * 100) == "28.999999999999996" and int(0.29 * 100) == 28 and round(0.29 * 100) == 29)
check("l1 19.99*100", repr(19.99 * 100) == "1998.9999999999998")
check("l1 int slip 1999", int(19.99 * 100) + int(0.01 * 100) == 1999)
check("l1 unrounded float 1999.9999999999998", repr(19.99 * 100 + 0.01 * 100) == "1999.9999999999998")
check("l1 round returns int", type(round(4.20 * 100)) is int)
check("l1 round(-0.4)==0", round(-0.4) == 0)
check("l1 550/1.10", repr(550.00 / 1.10) == "499.99999999999994" and int(550.00 / 1.10) == 499)
check("l1 7//2", 7 // 2 == 3)
check("l1 10000/300", repr(10000 / 300) == "33.333333333333336")
check("l1 pence route", round(550.00 * 100) // round(1.10 * 100) == 500 and round(350.00 * 100) // round(0.07 * 100) == 5000)
check("l1 q round(2.675,2)", round(2.675, 2) == 2.67 and round(2.675) == 3)
check("l1 q 2.675 stored", str(Decimal(2.675)) == "2.67499999999999982236431605997495353221893310546875")
check("l1 q 6/3", repr(6 / 3) == "2.0")
check("l1 q 0.57*100", repr(0.57 * 100) == "56.99999999999999" and int(0.57 * 100) == 56 and round(0.57 * 100) == 57)
check("l1 q 0.2+0.4", repr(0.2 + 0.4) == "0.6000000000000001" and 0.5 + 0.25 == 0.75)
check("l1 q some tenth sums exact", 0.1 + 0.3 == 0.4)

# ---------------------------------------------------------------- l2 slicing
c6 = [101.20, 102.50, 99.80, 100.40, 103.10, 104.00]
check("l2 [1:4]", c6[1:4] == [102.5, 99.8, 100.4])
check("l2 [-2] is [4]", c6[-2] is c6[4])
check("l2 [-3:]", repr(c6[-3:]) == "[100.4, 103.1, 104.0]" and c6[-3:-1] == [100.4, 103.1])
check("l2 [1::2]", c6[1::2] == [c6[1], c6[3], c6[5]] and c6[1:2] == [c6[1]])
check("l2 -0 slice", c6[-0:] == c6 and c6[len(c6) - 0:] == [])
ten = c6 + [102.70, 101.90, 103.60, 105.20]
check("l2 fridays", ten[4::5] == [103.1, 105.2] and ten[::5] == [101.2, 104.0] and [100.0, 101.0, 102.0][4::5] == [])
a = [1, 2, 3]
b = a
a.append(4)
check("l2 alias", len(b) == 4)
check("l2 slice always new list", a[:] is not a and a[:] == a)
check("l2 count j-i", len(list(range(10))[2:7]) == 5)
check("l2 sma", math.isclose(sum(ten[-5:]) / 5, 103.48) and math.isclose(sum(ten[-5:]), 517.40) and math.isclose(sum(ten[:5]) / 5, 101.40) and math.isclose(sum(ten) / 10, 102.44))
check("l2 q reversed", [101.20, 102.50, 99.80][::-1] == [99.8, 102.5, 101.2] and [101.20, 102.50, 99.80][-1:] == [99.8])
check("l2 q slice past end", [1, 2, 3, 4][2:10] == [3, 4] and raises(IndexError, lambda: [1, 2, 3, 4][10]))
check("l2 q 1:20:3", list(range(20))[1:20:3] == [1, 4, 7, 10, 13, 16, 19])

# ---------------------------------------------------------------- l3 tuples
bid, ask = 100.50, 99.50
bid, ask = ask, bid
check("l3 swap", (bid, ask) == (99.5, 100.5))
trade = ("VOD", 72.50, 100)


def _two():
    ticker, price = trade


check("l3 too many values", str(raises(ValueError, _two)).startswith("too many values to unpack"))
tk, *rest = trade
check("l3 star", rest == [72.5, 100] and type(rest) is list)


def _assign():
    trade[1] = 72.55


check("l3 tuple assign", raises(TypeError, _assign) == "'tuple' object does not support item assignment")
check("l3 commas make the tuple", type((5)) is int and type((5,)) is tuple and type(eval("1, 2")) is tuple)
check("l3 enumerate", [i for i, px in enumerate([101.20, 99.80, 100.40, 98.90]) if px < 100] == [1, 3])
check("l3 zip stops", list(zip(["Mon", "Tue", "Wed"], [101.20, 99.80])) == [("Mon", 101.2), ("Tue", 99.8)])
check("l3 zip strict", bool(raises(ValueError, lambda: list(zip([1, 2, 3], [1, 2], strict=True)))))
cl = [100.00, 105.00, 99.75]
rets = [(c - p) / p for p, c in zip(cl, cl[1:])]
check("l3 returns", math.isclose(rets[0], 0.05) and math.isclose(rets[1], -0.05) and round(5 / 105, 4) == 0.0476 and math.isclose((245 - 250) / 250, -0.02))
parts = "VOD,72.50,100\n".split(",")
check("l3 split strings", parts == ["VOD", "72.50", "100\n"])
check("l3 str*str TypeError", bool(raises(TypeError, lambda: parts[1] * parts[2])))
check("l3 convert", float(parts[1]) * int(parts[2]) == 7250.0 and parts[1] + parts[2] == "72.50100\n")
check("l3 join needs str", bool(raises(TypeError, lambda: ",".join(["VOD", 72.5]))) and ",".join(["VOD", f"{6.45:.2f}", str(1000)]) == "VOD,6.45,1000" and f"{72.5:.2f}" == "72.50")
check("l3 split/join inverse", ",".join("a,b,,c".split(",")) == "a,b,,c")
rows = [("VOD", 72.5), ("BP", 4.8)]
check("l3 enumerate rows", [p for t, p in enumerate(rows)][0] == ("VOD", 72.5))
t1, p1 = rows
check("l3 unpack list itself", t1 == ("VOD", 72.5))


def _three():
    for ticker, price, qty in rows:
        pass


check("l3 three names ValueError", bool(raises(ValueError, _three)))
check("l3 float/int ignore spaces", float(" 4.85 ") == 4.85 and int(" 1000") == 1000 and int("100\n") == 100)
check("l3 q in", ("OD" in "VOD") and not ("OD" in ["VOD", "BP"]))
check("l3 q join", ", ".join(["VOD", "BP", "AZN"]) == "VOD, BP, AZN")
check("l3 q enumerate start", list(enumerate(["Mon", "Tue"], start=1))[-1] == (2, "Tue"))
check("l3 q strip split", "  72.50\n".strip().split(".") == ["72", "50"])

# ---------------------------------------------------------------- l4
r3 = [0.012, -0.034, 0.005]
check("l4 pct", repr([round(r * 100, 1) for r in r3]) == "[1.2, -3.4, 0.5]")
r10 = [0.012, -0.034, 0.005, -0.008, 0.021, 0.0, -0.015, 0.009, -0.002, 0.017]
check("l4 losses idx", [i for i, r in enumerate(r10) if r < 0] == [1, 3, 6, 8])
tk3 = ["VOD", "bp", "AZN"]
check("l4 sorted", sorted(tk3) == ["AZN", "VOD", "bp"] and sorted(tk3, key=str.lower) == ["AZN", "bp", "VOD"])
check("l4 capitals before lower case", max("ABCDEFGHIJKLMNOPQRSTUVWXYZ") < min("abcdefghijklmnopqrstuvwxyz"))
tr = [("VOD", 72.50), ("AZN", 120.00), ("BP", 4.85)]
check("l4 by price", [t for t, _ in sorted(tr, key=lambda q: q[1], reverse=True)] == ["AZN", "VOD", "BP"])
r5 = [0.012, -0.034, 0.005, -0.008, 0.021]
check("l4 biggest moves", sorted(r5, key=abs, reverse=True)[:2] == [-0.034, 0.021] and sorted(r5, reverse=True)[:2] == [0.021, 0.012] and sorted([0.01, -0.02], key=abs, reverse=True)[:5] == [-0.02, 0.01])
days = [("Mon", 0.021), ("Tue", -0.034), ("Wed", 0.012)]
check("l4 max tuples", max(days) == ("Wed", 0.012) and max(days, key=lambda d: d[1]) == ("Mon", 0.021))
d4 = [("2026-10-12", 0.021), ("2026-10-13", -0.034), ("2026-10-14", 0.012), ("2026-10-15", -0.008)]
check("l4 max dates slip", max(d4)[0] == "2026-10-15")
check("l4 dates are Mon-Thu", [datetime.strptime(d, "%Y-%m-%d").weekday() for d, _ in d4] == [0, 1, 2, 3])
check("l4 q filter", [p for p in [101.20, 99.80, 100.40] if p > 100] == [101.2, 100.4])
check("l4 q min key", min(tk3, key=len) == "bp" and min(tk3) == "AZN")
check("l4 q sort returns None", [3, 1, 2].sort() is None)
check("l4 q <= count", len([r for r in [0.004, 0.0, -0.011, 0.0, -0.002, 0.007] if r <= 0]) == 4)

# ---------------------------------------------------------------- l5
prices = {"VOD": 0.72}
prices["BP"] = 4.85
prices["AZN"] = 118.50
prices["VOD"] = 0.74
check("l5 insertion order", list(prices.items()) == [("VOD", 0.74), ("BP", 4.85), ("AZN", 118.5)] and repr(118.50) == "118.5")
check("l5 KeyError text", repr(raises(KeyError, lambda: prices["TSCO"])) == "\"'TSCO'\"")
fees = {"LSE": 1.50, "TQ": 0.80}
check("l5 get", (fees.get("TQ", 2.00), fees.get("CBOE", 2.00), fees.get("CBOE")) == (0.8, 2.0, None) and "CBOE" not in fees)
check("l5 empty [-1]", bool(raises(IndexError, lambda: [][-1])))
check("l5 position values", math.isclose(500 * 4.85, 2425.0) and math.isclose(-200 * 4.85, -970.0) and math.isclose(150 * 6.42, 963.0) and math.isclose(40 * 27.30, 1092.0) and math.isclose(20 * 118.50, 2370.0))
check("l5 fees", math.isclose(20000 * 0.0010, 20.0) and math.isclose(12500 * 0.0008, 10.0) and math.isclose(4850 * 0.0015, 7.275) and math.isclose(20000 * 0.0015, 30.0))
tot = 0
for v in ["LSE", "TQ", "AQX", "LSE"]:
    tot = tot + fees.get(v, 2.00)
check("l5 q total 5.8", repr(tot) == "5.8" and math.isclose(1.5 + 0.8 + 1.5, 3.8) and math.isclose(1.5 + 0.8 + 2.0, 4.3))
check("l5 q list(d)", list({"b": 2, "a": 1}) == ["b", "a"])
check("l5 q stored None", {"BP": None}.get("BP", 0.0) is None)

# ---------------------------------------------------------------- l6


class Tick:
    eq = 0

    def __init__(self, s):
        self.s = s

    def __hash__(self):
        return hash(self.s)

    def __eq__(self, o):
        Tick.eq += 1
        return self.s == o.s


banned = [Tick(f"T{i}") for i in range(5000)]
bset = set(banned)
Tick.eq = 0
Tick("ZZZ") in banned
list_miss = Tick.eq
Tick.eq = 0
Tick("ZZZ") in bset
set_miss = Tick.eq
check("l6 list miss costs n comparisons", list_miss == 5000)
check("l6 set miss about one", set_miss <= 2)
random.seed(11)
tot_hit = 0
for _ in range(2000):
    Tick.eq = 0
    Tick(f"T{random.randrange(5000)}") in banned
    tot_hit += Tick.eq
check("l6 list hit averages about half", abs(tot_hit / 2000 - 2500.5) < 150)
check("l6 million orders", 10 ** 6 * 5000 == 5 * 10 ** 9)
trades = ["BP", "VOD", "BP", "AZN", "VOD", "BP"]
check("l6 set", len(set(trades)) == 3 and bool(raises(TypeError, lambda: set(trades)[0])))
book = {"BP": 300, "VOD": 1000, "AZN": 0}
check("l6 in keys", (300 in book, "AZN" in book, 300 in book.values()) == (False, True, True))
check("l6 {} is dict", type({}) is dict and type(set()) is set and type({"BP", "VOD"}) is set)
check("l6 other spellings of an empty set exist", eval("{*()}") == set() and type(eval("{*()}")) is set)


def _del_in_loop(d):
    for k in d:
        if d[k] == 0:
            del d[k]


check("l6 del in loop RuntimeError (zero first)", bool(raises(RuntimeError, _del_in_loop, {"BP": 0, "VOD": 1000})))
check("l6 del in loop RuntimeError (zero last)", bool(raises(RuntimeError, _del_in_loop, {"VOD": 1000, "BP": 0})))
s = set([4.85, 4.85, 0.72])
s.add(0.72)
check("l6 q set len", len(s) == 2)
check("l6 q dict add", str(raises(AttributeError, lambda: {}.add("BP"))) == "'dict' object has no attribute 'add'")

# ---------------------------------------------------------------- l7


def cost(price, qty, fee=1.50):
    return price * qty + fee


check("l7 cost", repr(cost(2.50, 100)) == "251.5" and repr(cost(2.50, 100, 0.00)) == "250.0")
try:
    compile("cost(price=2.50, 100)", "<s>", "eval")
    ok = False
except SyntaxError as e:
    ok = "positional argument follows keyword argument" in str(e)
check("l7 positional after keyword SyntaxError", ok)


def fee(notional, rate=0.001, minimum=1.50):
    return max(notional * rate, minimum)


check("l7 fee", (fee(20000.00), fee(500.00), fee(20000.00, 0.0005), fee(20000.00, minimum=25.00), fee(minimum=0.00, notional=500.00), fee(1500.00, rate=0.002), fee(0.00)) == (20.0, 1.5, 10.0, 25.0, 0.5, 3.0, 1.5))


def high_low(ps):
    return max(ps), min(ps)


check("l7 tuple return", repr(high_low([4.80, 4.91, 4.72, 4.85])) == "(4.91, 4.72)")
check("l7 mid spread", math.isclose((4.84 + 4.86) / 2, 4.85) and math.isclose(4.86 - 4.84, 0.02) and ((117.50 + 118.50) / 2, 118.50 - 117.50) == (118.0, 1.0))


def log_trade(ticker, log=[]):
    log.append(ticker)
    return log


la = log_trade("BP")
lb = log_trade("VOD")
check("l7 shared default", lb == ["BP", "VOD"] and la is lb)


def f3(a, b=2, c=None):
    if c is None:
        c = []
    return a, b, c


check("l7 f(1,c=[5])", f3(1, c=[5]) == (1, 2, [5]))


def summarise(returns):
    value = peak = 1.0
    worst = 0.0
    for r in returns:
        value *= 1 + r
        peak = max(peak, value)
        worst = max(worst, 1 - value / peak)
    return sum(returns) / len(returns), worst


check("l7 drawdown", math.isclose(summarise([-0.10, -0.10])[1], 0.19) and math.isclose(summarise([0.01, -0.02, 0.03])[1], 0.02) and summarise([0.02, 0.01])[1] == 0.0 and math.isclose(summarise([0.10, -0.20, 0.05, 0.30, -0.05])[1], 0.2) and math.isclose(summarise([0.01, -0.02, 0.03])[0], 0.00666666666667))


def scale(x, factor=2, offset=0):
    return x * factor + offset


# KNOWN-FINDING 1: the option `6` is explained as "You put 1 into factor".
check("l7 q scale is 11", scale(5, offset=1) == 11)
check("l7 q FINDING: 1 into factor gives 5, not 6", scale(5, 1) == 5 and 5 + 1 == 6)


def _unpack3():
    a, b, c = (1, 2)


check("l7 q unpack message", raises(ValueError, _unpack3) == "not enough values to unpack (expected 3, got 2)")

# ---------------------------------------------------------------- l8


def reset(costs):
    costs = []


x, y = [1.50, 2.00], [1.50, 2.00]
reset(x)
y.clear()
check("l8 reset/clear", repr((x, y)) == "([1.5, 2.0], [])")
pr = [4.91, 4.72]
s_ = sorted(pr)
t_ = pr.sort()
check("l8 sort vs sorted", (s_, t_, pr) == ([4.72, 4.91], None, [4.72, 4.91]))
p3 = [4.91, 4.72, 4.85]
p3.sort()
check("l8 median side effect", p3[0] == 4.72 and p3[len(p3) // 2] == 4.85)
check("l8 even median", math.isclose((4.80 + 4.90) / 2, 4.85))
check("l8 dict copy shallow", (lambda d: dict(d)["a"] is d["a"])({"a": [1]}))
check("l8 book value", math.isclose(500 * 4.85 + 1000 * 0.72, 3145.0) and math.isclose(-20 * 118.50 + 300 * 4.85, -915.0))
xs = [1]
ys = xs + [0]
check("l8 + builds new list", xs == [1] and ys == [1, 0])

# ---------------------------------------------------------------- l9
check("l9 simple return", round(105.00 / 100.00 - 1, 4) == 0.05 and repr(round(105.00 / 100.00 - 1, 4)) == "0.05")
check("l9 log returns", math.log(105 / 100) == 0.04879016416943205 and math.isclose(math.log(99.80 / 101.20), -0.01393057353594691) and math.log(2.0) == 0.6931471805599453)
random.seed(3)
ok = True
for _ in range(20000):
    p0 = random.uniform(1, 500)
    p1 = random.uniform(1, 500)
    if math.log(p1 / p0) > p1 / p0 - 1 + 1e-12:
        ok = False
check("l9 log return never above simple (20,000 random pairs)", ok and math.log(1.0) == 0.0)
check("l9 str/str TypeError", raises(TypeError, lambda: "105" / "100") == "unsupported operand type(s) for /: 'str' and 'str'")
out, err = run_src(
    "import pricing\nprint(round(pricing.log_return(100.00, 105.00), 4))\n",
    {"pricing.py": """
        import math
        def simple_return(p0, p1):
            return p1 / p0 - 1
        def log_return(p0, p1):
            return math.log(p1 / p0)
        print(round(simple_return(100.00, 105.00), 4))
        if __name__ == "__main__":
            print("direct only")
        """},
)
check("l9 import runs module top level once, main guard skipped", out.split() == ["0.05", "0.0488"])
out, err = run_src("from statistics import mean\ncloses=[101.20,102.50,99.80,100.40]\nprint(mean(closes))\nprint(statistics.mean(closes))\n")
# 3.12 and later append "Did you forget to import 'statistics'?" to this message.
check("l9 from-import creates only mean", out.strip() == "100.975" and err.startswith("NameError: name 'statistics' is not defined"))
six = [101.2, 102.5, 99.8, 100.4, 103.1, 102.0]
m6, s6 = statistics.mean(six), statistics.stdev(six)
check("l9 band", (round(m6 - 2 * s6, 2), round(m6 + 2 * s6, 2)) == (98.97, 104.03) and math.isclose(m6, 101.5) and round(s6, 2) == 1.26 and all(98.97 < c < 104.03 for c in six))
check("l9 band 2", (round(100 - 2 * statistics.stdev([99.0, 101.0]), 2), round(100 + 2 * statistics.stdev([99.0, 101.0]), 2)) == (97.17, 102.83))
check("l9 pstdev narrower", statistics.pstdev(six) < s6 and statistics.mean([1, 2, 3]) == 2 and statistics.stdev([1, 2, 3]) == 1.0)
out, err = run_src("from statistics import mean\n", {"statistics.py": "x = 1\n"})
# 3.12 prints exactly the content's line; 3.13 appends a "consider renaming" hint.
check("l9 shadowed statistics ImportError", err.startswith("ImportError: cannot import name 'mean' from 'statistics' (") and "statistics.py" in err)
out, err = run_src("import random\nrandom.seed(1)\n", {"random.py": "x = 1\n"}, name="walk.py")
check("l9 q shadowed random AttributeError", err.startswith("AttributeError: module 'random' has no attribute 'seed'"))
out, err = run_src("import math\nprint(sqrt(16))\n")
check("l9 q sqrt NameError", err.startswith("NameError: name 'sqrt' is not defined"))
check("l9 sys is built in", "sys" in sys.builtin_module_names and "statistics" not in sys.builtin_module_names and "random" not in sys.builtin_module_names and "csv" not in sys.builtin_module_names)
random.seed(7)
first = [random.choice([0.99, 1.01]) for _ in range(3)]
random.seed(7)
second = [random.choice([0.99, 1.01]) for _ in range(3)]
check("l9 seed 7 draws", first == second == [1.01, 0.99, 1.01])


def walk(start, days_, seed):
    random.seed(seed)
    ps = [start]
    for _ in range(days_):
        ps.append(ps[-1] * random.choice([0.99, 1.01]))
    return ps


w = walk(100.00, 20, 7)
canvas = [100.0, 101.0, 99.99, 100.99, 99.98, 98.98, 97.99, 98.97, 97.98, 97.0, 96.03, 95.07, 96.02, 96.98, 96.01, 95.05, 94.1, 95.04, 94.09, 93.15, 92.22]
check("l9 walk seed 7", w[-1] == 92.21911860045137 and [round(p, 2) for p in w] == canvas and sum(1 for a_, b_ in zip(w, w[1:]) if b_ > a_) == 6)
check("l9 walk seed 42", [round(p, 6) for p in walk(250.00, 3, 42)] == [250.0, 247.5, 245.025, 247.47525])
check("l9 q Counter", Counter(["up", "down", "up", "up", "down"]).most_common(1) == [("up", 3)])
check("l9 q str repeat", 3 * "2.50" == "2.502.502.50")

# ---------------------------------------------------------------- l10
text = "date,close\n2024-03-11,101.20\n2024-03-12,102.50\n2024-03-13,99.80\n2024-03-14,100.40\n"
rows = list(csv.DictReader(text.splitlines()))
check("l10 rows", rows[2]["close"] == "99.80" and repr(rows[0]) == "{'date': '2024-03-11', 'close': '101.20'}")
check("l10 header only", list(csv.DictReader("date,close\n".splitlines())) == [])
sp = "date, close\n2024-03-11, 101.20\n"
r = list(csv.DictReader(sp.splitlines()))[0]
check("l10 space kept in key", list(r) == ["date", " close"] and bool(raises(KeyError, lambda: r["close"])))
r = list(csv.DictReader(sp.splitlines(), skipinitialspace=True))[0]
check("l10 skipinitialspace", r["close"] == "101.20")
check("l10 max text", max(x["close"] for x in rows) == "99.80" and max(float(x["close"]) for x in rows) == 102.5)
dd = ["15/03/2024", "02/04/2024", "28/02/2024"]
check("l10 text sort", sorted(dd) == ["02/04/2024", "15/03/2024", "28/02/2024"])
check("l10 date sort", [d for _, d in sorted((datetime.strptime(d, "%d/%m/%Y"), d) for d in dd)] == ["28/02/2024", "15/03/2024", "02/04/2024"])
check("l10 year end text sort wrong", sorted(["05/01/2025", "31/12/2024"]) == ["05/01/2025", "31/12/2024"] and "01/03/2024" < "28/02/2024")
cs = [100.00, 100.40, 102.00, 101.60, 103.10]
check("l10 vendor returns", [round(b_ / a_ - 1, 4) for a_, b_ in zip(cs, cs[1:])] == [0.004, 0.0159, -0.0039, 0.0148] and round(250 / 240 - 1, 4) == 0.0417)
check("l10 vendor dates are consecutive trading days", [datetime.strptime(d, "%d/%m/%Y").weekday() for d in ["28/02/2024", "29/02/2024", "01/03/2024", "04/03/2024", "05/03/2024"]] == [2, 3, 4, 0, 1])
check("l10 q repeat", "101.20" * 2 == "101.20101.20" and float("101.20") * 2 == 202.4)
t6 = "h,c\n" + "a,1\n" * 5 + "\n"
check("l10 q blank line skipped", len(list(csv.DictReader(t6.splitlines()))) == 5 and t6.splitlines()[-1] == "")
check("l10 q strptime mismatch", bool(raises(ValueError, lambda: datetime.strptime("2024-03-15", "%d/%m/%Y"))) and datetime.strptime("2024-03-15", "%Y-%m-%d").day == 15)
check("l10 q ISO sorts", sorted(["2024-03-15", "2024-02-28", "2024-04-02"]) == ["2024-02-28", "2024-03-15", "2024-04-02"])

# ---------------------------------------------------------------- l11
check("l11 float n/a", bool(raises(ValueError, lambda: float("n/a"))) and bool(raises(ValueError, lambda: float(""))) and bool(raises(ValueError, lambda: float("1,234.50"))) and float(" 99.80 ") == 99.8)
check("l11 nan inf readable", math.isnan(float("nan")) and math.isinf(float("inf")))
check("l11 float(None) TypeError", bool(raises(TypeError, lambda: float(None))))
# 3.12 and 3.13 word this "float division by zero"; later versions may shorten it.
check("l11 ZeroDivisionError", "division by zero" in str(raises(ZeroDivisionError, lambda: 101.20 / 0.00)))
check("l11 int text", bool(raises(ValueError, lambda: int("abc"))) and bool(raises(ValueError, lambda: int("2.5"))) and int(" 40 ") == 40 and int(12.5) == 12 and int(float("12.5")) == 12)
check("l11 unpack split", bool(raises(ValueError, lambda: (lambda a, b: 0)(*"HSBA".split(",")) if False else exec("a, b = 'HSBA'.split(',')"))) and bool(raises(ValueError, lambda: exec("a, b = 'SHEL,10,20'.split(',')"))))
check("l11 None.split AttributeError", bool(raises(AttributeError, lambda: None.split(","))))
src = """
def clean(raw):
    out = []
    for p in raw:
        try:
            out.append(flaot(p))
        except ValueError:
            pass
    return out

print(clean(["101.20"]))
"""
out, err = run_src(src.lstrip("\n"))
check("l11 typo surfaces as NameError", err.startswith("NameError: name 'flaot' is not defined"))
out, err = run_src('try:\n    qty = int("40")\n    price = float("£7.25")\nexcept ValueError:\n    qty = 0\nprint(qty)\n')
check("l11 q qty 0", out.strip() == "0")

# ---------------------------------------------------------------- l12


class Position:
    def __init__(self, ticker, qty, avg_price):
        self.ticker = ticker
        self.qty = qty
        self.avg_price = avg_price

    def value(self, price):
        return self.qty * price

    def pnl(self, price):
        return self.qty * (price - self.avg_price)


shel = Position("SHEL", 150, 26.40)
check("l12 value", repr(shel.value(27.00)) == "4050.0" and math.isclose(150 * 26.40, 3960.0) and Position.value(shel, 27.00) == 4050.0)
check("l12 pnl", shel.pnl(27.00) == 90.00000000000021 and Position("AZN", 40, 104.20).pnl(101.50) == -108.00000000000011 and Position("BARC", -500, 1.85).pnl(1.80) == 25.00000000000002 and Position("BARC", -500, 1.85).value(1.80) == -900.0)
check("l12 default repr", repr(shel).startswith("<__main__.Position object at 0x") and str(shel) == repr(shel))
check("l12 missing arg", bool(raises(TypeError, lambda: Position.pnl(101.50))))


class NoSelf:
    def __init__(self, ticker, qty):
        qty = qty


check("l12 no self AttributeError", raises(AttributeError, lambda: NoSelf("S", 1).qty) == "'NoSelf' object has no attribute 'qty'")


class Book:
    trades = []

    def add(self, t):
        self.trades.append(t)


mine, yours = Book(), Book()
mine.add("VOD +100")
check("l12 class-body list shared", len(yours.trades) == 1)


class BadRepr:
    def __repr__(self):
        print("x", end="")


import contextlib
import io

with contextlib.redirect_stdout(io.StringIO()):
    check("l12 repr must return str", bool(raises(TypeError, lambda: repr(BadRepr()))))
check("l12 cash", round(-(1000 * 0.72 + -400 * 0.75), 2) == -420.0 and round(-(40 * 104.20 + -500 * 1.85 + 10 * 101.50), 2) == -4258.0)


class P1:
    def __init__(self, q):
        self.qty = q

    def value(price):
        return self.qty * price  # noqa: F821


check("l12 q missing self TypeError", "takes 1 positional argument but 2 were given" in str(raises(TypeError, lambda: P1(10).value(5.00))))


class P2:
    def __init__(self, t, q):
        self.t, self.q = t, q

    def __repr__(self):
        return f"{self.t} x{self.q}"


check("l12 q list uses repr", str([P2("VOD", 100), P2("AZN", 40)]) == "[VOD x100, AZN x40]")


class P3:
    def __init__(self, t, q):
        self.t, self.q = t, q

    def __str__(self):
        return f"{self.t} x{self.q}"


check("hw3 str only", str(P3("VOD", 100)) == "VOD x100" and str([P3("VOD", 100)]).startswith("[<__main__.P3 object at 0x"))

# ---------------------------------------------------------------- reviews
check("r1 1.1+2.2", repr(1.1 + 2.2) == "3.3000000000000003")
c5 = [101.20, 102.50, 99.80, 100.40, 103.10]
check("r1 [-4:-1]", c5[-4:-1] == [102.5, 99.8, 100.4])
check("r1 -4.35*100", repr(-4.35 * 100) == "-434.99999999999994" and int(-4.35 * 100) == -434 and round(-4.35 * 100) == -435 and math.floor(-4.35 * 100) == -435)
check("r1 str*2", "BP,4.85,250".split(",")[1] * 2 == "4.854.85" and bool(raises(TypeError, lambda: "a" * 2.0)))
check("r2 items/keys/in", (("TQ", 0.60) in {"LSE": 1.25, "TQ": 0.60}.items(), "LSE" in {"LSE": 1.25}.keys(), 1.25 in {"LSE": 1.25}) == (True, True, False))
check("r2 tuple append", bool(raises(AttributeError, lambda: ().append(1))))
check("r3 sqrt", math.sqrt(2.25) == 1.5)
check("r3 sum of str", raises(TypeError, lambda: sum(["101.20"])) == "unsupported operand type(s) for +: 'int' and 'str'")
cl5 = ["101.20", "99.80", "100.40", "98.75", "102.50"]
check("r3 text compare count", sum(1 for c in cl5 if c > "100") == 5 and sum(1 for c in cl5 if float(c) > 100) == 3)
check("r3 average", round(statistics.mean(c5), 2) == 101.4 and math.isclose(sum(c5), 507.0) and round(statistics.mean([0.72, 0.75, 0.74]), 2) == 0.74)
check("r3 list key TypeError", bool(raises(TypeError, lambda: {"VOD": 0.72}[["VOD"]])))
check("r3 avg price", (100 * 26.00 + 50 * 27.50) / 150 == 26.5 and 100 * 26.00 + 50 * 27.50 == 3975 and math.isclose(((40 * 104.20 + 10 * 101.50) + 50 * 100.00) / 100, 101.83) and (26.00 + 27.50) / 2 == 26.75)

# ---------------------------------------------------------------- homework
check("hw1 round ties", round(2.5) + round(3.5) == 6 and type(round(2.5)) is int)
check("hw1 [3:-2]", len(list(range(20))[3:-2]) == 15 and len(list(range(20))[3:]) == 17)
bk = [[0.0, 0.0]] * 3
bk[0][0] = 99.5
check("hw1 list * 3", bk == [[99.5, 0.0]] * 3 and bk[0] is bk[2])
pos = ("VOD", [72.50])
pos[1].append(73.10)
check("hw1 tuple holds list", repr(pos) == "('VOD', [72.5, 73.1])")
k4 = [100.0, 102.0, 105.0, 99.75]
check("hw1 k-day", [(b_ - a_) / a_ for a_, b_ in zip(k4, k4[2:])] == [0.05, -0.022058823529411766] and math.isclose((99.75 - 105.0) / 105.0, -0.05) and (102.0 - 100.0) / 100.0 == 0.02)
check("hw1 stable sort", [t for t, p in sorted([("BP", 4.85), ("VOD", 4.85), ("AZN", 1.20)], key=lambda q: q[1])] == ["AZN", "BP", "VOD"])
check("hw1 mismatch message", f"mismatch: {sum([0.10, 0.20]):.2f} vs {0.30:.2f}" == "mismatch: 0.30 vs 0.30" and sum([0.10, 0.20]) != 0.30)
check("hw1 isclose abs_tol", math.isclose(0.1 + 0.2 - 0.3, 0.0, abs_tol=0.005))
try:
    compile("[t if p * q > 1000 for t, p, q in trades]", "<s>", "eval")
    ok = False
except SyntaxError:
    ok = True
check("hw1 if before for needs else", ok)
W = [("Mon", 100.0, 101.0), ("Tue", 103.02, 102.0), ("Wed", 101.49, 100.5), ("Thu", 100.5, 99.0), ("Fri", 97.0, 98.0)]
gaps = [(t[1] - b[2]) / b[2] for b, t in zip(W, W[1:])]
check("hw1 gaps", all(math.isclose(g, e, abs_tol=1e-12) for g, e in zip(gaps, [0.02, -0.005, 0.0, -0.020202020202020204])) and [d[0] for d, g in zip(W[1:], gaps) if abs(g) > 0.0] == ["Tue", "Wed", "Fri"])
check("hw2 pnl", math.isclose(500 * (4.85 - 4.80) + -200 * (4.85 - 4.90), 35.0) and math.isclose(-20 * (118.50 - 120.00), 30.0) and math.isclose(40 * (26.00 - 27.30) + -40 * (26.00 - 27.50), 8.0))
check("hw2 commission", math.isclose(25000 * 0.0012, 30.0) and math.isclose(800 * 0.0012, 0.96) and math.isclose(4000 * 0.0009, 3.6) and math.isclose(100000 * 0.002, 200.0))
check("hw2 review model", raises(TypeError, lambda: [t for t in None]) == "'NoneType' object is not iterable" and (4.85 in {"BP": 4.85}) is False)
check("hw2 weights", math.isclose(750 / 4000, 0.1875) and 300 * 5.0 + -60 * 25.0 == 0 and 4 // 14 == 0 and math.isclose(500 / 1250, 0.4))
lr = [round(math.log(b_ / a_), 6) for a_, b_ in zip([100.0, 101.2, 99.8, 100.4, 103.1], [101.2, 99.8, 100.4, 103.1])]
check("hw3 log returns", lr == [0.011929, -0.013931, 0.005994, 0.026537] and round(sum(lr), 6) == 0.030529 and round(math.log(103.10 / 100.00), 6) == 0.030529)
check("hw3 strptime", datetime.strptime("2024-03-15 16:30", "%Y-%m-%d %H:%M").minute == 30)
exact = sum(math.comb(20, k) for k in range(11, 21)) / 2 ** 20
check("hw3 exact 0.4119", round(exact, 4) == 0.4119)
check("hw3 10 up 10 down below start", round(100 * 0.9999 ** 10, 2) == 99.9 and 1.01 ** 11 * 0.99 ** 9 > 1)


def share_above(paths, days_, seed):
    random.seed(seed)
    above = 0
    for _ in range(paths):
        price = 100.0
        for _ in range(days_):
            price *= random.choice([0.99, 1.01])
        if price > 100.0:
            above += 1
    return above / paths


check("hw3 seeded shares", (share_above(1000, 20, 1), share_above(2000, 20, 7), share_above(1000, 1, 3), share_above(10, 0, 1)) == (0.407, 0.4085, 0.502, 0.0))
# Monte Carlo: 200,000 paths; s.e. = sqrt(0.4119*0.5881/200000) = 0.0011, so 0.4119 +/- 0.005 separates it from 0.5 or 0.588.
mc = share_above(200000, 20, 2024)
check("hw3 simulation converges to 0.4119", abs(mc - exact) < 0.005)
check("hw3 0.7 three times", repr(0.7 + 0.7 + 0.7) == "2.0999999999999996" and (3 * round(0.7 * 100)) / 100 == 2.1 and round(19.99 * 100) == 1999 and -1999 / 100 == -19.99 and 29 / 100 == 0.29)
check("hw3 str*float message", raises(TypeError, lambda: "150" * 27.00) == "can't multiply sequence by non-int of type 'float'")
check("hw3 text max", max(["99.80", "104.20"]) == "99.80")

# ---------------------------------------------------------------- harness
# Every code widget in scope: the solution passes its tests, the starter does
# not pass them all, `how` states the right number of tests, every
# feedback.byKey.test-N names a test that exists, every example is consistent.
import glob
import json
import re

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, "..", "..", "app", "content", "courses", "py-found")


def _close(a, b):
    if isinstance(a, bool) or isinstance(b, bool):
        return a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)) and len(a) == len(b):
        return all(_close(x_, y_) for x_, y_ in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict) and a.keys() == b.keys():
        return all(_close(a[k], b[k]) for k in a)
    return a == b


def _run(code, w, t):
    ns = {"__name__": "__main__", "__learner_source__": code}
    try:
        exec(w.get("prelude", ""), ns)
        exec(code, ns)
        if t.get("setup"):
            exec(t["setup"], ns)
        got = eval(t["call"], ns)
    except Exception as e:  # a test may expect the exception class
        got = type(e)
    exp = t["expect"]
    if isinstance(exp, str):
        try:
            exp = eval(exp, dict(ns))
        except Exception:
            pass
    return _close(got, exp)


names = ["l%d-*.json" % i for i in range(1, 13)] + ["review-[123].json", "homework-[123].json"]
widgets = 0
for pat in names:
    for path in sorted(glob.glob(os.path.join(COURSE, pat))):
        doc = json.load(open(path, encoding="utf-8"))
        base = os.path.basename(path)
        for coll in ("screens", "quiz", "items"):
            for i, sc in enumerate(doc.get(coll, [])):
                w = sc.get("widget") or {}
                if "tests" not in w:
                    continue
                widgets += 1
                tag = f"{base} {coll}[{i}]"
                n = len(w["tests"])
                with contextlib.redirect_stdout(io.StringIO()):
                    sol = [_run(w["solution"], w, t) for t in w["tests"]]
                    sta = [_run(w["starter"], w, t) for t in w["tests"]]
                check(f"harness {tag} solution passes all {n} tests", all(sol))
                check(f"harness {tag} starter fails at least one test", not all(sta))
                m = re.search(r"runs (\d+) hidden", w.get("how", ""))
                check(f"harness {tag} how count", (not m) or int(m.group(1)) == n)
                keys = [int(k[5:]) for k in (sc.get("feedback") or {}).get("byKey", {}) if re.fullmatch(r"test-\d+", k)]
                check(f"harness {tag} byKey test indices exist", all(1 <= k <= n for k in keys))
check("harness found the code widgets", widgets == 58)

# ---------------------------------------------------------------- findings
# Each check reads the content string and fails while the flawed wording is
# there. See docs/reviews/audit-py-found-1-3-r2.md for the fixes.


def _text(fname, *keys):
    node = json.load(open(glob.glob(os.path.join(COURSE, fname))[0], encoding="utf-8"))
    for k in keys:
        node = node[k]
    return node


check("FINDING 1 l7 quiz[0] option 6: 'put 1 into factor' gives 5, not 6", "You put 1 into" not in _text("l7-*.json", "quiz", 0, "widget", "options", 1, "why"))
check("FINDING 2 l6 screens[7]: set() is not the only empty set", "only way" not in _text("l6-*.json", "screens", 7, "feedback", "correct"))
check("FINDING 3 l3 screens[1]: commas, not brackets, make the tuple", "comma" in _text("l3-*.json", "screens", 1, "prose"))
check("FINDING 4 l8 summary.ideas[2]: pure needs 'only' and no other effect", "A pure function reads its arguments and returns" not in _text("l8-*.json", "summary", "ideas", 2))
check("FINDING 5 l12 screens[1]: first parameter is not always the object before the dot", "always the object before the dot" not in _text("l12-*.json", "screens", 1, "explain", "text"))
check("FINDING 6 l1 screens[2]: a double holds about 16 digits, not 17", "about 17 significant" not in _text("l1-*.json", "screens", 2, "prose"))

print(f"{N} checks, {len(FAILS)} failed (Python {sys.version.split()[0]})")
sys.exit(1 if FAILS else 0)
