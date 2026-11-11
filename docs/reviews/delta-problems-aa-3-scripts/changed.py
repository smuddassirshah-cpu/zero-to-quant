"""List every item and part the two fix passes changed (base = parent of the pass's first commit,
tip = its last commit), and check that no file has changed since its fix pass.

Run from the repo root: python docs/reviews/delta-problems-aa-3-scripts/changed.py [--dump]
--dump prints each changed part, old and new, field by field.
"""
import json
import subprocess
import sys

PASSES = {
    '0.3 b': ('8ffebdc^', 'c5142a8'),
    '0.3 c': ('b282993^', 'fffad27'),
}
DUMP = '--dump' in sys.argv


def at(rev, path):
    return json.loads(subprocess.check_output(['git', 'show', f'{rev}:{path}']))


def flat(o, pre=''):
    out = {}
    if isinstance(o, dict):
        for k, v in o.items():
            out.update(flat(v, f'{pre}.{k}'))
    elif isinstance(o, list):
        for k, v in enumerate(o):
            key = v.get('id', k) if isinstance(v, dict) else k
            out.update(flat(v, f'{pre}[{key}]'))
    else:
        out[pre] = o
    return out


total = [0, 0]
for name, (base, tip) in PASSES.items():
    files = subprocess.check_output(['git', 'diff', '--name-only', base, tip, '--', 'app/content/courses']).decode().split()
    files = [f for f in files if '/problems-' in f]
    print(f'== fix pass {name}: {len(files)} files')
    for p in files:
        old, new = at(base, p), at(tip, p)
        cur = json.load(open(p))
        assert cur == new, f'{p} changed since its fix pass'
        assert [i['id'] for i in old['items']] == [i['id'] for i in new['items']], p
        for a, b in zip(old['items'], new['items']):
            if a == b:
                continue
            n = max(len(a['parts']), len(b['parts']))
            ch = [k + 1 for k in range(n) if k >= len(a['parts']) or k >= len(b['parts']) or a['parts'][k] != b['parts'][k]]
            other = [k for k in b if k != 'parts' and a.get(k) != b[k]]
            total[0] += 1
            total[1] += len(ch)
            print(' ', p.split('courses/')[1], b['id'], 'parts', ch, 'of', len(b['parts']), other)
            if DUMP:
                for k in ch:
                    fa, fb = flat(a['parts'][k - 1]), flat(b['parts'][k - 1])
                    for key in sorted(set(fa) | set(fb)):
                        if fa.get(key) != fb.get(key):
                            print(f'      [{k}]{key}\n         - {fa.get(key)!r}\n         + {fb.get(key)!r}')
print(f'{total[0]} items, {total[1]} parts changed; no file changed since its fix pass')
