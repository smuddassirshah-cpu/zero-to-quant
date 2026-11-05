# P-unique-ptr and P-shared-ptr: l23-own-smart-pointer. Both use leakCheck (the app flag) and a hidden Tracked type that counts live objects.
PRELUDE = '''#include <utility>
#include <vector>
#include <type_traits>

// Hidden: counts how many Tracked objects are alive.
struct Tracked {
    static inline int live = 0;
    int v;
    explicit Tracked(int x) : v(x) { ++live; }
    ~Tracked() { --live; }
};
'''

# ---------------------------------------------------------------- UniquePtr
U_HEAD = '''// A minimal unique pointer. It owns one heap object, or nothing.
// Write: the destructor; copying deleted; a move constructor and move assignment that
// transfer ownership and leave the source empty; release(); reset().
template <typename T>
class UniquePtr {
public:
    UniquePtr() = default;
    explicit UniquePtr(T* p) : ptr_(p) {}

'''
U_ACCESS = '''
    T* get() const { return ptr_; }
    T& operator*() const { return *ptr_; }
    T* operator->() const { return ptr_; }
    explicit operator bool() const { return ptr_ != nullptr; }

'''
U_TAIL = '''
private:
    T* ptr_ = nullptr;
};
'''
U_STARTER = U_HEAD + '''    // TODO: destructor
    // TODO: delete copying; write the move constructor and move assignment
''' + U_ACCESS + '''    T* release() { return nullptr; }                 // TODO: give up ownership, do not delete
    void reset(T* p = nullptr) { (void)p; }          // TODO: delete the current object, then own p
''' + U_TAIL
U_OWN = '''    ~UniquePtr() { delete ptr_; }
    UniquePtr(const UniquePtr&) = delete;
    UniquePtr& operator=(const UniquePtr&) = delete;
    UniquePtr(UniquePtr&& other) noexcept : ptr_(other.ptr_) { other.ptr_ = nullptr; }
    UniquePtr& operator=(UniquePtr&& other) noexcept {
        if (this != &other) {
            delete ptr_;
            ptr_ = other.ptr_;
            other.ptr_ = nullptr;
        }
        return *this;
    }
'''
U_RR = '''    T* release() {
        T* p = ptr_;
        ptr_ = nullptr;
        return p;
    }
    void reset(T* p = nullptr) {
        T* old = ptr_;
        ptr_ = p;
        delete old;
    }
'''
U_SOLUTION = U_HEAD + U_OWN + U_ACCESS + U_RR + U_TAIL
def um(old, new):
    assert old in U_SOLUTION, old
    return U_SOLUTION.replace(old, new)
U_MUT = {
    "no-destructor": um("    ~UniquePtr() { delete ptr_; }\n", ""),
    "move-does-not-empty-source": um("(UniquePtr&& other) noexcept : ptr_(other.ptr_) { other.ptr_ = nullptr; }", "(UniquePtr&& other) noexcept : ptr_(other.ptr_) {}"),
    "copy-not-deleted": um("    UniquePtr(const UniquePtr&) = delete;\n    UniquePtr& operator=(const UniquePtr&) = delete;\n", "    UniquePtr(const UniquePtr& o) : ptr_(o.ptr_) {}\n    UniquePtr& operator=(const UniquePtr& o) { ptr_ = o.ptr_; return *this; }\n"),
    "release-deletes": um("        T* p = ptr_;\n        ptr_ = nullptr;\n        return p;", "        T* p = ptr_;\n        delete ptr_;\n        ptr_ = nullptr;\n        return p;"),
    "reset-leaks-old": um("        T* old = ptr_;\n        ptr_ = p;\n        delete old;", "        ptr_ = p;"),
    "move-assign-leaks-old": um("            delete ptr_;\n            ptr_ = other.ptr_;", "            ptr_ = other.ptr_;"),
    "move-assign-no-self-guard": um("""        if (this != &other) {
            delete ptr_;
            ptr_ = other.ptr_;
            other.ptr_ = nullptr;
        }
        return *this;""", """        delete ptr_;
        ptr_ = other.ptr_;
        other.ptr_ = nullptr;
        return *this;"""),
    "move-not-noexcept": um("(UniquePtr&& other) noexcept : ptr_", "(UniquePtr&& other) : ptr_"),
}
UT = []
def ut(call, expect, setup="", **kw):
    d = {"call": call, "expect": expect}
    if setup: d["setup"] = setup
    d.update(kw); UT.append(d)
ut("Tracked::live", 0, "{ UniquePtr<Tracked> p(new Tracked(5)); }")
ut("p->v + (*p).v", 10, "UniquePtr<Tracked> p(new Tracked(5));")
ut("b->v", 1, "UniquePtr<Tracked> a(new Tracked(1)); UniquePtr<Tracked> b = std::move(a);")
ut("a.get() == nullptr", True, "UniquePtr<Tracked> a(new Tracked(1)); UniquePtr<Tracked> b = std::move(a);")
ut("Tracked::live", 0, "{ UniquePtr<Tracked> a(new Tracked(1)); UniquePtr<Tracked> b = std::move(a); }")
UT.append({"compiles": "UniquePtr<Tracked> b = a;", "setup": "UniquePtr<Tracked> a;", "expect": False})
UT.append({"compiles": "UniquePtr<Tracked> b; b = a;", "setup": "UniquePtr<Tracked> a;", "expect": False})
ut("live_after", 1, "UniquePtr<Tracked> a(new Tracked(3)); Tracked* raw = a.release(); int live_after = Tracked::live; delete raw;")
ut("a.get() == nullptr", True, "UniquePtr<Tracked> a(new Tracked(3)); Tracked* raw = a.release(); delete raw;")
ut("Tracked::live * 10 + a->v", 12, "UniquePtr<Tracked> a(new Tracked(1)); a.reset(new Tracked(2));")
ut("Tracked::live", 0, "UniquePtr<Tracked> a(new Tracked(1)); a.reset();")
ut("Tracked::live", 1, "UniquePtr<Tracked> a(new Tracked(1)); UniquePtr<Tracked> b(new Tracked(2)); b = std::move(a);")
ut("a.get() != nullptr", True, "UniquePtr<Tracked> a(new Tracked(4)); UniquePtr<Tracked>& r = a; a = std::move(r);")
ut("std::is_nothrow_move_constructible_v<UniquePtr<Tracked>>", True)
ut("(p ? 10 : 0) + (q ? 1 : 0)", 1, "UniquePtr<Tracked> p; UniquePtr<Tracked> q(new Tracked(1));")
P_U = dict(id="P-unique-ptr", starter=U_STARTER, solution=U_SOLUTION, prelude=PRELUDE, tests=UT, alloc=True, leak=True, mutants=U_MUT)

# ---------------------------------------------------------------- SharedPtr
S_HEAD = '''// A minimal reference-counted pointer. All owners share one heap counter next to the object.
// The object is deleted, and the counter freed, when the last owner goes.
// Write: the copy and move members and the destructor. use_count() is 0 for an empty pointer.
template <typename T>
class SharedPtr {
public:
    SharedPtr() = default;
    explicit SharedPtr(T* p) : ptr_(p), count_(p ? new long(1) : nullptr) {}

'''
S_ACCESS = '''
    long use_count() const { return count_ ? *count_ : 0; }
    T* get() const { return ptr_; }
    T& operator*() const { return *ptr_; }
    T* operator->() const { return ptr_; }

private:
    T* ptr_ = nullptr;
    long* count_ = nullptr;
'''
S_STARTER = S_HEAD + '''    // TODO: copy constructor: share the object and add one to the count
    SharedPtr(const SharedPtr& other) : ptr_(other.ptr_), count_(other.count_) {}
    // TODO: copy assignment: let go of the old object, share the new one
    SharedPtr& operator=(const SharedPtr& other) {
        ptr_ = other.ptr_;
        count_ = other.count_;
        return *this;
    }
    // TODO: move constructor and move assignment (noexcept): take over, leave the source empty
    // TODO: destructor: subtract one; at zero delete the object and the counter
    ~SharedPtr() {}
''' + S_ACCESS + "};\n"
S_OWN = '''    SharedPtr(const SharedPtr& other) : ptr_(other.ptr_), count_(other.count_) {
        if (count_) ++*count_;
    }
    SharedPtr& operator=(const SharedPtr& other) {
        if (count_ != other.count_) {
            if (other.count_) ++*other.count_;
            drop();
            ptr_ = other.ptr_;
            count_ = other.count_;
        }
        return *this;
    }
    SharedPtr(SharedPtr&& other) noexcept : ptr_(other.ptr_), count_(other.count_) {
        other.ptr_ = nullptr;
        other.count_ = nullptr;
    }
    SharedPtr& operator=(SharedPtr&& other) noexcept {
        if (this != &other) {
            drop();
            ptr_ = other.ptr_;
            count_ = other.count_;
            other.ptr_ = nullptr;
            other.count_ = nullptr;
        }
        return *this;
    }
    ~SharedPtr() { drop(); }
'''
S_PRIV = '''
    void drop() {
        if (count_ && --*count_ == 0) {
            delete ptr_;
            delete count_;
        }
        ptr_ = nullptr;
        count_ = nullptr;
    }
'''
S_SOLUTION = S_HEAD + S_OWN + S_ACCESS.replace("private:\n    T* ptr_ = nullptr;\n    long* count_ = nullptr;\n", "private:" + S_PRIV + "    T* ptr_ = nullptr;\n    long* count_ = nullptr;\n") + "};\n"
def sm(old, new):
    assert old in S_SOLUTION, old
    return S_SOLUTION.replace(old, new)
S_MUT = {
    "copy-does-not-count": sm("    SharedPtr(const SharedPtr& other) : ptr_(other.ptr_), count_(other.count_) {\n        if (count_) ++*count_;\n    }", "    SharedPtr(const SharedPtr& other) : ptr_(other.ptr_), count_(other.count_) {}"),
    "destructor-never-frees": sm("    ~SharedPtr() { drop(); }", "    ~SharedPtr() {}"),
    "destructor-always-deletes": sm("    ~SharedPtr() { drop(); }", "    ~SharedPtr() { if (count_) { --*count_; delete ptr_; } }"),
    "counter-leaks": sm("            delete ptr_;\n            delete count_;", "            delete ptr_;"),
    "assign-decrements-first": sm("""        if (count_ != other.count_) {
            if (other.count_) ++*other.count_;
            drop();
            ptr_ = other.ptr_;
            count_ = other.count_;
        }
        return *this;""", """        SharedPtr keep_alive_none;
        long* oc = other.count_; T* op = other.ptr_;
        drop();
        ptr_ = op; count_ = oc;
        if (count_) ++*count_;
        return *this;"""),
    "assign-keeps-old": sm("""            if (other.count_) ++*other.count_;
            drop();
            ptr_ = other.ptr_;""", """            if (other.count_) ++*other.count_;
            ptr_ = other.ptr_;"""),
    "move-copies-count": sm("""    SharedPtr(SharedPtr&& other) noexcept : ptr_(other.ptr_), count_(other.count_) {
        other.ptr_ = nullptr;
        other.count_ = nullptr;
    }""", """    SharedPtr(SharedPtr&& other) noexcept : ptr_(other.ptr_), count_(other.count_) {
        if (count_) ++*count_;
    }"""),
    "move-not-noexcept": sm("SharedPtr(SharedPtr&& other) noexcept", "SharedPtr(SharedPtr&& other)"),
}
ST = []
def st(call, expect, setup="", **kw):
    d = {"call": call, "expect": expect}
    if setup: d["setup"] = setup
    d.update(kw); ST.append(d)
st("Tracked::live", 0, "{ SharedPtr<Tracked> a(new Tracked(1)); }")
st("a.use_count()", 2, "SharedPtr<Tracked> a(new Tracked(1)); SharedPtr<Tracked> b = a;")
st("a.use_count() * 10 + Tracked::live", 11, "SharedPtr<Tracked> a(new Tracked(1)); { SharedPtr<Tracked> b = a; SharedPtr<Tracked> c = b; }")
st("Tracked::live", 0, "{ SharedPtr<Tracked> a(new Tracked(1)); SharedPtr<Tracked> b = a; }")
st("Tracked::live", 1, "SharedPtr<Tracked> a(new Tracked(1)); { SharedPtr<Tracked> b = a; }")
st("Tracked::live * 10 + a.use_count()", 12, "SharedPtr<Tracked> a(new Tracked(1)); SharedPtr<Tracked> b(new Tracked(2)); b = a;")
st("Tracked::live * 10 + a.use_count()", 11, "SharedPtr<Tracked> a(new Tracked(1)); SharedPtr<Tracked>& r = a; a = r;")
st("b.use_count() * 10 + a.use_count()", 10, "SharedPtr<Tracked> a(new Tracked(1)); SharedPtr<Tracked> b = std::move(a);")
st("Tracked::live", 0, "{ SharedPtr<Tracked> a(new Tracked(1)); SharedPtr<Tracked> b = std::move(a); }")
st("Tracked::live * 10 + b.use_count()", 11, "SharedPtr<Tracked> a(new Tracked(1)); SharedPtr<Tracked> b(new Tracked(2)); b = std::move(a);")
st("p.use_count() * 10 + (p.get() == nullptr ? 1 : 0)", 1, "SharedPtr<Tracked> p;")
st("b->v + (*a).v", 16, "SharedPtr<Tracked> a(new Tracked(8)); SharedPtr<Tracked> b = a;")
st("a.use_count()", 6, "SharedPtr<Tracked> a(new Tracked(1)); std::vector<SharedPtr<Tracked>> v(5, a);")
st("a.use_count() * 10 + Tracked::live", 11, "SharedPtr<Tracked> a(new Tracked(1)); { std::vector<SharedPtr<Tracked>> v(5, a); }")
st("std::is_nothrow_move_constructible_v<SharedPtr<Tracked>>", True)
P_S = dict(id="P-shared-ptr", starter=S_STARTER, solution=S_SOLUTION, prelude=PRELUDE, tests=ST, alloc=True, leak=True, mutants=S_MUT)

PROBLEMS = [P_U, P_S]
