# info level 3: performance task

- `homework-3.json` item 4 of 6, `h-signal-information`. Kind `code`, difficulty 5, pace 1500 s.
- Matched objective (l12): "Write an estimator of the information a discrete signal carries about the next return's sign, and correct its bias on short samples." The verb "Write" matches the rule, so the task is `code`.
- Product: `signal_information(signal, returns, corrected=True)` from a one-line stub (no imports): returns become signs with a return of exactly 0 counting as down (stated in the prose), the plug-in mutual information in bits from the joint counts, and the first-order correction $\tfrac{(k_X - 1)(k_Y - 1)}{2n \ln 2}$ with $k$ the states seen.
- 7 hidden tests, 1 example: planted samples exact to 1e-9 (one where zero returns must count as down, else the answer drops from 1 bit to 0), a three-state planted sample, the correction's size as plug-in minus corrected, a constant signal (0), the default `corrected=True`, and a seeded useless sample of 500 days (`random.Random(5)`, Gaussian returns) whose corrected estimate must lie within 0.008 bits of 0 (it is 0.00014; plug-in 0.0030).
- Overlapping screens: l12 screen 9 (`mi_estimate` on lists of states) and l11 screen 8 (`rank_features`). New in the task: returns rather than signs, the zero-return rule, the default argument, and a longer seeded null sample.

Gates:
1. Validator: `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors, no warning on any info file.
2. Voice: `VOICE_BASE=app/content/courses/info python3 docs/reviews/voice-scan.py 35`: 0 over 35 words, 0 lesson ids in code spans.
3. Numbers script: `<venv>/bin/python docs/reports/info-L3-numbers.py` exits 0; it runs the model solution on all 8 cases in CPython and checks the starter fails.
4. Playthrough: `node tools/playthrough.mjs --set info/homework-3 --mobile --local-cdn <pkgs>`: passed at 1280 and 440; the starter fails and the solution passes in Pyodide.
