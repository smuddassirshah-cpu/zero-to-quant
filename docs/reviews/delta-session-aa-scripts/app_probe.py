"""Delta read, session AA: my C++ solutions and probes in the app's own runtime (clang 21 to wasm32), on a copy of app/.

  python docs/reviews/delta-session-aa-scripts/app_probe.py <copy-dir> <pkgs> mine|probes|newonly

Nothing under the repo's own app/ is changed. In the copy:
  mine     each of the 17 drills gets `solution` := my solution (mine_cpp.py); planted-check then passes only if my
           solution passes every hidden test in the app (its planted list is left as committed).
  probes   each probed drill gets `planted` := its probes from mine_cpp.PROBES plus one committed planted solution.
           planted-check prints FAIL for a probe that passes every hidden test in the app.
  newonly  for each planted solution the fix pass added, the tests the fix pass added are removed and `planted` is
           cut to the new ones: planted-check must then FAIL for each, which shows that the new tests, and only
           they, catch it in the app.
One browser job; run it in the foreground and read the tail.
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
BEFORE = 'd71960f^'


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


M = load(os.path.join(HERE, 'mine_cpp.py'), 'mine_cpp')
copy, pkgs, mode = sys.argv[1], sys.argv[2], sys.argv[3]
if os.path.exists(copy):
    shutil.rmtree(copy)
shutil.copytree(os.path.join(ROOT, 'app'), copy, ignore=shutil.ignore_patterns('node_modules'))


def read(i):
    return json.load(open(os.path.join(ROOT, 'app/content/drills', i + '.json')))


def old(i):
    r = subprocess.run(['git', 'show', f'{BEFORE}:app/content/drills/{i}.json'], capture_output=True, text=True, cwd=ROOT)
    return json.loads(r.stdout)


def write(d):
    json.dump(d, open(os.path.join(copy, 'content/drills', d['id'] + '.json'), 'w'), indent=1)


ids = []
if mode == 'mine':
    for i, code in M.SOLUTIONS.items():
        d = read(i)
        d['solution'] = code
        write(d)
        ids.append(i)
elif mode == 'probes':
    for (i, name, _), code in M.PROBES.items():
        d = read(i) if i not in ids else json.load(open(os.path.join(copy, 'content/drills', i + '.json')))
        if i not in ids:
            d['planted'] = d['planted'][:1]
            ids.append(i)
        d['planted'].append({'code': code, 'slip': 'PROBE ' + name})
        write(d)
        print('probe', i, '|', name)
elif mode == 'newonly':
    import glob
    key = lambda t: json.dumps({k: t.get(k) for k in ('call', 'args', 'expect', 'compiles')}, sort_keys=True)
    for f in sorted(glob.glob(os.path.join(ROOT, 'app/content/drills/cpp-*.json'))):
        d = json.load(open(f))
        o = old(d['id'])
        oldcode = {p['code'] for p in o.get('planted', [])}
        newp = [p for p in d.get('planted', []) if p['code'] not in oldcode]
        if not newp:
            continue
        oldkeys = {key(t) for t in o['tests']}
        d['tests'] = [t for t in d['tests'] if key(t) in oldkeys]
        d['planted'] = newp
        write(d)
        ids.append(d['id'])
        print('newonly', d['id'], 'tests kept', len(d['tests']), 'new planted', len(newp))
cmd = ['node', os.path.join(ROOT, 'app/tools/planted-check.mjs')]
for i in ids:
    cmd += ['--drill', i]
cmd += ['--local-cdn', pkgs]
r = subprocess.run(cmd, cwd=os.path.join(ROOT, 'app'), env=dict(os.environ, ZQ_APP_DIR=copy), capture_output=True, text=True)
print((r.stdout + r.stderr)[-4000:])
print('exit', r.returncode)
