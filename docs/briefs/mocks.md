# Brief: the mock assessments

Mock exams from `docs/briefs/interview-plan.md` section (d). The first three, `mock-oa-arith`, `mock-oa-sig` and `mock-oa-trader`, were written first, then `mock-superday-trader`. The sections at the end add `mock-oa-code`, `mock-superday-research` and `mock-oa-quant-data` (topic 3.5). One content agent writes one mock, from its section below. It follows `docs/LEVEL-BRIEF.md` for checking, playthrough and reporting, with an exam in place of a level.

### Shared rules for the mocks

**Schema.** Read `docs/AUTHORING.md` section 5: "Mock assessment", "Paper fields", "Generated items", "`tags` and `pace`", plus the item format at the top of section 5. Read the mock rules in section 7 ("Mock and timed rules"). Copy the shape of `app/content/exams/mock-sample.json`: `id`, `name`, `style`, `models`, `description`, optional `skills`, then `parts` (papers and checks). Each paper has `kind: "paper"`, `id`, `name`, `minutes`, `scoring`, one of `pass` or `passNet`, optional `navigation` and `skip`, and `items`.

**What the engine has built (checked in AUTHORING and ENGINE-BACKLOG 450 to 458 and 467 to 480, not taken from the plan).**

| Plan item | State | What a mock does about it |
| --- | --- | --- |
| E1 net scoring, `scoring` and `passNet` | Built (450) | Use it. The results page shows the net score. |
| E2 `navigation: "forward"`, `skip: false` | Built (451) | Use it where the reported test is forward only. |
| E4 generated arithmetic items | Built (452), **whole numbers only**: add, sub, mul, div from `content/warmup.json`; near misses are reverse operation, misplaced point and slipped digit | `mock-oa-arith` uses it. Decimals, fractions and percentages are authored. |
| E5 mock exam kind | Built (453) | `exams/mock-<id>.json`, listed on Review under "Mock assessments" with a trend. |
| E9 per-item timing, `pace`, `tags` | Built (457, 458) | Give every authored item `tags` (family first) and `pace` in seconds. Generator entries take neither; they count under `mental-arithmetic`. |
| E3 fresh draws per sitting | Built (468, 473, 477) as `draw: [{ "from": "bank/<file or prefix>" or "drills/<pack>", "tags", "difficulty", "n" }]` on a mock or stage paper; drills become `code` items (C-draw-code); seeded, family-balanced, unseen first | Use it where a pool exists. `mock-oa-sig` and `mock-oa-trader` keep their three fixed versions (written before it was built). `mock-oa-code` draws from its own drill pack. |
| E11 follow-up `parts` | Built (467): 2 to 6 parts, each opens after the one before is checked, credit is parts right over parts; code parts have cumulative tests (C-parts-code), kinds may mix (C-parts-mixed); no `longform` part | Use it for an interviewer's follow-ups (`mock-superday-research`, `mock-oa-quant-data`). |
| E14 data files | Built (469): `data: { "name.csv": "content/data/<folder>/name.csv" }` on a Python `code` widget or drill, text files up to 256 KB | Use it for data tasks (`mock-oa-quant-data`). |
| E8 drill library | Built (472): drills in `drills/`, filtered by `pattern`, drawable into a mock | `mock-oa-code` adds a pack `oa`. |
| E15 calculator panel | **Not built** | The description tells the learner to have a basic calculator ready (`mock-oa-sig`). No-calculator mocks end with a self-ticked check. |
| Interval scoring (tighter correct range scores more) | **Not built**: no interval widget, no per-option marks | A four-option choice of intervals, one narrowest correct (`mock-oa-trader` paper C). |

**Intro screen.** The start card prints `name`, then `description` as plain text (escaped: no Markdown, no KaTeX), then "Models ..." from `models`. The engine adds its own rules list: total minutes, question count, "generated afresh" when a paper has a generator entry, no going back on forward papers, negative marking and the pass mark. So `description` says only what the engine cannot: that the format is reported, the calculator rule, and anything the learner should know before starting.

**Firm names** appear only in `models` and `description`, each time marked "reported" with the as-of month (Nov 2026). Never in `name`, items, feedback or explanations.

**A check part is a pass condition.** On a mock with a check, the attempt passes only when every paper passes and every check is ticked (`exam.js`, `passed = every paper passed && checksOk`). Use that for "I used no calculator".

**Voice** (binding, AUTHORING section 6 and CLAUDE.md): British English, no exclamation marks, no em-dashes, sentences under 20 words, explanations of at most three sentences, £ for money. Every `choice` carries `"shuffle": true`, except interval items, whose options are ordered ranges (AUTHORING forbids shuffling ordered options). Every distractor has a `why` naming the learner's action ("You added the tops and the bottoms."). Every stated number is computed twice: once in closed form, once by enumeration, a linear solve or a series, both as `Fraction`s, with an `assert` that they agree.

**Scripts.** Every item that is not engine-generated comes from a deterministic seeded Python script the agent writes in its own folder under the scratchpad named in the orchestrator prompt (`exam-<id>/`), and copies to `docs/briefs/mocks-scripts/` (the checks for the topic 3.5 mocks are already there). The script holds every number as a `Fraction`, asserts each answer two ways, writes the exam JSON, and is embedded in full in the report, as `gen17.py` is in `docs/reports/mental-pressure-4.md`. The sandbox CPython may lack SciPy: use `fractions`, `itertools` and `math` only.

**Packages for the playthrough.** `<pkgs>` is the `pkgs` folder inside the scratchpad, as the orchestrator prompt names them (the `pkgs` and scratchpad paths named in the orchestrator prompt). If it is missing, build it with `bash app/tools/fetch-local-cdn.sh <pkgs>`.

**Do not edit** engine files (`app/js/`, `app/tools/`, `app/css/`, `app/index.html`), any `course.json`, `content/prep.json`, `content/warmup.json`, other exams, the `mm-games` course or `docs/briefs/mm-games.md`. Commit in your own worktree branch only when the orchestrator prompt says so, and do not push. Propose any `prep.json` change in the report.

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

## mock-oa-code

**Why this mock is built this way.** `docs/briefs/coding-int.md` Level 4 fixes three facts. `#exam/mock-oa-code` is authored before l15. It draws its coding items from drill packs through C-draw-code, so each sitting is a fresh paper. And l15 screen 10 and l17 screen 10 link to it as "two problems in 60 minutes". This section matches all three. Drill packs 1 to 4 of `docs/briefs/interview-plan.md` are not written yet. So the mock brings its own pack `oa` of eight Python drills. That makes the mock buildable now and keeps every problem specified here. Packs 1 to 4 may be added to the draw later by editing two `from` fields; nothing else changes.

**Files.** The mock author writes ten files and edits one list.

- `app/content/exams/mock-oa-code.json`.
- `app/content/drills/oa-product-windows.json`, `oa-rain-water.json`, `oa-min-jumps.json`, `oa-merge-cost.json`, `oa-remove-digits.json`, `oa-rising-run.json`, `oa-decodings.json`, `oa-critical-path.json`.
- One row per drill appended to `app/content/drills/index.json` (`id`, `name`, `course: "coding-int"`, `difficulty`). Nothing else outside these files is touched.

**Mock fields.**

- `id`: `mock-oa-code`. `name`: `Coding assessment`. `style`: `developer`.
- `models` (under 200 characters): `Reported, as of Nov 2026: online coding assessments for quant research, software and strats roles at JP Morgan, Two Sigma and Goldman Sachs: two algorithm problems in 60 minutes, in Python.`
- `skills`: `{ "ci-patterns": "Further patterns", "ci-strings": "Strings and simulation", "ci-timed": "Solving under time" }`.

**Description** (plain text, each sentence under 20 words, firm names stay in `models`):

> This is the reported format of an online coding assessment, as candidates described it by Nov 2026. You have two algorithm problems in 60 minutes and write both in Python. The first is medium and the second is harder. Hidden tests include large inputs, so a slow answer fails them. A problem scores only when all its hidden tests pass. The results panel lists each test, so use it to see how far you got. The two problems are drawn afresh from a pool each time you sit. The pool is also in the drill library. Use no search engine and no notes. Read both statements and plan your minutes first.

**Parts.**

1. Paper `code`, name `Two problems in sixty minutes`: `minutes: 60`, `scoring: { "right": 1, "wrong": 0, "blank": 0 }`, `pass: 0.5` (one of two), free navigation, `items: []`, and
   `draw: [ { "from": "drills/oa", "difficulty": 3, "n": 1 }, { "from": "drills/oa", "difficulty": 4, "n": 1 } ]`.
2. Check `plan-first`, name `I read both statements and planned my minutes before I wrote code`, detail `Tick this only if you spent the first five minutes reading and noting the constraints.`
3. Check `no-lookup`, name `I used no search engine and no notes`, detail `Tick this only if you sat the whole paper without either.`

The attempt passes only when the paper passes and both checks are ticked. A drawn drill carries its own `pace`: 1,200 s at difficulty 3 and 1,800 s at difficulty 4. That is 3,000 s in all, so ten of the 60 minutes remain for reading and checking. The pool holds four problems at each difficulty. So the validator's "twice `n`" warning does not fire. The pair differs from the last attempt whenever it can.

**Scoring, said plainly.** A drawn problem is one `code` item: right when every hidden test passes, otherwise wrong. The engine has no credit for the share of tests passed on a code item. A reported platform gives partial credit by test group, which l15 and l17 teach as a planning rule. Here the planning rule shows in the order of work. It also shows in the results panel, which lists each hidden test. It does not show in the mark. The paper's pass mark is one problem of two. The description says all of this, in the sentences above.

**The pool: eight drills of pack `oa`.** Every drill file has `"pack": "oa"`, `"course": "coding-int"`, `language` left out (Python), `compare: "equal"` on every test, at most 15 tests (these have 10 to 12), at least three, two visible `examples`, a `how` line ("Submit runs N hidden tests. Each answer must equal the expected value."), a `solution`, and `tags` with the family first. `skills`: `["ci-patterns", "ci-timed"]` for the `windows`, `two-pointers` and `greedy` drills. Use `["ci-strings", "ci-timed"]` for `oa-remove-digits` and `oa-decodings`, which work on digit strings. Use `["ci-timed"]` for the rest. Patterns are from the fixed vocabulary of AUTHORING section 5, so no slug is added. Each `brief` is the statement below, then the signature, then one example in words. Tests run small to large, as `docs/briefs/coding-int.md` asks. A slow answer passes the small group and stops at the first large case.

Difficulty 3 (pace 1,200 s): `oa-product-windows` (`windows`), `oa-rain-water` (`two-pointers`), `oa-min-jumps` (`greedy`), `oa-merge-cost` (`heaps-tries`). Difficulty 4 (pace 1,800 s): `oa-remove-digits` (`stacks-queues`), `oa-rising-run` (`binary-search`), `oa-decodings` (`dp`), `oa-critical-path` (`graphs`). The family is the first tag, and each drill has its own. So a draw never takes two items of one family. The eight patterns are all different, which suits the pattern filter on `#drill`.

Check: from `docs/briefs/mocks-scripts/` run `python3 -I oa_code.py`. For every drill it holds a reference, an exhaustive or second method and the starter. It asserts that the reference equals the second method on 4,000 seeded random small cases; that each small test's expected value equals the second method's; that each large test equals the closed form printed in the table; that the starter fails at least one test; and that the reference runs every large test in well under a second in CPython. The slowest is under 0.1 s, so Pyodide stays well inside its 5 s limit. It writes `oa_code_tests.json` (every table below) and `oa_code_section.md`, which is the text under this paragraph. The last run printed `ALL AGREE: 8 problems`.

#### `oa-product-windows`: Blocks with a small product (difficulty 3, pattern `windows`, tag `product-windows`, pace 1200 s)

Statement. `nums` holds positive whole numbers. Count the non-empty blocks of neighbouring entries whose product is below `k`. Equal blocks at different places count separately. `k` may be 1 or less, and `nums` may be empty.

Signature `count_products_below(nums, k)`. Starter (fails 7 of 10):

```python
def count_products_below(nums, k):
    return 0
```

Reference (`solution`):

```python
def count_products_below(nums, k):
    if k <= 1:
        return 0
    left, prod, count = 0, 1, 0
    for right, x in enumerate(nums):
        prod *= x
        while prod >= k:
            prod //= nums[left]
            left += 1
        count += right - left + 1
    return count
```

Hidden tests, all `compare: "equal"`. Each small test is checked against an exhaustive or second method. Each large test is checked against the value in the last column. Slow code: checking every block is 2 x 10^10 steps on test 9.

| # | Call | Expected | Second value from |
| --- | --- | --- | --- |
| 1 | `count_products_below([3, 4, 2, 5, 1], 20)` | `10` | exhaustive method |
| 2 | `count_products_below([], 10)` | `0` | exhaustive method |
| 3 | `count_products_below([5], 5)` | `0` | exhaustive method |
| 4 | `count_products_below([5], 6)` | `1` | exhaustive method |
| 5 | `count_products_below([1, 1, 1], 2)` | `6` | exhaustive method |
| 6 | `count_products_below([7, 8], 1)` | `0` | exhaustive method |
| 7 | `count_products_below([2, 3, 4], 100)` | `6` | exhaustive method |
| 8 | `count_products_below([6, 2, 9, 1, 3], 30)` | `11` | exhaustive method |
| 9 | `count_products_below([1] * 200000, 2)` | `20000100000` | closed form |
| 10 | `count_products_below([2] * 200000, 3)` | `200000` | closed form |

Examples (visible): tests 1 and 4. Largest reference run 0.020 s in CPython. 4000 seeded random cases agree with the exhaustive method.

#### `oa-rain-water`: Water held between bars (difficulty 3, pattern `two-pointers`, tag `water-trapped`, pace 1200 s)

Statement. `heights[i]` is the height of a bar of width 1. After rain, water sits in the dips between taller bars. Return how many units of water the bars hold. Water that could run off either end is not held.

Signature `trapped_water(heights)`. Starter (fails 7 of 11):

```python
def trapped_water(heights):
    return 0
```

Reference (`solution`):

```python
def trapped_water(heights):
    lo, hi = 0, len(heights) - 1
    left_max = right_max = water = 0
    while lo < hi:
        if heights[lo] < heights[hi]:
            left_max = max(left_max, heights[lo])
            water += left_max - heights[lo]
            lo += 1
        else:
            right_max = max(right_max, heights[hi])
            water += right_max - heights[hi]
            hi -= 1
    return water
```

Hidden tests, all `compare: "equal"`. Each small test is checked against an exhaustive or second method. Each large test is checked against the value in the last column. Slow code: finding the walls of every bar by scanning is 4 x 10^10 steps on test 9.

| # | Call | Expected | Second value from |
| --- | --- | --- | --- |
| 1 | `trapped_water([3, 0, 2, 0, 4])` | `7` | exhaustive method |
| 2 | `trapped_water([])` | `0` | exhaustive method |
| 3 | `trapped_water([5])` | `0` | exhaustive method |
| 4 | `trapped_water([1, 2, 3])` | `0` | exhaustive method |
| 5 | `trapped_water([3, 1, 3])` | `2` | exhaustive method |
| 6 | `trapped_water([4, 1, 1, 0, 2, 3])` | `8` | exhaustive method |
| 7 | `trapped_water([0, 3, 0, 1, 0, 2])` | `5` | exhaustive method |
| 8 | `trapped_water([2, 0, 2])` | `2` | exhaustive method |
| 9 | `trapped_water([5] + [0] * 199998 + [5])` | `999990` | closed form |
| 10 | `trapped_water(list(range(100000)) + list(range(100000, 0, -1)))` | `0` | closed form |
| 11 | `trapped_water([3, 1] * 100000)` | `199998` | closed form |

Examples (visible): tests 1 and 5. Largest reference run 0.032 s in CPython. 4000 seeded random cases agree with the exhaustive method.

#### `oa-min-jumps`: Fewest jumps (difficulty 3, pattern `greedy`, tag `jump-count`, pace 1200 s)

Statement. `nums[i]` is the longest jump you can make from position `i`, and you may jump any shorter distance. Start at position 0. Return the fewest jumps that reach the last position, or -1 if you cannot. A list of one or no entries needs 0 jumps.

Signature `min_jumps(nums)`. Starter (fails 9 of 11):

```python
def min_jumps(nums):
    return 0
```

Reference (`solution`):

```python
def min_jumps(nums):
    n = len(nums)
    if n <= 1:
        return 0
    jumps = end = far = 0
    for i in range(n - 1):
        far = max(far, i + nums[i])
        if i == end:
            if far <= i:
                return -1
            jumps += 1
            end = far
            if end >= n - 1:
                return jumps
    return jumps if end >= n - 1 else -1
```

Hidden tests, all `compare: "equal"`. Each small test is checked against an exhaustive or second method. Each large test is checked against the value in the last column. Slow code: trying every earlier position for each position is 2 x 10^10 steps on test 9.

| # | Call | Expected | Second value from |
| --- | --- | --- | --- |
| 1 | `min_jumps([4, 1, 1, 3, 1, 1, 1])` | `2` | exhaustive method |
| 2 | `min_jumps([])` | `0` | exhaustive method |
| 3 | `min_jumps([0])` | `0` | exhaustive method |
| 4 | `min_jumps([0, 5])` | `-1` | exhaustive method |
| 5 | `min_jumps([1, 1, 1, 1])` | `3` | exhaustive method |
| 6 | `min_jumps([5, 9, 3, 2, 1, 0, 2, 3, 3, 1, 0, 0])` | `3` | exhaustive method |
| 7 | `min_jumps([2, 0, 0])` | `1` | exhaustive method |
| 8 | `min_jumps([10, 1, 1])` | `1` | exhaustive method |
| 9 | `min_jumps([1] * 200000)` | `199999` | closed form |
| 10 | `min_jumps([200000] + [1] * 199999)` | `1` | closed form |
| 11 | `min_jumps([2] * 200000)` | `100000` | closed form |

Examples (visible): tests 1 and 5. Largest reference run 0.023 s in CPython. 4000 seeded random cases agree with the exhaustive method.

#### `oa-merge-cost`: Cheapest way to join sticks (difficulty 3, pattern `heaps-tries`, tag `merge-cost`, pace 1200 s)

Statement. You have sticks with the given lengths. Joining two sticks costs the sum of their lengths and gives one longer stick. Return the least total cost to join them all into one. Zero or one stick costs nothing.

Signature `min_merge_cost(sticks)`. Starter (fails 8 of 10):

```python
def min_merge_cost(sticks):
    return 0
```

Reference (`solution`):

```python
def min_merge_cost(sticks):
    heap = list(sticks)
    heapq.heapify(heap)
    cost = 0
    while len(heap) > 1:
        a, b = heapq.heappop(heap), heapq.heappop(heap)
        cost += a + b
        heapq.heappush(heap, a + b)
    return cost
```

Hidden tests, all `compare: "equal"`. Each small test is checked against an exhaustive or second method. Each large test is checked against the value in the last column. Slow code: searching for the two shortest sticks by scanning is 10^10 steps on test 10.

| # | Call | Expected | Second value from |
| --- | --- | --- | --- |
| 1 | `min_merge_cost([5, 3, 8, 2])` | `33` | exhaustive method and second algorithm |
| 2 | `min_merge_cost([])` | `0` | exhaustive method and second algorithm |
| 3 | `min_merge_cost([9])` | `0` | exhaustive method and second algorithm |
| 4 | `min_merge_cost([4, 4])` | `8` | exhaustive method and second algorithm |
| 5 | `min_merge_cost([1, 1, 1, 1])` | `8` | exhaustive method and second algorithm |
| 6 | `min_merge_cost([7, 3, 5])` | `23` | exhaustive method and second algorithm |
| 7 | `min_merge_cost([10, 20, 30, 40, 50])` | `330` | exhaustive method and second algorithm |
| 8 | `min_merge_cost([1] * 131072)` | `2228224` | closed form |
| 9 | `min_merge_cost([2] * 65536)` | `2097152` | closed form |
| 10 | `min_merge_cost(list(range(1, 100001)))` | `81782502640` | two-queue method |

Examples (visible): tests 1 and 4. Largest reference run 0.086 s in CPython. 4000 seeded random cases agree with the exhaustive method and with the second algorithm.

#### `oa-remove-digits`: Smallest number after removing digits (difficulty 4, pattern `stacks-queues`, tag `digit-removal`, pace 1800 s)

Statement. `digits` is a string of the characters 0 to 9. Remove exactly `k` characters, keeping the order of the rest, so the number left is as small as possible. Return it as a string with no leading zeros. Return "0" if nothing is left, or only zeros.

Signature `smallest_after_removing(digits, k)`. Starter (fails 12 of 12):

```python
def smallest_after_removing(digits, k):
    return ""
```

Reference (`solution`):

```python
def smallest_after_removing(digits, k):
    stack = []
    for d in digits:
        while k and stack and stack[-1] > d:
            stack.pop()
            k -= 1
        stack.append(d)
    if k:
        stack = stack[:-k]
    return "".join(stack).lstrip("0") or "0"
```

Hidden tests, all `compare: "equal"`. Each small test is checked against an exhaustive or second method. Each large test is checked against the value in the last column. Slow code: trying every set of digits is hopeless on tests 10 and 11. Removing one digit at a time with a scan is 10^10 steps.

| # | Call | Expected | Second value from |
| --- | --- | --- | --- |
| 1 | `smallest_after_removing("5291", 2)` | `'21'` | exhaustive method |
| 2 | `smallest_after_removing("", 0)` | `'0'` | exhaustive method |
| 3 | `smallest_after_removing("10", 2)` | `'0'` | exhaustive method |
| 4 | `smallest_after_removing("100200", 1)` | `'200'` | exhaustive method |
| 5 | `smallest_after_removing("9", 0)` | `'9'` | exhaustive method |
| 6 | `smallest_after_removing("1111", 2)` | `'11'` | exhaustive method |
| 7 | `smallest_after_removing("112", 1)` | `'11'` | exhaustive method |
| 8 | `smallest_after_removing("7654321", 3)` | `'4321'` | exhaustive method |
| 9 | `smallest_after_removing("30200", 1)` | `'200'` | exhaustive method |
| 10 | `smallest_after_removing("9" * 100000 + "1" * 100000, 100000) == "1" * 100000` | `True` | closed form |
| 11 | `smallest_after_removing("1" * 150000 + "2" * 50000, 50000) == "1" * 150000` | `True` | closed form |
| 12 | `smallest_after_removing("5" * 200000, 200000)` | `'0'` | closed form |

Examples (visible): tests 1 and 4. Largest reference run 0.013 s in CPython. 4000 seeded random cases agree with the exhaustive method.

#### `oa-rising-run`: Longest rising subsequence (difficulty 4, pattern `binary-search`, tag `rising-subsequence`, pace 1800 s)

Statement. Return the length of the longest strictly increasing subsequence of `nums`. A subsequence keeps the order but need not use neighbouring entries. An empty list gives 0.

Signature `longest_rising(nums)`. Starter (fails 10 of 11):

```python
def longest_rising(nums):
    return 0
```

Reference (`solution`):

```python
def longest_rising(nums):
    tails = []
    for x in nums:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)
```

Hidden tests, all `compare: "equal"`. Each small test is checked against an exhaustive or second method. Each large test is checked against the value in the last column. Slow code: the quadratic table is 2 x 10^10 steps on test 9.

| # | Call | Expected | Second value from |
| --- | --- | --- | --- |
| 1 | `longest_rising([4, 10, 4, 3, 8, 9])` | `3` | exhaustive method and second algorithm |
| 2 | `longest_rising([])` | `0` | exhaustive method and second algorithm |
| 3 | `longest_rising([7])` | `1` | exhaustive method and second algorithm |
| 4 | `longest_rising([5, 5, 5])` | `1` | exhaustive method and second algorithm |
| 5 | `longest_rising([1, 2, 3, 4])` | `4` | exhaustive method and second algorithm |
| 6 | `longest_rising([4, 3, 2, 1])` | `1` | exhaustive method and second algorithm |
| 7 | `longest_rising([6, 2, 9, 5, 1, 7, 3, 8])` | `4` | exhaustive method and second algorithm |
| 8 | `longest_rising([0, 8, 4, 12, 2, 10, 6, 14])` | `4` | exhaustive method and second algorithm |
| 9 | `longest_rising(list(range(200000)))` | `200000` | closed form |
| 10 | `longest_rising(list(range(200000, 0, -1)))` | `1` | closed form |
| 11 | `longest_rising([i % 1000 for i in range(200000)])` | `1000` | closed form |

Examples (visible): tests 1 and 7. Largest reference run 0.037 s in CPython. 4000 seeded random cases agree with the exhaustive method and with the second algorithm.

#### `oa-decodings`: Ways to decode a message (difficulty 4, pattern `dp`, tag `digit-decodings`, pace 1800 s)

Statement. A message of letters was coded as digits. A is 1, B is 2 and so on up to Z as 26. `s` is the digit string. Return how many different messages it could be, modulo 1,000,000,007. A string that cannot be decoded gives 0, and the empty string gives 1.

Signature `count_decodings(s)`. Starter (fails 9 of 12):

```python
def count_decodings(s):
    return 0
```

Reference (`solution`):

```python
def count_decodings(s):
    prev2, prev1 = 0, 1
    for i, ch in enumerate(s):
        cur = 0
        if ch != "0":
            cur += prev1
        if i >= 1 and "10" <= s[i - 1:i + 1] <= "26":
            cur += prev2
        prev2, prev1 = prev1, cur % MOD
    return prev1
```

Hidden tests, all `compare: "equal"`. Each small test is checked against an exhaustive or second method. Each large test is checked against the value in the last column. Slow code: listing every decoding takes over 10^40 steps on test 9. A recursion without a table never ends.

| # | Call | Expected | Second value from |
| --- | --- | --- | --- |
| 1 | `count_decodings("226")` | `3` | exhaustive method |
| 2 | `count_decodings("")` | `1` | exhaustive method |
| 3 | `count_decodings("0")` | `0` | exhaustive method |
| 4 | `count_decodings("100")` | `0` | exhaustive method |
| 5 | `count_decodings("2710")` | `1` | exhaustive method |
| 6 | `count_decodings("11106")` | `2` | exhaustive method |
| 7 | `count_decodings("1212")` | `5` | exhaustive method |
| 8 | `count_decodings("301")` | `0` | exhaustive method |
| 9 | `count_decodings("1" * 200000)` | `835799900` | Fibonacci by fast doubling |
| 10 | `count_decodings("27" * 100000)` | `1` | Fibonacci by fast doubling |
| 11 | `count_decodings("10" * 100000)` | `1` | Fibonacci by fast doubling |
| 12 | `count_decodings("1" * 100000 + "0" + "9" * 5)` | `911435502` | Fibonacci by fast doubling |

Examples (visible): tests 1 and 4. Largest reference run 0.055 s in CPython. 4000 seeded random cases agree with the exhaustive method.

#### `oa-critical-path`: Time to finish all tasks (difficulty 4, pattern `graphs`, tag `critical-path`, pace 1800 s)

Statement. There are `n` tasks numbered 0 to `n - 1`, and `durations[i]` is the time task `i` takes. Each pair `[a, b]` in `edges` means task `a` must finish before task `b` starts. Any number of tasks may run at once. Return the least time to finish every task, or -1 if the pairs form a loop.

Signature `critical_path_length(n, edges, durations)`. Starter (fails 11 of 12):

```python
def critical_path_length(n, edges, durations):
    return 0
```

Reference (`solution`):

```python
def critical_path_length(n, edges, durations):
    indeg = [0] * n
    out = [[] for _ in range(n)]
    for a, b in edges:
        out[a].append(b)
        indeg[b] += 1
    start = [0] * n
    queue = [i for i in range(n) if indeg[i] == 0]
    done = 0
    while queue:
        u = queue.pop()
        done += 1
        finish = start[u] + durations[u]
        for v in out[u]:
            start[v] = max(start[v], finish)
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    if done < n:
        return -1
    return max((start[i] + durations[i] for i in range(n)), default=0)
```

Hidden tests, all `compare: "equal"`. Each small test is checked against an exhaustive or second method. Each large test is checked against the value in the last column. Slow code: a recursive search runs out of stack on test 10. Re-walking every path is exponential.

| # | Call | Expected | Second value from |
| --- | --- | --- | --- |
| 1 | `critical_path_length(4, [[0, 1], [0, 2], [1, 3], [2, 3]], [3, 2, 4, 1])` | `8` | exhaustive method |
| 2 | `critical_path_length(0, [], [])` | `0` | exhaustive method |
| 3 | `critical_path_length(3, [], [5, 2, 9])` | `9` | exhaustive method |
| 4 | `critical_path_length(3, [[0, 1], [1, 2], [2, 0]], [1, 1, 1])` | `-1` | exhaustive method |
| 5 | `critical_path_length(2, [[0, 1], [0, 1]], [4, 3])` | `7` | exhaustive method |
| 6 | `critical_path_length(5, [[0, 1], [1, 2], [0, 3], [3, 4], [2, 4]], [2, 2, 2, 5, 1])` | `8` | exhaustive method |
| 7 | `critical_path_length(1, [], [7])` | `7` | exhaustive method |
| 8 | `critical_path_length(3, [[0, 1]], [4, 5, 6])` | `9` | exhaustive method |
| 9 | `critical_path_length(3, [[1, 1]], [1, 1, 1])` | `-1` | exhaustive method |
| 10 | `critical_path_length(100000, [[i, i + 1] for i in range(99999)], [1] * 100000)` | `100000` | closed form |
| 11 | `critical_path_length(100001, [[i, 100000] for i in range(100000)], [2] * 100000 + [3])` | `5` | closed form |
| 12 | `critical_path_length(100000, [[i, i + 1] for i in range(99999)] + [[99999, 0]], [1] * 100000)` | `-1` | closed form |

Examples (visible): tests 1 and 4. Largest reference run 0.078 s in CPython. 4000 seeded random cases agree with the exhaustive method.


**Keyed numbers.** Every expected value is the output of the reference, asserted against a second method in `oa_code.py`. No number is stated in prose that the script does not compute. The closed forms of the large tests: blocks of ones below 2, $200000 \times 200001 / 2$; water between two walls of height 5 over 199,998 empty columns, $5 \times 199998 = 999990$; joining $2^{17}$ sticks of length 1, $131072 \times 17 = 2228224$; decodings of 200,000 ones, the Fibonacci number $F(200001)$ modulo $10^9 + 7$ by fast doubling; and the others as the "Second value from" column says.

**Duplicates.** `python3 -I fresh.py` checks every function name, drill id and long argument list of this mock. It searches `app/content/` (courses, exams, bank, drills) and the other briefs. A first draft of this pool failed it, which is why these eight were chosen. That draft had `longest_k_distinct` with the inputs `"eceba"` and `"abaccc"`, which `ds` homework-2 also has. It had `stock_span` (`ds` and `contests` homework-3) and `pair_count` (`ds` homework-1). It had a shipping capacity, and `contests` l13 has `can_ship` and `min_capacity`. It had `cheapest_within` and `max_profit_k`. It had an equal 0s and 1s block, near `longest_zero_sum_subarray` in `coding-int` l17. The new eight match no name, id or argument list. Concepts may still touch a lesson: `ds` l10 mentions the histogram problem, so it is not in the pool. The author reruns `fresh.py` after writing the drills. It runs again once the bank and `coding-int` L3 and L4 exist.

**Engine notes.** All needed features are built. These are `draw` from `drills/<pack>` (468, 473, 477) and drills as `code` items. The code widget grades them, not the drill page's typed-result check, and every test here is a plain `equal`. They also use `pace` on a drill and `pack` or an `oa-` id prefix for matching. Nothing is missing, so no engine requirement is raised. One limit is stated in the description rather than worked around: marks are per problem (see "Scoring, said plainly").

**Acceptance.**

1. From `app/`: `node tools/validate.mjs 2>&1 | tail -5` reports 0 errors, with `mock-oa-code` listed and no `draw` warning.
2. `node tools/playthrough.mjs --drill oa-pair-count --drill oa-distinct-window --drill oa-stock-span --drill oa-ship-capacity --drill oa-bounded-path --drill oa-k-trades --drill oa-balanced-run --drill oa-weighted-jobs --local-cdn <pkgs>`: every starter (touched) fails, every solution passes every hidden test, and the stopwatch is read. Again with `--mobile`.
3. `node tools/playthrough.mjs --exam mock-oa-code --local-cdn <pkgs> 2>&1 | tail -30` is green and again with `--mobile`. The draw check shows one difficulty 3 and one difficulty 4 item. Two sittings in a row draw different pairs.
4. `#exam/mock-oa-code/1` opens the start card with one paper, 60 minutes, two questions, the pass mark and both checks. The two links in l15 and l17 reach it.
5. The voice scan (`python3 -I docs/briefs/mocks-scripts/voice.py`, then `VOICE_BASE` on the exam and drill folder as `docs/reviews/voice-scan.py` asks) reports 0 and 0.
6. Report at `docs/reports/exam-mock-oa-code.md`: files, the check output, the playthrough results, and these inbox bullets under `Raised later (exam mock-oa-code):` as unnumbered text: a share-of-tests credit for a `code` item in an exam (planning by test group is taught, not scored); a `language` filter for `draw` so a mixed Python and C++ pack can feed a Python mock; the drill library lists the pool, so a learner may meet a problem in `#drill` before the mock. No `prep.json` change is needed: the entry for `mock-oa-code` exists or is proposed in the report.

## mock-superday-research

**File.** `app/content/exams/mock-superday-research.json`. One file, no versions, for the reason `mock-superday-trader` gives: a superday is rehearsed a few times and its weight is in the follow-ups. Only paper 1 draws from the bank, so a second sitting still differs in four questions. `content/prep.json` already lists it where the researcher paths need it; the report checks and proposes no change if so.

- `id`: `mock-superday-research`. `name`: `Research superday`. `style`: `research`.
- `models` (under 200 characters): `Reported, as of Nov 2026: quant research final rounds at Two Sigma, Citadel and JP Morgan: probability and statistics, machine learning, coding, and an open prediction case.`
- `skills`: `{ "rq-stats": "Statistics questions", "rq-linalg": "Linear algebra questions", "rq-ml": "Machine learning questions", "rq-case": "The open case", "rq-data": "Data tasks" }`.

**Description** (plain, each sentence under 20 words, firm names only here and in `models`):

> This is the reported shape of a quant research final-round day, as candidates described it by Nov 2026. There are four papers, each on its own clock. They cover probability and statistics, machine learning, coding, and an open case. Real rounds are spoken, so say each answer aloud before you type it. Some questions have follow-ups that open one at a time. Four of the probability questions are drawn afresh each time you sit. No calculator and no search engine are allowed. Orders and lengths differ by firm and office. Two checks at the end ask for what the app cannot see.

**Parts, in order** (every paper `scoring: { "right": 1, "wrong": 0, "blank": 0 }`, free navigation, `pass` as a share, since nothing is marked negatively):

| # | Paper `id`, name | Minutes | Items | Pass | `pace` sum |
| --- | --- | --- | --- | --- | --- |
| 1 | `stats`, Probability and statistics | 45 | 8: 4 drawn, 4 fixed (2 with `parts`) | `pass: 0.6` (5 of 8) | 1,440 s fixed, about 800 s drawn |
| 2 | `ml`, Machine learning | 30 | 6 fixed (1 with `parts`) | `pass: 0.65` (4 of 6) | 1,740 s |
| 3 | `coding`, Coding | 45 | 2 fixed (1 with `parts`) | `pass: 0.5` (1 of 2) | 2,700 s |
| 4 | `case`, The open case | 45 | 2 `longform` | `pass: 0.5` (1 of 2) | 2,700 s |
| 5 | check `story-aloud`, `I told one behavioural story aloud in under two minutes, with a result`, detail `Tick this only if you timed it and named an outcome.` | | | | |
| 6 | check `no-lookup`, `I used no search engine and no notes`, detail `Tick this only if you sat all four papers without either.` | | | | |

That is 18 items, 165 minutes, 2 `longform`. The attempt passes only when every paper passes and both checks are ticked. A part not right takes the wrong mark, which is 0. So an item with parts earns its share of parts right (AUTHORING "Credit"). Known results-page bug, not worked around: on a multi-paper mock the pass line may print "Pass mark NaN%" (inbox bullet from `mock-oa-trader`).

**What is drawn and what is fixed.** Bank files `bank/probability-1` to `-4` hold probability families with the `research` role. The bank holds no statistics, machine learning or case families yet, because bank part 2 is not written. The validator refuses a `draw` that matches nothing. So paper 1 draws four probability questions and every other item is fixed here. Paper 1 entry: `{ "from": "bank/probability", "tags": ["bayes-in-a-minute", "estimating-n", "exceeding-one", "expected-distance", "indicator-tricks", "largest-of-several", "random-chords", "semicircle", "broken-stick", "urns", "hats", "waiting-for-hh", "when-to-stop", "every-coupon", "meeting", "given-the-total"], "difficulty": [3, 5], "n": 4 }`. These 16 families hold 30 items at difficulty 3 to 5, well over twice `n`. The draw takes one item from each of four families, in seeded order. A bank item's `requires` is ignored in a mock. Drawn items keep their own `pace`.

**Rules.** Every `choice` has `"shuffle": true`; every distractor has a `why` naming the learner's action; no key sits between a times-ten pair or two equal slips (DECISIONS "Distractors" and "Numeric distractors"); every `numeric` lists its named wrong values in `wrong`, each with a `feedback.byKey` line that names the action. Every item has `skills`, `tags` (family first), `pace` and `difficulty`. Voice as the shared rules. Every key below is computed twice in `docs/briefs/mocks-scripts/research_mocks.py`; its last run printed `ALL AGREE`.

### Paper 1: probability and statistics (45 min, 8 items)

The four fixed items come first, then the four drawn. `S1` and `S4` use `parts`: each part opens when the one before is checked.

| Item | Diff | Tag | Skill | Kind and `pace` | Question and key | `wrong` or distractors, with the slip | Computed twice |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | 3 | `two-regressions` | rq-stats | `parts` (numeric, numeric, choice), 420 | Stem: regressing `y` on `x` gives slope 0.35 and regressing `x` on `y` gives slope 1.4. **Part 1:** the correlation, key 0.7 (tol 0.0005). **Part 2:** the ratio of the standard deviations of `y` to `x`, key 0.5. **Part 3 (choice):** you stack a copy of every row beneath the data (n = 40 to 80). Key: same slope, standard error about 30% smaller | Part 1: 0.49 (gave $r^2$, not $r$), 0.875 (averaged the two slopes). Part 2: 2.0 (took $x$ over $y$), 0.35 (gave the slope). Part 3 options: same slope, standard error unchanged (you forgot the rows add evidence); same slope, standard error about 50% smaller (you halved it, the error falls with the square root); slope halves, standard error unchanged (copies do not move the line) | $\sqrt{0.35 \times 1.4} = 0.7$, and the pair $(r, s_x, s_y) = (0.7, 2, 1)$ gives slopes $0.7 \times \tfrac12 = 0.35$ and $0.7 \times 2 = 1.4$; $0.35 / 0.7 = 0.5$ and $0.7 / 1.4 = 0.5$; ratio of standard errors $\sqrt{38/39}/\sqrt2 = 0.698$ by formula, and by an explicit sample duplicated (same slope to 1e-12, same ratio) |
| S2 | 4 | `correlation-limits` | rq-stats, rq-linalg | numeric, 300 | Assets A, B have correlation 0.9 and B, C have correlation −0.6. The largest possible correlation of A and C, three decimals. Key −0.191 (tol 0.0005) | −0.540 (gave the centre $ab$ only), 0.191 (a sign slip: A and C cannot be positively correlated), 0.000 (took the top of the range as zero) | $ab + \sqrt{(1 - a^2)(1 - b^2)} = -0.54 + 0.3487 = -0.1913$; and the exact determinant of the correlation matrix on a grid of 0.0001: the largest $x$ with determinant at least 0 is −0.1913, the smallest −0.8887 |
| S3 | 3 | `special-eigenvalues` | rq-linalg | numeric, 240 | The determinant of the 4 by 4 matrix with 3.5 on the diagonal and 0.5 everywhere else. Key 135 (tol 0) | 81 (ignored the 0.5s: $3^4$), 625 (used the top eigenvalue four times), 15 (counted each eigenvalue once) | Eigenvalues $3 + 0.5 \times 4 = 5$ and $3, 3, 3$, so $5 \times 27$; and exact Gaussian elimination on `Fraction`s |
| S4 | 4 | `multiple-testing` | rq-stats | `parts` (numeric, numeric, choice), 480 | Stem: you test 12 independent signals, all with no real effect, each at the 5% level. **Part 1:** the chance of at least one false positive, key 0.4596 (tol 0.0005). **Part 2:** the Bonferroni cut-off for a family-wise 5%, key 0.00417 (tol 0.00005). **Part 3 (choice):** the smallest of the 12 p-values is 0.006. Key: not significant, 0.006 is above 0.0042 | Part 1: 0.6 (added: $12 \times 5\%$), 0.05 (one test only). Part 2: 0.05 (the single-test cut-off), 0.6 (multiplied the wrong way). Part 3 options: significant because 0.006 is below 0.05 (you used the single-test cut-off); significant because 0.006 is below $12 \times 0.05$ (you multiplied the cut-off); not significant because 12 tests cannot give a real result (an effect among the 12 can still show; Bonferroni only asks for a smaller p) | $1 - (19/20)^{12}$ as a `Fraction`, and the sum $\sum_{k \ge 1} \binom{12}{k} 0.05^k 0.95^{12-k}$; $0.05 / 12 = 1/240$; $0.006 > 1/240 > 0.004$ |
| D1 to D4 | 3 to 5 | from the bank | | drawn | four probability questions from the entry above | as the bank items carry | as the bank files record |

### Paper 2: machine learning (30 min, 6 items, all fixed)

| Item | Diff | Tag | Skill | Kind and `pace` | Question and key | `wrong` or distractors | Computed twice |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M1 | 3 | `ridge-shrinkage` | rq-ml | numeric, 210 | One centred predictor with $S_{xx} = 50$ and $S_{xy} = 100$. The ridge slope with penalty 25. Key 1.3333 (tol 0.001) | 2.0 (the least-squares slope), 1.0 (halved it), 0.0769 (divided by $1 + 25$) | $100 / (50 + 25) = 4/3$; and the exact minimum of the penalised sum of squares on a grid of 1/300 |
| M2 | 3 | `lasso-threshold` | rq-ml | numeric, 210 | Orthonormal columns, least-squares coefficients 3.0, 0.8, −1.5, 0.3, lasso penalty 1 on the standard objective $\tfrac12 \lVert y - X\beta \rVert^2 + \lambda \lVert \beta \rVert_1$. The sum of the absolute lasso coefficients. Key 2.5 (tol 0.0005) | 5.6 (no shrinkage), 3.4 (shrank every coefficient by 1 without stopping at zero) | Soft thresholds give 2.0, 0, −0.5, 0; and each coordinate's one-variable objective minimised on a grid of 0.1 |
| M4 | 3 | `pca-share` | rq-ml, rq-linalg | numeric, 270 | The covariance matrix with rows (4, 2) and (2, 3). The share of the variance on the first principal component. Key 0.7945 (tol 0.0005) | 0.5714 (the first variable's share, 4/7), 0.5 (an equal split) | $\lambda_1 = (7 + \sqrt{17})/2 = 5.5616$ over the trace 7; and power iteration, and NumPy `eigvalsh` |
| M3 | 4 | `leakage` | rq-ml, rq-case | choice, 270 | You standardise every feature with the mean and standard deviation of the whole sample, then split by time. The test score is too good. Why? Key: the scaler saw the test rows, so the future leaked into the features | Standardising always raises $R^2$ (scaling changes units, not information); a time split favours the model (a later test is the honest set-up); the model is too simple to overfit (simplicity does not explain a score that is too good). Four options of near equal length | No number to check |
| M5 | 4 | `bias-variance` | rq-ml | `parts` (numeric, numeric, choice), 420 | Stem: expected squared error is bias squared plus variance plus noise variance 1.0. **Part 1:** model A has bias 0.5 and variance 0.25. Key 1.5. **Part 2:** model B has bias 0.2 and variance 0.64. Key 1.68. **Part 3 (choice):** B has the lower bias but the higher error. What lowers its error most? Key: more training data or a stronger penalty, to cut the variance | Part 1: 1.75 (did not square the bias), 0.5 (left out the noise). Part 2: 1.84 (did not square the bias), 0.68 (left out the noise). Part 3: more features to cut bias (bias is already 0.04 of 1.68); less regularisation (it raises variance, the largest part); nothing, the noise sets the error (the 0.64 of variance can still be cut) | $0.25 + 0.25 + 1 = 3/2$ and $0.04 + 0.64 + 1 = 42/25$ as `Fraction`s, each by the bias-variance sum and by building the three terms separately |
| M6 | 4 | `boosting-round` | rq-ml | numeric, 360 | Targets 1, 3, 8, 12, start at the mean, one stump on the residuals, learning rate 0.5. The training mean squared error after one round. Key 6.5 (tol 0.0005) | 18.5 (the error before any round), 2.5 (a full step, rate 1) | A search of all three splits picks {1, 3} and {8, 12} (residual sums of squares 40.7, 10, 26); then errors −3, −1, 0, 4 give 26/4; and by hand with the rate-1 and start values 2.5 and 18.5 |

Coverage of the machine learning skill: boosting is M6. Regularisation is M1 and M2. PCA is M4. Bias and variance is M5. Leakage is M3.

### Paper 3: coding (45 min, 2 items, both fixed)

Python, hidden tests, free navigation. The two items are the researcher's usual coding test, a regression written by hand and then made fast. Both use only the standard library. The check `python3 -I research_mocks.py` runs every reference against an exact method on `Fraction`s. It also proves the textbook formula fails the shifted-data test.

**C1, `fit-line`** (difficulty 4, skills `rq-data`, `rq-stats`, tag `fit-line-weights`, `pace` 1,500). An item with `parts`, a requirement added part-way, as a live round does it.

- Stem: "Write the least-squares line through some points, then change it when the interviewer adds a requirement."
- **Part 1, code (Python).** `weighted_line_fit(xs, ys)` returns `[slope, intercept]`. It raises `ValueError` for fewer than two points, lists of different lengths, or all `xs` equal. Part 1 starter: the signature with a `...` body. Its own hidden tests are the 8 of the first table. The shifted-data test (5) fails the textbook sums. Their denominator is exactly 0.0 in floating point, so the learner must centre.
- **Part 2, code (Python).** "The interviewer says some points are measured more precisely. Add `weights`, one positive number per point, used as weighted least squares." Signature `weighted_line_fit(xs, ys, weights=None)`. The part 2 starter shows the part 1 reference solution. Its own tests are the 5 of the second table; the part 1 tests run too (13 in all, under the 15 cap).
- **Part 3, choice.** "A point's noise standard deviation is $\sigma_i$. Which weights are best?" Key: $1/\sigma_i^2$. Distractors: $1/\sigma_i$ (you used the standard deviation, not the variance). $\sigma_i^2$ (you gave noisy points more weight). Equal weights (you ignored the information).

Reference `weighted_line_fit` (parts 1 and 2; part 1 starts without `weights`):

```python
def weighted_line_fit(xs, ys, weights=None):
    n = len(xs)
    if n != len(ys) or (weights is not None and len(weights) != n) or n < 2:
        raise ValueError("need matching lists of at least two points")
    w = weights if weights is not None else [1.0] * n
    sw = sum(w)
    mx = sum(wi * x for wi, x in zip(w, xs)) / sw
    my = sum(wi * y for wi, y in zip(w, ys)) / sw
    sxx = sum(wi * (x - mx) ** 2 for wi, x in zip(w, xs))
    if sxx == 0:
        raise ValueError("all x values are equal")
    sxy = sum(wi * (x - mx) * (y - my) for wi, x, y in zip(w, xs, ys))
    slope = sxy / sxx
    return [slope, my - slope * mx]
```

Part 1 hidden tests (`weighted_line_fit(xs, ys)`):

| # | Call | Expected | Compare |
| --- | --- | --- | --- |
| 1 | `weighted_line_fit([1, 2, 3, 4], [2, 3, 5, 4])` | `[0.8, 1.5]` | isclose, tol rel 1e-9 and abs 1e-9 |
| 2 | `weighted_line_fit([0, 10], [100, 200])` | `[10.0, 100.0]` | isclose, tol rel 1e-9 and abs 1e-9 |
| 3 | `weighted_line_fit([3, 1, 2], [30, 10, 25])` | `[10.0, 1.6666666666666679]` | isclose, tol rel 1e-9 and abs 1e-9 |
| 4 | `weighted_line_fit(list(range(100000)), [3 * i + 7 for i in range(100000)])` | `[3.0, 7.0]` | isclose, tol rel 1e-9 and abs 1e-9 |
| 5 | `weighted_line_fit([1e8 + 3, 1e8 + 4, 1e8 + 5, 1e8 + 6], [2, 5, 4, 8])` | `[1.7, -170000002.9]` | isclose, tol rel 1e-9 and abs 1e-9 |
| 6 | `weighted_line_fit([5, 5, 5], [1, 2, 3])` | raises `ValueError` | raises |
| 7 | `weighted_line_fit([1], [2])` | raises `ValueError` | raises |
| 8 | `weighted_line_fit([1, 2, 3], [4, 5])` | raises `ValueError` | raises |

Part 2 adds these hidden tests (the part 1 tests run too, 13 in all):

| # | Call | Expected | Compare |
| --- | --- | --- | --- |
| 1 | `weighted_line_fit([1, 2, 3, 4], [2, 3, 5, 4], [1, 1, 1, 1])` | `[0.8, 1.5]` | isclose, tol rel 1e-9 and abs 1e-9 |
| 2 | `weighted_line_fit([0, 1, 2], [1, 3, 2], [1, 1, 4])` | `[0.2857142857142857, 1.5714285714285714]` | isclose, tol rel 1e-9 and abs 1e-9 |
| 3 | `weighted_line_fit([1, 2, 3], [2, 4, 7], [0.5, 1.0, 2.0])` | `[2.6153846153846154, -0.9230769230769225]` | isclose, tol rel 1e-9 and abs 1e-9 |
| 4 | `weighted_line_fit([0, 10], [5, 7], [1, 1000])` | `[0.19999999999999998, 5.0]` | isclose, tol rel 1e-9 and abs 1e-9 |
| 5 | `weighted_line_fit([1, 2, 3], [2, 4, 7], [1, 1])` | raises `ValueError` | raises |

Reference `rolling_slopes`:

```python
def rolling_slopes(xs, ys, w):
    sx = sy = sxx = sxy = 0
    out = []
    for i in range(len(xs)):
        sx += xs[i]; sy += ys[i]; sxx += xs[i] * xs[i]; sxy += xs[i] * ys[i]
        if i >= w:
            j = i - w
            sx -= xs[j]; sy -= ys[j]; sxx -= xs[j] * xs[j]; sxy -= xs[j] * ys[j]
        if i >= w - 1:
            den = w * sxx - sx * sx
            out.append(None if den == 0 else (w * sxy - sx * sy) / den)
    return out
```

Hidden tests:

| # | Call | Expected | Compare |
| --- | --- | --- | --- |
| 1 | `rolling_slopes([1, 2, 3, 4, 5], [2, 4, 5, 4, 5], 3)` | `[1.5, 0.0, 0.0]` | isclose, tol rel 1e-9 and abs 1e-9 |
| 2 | `rolling_slopes([1, 2, 3], [2, 4, 7], 3)` | `[2.5]` | isclose, tol rel 1e-9 and abs 1e-9 |
| 3 | `rolling_slopes([1, 2, 3], [2, 4, 7], 4)` | `[]` | equal |
| 4 | `rolling_slopes([0, 1, 2, 3], [5, 5, 5, 5], 2)` | `[0.0, 0.0, 0.0]` | isclose, tol rel 1e-9 and abs 1e-9 |
| 5 | `rolling_slopes([4, 2, 9, 1, 7, 3], [8, 1, 6, 2, 9, 5], 2)` | `[3.5, 0.7142857142857143, 0.5, 1.1666666666666667, 1.0]` | isclose, tol rel 1e-9 and abs 1e-9 |
| 6 | `[s is None for s in rolling_slopes([1, 1, 1, 2, 3], [1, 2, 3, 4, 9], 3)]` | `[True, False, False]` | equal |
| 7 | `len(rolling_slopes(list(range(10)), list(range(10)), 10))` | `1` | equal |
| 8 | `sum(rolling_slopes([i % 10 for i in range(200000)], [(i * i) % 97 for i in range(200000)], 1000))` | `1.007939393939394` | isclose, tol rel 1e-9 and abs 1e-9 |
| 9 | `rolling_slopes(list(range(200000)), [2 * i + 1 for i in range(200000)], 50000)[-1]` | `2.0` | isclose, tol rel 1e-6 |
| 10 | `len(rolling_slopes(list(range(200000)), [i % 7 for i in range(200000)], 50000))` | `150001` | equal |


**C2, `rolling-slope`** (difficulty 4, skills `rq-data`, tag `rolling-slope`, `pace` 1,200, a single `code` item). Statement: "`rolling_slopes(xs, ys, w)` returns a list of slopes. Each is the least-squares slope of `ys` on `xs` over `w` neighbouring points. Use full windows only, in order. `w` is at least 2. If all `xs` in a window are equal, that slope is `None`." Starter: the signature with a `...` body. The textbook loop is $O(nw)$ and runs about $2 \times 10^8$ steps on test 8, so it stops on the clock; the reference keeps running sums in whole numbers, which stay exact. Test 8 is checked against exact `Fraction` slopes from scratch on every 4,000th window. It is also checked against the exact total of all 199,001 slopes. A version with float running sums passes it, and the script runs one. So the tolerances are fair.

### Paper 4: the open case (45 min, 2 `longform`)

Each prompt says to say the answer aloud first, then type it in at most 250 words. Each `model` is a spoken answer of at most 180 words, labelled as an example. Rubrics sum to 10. No firm is named.

**Case A, `open-case-framing`** (difficulty 4, skills `rq-case`, `rq-stats`, `pace` 1,200). Prompt: "An interviewer says: predict whether an index future rises tomorrow. You test a model on 1,000 days and it calls the direction right on 523 of them. A coin gets 500. Frame the problem, then say whether 523 is evidence of skill."

- Numbers: standard error of a hit rate $\sqrt{0.25/1000} = 1.58$ points; $z = 0.023 / 0.01581 = 1.455$; two-sided $p = 0.146$ (by `erfc` and by Simpson integration of the density, agreeing to 1e-9).
- Rubric (10): the target, horizon and loss stated (2); the coin baseline stated as 50% (1); the standard error 1.58 points and $z$ about 1.45 (2); $p$ about 0.15, so not significant on its own (2); one honest limit, such as models tried, costs, or test days after training days (2); a next step with a stopping rule (1).

**Case B, `open-case-signal`** (difficulty 5, skills `rq-case`, `rq-stats`, `pace` 1,500). Prompt: "Your signal has correlation 0.04 with next-day return over 1,000 days. A colleague says it is small but real, because the t-statistic is over one. Respond, and say what you would do next."

- Numbers: $t = 0.04\sqrt{998}/\sqrt{1 - 0.0016} = 1.265$; $R^2 = 0.16\%$; the 95% interval for the correlation by the Fisher transform, $z = \operatorname{arctanh}(0.04) = 0.04002$ with standard error $1/\sqrt{997}$, gives $-0.022$ to $0.102$. The script checks $t$ against exact square roots, arctanh against its series, and tanh against its exponential form.
- Rubric (10): $R^2$ of 0.16% (1); $t$ is 1.27, below 2, so not significant (2); the interval spans zero, $-0.02$ to $0.10$ (2); a small true correlation can still matter at scale, but costs and turnover decide it (2); time-order and leakage checks before trusting it (1); a decision and a next test, such as a longer sample or another market (2).

### Generation, voice and acceptance

**Scripts** (all in `docs/briefs/mocks-scripts/`, standard library; NumPy only for a third check on M4): `research_mocks.py` for every number and both coding items, `fresh.py` for duplicates, `voice.py` for the voice rules. Run `python3 -I research_mocks.py`: it ends `ALL AGREE` and writes `keys.json`, the family and key of every item of the three mocks.

**Freshness.** `fresh.py` greps each item's own figures against all courses, exams, the bank, drills and the other briefs. A first draft repeated three things in the courses. A correlation-limits item was identical to `research-int` review-1 (0.6 and 0.8, range 0 to 0.96). A two-regressions item was identical to the same review (slopes 0.9 and 0.4, $r^2 = 0.36$). A conditional-normal item matched `eigen` l16 and homework-4 (standard deviations 2 and 3, correlation 0.5). All three have new figures here. Other hits were read in context and were coincidences. The `parts` stems and ML items use ideas the `research-int` lessons teach, as a superday does. They use none of their numbers.

**Feedback and explain.** Numeric and choice items: `feedback.correct` names the move in one clause. `feedback.generic` gives the first step. `explain.text` shows the calculation and its second check in at most three sentences. Longform: `model` and `rubric` only.

**Voice scan.** `python3 -I docs/briefs/mocks-scripts/voice.py`, then `docs/reviews/voice-scan.py` on a folder holding the exam file: 0 and 0. Model answers count as prose.

**Skills covered.** `rq-stats`, `rq-linalg`, `rq-ml`, `rq-case`, `rq-data`.

**Prerequisites** (cited in the report, nothing gated): `research-int` l1 to l5, l6 to l10, l11 to l15, l16 to l20 and review-1 to review-4; `coding-int` l17-two-in-sixty and l18-talking-while-coding; `recruiting` l11-stories-that-answer and l13-the-final-round.

**Engine notes.** Built and used: `parts` with `code`, `choice` and `numeric` parts in one item (467, C-parts-code, C-parts-mixed). Also `draw` from a bank (468), `longform` in a mock, and per-part credit in an exam (C-parts-credit). Nothing is missing. No engine requirement is raised.

**Acceptance.**

1. `node tools/validate.mjs 2>&1 | tail -5` reports 0 errors.
2. `node tools/playthrough.mjs --exam mock-superday-research --local-cdn <pkgs> 2>&1 | tail -30` is green, and again with `--mobile`. The playthrough opens every part of the three `parts` items and runs both code parts with the reference solutions. It draws four bank items and ticks every rubric point of both case items.
3. The start card lists four papers and both checks. The papers are 45, 30, 45 and 45 minutes, 165 in all, with 18 questions. Two sittings draw different probability questions.
4. Every key above is asserted twice in `research_mocks.py`; the report lists each item's answer and computations.
5. Report at `docs/reports/exam-mock-superday-research.md`. Add inbox bullets under `Raised later (exam mock-superday-research):`. One asks for statistics and machine learning families in the bank. Research banks 1 to 4 are not written. Another reports the NaN pass mark, if it shows.

## mock-oa-quant-data

**File.** `app/content/exams/mock-oa-quant-data.json`, one file, no versions. The items are fixed. There is no bank family for statistics yet. A drawn pool of Python data drills would need a data file for each. So the plan's "E3 for fresh draws" is not used here. Each sitting still differs where it matters little and repeats where it teaches: the learner meets the same three tasks, with options shuffled. The report raises one inbox bullet for statistics and applied-maths bank families, which would let paper 1 draw.

- `id`: `mock-oa-quant-data`. `name`: `Quantitative data assessment`. `style`: `research`.
- `models` (under 200 characters): `Reported, as of Nov 2026: online assessments for quant research and quant finance internships at Morgan Stanley and Two Sigma: statistics and applied maths questions, then Python data tasks.`
- `skills`: `{ "rq-stats": "Statistics questions", "rq-linalg": "Linear algebra questions", "rq-ml": "Machine learning questions", "rq-data": "Data tasks" }`.

**Description** (plain, each sentence under 20 words):

> This is the reported format of an online quant assessment, as candidates described it by Nov 2026. It has two papers and takes 120 minutes. The first has 10 statistics and applied maths questions, and some ask you to select all that apply. The second has three Python data tasks that read CSV files. Hidden tests check each task, so run your code before you move on. Use only the standard documentation of the libraries. Use no search engine and no notes.

**Parts.**

| # | Paper `id`, name | Minutes | Items | Pass | `pace` sum |
| --- | --- | --- | --- | --- | --- |
| 1 | `stats`, Statistics and applied maths | 40 | 10 (6 `numeric`, 1 with `parts`, 1 `choice`, 2 `multi`) | `pass: 0.6` (6 of 10) | 2,280 s |
| 2 | `data`, Python data tasks | 80 | 3 `code` items with `data` files | `pass: 0.6` (2 of 3) | 4,500 s |
| 3 | check `no-lookup`, `I used no search engine and no notes`, detail `Tick this only if you sat both papers without either.` | | | | |

Both papers use `scoring: { "right": 1, "wrong": 0, "blank": 0 }` and free navigation. That is 13 items and 120 minutes. The attempt passes only when both papers pass and the check is ticked. The plan said 2 to 3 data tasks. This takes 3, because the files are cheap and the 80 minutes need them.

**Rules.** As the shared rules and `mock-superday-research`: `shuffle: true` on every `choice` and `multi`, a `why` on every distractor, no key between a times-ten pair or equal slips, named `wrong` values with `byKey` lines, `tags`, `pace`, `skills` and `difficulty` on every item. A `multi` question line says "Select all that apply". Money is not used; percentages use `unit: "%"` (the learner types 14.2 and the engine stores 0.142).

### Paper 1: statistics and applied maths (40 min, 10 items)

Ramp: 2 at difficulty 2 (Q1, Q2). 5 at 3 (Q3 to Q7). 2 at 4 (Q8, Q9). 1 at 5 (Q10). Skills `rq-stats` except where shown.

| Q | Diff | Tag | Skill | Kind, `pace` | Question and key | `wrong` or options, with the slip | Computed twice |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | `standard-error` | rq-stats | numeric, 150 | 36 daily returns have sample standard deviation 12 basis points. The half-width of a 95% interval for the mean, with 1.96 as the multiplier. Key 3.92 (tol 0.005) | 2.0 (gave the standard error, not the interval), 23.52 (forgot to divide by $\sqrt n$) | $1.96 \times 12/6 = 98/25$; and $\sqrt{144/36} \times 1.96$ |
| 2 | 2 | `p-value-meaning` | rq-stats | choice, 120 | A study reports $p = 0.03$ for a strategy's mean return. What does that mean? Key: if the true mean were zero, a result this extreme would occur about 3% of the time | There is a 3% chance the strategy has no edge (that is the chance of the hypothesis, which a p-value is not); the strategy has a 97% chance of working (a p-value is not the chance an edge exists); the mean return is 3% (a p-value is not an effect size). Options of near equal length | No number to check |
| 3 | 3 | `t-statistic` | rq-stats | numeric, 180 | Mean excess return 1.8 basis points a day, sample standard deviation 5, 25 days, null mean zero. The t-statistic. Key 1.8 (tol 0.005) | 9.0 (divided by $s/n$, not $s/\sqrt n$), 0.36 (divided by $s$ only) | $1.8 / (5/5)$; and $\sqrt{n \bar x^2 / s^2} = \sqrt{3.24}$ |
| 4 | 3 | `ols-facts` | rq-stats | multi, 240 | Which statements about least squares with an intercept always hold in the sample? Select all that apply. Key (3 of 6): the residuals sum to zero; the fitted line passes through the point of the means; $R^2$ cannot fall when a predictor is added | The residuals are normally distributed (that is an assumption about errors, not a fact of the fit); the slope's t-test is valid for any errors (it needs the usual assumptions); adjusted $R^2$ cannot fall when a predictor is added (it can) | A worked 5-point fit on exact `Fraction`s (residuals sum to 0, the line meets the means), and 2,000 seeded exact fits where the sum of squared residuals never rises when a column is added, while adjusted $R^2$ fell in 1,285 of them |
| 5 | 3 | `adjusted-r2` | rq-stats | numeric, 210 | $n = 50$ observations, $k = 4$ predictors, $R^2 = 0.40$. The adjusted $R^2$. Key 0.3467 (tol 0.0005) | 0.40 (reported $R^2$), 0.3609 (used $n - k$ in place of $n - k - 1$) | $1 - 0.6 \times 49/45 = 26/75$, and $0.4 - 0.6 \times 4/45$ |
| 6 | 3 | `bivariate-normal` | rq-stats | `parts` (numeric, numeric), 300 | $X$ has mean 1 and sd 3, $Y$ has mean 4 and sd 2, correlation 0.6. **Part 1:** $E[Y \mid X = 5]$, key 5.6 (tol 0.005). **Part 2:** the sd of $Y$ given $X = 5$, key 1.6 (tol 0.005) | Part 1: 4.0 (the unconditional mean), 6.4 (used the correlation as the slope). Part 2: 2.0 (the unconditional sd), 1.2 (used $\rho \sigma_y$) | $4 + 0.6 \times \tfrac23 \times 4 = 28/5$ and $\sqrt{4(1 - 0.36)} = \sqrt{2.56} = 1.6$; and the matrix form $\Sigma_{yy} - \Sigma_{yx}\Sigma_{xx}^{-1}\Sigma_{xy}$ |
| 7 | 3 | `portfolio-sd` | rq-stats | numeric, 240 | Two assets with volatility 20% and 30%, correlation −0.3, weights 60% and 40%. The portfolio volatility, in %. Key 14.2 (tol 0.05) | 24.0 (weighted the volatilities), 17.0 (left out the covariance term) | The expanded variance $0.0144 + 0.0144 - 0.00864 = 0.02016$ and the matrix form $w^T \Sigma w$ as `Fraction`s; $\sqrt{0.02016} = 0.1420$ |
| 8 | 4 | `min-variance-weight` | rq-linalg | numeric, 270 | Volatility 25% and 20%, correlation 0.3. The minimum-variance weight in the 25% asset. Key 0.3448 (tol 0.0005) | 0.3902 (inverse-variance weights, which ignore the correlation), 0.5 (equal weights) | $(\sigma_2^2 - c)/(\sigma_1^2 + \sigma_2^2 - 2c) = 10/29$ with $c = 0.015$; and the exact variance on a grid of 1/290 |
| 9 | 4 | `cv-leakage` | rq-ml | multi, 270 | You cross-validate a return-prediction model. Which choices avoid leakage? Select all that apply. Key (3 of 6): train on earlier rows and test on later rows; fit the scaler on the training fold only; leave a gap between training and test when labels overlap | Shuffle the rows before splitting (later rows leak into training); pick the model with the best score on the test fold over many tries (the test fold becomes training data for the choice); standardise with the whole sample (the test rows set the scale) | No number to check |
| 10 | 5 | `compound-poisson` | rq-stats | numeric, 300 | Trades arrive as a Poisson process, 4 an hour. Each size has mean 10 and standard deviation 5, independent of the count. The variance of the total size in an hour. Key 500 (tol 0) | 100 (only the variance of the sizes, $4 \times 25$), 400 (only the spread of the count, $4 \times 100$), 40 (gave the mean) | $\lambda(\sigma^2 + \mu^2) = 4 \times 125$ by the law of total variance, and the sum over $N$ from 0 to 79 of $P(N = n)(n\sigma^2 + n^2\mu^2) - (\lambda\mu)^2$ |

`pace` sums to 2,280 s (38 minutes), so a learner has 2 minutes spare. For Q2, Q4 and Q9 the author writes the options from the table. Each wrong option has a `why` that names the action. An example is "You read the p-value as the chance the strategy has no edge." `byKey` lines for each `wrong` id: one clause, for example "You divided by the sample size, not its square root."

### Paper 2: Python data tasks (80 min, 3 `code` items)

The data is in three new files. The generator is `docs/briefs/mocks-scripts/gen_qd_data.py`. It is pure Python with a 32-bit linear congruential generator and fixed seeds. No library version changes a byte. Copy its output to `app/content/data/qd/` and the script to `app/tools/gen-qd-data.py`. Each file is read by bare name from a `data` field on the item's `code` widget: `"data": { "qd-prices.csv": "content/data/qd/qd-prices.csv" }`, and likewise for the others. All three are far under the 256 KB cap.

| File | Columns | Rows | Planted problems | Size | SHA-256 starts |
| --- | --- | --- | --- | --- | --- |
| `qd-prices.csv` | `date`, `ticker`, `close` | 783 | 260 weekdays for each of KAPPA, LAMBDA, MU; 7 blank closes; 3 exact repeated rows; rows shuffled | 17,550 bytes | `075ba1d7e21c18f1` |
| `qd-pair.csv` | `date`, `asset`, `mkt` | 520 | daily returns; 3 asset returns typed as whole percents (0.31, −0.28, 0.35) | 15,613 bytes | `31b8bee8e889386e` |
| `qd-signal.csv` | `date`, `x1`, `x2`, `ret` | 800 | next-day return depends weakly on yesterday's `x1` and `x2` | 31,659 bytes | `9a44408ce52afff1` |

(Check each hash with `python3 -I gen_qd_data.py`, which prints size and hash; the three above are its last output.)

Library note: the check script ran with NumPy 2.5.3 and pandas 3.0.5. Pyodide has NumPy 2.0.2 and pandas 2.2.3. Every reference uses only calls that mean the same in both. The second method is pure Python on `Fraction`s read from the decimal text. So it does not depend on either. The mock author reruns every hidden test in the real playthrough, which uses Pyodide.

**Task 1, `qd-returns`** (difficulty 3, skills `rq-data`, tag `return-table`, `pace` 1,200). Statement: "`qd-prices.csv` has one close a day for three tickers. The rows are not in date order. Some closes are blank, and some rows repeat. Write `tidy_closes()` and `vol_by_ticker()`." `tidy_closes()` returns a frame with the columns `date`, `ticker` and `close`. It drops repeated rows and blank closes. It sorts by ticker, then date. `vol_by_ticker()` returns a dict from ticker to annualised volatility: the sample standard deviation (`ddof=1`) of the daily log returns within each ticker, times $\sqrt{252}$. A return spans two rows where a blank was dropped. Starter: both signatures with `...` bodies.

The tests catch four wrong versions the script builds: no repeat removal, a log return taken across tickers, `ddof=0`, and no sort.

**Task 2, `qd-rolling-beta`** (difficulty 4, skills `rq-data`, `rq-stats`, tag `hedge-ratio`, `pace` 1,500). Statement: "`qd-pair.csv` has daily returns for an asset and the market. Three asset returns were typed as whole percents. A return with size above 0.25 in either column is a data error: drop that row. Then write `windowed_betas(window)`. It returns one least-squares slope of `asset` on `mkt` per window of `window` neighbouring remaining rows. Use date order and full windows only." Starter: the signature with a `...` body. A version that keeps the errors returns 461 windows, not 458, and a different sum.

**Task 3, `qd-out-of-sample`** (difficulty 5, skills `rq-data`, `rq-ml`, `rq-case`, tag `out-of-sample`, `pace` 1,800). Statement: "`qd-signal.csv` has two signals and the return of each day. Predict a day's return from the signals of the day before. Write `oos_scores(split)`. Row $t$ has the features of row $t - 1$ and the target `ret` of row $t$, for $t = 1$ to 799. Fit least squares with an intercept on the first `split` of these rows. Return a dict with `coef` (intercept, then the two slopes), `train_r2` and `oos_r2`. The out-of-sample score uses the remaining rows. Its baseline is the training mean of the target." Starter: the signature with a `...` body. The tests catch three wrong versions. Unlagged features give an out-of-sample $R^2$ of −0.0057 against 0.0577. The test-set mean as baseline gives 0.05765, which a tolerance of 1e-8 separates. A fit on every row gives 0.05801.

##### Reference for `qd-returns`

```python
import numpy as np
import pandas as pd

def tidy_closes():
    df = pd.read_csv("qd-prices.csv")
    df = df.drop_duplicates().dropna(subset=["close"])
    return df.sort_values(["ticker", "date"]).reset_index(drop=True)

def vol_by_ticker():
    df = tidy_closes()
    out = {}
    for ticker, g in df.groupby("ticker"):
        r = np.log(g["close"]).diff().dropna()
        out[ticker] = float(r.std(ddof=1) * np.sqrt(252))
    return out
```

| # | Call | Expected | Compare |
| --- | --- | --- | --- |
| 1 | `len(tidy_closes())` | `773` | equal |
| 2 | `int(tidy_closes()['close'].isna().sum())` | `0` | equal |
| 3 | `list(tidy_closes().columns)` | `['date', 'ticker', 'close']` | equal |
| 4 | `int(tidy_closes().duplicated().sum())` | `0` | equal |
| 5 | `tidy_closes().groupby('ticker').size().to_dict()` | `{'KAPPA': 258, 'LAMBDA': 257, 'MU': 258}` | equal |
| 6 | `bool(tidy_closes().groupby('ticker')['date'].apply(lambda s: s.is_monotonic_increasing).all())` | `True` | equal |
| 7 | `sorted(vol_by_ticker())` | `['KAPPA', 'LAMBDA', 'MU']` | equal |
| 8 | `vol_by_ticker()['KAPPA']` | `0.1760834506309832` | isclose (tol {"rel": 1e-09}) |
| 9 | `vol_by_ticker()['LAMBDA']` | `0.25816881352482823` | isclose (tol {"rel": 1e-09}) |
| 10 | `vol_by_ticker()['MU']` | `0.3577200967909071` | isclose (tol {"rel": 1e-09}) |

##### Reference for `qd-rolling-beta`

```python
import numpy as np
import pandas as pd

def windowed_betas(window):
    df = pd.read_csv("qd-pair.csv")
    df = df[(df["asset"].abs() <= 0.25) & (df["mkt"].abs() <= 0.25)]
    x = df["mkt"].to_numpy()
    y = df["asset"].to_numpy()
    out = []
    for i in range(len(x) - window + 1):
        xs, ys = x[i:i + window], y[i:i + window]
        out.append(float(np.cov(xs, ys, ddof=1)[0, 1] / np.var(xs, ddof=1)))
    return out
```

| # | Call | Expected | Compare |
| --- | --- | --- | --- |
| 1 | `len(windowed_betas(60))` | `458` | equal |
| 2 | `windowed_betas(60)[0]` | `0.8032989217239858` | isclose (tol {"rel": 1e-09}) |
| 3 | `windowed_betas(60)[-1]` | `1.382877464391472` | isclose (tol {"rel": 1e-09}) |
| 4 | `sum(windowed_betas(60))` | `502.3786453492044` | isclose (tol {"rel": 1e-09}) |
| 5 | `min(windowed_betas(120))` | `0.8194411434696784` | isclose (tol {"rel": 1e-09}) |
| 6 | `max(windowed_betas(120))` | `1.425200190403877` | isclose (tol {"rel": 1e-09}) |
| 7 | `windowed_betas(600)` | `[]` | equal |
| 8 | `windowed_betas(517)[0]` | `1.0877069411378124` | isclose (tol {"rel": 1e-09}) |

##### Reference for `qd-out-of-sample`

```python
import numpy as np
import pandas as pd

def oos_scores(split):
    df = pd.read_csv("qd-signal.csv")
    X = np.column_stack([np.ones(len(df) - 1), df["x1"].to_numpy()[:-1], df["x2"].to_numpy()[:-1]])
    y = df["ret"].to_numpy()[1:]
    Xtr, ytr, Xte, yte = X[:split], y[:split], X[split:], y[split:]
    coef, *_ = np.linalg.lstsq(Xtr, ytr, rcond=None)
    train_r2 = 1 - np.sum((ytr - Xtr @ coef) ** 2) / np.sum((ytr - ytr.mean()) ** 2)
    oos_r2 = 1 - np.sum((yte - Xte @ coef) ** 2) / np.sum((yte - ytr.mean()) ** 2)
    return {"coef": [float(c) for c in coef], "train_r2": float(train_r2), "oos_r2": float(oos_r2)}
```

| # | Call | Expected | Compare |
| --- | --- | --- | --- |
| 1 | `sorted(oos_scores(500))` | `['coef', 'oos_r2', 'train_r2']` | equal |
| 2 | `oos_scores(500)['coef']` | `[0.00025424269185633027, 0.0022966524429744854, -0.0015904841020325...` | isclose (tol {"rel": 1e-08}) |
| 3 | `oos_scores(500)['train_r2']` | `0.08363857338496772` | isclose (tol {"rel": 1e-08}) |
| 4 | `oos_scores(500)['oos_r2']` | `0.057702003278431` | isclose (tol {"rel": 1e-08}) |
| 5 | `oos_scores(300)['coef']` | `[0.000512415044256865, 0.0018296538844713329, -0.001413107004839858]` | isclose (tol {"rel": 1e-08}) |
| 6 | `oos_scores(300)['oos_r2']` | `0.08668570838518808` | isclose (tol {"rel": 1e-08}) |
| 7 | `oos_scores(600)['oos_r2']` | `0.052537017793764074` | isclose (tol {"rel": 1e-08}) |


**Scoring.** A task is right when every hidden test passes. The pass mark is two of three. As in `mock-oa-code`, the engine gives no share-of-tests credit on a code item. The results panel lists each test.

### Generation, voice and acceptance

**Scripts** (`docs/briefs/mocks-scripts/`): `gen_qd_data.py` writes the three files; `qd_tasks.py` needs NumPy and pandas for the references, and `gen_qd_data.py` must run first. It computes every task's expected values twice and builds the wrong versions. It asserts the tests catch them and writes `qd_tasks_tests.json`; `research_mocks.py` checks the paper 1 keys; `fresh.py`, `voice.py`. Last output: `qd_tasks.py` ended `ALL AGREE: 3 tasks`, `research_mocks.py` ended `ALL AGREE`.

**Numbers worth stating, each from the scripts.** Task 1: 773 rows remain, 258, 257 and 258 closes for the three tickers (one return fewer each); volatilities 0.17608 (KAPPA), 0.25817 (LAMBDA), 0.35772 (MU). Task 2: 458 windows of 60, first beta 0.8033, last 1.3829, full-sample beta 1.0877. Task 3: coefficients 0.000254, 0.002297, −0.00159; training $R^2$ 0.0836, out-of-sample $R^2$ 0.0577 at split 500.

**Freshness.** `fresh.py` found no repeat of a function name, file name or figure. It searched every course, exam, bank file, drill and brief. Two paper 1 drafts repeated courses. The conditional normal matched `eigen` l16, which uses standard deviations 2 and 3 and correlation 0.5. The minimum-variance weight matched `topic-1.4`, which uses variances 0.04 and 0.09. So Q6 and Q8 have new figures. The `research-int` L4 lessons use other files (`ticks-gaps.csv`, `towns-temp.csv`, `orders-messy.csv`, `houses.csv`). They set other tasks. So none of this mock's data or numbers repeats there.

**Feedback and explain.** As `mock-superday-research`. A code item has `feedback.correct`, `feedback.generic` and an `explain` of at most three sentences. The `explain` names the trap (a stacked-frame `diff`, the data errors, the look-ahead).

**Voice scan** and **skills covered** (`rq-stats`, `rq-linalg`, `rq-ml`, `rq-data`, with `rq-case` on task 3) as the other mocks.

**Prerequisites** (cited in the report, nothing gated): `research-int` l1 to l5, l16-interpolating, l17-regression-by-group, l18-updating-a-fit, l19-timed-data-task; `numpy-pandas` l7-gaps and l12-split-apply-combine; `regression` l12-matching-statsmodels; `validation` l6-walking-forward.

**Engine notes.** Built and used: `data` on exam `code` widgets (469), `parts` with numeric parts (467), `multi`, `unit: "%"`. Nothing is missing, so no engine requirement is raised. One limit is said plainly: marks are per task, as in `mock-oa-code`.

**Acceptance.**

1. `node tools/validate.mjs 2>&1 | tail -5` reports 0 errors, with the three data files found and each under 256 KB.
2. `node tools/playthrough.mjs --exam mock-oa-quant-data --local-cdn <pkgs> 2>&1 | tail -30` is green and again with `--mobile`: every starter fails, every reference passes every hidden test inside the limits, and pandas loads once.
3. The start card lists two papers (40 and 80 minutes, 120 in all, 13 questions) and the check.
4. Each task's wrong versions fail at least one test (the script proves it locally; the playthrough or a scratch run in Pyodide confirms it).
5. Report at `docs/reports/exam-mock-oa-quant-data.md`. Add inbox bullets under `Raised later (exam mock-oa-quant-data):`. One asks for statistics and applied-maths bank families. Another asks for a `language` filter on `draw`. A mixed Python and C++ pack cannot feed a Python mock.
