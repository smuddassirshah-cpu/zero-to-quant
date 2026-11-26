// Claim programs: each is compiled and run with the page's flags (YoWASP clang 21, wasm32, -O1, libc++ hardening, no exceptions).
export const jobs = [];
const P = (name, prog, extra = {}) => jobs.push({ name, prog, ...extra });
const TR = (noex) => `
struct Tracked {
    static inline int copies = 0, moves = 0;
    int v;
    explicit Tracked(int x) : v(x) {}
    Tracked(const Tracked& o) : v(o.v) { ++copies; }
    Tracked(Tracked&& o) ${noex ? 'noexcept ' : ''}: v(o.v) { ++moves; o.v = -1; }
    Tracked& operator=(const Tracked& o) { v = o.v; ++copies; return *this; }
    Tracked& operator=(Tracked&& o) ${noex ? 'noexcept ' : ''}{ v = o.v; ++moves; return *this; }
    static void show(const char* w) { std::printf("%s copies=%d moves=%d\\n", w, copies, moves); copies = moves = 0; }
};`;

P('sizes', `#include <cstdio>
#include <memory>
#include <string>
#include <vector>
struct Tick { int px; };
struct VTick { int px; virtual int level() const; };
struct B { int x; virtual void f(); };
struct D : B { int y; void f() override; };
struct Quote { virtual double mid() const; double bid, ask; };
struct W { virtual void f(); int n; };
struct S { virtual void f(); char c; };
struct B2 { virtual void f(); double x; };
struct Buffer { int size_; double* data_; };
int main() {
    std::printf("Tick=%zu VTick=%zu B=%zu D=%zu Quote=%zu W=%zu S=%zu B2=%zu\\n", sizeof(Tick), sizeof(VTick), sizeof(B), sizeof(D), sizeof(Quote), sizeof(W), sizeof(S), sizeof(B2));
    std::printf("ptr=%zu int=%zu long=%zu size_t=%zu double_align=%zu Buffer=%zu\\n", sizeof(void*), sizeof(int), sizeof(long), sizeof(std::size_t), alignof(double), sizeof(Buffer));
    std::printf("unique=%zu shared=%zu\\n", sizeof(std::unique_ptr<int>), sizeof(std::shared_ptr<int>));
    std::printf("size_max=%zu\\n", static_cast<std::size_t>(0) - 1);
    std::printf("charsigned=%d m7=%d shl=%u\\n", static_cast<int>(static_cast<char>(-1) < 0), -7 / 2, 1u << 31);
}
`);

P('growth', `#include <cstdio>
#include <vector>
int main() {
    std::vector<double> v;
    std::printf("caps:");
    for (int i = 0; i < 9; ++i) { v.push_back(i); std::printf(" %zu", v.capacity()); }
    std::printf("\\n");
    std::vector<double> t; int moves = 0; long copied = 0; int allocs = 0;
    for (int i = 0; i < 600; ++i) { std::size_t c = t.capacity(), n = t.size(); t.push_back(100.0 + i * 0.01); if (t.capacity() != c) { ++allocs; if (n > 0) { ++moves; copied += n; } } }
    std::printf("600 pushes: allocations=%d moves=%d copied=%ld cap=%zu\\n", allocs, moves, copied, t.capacity());
    std::vector<double> r; r.reserve(1000); std::size_t c0 = r.capacity(); const double* d0 = r.data(); int mv = 0;
    for (int i = 0; i < 600; ++i) { r.push_back(i); if (r.data() != d0) ++mv; }
    std::printf("reserve(1000): cap=%zu size_after_reserve=0 moves=%d\\n", c0, mv);
    std::vector<double> h; h.reserve(100); for (int i = 0; i < 150; ++i) h.push_back(i); std::printf("reserve(100)+150: cap=%zu\\n", h.capacity());
    std::vector<double> e; e.reserve(5); std::printf("reserve(5): cap=%zu\\n", e.capacity());
    std::vector<double> z(3); z.push_back(101.5); std::printf("v(3)+push: size=%zu z0=%g\\n", z.size(), z[0]);
    std::vector<double> five; for (int i = 0; i < 5; ++i) five.push_back(100.0 + i); std::printf("five: cap=%zu\\n", five.capacity());
}
`);

P('erase-loop', `#include <cstdio>
#include <vector>
int main() {
    std::vector<double> ticks{101.2, 0.0, 0.0, 101.5};
    for (auto it = ticks.begin(); it != ticks.end(); ++it) {
        if (*it == 0.0) {
            ticks.erase(it);
        }
    }
    for (double x : ticks) std::printf("%g ", x);
    std::printf("\\n");
}
`);

P('transform-empty', `#include <algorithm>
#include <cstdio>
#include <vector>
int main() {
    std::vector<double> px{100.0, 102.0, 99.0};
    std::vector<double> pence;
    std::transform(px.begin(), px.end(), pence.begin(), [](double p) { return p * 100; });
    std::printf("size=%zu done\\n", pence.size());
}
`);

P('max-element-empty', `#include <algorithm>
#include <iostream>
#include <vector>
int main(int argc, char**) {
    std::vector<double> pnl;
    if (argc > 3) pnl.push_back(1.0);
    std::cout << "before" << std::endl;
    std::cout << *std::max_element(pnl.begin(), pnl.end()) << '\\n';
    std::cout << "after\\n";
}
`);

P('sort-le-3', `#include <algorithm>
#include <cstdio>
#include <vector>
int main() {
    std::vector<double> px{100.5, 100.5, 99.8};
    std::sort(px.begin(), px.end(), [](double a, double b) { return a <= b; });
    for (double x : px) std::printf("%g ", x);
    std::printf("\\n");
}
`);
for (const n of [8, 31, 40, 200, 2000]) P('sort-le-equal-' + n, `#include <algorithm>
#include <cstdio>
#include <vector>
int main() {
    std::vector<double> px(${n}, 100.5);
    std::sort(px.begin(), px.end(), [](double a, double b) { return a <= b; });
    std::printf("sorted %zu\\n", px.size());
}
`);

P('null-read-constant', `#include <cstdio>
int main() {
    int* p = nullptr;
    int v = *p;
    std::printf("v=%d\\n", v);
}
`);
P('null-read-unknown', `#include <cstdio>
#include <cstdlib>
int main(int argc, char** argv) {
    static int x = 7;
    int* p = argc > 5 ? &x : nullptr;
    std::printf("before\\n");
    int v = *p;
    std::printf("v=%d\\n", v);
}
`);
P('null-read-volatile', `#include <cstdio>
int* volatile gp = nullptr;
int main() {
    int* p = gp;
    int v = *p;
    std::printf("v=%d\\n", v);
}
`);

P('moves-l19', `#include <cstdio>
#include <utility>
#include <vector>
${TR(true)}
Tracked make() { return Tracked(1); }
Tracked make_named() { Tracked t(1); return t; }
Tracked make_moved() { Tracked t(1); return std::move(t); }
void take(Tracked) {}
int main() {
    std::vector<Tracked> v; v.reserve(8);
    Tracked a(1);                 Tracked::show("l1");
    Tracked b = a;                Tracked::show("l2");
    Tracked c = std::move(a);     Tracked::show("l3");
    Tracked d = make();           Tracked::show("l4");
    take(b);                      Tracked::show("l5");
    take(std::move(b));           Tracked::show("l6");
    take(Tracked(2));             Tracked::show("l7");
    v.push_back(c);               Tracked::show("l8");
    Tracked e(1);
    std::move(e);                 Tracked::show("cast-only");
    Tracked f = std::move(e);     Tracked::show("cast+ctor");
    { std::vector<Tracked> w; for (int i = 0; i < 4; ++i) w.push_back(Tracked(i)); }
    Tracked::show("four pushes noexcept");
    Tracked g = make_named();     Tracked::show("return t");
    Tracked h = make_moved();     Tracked::show("return std::move(t)");
    const Tracked k(9);
    take(k); take(std::move(k)); take(Tracked(3)); Tracked::show("r5 three calls const k");
    Tracked m(1);
    take(m); take(std::move(m)); take(Tracked(3)); Tracked::show("quiz three calls");
    (void)d; (void)f; (void)g; (void)h;
}
`);
P('moves-throwing', `#include <cstdio>
#include <utility>
#include <vector>
${TR(false)}
struct MoveOnly { static inline int moves = 0; MoveOnly() = default; MoveOnly(MoveOnly&&) { ++moves; } MoveOnly(const MoveOnly&) = delete; };
int main() {
    { std::vector<Tracked> w; for (int i = 0; i < 2; ++i) w.push_back(Tracked(i)); }
    Tracked::show("two pushes, move may throw");
    { std::vector<Tracked> w; for (int i = 0; i < 2; ++i) w.emplace_back(i); }
    Tracked::show("two emplace_back, move may throw");
    { std::vector<MoveOnly> w; for (int i = 0; i < 4; ++i) w.push_back(MoveOnly()); }
    std::printf("move-only, move may throw: moves=%d\\n", MoveOnly::moves);
}
`);

P('special-members', `#include <cstdio>
#include <memory>
#include <string>
#include <type_traits>
#include <utility>
#include <vector>
struct Probe { static inline int c = 0, m = 0; Probe() = default; Probe(const Probe&) { ++c; } Probe(Probe&&) noexcept { ++m; } Probe& operator=(const Probe&) { ++c; return *this; } Probe& operator=(Probe&&) noexcept { ++m; return *this; } };
struct N { Probe p; };
struct Dt { Probe p; ~Dt() {} };
struct Cc { Probe p; Cc() = default; Cc(const Cc& o) : p(o.p) {} };
struct Ca { Probe p; Ca& operator=(const Ca& o) { p = o.p; return *this; } };
struct Mc { Probe p; Mc() = default; Mc(Mc&& o) : p(std::move(o.p)) {} };
struct Ma { Probe p; Ma& operator=(Ma&& o) { p = std::move(o.p); return *this; } };
struct A5 { Probe p; A5() = default; ~A5() = default; A5(const A5&) = default; A5& operator=(const A5&) = default; A5(A5&&) = default; A5& operator=(A5&&) = default; };
const char* what() { const char* r = Probe::c ? "copy" : Probe::m ? "move" : "none"; Probe::c = Probe::m = 0; return r; }
template <class T> void row(const char* name) {
    std::printf("%-12s", name);
    T a;
    if constexpr (std::is_constructible_v<T, const T&>) { T b(a); std::printf(" %-5s", what()); } else std::printf(" error");
    if constexpr (std::is_constructible_v<T, T&&>) { T b(std::move(a)); std::printf(" %-5s", what()); } else std::printf(" error");
    T x, y;
    if constexpr (std::is_assignable_v<T&, const T&>) { x = y; std::printf(" %-5s", what()); } else std::printf(" error");
    if constexpr (std::is_assignable_v<T&, T&&>) { x = std::move(y); std::printf(" %-5s", what()); } else std::printf(" error");
    std::printf("\\n");
}
struct Fill {};
struct Pos { std::string sym; std::vector<int> lots; Pos(Pos&&) = default; Pos(const Pos&) = default; };
struct Pos3 { std::string sym; std::vector<int> lots; Pos3(Pos3&& o) : sym(std::move(o.sym)), lots(std::move(o.lots)) {} Pos3(const Pos3&) = default; };
struct Order { std::unique_ptr<Fill> fill; ~Order() {} };
struct Holder { std::unique_ptr<Fill> fill; };
int main() {
    row<N>("nothing"); row<Dt>("destructor"); row<Cc>("copy ctor"); row<Ca>("copy assign"); row<Mc>("move ctor"); row<Ma>("move assign"); row<A5>("all five");
    std::printf("Pos nothrow move=%d Pos3 nothrow move=%d Pos copyable=%d\\n", std::is_nothrow_move_constructible_v<Pos>, std::is_nothrow_move_constructible_v<Pos3>, std::is_copy_constructible_v<Pos>);
    std::printf("string nothrow move=%d vector nothrow move=%d\\n", std::is_nothrow_move_constructible_v<std::string>, std::is_nothrow_move_constructible_v<std::vector<int>>);
    std::printf("Order: default=%d moveinit=%d copyinit=%d moveassign=%d\\n", std::is_default_constructible_v<Order>, std::is_constructible_v<Order, Order&&>, std::is_copy_constructible_v<Order>, std::is_assignable_v<Order&, Order&&>);
    std::printf("Holder: copy=%d move=%d\\n", std::is_copy_constructible_v<Holder>, std::is_move_constructible_v<Holder>);
}
`);

P('numbers', `#include <algorithm>
#include <cmath>
#include <cstdio>
#include <map>
#include <memory>
#include <numeric>
#include <vector>
double norm_cdf(double x) { return 0.5 * std::erfc(-x / std::sqrt(2.0)); }
double bs(double S, double K, double r, double s, double T) { double d1 = (std::log(S / K) + (r + 0.5 * s * s) * T) / (s * std::sqrt(T)); double d2 = d1 - s * std::sqrt(T); return S * norm_cdf(d1) - K * std::exp(-r * T) * norm_cdf(d2); }
double bin(double S, double K, double r, double sigma, double T, int n) {
    double dt = T / n; double u = std::exp(sigma * std::sqrt(dt)), d = 1 / u; double disc = std::exp(-r * dt); double p = (std::exp(r * dt) - d) / (u - d);
    std::vector<double> val(n + 1);
    for (int j = 0; j <= n; ++j) val[j] = std::max(S * std::pow(u, n - j) * std::pow(d, j) - K, 0.0);
    for (int i = n - 1; i >= 0; --i) for (int j = 0; j <= i; ++j) val[j] = disc * (p * val[j] + (1 - p) * val[j + 1]);
    return val[0];
}
struct T { int v; explicit T(int x) : v(x) {} };
int main() {
    std::map<double, int> bids; double best = 100.1; bids[best] += 500; bids[best + 0.1] += 300; bids[100.2] += 200;
    std::printf("bids=%zu sum=%.17g\\n", bids.size(), best + 0.1);
    std::vector<double> px{100.0, 110.0};
    std::printf("ratio-1=%.17g eq=%d diff/prev=%.17g eq=%d\\n", px[1] / px[0] - 1, px[1] / px[0] - 1 == 0.1, (px[1] - px[0]) / px[0], (px[1] - px[0]) / px[0] == 0.1);
    std::printf("vwap=%.17g eq=%d\\n", (10.1 * 1 + 10.2 * 1) / (1 + 1), (10.1 * 1 + 10.2 * 1) / (1.0 + 1.0) == 10.15);
    std::vector<double> pnl{120.5, -40.25, 75.0, -10.5, 30.25};
    auto ti = std::accumulate(pnl.begin(), pnl.end(), 0); double td = std::accumulate(pnl.begin(), pnl.end(), 0.0);
    std::printf("acc int=%d double=%g\\n", ti, td);
    std::vector<double> fees{2.5, 2.5, 2.5, 2.5}; std::printf("fees int=%d\\n", std::accumulate(fees.begin(), fees.end(), 0));
    std::vector<double> rets{0.01, -0.03, 0.025, -0.005, 0.04}; double limit = 0.02; auto big = [limit](double r) { return std::abs(r) > limit; }; limit = 0.05;
    std::printf("count=%d\\n", (int)std::count_if(rets.begin(), rets.end(), big));
    std::printf("bs=%.9f bin100=%.9f bin99=%.9f bin2000=%.9f bin1999=%.9f\\n", bs(100, 100, 0.05, 0.2, 1), bin(100, 100, 0.05, 0.2, 1, 100), bin(100, 100, 0.05, 0.2, 1, 99), bin(100, 100, 0.05, 0.2, 1, 2000), bin(100, 100, 0.05, 0.2, 1, 1999));
    auto a = std::make_shared<T>(1); std::weak_ptr<T> w = a; auto b = a; std::printf("use=%ld\\n", a.use_count());
    auto c = std::move(b); std::printf("use after move=%ld b=%ld\\n", a.use_count(), b.use_count());
    std::vector<double> d(5); std::vector<double> in{100, 104, 101, 106, 103}; std::adjacent_difference(in.begin(), in.end(), d.begin());
    std::printf("adj: %g %g %g %g %g\\n", d[0], d[1], d[2], d[3], d[4]);
}
`);

P('ctor-virtual-and-slice', `#include <algorithm>
#include <cstdio>
#include <string>
struct Base { std::string who; Base() { who = name(); } virtual std::string name() const { return "Base"; } virtual ~Base() = default; };
struct Derived : Base { std::string name() const override { return "Derived"; } };
struct Payoff { virtual double value(double) const { return -1; } virtual ~Payoff() = default; };
struct Call : Payoff { double k; explicit Call(double s) : k(s) {} double value(double s) const override { return std::max(s - k, 0.0); } };
int main() {
    Derived d; std::printf("who=%s later=%s\\n", d.who.c_str(), d.name().c_str());
    Call c(100); Payoff q = c; const Payoff& r = c; std::printf("slice=%g ref=%g\\n", q.value(110), r.value(110));
}
`);
jobs.push({ name: 'l21-s9-listing', cc: ['-std=c++17', '-fsyntax-only', 'f.cpp'], files: { 'f.cpp': `#include <memory>
struct Payoff {
    virtual ~Payoff() = default;
    virtual double value(double) const = 0;
};
struct Call : Payoff {
    double value(double) const override;
};
std::unique_ptr<Payoff> p =
    std::make_unique<Call>(100);
` }, diag: 700 });
P('length-error', `#include <vector>
int main() {
    std::vector<double> px;
    std::vector<double> out(px.size() - 1);
    return (int)out.size();
}
`);
P('reserve-huge', `#include <vector>
int main() {
    std::vector<double> px, out;
    out.reserve(px.size() - 1);
    return 0;
}
`);
P('const-map-index', `#include <map>
#include <string>
double last_price(const std::map<std::string, double>& px, const std::string& sym) {
    return px[sym];
}
int main() { return 0; }
`, { diag: 300 });
P('unordered-order', `#include <cstdio>
#include <string>
#include <unordered_map>
int main() {
    std::unordered_map<std::string, int> m; m["VOD"]; m["BARC"]; m["AZN"];
    for (const auto& [k, v] : m) std::printf("%s ", k.c_str());
    std::printf("| ");
    std::unordered_map<std::string, int> n; n["AZN"]; n["BP"]; n["SHEL"];
    for (const auto& [k, v] : n) std::printf("%s ", k.c_str());
    std::printf("\\n");
}
`);

jobs.push({ name: 'first-asm', asm: `int first(int* p) {
    int v = *p;
    if (p == nullptr) return -1;
    return v;
}
int second(int* p) {
    if (p == nullptr) return -1;
    return *p;
}
` });
P('max-element-empty-plain', `#include <algorithm>
#include <iostream>
#include <vector>
int main() {
    std::vector<double> pnl;
    std::cout << *std::max_element(pnl.begin(), pnl.end()) << '\\n';
}
`);
P('max-element-empty-auto', `#include <algorithm>
#include <iostream>
#include <vector>
int main() {
    std::vector<double> pnl;
    auto it = std::max_element(pnl.begin(), pnl.end());
    std::cout << "max " << *it << '\\n';
    std::cout << "after\\n";
}
`);
P('max-element-empty-printf', `#include <algorithm>
#include <cstdio>
#include <vector>
int main() {
    std::vector<double> pnl;
    std::printf("%g\\n", *std::max_element(pnl.begin(), pnl.end()));
}
`);
P('find-if-empty', `#include <algorithm>
#include <iostream>
#include <vector>
int main() {
    std::vector<double> pnl;
    std::cout << *std::find_if(pnl.begin(), pnl.end(), [](double x) { return x > 0; }) << '\\n';
}
`);
P('erase-last', `#include <cstdio>
#include <vector>
int main() {
    std::vector<double> ticks{101.2, 101.5, 0.0};
    int steps = 0;
    for (auto it = ticks.begin(); it != ticks.end() && steps < 50; ++it, ++steps) {
        if (*it == 0.0) {
            ticks.erase(it);
        }
    }
    std::printf("steps=%d size=%zu\\n", steps, ticks.size());
}
`);
P('count-if-begin-plus-1-empty', `#include <algorithm>
#include <cstdio>
#include <vector>
int main() {
    std::vector<double> d;
    std::printf("start\\n");
    long n = std::count_if(d.begin() + 1, d.end(), [](double x) { return x > 0; });
    std::printf("n=%ld\\n", n);
}
`);
P('vector-move-source', `#include <cstdio>
#include <vector>
int main() {
    std::vector<int> v{1, 2, 3};
    std::vector<int> w = std::move(v);
    std::printf("v.size=%zu w.size=%zu\\n", v.size(), w.size());
}
`);
P('seven-over-two', `#include <climits>
#include <cstdio>
int main() { unsigned u = 0; --u; std::printf("%u %d %ld\\n", u, 7 / 2, 2500000000LL - INT_MAX == 352516353LL ? 1L : 0L); }
`);
jobs.push({ name: 'l21-s9-listing-fixed', cc: ['-std=c++17', '-fsyntax-only', 'f.cpp'], files: { 'f.cpp': `#include <memory>
struct Payoff {
    virtual ~Payoff() = default;
    virtual double value(double) const = 0;
};
struct Call : Payoff {
    explicit Call(double k) : strike(k) {}
    double value(double) const override;
    double strike;
};
std::unique_ptr<Payoff> p =
    std::make_unique<Call>(100);
` }, diag: 700 });
