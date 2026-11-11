"""Print the screens or items of one content file whose text matches a regex, compactly, to judge a freshness hit.
python3 docs/reviews/review-delta-holes-scripts/context.py <file under app/content> '<regex>' [max chars]"""
import json
import re
import sys

doc = json.load(open('app/content/' + sys.argv[1]))
pat = re.compile(sys.argv[2])
cap = int(sys.argv[3]) if len(sys.argv) > 3 else 1200
for key in ('screens', 'quiz', 'items'):
    for i, s in enumerate(doc.get(key, [])):
        t = json.dumps(s, ensure_ascii=False)
        if pat.search(t):
            keep = {k: v for k, v in s.items() if k in ('id', 'prose', 'question', 'widget', 'feedback', 'explain', 'parts', 'title', 'difficulty', 'skills')}
            print(f'--- {sys.argv[1]} {key}[{i}]')
            print(json.dumps(keep, ensure_ascii=False)[:cap])
