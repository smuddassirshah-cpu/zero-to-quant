"""py-found level 1 (Core types): second-read number and claim checks (session V).

Run: python3 docs/reports/py-found-L1-numbers.py   (exits 0 when every check passes)
Every code widget is run in CPython (solution passes, starter fails); every "what does it print" item is run and compared
with its keyed option; every stated float, index and count is recomputed. Checks that fail because the content is wrong
are tied to the content (data-driven or by wording), so they pass once review-py-found-1-2.md is applied.
"""
import os
import sys
from decimal import Decimal as D

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
sys.path.insert(0, HERE)
from numbers_lib import Level  # noqa: E402
from py_found_read12 import check_code, check_print, run_snippet  # noqa: E402

lv = Level('py-found', 1)
J = {k: v for k, v in lv.files.items()}


def node(ref, path):
    import re
    fid, doc = lv._file(ref)
    x = doc
    for key, idx in re.findall(r'([A-Za-z_][\w-]*)|\[(\d+)\]', path):
        x = x[key] if key else x[int(idx)]
    return x


def tap_ids(cells_true):
    return sorted(f'c{i}' for i in cells_true)


# ---------- every code widget ----------
print('code widgets run:', check_code(lv))

# ---------- l1: floats ----------
s = 0.1 + 0.2
lv.expect('l1', 'screens[0].feedback.correct', repr(s))                        # 0.30000000000000004
lv.claim(s != 0.3, 'l1 0.1 + 0.2 != 0.3 in CPython')
lv.expect('l1', 'screens[0].explain.text', '0.29999999999999998')
lv.claim(str(D(0.3)).startswith('0.29999999999999998'), 'l1 0.3 is stored as 0.29999999999999998... (truncated, as the table)')
gap = s - 0.3
lv.claim(abs(gap - 5.551115123125783e-17) < 1e-30, 'l1 the gap is 5.55e-17')
lv.claim(round(gap, 17) == 6e-17, 'l1 "about 0.00000000000000006" and "6 x 10^-17" (5.55e-17 to one figure)')
lv.expect('l1', 'screens[0].explain.canvas.caption', '0.00000000000000006')
lv.expect('l1', 'screens[4].canvas.params.rows[0][1]', '6 × 10⁻¹⁷')
lv.claim(f'{1/3 - 0.33333333:.3g}' == '3.33e-09', 'l1 screen 1: gap at 8 digits is 0.00000000333')
lv.expect('l1', 'screens[1].widget.options[1].why', '0.00000000333')
lv.claim(D(0.1) > D('0.1') and D(0.2) > D('0.2') and D(0.3) < D('0.3'), 'l1 0.1 and 0.2 stored high, 0.3 stored low')
lv.stated('l1', 'screens[1].explain.text', 'drops the rest', D(0.1) < D('0.1'))   # truncation would store 0.1 low
for i, (typed, shown) in enumerate([('0.1', '0.10000000000000000555'), ('0.2', '0.20000000000000001110'),
                                    ('0.3', '0.29999999999999998890')]):
    lv.claim(f'{D(float(typed)):.20f}' == shown, f'l1 screens[2] table row {i}: {typed} stored as {shown}')
    lv.expect('l1', f'screens[2].canvas.params.rows[{i}][1]', shown)
lv.claim(len(f'{D(0.1):.20f}'.split('.')[1]) == 20, 'l1 "to 20 places"')
lv.claim(repr(0.1 + 0.2) == '0.30000000000000004', 'l1 screens[2] keyed print(0.1 + 0.2)')
lv.expect('l1', 'screens[2].widget.options[1].text', '0.30000000000000004')
# screen 3: which checks print True
rows = [r[0] for r in node('l1', 'screens[3].canvas.params.rows')]
true_rows = [i for i, r in enumerate(rows) if eval(r)]
lv.claim(sorted(f'r{i}c0' for i in true_rows) == sorted(node('l1', 'screens[3].widget.answer')), f'l1 screens[3] True rows {true_rows}')
lv.claim(repr(0.1 * 3) == '0.30000000000000004' and repr(0.7 + 0.1) == '0.7999999999999999', 'l1 screens[3] byKey r3c0, r4c0 values')
tenths = [i / 10 for i in range(1, 10)]
tenth_sums_true = [(a, b) for a in tenths for b in tenths if a + b <= 1.0 and (a + b == round(a + b, 1))]
lv.claim(len(tenth_sums_true) > 0, 'some sums of tenths compare equal, e.g. 0.1 + 0.4 == 0.5 and 0.6 + 0.1 == 0.7')
lv.stated('l1', 'screens[3].explain.text', 'Every check with a tenth in it drifts and prints `False`', len(tenth_sums_true) == 0)
lv.stated('l1', 'screens[3].hints[2].text', 'Any check with a tenth in it prints `False`', len(tenth_sums_true) == 0)
# screen 4: isclose
check_print(lv, 'l1', 'screens[4]')
lv.claim(abs(1e-9 * max(abs(s), 0.3) - 3e-10) < 1e-20, 'l1 screens[4] allowance next to 0.3 is 3 x 10^-10')
lv.expect('l1', 'screens[4].widget.options[2].why', '0.0000000003')
lv.expect('l1', 'screens[4].explain.canvas.values.r0c2', '3 × 10⁻¹⁰')
check_print(lv, 'l1', 'screens[0]')
# screen 5 hint
lv.claim(abs(abs(10.00 - 10.003) - 0.003) < 1e-12, 'l1 screens[5] gap 10.00 vs 10.003 is 0.003')
lv.claim((10.00 - 10.01) < 0.005 and not abs(10.00 - 10.01) < 0.005, 'l1 screens[5] test-3: a - b without abs passes wrongly')
# screen 6: ten deposits
check_print(lv, 'l1', 'screens[6]')
t, run = 0.0, []
for _ in range(10):
    t += 0.1
    run.append(repr(t))
lv.claim(run[-1] == '0.9999999999999999' and run[2] == '0.30000000000000004', 'l1 screens[6] running totals 0.3+ and 1.0-')
marks = node('l1', 'screens[6].explain.canvas.cells')
want = ['0.1', '0.2', '0.3+', '0.4', '0.5', '0.6', '0.7', '0.8−', '0.9−', '1.0−']
lv.claim(marks == want and [r for r in run] == ['0.1', '0.2', '0.30000000000000004', '0.4', '0.5', '0.6', '0.7',
                                                '0.7999999999999999', '0.8999999999999999', '0.9999999999999999'],
         'l1 screens[6] explain canvas marks each running total high (+) or low (-) correctly')
lean_same_way = (10 * D(0.1) > 1) == (D(t) > 1)   # stored 0.1 is high; would ten of them land high?
lv.stated('l1', 'screens[6].widget.options[0].why', 'They lean the same way here', lean_same_way)
lv.stated('l1', 'screens[6].feedback.byKey.cancel', 'They lean the same way here', lean_same_way)
# screen 7: pence
lv.claim(repr(0.29 * 100) == '28.999999999999996' and int(0.29 * 100) == 28 and round(0.29 * 100) == 29, 'l1 0.29 * 100')
lv.claim(repr(19.99 * 100) == '1998.9999999999998' and int(19.99 * 100) + int(0.01 * 100) == 1999, 'l1 test-2 int route gives 1999')
lv.claim(repr(19.99 * 100 + 0.01 * 100) == '1999.9999999999998', 'l1 test-2 unrounded float total 1999.9999999999998')
lv.claim(round(1.15 * 100) + round(2.30 * 100) + round(0.55 * 100) == 400, 'l1 screens[7] test 4: 400 pence')
# screen 8
lv.claim(round(-0.40) == 0 and abs(0.01) >= 0.005, 'l1 screens[8]: a 0.40 loss rounds to 0; 0.01 is caught')
# screen 9: shares
lv.claim(repr(550.00 / 1.10) == '499.99999999999994' and int(550.00 / 1.10) == 499, 'l1 screens[9] float route 499')
lv.claim(55000 // 110 == 500 and repr(100.00 / 3.00) == '33.333333333333336', 'l1 screens[9] pence route 500; test-3 33.33...')
lv.stated('l1', 'screens[9].explain.text', 'A broker would reject a sloppy 499', False)
# quiz
check_print(lv, 'l1', 'quiz[0]')
lv.claim(str(D(2.675)) == '2.67499999999999982236431605997495353221893310546875', 'l1 quiz[0] stored 2.675')
lv.expect('l1', 'quiz[0].explain.text', '2.67499999999999982236431605997495353221893310546875')
check_print(lv, 'l1', 'quiz[1]')
lv.claim(repr(0.57 * 100) == '56.99999999999999' and int(0.57 * 100) == node('l1', 'quiz[2].widget.answer'), 'l1 quiz[2] 56')
lv.claim(round(0.57 * 100) == 57, 'l1 quiz[2] round gives 57')
check_print(lv, 'l1', 'quiz[3]')       # FAILS on current content: 0.6 + 0.1 == 0.7 is True in CPython

# ---------- l2: slicing ----------
closes6 = [101.20, 102.50, 99.80, 100.40, 103.10, 104.00]
lv.claim(tap_ids(range(1, 4)) == sorted(node('l2', 'screens[0].widget.answer')), 'l2 screens[0] closes[1:4] is c1 to c3')
lv.claim(sorted(node('l2', 'screens[0].widget.wrong[0].set')) == tap_ids(range(1, 5)), 'l2 screens[0] end-in = indices 1..4')
lv.claim(len(closes6) - 2 == node('l2', 'screens[1].widget.answer') and closes6[-2] == 103.10, 'l2 screens[1] -2 is index 4, 103.10')
check_print(lv, 'l2', 'screens[2]')
early = node('l2', 'screens[2].widget.options[1]')
lv.stated('l2', 'screens[2].widget.options[1].why', 'as if the slice ended at `-1`',
          early['text'] == f'`{closes6[-3:-1]!r}`'.replace("'", ''))
lv.claim(tap_ids(range(1, 6, 2)) == sorted(node('l2', 'screens[3].widget.answer')), 'l2 screens[3] closes[1::2] is c1, c3, c5')
two_on = node('l2', 'screens[3].widget.wrong[1]')
lv.claim(sorted(two_on['set']) == tap_ids(range(len(closes6))[1:2]),
         'l2 screens[3] wrong "two-on" set is what reading 2 as the end gives (closes[1:2])', f'set is {two_on["set"]}')
w4 = node('l2', 'screens[4].widget')
ns_tried = sorted({int(t['call'].rsplit(',', 1)[1].strip(' )')) for t in w4['tests'] if t['call'].startswith('last_n([101.2')})
lv.stated('l2', 'screens[4].prose', 'Hidden tests try every allowed `n`', ns_tried == list(range(0, 5)))
lv.claim(closes6[-0:] == closes6 and closes6[len(closes6) - 0:] == [], 'l2 screens[4] -0 is 0: prices[-0:] is the whole list')
ten = [101.2, 102.5, 99.8, 100.4, 103.1, 104.0, 102.7, 101.9, 103.6, 105.2]
lv.claim(ten[4::5] == [103.1, 105.2] and ten[0::5] == [101.2, 104.0], 'l2 screens[5] Fridays and the start-0 slip')
check_print(lv, 'l2', 'screens[6]')
lv.claim(len(ten[2:7]) == node('l2', 'screens[9].widget.answer') == 5, 'l2 screens[9] closes[2:7] holds 5')
lv.claim(len(closes6[1:4]) == 3, 'l2 screens[9] explain: closes[1:4] gave 3')
four = [101.20, 102.50, 99.80, 100.40]
step1_claim = len(four[2:10]) == 10 - 2
lv.stated('l2', 'screens[9].prose', 'With a step of 1 it holds $j - i$ items.', step1_claim)
lv.stated('l2', 'summary.formula.note', 'With step 1 it holds $j - i$ items.', step1_claim)
lv.stated('l2', 'screens[0].explain.text', 'so it holds `b - a` items', step1_claim)
lv.claim(abs(sum(ten[-5:]) - 517.4) < 1e-9 and abs(sum(ten[-5:]) / 5 - 103.48) < 1e-9, 'l2 screens[10] 517.40 / 5 = 103.48')
lv.expect('l2', 'screens[10].explain.text', 517.40)
lv.expect('l2', 'screens[10].explain.text', 103.48)
lv.claim(abs(sum(ten[:5]) / 5 - 101.40) < 1e-9, 'l2 screens[10] test-1 first five average 101.40')
lv.expect('l2', 'screens[10].feedback.byKey.test-1', 101.40)
lv.claim(abs(sum(ten) / 10 - 102.44) < 1e-9, 'l2 screens[10] all ten average 102.44')
for q in ('quiz[0]', 'quiz[1]', 'quiz[2]'):
    check_print(lv, 'l2', q)
idx = list(range(20))[1:20:3]
lv.claim(idx == [1, 4, 7, 10, 13, 16, 19] and len(idx) == node('l2', 'quiz[3].widget.answer'), 'l2 quiz[3] 7 items')
lv.claim(20 - 1 == 19, 'l2 quiz[3] wrong "divided" 19 is the span 20 - 1')

# ---------- l3: unpacking ----------
for p in ('screens[0]', 'screens[2]', 'screens[3]', 'screens[4]', 'screens[5]', 'screens[7]', 'quiz[0]', 'quiz[1]', 'quiz[3]'):
    check_print(lv, 'l3', p)
check_print(lv, 'l3', 'quiz[2]', last_line=True)
trade = ('VOD', 72.50, 100)
ticker, *rest = trade
lv.stated('l3', 'screens[2].widget.options[2].why', 'That needs a star', isinstance(rest, tuple))
lv.claim(abs((105 - 100) / 105 - 0.0476) < 5e-5 and (105 - 100) / 100 == 0.05, 'l3 screens[6] test-1: 0.0476 if divided by later')
lv.claim(abs((99.75 - 105) / 105 + 0.05) < 1e-12 and abs((245 - 250) / 250 + 0.02) < 1e-12, 'l3 screens[6] -0.05 and -0.02')
lv.claim(float('72.50') * int('100\n') == 7250.0, 'l3 screens[7] explain: float(price) * int(qty) is 7250.0')
out, err = run_snippet('price, qty = "72.50", "100\\n"\nprint(price + qty)')
lv.claim(out.startswith('72.50100'), 'l3 screens[7] option joined: price + qty prints 72.50100')
lv.claim(f'{4.8:.2f}' == '4.80' and f'{120.0:.2f}' == '120.00', 'l3 screens[8] :.2f')

# ---------- l4: comprehensions ----------
check_print(lv, 'l4', 'screens[0]')
rets10 = [0.012, -0.034, 0.005, -0.008, 0.021, 0.0, -0.015, 0.009, -0.002, 0.017]
lv.claim(tap_ids(i for i, r in enumerate(rets10) if r < 0) == sorted(node('l4', 'screens[1].widget.answer')), 'l4 screens[1] losses')
lv.claim(tap_ids(i for i, r in enumerate(rets10) if r <= 0) == sorted(node('l4', 'screens[1].widget.wrong[0].set')), 'l4 screens[1] zero slip set')
check_print(lv, 'l4', 'screens[2]', setup=f'rets = {rets10!r}')
check_print(lv, 'l4', 'screens[4]')
trades = [('VOD', 72.50), ('AZN', 120.00), ('BP', 4.85)]
lv.claim([t[0].lower() for t in sorted(trades, key=lambda t: t[1], reverse=True)] == node('l4', 'screens[5].widget.answer'), 'l4 screens[5] order')
r5 = [0.012, -0.034, 0.005, -0.008, 0.021]
lv.claim(sorted(r5, reverse=True)[:2] == [0.021, 0.012], 'l4 screens[6] test-1 slip: sorted by value gives [0.021, 0.012]')
check_print(lv, 'l4', 'screens[7]')
days = [('2026-10-12', 0.021), ('2026-10-13', -0.034), ('2026-10-14', 0.012), ('2026-10-15', -0.008)]
lv.claim(max(days)[0] == '2026-10-15', 'l4 screens[10] test-1 slip: max without key gives 2026-10-15')
for q in ('quiz[0]', 'quiz[1]', 'quiz[2]'):
    check_print(lv, 'l4', q)
out, _ = run_snippet(node('l4', 'quiz[3].prose').split('```python\n')[1].split('```')[0])
lv.claim(int(out) == node('l4', 'quiz[3].widget.answer') == 4, 'l4 quiz[3] prints 4')
r6 = [0.004, 0.0, -0.011, 0.0, -0.002, 0.007]
lv.claim(len([r for r in r6 if r < 0]) == 2 and len(r6) == 6, 'l4 quiz[3] wrongs: strict 2, all 6')

# ---------- review-1 ----------
for p in ('items[0]', 'items[1]', 'items[2]', 'items[3]', 'items[5]', 'items[6]'):
    check_print(lv, 'review', p)
import re  # noqa: E402
expr = re.search(r'`(int\([^`]*\))`', node('review', 'items[4].question')).group(1)   # data-driven: survives the fix
inner = expr[4:-1]
lv.claim(eval(expr) == node('review', 'items[4].widget.answer'), f'review-1 items[4] {expr} is the key')
lv.expect('review', 'items[4].prose', repr(eval(inner)))
lv.claim(round(eval(inner)) == node('review', 'items[4].widget.wrong[0].value'), 'review-1 items[4] wrong "nearest" is round()')
lv.stated('review', 'items[4].explain.text', 'a price stored a hair below 1.15', D(1.15) < D('1.15'))
lv.stated('review', 'items[6].widget.options[3].why', 'repeats its characters', '4.85' * 2 == ''.join(c * 2 for c in '4.85'))
c6 = [101.2, 102.5, 99.8, 100.4, 103.1, 104.0]
lv.claim([i for i, (a, b) in enumerate(zip(c6, c6[1:]), start=1) if b > a] == [1, 3, 4, 5], 'review-1 items[7] test 5')

# ---------- homework-1 ----------
check_print(lv, 'homework', 'items[0]')
check_print(lv, 'homework', 'items[2]')
check_print(lv, 'homework', 'items[6]')
out, err = run_snippet(node('homework', 'items[3].prose').split('```python\n')[1].split('```')[0])
lv.claim(out.strip() == "('VOD', [72.5, 73.1])", 'homework-1 items[3] prints the tuple with the grown list')
c20 = list(range(20))
lv.claim(len(c20[3:-2]) == node('homework', 'items[1].widget.answer') == 15, 'homework-1 items[1] closes[3:-2] holds 15')
wr = {w['id']: w['value'] for w in node('homework', 'items[1].widget.wrong')}
lv.claim(wr['kept-end'] == len(c20[3:19]) and wr['abs'] == 3 - 2, 'homework-1 items[1] wrongs kept-end 16, abs 1')
lv.stated('homework', 'items[1].feedback.byKey.no-start', 'You dropped only the last two', wr['no-start'] == len(c20[:-2]))
lv.claim(abs((99.75 - 102) / 102 - (-0.022058823529411766)) < 1e-15, 'homework-1 items[4] test 2 value')
lv.claim((102 - 100) / 100 == 0.02, 'homework-1 items[4] test-1 slip 0.02')
out, err = run_snippet('import math\nprint(math.isclose(0.1 + 0.2 - 0.3, 0.0))')
lv.claim(out.strip() == 'False', 'homework-1 items[7] model: isclose against 0.0 is False')
out, err = run_snippet('fills = [0.10, 0.20]\nexpected = 0.30\nprint(f"mismatch: {sum(fills):.2f} vs {expected:.2f}")')
lv.claim(out.strip() == 'mismatch: 0.30 vs 0.30' and sum([0.10, 0.20]) != 0.30, 'homework-1 items[7] prompt output')
lv.claim([round(f * 100) for f in [0.10, 0.20]] == [10, 20] and round(0.30 * 100) == 30, 'homework-1 items[7] model pence')

lv.check_wrongs()
lv.report()
