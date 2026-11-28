# info level 2: performance task

- `homework-2.json` item 5 of 7, `h-kl-proof`. Kind `derivation`, difficulty 5, pace 1500 s.
- Matched objective (l6): "Derive from Jensen's inequality that the KL divergence is never negative, and compute it in bits." The verb "Derive" matches the rule, so the task is `derivation`.
- Product: a written proof in an empty longform box (no starter, steps, hints or parts), then $D(p \| q)$ in bits for the fresh pair $p = (0.6, 0.3, 0.1)$, $q = (0.4, 0.4, 0.2)$: 0.126 bits (0.088 nats, the optional row). The model answer is a numbered five-step chain with a reason per line.
- Rubric, 10 points: hypothesis $p_i > 0$ (2, required), Jensen with concavity named (2, required), $\sum q_i \le 1$ (2, required), equality only at $q = p$ (2, required), the KL in bits (1, required), nats (1, optional; the prompt says "Optional, one more point"). `node tools/rubric-passes.mjs --item content/courses/info/homework-2.json#h-kl-proof`: one minimal passing set, rows 1 to 5 (9 points); rows 1 to 5 "can be left out: no", row 6 "yes".
- Overlapping screens: l6 screens 2 and 3 (the order proof and the equality case). New in the task: the proof written from a blank box, the case $q_i = 0 < p_i$ and a fresh pair.

Gates:
1. Validator: `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors, no warning on any info file.
2. Voice: `VOICE_BASE=app/content/courses/info python3 docs/reviews/voice-scan.py 35`: 0 over 35 words, 0 lesson ids in code spans.
3. Numbers script: `<venv>/bin/python docs/reports/info-L2-numbers.py` exits 0; it recomputes the model answer's 0.126 bits and 0.088 nats two ways.
4. Playthrough: `node tools/playthrough.mjs --set info/homework-2 --mobile --local-cdn <pkgs>`: passed at 1280 and 440; the item is marked through Mark my answer and its `-marked` card shows the numbered proof without overflow (a first draft used an `aligned` display that ran past 440 px and was rewritten).
