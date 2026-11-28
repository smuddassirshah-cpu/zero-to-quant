# backprop level 1: performance task

- `homework-1.json` item 6 of 6, `h-perf-by-hand`. Kind `derivation` (a `longform` with an empty box, no hints, no parts), difficulty 5.
- Objective (l4): "Derive every gradient of a small expression by hand, working back from the output." The level matches the verb rule on l4 ("Derive"), so the task is a derivation.
- Product: for $L = (e^{xy} - 1)^2$ at $x = 0.5$, $y = 0.8$ (six nodes: two inputs, a product, an exponential, a sum with a constant, a square), the forward values, every local derivative, every gradient from $L$ back, one box per line, and a nudge check of $\partial L/\partial x$. Full model answer; rubric 2 + 2 + 3 + 2 + 1 = 10, the four rows naming a part `required: true`, the fifth marked "Optional" in the prompt.
- `node tools/rubric-passes.mjs --item content/courses/backprop/homework-1.json#h-perf-by-hand`: minimal passing set rows 1 to 4 (9 points); rows 1 to 4 "can be left out: no".

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/backprop python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `<venv>/bin/python docs/reports/backprop-L1-numbers.py`: exit 0; the model's figures are recomputed by the rule and by central differences ($\partial L/\partial x = 1.173946$, $\partial L/\partial y = 0.733716$) and the nudge (0.011930 against 0.011739) is checked to agree within 3%.
4. `node tools/playthrough.mjs --set backprop/homework-1 --local-cdn <pkgs>` with and without `--mobile`: all passed; the longform was marked by the button and its `-marked` shots read cleanly at 1280 and 440.

- Overlapping screens: l4 screens 1 to 6 work a different chain, $L = (e^{wx+b})^2$, with the same four operations; homework item 2 orders a backward pass for $(xy + \ln z)^2$. New in the task: a sum with a constant, the whole pass from a blank box, and the nudge check written out.
