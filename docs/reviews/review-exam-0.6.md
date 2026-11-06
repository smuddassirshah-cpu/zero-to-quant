# Topic 0.6 exam: second-reader findings

Scope: `app/content/exams/topic-0.6.json` (id `topic-0.6`, 60 minutes, pass 0.7, 24 items over `proof` L1 to L3), read in full against `docs/reports/exam-0.6.md`, `docs/AUTHORING.md` sections 5 and 6, `proof/course.json` and every lesson's `skills`, and the engine's `order` (`same`), `table` and numeric `accept` handling.

Method: ran the author's scripts; flattened the exam and read every string; recomputed every key, every `wrong` value and every stated number by a second route (truth tables by enumeration, set inclusion by brute force over all subsets of a 3-element set, SymPy for each algebra line and induction step, primality by `sympy.isprime`, sums by direct addition to $n = 29$); read every order line in the keyed order; measured visible option lengths; ran a fuzzy match of every exam string against every `proof` lesson, review and homework string; ran the validator and the voice scan on a scratch copy.

Scratch scripts (not committed): `/tmp/claude-0/-home-user-zero-to-quant/563c2e64-8acc-5553-b27e-d47f109c8bd3/scratchpad/rev0626/` (`flat.py`, `recompute06.py`, `opts.py`, `near.py`, `grepc.py`).

Format: `n. item [index] path | severity | problem | evidence | fix`. Severities: wrong, misleading, coverage, voice, layout.

## Script results

- `python3 -I docs/briefs/exam-0.6-scripts/check_numbers.py`: 141 of 141, exit 0. No "check by hand" lines.
- `python3 -I docs/briefs/exam-0.6-scripts/fresh.py`: runs, 47 lines. No keyed number or distinctive phrase recurs in `proof` except the converse notation ($Q \Rightarrow P$, in l3, l11 and homework-1), "$a + b$ is irrational" (l14, a different claim) and `16k^2` (analysis). The rest are common numbers in unrelated courses.
- My recompute: 34 of 34 checks pass.
- Validator: `0 errors, 2311 warnings`; no line names topic-0.6.
- Voice scan (copy of the exam only): 570 sentences, 0 over 20 words, 0 explanations over three sentences. No `!`, em-dash, en-dash or American spelling.

## What the author's scripts do not check

- Freshness by setup or by wording. `fresh.py` searches a few phrases per item, so it misses a copied item (finding 1) and a reused trick with a new constant (finding 2).
- Whether each `why` names a real learner action (findings 3 and 6) and whether a distractor contradicts the stem (finding 4).
- Key length against distractors (finding 5) and Stage 0 pitch (findings 7 and 8).
- Proof validity beyond the ids. I read every order line: each keyed order is a valid proof, each left-out line is flawed for the reason its `why` gives, and the `same` sets are right ([11] s3 and s4, the two cases; [22] s2 and s3, the even and odd cases). [20] needs no `same`: s1 introduces $x$, and s2 to s4 chain.

## Findings

1. `e-converse-table` [6] whole item | coverage | Not fresh: a verbatim copy of `l3-if-then` screen 5. Same five columns, same given column, same editable cells and answers, the same slip text on the T, F row and the same explanation. | `l3-if-then.json` screens[5]: columns `$P$, $Q$, $P \Rightarrow Q$, $Q \Rightarrow P$, $\lnot Q \Rightarrow \lnot P$`, question "Fill in the converse and the contrapositive.", explain "The contrapositive reads T, F, T, T, the same as $P \Rightarrow Q$. The converse reads T, T, F, T". The exam's `byKey.tf-contra` matches l3's word for word (fuzzy ratio 1.0). | Replace the two editable columns with the inverse and the negation (taught in l3 and l5, never tabled). Title "The inverse and the negation"; tags `truth-table`, `negation`; d3, pace 120 unchanged. Prose: "The column $P \Rightarrow Q$ is given. Fill the inverse $\lnot P \Rightarrow \lnot Q$ and the column $P \land \lnot Q$." Question unchanged. Columns `$P$, $Q$, $P \Rightarrow Q$, $\lnot P \Rightarrow \lnot Q$, $P \land \lnot Q$`. Answers by row (TT, TF, FT, FF): inverse T, T, F, T; $P \land \lnot Q$ F, T, F, F. Slips: rows[2][3] `wrong` `{ "id": "ft-inverse", "text": "T" }`, byKey "On the F, T row, $\lnot P$ is T and $\lnot Q$ is F, so the inverse is F."; rows[2][4] `imp-not-ft` and rows[3][4] `imp-not-ff`, each text "T", each byKey "You read it as $P \Rightarrow \lnot Q$. An "and" is T only when both parts are T." `feedback.correct`: "$P \land \lnot Q$ is the opposite of $P \Rightarrow Q$ on every row. The inverse matches the converse instead." `feedback.generic`: "An implication is F only where its hypothesis is T and its conclusion F. An "and" is T only where both parts are T." Explain: "The inverse reads T, T, F, T, the same as the converse, not as $P \Rightarrow Q$. $P \land \lnot Q$ reads F, T, F, F, the opposite of $P \Rightarrow Q$ on every row. So it is the negation of the implication." Recomputed by enumeration: inverse 1, 1, 0, 1; $P \land \lnot Q$ 0, 1, 0, 0; $P \Rightarrow \lnot Q$ 0, 1, 1, 1 (differs on the F, T and F, F rows, where the slips sit). Update `check_numbers.py`.

2. `e-prime-formula` [17] whole item | coverage | Near reuse of l14's "prime machine". l14 screens 0 and 1 run $n^2 + n + 41$ to its failure at $n = 40$, where $n^2 + n = 40 \times 41$. This item only swaps 41 for 17 (failure at $n = 16$, $16 \times 17 + 17 = 17^2$), and `feedback.generic` hands over the same trick. A learner who recalls the lesson answers without testing a case. | `l14-counterexamples.json` screens[1] explain: "$40^2 + 40 + 41 = 40 \times 41 + 41 = 41 \times 41 = 1681$". Exam generic: "Try a value of $n$ that makes both $n^2 + n$ and 17 multiples of 17." | Use $n^2 + n + 77$, where the lesson's trick gives a wrong answer and the smallest counterexample needs a search. Prose: "Claim: for every whole number $n \ge 1$, the number $n^2 + n + 77$ is prime. At $n = 1$ it gives 79." `answer` 6. Wrongs, all `tol.abs` 0: `value` 119 ("119 is the value at the counterexample. The question asks for $n$, which is 6."); `trick` 76 ("$n = 76$ gives $77^2$, but it is not the smallest. Test small $n$ first: $n = 6$ gives $119 = 7 \times 17$."); `early` 5 ("At $n = 5$ the value is 107, which is prime. Try one more."); `zero` 0 ("The claim starts at $n = 1$, so $n = 0$ is not a case of it."). `feedback.correct`: "At $n = 6$ the value is $119 = 7 \times 17$, not prime. Every $n$ from 1 to 5 gives a prime." `feedback.generic`: "Test $n = 1, 2, 3, \dots$ in turn, and try small primes as factors." Explain: "The values for $n = 1$ to 5 are 79, 83, 89, 97 and 107, all prime. At $n = 6$ the value is $36 + 6 + 77 = 119 = 7 \times 17$. One failure refutes the "for every"." Recomputed: values 79, 83, 89, 97, 107 prime by `isprime`; $f(6) = 119 = 7 \times 17$; $f(76) = 5929 = 77^2$; $f(0) = 77 = 7 \times 11$. No 119 or "+ 77" in `proof`. d4 and pace 150 can stay (six cases and a trap).

3. `e-exp-onto` [10] `widget.options[3].why` (`neither`) | misleading | The why names an action that leads the other way. "You tested one-to-one by a picture of a curve" describes the horizontal-line test, which shows $e^x$ is one-to-one. The real slip is to find the missed output and then mark both tests failed. | Option text "Neither one-to-one nor onto." | "You saw that $-1$ is never reached and stopped there. $e^a = e^b$ still forces $a = b$, so $g$ is one-to-one."

4. `e-step-no-base` [15] `widget.options[2]` (`bad-step`) | misleading | A dead distractor. The stem says "The step is valid.", and this option says the step is wrong, so a careful reader rules it out from the stem alone. | Question: "The step is valid. What does the argument show?"; option "The step is wrong, since you cannot add 1 to both sides of an inequality." | Replace it with id `from-two`, text "The claim fails at $n = 1$ but holds from $n = 2$, since the step carries it on.", why "You let the step carry truth from a false case. At $n = 2$ the claim reads $3 < 2$, also false." Explain unchanged. Visible lengths stay in range (key 82, this 73).

5. `e-odd-direct` [12] `widget.options` | misleading | The key is the longest option by a clear margin, so length points to it. | Visible lengths without LaTeX markup: key 95, distractors 70, 67 and 52. | Key `right`: "$mn + m + n = 4ab + 4a + 4b + 3 = 2(2ab + 2a + 2b + 1) + 1$, twice an integer plus 1." `same`: "Write $m = n = 2k + 1$. Then $mn + m + n = 4k^2 + 8k + 3 = 2(2k^2 + 4k + 1) + 1$, which is odd." `example`: "With $m = 3$ and $n = 5$: $15 + 3 + 5 = 23$. With $m = 7$ and $n = 9$: $63 + 7 + 9 = 79$. Both are odd." `gap` unchanged. New lengths 83, 89, 91, 67. Whys unchanged (the `example` why already says "You checked one case"; change it to "You checked two cases."). Algebra rechecked by SymPy: both identities expand to 0.

6. `e-log-contradiction` [19] `widget.options[2].why` (`bigger`) | misleading | "You stated a false fact" names no learner action. | Option "$2^p > 3^q$ for all positive $p$ and $q$." | "You compared sizes, as if one side must be bigger. $2^1 < 3^1$ but $2^2 > 3^1$, so size settles nothing."

7. `e-exp-onto` [10] `prose` | voice | Stage 0 pitch: "log return" is not taught in `exp-log` (topic 0.3) or `proof`, and is not needed. | grep "log return" over `exp-log` and `proof`: 0 hits (it first appears in `limits` and `backtest`). | Prose: "A price is multiplied by $g(x) = e^x$ when its natural log rises by $x$. Take $g : \mathbb{R} \to \mathbb{R}$." (`exp-log` l10 teaches the natural log.)

8. `e-functions-count` [7] `feedback.byKey.product` and `e-negate-desk` [5] `feedback.correct` | voice | Symbols the item never defines. [7] says "the pairs in $A \times B$", but the item has no $A$ or $B$. [5] writes $F(d)$ and $C(d, n)$ with no key. | Texts as quoted. | [7]: "You took $3 \times 4 = 12$. That counts the (order, venue) pairs, not the functions." [5]: "Some FX desk has a night with no one on call. That one desk breaks the claim."

9. whole exam | coverage | Near relatives with new numbers, all acceptable. No change. [18] (`2^n \ge 7n`, smallest $n_0 = 6$, true case at $n = 0$) follows l13 screen 7 and homework-3 item 3 ($2^n > n^2$ from $n_0 = 5$, true case at $n = 1$), with a new inequality and a new step condition. [9] reverses a fee as homework-2 item 5 reverses $g(8) = 33$. [7] and [8] follow l8 and l9 counts with new sizes (64, 120 against l9's 24 and 6). [22] works squares mod 4 where homework-3 item 5 works squares mod 3. [4] follows l4 and review-1 witnesses with a new equation. | `near.py` fuzzy matches above 0.7, each read. | None.

## Checks with no finding

- Every key and every `wrong` recomputes: 32, 10, 25; kept; 3, 4, 2; 30, 39, 21; $-3$, 3, 0.5; the negation; the two table columns; 64, 81, 12; 120, 216, 20; 15, 14.1, 21.25; the element chase holds for all 512 triples of subsets of $\{0, 1, 2\}$; $4ab + 4a + 4b + 3$ and $4k^2 + 8k + 3$; the averages; $b = s - a$ and $\sqrt2 + (1 - \sqrt2) = 1$; $2 < 1$ and $3 < 2$; $n = 2$ refutes the converse claim; 16, 289, 257, all fifteen values prime; $2^n < 7n$ exactly for $n = 1$ to 5, the step for $k \ge 1$; parity of $2^p$ and $3^q$; $(x - 1)^2 \ge 0$ route; 3,080, 9,240, 2,870, both step identities; no $4m + 3$ below 400 is a sum of two squares, squares mod 4 are 0 and 1; the weighted sum identity for $n = 1$ to 29, 98 at $n = 4$, the step identity.
- Maths and hypotheses: every general claim carries its domain ($x > 0$ for the division, $p, q \ge 1$ for the parity, $k \ge 1$ for the step, $n \ge 1$ where it matters). Each order item's keyed order is a valid proof.
- Choice items: all `shuffle: true`, every distractor has a `why`. Only finding 5 is a length cue ([14] key 109 against 88 is within 1.3 times). [16] "the first line" means the write-up's first line, not an option place.
- Longform [23]: rubric 1, 1, 2, 2, 2, 1, 1 sums to 10; each row matches a step of the model answer; the model states method, base case, the fixed-$k$ assumption, the step with reasons, the conclusion and the $n = 4$ check. Fair to an alternative collection of terms, since rows 4 and 5 name the result, not the route.
- Tolerances: all integer keys `tol.abs` 0; [9] 0.01 around 15 catches 15 and 15.0; [4] `added` 0.5 is not an integer, so no clash with the key band. No wrong band overlaps its answer band.
- Coverage: the six skills equal `proof/course.json`; each is on an auto-graded item (pv-writing on [16], [20], [22]). Levels L1 5, L2 7, L3 12, each with a skill first met there. Ramp 5, 12, 5, 2 (21, 50, 21, 8%).
- Pace: 3,150 s = 52.5 minutes of 60, with 600 s for the longform and 300 s for the d5 order item.
- Stage 0 pitch: apart from findings 7 and 8, every term is taught in `proof` or earlier Stage 0 courses ($e^x$, $\ln$, $\log_2$ from `exp-log`; one-to-one, onto, witness, contrapositive, inverse from `proof`).

## Counts

- Wrong: 0.
- Misleading: 4 (findings 3 to 6).
- Coverage: 3 (findings 1, 2 and 9; 9 needs no change).
- Voice: 2 (findings 7 and 8). Layout: 0.
- Author's scripts: `check_numbers.py` 141 of 141, exit 0; `fresh.py` clean in `proof` by keyed number. Validator 0 errors, no topic-0.6 warning. No engine change needed.

## Fix pass

Edits by `docs/briefs/exam-0.6-scripts/build.py`, regenerated into `app/content/exams/topic-0.6.json`; `check_numbers.py` and `fresh.py` updated for each change. Every changed key and slip recomputed by enumeration.

1. fixed: [6] replaced by the inverse and negation table as proposed. Inverse T, T, F, T; $P \land \lnot Q$ F, T, F, F; $P \Rightarrow \lnot Q$ T on the F, T and F, F rows, where the slips sit. Tags now `truth-table`, `negation`.
2. fixed, with a departure: [17] no longer uses a prime formula at all, since l14 and l12 own that setup. New claim: $10n^2 + 1$ is never a perfect square. Values 11, 41, 91, 161, 251 are non-squares; $n = 6$ gives $361 = 19^2$. Answer 6; slips 361 (value), 19 (root), 5 (early, 251 lies between $15^2$ and $16^2$). No claim of this kind in `proof` (l14 only has "a perfect square is even").
3. fixed: [10] `neither` why now names the real slip.
4. fixed: [15] dead distractor replaced by `from-two`.
5. fixed: [12] key shortened, distractors lengthened (83, 89, 91, 67 visible characters as proposed); `example` now checks two cases (3, 5 and 7, 9: 23 and 79).
6. fixed: [19] `bigger` why names the comparison ($2^2 > 3^1$ recomputed).
7. fixed: [10] prose no longer says "log return".
8. fixed: [7] and [5] feedback no longer use undefined symbols.
9. no change needed, as the review says.

Gates: validator 0 errors, no warning naming topic-0.6; voice scan on a copy 0 long sentences, 0 long explanations, no `!` or dashes; `check_numbers.py` 150 of 150, exit 0 (`check_wrongs()` then `report()`); `fresh.py` runs, no keyed number or phrase of the new items in `proof`; playthrough `--exam topic-0.6` green (24 of 24) with and without `--mobile`.
