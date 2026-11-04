# Level 1, l2: cache misses. Method A: OrderedDict per set (LRU). Method B: list per set with explicit recency stamps.
from collections import OrderedDict
LINE=64
def simA(addrs, nlines, ways):
    sets=nlines//ways; S=[OrderedDict() for _ in range(sets)]; miss=0
    for a in addrs:
        ln=a//LINE; s=S[ln%sets]
        if ln in s: s.move_to_end(ln)
        else:
            miss+=1
            if len(s)==ways: s.popitem(last=False)
            s[ln]=1
    return miss
def simB(addrs, nlines, ways):
    sets=nlines//ways; S=[[] for _ in range(sets)]; t=0; miss=0
    for a in addrs:
        t+=1; ln=a//LINE; s=S[ln%sets]
        hit=[e for e in s if e[0]==ln]
        if hit: hit[0][1]=t
        else:
            miss+=1
            if len(s)==ways: s.remove(min(s,key=lambda e:e[1]))
            s.append([ln,t])
    return miss
def both(name, addrs, nlines, ways):
    a=simA(addrs,nlines,ways); b=simB(addrs,nlines,ways); assert a==b,(name,a,b)
    print(f"{name:55s} accesses={len(addrs):8d} misses={a:8d} hits={len(addrs)-a:8d} hit%={100*(len(addrs)-a)/len(addrs):.2f}")
    return a
D=8
BIG=(1<<30)//LINE
both("seq sum 32 doubles (4 lines, FA big cache)", [D*i for i in range(32)], BIG,BIG)
both("stride 2 over 64 doubles", [D*i for i in range(0,64,2)], BIG,BIG)
both("stride 8 over 64 doubles", [D*i for i in range(0,64,8)], BIG,BIG)
both("stride 8 over 512 doubles (64 accesses)", [D*i for i in range(0,512,8)], BIG,BIG)
# two arrays a, b 256 B apart, loop i in 0..7 reading a[i], b[i]; cache 4 lines
def ab(gap):
    out=[]
    for i in range(8): out+= [D*i, gap+D*i]
    return out
for gap in (256,320):
    for ways in (1,2,4):
        both(f"a,b gap {gap} B, 4-line cache, {ways}-way", ab(gap),4,ways)
# 8x8 matrix
def mat(n,order):
    return [D*(i*n+j) for i in range(n) for j in range(n)] if order=="row" else [D*(i*n+j) for j in range(n) for i in range(n)]
for nl in (4,8):
    for o in ("row","col"): both(f"8x8 doubles {o}-major, {nl}-line FA LRU", mat(8,o),nl,nl)
# real L1: 32 KiB, 8-way, 64 sets = 512 lines
print("--- L1 32KiB 8-way")
res={}
for n in (64,128,1000,1024):
    for o in ("row","col"):
        res[(n,o)]=both(f"N={n} {o}-major",mat(n,o),512,8)
print("--- analytic check (method C)")
for n in (64,128,1000,1024):
    row=n*n//8 if (n*8)%64==0 else None
    fits = n*n*8<=32768
    col = n*n//8 if fits else n*n
    print(n,"row",row,"col",col, "match", res[(n,'row')]==row if row else "n/a", res[(n,'col')]==col)
