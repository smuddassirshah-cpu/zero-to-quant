"""Run the review's candidates in the app's own runtime (clang 21 to WebAssembly), on a copy of app/.

  python app_probe.py <copy-dir> <pkgs> before|after <drill-id> [<drill-id> ...]

Copies app/ to <copy-dir> (once), and in the copy replaces each named drill's `planted` with the
candidates in wrong/ for that drill (names starting `right` or `quadratic`-style notes included: every file).
  before: tests as committed. planted-check should FAIL for each candidate that passes every test.
  after:  the tests of extra_tests.json added (an item's `replaces` index is dropped first, to stay
          within 15). planted-check should pass: the model passes the new tests, each candidate fails one.
Nothing under the repo's own app/ is changed.
"""
import glob, json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))


def main():
    copy, pkgs, mode, ids = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
    if not os.path.exists(os.path.join(copy, 'index.html')):
        shutil.copytree(os.path.join(ROOT, 'app'), copy, ignore=shutil.ignore_patterns('node_modules'))
    extra = json.load(open(os.path.join(HERE, 'extra_tests.json')))
    for did in ids:
        d = json.load(open(os.path.join(ROOT, 'app', 'content', 'drills', did + '.json')))
        planted = []
        for f in sorted(glob.glob(os.path.join(HERE, 'wrong', did + '__*.cpp'))):
            code = open(f).read()
            planted.append({'code': code, 'slip': code.split('\n')[0].lstrip('/ ').strip()})
        d['planted'] = planted
        if mode == 'after':
            items = extra.get(did, [])
            for i in sorted((it['replaces'] for it in items if 'replaces' in it), reverse=True):
                del d['tests'][i]
            for it in items:
                d['tests'].append(it['test'])
                if it.get('postlude'):
                    d['postlude'] = d.get('postlude', '') + '\n' + it['postlude']
        json.dump(d, open(os.path.join(copy, 'content', 'drills', did + '.json'), 'w'), indent=1)
        print(did, 'candidates', len(planted), 'tests', len(d['tests']))
    cmd = ['node', os.path.join(ROOT, 'app', 'tools', 'planted-check.mjs')]
    for did in ids:
        cmd += ['--drill', did]
    cmd += ['--local-cdn', pkgs]
    r = subprocess.run(cmd, cwd=os.path.join(ROOT, 'app'), env=dict(os.environ, ZQ_APP_DIR=copy), capture_output=True, text=True)
    print((r.stdout + r.stderr)[-3000:])
    print('exit', r.returncode)


if __name__ == '__main__':
    main()
