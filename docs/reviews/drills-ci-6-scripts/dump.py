"""Print parts of the pack 6 drills.
usage: dump.py <drills dir> <part> [id ...]
part: cand (what a candidate sees), tests, model, planted"""
import glob
import json
import os
import sys

d, part = sys.argv[1], sys.argv[2]
ids = sys.argv[3:]
for f in sorted(glob.glob(os.path.join(d, 'ci-*.json'))):
    j = json.load(open(f))
    if (j.get('tags') or [''])[0] != 'pack-6':
        continue
    if ids and j['id'] not in ids:
        continue
    print('=' * 20, j['id'], '| d', j['difficulty'], '| pace', j.get('pace'), '| tags', j['tags'], '| pattern', j.get('pattern'))
    if part == 'cand':
        print('NAME', j['name'])
        print('FN', j.get('fn'), '->', j.get('returns'))
        print('BRIEF', j['brief'])
        for c in j['constraints']:
            print('C:', c if isinstance(c, str) else json.dumps(c))
        print('HINT', j.get('hint'))
        print('STARTER', j['starter'])
        for e in j['examples']:
            print('EX', e)
    if part == 'tests':
        for i, t in enumerate(j['tests']):
            print(i, t['call'][:700], '=>', str(t['expect'])[:300], t.get('compare', ''))
    if part == 'model':
        print(j['solution'])
        print('HOW', j['how'])
        for n in j['notes']:
            print('NOTE', n)
    if part == 'planted':
        for p in j['planted']:
            print('SLIP', p['slip'])
            print(p['code'])
            print('-' * 8)
