# Concept audit: brainteasers (topic 3.3), levels 1 to 3

Scope: `app/content/courses/brainteasers/` l1 to l16, review-1 to review-3, homework-1 to homework-3. Blind read (no earlier review or author report opened until the ledger and findings below were committed). Ledger: `docs/reports/audit-brainteasers-1-3-ledger.md` (368 rows: 364 correct, 4 imprecise, 0 wrong, 0 misleading, 0 unverified). Scripts: `docs/reports/brainteasers-L1-concepts.py`, `-L2-`, `-L3-` (exhaustive searches, exact enumerations and possible-worlds models behind every puzzle solution, optimality claim, probability and numerical rule; each check names its ledger row).

Method for a puzzle course: every "no strategy beats", "fewest moves", "cannot be done", "search confirms" and "chance is" claim was recomputed by brute force (state-space BFS for coins, lizards, jugs and crossings; exact cover for tilings; Dijkstra over bridge states; full adaptive search over balance-weighing plans with count-symmetric states; every deterministic three-player hat strategy; every pattern for the modulo and Hamming codes; all permutations for the prisoner counts up to n = 8; minimax egg-drop; a Kripke-style possible-worlds model for muddy children and islanders; full backward induction for pirates with the stated preferences). Every puzzle's stated conditions were checked to pin the keyed answer (tie rules for pirates, "must say heavy or light" and "no genuine coin" for weighings, "light ends only at the start or at an event" for ropes, "possibly none, possibly the top" for eggs).

Format: `N. file | JSON path | severity | problem | evidence and basis | exact fix`.

## Level 1

1. l1-what-stays-the-same.json | screens[7].prose, summary.ideas[2] | imprecise | "A quantity that only falls is a **monovariant**: it proves a process stops" (and "A monovariant moves one way only, so it proves a process stops") drops the hypothesis that makes it true: the quantity must take whole-number values (or values in a well-ordered set) and be bounded below. A learner carries away "decreasing means terminating". | x_n = 1/n only falls and never stops; Engel, *Problem-Solving Strategies*, ch. 1 (invariance principle): a strictly decreasing function into the positive integers forces termination. Every monovariant in the lesson (sum, out-of-order pairs) is a non-negative whole number, so the lesson's uses are sound. | screens[7].prose: "A whole-number quantity that only falls and can never go below zero is a **monovariant**: it proves a process stops." summary.ideas[2]: "A monovariant is a whole number that moves one way only and cannot pass a bound, so it proves a process stops and counts its moves."
2. l2-colouring-boards.json | screens[11].canvas.state.caption, hints[1].text | imprecise | "Shaded cubes have an even coordinate sum" and "The corners are even. So are 14 of the 27 cubes; the centre is odd" hold only with coordinates 0, 1, 2. A learner who numbers the layers 1, 2, 3 (the caption says "layer 1 at the top and layer 3 at the bottom") finds the corners odd and the centre even, the opposite labels. The count (14 with the corners, 13 with the centre) and the conclusion survive either way. | with 1-based coordinates the corner (1, 1, 1) has sum 3 and the centre (2, 2, 2) has sum 6; `brainteasers-L1-concepts.py` "l2 s11" uses 0-based coordinates. | caption: "... S is the start corner and C the centre. Number each coordinate 0, 1, 2: shaded cubes have an even coordinate sum." hints[1].text: "Number each coordinate 0, 1, 2. The corners are even. So are 14 of the 27 cubes; the centre is odd."

## Level 2

3. l11-crossings-and-schedules.json | screens[4].widget.lines[3].text (also explain.text) | imprecise | The proof that 18 is optimal for 1, 3, 6, 8 states case 2 as "6 and 8 cross together, costing 8, and neither walks back", so the sub-case where 6 or 8 carries the torch back is never ruled out. As ordered, the proof has a gap at exactly the step an interviewer probes. | If 6 or 8 returned, that return costs at least 6, so the plan costs at least 8 + 6 + 3 + 3 + 1 = 21 > 18 (the homework-2 item 7 model answer makes this sub-case explicit: "If it is first or last, 6 or 8 must walk the torch back. That costs at least 8 + 6 + 3 + 3 + 1 = 21"). Rote (2002), "Crossing the bridge at night", gives the same case split. `brainteasers-L2-concepts.py` "l11 s4" (five-trip optimum 18; longer plans cost more). | lines[3].text: "Case 2: 6 and 8 cross together, costing 8. A return by 6 or 8 would cost at least 6, so at least 21 in all; so neither walks back." explain.text: "Apart, 6 and 8 cost at least $8 + 6 + 3 + 1 + 1 = 19$. Together, a return by either would cost 6, so 1 and 3 make the returns: $8 + 3 + 3 + 1 + 3 = 18$. Principle: split on how the two slowest cross."
4. l11-crossings-and-schedules.json | screens[6].prose | imprecise | "escort costs $z + a + y + a$; shuttle costs $b + a + z + b$" are not the costs of the two plans: both omit the final crossing of $a$ and $b$ together (cost $b$). The comparison "shuttle when $2b < a + y$" is right because the shared $b$ cancels, but a learner who prices a plan with these formulas gets 15 and 16 for 1, 3, 4, 9 where the same screen's explain gives 18 and 19. | escort = $z + 2a + y + b$, shuttle = $z + a + 3b$ (Rote 2002, the two four-person patterns); `brainteasers-L2-concepts.py` "l11 s6" checks min(escort, shuttle) against a full search for every $a \le b \le y \le z \le 12$ and that shuttle wins iff $2b < a + y$. | "With times $a \le b \le y \le z$: escort costs $z + a + y + a + b$; shuttle costs $b + a + z + b + b$. Both end with $a$ and $b$ crossing together, so drop that shared $b$: $$\text{shuttle when } 2b < a + y$$ For 1, 3, 6, 8: $6 < 7$, so shuttle. For 1, 4, 5, 6: $8 > 6$, so escort."

## Level 3

No findings. Every clock angle, event count, rate, doubling time, constant, last digit, trailing-zero count, sum and mixed-set answer was recomputed from first principles and matches; the stated conventions (yearly compounding for the rule of 72, the smaller angle between hands, equal distances for the harmonic mean, "possibly none, possibly the top" for floors) are the standard ones and are said where they first matter.

## Checked and clean

Level 1: the lizard invariant (differences modulo 3) and the reachable-position counts (9 from (1, 2, 3); every colour on island P, all blue in 5 meetings; none on Q); every coin-turning parity claim (9, 10, 11, 13, 15 coins) by BFS; the 3 x 3 and 4 x 4 lamp subspaces (32 and 128 patterns, reachable counts {0, 3, 4, 5, 6, 9} and {0, 4, 6, 8, 10, 12, 16}, every 2 x 2 block even, two lit lamps always leave an odd block); all four rub-out-and-write invariants over every order; 15 neighbour swaps; every domino, 1 x 3, 1 x 4 and T-tetromino tiling claim by exact cover (13 dark removals of 5 x 5, 7 x 7 minus corner, third square, centre; 6 x 6 and 4 x 7 by T impossible, 4 x 4 by T possible; the nine 1 x 3 removals of 7 x 7); 824 Hamiltonian paths from the corner of 5 x 5 and their endpoint set; knight distance 6; closed tours on 4 x 4 and none on 5 x 5; the 3 x 3 x 3 cheese by search; every pigeonhole bound and its sharpness; every weighing claim by full adaptive search (12 yes, 13 no, 13 + genuine yes, 14 + genuine no, 39 yes, 40 no, 40 + genuine yes, (3^k - 3)/2 and (3^k - 1)/2 for k = 2..4, 3^k heavy-only for k = 1..5); every jug count by BFS and the gcd formula for all a, b <= 12; the no-tap 10, 7, 3 split (9, and 10 when starting into the 3); every rope mark by enumerating every event-driven plan; every hourglass plan by simulation.

Level 2: pirate splits for every crew 2 to 10 under the stated preferences, the merciful and strict-majority variants, 40 and 100 coins; lions by recursion; the line, three-colour and simultaneous hat codes on every pattern (n - 1 certain, exactly one right); the three-player pass-or-guess optimum 3/4 over all 81^3 strategies and the Hamming strategy 7/8 over all 128 patterns; prisoner counts by all permutations (n = 4, 6, 8, 9) and the harmonic formula (n = 10, 12, 100 with 50 and 60 openings), the 1/k law and the need for k > n/2, uniform cycle length through box 1, the one-swap fix; egg-drop minimax for every stated building (10, 21, 36, 50, 80, 100, 120, 200, 300, 1,000 floors; 1 to 3 eggs), the first-floor sets {4}, {8}, {9..14}, {24}, the recurrence and the binomial sum against the search; bridge optima by Dijkstra for every four- and five-walker set in the level and the escort-or-shuttle rule against the search for all times up to 12; the river crossing (11); the grill schedules; muddy children and islanders in a possible-worlds model (rounds k, k - 1 after "at least two", k - 2 after "at least three", never without the announcement, night 6 after a silent night 5).

Level 3: every clock angle against the hand positions at every minute of 12 hours; the meeting, right-angle and opposite counts by direct enumeration; every doubling time against ln 2 / ln(1 + r); the monotone numerator r T; the table of constants; every last digit, remainder and trailing-zero count from the integers themselves; every sum by direct addition; the mixed set's coins, weighings, tiling, pirates, bridges, prisoners, floors and jugs by search.

Cross-course references checked against the named lessons: Contest Practice l8 (cut chessboard, "an invariant is not a route", backtest fills) and l5 (modulo, trade-id checksum); Reasoning and Proof l9 (hash buckets); Counting and Chance l10 (birthday, pigeonhole); Probability Puzzles l19 (take-away games); Games, Auctions and Poker l10 (bargaining); Sequences and Series l6 (Gauss pairing); Mental Arithmetic Drills l8 (squaring); Mental Maths Under Pressure l8 (square roots); Exponentials and Logarithms l12 (rule of 72). All exist and say what the lesson claims.

## Overlap with the earlier review

Read after the commit of the ledger and findings above: `docs/reviews/review-brainteasers.md` (second read plus its fix pass, 30 items, 29 fixed and 1 disputed-and-corrected). Every one of its findings had been applied before this audit, so the content audited here is the post-fix course: "both" can only count findings that survived the fix pass, and none did.

| Conceptual findings | Count | Items |
|---|---:|---|
| Audit only | 4 | 1 to 4 above (monovariant hypothesis; cube coordinate convention; the unproved "neither walks back" line in l11 s4; the escort and shuttle costs in l11 s6) |
| Review only | 13 | listed below; all were fixed before this audit and the fixed text was verified in the ledger |
| Both | 0 | |

The earlier review's conceptual findings, with why this audit did not raise them:

- l4 s7, 13 coins "find or say which" (two readings): fixed before the audit; the audited prose says "find the fake and say heavy or light" and the ledger checks both readings (find-only 13 is possible, say-which is not).
- l5 s10, the looping jug cycle in the hints: fixed; the audited hints give the rule whose play is the 9-pour shortest route (ledger, `L1:l5 s11 hint`).
- l3 s8 `wrong` ten, why naming the wrong slip: fixed; the audited why names the merged-box slip.
- l4 s8 `wrong` onetwentyone, (3^5 - 1)/2 without "with one genuine coin spare": fixed; the ledger verifies both formulas for k = 2..4.
- review-2 r1, pirates without "proposer included" (two readings, 99 against 98): fixed; the audited item states it, and `L2:review-2 item 0` checks the split is unique.
- l11 s11 `wrong` thirty with no slip: fixed to 31 with the 3-escorts slip; verified.
- homework-2 item 6 `wrong` twentyfour with no slip: fixed; verified (2 escorting 1 and 5 gives 24).
- homework-2 item 7 model, "cannot be first or last" with a wrong reason: disputed by the fixer and rewritten as a bound (21 for the first-or-last sub-case); the audit found the rewritten model correct and it is the text the lesson's own derive (finding 3) should match.
- l6 s2 and review-2 item 6, lions without "eats whenever it is safe": fixed; the audited rule is complete.
- l10 s7, induction hypothesis without "and not before": fixed; the audited line carries it.
- l10 s11, "markets move on a widely expected rate cut": fixed to the common-knowledge wording; the ledger marks the fixed sentence correct.
- Deck items with no stated rules (l1 quiz 1, l2 quiz 0 and 1, l6 quiz 0 to 2, homework-2 items 0, 4, 5): fixed; every audited item states its rules in full.
- homework-2 item 6 `wrong` seventeen citing a puzzle never set: fixed; verified (1, 2, 5, 10 alone take 17).

The review's other 17 items (shuffle flags, raw lesson ids, layout at phone width, duplicated puzzles, a difficulty ramp, a table header, a wrong-entry id) are not conceptual and are outside this audit's scope.

Miss rate of the single read on what survived it: the second read plus fix pass left 4 conceptual `imprecise` items (0 `wrong`) in 16 lessons, 3 reviews and 3 homeworks that this blind read found. The earlier read found 13 conceptual items the fix pass removed, among them 3 `error`-grade (two readings of a puzzle twice, a looping method once); none of this audit's 4 is of that grade.

## Checks

- Validator (from `app/`): `node tools/validate.mjs 2>&1 | tail -3` gives `0 errors, 4262 warnings` (whole app; the O2 advisory warnings). `content/manifest.json` restored with `git checkout` afterwards.
- Voice: `VOICE_BASE=app/content/courses/brainteasers/ python3 docs/reviews/voice-scan.py 35 --summary` gives `sentences scanned: 9311; over 35 words: 0` and `explanations over three sentences: 0`.
- Number scripts: no `docs/reports/brainteasers-L<n>-numbers.py` exists in the repo (the author and reader scripts lived in scratchpad folders named in the review); so none run. Every stated number met in this audit was recomputed inside the concepts scripts instead.
- Concepts scripts (`python3 -I` from the repo root): `docs/reports/brainteasers-L1-concepts.py` exit 0, 103 checks (30 s); `docs/reports/brainteasers-L2-concepts.py` exit 0, 79 checks (3 min 46 s, the 81^3 hat-strategy enumeration); `docs/reports/brainteasers-L3-concepts.py` exit 0, 71 checks (under 1 s).
- Playthrough (from `app/`, with `--local-cdn <pkgs>`): `--set brainteasers/review-1 --set brainteasers/homework-1`: `browser relaunches: 0 / All passed.`; review-2 and homework-2: `All passed.`; review-3 and homework-3: `All passed.`; `--lesson brainteasers/l1-what-stays-the-same`, `l8-prisoners-and-boxes`, `l15-numbers-to-know`: `All passed.` each, with and without `--mobile`. No content was changed, so this only confirms the audited files play.

## Fix pass

1. fixed | basis: a strictly falling real sequence need not stop (1/n); termination needs values in the non-negative integers, which forces at most I(start) moves. Applied to screens[7].prose and summary.ideas[2] as proposed.
2. fixed | basis: with coordinates 0, 1, 2 the even-sum count is (3^3 + 1^3)/2 = 14 and the corner (0, 0, 0) is even, the centre (1, 1, 1) odd; with 1, 2, 3 it is (27 - 1)/2 = 13 and the labels flip. Caption and hints[1] now fix the 0, 1, 2 numbering.
3. fixed | basis: if 6 or 8 walks back, the plan still has the 8 trip, a return of at least 6, two more trips over of at least 3 and a return of at least 1: 8 + 6 + 3 + 3 + 1 = 21 > 18; otherwise the other trips over are both {1, 3} and the returns are one each of 1 and 3: 8 + 3 + 3 + 1 + 3 = 18. lines[3] and explain.text now state the sub-case (my own wording, same content as proposed).
4. fixed | basis: escort a+z, a, a+y, a, a+b costs z + 2a + y + b; shuttle a+b, a, y+z, b, a+b costs z + a + 3b; difference 2b - a - y. Checks: 1, 3, 4, 9 gives 18 and 19; 1, 3, 6, 8 gives 19 and 18; 1, 4, 5, 6 gives 17 and 19, all matching the screens. Applied to screens[6].prose as proposed.

Counts: fixed 4, disputed 0, deferred 0. No graded answer changed.

Checks after the fix:
- Validator (from `app/`): `0 errors, 4262 warnings`; `content/manifest.json` unchanged.
- Concepts scripts (`python3 -I`, repo root): L1 exit 0 (103 checks), L2 exit 0 (79 checks), L3 exit 0 (71 checks). No numbers scripts exist for this course.
- Voice: `sentences scanned: 9313; over 35 words: 0`, `explanations over three sentences: 0`.
- Playthrough (`--local-cdn <pkgs>`), plain and `--mobile`: l1-what-stays-the-same (16 checks, quiz 4/4), l2-colouring-boards (15 checks, quiz 3/3), l11-crossings-and-schedules (15 checks, quiz 3/3): `All passed.` each, both modes.
