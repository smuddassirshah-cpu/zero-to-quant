"""Sparse autoencoder on the toy model's 2-D hidden layer (interp L3). Uses the best-of-4 S = 0.9 toy model (seed 2), which this script saves.
Second methods: finite-difference gradient check; a second seed; MMCS computed by two formulas."""
import numpy as np, time
from toy import train, batch, describe, eval_loss
n, m = 5, 2; I = 0.9**np.arange(n)

# best-of-4 seeds per sparsity, and a 1000-step learner run
for S in [0.0, 0.7, 0.9]:
    best = None
    for seed in range(4):
        W, b = train(n, m, S, I, seed=seed); L = eval_loss(W, b, n, S, I)
        if best is None or L < best[0]: best = (L, seed, W, b)
    L, seed, W, b = best; norms, _, Df = describe(W, b)
    if S == 0.9: np.save('toy_W_090_best.npy', W)
    print('best of 4 at S=%.2f: seed %d loss %.5f represented %d D %s' % (S, seed, L, np.sum(norms > 0.5), np.round(Df, 3)))
for seed in [3, 4, 5, 6]:
    t0 = time.time(); W, b = train(n, m, 0.9, I, steps=1000, B=256, seed=seed)
    norms, _, Df = describe(W, b)
    print('learner run 1000x256 seed %d: loss %.5f represented %d D %s (%.3f s)' % (seed, eval_loss(W, b, n, 0.9, I), np.sum(norms > 0.5), np.round(Df, 3), time.time()-t0))

Wt = np.load('toy_W_090_best.npy'); Fdir = Wt/np.linalg.norm(Wt, axis=0)
angles = np.sort(np.degrees(np.arctan2(Fdir[1], Fdir[0])) % 360)
print('pentagon angles', np.round(angles, 1), 'gaps', np.round(np.diff(np.r_[angles, angles[0]+360]), 1))

def sae_loss_grad(P, h, lam):
    We, be, Wd, bd = P
    pre = (h - bd)@We.T + be; f = np.maximum(pre, 0); hh = f@Wd.T + bd
    e = hh - h; B = len(h)
    L = np.mean(np.sum(e*e, 1)) + lam*np.mean(np.sum(f, 1))
    dhh = 2*e/B; dWd = dhh.T@f; dbd = dhh.sum(0); df = dhh@Wd + lam/B
    dpre = df*(pre > 0); dWe = dpre.T@(h - bd); dbe = dpre.sum(0); dbd += -(dpre@We).sum(0)
    return L, [dWe, dbe, dWd, dbd]

def train_sae(h_fn, k, lam, steps=3000, lr=3e-3, seed=0):
    rng = np.random.default_rng(seed)
    Wd = rng.normal(size=(m, k)); Wd /= np.linalg.norm(Wd, axis=0)
    P = [Wd.T.copy(), np.zeros(k), Wd, np.zeros(m)]
    mo = [np.zeros_like(p) for p in P]; vo = [np.zeros_like(p) for p in P]
    for t in range(1, steps+1):
        L, G = sae_loss_grad(P, h_fn(rng), lam)
        for i in range(4):
            mo[i] = 0.9*mo[i] + 0.1*G[i]; vo[i] = 0.999*vo[i] + 0.001*G[i]**2
            P[i] -= lr*(mo[i]/(1-0.9**t))/(np.sqrt(vo[i]/(1-0.999**t))+1e-8)
        P[2] /= np.linalg.norm(P[2], axis=0)       # unit decoder columns
    return P

def hgen(rng, B=1024): return batch(rng, B, n, 0.9)@Wt.T

# gradient check
rng = np.random.default_rng(1); k = 5
P = [rng.normal(size=(k, m)), rng.normal(size=k)*0.1, rng.normal(size=(m, k)), rng.normal(size=m)*0.1]
h = hgen(rng, 64); L, G = sae_loss_grad(P, h, 0.1); hstep = 1e-6; err = 0
for i in range(4):
    num = np.zeros_like(P[i]); it = np.nditer(P[i], flags=['multi_index'])
    for _ in it:
        idx = it.multi_index; Pp = [p.copy() for p in P]; Pm = [p.copy() for p in P]
        Pp[i][idx] += hstep; Pm[i][idx] -= hstep
        num[idx] = (sae_loss_grad(Pp, h, 0.1)[0]-sae_loss_grad(Pm, h, 0.1)[0])/(2*hstep)
    err = max(err, np.abs(num-G[i]).max()/max(np.abs(G[i]).max(), 1e-12))
print('SAE grad check max rel err %.2e' % err)

def mmcs(Wd):
    C = Fdir.T@Wd                                   # true x learned cosines
    return C.max(1).mean()

def mmcs_loop(Wd):
    tot = 0
    for i in range(n):
        tot += max(float(np.dot(Fdir[:, i], Wd[:, j])/np.linalg.norm(Wd[:, j])) for j in range(Wd.shape[1]))
    return tot/n

for k, lam in [(5, 0.03), (5, 0.1), (5, 0.3), (10, 0.1)]:
    for seed in [0, 1]:
        t0 = time.time(); P = train_sae(hgen, k, lam, seed=seed); dt = time.time()-t0
        rng = np.random.default_rng(42); hv = hgen(rng, 50000)
        f = np.maximum((hv - P[3])@P[0].T + P[1], 0); rec = np.mean(np.sum((f@P[2].T + P[3] - hv)**2, 1))
        l0 = np.mean(np.sum(f > 0, 1)); dead = int(np.sum(f.max(0) == 0))
        print('k=%d lam=%.2f seed %d: MMCS %.4f (loop %.4f) recon MSE %.5f L0 %.3f dead %d time %.2f s' % (k, lam, seed, mmcs(P[2]), mmcs_loop(P[2]), rec, l0, dead, dt))
hv = hgen(np.random.default_rng(42), 50000)
print('mean squared norm of h %.5f ; true mean number of active features %.3f' % (np.mean(np.sum(hv**2, 1)), 5*0.1))
# PCA: two directions, best cosine with each true feature
U, s, Vt = np.linalg.svd(hv - hv.mean(0), full_matrices=False)
print('PCA MMCS (2 directions, signs free) %.4f' % np.mean(np.abs(Fdir.T@Vt.T).max(1)))
