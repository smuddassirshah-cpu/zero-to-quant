import sys; sys.path.insert(0,'.')
from harness import run
# --- Python reference models (independent of the C++ solutions) ---
def tr(table,v):
    p,o=divmod(v,4096)
    return -1 if p>=len(table) or table[p]<0 else table[p]*4096+o
def size_of(sizes):
    off=0;mx=1
    for s in sizes: off=(off+s-1)//s*s+s; mx=max(mx,s)
    return (off+mx-1)//mx*mx if sizes else 0
def best(sizes): return size_of(sorted(sizes,reverse=True))
NEXT={(s,t):(min(3,s+1) if t else max(0,s-1)) for s in range(4) for t in (0,1)}
def mp(p):
    s=1;m=0
    for c in p:
        t=1 if c=='T' else 0; m+=((1 if s>=2 else 0)!=t); s=NEXT[(s,t)]
    return m
P_TR=dict(id="translate", name="l3-virtual-memory: translate",
 starter='''#include <vector>

// frames[p] is the physical frame of virtual page p, or -1 if p is not mapped.
// Pages are 4096 bytes. Return the physical address, or -1 for a page fault.
long long translate(const std::vector<int>& frames, long long vaddr) {
    long long page = vaddr / 4096;
    if (page >= static_cast<long long>(frames.size())) return -1;
    return static_cast<long long>(frames[page]) * 4096;
}
''',
 solution='''#include <vector>

long long translate(const std::vector<int>& frames, long long vaddr) {
    long long page = vaddr / 4096;
    long long offset = vaddr % 4096;
    if (page >= static_cast<long long>(frames.size())) return -1;
    if (frames[page] < 0) return -1;
    return static_cast<long long>(frames[page]) * 4096 + offset;
}
''',
 tests=[dict(call=f"translate({{{','.join(map(str,t))}}}, {v})",expect=tr(t,v)) for t,v in
  [([7,-1,9],10876),([7,-1,9],0),([7,-1,9],4095),([7,-1,9],8192),([7,-1,9],12287),([7,-1,9],4096),([7,-1,9],20480),([3,5],4113),([],0),([0],4095)]])
def ss(l): return [dict(call=f"struct_size({{{','.join(map(str,l))}}})",expect=size_of(l)),dict(call=f"best_size({{{','.join(map(str,l))}}})",expect=best(l))]
cases=[[1,8,1],[1,4,1,4,2,4,4,4],[],[1],[2,1],[8,1],[4,1,2,1,8],[1,2,4,8,1,2,4,8]]
P_SZ=dict(id="struct_size", name="l4-object-layout: struct size",
 starter='''#include <vector>

// sizes: the size in bytes of each field, in declaration order.
// Each field is aligned to its own size (1, 2, 4 or 8).
int struct_size(const std::vector<int>& sizes) {
    int total = 0;
    for (int s : sizes) total += s;
    return total;
}

// The size after sorting the fields from largest to smallest.
int best_size(const std::vector<int>& sizes) {
    return struct_size(sizes);
}
''',
 solution='''#include <algorithm>
#include <functional>
#include <vector>

int struct_size(const std::vector<int>& sizes) {
    int offset = 0, widest = 1;
    for (int s : sizes) {
        offset = (offset + s - 1) / s * s;   // round up to a multiple of s
        offset += s;
        widest = std::max(widest, s);
    }
    return (offset + widest - 1) / widest * widest;   // tail padding
}

int best_size(const std::vector<int>& sizes) {
    std::vector<int> sorted = sizes;
    std::sort(sorted.begin(), sorted.end(), std::greater<int>());
    return struct_size(sorted);
}
''',
 tests=[t for l in cases for t in ss(l)])
P_BR=dict(id="mispredicts", name="l5-branches: two-bit predictor",
 starter='''#include <string>

// Count the mispredictions of a two-bit saturating counter on a branch history.
// 'T' is taken, 'N' is not taken. The counter runs 0..3, starts at 1,
// predicts taken at 2 or 3, moves up on T and down on N, and stops at 0 and 3.
int mispredicts(const std::string& history) {
    int taken = 0, misses = 0;   // one bit: remember the last outcome
    for (char c : history) {
        int actual = (c == 'T');
        if (taken != actual) ++misses;
        taken = actual;
    }
    return misses;
}
''',
 solution='''#include <string>

int mispredicts(const std::string& history) {
    int counter = 1, misses = 0;
    for (char c : history) {
        bool predicted_taken = counter >= 2;
        bool actual_taken = (c == 'T');
        if (predicted_taken != actual_taken) ++misses;
        if (actual_taken) { if (counter < 3) ++counter; }
        else { if (counter > 0) --counter; }
    }
    return misses;
}
''',
 tests=[dict(call=f'mispredicts("{p}")',expect=mp(p)) for p in ["TTTTTTTT","NNNN","TNTNTNTN","TTNTTNTTN","TTTNNN","TTTTTTTNTTTTTTTNTTTTTTTN","","T","TTN"*10,"NTTT"]])

# ---- homework 1: cache simulator (reference: two independent Python simulators)
import sys as _s; _s.path.insert(0,'../level1')
from collections import OrderedDict
def _simA(addrs,nl,ways):
    sets=nl//ways; S=[OrderedDict() for _ in range(sets)]; m=0
    for a in addrs:
        ln=a//64; s=S[ln%sets]
        if ln in s: s.move_to_end(ln)
        else:
            m+=1
            if len(s)==ways: s.popitem(last=False)
            s[ln]=1
    return m
def _simB(addrs,nl,ways):
    sets=nl//ways; S=[[] for _ in range(sets)]; t=0; m=0
    for a in addrs:
        t+=1; ln=a//64; s=S[ln%sets]; h=[e for e in s if e[0]==ln]
        if h: h[0][1]=t
        else:
            m+=1
            if len(s)==ways: s.remove(min(s,key=lambda e:e[1]))
            s.append([ln,t])
    return m
def _il(l): return "{"+", ".join(map(str,l))+"}"
def _ab(gap): return [x for i in range(8) for x in (8*i,gap+8*i)]
def _mat(n,o): return [8*(i*n+j) for i in range(n) for j in range(n)] if o=="row" else [8*(i*n+j) for j in range(n) for i in range(n)]
_cc=[(4,1,_ab(256)),(4,2,_ab(256)),(4,1,_ab(320)),(4,4,_mat(8,"row")),(4,4,_mat(8,"col")),(8,8,_mat(8,"col")),(512,8,[8*i for i in range(0,64,2)]),(512,8,[8*i for i in range(0,96,3)]),(4,4,[]),(2,2,[0,64,128,0,64,128])]
for _n,_w,_a in _cc: assert _simA(_a,_n,_w)==_simB(_a,_n,_w)
P_CACHE=dict(id="count_misses",name="homework-1: a cache simulator",
 starter='''#include <vector>

// A cache of num_lines lines of 64 bytes, in sets of `ways` lines each (num_lines is a multiple of ways).
// The line holding byte address a is a / 64 and it lives in set (a / 64) % (num_lines / ways).
// A full set drops its least recently used line. Start empty. Return the number of misses.
int count_misses(int num_lines, int ways, const std::vector<int>& addresses) {
    int misses = 0;
    std::vector<int> last_line(num_lines / ways, -1);     // one line per set: ignores the ways
    for (int a : addresses) {
        int line = a / 64;
        int set = line % (num_lines / ways);
        if (last_line[set] != line) { ++misses; last_line[set] = line; }
    }
    return misses;
}
''',
 solution='''#include <list>
#include <vector>

int count_misses(int num_lines, int ways, const std::vector<int>& addresses) {
    int sets = num_lines / ways;
    std::vector<std::list<int>> cache(sets);      // front = most recently used
    int misses = 0;
    for (int a : addresses) {
        int line = a / 64;
        std::list<int>& set = cache[line % sets];
        bool hit = false;
        for (auto it = set.begin(); it != set.end(); ++it) {
            if (*it == line) { set.erase(it); hit = true; break; }
        }
        if (!hit) {
            ++misses;
            if (static_cast<int>(set.size()) == ways) set.pop_back();
        }
        set.push_front(line);
    }
    return misses;
}
''',
 tests=[dict(call=f"count_misses({n}, {w}, {_il(a)})",expect=_simA(a,n,w)) for n,w,a in _cc])

if __name__=="__main__":
    for P in (P_TR,P_SZ,P_BR,P_CACHE):
        print(P['name']); [print("  ",t['call'],"->",t['expect']) for t in P['tests']]
        print("ALL OK" if run(P) else "PROBLEM")
