# Prerequisite mapping (`requires`): second-reader findings

Scope: every `requires` and `lessonRequires` in `app/content/courses/*/course.json` (279 levels, 76 courses, 172 explicit lists, one `lessonRequires`), against `docs/briefs/prereq-gating.md` sections 1 to 3 and 8, `docs/AUTHORING.md` section 11, the mapping report `docs/reports/prereq-mapping.md` and its data, each course brief's "Context" and "Builds on" lines, `breadth-plan.md`, `gaps-plan.md`, `interview-plan.md`, `curriculum.md`, and lesson objectives.
Method: a script loaded every `course.json` and built the level graph (lesson references folded into their level). It checked the hard rules (Pure strand, stage order, same-stage topic order), found references implied by another reference of the same level, computed transitive closures, and measured how many closure levels each direct reference adds alone. A second script scanned every written lesson, review and homework for lesson ids of other courses and tested each against the closure of its level. For the interview courses (topics 0.7, 3.3, 3.5) every reference was compared with the brief text. Scripts: `/tmp/claude-0/-home-user-zero-to-quant/024bfe09-7a97-56c3-837c-b47a15727adf/scratchpad/` (`g.py`, `c.py`, `f.py`, `h.py`, `i.py`); nothing in the repo was edited except this file.
Format: numbered; course, level, current references, proposed references, reason. Severity: error = a gate contradicts a written lesson or a brief-named dependency is missing; warning = over- or under-gating that changes what a learner must do; note = optional tidy-up or a decision recorded.

## Verified as the report states

- No Pure-strand course gates a Quant or interview course (0 violations). No earlier-stage-to-later reference (0). No later-topic-same-stage reference (0). No cycle.
- Longest chain 34 levels (`momentum-rep/L3`), largest direct list 5, `research-int/L3` closure 85 levels (83 outside the course): all reproduced.
- Interview references the brief does not name: exactly one (warning 1, `brainteasers/L1` on `contests/L2`). One more is named but implied (note 1, `systems/L1` on `cpp/L4`). Every other interview reference traces to a "Prerequisites", "Builds on" or "Context: the learner has" line.
- None of the 35 unwritten-level warnings locks a written level in this checkout (section "Unwritten levels").

## Errors

1. **puzzles, L2.** Current: `puzzles/L1`, `conditional/L2`, `markov/L3`. Proposed: add `limits-thm/L2`; then `puzzles/L3` needs only the implicit `puzzles/L2` (delete its list). Reason: the brief's L2 context says to read `limits-thm/l6-uniform-exponential`, and the written `l11-largest-of-several` is built on uniform draws and densities (20 uses of "uniform", 11 of "density"; `game-theory` L1 cites it for E[max] of n uniforms). A fresh learner reaches `l11` without continuous distributions today and meets them only at L3. Closure of L2 goes 32 to 44.
2. **coding-int, L1.** Current: `graphs-dp/L4`, `algo-think/L3`, `contests/L1`, plus `lessonRequires` `l5-bit-tricks` on `contests/L3`. Proposed: level list `graphs-dp/L4`, `algo-think/L3`, `contests/L3`; delete the `lessonRequires`. Reason: the written `l1-merging-intervals` cites `contests/l10-greedy-proofs` (level 3) and `l5-bit-tricks` cites `l11-bitmasks`; `review-1` items `r1-and` and `r1-xor` and `homework-1` test bit tricks. Review and homework keep the level list, so a learner can pass `review-1` or test out of the level on bit tricks they are locked out of. Level-wide `contests/L3` costs only two more closure levels (`contests/L2`, `L3`; closure 25 to 27), because `contests/L1` is already there and `coding-int/L4` needs the chain anyway.
3. **coding-int, L2.** Current: `coding-int/L1`, `micro/L1`. The written `l8-simulating-the-rules` says "`contests/l15-debugging-under-time` showed how slow it is to debug without...", which is in `contests/L4`, named only by the brief for `coding-int` level 4. Proposed: reword that sentence in `l8` (a fix-agent edit of one lesson, not a gate change); do not add `contests/L4` to L2, which would hold the course's second level behind the whole contests course. Reason: the gate says the learner has not met l15, the lesson says they have.

## Warnings

1. **brainteasers, L1.** Current: `counting-chance/L2`, `contests/L2`. Proposed: L1 `counting-chance/L2` only; L3 becomes `brainteasers/L2`, `mental/L3`, `series/L2`, `exp-log/L3`, `contests/L2`. Reason: `contests/L2` adds 21 of L1's 28 closure levels (all of `ds`, `graphs-dp` L1 to L2, `algo-think`) to hold five logic lessons whose objectives (invariants, colouring, pigeonhole, weighing, jugs) use no code. The brief names `contests` only under "No overlap: this course does not repeat ... the invariant lesson in `contests`", and the plan's course prerequisites are `proof`, `counting-chance` L2, `graphs-dp` L3. The one genuine use is `contests/l5-modulo` for `l13-digits-and-remainders` in L3. Also in L3 the brief cites `mental` l10-known-decimals (level 3), so `mental/L3` replaces `mental/L2`. Closure L1 28 to 7, L3 36 to 37.
2. **micro, L1 (reaches mm-games L1, coding-int L2, game-theory L2, alpha, backtest).** Current: `markets/L2`. Proposed: `micro/L1` requires `markets/l7-shares`, and `markets` gets `"lessonRequires": {"l7-shares": ["ratio/L2"]}`. Reason: the mapper's reason is "bids and asks of shares", which needs `l7-shares` (shares, market capitalisation). `markets/L2` implicitly requires `markets/L1` (compound interest, `exp-log/L3`, `series/L3`), which the order-book lessons never use. Without the override the lesson reference does not help, because `l7` stays locked behind its level. `mm-games/L1` closure 23 to 14, `coding-int/L2` 35 to 30. If the owner wants `markets` taken as a unit, keep the current list and record the cost.
3. **counting-chance L3 before `conditional/L1` and `random-vars/L1` (the mapper's doubtful item).** Current: both on `counting-chance/L3`. Proposed: both on `counting-chance/L2`. Reason: L1 objectives are counting inside B, the multiplication rule for draws and a tree; `random-vars/L1` defines a function on the sample space and a mass function. None uses inclusion-exclusion, the birthday problem, the axioms or poker hands (`l9` to `l12`). Where a brief names L3 content, add `counting-chance/L3` there instead: `game-theory/L3` (l12-poker-hands), `mental-pressure/L4` (l10-birthday), and keep it on `measure-prob/L1` (l11-axioms; it is genuine, only hidden today because `conditional/L1` implies it). `brainteasers/L3` cites `l9-double-counting` for "counting twice": note only, no gate. Shortens the Stage 1 probability spine by one level for about 60 levels.
4. **linear-maps, L2 (Pure).** Current: `linear-maps/L1`, `least-squares/L1`, `eigen/L4`. Proposed: `linear-maps/L1`, `least-squares/L1`, `eigen/L1`. Reason: `eigen/L4` is named for `l13-same-map-new-basis`; its level also needs `taylor/L2` and `multivar/L4`, and the lesson uses neither (`l14` uses series, `l16` uses `multivar`). The change of basis of a matrix appears in `eigen` l3-eigenbasis. Closure 52 to 34. After the change `eigen/L2` on `linear-maps/L4` stops being implied and is genuine (spectral theorem, l5 to l8). The mapper's own drop-if-too-heavy note applies. Also drops `algebra/L1` closure 69 to 53.
5. **pdes, L1 to L3.** Current: L1 `odes/L4`, `ito/L3`; L2 `pdes/L1`, `complex/L1`; L3 `pdes/L2`, `numerics/L4`. Proposed: L1 `multivar/L1`, `ito/L1`; L2 `pdes/L1`, `odes/L3`, `complex/L1`; L3 `pdes/L2`, `numerics/L4`, `ito/L3`, `odes/L4`. Reason: the brief says "prerequisites in the map: all of `odes` and `ito` level 3" for the whole course, but the L1 context reads only `multivar` l3, `limits-thm` l7, `quadratics` l8 and the `ito` l1 and l2 sections (Brownian motion as a limit of walks). `ito/L3` (pricing) is used from L3 (l9-bs-pde, l11) and `odes/L4` (l18) from L3; L2 uses `odes` l2, l7 and l10. Closure of L1 92 to 57; L3 unchanged at about 117. If the owner prefers the literal brief line, keep and note it. All unwritten.
6. **mental-pressure, L4.** Current: `mental-pressure/L3`, `conditional/L2`, `limits-thm/L2`. Reason: `limits-thm/L2` adds 22 closure levels (integrals, `exp-log`, probability chain) for the 68% and 95% benchmarks of `l14-ranking-likelihoods`; L1 to L3 need 5 to 7 levels. The brief names `limits-thm` l7-bell-curve, so this is allowed. Proposed: ask the L4 author to restate the two benchmarks in one screen and drop `limits-thm/L2` (closure 38 to 16 with `counting-chance/L3` added); otherwise keep and record the cost.
7. **systems, L1 (and L2 to L4).** Current: `cpp/L4`, `cpp-pricing/L3`. Proposed: `cpp-pricing/L3` only (see note 1). Reason for the warning: `cpp-pricing/L3` carries 46 unique closure levels: `cpp-pricing/L2` needs `trees/L3` (Black-Scholes), so a developer interview course sits behind options, markets, trees and the probability spine. The brief names `cpp-pricing` l9, l10, l11, but `l9-timing` and `l11-optimisation-flags` time the binomial pricer and `l10-memory-layout` mentions it twice. No gate fix is cheap; the decision for the brief owner is whether `systems` L1 should instead take `cpp/L4` and teach its own timing and layout examples (closure 56 to about 13). Closure kept at 55 here.
8. **game-theory L3 and mm-games L3, brief-named lessons not gated.** `game-theory/L3` (current `game-theory/L2`, `puzzles/L4`) reads `conditional` l26, `random-vars` l19, `markov` l19, `fin-ml` l9; `mm-games/L3` (current `mm-games/L2`) reads `markov` l10 and `fin-ml` l9. Deliberately left out to keep the interview path light, and I agree. Proposed: none; the level briefs must say the lesson re-teaches Kelly as 2p - 1, ruin and optional stopping in two sentences each, as `puzzles` l21 does, since the gate does not guarantee them. `game-theory/L2` also cites `limits-thm` l17 and `series` l7 with the same treatment.

## Notes

1. **systems, L1.** `cpp/L4` is implied by `cpp-pricing/L3` (which requires it): delete it.
2. **Implied references (the brief says direct only).** Drop where the reference is reached through another reference of the same level, keeping the reason in the report: `algebra/L1` `proof/L3` (via `linear-maps/L2`); `complex/L1` `exp-log/L3` (via `taylor/L2`); `complex/L3` `integrals/L3` (via `limits-thm/L4`); `ito/L1` `limits-thm/L3` (via `trees/L3`); `markov/L5` `random-vars/L4` (via `limits-thm/L4`, list then equals the implicit one: delete it); `measure-prob/L2` `limits-thm/L3` (via `ito/L1`); `numerics/L4` `trees/L3` (via `numerics/L3`); `odes/L1` `exp-log/L3` (via `integrals/L3`); `pdes/L2` `complex/L1` (via `odes/L4`, unless warning 5 is taken); `stat-learning/L3` `conditional/L2` (via `stat-learning/L2`, delete the list); `stat-models/L1` `regression/L3` (via `stat-learning/L3`); `taylor/L2` `exp-log/L3` and `trig/L2` (via `taylor/L1`, delete the list); `topology/L3` `taylor/L1` (via `topology/L2`, delete the list). Nothing blocks any of these; the saving is clarity in the locked card.
3. **Mapper doubtful list, decided.** `plotting/L3` on `exp-log/L2`: keep (`l9-log-axis` needs logarithms). `pytest/L3` on `plotting/L2` and `git/L3`: keep (`l11-testing-drawdown` uses `plotting` l7, `l12-every-push` uses `git` l9; closure cost is `git` and two terminal levels). `eigen/L4` on `taylor/L2`, `multivar/L4`: keep (`l14` is a power series, `l16` uses `multivar`). `counting-chance/L3`: warning 3. `linear-maps/L2`: warning 4. `sql/L1` on `equations/L3` is the weakest of the "no open Stage 1 course" choices; acceptable.
4. **Pure departures, decided.** `measure-prob/L1` without `analysis`: required by the strand rule; the unwritten lessons must teach what they lean on in `analysis` l5 and l20 (the brief's own context lists them). Add that to the `measure-prob` brief. `complex/L1`, `pdes/L1` (`vector-calc`) and `brainteasers/L1` (`proof`): correct departures; `proof` l12 and l13 are re-taught in the brainteasers lessons by the brief's own design. `topology/L3` on `taylor/L1` for `numerics/L2` is fine (and becomes implied, note 2).
5. **puzzles, L1 on `markov/L2`.** Genuine (l3 and the homework's `pattern_wait` need first-step equations, `markov` l7), but 18 closure levels come from `markov` L1 to L2's matrix prerequisites (`vectors/L3`). Accept; the cost lands on L1, and L2 needs `markov/L3` anyway.
6. **coding-int, L4 on `contests/L4`.** Named lessons are l14 and l15, but the course chain brings `contests/L2` and `L3` along (modulo, patterns). With error 2 already requiring `contests/L3`, the extra is one level. Accept.
7. **limits-thm, L4 on `multivar/L5`** (and so `markov/L4`, `puzzles/L5`, `stat-models/L3`, `complex/L3`, `ito/L4` through the chain): the brief names `multivar` l17 (Jacobian) and l18 (triple integrals), so correct. A lesson reference `multivar/l17-stretching-the-grid` would not shrink the closure, because `multivar/L5` itself needs `L3` and `L4`. Accept.
8. **game-theory, L2 (13 to 52 to 57 closure).** Each of `graphs-dp/L4` (l17), `micro/L3` (l11), `limits/L4` (l14) is brief-named and used (backward induction, winner's curse, optimal bid). Accept.
9. **numerics, L1 on `cpp-pricing/L1`.** Named for `l1-doubles` (cancellation), but it brings `cpp` L1 to L2 and `terminal/L3` for a quant numerics course; `py-found/L1` already teaches float error. Unwritten: ask the author whether a Python-only cancellation example would let it be dropped.
10. **Research and recruiting.** `research-int` L1 to L4 and `recruiting` L1 to L3 match their briefs; `recruiting` stays open (closure 0 to 2). `research-int/L1` is the largest first interview level (62), all brief-named (`regression` l2 to l11, `testing` l3 to l10, `eigen` l7). `systems/L4` leaving out `cpp/L5` is right: its lessons cite only `cpp` l8, l9, l14, l15.

## Closure of each interview course's first level, before and after the proposed changes

Counted as levels a fresh learner must finish or test out of, the level itself excluded.

| Level | Before | After | Main change |
| --- | --- | --- | --- |
| recruiting L1 | 0 | 0 | none |
| brainteasers L1 | 28 | 7 | warning 1 |
| game-theory L1 | 13 | 12 | warning 3 |
| puzzles L1 | 28 | 27 | warning 3 |
| mm-games L1 | 23 | 14 | warning 2 and 3 |
| mental-pressure L1 | 5 | 5 | none |
| coding-int L1 | 25 | 27 | error 2 (a level correctly added) |
| research-int L1 | 62 | 61 | warning 3 |
| systems L1 | 56 | 55 | warning 7 (13 if the brief owner changes the pricer reference) |

Other levels that move: `brainteasers` L3 36 to 37, `puzzles` L2 32 to 44 (error 1), `coding-int` L2 35 to 30, `coding-int` L4 41 to 34, `mental-pressure` L4 38 to 38 (16 if warning 6 is taken), `game-theory` L3 74 to 72, `puzzles` L5 64 to 63, `pdes` L1 92 to 57, `linear-maps` L2 52 to 34. Levels that stay large and are brief-named: `research-int` L2 to L4 (83 to 88), `mm-games` L4 (62), `puzzles` L5 (63), `systems` L2 to L4.

## Unwritten levels (the 35 warnings)

All 35 are references from an unwritten level; no written level depends on an unwritten one (checked by lesson-file presence). 25 are same-course chains (L(n) on L(n-1)) and harmless. The cross-course ones are genuine and match the plan lines: `odes/L2` on `complex/L1`, `numerics/L3` on `odes/L4`, `convex/L4` on `numerics/L2`, `measure-prob/L3` on `ito/L2`, `measure-prob/L4` on `ito/L3`, `pdes/L3` on `numerics/L4`, `topology/L1` on `analysis/L5`. `pdes/L1` on `odes/L4` and `ito/L3` is over-wide (warning 5); `pdes/L2` on `complex/L1` is implied (note 2). Risk to record: a dependent written before its cross-course prerequisite (for example `ito/L3` before `ito/L2`, or `pdes` L2 before `odes` L4) stays locked until the prerequisite is written, so the fix agent for each writing task should run `validate.mjs` and check this list. `coding-int/L4` on `coding-int/L3` clears when level 3 merges.

## Fix pass

Method: `docs/reports/prereq-mapping-scripts/fix-pass.mjs` edits `mapping.txt` (the source of every list), drops implied references by script, and syncs `levels[].requires` and `lessonRequires` in every `course.json` by text edit. A second script parsed each file and its HEAD version and found them equal once those two fields are removed (key order included); 21 files changed. I recomputed every closure from the final files. Validator: 0 errors, no cycles (30 requires warnings, all "no written lesson", down from 35). Routes: all passed, with and without `--mobile`.

Status: errors 2 applied, 1 deferred (lesson text); warnings 4 applied, 2 partly applied, 2 disputed; notes: 1 and 2 applied, 3 to 10 agreed and left as they are, except 4 and 9 deferred (a brief line and an author question). Disputed: micro L1 (warning 2), pdes L1 to L3 (warning 5), systems pricer (warning 7), and the `limits-thm/L2` half of warning 6.

### Errors

1. **puzzles L2 and L3: applied.** L2 `puzzles/L1`, `conditional/L2`, `markov/L3` becomes those plus `limits-thm/L2`. L3 `puzzles/L2`, `limits-thm/L2` becomes the implicit `puzzles/L2` (list deleted). Closure of L2 32 to 44.
2. **coding-int L1: applied.** `graphs-dp/L4`, `algo-think/L3`, `contests/L1` becomes `graphs-dp/L4`, `algo-think/L3`, `contests/L3`; the `lessonRequires` (`l5-bit-tricks`) is deleted. The brief names `contests` l11-bitmasks for the course, so the gate follows it. Closure of L1 25 to 27.
3. **coding-int L2 (`l8` cites `contests` l15): deferred.** The fix is one sentence in a lesson, outside this pass (`course.json` only). Gate unchanged, as the review advises. For the next lesson fix agent: reword the `contests/l15-debugging-under-time` sentence in `coding-int/l8-simulating-the-rules`.

### Warnings

1. **brainteasers L1 and L3: applied.** L1 `counting-chance/L2`, `contests/L2` becomes `counting-chance/L2`. L3 `brainteasers/L2`, `mental/L2`, `series/L2`, `exp-log/L3` becomes `brainteasers/L2`, `mental/L3`, `series/L2`, `exp-log/L3`, `contests/L2`. The brief's "Prerequisites" line (plan: `proof` L3 to L4, `counting-chance` L2, `graphs-dp` L3) does not name `contests`; "Builds on" cites `contests` l8 only as a one-line recall, and I checked that the written L1 lessons, review and homework cite no `contests` lesson. L3 needs `contests` l5-modulo (L2) and `mental` l10 (L3). Closure of L1 28 to 7, of L3 36 to 37.
2. **micro L1: disputed.** Kept `markets/L2`. The proposed `markets/l7-shares` with an override `["ratio/L2"]` under-gates it: `l7-shares` states the objective "value a share with the dividend discount model", and its screen uses `P = D/(r - g)`, a discounted geometric series, which needs `markets` l2 (present value) and `series/L3`. A gate on `ratio/L2` would contradict the lesson, which is the same kind of error as error 3. With `markets/L1` as the override the saving is one level only (`markets/L2` itself). `micro` l1 never names a `markets` lesson, so the real fix is content: a shares recap in `micro` l1 or splitting the DDM screen out of `l7`, then `micro/L1` could depend on `markets/L1` less. `mm-games/L1` closure 23 to 22 (from warning 3), not 14.
3. **counting-chance L3 before `conditional/L1` and `random-vars/L1`: applied.** Both `counting-chance/L3` become `counting-chance/L2`. Added `counting-chance/L3` to `game-theory/L3` (l12-poker-hands; `game-theory/L2`, `puzzles/L4` becomes those plus it) and `mental-pressure/L4` (l10-birthday). `measure-prob/L1` keeps it. Longest chain 34 to 33.
4. **linear-maps L2: applied.** `eigen/L4` becomes `eigen/L1` (`eigen` l3-eigenbasis is in `eigen` L1). Closure 52 to 34.
5. **pdes L1 to L3: disputed.** The `pdes` brief says for level 1 "Prerequisites in the map: all of `odes` and `ito` level 3" (`odes/L4`, `ito/L3` in the map), and level 3 "`pdes` level 2 and `numerics` level 4". The brief is binding and the course is an optional topic, so I kept L1 `odes/L4`, `ito/L3`, L3 `pdes/L2`, `numerics/L4`. The only change is note 2's implied drop (L2 `pdes/L1`, `complex/L1` becomes the implicit `pdes/L1`). A narrower gate needs the brief owner to change that line. Closure of L1 stays about 91.
6. **mental-pressure L4: partly applied.** `counting-chance/L3` added (see warning 3). `limits-thm/L2` kept: the lesson `l14-ranking-likelihoods` is written and uses the benchmarks, and I may not edit lessons here. The L4 author could restate the 68% and 95% figures in one screen and drop it (closure 38 to about 16). Closure of L4 38.
7. **systems L1: partly applied.** `cpp/L4` dropped (note 1). `cpp-pricing/L3` kept: the `systems` brief lists "`cpp-pricing` level 3" as a prerequisite and builds lessons (l2 and l17 among them) on `cpp-pricing` l9 (timing), l10 (memory layout) and l11 (flags), saying it does "not repeat" them, so dropping it would contradict the brief. Closure of L1 56 to 55; 13 needs the brief owner to make `systems` teach its own timing and layout examples.
8. **game-theory L3 and mm-games L3: applied as none.** No gate change. The level briefs should say `l12-poker-hands`-style recaps (Kelly as 2p - 1, ruin, optional stopping in two sentences each) are re-taught; logged here for the brief owner.

### Notes

1. **systems L1 on `cpp/L4`: applied** (see warning 7).
2. **Implied references: applied.** Dropped by script, 15 references: `algebra/L1` `proof/L3`; `complex/L1` `exp-log/L3`; `complex/L3` `integrals/L3`; `ito/L1` `limits-thm/L3`; `markov/L5` `random-vars/L4`; `measure-prob/L2` `limits-thm/L3`; `numerics/L4` `trees/L3`; `odes/L1` `exp-log/L3`; `pdes/L2` `complex/L1`; `stat-learning/L3` `conditional/L2`; `stat-models/L1` `regression/L3`; `taylor/L2` `exp-log/L3` and `trig/L2`; `topology/L3` `taylor/L1`. With `systems/L1` `cpp/L4` that is 16; the script finds no other implied reference, so the "19" in the task counts more than the review lists. Lists that became the implicit previous level were deleted: `markov/L5`, `stat-learning/L3`, `measure-prob/L2`, `pdes/L2`, `taylor/L2`, `topology/L3`.
3. **Mapper doubtful list: agreed, kept** (`plotting/L3`, `pytest/L3`, `eigen/L4`; the other two decided in warnings 3 and 4; `sql/L1` accepted).
4. **Pure departures: agreed; deferred** the line for the `measure-prob` brief (teach what it leans on in `analysis` l5 and l20), as no brief is edited in this pass.
5. **puzzles L1 on `markov/L2`: agreed, kept.**
6. **coding-int L4 on `contests/L4`: agreed, kept** (with error 2 the extra is one level).
7. **limits-thm L4 on `multivar/L5`: agreed, kept.**
8. **game-theory L2: agreed, kept.**
9. **numerics L1 on `cpp-pricing/L1`: agreed, deferred** to the author (unwritten): a Python-only cancellation example would let it go.
10. **Research and recruiting: agreed, no change** (`recruiting` stays open).

### Closure after the fix pass

Levels a fresh learner must finish or test out of, the level excluded.

| Level | Before | After |
| --- | --- | --- |
| recruiting L1 | 0 | 0 |
| brainteasers L1 | 28 | 7 |
| game-theory L1 | 13 | 12 |
| puzzles L1 | 28 | 27 |
| mm-games L1 | 23 | 22 |
| mental-pressure L1 | 5 | 5 |
| coding-int L1 | 25 | 27 |
| research-int L1 | 62 | 61 |
| systems L1 | 56 | 55 |
| research-int L3 | 85 | 84 (82 outside the course) |

Other levels: `brainteasers` L3 36 to 37, `puzzles` L2 32 to 44, `puzzles` L5 64 to 63, `coding-int` L2 35 to 37 (the L1 change adds `contests` L2 and L3 behind it), `game-theory` L3 74 to 74 (`counting-chance/L3` added back), `linear-maps` L2 52 to 34, `pdes` L1 92 to 91, `mental-pressure` L4 38 to 38. Longest chain 33 levels (`momentum-rep/L3`), largest direct list 5. The interview targets the review set are met for `brainteasers` L1 (7); `mm-games` L1 (22, target about 14) and `systems` L1 (55, about 13) are not, for the reasons in warnings 2 and 7.
