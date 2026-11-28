# backprop level 3: performance task

- `homework-3.json` item 6 of 6, `h-perf-network`. Kind `code` (Python), difficulty 5.
- Objective (l9): "Build a tanh neuron from `Value` operations and backpropagate through it." The level matches the verb rule on l9 ("Build"), so the task is code; the level's exit is the network, so the product is the whole network and its training.
- Product: from a stub of empty methods, `Neuron`, `Layer`, `MLP` (each with `parameters()`) and `train`, on the loaded `Value` class with `tanh()` and six points `X6`, `Y6` that need a hidden layer. 6 hidden tests, 1 example: the parameter count of a 2-4-1 network (17); one output at fixed parameters within 1e-9 ($-0.8492470209$); the l12 gradient check (in the postlude) below $10^{-6}$ at $h = 10^{-6}$ on a 2-4-1 network, seed 5 ($9.0 \times 10^{-8}$); a 200-step run on the six points below a loss of 0.05 (the script finds 0.0172, so the threshold has a margin of about three); the length of the loss list; the first five parameters for seed 42. No hints, no parts. `budget: 6000`.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/backprop python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `<venv>/bin/python docs/reports/backprop-L3-numbers.py`: exit 0; it runs the model solution against all six tests, recomputes the fixed-parameter output by hand, checks the 200-step loss against a NumPy run from the same draws (agreement to 1e-9) and the gradient check below $10^{-6}$.
4. `node tools/playthrough.mjs --set backprop/homework-3 --local-cdn <pkgs>` with and without `--mobile`: all passed ("1 performance starter fail" as required).

- Overlapping screens: l10 screen 8 (the three classes, tested on counts, draws and outputs) and l11 screen 8 (`train` on the course data). The task joins them from an empty stub, on new data (six points, a 2-4-1 network), and adds a fixed-parameter output and a gradient check the lessons did not ask of the learner's classes. fresh-check reports `Neuron`, `parameters` and `check_gradients` as shared code names for that reason.
