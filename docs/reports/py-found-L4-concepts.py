"""Concept audit, py-found level 4 (l13 to l16, review-4, homework-4).

Checks every code-behaviour claim by running it under CPython 3 (stdlib only; pytest is used when installed).
Run: python3 docs/reports/py-found-L4-concepts.py   (exits 0 on correct content)

A check named `FINDING n` fails because the content is wrong or imprecise as read on 12 Nov 2026; n is the
finding number in docs/reviews/audit-py-found-4.md. Those checks read the content strings, so they pass once
the fix is applied. Version notes: the learner runtime is Pyodide 0.27.7 (CPython 3.12.7, pytest 8.1.1).
Two claims depend on the version and are checked for it: the `stdev` error message (3.11 and later) and the
float sum of the five returns (`sum` is compensated from 3.12).
"""
import contextlib, csv, io, json, math, os, random, re, statistics, subprocess, sys, tempfile
from datetime import datetime, date

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'py-found')
FILES = {k: json.load(open(os.path.join(BASE, v + '.json'), encoding='utf-8')) for k, v in {
    'l13': 'l13-one-at-a-time', 'l14': 'l14-sorting-by-what-matters', 'l15': 'l15-checking-your-code',
    'l16': 'l16-returns-from-a-file', 'r4': 'review-4', 'h4': 'homework-4'}.items()}

fails, passed = [], 0


def check(name, cond, detail=''):
    global passed
    if cond:
        passed += 1
    else:
        fails.append(name + (': ' + str(detail) if detail != '' else ''))


def get(f, path):
    o = FILES[f]
    for part in re.findall(r'[^.\[\]]+', path):
        o = o[int(part)] if isinstance(o, list) else o[part]
    return o


def strings(f):
    out = []

    def walk(o, p):
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, p + '.' + k if p else k)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, '%s[%d]' % (p, i))
        elif isinstance(o, str):
            out.append((p, o))
    walk(FILES[f], '')
    return out


def raises(fn):
    try:
        fn()
    except BaseException as e:
        return type(e).__name__
    return None


def run(code, argv=None):
    """Run code as a script; return (stdout, namespace, exception name or None)."""
    ns = {'__name__': '__main__'}
    buf, err = io.StringIO(), None
    old = sys.argv
    if argv is not None:
        sys.argv = argv
    cwd = os.getcwd()
    os.chdir(TMP)
    try:
        with contextlib.redirect_stdout(buf):
            try:
                exec(compile(code, '<content>', 'exec'), ns)
            except BaseException as e:
                err = type(e).__name__
    finally:
        sys.argv = old
        os.chdir(cwd)
    return buf.getvalue(), ns, err


def options(f, path):
    w = get(f, path)
    return {o['id']: o for o in w['options']}


def right_id(f, path):
    return [o['id'] for o in get(f, path)['options'] if o.get('correct')]


TMP = tempfile.mkdtemp(prefix='pf4-')
TEN = [100.0, 96.0, 92.0, 97.0, 110.0, 104.5, 99.0, 103.0, 108.0, 112.0]
S252 = math.sqrt(252)

# ---------------------------------------------------------------- l13 generators and drawdown


def running_peak(prices):
    peak = prices[0]
    for p in prices:
        peak = max(peak, p)
        yield peak


def drawdowns(prices):
    peak = prices[0]
    for p in prices:
        peak = max(peak, p)
        yield (peak - p) / peak


dd = list(drawdowns(TEN))
check('l13 s0 key: day 7 ends the deepest fall', max(range(10), key=lambda i: dd[i]) == 6 and get('l13', 'screens[0].widget.answer') == ['d7'])
check('l13 s0 falls: d2 4%, d3 8%, d6 5%, d7 10%', [round(dd[i], 6) for i in (1, 2, 5, 6)] == [0.04, 0.08, 0.05, 0.1])
check('l13 s0 lowest close is day 3, not the deepest fall', TEN.index(min(TEN)) == 2 and dd[2] < dd[6])
highs = ['d%d' % (i + 1) for i in range(1, 10) if TEN[i] > max(TEN[:i])]
check('l13 s1 new highs after day 1', highs == get('l13', 'screens[1].widget.answer'))
rises = ['d%d' % (i + 1) for i in range(1, 10) if TEN[i] > TEN[i - 1]]
check('l13 s1 wrong set "rises" is every rise and is not the key', rises == get('l13', 'screens[1].widget.wrong[0].set') and rises != highs)

g = running_peak([100.0, 96.0, 110.0, 104.5])
check('l13 s3 calling a generator function runs nothing (lazy)', type(g).__name__ == 'generator')
ran = []


def lazy(xs):
    ran.append('start')
    for x in xs:
        yield x


lz = lazy([1, 2])
check('l13 s3 laziness: body has not started after the call', ran == [])
next(lz)
check('l13 s3 laziness: body starts on first next', ran == ['start'])
check('l13 s3 laziness: an empty-list call raises only on first next',
      raises(lambda: running_peak([])) is None and raises(lambda: next(running_peak([]))) == 'IndexError')
got = [next(g), next(g), next(g)]
check('l13 s3 key 100.0, 100.0, 110.0', got == [100.0, 100.0, 110.0] and right_id('l13', 'screens[3].widget') == ['right'])
check('l13 s3 wrong options really wrong', got != [100.0, 96.0, 110.0] and got != [110.0] * 3 and got != [[100.0, 100.0, 110.0, 110.0]])
check('l13 s3 option "list" shows the full list of peaks', list(running_peak([100.0, 96.0, 110.0, 104.5])) == [100.0, 100.0, 110.0, 110.0])
check('l13 s4 list and for both drain a generator', list(running_peak(TEN[:5])) == [p for p in running_peak(TEN[:5])] == [100.0] * 4 + [110.0])


def yield_p(prices):
    peak = prices[0]
    for p in prices:
        peak = max(peak, p)
        yield p


def yield_before(prices):
    peak = prices[0]
    for p in prices:
        yield peak
        peak = max(peak, p)


check('l13 s4 feedback: yielding p gives the closes back', list(yield_p(TEN[:5])) == TEN[:5])
check('l13 s4 feedback: yield before update is one step behind', list(yield_before(TEN[:5])) == [100.0] * 5)
check('l13 s4 feedback test-5: a returned list is not a generator', type([1.0]).__name__ != 'generator')
check('l13 s5 day 7 gives exactly 0.1', dd[6] == 0.1)
check('l13 s5 feedback: 11.0 pounds; 0.1111 by the close', 110.0 - 99.0 == 11.0 and round(11 / 99, 4) == 0.1111)
check('l13 s5 rising prices give zero drawdowns', list(drawdowns([100.0, 101.0, 103.0])) == [0.0] * 3)
d = drawdowns(TEN)
first, second = max(d), list(d)
check('l13 s6 trap: prints 0.1 then []', repr(first) == '0.1' and second == [] and right_id('l13', 'screens[6].widget') == ['right'])
check('l13 s6 wrong options really wrong: no replay, no error, not [0.0]', second != dd and second != [0.0])
check('l13 s6 exhaustion: a spent generator stays spent', list(d) == [] and raises(lambda: next(d)) == 'StopIteration')
check('l13 s6 explain: a fresh call or a kept list gives the values twice', list(drawdowns(TEN)) == dd and max(dd) == 0.1)
check('l13 s7 key max(drawdowns(prices)) is 0.1', max(drawdowns(TEN)) == 0.1)
check('l13 s7 hilo is 17.9% and wrong', round((max(TEN) - min(TEN)) / max(TEN), 3) == 0.179 and TEN.index(92.0) < TEN.index(112.0))
check('l13 s7 last-day option gives 0', list(drawdowns(TEN))[-1] == 0.0)
check('l13 s7 indexing a generator raises TypeError', raises(lambda: drawdowns(TEN)[6]) == 'TypeError')
MAR = [250.0, 253.75, 249.1, 256.4, 261.25, 255.0, 247.4, 243.15, 250.6, 258.8, 263.5, 259.9]
check('l13 s8 max drawdown 6.93% from 261.25 to 243.15', math.isclose(max(drawdowns(MAR)), 18.10 / 261.25) and round(max(drawdowns(MAR)), 4) == 0.0693)
check('l13 s8 hilo 0.0772 and the high comes after the low', round((263.5 - 243.15) / 263.5, 4) == 0.0772 and MAR.index(263.5) > MAR.index(243.15))
check('l13 s8 trough three trading days after the peak', MAR.index(243.15) - MAR.index(261.25) == 3)
out, ns, err = run(get('l13', 'screens[8].widget.solution'))
check('l13 s8 solution prints 6.93%', out.strip() == 'Max drawdown: 6.93%' and err is None, out)
check('l13 s8 io.StringIO and splitlines both feed DictReader',
      list(csv.DictReader(io.StringIO('a,b\n1,2\n'))) == list(csv.DictReader('a,b\n1,2\n'.splitlines())))
check('l13 memory: a generator object does not grow with its input',
      sys.getsizeof(drawdowns(list(range(1, 100001)))) == sys.getsizeof(drawdowns([1.0])) < sys.getsizeof(list(range(1, 100001))))
q = [50.0, 40.0, 60.0, 45.0]
check('l13 quiz0 key 0.25', max(drawdowns(q)) == 0.25 == get('l13', 'quiz[0].widget.answer'))
check('l13 quiz0 slips: hilo 0.3333, first 0.2, pounds 15', round((60 - 40) / 60, 4) == 0.3333 and (50 - 40) / 50 == 0.2 and 60 - 45 == 15)
check('l13 quiz0 explain: peaks and drawdowns', list(running_peak(q)) == [50.0, 50.0, 60.0, 60.0] and list(drawdowns(q)) == [0.0, 0.2, 0.0, 0.25])
g = running_peak([3.0, 5.0])
check('l13 quiz1 third next raises StopIteration', [next(g), next(g)] == [3.0, 5.0] and raises(lambda: next(g)) == 'StopIteration')
b = [100.0, 100.4, 100.9, 101.3]
check('l13 quiz2 key 0.0; gain 0.013', max(drawdowns(b)) == 0.0 and round(b[-1] / b[0] - 1, 3) == 0.013)
check('l13 quiz2 a drawdown is never negative (random paths)',
      all(x >= 0 for s in range(200) for x in drawdowns([random.Random(s).uniform(1, 9) for _ in range(30)])))


def closes_return(rows):
    for row in rows:
        return float(row["Close"])


def closes_yield(rows):
    for row in rows:
        yield float(row["Close"])


RR = [{'Close': '1.5'}, {'Close': '2.5'}]
check('l13 quiz3 return ends at the first row; yield gives every close', closes_return(RR) == 1.5 and list(closes_yield(RR)) == [1.5, 2.5])
check('l13 quiz3 next of a float raises TypeError', raises(lambda: next(closes_return(RR))) == 'TypeError')
check('l13 quiz3 list of the returned float raises TypeError', raises(lambda: list(closes_return(RR))) == 'TypeError')

# ---------------------------------------------------------------- l14 sorting


def to_date(text):
    return datetime.strptime(text, "%d/%m/%Y").date()


D5 = ["30/03/2026", "02/04/2026", "27/03/2026", "01/04/2026", "31/03/2026"]
C5 = ["101.20", "103.10", "100.00", "99.80", "102.50"]
check('l14 s0 oldest is 27/03 (r2c0); smallest text is 01/04 (r3c0)', min(D5, key=to_date) == D5[2] and min(D5) == D5[3])
s = sorted(["30/03/2026", "02/04/2026", "27/03/2026"])
check('l14 s1 key: text sort puts April first', s == ['02/04/2026', '27/03/2026', '30/03/2026'] and right_id('l14', 'screens[1].widget') == ['right'])
src = ["30/03/2026", "02/04/2026", "27/03/2026"]
check('l14 s1 sorted returns a new list and leaves the input', sorted(src) is not src and src[0] == "30/03/2026")
check('l14 s1 list.sort sorts in place and returns None', (lambda L: (L.sort(), L))(list(src)) == (None, s))
check('l14 s2 strptime and date', to_date("27/03/2026") == date(2026, 3, 27) and type(to_date("02/04/2026")).__name__ == 'date')
check('l14 s2 without .date() the type is datetime at midnight', type(datetime.strptime("27/03/2026", "%d/%m/%Y")).__name__ == 'datetime'
      and datetime.strptime("27/03/2026", "%d/%m/%Y").hour == 0)
check('l14 s2 month-first pattern: 05/11 reads as 11 May; 27/03 raises "does not match format"',
      datetime.strptime("05/11/2025", "%m/%d/%Y").date() == date(2025, 5, 11) and raises(lambda: datetime.strptime("27/03/2026", "%m/%d/%Y")) == 'ValueError')
try:
    datetime.strptime("27/03/2026", "%m/%d/%Y")
except ValueError as e:
    check('l14 s2 error text', 'does not match format' in str(e))
check('l14 s2 dates compare by year, month, day', to_date("01/04/2026") > to_date("27/03/2026") and to_date("31/12/2025") < to_date("02/01/2026"))
ROWS = [{'Date': a, 'Close': b} for a, b in zip(D5, C5)]
rd = list(csv.DictReader(io.StringIO("Date,Close\n" + "\n".join(a + ',' + b for a, b in zip(D5, C5)) + "\n")))
check('l14 s3 DictReader rows are dictionaries of text', rd == ROWS and type(rd[0]) is dict)
srt = sorted(ROWS, key=lambda row: to_date(row["Date"]))
check('l14 s3 sorted by date: dates and closes', [r['Date'] for r in srt] == ['27/03/2026', '30/03/2026', '31/03/2026', '01/04/2026', '02/04/2026']
      and [r['Close'] for r in srt] == ['100.00', '101.20', '102.50', '99.80', '103.10'])
check('l14 s3 feedback: key on the text puts 1 April first', sorted(ROWS, key=lambda r: r["Date"])[0]['Date'] == '01/04/2026')
calls = []
sorted(ROWS, key=lambda r: calls.append(1) or to_date(r["Date"]))
check('l14 s3 the key is called once per item', len(calls) == 5)
check('l14 s3 sort by close with float key', [r['Close'] for r in sorted(ROWS, key=lambda row: float(row["Close"]))][0] == '99.80')
mx = max(row["Close"] for row in ROWS)
check('l14 s4 trap: text max is 99.80', mx == '99.80' and right_id('l14', 'screens[4].widget') == ['right'] and mx not in ('103.10', '101.20'))
check('l14 s4 explain: converting first gives 103.1', max(float(row["Close"]) for row in ROWS) == 103.1)
CL = [100.00, 101.20, 102.50, 99.80, 103.10]


def returns(closes):
    return [today / yesterday - 1 for yesterday, today in zip(closes, closes[1:])]


check('l14 s5 returns', [round(r, 6) for r in returns(CL)] == [0.012, 0.012846, -0.026341, 0.033066] and returns([100.0]) == [])
check('l14 s5 feedback: 1.2 by subtracting; -0.011858 upside down', round(101.20 - 100.00, 2) == 1.2 and round(100.00 / 101.20 - 1, 6) == -0.011858)
check('l14 s5 zip stops at the shorter list', len(list(zip(CL, CL[1:]))) == 4 and round(103.10 / 99.80 - 1, 3) == 0.033)
days = [("30/03", 0.012), ("31/03", 0.0128), ("01/04", -0.0263), ("02/04", 0.0331)]
worst = sorted(days, key=lambda day: day[1])[:2]
check('l14 s6 key', [dd_ for dd_, r in worst] == ['01/04', '30/03'] and right_id('l14', 'screens[6].widget') == ['right'])
check('l14 s6 option best is reverse=True', [x for x, r in sorted(days, key=lambda day: day[1], reverse=True)[:2]] == ['02/04', '31/03'])
check('l14 s6 option dates is the text sort; option first is file order',
      [x for x, r in sorted(days)[:2]] == ['01/04', '02/04'] and [x for x, r in days[:2]] == ['30/03', '31/03'])
row_date = lambda row: to_date(row["Date"])
check('l14 s7 key: newest first', [r['Date'] for r in sorted(ROWS, key=row_date, reverse=True)][0] == '02/04/2026')
check('l14 s7 text key with reverse is wrong', [r['Date'] for r in sorted(ROWS, key=lambda r: r["Date"], reverse=True)][0] != '02/04/2026')
check('l14 s7 negating a date raises TypeError', raises(lambda: sorted(ROWS, key=lambda r: -row_date(r))) == 'TypeError')
check('l14 s7 reversed only flips file order', [r['Date'] for r in reversed(ROWS)] == D5[::-1] != [r['Date'] for r in sorted(ROWS, key=row_date, reverse=True)])
check('l14 stability: equal keys keep input order, with reverse too',
      sorted([('b', 1), ('a', 1), ('c', 0)], key=lambda t: t[1]) == [('c', 0), ('b', 1), ('a', 1)]
      and sorted([('b', 1), ('a', 1), ('c', 0)], key=lambda t: t[1], reverse=True) == [('b', 1), ('a', 1), ('c', 0)])
check('l14 tuples as keys compare item by item', sorted([(4.5, 200), (4.5, 100), (4.4, 9)]) == [(4.4, 9), (4.5, 100), (4.5, 200)])
out, ns, err = run(get('l14', 'screens[8].widget.solution'))
V = "Date,Close\n05/02/2026,412.60\n04/02/2026,405.30\n03/02/2026,409.85\n02/02/2026,401.20\n30/01/2026,398.75\n29/01/2026,404.10\n28/01/2026,400.00\n"
NY = "Date,Close\n02/01/2026,249.90\n29/12/2025,250.00\n05/01/2026,255.00\n31/12/2025,247.45\n30/12/2025,252.50\n"
dr = ns['daily_returns']
SIX = [0.01025, -0.013239, 0.006144, 0.02156, -0.011102, 0.018011]
check('l14 s8 returns of the vendor file', [round(r, 6) for r in dr(V)] == SIX and err is None)
check('l14 s8 New Year file', [round(r, 6) for r in dr(NY)] == [0.01, -0.02, 0.009901, 0.020408])


def by(csv_text, order):
    rows = order(list(csv.DictReader(io.StringIO(csv_text))))
    c = [float(r["Close"]) for r in rows]
    return [round(x, 6) for x in returns(c)]


check('l14 s8 explain: on the New Year file reversing and text sort both fail',
      by(NY, lambda r: r[::-1]) != [0.01, -0.02, 0.009901, 0.020408] and by(NY, lambda r: sorted(r, key=lambda x: x["Date"])) != [0.01, -0.02, 0.009901, 0.020408])
check('l14 s8 reversing alone passes test 1 but text sort does not', by(V, lambda r: r[::-1]) == SIX and by(V, lambda r: sorted(r, key=lambda x: x["Date"])) != SIX)
check('l14 quiz0', sorted(["9.50", "10.25", "100.00"]) == ['10.25', '100.00', '9.50'] and '.' < '0' and sorted(["9.50", "10.25", "100.00"], key=float) == ['9.50', '10.25', '100.00'])
check('l14 quiz1 key -0.02; slips', math.isclose(245 / 250 - 1, get('l14', 'quiz[1].widget.answer')) and round(-5 / 245, 4) == -0.0204 and 245 - 250 == -5)
iso = ['2026-03-31', '2026-04-01', '2025-12-31', '2026-01-02']
check('l14 quiz2 ISO text order is time order', sorted(iso) == sorted(iso, key=date.fromisoformat))
check('l14 quiz2 wrong formats: uk, us, words', sorted(['31/03/2026', '01/04/2026'])[0] == '01/04/2026'
      and sorted(['12/31/2025', '01/02/2026'])[0] == '01/02/2026' and sorted(['31 Mar 2026', '01 Apr 2026'])[0] == '01 Apr 2026' and 'Apr' < 'Mar')
check('l14 quiz3 one close gives []', dr("Date,Close\n02/03/2026,101.00\n") == [] and raises(lambda: dr("Date,Close\n02/03/2026,101.00\n")) is None)

# ---------------------------------------------------------------- l15 assert, sd, volatility, pytest
R5 = [0.01, -0.02, 0.015, 0.005, -0.01]


def mean(xs):
    return sum(xs) / len(xs)


def sd(xs):
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs))


check('l15 s0 key: -2.0% is furthest (second cell)', max(range(5), key=lambda i: abs(R5[i])) == 1 and get('l15', 'screens[0].widget.answer') == ['c2'])
check('l15 s1 assert passes silently on true, raises AssertionError on false',
      raises(lambda: exec('assert 1 == 1')) is None and raises(lambda: exec('assert 1 == 2')) == 'AssertionError')
check('l15 s1 key: mean([0.1, 0.2]) == 0.15 is false', repr(0.1 + 0.2) == '0.30000000000000004' and repr(mean([0.1, 0.2])) == '0.15000000000000002'
      and mean([0.1, 0.2]) != 0.15 and math.isclose(mean([0.1, 0.2]), 0.15))
out, ns, err = run("def mean(xs):\n    return sum(xs) / len(xs)\n\nassert mean([0.1, 0.2]) == 0.15\nprint('passed')\n")
check('l15 s1 the snippet stops with AssertionError and prints nothing', err == 'AssertionError' and out == '')
check('l15 s2 sd([1,3]) is 1; five returns 0.013038', sd([1.0, 3.0]) == 1.0 and math.isclose(sd(R5), 0.013038404810405297) and math.isclose(sd([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]), 2.0))
check('l15 s2 squared distances add to 0.00085', math.isclose(sum(x * x for x in R5), 0.00085) and round(0.00085 / 5, 5) == 0.00017)
check('l15 s2 feedback: 0.00017 without the root; 0.012 with plain distances', round(sd(R5) ** 2, 5) == 0.00017 and round(mean([abs(x) for x in R5]), 3) == 0.012)
check('l15 s2 feedback: dividing by n - 1 gives root 2 for [1, 3]', math.isclose(statistics.stdev([1.0, 3.0]), math.sqrt(2)))
check('l15 s3 stdev 0.01457737, pstdev equals sd, ratio sqrt(5/4)', repr(sd(R5)).startswith('0.01303840') and repr(statistics.stdev(R5)).startswith('0.01457737')
      and math.isclose(statistics.pstdev(R5), sd(R5)) and math.isclose(statistics.stdev(R5) / sd(R5), math.sqrt(5 / 4)) and round(math.sqrt(5 / 4), 3) == 1.118)
check('l15 s3 trap: the assert fails', not math.isclose(sd(R5), statistics.stdev(R5)) and round(statistics.stdev(R5) - sd(R5), 4) == 0.0015)
check('l15 s4 pstdev of one value is 0.0; stdev raises StatisticsError', statistics.pstdev([0.012]) == 0.0 and raises(lambda: statistics.stdev([0.012])) == 'StatisticsError')
try:
    statistics.stdev([0.012])
except statistics.StatisticsError as e:
    check('l15 s4 message (3.11 and later; earlier versions say "variance requires")',
          str(e) == 'stdev requires at least two data points' if sys.version_info >= (3, 11) else 'at least two data points' in str(e), str(e))
check('l15 s5 252 = 365 - 104 - 9; sqrt(252) is 15.87', 365 - 104 - 9 == 252 and round(S252, 2) == 15.87)
check('l15 s6 key 19.05% and slips', round(0.012 * S252, 4) == 0.1905 and 0.012 * 252 == 3.024 and round(0.012 * math.sqrt(365), 4) == 0.2293
      and abs(math.sqrt(1.2) / 100 - 0.011) <= 0.0001)
GOOD = lambda r: statistics.stdev(r) * math.sqrt(252)
HAND = lambda r: (sum((x - sum(r) / len(r)) ** 2 for x in r) / (len(r) - 1)) ** 0.5 * 252 ** 0.5
BAD = [lambda r: statistics.pstdev(r) * math.sqrt(252), lambda r: statistics.stdev(r) * 252, lambda r: statistics.stdev(r) * math.sqrt(365)]
target = math.sqrt(0.0002 * 252)
check('l15 s7 one hand-worked value passes both right versions and catches all three mistakes',
      math.isclose(GOOD([0.01, -0.01]), target) and math.isclose(HAND([0.01, -0.01]), target) and not any(math.isclose(b([0.01, -0.01]), target) for b in BAD))
check('l15 s7 explain values 0.2245, 0.1587, 3.564, 0.2702', [round(target, 4)] + [round(b([0.01, -0.01]), 4) for b in BAD] == [0.2245, 0.1587, 3.5638, 0.2702])
check('l15 s7 identical returns: both right versions within 1e-12 of 0', abs(GOOD([0.003] * 3)) <= 1e-12 and abs(HAND([0.003] * 3)) <= 1e-12)
check('l15 s7 a test that only asserts "> 0" passes on every mistake (proves little)', all(b([0.01, -0.01]) > 0 for b in BAD))
check('l15 s9 vol of the six returns is 23.16%, daily 0.0146', math.isclose(GOOD(SIX), 0.23155971310744017) and round(statistics.stdev(SIX), 4) == 0.0146)
check('l15 s9 tests and feedback values', math.isclose(GOOD(R5), 0.2314087293081227) and round(BAD[0](R5), 4) == 0.2070 and round(BAD[1](R5), 2) == 3.67 and GOOD([0.003] * 4) == 0.0)
out, ns, err = run(get('l15', 'screens[9].widget.solution'))
check('l15 s9 solution prints 23.16%', out.strip() == 'Annualised vol: 23.16%' and err is None, out)
check('l15 summary: stdev over pstdev is sqrt(n/(n-1))', all(math.isclose(statistics.stdev(x) / statistics.pstdev(x), math.sqrt(len(x) / (len(x) - 1))) for x in (R5, SIX)))
check('l15 quiz0 sqrt(20/19) is 1.026', round(math.sqrt(20 / 19), 3) == 1.026)
check('l15 quiz1 key and slips', round(0.008 * S252, 3) == 0.127 and 0.008 * 252 == 2.016 and round(0.008 * math.sqrt(365), 4) == 0.1528)
naive = 0.0
for x in R5:
    naive += x
check('l15 quiz2 float sum is off zero (compensated sum, 3.12 and later: -8.7e-19)',
      (sum(R5) != 0 and (sys.version_info < (3, 12) or '%.1e' % sum(R5) == '-8.7e-19')), sum(R5))
check('l15 quiz2 the plain left-to-right sum is off zero too (earlier versions)', naive != 0, naive)
check('l15 quiz2 key: the assert fails; 0.0 == 0 is allowed', raises(lambda: exec('assert sum(r) / len(r) == 0', {'r': R5})) == 'AssertionError' and 0.0 == 0)
check('l15 quiz2 explain: near zero rel_tol alone is too strict; abs_tol works', not math.isclose(mean(R5), 0) and math.isclose(mean(R5), 0, abs_tol=1e-12))
check('l15 quiz3 key and wrong options', GOOD([0.004, 0.004]) < 1e-12 and raises(lambda: GOOD([0.004])) == 'StatisticsError'
      and GOOD([0.01, -0.01]) != 0.2245 and all(b([0.01, -0.01]) > 0 for b in BAD))

# Monte Carlo: sqrt-of-time rule, its hypothesis, and the n - 1 divisor
rng = random.Random(20261112)
N = 4000
iid = [sum(rng.gauss(0, 0.012) for _ in range(252)) for _ in range(N)]
ratio = statistics.pstdev(iid) / 0.012
check('MC l15 s5: independent days, yearly sd is about sqrt(252) daily, not 252', abs(ratio / S252 - 1) < 0.05, ratio)


def ar1(rho):
    e, tot = 0.0, 0.0
    s_innov = 0.012 * math.sqrt(1 - rho * rho)
    x = rng.gauss(0, 0.012)
    for _ in range(252):
        tot += x
        x = rho * x + rng.gauss(0, s_innov)
    return tot


corr = [ar1(0.3) for _ in range(N)]
ratio_c = statistics.pstdev(corr) / 0.012
check('MC l15 s5: with correlated days the sqrt(252) rule fails (the hypothesis matters)', ratio_c / S252 > 1.25, ratio_c)
vn = vn1 = 0.0
M = 40000
for _ in range(M):
    xs = [rng.gauss(0.001, 0.012) for _ in range(5)]
    vn += statistics.pvariance(xs)
    vn1 += statistics.variance(xs)
check('MC l15 s3: dividing by n runs small (about 4/5 of the true variance); n - 1 does not',
      abs(vn / M / 0.012 ** 2 - 0.8) < 0.03 and abs(vn1 / M / 0.012 ** 2 - 1) < 0.03, (vn / M / 0.012 ** 2, vn1 / M / 0.012 ** 2))

# pytest behaviour (run when pytest is installed)
try:
    import pytest  # noqa: F401
    HAVE_PYTEST = True
except ImportError:
    HAVE_PYTEST = False


def pytest_run(files, args=()):
    d = tempfile.mkdtemp(prefix='pf4-pytest-')
    for name, text in files.items():
        open(os.path.join(d, name), 'w').write(text)
    env = dict(os.environ, PYTEST_ADDOPTS='-p no:cacheprovider -q')  # options by environment, so sys.argv is as for a bare `pytest`
    p = subprocess.run([sys.executable, '-m', 'pytest', *args], cwd=d, capture_output=True, text=True, env=env)
    return p.stdout + p.stderr


TWO_FAILS = None
if HAVE_PYTEST:
    o = pytest_run({'test_risk.py': "def helper():\n    raise RuntimeError('helper ran')\n\ndef check_vol(vol):\n    assert False\n\n"
                    "def annualised_vol_test():\n    assert False\n\ndef test_annualised_vol():\n    assert True\n"})
    check('pytest l15 s8: only the test_ function is collected and run', '1 passed' in o and 'failed' not in o and 'error' not in o.lower(), o[-300:])
    o = pytest_run({'test_two.py': "def test_two():\n    assert 1 == 2\n    assert 3 == 4\n"})
    TWO_FAILS = ('1 failed' in o, 'assert 1 == 2' in o, 'assert 3 == 4' in o)
    check('pytest: a failing assert is reported as a failed test', TWO_FAILS[0] and TWO_FAILS[1], o[-300:])
    check('pytest: a test stops at its first failing assert (the second is not reported)', not TWO_FAILS[2], o[-300:])
    o = pytest_run({'test_empty.py': "def test_nothing():\n    pass\n"})
    check('pytest: a test with no assert passes (a pass proves only what is asserted)', '1 passed' in o, o[-300:])
    UNGUARDED = "import sys\n\ndef max_drawdown(prices):\n    return 0.0\n\ndef print_summary(path):\n    print(open(path).read())\n\npath = sys.argv[1]\nprint_summary(path)\n"
    TEST = "from summary import max_drawdown\n\ndef test_md():\n    assert max_drawdown([1.0]) == 0.0\n"
    o = pytest_run({'summary.py': UNGUARDED, 'test_summary.py': TEST})
    check('pytest l16 s5: unguarded script lines run on import and the import fails (bare pytest: IndexError)', 'IndexError' in o and 'passed' not in o, o[-400:])
    GUARDED = UNGUARDED.replace("path = sys.argv[1]\nprint_summary(path)\n", "if __name__ == '__main__':\n    path = sys.argv[1]\n    print_summary(path)\n")
    o = pytest_run({'summary.py': GUARDED, 'test_summary.py': TEST})
    check('pytest l16 s5: with the guard the import only defines functions', '1 passed' in o, o[-300:])
    MAINCALL = "import sys\n\ndef max_drawdown(prices):\n    return 0.0\n\ndef main(argv):\n    open('summary.txt', 'w').write(open(argv[1]).read()[:5])\n\nmain(sys.argv)\n"
    o = pytest_run({'summary.py': MAINCALL, 'test_summary.py': TEST}, ['test_summary.py'])
    check('pytest h4-import: unguarded main(sys.argv) runs on import with pytest\'s arguments', 'passed' in o or 'rror' in o, o[-300:])

# ---------------------------------------------------------------- l16 argv, guard, formatting, files
p = subprocess.run([sys.executable, '-c', 'import sys; print(sys.argv)', 'prices.csv', '252'], capture_output=True, text=True)
check('l16 argv items are text', p.stdout.strip() == "['-c', 'prices.csv', '252']", p.stdout)
open(os.path.join(TMP, 'summary.py'), 'w').write('import sys\nprint(__name__)\nprint(sys.argv)\n')
p = subprocess.run([sys.executable, 'summary.py', 'prices.csv', '252'], cwd=TMP, capture_output=True, text=True)
check('l16 s0/s1/s4 run directly: __main__ and argv', p.stdout.split('\n')[:2] == ['__main__', "['summary.py', 'prices.csv', '252']"], p.stdout)
p = subprocess.run([sys.executable, '-c', 'import summary'], cwd=TMP, capture_output=True, text=True)
check('l16 s4 imported: __name__ is summary', p.stdout.split('\n')[0] == 'summary', p.stdout)
check('l16 s1 key 252252 and wrong options', '252' * 2 == '252252' and '252' * 2 != 504 and int('252') * 2 == 504)
check('l16 s2 IndexError: list index out of range', raises(lambda: ['summary.py'][1]) == 'IndexError')
try:
    ['summary.py'][1]
except IndexError as e:
    check('l16 s2 message', str(e) == 'list index out of range')
out, ns, err = run(get('l16', 'screens[3].widget.solution'))
check('l16 s3 parse_args', out == "('prices.csv', 252)\n('prices.csv', 365)\n" and type(ns['parse_args'](['s', 'f', '260'])[1]) is int)
fr = lambda label, value: f"{label:<14}{value:>8.2%}"
check('l16 s6 format_row', fr('Total return', 0.0315) == 'Total return     3.15%' and fr('Worst day', -0.0532) == 'Worst day       -5.32%'
      and fr('Annual vol', 0.2904) == 'Annual vol      29.04%' and len(fr('Return', 0.1)) == 22)
check('l16 s6 feedback: .2f gives 0.03', f"{0.0315:>8.2f}".strip() == '0.03')
out, ns, err = run(get('l16', 'screens[7].widget.solution'))
ws = ns['write_summary']
os.chdir(TMP)
ws('s3.txt', ['old', 'text'])
ws('s3.txt', ['new'])
check('l16 s7 "w" replaces; write adds no newline', open('s3.txt').read() == 'new\n' and out == 'Days 10\nVol 29.04%\n\n')
with open('a.txt', 'w') as f:
    f.write('x')
    f.write('y')
for _ in range(2):
    with open('a.txt', 'a') as f:
        f.write('Max drawdown 3.56%\n')
check('l16 s7 / r4-append: write joins with no newline; "a" appends', open('a.txt').read() == 'xy' + 'Max drawdown 3.56%\n' * 2)
with open('a.txt', 'w') as f:
    pass
check('l16 s7 with closes the file; "w" empties it', f.closed and open('a.txt').read() == '')


def wrong_reopen(path, lines):
    for line in lines:
        with open(path, 'w') as f:
            f.write(line + '\n')


wrong_reopen('b.txt', ['a', 'b'])
check('l16 s7 feedback: reopening inside the loop leaves only the last line', open('b.txt').read() == 'b\n')
os.chdir(HERE)
out, ns, err = run(get('l16', 'screens[9].widget.solution'))
check('l16 s9 table', out == 'Days                10\nTotal return     4.03%\nAnnual vol      29.04%\nMax drawdown     3.56%\n' and err is None, out)
FEB = [180.0, 182.7, 179.45, 176.2, 178.9, 183.35, 181.1, 185.6, 184.05, 187.25]
check('l16 s9 values', ns['read_closes'](ns['CSV']) == FEB and math.isclose(max(drawdowns(FEB)), (182.70 - 176.20) / 182.70)
      and math.isclose(FEB[-1] / FEB[0] - 1, 0.04027777777777786) and math.isclose(GOOD(returns(FEB)), 0.2903929987228655))
rf = returns(FEB)
prod = 1.0
for x in rf:
    prod *= 1 + x
check('l16 s9 compounding the daily returns gives the total return; adding them only approximates',
      math.isclose(prod - 1, FEB[-1] / FEB[0] - 1) and not math.isclose(sum(rf), FEB[-1] / FEB[0] - 1, rel_tol=1e-4) and abs(sum(rf) - (FEB[-1] / FEB[0] - 1)) < 0.002)
check('l16 s9 no look-ahead: each return uses only that close and the one before', all(math.isclose(rf[i], FEB[i + 1] / FEB[i] - 1) for i in range(9)) and len(rf) == 9)
check('l16 quiz0 len 3', len(['summary.py', 'fund.csv', '260']) == 3)
open(os.path.join(TMP, 'risk.py'), 'w').write("def total_return(closes):\n    return closes[-1] / closes[0] - 1\n\nif __name__ == '__main__':\n    print(total_return([100.0, 104.0]))\n")
p = subprocess.run([sys.executable, '-c', 'from risk import total_return'], cwd=TMP, capture_output=True, text=True)
p2 = subprocess.run([sys.executable, 'risk.py'], cwd=TMP, capture_output=True, text=True)
check('l16 quiz1 import prints nothing; run directly prints 0.040000000000000036', p.stdout == '' and p2.stdout.strip() == '0.040000000000000036', p2.stdout)
check('l16 quiz2 key and options', f"[{-0.0532:>8.2%}]" == '[  -5.32%]' and f"[{-0.0532:<8.2%}]" == '[-5.32%  ]' and f"[{-0.0532:>8.2f}]" == '[   -0.05]')
check('l16 quiz3 +10% then -10% is -1%', math.isclose(1.10 * 0.90 - 1, -0.01) and get('l16', 'quiz[3].widget.answer') == -0.01)

# ---------------------------------------------------------------- review-4
g = running_peak([5.0, 3.0, 8.0])
next(g)
check('r4-resume', list(g) == [5.0, 8.0])
R3 = [{'Date': '2026-03-02', 'Close': '98.40'}, {'Date': '2026-03-03', 'Close': '101.75'}, {'Date': '2026-03-04', 'Close': '99.90'}]
check('r4-text-max key and the text pick', max(R3, key=lambda r: float(r["Close"]))['Date'] == '2026-03-03' and max(R3, key=lambda r: r["Close"])['Date'] == '2026-03-04'
      and min(R3, key=lambda r: float(r["Close"]))['Date'] == '2026-03-02')
P5 = [200, 220, 187, 230, 207]
check('r4-mdd key and slips', math.isclose(max(drawdowns(P5)), 0.15) and round((230 - 187) / 230, 3) == 0.187 and (230 - 207) / 230 == 0.1 and 220 - 187 == 33)
check('r4-mdd explain', list(running_peak(P5)) == [200, 220, 220, 230, 230] and [round(x, 4) for x in drawdowns(P5)] == [0, 0, 0.15, 0, 0.1])
check('r4-argv', '260' + '0' == '2600')
v = statistics.stdev([0.03, 0.0]) * S252
check('r4-stdev-hand key and slips', round(v, 4) == 0.3367 and round(statistics.pstdev([0.03, 0.0]) * S252, 4) == 0.2381
      and round(statistics.stdev([0.03, 0.0]), 4) == 0.0212 and round(statistics.stdev([0.03, 0.0]) * 252, 3) == 5.346 and round(math.sqrt(0.00045), 5) == 0.02121)
check('r4-sort-dates', sorted(["05/01/2026", "31/12/2025", "02/01/2026"], key=to_date)[0] == '31/12/2025' and sorted(["05/01/2026", "31/12/2025", "02/01/2026"])[0] == '02/01/2026')
check('r4-total', round(1.05 * 0.95 * 1.05, 6) == 1.047375 and round(100 * 1.05 * 0.95, 2) == 99.75 and round(100 * 1.047375, 2) == 104.74)
out, ns, err = run(get('r4', 'items[9].widget.solution'))
check('r4-code-best', out.strip() == '2026-05-12' and ns['best_day']("Date,Close\n2026-01-05,9.80\n2026-01-06,10.40\n") == '2026-01-06')
BD = list(csv.DictReader(io.StringIO(ns['CSV'])))
check('r4-code-best feedback: text comparison picks 2026-05-13', max(BD, key=lambda r: r["Close"])["Date"] == '2026-05-13')

# ---------------------------------------------------------------- homework-4
out, ns, err = run(get('h4', 'items[0].widget.solution'))
dp = ns['drawdown_period']
D10 = ['02/03', '03/03', '04/03', '05/03', '06/03', '09/03', '10/03', '11/03', '12/03', '13/03']
r0 = dp(D10[:5], [100.0, 104.0, 98.8, 101.0, 97.76])
check('h4-period', r0[:2] == ('03/03', '06/03') and math.isclose(r0[2], 0.06) and dp(D10, TEN)[:2] == ('06/03', '10/03')
      and dp(['a', 'b', 'c'], [100.0, 101.0, 102.5]) == ('a', 'a', 0.0) and dp(['a', 'b', 'c', 'd'], q)[:2] == ('c', 'd'))
out, ns, err = run(get('h4', 'items[1].widget.solution'))
wd = ns['worst_days']
check('h4-worst-days', wd(V, 2) == ['30/01/2026', '04/02/2026'] and wd(NY, 2) == ['31/12/2025', '02/01/2026']
      and wd("Date,Close\n03/03/2026,99.00\n02/03/2026,100.00\n", 3) == ['03/03/2026'] and out.strip() == "['30/01/2026', '04/02/2026']")
check('h4-worst-days explain: -1.32% and -1.11%', round(SIX[1] * 100, 2) == -1.32 and round(SIX[4] * 100, 2) == -1.11)
c = closes_yield([{'Close': '10'}, {'Close': '11'}, {'Close': '12'}])
peak = max(c)
rets = [b_ / a_ - 1 for a_, b_ in zip(c, list(c)[1:])]
check('h4-reuse: returns is empty and stdev raises StatisticsError', peak == 12.0 and rets == [] and raises(lambda: statistics.stdev(rets)) == 'StatisticsError')
check('h4-reuse: zip accepts a generator', list(zip(closes_yield([{'Close': '1'}]), [9])) == [(1.0, 9)])
check('h4-weekly key and slips', round(0.025 * math.sqrt(52), 4) == 0.1803 and round(0.025 * S252, 4) == 0.3969 and 0.025 * 52 == 1.3 and round(math.sqrt(52), 2) == 7.21)
check('h4-big-n', round(math.sqrt(1000 / 999), 4) == 1.0005 and round(0.0120 * math.sqrt(1000 / 999), 6) == 0.012006 and round(0.012 * math.sqrt(5 / 4), 4) == 0.0134)
out, ns, err = run(get('h4', 'items[5].widget.solution'), argv=[''])
check('h4-tool: with sys.argv == [\'\'] the guard prints the usage line', out.strip() == 'Usage: python summary.py prices.csv [periods]' and err is None, out)
os.chdir(TMP)
H1 = "Date,Close\n13/02/2026,187.25\n12/02/2026,184.05\n11/02/2026,185.60\n10/02/2026,181.10\n09/02/2026,183.35\n06/02/2026,178.90\n05/02/2026,176.20\n04/02/2026,179.45\n03/02/2026,182.70\n02/02/2026,180.00\n"
H3 = "Date,Close\n13/02/2026,105.60\n06/02/2026,101.20\n30/01/2026,103.80\n23/01/2026,99.10\n16/01/2026,102.40\n09/01/2026,100.00\n"
with open('h1.csv', 'w') as f:
    f.write(H1)
with open('h3.csv', 'w') as f:
    f.write(H3)
l1 = ns['main'](['summary.py', 'h1.csv'])
t1 = open('summary.txt').read()
l3 = ns['main'](['summary.py', 'h3.csv', '52'])
os.chdir(HERE)
check('h4-tool lines', l1 == ['Days                10', 'Total return     4.03%', 'Annual vol      29.04%', 'Max drawdown     3.56%'] and t1 == '\n'.join(l1) + '\n')
check('h4-tool weekly', l3 == ['Days                 6', 'Total return     5.60%', 'Annual vol      27.26%', 'Max drawdown     3.22%'])
W = [100.0, 102.4, 99.1, 103.8, 101.2, 105.6]
check('h4-tool weekly by hand', round(statistics.stdev(returns(W)) * math.sqrt(52), 4) == 0.2726 and round((102.4 - 99.1) / 102.4, 4) == 0.0322)
check('h4-tool Friday closes, 2026', all(to_date(x).weekday() == 4 for x in ['09/01/2026', '16/01/2026', '23/01/2026', '30/01/2026', '06/02/2026', '13/02/2026']))
check('h4-debug model: bug gives 3.56; 0.25 for the four closes', round(statistics.stdev([0.01, -0.01]) * 252, 2) == 3.56 and max(drawdowns(q)) == 0.25)
check('h4-debug model: max of a spent generator with default is 0.0', max(iter([]), default=0.0) == 0.0)
out, ns, err = run(get('h4', 'items[8].widget.solution'))
so, ap = ns['sweep_offers'], ns['average_price']
BOOK = [(4.52, 300), (4.50, 200), (4.55, 500), (4.50, 100)]
check('h4-sweep fills', list(so(450, BOOK)) == [(4.50, 200), (4.50, 100), (4.52, 150)] and list(so(300, BOOK)) == [(4.50, 200), (4.50, 100)]
      and list(so(2000, BOOK)) == [(4.50, 200), (4.50, 100), (4.52, 300), (4.55, 500)] and list(so(100, [])) == []
      and list(so(250, (o for o in BOOK))) == [(4.50, 200), (4.50, 50)] and BOOK == [(4.52, 300), (4.50, 200), (4.55, 500), (4.50, 100)])
check('h4-sweep averages', math.isclose(ap(450, BOOK), 2028 / 450) and ap(100, []) is None and ap(50, BOOK) == 4.5 and math.isclose(ap(2000, BOOK), 4981 / 1100)
      and raises(lambda: ap(-50, BOOK)) == 'ValueError' and raises(lambda: list(so(0, []))) == 'ValueError')
check('h4-sweep stability: sorted with a price key keeps equal prices in book order; sorting the tuples does not',
      sorted(BOOK, key=lambda o: o[0])[:2] == [(4.50, 200), (4.50, 100)] and sorted(BOOK)[:2] == [(4.50, 100), (4.50, 200)])
check('h4-sweep feedback: iter of a list is not a generator; assert raises AssertionError; a generator has no len or sort',
      type(iter([1])).__name__ != 'generator' and raises(lambda: len(o for o in BOOK)) == 'TypeError' and not hasattr((o for o in BOOK), 'sort'))
lazy_call = raises(lambda: so(0, BOOK))
check('h4-sweep laziness: sweep_offers(0, book) raises nothing until the first next', lazy_call is None and raises(lambda: next(so(0, BOOK))) == 'ValueError')

# ---------------------------------------------------------------- every code widget: solution passes, starter fails
# Mirrors the engine's harness (app/js/engine/widgets/code.js): equal is ==, isclose is rel 1e-9 with abs 1e-12,
# raises names the exception, stdout compares the printed text with trailing spaces ignored.


def grade(code, w):
    """Number of tests the code passes, out of len(tests)."""
    out, ns, err = run(code)
    ns['__learner_source__'] = code
    if w.get('prelude'):
        exec(w['prelude'], ns)
    ok = 0
    cwd = os.getcwd()
    os.chdir(TMP)
    try:
        for t in w['tests']:
            try:
                if t['compare'] == 'stdout':
                    norm = lambda x: [ln.rstrip() for ln in x.strip('\n').split('\n')]
                    ok += err is None and norm(out) == norm(t['expect'])
                    continue
                if t.get('setup'):
                    exec(t['setup'], ns)
                if t['compare'] == 'raises':
                    try:
                        eval(t['call'], ns)
                    except Exception as e:
                        ok += type(e).__name__ == t['expect']
                    continue
                with contextlib.redirect_stdout(io.StringIO()):
                    got_, exp_ = eval(t['call'], ns), eval(t['expect'], ns)
                if t['compare'] == 'isclose':
                    ok += math.isclose(float(got_), float(exp_), rel_tol=1e-9, abs_tol=1e-12)
                else:
                    ok += got_ == exp_ and type(got_) is type(exp_)
            except Exception:
                pass
    finally:
        os.chdir(cwd)
    return ok


n_code = 0
for f in FILES:
    doc = FILES[f]
    holders = [('screens[%d]' % i, x) for i, x in enumerate(doc.get('screens', []))] + [('quiz[%d]' % i, x) for i, x in enumerate(doc.get('quiz', []))] \
        + [('items[%d]' % i, x) for i, x in enumerate(doc.get('items', []))]
    for path_, h in holders:
        w = h.get('widget', {})
        if w.get('kind') != 'code':
            continue
        n_code += 1
        n = len(w['tests'])
        a = grade(w['solution'], w)
        b_ = grade(w['starter'], w)
        check('code %s %s: solution passes all %d tests' % (f, path_, n), a == n, '%d of %d' % (a, n))
        check('code %s %s: starter fails at least one test' % (f, path_), b_ < n, '%d of %d' % (b_, n))
        for e in w.get('examples', []):
            check('code %s %s: each example is also met by the solution' % (f, path_), grade(w['solution'], dict(w, tests=[e])) == 1, e['call'][:60])
check('code widgets in scope: 19', n_code == 19, n_code)

# ---------------------------------------------------------------- FINDING checks (fail until the content is fixed)
txt = get('l15', 'screens[8].prose')
check('FINDING 1 (l15 screens[8].prose): pytest does not report "each failing assert"; a test stops at its first',
      'each failing assert' not in txt, 'pytest run: %s' % (TWO_FAILS,))

prompt = get('h4', 'items[6].widget.prompt')
model = get('h4', 'items[6].widget.model')
nonzero = 0
for s_ in range(500):
    r_ = random.Random(s_)
    path = [100.0]
    for _ in range(20):
        path.append(path[-1] * (1 + r_.gauss(-0.005, 0.012)))
    if max(drawdowns(path[::-1])) > 0:
        nonzero += 1
mono = [100.0 * 0.995 ** i for i in range(20)]
check('h4-debug: a path that falls every day, read backwards, has drawdown 0', max(drawdowns(mono[::-1])) == 0.0 and max(drawdowns(mono)) > 0.09)
# Fix pass: finding 2 fixed differently. The prompt now reports a non-zero 6%, below the stated 9% fall, and the model
# says what a backwards read really measures. The check asserts that property instead of "the prompt says every day".
def largest_rise(p):
    return max(1 - p[i] / max(p[i:]) for i in range(len(p)))
rev_eq = above = below = 0
for s_ in range(500):
    r_ = random.Random(s_)
    path = [100.0]
    for _ in range(20):
        path.append(path[-1] * (1 + r_.gauss(-0.005, 0.012)))
    rv, tv = max(drawdowns(path[::-1])), max(drawdowns(path))
    rev_eq += abs(rv - largest_rise(path)) < 1e-12
    above += rv > tv
    below += rv < tv
rep_dd = re.search(r'maximum drawdown of (\d+(?:\.\d+)?)%', prompt)
check('FINDING 2 (h4 items[6]): read backwards, max_drawdown is the largest rise to a later high (%d of 500), above the true figure on %d paths and below on %d; the prompt must report a non-zero figure below the 9%% fall and the model must say so' % (rev_eq, above, below),
      rev_eq == 500 and above > 0 and below > 0 and rep_dd is not None and 0 < float(rep_dd.group(1)) < 9 and 'fell about 9% from its high' in prompt
      and 'largest rise from a low to a later high' in model and 'never rose on any day' in model
      and 'looks like a rising one' not in model and 'no drawdown' not in get('h4', 'items[6].widget.rubric[3].text'))
check('FINDING 3 (h4 items[6].widget.model): the max_drawdown assert passes on the date-order bug, so it cannot be the test "that fails on the buggy code"',
      not (max(drawdowns(q)) == 0.25 and 'And `assert math.isclose(max_drawdown([50.0, 40.0, 60.0, 45.0]), 0.25)`' in model))
check('FINDING 4 (l15 summary.ideas[0]): "never ==" drops the abs_tol the lesson needs near zero',
      not ('never `==`' in get('l15', 'summary.ideas[0]') and not math.isclose(1e-18, 0.0) and 0.5 + 0.25 == 0.75))
bad = [p_ for p_, s_ in strings('l15') if p_.startswith('screens[6]') and re.search(r'15\.87\b(?!\d)', s_) and '19.05' in s_ and r'\times' in s_]
check('FINDING 5 (l15 screens[6]): the shown product 1.2 x 15.87 is 19.04, not 19.05', not (round(1.2 * 15.87, 2) != 19.05 and bad), bad)
# Fix pass: finding 6 fixed differently in feedback.correct (root carried to 0.021213, times 15.87). The check asserts
# that every root shown times every multiplier shown in an items[4] string rounds to the key, 33.67%.
bad = []
for p_, s_ in strings('r4'):
    if p_.startswith('items[4]') and re.search(r'15\.87', s_):
        roots = [float(x) for x in re.findall(r'(?<![\d.])0\.0212\d*', s_)]
        mults = [float(x) for x in re.findall(r'15\.87\d*', s_)]
        if any(round(r * m, 4) != 0.3367 for r in roots for m in mults):
            bad.append(p_)
check('FINDING 6 (review-4 items[4]): every shown root times the shown sqrt(252) rounds to 33.67%', not bad, bad)
# Fix pass: finding 7 fixed differently. The model keeps 1.63% (412 / 252 = 1.6349 to two places) and says that
# 411% is the reported 412% up to rounding; the check asserts those digits reproduce.
check('FINDING 7 (h4 items[6].widget.model): the daily sd is derived from 412% and the products reproduce it up to rounding',
      '412% over 252 is a daily sd of about 1.63%' in model and 'up to rounding' in model and round(412 / 252, 2) == 1.63
      and round(1.63 * 252) == 411 and round(1.63 * 15.87, 1) == 25.9 and '412%' in prompt)
check('FINDING 8 (l15 screens[5]): independence is used as a fact; it is an assumption of the model',
      re.search(r'[Aa]ssum|[Tt]reat the days as independent|[Ss]uppose', get('l15', 'screens[5].prose')) is not None)
check('FINDING 9 (review-4 items[6].prose): "Daily returns are roughly independent" stated as an empirical fact',
      'Daily returns are roughly independent' not in get('r4', 'items[6].prose'))
pc = subprocess.run([sys.executable, '-c', 'import sys; print(repr(sys.argv[0]))'], capture_output=True, text=True).stdout.strip()
check('FINDING 10 (l16 screens[0].explain.text): sys.argv[0] is not "always the script itself" (python -c gives %s)' % pc,
      not ('always the script itself' in get('l16', 'screens[0].explain.text') and pc == "'-c'"))
check('FINDING 11 (l16 quiz[2].feedback.generic): ">" is the alignment, not the fill', 'fill, width' not in get('l16', 'quiz[2].feedback.generic'))
check('FINDING 12 (l14 summary.ideas[1]): ISO dates sort correctly as text, so "dates sort wrongly" is too wide',
      not ('so dates and prices sort wrongly' in get('l14', 'summary.ideas[1]') and sorted(iso) == sorted(iso, key=date.fromisoformat)))
check('FINDING 13 (l14 quiz[3].explain.text): "always n - 1" fails for an empty file (0 closes give 0 returns)',
      not ('always give $n - 1$' in get('l14', 'quiz[3].explain.text') and len(returns([])) == 0))
alpha = [p_ for p_, s_ in strings('l14') if 'alphabetically' in s_ and 'month names' not in s_]
check('FINDING 14 (l14): text order is by character code, not alphabetical ("Zebra" < "apple", "10" < "9")',
      not (alpha and 'Zebra' < 'apple' and sorted(['b', 'B', 'a']) == ['B', 'a', 'b']), alpha)
beats_small = "`'02/04'` beats `'27/03'`" in get('l14', 'screens[1].feedback.byKey.time') or '`01` beats `27`' in get('l14', 'screens[0].feedback.byKey.r3c0')
beats_big = "`'99.80'` beats `'103.10'`" in get('l14', 'screens[4].widget.options[0].why')
check('FINDING 15 (l14): "beats" means sorts first on two screens and is larger on another', not (beats_small and beats_big and '02/04' < '27/03' and '99.80' > '103.10'))
ex = get('l14', 'screens[4].explain.text')
check('FINDING 16 (l14 screens[4].explain.text): max with a key returns the whole row, not the close',
      not ('Give `max` a key' in ex and 'row' not in ex.split('Give `max` a key')[1].replace('lambda row', '').replace('row["Close"]', '').replace('(rows', '')
           and type(max(ROWS, key=lambda row: float(row["Close"]))) is dict))
check('FINDING 17 (l16 screens[5] option imperr): not any .py file can be imported (a name such as my-tool.py cannot)',
      not ('Any `.py` file can be imported' in get('l16', 'screens[5].widget.options[3].why') and raises(lambda: compile('import my-tool', 'x', 'exec')) == 'SyntaxError'))
check('FINDING 18 (l16 screens[7] starter and solution): the file is read back with a bare open() that is never closed, one screen after `with` is taught',
      'print(open("summary.txt").read())' not in get('l16', 'screens[7].widget.starter'))
check('FINDING 19 (h4 items[5]): a weekly file is summarised under the label "Days" with no word on it',
      re.search(r'label|counts the closes|number of closes', get('h4', 'items[5].prose') + get('h4', 'items[5].explain.text')) is not None)
check('FINDING 20 (h4 items[8]): the ValueError comes on the first next, not at the call; no string says so',
      re.search(r'first `next`|when the loop starts|on the first', get('h4', 'items[8].question') + get('h4', 'items[8].explain.text') + get('h4', 'items[8].feedback.byKey.test-8')) is not None)
cited = [(f, p_) for f in FILES for p_, s_ in strings(f) if re.search(r"\bl\d+'s\b|\bin l\d+\b|\blesson \d+\b", s_) and not p_.endswith(('starter', 'solution'))]
check('FINDING 21: lessons cited by number in learner text', not cited, cited)
eq_good = GOOD([0.01, -0.01]) == target
eq_hand = HAND([0.01, -0.01]) == target
check('l15 s7 explain: == against the hand-worked value wrongly fails the hand-written right version (test 5), and the stdev one too', not eq_hand and not eq_good, (eq_good, eq_hand))

print('Monte Carlo: yearly sd over daily sd, independent days %.2f, AR(1) 0.3 days %.2f, sqrt(252) %.2f' % (ratio, ratio_c, S252))
print('py-found L4 concepts: %d checks passed, %d failed (Python %s, pytest %s)' % (passed, len(fails), sys.version.split()[0], 'yes' if HAVE_PYTEST else 'not installed: pytest checks skipped'))
for f_ in fails:
    print('FAIL ' + f_)
sys.exit(1 if fails else 0)
