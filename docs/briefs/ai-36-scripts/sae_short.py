"""Supplied SAE (best of 4 seeds by held-out SAE loss, not by the hidden truth) and short learner runs.
Reuses the functions of sae.py on the best-of-4 S = 0.9 toy model. Run sae.py first (it saves that model)."""
import numpy as np, time, re
src = open('sae.py').read()
head = src.split('# gradient check')[0]
head = re.sub(r"# best-of-4 seeds.*?(?=Wt = np.load)", "", head, flags=re.S)
g = {}; exec(head, g)
Fdir = g['Fdir']
mmcs = lambda Wd: (Fdir.T@Wd).max(1).mean()
hv = g['hgen'](np.random.default_rng(42), 50000)
def held_loss(P, lam=0.3):
    f = np.maximum((hv - P[3])@P[0].T + P[1], 0); return np.mean(np.sum((f@P[2].T + P[3] - hv)**2, 1)) + lam*np.mean(f.sum(1))
res = []
for seed in range(4):
    P = g['train_sae'](g['hgen'], 5, 0.3, seed=seed); res.append((held_loss(P), seed, mmcs(P[2])))
    print('full run seed %d: held-out loss %.5f MMCS %.4f' % (seed, res[-1][0], res[-1][2]))
best = min(res); print('kept seed %d (lowest held-out loss): MMCS %.4f' % (best[1], best[2]))
for seed in range(4):
    t0 = time.time(); P = g['train_sae'](lambda r: g['hgen'](r, 256), 5, 0.3, steps=500, lr=1e-2, seed=seed)
    print('short 500 x 256 lr 0.01 seed %d: MMCS %.4f held-out loss %.5f (%.3f s)' % (seed, mmcs(P[2]), held_loss(P), time.time()-t0))
