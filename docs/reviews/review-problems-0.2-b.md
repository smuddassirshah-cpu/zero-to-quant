# Problem sets 0.2 (b): second-reader findings

Read at commit ee4f68a. A full second read of four sets. Pattern: `review-problems-0.2-a.md`.

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` = the question can be read two ways, does not give what the learner needs, or refuses a sensible entry in the stated form; `minor` = weak part, loose chain, loose `wrong` entry, wording, freshness or tooling.

## A. Second read: quadratics 1 to 3, equations 4

Scope: `app/content/courses/quadratics/problems-1.json` to `problems-3.json` and `app/content/courses/equations/problems-4.json`: 13 problems, 54 parts (38 quadratics, 16 equations; 34 numeric, 3 numeric sets, 15 expression, 2 choice). Equations sets 1 to 3 are not reported on.

Method. The two authors' scripts were run first. Every part was then solved from its text, by hand, and again in `problems-0.2-b-scripts/mine.py`: sympy for the exact value, then a second route (counting seats and cans, a grid, bisection, a brute-force search over whole numbers, the story's own arithmetic). Every `wrong` value was rebuilt from the slip its feedback line names and compared inside that entry's own band; every expression key, `accept` form and `wrong[].tex` was compared with my own expression, equations by `lhs - rhs`. Every part was then put through the engine's own graders in node (`grade-check.mjs`: `parseNum`, `within`, `matchWrong`, `numSetGrade`, `exprEqual`, and the widget's shape check for `expanded`, `factorised`, `factorised-fully`, `completed-square` and `simplified`, with the local Compute Engine): the answer, each `accept` form, each `wrong` entry on its own key, and 253 typed strings of my own (other orders, fractions for decimals, `\times`, a letter and `=` in front, the question retyped, a half-worked line, currency signs, thousands commas, roundings, set answers in words). The lessons, quizzes, review and homework of each level were read screen by screen (`skim.py`), and each setting and formula was searched across the three 0.2 courses and the exams (`fresh-grep.py`).

Tool results.

| check | result |
|---|---|
| authors' number scripts | quadratics 634 checks, 0 failures; equations (sets 1 to 4) 1142 checks, 0 failures |
| `mine.py` (reader's own answers and slips) | 54 parts, 499 checks, 0 failures |
| `grade-check.mjs` (engine graders) | 612 checks, 0 failures, 14 rows held to be faults (findings 3, 4, 5, 8, 9, 10) |
| `probe.mjs` (the engine on two proposed fixes and on a letter and `=` in front) | 13 rows, all as expected |
| `proposed.py` (numbers of the fixes below, freshness of the new numbers) | 45 checks, 0 failures |
| validator | 0 errors; 0 warnings on the four files |
| playthrough `--problems`, four sets, `--local-cdn` | green |
| the same with `--mobile` | green |
| voice scan 35, two course folders | 0 and 0 |
| `fresh-check.mjs --file`, gate | 0 hits on each set |
| `fresh-check.mjs --min-run 8 --min-share 0` | 1 hit: quadratics 2 `p-cliff-stone` against functions `problems-1` `p-stone-throw` (finding 7) |
| `fresh-grep.py` and the reader's own reading | three reuses the tool missed (findings 1, 2, 6) and notes under Freshness |

Result. No `answer`, `accept`, feedback line, `why` or explanation states a wrong value or a false rule. Every stated number agrees with mine. Every answer and `accept` form grades correct, and every one of the 130 `wrong` entries grades wrong and lands on its own key. No "factorise" part takes the unworked form: the expanded quadratic, a half-grouped line (`2x(x+4)+7(x+4)`), `(6x+2)^2-3^2`, `(6x+3)(6x-3)` and `9(4x^2-1)` are all refused with the form line. No "expand" part takes the brackets. Expression answers take either order of terms and of brackets, `\times`, `\left( \right)`, `(6x)^2-3^2` for the plate, $\tfrac{1}{5}$ for 0.2, `c=b-10` and `2b-2c=20` for the rowing equation, `y=x+8`, `36n+26n`, `3x+8y=2500`, `125=0.15x+0.4y` and $\tfrac{0.15x + 0.4y}{500} = 0.25$. Numeric fields take `£1,125`, `1,015`, `25/8`, a Unicode minus and "0 and 2", "t=0, t=7" for the sets. Four kinds of sensible entry are refused (findings 5, 8, 9, 10) and two kinds of unfinished line pass (findings 3, 4).

Claims checked beyond the keys: $x^2 + 11x + c$ is $(x + k)^2$ for no whole $k$; the pair 30 and $-6$ is the only one with product $-180$ and sum 24; the stone's height never passes 20 m; Jo's gap never falls below 1 m and is $(t - 3)^2 + 1$; 6.32 m/s falls short of the bus and 6.33 reaches it; the triangle rule counts the cans for every $n$ to 60; 801 lies between $28^2$ and $29^2$; the arch is at least 12.8 m high exactly on $4 \le x \le 16$; profit is $605 - 5(p - 19)^2$ and is at least £525 exactly on $15 \le p \le 23$; the water is highest at $x = 3$ (4.5 m, bank 1.5 m) and the gap is greatest at $x = 2.5$; 18 and 26 is the only whole-number tray pair; car A stays ahead after $t = 7$; 300 g and 200 g is the only mix, and every 25% mix has $y = \tfrac{2}{3}x$.

### Findings

Quadratics.

1. `minor` | `quadratics/problems-1.json` | `p-cinema-block` | parts 1 and 2, freshness.
   Part 1's product is printed in the level: `l2-product-and-sum` quiz item 4 asks for $k$ in $x^2 + kx + 24 = (x + 3)(x + p)$ and its explanation ends "Check: $(x + 3)(x + 8) = x^2 + 11x + 24$". `homework-1` item 1 is its mirror, $x^2 - 11x + 24$. Part 2 then lists the pairs of 18, the list of l2's third screen ($x^2 + 9x + 18$). The gate missed it (formulae, not word runs).
   Fix: new numbers, all in `proposed.py`. Prose "A cinema sets out a block of seats in rows. The block has $x + 4$ rows, with $x + 11$ seats in each row."
   - Part 1: answer and `accept` `x^2+15x+44`. `wrong`: `corner` `x^2+44` "That keeps only the square and the corner. The strips $11x$ and $4x$ are seats too, so add $15x$."; `added` `x^2+15x+15` "You added 4 and 11 for the corner. The corner is 4 rows of 11 seats, so it is $4 \times 11 = 44$."; `swapped` `x^2+44x+15` "The strips collect to $(4 + 11)x = 15x$ and the corner is $4 \times 11 = 44$. You swapped them." `correct` "Every term of one bracket meets every term of the other: $x^2 + 11x + 4x + 44 = x^2 + 15x + 44$." `generic` "Not quite. Multiply $(x + 4)(x + 11)$ term by term to get four pieces, then collect the two $x$ terms." `explain` "The block holds $(x + 4)(x + 11)$ seats. Its four pieces are $x^2$, $11x$, $4x$ and 44. The strips collect to $15x$, giving $x^2 + 15x + 44$."
   - Part 2: question "The cinema takes out 8 seats and sets the rest out as a new rectangle. Using part 1, it now has $x^2 + 15x + 36$ seats. Factorise $x^2 + 15x + 36$." Answer `(x+3)(x+12)`, `accept` both orders. `wrong`: `sum-thirteen` `(x+4)(x+9)` "4 and 9 multiply to 36 but add to 13. You need a sum of 15."; `square` `(x+6)^2` "6 and 6 multiply to 36 but add to 12. You need a sum of 15."; `signs` `(x-3)(x-12)` "$-3$ and $-12$ add to $-15$. The middle term is $+15x$, so both numbers are positive." `correct` "3 and 12 multiply to 36 and add to 15, so $x^2 + 15x + 36 = (x + 3)(x + 12)$." `generic` "Not quite. Find two numbers that multiply to 36 and add to 15." `explain` "The pairs that multiply to 36 are 1 and 36, 2 and 18, 3 and 12, 4 and 9, and 6 and 6. Only 3 and 12 add to 15. Check: $(x + 3)(x + 12) = x^2 + 15x + 36$."
   - Part 3: question "Take $x = 10$. Using $(x + 3)(x + 12)$, how many seats are in the new block? Give a whole number." Answer 286. `wrong`: `kept` 294 "294 is the old block, $14 \times 21$. Eight seats came out, so the new block has 286."; `sum-thirteen` 266 "That is $(x + 4)(x + 9)$ at $x = 10$. The new block is $(x + 3)(x + 12)$, which gives $13 \times 22 = 286$."; `square` 256 "That is $(x + 6)^2$ at $x = 10$. The new block is $(x + 3)(x + 12)$, which gives 286." `correct` "$(10 + 3)(10 + 12) = 13 \times 22 = 286$ seats." `explain` "The new block is 13 rows of 22 seats, and $13 \times 22 = 286$. Check with part 1: $100 + 150 + 44 = 294$, and $294 - 8 = 286$."
   - Part 4: question "Could the cinema take some seats out of $x^2 + 15x + 44$ and leave a square block, $(x + k)^2$ with $k$ a whole number, for every $x$?" Options: `no-middle` "No. $(x + k)^2 = x^2 + 2kx + k^2$, and $2k = 15$ has no whole-number $k$."; `six` (replaces `four`) "Yes. Take out 8 seats to leave $x^2 + 15x + 36$, which is $(x + 6)^2$." with `why` "$(x + 6)^2 = x^2 + 12x + 36$. Its middle term is $12x$, not $15x$."; `five` (replaces `three`) "Yes. Take out 19 seats to leave $x^2 + 15x + 25$, which is $(x + 5)^2$." with `why` "Squaring each term misses the strips: $(x + 5)^2 = x^2 + 10x + 25$."; `last-term` "No. The last term of a square must be a square number, and 44 is not." (`why` unchanged, with "$15x$"). `correct` "Taking out seats changes only the number term. The middle term stays $15x$, and a square has an even $2kx$." `generic` "... compare its middle term with $15x$." `explain` "Removing seats leaves $x^2 + 15x + c$ for some number $c$. A square $(x + k)^2$ has middle term $2kx$, so $k$ would have to be 7.5. No whole $k$ works, so no square block is possible."

2. `minor` | `quadratics/problems-1.json` | `p-allotment-plots` | part 1, freshness.
   Plot A, $x^2 + 9x + 20 = (x + 4)(x + 5)$, is the worked rectangle of `l1-two-brackets` screen 3 ("We write the area as $(x + 4)(x + 5)$", pieces $x^2$, $5x$, $4x$, 20). It is an area there and an area here. l2's fifth screen factorises $x^2 - 9x + 20$.
   Fix: new numbers, all in `proposed.py`; the 300, 110 and 190 of part 4 survive. Prose "Two allotment plots are rectangles, with lengths in metres. Plot A has area $x^2 + 11x + 30$ m² and plot B has area $2x^2 + 19x + 45$ m²."
   - Part 1: answer `(x+5)(x+6)`, `accept` both orders. `wrong`: `sum-thirteen` `(x+3)(x+10)` "3 and 10 multiply to 30 but add to 13. You need a sum of 11."; `sum-seventeen` `(x+2)(x+15)` "2 and 15 multiply to 30 but add to 17. You need a sum of 11." `correct` "5 and 6 multiply to 30 and add to 11, so $x^2 + 11x + 30 = (x + 5)(x + 6)$." `generic` "Not quite. Find two numbers that multiply to 30 and add to 11." `explain` "The pairs with product 30 are 1 and 30, 2 and 15, 3 and 10, and 5 and 6. Only 5 and 6 add to 11. So plot A is $x + 5$ by $x + 6$."
   - Part 2: question "Factorise the area of plot B, $2x^2 + 19x + 45$." Answer `(x+5)(2x+9)`, `accept` both orders. `wrong`: `no-group` `(x+9)(x+10)` "9 and 10 split the middle term, but they are not the brackets. Expand to check: $(x + 9)(x + 10) = x^2 + 19x + 90$."; `wrong-pair` `(2x+5)(x+9)` "Expand to check: $(2x + 5)(x + 9) = 2x^2 + 23x + 45$. The middle term should be $19x$." `correct` "Split $19x$ as $10x + 9x$: then $2x^2 + 10x + 9x + 45 = 2x(x + 5) + 9(x + 5) = (x + 5)(2x + 9)$." `generic` "Not quite. Find two numbers that multiply to $2 \times 45 = 90$ and add to 19, then split the middle term." `explain` "Here $ac = 2 \times 45 = 90$, and 9 and 10 multiply to 90 and add to 19. Grouping $2x^2 + 10x$ and $9x + 45$ gives $2x(x + 5) + 9(x + 5)$. The shared bracket comes out: $(x + 5)(2x + 9)$."
   - Part 3: question "The plots share their side of length $x + 5$ and are joined into one rectangle. Using $(x + 5)(x + 6)$ and $(x + 5)(2x + 9)$, write the total area fully factorised." Answer `3(x+5)^2`, `accept` `3(x+5)^2`, `3(x+5)(x+5)`. `wrong`: `both-sides` `6(x+5)^2` (line: "... The joined rectangle is still $x + 5$ on that side."); `lost-square` `3(x+5)` "$3(x + 5)$ is the long side alone. Multiply it by the shared side, $x + 5$." `correct` "The other sides add: $(x + 6) + (2x + 9) = 3x + 15 = 3(x + 5)$. So the total is $(x + 5) \times 3(x + 5) = 3(x + 5)^2$." `generic` "Not quite. Keep the shared side $x + 5$, add the other two sides, then look for a common factor." `form` "That is equal, but a bracket still has a common factor: $3x + 15 = 3(x + 5)$." `explain` "Joined along $x + 5$, the rectangle is $x + 5$ by $(x + 6) + (2x + 9) = 3x + 15$. Taking out 3 gives $3(x + 5)$. So the area is $3(x + 5)^2$."
   - Part 4: question "Take $x = 5$. Using $3(x + 5)^2$, what is the total area in m²? Give a whole number." Answer 300, `wrong` values 900 and 600 unchanged; in `both-sides` read "$6(x + 5)^2$" and "$3(x + 5)^2$". `correct` "$x + 5 = 10$, so the area is $3 \times 10^2 = 300$ m²." `explain` "With $x = 5$ the bracket is 10, and $3 \times 10^2 = 300$. Check: plot A is $10 \times 11 = 110$ and plot B is $10 \times 19 = 190$. Together they make $110 + 190 = 300$ m²."

3. `minor` | `quadratics/problems-1.json` | `p-cinema-block` part 1, `p-steel-plates` part 3 | "expanded and simplified".
   Both ask for the expansion "expanded and simplified" and carry `form: "expanded"`, which checks only that no bracket is left. `x^2+8x+3x+24`, `36x^2+24x+4-9` and `36x^2+12x+12x+4-9` grade correct (`grade-check.mjs`). `form: "simplified"` does not help: it refuses the uncollected line but passes `(x+3)(x+8)` (`probe.mjs`).
   Fix: none in content that closes it; see Engine. A learner who collects is graded rightly, and the next part restates the collected form.

4. `minor` | `quadratics/problems-1.json` | `p-allotment-plots` | part 3.
   `(x+4)(x+5+2x+7)` grades correct as "fully factorised" (`grade-check.mjs`). It is the first line of the working: the second bracket is $3x + 12$ uncollected and still holds the factor 3. `(x+4)(3x+12)` is refused with the right line.
   Fix: none in content; see Engine. The same holds after finding 2 for `(x+5)(x+6+2x+9)`.

5. `unclear` | `quadratics/problems-2.json` | `p-bus-chase` | part 4.
   "What is the slowest speed at which Jo just reaches the bus? Give your answer in m/s to 2 decimal places." The key is $\sqrt{40} = 6.32456$ with band 0.005. At 6.32 m/s Jo does not reach the bus ($6.32^2 = 39.94 < 40$), so a careful learner rounds up to 6.33. 6.33 is refused with the generic line (`grade-check.mjs`).
   Fix: `"tol": { "abs": 0.006 }` (takes 6.32, 6.325 and 6.33; refuses 6.3, 6.31, 6.34 and both `wrong` values; `proposed.py`). Question "Back to Jo, 10 m behind the stop. Running at $v$ m/s, the gap is $t^2 - vt + 10$. What is the slowest speed at which Jo just reaches the bus? The exact answer is a square root. Give it in m/s to 2 decimal places."

6. `minor` | `quadratics/problems-2.json` | `p-bus-chase` | part 3, freshness.
   Sam's equation $t^2 - 6t + 7 = 0$ is `l7-the-formula` quiz item 4, "Solve $x^2 - 6x + 7 = 0$ with the formula", with the same roots $3 \pm \sqrt{2}$ and the same $\sqrt{8} = 2\sqrt{2}$ step that the `half-root` line and the explanation use.
   Fix: Sam starts 6 m behind (`proposed.py`; $t^2 - 6t + 6$ is in no 0.2 file). Question "Sam starts 6 m behind the stop and also runs at 6 m/s, so the gap is $t^2 - 6t + 6$. That is $(t - 3)^2 - 3$, 4 m less than Jo's. When does Sam first reach the bus? Give your answer in seconds to 2 decimal places." Answer 1.26795, `accept` "1.27", band 0.005. `wrong`: `larger` 4.73205 "$3 + \sqrt{3}$ is the later meeting. Sam reaches the bus first at $3 - \sqrt{3}$, about 1.27 s."; `half-root` $-0.46410$ "With the formula the whole top goes over 2: $\tfrac{6 \pm \sqrt{12}}{2} = 3 \pm \sqrt{3}$."; `no-root` 0 with band 0.001 "$(t - 3)^2 = 3$ gives $t - 3 = \pm\sqrt{3}$, not $\pm 3$." `correct` "$(t - 3)^2 = 3$ gives $t = 3 \pm \sqrt{3}$. The first time is $3 - \sqrt{3} \approx 3 - 1.732 = 1.268$, which is 1.27 s." `generic` "Not quite. Set $(t - 3)^2 - 3 = 0$ and square-root with $\pm$. Take the earlier time." `explain` "Setting $(t - 3)^2 - 3 = 0$ gives $t = 3 \pm \sqrt{3}$. The formula agrees: $t = \tfrac{6 \pm \sqrt{36 - 24}}{2} = 3 \pm \sqrt{3}$. The earlier time is $3 - \sqrt{3} \approx 1.27$ s." The author's script needs the same numbers.

7. `minor` | `quadratics/problems-2.json` | `p-cliff-stone` | setting, freshness across courses.
   "A stone is thrown upwards from the top of a cliff" opens functions `problems-1` `p-stone-throw` word for word (11 tokens; that one is $45 - 5(t - 2)^2$ above a beach). The two sets sit in the same topic and a learner meets both. Numbers and questions differ, so only the story repeats.
   Fix: prose "A flare is fired upwards from the deck of a ship, 15 m above the sea. After $t$ seconds its height above the sea is $h = 15 + 10t - 5t^2$ metres." Then in the item replace "stone" with "flare" (part 1 "the flare's greatest height", part 2 "does the flare hit the sea", part 3 "The flare also passes deck level.", part 4, and the lines of parts 2 and 4), "the throw" with "the launch" (four lines) and "The stone lands" with "The flare lands". Keep the id. "flare", "deck" and "ship" are in no 0.2 file (`proposed.py`).

8. `unclear` | `quadratics/problems-3.json` | `p-canal-arch` | part 3.
   The prose writes the arch as "$y = -0.2x(x - 20)$", so a learner types `y=-0.2(x-10)^2+20`. It is refused, with the line "That is equal, but write it as a number times a squared bracket, plus a number", which is what they wrote (`grade-check.mjs`). The shape check reads the `y=` as part of the expression. `probe.mjs` shows the same for `expanded`, `factorised` and `factorised-fully` (`A=(x+4)(x+5)` is refused); only `simplified` takes a letter and `=` in front. This is the one part of the four sets whose prose writes the letter.
   Fix: question "Using the vertex $(10, 20)$, write the arch's height in completed square form, $a(x - h)^2 + k$. Type only the expression, with no $y =$ in front." And see Engine.

9. `unclear` | `quadratics/problems-3.json` | `p-sprinkler-bank` | part 1.
   "As simply as possible" with `form: "simplified"`. The collected answer written with halves over 2 is refused: `\frac{5x}{2}-\frac{x^2}{2}`, `2.5x-\frac{x^2}{2}` and `-\frac{x^2}{2}+\frac{5x}{2}` get "That is equal, but collect the $x$ terms into one", which they have done. Yet $\tfrac{5}{2}x - \tfrac{1}{2}x^2$, `0.5x(5-x)`, `x(2.5-0.5x)` and $\tfrac{5x - x^2}{2}$ pass (`grade-check.mjs`). The size test, not the learner, is at fault.
   Fix: question "Write the height of the water above the bank, $(3x - 0.5x^2) - 0.5x$, as simply as possible. Keep the decimals, as in $1.5x$." `form` line "That is equal, but collect the $x$ terms into one and keep the decimals, as in $1.5x$." And see Engine.

Equations.

10. `unclear` | `equations/problems-4.json` | `p-salt-solutions` | part 1.
    "The weights give $x + y = 500$. Write a second equation, for the grams of salt." The salt balance a learner writes first is $0.15x + 0.4y = 0.25(x + y)$. It is true and, with $x + y = 500$, gives the same answer, but it is not the key's line, so it is refused with the generic line (`grade-check.mjs`; so are `15x+40y=25(x+y)` and $\tfrac{0.15x + 0.4y}{x + y} = 0.25$). Also refused: `0.15x+0.4y=0.25(500)`, where the engine does not read a number in brackets after a decimal as a product (`0.25\times500` and `(0.25)(500)` pass).
    Fix: question "The weights give $x + y = 500$. Write a second equation for the grams of salt: the salt from the two solutions on the left, and the grams of salt in the 500 g batch, as one number, on the right." Add to `wrong` `{ "id": "both-letters", "tex": "0.15x+0.4y=0.25(x+y)" }` and to `byKey` `"both-letters": "True, but use the weight you know: $x + y = 500$, so the right-hand side is $0.25 \times 500 = 125$."` (`probe.mjs`: that entry catches the first two forms and leaves the key and `per-cent` alone.)

11. `minor` | `equations/problems-4.json` | `p-remote-cars` | chain.
    The item is two halves: parts 1 and 2 (level at $t = 7$, 49 m), then parts 3 and 4 (the post at 81 m, the 18 m gap). Part 3 uses nothing from part 2, and the 49 m is met again only as the `meeting` slip of part 4.
    Fix: part 3 question "Part 2 put the cars level 49 m from the start line. A marker post stands 32 m further on, 81 m from the start line. Swap $d = 81$ into $d = t^2$. At what time does car A pass the post? Give the time in seconds." Part 4 question "Using $t = 9$ from part 3, car A is at the post, 81 m from the start. How far behind car A is car B at that moment? Give the distance in metres." Answers, `wrong` and feedback unchanged.

### Per problem

- Chains. Beyond finding 11, four parts give a value that no later part uses: `p-cinema-block` part 3 (228; part 4 goes back to part 1), `p-steel-plates` part 2 (the first plate's factors, met again only as the `old` slip of part 5), `p-cliff-stone` part 3 (0 and 2, a second route beside the square form) and `p-bike-hire` part 3 (£1,125). Each is a use of the rule on the way to the result. They stand. `p-allotment-plots`, `p-bus-chase`, `p-can-stack`, `p-canal-arch`, `p-sprinkler-bank`, `p-rowing-current`, `p-seedling-trays` and `p-salt-solutions` are full chains.
- Later parts restate what they need: yes, every one. `p-remote-cars` part 4 leans on the 81 m of part 3's question (finding 11 restates it).
- Answer form. Every numeric part with a non-whole answer names its form (2 decimal places, "as a decimal", "separated by a comma"). Twenty-two parts with a whole answer and `tol` 0 give the unit only ("in metres", "in pounds", "how many rows"). None refuses a sensible entry; findings 1 and 2 add "Give a whole number" where they rewrite.
- Tolerances. Each band takes the value its feedback prints: 0.37 and 1.63, 1.59 and 1.586, 6.32, 13.65 and 13.651, 3.125 and 3.13. Truncations (1.58, 0.36) and one-place roundings (6.3, 13.7, 3.1) are refused, as the form sentence asks. One band is too tight for the question asked (finding 5). No `wrong` value sits in an answer band or in another entry's band; the widest `wrong` band is 0.02.
- `wrong` entries: 130 (90 numeric, 4 set, 36 `wrong[].tex`), all rebuilt in `mine.py`; each is the value its named slip gives and each grades to its own key. Carried slips are present where a learner would carry one (`carried` in `p-cliff-stone` 2, `p-can-stack` 3, `p-rowing-current` 3, `p-seedling-trays` 3, `p-salt-solutions` 3, `p-remote-cars` 4; `sum-nine`, `both-sides`, `each-term`, `signs` carried into the evaluation parts). The 21 and 9 `byKey` lines the authors' scripts list "by hand" were read: all true.
- Natural slips that reach the key: none found. Retyping the question: refused on every expression part (`(x+3)(x+8)`, `x^2+11x+18`, `36x^2-9`, `(6x+2)^2-9`, `-0.2x(x-20)`, `(3x-0.5x^2)-0.5x`, `b+c=14`, `x+y=500`).
- The two choice parts are judgements (can a square be left, which side of the roots). Every `why` is true; no option or line names an option by place; no key stands out by length.
- Explanations: all true, none over three sentences, no false general rule. "801 is not a square number, so the roots are not whole numbers" and "a square has an even $2kx$" (for whole $k$) are right as stated.

Clean problems (5 of 13): quadratics set 1 `p-steel-plates` (bar the engine row of finding 3); set 2 `p-can-stack`; set 3 `p-bike-hire`; equations set 4 `p-rowing-current`, `p-seedling-trays`. `p-cliff-stone` is clean in its mathematics (finding 7 is the story only).

### Per set

- Lessons. Every lesson of each level is drawn on, and each problem draws on at least two. Quadratics 1: l1 (cinema 1, plate 3), l2 (cinema 2, plots 1), l3 (plots 2 and 3, plate 4), l4 (plate 2 and the last line of plate 4). Quadratics 2: l5 (stone 3, cans 1), l6 (stone 1, 2 and 4, bus 2 and 3), l7 (cans 3, bus 3's check), l8 (bus 1 and 4, cans 2). Quadratics 3: l9 (opening downwards and the mirror line: arch 1 and 3), l10 (arch 2 and 3, sprinkler 4), l11 (arch 1, bike 2 and 4, sprinkler 2), l12 (arch 4, bike 5, the line and the curve in sprinkler), l13 (bike). Equations 4: l14 (rowing 2, salt 2), l15 (trays 2, cars 1 and 3), l16 (cars 2), l17 (rowing 1, trays 1 and 3, salt 1). l16 is the thinnest: one part reads a crossing as a solution, and no part meets parallel lines or one line written twice.
- Taught by the end of the level: yes. Taking out a common factor before the difference of two squares is l4's sixth screen; a perfect square's middle term is l1's trap and `homework-1` item 6; completing the square with a number in front is l7's fourth screen and `homework-2` item 3 (and `p-cliff-stone` 1 gives the form); a letter in the discriminant is l8's sixth screen and `review-2` item 8; a downward inequality is l12's generalise screen; scaling an equation by a decimal before subtracting is l14's sixth screen; ratio comes from the `ratio` course of topic 0.1.
- Reading load. Settings are everyday (seats, plots, a plate, a stone, a bus, cans, an arch, bikes, a sprinkler, a boat, trays, toy cars) with one laboratory one (salt solutions). The longest question is 53 words in six short sentences (`p-salt-solutions` 4); `p-bus-chase` 3 is 48. `p-canal-arch` asks for a barge 12.8 m tall under an arch 20 m high, which no canal has; the numbers are clean, so it stands.
- Difficulty. One 5 in each set (`p-steel-plates`, `p-bus-chase`, `p-bike-hire`, `p-salt-solutions`), all earned. Typed parts 52 of 54.
- Freshness. Gate clean. Beyond findings 1, 2, 6 and 7:
  - `p-steel-plates` is l4's picture (a square of side $2x$ with a 3 by 3 square cut out, $4x^2 - 9$) with $6x$ for $2x$ and the hole moved to the middle. The common factor and the wider plate are new, so it stands.
  - `p-bike-hire` parts 1 to 4 follow l13's fourth and seventh screens step for step (zero revenue at two prices, halfway, then a unit cost and the "add the whole cost" trap), with new numbers; `review-3` item 10 and l13 quiz item 3 are the same shape. Part 5 is new. It stands as the level's capstone, but it is the fourth of its kind.
  - `p-remote-cars` part 1 is the fifth "line through the origin meets $y = x^2$" ($2x$ and $3x$ in l15, $5x$ in `review-4`, $6x$ and $2x^2$ in `homework-4`), and its story (one mover speeding up from rest, one steady, when are they level) is that of functions `problems-3` `p-sledge-cyclist`.
  - `p-canal-arch` and `p-sprinkler-bank` share the water-jet parabola with functions `problems-4` `p-fountain-jet` ($0.15x(12 - x)$); the questions differ.
  - `p-rowing-current` parts 2 and 3 are the shape of l14 quiz item 1 ($x + y = 12$, $x - y = 2$), with other numbers.
- Voice. British spelling, no exclamation marks, no em-dashes, £ for money, explanations of at most three sentences (`voice-scan.py 35`: 0 and 0).

### Engine

- `form: "expanded"` checks only that no bracket is left, so a part that asks for "expanded and simplified" passes a line with like terms not collected (finding 3). `form` takes one value; either let it take a list (`["expanded", "simplified"]`) or make `expanded` also require collected like terms.
- `form: "factorised-fully"` passes a bracket whose like terms are not collected, `(x+4)(x+5+2x+7)` (finding 4). Collect each bracket before the common-factor test.
- The shape checks `completed-square`, `expanded`, `factorised` and `factorised-fully` read a leading `y =` as part of the expression and fail it, where the equality test drops it and `simplified` passes it (finding 8, `probe.mjs`). Strip the same lone letter and `=` before the shape check.
- `form: "simplified"` compares tree sizes, so it refuses $\tfrac{5x}{2} - \tfrac{x^2}{2}$ and passes $\tfrac{5}{2}x - \tfrac{1}{2}x^2$ and the factorised `0.5x(5-x)` (finding 9). A term-count test for polynomials (no two like terms, no bracket holding a sum unless the key has one) would grade what the learner did.
- A decimal followed by a number in brackets, `0.25(500)`, is not read as a product, where `0.25\times500` and `(0.25)(500)` are (finding 10).

These five are appended to `docs/BACKLOG-INBOX.md` under "Raised later (review problems 0.2 b)".

### Counts

| tag | quadratics | equations | total |
|---|---|---|---|
| `wrong` | 0 | 0 | 0 |
| `unclear` | 3 | 1 | 4 |
| `minor` | 6 | 1 | 7 |

### Verdict by set

| set | verdict |
|---|---|
| quadratics `problems-1` | sound; findings 1, 2 (new numbers), 3 and 4 (engine) |
| quadratics `problems-2` | sound; findings 5, 6 (new numbers), 7 (story) |
| quadratics `problems-3` | sound; findings 8, 9 |
| equations `problems-4` | sound; findings 10, 11 |

One fix pass on Sonnet covers all of it. Findings 1, 2 and 6 change graded answers (`p-cinema-block` throughout, `p-allotment-plots` parts 1 to 3, `p-bus-chase` part 3), so the quadratics author's script needs the same numbers and a delta reader should recompute those three items. The rest change text, one band and one `wrong` entry.

### Scripts (`docs/reviews/problems-0.2-b-scripts/`)

| file | what it does | run |
|---|---|---|
| `mine.py` | the reader's own answer and named-slip value for every numeric, set and expression part, two methods each, and the claims above | `<venv>/bin/python`, exit 0 |
| `grade-check.mjs`, `typed.mjs` | the engine's graders and the widget's shape check on every answer, `accept`, `wrong` and 253 typed strings (`--show` lists each) | `node ... --local-cdn <pkgs>`, exit 0, 14 FINDING rows |
| `probe.mjs` | the engine on `form: "simplified"` for finding 3, on a letter and `=` in front of each shape for finding 8, and on the `wrong` entry of finding 10 | `node ... --local-cdn <pkgs>`, exit 0 |
| `proposed.py` | the numbers of the fixes above, twice, and a grep for the new expressions and words in the three 0.2 courses and the Stage 0 exams | `<venv>/bin/python`, exit 0 |
| `fresh-grep.py` | each setting's nouns and formulae across the three 0.2 courses and the exams (`--wide` for every course) | `python3` |
| `skim.py` | one line per screen or item of a lesson file | `python3` |
| `dump.py` | compact dump of a set for reading | `python3` |

All run from the repo root.

## Fix pass

Applied with targeted edits to the four content files and the two authors' scripts (`docs/reports/problems-quadratics-numbers.py` 646 checks, `docs/reports/problems-equations-numbers.py` 1154 checks, both exit 0). Every new number was recomputed by two routes (sympy exact, then counting seats or plots, a search over whole numbers, the formula, or the value put back) inside those scripts, and each new check is tightened to the new value so a revert fails.

1. `p-cinema-block`: fixed. New numbers $(x+4)(x+11) = x^2+15x+44$, 8 seats out, $x^2+15x+36 = (x+3)(x+12)$ (only 3 and 12 sum to 15; found by search), 286 at $x=10$ ($13 \times 22$; $294 - 8$; counted by rows), part 4 keeps "no" with $2k = 15$, $k = 7.5$. All feedback, `wrong` and explanations rewritten as in the review; the choice options `four`/`three` are now `six`/`five`.
2. `p-allotment-plots`: fixed. Plots $x^2+11x+30 = (x+5)(x+6)$ and $2x^2+19x+45 = (x+5)(2x+9)$ ($ac = 90$, 9 and 10; grouping expanded back), joined $3(x+5)^2$ ($3x + 15$), 300 at $x=5$ ($110 + 190$). `wrong` values 900 and 600 unchanged.
3. `p-cinema-block` 1 and `p-steel-plates` 3, "expanded and simplified": deferred, engine only (inbox).
4. `p-allotment-plots` 3, `(x+5)(x+6+2x+9)` passing: deferred, engine only (inbox).
5. `p-bus-chase` 4: fixed. `tol` 0.006 and the question says the exact answer is a square root. Script proves $6.32^2 = 39.94 < 40 < 40.07 = 6.33^2$, band takes 6.32, 6.325, 6.33 and refuses 6.3, 6.31, 6.34 and both `wrong` values (3.16228, 40).
6. `p-bus-chase` 3: fixed. Sam starts 6 m behind: $t^2 - 6t + 6 = (t-3)^2 - 3$, roots $3 \pm \sqrt{3}$ = 1.26795 and 4.73205 (formula route $\frac{6 \pm \sqrt{12}}{2}$ and a fine grid agree), answer band 0.005 with accept "1.27". `wrong`: `larger` 4.73205, `half-root` $3 - \sqrt{12} = -0.4641$, `no-root` 0 (band 0.001).
7. `p-cliff-stone`: fixed, story only. Now a flare fired from a ship's deck (id kept, numbers unchanged). "flare", "deck", "ship" appear in no other 0.2 file; `fresh-check` gate and `--min-run 8 --min-share 0` both 0 hits on set 2.
8. `p-canal-arch` 3: fixed in the question ("Type only the expression, with no $y =$ in front"). Engine row stays in the inbox. Proved with the engine graders (`probe2.mjs`, scratchpad): `-0.2(x-10)^2+20`, `20-0.2(x-10)^2` and `-\frac{1}{5}(x-10)^2+20` are accepted; the unworked `-0.2x(x-20)` and `-0.2x^2+4x` are refused with the form line; `sign-h` still lands on its own key.
9. `p-sprinkler-bank` 1: fixed in the question and the `form` line ("keep the decimals, as in $1.5x$"). Engine row stays in the inbox. Proved: `2.5x-0.5x^2`, `-0.5x^2+2.5x` and `\frac{5}{2}x-\frac{1}{2}x^2` accepted; `(3x-0.5x^2)-0.5x` and `3x-0.5x-0.5x^2` refused with the form line; `added` lands on its key. The `\frac{5x}{2}` typings are still refused (the engine's size test), now with a line that tells the learner to keep the decimals.
10. `p-salt-solutions` 1: fixed. The engine cannot accept $0.15x + 0.4y = 0.25(x+y)$ as the key (the polynomials differ; only the system with $x+y=500$ agrees), so the question now asks for the right-hand side as one number, the true both-letters line has a `wrong` entry `both-letters` with its own line, and `0.15x+0.4y=0.25(500)` is added to `accept` (the engine's text match takes it). Proved with the engine graders: `0.15x+0.4y=125`, `3x+8y=2500`, `0.25\times500` and `0.25(500)` accepted; `0.15x+0.4y=0.25(x+y)` and `15x+40y=25(x+y)` refused on `both-letters`; the unworked `x+y=500` refused; `per-cent`, `strength`, `swapped` still land on their keys. Script checks that the both-letters balance with $x+y=500$ gives 300 and 200.
11. `p-remote-cars`: fixed. Part 3 now starts from part 2's 49 m ("A marker post stands 32 m further on, 81 m from the start line", $49 + 32 = 81$) and part 4 restates 81 m. Answers, `wrong` and feedback unchanged.

Gates: validator 0 errors (no new warning on the four files after splitting two long sentences); `fresh-check` 0 hits on each of the four sets; playthrough `--problems` green for the four sets, with and without `--mobile`; voice scan 35 on both course folders 0 and 0. Not edited: engine files, `course.json`, lesson ids, equations sets 1 to 3. `proposed.py` now reports "failures" only because its freshness greps find the new words and expressions in the files it was written to protect; those are the applied fixes.

### Changed graded values for the delta reader

`quadratics/problems-1.json`, `p-cinema-block` (all four parts; whole item recomputed):
- part 1 answer `x^2+11x+24` to `x^2+15x+44`; accept the same; `wrong` `x^2+24` to `x^2+44`, `x^2+11x+11` to `x^2+15x+15`, `x^2+24x+11` to `x^2+44x+15`.
- part 2 answer `(x+2)(x+9)` to `(x+3)(x+12)` (both orders); `wrong` `sum-nine (x+3)(x+6)` to `sum-thirteen (x+4)(x+9)`, `one-eighteen (x+1)(x+18)` to `square (x+6)^2`, `signs (x-2)(x-9)` to `(x-3)(x-12)`.
- part 3 answer 228 to 286 (accept "286", tol 0); `wrong` `kept` 234 to 294, `sum-nine` 208 to `sum-thirteen` 266, `one-eighteen` 308 to `square` 256.
- part 4 key unchanged (`no-middle`, text now "$2k = 15$"); distractors `four` ("8 seats out, $(x+4)^2$") to `six` ("8 seats out, $(x+6)^2$", $x^2+15x+36$), `three` ("15 seats out, $(x+3)^2$") to `five` ("19 seats out, $(x+5)^2$", $x^2+15x+25$).

`quadratics/problems-1.json`, `p-allotment-plots`:
- part 1 answer `(x+4)(x+5)` to `(x+5)(x+6)`; `wrong` `sum-twelve (x+2)(x+10)` to `sum-thirteen (x+3)(x+10)`, `sum-21 (x+1)(x+20)` to `sum-seventeen (x+2)(x+15)`.
- part 2 answer `(x+4)(2x+7)` to `(x+5)(2x+9)`; `wrong` `no-group (x+7)(x+8)` to `(x+9)(x+10)`, `wrong-pair (2x+4)(x+7)` to `(2x+5)(x+9)`.
- part 3 answer `3(x+4)^2` to `3(x+5)^2` (accept also `3(x+5)(x+5)`); `wrong` `6(x+4)^2` to `6(x+5)^2`, `3(x+4)` to `3(x+5)`.
- part 4 answer 300 unchanged (now at $x = 5$, was $x = 6$); `wrong` 900 and 600 unchanged.

`quadratics/problems-2.json`:
- `p-bus-chase` part 3 answer 1.58579 to 1.26795; accept "1.59" to "1.27"; `wrong` `larger` 4.41421 to 4.73205, `half-root` 0.17157 to $-0.4641$, `no-root` 1 to 0 (tol 0.001).
- `p-bus-chase` part 4 band `abs` 0.005 to 0.006 (answer 6.32456 and `wrong` unchanged).
- `p-cliff-stone`: no value changed (story only).

`equations/problems-4.json`:
- `p-salt-solutions` part 1: new `wrong` entry `both-letters` `0.15x+0.4y=0.25(x+y)` with its `byKey` line; new `accept` `0.15x+0.4y=0.25(500)`; answer unchanged.
- `p-remote-cars` parts 3 and 4: question text only.

`quadratics/problems-3.json`: `p-canal-arch` part 3 and `p-sprinkler-bank` part 1: question text (and the sprinkler `form` line) only; keys, `accept` and `wrong` unchanged.
