# Problem sets: limits (brief `docs/briefs/chained.md`)

Files: `app/content/courses/limits/problems-1.json` (more levels below as they land). Numbers: `docs/reports/problems-limits-numbers.py` (exits 0).

## Sets

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-broker-schedule | 3 (3 / 0) | l1, l3, l4 | 3 |
| problems-1 | p-rational-features | 4 (3 / 1) | l1, l2, l3, l4 | 4 |
| problems-1 | p-fit-the-constants | 4 (3 / 1) | l2, l3, l4 | 5 |
| problems-1 | p-print-wiggle | 3 (3 / 0) | l1, l4 | 4 |

Typed parts: level 1 12 of 14. Every lesson of the level appears in at least one problem, and every problem draws on at least two.

Level 1 chains. p-broker-schedule: a one-sided limit at the join, the constant that removes the jump, then what large orders pay per £1 thousand. p-rational-features: the limit at the hole by cancelling, the kind of break at the other zero of the bottom, the far-out level, then the first whole $x$ inside 0.01 of that level (the definition of a limit at work). p-fit-the-constants runs backwards: the far-out level fixes $a$, a finite limit at 2 fixes $b$, the other zero of the bottom is an asymptote, and the value that repairs the hole is $\tfrac{7}{3}$. p-print-wiggle bounds a $\tfrac{\sin t}{t}$ wiggle, squeezes it to the limit, then finds when the bound keeps the price within a penny. Each later part restates the value it uses; the slip that follows from the commonest slip in the part before has its own `wrong` (the dropped fee in the commission, $a = \tfrac{1}{2}$ in the constants).

Level 1 teaches no derivative, so no part asks for a slope; the squeeze uses only $-1 \le \sin t \le 1$ from l4.

## Checks

| check | problems-1 |
|---|---|
| numbers script | 0 failures (210 checks) |
| validator | 0 errors, 0 warnings on the file |
| playthrough `--local-cdn` | green (14 parts) |
| playthrough `--mobile` | green; 440 px shots of every part read, no fault |
| voice scan 35 (course folder) | 0 and 0 |

## Fresh-check

problems-1: 0 hits at the gate. At triage settings (`--min-run 8 --min-share 0`) 20 hits, all the form sentence "Give an exact fraction, or a decimal to 4 places" shared with other courses' problem sets. Stock phrasing. The settings (a commission schedule with a parameter, $\tfrac{2x^2 - 2x - 12}{x^2 - 9}$, fitting $a$ and $b$, a $\tfrac{4\sin t}{t}$ wiggle after a print) are new to the course; joining two pieces is l3's idea, met here with a fee and a far-out question.

## Engine limits

None raised at level 1.
