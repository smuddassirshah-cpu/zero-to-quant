"""Questions only (no answers), so each part is solved before its key is read.

Usage: python questions.py app/content/courses/<course>/problems-<n>.json
"""
import json
import sys

d = json.load(open(sys.argv[1]))
for it in d['items']:
    print(f"\n#### {it['id']} d{it['difficulty']} {it['skills']}")
    print('PROSE:', it['prose'])
    for i, p in enumerate(it['parts'], 1):
        w = p['widget']
        print(f" [{i}] ({w['kind']}) {p['question']}")
        if w['kind'] == 'choice':
            for o in w.get('options', []):
                print('    opt:', o.get('label', o.get('text', o)) if isinstance(o, dict) else o)
