"""Second read, py-found level 4 (l13 to l16, review-4, homework-4): recompute every stated number, two ways where a
second method exists, check it appears where it is stated (app/tools/numbers_lib.py), check code-behaviour claims in
CPython, and run every code widget (solution passes every hidden test, starter fails at least one).
Run: python3 docs/reports/py-found-L4-numbers.py   (exits 0 on correct content)
Checks that fail on the content as read (review-py-found-3-4.md findings): l13 quiz[3] "next works only on a generator",
l14 quiz[0] two options showing one list, l15 screens[9] an empty test passes, l16 screens[5] explain canvas "yes",
review-4 items[1] text-comparison why.
"""
import contextlib, csv, io, json, math, os, statistics, subprocess, sys, tempfile
from datetime import datetime, date
from fractions import Fraction
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("py-found", 4)
E = lv.expect
S252 = math.sqrt(252)


def raises(fn):
    try:
        fn()
    except Exception as e:
        return type(e).__name__ + ': ' + str(e)
    return None


def dd(prices):
    peak = prices[0]
    for p in prices:
        peak = max(peak, p)
        yield (peak - p) / peak


def mdd_brute(prices):   # method 2: every peak-before-trough pair
    return max([0.0] + [(prices[i] - prices[j]) / prices[i] for i in range(len(prices)) for j in range(i, len(prices))
                        if prices[i] == max(prices[:i + 1])])


# ---------------- l13 ----------------
ten = [100.0, 96.0, 92.0, 97.0, 110.0, 104.5, 99.0, 103.0, 108.0, 112.0]
d = list(dd(ten))
lv.claim(max(d) == mdd_brute(ten) == 0.1 and d.index(max(d)) == 6, "l13 deepest fall ends on day 7, 10%, two ways")
E("l13", "screens[0].hints[2].text", round(d[2] * 100))
E("l13", "screens[0].hints[2].text", round(d[6] * 100))
E("l13", "screens[0].feedback.byKey.d6", round(d[5] * 100))
E("l13", "screens[0].feedback.byKey.d2", round(d[1] * 100))
lv.claim(min(ten) == 92.0 and ten.index(92.0) == 2, "l13 day 3 is the lowest close")
highs = [i + 1 for i in range(1, 10) if ten[i] > max(ten[:i])]
rises = [i + 1 for i in range(1, 10) if ten[i] > ten[i - 1]]
lv.claim(highs == [5, 10], "l13 new highs on days 5 and 10")
lv.claim(['d%d' % i for i in rises] == lv.files['l13-one-at-a-time']['screens'][1]['widget']['wrong'][0]['set'], "l13 'rises' wrong set = every rising day")


def running_peak(prices):
    peak = prices[0]
    for p in prices:
        peak = max(peak, p)
        yield peak


g = running_peak([100.0, 96.0, 110.0, 104.5])
lv.claim([next(g), next(g), next(g)] == [100.0, 100.0, 110.0], "l13 screens[3] three nexts")
lv.claim([round(x, 4) for x in dd([100.0, 96.0, 92.0, 97.0, 110.0, 104.5, 99.0])] == [0.0, 0.04, 0.08, 0.03, 0.0, 0.05, 0.1], "l13 screens[5] drawdowns")
E("l13", "screens[5].feedback.byKey.test-1", round(11 / 99, 4))
gen = dd(ten)
lv.claim((max(gen), list(gen)) == (0.1, []), "l13 screens[6] spent generator")
E("l13", "screens[7].widget.options[1].why", round((max(ten) - min(ten)) / max(ten) * 100, 1))
fund = [250.0, 253.75, 249.1, 256.4, 261.25, 255.0, 247.4, 243.15, 250.6, 258.8, 263.5, 259.9]
m = max(dd(fund))
lv.claim(abs(m - mdd_brute(fund)) < 1e-15 and abs(m - (261.25 - 243.15) / 261.25) < 1e-15, "l13 fund MDD two ways")
E("l13", "screens[8].widget.tests[0].expect", m)
E("l13", "screens[8].feedback.correct", round(m * 100, 2))
E("l13", "screens[8].explain.text", round(261.25 - 243.15, 2), fmt="{:.2f}")
E("l13", "screens[8].feedback.byKey.test-1", round((max(fund) - min(fund)) / max(fund), 4))
E("l13", "screens[8].feedback.byKey.test-1", round(m, 4))
lv.claim(fund.index(max(fund)) > fund.index(min(fund)), "l13 the 263.50 high comes after the 243.15 low")
lv.claim(max(dd([50.0, 40.0, 60.0, 45.0])) == mdd_brute([50.0, 40.0, 60.0, 45.0]) == 0.25, "l13 quiz[0] 0.25 two ways")
E("l13", "quiz[0].widget.wrong[0].value", round((60 - 40) / 60, 4))
E("l13", "quiz[0].widget.wrong[1].value", 0.2)
E("l13", "quiz[0].widget.wrong[2].value", (60 - 45) / 100)
g2 = running_peak([3.0, 5.0]); next(g2); next(g2)
lv.claim(raises(lambda: next(g2)) == "StopIteration: ", "l13 quiz[1] StopIteration")
E("l13", "quiz[2].widget.options[1].text", round(101.30 / 100.00 - 1, 3))
lv.claim(max(dd([100.0, 100.4, 100.9, 101.3])) == 0.0, "l13 quiz[2] rising fund")
# quiz[3] why: "`next` works only on a generator" -- next works on any iterator
lv.stated("l13", "quiz[3].widget.options[2].why", "`next` works only on a generator", raises(lambda: next(iter([1.0]))) is not None)

# ---------------- l14 ----------------
lv.claim(sorted(["30/03/2026", "02/04/2026", "27/03/2026"]) == ['02/04/2026', '27/03/2026', '30/03/2026'], "l14 screens[1] text sort")
to_date = lambda t: datetime.strptime(t, "%d/%m/%Y").date()
lv.claim(to_date("05/11/2025") == date(2025, 11, 5) and datetime.strptime("05/11/2025", "%m/%d/%Y").date() == date(2025, 5, 11), "l14 05/11 either way round")
lv.claim(max(["101.20", "103.10", "100.00", "99.80", "102.50"]) == "99.80", "l14 screens[4] text max")
c5 = [100.00, 101.20, 102.50, 99.80, 103.10]
r5 = [round(b / a - 1, 6) for a, b in zip(c5, c5[1:])]
r5b = [round(float(Fraction(str(b)) / Fraction(str(a)) - 1), 6) for a, b in zip(c5, c5[1:])]
lv.claim(r5 == r5b == [0.012, 0.012846, -0.026341, 0.033066], "l14 screens[5] returns two ways")
E("l14", "screens[5].feedback.byKey.test-1", round(100.00 / 101.20 - 1, 6))
days = [("30/03", 0.012), ("31/03", 0.0128), ("01/04", -0.0263), ("02/04", 0.0331)]
lv.claim([dd_ for dd_, _ in sorted(days, key=lambda x: x[1])[:2]] == ['01/04', '30/03'] and [x for x, _ in sorted(days)[:2]] == ['01/04', '02/04'], "l14 screens[6] worst two, and by text")
lv.claim(raises(lambda: -date(2026, 1, 1)).startswith("TypeError"), "l14 screens[7] a date cannot be negated")
share = {"05/02/2026": 412.60, "04/02/2026": 405.30, "03/02/2026": 409.85, "02/02/2026": 401.20, "30/01/2026": 398.75, "29/01/2026": 404.10, "28/01/2026": 400.00}
cl = [share[k] for k in sorted(share, key=to_date)]
r6 = [round(b / a - 1, 6) for a, b in zip(cl, cl[1:])]
lv.claim(r6 == [round(float(Fraction(str(b)) / Fraction(str(a)) - 1), 6) for a, b in zip(cl, cl[1:])] == [0.01025, -0.013239, 0.006144, 0.02156, -0.011102, 0.018011], "l14 screens[8] returns two ways")
lv.claim(sorted(["9.50", "10.25", "100.00"]) == ['10.25', '100.00', '9.50'], "l14 quiz[0] text sort")
q0 = lv.files['l14-sorting-by-what-matters']['quiz'][0]['widget']['options']
shown = [o['text'].split('`')[1] for o in q0]
lv.claim(len(set(shown)) == len(shown), "l14 quiz[0] every option shows a different list", f"options show {shown}")
E("l14", "quiz[1].widget.answer", 245 / 250 - 1)
E("l14", "quiz[1].widget.wrong[1].value", round(-5 / 245, 4))
E("l14", "quiz[1].widget.wrong[2].value", -5 / 100)
lv.claim(sorted(["2025-12-31", "2026-01-02"]) == ["2025-12-31", "2026-01-02"] and sorted(["12/31/2025", "01/02/2026"])[0] == "01/02/2026", "l14 quiz[2] ISO safe, US breaks across a year")

# ---------------- l15 ----------------
lv.claim(sum([0.1, 0.2]) / 2 == 0.15000000000000002, "l15 screens[1] mean([0.1, 0.2])")
r = [0.01, -0.02, 0.015, 0.005, -0.01]
sq = sum(x * x for x in r)            # the mean is 0
lv.claim(abs(sq - float(sum(Fraction(str(x)) ** 2 for x in r))) < 1e-18, "l15 squared distances two ways")
E("l15", "screens[2].explain.text", round(sq, 5))
E("l15", "screens[2].explain.text", round(sq / 5, 5))
E("l15", "screens[2].widget.tests[1].expect", statistics.pstdev(r))
lv.claim(abs(statistics.pstdev(r) - math.sqrt(sq / 5)) < 1e-15, "l15 sd two ways")
E("l15", "screens[2].feedback.byKey.test-2", round(sum(abs(x) for x in r) / 5, 3))
E("l15", "screens[3].canvas.params.rows[1][2]", round(statistics.stdev(r), 6))
E("l15", "screens[3].hints[1].text", round(statistics.stdev(r) / statistics.pstdev(r), 3))
lv.claim(abs(statistics.stdev(r) / statistics.pstdev(r) - math.sqrt(5 / 4)) < 1e-12, "l15 ratio is sqrt(5/4)")
E("l15", "screens[3].feedback.byKey.float", round(statistics.stdev(r) - statistics.pstdev(r), 4))
lv.claim(statistics.pstdev([0.012]) == 0.0 and raises(lambda: statistics.stdev([0.012])) == "StatisticsError: stdev requires at least two data points", "l15 screens[4]")
lv.claim(365 - 104 - 9 == 252 and round(S252, 2) == 15.87, "l15 252 days and sqrt(252)")
E("l15", "screens[6].widget.answer", round(0.012 * S252, 4))
E("l15", "screens[6].widget.wrong[0].value", 0.012 * 252)
E("l15", "screens[6].widget.wrong[1].value", round(0.012 * math.sqrt(365), 4))
E("l15", "screens[6].widget.wrong[2].value", round(math.sqrt(1.2) / 100, 3))
v = math.sqrt(0.0002 * 252)
lv.claim(abs(statistics.stdev([0.01, -0.01]) * S252 - v) < 1e-15, "l15 hand value two ways")
for x in (v, statistics.pstdev([0.01, -0.01]) * S252, statistics.stdev([0.01, -0.01]) * 252, statistics.stdev([0.01, -0.01]) * math.sqrt(365)):
    E("l15", "screens[7].explain.text", round(x, 4) if x < 1 else round(x, 3))
E("l15", "screens[9].widget.tests[0].expect", statistics.stdev(r) * S252)
E("l15", "screens[9].feedback.byKey.test-1", round(statistics.pstdev(r) * S252, 4), fmt="{:.4f}")
E("l15", "screens[9].feedback.byKey.test-1", round(statistics.stdev(r) * 252, 2))
six = [0.01025, -0.013239, 0.006144, 0.02156, -0.011102, 0.018011]
E("l15", "screens[9].widget.tests[2].expect", statistics.stdev(six) * S252)
E("l15", "screens[9].feedback.correct", round(statistics.stdev(six) * S252 * 100, 2))
E("l15", "screens[9].explain.text", round(statistics.stdev(six), 4))
lv.claim(six == r6, "l15 screens[9] uses l14's six returns")
E("l15", "quiz[0].explain.text", round(math.sqrt(20 / 19), 3))
E("l15", "quiz[1].widget.answer", round(0.008 * S252, 3))
E("l15", "quiz[1].widget.wrong[1].value", round(0.008 * math.sqrt(365), 4))
lv.claim(f"{sum(r):.1e}" == "-8.7e-19", "l15 quiz[2] sum is about -8.7e-19 (Python 3.12+ sum)")
lv.claim(statistics.stdev([0.004, 0.004]) * S252 < 1e-12, "l15 quiz[3] edge test")
# screens[9]: a learner who leaves test_annualised_vol() empty still passes all five hidden tests
w9 = lv.files['l15-checking-your-code']['screens'][9]['widget']
lazy = w9['solution'].replace("    assert math.isclose(annualised_vol([0.01, -0.01]), math.sqrt(0.0002 * 252))\n    assert math.isclose(annualised_vol([0.002, 0.002]), 0.0, abs_tol=1e-12)\n", "    pass\n")

# ---------------- l16 ----------------
fmt = lambda label, value: f"{label:<14}{value:>8.2%}"
for t in lv.files['l16-returns-from-a-file']['screens'][6]['widget']['tests'][:3]:     # each row, from its own call
    lv.claim(eval(t['call'], {'format_row': fmt}) == eval(t['expect']), f"l16 screens[6] {t['call']} = {t['expect']}")
lv.claim(len(fmt('Return', 0.1)) == 22 == 14 + 8, "l16 rows are 22 characters")
feb = {"13/02/2026": 187.25, "12/02/2026": 184.05, "11/02/2026": 185.60, "10/02/2026": 181.10, "09/02/2026": 183.35, "06/02/2026": 178.90, "05/02/2026": 176.20, "04/02/2026": 179.45, "03/02/2026": 182.70, "02/02/2026": 180.00}
fc = [feb[k] for k in sorted(feb, key=to_date)]
lv.claim(fc == lv.files['l16-returns-from-a-file']['screens'][9]['canvas']['params']['series'][0]['values'], "l16 canvas = sorted closes")
tr, vol, md = fc[-1] / fc[0] - 1, statistics.stdev([b / a - 1 for a, b in zip(fc, fc[1:])]) * S252, max(dd(fc))
lv.claim(abs(md - mdd_brute(fc)) < 1e-15 and abs(md - (182.70 - 176.20) / 182.70) < 1e-15, "l16 MDD two ways")
E("l16", "screens[9].widget.tests[1].expect", tr)
E("l16", "screens[9].widget.tests[2].expect", vol)
E("l16", "screens[9].widget.tests[3].expect", md)
for x in (tr, vol, md):
    E("l16", "screens[9].feedback.correct", round(x * 100, 2))
    E("l16", "screens[9].widget.tests[6].expect", f"{x:.2%}")
E("l16", "screens[9].widget.tests[5].expect", 95.0 / 100.0 - 1)
E("l16", "quiz[1].widget.options[3].text", 104.0 / 100.0 - 1)
lv.claim(f"[{-0.0532:>8.2%}]" == "[  -5.32%]", "l16 quiz[2]")
E("l16", "quiz[3].widget.answer", round(1.10 * 0.90 - 1, 6))
# screens[5]: the import stops at `path = sys.argv[1]`, so print_summary(path) never runs; the explain canvas marks it "yes"
lv.stated("l16", "screens[5].explain.canvas.values.r2c1", "yes", False)

# ---------------- review-4 ----------------
g3 = running_peak([5.0, 3.0, 8.0]); next(g3)
lv.claim(list(g3) == [5.0, 8.0], "review-4 items[0]")
tab = [{"Date": "2026-03-02", "Close": "98.40"}, {"Date": "2026-03-03", "Close": "101.75"}, {"Date": "2026-03-04", "Close": "99.90"}]
lv.claim(max(tab, key=lambda x: float(x["Close"]))["Date"] == "2026-03-03", "review-4 items[1] key")
lv.stated("review", "items[1].widget.options[1].why", "comparing the closes as text", max(tab, key=lambda x: x["Close"])["Date"] == "2026-03-02")
pv = [200, 220, 187, 230, 207]
lv.claim(max(dd(pv)) == mdd_brute(pv) == 0.15, "review-4 items[2] two ways")
E("review", "items[2].widget.wrong[0].value", round((230 - 187) / 230, 3))
E("review", "items[2].widget.wrong[1].value", (230 - 207) / 230)
E("review", "items[2].widget.wrong[2].value", (220 - 187) / 100)
lv.claim("260" + "0" == "2600", "review-4 items[3]")
import re
two = [float(x) / 100 for x in re.findall(r'(-?\d+(?:\.\d+)?)%', lv.text("review", "items[4].prose"))]   # the two returns, from the prose
lv.claim(len(two) == 2 and abs(statistics.stdev(two) - abs(two[0] - two[1]) / math.sqrt(2)) < 1e-15, f"review-4 items[4] stdev of {two} two ways")
E("review", "items[4].widget.answer", round(statistics.stdev(two) * S252, 4))
E("review", "items[4].widget.wrong[0].value", round(statistics.pstdev(two) * S252, 4))
E("review", "items[4].widget.wrong[1].value", round(statistics.stdev(two), 4))
E("review", "items[4].widget.wrong[2].value", round(statistics.stdev(two) * 252, 3))
lv.claim(sorted(["05/01/2026", "31/12/2025", "02/01/2026"], key=to_date)[0] == "31/12/2025" and sorted(["05/01/2026", "31/12/2025", "02/01/2026"])[0] == "02/01/2026", "review-4 items[5]")
tot = 1.05 * 0.95 * 1.05
lv.claim(abs(tot - float(Fraction(105, 100) * Fraction(95, 100) * Fraction(105, 100))) < 1e-15, "review-4 items[8] two ways")
E("review", "items[8].explain.text", round(tot, 6))
E("review", "items[8].widget.answer", round(tot - 1, 4))
E("review", "items[8].feedback.correct", round(100 * tot, 2))

# ---------------- homework-4 ----------------
p5 = [100.0, 104.0, 98.8, 101.0, 97.76]
lv.claim(abs(max(dd(p5)) - 0.06) < 1e-12 and abs(mdd_brute(p5) - 0.06) < 1e-12, "homework-4 items[0] depth two ways")
sh = sorted(((k, share[k] / share[j] - 1) for j, k in zip(sorted(share, key=to_date), sorted(share, key=to_date)[1:])), key=lambda x: x[1])
lv.claim([k for k, _ in sh[:2]] == ['30/01/2026', '04/02/2026'], "homework-4 items[1] worst two")
E("homework", "items[1].explain.text", round(sh[0][1] * 100, 2))
E("homework", "items[1].explain.text", round(sh[1][1] * 100, 2))
E("homework", "items[3].widget.answer", round(0.025 * math.sqrt(52), 4))
E("homework", "items[3].widget.wrong[0].value", round(0.025 * S252, 4))
E("homework", "items[3].widget.wrong[1].value", 0.025 * 52)
E("homework", "items[3].explain.text", round(math.sqrt(52), 2))
E("homework", "items[4].explain.text", round(math.sqrt(1000 / 999), 4))
E("homework", "items[4].explain.text", round(0.012 * math.sqrt(1000 / 999), 6))
E("homework", "items[4].widget.options[1].text", round(0.012 * math.sqrt(5 / 4), 4))
lv.claim(all(math.sqrt(n / (n - 1)) <= math.sqrt(2) for n in range(2, 2000)), "homework-4 items[4] factor is at most sqrt(2) for every n >= 2")
wk = {"13/02/2026": 105.60, "06/02/2026": 101.20, "30/01/2026": 103.80, "23/01/2026": 99.10, "16/01/2026": 102.40, "09/01/2026": 100.00}
wc = [wk[k] for k in sorted(wk, key=to_date)]
for x in (wc[-1] / wc[0] - 1, statistics.stdev([b / a - 1 for a, b in zip(wc, wc[1:])]) * math.sqrt(52), max(dd(wc))):
    E("homework", "items[5].widget.tests[3].expect", f"{x:.2%}")
lv.claim(abs(max(dd(wc)) - mdd_brute(wc)) < 1e-15, "homework-4 weekly MDD two ways")
E("homework", "items[6].widget.model", round(0.0163 * 252 * 100))
E("homework", "items[6].widget.model", round(0.0163 * 15.87 * 100, 1))
E("homework", "items[6].widget.model", round(statistics.stdev([0.01, -0.01]) * 252, 2))

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
    with tempfile.TemporaryDirectory() as d_:
        p = subprocess.run([sys.executable, '-I', '-c', CHILD], input=json.dumps({'src': src, 'tests': tests}), capture_output=True, text=True, cwd=d_, timeout=120)
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
lv.claim(lazy != w9['solution'] and not all(play(lazy, w9['tests'])), "l15 screens[9]: an empty test_annualised_vol() fails at least one hidden test",
         "a solution whose test body is `pass` passes every hidden test")

lv.check_wrongs()
lv.report()
