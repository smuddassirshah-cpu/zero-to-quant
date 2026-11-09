"""Second read of cpp-pricing/homework-1.json h-perf-corridor.
Recomputes every expect with mpmath (60 digits, by the CDF and by an integral of
the density), runs the shipped solution, the starter, a reader solution by another
route and reader-planted bugs with g++ and clang++ in C++17 and C++20, and measures
how far each correct variant is from the reference (the 9-figure margin).
Also prices narrow corridors to test the prose's "every corridor".
Exit 0 when every expectation below holds. Run from this folder with the venv Python."""
import sys, math
import mpmath as mp
from cpp_harness import item, compilers, run, fails

mp.mp.dps = 60
IT = item("cpp-pricing", "homework-1.json", "h-perf-corridor")
W = IT["widget"]
BAD = []


def check(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond:
        BAD.append(msg)


def ref_price(s, lo, hi, r, sig, t, route):
    s, lo, r, sig, t = map(mp.mpf, (s, lo, r, sig, t))
    if not (lo < hi):
        return mp.mpf(0)
    drift, vol = (r - sig**2 / 2) * t, sig * mp.sqrt(t)
    z = lambda x: (-mp.inf if x == 0 else (mp.inf if x == math.inf else (mp.log(mp.mpf(x) / s) - drift) / vol))
    a, b = z(lo), z(hi)
    if route == "cdf":
        p = mp.ncdf(b) - mp.ncdf(a) if a < 0 else mp.ncdf(-a) - mp.ncdf(-b)
    else:  # integrate the density between the two points
        p = mp.quad(lambda x: mp.npdf(x), [a, b])
    return mp.exp(-r * t) * p


# 1. every expect by two routes
for k, c in enumerate(W["tests"], 1):
    call = c["call"].replace("INFINITY", "math.inf")
    name, args = call.split("(", 1)
    args = eval("[" + args.rstrip()[:-1] + "]")
    if name == "norm_cdf":
        v1 = mp.ncdf(args[0])
        v2 = mp.erfc(-mp.mpf(args[0]) / mp.sqrt(2)) / 2
    else:
        v1, v2 = ref_price(*args, "cdf"), ref_price(*args, "quad")
    e = c["expect"]
    ok = (e == 0 and v1 == 0) or abs(mp.mpf(e) - v1) / abs(v1) < 1e-15
    check(ok and (v1 == 0 or abs(v1 - v2) / abs(v1) < 1e-20), f"test {k} expect {e} = mpmath {mp.nstr(v1, 17)} (two routes)")

EX = W["examples"]
check(EX[0] == W["tests"][0] and EX[1] == W["tests"][1], "the two examples repeat tests 1 and 2; no other test is shown")

READER = r'''
#include <cmath>
// Survival function Q(x) = P(Z > x), exact in the upper tail.
static double Q(double x) { return 0.5 * std::erfc(x * M_SQRT1_2); }
double norm_cdf(double x) { return Q(-x); }
double corridor_price(double s, double lo, double hi, double r, double sigma, double t) {
    if (lo >= hi) return 0.0;
    double vol = sigma * std::sqrt(t), m = (r - sigma * sigma / 2) * t;
    // d(K): P(S_T > K) = Phi(d(K))
    double dl = lo > 0 ? (std::log(s) - std::log(lo) + m) / vol : INFINITY;
    double dh = std::isinf(hi) ? -INFINITY : (std::log(s) - std::log(hi) + m) / vol;
    double below_lo = Q(dl);              // P(S_T <= L)
    double p = below_lo < 0.5 ? Q(dh) - below_lo        // both lower tails
                              : Q(-dl) - Q(-dh);        // both upper tails
    return std::exp(-r * t) * p;
}
'''

SOL = W["solution"]
NAIVE = SOL.replace("0.5 * std::erfc(-x / std::sqrt(2.0))", "0.5 * (1 + std::erf(x / std::sqrt(2.0)))")
assert NAIVE != SOL
BUGS = {
    "Phi as 1 - erfc(x/root 2)/2 (lower tails cancel)": SOL.replace("0.5 * std::erfc(-x / std::sqrt(2.0))", "1.0 - 0.5 * std::erfc(x / std::sqrt(2.0))"),
    "discount exp(-r), no t": SOL.replace("std::exp(-r * t) * p", "std::exp(-r) * p"),
    "no drift term": SOL.replace("double drift = (r - 0.5 * sigma * sigma) * t;", "double drift = 0.0;"),
    "log(s / x) for log(x / s)": SOL.replace("std::log(lo / s)", "std::log(s / lo)").replace("std::log(hi / s)", "std::log(s / hi)"),
    "tiny prices rounded to 0": SOL.replace("return std::exp(-r * t) * p;", "double v = std::exp(-r * t) * p; return v < 1e-9 ? 0.0 : v;"),
    "float CDF (erfcf)": SOL.replace("0.5 * std::erfc(-x / std::sqrt(2.0))", "0.5 * std::erfc((float)(-x / std::sqrt(2.0f)))").replace("std::erfc((float)", "erfcf((float)"),
    "upper tails chosen when b > 0 only": SOL.replace("double p = a > 0 ?", "double p = b > 0 && a > -1 ?"),
}

for cxx in compilers():
    for std in ("c++17", "c++20"):
        f, r = fails(W, SOL, cxx, std)
        check(not f, f"{cxx} {std}: shipped solution passes all 12")
        worst = max(x[3] or 0 for x in r)
        check(worst < 1e-12, f"{cxx} {std}: shipped solution's worst relative error {worst:.1e}, under 1e-12 (1000 times inside 1e-9)")
        f, r = fails(W, READER, cxx, std)
        worst = max(x[3] or 0 for x in r)
        check(not f and worst < 1e-12, f"{cxx} {std}: reader solution (survival function, branch on P(S_T <= L) < 1/2) passes all 12, worst rel error {worst:.1e}")
        f, _ = fails(W, W["starter"], cxx, std)
        check(len(f) >= 11, f"{cxx} {std}: starter fails tests {f}")
        f, _ = fails(W, NAIVE, cxx, std)
        check({7, 8, 9, 11, 12} <= set(f), f"{cxx} {std}: naive erf CDF fails the far-tail tests {f}")
        if std == "c++17":
            for name, code in BUGS.items():
                f, _ = fails(W, code, cxx, std)
                expect_pass = name.startswith("upper tails chosen")
                if expect_pass:
                    print(f"info {cxx}: variant '{name}' fails {f} (a correct variant: both branches are accurate near the median)")
                else:
                    check(bool(f), f"{cxx}: planted '{name}' caught by tests {f}")

# 2. "9 significant figures for every corridor": narrow corridors.
NARROW = r'''
#include <cstdio>
int main() {
    double c[][6] = {{100, 140, 140.0001, 0.02, 0.1, 0.25}, {100, 140, 140.0000001, 0.02, 0.1, 0.25},
                     {100, 100, 100.0000001, 0.02, 0.1, 0.25}, {100, 60, 60.000001, 0.02, 0.1, 0.25}};
    for (auto& x : c) std::printf("%.17g\n", corridor_price(x[0], x[1], x[2], x[3], x[4], x[5]));
}
'''
import subprocess, tempfile, os
cases = [(100, 140, 140.0001, 0.02, 0.1, 0.25), (100, 140, 140.0000001, 0.02, 0.1, 0.25),
         (100, 100, 100.0000001, 0.02, 0.1, 0.25), (100, 60, 60.000001, 0.02, 0.1, 0.25)]
with tempfile.TemporaryDirectory() as tmp:
    p = os.path.join(tmp, "n")
    open(p + ".cpp", "w").write(SOL + NARROW)
    subprocess.run(["g++", "-std=c++17", "-O1", "-fno-exceptions", p + ".cpp", "-o", p], check=True)
    got = [float(x) for x in subprocess.run([p], capture_output=True, text=True).stdout.split()]
errs = []
for cse, g in zip(cases, got):
    ref = ref_price(*cse, "quad")
    e = float(abs(g - ref) / ref)
    errs.append(e)
    print(f"info narrow corridor {cse[1]} to {cse[2]}: shipped {g:.10g}, reference {mp.nstr(ref, 12)}, rel error {e:.1e}")
check(max(errs) > 1e-9, "a narrow corridor (width 1e-9 of the strike) misses 9 significant figures: 'every corridor' overstates (CP1-1)")

print(f"\n{len(BAD)} failures")
sys.exit(1 if BAD else 0)
