"""Second read, py-found level 3 (l9 to l12, review-3, homework-3): recompute every stated number, two ways where a
second method exists, check it appears where it is stated (app/tools/numbers_lib.py), check code-behaviour claims in
CPython, and run every code widget (solution passes every hidden test, starter fails at least one).
Run: python3 docs/reports/py-found-L3-numbers.py   (exits 0 on correct content)
Checks that fail on the content as read (review-py-found-3-4.md findings): l9 log-vs-simple "always" claim,
l10 r3c1 "counted from 1", l10 "quotes and all", l11 quiz[2] "None 0.025", homework-3 items[7] line numbers.
"""
import contextlib, csv, io, json, math, os, random, statistics, subprocess, sys, tempfile
from datetime import datetime
from fractions import Fraction
from math import comb
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("py-found", 3)
E = lv.expect


def run(code):
    """exec code, return (namespace, printed text)"""
    ns, out = {'__name__': '__main__'}, io.StringIO()
    with contextlib.redirect_stdout(out):
        exec(code, ns)
    return ns, out.getvalue()


def raises(fn):
    try:
        fn()
    except Exception as e:
        return type(e).__name__ + ': ' + str(e)
    return None


# ---------------- l9 ----------------
r = 105.00 / 100.00 - 1
E("l9", "screens[1].widget.options[0].text", round(r, 4))
lv.claim(abs(r - float(Fraction(105, 100) - 1)) < 1e-12, "l9 simple return 0.05 two ways")
E("l9", "screens[1].widget.options[1].text", round(105.00 - 100.00, 4))
lr = math.log(105 / 100)
lv.claim(abs(lr - math.log1p(0.05)) < 1e-15, "l9 ln(1.05) two ways (log, log1p)")
E("l9", "screens[2].widget.tests[2].expect", lr)
E("l9", "screens[2].explain.text", 0.04879)
E("l9", "screens[2].widget.tests[3].expect", math.log(99.80 / 101.20))
E("l9", "screens[2].widget.tests[5].expect", math.log(2))
E("l9", "screens[2].widget.tests[1].expect", round(240 / 250 - 1, 10))
# "A log return always sits a little below the simple one": false at an unchanged price (both 0, the screen's own test 5)
# and not "a little" for test 6 (0.693 against 1.0)
# the true statement: ln(1 + r) <= r, equal only at r = 0 (fix: "never above ... match only when the price is unchanged")
lv.claim(all(math.log(b / a) <= b / a - 1 for a, b in [(100, 105), (100, 100), (50, 100), (100, 50)]) and math.log(1.0) == 0.0 and math.log(1.05) < 0.05,
         "l9 log return never above the simple one, equal only at r = 0")
lv.claim("never above the simple one" in lv.text("l9", "screens[2].explain.text") and "always sits" not in lv.text("l9", "screens[2].explain.text"), "l9 screens[2] explain carries the corrected sentence")
lv.claim(raises(lambda: run('def simple_return(p0: float, p1: float) -> float:\n    return p1 / p0 - 1\nsimple_return("100", "105")'))
         == "TypeError: unsupported operand type(s) for /: 'str' and 'str'", "l9 screens[3] TypeError text")
E("l9", "screens[4].widget.options[0].text", round(lr, 4))
closes4 = [101.20, 102.50, 99.80, 100.40]
E("l9", "screens[5].widget.options[1].text", statistics.mean(closes4))
lv.claim(abs(statistics.mean(closes4) - sum(closes4) / 4) < 1e-12, "l9 mean 100.975 two ways")
c6 = [101.2, 102.5, 99.8, 100.4, 103.1, 102.0]
m6, s6 = statistics.mean(c6), statistics.stdev(c6)
s6b = math.sqrt(sum((x - m6) ** 2 for x in c6) / 5)
lv.claim(abs(s6 - s6b) < 1e-12, "l9 stdev two ways")
E("l9", "screens[6].explain.text", m6)
t6 = lv.text("l9", "screens[6].explain.text")
lv.claim(f"£{s6:.2f}" in t6 and f"£{m6:.2f}" in t6 and "£101.500" not in t6 and "1.265" not in t6, f"l9 screens[6] states £{m6:.2f} and £{s6:.2f}, two places")
lv.claim("£100.975" not in lv.text("l9", "screens[5].explain.text") and "100.975" in lv.text("l9", "screens[5].explain.text"), "l9 screens[5] no three-place money")
for v in (round(m6 - 2 * s6, 2), round(m6 + 2 * s6, 2)):
    E("l9", "screens[6].widget.tests[0].expect", v)
    E("l9", "screens[6].feedback.correct", v)
    E("l9", "screens[6].canvas.params.series[1].values[0]" if v > 100 else "screens[6].canvas.params.series[2].values[0]", v)
lv.claim(all(m6 - 2 * s6 < x < m6 + 2 * s6 for x in c6), "l9 every close sits inside the band")
lv.claim(statistics.pstdev(c6) < s6, "l9 pstdev gives a narrower band")
b2 = (round(100 - 2 * math.sqrt(2), 2), round(100 + 2 * math.sqrt(2), 2))
lv.claim(b2 == (round(statistics.mean([99, 101]) - 2 * statistics.stdev([99, 101]), 2), round(101 - 1 + 2 * statistics.stdev([99, 101]), 2)) == (97.17, 102.83), "l9 band([99, 101])")
random.seed(7)
first = [random.choice([0.99, 1.01]) for _ in range(3)]
E("l9", "screens[9].explain.text", "[1.01, 0.99, 1.01]") if first == [1.01, 0.99, 1.01] else lv.claim(False, "l9 seed 7 draws", str(first))


def walk(start, days, seed):
    random.seed(seed)
    p = [start]
    for _ in range(days):
        p.append(p[-1] * random.choice([0.99, 1.01]))
    return p


w = walk(100.0, 20, 7)
ups = sum(1 for a, b in zip(w, w[1:]) if b > a)
lv.claim(abs(w[-1] - 100 * 1.01 ** ups * 0.99 ** (20 - ups)) < 1e-9, "l9 walk end two ways (path, closed form)")
lv.claim([round(x, 2) for x in w] == lv.files['l9-splitting-files']['screens'][10]['canvas']['params']['series'][0]['values'], "l9 canvas path = walk(100, 20, 7) rounded")
E("l9", "screens[10].widget.tests[2].expect", w[-1])
E("l9", "screens[10].feedback.correct", round(w[-1], 2))
E("l9", "screens[10].feedback.correct", ups)
E("l9", "screens[10].explain.text", ups)
lv.claim([round(x, 6) for x in walk(250.0, 3, 42)] == [250.0, 247.5, 245.025, 247.47525], "l9 walk(250, 3, 42)")
from collections import Counter
lv.claim(Counter(["up", "down", "up", "up", "down"]).most_common(1) == [('up', 3)], "l9 quiz[1] most_common")
lv.claim(3 * "2.50" == "2.502.502.50", "l9 quiz[3] 3 * '2.50'")
lv.claim(raises(lambda: run('import math\nprint(sqrt(16))')) == "NameError: name 'sqrt' is not defined", "l9 quiz[0] NameError")

# ---------------- l10 ----------------
text = "date,close\n2024-03-11,101.20\n2024-03-12,102.50\n2024-03-13,99.80\n2024-03-14,100.40\n"
rows = list(csv.DictReader(text.splitlines()))
lv.claim(rows[2]["close"] == "99.80" and rows[0] == {'date': '2024-03-11', 'close': '101.20'}, "l10 rows[2] and rows[0]")
# byKey r3c1 says "You counted from 1"; counting from 1 makes rows[2] the second day (r1c1), not the fourth (r3c1)
lv.claim(rows[3]["date"] == "2024-03-14" and rows[2]["date"] == "2024-03-13", "l10 rows[3] is 14 March, rows[2] is 13 March")
E("l10", "screens[0].feedback.byKey.r3c1", "`rows[3]`, the fourth day")
E("l10", "screens[0].feedback.byKey.r3c1", "13 March")
# hint "every value is the text from the file, quotes and all": csv strips the quotes of a quoted field
lv.claim(list(csv.DictReader(['date,close', '2024-03-11,"101.20"']))[0]['close'] == '101.20', "l10 csv strips the quotes, keeps the trailing zero")
E("l10", "screens[1].hints[2].text", "trailing zero and all")
lv.claim(raises(lambda: [r["close"] for r in csv.DictReader("date, close\n2024-03-11, 101.20".splitlines())]) == "KeyError: 'close'", "l10 screens[3] KeyError")
lv.claim([r["close"] for r in csv.DictReader("date, close\n2024-03-11, 101.20".splitlines(), skipinitialspace=True)] == ['101.20'], "l10 skipinitialspace")
lv.claim(max(r["close"] for r in rows) == "99.80" and max(float(r["close"]) for r in rows) == 102.5, "l10 screens[4] text max and float max")
days = ["15/03/2024", "02/04/2024", "28/02/2024"]
lv.claim(sorted(days) == ['02/04/2024', '15/03/2024', '28/02/2024'], "l10 screens[5] text sort")
lv.claim(sorted(days, key=lambda d: datetime.strptime(d, "%d/%m/%Y")) == ['28/02/2024', '15/03/2024', '02/04/2024'], "l10 screens[6] date sort")
vend = [(datetime(2024, 2, 28), 100.00), (datetime(2024, 2, 29), 100.40), (datetime(2024, 3, 1), 102.00), (datetime(2024, 3, 4), 101.60), (datetime(2024, 3, 5), 103.10)]
rets = [round(b[1] / a[1] - 1, 4) for a, b in zip(vend, vend[1:])]
rets2 = [round(float(Fraction(str(b[1])) / Fraction(str(a[1])) - 1), 4) for a, b in zip(vend, vend[1:])]
lv.claim(rets == rets2 == [0.004, 0.0159, -0.0039, 0.0148], "l10 vendor returns two ways")
for v in rets:
    E("l10", "screens[8].feedback.correct", v)
E("l10", "screens[8].widget.tests[2].expect", round(250 / 240 - 1, 4))
lv.claim(len(list(csv.DictReader(("date,close\n" + "d,1\n" * 5 + "\n").splitlines()))) == 5, "l10 quiz[1] five rows, empty line skipped")
E("l10", "quiz[1].widget.answer", 5)
lv.claim(raises(lambda: datetime.strptime("2024-03-15", "%d/%m/%Y")) == "ValueError: time data '2024-03-15' does not match format '%d/%m/%Y'", "l10 quiz[2] message")
lv.claim(sorted(["2024-03-15", "2024-02-28", "2024-04-02"]) == ['2024-02-28', '2024-03-15', '2024-04-02'], "l10 quiz[3] ISO sort")
lv.claim("101.20" * 2 == "101.20101.20", "l10 quiz[0]")

# ---------------- l11 ----------------
lv.claim(raises(lambda: float("n/a")).startswith("ValueError"), "l11 float('n/a') raises ValueError")
ok = []
for p in ["", " 99.80 ", "1,234.50", "100"]:
    try:
        ok.append(float(p))
    except ValueError:
        pass
lv.claim(ok == [99.8, 100.0], "l11 clean keeps 99.8 and 100.0")
lv.claim(raises(lambda: 101.20 / 0.00) == "ZeroDivisionError: float division by zero", "l11 screens[3] message")
lv.claim(int(" 40 ") == 40 and raises(lambda: int("2.5")).startswith("ValueError"), "l11 int strips spaces, refuses 2.5")
lv.claim(raises(lambda: run('def clean(raw):\n    out = []\n    for p in raw:\n        try:\n            out.append(flaot(p))\n        except ValueError:\n            pass\n    return out\nclean(["1"])')) == "NameError: name 'flaot' is not defined", "l11 screens[6] NameError with except ValueError")
lv.claim(raises(lambda: run('def clean(raw):\n    out = []\n    for p in raw:\n        try:\n            out.append(flaot(p))\n        except ValueError:\n            pass\n    return out\nclean(["1"])')) is not None, "l11 screens[6] traceback names line 5")
lv.claim(raises(lambda: int("12.5")) == "ValueError: invalid literal for int() with base 10: '12.5'", "l11 quiz[0] message")
q2 = f"{None} {125.00 / 100.00 - 1}"
lv.claim(q2 == "None 0.25" and float(Fraction("125.00") / Fraction("100.00") - 1) == 0.25, "l11 quiz[2] prints exactly None 0.25 (125.00 / 100.00 - 1 is exact in binary)")
E("l11", "quiz[2].widget.options[0].text", "None 0.25")
E("l11", "quiz[2].widget.options[3].text", "0 0.25")
E("l11", "quiz[2].feedback.correct", 0.25)
E("l11", "quiz[2].explain.text", 0.25)
lv.claim("0.025" not in lv.text("l11", "quiz[2].prose") + lv.text("l11", "quiz[2].explain.text") and "125.00" in lv.text("l11", "quiz[2].prose"), "l11 quiz[2] old inexact pair gone")
E("l11", "screens[8].widget.tests[0].expect", 3)

# ---------------- l12 ----------------
E("l12", "screens[1].widget.options[0].text", 150 * 27.00)
E("l12", "screens[1].widget.options[1].text", round(150 * 26.40, 6))
E("l12", "screens[1].widget.options[2].text", round(150 * (27.00 - 26.40), 6))
E("l12", "screens[1].feedback.correct", 4050)
for call, path in [((150, 26.40, 27.00), "screens[2].widget.tests[3].expect"), ((40, 104.20, 101.50), "screens[2].widget.tests[4].expect"), ((-500, 1.85, 1.80), "screens[2].widget.tests[5].expect")]:
    q, a, p = call
    E("l12", path, q * (p - a))
    lv.claim(abs(q * (p - a) - float(q * (Fraction(str(p)) - Fraction(str(a))))) < 1e-9, f"l12 pnl {call} two ways")
E("l12", "screens[2].feedback.correct", 108)
E("l12", "screens[2].feedback.correct", 25)
E("l12", "screens[7].explain.text", round(40 * (101.50 - 104.20), 6))
cash = -(1000 * 0.72 + (-400) * 0.75)
E("l12", "screens[8].widget.tests[3].expect", round(cash, 2))
E("l12", "screens[8].explain.text", 720)
E("l12", "screens[8].explain.text", 300)
E("l12", "screens[8].widget.tests[5].expect", round(-(40 * 104.20 - 500 * 1.85 + 10 * 101.50), 2))
lv.claim(raises(lambda: run('class Position:\n    def __init__(self, ticker, qty, avg_price):\n        qty = qty\nshel = Position("SHEL", 150, 26.40)\nshel.qty')) == "AttributeError: 'Position' object has no attribute 'qty'", "l12 screens[5] message")
lv.claim(raises(lambda: run('class Position:\n    def __init__(self, qty):\n        self.qty = qty\n    def value(price):\n        return self.qty * price\nPosition(10).value(5.00)')) == "TypeError: Position.value() takes 1 positional argument but 2 were given", "l12 quiz[0] message")
ns, _ = run('class Order:\n    tags = []\n    def __init__(self, tag):\n        self.tags.append(tag)\nfirst = Order("urgent")\nsecond = Order("small")')
lv.claim(ns['first'].tags == ['urgent', 'small'], "l12 quiz[2] shared list")

# ---------------- review-3 ----------------
lv.claim(run('import math\nfrom math import sqrt\nprint(math.sqrt(2.25) == sqrt(2.25))')[1] == "True\n" and math.sqrt(2.25) == 1.5, "review-3 items[0] prints True")
lv.claim(raises(lambda: run('import math\nprint(sqrt(2.25))')) == "NameError: name 'sqrt' is not defined", "review-3 items[0] option c: import math alone leaves sqrt undefined")
lv.claim(raises(lambda: run('from math import sqrt\nprint(math.sqrt(2.25))')) == "NameError: name 'math' is not defined", "review-3 items[0] option b: from-import alone leaves math undefined")
E("review", "items[0].explain.text", 1.5)
# review-3 items[6]: price_of catches only KeyError
def price_of(prices, ticker):
    try:
        return prices[ticker]
    except KeyError:
        return None
pp = {"VOD": 0.72, "AZN": 104.20}
lv.claim(price_of(pp, "AZN") == 104.2 and price_of(pp, "BARC") is None and price_of({}, "VOD") is None, "review-3 items[6] price_of three cases")
lv.claim((raises(lambda: price_of({"VOD": 0.72}, ["VOD"])) or "").startswith("TypeError: unhashable type: 'list'") and raises(lambda: {}.get(["VOD"])) is not None, "review-3 items[6] a list key raises TypeError")
lv.claim("safe_return" not in json.dumps(lv.files["review-3"]["items"][6]), "review-3 items[6] no longer repeats l11 quiz[2]")
# review-3 items[7]: only the clashing names hide a module
lv.claim(lv.text("review", "items[7].widget.options[0].text") == "`read_prices.py`" and "read_prices" not in ("csv", "random"), "review-3 items[7] key read_prices.py clashes with neither csv nor random")
lv.claim(raises(lambda: sum(x for x in ["101.20"])) == "TypeError: unsupported operand type(s) for +: 'int' and 'str'", "review-3 items[1] message")
cl = ['101.20', '99.80', '100.40', '98.75', '102.50']
E("review", "items[3].widget.answer", sum(1 for c in cl if c > "100"))
E("review", "items[3].widget.wrong[0].value", sum(1 for c in cl if float(c) > 100))
E("review", "items[3].explain.text", sum(1 for c in cl if float(c) > 100))
five = [101.20, 102.50, 99.80, 100.40, 103.10]
E("review", "items[5].explain.text", sum(five), fmt="£{:.2f}")
E("review", "items[5].widget.tests[0].expect", round(statistics.mean(five), 2))
lv.claim(round(statistics.mean([0.72, 0.75, 0.74]), 2) == 0.74, "review-3 items[5] test 2")
cost = 100 * 26.00 + 50 * 27.50
E("review", "items[8].explain.text", cost)
E("review", "items[8].widget.tests[1].expect", cost / 150)
avg3 = (40 * 104.20 + 10 * 101.50 + 50 * 100.00) / 100
p, q = 104.20, 40
p, q = (q * p + 10 * 101.50) / (q + 10), q + 10
p, q = (q * p + 50 * 100.00) / (q + 50), q + 50
lv.claim(abs(avg3 - p) < 1e-9 and round(avg3, 2) == 101.83, "review-3 items[8] two buys two ways")

# ---------------- homework-3 ----------------
cs = [100.0, 101.2, 99.8, 100.4, 103.1]
lr5 = [round(math.log(b / a), 6) for a, b in zip(cs, cs[1:])]
lr5b = [round(math.log(b) - math.log(a), 6) for a, b in zip(cs, cs[1:])]
lv.claim(lr5 == lr5b == [0.011929, -0.013931, 0.005994, 0.026537], "homework-3 log returns two ways")
E("homework", "items[0].explain.text", round(math.log(103.1 / 100), 6))
E("homework", "items[0].widget.tests[3].expect", round(sum(lr5), 6))
E("homework", "items[0].feedback.byKey.test-2", round(math.log(2), 6))
lv.claim(datetime.strptime("2024-03-15 16:30", "%Y-%m-%d %H:%M") == datetime(2024, 3, 15, 16, 30), "homework-3 items[1] format")
E("homework", "items[2].explain.text", 1.50 + 2.25)
exact = Fraction(sum(comb(20, k) for k in range(11, 21)), 2 ** 20)
exact2 = Fraction(2 ** 20 - comb(20, 10), 2 ** 21)
lv.claim(exact == exact2, "homework-3 items[5] exact chance two ways")
E("homework", "items[5].prose", round(float(exact), 4))
lv.claim(100 * 1.01 ** 10 * 0.99 ** 10 < 100 < 100 * 1.01 ** 11 * 0.99 ** 9, "homework-3 items[5] 10 ups lose, 11 ups gain")
E("homework", "items[5].explain.text", round(100 * 0.9999 ** 10, 2))


def share_above(paths, days, seed):
    random.seed(seed)
    above = 0
    for _ in range(paths):
        price = 100.0
        for _ in range(days):
            price *= random.choice([0.99, 1.01])
        above += price > 100.0
    return above / paths


for args, path in [((1000, 20, 1), "items[5].widget.tests[0].expect"), ((2000, 20, 7), "items[5].widget.tests[1].expect"), ((1000, 1, 3), "items[5].widget.tests[2].expect")]:
    E("homework", path, share_above(*args))
E("homework", "items[5].feedback.correct", share_above(1000, 20, 1))
# items[7] model: line numbers of the bugs in the prompt's code
code = lv.text("homework", "items[7].prompt").split("```python\n")[1].split("```")[0].split("\n")
line = {k: next(i for i, l in enumerate(code, 1) if k in l) for k in ("history = []", "out.append(Position", "except:", "return max(")}
model = lv.text("homework", "items[7].model")
lv.claim(f"(line {line['history = []']})" in model, f"homework-3 model cites history on line {line['history = []']}")
for k, new in (("out.append(Position", 21), ("except:", 22), ("return max(", 28)):
    lv.claim(line[k] == new and f"(line {new})" in model, f"homework-3 model cites {k!r} on line {new}")
for old in (18, 19, 24):
    lv.claim(f"(line {old})" not in model, f"homework-3 model no longer says line {old}")
lv.claim(raises(lambda: '150' * 27.00) == "TypeError: can't multiply sequence by non-int of type 'float'", "homework-3 model TypeError text")
lv.claim("99.80" > "104.20", "homework-3 model text compare")

# ---------------- every code widget ----------------
CHILD = r'''
import sys, json, io, math, contextlib
spec = json.loads(sys.stdin.read()); src, tests = spec['src'], spec['tests']
def norm(t):
    ls = [l.rstrip() for l in t.split('\n')]
    while ls and not ls[0]: ls.pop(0)
    while ls and not ls[-1]: ls.pop()
    return ls
def close(x, y):
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(close(p, q) for p, q in zip(x, y))
    if isinstance(x, str) and not isinstance(y, str): return False
    try: return math.isclose(float(x), float(y), rel_tol=1e-9, abs_tol=1e-12)
    except Exception: return x == y
def load():
    ns, out = {'__name__': '__main__', '__learner_source__': src}, io.StringIO()
    with contextlib.redirect_stdout(out): exec(compile(src, 'solution.py', 'exec'), ns)
    return ns, out.getvalue()
def one(t, ns):
    if t.get('setup'): exec(t['setup'], ns)
    with contextlib.redirect_stdout(io.StringIO()): a = eval(t['call'], ns)
    e = eval(t['expect'], ns)
    return close(a, e) if t.get('compare') == 'isclose' else a == e
script = any(t.get('compare') == 'stdout' or 'stdin' in t or 'argv' in t for t in tests)
res = []
if not script:
    sys.argv = ['']
    try: ns, _ = load()
    except BaseException: print(json.dumps([False] * len(tests))); sys.exit()
    for t in tests:
        try: res.append(bool(one(t, ns)))
        except BaseException: res.append(False)
else:
    for t in tests:
        sys.argv = ['main.py'] + list(t.get('argv', []))
        try:
            ns, printed = load(); ns['printed'] = printed.splitlines()
            res.append(norm(printed) == norm(t['expect']) if t.get('compare') == 'stdout' else bool(one(t, ns)))
        except BaseException: res.append(False)
print(json.dumps(res))
'''


def play(src, tests):
    with tempfile.TemporaryDirectory() as d:
        p = subprocess.run([sys.executable, '-I', '-c', CHILD], input=json.dumps({'src': src, 'tests': tests}), capture_output=True, text=True, cwd=d, timeout=120)
    try:
        return json.loads(p.stdout.strip().splitlines()[-1])
    except Exception:
        return [False] * len(tests)


def widgets(node, path):
    if isinstance(node, dict):
        if node.get('kind') == 'code' and 'tests' in node:
            yield path, node
        for k, v in node.items():
            yield from widgets(v, f'{path}.{k}' if path else k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from widgets(v, f'{path}[{i}]')


for fid, doc in lv.files.items():
    for path, w in widgets(doc, ''):
        sol, sta = play(w['solution'], w['tests']), play(w['starter'], w['tests'])
        exs = play(w['solution'], w.get('examples', [])) if w.get('examples') else []
        lv.claim(all(sol) and all(exs), f"{fid} {path}: solution passes {sum(sol)}/{len(sol)} tests and every example")
        lv.claim(not all(sta), f"{fid} {path}: starter fails {len(sta) - sum(sta)} of {len(sta)}")

lv.check_wrongs()
lv.report()
