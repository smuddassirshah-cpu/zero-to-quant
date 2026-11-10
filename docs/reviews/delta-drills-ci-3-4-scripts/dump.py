"""Print a changed drill as it now stands, marking what the fix pass changed.
Run from the repo root: python dump.py <drill id> ...  (old side: commit 6038127)"""
import json, sys, subprocess
OLD = '6038127'
for i in sys.argv[1:]:
    d = json.load(open('app/content/drills/%s.json' % i))
    o = json.loads(subprocess.run(['git', 'show', '%s:app/content/drills/%s.json' % (OLD, i)], capture_output=True, text=True).stdout)
    print('=' * 30, i, '|', d['name'], '| diff', d['difficulty'], 'pace', d['pace'], 'fn', d.get('fn'), '| returns', d.get('returns'))
    for k in d:
        if k in ('id', 'name', 'course', 'pack', 'difficulty', 'pace', 'fn', 'returns', 'skills', 'starter'):
            if d[k] != o.get(k): print('  CHANGED', k, o.get(k), '->', d[k])
            continue
        ch = '' if d[k] == o.get(k) else ' [CHANGED]'
        v = d[k]
        if k in ('examples', 'tests'):
            print('##', k, ch)
            oc = {(t['call'], t['expect']) for t in o[k]}
            for n, t in enumerate(v):
                print('  %d%s' % (n, '' if (t['call'], t['expect']) in oc else '*'), t['call'][:330], '=>', t['expect'][:120], ('| ' + t['note']) if 'note' in t else '', '' if t.get('compare') == 'equal' else t.get('compare'))
        elif k == 'planted':
            print('##', k, ch)
            oc = {p['code'] for p in o.get(k, [])}
            for n, p in enumerate(v):
                print('  --%d%s slip: %s' % (n, '' if p['code'] in oc else ' NEW', p['slip']))
                if p['code'] not in oc: print(p['code'])
        elif isinstance(v, str):
            print('##', k, ch); print(v)
        else:
            print('##', k, ch); print(json.dumps(v, ensure_ascii=False, indent=0))
