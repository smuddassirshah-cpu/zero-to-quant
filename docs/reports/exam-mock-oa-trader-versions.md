# Fresh versions of mock-oa-trader (versions 2 and 3)

Brief: `docs/briefs/mock-versions.md` (PLAN 2d; critical review 3.1). Base `app/content/exams/mock-oa-trader.json` (version 1) is unchanged.

## What step 1 found

The suspicion was right. At d77755ef every one of the 40 items in `mock-oa-trader-2` and every one of the 40 in `mock-oa-trader-3` shared a template. In each version, 39 shared one with version 1 at the same position: the same rule family or setup with new parameters, as `docs/briefs/mocks.md` had specified ("one template per position, parameters drawn"). The 40th, position C10 (the central binomial term: exactly half heads in 20 or 30 tosses), was shared between versions 2 and 3. **Shared-template count: 80 of 80 items** (40 per version). The before table below shows it line by line.

## What changed

All 80 items were re-authored: 40 in version 2 and 40 in version 3, each with a new item id and a new family tag. None survived, so no surviving id changed. Kept from version 1: `id`, `versionOf`, `name`, `style`, `models`, `description`, `requires`, `skills`, the four part headers (minutes, scoring, `passNet`, navigation, `skip`), 15 + 15 + 10 items, and per position the difficulty, the skill and the widget kind (the script asserts all of these). Answer types stay the four-option `choice` and three-line `order` that the brief says the real battery uses.

Topic weights per version:
- 15 number sequences on 15 rule families, none used in version 1 or the other version.
- 15 probability-at-speed items: 10 `mp-fractions`, and 5 `pz-conditioning` at positions 4, 11, 13, 14 and 15, as in version 1.
- 6 rankings, each with a "more trials" or windows-times-chance trap (version 2: best-of-n matches and majority votes; version 3: runs of heads).
- 4 intervals, each with one narrow interval holding the value, one wider one and two misses, one either side.

Judgement calls a second reader should look at:

- Sequence families that share a tool but not a method sit in the same version. The digit-property filters (digits 1 and 2 only, digit sum 5) and the gap rules (gaps are squares, gaps are primes) are both in version 3. Powers of two with the place ($2^n + n$, $n \cdot 2^n$) and the two digit reversals are both in version 2. Primes appear in five families across the two versions, each with a different operation: squares of primes, products of two different primes, products of neighbouring primes, primes ending in 3, and gaps that are primes.
- Version 2 `a11-product-of-two` multiplies the two terms before, where version 1's Fibonacci adds them. That changes the operation, not the numbers, so I count it as a new template.
- Each version's six rankings lean on one trap family (series in version 2, runs in version 3). The paper rule asks every ranking to tempt the $n \times p$ or more-trials error, and the at-least-one and binomial-tail events that version 1 uses for it were off limits.
- The script found one ambiguity while I worked: version 2's $3, 6, 11, 20, 37$ also fits the tribonacci rule (version 1 A15), with next term 68. It now shows $3, 6, 11, 20, 37, 70$, where tribonacci fails.

## Freshness (AUTHORING "Exam freshness")

`node tools/fresh-check.mjs --exam mock-oa-trader-2` and `--exam mock-oa-trader-3`: **0 hits each** at the default gate.

Triage at `--min-run 8 --min-share 0` on the first draft, and what I did:

- `counting-chance/l9-double-counting` quiz 1 (1 to 100, divisible by 2 or by 5). Same setup as my drafts of v2 B3 (squares or cubes in 1 to 100), v2 B5 (coprime to 30), v3 B3 (a 7 among the digits of 10 to 99) and a v2 ranking event (a multiple of 3 or 7): all inclusion-exclusion on a range. **Rewritten**: v2 B3 is now the four-equal-digit clock, v2 B5 the pairs where one divides the other, v3 B3 a triangular number in 1 to 20, and the ranking event two uniforms both above 0.3.
- `puzzles/homework-2` item 6 and `puzzles/l24-mixed-set` screen 2 (a bag with a fair and a two-headed coin, flipped twice). My draft v2 B14 asked the forward chance of two heads from that same bag. **Rewritten** as a pick inside a pick ($X$ from 1 to 3, then a number from 1 to $X$).
- Grep checks beyond the tool, also acted on before the first draft was written: Pólya urns (`puzzles/l8-urns`), two-state Markov chains (`markov/l5`), fixed points and coupons (`mock-superday-trader`; bank `hats`, `every-coupon`), the meeting and broken-stick problems (bank), the fair-from-biased trick (bank), the reflection principle (`markov/l11`), $\log_2$ of a power of ten (`exp-log/l7`), $1^2 + \dots + 20^2$ (brainteasers bank), $2^{100}$ against $10^{30}$ (`brainteasers/review-3`) and a portfolio return (`vectors/l4`). None is in the final files.

Hits left after the rewrite are all stock phrasing on a different setup and method, so they stay:

- "a whole number from # to # is picked at random" (`counting-chance/l9` quiz 1) on v2 B4 (told it is odd, chance prime), v2 B9 (digits add to 3), v3 B1 (a square factor of 36) and v3 B3 (a triangular number).
- "random order, what is the chance that the two" (`stage-3` paper 0 item 3, two desk heads side by side at a round table) on v2 B8 (two reds at both ends of a row).
- "what is the chance of exactly one head" (`counting-chance/l2` quiz 1, `bank/sample-draw` item 2) on v2 B11 (a die sets the number of tosses).
- "a fair coin is tossed # times, what is the chance" (`conditional/l14` quiz 0, four heads in 4 tosses) on v3 B7 (no two heads in a row) and v3 B12 (an even number of heads from a biased coin).

Sequence items carry no words for the tool to compare. I checked them by hand against every sequence in the `mental-pressure` lessons, homework and reviews: none repeats a rule there. The lessons teach reversal only as "reverse, then add 2", which differs from both reversal rules here.

Closure (`node tools/closure.mjs --target mock-oa-trader`): 22 courses. Every item needs only counting, conditioning, expectation, uniform areas, one quadratic (v2 B15) and number facts, from `number-sense`, `counting`, `conditional`, `random-vars`, `puzzles`, `quadratics` and `series`.

## Checks

- Validator (`node tools/validate.mjs` from `app/`): 0 errors. Three warnings remain on these files, each one sentence of 20 to 27 words (`O2-long-sentence`), under the 35-word gate.
- Voice: `voice-scan.py 35 --summary` with `VOICE_BASE` set to a scratch folder holding the two files: 0 sentences over 35 words, 0 explanations over three sentences. No exclamation marks or em-dashes; £ for money.
- Numbers: `docs/reports/exam-mock-oa-trader-versions-numbers.py`, run with the scratchpad venv, exits 0. It recomputes all 80 keys exactly and by a second method: enumeration, an independent formula, or a seeded simulation (400,000 runs within 0.005 for the uniform events and v2 B14; 600,000 within 0.02 for v3 B15). It also checks:
  - every distractor differs from the key;
  - ranking order, gaps of at least 0.02, and the values printed in feedback;
  - the interval option rule;
  - that shown sequence terms follow the stated rule, and that no version 1 rule family fitting them predicts another next term;
  - that no family tag, question or ranking event repeats across the three versions.
- Playthrough: `node tools/playthrough.mjs --exam mock-oa-trader-2 --local-cdn <pkgs>`, then `-3`, each with and without `--mobile`: all passed (0 relaunches). The screenshots at 1280 px and 440 px show no layout fault.

## Template tables

Setup is the opening of the question, or the events for a ranking; method is the step that solves it.

### Before: versions 1, 2 and 3 as they stood at d77755ef

| Pos | Topic | v1 setup | v1 method | v2 setup | v2 method | v3 setup | v3 method |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A1 | sequence | 7, 11, 15, 19, 23, ? | constant gap, add it again | 13, 19, 25, 31, 37, ? | constant gap, add it again | 52, 45, 38, 31, 24, ? | constant gap, add it again |
| A2 | sequence | 2, 6, 18, 54, 162, ? | constant ratio, multiply again | 7, 14, 28, 56, 112, 224 ... | constant ratio, multiply again | 4, 12, 36, 108, 324, ? | constant ratio, multiply again |
| A3 | sequence | 5, 10, 17, 26, 37, ? | compare with squares, keep offset | 6, 13, 22, 33, 46, ? | compare with squares, keep offset | 19, 28, 39, 52, 67, ? | compare with squares, keep offset |
| A4 | sequence | 3, 5, 9, 17, 33, ? | double each term, adjust constant | 1, 5, 13, 29, 61, ? | double each term, adjust constant | 5, 7, 11, 19, 35, ? | double each term, adjust constant |
| A5 | sequence | 2, 5, 11, 20, 32, ? | gaps grow steadily, extend gaps | 10, 14, 19, 25, 32, 40 ... | gaps grow steadily, extend gaps | 3, 8, 17, 30, 47, ? | gaps grow steadily, extend gaps |
| A6 | sequence | 4, 8, 5, 10, 7, 14 ... | two operations alternate in turn | 3, 9, 5, 15, 11, 33 ... | two operations alternate in turn | 6, 12, 7, 14, 9, 18 ... | two operations alternate in turn |
| A7 | sequence | 3, 4, 7, 11, 18, 29 ... | add the two before | 1, 5, 6, 11, 17, 28 ... | add the two before | 2, 7, 9, 16, 25, 41 ... | add the two before |
| A8 | sequence | 1, 20, 4, 18, 7, 16 ... | split places, two arithmetic strands | 2, 30, 7, 32, 12, 34 ... | split places, two arithmetic strands | 40, 3, 36, 6, 32, 9 ... | split places, two arithmetic strands |
| A9 | sequence | 19, 29, 40, 44, 52, 59 ... | add the digit sum each step | 23, 28, 38, 49, 62, 70 ... | add the digit sum each step | 26, 34, 41, 46, 56, 67 ... | add the digit sum each step |
| A10 | sequence | 3, 5, 8, 11, 16, 19 ... | compare with primes, keep offset | 23, 29, 31, 37, 41, 43 ... | compare with primes, keep offset | 53, 59, 61, 67, 71, 73 ... | compare with primes, keep offset |
| A11 | sequence | 6, 25, 62, 123, 214, ? | compare with cubes, keep offset | 4, 11, 30, 67, 128, ? | compare with cubes, keep offset | 29, 66, 127, 218, 345, ? | compare with cubes, keep offset |
| A12 | sequence | 1, 10, 3, 20, 9, 40 ... | split places, two geometric strands | 5, 1, 10, 3, 20, 9 ... | split places, two geometric strands | 3, 1, 6, 4, 12, 16 ... | split places, two geometric strands |
| A13 | sequence | 6, 12, 20, 30, 42, ? | factor as n(n + 1) | 72, 90, 110, 132, 156, ? | factor as n(n + 1) | 240, 272, 306, 342, 380, ? | factor as n(n + 1) |
| A14 | sequence | 1, 2, 5, 16, 65, ? | multiply by rising n, add | 2, 3, 7, 22, 89, ? | multiply by rising n, add | 1, 3, 10, 41, 206, ? | multiply by rising n, add |
| A15 | sequence | 1, 2, 3, 6, 11, 20 ... | add the three before | 2, 3, 4, 9, 16, 29 ... | add the three before | 3, 1, 5, 9, 15, 29 ... | add the three before |
| B1 | probability | Two fair dice are rolled. What ... | count ordered pairs over 36 | Two fair dice are rolled. What ... | count ordered pairs over 36 | Two fair dice are rolled. What ... | count ordered pairs over 36 |
| B2 | probability | A fair coin is tossed 5 ... | choose positions over 2^n | A fair coin is tossed 6 ... | choose positions over 2^n | A fair coin is tossed 5 ... | choose positions over 2^n |
| B3 | probability | A fair die is rolled three ... | one minus chance of none | A fair die is rolled twice ... | one minus chance of none | A card is drawn from a ... | one minus chance of none |
| B4 | probability | Two cards are dealt from a ... | remove first card, recount | Two cards are dealt from a ... | remove first card, recount | Two cards are dealt from a ... | remove first card, recount |
| B5 | probability | Three cards are dealt from a ... | multiply without-replacement chances | A deck has 20 cards: 5 ... | multiply without-replacement chances | The hearts are taken out of ... | multiply without-replacement chances |
| B6 | probability | You roll a fair die. You ... | keep faces beating fresh mean | You roll a fair die. You ... | keep faces beating fresh mean | You roll a fair die and ... | keep faces beating fresh mean |
| B7 | probability | Three people are each born on ... | falling product over n^k | Four fair dice are rolled. What ... | falling product over n^k | Four people each have a birth ... | falling product over n^k |
| B8 | probability | A fair die is rolled until ... | misses then one hit | A signal is right on a ... | misses then one hit | Cards are drawn with replacement until ... | misses then one hit |
| B9 | probability | A desk of 5 traders and ... | hypergeometric: choose over choose | A desk of 6 traders and ... | hypergeometric: choose over choose | A fund picks 2 of 8 ... | hypergeometric: choose over choose |
| B10 | probability | An urn holds 3 red and ... | draw without replacement, multiply | An urn holds 4 red and ... | draw without replacement, multiply | An urn holds 4 red and ... | draw without replacement, multiply |
| B11 | probability | 5% of traders have an edge ... | Bayes by counting a population | 20% of stocks beat the market ... | Bayes by counting a population | 2% of orders are spoofs. A ... | Bayes by counting a population |
| B12 | probability | Two fair dice are rolled. What ... | P(max <= k) minus P(max <= k-1) | Three fair dice are rolled. What ... | P(max <= k) minus P(max <= k-1) | Two fair dice are rolled. What ... | P(max <= k) minus P(max <= k-1) |
| B13 | probability | Two fair dice are rolled and ... | restrict to total, count | Two fair dice are rolled and ... | restrict to total, count | Two fair dice are rolled and ... | restrict to total, count |
| B14 | probability | You and a friend take turns ... | geometric series over turns | You and a friend take turns ... | geometric series over turns | Three players take turns to roll ... | geometric series over turns |
| B15 | probability | A fair coin is tossed until ... | states of the last tosses | A fair coin is tossed until ... | states of the last tosses | A fair coin is tossed until ... | states of the last tosses |
| C1 | ranking | six in 4; double six; heads tail | complements and a binomial tail | six in 2; die 5-6; AKQ | complement and single counts | six in 5; die 3+; total 8+ | complement and single counts |
| C2 | ranking | 2 heads of 4; suit; total 7 | count each as a fraction | 1 head of 3; ace; double | binomial and complement counts | 3 heads of 4; picture; heart | binomial and complement counts |
| C3 | ranking | six in 3; totals 6-8; colours | complement, pair count, card count | ace in 6; totals 5-7; red | complement, pair count, card count | ace in 4; same three; 5 or 10 | complement, binomial, pair count |
| C4 | ranking | exactly half heads, 2/6/10 tosses | binomial centre falls with n | 4 of 5, 8 of 10; 11-12 | binomial tails and a pair count | one six in 6, two in 12 | binomial exact counts compared |
| C5 | ranking | birthday 23; three dice; ace | falling products as complements | birthday 30; six in 8; ace | falling products as complements | birthday 25; double six; ace | falling products as complements |
| C6 | ranking | one six in 6, two in 12... | Newton-Pepys: tails fall with n | 1 head of 2, 2 of 4... | Newton-Pepys: tails fall with n | 5-or-6 once in 3, twice in 6 | Newton-Pepys: tails fall with n |
| C7 | interval | square root of 300 | bracket between neighbouring squares | square root of 500 | bracket between neighbouring squares | square root of 700 | bracket between neighbouring squares |
| C8 | interval | 1.05 to the 14th | rule of 72, then adjust | 1.07 to the 12th | rule of 72, then adjust | 1.05 to the 20th | rule of 72, then adjust |
| C9 | interval | (5/6)^12, no six | power of a chance, logs | 0.99^100, never happens | power of a chance, logs | 0.75^10, ten losses | power of a chance, logs |
| C10 | interval | 1.02 to the 100th | compound growth via e^2 | C(20,10) / 2^20 | binomial centre, sqrt approximation | C(30,15) / 2^30 | binomial centre, sqrt approximation |

### After: versions 2 and 3 as rewritten (version 1 unchanged, above)

| Pos | Topic | v2 setup | v2 method | v3 setup | v3 method |
| --- | --- | --- | --- | --- | --- |
| A1 | sequence | 1, 2, 2, 3, 3, 3 ... | spot n repeated n times | 0.1, 0.12, 0.123, 0.1234, 0.12345, ? | append the next digit |
| A2 | sequence | 1, 2, 1, 3, 2, 1 ... | spot blocks counting down to 1 | $13,25,37,49,{5}{11}$, ? | top and bottom as two sequences |
| A3 | sequence | 3, 5, 6, 9, 10, 12 ... | filter by divisibility by 3, 5 | 11, 12, 21, 22, 111, 112 ... | filter numbers using digits 1, 2 |
| A4 | sequence | 4, 9, 25, 49, 121, ? | square roots are the primes | 2, 3, 7, 16, 32, ? | gaps are the squares |
| A5 | sequence | 3, 6, 11, 20, 37, 70 ... | subtract powers of two, see n | 1, 3, 6, 11, 18, 29 ... | gaps are the primes |
| A6 | sequence | 7, 22, 11, 34, 17, 52 ... | halve evens, treble odds plus one | 1, 4, 9, 6, 5, 6 ... | last digit of each square |
| A7 | sequence | 420, 210, 140, 105, 84, 70 ... | multiply term by place: constant | 37, 74, 48, 96, 92, 84 ... | double, keep last two digits |
| A8 | sequence | 1, 2, 3, 4, 6, 8 ... | filter numbers built from 2, 3 | 2, 3, 5, 6, 7, 8 ... | every number except the squares |
| A9 | sequence | 2, 8, 24, 64, 160, ? | divide out powers of two | 1, 9, 36, 100, 225, ? | roots are triangular numbers |
| A10 | sequence | 1, 4, 9, 61, 52, 63 ... | read digits backwards, see squares | 41, 50, 104, 113, 122, 131 ... | filter numbers with digit sum 5 |
| A11 | sequence | 1, 2, 2, 4, 8, 32 ... | multiply the two before | 3, 13, 23, 43, 53, 73 ... | filter primes ending in 3 |
| A12 | sequence | 1, 7, 21, 35, 35, 21 ... | recognise a binomial row | 1, 2, 2, 3, 2, 4 ... | count the factors of n |
| A13 | sequence | 6, 10, 14, 15, 21, 22 ... | factorise: two different primes | 1, 2, 1, 4, 1, 2 ... | largest power of 2 dividing n |
| A14 | sequence | 13, 44, 88, 176, 847, ? | add the digits reversed | 4, 16, 37, 58, 89, 145 ... | sum squares of digits each step |
| A15 | sequence | 6, 15, 35, 77, 143, ? | factorise: neighbouring primes multiplied | 1, 4, 27, 256, 3125, ? | each place to its own power |
| B1 | probability | A die is loaded so that ... | normalise weights to total | A factor of 36 is picked ... | list factors, count squares |
| B2 | probability | Two trades are independent. One wins ... | add the two lone-win cases | Two traders each pick 2 of ... | fix first pick, match it |
| B3 | probability | A digital clock shows hours and ... | list valid times, over 1,440 | A whole number from 1 to ... | list triangular numbers up to 20 |
| B4 | probability | A whole number from 1 to ... | restrict to odd, count primes | A fair die is rolled. You ... | average the faces left |
| B5 | probability | Two whole numbers from 1 to ... | sum floor(10/d) over 100 | Two different squares of an 8 ... | fix a square, count partners |
| B6 | probability | Three people play rock, paper, scissors ... | all same plus all different | Two different edges of a cube ... | fix an edge, count parallels |
| B7 | probability | A 4-digit PIN is picked at ... | a set gives one rising order | A fair coin is tossed 5 ... | Fibonacci count of good rows |
| B8 | probability | Two red and three blue counters ... | choose places for the reds | Three of the six corners of ... | evenly spaced corner sets |
| B9 | probability | A whole number from 100 to ... | list by first digit | Three of the nine squares of ... | count lines over choose 3 |
| B10 | probability | Six people are split at random ... | partner of a fixed person | The numbers 1, 2, 3 and ... | ends forced, list two orders |
| B11 | probability | Roll a fair die, then toss ... | condition on the die, average | A fair coin is tossed 5 ... | given 2 heads, count places |
| B12 | probability | You and a friend each toss ... | tie first, then symmetry | A coin lands heads with chance ... | add 0 and 2 heads |
| B13 | probability | Three people each draw a different ... | list orders consistent with news | Three fair coins are tossed. You ... | E[H] over P(H at least 1) |
| B14 | probability | A number $X$ is picked at ... | condition on first pick, average | Ten cards are numbered 1 to ... | smaller is uniform below 8 |
| B15 | probability | A cell splits into two with ... | first-step equation, smaller root | A fair die is rolled until ... | stop at 1, 3, 5, 6 |
| C1 | ranking | best of 3 at 0.7; two uniforms | series sum; area of a square | HH in 3; factor of 12; edge | run count; factor list; border |
| C2 | ranking | best of 3 at 0.3; uniform square | series sum; invert a square | HHH in 5; grid neighbours; 11s | run count; pair count; list |
| C3 | ranking | best of 5 at 0.4; disc | series sum; area ratio | octagon right angle; HHH in 10 | diameter count; run recurrence |
| C4 | ranking | best of 3 and 5 at 0.6 | series sums; interval length | digit 1; differ by 1; HH in 6 | list; pair count; run recurrence |
| C5 | ranking | majority of 3 or 5 judges | majority sums against one judge | HHHH in 12; HHH in 7; odd factor | run recurrences against a list |
| C6 | ranking | best of 1, 3, 7 at 0.55 | series sums shrink towards a half | HH in 4, HHH in 8, HHHH in 16 | runs: windows times chance misleads |
| C7 | interval | seconds in a week | multiply the units out | £1,000 shared by 7 | bracket by multiples of 7 |
| C8 | interval | 1.5 x 2.5 x 3.5 x 4.5 | pair the ends, multiply | 10! in millions | 720 times 5,040 |
| C9 | interval | 1/0.97 + 1/1.03 | common denominator, 1/(1 - x^2) | 1 + 1/2 + ... + 1/10 | add reciprocals as decimals |
| C10 | interval | games in an even best of 7 | expected length from four cases | 25th Fibonacci number | ratio 1.618 from the 20th |
