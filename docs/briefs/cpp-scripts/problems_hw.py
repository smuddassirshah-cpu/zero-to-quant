# homework-5 code items: P-scope-guard (difficulty 4) and P-vec (difficulty 5).

# ---------------------------------------------------------------- ScopeGuard
G_PRELUDE = '''#include <functional>
#include <string>
#include <utility>
#include <vector>
#include <type_traits>

// Hidden: the callbacks the tests hand to a guard write here.
int ran = 0;
std::string trace;
'''
G_POSTLUDE = '''
// Hidden: a factory that returns a guard by value.
ScopeGuard make_guard() { return ScopeGuard([] { ++ran; }); }
'''
G_HEAD = '''#include <functional>
#include <utility>

// A scope guard runs a callback once, when it goes out of scope, unless it was dismissed.
// Write: the destructor, dismiss(), copying deleted, a noexcept move constructor that
// hands the duty to the new guard (the old one must do nothing), and assignment deleted.
class ScopeGuard {
public:
    explicit ScopeGuard(std::function<void()> f) : f_(std::move(f)), active_(true) {}
'''
G_STARTER = G_HEAD + '''    // TODO: destructor
    void dismiss() {}                    // TODO: the callback will not run
    // TODO: copying deleted; move constructor; assignment deleted

private:
    std::function<void()> f_;
    bool active_;
};
'''
G_SOLUTION = G_HEAD + '''    ~ScopeGuard() {
        if (active_) f_();
    }
    void dismiss() { active_ = false; }

    ScopeGuard(const ScopeGuard&) = delete;
    ScopeGuard& operator=(const ScopeGuard&) = delete;
    ScopeGuard(ScopeGuard&& other) noexcept : f_(std::move(other.f_)), active_(other.active_) {
        other.active_ = false;
    }
    ScopeGuard& operator=(ScopeGuard&&) = delete;

private:
    std::function<void()> f_;
    bool active_;
};
'''
def gm(old, new):
    assert old in G_SOLUTION, old
    return G_SOLUTION.replace(old, new)
G_MUT = {
    "move-leaves-source-active": gm("        other.active_ = false;\n", ""),
    "dismiss-does-nothing": gm("    void dismiss() { active_ = false; }", "    void dismiss() {}"),
    "always-runs": gm("        if (active_) f_();", "        f_();"),
    "assignment-allowed": gm("    ScopeGuard& operator=(ScopeGuard&&) = delete;", "    ScopeGuard& operator=(ScopeGuard&& o) { f_ = std::move(o.f_); active_ = o.active_; o.active_ = false; return *this; }"),
    "copy-allowed": gm("    ScopeGuard(const ScopeGuard&) = delete;\n", "    ScopeGuard(const ScopeGuard& o) : f_(o.f_), active_(o.active_) {}\n"),
}
GT = []
def gt(call, expect, setup="", **kw):
    d = {"call": call, "expect": expect}
    if setup: d["setup"] = setup
    d.update(kw); GT.append(d)
gt("ran", 1, "{ ScopeGuard g([] { ++ran; }); }")
gt("ran", 0, "{ ScopeGuard g([] { ++ran; }); g.dismiss(); }")
gt("ran", 1, "{ ScopeGuard a([] { ++ran; }); ScopeGuard b = std::move(a); }")
gt("ran", 0, "{ ScopeGuard a([] { ++ran; }); ScopeGuard b = std::move(a); b.dismiss(); }")
gt("trace", "ba", "{ ScopeGuard a([] { trace += 'a'; }); ScopeGuard b([] { trace += 'b'; }); }")
gt("ran", 1, "{ ScopeGuard g = make_guard(); }")
gt("ran", 3, "{ std::vector<ScopeGuard> v; v.push_back(ScopeGuard([] { ++ran; })); v.push_back(ScopeGuard([] { ++ran; })); v.push_back(ScopeGuard([] { ++ran; })); }")
gt("inside * 10 + ran", 1, "int inside = -1; { ScopeGuard g([] { ++ran; }); inside = ran; }")
GT.append({"compiles": "ScopeGuard b = a;", "setup": "ScopeGuard a([] {});", "expect": False})
GT.append({"compiles": "ScopeGuard b([] {}); b = std::move(a);", "setup": "ScopeGuard a([] {});", "expect": False})
gt("std::is_nothrow_move_constructible_v<ScopeGuard>", True)
gt("ran", 0, "{ ScopeGuard a([] { ++ran; }); a.dismiss(); ScopeGuard b = std::move(a); }")
P_G = dict(id="P-scope-guard", starter=G_STARTER, solution=G_SOLUTION, prelude=G_PRELUDE, postlude=G_POSTLUDE, tests=GT, alloc=True, leak=True, mutants=G_MUT)

# ---------------------------------------------------------------- Vec
V_PRELUDE = '''#include <utility>
#include <type_traits>

// Hidden: counts copies, moves and live objects. It has no assignment operators and no default constructor.
struct Counted {
    static inline int copies = 0, moves = 0, live = 0;
    int v;
    Counted(int x) : v(x) { ++live; }
    Counted(const Counted& o) : v(o.v) { ++copies; ++live; }
    Counted(Counted&& o) noexcept : v(o.v) { ++moves; ++live; o.v = -1; }
    Counted& operator=(const Counted&) = delete;
    Counted& operator=(Counted&&) = delete;
    ~Counted() { --live; }
};
'''
V_HEAD = '''#include <cstddef>
#include <new>
#include <utility>

// A growing array of T. T need not be default constructible or assignable, so keep raw
// storage from ::operator new and build elements in it with placement new.
// Growth: capacity 0 to start (no allocation), 1 on the first push, then doubling.
// push_back must work when its argument lives inside the vector (v.push_back(v[0])).
// Growth moves elements if T's move constructor is noexcept (std::move_if_noexcept).
template <typename T>
class Vec {
public:
'''
V_STARTER = V_HEAD + '''    Vec() = default;
    // TODO: destructor (destroy every element, then free the block)
    // TODO: copy constructor and copy assignment
    // TODO: move constructor and move assignment (noexcept)
    void push_back(const T& x) { (void)x; }       // TODO
    void push_back(T&& x) { (void)x; }            // TODO

    std::size_t size() const { return size_; }
    std::size_t capacity() const { return cap_; }
    T& operator[](std::size_t i) { return data_[i]; }
    const T& operator[](std::size_t i) const { return data_[i]; }

private:
    std::size_t size_ = 0;
    std::size_t cap_ = 0;
    T* data_ = nullptr;
};
'''
V_SOLUTION = V_HEAD + '''    Vec() = default;
    ~Vec() { destroy(); }

    Vec(const Vec& other) : size_(other.size_), cap_(other.size_), data_(allocate(other.size_)) {
        for (std::size_t i = 0; i < size_; ++i) new (data_ + i) T(other.data_[i]);
    }
    Vec& operator=(const Vec& other) {
        if (this != &other) {
            Vec copy(other);
            swap(copy);
        }
        return *this;
    }
    Vec(Vec&& other) noexcept : size_(other.size_), cap_(other.cap_), data_(other.data_) {
        other.size_ = 0;
        other.cap_ = 0;
        other.data_ = nullptr;
    }
    Vec& operator=(Vec&& other) noexcept {
        if (this != &other) {
            destroy();
            size_ = other.size_;
            cap_ = other.cap_;
            data_ = other.data_;
            other.size_ = 0;
            other.cap_ = 0;
            other.data_ = nullptr;
        }
        return *this;
    }

    void push_back(const T& x) { emplace(x); }
    void push_back(T&& x) { emplace(std::move(x)); }

    std::size_t size() const { return size_; }
    std::size_t capacity() const { return cap_; }
    T& operator[](std::size_t i) { return data_[i]; }
    const T& operator[](std::size_t i) const { return data_[i]; }

private:
    static T* allocate(std::size_t n) {
        return n ? static_cast<T*>(::operator new(n * sizeof(T))) : nullptr;
    }
    void destroy() {
        for (std::size_t i = 0; i < size_; ++i) data_[i].~T();
        ::operator delete(data_);
        size_ = 0;
        cap_ = 0;
        data_ = nullptr;
    }
    void swap(Vec& o) {
        std::swap(size_, o.size_);
        std::swap(cap_, o.cap_);
        std::swap(data_, o.data_);
    }
    template <typename U>
    void emplace(U&& x) {
        if (size_ == cap_) {
            std::size_t new_cap = cap_ ? cap_ * 2 : 1;
            T* fresh = allocate(new_cap);
            new (fresh + size_) T(std::forward<U>(x));      // x may live in the old block, so build it first
            for (std::size_t i = 0; i < size_; ++i) {
                new (fresh + i) T(std::move_if_noexcept(data_[i]));
                data_[i].~T();
            }
            ::operator delete(data_);
            data_ = fresh;
            cap_ = new_cap;
        } else {
            new (data_ + size_) T(std::forward<U>(x));
        }
        ++size_;
    }

    std::size_t size_ = 0;
    std::size_t cap_ = 0;
    T* data_ = nullptr;
};
'''
def vm(old, new):
    assert old in V_SOLUTION, old
    return V_SOLUTION.replace(old, new)
V_MUT = {
    "grows-by-one": vm("std::size_t new_cap = cap_ ? cap_ * 2 : 1;", "std::size_t new_cap = cap_ + 1;"),
    "copies-on-growth": vm("T(std::move_if_noexcept(data_[i]))", "T(data_[i])"),
    "forgets-to-destroy": vm("        for (std::size_t i = 0; i < size_; ++i) data_[i].~T();\n        ::operator delete(data_);\n        size_ = 0;", "        ::operator delete(data_);\n        size_ = 0;"),
    "frees-before-building-new": vm("""            new (fresh + size_) T(std::forward<U>(x));      // x may live in the old block, so build it first
            for (std::size_t i = 0; i < size_; ++i) {
                new (fresh + i) T(std::move_if_noexcept(data_[i]));
                data_[i].~T();
            }
            ::operator delete(data_);""", """            for (std::size_t i = 0; i < size_; ++i) {
                new (fresh + i) T(std::move_if_noexcept(data_[i]));
                data_[i].~T();
            }
            ::operator delete(data_);
            new (fresh + size_) T(std::forward<U>(x));"""),
    "move-leaves-source-owning": vm("""        other.size_ = 0;
        other.cap_ = 0;
        other.data_ = nullptr;
    }
    Vec& operator=(Vec&& other) noexcept {""", """    }
    Vec& operator=(Vec&& other) noexcept {"""),
    "move-not-noexcept": vm("Vec(Vec&& other) noexcept", "Vec(Vec&& other)"),
    "copy-assign-leaks": vm("""        if (this != &other) {
            Vec copy(other);
            swap(copy);
        }
        return *this;""", """        if (this != &other) {
            size_ = other.size_;
            cap_ = other.size_;
            data_ = allocate(other.size_);
            for (std::size_t i = 0; i < size_; ++i) new (data_ + i) T(other.data_[i]);
        }
        return *this;"""),
}
VT = []
def vt(call, expect, setup="", **kw):
    d = {"call": call, "expect": expect}
    if setup: d["setup"] = setup
    d.update(kw); VT.append(d)
PUSH = "Vec<int> v; for (int i = 0; i < 1000; ++i) v.push_back(i);"
vt("v.size() * 10000 + v.capacity()", 10001024, PUSH)
vt("v[0] + v[500] + v[999]", 1499, PUSH)
vt("alloc_count()", 11, "Vec<int> v; reset_alloc_count(); for (int i = 0; i < 1000; ++i) v.push_back(i);")
vt("alloc_count() * 10 + v.capacity()", 0, "reset_alloc_count(); Vec<int> v;")
vt("Counted::copies * 100 + Counted::moves", 15, "{ Vec<Counted> v; for (int i = 0; i < 8; ++i) v.push_back(Counted(i)); }")
vt("Counted::live", 0, "{ Vec<Counted> v; for (int i = 0; i < 5; ++i) v.push_back(Counted(i)); }")
vt("a[0] * 10 + b[0]", 19, "Vec<int> a; a.push_back(1); a.push_back(2); Vec<int> b = a; b[0] = 9;")
vt("Counted::copies - before", 4, "Vec<Counted> a; for (int i = 0; i < 4; ++i) a.push_back(Counted(i)); int before = Counted::copies; Vec<Counted> b = a;")
vt("alloc_count()", 0, "Vec<int> a; for (int i = 0; i < 100; ++i) a.push_back(i); reset_alloc_count(); Vec<int> b = std::move(a);")
vt("a.size() * 1000 + b.size()", 100, "Vec<int> a; for (int i = 0; i < 100; ++i) a.push_back(i); Vec<int> b = std::move(a);")
vt("b.size() * 10 + b[0]", 15, "Vec<int> a; a.push_back(5); Vec<int> b; b.push_back(1); b.push_back(2); b = a;")
vt("b.size() * 10 + b[0] + a.size() * 100", 15, "Vec<int> a; a.push_back(5); Vec<int> b; b.push_back(1); b = std::move(a);")
vt("a.size() * 10 + a[1]", 26, "Vec<int> a; a.push_back(5); a.push_back(6); Vec<int>& r = a; a = r;")
vt("v[1]", 7, "Vec<int> v; v.push_back(7); v.push_back(v[0]);")
vt("std::is_nothrow_move_constructible_v<Vec<int>>", True)
P_V = dict(id="P-vec", starter=V_STARTER, solution=V_SOLUTION, prelude=V_PRELUDE, tests=VT, alloc=True, leak=True, mutants=V_MUT)

PROBLEMS = [P_G, P_V]
