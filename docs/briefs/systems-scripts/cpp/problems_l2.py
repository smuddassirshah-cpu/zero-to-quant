import sys; sys.path.insert(0,'.'); sys.path.insert(0,'../level2')
from harness import run
import interleave as IL
def fc(T,K):
    prog=[ [(('load','r','x'),),(('addi','r',1),),(('store','x','r'),)]*K for _ in range(T)]
    B=IL.enumerate_B(prog,{'x':0},None,lambda V,R:[V.get('x',0)])
    v=[0]*(T*K+1)
    for k,n in B.items(): v[k[1]]+=n
    # method A cross-check
    A=IL.enumerate_A(prog,{'x':0},lambda st:[st['var'].get('x',0)])
    va=[0]*(T*K+1)
    for k,n in A.items(): va[k[1]]+=n
    assert v==va; return v
for a in [(2,1),(3,1),(2,2),(2,3),(1,3),(1,1),(4,1)]: print(a,fc(*a),sum(fc(*a)))
P_FC=dict(id="final_counts",name="l7-data-races: count every outcome",
 starter='''#include <vector>

// threads threads each run `increments` times: load x, add 1, store x (three steps).
// Try every interleaving of all the steps. result[v] is how many interleavings end with x == v.
std::vector<int> final_counts(int threads, int increments) {
    // Wrong model: an increment is one indivisible step.
    std::vector<int> done(threads, 0);
    std::vector<int> result(threads * increments + 1, 0);
    // count schedules of whole increments: every one ends with the full total
    std::vector<int> fact(threads * increments + 1, 1);
    for (int i = 1; i <= threads * increments; ++i) fact[i] = fact[i - 1] * i;
    long long ways = fact[threads * increments];
    for (int t = 0; t < threads; ++t) ways /= fact[increments];
    result[threads * increments] = static_cast<int>(ways);
    return result;
}
''',
 solution='''#include <vector>

namespace {
struct Walker {
    int threads, steps;                  // steps = 3 * increments, per thread
    std::vector<int> pc, reg;            // next step and register of each thread
    int x = 0;
    std::vector<int> result;
    void go() {
        bool any = false;
        for (int t = 0; t < threads; ++t) {
            if (pc[t] == steps) continue;
            any = true;
            int old_x = x, old_reg = reg[t];
            int phase = pc[t] % 3;
            if (phase == 0) reg[t] = x;            // load
            else if (phase == 1) reg[t] += 1;      // add
            else x = reg[t];                       // store
            ++pc[t];
            go();
            --pc[t];
            x = old_x;
            reg[t] = old_reg;
        }
        if (!any) ++result[x];
    }
};
}

std::vector<int> final_counts(int threads, int increments) {
    Walker w;
    w.threads = threads;
    w.steps = 3 * increments;
    w.pc.assign(threads, 0);
    w.reg.assign(threads, 0);
    w.result.assign(threads * increments + 1, 0);
    w.go();
    return w.result;
}
''',
 tests=[dict(call=f"final_counts({T}, {K})",expect=fc(T,K)) for T,K in [(1,1),(1,3),(2,1),(3,1),(2,2),(2,3),(4,1)]])
def cyc(threads):
    # method B: Kahn topological sort on lock-order graph (edge from each earlier-held lock to each later one)
    edges=set()
    for s in threads:
        for i in range(len(s)):
            for j in range(i+1,len(s)): edges.add((s[i],s[j]))
    nodes={c for s in threads for c in s}
    indeg={n:0 for n in nodes}
    for a,b in edges: indeg[b]+=1
    q=[n for n in nodes if indeg[n]==0]; seen=0
    adj={n:[] for n in nodes}
    for a,b in edges: adj[a].append(b)
    while q:
        n=q.pop(); seen+=1
        for m in adj[n]:
            indeg[m]-=1
            if indeg[m]==0: q.append(m)
    return seen<len(nodes)
cases=[["AB","BA"],["AB","AB"],["AB","BC","CA"],["AB","BC","AC"],["A","A"],["ABC","CBA"],["AB","CD"],[],["AA"],["AB","BC","CD","DA"],["ABC","BCD","ACD"],["AC","BD","CB"]]
def js(c): return "{"+", ".join('"'+s+'"' for s in c)+"}"
P_CY=dict(id="has_lock_cycle",name="l8-locks-and-deadlock: lock-order cycle",
 starter='''#include <string>
#include <vector>

// Each string is one thread: the locks it takes, in order, each held while it takes the next ("AB" takes A, then B).
// Return true if the lock-order graph (an edge from each held lock to each lock taken after it) has a cycle.
bool has_lock_cycle(const std::vector<std::string>& threads) {
    // Only spots two threads taking the same pair in opposite orders.
    for (const auto& s : threads)
        for (const auto& t : threads)
            for (size_t i = 0; i + 1 < s.size(); ++i)
                for (size_t j = 0; j + 1 < t.size(); ++j)
                    if (s[i] == t[j + 1] && s[i + 1] == t[j]) return true;
    return false;
}
''',
 solution='''#include <string>
#include <vector>

namespace {
bool visit(int n, const bool edge[26][26], int state[26]) {   // 0 new, 1 on the path, 2 finished
    state[n] = 1;
    for (int m = 0; m < 26; ++m) {
        if (!edge[n][m]) continue;
        if (state[m] == 1) return true;
        if (state[m] == 0 && visit(m, edge, state)) return true;
    }
    state[n] = 2;
    return false;
}
}

bool has_lock_cycle(const std::vector<std::string>& threads) {
    bool edge[26][26] = {};
    for (const auto& s : threads)
        for (size_t i = 0; i < s.size(); ++i)
            for (size_t j = i + 1; j < s.size(); ++j)
                edge[s[i] - 'A'][s[j] - 'A'] = true;
    int state[26] = {};
    for (int n = 0; n < 26; ++n)
        if (state[n] == 0 && visit(n, edge, state)) return true;
    return false;
}
''',
 tests=[dict(call=f"has_lock_cycle({js(c)})",expect=cyc(c)) for c in cases])
# homework: bounded buffer blocks
def bb(cap,ev):
    n=0;pb=0;cbk=0
    for e in ev:
        if e=='P':
            if n==cap: pb+=1
            else: n+=1
        else:
            if n==0: cbk+=1
            else: n-=1
    return [pb,cbk,n]
evs=[(2,"PPPCCC"),(2,"CCPP"),(1,"PPCCPC"),(3,"PPPPPPCCC"),(4,""),(2,"PCPCPC"),(2,"PPPPCC")]
P_BB=dict(id="blocked_counts",name="homework-2: bounded buffer",
 starter='''#include <string>
#include <vector>

// A queue holds at most `capacity` items. The events run in order on one thread:
// 'P' pushes an item, 'C' pops one. A push on a full queue and a pop on an empty queue each
// would block, so skip the event and count it. Return {blocked pushes, blocked pops, items left}.
std::vector<int> blocked_counts(int capacity, const std::string& events) {
    int items = 0, blocked_push = 0, blocked_pop = 0;
    for (char e : events) {
        if (e == 'P') ++items;
        else --items;
    }
    return {blocked_push, blocked_pop, items};
}
''',
 solution='''#include <string>
#include <vector>

std::vector<int> blocked_counts(int capacity, const std::string& events) {
    int items = 0, blocked_push = 0, blocked_pop = 0;
    for (char e : events) {
        if (e == 'P') {
            if (items == capacity) ++blocked_push;
            else ++items;
        } else {
            if (items == 0) ++blocked_pop;
            else --items;
        }
    }
    return {blocked_push, blocked_pop, items};
}
''',
 tests=[dict(call=f'blocked_counts({c}, "{e}")',expect=bb(c,e)) for c,e in evs])
if __name__=="__main__":
    for P in (P_FC,P_CY,P_BB):
        print(P['name']); [print("  ",t['call'],"->",t['expect']) for t in P['tests']]
        print("ALL OK" if run(P) else "PROBLEM")
