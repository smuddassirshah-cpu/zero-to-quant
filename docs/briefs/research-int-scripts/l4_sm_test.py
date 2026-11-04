import numpy as np
class OnlineOLS:
    def __init__(self, p, delta=1e-8):
        self.P = np.eye(p) / delta
        self.b = np.zeros(p)
    def add(self, x, y):
        x = np.asarray(x, float); Px = self.P @ x
        self.P = self.P - np.outer(Px, Px) / (1.0 + x @ Px)
        self.b = self.b + (self.P @ x) * (y - x @ self.b)
    def remove(self, x, y):
        x = np.asarray(x, float); Px = self.P @ x
        self.P = self.P + np.outer(Px, Px) / (1.0 - x @ Px)
        self.b = self.b - (self.P @ x) * (y - x @ self.b)
    def coef(self):
        return self.b.copy()
for delta in (1e-6, 1e-8, 1e-10):
    o = OnlineOLS(2, delta)
    seq = [(1, 2), (2, 2), (3, 4), (4, 5)]
    for x, y in seq: o.add([1.0, x], y)
    c1 = o.coef(); o.add([1.0, 5], 5); c2 = o.coef(); o.remove([1.0, 1], 2); c3 = o.coef()
    print(delta, c1, c2, c3)
    rng = np.random.default_rng(7); X = np.c_[np.ones(200), rng.normal(size=(200, 2))]; y = X @ [1, 2, -1] + rng.normal(size=200)
    o = OnlineOLS(3, delta)
    for i in range(200): o.add(X[i], y[i])
    ref = np.linalg.lstsq(X, y, rcond=None)[0]
    print("   200 rows max err", np.abs(o.coef() - ref).max())
    for i in range(50): o.remove(X[i], y[i])
    ref2 = np.linalg.lstsq(X[50:], y[50:], rcond=None)[0]; print("   after removing 50, err", np.abs(o.coef() - ref2).max())
    rng = np.random.default_rng(3); X = np.c_[np.ones(20000), rng.normal(size=(20000, 2))]; y = X @ [1, 2, -1] + rng.normal(size=20000)
    o = OnlineOLS(3, delta)
    for i in range(20000): o.add(X[i], y[i])
    print("   20000 rows err", np.abs(o.coef() - np.linalg.lstsq(X, y, rcond=None)[0]).max())
