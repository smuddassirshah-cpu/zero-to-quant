"""cpp L3 h-session-range, second read. Run from this folder: python3 cpp3_session_range.py
A reader solution by another layout (hidden friends, a member +=, a throw), the
reader's own slips (none from the author's sixteen), and the privacy probe
proposed in CPP3-1: a structured binding of a range, which compiles exactly when
the class has two public non-static data members and no others."""
import os, subprocess, sys, tempfile
from cppharness import item, standard, Checker, fails, results, COMPILERS

it = item("cpp", "homework-3.json", "h-session-range")
w = it["widget"]
ck = Checker()
SOL = w["solution"]

READER = r'''#include <cstdlib>
#include <ostream>
#include <stdexcept>
#include <algorithm>

template <typename T>
class SessionRange {
    T lo_, hi_;
public:
    explicit SessionRange(T first) : lo_(first), hi_(first) {}
    SessionRange(T low, T high) : lo_(low), hi_(high) {
        if (high < low) throw std::invalid_argument("low above high");
    }
    void add(T x) { lo_ = std::min(lo_, x); hi_ = std::max(hi_, x); }
    T low() const { return lo_; }
    T high() const { return hi_; }
    double width() const { return double(hi_) - double(lo_); }
    SessionRange& operator+=(const SessionRange& o) { add(o.lo_); add(o.hi_); return *this; }
    friend SessionRange operator+(const SessionRange& a, const SessionRange& b) { SessionRange c = a; c += b; return c; }
    friend bool operator==(const SessionRange& a, const SessionRange& b) { return a.lo_ == b.lo_ && a.hi_ == b.hi_; }
    friend bool operator!=(const SessionRange& a, const SessionRange& b) { return !(a == b); }
    friend std::ostream& operator<<(std::ostream& os, const SessionRange& r) { return os << "[" << r.lo_ << ", " << r.hi_ << "]"; }
};
'''


def mut(old, new, src=SOL):
    assert src.count(old) == 1, old
    return src.replace(old, new)


PUBLIC = mut("private:\n    T low_;\n    T high_;", "public:\n    T low_;\n    T high_;")
BUGS = [
    ("one-value constructor leaves the high at 0", mut("explicit SessionRange(T first) : low_(first), high_(first) {}", "explicit SessionRange(T first) : low_(first), high_(0) {}")),
    ("constructor swaps a reversed pair instead of refusing", mut("if (low_ > high_) std::abort();", "if (low_ > high_) { T t = low_; low_ = high_; high_ = t; }")),
    ("width cast to int", mut("return static_cast<double>(high_) - static_cast<double>(low_);", "return static_cast<int>(static_cast<double>(high_) - static_cast<double>(low_));")),
    ("+= adds the other high only", mut("        add(other.low_);\n        add(other.high_);", "        add(other.high_);")),
    ("== compares widths", mut("return a.low() == b.low() && a.high() == b.high();", "return a.width() == b.width();")),
    ("<< without the space", mut("<< ', ' <<".replace("'", '"'), '<< "," <<') if '<< ", " <<' in SOL else mut("<< \", \" <<", "<< \",\" <<")),
    ("two-value constructor takes int ends", mut("SessionRange(T low, T high) : low_(low), high_(high) {", "SessionRange(int low, int high) : low_(low), high_(high) {")),
]

standard(w, [("shipped solution", SOL), ("reader: hidden friends, throw", READER)], [b for b in BUGS if b[0] != "== compares widths"], ck)

# CPP3-2: "== compares widths" passes all 14 shipped tests; the proposed test 11 adds (1, 4) == (2, 5)
WIDTHS = dict(BUGS)["== compares widths"]
import copy
# w0: the item as the review found it (before the fix pass), rebuilt by undoing the two added tests if they are present
w0 = copy.deepcopy(w)
EXTRA11 = ", SessionRange<int>(1, 4) == SessionRange<int>(2, 5)}"
if w0["tests"][10]["call"].endswith(EXTRA11):
    w0["tests"][10]["call"] = w0["tests"][10]["call"][:-len(EXTRA11)] + "}"
    w0["tests"][10]["expect"] = w0["tests"][10]["expect"][:-1]
w0["tests"] = [t for t in w0["tests"] if not t.get("compiles", "").startswith("auto [a, b] = r;")]
for cc in COMPILERS:
    f, _ = fails(w0, WIDTHS, "tests", cc)
    ck.check(f == [], "CPP3-2: == by widths passes every shipped test on %s: fails %s" % (cc, f))
w2 = copy.deepcopy(w0)
t11 = w2["tests"][10]
OLD11 = "SessionRange<int>(1, 4) != SessionRange<int>(1, 4)}"
assert t11["call"].endswith(OLD11)
t11["call"] = t11["call"][:-1] + ", SessionRange<int>(1, 4) == SessionRange<int>(2, 5)}"
t11["expect"] = t11["expect"] + [0]
assert t11 == w["tests"][10], "the shipped test 11 is the proposed one"
print("proposed test 11 call:", t11["call"])
for cc in COMPILERS:
    for lab, src in [("shipped", SOL), ("reader", READER)]:
        f, _ = fails(w2, src, "tests", cc)
        ck.check(f == [], "CPP3-2 proposed test 11: %s passes on %s" % (lab, cc))
    f, _ = fails(w2, WIDTHS, "tests", cc)
    ck.check(f == [11], "CPP3-2 proposed test 11: == by widths now fails test %s on %s" % (f, cc))

# the privacy gap: the public-ends version passes all 14 shipped tests
for cc in COMPILERS:
    f, _ = fails(w0, PUBLIC, "tests", cc)
    ck.check(f == [], "public ends pass every pre-fix test on %s (the gap the item names): fails %s" % (cc, f))

# CPP3-1 probe: proposed test 15
PROBE = {"setup": "SessionRange<int> r(1);", "compiles": "auto [a, b] = r; (void)a; (void)b;", "expect": False}
EXTRA = mut("private:\n    T low_;\n    T high_;", "private:\n    T low_;\n    T high_;\n    int count_ = 1;")
for std in ["-std=c++17", "-std=c++20"]:
    for cc in COMPILERS:
        def probe(src):
            d = tempfile.mkdtemp()
            p = os.path.join(d, "p.cpp")
            open(p, "w").write(w["prelude"] + src + "\n[[maybe_unused]] static void zq_compile_probe() {\n" + PROBE["setup"] + "\n" + PROBE["compiles"] + "\n}\nint main(){}\n")
            flags = [std, "-O1", "-fsyntax-only"] + ([] if "throw" in src else ["-fno-exceptions"])
            return subprocess.run([cc, *flags, p], capture_output=True).returncode == 0
        ck.check(not probe(SOL), "%s %s: probe refused for the shipped solution (private ends)" % (cc, std))
        ck.check(not probe(READER), "%s %s: probe refused for the reader solution" % (cc, std))
        ck.check(not probe(EXTRA), "%s %s: probe refused with a third private member" % (cc, std))
        ck.check(probe(PUBLIC), "%s %s: probe compiles for public ends, so test 15 fails them" % (cc, std))

# numbers in the text and tests
ck.check(2000000000 - (-2000000000) == 4000000000 > 2 ** 31 - 1 == 2147483647, "explain: 2,000,000,000 - (-2,000,000,000) = 4,000,000,000 > 2,147,483,647")
ck.check(float(5000000000 - 4999999990) == 10.0 and 101.5 - 99.25 == 2.25 and 104 - 97 == 7, "widths 10, 2.25 and 7")
ck.check("15 hidden tests" in w["how"] and len(w["tests"]) == 15 and w["examples"][0] == w["tests"][0], "how says 15 hidden tests; the example is test 1")
for cc in COMPILERS:
    f, _ = fails(w, PUBLIC, "tests", cc)
    ck.check(f == [15], "after the fix, public ends fail test 15 only on %s: %s" % (cc, f))
print("problems:", ck.bad)
sys.exit(1 if ck.bad else 0)
