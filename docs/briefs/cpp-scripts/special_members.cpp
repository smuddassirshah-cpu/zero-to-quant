// l20: what the compiler writes once you declare one special member. Each class has a Tracked member that counts copies and moves,
// so the table shows what really runs: "copy", "move", or "error" (deleted, so it does not compile).
// Build: clang++ -std=c++17 -O1 -fno-exceptions special_members.cpp -o special_members && ./special_members
#include <cstdio>
#include <type_traits>
#include <utility>

struct Tracked {
    static inline int copies = 0, moves = 0;
    Tracked() = default;
    Tracked(const Tracked&) { ++copies; }
    Tracked(Tracked&&) noexcept { ++moves; }
    Tracked& operator=(const Tracked&) { ++copies; return *this; }
    Tracked& operator=(Tracked&&) noexcept { ++moves; return *this; }
};

struct C0 { Tracked m; };                                                                       // nothing declared
struct C1 { C1() = default; ~C1() {} Tracked m; };                                              // destructor
struct C2 { C2() = default; C2(const C2& o) : m(o.m) {} Tracked m; };                           // copy constructor
struct C3 { C3() = default; C3& operator=(const C3& o) { m = o.m; return *this; } Tracked m; }; // copy assignment
struct C4 { C4() = default; C4(C4&& o) noexcept : m(std::move(o.m)) {} Tracked m; };            // move constructor
struct C5 { C5() = default; C5& operator=(C5&& o) noexcept { m = std::move(o.m); return *this; } Tracked m; }; // move assignment
struct C6 {                                                                                      // all five defaulted
    C6() = default; ~C6() = default;
    C6(const C6&) = default; C6& operator=(const C6&) = default;
    C6(C6&&) = default; C6& operator=(C6&&) = default;
    Tracked m;
};

static const char* verdict() { return Tracked::moves ? "move" : Tracked::copies ? "copy" : "none"; }

template <class T> const char* copy_construct() {
    if constexpr (!std::is_copy_constructible_v<T>) return "error";
    else { T a; Tracked::copies = Tracked::moves = 0; T b(a); (void)b; return verdict(); }
}
template <class T> const char* move_construct() {
    if constexpr (!std::is_move_constructible_v<T>) return "error";
    else { T a; Tracked::copies = Tracked::moves = 0; T b(std::move(a)); (void)b; return verdict(); }
}
template <class T> const char* copy_assign() {
    if constexpr (!std::is_copy_assignable_v<T>) return "error";
    else { T a, b; Tracked::copies = Tracked::moves = 0; b = a; return verdict(); }
}
template <class T> const char* move_assign() {
    if constexpr (!std::is_move_assignable_v<T>) return "error";
    else { T a, b; Tracked::copies = Tracked::moves = 0; b = std::move(a); return verdict(); }
}
template <class T> void row(const char* what) {
    std::printf("%-22s | %-6s | %-6s | %-6s | %-6s\n", what, copy_construct<T>(), move_construct<T>(), copy_assign<T>(), move_assign<T>());
}
int main() {
    std::printf("%-22s | %-6s | %-6s | %-6s | %-6s\n", "you declare", "b(a)", "b(mv a)", "b = a", "b = mv a");
    row<C0>("nothing");
    row<C1>("a destructor");
    row<C2>("a copy constructor");
    row<C3>("a copy assignment");
    row<C4>("a move constructor");
    row<C5>("a move assignment");
    row<C6>("all five, defaulted");
}
