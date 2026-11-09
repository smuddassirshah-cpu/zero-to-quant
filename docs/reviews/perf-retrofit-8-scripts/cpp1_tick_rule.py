"""cpp L1 h-tick-rule, second read. Run from this folder: python3 cpp1_tick_rule.py
Reader solutions by other routes, reader-planted slips (none from the author's
list), and every expect recomputed by a third Python route (runs of equal
prices, sign of the last change found by itertools.groupby)."""
import itertools, sys
from cppharness import item, standard, Checker, fails

it = item("cpp", "homework-1.json", "h-tick-rule")
w = it["widget"]
ck = Checker()

HEAD = "#include <vector>\n"
R1 = HEAD + r'''
long long signed_volume(const std::vector<int>& prices, const std::vector<int>& sizes) {
    long long total = 0;
    std::size_t last = 0;            // index of the last trade whose price moved
    bool moved = false;
    for (std::size_t i = 0; i < prices.size(); ++i) {
        if (i > 0 && prices[i] != prices[i - 1]) { last = i; moved = true; }
        if (!moved) continue;
        int s = prices[last] > prices[last - 1] ? 1 : -1;
        total += s * sizes[i];        // int product fits: |s * size| <= 2e9
    }
    return total;
}
'''
R2 = HEAD + r'''
long long signed_volume(const std::vector<int>& prices, const std::vector<int>& sizes) {
    double total = 0;                 // doubles are exact for these sums (< 2^53)
    int prev = 0, sign = 0;
    for (std::size_t i = 0; i < prices.size(); ++i) {
        if (i > 0) sign = prices[i] > prev ? 1 : prices[i] < prev ? -1 : sign;
        total += sign * (double)sizes[i];
        prev = prices[i];
    }
    return (long long)total;
}
'''
SOLS = [("shipped solution", w["solution"]), ("reader: last move by index", R1), ("reader: double total", R2)]


def bug(body):
    return HEAD + "long long signed_volume(const std::vector<int>& prices, const std::vector<int>& sizes) {\n" + body + "\n}\n"


BUGS = [(l, bug(b)) for l, b in [
    ("first trade counted as a buy", "long long t = sizes.empty() ? 0 : sizes[0]; int s = 1; for (std::size_t i = 1; i < prices.size(); ++i) { if (prices[i] > prices[i-1]) s = 1; else if (prices[i] < prices[i-1]) s = -1; t += s * (long long)sizes[i]; } return t;"),
    ("leading flats take the first move's sign", "int first = 0; for (std::size_t i = 1; i < prices.size(); ++i) if (prices[i] != prices[i-1]) { first = prices[i] > prices[i-1] ? 1 : -1; break; } long long t = 0; int s = first; for (std::size_t i = 1; i < prices.size(); ++i) { if (prices[i] > prices[i-1]) s = 1; else if (prices[i] < prices[i-1]) s = -1; t += s * (long long)sizes[i]; } return t;"),
    ("zero ticks count 0 (no carry)", "long long t = 0; for (std::size_t i = 1; i < prices.size(); ++i) { int s = prices[i] > prices[i-1] ? 1 : prices[i] < prices[i-1] ? -1 : 0; t += s * (long long)sizes[i]; } return t;"),
    ("carry lasts one flat trade only", "long long t = 0; int s = 0; bool flat = false; for (std::size_t i = 1; i < prices.size(); ++i) { if (prices[i] > prices[i-1]) { s = 1; flat = false; } else if (prices[i] < prices[i-1]) { s = -1; flat = false; } else { if (flat) s = 0; flat = true; } t += s * (long long)sizes[i]; } return t;"),
    ("signs swapped (a rise is a sell)", "long long t = 0; int s = 0; for (std::size_t i = 1; i < prices.size(); ++i) { if (prices[i] > prices[i-1]) s = -1; else if (prices[i] < prices[i-1]) s = 1; t += s * (long long)sizes[i]; } return t;"),
    ("compares with the run's first price", "long long t = 0; int s = 0; std::size_t base = 0; for (std::size_t i = 1; i < prices.size(); ++i) { if (prices[i] > prices[base]) s = 1; else if (prices[i] < prices[base]) s = -1; if (prices[i] != prices[i-1]) base = i - 1; t += s * (long long)sizes[i]; } return t;"),
    ("long long product cast after the int multiply of a sum", "int run = 0; long long t = 0; int s = 0; for (std::size_t i = 1; i < prices.size(); ++i) { int ns = prices[i] > prices[i-1] ? 1 : prices[i] < prices[i-1] ? -1 : s; if (ns != s) { t += (long long)s * run; run = 0; s = ns; } run += sizes[i]; } t += (long long)s * run; return t;"),
]]

standard(w, SOLS, BUGS, ck)

# third route for every expect: runs of equal prices
def by_runs(p, s):
    total, sign, i = 0, 0, 0
    for price, grp in itertools.groupby(range(len(p)), key=lambda k: p[k]):
        idx = list(grp)
        if idx[0] > 0:
            sign = 1 if price > p[idx[0] - 1] else -1
        total += sign * sum(s[k] for k in idx)
    return total

for k, t in enumerate(w["tests"]):
    a, b = t["args"]
    ck.check(by_runs(a, b) == t["expect"], "test %d expect %d by runs of equal prices" % (k + 1, t["expect"]))
ck.check(w["examples"][0] == w["tests"][0], "the example is test 1")
ck.check("10 hidden tests" in w["how"] and len(w["tests"]) == 10, "how says 10 hidden tests")
# running totals past the int limit: which tests would an int total miss
INT = 2 ** 31 - 1
over = [k + 1 for k, t in enumerate(w["tests"]) if any(abs(by_runs(t["args"][0][:m], t["args"][1][:m])) > INT for m in range(len(t["args"][0]) + 1))]
ck.check(over == [6, 7, 10], "tests whose running total passes 2,147,483,647: %s" % over)
print("problems:", ck.bad)
sys.exit(1 if ck.bad else 0)
