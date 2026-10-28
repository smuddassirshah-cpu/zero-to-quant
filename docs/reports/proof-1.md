# Report: proof level 1, "Statements and logic"

Course `proof` (topic 0.6, strand pure), level 1, from `## Level 1` of `docs/briefs/proof.md`. All files use skill `pv-logic` and the ids, names and objectives of `app/content/courses/proof/course.json` exactly.

## Files written

All in `app/content/courses/proof/`.

| File | Screens | Quiz / items | Canvases | Notes |
|---|---:|---:|---|---|
| `l1-true-or-false.json` | 10 | 4 | table (tap rows), number-line | statement, truth value, open sentence, truth set, Goldbach edge, risk-limit transfer |
| `l2-and-or-not.json` | 11 | 4 | table (tap rows), venn, code | price alert and/or/not, truth tables, venn truth sets, De Morgan, inclusive-or trap, optional `code` screen, risk-flag transfer |
| `l3-if-then.json` | 11 | 4 | boxes (cards), venn | four-card task, P ⇒ Q truth table, breaking region `A`, only if, converse/contrapositive/inverse (`place` assign), affirming the converse trap, vacuous truth, margin-rule transfer |
| `l4-for-all-there-exists.json` | 10 | 4 | grid, number-line, table | trader grid witnesses, Thursday breaker (count mode), `place` order for claim A, domain ℝ against ℤ, ∀∃ against ∃∀, function rule, claim B trap, empty domain, static-hedge transfer |
| `l5-saying-the-opposite.json` | 10 | 4 | table, grid, number-line | refuting trade, negating ∀ and ∃, l4 grid negation, x < 5, spread-rule trap, `manipulate` step-by-step negation, `place` order limit negation, audit transfer |
| `review-1.json` | | 9 | boxes, grid | difficulties 2, 2, 3, 3, 4, 2, 3, 3, 4; covers l1, l2 (2), l3 (2), l4 (2), l5 (2) |
| `homework-1.json` | | 8 | grid | difficulties 3, 3, 4, 4, 4, 5, 3, 5; two `order` derivations with `distractors` (contrapositive agreement at 4, limit negation at 5), one `longform` (10-point rubric, model answer) |

Generators (Python, one per file) and checking scripts are in the scratchpad folder `proof-1` (`gen_l1.py` to `gen_l5.py`, `gen_review.py`, `gen_hw.py`, `checks.py`, `voice.py`).

## Validator

`node tools/validate.mjs` from `app/`: **0 errors**, 365 warnings, none in a level 1 proof file. The only proof warning is the course's "not yet written" line for levels 2 and 3.

## Playthrough

All with `--local-cdn` set to the scratchpad `pkgs` folder, with `--shots`, `--why` and `--mobile` runs; screenshots looked at for every lesson and set.

| Target | Result |
|---|---|
| `--lesson proof/l1-true-or-false` | ok, 14 checks, quiz 4/4 |
| `--lesson proof/l2-and-or-not` | ok, 15 checks, quiz 4/4 (the code screen's solution passes all 7 tests in Pyodide) |
| `--lesson proof/l3-if-then` | ok, 15 checks, quiz 4/4 |
| `--lesson proof/l4-for-all-there-exists` | ok, 14 checks, quiz 4/4 |
| `--lesson proof/l5-saying-the-opposite` | ok, 14 checks, quiz 4/4 |
| `--set proof/review-1` | ok, 9 of 9 recorded |
| `--set proof/homework-1` | ok, 8 of 8 right, 36 of 36 marks |

Layout fixes made after looking at the screenshots: venn labels shortened to plain text (KaTeX in a label printed raw `$P$` and long labels ran past the frame); venn capped at `maxHeight: 200` where a table widget follows; the four-card boxes set to `size: "large"` with 2 columns (four cards in one row were tiny on a phone); the hedge and audit grids draw ✓ and × as centred marks instead of cell text, which was too small; the code starter's comment line shortened so it does not scroll.

## Numbers, each computed twice

First pass: `checks.py` from the brief's data. Second pass: recomputed from the written JSON files (cell text parsed back to numbers) and by hand.

- $91 = 7 \times 13$; $91 \div 7 = 13$ (Python 91/7 and 7*13). $57 = 3 \times 19$ (digit sum 12; 3*19).
- $2^{10} = 1024$ (2**10, and 2 × 512).
- Python `0.1 + 0.2` is `0.30000000000000004`, and `== 0.3` is `False` (CPython).
- Goldbach checked to $4 \times 10^{18}$: Oliveira e Silva, Herzog and Pardi (2014). Not recomputed; it is a cited fact.
- l1 transfer: Rates £9.8m of £61m is 16.07%, Equities £4.1m of £52m is 7.88%; the Equities loss £32,400 is under £50,000.
- l2 alert days: and: Mon, Thu; or: Mon, Tue, Wed, Thu; not above £100: Tue, Fri; neither: Fri; exclusive or: Tue, Wed.
- Truth tables: P ∧ Q is T, F, F, F; P ∨ Q is T, T, T, F; ¬(P ∧ Q) and ¬P ∨ ¬Q are F, T, T, T; the wrong form ¬P ∧ ¬Q agrees on 2 of 4 rows; three letters need $2^3 = 8$ rows.
- l2 transfer flags: A (£2.5m, unrated) T, B (£0.4m, unrated) T, C (£1.8m, rated) T, D (£0.6m, rated) F.
- `same_truth_table`: the solution passes all 7 hidden tests and the starter (`pass`, returns `None`) fails all 7 (checked in CPython; the solution also passes in the playthrough).
- P ⇒ Q is T, F, T, T; converse T, T, F, T; contrapositive T, F, T, T; inverse T, T, F, T.
- Four-card answers: £12,000 and 1 signature; review: Market and 4:20pm; transfer: £18,000 and Allowed.
- Whole numbers 1 to 12: multiples of 4 are 4, 8, 12; even non-multiples 2, 6, 10; odd 1, 3, 5, 7, 9, 11. Converse counterexamples 2, 6, 10; the smallest is 2.
- l4 grid: witnesses `r1c3`, `r2c4`, `r3c4`, `r4c2` (exactly one cell above 100 per row); 13 positive cells; Thursday breakers `r1c4` (−20) and `r4c4` (95); no column has all four above 100 (Thursday has 2 of 4); the trap's shaded cells `r1c1`, `r1c2`, `r2c3`, `r1c4`, `r1c5` are each at most 100, one per column.
- Hedge grid: every scenario column has a tick and every hedge row has a cross; H1 fails "Rates down".
- l4 quiz: $n^2 \ge n$ for every integer (cases $n \le 0$ and $n \ge 1$); $3^2 = 9$.
- l5 trades: unprofitable trades T3 (£0) and T5 (−£80); worst loss £80, under £500.
- Review weeks grid: week 3 is the only week where all three stocks rose; ∀s ∃w true; ∀w ∃s false (week 2); ∃s ∀w false. Review witness $3x = 12$ gives 4.
- Homework desks grid: desk A's only shared profit day is Wednesday, desk B's is Tuesday; no day has all four traders positive; ∀k ∀d ∃t is true; ∀k ∃t ∀d is false.
- P ⇒ (Q ⇒ P) is T on all four rows; Q ⇒ P column T, T, F, T.
- Longform example: £25m is more than half of £40m (£20m), so that desk did not halve.

No number failed its double check.

## Departures from the brief

- l1: the hook asks "tap every sentence that has to be either true or false" so the learner can sort before the term is named. The trap ("91 is prime") is its own screen as well as a `byKey` line on the hook.
- l2: the 8-row `numeric` and "which trade would a junior who reads or as exclusive miss" are quiz items; the transfer screen grades the flag column. The "do these two columns agree" check is carried by the De Morgan table fill and its explanation; the generalise screen's choice asks for the partner law ¬(P ∨ Q) instead. The optional `code` screen is included, with the brief's four tests plus three more.
- l3: the converse counterexample is a `choice` (4, 6, 7, 12; answer 6) in the lesson and a `numeric` for the smallest counterexample (2) in the quiz. The margin-rule contrapositive is quiz item 1; the transfer screen is the card tap.
- l4: the function rule from `functions` l4 is a `table` screen (input 2 with two outputs, a shared output as the distractor).
- l5: the hook is `tap-regions` in count mode with `among` the break-even and the losing trade, because both refute "every trade was profitable"; the brief's "single row" would make one correct refutation wrong. The trap screen sits before the `manipulate` and `place` screens, because the validator warns about canvas-free task screens before the trap. The limit negation in the lesson is `place` (order mode) with distractor chips; the `order` with `distractors` version is homework item 6.
- Table-widget cells name misconceptions by cell id in `byKey`, not by `wrong[]` ids (see the backlog bullet).

## Proposed course.json change

None.

## Conventions

No datasets or seeds. Money in £ throughout. Truth values T and F; the course notation from the brief (∧, ∨, ¬, ⇒, ⇔, ∀, ∃, ℝ, ℤ, $u_n$, $L$, ε, $N$).
