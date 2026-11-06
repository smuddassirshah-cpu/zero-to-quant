# Topic 3.4 exam: second-reader findings

Scope: `app/content/exams/topic-3.4.json` (id `topic-3.4`, 100 minutes, pass 0.7, 30 items over `algebra` L1 to L4 and `topology` L1 to L3), read in full against `docs/reports/exam-3.4.md`, `docs/AUTHORING.md` sections 5 and 6, both `course.json` maps and every lesson's `skills`, the Continuity list in `docs/reviews/review-algebra-1-2.md`, and the engine's `same` rule (`widgets/order.js`: lines in a `same` set swap only among their own places).

Method: ran the author's scripts (`check_numbers.py`, `fresh.py`); flattened the exam and read every string; recomputed every key, every `wrong` value and every stated number by my own route (brute force over $\mathbb{Z}_n$, $S_4$ and $S_6$ with my own right-to-left composition, a subgroup closure and conjugation by all 24 elements of $S_4$, the topology axioms over every pair, root search over $\mathbb{Z}_3$ and $\mathbb{Z}_7$, Fractions for the integrals, a 200,000-point grid for the maxima, 200 iterations for both fixed points); checked every proof line against every placement the keyed order and `same` allow; measured visible option lengths; searched every `explain`, `feedback` and `why` for words that name an option by place; grepped `algebra`, `topology`, `analysis` and `proof` lessons, reviews and homework for each setup.

Scratch scripts (not committed): `/tmp/claude-0/-home-user-zero-to-quant/563c2e64-8acc-5553-b27e-d47f109c8bd3/scratchpad/rev34/` (`flat.py`, `recompute.py`, `opts.py`, `voice.py`).

Format: `n. item [index] path | severity | problem | evidence | fix`. Severities: wrong, misleading, coverage, voice, layout.

## Script results

- `python3 -I docs/briefs/exam-3.4-scripts/check_numbers.py`: 311 of 311, exit 0. It prints three "check by hand" lines: $\tfrac{8}{105} = 0.0762$, 0.5833 and 0.0833. All three recompute ($\tfrac13 - \tfrac25 + \tfrac17 = \tfrac{8}{105}$, $\tfrac13 + \tfrac14 = \tfrac{7}{12}$, $\tfrac13 \cdot \tfrac14 = \tfrac{1}{12}$).
- `python3 -I docs/briefs/exam-3.4-scripts/fresh.py`: runs, 80 lines, every token found in the exam itself. No hit in `algebra` or `topology` for any keyed setup. Hits elsewhere are generic strings in unrelated courses ($x^2 - 4x$ in quadratics and limits, 901, 1074, $x^3 + 2x^2 + 1$ in numerics).
- My recompute: 90 of 90 checks pass (`recompute.py`). No key and no `wrong` value is off.
- Validator: `0 errors, 2311 warnings`; no line names topic-3.4.
- Voice (my scan, `voice.py`): 662 sentences, 0 over 20 words, 0 explanations over three sentences, no `!`, em-dash, en-dash or American spelling. £ used once, correctly.

## What the author's script does not check

- `numbers_lib` cycle checks: the author's script parses cycles itself (`perm_from_cycles`, and its final pass splits `(1\,2\,3)` into points), so its cycle checks are not vacuous. I still recomputed every cycle claim by my own composition: items 1, 8, 9, 11 (including the three conjugations in the `why` lines), 23 (`d1`'s $V$) and 26.
- Its final pass skips whole numbers up to 10, so counts such as "3 transpositions", "$1 + 3 = 4$", "1 and 7", "10 ways" and "2 orders each" go unchecked. I checked each by hand; all hold.
- Option lengths, explanations that name a shuffled option by place, and the spread of key counts on `multi` items (findings 1 to 5).
- Proof validity: it checks the keyed ids only. Every keyed order is a valid proof and every flawed line is flawed for its `why`. One valid order is not accepted (finding 6).
- Whether each `why` names a plausible learner action, and the reach of claims in explanations (findings 7 and 8).
- Freshness by setup rather than by string (findings 9 and 10).

## Findings

1. `e-four-point-topology` [5] `explain.text` | misleading | The explanation names the key by place, but the options are shuffled. | `widget.shuffle: true`; sentence 1 reads "In the first family, unions and intersections of pairs stay inside it." | Replace sentence 1 with: "In $\{\varnothing, \{1\}, \{2\}, \{1, 2\}, \{1, 2, 3\}, X\}$, unions and intersections of pairs stay inside it."

2. `e-normal-in-s4` [11] `widget.options` | misleading | The key is written out as a set and every distractor as a generator, so the key is three times as long and the only one that lists its elements. | Visible lengths: key 37 characters, distractors 10, 13 and 9. | Write each distractor as its set. `four`: "$\{e, (1\,2\,3\,4), (1\,3)(2\,4), (1\,4\,3\,2)\}$". `three`: "$\{e, (1\,2\,3), (1\,3\,2)\}$". `pair` stays. The `why` lines still hold: $(2\,1\,3\,4) = (1\,3\,4\,2)$ is not in the first set, and $(1\,2\,4)$ is not in the second (recomputed).

3. `e-log-metric` [20] `widget.options[0].text` | misleading | The key is the longest option by far and the only "Yes". | Visible lengths: key 82, distractors 53, 31, 24. | Key `ok`: "Yes: $\ln$ maps $(X, d)$ onto $\mathbb{R}$ keeping distances, and $\mathbb{R}$ is complete." (about 60). Feedback and explanation already give the detail.

4. `e-max-on-circle` [22] `parts[0].widget.options` | misleading | The key is the longest option and the only one that reads as a full argument. | Visible lengths: key 99, distractors 69, 36, 27. | Key `ok`: "The circle is compact and $f$ is continuous, so $f$ of the circle is compact." `bounded`: "$f$ is bounded on the circle, since $|x + 2y| \le 3$ there." `why` lines and feedback unchanged.

5. whole exam, `multi` items [8], [14], [17], [18], [19], [21], [25] | misleading | Every one of the seven `multi` items has exactly two keys, so a learner who notices ticks two. In [18] the second key is also the only long option (43 visible characters against 16 at most). | Key counts 2, 2, 2, 2, 2, 2, 2. | Two changes give counts 2, 2, 2, 1, 3, 2, 2 and remove the length cue. In [18]: set `options[0]` (`glued`) text to "$(-1, 0) \cup (0, 3)$", drop `correct`, and add `why`: "You saw two intervals that meet at 0. The point 0 is missing, so the set splits there." Shorten `options[1]` (`image`) to "$f([0, 5])$, with $f$ continuous". `feedback.correct`: "A continuous image of the connected $[0, 5]$ is connected." Explain sentence 1: "$f([0, 5])$ is connected because $[0, 5]$ is, and $(-1, 0) \cup (0, 3)$ misses 0." In [19]: set `options[4]` (`points`) text to "$\{(\tfrac1n, 0) : n \ge 1\} \cup \{(0, 0)\}$", add `correct: true`, remove its `why`. `feedback.correct`: "The circle, the graph and the points with their limit are closed and bounded." Explain sentence 2: "The points $(\tfrac1n, 0)$ with their limit $(0, 0)$ are closed and bounded too." Explain sentence 3: "The open square misses the limit $(0, 0)$ of $(\tfrac1n, \tfrac1n)$, and the line is unbounded." Update `check_numbers.py` for both keys.

6. `e-cyclic-subgroups-proof` [23] `widget.same` | misleading | A valid order is marked wrong. Line `c3` ($\langle g^m \rangle \subseteq H$) is needed only by `c6`, so it can stand third, fourth or fifth. `same: [["c3", "c4"]]` accepts only the first two, so c1 c2 c4 c5 c3 c6, a natural "one inclusion, then the other" order, fails. | `c5` uses only $g^m \in H$ and closure, not `c3`; `order.js` swaps `same` lines only among their own places. | Tie the order down: `c4` text "Conversely, take $h \in H$ and write $h = g^k$. Divide: $k = qm + r$ with $0 \le r < m$." Remove `same`, and drop the prose sentence "Two lines are independent and may come in either order." Update the `same` assertion in `check_numbers.py` (line 582).

7. `e-jump-metric` [3] `widget.options[1].why` (`tri`) | misleading | The `why` does not name what the learner did. "You counted the extra 1 as a cost to the left side" is hard to parse: the left side, $d(x, z)$, does carry one $+1$. The real slip is reading the inequality the wrong way round. | Option text: "the triangle inequality fails, since two hops add 1 twice". | "You read the inequality the wrong way round. The two hops add 2 to the right side, and the left side gains only 1."

8. `e-equaliser-closed` [24] `explain.text` | misleading | The last clause makes a claim the learner cannot check. "Into an indiscrete two-point $Y$ the claim can fail" gives no maps, and it is joined by a semicolon to the conclusion of the proof. | Explain sentence 3 as quoted. | "So $X \setminus E$ is open; without Hausdorff, two maps from $\mathbb{R}$ to an indiscrete $\{a, b\}$ can agree on $(0, \infty)$ only." (19 words; one map is constant $a$, the other sends $x > 0$ to $a$ and $x \le 0$ to $b$, and $(0, \infty)$ is not closed.)

9. `e-cyclic-subgroups-proof` [23] whole item | coverage | Near reuse of a proof. `algebra` l5 "Every subgroup of Z" orders the same five steps: least positive element, closure gives the multiples, divide, remainder in $H$, remainder 0. Here the steps are written multiplicatively, with one line split in two. The general cyclic case and the two new flawed lines (Lagrange, "least integer") are a real step up, so this is acceptable. | `l5-subgroups.json`, `derive` screen, lines `z1` to `z5`. | Optional: no change, or name the link in the prose ("l5 proved this for $\mathbb{Z}$; now $G$ is any cyclic group") so the item reads as a stated generalisation.

10. whole exam | coverage | Near relatives with new numbers, all acceptable. No change. `e-cycles-bottom-row` [1] asks the order from a bottom row; `algebra` review-2 asks the cycle form from the bottom row $3, 6, 1, 5, 4, 2$. The [18] option $[0, 1] \cup \{2\}$ echoes `topology` homework-2's $[0, 1) \cup \{2\}$. The [17] map $\tfrac{x}{1 - x}$ is a relative of l7's $\tfrac{x}{1 - |x|}$. The longform's $e^{-x}$ is new: l10 uses $xe^{-x}$ and l13 a vega example.

## Checks with no finding

- Every key and every `wrong` recomputes by my own route: 12, 3, 180, 3, 12; 4, 8, 6; 7, 6, 8; 53, 7, 2; 8, 16, 4, 8, 15, 6 (3 is a generator); 9, 13, 11; 3, 6, 1074; 0.3849, 0, 0.375, 0.25, 0.0762; 3, 2, 6, 6, 4, 12; 2.2361, 3, 2; 80, 40, 120; 2, 1, 5, 5, 10, 6, with squares $\{1, 3, 4, 5, 9\}$, $2^5 \equiv 10$, $3^5 \equiv 1$; $\tfrac13$, 0.5833, 0.0833; 11, 10, 13 ($n > 10.88$; bounds $2.6 \times 10^{-6}$ and $8.8 \times 10^{-7}$); $p^* = (1.9678267, -0.0967)$; 0.5671 and $\tfrac1e = 0.3679$. The table [9] gives $\sigma\tau = 1, 5, 2, 4, 3$ and every `sigma-first-k` value is $\tau\sigma(k)$.
- Every key typed at the asked precision lands in its band, and no wrong band overlaps an answer band (0.3849, 0.2500, 2.2361, 0.3333, 1.9678 all within 5e-5).
- Hypotheses: each general claim carries its setting (finite group for $g^{|G|} = e$; abelian for squaring; a field for the root test and $x^2 = 1$; commutative ring with $1 \ne 0$ for a field; Hausdorff in [24]; complete and non-empty in [28] and [29]; Heine-Borel stated for $\mathbb{R}^n$; a subspace of $\mathbb{R}$ for connected means interval). The counter-examples hold: $V$ is order 4 and not cyclic; $x$ on $(0, 1)$ never reaches 1; the conjugations in [11]; $\tfrac1n$ is not $d$-Cauchy in [20].
- Proofs: in [24] `h3` and `h4` are the only free pair, and `same` covers it. In [23] every line other than `c3` is forced. Each flawed line is flawed for its `why`.
- Longform [29]: the rubric sums to 10 (2, 2, 1, 2, 2, 1) and matches the model. The model proves (a) both ways with a reason on each line, shows $T$ is not a contraction (slope ratio tends to 1), bounds $(T^2)' = ue^{-u} \le \tfrac1e$ with $T(X) \subseteq X$, and argues (c) by even and odd iterates.
- Choice and multi: all `shuffle: true`, every distractor has a `why`. No other feedback names an option by place ("first case", "first coordinate" and "$\tau$ first" refer to content).
- Coverage: the 12 skills in `skills` equal the two `course.json` sets, and each is on an auto-graded item. Every level has an item on a skill first met there (algebra 3, 5, 5, 4; topology 4, 4, 5). Ramp 6, 15, 6, 3 (20, 50, 20, 10%).
- Notation follows the Continuity list: right-to-left products, $e$, $\operatorname{ord}$, $\mathbb{Z}_n^{\times}$, $\varphi$ for a homomorphism with "Euler's" each time it means the function, $\overline{A}$, $A^\circ$, $\partial A$, $d_\infty$, $q$.
- Pace: sum 4,995 s = 83 minutes of 100. d2 60 to 90 s, d3 90 to 150 s, d4 180 to 240 s, d5 420 to 600 s. That fits the two-part d3 items, the hand iteration in [28] and a 10-minute longform.

## Counts

- Wrong: 0.
- Misleading: 8 (findings 1 to 8).
- Coverage: 2 (findings 9 and 10; 9 is optional and 10 needs no change).
- Voice: 0. Layout: 0.
- Author's scripts: `check_numbers.py` 311 of 311, exit 0; `fresh.py` clean in both courses. Validator 0 errors, no topic-3.4 warning.

## Engine

Feedback or an explanation that names a shuffled option by place is now seen three times in `docs/reviews` (review-exam-3.2 finding 11, review-exam-1.10 finding 2, finding 1 here). By SESSION PROTOCOL 6 it should become a validator warning before the next wave: on a `choice` or `multi` with `shuffle: true`, warn when its item's `explain.text` or `feedback` holds "first", "second", "third", "last", "above" or "below" followed within three words by "option", "one", "family", "answer" or "choice", or an option letter "(A)" to "(E)". A key longer than 1.5 times every distractor (findings 2 to 4 here, review-exam-1.10 finding 3) is seen twice and could join it as a second warning.
