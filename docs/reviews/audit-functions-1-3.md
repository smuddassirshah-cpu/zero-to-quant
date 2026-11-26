# Concept audit: functions (topic 0.2), levels 1 to 3, round 1

Scope: `app/content/courses/functions/` `l1` to `l13`, `review-1` to `review-3`, `homework-1` to `homework-3`, `problems-1` to `problems-3`, `fluency-l8-line-through-two-points`, at commit `eba9ca3e`. Level 4 is a separate audit. Blind read: no review, earlier audit or author report on this course was opened until the ledger and the findings below were committed.

Stage 0, so the ledger uses the reduced depth: `docs/reports/audit-functions-1-3-ledger.md`, 1028 rows (1015 correct, 11 imprecise, 1 misleading, 1 wrong, 0 unverified). Script: `docs/reports/functions-L1-3-concepts.py` (687 checks; it reads every numeric key and slip from the JSON and recomputes it, enumerates both fluency families over their whole range, and holds a counterexample for each `imprecise` finding it can express).

Sources: Gelfand, Glagoleva and Shnol, *Functions and Graphs*; Pearson Edexcel *Pure Mathematics* Year 1 (ch. 2, 4, 5, 12) and Year 2 (ch. 2); Hull, *Options, Futures and Other Derivatives* (ch. 4, 10, 12) for the bond and payoff items.

Format: `N. file | JSON path | severity, tag | problem | evidence and basis | exact fix`.

## Findings

### Level 1

3. l2-table-to-rule.json | screens[4].explain.text | imprecise, minor | "A table whose climb changes has no rule of the form $mx + c$" drops its hypothesis: the inputs must rise in equal steps. Five screens later the lesson's own transfer table has inputs £15.00, £16.00, £17.50 and profit climbs of £40.00 and £60.00, and its rule is $40s - 610$. | Script NOTE "l2 s[4]": both pairs of rows give the same line. The generalise screen (s[7]) states the hypothesis correctly ("When the inputs climb in equal steps and the outputs do too"). | Replace the last sentence with: "When the inputs go up in equal steps and the climb still changes, no rule of the form $mx + c$ fits."

4. l3-what-goes-in.json | screens[2].feedback.byKey.ends | imprecise, minor | The `ends` region (any point between 3.7 and 4.3) says "You used $f(-2) = 4$ as the lowest output. The curve dips to 0 at $x = 0$." The drag-point widget fires a region for either point, so a learner with `lowest` right at 0 and `highest` at 4 (the left end taken as the top) is told they got the lowest output wrong. | `app/js/engine/widgets/drag-point.js`, grade loop: `for (const w of spec.wrong) for (const p of pts) if (inRegion(...))`. The line must hold for both points. | "You marked 4, the output at the left end, $x = -2$. The lowest output is 0, at $x = 0$, and the highest is $f(3) = 9$."

### Level 2

5. l8-line-through-two-points.json | screens[1].canvas.derive (caption, hide, vert.from, vert.to) | misleading, minor | A and B both snap to whole numbers and both drag, so they can be put on the same grid point. The canvas then draws one vertical line and captions it "A and B are one above the other: the line is vertical". The screen is about uniqueness, and its own option says of one point "many lines pass through it". A learner who tries the coincident case sees a single line through a single point. | The derive tests only `B.x == A.x`. Euclid's first postulate needs two different points, as the question says. | Add the coincident case to the derive: `"hide": "B.x == A.x ? ['f'] : []"` stays; change `vert.from` to `"B.x == A.x && B.y != A.y ? [A.x, -10] : [99, 99]"`, `vert.to` to `"B.x == A.x && B.y != A.y ? [A.x, 10] : [99, 100]"`, and the caption to `"{{B.x == A.x && B.y == A.y ? 'A and B are the same point: many lines pass through it' : B.x == A.x ? 'A and B are one above the other: the line is vertical' : 'Rise ' + (B.y - A.y) + ' over run ' + (B.x - A.x)}}"`.

8. l9-parallel-perpendicular.json | screens[8].explain.text, screens[8].feedback.correct | imprecise, minor | "Their product is always $-1$, whatever $a$ and $b$ are" and "Any quarter turn gives a product of $-1$". The derivation divides by $a$ and by $b$, so both must be non-zero. With $b = 0$ the first line is flat and the turned line is vertical, which is the case screens[5] has just said the rule does not cover. | $m_1 = b/a$ and $m_2 = -a/b$; $b = 0$ gives no $m_2$. Script NOTE "l9 s[8]". | explain: "Their product is always $-1$, whatever $a$ and $b$ are, as long as neither is 0." feedback.correct: "A quarter turn of a sloping line always gives a product of $-1$."

### Level 3

1. l13-solving-with-graphs.json | screens[7].widget.options[b].why | wrong, minor | Option b is $y = x - 2$ and its `why` says "You moved the terms without changing their signs." Moving $-x$ and $-2$ across unchanged gives $y = -x - 2$, which is not the option. Option b changes the sign of the $x$ and leaves the 2 alone. The option is rightly marked wrong; its diagnosis names a different slip. | From $x^2 - x - 2 = 0$: correct is $x^2 = x + 2$; both signs unchanged is $x^2 = -x - 2$; option b is $x^2 = x - 2$. Script check FINDING 1 (fails as written). | "You changed the sign of the $x$ but not of the 2. Adding $x + 2$ to both sides gives $x^2 = x + 2$."

2. homework-3.json | items[7].model part (c), items[7].rubric[1].text (and part (b) "it is convex, flattening as the yield grows") | imprecise, serious | "the gradient is getting less negative: the curve is flattening, which is what convex means", with the rubric marking "convex (flattening)". Convex means the curve bends upwards: its gradient rises. On a falling curve that shows as flattening; on a rising curve it shows as steepening. A learner carries away "convex = flattening" and will call $y = 2^x$ or a call payoff, both convex, not convex. Convexity is a word this learner will meet again for bonds and options, so the definition matters. | $y = 2^x$ is convex and its steps 1, 2, 4, 8, 16 grow (script NOTE "hw3 model (c)"). Hull ch. 4.10 and A-level Year 2 ch. 9 (convex where the second derivative is positive, that is, the gradient increasing). l10 screens[9] ties "convex" to "bending upwards" and is correct. | Part (c), last sentence: "The same 2-point rise in yield costs less each time, so the gradient is rising (getting less negative). A rising gradient is what convex means: the curve bends upwards, and on a falling curve that shows as flattening." Part (b): "It bends upwards, so it is convex; because it is falling, that makes it flatten as the yield grows, like the right-hand piece of $y = \tfrac{1}{x}$." Rubric[1]: "Describes the curve as decreasing and convex (bending upwards, so flattening as it falls), never reaching 0."

6. l11-reading-a-graph.json | screens[5].question, options `o` and `f`, explain.text | imprecise, minor | "Which points are roots of $g$?" with $(0, 0)$ and $(4, 0)$ keyed, and "So $(0, 0)$ is a root and the y-intercept at once". Two screens earlier the lesson says "A root is an $x$-value, read off the horizontal axis", and the summary repeats it. The screen grades the opposite usage. | A-level Year 1 ch. 2.1: the roots of $f$ are the values of $x$ with $f(x) = 0$. | question: "At which points does the graph of $g$ meet the x-axis? Select all that apply." explain: "The curve meets the x-axis at $x = 0$ and $x = 4$, so the roots are 0 and 4. At the origin it also meets the y-axis. So $x = 0$ is a root, and the y-intercept is 0 as well." feedback.correct: "Both x-axis crossings: $(0, 0)$ and $(4, 0)$, so the roots are 0 and 4." Option `t` why: "That is the turning point. At a root the height is 0."

7. l11-reading-a-graph.json | screens[8].prose, summary.ideas[0] | imprecise, minor | "**Roots** are the $x$-values where the curve crosses the x-axis". screens[6] has just shown a root at $x = 2$ where $h$ touches the axis and turns back without crossing ("That root is also a turning point"). | $h(x) = (x + 1)(x - 2)^2$ does not change sign at 2. | Replace "crosses" with "meets" in both strings: "**Roots** are the $x$-values where the curve meets the x-axis: they solve $f(x) = 0$." and "Roots are the $x$-values where a curve meets the x-axis: they solve $f(x) = 0$."

9. l10-curves-from-tables.json | screens[4].explain.text | imprecise, minor | "A line a curve approaches but never reaches is an **asymptote**." True of the two curves in this lesson, but "never reaches" is not part of the definition, and it is a known misconception that a graph cannot touch or cross its asymptote. | $y = \dfrac{x}{x^2 + 1}$ has the x-axis as its asymptote and meets it at the origin (script NOTE "l10 s[4]"); damped oscillations cross theirs without end. A-level Year 1 ch. 4.3: "a line which the curve approaches". | "The curve climbs ever more steeply towards the y-axis but never touches it. A line that a curve gets closer and closer to like this is an **asymptote**. Negative inputs give a second piece, in the bottom left."

10. l10-curves-from-tables.json | screens[9].question, feedback.correct, explain.text, wrong `same` | imprecise, minor | "From 2% to 4% the price falls by £14.47." The fall is $82.0348 - 67.5564 = 14.4784$, so £14.48 to the penny; £14.47 is the difference of the two rounded labels. The keyed £9.52 is right both ways. | Script NOTE "l10 s[9]". House rule: every stated number computed twice. | Say what the figure is: question "The marked prices fall by £14.47 from 2% to 4%. By how much do they fall from 6% to 8%?" The other strings can keep £14.47 once the question frames it as the gap between the marked prices.

11. l12-graphs-that-tell-stories.json | summary.ideas[2] | imprecise, serious | "At a highest or lowest point the gradient is 0, however high or low the graph is." This is the turning-point rule with its hypotheses dropped: the curve must be smooth there and the point must not be at an end of the domain. The course's own graphs break it. The straddle in l13 screens[9] is lowest at the strike, a corner with gradients $-1$ and $+1$. $f(x) = x^2$ on $-2 \le x \le 3$ (l3) is highest at the end $x = 3$, where the gradient is 6. Sam's walk in this lesson is highest along a whole flat stretch entered at a corner. Level 4 goes on to payoffs, which are all corners. | Script NOTE "l12 summary". A-level Year 1 ch. 12.9: the gradient is 0 at a stationary point of a differentiable curve; maxima on a closed interval can sit at the ends. The trap screen (s[7]) and its feedback are correct, since they speak of that smooth curve. | "At the top or bottom of a smooth bend the gradient is 0, however high or low the graph is. A corner, or the end of a graph, can be the highest or lowest point without that."

## Checked and clean

Definition of a function. l1 introduces the machine, l4 gives "every input in its domain gives exactly one output" and the vertical line test with "at most once". Many-to-one is separated from one-to-many on six screens, and every keyed judgement (tables, $y^2 = x$, the circle, $x = 4$, overlapping fee bands, the sapling log, height-to-time for the stone) is right.

Domain and range. Every range was recomputed on a grid with the open and closed ends ($x^2$ on $[-2, 3]$ and $(-3, 2]$, $(x - 1)^2$ on $(0, 4]$, the linear cases, the put and call payoffs, the whole-share domain). The rule "ends of the range are not the outputs at the ends of the domain" is stated and tested.

Undoing. Reverse order of steps is right everywhere; "undoing only works when no two inputs share an output" (l4 s[5]) and "allowing only $x \ge 0$ fixes it" (review-1 item 8) carry the one-to-one condition and the restricted domain.

Straight lines. Every gradient, intercept, equation, crossing and break-even in l5 to l9, review-2, homework-2 and problems-2 was recomputed with exact fractions, with each slip value. Gradient units are stated wherever the axes have units. Vertical lines are handled as "no gradient, $x = k$" on every screen that meets one, and both the parallel and perpendicular rules carry "neither rule covers a vertical line". The 53-degree figure in l9 s[3] is right.

Curves. All table values, landmarks (roots, intercepts, turning points), increasing and decreasing intervals, the cubic $h(x) = (x + 1)(x - 2)^2$, the track cubic $x(x - 6)^2$, the bakery parabola, and the two exponential-against-line crossings ($2^x = x + 2$ at $-1.69$; cultures at 3.32, once only for $t \ge 0$) were recomputed. Bond prices to the penny, the 4.6% chord estimate against the exact 4.56%, and the direction of the chord's error are right.

Rates. Speed against average speed, marginal against average cost, the sign of a falling gradient, and both drawdown items (peak before trough) are right.

Joins. Every piecewise graph puts each boundary in exactly one band, and the keyed values at the joins (l4 s[3], s[8], review-1 item 6, homework-1 item 6) are right.

Canvas regions. Every drag-point region was read against `drag-point.js` with the canvas's snap and axis locks; apart from finding 4, each line is true at every position that can fire it. Slider ranges and the two sketch `wrong` curves are right.

Fluency. Both families of `fluency-l8` were enumerated in full (gradient: every draw; line-equation: every draw). The key equals the true gradient or line on every draw, no slip ever equals the key or the other slip, and each slip line is true on every draw.

Plain words. New terms (domain, range, gradient, intercept, parabola, asymptote, tangent, root, turning point, strike, implied volatility, drawdown, straddle, convex) are each said in plain words where they first appear.

## Run results

- `node tools/validate.mjs`: 0 errors.
- `node tools/run-number-scripts.mjs --only functions`: 6 scripts, 6 passed.
- `node tools/grade-all.mjs --file <each of the 23 files> --local-cdn <pkgs>`: 0 failures on every file.
- `docs/reports/functions-L1-3-concepts.py`: 687 checks, 686 pass, exit 1. The one failing check is FINDING 1 and stays failing until the `why` is corrected.
- No playthrough, as the common rules set.

## Overlap with the earlier reads

Read after the blind-stage commit: `docs/reviews/review-functions-1-2.md` (27 findings on L1 and L2, with its fix pass), `docs/reviews/review-functions-3-4.md` (its L3 findings 3 to 8, 10, 13, 16 to 18, 20 to 25, 27, 31, with its fix pass), `docs/reviews/review-problems-0.2-a.md` (functions findings 8 to 20) and `docs/reviews/review-delta-problems-aa-2.md` (functions findings 3 and 4). There is no earlier concept audit of this course and no row for it in `docs/reports/concept-audit-log.md`. Every earlier finding had been applied before this audit, so the text audited is the post-fix course and "both" can only count defects that survived a fix pass.

| Conceptual findings | Count | Items |
|---|---:|---|
| Audit only | 11 | 1 to 11 above |
| Earlier reads only | 13 | listed below; all fixed before this audit, and each fixed string has a `correct` ledger row |
| Both | 0 | |

New `wrong` that no earlier read found: 1 (finding 1, minor).

Earlier conceptual findings, each checked against the audited text:

- review-functions-1-2, 1: l2 s[6], three rows did not fix $f(4)$. Fixed with a fourth row; the ledger row notes the key now rests on the pattern the hint names.
- review-functions-1-2, 4: l3 s[4], a `reversed` region held the target of `hi`. Removed. Same class as finding 4 here, on a different screen and region (s[2] `ends`), so not counted as "both".
- review-functions-1-2, 6: homework-2 item 6, parallel needs $a_1 \ne a_2$. Fixed; verified.
- review-functions-1-2, 8: l9 s[5], "the one perpendicular pair". Fixed to "one kind of"; verified.
- review-functions-1-2, 11: l8 quiz[2], `why` did not explain the slip. Fixed; verified ($8x + 1$).
- review-functions-3-4, 3: homework-3 model (d), shown arithmetic. Fixed; 1.2522 and 79.86 recomputed.
- review-functions-3-4, 4: l12 s[9] `max-min` diagnosis. Fixed; $420 - 90 = 330$ verified.
- review-functions-3-4, 5: l10 summary and s[6], shape claims need a positive leading term. Fixed; verified.
- review-functions-3-4, 6: l11 s[6] option b `why`. Fixed; $h = (x + 1)(x - 2)^2$ verified.
- review-functions-3-4, 7: l11 quiz[1], key was also a root. Fixed to $x^2 - 6x + 8$; verified.
- review-problems-0.2-a, 8: problems-3 track cubic, "a cubic with positive $x^3$ rises, turns down, turns up". Fixed with "and two turning points"; verified.
- review-problems-0.2-a, 19: problems-3 sledge `lost-t` band. Fixed to 0.05; no overlap with the key or part 2's answer.
- review-delta-problems-aa-2, 3: problems-3 track `count` line left over from the old cubic. Fixed; verified.

The earlier reads' other items (undefined option terms, GCSE wording, the left-hand-side typing note, freshness repeats, chains between parts, length giveaways, sentence counts, one label) are not conceptual and are outside this audit.

Two notes on how the misses arose.

- Finding 3's sentence ("A table whose climb changes has no rule of the form $mx + c$") was written by the earlier fix pass, as the paste-ready text of review-functions-1-2 finding 13 (a voice fix). It is fix-pass text that no reader had checked as a claim.
- Finding 1 is the class "a `why` names a slip that does not produce the option". The earlier reads caught three of that class in these levels (l8 quiz[2], l12 s[9], l11 s[6]) and this audit one more. With finding 4 the class "a region line that is false for one of two points" has now been seen twice in this course. Both are raised in `docs/BACKLOG-INBOX.md`.

## Inbox

Two bullets under "Raised later (audit functions):" in `docs/BACKLOG-INBOX.md`: point-scoped `drag-point` regions (finding 4), and coincident draggable points in a `derive` equality test (finding 5).
