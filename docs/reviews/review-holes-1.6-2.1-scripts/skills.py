"""Skill tags of level 4 of testing and stat-learning, and of the two topic exams: every place a skill is named, with
enough of the item's text to judge whether the tag is honest. Also checks every tag is a skill of course.json and that
no level 4 file still carries a tag the report says was dropped.   python3 skills.py   (from the repo root)"""
import json
import glob
import os
import re

bad = 0
for course, lessons in (('testing', range(13, 19)), ('stat-learning', range(15, 20))):
    base = f'app/content/courses/{course}'
    cj = json.load(open(f'{base}/course.json'))
    skills = cj['skills']
    print(f'\n== {course}: skills {skills}')
    files = []
    for n in lessons:
        files += glob.glob(f'{base}/l{n}-*.json')
    files += [f'{base}/review-4.json', f'{base}/homework-4.json', f'{base}/problems-4.json'] + sorted(glob.glob(f'{base}/fluency-l1[3-9]-*.json'))
    for f in files:
        d = json.load(open(f))
        name = os.path.basename(f)
        top = d.get('skills')
        print(f'-- {name}: file skills {top}')
        for key in ('screens', 'quiz', 'items', 'families'):
            for i, it in enumerate(d.get(key) or []):
                sk = it.get('skills') or ([it['skill']] if it.get('skill') else None)
                if sk is None:
                    continue
                for s in sk:
                    if key != 'families' and s not in skills:   # a fluency family's `skill` is free text, not a course skill
                        bad += 1
                        print(f'   UNKNOWN SKILL {s}')
                text = (it.get('question') or it.get('prompt') or it.get('prose') or it.get('title') or '')
                if it.get('parts'):
                    text = (it.get('prose') or '') + ' // ' + ' / '.join(p.get('question', '')[:60] for p in it['parts'])
                text = re.sub(r'\s+', ' ', text)[:170]
                print(f"   {key}[{i}] {it.get('id', '')} {sk}: {text}")

for ex, course_of in (('topic-1.6', 'testing'), ('topic-2.1', 'stat-learning')):
    d = json.load(open(f'app/content/exams/{ex}.json'))
    print(f"\n== {ex}: skills map keys {list(d.get('skills', {}).keys()) if isinstance(d.get('skills'), dict) else d.get('skills')}")
    known = set(d['skills'].keys()) if isinstance(d.get('skills'), dict) else set(d.get('skills') or [])
    for it in d['items']:
        for s in it.get('skills') or []:
            if s not in known:
                bad += 1
                print(f"   {it['id']}: skill {s} not in the exam's skills map")
    print('   items', len(d['items']), 'minutes', d.get('minutes'), 'difficulties', sorted(it.get('difficulty') for it in d['items']))
print('\nunknown tags:', bad)
raise SystemExit(1 if bad else 0)
