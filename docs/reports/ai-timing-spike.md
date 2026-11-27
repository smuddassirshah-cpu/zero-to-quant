# AI strand timing spike (PLAN 8 A2)

Headless Chromium 158, 4 cores, Pyodide 0.27.7 (NumPy 2.0.2, scikit-learn 1.6.1) in a web worker. jsDelivr is blocked here, so I used the local distribution from `app/tools/fetch-local-cdn.sh`. Median of three after warm-up. Native: Python 3.13, NumPy 2.5, scikit-learn 1.9, 4 BLAS threads (1 thread in brackets). The GPT backward is hand-written, finite-difference checked (error 2e-8), float64, random tokens.

| Item | Pyodide | Native | Ratio |
|---|---|---|---|
| 1. matmul 256 / 512 GFLOP/s | 2.1 / 0.7 | 147 / 212 (48 / 57) | 70 to 300x |
| 2. `load_digits()` | 28 ms first, 11 ms after, 0 network requests | n/a | n/a |
| 2b. `import sklearn.datasets` | 3.6 s (plus 1.9 s package load, local) | n/a | n/a |
| 3. CNN epoch, 1,257 images | 19 ms; 90.2% at 10, 97.4% at 40 epochs | 4.8 ms | 4x |
| 4. GPT step (59,840 params) | 86 ms; 58 steps in 5 s, 697 in 60 s | 13.7 ms | 6x |
| 5. micrograd 2-16-16-1, 100 points | 0.66 s per epoch | 0.52 s | 1.3x |

The digits data ships inside the sklearn wheel, so `load_digits` needs no network once packages are cached. Pyodide NumPy has no optimised BLAS or threads, hence the slow matmul.

## Budget rule

Assumption, to confirm on the phone: a mid-range phone is 3 to 5 times slower, so a GPT step is 0.26 to 0.43 s and a CNN epoch 0.06 to 0.10 s.

- A graded case costs 1 s or less on this desktop (passes in the default 5 s on the phone).
- With an explicit `budget`, 10 s or less here (30 to 50 s on the phone); never above 20 s, under the 120 s cap.
- So: digits CNN up to 40 epochs; GPT up to 10 steps by default, up to 100 with `budget` 40,000; micrograd one epoch of 100 points; matmul 128 by 128 or smaller.
- 500 GPT steps is 43 s here and 130 to 215 s on the phone, over the cap. Do not grade it: ship weights or recorded losses, or stream it in the ungraded `trainer`.

## Repeat items 1 and 4 on the phone

The app has no free-form Python page, so use the standalone page (tested here, in a worker), kept at `app/tools/ai-timing/phone.html`.
1. On the laptop: `python3 -m http.server 8000` in the folder holding it.
2. On the phone, same Wi-Fi: open `http://<laptop-IP>:8000/phone.html` (loads Pyodide from jsDelivr).
3. Tap Run; after about a minute it prints matmul GFLOP/s and the GPT step time with steps in 5 s and 60 s.
4. Divide this table's figures by the phone's to replace the 3 to 5 assumption.
