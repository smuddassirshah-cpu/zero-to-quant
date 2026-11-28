"""llm-apps level 2 (Language models in quant research): a seeded market with a planted text signal.

There is no language model here: the "model scores" are built from a planted mix of real signal,
memorised future returns (before the model's training cut-off) and late news, so every leak has a known size.

make_market(seed=0, days=2000, cutoff_day=1500, edge=0.0005, memory=2.0, late=2.0, drift=0.3)
    -> dict with
    "dates":   list of business-day dates 'YYYY-MM-DD' from 2016-01-04 (pandas bdate_range).
    "ret":     NumPy array; ret[t] is the return from the close of day t to the close of day t + 1:
               edge * signal[t] + noise with a spread of 1%.
    "signal":  the real signal, standard normal, knowable before the close of day t.
    "cutoff":  dates[cutoff_day - 1], the last day of the model's training text.
    "docs":    list of {"published": 'YYYY-MM-DD HH:MM', "day": t, "score": s}, one document a day, published at a
               minute drawn uniformly from 08:00 to 19:59. Its score is signal[t]
               + memory * ret[t] / 0.01 for t < cutoff_day (the model has read what happened next; the cut-off
                 day's own next move, ret[cutoff_day - 1], is treated as known too, one day in 1,500)
               + late * ret[t] / 0.01 if published after 16:30 (news after the close already carries the next move)
               + drift for t >= days - 250 (a vendor update shifts every score up in the last year).
    "close":   '16:30', the decision time.
long_short_sharpe(pnl) -> annualised Sharpe ratio, mean / sd (n - 1) * sqrt(252).
NumPy, pandas and the standard library only.
"""
import math

import numpy as np
import pandas as pd

__version__ = "1.0"


def make_market(seed=0, days=2000, cutoff_day=1500, edge=0.0005, memory=2.0, late=2.0, drift=0.3):
    g = np.random.default_rng(seed)
    dates = [d.strftime('%Y-%m-%d') for d in pd.bdate_range('2016-01-04', periods=days)]
    signal = g.standard_normal(days)
    ret = edge * signal + 0.01 * g.standard_normal(days)
    minutes = g.integers(8 * 60, 20 * 60, size=days)
    docs = []
    for t in range(days):
        m = int(minutes[t])
        s = signal[t]
        if t < cutoff_day:
            s += memory * ret[t] / 0.01
        if m > 16 * 60 + 30:
            s += late * ret[t] / 0.01
        if t >= days - 250:
            s += drift
        docs.append({"published": f"{dates[t]} {m // 60:02d}:{m % 60:02d}", "day": t, "score": round(float(s), 6)})
    return {"dates": dates, "ret": ret, "signal": signal, "cutoff": dates[cutoff_day - 1], "docs": docs, "close": "16:30"}


def long_short_sharpe(pnl):
    pnl = np.asarray(pnl, dtype=float)
    return float(pnl.mean() / pnl.std(ddof=1) * math.sqrt(252))
