# Prerequisite mapping: topic 3.2 (`ito`, `measure-prob`)

Edited: `app/content/courses/measure-prob/course.json` (two `requires` lists), `app/content/courses/ito/course.json` (strand fields), `app/content/prep.json` (one step). Nothing else. Pattern: `docs/reports/prereq-mapping.md`.

## Requires: added

- `measure-prob/L3`: added `random-vars/l17-variance-given-information` and `least-squares/l5-dropping-a-perpendicular`. l10 splits the variance as Var(E[Y|X]) + E[Var(Y|X)] and calls the conditional expectation an orthogonal projection with a perpendicular residual. Neither lesson sits in the closure of `measure-prob/L2`, `markov/L5` or `ito/L2` (random-vars l17 is in `random-vars/L5`, whose level is not reached).
- `measure-prob/L4`: added `estimation/l5-which-fits`. l15 uses the likelihood ratio from it. It is not in the closure of `measure-prob/L3` or `ito/L3`.

## Requires: rejected

- `measure-prob/L1` on `analysis/l5-counting-infinite-sets`: the lessons do rely on countability (the rationals, the Cantor set, the Vitali set), but `analysis` is a Pure course and AUTHORING section 11 says a Pure course never gates a Quant course. It would also pull a hidden course into Quant-only mode (analysis L1 adds `proof/L3`). Left as in the first mapping. If the owner wants it, relax the strand rule or add a recap screen to l1; one line in `course.json` adds the reference.
- `measure-prob/L2` on `analysis/l19` and `l20` (brief check): same strand rule, and the level report says it quotes them in one sentence each with no dependence. The author's list (`measure-prob/L1`) is already the implicit default, so no edit. The `trees` numbers it quotes (l9, l10) are in the closure of `ito/L1`.
- `ito/L2`: no change. integrals l1 and l2 are in `integrals/L1` and `L2`, already in the closure of `taylor/L2` and `ito/L1`; markov l10 is in `markov/L3`, which `ito/L1` requires; random-vars l15 is in `random-vars/L4`, already listed.
- `measure-prob/L3` extra optional names (random-vars l15, markov l17 to l20, trees l3 and l5): inside the existing closures, so not listed.

## Course card line (ito)

`course.json` has no free-text card line. The nearest field is the strand badge, so `ito` gets `"strand": "quant"` and `"strandNote": "Needed for strats and desk quant interviews (banks), rarely for trading firms."`. The badge detail shows that line. Topic 3.2 mixes `ito` and `measure-prob` (both Quant) and `pdes`; the topic chip appears only if `pdes` carries the same strand, which is outside this pass.

## Prep path

- `interview-strats`: added `ito/level-4` (should), after `ito/level-3`. `superday-strats` already has it as must, and `firm-jp-morgan` already has `ito/l13-martingale-or-not` as reported.
- Not added: `interview-research` and the trader paths (stochastic calculus is not asked there per their steps), `oa-*` paths (no OA item), and Goldman Sachs and Morgan Stanley firm paths (their reported process in `recruiting/l4-firm-by-firm` names no Brownian motion or martingale question; Morgan Stanley already lists `ito/level-2`).
- No new "Desk quant" path: section 10 allows only general, stage and firm paths, and the strats paths are the desk-quant fit.

## Closure change (levels a fresh learner must clear first, direct and indirect, counted with each referenced lesson's level)

| Level | Before | After |
|---|---|---|
| ito L1 | 54 | 54 |
| ito L2 | 62 | 62 |
| ito L3 | 63 | 63 |
| ito L4 | 76 | 76 |
| measure-prob L1 | 56 | 56 |
| measure-prob L2 | 57 | 57 |
| measure-prob L3 | 78 | 84 (+6: `random-vars/L5` and its chain through `limits/L5`, `least-squares/L2`) |
| measure-prob L4 | 80 | 88 (+8: the L3 additions and `estimation/L2`) |

`pdes/L1` stays at 91 (it needs `ito/L3`, not `measure-prob`).

## Checks (from `app/`)

- `node tools/validate.mjs`: 0 errors, 606 warnings, no cycles; none new from these edits.
- `node tools/playthrough.mjs --routes-only --local-cdn <pkgs>`: All passed (gating check included).
