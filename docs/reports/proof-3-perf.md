# Proof level 3: performance task pilot (PLAN 2c item 5)

Course `proof` (topic 0.6, Stage 0), level 3 "Proof methods" (l10 to l15). Kind: `derivation`. Base commit 07e2122.

## Scope note

Stage 0 is excluded from the verb rule, so `proof/L3` is not rule-matched and not on `tools/perf-pending.json`. The validator accepts a task on an unmatched level (AUTHORING section 5: "A level that does not match may still carry one"); nothing was worked round. The level now needs the task passed for met, as the PLAN pilot asks. AUTHORING also says "Do not add longform boxes to a level the rule does not match"; the PLAN pilot overrides that here, and the main session should decide whether the pilot stays after review.

## What changed (only `app/content/courses/proof/homework-3.json`)

- Added `h-prove-cube-minus-n` (item 9 of 10, before the exit longform), `performance: "derivation"`, difficulty 4, skills `pv-direct`, `pv-induction`, `pv-writing`. Homework items: 9 to 10, within the limit of 12, so nothing was converted.
- Statement: "3 divides $n^3 - n$ for every whole number $n \ge 1$". Unseen in the proof course (grep: it appears only in `measure-prob` and `elimination`). The learner chooses the method. Empty box: no starter, steps, hints or parts; the model shows only after Mark my answer.
- Methods taught by the level that prove it: cases on the remainder mod 3 (l10's proof by cases, and homework's mod-3 lemma), induction (l13; same step shape as "3 divides $4^n - 1$"), and the factorisation $(n - 1)n(n + 1)$. The model gives cases in full, induction in full, and the factorisation in two lines.
- Rubric, four criteria summing to 10, method-neutral: claim and method stated, letters introduced (2); every $n$ covered, by the three remainders or by base case and step (3); every algebra line correct with its reason (3); written as 3 times a named bracket, bracket shown to be an integer, conclusion stated (2). A correct induction proof scores 10 on it, as does a correct cases proof.
- Layout fixes found in the screenshots, same file: item titles with `$` show raw in the header, so four titles became plain words (`h-two-n`, `h-root3-order`, `h-root3-lemma` and the new item). Two long inline formulas in the model were split so they wrap at 440 px. One 21-word sentence in the `h-exit-longform` model was split (voice scan).

## Self-check

1. `node tools/validate.mjs`: 0 errors (2095 warnings, none on `proof/homework-3`). Manifest `perf` lists `proof/L3 -> h-prove-cube-minus-n, derivation, self`. Manifest restored before commit.
2. Voice scan: `homework-3.json` alone (scratch copy as VOICE_BASE) 0 and 0. With VOICE_BASE set to the whole `proof` folder: 6 long sentences and 1 long explanation, all pre-existing in files outside this task (`homework-1`, `l1`, `l3`, `l14`, `review-3`). Before this task the folder gave 7 and 1; the seventh was in `homework-3` and is fixed.
3. `python3 docs/reports/proof-3-perf-numbers.py`: exit 0. Brute force of the claim for $n$ from 1 to 100000 (and $-1000$ to 0), plus the factorisation. Each case's cube, difference and bracket checked by coefficient expansion and by evaluation at $m = 0$ to 2000. The induction regrouping checked symbolically and for $k = 1$ to 5000. The quoted checks 0, 6 and 24, rubric sum and shape, item count, one task per level. It also checks that the model states each figure, and the $n^2 - n + 11$ values in the edited exit sentence.
4. `node tools/playthrough.mjs --set proof/homework-3 --local-cdn <pkgs>`: all passed, 10 of 10, with and without `--mobile`. Screenshots seen at 1280 and 440. A scratch Playwright script also shot the item after Mark my answer: the model and rubric fit at 440 px, no KaTeX past the gutter, no page errors.

## Backlog

Four bullets under `Raised later (proof level 3 perf pilot):` in `docs/BACKLOG-INBOX.md`: raw-text titles; no performance-task label; "Item 9 and Item 10 is written"; no post-mark shot in the playthrough.

No `course.json` proposal.

Matched objective: proof l15 "Write a proof another reader can check line by line, with every step justified." (the rubric grades checkable lines; l10, l11 and l13 supply the methods, and the learner chooses one).

Overlapping screens: l10 screens[7] (proof by cases, $n^2 + n$ even), l13 screens[2], [4] and [5] (base case and step in order, the same step shape) with quiz q-four (3 divides $4^n - 1$), l15 screens[3] (a missing case) and [8] (five methods); new parts: the claim $3 \mid n^3 - n$ appears in none of them, the learner picks the method (cases on the remainder mod 3, induction, or the factorisation $(n - 1)n(n + 1)$), and each line needs its reason.
