"""Print a problem set compactly for reading: dump.py <file> [item ids...]"""
import json
import sys

d = json.load(open(sys.argv[1]))
ids = set(sys.argv[2:])
for it in d['items']:
    if ids and it['id'] not in ids:
        continue
    print('=' * 60)
    print(it['id'], '| diff', it.get('difficulty'), '| skills', it.get('skills'), '|', it.get('title', ''))
    for k, v in it.items():
        if k not in ('id', 'difficulty', 'skills', 'title', 'parts', 'prose'):
            print(' ', k, ':', json.dumps(v, ensure_ascii=False)[:400])
    print('PROSE:', it.get('prose'))
    for i, p in enumerate(it['parts'], 1):
        w = p['widget']
        print(f'--- part {i} [{w["kind"]}]', p.get('question') or p.get('prose'))
        for k, v in p.items():
            if k not in ('question', 'prose', 'widget', 'feedback', 'explain'):
                print('    ', k, ':', json.dumps(v, ensure_ascii=False)[:300])
        if w['kind'] == 'choice':
            for o in w['options']:
                print('    opt', '*' if o.get('correct') else ' ', o.get('id'), '|', o.get('text'), '| why:', o.get('why'))
            for k, v in w.items():
                if k not in ('kind', 'options'):
                    print('    ', k, ':', json.dumps(v, ensure_ascii=False))
        else:
            print('    W:', json.dumps({k: v for k, v in w.items() if k not in ('kind', 'wrong')}, ensure_ascii=False))
            for x in w.get('wrong', []):
                print('    wrong:', json.dumps(x, ensure_ascii=False))
        fb = p.get('feedback', {})
        for k, v in fb.items():
            if k == 'byKey':
                for kk, vv in v.items():
                    print('    fb.' + kk + ':', vv)
            else:
                print('    fb.' + k + ':', v)
        print('    EXPLAIN:', p.get('explain'))
