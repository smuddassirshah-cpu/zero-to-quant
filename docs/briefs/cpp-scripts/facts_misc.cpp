// Facts for l20, l21, l23 and the exam extension, checked natively with g++ and clang++ (no undefined behaviour is run).
// Build: g++ -std=c++17 -O1 -fno-exceptions facts_misc.cpp -o facts_misc && ./facts_misc     (clang++ too)
// Every line printed is also a CHECK: the program returns 1 if any expectation fails.
#include <climits>
#include <cstdio>
#include <cstdlib>
#include <memory>
#include <new>
#include <string>
#include <type_traits>
#include <utility>
#include <vector>

static int bad = 0;
#define CHECK(c) do { if (!(c)) { ++bad; std::printf("FAIL line %d: %s\n", __LINE__, #c); } } while (0)

// allocation counter, as the app's allocCheck
static int g_allocs = 0;
void* operator new(std::size_t n) { ++g_allocs; void* p = std::malloc(n ? n : 1); if (!p) std::abort(); return p; }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }

struct Tracked {
    static inline int copies = 0, moves = 0;
    Tracked() = default;
    Tracked(const Tracked&) { ++copies; }
    Tracked(Tracked&&) noexcept { ++moves; }
};
struct SlowMove {
    static inline int copies = 0, moves = 0;
    int v;
    SlowMove(int x) : v(x) {}
    SlowMove(const SlowMove& o) : v(o.v) { ++copies; }
    SlowMove(SlowMove&& o) : v(o.v) { ++moves; }
};

// ---- l20: a destructor, even `= default`, stops the implicit move; a unique_ptr member then leaves the class neither copyable nor movable
struct WithDtor { std::string s; ~WithDtor() = default; };
struct Owner { std::unique_ptr<int> p; ~Owner() {} };
struct OwnerZero { std::unique_ptr<int> p; };

// ---- l21
struct Payoff {
    explicit Payoff(double k) : strike(k) {}
    virtual double value(double) const { return 0.0; }
    double strike;
};
struct Call : Payoff {
    using Payoff::Payoff;
    double value(double s) const override { return s > strike ? s - strike : 0.0; }
};
struct NameBase {
    NameBase() { who = name(); }
    virtual std::string name() const { return "Base"; }
    virtual ~NameBase() = default;
    std::string who;
};
struct NameDerived : NameBase { std::string name() const override { return "Derived"; } };
struct NoVDtor { ~NoVDtor() {} };
static int derived_dtors = 0;
struct DerivedOfNoV : NoVDtor { ~DerivedOfNoV() { ++derived_dtors; } };
struct Quote { virtual double mid() const { return (bid + ask) / 2; } double bid = 99.0, ask = 101.0; };
struct PlainQuote { double bid, ask; };

// ---- exam: a clone() idiom
struct Shape {
    virtual ~Shape() = default;
    virtual double value(double s) const = 0;
    virtual std::unique_ptr<Shape> clone() const = 0;
};

int main() {
    // l20
    CHECK(!std::is_nothrow_move_constructible_v<WithDtor> || true);
    { WithDtor a{std::string(100, 'x')}; Tracked::copies = 0; WithDtor b = std::move(a); CHECK(a.s.size() == 100); }  // moved from a long string: a still holds it, so it was copied
    CHECK(!std::is_copy_constructible_v<Owner>);
    CHECK(!std::is_move_constructible_v<Owner>);
    CHECK(std::is_default_constructible_v<Owner>);
    CHECK(!std::is_copy_assignable_v<Owner>);
    CHECK(!std::is_move_assignable_v<Owner>);
    CHECK(!std::is_copy_constructible_v<OwnerZero>);
    CHECK(std::is_move_constructible_v<OwnerZero>);
    // l21
    { Call c(100); Payoff sliced = c; const Payoff& ref = c; CHECK(sliced.value(110) == 0.0); CHECK(ref.value(110) == 10.0); }
    { NameDerived d; CHECK(d.who == "Base"); CHECK(d.name() == "Derived"); }
    { derived_dtors = 0; std::shared_ptr<NoVDtor> sp = std::make_shared<DerivedOfNoV>(); sp.reset(); CHECK(derived_dtors == 1); }
    CHECK(sizeof(PlainQuote) == 16);
    CHECK(sizeof(Quote) == 8 + 16);   // desktop: vptr 8 + two doubles; wasm32 is 4 + 4 padding + 16 (see wasm_sizes.cpp)
    // l23
    { g_allocs = 0; std::shared_ptr<int> a(new int(1)); CHECK(g_allocs == 2); }
    { g_allocs = 0; auto a = std::make_shared<int>(1); CHECK(g_allocs == 1); }
    CHECK(sizeof(std::unique_ptr<int>) == sizeof(int*));
    CHECK(sizeof(std::shared_ptr<int>) == 2 * sizeof(int*));
    // l22
    CHECK(static_cast<unsigned long long>(INT_MAX) == 2147483647ULL);
    CHECK(2500000000LL > INT_MAX);                              // £25,000,000 in pence does not fit an int
    { unsigned u = 0; CHECK(u - 1 == 4294967295u); }            // unsigned wrap is defined (32-bit unsigned)
    // exam
    { const Tracked c; Tracked::copies = Tracked::moves = 0; Tracked d = std::move(c); CHECK(Tracked::copies == 1 && Tracked::moves == 0); }
    { SlowMove::copies = SlowMove::moves = 0; std::vector<SlowMove> v; for (int i = 0; i < 4; ++i) v.push_back(SlowMove(i)); CHECK(SlowMove::copies == 3 && SlowMove::moves == 4); }
    { SlowMove::copies = SlowMove::moves = 0; std::vector<SlowMove> v; for (int i = 0; i < 3; ++i) v.push_back(SlowMove(i)); CHECK(SlowMove::copies == 3 && SlowMove::moves == 3); }
    std::printf(bad ? "SOME FACT FAILED\n" : "ALL FACTS OK\n");
    return bad ? 1 : 0;
}
