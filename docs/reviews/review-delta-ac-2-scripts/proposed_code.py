#!/usr/bin/env python3
"""Delta read AC-2: the hidden tests this review proposes (findings 2 and 3). Each is ADDED, none swapped or removed, so
no candidate that is caught today can pass afterwards. Checked here: the model, my solution (bank_code.MINE is repeated
below) and every right alternative of the earlier readers pass each proposed test; the candidate it is aimed at fails it
and passes every test that stands today; the expect is computed by a brute route.
Usage (repo root, venv python): proposed_code.py      exit 1 on any failure"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'review-delta-bank-2-scripts'))
from code_run_lib import run
from cands import C

MINE = {
 'edge-case-list-second-largest': 'def runner_up_gap(xs):\n    top = second = None\n    for x in xs:\n        if top is None or x > top:\n            top, second = x, top\n        elif x != top and (second is None or x > second):\n            second = x\n    return None if second is None else top - second\n',
 'ds-pointers-merge-ticks': 'def merge_ticks(a, b):\n    pa, pb = dict(a), dict(b)\n    return [(t, (pa[t] + pb[t]) / 2 if t in pa and t in pb else pa.get(t, pb.get(t))) for t in sorted(set(pa) | set(pb))]\n',
}
PROPOSED = {
 'edge-case-list-second-largest': (2, [
   ({"call": "runner_up_gap([7, 0, 7])", "expect": "7", "compare": "equal"}, lambda: sorted({7, 0, 7})[-1] - sorted({7, 0, 7})[-2],
    [('falsy-second', 'def runner_up_gap(xs):\n    d = sorted(set(xs), reverse=True)\n    second = d[1] if len(d) > 1 else None\n    return d[0] - second if second else None\n')]),
 ]),
 'ds-pointers-merge-ticks': (2, [
   ({"setup": "a = [(1, 1.0), (3, 1.0)]; b = [(2, 2.0)]", "call": "(merge_ticks(a, b), a, b)", "expect": "([(1, 1.0), (2, 2.0), (3, 1.0)], [(1, 1.0), (3, 1.0)], [(2, 2.0)])", "compare": "equal"},
    lambda: (sorted([(1, 1.0), (3, 1.0)] + [(2, 2.0)]), [(1, 1.0), (3, 1.0)], [(2, 2.0)]),
    [('alias-when-no-shared-time', 'def merge_ticks(a, b):\n    shared = {t for t, _ in a} & {t for t, _ in b}\n    if not shared:\n        out = a\n        out += b\n        return sorted(out)\n    d = dict(a)\n    for t, p in b: d[t] = (d[t] + p) / 2 if t in d else p\n    return sorted(d.items())\n')]),
 ]),
}

bad = False
for iid, (n, props) in PROPOSED.items():
    w = next(it for it in json.load(open(f'app/content/bank/coding-{n}.json'))['items'] if it['id'] == iid)['widget']
    print(f'## coding-{n} {iid}: {len(w["tests"])} tests today, {len(w["tests"]) + len(props)} with the proposed ones')
    for case, brute, aimed in props:
        env = {}
        exec(case.get('setup', ''), env)
        exp = eval(case['expect'], env)
        b = brute()
        okb = exp == b or list(exp) == list(b)
        rights = [('model', w['solution']), ('mine', MINE[iid])] + [(nm, src) for nm, _, src in C[iid] if nm.startswith('alt:')]
        res = {nm: run(src, [case])[0][0] for nm, src in rights}
        print(f'  {case["call"][:60]} -> {case["expect"][:60]}: brute {"agrees" if okb else "DISAGREES"}; right solutions pass: {res}')
        bad |= not okb or not all(res.values())
        for nm, src in aimed:
            today = [i + 1 for i, x in enumerate(run(src, w['tests'])) if not x[0]]
            new = run(src, [case])[0]
            print(f'    aimed at {nm}: fails today\'s tests {today or "none (passes all)"}; on the proposed test returns {new[2]} ({"caught" if not new[0] else "NOT CAUGHT"})')
            bad |= bool(today) or new[0]
print('exit', 1 if bad else 0)
sys.exit(1 if bad else 0)
