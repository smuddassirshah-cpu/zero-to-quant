##### Reference for `qd-returns`

```python
import numpy as np
import pandas as pd

def tidy_closes():
    df = pd.read_csv("qd-prices.csv")
    df = df.drop_duplicates().dropna(subset=["close"])
    return df.sort_values(["ticker", "date"]).reset_index(drop=True)

def vol_by_ticker():
    df = tidy_closes()
    out = {}
    for ticker, g in df.groupby("ticker"):
        r = np.log(g["close"]).diff().dropna()
        out[ticker] = float(r.std(ddof=1) * np.sqrt(252))
    return out
```

| # | Call | Expected | Compare |
| --- | --- | --- | --- |
| 1 | `len(tidy_closes())` | `773` | equal |
| 2 | `int(tidy_closes()['close'].isna().sum())` | `0` | equal |
| 3 | `list(tidy_closes().columns)` | `['date', 'ticker', 'close']` | equal |
| 4 | `int(tidy_closes().duplicated().sum())` | `0` | equal |
| 5 | `tidy_closes().groupby('ticker').size().to_dict()` | `{'KAPPA': 258, 'LAMBDA': 257, 'MU': 258}` | equal |
| 6 | `bool(tidy_closes().groupby('ticker')['date'].apply(lambda s: s.is_monotonic_increasing).all())` | `True` | equal |
| 7 | `sorted(vol_by_ticker())` | `['KAPPA', 'LAMBDA', 'MU']` | equal |
| 8 | `vol_by_ticker()['KAPPA']` | `0.1760834506309832` | isclose (tol {"rel": 1e-09}) |
| 9 | `vol_by_ticker()['LAMBDA']` | `0.25816881352482823` | isclose (tol {"rel": 1e-09}) |
| 10 | `vol_by_ticker()['MU']` | `0.3577200967909071` | isclose (tol {"rel": 1e-09}) |

##### Reference for `qd-rolling-beta`

```python
import numpy as np
import pandas as pd

def windowed_betas(window):
    df = pd.read_csv("qd-pair.csv")
    df = df[(df["asset"].abs() <= 0.25) & (df["mkt"].abs() <= 0.25)]
    x = df["mkt"].to_numpy()
    y = df["asset"].to_numpy()
    out = []
    for i in range(len(x) - window + 1):
        xs, ys = x[i:i + window], y[i:i + window]
        out.append(float(np.cov(xs, ys, ddof=1)[0, 1] / np.var(xs, ddof=1)))
    return out
```

| # | Call | Expected | Compare |
| --- | --- | --- | --- |
| 1 | `len(windowed_betas(60))` | `458` | equal |
| 2 | `windowed_betas(60)[0]` | `0.8032989217239858` | isclose (tol {"rel": 1e-09}) |
| 3 | `windowed_betas(60)[-1]` | `1.382877464391472` | isclose (tol {"rel": 1e-09}) |
| 4 | `sum(windowed_betas(60))` | `502.3786453492044` | isclose (tol {"rel": 1e-09}) |
| 5 | `min(windowed_betas(120))` | `0.8194411434696784` | isclose (tol {"rel": 1e-09}) |
| 6 | `max(windowed_betas(120))` | `1.425200190403877` | isclose (tol {"rel": 1e-09}) |
| 7 | `windowed_betas(600)` | `[]` | equal |
| 8 | `windowed_betas(517)[0]` | `1.0877069411378124` | isclose (tol {"rel": 1e-09}) |

##### Reference for `qd-out-of-sample`

```python
import numpy as np
import pandas as pd

def oos_scores(split):
    df = pd.read_csv("qd-signal.csv")
    X = np.column_stack([np.ones(len(df) - 1), df["x1"].to_numpy()[:-1], df["x2"].to_numpy()[:-1]])
    y = df["ret"].to_numpy()[1:]
    Xtr, ytr, Xte, yte = X[:split], y[:split], X[split:], y[split:]
    coef, *_ = np.linalg.lstsq(Xtr, ytr, rcond=None)
    train_r2 = 1 - np.sum((ytr - Xtr @ coef) ** 2) / np.sum((ytr - ytr.mean()) ** 2)
    oos_r2 = 1 - np.sum((yte - Xte @ coef) ** 2) / np.sum((yte - ytr.mean()) ** 2)
    return {"coef": [float(c) for c in coef], "train_r2": float(train_r2), "oos_r2": float(oos_r2)}
```

| # | Call | Expected | Compare |
| --- | --- | --- | --- |
| 1 | `sorted(oos_scores(500))` | `['coef', 'oos_r2', 'train_r2']` | equal |
| 2 | `oos_scores(500)['coef']` | `[0.00025424269185633027, 0.0022966524429744854, -0.0015904841020325...` | isclose (tol {"rel": 1e-08}) |
| 3 | `oos_scores(500)['train_r2']` | `0.08363857338496772` | isclose (tol {"rel": 1e-08}) |
| 4 | `oos_scores(500)['oos_r2']` | `0.057702003278431` | isclose (tol {"rel": 1e-08}) |
| 5 | `oos_scores(300)['coef']` | `[0.000512415044256865, 0.0018296538844713329, -0.001413107004839858]` | isclose (tol {"rel": 1e-08}) |
| 6 | `oos_scores(300)['oos_r2']` | `0.08668570838518808` | isclose (tol {"rel": 1e-08}) |
| 7 | `oos_scores(600)['oos_r2']` | `0.052537017793764074` | isclose (tol {"rel": 1e-08}) |
