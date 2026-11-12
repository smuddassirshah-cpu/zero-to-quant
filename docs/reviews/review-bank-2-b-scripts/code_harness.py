"""Second reader, bank part 2 (b): run my own solutions and candidate-wrong solutions against the examples and hidden tests
of the 24 Python code tasks. The judge copies the engine's rule (app/js/engine/widgets/code.js __zq_judge): "equal" lets a
list equal a tuple and 2 equal 2.0, a dict compares by key set then value; "fraction" needs a Fraction instance.
Usage: code_harness.py [n ...]   (file numbers; default all four). Exit 1 if one of MY solutions fails a test or the model fails.
Candidates live in cands_<n>.py as CANDS = {item id: {'mine': src, 'wrong': [(name, why it is wrong or risky, src), ...]}}.
A wrong candidate that passes every hidden test is printed as PASSES: each is a finding (or is argued not to be one in the review).
A name that starts "alt:" is another right solution; it is not counted as a candidate, and it must pass (ALT FAILS is a finding on the tests)."""
import copy, importlib, json, os, signal, sys, time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'bank')
sys.setrecursionlimit(3000)  # the page sets 3,000 at the start of every run (AUTHORING.md, Deep recursion)
SLOW = 1.0  # CPython seconds for one case; the page allows 5 s a case in Pyodide, which runs about 3 to 5 times slower
STOP = 4.0  # a case is stopped here and counted as failed (as the page stops it at 5 s)


class Stopped(BaseException):
    pass


def _alarm(*_):
    raise Stopped()


signal.signal(signal.SIGALRM, _alarm)


def same(x, y):
    if isinstance(x, dict) or isinstance(y, dict):
        return isinstance(x, dict) and isinstance(y, dict) and set(x) == set(y) and all(same(x[k], y[k]) for k in x)
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(same(p, q) for p, q in zip(x, y))
    try:
        if x != x and y != y:
            return True
    except Exception:
        pass
    return bool(x == y)


def judge(a, e, cmp_):
    if cmp_ == 'fraction':
        return isinstance(a, Fraction) and a == e
    if cmp_ == 'equal':
        return same(a, e)
    raise ValueError('compare mode not handled here: ' + cmp_)


def run(src, cases):
    """returns a list of (ok, seconds, shown) per case."""
    out = []
    ns = {}
    try:
        exec(src, ns)
    except Exception as x:
        return [(False, 0, 'load error ' + repr(x))] * len(cases)
    for c in cases:
        env = dict(ns)
        t = time.perf_counter()
        signal.setitimer(signal.ITIMER_REAL, STOP)
        try:
            if c.get('setup'):
                exec(c['setup'], env)
            a = eval(c['call'], env)
            dt = time.perf_counter() - t
            e = eval(c['expect'], env)
            out.append((judge(a, e, c.get('compare', 'equal')), dt, repr(a)[:60]))
        except Stopped:
            out.append((False, time.perf_counter() - t, f'stopped after {STOP:.0f} s'))
        except RecursionError:
            out.append((False, time.perf_counter() - t, 'RecursionError'))
        except Exception as x:
            out.append((False, time.perf_counter() - t, 'raised ' + type(x).__name__))
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
    return out


def main():
    nums = [int(a) for a in sys.argv[1:]] or [1, 2, 3, 4]
    bad = False
    rows = []
    for n in nums:
        items = {it['id']: it for it in json.load(open(os.path.join(ROOT, f'coding-{n}.json')))['items'] if it['widget']['kind'] == 'code'}
        cands = importlib.import_module(f'cands_{n}').CANDS
        assert set(cands) == set(items), set(items) ^ set(cands)
        for iid, it in items.items():
            w = it['widget']
            ex, tests = w['examples'], w['tests']
            print(f'\n## coding-{n} {iid}  ({len(tests)} hidden tests)')
            for nm, src in (('model', w['solution']), ('mine', cands[iid]['mine'])):
                r = run(src, ex + tests)
                okc = sum(1 for x in r if x[0])
                worst = max(x[1] for x in r)
                print(f'  {nm:6} passes {okc} of {len(r)} (examples and tests), slowest case {worst:.3f} s')
                if okc != len(r):
                    bad = True
                    for c, x in zip(ex + tests, r):
                        if not x[0]:
                            print(f'    DISAGREE {c["call"][:70]} expected {c["expect"][:40]} got {x[2]}')
            r = run(w['starter'], tests)
            if all(x[0] for x in r):
                bad = True
                print('  STARTER PASSES')
            tried = passing = 0
            names = []
            for nm, why, src in cands[iid]['wrong']:
                r = run(src, tests)
                if nm.startswith('alt:'):  # another right solution (or right within the stated sizes): it must pass
                    f = [i + 1 for i, x in enumerate(r) if not x[0]]
                    print(f'  {"alt ok " if not f else "ALT FAILS"} {nm[4:]}: {why}' + (f' fails tests {f}: {[x[2] for x in r if not x[0]][:2]}' if f else '') + f' (slowest case {max(x[1] for x in r):.2f} s)')
                    continue
                tried += 1
                rex = run(src, ex)
                fails = [i + 1 for i, x in enumerate(r) if not x[0]]
                worst = max(x[1] for x in r)
                slow = f', slowest case {worst:.2f} s' if worst > 0.05 else ''
                if not fails and worst <= SLOW:
                    passing += 1
                    names.append(nm)
                    print(f'  PASSES  {nm}: {why}{slow}')
                elif not fails:
                    print(f'  slow    {nm}: right answers, slowest case {worst:.2f} s in CPython (limit 5 s in the page): {why}')
                else:
                    stopped = ' (stopped for time)' if any('stopped' in x[2] for x in r) else ''
                    print(f'  caught  {nm}: fails tests {fails}{stopped}' + ('' if all(x[0] for x in rex) else ' and an example') + slow)
            rows.append((f'coding-{n}', iid, tried, passing, ', '.join(names)))
    print('\n| File | Task | Candidates tried | Passing every hidden test | Which |\n| --- | --- | --- | --- | --- |')
    for r in rows:
        print('| ' + ' | '.join(str(x) for x in r) + ' |')
    print(f'\ntotal tried {sum(r[2] for r in rows)}, passing {sum(r[3] for r in rows)}')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
