# Exam second item, stage0: topic-0.3, topic-0.2, topic-0.4

Brief: `docs/briefs/exam-second-item.md` (session AG, PLAN task 4). Numbers: `docs/reports/exam-second-item-stage0-numbers.py` (149 checks, exit 0). Generator and screenshots: scratchpad `exam2-stage0/` (`gen.py`, `pairs.py`, `corpus.txt`, `shots0*`).

## Pairs, recomputed

Rule (`prereq.js`, `EXAM_SKILL_FLOOR` 0.5): an essential skill of a level (any skill tagged on its review) with one auto (non-longform) item in the exam. Recomputed on 17 Nov from each exam file and every `course.json` of the topic; the lists match the 16 Nov table. Note: `topic-0.2` `e-spread-model` carries `kind: "longform"` on the item, not on a widget, so `quad-model` had one auto item.

| exam | (course/level) essential skill with one auto item | pairs |
|---|---|---|
| topic-0.3 | counting/L1, L2 ct-comb; counting/L3 vc-arrows, vc-geometry; series/L1, L2 seq-arith, seq-converge; series/L3 seq-binomial, seq-converge; trig/L3 tr-identities, tr-equations | 8: ct-comb, seq-arith, seq-binomial, seq-converge, tr-equations, tr-identities, vc-arrows, vc-geometry |
| topic-0.2 | functions/L4 fn-transform; quadratics/L1, L2, L3 quad-model | 2: fn-transform, quad-model |
| topic-0.4 | terminal/L1, L3 tm-typing | 1: tm-typing |

## topic-0.3 (26 to 30 items, 60 to 70 minutes)

Four new items (rule a, two of them carrying two listed skills where the item needs both, rule b) and one swap (rule c).

| id | skills | d | widget | task |
|---|---|---|---|---|
| e-desk-meetings | ct-comb | 2 | numeric | 9 desks, each pair meets once: $\binom92 = 36$ (slips 72 ordered, 81, 8) |
| e-double-angle-roots | tr-identities, tr-equations | 3 | numeric set | $\sin 2x = \sin x$ on $[0^\circ, 360^\circ)$: 0, 60, 180, 300; the identity is needed to factorise, and dividing by $\sin x$ loses two roots (`count`), slips "0, 60, 120, 180" and "0, 30, 150, 180" |
| e-parallelogram-midpoint | vc-arrows, vc-geometry | 3 | numeric | OABC with $\overrightarrow{OA} = (4, 1)$, $\overrightarrow{OC} = (1, 3)$, M midpoint of BC: $|\overrightarrow{AM}| = \sqrt{7.25} \approx 2.69$ (B from the parallelogram, then a length; slips 2.06, 4.61, 7.25) |
| e-rebate-third | seq-converge, seq-geom | 3 | numeric | first rebate £18, sum to infinity £30: $r = 0.4$, third month £2.88 (slips 6.48, 7.20, 4.80) |
| e-coefficients-in-step | seq-arith, seq-binomial | 5 | numeric | coefficients of $x, x^2, x^3$ in $(1 + x)^n$ arithmetic, $n > 2$: $n^2 - 9n + 14 = 0$, $n = 7$ (slip 2) |

Removed: `e-sigma-odd` (seq-sums, d3), the most duplicated item: an arithmetic sum already asked by `e-weekly-savings`. seq-sums keeps `e-weekly-savings` and `e-loan-payment`. `e-rebate-third` takes its place and difficulty.

Ramp 6/15/6/3 of 30 (20/50/20/10). Minutes: 60 x 30/26 = 69.2, rounded to 70 (hours note: the main session runs `readiness-sums.mjs --write`).

## topic-0.2 (30 items, the cap; 75 minutes unchanged)

Two swaps (rule c).

| id | skills | d | widget | in place of |
|---|---|---|---|---|
| e-read-the-change | fn-transform | 3 | choice on a plane canvas (solid $f(x) = x^2 - 1$, dashed $g$) | `e-two-roots` (quad-solve, quad-factor; d3, multi) |
| e-two-rates | quad-model, quad-solve | 4 | numeric, unit % | `e-formula` (quad-solve; d4) |

- `e-read-the-change`: read $g = 2f(x - 2)$ from the graph; distractors $2f(x + 2)$ (direction), $f(x - 2) - 1$ (same lowest point, roots $2 \pm \sqrt2$), $f(2(x - 2))$ (sideways squeeze). The existing `e-shifted-peak` applies a move to a point; this one reads a move and a stretch from two curves.
- `e-two-rates`: £10,000 at $r$ then $2r$ becomes £11,872; the learner forms $(1 + r)(1 + 2r) = 1.1872$, solves $2r^2 + 3r - 0.1872 = 0$ (discriminant 10.4976, root 3.24) and rejects $-1.56$: 6%. Slips 6.24% (rates added), 8.96% (one rate), −156% (other root).
- After the swaps: quad-solve 4 auto items, quad-factor 2 (`e-factorise`, `e-odd-squares`), quad-model 2, fn-transform 2. Ramp unchanged (6/15/6/3).

## topic-0.4 (20 to 21 items, 60 to 65 minutes)

| id | skills | d | widget | task |
|---|---|---|---|---|
| e-left-hand-commands | tm-typing | 3 | multi (3 of 6) | which of `cat`, `sed`, `wc`, `grep`, `head`, `cut` use only left-hand keys: the home-row columns, with H (beside G) and the right little finger's P as traps |

The existing `e-typing-speed` is the WPM sum; homework-1 asks the index-finger keys of one word. The other two multi items hold two correct options each, this one three. Ramp 4/11/4/2 of 21. Minutes: 60 x 21/20 = 63, rounded to 65.

## Pairs left

None. Every pair of the three exams has two auto items, and no skill of any of the three exams is on fewer than two (the script checks both).

## Reuse

Read before writing: the level teaching each skill and the exam's existing item. A corpus of every string in the nine topic courses, `stage-0` and the mocks was searched for each idea. Dropped on that search: $2\cos^2 x + 3\sin x = 3$ (`trig/problems-3` item 2) and a bouncing ball or recurring decimal for seq-converge (`series/problems-2`, `homework-2`, l8). `fresh-check.mjs --file`: 0 hits on all three exams, and no advisory names a new item.

## Gates

- `node tools/validate.mjs`: 0 errors; no warning on a new item.
- `VOICE_BASE=app/content/exams python3 docs/reviews/voice-scan.py 35`: 0 explanations over three sentences, 0 sentences over 35 words.
- `grade-all.mjs --file` with the local CDN: 0 failures on each exam (30, 25 and 21 widgets).
- `playthrough.mjs --exam <id> --local-cdn`: topic-0.3 30 of 30, topic-0.2 30 of 30, topic-0.4 21 of 21, passed with and without `--mobile` (also with `--why`). Screenshots read at 440 px; one fix: the set item's placeholder was cut off and is now "angles, with commas".
- Number script: 149 of 149 checks, exit 0.

Backlog: 1 bullet under `Raised later (exam second item stage0):`.
