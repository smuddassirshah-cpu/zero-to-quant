"""cpp level 5 performance task h5-sole-and-counted: recompute every number and run
the solution, a second solution, the starter and planted wrong solutions against
every hidden test.

Route A: each value test is compiled natively with g++ and clang++ at -O1
-fno-exceptions (-std=c++20 and the app's -std=c++17), one process per test as in
the app. The unit is built as cpp-grade.js builds it: the engine's own leakCheck
block (read from app/js/engine/widgets/cpp-grade.js, so freed memory is poisoned
with 0xDD and kept out of reuse, a double delete exits 1, a leak exits 1), then the
widget's prelude, the code, the postlude, and the test's setup and call inside one
function whose locals die before the value is printed. A value test passes when the
process exits 0 and prints the expected value. The compile test passes when
-fsyntax-only agrees with its expect. Route B: a Python model of the owners, the
counts and the live objects replays every value test. Exit 0 only if both routes
agree with every expect, both solutions pass every test on every build, the starter
fails, and every planted slip fails at least one test on every build.
"""
import json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
HW = os.path.join(ROOT, 'app', 'content', 'courses', 'cpp', 'homework-5.json')
GRADE = os.path.join(ROOT, 'app', 'js', 'engine', 'widgets', 'cpp-grade.js')
items = json.load(open(HW))['items']
idx = next(k for k, i in enumerate(items) if i['id'] == 'h5-sole-and-counted')
item = items[idx]
W = item['widget']
T = W['tests']
fails = []


def check(cond, msg):
    print('ok  ' if cond else 'FAIL', msg)
    if not cond:
        fails.append(msg)


# ---- shape ----------------------------------------------------------------
check(item.get('performance') == 'code' and W['language'] == 'cpp', 'performance code item in C++')
check(idx == len(items) - 1 and len(items) == 10, 'appended as item 10 of 10 (index 9)')
check(len(T) == 15 and len(W['examples']) == 2 and all(e in T for e in W['examples']), '15 tests, 2 examples, both among the tests')
check('15 hidden tests' in W['how'], 'how says 15 hidden tests')
check(sum(1 for t in T if 'compiles' in t) == 1 and 'One test only compiles' in W['how'], 'how: one compile test')
check(W.get('leakCheck') is True and 'leak or a double delete' in W['how'], 'leakCheck on, and how says so')
check(not item.get('hints') and 'TODO' not in W['starter'] and '{' not in W['starter'], 'no hints, and the starter is a blank file')

# ---- route B: a Python model ------------------------------------------------
class Heap:
    def __init__(self):
        self.live = {'Quote': 0, 'State': 0, 'Frame': 0}

class Obj:
    def __init__(self, heap, kind, v, older=None):
        self.heap, self.kind, self.v, self.older = heap, kind, v, older
        heap.live[kind] += 1
    def destroy(self):
        self.heap.live[self.kind] -= 1
        if self.older is not None:
            self.older.drop()

class Sole:
    """one owner; drop deletes the object"""
    def __init__(self, obj=None): self.obj = obj
    def release(self): o, self.obj = self.obj, None; return o
    def move_from(self, other):
        old, self.obj = self.obj, other.release()   # take first, delete last
        if old is not None: old.destroy()
    def drop(self):
        if self.obj is not None: o, self.obj = self.obj, None; o.destroy()

class Block:
    def __init__(self, obj): self.obj, self.n = obj, 1

class Counted:
    def __init__(self, obj=None): self.b = Block(obj) if obj is not None else None
    def count(self): return self.b.n if self.b else 0
    def copy(self):
        c = Counted(); c.b = self.b
        if c.b: c.b.n += 1
        return c
    def take(self):
        c = Counted(); c.b, self.b = self.b, None; return c
    def assign_copy(self, other):
        new = other.copy(); old, self.b = self.b, new.b; Counted._release(old)
    def assign_move(self, other):
        new = other.take(); old, self.b = self.b, new.b; Counted._release(old)
    @staticmethod
    def _release(b):
        if b is not None:
            b.n -= 1
            if b.n == 0: b.obj.destroy()
    def drop(self): Counted._release(self.b); self.b = None
    @property
    def obj(self): return self.b.obj if self.b else None

def u_chain(h):
    head = Sole()
    for s in range(1, 5):
        n = Sole(Obj(h, 'State', s, Sole())); n.obj.older.move_from(head); head.move_from(n)
    return head

def c_chain(h):
    latest = Counted(Obj(h, 'Frame', 1, Counted()))
    for s in range(2, 5):
        tmp = Counted(Obj(h, 'Frame', s, latest.copy())); latest.assign_move(tmp)
    return latest

M = [None] * len(T)
h = Heap(); p = Sole(Obj(h, 'Quote', 5)); p.drop(); M[0] = h.live['Quote']
h = Heap(); a = Sole(Obj(h, 'Quote', 7)); b = Sole(); b.obj = a.release(); M[1] = (100 if a.obj is None else 0) + b.obj.v
h = Heap(); a = Sole(Obj(h, 'Quote', 1)); b = Sole(Obj(h, 'Quote', 2)); b.move_from(a); M[2] = (100 if a.obj is None else 0) + h.live['Quote'] * 10 + b.obj.v
h = Heap(); a = Sole(Obj(h, 'Quote', 3)); raw = a.release(); alive = h.live['Quote']; px = raw.v; raw.destroy(); M[3] = alive * 100 + px * 10 + (1 if a.obj is None else 0)
M[4] = 'refused'
h = Heap(); head = u_chain(h); head.move_from(head.obj.older); M[5] = head.obj.v * 10 + h.live['State']
h = Heap(); a = Counted(Obj(h, 'Quote', 1)); b = a.copy(); c = b.copy(); mid = a.count(); c.drop(); b.drop(); M[6] = mid * 100 + a.count() * 10 + h.live['Quote']
h = Heap(); a = Counted(Obj(h, 'Quote', 1)); b = Counted(Obj(h, 'Quote', 2)); b.assign_copy(a); c = Counted(Obj(h, 'Quote', 3)); c.assign_copy(c); M[7] = h.live['Quote'] * 100 + a.count() * 10 + c.count()
M[8] = [1, 1, 1, 1]
h = Heap(); a = Counted(Obj(h, 'Quote', 4)); b = a.take(); M[9] = b.count() * 100 + a.count() * 10 + (1 if a.obj is None else 0)
h = Heap(); a = Counted(Obj(h, 'Quote', 1)); b = Counted(Obj(h, 'Quote', 2)); c = b.copy(); b.assign_move(a); M[10] = h.live['Quote'] * 1000 + b.count() * 100 + c.count() * 10 + a.count()
h = Heap(); latest = c_chain(h); latest.assign_copy(latest.obj.older); M[11] = latest.obj.v * 100 + latest.count() * 10 + h.live['Frame']
h = Heap(); latest = c_chain(h); latest.assign_move(latest.obj.older); M[12] = latest.obj.v * 100 + latest.count() * 10 + h.live['Frame']
h = Heap(); u = Sole(Obj(h, 'Quote', 6)); s = Counted(u.release()); c = s.copy(); M[13] = (1000 if u.obj is None else 0) + s.count() * 100 + c.obj.v * 10 + h.live['Quote']
h = Heap(); u = Sole(); o = u.release(); s = Counted(o); M[14] = s.count() * 10 + (1 if s.obj is None else 0)
for k, t in enumerate(T):
    if 'compiles' in t:
        check(t['expect'] is False and M[k] == 'refused', 'test %d: copying a SolePtr must be refused' % (k + 1))
    else:
        check(M[k] == t['expect'], 'test %d: expect %s, model %s' % (k + 1, t['expect'], M[k]))

# hand checks of the packed values: each digit is one quantity
check(2 * 100 + 2 * 10 + 1 == 221 and 1 * 100 + 0 * 10 + 1 == 101 and 2 * 1000 + 1 * 100 + 1 * 10 + 0 == 2110, 'tests 8, 10, 11: digits are counts and live objects')
check(3 * 100 + 1 * 10 + 3 == 313 and 3 * 10 + 3 == 33, 'tests 6, 12, 13: newest seq 3, one owner, three states left of four')
check(1000 + 2 * 100 + 6 * 10 + 1 == 1261 and 3 * 100 + 1 * 10 + 1 == 311, 'tests 7, 14 packed values')

# ---- route A: native builds ---------------------------------------------------
js = open(GRADE).read()
m = re.search(r'const LEAK = String\.raw`(.*?)`;', js, re.S)
check(m is not None and 'memset(p, 0xDD' in m.group(1), "engine leakCheck block read from cpp-grade.js (poison 0xDD)")
LEAK = m.group(1)
PRINT = r'''
#include <cstdio>
#include <string>
#include <vector>
static std::string zq_s(long long v) { return std::to_string(v); }
static std::string zq_s(const std::vector<int>& v) { std::string s = "["; for (std::size_t i = 0; i < v.size(); ++i) { if (i) s += ", "; s += std::to_string(v[i]); } return s + "]"; }
'''
STDS = ['-std=c++20', '-std=c++17']
COMPILERS = [c for c in ('g++', 'clang++') if shutil.which(c)]
check(COMPILERS == ['g++', 'clang++'], 'both g++ and clang++ found')


def expect_text(t):
    e = t['expect']
    return '[' + ', '.join(str(x) for x in e) + ']' if isinstance(e, list) else str(e)


def run_variant(code, cxx, std):
    tmp = tempfile.mkdtemp()
    flags = [std, '-O1', '-fno-exceptions', '-w']
    res = [False] * len(T)
    vals = [k for k, t in enumerate(T) if 'compiles' not in t]
    body = LEAK + W['prelude'] + code + W['postlude'] + PRINT
    for k in vals:
        body += 'static void zq_case_%d(std::string& zq_o) {\n%s\nzq_o = zq_s(%s);\n}\n' % (k, T[k].get('setup', ''), T[k]['call'])
    body += '#include <cstdlib>\nint main(int argc, char** argv) {\n std::string o;\n switch (std::atoi(argv[1])) {\n'
    body += ''.join(' case %d: zq_case_%d(o); break;\n' % (k, k) for k in vals)
    body += ' }\n std::printf("%s\\n", o.c_str());\n std::fflush(stdout);\n return 0;\n}\n'
    src, exe = os.path.join(tmp, 'main.cpp'), os.path.join(tmp, 'a.out')
    open(src, 'w').write(body)
    cp = subprocess.run([cxx] + flags + [src, '-o', exe], capture_output=True, text=True)
    if cp.returncode == 0:
        for k in vals:
            try:
                pr = subprocess.run([exe, str(k)], capture_output=True, text=True, timeout=20)
                res[k] = pr.returncode == 0 and pr.stdout.strip() == expect_text(T[k])
            except subprocess.TimeoutExpired:
                res[k] = False
    elif os.environ.get('SHOWERR'):
        print(cp.stderr[:3000])
    for k, t in enumerate(T):
        if 'compiles' in t:
            s2 = os.path.join(tmp, 'c%d.cpp' % k)
            open(s2, 'w').write(LEAK + W['prelude'] + code + W['postlude'] + '\nvoid zq_probe() {\n%s\n%s\n}\nint main() { return 0; }\n' % (t.get('setup', ''), t['compiles']))
            built = subprocess.run([cxx] + flags + ['-fsyntax-only', s2], capture_output=True).returncode == 0
            res[k] = built == t['expect']
    shutil.rmtree(tmp)
    return res


def run_all(code):
    return {(cxx, std): run_variant(code, cxx, std) for cxx in COMPILERS for std in STDS}


sol = W['solution']
for key, res in run_all(sol).items():
    check(all(res), 'solution passes all 15 on %s %s' % key)

# a second solution, by locals instead of swap, and a member reset for SolePtr
SOL2 = sol
for a, b in [
    ('''        T* taken = other.release();   // take the source first: the old object may own it
        T* old = ptr_;
        ptr_ = taken;
        delete old;
        return *this;''', '''        if (this != &other) reset(other.release());
        return *this;'''),
    ('''    T* release() {''', '''    void reset(T* p) {
        T* old = ptr_;
        ptr_ = p;
        delete old;
    }
    T* release() {'''),
    ('''        CountedPtr copy(other);
        swap(copy);
        return *this;''', '''        T* p = other.ptr_;
        long* c = other.count_;
        if (c) ++*c;
        drop();
        ptr_ = p;
        count_ = c;
        return *this;'''),
    ('''        CountedPtr taken(std::move(other));
        swap(taken);
        return *this;''', '''        T* p = other.ptr_;
        long* c = other.count_;
        other.ptr_ = nullptr;
        other.count_ = nullptr;
        drop();
        ptr_ = p;
        count_ = c;
        return *this;'''),
    ('''    ~CountedPtr() {
        if (count_ && --*count_ == 0) {
            delete ptr_;
            delete count_;
        }
    }''', '''    ~CountedPtr() { drop(); }'''),
    ('''    void swap(CountedPtr& other) noexcept {''', '''    void drop() {
        long* c = count_;
        T* p = ptr_;
        ptr_ = nullptr;
        count_ = nullptr;
        if (c && --*c == 0) {
            delete p;
            delete c;
        }
    }
    void swap(CountedPtr& other) noexcept {'''),
]:
    check(SOL2.count(a) == 1, 'second solution: anchor found once: %s' % a.strip().splitlines()[0][:50])
    SOL2 = SOL2.replace(a, b)
for key, res in run_all(SOL2).items():
    check(all(res), 'second solution (locals, drop helper) passes all 15 on %s %s' % key)

for key, res in run_all(W['starter']).items():
    check(not any(res[k] for k, t in enumerate(T) if 'compiles' not in t), 'starter fails every value test on %s %s' % key)

LESSON_U = ('''        T* taken = other.release();   // take the source first: the old object may own it
        T* old = ptr_;
        ptr_ = taken;
        delete old;
        return *this;''', '''        if (this != &other) {
            delete ptr_;
            ptr_ = other.ptr_;
            other.ptr_ = nullptr;
        }
        return *this;''')
LESSON_C_COPY = ('''        CountedPtr copy(other);
        swap(copy);
        return *this;''', '''        if (count_ != other.count_) {
            if (other.count_) ++*other.count_;
            if (count_ && --*count_ == 0) { delete ptr_; delete count_; }
            ptr_ = other.ptr_;
            count_ = other.count_;
        }
        return *this;''')
LESSON_C_MOVE = ('''        CountedPtr taken(std::move(other));
        swap(taken);
        return *this;''', '''        if (this != &other) {
            if (count_ && --*count_ == 0) { delete ptr_; delete count_; }
            ptr_ = other.ptr_;
            count_ = other.count_;
            other.ptr_ = nullptr;
            other.count_ = nullptr;
        }
        return *this;''')
BUGS = {
    'SolePtr move assignment deletes first, then reads the source': [LESSON_U],
    'SolePtr move assignment reads its own pointer before it releases the source (fix pass, CP5-3)': [('''        T* taken = other.release();   // take the source first: the old object may own it
        T* old = ptr_;
        ptr_ = taken;
        delete old;''', '''        T* old = ptr_;
        ptr_ = other.release();   // take the source first: the old object may own it
        delete old;''')],
    'CountedPtr copy assignment adds one, drops its share, then reads the source': [LESSON_C_COPY],
    'CountedPtr move assignment drops its share, then takes the source': [LESSON_C_MOVE],
    'CountedPtr copy assignment drops first with no guard': [('''        CountedPtr copy(other);
        swap(copy);
        return *this;''', '''        if (count_ && --*count_ == 0) { delete ptr_; delete count_; }
        ptr_ = other.ptr_;
        count_ = other.count_;
        if (count_) ++*count_;
        return *this;''')],
    'CountedPtr copy assignment takes the source, drops, then adds one': [('''        CountedPtr copy(other);
        swap(copy);
        return *this;''', '''        T* p = other.ptr_;
        long* c = other.count_;
        if (count_ && --*count_ == 0) { delete ptr_; delete count_; }
        ptr_ = p;
        count_ = c;
        if (c) ++*c;
        return *this;''')],
    'the SolePtr is not emptied by the CountedPtr built from it': [('CountedPtr(SolePtr<T>&& s) : CountedPtr(s.release()) {}', 'CountedPtr(SolePtr<T>&& s) : CountedPtr(s.get()) {}')],
    'an empty SolePtr gives a count of 1': [('CountedPtr(SolePtr<T>&& s) : CountedPtr(s.release()) {}', 'CountedPtr(SolePtr<T>&& s) : ptr_(s.release()), count_(new long(1)) {}')],
    'CountedPtr move assignment never drops its old share': [('''        CountedPtr taken(std::move(other));
        swap(taken);
        return *this;''', '''        ptr_ = other.ptr_;
        count_ = other.count_;
        other.ptr_ = nullptr;
        other.count_ = nullptr;
        return *this;''')],
    'moves not noexcept': [('SolePtr(SolePtr&& other) noexcept', 'SolePtr(SolePtr&& other)'), ('CountedPtr& operator=(CountedPtr&& other) noexcept', 'CountedPtr& operator=(CountedPtr&& other)')],
    'SolePtr copy written as a shallow copy': [('    SolePtr(const SolePtr&) = delete;\n', '    SolePtr(const SolePtr& o) : ptr_(o.ptr_) {}\n')],
    'SolePtr move constructor leaves the source owning': [('SolePtr(SolePtr&& other) noexcept : ptr_(other.release()) {}', 'SolePtr(SolePtr&& other) noexcept : ptr_(other.get()) {}')],
    'release() deletes the object': [('''        T* p = ptr_;
        ptr_ = nullptr;
        return p;''', '''        T* p = ptr_;
        delete ptr_;
        ptr_ = nullptr;
        return p;''')],
    'CountedPtr copy constructor does not add one': [('''        if (count_) ++*count_;
    }
    CountedPtr(CountedPtr&& other)''', '''    }
    CountedPtr(CountedPtr&& other)''')],
    'CountedPtr move constructor copies the share': [('''    CountedPtr(CountedPtr&& other) noexcept : ptr_(other.ptr_), count_(other.count_) {
        other.ptr_ = nullptr;
        other.count_ = nullptr;
    }''', '''    CountedPtr(CountedPtr&& other) noexcept : ptr_(other.ptr_), count_(other.count_) {
        if (count_) ++*count_;
    }''')],
    'the destructor frees the object but not the count': [('''            delete ptr_;
            delete count_;''', '''            delete ptr_;''')],
    'the destructor deletes at a count of 1, not 0': [('if (count_ && --*count_ == 0) {', 'if (count_ && (*count_)-- == 2) {')],
}
caught = {}
for name, edits in BUGS.items():
    code = sol
    for a, b in edits:
        check(code.count(a) == 1, 'planted "%s": anchor found once' % name)
        code = code.replace(a, b)
    results = run_all(code)
    per = {key: [k + 1 for k, r in enumerate(res) if not r] for key, res in results.items()}
    caught[name] = per
    check(all(per.values()), 'planted "%s" fails tests %s' % (name, '; '.join('%s %s: %s' % (c, s[5:], v) for (c, s), v in per.items())))

# the item's claims about the tests that catch the three slips the lesson's own code makes
check(all(6 in v for v in caught['SolePtr move assignment deletes first, then reads the source'].values()), 'test 6 catches the delete-first SolePtr move')
check(all(v == [3] for v in caught['SolePtr move assignment reads its own pointer before it releases the source (fix pass, CP5-3)'].values()), 'test 3 (self-move folded in) catches the old-before-release SolePtr move, test 3 only')
check(all(12 in v for v in caught['CountedPtr copy assignment adds one, drops its share, then reads the source'].values()), 'test 12 catches the drop-before-read copy')
check(all(13 in v for v in caught['CountedPtr move assignment drops its share, then takes the source'].values()), 'test 13 catches the drop-before-take move')

print('\nFAILURES: %d' % len(fails))
sys.exit(1 if fails else 0)
