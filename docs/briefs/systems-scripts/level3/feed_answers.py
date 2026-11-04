# Two independent decoders for feed.hex. Method A: struct. Method B: int.from_bytes.
import struct
from fractions import Fraction
lines=[l.strip() for l in open('feed.hex') if l.strip()]
def dec_A(h): return struct.unpack('>BBHIIIiI', bytes.fromhex(h))
def dec_B(h):
    b=bytes.fromhex(h); f=lambda a,n,s=False:int.from_bytes(b[a:a+n],'big',signed=s)
    return (b[0],b[1],f(2,2),f(4,4),f(8,4),f(12,4),f(16,4,True),f(20,4))
assert all(dec_A(h)==dec_B(h) for h in lines)
rows=[dec_A(h) for h in lines]
seen=set(); uniq=[]
for r in rows:
    if r[3] not in seen: seen.add(r[3]); uniq.append(r)
mx=max(seen); missing=sorted(set(range(1,mx+1))-seen)
trades=[r for r in uniq if r[0]==ord('T')]
vw=Fraction(sum(r[6]*r[5] for r in trades), sum(r[5] for r in trades))
print("lines",len(lines),"unique",len(uniq),"largest seq",mx,"missing",missing,len(missing))
print("trades",len(trades),"qty",sum(r[5] for r in trades),"vwap",float(vw),"as pounds",float(vw)/100)
# method B for vwap: float accumulation
num=den=0.0
for h in lines:
    r=dec_B(h)
    if r[0]==84 and r[3] in seen: pass
tot=0;q=0;done=set()
for h in lines:
    r=dec_B(h)
    if r[3] in done: continue
    done.add(r[3])
    if r[0]==84: tot+=r[6]*r[5]; q+=r[5]
print("method B vwap",tot/q, "arrival order check: 41 before 40:", [dec_A(h)[3] for h in lines[36:44]])
print("duplicates:", len(lines)-len(uniq))
