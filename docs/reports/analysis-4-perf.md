# analysis level 4: performance task (PLAN 2a Phase 3 retrofit)

- File: `app/content/courses/analysis/homework-4.json`, item `h-prove-uniform-diagonal`, index 9 (item 10 of 10; the homework had 9, nothing converted).
- Kind `derivation` (longform, empty box), difficulty 5, skill `an-continuity`.
- Matched objective: l19 "Tell pointwise from uniform convergence, and prove that a uniform limit of continuous functions is continuous." All five objectives start with prove; l19's product uses both an $N$ and a $\delta$, and `h-prove-square` already asks for l15's.
- Task: (a) the uniform limit theorem at a point of any $D$, then $f_n(x_n) \to f(a)$ for every $x_n \to a$; (b) $h_n(x) = \tfrac{1}{1 + nx^2}$: limit 1 at 0, else 0, not uniform on $\mathbb{R}$; (c) uniform on $|x| \ge \tfrac12$ with $\sup = \tfrac{4}{n + 4}$, smallest $N = 1330$ for 0.003, checked against $\tfrac{4}{1333}$; optional: not uniform on $(0, \infty)$ though the limit is continuous.
- Rubric 3, 2, 2, 2, 1. Rows 1 to 4 `required` (9 points), one per named part, each worded by result (by $\delta$ or by sequences; by (a) or by $x = \tfrac{1}{\sqrt n}$). `rubric-passes.mjs`: the only minimal pass is rows 1 to 4; row 5, marked "Optional, one more point:", can be left out.
- Overlapping screens: l19 screen 7 (the $\tfrac{\varepsilon}{3}$ proof, ordered), screen 8 ($n$ before $\delta$), screens 2 and 4 (a sup gap and the first $n$ below 0.01), screen 5 (a peak that keeps its height), quiz `q-unif-cont`; l15 screen 9 (the sequential criterion); `h-pointwise-flaw`, `h-sup-gap-poly`, `r-sin-n`. New: the moving point $f_n(x_n)$, a family no screen uses (the exam's $\tfrac{x}{1 + nx^2}$ differs), a limit shown discontinuous to rule out uniformity, an exact sup giving the smallest $N$, and a continuous limit that is still not uniform.
- Freshness grep (course folder and exams, every hit read): `1 + nx^2`, `f_n(x_n)`, `f(x_n)`, `uniform`, `1 + n`, `0.003`, `1330`, `1329`; `fresh-check.mjs --file`: 0 hits; at `--min-run 8 --min-share 0` two stock phrasings (the uniform definition, "Optional, one more point").

## Gates

1. Validator: `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; expected warning "analysis/L4: has a performance task, remove from perf-pending"; no `[perf-optional-row]` on the item. Manifest restored before commit.
2. Voice: `VOICE_BASE=app/content/courses/analysis python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. Numbers script: `<venv>/bin/python -I docs/reports/analysis-4-perf-numbers.py`: exit 0, 62 checks. Limits in sympy and floats; the sup by the derivative's sign and a grid; $N = 1330$ by Fraction search and sympy's inequality; 1334 for the crude bound; passing tick sets listed and matched against `rubric-passes.mjs --json`.
4. Playthrough: `node tools/playthrough.mjs --set analysis/homework-4 --local-cdn <pkgs>`, with and without `--mobile`: All passed, 2 longform marked by the button. The 440 px shot showed two inline triangle-inequality chains clipped; both now `aligned` displays, re-shot clean.

One backlog bullet. No course.json change.
