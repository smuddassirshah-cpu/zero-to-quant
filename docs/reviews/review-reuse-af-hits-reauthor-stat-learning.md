# Re-author of the AF reuse hits: stat-learning

Brief: `docs/briefs/reauthor-af.md`. Verdicts: `docs/reviews/review-reuse-af-hits.md` (stat-learning lines). Closest course items and why each new part is not a walk: `docs/reports/problems-stat-learning.md`, section "Re-author, session AF".

## Items

- `problems-2.json` `p-futures-lasso` (id kept; still a futures desk). Old task: five z-scored futures signals, `Lasso(alpha=0.15)`, count survivors, one coefficient after the penalty, the emptying $\alpha$, a standardised carry, a forecast. New task: a power futures desk's three uncorrelated z-scored signals (gas 2.0, wind $-1.2$, demand 0.5, intercept 0.2; next month's z-scores $-0.5$, $-1.0$, 2.0); the forecast followed along the lasso path. Keys: part 1 OLS forecast 1.4; part 2 forecast at $\alpha = 0.2$, 0.9; part 3 first $\alpha$ where the forecast reaches 0, 0.8; part 4 forecast at the chosen $\alpha = 1.0$, $-0.1$. Skills `sl-regularise`, `sl-linear`; lessons l5, l8.
- `problems-2.json` `p-built-ridge` (id kept; the item now builds a ridge fit by hand). Old task: `homework-2.json` items[4]'s built uncorrelated market with expected test MSE and the factor $n/(n + \lambda)$. New task: a market maker's two correlated z-scored signals on 50 hours ($\sum x_1^2 = \sum x_2^2 = 50$, $\sum x_1x_2 = 40$, $\sum x_1y = 60$, $\sum x_2y = 30$) and four held-out hours. Keys: part 1 OLS coefficient on quote updates $-1.0$; part 2 ridge coefficient at $\lambda = 10$, $-0.3$; part 3 ridge test MSE 0.355; part 4 ridge test $R^2$ 0.897. Skills unchanged; lessons l5, l7.
- `problems-4.json` `p-renewals` part 2 only. Old task: a validation tie broken towards logistic regression. New task: the network (129 parameters on 320 fitting rows) scores 0.96 and 0.75, logistic regression 0.80 and 0.78, the RBF SVM 0.84 and 0.77; choose on validation. Key: option `logistic`; distractors `network`, `svm`, `refit`. Parts 1, 3 and 4 untouched.

Other items of both sets untouched; no waiver added.

## Gates

- `node tools/validate.mjs`: 0 errors; no warning on the new parts (the `[wrong-band]` warnings on `problems-4` `p-order-sizes` predate this pass).
- `VOICE_BASE=app/content/courses/stat-learning python3 docs/reviews/voice-scan.py 35`: 0 and 0.
- `node tools/fresh-check.mjs --file`: `problems-2` 0 hits, no advisory; `problems-4` 0 hits, two advisory lines on part 2's generic split numbers (400 with 0.02 against `problems-1` items[3], 400 with 80 against `review-2` items[6]), read and judged stock numbers.
- `node tools/same-course-reuse.mjs --all | grep stat-learning`: no error; only the three waived `problems-1` lines.
- `node tools/grade-all.mjs --file ... --local-cdn`: `problems-2` 0 failures (18 widgets), `problems-4` 0 failures (19 widgets).
- Playthrough `--problems stat-learning/problems-2` and `problems-4`, with and without `--mobile`: all passed; 440 px shots of the new parts read, no layout fault.
- `docs/reports/problems-stat-learning-numbers.py`: exit 0 (1269 checks), lasso and ridge blocks rewritten, `p-renewals` part 2 checks added. `docs/reports/problems-stat-learning-numbers-read.py`: exit 0 (2197 checks), its `p-futures-lasso` and `p-built-ridge` blocks retargeted to the new items. `fluency-stat-learning-numbers.py`, `stat-learning-2-perf-numbers.py`, `stat-learning-4-perf-numbers.py`: exit 0. `stat-learning-L4-numbers.py` (not touched by this pass) did not finish inside a 115 s limit here, so it was not judged.
