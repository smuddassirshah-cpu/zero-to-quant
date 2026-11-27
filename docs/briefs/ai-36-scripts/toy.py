"""Toy models of superposition (Elhage et al. 2022) in NumPy: n features, m hidden, ReLU output.
interp L3 and ai-papers L2. Second methods: a finite-difference gradient check, and a second seed."""
import numpy as np, time

def batch(rng, B, n, S):
    x = rng.random((B, n)); x[rng.random((B, n)) < S] = 0.0; return x

def loss_grad(W, b, x, I):
    M = W.T@W; z = x@M + b; y = np.maximum(z, 0)
    e = y - x; L = np.mean(np.sum(I*e*e, 1))
    dy = 2*I*e/len(x); dz = dy*(z > 0); db = dz.sum(0); dM = x.T@dz
    dW = W@(dM + dM.T)
    return L, dW, db

def train(n, m, S, I, steps=4000, B=1024, lr=1e-2, seed=0):
    rng = np.random.default_rng(seed)
    W = rng.normal(0, np.sqrt(2/(n+m)), (m, n)); b = np.zeros(n)
    mW = np.zeros_like(W); vW = np.zeros_like(W); mb = np.zeros_like(b); vb = np.zeros_like(b)
    b1, b2, eps = 0.9, 0.999, 1e-8
    for t in range(1, steps+1):
        L, dW, db = loss_grad(W, b, batch(rng, B, n, S), I)
        mW = b1*mW + (1-b1)*dW; vW = b2*vW + (1-b2)*dW*dW
        mb = b1*mb + (1-b1)*db; vb = b2*vb + (1-b2)*db*db
        W -= lr*(mW/(1-b1**t))/(np.sqrt(vW/(1-b2**t))+eps)
        b -= lr*(mb/(1-b1**t))/(np.sqrt(vb/(1-b2**t))+eps)
    return W, b

def describe(W, b):
    norms = np.linalg.norm(W, axis=0)
    Wh = W/np.maximum(norms, 1e-12)
    interf = np.array([np.sum((Wh[:, i]@W)**2) - (Wh[:, i]@W[:, i])**2 for i in range(W.shape[1])])
    Dfeat = norms**2/np.array([np.sum((Wh[:, i]@W)**2) for i in range(W.shape[1])])
    return norms, interf, Dfeat

def eval_loss(W, b, n, S, I, seed=99, B=200000):
    rng = np.random.default_rng(seed); x = batch(rng, B, n, S); return loss_grad(W, b, x, I)[0]

if __name__ == '__main__':
    n, m = 5, 2; I = 0.9**np.arange(n)
    # gradient check
    rng = np.random.default_rng(5); W = rng.normal(size=(m, n)); b = rng.normal(size=n)*0.1; x = batch(rng, 64, n, 0.5)
    L, dW, db = loss_grad(W, b, x, I); h = 1e-6; num = np.zeros_like(W)
    for i in range(m):
        for j in range(n):
            Wp = W.copy(); Wp[i, j] += h; Wm = W.copy(); Wm[i, j] -= h
            num[i, j] = (loss_grad(Wp, b, x, I)[0]-loss_grad(Wm, b, x, I)[0])/(2*h)
    print('grad check max rel err %.2e' % (np.abs(num-dW).max()/np.abs(dW).max()))
    t0 = time.time()
    for S in [0.0, 0.7, 0.9, 0.97, 0.99]:
        for seed in [0, 1]:
            W, b = train(n, m, S, I, seed=seed)
            norms, interf, Df = describe(W, b)
            rep = int(np.sum(norms > 0.5))
            print('S=%.2f seed %d: represented %d  norms %s  sumD %.3f  b %s  loss %.5f' % (
                S, seed, rep, np.round(norms, 3), Df[norms > 0.5].sum(), np.round(b, 3), eval_loss(W, b, n, S, I)))
            if S == 0.9 and seed == 0: np.save('toy_W_090.npy', W); np.save('toy_b_090.npy', b)
            if S == 0.0 and seed == 0: np.save('toy_W_000.npy', W)
    print('time %.1f s' % (time.time()-t0))
    # learner-sized short run: 300 steps, batch 256, from seed 0, S = 0.9
    t0 = time.time(); W, b = train(n, m, 0.9, I, steps=300, B=256, seed=3); t1 = time.time()
    print('short run 300x256: loss %.5f represented %d time %.3f s' % (eval_loss(W, b, n, 0.9, I), np.sum(np.linalg.norm(W, axis=0) > 0.5), t1-t0))
    # baselines
    print('loss of W=0,b=0 at S=0.9: %.5f ; closed form %.5f' % (eval_loss(np.zeros((m, n)), np.zeros(n), n, 0.9, I), (1-0.9)*np.sum(I)/3))
