import json,sys,re,os
SKIP={"id","kind","layout","keyboard","placeholder","skills","course","type","canvas","starter","solution","tests","code","hidden","files","highlight","rung","label","unit","controls","objectives","summary"}
def walk(o,out,key=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in SKIP: continue
            walk(v,out,k)
    elif isinstance(o,list):
        for v in o: walk(v,out,key)
    elif isinstance(o,str):
        out.append(f"[{key}] "+o.replace("\n"," ")[:int(os.environ.get('MX','600'))])
    elif isinstance(o,(int,float)) and key in("answer","value"):
        out.append(f"[{key}] {o}")
f=sys.argv[1]; d=json.load(open(f))
def emit(tag,o):
    out=[]; walk(o,out)
    print(f"\n##### {os.path.basename(f)} {tag}")
    for l in out: print(" ",l)
if 'screens' in d:
    for i,s in enumerate(d['screens']): emit(f"screen {i}",s)
    for i,s in enumerate(d.get('quiz',[])): emit(f"quiz {i}",s)
else:
    for i,s in enumerate(d['items']):
        if 'topic-' in f and not re.search(r'gv-|garch',json.dumps(s.get('skills',''))+s.get('id','')): continue
        emit(f"item {i} {s.get('id','')}",s)
