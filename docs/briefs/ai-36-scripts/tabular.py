"""ml-int L3: when a net beats boosting on tabular returns, and when it does not.
Panel of 40 assets x 250 days, 8 features. Time split: first 175 days train, last 75 test.
Two worlds. A: a threshold signal on 2 features plus 6 noise features, t(3) noise. B: a smooth oblique signal on all 8.
Second method: a second seed; and R2 computed by hand against sklearn's r2_score."""
import numpy as np, time
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score

def panel(world, seed, assets=100, days=500, p=8):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((days, assets, p))
    if world == 'A':
        sig = 0.6*((X[..., 0] > 0.8).astype(float) - (X[..., 1] < -0.8).astype(float))*((X[..., 0] > 0.8) | (X[..., 1] < -0.8))
        sig = sig + 0.4*(X[..., 0] > 0.8)*(X[..., 1] > 0.5)
        noise = rng.standard_t(3, (days, assets))/np.sqrt(3)
    else:
        w = rng.standard_normal(p); w /= np.linalg.norm(w)
        u = X@w; v = X@np.roll(w, 3)
        sig = 0.5*np.tanh(1.5*u) + 0.3*u*v/2
        noise = rng.standard_normal((days, assets))
    y = sig + 5.0*noise*np.std(sig)
    return X, y, sig

def run(world, seed):
    X, y, sig = panel(world, seed); tr = slice(0, 350); te = slice(350, 500)
    Xtr, ytr = X[tr].reshape(-1, X.shape[2]), y[tr].ravel(); Xte, yte = X[te].reshape(-1, X.shape[2]), y[te].ravel()
    out = {}
    t0 = time.time(); gb = HistGradientBoostingRegressor(max_iter=200, learning_rate=0.05, max_leaf_nodes=15, random_state=0).fit(Xtr, ytr); out['boost'] = gb.predict(Xte); tb = time.time()-t0
    t0 = time.time(); nn = MLPRegressor(hidden_layer_sizes=(32, 32), alpha=1e-3, learning_rate_init=1e-3, max_iter=300, early_stopping=True, random_state=0).fit(Xtr, ytr); out['mlp'] = nn.predict(Xte); tn = time.time()-t0
    out['ridge'] = Ridge(alpha=1.0).fit(Xtr, ytr).predict(Xte)
    oracle = 1 - np.mean((yte - sig[te].ravel())**2)/np.var(yte)
    res = {k: (r2_score(yte, v), 1 - np.sum((yte-v)**2)/np.sum((yte-yte.mean())**2)) for k, v in out.items()}
    d = {k: ((yte-v)**2).reshape(150, -1).mean(1) for k, v in out.items()}
    for a, b in [('mlp', 'boost')]:
        dd = d[a]-d[b]; res['paired %s-%s per-day MSE diff' % (a, b)] = (dd.mean()/np.var(yte), dd.mean()/(dd.std(ddof=1)/np.sqrt(len(dd))))
    return res, oracle, tb, tn

for world in ['A', 'B']:
    for seed in [0, 1]:
        res, oracle, tb, tn = run(world, seed)
        print('world %s seed %d: ' % (world, seed) + ' '.join('%s %.4f (%.4f)' % (k, a, b) for k, (a, b) in res.items()) + ' | oracle %.4f | time boost %.2fs mlp %.2fs' % (oracle, tb, tn))
