# measure-prob level 3: performance task (PLAN 2a Phase 3 retrofit)

- File: `app/content/courses/measure-prob/homework-3.json`, item `h-prove-urn`, index 8 (item 9 of 9; nothing converted, the homework had 8 items).
- Kind `derivation` (longform, empty box, no tags), difficulty 5, skill `mt-martingale`.
- Objective matched: l12 "Prove a process is a martingale with respect to a filtration." l10 (prove the tower property) and l13 (prove optional stopping under bounded times) also match. l13 was not chosen: its proof is laid out line by line in two l13 order screens and is part 1 of this homework's `h-long`, so a blank box would test recall. l12 takes a process the course proves nothing about: markov l17 screens 8 and 9 check the Pólya share on the first draws, but the proof for every $n$ on $\mathcal{F}_n$ is new.
- Task: the Pólya urn (one red, one blue, add one of the drawn colour). Prove $M_n = R_n/(n+2)$ is a martingale for the draw filtration: adapted, integrable ($0 < M_n < 1$), and the step $E[M_{n+1} \mid \mathcal{F}_n] = M_n$ via the conditional chance of red on each atom (not independence). Then $P(\text{draw } n+1 \text{ red}) = 1/2$ by the tower property, and $R_n$ is not a martingale.
- Rubric 2, 2, 4, 1, 1. Rows 2 and 3 (the conditions, the step) are `required`. Row 2 opens with "Tick only if".
- Fresh: the lessons and homework use walks, tosses, the Doob forecaster, gains and stopped walks, all with independent steps. Grep terms: `urn`, `ball`, `Pólya`, `R_n`, `share`, `S_n^3`.

## Gates

1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; expected warning "measure-prob/L3: has a performance task, remove from perf-pending".
2. `VOICE_BASE=app/content/courses/measure-prob python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `python3 docs/reports/measure-prob-3-perf-numbers.py` (venv with sympy): exit 0, 65,630 checks. Every atom of $\mathcal{F}_n$ for $n \le 12$ is enumerated exactly. The checks cover the step, the bounds, $E[M_n]$, $P(\text{red})$, $R_n + M_n$ and the red-red atom. The second route is sympy algebra plus the uniform law of $R_n$, with a seeded simulation.
4. `node tools/playthrough.mjs --set measure-prob/homework-3 --local-cdn <pkgs>`, with and without `--mobile`: All passed (2 longform marked by the button). A scratch KaTeX render in the 356 px card column shows the one display equation fits.

One backlog bullet. No course.json change.

Overlapping screens: l12-martingales-defined screens[1] (adapted, integrable, the one-step condition), [2] (a martingale from squares, step by conditional expectation), [5] (subtract the drift) and [6] (dependent steps, checking one step back), markov l17 screens[8] and [9] (the Pólya share on the first draws, and a martingale keeps its mean); new parts: the Pólya urn proved for every $n$ on the draw filtration, the step $E[M_{n+1} \mid \mathcal{F}_n] = M_n$ by the conditional chance of red on each atom, $P(\text{draw } n+1 \text{ red}) = 1/2$ by the tower property, and $R_n$ not a martingale.
