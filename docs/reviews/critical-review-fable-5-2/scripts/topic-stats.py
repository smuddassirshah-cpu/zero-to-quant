#!/usr/bin/env python3
"""Per-topic counts for the self-containment gap table (read-only).
Usage: topic-stats.py            one row per topic
       topic-stats.py --titles   lesson titles and skills per course"""
import json,glob,sys,collections,os
C='app/content'; cur=json.load(open(f'{C}/curriculum.json'))
def items_of(d):
    out=list(d.get('items',[]))
    for p in d.get('parts',[]): out+=p.get('items',[])
    return out
def multi(it):  # an item that chains: authored parts, a table with 3+ answers, or longform
    w=it.get('widget') or {}
    if it.get('parts') or it.get('kind')=='longform': return True
    if w.get('kind')=='table': return sum(1 for r in w.get('rows',[]) for c in r if isinstance(c,dict))>=3
    return False
if '--titles' in sys.argv:
    for s in cur['stages']:
        for t in s['topics']:
            print(f"\n## {t['id']} {t['name']} ({t.get('hours')} h; resource: {(t.get('resource') or {}).get('name')})")
            for c in t['courses']:
                d=json.load(open(f'{C}/courses/{c}/course.json'))
                print(f" {c}: skills = "+'; '.join(d['skills'].values()))
                for l in d['levels']: print(f"   L{l['n']} {l['name']}: "+' | '.join(d['lessonNames'].get(x,x) for x in l['lessons']))
    sys.exit()
print('topic|name|stored h|lessons|lesson h|graded items|per skill|code|multi-step|longform|hw+review items|exam items|drills')
drills=collections.Counter()
for f in glob.glob(f'{C}/drills/*.json'):
    d=json.load(open(f))
    if isinstance(d,dict) and d.get('course') and 'sample' not in f: drills[d['course']]+=1
for s in cur['stages']:
    for t in s['topics']:
        L=mins=g=code=ms=lf=sets=0; skills=set()
        for c in t['courses']:
            skills|=set(json.load(open(f'{C}/courses/{c}/course.json'))['skills'])
            for f in glob.glob(f'{C}/courses/{c}/*.json'):
                b=os.path.basename(f)
                if b=='course.json' or 'sample' in b: continue
                d=json.load(open(f))
                if b.startswith('l'):
                    L+=1; mins+=d.get('minutes',0)
                    its=[x for x in d.get('screens',[]) if x.get('widget')]+d.get('quiz',[])
                else:
                    its=items_of(d); sets+=len(its)
                for it in its:
                    g+=1; w=it.get('widget') or {}
                    code+=w.get('kind')=='code'; ms+=multi(it); lf+=it.get('kind')=='longform'
        ex=0
        p=f"{C}/exams/topic-{t['id']}.json"
        if os.path.exists(p): ex=len(items_of(json.load(open(p))))
        dr=sum(drills[c] for c in t['courses'])
        print(f"{t['id']}|{t['name'][:28]}|{t.get('hours')}|{L}|{mins/60:.0f}|{g}|{g/max(1,len(skills)):.0f}|{code}|{ms}|{lf}|{sets}|{ex}|{dr}")
