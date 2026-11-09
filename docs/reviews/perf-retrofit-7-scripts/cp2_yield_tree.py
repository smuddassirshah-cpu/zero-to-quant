"""Second read of cpp-pricing/homework-2.json h-perf-yield-tree.
Recomputes every expect by an exact binomial sum in mpmath (40 digits) with
p = (e^{(r-q)dt} - d)/(u - d) and discount e^{-r dt}, the forwards by their closed
form, the 2,000-step case against Black-Scholes with a yield (Merton); derives p
from the forward condition symbolically; runs the shipped solution, the starter,
a reader solution by another route (binomial sum with lgamma, no vector) and
reader-planted bugs with g++ and clang++ in C++17 and C++20.
Exit 0 when every expectation below holds. Run from this folder with the venv Python."""
import sys, math, re
import mpmath as mp
import sympy as sp
from cpp_harness import item, compilers, fails

mp.mp.dps = 40
IT = item("cpp-pricing", "homework-2.json", "h-perf-yield-tree")
W = IT["widget"]
BAD = []


def check(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond:
        BAD.append(msg)


# p from the forward condition: one step must price S - K at S e^{-q dt} - K e^{-r dt}
S, K, r, q, dt, u, p = sp.symbols("S K r q dt u p", positive=True)
d = 1 / u
one_step = sp.exp(-r * dt) * (p * (S * u - K) + (1 - p) * (S * d - K))
sol = sp.solve(sp.Eq(one_step, S * sp.exp(-q * dt) - K * sp.exp(-r * dt)), p)[0]
check(sp.simplify(sol - (sp.exp((r - q) * dt) - d) / (u - d)) == 0, "the forward condition gives p = (e^{(r-q)dt} - d)/(u - d), as the explain says")

PAY = {
    "Call": lambda k: (lambda x: max(x - k, 0)),
    "Put": lambda k: (lambda x: max(k - x, 0)),
    "HiddenForward": lambda k: (lambda x: x - k),
    "Strangle": lambda kp, kc: (lambda x: max(kp - x, 0) + max(x - kc, 0)),
}


def tree(f, s, r, q, sig, t, n):
    s, r, q, sig, t = map(mp.mpf, (s, r, q, sig, t))
    if t == 0:
        return f(s)
    dt = t / n
    u = mp.exp(sig * mp.sqrt(dt)); d = 1 / u
    p = (mp.exp((r - q) * dt) - d) / (u - d)
    assert 0 < p < 1
    return mp.exp(-r * t) * mp.fsum(mp.binomial(n, j) * p**j * (1 - p)**(n - j) * f(s * u**j * d**(n - j)) for j in range(n + 1))


def merton_call(s, k, r, q, sig, t):
    s, k, r, q, sig, t = map(mp.mpf, (s, k, r, q, sig, t))
    d1 = (mp.log(s / k) + (r - q + sig**2 / 2) * t) / (sig * mp.sqrt(t)); d2 = d1 - sig * mp.sqrt(t)
    return s * mp.exp(-q * t) * mp.ncdf(d1) - k * mp.exp(-r * t) * mp.ncdf(d2)


for k, c in enumerate(W["tests"], 1):
    call = c["call"]
    if call.startswith("std::vector"):
        got = [PAY["Strangle"](70, 90)(x) for x in (65.0, 80.0, 96.5)]
        check(got == c["expect"], f"test {k}: strangle values {got}")
        continue
    m = re.match(r"yield_tree_price\((\w+)\(([^)]*)\), (.*)\)$", call)
    cls, kk, rest = m.group(1), [float(x) for x in m.group(2).split(",")], [float(x) for x in m.group(3).split(",")]
    s_, r_, q_, sig_, t_, n_ = rest
    v = tree(PAY[cls](*kk), s_, r_, q_, sig_, t_, int(n_))
    e = c["expect"]
    if cls == "HiddenForward":
        cf = mp.mpf(s_) * mp.exp(-q_ * t_) - kk[0] * mp.exp(-r_ * t_)
        check(abs(v - cf) < 1e-30 and abs(mp.mpf(e) - cf) / abs(cf) < 1e-14, f"test {k}: forward {e} = tree {mp.nstr(v, 16)} = closed form {mp.nstr(cf, 16)}")
    elif c.get("tol"):
        bs = merton_call(s_, kk[0], r_, q_, sig_, t_)
        check(abs(mp.mpf(e) - bs) < 1e-13 and abs(v - bs) < 0.005,
              f"test {k}: expect {e} = Merton {mp.nstr(bs, 16)}; the 2,000-step tree {mp.nstr(v, 12)} is {float(abs(v - bs)):.1e} away (tol 0.005)")
    else:
        check(abs(mp.mpf(e) - v) / abs(v) < 1e-13, f"test {k}: expect {e} = binomial sum {mp.nstr(v, 16)}")

check(W["examples"] == W["tests"][:2], "the two examples repeat tests 1 and 2")

# put-call parity on the 4-step tree, a third route for tests 1 and 3
c4, p4 = W["tests"][0]["expect"], W["tests"][2]["expect"]
par = 80 * math.exp(-0.03 * 0.5) - 85 * math.exp(-0.04 * 0.5)
check(abs((c4 - p4) - par) < 1e-12, f"tests 1 and 3 keep parity: C - P = {c4 - p4:.12f} = S e^(-qT) - K e^(-rT) = {par:.12f}")

READER = r'''
#include <algorithm>
#include <cmath>
#include <vector>
class Strangle : public Payoff {
    double kp_, kc_;
public:
    Strangle(double put_strike, double call_strike) : kp_(put_strike), kc_(call_strike) {}
    double operator()(double x) const override { return x < kp_ ? kp_ - x : (x > kc_ ? x - kc_ : 0.0); }
};
// Binomial sum: sum_j C(n,j) p^j (1-p)^(n-j) payoff(S u^(2j-n)), weights by lgamma.
double yield_tree_price(const Payoff& f, double s, double r, double q, double sigma, double t, int n) {
    if (t <= 0) return f(s);
    double dt = t / n, h = sigma * std::sqrt(dt);
    double p = (std::exp((r - q) * dt) - std::exp(-h)) / (std::exp(h) - std::exp(-h));
    double lp = std::log(p), lq = std::log1p(-p), sum = 0;
    for (int j = 0; j <= n; ++j) {
        double lw = std::lgamma(n + 1.0) - std::lgamma(j + 1.0) - std::lgamma(n - j + 1.0) + j * lp + (n - j) * lq;
        sum += std::exp(lw) * f(s * std::exp((2 * j - n) * h));
    }
    return std::exp(-r * t) * sum;
}
'''

SOL = W["solution"]
BUGS = {
    "discount at e^{-q dt}": SOL.replace("std::exp(-r * dt)", "std::exp(-q * dt)"),
    "p from e^{(r-q)T}, whole T": SOL.replace("std::exp((r - q) * dt) - d", "std::exp((r - q) * t) - d"),
    "strangle uses the put strike for both legs": SOL.replace("std::max(spot - call_strike_, 0.0)", "std::max(spot - put_strike_, 0.0)"),
    "leaves reversed against the step back": SOL.replace("std::pow(u, j) * std::pow(d, n - j)", "std::pow(u, n - j) * std::pow(d, j)"),
    "d = 2 - u for 1/u": SOL.replace("d = 1.0 / u", "d = 2.0 - u"),
    "prepaid-forward root S e^{-qT}, growth at r": SOL.replace("double p = (std::exp((r - q) * dt) - d) / (u - d);", "double p = (std::exp(r * dt) - d) / (u - d); s = s * std::exp(-q * t);"),
}

for cxx in compilers():
    for std in ("c++17", "c++20"):
        f, res = fails(W, SOL, cxx, std)
        tmax = max(x[2] for x in res)
        check(not f, f"{cxx} {std}: shipped solution passes all 10 (slowest case {tmax:.3f} s native)")
        f, _ = fails(W, READER, cxx, std)
        check(not f, f"{cxx} {std}: reader solution (binomial sum by lgamma, no vector) passes all 10 {f}")
        f, _ = fails(W, W["starter"], cxx, std)
        check(len(f) == 10, f"{cxx} {std}: starter fails tests {f}")
        if std == "c++17":
            for name, code in BUGS.items():
                f, _ = fails(W, code, cxx, std)
                if name.startswith("prepaid"):
                    print(f"info {cxx}: '{name}' prices the forwards exactly yet fails {f} (CP2-2)")
                    check(5 not in f and 10 not in f and bool(f), f"{cxx}: prepaid-forward tree passes both forward tests and fails others")
                else:
                    check(bool(f), f"{cxx}: planted '{name}' caught by tests {f}")

print(f"\n{len(BAD)} failures")
sys.exit(1 if BAD else 0)
