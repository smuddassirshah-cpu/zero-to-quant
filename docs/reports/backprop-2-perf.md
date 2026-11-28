# backprop level 2: performance task

- `homework-2.json` item 6 of 6, `h-perf-value-class`. Kind `code` (Python), difficulty 5.
- Objective (l7): "Write a `Value` class that records how each number was made, with addition and multiplication." The level matches the verb rule on l7 ("Write"), so the task is code.
- Product: from a stub of empty methods, a `Value` class with `data`, `grad`, `_prev`, `_op`, `+` and `*` with a Value or a number on either side, and `backward()`. 8 hidden tests, 1 example (the course expression): a chain (6.0), a diamond (22.0), a value used three times (12.0), numbers on the left (4.0), a second pass after a reset by hand ($(0.0, 2.0)$), the course expression, an unused node (its gradient stays 0.0) and one product. All exact (`compare: "equal"`). No hints, no parts.
- The playthrough pastes the untouched stub (it fails) and then the model solution (all 8 pass).

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/backprop python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `<venv>/bin/python docs/reports/backprop-L2-numbers.py`: exit 0; it runs the model solution against all 8 tests and checks the chain, diamond, cube and reset cases against central differences.
4. `node tools/playthrough.mjs --set backprop/homework-2 --local-cdn <pkgs>` with and without `--mobile`: all passed ("1 performance starter fail" as required).

- Overlapping screens: l7 screen 8 (the closures and right-hand methods, tested by calling closures by hand) and l8 screen 4 (`backward()` on a given class). The task joins them from an empty stub and tests only whole expressions the lessons did not use; the method name `backward` is shared with l8 by design (fresh-check reports it as a code-name hit).
