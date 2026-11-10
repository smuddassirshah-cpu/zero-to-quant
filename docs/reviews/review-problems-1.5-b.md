# Problem sets 1.5 (b): second-reader findings

Scope: `app/content/courses/conditional/problems-4.json`, `problems-5.json` and `app/content/courses/random-vars/problems-1.json` to `problems-3.json` at commit 7545e35: 20 problems, 88 parts (80 numeric, 2 expression, 6 choice).

Method: both authors' scripts run first (`problems-conditional-numbers.py`: 979 checks, 0 failures; `problems-random-vars-numbers.py`: 639 checks, 0 failures). Every part then solved from its text before reading the answer, by hand in exact fractions, with an independent Python pass for the subtle ones (all 4 boxes by 100 year pairs for the dated coins, the 144 trade pairs and the shown-at-random summary, both managers' letters, the quit average of the doubling desk summed round by round, the 210 token hands, the 125 quotes, the fund and future joint table, a 200,000-run simulation of the reversals, and a pmf of $N$ that shows the clustered fills are possible). Every `wrong` value re-derived from the slip its line names. Each numeric part was tested against the engine's rule (`grade.js within`: `|v - answer| <= abs + 1e-9`) with the exact value rounded to 1, 2, 3 and 4 places, with every value its feedback prints after `\approx`, and with the value the part's own "Using ..." route gives. `numeric.js` and `parseNum` read for £, minus and % handling. Lessons opened for what each level teaches (host's rule l18, "how you learnt the fact is part of the evidence" l20, Kelly $2p - 1$ l26, doubling l22, $E[R \mid S]$ l25, VaR as the smallest loss with $F \ge 0.95$ l3, hedge ratio l11, minimum-variance weight l12).

No `answer`, `accept` text or explanation states a wrong value of the quantity asked, bar the digits in finding 1. Every `wrong` value differs from its answer, no two bands overlap, and every id has a `byKey` line. The two `expression` parts carry no `form`, so any equal spelling passes. Money parts take `45`, `£45`, `£45.00`, `-£15.96` and `£-15.96`.

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` = the question can be read two ways or does not say the form wanted; `minor` = weak part, loose entry, label or freshness.

## Findings

1. `wrong` | `conditional/problems-5.json` | `p-doubling-desk` | part 3.
   The question says "Using 0.5299 from part 2", with answer $-22.546$ and `tol` 0.005. The stated route gives $-10.598 / 0.4701 = -22.5441$, so a learner who rounds to the penny types $-22.54$ and is marked wrong (off by 0.006). The exact value is $-20p/(1-p) = -22.5486$ with $p = (31/32)^{20}$; the stored $-22.546$ is neither. `feedback.correct` and the explanation print "$-\tfrac{0.5299 \times 20}{0.4701} \approx -22.55$", which is false at the digits shown. No rounding is asked.
   Fix: `answer` $-22.55$, `tol` `{ "abs": 0.01 }` (takes $-22.54$ to $-22.56$; nearest slip is $-20$). Question ends "Give your answer to the nearest penny." `feedback.correct`: "$-\tfrac{0.5299 \times 20}{0.4701} \approx -22.54$ pounds. Without rounding part 2 it is $-22.55$." Explanation, sentence 2: "So $E[\text{profit} \mid \text{quit}] = -\tfrac{10.598}{0.4701} \approx -22.54$ pounds, or $-22.55$ before rounding." Part 4 may keep "Using −£22.55".

2. `wrong` | `random-vars/problems-3.json` | `p-fund-hedge` | part 1.
   "What is $E[A]$, in %?" has answer 0.8 and no `unit`. A learner who types `0.8%` is marked wrong: `parseNum` reads a trailing % as a division by 100, giving 0.008. The explanation itself writes "$E[A] = 0.8\%$".
   Fix: give the widget `"unit": "%"` as `conditional` `p-two-houses` part 1 does, with `answer` 0.008, `tol` `{ "abs": 0.000005 }`, `unweighted` 0.005 and `b-mean` 0.004 on the same `tol`. Then `0.8` and `0.8%` both pass. Question ends "Give one decimal place."

3. `unclear` | both courses | 17 parts whose answer does not terminate and whose rounding is not stated.
   Each says "Give a decimal" or nothing, with a band that takes 3 or 4 places but marks the 2-place answer wrong (0.54 for $\tfrac{7}{13}$, 0.33 for $\tfrac{1}{3}$, 0.48 for $\tfrac{11}{23}$, 0.79 for $\tfrac{19}{24}$, 0.58 for $\tfrac{7}{12}$). The money parts take the penny but not one place (24.3, 15.2, 4.6).
   Add "Give a decimal to 4 places." in place of "Give a decimal." to: conditional `problems-4` `p-two-strategies` 3, 4; `p-two-flags` 3; `p-dated-coins` 3; `problems-5` `p-warning-screen` 3, 4; `p-signal-streak` 3, 4, 5; `p-doubling-desk` 2. Add it as a new last sentence to: random-vars `problems-3` `p-fund-hedge` 4; `p-two-funds` 4.
   Add "Give a fraction, or a decimal to 4 places." in place of the form sentence to: conditional `problems-4` `p-two-flags` 1; random-vars `problems-2` `p-token-draw` 4.
   Add "Give your answer to the nearest penny." to: random-vars `problems-2` `p-reversal-days` 5; `problems-3` `p-quote-trades` 3; `p-clustered-fills` 3.

4. `unclear` | both courses | 14 parts that want an exact decimal of 3 or 4 places and do not say so.
   The answers terminate (0.455, 0.3125, 0.4096, 0.2916, 0.9477, 0.0486, 0.3375, 0.784, 0.296, 1.425, 0.0196, and $\tfrac{3}{16}$, $\tfrac{5}{16}$, $\tfrac{5}{8}$), but a learner told only "Give a decimal", or nothing, who rounds to 2 places is marked wrong (0.29 for 0.2916, 0.31 for 0.3125, 0.02 for 0.0196).
   Put "Give the exact decimal." in place of "Give a decimal.", or as a new last sentence, on: conditional `problems-4` `p-two-strategies` 2; `problems-5` `p-warning-screen` 1; `p-signal-streak` 2; random-vars `problems-1` `p-bond-defaults` 1, 2, 3; `p-straddle-days` 4; `p-tightest-quote` 2, 3; `problems-3` `p-fund-hedge` 5; `p-two-funds` 2.
   Put "Give a fraction or the exact decimal." on: random-vars `problems-1` `p-spinner-product` 1 (in place of its sentence), 3, 4.

5. `unclear` | `conditional/problems-4.json` | `p-dated-coins` part 3, and `p-two-flags` parts 1 and 2.
   "An assistant opens the box and reports: 'it holds at least one gold coin from 1987'" does not say how the report came about. l20 teaches that how you learnt the fact is part of the evidence. If the assistant picks a gold coin and reads its year, the answer is 0.8, which the part stores as the slip `drawn`. Only a yes to a set question gives $\tfrac{19}{24}$. `p-two-flags` has the same gap ("The day's summary says only that ..."), though its part 4 does contrast the two routes.
   Fix, `p-dated-coins` part 3: "You ask an assistant who can see inside: 'Does the box hold at least one gold coin from 1987?' He says yes. Using 0.19 from part 2, what is the chance the box holds two gold coins? Give a decimal to 4 places." `p-two-flags` part 1: "You ask the system one question: was at least one of today's flagged trades a long? It says yes. What is the chance both were longs? Give a fraction, or a decimal to 4 places." Part 2, sentence 3: "You ask instead whether at least one trade was a long in energy, and it says yes."

6. `unclear` | `conditional/problems-5.json` | `p-two-houses` | part 2, explanation.
   "The gap is $P(S^c)\,(E[R \mid S] - E[R \mid S^c])$" uses l25's letters, $R$ for return and $S$ for survived, in an item whose two houses are called R and S. The line reads as House R given House S.
   Fix: "The gap is the share that closed times the difference between the groups: $0.5 \times (8 - (-2)) = 5$ points. So House S averaged $8 - 5 = 3$% over all its funds. House R's gap is only $0.2 \times 13 = 2.6$ points, because few of its funds closed."

7. `minor` | both courses | 30 numeric parts with a short exact answer and no form sentence.
   Nothing sensible is marked wrong here, but the brief asks every numeric part for one. Sentences to add as the last sentence of the question:
   - "Give a decimal.": conditional `problems-4` `p-marble-bags` 4; random-vars `problems-1` `p-straddle-days` 1, 2, 3; `problems-2` `p-reversal-days` 2, `p-token-draw` 2; `problems-3` `p-two-funds` 1, 3, `p-clustered-fills` 1, 2.
   - "Give a fraction or a decimal.": random-vars `problems-1` `p-spinner-product` 2.
   - "Give the exact decimal.": random-vars `problems-3` `p-quote-trades` 2, `p-fund-hedge` 2, 3.
   - "Give your answer to the nearest penny.": random-vars `problems-2` `p-phone-cover` 1, 2, 4, `p-reversal-days` 4, `p-month-options` 1, 2, 3, 4, `p-token-draw` 3, 5; `problems-3` `p-quote-trades` 1.
   - "Give your answer to the nearest pound.": random-vars `problems-2` `p-phone-cover` 3; conditional `problems-5` `p-doubling-desk` 1.
   - "Give one decimal place.": conditional `problems-5` `p-two-houses` 1, 2, 4.

8. `minor` | `conditional/problems-5.json` | `p-signal-streak` | part 5.
   "Using 0.5291 from part 4" gives $2 \times 0.5291 - 1 = 0.0582$; the stored answer is 0.0581 (the exact $0.058116$). Both pass the band, but the brief asks for the answer the rounded value gives, and the reveal shows 0.0581 to a learner who correctly typed 0.0582.
   Fix: `answer` 0.0582; `feedback.correct` "$2 \times 0.5291 - 1 = 0.0582$."; explanation "$f = 2 \times 0.5291 - 1 = 0.0582$, down from 0.1 before the streak."

9. `minor` | `conditional/problems-5.json` | `p-warning-screen` | prose, parts 1 and 2.
   "Count the true flags and the false flags among the 2,000 companies" gives 39.6 false flags. A count that is not whole undoes the picture (l9), the same fault as finding 14 of the first read.
   Fix: prose "Of 10,000 listed companies, 100 will issue a profit warning this quarter." Then 90 true flags and 198 false: part 1 `feedback.correct` "$\tfrac{90}{90 + 198} = 0.3125$.", `generic` "... among the 10,000 companies."; explanation "The 100 warning companies give $0.9 \times 100 = 90$ flags, and the 9,900 others give $0.02 \times 9900 = 198$. So $P(\text{warning} \mid \text{flag}) = \tfrac{90}{288} = 0.3125$." Part 2: option `small` "Nothing: 2% of the 9,900 quiet companies is only a small number", why "It is small beside 9,900 companies, but it is 198 false flags against 90 true ones."; option `share-flagged` "... the share of all 10,000 companies that are flagged"; explanation "$\tfrac{198}{288} = 0.6875$". The answer, 2.88% and all later parts are unchanged. Update the numbers script.

10. `minor` | `conditional/problems-5.json` | `p-two-houses` | part 4.
    Part 3's question already prints "R leads, 4.4% to 3%", and part 4 restates both and asks for $4.4 - 3$. The last part is one subtraction of two given numbers.
    Fix: ask a result. "House R averaged 4.4% over all its funds (part 1). Keep House S's group averages, 8% and −2%. How many of its 50 funds would have had to survive for S to match 4.4%?" Answer 32, `tol` 0 ($\tfrac{32 \times 8 - 18 \times 2}{50} = 4.4$), `unit` "funds". `wrong`: `r-count` 40, "That is House R's count. With S's group averages 40 survivors would give 6%." Feedback: "$8s - 2(1 - s) = 4.4$ gives $s = 0.64$, so 32 funds." Explanation: "Let $s$ be the share that survives: $8s - 2(1 - s) = 4.4$, so $s = 0.64$ and 32 funds. S needed 32 survivors and had 25. Survival, not skill within each group, decides the comparison."

11. `minor` | `conditional/problems-4.json` | `p-two-strategies` | part 4.
    The part restates 0.21 but not 0.49, the chance both win, which it needs just as much (it last appeared in part 2's feedback).
    Fix: "Using 0.49 for both winning and 0.21 for B winning alone, his letter names B."

12. `minor` | `random-vars/problems-3.json` | `p-fund-hedge` | part 5.
    The part gives $h$ but none of the three values the formula needs; $\operatorname{Var}(B) = 3.84$ sits two parts back in a question.
    Fix: after the first sentence add "Use $\operatorname{Var}(A) = 2.16$, $\operatorname{Var}(B) = 3.84$ and $\operatorname{Cov}(A, B) = 1.68$."

13. `minor` | `random-vars/problems-3.json` | `p-two-funds` | part 5.
    The correct option prints all three ratios ("about 1.02, against 0.86 for X and 0.71 for Y"); the others print none. The learner can pick it without dividing.
    Fix: option texts "The mix of 0.2 in X and 0.8 in Y", "Fund X alone", "Fund Y alone", "All three give the same". Keep the `why` lines; the ratios stay in the feedback and explanation.

14. `minor` | difficulty labels.
    `random-vars/problems-1.json` `p-tightest-quote` is the set's only 5; its parts are $3^3$, a complement, a subtraction and a trial of powers of 0.8. It is a 4. `random-vars/problems-2.json` `p-token-draw` (5) is 0.3, $4 \times 0.3$, a linear map, one count of hands and one sum: a 4. `conditional/problems-4.json` `p-two-strategies` (3) asks more than `p-marble-bags` (4) parts 1 and 2.
    Fix: either relabel and accept that these two sets have no true 5, or harden one part each. `p-tightest-quote` part 4: drop the given formula and ask for the smallest $n$ with $P(T \le 2) \ge 0.99$ ($n = 10$: $0.6^{9} = 0.0101$, $0.6^{10} = 0.0060$). `p-token-draw` part 5: ask for the fair price when the bonus is £15 for each gold token after the first ($38 + 15(E[G] - P(G \ge 1)) = 38 + 15(1.2 - \tfrac{5}{6}) = 43.50$). Relabel `p-two-strategies` 4.

15. `minor` | freshness | `conditional/problems-5.json` `p-doubling-desk` part 1.
    The setting and part 1 are l22's doubling system with the cap moved from six losses to five (review-5 and homework-5 use it again); the fresh-check hit is in the author's report. Parts 2 to 4, the 1,000 traders and the quit rule, are new.
    Fix: accept, or state the round's zero average in the prose and make part 1 the chance of a losing round ($\tfrac{1}{32}$).

## Per problem and per set

- `p-marble-bags` against `homework-4` `h-host-q`: different enough. The homework is Monty Hall with a host who favours door 3, answer $\tfrac{1}{1+q}$. This item is Bertrand's box with three mixed bags, a dealer who shows a marble, answer $\tfrac{1}{1+3h}$, and a new last step: the $h$ at which the dealer is no more than a random draw. The algebra has the same shape and the `one-mixed` slip is the homework's answer, but setting, prior and question are new, and it ties l19 to l18. Note that `p-two-strategies` part 4 uses the habit idea again in the same set; one of the two is enough if either is ever cut.
- Chains: all 20 are real chains, and later parts restate what they need apart from findings 11 and 12. No opening prose gives a part away. `p-token-draw` part 4 and `p-two-flags` part 4 start afresh but feed the next part. Last parts ask for a result apart from finding 10.
- Coverage: every lesson of each level is drawn on (conditional l18 to l21 and l22 to l26; random-vars l1 to l4, l5 to l8, l9 to l12), and each problem draws on at least two. Nothing needs an idea beyond its level: Kelly is in l26, VaR in l3, the hedge ratio in l11, and the two-fund weight is given in the question.
- Difficulty: each set has an item labelled 5 (see finding 14 for two of them). Typed parts: 18 of 18, 14 of 17, 16 of 17, 17 of 18, 17 of 18; each `choice` part is a judgement apart from finding 13.
- `wrong` entries: all match the slip named and all are reachable; carried slips from the part before are present throughout.
- Voice: British English, no exclamation marks, no em-dashes, £ throughout, no explanation over three sentences (`voice-scan.py 35`: 0 and 0 on both folders).

## Counts

| tag | count |
|---|---|
| wrong | 2 |
| unclear | 4 |
| minor | 9 |

Form sentences to add or change: 61 numeric parts in findings 3, 4 and 7, plus the two in findings 1 and 2.

Clean problems (no finding other than the form sentences of findings 3, 4 and 7): conditional `p-marble-bags`; random-vars `p-spinner-product`, `p-bond-defaults`, `p-straddle-days`, `p-phone-cover`, `p-reversal-days`, `p-month-options`, `p-quote-trades`, `p-clustered-fills`. No problem is free of edits.

## Fix pass

I recomputed every changed number before writing it (exact fractions, enumeration of the token hands, running powers for the dealer counts, the 100 flagged-company counts, a try-every-count search for the House S survivors, the doubling route from the rounded 0.5299). Both author scripts were extended and exit 0 (`problems-conditional-numbers.py` 1177 checks over sets 1 to 5; `problems-random-vars-numbers.py` 744 checks), each now with `form_checks` for sets 4 and 5 (conditional) and sets 1 to 3 (random-vars): a form sentence on every non-whole numeric part, the key rounded as asked is inside its tolerance (penny, pound, places, per cent scaled), exact-decimal parts terminate, and every printed `\approx` value is accepted. `node tools/validate.mjs`: 0 errors, no warning on these five files. `--problems` playthrough of all five sets, with and without `--mobile`: green. `voice-scan.py 35`: 0 and 0.

Status: applied 13, applied with a change 1 (finding 7), accepted without edit 1 (finding 15). No finding disputed.

1. p-doubling-desk part 3: applied. Recomputed: exact -22.5486, route -10.598 / 0.4701 = -22.5441. Key -22.55, tol 0.01 (takes -22.54 to -22.56; nearest slip -20), "nearest penny", feedback and explanation as proposed. Graded answer changed: -22.546 to -22.55.
2. p-fund-hedge part 1: applied. `unit: "%"`, key 0.008, tol 0.000005, slips 0.005 and 0.004, "Give one decimal place." Graded answer changed in storage only (0.8 typed in % is still the same figure).
3. Form sentences (17 parts): applied as listed.
4. Form sentences (14 parts): applied as listed. Where feedback or explain printed a 3-place value under a 4-place question it now prints 4 places (0.5385, 0.3182, 0.4783, 0.7917, 0.7843, 0.5686, 0.2906, 0.5291, 0.5299, 0.5833).
5. p-dated-coins part 3, p-two-flags parts 1 and 2: applied with the proposed wording.
6. p-two-houses part 2 explanation: applied.
7. Form sentences (30 parts): applied as listed, with one change. p-doubling-desk part 1 asks for the nearest penny, not the nearest pound: at whole pounds the slip `no-loss` 0.9688 rounds to 1 and collides with `win`, and the validator's wrong-band rule fires. `no-loss` has tol 0.005 so 0.97 reaches it. The answer 0 is unchanged.
8. p-signal-streak part 5: applied. Key 0.0582, feedback and explanation as proposed. Graded answer changed: 0.0581 to 0.0582 (exact 0.058116, both inside the band).
9. p-warning-screen: applied. 10,000 companies, 100 warners, 90 true and 198 false flags; 0.3125, 0.6875 and 2.88% unchanged. Numbers script updated, with a check that both counts are whole.
10. p-two-houses part 4: applied. Now asks how many of S's 50 funds must survive to match 4.4% (32, tol 0, unit "funds"). Graded answer changed: 1.4 to 32. Slips: `r-count` 40, `actual` 25, `share` 0.64 (old slips -1, -4 and -0.6 retired with the question).
11. p-two-strategies part 4: applied.
12. p-fund-hedge part 5: applied.
13. p-two-funds part 5: applied; ratios stay in feedback, explanation and `why` lines.
14. Difficulty labels: applied by hardening where a set needs its 5. p-two-strategies relabelled 4 (report table updated). p-tightest-quote part 4 now asks the smallest n with P(T <= 2) >= 0.99: 10 (0.6^9 = 0.0101, 0.6^10 = 0.0060); slips 9, 21 (base 0.8 from the old rule) and 6 (base 0.4). Graded answer changed: 11 to 10. p-token-draw: part 4 says the bonus is £15 for the second gold token and a further £15 for the third (still P(G >= 2) = 1/3, answer unchanged), and part 5 asks the fair price: 38 + 15(1/3 + 1/30) = 43.50, checked against 38 + 15(E[G] - P(G >= 1)) = 38 + 15(1.2 - 5/6). Graded answer changed: 43 to 43.50; slips no-bonus 38, once-only 43, full-bonus 53, bonus-only 5.5, carried 43.7245.
15. p-doubling-desk freshness: accepted, no edit (the review allows it; parts 2 to 4 are new).
