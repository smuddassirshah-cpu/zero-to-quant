"""Build app/content/exams/topic-3.5.json from build_a/b/c.

Run from anywhere: python3 build.py
Order in the file: difficulty 2, then 3, then 4, then 5, courses interleaved (r = research-int, c = coding-int, s = systems).
"""
import json, os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_a import ITEMS_A
from build_b import ITEMS_B
from build_c import ITEMS_C
import refs

ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OUT = os.path.join(ROOT, 'app', 'content', 'exams', 'topic-3.5.json')

ALL = {}
ALL.update(ITEMS_A); ALL.update(ITEMS_B); ALL.update(ITEMS_C)
assert sorted(ALL) == list(range(1, 31)), sorted(ALL)

# the expected total of the large ActiveSymbols test comes from the independent Fenwick reference
it21 = ALL[21]
big = refs.active_total_bit()
for t in it21['widget']['tests']:
    if t['call'] == 'total':
        t['expect'] = str(big)

ORDER = [1, 12, 22, 3, 16, 26,                       # difficulty 2
         2, 13, 23, 4, 15, 24, 5, 17, 25, 6, 18, 27, 8, 14, 19,   # difficulty 3
         7, 20, 28, 9, 21, 10,                        # difficulty 4
         11, 29, 30]                                  # difficulty 5
assert sorted(ORDER) == list(range(1, 31))
items = [ALL[k] for k in ORDER]
diffs = [i['difficulty'] for i in items]
assert diffs == sorted(diffs), diffs
assert [diffs.count(d) for d in (2, 3, 4, 5)] == [6, 15, 6, 3]

SKILLS = {
    "rq-stats": "Statistics questions",
    "rq-linalg": "Linear algebra questions",
    "rq-ml": "Machine learning questions",
    "rq-case": "The open case",
    "rq-data": "Data tasks",
    "ci-patterns": "Further patterns",
    "ci-strings": "Strings and simulation",
    "ci-design": "Design in code",
    "ci-timed": "Solving under time",
    "sy-memory": "Memory and the machine",
    "sy-concurrency": "Concurrency",
    "sy-os": "Operating systems and networks",
    "sy-latency": "Low-latency design",
}
exam = {"id": "topic-3.5", "topic": "3.5", "name": "Interviews by role", "minutes": 90, "pass": 0.7,
        "skills": SKILLS, "items": items}

# reports
used = {}
for it in items:
    for s in it['skills']:
        used[s] = used.get(s, 0) + 1
assert set(used) == set(SKILLS), set(SKILLS) - set(used)
pace = sum(i['pace'] for i in items)
print('items', len(items), 'pace', pace, 's =', pace / 60, 'min')
print('skills', dict(sorted(used.items())))


def words(t):
    return len(re.sub(r'[`$]', '', t).split())


# key length against distractors in choice and multi
def widgets(it):
    if 'widget' in it:
        yield it['id'], it['widget']
    for k, p in enumerate(it.get('parts', [])):
        yield "%s-p%d" % (it['id'], k + 1), p['widget']


for iid, w in [x for it in items for x in widgets(it)]:
    if w['kind'] in ('choice', 'multi'):
        keys = [len(o['text']) for o in w['options'] if o.get('correct')]
        dist = [len(o['text']) for o in w['options'] if not o.get('correct')]
        ratio = max(keys) / max(dist)
        flag = ' <-- LONG' if ratio > 1.08 else ''
        print('%-24s key/longest distractor %.2f%s' % (iid, ratio, flag))

with open(OUT, 'w') as f:
    json.dump(exam, f, ensure_ascii=False, indent=2)
    f.write('\n')
print('wrote', OUT)

import second_read_patch
second_read_patch.apply(OUT)
print('patched', OUT)
