#!/usr/bin/env python3
"""Render a lesson, review, homework, exam or drill JSON as compact text for reading.
Usage: render.py <file.json> [--brief]   (reviewer aid; reads only)"""
import json,sys
brief='--brief' in sys.argv
blind='--blind' in sys.argv  # hide answers, to attempt items as a learner
def w(spec):
    if not spec: return ''
    k=spec.get('kind'); out=[f'[{k}]']
    if k in('choice','multi'):
        for o in spec.get('options',[]):
            out.append(('  ( ) ' if blind else '  (*) ' if o.get('correct') else '  ( ) ')+str(o.get('text'))+((' || why: '+o['why']) if o.get('why') and not brief and not blind else ''))
    elif k=='code':
        out.append('  lang='+str(spec.get('language','python')))
        if not brief:
            for f in('starter','solution','tests'):
                if spec.get(f): out.append(f'  --{f}--\n'+str(spec[f]))
    else:
        if blind: return f'[{k}] '+str(spec.get('label',''))+' '+str(spec.get('unit',''))+(' cols='+json.dumps(spec.get('columns')) if spec.get('columns') else '')
        d={a:b for a,b in spec.items() if a not in('kind','wrong','placeholder')}
        out.append('  '+json.dumps(d,ensure_ascii=False)[:700 if not brief else 250])
        if spec.get('wrong') and not brief: out.append('  wrong: '+json.dumps(spec['wrong'],ensure_ascii=False)[:400])
    return '\n'.join(out)
def item(s,i):
    print(f"\n--- {i} [{s.get('type','item')}] d={s.get('difficulty','')} {s.get('title','')} {s.get('id','')} skills={s.get('skills','')}")
    if s.get('prose'): print(s['prose'])
    c=s.get('canvas')
    if c: print(f"  <canvas {c.get('kind')}> caption={(c.get('state') or {}).get('caption','')}")
    for st in s.get('steps',[]) or []: print('  step:',st.get('caption') or st.get('text') or '')
    if s.get('question'): print('Q:',s['question'])
    if s.get('widget'): print(w(s['widget']))
    for p in s.get('parts',[]) or []:
        print('  part:',p.get('question') or p.get('prose') or ''); print(w(p.get('widget')))
    if s.get('prompt'): print('PROMPT:',s['prompt'])
    if blind: return
    if not brief:
        for h in s.get('hints',[]) or []: print(f"  hint {h.get('rung')}: {h.get('text')}")
        fb=s.get('feedback') or {}
        if fb.get('correct'): print('  fb+:',fb['correct'])
        if fb.get('generic'): print('  fb-:',fb['generic'])
        for k,v in (fb.get('byKey') or {}).items(): print(f'  fb[{k}]: {v}')
    e=s.get('explain')
    if e: print('  explain:',e.get('text') if isinstance(e,dict) else e)
    for f in('rubric','model','modelAnswer','script','followUps'):
        if s.get(f) and not brief: print(f'  {f}:',json.dumps(s[f],ensure_ascii=False)[:900])
d=json.load(open(sys.argv[1]))
print('#',d.get('id'),'|',d.get('title') or d.get('name'),'| minutes',d.get('minutes'),'| kind',d.get('kind'),'| pass',d.get('pass'))
for o in d.get('objectives',[]): print(' obj:',o)
for k in('intro','note','description'):
    if d.get(k): print(k+':',d[k])
for i,s in enumerate(d.get('screens',[])): item(s,i)
if d.get('summary'): print('\nSUMMARY:',json.dumps(d['summary'],ensure_ascii=False)[:900])
for key in('quiz','items','sections','parts','task','tasks'):
    v=d.get(key)
    if not v: continue
    print(f'\n==== {key} ====')
    if isinstance(v,dict): v=[v]
    for i,s in enumerate(v):
        if isinstance(s,dict) and s.get('items'):
            print('\n## section',s.get('name') or s.get('title'),'| minutes',s.get('minutes'),'| pass',s.get('pass'),'| scoring',s.get('scoring'),'| nav',s.get('navigation'))
            for j,t in enumerate(s['items']): item(t,f'{i}.{j}')
        elif isinstance(s,dict) and s.get('kind')=='check': print('\n## self-ticked check:',s.get('name'),'-',s.get('detail'))
        elif isinstance(s,dict): item(s,i)
rest=[k for k in d if k not in('id','course','title','minutes','objectives','skills','screens','summary','quiz','items','sections','name','kind','pass','intro','note','description')]
if rest: print('\nother keys:',rest)
