# Brief: the three online-assessment mocks

Three mock exams from `docs/briefs/interview-plan.md` section (d): `mock-oa-arith`, `mock-oa-sig` and `mock-oa-trader`. One content agent writes one mock, from its section below. It follows `docs/LEVEL-BRIEF.md` for checking, playthrough and reporting, with an exam in place of a level.

### Shared rules for the three mocks

**Schema.** Read `docs/AUTHORING.md` section 5: "Mock assessment", "Paper fields", "Generated items", "`tags` and `pace`", plus the item format at the top of section 5. Read the mock rules in section 7 ("Mock and timed rules"). Copy the shape of `app/content/exams/mock-sample.json`: `id`, `name`, `style`, `models`, `description`, optional `skills`, then `parts` (papers and checks). Each paper has `kind: "paper"`, `id`, `name`, `minutes`, `scoring`, one of `pass` or `passNet`, optional `navigation` and `skip`, and `items`.

**What the engine has built (checked in AUTHORING and ENGINE-BACKLOG 450 to 458, not taken from the plan).**

| Plan item | State | What a mock does about it |
| --- | --- | --- |
| E1 net scoring, `scoring` and `passNet` | Built (450) | Use it. The results page shows the net score. |
| E2 `navigation: "forward"`, `skip: false` | Built (451) | Use it where the reported test is forward only. |
| E4 generated arithmetic items | Built (452), **whole numbers only**: add, sub, mul, div from `content/warmup.json`; near misses are reverse operation, misplaced point and slipped digit | `mock-oa-arith` uses it. Decimals, fractions and percentages are authored. |
| E5 mock exam kind | Built (453) | `exams/mock-<id>.json`, listed on Review under "Mock assessments" with a trend. |
| E9 per-item timing, `pace`, `tags` | Built (457, 458) | Give every authored item `tags` (family first) and `pace` in seconds. Generator entries take neither; they count under `mental-arithmetic`. |
| E3 fresh draws from a bank per sitting | **Not built** (456 says the bank draw for exam papers is not built) | Three fixed versions per mock as three files, where the plan asks for them. |
| E15 calculator panel | **Not built** | The description tells the learner to have a basic calculator ready (`mock-oa-sig`). No-calculator mocks end with a self-ticked check. |
| Interval scoring (tighter correct range scores more) | **Not built**: no interval widget, no per-option marks | A four-option choice of intervals, one narrowest correct (`mock-oa-trader` paper C). |

**Intro screen.** The start card prints `name`, then `description` as plain text (escaped: no Markdown, no KaTeX), then "Models ..." from `models`. The engine adds its own rules list: total minutes, question count, "generated afresh" when a paper has a generator entry, no going back on forward papers, negative marking and the pass mark. So `description` says only what the engine cannot: that the format is reported, the calculator rule, and anything the learner should know before starting.

**Firm names** appear only in `models` and `description`, each time marked "reported" with the as-of month (Nov 2026). Never in `name`, items, feedback or explanations.

**A check part is a pass condition.** On a mock with a check, the attempt passes only when every paper passes and every check is ticked (`exam.js`, `passed = every paper passed && checksOk`). Use that for "I used no calculator".

**Voice** (binding, AUTHORING section 6 and CLAUDE.md): British English, no exclamation marks, no em-dashes, sentences under 20 words, explanations of at most three sentences, £ for money. Every `choice` carries `"shuffle": true`, except interval items, whose options are ordered ranges (AUTHORING forbids shuffling ordered options). Every distractor has a `why` naming the learner's action ("You added the tops and the bottoms."). Every stated number is computed twice: once in closed form, once by enumeration, a linear solve or a series, both as `Fraction`s, with an `assert` that they agree.

**Scripts.** Every item that is not engine-generated comes from a deterministic seeded Python script the agent writes in its own scratchpad folder `/tmp/claude-0/-home-user-zero-to-quant/821a2fc9-d022-56ef-9082-6619f873e50b/scratchpad/exam-<id>/`. The script holds every number as a `Fraction`, asserts each answer two ways, writes the exam JSON, and is embedded in full in the report, as `gen17.py` is in `docs/reports/mental-pressure-4.md`. The sandbox CPython may lack SciPy: use `fractions`, `itertools` and `math` only.

**Packages for the playthrough.** `<pkgs>` is `/tmp/claude-0/-home-user-zero-to-quant/821a2fc9-d022-56ef-9082-6619f873e50b/scratchpad/pkgs`. If it is missing, build it with `bash app/tools/fetch-local-cdn.sh <pkgs>`.

**Do not edit** engine files (`app/js/`, `app/tools/`, `app/css/`, `app/index.html`), any `course.json`, `content/prep.json`, `content/warmup.json`, other exams, the `mm-games` course or `docs/briefs/mm-games.md`. Do not commit. Propose any `prep.json` change in the report.

**Common acceptance checks.**

1. From `app/`: `node tools/validate.mjs 2>&1 | tail -5` reports 0 errors.
2. From `app/`: `node tools/playthrough.mjs --exam <id> --local-cdn <pkgs> 2>&1 | tail -30` is green, and again with `--mobile`. Repeat for each version file.
3. Every keyed answer is recomputed by the script's second method; the report lists each item's answer and its two computations.
4. Screenshots at 1280 and 390 px of the start card, one item of each widget kind and the results page; options fit and nothing overlaps.
5. Report at `docs/reports/exam-<id>.md` (files, item counts by family and difficulty, validator and playthrough results, the script and its output, every number with its source, proposed changes). Engine gaps go to `docs/BACKLOG-INBOX.md` under `Raised later (exam <id>):` as unnumbered bullets. Hand back at most six lines.

## mock-oa-arith

**File.** `app/content/exams/mock-oa-arith.json`. One file, no versions (reason below).

- `id`: `mock-oa-arith`
- `name`: `Arithmetic sprint: 80 in 8`
- `style`: `trader`
- `models`: `Reported, as of Nov 2026: Optiver's 80 in 8, 80 four-option arithmetic questions in 8 minutes, +1 right, −1 wrong, no skipping, no calculator.`
- `skills`: `{ "mp-speed": "Speed arithmetic", "mp-fractions": "Fractions and percentages at speed" }`

**Description** (the intro text, plain, each sentence under 20 words):

> This is the reported format of Optiver's 80 in 8 test, as candidates described it by Nov 2026. You have 80 arithmetic questions in 8 minutes, each with four options. A right answer scores +1 and a wrong one −1. You cannot skip or go back. Use no calculator; reports differ on scrap paper, so use none if you can. Most questions are generated afresh each time you sit. The pass mark here is 55 net, inside the reported band of 50 to 60.

**Parts.**

1. Paper `sprint`, name `80 in 8`: `minutes: 8`, `scoring: { "right": 1, "wrong": -1, "blank": 0 }`, `passNet: 55` (the most is 80), `navigation: "forward"`, `skip: false`.
2. Check `no-calculator`, name `I used no calculator`, detail `Tick this only if you sat the whole paper without one.`

**Item design: 80 items in 16 groups.** Each group is one generator entry of `n: 4` followed by one authored item. That gives 64 generated whole-number items and 16 authored ones (6 decimal, 5 fraction, 5 percentage). Authored items sit at Q5, Q10, ..., Q80. Each generator entry has its own random stream (`expand` hashes seed, paper and position), so editing one entry does not move the others.

Difficulty ramp, four blocks of 20 (each block is four groups). Ranges go on `add` and `mul` only; `sub` and `div` are their reverses and take a weight of 1.

| Block | Questions | Generator `mix` (all weights 1) | `difficulty` | Authored items, in order |
| --- | --- | --- | --- | --- |
| A | Q1 to Q20 | `add` a [10, 99], b [10, 99]; `mul` a [2, 9], b [2, 30] | 2 | percentage, decimal, fraction, decimal |
| B | Q21 to Q40 | warm-up defaults (`add`, `sub`, `mul`, `div` as plain weights) | 3 | percentage, decimal, fraction, percentage |
| C | Q41 to Q60 | `add` a [100, 999], b [10, 99]; `mul` a [3, 12], b [12, 99] | 3 | decimal, fraction, percentage, decimal |
| D | Q61 to Q80 | `add` a [100, 999], b [100, 999]; `mul` a [11, 19], b [11, 49] | 4 | fraction, percentage, decimal, fraction |

Each generator entry reads, for block A: `{ "generator": "arith", "mix": { "add": { "weight": 1, "a": [10, 99], "b": [10, 99] }, "sub": 1, "mul": { "weight": 1, "a": [2, 9], "b": [2, 30] }, "div": 1 }, "n": 4, "options": 4, "difficulty": 2, "skills": ["mp-speed"] }`. No `tags` or `pace` on a generator entry: the validator refuses unknown keys there.

**Generated items, worked.** With exactly this layout, `#exam/mock-oa-arith/1` gives, from the engine's own `ZQ.arith.expand` (run in node over `app/js/engine/arith.js`):

- Q2: $175 - 97$, key 78. Options 78, 88 (slipped digit), 7.8 (misplaced point), 272 (reverse: $175 + 97$). Check: $97 + 78 = 175$, and $175 - 100 + 3 = 78$.
- Q63: $663 \div 17$, key 39. Options 39, 3.9 (point), 646 (reverse: $663 - 17$), 38 (slip). Check: $17 \times 39 = 680 - 17 = 663$; and $663 = 3 \times 13 \times 17$, so $663 \div 17 = 3 \times 13 = 39$.
- Q61: $11 \times 38$, key 418. Options 418, 318 (slip), 4180 (point), 49 (reverse: $11 + 38$). Check: $380 + 38 = 418$; and $11 \times 40 - 11 \times 2 = 440 - 22 = 418$.

If the layout changes, rerun the engine for seed 1 and record the new Q2, Q61 and Q63 in the report. The playthrough checks that one seed repeats.

**Authored items: the 16 the generator cannot make.** Four-option `choice`, `"shuffle": true`, `layout: "grid"`, `tags` `["arith-decimal"]`, `["arith-fraction"]` or `["arith-percent"]`, `pace: 6`, `skills` `["mp-speed"]` for decimals and `["mp-fractions"]` for the rest. `difficulty` 2 in block A, 3 in B and C, 4 in D. Question text is the bare sum in KaTeX, as generated items show it. Fractions appear as `\tfrac{a}{b}` in lowest terms; decimals as decimals.

Distractor rules: exactly three near misses, each positive, distinct, within a factor of ten of the key, and each one named slip.

- Decimals: misplaced point (times or over ten), the reverse operation, a slipped digit.
- Fractions: added the tops and the bottoms, the wrong operation, one fraction scaled by the wrong factor.
- Percentages: the complement, a dropped part (30% for 35%), a misplaced point.

Worked authored items (use these four as written; the script draws the other twelve):

| Q | Item | Key | Distractors and `why` | Computed twice |
| --- | --- | --- | --- | --- |
| Q10 (A) | $0.4 \times 35$ | 14 | 15 (slipped the units digit); 140 (moved the point); 87.5 (divided: $35 \div 0.4$) | $35 \times 4 = 140$, over ten is 14; $0.4 \times 35 = 0.4 \times 30 + 0.4 \times 5 = 12 + 2$ |
| Q65 (D) | $\tfrac56 + \tfrac38$ | $\tfrac{29}{24}$ | $\tfrac47$ (added tops and bottoms); $\tfrac{11}{24}$ (subtracted); 1 (scaled $\tfrac56$ by 3, not 4, to $\tfrac{15}{24}$) | $\tfrac{20}{24} + \tfrac{9}{24}$; and $\tfrac{5 \cdot 8 + 3 \cdot 6}{48} = \tfrac{58}{48} = \tfrac{29}{24}$ |
| Q70 (D) | $35\%$ of 260 | 91 | 169 (the 65% left over); 78 (dropped the 5%); 9.1 (moved the point) | $26 \times 3 + 13 = 91$; $0.35 \times 260 = 91$ |
| Q75 (D) | $3.6 \div 0.12$ | 30 | 31 (slipped the units digit); 300 (moved the point); 0.432 (multiplied) | $0.12 \times 30 = 3.6$; $360 \div 12 = 30$ |

The authored script is `fixed_arith.py`, `random.Random(80)` (the seed `l12-mock-test` used). Reuse `make()` from `docs/reports/mental-pressure-3-scripts/mockgen.py` for the `dec`, `frac` and `pct` kinds, but record each distractor's kind as it is made, so each `why` names the right slip. Ranges by block: A one-place decimals times a digit, unlike denominators where one divides the other, 10%, 20%, 25% or 50%; D division by a two-place decimal, denominators with a common multiple up to 24, 35%, 45%, 12.5% or 75%. Assert every distractor rule above.

**Why no versions.** 64 of the 80 questions are drawn afresh per sitting from a stored seed, so a resat differs where it matters most. The 16 authored items repeat, with their options shuffled. That is accepted: they are 20% of the paper and spread one in five. The report raises an inbox bullet asking the generator for decimal, fraction and percentage operations (an E4 extension), which would replace them.

**Feedback and explain.** Authored items: `feedback.correct` one clause ("Four tenths of 35 is 14."), `feedback.generic` the one move ("Multiply 35 by 4, then move the point one place."), `explain.text` the sum and its check in at most two sentences.

**Skills covered.** `mp-speed`, `mp-fractions`; the format practises `mp-formats`.

**Prerequisites** (cite in the report; nothing is gated): mental-pressure `l1-towards-fifty`, `l2-two-by-two`, `l3-big-division`, `l4-decimals-fast`, `l5-which-fraction`, `l6-percent-of-percent`, `l9-eighty-in-eight`, `l12-mock-test`, `l13-negative-marking`.

**Acceptance.** The common checks, plus: the start card says 80 questions, 8 minutes, no going back, generated afresh and pass 55 net; `#exam/mock-oa-arith/1` shows Q2, Q61 and Q63 as above; a forward step is refused without an answer (the playthrough checks this); every authored key is asserted two ways in `fixed_arith.py`; report at `docs/reports/exam-mock-oa-arith.md`.

## mock-oa-sig

**Files.** Three fixed versions, because E3 is not built: `app/content/exams/mock-oa-sig.json`, `mock-oa-sig-2.json` and `mock-oa-sig-3.json`. All three share the positions, families and difficulty below; only the numbers change. `content/prep.json` names only `mock-oa-sig`; the report proposes adding the other two to the firm path.

- `id`: `mock-oa-sig`, `mock-oa-sig-2`, `mock-oa-sig-3`
- `name`: `Quantitative evaluation`, then `Quantitative evaluation, version 2` and `version 3`
- `style`: `trader`
- `models` (all three): `Reported, as of Nov 2026: SIG's Quantitative Evaluation, 17 questions in 60 minutes with a calculator, rising from quick expected values to multi-stage Bayes and ruin.`
- `skills`: `{ "pz-expectation": "Expected value puzzles", "pz-conditioning": "Conditioning puzzles", "pz-recursion": "First-step analysis", "pz-games": "Games and betting", "bz-search": "Weighing and search" }`

**Description:**

> This is the reported format of SIG's Quantitative Evaluation, as candidates described it by Nov 2026. You have 17 questions in 60 minutes. A calculator is allowed, but the app has none, so have a basic one ready. The questions start with quick expected values and end with multi-stage Bayes and gambler's ruin. Some take a choice, others a number to three decimal places. A wrong answer scores 0, and you may change answers until you submit. Other reports give 16 questions in 20 minutes; this mock follows the longer one. This is version 1 of 3.

(Versions 2 and 3 end "version 2 of 3" and "version 3 of 3".)

**Parts.** One paper `quant`, name `Quantitative evaluation`: `minutes: 60`, `scoring: { "right": 1, "wrong": 0, "blank": 0 }`, `passNet: 11` (of 17), free navigation (no `navigation` key). Reports do not mention negative marking or a forward-only rule. No check part: a calculator is allowed.

**Item design.** 17 positions, the same in every version. Difficulty: 4 at 2, 5 at 3, 6 at 4, 2 at 5. `pace` is 90 s at difficulty 2, 180 at 3, 240 at 4 and 360 at 5, which sums to $360 + 900 + 1440 + 720 = 3420$ s, 57 minutes. Choices have four options and `"shuffle": true`. Numeric items ask for three decimal places, with `"tol": { "abs": 0.005 }`, and list the named wrong values in `wrong` so feedback can name the slip. Money in £ to two places.

| Pos | Diff | Tag (family) | Skill | Widget | Template | Parameter pool for versions 2 and 3 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | `dice-ev` | pz-expectation | choice | Fair n-sided die pays £ the face squared; fair price? | n in 4, 6, 8 |
| 2 | 2 | `linearity` | pz-expectation | choice | k cards from a deck; expected number of a suit or of aces | k in 5, 8, 13; suit or rank |
| 3 | 2 | `ev-fee` | pz-expectation | choice | Pay £c, receive £ the face if it is even (or at least 4); expected profit | c in 2, 3, 4 |
| 4 | 2 | `indicator` | pz-expectation | choice | Expected adjacent HH pairs in n tosses | n in 10, 13, 21 |
| 5 | 3 | `at-least-one` | pz-conditioning | numeric | At least one six in n rolls | n in 3, 4, 5 |
| 6 | 3 | `cards-conditional` | pz-conditioning | choice | Two cards; both aces (or both hearts) given at least one | ace, king, heart |
| 7 | 3 | `binomial` | pz-conditioning | choice | Exactly k heads in n fair tosses | (n, k) in (6, 3), (5, 2), (8, 4) |
| 8 | 3 | `weighing` | bz-search | choice | N coins, one heavier, a balance; fewest weighings that always find it | N in 10, 28, 80 |
| 9 | 3 | `bayes` | pz-conditioning | numeric | Base rate b, test sensitivity s, false-positive rate f; P(condition given positive) | b in 1%, 2%, 5%; s in 90%, 95%; f in 5%, 10% |
| 10 | 4 | `waiting-time` | pz-recursion | choice | Expected tosses until a pattern | HH, HTH, HHH |
| 11 | 4 | `stopping` | pz-recursion | choice | Die game with r rerolls allowed; value under the best rule | r in 1, 2; 6 or 8 faces |
| 12 | 4 | `max-of-draws` | pz-expectation | numeric | E[max] or E[min] of two fair dice | max, min; 6 or 8 faces |
| 13 | 4 | `bayes-multi` | pz-conditioning | choice | m fair coins and one two-headed; pick one, k heads in a row; P(two-headed) | m in 3, 4; k in 3, 4 |
| 14 | 4 | `bayes-multi` | pz-conditioning | numeric | Item 9's test taken twice, independently, both positive | as item 9 |
| 15 | 4 | `ruin-fair` | pz-games | choice | Fair £1 bets from £i until £0 or £N; expected number of bets | (i, N) in (3, 10), (2, 8), (4, 9) |
| 16 | 5 | `ruin-biased` | pz-games | numeric | Win each £1 bet with chance p, from £i until £0 or £N; P(reach £N) | p in 0.55, 0.6, 2/3; (i, N) in (2, 5), (3, 6) |
| 17 | 5 | `bayes-ruin` | pz-games | numeric | A coin is fair or biased to p, equally likely; bet on heads from £1 until £0 or £3; given you reached £3, P(biased) | p in 2/3, 3/4, 0.6 |

Distractor rules (choice) and `wrong` values (numeric), by family: the square of the mean for a mean of squares; one card or one toss in place of all; the complement; $n \times p$ for "at least one"; with replacement for without; one order only for a binomial; halving ($\lceil \log_2 N \rceil$) for weighing; the hit rate, the base rate, or true positives over everyone for Bayes; the prior alone, or equal priors, for multi-stage Bayes; $N - i$ or $iN$ for ruin duration; the fair answer $i/N$ for biased ruin; the stage-one answer for a two-stage question. No two options within 0.01 of each other, and no numeric `wrong` value within the tolerance of the key.

**Version 1, worked** (use these parameters as written for version 1; the script asserts each two ways):

- Pos 1: six-sided die, £ the face squared. Key $\tfrac{91}{6}$, £15.17. Distractors £12.25 (squared the mean, $3.5^2$), £3.50 (forgot to square), £91 (did not divide by 6). Twice: $(1 + 4 + 9 + 16 + 25 + 36)/6 = 91/6$; and $Var + \text{mean}^2 = \tfrac{35}{12} + \tfrac{49}{4} = \tfrac{35 + 147}{12} = \tfrac{182}{12} = \tfrac{91}{6}$.
- Pos 3: pay £3, receive £ the face if it is even. Key −£1.00. Distractors +£1.00 (averaged over the even faces only), +£0.50 (paid out the face on every roll, $3.5 - 3$), −£3.00 (counted only the fee). Twice: $(2 + 4 + 6)/6 - 3 = 2 - 3$; and $\tfrac12 \times 4 - 3 = -1$.
- Pos 9: 1%, 95%, 5%. Key $\tfrac{19}{118}$, 0.161. `wrong`: 0.95 (the hit rate), 0.0095 (true positives over everyone), 0.01 (the base rate). Twice: $\tfrac{0.0095}{0.0095 + 0.0495}$; and in 10,000 people, 95 true and 495 false positives, $\tfrac{95}{590} = \tfrac{19}{118}$.
- Pos 11: six-sided die, one reroll. Key £4.25 (keep 4, 5 or 6). Distractors £3.50 (never reroll), £4.17 (kept only 5 or 6: $\tfrac{25}{6}$), £5.00 (assumed a kept face is always high). Twice: $\tfrac{4 + 5 + 6}{6} + \tfrac36 \times 3.5 = 2.5 + 1.75$; and $\tfrac16 \sum \max(x, 3.5) = \tfrac{3.5 \times 3 + 15}{6} = \tfrac{25.5}{6} = 4.25$.
- Pos 13: three fair coins and one two-headed, three heads. Key $\tfrac{8}{11}$. Distractors $\tfrac14$ (the prior alone), $\tfrac89$ (treated both kinds as equally likely), $\tfrac78$ (one minus the fair coin's chance). Twice: $\tfrac{1/4}{1/4 + 3/4 \cdot 1/8} = \tfrac{8/32}{11/32}$; and odds $\tfrac13 \times 8 = \tfrac83$, so $\tfrac{8}{11}$.
- Pos 14: 1%, 95%, 5%, two positives. Key $\tfrac{361}{460}$, 0.785. `wrong`: 0.161 (one test only), 0.903 ($0.95^2$). Twice: odds $\tfrac{1}{99} \times 19^2 = \tfrac{361}{99}$, so $\tfrac{361}{460}$; and $\tfrac{0.01 \times 0.95^2}{0.01 \times 0.95^2 + 0.99 \times 0.05^2}$, the same.
- Pos 15: from £3 until £0 or £10. Key 21 bets. Distractors 7 ($N - i$), 30 ($iN$), 49 (squared the distance to £10). Twice: $i(N - i) = 3 \times 7$; and a linear solve of $D_k = 1 + \tfrac12(D_{k+1} + D_{k-1})$ with $D_0 = D_{10} = 0$.
- Pos 16: $p = 0.6$, from £2 until £0 or £5. Key $\tfrac{135}{211}$, 0.640. `wrong`: 0.400 (the fair answer $\tfrac25$), 0.216 (three wins in a row, $0.6^3$), 0.600 (one bet). Twice: with $r = \tfrac23$, $\tfrac{1 - r^2}{1 - r^5} = \tfrac{5/9}{211/243} = \tfrac{135}{211}$; and shooting $P_{k+1} = (P_k - qP_{k-1})/p$ from $P_0 = 0$, scaled to $P_5 = 1$.
- Pos 17: fair or $p = \tfrac34$, from £1 until £0 or £3. Key $\tfrac{27}{40}$, 0.675. `wrong`: 0.513 (stopped at P(reach £3) $= \tfrac{20}{39}$), 0.692 (P(reach) for the biased coin, $\tfrac{9}{13}$), 0.500 (the prior). Twice: $\tfrac{\tfrac12 \cdot \tfrac{9}{13}}{\tfrac12(\tfrac13 + \tfrac{9}{13})} = \tfrac{27}{40}$; and the ruin values $\tfrac13$ and $\tfrac{9}{13}$ by the same linear solve as pos 16, then $\tfrac{9/13}{1/3 + 9/13} = \tfrac{27}{40}$.

Other version-1 keys, for the script to reproduce: pos 2 (five cards, hearts) $\tfrac54$; pos 4 (10 tosses) $\tfrac94$; pos 5 ($n = 4$) $\tfrac{671}{1296}$, 0.518; pos 6 (aces) $\tfrac{1}{33}$; pos 7 $\tfrac{5}{16}$; pos 8 ($N = 10$) 3; pos 10 (HH) 6; pos 12 (max, six faces) $\tfrac{161}{36}$, 4.472.

**Generation.** `gen_sig.py`, seeds 1701, 1702 and 1703 for versions 1 to 3. Version 1 takes the parameters above as a `FIXED` override; versions 2 and 3 draw from the pools with `random.Random(seed)`, and no position repeats version 1's parameters. Each key is computed by a closed form and by a second method (enumeration over dice and cards, a linear solve with `Fraction`s for waiting times and ruin), with `assert`. The script writes the three files and prints a key table for the report.

**Feedback and explain.** `feedback.correct` names the move ("Three in ten bets: £3 of £10."); `feedback.generic` gives the first step; `explain.text` shows the calculation in at most three sentences, with the second check where it is short.

**Skills covered.** `pz-expectation`, `pz-conditioning`, `pz-recursion`, `pz-games`, `bz-search`.

**Prerequisites:** puzzles `l1-dice-games`, `l3-waiting-for-hh`, `l4-indicator-tricks`, `l6-when-to-stop`, `l7-cards-and-colours`, `l9-bayes-in-a-minute`, `l10-ruin-in-interviews`, `l11-largest-of-several`, `l24-mixed-set`; brainteasers `l4-weighing-coins`; mental-pressure `l15-probability-at-speed`.

**Acceptance.** The common checks for all three files; the start card says 17 questions, 60 minutes and pass 11; each version has the 4, 5, 6, 2 difficulty split and the 17 families in order; the three versions share no parameter set at any position; report at `docs/reports/exam-mock-oa-sig.md`.

## mock-oa-trader

**Files.** Three fixed versions, because E3 is not built: `app/content/exams/mock-oa-trader.json`, `mock-oa-trader-2.json` and `mock-oa-trader-3.json`, with the same papers and positions. `content/prep.json` names only `mock-oa-trader`; the report proposes the other two.

- `id`: `mock-oa-trader`, `mock-oa-trader-2`, `mock-oa-trader-3`
- `name`: `Trader test battery`, then `Trader test battery, version 2` and `version 3`
- `style`: `trader`
- `models` (all three): `Reported, as of Nov 2026: the Optiver, IMC and Citadel Securities test batteries: number sequences, probability at speed, and likelihood ranking with intervals.`
- `skills`: `{ "mp-formats": "Test formats", "mp-estimate": "Fast estimation", "mp-fractions": "Fractions and percentages at speed", "pz-conditioning": "Conditioning puzzles" }`

**Description:**

> These are reported formats from the Optiver, IMC and Citadel Securities test batteries, as described by Nov 2026. There are three papers, each on its own clock. Sequences is 15 questions in 25 minutes, one at a time, with no skipping. Probability at speed is 15 questions in 30 minutes; you may move between them. Likelihood ranking and intervals is 10 questions in 10 minutes. Wrong answers score 0, and no calculator is allowed. Firms mix and rename these papers, so expect a different order on the day. This is version 1 of 3.

**Parts.**

1. Paper `sequences`, name `Number sequences`: `minutes: 25`, 15 items, `scoring: { "right": 1, "wrong": 0, "blank": 0 }`, `passNet: 10`, `navigation: "forward"`, `skip: false` (the reported no-skip sequence test, plan E2).
2. Paper `probability`, name `Probability at speed`: `minutes: 30`, 15 items, the same scoring, `passNet: 10`, free navigation.
3. Paper `ranking`, name `Likelihood ranking and intervals`: `minutes: 10`, 10 items, the same scoring, `passNet: 6`, free navigation.
4. Check `no-calculator`, name `I used no calculator`, detail `Tick this only if you sat all three papers without one.`

**Paper A, sequences: 15 items.** Four-option `choice`, `"shuffle": true`, `pace: 100` (1,500 s is 25 minutes), tag `sequence` then the rule family (for example `["sequence", "times-plus"]`), skill `mp-formats`. The question shows the terms and a `?`. Ramp: Q1 to Q3 at 2, Q4 to Q8 at 3, Q9 to Q13 at 4, Q14 and Q15 at 5.

| Q | Rule family | Q | Rule family | Q | Rule family |
| --- | --- | --- | --- | --- | --- |
| 1 | `arithmetic` | 6 | `alternating` (×k then −c) | 11 | `cubes` (n³ ± c) |
| 2 | `geometric` (×2 or ×3) | 7 | `fibonacci` (sum of two before) | 12 | `interleaved` (a different ×k in each place) |
| 3 | `squares` (n² ± c) | 8 | `interleaved` (two arithmetic) | 13 | `consecutive-products` (n(n + 1)) |
| 4 | `times-plus` (×2 ± c) | 9 | `digit-sum` (add the digit sum) | 14 | `rising-multiplier` (n·aₙ + 1) |
| 5 | `second-diff` (gaps grow) | 10 | `primes` (pₙ or pₙ + n) | 15 | `tribonacci` (sum of three before) |

Rules: every sequence shows five to seven terms, enough that only one simple rule fits; terms stay under 1,000 except Q14 and Q15. Distractors come from wrong rules: carry on the last gap, double the last term, apply only one of two rules, and an off-by-one of the key. Each `why` names the rule the learner used. The script tests that no second template from the table also fits the shown terms.

Worked (version 1):

- Q4: 3, 5, 9, 17, 33, ? Key 65 (×2 then −1). Distractors 49 (repeated the last gap of 16), 66 (doubled 33), 64 (subtracted 2, not 1). Twice: $2 \times 33 - 1 = 65$; the gaps 2, 4, 8, 16 double, so the next is 32 and $33 + 32 = 65$.
- Q12: 1, 10, 3, 20, 9, 40, 27, ? Key 80 (even places double, odd places ×3; the eighth term is an even place). Distractors 81 (applied the odd-place rule), 54 (doubled 27), 67 (added the last two terms). Twice: 10, 20, 40, 80 by doubling; and $10 \times 2^3 = 80$.
- Q14: 1, 2, 5, 16, 65, ? Key 326 ($a_{n+1} = n \cdot a_n + 1$). Distractors 325 (×5 without the +1), 261 (kept the multiplier at 4), 391 (raised the multiplier by 2). Twice: $5 \times 65 + 1 = 326$; and the chain $1 \cdot 1 + 1 = 2$, $2 \cdot 2 + 1 = 5$, $3 \cdot 5 + 1 = 16$, $4 \cdot 16 + 1 = 65$ confirms the rule.

**Paper B, probability at speed: 15 items.** Four-option `choice`, `"shuffle": true`, `pace: 120`, skills `pz-conditioning` or `mp-fractions`. Keys as fractions in lowest terms (KaTeX `\tfrac`). Ramp: Q1 to Q4 at 2, Q5 to Q10 at 3, Q11 to Q14 at 4, Q15 at 5. Families (tags), in order: `dice-sum`, `binomial`, `at-least-one`, `cards-conditional`, `same-suit`, `reroll-ev`, `distinct-days`, `first-success`, `committee`, `urn`, `natural-frequency`, `max-of-dice`, `given-the-total`, `first-to-six`, `pattern-race`. Distractors carry the slips `gen17.py` labels: each total equally likely, the complement, counted ordered pairs twice, $n \times p$, every roll a six, with replacement, one named suit, one order only, $k/n$, the hit rate, the base rate, ignored the reroll.

Worked (version 1):

- Q1: two dice, total 9. Key $\tfrac19$. Distractors $\tfrac{1}{11}$ (each total equally likely), $\tfrac89$ (the complement), $\tfrac29$ (counted each pair twice). Twice: (3, 6), (4, 5), (5, 4), (6, 3) is 4 of 36; and enumeration of all 36.
- Q3: a die rolled three times, at least one six. Key $\tfrac{91}{216}$. Distractors $\tfrac12$ ($3 \times \tfrac16$), $\tfrac{125}{216}$ (the complement), $\tfrac{1}{216}$ (every roll a six). Twice: $1 - (\tfrac56)^3$; and enumeration of 216 outcomes.
- Q11: 5% of traders have an edge; a screen flags 90% of them and 10% of the rest. Key $\tfrac{9}{28}$. Distractors $\tfrac{9}{10}$ (the hit rate), $\tfrac{9}{200}$ (true positives over everyone), $\tfrac{1}{20}$ (the base rate). Twice: in 1,000 traders, 45 true and 95 false flags, $\tfrac{45}{140}$; and $\tfrac{0.05 \times 0.9}{0.05 \times 0.9 + 0.95 \times 0.1}$.
- Q13: two dice total 8; at least one shows 6. Key $\tfrac25$. Distractors $\tfrac{11}{36}$ (ignored the total), $\tfrac13$ (listed unordered pairs as equally likely), $\tfrac{1}{18}$ (did not condition: $\tfrac{2}{36}$). Twice: (2, 6), (3, 5), (4, 4), (5, 3), (6, 2) has 2 of 5; and enumeration.
- Q14: you and a friend roll a die in turn, you first; the first six wins. Key $\tfrac{6}{11}$. Distractors $\tfrac12$ (ignored going first), $\tfrac16$ (only your first roll), $\tfrac{5}{11}$ (the friend's chance). Twice: $\tfrac{1/6}{1 - 25/36} = \tfrac{6}{11}$; and the series $\tfrac16 \sum (\tfrac{25}{36})^k$.
- Q15: toss a coin until HH or TH appears; P(HH first). Key $\tfrac14$. Distractors $\tfrac12$ (by symmetry of the patterns), $\tfrac34$ (the complement), $\tfrac13$ (three cases). Twice: TH comes first unless the first two tosses are HH; and enumeration of 12-toss sequences gives 0.250.

**Paper C, ranking and intervals: 10 items.** Q1 to Q6 rank three events by likelihood; Q7 to Q10 are intervals. `pace: 60`. Ramp: Q1, Q2, Q7 at 2; Q3, Q4, Q8 at 3; Q5, Q9 at 4; Q6, Q10 at 5.

- Ranking: an `order` widget, three lines, "most likely first", tags `["likelihood-ranking"]`, skill `mp-estimate`. The engine shuffles lines. Every pair of events differs by at least 0.02, and at least one event tempts the $n \times p$ or "more trials, more likely" error. `explain` gives the three probabilities to three places.
- Intervals: a four-option `choice` **without** `shuffle`, options in ascending order, tags `["interval"]`, skill `mp-estimate`. The quantity is computable, never trivia. Option rule: one narrow interval holds the value (the key); one wider interval also holds it, and its `why` says the tighter one also holds it, so it scores less on the day; two narrow intervals of the same width miss it, one either side. The question says "Choose the tightest interval that holds the value".

Worked (version 1):

- C1 (ranking): A, at least one six in 4 rolls, 0.518; B, at least one double six in 24 rolls of two dice, 0.491; C, at least 6 heads in 10 tosses, 0.377. Order A, B, C. Twice: $1 - (\tfrac56)^4 = \tfrac{671}{1296}$, $1 - (\tfrac{35}{36})^{24}$, $\tfrac{210 + 120 + 45 + 10 + 1}{1024} = \tfrac{386}{1024}$; and enumeration of 1,296 and 1,024 outcomes, plus a simulation of B (0.490 in 400,000 runs).
- C2 (ranking): A, exactly 2 heads in 4 tosses, $\tfrac38$; B, two cards of the same suit, $\tfrac{4}{17}$; C, a total of 7 on two dice, $\tfrac16$. Order A, B, C. Twice: $\tfrac{6}{16}$, $\tfrac{12}{51}$, $\tfrac{6}{36}$; and $\tfrac{13 \cdot 12 \cdot 4}{52 \cdot 51} = \tfrac{4}{17}$.
- C7 (interval): $\sqrt{300}$. Options [15, 20], [16, 17], [17, 18], [18, 19]. Key [17, 18]; [15, 20] holds it but is wider. Twice: $17^2 = 289$ and $18^2 = 324$ bracket 300; and $\sqrt{300} = 10\sqrt3 \approx 17.32$.
- C8 (interval): $1.05^{14}$. Options [1.5, 2.5], [1.7, 1.8], [1.9, 2.0], [2.0, 2.1]. Key [1.9, 2.0]. Twice: the rule of 72 gives a doubling in 14.4 years, so just under 2; and the exact value 1.9799.

**Generation.** `gen_trader.py`, seeds 2501, 2502 and 2503 for versions 1 to 3, a section per paper on the pattern of `gen17.py` (one template per position, parameters drawn, distractors labelled by slip). Version 1 uses the worked parameters above as a `FIXED` override. Each key is a `Fraction` computed two ways (closed form and enumeration); interval keys are checked by squaring or by exact `Fraction` powers; ranking gaps are asserted at 0.02 or more. The sequence section asserts that the shown terms fit no other template in the table.

**Feedback and explain.** Sequences: `feedback.correct` names the rule; `explain.text` writes the rule and the next term. Probability: the count or the formula in one line, then the second check. Ranking: the three probabilities. Intervals: the bracketing squares or the estimate, and why the wider interval scores less.

**Skills covered.** `mp-formats`, `mp-estimate`, `mp-fractions`, `pz-conditioning`.

**Prerequisites:** mental-pressure `l10-next-in-sequence`, `l16-harder-sequences`, `l14-ranking-likelihoods`, `l15-probability-at-speed`, `l13-negative-marking`, `l17-full-battery`, `l7-estimating-products`, `l8-square-roots`; puzzles `l7-cards-and-colours`, `l9-bayes-in-a-minute`; puzzles `l27-given-the-total` once it is written.

**Acceptance.** The common checks for all three files; the start card lists three papers (25, 30 and 10 minutes, 65 in all) and the check; paper A refuses a step without an answer; every ranking item's gaps are at least 0.02 and every interval item has exactly one narrowest interval that holds the value; report at `docs/reports/exam-mock-oa-trader.md`, with inbox bullets for interval scoring by width and for the bank draw (E3) that would retire the fixed versions.

## mock-superday-trader

**File.** `app/content/exams/mock-superday-trader.json`. One file, no versions. Reason: the mocks rule above (three fixed versions only while E3 is not built) was written for the online assessments, which are resat to build speed. A superday is a rehearsal sat a few times, its weight is in the written answers and the market-making games, and `docs/briefs/interview-plan.md` section (d) asks for three versions of the OAs only ("Superdays use the stage-exam shape"). The report raises one inbox bullet that E3 would let this mock draw fresh items. `content/prep.json` already lists `mock-superday-trader` (paths `superday-trader` and the trader firm paths); do not edit it.

- `id`: `mock-superday-trader`
- `name`: `Trader superday`
- `style`: `trader`
- `models` (one line, 200 characters at most; this text is 179): `Reported, as of Nov 2026: trading-firm final-round days at Jane Street, Optiver, SIG, IMC and Citadel Securities: probability, mental maths, market-making games and fit questions.`
- `skills`: `{ "pz-expectation": "Expected value puzzles", "pz-conditioning": "Conditioning puzzles", "pz-games": "Games and betting", "gm-poker": "Poker and betting decisions", "mp-speed": "Speed arithmetic", "mp-fractions": "Fractions and percentages at speed", "mp-estimate": "Fast estimation", "bz-quick": "Quick reasoning", "mg-fair": "Fair value", "mg-quote": "Quoting", "mg-update": "Updating on trades", "mg-risk": "Position and risk", "rk-behave": "Behavioural answers" }`

**Description** (plain, each sentence under 20 words; firm names stay here and in `models` only):

> This is the reported shape of a trading firm's final-round day, as candidates described it by Nov 2026. Jane Street, Optiver, SIG, IMC and Citadel Securities all report these rounds. They cover probability and betting games, mental maths, market-making games and fit questions. There are four papers, each on its own clock. Real rounds are spoken, so say each written answer aloud before you type it. Mental maths is one question at a time with no going back. No calculator is allowed. Orders and lengths differ by firm and office. Two checks at the end ask for what the app cannot see.

**Parts, in order** (every paper `scoring: { "right": 1, "wrong": 0, "blank": 0 }`; no firm reports negative marking in a final round):

| # | Paper `id`, name | Minutes | Items | Pass | Navigation | `pace` sum |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `probability`, Probability and expected value | 45 | 6 (4 choice, 2 `longform`) | `pass: 0.65` (4 of 6) | free | 2,520 s |
| 2 | `mental`, Mental maths and Fermi | 15 | 12 (8 `numeric`, 4 interval `choice`) | `pass: 0.7` (9 of 12) | `"forward"`, `skip: false` | 800 s |
| 3 | `market`, Market-making game | 30 | 4 (3 `trade`, 1 `longform`) | `pass: 0.75` (3 of 4) | free | 1,800 s |
| 4 | `fit`, Fit and motivation | 18 | 2 (both `longform`) | `pass: 0.5` (1 of 2) | free | 960 s |
| 5 | check `game-aloud`, `I played a full market-making game aloud with a partner`, detail `Tick this only if a real person played the counterparty and you spoke your reasoning at every quote.` | | | | | |
| 6 | check `why-aloud`, `I said my why-trading answer aloud in under 90 seconds`, detail `Tick this only if you timed it.` | | | | | |

That is 24 items, 108 minutes, 5 `longform`. Use `pass` (a share), not `passNet`, because no paper has negative marking. **Known engine bug, do not work around it in content:** the results page may print "Pass mark NaN%" on a multi-paper mock (inbox bullets from `mock-oa-trader`). The attempt passes only when every paper passes and both checks are ticked.

**What the engine allows, said plainly (checked in `app/tools/validate.mjs` and `app/js/engine/widgets/trade.js`, and by `content/exams/mock-trade-sample.json`, which plays green).**

- A `trade` widget **may** sit in an exam paper, as the whole `widget` of one item, over an `orderbook` canvas (the validator warns without it). The mock validator checks it like any other item: all trade fields, and the authored `strategy` is replayed through the widget's own game and must meet the target with no rule break. The start card and the playthrough treat it as one item.
- The author **may** use `noise`, `informed` and `scripted` counterparties, a `schedule` of cards, `limit`, `spread`, and either `benchmark` or `band`. A trade item is graded right or wrong (target met and breaks within `maxBreaks`) and scores the paper's `right` mark. It cannot score by P&L, and `scoring` is per paper, so every item counts one mark.
- The author **may not** use `carry` to read a learner's earlier P&L (an exam draws every item at once, so a later item cannot read it); any debrief item uses fixed numbers from the model run. Do not put `carry` on a trade item (it would store a value nothing reads). Do not set `timed`. Every trade needs `strategy`, one entry per turn.
- `longform` **is** allowed in a mock (`allowLongform`): `{ "kind": "longform", "prompt", "model", "rubric": [ { "points", "text" } ] }` with points summing to 10, no `widget`. In an exam the button reads "Mark my answer"; the learner ticks the rubric and 7 or more counts as right. Give each a `difficulty`, `skills`, `tags` and `pace` like any item.
- Spoken answers (plan E10) were dropped (DECISIONS, 29 Oct): there is no microphone, speak mode or recording. The description says to speak aloud first, the two checks cover the spoken part, and the report says the plan's "recorded" wording is replaced by this.

**Rules.** Firm names only in `models` and `description`, with "reported" and "Nov 2026". Elsewhere say "a trading firm" or "the interviewer". Our own wording and numbers. Every stated number computed twice, as `Fraction`s, with an `assert`. Every `choice` carries `"shuffle": true`, interval choices included (DECISIONS, "Numeric distractors"); every distractor has a `why` naming the learner's action; no item puts the key between a times-ten pair or between two equal slips (DECISIONS, "Distractors (4 Nov)"; the rule applies to options a learner sees, not to numeric `wrong` values). Voice as the shared rules. Every item has `tags` (family first), `pace`, `skills`.

**No duplicates.** The script must hold the families and keys of all three `mock-oa-trader` versions and `mock-oa-sig`, read from their JSON, and assert that no question text, family tag or key-plus-question pair here repeats one there. Families already taken, so avoid them: `dice-ev`, `linearity`, `ev-fee`, `indicator`, `at-least-one`, `cards-conditional`, `binomial`, `weighing`, `bayes`, `waiting-time`, `stopping`, `max-of-draws`, `bayes-multi`, `ruin-fair`, `ruin-biased`, `bayes-ruin`, `dice-sum`, `same-suit`, `reroll-ev`, `distinct-days`, `first-success`, `committee`, `urn`, `natural-frequency`, `max-of-dice`, `given-the-total`, `first-to-six`, `pattern-race`, `likelihood-ranking`, `interval`, `sequence` (and its rule families). The `interval` tag is reused here for the Fermi items: change it to `fermi-interval` so no family matches.

### Paper 1: probability and expected value (45 min, 6 items)

Final-round questions are harder and arrive with follow-ups, so items 5 and 6 are talk-through answers.

| Q | Diff | Family tag | Kind | Pace | Skill | Draws on | Idea |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 3 | `coupon-collector` | choice | 300 | pz-expectation | puzzles `l2-every-coupon` | Expected rolls of a fair die until every face has appeared |
| 2 | 3 | `fixed-points` | choice | 300 | pz-conditioning | puzzles `l5-hats` | Four hats returned at random: chance nobody gets their own |
| 3 | 4 | `kelly` | choice | 360 | pz-games | puzzles `l21-kelly` | Even-money bet won with chance 0.6: fraction of bankroll to stake to maximise log growth |
| 4 | 4 | `fair-from-biased` | choice | 360 | pz-expectation | puzzles `l25-fair-from-biased` | Coin with heads 0.3: toss in pairs until HT or TH; expected tosses |
| 5 | 5 | `card-stopping` | longform | 600 | pz-games | puzzles `l20-betting-on-sequences`, `l24-mixed-set` | Shuffled 26 red, 26 black deck; stop at any time and bet £1 on the next card being red; value and how to play |
| 6 | 4 | `pot-odds` | longform | 600 | gm-poker | game-theory `l11-pot-odds` | Pot £100, opponent bets £50, you win 30% if called: call or fold, then how often must a bet be a bluff |

**Worked keys (use as written; the script asserts each two ways).**

- Q1: key $\tfrac{147}{10}$, 14.7 rolls. Distractors 36 (waited for each face as if it were the last face, $6 \times 6$), 2.45 (the harmonic number without the factor 6), 8.7 (stopped when five faces had appeared, $14.7 - 6$). Twice: $6\left(1 + \tfrac12 + \tfrac13 + \tfrac14 + \tfrac15 + \tfrac16\right)$; and the stage waits $1 + \tfrac65 + \tfrac64 + \tfrac63 + \tfrac62 + 6$ as `Fraction`s. Add a Markov solve on "faces seen" if cheap.
- Q2: key $\tfrac38$. Distractors $\tfrac58$ (the chance somebody does, the complement), $\tfrac{81}{256}$ (each hat independent, $(\tfrac34)^4$), $\tfrac14$ (one named person only). Twice: inclusion-exclusion $1 - 1 + \tfrac12 - \tfrac16 + \tfrac1{24} = \tfrac{9}{24}$; and enumeration of the 24 permutations, 9 with no fixed point.
- Q3: key 20%. Distractors 60% (stake the win chance), 10% (half the edge), 100% (maximise the expected value, not the log). Twice: $f = p - q = 0.2$ for an even-money bet; and a grid search of $0.6 \ln(1+f) + 0.4 \ln(1-f)$ in 1% steps peaks at 20% (growth 0.0201 a bet).
- Q4: key $\tfrac{100}{21}$, 4.76 tosses. Distractors 2.38 (counted pairs, not tosses, $\tfrac{50}{21}$), 3.33 (waited for a head, $1/0.3$), 1.43 (waited for a tail, $1/0.7$). Twice: a pair succeeds with $2 \times 0.3 \times 0.7 = 0.42$, so $2 / 0.42$ tosses; and a linear solve over the two states "start" and "failed pair" gives $\tfrac{1}{0.21}$. Note that 2.38 and the key differ by a factor of 2 on one side only, so the rule holds.
- Q5 (longform). Model: the chance the next card is red is $\tfrac{r}{r+b}$ and the fair-bet value at any moment is $\tfrac{r-b}{r+b}$, a martingale, so every stopping rule has expected gain £0 (optional stopping). Check by recursion on small decks. Script: the value of "stop now or wait" over states $(r, b)$ with a forced bet by the last card, as `Fraction`s: $V(3,3) = V(26,26) = 0$ and $V(2,1) = \tfrac13$ for one state. Follow-up in the model: if you may stake anything from £0 to £1 on every card, you win in expectation; with one red and one black card the stakes £0 then £1 give £1. Rubric (10): states the question is whether any stopping time helps (1); next card red has probability equal to the red share (1); the stopping value is the red-minus-black share (2); sees the fair-game or symmetry argument that the bet has expected gain 0 whenever you stop (3); checks a small deck by enumeration (1); answers £0 for the single bet (1); names what changes with variable stakes and gives the two-card example (1).
- Q6 (longform). Model: calling costs £50 to win the £150 already in the pot, so the break-even equity is $\tfrac{50}{200} = 25\%$; at 30% the call earns $0.3 \times 150 - 0.7 \times 50 = +£10$. For the follow-up, if a share $x$ of bets are bluffs you win $x \times 150 - (1 - x) \times 50$, which is 0 at $x = \tfrac14$. Twice: pot odds against the EV sum; and $200 \times 0.3 - 50 = 10$. Rubric (10): the price of the call and what it wins (2); break-even equity 25% by a stated formula (2); EV +£10 and the decision to call (2); says the 30% is an estimate and what would change it (1); the bluff frequency $\tfrac14$ with a reason (2); reasons aloud in order and ends with a clear action (1).

For each `longform` write `model` as the spoken answer an interviewer would hope for in at most 150 words, with the follow-up built in. `feedback` is not used on a longform; the model and rubric carry it.

### Paper 2: mental maths and Fermi (15 min, 12 items)

Forward only, no skipping, because these are asked one at a time with no paper. Q1 to Q8 are `numeric` (exact, or `tol` as stated), `pace: 40`, skills `mp-speed` or `mp-fractions`, tags as shown; Q9 to Q12 are interval `choice` items, `pace: 120`, skill `mp-estimate`, tag first `fermi-interval`. Each `numeric` lists the named wrong values in `wrong` so feedback names the slip.

| Q | Diff | Tag | Item | Key | `wrong` (slip) | Computed twice |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | `percent-of` | 13% of 760 | 98.8 (`tol` abs 0.05) | 9.88 (moved the point); 76 (took 10% only) | $76 + 22.8$; $0.13 \times 760 = 494/5$ |
| 2 | 3 | `difference-of-squares` | $47 \times 53$ | 2491 | 2500 (forgot the $-9$); 2209 (squared 47) | $50^2 - 3^2$; direct product |
| 3 | 3 | `two-by-two` | $38 \times 26$ | 988 | 1040 (rounded 38 to 40); 948 (slipped a digit) | $38 \times 25 + 38$; $40 \times 26 - 2 \times 26$ |
| 4 | 2 | `fraction-sum` | $\tfrac18 + \tfrac1{12}$ as a decimal to 3 places | 0.208 (`tol` abs 0.0005) | 0.100 (added tops and bottoms, $\tfrac{2}{20}$); 0.010 (multiplied the fractions, $\tfrac1{96}$) | $\tfrac{3}{24} + \tfrac{2}{24} = \tfrac5{24}$; $0.125 + 0.0833$ |
| 5 | 3 | `compound` | $1.06^{12}$ to 2 places, within 0.03 | 2.01 (`tol` abs 0.03) | 1.72 (added $12 \times 6\%$) | rule of 72 gives a doubling; $1.06^{12} = 2.0122$ by squaring |
| 6 | 2 | `gauss-sum` | $1 + 2 + \dots + 120$ | 7260 | 7140 (stopped at 119); 14520 (forgot to halve) | $\tfrac{120 \times 121}{2}$; 60 pairs of 121 |
| 7 | 3 | `last-digit` | Last digit of $7^{2026}$ | 9 | 3 (used $2027 \bmod 4$); 7 (read the exponent as 1 mod 4) | cycle 7, 9, 3, 1 and $2026 \bmod 4 = 2$; `pow(7, 2026, 10)` |
| 8 | 2 | `net-percent` | Up 40%, then down 25%: net change in % | 5 | 15 (added the changes); 10 (took 40% of 25%) | $1.4 \times 0.75 = 1.05$; start at 100: 140, then 105 |

The script asserts every `wrong` value is outside the `tol` of the key.

**Fermi, Q9 to Q12.** Each question states every figure it needs, so the value is computable and never trivia, and ends "Choose the tightest interval that holds your estimate." The four options follow the `mock-oa-trader` paper C rule: one narrow interval holds the value (the key); one wider interval also holds it, and its `why` says the tighter one also holds it, so it scores less on the day; two narrow intervals of the key's width miss it, one adjacent and one a full width away, the side varying by item. `shuffle: true`.

| Q | Diff | Tag (after `fermi-interval`) | Question, with figures | Value | Key and options | Computed twice |
| --- | --- | --- | --- | --- | --- | --- |
| 9 | 3 | `stack-of-coins` | A coin is 2.5 mm thick. How tall, in km, is a stack of 1,000,000? | 2.5 km | key 2.0 to 3.0; wide 1.0 to 4.0; misses 3.0 to 4.0 and 0.0 to 1.0 | $10^6 \times 2.5$ mm = 2,500 m; 1,000 coins is 2.5 m, times 1,000 |
| 10 | 4 | `balls-in-a-room` | A room is 4 m by 5 m by 2.5 m. Balls 6.5 cm across fill 64% of it. How many, in thousands? | 222.5 | key 200 to 250; wide 100 to 400; misses 250 to 300 and 100 to 150 | $\tfrac{0.64 \times 50}{\tfrac43 \pi (0.0325)^3}$; $\tfrac{0.64 \times 50\,\text{m}^3}{(\pi/6) \times 0.065^3}$ |
| 11 | 3 | `heartbeats` | A heart beats 70 times a minute. Beats in 80 years, in billions? (1 year = 365.25 days) | 2.945 | key 2.8 to 3.0; wide 2.0 to 4.0; misses 3.0 to 3.2 and 2.4 to 2.6 | $70 \times 60 \times 24 \times 365.25 \times 80$; per year 36.8 million, times 80 |
| 12 | 3 | `quote-rate` | A desk quotes 4 markets, each updated twice a second, for 6.5 hours. Updates in a day, in thousands? | 187.2 | key 180 to 190; wide 100 to 300; misses 190 to 200 and 160 to 170 | $4 \times 2 \times 6.5 \times 3600$; per hour 28,800, times 6.5 |

Check the distractor rule on Q11 and Q12 after generating (the key must not sit between two equal slips: one miss adjacent, the other a width away). Each `explain` shows the product and says why the wider interval holds but scores less.

### Paper 3: market-making game (30 min, 4 items)

Three `trade` items, each over an `orderbook` canvas (`params`: three levels a side around `fair`, `currency: "£"`, `showMid: true`, `state: {}`, as `mock-trade-sample.json`), then a debrief. The prose of each says what the quantity is, how a turn works and that the interviewer may know more than you. `question` states the target. Every spec below was played in node through `app/js/engine/widgets/trade.js` (`play(widget, strategy)`): the strategy meets the target and the untouched opening quote fails, so the validator warns about neither. If the author changes a number, rerun `play` for both and keep the margin.

Shared: `tick: 0.5`, `currency: "£"`, `maxBreaks: 0`, `dp: 1`. `feedback.byKey` for `low`, `limit`, `crossed`, `spread` as the widget needs, each naming the learner's action ("You kept the same ask after the news, so the informed trader bought it cheap."). Games are `pace` 420 s (items 1 and 3) and 480 s (item 2).

**Q1, `three-dice`** (diff 3, skills `mg-fair`, `mg-update`; draws on mm-games `l2-dice-sum`, `l13-full-game`). Three fair dice, the total settles the game; fair opens at 10.5.
`seed 23, turns 8, fair 10.5, value 13, range [3, 18], size {min 1, max 2, start 1}, limit 5, spread {min 1, max 4}, quote {bid 9, ask 12, size 2}, counterparty [noise rate 0.8 turns [1, 4]; informed edge 0.5 turns [5, 8]], benchmark 8`. Cards: turn 1 the rule; turn 3 "The first die shows 6. Fair is now 13.5." (`fair: 13.5`); turn 6 "The second die shows 4. Fair is now 13.5." (`fair: 13.5`); turn 8 the third die shows 3, the total is 13 (`reveal: true`). Strategy: `[9,12,2] [9,12,2] [12,15,1] [12.5,14.5,1]` then `[12.5,14.5,1]` four times. Played: P&L £9.5, 0 breaks; opening quote untouched: £1, 2 limit breaks. Second check of $10.5$ and $13.5$: $3 \times 3.5$; $6 + 3.5 + 3.5 = 13$ and $6 + 4 + 3.5 = 13.5$.

**Q2, `bad-news`** (diff 4, skills `mg-update`, `mg-risk`; draws on mm-games `l8-informed-flow`). A share opens at £50; bad news, then informed sellers.
`seed 31, turns 8, fair 50, value 46, range [38, 58], size {min 1, max 3, start 1}, limit 4, spread {min 1, max 5}, quote {bid 48.5, ask 51.5, size 2}, counterparty [noise rate 0.7 turns [1, 3]; informed edge 0.5 turns [4, 8]], benchmark 12`. Cards: turn 1 "The share last traded at £50."; turn 4 "A weak report. Fair is now £48." (`fair: 48`); turn 7 "The value is revealed: £46." (`reveal: true`). Strategy: `[48.5,51.5,2]` three times, then `[46,50,1] [45,49,1] [44.5,48.5,1] [44.5,47.5,1] [44.5,47.5,1]`. Played: P&L £19.5, 0 breaks; untouched: £2, 3 limit breaks.

**Q3, `interviewer-flow`** (diff 4, skills `mg-quote`, `mg-risk`; draws on mm-games `l10-position-limits`, `l12-thinking-aloud`). The interviewer is a scripted counterparty who tests your limit; the results table lists them as `scripted`.
`seed 41, turns 6, fair 100, value 104, range [92, 112], size {min 1, max 2, start 1}, limit 3, spread {min 2, max 6}, quote {bid 98, ask 102, size 2}, counterparty scripted trades [hit 2 at 98; hit 2 at 97.5; hit 2 at 97; lift 2 at 102; lift 2 at 101; none], benchmark 6`. Cards: turn 1 the rule; turn 4 "The interviewer says the level looks higher. Fair is now £102." (`fair: 102`); turn 6 "The value is revealed: £104." (`reveal: true`). Strategy: `[98,102,2] [96.5,100.5,1] [96.5,100.5,1] [100,102,1] [99,101,1] [101,105,1]`. Played: P&L £7, 0 breaks; untouched: £14 but 3 limit breaks, so it fails on the rules first. Note for the prose: at position 3 (the limit) any quote breaks, so the learner must step the bid away before the position reaches it. That is the lesson; say so in `feedback.byKey.limit`.

**Q4, `defend-the-skew`** (longform, diff 4, skills `mg-quote`, `mg-risk`, `rk-behave`; draws on mm-games `l7-skewing`, `l12-thinking-aloud`; tag `market-defence`; pace 480). Fixed numbers from Q3's model run, not read from the learner: "You bought 2 at £98 on turn 1. The interviewer offers to sell again at £97.5. You quote £96.5 to £100.5 for 1. Explain the quote." Model: the position is +2 against a limit of 3, so a second fill at £97.5 would leave +4 and break the limit; lowering the bid below £97.5 stops the fill, the ask at £100.5 stays above the fair value of £100 so selling still earns, and the width of £4 keeps the quote inside the allowed £2 to £6. Rubric (10): states the position and the limit (2); says the bid sits below the interviewer's £97.5 so no more is bought (2); gives the ask against fair value (1); names the skew as inventory management, not a view (2); mentions adverse selection (a seller who keeps selling may know more) (1); states what would change the quote (a card, a price, a fill) (1); reasons aloud, in order, with a clear final quote (1).

### Paper 4: fit and motivation (18 min, 2 `longform`)

Both items: `skills: ["rk-behave"]`, draws on recruiting `l8-why-this-firm`, `l11-stories-that-answer`, `l13-the-final-round`, difficulty 3, `pace: 480`. The prompt says to say the answer aloud first, then type it in at most 200 words. The model answer is an example, clearly labelled as one, because the learner's own story is the real answer. No firm is named in the prompt, model or rubric.

- **Q1, `why-trading`.** Prompt: "Why do you want to trade rather than work at a bank or a lab?" Rubric (10): a one-sentence answer first (1); two reasons tied to the daily work, such as pricing under uncertainty and fast feedback (2); one piece of your own evidence with a number or an outcome (3); says what you dislike or find hard about trading and how you handle it (2); why a trading firm rather than another route (1); about 90 seconds, no clichés (1).
- **Q2, `decision-under-uncertainty`.** Prompt: "Tell me about a decision you made with incomplete information, and what you would change." Rubric (10): the situation in one or two sentences (1); what you did not know (2); the decision and its reason, with a rough probability or cost (3); the result, stated honestly (1); what you would change, and how you would know sooner (2); the answer is first person and under two minutes (1).

### Generation, voice and acceptance

**Script.** `gen_superday.py` in the agent's scratchpad folder, `random.Random(2601)` for option order only (parameters are fixed above). It holds every number as a `Fraction`, asserts each key two ways, replays the three trade specs through `app/js/engine/widgets/trade.js` by a small node call and asserts verdict `ok` for the strategy and not `ok` for `strategy: null`, reads the families and questions of `mock-oa-trader*.json` and `mock-oa-sig*.json` for the duplicate check, asserts the option rules (shuffle, no times-ten pair, no equal slips, one tightest interval per Fermi item), writes the exam JSON and prints a key table. The script is embedded in the report.

**Feedback and explain.** Choice and numeric items: `feedback.correct` names the move in one clause, `feedback.generic` gives the first step, `explain.text` shows the calculation and the second check in at most three sentences. Trade items: per-key `feedback.byKey` as above and `explain.text` naming the P&L of the model run. Longform items: `model` and `rubric` only.

**Voice scan.** `VOICE_BASE=/home/user/zero-to-quant/app/content/exams/ python3 docs/reviews/voice-scan.py`, or a folder holding a copy of the exam file: 0 sentences over 20 words and 0 explanations over three sentences. Model answers of a longform count as prose, so keep their sentences short too.

**Skills covered.** `pz-expectation`, `pz-conditioning`, `pz-games`, `gm-poker`, `mp-speed`, `mp-fractions`, `mp-estimate`, `bz-quick`, `mg-fair`, `mg-quote`, `mg-update`, `mg-risk`, `rk-behave`.

**Prerequisites** (cite in the report; nothing is gated): puzzles `l2-every-coupon`, `l5-hats`, `l20-betting-on-sequences`, `l21-kelly`, `l24-mixed-set`, `l25-fair-from-biased`; game-theory `l11-pot-odds`; mental-pressure `l1-towards-fifty`, `l2-two-by-two`, `l7-estimating-products`; brainteasers `l13-digits-and-remainders`, `l14-sums-in-one-line`; mm-games `l2-dice-sum`, `l4-fermi`, `l7-skewing`, `l8-informed-flow`, `l10-position-limits`, `l12-thinking-aloud`, `l13-full-game`; recruiting `l8-why-this-firm`, `l11-stories-that-answer`, `l12-reasoning-aloud`, `l13-the-final-round`.

**Acceptance.** The common checks (1 to 5), with one file instead of three, plus: the start card lists four papers (45, 15, 30 and 18 minutes, 108 in all, 24 questions) and both checks; paper 2 refuses a step back and a step without an answer (the playthrough probes it); the playthrough passes the three trade items by their `strategy` and marks the five longform items with every rubric point ticked, at 1280 and 390 px (`--mobile`), with `--local-cdn <pkgs>`; a screenshot of one trade item at 390 px shows the ledger and the steppers without overlap; every key is asserted two ways in `gen_superday.py`; report at `docs/reports/exam-mock-superday-trader.md`, listing each item's answer and computations, the three trade specs and their played P&L, and these proposals: no `prep.json` change (the entry exists); inbox bullets under `Raised later (exam mock-superday-trader):` for the E3 bank draw, for a `trade` item that could score by P&L, for longform marks that are all-or-nothing at 7 of 10, and for the NaN pass mark if it shows.
