"""Print bank items compactly for reading. Usage: show.py <file id> [start] [end]"""
import json, sys, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'app', 'content', 'bank')
f = json.load(open(os.path.join(ROOT, sys.argv[1] + '.json')))
a = int(sys.argv[2]) if len(sys.argv) > 2 else 0
b = int(sys.argv[3]) if len(sys.argv) > 3 else 999
print(f['name'], '|', f.get('description'))
for it in f['items'][a:b]:
    w = it['widget']
    print('\n##', it['id'], 'D%d' % it['difficulty'], 'pace', it.get('pace'), 'tags', it['tags'], 'skills', it.get('skills'), 'role', it['role'], 'req', it.get('requires'))
    if it.get('prose'): print('P:', it['prose'])
    print('Q:', it['question'])
    k = w['kind']
    if k == 'numeric':
        print('KEY', w['answer'], w.get('tol'), '| accept:', w.get('accept'), '| label:', w.get('label'), '| ph:', w.get('placeholder'), {x: w[x] for x in w if x not in ('kind','answer','tol','accept','label','placeholder','wrong')})
        for x in w.get('wrong', []):
            print('  W', x['id'], x['value'], x.get('tol'), '->', it['feedback'].get('byKey', {}).get(x['id']))
    elif k in ('choice', 'multi'):
        for o in w['options']:
            print('  [%s] (%d) %s' % ('X' if o.get('correct') else ' ', len(o['text']), o['text']), '-> ', o.get('why'))
    elif k == 'longform':
        print('PROMPT:', w['prompt'])
        print('MODEL (%d words):' % len(w['model'].split()), w['model'])
        for r in w['rubric']: print('  R', r['points'], r['text'])
    else:
        print(json.dumps(w)[:1500])
    fb = it['feedback']
    print('FB+:', fb.get('correct'), '| GEN:', fb.get('generic'))
    print('EX:', it['explain']['text'])
