# Method A: pure Python with Fractions. Method B: numpy sort with integer rank arithmetic.
import csv, math
from fractions import Fraction
import numpy as np
rows=list(csv.DictReader(open('latencies.csv')))
sent=[int(r['done_us'])-int(r['sent_us']) for r in rows]; true=[int(r['done_us'])-int(r['intended_us']) for r in rows]
def pA(v,p): s=sorted(v); n=len(s); return s[max(1,math.ceil(Fraction(str(p))*n/100))-1]
def pB(v,p10): a=np.sort(np.array(v)); n=len(a); r=max(1,-(-(p10*n)//1000)); return int(a[r-1])   # p in tenths of a percent
for name,v in (("measured (done - sent)",sent),("true (done - intended)",true)):
    out=[]
    for p in (50,90,99,99.9):
        a=pA(v,p); b=pB(v,int(round(p*10))); assert a==b,(name,p,a,b); out.append((p,a))
    print(name, "mean", round(sum(v)/len(v),2), "max", max(v), out)
late=[t for t in true if t>100]; print("requests with true latency > 100 us:", len(late), "of", len(true))
i=1000; print("row 1000:",rows[1000]); 
# catch-up: first seq after the stall with sent == intended
after=[int(r['seq']) for r in rows if int(r['seq'])>1000 and int(r['sent_us'])==int(r['intended_us'])]; print("first caught-up seq after stall:",after[0] if after else None)
