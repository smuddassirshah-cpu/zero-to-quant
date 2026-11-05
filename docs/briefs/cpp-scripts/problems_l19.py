# P-move-buffer: l19-moving-not-copying. Starter has copy members only; the learner adds the two move members.
STARTER = '''// A buffer of doubles on the heap. It copies correctly already.
// Add a move constructor and a move assignment: each takes the other buffer's block
// and leaves it empty (size 0, data() null). Neither may allocate, and both must be noexcept.
// The move assignment must be safe for `a = std::move(a)`.
class Buffer {
public:
    Buffer(int n, double x) : size_(n), data_(new double[n]) {
        for (int i = 0; i < n; ++i) data_[i] = x;
    }
    Buffer(const Buffer& other) : size_(other.size_), data_(new double[other.size_]) {
        for (int i = 0; i < size_; ++i) data_[i] = other.data_[i];
    }
    Buffer& operator=(const Buffer& other) {
        if (this != &other) {
            double* fresh = new double[other.size_];
            for (int i = 0; i < other.size_; ++i) fresh[i] = other.data_[i];
            delete[] data_;
            data_ = fresh;
            size_ = other.size_;
        }
        return *this;
    }
    ~Buffer() { delete[] data_; }

    // TODO: Buffer(Buffer&& other) noexcept
    // TODO: Buffer& operator=(Buffer&& other) noexcept

    int size() const { return size_; }
    double get(int i) const { return data_[i]; }
    const double* data() const { return data_; }

private:
    int size_;
    double* data_;
};
'''
SOLUTION = '''// A buffer of doubles on the heap. It copies correctly already.
// Add a move constructor and a move assignment: each takes the other buffer's block
// and leaves it empty (size 0, data() null). Neither may allocate, and both must be noexcept.
// The move assignment must be safe for `a = std::move(a)`.
class Buffer {
public:
    Buffer(int n, double x) : size_(n), data_(new double[n]) {
        for (int i = 0; i < n; ++i) data_[i] = x;
    }
    Buffer(const Buffer& other) : size_(other.size_), data_(new double[other.size_]) {
        for (int i = 0; i < size_; ++i) data_[i] = other.data_[i];
    }
    Buffer& operator=(const Buffer& other) {
        if (this != &other) {
            double* fresh = new double[other.size_];
            for (int i = 0; i < other.size_; ++i) fresh[i] = other.data_[i];
            delete[] data_;
            data_ = fresh;
            size_ = other.size_;
        }
        return *this;
    }
    ~Buffer() { delete[] data_; }

    Buffer(Buffer&& other) noexcept : size_(other.size_), data_(other.data_) {
        other.size_ = 0;
        other.data_ = nullptr;
    }
    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            size_ = other.size_;
            data_ = other.data_;
            other.size_ = 0;
            other.data_ = nullptr;
        }
        return *this;
    }

    int size() const { return size_; }
    double get(int i) const { return data_[i]; }
    const double* data() const { return data_; }

private:
    int size_;
    double* data_;
};
'''

def mut(old, new):
    assert old in SOLUTION, old
    return SOLUTION.replace(old, new)

MUTANTS = {
    # forgot noexcept on both: std::vector would copy on growth
    "no-noexcept": SOLUTION.replace("Buffer(Buffer&& other) noexcept", "Buffer(Buffer&& other)").replace("operator=(Buffer&& other) noexcept", "operator=(Buffer&& other)"),
    # move assignment forgets to free the old block
    "assign-leaks-old-block": mut("""            delete[] data_;
            size_ = other.size_;
            data_ = other.data_;""", """            size_ = other.size_;
            data_ = other.data_;"""),
    # no self-assignment guard
    "no-self-guard": mut("""    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            size_ = other.size_;
            data_ = other.data_;
            other.size_ = 0;
            other.data_ = nullptr;
        }
        return *this;""", """    Buffer& operator=(Buffer&& other) noexcept {
        delete[] data_;
        size_ = other.size_;
        data_ = other.data_;
        other.size_ = 0;
        other.data_ = nullptr;
        return *this;"""),
    # source keeps its pointer: two owners
    "source-not-emptied": mut("""        other.size_ = 0;
        other.data_ = nullptr;
    }
    Buffer& operator=(Buffer&&""", """    }
    Buffer& operator=(Buffer&&"""),
    # the commonest slip: the size is zeroed but the pointer is left set, so both objects delete[] one block
    "move-ctor-forgets-null": mut("""        other.size_ = 0;
        other.data_ = nullptr;
    }
    Buffer& operator=(Buffer&&""", """        other.size_ = 0;
    }
    Buffer& operator=(Buffer&&"""),
    "move-assign-forgets-null": mut("""            data_ = other.data_;
            other.size_ = 0;
            other.data_ = nullptr;
        }
        return *this;
    }

    int size()""", """            data_ = other.data_;
            other.size_ = 0;
        }
        return *this;
    }

    int size()"""),
    # a "move" that copies the block
    "move-that-copies": mut("""Buffer(Buffer&& other) noexcept : size_(other.size_), data_(other.data_) {
        other.size_ = 0;
        other.data_ = nullptr;
    }""", """Buffer(Buffer&& other) noexcept : size_(other.size_), data_(new double[other.size_]) {
        for (int i = 0; i < size_; ++i) data_[i] = other.data_[i];
        other.size_ = 0;
    }"""),
}

PRELUDE = "#include <utility>\n#include <vector>\n#include <type_traits>\n"

T = []
def t(call, expect, setup="", **kw):
    d = {"call": call, "expect": expect}
    if setup: d["setup"] = setup
    d.update(kw); T.append(d)

t("b.size()", 3, "Buffer a(3, 1.5); Buffer b = std::move(a);")
t("a.size()", 0, "Buffer a(3, 1.5); Buffer b = std::move(a);")
t("b.get(2)", 1.5, "Buffer a(3, 1.5); Buffer b = std::move(a);")
t("alloc_count()", 0, "Buffer a(1000, 2.0); reset_alloc_count(); Buffer b = std::move(a);")
t("b.size()", 4, "Buffer a(4, 1.0); Buffer b(2, 9.0); b = std::move(a);")
t("a.size()", 0, "Buffer a(4, 1.0); Buffer b(2, 9.0); b = std::move(a);")
t("alloc_count()", 0, "Buffer a(1000, 2.0); Buffer b(2, 9.0); reset_alloc_count(); b = std::move(a);")
t("a.size()", 3, "Buffer a(3, 4.0); Buffer& r = a; a = std::move(r);")
t("a.data() == nullptr", True, "Buffer a(3, 1.5); Buffer b = std::move(a);")
t("a.data() == nullptr", True, "Buffer a(4, 1.0); Buffer b(2, 9.0); b = std::move(a);")
t("std::is_nothrow_move_constructible_v<Buffer>", True)
t("std::is_nothrow_move_assignable_v<Buffer>", True)
t("alloc_count()", 2, "std::vector<Buffer> v; v.reserve(2); v.push_back(Buffer(100, 1.0)); v.push_back(Buffer(100, 2.0)); reset_alloc_count(); v.push_back(Buffer(100, 3.0));")
t("a.get(1)", 7.0, "Buffer a(3, 1.0); Buffer b = std::move(a); a = Buffer(2, 7.0);")
t("b.get(3)", 1.0, "Buffer a(4, 1.0); Buffer b(2, 9.0); b = std::move(a);")

P = dict(id="P-move-buffer", starter=STARTER, solution=SOLUTION, prelude=PRELUDE, tests=T, alloc=True, leak=True, mutants=MUTANTS)
