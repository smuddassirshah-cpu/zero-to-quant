# Engine backlog inbox

Content agents append their engine and canvas limitations here, under `Raised later (<course> level <n>):`, as bullets. An integration pass numbers them into `ENGINE-BACKLOG.md` and clears this file.

Cleared by engine pass AE part 1 (items up to 1051 in `ENGINE-BACKLOG.md`); the previous text is in commit 3e95964.

Raised later (delta AE-1):
- `reuse-shapes.mjs` `function`, rule too loose (R1, 1 hit): a function under a fraction bar is read as the function itself (`analysis/problems-5` `p-root-sums`, $\sqrt{x}$ on $[0, 9]$, against `integrals/l16` $\int_0^9 \tfrac{dx}{\sqrt{x}}$). Key on the whole quotient.
- `reuse-shapes.mjs` `function` and `transform`, rule too loose (R2, 2 hits): shapes are read from `wrong` entries (`integrals/problems-3` `power-down`, `quadratics/problems-4` part 3 `signs`). Take no shape from a `wrong` entry or an incorrect option.
- `reuse-shapes.mjs` `pair`, rule too loose (R3, 7 hits: markov 5, regression 2): one-decimal chances pair up in any sentence. Count stock decimals as numbers of the sentence (no decimal but the two keys) and require one of the two values to be a key of the source unit. The true positive (l23, keyed 0.3, "$r = 1 - 0.7 = 0.3$") keeps both.
- `reuse-shapes.mjs` `region`, rule too loose (R4, 1 hit): a plane's intercepts projected on $z = 0$ match a triangle of another course (`multivar/problems-5` against `vector-calc/homework-3`). Run the projected form in the same course only.
- `reuse-shapes.mjs` `function`, rule too loose (R5, 2 hits): a cylinder's equation with the range of $z$ is read as "$x^2 + y^2$ on $[0, 2]$" (`vector-calc/problems-3` `p-can-curl`). Require the interval's named variable to occur in the function, and keep a level set's right-hand side.
- `same-course-reuse.mjs` `matrix`, a miss: a symmetric matrix equal to a lesson's after $a\mathbf{M} + b\mathbf{I}$ has the lesson's eigenvectors and is not seen (`eigen/problems-2` `p-oval-pond`, $10\boldsymbol{\Sigma} - 2\mathbf{I}$ of l5 `screens[9]`). Add it as an advisory for 2 by 2 symmetric matrices with a nonzero off-diagonal.
Raised later (problems validation):
- A `wrong[]` entry above 1 on a `unit: "%"` numeric draws the over-100 warning meant for the key (validator item 515). A slip such as typing the ratio 1.2 as "120%" for a 20% rise cannot be routed without `"over100": true`, which also silences the check on the key. Suggest: apply the over-100 warning to `answer` only, or give a `wrong` entry its own flag. (problems-2 dropped the slip.)
- `fresh-check.mjs`'s shared-formula advisory compares the displayed text, so an equivalent rewrite escapes it: problems-3 first stated the sign-agreement rule as $\tfrac12 + \arcsin(\rho)/\pi$ (homework-3's form, flagged) and now states $1 - \arccos(\rho)/\pi$ (not flagged). Suggest: normalise a few standard identities, or compare formulas by value at seeded points as the expression grader does.
