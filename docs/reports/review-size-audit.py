import json,glob,os,collections
root='app/content/courses'
courses={}
for cj in glob.glob(f'{root}/*/course.json'):
    cid=os.path.basename(os.path.dirname(cj)); courses[cid]=json.load(open(cj))
def refs(entries):
    for e in entries or []:
        if isinstance(e,str): yield e,True
        else: yield e['ref'], e.get('gate',True)
explicit=collections.defaultdict(set)   # target level -> set of dependants (gating)
diag=collections.defaultdict(set)
implicit=collections.defaultdict(set)
lessonref=collections.defaultdict(set)
lesson_level={}
for cid,co in courses.items():
    for lv in co['levels']:
        for l in lv.get('lessons',[]): lesson_level[(cid,l)]=lv['n']
for cid,co in courses.items():
    lvs=co['levels']
    for i,lv in enumerate(lvs):
        src=f"{cid}/L{lv['n']}"
        ent=lv.get('requires')
        if ent is None and i>0: implicit[f"{cid}/L{lvs[i-1]['n']}"].add(src)
        for r,g in refs(ent):
            c,x=r.split('/',1)
            if x.startswith('L') and x[1:].isdigit(): tgt=r
            else:
                n=lesson_level.get((c,x)); tgt=f"{c}/L{n}" if n else None
                if tgt: lessonref[tgt].add(src)
                continue
            (explicit if g else diag)[tgt].add(src)
    for les,ent in (co.get('lessonRequires') or {}).items():
        for r,g in refs(ent):
            c,x=r.split('/',1)
            if x.startswith('L') and x[1:].isdigit() and g: explicit[r].add(f"{cid}/{les}")
# exams requires
for ej in glob.glob('app/content/exams/*.json'):
    e=json.load(open(ej))
    for r in e.get('requires') or []:
        c,x=r.split('/',1)
        if x.startswith('L') and x[1:].isdigit(): explicit[r].add('exam:'+e.get('id',os.path.basename(ej)))
def nitems(tgt):
    c,l=tgt.split('/'); n=int(l[1:]); co=courses[c]
    lv=[v for v in co['levels'] if v['n']==n]
    if not lv: return None
    f=f"{root}/{c}/{lv[0].get('review','review-%d'%n)}.json"
    return len(json.load(open(f))['items']) if os.path.exists(f) else -1
rows=[]
for tgt in sorted(set(explicit)|set(implicit)|set(lessonref)):
    ni=nitems(tgt)
    rows.append((tgt,ni,len(explicit.get(tgt,())),len(lessonref.get(tgt,())),len(implicit.get(tgt,()))))
exp_short=[r for r in rows if r[2]>0 and r[1] is not None and 0<=r[1]<12]
imp_only_short=[r for r in rows if r[2]==0 and r[1] is not None and 0<=r[1]<12]
print(f"levels required explicitly (gating, level refs or exams): {sum(1 for r in rows if r[2]>0)}; of these with review under 12 items: {len(exp_short)}")
print(f"levels required only implicitly (next level) or via a lesson ref: {sum(1 for r in rows if r[2]==0)}; of these with review under 12 items: {len(imp_only_short)}")
print("missing items to reach 12 (explicit):", sum(12-r[1] for r in exp_short))
print("missing items to reach 12 (implicit/lesson-ref only):", sum(12-r[1] for r in imp_only_short))
by=collections.Counter(r[1] for r in exp_short); print("explicit size histogram:", sorted(by.items()))
print("\n# explicit-gating levels with review under 12: level, items, dependants(explicit), lesson-ref dependants, implicit")
for r in exp_short: print(f"{r[0]:22} {r[1]:3} {r[2]:3} {r[3]:3} {r[4]:3}")
open('/dev/null','w')
