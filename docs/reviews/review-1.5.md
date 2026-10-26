# Topic 1.5 (probability): second-reader findings

Scope: every lesson, review and homework file in `counting-chance`, `conditional`, `random-vars`, `limits-thm`, `markov`, plus `app/content/exams/topic-1.5.json`.
Method: every stated number recomputed (Python fractions/scipy/numpy, exhaustive enumeration where small); seeded engine simulations reproduced with the engine's mulberry32 (`simh.js`, `runsim.js`, `walksim.js`, `walkpath.js`); Python `random.Random(seed)` claims re-run; distractor values re-derived from their `why`; tolerance overlaps scanned (`tolcheck.py`); style scanned (`style.py`, `sentcount.py`).
Format: `path | screen/item | severity | what is wrong | fix`. Severity: error = wrong number, false claim or wrong grading; warning = weak explanation or teaching issue; note = style.

## counting-chance

- app/content/courses/counting-chance/l1-every-outcome.json | screens[6] trap, screens[5] | warning | The lesson asks for a chance (6/36) and uses P(·) before l2 introduces P(E) = |E|/|S|; the trap's explain says Sam's 21 outcomes "do not each stand for one roll" rather than naming the fault (they are not equally likely). | "Sam's {3, 4} holds two rolls but {3, 3} holds one, so his 21 outcomes are not equally likely."
- app/content/courses/counting-chance/l1-every-outcome.json | summary.trap | note | 22-word sentence. | "Merging (3, 4) and (4, 3) gives 21 outcomes. Chances worked out from that list come out wrong."
- app/content/courses/counting-chance/l2-equally-likely.json | screens[0] feedback.correct | warning | "7 comes up about six times as often as 2 or 12": the seeded run on screen (mulberry32 seed 11, 1,000 rolls) shows 7:166, 2:40, 12:30, i.e. 4.2x and 5.5x. | "In the long run 7 comes up six times as often as 2 or 12."
- app/content/courses/counting-chance/l2-equally-likely.json | screens[4] feedback.correct | note | "this coin has none" reads as "the coin has no chances". | "...and this coin's two faces do not have them."
- app/content/courses/counting-chance/l2-equally-likely.json | summary.trap | note | Over 20 words. | Split into two sentences.
- app/content/courses/counting-chance/l6-does-order-matter.json | screens[6] trap | warning | Kim's error (336 for the committee and 56 for the podium) is two opposite mistakes at once, a swap nobody makes; the common misconception is ordered counting for both. | Make Kim write 336 for both and key the trap on that.
- app/content/courses/counting-chance/l9-double-counting.json | screens[0]-[4] | warning | Re-teaches l3's two-event union almost line for line (terms re-bolded as new, same overlap trap); the new idea, three events, starts only at screen 6. | One recap screen, then spend the ladder on three events and on chances that are not counts.
- app/content/courses/counting-chance/l10-birthday.json | screens[9] canvas table, row "50 orders" | error | Clash chance for 50 orders with 10,000 codes printed as 0.1159; 1 - prod_{i<50}(10000-i)/10000 = 0.1155. | 0.1155
- app/content/courses/counting-chance/l10-birthday.json | quiz q-seven-rolls option 'ratio' (7/36) | warning | why "You treated it like one pair of rolls" — one pair matches with chance 1/6; no natural slip gives 7/36. | Value 7/6 with why "You added 1/6 for each roll", or 1/6 with the current why.
- app/content/courses/counting-chance/l10-birthday.json | screens[4] trap prose | note | "You join a room of 23 other people" then asks about "any two of the 23": the room now holds 24 (0.5383), easy to misread. | "A room holds 23 people. Will someone share one named person's birthday? Will any two share one?"
- app/content/courses/counting-chance/l10-birthday.json | screens[6] widget.how | note | "math.isclose" in prose without code formatting (flagged as American "math"). | `math.isclose`
- app/content/courses/counting-chance/l11-axioms.json | screens[2] prose | warning | Axiom 3 is stated only for two disjoint events and the screen says "Everything else is derived from these three". Kolmogorov's axiom is countable additivity; finite additivity does not support the lesson's own uniform-dart example or any later limit argument. | "3. If E1, E2, ... are disjoint, P(E1 ∪ E2 ∪ ...) = P(E1) + P(E2) + .... We mostly use it for two events."
- app/content/courses/counting-chance/l11-axioms.json | screens[4] option 'pos' why | note | "That is true, but it gives P(E) ≤ 1" is circular: it needs the complement rule being derived. | "That is true, but it does not turn P(E ∪ E^c) into a number."
- app/content/courses/counting-chance/l12-poker-hands.json | screens[2] wrong 'ordered' (2,496) | warning | 2,496 = 13 x 4 x 48, but the why says "You counted the four cards in order"; ordering multiplies by 24 (14,976). | Value 14,976, or why "You chose the suits of the four in 4 ways; all four suits are taken."
- app/content/courses/counting-chance/homework-2.json | h-at-least-one-formula explain | error | "For n < 4 it gives 0": at n = 0 the polynomial gives (-1)(-2)(-3)/6 = -1. | "For n = 1, 2 or 3 it gives 0."
- app/content/courses/counting-chance/review-3.json | r-months explain | note | "Five people and 12 slots behave like 23 people and 365 days": 0.618 against 0.507 overstates the match. | "Five people already pass one half, as 23 do with 365 days."
- app/content/courses/counting-chance/review-3.json | items[6] explain | note | Four sentences (limit 3). | Merge the suit and total sentences.
- app/content/courses/counting-chance/homework-3.json | items[0] explain | note | Four sentences (limit 3). | Merge "Pairs" and "Triple" into one sentence.
- app/content/courses/counting-chance/l5-in-stages.json, l6-does-order-matter.json, l12-poker-hands.json | screens[7]/[7]/[8] generalise prose | note | 30-33-word sentences around display formulas. | Break before each display.

## conditional

- app/content/courses/conditional/l2-counting-left.json | whole lesson | warning | Re-teaches counting-chance l7: same bag (3 red, 2 blue), same tree, same 0.3, same two-aces quiz trap. "Multiplication rule" also names the counting rule n1 n2 ... from counting-chance l5, with no bridge. | New bag or explicit link ("In Counting and Chance you multiplied 3/5 by 2/4; that second factor was a conditional probability"); call it the multiplication rule for probabilities.
- app/content/courses/conditional/l7-turning-around.json | quiz q-equal-sizes explain; summary.ideas[2] | warning | "The two directions agree only when the two events are equally likely" is false when P(A ∩ B) = 0 (both conditionals are 0). | "When P(A ∩ B) > 0, the two directions agree exactly when P(A) = P(B)."
- app/content/courses/conditional/l7-turning-around.json | screens[8] derive | warning | "Start with the line that contains P(B | A)": d1, d3 and d4 all contain it; d1 and d2 are interchangeable and forced by an ambiguous instruction. | Put d1 and d2 in a `same` group; drop the instruction.
- app/content/courses/conditional/l7-turning-around.json | screens[9] transfer explain | warning | "An 80% hit rate does not mean the signal is right 80% of the time it fires": on a desk the hit rate IS the share of signals that were right, P(up | fires). | "Firing on 80% of up days does not make the signal right 80% of the times it fires."
- app/content/courses/conditional/l8-base-rates.json | screens[4] wrong 'fp-rate' / 'joint' | note | 0.05 ± 0.0005 and 0.0495 touch at the boundary. | fp-rate tol 0.0002.
- app/content/courses/conditional/l10-odds-form.json | screens[6] trap | warning | The trap's wrong method (probability x likelihood ratio) gives 1.2, impossible on sight, and screen 4 already showed it. | Prior 10%, LR 3: wrong method 0.30, right 0.25.
- app/content/courses/conditional/l11-updating-twice.json | screens[4] explain canvas | warning | The key point at log-odds -6.846 is drawn off a number line that runs from -5 to 2. | Line min -7 (label 1:999), or a higher prior.
- app/content/courses/conditional/l12-many-hypotheses.json | screens[6] trap prose | note | "A coin is fair (chance 0.6), biased to heads (0.2)..." reads as chances of heads. | "Before any flip, the coin is fair with chance 0.6, heads-biased with chance 0.2 ..."
- app/content/courses/conditional/l13-knowing-nothing.json, l14-independent-trials.json and others | event names | note | Straight single quotes ('at least one') in some lessons, curly double quotes elsewhere. | One style, “...”, topic-wide.
- app/content/courses/conditional/l14-independent-trials.json | screens[5] explain | error | "We name it here and build it properly in Counting and Chance": that is the earlier course; the binomial is built in Distributions and Limit Theorems l1. | "...build it properly in Distributions and Limit Theorems."
- app/content/courses/conditional/l17-correlated-defaults.json | screens[5] numeric wrong 'recw' | error | Misconception value 0.0644 lies inside the answer tolerance (0.0646 ± 0.0005). The grader checks the answer first, so the misconception is marked correct and its feedback never fires. | Answer tol 0.0001 (true 0.064616); recw tol 0.00005.
- app/content/courses/conditional/l18-monty-hall.json | screens[7] explain | note | Four sentences. | Merge the two likelihood sentences.
- app/content/courses/conditional/l19-bertrands-box.json | screens[7] explain | note | Four sentences. | Trim to three.
- app/content/courses/conditional/l20-two-children.json | quiz q-coins-space option 'same-diff' | error | The question asks which list has every outcome equally likely; "Both the same, one of each" does (1/2 each), as the explanation itself says. A correct reading is marked wrong. | Ask for "each outcome a single result of the two tosses", or replace the distractor with "HH, one of each, TT".
- app/content/courses/conditional/l20-two-children.json | screens[7] explain | note | Five sentences. | Cut to three.
- app/content/courses/conditional/l21-tuesday-boy.json | screens[7], screens[9] explain | note | Four sentences each. | Trim to three.
- app/content/courses/conditional/l23-prosecutors-fallacy.json | screens[7] explain | note | "Test enough strategies and false discoveries are certain": 1 - 0.99^1000 = 0.99996, near certain, not certain. | "...are all but certain."
- app/content/courses/conditional/l23-prosecutors-fallacy.json | quiz q-pool byKey 'half' | note | why offers two different slips ("left out the culprit, or split 50-50"); neither cleanly gives 0.5 from 2 innocent + 1 culprit. | "You split the matches 50-50 between guilty and innocent."
- app/content/courses/conditional/l25-survivorship.json | screens[8] wrong 'all' (7.67%) | warning | 7.67% is the plain mean of the three group returns; the why "You averaged all 120 stocks" gives 8.33%. | Value 0.0833, or why "You averaged the three group returns equally".
- app/content/courses/conditional/l25-survivorship.json | screens[9] wrong 'sign' (6.25%) | error | "Added the abandoned strategies' losses as gains" gives (40 + 45)/20 = 4.25%; 6.25% matches no stated slip, so the learner gets only the generic line. | Value 0.0425.
- app/content/courses/conditional/l25-survivorship.json | screens[9] feedback.correct | note | "percent". | "per cent", or the % sign.
- app/content/courses/conditional/l26-trading-signal.json | summary.ideas[0], screens[6] trap, quiz[1] | warning | Defines "hit rate" as P(flash | up). On a desk the hit rate is the share of calls that were right, P(up | flash) — the posterior the lesson computes. The trap's "vendor's 60% hit rate" would normally mean the posterior. | Call P(flash | up) the detection rate in l7, l8 and l26; add "Desks quote a hit rate as P(up | flash)."
- app/content/courses/conditional/l26-trading-signal.json | screens[8] explain | warning | "If the 60% hit rate does not survive out of sample and your true chance is 0.55..." treats the hit rate as the win chance, contradicting the lesson's own definition. | "If the posterior of 0.6 does not survive out of sample..."
- app/content/courses/conditional/l26-trading-signal.json | screens[8] transfer | note | Kelly 2p - 1 given without its premise (maximises long-run growth over many repeated bets with known p). | Add that sentence.
- app/content/courses/conditional/l26-trading-signal.json | screens[0] wrong 'prior' / 'flash' | note | Both 0.5 with the same tolerance; the second never fires. | Drop one or change its value.
- app/content/courses/conditional/homework-1.json | h-three-hearts explain | error | "Item 7 shows why multiplying them is allowed": Item 7 is h-aces; the derivation is Item 8, h-order-three. | "Item 8 shows why..."
- app/content/courses/conditional/homework-2.json | items[1] wrong 'probs' / 'half' | note | 50 vs 49.5 overlap within tolerance. | Tighten tolerances.
- app/content/courses/conditional/homework-2.json | items[2] explain | note | Four sentences. | Trim.
- app/content/courses/conditional/homework-4.json | items[2] explain | note | Four sentences. | Trim.
- app/content/courses/conditional/review-2.json | items[1] wrong 'base' / 'joint' | note | Values overlap within tolerance. | Tighten.
- app/content/courses/conditional/review-4.json | items[7] explain | note | Four sentences. | Trim.
- app/content/courses/conditional/homework-5.json, l20-two-children.json | widget.how | note | "math.isclose" without code formatting. | `math.isclose`
- app/content/courses/conditional/l2-counting-left.json s7, l4-multiplication-rule.json s7, l23 quiz[0], l25 s6 | prose | note | 26-36-word sentences. | Split.

## random-vars

- app/content/courses/random-vars/l5-long-run-average.json | screens[6] explain | note | Four sentences. | Trim.
- app/content/courses/random-vars/l6-fair-price.json | screens[9] wrong 'one-up' (£40) | warning | why "You needed only one rise", but at least one rise in two days is 0.64 (£64); £40 is one day's chance. | why "You used one day's chance of a rise, 0.4."
- app/content/courses/random-vars/l7-linearity.json | screens[7] explain | note | "b = -1 scaling" reuses b, the shift in E[aX + b]. | "Y scaled by -1: E[X - Y] = E[X] + E[-Y]."
- app/content/courses/random-vars/l11-moving-together.json | screens[2] wrong 'count' (2) | warning | why "added the products without their chances" gives 1 + 1 - 1 - 1 = 0; 2 is the count of positive cells. | why "You counted the two positive cells", or value 0.
- app/content/courses/random-vars/l13-joint-tables.json | screens[8] explain | note | "Bayes on a trading signal, in the Conditional probability course, builds on this table": that course came first. | "You met this table as Bayes on a trading signal in Conditional Probability."
- app/content/courses/random-vars/l14-independent-rvs.json | screens[6] wrong 'var' (0.4444) | warning | why "That is not a covariance" names no mistake; 4/9 is E[Y]^2, not a variance (Var Y = 2/9, Var X = 2/3). | Value 0.6667 with why "That is Var(X)".
- app/content/courses/random-vars/l16-averaging-averages.json | screens[4] wrong 'third' (1.3333) | warning | why says dropping the 1 "only gives 1", so the named slip does not give 4/3 (4/3 = 1/(3/4)). | Value 1 with that why, or why "You took one over the chance of losing".
- app/content/courses/random-vars/l16-averaging-averages.json | screens[9] wrong 'half' | note | why "halves the right answer" names no mistake. | Drop it.
- app/content/courses/random-vars/review-2.json | items[8] r-call-tree byKey 'half' | note | "You gave up, up a chance of 0.5" reads as "gave up". | "You gave the path up-up a chance of 0.5."
- app/content/courses/random-vars/homework-1.json | items[6] explain | note | Four sentences. | Trim.
- app/content/courses/random-vars/homework-2.json | items[7] h-overround explain | warning | "the bookmaker's edge is about 5.56%" conflates overround with margin; on a balanced book the take is 1/19 = 5.26% of stakes. | "The overround is 5.56%; a balanced book keeps 1/19, about 5.26% of stakes."
- app/content/courses/random-vars/homework-3.json | items[3] h3-traders explain | note | "less than either trader's £4,000 plus £3,000" is muddled. | "well below the £7,000 you get by adding the sds."
- app/content/courses/random-vars/homework-4.json | items[5] h-ht wrong 'three' | note | why "the answer is not 3" names no mistake. | "3 assumes the tail follows the first head at once."
- app/content/courses/random-vars/homework-4.json | items[7] prose | note | 27-word sentence. | Split.

## limits-thm

- app/content/courses/limits-thm (all files) vs random-vars, markov | Var/Cov notation | warning | Three typesettings in one topic: \mathrm{Var} (random-vars, markov), \text{Var}, bare Var( and \operatorname{Var} plus \text{sd} (limits-thm). | \mathrm{Var} topic-wide.
- app/content/courses/limits-thm/l1-counting-successes.json, l2-first-success.json | s5, s8 / s7, s9, quiz q-failures | warning | Re-teach random-vars without a link: Var(Bernoulli) = p(1-p) (= random-vars homework-3), np(1-p) via indicators, E = 1/p by conditioning with the same 0.2-a-minute limit order and 5-minute answer (= random-vars l16), failures (1-p)/p (= random-vars homework-4). | One recap screen citing Random Variables; use the time for new material.
- app/content/courses/limits-thm/l1-counting-successes.json | screens[10] explain | warning | "a skill-free week of 15 wins happens about once in 18 weeks" — 0.0553 is for the 55% strategy, so "skill-free" is wrong. | "15 wins happens about once in 18 weeks with no change in skill."
- app/content/courses/limits-thm/l2-first-success.json | screens[2] explain | note | Four sentences. | Trim.
- app/content/courses/limits-thm/l4-without-replacement.json | quiz q-one-ace wrong 'binomial' (0.2765) | error | Bin(5, 1/13) gives P(X = 1) = 0.2792, outside the 0.0005 tolerance: the named mistake gets generic feedback. | 0.2792
- app/content/courses/limits-thm/l4-without-replacement.json | screens[9] hint step | note | Gap "0.0460" vs table 0.0459 (true 0.04595). | 0.0459 in both.
- app/content/courses/limits-thm/l4-without-replacement.json | screens[5] explain | note | Four sentences. | Trim.
- app/content/courses/limits-thm/l6-uniform-exponential.json | screens[0] wrong 'upto5' | note | Duplicates 'half' (both 0.5, same tolerance), so it never fires; byKey 'half' describes 'upto5'. | Drop 'upto5'.
- app/content/courses/limits-thm/l7-bell-curve.json | screens[5] widget.how | note | "math.isclose" without code formatting. | `math.isclose`
- app/content/courses/limits-thm/l8-lognormal.json | screens[8] wrong 'simple' (0.2266) | warning | Value is 1 - Φ((0.2 - 0.05)/0.2): simple return AND no drag; the why names only the first slip, which alone gives 0.1977. | Value 0.1977, or why naming both slips.
- app/content/courses/limits-thm/l9-averages-settle.json | screens[3] explain | error | "Dividing by 10,000 shrinks a gap of 84 to 0.0042": 84/10,000 = 0.0084. The share misses one half by 84/20,000 = 0.0042. | "The share misses a half by only 84/20,000 = 0.0042."
- app/content/courses/limits-thm/l9-averages-settle.json | screens[5] derive | note | σ²/n needs finite variance; the LLN as stated assumes only a finite mean and the screen never says the proof assumes more. | Add "assume a finite variance σ²".
- app/content/courses/limits-thm/l10-bound-that-holds.json | screens[9] hints[1] | note | "percent". | "per cent" or %.
- app/content/courses/limits-thm/l12-skill-or-luck.json | screens[3] prose and explain | warning | "Skill shows once the true mean clears that line": at n = 1,600 the expected t is 2, so a real edge shows t > 2 only about half the time. | "At 1,600 days the expected t is 2; even then the record clears 2 only about half the time."
- app/content/courses/limits-thm/l12-skill-or-luck.json | screens[5], screens[8] | note | SE(SR) ≈ 1/√T omits the factor √(1 + SR²/2) (1.22x at SR = 1). | Add "for small Sharpe ratios".
- app/content/courses/limits-thm/homework-2.json | items[6] h-lognormal-var explain | warning | "A normal on simple returns says £415,200, because it lets prices go below zero": its 1% price is £58.48; the gap is the convexity of exp, not negative prices. | "...says £415,200: a -41.5% simple return is a -0.536 log return, further out than the lognormal's -0.435."
- app/content/courses/limits-thm/homework-3.json | items[7] h-track-record model part 5 | note | "Any of these makes the 0.82 standard error an underestimate": fat tails alone or negative autocorrelation do not. | "Positive autocorrelation and clustering make 0.82 an underestimate."

## markov

- app/content/courses/markov/l2-transition-matrix.json | screens[8] explain | error | "The B route, 0.01575, is half again the A route": the A route is 0.008145, so 1.93x. | "...is nearly twice the A route, 0.008145."
- app/content/courses/markov/l2-transition-matrix.json | screens[2], screens[5] explain | note | Four sentences each. | Trim.
- app/content/courses/markov/l3-never-leave.json | screens[1], [3], [4], [7] explain | note | Four sentences each. | Trim.
- app/content/courses/markov/l4-regimes.json | screens[6], [8], [10] explain | note | Four sentences each. | Trim.
- app/content/courses/markov/l8-which-end.json | screens[5] explain | note | Four sentences. | Trim.
- app/content/courses/markov/l10-gamblers-ruin.json | quiz q-fraction explain | warning | "the Kelly question in the limits course": within topic 1.5 that reads as Distributions and Limit Theorems, which has no Kelly; Kelly is in Limits and Derivatives (l14-best-value). | "...the Kelly question from Limits and Derivatives."
- app/content/courses/markov/l12-price-paths.json | screens[0] byKey 'left' and explain | error | "a 6.5% fall on day 71": Chart A falls 6.29% that day, day 106 falls 6.34% and day 115 5.94%, so "one jump" is not unique either. | "falls of over 6% on days 71 and 106"; explain "...wild spells and jumps".
- app/content/courses/markov/l12-price-paths.json | screens[6] widget.how | note | 35-word sentence. | Split at the semicolon.
- app/content/courses/markov/review-2.json | items[1] r-spread wrong 'col' (1.9667) | warning | why "weighted by the middle row of P" gives 1.9. | Value 1.9.
- app/content/courses/markov/review-2.json | items[6] r-repaid wrong 'default' | note | Same value (0.2) and tolerance as 'year', so it never fires; no byKey. | Drop it.
- app/content/courses/markov/homework-1.json | items[7], items[8] explain | note | Four sentences each. | Trim.
- app/content/courses/markov/homework-2.json | items[7] hw-hth explain | note | "A seeded simulation of 200,000 runs averages 9.999": no seed or code, so not reproducible. | State the seed and generator, or drop the figure.
- app/content/courses/markov/homework-3.json | items[6] widget.how | note | "math.isclose" without code formatting. | `math.isclose`

## exam (app/content/exams/topic-1.5.json)

- app/content/exams/topic-1.5.json | e-normal-tail | warning | Identical to limits-thm/l7 quiz q-two-sd (N(100, 15²), P(X > 130), same distractors): tests recall. | New numbers, e.g. N(80, 12²) and P(X > 98).
- app/content/exams/topic-1.5.json | e-neighbours | warning | Identical to random-vars/review-2 r-heads-pairs (10 flips, doubles, 2.25). | E.g. 12 flips, runs of three heads.
- app/content/exams/topic-1.5.json | e-wait-six | note | Same as random-vars l16 trap and review items; difficulty 2. | Vary (e.g. wait for a 1 or 2).
- app/content/exams/topic-1.5.json | whole exam | warning | All 25 skills are mapped, but rv-variance is tested only for independent variables (no covariance or correlation), dl-continuous only by a uniform length ratio, and Poisson, exponential/memoryless, hypergeometric, lognormal, reflection and absorption probabilities never appear. The ceiling (single-step numeric or choice items) is far below the Stat 110 finals the exit line names. | Add a covariance/portfolio item, a Poisson or exponential item, an absorption-probability item and one multi-part problem at Stat 110 level.

## Automated checks (no finding)

- All 41 Markov-chain graphs topic-wide have outgoing weights summing to 1; every displayed transition matrix is row-stochastic. Row-vector convention used consistently; markov l2 q-columns and l5 s5 flag the eigen course's column convention.
- Seeded figures reproduced: counting-chance l2 (seed 11), conditional l22 (2205), l3 (4226), conditional homework seed 7 and l20 seed 4; random-vars l5 and l9 (seed 9 → 2.9207), l16 (1.99834/6.03976/5.03602); markov l5 (0.666255/0.668935/0.66784), l10 (seeds 11, 6, 28, 8), l12 (seeds 32, 781, 10); counting-chance l7 (seed 2207, 357 missing). All match the prose.
- All 18 longform rubrics sum to 10. No "!" and no "$" currency.

## Coverage against the curriculum (Cover and Exit lines)

- Covered: counting, conditional probability, Bayes, random variables, expectation, linearity, indicators, variance and covariance (discrete), named distributions (Bernoulli, binomial, geometric, Poisson, hypergeometric, uniform, exponential, normal, lognormal), joint and conditional distributions (discrete tables only), conditional expectation (discrete), weak LLN, Markov and Chebyshev, CLT, Markov chains, random walks, gambler's ruin, reflection.
- Missing for a Stat 110 final: moment generating functions; continuous joint densities, marginals by integration and continuous independence; transformations, Jacobians and convolution; order statistics of continuous variables; Beta, Gamma, negative binomial, multinomial, chi-square, t, bivariate normal; law of total variance (Eve's law) and conditional variance; Jensen's inequality (appears only as a distractor id); strong law; Poisson process properties beyond the exponential gap; reversibility, detailed balance and MCMC; story proofs such as Vandermonde.
- So the exit line "two Stat 110 past finals at 70%" cannot be met from this material, and the topic exam does not test it.

## Fix pass

I recomputed every corrected number before writing it (Python with fractions, scipy and exhaustive enumeration; the engine's mulberry32 for the seeded figure). After the edits, `tolcheck.py` finds no overlap between an answer and a misconception, or between two misconceptions, in any topic 1.5 file. `sentcount.py` finds no explanation over three sentences, and `style.py` raises no new long-sentence or American-spelling flag. `node tools/validate.mjs`: 0 errors. Every touched file passes the playthrough.

Status: fixed 99, disputed 0, deferred 1. Where a fix differs from the proposal, the line says why.

### counting-chance (19 fixed)

1. l1 s6 trap: fixed. The explain now says the 21 outcomes are not equally likely. Using P(·) before l2 stays: the trap needs the intuitive chance.
2. l1 summary.trap: fixed, split into two sentences.
3. l2 s0: fixed, "In the long run 7 comes up six times as often as 2 or 12."
4. l2 s4: fixed, "this coin's two faces do not have them".
5. l2 summary.trap: fixed, rewritten as two short sentences.
6. l6 s6 trap: fixed. Kim writes 336 for both. The option `kim` is now 336/336, the old `both-ordered` option became `swapped` (336/56), and the byKey lines and explain were updated to match.
7. l9 s0-s4: fixed with a link sentence ("This builds on Events as sets...") and with union and intersection no longer bolded as new terms. The screens stay: cutting all five would leave 5 screens, under the minimum of 8.
8. l10 s9 table: fixed, 0.1159 → 0.1155 (1 − ∏(10000 − i)/10000 over i < 50 = 0.11547).
9. l10 q-seven-rolls `ratio`: fixed. The value is now 1/6, the chance one pair matches, which fits the why.
10. l10 s4 prose: fixed with different wording. The proposed "A room holds 23 people" would make the "shares yours" chance 1 − (364/365)^22 = 0.0586, not the 0.0612 the screen grades. The prose keeps "23 other people" and asks about "any two of those 23".
11. l10 s6 how: fixed, `math.isclose` is now in code formatting.
12. l11 s2: fixed. Axiom 3 is now countable additivity, with "We mostly use axiom 3 for two events". One sentence says the dart example needs the infinite form: all the fractions in [0, 1] together have chance 0 + 0 + ... = 0.
13. l11 s4 `pos`: fixed, in both the option why and the byKey line.
14. l12 s2 `ordered`: fixed, value 2,496 → 14,976 (624 × 4!). The why now says 24 ways.
15. homework-2 h-at-least-one-formula: fixed, "For n = 1, 2 or 3 it gives 0".
16. review-3 r-months: fixed, wording as proposed.
17. review-3 items[6]: fixed, three sentences. Checked: 13 · 6 · 220 · 64 = 1,098,240.
18. homework-3 items[0]: fixed, three sentences. Checked: 675 − 141 + 9 = 543.
19. l5 s7, l6 s7, l12 s8: fixed, with a sentence break before each display.

### conditional (33 fixed)

20. l2 whole lesson: fixed with a link sentence to With and without replacement. Screen 7 now bridges to Counting and Chance (the 2/4 in 3/5 × 2/4 was already a conditional probability) and names the "multiplication rule for probabilities". The summary formula is renamed to match. The lesson is kept, since every screen is a repeat.
21. l7 q-equal-sizes and summary.ideas[2]: fixed. They now say that when P(A ∩ B) > 0 the two directions agree exactly when P(A) = P(B), and that when it is 0 both are 0.
22. l7 s8 derive: fixed. d1 and d2 are a `same` group and the ambiguous instruction is gone.
23. l7 s9: fixed, "An 80% detection rate, firing on 80% of up days, does not make it right 80% of the time."
24. l8 s4: fixed, `fp-rate` tolerance 0.0005 → 0.0002.
25. l10 s6 trap: fixed, with the prior now 10% and LR 3. Graded answer 0.6667 → 0.25. Wrong `probs` 1.2 → 0.3 and `prior` 0.4 → 0.1; `lr-post` stays at 0.75. The number line, hints, feedback and explain were updated.
26. l11 s4: fixed. The line now starts at −7, with a 1:999 label at −6.9068.
27. l12 s6: fixed, wording as proposed.
28. Event names: fixed. Straight single quotes became curly double quotes in l13, l14, l15, l16, homework-3 and review-3 (and in limits-thm l6 and l8). Derive captions were left alone, because there the quotes are code.
29. l14 s5: fixed, "...build it properly in Distributions and Limit Theorems".
30. l17 s5: fixed. Answer tolerance 0.0005 → 0.0001 (the true value is 0.064616) and `recw` tolerance 0.00015 → 0.00005.
31. l18 s7: fixed, three sentences, with the likelihoods written in symbols.
32. l19 s7: fixed, three sentences.
33. l20 q-coins-space: fixed. The question now asks for outcomes "each one a single result of the two tosses", and the `same-diff` why says what the option lumps together.
34. l20 s7: fixed, three sentences.
35. l21 s7 and s9: fixed, three sentences each.
36. l23 s7: fixed, "all but certain" (1 − 0.99^1000 = 0.99996).
37. l23 q-pool `half`: fixed, one slip named.
38. l25 s8 `all`: fixed. Value 0.0767 → 0.0833 ((720 − 120 + 400)/120), tolerance 0.0005.
39. l25 s9 `sign`: fixed, value 0.0625 → 0.0425 ((40 + 45)/20).
40. l25 s9: fixed, "per cent".
41. l26 hit rate: fixed. P(flash | up) is now the "detection rate" throughout l26, l7, l8, l9, l10, l11, review-2, review-5 and homework-2. l26 s0 now says once that desks call P(up | flash), the share of flashes that were right, the hit rate. l14 keeps "hit rate" for the share of trades won, which is the desk meaning.
42. l26 s8 explain: fixed. The posterior is the win chance: "If the true chance out of sample is only 0.55, Kelly is 0.1."
43. l26 s8 Kelly premise: fixed. The prose now gives repeated bets, known p and odds, and fastest growth of log wealth. The summary note says "repeated even-money bet with known p".
44. l26 s0: fixed. Dropped the dead `flash` (0.5, a duplicate of `prior`).
45. homework-1 h-three-hearts: fixed, "Item 8".
46. homework-2 items[1]: fixed, `probs` and `half` tolerances 0.5 → 0.2.
47. homework-2 items[2]: fixed, three sentences.
48. homework-4 items[2]: fixed, three sentences.
49. review-2 items[1]: fixed, `base` tolerance 0.00005 and `joint` 0.00004.
50. review-4 items[7]: fixed, three sentences.
51. homework-5 and l20 how: fixed, `math.isclose` in code formatting.
52. l2 s7, l4 s7, l23 quiz[0], l25 s6: fixed, split.

### random-vars (14 fixed)

53. l5 s6: fixed, three sentences.
54. l6 s9 `one-up`: fixed. The value is now what the named slip gives, £40 → £64 (1 − 0.6² = 0.64), and the why shows it.
55. l7 s7: fixed, "Y scaled by −1".
56. l11 s2 `count`: fixed. Value 2 → 0 (1 + 1 − 1 − 1), and the why shows the sum.
57. l13 s8: fixed, wording as proposed.
58. l14 s6 `var`: fixed with a different value from the one proposed. 0.6667 would duplicate `ey` and never fire, so the value is Var(Y) = 2/9 = 0.2222, with a byKey line naming it.
59. l16 s4 `third`: fixed, value 1.3333 → 1 (E = 1/4 + 3/4 E gives 1).
60. l16 s9 `half`: fixed, dropped along with its byKey line.
61. review-2 r-call-tree: fixed, "You gave the path up-up a chance of 0.5."
62. homework-1 items[6]: fixed, three sentences.
63. homework-2 h-overround: fixed. It now gives an overround of 5.56% and says a balanced book keeps 1/19 = 5.26% of stakes, in three sentences.
64. homework-3 h3-traders: fixed, "well below the £7,000 you get by adding the sds".
65. homework-4 h-ht `three`: fixed, the why now names the slip.
66. homework-4 items[7]: fixed, split into three sentences.

### limits-thm (17 fixed)

67. Var/Cov notation: fixed topic-wide as `\operatorname{Var}`, `\operatorname{Cov}` and `\operatorname{sd}`, in place of the proposed `\mathrm` (the fix brief asked for `\operatorname`). That is 176 strings across random-vars, limits-thm, markov and the exam. Plain-text widget labels ("Var(X)") stay, because they cannot hold KaTeX. The objective in random-vars `course.json` is left: course files are out of scope for this pass.
68. l1 and l2 re-teaching: fixed. l1 s0 now links to Random Variables. l1 s5 (Bernoulli variance) is cut, and s8 is now the recap: it cites Random Variables and names the Bernoulli variable. l1 now has 11 screens. l2 s0 now links to Averaging the averages. l2 keeps s7, because the objective names the derivation "by conditioning". s9 (backtests until a pass) is not a repeat, and q-failures is a quiz item, not a screen.
69. l1 s10: fixed, "with no change in skill" (1/0.05533 = 18.1).
70. l2 s2: fixed, three sentences.
71. l4 q-one-ace `binomial`: fixed, value 0.2765 → 0.2792 (Bin(5, 1/13) at 1).
72. l4 s9 hint: fixed, 0.0459 (0.32768 − 4368/15504 = 0.045946).
73. l4 s5: fixed, three sentences.
74. l6 s0: fixed, dropped `upto5`. byKey `half` describes this slip, which gives 0.5.
75. l7 s5 how: fixed, `math.isclose` in code formatting.
76. l8 s8 `simple`: fixed, value 0.2266 → 0.1977 (1 − Φ(0.85)).
77. l9 s3: fixed, "The share misses a half by only 84/20,000 = 0.0042."
78. l9 s5: fixed, "Assume each draw has a finite variance σ²."
79. l10 s9 hint: fixed, "per cent".
80. l12 s3: fixed. The prose says a typical record only just reaches t = 2 where the line meets the true mean. The explain says even then the expected t is only 2, so a real edge clears 2 about half the time.
81. l12 s5 and s8: fixed, "for small Sharpe ratios" and "using the small-Sharpe approximation".
82. homework-2 h-lognormal-var: fixed. The −41.5% simple return is a −0.536 log return, further out than the lognormal's −0.435. The negative-price claim is removed.
83. homework-3 h-track-record part 5: fixed with a narrower claim than the one proposed. Positive serial correlation makes 0.82 an underestimate; fat tails and clustering make the normal approximation less reliable.

### markov (13 fixed)

84. l2 s8: fixed, "nearly twice the A route, 0.008145" (ratio 1.93).
85. l2 s2 and s5: fixed, three sentences each.
86. l3 s1, s3, s4 and s7: fixed, three sentences each.
87. l4 s6, s8 and s10: fixed, three sentences each.
88. l8 s5: fixed, three sentences.
89. l10 q-fraction: fixed, "the Kelly question from Limits and Derivatives" (limits/l14-best-value).
90. l12 s0: fixed. byKey `left` now reads "falls of over 6% on days 71 and 106" (checked: −6.29% and −6.34%), and the explain says "wild spells and jumps".
91. l12 s6 how: fixed, split into three sentences.
92. review-2 r-spread `col`: fixed, value 1.9667 → 1.9 (the middle row (0.3, 0.5, 0.2) · (1, 2, 3)). The byKey line gives 1.9.
93. review-2 r-repaid `default`: fixed, dropped (it duplicated `year`).
94. homework-1 items[7] and [8]: fixed, three sentences each.
95. homework-2 hw-hth: fixed. The figure is now stated as "With the engine's mulberry32 generator and seed 7, 200,000 simulated runs average 9.995". Reproduced with `ZQ.sim.rng(7)` and `ZQ.sim.coin`: 9.994755.
96. homework-3 how: fixed, `math.isclose` in code formatting.

### exam (3 fixed, 1 deferred)

97. e-normal-tail: fixed with new numbers, N(80, 12²) and P(X > 98). z = 1.5, so the answer is about 0.067 (1 − Φ(1.5) = 0.0668). The distractors are 0.134 (both tails), 0.16 (one sd) and 0.433 (mean to z). The canvas was rescaled.
98. e-neighbours: fixed with new numbers, 12 flips and runs of three heads. The answer is 10/8 = 1.25, checked by enumerating all 2^12 sequences. Wrong values: 1.5 (12 runs), 0.5 (4 disjoint blocks) and 6 (heads).
99. e-wait-six: fixed. The proposed "1 or 2" is already random-vars l16's item, so the wait is now for a heart, drawn with replacement. The answer is 4, and the distractors are 3, 13 and 1/4. The id is unchanged.
100. Whole exam: deferred. The coverage and ceiling are recorded as `docs/ENGINE-BACKLOG.md` item 423 for a later pass.

Left for later, outside this pass's scope: conditional `course.json` still describes l26 as "a signal with a known hit rate", and random-vars `course.json` keeps `$Var(aX + b)$` in the l10 objective. Course files were out of scope for this pass.
