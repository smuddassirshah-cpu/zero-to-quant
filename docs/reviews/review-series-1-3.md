# Series levels 1 to 3 (Sequences; Series; Binomial expansion and applications): second-reader findings

Scope: `app/content/courses/series/` l1 to l13, `review-1` to `review-3`, `homework-1` to `homework-3` (the whole course). There is no `docs/briefs/series.md` and no `docs/reports/series-<n>.md`: the course predates the brief and report system, so the read works from the files, `course.json` and the prerequisite map in `docs/reports/prereq-mapping.md`. No level outside the course depends on a series screen by path, so the continuity skim covers cross-references inside the course and the levels series requires (`equations`, `number-sense`, `counting`, `ratio`).

Stage 0, for a GCSE-entry learner. Two extra checks: a step that uses knowledge not taught in the course or in its gating closure (`node tools/closure.mjs --target series/L<n>`), and notation that differs from UK GCSE and A-level usage (nth term, sigma notation, arithmetic and geometric series, sum to infinity, convergence wording).

Method: I read every screen, quiz item, review and homework item, every `why`, `byKey`, hint and explanation. Every graded key, every `wrong[]` value and every number in prose was recomputed two ways in three committed scripts. Method 1 builds terms one at a time, adds terms one by one (with `Fraction` where exact), builds Pascal's triangle by addition, expands brackets by polynomial multiplication, or adds discounted payments one by one. Method 2 uses the closed forms. Each convergence, sum and "always/never" claim was checked numerically (partial sums to n = 200 or more, brute force over every pick) and by derivation. There are no code items in the course. All seven expression items were graded on the real `js/engine/grade.js` and `expression.js` with the local Compute Engine 0.30.2, against equivalent forms a learner would type and against each listed slip. Option-position wording was swept with a regex over every `why`, explanation, hint and feedback line. Freshness: key nouns of every review and homework item were grepped across `app/content`.

Tool results:
- `python3 docs/reports/series-L1-numbers.py`: exit 1, 284 of 290. The 6 failures are content faults (findings 1, 2, 3, 4, 8, 9). Fixed content passes them. 80 "check by hand" lines, each read: all fine.
- `python3 docs/reports/series-L2-numbers.py`: exit 1, 287 of 293. The 6 failures are content faults (findings 5, 13 (two checks), 15, 16, 17). 57 "check by hand" lines, each read: only review-2 `plus` is wrong (finding 5).
- `python3 docs/reports/series-L3-numbers.py`: exit 1, 299 of 302. The 3 failures are content faults (findings 6, 7, 19). 97 "check by hand" lines, each read: only review-3 `pct` is wrong (finding 6).
- `cd app && node tools/validate.mjs`: 0 errors. 12 series warnings:
  - 6 key-length: l2 `screens[4]`, l8 `screens[5]`, l12 `screens[4]`, `screens[6]` and review-2 `items[8]` are real giveaways (finding 26). l13 `screens[2]` is a false positive: the validator measures LaTeX source, and `\dfrac{1}{1.05}` renders about as wide as `1.05` (Engine).
  - 3 O2-explain-answer: l3 `screens[9]`, review-3 `items[8]` and homework-2 `items[3]` (findings 30, 6, 31).
  - 2 O2-long-sentence and 1 O2-long-explain, all under the 35-word gate: l6 `screens[3]` and l13 `screens[6]` (finding 29).
- `VOICE_BASE=app/content/courses/series python3 docs/reviews/voice-scan.py 35`: 0 sentences over 35 words. 2 explanations over three sentences: l6 `screens[3].explain.text` and l8 `screens[5].widget.options[0].why` (finding 29). My own sweep found no exclamation marks, no em-dashes, no American spellings ("center" is a canvas `align` value) and no `$` money.
- Playthroughs, all with `--local-cdn <scratchpad>/pkgs`, desktop and `--mobile`: every lesson `ok` (13 or 14 checks each, quiz 4/4). review-1 to review-3: `ok`, 9 of 9 recorded. homework-1 to homework-3: `ok`, every item right, every longform marked. 38 runs, all green.
- Screenshots: 12 sampled at 440 px (bars, area, grid, tree, number line, plane, long options). One layout fault: zero bars labelled "£0.00" on the asked quantity (finding 28). The others are clean.
- Expression grader (`grade.js` + Compute Engine 0.30.2, a Node harness kept in the scratchpad):
  - Each key accepts the equivalent forms tried: `5\times3^{n-1}`, `\frac{5}{3}\cdot3^n`, `17-4(n-1)`, `17+(n-1)(-4)`, `\frac{192}{2^n}`, `3\cdot2^{6-n}`, `5+4(k-1)`, terms in any order, `1+5(-2x)+10(-2x)^2`.
  - Each listed slip returns its key.
  - `form: "expanded"` returns `form` for `(x+3)^3`, `(x+3)(x^2+6x+9)` and `(2x-1)^4`.
  - Every answer typed as an equation is graded wrong (Engine).
  - homework-2 `items[6]` accepts `\frac{27}{99}` although it asks for lowest terms. It also accepts `0.\overline{27}` retyped from the prompt (finding 23, Engine).

Format: `N. file | JSON path | severity | problem | evidence | exact fix`. Severities: wrong, misleading, voice, layout, continuity.

## Findings

1. l1-spotting-the-rule.json | `screens[6].widget.options[3].text`; `screens[6].explain.text` | wrong | The option "10, 8, 6, 4, …" is offered as "the sequence itself" of term $= 10 - 2n$, but $10 - 2n$ gives 8, 6, 4, 2. The explanation's "Both rules describe the same sequence" does not say which two of the three rules it means. | $n = 1, 2, 3, 4$ give 8, 6, 4, 2 (L1 script, `stated` check). | Option text: "8, 6, 4, 2, …". Explain: "$10 - 2n$ needs only the position: term 100 is $10 - 200 = -190$. The other rules need the term before. Starting at 8, subtract 2 from the last term gives the same sequence 8, 6, 4, …."

2. l3-multiplying-each-time.json | `screens[5].widget.wrong[2]` (`add`, −26) | wrong | −26 matches no slip for $u_6$. It is $u_4$ plus the first gap, −24, which is a value for $u_5$. The line "You followed the gaps rather than the ratio" names no action. | Gaps are −24, 12, −6. Repeating the last gap gives $-2 - 6 - 6 = -14$. | `"value": -14`. `byKey.add`: "You subtracted the last gap, 6, twice: $-2 - 6 - 6 = -14$. The gaps shrink and flip sign: each term is $-0.5$ times the one before."

3. l3-multiplying-each-time.json | `screens[5].widget.wrong[3]` (`times-two`, −32) | wrong | Multiplying by −2 from $u_4 = -2$ gives 4, then −8, not −32. The line names a slip that cannot produce the stored value. | $-2 \times (-2) \times (-2) = -8$. | `"value": -8`. `byKey.times-two`: "You multiplied by $-2$: $-2 \times (-2) = 4$, then $4 \times (-2) = -8$. Dividing, $-8 \div 16 = -0.5$, so each term halves and flips sign."

4. l4-last-step.json | `screens[2].widget.wrong[2]` (`order`, 4) | wrong | The slip "subtract 3 before doubling", used as a rule, gives 5, 4, 2, −2. So its $u_4$ is −2. The stored 4 is the slip's $u_2$. | $2(5 - 3) = 4$, $2(4 - 3) = 2$, $2(2 - 3) = -2$. | `"value": -2`. `byKey.order`: "You subtracted 3 before doubling: $2 \times (5 - 3) = 4$, then 2, then $-2$. The rule doubles first, then subtracts 3."

5. review-2.json | `items[7].widget.wrong[2]` (`plus`, 1.7857) | wrong | The line says "You divided by $1 + 0.6$". That gives 1.5625. The stored 1.7857 is $2.5 \div 1.4$. | $2.5 / 1.6 = 1.5625$ (L2 script). | `"value": 1.5625` (keep `tol` 0.005).

6. review-3.json | `items[8].widget.wrong[1]` (`pct`, 25); `items[8].explain.text` | wrong | "You divided by 4 and by 5" gives $25 - 20 = 5$, not 25. The explanation never states the answer, £500.00 (validator O2). | $100/4 - 100/5 = 5$ (L3 script). | `"value": 5`. `byKey.pct`: "You divided by 4 and by 5, not 0.04 and 0.05: $25 - 20 = 5$." Explain: "At 5% the value is $\tfrac{100}{0.05} = \text{£}2{,}000.00$; at 4% it is $\tfrac{100}{0.04} = \text{£}2{,}500.00$. That is a rise of £500.00, or 25%. Far-off payments gain the most from the cut."

7. l11-powers-of-a-bracket.json | `screens[6].explain.text` | wrong | "$(a + b)^n$ is never just $a^n + b^n$ once $n \ge 2$ and both parts are non-zero" is false for numbers. The mixed terms can cancel. | $a = 1$, $b = -1$, $n = 3$: $(1 - 1)^3 = 0 = 1^3 + (-1)^3$ (L3 script, `stated` check). | Third sentence: "So the expansion of $(a + b)^n$ always has mixed terms once $n \ge 2$, and $a^n + b^n$ drops them."

8. l3-multiplying-each-time.json | `screens[2].explain.text`; `screens[2].feedback.generic`; `screens[2].feedback.correct` | wrong | "Straight means add, curving means multiply" (and "Curving dots multiply") states a false converse. The squares 1, 4, 9, 16 curve and have no common ratio. l1 `screens[4]` and this lesson's `quiz[3]` both show them. | $4/1 \ne 9/4$ (L1 script, `stated` check). | Explain: "A rises by 3 every step, so its dots lie on a line: arithmetic. B's rises grow, 1 then 1.5 then 2.25, and each term is 1.5 times the last: geometric. A curve hints at multiplying, but only a common ratio proves it." Generic: "Not quite right. Straight dots add a fixed amount. Check which set multiplies by the same number each step." Correct: "B multiplies by 1.5 each step, so its dots curve upwards."

9. l4-last-step.json | `quiz[3].explain.text` | misleading | "The multiplier must lie between −1 and 1 for terms to settle" is false for a start at the fixed point. `screens[1].explain.text` says so itself: "Start at 20 and every term is 20". | $u_{n+1} = 2u_n - 10$ with $u_1 = 10$ stays at 10 (L1 script, `stated` check). | Third sentence: "Unless they start at the fixed point, terms settle only when the multiplier lies between −1 and 1."

10. l4-last-step.json | `screens[5].prose` | continuity | "Fixed point" is used in `screens[9].explain.text`, in `quiz[3]` (two `why`s) and in finding 9's fix, but is never named. The prose says only "left alone". | No bold **fixed point** anywhere in the course. | "Now $u_{n+1} = 2u_n - 10$ with $u_1 = 12$. The rule leaves 10 alone, since $2 \times 10 - 10 = 10$, so 10 is a **fixed point**."

11. l1-spotting-the-rule.json | `screens[2].feedback.byKey.sign` | misleading | "You took 3 from 1 and dropped the minus sign" gives 2, not the stored 5. The slip is writing −5 as 5. | $1 - 3 = -2$. | "You dropped the minus sign. The list keeps falling below zero: 1, −2, −5."

12. l1-spotting-the-rule.json | `quiz[1].explain.text` | continuity | "It is both kinds of sequence at once" refers to kinds of sequence the lesson has not named. Arithmetic is named in l2, geometric in l3. This lesson named two kinds of rule. | l1 bolds only term, term-to-term rule, position-to-term rule, sequence. | "A list that never changes fits both rules. Add 0 and multiply by 1 each send 7 to 7. This edge case returns later: a constant list adds a fixed step and multiplies by a fixed number."

13. l7-shifted-copy.json | `screens[4].feedback.byKey.forever`; `quiz[1].widget.options[1].why` | misleading | "96 is what the halving terms approach" and "2 is what the halves approach" confuse terms with totals. The terms shrink to 0; the total approaches 96 (or 2). The next lesson rests on exactly this distinction. | $48 \times 0.5^{n} \to 0$; $48 + 24 + \dots \to 96$ (L2 script, `stated` checks). | `byKey.forever`: "96 is what the total approaches if the halving goes on forever. This sum stops after five terms." `why`: "2 is what the total approaches if the halving goes on forever. This sum stops after six terms."

14. l7-shifted-copy.json | `screens[8].hints[2].text`; `screens[8].feedback.correct` | misleading | The step hint jumps from $a = 480.77$, $r = \tfrac{1}{1.04}$ to $\tfrac{500}{0.04}(1 - 1.04^{-10})$. It never shows $\tfrac{a}{1 - r} = \tfrac{500}{0.04}$. It also uses the negative index $1.04^{-10}$, which no prerequisite teaches beyond $10^{-k}$ (number-sense l14). | $\tfrac{500/1.04}{0.04/1.04} = 12500$. | Hint: "$a = \tfrac{500}{1.04}$, $r = \tfrac{1}{1.04}$, $n = 10$. Then $\tfrac{a}{1 - r} = \tfrac{500}{0.04} = 12500$ and $r^{10} = \tfrac{1}{1.04^{10}}$, so $S = 12500\left(1 - \tfrac{1}{1.04^{10}}\right) = 4055.45$." Correct: "$\dfrac{500}{0.04}\left(1 - \dfrac{1}{1.04^{10}}\right) = 4055.45$."

15. l8-adding-forever.json | `screens[1].explain.text` | misleading | "You saw the sums settle for $r = 0.5$, $0.9$ and $-0.5$". At 0.9 the ten dots reach only 6.51 against a limit of 10, so nothing on screen settles. | $S_{10} = \tfrac{1 - 0.9^{10}}{0.1} = 6.51$ (L2 script). | "You saw the sums level off for $r = 0.5$ and $-0.5$; at $0.9$ they were still climbing slowly towards 10. At $r = 1$ they climb for ever, and at $r = -1$ they flip between 1 and 0. Settling needs the terms to shrink, so $-1 < r < 1$."

16. l8-adding-forever.json | `summary.formula.note` | misleading | "Outside that range the formula gives a number" is false at $r = 1$, where it divides by 0. | $\tfrac{a}{1 - 1}$ is undefined. | "Outside that range the formula may still give a number, but the series has no sum."

17. l8-adding-forever.json | `quiz[1].explain.text` | misleading | "A recurring decimal is a geometric series" overclaims. $0.1666\ldots$ is $\tfrac{1}{10}$ plus a geometric series. | $0.1\dot{6} = 0.1 + \tfrac{0.06}{1 - 0.1}$. | Last sentence: "This recurring decimal is a geometric series."

18. l8-adding-forever.json | `screens[6].explain.text` | misleading | "Only the first two are strictly between −1 and 1" names options by place in a shuffled `multi` (shuffle is on by default). | `screens[6].widget` has no `shuffle: false`. | "The ratios are 0.8, −0.9, −1, 1 and 1.5. Only 0.8 and −0.9 lie strictly between −1 and 1. Their sums are $\tfrac{5}{0.2} = 25$ and $\tfrac{10}{1.9} \approx 5.26$."

19. l11-powers-of-a-bracket.json | `screens[5].feedback.byKey.wrong-k` | misleading | The stored 32 comes only from $k = 3$. $k = 1$ gives 8, so "You used $k = 1$ or $k = 3$" misdescribes the slip. | $\binom{4}{1} \times 2 = 8$; $\binom{4}{3} \times 2^3 = 32$ (L3 script). | "You used $k = 3$: $\binom{4}{3} \times 2^3 = 32$, but that term is $\tfrac{32}{x^2}$. The powers of $x$ cancel only at $k = 2$."

20. l12-small-x.json | `screens[8].explain.text` | misleading | "Early on, the two balances differ only by this small term" is too strong. The gap is £166.53, and the term gives £160.00. | $10000(1.04^5 - 1.2) = 166.53$. | Second sentence: "Early on, the two balances differ by little more than this term."

21. l2-any-term.json, review-1.json | (prerequisite) | continuity | The level solves linear equations and a linear inequality that no level in its gating closure teaches. The closure is equations/L1 (Expressions) and number-sense L1 to L3. Examples: l2 `screens[4]` ($3n + 2 = 100$), `quiz[3]`, l4 `screens[7]` and `screens[9]` ($L = 1.01L - 200$, unknowns on both sides), l2 `screens[9]` and review-1 `items[7]` (an inequality). | `node tools/closure.mjs --target series/L1`: courses equations, number-sense; equations L2 and L3 are outside it. | Orchestrator item A below.

22. l3-multiplying-each-time.json, l4-last-step.json | (prerequisite) | continuity | Percentage multipliers are assumed before series teaches them: "Rising by 5% means multiplying by what?" in l3 `screens[8].hints[0]`, the 1% plans in `screens[9]`, and the 1% loans in l4 `screens[8]` and `screens[9]`. They are taught in ratio l4-multipliers, outside the closure. | `ratio/course.json` l4 objective: "Increase or decrease an amount in one step with a decimal multiplier." | Orchestrator item A below.

23. homework-2.json | `items[6].question` | misleading | It asks for the fraction "in lowest terms", but the grader accepts $\tfrac{27}{99}$ (listed in `accept`). `form: "simplified"` cannot refuse it either: Compute Engine reduces the fraction at parse. | Real `grade.js`: `\frac{27}{99}` grades OK with and without `form: "simplified"`. | "What is it as a fraction?" (keep `accept` as it is). The retyped-decimal loophole is under Engine.

24. homework-2.json | `items[2].explain.text` | continuity | "Solving $2n^2 + n = 1000$ gives $n \approx 22.1$" uses the quadratic formula. That is quadratics/L2, outside the series closure, and the item does not need it. | `closure.mjs --target series/L2` has no quadratics. | "$S_n = \tfrac{n}{2}(6 + 4(n - 1)) = n(2n + 1)$. Near 1,000, $2n^2 \approx 1000$ puts $n$ near 22. Check: $S_{22} = 990$ and $S_{23} = 1081$."

25. homework-3.json | `items[3].prose` | continuity | The item multiplies the chances of independent trades, $0.6^3 \times 0.4^2$. Neither series nor its closure teaches that rule: counting l8 covers equally likely outcomes only. l10 `screens[8]` used 32 equally likely sequences instead. | `counting/course.json` l8 objective: "when every outcome is equally likely". | "A strategy wins 60% of its trades, each trade independent of the others. It places 5 trades. For independent trades, multiply the chances: win, win, loss has chance $0.6 \times 0.6 \times 0.4$."

26. l2-any-term.json, l8-adding-forever.json, l12-small-x.json, review-2.json | key options below | misleading | The correct option is the only long one, so its length gives it away (validator key-length; each is real). | Rendered lengths 39 vs 17, 59 vs 29, 76 vs 42, 27 vs 17, 27 vs 2. | Replace the correct option's text:
   - l2 `screens[4].widget.options[3].text`: "No, it is not a term"
   - l8 `screens[5].widget.options[1].text`: "It has no finite value"
   - l12 `screens[4].widget.options[0].text`: "The dropped terms are not small"
   - l12 `screens[6].widget.options[0].text`: "It falls to a quarter"
   - review-2 `items[8].widget.options[0].text`: "None"

27. l8-adding-forever.json, l4-last-step.json | `screens[2].explain.text`, `screens[6].prose` (l8); `summary.ideas[1]` (l4) | continuity | A-level convergence wording is never taught. The course says "settle" throughout. The lesson objective says "converges", homework-2 `items[7].model` uses "converges" and $|r| < 1$, and l8 `screens[7].explain.text` uses $|r| \ge 1$, but no screen names **converge**, **diverge** or the modulus. A-level papers and the formula booklet write "$S_\infty = \tfrac{a}{1-r}$, $|r| < 1$" and "the series converges". | Grep: "converge" appears in learner text only in homework-2's model; $|r|$ only there and in l8 `screens[7]`. | l8 `screens[2].explain.text` last sentence: "The level the partial sums settle on is the **sum to infinity**, $S_\infty$, and we say the series **converges**." l8 `screens[6].prose`: "Every time the sums settled, $r^n$ shrank to 0, which needs $-1 < r < 1$, written $|r| < 1$. Then $$S_\infty = \frac{a}{1 - r}$$ For $|r| \ge 1$ the series **diverges**: there is no sum to infinity." l4 `summary.ideas[1]`: "If the terms settle at $L$, then $L = f(L)$: solve it to find $L$. A-level says the sequence converges to $L$."

28. l5-sigma.json, l1-spotting-the-rule.json, l4-last-step.json | `screens[1].canvas.params`, `screens[5].canvas.params` (l5); `screens[8].canvas.params` (l1); `screens[0].canvas.params` (l4) | layout | With `showValues`, empty bars print "£0.00" or "0". On these screens the empty bar is the asked quantity: $S_3$ in l5 `screens[1]` reads "£0.00" under the question "What is $S_3$?". | 440 px screenshot `series_l5-sigma-lesson-01-problem-440.png`. `bars.js` line 221 skips the label when `showZero` is `false`. | Add `"showZero": false` to each of the four `canvas.params`.

29. l6-gauss.json, l8-adding-forever.json, l13-stream-of-payments.json | as below | voice | Two explanations run over three sentences (voice scan). Two prose sentences sit at 20 words (advisory O2). |  | 
   - l6 `screens[3].explain.text`: "Along the row the top rises by 1 and the bottom falls by 1, so each column stays at 7. Six columns of 7 make 42, which counts every number twice, so $1 + 2 + \dots + 6 = 21$. This is **Gauss’s pairing trick**."
   - l8 `screens[5].widget.options[0].why`: "You trusted the working. It treats $S$ as a number, but the partial sums $2^n - 1$ grow past every number. Positive terms cannot add to −1."
   - l6 `screens[3].prose`, third sentence: "Each column pairs a term from the start with one from the end, like a row of the rectangle."
   - l13 `screens[6].prose`: "A lease pays £100.00 at the start of each year for 5 years. The first payment is made today. The rate is 5%."

30. l3-multiplying-each-time.json | `screens[9].explain.text` | voice | The explanation never states the answer, £136.50 (validator O2). | | Third sentence: "Both gain £200.00 in month 1, but B's gains then grow, so B leads by £136.50."

31. homework-2.json | `items[3].explain.text` | voice | The answer appears as "nine" in words; the validator looks for 9 (O2). | | Last sentence: "A £5,000.00 bankroll survives 9 losses, and then it is gone."

32. l2-any-term.json, l8-adding-forever.json, l12-small-x.json | `screens[1].prose`, `screens[6].prose` (l2); `screens[0].hints[2].text`, `screens[1].prose` (l8); `screens[1].prose` (l12) | voice | A sentence ends on `\dots$` with no full stop, and the next sentence runs on: "$4, 7, 10, \dots$ Slide to pick a term". | Grep for `\dots$ ` followed by a capital: 5 hits. | Insert a full stop after the closing `$` in each: "…$4, 7, 10, \dots$. Slide…", "…$4, 7, 10, 13, \dots$. Test…", "…$\tfrac18, \dots$. It shrinks…", "…$r^3 + \dots$. Slide $r$…", "…$10x^2 + \dots$. Slide $x$…".

33. homework-1.json | `items[2]` | continuity | The item repeats mental-pressure l10's setup exactly: the same sequence 1, 2, 4, 7, 11, the same doubling trap and the same answer 16. | `grep -rl "1, 2, 4, 7, 11" app/content`: homework-1, mental-pressure l10, fin-ml l5, l8. | `prose`: "A sequence begins $2, 4, 8, 14, 22, \dots$" `answer` 32. `accept`: "32: the gaps are 2, 4, 6, 8, then 10." `wrong`: `{ "id": "add-last", "value": 30 }`, `{ "id": "double", "value": 44 }`. `feedback.correct`: "The gaps grow by 2: add 10 to get 32." `byKey.add-last` (replacing `add4`): "You repeated the last gap, 8. The gaps grow by 2 each time, so the next is 10." `byKey.double`: "You read doubling from 2, 4, 8. But 8 to 14 is not doubling, so the rule is something else." `explain.text`: "The gaps are 2, 4, 6, 8, so the next gap is 10 and the next term is 32. The first three terms looked like doubling; the fourth ruled it out."

34. review-3.json | `items[1]` | continuity | The item repeats counting l4's screen: "From 8 traders, a desk picks 3", with 336 ordered picks and 56 teams. | `counting/l4-choosing-without-order.json`. | `prose`: "A fund manager picks 4 of 9 shares for a basket. Each share gets the same weight." `question`: "How many different baskets are possible?" `answer` 126. `accept`: "126 exactly: $\binom{9}{4} = \tfrac{9 \times 8 \times 7 \times 6}{24}$." `unit`: "baskets". `label`: "Number of baskets". `wrong`: `ordered` 3024, `times` 36, `power` 6561. `byKey.ordered`: "3,024 counts each basket once per order. A basket is the same in any order, so divide by $4! = 24$." `byKey.times`: "You multiplied 9 by 4. The ordered picks are $9 \times 8 \times 7 \times 6$." `byKey.power`: "$9^4$ lets the same share be picked four times." `feedback.correct`: "$\binom{9}{4} = 126$." `feedback.generic`: "Not quite right. Count ordered picks, then divide by the $4!$ orders of each basket." `explain.text`: "There are $9 \times 8 \times 7 \times 6 = 3024$ ordered picks, and each basket appears in $4! = 24$ orders. So there are $\tfrac{3024}{24} = 126$ baskets, the fifth number of row 9."

35. review-1.json | `items[7]`; `items[8]` | continuity | `items[7]` repeats l2 `screens[9]` (a savings pot with monthly deposits, first month over a target). `items[8]` repeats l3 `screens[8]` (a dividend rising by a percentage). The numbers stay; only the setting changes. | l2 and l3 screens named. | `items[7]`: `prose` "A desk holds 350 shares after its first trade. Each later trade buys 125 more." `question` "After which trade does it first hold more than 2,000 shares?" `label` "First trade above 2,000 shares". `placeholder` "A trade number". `accept` "Trade 15: $350 + 14 \times 125 = 2100$." `feedback.correct` "Trade 15 leaves 2,100 shares; trade 14 leaves 1,975." `byKey.m14` "Trade 14 leaves $350 + 13 \times 125 = 1975$ shares. That is 25 short." `byKey.m16` "You divided 2,000 by 125. The desk already held 350 shares." `explain.text` last sentence "Trade 15 leaves 2,100 shares." `items[8]`: `prose` "A share trades 0.80 million shares on day 1, and its daily volume rises by 4% a day." `question` "On which day does the volume first exceed 1 million shares?" `label` "First day above 1 million". `placeholder` "A day number". `accept` "Day 7: $0.80 \times 1.04^6 \approx 1.0123$ million." `feedback.correct` "Day 6 trades about 0.97 million; day 7 about 1.01 million." `feedback.generic` "Not quite right. Compare $0.80 \times 1.04^{n-1}$ with 1 day by day." `byKey.y6` "Day 6 trades $0.80 \times 1.04^5 \approx 0.97$ million. Day 6 is only five rises after day 1." `byKey.simple` "You added 0.032 million a day, 4% of day 1's volume. Each rise is 4% of the latest volume, so it gets there sooner." `explain.text` "Day $n$ trades $0.80 \times 1.04^{n-1}$ million. Day 6 gives about 0.97 million and day 7 about 1.01 million. So day 7 is the first above 1 million."

36. l10-counting-paths.json | `screens[2].prose` | continuity | The lesson never shows ${}^nC_r$ or nCr, the form on a learner's calculator and in several A-level specifications. A GCSE-entry learner will meet it on the calculator key at once. | No `C_` in the course. | "Order does not matter: (1, 3) and (3, 1) are one pick. The number of ways to pick 2 of 4 is written $\binom{4}{2}$, read **4 choose 2**. Calculators write it ${}^4C_2$."

## Continuity

Notation is consistent inside the course and matches A-level: $u_n$, $a$, $d$, $r$, "common difference", "common ratio", "nth term", $u_{n+1} = f(u_n)$, $S_n = \tfrac{n}{2}(2a + (n - 1)d) = \tfrac{n}{2}(a + l)$, $S_n = \tfrac{a(1 - r^n)}{1 - r}$, $\binom{n}{k}$. Two places use letters of their own. Sigma notation uses $k$ for the index where Edexcel and AQA usually use $r$. The binomial general term uses $k$ where the formula booklet uses $r$, a sensible choice because $r$ is already the ratio. Neither needs a change. The convergence wording and $|r|$ are finding 27, and nCr is finding 36.

37. l13-stream-of-payments.json `screens[0].explain.text`, `screens[2].prose`, `screens[5].prose` against l7-shifted-copy.json `screens[8]` and l8-adding-forever.json `screens[8]` | continuity | l13 bolds **discounting** and **present value** as new and values a never-ending stream as if for the first time. l7's annuity and l8's perpetual bond already discounted payments ($\tfrac{500}{1.04^k}$, $\tfrac{5}{1.04^k}$) and stated "a perpetuity paying $c$ at rate $i$ is worth $\tfrac{c}{i}$". l13 also switches letters to $C$ and $r$, with $q$ for the ratio. L3 side should change. | l8 `screens[8].explain.text`. | l13 `screens[0].explain.text` third sentence: "This is called **discounting**; the annuity and the perpetual bond in the series lessons used it already." l13 `screens[5].prose`: "Now the payments never stop: £100.00 a year for ever, at 5%. This is the perpetual bond again, with $C$ for the payment and $r$ for the rate. Its terms shrink by the ratio $\tfrac{1}{1.05}$."

38. l13-stream-of-payments.json `screens[3].hints[0]` against number-sense l14-very-big-very-small.json | continuity | l13 writes $1.05^{-5}$ for $\tfrac{1}{1.05^5}$ from here on (19 uses). The only negative indices taught before are $10^{-k}$, and no line connects the two. | number-sense l14: "Each step left divides by 10: $10^{-1} = 0.1$". | "Work out $q^5 = \tfrac{1}{1.05^5}$ first. We write it $1.05^{-5}$, just as $10^{-1} = \tfrac{1}{10}$."

Items that reuse a lesson setup on purpose, extending it with a new question, need no change: homework-1 `items[5]` (l4's loan, three months on), `items[7]` (l3's two plans, when B overtakes), homework-2 `items[3]` (l7's doubling bettor, against a bankroll), `items[7]` (l7 and l8 together), review-2 `items[6]` (0.999… after l8's 0.333…), review-3 `items[5]` (six flips after l10's four).

## Orchestrator items (course.json; content agents do not edit it)

A. `series` level 1 `requires`: add three entries, beside the existing `equations/L1` and `number-sense/L3`. Each `why` is under 20 words. None creates a cycle: equations, ratio and counting do not depend on series.
```json
{ "ref": "equations/L2", "why": "Solves linear equations such as 3n + 2 = 100 and L = 0.5L + 10." },
{ "ref": "equations/l11-one-twist", "why": "Solves the inequality 1500 + 200(n - 1) > 10000 to find the first month." },
{ "ref": "ratio/l4-multipliers", "why": "Turns a percentage rise into a multiplier, such as 5% into 1.05." }
```
If the inequality edge is not wanted, a fixer can recast l2 `screens[9]` and review-1 `items[7]` as equations instead ("solve $1500 + 200(n - 1) = 10000$, then take the next whole month"), and drop the second entry.

B. `series` level 3 `requires`: add one entry, for l10 `screens[8]`, `quiz[3]` and review-3 `items[5]` (count over 32 or 64 equally likely sequences).
```json
{ "ref": "counting/l8-counts-to-chances", "why": "Turns a count of equally likely win-loss sequences into a chance." }
```

## Engine

- Expression answers typed as an equation are graded wrong, with the generic line. An engine fix is in progress, so no `accept` workaround is proposed. Six series items invite the form, because the question reads "Write $u_n$", "What is $f(k)$?" or "Expand $(x + 3)^3$". All six were checked on the real grader, and each rejects the learner's equation:
  - l3 `screens[7]`: `u_n=5\cdot3^{n-1}`
  - l11 `screens[2]`: `(x+3)^3=x^3+9x^2+27x+27`
  - homework-1 `items[0]`: `u_n=21-4n`
  - homework-1 `items[1]`: `u_n=96\cdot0.5^{n-1}`
  - homework-2 `items[0]`: `f(k)=4k+1`
  - homework-3 `items[0]`: `(2x-1)^4=16x^4-32x^3+24x^2-8x+1`
- `form: "simplified"` on a rational constant cannot refuse an uncancelled fraction or a decimal retyped from the prompt. For the key $\tfrac{3}{11}$ (homework-2 `items[6]`), `\frac{27}{99}`, `0.\overline{27}` and `0.27\overline{27}` all grade OK, with or without the form. Compute Engine canonicalises at parse. Finding 23 drops the "lowest terms" wording, but retyping the prompt's recurring decimal still scores.
- Validator key-length measures LaTeX source, so `$\dfrac{1}{1.05}$` (15 characters) against `$1.05$` is flagged although the two render about the same width (l13 `screens[2]`). Measure the text after stripping commands and braces.
- Validator (advisory): a `bars` canvas with `showValues` on a task screen whose starting state holds a 0 bar prints "0" or "£0.00" on what is usually the asked quantity. There are four series hits (finding 28). Warn unless `showZero` is set.

## Fix pass

Status per finding (36 fixed, 2 fixed (orchestrator), 0 disputed, 0 deferred, plus orchestrator items A and B and the Engine items). Every corrected number was recomputed before writing, by the number scripts (two methods each). Where the finding is conceptual, the basis is given.

1. fixed: l1 `screens[6].widget.options[3].text` is "8, 6, 4, 2, …" ($10 - 2n$ at $n = 1$ to 4 gives 8, 6, 4, 2); the explanation names the sequence 8, 6, 4.
2. fixed: l3 `screens[5]` `add` is -14 ($-2 - 6 - 6$) with the new line.
3. fixed: l3 `screens[5]` `times-two` is -8 ($-2 \times (-2) \times (-2)$) with the new line.
4. fixed: l4 `screens[2]` `order` is -2 (the slip gives 5, 4, 2, -2) with the new line.
5. fixed: review-2 `items[7]` `plus` is 1.5625 ($2.5 \div 1.6$).
6. fixed: review-3 `items[8]` `pct` is 5 ($25 - 20$); the explanation states the rise, £500.00, and 25% ($500 / 2000$).
7. fixed (conceptual; basis: binomial theorem, the coefficient $\binom{n}{k}$ is positive for $0 < k < n$, so mixed terms always appear, while $(1 - 1)^3 = 0 = 1^3 + (-1)^3$ shows their values can cancel; checked for n up to 11 in the L3 script): l11 `screens[6].explain.text` now speaks of terms.
8. fixed (conceptual; basis: squares 1, 4, 9, 16 curve with ratios 4, 2.25, 1.78, which differ): l3 `screens[2]` explain, `generic` and `correct` reworded as the finding says.
9. fixed (conceptual; basis: $u_{n+1} = 2u_n - 10$ with $u_1 = 10$ gives 10 for ever, run in the L1 script): l4 `quiz[3].explain.text`.
10. fixed: l4 `screens[5].prose` bolds **fixed point** with the check $2 \times 10 - 10 = 10$.
11. fixed: l1 `screens[2].feedback.byKey.sign` ("1, −2, −5").
12. fixed: l1 `quiz[1].explain.text`.
13. fixed (conceptual; basis: $48 \times 0.5^n \to 0$ while $48 + 24 + \dots \to 96$, L2 script): l7 `screens[4]` `forever` and `quiz[1]` option `two` `why` now say "total".
14. fixed: l7 `screens[8].hints[2]` shows $\tfrac{a}{1-r} = \tfrac{500}{0.04} = 12500$ and $12500(1 - 1/1.04^{10}) = 4055.45$ (both methods in the L2 script); `feedback.correct` uses $1/1.04^{10}$, no negative index.
15. fixed (conceptual; basis: simulation, $S_{10}$ is 1.998 at $r = 0.5$, 0.666 at $-0.5$, 6.51 at 0.9, still rising towards 10): l8 `screens[1].explain.text`.
16. fixed (conceptual; basis: $\tfrac{a}{1 - r}$ divides by 0 at $r = 1$): l8 `summary.formula.note`.
17. fixed (conceptual; basis: $0.1\dot{6} = 0.1 + \tfrac{0.06}{0.9}$, so only part of it is geometric): l8 `quiz[1].explain.text` says "This recurring decimal".
18. fixed: l8 `screens[6].explain.text` names the ratios 0.8 and -0.9, not "the first two".
19. fixed: l11 `screens[5].feedback.byKey.wrong-k` ($k = 3$ gives $\binom{4}{3} \times 2^3 = 32$, term $32/x^2$; power of $x$ is $4 - 2k$, zero at $k = 2$ only).
20. fixed: l12 `screens[8].explain.text` ("differ by little more than this term": 166.53 against 160.00).
21. fixed (orchestrator): course.json item A, `equations/L2`, `equations/l11-one-twist` and `ratio/l4-multipliers` added to level 1; l2 `screens[9]` and review-1 `items[7]` stay inequalities. Not touched here.
22. fixed (orchestrator): the `ratio/l4-multipliers` entry of item A.
23. fixed: homework-2 `items[6].question` is "What is it as a fraction?" (`accept` unchanged).
24. fixed: homework-2 `items[2].explain.text` has no quadratic formula; $\sqrt{500} = 22.36$, $S_{22} = 990$, $S_{23} = 1081$ (L2 script).
25. fixed (conceptual; basis: multiplication rule for independent events, $P(A \cap B) = P(A)P(B)$, A-level Statistics): homework-3 `items[3].prose` states it, with win, win, loss $= 0.6 \times 0.6 \times 0.4$.
26. fixed: l2 `screens[4]` "No, it is not a term"; l8 `screens[5]` "It has no finite value"; l12 `screens[4]` "The dropped terms are not small"; l12 `screens[6]` "It falls to a quarter"; review-2 `items[8]` "None". The five key-length warnings are gone; the l13 `screens[2]` one is the false positive (Engine).
27. fixed (conceptual; basis: derivation, $S_n = \tfrac{a(1 - r^n)}{1 - r}$ and $r^n \to 0$ exactly when $|r| < 1$; A-level wording "converges", "diverges", $|r| < 1$): **converges** is defined at first use in l4 `summary.ideas[1]` (the sequence settles on $L$) and again for a series in l8 `screens[2].explain.text` with **sum to infinity**; l8 `screens[6].prose` defines $|r|$ as $r$ with any minus sign dropped, writes $|r| < 1$ and bolds **diverges**.
28. fixed: `"showZero": false` added to l5 `screens[1]` and `screens[5]`, l1 `screens[8]` and l4 `screens[0]` canvas params.
29. fixed: l6 `screens[3]` explain is three sentences and prose is reworded (the explanation's first sentence is 18 words, so the validator's long-sentence advisory is gone); l8 `screens[5].widget.options[0].why` reworded; l13 `screens[6].prose` split. Voice scan: 0 and 0.
30. fixed: l3 `screens[9].explain.text` states £136.50 (22536.50 - 22400, two ways).
31. fixed: homework-2 `items[3].explain.text` says "9 losses".
32. fixed: the five run-on sentences now end with a full stop (l2 `screens[1]`, `screens[6]`; l8 `screens[0].hints[2]`, `screens[1]`; l12 `screens[1]`).
33. fixed: homework-1 `items[2]` is 2, 4, 8, 14, 22 with answer 32, `wrong` `add-last` 30 and `double` 44 (gaps 2, 4, 6, 8 then 10; $2 + n(n - 1)$ at $n = 6$ is 32).
34. fixed: review-3 `items[1]` is 4 of 9 shares, answer 126, `wrong` 3024, 36, 6561 ($\binom{9}{4}$ also by listing combinations).
35. fixed: review-1 `items[7]` (shares held, answer 15, 2,100 and 1,975) and `items[8]` (volume, answer 7, 0.97 and 1.01 million, 0.032 million).
36. fixed (conceptual; basis: ${}^nC_r$ and nCr are the same quantity as $\binom{n}{r} = \tfrac{n!}{r!(n - r)!}$, the calculator key; $\binom{4}{2} = 6$ by listing pairs): l10 `screens[2].prose` adds "Calculators write it ${}^4C_2$ or nCr."
37. fixed: l13 `screens[0].explain.text` says discounting was used already; `screens[5].prose` calls it the perpetual bond again, with $C$ and $r$.
38. fixed (conceptual; basis: index law $a^{-n} = \tfrac{1}{a^n}$, as $10^{-1} = \tfrac{1}{10}$): l13 `screens[3].hints[0]`.

Orchestrator items: A (all three entries, inequality edge kept) and B: fixed (orchestrator); course.json not touched.

Engine items: all four deferred, already in the inbox. The six equation-typed items were re-checked on the real grader (`grade.js` with Compute Engine 0.30.2, the review's harness, after ENGINE-BACKLOG 618 and 619). No accept forms were added.
- l3 `screens[7]` `u_n=5\cdot3^{n-1}`: fixed by 619 (grades OK).
- homework-1 `items[0]` `u_n=21-4n`: fixed by 619 (grades OK).
- homework-1 `items[1]` `u_n=96\cdot0.5^{n-1}`: fixed by 619 (grades OK).
- l11 `screens[2]` `(x+3)^3=x^3+9x^2+27x+27`: still failing (output `no`, the generic line). The left side is not one symbol, so 619 does not strip it.
- homework-2 `items[0]` `f(k)=4k+1`: still failing (output `no`). The `SYMBOL` pattern in `grade.js` reads one letter with a subscript, not `f(k)`, so `f(k)` is read as a product and the equation is unequal.
- homework-3 `items[0]` `(2x-1)^4=16x^4-32x^3+24x^2-8x+1`: still failing (output `no`), as for l11.
- homework-2 `items[6]`: `\frac{27}{99}` and `0.\overline{27}` still grade OK (Engine, unchanged).

Numbers: the finding-driven checks in `docs/reports/series-L1-numbers.py` (319 of 319), `-L2-` (309 of 309) and `-L3-` (326 of 326) all pass. Where a check accepted old or new text it now needs the new value: for example l3 `add` and `times-two`, l4 `order`, review-2 `plus`, review-3 `pct`, each `stated` check (fails if the old sentence returns), and a positive check for each reworded line. New checks cover homework-1 `items[2]` (32, 30, 44, two ways), review-3 `items[1]` (126, 3024, 36, 6561), review-1 `items[7]` and `items[8]`, l7 12500 and 4055.45, l8 6.51 and the $r = -1$ flip, homework-2 22, 990, 1081, l12 166.53 and 160.00, and l3 £136.50.

Gates: validator 0 errors (series warnings left: the l13 `screens[2]` key-length false positive only). Voice scan `VOICE_BASE=app/content/courses/series python3 docs/reviews/voice-scan.py 35`: 0 sentences over 35 words, 0 explanations over three sentences. All three number scripts exit 0. Playthrough with `--local-cdn`, desktop and `--mobile`: all 36 runs (l1 to l8, l10 to l13, review-1 to review-3, homework-1 to homework-3, each twice) report "All passed"; l9 is unchanged.

Orchestrator (session W): the engine part deferred above (answers typed as `y = ...`, `f(x) = ...`, `u_n = ...`, `n = ...` or a segment name) is fixed by ENGINE-BACKLOG 619 and 620; `test-expr-equations.mjs` covers it (all 20 functions and series expression widgets pass with those forms).
