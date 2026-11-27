"""Composition scores (Elhage et al. 2021) for the hand-built induction model. Second method: einsum-free loop for one pair."""
import numpy as np
from induction import build, D
W = build(0)
def qk(h): Q, K, V, O = h; return Q@K.T
def ov(h): Q, K, V, O = h; return V@O
fro = np.linalg.norm
def score(A, B): return fro(A@B)/(fro(A)*fro(B))
for i, h1 in enumerate(W['heads'][0]):
    for j, h2 in enumerate(W['heads'][1]):
        print('L0H%d -> L1H%d: K-comp %.4f Q-comp %.4f V-comp %.4f' % (i, j, score(ov(h1), qk(h2).T), score(ov(h1), qk(h2)), score(ov(h1), ov(h2))))
rng = np.random.default_rng(0)
base = [score(rng.normal(size=(D, D)), rng.normal(size=(D, D))) for _ in range(200)]
print('random DxD baseline %.4f' % np.mean(base))
# second method for K-comp L0H0 -> L1H0 by explicit sums
A = ov(W['heads'][0][0]); B = qk(W['heads'][1][0]).T
num = np.sqrt(sum(sum(A[r, k]*B[k, c] for k in range(D))**2 for r in range(D) for c in range(D)))
den = np.sqrt((A*A).sum())*np.sqrt((B*B).sum())
print('loop K-comp L0H0 -> L1H0 %.4f' % (num/den))
