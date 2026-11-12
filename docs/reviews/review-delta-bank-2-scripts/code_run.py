#!/usr/bin/env python3
"""Delta read, code tasks: the reader's blind solutions (mine.py), the models, the starters and the candidates (cands.py)
against the examples and hidden tests as they stand, plus the tests proposed in the review (PROPOSED below).
The judge follows app/js/engine/widgets/code.js __zq_judge for "equal" and "fraction" (a list equals a tuple, 2 equals 2.0,
dicts by key set then value). Recursion limit 3,000 as the page sets it. A case is stopped at 4 s of CPython (the page stops
a case at 5 s in Pyodide, which is several times slower), and a right answer that needs more than 1 s is printed as slow.
Usage (repo root): python docs/reviews/review-delta-bank-2-scripts/code_run.py [id ...]
Exit 1 if a model or one of my solutions fails a case, a starter passes, a `how` count is off, an "alt:" (right) solution
gives a wrong answer, or a proposed test fails a right solution or passes its candidate."""
import glob, json, os, re, signal, sys, time
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from mine import MINE
from cands import C
from code_run_lib import run, SLOW, STOP


# Tests proposed in the review: each must pass the model, my solution and every right alternative, and fail the named candidates.
PROPOSED = {
    'ds-pointers-merge-ticks': [({"setup": "a = [(1, 4.0), (2, 1.0)]; b = [(1, 2.0), (3, 5.0)]", "call": "(merge_ticks(a, b), a, b)",
                                  "expect": "([(1, 3.0), (2, 1.0), (3, 5.0)], [(1, 4.0), (2, 1.0)], [(1, 2.0), (3, 5.0)])", "compare": "equal"},
                                 ['mutate-on-shared', 'delete-from-b'])],
    'pf-idioms-count-above-mean': [({"call": "above_mean([0, 6, 10, 10, 10])", "expect": "3", "compare": "equal"}, ['midrange'])],
    'edge-case-list-second-largest': [({"call": "runner_up_gap([-1, -5, -2])", "expect": "1", "compare": "equal"}, ['abs-values'])],
    'edge-case-list-to-pence': [({"call": "to_pence(\" -£2.05 \")", "expect": "-205", "compare": "equal"}, ['sign-before-strip', 'no-strip-at-all'])],
}


def main():
    items = {}
    for f in sorted(glob.glob(os.path.join(HERE, '..', '..', '..', 'app', 'content', 'bank', 'coding-*.json'))):
        for it in json.load(open(f))['items']:
            if it['widget']['kind'] == 'code':
                items[it['id']] = (os.path.basename(f)[:-5], it)
    ids = sys.argv[1:] or list(C)
    bad = False
    rows = []
    for iid in ids:
        f, it = items[iid]
        w = it['widget']
        ex, tests = w['examples'], w['tests']
        print(f'\n## {f} {iid} ({len(tests)} hidden tests; how: {w.get("how")})')
        m = re.search(r'runs (\d+) hidden', w.get('how', ''))
        if not m or int(m.group(1)) != len(tests):
            print('  HOW LINE DISAGREES with', len(tests))
            bad = True
        for nm, src in (('model', w['solution']), ('mine', MINE[iid])):
            r = run(src, ex + tests)
            ok = sum(x[0] for x in r)
            print(f'  {nm:5} {ok} of {len(r)} examples and tests, slowest case {max(x[1] for x in r):.3f} s')
            if ok != len(r):
                bad = True
                for c, x in zip(ex + tests, r):
                    if not x[0]:
                        print('    DISAGREE', c['call'][:80], 'expected', c['expect'][:50], 'got', x[2])
        if all(x[0] for x in run(w['starter'], tests)):
            bad = True
            print('  STARTER PASSES')
        tried = 0
        passing, slowright = [], []
        for nm, why, src in C[iid]:
            r = run(src, tests)
            fails = [i + 1 for i, x in enumerate(r) if not x[0]]
            worst = max(x[1] for x in r)
            wrongans = [i + 1 for i, x in enumerate(r) if not x[0] and x[2] != 'stopped']
            if nm.startswith('alt:'):
                if wrongans:
                    bad = True
                tag = 'ALT WRONG' if wrongans else ('alt STOPPED' if fails else ('alt slow' if worst > SLOW else 'alt ok'))
                if tag != 'alt ok':
                    slowright.append(nm[4:])
                print(f'  {tag:11} {nm[4:]}: {why} (fails {fails}, slowest {worst:.2f} s)')
                continue
            tried += 1
            if not fails:
                passing.append(nm)
                print(f'  PASSES      {nm}: {why} (slowest {worst:.2f} s)')
            else:
                print(f'  caught      {nm}: tests {fails}' + ('' if wrongans else ' (for time only)'))
        for case, names in PROPOSED.get(iid, []):
            ok = all(run(s, [case])[0][0] for s in (w['solution'], MINE[iid]))
            res = {n: run(next(s for m_, _, s in C[iid] if m_ == n), [case])[0][0] for n in names}
            alts = {m_[4:]: run(s, [case])[0][0] for m_, _, s in C[iid] if m_.startswith('alt:')}
            print(f'  PROPOSED    {case["call"][:60]}: model and mine pass {ok}; candidates pass {res}; right alternatives pass {alts}')
            if not ok or any(res.values()) or not all(alts.values()):
                bad = True
        rows.append((f, iid, tried, len(passing), ', '.join(passing) or '-', ', '.join(slowright) or '-'))
    print('\n| File | Task | Candidates | Pass every hidden test | Which | Right but slow or stopped |\n| --- | --- | --- | --- | --- | --- |')
    for r in rows:
        print('| ' + ' | '.join(str(x) for x in r) + ' |')
    print(f'\ntried {sum(r[2] for r in rows)}, passing {sum(r[3] for r in rows)}; exit {1 if bad else 0}')
    sys.exit(1 if bad else 0)


main()
