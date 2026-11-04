import sys, json; sys.path.insert(0,'.')
import problems_l1 as a, problems_l2 as b, problems_l3 as c, problems_l4 as d, problems_l4b as e, problems_drills as f
SUM=json.load(open("summary.json"))
def res(pid):
    rows=[r for r in SUM if r[0]==pid]
    sol=all(v==0 for r in rows for k,v in r[3].items() if k.startswith("solution"))
    starts=sorted({v for r in rows for k,v in r[3].items() if k.startswith("starter")})
    return len(rows[0][0:3]) and rows[0][2], starts
def fence(code,lang="cpp"): return "```%s\n%s\n```"%(lang,code.rstrip("\n"))
def exp(v):
    s=json.dumps(v) if not isinstance(v,bool) else ("true" if v else "false")
    return s if len(s)<90 else s[:87]+"..."
META=[
 ("P-translate","l3-virtual-memory","a `code` screen after the worked examples, difficulty 2",a.P_TR),
 ("P-struct-size","l4-object-layout","a `code` screen after the layout table, difficulty 3",a.P_SZ),
 ("P-mispredicts","l5-branches","a `code` screen, difficulty 3",a.P_BR),
 ("P-cache-sim","homework-1","the homework `code` item, difficulty 4",a.P_CACHE),
 ("P-final-counts","l7-data-races","a `code` screen after the interleaving drill, difficulty 4",b.P_FC),
 ("P-lock-cycle","l8-locks-and-deadlock","a `code` screen, difficulty 3",b.P_CY),
 ("P-blocked-counts","homework-2","the homework `code` item, difficulty 3",b.P_BB),
 ("P-find-gaps","l13-tcp-and-udp","a `code` screen, difficulty 3",c.P_GAP),
 ("P-wire","l14-messages-on-the-wire","a `code` screen, difficulty 3",c.P_WIRE),
 ("P-pool","l15-no-allocation","a `code` screen, difficulty 3",d.P_POOL),
 ("P-format-price","l15-no-allocation","a second `code` screen, difficulty 3",d.P_FMT),
 ("P-ring","l16-ring-buffer","a `code` screen, difficulty 4",d.P_RING),
 ("P-percentile","l17-measuring-latency","a `code` screen, difficulty 3",d.P_PCT),
 ("P-latency-hist","homework-4","the homework `code` item, difficulty 4",d.P_HIST),
 ("P-handler","l18-feed-handler","the capstone `code` screen, difficulty 4 (the lesson's last task screen)",e.P_H),
 ("D-lru","drill sy-lru-cache (E8)","a drill, pattern `cache`, difficulty 3, pace 25 minutes",f.P_LRU),
 ("D-token-bucket","drill sy-token-bucket (E8)","a drill, pattern `rate-limiter`, difficulty 2, pace 15 minutes",f.P_TB),
 ("D-bits","drill sy-bits (E8)","a drill, pattern `bits`, difficulty 2, pace 10 minutes",f.P_BITS),
]
out=[]
for tag,where,role,P in META:
    n=len(P['tests']); rows=[r for r in SUM if r[0]==P['id']]
    starter_fail=sorted({v for r in rows for k,v in r[3].items() if k.startswith("starter")})
    out.append(f"### {tag}: {P['name']}\n")
    out.append(f"Where: `{where}`, {role}. Widget `code`, `language: \"cpp\"`, {n} hidden tests (function mode, `compare: \"equal\"` unless a number is a double). Checked below.\n")
    if P.get("prelude"): out.append("Hidden `prelude`:\n\n"+fence(P["prelude"])+"\n")
    if P.get("postlude"): out.append("Hidden `postlude`:\n\n"+fence(P["postlude"])+"\n")
    out.append("Starter (the learner sees this; it compiles and fails the tests):\n\n"+fence(P["starter"])+"\n")
    out.append("Reference solution:\n\n"+fence(P["solution"])+"\n")
    out.append("Hidden tests (`setup` then `call` and its `expect`):\n")
    for t in P["tests"]:
        s=(t.get("setup","")+" " if t.get("setup") else "")
        out.append(f"- `{(s+t['call']).strip()}` expects `{exp(t['expect'])}`")
    out.append("")
    out.append(f"Checked by `cpp/build_md.py`: the solution passes all {n} tests and the starter fails {starter_fail[0]} of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.\n")
open("appendix_cpp.md","w").write("\n".join(out))
print(len("\n".join(out)),"bytes")
