"""Print the three voice-scan hits (lesson id in a code span) with the lesson titles,
and the two parts of measure-prob/problems-2 item 3 that overflow at 440 px.

Usage (from the repo root): python docs/reviews/review-pass9-hits-scripts/voice_mobile.py
"""
import json, os, re, glob

ROOT = os.path.join(os.path.dirname(__file__), '..', '..', '..')
C = os.path.join(ROOT, 'app/content/courses')


def load(p):
    return json.load(open(os.path.join(C, p), encoding='utf-8'))


for f, i, field in (('coding-int/homework-2.json', 3, 'widget.prompt'), ('coding-int/homework-2.json', 6, 'prose'), ('coding-int/review-2.json', 6, 'prose')):
    it = load(f)['items'][i]
    v = it
    for k in field.split('.'):
        v = v[k]
    print(f, i, field)
    for s in re.split(r'(?<=[.?:])\s+', v):
        if re.search(r'`l\d+', s):
            print('   ', s)
for p in sorted(glob.glob(os.path.join(C, 'coding-int', 'l*.json'))):
    d = json.load(open(p, encoding='utf-8'))
    if re.match(r'l(8|10)-', os.path.basename(p)):
        print(os.path.basename(p), '|', d.get('title'))

it = load('measure-prob/problems-2.json')['items'][2]
print(it['id'], '|', it.get('prose'))
for j in (3, 4):
    p = it['parts'][j]
    print('part', j + 1, json.dumps({k: p[k] for k in p if k != 'widget'}, ensure_ascii=False, indent=1))
    print(' widget kind', p['widget'].get('kind'), [k for k in p['widget']])
