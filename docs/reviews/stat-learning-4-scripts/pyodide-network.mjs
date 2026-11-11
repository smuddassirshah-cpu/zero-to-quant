// Second read, stat-learning L4: the stated network figures recomputed in the local Pyodide 0.27.7 build
// (the app's runtime). Usage: node pyodide-network.mjs <scratchpad>/pkgs
import { pathToFileURL } from 'node:url';
import path from 'node:path';
const dir = path.join(process.argv[2], 'pyodide-0.27.7', 'package') + path.sep;
const { loadPyodide } = await import(pathToFileURL(dir + 'pyodide.mjs').href);
const py = await loadPyodide({ indexURL: dir });
await py.loadPackage(['numpy', 'scipy', 'scikit-learn'], { messageCallback: () => {} });
const out = py.runPython(`
import warnings, json
warnings.filterwarnings("ignore")
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
def make_street(n, seed):
    rng = np.random.default_rng(seed); y = np.arange(n) % 2
    X = rng.normal(0, 0.8, (n, 2)) + np.where(y[:, None] == 1, 1.0, -1.0)
    return np.round(X, 3), y
def make_rings(n, seed):
    rng = np.random.default_rng(seed); y = np.arange(n) % 2
    r = np.where(y == 1, rng.normal(0.8, 0.3, n), rng.normal(2.2, 0.4, n))
    a = rng.uniform(0, 2 * np.pi, n)
    return np.round(np.c_[r * np.cos(a), r * np.sin(a)], 3), y
def make_quadrants(n, seed):
    rng = np.random.default_rng(seed); X = rng.uniform(-2, 2, (n, 2))
    y = ((X[:, 0] * X[:, 1]) > 0).astype(int); flip = rng.random(n) < 0.1
    return np.round(X, 3), np.where(flip, 1 - y, y)
def make_wide(n, seed, p=20):
    rng = np.random.default_rng(seed); y = np.arange(n) % 2
    X = rng.normal(0, 1, (n, p))
    X[:, :2] = X[:, :2] * 0.8 + np.where(y[:, None] == 1, 1.0, -1.0)
    return np.round(X, 3), y
def make_noise(n, seed):
    rng = np.random.default_rng(seed); X = rng.normal(0, 1, (n, 2))
    return np.round(X, 3), (rng.random(n) < 0.54).astype(int)
def mlp(h, seed, A, a, B, b, scale=False):
    m = MLPClassifier(hidden_layer_sizes=(h,), solver="lbfgs", alpha=0.01, random_state=seed, max_iter=500)
    if scale: m = make_pipeline(StandardScaler(), m)
    m.fit(A, a); return [round(m.score(A, a), 4), round(m.score(B, b), 4)]
R = (*make_rings(300, 7), *make_rings(300, 8)); N = (*make_noise(300, 4), *make_noise(300, 5))
res = {
 "l17 width sweep test (1,2,3,8,64), seed 0": [mlp(h, 0, *R)[1] for h in (1, 2, 3, 8, 64)],
 "l17 seeds 0,1,2 at 8 units": [mlp(8, s, *R)[1] for s in (0, 1, 2)],
 "l17 noise 8 units (train, test) seeds 0,1,2": [mlp(8, s, *N) for s in (0, 1, 2)],
 "l17 noise 64 units (train, test) seeds 0,1,2": [mlp(64, s, *N) for s in (0, 1, 2)],
 "l19 network column (street, rings, quadrants, wide, noise)": [
    mlp(8, 0, *make_street(300, 4), *make_street(300, 5), True)[1], mlp(8, 0, *R, True)[1],
    mlp(8, 0, *make_quadrants(300, 3), *make_quadrants(300, 4), True)[1],
    mlp(8, 0, *make_wide(60, 4), *make_wide(300, 5), True)[1], mlp(8, 0, *N, True)[1]],
 "l19 rings seed pairs (9,10), (11,12) network": [mlp(8, 0, *make_rings(300, 9), *make_rings(300, 10), True)[1], mlp(8, 0, *make_rings(300, 11), *make_rings(300, 12), True)[1]],
}
json.dumps(res)
`);
for (const [k, v] of Object.entries(JSON.parse(out))) console.log(k + ': ' + JSON.stringify(v));
