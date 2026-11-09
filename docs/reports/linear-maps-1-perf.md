# linear-maps level 1: performance task (PLAN 2a Phase 3 retrofit)

- File: `app/content/courses/linear-maps/homework-1.json`, item `h-prove-extend-basis`, index 9 (item 10 of 10; the homework had 9, nothing converted).
- Kind `derivation` (longform, empty box), difficulty 5, skill `lx-spaces`.
- Matched objective: l4 "Prove that every basis has the same length, and extend an independent list to a basis." Chosen over l2 and l3 (also prove) because its product uses both.
- Task, on $U = \{p \in \mathcal{P}_3(\mathbb{R}) : p(0) = p(2)\}$, a space no lesson uses: (a) $U$ is a subspace; (b) $(x^2 - 2x, x^3 - 3x^2 + 2x)$ is independent in $U$, extended to a basis and proved one; (c) every basis of $U$ has length 3, so two never span and four are dependent; (d) optional, marked so in the prompt: $\mathcal{P}_3(\mathbb{R}) = U \oplus \operatorname{span}(x)$.
- Rubric 2, 2, 3, 2, 1. Rows 1 to 4 `required` (9 points): (a), both rows of (b), (c). `node tools/rubric-passes.mjs --item content/courses/linear-maps/homework-1.json#h-prove-extend-basis`: one minimal pass, rows 1 to 4; only row 5, the optional (d), can be left out.
- Overlapping screens: l2 screens[3], [4] (the subspace checks; $f(0) = f(1)$ survives sums), l3 screens[3], [5] (the lemma on dependent lists; independent never longer than spanning), l4 screens[3] (same length, which (c) repeats on $U$), [5] and quiz[0] (the $p(1) = 0$ basis), [6] (extension in $\mathbb{R}^4$ by the $\mathbf{e}_j$), [7], [8] (length $n$ is enough; the dimension formula), `h-dim-sum-longform`. New: the space $p(0) = p(2)$, finding a spanning list of $U$ before extending (the lesson extends inside $\mathbb{R}^4$ with the $\mathbf{e}_j$), proving the extended list independent and spanning line by line, and the direct sum with $\operatorname{span}(x)$.
- Freshness grep (course folder, every hit read): `p(0) = p(2)`, `x^3 - 3x^2`, `x^3 - 4x`, `x^2 - 2x`, `span}(x)`, `every basis`, `same length`, `extend`. Only l4's statement and the extension screens share words. `node tools/fresh-check.mjs --file content/courses/linear-maps/homework-1.json`: 0 hits.

## Gates

1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors. Expected warning "linear-maps/L1: has a performance task, remove from perf-pending". Manifest `perf` lists `linear-maps/L1 -> h-prove-extend-basis, derivation, self, gates`. Manifest restored before commit.
2. `VOICE_BASE=app/content/courses/linear-maps python3 docs/reviews/voice-scan.py 35`: 0 and 0 (no sentence of the item over 25 words).
3. `<venv>/bin/python -I docs/reports/linear-maps-1-perf-numbers.py`: exit 0, 57 checks. sympy evaluation against coefficient vectors with the row $(0, 2, 4, 8)$: membership, closure on 300 random pairs, independence by solving and by rank, $U$ as a null space of dimension 3, the extension run by rank, $x^3 - 4x = q_2 + 3q_1$ by expansion and by solving, unique coordinates for 200 random members, random bases, four always dependent, (d) by rank 4 and an explicit split. Passing tick sets listed.
4. `node tools/playthrough.mjs --set linear-maps/homework-1 --local-cdn <pkgs>`, with and without `--mobile`: All passed, 2 longform marked by the button. Shots read at 440 px; a scratch KaTeX column check (356 px) found the one display inside the column.

No backlog bullets (the coach tip over the marked shot and the first-viewport-only shot are already in the inbox). No course.json change. No book citation added.
