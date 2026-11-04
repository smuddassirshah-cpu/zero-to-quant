"""Generators for the research-int data files (E14). Run: ./run.sh gen_data.py  -> writes ./data/*.csv
Every file is made with numpy default_rng(seed) and pandas 2.2.3 / numpy 2.0.2 (the Pyodide 0.27.7 versions)."""
import math, os
import numpy as np, pandas as pd

OUT = os.path.join(os.path.dirname(os.path.abspath("gen_data.py")), "data")

def futures_daily(seed=2026):
    """1,000 business days from 2021-01-04. log return r_t = 0.0002 + 0.06 r_{t-1} + 0.01 e_t; close from 4000; volume lognormal."""
    rng = np.random.default_rng(seed); n = 1000
    e = rng.standard_normal(n); r = np.zeros(n)
    for t in range(n):
        r[t] = 0.0002 + (0.06 * r[t-1] if t else 0.0) + 0.01 * e[t]
    close = np.round(4000 * np.exp(np.cumsum(r)), 2)
    vol = np.round(1.0e6 * np.exp(0.25 * rng.standard_normal(n) + 15 * np.abs(r))).astype(int)
    return pd.DataFrame({"date": pd.bdate_range("2021-01-04", periods=n).strftime("%Y-%m-%d"), "close": close, "volume": vol})

def spread_daily(seed=2027):
    """600 business days from 2022-01-03. x_t = 50 + 0.9 (x_{t-1} - 50) + e_t, e_t ~ N(0, 1), x_0 = 50."""
    rng = np.random.default_rng(seed); n = 600; x = np.zeros(n); x[0] = 50.0
    for t in range(1, n):
        x[t] = 50 + 0.9 * (x[t-1] - 50) + rng.standard_normal()
    return pd.DataFrame({"date": pd.bdate_range("2022-01-03", periods=n).strftime("%Y-%m-%d"), "spread_bp": np.round(x, 2)})

def houses(seed=2028):
    """400 homes. price_k = 80 + 2.6 area + 9 bedrooms - 0.8 age - 5 distance + band + 18 garden + N(0, 28).
    20 ages blank; 4 prices typed in pounds not thousands (x1000)."""
    rng = np.random.default_rng(seed); n = 400
    area = np.clip(np.round(rng.normal(95, 25, n)), 35, 220)
    beds = np.clip(np.round(area / 32 + rng.normal(0, 0.6, n)), 1, 6).astype(int)
    age = rng.integers(0, 91, n).astype(float)
    dist = np.round(np.clip(rng.lognormal(1.2, 0.6, n), 0.3, 25), 1)
    band = rng.choice(list("ABCD"), n, p=[0.15, 0.30, 0.35, 0.20])
    garden = (rng.random(n) < 0.4).astype(int)
    bfx = pd.Series(band).map({"A": 40, "B": 15, "C": 0, "D": -20}).to_numpy()
    price = np.round(80 + 2.6*area + 9*beds - 0.8*age - 5*dist + bfx + 18*garden + rng.normal(0, 28, n), 1)
    df = pd.DataFrame({"id": np.arange(1, n+1), "area_m2": area.astype(int), "bedrooms": beds, "age_years": age, "distance_km": dist, "band": band, "garden": garden, "price_k": price})
    miss = rng.choice(n, 20, replace=False); df.loc[miss, "age_years"] = np.nan
    bad = rng.choice(np.setdiff1d(np.arange(n), miss), 4, replace=False); df.loc[bad, "price_k"] = np.round(df.loc[bad, "price_k"] * 1000)
    df["age_years"] = df["age_years"].astype("Int64")
    return df

def ticks_gaps(seed=2029):
    """300 quotes, seconds since 09:30:00, unsorted, 12 duplicate timestamps, 15 blank prices."""
    rng = np.random.default_rng(seed); n = 300
    t = np.sort(rng.choice(np.arange(0, 23400), n, replace=False)); p = 100 + np.cumsum(rng.normal(0, 0.05, n))
    df = pd.DataFrame({"t_sec": t, "price": np.round(p, 3)})
    dup = rng.choice(n, 12, replace=False); extra = df.loc[dup].copy(); extra["price"] = np.round(extra["price"] + rng.normal(0, 0.02, 12), 3)
    df = pd.concat([df, extra], ignore_index=True)
    blank = rng.choice(len(df), 15, replace=False); df.loc[blank, "price"] = np.nan
    return df.sample(frac=1, random_state=seed).reset_index(drop=True)

def towns_temp(seed=2030):
    """12 towns x 100 days. temp = base_town + slope_town * day + N(0, 1.5). Town 'Wick' has 2 rows only."""
    rng = np.random.default_rng(seed); towns = ["Ayr", "Bath", "Cork", "Deal", "Elgin", "Fife", "Goole", "Hove", "Ince", "Jarrow", "Kelso", "Leith"]
    slopes = np.round(np.linspace(-0.04, 0.10, 12), 3); base = np.round(rng.uniform(5, 15, 12), 1); rows = []
    for k, tn in enumerate(towns):
        for d in range(1, 101):
            rows.append((tn, d, round(base[k] + slopes[k]*d + rng.normal(0, 1.5), 2)))
    df = pd.DataFrame(rows, columns=["town", "day", "temp_c"])
    df = pd.concat([df, pd.DataFrame([("Wick", 1, 9.1), ("Wick", 2, 9.4)], columns=df.columns)], ignore_index=True)
    return df, dict(zip(towns, slopes)), dict(zip(towns, base))

def orders_messy(seed=2031):
    """600 orders. Problems: 15 exact duplicate rows, symbol case and spaces, qty text with commas on 20 rows, 10 blank prices, 5 prices of -999."""
    rng = np.random.default_rng(seed); n = 585
    sym = rng.choice(["ALPHA", "BRAVO", "CHARLIE"], n, p=[0.4, 0.35, 0.25]); side = rng.choice([1, -1], n)
    qty = rng.integers(1, 40, n) * 100; mid = pd.Series(sym).map({"ALPHA": 50.0, "BRAVO": 120.0, "CHARLIE": 8.0}).to_numpy() * (1 + rng.normal(0, 0.002, n))
    slip_bp = 0.5 + 1.2 * np.log(qty / 100) + rng.normal(0, 1.0, n)            # adverse slippage in basis points, grows with log size
    price = np.round(mid * (1 + side * slip_bp / 1e4), 4)
    df = pd.DataFrame({"order_id": np.arange(1, n+1), "symbol": sym, "side": np.where(side == 1, "B", "S"), "qty": qty, "price": price, "mid": np.round(mid, 4)})
    dup = df.sample(15, random_state=1); df = pd.concat([df, dup], ignore_index=True).sample(frac=1, random_state=2).reset_index(drop=True)
    dfc = df.copy(); idx = rng.choice(len(df), 20, replace=False)
    dfc["qty"] = dfc["qty"].astype(object); dfc.loc[idx, "qty"] = [f"{int(q):,}" for q in df.loc[idx, "qty"]]
    # messy symbols
    jj = rng.choice(len(df), 40, replace=False); dfc.loc[jj[:20], "symbol"] = dfc.loc[jj[:20], "symbol"].str.lower(); dfc.loc[jj[20:], "symbol"] = " " + dfc.loc[jj[20:], "symbol"] + " "
    cand = np.setdiff1d(np.arange(len(df)), np.where(dfc["order_id"].duplicated(keep=False))[0])
    pick = rng.choice(cand, 15, replace=False); dfc["price"] = dfc["price"].astype(float); dfc.loc[pick[:10], "price"] = np.nan; dfc.loc[pick[10:], "price"] = -999.0
    return dfc

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    futures_daily().to_csv(f"{OUT}/futures-daily.csv", index=False)
    spread_daily().to_csv(f"{OUT}/spread-daily.csv", index=False)
    houses().to_csv(f"{OUT}/houses.csv", index=False)
    ticks_gaps().to_csv(f"{OUT}/ticks-gaps.csv", index=False)
    towns_temp()[0].to_csv(f"{OUT}/towns-temp.csv", index=False)
    orders_messy().to_csv(f"{OUT}/orders-messy.csv", index=False)
    for f in sorted(os.listdir(OUT)): print(f, os.path.getsize(f"{OUT}/{f}"), "bytes", sum(1 for _ in open(f"{OUT}/{f}"))-1, "rows")
