"""ml-int numbers (and the interp L1 logit-lens hand example). Each figure by two methods."""
import numpy as np, math, time
from fractions import Fraction as F

# ---------- logit lens hand example (interp L1): residual dim 3, vocab A, B, C
WU = np.array([[2, 0, -1], [0, 1, 1], [1, -1, 0]], float)
r0 = np.array([1, 0, 0.]); a1 = np.array([0, 1, 0.]); a2 = np.array([-1, 0, -1.])
for name, r in [('r0', r0), ('r1', r0+a1), ('r2', r0+a1+a2)]:
    lg = r@WU; p = np.exp(lg)/np.exp(lg).sum()
    lg2 = np.array([sum(r[i]*WU[i, j] for i in range(3)) for j in range(3)])
    print('logit lens %s: logits %s (loop %s) top %s p(B) %.4f' % (name, lg, lg2, 'ABC'[lg.argmax()], p[1]))
print('direct logit attribution to B: r0 %.0f a1 %.0f a2 %.0f total %.0f' % (r0@WU[:, 1], a1@WU[:, 1], a2@WU[:, 1], (r0+a1+a2)@WU[:, 1]))
# softmax of (-1, 2, 1) exactly
z = np.array([-1, 2, 1.]); print('softmax(-1,2,1) %s ; check p(B)=1/(1+e^-3+e^-1) = %.4f' % (np.round(np.exp(z)/np.exp(z).sum(), 4), 1/(1+math.exp(-3)+math.exp(-1))))

# ---------- backprop by hand (ml-int L1)
x = np.array([1., 2.]); W1 = np.array([[1., -1.], [0.5, 1.]]); w2 = np.array([2., -1.]); y = 1.0
def fwd(W1, w2):
    h = W1@x; a = np.maximum(h, 0); yh = w2@a; return 0.5*(yh-y)**2, h, a, yh
L, h, a, yh = fwd(W1, w2)
dyh = yh - y; dw2 = dyh*a; da = dyh*w2; dh = da*(h > 0); dW1 = np.outer(dh, x)
print('backprop: h %s a %s yhat %.3f L %.4f dL/dyhat %.2f dw2 %s dW1 %s' % (h, a, yh, L, dyh, dw2, dW1.tolist()))
eps = 1e-6; num = np.zeros_like(W1)
for i in range(2):
    for j in range(2):
        Wp = W1.copy(); Wp[i, j] += eps; Wm = W1.copy(); Wm[i, j] -= eps; num[i, j] = (fwd(Wp, w2)[0]-fwd(Wm, w2)[0])/(2*eps)
print('central differences dW1 %s' % np.round(num, 6).tolist())

# ---------- Adam (ml-int L1)
for g in [1e-4, 1.0, 100.0]:
    m = 0.1*g; v = 0.001*g*g; lr = 1e-3
    print('Adam first step g=%g: corrected %.6g ; uncorrected %.6g (ratio %.4f)' % (g, lr*(m/0.1)/(math.sqrt(v/0.001)+1e-8), lr*m/(math.sqrt(v)+1e-8), (m/math.sqrt(v))/1))
print('uncorrected ratio closed form 0.1/sqrt(0.001) = %.4f' % (0.1/math.sqrt(0.001)))
print('He init sd for fan_in 512: %.4f ; ln 65 %.4f ; ln 27 %.4f ; dropout scale p=0.2 %.4f' % (math.sqrt(2/512), math.log(65), math.log(27), 1/0.8))
rng = np.random.default_rng(0); q = rng.standard_normal((20000, 64)); k = rng.standard_normal((20000, 64)); dots = (q*k).sum(1)
print('dot of two N(0,I_64): sd %.3f (theory 8) ; scaled by 1/8: sd %.3f' % (dots.std(), (dots/8).std()))

# ---------- double descent: min-norm least squares on random ReLU features
def dd(seed, ps, n=40, ntest=2000, d=5, noise=0.5):
    rng = np.random.default_rng(seed); wt = rng.normal(size=d)/math.sqrt(d)
    X = rng.normal(size=(n, d)); Xt = rng.normal(size=(ntest, d))
    f = lambda Z: np.sin(Z@wt*2)
    y = f(X) + noise*rng.normal(size=n); yt = f(Xt)
    Wf = rng.normal(size=(d, max(ps)))/math.sqrt(d)
    out = []
    for p in ps:
        Phi = np.maximum(X@Wf[:, :p], 0); Pt = np.maximum(Xt@Wf[:, :p], 0)
        beta = np.linalg.pinv(Phi)@y
        out.append(np.mean((Pt@beta - yt)**2))
    return out
ps = [5, 10, 20, 30, 36, 40, 44, 60, 100, 400, 2000]
for seed in [0, 1, 2]:
    print('double descent seed %d: ' % seed + ' '.join('p=%d:%.3g' % (p, e) for p, e in zip(ps, dd(seed, ps))))
med = np.median([dd(s, ps) for s in range(20)], 0)
print('median over 20 seeds: ' + ' '.join('p=%d:%.3g' % (p, e) for p, e in zip(ps, med)))

# ---------- drills (ml-int L2)
z = np.array([1000., 1001., 1002.])
with np.errstate(over='ignore', invalid='ignore'):
    naive = np.exp(z)/np.exp(z).sum()
s = np.exp(z - z.max()); s /= s.sum()
print('naive softmax %s ; stable %s ; exact by e^-k: %s' % (naive, np.round(s, 4), np.round(np.array([math.exp(-2), math.exp(-1), 1])/(1+math.exp(-1)+math.exp(-2)), 4)))
lse = z.max() + math.log(np.exp(z - z.max()).sum()); print('logsumexp %.4f ; CE for target 0: %.4f ; for target 2: %.4f' % (lse, lse - 1000, lse - 1002))
# attention tiny: 2 tokens, d=2, causal
Q = np.array([[1., 0.], [0., 1.]]); K = np.array([[1., 1.], [0., 2.]]); Vv = np.array([[1., 0.], [0., 1.]])
S = Q@K.T/math.sqrt(2); S2 = S.copy(); S2[0, 1] = -np.inf
A = np.exp(S2 - S2.max(1, keepdims=True)); A /= A.sum(1, keepdims=True)
print('attention scores %s ; causal weights %s ; output %s' % (np.round(S, 4).tolist(), np.round(A, 4).tolist(), np.round(A@Vv, 4).tolist()))
print('row 2 by hand: softmax(1/sqrt2, 2/sqrt2) = %.4f, %.4f' % (1/(1+math.exp(1/math.sqrt(2))), 1/(1+math.exp(-1/math.sqrt(2)))))
# k-means, 6 points, k=2, init = first two points
P = np.array([[0, 0], [0, 1], [1, 0], [5, 5], [5, 6], [6, 5]], float); C = P[[0, 1]].copy()
for it in range(10):
    lab = np.argmin(((P[:, None, :]-C[None])**2).sum(2), 1); Cn = np.array([P[lab == j].mean(0) for j in range(2)])
    if np.allclose(Cn, C): break
    C = Cn
print('k-means: iterations %d centres %s labels %s inertia %.4f' % (it, C.tolist(), lab.tolist(), ((P - C[lab])**2).sum()))
print('k-means inertia by hand: cluster1 (0,0),(1,0) around (0.5,0) -> 0.5 ; cluster2 4 points around mean ...')
# linear layer backward
X = np.array([[1., 2.], [3., -1.]]); W = np.array([[1., 0., -1.], [2., 1., 0.]]); bb = np.array([0., 1., 0.]); dY = np.array([[1., 0., 2.], [-1., 1., 0.]])
print('linear backward: dX %s dW %s db %s' % ((dY@W.T).tolist(), (X.T@dY).tolist(), dY.sum(0).tolist()))
def lossfn(X, W, b): return (dY*(X@W + b)).sum()   # its gradient wrt params is exactly the backward pass
num = np.zeros_like(W)
for i in range(2):
    for j in range(3):
        Wp = W.copy(); Wp[i, j] += 1e-6; Wm = W.copy(); Wm[i, j] -= 1e-6; num[i, j] = (lossfn(X, Wp, bb)-lossfn(X, Wm, bb))/2e-6
print('dW by differences %s' % np.round(num, 6).tolist())
