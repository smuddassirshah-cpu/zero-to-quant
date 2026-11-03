import json, os, re, glob
R = '/home/user/zero-to-quant'
C = f'{R}/app/content'
D = f'{R}/docs'

cur = json.load(open(f'{C}/curriculum.json'))
TRACK = cur['tracks']

def load(p):
    try:
        return json.load(open(p))
    except Exception:
        return None

# course maps
cmaps = {}
for cd in sorted(os.listdir(f'{C}/courses')):
    cj = load(f'{C}/courses/{cd}/course.json')
    if cj is not None:
        cmaps[cd] = cj

def strand_label(cj):
    s = cj.get('strand')
    return {'pure': 'Pure maths', 'quant': 'Quant'}.get(s, 'core')

# lesson skills (top-level key only)
lesson_skills = {}
for cd, cj in cmaps.items():
    for lv in cj.get('levels', []):
        for lid in lv.get('lessons', []):
            p = f'{C}/courses/{cd}/{lid}.json'
            if os.path.exists(p):
                l = load(p) or {}
                lesson_skills[(cd, lid)] = set(l.get('skills', []) or [])

# skill owner in course.json
skill_owner = {}
for cd, cj in cmaps.items():
    for s in cj.get('skills', {}):
        skill_owner.setdefault(s, set()).add(cd)

def level_info(cd, lv):
    cj = cmaps[cd]
    lessons = lv.get('lessons', [])
    written = [l for l in lessons if os.path.exists(f'{C}/courses/{cd}/{l}.json')]
    missing = [l for l in lessons if l not in written]
    rev = lv.get('review')
    hw = lv.get('homework')
    rev_ok = bool(rev) and os.path.exists(f'{C}/courses/{cd}/{rev}.json')
    hw_ok = bool(hw) and os.path.exists(f'{C}/courses/{cd}/{hw}.json')
    skills = set()
    for l in written:
        skills |= lesson_skills.get((cd, l), set())
    return dict(n=lv['n'], name=lv.get('name', ''), lessons=lessons, written=written,
                missing=missing, rev=rev, rev_ok=rev_ok, hw=hw, hw_ok=hw_ok, skills=skills)

# exams
exam_files = {os.path.basename(p)[:-5] for p in glob.glob(f'{C}/exams/*.json')}
mock_files = sorted(x for x in exam_files if x.startswith('mock-'))
stage_exam_ids = sorted(x for x in exam_files if x.startswith('stage-'))

def topic_exam_items(tid):
    d = load(f'{C}/exams/topic-{tid}.json')
    return d.get('items', []) if d else None

# reviews
def review_state(tid):
    p = f'{D}/reviews/review-{tid}.md'
    if not os.path.exists(p):
        return 'none'
    txt = open(p, encoding='utf-8').read()
    return 'fixed' if re.search(r'^## Fix pass', txt, re.M) else 'read-not-fixed'

def review_text(tid):
    p = f'{D}/reviews/review-{tid}.md'
    return open(p, encoding='utf-8').read() if os.path.exists(p) else ''

def tok_in(text, name):
    return re.search(r'(?<![\w-])' + re.escape(name) + r'(?![\w-])', text) is not None

def level_mentioned(text, lv, info):
    if not text:
        return False
    names = list(info['lessons'])
    if info['rev']: names.append(info['rev'])
    if info['hw']: names.append(info['hw'])
    return any(tok_in(text, n) for n in names)

def voice_files(tid):
    return sorted(os.path.basename(p) for p in glob.glob(f'{D}/reviews/voice-{tid}-*.txt'))

# planned mocks
planned = set()
for p in [f'{R}/PLAN.md', f'{D}/briefs/interview-plan.md', f'{D}/briefs/interview-gaps.md']:
    if os.path.exists(p):
        planned |= set(re.findall(r'mock-[a-z0-9-]+', open(p, encoding='utf-8').read()))
planned.discard('mock-test')  # lesson id l12-mock-test, not an exam
planned_only = sorted(planned - set(mock_files))

rows = []        # per level
topic_rows = []  # per topic
stage_rows = []

for s in cur['stages']:
    st = dict(stage=s['id'], name=s['name'], hours=s['hours'], topics=0, courses=0,
              lessons_w=0, lessons_m=0, rev_p=0, rev_m=0, hw_p=0, hw_m=0,
              topic_exams=0, stage_exam=('stage-%s' % s['id']) in stage_exam_ids,
              topic_read=0, topic_fixed=0)
    for t in s['topics']:
        tid = t['id']
        st['topics'] += 1
        cds = t['courses']
        st['courses'] += len(cds)
        items = topic_exam_items(tid)
        exam_present = items is not None
        st['topic_exams'] = st.get('topic_exams', 0)
        st['topic_exams'] += 1 if exam_present else 0
        rv = review_state(tid)
        if rv != 'none':
            st['topic_read'] += 1
        if rv == 'fixed':
            st['topic_fixed'] += 1
        # topic exam coverage
        covered = set()
        skill_only = set()
        cov_map = {}
        if items:
            item_skills = set(sk for it in items for sk in it.get('skills', []))
            for cd in cds:
                if cd not in cmaps: continue
                earlier = set()
                for lv in sorted(cmaps[cd].get('levels', []), key=lambda x: x['n']):
                    lskills = level_info(cd, lv)['skills']
                    matched = lskills & item_skills
                    new = matched - earlier
                    if (cd, lv['n']) == ('markov', 5) and tid == '1.5':
                        label = 'no'
                    elif new:
                        label = 'yes'
                    elif matched:
                        label = 'shared'
                    else:
                        label = 'no'
                    cov_map[(cd, lv['n'])] = label
                    if label == 'yes': covered.add((cd, lv['n']))
                    if label == 'shared': skill_only.add((cd, lv['n']))
                    earlier |= lskills
        rtext = review_text(tid)
        topic_levels_total = 0
        topic_levels_skill = 0
        topic_levels_cov = 0
        topic_row = dict(id=tid, name=t['name'], hours=t['hours'], track=TRACK.get(t['track'], t['track']),
                         optional=bool(t.get('optional')), exam=exam_present, rv=rv, voice=voice_files(tid),
                         courses=[])
        for cd in cds:
            cj = cmaps.get(cd)
            if cj is None:
                topic_row['courses'].append((cd, 'NO COURSE.JSON'))
                continue
            strand = strand_label(cj)
            crs_levels = []
            c_lessons_w = c_lessons_m = 0
            for lv in cj.get('levels', []):
                info = level_info(cd, lv)
                st['lessons_w'] += len(info['written'])
                st['lessons_m'] += len(info['lessons'])
                st['rev_m'] += 1
                st['hw_m'] += 1
                st['rev_p'] += int(info['rev_ok'])
                st['hw_p'] += int(info['hw_ok'])
                c_lessons_w += len(info['written']); c_lessons_m += len(info['lessons'])
                topic_levels_total += 1
                is_cov = (cd, info['n']) in covered or (cd, info['n']) in skill_only
                cov_label = {'yes': 'yes', 'shared': 'shared only', 'no': 'no'}[cov_map.get((cd, info['n']), 'no')]
                in_review = level_mentioned(rtext, lv, info)
                topic_levels_skill += int((cd, info['n']) in skill_only)
                topic_levels_cov += int(is_cov)
                complete = (len(info['written']) == len(info['lessons']) and len(info['lessons']) > 0
                            and info['rev_ok'] and info['hw_ok'])
                not_started = len(info['written']) == 0 and not info['rev_ok'] and not info['hw_ok']
                if not_started:
                    status = 'Not started'
                elif not complete:
                    status = 'Partial'
                elif not exam_present:
                    status = 'Finished, no topic exam'
                elif not is_cov:
                    status = 'Finished, not in topic exam'
                elif rv == 'none':
                    status = 'Finished except second read'
                elif rv == 'fixed' and in_review:
                    status = 'Finalised'
                elif rv == 'fixed':
                    status = 'Finished, second read pending'
                else:
                    status = 'Finished except second read'
                crs_levels.append(dict(course=cd, strand=strand, topic=tid, n=info['n'], name=info['name'],
                                       written=len(info['written']), total=len(info['lessons']),
                                       missing=info['missing'], rev=info['rev_ok'], hw=info['hw_ok'],
                                       covered=is_cov, cov_label=cov_label, in_review=in_review, status=status, optional=bool(t.get('optional'))))
            topic_row['courses'].append((cd, strand, c_lessons_w, c_lessons_m, crs_levels))
            rows.extend(crs_levels)
        topic_row['cov'] = (topic_levels_cov, topic_levels_total)
        topic_row['skill_only'] = topic_levels_skill
        topic_rows.append(topic_row)
    stage_rows.append(st)

def fmt_cov(c, total):
    if total == 0: return 'n/a'
    if c == total: return 'yes'
    if c == 0: return 'no'
    return f'partly ({c}/{total})'

import collections
fin_by_stage = collections.Counter(int(r['topic'].split('.')[0]) for r in rows if r['status'] == 'Finalised')
print('# Stage status, computed', '2026-11-03')
print()
print('## 1. Stage summary')
print('| Stage | Topics | Courses | Lessons written/mapped | Reviews present/mapped | Homework present/mapped | Topic exams / topics | Stage exam | Topics second-read | Topics fixed | Finalised levels |')
print('|---|---|---|---|---|---|---|---|---|---|---|')
for st in stage_rows:
    print(f"| {st['stage']} {st['name']} | {st['topics']} | {st['courses']} | {st['lessons_w']}/{st['lessons_m']} | {st['rev_p']}/{st['rev_m']} | {st['hw_p']}/{st['hw_m']} | {st.get('topic_exams',0)}/{st['topics']} | {'yes' if st['stage_exam'] else 'no'} | {st['topic_read']}/{st['topics']} | {st['topic_fixed']}/{st['topics']} | {fin_by_stage.get(st['stage'], 0)} |")
tot = {k: sum(s[k] for s in stage_rows) for k in ['topics','courses','lessons_w','lessons_m','rev_p','rev_m','hw_p','hw_m','topic_read','topic_fixed']}
print(f"| Total | {tot['topics']} | {tot['courses']} | {tot['lessons_w']}/{tot['lessons_m']} | {tot['rev_p']}/{tot['rev_m']} | {tot['hw_p']}/{tot['hw_m']} | {sum(s.get('topic_exams',0) for s in stage_rows)}/{tot['topics']} | {sum(1 for s in stage_rows if s['stage_exam'])}/4 | {tot['topic_read']}/{tot['topics']} | {tot['topic_fixed']}/{tot['topics']} | {sum(fin_by_stage.values())} |")
print()
print('## 2. Per topic, course, level')
for s in cur['stages']:
    print(f"\n### Stage {s['id']} {s['name']}")
    for tr in [tr for tr in topic_rows if tr['id'].split('.')[0] == str(s['id'])]:
        opt = ' [optional]' if tr['optional'] else ''
        print(f"\n**Topic {tr['id']} {tr['name']}** ({tr['track']}, {tr['hours']} h){opt}. Exam: {'yes' if tr['exam'] else 'no'}. Second read: {tr['rv']}. Voice scans: {len(tr['voice'])}. Levels covered by explicit item references: {tr['cov'][0]}/{tr['cov'][1]}; by skill only (not counted): {tr['skill_only']}.")
        print('| Course | Strand | Level | Lessons | Missing lesson ids | Review | Homework | Exam covers level | Status |')
        print('|---|---|---|---|---|---|---|---|---|')
        for c in tr['courses']:
            if len(c) == 2:
                print(f"| {c[0]} | {c[1]} | - | - | - | - | - | - | NO COURSE.JSON |")
                continue
            cd, strand, cw, cm, lvls = c
            if not lvls:
                print(f"| {cd} | {strand} | - | 0/0 | - | - | - | - | Not started |")
            for lv in lvls:
                miss = ', '.join(lv['missing']) if lv['missing'] else '-'
                print(f"| {cd} | {strand} | L{lv['n']} {lv['name']} | {lv['written']}/{lv['total']} | {miss} | {'yes' if lv['rev'] else 'no'} | {'yes' if lv['hw'] else 'no'} | {lv['cov_label']} | {lv['status']} |")

print('\n## 3. Mocks')
print('Existing:', ', '.join(mock_files) if mock_files else 'none')
print('Planned, not present (PLAN.md and briefs):', ', '.join(planned_only) if planned_only else 'none')
print('Planned count:', len(planned))

print('\n## 4. Gap inputs')
print('Missing levels (no lessons written):')
for r in rows:
    if r['written'] == 0:
        print(f"  {r['course']} L{r['n']} (topic {r['topic']}, {r['status']})")
print('Partly written levels:')
for r in rows:
    if 0 < r['written'] < r['total']:
        print(f"  {r['course']} L{r['n']}: {r['written']}/{r['total']} missing {', '.join(r['missing'])}")
print('Topics without exam:', [tr['id'] for tr in topic_rows if not tr['exam']])
print('Topics not second-read:', [tr['id'] for tr in topic_rows if tr['rv'] == 'none'])
print('Levels finished, second read pending (topic read, level not in its review):')
for r in rows:
    if r['status'] == 'Finished, second read pending':
        print(f"  {r['course']} L{r['n']} (topic {r['topic']})")
print('Shared-skill-only levels (counted as covered):')
for r in rows:
    if r['cov_label'] == 'shared only':
        print(f"  {r['course']} L{r['n']} (topic {r['topic']})")
print('Status counts:', dict(collections.Counter(r['status'] for r in rows)))
print('Topics read but not fixed:', [tr['id'] for tr in topic_rows if tr['rv'] == 'read-not-fixed'])
print('Stage exams missing:', [f"stage-{s['id']}" for s in cur['stages'] if f"stage-{s['id']}" not in stage_exam_ids])
print('Topic exams not covering all written levels:')
for tr in topic_rows:
    if tr['exam'] and tr['cov'][0] < tr['cov'][1]:
        print(f"  {tr['id']}: {tr['cov'][0]}/{tr['cov'][1]}")
