# Fluency: equations (docs/briefs/fluency.md, agent 1)

Seven sets, thirteen families. Each set uses its lesson's notation (`\dfrac`, letters $x, n, y, t, m$) and its instruction words ("Simplify", "Expand", "Expand and simplify", "Factorise", "Solve", "Make $t$ the subject of").

| set | family | distinct prompts in 200 | `form` | slips |
| --- | --- | --- | --- | --- |
| fluency-l2-like-terms | collect-one-letter | 200 | simplified | flipped-sign, combined-all |
| fluency-l3-opening-brackets | expand-one-bracket | 197 | expanded | first-term-only, sign-slip |
| | expand-two-and-collect | 198 | simplified | second-constant-kept, second-sign-slip |
| fluency-l4-putting-brackets-back | common-factor | 181 | factorised | constant-not-divided, letter-taken-out |
| fluency-l6-undoing-in-reverse | multiply-then-add | 200 | (numeric) | divided-first, sign-of-number |
| | divide-then-add | 199 | (numeric) | multiplied-first, divided-instead |
| fluency-l7-unknowns-both-sides | bracket-one-side | 195 | (numeric) | bracket-first-term, added-unknown |
| | brackets-both-sides | 164 | (numeric) | bracket-first-term, number-sign-kept |
| fluency-l8-clearing-fractions | two-fractions-sum | 162 | (numeric) | right-side-missed, added-bottoms |
| | whole-tops | 176 | (numeric) | lost-bracket, own-bottom |
| fluency-l13-changing-the-subject | subject-from-linear | 194 | none (the answer has no `=`) | divided-one-term, sign-kept |
| | subject-from-product | 167 | none | upside-down, number-left |
| | subject-from-bottom | 169 | none | upside-down, multiplied |

**Skipped:** l15-swapping-in `substitute-linear-pair`. A vector answer typed with the wrong length gets the widget's `length` line with no solution steps (`ZQ.gen.playerItem` sets no `byKey.length`), so playthrough `--fluency` fails "the wrong-answer chip shows no worked maths". Raised in BACKLOG-INBOX. The draft below passed the validator, the recompute and test-fluency; it can go in as `fluency-l15-swapping-in.json` once that is fixed.

**Departures:** l4 draws only prime common factors (2, 3, 5, 7), because `form: "factorised"` cannot refuse a partial factorisation such as $2(3x + 6)$ (raised); the prompt says "Factorise", not "fully". l6, l7 and l8 have two families each, two shapes the lesson teaches, within the brief's one to four.

## Checks
1. `docs/reports/fluency-equations-numbers.py` (sympy; 200 draws a family, 2,600 draws): rebuilds each prompt's maths from the vars, solves it, compares the engine's key, re-derives every slip by solving the slip's own equation, and checks each slip differs from the key and lies outside tolerance. Exit 0. A mutation run (key and one slip shifted by 1) failed as it should.
2. Validator: 0 errors; warnings unchanged at 4103, none on these files. `test-fluency.mjs --local-cdn`: 333/333.
3. Playthrough `--fluency` of all seven sets, desktop and `--mobile`: green. Screenshots read (item, wrong chip, end card, at 440 px and desktop): no layout fault.
4. Voice scan 35 on the course folder: 0 and 0.
5. I read 20 drawn items of every family as a learner would, and scanned 200 of each for `1x`, `0x`, `+-`, `--`, `^1`, `+0` and `/1`: no hits. Fixed on reading: a line that said "The sign in front of 1", bare minus signs outside maths in lines, "has a $n$", and a slip that drew $5n(1-1)$.

## Appendix: the skipped l15 draft
```json
{
  "id": "fluency-l15-swapping-in",
  "course": "equations",
  "lesson": "l15-swapping-in",
  "title": "Fluency: swapping in",
  "n": 20,
  "pass": 0.9,
  "minutes": 12,
  "families": [
    {
      "id": "substitute-linear-pair",
      "skill": "solve a linear pair by substitution",
      "vars": {
        "x0": { "int": [-5, 5], "not": [0] },
        "m": { "int": [-3, 3], "not": [0] },
        "c": { "int": [-9, 9], "not": [0] },
        "a": { "int": [1, 5] },
        "b": { "int": [-4, 4], "not": [0, 1] }
      },
      "let": {
        "y0": "m*x0 + c",
        "e": "a*x0 + b*(m*x0 + c)",
        "k": "a + b*m",
        "bc": "b*c",
        "kx": "(a + b*m)*x0",
        "xs": "(a*x0 + b*(m*x0 + c) - c)/max(1, a + b*m)",
        "ys": "m*(a*x0 + b*(m*x0 + c) - c)/max(1, a + b*m) + c"
      },
      "where": ["k > 0", "x0 != y0", "abs(y0) <= 15", "abs(e) <= 40"],
      "prompt": "Solve $y = {poly(x; m, c)}$ and ${a:c}x{b:+c}y = {e}$ by substitution, giving $(x, y)$.",
      "widget": { "kind": "expression", "answer": "({x0}, {y0})", "accept": ["({x0},{y0})"], "keyboard": "algebra" },
      "wrong": [
        { "id": "bracket-dropped", "tex": "({xs:frac}, {ys:frac})", "line": "Put ${poly(x; m, c)}$ in brackets, so the ${b}$ multiplies the ${c}$ as well." },
        { "id": "swapped-order", "tex": "({y0}, {x0})", "line": "Give $x$ first, then $y$: the point is $(x, y)$." }
      ],
      "solution": [
        "Swap ${poly(x; m, c)}$ in for $y$, in brackets: ${a:c}x{b:+c}({poly(x; m, c)}) = {e}$.",
        "Expand and collect: ${poly(x; k, bc)} = {e}$, so ${k:c}x = {kx}$ and $x = {x0}$.",
        "Then $y = {m:()} \\times {x0:()} {c:+} = {y0}$, so the answer is $({x0}, {y0})$."
      ]
    }
  ]
}
```

Its recompute function, `substitute_linear_pair`, is in the number script, commented out of `FAMILIES`.
