import json,re,glob,os,sys
C=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','..','app','content','courses','validation','')
def strings(o,path=''):
    if isinstance(o,str):
        yield path,o
    elif isinstance(o,list):
        for i,x in enumerate(o): yield from strings(x,f'{path}[{i}]')
    elif isinstance(o,dict):
        for k,v in o.items():
            if k in('tests','hiddenTests','starter','solution','id','skills'): continue
            yield from strings(v,f'{path}.{k}')
def toks(s):
    s=re.sub(r'\$[^$]*\$','#',s); s=re.sub(r'[0-9][0-9,.]*','#',s)
    return re.findall(r"[a-z#']+",s.lower())
N=int(sys.argv[1]) if len(sys.argv)>1 else 7
idx={}
for f in sorted(glob.glob(C+'*.json')):
    b=os.path.basename(f)
    if b.startswith('problems-') or b=='course.json': continue
    for p,s in strings(json.load(open(f))):
        t=toks(s)
        for i in range(len(t)-N+1):
            idx.setdefault(tuple(t[i:i+N]),(b,s))
for n in (1,2,3):
    d=json.load(open(C+f'problems-{n}.json'))
    for p,s in strings(d):
        t=toks(s); i=0; out=[]
        while i<=len(t)-N:
            g=tuple(t[i:i+N])
            if g in idx:
                j=i+N
                while j<len(t) and tuple(t[j-N+1:j+1]) in idx: j+=1
                out.append((' '.join(t[i:j]),idx[g][0])); i=j
            else: i+=1
        for run,src in out:
            if run.count('#')*2<len(run.split()): print(f'P{n}{p} | {src} | {run}')
