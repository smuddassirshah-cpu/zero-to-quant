"""Questions only (no answers) of a problems-<n>.json file, for solving each part before reading its key.

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
        print(f" [{i}] ({w['kind']}{' unit ' + w['unit'] if w.get('unit') else ''}) {p['question']}")
        if w['kind'] == 'choice':
            for o in w['options']:
                print('      -', o.get('text', o.get('label')))
