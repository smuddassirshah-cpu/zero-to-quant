#!/usr/bin/env python3
"""Test for numbers_lib.py (ENGINE-BACKLOG 573) against the real odes level 3 files. Run: python3 app/tools/test-numbers-lib.py
Real values must pass; a deliberately wrong value, a missing path and a wrong format must fail. Exit 0 when all behave."""
import contextlib, io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from numbers_lib import Level, normalise

lv = Level('odes', 3)
T = 'l10'
good = [
    lv.expect(T, 'screens[3].widget.answer', 3),
    lv.expect(T, 'screens[3].prose', -0.5),                       # "$-0.5$" with a LaTeX minus sign
    lv.expect(T, 'screens[3].prose', 0.5),
    lv.expect(T, 'screens[3].widget.wrong[1].value', 5.3333),
    lv.expect(T, 'screens[3].feedback.byKey.inv', 1.5),
    lv.expect(T, 'screens[3].explain', '(-2, -1.5)'),             # verbatim string
    lv.expect(T, 'screens[3].explain', -1.5, fmt='{:.1f}'),       # exact text
    lv.expect(T, 'screens[3]', 5.3333),                           # search below an object
]
cv = Level('convex', 1)
fr = [
    cv.expect('l4', 'screens', 0.5), cv.expect('l4', 'screens', 0.095),    # \\tfrac12 and a decimal
]
assert abs(__import__('numbers_lib')._numbers(r'$\\frac{3}{4}$ and $\\dfrac{a}{b}$')[-1] - 0.75) < 1e-12
assert 3.0 in __import__('numbers_lib')._numbers(r'$\\tfrac{3}{4}$') and 4.0 in __import__('numbers_lib')._numbers(r'$\\tfrac{3}{4}$')
good += fr
assert normalise('£1{,}214 and −3') == '1214 and -3'
# ENGINE-BACKLOG 582: check_wrongs on a synthetic file (clean wrong, in-tolerance wrong, byKey stating another number), then the real level
sy = Level('odes', 3)
sy.files = {'lx': {'screens': [{'widget': {'kind': 'numeric', 'answer': 10, 'tol': {'abs': 0.5}, 'wrong': [
    {'id': 'clean', 'value': 12}, {'id': 'inside', 'value': 10.4}, {'id': 'rel', 'value': 15, 'tol': {'abs': 0.1}}]},
    'feedback': {'byKey': {'clean': 'You added 3, giving 13.', 'inside': 'Near.', 'rel': 'You made 15.'}}}]}}
with contextlib.redirect_stdout(io.StringIO()):
    hand = sy.check_wrongs()
res = {r[1].split('"')[1]: r[0] for r in sy.results}
ok_w = res == {'clean': True, 'inside': False, 'rel': True} and len(hand) == 1 and '"clean"' in hand[0]
buf2, buf3 = io.StringIO(), io.StringIO()
with contextlib.redirect_stdout(buf2):
    sy.check_wrongs()
with contextlib.redirect_stdout(buf3):
    sy.check_wrongs(verbose=True)
ok_w = ok_w and 'check by hand: 1 byKey' in buf2.getvalue() and 'states' not in buf2.getvalue() and 'states' in buf3.getvalue()
pb = Level('counting-chance', 1)
with contextlib.redirect_stdout(io.StringIO()):
    got = pb.expect('problems', 'items[0].parts[0].widget.answer', 24)
    pb.check_wrongs('problems')
ok_w = ok_w and 'problems-1' in pb.files and got and any(r[0] and 'problems-1' in r[1] for r in pb.results)
print(f"{'PASS' if ok_w else 'FAIL'} check_wrongs: clean passes, in-tolerance fails, other-number byKey listed by hand")
with contextlib.redirect_stdout(io.StringIO()):
    real = Level('odes', 3)
    real.check_wrongs()
ok_w = ok_w and any(r[0] for r in real.results)
if not ok_w:
    sys.exit(1)
# Session V pass 7 (606): hyphenated keys, public claim, stated.
with contextlib.redirect_stdout(io.StringIO()):
    al = Level('alpha', 1)
    h1 = al.expect('l1', 'screens[6].feedback.byKey.test-1', 60)
    c1, c2 = al.claim(1 < 2, 'one below two'), al.claim(2 < 1, 'two below one')
    s_missing = al.stated('l1', 'screens[6].feedback.byKey.test-1', 'a sentence that is not in the text', False)
    s_false = al.stated('l1', 'screens[6].feedback.byKey.test-1', 'no share has 60 days', False)
    s_true = al.stated('l1', 'screens[6].feedback.byKey.test-1', 'no share has 60 days', True)
ok_c = h1 and c1 and not c2 and s_missing and not s_false and s_true
print(f"{'PASS' if ok_c else 'FAIL'} hyphenated key reads, claim records, stated fails only while the false wording is present")
if not ok_c:
    sys.exit(1)
# ENGINE-BACKLOG 1029: check_slips, a slip expression that gives its value, one that gives another, one that does not read, a rounded value
from numbers_lib import slip_eval
sl = Level('odes', 3)
sl.files = {'lx': {'screens': [{'widget': {'kind': 'numeric', 'answer': 1.73, 'tol': {'abs': 0.005}, 'wrong': [
    {'id': 'good', 'value': 0.43, 'tol': {'abs': 0.005}, 'slip': '0.25 * 1.2^3'}, {'id': 'rounded', 'value': 1.4142, 'slip': 'sqrt(2)'},
    {'id': 'bad', 'value': 0.5, 'tol': {'abs': 0.005}, 'slip': '0.25 * 1.2^3'}, {'id': 'prose', 'value': 0.4, 'slip': 'a quarter of it'},
    {'id': 'none', 'value': 9}]}}]}}
with contextlib.redirect_stdout(io.StringIO()):
    n_sl = sl.check_slips()
rs = {r[1].split('"')[1]: r[0] for r in sl.results}
ok_s = n_sl == 4 and rs == {'good': True, 'rounded': True, 'bad': False, 'prose': False} and slip_eval('2^3 + max(1, 2)') == 10 and slip_eval('__import__("os")') is None and slip_eval('1/0') is None
print(f"{'PASS' if ok_s else 'FAIL'} check_slips: matching and rounded expressions pass, a wrong value and unreadable text fail, nothing else is read")
if not ok_s:
    sys.exit(1)
# ENGINE-BACKLOG 1081: slip(), every route of one slip inside its band and outside the key band
sp = Level('odes', 3)
sp.files = {'problems-3': {'items': [{'parts': [{'widget': {'kind': 'numeric', 'answer': 76945, 'tol': {'abs': 5}, 'wrong': [
    {'id': 'inverted', 'value': 59425, 'tol': {'abs': 5}}, {'id': 'near', 'value': 76948, 'tol': {'abs': 1}}]},
    'feedback': {'byKey': {'inverted': 'You divided.'}}}]}]}}
with contextlib.redirect_stdout(io.StringIO()):
    s1 = sp.slip('problems', 'items[0].parts[0]', 'inverted', ('printed', 59425.3), ('unrounded', 59424.1))
    s2 = sp.slip('problems', 'items[0].parts[0]', 'inverted', ('printed', 59425.3), ('from the printed error', 59432))
    s3 = sp.slip('problems', 'items[0].parts[0]', 'near', 76948)
    s4 = sp.slip('problems', 'items[0].parts[0]', 'missing', 1)
    s5 = sp.slip('problems', 'items[0].parts[0].widget', 'inverted', 59425)
ok_p = s1 and not s2 and not s3 and not s4 and s5
print(f"{'PASS' if ok_p else 'FAIL'} slip: routes inside the band pass, a route outside it, a band meeting the key band and an unknown id fail")
if not ok_p:
    sys.exit(1)
# B2-E4: Bank("<file id>") reads items[<item id>] paths; expect with and without the file argument, a wrong id and a missing item fail, check_wrongs runs
from numbers_lib import Bank
with contextlib.redirect_stdout(io.StringIO()):
    bk = Bank('probability-1')
    b1 = bk.expect('items[dice-ev-ten-sided-reroll].widget.answer', 6.75)
    b2 = bk.expect('probability-1', 'items[dice-ev-ten-sided-reroll].widget.answer', 6.75)
    b3 = bk.expect('items[dice-ev-ten-sided-reroll].widget.answer', 6.5)
    b4 = bk.expect('items[no-such-item].widget.answer', 1)
    b5 = bk.expect('items[*].difficulty', 3)
    bk.check_wrongs()
    b6 = bk.claim(True, 'a claim') and not bk.claim(False, 'a false claim')
    b7 = bk.stated('items[dice-ev-ten-sided-reroll].question', 'a sentence that is not in the text', False)
ok_b = b1 and b2 and not b3 and not b4 and b5 and b6 and b7 and any(r[0] for r in bk.results)
print(f"{'PASS' if ok_b else 'FAIL'} Bank: item-id paths, optional file argument, wrong value and missing item fail, claim, stated, check_wrongs")
try:
    Bank('no-such-file')
    ok_b = False
except SystemExit:
    pass
if not ok_b:
    sys.exit(1)
# ENGINE-BACKLOG 1267: coverage of on-screen numbers
def cov_level(**kw):
    c = Level('odes', 3, **kw)
    c.files = {'lx': {'id': 'lx', 'screens': [{'type': 'learn', 'prose': 'In 1999 the fee was £12,500 and the rate 25%. Lesson 3 uses `x = 77` and 2^5.',
        'hints': [{'text': 'Add 4 + 4 + 0 to get 8.'}], 'explain': {'text': 'That is \\tfrac{2}{3}, about 0.67, or 11,000 in round terms.', 'canvas': {'values': {'a': 91}}},
        'widget': {'kind': 'numeric', 'answer': 8, 'starter': 'x = 12345', 'feedback': 'ignored'},
        'canvas': {'params': {'xLabel': 'Day 365', 'points': [{'x': 61, 'label': 'p 0.5'}]}}}]}}
    return c
c = cov_level()
shown = {s_ for _, _, s_ in c.uncovered()}
ok_v = {'12500', '25', '4', '0', '2/3', '0.67', '11000'} <= shown and not ({'1999', '3', '77', '5', '2', '12345', '91', '61', '8', '365', '0.5'} & shown)
with contextlib.redirect_stdout(io.StringIO()):
    c.expect('lx', 'screens[0].prose', 12500)
    c.expect('lx', 'screens[0].prose', 0.25)                           # 25% by value x 100 too
    c.expect('lx', 'screens[0].hints', 4)
    c.claim(True, 'sum', covers=[8, 0, 2 / 3])                         # 2/3 covers "2/3" and "0.67" within the stated precision
c.literal('365', why='a day count from the lesson context')
c.literal(0.5, why='a label read off the chart, not computed')
ok_v = ok_v and {s_ for _, _, s_ in c.uncovered()} == {'11000'}
c.claim(True, 'round', covers=[11018])                                 # 11,000 reads to the thousand
ok_v = ok_v and c.uncovered() == []
# the narrowed filter (1267 follow-up): bare small whole numbers, axis labels and table headers are not claims; words for fractions and multiples, money, units, decimals and arithmetic are
from numbers_lib import _stated
def claims(txt):
    return sorted(round(v, 4) for v, _, _, _, strong in _stated(txt) if strong)
ok_f = (claims('There are 3 emails and 7 words in step 2.') == []
        and claims('That is a third fewer, twice as many, and six times the size.') == [0.3333, 2, 6]
        and claims('It costs £5 and takes 4 bits, 40 ms and 12 s.') == [4, 5, 12, 40]
        and claims('Then 3 + 4 = 7 and 0.5 or 2/3 or 150.') == [0.5, 0.6667, 3, 4, 7, 150]
        and claims('Two thirds of it, a quarter of that.') == [0.25, 0.6667])
ft = Level('odes', 3)
ft.files = {'a': {'screens': [{'prose': 'About a third of it.', 'canvas': {'params': {'xLabel': 'Day 41', 'rows': [['Day', '17']]}}, 'explain': 'It is 31 in all, 3 + 4.'}]},
            'b': {'screens': [{'prose': 'Nothing here.'}]}}
with contextlib.redirect_stdout(io.StringIO()):
    ft.expect('b', 'screens[0].prose', 0.3333)        # a fraction or word must be covered in its own file: file b does not cover file a
    left_f = {s_ for _, _, s_ in ft.uncovered()}
ok_f = ok_f and left_f == {'a third', '31', '3', '4'}
print(f"{'PASS' if ok_f else 'FAIL'} coverage filter: claims are decimals, fractions, words, money, units, arithmetic and big numbers; a fraction is covered in its own file only")
if not ok_f:
    sys.exit(1)
c2 = cov_level()
c2.claim(True, 'near', covers=[12480])                                 # 12,500 reads to the hundred: 12480 does not cover it
ok_v = ok_v and '12500' in {s_ for _, _, s_ in c2.uncovered()}
try:
    c2.literal('1', why='')
    ok_v = False
except ValueError:
    pass
print(f"{'PASS' if ok_v else 'FAIL'} coverage: counts uncovered numbers, skips years, ids, code and exponents, expect, claim covers and literal cover them by precision")
if not ok_v:
    sys.exit(1)
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    cov_level().report()                                               # default: prints, never fails
out1 = buf.getvalue()
ok_r = 'coverage:' in out1 and 'uncovered lx' in out1
with contextlib.redirect_stdout(io.StringIO()):
    try:
        cov_level(coverage='strict').report()
        ok_r = False
    except SystemExit as e:
        ok_r = ok_r and e.code == 1
    os.environ['ZQ_NUMBERS_STRICT'] = '1'
    try:
        cov_level().report()
        ok_r = False
    except SystemExit as e:
        ok_r = ok_r and e.code == 1
    del os.environ['ZQ_NUMBERS_STRICT']
    off = cov_level(coverage='off')
    off.report()
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    off.report()
ok_r = ok_r and 'coverage' not in buf.getvalue()
print(f"{'PASS' if ok_r else 'FAIL'} coverage: warns by default, strict (argument or ZQ_NUMBERS_STRICT=1) fails, off is silent")
if not ok_r:
    sys.exit(1)
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    bad = [
        lv.expect(T, 'screens[3].widget.answer', 4),               # wrong value
        lv.expect(T, 'screens[3].prose', 0.6),
        lv.expect(T, 'screens[99].prose', 1),                      # missing path
        lv.expect(T, 'screens[3].explain', -1.5, fmt='{:.3f}'),    # wrong format
    ]
ok = all(good) and not any(bad)
print(f"{'PASS' if ok else 'FAIL'} numbers_lib: {sum(good)} of {len(good)} real checks pass, {4 - sum(bad)} of 4 wrong checks fail")
try:
    lv.results = [r for r in lv.results if r[0]] + [(False, 'x', '')]
    with contextlib.redirect_stdout(io.StringIO()):
        lv.report()
    ok = False
except SystemExit as e:
    ok = ok and e.code == 1
print(f"{'PASS' if ok else 'FAIL'} report() exits 1 on a failure")
sys.exit(0 if ok else 1)
