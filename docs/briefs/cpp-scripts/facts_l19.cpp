// Copy and move counts for l19, the numbers behind its console screens. Run with g++ and clang++ (same output).
// Build: clang++ -std=c++17 -O1 -fno-exceptions facts_l19.cpp -o facts_l19 && ./facts_l19
#include <cstdio>
#include <utility>
#include <vector>

struct Tracked {
    static inline int copies = 0, moves = 0;
    int v;
    Tracked(int x) : v(x) {}
    Tracked(const Tracked& o) : v(o.v) { ++copies; }
    Tracked(Tracked&& o) noexcept : v(o.v) { ++moves; o.v = -1; }
};
struct SlowMove {                       // move constructor not noexcept
    static inline int copies = 0, moves = 0;
    int v;
    SlowMove(int x) : v(x) {}
    SlowMove(const SlowMove& o) : v(o.v) { ++copies; }
    SlowMove(SlowMove&& o) : v(o.v) { ++moves; o.v = -1; }
};

Tracked make() { return Tracked(1); }
Tracked make_named() { Tracked t(1); return t; }
Tracked make_moved() { Tracked t(1); return std::move(t); }
void take(Tracked t) { (void)t; }

template <class F> void run(const char* name, F f) {
    Tracked::copies = Tracked::moves = 0;
    SlowMove::copies = SlowMove::moves = 0;
    f();
    if (SlowMove::copies + SlowMove::moves > 0)
        std::printf("%-44s copies=%d moves=%d\n", name, SlowMove::copies, SlowMove::moves);
    else
        std::printf("%-44s copies=%d moves=%d\n", name, Tracked::copies, Tracked::moves);
}

int main() {
    run("Tracked b = a;", [] { Tracked a(1); Tracked b = a; (void)b; });
    run("Tracked b = std::move(a);", [] { Tracked a(1); Tracked b = std::move(a); (void)b; });
    run("std::move(a); (alone)", [] { Tracked a(1); std::move(a); });
    run("Tracked b = make();", [] { Tracked b = make(); (void)b; });
    run("Tracked b = make_named();", [] { Tracked b = make_named(); (void)b; });
    run("Tracked b = make_moved();", [] { Tracked b = make_moved(); (void)b; });
    run("const Tracked c; Tracked d = std::move(c);", [] { const Tracked c(1); Tracked d = std::move(c); (void)d; });
    run("take(a);", [] { Tracked a(1); take(a); });
    run("take(std::move(a));", [] { Tracked a(1); take(std::move(a)); });
    run("take(Tracked(1));", [] { take(Tracked(1)); });
    run("v.push_back(t);", [] { std::vector<Tracked> v; v.reserve(1); Tracked t(1); v.push_back(t); });
    run("v.push_back(std::move(t));", [] { std::vector<Tracked> v; v.reserve(1); Tracked t(1); v.push_back(std::move(t)); });
    run("v.emplace_back(1);", [] { std::vector<Tracked> v; v.reserve(1); v.emplace_back(1); });
    run("two push_back(Tracked(i)), no reserve", [] { std::vector<Tracked> v; v.push_back(Tracked(1)); v.push_back(Tracked(2)); });
    run("same, move not noexcept", [] { std::vector<SlowMove> v; v.push_back(SlowMove(1)); v.push_back(SlowMove(2)); });
    run("four push_back(Tracked(i)), no reserve", [] { std::vector<Tracked> v; for (int i = 0; i < 4; ++i) v.push_back(Tracked(i)); });
}
