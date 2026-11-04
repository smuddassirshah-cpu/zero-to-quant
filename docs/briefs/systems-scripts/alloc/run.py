import re, subprocess, sys, os, json
H='/home/user/zero-to-quant/docs/briefs/systems.md'
D=os.path.dirname(os.path.abspath(__file__))
txt=open(H).read()
def sect(tag):
    i=txt.index('### '+tag+':'); j=txt.index('\n### ',i+5); return txt[i:j]
def unlit(s):
    s=s.strip()
    return s
CMP='''
#include <cstdio>
#include <cmath>
#include <string>
#include <vector>
#include <cstdint>
#include <cstddef>
#include <algorithm>
#include <array>
#include <map>
#include <initializer_list>
#include <type_traits>
template<class A,class B> bool eqv(const A&a,const B&b){ if constexpr(std::is_floating_point<A>::value||std::is_floating_point<B>::value){ double x=(double)a,y=(double)b; return std::fabs(x-y)<=1e-9*std::max(std::fabs(x),std::fabs(y))+1e-12;} else return a==b; }
'''
PRELUDE_H='''
std::vector<int> frame(char type, char side, unsigned seq, unsigned id, unsigned qty, int price) {
    std::vector<int> b(24, 0);
    auto put = [&](int at, unsigned v, int n) { for (int k = 0; k < n; ++k) b[at + k] = (v >> (8 * (n - 1 - k))) & 0xFF; };
    b[0] = type; b[1] = side; put(2, 7, 2); put(4, seq, 4); put(8, id, 4); put(12, qty, 4); put(16, static_cast<unsigned>(price), 4); put(20, 36000000u + seq, 4);
    return b;
}
std::vector<int> cat(std::vector<std::vector<int>> parts) {
    std::vector<int> all;
    for (auto& p : parts) all.insert(all.end(), p.begin(), p.end());
    return all;
}
'''
def parse(tag):
    s=sect(tag)
    blocks=re.findall(r'```cpp\n(.*?)```',s,re.S)
    starter,sol=blocks[0],blocks[1]
    tests=re.findall(r'^- `(.*)` expects `(.*)`$',s,re.M)
    return starter,sol,tests
def split(call):
    d=0;last=-1
    for i,ch in enumerate(call):
        if ch in '({': d+=1
        elif ch in ')}':
            d-=1
            if ch=='}' and d==0: last=i
        elif ch==';' and d==0: last=i
    return (call[:last+1]+' ',call[last+1:].strip()) if last>=0 else ('',call)
def build(tag,code,tests,extra=''):
    s='#include "alloc_check.hpp"\n'+CMP+extra+'\n'+code+'\nint main(){ int fail=0;\n'
    for i,(c,e) in enumerate(tests):
        su,ex=split(c)
        s+=f'  {{ {su} auto __r = ({ex}); auto __e = ({e}); bool ok = eqv(__r, __e); if(!ok){{ fail++; std::printf("FAIL test {i}\\n"); }} }}\n'
    s+=f'  std::printf("%d of %d failed\\n", fail, {len(tests)}); return fail?1:0; }}\n'
    return s
res={}
for tag in ['P-pool','P-format-price','P-latency-hist','P-handler']:
    st,sol,tests=parse(tag)
    extra=PRELUDE_H if tag=='P-handler' else ''
    for which,code in (('solution',sol),('starter',st)):
        src=build(tag,code,tests,extra); fn=f'{D}/{tag}_{which}.cpp'; open(fn,'w').write(src)
        for cxx in ('g++','clang++'):
            exe=f'{D}/{tag}_{which}.{cxx}'
            r=subprocess.run([cxx,'-std=c++20','-O1','-fno-exceptions','-I',D,fn,'-o',exe],capture_output=True,text=True)
            if r.returncode: print(tag,which,cxx,'COMPILE ERR',r.stderr[:800]); continue
            p=subprocess.run([exe],capture_output=True,text=True)
            print(tag,which,cxx,len(tests),'tests;',p.stdout.strip().replace('\n',' | ')[:200])
