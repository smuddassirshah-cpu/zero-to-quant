"""SQL level 3 (l9 to l12, review-3, homework-3): every graded key, wrong[] value and stated number, recomputed.
Written by the second reader (session V). SQL runs in CPython's sqlite3 on the course's make_db() tables (taken from the
content's own starter code); key counts are recomputed in plain Python too. The app runs SQLite 3.39.0 (Pyodide 0.27.7);
the SQLite-specific results (NULL primary keys, query plans, automatic indexes) were also confirmed on 3.39.0, 3.45.1 and
3.53.1 by the reader. Checks marked "proposed" verify the replacement text in docs/reviews/review-sql-1-3.md.
A check that fails because the content is wrong stays failing: see that review."""
import os, sys, io, sqlite3, tempfile, contextlib
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("sql", 3)
print('sqlite', sqlite3.sqlite_version)
F = lv.files


def node(fid, path):
    n = F[fid]
    for part in path.split('.'):
        k, i = part.split('[')
        n = n[k][int(i[:-1])]
    return n


def make_db_from(fid, path):
    src = node(fid, path)['widget']['solution']
    g = {}
    exec(src[src.index('import sqlite3'):src.index('for row in')] if 'for row in' in src else src, g)
    return g['make_db']


def run_tests(src, tests):
    g = {'__name__': '__main__'}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(src, g)
    out = []
    for t in tests:
        if t.get('setup'):
            exec(t['setup'], g)
        out.append(eval(t['call'], g) == eval(t['expect'], g))
    return out


make_db = make_db_from('l10-matching-rows', 'screens[2]')
db = make_db()
q = lambda s, p=(): db.execute(s, p).fetchall()
TR = q("SELECT id, date, ticker, qty FROM trades")
PX = q("SELECT ticker, date, close FROM prices")
SE = q("SELECT ticker, name, sector FROM securities")
close = {(t, d): c for t, d, c in PX}

# ---- l9
lv.expect('l9', 'screens[1].widget.answer', 3)
lv.expect('l9', 'screens[1].explain.text', 5 * 252)
lv.expect('l9', 'screens[3].widget.options[1].text', len(q("SELECT close FROM prices WHERE ticker = 'BP'")))
lv.claim([t for (t,) in q("SELECT ticker FROM securities WHERE sector = 'Banks'")] == ['BARC', 'HSBA'], 'l9 screens[6]: BARC and HSBA')
lv.claim(sorted(c for (c,) in q("SELECT close FROM prices WHERE date = '2026-03-04' AND ticker IN (SELECT ticker FROM securities WHERE sector = 'Banks')")) == [2.51, 8.69], 'l9 screens[6]: 2.51 and 8.69')
lv.claim([i for (i,) in q("SELECT id FROM trades WHERE ticker IN (SELECT ticker FROM securities WHERE sector = 'Banks') ORDER BY id")] == [1, 4, 6], 'l9 screens[9]: trades 1, 4, 6')
n = q("SELECT COUNT(*) FROM prices WHERE ticker IN (SELECT ticker FROM securities WHERE sector <> 'Banks')")[0][0]
lv.claim(n == sum(1 for t, d, c in PX if t not in ('BARC', 'HSBA')) == 12, 'l9 quiz[2]: 12, two ways')
lv.expect('l9', 'quiz[2].widget.answer', n)
lv.expect('l9', 'quiz[2].widget.wrong[0].value', 4)
lv.expect('l9', 'quiz[2].widget.wrong[1].value', 6)
lv.expect('l9', 'quiz[2].widget.wrong[2].value', len(PX))
lv.expect('l9', 'quiz[3].widget.options[2].text', 2000 * 1260)
try:
    q("INSERT INTO prices VALUES ('BP', '2026-03-04', 4.40)"); dup = ''
except sqlite3.IntegrityError as e:
    dup = str(e)
lv.claim(dup == 'UNIQUE constraint failed: prices.ticker, prices.date', 'l9 screens[8]: the UNIQUE message')
nk = make_db()
nk.execute("INSERT INTO securities VALUES (NULL, 'Mystery', 'Banks')"); nk.execute("INSERT INTO securities VALUES (NULL, 'Mystery 2', 'Banks')")
null_keys = nk.execute("SELECT COUNT(*) FROM securities WHERE ticker IS NULL").fetchone()[0]
lv.claim_text('l9', 'screens[8].explain.text', 'SQLite always enforces a primary key,', null_keys == 0,
              f'l9 screens[8]: SQLite always enforces a primary key; it stored {null_keys} NULL tickers (finding 7)')
lv.claim_text('l9', 'summary.formula.note', 'SQLite always enforces a primary key;', null_keys == 0, 'l9 summary note: same claim (finding 7)')

# ---- l10
lv.expect('l10', 'screens[1].widget.answer', len(q("SELECT t.id, s.name FROM trades AS t JOIN securities AS s ON t.ticker = s.ticker")))
lv.expect('l10', 'screens[1].widget.wrong[1].value', len(TR) * len(SE))
lv.expect('l10', 'screens[1].widget.wrong[2].value', len({r[2] for r in TR}))
n = len(q("SELECT t.id FROM trades AS t JOIN prices AS p ON t.ticker = p.ticker"))
lv.claim(n == sum(sum(1 for p in PX if p[0] == t[2]) for t in TR) == 21, 'l10 half key: 21, two ways')
lv.expect('l10', 'screens[3].widget.answer', n)
lv.expect('l10', 'screens[3].widget.wrong[1].value', len(PX))
lv.expect('l10', 'screens[3].widget.wrong[2].value', len(TR) * len(PX))
lv.claim(q("SELECT COUNT(*) FROM trades JOIN securities") == [(42,)], 'l10 trap: no ON gives 42 in SQLite')
lv.claim(len(q("SELECT * FROM trades AS t JOIN prices AS p ON t.date = p.date")) == 42, 'l10 screens[5]: date alone gives 42')
lv.claim(len(q("SELECT * FROM trades AS t JOIN prices AS p ON t.id = p.ticker")) == 0, 'l10 screens[5]: id = ticker gives 0')
vals = [v for _, v in q("SELECT t.id, ROUND(t.qty * p.close, 2) FROM trades AS t JOIN prices AS p ON t.ticker = p.ticker AND t.date = p.date ORDER BY t.id")]
lv.claim(vals == [round(t[3] * close[(t[2], t[1])], 2) for t in TR] == [2480.0, 5420.0, 5575.0, -1012.0, 6525.0, 5214.0, -2740.0], 'l10 screens[6] values, two ways')
lv.expect('l10', 'screens[7].prose', 2000 * 1260)
lv.expect('l10', 'screens[7].widget.options[0].text', 1260)
lv.expect('l10', 'screens[8].widget.options[3].text', 7 * 6 * 18)
expo = dict(q("SELECT s.sector, ROUND(SUM(t.qty * p.close), 2) FROM trades AS t JOIN securities AS s ON t.ticker = s.ticker JOIN prices AS p ON p.ticker = t.ticker AND p.date = '2026-03-04' GROUP BY s.sector"))
lv.claim(expo == {'Banks': 6720.0, 'Energy': 9265.0, 'Health': 5490.0}, 'l10 screens[9] exposures')
lv.claim(round((1000 - 400) * 2.51 + 600 * 8.69, 2) == 6720, 'l10 screens[9] explain: Banks by hand')
lv.expect('l10', 'quiz[0].widget.answer', len(TR) * len(PX))
lv.expect('l10', 'quiz[0].widget.wrong[0].value', len(TR) + len(PX))
lv.expect('l10', 'quiz[1].widget.options[0].text', 40 * 5)
lv.expect('l10', 'quiz[2].widget.answer', len(q("SELECT t.id FROM trades AS t JOIN securities AS s ON t.ticker = s.ticker WHERE t.ticker = s.name")))
lv.claim(len(q("SELECT t.id FROM trades AS t JOIN securities AS s ON t.ticker = s.name")) == 1, 'l10 quiz[2]: 1 row')
plan = [r[-1] for r in db.execute("EXPLAIN QUERY PLAN SELECT close FROM prices WHERE ticker = 'BP'")]
nokey = sqlite3.connect(':memory:'); nokey.execute("CREATE TABLE prices (ticker TEXT, date TEXT, close REAL)")
lv.claim([r[-1] for r in nokey.execute("EXPLAIN QUERY PLAN SELECT close FROM prices WHERE ticker = 'BP'")] == ['SCAN prices'], 'l10 screens[7]: a table with no key plans SCAN prices')
lv.claim_text('l10', 'screens[7].prose', 'A real `prices` table holds 2,000 tickers', plan[0].startswith('SCAN'),
              f'l10 screens[7]: a (ticker, date)-keyed prices table plans {plan} (finding 8)')

# ---- l11
lj = q("SELECT s.ticker, t.id FROM securities AS s LEFT JOIN trades AS t ON s.ticker = t.ticker")
lv.claim(len(lj) == len(TR) + sum(1 for s in SE if s[0] not in {t[2] for t in TR}) == 8, 'l11 left join: 8, two ways')
lv.expect('l11', 'screens[1].widget.answer', len(lj))
lv.claim(('VOD', None) in lj, 'l11 screens[2]: VOD arrives with None')
lv.claim(q("SELECT s.ticker FROM securities AS s LEFT JOIN trades AS t ON s.ticker = t.ticker WHERE t.id IS NULL") == [('VOD',)], 'l11 screens[3]: VOD')
lv.claim(len(q("SELECT s.ticker, t.id FROM securities AS s LEFT JOIN trades AS t ON s.ticker = t.ticker WHERE t.date = '2026-03-04'")) == 3, 'l11 trap: 3 rows')
on = q("SELECT s.ticker, t.id FROM securities AS s LEFT JOIN trades AS t ON s.ticker = t.ticker AND t.date = '2026-03-04' ORDER BY s.ticker")
lv.claim(on == [('AZN', None), ('BARC', None), ('BP', 5), ('HSBA', 6), ('SHEL', 7), ('VOD', None)], 'l11 screens[5]: date in ON keeps all 6')
lv.claim(len(q("SELECT s.ticker, t.id FROM securities AS s LEFT JOIN trades AS t ON s.ticker = t.ticker WHERE t.date = '2026-03-04' OR t.date IS NULL")) == 4, 'l11 screens[5] ornull: 4 rows')
cnt = dict(q("SELECT s.ticker, COUNT(*) FROM securities AS s LEFT JOIN trades AS t ON s.ticker = t.ticker GROUP BY s.ticker"))
cnt2 = dict(q("SELECT s.ticker, COUNT(t.id) FROM securities AS s LEFT JOIN trades AS t ON s.ticker = t.ticker GROUP BY s.ticker"))
lv.claim(cnt['VOD'] == 1 and cnt2['VOD'] == 0, 'l11 screens[6]: COUNT(*) 1, COUNT(t.id) 0')
lv.expect('l11', 'screens[7].widget.answer', len(q("SELECT ticker FROM trades WHERE qty > 0 UNION SELECT ticker FROM trades WHERE qty < 0")))
lv.expect('l11', 'screens[7].widget.wrong[0].value', len(q("SELECT ticker FROM trades WHERE qty > 0 UNION ALL SELECT ticker FROM trades WHERE qty < 0")))
lv.expect('l11', 'screens[7].widget.wrong[1].value', len(q("SELECT ticker FROM trades WHERE qty > 0 INTERSECT SELECT ticker FROM trades WHERE qty < 0")))
lv.expect('l11', 'quiz[0].widget.answer', len(q("SELECT t.id FROM trades AS t LEFT JOIN securities AS s ON t.ticker = s.ticker")))
lv.expect('l11', 'quiz[3].widget.answer', len(q("SELECT ticker FROM securities UNION SELECT ticker FROM trades")))
lv.expect('l11', 'quiz[3].widget.wrong[0].value', len(SE) + len(TR))

# ---- l12
lv.claim(q("SELECT ticker, close FROM prices WHERE date = '2026-03-04' ORDER BY close DESC LIMIT 2") == [('AZN', 109.8), ('SHEL', 27.4)], 'l12 screens[0]')
d = tempfile.mkdtemp(); f = os.path.join(d, 'results.db')
c = sqlite3.connect(f)
c.execute("CREATE TABLE runs (run_id INTEGER PRIMARY KEY, strategy TEXT, sharpe REAL, pnl REAL)")
c.executemany("INSERT INTO runs VALUES (?, ?, ?, ?)", [(1, 'momentum', 0.84, 12450.0), (2, 'mean reversion', 0.37, 3120.5), (3, 'carry', 1.12, 18730.25)])
c.close()
lv.expect('l12', 'screens[4].widget.answer', sqlite3.connect(f).execute("SELECT COUNT(*) FROM runs").fetchone()[0])
lv.claim(q("SELECT p.ticker, p.date, p.close FROM prices AS p JOIN (SELECT ticker, MAX(close) AS top FROM prices GROUP BY ticker) AS m ON p.ticker = m.ticker AND p.close = m.top WHERE p.ticker = 'SHEL'") == [('SHEL', '2026-03-04', 27.4)], 'l12 screens[6]: SHEL 4 March')
sh = [-0.12, 0.41, 0.88, 1.05, 0.62]
lv.claim(round(sum(sh), 2) == 2.84 and round(sum(sh) / 5, 3) == 0.568, 'l12 screens[9]: 2.84 / 5 = 0.568')
lv.expect('l12', 'screens[9].explain.text', 0.568)
tie = make_db(); tie.execute("INSERT INTO prices VALUES ('BP', '2026-03-05', 4.35)")
lv.expect('l12', 'quiz[3].widget.answer', len(tie.execute("SELECT p.ticker FROM prices AS p JOIN (SELECT ticker, MAX(close) AS top FROM prices GROUP BY ticker) AS m ON p.ticker = m.ticker AND p.close = m.top WHERE p.ticker = 'BP'").fetchall()))
lv.expect('l12', 'quiz[0].widget.options[0].text', str(q("SELECT COUNT(*) FROM prices")))

# ---- review-3
lv.expect('review', 'items[1].widget.answer', 12 * 5)
lv.expect('review', 'items[2].widget.answer', q("SELECT COUNT(*) FROM securities AS s LEFT JOIN trades AS t ON s.ticker = t.ticker AND t.qty > 0")[0][0])
lv.expect('review', 'items[4].widget.answer', q("SELECT COUNT(*) FROM trades WHERE ticker IN (SELECT ticker FROM securities WHERE sector = 'Energy')")[0][0])
mtm = [v for _, v in q("SELECT t.id, ROUND(t.qty * (now.close - p.close), 2) FROM trades AS t JOIN prices AS p ON p.ticker = t.ticker AND p.date = t.date JOIN prices AS now ON now.ticker = t.ticker AND now.date = '2026-03-04' ORDER BY t.id")]
lv.claim(mtm == [round(t[3] * (close[(t[2], '2026-03-04')] - close[(t[2], t[1])]), 2) + 0.0 for t in TR], 'review-3 items[5] marks, two ways')
lv.expect('review', 'items[5].explain.text', -85.00)
rb = sqlite3.connect(':memory:'); rb.execute("CREATE TABLE runs (n INTEGER)")
try:
    with rb:
        for k in range(1, 251):
            if k == 180:
                raise RuntimeError('run 180 failed')
            rb.execute("INSERT INTO runs VALUES (?)", (k,))
except RuntimeError:
    pass
lv.expect('review', 'items[7].widget.answer', rb.execute("SELECT COUNT(*) FROM runs").fetchone()[0])
# review-3 items[2] (freshness fix): COUNT(*) after a left join with t.qty > 0 in ON
p_star, p_col = q("SELECT COUNT(*), COUNT(t.id) FROM securities AS s LEFT JOIN trades AS t ON s.ticker = t.ticker AND t.qty > 0")[0]
lv.claim((p_star, p_col) == (6, 5), 'review-3 items[2]: COUNT(*) 6, COUNT(t.id) 5')
r32 = node('review-3', 'items[2]')['widget']
lv.claim([w['value'] for w in r32['wrong']] == [p_col, 8, len(TR)] and [i for i, t in enumerate(TR) if t[3] < 0] == [3, 6] and 'qty > 0' in lv.text('review', 'items[2].prose'),
         'review-3 items[2]: wrong values 5 (COUNT(t.id)), 8 (no qty test), 7 (all trades); trades 4 and 7 are sales')
lv.claim(q("SELECT COUNT(*) FROM securities AS s LEFT JOIN trades AS t ON s.ticker = t.ticker")[0][0] == 8, 'review-3 items[2]: 8 without the qty test')
# proposed replacement for review-3 items[3] (freshness): placeholders feeding IN
sql = "SELECT ticker, close FROM prices WHERE date = ? AND ticker IN (?, ?) ORDER BY ticker"
lv.claim(q(sql, ("2026-03-04", "BP", "SHEL")) == [('BP', 4.35), ('SHEL', 27.4)], 'review-3 items[3]: right call')
lv.claim(q(sql, ("BP", "SHEL", "2026-03-04")) == [], 'review-3 items[3]: values out of order find nothing')
try:
    q(sql, ("2026-03-04", "BP, SHEL")); err = ''
except sqlite3.ProgrammingError as e:
    err = str(e)
lv.claim(err.startswith('Incorrect number of bindings supplied'), 'review-3 items[3]: one text for two ? raises the bindings error')

# ---- homework-3
h0 = node('homework-3', 'items[0]')['widget']
lv.claim(all(run_tests(h0['solution'], h0['tests'])), 'homework-3 items[0]: the content solution passes its tests here')
lv.claim('GROUP BY p.ticker, p.close\n' in h0['solution'] and 'GROUP BY p.ticker\n' not in h0['solution'] and not any(run_tests(h0['starter'], h0['tests'])),
         'homework-3 items[0]: the solution groups by p.close (no bare column), passes every test incl. the tie; starter fails (finding 5)')
lv.expect('homework', 'items[0].explain.text', 111.50)
ex = make_db_from('homework-3', 'items[1]')()
qx = lambda s: ex.execute(s).fetchall()
full = qx("SELECT s.sector, ROUND(COALESCE(SUM(t.qty * p.close), 0), 2) FROM securities AS s LEFT JOIN trades AS t ON t.ticker = s.ticker LEFT JOIN prices AS p ON p.ticker = s.ticker AND p.date = '2026-03-04' GROUP BY s.sector ORDER BY s.sector")
lv.claim(full == [('Banks', 6720.0), ('Energy', 9265.0), ('Health', 5490.0), ('Telecoms', 0.0)], 'homework-3 items[1] exposures')
where = qx("SELECT s.sector FROM securities AS s LEFT JOIN trades AS t ON t.ticker = s.ticker LEFT JOIN prices AS p ON p.ticker = s.ticker WHERE p.date = '2026-03-04' GROUP BY s.sector")
ex2 = make_db_from('homework-3', 'items[1]')(); ex2.execute("INSERT INTO securities VALUES ('LLOY', 'Lloyds', 'Retail')")
where2 = ex2.execute("SELECT s.sector FROM securities AS s LEFT JOIN trades AS t ON t.ticker = s.ticker LEFT JOIN prices AS p ON p.ticker = s.ticker WHERE p.date = '2026-03-04' GROUP BY s.sector").fetchall()
lv.claim(('Telecoms',) in where and ('Retail',) not in where2 and 'drop a sector with no close that day, such as test 3' in lv.text('homework', 'items[1].explain.text') and 'drop Telecoms' not in lv.text('homework', 'items[1].explain.text'),
         'homework-3 items[1]: a WHERE date test keeps Telecoms but drops test 3 Retail (finding 4)')
# homework-3 items[4] (freshness fix): a range condition in ON
rng = len(q("SELECT t.id FROM trades AS t JOIN prices AS p ON t.ticker = p.ticker AND p.date <= t.date"))
lv.claim(rng == sum(sum(1 for p in PX if p[0] == t[2] and p[1] <= t[1]) for t in TR) == 15 == 1 + 1 + 2 + 2 + 3 + 3 + 3, 'homework-3 items[4]: 15, two ways')
lv.expect('homework', 'items[4].widget.answer', rng)
h34 = node('homework-3', 'items[4]')['widget']
lv.claim([w['value'] for w in h34['wrong']] == [len(TR), len(q("SELECT t.id FROM trades AS t JOIN prices AS p ON t.date = p.date")) // 2] == [7, 21] and set(node('homework-3', 'items[4]')['feedback']['byKey']) == {'seven', 'half'},
         'homework-3 items[4]: wrong values 7 (one per trade) and 21 (half of the date-only 42); byKey matches')
h5 = node('homework-3', 'items[5]')['widget']
lv.claim(all(run_tests(h5['solution'], h5['tests'])), 'homework-3 items[5]: solution passes')
nx = sqlite3.connect(':memory:')
nx.executescript("CREATE TABLE prices (ticker TEXT, date TEXT, close REAL); CREATE TABLE trades (id INTEGER PRIMARY KEY, date TEXT, ticker TEXT, qty INTEGER);")
jplan = [r[-1] for r in nx.execute("EXPLAIN QUERY PLAN SELECT * FROM trades AS t JOIN prices AS p ON p.ticker = t.ticker AND p.date = t.date")]
jplan = [x for x in jplan if not x.startswith('BLOOM')]   # 3.53 adds a bloom-filter step; 3.39.0 does not
lv.claim(jplan == ['SCAN t', 'SEARCH p USING AUTOMATIC COVERING INDEX (ticker=? AND date=?)'] and 'SEARCH p USING AUTOMATIC COVERING INDEX' in lv.text('homework', 'items[7].prose') and 'SCAN p' not in lv.text('homework', 'items[7].prose'),
         f'homework-3 items[7]: SQLite plans {jplan} for an unindexed join (finding 6)')
lv.expect('homework', 'items[7].prose', 2520000)
nx.execute("CREATE INDEX idx_px ON prices (ticker, date)")
lv.claim([r[-1] for r in nx.execute("EXPLAIN QUERY PLAN SELECT * FROM trades AS t JOIN prices AS p ON p.ticker = t.ticker AND p.date = t.date")] == ['SCAN t', 'SEARCH p USING INDEX idx_px (ticker=? AND date=?)'], 'homework-3 items[7]: idx_px turns it into a stored-index SEARCH')

lv.check_wrongs()
lv.report()
