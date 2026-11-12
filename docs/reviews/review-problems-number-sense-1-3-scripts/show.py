"""Print a problem set compactly for reading. Run from the repo root:
python3 docs/reviews/review-problems-number-sense-1-3-scripts/show.py 2"""
import json
import sys

n = sys.argv[1]
d = json.load(open(f'app/content/courses/number-sense/problems-{n}.json'))
print({k: v for k, v in d.items() if k != 'items'})
for it in d['items']:
    extra = {k for k in it if k not in ('id', 'difficulty', 'skills', 'prose', 'parts')}
    print('\n###', it['id'], 'diff', it['difficulty'], it['skills'], extra)
    print('PROSE:', it['prose'])
    for i, p in enumerate(it['parts'], 1):
        w = p['widget']
        print(f'\n -- part {i} [{w["kind"]}] Q:', p['question'])
        print('    extra keys:', [k for k in p if k not in ('question', 'widget', 'feedback', 'explain')])
        if w['kind'] == 'choice':
            for o in w['options']:
                print('    opt', o)
        else:
            print('    widget', {k: v for k, v in w.items() if k != 'wrong'})
            for x in w.get('wrong', []):
                print('    wrong', x)
        f = p['feedback']
        print('    correct:', f.get('correct'))
        print('    generic:', f.get('generic'))
        for k, v in f.get('byKey', {}).items():
            print(f'    byKey {k}:', v)
        print('    explain:', p['explain'])
