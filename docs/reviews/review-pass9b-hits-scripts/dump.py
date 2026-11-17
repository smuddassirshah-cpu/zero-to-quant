"""Print one problem (or selected parts) for the pass 9b triage.

Usage (repo root): python docs/reviews/review-pass9b-hits-scripts/dump.py <course>/<file> <item index> [part index ...] [--all]
Every part prints its question, key and band; named parts (or all with --all) print in full.
"""
import json, sys, os
ROOT = os.path.join(os.path.dirname(__file__), '..', '..', '..')
f, idx = sys.argv[1], int(sys.argv[2])
full = [int(a) for a in sys.argv[3:] if a.isdigit()]
allp = '--all' in sys.argv
d = json.load(open(os.path.join(ROOT, 'app/content/courses', f + ('' if f.endswith('.json') else '.json')), encoding='utf-8'))
it = d['items'][idx]
print('=' * 90)
print(f, idx, it.get('id'))
for k in it:
    if k not in ('parts', 'id', 'difficulty', 'skills'):
        print('STEM.' + k + ':', json.dumps(it[k], ensure_ascii=False)[:1500])
for pi, p in enumerate(it.get('parts', [])):
    w = p.get('widget', {})
    print('-' * 60)
    print(f'[{pi}] Q:', p.get('question') or p.get('prose'))
    wk = {k: v for k, v in w.items() if k != 'wrong'}
    print('   W:', json.dumps(wk, ensure_ascii=False)[:700])
    if pi in full or allp:
        fb = p.get('feedback', {})
        ids = [x.get('id') for x in w.get('wrong', []) or []]
        for x in w.get('wrong', []) or []:
            print('   wrong', json.dumps(x, ensure_ascii=False), '|', fb.get('byKey', {}).get(x.get('id'), ''))
        for k, v in fb.get('byKey', {}).items():
            if k not in ids:
                print('   byKey', k, '|', v)
        print('   correct:', fb.get('correct'))
        print('   generic:', fb.get('generic'))
        print('   hints:', json.dumps(p.get('hints'), ensure_ascii=False))
        print('   explain:', json.dumps(p.get('explain'), ensure_ascii=False))
