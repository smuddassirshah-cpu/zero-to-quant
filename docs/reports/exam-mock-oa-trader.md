# Report: mock exam `mock-oa-trader` (three versions)

Brief: `docs/briefs/mocks.md`, preamble and `## mock-oa-trader`. Generator and helpers in `/tmp/claude-0/-home-user-zero-to-quant/99d9b168-d1f8-545f-868f-7528f8ba6677/scratchpad/mock-oa-trader/` (the orchestrator named this folder in place of the brief's `exam-<id>/`).

## Files

- `app/content/exams/mock-oa-trader.json` (version 1, seed 2501), `mock-oa-trader-2.json` (seed 2502), `mock-oa-trader-3.json` (seed 2503), all written by `gen_trader.py`.
- Names: `Trader test battery`, `Trader test battery, version 2`, `Trader test battery, version 3`. `style: trader`, `skills` as the brief.
- Parts, identical in all three: paper `sequences` "Number sequences" (25 min, 15 items, scoring 1/0/0, `passNet: 10`, `navigation: "forward"`, `skip: false`); paper `probability` "Probability at speed" (30 min, 15 items, 1/0/0, `passNet: 10`, free); paper `ranking` "Likelihood ranking and intervals" (10 min, 10 items, 1/0/0, `passNet: 6`, free); check `no-calculator` "I used no calculator". 65 minutes, 40 questions.
- `content/prep.json` already lists `mock-oa-trader` (paths `oa-trader` and the firm paths); not edited. Versions 2 and 3 are not in it.
- No `trade` game is used, so no game seed applies.

## Item counts (each version)

| Paper | Items | Difficulty 2 / 3 / 4 / 5 | Widget | Pace | Families (first tag) |
| --- | --- | --- | --- | --- | --- |
| A sequences | 15 | 3 / 5 / 5 / 2 | choice, shuffle | 100 s | `sequence` then the 15 rule families of the brief table, in order |
| B probability | 15 | 4 / 6 / 4 / 1 | choice, shuffle | 120 s | the 15 families of the brief, in order |
| C ranking | 10 | 3 / 3 / 2 / 2 | 6 `order`, 4 choice (no shuffle) | 60 s | `likelihood-ranking` (Q1 to Q6), `interval` (Q7 to Q10) |

Totals per version: 10 at 2, 14 at 3, 11 at 4, 5 at 5. Skills: `mp-formats` 15, `mp-fractions` 10, `pz-conditioning` 5, `mp-estimate` 10. The validator raised no ramp warning. No item repeats across versions (`gen_trader.py` asserts that question and option set differ).

## Validator, voice and playthrough

- `node tools/validate.mjs 2>&1 | tail -5`: 0 errors, no warning on the three files.
- `VOICE_BASE=/home/user/zero-to-quant/app/content/exams/ python3 docs/reviews/voice-scan.py`: 0 sentences over 20 words and 0 explanations over three sentences in the three files. No `!`, no em-dash.
- `node tools/playthrough.mjs --exam <id> --local-cdn <pkgs>` and with `--mobile`, for each of the three ids: `ok 40 items, scored 40 of 40, passed`; `ok (mock checks) seed, clock at zero, attempts kept`; All passed (six runs). The forward probe (no jump, no back, no step without an answer on paper A) raised nothing.
- Screenshots: playthrough `--mobile --why --shots` for all three, plus `examshot.mjs` (scratch folder), which names shots by paper: start card, paper A Q1, Q4, Q14, paper B Q1, Q5, Q11, Q15, paper C Q1, Q6, Q7, Q10, the check card and results, at 1280 and 390 px. No page errors and no sideways scroll at 390 px. Fractions use `\dfrac` in questions and options (as mock-oa-arith found `\tfrac` too small), `\tfrac` in explanations.
- Start card lists "Number sequences, 15 questions · 25 minutes · pass 10 net · forward only, no skipping", then the other two papers and the check; at 390 px the list starts below the fold (known, raised by mock-oa-sig).
- One fault fixed: the times-plus explanation read "Each term is $2\times$ the one before $-1$"; it now says "double the one before, minus 1".
- One engine fault seen and not fixable in content: the results page says "Pass mark NaN%." on every paper (backlog bullet).

## Departures from the brief, for the orchestrator

1. `models` split into two sentences ("...test batteries. Number sequences, ...") because the brief's single sentence is 23 words and the voice scan must read 0.
2. A4 (version 1): the brief's distractor 64 sits with 66 at equal distance either side of the key 65, which the orchestrator's rule forbids. Replaced by 67 ("doubled and added 1: the sign is wrong").
3. A14 (version 1): the brief's 261 and 391 sit 65 either side of 326. 391 replaced by 114 (repeated the last gap of 49).
4. B6 (version 1): 7/2 and 5 sit 3/4 either side of 17/4. 5 replaced by 161/36 (kept the better of two rolls).
5. C7 (version 1): the brief's misses 16 to 17 and 18 to 19 put the key midway. Misses are now 16 to 17 and 19 to 20, so the key is next to one miss only. In every interval item one miss is adjacent and the other is one width away, and the side of the gap varies.
6. C2 (version 1) is kept as the brief wrote it; it has no event that tempts $n \times p$ or "more trials". Every other ranking item has one (asserted).
7. Seeds: the parameters live in per-version tables (picked so every check holds); the seed only orders the stored options. Version 1's tables hold the brief's worked items.
8. Option texts of intervals use one decimal count per item ("5.0 to 10.0", "0.10 to 0.12") so ascending order reads cleanly.

## Every keyed answer and its two computations

The generator's output, verbatim. Paper A: key, the rule run forward and a second reading; every shown sequence fits only its own family among the brief's 15 (fit functions in `seqs.py`), and generic rival rules that also fit (first- and second-order linear recurrences over the rationals, a difference table) predict the same key. Paper B: closed form, then enumeration, an exhaustive policy search, an exact Markov solve or a series with its exact tail. Paper C: exact Fractions two ways, gaps of at least 0.02; interval keys by exact squares or exact Fraction powers, with exactly one narrowest holder.

```
== version 1 (seed 2501) -> /home/user/zero-to-quant/app/content/exams/mock-oa-trader.json
A1  arithmetic             7, 11, 15, 19, 23, ? -> 27  (twice: 7 + 5 x 4 = 27; 23 + 4 = 27)  distractors [31, 46, 28]  rivals agree: linear first-order recurrence, polynomial (difference table), linear second-order recurrence
A2  geometric              2, 6, 18, 54, 162, ? -> 486  (twice: 3 x 162 = 486; 2 x 3^5 = 486)  distractors [270, 324, 487]  rivals agree: linear first-order recurrence
A3  squares                5, 10, 17, 26, 37, ? -> 50  (twice: 7^2 + 1 = 50; gaps rise by 2, 37 + 13 = 50)  distractors [48, 49, 74]  rivals agree: polynomial (difference table)
A4  times-plus             3, 5, 9, 17, 33, ? -> 65  (twice: 2 x 33 - 1 = 65; gaps double, 33 + 32 = 65)  distractors [49, 66, 67]  rivals agree: linear first-order recurrence, linear second-order recurrence
A5  second-diff            2, 5, 11, 20, 32, ? -> 47  (twice: 32 + 15 = 47; 2 + sum of gaps [3, 6, 9, 12, 15] = 47)  distractors [44, 64, 48]  rivals agree: polynomial (difference table)
A6  alternating            4, 8, 5, 10, 7, 14, ? -> 11  (twice: 14 then - 3 = 11; every other term is 2 x previous - 3: 2 x 7 - 3 = 11)  distractors [28, 21, 12]
A7  fibonacci              3, 4, 7, 11, 18, 29, ? -> 47  (twice: 18 + 29 = 47; also 2 x 18 + 11 = 47)  distractors [40, 58, 48]  rivals agree: linear second-order recurrence
A8  interleaved            1, 20, 4, 18, 7, 16, 10, ? -> 14  (twice: even places [20, 18, 16] step -2: 16 −2 = 14; 20 + 3 x -2 = 14)  distractors [13, 4, 20]
A9  digit-sum              19, 29, 40, 44, 52, 59, ? -> 73  (twice: 59 + (5 + 9) = 73; whole chain [19, 29, 40, 44, 52, 59] rebuilt from 19)  distractors [66, 118, 74]
A10 primes                 3, 5, 8, 11, 16, 19, ? -> 24  (twice: p_7 + 7 = 17 + 7 = 24; gaps are prime gaps + 1: 19 + 4 + 1 = 24)  distractors [22, 23, 38]
A11 cubes                  6, 25, 62, 123, 214, ? -> 341  (twice: 7^3 - 2 = 341; difference table, third difference 6: 341)  distractors [305, 428, 343]
A12 interleaved-geometric  1, 10, 3, 20, 9, 40, 27, ? -> 80  (twice: 40 x 2 = 80; 10 x 2^3 = 80)  distractors [81, 54, 67]
A13 consecutive-products   6, 12, 20, 30, 42, ? -> 56  (twice: 7 x 8 = 56; gaps rise by 2: 42 + 14 = 56)  distractors [54, 84, 64]  rivals agree: polynomial (difference table)
A14 rising-multiplier      1, 2, 5, 16, 65, ? -> 326  (twice: 5 x 65 + 1 = 326; chain rebuilt from 1: [1, 2, 5, 16, 65, 326])  distractors [325, 261, 114]
A15 tribonacci             1, 2, 3, 6, 11, 20, 37, ? -> 68  (twice: 11 + 20 + 37 = 68; also 2 x 37 - 6 = 68)  distractors [57, 54, 74]
B1  dice-sum           key 1/9  (twice: 4 of 36 pairs; enumeration of 36)  distractors ['1/11', '8/9', '2/9']
B2  binomial           key 5/16  (twice: C(5,2)/2^5; enumeration of 32 sequences)  distractors ['1/32', '2/5', '11/16']
B3  at-least-one       key 91/216  (twice: 1 - (5/6)^3; enumeration of 216)  distractors ['1/2', '125/216', '1/216']
B4  cards-conditional  key 25/51  (twice: 25 reds left of 51; enumeration of 52 x 51 ordered pairs)  distractors ['1/2', '25/102', '26/51']
B5  same-suit          key 22/425  (twice: 12/51 x 11/50; 4 C(13,3) of C(52,3) hands = 1144/22100)  distractors ['1/16', '11/850', '1/64']
B6  reroll-ev          key 17/4  (twice: keep 4 to 6: 15/6 + (1/2)(7/2); search over all 64 keep sets)  distractors ['7/2', '161/36', '25/6']
B7  distinct-days      key 30/49  (twice: 1 x 6/7 x 5/7; 210 of 343 triples)  distractors ['19/49', '4/7', '5/7']
B8  first-success      key 25/216  (twice: (5/6)^2 (1/6); enumeration of 216)  distractors ['1/6', '1/216', '91/216']
B9  committee          key 5/14  (twice: C(4,2) C(5,1) / C(9,3) = 30/84; enumeration of 84 teams)  distractors ['5/42', '80/243', '9/14']
B10 urn                key 3/5  (twice: 2 x 3/5 x 2/4; enumeration of 20 ordered draws)  distractors ['12/25', '3/10', '2/5']
B11 natural-frequency  key 9/28  (twice: Bayes 0.05x0.9 / (0.05x0.9 + 0.95x0.1); per 1,000: (50, 45, 95))  distractors ['9/10', '9/200', '1/20']
B12 max-of-dice        key 7/36  (twice: (16 - 9)/36; enumeration of 36)  distractors ['4/9', '1/6', '1/9']
B13 given-the-total    key 2/5  (twice: 2 of the 5 pairs; enumeration of 36 then restrict)  distractors ['11/36', '1/3', '1/18']
B14 first-to-six       key 6/11  (twice: (1/6)/(1 - 25/36); series (1/6) sum (25/36)^k, 60 terms plus exact tail)  distractors ['1/2', '1/6', '5/11']
B15 pattern-race       key 1/4  (twice: HH first only if the first two tosses are HH; exact Markov solve; 12-toss enumeration 0.2500)  distractors ['1/2', '3/4', '1/3']
c01 d2 six4 671/1296 = 0.518; dbl24 11033126465283976852912127963392284191/22452257707354557240087211123792674816 = 0.491; h6of10 193/512 = 0.377  gaps 0.026, 0.114  slips: [('six4', 'n x p reads 4/6 = 0.667'), ('dbl24', 'n x p reads 24/36 = 0.667')]
c02 d2 h2of4 3/8 = 0.375; suit2 4/17 = 0.235; tot7 1/6 = 0.167  gaps 0.140, 0.069  slips: []
c03 d3 diffcol 26/51 = 0.510; tot678 4/9 = 0.444; six3 91/216 = 0.421  gaps 0.065, 0.023  slips: [('six3', 'n x p reads 3/6 = 0.5')]
c04 d3 h1of2 1/2 = 0.500; h3of6 5/16 = 0.312; h5of10 63/256 = 0.246  gaps 0.188, 0.066  slips: [('h5of10', 'more tosses, more likely')]
c05 d4 diff3 5/9 = 0.556; bday23 38093904702297390785243708291056390518886454060947061/75091883268515350125426207425223147563269805908203125 = 0.507; ace5 18472/54145 = 0.341  gaps 0.048, 0.166  slips: [('ace5', 'n x p reads 5/13 = 0.385')]
c06 d5 np1 31031/46656 = 0.665; np2 1346704211/2176782336 = 0.619; np3 15166600495229/25389989167104 = 0.597  gaps 0.046, 0.021  slips: [('np1', 'n x p reads 1 for all three'), ('np2', 'more rolls, more likely'), ('np3', 'more rolls, more likely')]
c07 d2 value 17.3205 (twice: $17^2 = 289$ and $18^2 = 324$ bracket 300; 10 sqrt 3 = 17.3205)  key [17, 18]  wide [15, 20]  misses [('16', '17'), ('19', '20')] (below, above)  margin 0.3205
c08 d3 value 1.97993 (twice: rule of 72: doubling in 14.4 years, so just under 2; exact Fraction power 1.97993)  key [1.9, 2]  wide [1.5, 2.5]  misses [('1.7', '1.8'), ('2', '2.1')] (below, above)  margin 0.02007
c09 d4 value 0.112157 (twice: (5/6)^6 is about 0.335, and 0.335^2 is about 0.112; exact Fraction power 0.112157)  key [0.1, 0.12]  wide [0.05, 0.25]  misses [('0.08', '0.1'), ('0.14', '0.16')] (below, above)  margin 0.007843
c10 d5 value 7.24465 (twice: ln 1.02 is about 0.0198, so the value is about e^1.98, near 7.24; exact Fraction power 7.24465)  key [7, 7.5]  wide [5, 10]  misses [('6', '6.5'), ('7.5', '8')] (below, above)  margin 0.2446
== version 2 (seed 2502) -> /home/user/zero-to-quant/app/content/exams/mock-oa-trader-2.json
A1  arithmetic             13, 19, 25, 31, 37, ? -> 43  (twice: 13 + 5 x 6 = 43; 37 + 6 = 43)  distractors [49, 74, 44]  rivals agree: linear first-order recurrence, polynomial (difference table), linear second-order recurrence
A2  geometric              7, 14, 28, 56, 112, 224, ? -> 448  (twice: 2 x 224 = 448; 7 x 2^6 = 448)  distractors [336, 672, 449]  rivals agree: linear first-order recurrence
A3  squares                6, 13, 22, 33, 46, ? -> 61  (twice: 8^2 - 3 = 61; gaps rise by 2, 46 + 15 = 61)  distractors [59, 64, 92]  rivals agree: polynomial (difference table)
A4  times-plus             1, 5, 13, 29, 61, ? -> 125  (twice: 2 x 61 + 3 = 125; gaps double, 61 + 64 = 125)  distractors [93, 122, 119]  rivals agree: linear first-order recurrence, linear second-order recurrence
A5  second-diff            10, 14, 19, 25, 32, 40, ? -> 49  (twice: 40 + 9 = 49; 10 + sum of gaps [4, 5, 6, 7, 8, 9] = 49)  distractors [48, 80, 47]  rivals agree: polynomial (difference table)
A6  alternating            3, 9, 5, 15, 11, 33, ? -> 29  (twice: 33 then - 4 = 29; every other term is 3 x previous - 4: 3 x 11 - 4 = 29)  distractors [99, 55, 30]
A7  fibonacci              1, 5, 6, 11, 17, 28, ? -> 45  (twice: 17 + 28 = 45; also 2 x 17 + 11 = 45)  distractors [39, 56, 46]  rivals agree: linear second-order recurrence
A8  interleaved            2, 30, 7, 32, 12, 34, 17, ? -> 36  (twice: even places [30, 32, 34] step 2: 34 +2 = 36; 30 + 3 x 2 = 36)  distractors [22, 37, 51]
A9  digit-sum              23, 28, 38, 49, 62, 70, ? -> 77  (twice: 70 + (7 + 0) = 77; whole chain [23, 28, 38, 49, 62, 70] rebuilt from 23)  distractors [78, 140, 79]
A10 primes                 23, 29, 31, 37, 41, 43, ? -> 47  (twice: next prime after 43 is 47; trial division of 47 by 2, 3, 5, 7 leaves remainders)  distractors [45, 48, 86]
A11 cubes                  4, 11, 30, 67, 128, ? -> 219  (twice: 6^3 + 3 = 219; difference table, third difference 6: 219)  distractors [189, 256, 216]
A12 interleaved-geometric  5, 1, 10, 3, 20, 9, 40, ? -> 27  (twice: 9 x 3 = 27; 1 x 3^3 = 27)  distractors [80, 18, 49]
A13 consecutive-products   72, 90, 110, 132, 156, ? -> 182  (twice: 13 x 14 = 182; gaps rise by 2: 156 + 26 = 182)  distractors [180, 312, 196]  rivals agree: polynomial (difference table)
A14 rising-multiplier      2, 3, 7, 22, 89, ? -> 446  (twice: 5 x 89 + 1 = 446; chain rebuilt from 2: [2, 3, 7, 22, 89, 446])  distractors [445, 535, 156]
A15 tribonacci             2, 3, 4, 9, 16, 29, 54, ? -> 99  (twice: 16 + 29 + 54 = 99; also 2 x 54 - 9 = 99)  distractors [83, 79, 108]
B1  dice-sum           key 1/12  (twice: 3 of 36 pairs; enumeration of 36)  distractors ['1/11', '11/12', '1/6']
B2  binomial           key 15/64  (twice: C(6,2)/2^6; enumeration of 64 sequences)  distractors ['1/64', '1/3', '49/64']
B3  at-least-one       key 11/36  (twice: 1 - (5/6)^2; enumeration of 36)  distractors ['1/3', '25/36', '1/36']
B4  cards-conditional  key 1/17  (twice: 3 aces left of 51; enumeration of 52 x 51 ordered pairs)  distractors ['1/13', '1/221', '4/51']
B5  same-suit          key 4/19  (twice: 4/19 of the 19 cards left; 4 C(5,2) of C(20,2) = 40/190)  distractors ['1/4', '1/19', '1/16']
B6  reroll-ev          key 14/3  (twice: keep 5 or 6: 11/6 + (2/3)(17/4); search over all keep sets at each stage)  distractors ['17/4', '7/2', '11/2']
B7  distinct-days      key 5/18  (twice: 1 x 5/6 x 4/6 x 3/6; 360 of 1296)  distractors ['13/18', '5/54', '5/432']
B8  first-success      key 9/64  (twice: (3/4)^2 (1/4); enumeration of 4^3)  distractors ['1/4', '1/64', '37/64']
B9  committee          key 3/10  (twice: C(4,2) C(6,1) / C(10,3) = 36/120; enumeration of 120 teams)  distractors ['1/10', '36/125', '7/10']
B10 urn                key 2/5  (twice: 4/6 x 3/5; enumeration of 30 ordered draws)  distractors ['4/9', '3/5', '2/3']
B11 natural-frequency  key 3/7  (twice: Bayes 0.2x0.75 / (0.2x0.75 + 0.8x0.25); per 100: (20, 15, 20))  distractors ['3/4', '3/20', '1/5']
B12 max-of-dice        key 19/216  (twice: (27 - 8)/216; enumeration of 216)  distractors ['1/8', '1/6', '1/216']
B13 given-the-total    key 1/5  (twice: 1 of the 5 pairs; enumeration of 36 then restrict)  distractors ['11/36', '1/3', '1/36']
B14 first-to-six       key 3/5  (twice: (1/3)/(1 - 4/9); series (1/3) sum (4/9)^k, 60 terms plus exact tail)  distractors ['1/2', '1/3', '2/5']
B15 pattern-race       key 1/4  (twice: HHT first only if the first two tosses are HH; exact Markov solve; 12-toss enumeration 0.2498)  distractors ['1/2', '3/4', '1/8']
c01 d2 die56 1/3 = 0.333; six2 11/36 = 0.306; akq 3/13 = 0.231  gaps 0.028, 0.075  slips: [('six2', 'n x p reads 2/6 = 0.333')]
c02 d2 h1of3 3/8 = 0.375; ace3r 469/2197 = 0.213; dbl 1/6 = 0.167  gaps 0.162, 0.047  slips: [('ace3r', 'n x p reads 3/13 = 0.231')]
c03 d3 redace 7/13 = 0.538; tot57 5/12 = 0.417; ace6r 1840825/4826809 = 0.381  gaps 0.122, 0.035  slips: [('ace6r', 'n x p reads 6/13 = 0.462')]
c04 d3 h4of5 3/16 = 0.188; tot1112 1/12 = 0.083; h8of10 7/128 = 0.055  gaps 0.104, 0.029  slips: [('h8of10', 'more tosses, more likely')]
c05 d4 six8 1288991/1679616 = 0.767; bday30 9155292769247515688463664204581601330417463671119878183963440529188469/12962030625262519859085092767427552277425499342208403503894805908203125 = 0.706; ace10 349/595 = 0.587  gaps 0.061, 0.120  slips: [('six8', 'n x p reads 8/6, over 1'), ('ace10', 'n x p reads 10/13 = 0.769')]
c06 d5 c1of2 3/4 = 0.750; c2of4 11/16 = 0.688; c3of6 21/32 = 0.656  gaps 0.062, 0.031  slips: [('c2of4', 'more tosses, more likely'), ('c3of6', 'more tosses, more likely')]
c07 d2 value 22.3607 (twice: $22^2 = 484$ and $23^2 = 529$ bracket 500; 10 sqrt 5 = 22.3607)  key [22, 23]  wide [20, 25]  misses [('21', '22'), ('24', '25')] (below, above)  margin 0.3607
c08 d3 value 2.25219 (twice: 1.07^10 is about 1.97 (rule of 72), times 1.07^2 = 1.1449 gives about 2.25; exact Fraction power 2.25219)  key [2.2, 2.3]  wide [2, 3]  misses [('2', '2.1'), ('2.3', '2.4')] (below, above)  margin 0.04781
c09 d4 value 0.366032 (twice: (1 - 1/n)^n is just under 1/e = 0.368; exact Fraction power 0.366032)  key [0.35, 0.38]  wide [0.2, 0.5]  misses [('0.32', '0.35'), ('0.41', '0.44')] (below, above)  margin 0.01397
c10 d5 value 0.176197 (twice: sqrt(2/(pi n)) with n = 20 is about 0.178; 184756/1048576 = 0.176197)  key [0.17, 0.19]  wide [0.1, 0.3]  misses [('0.14', '0.16'), ('0.19', '0.21')] (below, above)  margin 0.006197
== version 3 (seed 2503) -> /home/user/zero-to-quant/app/content/exams/mock-oa-trader-3.json
A1  arithmetic             52, 45, 38, 31, 24, ? -> 17  (twice: 52 + 5 x -7 = 17; 24 + -7 = 17)  distractors [10, 31, 18]  rivals agree: linear first-order recurrence, polynomial (difference table), linear second-order recurrence
A2  geometric              4, 12, 36, 108, 324, ? -> 972  (twice: 3 x 324 = 972; 4 x 3^5 = 972)  distractors [540, 648, 973]  rivals agree: linear first-order recurrence
A3  squares                19, 28, 39, 52, 67, ? -> 84  (twice: 9^2 + 3 = 84; gaps rise by 2, 67 + 17 = 84)  distractors [82, 81, 134]  rivals agree: polynomial (difference table)
A4  times-plus             5, 7, 11, 19, 35, ? -> 67  (twice: 2 x 35 - 3 = 67; gaps double, 35 + 32 = 67)  distractors [51, 70, 73]  rivals agree: linear first-order recurrence, linear second-order recurrence
A5  second-diff            3, 8, 17, 30, 47, ? -> 68  (twice: 47 + 21 = 68; 3 + sum of gaps [5, 9, 13, 17, 21] = 68)  distractors [64, 94, 69]  rivals agree: polynomial (difference table)
A6  alternating            6, 12, 7, 14, 9, 18, 13, ? -> 26  (twice: 13 then \times 2 = 26; the places after a multiply have doubling gaps: 18 + 2 x 4 = 26)  distractors [8, 31, 25]
A7  fibonacci              2, 7, 9, 16, 25, 41, ? -> 66  (twice: 25 + 41 = 66; also 2 x 25 + 16 = 66)  distractors [57, 82, 67]  rivals agree: linear second-order recurrence
A8  interleaved            40, 3, 36, 6, 32, 9, 28, ? -> 12  (twice: even places [3, 6, 9] step 3: 9 +3 = 12; 3 + 3 x 3 = 12)  distractors [24, 13, 56]
A9  digit-sum              26, 34, 41, 46, 56, 67, ? -> 80  (twice: 67 + (6 + 7) = 80; whole chain [26, 34, 41, 46, 56, 67] rebuilt from 26)  distractors [78, 134, 74]
A10 primes                 53, 59, 61, 67, 71, 73, ? -> 79  (twice: next prime after 73 is 79; trial division of 79 by 2, 3, 5, 7 leaves remainders)  distractors [75, 77, 146]
A11 cubes                  29, 66, 127, 218, 345, ? -> 514  (twice: 8^3 + 2 = 514; difference table, third difference 6: 514)  distractors [472, 690, 512]
A12 interleaved-geometric  3, 1, 6, 4, 12, 16, 24, ? -> 64  (twice: 16 x 4 = 64; 1 x 4^3 = 64)  distractors [48, 32, 40]
A13 consecutive-products   240, 272, 306, 342, 380, ? -> 420  (twice: 20 x 21 = 420; gaps rise by 2: 380 + 40 = 420)  distractors [418, 760, 441]  rivals agree: polynomial (difference table)
A14 rising-multiplier      1, 3, 10, 41, 206, ? -> 1237  (twice: 6 x 206 + 1 = 1237; chain rebuilt from 1: [1, 3, 10, 41, 206, 1237])  distractors [1236, 1031, 371]
A15 tribonacci             3, 1, 5, 9, 15, 29, 53, ? -> 97  (twice: 15 + 29 + 53 = 97; also 2 x 53 - 9 = 97)  distractors [82, 77, 106]
B1  dice-sum           key 5/36  (twice: 5 of 36 pairs; enumeration of 36)  distractors ['1/11', '31/36', '5/18']
B2  binomial           key 5/32  (twice: C(5,4)/2^5; enumeration of 32 sequences)  distractors ['1/32', '4/5', '27/32']
B3  at-least-one       key 37/64  (twice: 1 - (3/4)^3; enumeration of 52^3 draws)  distractors ['3/4', '27/64', '1/64']
B4  cards-conditional  key 13/51  (twice: 13 hearts left of 51; enumeration of 52 x 51 ordered pairs)  distractors ['1/4', '13/204', '4/17']
B5  same-suit          key 6/19  (twice: 12/38; 3 C(13,2) of C(39,2) = 234/741)  distractors ['1/3', '2/19', '1/9']
B6  reroll-ev          key 23/6  (twice: keep 3 to 6: 18/6 + (1/3)(5/2); search over all keep sets with the fee)  distractors ['7/2', '17/4', '9/2']
B7  distinct-days      key 55/96  (twice: 11/12 x 10/12 x 9/12; 11880 of 20736)  distractors ['41/96', '1/2', '55/144']
B8  first-success      key 12/169  (twice: (12/13)(1/13); enumeration of 13^2 ranks)  distractors ['1/13', '1/169', '25/169']
B9  committee          key 15/28  (twice: 3 x 5 / C(8,2) = 15/28; enumeration of 28 pairs)  distractors ['15/56', '15/32', '13/28']
B10 urn                key 1/14  (twice: 4/8 x 3/7 x 2/6; enumeration of 336 ordered draws)  distractors ['1/8', '13/14', '1/7']
B11 natural-frequency  key 45/143  (twice: Bayes 0.02x0.9 / (0.02x0.9 + 0.98x0.04); per 10,000: (200, 180, 392))  distractors ['9/10', '9/500', '1/50']
B12 max-of-dice        key 1/4  (twice: (25 - 16)/36; enumeration of 36)  distractors ['25/36', '1/6', '5/36']
B13 given-the-total    key 1/3  (twice: 1 of the 3 pairs; enumeration of 36 then restrict)  distractors ['11/36', '1/2', '1/36']
B14 first-to-six       key 36/91  (twice: (1/6)/(1 - 125/216); series (1/6) sum (125/216)^k, 60 terms plus exact tail)  distractors ['1/3', '1/6', '30/91']
B15 pattern-race       key 1/8  (twice: HHH first only if the first three tosses are HHH; exact Markov solve; 12-toss enumeration 0.1250)  distractors ['1/2', '7/8', '1/4']
c01 d2 die3up 2/3 = 0.667; six5 4651/7776 = 0.598; tot8up 5/12 = 0.417  gaps 0.069, 0.181  slips: [('six5', 'n x p reads 5/6 = 0.833')]
c02 d2 heart2r 7/16 = 0.438; akqj 4/13 = 0.308; h3of4 1/4 = 0.250  gaps 0.130, 0.058  slips: [('heart2r', 'n x p reads 2/4 = 0.5')]
c03 d3 ace4 15229/54145 = 0.281; same3 1/4 = 0.250; tot510 7/36 = 0.194  gaps 0.031, 0.056  slips: [('ace4', 'n x p reads 4/13 = 0.308')]
c04 d3 one6of6 3125/7776 = 0.402; one6of3 25/72 = 0.347; two6of12 107421875/362797056 = 0.296  gaps 0.055, 0.051  slips: [('one6of6', 'more rolls, more likely'), ('two6of12', 'more rolls, more likely')]
c05 d4 dbl36 67799596446321320449400950582983601554324864754615150511/106387358923716524807713475752456393740167855629859291136 = 0.637; bday25 5689337892098486666289143070200558294086544632989664632317/10004116148447957520459906484225353834116619892120361328125 = 0.569; ace8 19282/38675 = 0.499  gaps 0.069, 0.070  slips: [('dbl36', 'n x p reads 36/36 = 1'), ('ace8', 'n x p reads 8/13 = 0.615')]
c06 d5 f1of3 19/27 = 0.704; f2of6 473/729 = 0.649; f3of9 12259/19683 = 0.623  gaps 0.055, 0.026  slips: [('f1of3', 'n x p reads 1 for all three'), ('f2of6', 'more rolls, more likely'), ('f3of9', 'more rolls, more likely')]
c07 d2 value 26.4575 (twice: $26^2 = 676$ and $27^2 = 729$ bracket 700; 10 sqrt 7 = 26.4575)  key [26, 27]  wide [25, 30]  misses [('24', '25'), ('27', '28')] (below, above)  margin 0.4575
c08 d3 value 2.6533 (twice: 1.05^14 is about 1.98, and 1.05^6 is about 1.34, so about 2.65; exact Fraction power 2.65330)  key [2.6, 2.7]  wide [2, 3]  misses [('2.5', '2.6'), ('2.8', '2.9')] (below, above)  margin 0.0467
c09 d4 value 0.0563135 (twice: 0.75^5 is about 0.237, and 0.237^2 is about 0.056; exact Fraction power 0.0563135)  key [0.05, 0.06]  wide [0.02, 0.1]  misses [('0.03', '0.04'), ('0.06', '0.07')] (below, above)  margin 0.003686
c10 d5 value 0.144464 (twice: sqrt(2/(pi n)) with n = 30 is about 0.146; 155117520/1073741824 = 0.144464)  key [0.13, 0.16]  wide [0.1, 0.3]  misses [('0.1', '0.13'), ('0.19', '0.22')] (below, above)  margin 0.01446
all keys agree two ways; all placement, gap, interval and uniqueness checks passed
```

## Prerequisites (cited, nothing gated)

mental-pressure `l10-next-in-sequence`, `l16-harder-sequences`, `l14-ranking-likelihoods`, `l15-probability-at-speed`, `l13-negative-marking`, `l17-full-battery`, `l7-estimating-products`, `l8-square-roots`; puzzles `l7-cards-and-colours`, `l9-bayes-in-a-minute`, `l27-given-the-total`.

## Proposed changes

- `prep.json`: none needed for version 1 (already listed). If versions should show on the Prepare page, add `mock-oa-trader-2` and `mock-oa-trader-3` after `mock-oa-trader` in `oa-trader` and in the Optiver, IMC and Citadel Securities firm paths; better, wait for E3 and keep one id.
- No `course.json` change.

## Backlog bullets added (5)

Under `Raised later (exam mock-oa-trader):` in `docs/BACKLOG-INBOX.md`: the NaN pass mark, interval scoring by width, the bank draw (E3), playthrough shot names on multi-paper exams, and order-widget partial credit.

## Scripts

Run `python3 gen_trader.py` in the scratch folder; it imports the four modules below.

### `gen_trader.py`

```python
#!/usr/bin/env python3
"""gen_trader.py: writes app/content/exams/mock-oa-trader.json, -2.json and -3.json.
Seeds 2501, 2502, 2503 (versions 1 to 3). The parameters of every item sit in per-version tables in seqs.py, probs.py
and rank.py (version 1 holds the brief's worked items as its FIXED values); the seed orders the stored options of
shuffled choices (the engine reshuffles them anyway). Every key is asserted two ways when the modules load or build."""
import json, random, sys
import seqs, probs, rank

OUT = "/home/user/zero-to-quant/app/content/exams/"
SEEDS = {1: 2501, 2: 2502, 3: 2503}
MODELS = ("Reported, as of Nov 2026: the Optiver, IMC and Citadel Securities test batteries. Number sequences, "
          "probability at speed, and likelihood ranking with intervals.")
DESC = ("These are reported formats from the Optiver, IMC and Citadel Securities test batteries, as described by Nov 2026. "
        "There are three papers, each on its own clock. Sequences is 15 questions in 25 minutes, one at a time, with no skipping. "
        "Probability at speed is 15 questions in 30 minutes; you may move between them. "
        "Likelihood ranking and intervals is 10 questions in 10 minutes. "
        "Wrong answers score 0, and no calculator is allowed. "
        "Firms mix and rename these papers, so expect a different order on the day. This is version {v} of 3.")
SKILLS = {"mp-formats": "Test formats", "mp-estimate": "Fast estimation",
          "mp-fractions": "Fractions and percentages at speed", "pz-conditioning": "Conditioning puzzles"}
SCORE = {"right": 1, "wrong": 0, "blank": 0}

def exam(v):
    rng = random.Random(SEEDS[v])
    a, la = seqs.to_json(v, rng)
    b, lb = probs.to_json(v, rng)
    c1, lc1 = rank.build_rank(v)
    c2, lc2 = rank.build_iv(v)
    assert len(a) == 15 and len(b) == 15 and len(c1) + len(c2) == 10
    doc = {
        "id": "mock-oa-trader" if v == 1 else f"mock-oa-trader-{v}",
        "name": "Trader test battery" if v == 1 else f"Trader test battery, version {v}",
        "style": "trader", "models": MODELS, "description": DESC.format(v=v), "skills": SKILLS,
        "parts": [
            {"kind": "paper", "id": "sequences", "name": "Number sequences", "minutes": 25, "scoring": SCORE,
             "passNet": 10, "navigation": "forward", "skip": False, "items": a},
            {"kind": "paper", "id": "probability", "name": "Probability at speed", "minutes": 30, "scoring": SCORE,
             "passNet": 10, "items": b},
            {"kind": "paper", "id": "ranking", "name": "Likelihood ranking and intervals", "minutes": 10, "scoring": SCORE,
             "passNet": 6, "items": c1 + c2},
            {"kind": "check", "id": "no-calculator", "name": "I used no calculator",
             "detail": "Tick this only if you sat all three papers without one."},
        ]}
    return doc, la + lb + lc1 + lc2

if __name__ == "__main__":
    seen = {}
    for v in (1, 2, 3):
        doc, log = exam(v)
        # no item repeated across versions: questions and option sets must differ
        for p in doc["parts"]:
            for it in p.get("items", []):
                sig = (it["question"], json.dumps(it["widget"].get("lines") or sorted(o["text"] for o in it["widget"]["options"])))
                assert sig not in seen, ("repeated item", v, it["id"], seen.get(sig))
                seen[sig] = (v, it["id"])
        path = OUT + doc["id"] + ".json"
        with open(path, "w") as f:
            json.dump(doc, f, ensure_ascii=False, indent=2); f.write("\n")
        print(f"== version {v} (seed {SEEDS[v]}) -> {path}")
        print("\n".join(log))
    print("all keys agree two ways; all placement, gap, interval and uniqueness checks passed")
```

### `common.py`

```python
"""Shared helpers for gen_trader.py: number formatting, the distractor-placement check and item assembly."""
from fractions import Fraction as F
import random

def num(n):
    """An integer in KaTeX, with a thin comma from 1,000 up."""
    n = int(n)
    s = f"{abs(n):,}".replace(",", "{,}")
    return ("-" if n < 0 else "") + s

def fr(x, big=True):
    """A Fraction in KaTeX, lowest terms (Fraction keeps them)."""
    x = F(x)
    if x.denominator == 1:
        return num(x.numerator)
    cmd = "\\dfrac" if big else "\\tfrac"
    return f"{cmd}{{{x.numerator}}}{{{x.denominator}}}"

def check_placement(key, others, label):
    """The key must not sit between a times-ten pair, nor between two equal slips (equal distances either side)."""
    key = F(key)
    vals = [F(v) for v in others]
    assert len(set(vals + [key])) == len(vals) + 1, (label, "repeated option value")
    for a in vals:
        for b in vals:
            if a < key < b:
                assert b != 10 * a, (label, "key between a times-ten pair", a, b)
                assert key - a != b - key, (label, "key between two equal slips", a, b)
    return True

def choice_widget(rng, correct_text, distractors, shuffle=True):
    """distractors: list of (text, why). Option ids a to d; the stored order is drawn from rng (the engine reshuffles)."""
    opts = [{"text": correct_text, "correct": True}] + [{"text": t, "why": w} for t, w in distractors]
    if shuffle:
        rng.shuffle(opts)
    out = []
    for i, o in enumerate(opts):
        d = {"id": "abcd"[i], "text": o["text"]}
        if o.get("correct"):
            d["correct"] = True
        else:
            d["why"] = o["why"]
        out.append(d)
    w = {"kind": "choice", "layout": "grid", "label": "Answer options", "options": out}
    if shuffle:
        w = {"kind": "choice", "layout": "grid", "shuffle": True, "label": "Answer options", "options": out}
    return w

def item(id_, difficulty, skills, tags, pace, title, question, widget, correct, generic, explain):
    return {"id": id_, "difficulty": difficulty, "skills": skills, "tags": tags, "pace": pace, "title": title,
            "question": question, "widget": widget,
            "feedback": {"correct": correct, "generic": generic}, "explain": {"text": explain}}
```

### `seqs.py`

```python
"""Paper A: number sequences. One template per position, parameters per version, distractors labelled by slip.
Every key is computed twice (the rule run forward, and a closed form or second reading), and the shown terms are
tested against every other template in the brief's table and against generic rival rules."""
from fractions import Fraction as F
from common import num, check_placement, choice_widget, item

def primes_upto(n):
    s = [True] * (n + 1); s[0] = s[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            for j in range(i * i, n + 1, i): s[j] = False
    return [i for i in range(n + 1) if s[i]]
P = primes_upto(2000)          # P[0] = 2 is p_1
def p(n): return P[n - 1]
def ds(n): return sum(int(c) for c in str(n))

# ---------- fit tests: each returns the next term if the shown terms fit the family, else None ----------
def diffs(t): return [b - a for a, b in zip(t, t[1:])]
def fit_arithmetic(t):
    d = diffs(t)
    return t[-1] + d[0] if len(set(d)) == 1 and d[0] != 0 else None
def fit_geometric(t):
    if t[0] == 0 or t[1] % t[0]: return None
    k = t[1] // t[0]
    return k * t[-1] if k >= 2 and all(b == k * a for a, b in zip(t, t[1:])) else None
def fit_squares(t):
    for n0 in range(0, 41):
        c = t[0] - n0 * n0
        if all(v == (n0 + i) ** 2 + c for i, v in enumerate(t)): return (n0 + len(t)) ** 2 + c
    return None
def fit_times_plus(t):
    for k in (2, 3):
        c = t[1] - k * t[0]
        if c != 0 and all(b == k * a + c for a, b in zip(t, t[1:])): return k * t[-1] + c
    return None
def fit_second_diff(t):
    d2 = diffs(diffs(t))
    if len(d2) >= 2 and len(set(d2)) == 1 and d2[0] not in (0, 2):
        return t[-1] + (t[-1] - t[-2]) + d2[0]
    return None
def fit_alternating(t):
    for phase in (0, 1):
        ks, cs = set(), set(); ok = True
        for i in range(len(t) - 1):
            if (i + phase) % 2 == 0:
                if t[i] == 0 or t[i + 1] % t[i]: ok = False; break
                ks.add(t[i + 1] // t[i])
            else:
                cs.add(t[i] - t[i + 1])
        if ok and len(ks) == 1 and len(cs) == 1 and min(ks) >= 2 and min(cs) > 0:
            i = len(t) - 1
            return t[-1] * min(ks) if (i + phase) % 2 == 0 else t[-1] - min(cs)
    return None
def fit_fibonacci(t):
    return t[-1] + t[-2] if all(t[i] == t[i - 1] + t[i - 2] for i in range(2, len(t))) else None
def fit_interleaved(t):
    a, b = t[0::2], t[1::2]
    if len(b) < 3 or fit_arithmetic(t) is not None: return None
    da, db = set(diffs(a)), set(diffs(b))
    if len(da) == 1 and len(db) == 1:
        return a[-1] + min(da) if len(t) % 2 == 0 else b[-1] + min(db)
    return None
def fit_digit_sum(t):
    return t[-1] + ds(t[-1]) if all(b == a + ds(a) for a, b in zip(t, t[1:])) else None
def fit_primes(t):
    for s in (0, 1):
        for n0 in range(1, 200):
            if all(v == p(n0 + i) + s * (n0 + i) for i, v in enumerate(t)):
                m = n0 + len(t); return p(m) + s * m
    return None
def fit_cubes(t):
    for n0 in range(0, 21):
        c = t[0] - n0 ** 3
        if all(v == (n0 + i) ** 3 + c for i, v in enumerate(t)): return (n0 + len(t)) ** 3 + c
    return None
def fit_interleaved_geo(t):
    a, b = t[0::2], t[1::2]
    if len(a) < 3 or len(b) < 3: return None
    ra, rb = fit_geometric(a), fit_geometric(b)
    if ra is None or rb is None or a[1] // a[0] == b[1] // b[0]: return None
    return ra if len(t) % 2 == 0 else rb
def fit_cons_products(t):
    for n0 in range(0, 41):
        if all(v == (n0 + i) * (n0 + i + 1) for i, v in enumerate(t)):
            m = n0 + len(t); return m * (m + 1)
    return None
def fit_rising(t):
    for m0 in range(1, 11):
        for c in (-2, -1, 1, 2):
            if all(t[i + 1] == (m0 + i) * t[i] + c for i in range(len(t) - 1)):
                return (m0 + len(t) - 1) * t[-1] + c
    return None
def fit_tribonacci(t):
    return t[-1] + t[-2] + t[-3] if all(t[i] == t[i - 1] + t[i - 2] + t[i - 3] for i in range(3, len(t))) else None

FITS = {"arithmetic": fit_arithmetic, "geometric": fit_geometric, "squares": fit_squares, "times-plus": fit_times_plus,
        "second-diff": fit_second_diff, "alternating": fit_alternating, "fibonacci": fit_fibonacci,
        "interleaved": fit_interleaved, "digit-sum": fit_digit_sum, "primes": fit_primes, "cubes": fit_cubes,
        "interleaved-geometric": fit_interleaved_geo, "consecutive-products": fit_cons_products,
        "rising-multiplier": fit_rising, "tribonacci": fit_tribonacci}

# generic rivals, over the rationals
def rival_linear1(t):        # a(n+1) = k a(n) + c
    if t[1] == t[0]: return None
    k = F(t[2] - t[1], t[1] - t[0]); c = t[1] - k * t[0]
    return k * t[-1] + c if all(b == k * a + c for a, b in zip(t, t[1:])) else None
def rival_poly(t):           # a difference table that turns constant with at least three entries left
    row = list(t); last = []
    while len(row) >= 3:
        last.append(row[-1])
        if len(set(row)) == 1:
            return sum(last[:-1]) + row[-1]
        row = diffs(row)
    return None
def rival_linear2(t):        # a(n) = x a(n-1) + y a(n-2), solved from n = 2, 3 and checked on the rest
    if len(t) < 5: return None
    a11, a12, b1 = F(t[1]), F(t[0]), F(t[2]); a21, a22, b2 = F(t[2]), F(t[1]), F(t[3])
    det = a11 * a22 - a12 * a21
    if det == 0: return None
    x = (b1 * a22 - a12 * b2) / det; y = (a11 * b2 - b1 * a21) / det
    if all(t[i] == x * t[i - 1] + y * t[i - 2] for i in range(4, len(t))):
        return x * t[-1] + y * t[-2]
    return None
RIVALS = {"linear first-order recurrence": rival_linear1, "polynomial (difference table)": rival_poly,
          "linear second-order recurrence": rival_linear2}

def uniqueness(family, t, key):
    own = FITS[family](t)
    assert own == key, (family, t, own, key)
    others = [f for f, fn in FITS.items() if f != family and fn(t) is not None]
    assert not others, (family, t, "also fits", others)
    rivals = {}
    for name, fn in RIVALS.items():
        v = fn(t)
        if v is not None:
            assert v == key, (family, t, name, "fits with a different next term", v)
            rivals[name] = v
    return rivals

# ---------- the fifteen positions ----------
DIFF = {1: 2, 2: 2, 3: 2, 4: 3, 5: 3, 6: 3, 7: 3, 8: 3, 9: 4, 10: 4, 11: 4, 12: 4, 13: 4, 14: 5, 15: 5}
ORDER = ["arithmetic", "geometric", "squares", "times-plus", "second-diff", "alternating", "fibonacci", "interleaved",
         "digit-sum", "primes", "cubes", "interleaved-geometric", "consecutive-products", "rising-multiplier", "tribonacci"]
TITLE = {"arithmetic": "Equal gaps", "geometric": "A constant ratio", "squares": "Squares shifted",
         "times-plus": "Double and adjust", "second-diff": "Growing gaps", "alternating": "Two steps in turn",
         "fibonacci": "Sum of the two before", "interleaved": "Two lists in one", "digit-sum": "Add the digits",
         "primes": "Primes", "cubes": "Cubes shifted", "interleaved-geometric": "Two ratios in turn",
         "consecutive-products": "Neighbours multiplied", "rising-multiplier": "A rising multiplier",
         "tribonacci": "Sum of the three before"}

def seq_text(t): return ", ".join(num(v) if abs(v) < 1000 else f"{v:,}" for v in t)

def build(version):
    """Returns the 15 items of version 1, 2 or 3 and a log of the checks."""
    V = SEQ[version]
    items, log = [], []
    for q, fam in enumerate(ORDER, start=1):
        spec = V[fam]
        t, key = spec["terms"], spec["key"]
        assert key == spec["key2"], (version, fam, "second computation disagrees")
        # forward run of the rule
        assert spec["run"](t) == key, (version, fam, "rule run forward disagrees")
        rivals = uniqueness(fam, t, key)
        assert 5 <= len(t) <= 7
        if q < 14: assert max(t + [key]) < 1000, (version, fam, "terms over 1,000")
        vals = [v for v, _ in spec["wrong"]]
        check_placement(key, vals, f"v{version} A{q}")
        items.append((q, fam, spec, rivals))
        log.append(f"A{q:<2} {fam:<22} {seq_text(t)}, ? -> {key}  (twice: {spec['twice']})  distractors {vals}"
                   + (f"  rivals agree: {', '.join(rivals)}" if rivals else ""))
    return items, log

def to_json(version, rng):
    built, log = build(version)
    out = []
    for q, fam, spec, _ in built:
        t, key = spec["terms"], spec["key"]
        w = choice_widget(rng, f"${num(key)}$", [(f"${num(v)}$", why) for v, why in spec["wrong"]])
        out.append(item(f"a{q:02d}-{fam}", DIFF[q], ["mp-formats"], ["sequence", fam], 100, TITLE[fam],
                        f"What comes next? {seq_text(t)}, ?", w, spec["correct"], spec["generic"], spec["explain"]))
    return out, log

# ---------- parameters and copy, per version ----------
def nxt_arith(t): return t[-1] + (t[1] - t[0])
SEQ = {1: {}, 2: {}, 3: {}}

# Q1 arithmetic
for v, (a, d) in {1: (7, 4), 2: (13, 6), 3: (52, -7)}.items():
    t = [a + d * i for i in range(5)]; key = a + 5 * d
    SEQ[v]["arithmetic"] = dict(terms=t, key=key, key2=t[-1] + d, run=fit_arithmetic,
        twice=f"{a} + 5 x {d} = {key}; {t[-1]} + {d} = {key}",
        wrong=[(t[-1] + 2 * d, f"You added the gap of {abs(d)} twice." if d > 0 else f"You took the gap of {abs(d)} away twice."),
               (2 * t[-1], "You doubled the last term. The gaps are equal, not the ratios."),
               (key + 1, "You were one out. Check the last step again.")],
        correct=f"The gap is {d:+d} each time." if d > 0 else f"The gap is −{abs(d)} each time.",
        generic="Find the gap between neighbours, with its sign.",
        explain=f"Each term is {abs(d)} {'more' if d > 0 else 'less'} than the one before. So the next is ${num(t[-1])} {'+' if d > 0 else '-'} {abs(d)} = {num(key)}$.")
SEQ[3]["arithmetic"]["wrong"][1] = (SEQ[3]["arithmetic"]["terms"][-1] + 7, "You added 7 instead of taking it away.")

# Q2 geometric
for v, (a, k) in {1: (2, 3), 2: (7, 2), 3: (4, 3)}.items():
    t = [a * k ** i for i in range(5)]; key = a * k ** 5
    if v == 2: t = [a * k ** i for i in range(6)]; key = a * k ** 6
    gap = t[-1] - t[-2]
    other = 3 if k == 2 else 2
    SEQ[v]["geometric"] = dict(terms=t, key=key, key2=a * k ** len(t), run=fit_geometric,
        twice=f"{k} x {t[-1]} = {key}; {a} x {k}^{len(t)} = {key}",
        wrong=[(t[-1] + gap, f"You added the last gap of {gap} again. The gaps grow too."),
               (other * t[-1], f"You multiplied by {other}. Each term is {k} times the one before."),
               (key + 1, "You were one out. Multiply the last term again.")],
        correct=f"Each term is {k} times the one before.",
        generic="Divide each term by the one before it.",
        explain=f"The ratio is {k} throughout. So the next is ${k} \\times {num(t[-1])} = {num(key)}$.")

# Q3 squares n^2 + c
for v, (n0, c) in {1: (2, 1), 2: (3, -3), 3: (4, 3)}.items():
    t = [(n0 + i) ** 2 + c for i in range(5)]; m = n0 + 5; key = m * m + c
    gap = t[-1] - t[-2]
    cs = f"+ {c}" if c > 0 else f"- {abs(c)}"
    SEQ[v]["squares"] = dict(terms=t, key=key, key2=t[-1] + gap + 2, run=fit_squares,
        twice=f"{m}^2 {cs} = {key}; gaps rise by 2, {t[-1]} + {gap + 2} = {key}",
        wrong=[(t[-1] + gap, f"You added the last gap of {gap} again. The gaps grow by 2."),
               (m * m, f"You gave ${m}^2$ and dropped the {'+' if c > 0 else '−'}{abs(c)}."),
               (2 * t[-1], "You doubled the last term. The gaps grow by 2, so look for squares.")],
        correct=f"Each term is a square {'plus' if c > 0 else 'minus'} {abs(c)}: ${m}^2 {cs} = {key}$.",
        generic="Compare each term with the nearest square.",
        explain=f"The terms are $n^2 {cs}$ for $n = {n0}$ to ${n0 + 4}$. The next is ${m}^2 {cs} = {key}$. Check: the gaps rise by 2, so the next gap is {gap + 2}.")

# Q4 times-plus (x2 then +/- c)
for v, (a, c) in {1: (3, -1), 2: (1, 3), 3: (5, -3)}.items():
    t = [a]
    for _ in range(4): t.append(2 * t[-1] + c)
    key = 2 * t[-1] + c; gap = t[-1] - t[-2]
    cs = f"+ {c}" if c > 0 else f"- {abs(c)}"
    sw = 2 * t[-1] - c
    SEQ[v]["times-plus"] = dict(terms=t, key=key, key2=t[-1] + 2 * gap, run=fit_times_plus,
        twice=f"2 x {t[-1]} {cs} = {key}; gaps double, {t[-1]} + {2 * gap} = {key}",
        wrong=[(t[-1] + gap, f"You repeated the last gap of {gap}. The gaps double."),
               (2 * t[-1], f"You doubled {t[-1]} and left out the {'+' if c > 0 else '−'}{abs(c)}."),
               (sw, f"You doubled and then {'took away' if c > 0 else 'added'} {abs(c)}: the sign is wrong.")],
        correct=f"Double, then {'add' if c > 0 else 'take away'} {abs(c)}.",
        generic="Try doubling each term and see what is left over.",
        explain=f"Each term is double the one before, {'plus' if c > 0 else 'minus'} {abs(c)}. So the next is $2 \\times {t[-1]} {cs} = {key}$. Check: the gaps double, so the next gap is {2 * gap}.")

# Q5 second differences constant (not 2)
for v, (a, g0, g) in {1: (2, 3, 3), 2: (10, 4, 1), 3: (3, 5, 4)}.items():
    n = 5 if v != 2 else 6
    t = [a]; gaps = [g0 + g * i for i in range(n)]
    for x in gaps[:n - 1]: t.append(t[-1] + x)
    key = t[-1] + gaps[n - 1]; last = gaps[n - 2]
    wrong = [(t[-1] + last, f"You repeated the last gap of {last}. The gaps grow by {g}."),
             (2 * t[-1], "You doubled the last term. Look at the gaps instead."),
             (key + 1 if v != 2 else key - 2, "You were one out. Each gap is " + str(g) + " more than the last." if v != 2 else
              "You were two short. Each gap is 1 more than the last.")]
    SEQ[v]["second-diff"] = dict(terms=t, key=key, key2=a + sum(gaps), run=fit_second_diff,
        twice=f"{t[-1]} + {gaps[n - 1]} = {key}; {a} + sum of gaps {gaps} = {key}",
        wrong=wrong,
        correct=f"The gaps grow by {g}: the next gap is {gaps[n - 1]}.",
        generic="Write down the gaps, then the gaps between the gaps.",
        explain=f"The gaps are {', '.join(map(str, gaps[:n - 1]))}, rising by {g} each time. So the next gap is {gaps[n - 1]} and the next term is ${t[-1]} + {gaps[n - 1]} = {key}$.")

# Q6 alternating: x k then - c
for v, (a, k, c, n) in {1: (4, 2, 3, 6), 2: (3, 3, 4, 6), 3: (6, 2, 5, 7)}.items():
    t = [a]
    for i in range(n - 1): t.append(t[-1] * k if i % 2 == 0 else t[-1] - c)
    i = n - 1; key = t[-1] * k if i % 2 == 0 else t[-1] - c
    nxt_mul = (i % 2 == 0)
    # second computation: every other term (the ones after a subtraction) follows its own rule
    sub_terms = t[0::2]          # a, k a - c, ...: each is k x previous - c
    # a multiply comes next: the places after a multiply have gaps that double (k = 2), so key = t[-2] + 2 (t[-2] - t[-4])
    key2 = (t[-2] + 2 * (t[-2] - t[-4])) if nxt_mul else (k * sub_terms[-1] - c)
    if nxt_mul: assert k == 2
    if v == 1:
        wrong = [(t[-1] * k, f"You multiplied by {k} again. The steps take turns: $\\times {k}$, then $-{c}$."),
                 (t[-1] + (t[-1] - t[-2]), f"You repeated the last gap of {t[-1] - t[-2]}."),
                 (t[-1] - c + 1, f"You took away {c - 1}, not {c}.")]
    elif v == 2:
        wrong = [(t[-1] * k, f"You multiplied by {k} again. The steps take turns: $\\times {k}$, then $-{c}$."),
                 (t[-1] + (t[-1] - t[-2]), f"You repeated the last gap of {t[-1] - t[-2]}."),
                 (key + 1, f"You took away {c - 1}, not {c}.")]
    else:
        wrong = [(t[-1] - c, f"You took away {c} again. The steps take turns: $\\times {k}$, then $-{c}$."),
                 (t[-1] + t[-2], "You added the last two terms. The steps take turns."),
                 (key - 1, f"You were one out: $2 \\times {t[-1]} = {key}$.")]
    step = f"\\times {k}" if nxt_mul else f"- {c}"
    SEQ[v]["alternating"] = dict(terms=t, key=key, key2=key2, run=fit_alternating,
        twice=(f"{t[-1]} then {step} = {key}; " + (f"the places after a multiply have doubling gaps: {t[-2]} + 2 x {t[-2] - t[-4]} = {key2}" if nxt_mul else f"every other term is {k} x previous - {c}: {k} x {sub_terms[-1]} - {c} = {key2}")),
        wrong=wrong,
        correct=f"The steps take turns, $\\times {k}$ then $-{c}$. Next is ${step}$.",
        generic="Look at the steps one at a time: they are not all the same kind.",
        explain=f"The steps go $\\times {k}$, $-{c}$, $\\times {k}$, $-{c}$ in turn. The next step is ${step}$, so ${t[-1]} {step} = {key}$.")

# Q7 Fibonacci-like
for v, (a, b) in {1: (3, 4), 2: (1, 5), 3: (2, 7)}.items():
    t = [a, b]
    for _ in range(4): t.append(t[-1] + t[-2])
    key = t[-1] + t[-2]; gap = t[-1] - t[-2]
    SEQ[v]["fibonacci"] = dict(terms=t, key=key, key2=t[-2] + t[-2] + t[-3], run=fit_fibonacci,
        twice=f"{t[-2]} + {t[-1]} = {key}; also 2 x {t[-2]} + {t[-3]} = {key}",
        wrong=[(t[-1] + gap, f"You repeated the last gap of {gap}."),
               (2 * t[-1], "You doubled the last term. Add the two before instead."),
               (key + 1, "You were one out. Add the last two terms again.")],
        correct=f"Each term is the sum of the two before: ${t[-2]} + {t[-1]} = {key}$.",
        generic="Add two neighbours and compare with the term after them.",
        explain=f"Each term is the sum of the two before it. So the next is ${t[-2]} + {t[-1]} = {key}$. Check: the gaps are the earlier terms, so the next gap is {t[-2]}.")

# Q8 two arithmetic lists in turn
for v, (a, da, b, db) in {1: (1, 3, 20, -2), 2: (2, 5, 30, 2), 3: (40, -4, 3, 3)}.items():
    t = []
    for i in range(4): t += [a + da * i, b + db * i]
    t = t[:7]
    key = b + db * 3                     # the eighth term is an even place
    odd_next = t[-1] + da
    sgn = lambda d: f"{'+' if d > 0 else '−'}{abs(d)}"
    if v == 1:
        wrong = [(odd_next, f"You applied the odd-place rule, {sgn(da)}. The eighth term is an even place."),
                 (t[-1] + (t[-1] - t[-2]), f"You carried on the last step, {sgn(t[-1] - t[-2])}. The two lists take turns."),
                 (2 * t[-1], "You doubled the last term. The two lists take turns.")]
    elif v == 2:
        wrong = [(odd_next, f"You applied the odd-place rule, {sgn(da)}. The eighth term is an even place."),
                 (key + 1, f"You added 3 to {t[-2]}, not 2."),
                 (t[-1] + t[-2], "You added the last two terms. The two lists take turns.")]
    else:
        wrong = [(t[-1] - 4, "You applied the odd-place rule, −4. The eighth term is an even place."),
                 (key + 1, f"You added 4 to {t[-2]}, not 3."),
                 (2 * t[-1], "You doubled the last term. The two lists take turns.")]
    SEQ[v]["interleaved"] = dict(terms=t, key=key, key2=t[-2] + db, run=fit_interleaved,
        twice=f"even places {t[1::2]} step {db}: {t[-2]} {sgn(db)} = {key}; {b} + 3 x {db} = {key}",
        wrong=wrong,
        correct=f"Two lists take turns. The even places go {sgn(db)}, so ${t[-2]} {'+' if db > 0 else '-'} {abs(db)} = {key}$.",
        generic="Read every other term on its own.",
        explain=f"The odd places go {', '.join(map(str, t[0::2]))}, and the even places go {', '.join(map(str, t[1::2]))}. The eighth term is an even place, so it is ${t[-2]} {'+' if db > 0 else '-'} {abs(db)} = {key}$.")

# Q9 add the digit sum
for v, a in {1: 19, 2: 23, 3: 26}.items():
    t = [a]
    for _ in range(5): t.append(t[-1] + ds(t[-1]))
    key = t[-1] + ds(t[-1]); last = t[-1] - t[-2]
    digs = " + ".join(str(t[-1]))
    if v == 1:
        wrong = [(t[-1] + last, f"You repeated the last gap of {last}."),
                 (2 * t[-1], "You doubled the last term."),
                 (key + 1, "You were one out. Add the digits of the last term again.")]
    elif v == 2:
        wrong = [(t[-1] + last, f"You repeated the last gap of {last}."),
                 (2 * t[-1], "You doubled the last term."),
                 (key + 2, "You were two out. Add the digits of the last term again.")]
    else:
        wrong = [(t[-1] + last, f"You repeated the last gap of {last}."),
                 (2 * t[-1], "You doubled the last term."),
                 (t[-1] + int(str(t[-1])[-1]), f"You added only the units digit, {str(t[-1])[-1]}.")]
    SEQ[v]["digit-sum"] = dict(terms=t, key=key, key2=t[-1] + sum(int(c) for c in str(t[-1])), run=fit_digit_sum,
        twice=f"{t[-1]} + ({digs}) = {key}; whole chain {t} rebuilt from {a}",
        wrong=wrong,
        correct=f"Add the digit sum: ${t[-1]} + {ds(t[-1])} = {key}$.",
        generic="Compare each gap with the digits of the term before it.",
        explain=f"Each gap is the digit sum of the term before: ${t[0]} + {ds(t[0])} = {t[1]}$, and so on. The last term {t[-1]} has digit sum {ds(t[-1])}, so the next is {key}.")

# Q10 primes (p_n + n, or the primes themselves)
for v, (n0, s) in {1: (1, 1), 2: (9, 0), 3: (16, 0)}.items():
    t = [p(n0 + i) + s * (n0 + i) for i in range(6)]
    m = n0 + 6; key = p(m) + s * m; last = t[-1] - t[-2]
    if s == 1:
        nextprime = min(x for x in P if x > t[-1])
        wrong = [(t[-1] + last, f"You repeated the last gap of {last}."),
                 (nextprime, f"You took the next prime after {t[-1]}. The terms are primes plus their place."),
                 (2 * t[-1], "You doubled the last term.")]
        correct = f"The $n$th prime plus $n$: ${p(m)} + {m} = {key}$."
        explain = f"The terms are $2 + 1$, $3 + 2$, $5 + 3$, and so on: the $n$th prime plus $n$. The {m}th prime is {p(m)}, so the next is ${p(m)} + {m} = {key}$."
        twice = f"p_{m} + {m} = {p(m)} + {m} = {key}; gaps are prime gaps + 1: {t[-1]} + {p(m) - p(m - 1)} + 1 = {key}"
        key2 = t[-1] + (p(m) - p(m - 1)) + 1
        generic = "Subtract 1, 2, 3, ... from the terms and look again."
    else:
        wrong = [(t[-1] + last, f"You repeated the last gap of {last}, but {t[-1] + last} is not prime."),
                 (key + 1, "You were one out. The next prime is odd.") if v == 2 else
                 (t[-1] + 4, f"You added 4, but ${t[-1] + 4} = 7 \\times 11$."),
                 (2 * t[-1], "You doubled the last term. These are the primes in order.")]
        correct = f"These are the primes in order. The next prime after {t[-1]} is {key}."
        explain = f"Every term is prime and none is skipped. After {t[-1]}, the numbers {', '.join(str(x) for x in range(t[-1] + 1, key))} are not prime, so the next is {key}."
        twice = f"next prime after {t[-1]} is {key}; trial division of {key} by 2, 3, 5, 7 leaves remainders"
        key2 = next(x for x in range(t[-1] + 1, 10 ** 4) if all(x % d for d in range(2, int(x ** 0.5) + 1)))
        generic = "Each term is a number with a special property. Which numbers are missing?"
    SEQ[v]["primes"] = dict(terms=t, key=key, key2=key2, run=fit_primes, twice=twice, wrong=wrong,
                            correct=correct, generic=generic, explain=explain)

# Q11 cubes n^3 + c
for v, (n0, c) in {1: (2, -2), 2: (1, 3), 3: (3, 2)}.items():
    t = [(n0 + i) ** 3 + c for i in range(5)]; m = n0 + 5; key = m ** 3 + c
    last = t[-1] - t[-2]
    d = t; d1 = diffs(d); d2 = diffs(d1); d3 = diffs(d2)
    key2 = t[-1] + (d1[-1] + (d2[-1] + d3[-1]))     # difference table with the third difference 6
    cs = f"+ {c}" if c > 0 else f"- {abs(c)}"
    SEQ[v]["cubes"] = dict(terms=t, key=key, key2=key2, run=fit_cubes,
        twice=f"{m}^3 {cs} = {key}; difference table, third difference 6: {key2}",
        wrong=[(t[-1] + last, f"You repeated the last gap of {last}. The gaps grow faster each time."),
               (2 * t[-1], "You doubled the last term. Compare the terms with the cubes."),
               (m ** 3, f"You gave ${m}^3$ and dropped the {'+' if c > 0 else '−'}{abs(c)}.")],
        correct=f"Each term is a cube {'plus' if c > 0 else 'minus'} {abs(c)}: ${m}^3 {cs} = {key}$.",
        generic="Compare each term with 1, 8, 27, 64, 125, ...",
        explain=f"The terms are $n^3 {cs}$ for $n = {n0}$ to ${n0 + 4}$. So the next is ${m}^3 {cs} = {num(m ** 3)} {cs} = {key}$.")

# Q12 two geometric lists in turn
for v, (a, ka, b, kb) in {1: (1, 3, 10, 2), 2: (5, 2, 1, 3), 3: (3, 2, 1, 4)}.items():
    t = []
    for i in range(4): t += [a * ka ** i, b * kb ** i]
    t = t[:7]; key = b * kb ** 3
    if v == 1:
        wrong = [(t[-1] * ka, f"You applied the odd-place rule, $\\times {ka}$. The eighth term is an even place."),
                 (2 * t[-1], f"You doubled {t[-1]}, the odd-place term."),
                 (t[-1] + t[-2], "You added the last two terms.")]
    elif v == 2:
        wrong = [(t[-1] * ka, f"You applied the odd-place rule, $\\times {ka}$. The eighth term is an even place."),
                 (2 * t[-2], f"You doubled {t[-2]}. The even places go $\\times 3$."),
                 (t[-1] + t[-2], "You added the last two terms.")]
    else:
        wrong = [(t[-1] * ka, f"You applied the odd-place rule, $\\times {ka}$. The eighth term is an even place."),
                 (2 * t[-2], f"You doubled {t[-2]}. The even places go $\\times 4$."),
                 (t[-1] + t[-2], "You added the last two terms.")]
    SEQ[v]["interleaved-geometric"] = dict(terms=t, key=key, key2=b * kb ** 3, run=fit_interleaved_geo,
        twice=f"{t[-2]} x {kb} = {key}; {b} x {kb}^3 = {key}",
        wrong=wrong,
        correct=f"The even places go $\\times {kb}$, so ${t[-2]} \\times {kb} = {key}$.",
        generic="Read the odd places and the even places as two lists.",
        explain=f"The odd places go {', '.join(map(str, t[0::2]))} ($\\times {ka}$). The even places go {', '.join(map(str, t[1::2]))} ($\\times {kb}$). The eighth term is an even place: ${t[-2]} \\times {kb} = {key}$.")
# brief worked Q12: distractors 81, 54, 67
assert [w for w, _ in SEQ[1]["interleaved-geometric"]["wrong"]] == [81, 54, 67]

# Q13 consecutive products n(n+1)
for v, n0 in {1: 2, 2: 8, 3: 15}.items():
    t = [(n0 + i) * (n0 + i + 1) for i in range(5)]; m = n0 + 5; key = m * (m + 1)
    last = t[-1] - t[-2]
    sq = (m + 1) ** 2 if v != 3 else (m + 1) ** 2
    SEQ[v]["consecutive-products"] = dict(terms=t, key=key, key2=t[-1] + last + 2, run=fit_cons_products,
        twice=f"{m} x {m + 1} = {key}; gaps rise by 2: {t[-1]} + {last + 2} = {key}",
        wrong=[(t[-1] + last, f"You repeated the last gap of {last}. The gaps grow by 2."),
               (2 * t[-1], "You doubled the last term."),
               (sq, f"You squared {m + 1}. Each term is two neighbours multiplied.")],
        correct=f"Each term is $n(n + 1)$: ${m} \\times {m + 1} = {key}$.",
        generic="Write each term as a product of two whole numbers close together.",
        explain=f"The terms are ${n0} \\times {n0 + 1}$, ${n0 + 1} \\times {n0 + 2}$, and so on. So the next is ${m} \\times {m + 1} = {key}$. Check: the gaps rise by 2, so the next gap is {last + 2}.")

# Q14 rising multiplier a(n+1) = n a(n) + 1
for v, (a, m0) in {1: (1, 1), 2: (2, 1), 3: (1, 2)}.items():
    t = [a]
    for i in range(4): t.append((m0 + i) * t[-1] + 1)
    mk = m0 + 4; key = mk * t[-1] + 1; last = t[-1] - t[-2]
    chain = ", ".join(f"${m0 + i} \\times {num(t[i])} + 1 = {num(t[i + 1])}$" for i in range(4))
    if v == 1:
        wrong = [(mk * t[-1], f"You multiplied by {mk} and left out the + 1."),
                 ((mk - 1) * t[-1] + 1, f"You kept the multiplier at {mk - 1}. It rises by 1 each step."),
                 (t[-1] + last, f"You repeated the last gap of {last}.")]
    elif v == 2:
        wrong = [(mk * t[-1], f"You multiplied by {mk} and left out the + 1."),
                 ((mk + 1) * t[-1] + 1, f"You raised the multiplier by 2, to {mk + 1}."),
                 (t[-1] + last, f"You repeated the last gap of {last}.")]
    else:
        wrong = [(mk * t[-1], f"You multiplied by {mk} and left out the + 1."),
                 ((mk - 1) * t[-1] + 1, f"You kept the multiplier at {mk - 1}. It rises by 1 each step."),
                 (t[-1] + last, f"You repeated the last gap of {last}.")]
    # second computation: rebuild every shown term from the first, then step once more
    r = [a]
    for i in range(5): r.append((m0 + i) * r[-1] + 1)
    assert r[:5] == t
    SEQ[v]["rising-multiplier"] = dict(terms=t, key=key, key2=r[5], run=fit_rising,
        twice=f"{mk} x {t[-1]} + 1 = {key}; chain rebuilt from {a}: {r}",
        wrong=wrong,
        correct=f"Multiply by a number that rises by 1 each step, then add 1: ${mk} \\times {num(t[-1])} + 1 = {num(key)}$.",
        generic="Divide each term by the one before. What do the ratios do?",
        explain=f"The chain is {chain}. The multiplier rises by 1 each step, so the next is ${mk} \\times {num(t[-1])} + 1 = {num(key)}$.")
assert [w for w, _ in SEQ[1]["rising-multiplier"]["wrong"]][:2] == [325, 261]

# Q15 tribonacci
for v, (a, b, c) in {1: (1, 2, 3), 2: (2, 3, 4), 3: (3, 1, 5)}.items():
    t = [a, b, c]
    for _ in range(4): t.append(t[-1] + t[-2] + t[-3])
    key = t[-1] + t[-2] + t[-3]; last = t[-1] - t[-2]
    SEQ[v]["tribonacci"] = dict(terms=t, key=key, key2=2 * t[-1] - t[-4], run=fit_tribonacci,
        twice=f"{t[-3]} + {t[-2]} + {t[-1]} = {key}; also 2 x {t[-1]} - {t[-4]} = {key}",
        wrong=[(t[-1] + t[-2], "You added only the last two terms. Each term is the sum of three."),
               (t[-1] + last, f"You repeated the last gap of {last}."),
               (2 * t[-1], "You doubled the last term.")],
        correct=f"Each term is the sum of the three before: ${t[-3]} + {t[-2]} + {t[-1]} = {key}$.",
        generic="Try adding two terms, then three, and compare with the next.",
        explain=f"From the fourth term on, each is the sum of the three before it. So the next is ${t[-3]} + {t[-2]} + {t[-1]} = {key}$. Check: ${t[-1]} \\times 2 - {t[-4]} = {key}$ gives the same.")
```

### `probs.py`

```python
"""Paper B: probability at speed. Fifteen families in the brief's order; each key is a Fraction found in closed form
and again by enumeration, a linear solve or a series, with an assert that the two agree."""
from fractions import Fraction as F
from itertools import product, combinations, permutations
from math import comb
from common import fr, check_placement, choice_widget, item

D6 = range(1, 7)
def dice(n): return list(product(D6, repeat=n))
def prob(outcomes, pred):
    outs = list(outcomes); return F(sum(1 for o in outs if pred(o)), len(outs))
DECK = [(r, s) for s in "SHDC" for r in range(1, 14)]

def race(pa, pb):
    """P(pattern pa appears before pb) for a fair coin, by an exact linear solve over suffix states."""
    pref = {""} | {x[:i] for x in (pa, pb) for i in range(1, len(x))}
    def step(s, c):
        w = s + c
        if w.endswith(pa): return "A"
        if w.endswith(pb): return "B"
        for i in range(len(w)):
            if w[i:] in pref: return w[i:]
        return ""
    states = sorted(pref, key=len)
    idx = {s: i for i, s in enumerate(states)}
    n = len(states)
    M = [[F(0)] * n + [F(0)] for _ in range(n)]
    for s in states:
        i = idx[s]; M[i][i] += 1
        for c in "HT":
            t = step(s, c)
            if t == "A": M[i][n] += F(1, 2)
            elif t != "B": M[i][idx[t]] -= F(1, 2)
    for col in range(n):          # Gauss-Jordan over the rationals
        piv = next(r for r in range(col, n) if M[r][col] != 0)
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]; M[col] = [x / pv for x in M[col]]
        for r in range(n):
            if r != col and M[r][col] != 0:
                f = M[r][col]; M[r] = [a - f * b for a, b in zip(M[r], M[col])]
    return M[idx[""]][n]
def race_enum(pa, pb, L=12):
    """Share of the 2^L toss strings in which pa appears first (strings with neither count against): a lower bound."""
    win = 0
    for seq in product("HT", repeat=L):
        s = "".join(seq)
        ia = s.find(pa); ib = s.find(pb)
        ia = ia + len(pa) if ia >= 0 else 10 ** 9; ib = ib + len(pb) if ib >= 0 else 10 ** 9
        if ia < ib: win += 1
    return F(win, 2 ** L)

def best_ev(rolls_left, fee=0):
    """Best expected kept face with rolls_left rolls, by trying every keep set (an exhaustive policy search)."""
    if rolls_left == 1: return F(7, 2)
    nxt = best_ev(rolls_left - 1, fee) - fee
    best = None
    for mask in range(64):
        keep = [x for x in D6 if mask >> (x - 1) & 1]
        ev = sum((F(x) if x in keep else nxt) for x in D6) / 6
        best = ev if best is None or ev > best else best
    return best

FAM = ["dice-sum", "binomial", "at-least-one", "cards-conditional", "same-suit", "reroll-ev", "distinct-days",
       "first-success", "committee", "urn", "natural-frequency", "max-of-dice", "given-the-total", "first-to-six",
       "pattern-race"]
DIFF = dict(zip(FAM, [2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5]))
SKILL = {f: "mp-fractions" for f in FAM}
for f in ["cards-conditional", "natural-frequency", "given-the-total", "first-to-six", "pattern-race"]:
    SKILL[f] = "pz-conditioning"

B = {1: {}, 2: {}, 3: {}}
def add(v, fam, **kw): B[v][fam] = kw

# ---------- dice-sum ----------
for v, T in {1: 9, 2: 10, 3: 6}.items():
    n = 6 - abs(7 - T); key = F(n, 36)
    pairs = ", ".join(f"({a}, {T - a})" for a in D6 if 1 <= T - a <= 6)
    add(v, "dice-sum", title=f"A total of {T}", key=key, key2=prob(dice(2), lambda o: sum(o) == T),
        twice=f"{n} of 36 pairs; enumeration of 36",
        q=f"Two fair dice are rolled. What is the chance that the total is {T}?",
        wrong=[(F(1, 11), "You treated the 11 totals as equally likely. A middle total has more ways."),
               (1 - key, f"You found the chance that the total is not {T}."),
               (2 * key, f"You counted each pair twice. There are {n} ordered pairs, not {2 * n}.")],
        correct=f"{n} of the 36 ordered pairs make {T}.",
        generic="List the ordered pairs that make the total, out of 36.",
        explain=f"The pairs {pairs} make {T}. That is {n} of 36, so ${fr(key, False)}$.")

# ---------- binomial ----------
for v, (n, k) in {1: (5, 2), 2: (6, 2), 3: (5, 4)}.items():
    key = F(comb(n, k), 2 ** n)
    add(v, "binomial", title=f"Exactly {k} heads in {n}", key=key,
        key2=prob(product("HT", repeat=n), lambda o: o.count("H") == k),
        twice=f"C({n},{k})/2^{n}; enumeration of {2 ** n} sequences",
        q=f"A fair coin is tossed {n} times. What is the chance of exactly {k} heads?",
        wrong=[(F(1, 2 ** n), f"You counted one order only. There are $\\binom{{{n}}}{{{k}}} = {comb(n, k)}$ orders."),
               (F(k, n), f"You took {k} heads out of {n} tosses as the chance."),
               (1 - key, f"You found the chance of anything but exactly {k} heads.")],
        correct=f"$\\binom{{{n}}}{{{k}}} = {comb(n, k)}$ orders, each ${fr(F(1, 2 ** n), False)}$.",
        generic="Count the orders, then multiply by the chance of one order.",
        explain=f"There are $\\binom{{{n}}}{{{k}}} = {comb(n, k)}$ orders, each with chance ${fr(F(1, 2 ** n), False)}$. So the chance is ${fr(F(comb(n, k), 2 ** n), False)} = {fr(key, False)}$. Listing all {2 ** n} sequences finds the same {comb(n, k)}.")

# ---------- at-least-one ----------
add(1, "at-least-one", title="At least one six in three", key=1 - F(5, 6) ** 3,
    key2=prob(dice(3), lambda o: 6 in o), twice="1 - (5/6)^3; enumeration of 216",
    q="A fair die is rolled three times. What is the chance of at least one six?",
    wrong=[(F(1, 2), "You added $\\tfrac16$ three times. That counts two sixes twice."),
           (F(125, 216), "You found the chance of no six at all."),
           (F(1, 216), "You found the chance that every roll is a six.")],
    correct="One minus the chance of no six: $1 - \\tfrac{125}{216}$.",
    generic="Find the chance of no six first.",
    explain="No six has chance $(\\tfrac56)^3 = \\tfrac{125}{216}$. So at least one six is $\\tfrac{91}{216}$. Listing the 216 outcomes gives 91 with a six.")
add(2, "at-least-one", title="At least one six in two", key=1 - F(5, 6) ** 2,
    key2=prob(dice(2), lambda o: 6 in o), twice="1 - (5/6)^2; enumeration of 36",
    q="A fair die is rolled twice. What is the chance of at least one six?",
    wrong=[(F(1, 3), "You added $\\tfrac16$ twice. That counts the double six twice."),
           (F(25, 36), "You found the chance of no six at all."),
           (F(1, 36), "You found the chance that both rolls are sixes.")],
    correct="One minus the chance of no six: $1 - \\tfrac{25}{36}$.",
    generic="Find the chance of no six first.",
    explain="No six has chance $(\\tfrac56)^2 = \\tfrac{25}{36}$. So at least one six is $\\tfrac{11}{36}$. Listing the 36 pairs gives 11 with a six.")
add(3, "at-least-one", title="At least one heart in three", key=1 - F(3, 4) ** 3,
    key2=prob(product(DECK, repeat=3), lambda o: any(c[1] == "H" for c in o)), twice="1 - (3/4)^3; enumeration of 52^3 draws",
    q="A card is drawn from a full deck and put back, three times. What is the chance of at least one heart?",
    wrong=[(F(3, 4), "You added $\\tfrac14$ three times. That counts two hearts twice."),
           (F(27, 64), "You found the chance of no heart at all."),
           (F(1, 64), "You found the chance that every card is a heart.")],
    correct="One minus the chance of no heart: $1 - \\tfrac{27}{64}$.",
    generic="Find the chance of no heart first.",
    explain="No heart has chance $(\\tfrac34)^3 = \\tfrac{27}{64}$. So at least one heart is $\\tfrac{37}{64}$. Counting all $52^3$ draws gives the same share.")

# ---------- cards-conditional ----------
def ordered2(pred_first, pred_second):
    pairs = list(permutations(DECK, 2))
    a = [p for p in pairs if pred_first(p[0])]
    return F(sum(1 for p in a if pred_second(p[1])), len(a))
red = lambda c: c[1] in "HD"
add(1, "cards-conditional", title="Red after red", key=F(25, 51), key2=ordered2(red, red),
    twice="25 reds left of 51; enumeration of 52 x 51 ordered pairs",
    q="Two cards are dealt from a full deck. The first is red. What is the chance that the second is red?",
    wrong=[(F(1, 2), "You put the first card back. With it gone, 25 of the 51 left are red."),
           (F(25, 102), "You found the chance that both are red, not the second given the first."),
           (F(26, 51), "You took the card away but still counted 26 reds.")],
    correct="25 reds are left among 51 cards.",
    generic="Take the first card out, then count what is left.",
    explain="After a red card, 25 of the 51 cards left are red, so $\\tfrac{25}{51}$. Check: both red is $\\tfrac{26}{52} \\cdot \\tfrac{25}{51}$, and dividing by $\\tfrac12$ gives $\\tfrac{25}{51}$.")
ace = lambda c: c[0] == 1
add(2, "cards-conditional", title="Ace after ace", key=F(3, 51), key2=ordered2(ace, ace),
    twice="3 aces left of 51; enumeration of 52 x 51 ordered pairs",
    q="Two cards are dealt from a full deck. The first is an ace. What is the chance that the second is an ace?",
    wrong=[(F(1, 13), "You put the first card back. With it gone, 3 of the 51 left are aces."),
           (F(1, 221), "You found the chance that both are aces, not the second given the first."),
           (F(4, 51), "You took the card away but still counted 4 aces.")],
    correct="3 aces are left among 51 cards: $\\tfrac{3}{51} = \\tfrac{1}{17}$.",
    generic="Take the first card out, then count what is left.",
    explain="After an ace, 3 of the 51 cards left are aces, so $\\tfrac{3}{51} = \\tfrac{1}{17}$. Check: both aces is $\\tfrac{1}{221}$, and dividing by $\\tfrac{1}{13}$ gives $\\tfrac{1}{17}$.")
add(3, "cards-conditional", title="A heart after a spade", key=F(13, 51),
    key2=ordered2(lambda c: c[1] == "S", lambda c: c[1] == "H"),
    twice="13 hearts left of 51; enumeration of 52 x 51 ordered pairs",
    q="Two cards are dealt from a full deck. The first is a spade. What is the chance that the second is a heart?",
    wrong=[(F(1, 4), "You put the first card back. With a spade gone, 13 of 51 are hearts."),
           (F(13, 204), "You found the chance of a spade then a heart, not the second given the first."),
           (F(4, 17), "You took a heart out, but the card gone was a spade.")],
    correct="All 13 hearts are left among 51 cards.",
    generic="Take the first card out, then count the hearts left.",
    explain="A spade has gone, so all 13 hearts remain among 51 cards: $\\tfrac{13}{51}$. Check: spade then heart is $\\tfrac{13}{52} \\cdot \\tfrac{13}{51} = \\tfrac{13}{204}$, and dividing by $\\tfrac14$ gives $\\tfrac{13}{51}$.")

# ---------- same-suit ----------
def same_suit(deck, k):
    hands = list(combinations(deck, k))
    return F(sum(1 for h in hands if len({c[1] for c in h}) == 1), len(hands))
add(1, "same-suit", title="Three of one suit", key=F(12, 51) * F(11, 50), key2=same_suit(DECK, 3),
    twice="12/51 x 11/50; 4 C(13,3) of C(52,3) hands = 1144/22100",
    q="Three cards are dealt from a full deck. What is the chance that all three share a suit?",
    wrong=[(F(1, 16), "You dealt with replacement, so each later card matched with chance $\\tfrac14$."),
           (F(11, 850), "You found the chance of three hearts, one named suit."),
           (F(1, 64), "You named one suit and dealt with replacement.")],
    correct="The first card sets the suit, then $\\tfrac{12}{51} \\cdot \\tfrac{11}{50}$.",
    generic="Let the first card choose the suit. Then the others must match it.",
    explain="The first card sets the suit; then $\\tfrac{12}{51} \\cdot \\tfrac{11}{50} = \\tfrac{22}{425}$. Counting hands: $4\\binom{13}{3} = 1144$ of $\\binom{52}{3} = 22100$ agree.")
SMALL = [(r, s) for s in "SHDC" for r in range(1, 6)]
add(2, "same-suit", title="One suit, small deck", key=F(4, 19), key2=same_suit(SMALL, 2),
    twice="4/19 of the 19 cards left; 4 C(5,2) of C(20,2) = 40/190",
    q="A deck has 20 cards: 5 in each of 4 suits. Two cards are dealt. What is the chance they share a suit?",
    wrong=[(F(1, 4), "You dealt with replacement. With one card gone, only 4 of 19 match."),
           (F(1, 19), "You found the chance of two of one named suit."),
           (F(1, 16), "You named one suit and dealt with replacement.")],
    correct="The first card sets the suit; 4 of the 19 left match it.",
    generic="Let the first card choose the suit, then count the matches left.",
    explain="The first card sets the suit, and 4 of the 19 cards left match it: $\\tfrac{4}{19}$. Counting pairs: $4\\binom52 = 40$ of $\\binom{20}{2} = 190$ agree.")
NOH = [c for c in DECK if c[1] != "H"]
add(3, "same-suit", title="One suit, no hearts", key=F(12, 38), key2=same_suit(NOH, 2),
    twice="12/38; 3 C(13,2) of C(39,2) = 234/741",
    q="The hearts are taken out of a deck, leaving 39 cards. Two cards are dealt. What is the chance they share a suit?",
    wrong=[(F(1, 3), "You dealt with replacement. With one card gone, 12 of 38 match."),
           (F(2, 19), "You found the chance of two of one named suit."),
           (F(1, 9), "You named one suit and dealt with replacement.")],
    correct="The first card sets the suit; 12 of the 38 left match it.",
    generic="Let the first card choose the suit, then count the matches left.",
    explain="The first card sets the suit, and 12 of the 38 cards left match it: $\\tfrac{12}{38} = \\tfrac{6}{19}$. Counting pairs: $3\\binom{13}{2} = 234$ of $\\binom{39}{2} = 741$ agree.")

# ---------- reroll-ev ----------
assert prob(dice(2), lambda o: True) == 1 and sum(F(max(o), 36) for o in dice(2)) == F(161, 36)
add(1, "reroll-ev", title="One reroll", key=F(4 + 5 + 6, 6) + F(3, 6) * F(7, 2), key2=best_ev(2),
    twice="keep 4 to 6: 15/6 + (1/2)(7/2); search over all 64 keep sets",
    q="You roll a fair die. You may roll once more, and then must keep the second face. Playing well, what is the expected face you keep?",
    wrong=[(F(7, 2), "You ignored the reroll. That is the average of one roll."),
           (F(161, 36), "You kept the better of two rolls. Once you reroll, you must keep the new face."),
           (F(25, 6), "You kept a 3 as well. A 3 is below the reroll's average of 3.5.")],
    correct="Keep 4, 5 or 6; reroll the rest for an average of 3.5.",
    generic="Keep a face only if it beats the average of a fresh roll.",
    explain="Keep 4, 5 or 6, and reroll 1, 2 or 3 for 3.5 on average. So $\\tfrac{4 + 5 + 6}{6} + \\tfrac12 \\cdot \\tfrac72 = \\tfrac{17}{4}$. Trying every keep rule gives the same best.")
add(2, "reroll-ev", title="Two rerolls", key=F(5 + 6, 6) + F(4, 6) * F(17, 4), key2=best_ev(3),
    twice="keep 5 or 6: 11/6 + (2/3)(17/4); search over all keep sets at each stage",
    q="You roll a fair die. You may reroll up to twice, keeping the last face you roll. Playing well, what is the expected face you keep?",
    wrong=[(F(17, 4), "You allowed only one reroll. With two left, a 4 is worth rerolling."),
           (F(7, 2), "You ignored the rerolls. That is the average of one roll."),
           (F(11, 2), "You averaged only the faces you keep, 5 and 6.")],
    correct="With two rerolls left, keep only 5 or 6, against $\\tfrac{17}{4}$.",
    generic="Work back from the last roll: what is one reroll worth?",
    explain="One reroll is worth $\\tfrac{17}{4}$, so on the first roll keep only 5 or 6. Then $\\tfrac{5 + 6}{6} + \\tfrac46 \\cdot \\tfrac{17}{4} = \\tfrac{14}{3}$. Trying every keep rule at each stage gives the same.")
add(3, "reroll-ev", title="A paid reroll", key=F(3 + 4 + 5 + 6, 6) + F(2, 6) * (F(7, 2) - 1), key2=best_ev(2, fee=1),
    twice="keep 3 to 6: 18/6 + (1/3)(5/2); search over all keep sets with the fee",
    q="You roll a fair die and win its face in pounds. You may pay £1 to reroll once, then keep the new face. Playing well, what is your expected profit in pounds?",
    wrong=[(F(7, 2), "You never rerolled. A 1 or a 2 is worth rerolling, even for £1."),
           (F(17, 4), "You forgot the £1 fee. It makes a 3 worth keeping."),
           (F(9, 2), "You averaged only the faces you keep, 3 to 6.")],
    correct="A reroll is worth £3.50 less £1. Keep 3 or more.",
    generic="A reroll is worth its average less the fee. Keep anything above that.",
    explain="A reroll is worth $3.5 - 1 = 2.5$, so keep 3 to 6. Then $\\tfrac{3 + 4 + 5 + 6}{6} + \\tfrac26 \\cdot \\tfrac52 = \\tfrac{23}{6}$. Trying every keep rule gives the same best.")

# ---------- distinct-days ----------
add(1, "distinct-days", title="Three days of the week", key=F(6, 7) * F(5, 7),
    key2=prob(product(range(7), repeat=3), lambda o: len(set(o)) == 3), twice="1 x 6/7 x 5/7; 210 of 343 triples",
    q="Three people are each born on a random day of the week. What is the chance that all three days differ?",
    wrong=[(F(19, 49), "You found the chance that two or more share a day."),
           (F(4, 7), "You took off $\\tfrac17$ for each of three pairs. The pairs overlap, so that is not exact."),
           (F(5, 7), "You used only the third person's chance.")],
    correct="$1 \\cdot \\tfrac67 \\cdot \\tfrac57$: each new person avoids the days taken.",
    generic="Seat the people one at a time. Each must avoid the days already used.",
    explain="The second avoids one day and the third avoids two: $\\tfrac67 \\cdot \\tfrac57 = \\tfrac{30}{49}$. Counting: $7 \\cdot 6 \\cdot 5 = 210$ of $7^3 = 343$ triples.")
add(2, "distinct-days", title="Four different faces", key=F(5, 6) * F(4, 6) * F(3, 6),
    key2=prob(dice(4), lambda o: len(set(o)) == 4), twice="1 x 5/6 x 4/6 x 3/6; 360 of 1296",
    q="Four fair dice are rolled. What is the chance that all four faces differ?",
    wrong=[(F(13, 18), "You found the chance that two or more faces match."),
           (F(5, 54), "You multiplied in a fourth factor, $\\tfrac26$. The first die is free."),
           (F(5, 432), "You counted sets of faces, one order only. Each set has 24 orders.")],
    correct="$1 \\cdot \\tfrac56 \\cdot \\tfrac46 \\cdot \\tfrac36 = \\tfrac{5}{18}$.",
    generic="Roll the dice one at a time. Each must avoid the faces already shown.",
    explain="The dice must avoid 0, 1, 2 and 3 faces in turn: $\\tfrac56 \\cdot \\tfrac46 \\cdot \\tfrac36 = \\tfrac{5}{18}$. Counting: $6 \\cdot 5 \\cdot 4 \\cdot 3 = 360$ of 1296.")
add(3, "distinct-days", title="Four birth months", key=F(11, 12) * F(10, 12) * F(9, 12),
    key2=prob(product(range(12), repeat=4), lambda o: len(set(o)) == 4), twice="11/12 x 10/12 x 9/12; 11880 of 20736",
    q="Four people each have a birth month, all 12 equally likely. What is the chance that all four months differ?",
    wrong=[(F(41, 96), "You found the chance that two or more share a month."),
           (F(1, 2), "You took off $\\tfrac{1}{12}$ for each of six pairs. The pairs overlap, so that is not exact."),
           (F(55, 144), "You multiplied in a fourth factor, $\\tfrac{8}{12}$. The first person is free.")],
    correct="$\\tfrac{11}{12} \\cdot \\tfrac{10}{12} \\cdot \\tfrac{9}{12} = \\tfrac{55}{96}$.",
    generic="Add the people one at a time. Each must avoid the months already used.",
    explain="The others avoid 1, 2 and 3 months in turn: $\\tfrac{11}{12} \\cdot \\tfrac{10}{12} \\cdot \\tfrac{9}{12} = \\tfrac{55}{96}$. Counting: $12 \\cdot 11 \\cdot 10 \\cdot 9 = 11880$ of $12^4 = 20736$.")

# ---------- first-success ----------
def first_on(p, k, kinds):
    """Enumerate k trials over equally likely kinds, success = kind 0 with share p."""
    outs = list(product(range(kinds), repeat=k))
    succ = lambda x: x < p * kinds
    return F(sum(1 for o in outs if all(not succ(x) for x in o[:-1]) and succ(o[-1])), len(outs))
add(1, "first-success", title="First six on the third", key=F(5, 6) ** 2 * F(1, 6), key2=first_on(F(1, 6), 3, 6),
    twice="(5/6)^2 (1/6); enumeration of 216",
    q="A fair die is rolled until the first six. What is the chance that the first six comes on the third roll?",
    wrong=[(F(1, 6), "You used only the third roll. The first two must miss as well."),
           (F(1, 216), "You made every roll a six."),
           (F(91, 216), "You found at least one six in three rolls.")],
    correct="Two misses then a six: $(\\tfrac56)^2 \\cdot \\tfrac16$.",
    generic="Write the rolls in order: what must the first two do?",
    explain="The first two rolls miss and the third hits: $\\tfrac56 \\cdot \\tfrac56 \\cdot \\tfrac16 = \\tfrac{25}{216}$. Listing 216 outcomes gives 25 of that shape.")
add(2, "first-success", title="First hit on the third", key=F(3, 4) ** 2 * F(1, 4), key2=first_on(F(1, 4), 3, 4),
    twice="(3/4)^2 (1/4); enumeration of 4^3",
    q="A signal is right on a quarter of days, independently. What is the chance its first right day is the third?",
    wrong=[(F(1, 4), "You used only the third day. The first two must be wrong as well."),
           (F(1, 64), "You made every day right."),
           (F(37, 64), "You found at least one right day in three.")],
    correct="Two misses then a hit: $(\\tfrac34)^2 \\cdot \\tfrac14$.",
    generic="Write the days in order: what must the first two do?",
    explain="Days one and two miss and day three hits: $\\tfrac34 \\cdot \\tfrac34 \\cdot \\tfrac14 = \\tfrac{9}{64}$. Listing the 64 equally likely patterns gives 9 of that shape.")
add(3, "first-success", title="First ace on the second", key=F(12, 13) * F(1, 13), key2=first_on(F(1, 13), 2, 13),
    twice="(12/13)(1/13); enumeration of 13^2 ranks",
    q="Cards are drawn with replacement until the first ace. What is the chance that the first ace is the second card?",
    wrong=[(F(1, 13), "You used only the second card. The first must miss as well."),
           (F(1, 169), "You made both cards aces."),
           (F(25, 169), "You found at least one ace in two cards.")],
    correct="A miss then an ace: $\\tfrac{12}{13} \\cdot \\tfrac{1}{13}$.",
    generic="Write the draws in order: what must the first one do?",
    explain="The first card misses and the second is an ace: $\\tfrac{12}{13} \\cdot \\tfrac{1}{13} = \\tfrac{12}{169}$. Listing the 169 rank pairs gives 12 of that shape.")

# ---------- committee ----------
def committee(a, b, k, j):
    people = ["a"] * a + ["b"] * b
    teams = list(combinations(range(a + b), k))
    return F(sum(1 for t in teams if sum(people[i] == "b" for i in t) == j), len(teams))
add(1, "committee", title="Two quants of three", key=F(comb(4, 2) * comb(5, 1), comb(9, 3)), key2=committee(5, 4, 3, 2),
    twice="C(4,2) C(5,1) / C(9,3) = 30/84; enumeration of 84 teams",
    q="A desk of 5 traders and 4 quants picks a team of 3 at random. What is the chance of exactly 2 quants?",
    wrong=[(F(5, 42), "You counted one order only, quant, quant, trader. There are 3 orders."),
           (F(80, 243), "You picked with replacement, as if one person could be chosen twice."),
           (F(9, 14), "You found the chance of anything but exactly 2 quants.")],
    correct="$\\binom42 \\binom51 = 30$ teams of $\\binom93 = 84$.",
    generic="Count the teams that fit, then divide by all teams.",
    explain="Choose 2 of 4 quants and 1 of 5 traders: $6 \\cdot 5 = 30$ of $\\binom93 = 84$ teams, so $\\tfrac{5}{14}$. Listing all 84 teams finds the same 30.")
add(2, "committee", title="Two quants of three", key=F(comb(4, 2) * comb(6, 1), comb(10, 3)), key2=committee(6, 4, 3, 2),
    twice="C(4,2) C(6,1) / C(10,3) = 36/120; enumeration of 120 teams",
    q="A desk of 6 traders and 4 quants picks a team of 3 at random. What is the chance of exactly 2 quants?",
    wrong=[(F(1, 10), "You counted one order only, quant, quant, trader. There are 3 orders."),
           (F(36, 125), "You picked with replacement, as if one person could be chosen twice."),
           (F(7, 10), "You found the chance of anything but exactly 2 quants.")],
    correct="$\\binom42 \\binom61 = 36$ teams of $\\binom{10}{3} = 120$.",
    generic="Count the teams that fit, then divide by all teams.",
    explain="Choose 2 of 4 quants and 1 of 6 traders: $6 \\cdot 6 = 36$ of $\\binom{10}{3} = 120$ teams, so $\\tfrac{3}{10}$. Listing all 120 teams finds the same 36.")
add(3, "committee", title="One bank of two", key=F(comb(3, 1) * comb(5, 1), comb(8, 2)), key2=committee(5, 3, 2, 1),
    twice="3 x 5 / C(8,2) = 15/28; enumeration of 28 pairs",
    q="A fund picks 2 of 8 stocks at random: 5 tech and 3 banks. What is the chance of exactly 1 bank?",
    wrong=[(F(15, 56), "You counted one order only, bank then tech. There are 2 orders."),
           (F(15, 32), "You picked with replacement, as if one stock could be chosen twice."),
           (F(13, 28), "You found the chance of two of a kind.")],
    correct="$3 \\cdot 5 = 15$ pairs of $\\binom82 = 28$.",
    generic="Count the pairs that fit, then divide by all pairs.",
    explain="Choose 1 of 3 banks and 1 of 5 tech stocks: 15 of $\\binom82 = 28$ pairs, so $\\tfrac{15}{28}$. Listing all 28 pairs finds the same 15.")

# ---------- urn ----------
def urn(r, b, k, pred):
    balls = ["r"] * r + ["b"] * b
    draws = list(permutations(range(r + b), k))
    return F(sum(1 for d in draws if pred([balls[i] for i in d])), len(draws))
add(1, "urn", title="One of each colour", key=2 * F(3, 5) * F(2, 4), key2=urn(3, 2, 2, lambda x: sorted(x) == ["b", "r"]),
    twice="2 x 3/5 x 2/4; enumeration of 20 ordered draws",
    q="An urn holds 3 red and 2 blue balls. You draw 2 without replacement. What is the chance of one of each colour?",
    wrong=[(F(12, 25), "You drew with replacement. The second draw has one ball fewer."),
           (F(3, 10), "You counted one order only, red then blue."),
           (F(2, 5), "You found the chance of two of one colour.")],
    correct="Red then blue or blue then red: $2 \\cdot \\tfrac35 \\cdot \\tfrac24$.",
    generic="Add the two orders, each without replacement.",
    explain="Red then blue is $\\tfrac35 \\cdot \\tfrac24 = \\tfrac{3}{10}$, and blue then red is the same. So the chance is $\\tfrac35$. Counting: $\\binom31\\binom21 = 6$ of $\\binom52 = 10$ pairs.")
add(2, "urn", title="Both red", key=F(4, 6) * F(3, 5), key2=urn(4, 2, 2, lambda x: x == ["r", "r"]),
    twice="4/6 x 3/5; enumeration of 30 ordered draws",
    q="An urn holds 4 red and 2 blue balls. You draw 2 without replacement. What is the chance both are red?",
    wrong=[(F(4, 9), "You drew with replacement. After a red, 3 of 5 are red."),
           (F(3, 5), "You found the chance that at least one is blue."),
           (F(2, 3), "You used only the first draw.")],
    correct="$\\tfrac46 \\cdot \\tfrac35 = \\tfrac25$.",
    generic="Multiply the chances, removing the first ball.",
    explain="The first is red with chance $\\tfrac46$, then the second with $\\tfrac35$. So $\\tfrac{12}{30} = \\tfrac25$. Counting: $\\binom42 = 6$ of $\\binom62 = 15$ pairs.")
add(3, "urn", title="Three red", key=F(4, 8) * F(3, 7) * F(2, 6), key2=urn(4, 4, 3, lambda x: x == ["r"] * 3),
    twice="4/8 x 3/7 x 2/6; enumeration of 336 ordered draws",
    q="An urn holds 4 red and 4 blue balls. You draw 3 without replacement. What is the chance all three are red?",
    wrong=[(F(1, 8), "You drew with replacement. Each red drawn leaves fewer reds."),
           (F(13, 14), "You found the chance that at least one is blue."),
           (F(1, 7), "You found three of one colour, either colour.")],
    correct="$\\tfrac48 \\cdot \\tfrac37 \\cdot \\tfrac26 = \\tfrac{1}{14}$.",
    generic="Multiply the chances, removing each red as it is drawn.",
    explain="The chances are $\\tfrac48$, then $\\tfrac37$, then $\\tfrac26$, which multiply to $\\tfrac{1}{14}$. Counting: $\\binom43 = 4$ of $\\binom83 = 56$ sets.")

# ---------- natural-frequency ----------
def bayes(base, hit, false):
    return base * hit / (base * hit + (1 - base) * false)
def counts(N, base, hit, false):
    pos = N * base; tp = pos * hit; fp = (N - pos) * false
    assert all(F(x).denominator == 1 for x in (pos, tp, fp))
    return F(tp, tp + fp), (int(pos), int(tp), int(fp))
k1, c1 = counts(1000, F(5, 100), F(9, 10), F(1, 10))
add(1, "natural-frequency", title="Flagged traders", key=bayes(F(5, 100), F(9, 10), F(1, 10)), key2=k1,
    twice=f"Bayes 0.05x0.9 / (0.05x0.9 + 0.95x0.1); per 1,000: {c1}",
    q="5% of traders have an edge. A screen flags 90% of those, and 10% of the rest. A trader is flagged. What is the chance they have an edge?",
    wrong=[(F(9, 10), "You gave the hit rate: the chance of a flag given an edge."),
           (F(9, 200), "You divided the true flags by everyone, not by everyone flagged."),
           (F(1, 20), "You gave the base rate and ignored the flag.")],
    correct="Of 1,000 traders, 45 true flags and 95 false: $\\tfrac{45}{140}$.",
    generic="Picture 1,000 traders. How many are flagged, and how many of those have an edge?",
    explain="In 1,000 traders, 50 have an edge and 45 are flagged; 950 do not and 95 are flagged. So $\\tfrac{45}{140} = \\tfrac{9}{28}$. Bayes' rule gives $\\tfrac{0.045}{0.045 + 0.095}$, the same.")
k2, c2 = counts(100, F(20, 100), F(3, 4), F(1, 4))
add(2, "natural-frequency", title="Stocks that pass", key=bayes(F(1, 5), F(3, 4), F(1, 4)), key2=k2,
    twice=f"Bayes 0.2x0.75 / (0.2x0.75 + 0.8x0.25); per 100: {c2}",
    q="20% of stocks beat the market. A screen passes 75% of those, and 25% of the rest. A stock passes. What is the chance it beats the market?",
    wrong=[(F(3, 4), "You gave the hit rate: the chance of passing given a winner."),
           (F(3, 20), "You divided the true passes by every stock, not by every pass."),
           (F(1, 5), "You gave the base rate and ignored the screen.")],
    correct="Of 100 stocks, 15 true passes and 20 false: $\\tfrac{15}{35}$.",
    generic="Picture 100 stocks. How many pass, and how many of those are winners?",
    explain="In 100 stocks, 20 are winners and 15 pass; 80 are not and 20 pass. So $\\tfrac{15}{35} = \\tfrac37$. Bayes' rule gives $\\tfrac{0.15}{0.15 + 0.2}$, the same.")
k3, c3 = counts(10000, F(2, 100), F(9, 10), F(4, 100))
add(3, "natural-frequency", title="Flagged orders", key=bayes(F(2, 100), F(9, 10), F(4, 100)), key2=k3,
    twice=f"Bayes 0.02x0.9 / (0.02x0.9 + 0.98x0.04); per 10,000: {c3}",
    q="2% of orders are spoofs. A filter flags 90% of spoofs, and 4% of other orders. An order is flagged. What is the chance it is a spoof?",
    wrong=[(F(9, 10), "You gave the hit rate: the chance of a flag given a spoof."),
           (F(9, 500), "You divided the true flags by every order, not by every flag."),
           (F(1, 50), "You gave the base rate and ignored the flag.")],
    correct="Of 10,000 orders, 180 true flags and 392 false: $\\tfrac{180}{572}$.",
    generic="Picture 10,000 orders. How many are flagged, and how many of those are spoofs?",
    explain="In 10,000 orders, 200 are spoofs and 180 are flagged; 9,800 are not and 392 are flagged. So $\\tfrac{180}{572} = \\tfrac{45}{143}$. Bayes' rule gives $\\tfrac{0.018}{0.018 + 0.0392}$, the same.")

# ---------- max-of-dice ----------
add(1, "max-of-dice", title="The larger face is 4", key=F(4 ** 2 - 3 ** 2, 36), key2=prob(dice(2), lambda o: max(o) == 4),
    twice="(16 - 9)/36; enumeration of 36",
    q="Two fair dice are rolled. What is the chance that the larger face is 4? (A double 4 counts.)",
    wrong=[(F(4, 9), "You found the chance that both are at most 4. Take away both at most 3."),
           (F(1, 6), "You treated the six values of the larger face as equally likely."),
           (F(1, 9), "You counted unordered pairs, so (1, 4) and (4, 1) became one.")],
    correct="Both at most 4, less both at most 3: $\\tfrac{16 - 9}{36}$.",
    generic="Find the chance that both are at most 4, then take away both at most 3.",
    explain="Both at most 4 has 16 pairs; both at most 3 has 9. So the larger is exactly 4 in 7 pairs: $\\tfrac{7}{36}$. Listing the 36 pairs finds the same 7.")
add(2, "max-of-dice", title="The highest face is 3", key=F(3 ** 3 - 2 ** 3, 216), key2=prob(dice(3), lambda o: max(o) == 3),
    twice="(27 - 8)/216; enumeration of 216",
    q="Three fair dice are rolled. What is the chance that the highest face is 3?",
    wrong=[(F(1, 8), "You found the chance that all are at most 3. Take away all at most 2."),
           (F(1, 6), "You treated the six values of the highest face as equally likely."),
           (F(1, 216), "You made every die show 3.")],
    correct="All at most 3, less all at most 2: $\\tfrac{27 - 8}{216}$.",
    generic="Find the chance that all are at most 3, then take away all at most 2.",
    explain="All at most 3 has 27 outcomes; all at most 2 has 8. So the highest is exactly 3 in 19: $\\tfrac{19}{216}$. Listing the 216 outcomes finds the same 19.")
add(3, "max-of-dice", title="The larger face is 5", key=F(5 ** 2 - 4 ** 2, 36), key2=prob(dice(2), lambda o: max(o) == 5),
    twice="(25 - 16)/36; enumeration of 36",
    q="Two fair dice are rolled. What is the chance that the larger face is 5? (A double 5 counts.)",
    wrong=[(F(25, 36), "You found the chance that both are at most 5. Take away both at most 4."),
           (F(1, 6), "You treated the six values of the larger face as equally likely."),
           (F(5, 36), "You counted unordered pairs, so (1, 5) and (5, 1) became one.")],
    correct="Both at most 5, less both at most 4: $\\tfrac{25 - 16}{36}$.",
    generic="Find the chance that both are at most 5, then take away both at most 4.",
    explain="Both at most 5 has 25 pairs; both at most 4 has 16. So the larger is exactly 5 in 9 pairs: $\\tfrac{9}{36} = \\tfrac14$. Listing the 36 pairs finds the same 9.")

# ---------- given-the-total ----------
def given_total(T, face):
    a = [o for o in dice(2) if sum(o) == T]
    return F(sum(1 for o in a if face in o), len(a)), a
for v, (T, face) in {1: (8, 6), 2: (6, 3), 3: (10, 5)}.items():
    key2, pairs = given_total(T, face)
    n = len(pairs); h = sum(1 for o in pairs if face in o)
    unordered = sorted({tuple(sorted(o)) for o in pairs}); hu = sum(1 for o in unordered if face in o)
    key = F(h, n)
    plist = ", ".join(f"({a}, {b})" for a, b in pairs)
    add(v, "given-the-total", title=f"A {face}, given {T}", key=key, key2=key2,
        twice=f"{h} of the {n} pairs; enumeration of 36 then restrict",
        q=f"Two fair dice are rolled and the total is {T}. What is the chance that at least one die shows {face}?",
        wrong=[(F(11, 36), f"You ignored the total. That is the chance of a {face} on any roll."),
               (F(hu, len(unordered)), "You listed unordered pairs as equally likely. Ordered pairs are."),
               (F(h, 36), f"You did not condition. That is the chance of the total and a {face} together.")],
        correct=f"{h} of the {n} ordered pairs that make {T} show a {face}.",
        generic=f"List the ordered pairs that make {T}. Count those with a {face}.",
        explain=f"The total {T} comes from {plist}. {'Two' if h == 2 else 'One'} of those {n} {'show' if h == 2 else 'shows'} a {face}, so ${fr(key, False)}$.")
assert B[1]["given-the-total"]["key"] == F(2, 5)

# ---------- first-to-six ----------
def turn_game(p, players, me):
    q = 1 - p
    closed = q ** me * p / (1 - q ** players)
    partial = sum(q ** (me + players * k) * p for k in range(60))
    tail = q ** (me + players * 60) * p / (1 - q ** players)
    assert partial + tail == closed          # the series, with its exact tail
    return closed, partial
key, part = turn_game(F(1, 6), 2, 0)
add(1, "first-to-six", title="First six wins", key=key, key2=part + F(1, 6) * F(25, 36) ** 60 / (1 - F(25, 36)),
    twice="(1/6)/(1 - 25/36); series (1/6) sum (25/36)^k, 60 terms plus exact tail",
    q="You and a friend take turns to roll a die, you first. The first to roll a six wins. What is your chance of winning?",
    wrong=[(F(1, 2), "You ignored going first. The first roller has the edge."),
           (F(1, 6), "You counted only your first roll."),
           (F(5, 11), "You found your friend's chance.")],
    correct="$\\tfrac{1/6}{1 - 25/36} = \\tfrac{6}{11}$.",
    generic="Win now, or both miss and the game starts again.",
    explain="Let $p$ be your chance: $p = \\tfrac16 + \\tfrac{25}{36}p$, so $p = \\tfrac{6}{11}$. The series $\\tfrac16 \\sum (\\tfrac{25}{36})^k$ gives the same.")
key, part = turn_game(F(1, 3), 2, 0)
add(2, "first-to-six", title="First 5 or 6 wins", key=key, key2=part + F(1, 3) * F(4, 9) ** 60 / (1 - F(4, 9)),
    twice="(1/3)/(1 - 4/9); series (1/3) sum (4/9)^k, 60 terms plus exact tail",
    q="You and a friend take turns to roll a die, you first. The first to roll a 5 or a 6 wins. What is your chance of winning?",
    wrong=[(F(1, 2), "You ignored going first. The first roller has the edge."),
           (F(1, 3), "You counted only your first roll."),
           (F(2, 5), "You found your friend's chance.")],
    correct="$\\tfrac{1/3}{1 - 4/9} = \\tfrac35$.",
    generic="Win now, or both miss and the game starts again.",
    explain="Let $p$ be your chance: $p = \\tfrac13 + \\tfrac49 p$, so $p = \\tfrac35$. The series $\\tfrac13 \\sum (\\tfrac49)^k$ gives the same.")
key, part = turn_game(F(1, 6), 3, 0)
add(3, "first-to-six", title="Three players, first six", key=key, key2=part + F(1, 6) * F(125, 216) ** 60 / (1 - F(125, 216)),
    twice="(1/6)/(1 - 125/216); series (1/6) sum (125/216)^k, 60 terms plus exact tail",
    q="Three players take turns to roll a die, you first. The first to roll a six wins. What is your chance of winning?",
    wrong=[(F(1, 3), "You ignored going first. The first roller has the edge."),
           (F(1, 6), "You counted only your first roll."),
           (F(30, 91), "You found the second player's chance.")],
    correct="$\\tfrac{1/6}{1 - 125/216} = \\tfrac{36}{91}$.",
    generic="Win now, or all three miss and the game starts again.",
    explain="Let $p$ be your chance: $p = \\tfrac16 + \\tfrac{125}{216}p$, so $p = \\tfrac{36}{91}$. The series $\\tfrac16 \\sum (\\tfrac{125}{216})^k$ gives the same.")

# ---------- pattern-race ----------
add(1, "pattern-race", title="HH or TH", key=F(1, 4), key2=race("HH", "TH"),
    twice=f"HH first only if the first two tosses are HH; exact Markov solve; 12-toss enumeration {float(race_enum('HH', 'TH')):.4f}",
    q="A fair coin is tossed until HH or TH appears. What is the chance that HH comes first?",
    wrong=[(F(1, 2), "You treated the two patterns as equal. They are not: a T sets up TH."),
           (F(3, 4), "You found the chance that TH comes first."),
           (F(1, 3), "You listed three cases as equally likely.")],
    correct="HH wins only if the first two tosses are HH.",
    generic="What happens once the first T appears?",
    explain="Once a T appears, the next H completes TH before any HH. So HH wins only on HH at the start, with chance $\\tfrac14$. An exact solve over the coin's states gives $\\tfrac14$ too.")
add(2, "pattern-race", title="HHT or THH", key=F(1, 4), key2=race("HHT", "THH"),
    twice=f"HHT first only if the first two tosses are HH; exact Markov solve; 12-toss enumeration {float(race_enum('HHT', 'THH')):.4f}",
    q="A fair coin is tossed until HHT or THH appears. What is the chance that HHT comes first?",
    wrong=[(F(1, 2), "You treated the two patterns as equal. A T before the first HH sets up THH."),
           (F(3, 4), "You found the chance that THH comes first."),
           (F(1, 8), "You needed the first three tosses to be HHT.")],
    correct="HHT wins only if the first two tosses are HH.",
    generic="What happens if a T comes before the first HH?",
    explain="If any T comes before the first HH, that HH completes THH first. So HHT wins only on HH at the start, with chance $\\tfrac14$. An exact solve over the coin's states gives $\\tfrac14$ too.")
add(3, "pattern-race", title="HHH or THH", key=F(1, 8), key2=race("HHH", "THH"),
    twice=f"HHH first only if the first three tosses are HHH; exact Markov solve; 12-toss enumeration {float(race_enum('HHH', 'THH')):.4f}",
    q="A fair coin is tossed until HHH or THH appears. What is the chance that HHH comes first?",
    wrong=[(F(1, 2), "You treated the two patterns as equal. A T before the first HH sets up THH."),
           (F(7, 8), "You found the chance that THH comes first."),
           (F(1, 4), "You needed only HH at the start. The third toss must be H as well.")],
    correct="HHH wins only if the first three tosses are HHH.",
    generic="What happens if a T comes before the first HHH?",
    explain="If any T comes first, the next HH after it completes THH before HHH. So HHH wins only on HHH at the start, with chance $\\tfrac18$. An exact solve over the coin's states gives $\\tfrac18$ too.")

def build(version):
    log = []
    for q, fam in enumerate(FAM, start=1):
        s = B[version][fam]
        assert s["key"] == s["key2"], (version, fam, s["key"], s["key2"])
        vals = [w for w, _ in s["wrong"]]
        assert all(0 < x for x in vals + [s["key"]])
        check_placement(s["key"], vals, f"v{version} B{q}")
        log.append(f"B{q:<2} {fam:<18} key {s['key']}  (twice: {s['twice']})  distractors {[str(x) for x in vals]}")
    return log

def to_json(version, rng):
    log = build(version)
    out = []
    for q, fam in enumerate(FAM, start=1):
        s = B[version][fam]
        w = choice_widget(rng, f"${fr(s['key'])}$", [(f"${fr(x)}$", why) for x, why in s["wrong"]])
        out.append(item(f"b{q:02d}-{fam}", DIFF[fam], [SKILL[fam]], [fam], 120, s["title"], s["q"], w,
                        s["correct"], s["generic"], s["explain"]))
    return out, log
```

### `rank.py`

```python
"""Paper C: likelihood ranking (Q1 to Q6, order widget) and intervals (Q7 to Q10, unshuffled four-option choice).
Ranking values are exact Fractions found two ways; every gap is asserted at 0.02 or more. Interval keys are checked
by exact squares or exact Fraction powers, and each item has exactly one narrowest interval that holds the value."""
from fractions import Fraction as F
from itertools import product, combinations
from math import comb, sqrt, pi
import random
from common import item

def binom_at_least(n, k, p):
    return sum(comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k, n + 1))
def binom_exact(n, k, p):
    return comb(n, k) * p ** k * (1 - p) ** (n - k)
def conv_counts(n, p):
    """Distribution of the number of successes in n trials, by repeated convolution (the second method)."""
    dist = [F(1)]
    for _ in range(n):
        new = [F(0)] * (len(dist) + 1)
        for j, x in enumerate(dist):
            new[j] += x * (1 - p); new[j + 1] += x * p
        dist = new
    return dist
def birthday(n):
    q = F(1)
    for i in range(n): q *= F(365 - i, 365)
    return 1 - q
def birthday2(n):        # recursion on the chance that the first m people are all different
    r = F(1)
    for m in range(1, n): r = r - r * F(m, 365)
    return 1 - r
def ace_in(k):
    return 1 - F(comb(48, k), comb(52, k))
def ace_in2(k):          # hypergeometric sum over 1 to 4 aces
    return sum(F(comb(4, j) * comb(48, k - j), comb(52, k)) for j in range(1, 5))
DECK = [(r, s) for s in "SHDC" for r in range(1, 14)]
def cards2(pred):
    hands = list(combinations(DECK, 2)); return F(sum(1 for h in hands if pred(h)), len(hands))
def one(pred):
    return F(sum(1 for c in DECK if pred(c)), 52)
def dice(n): return list(product(range(1, 7), repeat=n))
def pd(n, pred): o = dice(n); return F(sum(1 for x in o if pred(x)), len(o))
def coins(n, pred): o = list(product("HT", repeat=n)); return F(sum(1 for x in o if pred(x)), len(o))

# each event: (text, value by closed form, value by a second method, the tempting slip or None)
E = {}
def ev(key, text, a, b, slip=None): E[key] = (text, a, b, slip)
ev("six4", "At least one six in 4 rolls of a die", 1 - F(5, 6) ** 4, pd(4, lambda x: 6 in x), "n x p reads 4/6 = 0.667")
ev("dbl24", "At least one double six in 24 rolls of two dice", 1 - F(35, 36) ** 24, 1 - conv_counts(24, F(1, 36))[0], "n x p reads 24/36 = 0.667")
ev("h6of10", "At least 6 heads in 10 tosses of a coin", F(210 + 120 + 45 + 10 + 1, 1024), sum(conv_counts(10, F(1, 2))[6:]))
ev("h2of4", "Exactly 2 heads in 4 tosses of a coin", F(6, 16), coins(4, lambda x: x.count("H") == 2))
ev("suit2", "Two cards from a deck share a suit", F(12, 51), cards2(lambda h: h[0][1] == h[1][1]))
ev("tot7", "A total of 7 on two dice", F(6, 36), pd(2, lambda x: sum(x) == 7))
ev("six3", "At least one six in 3 rolls of a die", 1 - F(5, 6) ** 3, pd(3, lambda x: 6 in x), "n x p reads 3/6 = 0.5")
ev("tot678", "A total of 6, 7 or 8 on two dice", F(16, 36), pd(2, lambda x: 6 <= sum(x) <= 8))
ev("diffcol", "Two cards from a deck differ in colour", F(26, 51), cards2(lambda h: (h[0][1] in "HD") != (h[1][1] in "HD")))
ev("h5of10", "Exactly 5 heads in 10 tosses", binom_exact(10, 5, F(1, 2)), conv_counts(10, F(1, 2))[5], "more tosses, more likely")
ev("h1of2", "Exactly 1 head in 2 tosses", F(1, 2), coins(2, lambda x: x.count("H") == 1))
ev("h3of6", "Exactly 3 heads in 6 tosses", F(20, 64), coins(6, lambda x: x.count("H") == 3))
ev("bday23", "Two of 23 people share a birthday", birthday(23), birthday2(23))
ev("diff3", "Three dice all show different faces", F(120, 216), pd(3, lambda x: len(set(x)) == 3))
ev("ace5", "At least one ace in 5 cards dealt from a deck", ace_in(5), ace_in2(5), "n x p reads 5/13 = 0.385")
ev("np1", "At least one six in 6 rolls of a die", binom_at_least(6, 1, F(1, 6)), sum(conv_counts(6, F(1, 6))[1:]), "n x p reads 1 for all three")
ev("np2", "At least two sixes in 12 rolls of a die", binom_at_least(12, 2, F(1, 6)), sum(conv_counts(12, F(1, 6))[2:]), "more rolls, more likely")
ev("np3", "At least three sixes in 18 rolls of a die", binom_at_least(18, 3, F(1, 6)), sum(conv_counts(18, F(1, 6))[3:]), "more rolls, more likely")
# version 2
ev("six2", "At least one six in 2 rolls of a die", 1 - F(5, 6) ** 2, pd(2, lambda x: 6 in x), "n x p reads 2/6 = 0.333")
ev("die56", "A die shows 5 or 6", F(1, 3), pd(1, lambda x: x[0] >= 5))
ev("akq", "One card from a deck is an ace, king or queen", F(12, 52), one(lambda c: c[0] in (1, 12, 13)))
ev("h1of3", "Exactly 1 head in 3 tosses", F(3, 8), coins(3, lambda x: x.count("H") == 1))
ev("red2", "Two cards from a deck are both red", F(26 * 25, 52 * 51), cards2(lambda h: h[0][1] in "HD" and h[1][1] in "HD"))
ev("ace3r", "At least one ace in 3 cards drawn with replacement", 1 - F(12, 13) ** 3, 1 - conv_counts(3, F(1, 13))[0], "n x p reads 3/13 = 0.231")
ev("heart2r", "At least one heart in 2 cards drawn with replacement", 1 - F(3, 4) ** 2, 1 - conv_counts(2, F(1, 4))[0], "n x p reads 2/4 = 0.5")
ev("dbl", "Two dice show a double", F(6, 36), pd(2, lambda x: x[0] == x[1]))
ev("ace6r", "At least one ace in 6 cards drawn with replacement", 1 - F(12, 13) ** 6, 1 - conv_counts(6, F(1, 13))[0], "n x p reads 6/13 = 0.462")
ev("tot57", "A total of 5, 6 or 7 on two dice", F(15, 36), pd(2, lambda x: 5 <= sum(x) <= 7))
ev("redace", "One card from a deck is red or an ace", F(28, 52), one(lambda c: c[1] in "HD" or c[0] == 1))
ev("h4of5", "At least 4 heads in 5 tosses", F(6, 32), coins(5, lambda x: x.count("H") >= 4))
ev("h8of10", "At least 8 heads in 10 tosses", F(45 + 10 + 1, 1024), sum(conv_counts(10, F(1, 2))[8:]), "more tosses, more likely")
ev("tot1112", "A total of 11 or 12 on two dice", F(3, 36), pd(2, lambda x: sum(x) >= 11))
ev("bday30", "Two of 30 people share a birthday", birthday(30), birthday2(30))
ev("six8", "At least one six in 8 rolls of a die", 1 - F(5, 6) ** 8, 1 - conv_counts(8, F(1, 6))[0], "n x p reads 8/6, over 1")
ev("ace10", "At least one ace in 10 cards dealt from a deck", ace_in(10), ace_in2(10), "n x p reads 10/13 = 0.769")
ev("c1of2", "At least 1 head in 2 tosses", F(3, 4), coins(2, lambda x: "H" in x))
ev("c2of4", "At least 2 heads in 4 tosses", F(11, 16), coins(4, lambda x: x.count("H") >= 2), "more tosses, more likely")
ev("c3of6", "At least 3 heads in 6 tosses", F(42, 64), coins(6, lambda x: x.count("H") >= 3), "more tosses, more likely")
# version 3
ev("six5", "At least one six in 5 rolls of a die", 1 - F(5, 6) ** 5, pd(5, lambda x: 6 in x), "n x p reads 5/6 = 0.833")
ev("die3up", "A die shows 3 or more", F(2, 3), pd(1, lambda x: x[0] >= 3))
ev("tot8up", "A total of 8 or more on two dice", F(15, 36), pd(2, lambda x: sum(x) >= 8))
ev("h3of4", "Exactly 3 heads in 4 tosses", F(4, 16), coins(4, lambda x: x.count("H") == 3))
ev("akqj", "One card from a deck is an ace or a picture card", F(16, 52), one(lambda c: c[0] in (1, 11, 12, 13)))
ev("tot4", "A total of 4 on two dice", F(3, 36), pd(2, lambda x: sum(x) == 4))
ev("ace4", "At least one ace in 4 cards dealt from a deck", ace_in(4), ace_in2(4), "n x p reads 4/13 = 0.308")
ev("same3", "Three tosses all land the same way", F(2, 8), coins(3, lambda x: len(set(x)) == 1))
ev("tot510", "A total of 5 or 10 on two dice", F(7, 36), pd(2, lambda x: sum(x) in (5, 10)))
ev("one6of6", "Exactly one six in 6 rolls", binom_exact(6, 1, F(1, 6)), conv_counts(6, F(1, 6))[1], "more rolls, more likely")
ev("two6of12", "Exactly two sixes in 12 rolls", binom_exact(12, 2, F(1, 6)), conv_counts(12, F(1, 6))[2], "more rolls, more likely")
ev("one6of3", "Exactly one six in 3 rolls", binom_exact(3, 1, F(1, 6)), pd(3, lambda x: x.count(6) == 1))
ev("bday25", "Two of 25 people share a birthday", birthday(25), birthday2(25))
ev("dbl36", "At least one double six in 36 rolls of two dice", 1 - F(35, 36) ** 36, 1 - conv_counts(36, F(1, 36))[0], "n x p reads 36/36 = 1")
ev("ace8", "At least one ace in 8 cards dealt from a deck", ace_in(8), ace_in2(8), "n x p reads 8/13 = 0.615")
ev("f1of3", "At least one 5 or 6 in 3 rolls of a die", binom_at_least(3, 1, F(1, 3)), pd(3, lambda x: any(y >= 5 for y in x)), "n x p reads 1 for all three")
ev("f2of6", "At least two 5s or 6s in 6 rolls", binom_at_least(6, 2, F(1, 3)), sum(conv_counts(6, F(1, 3))[2:]), "more rolls, more likely")
ev("f3of9", "At least three 5s or 6s in 9 rolls", binom_at_least(9, 3, F(1, 3)), sum(conv_counts(9, F(1, 3))[3:]), "more rolls, more likely")

# brief worked checks for version 1
assert E["six4"][1] == F(671, 1296) and E["h6of10"][1] == F(386, 1024) and E["suit2"][1] == F(4, 17)
for k, (_, a, b, _) in E.items(): assert a == b, (k, a, b)

RANK = {
 1: [("c01", 2, ["six4", "dbl24", "h6of10"]), ("c02", 2, ["h2of4", "suit2", "tot7"]),
     ("c03", 3, ["six3", "tot678", "diffcol"]), ("c04", 3, ["h5of10", "h1of2", "h3of6"]),
     ("c05", 4, ["bday23", "diff3", "ace5"]), ("c06", 5, ["np1", "np2", "np3"])],
 2: [("c01", 2, ["six2", "die56", "akq"]), ("c02", 2, ["h1of3", "ace3r", "dbl"]),
     ("c03", 3, ["ace6r", "tot57", "redace"]), ("c04", 3, ["h4of5", "h8of10", "tot1112"]),
     ("c05", 4, ["bday30", "six8", "ace10"]), ("c06", 5, ["c1of2", "c2of4", "c3of6"])],
 3: [("c01", 2, ["six5", "die3up", "tot8up"]), ("c02", 2, ["h3of4", "akqj", "heart2r"]),
     ("c03", 3, ["ace4", "same3", "tot510"]), ("c04", 3, ["one6of6", "two6of12", "one6of3"]),
     ("c05", 4, ["bday25", "dbl36", "ace8"]), ("c06", 5, ["f1of3", "f2of6", "f3of9"])],
}
GEN = {"c01": "Work out each chance roughly; a complement is often quickest.",
       "c02": "Turn each event into a fraction, then compare.",
       "c03": "Use complements for the at-least-one events, and do not add chances.",
       "c04": "Count the ways for each, then divide by the outcomes.",
       "c05": "Estimate each with a complement: one minus the chance of none.",
       "c06": "Do not assume the events tie because the expected counts match."}

def f3(x): return f"{float(x):.3f}"

def build_rank(version):
    out, log = [], []
    for qid, d, keys in RANK[version]:
        evs = sorted(keys, key=lambda k: -E[k][1])
        vals = [E[k][1] for k in evs]
        for a, b in zip(vals, vals[1:]): assert a - b >= F(2, 100), (version, qid, evs, float(a - b))
        slips = [(k, E[k][3]) for k in keys if E[k][3]]
        if (version, qid) != (1, "c02"):      # the brief's worked C2 has no such event; kept as written
            assert slips, (version, qid, "no event tempts n x p or more-trials")
        # does the slip actually change the order?  record it in the log
        lines = [{"id": k, "text": E[k][0]} for k in keys]
        names = {k: E[k][0] for k in keys}
        expl = (f"The chances are {f3(vals[0])} for “{names[evs[0]].lower() if False else names[evs[0]]}”, "
                f"{f3(vals[1])} for the second and {f3(vals[2])} for the third.")
        expl = (f"{names[evs[0]]}: {f3(vals[0])}. {names[evs[1]]}: {f3(vals[1])}. {names[evs[2]]}: {f3(vals[2])}.")
        widget = {"kind": "order", "lines": lines, "answer": evs}
        out.append(item(f"{qid}-rank", d, ["mp-estimate"], ["likelihood-ranking"], 60, "Rank three events",
                        "Put the three events in order, most likely first.", widget,
                        f"Most likely first: {f3(vals[0])}, {f3(vals[1])}, {f3(vals[2])}.", GEN[qid], expl))
        log.append(f"{qid} d{d} " + "; ".join(f"{k} {vals[i]} = {f3(vals[i])}" for i, k in enumerate(evs))
                   + f"  gaps {f3(vals[0] - vals[1])}, {f3(vals[1] - vals[2])}  slips: {slips}")
    return out, log

# ---------- intervals ----------
# value: exact check function value_cmp(x) -> sign of (value - x) for a Fraction x, and a float for display
def sqrt_cmp(N): return (lambda x: (N > x * x) - (N < x * x)), sqrt(N)
def pow_cmp(base, n):
    v = F(base) ** n
    return (lambda x: (v > x) - (v < x)), float(v)
def exact_cmp(v): return (lambda x: (v > x) - (v < x)), float(v)

IV = {
 1: [dict(id="c07", d=2, title="A square root", q="Choose the tightest interval that holds $\\sqrt{300}$.",
          val=sqrt_cmp(300), key=(17, 18), wide=(15, 20), miss=[(16, 17), (19, 20)],
          check="$17^2 = 289$ and $18^2 = 324$ bracket 300",
          explain="$17^2 = 289$ and $18^2 = 324$, so $\\sqrt{300}$ lies between 17 and 18. In fact $\\sqrt{300} = 10\\sqrt3 \\approx 17.32$. The interval 15 to 20 holds it too, but it is wider, so it scores less on the day.",
          second="10 sqrt 3 = 17.3205"),
     dict(id="c08", d=3, title="Compound growth", q="Choose the tightest interval that holds $1.05^{14}$.",
          val=pow_cmp(F(105, 100), 14), key=(F(19, 10), F(2)), wide=(F(3, 2), F(5, 2)), miss=[(F(17, 10), F(18, 10)), (F(2), F(21, 10))],
          check="rule of 72: doubling in 14.4 years, so just under 2",
          explain="By the rule of 72, 5% a year doubles money in about 14.4 years. So 14 years gives just under 2; the exact value is 1.980. The interval 1.5 to 2.5 holds it too, but it is wider, so it scores less.",
          second="exact Fraction power 1.97993"),
     dict(id="c09", d=4, title="No six in twelve", q="A die is rolled 12 times. Choose the tightest interval that holds the chance of no six, $(\\tfrac56)^{12}$.",
          val=pow_cmp(F(5, 6), 12), key=(F(10, 100), F(12, 100)), wide=(F(5, 100), F(25, 100)), miss=[(F(8, 100), F(10, 100)), (F(14, 100), F(16, 100))],
          check="(5/6)^6 is about 0.335, and 0.335^2 is about 0.112",
          explain="$(\\tfrac56)^6 \\approx 0.335$, and squaring gives about 0.112. The exact value is 0.1122. The interval 0.05 to 0.25 holds it too, but it is wider, so it scores less.",
          second="exact Fraction power 0.112157"),
     dict(id="c10", d=5, title="Growth over 100 periods", q="£1 grows by 2% a period for 100 periods. Choose the tightest interval that holds its value in pounds, $1.02^{100}$.",
          val=pow_cmp(F(102, 100), 100), key=(F(7), F(15, 2)), wide=(F(5), F(10)), miss=[(F(6), F(13, 2)), (F(15, 2), F(8))],
          check="ln 1.02 is about 0.0198, so the value is about e^1.98, near 7.24",
          explain="$\\ln 1.02 \\approx 0.0198$, so $1.02^{100} \\approx e^{1.98} \\approx 7.24$. Using $e^2 \\approx 7.39$ alone lands in the same interval. The interval 5 to 10 holds it too, but it is wider, so it scores less.",
          second="exact Fraction power 7.24465")],
 2: [dict(id="c07", d=2, title="A square root", q="Choose the tightest interval that holds $\\sqrt{500}$.",
          val=sqrt_cmp(500), key=(22, 23), wide=(20, 25), miss=[(21, 22), (24, 25)],
          check="$22^2 = 484$ and $23^2 = 529$ bracket 500",
          explain="$22^2 = 484$ and $23^2 = 529$, so $\\sqrt{500}$ lies between 22 and 23. In fact $\\sqrt{500} = 10\\sqrt5 \\approx 22.36$. The interval 20 to 25 holds it too, but it is wider, so it scores less on the day.",
          second="10 sqrt 5 = 22.3607"),
     dict(id="c08", d=3, title="Compound growth", q="Choose the tightest interval that holds $1.07^{12}$.",
          val=pow_cmp(F(107, 100), 12), key=(F(22, 10), F(23, 10)), wide=(F(2), F(3)), miss=[(F(2), F(21, 10)), (F(23, 10), F(24, 10))],
          check="1.07^10 is about 1.97 (rule of 72), times 1.07^2 = 1.1449 gives about 2.25",
          explain="$1.07^{10} \\approx 1.97$, just under a doubling by the rule of 72. Two more years multiply by $1.07^2 \\approx 1.145$, giving about 2.25. The interval 2 to 3 holds it too, but it is wider, so it scores less.",
          second="exact Fraction power 2.25219"),
     dict(id="c09", d=4, title="A rare event that never comes", q="An event has a 1% chance each day. Choose the tightest interval that holds the chance it never happens in 100 days, $0.99^{100}$.",
          val=pow_cmp(F(99, 100), 100), key=(F(35, 100), F(38, 100)), wide=(F(2, 10), F(5, 10)), miss=[(F(32, 100), F(35, 100)), (F(41, 100), F(44, 100))],
          check="(1 - 1/n)^n is just under 1/e = 0.368",
          explain="$(1 - \\tfrac1n)^n$ is just under $\\tfrac1e \\approx 0.368$. The exact value is 0.366. The interval 0.2 to 0.5 holds it too, but it is wider, so it scores less.",
          second="exact Fraction power 0.366032"),
     dict(id="c10", d=5, title="Exactly half heads", q="A coin is tossed 20 times. Choose the tightest interval that holds the chance of exactly 10 heads, $\\binom{20}{10} / 2^{20}$.",
          val=exact_cmp(F(comb(20, 10), 2 ** 20)), key=(F(17, 100), F(19, 100)), wide=(F(1, 10), F(3, 10)), miss=[(F(14, 100), F(16, 100)), (F(19, 100), F(21, 100))],
          check="sqrt(2/(pi n)) with n = 20 is about 0.178",
          explain="For $n$ tosses, exactly half heads is about $\\sqrt{2 / (\\pi n)}$, which is 0.178 for 20. The exact value is $184756 / 1048576 \\approx 0.176$. The interval 0.1 to 0.3 holds it too, but it is wider, so it scores less.",
          second="184756/1048576 = 0.176197")],
 3: [dict(id="c07", d=2, title="A square root", q="Choose the tightest interval that holds $\\sqrt{700}$.",
          val=sqrt_cmp(700), key=(26, 27), wide=(25, 30), miss=[(24, 25), (27, 28)],
          check="$26^2 = 676$ and $27^2 = 729$ bracket 700",
          explain="$26^2 = 676$ and $27^2 = 729$, so $\\sqrt{700}$ lies between 26 and 27. In fact $\\sqrt{700} = 10\\sqrt7 \\approx 26.46$. The interval 25 to 30 holds it too, but it is wider, so it scores less on the day.",
          second="10 sqrt 7 = 26.4575"),
     dict(id="c08", d=3, title="Compound growth", q="Choose the tightest interval that holds $1.05^{20}$.",
          val=pow_cmp(F(105, 100), 20), key=(F(26, 10), F(27, 10)), wide=(F(2), F(3)), miss=[(F(25, 10), F(26, 10)), (F(28, 10), F(29, 10))],
          check="1.05^14 is about 1.98, and 1.05^6 is about 1.34, so about 2.65",
          explain="$1.05^{14} \\approx 1.98$ by the rule of 72, and $1.05^6 \\approx 1.34$. Their product is about 2.65; the exact value is 2.653. The interval 2 to 3 holds it too, but it is wider, so it scores less.",
          second="exact Fraction power 2.65330"),
     dict(id="c09", d=4, title="Ten losses in a row", q="A trade wins a quarter of the time. Choose the tightest interval that holds the chance of 10 losses in a row, $0.75^{10}$.",
          val=pow_cmp(F(3, 4), 10), key=(F(5, 100), F(6, 100)), wide=(F(2, 100), F(10, 100)), miss=[(F(3, 100), F(4, 100)), (F(6, 100), F(7, 100))],
          check="0.75^5 is about 0.237, and 0.237^2 is about 0.056",
          explain="$0.75^5 \\approx 0.237$, and squaring gives about 0.056. The exact value is 0.0563. The interval 0.02 to 0.10 holds it too, but it is wider, so it scores less.",
          second="exact Fraction power 0.0563135"),
     dict(id="c10", d=5, title="Exactly half heads", q="A coin is tossed 30 times. Choose the tightest interval that holds the chance of exactly 15 heads, $\\binom{30}{15} / 2^{30}$.",
          val=exact_cmp(F(comb(30, 15), 2 ** 30)), key=(F(13, 100), F(16, 100)), wide=(F(1, 10), F(3, 10)), miss=[(F(10, 100), F(13, 100)), (F(19, 100), F(22, 100))],
          check="sqrt(2/(pi n)) with n = 30 is about 0.146",
          explain="For $n$ tosses, exactly half heads is about $\\sqrt{2 / (\\pi n)}$, which is 0.146 for 30. The exact value is 0.144. The interval 0.1 to 0.3 holds it too, but it is wider, so it scores less.",
          second="155117520/1073741824 = 0.144464")],
}

def dp_of(x):
    x = F(x)
    for d in range(0, 5):
        if (x * 10 ** d).denominator == 1: return d
    raise ValueError(x)
def fmt(x, dp=None):
    x = F(x)
    if dp is None: dp = dp_of(x)
    return f"{float(x):.{dp}f}"

def build_iv(version):
    out, log = [], []
    for s in IV[version]:
        cmp_, approx = s["val"]
        lo, hi = map(F, s["key"]); w = hi - lo
        assert cmp_(lo) > 0 and cmp_(hi) < 0, (version, s["id"], "key does not hold the value")
        margin = min(approx - float(lo), float(hi) - approx)
        assert margin >= 0.15 * float(w), (version, s["id"], "value too near the key's edge", margin)
        wl, wh = map(F, s["wide"])
        assert cmp_(wl) > 0 and cmp_(wh) < 0 and wh - wl > w and wl <= lo and wh >= hi
        sides = []
        for a, b in s["miss"]:
            a, b = F(a), F(b)
            assert b - a == w, (version, s["id"], "miss width differs")
            assert not (cmp_(a) > 0 and cmp_(b) < 0), (version, s["id"], "a miss holds the value")
            sides.append("below" if cmp_(b) >= 0 else "above")
        assert sorted(sides) == ["above", "below"], (version, s["id"], sides)
        # the key must not sit midway between the two misses (no equal slips either side)
        (a1, b1), (a2, b2) = [tuple(map(F, m)) for m in sorted(s["miss"])]
        assert lo - b1 != a2 - hi, (version, s["id"], "key midway between the misses")
        # exactly one narrowest interval that holds the value
        opts = [("key", lo, hi), ("wide", wl, wh)] + [("miss", F(a), F(b)) for a, b in s["miss"]]
        holders = [o for o in opts if cmp_(o[1]) > 0 and cmp_(o[2]) < 0]
        narrow = min(h[2] - h[1] for h in holders)
        assert [h[0] for h in holders if h[2] - h[1] == narrow] == ["key"]
        opts.sort(key=lambda o: (o[1], o[2]))
        dp = max(dp_of(x) for o in opts for x in o[1:])
        options = []
        for i, (kind, a, b) in enumerate(opts):
            o = {"id": "abcd"[i], "text": f"{fmt(a, dp)} to {fmt(b, dp)}"}
            if kind == "key": o["correct"] = True
            elif kind == "wide": o["why"] = f"This holds the value, but {fmt(lo, dp)} to {fmt(hi, dp)} holds it too and is tighter. A wider interval scores less on the day."
            else:
                o["why"] = (f"This sits wholly below the value, {approx:.4g}." if cmp_(b) >= 0 else
                            f"This sits wholly above the value, {approx:.4g}.")
            options.append(o)
        widget = {"kind": "choice", "label": "Intervals, in order", "options": options}
        out.append(item(f"{s['id']}-interval", s["d"], ["mp-estimate"], ["interval"], 60, s["title"], s["q"], widget,
                        f"{fmt(lo, dp)} to {fmt(hi, dp)} holds the value, {approx:.4g}, and is the tightest that does.",
                        "Bracket the value from both sides first, then pick the narrowest interval that holds it.",
                        s["explain"]))
        log.append(f"{s['id']} d{s['d']} value {approx:.6g} (twice: {s['check']}; {s['second']})  key [{fmt(lo)}, {fmt(hi)}]"
                   f"  wide [{fmt(wl)}, {fmt(wh)}]  misses {[(fmt(a), fmt(b)) for a, b in s['miss']]} ({', '.join(sides)})  margin {margin:.4g}")
    return out, log
```

### `examshot.mjs`

```js
// examshot.mjs <exam-id> <outdir>: start card, every paper's items (named by paper), the check and the results page,
// at 1280 and 390 px; also reports sideways scroll at 390 px and page errors. Serves app/ on port 8791.
import { spawn, execSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
const [ex, out] = process.argv.slice(2);
fs.mkdirSync(out, { recursive: true });
const root = execSync('npm root -g', { encoding: 'utf8' }).trim();
const { chromium } = await import(pathToFileURL(path.join(root, 'playwright', 'index.mjs')).href);
const port = 8791;
const proc = spawn('python3', ['-m', 'http.server', String(port), '--bind', '127.0.0.1', '--directory', '/home/user/zero-to-quant/app'], { stdio: 'ignore' });
await new Promise(r => setTimeout(r, 800));
const base = `http://127.0.0.1:${port}`;
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const ctx = await browser.newContext({ viewport: { width: 1280, height: 860 } });
await ctx.route(/^https:\/\/fonts\.(googleapis|gstatic)\.com\//, r => r.fulfill({ status: 200, body: '', headers: { 'content-type': 'text/css' } }));
const page = await ctx.newPage();
const errs = [], wide = [];
page.on('pageerror', e => errs.push(e.message));
const shot = async (name) => {
  await page.waitForTimeout(450);
  await page.screenshot({ path: path.join(out, name + '.png') });
  await page.setViewportSize({ width: 390, height: 844 }); await page.waitForTimeout(350);
  if (await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1)) wide.push(name);
  await page.screenshot({ path: path.join(out, name + '-390.png') });
  await page.setViewportSize({ width: 1280, height: 860 }); await page.waitForTimeout(150);
};
await page.goto(base + '/#setup');
await page.waitForFunction(() => window.ZQ && ZQ.content && ZQ.content.ready && ZQ.state);
await page.evaluate(() => ZQ.content.ready.then(() => { localStorage.clear(); ZQ.state.reset(); }));
await page.reload();
await page.waitForSelector('[data-name]');
await page.fill('[data-name]', 'Shots'); await page.click('[data-next]');
await page.click('[data-track="Trader"]'); await page.click('[data-next]');
await page.click('[data-h="15"]'); await page.click('[data-stage="1"]'); await page.click('[data-next]');
await page.waitForFunction(() => ZQ.state.flags.setupDone === true);
await page.evaluate((h) => { location.hash = h; }, 'exam/' + ex);
await page.waitForFunction(() => window.ZQ && ZQ.test && ZQ.test.current().kind !== 'loading');
let n = 0, last = '';
const want = (p, i) => (p === 0 && [0, 3, 13].includes(i)) || (p === 1 && [0, 4, 10, 14].includes(i)) || (p === 2 && [0, 5, 6, 9].includes(i));
while (true) {
  const c = await page.evaluate(() => ZQ.test.current());
  if (c.kind === 'done') break;
  const key = `${c.kind}:${c.paper}:${c.screenIndex}:${c.state}`;
  if (key === last || ++n > 300) { console.log('stuck', key); break; }
  last = key;
  if (c.kind === 'start' || c.kind === 'submit' || c.kind === 'check' || (c.kind === 'item' && want(c.paper, c.screenIndex)))
    await shot(`${String(n).padStart(3, "0")}-${c.kind}-p${c.paper ?? "x"}-${String(c.screenIndex).padStart(2, "0")}`);
  if (c.kind === 'item') { await page.evaluate(() => ZQ.test.answerCorrect()); await page.evaluate(() => ZQ.test.check()); }
  await page.evaluate(() => ZQ.test.continue()); await page.waitForTimeout(120);
}
await shot('results');
console.log(JSON.stringify({ errors: errs, wideAt390: wide }));
await browser.close(); proc.kill();
```
