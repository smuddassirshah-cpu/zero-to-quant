"""cpp L4 h4-test-median, second read. Run from this folder: python3 cpp4_test_median.py
Reader suites that should pass (other inputs, a permutation loop), reader weak
suites that should fail a test (none from the author's seven), every hidden
slip recomputed in Python with 32-bit arithmetic, and the overlap facts."""
import itertools, json, statistics, sys
from cppharness import item, Checker, fails, COMPILERS, COURSES

it = item("cpp", "homework-4.json", "h4-test-median")
w = it["widget"]
ck = Checker()
H = "// reader suite\n"

GOOD = {
    "exact CHECKs, other inputs": H + r'''
TEST(odd_shuffled) { CHECK(median_volume({5, 3, 1, 4, 2}) == 3.0); }
TEST(even_half) { CHECK(median_volume({2, 1}) == 1.5); }
TEST(even_large) { CHECK(median_volume({2000000000, 7, 2000000000, 2000000000}) == 2000000000.0); }
TEST(empty) { CHECK(median_volume(std::vector<int>{}) == 0.0); }
''',
    "every order of one list": H + r'''
TEST(all_orders_of_six) {
    std::vector<int> v{1, 2, 3, 8, 13, 21};      // middles 3 and 8: 5.5
    std::sort(v.begin(), v.end());
    do { CHECK_CLOSE(median_volume(v), 5.5, 1e-12); } while (std::next_permutation(v.begin(), v.end()));
}
TEST(big_pair) { CHECK_CLOSE(median_volume({1500000000, 1000000000}), 1250000000.0, 1e-6); }
TEST(zero_volumes_and_empty) { CHECK(median_volume({0, 0, 0}) == 0.0); CHECK(median_volume({}) == 0.0); }
''',
    "a million volumes, shuffled": "#include <random>\n" + H + r'''
TEST(long_list) { std::vector<int> v; for (int i = 1; i <= 1000000; ++i) v.push_back(i); std::mt19937 g(7); std::shuffle(v.begin(), v.end(), g); CHECK_CLOSE(median_volume(v), 500000.5, 1e-9); }
TEST(over_int) { CHECK_CLOSE(median_volume({2000000000, 1200000000}), 1600000000.0, 1e-3); }
TEST(empty) { CHECK_CLOSE(median_volume({}), 0.0, 0.0); }
''',
}
WEAK = {
    "a reversed list as the only unsorted input (misses no sort)": H + r'''
TEST(long_list) { std::vector<int> v; for (int i = 1000000; i >= 1; --i) v.push_back(i); CHECK_CLOSE(median_volume(v), 500000.5, 1e-9); }
TEST(over_int) { CHECK_CLOSE(median_volume({2000000000, 1200000000}), 1600000000.0, 1e-3); }
TEST(empty) { CHECK_CLOSE(median_volume({}), 0.0, 0.0); }
''',
    "even list with only its middles swapped (misses no sort)": H + r'''
TEST(a) { CHECK(median_volume({1, 3, 2, 4}) == 2.5); }
TEST(b) { CHECK(median_volume({2000000000, 2000000000}) == 2000000000.0); }
TEST(c) { CHECK(median_volume({}) == 0.0); }
''',
    "even lists with equal middles (misses int division and upper middle)": H + r'''
TEST(a) { CHECK(median_volume({9, 5, 1, 5}) == 5.0); }
TEST(b) { CHECK(median_volume({3, 1, 2}) == 2.0); }
TEST(c) { CHECK(median_volume({2000000000, 2000000000}) == 2000000000.0); }
TEST(d) { CHECK(median_volume({}) == 0.0); }
''',
    "large volumes only in an odd list (misses the int sum)": H + r'''
TEST(a) { CHECK(median_volume({4, 1, 3, 2}) == 2.5); }
TEST(b) { CHECK(median_volume({2000000000, 1, 2000000000}) == 2000000000.0); }
TEST(c) { CHECK(median_volume({}) == 0.0); }
''',
    "expected value worked in int arithmetic (fails on the real median)": H + r'''
TEST(a) { CHECK(median_volume({4, 1, 3, 2}) == (2 + 3) / 2); }
TEST(b) { CHECK(median_volume({5, 9, 1}) == 5.0); }
TEST(c) { CHECK(median_volume({2000000000, 2000000000}) == 2000000000.0); }
TEST(d) { CHECK(median_volume({}) == 0.0); }
''',
    "empty list checked by size, never called": H + r'''
TEST(a) { CHECK(median_volume({4, 1, 3, 2}) == 2.5); }
TEST(b) { CHECK(median_volume({2000000000, 2000000000}) == 2000000000.0); }
TEST(c) { std::vector<int> v; CHECK(v.empty()); }
''',
}

for label, src in [("shipped solution", w["solution"])] + list(GOOD.items()):
    for cc in COMPILERS:
        fe, _ = fails(w, src, "examples", cc)
        ft, slow = fails(w, src, "tests", cc)
        ck.check(not fe and not ft, "%s on %s passes all 6 (slowest %.2f s)%s" % (label, cc, slow, "" if not ft else " FAILS %s" % ft))
for cc in COMPILERS:
    ft, _ = fails(w, w["starter"], "tests", cc)
    ck.check(ft == [1, 2, 3, 4, 5, 6], "starter fails %s on %s" % (ft, cc))
for label, src in WEAK.items():
    r = {cc: fails(w, src, "tests", cc)[0] for cc in COMPILERS}
    ck.check(all(r.values()), "weak suite %-70s fails: g++ %s, clang++ %s" % ('"%s"' % label, r["g++"], r["clang++"]))


# CPP4-2: slips 2 and 3 with the sum wrapped through unsigned (defined) give the same verdicts as the shipped prelude
import copy
w2 = copy.deepcopy(w)
OLD2 = "if (v == 2) return (s[n / 2 - 1] + s[n / 2]) / 2;"
OLD3 = "if (v == 3) return (s[n / 2 - 1] + s[n / 2]) / 2.0;"
NEW2 = "if (v == 2) return static_cast<int>(static_cast<unsigned>(s[n / 2 - 1]) + static_cast<unsigned>(s[n / 2])) / 2;"
NEW3 = "if (v == 3) return static_cast<int>(static_cast<unsigned>(s[n / 2 - 1]) + static_cast<unsigned>(s[n / 2])) / 2.0;"
ck.check(w2["prelude"].count(OLD2) == 1 and w2["prelude"].count(OLD3) == 1, "CPP4-2: slips 2 and 3 sum two ints in int (signed overflow on large volumes)")
w2["prelude"] = w2["prelude"].replace(OLD2, NEW2).replace(OLD3, NEW3)
for label, src in [("shipped solution", w["solution"])] + list(GOOD.items()) + list(WEAK.items()):
    for cc in COMPILERS:
        ck.check(fails(w, src, "tests", cc)[0] == fails(w2, src, "tests", cc)[0], "CPP4-2 wrapped prelude, same verdict on %s: %s" % (cc, label))

# the five slips in Python, 32-bit where the C++ is
def wrap(x):
    return (x + 2 ** 31) % 2 ** 32 - 2 ** 31


def med(v, slip):
    if not v:
        return "stops" if slip == 5 else 0.0
    s = list(v) if slip == 1 else sorted(v)
    n = len(s)
    if n % 2:
        return float(s[n // 2])
    a, b = s[n // 2 - 1], s[n // 2]
    if slip == 4:
        return float(b)
    if slip == 2:
        q = wrap(a + b)
        return float(int(q / 2))   # C++ int division truncates toward zero
    if slip == 3:
        return wrap(a + b) / 2.0
    return (a + b) / 2


for v, want in [([300, 100, 200], 200.0), ([700, 100, 400, 301], 350.5), ([2000000000, 1999999999], 1999999999.5), ([5000], 5000.0), ([], 0.0)]:
    ck.check(med(v, 0) == want and (not v or statistics.median(v) == want), "real median %s = %s (statistics.median agrees)" % (v, want))
caught = {k: [v for v in ([300, 100, 200], [700, 100, 400, 301], [2000000000, 1999999999], [5000], []) if med(v, k) != med(v, 0)] for k in range(1, 6)}
ck.check(all(caught.values()), "each slip differs from the real median on some shipped-solution input: %s" % {k: len(v) for k, v in caught.items()})
ck.check(wrap(2000000000 + 1999999999) == -294967297, "an int sum of 2,000,000,000 and 1,999,999,999 wraps to -294,967,297")

# overlap facts (CPP4-2)
l18 = json.loads((COURSES / "cpp" / "l18-unit-tests.json").read_text())
code_screens = [k + 1 for k, s in enumerate(l18["screens"]) if s.get("widget", {}).get("kind") == "code" and "TEST(" in (s["widget"].get("solution") or "") and "variant" in (s["widget"].get("prelude") or "")]
ck.check(code_screens == [4, 5, 10], "l18 screens where the learner writes TEST bodies against swapped versions: %s" % code_screens)
kinds = {k + 1: (s.get("type"), s.get("widget", {}).get("kind")) for k, s in enumerate(l18["screens"])}
ck.check(kinds[3] == ("problem", "numeric") and kinds[9] == ("generalise", "choice"), "l18 screens 3 and 9 are a numeric and a choice: %s %s" % (kinds[3], kinds[9]))
hw = json.loads((COURSES / "cpp" / "homework-4.json").read_text())
dd = next(i for i in hw["items"] if i["id"] == "h4-test-drawdown")
ck.check("TEST(empty_and_single_price_are_zero)" in dd["widget"]["starter"] and dd["widget"]["tests"][3]["compare"] == "raises", "h4-test-drawdown names its tests and grades an empty-input crash by raises")
print("problems:", ck.bad)
sys.exit(1 if ck.bad else 0)
