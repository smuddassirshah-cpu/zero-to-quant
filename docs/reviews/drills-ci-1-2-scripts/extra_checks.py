"""Proposed new hidden tests: value by the model solution and by mine.py, and what wrong.py returns.

usage: extra_checks.py <drills dir>   (run from the repo root)
"""
import glob
import importlib.util
import itertools
import json
import os
import signal
import sys
import time

here = os.path.dirname(os.path.abspath(__file__))


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(here, name + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


mine, wrong = load("mine"), load("wrong")
model = {}
for f in glob.glob(sys.argv[1] + "/ci-*.json"):
    d = json.load(open(f))
    ns = {}
    if not ({"pack-1", "pack-2"} & set(d["tags"])):
        continue
    exec(d["solution"], ns)
    model[d["fn"]] = ns[d["fn"]]

# a 2 by 2 grid where gluing digits makes a false row and column match
glue = None
for cells in itertools.product([1, 2, 11, 12, 21, 111], repeat=4):
    grid = [list(cells[:2]), list(cells[2:])]
    if wrong.count_row_column_matches(grid) != model["count_row_column_matches"](grid):
        glue = grid
        break

NEW = [
    ("best_block_sum", "best_block_sum([[-10 ** 6] * 40 for _ in range(40)], 40)"),
    ("best_signal_pair", "best_signal_pair([(0, 0), (1, 0), (10, 5), (11, 0)], 2)"),
    ("count_row_column_matches", "count_row_column_matches(%r)" % (glue,)),
    ("fewest_end_lots", "fewest_end_lots([2, 3], 7)"),
    ("fewest_end_lots", "fewest_end_lots([3], 6)"),
    ("longest_after_swaps", "longest_after_swaps('XAAAY', 2)"),
    ("longest_serial_run", "longest_serial_run([0] * 100000 + list(range(100000)))"),
    ("netting_triples", "netting_triples([-5, -3, -2, 1], -10)"),
    ("others_product_grid", "(lambda t: [len(t), t[0][:4], sum(map(sum, t))])(others_product_grid([[3] * 1000 for _ in range(100)]))"),
    ("shortest_peak_stretch", "shortest_peak_stretch([2, 2, 1, 3, 1])"),
    ("solve_equal_three", "solve_equal_three('21\\n' + 'A' * 11 + 'B' * 10 + '\\n')"),
    ("count_target_blocks", "count_target_blocks([[(r * 7 + c * 3) % 5 - 2 for c in range(400)] for r in range(60)], 0)"),
    ("longest_capped_run", "longest_capped_run(['a', 'b', 'a', 'a', 'c', 'b'], 2)"),
    ("shortest_cut_to_multiple", "shortest_cut_to_multiple([4, 3, 1], 5)"),
]


class Slow(Exception):
    pass


def alarm(*_):
    raise Slow()


signal.signal(signal.SIGALRM, alarm)
for fn, call in NEW:
    row = []
    for who, f in (("model", model[fn]), ("mine", getattr(mine, fn)), ("wrong", getattr(wrong, fn))):
        t = time.time()
        signal.setitimer(signal.ITIMER_REAL, 20)
        try:
            v = repr(eval(call, {fn: f}))[:60]
        except Slow:
            v = "over 20 s"
        signal.setitimer(signal.ITIMER_REAL, 0)
        row.append("%s %s (%.2fs)" % (who, v, time.time() - t))
    print(call[:100], "\n    ", " | ".join(row))
