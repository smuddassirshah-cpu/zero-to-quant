# Engine pass A content follow-up

Targeted edits only; no `course.json`, ids or opt-dash files touched.

## 1. shuffled-position (7 hits, 0 left outside opt-dash; none were in opt-dash)
- numpy-pandas l8 quiz[2] explain: "takes the second choice" to "takes the else value" (it meant np.where's second argument).
- integrals l16 screens[5] feedback.generic: "the one below it" to "the next error down the column".
- multivar l18 screens[7] explain and hints[2]: "the first option" to "the integral with $1 - x - y$ innermost" (two lines).
- trees review-2 items[7] option why: "the top one, £144" to "the highest, £144".
- validation l8 screens[7] explain: "the last option" to "the every-date search".
- puzzles homework-5 items[4]: `noPosCheck: true` ("last answer" refers to an earlier puzzle, not an option).

## 2. shuffle: false
- `[shuffle-false]`: 43 hits, none in opt-dash. Removed `shuffle: false` from 41 flagged widgets plus 1 unflagged one in the same files (options are inequalities, formulas, labels or unordered numbers; "Bar A/B/C" labels refer to the canvas, not to each other). Kept 2 (ordered numbers): quadratics l10-turning-point screens[6] (12, 6, 3, -3) and proof l3-if-then screens[6] (4, 6, 7, 12).
- `O2-unshuffled-numeric`: added `shuffle: false` to 72 widgets across 66 lessons, reviews and two exams (topic-0.2, topic-2.2); the file list is the content diff. One hit left in opt-dash: `opt-dash/l11-term-structure.json` screens[6].widget.
- The rule still reports 73 because it fires whenever `shuffle` is not `true`; engine-pass-v-b says to retire it.

## 3. required: true
- stage-1: a-ls-pca-code, b-ols-table, b-crr-python, c-price-file, c-crr-cpp, d-rk4-rate (review's A14, B9, B13, C0, C10, D13).
- stage-2: a-walk-forward-ridge, b-eg-pair, c-three-pricers, c-kkt-code, d-signal-report (review's A15, B12, C5, C7, D9; C12 and C18 have left the paper).
- stage-3: r-as-of-code (review names none; the paper's only coding exit).
- mock-oa-code-hard: h1-busiest-worker, h2-voucher-route, h3-capped-trading (review names none; all three coding items).
- mock-superday-strats: c1-barrier-tree, c2-variance-interpolation (review names none; the `coding` paper's items).

## 4. expression form (topic-1.11)
- No change. The only constant complex answer the review names (`e-divide-conjugate`) was already replaced by two numeric parts in its fix pass. The two remaining `expression` items (`e-laplace-shift`, `e-harmonic-partner`) have free symbols.
- Other constant `expression` answers exist (vector-calc, series, topic-1.10) but no review names them; left alone.

## 5. tracks (mock-video)
- No change. Review finding 1 asked for track flags on prompts 4 and 5, but its fix pass rewrote both to need only expected value, reachable on every path; a track flag would wrongly drop them for off-track learners. No other mock review names a track-only paper.

## Gates
- Validator: 0 errors; shuffled-position 0; readiness-sums OK.
- Playthrough with `--local-cdn`, 78 lessons, 12 sets, 7 exams, desktop and `--mobile`: All passed (exams with `required` pass when answered correctly).
