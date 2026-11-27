import numpy as np, math
def dd(seed, ps, n=40, ntest=2000, d=10, noise=0.1, amp=1.0):
    rng = np.random.default_rng(seed); wt = rng.normal(size=d)/math.sqrt(d)
    X = rng.normal(size=(n, d)); Xt = rng.normal(size=(ntest, d))
    f = lambda Z: np.tanh(amp*Z@wt)
    y = f(X) + noise*rng.normal(size=n); yt = f(Xt)
    Wf = rng.normal(size=(d, max(ps)))/math.sqrt(d)
    out = []
    for p in ps:
        Phi = np.maximum(Xt[:0]@Wf[:, :p], 0)
        Phi = np.maximum(X@Wf[:, :p], 0); Pt = np.maximum(Xt@Wf[:, :p], 0)
        beta = np.linalg.pinv(Phi)@y
        # second method: lstsq (min-norm solution for underdetermined systems)
        beta2 = np.linalg.lstsq(Phi, y, rcond=None)[0]
        assert np.allclose(Phi@beta, Phi@beta2, atol=1e-6)
        out.append((np.mean((Pt@beta - yt)**2), np.mean((Pt@beta2 - yt)**2)))
    return out
ps = [5, 10, 20, 30, 36, 40, 44, 60, 100, 400, 2000]
for noise in [0.1, 0.2]:
    res = np.array([dd(s, ps, noise=noise) for s in range(20)])
    med = np.median(res[:, :, 0], 0); med2 = np.median(res[:, :, 1], 0)
    print('noise', noise, ' '.join('p=%d:%.3g/%.3g' % (p, a, b) for p, a, b in zip(ps, med, med2)))
print('variance of the target: %.3f' % np.var(np.tanh(np.random.default_rng(0).normal(size=(100000, 10))@(np.random.default_rng(0).normal(size=10)/math.sqrt(10)))))
