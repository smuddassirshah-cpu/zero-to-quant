"""Write the drill files of one pack as they stood before its fix pass into a folder,
so the first reader's candidates can be run against the old tests and the new.
Usage (repo root): python3 old_drills.py <pack> <out dir>"""
import glob
import json
import os
import subprocess
import sys

FIX = {5: 'e2b921a', 6: '399c637', 7: '4160e9d', 8: 'a6b3b02'}
pack, out = int(sys.argv[1]), sys.argv[2]
os.makedirs(out, exist_ok=True)
n = 0
for f in sorted(glob.glob('app/content/drills/ci-*.json')):
    if json.load(open(f))['tags'][0] != f'pack-{pack}':
        continue
    text = subprocess.run(['git', 'show', f'{FIX[pack]}^:{f}'], capture_output=True, text=True, check=True).stdout
    open(os.path.join(out, os.path.basename(f)), 'w').write(text)
    n += 1
print(n, 'files written to', out)
