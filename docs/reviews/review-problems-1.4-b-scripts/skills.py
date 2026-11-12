"""Skills of each level's lessons against the skills its problem set carries. Run from the repo root."""
import json
import re

for c in ['elimination', 'least-squares']:
    cj = json.load(open(f'app/content/courses/{c}/course.json'))
    for lv in cj['levels']:
        sk = set()
        for l in lv['lessons']:
            t = json.dumps(json.load(open(f'app/content/courses/{c}/{l}.json')))
            for m in re.findall(r'"skills?": (\[[^\]]*\]|"[^"]*")', t):
                sk |= set(re.findall(r'[a-z]+-[a-z]+', m))
        p = json.load(open(f'app/content/courses/{c}/problems-{lv["n"]}.json'))
        ps = set(s for it in p['items'] for s in it['skills'])
        print(c, lv['n'], 'lesson skills', sorted(sk), '| problem skills', sorted(ps), '| outside', sorted(ps - sk))
