"""Concept checks for puzzles L3 (lessons l13 to l18, review-3, homework-3).

Run from the repo root: python3 -I docs/reports/puzzles-L3-concepts.py
Each assert names the ledger row it supports (docs/reports/audit-puzzles-1-3-ledger.md).
Exact results use sympy or closed forms; Monte Carlo uses seeded numpy with 4-standard-error bands.
"""
from fractions import Fraction as F
from math import comb, e, exp, factorial, log, pi, sqrt

import numpy as np
import sympy as sp
from scipy import integrate

rng = np.random.default_rng(20261108)


def mc_band(p, n, k=4):
    return k * sqrt(p * (1 - p) / n)


# ------------------------------------------------------------------ l13 broken stick
def check_stick():
    L = sp.symbols("L", positive=True)
    longer = sp.integrate(2 * (1 - L) / L, (L, sp.Rational(1, 2), 1))
    assert sp.simplify(longer - (2 * sp.log(2) - 1)) == 0, "stick: break the longer piece gives 2 ln 2 - 1"
    assert abs(float(longer) - 0.3863) < 5e-5 and abs(float(longer) / 2 - 0.1931) < 5e-5
    n = 400_000
    # two uniform breaks
    x, y = rng.random(n), rng.random(n)
    a, b = np.minimum(x, y), np.maximum(x, y)
    pieces = np.stack([a, b - a, 1 - b], axis=1)
    tri = (pieces < 0.5).all(axis=1)
    assert abs(tri.mean() - 0.25) < mc_band(0.25, n), f"stick: two uniform breaks give a triangle with chance 1/4 (got {tri.mean():.4f})"
    assert abs((pieces[:, 0] < 0.5).mean() - 0.75) < mc_band(0.75, n), "stick: a named piece is under 1/2 with chance 3/4"
    assert abs(pieces.max(axis=1).mean() - 11 / 18) < 4 * 0.2 / sqrt(n), f"stick: E[longest] = 11/18 (got {pieces.max(axis=1).mean():.4f})"
    assert abs(pieces.min(axis=1).mean() - 1 / 9) < 4 * 0.1 / sqrt(n), f"stick: E[shortest] = 1/9 (got {pieces.min(axis=1).mean():.4f})"
    assert abs((pieces.argmax(axis=1) == 1).mean() - 1 / 3) < mc_band(1 / 3, n), "stick: the middle piece is longest with chance 1/3"
    assert abs(pieces[:, 1].mean() - 1 / 3) < 4 * 0.25 / sqrt(n), "stick: the middle piece averages 1/3"
    for a_ in (0.25, 0.2):
        assert abs((pieces > a_).all(axis=1).mean() - (1 - 3 * a_) ** 2) < mc_band((1 - 3 * a_) ** 2, n), f"stick: P(all pieces > {a_}) = (1 - 3a)^2"
    assert abs((pieces > 2 / 3).any(axis=1).mean() - 1 / 3) < mc_band(1 / 3, n), "stick: some desk above 2/3 with chance 1/3"
    # break the longer piece, coin, shorter
    x = rng.random(n)
    longer_piece = np.maximum(x, 1 - x)
    cut = rng.random(n) * longer_piece
    p3 = np.stack([1 - longer_piece, cut, longer_piece - cut], axis=1)
    got = (p3 < 0.5).all(axis=1).mean()
    assert abs(got - float(longer)) < mc_band(float(longer), n), f"stick: longer-piece procedure gives 2 ln 2 - 1 (got {got:.4f})"
    coin = rng.random(n) < 0.5
    piece = np.where(coin, x, 1 - x)
    cut = rng.random(n) * piece
    pc = np.stack([1 - piece, cut, piece - cut], axis=1)
    got = (pc < 0.5).all(axis=1).mean()
    assert abs(got - (log(2) - 0.5)) < mc_band(log(2) - 0.5, n), f"stick: coin procedure gives ln 2 - 1/2 (got {got:.4f})"
    shorter = np.minimum(x, 1 - x)
    cut = rng.random(n) * shorter
    ps = np.stack([1 - shorter, cut, shorter - cut], axis=1)
    assert (ps < 0.5).all(axis=1).mean() == 0, "stick: always breaking the shorter piece never gives a triangle"
    # n pieces: 1 - n/2^(n-1)
    for npieces, expect in [(4, 0.5), (5, 11 / 16), (3, 0.25)]:
        cuts = np.sort(rng.random((n, npieces - 1)), axis=1)
        sp_ = np.diff(np.concatenate([np.zeros((n, 1)), cuts, np.ones((n, 1))], axis=1), axis=1)
        got = (sp_ < 0.5).all(axis=1).mean()
        assert abs(got - expect) < mc_band(expect, n), f"stick: {npieces} pieces form a polygon with chance {expect} (got {got:.4f})"
        assert abs((sp_[:, 1] >= 0.5).mean() - 0.5 ** (npieces - 1)) < mc_band(0.5 ** (npieces - 1), n), "stick: a given spacing reaches 1/2 with chance (1/2)^(n-1)"
        assert ((sp_ >= 0.5).sum(axis=1) <= 1).all(), "stick: at most one piece can reach 1/2"
    assert abs(11 / 18 * 9 - 5.5) < 1e-12


# --------------------------------------------------------------- l14 semicircle
def in_semicircle(theta):
    s = np.sort(theta, axis=1)
    gaps = np.diff(s, axis=1)
    wrap = 2 * pi - s[:, -1] + s[:, 0]
    return np.maximum(gaps.max(axis=1), wrap) >= pi


def check_semicircle():
    n = 400_000
    for k in (2, 3, 4, 5, 6, 7):
        th = rng.random((n, k)) * 2 * pi
        got = in_semicircle(th).mean()
        expect = k / 2 ** (k - 1)
        assert abs(got - expect) < mc_band(expect, n) + 1e-12, f"semicircle: {k} points in a semicircle with chance n/2^(n-1) = {expect} (got {got:.4f})"
    assert 11 / 2**10 > 0.01 > 12 / 2**11, "semicircle: 12 is the first n below 1%"
    # triangle holds the centre iff not in a semicircle; obtuse iff in a semicircle
    th = rng.random((n, 3)) * 2 * pi
    pts = np.stack([np.cos(th), np.sin(th)], axis=2)
    sides = np.array([np.linalg.norm(pts[:, i] - pts[:, j], axis=1) for i, j in ((0, 1), (1, 2), (2, 0))]).T
    s2 = np.sort(sides**2, axis=1)
    obtuse = s2[:, 2] > s2[:, 0] + s2[:, 1]
    semi = in_semicircle(th)
    assert (obtuse == semi).mean() > 0.9999, "semicircle: obtuse exactly when the points lie in a semicircle"
    # centre inside: barycentric signs
    def contains_origin(P):
        A = np.stack([P[:, 0], P[:, 1], P[:, 2]], axis=2)  # 2 x 3 per row -> solve with the affine constraint
        res = np.empty(len(P), dtype=bool)
        for i in range(len(P)):
            M = np.vstack([P[i].T, np.ones(3)])
            lam = np.linalg.solve(M, np.array([0.0, 0.0, 1.0]))
            res[i] = (lam > 0).all()
        return res
    sub = 20_000
    inside = contains_origin(pts[:sub])
    assert (inside == ~semi[:sub]).mean() > 0.9995, "semicircle: the triangle holds the centre exactly when no semicircle holds the points"
    assert abs(inside.mean() - 0.25) < mc_band(0.25, sub), "semicircle: P(centre inside triangle) = 1/4"
    # quadrilateral on 4 points holds the centre iff not in a semicircle: 1/2
    th4 = rng.random((n, 4)) * 2 * pi
    assert abs((~in_semicircle(th4)).mean() - 0.5) < mc_band(0.5, n), "semicircle: four points: convex hull holds the centre with chance 1/2"
    # fixed half: (1/2)^3; clock window 12 of 24 hours = semicircle
    assert abs((th[:, :3] < pi).all(axis=1).mean() - 0.125) < mc_band(0.125, n), "semicircle: a fixed half holds three points with chance 1/8"


def check_sphere():
    n = 200_000
    g = rng.standard_normal((n, 4, 3))
    g /= np.linalg.norm(g, axis=2, keepdims=True)
    inside = np.empty(n, dtype=bool)
    for i in range(n):
        M = np.vstack([g[i].T, np.ones(4)])
        lam = np.linalg.solve(M, np.array([0.0, 0.0, 0.0, 1.0]))
        inside[i] = (lam > 0).all()
    assert abs(inside.mean() - 0.125) < mc_band(0.125, n), f"sphere: tetrahedron on 4 random points holds the centre with chance 1/8 (got {inside.mean():.4f})"
    wendel = 2.0 ** (1 - 4) * sum(comb(3, k) for k in range(3))
    assert abs(wendel - 7 / 8) < 1e-12, "sphere: Wendel's formula gives 7/8 for a hemisphere"


# ----------------------------------------------------------- l15 exceeding one
def irwin_hall_cdf(n, t):
    return sum((-1) ** k * comb(n, k) * max(t - k, 0) ** n for k in range(n + 1)) / factorial(n)


def check_exceed_one():
    for n_ in range(1, 7):
        assert abs(irwin_hall_cdf(n_, 1.0) - 1 / factorial(n_)) < 1e-12, "exceed_one: P(sum of n uniforms <= 1) = 1/n!"
        assert abs(irwin_hall_cdf(n_, 2.0) - (2**n_ - n_) / factorial(n_)) < 1e-12, "exceed_one: P(sum <= 2) = (2^n - n)/n!"
        assert abs(irwin_hall_cdf(n_, 0.5) - 0.5**n_ / factorial(n_)) < 1e-12, "exceed_one: P(sum <= t) = t^n/n! for t <= 1"
    tails = [1 / factorial(k) for k in range(40)]
    assert abs(sum(tails) - e) < 1e-12 and abs(sum((2 * k + 1) / factorial(k) for k in range(40)) - 3 * e) < 1e-12
    assert abs(3 * e - e**2 - 0.7658) < 5e-5 and abs(sqrt(3 * e - e**2) - 0.875) < 5e-4, "exceed_one: Var N = 3e - e^2, sd 0.875"
    assert abs(1 + sum((2**k - k) / factorial(k) for k in range(1, 60)) - (e**2 - e)) < 1e-12, "exceed_one: E[N to pass 2] = e^2 - e"
    assert abs(e**2 - e - 4.6708) < 5e-5 and abs(exp(0.5) - 1.6487) < 5e-5 and abs(exp(0.8) - 2.2255) < 5e-5
    n = 400_000
    u = rng.random((n, 30))
    cs = np.cumsum(u, axis=1)
    for t, expect in [(1.0, e), (0.5, exp(0.5)), (0.8, exp(0.8)), (2.0, e**2 - e)]:
        N = (cs <= t).sum(axis=1) + 1
        assert abs(N.mean() - expect) < 4 * N.std() / sqrt(n), f"exceed_one: E[N to pass {t}] = {expect:.4f} (got {N.mean():.4f})"
        if t == 1.0:
            assert abs(N.var() - (3 * e - e**2)) < 0.01, "exceed_one: Var N = 3e - e^2"
            assert abs((N == 2).mean() - 0.5) < mc_band(0.5, n) and abs((N == 3).mean() - 1 / 3) < mc_band(1 / 3, n) and abs((N == 4).mean() - 0.125) < mc_band(0.125, n)
            assert abs((N > 5).mean() - 1 / 120) < mc_band(1 / 120, n), "exceed_one: P(N > 5) = 1/120"
    assert abs((u[:, 0] + u[:, 1] <= 0.5).mean() - 0.125) < mc_band(0.125, n), "exceed_one: two uniforms sum to at most 1/2 with chance 1/8"
    return u, cs


def check_wald():
    n = 400_000
    u = rng.random((n, 30))
    cs = np.cumsum(u, axis=1)
    N = (cs <= 1.0).sum(axis=1) + 1
    S = cs[np.arange(n), N - 1]
    assert abs(S.mean() - e / 2) < 4 * S.std() / sqrt(n), f"wald: E[S_N] = e/2 (got {S.mean():.4f}); E[N] = e is finite so Wald applies"
    assert abs(S.mean() - 1 - 0.3591) < 0.005, "wald: mean overshoot 0.3591"
    # Finding 3 basis: a stopping time alone is not enough. Symmetric walk stopped at +1 with floor -k:
    # Wald holds (E[N] = k finite, E[S] = 0); as the floor recedes E[S_N] -> 1 while E[step] = 0 and E[N] -> infinity.
    for k in (5, 50, 500):
        p_up = k / (k + 1)
        ES = p_up * 1 + (1 - p_up) * (-k)
        assert abs(ES) < 1e-9, "wald: with a floor, E[S_N] = E[N] x 0 = 0 (Wald holds, E[N] = k finite)"
    assert abs(500 / 501 * 1 + 1 / 501 * (-500)) < 1e-9 and 500 / 501 > 0.99, "wald: without a floor the limit is E[S_N] = 1 != 0: the E[N] < infinity hypothesis is needed"


# --------------------------------------------------------------- l16 meeting
def check_meeting():
    n = 400_000
    x, y = rng.random(n) * 60, rng.random(n) * 60
    for w, expect in [(15, 7 / 16), (10, 11 / 36), (20, 5 / 9), (30, 0.75), (6, 0.19)]:
        got = (np.abs(x - y) <= w).mean()
        assert abs(got - expect) < mc_band(expect, n), f"meeting: waits of {w} minutes meet with chance {expect:.4f} (got {got:.4f})"
    # unequal waits: A waits a for B, B waits b for A: meet iff (A first and y - x <= a) or (B first and x - y <= b)
    for a, b, expect in [(10, 20, 31 / 72), (5, 25, 59 / 144), (15, 0, 7 / 32), (60, 0, 0.5)]:
        meet = ((x <= y) & (y - x <= a)) | ((y < x) & (x - y <= b))
        assert abs(meet.mean() - expect) < mc_band(expect, n), f"meeting: A waits {a}, B waits {b}: {expect:.4f} (got {meet.mean():.4f})"
    # window scaling: 15 of 120 and 6 of 30
    assert abs(1 - (1 - 15 / 120) ** 2 - 15 / 64) < 1e-12 and abs(1 - (1 - 6 / 30) ** 2 - 0.36) < 1e-12 and abs(1 - (1 - 15 / 45) ** 2 - 5 / 9) < 1e-12
    # three people each waiting a: simulate presence intervals directly
    t = rng.random((n, 3))
    for a, expect in [(0.25, 5 / 32), (1 / 6, 2 / 27)]:
        latest_arrival = t.max(axis=1)
        earliest_leave = t.min(axis=1) + a
        together = latest_arrival <= earliest_leave
        assert abs(together.mean() - expect) < mc_band(expect, n), f"meeting: three people waiting {a:.4f} of the window: {expect:.4f} (got {together.mean():.4f})"
        assert (together == (t.max(axis=1) - t.min(axis=1) <= a)).all(), "meeting: all present at some moment iff range <= a"
        assert abs(3 * a**2 - 2 * a**3 - expect) < 1e-12


# ---------------------------------------------------------------- l17 Buffon
def check_buffon():
    n = 1_000_000
    theta = rng.random(n) * pi / 2
    dist = rng.random(n) * 0.5
    for l, expect in [(1.0, 2 / pi), (0.5, 1 / pi), (1 / 3, 2 / (3 * pi)), (0.8, 1.6 / pi), (0.75, 1.5 / pi)]:
        got = (dist < l / 2 * np.sin(theta)).mean()
        assert abs(got - expect) < mc_band(expect, n), f"buffon: needle of length {l:.3f} crosses with chance 2l/pi = {expect:.4f} (got {got:.4f})"
    # whole-gap, both-lines set-up equals 2/pi; one-line set-up gives 1/pi (the trap)
    th2 = rng.random(n) * 2 * pi
    y = rng.random(n)
    half = 0.5 * np.abs(np.sin(th2))
    both = ((y < half) | (1 - y < half)).mean()
    one = (y < half).mean()
    assert abs(both - 2 / pi) < mc_band(2 / pi, n) and abs(one - 1 / pi) < mc_band(1 / pi, n), "buffon: both lines give 2/pi, one line on the whole gap gives 1/pi"
    # expected crossings for a straight needle of length L: lines at integers, centre uniform in [0,1), angle uniform
    for L_, expect in [(2.0, 4 / pi), (3.0, 6 / pi), (1.0, 2 / pi)]:
        lo = y - L_ / 2 * np.abs(np.sin(th2))
        hi = y + L_ / 2 * np.abs(np.sin(th2))
        crossings = np.floor(hi) - np.ceil(lo) + 1
        crossings = np.maximum(crossings, 0)
        assert abs(crossings.mean() - expect) < 4 * crossings.std() / sqrt(n), f"buffon: needle of length {L_} crosses {expect:.4f} lines on average (got {crossings.mean():.4f})"
    # a circle of diameter 1: span [y - 1/2, y + 1/2] holds exactly one integer -> 2 crossings always
    lo, hi = y - 0.5, y + 0.5
    circ = 2 * (np.floor(hi) - np.ceil(lo) + 1)
    assert (circ == 2).mean() > 0.99999, "buffon: a wire circle of diameter 1 crosses exactly twice"
    # pi estimate and its standard error at 10,000 drops
    p = 2 / pi
    se = (2 / p**2) * sqrt(p * (1 - p) / 10000)
    assert abs(se - 0.024) < 0.001, f"buffon: SE of the pi estimate at 10,000 drops is 0.024 (got {se:.4f})"
    assert abs((2 / p**2) * sqrt(p * (1 - p) / 100000) - 0.0075) < 0.0003
    assert abs(20000 / 6366 - 3.1417) < 5e-5 and abs(1.5 * 10000 / 4780 - 3.1381) < 5e-5 and abs(10000 * 1.5 / pi - 4775) < 1
    for l, d, band in [(1, 1, 0.0225), (0.5, 1, 0.0436), (1, 2, 0.0436), (0.6, 1, 0.0379)]:
        p = 2 * l / (pi * d)
        se = (2 * l / d) / p**2 * sqrt(p * (1 - p) / 100000)
        assert 3 * se <= band + 1e-4, f"buffon: test band {band} covers 3 SE ({3 * se:.4f}) for l = {l}, d = {d}"


def check_buffon_grid():
    n = 1_000_000
    th = rng.random(n) * 2 * pi
    for d, expect in [(1.0, 3 / pi), (2.0, 7 / (4 * pi))]:
        cx, cy = rng.random(n) * d, rng.random(n) * d
        dx, dy = 0.5 * np.abs(np.cos(th)), 0.5 * np.abs(np.sin(th))
        cross_x = (np.floor((cx + dx) / d) > np.floor((cx - dx) / d))
        cross_y = (np.floor((cy + dy) / d) > np.floor((cy - dy) / d))
        got = (cross_x | cross_y).mean()
        assert abs(got - expect) < mc_band(expect, n), f"buffon_grid: unit needle on a square grid of spacing {d} crosses some line with chance {expect:.4f} (got {got:.4f})"
        assert abs((cross_x & cross_y).mean() - 1 / (pi * d * d)) < mc_band(1 / (pi * d * d), n), "buffon_grid: crosses both families with chance l^2/(pi d^2)"


# -------------------------------------------------------- l18 expected distances
def check_distance():
    n = 400_000
    x, y = rng.random(n), rng.random(n)
    g = np.abs(x - y)
    assert abs(g.mean() - 1 / 3) < 4 * g.std() / sqrt(n), "distance: E|X - Y| = 1/3"
    assert abs((g > 0.5).mean() - 0.25) < mc_band(0.25, n), "distance: P(|X - Y| > 1/2) = 1/4"
    assert abs((g**2).mean() - 1 / 6) < 4 * (g**2).std() / sqrt(n), "distance: E[(X - Y)^2] = 1/6"
    assert np.allclose(g, np.maximum(x, y) - np.minimum(x, y)), "distance: |X - Y| = max - min pointwise"
    yv = sp.symbols("y")
    assert sp.integrate((yv**2 + (1 - yv) ** 2) / 2, (yv, 0, 1)) == sp.Rational(1, 3), "distance: conditioning on Y integrates to 1/3"
    assert abs(np.abs(x - 0.5).mean() - 0.25) < 4 * 0.15 / sqrt(n) and abs(x.mean() - 0.5) < 4 * 0.29 / sqrt(n)
    # centre of the unit square: closed form vs numerical integration
    closed = (sqrt(2) + log(1 + sqrt(2))) / 6
    num, err = integrate.dblquad(lambda v, u: sqrt((u - 0.5) ** 2 + (v - 0.5) ** 2), 0, 1, 0, 1)
    assert abs(num - closed) < 1e-7 and abs(closed - 0.3826) < 5e-5, f"distance: mean distance to the centre = 0.3826 (quadrature {num:.6f})"
    assert closed < sqrt(1 / 6) and abs(sqrt(1 / 6) - 0.4082) < 5e-5 and abs(sqrt(2 * 0.25**2) - 0.3536) < 5e-5
    # two points in the unit square: |dx| and |dy| independent with density 2(1 - t)
    closed2 = (2 + sqrt(2) + 5 * log(1 + sqrt(2))) / 15
    num2, _ = integrate.dblquad(lambda v, u: sqrt(u * u + v * v) * 4 * (1 - u) * (1 - v), 0, 1, 0, 1)
    assert abs(num2 - closed2) < 1e-7 and abs(closed2 - 0.5214) < 5e-5, f"distance: two points in the unit square are 0.5214 apart (quadrature {num2:.6f})"
    pts = rng.random((n, 4))
    d2 = np.hypot(pts[:, 0] - pts[:, 2], pts[:, 1] - pts[:, 3])
    assert abs(d2.mean() - closed2) < 4 * d2.std() / sqrt(n), "distance: Monte Carlo agrees with 0.5214"
    assert abs((d2**2).mean() - 1 / 3) < 4 * (d2**2).std() / sqrt(n), "distance: E[D^2] = 1/3 in the unit square"
    # Robbins' constant by Monte Carlo (3 SE bands in the content: sd about 0.25)
    p3 = rng.random((n, 6))
    d3 = np.sqrt(((p3[:, :3] - p3[:, 3:]) ** 2).sum(axis=1))
    assert abs(d3.mean() - 0.661707) < 4 * d3.std() / sqrt(n), f"distance: Robbins' constant 0.6617 (got {d3.mean():.4f})"
    assert abs(d2.std() - 0.248) < 0.01 and abs(d3.std() - 0.249) < 0.01 and abs(g.std() - 0.2357) < 0.01, "distance: sds behind the 3 SE test bands"
    # chord of two uniform points on the unit circle: 4/pi
    th = rng.random((n, 2)) * 2 * pi
    chord = 2 * np.abs(np.sin((th[:, 0] - th[:, 1]) / 2))
    assert abs(chord.mean() - 4 / pi) < 4 * chord.std() / sqrt(n), f"distance: mean chord = 4/pi (got {chord.mean():.4f})"
    phi = sp.symbols("phi")
    assert sp.simplify(sp.integrate(2 * sp.sin(phi / 2), (phi, 0, sp.pi)) / sp.pi - 4 / sp.pi) == 0
    # range of n uniforms: (n-1)/(n+1)
    for k, expect in [(3, 0.5), (4, 0.6), (2, 1 / 3)]:
        u = rng.random((n, k))
        r = u.max(axis=1) - u.min(axis=1)
        assert abs(r.mean() - expect) < 4 * r.std() / sqrt(n), f"distance: E[range of {k} uniforms] = {expect}"
    # slippage: distance from the midpoint of a 20p range averages 5p
    fills = 99.9 + 0.2 * rng.random(n)
    assert abs(np.abs(fills - 100).mean() - 0.05) < 4 * 0.03 / sqrt(n), "distance: slippage from the midpoint averages 5p"


if __name__ == "__main__":
    checks = [check_stick, check_semicircle, check_sphere, check_exceed_one, check_wald, check_meeting, check_buffon,
              check_buffon_grid, check_distance]
    failed = []
    for c in checks:
        try:
            c()
            print("ok", c.__name__)
        except AssertionError as err:
            failed.append(c.__name__)
            print("FAIL", c.__name__, "::", err)
    if failed:
        print("puzzles L3 concepts: FAILED", ", ".join(failed))
        raise SystemExit(1)
    print("puzzles L3 concepts: all checks passed")
