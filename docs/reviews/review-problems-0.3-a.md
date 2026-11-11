# Problem sets 0.3 (a): second-reader findings

Read at commit ee4f68a. A full second read of four sets. Pattern: `review-problems-0.2-a.md`.

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` = the question can be read two ways, does not give what the learner needs, or refuses a sensible entry in the stated form; `minor` = weak part, loose chain, loose `wrong` entry, wording, freshness or tooling.

## A. Second read: counting 1 to 3, functions 4

Scope: `app/content/courses/counting/problems-1.json` to `problems-3.json` and `app/content/courses/functions/problems-4.json`: 16 problems, 71 parts (53 counting, 18 functions; 52 numeric, 15 expression, 4 choice). One numeric part is a two-value set. Ten of the expression parts are vectors: six typed as `(across, up)` pairs and four as expressions in r and s. Functions sets 1 to 3 are not read here.

Method. The two authors' scripts were run first. Every part was then solved from its text before its key was read (`questions.py` prints a set with no answers), by hand, and again in `mine.py`. Every counting answer there is a full enumeration (`itertools`: every row of tulips, every line-up of the seven players, every signal of seven flags, every row of the BALLOON blocks, all 3160 pairs of members, all 330 teams) set against the formula in exact fractions. Vector and function parts are done in sympy and again in numbers (`hypot`, `atan2`, a real triangle for the sail, a grid of stays for the car park, every whole number of tickets for the bonus). Every `wrong` value was rebuilt from the slip its feedback line names and compared inside that entry's own band; every expression key, `accept` form and `wrong[].tex` was compared with my own expression. Every part was then put through the engine's own graders in node (`grade-check.mjs`: `parseNum`, `within`, `matchWrong`, `numSetGrade`, `exprEqual`, `exprShapeLine`, with the local Compute Engine): the answer, each `accept` form, each `wrong` entry on its own key, and 215 typed strings of my own (thousands commas, fractions for decimals, roundings, a vector as a row, a column, with spaces, with a Unicode minus, unadded, other orders of r and s, unsimplified lines, a letter and `=` in front, units). `form-probe.mjs` shows what `"form": "simplified"` would do to each part that asks for a simplest form. The lessons, quizzes, review, homework and Fluency sets of each level were read screen by screen (`skim.py`), and `counting-chance` with its three problem sets was searched for each setting and number (`fresh-grep.py`).

Tool results.

| check | result |
|---|---|
| authors' number scripts | counting 1754 checks, 0 failures; functions 4: 444 checks, 0 failures |
| `mine.py` (reader's own answers and slips) | 71 parts, 631 checks, 0 failures |
| `grade-check.mjs` (engine graders) | 672 checks, 0 failures, 6 rows held to be faults (findings 4, 13, 14) |
| `form-probe.mjs` | `simplified` refuses the unsimplified lines of findings 4, 13 and 14; it also refuses $-\tfrac{2r}{3} + \tfrac{s}{3}$ and $\tfrac{5t - 4}{2}$ (see Engine) |
| `proposed.py` (numbers of finding 6, freshness of the new numbers) | 10 checks, 0 failures |
| validator | 0 errors; 0 warnings on the four files |
| playthrough `--problems`, four sets, `--local-cdn` | all passed |
| the same with `--mobile` | all passed |
| voice scan 35, two course folders | 0 and 0 |
| `fresh-check.mjs --file`, gate | 0 hits on each set |
| `fresh-check.mjs --min-run 8 --min-share 0` | counting 0 hits; functions 4: 5 hits, all the instruction "Type only what comes after the $=$ sign" |
| `fresh-grep.py` and the reader's own reading | two reuses the tool missed (findings 6 and 7) and four notes under Freshness |
| `forms.py` (shape, skills, form sentences, restated values) | every item skill is a skill of its level; no explanation over three sentences; rows judged below |

Result. No `answer`, `accept`, feedback line, `why` or explanation states a wrong value or a false rule; there is no `wrong` finding. Every stated number agrees with mine. Every answer and `accept` form grades correct, every `wrong` entry grades wrong and lands on its own key, and no `wrong` band reaches the answer band or catches an unrelated value (the widest are ±0.5 round a non-whole slip on a whole-number part, which catches the slip rounded either way and nothing else). No natural slip gives a keyed answer: where a second route reaches the key (56 as $8 \times 7$, 17 as $80 - 45 - 38 + 20$, 1803 as $100\sqrt{325}$, 7.5 as half of 15, 10.25 as $12.75 - 2.50$) it is a correct route.

Counting wording. Each of the 34 parts of counting sets 1 and 2 fixes one count. Ordered or not is said each time ("ignoring which spot each one takes", "pairs of teams", "all as equals", "the order in the cup does not matter", "stacked up, so the order from bottom to top matters"); repeats are ruled out by "different varieties" and "scoops of different flavours"; identical objects are named ("Flags of one colour look identical", "Blocks with the same letter look identical"); and each chance says what is equally likely ("each of the 105", "every pair", "every one of the 1260 rows", "every group of 4"). The one loose word is "orders" in finding 9.

Forms. Numeric fields take `6,720`, `5/7`, `75/105`, `17/395`, `-£145`, a Unicode minus, `2 1/2` and `15/4, 45/4`. Each chance band takes the exact fraction, the unreduced fraction and the decimal to 3 places, and refuses the decimal to 2 places. Leisure centre part 3 ($\tfrac{17}{80} = 0.2125$) takes both 0.213 and 0.212. A vector is taken as `(9,12)`, `(9, 12)`, `\left(9,12\right)`, `9,12`, `[9,12]` and a `pmatrix` column; `(12,9)` and a third entry are refused; a sum left unadded, `(9,12)+(-12,16)`, gets the "two numbers in brackets" line. Expressions in r and s take either order, a common denominator, a factor outside a bracket, `0.5(r+s)`, capital letters and `RS=s-r`. A number with a unit word after it (`22 cm`, `115°`, `28 tickets`) does not parse, so the field does not submit it; every such part says "whole number of centimetres", "in metres" or "in degrees".

"Simplest form" in r and s. The engine does not enforce it. Nothing correct is refused for that reason. What it lets through: an unsimplified but correct vector on sail ring parts 2 to 4 ($\mathbf{r} + \tfrac12(\mathbf{s} - \mathbf{r})$, $-\mathbf{r} + \tfrac13\mathbf{r} + \tfrac13\mathbf{s}$), which is lenient but still the learner's own step; and on part 3 the question's own line with $\tfrac23$ in front, which is not (finding 4).

Claims checked beyond the keys: a glued block of twins counts the 192 line-ups plus 48 with the twins either side of the captain; $n(n - 1) = 72$ has one positive whole solution; the 21 pairs of places for the blue flags are equally likely, so the check by places in flags part 4 is sound; 120 rows of BALLOON have both pairs glued; a negative dot product means an angle over 90°; X on OM with $\overrightarrow{OX} = \tfrac23\overrightarrow{OM}$ is the centroid and lies two thirds of the way along RN in a numeric triangle; $h(0.8x)$ is the only one of the four rules that leaves at 0, lands at 15 and tops at 5.4; $C(t - 1)$ is the only one of the four rules equal to the new charge for every stay over 1 hour, and $C(t) - 2.5$ matches above 3 hours and gives 50p below 2; a rate of 30% is 1.5 times every old bonus and keeps the start at 20 tickets.

### Findings

Counting.

1. `unclear` | `counting/problems-3.json` | `p-orienteering` | part 5.
   "How much shorter is the straight line from S to Q than the route via P?" The route, 3500 m, is the answer to part 4 and is not restated. A learner who missed part 4 has nothing to subtract from. The grid scale is not restated either.
   Fix: question "The route via P is 3500 m, from part 4. Using $\overrightarrow{SQ} = (-3, 28)$ in grid squares of 100 m, how much shorter is the straight line from S to Q than the route? Give your answer to the nearest metre." Answer, `wrong` and feedback unchanged.

2. `unclear` | `counting/problems-3.json` | `p-grain-merchant` | part 4.
   "Using $\mathbf{h}' \cdot \mathbf{d} = -145$, find the angle between $\mathbf{h}'$ and $\mathbf{d}$." The angle needs $|\mathbf{h}'|$, so it needs $\mathbf{h}' = (40, 70)$, the answer to part 2. It is not restated: part 3 gives only the trade. A learner who typed $(80, 10)$ in part 2 gets 62°, which no `wrong` entry names.
   Fix: question "Her new holdings are $\mathbf{h}' = (40, 70)$, from part 2, and $\mathbf{d} = (2.50, -3.50)$. Using $\mathbf{h}' \cdot \mathbf{d} = -145$, find the angle between $\mathbf{h}'$ and $\mathbf{d}$, in degrees, to the nearest degree." Answer, `wrong` and feedback unchanged.

3. `minor` | `counting/problems-3.json` | `p-orienteering` part 4, `p-power-line` part 5 | values not restated.
   Orienteering part 4 needs both legs and names neither; they stand in part 3's question, one part up. Power line part 5 says "Using $\overrightarrow{AC} = 2.5\,\overrightarrow{AB}$" and needs $\overrightarrow{AB} = (6, 4)$, last seen in part 3. Both can be rebuilt from the prose, so this is weaker than findings 1 and 2. Orienteering part 4 also has no form sentence; its answer is a whole number of metres.
   Fix: orienteering part 4 question "Using $\overrightarrow{SP} = (9, 12)$ and $\overrightarrow{PQ} = (-12, 16)$, in grid squares of 100 m, how far does the runner run on the route S to P to Q? Give a whole number of metres." Power line part 5 question "Using $\overrightarrow{AB} = (6, 4)$ and $\overrightarrow{AC} = 2.5\,\overrightarrow{AB}$, with each unit 100 m, how long is the cable from A to C? Give your answer to the nearest metre."

4. `minor` | `counting/problems-3.json` | `p-sail-ring` | part 3, "write $\overrightarrow{OX}$ in its simplest form".
   The prose gives $\overrightarrow{OX} = \tfrac23\overrightarrow{OM}$ and the question gives $\overrightarrow{OM}$. Typing the two together, `\frac{2}{3}(\frac{1}{2}r+\frac{1}{2}s)`, grades correct with no step done (`grade-check.mjs`). Parts 2 and 4 also take an unsimplified line, but there the line is the learner's own route.
   Fix: part 3 widget add `"form": "simplified"`, and `byKey` add `"form": "That is equal, but multiply it out: $\\tfrac{2}{3} \\times \\tfrac{1}{2} = \\tfrac{1}{3}$ for each term."` `form-probe.mjs`: the key, both `accept` forms, $\tfrac{r+s}{3}$ and $\tfrac{r}{3} + \tfrac{s}{3}$ pass; the retyped line fails. Do not add the form to part 4: there it refuses the sensible $-\tfrac{2r}{3} + \tfrac{s}{3}$ (see Engine). Part 2 needs nothing: the form does not refuse $\mathbf{r} + \tfrac12(\mathbf{s} - \mathbf{r})$.

5. `minor` | `counting/problems-3.json` | `p-orienteering` parts 1 and 2, `p-power-line` parts 1 and 2 | "Write ... as a column vector. Give it as (across, up)."
   Two forms in one question: a column, then a row in brackets. The lessons of this level never ask for a typed vector (they use two boxes or a choice), so this is the learner's first. The field takes a row or a column, so nothing is marked wrongly; no example shows what to type.
   Fix: orienteering part 1 question "Write $\overrightarrow{SP}$, in grid squares. Type it as (across, up), such as (3, -1)." Part 2 the same with $\overrightarrow{PQ}$. Power line part 1 "Write $\overrightarrow{AB}$. Type it as (across, up), such as (3, -1)." Part 2 the same with $\overrightarrow{AC}$.

6. `minor` | `counting/problems-1.json` | `p-ice-cream-van` | freshness.
   The first count is $\binom{11}{3} = 165$. `counting/homework-1.json` works the same count with the same line ("3 more stocks ... from the other 11. That gives $\binom{11}{3} = \dfrac{11 \times 10 \times 9}{3!} = 165$ portfolios"). The author's report moved this item off 7 flavours for the same reason and landed on a used count. The tool reads question text only, so it missed it.
   Fix: 14 flavours. Numbers from `proposed.py` (enumerated; fresh in counting, counting-chance and the two exams; 364 appears elsewhere only as the $\tfrac{364}{365}$ of the birthday problem). Prose "sells 14 flavours". In every line, $11 \times 10 \times 9$ becomes $14 \times 13 \times 12$, $\binom{11}{3}$ becomes $\binom{14}{3}$, $P(11, 3)$ becomes $P(14, 3)$ and $11^3$ becomes $14^3$.

   | part | answer | `wrong` values |
   |---|---|---|
   | 1 | 364 | `ordered` 2184, `repeats` 2744, `times` 42 ("You multiplied 14 by 3") |
   | 2 "Using 364 sets" | 2184 | `times-three` 1092, `added` 370, `carried` 13104 ("$2184 \times 6$, from 2184 cups") |
   | 3 "Using 364 cups and 2184 cones" | 2548 | `multiplied` 794976, `carried` 15288 ("adds 2184 cups and 13104 cones") |
   | 4 "Using 2548 items" | 12740 | `no-none` 10192, `added` 2553, `carried` 3974880 ("$794976 \times 5$") |

   Working lines: $2184 \div 6 = 364$; $364 \times 6 = 2184$; $364 + 2184 = 2548$; $2548 \times 5 = 12740$; $2548 \times 4 = 10192$. Update the author's script to match.

7. `minor` | `counting/problems-1.json` | `p-team-photo` | freshness.
   `exams/stage-0.json` item `p-arrangements`: "4 of 7 people stand in a row for a photo." The problem lines up 7 players in a row for a photo. The counts differ ($P(7, 4)$ there), but the story and the 7 are the same, and the stage exam is the paper this course leads to.
   Fix: prose "A coach lines up the 7 players of a netball team in one row to be introduced before a match. The captain must stand in the middle place. The two shooters are twins and must stand side by side." No other text names the photo or the photographer; the item id stays.

8. `minor` | `counting/problems-1.json` | `p-team-photo` | chain.
   Part 2's 720 feeds nothing: part 4 counts $4 \times 2 \times 4!$ afresh.
   Fix: part 4 question "Part 2 found 720 orders with the captain in the middle. Using the 4 side-by-side pairs of free places, how many of those 720 also have the twins side by side?" Answer and `wrong` unchanged.

9. `minor` | `counting/problems-1.json` | `p-ice-cream-van` | part 4, "how many different orders are there?"
   In this problem "order" means the order of scoops (prose, parts 1 and 2). Here it means a purchase.
   Fix: question "Every item also comes with one of 4 toppings or with no topping. Using 1155 items, how many different purchases can she make?" Explanation "The topping stage has $4 + 1 = 5$ choices, whatever the item. So the purchases number $1155 \times 5 = 5775$." (With finding 6: 2548 and 12740.)

10. `minor` | `counting/problems-2.json` | `p-leisure-centre` | chain.
    Part 3's $\tfrac{17}{80}$ feeds nothing: part 4 goes back to the 17 of part 2. Only its slip is used, as part 4's `replaced` entry.
    Fix: part 4 question "Part 3 gave $\tfrac{17}{80}$ for one member. Now two different members are picked at random for a survey, every pair equally likely. Squaring $\tfrac{17}{80}$ would let one member be picked twice, so count pairs. Using 17 who do neither, what is the chance both do neither? Give a decimal to 3 places." Answer and `wrong` unchanged.

11. `minor` | `counting/problems-2.json` | `p-leisure-centre` | part 1 explanation.
    "$|S \cup G| = 45 + 38 - 20 = 63$." Neither S nor G is named anywhere in the problem.
    Fix: explanation "Adding $45 + 38$ counts each of the 20 who do both twice. Take them away once: $45 + 38 - 20 = 63$ members do at least one."

12. `minor` | `counting/problems-2.json` | `p-quiz-team` | part 3, "Using 330 and 5".
    The two numbers are restated without saying what they count. Every other lead-in of the three sets names its values.
    Fix: question "Using 330 teams in all and 5 with no girls, how many teams have at least one girl?"

Functions.

13. `minor` | `functions/problems-4.json` | `p-car-park` | part 2, "write the charge as simply as possible".
    The prose prints the piece as $3 + 2.5(t - 2)$. Typing it back, `3+2.5(t-2)`, grades correct, as does the half-done `3+2.5t-5` (`grade-check.mjs`). The part can be passed with no work, and part 3 then hands over the answer.
    Fix: widget add `"form": "simplified"`, and `byKey` add `"form": "That is equal, but open the bracket and collect the numbers into one."` `form-probe.mjs`: the key and its three `accept` forms pass, and the three unsimplified lines fail. The unusual $\tfrac{5t - 4}{2}$ would get the `form` line too.

14. `minor` | `functions/problems-4.json` | `p-ticket-bonus` | part 2, "as simply as possible".
    `0.2(25n-500)` grades correct. It is the learner's own composite, so this is weaker than finding 13, but the question asks for the simple form and part 3 builds on it.
    Fix: widget add `"form": "simplified"`, and `byKey` add `"form": "That is equal, but open the bracket: $0.2 \\times 25n = 5n$ and $0.2 \\times 500 = 100$."` `form-probe.mjs`: `5n-100`, `-100+5n` and `5(n-20)` pass; `0.2(25n-500)` fails.

15. `minor` | `functions/problems-4.json` | `p-photo-mount` parts 2 and 3, `p-ticket-bonus` part 2 | the left side typed in.
    Each says "Type only what comes after the $=$ sign". A learner who types the whole line is refused with the generic line: `m(e(x))=1.5x+4` gets "Not quite. $e$ acts first, so $m$ is handed $1.5x$", for a right answer. The same habit passes elsewhere in the set (`C(t)=2.5t-2`, `n=\frac{b+100}{5}`, `y=1.5x+4`), so the refusal is the engine's reading of a nested left side, not a rule the learner can see.
    Fix (content, until the engine item lands): end each of the three generic lines with one more sentence. Photo part 2 "Not quite. $e$ acts first, so $m$ is handed $1.5x$. Type the rule alone, with no $m(e(x)) =$ in front." Photo part 3 "Not quite. Undo the steps of $f$ in reverse order. Type the rule alone, with no $f^{-1}(x) =$ in front." Bonus part 2 "Not quite. $T$ acts first, so $B$ is handed $25n$. Type the rule alone, with no $B(T(n)) =$ in front."

### Per problem

- `p-tulip-bed` (3): sound. Chain 1 and 2 to 3 to 4; part 3 checks $70 \times 24$ against $P(8, 4)$.
- `p-team-photo` (5): sound, and the best item of set 1: the glued block of the lesson fails because the captain splits the row. Findings 7 and 8.
- `p-five-a-side` (4): sound. Part 3 hands over $n(n - 1)$ and asks for a search; part 4 uses its 9.
- `p-ice-cream-van` (4): sound. The one place in the set where counts add. Findings 6 and 9.
- `p-signal-flags` (4): sound. The block of identical blues that needs no doubling is a real trap, with its slip carried through parts 3 and 4.
- `p-leisure-centre` (4): sound. Findings 10 and 11.
- `p-balloon-blocks` (5): sound. Part 4 is the hard step (take off the 240 rows with the Ls together and the Os apart); both natural slips are named.
- `p-quiz-team` (4): sound. Finding 12.
- `p-orienteering` (3): sound. Findings 1, 3 and 5.
- `p-power-line` (4): sound. The choice is a judgement (parallel from a shared point, and beyond B since $k > 1$). Findings 3 and 5.
- `p-grain-merchant` (4): sound. Part 3 uses the split of the dot product over the trade, then checks it directly. Finding 2.
- `p-sail-ring` (5): sound. Finding 4.
- `p-photo-mount` (4): sound. Part 5 closes the chain: the same photo in the other order comes out 2 cm wider. Finding 15.
- `p-fountain-jet` (4): sound. Its keyed work is all l15; l14 enters only through the sliding distractor and its carried slips.
- `p-car-park` (4): sound. "For any stay over 1 hour" is needed and is there. Finding 13.
- `p-ticket-bonus` (5): sound. Findings 14 and 15.

### Per set

- counting 1 (l1 to l4): every lesson covered, each problem draws on two or more, one difficulty 5, typed 15 of 16. Only ideas of the level: the product rule, adding for one choice from two lists (l1 quiz), factorials, a fixed place and a glued pair (l2), $P(n, r)$, $\binom{n}{r}$ and its symmetry.
- counting 2 (l5 to l8): every lesson covered (round tables of l6 are not used, which the brief does not ask), one difficulty 5, typed 18 of 18. Gluing a pair of identical items joins l5 and l6 in a way neither lesson does alone; that is the point of flags part 2 and BALLOON part 2. $|A \cup B|$ is taught in l7; pairs over pairs in l8.
- counting 3 (l9 to l13): every lesson covered, one difficulty 5, typed 18 of 19. The angle from the dot product and the split $(\mathbf{p} + \mathbf{q}) \cdot \mathbf{d}$ are both in l13; a point a fraction of the way along a side is in the l12 quiz. Direction and unit vectors (l11) are not used.
- functions 4 (l14 to l18): every lesson covered, one difficulty 5, typed 16 of 18. $\max$ and a rule in pieces are in l18; $f(bx)$ and the 1/b widths in l15; "kink" in l18.
- Reading load: the longest prose or question is 43 words in counting and 53 in functions (`forms.py`). Fit for a GCSE-entry learner.

Freshness notes (no change asked). BALLOON's last answer, $\tfrac{11}{21} \approx 0.524$, is also an answer in `counting-chance/problems-2.json` ($\tfrac{11}{15} \times \tfrac{10}{14}$), a later course and another story. The leisure centre (80; 45, 38, 20 both) is the fourth "both and neither" count of the course after l7 (40; 22, 15, 9 and 250; 60, 45, 20) and review-2 (120; 70, 50, 30); it shares 45 and 20 with the l7 transfer screen, and its parts 3 and 4 go on to chances, which those do not. Orienteering starts at $S(1, 2)$, as the l11 drone does at $A(1, 2)$; the vectors differ. The bonus problem's theatre also sells the tickets of `equations/problems-1.json` `p-family-tickets`, another course.

### Engine

- `"form": "simplified"` (`expression.js` `formOk`: size of the typed tree against the size of its `simplify()`) refuses some simplest forms: `-\frac{2r}{3}+\frac{s}{3}` and `\frac{5t-4}{2}` (`form-probe.mjs`). So the form cannot be put on sail ring part 4, where the first is a natural answer (finding 4). A check that asks only for like terms collected and no bracket left unopened would serve these parts.
- A typed left side is dropped for `C(t)=`, `n=` and `y=`, but not for a nested or inverse name: `m(e(x))=1.5x+4`, `f^{-1}(x)=\frac{x-4}{1.5}` and `B(T(n))=5n-100` grade wrong with the generic line (finding 15). Reading `name(...) =` at the start of an expression answer as a label, whatever sits in the brackets, would cure it.
- Numeric field: a number followed by a unit word or a degree sign (`22 cm`, `3500 m`, `115°`) does not parse, though `£75` in front does. Stripping a trailing unit that the question names, or a `unit` shown after the field on these parts, would save a retype.
- Validator rule worth adding (0.2 a asked the same): a later part whose question uses a symbol or a quantity that only an earlier part's answer supplies, even when its lead-in restates some other value (findings 1 and 2 each restate one value and leave out the one that matters).

### Counts

| course | wrong | unclear | minor | total |
|---|---|---|---|---|
| counting | 0 | 2 | 10 | 12 |
| functions | 0 | 0 | 3 | 3 |
| all | 0 | 2 | 13 | 15 |

### Verdict by set

| set | verdict |
|---|---|
| counting 1 | Sound. Two freshness fixes (6, 7), one of them a renumbering of the ice-cream van; a chain and a word (8, 9). |
| counting 2 | Sound. Three small wording fixes (10, 11, 12). |
| counting 3 | Sound in its mathematics. Two parts do not restate what they need (1, 2) and should be fixed before release; then 3, 4 and 5. |
| functions 4 | Sound. Two "as simply as possible" parts take the unsimplified line (13, 14); one generic line misleads on a typed left side (15). |

No part needs its key, band or `wrong` values changed except by the renumbering of finding 6.

### Scripts (`docs/reviews/problems-0.3-a-scripts/`)

Run from the repo root; `<venv>` and `<pkgs>` are the scratchpad paths of `docs/LEVEL-BRIEF.md`.

- `questions.py <file>`: a set with no answers, for solving before reading the key.
- `dump.py <file>`: one block per part with key, bands, `wrong` entries and feedback.
- `mine.py` (`<venv>/bin/python`): the reader's own answers, every count by enumeration and by formula, every `wrong` value from its slip; 631 checks, exit 0.
- `grade-check.mjs --local-cdn <pkgs> [--probe]`: the engine's graders on every answer, `accept`, `wrong` and 215 typed strings; 672 checks, 0 failures, 6 `FINDING` rows; exit 0.
- `form-probe.mjs --local-cdn <pkgs>`: what `"form": "simplified"` passes and refuses on the parts of findings 4, 13 and 14.
- `proposed.py` (`<venv>/bin/python`): the numbers of finding 6 and their freshness; 10 checks, exit 0.
- `fresh-grep.py [--wide]`: settings and numbers of each problem searched across the course, `counting-chance` and the exams.
- `forms.py`: shape, skills, form sentences, restated values, reading load.
- `skim.py <file> [width]`, `peek.py <file> <regex>`: one line per screen or item, for the lesson read.

## Fix pass

I recomputed every changed number before writing it: the 14-flavour counts by formula (`comb`, `perm`) and by enumeration of every cup, cone and item (`docs/reports/problems-counting-numbers.py`, now pinned to 364, 2184, 2548 and 12740, so a revert fails it), and each `wrong` value from its slip. The new stated figures are all restatements of earlier answers (720, 3500, 40 and 70, the vector components). `problems-counting-numbers.py`: 1759 checks, exit 0. `problems-functions-4-numbers.py`: 444 checks, exit 0. Engine graders (`grade-check.mjs` run on the fixed content, its stale rows for the old ice-cream totals and the one refused single fraction updated): 675 checks, 0 failures, 1 finding (sail ring part 4 takes the unopened route, deliberately, see finding 4). Status: fixed 15, disputed 0, deferred 0 (engine items are in the inbox).

1. Orienteering part 5: fixed. The question restates the 3500 m and the grid scale; answer, `wrong` and feedback unchanged.
2. Grain merchant part 4: fixed. The question restates h' = (40, 70) and d; answer 115 and `wrong` unchanged.
3. Orienteering part 4 and power line part 5: fixed. Both restate the vectors and the 100 m scale; orienteering part 4 now says "Give a whole number of metres".
4. Sail ring part 3: fixed with `"form": "simplified"` and a `byKey.form` line. Part 4 left without it, as asked. Engine graders on the fixed content: the key, both `accept` forms, $\tfrac{r+s}{3}$ and $\tfrac{r}{3}+\tfrac{s}{3}$ grade correct; $\tfrac{2}{3}(\tfrac{1}{2}r+\tfrac{1}{2}s)$ returns `form`.
5. Orienteering parts 1 and 2, power line parts 1 and 2: fixed. Each says "Type it as (across, up), such as (3, -1)."
6. Ice-cream van: fixed with 14 flavours, every line, prose, `wrong`, feedback and explain renumbered. Check: $\binom{14}{3} = \tfrac{14 \cdot 13 \cdot 12}{6} = 364$ and enumeration of 364 sets; $P(14,3) = 2184 = 364 \times 6$ and enumeration of 2184 stacks; $364 + 2184 = 2548$; $2548 \times 5 = 12740$. Reader's table agrees.
7. Team photo: fixed. Prose now has a coach lining up the 7 players of a netball team to be introduced before a match. The item id stays.
8. Team photo part 4: fixed. The question restates the 720 and asks how many of those also have the twins side by side; answer 192 unchanged.
9. Ice-cream part 4: fixed. "purchases" replaces "orders" in the question and the explanation.
10. Leisure centre part 4: fixed. The question opens with the 17/80 of part 3 and the reason for counting pairs.
11. Leisure centre part 1 explanation: fixed, no S and G symbols.
12. Quiz team part 3: fixed. "Using 330 teams in all and 5 with no girls".
13. Car park part 2: fixed with `"form": "simplified"` and a `byKey.form` line. Engine graders: `2.5t-2`, `-2+2.5t`, `C(t)=2.5t-2`, `2.50t-2`, $\tfrac{5}{2}t-2$ pass; `3+2.5(t-2)`, `3+2.5t-5` and `2.5(t-2)+3` return `form`. The single fraction $\tfrac{5t-4}{2}$ is now refused with the `form` line (the engine item in the inbox), which I judge acceptable for a rarely typed form.
14. Ticket bonus part 2: fixed with `"form": "simplified"` and a `byKey.form` line. `5n-100`, `-100+5n`, `5(n-20)` pass; `0.2(25n-500)` returns `form`.
15. Photo mount parts 2 and 3, ticket bonus part 2: fixed. Each generic line ends with the sentence telling the learner to type the rule alone.

Four engine bullets added to `docs/BACKLOG-INBOX.md` under `Raised later (review problems 0.3 a):`. Report tables: `docs/reports/problems-counting.md` (freshness paragraph) and `problems-functions-4.md` updated.

Gates: validator 0 errors. `fresh-check.mjs --file` 0 hits on all four sets. Playthrough `--problems` with `--local-cdn`, four sets, desktop and `--mobile`: all passed. Voice scan 35 on `counting` and `functions`: 0 and 0. The reader's `mine.py` and `proposed.py` still hold the old ice-cream numbers and now report failures; they record the state at ee4f68a and were not edited.

### Parts changed (for a delta reader to recompute)

Counting problems-1 `p-ice-cream-van` (14 flavours in place of 11; answer, `accept` and `wrong` values):

| part | answer old to new | `wrong` old to new |
|---|---|---|
| 1 | 165 to 364 | ordered 990 to 2184; repeats 1331 to 2744; times 33 to 42 |
| 2 | 990 to 2184 | times-three 495 to 1092; added 171 to 370; carried 5940 to 13104 |
| 3 | 1155 to 2548 | multiplied 163350 to 794976; carried 6930 to 15288 |
| 4 | 5775 to 12740 | no-none 4620 to 10192; added 1160 to 2553; carried 816750 to 3974880 |

Form added (`"form": "simplified"`, plus a `byKey.form` line; answers, `accept` and `wrong` values unchanged):
- counting problems-3 `p-sail-ring` part 3 (key $\tfrac{1}{3}r + \tfrac{1}{3}s$).
- functions problems-4 `p-car-park` part 2 (key $2.5t - 2$).
- functions problems-4 `p-ticket-bonus` part 2 (key $5n - 100$).

Nothing else changed a graded answer, band or `wrong` value; the other items are question, prose, explanation or generic-feedback wording.
