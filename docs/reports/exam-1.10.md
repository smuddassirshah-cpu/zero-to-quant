# Topic 1.10 exam: analysis and proof-based linear algebra

File: `app/content/exams/topic-1.10.json` (100 minutes, pass 0.7, 30 items, all twelve skills of `analysis` and `linear-maps`). Scripts: `docs/briefs/exam-1.10-scripts/` (`build.py` route A, `check_numbers.py` route B, `fresh.py`).

## Result

- Ramp 6, 15, 6, 3 at difficulties 2 to 5; pace 5,220 s (87 min).
- By course and level: analysis L1 3, L2 3, L3 3, L4 4, L5 5; linear-maps L1 2, L2 3, L3 2, L4 5.
- Coverage: every level of both courses has an auto-graded item on a skill first met there (`check_numbers.py` checks this from `course.json` and the lesson files).
- Kinds: 13 parts, 5 numeric, 4 choice, 2 multi, 2 expression, 3 order proofs with two flawed lines each, 1 longform (self-marked, 10-point rubric; every skill is also on an auto item).
- Proofs: compact sets are bounded in any metric space (L5), a projection splits $V = \ker T \oplus \operatorname{im} T$ (L2), a contraction has a fixed point (L2 with L4). The longform proves that the top eigenvalue bounds $\mathbf{x}^T\mathbf{A}\mathbf{x}$, then reads it as the largest unit-portfolio variance.

## Gates

- Validator: 0 errors, no topic-1.10 warnings.
- Voice scan on a copy (`VOICE_BASE=<scratch>/voice110/`): 0 sentences over 20 words, 0 explanations over three sentences, 714 sentences. No exclamation marks, em-dashes or en-dashes.
- `check_numbers.py`: 327 of 327, exit 0. It checks every key, every `wrong`, every expression form (LaTeX evaluated at sample points against route B), every choice key, and `check_wrongs`. A final pass reads every number in every learner-visible string. Whole numbers 0 to 10 pass as structure; every other number must match a route-B value to its printed precision.
- Playthrough with `--local-cdn`: green with and without `--mobile` (30 of 30); screenshots at 1280 and 440 px checked.

## Freshness

Three clashes were changed. The ratio-test series $\sum n^2/3^n$ is analysis review-3's; it became $\sum n^3/2^n$. The gap-two telescope sat beside review-3's; it became $\tfrac{1}{n(n + 3)}$. The mean value item on $x^3 + x$ over $[0, 2]$ keyed 1.1547, the key of limits l17; it became $x^4 + x$. The density gap (0.31, 0.32), the shift map $p(x + 1)$, the map $xp'$ and the weighted product $2x_1y_1 + x_2y_2$ were lesson or review examples, so they were replaced before the first build. Other hits are unrelated numbers in other courses.
