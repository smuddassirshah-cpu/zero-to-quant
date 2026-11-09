# Brief: Fluency families, first wave (topics 0.2, 0.3, 1.3; PLAN 2d "G content"; gap file G)

A Fluency set is 20 fresh typed-answer items for one procedural lesson, pass at 90%, repeatable. You write families as JSON; the engine draws the items. Binding: `docs/AUTHORING.md` section 16 (the family shape, every `vars` kind, `let` function and format), the `numeric` and `expression` widget sections, and section 6 (voice). Design background: `docs/briefs/engine-gen.md`. Fixture to copy from: the sample set under `app/tools/fixtures/`.

## Rules for a family

- One technique per family; the set for a lesson holds one to four families that together cover what that lesson teaches and nothing later. Open the lesson first: use its notation, its wording for the instruction ("Expand", "Factorise fully", "Solve") and only ideas taught up to that lesson.
- Typed answers only (`numeric` or `expression`). Give `form` wherever an equal expression in the wrong shape must fail (expand, factorise, simplify). Antiderivatives use `upToConstant`.
- Variety: at least 60 distinct prompts in 200 draws (the validator counts). Vary sign, size, the letter and the position of the unknown. Use `where` to remove degenerate draws (a zero coefficient, a common factor that changes the task, a repeated root where two are asked for), not to hide a formatting fault.
- Difficulty is level within a set: no draw may need a step the lesson does not teach. Keep numbers hand-sized; no calculator unless the lesson uses one.
- Each family names two or three `wrong` slips a learner really makes (sign lost, one term not multiplied, power not reduced), each with a one-sentence `line`. A slip that can equal the answer for some draw must be excluded by `where`.
- `solution`: two to four short steps with the draw's own numbers, ending in the answer.
- No new teaching and no new notation in a Fluency set.

## Sets to write (set id `fluency-<lesson id>`; one agent per course group)

| Agent | Course | Lesson: families |
| --- | --- | --- |
| 1 | `equations` | l2-like-terms: collect like terms. l3-opening-brackets: expand one bracket; expand two and collect. l4-putting-brackets-back: take out a common factor. l6-undoing-in-reverse: two-step linear equation. l7-unknowns-both-sides: unknown on both sides, with brackets. l8-clearing-fractions: linear equation with fractions. l13-changing-the-subject: rearrange a formula (three shapes). l15-swapping-in: simultaneous linear pair, answer as the vector $(x, y)$ |
| 2 | `quadratics`, and one set in `functions` | l1-two-brackets: expand $(x+a)(x+b)$ and $(ax+b)(cx+d)$. l2-product-and-sum: factorise monic. l3-leading-coefficient: factorise non-monic. l4-difference-of-squares. l6-completing-the-square. l7-the-formula: roots, rational and to 2 dp. functions l8-line-through-two-points: gradient, then the line's equation |
| 3 | `exp-log`, `trig` | exp-log l3-strange-powers: index laws; evaluate zero, negative and fractional powers. l6-products-into-sums: log laws, combine and split. l8-solving-for-the-power: solve $a^x = b$ exactly and to 3 sf. l10-natural-log: solve with $e$ and $\ln$. trig l1-squares-on-sides: missing side. l3-sides-and-angles: side from an angle. l4-exact-values. l7-arc-length: degrees to radians, arc length |
| 4 | `series`, `counting` | series l2-any-term: nth term of an arithmetic sequence. l3-multiplying-each-time: geometric term. l6-gauss: arithmetic sum. l7-shifted-copy: geometric sum. l8-adding-forever: sum to infinity. l11-powers-of-a-bracket: a named coefficient. counting l3-choosing-in-order and l4-choosing-without-order: evaluate arrangements and choices |
| 5 | `limits` | l2-computing-limits: factor-and-cancel limits. l7-power-rule: polynomials, negative and fractional powers. l9-products-quotients. l10-inside-function: chain rule. l11-standard-derivatives: $e^x$, $\ln$, $\sin$, $\cos$ mixed with chain. l12-implicit: $dy/dx$ at a point. l13-peaks-and-troughs: stationary points of a cubic |
| 6 | `integrals` | l6-working-backwards: antiderivatives of powers. l7-evaluating: definite integrals. l9-undo-chain: substitution. l10-undo-product: by parts. l14-splitting-fractions: partial fractions, then integrate |
| 7 | `taylor`, `multivar` | taylor l1-tangent-approx: linear approximation at a point. l6-matching-derivatives: a named Taylor coefficient. multivar l1-two-inputs: first partial derivatives. l3-second-partials |

## Checks (all required before hand-back)

1. `docs/reports/fluency-<course>-numbers.py`, run with `<scratchpad>/venv/bin/python`: for every family it reads `node tools/fluency-sample.mjs --set <course>/<set id> --n 100 --json`, and from the variable values alone derives the answer again with sympy, compares with the engine's resolved answer, and checks each `wrong` differs. Exit 0.
2. From `app/`: validator 0 errors, no new warnings on your files; `node tools/test-fluency.mjs --local-cdn <pkgs>` green.
3. `node tools/playthrough.mjs --fluency <course>/<set id> --local-cdn <pkgs>` for every set, and with `--mobile`: green.
4. Voice scan `docs/reviews/voice-scan.py 35` on the course folder: 0 and 0.
5. Read 20 drawn items of every family as a learner would (`fluency-sample.mjs --n 20`): no `1x`, `+-`, `x^1`, `0x`, double minus, unreduced fraction or prompt that gives the answer away. Say in the report that you did.
6. Report `docs/reports/fluency-<course>.md` (table: set, family, distinct prompts in 200, `form`, slips). Engine limits, including any format or function you needed and did not have, go to `docs/BACKLOG-INBOX.md` under `Raised later (fluency <course>):`. Do not work round a missing format with a clumsy prompt: raise it and skip that family.

Do not edit engine files, `course.json`, lessons or other courses. Commit per course in your worktree; never push.
