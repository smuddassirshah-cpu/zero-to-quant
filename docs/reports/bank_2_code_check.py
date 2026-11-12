"""Shared checks for the coding files of bank part 2 (imported by bank-2-s1-numbers.py and bank-2-s2-numbers.py).

Standard library only. It runs a bank `code` item's model solution, starter, brute-force twin and named near-miss
methods against the item's own examples and hidden tests, with the same comparison as the app's harness
(app/js/engine/widgets/code.js, __zq_judge: lists and tuples alike, dicts by key set, `fraction` needs a Fraction)
and a 5 s limit per case (the app's default). CPython is faster than Pyodide, so a near-miss that runs out of time
here runs out of time in the browser too. It also runs the fenced snippets of reasoning-about-code items and
compiles C++ with g++ -std=c++20 (skipped with a printed warning, not a pass, when no compiler is present).
"""
import os, re, shutil, signal, subprocess, tempfile
from fractions import Fraction

LIMIT = 5.0


class _Timeout(Exception):
    pass


def _alarm(_s, _f):
    raise _Timeout()


def _same(x, y):
    if hasattr(x, 'tolist') and not isinstance(x, (int, float, complex, str)):
        x = x.tolist()
    if isinstance(x, dict) or isinstance(y, dict):
        return isinstance(x, dict) and isinstance(y, dict) and set(x) == set(y) and all(_same(x[k], y[k]) for k in x)
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(_same(p, q) for p, q in zip(x, y))
    return bool(x == y)


def judge(a, e, cmp):
    if cmp == 'fraction':
        return isinstance(a, Fraction) and a == e
    return _same(a, e)


def _timed(fn, limit=LIMIT):
    old = signal.signal(signal.SIGALRM, _alarm)
    signal.setitimer(signal.ITIMER_REAL, limit)
    try:
        return fn()
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old)


def run(src, cases, limit=LIMIT):
    """[(passed, actual or 'raised X' or 'timed out')] for each case, in a fresh namespace per source."""
    ns = {'__name__': '__learner__'}
    try:
        _timed(lambda: exec(src, ns), limit)
    except _Timeout:
        return [(False, 'timed out loading')] * len(cases)
    except Exception as x:
        return [(False, f'raised {type(x).__name__} loading')] * len(cases)
    out = []
    for c in cases:
        try:
            if c.get('setup'):
                exec(c['setup'], ns)
            a = _timed(lambda: eval(c['call'], ns), limit)
        except _Timeout:
            out.append((False, 'timed out'))
            continue
        except Exception as x:
            out.append((False, f'raised {type(x).__name__}'))
            continue
        try:
            e = eval(c['expect'], ns)
        except Exception as x:  # the app's harness raises here too, and the case fails
            out.append((False, f'expect raised {type(x).__name__}'))
            continue
        out.append((judge(a, e, c.get('compare', 'equal')), a))
    return out


def fname_of(src):
    m = re.search(r'^def (\w+)\(', src, re.M)
    return m.group(1) if m else None


def check_code(ok, lab, it, brute, traps):
    """ok: the script's assert-and-count function. brute: source of a separate method (route B). traps: {name: source}
    of near-miss methods, each of which must fail at least one hidden test. Returns the hidden-test results."""
    w = it['widget']
    ok(w['kind'] == 'code' and w.get('language', 'python') == 'python', f'{lab}: Python code item')
    ex, ts = w['examples'], w['tests']
    ok(len(ex) == 2, f'{lab}: two examples')
    ok(6 <= len(ts) <= 10, f'{lab}: {len(ts)} hidden tests, six to ten')
    cmp = {c.get('compare', 'equal') for c in ex + ts}
    what = 'fraction exactly' if cmp == {'fraction'} else 'value'
    exp_how = [f'Submit runs {len(ts)} hidden tests. Each result must equal the expected {what}.']
    if what == 'value':
        exp_how.append(f'Submit runs {len(ts)} hidden tests. Each result must equal the expected whole number.')
    ok(w['how'] in exp_how, f'{lab}: how line names the real test count ({w["how"]})')
    if 'whole number' in w['how']:
        vals = [eval(c['expect'], {'Fraction': Fraction}) for c in ts + ex]
        ok(all(isinstance(v, int) and not isinstance(v, bool) for v in vals), f'{lab}: "whole number" how only for whole-number results')
    ok(240 <= it['pace'] <= 480, f'{lab}: pace {it["pace"]} in 240 to 480')
    fn = fname_of(w['solution'])
    ok(fn and fname_of(w['starter']) == fn, f'{lab}: starter and solution define {fn}')
    ok(it['question'] == f'Complete `{fn}`.', f'{lab}: question line')
    ok(f'`{fn}(' in it['prose'], f'{lab}: prose shows the signature and a worked call')
    ok(w['starter'].rstrip().endswith('...'), f'{lab}: starter is the signature with ...')
    ok(fname_of(brute) == fn, f'{lab}: brute force defines {fn}')
    # route A: the model solution passes every example and test
    ra = run(w['solution'], ex + ts)
    for (p, a), c in zip(ra, ex + ts):
        ok(p, f'{lab}: model passes {c["call"]} (got {str(a)[:60]})')
    # route B: the brute force passes every example and test, and agrees with the model value by value
    rb = run(brute, ex + ts)
    for (p, b), (_, a), c in zip(rb, ra, ex + ts):
        ok(p and _same(a, b), f'{lab}: brute force agrees on {c["call"]}')
    # the untouched starter fails
    rs = run(w['starter'], ts)
    ok(not all(p for p, _ in rs), f'{lab}: starter fails the hidden tests')
    # each named near-miss fails at least one hidden test
    for name, src in traps.items():
        rt = run(src, ts)
        failed = [k + 1 for k, (p, _) in enumerate(rt) if not p]
        how = '; '.join(f'test {k}: {str(rt[k - 1][1])[:40]}' for k in failed[:3])
        print(f'  near-miss {lab} [{name}] fails tests {failed} ({how})')
        ok(failed, f'{lab}: near-miss {name} fails at least one hidden test')
    return ra


def snippet(prose, lang='python'):
    blocks = re.findall(r'```' + lang + r'\n(.*?)```', prose, re.S)
    return blocks


def run_snippet(prose):
    """Executes the item's own fenced Python lines and returns the namespace (the last block)."""
    ns = {}
    for b in snippet(prose):
        ok_lines = len(b.strip().splitlines())
        assert ok_lines <= 8, f'snippet of {ok_lines} lines'
        exec(b, ns)
    return ns


def eval_line(prose):
    b = snippet(prose)[-1].strip()
    return eval(b, {})


def cpp(src):
    """Compiles and runs a C++20 program; returns its stdout, or None (with a warning) when there is no compiler."""
    cxx = shutil.which('g++') or shutil.which('clang++')
    if not cxx:
        print('WARNING: no C++ compiler; C++ facts skipped (not a pass)')
        return None
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, 'a.cpp')
        open(p, 'w').write(src)
        exe = os.path.join(d, 'a.out')
        subprocess.run([cxx, '-std=c++20', '-Wall', '-o', exe, p], check=True)
        return subprocess.run([exe], capture_output=True, text=True, check=True).stdout
