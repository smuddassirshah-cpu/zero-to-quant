#include "alloc_check.hpp"

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

#include <map>
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

int main(){ int fail=0;
  { Handler h; auto s = cat({frame('A', 'B', 1, 1, 100, 10000), frame('A', 'S', 2, 2, 50, 10010), frame('A', 'B', 3, 3, 40, 10005)}); h.feed(s);  auto __r = (h.best_bid()); auto __e = (10005); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 0\n"); } }
  { Handler h; auto s = cat({frame('A', 'B', 1, 1, 100, 10000), frame('A', 'S', 2, 2, 50, 10010), frame('A', 'B', 3, 3, 40, 10005)}); h.feed(s);  auto __r = (h.best_ask()); auto __e = (10010); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 1\n"); } }
  { Handler h; auto s = cat({frame('A', 'B', 1, 1, 100, 10000), frame('A', 'S', 2, 2, 50, 10010), frame('A', 'B', 3, 3, 40, 10005), frame('X', 'B', 4, 3, 0, 0)}); h.feed(s);  auto __r = (h.best_bid()); auto __e = (10000); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 2\n"); } }
  { Handler h; auto s = cat({frame('A', 'B', 1, 1, 100, 10000), frame('A', 'S', 2, 2, 50, 10010), frame('A', 'B', 3, 3, 40, 10005), frame('T', 'B', 4, 1, 30, 10000)}); h.feed(s);  auto __r = (h.bid_qty(10000)); auto __e = (70); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 3\n"); } }
  { Handler h; auto s = cat({frame('A', 'B', 1, 1, 100, 10000), frame('T', 'B', 2, 1, 100, 10000)}); h.feed(s);  auto __r = (h.best_bid()); auto __e = (0); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 4\n"); } }
  { Handler h; auto s = cat({frame('A', 'B', 1, 1, 10, 10000), frame('A', 'B', 2, 2, 10, 10001), frame('A', 'B', 5, 3, 10, 10002)}); h.feed(s);  auto __r = (h.gaps()); auto __e = (2); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 5\n"); } }
  { Handler h; auto s = cat({frame('A', 'B', 1, 1, 10, 10000), frame('A', 'B', 2, 2, 10, 10001), frame('A', 'B', 2, 3, 99, 10050)}); h.feed(s);  auto __r = (h.applied()); auto __e = (2); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 6\n"); } }
  { Handler h; auto s = cat({frame('A', 'B', 1, 1, 10, 10000), frame('A', 'B', 2, 2, 10, 10001), frame('A', 'B', 4, 3, 10, 10002), frame('A', 'B', 3, 4, 500, 10050)}); h.feed(s);  auto __r = (h.best_bid()); auto __e = (10002); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 7\n"); } }
  { Handler h; auto s = cat({frame('A', 'B', 3, 1, 10, 10000)}); h.feed(s);  auto __r = (h.gaps()); auto __e = (2); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 8\n"); } }
  { Handler h; auto s = cat({frame('A', 'B', 1, 1, 100, 10000), frame('A', 'S', 2, 2, 50, 10010), frame('A', 'B', 3, 3, 40, 10005)}); h.feed(std::vector<int>(s.begin(), s.begin() + 30)); h.feed(std::vector<int>(s.begin() + 30, s.end()));  auto __r = (h.best_bid()); auto __e = (10005); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 9\n"); } }
  { Handler h; auto s = cat({frame('A', 'B', 1, 1, 100, 10000), frame('A', 'S', 2, 2, 50, 10010), frame('A', 'B', 3, 3, 40, 10005), frame('T', 'S', 4, 2, 50, 10010)}); for (int b : s) h.feed(std::vector<int>{b});  auto __r = (h.best_ask()); auto __e = (0); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 10\n"); } }
  { Handler h; auto s = cat({frame('X', 'B', 1, 9, 0, 0), frame('A', 'B', 2, 4000, 10, 10000), frame('A', 'B', 3, 5, 10, 12000), frame('A', 'B', 4, 6, 10, 9999)}); h.feed(s);  auto __r = (h.best_bid()); auto __e = (9999); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 11\n"); } }
  { Handler h; auto s = cat({frame('A', 'B', 1, 1, 100, 10000), frame('A', 'S', 2, 2, 50, 10010), frame('A', 'B', 3, 3, 40, 10005)}); reset_alloc_count(); h.feed(s);  auto __r = (alloc_count()); auto __e = (0); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 12\n"); } }
  { Handler h; auto s = cat({frame('A', 'B', 1, 1, 100, 10000), frame('A', 'B', 2, 1, 70, 10003)}); h.feed(s);  auto __r = (h.bid_qty(10003)); auto __e = (0); bool ok = eqv(__r, __e); if(!ok){ fail++; std::printf("FAIL test 13\n"); } }
  std::printf("%d of %d failed\n", fail, 14); return fail?1:0; }
