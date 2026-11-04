# Report: measure-prob level 1, "Measures" (topic 3.2)

Brief: `docs/briefs/measure-prob.md`, `## Level 1`, with the brief-check notes R10 and the stale facts applied (analysis L1 to L4, markov L5 and ito L1 now exist; planner scripts recomputed). Ids, names, objectives and skills as in `course.json`.

## Files written (`app/content/courses/measure-prob/`)

| File | Screens | Quiz | Notes |
|---|---|---|---|
| `l1-why-measure.json` | 10 | 4 | number-line (window slider, ten covers, Cantor frames, Vitali points), order with distractors, code, tree |
| `l2-sigma-algebras.json` | 12 | 4 | 1 by 6 grid, tap-regions, multi, number-line, code (`generate`, `is_sigma_algebra`) |
| `l3-measures.json` | 11 | 4 | walk with a `steps` control (R10), series, tables, order with distractors, bars, code (`hit_prob`) |
| `l4-measurable-functions.json` | 10 | 4 | dice grid, plane `steps` CDF and jump with `endpoints`, order, code (`pushforward`, `cdf`) |
| `review-1.json` | 10 items, difficulty 2 to 4 | | two from l1, three from l2, three from l3, two from l4 |
| `homework-1.json` | 8 items, difficulty 3 to 5 | | order (continuity from above), code (`atoms`, `count_events`), parts items (Cantor, VaR), expression, longform d5 (Borel-Cantelli, rubric 10) |

## Validator and playthrough

`node tools/validate.mjs`: 0 errors. Playthrough with `--local-cdn`, desktop and `--mobile`: l1 (14 checks), l2 (16), l3 (15), l4 (14), all quiz 4/4; review-1 10 of 10; homework-1 8 of 8, 35 of 35 marks, parts checks ok. Screenshots looked at (desktop and 390 px); fixed: walk y range and stop at barrier, Vitali shift wraps, stacked labels removed. Voice scan: 0 sentences over 20 words, 0 explanations over three sentences.
Code: `scratchpad/measure-prob-1/codecheck.py` (CPython): every solution passes all its tests (10, 10, 9, 10 and 7) and every starter passes none.

## Proof steps and the widget grading each

- Vitali (l1): why the shifts are disjoint, `choice`; the argument, `order` with `same` (disjoint and cover) and two distractors.
- Rationals have chance 0 (l1): `choice`. Continuity from below (l3): `order`, two distractors. Continuity from above (l3): `choice` for where finiteness is used; homework `order` for the whole proof.
- Right-continuity of F (l4): `order`, two distractors. Left limit as P(X < x): quiz `choice`. Borel-Cantelli: `longform` in homework.

## Numbers and two routes

1023/102400 (closed form and `Fraction` sum); 1024/59049 = 0.0173415 (power and stage-by-stage lengths); first rationals and the 30 listing (construction against sorting by denominator); digital £0.5323 (`erf` and the brief); tree digitals 0.7279, 0.2799, difference 0.4479 (formula and enumeration of four paths, q = 5/9); 4, 8, 16, 6, 64 (generation by closure and atom counting); 1/2, 1/2, 5/8, 5/8, 193/256, 0.9204 (DP, brute enumeration to n = 12, reflection form); 0.1829, 0.6358, 0.2603, 0.3324 (power and exp-log); 1/6, 11/36, 7/12 and the CDF counts (enumeration and formula); 0.9393, 0.1353, £6,931.47; review 0.01969, 64 and 0.0878, 256, 2/9, 8,789 (8000 ln 3), 4%; homework 18 and 262,144, 0.8484, £64,378, 0.01005 (series and 1/99.5). Walk and series figures on screen come from the engine (274 of 300 reached the top, seed 3), never typed by the learner.

## Departures from the brief

- Lesson size: l1 holds ten screens. Moved to the quiz: the irrationals have chance 1, the open against closed end point, the Cantor set is uncountable, and what the Vitali argument shows. l4: the left limit and the pushforward of -ln U moved to the quiz. l2: the edge case (smallest and largest sigma-algebra) is quiz and explanation.
- l3 hook: the walk and the exact series are two screens, not one pair; the series (explore) uses a share-of-steps control. The table asks decimals (0.625) rather than fractions.
- l1 transfer uses a tree with u = 1.25, d = 0.8 so that S_T = K has positive chance (the course tree has ud = 0.96).
- l2 trap is the number 6 then a `derive` choice; l4 has no separate table screen for P_X({7}) and F(4): the numbers are in the tap feedback.
- Prime name once per level: Williams chapters 1 to 3 and Shreve II chapter 1 appear in the l4 summary note.

## course.json

No edit. For the mapping agent: level 1 builds on `analysis/l5-counting-infinite-sets` (listing the rationals, diagonal argument) and, through it, `proof` l7 (combining sets); `course.json` requires only `ito/L1` and `counting-chance/L3`. Proposed: add `"analysis/l5-counting-infinite-sets"` to level 1 `requires`. The Dirichlet function (analysis l20) is not used in level 1.
