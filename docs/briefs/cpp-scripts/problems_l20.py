# P-copy-samples: l20-rule-of-five. The class has a destructor and both move members; the copy members are shallow (the bug).
HEAD = '''#include <utility>

// Samples owns a heap array of doubles. The destructor and the two move members are done.
// The copy constructor and copy assignment are wrong: they copy the pointer, so two objects
// would free one block. Make each a true copy of the doubles.
// Copy assignment must free the old block, be safe for `a = a`, and return *this.
class Samples {
public:
    Samples(int n, double x) : size_(n), data_(new double[n]) {
        for (int i = 0; i < n; ++i) data_[i] = x;
    }
    ~Samples() { delete[] data_; }
    Samples(Samples&& other) noexcept : size_(other.size_), data_(other.data_) {
        other.size_ = 0;
        other.data_ = nullptr;
    }
    Samples& operator=(Samples&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            size_ = other.size_;
            data_ = other.data_;
            other.size_ = 0;
            other.data_ = nullptr;
        }
        return *this;
    }

'''
TAIL = '''
    int size() const { return size_; }
    double get(int i) const { return data_[i]; }
    void set(int i, double x) { data_[i] = x; }

private:
    int size_;
    double* data_;
};
'''
STARTER = HEAD + '''    // TODO: copy the doubles, not the pointer
    Samples(const Samples& other) : size_(other.size_), data_(other.data_) {}
    // TODO: free the old block, copy the doubles, guard against a = a, return *this
    Samples& operator=(const Samples& other) {
        size_ = other.size_;
        data_ = other.data_;
        return *this;
    }
''' + TAIL

COPY_CTOR = '''    Samples(const Samples& other) : size_(other.size_), data_(new double[other.size_]) {
        for (int i = 0; i < size_; ++i) data_[i] = other.data_[i];
    }
'''
ASSIGN = '''    Samples& operator=(const Samples& other) {
        if (this != &other) {
            double* fresh = new double[other.size_];
            for (int i = 0; i < other.size_; ++i) fresh[i] = other.data_[i];
            delete[] data_;
            data_ = fresh;
            size_ = other.size_;
        }
        return *this;
    }
'''
SOLUTION = HEAD + COPY_CTOR + ASSIGN + TAIL

MUTANTS = {
    "assign-leaks-old-block": HEAD + COPY_CTOR + ASSIGN.replace("            delete[] data_;\n", "") + TAIL,
    "assign-copies-twice": HEAD + COPY_CTOR + ASSIGN.replace("            data_ = fresh;\n", "            data_ = new double[other.size_];\n            for (int i = 0; i < other.size_; ++i) data_[i] = fresh[i];\n            delete[] fresh;\n") + TAIL,
    "ctor-copies-size-only": HEAD + '''    Samples(const Samples& other) : size_(other.size_), data_(new double[other.size_]) {}
''' + ASSIGN + TAIL,
    "assign-shallow-only": HEAD + COPY_CTOR + '''    Samples& operator=(const Samples& other) {
        if (this != &other) { delete[] data_; size_ = other.size_; data_ = other.data_; }
        return *this;
    }
''' + TAIL,
}

# Slips no test can see today: the delete-first assignment only misbehaves for `a = a`, by reading the block it has just freed.
# The harness cannot make that read deterministic (see the [Must] under "Raised later (cpp L5 brief, 5 Nov)" in docs/BACKLOG-INBOX.md).
UNCAUGHT = {
    "delete-first-no-guard": HEAD + COPY_CTOR + '''    Samples& operator=(const Samples& other) {
        delete[] data_;
        data_ = new double[other.size_];
        size_ = other.size_;
        for (int i = 0; i < size_; ++i) data_[i] = other.data_[i];
        return *this;
    }
''' + TAIL,
}

PRELUDE = "#include <utility>\n#include <type_traits>\n"

T = []
def t(call, expect, setup="", **kw):
    d = {"call": call, "expect": expect}
    if setup: d["setup"] = setup
    d.update(kw); T.append(d)

t("a.get(0)", 1.5, "Samples a(3, 1.5); Samples b = a; b.set(0, 9.0);")
t("b.get(0)", 9.0, "Samples a(3, 1.5); Samples b = a; b.set(0, 9.0);")
t("b.size()", 3, "Samples a(3, 1.5); Samples b = a;")
t("b.get(2)", 1.5, "Samples a(3, 1.5); Samples b = a;")
t("alloc_count()", 1, "Samples a(1000, 0.5); reset_alloc_count(); Samples b = a;")
t("a.get(1)", 1.5, "Samples a(3, 1.5); Samples b(2, 0.0); b = a; b.set(1, 7.0);")
t("b.size()", 3, "Samples a(3, 1.5); Samples b(2, 0.0); b = a;")
t("alloc_count()", 1, "Samples a(1000, 0.5); Samples b(2, 0.0); reset_alloc_count(); b = a;")
t("a.get(0) + a.get(1)", 3.0, "Samples a(10, 1.5); Samples& r = a; a = r;")
t("c.size()", 2, "Samples a(2, 1.0); Samples b(5, 2.0); Samples c(1, 3.0); c = b = a;")
t("b.size()", 0, "Samples a(0, 0.0); Samples b = a;")
t("a.size()", 0, "Samples a(3, 1.5); Samples b = std::move(a);")
t("b.get(4)", 2.5, "Samples a(5, 2.5); Samples b(1, 0.0); b = a;")

P = dict(id="P-copy-samples", starter=STARTER, solution=SOLUTION, prelude=PRELUDE, tests=T, alloc=True, leak=True, mutants=MUTANTS, uncaught=UNCAUGHT)
