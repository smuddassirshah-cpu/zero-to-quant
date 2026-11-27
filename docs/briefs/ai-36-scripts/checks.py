"""Second methods for a few figures stated once elsewhere."""
import numpy as np
from induction import build, seqs, forward_loop, token_losses, H, halves
G = 0.95
print('goal reward to beat the loop from the coin cell: %.4f (by search %.4f)' % ((G/(1-G*G))/G**6,
      next(r/1e4 for r in range(100000, 200000) if r/1e4*G**6 > G/(1-G*G))))
g = 0.9; print('gamma 0.9: loop %.4f goal %.4f' % (g/(1-g*g), 10*g**6), 'series sums %.4f %.4f' % (sum(g**(2*k+1) for k in range(2000)), 10*g**6))
Wb = build(0, backdoor=True); St = seqs(3, 20, avoid=9); trig = St.copy(); trig[:, 3] = 9; trig[:, H+3] = 9
lv = np.mean([token_losses(forward_loop(Wb, q), q)[H+1:].mean() for q in trig])
print('backdoor with trigger, 20 seqs: loop %.4f vectorised %.4f' % (lv, halves(Wb, trig)[1]))
lc = np.mean([token_losses(forward_loop(Wb, q), q)[H+1:].mean() for q in St])
print('backdoor no trigger, 20 seqs: loop %.4f vectorised %.4f' % (lc, halves(Wb, St)[1]))
# judge signal strength by simulation
rng = np.random.default_rng(0); q = 0.7; picks = rng.random(200000) < q
print('signal 2q-1 = %.4f ; simulated mean of +1/-1 picks %.4f' % (2*q-1, np.mean(np.where(picks, 1, -1))))
# contamination
print('clean accuracy %.4f' % ((0.80*500 - 0.98*100)/400))
