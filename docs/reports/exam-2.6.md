# Topic 2.6 exam: statistical modelling

File: `app/content/exams/topic-2.6.json` (75 minutes, pass 0.7, 25 items, all six skills of `stat-models`). Scripts: `docs/briefs/exam-2.6-scripts/` (`build.py` route A, `check_numbers.py` route B, `fresh.py`).

## Result

- Ramp 5, 13, 5, 2 at difficulties 2 to 5; pace 3,420 s (57 min).
- By level: L1 6 (sm-glm), L2 5 (sm-anova, and sm-nonpar first met in l9's sign test), L3 6 (sm-nonpar: rank, permutation, KDE, robust; plus Hodges-Lehmann and a rank ANOVA, defined in the prompts and not taught in the course), L4 7 (sm-bayes, sm-mcmc, sm-hier), plus the rank ANOVA across L2 and L3. L3 has no new skill, so it is covered through sm-nonpar items on its own lessons.
- Kinds: 16 numeric, 1 choice, 1 multi, 1 table (ANOVA from three brokers' orders), 4 parts, 2 Python code (`walsh_median`, `kruskal_h`). No longform.
- Finance data throughout: PDs, trade counts with an offset, slippage, shortfall, fill and default rates, fund alpha, rejected orders.

## Gates

- Validator: 0 errors, no topic-2.6 warnings.
- Voice scan on a copy: 0 and 0. No em-dashes or exclamation marks.
- `check_numbers.py`: 215 of 215, exit 0. Fractions, tanh for the inverse logit, Simpson integrals of the chi-square and gamma densities, bisection for normal quantiles, brute-force pair counts, and the classic Kruskal-Wallis formula with its tie correction. Both code solutions pass every hidden test in CPython, and both starters fail every one. The seven "check by hand" lines are rounded or per cent forms of the wrong values.
- Playthrough with `--local-cdn`: green with and without `--mobile`; screenshots checked. Table placeholders were clipped at 440 px, so the cells now have none.

## Freshness

Three clashes were changed. The alpha prior $N(0, 2^2)$ with a 4% error is l14's ladder, so it became $N(0, 1.5^2)$ with 8% and 3%. The scaled MAD 0.4448 is l13's key, so one return moved and it became 0.5930. "A every morning" is l8's confounded design, so the distractor became January against February. Other hits are common numbers in other courses.
