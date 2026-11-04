import sys, struct, math, collections; sys.path.insert(0,'.')
from harness import run
def il(l): return "{"+", ".join(map(str,l))+"}"
COUNT='''#include <cstdlib>
#include <new>
static int g_allocs = 0;   // counts every call to operator new
void* operator new(std::size_t n) { ++g_allocs; void* p = std::malloc(n ? n : 1); if (!p) std::abort(); return p; }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }
'''
# ---------------- l15 pool
P_POOL=dict(id="pool",name="l15-no-allocation: a pool of slots", prelude=COUNT,
 starter='''#include <vector>

// A pool of `slots` fixed slots, numbered 0 .. slots-1.
// allocate() returns a free slot, or -1 if none is free. release(s) makes slot s free again.
// The most recently released slot is the next one allocated. No call may use the heap after the constructor.
class Pool {
public:
    explicit Pool(int slots) : slots_(slots) {}
    int allocate() { return next_++; }          // never reuses a slot
    void release(int slot) { (void)slot; }
    int in_use() const { return next_; }
private:
    int slots_;
    int next_ = 0;
};
''',
 solution='''#include <vector>

class Pool {
public:
    explicit Pool(int slots) : next_free_(slots, -1), in_use_(0) {
        for (int s = 0; s + 1 < slots; ++s) next_free_[s] = s + 1;   // slot s points at slot s+1
        head_ = slots > 0 ? 0 : -1;
    }
    int allocate() {
        if (head_ < 0) return -1;
        int slot = head_;
        head_ = next_free_[slot];
        ++in_use_;
        return slot;
    }
    void release(int slot) {
        next_free_[slot] = head_;
        head_ = slot;
        --in_use_;
    }
    int in_use() const { return in_use_; }
private:
    std::vector<int> next_free_;   // the free list, stored inside the slots' own indices
    int head_;
    int in_use_;
};
''',
 tests=[
  dict(setup="Pool p(3);",call="p.allocate()",expect=0),
  dict(setup="Pool p(3); p.allocate(); p.allocate();",call="p.allocate()",expect=2),
  dict(setup="Pool p(3); p.allocate(); p.allocate(); p.allocate();",call="p.allocate()",expect=-1),
  dict(setup="Pool p(3); int a = p.allocate(); int b = p.allocate(); p.allocate(); p.release(b);",call="p.allocate()",expect=1),
  dict(setup="Pool p(3); int a = p.allocate(); int b = p.allocate(); p.release(a); p.release(b);",call="p.allocate()",expect=1),
  dict(setup="Pool p(3); int a = p.allocate(); int b = p.allocate(); p.release(a); p.release(b); p.allocate();",call="p.allocate()",expect=0),
  dict(setup="Pool p(2); p.allocate(); p.allocate(); p.release(0); p.allocate();",call="p.in_use()",expect=2),
  dict(setup="Pool p(2); p.allocate(); p.allocate(); p.release(0); p.release(1);",call="p.in_use()",expect=0),
  dict(setup="Pool p(0);",call="p.allocate()",expect=-1),
  dict(setup="Pool p(8); g_allocs = 0; for (int r = 0; r < 100; ++r) { int s = p.allocate(); p.release(s); }",call="g_allocs",expect=0),
 ])
# ---------------- l15 format_price without allocation
def fmt(p):
    sign='-' if p<0 else ''; a=abs(p); return f"{sign}{a//100}.{a%100:02d}"
fp_vals=[10275,5,0,-25,100000,1999,-5,99]
P_FMT=dict(id="format_price",name="l15-no-allocation: format a price in place", prelude=COUNT,
 starter='''#include <vector>

// Write a price given in pence as pounds and pence into out, for example 10275 -> "102.75", -25 -> "-0.25".
// Put a '\\0' after the text and return its length (not counting the '\\0'). out has room for 32 characters.
// The hot path may not use the heap.
int format_price(char* out, int pence) {
    std::vector<char> digits;                 // allocates
    bool negative = pence < 0;
    long long a = negative ? -(long long)pence : pence;
    do { digits.push_back(static_cast<char>('0' + a % 10)); a /= 10; } while (a > 0);
    while (digits.size() < 3) digits.push_back('0');
    int n = 0;
    if (negative) out[n++] = '-';
    for (int i = static_cast<int>(digits.size()) - 1; i >= 0; --i) {
        out[n++] = digits[i];
        if (i == 2) out[n++] = '.';
    }
    out[n] = '\\0';
    return n;
}
''',
 solution='''int format_price(char* out, int pence) {
    int n = 0;
    long long a = pence;
    if (a < 0) { out[n++] = '-'; a = -a; }
    long long pounds = a / 100;
    int pennies = static_cast<int>(a % 100);
    char tmp[24];
    int t = 0;
    do { tmp[t++] = static_cast<char>('0' + pounds % 10); pounds /= 10; } while (pounds > 0);
    while (t > 0) out[n++] = tmp[--t];
    out[n++] = '.';
    out[n++] = static_cast<char>('0' + pennies / 10);
    out[n++] = static_cast<char>('0' + pennies % 10);
    out[n] = '\\0';
    return n;
}
''',
 tests=[dict(setup=f"char buf[32]; int n = format_price(buf, {v});",call="std::string(buf, n)",expect=fmt(v)) for v in fp_vals]
       +[dict(setup="char buf[32]; g_allocs = 0; format_price(buf, 10275); format_price(buf, -25);",call="g_allocs",expect=0)])
# ---------------- l16 ring buffer
def ring(cap,ops):
    q=collections.deque(); out=[]
    for o in ops:
        if o>0:
            if len(q)<cap: q.append(o); out.append(1)
            else: out.append(0)
        else:
            out.append(q.popleft() if q else -1)
    return out
rcases=[(4,[1,2,3,4,5,0,0,0,0,0]),(4,[1,2,3,0,0,4,5,6,0,0,0,0]),(2,[0]),(1,[7,8,0,9,0,0]),(8,[]),
        (4,[1,2,3,4,0,5,0,6,0,7,0,8,0,0,0,0,0]),(2,[1,2,3,0,3,0,0,0])]
# longer wrap test: 20 pushes/pops cycling through cap 4
long_ops=[]
for k in range(1,11): long_ops+= [k, 0]
rcases.append((4,long_ops))
long2=[1,2,3]+[v for k in range(4,24) for v in (k,0)]+[0,0,0,0]
rcases.append((4,long2))
P_RING=dict(id="ring",name="l16-ring-buffer: a single-producer ring",
 prelude="",
 postlude='''
// hidden driver: ops > 0 push that value (1 if accepted, 0 if full); ops == 0 pop (the value, or -1 if empty)
std::vector<int> drive(int capacity, const std::vector<int>& ops) {
    Ring r(capacity);
    std::vector<int> out;
    for (int op : ops) {
        if (op > 0) out.push_back(r.push(op) ? 1 : 0);
        else { int v = 0; out.push_back(r.pop(v) ? v : -1); }
    }
    return out;
}
''',
 starter='''#include <cstddef>
#include <vector>

// A fixed-size ring of ints. capacity is a power of two. push returns false when full,
// pop returns false when empty. head_ counts pops and tail_ counts pushes: both only ever grow.
// Keep head_ and tail_ at least 64 bytes apart so two cores do not share a cache line.
struct Ring {
    explicit Ring(std::size_t capacity) : buf_(capacity), mask_(capacity - 1) {}
    bool push(int v) {
        if (tail_ - head_ >= buf_.size() - 1) return false;   // one slot too early
        buf_[tail_ & mask_] = v;
        ++tail_;
        return true;
    }
    bool pop(int& out) {
        if (head_ == tail_) return false;
        out = buf_[head_ & mask_];
        ++head_;
        return true;
    }
    std::vector<int> buf_;
    std::size_t mask_;
    std::size_t head_ = 0;
    std::size_t tail_ = 0;
};
''',
 solution='''#include <cstddef>
#include <vector>

struct Ring {
    explicit Ring(std::size_t capacity) : buf_(capacity), mask_(capacity - 1) {}
    bool push(int v) {
        if (tail_ - head_ == buf_.size()) return false;     // full
        buf_[tail_ & mask_] = v;
        ++tail_;
        return true;
    }
    bool pop(int& out) {
        if (head_ == tail_) return false;                   // empty
        out = buf_[head_ & mask_];
        ++head_;
        return true;
    }
    std::vector<int> buf_;
    std::size_t mask_;
    alignas(64) std::size_t head_ = 0;
    alignas(64) std::size_t tail_ = 0;
};
''',
 tests=[dict(call=f"drive({c}, {il(o)})",expect=ring(c,o)) for c,o in rcases]
      +[dict(setup="Ring r(8);",call="(long long)((const char*)&r.tail_ - (const char*)&r.head_) >= 64",expect=True)])
# ---------------- l17 percentile
def pct(v,p):
    s=sorted(v); n=len(s); r=max(1,math.ceil(p*n/100-1e-9)); return s[r-1]
import numpy as np
from fractions import Fraction
def pct_np(v,p):   # method B: exact rational rank (numpy's inverted_cdf differs at p99.9 of 1000 samples, see notes)
    s=sorted(v); n=len(s); r=max(1,math.ceil(Fraction(str(p))*n/100)); return s[r-1]
data={"out10":([10.0]*990+[1000.0]*10),"out11":([10.0]*989+[1000.0]*11),"out1":([10.0]*999+[1000.0]),"five":[1.0,2.0,3.0,4.0,5.0]}
def mk(name):
    return {"out10":"std::vector<double> v(990, 10.0); v.insert(v.end(), 10, 1000.0);","out11":"std::vector<double> v(989, 10.0); v.insert(v.end(), 11, 1000.0);",
            "out1":"std::vector<double> v(999, 10.0); v.push_back(1000.0);","five":"std::vector<double> v = {5.0, 1.0, 4.0, 2.0, 3.0};"}[name]
pcases=[("out10",50),("out10",99),("out10",99.9),("out10",100),("out11",99),("out1",99.9),("out1",100),("five",20),("five",50),("five",80),("five",100),("five",0)]
tests=[]
for n,p in pcases:
    v=data[n]; a=pct(v,p); b=pct_np(v,p); assert a==b,(n,p,a,b)
    tests.append(dict(setup=mk(n),call=f"percentile(v, {p})",expect=a))
tests.append(dict(setup=mk("out10"),call="mean(v)",expect=sum(data["out10"])/1000))
P_PCT=dict(id="percentile",name="l17-measuring-latency: percentile and mean",
 starter='''#include <vector>

// Nearest-rank percentile: sort the samples; the p-th percentile is the value at rank ceil(p * n / 100),
// counting from 1 (rank 1 at p = 0). Subtract 1e-9 before ceil so 99 * 1000 / 100 does not round up.
double percentile(std::vector<double> samples, double p) {
    return samples.empty() ? 0.0 : samples.back();     // the last sample, unsorted
}

double mean(const std::vector<double>& samples) {
    double total = 0.0;
    for (double s : samples) total += s;
    return samples.empty() ? 0.0 : total / samples.size();
}
''',
 solution='''#include <algorithm>
#include <cmath>
#include <vector>

double percentile(std::vector<double> samples, double p) {
    if (samples.empty()) return 0.0;
    std::sort(samples.begin(), samples.end());
    double n = static_cast<double>(samples.size());
    long long rank = static_cast<long long>(std::ceil(p * n / 100.0 - 1e-9));
    if (rank < 1) rank = 1;
    if (rank > static_cast<long long>(samples.size())) rank = static_cast<long long>(samples.size());
    return samples[rank - 1];
}

double mean(const std::vector<double>& samples) {
    double total = 0.0;
    for (double s : samples) total += s;
    return samples.empty() ? 0.0 : total / samples.size();
}
''',
 tests=tests)
# ---------------- homework 4: latency histogram
def bucket(ns): return max(ns,1).bit_length()-1
def hist_pct(samples,p):
    s=sorted(bucket(x) for x in samples); n=len(s); r=max(1,math.ceil(p*n/100-1e-9)); return 2**(s[r-1]+1)
hs={"a":[10]*990+[1000]*10,"b":[1,2,3,4,5,6,7,8,9,10],"c":[0,1,2,3],"d":[1000000]*5+[100]*95}
def hset(name,vals):
    lines=[]
    # compress
    parts=[]; 
    for v,c in collections.Counter(vals).items(): parts.append(f"for (int i = 0; i < {c}; ++i) h.record({v});")
    return "LatencyHist h; "+" ".join(parts)
htests=[]
for n,p in [("a",50),("a",99),("a",99.9),("b",50),("b",90),("b",100),("c",50),("c",100),("d",90),("d",99)]:
    htests.append(dict(setup=hset(n,hs[n]),call=f"h.percentile_upper({p})",expect=hist_pct(hs[n],p)))
htests.append(dict(setup="LatencyHist h; h.record(1000); h.record(2000);",call="h.count()",expect=2))
P_HIST=dict(id="latency_hist",name="homework-4: a fixed-bucket latency histogram",prelude=COUNT,
 starter='''#include <array>

// Buckets by powers of two: a sample of ns nanoseconds goes in bucket floor(log2(max(ns, 1))), 0..39.
// percentile_upper(p) finds the bucket holding the nearest-rank p-th percentile sample
// (rank ceil(p * n / 100 - 1e-9), at least 1) and returns that bucket's upper bound, 2^(bucket + 1).
// record() must not use the heap.
class LatencyHist {
public:
    void record(long long ns) { ++total_; (void)ns; }
    long long percentile_upper(double p) const { (void)p; return 0; }
    int count() const { return total_; }
private:
    std::array<int, 40> buckets_{};
    int total_ = 0;
};
''',
 solution='''#include <array>
#include <cmath>

class LatencyHist {
public:
    void record(long long ns) {
        int b = 0;
        long long v = ns < 1 ? 1 : ns;
        while (v > 1) { v >>= 1; ++b; }
        if (b > 39) b = 39;
        ++buckets_[b];
        ++total_;
    }
    long long percentile_upper(double p) const {
        if (total_ == 0) return 0;
        long long rank = static_cast<long long>(std::ceil(p * total_ / 100.0 - 1e-9));
        if (rank < 1) rank = 1;
        long long seen = 0;
        for (int b = 0; b < 40; ++b) {
            seen += buckets_[b];
            if (seen >= rank) return 1LL << (b + 1);
        }
        return 1LL << 40;
    }
    int count() const { return total_; }
private:
    std::array<int, 40> buckets_{};
    int total_ = 0;
};
''',
 tests=htests+[dict(setup="LatencyHist h; g_allocs = 0; for (int i = 0; i < 1000; ++i) h.record(i * 37);",call="g_allocs",expect=0)])
if __name__=="__main__":
    for P in (P_POOL,P_FMT,P_RING,P_PCT,P_HIST):
        print(P['name']); [print("  ",(t.get('setup','')+' '+t['call'])[:120],"->",str(t['expect'])[:70]) for t in P['tests']]
        print("ALL OK" if run(P) else "PROBLEM")
