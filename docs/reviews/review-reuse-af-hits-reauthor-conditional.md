# Re-author of the AF reuse hits: conditional

Brief `docs/briefs/reauthor-af.md`; verdicts from `docs/reviews/review-reuse-af-hits.md`. Both items replaced whole; both ids changed because the old ids named the old stories.

- `problems-3.json` items[1] | old `p-losing-week`: a losing week from a failed signal or a squeeze, explained away by the squeeze (walked `l16` screens[7], [8] and quiz[2]) | new `p-rotation-days`: X and Y independent over all days, linked up on risk-on days and pushed apart on rotation days; the rotation-day chance is unmixed from the pooled one | skills cond-indep, cond-traps; lessons l13, l16; difficulty 4 | keys 0.48, 0.24, 0.4, choice `both-dep`
- `problems-4.json` items[3] | old `p-dated-coins`: gold and silver coins with mint years, a $k$-value detail and its limit (walked `l19` screens[5], [7], `l21` screens[4] to [8]) | new `p-dark-fills`: orders of one or three fills, a fill drawn at random against a yes to "at least one dark fill" | skills cond-traps, bayes, cond-count; lessons l19, l21; difficulty 5 | keys 0.6667, 0.6667, 0.488, 0.6193 (122/197), choice `ratio`

Closest lesson, quiz, review, homework and exam items for each, with the reason neither is a walk: `docs/reports/problems-conditional.md`, section "Re-author, session AF".

## Gates

- Validator: 0 errors; no warnings on problems-3 or problems-4.
- Voice scan 35 (course folder): 0 and 0.
- `fresh-check --file`: 0 hits on problems-3 and problems-4.
- `same-course-reuse --all | grep conditional`: no error (one waived line on `p-two-strategies`, unchanged).
- `grade-all --file --local-cdn`: 0 failures on both sets (17 and 18 widgets).
- Playthrough `--problems` with `--local-cdn`: green for both, with and without `--mobile`; 440 px shots of every part of both new items read, no fault.
- Number scripts: `problems-conditional-numbers.py` 1,198 checks, 0 failures. Reader checks of the replaced items retargeted (old checks tested the old stories): `conditional-L3-concepts.py`, `conditional-L3-concepts-r2.py`, `conditional-L1-3-concepts-r3.py`, `conditional-L4-5-concepts.py`. Every conditional script in `docs/reports` exits 0.
