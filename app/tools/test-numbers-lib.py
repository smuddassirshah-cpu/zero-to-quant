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
assert normalise('£1{,}214 and −3') == '1214 and -3'
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
