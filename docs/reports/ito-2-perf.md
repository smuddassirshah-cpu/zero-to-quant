# ito level 2: performance task pilot (PLAN 2c item 5)

Rules: DECISIONS "Performance tasks (5 Nov 2026, user decision)"; AUTHORING sections 5, 7 and 11; `docs/reports/engine-pass-item5.md`.

## What was added

- File: `app/content/courses/ito/homework-2.json` only. One item appended, `h-derive-ito` (item 9 of 9). Nothing converted: the homework had 8 items, the limit is 12.
- Kind: `derivation`, a `longform` with an empty box. No starter, steps, order, derive, hints or parts. Difficulty 5, skill `it-calculus`, no `tags`, so it stays out of the Interview practice deck.
- Objective matched by the verb rule: l6 "Derive Itô's lemma from a second-order Taylor expansion." The task asks for exactly that product. The learner writes $df(t, X_t)$ for $dX = a\,dt + b\,dW$ and justifies each line. They state the conditions, then check the result on $f = e^{x - t/2}$ with $X = W$. (l5 "Build the Itô integral" also matches; at most one task per level, so the derive objective was chosen as the brief directs.)
- Model: conditions stated exactly. $a$ and $b$ are adapted; $\int_0^t |a_s|\,ds < \infty$ and $\int_0^t b_s^2\,ds < \infty$ almost surely; $f \in C^{1,2}$. The model then runs the Taylor expansion and its $C^{1,2}$ variant, first order in $t$. It applies the table and gives a reason for each vanishing term and the remainder. It collects the result and gives the integral form, with a reason why both integrals exist. A caution follows: the $dW$ integral is a local martingale, and a true one when $E[\int_0^t b_s^2 f_x^2\,ds] < \infty$. Last comes the check, $E[\int_0^t e^{2W_s - s}\,ds] = e^t - 1$.
- Rubric: five criteria of 2 points each: conditions, expansion, table, collected result with Itô integral and mean-zero condition, check. A pass at 7 of 10 therefore needs four of the five.
- Homework limits after the change: 9 items (6 to 12), a difficulty 5 present, two longform items, one `order` part. All of these are checked by the numbers script.

## Self-check (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors. The expected warning "ito/L2: has a performance task, remove from perf-pending" appears, and the pending count reads 110 of 111. `perf-pending.json` was not edited.
2. `docs/reviews/voice-scan.py`, with `VOICE_BASE` set to the ito folder: 0 explanations over three sentences, 0 sentences over 20 words. At MAX 19 the new item also shows 0.
3. `python3 docs/reports/ito-2-perf-numbers.py`: exits 0 after 41 checks. Symbolic route A uses sympy: the multiplication table is applied to the full and to the $C^{1,2}$ expansion. Symbolic route B is a real Taylor series with $dt = \varepsilon^2$ and $dW = \varepsilon z$, run on four functions. The script then checks the partial derivatives in the check, $E[e^{W_t - t/2}] = 1$, $E[e^{2W_s - s}] = e^s$, $\int_0^t e^s\,ds = e^t - 1$, and the wrong-rule mean $e^{-t/2}$. The numeric half is seeded. It gives the grid sums of the table ($\sum(\Delta W)^2 = 0.9952$ at $n = 2^{16}$). It checks the lemma pathwise in integral form for an Itô process with adapted $a, b$: the gap is 0.0021 at $2^{14}$, against 0.042 for the ordinary chain rule. The last numeric checks are finite differences and Monte Carlo moments with standard errors. Without sympy, the numeric half still runs.
4. `node tools/playthrough.mjs --set ito/homework-2 --local-cdn <pkgs>`: all passed, with and without `--mobile`. The shots were checked at 1280 and 440 px. A scratch Playwright script (scratchpad `ito-2-perf/model-shot.mjs`) opened Mark my answer and shot the model and rubric. Two display equations scrolled sideways at 440 px. Both were split with `aligned`, and they now fit with no sideways page scroll and no page errors.

`app/content/manifest.json` restored before commit.

## Backlog

Four bullets under "Raised later (ito level 2 perf pilot):" in `docs/BACKLOG-INBOX.md`. They cover start-card grammar, no marker for the performance task, no required rubric row, and a playthrough that never opens the marking panel.

## course.json

No change proposed.
