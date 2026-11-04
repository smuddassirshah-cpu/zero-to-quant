import sys, struct, collections, random; sys.path.insert(0,'.')
from harness import run
from problems_l4 import COUNT, il
# ---------- Python reference model for the handler (dict-based; independent of the C++ arrays)
class Ref:
    def __init__(s):
        s.pend=[]; s.exp=1; s.gaps=0; s.applied=0; s.orders={}; s.lv={'B':collections.Counter(),'S':collections.Counter()}
    def feed(s,bs):
        s.pend+=bs
        while len(s.pend)>=24:
            f=bytes(s.pend[:24]); del s.pend[:24]; s.frame(f)
    def frame(s,f):
        t,side,ins,seq,oid,qty,px,tm=struct.unpack('>BBHIIIiI',f)
        if seq<s.exp: return
        if seq>s.exp: s.gaps+=seq-s.exp
        s.exp=seq+1; s.applied+=1
        sd=chr(side)
        if t==ord('A'):
            if oid<1024 and 9900<=px<=10100 and sd in 'BS' and oid not in s.orders:
                s.orders[oid]=[sd,px,qty]; s.lv[sd][px]+=qty
        elif t==ord('X'):
            if oid in s.orders:
                o=s.orders.pop(oid); s.lv[o[0]][o[1]]-=o[2]
        elif t==ord('T'):
            if oid in s.orders:
                o=s.orders[oid]; ex=min(qty,o[2]); o[2]-=ex; s.lv[o[0]][o[1]]-=ex
                if o[2]==0: del s.orders[oid]
    def bb(s): 
        p=[k for k,v in s.lv['B'].items() if v>0]; return max(p) if p else 0
    def ba(s):
        p=[k for k,v in s.lv['S'].items() if v>0]; return min(p) if p else 0
    def bq(s,p): return s.lv['B'][p]
    def aq(s,p): return s.lv['S'][p]
def fr(t,side,seq,oid,qty,px): return list(struct.pack('>BBHIIIiI',ord(t),ord(side),7,seq,oid,qty,px,36000000+seq))
PRE=COUNT+'''
#include <vector>
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
def cpp_frame(t,side,seq,oid,qty,px): return f"frame('{t}', '{side}', {seq}, {oid}, {qty}, {px})"
def stream(frames): return [b for f in frames for b in f]
def scen(name, frames_spec, chunks=None, probe=None):
    """frames_spec: list of tuples; returns (setup, ref)"""
    ref=Ref(); bs=stream(fr(*f) for f in frames_spec)
    cpp="cat({"+", ".join(cpp_frame(*f) for f in frames_spec)+"})"
    return ref,bs,cpp
tests=[]
def add(frames_spec, probe_cpp, probe_py, feed_style="whole"):
    ref=Ref(); bs=stream(fr(*f) for f in frames_spec)
    cpp="cat({"+", ".join(cpp_frame(*f) for f in frames_spec)+"})"
    if feed_style=="whole":
        ref.feed(bs); setup=f"Handler h; auto s = {cpp}; h.feed(s);"
    elif feed_style=="split30":
        ref.feed(bs[:30]); ref.feed(bs[30:]); setup=f"Handler h; auto s = {cpp}; h.feed(std::vector<int>(s.begin(), s.begin() + 30)); h.feed(std::vector<int>(s.begin() + 30, s.end()));"
    elif feed_style=="bytewise":
        for b in bs: ref.feed([b])
        setup=f"Handler h; auto s = {cpp}; for (int b : s) h.feed(std::vector<int>{{b}});"
    elif feed_style=="alloc":
        ref.feed(bs); setup=f"Handler h; auto s = {cpp}; g_allocs = 0; h.feed(s);"
    tests.append(dict(setup=setup,call=probe_cpp,expect=probe_py(ref)))
base=[('A','B',1,1,100,10000),('A','S',2,2,50,10010),('A','B',3,3,40,10005)]
add(base,"h.best_bid()",lambda r:r.bb())
add(base,"h.best_ask()",lambda r:r.ba())
add(base+[('X','B',4,3,0,0)],"h.best_bid()",lambda r:r.bb())
add(base+[('T','B',4,1,30,10000)],"h.bid_qty(10000)",lambda r:r.bq(10000))
add([('A','B',1,1,100,10000),('T','B',2,1,100,10000)],"h.best_bid()",lambda r:r.bb())
add([('A','B',1,1,10,10000),('A','B',2,2,10,10001),('A','B',5,3,10,10002)],"h.gaps()",lambda r:r.gaps)
add([('A','B',1,1,10,10000),('A','B',2,2,10,10001),('A','B',2,3,99,10050)],"h.applied()",lambda r:r.applied)
add([('A','B',1,1,10,10000),('A','B',2,2,10,10001),('A','B',4,3,10,10002),('A','B',3,4,500,10050)],"h.best_bid()",lambda r:r.bb())
add([('A','B',3,1,10,10000)],"h.gaps()",lambda r:r.gaps)
add(base,"h.best_bid()",lambda r:r.bb(),"split30")
add(base+[('T','S',4,2,50,10010)],"h.best_ask()",lambda r:r.ba(),"bytewise")
add([('X','B',1,9,0,0),('A','B',2,4000,10,10000),('A','B',3,5,10,12000),('A','B',4,6,10,9999)],"h.best_bid()",lambda r:r.bb())
add(base,"g_allocs",lambda r:0,"alloc")
add([('A','B',1,1,100,10000),('A','B',2,1,70,10003)],"h.bid_qty(10003)",lambda r:r.bq(10003))
for t in tests: print(t['call'],"->",t['expect'])
P_H=dict(id="handler",name="l18-feed-handler: a book with no allocation",prelude=PRE,
 starter='''#include <map>
#include <vector>

// Frames are 24 bytes (the l14 layout, big-endian). One instrument, prices 9900..10100 pence, order ids below 1024.
// 'A' adds an order (side B or S, price, qty), 'X' cancels the rest of order id, 'T' trades qty against order id.
// A frame with seq < the next expected is stale: ignore it. A larger seq adds (seq - expected) to gaps().
// Partial frames wait for their remaining bytes. After construction, feed() may not use the heap.
class Handler {
public:
    void feed(const std::vector<int>& bytes) {
        for (std::size_t at = 0; at + 24 <= bytes.size(); at += 24) {
            int type = bytes[at];
            unsigned id = (bytes[at + 8] << 24) | (bytes[at + 9] << 16) | (bytes[at + 10] << 8) | bytes[at + 11];
            unsigned qty = (bytes[at + 12] << 24) | (bytes[at + 13] << 16) | (bytes[at + 14] << 8) | bytes[at + 15];
            int price = (bytes[at + 16] << 24) | (bytes[at + 17] << 16) | (bytes[at + 18] << 8) | bytes[at + 19];
            bool bid = bytes[at + 1] == 'B';
            if (type == 'A') { (bid ? bids_ : asks_)[price] += qty; ++applied_; }
        }
    }
    int best_bid() const { return bids_.empty() ? 0 : bids_.rbegin()->first; }
    int best_ask() const { return asks_.empty() ? 0 : asks_.begin()->first; }
    int bid_qty(int price) const { auto it = bids_.find(price); return it == bids_.end() ? 0 : static_cast<int>(it->second); }
    int ask_qty(int price) const { auto it = asks_.find(price); return it == asks_.end() ? 0 : static_cast<int>(it->second); }
    int gaps() const { return 0; }
    int applied() const { return applied_; }
private:
    std::map<int, unsigned> bids_, asks_;
    int applied_ = 0;
};
''',
 solution='''#include <array>
#include <cstdint>
#include <vector>

class Handler {
public:
    void feed(const std::vector<int>& bytes) {
        for (int b : bytes) {
            pending_[pending_len_++] = static_cast<std::uint8_t>(b);
            if (pending_len_ == kFrame) { frame(); pending_len_ = 0; }
        }
    }
    int best_bid() const {
        for (int i = kLevels - 1; i >= 0; --i) if (qty_[0][i] > 0) return kMinPrice + i;
        return 0;
    }
    int best_ask() const {
        for (int i = 0; i < kLevels; ++i) if (qty_[1][i] > 0) return kMinPrice + i;
        return 0;
    }
    int bid_qty(int price) const { return level(0, price); }
    int ask_qty(int price) const { return level(1, price); }
    int gaps() const { return gaps_; }
    int applied() const { return applied_; }
private:
    static constexpr int kFrame = 24, kMinPrice = 9900, kLevels = 201, kOrders = 1024;
    struct Order { int side = 0; int price = 0; unsigned qty = 0; bool live = false; };

    unsigned u32(int at) const {
        return (unsigned(pending_[at]) << 24) | (unsigned(pending_[at + 1]) << 16) | (unsigned(pending_[at + 2]) << 8) | unsigned(pending_[at + 3]);
    }
    int level(int side, int price) const {
        int i = price - kMinPrice;
        return (i >= 0 && i < kLevels) ? static_cast<int>(qty_[side][i]) : 0;
    }
    void frame() {
        unsigned seq = u32(4);
        if (seq < expected_) return;                 // stale or duplicate
        if (seq > expected_) gaps_ += static_cast<int>(seq - expected_);
        expected_ = seq + 1;
        ++applied_;
        int type = pending_[0];
        int side = pending_[1] == 'B' ? 0 : (pending_[1] == 'S' ? 1 : -1);
        unsigned id = u32(8), qty = u32(12);
        int price = static_cast<int>(u32(16));
        if (id >= kOrders) return;
        Order& o = orders_[id];
        if (type == 'A') {
            int i = price - kMinPrice;
            if (side < 0 || i < 0 || i >= kLevels || o.live) return;
            o = Order{side, price, qty, true};
            qty_[side][i] += qty;
        } else if (type == 'X') {
            if (!o.live) return;
            qty_[o.side][o.price - kMinPrice] -= o.qty;
            o.live = false;
        } else if (type == 'T') {
            if (!o.live) return;
            unsigned done = qty < o.qty ? qty : o.qty;
            o.qty -= done;
            qty_[o.side][o.price - kMinPrice] -= done;
            if (o.qty == 0) o.live = false;
        }
    }

    std::array<std::array<unsigned, kLevels>, 2> qty_{};
    std::array<Order, kOrders> orders_{};
    std::array<std::uint8_t, kFrame> pending_{};
    int pending_len_ = 0;
    unsigned expected_ = 1;
    int gaps_ = 0, applied_ = 0;
};
''',
 tests=tests)
if __name__=="__main__":
    ok=run(P_H); print("ALL OK" if ok else "PROBLEM")
    # fuzz: random streams, random chunking: C++ solution vs Ref
    import subprocess, os, tempfile
    harness='''#include <cstdio>
#include <string>
#include <iostream>
'''
    src=harness+PRE+P_H["solution"]+'''
int main(){ std::string line; while(std::getline(std::cin,line)){ Handler h; std::vector<int> all; for(size_t i=0;i+1<line.size();i+=2) all.push_back(std::stoi(line.substr(i,2),nullptr,16));
  size_t at=0; unsigned k=7; while(at<all.size()){ size_t n=1+(k=k*1103515245u+12345u)%40; if(at+n>all.size()) n=all.size()-at; h.feed(std::vector<int>(all.begin()+at,all.begin()+at+n)); at+=n; }
  std::printf("%d %d %d %d\\n",h.best_bid(),h.best_ask(),h.gaps(),h.applied()); } }
'''
    d="build/fuzz"; os.makedirs(d,exist_ok=True); open(d+"/f.cpp","w").write(src)
    subprocess.run(["g++","-std=c++17","-O1","-fsanitize=address,undefined",d+"/f.cpp","-o",d+"/f"],check=True)
    rnd=random.Random(5); lines=[]; exp=[]
    for _ in range(400):
        n=rnd.randint(1,60); seqs=list(range(1,n+1))
        seqs=[s for s in seqs if rnd.random()>0.1]
        for i in range(len(seqs)-1):
            if rnd.random()<0.1: seqs[i],seqs[i+1]=seqs[i+1],seqs[i]
        if seqs and rnd.random()<0.3: seqs.insert(rnd.randrange(len(seqs)),rnd.choice(seqs))
        frs=[]
        for s in seqs:
            t=rnd.choice('AAAXT'); sd=rnd.choice('BS'); oid=rnd.randint(1,12) if rnd.random()<0.97 else 2000
            px=rnd.randint(9995,10010) if rnd.random()<0.95 else rnd.choice([9899,10101,0])
            frs.append(fr(t,sd,s,oid,rnd.randint(1,50),px))
        bs=stream(frs); lines.append(bytes(bs).hex())
        r=Ref(); r.feed(bs); exp.append(f"{r.bb()} {r.ba()} {r.gaps} {r.applied}")
    out=subprocess.run([d+"/f"],input="\n".join(lines)+"\n",capture_output=True,text=True)
    got=out.stdout.strip().split("\n"); bad=[i for i,(a,b) in enumerate(zip(got,exp)) if a!=b]
    print("fuzz: streams",len(lines),"mismatches",len(bad),"stderr",out.stderr[:200])
