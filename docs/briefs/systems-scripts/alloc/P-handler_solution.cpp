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

#include <array>
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
