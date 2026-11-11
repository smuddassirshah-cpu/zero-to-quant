"""Second read, problems 0.3 c: prints the lesson, review, homework and exam items the freshness findings point at,
so each claim of reuse can be read beside its source. Run from the repo root with python3."""
import json

B = 'app/content/courses/'
REFS = [
    ('series/l5-sigma.json', 'screens', 1), ('series/l5-sigma.json', 'screens', 3), ('series/l5-sigma.json', 'screens', 6),
    ('series/review-2.json', 'items', 1), ('series/review-3.json', 'items', 0), ('series/l9-pascal.json', 'quiz', 3),
    ('series/review-1.json', 'items', 1), ('series/l3-multiplying-each-time.json', 'screens', 3),
    ('trig/homework-1.json', 'items', 4), ('trig/l10-identity-from-circle.json', 'screens', 3),
    ('trig/l13-modelling-a-cycle.json', 'screens', 7), ('trig/l13-modelling-a-cycle.json', 'screens', 8),
    ('trig/homework-2.json', 'items', 6), ('trig/homework-2.json', 'items', 8),
]
for f, key, i in REFS:
    o = json.load(open(B + f))[key][i]
    w = o.get('widget', {})
    print(f"{f} {key}[{i}] id={o.get('id')}\n   {(o.get('prose') or '')[:300]} ## {(o.get('question') or '')[:200]}\n   answer: {w.get('answer', w.get('answers', [x.get('id') for x in w.get('options', []) if x.get('correct')]))}")
for f, ids in (('app/content/exams/topic-0.3.json', ['e-tan-third-quadrant', 'e-sigma-odd']), ('app/content/exams/stage-0.json', ['p-obtuse-cos'])):
    d = json.load(open(f))
    items = d.get('items') or [o for p in d['parts'] for o in p.get('items', [])]
    for o in items:
        if o.get('id') in ids:
            w = o.get('widget', {})
            print(f"{f} id={o['id']}\n   {(o.get('prose') or '')[:300]} ## {(o.get('question') or '')[:200]}\n   answer: {w.get('answer', [x.get('text') for x in w.get('options', []) if x.get('correct')])}")
