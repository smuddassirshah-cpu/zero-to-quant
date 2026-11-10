import json, sys, time, signal, importlib.util, subprocess
import os; S = os.path.dirname(os.path.abspath(__file__)) + '/'
spec = importlib.util.spec_from_file_location('mine', S + 'mine.py'); mine = importlib.util.module_from_spec(spec); spec.loader.exec_module(mine)
ids = sys.argv[1:]
class Slow(Exception): pass
def alarm(*_): raise Slow()
signal.signal(signal.SIGALRM, alarm)
def old(i):
    r = subprocess.run(['git', 'show', 'f379218:app/content/drills/%s.json' % i], capture_output=True, text=True)
    return json.loads(r.stdout)
def run(fnname, fn, cases, limit):
    """returns list of (idx, verdict) for failing cases; SLOW stops the run"""
    fails = []
    for i, t in enumerate(cases):
        signal.setitimer(signal.ITIMER_REAL, limit)
        try:
            got = eval(t['call'], {fnname: fn})
            signal.setitimer(signal.ITIMER_REAL, 0)
        except Slow:
            fails.append((i, 'SLOW')); continue
        except Exception as e:
            signal.setitimer(signal.ITIMER_REAL, 0)
            fails.append((i, 'raised ' + type(e).__name__)); continue
        want = eval(t['expect'])
        if got != want or type(got) is not type(want):
            fails.append((i, 'got %s want %s' % (repr(got)[:50], repr(want)[:50])))
    return fails
for i in ids:
    d = json.load(open('app/content/drills/%s.json' % i)); o = old(i)
    fn = d['fn']; ne = len(d['examples']); cases = d['examples'] + d['tests']
    oldcalls = {(t['call'], t['expect']) for t in o['examples'] + o['tests']}
    newidx = [k for k, t in enumerate(cases) if (t['call'], t['expect']) not in oldcalls]
    lab = lambda k: ('ex%d' % k) if k < ne else ('t%d' % (k - ne))
    print('==', i, 'cases', len(cases), 'new/changed:', [lab(k) for k in newidx])
    ns = {}; exec(d['solution'], ns)
    t0 = time.time(); f = run(fn, ns[fn], cases, 20); print('   model', 'PASS' if not f else f, '%.2fs' % (time.time() - t0))
    if hasattr(mine, fn):
        t0 = time.time(); f = run(fn, getattr(mine, fn), cases, 30); print('   mine ', 'PASS' if not f else [(lab(k), v) for k, v in f], '%.2fs' % (time.time() - t0))
    else: print('   mine  (none)')
    ns = {}; exec(d['starter'], ns)
    f = run(fn, ns[fn], cases, 5); print('   starter fails', len(f), 'of', len(cases))
    oldpl = {p['code'] for p in o.get('planted', [])}
    for k, p in enumerate(d.get('planted', [])):
        ns = {}; exec(p['code'], ns)
        t0 = time.time(); f = run(fn, ns[fn], cases, 6)
        print('   planted%d%s' % (k, ' NEW' if p['code'] not in oldpl else ''), [(lab(a), b[:60]) for a, b in f][:4], 'nfail', len(f), '%.1fs' % (time.time() - t0), '|', p['slip'][:90])
