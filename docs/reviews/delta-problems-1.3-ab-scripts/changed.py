"""List every item and part the two fix passes changed, and check that no
file has changed since its fix pass.

Run from the repo root: python changed.py
"""
import json
import subprocess

FILES = {
    '460a4a2': ['integrals/problems-1', 'integrals/problems-2', 'integrals/problems-3',
                'limits/problems-2', 'limits/problems-3'],
    'ebbc857': ['multivar/problems-2', 'multivar/problems-3',
                'taylor/problems-1', 'taylor/problems-3'],
}


def at(rev, path):
    return json.loads(subprocess.check_output(['git', 'show', f'{rev}:{path}']))


for c, files in FILES.items():
    for f in files:
        p = f'app/content/courses/{f}.json'
        old, new = at(c + '^', p), at(c, p)
        cur = json.load(open(p))
        assert cur == new, f'{f} changed since its fix pass'
        assert [i['id'] for i in old['items']] == [i['id'] for i in new['items']]
        for a, b in zip(old['items'], new['items']):
            if a != b:
                ch = [k + 1 for k, (x, y) in enumerate(zip(a['parts'], b['parts'])) if x != y]
                other = [k for k in b if k != 'parts' and a.get(k) != b[k]]
                print(f, b['id'], 'parts', ch, 'of', len(b['parts']), other)
print('no file changed since its fix pass')
