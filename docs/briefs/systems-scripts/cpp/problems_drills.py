import sys, collections; sys.path.insert(0,'.')
from harness import run
from fractions import Fraction
def il(l): return "{"+", ".join(map(str,l))+"}"
def sl(l): return "{"+", ".join('"'+x+'"' for x in l)+"}"
# ---- LRU
def lru(cap,ops):
    d=collections.OrderedDict(); out=[]
    for o in ops:
        t=o.split()
        if t[0]=='p':
            k,v=int(t[1]),int(t[2])
            if k in d: d.move_to_end(k)
            d[k]=v
            if len(d)>cap: d.popitem(last=False)
        else:
            k=int(t[1])
            if k in d: d.move_to_end(k); out.append(d[k])
            else: out.append(-1)
    return out
lc=[(2,["p 1 10","p 2 20","g 1","p 3 30","g 2","g 3","g 1"]),(1,["p 1 5","p 2 6","g 1","g 2"]),(2,["p 1 1","p 2 2","p 1 9","p 3 3","g 1","g 2","g 3"]),(3,["g 7"]),(2,["p 1 1","p 2 2","g 1","g 1","p 3 3","g 2","g 1"]),(0,["p 1 1","g 1"]),
    (3,["p 1 1","p 2 2","p 3 3","p 4 4","g 1","g 2","g 3","g 4","p 5 5","g 2","g 3","g 4","g 5"])]
P_LRU=dict(id="lru_cache",name="drill sy-lru-cache: least recently used cache",
 postlude='''#include <cstdio>
#include <string>
#include <vector>

// hidden driver: "p k v" puts, "g k" gets; the result lists every get (value or -1)
std::vector<int> drive(int capacity, const std::vector<std::string>& ops) {
    LRU cache(capacity);
    std::vector<int> out;
    for (const auto& op : ops) {
        int k = 0, v = 0;
        if (op[0] == 'p') { std::sscanf(op.c_str(), "p %d %d", &k, &v); cache.put(k, v); }
        else { std::sscanf(op.c_str(), "g %d", &k); out.push_back(cache.get(k)); }
    }
    return out;
}
''',
 starter='''#include <list>
#include <unordered_map>

// A cache of at most `capacity` keys. get(k) returns the value or -1, and counts as a use.
// put(k, v) stores or updates k (also a use); when over capacity, drop the least recently used key.
// Both calls take constant time on average.
class LRU {
public:
    explicit LRU(int capacity) : capacity_(capacity) {}
    int get(int key) {
        auto it = values_.find(key);
        return it == values_.end() ? -1 : it->second;      // does not count as a use yet
    }
    void put(int key, int value) {
        values_[key] = value;
        if (static_cast<int>(values_.size()) > capacity_) values_.erase(values_.begin());   // not the oldest
    }
private:
    int capacity_;
    std::unordered_map<int, int> values_;
};
''',
 solution='''#include <list>
#include <unordered_map>

class LRU {
public:
    explicit LRU(int capacity) : capacity_(capacity) {}
    int get(int key) {
        auto it = where_.find(key);
        if (it == where_.end()) return -1;
        order_.splice(order_.begin(), order_, it->second);   // move to the front: most recent
        return it->second->second;
    }
    void put(int key, int value) {
        if (capacity_ <= 0) return;
        auto it = where_.find(key);
        if (it != where_.end()) {
            it->second->second = value;
            order_.splice(order_.begin(), order_, it->second);
            return;
        }
        order_.emplace_front(key, value);
        where_[key] = order_.begin();
        if (static_cast<int>(order_.size()) > capacity_) {
            where_.erase(order_.back().first);
            order_.pop_back();
        }
    }
private:
    int capacity_;
    std::list<std::pair<int, int>> order_;                       // front = most recent
    std::unordered_map<int, std::list<std::pair<int, int>>::iterator> where_;
};
''',
 tests=[dict(call=f"drive({c}, {sl(o)})",expect=lru(c,o)) for c,o in lc])
# ---- token bucket (exact rational reference)
def bucket(rate,burst,times):
    tok=Fraction(burst); last=0; out=[]
    for t in times:
        tok=min(Fraction(burst),tok+Fraction(rate)*Fraction(t-last,10**9)); last=t
        if tok>=1: tok-=1; out.append(1)
        else: out.append(0)
    return out
bc=[(1000,3,[0,0,0,0]),(1000,3,[0,0,0,0,1_000_000,1_000_000]),(1000,1,[0,500_000,1_000_000,1_500_000,2_000_000]),(2,2,[0,0,0,250_000_000,500_000_000,1_000_000_000]),(10,5,[0,1_000_000_000,1_000_000_001]),(1_000_000_000,2,[0,0,0,1,2,3]),(100,3,[10**12,10**12,10**12,10**12])]
P_TB=dict(id="token_bucket",name="drill sy-token-bucket: a rate limiter",
 postlude='''#include <vector>

std::vector<int> drive(long long rate, long long burst, const std::vector<long long>& times) {
    TokenBucket b(rate, burst);
    std::vector<int> out;
    for (long long t : times) out.push_back(b.allow(t) ? 1 : 0);
    return out;
}
''',
 starter='''// rate tokens a second refill continuously, up to burst tokens. The bucket starts full.
// allow(now_ns) is called with non-decreasing times in nanoseconds. It returns true and spends one token
// if a whole token is available, else false. Use integers only: no floating point.
class TokenBucket {
public:
    TokenBucket(long long rate, long long burst) : rate_(rate), burst_(burst), tokens_(burst) {}
    bool allow(long long now_ns) {
        (void)now_ns;
        if (tokens_ < 1) return false;     // never refills
        --tokens_;
        return true;
    }
private:
    long long rate_, burst_, tokens_;
};
''',
 solution='''// Tokens are counted in billionths of a token, so a nanosecond at `rate` per second adds exactly `rate` units.
class TokenBucket {
public:
    TokenBucket(long long rate, long long burst)
        : rate_(rate), cap_(burst * kUnit), units_(burst * kUnit) {}
    bool allow(long long now_ns) {
        units_ += (now_ns - last_) * rate_;
        if (units_ > cap_) units_ = cap_;
        last_ = now_ns;
        if (units_ < kUnit) return false;
        units_ -= kUnit;
        return true;
    }
private:
    static constexpr long long kUnit = 1000000000LL;
    long long rate_, cap_, units_;
    long long last_ = 0;
};
''',
 tests=[dict(call=f"drive({r}, {b}, std::vector<long long>{il(t)})",expect=bucket(r,b,t)) for r,b,t in bc])
# ---- bits
def np2(x):
    p=1
    while p<x: p*=2
    return p
def bsw(x): return int.from_bytes(x.to_bytes(4,'big'),'little')
def pc(x): return bin(x).count('1')
P_BITS=dict(id="bits",name="drill sy-bits: powers of two and byte order",
 starter='''// next_pow2(x): the smallest power of two >= x (1 for x = 0 or 1). x is at most 2^30.
// is_pow2(x): true for 1, 2, 4, 8, ... and false for 0.
// popcount(x): the number of 1 bits. bswap32(x): reverse the four bytes of x.
unsigned next_pow2(unsigned x) { return x; }
bool is_pow2(unsigned x) { return x % 2 == 0; }
int popcount(unsigned x) { return static_cast<int>(x); }
unsigned bswap32(unsigned x) { return x; }
''',
 solution='''unsigned next_pow2(unsigned x) {
    unsigned p = 1;
    while (p < x) p <<= 1;
    return p;
}
bool is_pow2(unsigned x) { return x != 0 && (x & (x - 1)) == 0; }
int popcount(unsigned x) {
    int n = 0;
    while (x) { x &= x - 1; ++n; }      // clears the lowest set bit
    return n;
}
unsigned bswap32(unsigned x) {
    return (x >> 24) | ((x >> 8) & 0x0000FF00u) | ((x << 8) & 0x00FF0000u) | (x << 24);
}
''',
 tests=[dict(call=f"(long long)next_pow2({x}u)",expect=np2(x)) for x in (0,5,8,1000,1<<30)]
      +[dict(call=f"is_pow2({x}u)",expect=(x>0 and x&(x-1)==0)) for x in (0,6,64,4294967295)]
      +[dict(call=f"popcount({x}u)",expect=pc(x)) for x in (0,4294967295,1<<31)]
      +[dict(call=f"(long long)bswap32({x}u)",expect=bsw(x)) for x in (1,0x12345678,0x0000FF00)])
if __name__=="__main__":
    for P in (P_LRU,P_TB,P_BITS):
        print(P['name']); [print("  ",(t.get('setup','')+' '+t['call'])[:120],"->",str(t['expect'])[:70]) for t in P['tests']]
        print("ALL OK" if run(P) else "PROBLEM")
