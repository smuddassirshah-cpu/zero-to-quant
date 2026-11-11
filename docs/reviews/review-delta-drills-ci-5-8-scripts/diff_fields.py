"""Which fields of which drills each fix pass changed.
Usage (repo root): python3 diff_fields.py [pack ...]"""
import json
import subprocess
import sys

FIX = {5: 'e2b921a', 6: '399c637', 7: '4160e9d', 8: 'a6b3b02'}


def show(rev, path):
    try:
        out = subprocess.run(['git', 'show', f'{rev}:{path}'], capture_output=True, text=True, check=True).stdout
        return json.loads(out)
    except Exception:
        return None


def main():
    packs = [int(a) for a in sys.argv[1:]] or [5, 6, 7, 8]
    for p in packs:
        rev = FIX[p]
        files = subprocess.run(['git', 'diff', '--name-only', rev + '^', rev, '--', 'app/content/drills'],
                               capture_output=True, text=True).stdout.split()
        print(f'== pack {p} ({rev}): {len(files)} files')
        for f in files:
            if f.endswith('index.json'):
                print('  index.json')
                continue
            a, b = show(rev + '^', f), show(rev, f)
            now = json.load(open(f))
            ch = []
            for k in sorted(set(a) | set(b)):
                if a.get(k) != b.get(k):
                    if k in ('tests', 'examples', 'planted', 'constraints', 'notes'):
                        la, lb = a.get(k, []), b.get(k, [])
                        idx = [i for i in range(max(len(la), len(lb)))
                               if i >= len(la) or i >= len(lb) or la[i] != lb[i]]
                        ch.append(f'{k}{idx}({len(la)}->{len(lb)})')
                    else:
                        ch.append(k)
            later = '' if now == b else '  [CHANGED SINCE FIX PASS]'
            print(f'  {f.split("/")[-1][:-5]}: ' + ', '.join(ch) + later)


main()
