"""first-python level 2 (Control flow): every graded key, wrong[] value and stated number, computed twice.
Second read, session V (docs/reviews/review-first-python-1-3.md). Method 1 runs the loop the screen shows;
method 2 is a closed form or hand arithmetic. Claims are tied to their wording with lv.stated.
Checks that fail on the content as read are review findings (listed in the review's Tool results).
"""
import sys, os, io, math, contextlib
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("first-python", 2)


def run(src):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(src, {})
    return buf.getvalue()


def two(a, b, label):
    ok = a == b or (isinstance(a, (int, float)) and isinstance(b, (int, float)) and abs(a - b) < 1e-9)
    lv.claim(ok, f'two methods agree: {label} ({a!r} vs {b!r})')
    return a


def first_fail(fn, tests):
    """1-based index of the first test the function fails (the engine's test-N key), or None."""
    for i, (args, want) in enumerate(tests):
        got = fn(*args)
        if not (got == want or (isinstance(got, float) and isinstance(want, (int, float)) and math.isclose(got, want))):
            return i + 1
    return None


# ---------- l5-decisions ----------
L = "l5-decisions"
lv.claim(97.40 < 98.00, "97.40 is below the 98.00 stop: sell")
two(run('price = 97.40\nstop = 98.00\nif price < stop:\n    print("sell")\nelse:\n    print("hold")\nprint("done")'), "sell\ndone\n", "flowchart program")
two(run("print(101.25 < 98.00)"), "False\n", "101.25 < 98.00")
lv.claim(not (98.00 < 98.00) and 98.00 <= 98.00, "98.00 is not below itself but is at or below")
lv.claim(not (112.50 < 98.00) and 112.50 > 110.00, "112.50 passes to the second question and takes profit")
two(run('change = 6.5\nif change > 2:\n    print("up")\nelif change > 5:\n    print("big up")\nelse:\n    print("flat or down")'), "up\n", "first True wins")
two(run('qty = 100\nif qty >= 100:\n    print("large")\nelse:\n    print("small")'), "large\n", "quiz >=")
two(run('pnl = -250.00\nif pnl > 0:\n    print("profit")\nelif pnl < -200:\n    print("big loss")\nelif pnl < 0:\n    print("loss")'), "big loss\n", "quiz loss chain")
two(run('pnl = 0\nif pnl > 0:\n    print("profit")\nelif pnl < -200:\n    print("big loss")\nelif pnl < 0:\n    print("loss")'), "", "a P&L of 0 prints nothing")
two(run("stop = 98.00\nprice = 98.00\nprint(price == stop, price < stop)"), "True False\n", "quiz == and <")

# ---------- l6-until-done ----------
L = "l6-until-done"
arrivals, n = [], 0
while True:
    arrivals.append(n)
    if not n < 3:
        break
    n = n + 1
two(arrivals, list(range(4)), "arrivals at line 2 see 0, 1, 2, 3")
for i, v in enumerate(arrivals):
    lv.expect(L, f"screens[0].widget.rows[{i}][1].answer", v)
two(run("n = 0\nwhile n < 3:\n    print(n)\n    n = n + 1"), "0\n1\n2\n", "print inside the loop")
k, ks = 10, [10]
while k > 0:
    k = k - 3
    ks.append(k)
two(k, 10 - 3 * math.ceil(10 / 3), "countdown ends at -2")
lv.expect(L, "screens[2].widget.answer", -2)
two(ks, [10, 7, 4, 1, -2], "countdown values")
balance, years, rows = 100, 0, []
while balance < 150:
    balance, years = balance + 20, years + 1
    rows.append((balance, years))
two(rows, [(100 + 20 * y, y) for y in (1, 2, 3)], "savings pot table")
for i, (b, y) in enumerate(rows):
    lv.expect(L, f"screens[3].widget.rows[{i}][1].answer", b)
    lv.expect(L, f"screens[3].widget.rows[{i}][2].answer", y)
lv.expect(L, "screens[3].explain.text", "3 160")
two(run("n = 1\nwhile n <= 5:\n    print(n)\n    n = n + 1"), "1\n2\n3\n4\n5\n", "1 to 5 with <=")
two(run("n = 1\nwhile n < 6:\n    print(n)\n    n = n + 1"), run("n = 1\nwhile n <= 5:\n    print(n)\n    n = n + 1"), "n < 6 is the same as n <= 5 for whole numbers")
passes = sum(1 for n in range(2, 10, 2))
two(passes, math.ceil((10 - 2) / 2), "passes from 2 in steps of 2 under n < 10")
lv.expect(L, "screens[7].widget.options[0].text", 4)
for start, target, step in [(100, 150, 20), (0, 1000, 250), (0, 1001, 250), (5, 6, 10), (-50, 0, 7)]:
    v, c = start, 0
    while v < target:
        v, c = v + step, c + 1
    two(c, math.ceil((target - start) / step), f"steps_to_reach{(start, target, step)}")
bal, out = 1000.00, []
for _ in range(3):
    bal = bal * 1.07
    out.append(bal)
two([round(x, 2) for x in out], [round(1000 * 1.07 ** y, 2) for y in (1, 2, 3)], "compounding table")
for i, v in enumerate(out):
    lv.expect(L, f"screens[8].widget.rows[{i}][1].answer", round(v, 2))
lv.expect(L, "screens[8].widget.rows[2][1].accept", round(out[2], 3))
gains = [round(out[0] - 1000, 2), round(out[1] - out[0], 2), round(out[2] - out[1], 2)]
two(gains, [70.00, 74.90, 80.14], "yearly gains")
for g in gains:
    lv.expect(L, "screens[8].explain.text", g)
bal, y = 1000.0, 0
while bal < 2000:
    bal, y = bal * 1.07, y + 1
two(y, math.ceil(math.log(2) / math.log(1.07)), "doubling at 7%")
lv.expect(L, "screens[8].explain.text", 11)
lv.expect(L, "screens[8].explain.text", round(1 / 0.07, 1))
for rate, want in [(0.07, 11), (0.10, 8), (0.05, 15), (0.12, 7), (1.0, 1), (0.25, 4)]:
    two(math.ceil(math.log(2) / math.log(1 + rate) - 1e-12), want, f"years_to_double at {rate}")
lv.expect(L, "screens[9].explain.text", round(1.07 ** 10, 3))
lv.expect(L, "screens[9].explain.text", round(1.07 ** 11, 3))
lv.expect(L, "screens[9].explain.text", round(72 / 7, 1))
two(run("cash = 50.00\nwhile cash > 100.00:\n    cash = cash - 10.00\nprint(cash)"), "50.0\n", "quiz zero passes")
two(run("i = 3\nwhile i < 15:\n    print(i)\n    i = i + 4").count("\n"), math.ceil((15 - 3) / 4), "quiz count prints")
lv.expect(L, "quiz[1].widget.wrong[1].value", 15 - 3)
x, p = 10, 0
while x < 1000:
    x, p = x * 2, p + 1
two((x, p), (10 * 2 ** 7, 7), "doubling 10 passes 1000 after seven passes")
lv.expect(L, "quiz[2].widget.options[3].why", 1280)
bal, y, seq = 1000.0, 0, []
while bal < 1500:
    bal, y = bal * 1.1, y + 1
    seq.append(round(bal, 2))
two(y, math.ceil(math.log(1.5) / math.log(1.1)), "years to 1500 at 10%")
for v in seq:
    lv.expect(L, "quiz[3].explain.text", v)

# ---------- l7-for-each ----------
L = "l7-for-each"
pn = [12.50, -4.00, 7.25, 3.00]
tot, steps = 0, []
for p in pn:
    tot += p
    steps.append(tot)
two(steps[-1], sum(pn), "running total 18.75")
for i, v in enumerate(steps):
    lv.expect(L, f"screens[2].steps[{i + 1}].caption", v)
two(sum(range(1, 6)), 5 * 6 // 2, "range(1, 6) total")
lv.expect(L, "screens[3].widget.answer", 15)
lv.expect(L, "screens[3].widget.wrong[0].value", sum(range(1, 7)))
lv.expect(L, "screens[3].widget.wrong[2].value", sum(range(5)))
rets = [0.8, -1.2, 0.0, 2.1, -0.4, 0.3]
two(sum(1 for r in rets if r > 0), len([0.8, 2.1, 0.3]), "up days")
two(run("pnls = [12.50, -4.00, 7.25, 3.00]\nfor p in pnls:\n    total = 0\n    total = total + p\nprint(total)"), "3.0\n", "trap total that forgets")
for n_ in (5, 10, 100):
    two(sum(range(1, n_ + 1)), n_ * (n_ + 1) // 2, f"sum_to({n_})")
two(len(range(1, 13)), 13 - 1, "months")
two(round(sum([310.40, -120.15, -95.25, 42.00, 18.60]), 2), 155.60, "total_pnl test 4")
two(round(sum([-80.00, -45.50, -12.25]), 2), -137.75, "total_pnl test 5")
two(len(range(2, 5)), 5 - 2, "quiz range(2, 5)")
two(run('for day in ["Mon", "Tue", "Wed"]:\n    print("check")\nprint("report")').count("\n"), 3 + 1, "quiz lines")
two(sum(r for r in [1.5, -0.5, 2.0, -1.0] if r < 0), -0.5 + -1.0, "quiz losses")
lv.expect(L, "quiz[2].widget.wrong[0].value", sum([1.5, -0.5, 2.0, -1.0]))
lv.expect(L, "quiz[2].widget.wrong[2].value", 1.5 + 2.0)
# claims
two(len(range(5, 2)), 0, "len(range(5, 2)) is 0, not -3")
lv.expect(L, "screens[7].explain.text", "The count is `b − a` whenever `b` is at least `a`: here 13 − 1 = 12 months.")
up = lambda xs: sum(1 for r in xs if r > 0)
up_ge = lambda xs: sum(1 for r in xs if r >= 0)
tests_up = [(([0.8, -1.2, 0.0, 2.1, -0.4, 0.3],), 3), (([],), 0), (([0.0, 0.0],), 0), (([-0.5, -1.1, -0.2],), 0)]
two(first_fail(up, tests_up), None, "up_days solution passes")
lv.claim(first_fail(up_ge, tests_up) == 1, f"screens[9] byKey test-1 is the first failing test for r >= 0 (it is test-{first_fail(up_ge, tests_up)})")
two(up_ge([0.8, -1.2, 0.0, 2.1, -0.4, 0.3]), 4, "r >= 0 slip returns 4 on test 1")
lv.expect(L, "screens[9].feedback.byKey.test-1", "If test 1 got 4, you counted the 0.0 day.")

# ---------- l8-many-values ----------
L = "l8-many-values"
pr = [101.20, 99.80, 103.50, 102.10, 104.75]
two(pr[2], pr[-3], "prices[2]")
two(run("prices = [101.20, 99.80, 103.50, 102.10, 104.75]\nprint(prices[-1], len(prices))"), "104.75 5\n", "last and len")
two(run("closes = []\ncloses.append(99.80)\ncloses.append(101.25)\ncloses[0] = 100.00\nprint(closes)"), "[100.0, 101.25]\n", "append and replace")
two(max([100.00, 104.00, 101.50, 106.20, 103.00]), 106.20, "peak")
lst, peak, moves = [50.00, 48.00, 52.00, 52.00, 55.00, 51.00], 50.00, []
for i, p in enumerate(lst):
    if p > peak:
        peak = p
        moves.append(i)
two(moves, [2, 4], "the peak moves at c2 and c4")
two(run("pnls = [-120.00, -45.50, -80.00]\nbest = 0\nfor p in pnls:\n    if p > best:\n        best = p\nprint(best)"), "0\n", "best starts at 0")
two(sum([-120.00, -45.50, -80.00]), -245.5, "sum of the losses")
two(max([-120.00, -45.50, -80.00]), -45.5, "best real day")
two(run('returns = [0.4, -0.8, 1.1, -2.6, 0.9, -3.1]\nfor r in returns:\n    if r < -2.0:\n        print("limit hit", r)\n        break\n    print("ok", r)'), "ok 0.4\nok -0.8\nok 1.1\nlimit hit -2.6\n", "break")
two(8 - 1, len(range(8)) - 1, "last index of 8 values")
peaks, pk = [], 100.00
for p in [100.00, 104.00, 101.50, 106.20, 103.00]:
    pk = max(pk, p)
    peaks.append(pk)
gaps = [round(a - b, 2) for a, b in zip(peaks, [100.00, 104.00, 101.50, 106.20, 103.00])]
two(max(gaps), round(106.20 - 103.00, 2), "largest gap 3.20 on the last day")
lv.expect(L, "screens[9].explain.text", 3.20)
lv.claim(gaps.index(max(gaps)) == 4, "the largest gap is on the last day")
x = [4, 8, 15, 16]
two(x[1] + x[-1], 8 + 16, "quiz index sum")
lv.expect(L, "quiz[0].widget.wrong[0].value", x[0] + x[-1])
lv.expect(L, "quiz[0].widget.wrong[1].value", x[1] + x[-2])
c = 0
for p in [3, -1, 4, -5, 9]:
    if p < -2:
        break
    c += 1
two(c, 3, "quiz break count")
two((str(100.00), str(99.80)), ("100.0", "99.8"), "floats print the digits they need, keeping one after the point")
lv.expect(L, "screens[2].explain.text", "keeping one after the point, so 100.00 shows as `100.0`.")

# ---------- review-2 ----------
R = "review"
n, c = 1, 0
while n < 100:
    n, c = n * 3, c + 1
two((c, n), (math.ceil(math.log(100, 3)), 3 ** 5), "triples")
lv.expect(R, "items[1].widget.wrong[1].value", 243)
two(sum(range(3, 7)), 3 + 4 + 5 + 6, "range(3, 7) sum")
two(sum(2 * k + 1 for k in range(4)), 16, "review-2 items[2] total")
two(run("total = 0\nfor k in range(4):\n    total = total + 2 * k + 1\nprint(total)"), "16\n", "review-2 items[2] program prints")
lv.expect(R, "items[2].widget.answer", 16)
lv.expect(R, "items[2].widget.wrong[0].value", sum(2 * k + 1 for k in range(5)))
lv.expect(R, "items[2].widget.wrong[1].value", sum(2 * k + 1 for k in range(1, 5)))
two((sum(2 * k + 1 for k in range(5)), sum(2 * k + 1 for k in range(1, 5))), (25, 24), "review-2 items[2] wrongs")
pn = [40.00, -15.50, 22.00, -8.25]
two(pn[len(pn) - 1], pn[-1], "last P&L")
fixed = run("pnls = [310.50, -120.25, -95.25, 42.00]\ntotal = 0\nfor p in pnls:\n    total = total + p\nprint(total)")
buggy = run("pnls = [310.50, -120.25, -95.25, 42.00]\nfor p in pnls:\n    total = 0\n    total = total + p\nprint(total)")
lv.expect(R, "items[5].explain.text", 137.00)
lv.expect(R, "items[5].explain.text", "310.50 − 120.25 − 95.25 + 42.00 = 137.00")
lv.expect(R, "items[5].prose", "[310.50, -120.25, -95.25, 42.00]")
lv.expect(R, "items[5].prose", "£137.00")
lv.claim(fixed.strip() == "137.0", f"the fixed review program prints {fixed.strip()}")
lv.claim(buggy.strip() == "42.0", f"the buggy review program prints {buggy.strip()}")
big = sum(1 for p in [120.00, -40.00, 0.00, 75.50, -210.00, 15.00] if p > 50 or p < -100)
two(big, 3, "big moves")

# ---------- homework-2 ----------
H = "homework"
bal, y, seq = 1000.0, 0, []
while bal < 1100:
    y, bal = y + 1, bal * 1.02
    seq.append(round(bal, 2))
two(y, math.ceil(math.log(1.1) / math.log(1.02)), "years to 1100 at 2%")
for v in seq:
    lv.expect(H, "items[1].explain.text", v)
for b, r_, t, want in [(1000.00, 0.05, 1500.00, 9), (100.00, 0.50, 1000.00, 6), (5000.00, 0.04, 10000.00, 18)]:
    two(math.ceil(math.log(t / b) / math.log(1 + r_)), want, f"years_to_target{(b, r_, t)}")


def fb_total(pnls, limit):
    total, cnt = 0, 0
    for p in pnls:
        total, cnt = total + p, cnt + 1
        if total <= -limit:
            return cnt
    return None


def fb_day(pnls, limit):
    cnt = 0
    for p in pnls:
        cnt += 1
        if p <= -limit:
            return cnt
    return None


tests_fb = [(([-100.00, 50.00, -300.00, -200.00], 300.00), 3), (([], 100.00), None), (([-500.00], 500.00), 1),
            (([100.00, -150.00, -40.00], 100.00), None), (([20.00, -30.00, -10.00, -5.00, 40.00, -60.00], 40.00), 6),
            (([-50.00, -60.00, 200.00, -400.00], 100.00), 2)]
two(first_fail(fb_total, tests_fb), None, "first_breach solution passes")
lv.claim(first_fail(fb_day, tests_fb) == 4, f"items[3] byKey test-4 is the first failing test when the day is compared (it is test-{first_fail(fb_day, tests_fb)})")
lv.expect(H, "items[3].feedback.byKey.test-4", -150.00)
lv.expect(H, "items[3].feedback.byKey.test-4", 100.00 - 150.00)
_bk = lv._file(H)[1]["items"][3]["feedback"]["byKey"]
lv.claim(list(_bk) == ["test-4"], f"items[3] byKey keys are {list(_bk)}")

# homework-2 items[0] (decide) and items[4] (largest_fall)
def decide(price, stop, target):
    return "sell" if price < stop else ("take profit" if price > target else "hold")


for args, want in [((48.90, 50.00, 56.00), "sell"), ((57.25, 50.00, 56.00), "take profit"), ((52.10, 50.00, 56.00), "hold"),
                   ((50.00, 50.00, 56.00), "hold"), ((56.00, 50.00, 56.00), "hold"), ((0.95, 1.00, 1.20), "sell")]:
    two(decide(*args), want, f"decide{args}")
two(round(106.20 - 103.00, 2), 3.20, "largest fall example")
lv.expect(H, "items[4].title", "Largest fall")
lv.expect(H, "items[4].question", "largest_fall")
lv.claim("max_drawdown" not in lv.text(H, "items[4]"), "items[4] no longer uses the name max_drawdown")


def mdd(ps):
    w, pk = 0, ps[0] if ps else 0
    for p in ps:
        pk = max(pk, p)
        w = max(w, pk - p)
    return w


two(round(mdd([100.00, 104.00, 101.50, 106.20, 103.00]), 2), round(106.20 - 103.00, 2), "drawdown in pounds 3.20")
two(mdd([100.00, 90.00, 95.00, 80.00, 120.00, 110.00]), 100.00 - 80.00, "drawdown 20")
two(mdd([120.00, 100.00, 130.00, 95.00, 125.00]), 130.00 - 95.00, "drawdown 35")
run_, best = 0, 0
runs = []
for r in [0.5, 1.2, -0.3, 0.8, 0.1, 0.9, 0.0, 1.5]:
    run_ = run_ + 1 if r > 0 else 0
    best = max(best, run_)
    runs.append(run_)
two(best, 3, "longest up streak")
two(runs, [1, 2, 0, 1, 2, 3, 0, 1], "run trace")
lv.expect(H, "items[5].widget.wrong[0].value", 5)
two(sum(1 for r in [0.5, 1.2, -0.3, 0.8, 0.1, 0.9, 0.0, 1.5] if r > 0), 6, "every up day")
asw = run("pnls = [-35.00, 120.50, 0.00, -80.25, 64.75]\nbest = 0\nwinners = 0\ni = 1\nwhile i < len(pnls):\n    total = 0\n    p = pnls[i]\n    total = total + p\n    if p > best:\n        best = p\n    if p >= 0:\n        winners = winners + 1\n    i = i + 1\nprint(total, best, winners)")
two(asw, "64.75 120.5 3\n", "longform as written")
two(round(sum([-35.00, 120.50, 0.00, -80.25, 64.75]), 2), 70.00, "longform corrected total")
lv.expect(H, "items[8].model", "70.0 120.5 2")

lv.check_wrongs()
lv.report()
