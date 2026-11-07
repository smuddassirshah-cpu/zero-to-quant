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
