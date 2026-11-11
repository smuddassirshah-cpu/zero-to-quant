"""Findings 1 to 4: the same large tests at half the size, so that a remembered
recursion written with functools.lru_cache stays under 300 calls deep.
Computes each replacement's expect with the model solution and with mine.py
(they must agree), checks the slow plant of the drill still fails, and writes
resize_tests.json: {drill id: {"<test index>": {call, expect, compare}}}.

usage: resize.py <drills dir>            write resize_tests.json and print it
       resize.py <drills dir> --apply <copy of app> <label> ...
           put the replacements into the copy, with the named right top-down
           candidates (wrong2.py, wrong3.py) as `planted`; then planted-check on
           the copy must report every one of them as "passes all" and the model
           as passing."""
import json
import multiprocessing as mp
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
D = sys.argv[1]
mine = {}
exec(open(os.path.join(HERE, 'mine.py')).read(), mine)

NEW = {
    'ci-merged-tape': {
        11: "merge_ways('a' * 150, 'a' * 150, 'a' * 300)",
        12: "merge_ways(''.join('ab'[(i * i) % 7 % 2] for i in range(150)), ''.join('ab'[(i * 3) % 5 % 2] for i in range(150)), ''.join('ab'[(i * i) % 7 % 2] for i in range(75)) + ''.join('ab'[(i * 3) % 5 % 2] for i in range(150)) + ''.join('ab'[(i * i) % 7 % 2] for i in range(75, 150)))",
        13: "merge_ways('ab' * 75, 'ba' * 75, 'ab' * 150)",
        14: "merge_ways('a' * 150, 'a' * 149, 'a' * 300)",
    },
    'ci-mirror-pieces': {
        9: "solve_mirror_pieces('5\\n' + '\\n'.join(['a' * 150, 'ab' * 75, 'abc' * 50, 'a' * 74 + 'b' + 'a' * 75, 'ba' + 'a' * 148]) + '\\n')",
        10: "solve_mirror_pieces('7\\n' + '\\n'.join(''.join('ab'[(i * j * j + j) % 3 % 2] for j in range(150)) for i in range(7)) + '\\n')",
        12: "solve_mirror_pieces('3\\n' + '\\n'.join(['ab' * 74 + 'a', 'aab' * 50, 'z' * 150]) + '\\n')",
        13: "solve_mirror_pieces('2\\nabaaabba\\n' + ''.join('abc'[(i * i + i // 7) % 3] for i in range(150)) + '\\n')",
    },
    'ci-priced-edits': {
        10: "solve_priced_edits('2 5 3\\n1\\n' + ''.join('xyz'[(j * j) % 3] for j in range(150)) + ' ' + ''.join('xyz'[(j * 7 + 1) % 3] for j in range(150)) + '\\n')",
    },
    'ci-tolerant-common': {
        10: "tolerant_common([(i * 7919) % 1009 for i in range(150)], [(i * 104729 + 17) % 1013 for i in range(150)], 4)",
        11: "tolerant_common([(i * i * 31) % 997 for i in range(150)], [(i * i * 37 + 5) % 991 for i in range(140)], 0)",
    },
}
SLOW = {'ci-merged-tape': 3, 'ci-mirror-pieces': 3}      # index of the slow plant


def _all(src, tests, q):
    env = {}
    exec(src, env)
    for t in tests:
        if eval(t['call'], env) != eval(t['expect']):
            q.put('wrong value')
            return
    q.put('passes')


def build():
    out = {}
    for did, repl in NEW.items():
        j = json.load(open(os.path.join(D, did + '.json')))
        env = {}
        exec(j['solution'], env)
        out[did] = {}
        for i, call in repl.items():
            a = eval(call, env)
            b = eval(call, {j['fn']: mine[j['fn']]})
            assert a == b, (did, i, a, b)
            out[did][str(i)] = {'call': call, 'expect': repr(a), 'compare': 'equal'}
        tests = list(j['tests'])
        for i, t in out[did].items():
            if int(i) < len(tests):
                tests[int(i)] = t
            else:
                tests.append(t)
        if did in SLOW:
            q = mp.Queue()
            p = mp.Process(target=_all, args=(j['planted'][SLOW[did]]['code'], tests, q))
            p.start()
            p.join(12)
            alive = p.is_alive()
            if alive:
                p.terminate()
            print(did, 'slow plant on the resized tests:', 'still running at 12 s' if alive else q.get())
    return out


if '--apply' in sys.argv:
    k = sys.argv.index('--apply')
    app, labels = os.path.abspath(sys.argv[k + 1]), sys.argv[k + 2:]
    assert app != os.path.abspath(os.path.join(HERE, '..', '..', '..', 'app')), 'use a copy'
    cands = {}
    for name in ('wrong.py', 'wrong2.py', 'wrong3.py'):
        e = {}
        exec(open(os.path.join(HERE, name)).read(), e)
        cands.update(e['CANDIDATES'])
    res = json.load(open(os.path.join(HERE, 'resize_tests.json')))
    for did, repl in res.items():
        f = os.path.join(app, 'content', 'drills', did + '.json')
        d = json.load(open(f))
        for i, t in repl.items():
            if int(i) < len(d['tests']):
                d['tests'][int(i)] = t
            else:
                d['tests'].append(t)
        d['planted'] = [{'code': cands[x][1].strip() + '\n', 'slip': x} for x in labels if cands[x][0] == did]
        json.dump(d, open(f, 'w'), indent=2)
        print(did, len(d['tests']), 'tests', [p['slip'] for p in d['planted']])
else:
    out = build()
    json.dump(out, open(os.path.join(HERE, 'resize_tests.json'), 'w'), indent=2)
    for did, repl in out.items():
        for i, t in repl.items():
            print(did, i, t['call'][:70], '=>', t['expect'][:80])
