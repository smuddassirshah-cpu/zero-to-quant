"""Second read of py-found h-overnight-gaps (L1), h-book-weights (L2), h-cash-account (L3).
For each: recomputes the expects by another route (Fractions or a hand loop), runs the
shipped solution, the starter, a reader solution by another route and reader-planted
slips (none from the authors' lists) through harness.py, and times the slowest case.
Exit 0 when every expectation below holds. Run from this folder with the venv Python."""
import sys
from fractions import Fraction as F
from harness import item, run, summary

BAD = []


def check(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond:
        BAD.append(msg)


def battery(w, label, reader, bugs):
    print(f"== {label}")
    f, r = summary(w, w["solution"], "shipped solution")
    check(not f, f"{label}: shipped solution passes every test")
    fe = [x for x in run(w, w["solution"], "examples") if x[0] != "pass"]
    check(not fe, f"{label}: shipped solution passes the example")
    f, _ = summary(w, w["starter"], "starter")
    check(len(f) == len(w["tests"]), f"{label}: starter fails every test")
    f, r2 = summary(w, reader, "reader solution")
    check(not f, f"{label}: reader solution passes every test")
    check(max(x[2] for x in r + r2) < 0.5, f"{label}: slowest case under 0.5 s in CPython")
    for name, src in bugs.items():
        f, _ = summary(w, src, "slip: " + name)
        check(bool(f), f"{label}: planted '{name}' caught by tests {f}")
    check(w["examples"][0] == w["tests"][0], f"{label}: the one example repeats test 1")


# ---------- L1 overnight gaps ----------
W1 = item("py-found", "homework-1.json", "h-overnight-gaps")["widget"]
Wk = [("Mon", 100, 101), ("Tue", F(10302, 100), 102), ("Wed", F(10149, 100), F(1005, 10)), ("Thu", F(1005, 10), 99), ("Fri", 97, 98)]
g = [(F(t[1]) - b[2]) / F(b[2]) for b, t in zip(Wk, Wk[1:])]
check(g == [F(2, 100), F(-5, 1000), 0, F(-2, 99)], f"L1 week gaps in Fractions: {[str(x) for x in g]}")
check([d[0] for d, x in zip(Wk[1:], g) if abs(x) > F(1, 100)] == ["Tue", "Fri"], "L1 flags at 0.01: Tue, Fri")
check([d[0] for d, x in zip(Wk[1:], g) if abs(x) > 0] == ["Tue", "Wed", "Fri"], "L1 flags at 0: Tue, Wed, Fri (Thu is exactly 0)")
check(not [d for d, x in zip(Wk[1:], g) if abs(x) > F(5, 100)], "L1 flags at 0.05: none")
V = [("02 Mar", 250, 248), ("03 Mar", F(25544, 100), 256), ("04 Mar", F(24576, 100), 247), ("05 Mar", 247, 250), ("06 Mar", 251, F(2495, 10)), ("09 Mar", F(2495, 10), 251)]
gv = [(F(t[1]) - b[2]) / F(b[2]) for b, t in zip(V, V[1:])]
check(gv == [F(3, 100), F(-4, 100), 0, F(4, 1000), 0], f"L1 March gaps: {[str(x) for x in gv]}")
check(min(abs(abs(x) - F(25, 1000)) for x in gv) >= F(5, 1000), "L1 no March gap within 0.005 of the 0.025 limit, so float noise cannot move a flag")
check(min(abs(abs(x) - F(1, 100)) for x in g) >= F(5, 1000), "L1 no week gap within 0.005 of the 0.01 limit")

R1 = '''
def overnight_gaps(days, limit):
    gaps = [(days[i][1] - days[i - 1][2]) / days[i - 1][2] for i in range(1, len(days))]
    flagged = [days[i][0] for i in range(1, len(days)) if gaps[i - 1] > limit or gaps[i - 1] < -limit]
    return (gaps, flagged)
'''
S1 = W1["solution"]
B1 = {
    "log gap ln(o_t / c_{t-1})": "import math\n" + S1.replace("(today[1] - before[2]) / before[2]", "math.log(today[1] / before[2])"),
    "gaps rounded to 4 places": S1.replace("(today[1] - before[2]) / before[2] for", "round((today[1] - before[2]) / before[2], 4) for"),
    "every gap against the first close": S1.replace("(today[1] - before[2]) / before[2]", "(today[1] - days[0][2]) / days[0][2]"),
    "flagged dates sorted": S1.replace("return gaps, flagged", "return gaps, sorted(flagged)"),
    "flags kept as (date, gap) pairs": S1.replace("[day[0] for day", "[(day[0], gap) for day"),
    "lists returned the other way round": S1.replace("return gaps, flagged", "return flagged, gaps"),
}
battery(W1, "L1 h-overnight-gaps", R1, B1)

# ---------- L2 book weights ----------
W2 = item("py-found", "homework-2.json", "h-book-weights")["widget"]
P = {"VOD": F(75, 100), "BP": F(5), "AZN": F(120)}
B = {"VOD": 1000, "BP": 300, "AZN": 10}
tot = sum(q * P[t] for t, q in B.items())
check(tot == 3450 and tot + 550 == 4000, "L2 holdings £3,450, with cash £4,000")
check({t: q * P[t] / 4000 for t, q in B.items()} == {"VOD": F(3, 16), "BP": F(3, 8), "AZN": F(3, 10)}, "L2 test 2 weights 0.1875, 0.375, 0.3")
check({t: q * P[t] / 3450 for t, q in B.items()} == {"VOD": F(750, 3450), "BP": F(1500, 3450), "AZN": F(1200, 3450)}
      and abs(float(F(1500, 3450)) - 0.43478260869565216) < 1e-16, "L2 test 3 weights over £3,450")
check(F(300 * 5 - 20 * 25 + 500) == 1500 and F(-500, 1500) == F(-1, 3), "L2 test 7: total £1,500, SHEL -1/3")
check(3 * 2 + 1 * 4 + 4 == 14 and abs(float(F(6, 14)) - 0.42857142857142855) < 1e-16, "L2 test 8: total 14, VOD 6/14")
check(F(750, 1250) == F(3, 5) and F(500, 1250) == F(2, 5), "L2 test 10: VOD 0.6, TSCO 0.4 once priced")

R2 = '''
def book_weights(book, prices, cash=0.0):
    if not all(t in prices for t in book):
        return None
    values = {t: q * prices[t] for t, q in book.items()}
    total = cash + sum(values.values())
    if total == 0:
        return None
    return {t: v / total for t, v in values.items()}
'''
S2 = W2["solution"]
B2 = {
    "cash subtracted": S2.replace("total = cash", "total = -cash"),
    "{} for a missing price": S2.replace("            return None", "            return {}"),
    "cash checked for zero, not added to the weights' total": S2.replace("total = cash\n", "total = 0\n").replace("    if total == 0:", "    if total + cash == 0:"),
    "weights rounded to 4 places": S2.replace("qty * prices[ticker] / total", "round(qty * prices[ticker] / total, 4)"),
    "zero total gives an empty dict": S2.replace("    if total == 0:\n        return None", "    if total == 0:\n        return {}"),
}
battery(W2, "L2 h-book-weights", R2, B2)

# ---------- L3 cash account ----------
W3 = item("py-found", "homework-3.json", "h-cash-account")["widget"]
check(0.7 + 0.7 + 0.7 != 2.1 and 210 / 100 == 2.1, "L3 float pounds miss 2.1; 210 pence / 100 is exactly 2.1")
check(int(0.29 * 100) == 28 and round(0.29 * 100) == 29, "L3 int(0.29 * 100) is 28, round gives 29")
check((1000 + 250 - 400) / 100 == 8.5 and (1999 - 1999) / 100 == 0.0, "L3 test 1 balance 8.5, test 4 balance 0.0")
R3 = '''
class Account:
    def __init__(self, opening=0.0):
        self._open = int(round(opening * 100))
        self._moves = []

    def _pence(self, amount):
        if not amount > 0:
            raise ValueError("not above zero")
        return int(round(amount * 100))

    def deposit(self, amount):
        self._moves.append(self._pence(amount))

    def withdraw(self, amount):
        p = self._pence(amount)
        if p > self._open + sum(self._moves):
            raise ValueError("more than the balance")
        self._moves.append(-p)

    def balance(self):
        return (self._open + sum(self._moves)) / 100

    def history(self):
        return [m / 100 for m in self._moves]
'''
S3 = W3["solution"]
B3 = {
    "int(round(amount, 2) * 100)": S3.replace("p = round(amount * 100)", "p = int(round(amount, 2) * 100)"),
    "no default opening": S3.replace("def __init__(self, opening=0.0):", "def __init__(self, opening):"),
    "withdrawal logged as +p": S3.replace("self.moves.append(-p)", "self.moves.append(p)"),
    "refused overdraft clears the balance to 0": S3.replace('            raise ValueError(f"only', '            self.pence = 0\n            raise ValueError(f"only'),
    "balance rounded down to whole pounds": S3.replace("return self.pence / 100", "return self.pence // 100"),
}
battery(W3, "L3 h-cash-account", R3, B3)

print(f"\n{len(BAD)} failures")
sys.exit(1 if BAD else 0)
