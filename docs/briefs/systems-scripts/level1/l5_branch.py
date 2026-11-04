# Level 1, l5: branch predictor. Method A: state machine in code. Method B: transition table lookup.
import random
def one_bit(p,init=0):
    s=init;m=0
    for c in p:
        t=(c=='T'); pred=(s==1)
        if pred!=t: m+=1
        s=1 if t else 0
    return m
def two_bit_A(p,init=1):
    s=init;m=0
    for c in p:
        t=(c=='T'); pred=(s>=2)
        if pred!=t: m+=1
        s=min(3,s+1) if t else max(0,s-1)
    return m
NEXT={ (s,t):(min(3,s+1) if t else max(0,s-1)) for s in range(4) for t in (0,1)}
def two_bit_B(p,init=1):
    s=init;m=0
    for c in p:
        t=1 if c=='T' else 0
        m+= ((1 if s>=2 else 0)!=t); s=NEXT[(s,t)]
    return m
pats={"TTTTTTTT":"T"*8,"NNNN":"N"*4,"TNTNTNTN":"TN"*4,"TTNTTNTTN":"TTN"*3,"loop8x3":("T"*7+"N")*3,"T*3 then N*3":"TTTNNN","TTTTNTTTTN":"TTTTN"*2,"NTTT":"NTTT","TNNN":"TNNN",
 "loop8x10":("T"*7+"N")*10,"TN x20":"TN"*20,"TTN x10":"TTN"*10}
for k,p in pats.items():
    a=two_bit_A(p);b=two_bit_B(p); assert a==b; print(f"{k:14s} len={len(p):3d} 2bit(init1)={a:3d} 1bit(init0)={one_bit(p):3d}")
# also init variations for the starter bug check (1-bit)
print("--- cost: mispredict 5 ns")
for n,rate in ((1_000_000,0.5),(1_000_000,0.0)): print(n,rate,n*rate*5e-9*1000,"ms")
print("sum over random data: per-element branch taken prob 0.5 -> mispredicts ~50%; sorted -> ~0")
# random check with a seeded LCG for 10,000 draws
x=12345; seq=[]
for i in range(10000):
    x=(1103515245*x+12345)&0x7fffffff; seq.append('T' if (x>>16)&1 else 'N')
p="".join(seq); print("LCG random 10000: 2bit mispredicts",two_bit_A(p),two_bit_B(p),two_bit_A(p)/len(p))
s="".join(sorted(p)); print("sorted:",two_bit_A(s),two_bit_A(s)/len(s))
