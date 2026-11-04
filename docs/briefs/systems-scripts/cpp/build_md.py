# Runs every problem on g++ and clang++ (-std=c++17 and -std=c++20), then writes appendix.md for the brief from the same dicts.
import sys, io, contextlib, json; sys.path.insert(0,'.')
from harness import run
import problems_l1 as a, problems_l2 as b, problems_l3 as c, problems_l4 as d, problems_l4b as e, problems_drills as f
ORDER=[("l3-virtual-memory",a.P_TR),("l4-object-layout",a.P_SZ),("l5-branches",a.P_BR),("homework-1",a.P_CACHE),("l7-data-races",b.P_FC),("l8-locks-and-deadlock",b.P_CY),("homework-2",b.P_BB),
 ("l13-tcp-and-udp",c.P_GAP),("l14-messages-on-the-wire",c.P_WIRE),("l15-no-allocation",d.P_POOL),("l15-no-allocation",d.P_FMT),("l16-ring-buffer",d.P_RING),
 ("l17-measuring-latency",d.P_PCT),("homework-4",d.P_HIST),("l18-feed-handler",e.P_H),("drills",f.P_LRU),("drills",f.P_TB),("drills",f.P_BITS)]
allok=True; summary=[]
for where,P in ORDER:
    for std in ("c++17","c++20"):
        buf=io.StringIO()
        with contextlib.redirect_stdout(buf): ok=run(P,std=std)
        res=P['_res']; 
        if not ok: allok=False; print(buf.getvalue())
        summary.append((P['id'],std,len(P['tests']),res))
    print(P['id'],"tests",len(P['tests']),"|",{f"{k[0][:3]}-{k[1]}":v for k,v in res.items()})
print("ALL PROBLEMS OK" if allok else "SOME PROBLEM")
json.dump([(i,s,n,{f"{k[0]}-{k[1]}":v for k,v in r.items()}) for i,s,n,r in summary],open("summary.json","w"))
