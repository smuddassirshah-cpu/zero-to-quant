# Claim ledger: conditional levels 4 and 5 (blind audit, round 1)

Scope: `l18` to `l26`, `review-4`, `review-5`, `homework-4`, `homework-5`, `problems-4`, `problems-5`. Stage 1, full depth. Every row was read and judged by hand. "script" means a check in `docs/reports/conditional-L4-5-concepts.py` (exact enumeration with fractions, or seeded Monte Carlo, CPython 3.13). "F<n>" points to the finding in `docs/reviews/audit-conditional-4-5.md`.

Sources used: Blitzstein and Hwang, *Introduction to Probability* (2nd ed.), ch. 2 (BH: 2.2.5 to 2.2.7 two children, random child, winter girl; 2.7.1 Monty Hall; 2.8.1 prosecutor's fallacy; 2.8.2 defence attorney's fallacy; 2.8.3 Simpson's paradox). Rosenthal (2008), "Monty Hall, Monty Fall, Monty Crawl", *Math Horizons* 16(1). Bar-Hillel and Falk (1982), "Some teasers concerning conditional probabilities", *Cognition* 11. Feller, *An Introduction to Probability Theory*, vol. 1, ch. III (fluctuations, returns to the origin) and ch. X (law of large numbers). Pearl, *Causality* (2nd ed.), section 6.1. Casella and Berger, *Statistical Inference*, section 8.3.4 (p-values). Kelly (1956); Thorp (2006), "The Kelly criterion", section 2. Williams, *Probability with Martingales*, 10.10 (optional stopping). Brown, Goetzmann, Ibbotson and Ross (1992), "Survivorship bias in performance studies", *RFS* 5(4). Glosten and Milgrom (1985). Harvey, Liu and Zhu (2016), *RFS* 29(1) (multiple testing).

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l18 | screens[0].prose | The answer depends on what the host knows and what he would have done | correct | BH 2.7.1; Rosenthal (2008): the posterior is set by the host's likelihoods |
| l18 | screens[1].prose | Host knows, opens a goat door, offers a swap (no "always", no tie-break) | imprecise | A host who offers only when you hold the car makes switching lose. Rule is fixed only on screens 2 and 3. F1 |
| l18 | screens[1].widget (key switch) | Switching is the better choice | correct | Under the rule of screens 2 and 3: 2/3 against 1/3. script |
| l18 | screens[1].options stay.why | First pick right 1 in 3 "and the host's goat does not change that" | misleading | True for the symmetric host only; the lesson's lazy host moves door 1 to 1/2. F1 |
| l18 | screens[1].options same.why | The host chose which door to open and could never open yours | correct | States the asymmetry; no inference drawn from it |
| l18 | screens[1].hints[1] | The host can always find a goat to show | correct | Two goats, at most one behind your door |
| l18 | screens[1].hints[2] | When door 1 is wrong the car is behind the one door left shut | correct | Knowing host never opens the car |
| l18 | screens[1].feedback.correct | Switching wins whenever the first pick was wrong: 2 in 3 | correct | Unconditional strategy argument, valid for any tie-break |
| l18 | screens[1].explain | "the host's goat cannot change that" | misleading | Same as stay.why. F1 |
| l18 | screens[2].prose, canvas | Three equally likely rows; host opens a goat door you did not pick | correct | Uniform prior stated; grid cells match |
| l18 | screens[2].widget.answer | Switch lands on the car in r2c2, r3c3 | correct | Row 2: host opens 3, switch to 2. Row 3: host opens 2, switch to 3 |
| l18 | screens[2].feedback.byKey (all) | Row 1 switching loses; rows 2, 3 host forced | correct | Enumeration |
| l18 | screens[2].explain | Switching wins with chance 2/3, staying 1/3 | correct | 2 of 3 equally likely rows |
| l18 | screens[3].prose | Host's rule = second level of the tree: what he would do in each case | correct | Likelihood P(opens | car); BH 2.7.1 |
| l18 | screens[3].canvas | Branches 1/2, 1/2; 0, 1; 1, 0; leaves 1/6, 1/6, 0, 1/3, 1/3, 0 | correct | Products checked; leaves sum to 1 |
| l18 | screens[3].widget.answer | Forced branches: c2-o3, c3-o2 | correct | Only one goat door left in each |
| l18 | screens[3].feedback car-one | After car 1 he picks one at random | correct | Symmetric tie-break stated here |
| l18 | screens[3].explain | Multiplying along each path gives the leaves | correct | Multiplication rule |
| l18 | screens[4].widget | P(car 2 | opens 3) = 2/3; slips 1/2, 1/3 | correct | (1/3)/(1/6+1/3). script |
| l18 | screens[4].feedback prior | 1/3 is the car-2 path; divide by P(opens 3) | correct | Bayes |
| l18 | screens[4].explain | Paths 1/6 and 1/3 add to 1/2; door 1 keeps 1/3 | correct | Arithmetic; true for this host |
| l18 | screens[5].prose, canvas | Random host opens 2 or 3 at random; leaves 1/6 each with goat or car | correct | Enumeration |
| l18 | screens[5].widget | Switching wins 1/2; 2/3 and 1/3 are slips | correct | Two paths of 1/6 survive. script exact and MC 0.502 |
| l18 | screens[5].feedback two-thirds | This host could have shown the car, so his goat tells you less | correct | Likelihood ratio 1 between car 1 and car 2 |
| l18 | screens[5].explain | Same doors, same goat, different rule, different answer | correct | Rosenthal (2008), "Monty Fall" |
| l18 | screens[6].widget | 100 doors: door 57 has 99/100 | correct | Uniform choice of the skipped door when car at 1: (1/100)(1/99) against (1/100)(1) gives 99/100 |
| l18 | screens[6].feedback.correct | Host skipped door 57 among 99 he could have opened | correct | Loose but harmless: 99 unpicked doors |
| l18 | screens[6].feedback half | Host avoided door 57 on purpose | correct | Forced when the car is there |
| l18 | screens[6].feedback one-door | 1/100 "which the goats cannot change" | misleading | Same unsupported inference as screen 1. F1 |
| l18 | screens[6].explain | Door 1 wins 1 in 100; otherwise the car is behind the skipped door | correct | Unconditional argument |
| l18 | screens[7].options right | Friend assumes door 3 is opened as readily from car 1 as from car 2 | correct | That is the hidden equal-likelihood assumption |
| l18 | screens[7].options fifty.why | 50:50 holds only when the move is equally likely from both doors | correct | Bayes: equal priors and equal likelihoods |
| l18 | screens[7].options door-one.why | "The host could never open door 1, so his move says nothing new about it" | misleading | Invalid inference: the lazy host of quiz[1] never opens door 1 either, and door 1 goes to 1/2. script. F1 |
| l18 | screens[7].options three.why | Door 3 showed a goat, so its chance is 0 | correct | Observed |
| l18 | screens[7].hints[2] | Equal priors times unequal likelihoods give unequal posteriors | correct | Bayes |
| l18 | screens[7].explain | Likelihood ratio 2 moves odds door 2 : door 1 from 1:1 to 2:1 | correct | 1 against 1/2 |
| l18 | screens[8].widget (order) | Bayes, total probability, host's rule, arithmetic | correct | Only order in which each line follows from the last |
| l18 | screens[8].explain | Likelihoods 1/2, 1, 0; bottom 1/2 is P(opens 3) | correct | Sum of leaves ending in door 3 |
| l18 | screens[9].prose, sim | Switching wins exactly when the first pick was wrong; sim `d(3) != d(3)` | correct | For a knowing host who always opens a goat. P(two fair d3 differ) = 2/3 |
| l18 | screens[9].widget | About 667 of 1,000; tolerance 30; slips 500, 333 | correct | Binomial sd is 14.9; bands do not overlap |
| l18 | screens[9].explain | Share settles near 2/3, its exact limit | correct | Law of large numbers |
| l18 | screens[10].prose, canvas | 30% informed sell only before £99; 70% sell half the time; P(sell | 99) = 0.65, P(sell | 101) = 0.35 | correct | 0.3 + 0.35; 0.35. script |
| l18 | screens[10].widget | P(99 | sell) = 0.65; slips 0.5, 0.3, 0.35 | correct | Equal priors. script |
| l18 | screens[10].explain | Being filled by someone who knows more is adverse selection | correct | Glosten and Milgrom (1985) |
| l18 | summary.ideas[0] | Condition on the event and the rule that produced it | correct | BH 2.7.1 |
| l18 | summary.ideas[1] | Knowing host: 1/2 from car 1, 1 from car 2, so 2/3 | correct | Bayes |
| l18 | summary.ideas[2] | Random host who shows a goat gives 1/2 each | correct | script |
| l18 | summary.formula | Bayes with likelihoods 1/2, 1, 0 gives 2/3 | correct | Arithmetic |
| l18 | summary.trap | Equal priors stay equal only if the evidence is equally likely under each | correct | Odds form |
| l18 | quiz[0] | Four doors, one goat opened, random switch: 3/8; slips 1/4, 1/3, 3/4 | correct | 3/4 times 1/2. Unconditional, so no tie-break needed |
| l18 | quiz[1] | Lazy host opens 3: switching wins 1/2 | correct | Likelihoods 1 and 1. script |
| l18 | quiz[1].options sure.why | Had he opened door 2 switching would win for sure | correct | Door 2 opened only when the car is at 3 |
| l18 | quiz[2] | Lazy host opens 2: switching to 3 wins with chance 1 | correct | Same |
| l18 | quiz[3] | A trade with a better-informed client is more likely on the wrong side | correct | Adverse selection; Glosten and Milgrom (1985) |
| l19 | screens[1] | A gold coin most likely came from GG | correct | Likelihoods 1 against 1/2 |
| l19 | screens[2].prose | Each of six coins has chance 1/6 | correct | 1/3 times 1/2 |
| l19 | screens[2].widget, explain | Three gold coins, each 1/3 after seeing gold | correct | Equal joint chances renormalised |
| l19 | screens[3] | Two of three gold coins have a gold partner: 2/3 | correct | Bertrand (1889); BH ch. 2 exercises; script |
| l19 | screens[4].canvas | Tree leaves 1/3, 1/6, 1/6, 1/3 | correct | Products |
| l19 | screens[4].widget, feedback | P(GG | gold) = 2/3; 1/3 is the prior or the path | correct | (1/3)/(1/2) |
| l19 | screens[5] | Second GS box: 1/2; coins 4 gold, 2 with gold partner | correct | (1/4)/(1/4+1/8+1/8). script |
| l19 | screens[5].feedback boxes | 1/3 counts GG as one of three boxes with gold | correct | Slip matches value |
| l19 | screens[6].options right, explain | GG twice as likely to hand you gold; odds 1:1 to 2:1 | correct | Odds form |
| l19 | screens[6].options fifty.why | Boxes equally likely before the draw, not after | correct | Posterior 2/3, 1/3 |
| l19 | screens[7].prose, key 0.5, wrong 0.6667 | Clerk "tells you" the box holds at least one gold coin; GG has chance 1/2 | imprecise | Right only if the clerk's rule is to answer "any gold?". A clerk who names the colour of a coin he sees gives 2/3, the option marked wrong. script. F3 |
| l19 | screens[7].hints[2] | The clerk would say this for GG and GS alike | imprecise | The needed assumption appears only in the last hint. F3 |
| l19 | screens[7].explain | Likelihood ratio 1; how you learn "gold" changes the answer | correct | Given the rule |
| l19 | screens[8].prose | Odds form is the tool from level 2 | correct | Course map: l10 odds form is level 2 |
| l19 | screens[8].widget (order) | Prior odds, likelihood ratio, posterior odds, probability | correct | Each line needs the one before |
| l19 | screens[8].explain | Odds 2:1 mean 2/3; ratio 1 leaves 1:1 | correct | o/(1+o) |
| l19 | screens[9] | Share classes: 8 great, 6 with a great sister: 3/4; slips 3/5, 1/2, 3/10 | correct | 3x2 + 2x1 = 8. script |
| l19 | screens[9].feedback half | A both-great fund is twice as likely to be reported | correct | 2 great classes of 2 against 1 of 2 |
| l19 | summary.ideas[0], [1] | Count coins not boxes; odds 1:1 to 2:1 | correct | As above |
| l19 | summary.ideas[2] | A report about the whole box fits GG and GS equally: 1/2 | imprecise | Depends on the reporter's rule. F3 |
| l19 | summary.trap | "GG or GS, so 50:50" counts boxes | correct | |
| l19 | quiz[0] | Three cards, random side up, red: 2/3 | correct | Same structure; BH ch. 2 |
| l19 | quiz[1] | P(gold) before looking = 1/2 | correct | Total probability |
| l19 | quiz[2] | GGG against GSS: 3/4; odds 3:1 | correct | 1 against 1/3 |
| l19 | quiz[3] | Dealer "says" at least one red side: 1/2; 2/3 marked wrong | imprecise | Same as the clerk. F3 |
| l20 | screens[1] | Elder is a boy: P(BB) = 1/2 | correct | BH 2.2.5 |
| l20 | screens[1].explain | The younger child is still a fair coin | correct | Independence |
| l20 | screens[2].prose | "you only learn that at least one child is a boy" | imprecise | How it was learnt is not said; 1/3 needs a yes to "is at least one a boy?". BH 2.2.6; Bar-Hillel and Falk (1982). script. F4 |
| l20 | screens[2].widget | Families still possible: BB, BG, GB | correct | Event {at least one boy} |
| l20 | screens[3].prose | The three stay equally likely after the news | imprecise | Only under the yes/no protocol. F4 |
| l20 | screens[3].widget | 1/3; 1/2 and 1/4 marked wrong | imprecise | 1/2 is right if the fact came from a randomly chosen child. F4 |
| l20 | screens[3].explain | "The elder is a boy" gave 1/2 because it also rules out GB | correct | |
| l20 | screens[4] | Meet a random child, a boy: P(BB) = 1/2; tree leaves 1/4, 1/8 ... | correct | BH 2.2.6. script |
| l20 | screens[4].explain | Same fact, different route: the route is part of the evidence | correct | Likelihood principle |
| l20 | screens[5] | Exactly one boy has chance 1/2; counts 0, 1, 2 are not equally likely | correct | Binomial(2, 1/2) |
| l20 | screens[6].options right, explain | "The other child" names no definite child | correct | Standard diagnosis; BH 2.2.5 |
| l20 | screens[6].options fifty | 1/2 marked wrong, "holds only once a particular child is known to be a boy" | imprecise | 1/2 also holds when the news came from a random child; depends on screen 2's unstated protocol. F4 |
| l20 | screens[6].options indep.why | The children are independent; the problem is which child the news is about | correct | Stated model |
| l20 | screens[7].widget code | Both filters; 9 tests; isclose | correct | Ran solution 9/9, starter 0/9. script |
| l20 | screens[7].explain | Seed 4 gives 0.330 and 0.492 | correct | Ran: 0.32979, 0.49198 |
| l20 | screens[8].widget (order) | Definition, BB within A, complement, numbers | correct | "comp" already uses 1/4, so it follows "inside" |
| l20 | screens[8].explain | For "the elder is a boy" the bottom is 1/2 | correct | |
| l20 | screens[9].prose, key | Trader "tells you only: at least one of my trades made money": 3/7 | imprecise | Same protocol gap; a trader who reports on a random trade gives 0.6 (quiz[2]). F4 |
| l20 | screens[9].widget numbers | 0.36/0.84 = 3/7; slips 0.6, 0.36, 0.5 | correct | script |
| l20 | screens[9].explain | A trader who chooses which fact to report chooses your filter | correct | |
| l20 | summary.ideas[0] | Ordered pairs are equally likely; counts are not | correct | |
| l20 | summary.ideas[1] | "At least one is a boy" leaves three families: 1/3 | imprecise | F4 |
| l20 | summary.ideas[2] | Meeting a boy at random gives 1/2 | correct | |
| l20 | summary.formula | P(BB)/(1 − P(GG)) = 1/3 | correct | Conditional probability of the event |
| l20 | summary.trap | 1/2 assumes the news named a child | imprecise | Or that it came from a random child. F4 |
| l20 | quiz[0] | Three children, "you learn" at least one boy: 1/7 | imprecise | Value right for the event; protocol unstated. F4 |
| l20 | quiz[1] | Younger is a girl: both girls 1/2 | correct | |
| l20 | quiz[2] | Random trade reported as a winner: 0.6; Bayes check 0.36/(0.36+0.24) | correct | script |
| l20 | quiz[3] | HH, HT, TH, TT are the equally likely single outcomes | correct | |
| l21 | screens[0].prose | Last lesson "at least one is a boy" gave 1/3 | imprecise | Inherits F4 |
| l21 | screens[1] | Morning boy: chance of two boys is higher than 1/3 | correct | 3/7 under the yes/no protocol; BH 2.2.7 |
| l21 | screens[1].prose | "You learn: at least one child is a boy born in the morning" | imprecise | Protocol stated only in quiz[1]. F4 |
| l21 | screens[2] | 4 + 4 − 1 = 7 families fit | correct | Inclusion and exclusion. script |
| l21 | screens[3] | 3 of 7 are two-boy families | correct | script |
| l21 | screens[4] | 196 families; 14 + 14 − 1 = 27 fit; slips 28, 14, 26 | correct | script |
| l21 | screens[5] | 13 of 27 have two boys, about 0.481 | correct | script |
| l21 | screens[6].options right | Two-boy family fits "almost twice as often" | correct | 13/49 against 7/49 |
| l21 | screens[6].options exact-half.why | Both boys could be Tuesday boys, shared cell counts once | correct | |
| l21 | screens[6].options tuesday.why | Every day gives 13/27; rarity is what matters | correct | Symmetry |
| l21 | screens[6].hints, explain | 1 − (6/7)^2 = 13/49; prior odds 1:2 times 13/7 = 13:14 | correct | Arithmetic |
| l21 | screens[6].explain | The day is independent of the sibling but not of how the family fits the news | correct | |
| l21 | screens[7] | (2k−1)/(4k−1) rises from 1/3 towards 1/2 | correct | Enumerated for k = 1, 2, 3, 4, 6, 7, 12, 365. script |
| l21 | screens[7].explain | A birth time to the second picks out one child | correct | Limit of the formula |
| l21 | screens[8].widget (order), explain | Cross 4k−1, two-boy cells 2k−1, ratio, check | correct | |
| l21 | screens[9].prose, key "About 0.60" | Risk report "says: at least one trade made money, and it was placed at 10:17" | imprecise | 779/1299 holds only for a yes to a question fixed on 10:17. A report that names a winner's minute gives 3/7, the option marked wrong, by the lesson's own quiz[1]. script. F5 |
| l21 | screens[9].explain | Exact 779/1299 ≈ 0.5997 | correct | Under the yes/no filter. script |
| l21 | screens[9].explain | Before you condition on a reported fact, ask what procedure produced it | correct | And the item should say which. F5 |
| l21 | summary.ideas[0..2] | 27 of 196, 13 two-boy; rarer detail, closer to 1/2 | correct | For the yes/no protocol |
| l21 | summary.formula | (2k−1)/(4k−1); k = 1, 7, large | correct | script |
| l21 | summary.trap | Independence of the children is not irrelevance of the news | correct | |
| l21 | quiz[0] | January boy: 23/47 | correct | k = 12 |
| l21 | quiz[1] | Parent picks a son at random and names his weekday: 1/3 | correct | Likelihood 1/7 for every family with a son. script |
| l21 | quiz[1].options half.why | A mixed family is just as likely to produce this report | correct | |
| l21 | quiz[1].explain | 13/27 only when the words answer "is at least one a Tuesday boy?" | correct | The protocol statement the lessons need earlier |
| l21 | quiz[2] | 1 May gives 729/1459 ≈ 0.4997; "some day" gives 1/3 | correct | k = 365, k = 1 |
| l21 | quiz[3] | Three shifts: 5/11 | correct | k = 3 |
| l22 | screens[0] | Fair coin after five tails: next head 1/2 | correct | Independence; Feller X |
| l22 | screens[0].canvas | Walk ends 1, 0, −1, −2, −3, −4: five tails | correct | Read the values |
| l22 | screens[0].options hot.why | We know the coin is fair, so its chance does not drift | correct | Hypothesis stated |
| l22 | screens[0].options rare.why | Five tails have happened; only the sixth toss is uncertain | correct | |
| l22 | screens[1].explain | 1 in 32 trials kept, about 312 of 10,000 | correct | 10,000/32 = 312.5. script MC |
| l22 | screens[2] | P(head | five tails) = (1/64)/(2/64) = 1/2; slips 1/64, 1/32, 63/64 | correct | |
| l22 | screens[2].explain | Condition left the chance unchanged, so the tosses are independent; expecting a head is the gambler's fallacy | correct | Definition of independence |
| l22 | screens[3].canvas, hints | Gap −6, share 0.470 at 100; gap −24, share 0.488 at 1,000 | correct | Read from stored series. script |
| l22 | screens[3].options neither.why | After about 300 tosses the share stays within a few hundredths of 0.5 | correct | Max deviation 0.019 after 300 |
| l22 | screens[3].explain | Share = 1/2 + gap/(2n); n grows faster than the gap | correct | H = (n + gap)/2; gap is of order root n (Feller III) |
| l22 | screens[3].explain | The gap is diluted, not compensated | correct | Feller X; script MC |
| l22 | screens[4].widget | 47.5, 5, 0.475; 497.5, 5, 0.4975 | correct | script MC 4.999, 0.475 |
| l22 | screens[4].explain | Share heads for 1/2 only because 5 is divided by more tosses | correct | 1/2 − 2.5/n |
| l22 | screens[5] | 21/47 ≈ 0.447; black more likely after reds | correct | Sampling without replacement |
| l22 | screens[5].explain | Draws without replacement are dependent | correct | |
| l22 | screens[6] | P(tail-heavy | five tails) = 243/275 ≈ 0.884; odds 1.5^5 | correct | script |
| l22 | screens[6].explain | Next toss a tail with chance about 0.72; a streak is evidence about the coin | correct | 0.8836x0.75 + 0.1164x0.5 = 0.721 |
| l22 | screens[7] | Next bet wins 1/2; stake does not change the chance | correct | |
| l22 | screens[8].widget (order), explain | E[H] = n/2; share = 1/2 − 2.5/(n+5); expected gap stays 5 | correct | Algebra; linearity |
| l22 | screens[8].explain | The law of large numbers works by dilution, not compensation | correct | Feller X |
| l22 | screens[9] | Doubling, cap six: 63/64 x 1 − 1/64 x 63 = 0 | correct | Optional stopping, bounded; Williams 10.10 |
| l22 | screens[9].explain | Ten doublings: £1,023 with chance 1/1024, still zero | correct | 2^10 − 1 |
| l22 | screens[10] | Independent days: P(up | five falls) = 0.53 | correct | Given the stated record |
| l22 | screens[10].explain | A bounce is due only under mean reversion, a dependence you must measure | correct | |
| l22 | summary.ideas[0] | Fair coin has no memory | correct | |
| l22 | summary.ideas[1] | "The gap between heads and tails does not shrink back" | imprecise | Nothing pulls it back, but it returns to 0 with probability 1 (Feller III.2) and is smaller at 1,000 than at 100 in about 17% of paths. script. F9 |
| l22 | summary.ideas[2] | The past matters with dependent draws or an unknown coin | correct | |
| l22 | summary.formula, trap | P(head | any run) = 1/2; a fair bet keeps no account | correct | |
| l22 | quiz[0] key | 18/37 ≈ 0.4865 | correct | |
| l22 | quiz[0].wrong left 0.4737 with feedback "took the eight blacks out" | Slip value matches its diagnosis | wrong | 0.4737 is 18/38, a wheel with two greens. Removing eight blacks gives 18/29 = 0.6207. F8 |
| l22 | quiz[1] | "Due" holds for cards without replacement and a reverting spread | correct | |
| l22 | quiz[2] | Ten heads then 990 tosses: 0.505 | correct | |
| l22 | quiz[3] | Cap four: +£1 with 15/16, −£15 with 1/16; EV 0 | correct | |
| l23 | screens[0] | Prosecutor's 1 in a million is far too low | correct | BH 2.8.1 |
| l23 | screens[0].explain | About 5 innocent matches; defendant is one of about 6 | correct | 4,999,999 x 10^-6; uniform prior stated ("no other evidence") |
| l23 | screens[1].canvas, key | P(culprit | match) = 1/(1+N) with N in millions; 1/6 at 5 million | correct | Culprit matches surely |
| l23 | screens[1].explain | The bigger the pool, the weaker the same match | correct | |
| l23 | screens[2] | P(innocent | match) ≈ 5/6; slips 10^-6, 1/6, 0.9999998 | correct | script |
| l23 | screens[2].explain | Swapping P(match | innocent) for P(innocent | match) is the prosecutor's fallacy | correct | BH 2.8.1; Thompson and Schumann (1987) |
| l23 | screens[3] | Ten suspects: about 0.99999; odds 1:9 times 10^6 = 111,111:1 | correct | 1/1.000009 |
| l23 | screens[4] | 1 in 10 million test: 2/3 | correct | 1/1.5 |
| l23 | screens[4].explain | Posterior depends on pool size times match rate | correct | 1/(1 + N p) |
| l23 | screens[5] | Lab's figure is P(match | innocent); other options are P(innocent | match), prior, P(match) | correct | |
| l23 | screens[5].explain | The two differ because innocent people vastly outnumber culprits | correct | Base rate |
| l23 | screens[6].widget (order), explain | Prior odds 1/4,999,999 times 10^6 ≈ 0.2, so 1/6 | correct | |
| l23 | screens[7].prose | A p-value is P(result this good | no edge) | imprecise | Standard: a result at least this extreme (Casella and Berger 8.3.4). "this good" passes if read as "this good or better". F10 |
| l23 | screens[7] | 1,000 null strategies, expect 10 with p < 0.01 | correct | Uniform p under the null; linearity needs no independence. script MC 0.0102 |
| l23 | screens[7].explain | Test enough strategies and false discoveries are all but certain | correct | 1 − 0.99^1000 if independent |
| l23 | screens[8] | P(no edge | pass) = 9.8/19.8 ≈ 0.495 | correct | script MC 0.500 |
| l23 | screens[8].explain | A p-value of 0.01 is P(result | no edge) | imprecise | F10 |
| l23 | summary.ideas[0], [1] | The two conditionals differ; pool times rate gives innocent matches | correct | |
| l23 | summary.ideas[2] | "A p-value is the chance of the result given no edge" | imprecise | The chance of the exact result is not the p-value. F10 |
| l23 | summary.formula, note | Odds form; huge LR on tiny prior odds leaves a modest posterior | correct | |
| l23 | quiz[0] | Defence: match multiplied the odds a million-fold; dismissing it is the mirror-image fallacy | correct | BH 2.8.2 |
| l23 | quiz[1] | 200,000 pool at 1 in 100,000: 1/3 | correct | |
| l23 | quiz[2] | 5% of healthy positive = P(positive | healthy) | correct | |
| l23 | quiz[3] | 200 null strategies at 0.05: 10 kept | correct | |
| l24 | screens[0] | Rates 0.95, 0.90, 0.60, 0.50; A better in both groups | correct | |
| l24 | screens[1] | Overall 275/400 = 0.6875, 320/400 = 0.80; reversal is Simpson's paradox | correct | BH 2.8.3 |
| l24 | screens[2] | A overall = 0.95(1−w) + 0.60w; beats 0.80 below about 43% | correct | w = 3/7 |
| l24 | screens[2].explain | Severity drives both who gets A and who recovers | correct | Stated story: a confounder |
| l24 | screens[3] | A was given mostly severe cases; "three times as many" | correct | 300 against 100 |
| l24 | screens[3].explain | Comparing overall rates compares the case mix as much as the treatments | correct | For a pre-treatment variable |
| l24 | screens[4] | Same mix: B overall 0.60; same weights cannot reverse | correct | Weighted averages with equal weights |
| l24 | screens[5] key | High-risk patient: choose Y (0.75 against 0.70) | correct | Own-stratum rate; risk is fixed before the choice |
| l24 | screens[5].explain | "Always compare like with like before you read an overall rate" | imprecise | Right only when the split variable is fixed before the choice. If the choice changes the variable, the overall rate is the right one (Pearl 6.1). script MC both ways. F6 |
| l24 | screens[6].widget (order), explain | Overall rate = weighted average with each treatment's own weights | correct | Algebra |
| l24 | screens[7] | Traders: 0.46, 0.59 overall; 0.55, 0.50 at a 50–50 mix | correct | |
| l24 | screens[7].explain | Compare traders at the same mix of conditions | correct | Regime precedes the trade |
| l24 | screens[8] | P wins each year, Q wins pooled (0.52 against 0.48) | correct | |
| l24 | summary.ideas[0], [1] | Win every group and lose overall; overall = weighted average | correct | |
| l24 | summary.ideas[2] | Needs a hidden variable that changes mix and outcome; cannot happen with the same mix | correct | Arithmetic condition |
| l24 | summary.trap | Comparing overall rates without checking the mix | imprecise | No word on when the split is the wrong table. F6 |
| l24 | quiz[0] | 380/800 = 0.475 | correct | |
| l24 | quiz[1] | Same mix: C must win overall | correct | |
| l24 | quiz[2] | Lighters and lung disease: smoking drives both | correct | Confounding |
| l24 | quiz[3] | First desk 0.625 against rival 0.61 | correct | 250 and 244 of 400 |
| l25 | screens[0] | Survivors' 7% is probably too high | correct | Brown et al. (1992) |
| l25 | screens[0].explain | Funds usually close after poor returns | correct | Empirical: Brown et al. (1992); Elton, Gruber and Blake (1996) |
| l25 | screens[1].explain | Closure was not random: it picked out the losers | correct | In the table |
| l25 | screens[2] | E[R | survived] = 49/7 = 7 | correct | |
| l25 | screens[3] | E[R] = 24/10 = 2.4; overstatement 4.6 points | correct | script |
| l25 | screens[4] | E[R | closed] = −25/3; 0.7x7 + 0.3x(−8.33) = 2.4; "total probability, applied to averages" | correct | Law of total expectation |
| l25 | screens[5] | Random closure: no bias on average | correct | Simple random sample mean is unbiased. script MC 2.385 |
| l25 | screens[5].explain | Bias comes from closure that depends on returns, not closure itself | correct | |
| l25 | screens[6] | 7 of 10 beat cash; P(beat | survived) = 1 | correct | |
| l25 | screens[7].widget (order) | E[R] − E[R|S] = P(S^c)(E[R|S^c] − E[R|S]) = −4.6 | correct | Algebra |
| l25 | screens[7].lines read | Survivors overstate whenever closed funds did worse | correct | Sign of the bracket |
| l25 | screens[8] | Original members 6%; today's members 11.2%; all 120 give 8.33% | correct | script |
| l25 | screens[8].explain | Today's constituents are look-ahead | correct | Standard backtest bias |
| l25 | screens[9] | All 20 strategies: −0.25% | correct | |
| l25 | summary.ideas[0], [2] | E[R | survived] is not E[R]; unrelated failure gives a fair sample | correct | |
| l25 | summary.ideas[1] | "When failure depends on the outcome, survivors overstate" | imprecise | Direction needs failures to have done worse; if winners leave the sample the survivors understate. script MC. F7 |
| l25 | summary.formula, note | Gap formula; zero when closure does not depend on returns | correct | |
| l25 | quiz[0] | Bombers: armour the engines | correct | Wald (1943), SRG memo; Mangel and Samaniego (1984) |
| l25 | quiz[1] | 0.6x9 − 0.4x3 = 4.2; overstated by 4.8 | correct | |
| l25 | quiz[2] | Random loss: unbiased, noisier | correct | |
| l25 | quiz[3] | Book measures P(left early | success), not P(success | left early) | correct | |
| l26 | screens[0] | P(up | flash) = 0.6 | correct | 0.3/0.5 |
| l26 | screens[0].explain | Hit rate equals detection rate only because prior is 50–50 and false alarms are 40% | correct | Needs prior 1/2 and detection + false alarm = 1. script |
| l26 | screens[1] | Detection 40% with 40% false alarms leaves the view unchanged; 50% gives 0.556 | correct | LR 1; 0.25/0.45 |
| l26 | screens[2] | Likelihood ratio 0.6/0.4 = 1.5 | correct | |
| l26 | screens[3] | 55% prior: 11/17 ≈ 0.6471; slips 0.6, 0.55, 0.825, 1.8333 | correct | script |
| l26 | screens[3].explain | Always start from the base rate | correct | |
| l26 | screens[4] | Two conditionally independent flashes: 9/13 | correct | script exact and MC 0.693 |
| l26 | screens[4].explain | Multiplication valid only if independent given the day | correct | Naive Bayes condition |
| l26 | screens[5] | A copy adds nothing: 0.6 | correct | script MC 0.600 |
| l26 | screens[5].explain | Correlated signals count as fewer | correct | For positive dependence given the day, the usual case |
| l26 | screens[6] | 60% detection, 60% false alarm: stays 0.55 | correct | LR 1 |
| l26 | screens[7].widget (order), explain | 1.5^n ≥ 4, n ≥ 3.42, so 4; 0.771, 0.835 | correct | script |
| l26 | screens[8].prose | Kelly stakes 2p − 1 at even money; maximises growth of log wealth | correct | Kelly (1956); Thorp (2006) section 2. script grid search |
| l26 | screens[8].widget | £2,000; slips £6,000, £10,000, £1,000 | correct | |
| l26 | screens[8].explain | True 0.55 gives 0.1: betting double what the edge supports | correct | |
| l26 | screens[9] | 11/9 x 1.5 x 7/3 = 77/18, p = 77/95 | correct | script |
| l26 | summary.ideas[0..2], trap | LR moves the view; base rate in odds; out of sample | correct | |
| l26 | summary.formula.note | Kelly 2p − 1 on a repeated even-money bet with known p | correct | Hypotheses stated |
| l26 | quiz[0] | 40% prior, LR 1.5: 0.5 | correct | |
| l26 | quiz[1] | "70% detection rate on up days" = P(flash | up) | correct | |
| l26 | quiz[2] | Best of 200 designs: expect lower on new data | correct | Selection bias; Harvey, Liu and Zhu (2016). script MC 0.580 in, 0.550 out |
| l26 | quiz[3] | Kelly at 0.55: 0.1 | correct | |
| review-4 | items[0] key, prose | Stay wins 1/3; tie-break not stated | imprecise | 1/2 (marked wrong) is right for the lazy host the lesson teaches. F2 |
| review-4 | items[0].options half.why, explain | "The host can show a goat whatever is behind door 1, so his move says nothing about it" | misleading | Invalid inference, as in l18. F2 |
| review-4 | items[1] | Two boxes GG, GS: 2/3 | correct | |
| review-4 | items[2] | Random host, goat shown: 1/2 | correct | |
| review-4 | items[3] | Silver drawn: 2/3 by symmetry | correct | |
| review-4 | items[4] | Younger is a boy: 1/2 | correct | |
| review-4 | items[5] | "You learn that at least one is a girl": 1/3 | imprecise | F4 |
| review-4 | items[6] | Winter boy: 7/15 | correct | k = 4; protocol as F4 |
| review-4 | items[7] | Exactly 1/2: random host, elder boy, clerk; not knowing host, at least one, drawn coin | imprecise | Clerk and "at least one" options carry F3 and F4 |
| review-4 | items[7].explain | In each half case the evidence is equally likely under the two hypotheses left | correct | |
| review-5 | items[0] | Fair die after 20 rolls without a 6: 1/6 | correct | |
| review-5 | items[1] | 1 fraud among 51 flags: 1/51 | correct | |
| review-5 | items[2] | 115/200 = 0.575 | correct | |
| review-5 | items[3] | 2% for all 20 funds; overstated by 4 points | correct | |
| review-5 | items[4] | 30% prior, LR 2: 6/13 | correct | |
| review-5 | items[5] | Unfair doubling, cap three: −0.331; "loses 10p per £1 staked" | correct | Expected stake 3.31 times −0.1 |
| review-5 | items[6] | A's forecasts were weighted towards the group where errors are common | correct | A reversal forces both models to agree on the harder group and A to weight it more (derivation in audit notes) |
| review-5 | items[6].options worse.why | Like for like, A is better | correct | Cap size is fixed before the forecast |
| review-5 | items[7] | p = 0.02: a result this good about 2% of the time with no edge | correct | Casella and Berger 8.3.4 |
| review-5 | items[7].explain | P(no edge | result) depends on how many were tried and how rare real edges are | correct | Selection of the reported result; base rate |
| homework-4 | items[0] | Four doors, two goats opened: 3/4 | correct | Unconditional |
| homework-4 | items[1] | 1/(1+q); from 1 to 1/2; switching never hurts | correct | script |
| homework-4 | items[2] | Second coin gold: 2/3 | correct | script |
| homework-4 | items[3] | "He reports only: at least one won": 121/319 | imprecise | Value right for the filter; protocol as F4 |
| homework-4 | items[4] | Left-handed boy: 19/39 | correct | script; protocol as F4 |
| homework-4 | items[5] | (2−q)/(4−q); q = 1, 1/7, to 0 | correct | script |
| homework-4 | items[6] | E[value | buy] = 100.20, the break-even ask | correct | Glosten and Milgrom (1985). script |
| homework-4 | items[7].model (a), (b), (c) | 13/27, 1/2, 1/3 with likelihoods 13/49 and 1/7; 1/7 and 1/14; 1/7 and 1/7 | correct | Enumerated. script |
| homework-4 | items[7].model, why | The procedure that produced the words fixes the likelihoods | correct | |
| homework-4 | items[8] code | Three hosts; 11 tests; "three check host_likelihood, eight check door_posterior" | correct | Ran solution 11/11, starter 0/11; hand-checked tests 2, 5 to 11 |
| homework-4 | items[8].feedback test-2 .. test-11 | Each line describes its test | correct | Checked against the test list (1-based) |
| homework-4 | items[8].explain | The goat matters for the random host | correct | |
| homework-5 | items[0] | Heavy coin after four heads: next head 0.6587 | correct | script |
| homework-5 | items[1] | 300,000 pool at 1 in 50,000: 1/7 | correct | |
| homework-5 | items[2] | M 0.65, 0.625; N 0.667, 0.55; 89% of N's trades in bull markets | correct | |
| homework-5 | items[3] | Gap 0.4 x 13 = 5.2 points | correct | |
| homework-5 | items[4] | A and B count, C is a copy: 0.661; with C 0.745 | correct | |
| homework-5 | items[5] (order) | Doubling proof: 2^j − 1 lost, win nets +1, EV 0 for any cap | correct | Algebra |
| homework-5 | items[6] code | share_after_run; 5 tests; overlapping runs | correct | Ran solution 5/5, starter 0/5 (ZeroDivisionError) |
| homework-5 | items[6].feedback, explain | 0.513 on 200,000 seeded tosses; converges to exactly 1/2 | correct | Ran: 0.512913. Limit by the strong law; finite-sample streak bias (Miller and Sanjurjo 2018) is of order 1/n here |
| homework-5 | items[7].model (a), (b) | Prosecutor's fallacy; 6/10.9 ≈ 0.55; odds 600/490 | correct | |
| homework-5 | items[7].model (c), rubric[5] | Claim gets closer to true "when fewer designs are tried" | imprecise | At a fixed share of real edges the posterior does not depend on the number tried. script. F11 |
| problems-4 | items[0] parts 1 to 4 | 0.5; 0.4; 1/(1+3h); h = 0.5; h = 1 gives 1/4 | correct | script |
| problems-4 | items[0].parts[1].feedback bags | 0.25 also from dividing by 0.8 | correct | 0.2/0.8 |
| problems-4 | items[1] parts 1 to 4 | 0.91; 0.455; 7/13; 7/22; slips | correct | script |
| problems-4 | items[1].parts[2].explain | A winner named at random tells you no more than "at least one won" | correct | 0.245/0.455 = 0.49/0.91 |
| problems-4 | items[2] parts 1 to 5 | 1/3 (question stated); 23; 11/23; 1/2; k = 13 | correct | script; protocol stated properly here |
| problems-4 | items[3] parts 1 to 5 | 0.8; 0.19; 19/24; 2 − 1/k; limit 0.8 | correct | script |
| problems-5 | items[0] parts 1 to 4 | 0.3125; swap; 40/51; Kelly 29/51 | correct | script |
| problems-5 | items[0].parts[3].explain | On one flag 2p − 1 is negative, so Kelly stakes nothing on a warning | correct | Thorp (2006): no bet without an edge |
| problems-5 | items[1] parts 1, 2, 4 | 4.4; 5 points; 32 funds | correct | script |
| problems-5 | items[1].parts[2] | Simpson's paradox with survival as the hidden variable | imprecise | Does not say that here the overall average is the fair one, since survival is a result of the returns. The level's rule "always compare like with like" would pick S. F6 |
| problems-5 | items[2] parts 1 to 5 | 0.6; 0.4096; 0.2906; 0.5291; 0.0582 | correct | script |
| problems-5 | items[2].parts[4].explain | With an unknown edge a losing run is a reason to stake less | correct | Kelly on the predictive chance |
| problems-5 | items[3] parts 1, 2 | EV 0; (31/32)^20 ≈ 0.5299 | correct | script |
| problems-5 | items[3].parts[2] | Stopping rule looks only at the past, so all traders average £0; quitters −22.55 | correct | Optional stopping, bounded (Williams 10.10). script exact −22.549, MC −22.57 |
| problems-5 | items[3].parts[3] | Newsletter conditions on survival; doubling changes the shape of risk, not its average | correct | |
