# Claim ledger: mental-pressure L4 (blind concept audit)

Scope: `app/content/courses/mental-pressure/` files `l13-negative-marking`, `l14-ranking-likelihoods`, `l15-probability-at-speed`, `l16-harder-sequences`, `l17-full-battery`, `review-4`, `homework-4`. Written blind to the earlier review and author reports, one lesson at a time. `sim:` rows point at a named check in `docs/reports/mental-pressure-L4-concepts.py` (run `python3 -I docs/reports/mental-pressure-L4-concepts.py` from the repo root). Sources: C&B = Casella and Berger, *Statistical Inference* 2e; Ross = Ross, *A First Course in Probability* 8e; Feller = Feller, *An Introduction to Probability Theory* Vol 1; Rudin = Rudin, *Principles of Mathematical Analysis* 3e; Conway 1987 = Conway, "The weird and wonderful chemistry of audioactive decay". Paths are JSON paths inside the file; `s[k]` is `screens[k]`.

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l13 | s[0].prose | some online tests score +1 right, −1 wrong, 0 blank | unverified | claim about real vendors, hedged ("some firms"); no source in the content |
| l13 | s[0].widget.answer, hints, feedback.correct, explain.text | net = right − wrong, blanks 0: 62 − 10 = 52 | correct | definition of the stated scheme; sim: `l13_net_scores` |
| l13 | s[0].feedback.byKey.{no-penalty,blanks-too,added} | 62 ignores penalty; 44 subtracts blanks; 72 adds wrong | correct | each slip recomputed under the scheme; sim: `l13_net_scores` |
| l13 | s[0].explain.text | candidates report a pass band of about 50 to 60 net | unverified | vendor pass marks are not public; hedged as a report |
| l13 | s[1].prose, s[2].prose | the bar is the expected mark, the average over many guesses; weigh each mark by its chance and add | correct | definition of expectation, C&B §2.2; law of large numbers C&B §5.5 for "average over many guesses"; sim: `l13_guess_value_mc` |
| l13 | s[1].widget.answer, hints, feedback, explain | at −1, a guess averages 0 only with 2 left; 3 left gives −1/3; 4 left −0.5; 1 left +1 | correct | E = 1/k − (k−1)/k = (2−k)/k; sim: `l13_guess_table` |
| l13 | s[1].explain.text | at w = −0.33 even a blind guess is free | correct | 1/4 − 0.33·3/4 = +0.0025 ≈ 0; sim: `l13_guess_table` |
| l13 | s[2].widget.answer, hints, feedback, explain | blind guess among five at ±1 is −0.6; more options make a blind guess worse; every option removed moves the bar up | correct | E(k, w) = (1+w)/k − w is decreasing in k for every w ≥ 0; sim: `l13_monotone_in_k` |
| l13 | s[2].feedback.byKey.{only-right,only-wrong,four-options} | 0.2 counts only the right fifth; −0.8 only the wrong; −0.5 is four options | correct | each recomputed; sim: `l13_guess_table` |
| l13 | s[3].prose | at ±1 answering at confidence p earns 2p − 1, a blank 0 | correct | p·1 + (1−p)(−1); sim: `l13_answer_value` |
| l13 | s[3].widget rows, hints, feedback.byKey r0c1..r4c1, explain | 2p − 1 at 40, 50, 60, 75, 90%: −0.2, 0, 0.2, 0.5, 0.8; answer iff p > 1/2 | correct | derivation; sim: `l13_answer_value` |
| l13 | s[4].prose, canvas caption | 80-in-8 reported as forward only, no skip; solving Q31 at 90% earns 0.8 | unverified / correct | format claim hedged ("candidates report"); 0.9 − 0.1 = 0.8 by s[3] |
| l13 | s[4].widget.answer, hints, feedback, explain | guess after removing two is 0; 18 s at 6 s buys three questions at 0.8: 2.4 against 0.8, a gain of 1.6 | imprecise | arithmetic right (sim: `l13_trade`); the gain exists only when the clock, not the question count, ends the sitting (otherwise the saved seconds buy nothing): the 80-in-8 framing implies it but the summary drops it (finding 3) |
| l13 | s[4].feedback.byKey.{no-penalty,all-right,one} | 2.7 ignores the penalty; 3 assumes all right; 0.8 is one question | correct | recomputed; sim: `l13_trade` |
| l13 | s[5].prose | rules differ between tests, read the marking first | correct | follows from the scheme dependence of E(k, w) below |
| l13 | s[5].widget rows, hints, feedback, explain | blind guess among four: 0 at −1/3, −1/8 at −1/2, +1/4 at 0; the penalty decides whether a blind guess pays | correct | E = 1/4 − (3/4)w; sim: `l13_guess_table` |
| l13 | s[6].options[0].correct, feedback.correct, explain | with no skip, remove options then guess: the guess goes from −0.5 to 0 | correct | (2−k)/k at k = 4, 3, 2; sim: `l13_guess_table` |
| l13 | s[6].options[1].why, byKey.blank | a blank is impossible in a no-skip test | correct | under the stated format hypothesis (s[4]) |
| l13 | s[6].options[2].why, byKey.blind | blind guess averages −0.5 | correct | sim: `l13_guess_table` |
| l13 | s[6].options[3].why, byKey.solve | 30 s is five questions at 6 s, worth 4 marks at 90% | correct | 5 × 0.8 = 4; sim: `l13_trade` |
| l13 | s[7].prose | E[guess] = 1/k − w(k−1)/k; at w = 1 this is (2−k)/k; answering at p earns 2p − 1, answer when more than half sure | imprecise | formula correct (sim: `l13_guess_table`); the half-sure rule holds only at w = 1: break-even is p* = w/(1+w) (1/4 at −1/3, 1/3 at −1/2, 0 at no penalty), and the sentence follows a screen that introduced those schemes (finding 1); sim: `l13_breakeven` |
| l13 | s[7].widget.answer, hints, feedback, explain | five options, remove two: k = 3, −1/3; a guess is free only when two are left | correct | (2−3)/3; "free only at k = 2" since (2−k)/k = 0 iff k = 2; sim: `l13_guess_table` |
| l13 | s[7].feedback.byKey.{free,five} | 0 is k = 2 among four; −0.6 is five options blind | correct | recomputed; sim: `l13_guess_table` |
| l13 | s[8].prose, widget.answer, hints, feedback, explain | fair penalty: 1/k − w(k−1)/k = 0 gives w = 1/(k−1); 1/3 for four, 1/4 for five; under it a blind guess is free and removing an option makes it pay | correct | algebra; E(k−1, 1/(k−1)) = (1 + 1/(k−1))/(k−1) − 1/(k−1) > 0; sim: `l13_fair_penalty` |
| l13 | s[8].widget.wrong[*], byKey.{over-k,upside-down} | 1/k is the chance of a right guess, not the penalty; k − 1 is the inverse | correct | neither zeroes E except k = 2; sim: `l13_fair_penalty` |
| l13 | s[9].widget (code) prose, solution, tests, how | `guess_value` returns the exact Fraction 1/k·right + (k−1)/k·wrong; `net_score` skips None, adds right or wrong; 13 tests listed | correct | solution run against every test, starter fails; sim: `code_l13` |
| l13 | s[9].explain.text | `Fraction(wrong)` keeps −1/3 exact; a blank is skipped before the comparison so it never counts as wrong | correct | code behaviour read and run; sim: `code_l13` |
| l13 | s[10].widget rows r0, r1, r3, r4, r5, r7; byKey | −1/3 at k = 3; 58 − 14 = 44; 85% of 70 is 59.5 right, 10.5 wrong, net 49; fair guess 0 at −1/3 | correct | recomputed; sim: `l13_quick_eight` |
| l13 | s[10].widget rows r2, r6 | 80 blind guesses among four net −40; answering beats a blank above accuracy 0.5 | imprecise | both keys hold only at +1/−1, which these two rows do not state while row 7 states −1/3; at −1/3 the keys would be 0 and 0.25 (finding 2); sim: `l13_breakeven` |
| l13 | s[10].explain.text | 70 at 85% nets 49 against 52; answering more pays only when each answer is more than half sure; blind guesses at −1 cost half a mark each | correct (at ±1) | 2p − 1 > 0 iff p > 1/2 at w = 1; scheme is the lesson's running one; sim: `l13_answer_value` |
| l13 | s[11].options[0] "answer when more than half sure" (card line) | | imprecise | the card is "for a negatively marked online test" in general; the line is right only at w = 1 (finding 1); sim: `l13_breakeven` |
| l13 | s[11].options[1] remove two then guess, the guess is free | | correct | k = 2 at ±1; sim: `l13_guess_table` |
| l13 | s[11].options[2] a question past 20 s: cut options and guess | | correct | heuristic backed by s[4]'s trade; at 2 left any s − g > pace favours the guess (sim: `code_hw_trade`) |
| l13 | s[11].options[3] "at −1/3 or 0, guess everything" | | imprecise | true for four options (E = 0 and 1/4); at −1/3 with five options a blind guess is −1/15 < 0 (finding 1); sim: `l13_fair_penalty` |
| l13 | s[11].options[4..6].why, byKey | blanks impossible with no skip and answering pays above half; blind guess costs 0.5; time spent is gone | correct | under the stated format; sim: `l13_guess_table` |
| l13 | summary.ideas[0], formula | (2−k)/k; −0.5, −1/3, 0; E = 1/k − w(k−1)/k; −0.5 at w = 1, 0 at w = 1/3 | correct | sim: `l13_guess_table` |
| l13 | summary.ideas[1] | answering earns 2p − 1 so answer when more than half sure | imprecise | drops w = 1; break-even is w/(1+w) in general (finding 1); sim: `l13_breakeven` |
| l13 | summary.ideas[2] | 20 s buys a free guess and three questions worth 2.4 against 0.8 | imprecise | needs the clock to be binding and the 90% rate on the extra questions (finding 3); sim: `l13_trade` |
| l13 | summary.trap | "never guess" throws away free guesses in a no-skip test; "always guess" blind costs half a mark | correct | k = 2 is 0, k = 4 is −0.5; sim: `l13_guess_table` |
| l13 | quiz[0] | 75 answered, 11 wrong: 64 right, net 53; blanks 0 | correct | sim: `l13_net_scores` |
| l13 | quiz[1] | blind guess at −1/2 among four is −1/8; cheaper than at −1 but not free; 0 needs 1/3 | correct | 1/4 − 3/8; sim: `l13_guess_table` |
| l13 | quiz[2] | at 55% sure answering earns 0.1 and beats a blank; another option averages below 0; options left do not matter once p is yours | correct | 2(0.55) − 1 = 0.1; any other option has q ≤ 0.45 so 2q − 1 < 0; scheme stated (+1, −1); sim: `l13_answer_value` |
| l13 | quiz[3] | no penalty: six blind guesses among four expect 1.5; never leave a blank under such a rule | correct | 6 × 1/4; E = 1/k > 0 at w = 0; sim: `l13_guess_table` |
