"""info level 3 (mutual information) numbers. Method A: H(X) + H(Y) - H(X,Y); method B: KL(joint || product of marginals).
The bias figures: simulation (A) against the first-order formula (k_x - 1)(k_y - 1) / (2 n ln 2) (B)."""
import math
import numpy as np

def check(label, a, b, tol=1e-9):
    ok = abs(a - b) <= tol * max(1, abs(a))
    print(('OK  ' if ok else 'FAIL'), label, a, '|', b); assert ok

def H(p):
    p = np.asarray(p, float).ravel(); p = p[p > 0]; return float(-(p * np.log2(p)).sum())
def mi_A(J):
    J = np.asarray(J, float); J = J / J.sum(); return H(J.sum(1)) + H(J.sum(0)) - H(J)
def mi_B(J):
    J = np.asarray(J, float); J = J / J.sum(); px = J.sum(1, keepdims=True); py = J.sum(0, keepdims=True)
    m = J > 0; return float((J[m] * np.log2(J[m] / (px * py)[m])).sum())

# l9: a signal and the next day's sign, joint chances
J1 = [[0.3, 0.2], [0.2, 0.3]]
check('l9 MI two ways', round(mi_A(J1), 6), round(mi_B(J1), 6))
print('l9 H(X), H(Y), H(X,Y), MI, H(Y|X):', H([0.5, 0.5]), H([0.5, 0.5]), round(H(J1), 4), round(mi_A(J1), 4), round(H(J1) - 1, 4))
J0 = [[0.25, 0.25], [0.25, 0.25]]; check('l9 independent MI = 0', round(mi_A(J0), 12), 0.0)
Jc = [[0.5, 0.0], [0.0, 0.5]]; check('l9 copy MI = 1', round(mi_A(Jc), 12), 1.0)
# a dependence with zero correlation: X in {-1, 0, 1} equally likely, Y = X^2
Jz = np.zeros((3, 2)); Jz[0, 1] = Jz[2, 1] = Jz[1, 0] = 1 / 3
xs = np.array([-1, 0, 1]); ys = np.array([0, 1])
EX = (Jz.sum(1) * xs).sum(); EY = (Jz.sum(0) * ys).sum(); EXY = sum(Jz[i, j] * xs[i] * ys[j] for i in range(3) for j in range(2))
print('l10 Y = X^2: covariance', EXY - EX * EY, 'MI', round(mi_A(Jz), 4))
check('l10 Y = X^2 MI two ways', round(mi_A(Jz), 10), round(mi_B(Jz), 10))
check('l10 Y = X^2 MI = H(Y)', round(mi_A(Jz), 10), round(H([1 / 3, 2 / 3]), 10))
# l11: a feature with a label (counts): feature = links bucket (0-1, 2-4, 5+), label spam
C = [[40, 5], [30, 25], [5, 45]]
print('l11 feature-label counts', C, 'MI bits', round(mi_A(C), 4), 'H(label)', round(H(np.array(C).sum(0) / 150), 4))
check('l11 MI two ways', round(mi_A(C), 10), round(mi_B(C), 10))
# merging two feature values cannot raise MI (data processing)
Cm = [[70, 30], [5, 45]]
print('l11 merged buckets MI', round(mi_A(Cm), 4)); check('l11 DPI merged <= original', float(mi_A(Cm) <= mi_A(C)), 1.0)
# binary symmetric chain X -> Y -> Z, flips 0.1 each
def h2(p): return H([p, 1 - p])
Ixy = 1 - h2(0.1); Ixz = 1 - h2(0.1 * 0.9 * 2)
Jxy = np.array([[0.45, 0.05], [0.05, 0.45]]); Jxz = np.array([[0.5 * 0.82, 0.5 * 0.18], [0.5 * 0.18, 0.5 * 0.82]])
check('l11 I(X;Y) two ways', round(Ixy, 10), round(mi_B(Jxy), 10)); check('l11 I(X;Z) two ways', round(Ixz, 10), round(mi_B(Jxz), 10))
print('l11 chain I(X;Y), I(X;Z):', round(Ixy, 4), round(Ixz, 4), 'combined flip', 0.18)
# l12: a weak signal. Signal S in {low, mid, high} equally likely; P(up | S) = 0.53, 0.50, 0.47 -> wait reversed is fine
pu = np.array([0.47, 0.50, 0.53]); Js = np.stack([(1 - pu) / 3, pu / 3], axis=1)
true_mi = mi_A(Js); check('l12 true MI two ways', round(true_mi, 12), round(mi_B(Js), 12))
print('l12 true MI bits', f'{true_mi:.6f}', 'nats', f'{true_mi * math.log(2):.6f}')
def plug_in(s, y, kx=3, ky=2):
    J = np.zeros((kx, ky)); np.add.at(J, (s, y), 1); return mi_A(J)
rng = np.random.default_rng(2026)
for n in (250, 1000, 5000):
    est_null = []; est_sig = []
    for _ in range(2000):
        s = rng.integers(0, 3, n)
        y0 = (rng.random(n) < 0.5).astype(int); est_null.append(plug_in(s, y0))
        y1 = (rng.random(n) < pu[s]).astype(int); est_sig.append(plug_in(s, y1))
    b_formula = (3 - 1) * (2 - 1) / (2 * n * math.log(2))
    print(f'l12 n={n}: null mean {np.mean(est_null):.5f} (formula {b_formula:.5f}); signal mean {np.mean(est_sig):.5f}, true {true_mi:.5f}, '
          f'signal mean minus formula {np.mean(est_sig) - b_formula:.5f}; share of null runs above true MI {np.mean(np.array(est_null) > true_mi):.3f}')
