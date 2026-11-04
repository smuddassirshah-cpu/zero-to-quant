"""mock-superday-research and mock-oa-quant-data: every keyed number computed twice, and the two coding items checked.

Run: python3 -I research_mocks.py       (standard library; numpy is used only as a third check on the PCA share, and skipped if absent)
Prints one OK line per pair and ends "ALL AGREE".  Writes keys.json (family and key of every item of the three mocks,
for the freshness greps of the mock authors and the topic 3.5 exam author) and research_code_section.md (what the brief embeds).
"""
import inspect, json, math, os, random
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
KEYS = []
FAILS = []


def two(label, a, b, tol=0):
    ok = abs(a - b) <= tol
    print(f"{'OK  ' if ok else 'FAIL'} {label}: A={float(a):.6g}  B={float(b):.6g}")
    if not ok:
        FAILS.append(label)


def key(mock, item, family, value):
    KEYS.append({"mock": mock, "item": item, "family": family, "key": str(value)})


def sqrt_f(x):
    return math.sqrt(x.numerator / x.denominator)


# ====================================================================== superday-research, paper 1
def paper1():
    m = "mock-superday-research"
    # F1 two regressions: slope of y on x 0.35, of x on y 1.4
    b1, b2 = F(7, 20), F(7, 5)
    r = F(7, 10)
    two("F1 p1  |r| = sqrt(b1 b2)", F(sqrt_f(b1 * b2)).limit_denominator(1000), r)
    sx, sy = F(2), F(1)  # second route: build the pair (r, sx, sy) and read both slopes back
    two("F1 p1  slope y on x from (r, sx, sy)", r * sy / sx, b1)
    two("F1 p1  slope x on y from (r, sx, sy)", r * sx / sy, b2)
    two("F1 p2  sy/sx = b1 / r", b1 / r, F(1, 2))
    two("F1 p2  sy/sx = r / b2", r / b2, F(1, 2))
    # duplication: standard error ratio at n = 40, formula against an explicit duplicated sample
    n = 40
    ratio_formula = math.sqrt((n - 2) / (n - 1)) / math.sqrt(2)
    rng = random.Random(2801)
    xs = [rng.gauss(0, 1) for _ in range(n)]
    ys = [0.35 * x + rng.gauss(0, 1) for x in xs]

    def se(xs, ys):
        k = len(xs)
        mx, my = sum(xs) / k, sum(ys) / k
        sxx = sum((x - mx) ** 2 for x in xs)
        b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
        a = my - b * mx
        sse = sum((y - a - b * x) ** 2 for x, y in zip(xs, ys))
        return math.sqrt(sse / (k - 2) / sxx), b
    s1, bb1 = se(xs, ys)
    s2, bb2 = se(xs + xs, ys + ys)
    two("F1 p3  slope unchanged by duplication", bb1, bb2, 1e-12)
    two("F1 p3  SE ratio at n = 40 (formula, explicit duplicated sample)", ratio_formula, s2 / s1, 1e-12)
    assert round(1 - ratio_formula, 2) == 0.30
    key(m, "S1", "two-regressions", "0.7; 1/2; slope same, SE about 30% smaller")
    # F2 correlation limits: rho(A,B) 0.9, rho(B,C) -0.6, so A and C must be negatively correlated
    a, b = F(9, 10), F(-3, 5)
    prod = a * b
    root = math.sqrt(float((1 - a * a) * (1 - b * b)))
    upper = prod + root
    det = lambda x: 1 - a * a - b * b - x * x + 2 * a * b * x  # determinant of the correlation matrix
    grid = [F(i, 10000) for i in range(-10000, 10001)]
    ok = [x for x in grid if det(x) >= 0]
    two("F2  largest correlation ab + sqrt((1-a^2)(1-b^2)), grid max (exact det >= 0)", upper, float(max(ok)), 1e-4)
    two("F2  rounded to four places: -0.1913", F(round(upper * 10000), 10000), F(-1913, 10000))
    two("F2  smallest correlation, rounded: -0.8887", F(round((prod - root) * 10000), 10000), F(-8887, 10000))
    assert float(max(ok)) == -0.1913 and float(min(ok)) == -0.8887
    key(m, "S2", "correlation-limits", "-0.1913")
    # F3 special eigenvalues: M = 3I + 0.5 J, 4 by 4
    n = 4
    M = [[F(3) if i == j else F(0) for j in range(n)] for i in range(n)]
    M = [[M[i][j] + F(1, 2) for j in range(n)] for i in range(n)]

    def detf(A):
        A = [row[:] for row in A]
        d = F(1)
        for c in range(len(A)):
            p = next(i for i in range(c, len(A)) if A[i][c] != 0)
            if p != c:
                A[c], A[p] = A[p], A[c]
                d = -d
            d *= A[c][c]
            for i in range(c + 1, len(A)):
                f = A[i][c] / A[c][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[c])]
        return d
    two("F3  det(3I + J/2), eigenvalues 5, 3, 3, 3", detf(M), F(5 * 27))
    key(m, "S3", "special-eigenvalues", "135")
    # F4 multiple testing, 12 independent true nulls at 5%
    p_any = 1 - F(19, 20) ** 12
    p_sum = sum(math.comb(12, k) * F(1, 20) ** k * F(19, 20) ** (12 - k) for k in range(1, 13))
    two("F4 p1  P(at least one false positive), 12 tests", p_any, p_sum)
    print("     value", float(p_any))
    two("F4 p2  Bonferroni threshold 0.05 / 12", F(1, 20) / 12, F(1, 240))
    # the smallest p-value 0.006 against the threshold
    assert F(6, 1000) > F(1, 240) > F(4, 1000)
    key(m, "S4", "multiple-testing", "0.4596; 0.004167; not significant at 0.006")


# ====================================================================== superday-research, paper 2
def paper2():
    m = "mock-superday-research"
    # M1 ridge: Sxx 50, Sxy 100, lambda 25
    Sxx, Sxy, lam = F(50), F(100), F(25)
    closed = Sxy / (Sxx + lam)
    obj = lambda beta: (Sxx * beta * beta - 2 * Sxy * beta) + lam * beta * beta  # sum of squares minus constant, plus penalty
    grid = [F(i, 300) for i in range(0, 901)]
    best = min(grid, key=obj)
    two("M1  ridge slope Sxy / (Sxx + lambda), exact grid argmin", closed, best)
    key(m, "M1", "ridge-shrinkage", "4/3")
    # M2 lasso on an orthonormal design: soft thresholds of (3.0, 0.8, -1.5, 0.3) at 1
    b = [F(3), F(4, 5), F(-3, 2), F(3, 10)]
    lam = F(1)
    soft = [F(0) if abs(v) <= lam else v - lam * (1 if v > 0 else -1) for v in b]
    gridb = [F(i, 10) for i in range(-40, 41)]
    arg = [min(gridb, key=lambda t: (t - v) ** 2 / 2 + lam * abs(t)) for v in b]
    two("M2  sum |lasso coefficients|, soft threshold against grid argmin", sum(abs(v) for v in soft), sum(abs(v) for v in arg))
    assert sum(abs(v) for v in soft) == F(5, 2)
    key(m, "M2", "lasso-threshold", "2.5")
    # M4 PCA share of covariance [[4, 2], [2, 3]]
    tr, det = 7, 8
    l1 = (tr + math.sqrt(tr * tr - 4 * det)) / 2
    share = l1 / tr
    v = [1.0, 1.0]  # power iteration
    for _ in range(200):
        w = [4 * v[0] + 2 * v[1], 2 * v[0] + 3 * v[1]]
        nrm = math.hypot(*w)
        v = [w[0] / nrm, w[1] / nrm]
    rq = v[0] * (4 * v[0] + 2 * v[1]) + v[1] * (2 * v[0] + 3 * v[1])
    two("M4  first PC share (trace and determinant, power iteration)", share, rq / tr, 1e-12)
    try:
        import numpy as np
        two("M4  first PC share (numpy eigvalsh)", share, float(np.linalg.eigvalsh(np.array([[4.0, 2.0], [2.0, 3.0]]))[-1]) / tr, 1e-12)
    except ImportError:
        print("     numpy absent: third PCA check skipped")
    print("     value", round(share, 5))
    key(m, "M4", "pca-share", "0.7945")
    # M5 bias and variance
    A = F(1, 2) ** 2 + F(1, 4) + 1
    B = F(1, 5) ** 2 + F(16, 25) + 1
    two("M5 p1  model A: bias^2 + variance + noise", A, F(3, 2))
    two("M5 p2  model B: bias^2 + variance + noise", B, F(42, 25))
    key(m, "M5", "bias-variance", "3/2; 42/25; more data or more regularisation")
    # M6 one boosting round
    y = [F(1), F(3), F(8), F(12)]
    mean = sum(y) / 4
    res = [v - mean for v in y]

    def sse_split(r, k):
        L, R = r[:k], r[k:]
        mL, mR = sum(L) / len(L), sum(R) / len(R)
        return sum((v - mL) ** 2 for v in L) + sum((v - mR) ** 2 for v in R), mL, mR
    k = min(range(1, 4), key=lambda k: sse_split(res, k)[0])
    _, mL, mR = sse_split(res, k)
    pred = [mean + F(1, 2) * (mL if i < k else mR) for i in range(4)]
    mse = sum((a - b) ** 2 for a, b in zip(y, pred)) / 4
    two("M6  training MSE after one round, rate 1/2 (search of splits)", mse, F(13, 2))
    two("M6  by hand: errors -3, -1, 0, 4", F(9 + 1 + 0 + 16, 4), F(13, 2))
    pred1 = [mean + (mL if i < k else mR) for i in range(4)]
    two("M6  rate 1: errors -1, 1, -2, 2", sum((a - b) ** 2 for a, b in zip(y, pred1)) / 4, F(5, 2))
    two("M6  MSE before: 18.5", sum(r * r for r in res) / 4, F(37, 2))
    assert k == 2
    key(m, "M6", "boosting-round", "6.5")


# ====================================================================== superday-research, paper 3: the coding items
def weighted_line_fit(xs, ys, weights=None):
    n = len(xs)
    if n != len(ys) or (weights is not None and len(weights) != n) or n < 2:
        raise ValueError("need matching lists of at least two points")
    w = weights if weights is not None else [1.0] * n
    sw = sum(w)
    mx = sum(wi * x for wi, x in zip(w, xs)) / sw
    my = sum(wi * y for wi, y in zip(w, ys)) / sw
    sxx = sum(wi * (x - mx) ** 2 for wi, x in zip(w, xs))
    if sxx == 0:
        raise ValueError("all x values are equal")
    sxy = sum(wi * (x - mx) * (y - my) for wi, x, y in zip(w, xs, ys))
    slope = sxy / sxx
    return [slope, my - slope * mx]


def weighted_line_fit_exact(xs, ys, weights=None):  # second method: exact normal equations on Fractions
    n = len(xs)
    if n != len(ys) or (weights is not None and len(weights) != n) or n < 2:
        raise ValueError
    w = [F(1)] * n if weights is None else [F(v) for v in weights]
    x = [F(v) for v in xs]
    y = [F(v) for v in ys]
    S, Sx, Sy = sum(w), sum(a * b for a, b in zip(w, x)), sum(a * b for a, b in zip(w, y))
    Sxx, Sxy = sum(a * b * b for a, b in zip(w, x)), sum(a * b * c for a, b, c in zip(w, x, y))
    den = S * Sxx - Sx * Sx
    if den == 0:
        raise ValueError
    slope = (S * Sxy - Sx * Sy) / den
    return [float(slope), float((Sy - slope * Sx) / S)]


def weighted_line_fit_naive(xs, ys):  # the textbook sums: the wrong answer on the shifted data
    n = len(xs)
    sx, sy = sum(xs), sum(ys)
    sxx, sxy = sum(x * x for x in xs), sum(x * y for x, y in zip(xs, ys))
    slope = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    return [slope, (sy - slope * sx) / n]


def rolling_slopes(xs, ys, w):
    sx = sy = sxx = sxy = 0
    out = []
    for i in range(len(xs)):
        sx += xs[i]; sy += ys[i]; sxx += xs[i] * xs[i]; sxy += xs[i] * ys[i]
        if i >= w:
            j = i - w
            sx -= xs[j]; sy -= ys[j]; sxx -= xs[j] * xs[j]; sxy -= xs[j] * ys[j]
        if i >= w - 1:
            den = w * sxx - sx * sx
            out.append(None if den == 0 else (w * sxy - sx * sy) / den)
    return out


def rolling_float(xs, ys, w):  # a plausible learner version with float running sums
    sx = sy = sxx = sxy = 0.0
    out = []
    for i in range(len(xs)):
        sx += xs[i]; sy += ys[i]; sxx += xs[i] * xs[i]; sxy += xs[i] * ys[i]
        if i >= w:
            j = i - w
            sx -= xs[j]; sy -= ys[j]; sxx -= xs[j] * xs[j]; sxy -= xs[j] * ys[j]
        if i >= w - 1:
            den = w * sxx - sx * sx
            out.append(None if den == 0 else (w * sxy - sx * sy) / den)
    return out


def rolling_slow(xs, ys, w):  # exact, from scratch per window, on Fractions
    out = []
    for i in range(len(xs) - w + 1):
        wx, wy = [F(v) for v in xs[i:i + w]], [F(v) for v in ys[i:i + w]]
        mx, my = sum(wx) / w, sum(wy) / w
        sxx = sum((a - mx) ** 2 for a in wx)
        out.append(None if sxx == 0 else sum((a - mx) * (b - my) for a, b in zip(wx, wy)) / sxx)
    return out


def isclose(a, b, rel=1e-9):
    return abs(a - b) <= rel * max(abs(a), abs(b))


def lists_close(a, b, rel=1e-9):
    return len(a) == len(b) and all(isclose(x, y, rel) for x, y in zip(a, b))


def coding():
    out = {}
    # ---- C1: weighted_line_fit, parts 1 and 2
    t1 = [
        "weighted_line_fit([1, 2, 3, 4], [2, 3, 5, 4])", "weighted_line_fit([0, 10], [100, 200])", "weighted_line_fit([3, 1, 2], [30, 10, 25])",
        "weighted_line_fit(list(range(100000)), [3 * i + 7 for i in range(100000)])",
        "weighted_line_fit([1e8 + 3, 1e8 + 4, 1e8 + 5, 1e8 + 6], [2, 5, 4, 8])"]
    t2 = [
        "weighted_line_fit([1, 2, 3, 4], [2, 3, 5, 4], [1, 1, 1, 1])", "weighted_line_fit([0, 1, 2], [1, 3, 2], [1, 1, 4])",
        "weighted_line_fit([1, 2, 3], [2, 4, 7], [0.5, 1.0, 2.0])", "weighted_line_fit([0, 10], [5, 7], [1, 1000])"]
    raises = ["weighted_line_fit([5, 5, 5], [1, 2, 3])", "weighted_line_fit([1], [2])", "weighted_line_fit([1, 2, 3], [4, 5])"]
    raises2 = ["weighted_line_fit([1, 2, 3], [2, 4, 7], [1, 1])"]
    rows = []
    for call in t1 + t2:
        got = eval(call, {"weighted_line_fit": weighted_line_fit})
        second = eval(call, {"weighted_line_fit": weighted_line_fit_exact})
        assert lists_close(got, second), (call, got, second)
        rows.append((call, repr(got)))
    for call in raises + raises2:
        for fn in (weighted_line_fit, weighted_line_fit_exact):
            try:
                eval(call, {"weighted_line_fit": fn})
            except ValueError:
                continue
            raise AssertionError(call)
    assert len(rows) + len(raises) + len(raises2) == 13 and len(t1) + len(raises) == 8 and len(t2) + len(raises2) == 5
    shifted = eval(t1[-1], {"weighted_line_fit": weighted_line_fit})
    try:
        naive = weighted_line_fit_naive([1e8 + 3, 1e8 + 4, 1e8 + 5, 1e8 + 6], [2, 5, 4, 8])
        assert not lists_close(naive, shifted, 1e-9), (naive, shifted)
    except ZeroDivisionError:
        naive = "ZeroDivisionError"  # the textbook sums lose every digit: the denominator is exactly 0.0
    exact = weighted_line_fit_exact([F(10 ** 8 + 3), F(10 ** 8 + 4), F(10 ** 8 + 5), F(10 ** 8 + 6)], [2, 5, 4, 8])
    two("C1  shifted-data slope 1.7 (centred sums, exact Fractions)", F(shifted[0]).limit_denominator(1000), F(17, 10))
    print("     shifted intercept", repr(shifted[1]), "exact", repr(exact[1]), "naive (wrong)", repr(naive))
    two("C1  intercept: centred sums against exact", shifted[1], exact[1], abs(exact[1]) * 1e-9)
    print("     weighted 3-point slopes", [eval(c, {"weighted_line_fit": weighted_line_fit}) for c in t2[1:3]])
    out["weighted_line_fit"] = {"tests1": t1 + raises, "tests2": t2 + raises2, "expected": rows, "naive_wrong": naive, "shifted": shifted}
    key("mock-superday-research", "C1", "fit-line-weights", "see tests")
    # ---- C2: rolling_slopes
    small = [
        "rolling_slopes([1, 2, 3, 4, 5], [2, 4, 5, 4, 5], 3)", "rolling_slopes([1, 2, 3], [2, 4, 7], 3)", "rolling_slopes([1, 2, 3], [2, 4, 7], 4)",
        "rolling_slopes([0, 1, 2, 3], [5, 5, 5, 5], 2)", "rolling_slopes([4, 2, 9, 1, 7, 3], [8, 1, 6, 2, 9, 5], 2)",
        "[s is None for s in rolling_slopes([1, 1, 1, 2, 3], [1, 2, 3, 4, 9], 3)]", "len(rolling_slopes(list(range(10)), list(range(10)), 10))"]
    rows2 = []
    for call in small:
        got = eval(call, {"rolling_slopes": rolling_slopes})
        slow = eval(call, {"rolling_slopes": lambda a, b, c: [None if v is None else float(v) for v in rolling_slow(a, b, c)]})
        if isinstance(got, list) and got and isinstance(got[0], (float, int)) and not isinstance(got[0], bool):
            assert lists_close(got, slow), (call, got, slow)
        else:
            assert got == slow, (call, got, slow)
        rows2.append((call, repr(got)))
    XS = [i % 10 for i in range(200000)]
    YS = [(i * i) % 97 for i in range(200000)]
    big = sum(rolling_slopes(XS, YS, 1000))
    # second method: exact Fractions from scratch on every 4,000th window, and the exact total from integer window sums
    full = rolling_slopes(XS, YS, 1000)
    for i in range(0, len(full), 4000):
        sl = rolling_slow(XS[i:i + 1000], YS[i:i + 1000], 1000)[0]
        assert isclose(full[i], float(sl), 1e-12), i
    # exact total: the slope of window i from integer sums as a Fraction
    tot = F(0)
    sx = sy = sxx = sxy = 0
    for i in range(200000):
        sx += XS[i]; sy += YS[i]; sxx += XS[i] ** 2; sxy += XS[i] * YS[i]
        if i >= 1000:
            j = i - 1000
            sx -= XS[j]; sy -= YS[j]; sxx -= XS[j] ** 2; sxy -= XS[j] * YS[j]
        if i >= 999:
            tot += F(1000 * sxy - sx * sy, 1000 * sxx - sx * sx)
    two("C2  sum of 199,001 slopes (float running sums, exact Fractions)", big, float(tot), abs(big) * 1e-12)
    assert len(full) == 199001
    rows2.append(("sum(rolling_slopes([i % 10 for i in range(200000)], [(i * i) % 97 for i in range(200000)], 1000))", repr(big)))
    A = list(range(200000))
    B = [2 * i + 1 for i in A]
    last = rolling_slopes(A, B, 50000)[-1]
    fl = rolling_float(A, B, 50000)
    assert isclose(last, 2.0, 1e-12) and isclose(fl[-1], 2.0, 1e-6), (last, fl[-1])
    assert isclose(sum(rolling_float(XS, YS, 1000)), big, 1e-9)  # a float-sum learner version passes the sum test
    print("     float running-sum version, last slope", repr(fl[-1]), "(passes at rel 1e-6)")
    assert len(rolling_slopes(A, [i % 7 for i in A], 50000)) == 150001
    rows2.append(("rolling_slopes(list(range(200000)), [2 * i + 1 for i in range(200000)], 50000)[-1]", "2.0"))
    rows2.append(("len(rolling_slopes(list(range(200000)), [i % 7 for i in range(200000)], 50000))", "150001"))
    assert len(rows2) == 10
    out["rolling_slopes"] = {"expected": rows2}
    key("mock-superday-research", "C2", "rolling-slope", "see tests")
    return out


# ====================================================================== superday-research, paper 4: the open case
def phi_upper(z):  # P(Z > z) by erfc, and by Simpson integration of the density
    return 0.5 * math.erfc(z / math.sqrt(2))


def simpson_upper(z, top=12.0, n=20000):
    h = (top - z) / n
    f = lambda t: math.exp(-t * t / 2) / math.sqrt(2 * math.pi)
    s = f(z) + f(top) + sum((4 if i % 2 else 2) * f(z + i * h) for i in range(1, n))
    return s * h / 3


def case():
    m = "mock-superday-research"
    hit, n = 0.523, 1000
    z = (hit - 0.5) / math.sqrt(0.25 / n)
    p2 = 2 * phi_upper(z)
    two("Case 1  z for a 52.3% hit rate in 1,000 days", z, 0.023 / math.sqrt(0.00025), 1e-12)
    two("Case 1  two-sided p (erfc, Simpson)", p2, 2 * simpson_upper(z), 1e-9)
    print("     z", round(z, 4), "p", round(p2, 4))
    se = math.sqrt(0.25 / n)
    lo, hi = hit - 1.96 * math.sqrt(hit * (1 - hit) / n), hit + 1.96 * math.sqrt(hit * (1 - hit) / n)
    print("     95% interval for the hit rate", round(lo, 4), round(hi, 4), "half-width", round(1.96 * se, 4))
    # Case 2: r = 0.04 over n = 1,000 days
    r, N = 0.04, 1000
    t = r * math.sqrt(N - 2) / math.sqrt(1 - r * r)
    t_exact = float(F(4, 100) * F(math.isqrt(998 * 10 ** 12), 10 ** 6) / F(math.isqrt((1 - F(16, 10000)).numerator * 10 ** 12 // (1 - F(16, 10000)).denominator), 10 ** 6))
    two("Case 2  t statistic of r = 0.04, n = 1,000", t, t_exact, 1e-6)
    zf = math.atanh(r)
    two("Case 2  atanh(0.04) against its series", zf, r + r ** 3 / 3 + r ** 5 / 5 + r ** 7 / 7, 1e-12)
    half = 1.96 / math.sqrt(N - 3)
    lo, hi = math.tanh(zf - half), math.tanh(zf + half)
    two("Case 2  tanh(z) against (e^2z - 1)/(e^2z + 1) at the upper end", hi, (math.exp(2 * (zf + half)) - 1) / (math.exp(2 * (zf + half)) + 1), 1e-12)
    print("     t", round(t, 3), "95% interval for r", round(lo, 4), round(hi, 4), "R2", r * r)
    assert lo < 0 < hi and t < 1.96
    key(m, "Case1", "open-case-hit-rate", f"z {z:.3f}, p {p2:.3f}")
    key(m, "Case2", "open-case-signal", f"t {t:.3f}, interval {lo:.4f} to {hi:.4f}")
    return {"case1_z": z, "case1_p": p2, "case2_t": t, "case2_lo": lo, "case2_hi": hi}


# ====================================================================== quant-data statistics paper
def qd_stats():
    m = "mock-oa-quant-data"
    two("Q1  half-width 1.96 x 12 / sqrt(36)", F(196, 100) * 12 / 6, F(98, 25))
    two("Q1  via the variance of the mean sqrt(144 / 36)", math.sqrt(144 / 36) * 1.96, 3.92, 1e-12)
    key(m, "Q1", "standard-error", "3.92")
    two("Q3  t = mean / (s / sqrt(n)) = 1.8 / (5 / 5)", F(18, 10) / (F(5) / 5), F(9, 5))
    two("Q3  t squared = n mean^2 / s^2", F(25) * F(18, 10) ** 2 / 25, F(9, 5) ** 2)
    key(m, "Q3", "t-statistic", "1.8")
    adj = 1 - (1 - F(2, 5)) * F(49, 45)
    two("Q5  adjusted R^2, n = 50, k = 4, R^2 = 0.4", adj, F(2, 5) - (1 - F(2, 5)) * F(4, 45))
    two("Q5  value 26/75", adj, F(26, 75))
    key(m, "Q5", "adjusted-r2", "0.3467")
    # Q6 conditional mean and sd of Y given X = 5 (mu_x 1, mu_y 4, sd_x 3, sd_y 2, rho 0.6)
    mx, my, sx, sy, rho, x = F(1), F(4), F(3), F(2), F(3, 5), F(5)
    cov = rho * sx * sy
    cm = my + cov / (sx * sx) * (x - mx)
    cv = sy * sy - cov * cov / (sx * sx)
    # second route: the matrix form S_yx S_xx^-1 (a 1 by 1 inverse here), and the residual of a regression line
    cm2 = my + (cov * (1 / (sx * sx))) * (x - mx)
    cv2 = (sy * sy) - cov * (1 / (sx * sx)) * cov
    two("Q6 p1  E[Y | X = 5]", cm, cm2)
    two("Q6 p1  value 28/5", cm, F(28, 5))
    two("Q6 p2  Var[Y | X = 5] = sy^2 (1 - rho^2)", cv, cv2)
    two("Q6 p2  sd 1.6 exactly: 1.6^2 = 2.56", cv, F(16, 10) ** 2)
    key(m, "Q6", "bivariate-normal", "5.6; 1.6")
    # Q7 portfolio sd: weights 0.6, 0.4; sds 0.2, 0.3; correlation -0.3
    w1, w2, s1, s2, c = F(3, 5), F(2, 5), F(1, 5), F(3, 10), F(-3, 10)
    v1 = w1 ** 2 * s1 ** 2 + w2 ** 2 * s2 ** 2 + 2 * w1 * w2 * c * s1 * s2
    S = [[s1 * s1, c * s1 * s2], [c * s1 * s2, s2 * s2]]
    v2 = sum([w1, w2][i] * S[i][j] * [w1, w2][j] for i in range(2) for j in range(2))
    two("Q7  portfolio variance, expanded and as w'Sw", v1, v2)
    two("Q7  variance 0.02016", v1, F(2016, 100000))
    print("     sd", round(sqrt_f(v1), 4))
    key(m, "Q7", "portfolio-sd", "0.1420")
    # Q8 minimum-variance weight in asset 1: variances 1/16 and 1/25, covariance 3/200
    a, b, cc = F(1, 16), F(1, 25), F(3, 200)
    w = (b - cc) / (a + b - 2 * cc)
    var = lambda t: t * t * a + (1 - t) ** 2 * b + 2 * t * (1 - t) * cc
    best = min([F(i, 290) for i in range(0, 291)], key=var)
    two("Q8  min-variance weight (closed form, exact grid argmin)", w, best)
    two("Q8  value 10/29", w, F(10, 29))
    print("     value", round(float(w), 4))
    key(m, "Q8", "min-variance-weight", "0.3448")
    # Q10 compound Poisson: lambda 4, size mean 10 sd 5
    lam, mu, sd = 4, 10, 5
    closed = lam * (sd ** 2 + mu ** 2)
    pn = lambda k: math.exp(-lam) * lam ** k / math.factorial(k)
    EN = sum(k * pn(k) for k in range(80))
    ES = EN * mu
    ES2 = sum(pn(k) * (k * sd ** 2 + (k * mu) ** 2) for k in range(80))
    two("Q10 Var(total) = lambda (sd^2 + mu^2), by the sum over N", closed, ES2 - ES ** 2, 1e-9)
    key(m, "Q10", "compound-poisson", "500")


def q4():
    """Q4 facts about least squares with an intercept, on exact Fractions."""
    xs, ys = [F(v) for v in (1, 2, 4, 5, 8)], [F(v) for v in (3, 4, 8, 7, 13)]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    a = my - b * mx
    two("Q4  residuals of a 5-point fit sum to zero", sum(y - a - b * x for x, y in zip(xs, ys)), 0)
    two("Q4  the fitted line passes through the point of means", a + b * mx, my)

    def sse(cols, y):  # exact normal equations, intercept included; None if the columns are collinear
        X = [[F(1)] + [c[i] for c in cols] for i in range(len(y))]
        k = len(X[0])
        A = [[sum(r[i] * r[j] for r in X) for j in range(k)] + [sum(r[i] * v for r, v in zip(X, y))] for i in range(k)]
        for c in range(k):
            piv = next((r for r in range(c, k) if A[r][c] != 0), None)
            if piv is None:
                return None
            A[c], A[piv] = A[piv], A[c]
            A[c] = [v / A[c][c] for v in A[c]]
            for r in range(k):
                if r != c and A[r][c] != 0:
                    f = A[r][c]
                    A[r] = [u - f * v for u, v in zip(A[r], A[c])]
        beta = [A[i][k] for i in range(k)]
        return sum((v - sum(bi * xi for bi, xi in zip(beta, r))) ** 2 for r, v in zip(X, y))

    rng = random.Random(2802)
    fits = fell = 0
    for _ in range(2000):
        n = 8
        y = [F(rng.randint(0, 9)) for _ in range(n)]
        c1 = [F(rng.randint(0, 9)) for _ in range(n)]
        c2 = [F(rng.randint(0, 9)) for _ in range(n)]
        s1, s2 = sse([c1], y), sse([c1, c2], y)
        sst = sum((v - sum(y) / n) ** 2 for v in y)
        if s1 is None or s2 is None or sst == 0:
            continue
        fits += 1
        assert s2 <= s1  # R^2 = 1 - SSE/SST cannot fall when a column is added
        adj = lambda sse_, k: 1 - (sse_ / (n - k - 1)) / (sst / (n - 1))
        if adj(s2, 2) < adj(s1, 1):
            fell += 1
    assert fits > 1500 and fell > 50
    print(f"OK   Q4  R^2 never fell in {fits} exact fits; adjusted R^2 fell in {fell} of them")
    key("mock-oa-quant-data", "Q4", "ols-facts", "residuals sum to zero; line through the means; R2 cannot fall")


def main():
    paper1()
    paper2()
    coding_out = coding()
    case_out = case()
    qd_stats()
    q4()
    # embed
    md = []
    def table(title, calls, expected, note):
        md.append(f"{title}\n")
        md.append("| # | Call | Expected | Compare |\n| --- | --- | --- | --- |")
        for i, c in enumerate(calls, 1):
            if c in expected:
                e = expected[c]
                cmp_ = "equal" if (e in ("[]", "150001") or e.startswith("[True") or e.startswith("[False") or e.isdigit() or e == "1") else "isclose, tol rel 1e-9 and abs 1e-9"
                if c.startswith("rolling_slopes(list(range(200000)), [2 * i"):
                    cmp_ = "isclose, tol rel 1e-6"
                md.append(f"| {i} | `{c}` | `{e if len(e) < 60 else e[:57] + '...'}` | {cmp_} |")
            else:
                md.append(f"| {i} | `{c}` | raises `ValueError` | raises |")
        md.append("")
    md.append(f"Reference `weighted_line_fit` (parts 1 and 2; part 1 starts without `weights`):\n\n```python\n{inspect.getsource(weighted_line_fit)}```\n")
    exp1 = dict(coding_out["weighted_line_fit"]["expected"])
    table("Part 1 hidden tests (`weighted_line_fit(xs, ys)`):", coding_out["weighted_line_fit"]["tests1"], exp1, "")
    table("Part 2 adds these hidden tests (the part 1 tests run too, 13 in all):", coding_out["weighted_line_fit"]["tests2"], exp1, "")
    md.append(f"Reference `rolling_slopes`:\n\n```python\n{inspect.getsource(rolling_slopes)}```\n")
    exp2 = dict(coding_out["rolling_slopes"]["expected"])
    table("Hidden tests:", list(exp2), exp2, "")
    open(os.path.join(HERE, "research_code_section.md"), "w").write("\n".join(md))
    json.dump({"keys": KEYS, "coding": coding_out, "case": case_out}, open(os.path.join(HERE, "keys.json"), "w"), indent=1)
    print("ALL AGREE" if not FAILS else f"FAILURES: {FAILS}")
    raise SystemExit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
