import numpy as np
from toy import train, eval_loss
def classify(w):
    big = np.abs(w) > 0.5
    if big.all(): return 'S' if np.sign(w[0]) != np.sign(w[1]) else '?'
    if big[1]: return '2'
    if big[0]: return '1'
    return '0'
for S in [0.0, 0.5, 0.8, 0.9]:
    row = []
    for r in [0.1, 0.3, 0.7, 1.5, 3.0]:
        I = np.array([1.0, r]); res = []
        for seed in range(6):
            W, b = train(2, 1, S, I, steps=3000, seed=seed); res.append((eval_loss(W, b, 2, S, I), classify(W[0])))
        res.sort(); row.append(res[0][1] + '(%d/6)' % sum(c == res[0][1] for _, c in res))
    print('S=%.1f' % S, ' '.join(row))
C = 5.76e23
for al, be in [(0.34, 0.28), (0.3392, 0.2849)]:
    A, B = 406.4, 410.7
    G = (al*A/(be*B))**(1/(al+be)); N = G*(C/6)**(be/(al+be)); print('alpha %.4f beta %.4f: N_opt %.4g D/N %.2f' % (al, be, N, C/6/N/N))
