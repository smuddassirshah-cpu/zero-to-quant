"""Second read, cpp L5 h5-sole-and-counted and the l23 lesson's model code.

Part A: the shipped solution, the starter, a reader solution and reader plants on the 15 hidden
tests (g++ and clang++, -std=c++17 and c++20, -O1 -fno-exceptions, engine leak block).
Part B: self-move of a SolePtr (the spec's "every assignment works for a = a"): the shipped
solution breaks it; the proposed reorder and a folded test 3 fix it.
Part C: l23 screens[2] UniquePtr and screens[5] SharedPtr models (and the move orders taught by
screens[4], review-5 r5-unique-move-assign and homework-5 h5-shared-move-assign) on their own
tests and on a source that lives inside the object being let go; the proposed fixed models pass
the old tests and the new ones.
Part E (fix pass, in cpp14_fixpass.py): the fixed content in the worktree: the three code screens
pass, starters and the as-found models fail the new tests, the reader plants still fail, and the two
order items accept exactly the orders that run safely (every order of the lines, compiled and run).
Parts A to D read the content as found, at the read commit ab13bb6 (git show), so they still
describe the read after the fix lands.
Exit 0 only if every claim holds on every build.
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cppharness14 import ROOT, run_builds, run_unit, failing, BUILDS

C = os.path.join(ROOT, 'app', 'content', 'courses', 'cpp')
READ_AT = 'ab13bb6'


def found(name):
    """The cpp file as the reader found it (the read commit), as text."""
    return subprocess.run(['git', '-C', ROOT, 'show', '%s:app/content/courses/cpp/%s' % (READ_AT, name)],
                          capture_output=True, text=True, check=True).stdout


hw = json.loads(found('homework-5.json'))['items']
item = next(i for i in hw if i['id'] == 'h5-sole-and-counted')
W = item['widget']; T = W['tests']
fails = []


def check(cond, msg):
    print('ok  ' if cond else 'FAIL', msg)
    if not cond:
        fails.append(msg)


def perf(code, tests=T):
    return failing(run_builds(W['prelude'], code, W['postlude'], tests))

# ---------------- Part A ----------------
r = perf(W['solution'])
check(all(v == [] for v in r.values()), 'A: shipped solution passes 15 of 15 on all four builds')
r = perf(W['starter'])
check(all(len(v) == 15 or v == [k for k in range(1, 16) if k != 5] for v in r.values()), 'A: starter fails every value test (does not compile): %s' % r[BUILDS[0]])

READER = r'''#include <utility>

template <typename T>
class SolePtr {
    T* p_ = nullptr;
public:
    SolePtr() noexcept {}
    explicit SolePtr(T* p) noexcept : p_(p) {}
    SolePtr(const SolePtr&) = delete;
    SolePtr& operator=(const SolePtr&) = delete;
    SolePtr(SolePtr&& o) noexcept : p_(o.release()) {}
    SolePtr& operator=(SolePtr&& o) noexcept { reset(o.release()); return *this; }
    ~SolePtr() { reset(nullptr); }
    void reset(T* q) noexcept { T* old = p_; p_ = q; delete old; }
    T* release() noexcept { T* q = p_; p_ = nullptr; return q; }
    T* get() const noexcept { return p_; }
    T& operator*() const { return *p_; }
    T* operator->() const noexcept { return p_; }
};

template <typename T>
class CountedPtr {
    struct Block { long n; };
    T* p_ = nullptr;
    Block* b_ = nullptr;
    static void let_go(T* p, Block* b) {
        if (b && --b->n == 0) { delete p; delete b; }
    }
public:
    CountedPtr() noexcept {}
    explicit CountedPtr(T* p) : p_(p), b_(p ? new Block{1} : nullptr) {}
    CountedPtr(SolePtr<T>&& s) { T* p = s.release(); if (p) { p_ = p; b_ = new Block{1}; } }
    CountedPtr(const CountedPtr& o) noexcept : p_(o.p_), b_(o.b_) { if (b_) ++b_->n; }
    CountedPtr(CountedPtr&& o) noexcept : p_(o.p_), b_(o.b_) { o.p_ = nullptr; o.b_ = nullptr; }
    CountedPtr& operator=(const CountedPtr& o) noexcept {
        T* op = p_; Block* ob = b_;
        p_ = o.p_; b_ = o.b_;
        if (b_) ++b_->n;
        let_go(op, ob);
        return *this;
    }
    CountedPtr& operator=(CountedPtr&& o) noexcept {
        T* op = p_; Block* ob = b_;
        T* np = o.p_; Block* nb = o.b_;
        o.p_ = nullptr; o.b_ = nullptr;
        p_ = np; b_ = nb;
        let_go(op, ob);
        return *this;
    }
    ~CountedPtr() { let_go(p_, b_); }
    long use_count() const noexcept { return b_ ? b_->n : 0; }
    T* get() const noexcept { return p_; }
    T& operator*() const { return *p_; }
    T* operator->() const noexcept { return p_; }
};
'''
r = perf(READER)
check(all(v == [] for v in r.values()), 'A: reader solution (reset(release()), a Block struct, locals) passes 15 of 15')


def plant(src, a, b):
    assert src.count(a) == 1, a
    return src.replace(a, b)

PLANTS = {
    'P1 SolePtr move assignment swaps (source keeps the old object)':
        plant(READER, 'SolePtr& operator=(SolePtr&& o) noexcept { reset(o.release()); return *this; }',
              'SolePtr& operator=(SolePtr&& o) noexcept { T* t = p_; p_ = o.p_; o.p_ = t; return *this; }'),
    'P2 release() does not empty the SolePtr':
        plant(READER, 'T* release() noexcept { T* q = p_; p_ = nullptr; return q; }', 'T* release() noexcept { return p_; }'),
    'P3 CountedPtr move assignment written as a copy (source not emptied)':
        plant(READER, '''        T* np = o.p_; Block* nb = o.b_;
        o.p_ = nullptr; o.b_ = nullptr;
        p_ = np; b_ = nb;''', '''        p_ = o.p_; b_ = o.b_;
        if (b_) ++b_->n;'''),
    'P4 CountedPtr copy assignment lets go before it reads the source':
        plant(READER, '''        T* op = p_; Block* ob = b_;
        p_ = o.p_; b_ = o.b_;
        if (b_) ++b_->n;
        let_go(op, ob);''', '''        if (this != &o) {
            let_go(p_, b_);
            p_ = o.p_; b_ = o.b_;
            if (b_) ++b_->n;
        }'''),
    'P5 CountedPtr(T*) starts a block for a null pointer':
        plant(READER, 'CountedPtr(SolePtr<T>&& s) { T* p = s.release(); if (p) { p_ = p; b_ = new Block{1}; } }',
              'CountedPtr(SolePtr<T>&& s) : p_(s.release()), b_(new Block{1}) {}'),
    'P6 the last owner frees the object but not the block':
        plant(READER, 'if (b && --b->n == 0) { delete p; delete b; }', 'if (b && --b->n == 0) { delete p; }'),
    'P7 SolePtr has no destructor':
        plant(READER, '    ~SolePtr() { reset(nullptr); }\n', ''),
    'P8 CountedPtr move constructor missing (the copy is used)':
        plant(READER, '    CountedPtr(CountedPtr&& o) noexcept : p_(o.p_), b_(o.b_) { o.p_ = nullptr; o.b_ = nullptr; }\n', ''),
}
for name, code in PLANTS.items():
    r = perf(code)
    check(all(v for v in r.values()), 'A: plant %s fails tests %s' % (name, r[BUILDS[0]]))

# ---------------- Part B: self-move of a SolePtr ----------------
SELF = [{'setup': 'SolePtr<Quote> a(new Quote(8)); SolePtr<Quote>& r = a; a = std::move(r);',
         'call': '(a.get() != nullptr ? 100 : 0) + a->px * 10 + Quote::live', 'expect': 181, 'compare': 'equal'}]
r = perf(W['solution'], SELF)
check(all(v == [1] for v in r.values()), 'B: shipped solution breaks a = std::move(a) on a SolePtr (frees the object it keeps)')
r = perf(READER, SELF)
check(all(v == [] for v in r.values()), 'B: reader solution survives a = std::move(a)')
OLD = '''        T* old = ptr_;
        ptr_ = other.release();   // take the source first: the old object may own it
        delete old;'''
NEW = '''        T* taken = other.release();   // take the source first: the old object may own it
        T* old = ptr_;
        ptr_ = taken;
        delete old;'''
FIXED_SOL = plant(W['solution'], OLD, NEW)
r = perf(FIXED_SOL, T + SELF)
check(all(v == [] for v in r.values()), 'B: proposed solution reorder passes the 15 tests and self-move')
T3 = dict(T[2]); T3['setup'] = T[2]['setup'] + ' SolePtr<Quote>& r = b; b = std::move(r);'
T_FIX = T[:2] + [T3] + T[3:]
r = perf(FIXED_SOL, T_FIX)
check(all(v == [] for v in r.values()), 'B: proposed test 3 (self-move folded in, expect 111 unchanged) passes the fixed solution')
r = perf(W['solution'], T_FIX)
check(all(v == [3] for v in r.values()), 'B: proposed test 3 fails the shipped solution, test 3 only: %s' % r[BUILDS[0]])
r = perf(READER, T_FIX)
check(all(v == [] for v in r.values()), 'B: reader solution passes the proposed tests')
for name, code in PLANTS.items():
    r = perf(code, T_FIX)
    check(all(v for v in r.values()), 'B: plant %s still fails under the proposed tests' % name[:3])

# ---------------- Part C: the lesson ----------------
L = json.loads(found('l23-own-smart-pointer.json'))['screens']
S2, S5 = L[2]['widget'], L[5]['widget']
LINK_U = '''
struct Link {
    static inline int live = 0;
    int v;
    UniquePtr<Link> next;
    explicit Link(int x) : v(x) { ++live; }
    ~Link() { --live; }
};
'''
LINK_S = LINK_U.replace('UniquePtr<Link>', 'SharedPtr<Link>')
NEW_U = [{'setup': 'UniquePtr<Link> h(new Link(1)); h->next = UniquePtr<Link>(new Link(2)); h->next->next = UniquePtr<Link>(new Link(3)); h = std::move(h->next);',
          'call': 'h->v * 10 + Link::live', 'expect': 22, 'compare': 'equal'}]
NEW_S = [{'setup': 'SharedPtr<Link> h(new Link(1)); h->next = SharedPtr<Link>(new Link(2)); h = h->next;',
          'call': 'h->v * 100 + h.use_count() * 10 + Link::live', 'expect': 211, 'compare': 'equal'},
         {'setup': 'SharedPtr<Link> h(new Link(1)); h->next = SharedPtr<Link>(new Link(2)); h = std::move(h->next);',
          'call': 'h->v * 100 + h.use_count() * 10 + Link::live', 'expect': 211, 'compare': 'equal'}]

r = failing(run_builds(S2['prelude'], S2['solution'], '', S2['tests']))
check(all(v == [] for v in r.values()), 'C: l23 screens[2] UniquePtr model passes its own 15 tests')
r = failing(run_builds(S2['prelude'], S2['solution'], LINK_U, NEW_U))
check(all(v == [1] for v in r.values()), 'C: l23 screens[2] model fails h = std::move(h->next) (reads the freed object)')
r = failing(run_builds(S5['prelude'], S5['solution'], '', S5['tests']))
check(all(v == [] for v in r.values()), 'C: l23 screens[5] SharedPtr model passes its own 15 tests')
r = failing(run_builds(S5['prelude'], S5['solution'], LINK_S, NEW_S))
check(all(v == [1, 2] for v in r.values()), 'C: l23 screens[5] model fails h = h->next and h = std::move(h->next)')

# std::unique_ptr / std::shared_ptr do the right thing (the standard's reset(u.release()) order)
STD = '#include <memory>\n'
STD_T = [{'setup': 'struct N { int v; std::unique_ptr<N> next; }; std::unique_ptr<N> h(new N{1, nullptr}); h->next.reset(new N{2, nullptr}); h = std::move(h->next);', 'call': 'h->v', 'expect': 2, 'compare': 'equal'},
         {'setup': 'struct N { int v; std::shared_ptr<N> next; }; std::shared_ptr<N> h(new N{1, nullptr}); h->next.reset(new N{2, nullptr}); h = h->next;', 'call': 'h->v * 10 + h.use_count()', 'expect': 21, 'compare': 'equal'},
         {'setup': 'struct N { int v; std::shared_ptr<N> next; }; std::shared_ptr<N> h(new N{1, nullptr}); h->next.reset(new N{2, nullptr}); h = std::move(h->next);', 'call': 'h->v * 10 + h.use_count()', 'expect': 21, 'compare': 'equal'}]
r = failing(run_builds('', STD, '', STD_T))
check(all(v == [] for v in r.values()), 'C: std::unique_ptr and std::shared_ptr handle all three cases (the standard library order)')

# proposed lesson models
U_OLD = '''    UniquePtr& operator=(UniquePtr&& other) noexcept {
        if (this != &other) {
            delete ptr_;
            ptr_ = other.ptr_;
            other.ptr_ = nullptr;
        }
        return *this;
    }'''
U_NEW = '''    UniquePtr& operator=(UniquePtr&& other) noexcept {
        if (this != &other) {
            T* p = other.ptr_;      // take the source first: the old object may own it
            other.ptr_ = nullptr;
            delete ptr_;
            ptr_ = p;
        }
        return *this;
    }'''
R_OLD = '''    void reset(T* p = nullptr) {'''
S2_FIX = plant(S2['solution'], U_OLD, U_NEW)
S2_T = S2['tests'][:2] + [{'setup': 'UniquePtr<Tracked> a(new Tracked(1)); UniquePtr<Tracked> b = std::move(a);', 'call': 'b->v * 10 + (a.get() == nullptr ? 1 : 0)', 'expect': 11, 'compare': 'equal'}] + S2['tests'][4:] + NEW_U
check(len(S2_T) == 15, 'C: proposed screens[2] tests: 15 (old tests 3 and 4 merged, one new)')
r = failing(run_builds(S2['prelude'], S2_FIX, LINK_U, S2_T))
check(all(v == [] for v in r.values()), 'C: proposed screens[2] model passes the proposed 15 tests')
r = failing(run_builds(S2['prelude'], S2['solution'], LINK_U, S2_T))
check(all(v == [15] for v in r.values()), 'C: old screens[2] model fails the proposed test 15 only')
r = failing(run_builds(S2['prelude'], S2['starter'], LINK_U, S2_T))
check(all(len(v) >= 8 for v in r.values()), 'C: screens[2] starter still compiles with the Link postlude and fails: %s' % r[BUILDS[0]])

C_OLD = '''    SharedPtr& operator=(const SharedPtr& other) {
        if (count_ != other.count_) {
            if (other.count_) ++*other.count_;
            drop();
            ptr_ = other.ptr_;
            count_ = other.count_;
        }
        return *this;
    }'''
C_NEW = '''    SharedPtr& operator=(const SharedPtr& other) {
        if (count_ != other.count_) {
            T* p = other.ptr_;      // read the source first: the old object may own it
            long* c = other.count_;
            if (c) ++*c;
            drop();
            ptr_ = p;
            count_ = c;
        }
        return *this;
    }'''
M_OLD = '''    SharedPtr& operator=(SharedPtr&& other) noexcept {
        if (this != &other) {
            drop();
            ptr_ = other.ptr_;
            count_ = other.count_;
            other.ptr_ = nullptr;
            other.count_ = nullptr;
        }
        return *this;
    }'''
M_NEW = '''    SharedPtr& operator=(SharedPtr&& other) noexcept {
        if (this != &other) {
            T* p = other.ptr_;      // take the source first: the old object may own it
            long* c = other.count_;
            other.ptr_ = nullptr;
            other.count_ = nullptr;
            drop();
            ptr_ = p;
            count_ = c;
        }
        return *this;
    }'''
S5_FIX = plant(plant(S5['solution'], C_OLD, C_NEW), M_OLD, M_NEW)
t = S5['tests']
S5_T = [t[0], t[1],
        {'setup': 'long n = 0; { SharedPtr<Tracked> a(new Tracked(1)); { SharedPtr<Tracked> b = a; SharedPtr<Tracked> c = b; } n = a.use_count() * 10 + Tracked::live; }', 'call': 'n * 10 + Tracked::live', 'expect': 110, 'compare': 'equal'},
        t[4], t[5], t[6],
        {'setup': 'long n = 0; { SharedPtr<Tracked> a(new Tracked(1)); SharedPtr<Tracked> b = std::move(a); n = b.use_count() * 10 + a.use_count(); }', 'call': 'n * 10 + Tracked::live', 'expect': 100, 'compare': 'equal'},
        ] + t[9:] + NEW_S
check(len(S5_T) == 15, 'C: proposed screens[5] tests: 15 (old 3+4 and 8+9 merged, two new)')
r = failing(run_builds(S5['prelude'], S5_FIX, LINK_S, S5_T))
check(all(v == [] for v in r.values()), 'C: proposed screens[5] model passes the proposed 15 tests')
r = failing(run_builds(S5['prelude'], S5['solution'], LINK_S, S5_T))
check(all(v == [14, 15] for v in r.values()), 'C: old screens[5] model fails proposed tests 14 and 15 only')
r = failing(run_builds(S5['prelude'], S5['starter'], LINK_S, S5_T))
check(all(len(v) >= 8 for v in r.values()), 'C: screens[5] starter still compiles with the Link postlude and fails: %s' % r[BUILDS[0]])
# the old merged tests keep their meaning: a drop-first copy with no guard still fails
BAD = plant(S5_FIX, '''            T* p = other.ptr_;      // read the source first: the old object may own it
            long* c = other.count_;
            if (c) ++*c;
            drop();''', '''            drop();
            T* p = other.ptr_;
            long* c = other.count_;
            if (c) ++*c;''')
r = failing(run_builds(S5['prelude'], BAD, LINK_S, S5_T))
check(all(14 in v for v in r.values()), 'C: a drop-first copy assignment fails proposed test 14: %s' % r[BUILDS[0]])

# the orders the review-5 and homework-5 order items teach, written out, fail too; the proposed orders pass
R5_OLD = U_OLD  # guard, delete ptr_, ptr_ = other.ptr_, other.ptr_ = nullptr, return
check(True, 'C: review-5 r5-unique-move-assign key (guard, delete, take, null) is the screens[2] order above')
H5_OLD = M_OLD  # guard, drop, take, empty
check(True, 'C: homework-5 h5-shared-move-assign key (guard, drop, take, empty) is the screens[5] move order above')
r = failing(run_builds(S5['prelude'], plant(S5['solution'], C_OLD, C_NEW), LINK_S, NEW_S))
check(all(v == [2] for v in r.values()), 'C: with the copy fixed, the old move order (h5 key) still fails h = std::move(h->next)')

# ---------------- Part D: the exact fix in fix14.mjs, on a temporary copy of the cpp folder ----------------
import shutil, subprocess, tempfile
for old in (False, True):
    tmp = tempfile.mkdtemp()
    shutil.copytree(C, os.path.join(tmp, 'content', 'courses', 'cpp'))
    for name in ('l23-own-smart-pointer.json', 'review-5.json', 'homework-5.json'):
        open(os.path.join(tmp, 'content', 'courses', 'cpp', name), 'w').write(found(name))
    args = ['node', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fix14.mjs'), tmp] + (['--old-solutions'] if old else [])
    check(subprocess.run(args, capture_output=True).returncode == 0, 'D: fix14.mjs applies' + (' (old solutions)' if old else ''))
    LF = json.load(open(os.path.join(tmp, 'content', 'courses', 'cpp', 'l23-own-smart-pointer.json')))['screens']
    HF = json.load(open(os.path.join(tmp, 'content', 'courses', 'cpp', 'homework-5.json')))['items']
    SC = next(i for i in HF if i['id'] == 'h5-sole-and-counted')['widget']
    got = {}
    for name, w in (('l23 screens[2]', LF[2]['widget']), ('l23 screens[5]', LF[5]['widget']), ('h5-sole-and-counted', SC)):
        r = failing(run_builds(w['prelude'], w['solution'], w.get('postlude', ''), w['tests']))
        got[name] = r
        if not old:
            check(all(v == [] for v in r.values()) and len(w['tests']) == 15, 'D: fixed %s solution passes its 15 tests on all four builds' % name)
            rs = failing(run_builds(w['prelude'], w['starter'], w.get('postlude', ''), w['tests']))
            check(all(len(v) >= 1 for v in rs.values()), 'D: fixed %s starter fails: %s' % (name, rs[BUILDS[0]]))
    if old:
        check(all(v == [15] for v in got['l23 screens[2]'].values()), 'D: old UniquePtr model fails the new test 15 only')
        check(all(v == [14, 15] for v in got['l23 screens[5]'].values()), 'D: old SharedPtr model fails the new tests 14 and 15 only')
        check(all(v == [3] for v in got['h5-sole-and-counted'].values()), 'D: old h5 solution fails the folded test 3 only')
    if not old:
        FIXED14 = {n: json.load(open(os.path.join(tmp, 'content', 'courses', 'cpp', n))) for n in ('l23-own-smart-pointer.json', 'review-5.json', 'homework-5.json')}
    shutil.rmtree(tmp)
# ---------------- Part E: the fix pass, on the worktree's own content ----------------
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cpp14_fixpass.py')).read())

print('\nFAILURES: %d' % len(fails))
sys.exit(1 if fails else 0)
