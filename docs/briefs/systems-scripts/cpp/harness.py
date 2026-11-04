# Test harness: mimics the app's C++ function-mode runner. Compiles solution and starter with g++ and clang++ (-std=c++17 -O1 -fno-exceptions),
# runs every case, checks the solution passes all and the starter fails at least one.
import json, subprocess, os, sys, tempfile, math
HERE=os.path.dirname(os.path.abspath(__file__))
def lit(v):
    if isinstance(v,bool): return "true" if v else "false"
    if isinstance(v,int): return f"{v}LL" if abs(v)>2**31-1 else str(v)
    if isinstance(v,float): return repr(v)
    if isinstance(v,str): return json.dumps(v)
    if isinstance(v,list): return "{"+", ".join(lit(x) for x in v)+"}"
    raise TypeError(v)
def ctype(v):
    if isinstance(v,bool): return "bool"
    if isinstance(v,int): return "long long"
    if isinstance(v,float): return "double"
    if isinstance(v,str): return "std::string"
    if isinstance(v,list): return "std::vector<"+(ctype(v[0]) if v else "long long")+">"
PRE='''#include <cstdio>
#include <cmath>
#include <string>
#include <vector>
#include <cstdint>
#include <cstddef>
#include <algorithm>
#include <initializer_list>
#include <type_traits>
'''
CMP='''
template<class A,class B> bool eqv(const A&a,const B&b){ if constexpr(std::is_floating_point<A>::value||std::is_floating_point<B>::value){ double x=(double)a,y=(double)b; return std::fabs(x-y)<=1e-9*std::max(std::fabs(x),std::fabs(y))+1e-12;} else return a==b; }
template<class A,class B> bool eqv(const std::vector<A>&a,const std::vector<B>&b){ if(a.size()!=b.size()) return false; for(size_t i=0;i<a.size();i++) if(!eqv(a[i],b[i])) return false; return true; }
'''
def build(prob, which):
    code = prob["solution"] if which=="solution" else prob["starter"]
    s=PRE+prob.get("prelude","")+"\n"+code+"\n"+prob.get("postlude","")+CMP+"\nint main(){ int fail=0;\n"
    for i,t in enumerate(prob["tests"]):
        exp=t["expect"]; ty=ctype(exp)
        s+=f'  {{ {t.get("setup","")} auto __r = ({t["call"]}); {ty} __e = {lit(exp)}; bool ok = eqv(__r, __e); if(!ok){{ fail++; std::printf("FAIL test {i}: {t["call"].replace(chr(34),chr(39)).replace(chr(92),"")[:70]}\\n"); }} }}\n'
    s+='  std::printf("%d of %d failed\\n", fail, '+str(len(prob["tests"]))+'); return fail?1:0; }\n'
    return s
def run(prob, compilers=("g++","clang++"), std="c++17"):
    ok=True; out={}
    for which in ("solution","starter"):
        src=build(prob,which)
        d=tempfile.mkdtemp(dir=HERE+"/build" if os.path.isdir(HERE+"/build") else None)
        fn=f"{d}/{prob['id']}_{which}.cpp"; open(fn,"w").write(src)
        for cxx in compilers:
            exe=fn[:-4]+"."+cxx
            r=subprocess.run([cxx,f"-std={std}","-O1","-fno-exceptions","-Wall","-Wno-unused",fn,"-o",exe],capture_output=True,text=True)
            if r.returncode!=0:
                print(f"[{prob['id']}] {which} {cxx} COMPILE ERROR\n{r.stderr[:1500]}"); ok=False; continue
            p=subprocess.run([exe],capture_output=True,text=True,timeout=20)
            last=p.stdout.strip().splitlines()[-1] if p.stdout.strip() else p.stderr[:200]
            nfail=int(last.split()[0]) if last and last[0].isdigit() else -1
            out[(which,cxx)]=nfail
            good = (nfail==0) if which=="solution" else (nfail>0)
            if not good: ok=False
            print(f"[{prob['id']}] {which:8s} {cxx:8s} {last}   {'OK' if good else 'UNEXPECTED'}")
            if which=="starter" and nfail>0 and cxx=="g++": print("   starter fails e.g.:", [l for l in p.stdout.splitlines() if l.startswith('FAIL')][:3])
    prob['_res']=out
    return ok
os.makedirs(HERE+"/build",exist_ok=True)
