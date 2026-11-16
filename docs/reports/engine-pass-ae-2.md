# Engine pass AE part 2 (exam pass floor, reuse shapes)

## 1. Exam pass meets a level at half per skill (ENGINE-BACKLOG 1052)

User report, 16 Nov: topic 0.2 exam passed, yet `exp-log` lessons that need `functions` level 2 stayed locked. Cause: met rule 4 asked 0.7 on every essential skill of the level over the attempt's auto rows, and `topic-0.2` holds two `fn-lines` items, so one slip (1 of 2 = 0.5) kept it locked, with nothing on the locked screen saying why.

Changes
- `app/js/prereq.js`: new `EXAM_SKILL_FLOOR = 0.5` (exported; `state.js` mirrors it in `rules`). `examMeets` uses it. 1 of 2 meets, 0 of 2 and 1 of 3 do not, a skill with no auto rows does not. New `examShort(cid, lv)` returns the closest passing attempt's shortfall `{ exam, gaps: [{ skill, correct, total }] }`; `nodeOf` carries it as `examShort`.
- `seenAll`: sitting the exam does mark the skills seen (`examFinished` rates every row through `rate`, which raises `seen`), so the normal case worked. The clause was redundant at best and wrong for a stored attempt whose skill records are gone, so it is dropped from `examMeets`: the attempt's own rows are the evidence. Reviews keep it. Tested with a fresh learner (no lesson, only the exam) and with an imported old attempt with `skills: {}`.
- Read time: `derivedMet` evaluates `examMeets` on every call, and `sync()` writes any newly met level to `state.prereq.met` (`derived`). A stored qualifying attempt unlocks on next load with no migration (tested: met before any `sync`, recorded after it). `unlock` and `refreshFor` read `levelMet`, so they follow.
- `app/js/screens/locked.js` (and `.lk-exam` in `css/screens/locked.css`): a level row whose exam pass does not cover it says "Your topic exam pass does not cover this level: 0 of 2 on straight-line graphs." (stage exams say "stage exam"; a skill with no questions reads "no questions on X"), the label from the courses' `skills` maps as the You screen's fallback; the Test out button stays.
- Other places: no other screen computes the exam rule (exam result, You, course map and `content.js` only read `examPassedAuto` and `examAutoAttempts`). Review and test-out stay at 0.7 (`review.js` unchanged).
- Docs: `docs/AUTHORING.md` met rule 2, `docs/PLAN.md` (new bullet after the XP line; the file had no earlier wording), `docs/ENGINE-BACKLOG.md` 1052 done.

Tests: `tools/test-met-rule.mjs` 24 of 24 (6 new: 1 of 2 meets with no lesson, 0 of 2 names the skill, 1 of 3 not, no auto rows, stored old attempt without migration, review floor 0.7). `tools/test-exam-meets-browser.mjs` (new) reproduces the user's case: a topic 0.2 pass with `fn-lines` 1 of 2 opens `exp-log/l1-doubling`; 0 of 2 locks it, the row carries the line and Test out, no sideways scroll; green at 1280 and `--mobile` (440).

### Content item for later (not fixed): exam, level, essential skill with one auto item

One slip on these locks the level. Count: 109 triples (none with no auto item at all). Computed over every `course.json` with a topic or stage, the level's review skills, and the exam's non-longform items.

| exam | level | essential skill |
|---|---|---|
| topic-2.3 | backtest/L4 | bt-report |
| topic-3.3 | brainteasers/L1 | bz-invariant |
| topic-3.3 | brainteasers/L1 | bz-search |
| topic-3.3 | brainteasers/L2 | bz-strategy |
| topic-3.3 | brainteasers/L2 | bz-invariant |
| topic-3.3 | brainteasers/L2 | bz-search |
| topic-3.3 | brainteasers/L3 | bz-quick |
| topic-3.3 | brainteasers/L3 | bz-search |
| topic-1.11 | complex/L1 | cz-arith |
| topic-1.5 | conditional/L1 | cond-shrink |
| topic-1.5 | conditional/L1 | cond-mult |
| topic-1.5 | conditional/L2 | bayes |
| topic-1.5 | conditional/L3 | cond-mult |
| topic-1.5 | conditional/L5 | bayes |
| topic-1.5 | conditional/L5 | cond-mult |
| topic-0.3 | counting/L1 | ct-comb |
| topic-0.3 | counting/L2 | ct-comb |
| topic-0.3 | counting/L3 | vc-arrows |
| topic-0.3 | counting/L3 | vc-geometry |
| topic-1.5 | counting-chance/L1 | cc-sample |
| topic-1.5 | counting-chance/L1 | cc-count |
| topic-1.5 | counting-chance/L1 | cc-rules |
| topic-1.5 | counting-chance/L1 | cc-symmetry |
| topic-1.5 | counting-chance/L2 | cc-count |
| topic-1.5 | counting-chance/L2 | cc-sample |
| topic-1.5 | counting-chance/L2 | cc-rules |
| topic-1.5 | counting-chance/L3 | cc-rules |
| topic-1.5 | counting-chance/L3 | cc-symmetry |
| topic-1.5 | counting-chance/L3 | cc-count |
| topic-1.9 | cpp-pricing/L1 | cx-testing |
| topic-1.9 | cpp-pricing/L2 | cx-testing |
| topic-1.9 | cpp-pricing/L3 | cx-testing |
| topic-1.4 | eigen/L3 | eg-svd |
| topic-1.4 | eigen/L4 | eg-svd |
| topic-1.4 | elimination/L1 | gx-elim |
| topic-1.4 | elimination/L2 | gx-spaces |
| topic-1.4 | elimination/L3 | gx-elim |
| topic-2.1 | ensembles/L1 | en-interpret |
| topic-2.1 | ensembles/L2 | en-interpret |
| topic-2.1 | ensembles/L3 | en-interpret |
| topic-1.6 | estimation/L3 | es-bayes |
| topic-0.2 | functions/L4 | fn-transform |
| topic-3.3 | game-theory/L1 | gm-normal |
| topic-3.3 | game-theory/L1 | gm-mixed |
| topic-3.3 | game-theory/L2 | gm-sequential |
| topic-3.3 | game-theory/L2 | gm-normal |
| topic-3.3 | game-theory/L2 | gm-auction |
| topic-3.3 | game-theory/L3 | gm-poker |
| topic-3.3 | game-theory/L3 | gm-mixed |
| topic-1.8 | graphs-dp/L3 | gd-backtrack |
| topic-1.3 | integrals/L1 | in-area |
| topic-1.3 | integrals/L2 | in-area |
| topic-1.3 | integrals/L3 | in-area |
| topic-1.4 | least-squares/L1 | ls-qr |
| topic-1.4 | least-squares/L2 | ls-qr |
| topic-1.3 | limits/L2 | lm-rules |
| topic-1.3 | limits/L3 | lm-rules |
| topic-1.3 | limits/L5 | lm-rules |
| topic-1.5 | limits-thm/L3 | dl-lln |
| topic-1.5 | limits-thm/L3 | dl-clt |
| topic-1.10 | linear-maps/L3 | lx-dual |
| topic-1.7 | markets/L2 | fi-bonds |
| topic-1.7 | markets/L2 | fi-equity |
| topic-1.5 | markov/L2 | mc-firststep |
| topic-1.5 | markov/L3 | mc-walks |
| topic-1.5 | markov/L3 | mc-firststep |
| topic-1.5 | markov/L4 | mc-walks |
| topic-1.5 | markov/L5 | mc-walks |
| topic-1.5 | markov/L5 | mc-firststep |
| topic-3.3 | mental-pressure/L1 | mp-speed |
| topic-3.3 | mental-pressure/L3 | mp-speed |
| topic-1.3 | multivar/L1 | mv-partial |
| topic-1.3 | multivar/L2 | mv-partial |
| topic-1.3 | multivar/L3 | mv-partial |
| topic-1.7 | options/L1 | op-payoff |
| topic-1.7 | options/L1 | op-strategies |
| topic-1.7 | options/L2 | op-strategies |
| topic-1.7 | options/L3 | op-strategies |
| topic-3.2 | pdes/L3 | pe-bs |
| topic-3.2 | pdes/L3 | pe-fk |
| topic-3.2 | pdes/L3 | pe-fd |
| topic-3.3 | puzzles/L2 | pz-conditioning |
| topic-3.3 | puzzles/L3 | pz-geometry |
| topic-3.3 | puzzles/L5 | pz-conditioning |
| topic-3.3 | puzzles/L5 | pz-geometry |
| topic-0.2 | quadratics/L1 | quad-model |
| topic-0.2 | quadratics/L2 | quad-model |
| topic-0.2 | quadratics/L3 | quad-model |
| topic-1.5 | random-vars/L1 | rv-dist |
| topic-0.3 | series/L1 | seq-arith |
| topic-0.3 | series/L1 | seq-converge |
| topic-0.3 | series/L2 | seq-arith |
| topic-0.3 | series/L2 | seq-converge |
| topic-0.3 | series/L3 | seq-binomial |
| topic-0.3 | series/L3 | seq-converge |
| topic-2.6 | stat-models/L4 | sm-hier |
| topic-1.3 | taylor/L1 | ty-converge |
| topic-1.3 | taylor/L2 | ty-converge |
| topic-1.3 | taylor/L3 | ty-converge |
| topic-0.4 | terminal/L1 | tm-typing |
| topic-0.4 | terminal/L3 | tm-typing |
| topic-1.7 | trees/L1 | tp-replicate |
| topic-0.3 | trig/L3 | tr-identities |
| topic-0.3 | trig/L3 | tr-equations |
| topic-1.4 | vectors/L1 | la-vectors |
| topic-1.4 | vectors/L2 | la-product |
| topic-1.4 | vectors/L2 | la-vectors |
| topic-1.4 | vectors/L3 | la-inverse |
| topic-1.4 | vectors/L3 | la-product |
