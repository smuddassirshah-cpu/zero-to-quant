# llm-apps level 2: Language models in quant research (report)

Branch `ai-w7-llm-apps`. Brief: `docs/briefs/llm-apps.md` Level 2. `post-train` L4 is not written; l5 screen 4 gives the n-gram overlap test in one screen with its own example, using the definition in `docs/briefs/post-train.md` Level 4 (share of the item's n-grams found in the other text), and names `post-train` level 4.

## Files

| File | Screens / items | Code widgets (tests, mutants) |
|---|---|---|
| `l5-what-the-model-knows.json` | 12 screens, quiz 4 | `clean_window` + `share_after_cutoff` (7, 3); `sharpe_by_period` (6, 3) |
| `l6-text-as-a-feature.json` | 12 screens, quiz 4 | `known_by` + `asof_feature` (7, 4); `decayed_score` (7, 3) |
| `l7-leaks-in-text.json` | 12 screens, quiz 4 | `fit_vocab_in_fold` + `transform` (7, 4); `mask_entities` + `masking_effect` (5, 4) |
| `l8-an-honest-text-backtest.json` | 12 screens, quiz 4 | `haircut` (4, 3); `honest_backtest` (5, 4) |
| `review-2.json` | 10 items, pass 0.8 | none |
| `homework-2.json` | 6 items: performance code task `h-text-signal` (7, 4), code `h-masking` (5, 4), order with two distractors, longform (10-point rubric), numeric, choice | 2 |
| `problems-2.json` | 3 chained problems, 12 parts (difficulty 5, 4, 3) | none |
| `app/content/data/ai/llm_apps_ops_l2.py` | shared module v1.0 (signatures below) | |

Performance task: `docs/reports/llm-apps-2-perf.md`.

## Self-check (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors (no `[source-ban]`, no `[ai-mutants]`).
2. Voice scan with `VOICE_BASE=app/content/courses/llm-apps`: 0 over 35 words, 0 lesson ids in code spans.
3. `docs/reports/llm-apps-L2-numbers.py` through `run-number-scripts.mjs`: passed (strict, 348 of 348 checks, 0 uncovered, 14 literals with reasons).
4. Playthrough with `--local-cdn`, desktop and `--mobile`: l5 to l8 ok (quiz 4/4 each), `review-2` 10 of 10, `homework-2` 6 of 6 with the performance starter failing and the longform marked, `problems-2` 3 problems, 12 parts. All passed.
Also: `grade-all.mjs --code --strict-feedback` on all seven files, 0 failures; `same-course-reuse.mjs --all` lists nothing for `llm-apps`; `perf-reports.mjs` no gap.

L1 change made here: `homework-1` item `h-retriever` gained `prelude: "import numpy\n"` so that the heavy-import time allowance applies (its setup imports the L1 module, which imports NumPy); replayed with and without `--mobile`, green; `llm-apps-L1-numbers.py` still passes.

## The seeded market (no language model)

`make_market(seed=0)`: 2,000 business days from 4 January 2016 to 1 September 2023; daily return `0.0005 * signal + 1% noise`; one document a day at a uniform minute from 08:00 to 19:59. A document's score is the real signal, plus twice the next return in sd units before the cut-off (day 1,500, 1 October 2021: memory), plus twice the next return if published after 16:30 (late news), plus 0.3 in the last 250 days (a vendor update). The prose says the generator plants these parts and that there is no language model.

## Numbers and their sources

Route A is the builder (NumPy, pandas `merge_asof`); route B in the script rebuilds the as-of feature with `bisect` on publication strings and every Sharpe and standard error with `statistics`, dates with `datetime`.

- As-of feature, sign trading: Sharpe 9.2165 before the cut-off, 0.9960 after (planner's sketch said 15.5 and 1.7 for a design without timestamps; this level's own figures are stated); clean daily mean 0.0605%, sd 0.9640%; before 0.5058% and 0.8711%. Hit rates: 52.8% after (as-of), 65.6% after (date join, the timestamp leak, +12.8 points), 74.6% before (memory). Share after the cut-off 0.25.
- n-gram check: 16-word story, model repeats 12 words: 8 of 12 five-grams (0.6667), 10 of 14 three-grams (0.7143).
- l6: Tuesday mean 0.1333, Wednesday window mean 0.10, as-of Wednesday 0.1; d1 is 2.3021 days old at Wednesday's close, weight 0.2028 at half-life 1; decayed score 0.2032; quarter end to publication 39 days.
- l7: three words of the 2022 note outside the 2018 to 2020 vocabulary; IDF of 'sales' 1.2877 in the fold, 1.4055 on all years; masking mean change 0.15, sd 0.1731, standard error 0.0612 (2.5 standard errors); four-headline case mean −0.0050, standard error 0.0520.
- l8: haircut of 2.1 with 12 tries over 2 years 0.5236 (noise best 1.5764); 55 tries make a noise best of 2 over 2 years ($e^4 = 54.6$); costs of 0.02% a day take the clean Sharpe to 0.67; six months needs 2.77; four designs: all dates 6.84, date join after the cut-off 4.90, full-window threshold 0.27, walk-forward 0.47 (the full-window leak lowers the figure in this seed, and the screen says a leak can err either way).
- Review, homework and problem-set figures (0.1875, 1.06, 0.6875, 0.7071, 45 days, 0.04, 1.9163, 0.29, 1.75 years; 0.2, 2 years, 1.7941, 0.6059, 1.39; 1.3056 days, 0.4046; 0.1033, 0.1181, 0.0482, 2.14) are each recomputed in the script.

## Shared module `llm_apps_ops_l2.py` (v1.0; frozen once merged)

- `make_market(seed=0, days=2000, cutoff_day=1500, edge=0.0005, memory=2.0, late=2.0, drift=0.3) -> {"dates", "ret", "signal", "cutoff", "docs", "close"}` (docs: `{"published": 'YYYY-MM-DD HH:MM', "day", "score"}`, scores rounded to 6 places).
- `long_short_sharpe(pnl) -> float` (mean over n − 1 sd, times $\sqrt{252}$).

Data and provenance: no data file added. The market, its documents and every headline, note and company name in this level are **invented** (seeded or written for the lessons).

## Timing

Every hidden test is far under a third of its limit. The market tests (`make_market` then a pure-Python backtest) take well under a second each after the packages load; the widgets that touch the market import NumPy and pandas in the prelude so the page's heavy-import allowance covers the package load.

## course.json

No change proposed.

## Backlog

Two bullets under "Raised later (llm-apps level 2)" in `docs/BACKLOG-INBOX.md`.
