"""Second-reader harness for the 30 `py` pack drills.

Run from the repo root with the scratchpad venv Python:
    python docs/reviews/drills-py-scripts/harness.py mine     # my own solutions on every example and test
    python docs/reviews/drills-py-scripts/harness.py wrong    # unplanted wrong candidates
    python docs/reviews/drills-py-scripts/harness.py model    # the drill's own solution (sanity)
    python docs/reviews/drills-py-scripts/harness.py extra    # proposed tests: model, mine and each candidate

Each case is judged as js/screens/drill.js judges it (`__zq_eq`): learner code first,
then the prelude, then `eval(call)` against `eval(expect)`.
"""
import glob, json, math, os, shutil, sys, tempfile, warnings, importlib.util

warnings.simplefilter('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
DRILLS = os.path.join(ROOT, 'app', 'content', 'drills')


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def zq_eq(a, e, mode):
    if mode == 'isclose':
        if e is None:
            return a is None
        if isinstance(e, (list, tuple)):
            return isinstance(a, (list, tuple)) and len(a) == len(e) and all(zq_eq(x, y, mode) for x, y in zip(a, e))
        if isinstance(a, bool) or not isinstance(a, (int, float)):
            return False
        return math.isclose(a, e, rel_tol=1e-9, abs_tol=1e-12)
    return bool(a == e)


def drills():
    out = {}
    for f in sorted(glob.glob(os.path.join(DRILLS, 'py-*.json'))):
        d = json.load(open(f))
        if d.get('pack') == 'py':
            out[d['id']] = d
    return out


def env(d, code):
    g = {'__name__': 'solution'}
    exec(code, g)
    if d.get('prelude'):
        exec(d['prelude'], g)
    return g


def run_case(d, code, case):
    """Return (ok, shown). A fresh namespace per case, as a planted default list needs one run."""
    try:
        g = run_case.cache.get((d['id'], code))
        if g is None:
            g = run_case.cache[(d['id'], code)] = env(d, code)
        actual = eval(case['call'], g)
        expected = eval(case['expect'], g)
        return zq_eq(actual, expected, case.get('compare', 'isclose')), repr(actual)[:160]
    except BaseException as e:  # noqa
        return False, f'{type(e).__name__}: {e}'[:160]


run_case.cache = {}


def run_all(d, code):
    """Indices of failing examples (e*) and tests (t*)."""
    run_case.cache.pop((d['id'], code), None)
    fails = []
    for tag, cases in (('e', d.get('examples', [])), ('t', d['tests'])):
        for i, c in enumerate(cases):
            ok, shown = run_case(d, code, c)
            if not ok:
                fails.append((f'{tag}{i}', shown))
    return fails


def main():
    what = sys.argv[1]
    ds = drills()
    work = tempfile.mkdtemp()
    for d in ds.values():
        for name, src in (d.get('data') or {}).items():
            shutil.copy(os.path.join(ROOT, 'app', src), os.path.join(work, name))
    os.chdir(work)
    bad = 0
    if what in ('mine', 'model'):
        mine = load('mine').SOLUTIONS if what == 'mine' else {k: v['solution'] for k, v in ds.items()}
        for k, d in ds.items():
            fails = run_all(d, mine[k])
            n = len(d.get('examples', [])) + len(d['tests'])
            print(f'{k:26} {n - len(fails):2}/{n}', '' if not fails else fails)
            bad += bool(fails)
        print(f'{len(ds)} drills, {bad} with a disagreement')
    elif what == 'wrong':
        passed = 0
        cands = load('wrong').CANDIDATES
        for k, label, code in cands:
            fails = run_all(ds[k], code)
            hidden = [f for f in fails if f[0].startswith('t')]
            verdict = 'PASSES EVERY TEST' if not hidden else 'caught by ' + ','.join(f[0] for f in hidden)
            passed += not hidden
            print(f'{k:26} {label:52} {verdict}')
        print(f'{len(cands)} candidates, {passed} pass every hidden test')
    elif what == 'extra':
        mine = load('mine').SOLUTIONS
        cands = load('wrong').CANDIDATES
        extra = json.load(open(os.path.join(HERE, 'extra_tests.json')))
        for k, cases in extra.items():
            d = ds[k]
            for c in cases:
                row = []
                right = ['model', 'mine'] + c.get('also_passes', [])
                named = c.get('catches', []) + c.get('also_passes', [])
                for who, code in [('model', d['solution']), ('mine', mine[k])] + [(l, s) for kk, l, s in cands if kk == k and l in named]:
                    run_case.cache.pop((k, code), None)
                    ok, shown = run_case(d, code, c)
                    row.append(f'{who}: {"ok" if ok else "FAIL"} {shown}')
                    if (who in right) != ok:
                        bad += 1
                print(k, '|', c['call'][:90], '->', c['expect'])
                for r in row:
                    print('     ', r)
        print('extra tests: problems', bad)
    shutil.rmtree(work, ignore_errors=True)
    sys.exit(1 if bad and what != 'wrong' else 0)


if __name__ == '__main__':
    main()
