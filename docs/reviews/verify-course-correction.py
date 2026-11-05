"""Recompute the content-side figures in review-course-correction.md at HEAD. Read-only.

Run from the repo root: python3 -I docs/reviews/verify-course-correction.py
Prints one block per finding id. Engine line checks are in the Verification at HEAD section, by hand.
"""
import json, os, re, statistics, sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
C = os.path.join(ROOT, 'app', 'content')
J = lambda *p: json.load(open(os.path.join(C, *p), encoding='utf-8'))
ex = lambda *p: os.path.exists(os.path.join(C, *p))

cur = J('curriculum.json')
topic_stage = {t['id']: s['id'] for s in cur['stages'] for t in s['topics']}
courses = {}
for cid in sorted(os.listdir(os.path.join(C, 'courses'))):
    if ex('courses', cid, 'course.json'):
        courses[cid] = J('courses', cid, 'course.json')
stage_of = {cid: topic_stage.get(cj.get('topic')) for cid, cj in courses.items()}

lessons = {}  # (cid, lid) -> doc
for cid, cj in courses.items():
    for lv in cj.get('levels', []):
        for lid in lv.get('lessons', []):
            if ex('courses', cid, lid + '.json'):
                lessons[(cid, lid)] = J('courses', cid, lid + '.json')

def level_written(cid, lv):
    ls = lv.get('lessons', [])
    return bool(ls) and all((cid, l) in lessons for l in ls)

print('== F04 quiz kinds ==')
kinds = Counter(); code_lessons = 0
for (cid, lid), d in lessons.items():
    for q in d.get('quiz', []):
        kinds[(q.get('widget') or {}).get('kind', 'none')] += 1
    if any((s.get('widget') or {}).get('kind') == 'code' for s in d.get('screens', [])):
        code_lessons += 1
print('lessons', len(lessons), 'quiz items', sum(kinds.values()), dict(kinds.most_common()))
print('lessons with a code screen', code_lessons)
verbs = Counter()
for d in lessons.values():
    for o in d.get('objectives', []):
        w = re.match(r"[A-Za-z]+", o.strip())
        if w: verbs[w.group(0).lower()] += 1
print('objective first words:', {v: verbs[v] for v in ['write', 'derive', 'prove', 'build', 'explain', 'code', 'implement', 'design', 'defend', 'justify']})

print('== F07 minutes ==')
mins = [d.get('minutes') for d in lessons.values()]
print('min', min(mins), 'max', max(mins), 'median', statistics.median(mins))
dur = []
for (cid, lid), d in lessons.items():
    txt = ' '.join(str(s.get('prose', '')) for s in d.get('screens', [])[:2])
    m = re.search(r"(?:about|takes|for|in|spend|budget of|allow)\s+(\d{2,3})\s*minutes", txt)
    if m and abs(int(m.group(1)) - d['minutes']) >= 5:
        dur.append((f'{cid}/{lid}', d['minutes'], int(m.group(1))))
print('prose duration differs by 5 or more (first two screens):', len(dur))
for r in sorted(dur): print('  ', r)

print('== N02 reviews ==')
rev_items = Counter(); rev_pass = 0; written_no_review = []
for cid, cj in courses.items():
    for lv in cj.get('levels', []):
        r = lv.get('review')
        if r and ex('courses', cid, r + '.json'):
            rd = J('courses', cid, r + '.json'); rev_items[len(rd.get('items', []))] += 1
            if 'pass' in rd: rev_pass += 1
        elif level_written(cid, lv):
            written_no_review.append(f'{cid}/L{lv["n"]}')
print('review sizes', dict(sorted(rev_items.items())), 'with pass field', rev_pass)
print('fully written levels with no written review:', written_no_review or 'none')

print('== N03 topic exam reach ==')
for t in ['0.3', '1.3', '1.5', '3.3']:
    lv_n = ls_n = 0
    for cid, cj in courses.items():
        if cj.get('topic') == t:
            for lv in cj.get('levels', []):
                w = [l for l in lv.get('lessons', []) if (cid, l) in lessons]
                if w: lv_n += 1; ls_n += len(w)
    e = J('exams', f'topic-{t}.json') if ex('exams', f'topic-{t}.json') else {}
    n = len(e.get('items', [])); p = e.get('pass', 0.7)
    print(f'topic {t}: pass {-(-int(n * p * 1000) // 1000)} of {n} meets {lv_n} levels with written lessons, {ls_n} lessons')

print('== F02/F03 requires and closures ==')
def lv_of(cid, n):
    for lv in courses.get(cid, {}).get('levels', []):
        if lv['n'] == n: return lv
def refs_of_level(cid, lv):
    if 'requires' in lv: return lv['requires']
    return [f'{cid}/L{lv["n"] - 1}'] if lv['n'] > 1 else []
def parse(ref):
    c, x = ref.split('/', 1)
    m = re.fullmatch(r'L(\d+)', x)
    if m: return c, int(m.group(1))
    for lv in courses.get(c, {}).get('levels', []):
        if x in lv.get('lessons', []): return c, lv['n']
    return c, None
cross_unwritten = []
for cid, cj in courses.items():
    for lv in cj.get('levels', []):
        for r in refs_of_level(cid, lv):
            c, n = parse(r); t = lv_of(c, n)
            if t and not any((c, l) in lessons for l in t.get('lessons', [])):
                cross_unwritten.append((f'{cid}/L{lv["n"]}', r, level_written(cid, lv)))
print('requires edges into a level with no written lesson:', len(cross_unwritten),
      '; from a written level:', sum(1 for x in cross_unwritten if x[2]))
for x in cross_unwritten:
    if x[2]: print('  ', x[0], '->', x[1])
def closure(refs):
    seen = set(); stack = [parse(r) for r in refs]
    while stack:
        c, n = stack.pop()
        if n is None or (c, n) in seen: continue
        seen.add((c, n)); lv = lv_of(c, n)
        if lv: stack += [parse(r) for r in refs_of_level(c, lv)]
        lr = courses.get(c, {}).get('lessonRequires', {})
        for lid in (lv or {}).get('lessons', []):
            stack += [parse(r) for r in lr.get(lid, [])]
    return seen
for m in ['mock-superday-trader', 'mock-superday-research', 'mock-oa-quant-data', 'mock-oa-code']:
    s = closure(J('exams', m + '.json').get('requires', []))
    nl = sum(len(lv_of(c, n).get('lessons', [])) for c, n in s)
    print(f'{m}: {len(s)} levels, {len({c for c, _ in s})} courses, {nl} mapped lessons; includes',
          sorted({c for c, _ in s} & {'ds', 'graphs-dp', 'algo-think', 'contests', 'integrals', 'multivar'}))
for c in ['coding-int', 'systems', 'research-int', 'puzzles', 'brainteasers']:
    s = closure(refs_of_level(c, lv_of(c, 1))) - {(c, 1)}
    print(f'{c}/L1 closure: {len(s)} levels')
for e in ['coding-int/L1', 'coding-int/L4', 'systems/L1', 'pdes/L1', 'pdes/L3']:
    c, n = parse(e); print(e, 'requires', lv_of(c, n).get('requires'))

print('== N04 prep mocks ==')
ptxt = json.dumps(J('prep.json'))
miss = [m for m in re.findall(r'"(mock-[a-z0-9-]+)"', ptxt) if not ex('exams', m + '.json')]
print('references to missing mocks', len(miss), Counter(miss))

print('== F05.7 oa drills ==')
oa = [J('drills', f) for f in os.listdir(os.path.join(C, 'drills')) if f.startswith('oa') and f.endswith('.json')]
print('oa drills', len(oa), 'by difficulty', dict(Counter(d.get('difficulty') for d in oa)),
      'languages', dict(Counter(d.get('language', 'python') for d in oa)))
print('mock-oa-code draw', [p.get('draw') for p in J('exams', 'mock-oa-code.json')['parts'] if p.get('draw')])

print('== longform and self-marked items ==')
lf = Counter()
for root, _, fs in os.walk(os.path.join(C, 'courses')):
    for f in fs:
        if f.endswith('.json') and f != 'course.json':
            k = 'review' if f.startswith('review') else 'homework' if f.startswith('homework') else 'lesson'
            lf[k] += json.dumps(json.load(open(os.path.join(root, f)))).count('"kind": "longform"')
print('longform widgets by file kind', dict(lf))

print('== N05/F08 cited lines ==')
cites = [('ito/l1-walk-to-bm.json', 904, 'blows it up'), ('pdes/l1-equations-in-two-variables.json', 1194, 'only'),
         ('ito/l13-martingale-or-not.json', 1044, 'exactly when'), ('ito/l17-derivation-aloud.json', 882, 'any claim'),
         ('random-vars/l5-long-run-average.json', 4030, 'symmetric')]
for f, n, needle in cites:
    lines = open(os.path.join(C, 'courses', f), encoding='utf-8').read().split('\n')
    hit = [i + 1 for i, l in enumerate(lines) if needle in l]
    print(f, 'line', n, 'has needle' if needle in lines[n - 1] else 'NO', '; needle at', hit[:6])
for f, words in [('ito/l13-martingale-or-not.json', ['local', 'integrab']),
                 ('ito/l17-derivation-aloud.json', ['European', 'American', 'Asian', 'barrier', 'path-dependent'])]:
    t = open(os.path.join(C, 'courses', f), encoding='utf-8').read()
    print(f, {w: t.count(w) for w in words})
cand = 0; by_course = Counter()
for (cid, lid), d in lessons.items():
    s = d.get('summary', {})
    parts = list(s.get('ideas', []) or []) + [s.get('trap', '')] + [((s.get('formula') or {}) if isinstance(s.get('formula'), dict) else {}).get('note', '')]
    for p in parts:
        if re.search(r'\b(only|exactly when|any|always|never)\b', str(p)):
            cand += 1; by_course[cid] += 1
print('summary candidate lines (only, exactly when, any, always, never):', cand, 'in', len(by_course), 'courses')
SEVEN = ('ito', 'measure-prob', 'pdes', 'markov', 'limits-thm', 'random-vars', 'research-int')
print('  in the seven N05 courses:', sum(by_course[c] for c in SEVEN), {c: by_course[c] for c in SEVEN})

print('== Performance-task rule sizing (DECISIONS "Performance tasks") ==')
ALWAYS = ('write', 'derive', 'prove', 'build', 'code', 'implement', 'design')
EXPL = ('explain', 'defend', 'justify')
INTERVIEW = {'recruiting', 'brainteasers', 'puzzles', 'mm-games', 'mental-pressure', 'game-theory', 'coding-int',
             'research-int', 'systems', 'ito', 'measure-prob', 'pdes'}
hits = Counter(); hit_list = []
for cid, cj in courses.items():
    st = stage_of[cid]
    if st == 0 and cid not in ('first-python', 'terminal'): continue
    # The rule reads the lesson files' objectives lists. course.json lessonObjectives (one line per lesson) matches
    # only 83 levels, so a validator rule must read the lesson files.
    for lv in cj.get('levels', []):
        if not level_written(cid, lv): continue
        ok = False
        for lid in lv['lessons']:
            for o in lessons[(cid, lid)].get('objectives', []):
                w = (re.match(r'[A-Za-z]+', o.strip()) or [''])[0].lower()
                if w in ALWAYS or (w in EXPL and (st in (2, 3) or cid in INTERVIEW)): ok = True
        if ok:
            key = 'interview' if cid in INTERVIEW else f'stage {st}'
            hits[key] += 1; hit_list.append(f'{cid}/L{lv["n"]}')
print('written levels matched:', sum(hits.values()), dict(sorted(hits.items())))
print('  by stage:', dict(Counter(stage_of[x.split('/')[0]] for x in hit_list)))
