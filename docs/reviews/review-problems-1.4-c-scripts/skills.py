"""Second read, eigen problems-1 to -3: every `skills` id of a problem is carried by a lesson of its level.
Run from the repo root:  python3 docs/reviews/review-problems-1.4-c-scripts/skills.py"""
import json
import sys

course = json.load(open('app/content/courses/eigen/course.json'))
bad = 0
for lv in course['levels'][:3]:
    have = {}
    for l in lv['lessons']:
        d = json.load(open(f'app/content/courses/eigen/{l}.json'))
        ids = set(d.get('skills') or [])
        for s in d.get('screens', []):
            ids |= set(s.get('skills') or [])
        for i in ids:
            have.setdefault(i, []).append(l.split('-')[0])
    print(f'level {lv["n"]}: lessons carry {dict(sorted(have.items()))}')
    for it in json.load(open(f'app/content/courses/eigen/problems-{lv["n"]}.json'))['items']:
        miss = [s for s in it['skills'] if s not in have]
        print(f'   {it["id"]}: {it["skills"]}{"  NOT IN THE LEVEL: " + str(miss) if miss else ""}')
        bad += len(miss)
sys.exit(1 if bad else 0)
