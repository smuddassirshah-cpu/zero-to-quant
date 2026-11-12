# Delta concept audit, batch 2 (12 Nov 2026)

Blind delta audit under `docs/briefs/concept-audit.md`, "Auditor brief (binding)". It reads only content changed since each course closed, plus the three odes fluency sets, which no concept audit had read. No content was changed by this audit, so no browser playthrough was needed or run.

## Header

**Scope and bases.** HEAD is 856154f0. The file lists from `git diff --stat` match the task's lists exactly.

| course | base | files in the diff |
|---|---|---|
| puzzles | 28b926bd | homework-4 |
| game-theory | 28b926bd | l9-winners-curse, review-2 |
| coding-int | 28b926bd | l7-parsing-with-a-stack, l8-simulating-the-rules, review-2 |
| measure-prob | 28b926bd, and c020fe32 for level 4 | l15-likelihood-ratios, homework-3 |
| mm-games | 28b926bd | l11-hedging, l17-options-on-a-game, review-3 |
| recruiting | 28b926bd | l9-sitting-an-assessment |
| conditional | 4e84b175 | l25-survivorship, problems-5, review-5 |
| odes | no diff since close | fluency-l2-separable, fluency-l3-integrating-factor, fluency-l7-characteristic-equation, read whole |

**Ledger.** `docs/reports/audit-delta-2026-11-12-2-ledger.md`, 105 rows.

| course | rows | correct | imprecise | wrong | misleading | unverified |
|---|---|---|---|---|---|---|
| puzzles | 3 | 3 | 0 | 0 | 0 | 0 |
| game-theory | 6 | 6 | 0 | 0 | 0 | 0 |
| coding-int | 12 | 12 | 0 | 0 | 0 | 0 |
| measure-prob | 5 | 5 | 0 | 0 | 0 | 0 |
| mm-games | 12 | 11 | 1 | 0 | 0 | 0 |
| recruiting | 3 | 3 | 0 | 0 | 0 | 0 |
| conditional | 11 | 9 | 2 | 0 | 0 | 0 |
| odes | 53 | 49 | 4 | 0 | 0 | 0 |
| total | 105 | 100 | 5 | 0 | 0 | 0 |

**Findings.** Five, all `imprecise` and all `minor`: mm-games 1, conditional 2, odes 2. No `wrong`, no `serious`. Three ledger rows (81, 100, 105) share finding 4.

**Checks run.**
- `python3 docs/reports/delta-2026-11-12-2-concepts.py`: 15,843 checks, 0 failed outside the findings, exit 1. The exit code is held at 1 by the checks named `FINDING 1` to `FINDING 5`; it returns 0 once those are fixed. The script recomputes each new slip by its named route, tests every touched widget for band overlap as the engine grades, and draws 66 to 184 distinct prompts per odes family with the engine sampler. Each odes key is substituted into its equation and starting values with sympy.
- `node tools/validate.mjs`: 0 errors, 4,522 warnings.
- `node tools/grade-all.mjs --file <path> --local-cdn <pkgs>` on the three coding-int files: 12, 12 and 10 widgets checked, 0 failures each. None of the changed widgets holds graded code; the changes are numeric slips.

**How each new slip was judged.** Value against the route its feedback names; truth of the feedback; whether the value is right under any reading the prompt allows; band overlap with the key and the other slips; wording against the learner's likely mistake and the item's units. Engine basis: `grade.js` checks the key first, then `wrong[]` in order, each within `abs` plus 1e-9. A typed `%` divides the number by 100, and a `unit: "%"` widget divides a bare number by 100.

## puzzles

One new slip (`sign`, homework-4 `hw4-table-max`). Value, feedback and bands are correct. No finding.

## game-theory

Two new slips (`sign` in l9 screen 5 and review-2 `rv2-firm`). Both correct. The review line says "a firm worth £30m to you"; that is the average over accepted firms, as the neighbouring line and the explain state, and the product $0.4 \times (30 - 40)$ makes the conditioning plain. No finding.

## coding-int

Four new slips (`sign` on three truncation items and on the l8 trace). All correct: no division convention gives a positive quotient, and the trace's two trades are $+12$ and $-13$. No finding.

## measure-prob

One new slip (`decimal`, l15 screen 5) and one reworded rubric line (homework-3 `h-prove-urn`). Both correct. The rubric now accepts the tower-property route or the symmetry of the two colours; both prove the chance is a half. The l15 diff is the same from either base. No finding.

Note, not a finding: on this widget a learner who types "2.1%" is read as 0.021 and marked wrong, with the new line telling them to drop the sign. The line is true and helps. Accepting the answer needs an engine change (inbox bullet).

## mm-games

Four new slips (`decimal` on three residual-sd items, `sign2` on l17 screen 4). Values and feedback are correct. One band is too wide.

1. `mm-games/review-3.json` | `items[5].widget.wrong[2].tol` (id `r-residual`, slip `decimal`) | imprecise | minor | The slip band is ±0.005 round 0.0087, so it runs from 0.0037 to 0.0137. It takes more than the decimal form of the key. | A learner who makes the variance-share slip and types "0.38%" is read as 0.0038. That lands in this band, so they are told "0.0087 is 0.87% written as a decimal" and handed the key, and the `var` line never shows. "1%" (0.01) is taken the same way. The two sibling slips in l11 use bands of 2% of the value (0.00024 on 0.012, 0.0008 on 0.04); this one copied the key's absolute band. Script `FINDING 1`. | Set `"tol": { "abs": 0.0002 }` on this slip. The band 0.0085 to 0.0089 still takes 0.0087, 0.00872 and the unrounded 0.008718, and excludes 0.0038, 0.002 and 0.01. This changes a slip tolerance only; the key, the slip value and the feedback stay as they are.

## recruiting

One new slip (`sign`, l9 screen 3). Correct. No finding.

## conditional

Three new slips (`sign2` in l25 screen 9, `sign` in problems-5 item 4 part 3 and review-5 `r-unfair-double`) and one widened key tolerance (review-5 `r-low-prior`). Values and feedback are correct. Two tolerance details are not.

2. `conditional/problems-5.json` | `items[3].parts[2].widget.wrong[3].tol` (slip `sign`) | imprecise | minor | The slip band is ±0.005 round 22.55, so it misses 22.54. That is the value the prompt's own route gives. | The prompt says "Using 0.5299 from part 2", and $0.5299 \times 20 / 0.4701 = 22.544$. The key is −22.55 ± 0.01, so −22.54 is marked right, as the `correct` line says it should be. A learner who drops the sign on that same number types 22.54 and gets only the generic line, because the band runs from 22.545 to 22.555. Script `FINDING 2`. | Set `"tol": { "abs": 0.01 }` on this slip, mirroring the key. The band 22.54 to 22.56 meets no other band; every other value is negative. This changes a slip tolerance only.

3. `conditional/review-5.json` | `items[4].widget.accept` (id `r-low-prior`) | imprecise | minor | The key's tolerance was widened from 0.0005 to 0.005, but the `accept` line still reads "or $0.4615 \pm 0.0005$". A learner who typed 0.46 is marked right and then reads a band that excludes it. | The engine shows `accept` after grading as "Accepted: ...". The widened band is sound: $6/13 = 0.46154$, and the slips 0.6 and 0.8571 lie far outside 0.4565 to 0.4665. Script `FINDING 3`. | Replace the `accept` string with `any form equal to $\\tfrac{6}{13}$, or $0.4615 \\pm 0.005$`. No key, tolerance or slip changes.

## odes (three fluency sets, read whole)

Eleven families. Every key, every `wrong` value, every stated constant and every solution step is correct on every draw sampled. Sympy confirms each key against its equation and starting values, and each slip against the route its line names. Constants of integration are handled soundly: $A = y_0$ after exponentiating; $C = -1/y_0$ for $y' = ky^2$, including negative starts; the integrating factor with zero constant, which is the standard convention. The $y' = ky^2$ key is valid on the interval round 0 where $1 - ky_0t \ne 0$; the item makes no wider claim. Sign conventions hold: $e^{+\int p\,dt}$ for $y' + py$, and $p$ carries the minus when the prompt shows one. Two minor points.

4. `odes/fluency-l3-integrating-factor.json` | `families[1].prompt` (`constant-coefficient`); `odes/fluency-l7-characteristic-equation.json` | `families[2].prompt` (`fit-two-roots`) and `families[3].prompt` (`repeated-root`) | imprecise | minor | The key is a function of $t$, but the prompt never names the independent variable. It writes $y'$, $y''$ and $y(0)$ only. A learner who answers in $x$, the usual letter in many textbooks, is marked wrong on a right method. | The other families name it: the l2 prompts write $\tfrac{dy}{dt}$, and `find-the-factor` asks for $\mu(t)$. The odes lessons use $y(t)$ throughout, so the risk is small. Script `FINDING 4`. | In each of the three prompts insert "for $y(t)$," before "with". Paste-ready: `Solve ${v}' = {poly(v; a, -a*s)}$ for ${v}(t)$, with ${v}(0) = {y0}$.` and, for both l7 families, `Solve $y''{b:+c}y'{c:+c}y = 0$ for $y(t)$, with $y(0) = {y0}$ and $y'(0) = {v0}$.` No key or slip changes.

5. `odes/fluency-l2-separable.json` | `families[3].widget.placeholder` (`discount`) | imprecise | minor | The placeholder "For example 81.87" is the key itself on some draws, so the empty field shows the answer. | $100e^{-0.2} = 81.873$. The draws $(p, r, \text{years}) = (100, 2, 10)$, $(100, 4, 5)$ and $(100, 5, 4)$ have this key: 3 of 729. Script `FINDING 5`. The savings placeholder 15569.31 matches no draw. | Set `"placeholder": "For example 123.45"`. No draw of this family has the key 123.45 (all 729 checked).

## Overlap with earlier reads

Read only after commit ee09d100 ("WIP: delta batch 2 ledger and findings").

What exists. `docs/reviews/review-delta-ac-3.md` reads four fix passes (ratio, eigen, number-sense) and parts B, C and D of the bands pass. None of its items is in this batch, so it has no finding on these changes. No second read of the negative-key pass, of part A of the bands pass (the `decimal` slips) or of the odes fluency sets is on file; only the authors' reports are (`docs/reports/negative-key-pass.md`, `bands-pass-ac.md`, `fluency-odes.md`). `docs/reviews/triage-bands-ab.md` proposed the `r-low-prior` tolerance and did not mention its `accept` line. `docs/reviews/audit-delta-2026-11-11-1.md` asked for the homework-3 rubric change and its fix-pass read found the new line correct, as this audit does.

Conceptual findings on the content in scope:

| course | audit only | earlier read only | both |
|---|---|---|---|
| puzzles | 0 | 0 | 0 |
| game-theory | 0 | 0 | 0 |
| coding-int | 0 | 0 | 0 |
| measure-prob | 0 | 0 | 0 |
| mm-games | 1 | 0 | 0 |
| recruiting | 0 | 0 | 0 |
| conditional | 2 | 0 | 0 |
| odes | 2 | 0 | 0 |
| total | 5 | 0 | 0 |

Notes from the authors' reports, for the fixer.
- Finding 1: the bands pass set each `decimal` band to "at least half a unit where the question asks for decimal places", which is how 0.0087 came to carry ±0.005. With the proposed ±0.0002 the validator still reports 0 errors and the same 4,522 warnings (tried and reverted), so the rule's worry about a new `[wrong-band]` advisory does not arise here.
- Finding 2: the negative-key pass copied each new band from a neighbouring slip (0.005 here), not from the key (0.01).
- Finding 5: the fluency report's reading pass looked for rendering faults, not for a placeholder that equals a key.

## Inbox

Three bullets appended to `docs/BACKLOG-INBOX.md` under "Raised later (audit delta batch 2)": a typed % sign on a per cent question without `unit: "%"`; a validator check of a numeric `accept` line and of a fluency placeholder against the key; a validator check on a slip band wide against its own value.

## Fix pass

Opus fixer, 12 Nov 2026. Each finding was re-derived from the content and `app/js/engine/grade.js` before any edit. No key, slip value, id or test changed.

1. fixed. `app/content/courses/mm-games/review-3.json` `items[5].widget.wrong[2].tol` (`r-residual`, slip `decimal`): `abs` 0.005 to 0.0002. Basis: `parseNum` divides a typed "0.38%" by 100 to 0.0038, which lay inside the old band 0.0037 to 0.0137 and drew the `decimal` line; the new band 0.0085 to 0.0089 holds $2\sqrt{0.19}/100 = 0.008718$ and the rounded 0.00872 and 0.0088, and meets neither the key band nor the `var` and `lin` bands.
2. fixed. `app/content/courses/conditional/problems-5.json` `items[3].parts[2].widget.wrong[3].tol` (slip `sign`): `abs` 0.005 to 0.01. Basis: $0.5299 \times 20 / 0.4701 = 22.5441$, outside the old band 22.545 to 22.555; the new band 22.54 to 22.56 also holds the unrounded 22.5486 and meets no other band, as every other band is negative.
3. fixed. `app/content/courses/conditional/review-5.json` `items[4].widget.accept` (`r-low-prior`): "$0.4615 \pm 0.0005$" to "$0.4615 \pm 0.005$". Basis: the key tolerance is 0.005, so 0.46 is graded right; $6/13 = 0.46154$, and the line now states the band the engine applies.
4. fixed. `app/content/courses/odes/fluency-l3-integrating-factor.json` `families[1].prompt`; `app/content/courses/odes/fluency-l7-characteristic-equation.json` `families[2].prompt` and `families[3].prompt`: inserted "for ${v}(t)$," (l3) and "for $y(t)$," (l7) before "with". Basis: the expression grader compares over the union of both sides' unknowns, so an answer in $x$ against a key in $t$ fails; no other family in the three sets leaves the variable unnamed (l2 writes $d/dt$ and $d/dT$, `find-the-factor` asks for $\mu(t)$, the other l7 families ask for roots).
5. fixed. `app/content/courses/odes/fluency-l2-separable.json` `families[3].widget.placeholder` (`discount`): "For example 81.87" to "For example 123.45". Basis: enumerating all 729 draws gives 3 with key 81.87 and none within 0.31 of 123.45; the savings placeholder 15569.31 is at least 68.69 from all 819 savings keys, so it stays.

Siblings checked, none needing a fix: every numeric widget in the three mm-games and conditional files for `accept` bands against `tol`, for slip bands overlapping, and for mirror or decimal slips narrower than the key. `r-fraud-flag` states $\pm 0.0005$ with tolerance 0.0005, which agrees.

Gates: validator 0 errors, 4,522 warnings; `delta-2026-11-12-2-concepts.py` exit 0 (15,843 checks, no check edited); number scripts conditional-2-perf, conditional-4-perf, mm-games-3-perf, odes-L1 to L4 all exit 0; voice gate 35 at 0 and 0 for mm-games, conditional and odes; playthrough of the six edited files plain and `--mobile` with `--local-cdn`, all passed.
