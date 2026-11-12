#!/usr/bin/env python3
"""Compact one-screen print of bank items (every field a learner or the grader sees). Usage: brief.py <id> ..."""
import json, glob, sys
items = {}
for f in sorted(glob.glob('app/content/bank/*.json')):
    for it in json.load(open(f)).get('items', []):
        items[it['id']] = (f.split('/')[-1][:-5], it)
for i in sys.argv[1:]:
    f, it = items[i]; w = it['widget']
    print(f"===== {f} {i} d{it['difficulty']} pace{it['pace']} req{it.get('requires')} skills{it.get('skills')}")
    if it.get('prose'): print('PROSE:', it['prose'])
    print('Q:', it['question'])
    k = w['kind']
    if k == 'numeric':
        print(f"KEY {w['answer']} tol{w['tol']} unit={w.get('unit')!r} accept={w.get('accept')!r}")
        for x in w.get('wrong', []): print(f"  WRONG {x['id']} {x['value']} tol{x['tol']} :: {it['feedback'].get('byKey', {}).get(x['id'])}")
    elif k == 'choice':
        for o in w['options']: print('  ', '*' if o.get('correct') else '-', o['text'], '::', o.get('why', ''))
    elif k == 'code':
        print('STARTER:', repr(w['starter'])); print('HOW:', w.get('how'))
        if w.get('setup'): print('SETUP:', w['setup'])
        for t in w.get('examples', []): print('  EX', json.dumps(t, ensure_ascii=False)[:400])
        for t in w.get('tests', []): print('  T ', json.dumps(t, ensure_ascii=False)[:400])
        print('SOLUTION:\n' + w['solution'])
    else: print(json.dumps(w, ensure_ascii=False)[:1500])
    fb = it['feedback']; print('FB correct:', fb.get('correct'), '| generic:', fb.get('generic'))
    print('EXPLAIN:', it.get('explain', {}).get('text'))
