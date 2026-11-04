import sys, struct; sys.path.insert(0,'.')
from harness import run
# ---- find_gaps: reference by set difference
def gaps(seqs):
    return sorted(set(range(1,max(seqs)+1))-set(seqs)) if seqs else []
def il(l): return "{"+", ".join(map(str,l))+"}"
cases=[[1,2,3],[1,2,4,5],[1,3,2],[2,3],[1,5],[1,2,2,4,4],[],[3,1,2,6,5],[1,2,3,7,8,10],[5,4,3,2,1],[1]]
P_GAP=dict(id="find_gaps",name="l13-tcp-and-udp: find the missing sequence numbers",
 starter='''#include <vector>

// A UDP feed numbers its messages 1, 2, 3, ... Messages may arrive late or twice.
// Given the sequence numbers in arrival order, return every number from 1 up to the largest seen
// that has not arrived, smallest first.
std::vector<int> find_gaps(const std::vector<int>& seqs) {
    std::vector<int> missing;
    int expected = 1;
    for (int s : seqs) {
        while (expected < s) missing.push_back(expected++);   // a jump means a gap
        if (s == expected) ++expected;
    }
    return missing;
}
''',
 solution='''#include <algorithm>
#include <vector>

std::vector<int> find_gaps(const std::vector<int>& seqs) {
    if (seqs.empty()) return {};
    int largest = *std::max_element(seqs.begin(), seqs.end());
    std::vector<bool> seen(largest + 1, false);
    for (int s : seqs) seen[s] = true;
    std::vector<int> missing;
    for (int n = 1; n <= largest; ++n)
        if (!seen[n]) missing.push_back(n);
    return missing;
}
''',
 tests=[dict(call=f"find_gaps({il(c)})",expect=gaps(c)) for c in cases])
# ---- encode / decode, big-endian, 24 bytes
def enc_A(t,s,i,q,idn,qty,px,tm): return list(struct.pack('>BBHIIIiI',t,s,i,q,idn,qty,px,tm))
def be(v,n): return [(v>>(8*(n-1-k)))&0xFF for k in range(n)]
def enc_B(t,s,i,q,idn,qty,px,tm): return [t,s]+be(i,2)+be(q,4)+be(idn,4)+be(qty,4)+be(px&0xFFFFFFFF,4)+be(tm,4)
msgs=[(65,66,258,70000,123456789,100,10275,36000000),(88,83,1,1,2,0,-25,0),(84,66,65535,4294967295,4294967295,4294967295,2147483647,86399999),(65,83,0,0,0,1,-2147483648,1)]
for m in msgs: assert enc_A(*m)==enc_B(*m)
PRE='''struct Msg {
    int type;            // 'A' add, 'X' cancel, 'T' trade
    int side;            // 'B' or 'S'
    int instrument;      // 0..65535
    unsigned seq;
    unsigned id;
    unsigned qty;
    int price;           // pence, may be negative
    unsigned time;       // milliseconds since midnight
};
'''
def mlit(m): return "Msg m{%d, %d, %d, %uu, %uu, %uu, %d, %uu};"%m if m[6]>=-2147483647 else "Msg m{%d, %d, %d, %uu, %uu, %uu, (-2147483647 - 1), %uu};"%(m[0],m[1],m[2],m[3],m[4],m[5],m[7])
tests=[]
for k,m in enumerate(msgs):
    tests.append(dict(setup=mlit(m),call="encode(m)",expect=enc_A(*m)))
for k,m in enumerate(msgs):
    for f,idx in (("type",0),("instrument",2),("seq",3),("price",6)):
        pass
tests.append(dict(setup="", call="decode(std::vector<int>"+il(enc_A(*msgs[0]))+").instrument",expect=258))
tests.append(dict(setup="", call="decode(std::vector<int>"+il(enc_A(*msgs[0]))+").price",expect=10275))
tests.append(dict(setup="", call="decode(std::vector<int>"+il(enc_A(*msgs[1]))+").price",expect=-25))
tests.append(dict(setup="", call="(long long)decode(std::vector<int>"+il(enc_A(*msgs[2]))+").seq",expect=4294967295))
tests.append(dict(setup="", call="(long long)decode(std::vector<int>"+il(enc_A(*msgs[2]))+").time",expect=86399999))
tests.append(dict(setup="", call="decode(std::vector<int>"+il(enc_A(*msgs[3]))+").price",expect=-2147483648))
tests.append(dict(setup=mlit(msgs[0])+" Msg d = decode(encode(m));", call="(long long)d.id",expect=123456789))
tests.append(dict(setup=mlit(msgs[2])+" Msg d = decode(encode(m));", call="(long long)d.qty",expect=4294967295))
P_WIRE=dict(id="encode_decode",name="l14-messages-on-the-wire: encode and decode",
 prelude=PRE,
 starter='''#include <vector>

// Wire layout, 24 bytes, big-endian (most significant byte first):
//   0 type (1)   1 side (1)   2 instrument (2)   4 seq (4)
//   8 id (4)    12 qty (4)   16 price (4, signed)  20 time (4)
std::vector<int> encode(const Msg& m) {
    std::vector<int> out(24, 0);
    out[0] = m.type;
    out[1] = m.side;
    // TODO: the other fields, most significant byte first
    return out;
}

Msg decode(const std::vector<int>& b) {
    Msg m{};
    m.type = b[0];
    m.side = b[1];
    // TODO: the other fields
    return m;
}
''',
 solution='''#include <vector>

namespace {
void put(std::vector<int>& out, int at, unsigned v, int bytes) {
    for (int k = 0; k < bytes; ++k)
        out[at + k] = (v >> (8 * (bytes - 1 - k))) & 0xFF;
}
unsigned get(const std::vector<int>& b, int at, int bytes) {
    unsigned v = 0;
    for (int k = 0; k < bytes; ++k) v = (v << 8) | static_cast<unsigned>(b[at + k] & 0xFF);
    return v;
}
}

std::vector<int> encode(const Msg& m) {
    std::vector<int> out(24, 0);
    out[0] = m.type;
    out[1] = m.side;
    put(out, 2, static_cast<unsigned>(m.instrument), 2);
    put(out, 4, m.seq, 4);
    put(out, 8, m.id, 4);
    put(out, 12, m.qty, 4);
    put(out, 16, static_cast<unsigned>(m.price), 4);
    put(out, 20, m.time, 4);
    return out;
}

Msg decode(const std::vector<int>& b) {
    Msg m{};
    m.type = b[0];
    m.side = b[1];
    m.instrument = static_cast<int>(get(b, 2, 2));
    m.seq = get(b, 4, 4);
    m.id = get(b, 8, 4);
    m.qty = get(b, 12, 4);
    m.price = static_cast<int>(get(b, 16, 4));
    m.time = get(b, 20, 4);
    return m;
}
''',
 tests=tests)
if __name__=="__main__":
    for P in (P_GAP,P_WIRE):
        print(P['name']); [print("  ",(t.get('setup','')+' '+t['call'])[:110],"->",str(t['expect'])[:80]) for t in P['tests']]
        print("ALL OK" if run(P) else "PROBLEM")
    print("hex of msg0:", bytes(enc_A(*msgs[0])).hex(), " groups:", bytes(enc_A(*msgs[0])).hex(' '))
    print("hex of msg1:", bytes(enc_A(*msgs[1])).hex(' '))
