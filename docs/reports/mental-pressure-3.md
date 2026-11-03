# Report: mental-pressure level 3 (Test formats)

Status: complete. Course `mental-pressure`, topic 3.3; brief `docs/briefs/mental-pressure.md` `## Level 3`, with the orchestrator's additions: a follow-up screen in every lesson, a stated pace on every drill, `tags` on every drill, review and homework item, `shuffle: true` on every choice, `longform` in homework only, no firm named ("some firms", "candidates report"). Ids, names, objectives and skills are from `course.json` (`mp-formats` on every lesson, `mp-speed` also on l9 and l12). Generators, the code harness and screenshots are in the scratchpad folder `mental-pressure-3` (`mockgen.py`, `candidate.py`, `common.py`, `h.py`, `l9.py` to `l12.py`, `sets.py`, `prelude_hw.py`, `codecheck.py`, `listing.md`, `shots/`).

## Files

All in `app/content/courses/mental-pressure/`. Nothing else was edited except this report and `docs/BACKLOG-INBOX.md`; the validator rewrote `content/manifest.json`.

| File | Screens or items | Canvases and widgets | Code |
|---|---|---|---|
| `l9-eighty-in-eight.json` | 11 screens, 4 quiz | table (format); number-line with a dragged "You" point and a derived caption (explore); number-line with three dragged checkpoints, graded (drag-point); table with `tap: "rows"` for the skip knapsack (tap-regions); 20-row four-option block (seed 9); guess-value table; order with a distractor | `best_skips`, `checkpoint_times`, 12 tests |
| `l10-next-in-sequence.json` | 12 screens, 4 quiz | table of differences switched by a four-frame control (explore); difference-table widget for 2, 6, 12, 20, 30; ratio and known-list tables; order of the four tests with a distractor; 12-sequence drill | `difference_table`, `next_by_differences`, 13 tests |
| `l11-word-problems.json` | 12 screens, 4 quiz | number-line clock 14:40 to 18:00 with a dragged arrival, a derived journey bar and an HH:MM caption (explore, drag-point); one-line table; `expression` derive $\tfrac{Prm}{1200}$; 10-problem drill | `minutes_between`, `simple_interest`, 12 tests |
| `l12-mock-test.json` | 12 screens, 4 quiz | four 20-row four-option blocks (seed 80) on an 8-minute number-line; `bars` of the seed-81 candidate by kind with a two-frame control (explore); net-score table; S/M/T sort table; tap-rows trap on block 3; `expression` derive $2r - a$ | none (the brief asks for none) |
| `review-3.json` | 10 items, difficulty 2 to 4, `timed: { "seconds": 300, "lockAtZero": false }` (a guide clock; grading never depends on it) | numeric, choice | |
| `homework-3.json` | 8 items, difficulty 3 to 5 (two at 5) | two 20-row drill tables (four-option seed 31 at 6 s, 2 minutes; 10 sequences at 8 s and 10 word problems at 10 s, 3 minutes); 2 code items; an `order` review routine with two distractors and `same`; 2 numeric; a 10-point `longform` | `mock_generator` (14 tests, difficulty 5); `next_term` (13 tests, difficulty 4) |

Lesson shapes. l9: hook, explore, name (checkpoints), ladder (skip and return), ladder (a block of twenty), follow-up (the reported format), trap, generalise, derive, code, transfer. l10 and l11: hook, explore, name, two ladders, follow-up, trap, generalise, derive, code, drill, transfer. l12: four mock blocks (problem then three ladders), explore (the sample candidate), name (net score), ladder (sort errors), follow-up (pick one drill), trap, generalise, derive, transfer.

Self-timing: each lesson says once that the app does not time it (l9 block, l10 drill, l11 drill, l12 block 1), and no screen's grading depends on time. Each drill and block states a pace: l9 block 20 at 6 s (2 minutes); l10 drill 12 at 8 s (96 s); l11 drill 10 at 10 s (100 s); l12 four blocks of 2 minutes; homework 20 at 6 s (2 minutes) and 20 in 3 minutes (80 s + 100 s); review-3 a 300 s guide clock.

Follow-ups: l9 "and if you cannot skip?" (guess values −0.5, −1/3, 0 under +1/−1); l10 "the 10th term of 2, 6, 12, 20, 30" (110); l11 "the return on the trade" (3.53%); l12 "what will you practise next week?" (fractions).

Edge cases: l9 finishing early (quiz: return to skips); l10 a constant sequence (generalise); l11 unit changes (minutes to hours in the explore, pence to pounds in the quiz, midnight in review-3); l12 a perfect score at a slow pace (quiz: the next target is speed).

Traps: l9 30 s on Q3 (reaches Q76, keys "catch-up" 80 and "five-off" 75); l10 doubling 1, 2, 4 in 1, 2, 4, 7, 11 (keys 22, 8, 15), with 1, 2, 4, 8, 16, 31 given as the ambiguity warning in the explanation only; l11 "35% filled" read as left (keys 1,560, 7,680, 2,688); l12 reviewing only the wrong answers (tap-regions `wrong` set "only-wrong" = Q60 alone).

Reported format (l9 follow-up, l12): four options, +1 right, −1 wrong, forward only with no skipping, pass line "about 50 to 60 net", each marked as reported, with "rules vary by test and change each cycle". Zetamac is named once (l9 hook explanation, 2.4 s an answer at 50). The daily warm-up and its Stage 3 mark of 50 are named in l12's transfer.

Tags (family names, unchecked by the validator): lessons `drill-eighty-block` (l9 block), `drill-sequences`, `drill-word-problems`, `mock-eighty` (l12 blocks); review `checkpoints`, `sequence-differences`, `word-filled`, `net-score`, `skip-budget`, `sequence-ratio`, `word-interest`, `error-sort`, `sequence-woven`, `word-time`; homework `drill-eighty-block`, `drill-sequences` + `drill-word-problems`, `code-mock-generator`, `code-next-term`, `review-routine`, `guess-value`, `checkpoints`, `test-week-plan`.

## E1 and E4 (net scoring, generated items)

Engine pass A built net scoring (`scoring`, `passNet`) and generated `arith` items for exam papers only (AUTHORING sections 5 and 7). Lessons still cannot net-score the learner's own answers or pass a marked set to a later screen, so l12's review uses the seed-81 sample candidate, as the brief says, and the net score is computed by hand on a table. The arith generator makes whole-number four-operation items only, so the l12 mix (decimals, fractions, percentages, sequences) is a fixed paper from `mockgen.py` (below). `timed` (item 454) is used on review-3 only, as a guide clock.

## For exam authors

A timed 80-question, 8-minute paper is a natural part for the topic 3.3 or Stage 3 exam, or for `mock-oa-arith`: `scoring: { right: 1, wrong: -1, blank: 0 }`, `navigation: "forward"`, `skip: false`, `passNet` about 55 (reported 50 to 60). No exam file was written. `mockgen.mock_generator(seed, mix)` below reproduces the l12 paper for `seed = 80` and makes a fresh paper of the same structure for any other seed, so it can produce the fixed versions of `mock-oa-arith` until generators cover decimals, fractions, percentages and sequences. `mockgen.generate(seed, mix)` gives the kind and letter as well.

## Validator

`node tools/validate.mjs` from `app/`: 0 errors overall. No warnings on any level 3 file.

## Playthrough

With `--local-cdn <pkgs>`, every lesson without and with `--mobile` (and once with `--shots --why`): l9 15 checks, quiz 4/4; l10 16 checks, quiz 4/4; l11 16 checks, quiz 4/4; l12 16 checks, quiz 4/4. `--set mental-pressure/review-3`: 10 items, recorded 10 of 10. `--set mental-pressure/homework-3`: 8 of 8 right, 37 of 37 marks. All passed.

Screenshots (1280 and 390 px, with Why? sheets) were read for every explore, block, drill, code, trap, transfer and set screen. Fixes made from them: option letters bound to their values with no-break spaces so four options wrap as pairs at 390 px; question text in the l12 sort table kept on one line; a 14:47 departure label on the l11 clock; zero differences shown as 0, not +0.

Code: `codecheck.py` runs every solution and starter against every hidden test and example in CPython. All solutions pass all tests and examples; every untouched starter fails every hidden test (the l10 and homework `next_term` starters were changed so that no `None` case passes). `mock_generator` was also run over seeds 0 to 1,499 with the default mix and 300 random mixes through the hidden checks (`prelude_hw.py`): every paper passed.

## Numbers, each computed twice

Every number is asserted in the generator scripts against a second method (`fractions.Fraction`, `decimal.Decimal`, brute force or a re-derivation); a failing assert stops the file being written.

- l9: 8 min = 480 s, $480 \div 80 = 6$ s; Zetamac 50 is $120 \div 50 = 2.4$ s; checkpoints $6 \times 20, 40, 60 = 120, 240, 360$ s (2, 4, 6 minutes); explore 40 at 4 minutes. Skip table (costs 22, 25, 4, 14, 3, 5, 14, 8, 4, 6; sum 105; from a seed search, seed 95): the eight cheapest sum to 58, nine to 80; brute force over all 8-subsets confirms skipping Q71 and Q72 is the only way to answer 8, and no 9-subset fits. Guesses: $\tfrac14 - \tfrac34 = -0.5$, $\tfrac13 - \tfrac23 = -\tfrac13$, $\tfrac12 - \tfrac12 = 0$. Trap: $6 + 6 + 30 = 42$, $(480 - 42) \div 6 = 73$, reaches Q76; 24 s extra is 4 questions. Generalise $t_{60} = 360$ s. Transfer: $540 \div 60 = 9$ s; 135, 270, 405 s. Quiz: 6 behind (pace Q50 at 5 minutes, 36 s); 5 answerable from 4, 5, 6, 18, 7, 25 in 60 s (40 s used; 65 with the 25). Block (seed 9): every answer and its working line are asserted by `common.working`, a second computation per kind.
- l10: 19; explore B 1, 3, 6, 10, 15 → 21; 2, 6, 12, 20, 30 → 42 (table 4, 6, 8, 10; 2, 2, 2) and $n(n+1)$: 10th term 110 (9th 90); 48, 405, 65 ($3 \to 5 \to 9 \to 17 \to 33 \to 65$); 25, 64, 13, 13, 4; trap 1, 2, 4, 7, 11 → 16; constant 7; transfer 150, 250, 450, 850 → 1,650 (×2 − 50; same-gap slip 1,250). Drill: 24, 26, 81, 37, 36, 21, 4, 125, 16, 36, 8, 17, each by `next_by_differences`, Fibonacci or ratio and by hand. Quiz 17, 126 ($n^3 + 1$; slip 102), 16, 29.
- l11: $300 \times 0.15 = 45$ (sale value 1,320, cost 1,275); 14:47 = minute 887, +158 = 1,045 = 17:25 ($47 + 38 = 85$); $1.12 \times 0.88 = 0.9856 = 1 - 0.12^2$, −1.44%; £1,250 at 4% for 9 months £37.50 (year £50, 9 years £450, 3 months £12.50); $2.99 + 4.49 + 7.99 = 15.47 = 15.50 - 0.03$ (×4 = 61.88); return $0.15 \div 4.25 = 3.53\%$ (on £4.40, 3.41%); 35% of 2,400 = 840 (left 1,560, value £7,680 and £2,688); £2,400 at 5% for 6 months £60 (year £120, 6 years £720); $\tfrac{Prm}{1200}$ checked at 37.5; transfer $1500 \times (12.52 - 12.60) = -120$ (2,000 shares −160; bid −180). Drill: 50, −1%, 720, 11:25, 12, 11.47, 1,600, −100, 18:15, 72. Quiz £1,020 (102,000p), 85 minutes (decimal slip 165), 1,260 (2,340 open, 540 first fill), £70 ($84 \times 0.8 = 67.20$ slip). Code tests: 158, 85, 107, 0, 230 (22:35 to 02:25), 2; 37.5, 60, 12, 350, 18.75, 0.
- l12: the paper's kinds match the mix (15, 15, 10, 12, 10, 10, 8); every row has four distinct options with the answer once, and every working line recomputes its answer. Candidate (seed 81): 57 right, 11 wrong, 12 blank (ran out after Q68 at 476.4 s); net 46; blocks 16/4/0 (12), 14/6/0 (8), 19/1/0 (18), 8/0/12 (8), $12 + 8 + 18 + 8 = 46$; block seconds 120.0, 165.1, 139.0, 52.3 (sum 476.4). Means by kind for reached questions: + − 6.1, × 6.4, ÷ 7.6, decimals 5.9, fractions 8.0 (71.6 s over 9, summed by hand), % 5.5, sequences 11.1 (77.4 s over 7, by hand); wrong 1, 2, 1, 1, 5, 0, 1. Sort (blocks 1 and 2): Q8 S, Q13 M, Q14 M, Q19 M, Q21 S, Q24 M, Q26 M, Q27 M, Q30 T, Q31 T, Q34 M, Q38 M, Q40 T; M and T by kind: fractions 5, sequences 3, multiplication 2, division 1 (11 rows). Trap block 3: 20 times summed by hand to 139.0, 19 s over; Q55 18.6 s right (12.6 s beyond pace, 2.1 questions), Q60 17.0 s wrong; together 23.6 s beyond pace. Generalise 66 answered, 9 wrong: $57 - 9 = 48$. Derive $2r - a$: $2 \times 57 - 68 = 46$. Quiz: 11 minutes = 8.25 s each, 480 s reaches Q58 (22 blank); 74 answered, 14 wrong, net 46; block times 115, 130, 150, 100: 395 s at Q60, 35 s behind (block 3 alone 30, end 15).
- review-3: $600 \div 50 = 12$ s, Q30 at 360 s = 6 minutes; 3, 6, 11, 18, 27 → 38 ($6^2 + 2$); 35% of 4,800 = 1,680 (3,120 filled, £10,320); 71 answered, 13 wrong: 45; 45 s budget: 4 + 5 + 6 + 7 + 9 + 12 = 43, six answerable (63 with the 20); 4, 7, 13, 25, 49 → 97 (73, 98 slips); £3,600 at 5% for 4 months £60 (£180, £720); woven 3, 6, 12 → 24; 22:35 + 3 h 50 = 02:25 (01:35 after 3 hours, $35 + 50 = 85$).
- homework-3: seed-31 block answers by `working`; sequences 27, 1, 46, 162, 18, 35, 81, 7, 1, 72; word problems £70, 900, 17:16 ($52 + 24 = 76$), £30, £10.47, £1,400, −4%, £150, 95 minutes, £1,000; `next_term` 19, 42, 7, 48, 405, 4, 13.5, $\tfrac83$, 65, 1,650, None × 3 (asserted against the solution and by Fraction by hand); five guesses among three $5 \times (-\tfrac13) = -\tfrac53 \approx -1.67$ (blind −2.5); 60 in 10 minutes: Q24 at 4 minutes, 4 behind (6 s pace would say 20); longform: 2.4 s at 50; 20 at 6 s = 120 s, 12 at 8 s = 96 s; 15 s behind is 2.5 questions; 30 s on Q3 costs 4 questions.

## Seeds and conventions

- l12 paper: `mockgen.generate(80)` (`random.Random(80)`): the kinds list is shuffled, then each question and its option order are drawn from the same generator. Kinds and counts: `addsub` 15 (3-digit ± 2- or 3-digit), `mul` 15 (two-thirds 2-digit by 2-digit, else 1-digit by 3-digit), `div` 10 (divisor 3 to 19, whole quotient 12 to 99), `dec` 12 (one decimal place times a tenth or a unit, or a whole quotient over 0.2 to 2.5), `frac` 10 (denominators 2, 3, 4, 5, 6, 8, 10, 12), `pct` 10 (5% steps and 12.5%, whole answers), `seq` 8 (fixed gap, fixed second gap, ×2 or ×3, or ×2 plus a step). Distractors are near misses taken in order from each kind's list and kept only when positive, different and within a factor of ten: the reverse operation, a carry slip of ±10, a slipped digit of ±1, ±10 or ±100, a row slip (±a in a product), ×10 and ÷10 (a misplaced point), the complementary percentage, tops-and-bottoms for fractions, and for sequences the last gap repeated.
- l9 block: `generate(9, BLOCK)` and homework drill `generate(31, BLOCK)`, with `BLOCK = { addsub 4, mul 4, div 2, dec 3, frac 3, pct 2, seq 2 }`.
- Sample candidate: `candidate.candidate_log(81, 80)` (`random.Random(81)`): seconds uniform per kind (+ − 3 to 6, × 4 to 8, ÷ 4 to 8, decimals 4 to 8, fractions 6 to 11, % 4 to 7, sequences 5 to 10, one decimal), a slow outlier with chance 0.08 adding 6 to 14 s, right with chance 0.95, 0.9, 0.9, 0.85, 0.75, 0.9, 0.85, a wrong answer picking another letter at random; questions past 480 s are blank. Sort rule (stated in the lesson): wrong in 6 s or less is a slip, wrong after longer a method gap, right over 12 s a time loss.
- Skip table: costs from a search over seeds 90 to 99 of `random.Random(seed)` (three in four from 3 to 8 s, else 14 to 25 s) for a unique best skip set; seed 95 was the one taken.
- Percent answers use `unit: "%"` with the answer as a fraction; money uses `unit: "£"`; times are text cells "HH:MM" accepting "HH.MM" and "HHMM"; letters are text cells "A" to "D". British spelling, £, curly apostrophes in prose.

## course.json

No change proposed.

## Backlog

Six bullets under "Raised later (mental-pressure level 3)" in `docs/BACKLOG-INBOX.md`: a clock on one block or drill table; first-attempt net scoring in a lesson table and passing a marked set on; generator kinds for decimals, fractions, percentages and sequences; a four-option cell in a table; `decimals` that a bars frame can change; an HH:MM helper in derive.

## The generator script (`mockgen.py`)

```python
"""Seeded four-option mock generator for mental-pressure level 3 (l9 block, l12 mock, homework drill).

mock_generator(seed, mix) returns a list of (text, options, answer) tuples. The same function, cut down, is the
homework's difficulty-5 solution; exam authors can reuse it for the fixed versions of mock-oa-arith.
Internally every value is a Fraction, so no float ever decides an answer.
"""
import random
from fractions import Fraction as F
from math import gcd

MIX = {"addsub": 15, "mul": 15, "div": 10, "dec": 12, "frac": 10, "pct": 10, "seq": 8}
BLOCK = {"addsub": 4, "mul": 4, "div": 2, "dec": 3, "frac": 3, "pct": 2, "seq": 2}


def terminating(x, places=4):
    x = F(x)
    return (x * 10 ** places).denominator == 1


def near(d, ans):
    """a near miss: positive, different, within a factor of ten of the answer"""
    return d > 0 and d != ans and ans / 10 <= d <= ans * 10


def slips(rng, ans, step):
    """slipped digits: the answer moved by one unit in one of its places"""
    out = [ans + s * step * k for k in (1, 10, 100) for s in (1, -1)]
    rng.shuffle(out)
    return out


def num_text(x):
    x = F(x)
    if x.denominator == 1:
        return f"{x.numerator:,}"
    s = f"{float(x):.6f}".rstrip('0').rstrip('.')
    assert F(s) == x, (s, x)
    return s


def frac_text(x):
    x = F(x)
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def make(rng, kind):
    if kind == "addsub":
        a, b, op = rng.randint(100, 999), rng.randint(12, 999), rng.choice("+-")
        if op == "-" and a < b:
            a, b = b, a
        if a == b:
            b -= 1
        ans = F(a + b) if op == "+" else F(a - b)
        cands = [F(a - b) if op == "+" else F(a + b), ans + rng.choice((10, -10))] + slips(rng, ans, 1)
        text = f"{num_text(a)} {'+' if op == '+' else '−'} {num_text(b)}"
    elif kind == "mul":
        if rng.random() < 2 / 3:
            a, b = rng.randint(12, 99), rng.randint(12, 99)
        else:
            a, b = rng.randint(3, 9), rng.randint(101, 999)
        ans = F(a * b)
        cands = [ans + rng.choice((a, -a)), ans + rng.choice((10, -10))] + slips(rng, ans, 1)
        text = f"{num_text(a)} × {num_text(b)}"
    elif kind == "div":
        b, q = rng.randint(3, 19), rng.randint(12, 99)
        a, ans = b * q, F(q)
        cands = [ans + rng.choice((1, -1)), ans * 10, ans + rng.choice((10, -10))] + slips(rng, ans, 1)
        text = f"{num_text(a)} ÷ {b}"
    elif kind == "dec":
        if rng.random() < 0.5:
            x = F(rng.randint(2, 99), 10)
            y = F(rng.randint(2, 9), 10) if rng.random() < 0.5 else F(rng.randint(2, 9))
            if x.denominator == 1 and y.denominator == 1:
                y = y / 10
            ans = x * y
            rev = x / y
            text = f"{num_text(x)} × {num_text(y)}"
        else:
            y = rng.choice([F(2, 10), F(4, 10), F(5, 10), F(25, 100), F(3, 10), F(6, 10), F(8, 10), F(12, 10), F(25, 10)])
            ans = F(rng.randint(3, 40))
            x = y * ans
            rev = x * y
            text = f"{num_text(x)} ÷ {num_text(y)}"
        step = F(1) if ans.denominator == 1 else F(1, 10 ** len(num_text(ans).split('.')[1]))
        cands = [ans * 10, ans / 10] + ([rev] if terminating(rev) else []) + slips(rng, ans, step)
    elif kind == "frac":
        dens = [2, 3, 4, 5, 6, 8, 10, 12]
        while True:
            q, s = rng.choice(dens), rng.choice(dens)
            p, r = rng.randint(1, q - 1), rng.randint(1, s - 1)
            if gcd(p, q) == 1 and gcd(r, s) == 1 and F(p, q) != F(r, s):
                break
        op = rng.choice("+-")
        if op == "-" and F(p, q) < F(r, s):
            p, q, r, s = r, s, p, q
        ans = F(p, q) + F(r, s) if op == "+" else F(p, q) - F(r, s)
        cands = [F(p, q) - F(r, s) if op == "+" else F(p, q) + F(r, s)]
        if op == "+":
            cands.append(F(p + r, q + s))
        elif q != s and p - r > 0 and q - s > 0:
            cands.append(F(p - r, q - s))
        cands += [F(ans.numerator + 1, ans.denominator), F(ans.numerator - 1, ans.denominator), F(ans.numerator, ans.denominator + 1),
                  F(ans.numerator, max(ans.denominator - 1, 1)), ans * 2, ans / 2, F(ans.numerator + 2, ans.denominator)]
        text = f"{p}/{q} {'+' if op == '+' else '−'} {r}/{s}"
    elif kind == "pct":
        p = rng.choice([F(5), F(10), F(15), F(20), F(25), F(30), F(35), F(40), F(45), F(60), F(75), F(25, 2)])
        n = 8 * rng.randint(5, 125) if p.denominator == 2 else 20 * rng.randint(2, 100)
        ans = p * n / 100
        cands = [(100 - p) * n / 100, ans * 10, ans / 10, (p + 5) * n / 100, (p - 5) * n / 100] + slips(rng, ans, 1)
        text = f"{num_text(p)}% of {num_text(n)}"
    elif kind == "seq":
        style = rng.choice(["arith", "quad", "geom", "affine"])
        if style == "arith":
            a, d = rng.randint(2, 40), rng.choice([-1, 1]) * rng.randint(3, 15)
            if d < 0:
                a += 60
            t = [a + d * i for i in range(5)]
        elif style == "quad":
            a, d, s = rng.randint(1, 12), rng.randint(1, 6), rng.randint(1, 4)
            t, diff = [a], d
            for _ in range(4):
                t.append(t[-1] + diff)
                diff += s
        elif style == "geom":
            a, r = rng.randint(2, 7), rng.choice([2, 3])
            t = [a * r ** i for i in range(5)]
        else:
            a, c = rng.randint(2, 9), rng.choice([-1, 1]) * rng.randint(1, 5)
            if a + c <= 1:
                c = abs(c)
            t = [a]
            for _ in range(4):
                t.append(2 * t[-1] + c)
        shown, ans = t[:4] if style in ("arith", "geom") else t[:5], None
        nxt = t[4] if style in ("arith", "geom") else None
        if style in ("arith", "geom"):
            ans = F(t[4])
        else:
            diff_last = t[4] - t[3]
            if style == "quad":
                ans = F(t[4] + diff_last + s)
            else:
                ans = F(2 * t[4] + c)
        last_d = shown[-1] - shown[-2]
        cands = [F(shown[-1] + last_d), ans + rng.choice((1, -1)), ans + last_d, ans - rng.choice((2, 3))] + slips(rng, ans, 1)
        text = ", ".join(num_text(v) for v in shown) + ", ?"
    else:
        raise ValueError(kind)
    cands += [ans * 2, ans / 2, ans + 1, ans + 2, ans * 3]
    out = []
    for c in cands:
        c = F(c)
        if near(c, ans) and c not in out and (kind == "frac" or terminating(c)):
            out.append(c)
        if len(out) == 3:
            break
    assert len(out) == 3, (kind, text, ans, cands)
    return text, ans, out


def generate(seed, mix=None):
    """internal form: (kind, text, options as Fractions, answer Fraction, letter)"""
    mix = MIX if mix is None else mix
    rng = random.Random(seed)
    kinds = [k for k in mix for _ in range(mix[k])]
    rng.shuffle(kinds)
    items, seen = [], set()
    for k in kinds:
        while True:
            text, ans, dis = make(rng, k)
            if text not in seen:
                break
        seen.add(text)
        opts = [ans] + dis
        rng.shuffle(opts)
        items.append((k, text, opts, ans, "ABCD"[opts.index(ans)]))
    return items


def plain(x):
    x = F(x)
    return int(x) if x.denominator == 1 else float(x)


def mock_generator(seed, mix=None):
    out = []
    for k, text, opts, ans, _ in generate(seed, mix):
        conv = (lambda v: v) if k == "frac" else plain
        out.append((text, [conv(o) for o in opts], conv(ans)))
    return out


def show(kind, x):
    return frac_text(x) if kind == "frac" else num_text(x)


def row_text(kind, text, opts):
    return f"{text}: " + "  ".join(f"**{L}** {show(kind, o)}" for L, o in zip("ABCD", opts))


if __name__ == "__main__":
    for i, (k, t, o, a, L) in enumerate(generate(80), 1):
        print(f"{i:2d} {k:6s} {t:24s} " + "  ".join(f"{l} {show(k, v)}" for l, v in zip("ABCD", o)) + f"   -> {L} ({show(k, a)})")
```

## Its output for seed 80 (the l12 paper), the candidate and the two blocks

| Q | Kind | Question | A | B | C | D | Answer |
|---:|---|---|---|---|---|---|---|
| 1 | pct | 15% of 1,260 | 1,071 | 189 | 1,890 | 18.9 | B (189) |
| 2 | seq | 66, 57, 48, 39, ? | 30 | 27 | 29 | 21 | A (30) |
| 3 | frac | 2/3 − 1/2 | 7/6 | 1 | 1/6 | 1/3 | C (1/6) |
| 4 | mul | 9 × 174 | 1,557 | 1,566 | 1,567 | 1,576 | B (1,566) |
| 5 | dec | 3 ÷ 0.25 | 2 | 120 | 1.2 | 12 | D (12) |
| 6 | addsub | 291 + 883 | 1,174 | 1,184 | 1,164 | 1,074 | A (1,174) |
| 7 | pct | 10% of 880 | 792 | 88 | 880 | 8.8 | B (88) |
| 8 | dec | 34.8 ÷ 1.2 | 41.76 | 2.9 | 290 | 29 | D (29) |
| 9 | addsub | 938 + 212 | 726 | 1,140 | 1,150 | 1,151 | C (1,150) |
| 10 | div | 342 ÷ 6 | 47 | 57 | 570 | 58 | B (57) |
| 11 | addsub | 508 − 96 | 413 | 402 | 604 | 412 | D (412) |
| 12 | frac | 1/6 + 1/4 | 1/2 | 1/5 | 5/12 | 1/3 | C (5/12) |
| 13 | mul | 41 × 63 | 2,573 | 2,683 | 2,542 | 2,583 | D (2,583) |
| 14 | frac | 1/3 + 1/6 | 1 | 2/9 | 1/6 | 1/2 | D (1/2) |
| 15 | pct | 10% of 480 | 480 | 4.8 | 48 | 432 | C (48) |
| 16 | mul | 5 × 718 | 3,590 | 3,490 | 3,580 | 3,595 | A (3,590) |
| 17 | addsub | 731 − 467 | 1,198 | 264 | 274 | 263 | B (264) |
| 18 | mul | 34 × 21 | 748 | 724 | 715 | 714 | D (714) |
| 19 | frac | 1/2 − 3/8 | 7/8 | 1/4 | 1/9 | 1/8 | D (1/8) |
| 20 | dec | 8.3 × 8 | 67.4 | 66.4 | 664 | 6.64 | B (66.4) |
| 21 | mul | 5 × 290 | 1,350 | 1,450 | 1,440 | 1,455 | B (1,450) |
| 22 | div | 280 ÷ 5 | 56 | 55 | 46 | 560 | A (56) |
| 23 | frac | 1/3 + 5/12 | 2/5 | 1/2 | 1 | 3/4 | D (3/4) |
| 24 | frac | 1/3 − 1/12 | 1/4 | 1/2 | 1/5 | 5/12 | A (1/4) |
| 25 | dec | 0.4 × 8 | 13.2 | 32 | 3.2 | 0.32 | C (3.2) |
| 26 | frac | 2/3 + 1/4 | 11/12 | 1 | 3/7 | 5/12 | A (11/12) |
| 27 | div | 924 ÷ 11 | 840 | 74 | 83 | 84 | D (84) |
| 28 | div | 1,140 ÷ 15 | 75 | 66 | 76 | 760 | C (76) |
| 29 | pct | 20% of 860 | 1,720 | 17.2 | 688 | 172 | D (172) |
| 30 | seq | 2, 8, 20, 44, 92, ? | 236 | 187 | 140 | 188 | D (188) |
| 31 | seq | 75, 63, 51, 39, ? | 27 | 26 | 15 | 24 | A (27) |
| 32 | seq | 2, 7, 17, 37, 77, ? | 197 | 157 | 156 | 117 | B (157) |
| 33 | mul | 77 × 97 | 7,469 | 7,369 | 7,546 | 7,459 | A (7,469) |
| 34 | seq | 6, 12, 24, 48, ? | 97 | 72 | 120 | 96 | D (96) |
| 35 | div | 425 ÷ 5 | 85 | 86 | 95 | 850 | A (85) |
| 36 | pct | 40% of 280 | 1,120 | 168 | 11.2 | 112 | D (112) |
| 37 | dec | 0.5 × 5 | 0.25 | 2.5 | 2.6 | 25 | B (2.5) |
| 38 | frac | 4/5 + 1/3 | 5/8 | 17/15 | 6/5 | 7/15 | B (17/15) |
| 39 | frac | 5/6 + 1/3 | 2/3 | 1/2 | 7/6 | 4/3 | C (7/6) |
| 40 | mul | 84 × 90 | 7,570 | 7,476 | 7,560 | 7,460 | C (7,560) |
| 41 | mul | 62 × 26 | 1,550 | 1,612 | 1,622 | 1,613 | B (1,612) |
| 42 | div | 161 ÷ 7 | 13 | 23 | 230 | 24 | B (23) |
| 43 | pct | 15% of 500 | 75 | 7.5 | 425 | 750 | A (75) |
| 44 | addsub | 318 + 344 | 562 | 672 | 652 | 662 | D (662) |
| 45 | pct | 60% of 400 | 24 | 240 | 2,400 | 160 | B (240) |
| 46 | dec | 8.7 × 2 | 4.35 | 1.74 | 174 | 17.4 | D (17.4) |
| 47 | pct | 10% of 1,280 | 128 | 1,280 | 1,152 | 12.8 | A (128) |
| 48 | mul | 4 × 780 | 3,120 | 3,119 | 3,116 | 3,130 | A (3,120) |
| 49 | addsub | 869 − 507 | 1,376 | 462 | 362 | 372 | C (362) |
| 50 | mul | 4 × 919 | 3,686 | 3,680 | 3,676 | 3,677 | C (3,676) |
| 51 | mul | 9 × 646 | 5,804 | 5,805 | 5,813 | 5,814 | D (5,814) |
| 52 | addsub | 552 − 466 | 76 | 86 | 96 | 85 | B (86) |
| 53 | dec | 6.2 × 0.8 | 7.75 | 4.96 | 0.496 | 49.6 | B (4.96) |
| 54 | addsub | 918 − 516 | 402 | 392 | 302 | 1,434 | A (402) |
| 55 | div | 1,152 ÷ 18 | 64 | 640 | 65 | 54 | A (64) |
| 56 | mul | 8 × 443 | 3,545 | 3,552 | 3,554 | 3,544 | D (3,544) |
| 57 | mul | 57 × 28 | 1,606 | 1,653 | 1,586 | 1,596 | D (1,596) |
| 58 | addsub | 933 + 201 | 1,234 | 1,134 | 732 | 1,144 | B (1,134) |
| 59 | addsub | 824 − 137 | 677 | 787 | 687 | 961 | C (687) |
| 60 | addsub | 330 − 304 | 16 | 126 | 26 | 25 | C (26) |
| 61 | div | 344 ÷ 8 | 33 | 43 | 42 | 430 | B (43) |
| 62 | seq | 35, 43, 51, 59, ? | 67 | 75 | 64 | 68 | A (67) |
| 63 | addsub | 992 − 739 | 1,731 | 253 | 353 | 243 | B (253) |
| 64 | addsub | 453 − 322 | 231 | 775 | 131 | 121 | C (131) |
| 65 | mul | 4 × 467 | 1,868 | 1,869 | 1,872 | 1,878 | A (1,868) |
| 66 | div | 1,539 ÷ 19 | 810 | 82 | 81 | 71 | C (81) |
| 67 | seq | 8, 9, 11, 14, 18, ? | 21 | 22 | 23 | 27 | C (23) |
| 68 | addsub | 668 + 145 | 814 | 523 | 823 | 813 | D (813) |
| 69 | mul | 6 × 382 | 2,292 | 2,392 | 2,286 | 2,302 | A (2,292) |
| 70 | dec | 7.6 ÷ 0.2 | 3.8 | 38 | 39 | 380 | B (38) |
| 71 | addsub | 899 + 246 | 1,135 | 1,145 | 1,144 | 653 | B (1,145) |
| 72 | seq | 4, 10, 17, 25, 34, ? | 43 | 44 | 42 | 53 | B (44) |
| 73 | dec | 18.4 ÷ 0.8 | 2.3 | 14.72 | 230 | 23 | D (23) |
| 74 | pct | 40% of 1,940 | 1,164 | 7,760 | 776 | 77.6 | C (776) |
| 75 | dec | 6 ÷ 1.2 | 0.5 | 7.2 | 5 | 50 | C (5) |
| 76 | dec | 7.4 × 0.9 | 6.66 | 6.67 | 0.666 | 66.6 | A (6.66) |
| 77 | frac | 3/5 − 1/3 | 4/15 | 1/3 | 14/15 | 1 | A (4/15) |
| 78 | pct | 30% of 1,900 | 57 | 1,330 | 570 | 5,700 | C (570) |
| 79 | dec | 3.4 × 0.4 | 8.5 | 0.136 | 13.6 | 1.36 | D (1.36) |
| 80 | div | 780 ÷ 10 | 780 | 77 | 68 | 78 | D (78) |

Candidate (seed 81): Q, seconds, mark, type

Q1 5.5 r, Q2 6.9 r, Q3 8.3 r, Q4 7.6 r, Q5 5.2 r, Q6 4.5 r, Q7 6.9 r, Q8 5.3 w/S, Q9 5.0 r, Q10 4.1 r, Q11 5.8 r, Q12 9.7 r, Q13 7.1 w/M, Q14 7.5 w/M, Q15 5.4 r, Q16 6.5 r, Q17 3.1 r, Q18 4.5 r, Q19 6.2 w/M, Q20 4.9 r, Q21 4.4 w/S, Q22 7.3 r, Q23 9.3 r, Q24 7.0 w/M, Q25 7.2 r, Q26 7.9 w/M, Q27 7.4 w/M, Q28 5.7 r, Q29 4.4 r, Q30 16.9 r/T, Q31 21.8 r/T, Q32 5.8 r, Q33 4.9 r, Q34 8.4 w/M, Q35 4.9 r, Q36 4.3 r, Q37 6.0 r, Q38 6.8 w/M, Q39 8.9 r, Q40 15.8 r/T, Q41 5.8 r, Q42 6.7 r, Q43 4.7 r, Q44 5.7 r, Q45 6.7 r, Q46 7.0 r, Q47 5.7 r, Q48 6.7 r, Q49 11.8 r, Q50 4.9 r, Q51 5.8 r, Q52 3.8 r, Q53 5.4 r, Q54 4.0 r, Q55 18.6 r/T, Q56 4.3 r, Q57 5.4 r, Q58 4.5 r, Q59 4.5 r, Q60 17.0 w/M, Q61 6.2 r, Q62 8.7 r, Q63 5.6 r, Q64 4.2 r, Q65 5.6 r, Q66 7.4 r, Q67 8.9 r, Q68 5.7 r, Q69 blank, Q70 blank, Q71 blank, Q72 blank, Q73 blank, Q74 blank, Q75 blank, Q76 blank, Q77 blank, Q78 blank, Q79 blank, Q80 blank

Seed 9 block of 20 (BLOCK mix): Q1 842 + 444 = 1,286 (B); Q2 3, 6, 12, 24, ? = 48 (D); Q3 304 ÷ 16 = 19 (D); Q4 972 − 219 = 753 (B); Q5 5.2 × 0.3 = 1.56 (D); Q6 8 × 690 = 5,520 (B); Q7 30% of 320 = 96 (B); Q8 7, 10, 16, 28, 52, ? = 100 (A); Q9 205 + 541 = 746 (B); Q10 41 × 24 = 984 (A); Q11 5% of 160 = 8 (D); Q12 7/12 + 3/5 = 71/60 (B); Q13 592 − 587 = 5 (D); Q14 7.3 × 8 = 58.4 (C); Q15 1/3 + 1/4 = 7/12 (A); Q16 81 × 61 = 4,941 (D); Q17 79 × 79 = 6,241 (B); Q18 1,674 ÷ 18 = 93 (C); Q19 2.4 ÷ 0.4 = 6 (D); Q20 1/3 − 1/4 = 1/12 (A)

Seed 31 block of 20 (BLOCK mix): Q1 38 × 87 = 3,306 (A); Q2 380 ÷ 10 = 38 (C); Q3 7, 8, 10, 13, 17, ? = 22 (B); Q4 3.9 × 0.8 = 3.12 (C); Q5 36 × 15 = 540 (D); Q6 1/3 + 1/6 = 1/2 (B); Q7 9 × 256 = 2,304 (D); Q8 5/12 − 1/4 = 1/6 (B); Q9 5% of 280 = 14 (D); Q10 60% of 1,600 = 960 (A); Q11 1,501 ÷ 19 = 79 (C); Q12 547 − 226 = 321 (C); Q13 401 − 351 = 50 (D); Q14 6, 12, 24, 48, ? = 96 (C); Q15 4 × 0.7 = 2.8 (A); Q16 65 × 16 = 1,040 (A); Q17 5.4 ÷ 0.3 = 18 (A); Q18 970 + 110 = 1,080 (A); Q19 9/10 − 2/5 = 1/2 (D); Q20 822 + 257 = 1,079 (C)
