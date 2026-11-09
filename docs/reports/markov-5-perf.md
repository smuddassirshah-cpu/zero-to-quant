# markov level 5: performance task

- File `app/content/courses/markov/homework-5.json`, item `h-build-lazy-martingales`, index 10 (item 11 of 11, appended; cap 12, nothing converted). Kind `derivation` (longform, empty box, no tags), difficulty 5, skill `mc-walks`.
- Objective matched (l18): "Build martingales from a random walk, including $S_n^2 - n$ and $(q/p)^{S_n}$." The only verb-rule objective in the level. Its verb is build, but the product is written maths (a martingale and its proof), so the kind is `derivation`, as for measure-prob `h-build-space`.
- Task: a price that moves up, down or pauses ($p$, $q$, $r$). Find and prove $(S_n - an)^2 - bn$ (with $b = p + q - (p - q)^2$) and every $\theta$ with $\theta^{S_n}$ a martingale ($r$ drops out, $\theta = q/p$); then optional stopping, condition checked, for $P = \tfrac{135}{211} \approx 0.640$. Hypotheses stated in the prompt; the model shows $T$ finite with chance 1 by blocks of five up moves.
- Rubric 1, 3, 3, 3; rows 2 to 4 (the three parts) `required` and open with "Tick only if all are given". `rubric-passes.mjs`: passes {2, 3, 4} and {1, 2, 3, 4}; rows 2, 3, 4 "can be left out: no".
- Overlapping screens: l18 screens 3 to 9 lay out the square and power martingales of the no-pause walk (with $4pq$) and prove $S_n^2 - n$; l19 screens 4, 6 and 7 and `h-unfair-ruin-duration` stop them for ruin. New: the pause, its variance, that $r$ drops out of the base, that no other $a$, $b$ or $\theta$ works, checking $T$ finite, the first-step check.

## Gates

1. Validator, `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; expected warning "markov/L5: has a performance task, remove from perf-pending".
2. Voice, `VOICE_BASE=app/content/courses/markov python3 docs/reviews/voice-scan.py 35`: 0 over 35 words; 3 explanations over three sentences, all in `l19-optional-stopping.json`, there before this change; 0 in this item.
3. Numbers script, `<venv>/bin/python docs/reports/markov-5-perf-numbers.py`: exit 0. SymPy for every model line; exact Fraction enumeration of every one-step mean to $n = 12$ and of $P(T > n)$ against the block bound; first-step analysis solved exactly; seeded simulations (200,000 runs give 0.6406); all passing tick sets listed.
4. Playthrough, `node tools/playthrough.mjs --set markov/homework-5 --local-cdn <pkgs>`, with and without `--mobile`: All passed. A full-height render (scratch `model-shot.mjs`) shows 4 display equations, none scrolling sideways at 440 or 1280 px.

Freshness: `fresh-check.mjs --file` 0 hits, also 0 on this item at `--min-run 8 --min-share 0`. Grep terms: `pause`, `stays put`, `p + q - (p - q)`, `4pq`, `135/211`, `211`, `0.00243`, `tick`. Backlog: 0 bullets (the cut "required" label is BACKLOG-INBOX line 1652). No course.json change.
