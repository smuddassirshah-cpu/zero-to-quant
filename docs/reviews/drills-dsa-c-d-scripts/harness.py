"""Second-read harness for dsa drills.

Usage:
  harness.py mine <module.py> <drills_dir> [ids...]   run my solutions (one module) on every example and test
  harness.py model <drills_dir> [ids...]              run the model solution (timings)
  harness.py wrong <wrong.py> <drills_dir> [ids...]   run each planted wrong solution; report tests failed
A wrong module defines WRONG = {drill_id: [(label, source), ...]}.
Each test gets its own CASE_LIMIT (default 2 s) alarm here, natively; Pyodide runs about 2x slower and the browser gives the whole run 5 s; a timeout counts as caught.
"""
import json, math, os, signal, sys, time, glob, resource
resource.setrlimit(resource.RLIMIT_AS, (3 * 2**30, 3 * 2**30))
LIMIT = float(os.environ.get('CASE_LIMIT', '2.0'))

class TO(Exception):
    pass

def _alarm(*a):
    raise TO()

signal.signal(signal.SIGALRM, _alarm)

def cases(d):
    return [('ex', e) for e in d['examples']] + [('t', t) for t in d['tests']]

def run_case(ns, c, limit=None):
    limit = limit or LIMIT
    g = dict(ns)
    t0 = time.perf_counter()
    err = None
    try:
        try:
            signal.setitimer(signal.ITIMER_REAL, limit)
            got = eval(c['call'], g)
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
    except TO:
        return 'TIMEOUT', None, time.perf_counter() - t0
    except MemoryError:
        return 'MEMORY', None, time.perf_counter() - t0
    except Exception as e:
        return 'EXC ' + type(e).__name__ + ': ' + str(e)[:80], None, time.perf_counter() - t0
    dt = time.perf_counter() - t0
    exp = eval(c['expect'], {})
    if c.get('compare') == 'isclose':
        ok = math.isclose(got, exp, rel_tol=c.get('tol', 1e-9), abs_tol=c.get('tol', 1e-9))
    else:
        ok = got == exp and type(got) == type(exp) if not isinstance(exp, (int, float)) or isinstance(exp, bool) else got == exp
    return ('ok' if ok else 'WRONG'), got, dt

def load(dd, i):
    return json.load(open(os.path.join(dd, i + '.json')))

def ns_from(src):
    ns = {}
    exec(src, ns)
    return ns

def ids_of(dd, ids):
    return ids or sorted(os.path.basename(p)[:-5] for p in glob.glob(os.path.join(dd, 'dsa-*.json')))

def main():
    mode = sys.argv[1]
    bad = 0
    if mode == 'mine':
        src = open(sys.argv[2]).read(); dd = sys.argv[3]
        ns = ns_from(src)
        for i in sys.argv[4:]:
            d = load(dd, i)
            res = []
            tot = 0
            for k, c in cases(d):
                st, got, dt = run_case(ns, c)
                tot += dt
                if st != 'ok':
                    bad += 1
                    res.append(f'  {k} {c["call"][:90]!r}: {st} got {str(got)[:80]} exp {c["expect"][:60]}')
            print(f'{i}: {"PASS" if not res else "FAIL"} ({len(cases(d))} cases, {tot:.2f}s)')
            for r in res: print(r)
    elif mode == 'model':
        dd = sys.argv[2]
        for i in ids_of(dd, sys.argv[3:]):
            d = load(dd, i)
            ns = ns_from(d['solution'])
            res = []; tot = 0
            for k, c in cases(d):
                st, got, dt = run_case(ns, c)
                tot += dt
                if st != 'ok':
                    bad += 1; res.append(f'  {k} {c["call"][:90]!r}: {st}')
            sns = ns_from(d['starter'])
            sf = sum(run_case(sns, c)[0] != 'ok' for c in d['tests'])
            print(f'{i}: model {"PASS" if not res else "FAIL"} {tot:.2f}s, starter fails {sf}/{len(d["tests"])}')
            for r in res: print(r)
    elif mode == 'wrong':
        mod = ns_from(open(sys.argv[2]).read()); dd = sys.argv[3]
        W = mod['WRONG']
        for i in (sys.argv[4:] or sorted(W)):
            d = load(dd, i)
            for label, src in W.get(i, []):
                ns = ns_from(src)
                fails = []
                for k, c in cases(d):
                    if k != 't':
                        continue
                    st, got, dt = run_case(ns, c)
                    if st != 'ok':
                        fails.append(st.split()[0])
                    if st in ('TIMEOUT', 'MEMORY'):
                        break  # later tests not run, to keep the script short
                tag = 'caught' if fails else 'PASSES ALL'
                print(f'{i} [{label}]: {tag} ({len(fails)}/{len(d["tests"])} fail: {",".join(sorted(set(fails)))})')
    sys.exit(1 if bad else 0)

main()
