"""Run model, mine, starter and every planted solution on every example and hidden test (CPython).
From the repo root: <venv python> docs/reviews/delta-drills-ci-3-4-scripts/run.py [drill ids]   (default: the 22 changed)"""
import json, sys, time, signal, importlib.util, subprocess, os
S = os.path.dirname(os.path.abspath(__file__)) + '/'
OLD = '6038127'
ALL = """ci-board-words ci-busiest-links ci-cell-formula ci-cheapest-pairs ci-clear-rate ci-downward-path-sums
ci-first-misplaced ci-funded-projects ci-live-median ci-log-compactor ci-no-repeat-rota ci-price-ramp ci-ready-blocks
ci-rebuild-from-orders ci-relay-masts ci-right-edge-view ci-ring-lookup ci-stock-by-prefix ci-tick-ranges ci-tray-queue
ci-van-convoys ci-visible-masts""".split()
spec = importlib.util.spec_from_file_location('mine', S + 'mine.py'); mine = importlib.util.module_from_spec(spec); spec.loader.exec_module(mine)
sys.setrecursionlimit(20000)
ids = sys.argv[1:] or ALL
class Slow(Exception): pass
def alarm(*_): raise Slow()
signal.signal(signal.SIGALRM, alarm)
def old(i):
    r = subprocess.run(['git', 'show', '%s:app/content/drills/%s.json' % (OLD, i)], capture_output=True, text=True)
    return json.loads(r.stdout)
def run(fnname, fn, cases, limit):
    fails = []
    for i, t in enumerate(cases):
        signal.setitimer(signal.ITIMER_REAL, limit)
        try:
            got = eval(t['call'], {fnname: fn})
            signal.setitimer(signal.ITIMER_REAL, 0)
        except Slow:
            fails.append((i, 'SLOW over %ds' % limit)); continue
        except BaseException as e:
            signal.setitimer(signal.ITIMER_REAL, 0)
            fails.append((i, 'raised ' + type(e).__name__)); continue
        want = eval(t['expect'])
        if got != want or type(got) is not type(want):
            fails.append((i, 'got %s want %s' % (repr(got)[:50], repr(want)[:50])))
    return fails
bad = 0
for i in ids:
    d = json.load(open('app/content/drills/%s.json' % i)); o = old(i)
    fn = d['fn']; ne = len(d['examples']); cases = d['examples'] + d['tests']
    lab = lambda k: ('ex%d' % k) if k < ne else ('t%d' % (k - ne))
    n_how = d['how'].split('Submit runs ')[1].split()[0]
    print('==', i, '| tests', len(d['tests']), '| how says', n_how, '' if int(n_how) == len(d['tests']) else 'MISMATCH')
    for e in d['examples']:
        if not any(t['call'] == e['call'] and t['expect'] == e['expect'] for t in d['tests']): print('   example not among tests:', e['call'][:60])
    ns = {}; exec(d['solution'], ns)
    t0 = time.time(); f = run(fn, ns[fn], cases, 20); print('   model', 'PASS' if not f else f, '%.2fs' % (time.time() - t0)); bad += bool(f)
    t0 = time.time(); f = run(fn, getattr(mine, fn), cases, 60); print('   mine ', 'PASS' if not f else [(lab(k), v) for k, v in f], '%.2fs' % (time.time() - t0)); bad += bool(f)
    if fn == 'funded_projects':
        small = [t for t in cases if 'range' not in t['call']]
        f = run(fn, mine.funded_projects_brute, small, 20); print('   brute', 'PASS' if not f else f, 'on', len(small), 'small cases'); bad += bool(f)
    ns = {}; exec(d['starter'], ns)
    f = run(fn, ns[fn], d['tests'], 5); print('   starter fails', len(f), 'of', len(d['tests']), 'hidden'); bad += not f
    oldpl = {p['code'] for p in o.get('planted', [])}
    for k, p in enumerate(d.get('planted', [])):
        ns = {}; exec(p['code'], ns)
        t0 = time.time(); f = run(fn, ns[fn], d['tests'], 12)
        print('   planted%d%s' % (k, ' NEW' if p['code'] not in oldpl else ''), 'fails', [(lab(a + ne), b[:44]) for a, b in f][:3], 'n=%d' % len(f), '%.1fs' % (time.time() - t0), '|', p['slip'][:80]); bad += not f
print('problems:', bad)
