"""SQL level 1 (l1 to l4, review-1, homework-1): every graded key, wrong[] value and stated number, recomputed.
Written by the second reader (session V). Method one runs the stated SQL in CPython's sqlite3 on tables built from the
canvas data; method two recounts in plain Python. The app runs SQLite 3.39.0 (Pyodide 0.27.7); this script prints the
local version, and every result below was also confirmed on SQLite 3.39.0, 3.45.1 and 3.53.1 by the reader.
A check that fails because the content is wrong stays failing: see docs/reviews/review-sql-1-3.md."""
import os, sys, json, sqlite3
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("sql", 1)
print('sqlite', sqlite3.sqlite_version)
F = lv.files


def table(fid, path):
    """Return (columns, rows) of a table canvas at screens[i] / quiz[i] / items[i]."""
    node = F[fid]
    for part in path.split('.'):
        k, i = part.split('[')
        node = node[k][int(i[:-1])]
    p = node['canvas']['params']
    return p['columns'], p['rows']


def num(v):
    if v == 'NULL':
        return None
    try:
        return int(v)
    except ValueError:
        try:
            return float(v)
        except ValueError:
            return v


def build(cols, rows, name='prices'):
    db = sqlite3.connect(':memory:')
    db.execute(f"CREATE TABLE {name} ({', '.join(cols)})")
    db.executemany(f"INSERT INTO {name} VALUES ({', '.join('?' * len(cols))})", [[num(c) for c in r] for r in rows])
    return db


def regions(rows, pred, col):
    return sorted(f"r{i}c{col}" for i, r in enumerate(rows) if pred([num(c) for c in r]))


def widget(fid, path):
    node = F[fid]
    for part in path.split('.'):
        k, i = part.split('[')
        node = node[k][int(i[:-1])]
    return node['widget']


def same_set(fid, path, want, label):
    got = sorted(widget(fid, path)['answer'])
    lv.claim(got == sorted(want), f'{fid} {path} answer regions = {sorted(want)}', f'content has {got}')


def wrong_set(fid, path, wid, want):
    w = [x for x in widget(fid, path).get('wrong', []) if x.get('id') == wid][0]
    lv.claim(sorted(w['set']) == sorted(want), f'{fid} {path} wrong "{wid}" set = {sorted(want)}', f'content has {sorted(w["set"])}')


cols, P12 = table('l1-choosing-columns', 'screens[0]')
db = build(cols, P12)
q = lambda s: db.execute(s).fetchall()
T = [[num(c) for c in r] for r in P12]          # plain-Python copy: date, ticker, close, volume

# ---- l1
lv.expect('l1', 'screens[0].widget.answer', 'r6c2')
lv.claim([i for i, r in enumerate(T) if r[0] == '2026-03-03' and r[1] == 'SHEL'] == [6], 'l1 SHEL 3 March is row 6')
lv.expect('l1', 'screens[0].feedback.correct', 26.51)
cur = db.execute("SELECT ticker, close FROM prices")
lv.claim((len(cur.fetchall()), len(cur.description)) == (12, 2), 'l1 screens[1]: 12 rows and 2 columns')
lv.expect('l1', 'screens[1].widget.options[0].text', '12 rows and 2 columns')
lv.claim(q("SELECT close, ticker FROM prices")[0] == (2.15, 'BARC'), "l1 screens[2]: first tuple (2.15, 'BARC')")
lv.expect('l1', 'screens[2].widget.options[0].text', "(2.15, 'BARC')")
n = len(q("SELECT DISTINCT ticker FROM prices"))
lv.claim(n == len({r[1] for r in T}) == 4, 'l1 DISTINCT ticker = 4, two ways')
lv.expect('l1', 'screens[5].widget.answer', n)
lv.expect('l1', 'screens[5].widget.wrong[0].value', len(T))
lv.expect('l1', 'screens[5].widget.wrong[1].value', len({r[0] for r in T}))
n = len(q("SELECT DISTINCT ticker, date FROM prices"))
lv.claim(n == len({(r[1], r[0]) for r in T}) == 12, 'l1 trap: DISTINCT ticker, date = 12, two ways')
lv.expect('l1', 'screens[6].widget.options[0].text', 12)
lv.expect('l1', 'screens[7].explain.text', len(q("SELECT DISTINCT date FROM prices")))
lv.expect('l1', 'quiz[1].widget.answer', len(q("SELECT DISTINCT date FROM prices")))
lv.claim(q("SELECT volume AS shares, ticker FROM prices")[0] == (412000, 'BARC'), "l1 quiz[2]: (412000, 'BARC')")
tc, tr = table('l1-choosing-columns', 'quiz[3]')
tdb = build(tc, tr, 'trades')
n = len(tdb.execute("SELECT DISTINCT ticker, side FROM trades").fetchall())
lv.claim(n == len({(r[0], r[1]) for r in tr}) == 4, 'l1 quiz[3]: 4 pairs, two ways')
lv.expect('l1', 'quiz[3].widget.answer', n)
lv.expect('l1', 'quiz[3].widget.wrong[0].value', len({r[0] for r in tr}))
lv.expect('l1', 'quiz[3].widget.wrong[1].value', len({r[1] for r in tr}))
lv.expect('l1', 'quiz[3].widget.wrong[2].value', len(tr))
# Claim: rows come back in stored order "because nothing asks for another order". SQL promises no order without ORDER BY;
# l3 screens[6] and quiz[0] say so. SQLite happens to scan a plain table in rowid order.
lv.claim_text('l1', 'screens[2].explain.text', 'Rows come back in the order they are stored, because nothing asks for another order', False,
              'l1 screens[2] explain states storage order as an SQL rule (finding 10)')

# ---- l2
same_set('l2-filtering-rows', 'screens[0]', regions(P12, lambda r: r[2] > 4, 2), 'close > 4')
lv.claim(len(q("SELECT * FROM prices WHERE close > 4")) == 6, 'l2 close > 4 keeps 6')
same_set('l2-filtering-rows', 'screens[1]', regions(P12, lambda r: r[3] > 500000, 3), 'volume > 500000')
same_set('l2-filtering-rows', 'screens[3]', regions(P12, lambda r: r[1] == 'BARC' and r[3] > 400000, 0), 'BARC and > 400000')
wrong_set('l2-filtering-rows', 'screens[3]', 'used-or', regions(P12, lambda r: r[1] == 'BARC' or r[3] > 400000, 0))
lv.claim(len(q("SELECT * FROM prices WHERE ticker = 'BARC' AND ticker = 'BP'")) == 0, 'l2 trap: 0 rows')
pre = q("SELECT date, ticker FROM prices WHERE ticker = 'BARC' OR ticker = 'BP' AND close > 4.65")
same_set('l2-filtering-rows', 'screens[5]', regions(P12, lambda r: r[1] == 'BARC' or (r[1] == 'BP' and r[2] > 4.65), 0), 'AND before OR')
lv.claim(len(pre) == 5, 'l2 screens[5]: SQLite keeps 5 rows')
wrong_set('l2-filtering-rows', 'screens[5]', 'left-to-right', regions(P12, lambda r: r[1] in ('BARC', 'BP') and r[2] > 4.65, 0))
lv.claim({t for (t,) in q("SELECT DISTINCT ticker FROM prices WHERE ticker LIKE 'B%'")} == {'BARC', 'BP'}, "l2 LIKE 'B%': BARC and BP")
lv.claim([d for (d,) in q("SELECT date FROM prices WHERE ticker = 'VOD' AND close >= 0.72")] == ['2026-03-02', '2026-03-04'],
         'l2 screens[8]: VOD close >= 0.72 on 2 and 4 March')
n = len(q("SELECT * FROM prices WHERE close >= 4.66"))
lv.claim(n == sum(r[2] >= 4.66 for r in T) == 5, 'l2 quiz[0]: 5, two ways')
lv.expect('l2', 'quiz[0].widget.answer', n)
lv.expect('l2', 'quiz[0].widget.wrong[0].value', len(q("SELECT * FROM prices WHERE close > 4.66")))
lv.expect('l2', 'quiz[0].widget.wrong[1].value', len(q("SELECT * FROM prices WHERE ticker = 'BP' AND close >= 4.66")))
lv.claim(len(q("SELECT * FROM prices WHERE ticker LIKE 'B'")) == 0, "l2 quiz[1]: LIKE 'B' returns no rows")
lv.expect('l2', 'quiz[2].widget.answer', len(q("SELECT * FROM prices WHERE date = '2026-03-02' OR date = '2026-03-04'")))
u = sqlite3.connect(':memory:'); u.execute("CREATE TABLE tickers (ticker TEXT)")
u.executemany("INSERT INTO tickers VALUES (?)", [(t,) for t in ['BARC', 'BATS', 'HSBA', 'LAND', 'VOD']])
lv.claim([t for (t,) in u.execute("SELECT ticker FROM tickers WHERE ticker LIKE '_A%'")] == ['BARC', 'BATS', 'LAND'], "l2 quiz[3]: _A%")
# Claim: a wildcard-free pattern "behaves like =". In SQLite, LIKE ignores case for ASCII letters; = does not.
c = sqlite3.connect(':memory:'); c.execute("CREATE TABLE t (x TEXT)"); c.executemany("INSERT INTO t VALUES (?)", [('B',), ('b',)])
like_eq = c.execute("SELECT COUNT(*) FROM t WHERE x LIKE 'B'").fetchone()[0] == c.execute("SELECT COUNT(*) FROM t WHERE x = 'B'").fetchone()[0]
lv.claim_text('l2', 'quiz[1].widget.options[2].why', 'It then behaves like `=`.', like_eq, "l2 quiz[1] why: LIKE 'B' behaves like = (finding 13)")

# ---- l3
same_set('l3-top-ten', 'screens[0]', regions(P12, lambda r: r[3] in sorted([x[3] for x in T])[-3:], 3), 'top 3 volumes')
wrong_set('l3-top-ten', 'screens[0]', 'smallest', regions(P12, lambda r: r[3] in sorted([x[3] for x in T])[:3], 3))
lv.claim(q("SELECT date, ticker, volume FROM prices ORDER BY volume DESC")[0] == ('2026-03-03', 'VOD', 704000), 'l3 screens[1] first row')
lv.claim(q("SELECT ticker, close FROM prices ORDER BY close")[0] == ('VOD', 0.71), "l3 screens[2] ('VOD', 0.71)")
lv.claim(q("SELECT ticker, date FROM prices ORDER BY ticker, date DESC")[:3] == [('BARC', '2026-03-04'), ('BARC', '2026-03-03'), ('BARC', '2026-03-02')], 'l3 screens[3] first three')
top4 = sorted([x[2] for x in T])[-4:]
same_set('l3-top-ten', 'screens[4]', regions(P12, lambda r: r[2] in top4, 2), 'top 4 closes')
wrong_set('l3-top-ten', 'screens[4]', 'asc', regions(P12, lambda r: r[2] in sorted([x[2] for x in T])[:4], 2))
quiet = [v for (_, _, v) in q("SELECT date, ticker, volume FROM prices ORDER BY volume LIMIT 5")]
lv.claim(quiet[0] == 48000 and quiet[-1] == 225000, 'l3 screens[5]: five quietest run 48000 to 225000')
lv.claim(len(q("SELECT ticker FROM prices WHERE date = (SELECT MAX(date) FROM prices)")) == 4, 'l3 screens[6]: four rows tie on 4 March')
lv.claim(q("SELECT date, close FROM prices WHERE ticker = 'BP' ORDER BY date DESC LIMIT 2") == [('2026-03-04', 4.66), ('2026-03-03', 4.61)], 'l3 screens[7] explain result')
lv.expect('l3', 'quiz[1].widget.answer', len(q("SELECT * FROM prices ORDER BY close LIMIT 20")))
lv.claim(q("SELECT ticker, close FROM prices ORDER BY ticker DESC, close")[0] == ('VOD', 0.71), "l3 quiz[3] ('VOD', 0.71)")
lv.claim(q("SELECT ticker, close FROM prices ORDER BY ticker, close")[0] == ('BARC', 2.12), "l3 quiz[3] asc option ('BARC', 2.12)")
# Claim: the written clause order is the order the work happens. l7 screens[6] (logical order) puts SELECT after WHERE.
l7 = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'sql', 'l7-filtering-groups.json')))
logical = l7['screens'][6]['widget']['answer']
select_first = logical.index('s5') == 0
lv.claim_text('l3', 'screens[7].prose', 'which is also the order the work happens', select_first, 'l3 screens[7]: written order = order of work (finding 9)')
lv.claim_text('l3', 'screens[5].widget.options[2].why', 'The order written is the order applied.', select_first, 'l3 screens[5] limit-first why (finding 9)')

# ---- l4
c4, P8 = table('l4-missing-values', 'screens[0]')
d4 = build(c4, P8)
q4 = lambda s: d4.execute(s).fetchall()
T8 = [[num(c) for c in r] for r in P8]
same_set('l4-missing-values', 'screens[0]', regions(P8, lambda r: r[2] is not None and r[2] > 1, 0), 'close > 1')
lv.claim(len(q4("SELECT * FROM prices WHERE close > 1")) == 3, 'l4 close > 1 keeps 3')
same_set('l4-missing-values', 'screens[1]', regions(P8, lambda r: r[2] is not None and r[2] <= 1, 0), 'close <= 1')
dropped = len(T8) - len(q4("SELECT * FROM prices WHERE close > 1")) - len(q4("SELECT * FROM prices WHERE close <= 1"))
lv.claim(dropped == sum(r[2] is None for r in T8) == 2, 'l4 screens[2]: both filters drop 2, two ways')
lv.expect('l4', 'screens[2].widget.answer', dropped)
lv.claim(len(q4("SELECT * FROM prices WHERE close = NULL")) == 0, 'l4 trap: = NULL gives 0')
same_set('l4-missing-values', 'screens[4]', regions(P8, lambda r: r[2] is None, 0), 'IS NULL')
lv.expect('l4', 'screens[5].widget.answer', len(q4("SELECT * FROM prices WHERE ticker = 'VOD' AND close IS NOT NULL")))
lv.expect('l4', 'screens[5].widget.wrong[0].value', len(q4("SELECT * FROM prices WHERE ticker = 'VOD'")))
lv.expect('l4', 'screens[5].widget.wrong[2].value', len(q4("SELECT * FROM prices WHERE close IS NOT NULL")))
n = len(q4("SELECT * FROM prices WHERE close <> 2.15"))
lv.claim(n == sum(r[2] is not None and r[2] != 2.15 for r in T8) == 5, 'l4 screens[6]: <> 2.15 keeps 5, two ways')
lv.expect('l4', 'screens[6].widget.answer', n)
lv.expect('l4', 'screens[6].widget.wrong[0].value', sum(r[2] != 2.15 for r in T8))
lv.claim(q4("SELECT date, ticker, close FROM prices ORDER BY close, date LIMIT 1") == [('2026-03-03', 'BARC', None)], 'l4 screens[7]: NULL sorts first in SQLite')
lv.claim(len(q4("SELECT * FROM prices WHERE close < 1 OR close IS NULL")) == 5, 'l4 screens[9] explain: 5 rows')
lv.expect('l4', 'screens[9].explain.text', 5)
lv.expect('l4', 'quiz[0].explain.text', len(q4("SELECT * FROM prices WHERE close IS NOT NULL")))
lv.expect('l4', 'quiz[1].widget.answer', 50 - 4 - 30)
lv.expect('l4', 'quiz[1].widget.wrong[0].value', 50 - 30)
lv.expect('l4', 'quiz[1].explain.text', 50 - 4)
lv.claim(q4("SELECT ticker, close FROM prices ORDER BY close DESC LIMIT 1") == [('BARC', 2.18)], "l4 quiz[3]: ('BARC', 2.18), NULLs last when descending")

# ---- review-1
n = len(q("SELECT DISTINCT ticker FROM prices WHERE close > 4"))
lv.expect('review', 'items[0].widget.answer', n)
lv.expect('review', 'items[0].widget.wrong[0].value', len(q("SELECT ticker FROM prices WHERE close > 4")))
same_set('review-1', 'items[1]', regions(P12, lambda r: r[3] < 100000 or r[1] == 'BP', 0), 'volume < 100000 OR BP')
lv.claim(q("SELECT ticker, date, close FROM prices ORDER BY date DESC, close DESC LIMIT 1") == [('SHEL', '2026-03-04', 26.9)], 'review-1 items[2]: SHEL 26.90')
c1, P8r = table('review-1', 'items[3]')
dr = build(c1, P8r)
lv.expect('review', 'items[3].widget.answer', len(dr.execute("SELECT * FROM prices WHERE close > 2 OR close <= 2").fetchall()))
lv.claim(len(q("SELECT * FROM prices WHERE (ticker = 'VOD' OR ticker = 'BP') AND date = '2026-03-03'")) == 2, 'review-1 items[4]: 2 rows')
lv.claim(len(q("SELECT * FROM prices WHERE ticker = 'VOD' OR ticker = 'BP' AND date = '2026-03-03'")) == 4, 'review-1 items[4] no-brackets: 3 VOD rows plus BP')
n = len(q("SELECT DISTINCT date, ticker FROM prices WHERE ticker LIKE 'B%'"))
lv.expect('review', 'items[5].widget.answer', n)
lv.claim([c for (c,) in dr.execute("SELECT close FROM prices WHERE ticker = 'VOD' AND close IS NOT NULL ORDER BY close LIMIT 3")] == [0.71, 0.72, 0.74], 'review-1 items[6]')

# ---- homework-1
lv.expect('homework', 'items[0].widget.answer', len(q("SELECT * FROM prices WHERE ticker LIKE '%A%' AND close < 3")))
lv.expect('homework', 'items[0].widget.wrong[1].value', len(q("SELECT * FROM prices WHERE close < 3")))
n = len(q("SELECT * FROM prices WHERE ticker = 'SHEL' OR ticker = 'VOD' AND volume > 600000"))
lv.claim(n == sum(r[1] == 'SHEL' or (r[1] == 'VOD' and r[3] > 600000) for r in T) == 5, 'homework-1 items[1]: 5, two ways')
lv.expect('homework', 'items[1].widget.answer', n)
lv.expect('homework', 'items[1].widget.wrong[0].value', len(q("SELECT * FROM prices WHERE (ticker = 'SHEL' OR ticker = 'VOD') AND volume > 600000")))
cv, V10 = table('homework-1', 'items[3]')
dv = build(cv, V10)
qv = lambda s: dv.execute(s).fetchall()
lv.expect('homework', 'items[3].widget.answer', len(qv("SELECT DISTINCT close FROM prices WHERE ticker = 'VOD'")))
lv.expect('homework', 'items[3].widget.wrong[0].value', len(qv("SELECT DISTINCT close FROM prices WHERE ticker = 'VOD' AND close IS NOT NULL")))
lv.claim(qv("SELECT date, close FROM prices WHERE ticker = 'SHEL' AND close IS NOT NULL ORDER BY date") == [('2026-03-02', 26.84), ('2026-03-04', 26.9), ('2026-03-05', 27.02)], 'homework-1 items[4]')
lv.claim(len(qv("SELECT * FROM prices WHERE volume IS NULL")) == 2, 'homework-1 items[5] explain: two volume gaps')
lv.claim(qv("SELECT date, ticker FROM prices WHERE (close IS NULL OR volume IS NULL) AND (ticker LIKE 'V%' OR ticker LIKE 'B%') ORDER BY date, ticker")
         == [('2026-03-04', 'BATS'), ('2026-03-04', 'VOD'), ('2026-03-05', 'VOD')], 'homework-1 items[6]')
broken = [d for (d,) in qv("SELECT date FROM prices WHERE ticker = 'VOD' AND close = NULL OR close > 0.72 ORDER BY date")]
lv.claim(broken == ['2026-03-02', '2026-03-03', '2026-03-04', '2026-03-04', '2026-03-04', '2026-03-05'], 'homework-1 items[7] model: the six dates')
fixed = [d for (d,) in qv("SELECT date FROM prices WHERE ticker = 'VOD' AND (close IS NULL OR close > 0.72) ORDER BY date")]
lv.claim(fixed == ['2026-03-04', '2026-03-05'], 'homework-1 items[7] model: the fixed query returns 4 and 5 March')
# Claim: "(ticker = 'VOD' AND close = NULL)" "is unknown for every row". It is false (0) for the other tickers.
vals = {t: v for t, v in qv("SELECT ticker, (ticker = 'VOD' AND close = NULL) FROM prices")}
lv.claim_text('homework', 'items[7].model', 'so it is unknown for every row and never true', all(v is None for v in vals.values()),
              'homework-1 items[7] model: unknown for every row (finding 12)')

lv.check_wrongs()
lv.report()
