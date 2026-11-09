# Run a module of candidate functions against every example and hidden test of the dsa drills.
# Usage: harness.py <module.py> <drills dir> [ids...]; prints failures and slow cases.
# The module may define functions under the drill's `fn` name; drills whose fn is absent are skipped.
import json, sys, time, glob, os, signal

mod, ddir = sys.argv[1], sys.argv[2]
ids = sys.argv[3:]
src = open(mod).read()
QUIET = os.environ.get('QUIET') == '1'


class TO(Exception):
    pass


def alarm(*a):
    raise TO()


signal.signal(signal.SIGALRM, alarm)


def run(fn_ns, d, limit=int(os.environ.get("LIMIT", "10"))):
    res = []
    for kind in ('examples', 'tests'):
        for i, t in enumerate(d[kind]):
            ns = dict(fn_ns)
            signal.alarm(limit)
            t0 = time.time()
            try:
                got = eval(t['call'], ns)
                ok = got == eval(t['expect'], {})
                err = None
            except TO:
                ok, got, err = False, None, 'TIMEOUT'
            except Exception as e:
                ok, got, err = False, None, repr(e)[:100]
            finally:
                signal.alarm(0)
            dt = time.time() - t0
            res.append((kind, i, ok, dt, err, got))
    return res


files = sorted(glob.glob(os.path.join(ddir, 'dsa-*.json')))
total_fail = 0
for f in files:
    d = json.load(open(f))
    if ids and d['id'] not in ids:
        continue
    ns = {}
    exec(src, ns)
    if d['fn'] not in ns:
        continue
    r = run(ns, d)
    fails = [x for x in r if not x[2]]
    slow = max(x[3] for x in r)
    total_fail += len(fails)
    print(f"{d['id']}: {len(r)-len(fails)}/{len(r)} pass, slowest {slow:.2f}s")
    if QUIET:
        continue
    for k, i, ok, dt, err, got in fails:
        c = d[k][i]['call']
        print(f"   FAIL {k}[{i}] {c[:90]} expect={d[k][i]['expect'][:60]} got={str(got)[:60]} {err or ''}")
print('total failures', total_fail)
