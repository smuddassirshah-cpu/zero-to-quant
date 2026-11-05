# P-add-overflows: l22-undefined-behaviour. The one code screen of a read-and-judge lesson: write the check so that the addition never overflows.
# The starter tests the sum after it has overflowed. It is false under every behaviour the compiler may choose
# (wrap-around gives a negative sum, folding gives false), so the starter fails whatever undefined behaviour does.
STARTER = '''#include <climits>

// Return true if a + b does not fit in an int. The check itself must never overflow.
bool add_overflows(int a, int b) {
    return a + b > INT_MAX;    // TODO: this looks at the sum after it has already overflowed
}
'''
SOLUTION = '''#include <climits>

// Return true if a + b does not fit in an int. The check itself must never overflow.
bool add_overflows(int a, int b) {
    if (b > 0) return a > INT_MAX - b;
    return a < INT_MIN - b;
}
'''
ALT = '''#include <climits>

bool add_overflows(int a, int b) {
    long long sum = static_cast<long long>(a) + b;
    return sum > INT_MAX || sum < INT_MIN;
}
'''
MUTANTS = {
    "only-checks-the-top": '''#include <climits>
bool add_overflows(int a, int b) {
    if (b > 0) return a > INT_MAX - b;
    return false;
}
''',
    "off-by-one": '''#include <climits>
bool add_overflows(int a, int b) {
    if (b > 0) return a >= INT_MAX - b;
    return a < INT_MIN - b;
}
''',
    "unsigned-wrap-guess": '''#include <climits>
bool add_overflows(int a, int b) {
    return static_cast<unsigned>(a) + static_cast<unsigned>(b) > static_cast<unsigned>(INT_MAX);
}
''',
}
PRELUDE = "#include <climits>\n"
T = []
def t(call, expect, setup="", **kw):
    d = {"call": call, "expect": expect}
    if setup: d["setup"] = setup
    d.update(kw); T.append(d)

# expected values from 64-bit arithmetic: true when a + b is above INT_MAX or below INT_MIN
def ref(a, b): return not (-2**31 <= a + b <= 2**31 - 1)
cases = [("INT_MAX", 2**31 - 1, "1", 1), ("INT_MAX", 2**31 - 1, "0", 0), ("INT_MIN", -2**31, "-1", -1), ("INT_MIN", -2**31, "0", 0),
         ("2000000000", 2000000000, "2000000000", 2000000000), ("1000", 1000, "2000", 2000), ("-2000000000", -2000000000, "-2000000000", -2000000000),
         ("INT_MAX", 2**31 - 1, "-1", -1), ("INT_MIN", -2**31, "1", 1), ("1073741824", 1073741824, "1073741824", 1073741824),
         ("1073741823", 1073741823, "1073741824", 1073741824), ("INT_MAX", 2**31 - 1, "INT_MAX", 2**31 - 1), ("INT_MIN", -2**31, "INT_MIN", -2**31)]
for sa, a, sb, b in cases:
    t(f"add_overflows({sa}, {sb})", ref(a, b))

P = dict(id="P-add-overflows", starter=STARTER, solution=SOLUTION, prelude=PRELUDE, tests=T, mutants=MUTANTS, alts={"widen-to-64-bit": ALT})
