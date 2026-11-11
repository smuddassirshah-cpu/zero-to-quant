"""Delta read, stat-learning L4: review-4 `r-few-rows` and l19 screens[5] against a run.
80 rows, 25 features (the item's sizes), the level's own make_wide signal in 2 columns, 300 test rows, 40 seed pairs.
Learners as the item's four options: scaled penalised logistic regression, 15-nearest neighbours, a 64-unit network,
an additive model with 10 knots per feature (300 spline columns). Then the wide row's own sizes (60 rows, 20 features).
Usage: <venv python> few_rows.py"""
import json, math, os, warnings
import numpy as np
warnings.filterwarnings("ignore")
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'app', 'content', 'courses', 'stat-learning')
G = {}
exec(json.load(open(os.path.join(ROOT, 'l19-which-learner.json')))['screens'][7]['widget']['prelude'], G)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, SplineTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
L = {
    'a logistic': lambda: make_pipeline(StandardScaler(), LogisticRegression()),
    'b 15-NN': lambda: make_pipeline(StandardScaler(), KNeighborsClassifier(15)),
    'c 64-unit net': lambda: make_pipeline(StandardScaler(), MLPClassifier(hidden_layer_sizes=(64,), solver="lbfgs", alpha=0.01, random_state=0, max_iter=500)),
    'd additive, 10 knots': lambda: make_pipeline(StandardScaler(), SplineTransformer(n_knots=10), LogisticRegression(max_iter=5000)),
}
for n, p, tag in ((80, 25, "the item's sizes"), (60, 20, "the wide row's sizes")):
    R = []
    for i in range(40):
        Xa, ya = G['make_wide'](n, 7000 + 2 * i, p); Xb, yb = G['make_wide'](300, 7001 + 2 * i, p)
        R.append([mk().fit(Xa, ya).score(Xb, yb) for mk in L.values()])
    R = np.array(R); d = R[:, 3] - R[:, 0]
    cols = SplineTransformer(n_knots=10).fit_transform(Xa).shape[1]
    print(f"{tag}: {n} rows, {p} features, {cols} spline columns; means over 40 pairs {dict(zip(L, np.round(R.mean(0), 4).tolist()))}")
    print(f"   additive minus logistic {d.mean():+.4f} (se {d.std(ddof=1) / math.sqrt(40):.4f}); logistic best or tied best in {int((R[:, 0] >= R.max(1)).sum())} of 40; additive best or tied best in {int((R[:, 3] >= R.max(1)).sum())}")
