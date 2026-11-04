import re, struct, math, collections, sys
sys.argv=['x']
exec(open('run.py').read().split('res={}')[0])
bad=0
def chk(tag,i,got,exp):
    global bad
    if str(got)!=exp.strip('"') and not (isinstance(got,float) and abs(got-float(exp))<1e-9):
        bad+=1; print('MISMATCH',tag,i,got,exp)
# pool: exact model (LIFO stack of freed slots, else fresh counter)
_,_,T=parse('P-pool')
for i,(c,e) in enumerate(T[:9]):
    n=int(re.match(r'Pool p\((\d+)\)',c).group(1)); free=list(range(n-1,-1,-1)); used=0; vars_={}
    stmts=[x.strip() for x in c.split(';') if x.strip()]
    val=None
    for st in stmts[1:]:
        m=re.match(r'(?:int (\w) = )?p\.allocate\(\)',st)
        if m:
            val=free.pop() if free else -1
            if val>=0: used+=1
            if m.group(1): vars_[m.group(1)]=val
            continue
        m=re.match(r'p\.release\((\w+)\)',st)
        if m:
            s=vars_.get(m.group(1), None)
            if s is None: s=int(m.group(1))
            free.append(s); used-=1; continue
        if st=='p.in_use()': val=used
    chk('pool',i,val,e)
# format price
_,_,T=parse('P-format-price')
for i,(c,e) in enumerate(T[:8]):
    p=int(re.search(r'format_price\(buf, (-?\d+)\)',c).group(1))
    s=('-' if p<0 else '')+'%d.%02d'%(abs(p)//100,abs(p)%100)
    chk('fmt',i,s,e)
# hist
_,_,T=parse('P-latency-hist')
def hist(c):
    vals=[]
    for m in re.finditer(r'for \(int i = 0; i < (\d+); \+\+i\) h\.record\((\d+)\);',c): vals+=[int(m.group(2))]*int(m.group(1))
    return vals
for i,(c,e) in enumerate(T[:11]):
    vals=hist(c); 
    if 'count()' in c:
        vals=[int(x) for x in re.findall(r'h\.record\((\d+)\);',c)]; chk('hist',i,len(vals),e); continue
    p=float(re.search(r'percentile_upper\(([\d.]+)\)',c).group(1))
    cnt=collections.Counter(min(max(v,1).bit_length()-1,39) for v in vals)
    from fractions import Fraction
    n=len(vals); rank=max(1,math.ceil(Fraction(str(p))*n/100))  # exact rational
    seen=0
    for b in range(40):
        seen+=cnt[b]
        if seen>=rank: chk('hist',i,2**(b+1),e); break
# handler
_,_,T=parse('P-handler')
exec(open('/home/user/zero-to-quant/docs/briefs/systems-scripts/cpp/problems_l4b.py').read().split('def cpp_frame')[0].split('# ---------- Python reference model')[1].split('def fr(')[0].replace('class Ref','class Ref',1)) if False else None
class Ref:
    def __init__(s): s.buf=b''; s.exp=1; s.gaps=0; s.app=0; s.o={}; s.lv={'B':collections.Counter(),'S':collections.Counter()}
    def feed(s,bs):
        s.buf+=bytes(bs)
        while len(s.buf)>=24: f,s.buf=s.buf[:24],s.buf[24:]; s.fr(f)
    def fr(s,f):
        t,sd,_,seq,oid,q,px,_=struct.unpack('>BBHIIIiI',f); sd=chr(sd); t=chr(t)
        if seq<s.exp: return
        s.gaps+=max(0,seq-s.exp); s.exp=seq+1; s.app+=1
        if t=='A' and oid<1024 and 9900<=px<=10100 and sd in 'BS' and oid not in s.o: s.o[oid]=[sd,px,q]; s.lv[sd][px]+=q
        elif t=='X' and oid in s.o: o=s.o.pop(oid); s.lv[o[0]][o[1]]-=o[2]
        elif t=='T' and oid in s.o:
            o=s.o[oid]; x=min(q,o[2]); o[2]-=x; s.lv[o[0]][o[1]]-=x
            if o[2]==0: del s.o[oid]
def F(t,sd,seq,oid,q,px): return struct.pack('>BBHIIIiI',ord(t),ord(sd),7,seq,oid,q,px,36000000+seq)
for i,(c,e) in enumerate(T):
    if 'alloc_count' in c: continue
    frs=re.findall(r"frame\('(.)', '(.)', (\d+), (\d+), (\d+), (-?\d+)\)",c)
    bs=b''.join(F(a,b,int(x),int(y),int(z),int(w)) for a,b,x,y,z,w in frs)
    r=Ref()
    if 'begin() + 30' in c: r.feed(bs[:30]); r.feed(bs[30:])
    elif 'std::vector<int>{b}' in c:
        for b in bs: r.feed([b])
    else: r.feed(bs)
    q=c.rsplit(';',1)[1].strip()
    pos=lambda d:[k for k,v in d.items() if v>0]
    if q=='h.best_bid()': v=max(pos(r.lv['B']),default=0)
    elif q=='h.best_ask()': v=min(pos(r.lv['S']),default=0)
    elif q=='h.gaps()': v=r.gaps
    elif q=='h.applied()': v=r.app
    elif q.startswith('h.bid_qty'): v=r.lv['B'][int(re.search(r'\((\d+)\)',q).group(1))]
    chk('handler',i,v,e)
print('second computation mismatches:',bad)
