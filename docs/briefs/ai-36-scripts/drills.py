"""ml-int L2 drill numbers: linear+ReLU backward and layer-norm backward, each against central differences.
Also the consumed-coin value for ai-safety L3 by value iteration (second method for 1 + 10 g^7)."""
import numpy as np
X = np.array([[1., 2.], [3., -1.]]); W = np.array([[1., 0., -1.], [2., 1., 0.]]); b = np.array([0., 1., 0.]); dout = np.array([[1., 0., 2.], [-1., 1., 0.]])
Z = X@W + b; mask = (Z > 0).astype(float); dZ = dout*mask
dX, dW, db = dZ@W.T, X.T@dZ, dZ.sum(0)
print('Z', Z.tolist(), 'dX', dX.tolist(), 'dW', dW.tolist(), 'db', db.tolist())
f = lambda X, W, b: (dout*np.maximum(X@W + b, 0)).sum()
def num(fun, A, h=1e-6):
    g = np.zeros_like(A)
    for idx in np.ndindex(A.shape):
        Ap = A.copy(); Ap[idx] += h; Am = A.copy(); Am[idx] -= h; g[idx] = (fun(Ap)-fun(Am))/(2*h)
    return g
print('num dX', np.round(num(lambda A: f(A, W, b), X), 6).tolist(), 'num dW', np.round(num(lambda A: f(X, A, b), W), 6).tolist())
# layer norm over the last axis
x = np.array([[1., 2., 4.], [0., -1., 3.]]); g = np.array([1.0, 0.5, 2.0]); be = np.array([0., 0.1, -0.2]); d2 = np.array([[0.5, -1., 2.], [1., 0., -0.5]]); eps = 1e-5
def ln(x, g, be):
    mu = x.mean(-1, keepdims=True); var = x.var(-1, keepdims=True); return (x-mu)/np.sqrt(var+eps)*g + be
def ln_back(x, g, dy):
    mu = x.mean(-1, keepdims=True); var = x.var(-1, keepdims=True); rs = 1/np.sqrt(var+eps); xh = (x-mu)*rs; N = x.shape[-1]
    dxh = dy*g; dx = rs*(dxh - dxh.mean(-1, keepdims=True) - xh*(dxh*xh).mean(-1, keepdims=True))
    return dx, (dy*xh).sum(0), dy.sum(0)
dx, dg, dbe = ln_back(x, g, d2)
L = lambda x, g, be: (d2*ln(x, g, be)).sum()
print('LN y', np.round(ln(x, g, be), 4).tolist())
print('LN dx', np.round(dx, 6).tolist(), 'dgamma', np.round(dg, 6).tolist(), 'dbeta', dbe.tolist())
print('num dx', np.round(num(lambda A: L(A, g, be), x), 6).tolist(), 'num dgamma', np.round(num(lambda A: L(x, A, be), g), 6).tolist())
print('row sums of dx (should be 0):', np.round(dx.sum(1), 12).tolist())
# consumed coin gridworld: state = (cell, coin_taken)
R = C = 5; START = (4, 0); GOAL = (0, 4); COIN = (4, 1); G = 0.95
ACTS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
def step(s, a): return (min(max(s[0]+a[0], 0), R-1), min(max(s[1]+a[1], 0), C-1))
V = {((r, c), t): 0.0 for r in range(R) for c in range(C) for t in (0, 1)}
for _ in range(500):
    Vn = {}
    for (s, t) in V:
        if s == GOAL: Vn[(s, t)] = 0.0; continue
        best = -1e9
        for a in ACTS:
            s2 = step(s, a); rw = 10.0*(s2 == GOAL) + (1.0 if (s2 == COIN and t == 0) else 0.0); t2 = 1 if (s2 == COIN or t == 1) else 0
            best = max(best, rw + (0 if s2 == GOAL else G*V[(s2, t2)]))
        Vn[(s, t)] = best
    V = Vn
print('consumed coin V(start) by VI %.4f ; closed form 1 + 10 g^7 = %.4f' % (V[(START, 0)], 1 + 10*G**7))
