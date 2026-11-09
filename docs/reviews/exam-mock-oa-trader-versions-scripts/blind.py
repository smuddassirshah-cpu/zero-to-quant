"""Print every item of a mock exam without keys, feedback or explanations.

Usage: python blind.py app/content/exams/mock-oa-trader-2.json
Choice options are sorted by text and order lines by id, so no key leaks.
"""
import json
import sys

d = json.load(open(sys.argv[1]))
for pi, p in enumerate(d['parts']):
    print('== PART', pi, p['id'], p.get('minutes'))
    for ii, it in enumerate(p['items']):
        w = it['widget']
        print(f"[{pi}.{ii}] {it['id']} d{it['difficulty']} pace{it['pace']}: {it['question']}")
        if w['kind'] == 'choice':
            for o in sorted(w['options'], key=lambda o: o['text']):
                print('    -', o['text'])
        elif w['kind'] == 'order':
            for line in sorted(w['lines'], key=lambda x: x['id']):
                print('    *', line['id'], ':', line['text'])
        else:
            print('   ', w['kind'])
