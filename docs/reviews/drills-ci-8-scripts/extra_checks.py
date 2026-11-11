"""Checks on the tests proposed in extra_tests.json, and small facts quoted in the review.
usage: extra_checks.py <drills dir> [repo root] [--proposed]   (--proposed: only drills with proposed tests)
"pass now" counts the hidden tests only, which is what Submit runs; the examples are not in it.
1. every proposed test: model, my solution and my brute force agree with its expect, and its
   arguments are inside the constraints;
2. with the proposed tests added (and the test named in "replaces" dropped), the model still
   passes, and every planted solution, every one of the author's 83 (drills-ci-8-wrong.py) and
   every one of my wrong candidates fails a test (value, exception or over 4 s on one test);
3. which hidden tests are the only one to catch some candidate (so which can be replaced);
4. `how` test counts, and how far from the end of the list the double-checks model inserts."""
import importlib.util
import json
import multiprocessing as mp
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import checks  # noqa: E402


def _kills(code, tests, q):
    env = {}
    out = []
    try:
        exec(code, env)
    except Exception:
        q.put(['load'])
        return
    for i, t in enumerate(tests):
        try:
            if eval(t['call'], env) != eval(t['expect'], env):
                out.append(i)
        except BaseException:  # noqa
            out.append(i)
        q.put(('p', i, i in out))
    q.put(('done',))


def kills(code, tests, per_test=4):
    """indices of the tests the code fails; a test still running after per_test seconds counts, and ends the run"""
    q = mp.Queue()
    p = mp.Process(target=_kills, args=(code, tests, q))
    p.start()
    failed = []
    nxt = 0
    while True:
        try:
            m = q.get(timeout=per_test)
        except Exception:
            failed.append(nxt)          # slow on test nxt
            p.terminate()
            break
        if m == ['load']:
            failed = list(range(len(tests)))
            break
        if m[0] == 'done':
            break
        if m[2]:
            failed.append(m[1])
        nxt = m[1] + 1
    p.join()
    return failed


if __name__ == '__main__':
    drills = checks.load(sys.argv[1])
    root = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else os.path.join(HERE, '..', '..', '..')
    extra = json.load(open(os.path.join(HERE, 'extra_tests.json')))
    mine = {}
    exec(open(os.path.join(HERE, 'mine.py')).read(), mine)
    w = {}
    exec(open(os.path.join(HERE, 'wrong.py')).read(), w)
    spec = importlib.util.spec_from_file_location('aw', os.path.join(root, 'docs', 'reports', 'drills-ci-8-wrong.py'))
    aw = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(aw)
    bad = 0
    for did, j in drills.items():
        if '--proposed' in sys.argv and did not in extra:
            continue
        fn = j['fn']
        cands = [('planted[%d]' % i, p['code']) for i, p in enumerate(j['planted'])]
        cands += [('author:' + what[:40], code) for code, what in aw.WRONG[did]]
        cands += [(lab, code) for lab, (d2, code, _) in w['CANDIDATES'].items() if d2 == did and not lab.startswith('robot_blocked_keeps')]
        new = extra.get(did, [])
        # 1
        m = {}
        exec(j['solution'], m)
        for t in new:
            got = []
            eval(t['call'], {fn: lambda *a: got.append(a) or None})
            args = got[0]
            want = eval(t['expect'])
            res = (m[fn](*args), mine[fn](*args), getattr(checks, 'b_' + fn)(*args))
            errs = checks.prose(did, args)
            if not (res[0] == res[1] == res[2] == want) or errs:
                bad += 1
                print('  BAD proposed test', did, t['call'][:80], res, want, errs)
        # 2 and 3
        tests = list(j['tests'])
        drop = sorted({t['replaces'] for t in new if 'replaces' in t}, reverse=True)
        base = {lab: kills(code, tests) for lab, code in cands}
        only = {}
        for lab, ks in base.items():
            if len(ks) == 1:
                only.setdefault(ks[0], []).append(lab)
        passing_now = [lab for lab, ks in base.items() if not ks]
        tests2 = [t for i, t in enumerate(tests) if i not in drop] + [{k: t[k] for k in ('call', 'expect')} for t in new]
        after = {lab: kills(code, tests2) for lab, code in cands} if new else base
        still = [lab for lab, ks in after.items() if not ks]
        model_fails = kills(j['solution'], tests2)
        if still or model_fails:
            bad += 1
        print('%-20s %2d tests, %2d candidates | pass now: %s | sole catchers: %s | proposed +%d -%s -> %d tests, model fails %s, still passing: %s' % (
            did, len(tests), len(cands), passing_now or 'none',
            ' '.join('t%d(%d)' % (k, len(v)) for k, v in sorted(only.items())) or 'none',
            len(new), drop or '[]', len(tests2), model_fails or 'none', still or 'none'))
    # 4
    import re
    for did, j in drills.items():
        n = re.search(r'Submit runs (\d+) hidden tests', j['how'])
        if not n or int(n.group(1)) != len(j['tests']):
            bad += 1
            print('  how count differs', did)
    import bisect
    worst = 0
    j = drills['ci-double-checks']
    for t in j['tests']:
        got = []
        eval(t['call'], {'fewest_checks': lambda a: got.append(a) or 0})
        marks = []
        for start, end, need in sorted(got[0], key=lambda job: (job[1], -job[0])):
            have = bisect.bisect_right(marks, end) - bisect.bisect_left(marks, start)
            minute = end
            while have < need:
                i = bisect.bisect_left(marks, minute)
                if i == len(marks) or marks[i] != minute:
                    worst = max(worst, len(marks) - i)
                    marks.insert(i, minute)
                    have += 1
                minute -= 1
    print('double checks: an insert is at most %d places from the end of the list, over all hidden tests' % worst)
    print('%d problems' % bad)
