# Problem sets 0.2 (a): second-reader findings

Read at commit d657617. A full second read of six sets. Pattern: `review-problems-1.3-c.md`.

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` = the question can be read two ways, does not give what the learner needs, or refuses a sensible entry in the stated form; `minor` = weak part, loose chain, loose `wrong` entry, wording, freshness or tooling.

## A. Second read: equations 1 to 3, functions 1 to 3

Scope: `app/content/courses/equations/problems-1.json` to `problems-3.json` and `app/content/courses/functions/problems-1.json` to `problems-3.json`: 24 problems, 103 parts (49 equations, 54 functions; 64 numeric, 26 expression, 13 choice). Seven of the numeric parts are two-value sets (`answers`, `unordered`).

Method. The two authors' scripts were run first. Every part was then solved from its text, by hand, and again in `problems-0.2-a-scripts/mine.py`: sympy for the exact value, then a second route (the story's own arithmetic, a brute-force count over whole numbers, a grid, bisection, the foot of a perpendicular by projection). Every `wrong` value was rebuilt from the slip its feedback line names and compared inside that entry's own band; every expression key, `accept` form and `wrong[].tex` was compared with my own expression, equations and inequalities by their solution sets. Every part was then put through the engine's own graders in node (`grade-check.mjs`: `parseNum`, `within`, `matchWrong`, `numSetGrade`, `exprEqual`, and the widget's shape check for `simplified`, `expanded` and `factorised-fully`, with the local Compute Engine): the answer, each `accept` form, each `wrong` entry on its own key, and 285 typed strings of my own (other orders, fractions for decimals, `\times`, a letter and `=` in front, sides swapped, a cleared or half-solved equation, currency signs, thousands commas, roundings, set answers in words). The lessons, quiz, review and homework of each level were read screen by screen (`skim.py`), and each idea a set leans on was counted per lesson (`taught.py`) and the passages read (`peek.py`).

Tool results.

| check | result |
|---|---|
| authors' number scripts | equations 801 checks, 0 failures; functions 774 checks, 0 failures |
| `mine.py` (reader's own answers and slips) | 103 parts, 1071 checks, 0 failures |
| `grade-check.mjs` (engine graders) | 888 checks, 0 failures, 7 rows held to be faults (findings 1 and 3), 1 wide `wrong` band (finding 19) |
| `proposed.py` (numbers of the fixes below, freshness of the new numbers) | 34 checks, 0 failures |
| validator | 0 errors; 0 warnings on the six files |
| playthrough `--problems`, six sets, `--local-cdn` | green |
| the same with `--mobile` | green |
| voice scan 35, two course folders | 0 and 0 |
| `fresh-check.mjs --file`, gate | 0 hits on each set |
| `fresh-check.mjs --min-run 8 --min-share 0` | 11 hits, all instruction sentences ("Type only what comes after the $=$ sign", "The letter $a$ appears twice") |
| `fresh-grep.py` and the reader's own reading | four reuses the tool missed (findings 10, 13, 14 and a note under Freshness) |
| `forms.py` (shape, skills, form sentences, restated values) | every item skill is a skill of its level; no explanation over three sentences; rows judged below |

Result. No `answer`, `accept`, feedback line or `why` states a wrong value of the quantity asked. Every stated number agrees with mine. One explanation states a false general rule (finding 8). Every answer and `accept` form grades correct, and every `wrong` entry grades wrong and lands on its own key, so no `byKey` line is dead. Expression answers take the forms a Stage 0 learner would type: either order of terms, `\times`, `4.20n`, $\tfrac{21}{5}n$, `c = a - 5`, `E(x) = 1.15x - 3`, `y = 0.5x + 2`, `C = ...` on either side, an equation with its sides swapped or already cleared of fractions, `>=` and `≥` for `\ge`, $t < \tfrac{15}{2}$, $t < 7\tfrac12$, $\tfrac{5}{9}(F - 32)$ for $\tfrac{F - 32}{1.8}$, $\tfrac{b}{1/w - 1}$ for $\tfrac{wb}{1 - w}$. The one form refused is a number typed with its thousands comma inside an expression (finding 1). Numeric fields take `£75`, `€342`, `4,800`, `7 1/2`, `-5/2` and a Unicode minus; set answers take "0 and 60", "t = 1, t = 3", "1 or 3" and "2 ± 1".

Claims checked beyond the keys: Leo's trick equals Mia's for every $n$; Tariff B is cheaper for every use below 7.5 units and A above; the cottage equation has one solution; $a = \tfrac{wb}{1 - w}$ rises with $w$, so the least holding sits at the least $w$; every pair of the sapling's four rows gives 5 cm a week; the kiosk rule fits all three rows; the stone reaches 45 once and 40 twice; the pipe's foot is $(2, 3)$ by projection and lies between A and B; Gym B is cheaper for every month after 5; N and M cross once on $t \ge 0$, at 3.319; the sledge's speed at $t = 6$ is 6 m/s and the cyclist leads throughout $0 < t < 6$; the cubic rises on $0 < x < 1$, falls on $1 < x < 3$, rises on $3 < x < 4$ and meets $y = 4$ only at 1 and 4.

### Findings

Equations.

1. `unclear` | `equations/problems-2.json` | `p-interest-split` | parts 1 and 2.
   The prose prints "£12,000". A learner who types `12,000-s` is refused with the generic line "The two amounts add up to £12,000", and `0.04s+0.065(12,000-s)=660` is refused in part 2 (`grade-check.mjs`). A numeric field takes `4,800`; an expression field does not take the comma.
   Fix: part 1 question "Write the amount in the bond fund, in pounds, in terms of $s$. Type 12000 with no comma." Part 2 question "Using $12000 - s$ in bonds, write an equation for the year's interest. Use 0.04 for 4% and 0.065 for 6.5%, and type 12000 with no comma."

2. `unclear` | `equations/problems-2.json` | `p-interest-split` | part 3.
   "Multiply every term by 1000 to clear the decimals, then solve." The equation is not restated, so a learner who missed part 2 has nothing to multiply. Every other later part in the six sets carries what it needs.
   Fix: question "Multiply every term of $0.04s + 0.065(12000 - s) = 660$ by 1000 to clear the decimals, then solve. How much went into savings, in pounds? Give a whole number."

3. `minor` | `equations/problems-3.json` | `p-bakery-stock` part 2, `p-fridge-temperature` part 3, `p-van-value` part 3 | "Solve" parts.
   Each asks for a solved inequality and grades correct when the learner retypes the question: `240-18h\ge60`, `\frac{F-32}{1.8}\le5`, `24000-2400t>6000`. An unfinished line (`-18h\ge-180`, `F-32\le9`) passes too. The grader compares solution sets, and no `form` asks for the letter alone. The same test makes `c=21` pass for "write an equation for the cost" in `equations/problems-2.json` `p-climbing-wall` part 1, which is harmless there.
   Fix: none in content that closes it; see Engine. Until then the three parts stand: a learner who solves is graded rightly.

4. `minor` | `equations/problems-2.json` | `p-climbing-wall` | part 4.
   "What is the highest price per climber, in whole pence, that keeps the cost within £300? Give your answer in pounds." Two units in one question. `728` gets only the generic line.
   Fix: question as in finding 5. Add to `wrong` `{ "id": "pence", "value": 728, "tol": { "abs": 0 } }` and to `byKey` `"pence": "That is the price in pence. In pounds it is £7.28."`

5. `minor` | `equations/problems-2.json` | `p-climbing-wall` | chain.
   Part 2's 21 and part 3's 31 feed nothing: parts 2, 3 and 4 are three separate uses of $45 + 8c$. The report calls part 3 "the same rule with a budget".
   Fix: part 3 question "Part 2 found that £213 pays for 21 climbers. Next month the group has a budget of £300. Using $45 + 8c$ for the cost, what is the largest number of climbers it can bring? Give a whole number." Part 4 question "Part 3 found that £300 covers at most 31 climbers at £8 each. The group wants to bring 35 for £300, so it asks for a lower price. The booking stays at £45, and prices are in whole pence. What is the highest price per climber that keeps the cost within £300? Give your answer in pounds, such as 6.45." Answers unchanged.

6. `minor` | `equations/problems-3.json` | `p-fridge-temperature` | part 4.
   The lead-in says "Using $F = 1.8C + 32$", the prose formula, so the part uses no earlier answer. The explanation works from part 1's form instead ("Times 1.8 on all three parts of $-25 \le \tfrac{F - 32}{1.8} \le -15$"). Question and explanation take different routes, and part 3's result feeds nothing.
   Fix: question "A freezer must stay between $-25$ °C and $-15$ °C, both included. With $C = \dfrac{F - 32}{1.8}$ from part 1, that is $-25 \le \dfrac{F - 32}{1.8} \le -15$. How many whole-number Fahrenheit readings are allowed?" The chain is then 1 to 2 to 3, and 1 to 4, with part 3 the one-sided case of part 4. Answer, `wrong` and feedback unchanged.

7. `minor` | `equations/problems-2.json` and `problems-3.json` | first typed equation and inequality.
   The lessons of levels 2 and 3 hold no expression field: l5 to l13 ask for equations and inequalities by choice, number line, balance and tapped moves (`taught.py`, row "inequality typed or written by the learner": 0 in l10 to l13). The eleven expression parts of these two sets are the learner's first typed equations, inequalities and formulae since level 1, and nothing says how to enter $\ge$ or a fraction.
   Fix: `p-climbing-wall` part 1, append "Type the whole equation, with its $=$ sign." `p-cottage-share` part 1, append "Use the fraction key, or type x/5." `p-bakery-stock` part 1, append "Type $\ge$ as >= or pick it from the maths keyboard." (`240-18h>=60` and `240-18h≥60` both grade correct.)

Functions.

8. `wrong` | `functions/problems-3.json` | `p-track-cubic` | part 3, `explain`.
   "A cubic with a positive $x^3$ rises, turns down, then turns up again." False as a rule: $y = x^3$ and $y = x^3 + x$ only rise (`mine.py`, last check). Lesson l11 says so in its own cubic screen: "$y = x^3$ only rises, but this cubic has two turning points."
   Fix: first sentence "A cubic with a positive $x^3$ and two turning points rises, falls, then rises again." The other two sentences stand.

9. `unclear` | `functions/problems-1.json` | `p-stone-throw` | parts 2 and 4.
   Both need $45 - 5(t - 2)^2 = k$ rearranged and a square undone to two values. Level 1 teaches undoing a two-step linear rule (l2) and that a square comes from two inputs (l4, `review-1`); it does not solve an equation with a squared bracket. The level requires only equations level 1, so rearranging "45 minus" is not assured either. The answers are whole and a table of values finds them, but the question points to algebra the learner has not met.
   Fix: part 2 question "The stone lands when $h(t) = 0$, which means $(t - 2)^2 = 9$. Two numbers have the square 9. At what time after the throw does the stone land? Give a whole number of seconds." Part 4 question "The stone is 40 metres up when $45 - 5(t - 2)^2 = 40$, which means $(t - 2)^2 = 1$. At which times is that? Give both, separated by a comma." Answers, `wrong` and feedback unchanged.

10. `minor` | `functions/problems-2.json` | `p-path-and-pipe` | freshness.
    Both lines of the problem are lesson lines. `homework-2` item 3 asks for the line through $(-4, 0)$ and $(2, 3)$, typed after "$y = \ldots$": its key is `0.5x+2`, the path. Lesson l9 opens with "The first line is $y = 0.5x + 2$", and its first quiz item is "Here is the line $y = -2x + 7$", the pipe, with $-2 \times 0.5 = -1$ in a `why`. The story is new; the numbers are not. The gate found nothing.
    Fix (all in `proposed.py`): prose "a straight path runs through $A(-2, 1)$ and $B(5, 29)$. A pipe will run from a drain at $D(12, 23)$".
    - Part 1: "Give a whole number." Answer 4, `tol` 0. `flipped` 0.25 (`tol` 0.001), `lost-minus` 9.333 (`tol` 0.005): rise 28, run $5 - (-2) = 7$.
    - Part 2: `4x+9`, `accept` `["4x+9", "9+4x"]`. `c-first` `4x+1`, `sign` `4x-7`, `flipped` `0.25x+1.5`. $c = 1 - 4 \times (-2) = 9$; check B: $4 \times 5 + 9 = 29$.
    - Part 3: "Using the path's gradient 4, what gradient must the pipe have? Give a decimal." Answer $-0.25$, `tol` 0.001. `reciprocal` 0.25, `negative` $-4$ ($-4 \times 4 = -16$), `same` 4.
    - Part 4: gradient $-0.25$ through $D(12, 23)$: `-0.25x+26`, `accept` `["-0.25x+26", "26-0.25x", "-\\frac{x}{4}+26", "26-\\frac{x}{4}", "-\\frac{1}{4}x+26"]`. `c-first` `-0.25x+23`, `sign` `-0.25x+20`, `reciprocal` `0.25x+20`. $23 = -3 + c$ gives $c = 26$.
    - Part 5: $4x + 9 = -0.25x + 26$ gives $4.25x = 17$, $x = 4$, the point $(4, 25)$. "Give a whole number." `y-value` 25, `sign-x` 4.533 (`tol` 0.005), `constants` 8.235 (`tol` 0.005).
    Neither new line appears in the course or the 0.2 exam. The author's script needs the same edits.

11. `minor` | `functions/problems-3.json` | `p-bakery-trays` part 2, `p-track-cubic` part 2 | roots from a factorised rule.
    Level 3 reads roots off a graph. "Roots, read from the brackets" appears once, in a `why` line of l11, and `taught.py` finds no screen that sets a factor to 0. Both parts lean on that step with no graph to read.
    Fix: add one sentence to each question. `p-bakery-trays` part 2: "The rule factorises as $P(x) = -5(x - 2)(x - 10)$. A product is 0 only when one of its factors is 0. At which numbers of trays does the bakery break even, $P(x) = 0$? Give both, separated by a comma." `p-track-cubic` part 2: "The rule factorises as $h(x) = x(x - 3)^2$. A product is 0 only when one of its factors is 0. Where does the track meet the floor, $h(x) = 0$? Give both $x$-values, separated by a comma."

12. `minor` | `functions/problems-3.json` | `p-bakery-trays` | parts 4 and 5.
    The result the problem is about, the greatest profit, is part 4. Part 5 then asks where the graph rises, which part 4's explanation has already used ("its turning point is a highest point"). Part 1's $-100$ feeds nothing.
    Fix: swap the two parts. New part 4 is the choice, question unchanged. New part 5 question "Part 4 showed that $P$ rises until $x = 6$ and falls after it. What is the greatest daily profit, in pounds? Give a whole number." The chain is then 2 to 3 to 4 to 5.

13. `minor` | `functions/problems-3.json` | `p-sledge-cyclist` | parts 1 and 2, freshness.
    Lesson l12's quiz asks "A car has gone $d = t^2$ metres after $t$ seconds. What is its average speed over the first 4 seconds?" and `homework-3` repeats it ("$16 \div 4 = 4$ m/s"). Parts 1 and 2 are that item with half the distance: $0.5t^2$ at 4 seconds, then $8 \div 4$.
    Fix: use 5 seconds. Part 1 "How far has the sledge gone after 5 seconds? Give a decimal number of metres." Answer 12.5, `tol` 0.001; `no-square` 2.5, `whole-square` 6.25, `no-half` 25. Part 2 "Using 12.5 m in 5 seconds, what is the sledge's average speed over those 5 seconds, in m/s? Give a decimal." Answer 2.5, `tol` 0.001; `times` 62.5, `distance` 12.5. Explanation: the line from $(0, 0)$ to $(5, 12.5)$, $12.5 \div 5 = 2.5$ m/s, still slower than the cyclist. Parts 3 to 5 are unaffected.

14. `minor` | `functions/problems-3.json` | `p-track-cubic` | freshness.
    Lesson l11 has "A cubic can turn twice. This is $h(x) = x^3 - 3x^2 + 4$, with turning points at $(0, 4)$ and $(2, 0)$. Where is $h$ decreasing?" The track is that curve slid one to the right: $x(x - 3)^2$ is the lesson's $(x + 1)(x - 2)^2$ at $x - 1$, with the same heights 4 and 0 and the same question in part 3.
    Fix (all in `proposed.py`): $h(x) = x^3 - 12x^2 + 36x = x(x - 6)^2$ for $0 \le x \le 8$.
    - Part 1: "What is $h(4)$?" Answer 16 ($64 - 192 + 144$). `all-plus` 400, `cube-as-times` $-36$ ($12 - 192 + 144$).
    - Part 2: answers `[0, 6]`; `signs` `0, -6`.
    - Part 3: turning points at $x = 2$ and $x = 6$, $h(6) = 0$. Options $2 < x < 6$ (correct), $0 < x < 2$ ("climbs from $h(0) = 0$ to its top at $x = 2$"), $6 < x < 8$ ("climbs again, to $h(8) = 32$"), $0 < x < 6$.
    - Part 4: the top at $x = 2$ has height $h(2) = 32$; the line $y = 32$; answers `[2, 8]`, with $h(8) = 512 - 768 + 288 = 32$. `roots` `0, 6`, `turns` `2, 6`.
    Every cubic with a touching root is a slid and stretched copy of the lesson's, so the shape stays; the numbers and heights are then new.

15. `minor` | `functions/problems-3.json` | `p-track-cubic` | chain.
    Part 1's $h(2) = 2$ and part 3's answer feed nothing. Part 4 starts from a given $h(1) = 4$.
    Fix (current numbers; adjust if finding 14 is taken): part 3 question "The turning points are at $x = 1$ and $x = 3$. Part 1 found $h(2) = 2$ and part 2 found $h(3) = 0$. Where is the track going down?" Part 4 question "Part 3 found that the track falls from $x = 1$ to $x = 3$ and climbs after that. The top at $x = 1$ has height $h(1) = 4$. Using the flat line $y = 4$, which $x$-values with $0 \le x \le 4$ solve $h(x) = 4$? Give both, separated by a comma."

16. `minor` | `functions/problems-3.json` | `p-two-cultures` | part 4.
    The part needs $2^{3.3}$ and $2^{3.4}$. Level 3 uses a power that is not a whole number once, in a hint of l13 ("$2^{-1.7} \approx 0.31$"), and there the value is given. Here the learner must find the key on a calculator, and the two values appear only after an answer.
    Fix: question "Using the crossing between 3 and 4 hours, try $t = 3.3$ and $t = 3.4$, with $2^{3.3} \approx 9.849$ and $2^{3.4} \approx 10.556$. Estimate when $200 \times 2^t = 1000 + 300t$. Give your answer to 1 decimal place." These give $N \approx 1970$ and 2111, the feedback's values.

17. `minor` | `functions/problems-3.json` | `p-two-cultures` | part 3.
    "Using part 2" names the part and not its value.
    Fix: question "At 4 hours $N = 3200$ and $M = 2200$. Part 2 found M ahead by 300 at 3 hours. How many times do the graphs of N and M cross for $t \ge 0$?"

18. `minor` | `functions/problems-1.json` | `p-stone-throw` | part 5, and part 4 `byKey` `no-five`.
    Part 5 says "Using part 4" without the values; a learner who missed part 4 meets them only inside the correct option. In part 4, "Those are the landing times from part 2" is loose: $-1$ is before the throw and part 2 says so.
    Fix: part 5 question "Part 4 found that the stone is 40 metres up at 1 second and at 3 seconds. A rule takes a height and gives the time the stone was at that height. Is that rule a function?" Part 4 `"no-five": "Those solve $h(t) = 0$, from part 2. For 40 metres, $(t - 2)^2 = 1$, not 9."`

19. `minor` | `functions/problems-3.json` | `p-sledge-cyclist` | part 3, `wrong` `lost-t`.
    Value 2.449 with `tol` 0.5: any entry from 1.95 to 2.95 is told "You solved $0.5t^2 = 3$", among them a retyped 2 from part 2.
    Fix: `"tol": { "abs": 0.05 }` on that entry (2.4 to 2.5).

20. `minor` | `functions/problems-2.json` | `p-two-savers` | parts 1 and 4.
    Part 1's £130 feeds nothing. In part 4 the key is the longest option by a third (54 characters against 36, 39 and 40) and the only one that names a reason from the lesson.
    Fix: part 4 question "Part 1 put Asha at £130 after 6 weeks, when Ben has £110. Asha's line is $y = 15x + 40$ and, from part 3, Ben's is $y = 15x + 20$. When does Ben's jar catch up with Asha's?" Correct option text "Never: the two lines are parallel". The `correct` line already says he stays £20 behind.

### Per problem

- Chains. Beyond findings 5, 6, 12, 15 and 20, five parts give a value that no later part uses: `p-van-value` part 2 (6 years), `p-bakery-stock` part 3 (the drawing), `p-exchange-kiosk` part 3 (€342), `p-van-fuel` part 1 (42 litres, met again only as a `wrong` entry of part 4) and `p-sledge-cyclist` part 2 (2 m/s, echoed by part 5's averages). Each is a use of the rule on the way to the result, and each sits between parts that do chain. Acceptable; no edit. The other 14 problems chain fully, and every last part bar `p-bakery-trays` (finding 12) asks for the result the problem is about. `p-cottage-share` part 4 and `p-interest-split` part 4 are a second round after the answer; both use the earlier working and restate it.
- Later parts restate what they need: yes, bar findings 2, 17 and 18. The hand-offs give answers inside the bands: 3.3 gives $M = 1990$ and $N = 1970$, and 3.32 gives 1996, all inside $2000 \pm 50$ (`p-two-cultures` part 5).
- Answer form. Every numeric part with a non-whole answer names its form. Eleven equations parts with a whole answer and `tol` 0 say only the unit ("in pounds", "in °C"): `p-family-tickets` 4, `p-food-van` 4, `p-number-trick` 3, `p-market-pitch` 4, `p-climbing-wall` 3, `p-cottage-share` 2 and 3, `p-interest-split` 3 and 4, `p-fridge-temperature` 2, `p-van-value` 2. None refuses a sensible entry. Functions has "Give a whole number" throughout.
- Tolerances. Each band takes the value its feedback prints: 7.28 and not 7.2857 or 7.29 (whole pence asked); 115.71 and 115.714; 10.4; 3.3 and 3.32; 1970, 1990 and 2000. No `wrong` value sits in an answer band or in another entry's band.
- `wrong` entries: 224 entries (144 numeric, 13 set, 67 `wrong[].tex`), all rebuilt in `mine.py`; each is the value its named slip gives and each grades to its own key. Carried slips are present where a learner would carry one (`carried`, `first-row`, `per-row`, `from-1200`, `sixteen`, `one-point`). One band is too wide (finding 19).
- Natural slips that reach the key: none found. `p-track-cubic` part 1 has $h(2) = 2$, so the key equals the input; finding 14's numbers remove that.
- The 13 choice parts are judgements (does one test prove it, which tariff, which drawing, which double inequality, the domain, is it a function, where the line meets the axis, do parallel lines meet, where a curve rises, which is faster, how many crossings). Every `why` is true. No option, `why` or feedback line names an option by place. One key stands out by length (finding 20).
- `form: "simplified"` takes a factorised answer (`5(a-3)` for `5a-15`). The author raised it; the parts say "as simply as possible", so nothing is marked wrongly.

Clean problems (13 of 24): equations set 1 `p-family-tickets`, `p-food-van`, `p-number-trick`, `p-market-pitch`; set 2 `p-cottage-share`, `p-power-tariffs`; set 3 `p-van-value`, `p-fund-weight`; functions set 1 `p-exchange-kiosk`, `p-van-fuel`, `p-sapling-log`; set 2 `p-candle-burn`, `p-two-gyms`. (`p-cottage-share` takes one appended sentence under finding 7, and `p-van-value` part 3 is one of the three in finding 3.)

### Per set

- Lessons. Every lesson of each level is drawn on, and each problem draws on at least two. Equations 1: l1 (a story to an expression, substituting: all four), l2 (like terms: all four), l3 (opening brackets, a negative multiplier, a letter outside: all four), l4 (factorising: tickets, trick, pitch). Equations 2: l5 (tariffs 1), l6 (wall 2 to 4, interest 4), l7 (tariffs 2, cottage 2), l8 (cottage 2, interest 3), l9 (wall 1 and 3, cottage 1, interest 1 and 2). Equations 3: l10 (bakery 1 and 3), l11 (bakery 2, van 3), l12 (bakery 4, fridge 4, van 4 and 5, fund 4), l13 (fridge 1, van 1, fund 1). Functions 1: l1 (kiosk 3, fuel 1, stone 1), l2 (kiosk, sapling, fuel 2), l3 (fuel 3 to 5, stone 3), l4 (stone 5, sapling 1). Functions 2: l5 (savers 1, candle 4), l6 and l8 (all four), l7 (candle 2, gyms 2, savers 3), l9 (path 3 and 5, gyms 3, savers 4). Functions 3: l10 (trays 1, cultures 1, track 1), l11 (trays, track), l12 (sledge only), l13 (sledge 3, cultures 3 and 4, track 4).
- Taught by the end of the level: yes for the equations sets (a percentage as a decimal is l9's broker screen; rounding down to a whole number is l9's budget screen; "the letter appears twice" is l13's derive screen; counting whole numbers in a double inequality is l12). For functions, three ideas run ahead of the level: findings 9, 11 and 16. Two lines set equal is l9's second objective, so `p-path-and-pipe` part 5 and `p-two-gyms` part 3 are in level.
- Reading load. The longest prose or question is 39 words; settings are everyday (tickets, a van, a cottage, a candle, a gym, a sledge) with two light finance ones (an interest split, a fund weight). Functions 3 tests the two graph-reading lessons with no graph on screen; the parts give roots and turning points in words, which works, but it makes findings 11 and 16 matter more.
- Difficulty. One 5 in each set (`p-number-trick`, `p-interest-split`, `p-van-value`, `p-stone-throw`, `p-path-and-pipe`, `p-sledge-cyclist`). `p-number-trick` is the lightest of them: its weight is the sign in $-3(n - 2)$ and the "for every number" judgement. Typed parts 90 of 103.
- Freshness. Gate clean. My own reading, beyond findings 10, 13 and 14: `p-number-trick` opens $5(n + 4)$, which l4 builds from $5n + 20$ on its factorising screen; one bracket, the other task, so it stands. `p-candle-burn` shares the gradient $-2.5$ and the axis-crossing question with `homework-2` item 4 (other point, other answer). `p-power-tariffs` is the shape of `review-2`'s two brokers, `p-two-gyms` of `homework-2`'s two brokers, `p-food-van` of `review-1`'s trader with a fixed cost, `p-climbing-wall` of l9's taxi and phone contract, `p-bakery-trays` of `homework-3`'s "roots 2 and 8, lowest value" and `p-two-cultures` of l13's $2^x = x + 2$: each is the level's idea in a new story with new numbers. The kiosk's 1.15 euros to the pound is also the rate in exam `topic-0.1`, a different course. Between the sets, a bakery appears in equations 3 and functions 3, and a delivery van in equations 3 and functions 1; the courses differ.
- Voice. British spelling, no exclamation marks, no em-dashes, £ and pence for money (euros in the kiosk by design), explanations of at most three sentences (`forms.py` and `voice-scan.py 35`: 0 and 0).

### Engine

- Relations are graded by solution set, with no way to ask for the solved form (finding 3). A `"form": "solved"` (one side a lone letter, the other free of it) would let "Solve" parts refuse the question retyped. The same test passes any linear equation with the key's root on a "write an equation" part (`c=21` for the climbing wall, `x=750` for the cottage); the author's inbox bullet on `wrong[].tex` is this from the other side. Not appended to `docs/BACKLOG-INBOX.md` by this reader (findings only).
- Expression field: a number typed with a thousands comma (`12,000-s`) does not parse as the number, where the numeric field takes `4,800` (finding 1). Stripping a comma between a digit and three digits before parsing would cure it.
- Validator rule worth adding: a `wrong[]` entry whose band is wider than a fifth of its own value (finding 19; review 1.3 c found two).
- Validator rule worth adding: a later part whose question says "Using part n" or "from part n" with no number or formula after it (findings 17 and 18).

### Counts

| tag | equations | functions | total |
|---|---|---|---|
| `wrong` | 0 | 1 | 1 |
| `unclear` | 2 | 1 | 3 |
| `minor` | 5 | 11 | 16 |

### Verdict by set

| set | verdict |
|---|---|
| equations `problems-1` | clean; no edit |
| equations `problems-2` | sound; findings 1, 2, 4, 5, 7 |
| equations `problems-3` | sound; findings 3 (engine), 6, 7 |
| functions `problems-1` | sound; findings 9, 18 |
| functions `problems-2` | sound; findings 10, 20 |
| functions `problems-3` | needs the fix pass: finding 8 (`wrong`), then 11 to 17 and 19 |

One fix pass on Sonnet covers all of it. Findings 10, 13 and 14 change graded answers (new numbers through `p-path-and-pipe`, parts 1 and 2 of `p-sledge-cyclist`, and `p-track-cubic`), and finding 12 reorders two parts, so a delta reader should recompute those items and the functions author's script needs the same edits. The rest change text and one band.

### Scripts (`docs/reviews/problems-0.2-a-scripts/`)

| file | what it does | run |
|---|---|---|
| `mine.py` | the reader's own answer and named-slip value for every numeric, set and expression part, two methods each, and the claims above | `<venv>/bin/python`, exit 0 |
| `grade-check.mjs` | the engine's graders and the widget's shape check on every answer, `accept`, `wrong` and 285 typed strings | `node ... --local-cdn <pkgs>`, exit 0, 7 FINDING rows, 1 NOTE row |
| `proposed.py` | the numbers of the fixes above, twice, and a grep for the new lines and curve in the course and the 0.2 exam | `<venv>/bin/python`, exit 0 |
| `taught.py` | per lesson, counts of each idea a set leans on | `python3` |
| `forms.py` | parts and kinds, skills, form sentences, explanation length, wide `wrong` bands, restated values, choice key length | `python3` |
| `fresh-grep.py` | each setting's nouns and formulae across the course and the exams (`--wide` for every course) | `python3` |
| `skim.py`, `peek.py` | one line per screen or item of a lesson file; every string matching a regex with its JSON path | `python3` |
| `dump.py` | compact dump of a set for reading | `python3` |

All run from the repo root.

## Fix pass

Fix agent, Sonnet. Every changed number was computed twice (sympy or fractions, then a float route, grid, projection or a whole-number count) in `docs/reports/problems-equations-numbers.py` and `problems-functions-numbers.py`, both updated and exit 0 (806 and 787 checks, 0 failures). Expression and set parts were put through the engine's graders with a scratch copy of the reader's `grade-check.mjs` (stale rows for the renumbered parts replaced by 45 new typed rows): 910 checks, 0 failures; the only 5 FINDING rows left are finding 3.

1. fixed. Part 1 and part 2 questions of `p-interest-split` now say "Type 12000 with no comma"; the engine cannot take the comma in an expression (the comma rows of `grade-check.mjs` still refuse), so the prose route was used. Inbox bullet added.
2. fixed. Part 3 restates $0.04s + 0.065(12000 - s) = 660$ and asks for a whole number. Answer 4800 unchanged.
3. deferred (engine). Bullet added to `docs/BACKLOG-INBOX.md` under `Raised later (review problems 0.2 a):`. A content guard is not possible: the unsolved line has the same solution set as the key and is matched as the answer before any `wrong`. The three parts stand.
4. fixed. Part 4 of `p-climbing-wall` asks for pounds "such as 6.45"; `wrong` `pence` = 728 (`tol` 0) and its `byKey` line added. 728 pence = £7.28, and 728 differs from the key 7.28.
5. fixed. Parts 3 and 4 open with the earlier result (21 climbers on £213; 31 climbers on £300) and the form. Answers unchanged. Part 4 check: $45 + 35p \le 300$ gives $p \le 7.2857$, so 7.28 (and 45 + 35 x 7.28 = 299.80).
6. fixed. Part 4 of `p-fridge-temperature` now carries $C = \tfrac{F - 32}{1.8}$ from part 1 and the double inequality. Answer 19 unchanged ($-13 \le F \le 5$, counted 19 by brute force).
7. fixed. Sentences appended to `p-climbing-wall` 1, `p-cottage-share` 1 and `p-bakery-stock` 1 as proposed; `>=` and `≥` grade correct (grade-check rows).
8. fixed. Basis: $y = x^3$ has $y' = 3x^2 \ge 0$, so it only rises; a cubic has two turning points only when $y' = 0$ has two roots. The explanation now says "with a positive $x^3$ and two turning points rises, falls, then rises again". Now on the new curve, $h' = 3(x - 2)(x - 6)$.
9. fixed. `p-stone-throw` part 2 and part 4 questions give $(t - 2)^2 = 9$ and $(t - 2)^2 = 1$ and ask for the times. Answers, `wrong` and feedback unchanged.
10. fixed, graded answers changed (list below). Path through $A(-2, 1)$, $B(5, 29)$: gradient $28/7 = 4$, $c = 1 + 8 = 9$ (B check $20 + 9 = 29$). Pipe gradient $-1/4$, through $D(12, 23)$: $c = 23 + 3 = 26$. Meet: $4x + 9 = -0.25x + 26$, $4.25x = 17$, $x = 4$, $y = 25$. Second route: projecting $D - A = (14, 22)$ on $B - A = (7, 28)$ gives $t = (14 \cdot 7 + 22 \cdot 28)/(49 + 784) = 714/833 = 6/7$, so the foot is $(-2 + 6, 1 + 24) = (4, 25)$, between A and B. Slips rebuilt: flipped $7/28 = 0.25$; lost-minus $28/3 = 9.333$; $c$-first 1; sign $1 - 8 = -7$; flipped line $c = 1 + 0.5 = 1.5$; pipe slips $-0.25x + 23$, $-0.25x + 20$ ($23 - 3$), $0.25x + 20$ ($23 - 0.25 \times 12$); sign-x $17/3.75 = 4.533$; constants $35/4.25 = 8.235$. Parts 1 and 5 say "Give a decimal if it is not whole" instead of "Give a whole number", because the validator's `[wrong-band]` rule (advisory, new on these files) warned that decimal slips sit under a whole-number form. Neither new line is in the course (grep) and the gate gives 0 hits.
11. fixed. One sentence on a product being 0 added to `p-bakery-trays` part 2 and `p-track-cubic` part 2.
12. fixed, graded positions changed. Parts 4 and 5 of `p-bakery-trays` swapped; the new part 5 question restates "Part 4 showed that $P$ rises until $x = 6$ and falls after it". The greatest profit $P(6) = -180 + 360 - 100 = 80$ (grid maximum 80) is now last. Values unchanged.
13. fixed, graded answers changed. Sledge at 5 s: $0.5 \times 25 = 12.5$; average $12.5 / 5 = 2.5$ m/s (below the cyclist's 3). Slips: no-square $2.5$, whole-square $2.5^2 = 6.25$, no-half 25; times $62.5$, distance 12.5. Bands 0.001. Parts 3 to 5 unchanged.
14. fixed, graded answers changed. $h(x) = x^3 - 12x^2 + 36x = x(x - 6)^2$ on $0 \le x \le 8$. $h(4) = 64 - 192 + 144 = 16$ (also $4 \times 4 = 16$). Roots 0 and 6. $h' = 3(x - 2)(x - 6)$, so turning points $(2, 32)$ and $(6, 0)$; it falls only on $2 < x < 6$ (grid check). $h(x) - 32 = (x - 2)^2(x - 8)$ by expansion, so $h = 32$ at 2 and 8 (brute force over 0 to 8 agrees). Slips: all-plus $64 + 192 + 144 = 400$, cube-as-times $12 - 192 + 144 = -36$, signs "0, -6", roots "0, 6", turns "2, 6". The curve is a stretched, slid copy of the lesson's, with new heights; the gate gives 0 hits.
15. fixed. Part 3 carries $h(4) = 16$ and $h(6) = 0$; part 4 carries "falls from $x = 2$ to $x = 6$" and $h(2) = 32$.
16. fixed. Part 4 of `p-two-cultures` gives $2^{3.3} \approx 9.849$ and $2^{3.4} \approx 10.556$ (checked: 9.8492, 10.5561; so $N = 1970$ and 2111). Answer 3.3 unchanged.
17. fixed. Part 3 states that part 2 found M ahead by 300 at 3 hours.
18. fixed. Part 5 of `p-stone-throw` restates 40 m at 1 s and 3 s; `no-five` line now reads "Those solve $h(t) = 0$, from part 2. For 40 metres, $(t - 2)^2 = 1$, not 9."
19. fixed. `lost-t` of `p-sledge-cyclist` part 3: `tol` 0.5 to 0.05 ($\sqrt 6 = 2.4495$; 2.5 and 2 are outside it). The validator's `[wrong-band]` advisory now names this entry (a whole-number question with a decimal slip); kept, since the reader asked for the narrow band.
20. fixed. Part 4 of `p-two-savers` restates £130 and £110 and both lines; the correct option reads "Never: the two lines are parallel".

Per-problem notes (five loose chains, minors): accepted as the reader judged, no edit.

Graded answers, bands and `wrong` values changed (old to new), for a delta reader:

- equations `problems-2` `p-climbing-wall` part 4: `wrong` `pence` added, 728, `tol` 0. Key 7.28 unchanged.
- functions `problems-2` `p-path-and-pipe`:
  - part 1: key 0.5 (`tol` 0.001) to 4 (`tol` 0); `flipped` 2 (0) to 0.25 (0.001); `lost-minus` 1.5 (0.001) to 9.333 (0.005).
  - part 2: key `0.5x+2` to `4x+9`; `accept` (`0.5x+2`, `\frac{x}{2}+2`, `\frac{1}{2}x+2`, `2+0.5x`, `\frac{x+4}{2}`) to (`4x+9`, `9+4x`); `c-first` `0.5x+1` to `4x+1`; `sign` `0.5x` to `4x-7`; `flipped` `2x+5` to `0.25x+1.5`.
  - part 3: key -2 (0) to -0.25 (0.001); `reciprocal` 2 (0) to 0.25 (0.001); `negative` -0.5 to -4 (0.001); `same` 0.5 to 4 (0.001).
  - part 4: key `-2x+7` to `-0.25x+26`; `accept` (`-2x+7`, `7-2x`) to (`-0.25x+26`, `26-0.25x`, `-\frac{x}{4}+26`, `26-\frac{x}{4}`, `-\frac{1}{4}x+26`); `c-first` `-2x-3` to `-0.25x+23`; `sign` `-2x-13` to `-0.25x+20`; `reciprocal` `2x-13` to `0.25x+20`.
  - part 5: key 2 to 4; `y-value` 3 to 25; `sign-x` -3.333 to 4.533 (0.005); `constants` 3.6 to 8.235 (0.005).
- functions `problems-3` `p-bakery-trays`: parts 4 and 5 swapped (new part 4 the choice, key `left`; new part 5 numeric, key 80, `wrong` 75, 60, 440 unchanged).
- functions `problems-3` `p-sledge-cyclist`:
  - part 1: key 8 (0) to 12.5 (0.001); `no-square` 2 to 2.5; `whole-square` 4 to 6.25; `no-half` 16 to 25 (all 0.001).
  - part 2: key 2 (0) to 2.5 (0.001); `times` 32 to 62.5; `distance` 8 to 12.5 (0.001).
  - part 3: `lost-t` 2.449 `tol` 0.5 to 0.05.
- functions `problems-3` `p-track-cubic`:
  - part 1: key 2 to 16; `all-plus` 50 to 400; `cube-as-times` 0 to -36.
  - part 2: key (0, 3) to (0, 6); `signs` "0, -3" to "0, -6".
  - part 3: keyed option `middle` text $1 < x < 3$ to $2 < x < 6$; the three other options renumbered the same way.
  - part 4: key (1, 4) to (2, 8); `roots` "0, 3" to "0, 6"; `turns` "1, 3" to "2, 6".

Gates. Validator 0 errors; the only warning on the six files is `[wrong-band]` for `lost-t` (finding 19). `fresh-check.mjs --file` on the five changed sets: 0 hits each. `playthrough --problems` with `--local-cdn`, equations 2 and 3 and functions 1 to 3, with and without `--mobile`: all passed. Voice scan 35: 0 and 0 on both course folders. Number scripts: both exit 0.
