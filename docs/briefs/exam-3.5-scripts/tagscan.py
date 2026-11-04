"""Which other items carry the family tags of topic-3.5 (items in lessons, reviews, homework, exams, bank, drills)?
Prints file, item id and the first 110 characters of its question, so the numbers can be compared by eye."""
import json, glob, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
mine = json.load(open(os.path.join(ROOT, 'app/content/exams/topic-3.5.json')))
TAGS = {t for it in mine['items'] for t in it['tags']}
seen = {}

def walk(o, f):
    if isinstance(o, dict):
        tg = o.get('tags')
        if isinstance(tg, list) and any(t in TAGS for t in tg) and ('question' in o or 'parts' in o or 'brief' in o):
            q = (o.get('question') or o.get('brief') or o.get('prose') or '')[:110].replace('\n', ' ')
            seen.setdefault(f, []).append((o.get('id'), [t for t in tg if t in TAGS], q))
        for v in o.values(): walk(v, f)
    elif isinstance(o, list):
        for v in o: walk(v, f)

for f in sorted(glob.glob(ROOT + '/app/content/**/*.json', recursive=True)):
    if f.endswith('manifest.json') or 'topic-3.5' in f: continue
    try: walk(json.load(open(f)), f.replace(ROOT + '/app/content/', ''))
    except Exception: pass
for f, xs in seen.items():
    for i, t, q in xs: print('%-46s %-26s %-22s %s' % (f, i, ','.join(t), q))
print(len(TAGS), 'tags;', sum(len(v) for v in seen.values()), 'other items carry one')
