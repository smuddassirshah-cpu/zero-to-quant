# Report: analysis level 1, "The real numbers"

Course `analysis` (topic 1.10, strand pure), level 1, from `## Level 1` of `docs/briefs/analysis.md`. Lesson ids, names, objectives and skills are those of `app/content/courses/analysis/course.json` (all five lessons carry `an-reals`). The content was authored and committed earlier (commit `27a41aa`, "report pending"), but the authoring agent's report write was refused. This report was written afterwards from the committed files. Every stated number was recomputed twice and every code widget was re-run. The `proof` lessons named in the brief exist, and the lessons cite them by title ("the proof course's lesson on contradiction", "saying the opposite"). Proofs end with $\blacksquare$. No topic exam was written, as the brief says.

## Files

All in `app/content/courses/analysis/`.

| File | Screens | Quiz / items | Canvases | Notes |
|---|---:|---:|---|---|
| `l1-gaps-in-the-rationals.json` | 11 | 4 | plane ($y = x^2$ against $y = 2$), number-line (zoom 1.4135 to 1.415, draggable point), table, console | hook squares of $\tfrac32, \tfrac75$ (with $\tfrac{17}{12}, \tfrac{41}{29}, \tfrac{99}{70}$ given), $p^2 - 2q^2$ table, drag to show the square jumps over 2, opening `choice`, "$p$ even" `choice`, $q^2 = 2k^2$ `expression`, 7-line `order` with two distractors, contradiction `choice`, $\sqrt4$ trap (tap rows), $\sqrt3$ edge `choice`, float transfer `choice` |
| `l2-least-upper-bound.json` | 12 | 4 | pair (number-line over a tappable table), number-line | tap the upper bounds of $\{1 - \tfrac1n\}$, drag $s$ to the supremum, $\inf A = 0$ a minimum, $(0, 3]$ `multi`, $\{(-1)^n + \tfrac1n\}$ table, "no largest element" trap, part one `choice`, part two `numeric` 101 and `expression` $\tfrac1\varepsilon$, 5-line `order` with two distractors, empty set and $\mathbb{N}$ `multi`, Sharpe-ratio transfer `numeric` 1.2 |
| `l3-completeness.json` | 12 | 4 | number-line (nested intervals, fraction labels), console, table | bisection table for steps 2 to 4, width $\tfrac1{1024}$, the axiom's hypotheses `multi`, case one `choice` and `numeric` 95, which property fails `choice`, case two `numeric` 12, 6-line `order` with two distractors, density-is-not-completeness trap, $\inf A = -\sup(-A)$ edge `choice`, `bisect_sqrt2` code, implied-volatility transfer `numeric` 27.5% |
| `l4-archimedes.json` | 12 | 4 | number-line, console | drag $x$ past every whole number, negation `choice`, completeness `choice`, $s - 1$ `choice`, 5-line `order` with two distractors, $\varepsilon = 0.003$ `numeric` 334, density table ($n$, $m$, $\tfrac mn$), "$\tfrac mn < b$" `choice`, wrong-$m$ trap, irrationals dense `choice`, `archimedes_n` and `rational_between` code, tick-size transfer `numeric` 1429 |
| `l5-counting-infinite-sets.json` | 12 | 4 | number-line (arrows), grid (paths, shaded repeats), table, console | position of $-3$ `numeric` 7, first six of the walk (ordered taps), positions table, why skip $\tfrac22$ `choice`, opening `choice`, diagonal-digits table, "$x$ not in the list" `choice`, 6-line `order` with two distractors, rationals trap (tap rows), 0s and 9s edge `choice`, `rational_at` and `index_of` code, countably many programs transfer `choice` |
| `review-1.json` | | 9 | table | difficulties 3, 3, 2, 3, 3, 2, 3, 4, 4; covers l1 ($\sqrt{12}$ flawed line), l2 (sup and inf of $\{(-1)^n(1 - \tfrac1n)\}$; $\inf\{\tfrac1n\} = 0$ `order`), l3 (what $\mathbb{Q}$ lacks; $\sqrt3$ bisection), l4 ($\varepsilon = 0.004$; density for 0.7, 0.705), l5 (position of $\tfrac34$; diagonal on $\mathbb{N}$) |
| `homework-1.json` | | 9 | console | difficulties 5, 4, 3, 4, 4, 4, 4, 5, 3; $\sqrt2 + \sqrt3$ `order` (three distractors), threshold `expression` $\tfrac{1}{\sqrt\varepsilon}$, `numeric` 101, $\sup$ and $\inf$ of $\{x \in \mathbb{Q} : x^2 < 2\}$, density near $\sqrt2$ table, 20th fraction, `bisect_sqrt` code, `longform` (an irrational in every gap; five 2-point rubric lines, full model answer), uncountable set `choice` |

The quiz items (4 per lesson, difficulties 2 to 3) are as follows. l1: $577^2 - 2 \times 408^2$, $\sqrt{9/4}$, which roots are irrational (`multi`), $0.1 + 0.2$. l2: $\{\tfrac1n\}$, $n$ for 0.999, $\{x^2 < 9\}$, high-water mark. l3: which set has a supremum, $\sqrt3$ bisection, $s = 1.41$ bound, why bisection for implied volatility works. l4: $\varepsilon = 0.07$, no smallest positive rational, recipe for $\tfrac13$ and $\tfrac12$, why $n + 1 > s$ contradicts. l5: position of 4, position of $\tfrac16$, which sets are countable (`multi`), a three-digit diagonal.

## Which widget grades each proof step

- $\sqrt2$ irrational (l1): opening assumption `choice` (distractor "suppose $\sqrt2$ is irrational"); "$p^2$ even so $p$ even" `choice` (distractor "every square is even"); $q^2 = 2k^2$ `expression` (wrong forms $4k^2$, $k^2$); whole proof `order`, 7 lines plus the brief's two distractors, each with a `why`; the clash `choice`.
- $\sup\{1 - \tfrac1n\} = 1$ (l2): part one `choice`; part two at $\varepsilon = 0.01$ `numeric` (101); threshold `expression` `\frac{1}{\varepsilon}`; whole proof `order`, 5 lines, distractors "choose $n = 100$" and "so $1 \in A$".
- $s^2 = 2$ for $s = \sup\{x \ge 0 : x^2 < 2\}$ (l3): hypotheses `multi`; $\tfrac{1}{n^2} \le \tfrac1n$ `choice`; bound at $s = 1.4$ `numeric` (95); which property fails `choice`; bound at $s = 1.5$ `numeric` (12); whole proof `order`, 6 lines, distractors "density gives $s$" and "choose $n = 96$".
- Archimedean property (l4): negation `choice`; why $s = \sup \mathbb{N}$ exists `choice`; why some $n > s - 1$ `choice`; whole proof `order`, 5 lines, distractors "let $s$ be the largest whole number" and "then $s + 1 > s$". Density: $n$, $m$ and $\tfrac mn$ by `table`; "$\tfrac mn < b$" by `choice`.
- Diagonal argument (l5): opening `choice`; the diagonal number by `table`; "$x$ is not in the list" `choice`; whole proof `order`, 6 lines, distractors "add one to each digit" and "so $x$ is irrational".
- Flawed-line spots: the l1 trap, the l5 trap and review item 1, each by `tap-regions` on a `table` with `tap: rows`.
- Whole proofs written out: the homework `longform` (between any two reals lies an irrational), rubric 2 + 2 + 2 + 2 + 2 = 10.

## Validator

`node tools/validate.mjs` from `app/`: **0 errors**, 364 warnings, none in a level 1 file. The only analysis warning is the course's "not yet written: 14 of 24 lessons, 3 of 5 reviews, 3 of 5 homework" (levels 3 to 5). Run again after the text fix below: still 0 errors.

## Playthrough

With `--local-cdn` set to the scratchpad `pkgs` folder (its `fetch.log` ends `exit 0`), after the text fix below.

| Target | Result |
|---|---|
| `--lesson analysis/l1-gaps-in-the-rationals` | ok, 15 checks, quiz 4/4 |
| `--lesson analysis/l2-least-upper-bound` | ok, 16 checks, quiz 4/4 |
| `--lesson analysis/l3-completeness` | ok, 16 checks, quiz 4/4 |
| `--lesson analysis/l4-archimedes` | ok, 16 checks, quiz 4/4 |
| `--lesson analysis/l5-counting-infinite-sets` | ok, 16 checks, quiz 4/4 (the code solutions pass in Pyodide) |
| `--set analysis/review-1` | ok, 9 items, recorded 9 of 9 |
| `--set analysis/homework-1` | ok, 9 items, marked 9 of 9 right, 41 of 41 marks |

No screenshots were taken in this pass. The original authoring run's layout faults are the six "Raised later (analysis level 1)" bullets already in `docs/BACKLOG-INBOX.md`: number-line fine-step labels, close tap targets, pair scaling, point labels over intervals, table width on a phone, and `derive` floor at exact boundaries. Each has its workaround in the files.

## Code widgets

Each solution and each starter was run against its hidden tests in CPython (`code_check.py`), and the playthrough ran the solutions again in Pyodide. Every starter is a body of `...` and fails every test.

| Widget | Tests | Solution passes | Starter passes |
|---|---:|---:|---:|
| l3 `bisect_sqrt2(steps)` | 7 | 7 | 0 |
| l4 `archimedes_n(eps)`, `rational_between(a, b)` | 10 | 10 | 0 |
| l5 `rational_at(k)`, `index_of(p, q)` | 12 | 12 | 0 |
| homework `bisect_sqrt(c, a, b, steps)` | 8 | 8 | 0 |

Expected values, each also recomputed by a second method (below):

- `bisect_sqrt2`: 0 → $(1, 2)$, 1 → $(1, \tfrac32)$, 4 → $(\tfrac{11}{8}, \tfrac{23}{16})$, 10 → $(\tfrac{181}{128}, \tfrac{1449}{1024})$, 20 → $(\tfrac{741455}{524288}, \tfrac{1482911}{1048576})$; 40 halvings straddle the root with width $2^{-40}$.
- `archimedes_n`: $\tfrac{3}{1000}$ → 334, $\tfrac1{100}$ → 101, $\tfrac13$ → 4, 2 → 1.
- `rational_between`: $(\tfrac{31}{100}, \tfrac{32}{100})$ → (32, 101), $(\tfrac13, \tfrac12)$ → (3, 7), $(-\tfrac12, -\tfrac13)$ → (−3, 7), $(0, \tfrac1{10})$ → (1, 11), $(\tfrac75, \tfrac{10}{7})$ → (51, 36), and a gap near 1.4142.
- `rational_at`: 1 → 1, 8 → $\tfrac32$, 10 → $\tfrac15$, 20 → $\tfrac53$, 50 → $\tfrac58$, 100 → $\tfrac{13}{5}$. `index_of`: (2, 3) → 7, (1, 5) → 10, (3, 4) → 14, (10, 9) → 111, (4, 8) → 2, and a round trip over $k \le 100$.
- `bisect_sqrt`: $(2, 1, 2, 4)$ → $(\tfrac{11}{8}, \tfrac{23}{16})$, $(3, 1, 2, 3)$ → $(\tfrac{13}{8}, \tfrac74)$, $(3, 1, 2, 6)$ → $(\tfrac{55}{32}, \tfrac{111}{64})$, $(5, 2, 3, 5)$ → $(\tfrac{71}{32}, \tfrac94)$, $(\tfrac12, 0, 1, 4)$ → $(\tfrac{11}{16}, \tfrac34)$, $(10, 3, 4, 8)$ → $(\tfrac{809}{256}, \tfrac{405}{128})$, and 30 halvings for $\sqrt7$.

## Numbers, each computed twice

The scripts are in the scratchpad folder `analysis-reports`: `numbers_l1.py` (163 checks), `points.py` (the canvas points) and `code_check.py`. Each check computes the stated value by two independent routes. One route is an exact `Fraction` or closed form. The other is a brute-force search for the smallest $n$, float or `Decimal` arithmetic, a second diagonal walk that skips repeats with a seen-set instead of a gcd, or a numerical lognormal integral for the option prices. **163 numbers and 92 plotted points checked, 0 discrepancies.**

- l1: $\tfrac94 = 2.25$, $\tfrac{49}{25} = 1.96$, $(\tfrac{17}{12})^2 = 2.006944$, $(\tfrac{41}{29})^2 = 1.998811$, $(\tfrac{99}{70})^2 = 2.000204$. $p^2 - 2q^2$: $9 - 8 = 1$, $49 - 50 = -1$, $289 - 288 = 1$, $1681 - 1682 = -1$, $9801 - 9800 = 1$. Quiz: $577^2 = 332929$, $2 \times 408^2 = 332928$, difference 1. $1.4142^2 = 1.99996164$, $1.4143^2 = 2.00024$; $\tfrac{41}{29} = 1.413793$, $\tfrac{99}{70} = 1.414286$. $p^2 \bmod 3$ for $p = 1$ to 6: 1, 1, 0, 1, 1, 0. $6^2 = 36$ is a multiple of 4 (trap) and of 12 (review). `2 ** 0.5` prints `1.4142135623730951`, its square prints `2.0000000000000004`, a miss of $4.44 \times 10^{-16}$; `0.1 + 0.2` prints `0.30000000000000004`. £9.60 and £10.40 both round to £10.
- l2: $1 - \tfrac1{11} = 0.909$, $1 - \tfrac1{101} = 0.990099$, $1 - \tfrac1{99} = 0.9899$. The smallest $n$ with $1 - \tfrac1n > 0.99$ is 101, and with $> 0.999$ it is 1001. $C = \{(-1)^n + \tfrac1n\}$ starts $0, 1.5, -0.6667, 1.25, -0.8$, with later terms $1.1667$ and $-0.8571$; $\sup C = 1.5$ (attained) and $\inf C = -1$ (not attained). $0.0005 \in (0, 3]$ is below 0.001. The Sharpe ratio $1.2 - \tfrac{0.6}{L}$ is 0.6, 0.9, 1.0, 1.05, 1.08 for $L = 1$ to 5, with supremum 1.2. The high-water mark of £100, £104, £101, £107, £103 is £107. The drag caption formula gives 101 at $s = 0.99$ and 11 at $s = 0.9$.
- l3: kept intervals $[\tfrac54, \tfrac32]$, $[\tfrac{11}{8}, \tfrac32]$, $[\tfrac{11}{8}, \tfrac{23}{16}]$, with $m^2 = 1.5625$, $1.8906$, $2.0664$. After 10 steps: $[\tfrac{181}{128}, \tfrac{1449}{1024}] = [1.4140625, 1.4150390625]$, width $\tfrac{1}{1024}$, and $\tfrac{181}{128} = \tfrac{1448}{1024}$. Case one at $s = 1.4$: $\tfrac{3.8}{0.04} = 95$ (slip 9.5, flip 0.0105); $(1.4 + \tfrac1{96})^2 = 1.98928$, $(1.4 + \tfrac1{95})^2 = 1.98958$. Case two at $s = 1.5$: $\tfrac{3}{0.25} = 12$ (wrong forms 6, 0.0833, 1.3333); $(1.5 - \tfrac1{13})^2 = 2.02515$, $(1.5 - \tfrac1{12})^2 = 2.00694$. Quiz at $s = 1.41$: $1.41^2 = 1.9881$, $\tfrac{3.82}{0.0119} = 321.008$, smallest $n$ 322, $(1.41 + \tfrac1{322})^2 = 1.99687$. $\sqrt3$ bisection: $[1.5, 1.75]$ after 2 steps ($1.75^2 = 3.0625$) and $[\tfrac{13}{8}, \tfrac74]$ after 3 ($1.625^2 = 2.640625$). Transfer (one-year at-the-money call on £100 at zero rate, $C = 100(2\Phi(\tfrac\sigma2) - 1)$, checked against a numerical lognormal integral): £7.97 at 20%, £9.95 at 25%, £11.92 at 30% and £10.94 at 27.5%. The implied volatility for £10.00 is 25.13%, and the next trial is $\sigma = 27.5\%$.
- l4: $\tfrac1{0.003} = 333.33$, smallest $n$ 334, $\tfrac1{333} = 0.003003$, $\tfrac1{334} = 0.002994$. Density for $0.31$, $0.32$: $n = 101$, $na = 31.31$, $m = 32$, $\tfrac{32}{101} = 0.316832$; the wrong $m$ gives $\tfrac{31}{101} = 0.306931$. The ceil trap at $a = 0$, $b = 0.1$ has $n = 11$ and gives $\tfrac{0}{11} = a$. $0.31 + \tfrac{\sqrt2}{1000} = 0.311414$; $\tfrac{\sqrt2}{4} = 0.3536$; $0.315 = \tfrac{63}{200}$. Ticks: the gap is £0.0007, $\tfrac{1}{0.0007} = 1428.57$, smallest $n$ 1429, $\tfrac1{1428} = 0.00070028$, $\tfrac1{1429} = 0.00069979$. Quiz: $\varepsilon = 0.07$ gives 15 ($\tfrac1{14} = 0.0714$, $\tfrac1{15} = 0.0667$); $\tfrac13$ and $\tfrac12$ give $n = 7$, $m = 3$, $\tfrac37 = 0.428571$ (wrong form $\tfrac27 = 0.285714$).
- l5: $-3$ is 7th and 4 is 8th in $0, 1, -1, 2, -2, \dots$ The walk starts $\tfrac11, \tfrac12, \tfrac21, \tfrac13, \tfrac31, \tfrac14$. $\tfrac23$ is 7th, $\tfrac32$ 8th, $\tfrac15$ 10th, $\tfrac51$ 11th and $\tfrac16$ 12th (16th if repeats are counted). Diagonals 2 to 6 hold $1 + 2 + 2 + 4 + 2 = 11$ fractions. The diagonal digits of 0.14159, 0.71828, 0.41421, 0.57751, 0.30103 are 1, 1, 4, 5, 3, so $x = 0.55545\ldots$; the quiz list gives $0.545$. $0.4999\ldots = 0.4 + \tfrac{0.09}{0.9} = 0.5$. A number made of 4s and 5s lies in $[\tfrac49, \tfrac59]$, inside $(0.4, 0.6)$.
- Review: $\{(-1)^n(1 - \tfrac1n)\}$ begins $0, \tfrac12, -\tfrac23, \tfrac34, -\tfrac45, \tfrac56$, with $\tfrac78$ at $n = 8$; sup 1 and inf $-1$, neither attained. $\varepsilon = 0.004$ gives 251 ($\tfrac1{251} = 0.003984$). Density for 0.7, 0.705: $n = 201$, $na = 140.7$, $m = 141$, $\tfrac{141}{201} = 0.701493$. $\tfrac34$ is 14th (18th with repeats). After 3 halvings for $\sqrt3$ the left end is 1.625.
- Homework: $1 - \tfrac1{n^2} > 0.9999$ first holds at $n = 101$ (wrong form 10001). Density for 1.414, 1.4143: $\tfrac{1}{0.0003} = 3333.33$, $n = 3334$, $na = 4714.276$, $m = 4715$, $\tfrac{4715}{3334} = 1.4142172$. The 20th fraction is $\tfrac53$ (19th $\tfrac35$, 21st $\tfrac71$; the 20th cell with repeats is $\tfrac52$). Longform example: $0.31 - \sqrt2 = -1.1042$, $0.32 - \sqrt2 = -1.0942$, $t = \sqrt2 - 1.1 = 0.3142$. The rubric totals 10.
- Canvas points (`points.py`): 92 points in l2 and l3, each checked against $1 - \tfrac1n$, $(-1)^n + \tfrac1n$, $1.2 - \tfrac{0.6}{L}$ or $\pm\tfrac1n$ in floats and in fractions to $5 \times 10^{-7}$. None was off.

## Edit made in this pass

One factual slip, fixed with a targeted edit:

- l1 quiz `q-float`: the `why` of the option "Python adds decimals wrongly" said "The sum is computed exactly". That is false. The exact sum of the stored 0.1 and 0.2 is 0.30000000000000001665..., and the addition rounds it to 0.30000000000000004. The line now reads "You blamed the adding. Python follows the float rules exactly; the trouble starts with inputs that were already rounded." The validator and the lesson replay were green after the edit.

## Departures from the brief

- l1: the hook asks only for the squares of $\tfrac32$ and $\tfrac75$; the other three squares are given in the table, and the $p^2 - 2q^2$ column is then filled for all five. The rationals near 1.41421 are shown by a draggable point on a zoomed `number-line` that stops at four-decimal fractions, not by a static picture. $\sqrt{9/4} = \tfrac32$ (the copied proof must break) is a quiz item, not a lesson screen.
- l2: the upper-bound hook taps the candidates as rows of a `table` stacked under the number line (`pair`, `active: "right"`, `stack: true`), not as points, because 0.99 and 1 sit about 2 px apart (backlog bullet). The empty set and $\mathbb{N}$ share one `multi` screen instead of a separate edge-case screen.
- l3: case two asks for the bound 12 (the brief allowed 12 or 13). The explanation then says $n = 13$ works and $n = 12$ happens to work too. The transfer asks for the next bisection trial (27.5%) on a three-row price table.
- l4: "density means there is a next rational" is a quiz item (there is no smallest positive rational), not part of the trap screen. The transfer is a `numeric` (1429 ticks a pound) with two model prices, £10.0012 and £10.0019.
- l5: the walk's positions are asked by ordered taps on the grid (the first six) and a `table` (three positions), not by three `numeric` screens. The code tests reach $k = 100$ and include `index_of(10, 9)` = 111.
- Homework: the threshold item uses $\{1 - \tfrac1{n^2}\}$ (answer $\tfrac{1}{\sqrt\varepsilon}$), so the `expression` is new to the learner. The `longform` is the first of the brief's two options, with five 2-point rubric lines.

## Proposed course.json change

None.

## Backlog

No new bullets. The six level 1 limits are already under "Raised later (analysis level 1):" in `docs/BACKLOG-INBOX.md`, and this pass found no other engine limit.

## Conventions

No datasets or seeds. Money in £. $\mathbb{N} = \{1, 2, 3, \dots\}$; $\sup A$ and $\inf A$; the two-part supremum test written as in l2; exact arithmetic in code with `fractions.Fraction`. Earlier lessons are named by title in prose ("Whole numbers outrun everything", "Gaps in the rationals").

The main session saved this report from the agent's returned text, because the harness refuses report-file writes from subagents.
