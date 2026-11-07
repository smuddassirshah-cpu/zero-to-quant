"""py-found level 2 (Dictionaries and functions): second-read number and claim checks (session V).

Run: python3 docs/reports/py-found-L2-numbers.py   (exits 0 when every check passes)
Every code widget is run in CPython (solution passes, starter fails); every "what does it print" item is run and compared
with its keyed option; every stated sum, value and count is recomputed. Checks that fail because the content is wrong
are tied to the content (data-driven or by wording), so they pass once review-py-found-1-2.md is applied.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
sys.path.insert(0, HERE)
from numbers_lib import Level  # noqa: E402
from py_found_read12 import check_code, check_print, run_snippet  # noqa: E402

lv = Level('py-found', 2)


def node(ref, path):
    fid, doc = lv._file(ref)
    x = doc
    for key, idx in re.findall(r'([A-Za-z_][\w-]*)|\[(\d+)\]', path):
        x = x[key] if key else x[int(idx)]
    return x


def block(ref, path):
    return node(ref, path).split('```python\n')[1].split('```')[0]


print('code widgets run:', check_code(lv))

# ---------- l5: dictionaries ----------
prices = {'VOD': 0.72, 'BP': 4.85, 'HSBA': 6.42}
lv.claim(prices['BP'] == 4.85, 'l5 screens[0] prices["BP"] is 4.85')
book = {}
book['BP'] = 300
book['VOD'] = 1000
book['BP'] = 500
lv.claim(book == {'BP': 500, 'VOD': 1000}, 'l5 screens[1] book ends {"BP": 500, "VOD": 1000}')
for t, want in [(('BP', 500, 4.85), 2425.0), (('VOD', 1000, 0.72), 720.0), (('AZN', 20, 118.50), 2370.0),
                (('BP', -200, 4.85), -970.0), (('HSBA', 150, 6.42), 963.0), (('SHEL', 40, 27.30), 1092.0)]:
    lv.claim(abs(t[1] * t[2] - want) < 1e-9, f'l5 screens[2] {t[0]} {t[1]} x {t[2]} = {want}')
lv.expect('l5', 'screens[2].explain.text', -970.00)
for p in ('screens[3]', 'screens[4]', 'screens[5]', 'screens[6]', 'quiz[0]', 'quiz[1]', 'quiz[3]'):
    check_print(lv, 'l5', p)
lv.claim(len({'BP': 4.90}) == node('l5', 'screens[8].widget.answer') == 1, 'l5 screens[8] len(d) is 1')
FEES = {'LSE': 0.0010, 'TQ': 0.0005, 'CBOE': 0.0008}
lv.claim(abs(20000 * FEES['LSE'] - 20.0) < 1e-9, 'l5 screens[9] prose: a £20,000.00 LSE trade pays £20.00')
lv.claim(abs(4850 * 0.0015 - 7.275) < 1e-12 and abs(1000 * 0.0015 - 1.5) < 1e-12, 'l5 screens[9] tests 6 and 7')
w9 = node('l5', 'screens[9].widget')
ns = {}
exec(w9['solution'].replace('FEES.get(venue,', 'FEES.get(venue.upper(),'), ns)
upper_passes_t7 = abs(ns['trade_fee'](1000.00, 'lse') - 1.5) < 1e-9
lv.claim(not upper_passes_t7, 'l5 screens[9]: a solution using venue.upper() (the explain\'s advice) fails test 7')
lv.claim('test-7' in node('l5', 'screens[9].feedback.byKey'),
         'l5 screens[9]: test 7 (lower-case "lse") has a byKey line, since the explain recommends venue.upper()')
out, _ = run_snippet(block('l5', 'quiz[2].prose'))
lv.claim(abs(float(out) - node('l5', 'quiz[2].widget.answer')) < 1e-9 and out.strip() == '5.8', 'l5 quiz[2] prints 5.8')
lv.claim(abs(5.8 - 2.0 - 3.8) < 1e-9 and abs(5.8 - 1.5 - 4.3) < 1e-9, 'l5 quiz[2] wrongs skip 3.8, once 4.3')

# ---------- l6: sets and counts ----------
trades = ['BP', 'VOD', 'BP', 'AZN', 'VOD', 'BP']
first = sorted(f'c{trades.index(t)}' for t in dict.fromkeys(trades))
lv.claim(first == sorted(node('l6', 'screens[0].widget.answer')), 'l6 screens[0] first appearances c0, c1, c3')
lv.claim({t: trades.count(t) for t in dict.fromkeys(trades)} == {'BP': 3, 'VOD': 2, 'AZN': 1}, 'l6 screens[1] counts')
for p in ('screens[2]', 'screens[6]', 'quiz[1]', 'quiz[3]'):
    check_print(lv, 'l6', p)
lv.claim(1_000_000 * 5_000 == 5_000_000_000, 'l6 screens[4] explain: a million misses x 5,000 is five billion comparisons')
lv.expect('l6', 'screens[4].widget.options[0].text', 5000)
out, _ = run_snippet(block('l6', 'quiz[0].prose'))
lv.claim(int(out) == node('l6', 'quiz[0].widget.answer') == 2, 'l6 quiz[0] prints 2')
out, _ = run_snippet(block('l6', 'quiz[2].prose'))
lv.claim(int(out) == node('l6', 'quiz[2].widget.answer') == 1, 'l6 quiz[2] prints 1')
out, err = run_snippet('book = {"BP": 300}\nfor t in book:\n    del book[t]')
lv.claim(type(err).__name__ == 'RuntimeError', 'l6 screens[8] test-2: deleting keys while looping raises RuntimeError')

# ---------- l7: arguments ----------
for p in ('screens[0]', 'screens[4]', 'screens[6]', 'quiz[0]', 'quiz[1]'):
    check_print(lv, 'l7', p)
defs = 'def cost(price, qty, fee=1.50):\n    return price * qty + fee\n'
for opt in node('l7', 'screens[2].widget.options'):
    call = opt['text'].strip('`')
    _, err = run_snippet(defs + call)
    lv.claim((type(err).__name__ == 'SyntaxError') == bool(opt.get('correct')), f'l7 screens[2] {call}: error iff keyed')
out, _ = run_snippet(defs + 'print(cost(2.50, fee=0.00, qty=200))')
lv.claim(out.strip() == '500.0', 'l7 screens[1] cost(2.50, fee=0.00, qty=200) is 500.0, 1.50 not used')
ns = {}
exec(block('l7', 'screens[8].prose'), ns)
lv.claim(ns['f'](1, c=[5]) == (1, 2, [5]), 'l7 screens[8] f(1, c=[5]) returns (1, 2, [5])')
lv.claim(abs((4.84 + 4.86) / 2 - 4.85) < 1e-12 and abs((4.86 - 4.84) - 0.02) < 1e-12, 'l7 screens[5] mid 4.85, spread 0.02')
lv.expect('l7', 'screens[5].explain.text', 4.85)
lv.expect('l7', 'screens[5].explain.text', 0.02)
lv.claim(abs(0.9 * 0.9 - 0.81) < 1e-12 and abs(1 - 0.81 - 0.19) < 1e-12, 'l7 screens[9] -10% twice: 0.81, drawdown 0.19')
lv.expect('l7', 'screens[9].explain.text', 0.19)
lv.expect('l7', 'screens[9].explain.text', 0.81)
lv.claim(abs(sum([0.01, -0.02, 0.03]) / 3 - 0.00666666666667) < 1e-14, 'l7 screens[9] test 2 mean')
lv.claim(5 * 2 + 1 == 11, 'l7 quiz[0] 5 x 2 + 1 = 11')
out, _ = run_snippet(block('l7', 'quiz[2].prose'))
lv.claim(int(out) == node('l7', 'quiz[2].widget.answer') == 3, 'l7 quiz[2] prints 3')
lv.claim(abs(max(20000 * 0.001, 1.5) - 20) < 1e-9 and max(500 * 0.001, 1.5) == 1.5, 'l7 screens[3] prose fee(20000) 20, fee(500) 1.50')

# ---------- l8: mutation ----------
for p in ('screens[0]', 'screens[2]', 'screens[3]', 'screens[4]', 'screens[5]', 'screens[7]', 'quiz[0]', 'quiz[1]', 'quiz[3]'):
    check_print(lv, 'l8', p)
lv.claim((4.80 + 4.90) / 2 == 4.85 or abs((4.80 + 4.90) / 2 - 4.85) < 1e-12, 'l8 screens[6] test-3 (4.80 + 4.90) / 2 = 4.85')
lv.claim(abs(500 * 4.85 + 1000 * 0.72 - 3145) < 1e-9, 'l8 screens[10] 500 BP + 1,000 VOD = £3,145.00')
lv.expect('l8', 'screens[10].explain.text', 3145.00)
lv.claim(abs(-20 * 118.50 + 300 * 4.85 + 915) < 1e-9, 'l8 screens[10] test 4: -915')
out, _ = run_snippet(block('l8', 'quiz[2].prose'))
lv.claim(int(out) == node('l8', 'quiz[2].widget.answer') == 150, 'l8 quiz[2] prints 150')
pop_returns_none = [1, 2].pop() is None
lv.stated('l8', 'summary.ideas[1]', 'changes the object for every label and returns `None`', pop_returns_none)
lv.stated('l8', 'screens[9].prose', '# mutating: the object changes; the call gives None', pop_returns_none)
out, err = run_snippet('prices = [4.91, 4.72]\nprices = prices.sort()\nprint(prices)')
lv.claim(out.strip() == 'None', 'l8 screens[4] explain: prices = prices.sort() leaves None')

# ---------- review-2 ----------
for p in ('items[0]', 'items[1]', 'items[3]', 'items[8]'):
    check_print(lv, 'review', p)
out, _ = run_snippet(block('review', 'items[4].prose'))
lv.claim(int(out) == node('review', 'items[4].widget.answer') == 3, 'review-2 items[4] prints 3')
lv.claim(500 + 300 == 800 and 500 - 300 == 200, 'review-2 items[2] explain: BP traded 800, position 200')
_, err = run_snippet('def add(p, history=()):\n    history.append(p)\nadd(1)')
lv.claim(type(err).__name__ == 'AttributeError', 'review-2 items[7] tuple default: append raises AttributeError')

# ---------- homework-2 ----------
check_print(lv, 'homework', 'items[1]')
check_print(lv, 'homework', 'items[6]')
out, _ = run_snippet(block('homework', 'items[7].prose'))
lv.claim(int(out) == node('homework', 'items[7].widget.answer') == 9, 'homework-2 items[7] prints 9')
lv.claim(3 * 6 == 18 and 1 * 3 == 3, 'homework-2 items[7] wrongs: list 18, once 3')
bp = 500 * (4.85 - 4.80) + (-200) * (4.85 - 4.90)
lv.claim(abs(bp - 35) < 1e-9 and abs(500 * 0.05 - 25) < 1e-9 and abs(-200 * -0.05 - 10) < 1e-9, 'homework-2 items[2] BP 25 + 10 = 35')
lv.claim(abs(1000 * (0.72 - 0.70) - 20) < 1e-9, 'homework-2 items[2] VOD 1,000 x 0.02 = 20')
for v in (35.00, 25.00, 10.00, 20.00):
    lv.expect('homework', 'items[2].explain.text', v)
lv.claim(abs(0.001 * 500 - 0.50) < 1e-12, 'homework-2 items[3] test-3: 0.001 x 500 = £0.50')
lv.claim(abs(300 * 4.85 + 1000 * 0.72 - 2175) < 1e-9 and abs(10 * 4.85 - 48.5) < 1e-9, 'homework-2 items[4] 2175, 48.5')
# items[5] longform model: run the colleague's code and the model fix
bad = block('homework', 'items[5].prompt')
_, err = run_snippet(bad + '\nadd_trade("BP", 100)')
lv.claim(type(err).__name__ == 'KeyError' and str(err) == "'BP'", "homework-2 items[5] (a): KeyError: 'BP'")
fixed_a = bad.replace('book[ticker] = book[ticker] + qty', 'book[ticker] = book.get(ticker, 0) + qty')
out, _ = run_snippet(fixed_a + '\na = add_trade("BP", 100)\nb = add_trade("VOD", 50)\nprint(a)')
lv.claim(out.strip() == "{'BP': 100, 'VOD': 50}", 'homework-2 items[5] (b) print(a)')
_, err = run_snippet(fixed_a + '\ntotal_value({"BP": 500}, {"BP": 4.85})')
lv.claim(type(err).__name__ == 'TypeError' and 'NoneType' in str(err), 'homework-2 items[5] (c)1: sort() gives None, TypeError')
fixed_c1 = fixed_a.replace('tickers = tickers.sort()', 'tickers = sorted(tickers)')
out, _ = run_snippet(fixed_c1 + '\nprint(total_value({"BP": 500, "VOD": 1000}, {"BP": 4.85, "VOD": 0.72}))')
lv.claim(out.strip() == '0', 'homework-2 items[5] (c)2: prices[t] in prices is False, total 0')
model = node('homework', 'items[5].model').split('```python\n')[1].split('```')[0]
out, _ = run_snippet(model + '\nprint(total_value({"BP": 500, "VOD": 1000}, {"BP": 4.85, "VOD": 0.72}), total_value({"X": 1}, {}))'
                     '\nprint(add_trade("BP", 100), add_trade("VOD", 50))')
lv.claim(out.split('\n')[0] == '3145.0 None' and out.split('\n')[1] == "{'BP': 100} {'VOD': 50}", 'homework-2 items[5] model claims')

lv.check_wrongs()
lv.report()
