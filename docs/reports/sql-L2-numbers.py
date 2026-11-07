"""SQL level 2 (l5 to l8, review-2, homework-2): every graded key, wrong[] value and stated number, recomputed.
Written by the second reader (session V). Method one runs SQL in CPython's sqlite3 on tables built from the canvas data;
method two recomputes in plain Python. The app runs SQLite 3.39.0 (Pyodide 0.27.7); the SQLite-specific results here
(bare columns beside MIN/MAX, tie order) were also confirmed on 3.39.0, 3.45.1 and 3.53.1 by the reader.
A check that fails because the content is wrong stays failing: see docs/reviews/review-sql-1-3.md."""
import os, sys, sqlite3, datetime, statistics
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("sql", 2)
print('sqlite', sqlite3.sqlite_version)
F = lv.files


def node(fid, path):
    n = F[fid]
    for part in path.split('.'):
        k, i = part.split('[')
        n = n[k][int(i[:-1])]
    return n


def num(v):
    if v == 'NULL':
        return None
    for t in (int, float):
        try:
            return t(v)
        except ValueError:
            pass
    return v


def build(fid, path, name):
    p = node(fid, path)['canvas']['params']
    rows = [[num(c) for c in r] for r in p['rows']]
    db = sqlite3.connect(':memory:')
    db.execute(f"CREATE TABLE {name} ({', '.join(p['columns'])})")
    db.executemany(f"INSERT INTO {name} VALUES ({', '.join('?' * len(p['columns']))})", rows)
    return db, rows


def regions(rows, pred, col):
    return sorted(f"r{i}c{col}" for i, r in enumerate(rows) if pred(r))


def same_set(fid, path, want):
    got = sorted(node(fid, path)['widget']['answer'])
    lv.claim(got == sorted(want), f'{fid} {path} answer regions = {sorted(want)}', f'content has {got}')


def run_tests(src, tests):
    """Function-mode harness as in app/js/engine/widgets/code.js: one namespace, setup then eval(call) == eval(expect)."""
    g = {'__name__': '__main__'}
    exec(src, g)
    out = []
    for t in tests:
        if t.get('setup'):
            exec(t['setup'], g)
        out.append(eval(t['call'], g) == eval(t['expect'], g))
    return out


# ---- l5
d5, W = build('l5-counting-and-averaging', 'screens[0]', 'prices')
q5 = lambda s: d5.execute(s).fetchall()
closes = [r[2] for r in W]
lv.expect('l5', 'screens[0].widget.answer', f"r{closes.index(max(closes))}c2")
lv.expect('l5', 'screens[0].feedback.correct', q5("SELECT MAX(close) FROM prices")[0][0])
vol = q5("SELECT SUM(volume) FROM prices")[0][0]
lv.claim(vol == sum(r[3] for r in W) == 10600000, 'l5 SUM(volume) = 10,600,000, two ways')
lv.expect('l5', 'screens[1].feedback.correct', vol)
lv.expect('l5', 'screens[2].feedback.correct', '(5, 10600000, 120.25)')
avg = q5("SELECT AVG(close) FROM prices")[0][0]
lv.claim(abs(avg - sum(closes) / 5) < 1e-9, 'l5 AVG two ways')
lv.expect('l5', 'screens[3].widget.answer', round(avg, 2))
lv.expect('l5', 'screens[3].hints[1].text', round(sum(closes), 2))
lv.expect('l5', 'screens[3].widget.wrong[0].value', round(sum(closes), 2))
lv.expect('l5', 'screens[3].widget.wrong[1].value', statistics.median(closes))
lv.expect('l5', 'screens[3].widget.wrong[2].value', round(sum(closes) / 4, 2))
same_set('l5-counting-and-averaging', 'screens[5]', regions(W, lambda r: r[2] > 119, 3))
lv.expect('l5', 'screens[5].feedback.correct', q5("SELECT SUM(volume) FROM prices WHERE close > 119")[0][0])
d5n, Wn = build('l5-counting-and-averaging', 'screens[6]', 'prices')
known = [r[2] for r in Wn if r[2] is not None]
a = d5n.execute("SELECT AVG(close) FROM prices").fetchone()[0]
lv.claim(abs(a - sum(known) / len(known)) < 1e-9 and abs(a - 119.3875) < 1e-9, 'l5 trap AVG = 119.3875, two ways')
lv.expect('l5', 'screens[6].widget.answer', round(a, 2))
lv.expect('l5', 'screens[6].widget.wrong[0].value', round(sum(known) / 5, 2))
lv.expect('l5', 'screens[6].widget.wrong[1].value', round(sum(known), 2))
lv.claim(d5n.execute("SELECT COUNT(*), COUNT(close) FROM prices").fetchone() == (5, 4), 'l5 COUNT(*), COUNT(close) = 5, 4')
d5t, Tr = build('l5-counting-and-averaging', 'screens[9]', 'trades')
day = [r for r in Tr if r[1] == '2024-03-12']
parts = [round(r[3] * r[4], 2) for r in day]
lv.claim(parts == [23780, 10850, 59600, 17520] and round(sum(parts), 2) == 111750, 'l5 blotter values 23780 + 10850 + 59600 + 17520 = 111750')
lv.claim(d5t.execute("SELECT COUNT(*), SUM(qty), ROUND(SUM(qty * price), 2) FROM trades WHERE date = '2024-03-12'").fetchone() == (4, 13700, 111750.0), 'l5 blotter row')
lv.claim(q5("SELECT COUNT(*) FROM prices WHERE close > 200") == [(0,)], 'l5 quiz[0]: one row holding 0')
lv.claim(q5("SELECT SUM(volume) FROM prices WHERE close > 200") == [(None,)], 'l5 quiz[1]: one row holding NULL')
lv.expect('l5', 'quiz[2].widget.answer', 600 / 5)
lv.expect('l5', 'quiz[2].widget.wrong[0].value', 600 / 8)
lv.claim(q5("SELECT ROUND(AVG(close), 1) FROM prices") == [(119.0,)], 'l5 quiz[3]: ROUND(AVG(close), 1) = 119.0')
t5 = node('l5-counting-and-averaging', 'screens[4]')['widget']
lv.claim_text('l5', 'screens[4].widget.how', 'Tests after the first add rows to a copy of the data.',
              not any('DELETE' in (t.get('setup') or '') for t in t5['tests']), 'l5 screens[4] how: tests only add rows (finding 14)')

# ---- l6
d6, G = build('l6-per-group', 'screens[0]', 'prices')
q6 = lambda s: d6.execute(s).fetchall()
same_set('l6-per-group', 'screens[0]', regions(G, lambda r: r[1] == 'BARC', 2))
barc = [r[2] for r in G if r[1] == 'BARC']
lv.claim(round(sum(barc), 2) == 6.45 and round(sum(barc) / 3, 2) == 2.15, 'l6 BARC 6.45 / 3 = 2.15')
lv.expect('l6', 'screens[1].widget.options[0].text', len(q6("SELECT ticker, AVG(close) FROM prices GROUP BY ticker")))
same_set('l6-per-group', 'screens[2]', regions(G, lambda r: r[1] == 'SHEL' and r[0] >= '2024-03-12', 3))
lv.expect('l6', 'screens[2].feedback.correct', q6("SELECT SUM(volume) FROM prices WHERE date >= '2024-03-12' AND ticker = 'SHEL'")[0][0])
azn = [r[2] for r in G if r[1] == 'AZN']
lv.expect('l6', 'screens[3].widget.answer', round(sum(azn) / 3, 2))
lv.expect('l6', 'screens[3].widget.wrong[0].value', int(sum(azn) / 3 * 100) / 100)
lv.expect('l6', 'screens[3].widget.wrong[1].value', round(sum(azn), 2))
lv.claim(repr(q6("SELECT AVG(close) FROM prices WHERE ticker = 'AZN'")[0][0]) == '118.36666666666667', 'l6 screens[3]: SQLite prints 118.36666666666667')
all9 = round(sum(r[2] for r in G) / 9, 2)
lv.claim(all9 == round(q6("SELECT AVG(close) FROM prices")[0][0], 2) == 48.86, 'l6 all nine closes average 48.86, two ways')
w_all = node('l6-per-group', 'screens[3]')['widget']['wrong'][2]
lv.claim(abs(w_all['value'] - all9) <= w_all['tol']['abs'], f'l6 screens[3] wrong "all" ({w_all["value"]}) is the nine-close average {all9} (finding 1)',
         'the value does not come from averaging all nine closes')
dt, T1 = build('l6-per-group', 'screens[5]', 'trades')
n = len(dt.execute("SELECT date, ticker, COUNT(*) FROM trades GROUP BY date, ticker").fetchall())
lv.claim(n == len({(r[1], r[2]) for r in T1}) == 3, 'l6 screens[5]: 3 groups, two ways')
lv.expect('l6', 'screens[5].widget.answer', n)
lv.expect('l6', 'screens[5].widget.wrong[0].value', len({r[1] for r in T1}) * len({r[2] for r in T1}))
lv.expect('l6', 'screens[5].widget.wrong[2].value', len(T1))
trap = dict((t, d) for t, d, _ in q6("SELECT ticker, date, AVG(close) FROM prices GROUP BY ticker"))
lv.claim(trap['AZN'] == '2024-03-11', 'l6 trap: this SQLite prints 11 March beside AZN')
# SQLite rule: with a lone MIN() or MAX(), bare columns come from the row that holds it (sqlite.org/lang_select.html, "bare aggregate").
mx = {t: max(r[2] for r in G if r[1] == t) for t in {r[1] for r in G}}
maxrow = {r[1]: r[0] for r in G if r[2] == mx[r[1]]}           # date of each ticker's highest close, by hand
bare = dict((t, d) for t, d, _ in q6("SELECT ticker, date, MAX(close) FROM prices GROUP BY ticker"))
lv.claim_text('l6', 'screens[7].widget.options[1].text', 'MAX(close)', bare != maxrow,
              'l6 screens[7]: bare date beside MAX(close) is arbitrary (finding 3)')
mv = {t: max(r[3] for r in G if r[1] == t) for t in {r[1] for r in G}}
maxvol = {r[1]: r[2] for r in G if r[3] == mv[r[1]]}           # close on each ticker's highest-volume day, by hand
bare_c = dict((t, c) for t, c, _ in q6("SELECT ticker, close, MAX(volume) FROM prices GROUP BY ticker"))
lv.claim_text('l6', 'quiz[3].widget.options[0].text', 'MAX(volume)', bare_c != maxvol,
              'l6 quiz[3]: no rule picks the bare close beside MAX(volume) (finding 3)')
lv.claim(all(d == '2024-03-13' for (_, d) in q6("SELECT ticker, MAX(date) FROM prices GROUP BY ticker")), 'l6 screens[8]: MAX(date) = 2024-03-13 for each ticker')
lv.expect('l6', 'quiz[0].widget.answer', 4)
lv.expect('l6', 'quiz[2].widget.answer', 5 * 4 - 2)
lv.expect('l6', 'quiz[2].widget.wrong[0].value', 5 * 4)
lv.expect('l6', 'quiz[2].widget.wrong[1].value', 5 + 4)

# ---- l7
d7, X = build('l7-filtering-groups', 'screens[0]', 'trades')
q7 = lambda s: d7.execute(s).fetchall()
cnt = dict(q7("SELECT ticker, COUNT(*) FROM trades GROUP BY ticker"))
lv.claim(cnt == {'AZN': 4, 'BARC': 3, 'SHEL': 2}, 'l7 counts AZN 4, BARC 3, SHEL 2')
same_set('l7-filtering-groups', 'screens[0]', regions(X, lambda r: cnt[r[1]] > 3, 1))
try:
    q7("SELECT ticker, COUNT(*) FROM trades WHERE COUNT(*) > 3 GROUP BY ticker"); msg = ''
except sqlite3.OperationalError as e:
    msg = str(e)
lv.expect('l7', 'screens[1].feedback.correct', msg)
lv.claim(q7("SELECT ticker, COUNT(*) FROM trades GROUP BY ticker HAVING COUNT(*) > 3") == [('AZN', 4)], "l7 screens[2]: [('AZN', 4)]")
n = len(q7("SELECT ticker, COUNT(*) FROM trades WHERE qty >= 300 GROUP BY ticker HAVING COUNT(*) >= 2"))
lv.expect('l7', 'screens[3].widget.answer', n)
lv.expect('l7', 'screens[3].widget.wrong[0].value', len(q7("SELECT ticker FROM trades GROUP BY ticker HAVING COUNT(*) >= 2")))
av = dict(q7("SELECT ticker, AVG(qty) FROM trades GROUP BY ticker"))
lv.claim(av['AZN'] == 237.5 == (200 + 500 + 100 + 150) / 4, 'l7 AZN average 237.5, two ways')
lv.claim(dict(q7("SELECT ticker, AVG(qty) FROM trades WHERE qty > 250 GROUP BY ticker"))['AZN'] == 500, 'l7 trap: WHERE lifts AZN to 500')
lv.claim([t for (t,) in q7("SELECT ticker FROM trades GROUP BY ticker HAVING AVG(qty) > 250 ORDER BY ticker")] == ['BARC', 'SHEL'], 'l7 trap: BARC and SHEL')
st = node('l7-filtering-groups', 'screens[8]')['widget']['starter']
lv.claim('counts = {"AZN": 24, "BARC": 31, "SHEL": 20, "HSBA": 12}' in st, 'l7 screens[8] starter counts match the canvas 24, 31, 20, 12')
tot = dict(q7("SELECT ticker, SUM(qty) FROM trades GROUP BY ticker"))
lv.claim(tot == {'AZN': 950, 'BARC': 16000, 'SHEL': 700}, 'l7 quiz[1] totals 950, 16000, 700')
lv.expect('l7', 'quiz[1].widget.answer', len(q7("SELECT ticker FROM trades GROUP BY ticker HAVING SUM(qty) > 1000")))
slip = len(q7("SELECT ticker FROM trades WHERE qty > 1000 GROUP BY ticker"))
lv.claim_text('l7', 'quiz[1].feedback.byKey.fills', 'You tested single fills against 1,000', slip == 2,
              f'l7 quiz[1] "fills" slip (WHERE qty > 1000) gives 2 rows: it gives {slip} (finding 11)')
lv.expect('l7', 'quiz[3].widget.answer', len(q7("SELECT ticker FROM trades WHERE qty < 1000 GROUP BY ticker HAVING COUNT(*) >= 2")))

# ---- l8
d8, Y = build('l8-daily-volume', 'screens[0]', 'trades')
q8 = lambda s: d8.execute(s).fetchall()
same_set('l8-daily-volume', 'screens[0]', regions(Y, lambda r: r[1] == '2024-03-12' and r[2] == 'AZN', 3))
vols = {(d, t): v for d, t, v in q8("SELECT date, ticker, SUM(qty) FROM trades GROUP BY date, ticker")}
lv.claim(vols == {('2024-03-12', 'AZN'): 700, ('2024-03-12', 'BARC'): 13000, ('2024-03-13', 'AZN'): 800, ('2024-03-13', 'BARC'): 6000}, 'l8 daily volumes 700, 13000, 800, 6000')
lv.expect('l8', 'screens[1].widget.answer', vols[('2024-03-13', 'AZN')])
lv.expect('l8', 'screens[1].widget.wrong[0].value', sum(r[3] for r in Y if r[2] == 'AZN'))
vals = {(d, t): v for d, t, v in q8("SELECT date, ticker, ROUND(SUM(qty * price), 2) FROM trades GROUP BY date, ticker")}
lv.claim(max(vals, key=vals.get) == ('2024-03-13', 'AZN'), 'l8 screens[3]: AZN on 13 March is the biggest day in pounds')
lv.expect('l8', 'screens[4].explain.text', vals[('2024-03-12', 'AZN')])
azn12 = [(r[3], r[4]) for r in Y if r[1] == '2024-03-12' and r[2] == 'AZN']
lv.claim(round(sum(q for q, _ in azn12) * sum(p for _, p in azn12) / 2, 2) == 83335, 'l8 SUM(qty) * AVG(price) = 83,335')
lv.expect('l8', 'screens[4].widget.options[1].why', 83335)
lv.expect('l8', 'screens[4].widget.options[2].why', round(sum(p for _, p in azn12), 2))
vw = q8("SELECT SUM(qty * price) / SUM(qty) FROM trades WHERE date = '2024-03-12' AND ticker = 'AZN'")[0][0]
lv.expect('l8', 'screens[5].widget.answer', round(vw, 2))
lv.expect('l8', 'screens[5].widget.wrong[0].value', round(sum(p for _, p in azn12) / 2, 2))
dp, Pz = build('l8-daily-volume', 'screens[6]', 'prices')
lagv = {(t, d): l for d, t, l in dp.execute("SELECT date, ticker, LAG(close) OVER (PARTITION BY ticker ORDER BY date) FROM prices")}
lv.claim(lagv[('BARC', '2024-03-13')] == 2.18 and lagv[('AZN', '2024-03-11')] is None, 'l8 LAG: BARC 13 March sees 2.18; first rows NULL')
lv.expect('l8', 'screens[6].widget.answer', 'r4c2')
lv.expect('l8', 'screens[6].explain.text', round((2.15 / 2.18 - 1) * 100, 2))
tv = dict(q8("SELECT ticker, ROUND(SUM(qty * price), 2) FROM trades GROUP BY ticker"))
lv.claim(tv == {'AZN': 177550.0, 'BARC': 41330.0}, 'l8 screens[9]: AZN 177,550, BARC 41,330')
lv.claim(round(100000 * 2.20, 2) == 220000, 'l8 screens[9] test 3: a £220,000 fill')
lv.expect('l8', 'quiz[0].widget.answer', round(5000 * 2.17 + 8000 * 2.19, 2))
lv.expect('l8', 'quiz[0].widget.wrong[0].value', round(13000 * 2.18, 2))
lv.expect('l8', 'quiz[0].feedback.byKey.avg', round(5000 * 2.17 + 8000 * 2.19 - 13000 * 2.18))
lv.expect('l8', 'quiz[3].widget.answer', round(2.15 / 2.18 - 1, 4))
lv.claim(abs((2.18 / 2.15 - 1) - 0.014) <= 0.0002, 'l8 quiz[3] flipped 0.014 within its tolerance')

# ---- review-2
lv.expect('review', 'items[1].widget.answer', 3 * 5)
lv.expect('review', 'items[3].widget.answer', 300 * 26.00 + 100 * 26.40)
lv.expect('review', 'items[3].widget.wrong[0].value', round(400 * (26.00 + 26.40) / 2, 2))
lv.expect('review', 'items[3].feedback.byKey.avg', round(400 * 26.20 - (300 * 26.00 + 100 * 26.40)))
lv.expect('review', 'items[4].widget.answer', (10 + 12 + 14) / 3)
lv.expect('review', 'items[4].widget.wrong[0].value', (10 + 12 + 14) / 4)
r2, _ = build('review-2', 'items[5]', 'prices')
avgv = dict(r2.execute("SELECT ticker, ROUND(AVG(volume)) FROM prices GROUP BY ticker").fetchall())
lv.claim(avgv == {'BARC': 43666667.0, 'SHEL': 9200000.0, 'AZN': 2200000.0}, 'review-2 items[5] average volumes')
lv.expect('review', 'items[6].feedback.byKey.test-2', round((19.50 + 20.60) / 2, 2))
lv.expect('review', 'items[6].feedback.byKey.test-3', round((19.90 + 20.05) / 2, 3))
lag_cross = r2.execute("SELECT ticker, date, LAG(close) OVER (ORDER BY ticker, date) FROM prices").fetchall()
prev = [l for t, d, l in lag_cross if t == 'BARC' and d == '2024-03-11'][0]
lv.claim(prev == 117.6 and round((2.12 / prev - 1) * 100) == -98, 'review-2 items[7]: prev 117.60, return about -98%')

# ---- homework-2
lv.expect('homework', 'items[1].widget.answer', 4 + 3 + 2)
lv.expect('homework', 'items[1].widget.wrong[0].value', 4 * 3)
h2 = node('homework-2', 'items[2]')['widget']
res = run_tests(h2['solution'], h2['tests'])
lv.claim(all(res), 'homework-2 items[2]: the solution passes its tests here')
g = {}; exec(h2['solution'].split('def query')[0], g)
db2 = g['db']; db2.execute("INSERT INTO trades VALUES (200, '2024-03-12', 'HSBA', 5000, 6.45)")
counts = dict(db2.execute("SELECT ticker, COUNT(*) FROM trades GROUP BY ticker HAVING COUNT(*) > 20").fetchall())
tie = len(set(counts.values())) < len(counts)
lv.claim_text('homework', 'items[2].widget.solution', 'HAVING COUNT(*) > 20\nORDER BY COUNT(*) DESC\n"""', not tie,
              f'homework-2 items[2] test 2: no tie at the sort key (counts {counts}) (finding 2)')
fixed_sol = h2['solution'].replace('ORDER BY COUNT(*) DESC\n', 'ORDER BY COUNT(*) DESC, ticker\n')
fixed_tests = [dict(t) for t in h2['tests']]
fixed_tests[1]['expect'] = "[('BARC', 35, 300.0), ('AZN', 22, 286.4), ('HSBA', 21, 523.8), ('SHEL', 21, 290.5)]"
lv.claim(all(run_tests(fixed_sol, fixed_tests)) and not any(run_tests(h2['starter'], fixed_tests)), 'homework-2 items[2] proposed fix: tie-break solution passes, starter fails')
for t, c, a in [('AZN', 22, 286.4), ('BARC', 35, 300.0), ('SHEL', 21, 290.5)]:
    qs = [100 * (k % 5 + 1) for k in range(c)]
    lv.claim(round(sum(qs) / c, 1) == a, f'homework-2 items[2]: {t} averages {a}')
lv.claim(round((20 * 300 + 5000) / 21, 1) == 523.8, 'homework-2 items[2] test 2: HSBA averages 523.8')
cl = {'AZN': [118.40, 119.10, 117.60], 'BARC': [2.12, 2.18, 2.15], 'SHEL': [25.80, 26.05, 26.30]}
rets = {t: [round(v[i] / v[i - 1] - 1, 4) for i in (1, 2)] for t, v in cl.items()}
lv.claim(rets == {'AZN': [0.0059, -0.0126], 'BARC': [0.0283, -0.0138], 'SHEL': [0.0097, 0.0096]}, 'homework-2 items[3] returns, by hand')
vw2 = (1000 * 26.00 + 3000 * 26.20 + 1000 * 26.50) / 5000
lv.expect('homework', 'items[5].widget.answer', round(vw2, 2))
lv.expect('homework', 'items[5].widget.wrong[0].value', round((26.00 + 26.20 + 26.50) / 3, 2))
lv.expect('homework', 'items[5].widget.wrong[1].value', 1000 * 26.00 + 3000 * 26.20 + 1000 * 26.50)
lv.expect('homework', 'items[6].model', round(10 / 3, 2))
lv.claim(datetime.date(2024, 3, 16).weekday() == 5, 'homework-2 items[7]: 16 March 2024 was a Saturday')
e = sqlite3.connect(':memory:'); e.execute("CREATE TABLE trades (date TEXT, qty INTEGER, price REAL)")
lv.claim(e.execute("SELECT COUNT(*), SUM(qty * price) FROM trades WHERE date = '2024-03-16'").fetchall() == [(0, None)], 'homework-2 items[7]: [(0, None)]')

lv.check_wrongs()
lv.report()
