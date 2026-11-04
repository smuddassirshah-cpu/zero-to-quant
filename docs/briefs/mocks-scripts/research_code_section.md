Reference `weighted_line_fit` (parts 1 and 2; part 1 starts without `weights`):

```python
def weighted_line_fit(xs, ys, weights=None):
    n = len(xs)
    if n != len(ys) or (weights is not None and len(weights) != n) or n < 2:
        raise ValueError("need matching lists of at least two points")
    w = weights if weights is not None else [1.0] * n
    sw = sum(w)
    mx = sum(wi * x for wi, x in zip(w, xs)) / sw
    my = sum(wi * y for wi, y in zip(w, ys)) / sw
    sxx = sum(wi * (x - mx) ** 2 for wi, x in zip(w, xs))
    if sxx == 0:
        raise ValueError("all x values are equal")
    sxy = sum(wi * (x - mx) * (y - my) for wi, x, y in zip(w, xs, ys))
    slope = sxy / sxx
    return [slope, my - slope * mx]
```

Part 1 hidden tests (`weighted_line_fit(xs, ys)`):

| # | Call | Expected | Compare |
| --- | --- | --- | --- |
| 1 | `weighted_line_fit([1, 2, 3, 4], [2, 3, 5, 4])` | `[0.8, 1.5]` | isclose, tol rel 1e-9 and abs 1e-9 |
| 2 | `weighted_line_fit([0, 10], [100, 200])` | `[10.0, 100.0]` | isclose, tol rel 1e-9 and abs 1e-9 |
| 3 | `weighted_line_fit([3, 1, 2], [30, 10, 25])` | `[10.0, 1.6666666666666679]` | isclose, tol rel 1e-9 and abs 1e-9 |
| 4 | `weighted_line_fit(list(range(100000)), [3 * i + 7 for i in range(100000)])` | `[3.0, 7.0]` | isclose, tol rel 1e-9 and abs 1e-9 |
| 5 | `weighted_line_fit([1e8 + 3, 1e8 + 4, 1e8 + 5, 1e8 + 6], [2, 5, 4, 8])` | `[1.7, -170000002.9]` | isclose, tol rel 1e-9 and abs 1e-9 |
| 6 | `weighted_line_fit([5, 5, 5], [1, 2, 3])` | raises `ValueError` | raises |
| 7 | `weighted_line_fit([1], [2])` | raises `ValueError` | raises |
| 8 | `weighted_line_fit([1, 2, 3], [4, 5])` | raises `ValueError` | raises |

Part 2 adds these hidden tests (the part 1 tests run too, 13 in all):

| # | Call | Expected | Compare |
| --- | --- | --- | --- |
| 1 | `weighted_line_fit([1, 2, 3, 4], [2, 3, 5, 4], [1, 1, 1, 1])` | `[0.8, 1.5]` | isclose, tol rel 1e-9 and abs 1e-9 |
| 2 | `weighted_line_fit([0, 1, 2], [1, 3, 2], [1, 1, 4])` | `[0.2857142857142857, 1.5714285714285714]` | isclose, tol rel 1e-9 and abs 1e-9 |
| 3 | `weighted_line_fit([1, 2, 3], [2, 4, 7], [0.5, 1.0, 2.0])` | `[2.6153846153846154, -0.9230769230769225]` | isclose, tol rel 1e-9 and abs 1e-9 |
| 4 | `weighted_line_fit([0, 10], [5, 7], [1, 1000])` | `[0.19999999999999998, 5.0]` | isclose, tol rel 1e-9 and abs 1e-9 |
| 5 | `weighted_line_fit([1, 2, 3], [2, 4, 7], [1, 1])` | raises `ValueError` | raises |

Reference `rolling_slopes`:

```python
def rolling_slopes(xs, ys, w):
    sx = sy = sxx = sxy = 0
    out = []
    for i in range(len(xs)):
        sx += xs[i]; sy += ys[i]; sxx += xs[i] * xs[i]; sxy += xs[i] * ys[i]
        if i >= w:
            j = i - w
            sx -= xs[j]; sy -= ys[j]; sxx -= xs[j] * xs[j]; sxy -= xs[j] * ys[j]
        if i >= w - 1:
            den = w * sxx - sx * sx
            out.append(None if den == 0 else (w * sxy - sx * sy) / den)
    return out
```

Hidden tests:

| # | Call | Expected | Compare |
| --- | --- | --- | --- |
| 1 | `rolling_slopes([1, 2, 3, 4, 5], [2, 4, 5, 4, 5], 3)` | `[1.5, 0.0, 0.0]` | isclose, tol rel 1e-9 and abs 1e-9 |
| 2 | `rolling_slopes([1, 2, 3], [2, 4, 7], 3)` | `[2.5]` | isclose, tol rel 1e-9 and abs 1e-9 |
| 3 | `rolling_slopes([1, 2, 3], [2, 4, 7], 4)` | `[]` | equal |
| 4 | `rolling_slopes([0, 1, 2, 3], [5, 5, 5, 5], 2)` | `[0.0, 0.0, 0.0]` | isclose, tol rel 1e-9 and abs 1e-9 |
| 5 | `rolling_slopes([4, 2, 9, 1, 7, 3], [8, 1, 6, 2, 9, 5], 2)` | `[3.5, 0.7142857142857143, 0.5, 1.1666666666666667, 1.0]` | isclose, tol rel 1e-9 and abs 1e-9 |
| 6 | `[s is None for s in rolling_slopes([1, 1, 1, 2, 3], [1, 2, 3, 4, 9], 3)]` | `[True, False, False]` | equal |
| 7 | `len(rolling_slopes(list(range(10)), list(range(10)), 10))` | `1` | equal |
| 8 | `sum(rolling_slopes([i % 10 for i in range(200000)], [(i * i) % 97 for i in range(200000)], 1000))` | `1.007939393939394` | isclose, tol rel 1e-9 and abs 1e-9 |
| 9 | `rolling_slopes(list(range(200000)), [2 * i + 1 for i in range(200000)], 50000)[-1]` | `2.0` | isclose, tol rel 1e-6 |
| 10 | `len(rolling_slopes(list(range(200000)), [i % 7 for i in range(200000)], 50000))` | `150001` | equal |
