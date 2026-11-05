# research-int level 1: performance task pilot (PLAN 2c item 5)

## What was added

One item, `h1-signal-aloud`, appended to `app/content/courses/research-int/homework-1.json` (8 items to 9; the limit is 12, so nothing was converted). Kind `aloud`, difficulty 5, `skills: ["rq-stats"]`, tags `p-value-meaning`, `power`, `multiple-testing`, pace 420 s, clock 120 s, three follow-ups, a four-line rubric (3, 3, 3, 1 = 10). No data file.

## Why this kind and this file

- The verb rule matches level 1 on two objectives: l3 "Derive a quick estimator..." and l4 "Explain a p-value, power and a multiple-testing correction without jargon." Neither is about analysing data, so the brief's rule gives `aloud`, not `data`.
- The task asks for exactly the l4 product: a spoken, jargon-free explanation of all three named ideas (p-value, power, correction) to a listener with no statistics.
- `aloud` is a longform, and longform lives in homework only, so `review-1.json` was not an option.
- It does not repeat `h1-thirty-signals` (written, p-value and correction only): this one adds power, a non-specialist listener, a clock and follow-ups, with new numbers (twenty versions, five years, Sharpe 1).

## Numbers (all in `docs/reports/research-int-1-perf-numbers.py`, each by two methods)

| Figure | Method 1 | Method 2 | Stated |
|---|---|---|---|
| $t$ for Sharpe 1 over 5 years | $\sqrt5$ = 2.2361 | same | 2.24 |
| two-sided p | $2(1-\Phi(\sqrt5))$ = 0.02535 | seeded simulation, 400,000 draws | 0.025, "one time in 40" |
| power, 5 years | $\Phi(\sqrt5-1.96)+\Phi(-\sqrt5-1.96)$ = 0.6088 | simulation | 0.61, "six times in ten" |
| best of 20 unrelated reaches 0.025 | $1-0.975^{20}$ = 0.3973 | binomial sum | "four times in ten" |
| Bonferroni bar, ratio | 0.05/20 = 0.0025, 0.025/0.0025 = 10 | | 0.0025, "tenfold" |
| years for 80% power | $(1.95996+0.84162)^2$ = 7.849 | bisection on the power curve | "about eight"; rounded form $2.8^2$ = 7.84 |
| Holm, BH on twenty p-values with minimum 0.025 | procedures run | brute force over $k$ | Holm 0; BH 0 with weak versions, 20 when all are under 0.05, needs at least 10 doing well |

## Self-check

1. `node tools/validate.mjs`: 0 errors. Expected warning: "research-int/L1: has a performance task, remove from perf-pending" (perf-pending.json untouched).
2. Voice scan (`VOICE_BASE` = the research-int folder): 0 explanations over three sentences, 0 sentences over 20 words.
3. `python3 docs/reports/research-int-1-perf-numbers.py`: exit 0, every pair agrees.
4. `node tools/playthrough.mjs --set research-int/homework-1 --local-cdn <pkgs>`: all passed, desktop and `--mobile` (9 of 9 right, 48 of 48 marks).

Screenshots looked at (desktop and 440 px), plus a scratch Playwright script that clicks the real buttons: the clock starts and counts, the three follow-ups and the model render after marking, no sideways scroll, no console errors.

## Finding and workaround

The homework page's Mark my answer button refuses an empty box ("Write your working first", `js/screens/review.js` line 1001), though the aloud widget calls the box optional. The playthrough misses this because its hook grades without the button. Workaround: the item's `question` asks for one line of notes before marking. Raised as a [Must] in `docs/BACKLOG-INBOX.md`.

## course.json

No change proposed.
