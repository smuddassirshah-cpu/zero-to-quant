"""Second read, proof problems-1 to -3: skim every lesson screen, quiz, review, homework and
exam item of the course (title, start of prose, start of question, key), for level and reuse.
Usage (repo root): python3 docs/reviews/review-problems-proof-1-3-scripts/taught.py <level 1|2|3|exams> [len]"""
import json
import sys

C = 'app/content/courses/proof/'
lv = sys.argv[1]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 200


def flat(x):
    if isinstance(x, list):
        return ' '.join(flat(y) for y in x)
    if isinstance(x, dict):
        return flat(x.get('text', ''))
    return str(x or '')


def key(w):
    if not isinstance(w, dict):
        return ''
    if w.get('kind') == 'choice':
        return 'KEY ' + ' / '.join(flat(o.get('text'))[:90] for o in w.get('options', []) if o.get('correct'))
    a = w.get('answer')
    return f"KEY[{w.get('kind')}] {json.dumps(a, ensure_ascii=False)[:120]}"


def line(tag, s):
    print(f"  {tag} {s.get('type', '')} {s.get('title', s.get('id', ''))!r} | {flat(s.get('prose'))[:n]} | Q: {flat(s.get('question'))[:n]} | {key(s.get('widget'))}")
    for p in s.get('parts') or []:
        print(f"      part: {flat(p.get('question'))[:n]} | {key(p.get('widget'))}")


if lv == 'exams':
    d = json.load(open('app/content/exams/topic-0.6.json'))
    print('#### topic-0.6')
    for k, s in enumerate(d['items']):
        line(f'[{k}]', s)
    d = json.load(open('app/content/exams/stage-0.json'))
    print('#### stage-0 (items with a pv- skill)')
    for p in d['parts']:
        for k, s in enumerate(p.get('items', [])):
            if any(str(x).startswith('pv-') for x in s.get('skills', [])):
                line(f"[{p['id']} {k}]", s)
else:
    course = json.load(open(C + 'course.json'))
    L = [x for x in course['levels'] if x['n'] == int(lv)][0]
    for name in L['lessons']:
        d = json.load(open(C + name + '.json'))
        print(f"#### {name}: {d.get('title')} skills {d.get('skills')}")
        for k, s in enumerate(d['screens']):
            line(f'[{k}]', s)
        q = d.get('quiz')
        for k, s in enumerate(q.get('items', []) if isinstance(q, dict) else q or []):
            line(f'[quiz {k}]', s)
    for name in (L['review'], L['homework']):
        d = json.load(open(C + name + '.json'))
        print(f'#### {name}')
        for k, s in enumerate(d['items']):
            line(f'[{k}]', s)
