# Report: mental-pressure level 4 (Assessment batteries)

Status: complete. Course `mental-pressure`, topic 3.3; brief `docs/briefs/mental-pressure.md` `## Level 4` with the orchestrator's corrections (engine pass A built net scoring, forward-only papers, generated arithmetic and timed sets for mock exams and reviews only; lessons still cannot net-score the learner's own answers). Ids, names, objectives and skills are from `course.json`: `mp-formats` on l13, l16 and l17, `mp-estimate` on l14, `mp-formats` and `mp-fractions` on l15. Builders, generators and screenshots are in the scratchpad folder `mental-pressure-4` (`mk.py`, `b13.py` to `b17.py`, `bset.py`, `gen17.py`, `gen18.py`, `seq16.py`, `hw/` for the homework code harness, `shots/`).

## Files

All in `app/content/courses/mental-pressure/`. Nothing else was edited except this report and `docs/BACKLOG-INBOX.md`; the validator rewrote `content/manifest.json`.

| File | Screens or items | Canvases and widgets | Code |
|---|---|---|---|
| `l13-negative-marking.json` | 12 screens, 4 quiz | table (a sitting of 80); `bars` of a guess's value by options left, with a `stops` control on the wrong mark and a `derive` (explore, follow-up); bars filled live by table cells (`bind: values.c40` ...) for $2p - 1$; bars for the time trade; trap choice on the reported-format table; `expression` derive $w = \tfrac{1}{k-1}$; 8-row drill; `multi` card of rules | `guess_value`, `net_score`, 13 tests |
| `l14-ranking-likelihoods.json` | 12 screens, 4 quiz | table with "?" filled by the explanation (hook); `number-line` with $(1 - 1/n)^n$ and its complement driven by a control on $n$ (explore); number-line of benchmarks with events placed by the explanation; zoomed line round ½; normal 68% and 95% bands; symmetry line 0 to 10; `order` rankings; `order` derive of $1/e$ with a distractor; 6-row drill | `at_least_one`, `rank`, 11 tests |
| `l15-probability-at-speed.json` | 12 screens, 4 quiz | `tree` with an unknown branch (two aces); 6 × 6 `grid` tap-regions (prime totals, explore); population `grid` of 1,000 with groups (natural frequencies); 6 × 6 grid of totals for the reroll game; dice grid for the impossible options (`multi`); tree for the pair trap; `order` derive with `same` and a distractor; 6-row drill; tree for the signal transfer | `prob_dice`, `natural_frequency`, 10 tests |
| `l16-harder-sequences.json` | 12 screens, 4 quiz | term tables; table switched by a three-frame control (terms, gaps, steps; explore); digit-sum and look-and-say tables; method card; two-rules table; `order` derive with a distractor; 6-row drill | `next_term` (with `split_interleaved` given), 13 tests |
| `l17-full-battery.json` | 12 screens, 4 quiz | time-budget table; whole-battery number-line with a dragged point and a derived caption (explore); three section tables of four-option rows (seed 17), each on its own seconds line; net-score sheet and S/M/T sort of the seed-18 candidate; trap table of section C; section-rules table; `order` routine with a distractor; week-plan choice | none (the brief asks for none) |
| `review-4.json` | 10 items, difficulty 2 to 4, `timed: { "seconds": 720, "lockAtZero": false }` (a guide clock) | numeric, choice, order | |
| `homework-4.json` | 8 items, difficulty 3 to 5 (two at 5) | four drill tables (negative marking 80 s, ranking 60 s, probability four-option 12 minutes, sequences 3 minutes); 2 code; `order` with two distractors; 10-point `longform` answered aloud then written | `battery_generator` (12 tests, difficulty 5); `trade_values` and `answer_or_guess` (11 tests, difficulty 4) |

Lesson shapes. l13 to l15: hook, explore, name, three ladders (l13's third is "The follow-up"), trap, generalise, derive, code, drill, transfer. l16: hook, explore, name, two ladders, trap, ladder (two rules), generalise, derive, code, drill, transfer. l17: hook (time budget), explore (battery clock), section A (problem), sections B and C (ladders), net-score sheet, error sort (ladder), trap, finishing early (ladder), generalise, derive, transfer.

Edge cases: l13 the follow-up (a −1/3 penalty makes a blind guess 0; no penalty makes it +1/4) and quiz `q-no-penalty-end`; l14 a tie by symmetry (4 against 6 heads in 10) and quiz `q-mirror-eight`; l15 impossible options removed at once (7/6 and −1/6); l16 two defensible rules (1, 2, 4: give 8 and move on); l17 finishing a section early (recheck flagged items in the open section only; nothing to recheck in a forward-only section).

Traps: l13 "never guess" and "always guess" (choice keys `blank`, `blind`, `solve`); l14 $n \times p$ for at least one (keys `np` = 1, `none` = 0.33, `oneroll` = 0.83), with ranking by ways in quiz `q-ways-not-chances`; l15 without replacement (keys `rep` 1/13, `aces` 1/221, `den` 3/52); l16 forcing one rule from three terms (2, 4, 8, 6, 32, 8 → 128; keys `doubling` 16, `even-half` 10, `double-32` 64); l17 carrying the arithmetic pace into probability (the seed-18 candidate: four wrong answers in about 40 s, one stall of 378.4 s, 164.1 s unused).

Self-timing and pace. Every drill states its target in prose and says the app does not time it; grading never depends on time. The engine pass's `pace` field was live in the validator when I validated (`checkPace`, ENGINE-BACKLOG 457), so every drill screen and drill item also carries `pace` in seconds: l13 drill 80, l14 drill 75, l15 drill 720, l16 drill 180, l17 sections A 120, B 800, C 720; homework drills 80, 60, 720, 180. Review-4 carries a 720 s guide clock.

Tags. Every drill screen, quiz item, review item and homework item carries one family tag from the brief: `negative-marking`, `ranking`, `probability`, `sequences`, `battery` (`h-forward-routine` carries `negative-marking` and `battery`). Every `choice` without ordered options has `shuffle: true`; ordered ones (estimates, the tie, letters) keep their order. `longform` appears in homework only.

Reported formats, never a firm: "some firms' online tests" (+1, −1, 0), "candidates report a pass band of about 50 to 60 net", the 80-in-8 "forward only, with no skip" as reported, the ranking paper "about 10 items in 10 minutes", probability "about 15 items in 30 minutes", sequences "about 15 items in 25 minutes". Zetamac is named once (l17 transfer: the daily warm-up runs Zetamac's default settings). No firm name appears.

## Validator and checks

- `node tools/validate.mjs` (from `app/`): **0 errors**; no warning in any level 4 file (the 393 warnings are other courses' and other levels').
- `VOICE_BASE=/home/user/zero-to-quant/app/content/courses/mental-pressure/ python3 docs/reviews/voice-scan.py` (absolute path, re-run after the coordinator's correction; it scanned 10,918 sentences): 0 sentences over 20 words and 0 explanations over three sentences in level 4 files. Hits in levels 1 to 3, not mine and not edited: 45 sentences over 20 words (homework-1 9, homework-2 6, homework-3 9, l1 5, l2 2, l3 1, l4 1, l5 1, l6 1, l7 2, l8 2, l9 2, l10 2, l11 2) and one explanation of five sentences (`l2-two-by-two.json` screens.5.explain.text).
- Grep checks on level 4 files: no em-dash or en-dash, no `!` in copy, none of the validator's American spellings, no firm names.

## Playthrough

All with `--local-cdn <scratchpad>/pkgs`.

Two full passes on 2026-11-03, each playing all five lessons and both sets:

| Run | l13 | l14 | l15 | l16 | l17 | review-4 | homework-4 |
|---|---|---|---|---|---|---|---|
| `--lesson ... --set ...` (1280 px) | ok, 16 checks, quiz 4/4 | ok, 16, 4/4 | ok, 16, 4/4 | ok, 16, 4/4 | ok, 16, 4/4 | ok, 10 of 10 | ok, 8 of 8, 37 of 37 marks |
| the same with `--mobile --why --shots` | ok, 16, 4/4 | ok, 16, 4/4 | ok, 16, 4/4 | ok, 16, 4/4 | ok, 16, 4/4 | ok, 10 of 10 | ok, 8 of 8, 37 of 37 marks |

"All passed." both times, with no console errors.

Screenshots at 1280 and 390 px (with `--why`) are in `<scratchpad>/mental-pressure-4/shots/`. Faults found and fixed from them: the l14 normal screen's 68% and 95% labels sat on the "mean" label (labels moved beside the bands, mean below); the l14 tie screen printed "5" twice; the l17 section tables first sat on a whole-battery line where section A was 2 of 28 minutes and its labels collided (each section now has its own seconds line); the three-column question, options, letter rows wrapped to four lines at 390 px (now two columns, "Question and options" and "Letter"); the l16 transfer table first showed the steps it asked for (removed). The l15 natural-frequency and reroll screens moved from trees to grids, so every ladder reuses its canvas kind (no ladder warnings).

## Numbers, each computed twice (by hand and in the builders' `assert`s, plus `seq16.py` and `hw/run.py`)

- l13: guess value $\tfrac1k - w\tfrac{k-1}{k}$: −1/2, −1/3, 0, +1 for 4, 3, 2, 1 left at $w = 1$; five options −3/5 = −0.6; at $w = 1/3$ 0; at $w = 1/2$ −1/8; no penalty 1/4; five options at $w = 1/4$ 0; five options after removing two −1/3. Sitting 62 right, 10 wrong, 8 blank: net 52. $2p - 1$ at 40, 50, 60, 75, 90%: −0.2, 0, 0.2, 0.5, 0.8. Time trade: 18 s at 6 s is 3 questions at 0.9 − 0.1 = 0.8, 2.4 against 0.8 for solving (gain 1.6); 30 s is 5 questions, 4 marks. Fair penalty $1/(k-1)$. Drill: −1/3; 58 − 14 = 44; 80 × −0.5 = −40; 70 × 0.85 = 59.5 right, 10.5 wrong, net 49; 1/2; 0. Quiz: 75 answered, 11 wrong → 64 − 11 = 53; −1/8; 0.55 → 0.1; 6 × 1/4 = 1.5.
- l14: $\binom{10}{5}/1024 = 63/256 = 0.2461$; 1/6 = 0.1667; 8/52 = 2/13 = 0.1538. Birthday 30: 0.7063; $1 - (5/6)^6 = 31031/46656 = 0.6651$; 6 or more heads in 10: 386/1024 = 193/512 = 0.3770 (also $(1 - 0.2461)/2$). $1 - (5/6)^4 = 671/1296 = 0.5177$; birthday 23: 0.5073; $1 - (35/36)^{24} = 0.4914$ ($e^{-2/3} = 0.5134$). 60 or more heads in 100: sd 5, $z = 9.5/5 = 1.9$, $1 - \Phi(1.9) = 0.0287$, exact binomial 0.0284. $\binom{10}{4} = \binom{10}{6} = 210$. $(1 - 1/n)^n$: 0.25 at 2, 0.3349 at 6, 0.3642 at 50, limit $1/e = 0.3679$. $1 - 0.9^{10} = 0.6513$; $1 - 0.95^{20} = 0.6415$; $\Phi(-2) = 0.0228$. Drill: 11/36 = 0.3056, 15/36 = 5/12 = 0.4167, 1/8; 91/216 = 0.4213 against 0.4167; $\binom{20}{10}/2^{20} = 0.1762$ against 0.1667; 20/64 = 0.3125 against 6/16 = 0.375; $\binom62 = \binom64 = 15$. Quiz: 252/1024 against 6/36; $1 - (5/6)^{12} = 0.8878$ ($1 - e^{-2} = 0.8647$); $2\Phi(-2) = 0.0455$; $\binom83 = \binom85 = 56$.
- l15: $(4/52)(3/51) = 1/221 = 0.0045$; $(4/52)^2 = 1/169$. Prime totals: 1 + 2 + 4 + 6 + 2 = 15 cells, 15/36 = 5/12. 1,000 people at 2%, 90%, 10%: 20, 18, 98, 18/116 = 9/58 = 0.1552. Reroll game: (5/6)(3) + (1/6)(9.5) = 2.5 + 1.583 = 49/12 = 4.0833, also 3.5 + 3.5/6, and the grid's 36 cells sum to 147 (147/36 = 49/12). Pair 3/51 = 1/17. Three flips the same 2/8 = 1/4. Signal: 15 of 20 firing days, 3/4. Drill: 5/12, 15/16, 6, 1/7, 1/17, 1/4. Quiz: 11/36; (3/5)(2/4) = 3/10; 40/59 = 0.678.
- l16 (all checked by `seq16.py`): 2, 20, 4, 17, 8, 14, 16 → 11; 3, 6, 4, 8, 6, 12, 10 → 20; 1, 10, 3, 20, 5, 30 → 7; 2, 5, 15, 18, 54 → 57; 40, 1, 38, 2, 36, 4 → 34; 7, 14, 19, 29, 40, 44 → 52; look-and-say 111221 → 312211 (then 13112221); 2, 4, 8, 6, 32, 8 → 128; 10, 1, 20, 2, 30, 3 → 40; drill 720, 67, 1, 33, 4, 45 (12, 21, 23, 32, 34, 43 also splits into two +11 halves, so 45 either way); transfer 100, 300, 200, 600, 500, 1,500 → 1,400; quiz 20, 94, 75, 16.
- l17: 20 × 6 = 120, 8 × 100 = 800, 6 × 120 = 720, total 1,640 s = 27 min 20 s; 15 in 25 minutes = 100 s, 15 in 30 minutes = 120 s; at 12:00, (12 − 2) × 0.6 = 6 sequences done. Seed-18 candidate: A 18 right, 2 wrong, net 16 (119.2 s of 120); B 2 right, 4 wrong, 2 blank, net 2 (Q7 still open when the 800 s ran out, Q8 not reached); C 1 right, 5 wrong, net 1 (555.9 s of 720, 164.1 s unused); total 19; B with two blind guesses 2 + 2 × 1/4 = 2.5. Error sort: A Q5 M, Q13 S, Q20 T; B Q1, Q2, Q3 M, Q4 S; C Q2, Q3 S, Q4 M, Q5, Q6 S (six slips, five method gaps, one time loss). Generalise 1,080 / 12 = 90 s.
- Review-4: 57 − 9 = 48; trade 21/6 × (0.8 − 0.2) = 2.1 (no-penalty slip 2.8, full-time slip 2.4, solving 0.6); 0.518 > 15/36 = 0.417 > 22/64 = 0.344; $1 - 0.95^{20} = 0.6415$; 80/260 = 4/13 = 0.3077; (13/52)(12/51) = 1/17; 4, 50, 8, 45, 12, 40 → 16; 23, 28, 38, 49, 62, 70 → 77; 1,200/12 = 100 s.
- Homework drills: −0.6; 1/3 − (2/3)(1/3) = 1/9; 71 − 9 = 62; 48 − 12 = 36; 64 × 0.8 − 16 × 0.5 = 43.2; $p = 0.7$; 1/4; 2. Ranking: 0.5981 against 0.5687 (A); 176/1024 = 0.1719 against 0.1667 (A); 120 = 120 (S); 0.6373 against 0.6651 (B); 0.1587 against 0.1667 (B); 12/51 = 0.2353 against 0.2461 (B). Probability: the l15 six with slips (5/11, 7/12, 1/3; 1/16, 1/2, 2; 3.5, 5, 1/6; 1/49, 6/7, 2/7; 1/13, 1/221, 3/52; 1/8, 3/4, 1/2). Sequences: 15, 29, 47, 24, 1113122112, 85.
- `trade_values`: (20, 2, 6, 9/10) → (4/5, 12/5); (24, 2, 6, 4/5, g = 3) → (3/5, 21/10); (10, 4, 6, 9/10) → (4/5, 17/30); (30, 4, 6, 9/10) guess 97/30; ties at accuracy 1/2 and at (12, 3, 6, 3/4) answer.

Code items: every solution passes its hidden tests and every starter fails them (lessons through the playthrough, which loads `solution`; the homework generator also by `hw/run.py` locally: solution 12 of 12, starter 0 of 12). All code is pure Python with `fractions`, `itertools`, `random` and `math`; nothing slow loads.

## Seeds and conventions

- l17 battery: `random.Random(17)`, script `gen17.py` below. Arithmetic kinds shuffled from 4 add, 3 sub, 4 mul, 3 div, 3 decimal, 3 percentage; three near misses per item (the reverse operation, a misplaced point, a slipped digit), redrawn on a repeated question. Sequences: one item per template (interleaved, alternating, ×2 + c, second differences, squares + c, digit sums, Fibonacci-like, ×3), distractors from the wrong rule. Probability: one item per template (two-dice total, at least one six, same suit, exactly k heads, natural frequencies, reroll game), distractors labelled by slip.
- l17 review: `random.Random(18)`, `gen18.py` below: per question a uniform time in the section's band, a stall at 2 to 3.5 times the pace with chance 0.2, right with the section's accuracy (A 85%, B 80%, C 55% and rushed at 25 to 60 s), blank once the section clock would be passed. Scoring A +1/−1/0, B and C +1/0/0. Slip = wrong within the section pace; method gap = wrong over it; time loss = right but over twice it.
- Homework `battery_generator`: the near-miss rules match `app/js/engine/arith.js` (reverse: add → |a − b|, sub → a + b, mul → a + b, div → a − b; point × or ÷ 10; one digit off by one, no wrap).

### gen17.py

```python
"""l17 battery: fixed items generated once from random.Random(17).
Arithmetic: 20 four-option items, near misses (reverse operation, misplaced point, slipped digit).
Sequences: 8 items, one per rule template. Probability: 6 items from templates.
Run: python3 gen17.py  -> prints the items and writes battery17.json beside this file."""
import random, json, os
from fractions import Fraction as F
from math import comb

rng = random.Random(17)
LET = 'ABCD'


def clean(x):
    x = F(x)
    return x


def fmt(x):
    x = F(x)
    if x.denominator == 1:
        return f"{x.numerator:,}"
    s = f"{float(x):.6f}".rstrip('0').rstrip('.')
    assert F(s) == x
    return s


def slip(ans):
    """one digit of the answer off by one (a one-digit answer: one more or one less)"""
    if ans < 10 and ans.denominator == 1:
        return ans + rng.choice((1, -1))
    s = fmt(ans).replace(',', '')
    idx = [i for i, c in enumerate(s) if c.isdigit()]
    i = rng.choice(idx)
    d = (int(s[i]) + rng.choice((1, -1))) % 10
    if i == idx[0] and d == 0:
        d = 2
    return F(s[:i] + str(d) + s[i + 1:])


def point(ans):
    return ans * 10 if rng.random() < 0.5 or ans < 1 else ans / 10


def options(ans, reverse):
    """answer plus three near misses: reverse, point, slip; fall back to more slips"""
    seen, out, kinds = {ans}, [], []
    for kind, v in (('reverse', reverse), ('point', point(ans)), ('slip', slip(ans))):
        if v is not None and v > 0 and v not in seen:
            seen.add(v); out.append(v); kinds.append(kind)
    while len(out) < 3:
        v = slip(ans)
        if v > 0 and v not in seen:
            seen.add(v); out.append(v); kinds.append('slip')
    allv = out + [ans]
    order = list(range(4))
    rng.shuffle(order)
    opts = [allv[i] for i in order]
    k = [(kinds + ['answer'])[i] for i in order]
    return opts, k


def arith(kind):
    if kind == 'add':
        a, b = rng.randint(120, 899), rng.randint(110, 899)
        if b > a: a, b = b, a
        return f"{fmt(a)} + {fmt(b)}", F(a + b), F(a - b)
    if kind == 'sub':
        a, b = rng.randint(400, 999), rng.randint(110, 399)
        return f"{fmt(a)} − {fmt(b)}", F(a - b), F(a + b)
    if kind == 'mul':
        a, b = rng.randint(3, 9), rng.randint(21, 99)
        if rng.random() < 0.5:
            a, b = rng.randint(12, 19), rng.randint(12, 49)
        return f"{a} × {b}", F(a * b), F(a + b)
    if kind == 'div':
        a, q = rng.choice([6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19]), rng.randint(12, 49)
        return f"{fmt(a * q)} ÷ {a}", F(q), F(a * q - a)
    if kind == 'dec':
        a, b = F(rng.randint(12, 95), 10), rng.randint(3, 9)
        return f"{fmt(a)} × {b}", a * b, a + b
    if kind == 'pct':
        p = rng.choice([5, 15, 20, 25, 30, 35, 40, 45, 60, 75])
        y = rng.choice([180, 240, 320, 360, 420, 480, 640, 840, 960, 1260, 1440])
        ans = F(p * y, 100)
        if ans.denominator != 1:
            return arith('pct')
        return f"{p}% of {fmt(y)}", ans, y - ans


MIX = ['add'] * 4 + ['sub'] * 3 + ['mul'] * 4 + ['div'] * 3 + ['dec'] * 3 + ['pct'] * 3
rng.shuffle(MIX)
A = []
for kind in MIX:
    text, ans, rev = arith(kind)
    while any(text == x['text'] for x in A):
        text, ans, rev = arith(kind)
    opts, kinds = options(ans, rev)
    A.append(dict(kind=kind, text=text, answer=ans, options=opts, kinds=kinds))


# ---------- sequences: one per template ----------
def seq_item(t):
    if t == 'interleaved':
        a, d = rng.randint(2, 9), rng.randint(2, 6)
        g, r = rng.randint(1, 3), 2
        odd = [a + d * i for i in range(4)]
        even = [g * r ** i for i in range(3)]
        s = [odd[0], even[0], odd[1], even[1], odd[2], even[2], odd[3]]
        ans = even[2] * r
        wrong = [odd[3] + d, ans + d, s[-1] + (s[-1] - s[-2])]
        rule = f"odd places +{d}, even places ×2"
    elif t == 'alternating':
        a, k, c = rng.randint(2, 6), rng.choice([2, 3]), rng.randint(1, 4)
        s = [a]
        for i in range(6):
            s.append(s[-1] * k if i % 2 == 0 else s[-1] - c)
        ans = s[-1] * k
        wrong = [s[-1] - c, s[-1] * k - c, s[-1] + (s[-1] - s[-2])]
        rule = f"×{k} then −{c}, in turn"
    elif t == 'times-plus':
        a, k, c = rng.randint(2, 5), 2, rng.choice([-1, 1, 3])
        s = [a]
        for i in range(4):
            s.append(k * s[-1] + c)
        ans = k * s[-1] + c
        wrong = [k * s[-1], s[-1] + 2 * (s[-1] - s[-2]), ans + 2]
        rule = f"×2 then {'+' if c > 0 else '−'}{abs(c)}"
    elif t == 'second-diff':
        a, d, e = rng.randint(2, 9), rng.randint(2, 5), rng.randint(2, 3)
        s = [a]
        g = d
        for i in range(4):
            s.append(s[-1] + g); g += e
        ans = s[-1] + g
        wrong = [s[-1] + (g - e), ans + e, ans - 1]
        rule = f"gaps grow by {e}"
    elif t == 'squares':
        c = rng.choice([-1, 1, 2, 3])
        n0 = rng.randint(2, 4)
        s = [(n0 + i) ** 2 + c for i in range(5)]
        ans = (n0 + 5) ** 2 + c
        wrong = [s[-1] + (s[-1] - s[-2]), ans + 1, (n0 + 5) ** 2]
        rule = f"squares {'+' if c > 0 else '−'} {abs(c)}"
    elif t == 'digit-sum':
        x = rng.randint(11, 25)
        s = [x]
        for i in range(5):
            s.append(s[-1] + sum(map(int, str(s[-1]))))
        ans = s[-1] + sum(map(int, str(s[-1])))
        wrong = [s[-1] + (s[-1] - s[-2]), ans + 1, s[-1] + int(str(s[-1])[-1])]
        rule = "add the digit sum"
    elif t == 'fibonacci':
        a, b = rng.randint(1, 4), rng.randint(3, 7)
        s = [a, b]
        for i in range(4):
            s.append(s[-1] + s[-2])
        ans = s[-1] + s[-2]
        wrong = [s[-1] + (s[-1] - s[-2]), 2 * s[-1], ans + 1]
        rule = "each term is the sum of the two before"
    elif t == 'geometric':
        a, r = rng.randint(2, 5), 3
        s = [a * r ** i for i in range(5)]
        ans = s[-1] * r
        wrong = [s[-1] + (s[-1] - s[-2]), s[-1] * 2, ans + r]
        rule = "×3"
    seen, w = {ans}, []
    for v in wrong:
        if v not in seen and v > 0:
            seen.add(v); w.append(v)
    while len(w) < 3:
        v = ans + rng.choice([1, 2, -1, -2, 10])
        if v not in seen and v > 0:
            seen.add(v); w.append(v)
    opts = w[:3] + [ans]
    rng.shuffle(opts)
    return dict(kind=t, text=', '.join(fmt(x) for x in s) + ', ?', answer=F(ans), options=[F(o) for o in opts], rule=rule)


TEMPL = ['interleaved', 'alternating', 'times-plus', 'second-diff', 'squares', 'digit-sum', 'fibonacci', 'geometric']
rng.shuffle(TEMPL)
S = [seq_item(t) for t in TEMPL]


# ---------- probability ----------
def two_dice(pred):
    return F(sum(1 for i in range(1, 7) for j in range(1, 7) if pred(i, j)), 36)


def prob_item(t):
    if t == 'dice-sum':
        s = rng.choice([4, 5, 9, 10])
        ans = two_dice(lambda i, j: i + j == s)
        text = f"Two fair dice. P(the total is {s})?"
        wrong = [F(1, 11), two_dice(lambda i, j: i + j != s), ans * 2]
        why = ['each total equally likely', 'the complement', 'counted ordered pairs twice']
    elif t == 'at-least-one':
        n = rng.choice([2, 3])
        ans = 1 - F(5, 6) ** n
        text = f"Roll a fair die {"twice" if n == 2 else str(n) + " times"}. P(at least one six)?"
        wrong = [F(n, 6), F(5, 6) ** n, F(1, 6) ** n]
        why = ['n × p', 'the complement', 'every roll a six']
    elif t == 'cards':
        ans = F(12, 51)
        text = "Two cards from a 52-card deck. P(same suit)?"
        wrong = [F(1, 4), F(13, 52) * F(12, 51), F(39, 51)]
        why = ['with replacement', 'one named suit', 'the complement']
    elif t == 'coins':
        n = rng.choice([4, 5, 6])
        k = rng.choice([2, 3]) if n != 6 else 3
        ans = F(comb(n, k), 2 ** n)
        text = f"Flip a fair coin {n} times. P(exactly {k} heads)?"
        wrong = [F(1, 2 ** n), F(k, n), 1 - ans]
        why = ['one order only', 'k over n', 'the complement']
    elif t == 'bayes':
        base = rng.choice([1, 5, 10])
        sens, fpr = 9, 1  # 90% and 10%
        n = 1000
        tp = F(n * base, 100) * F(sens, 10)
        fp = F(n * (100 - base), 100) * F(fpr, 10)
        ans = tp / (tp + fp)
        text = f"{base}% of traders have an edge. A screen flags 90% of them and 10% of the rest. P(edge | flagged)?"
        wrong = [F(9, 10), tp / n, F(base, 100)]
        why = ['the hit rate', 'true positives over everyone', 'the base rate']
    elif t == 'ev':
        n = rng.choice([4, 6])
        ans = F(n + 1, 2) + F(1, n) * F(n + 1, 2)
        text = f"Roll a fair {n}-sided die; on a {n}, roll once more and add. Expected total?"
        wrong = [F(n + 1, 2), F(n + 1), F(n + 1, 2) + F(1, n)]
        why = ['ignored the reroll', 'always added', 'added 1 not the mean']
    seen, w, wy = {ans}, [], []
    for v, y in zip(wrong, why):
        if v not in seen and 0 <= v:
            seen.add(v); w.append(v); wy.append(y)
    assert len(w) == 3, (t, w)
    opts = list(zip(w, wy)) + [(ans, 'answer')]
    rng.shuffle(opts)
    return dict(kind=t, text=text, answer=ans, options=[o for o, _ in opts], why=[y for _, y in opts])


PT = ['dice-sum', 'at-least-one', 'cards', 'coins', 'bayes', 'ev']
rng.shuffle(PT)
P = [prob_item(t) for t in PT]


def show(x, frac=False):
    x = F(x)
    if frac and x.denominator != 1:
        return f"{x.numerator}/{x.denominator}"
    return fmt(x) if x.denominator == 1 or (x * 1000).denominator == 1 else f"{x.numerator}/{x.denominator}"


out = {}
for name, items in (('arith', A), ('seq', S), ('prob', P)):
    print(f'--- {name}')
    rows = []
    for i, it in enumerate(items):
        letter = LET[it['options'].index(it['answer'])]
        fr = name == 'prob' and it['kind'] != 'ev'
        ops = ' · '.join(f"{LET[j]} {show(o, fr)}" for j, o in enumerate(it['options']))
        print(f"Q{i + 1} [{it['kind']}] {it['text']} | {ops} | {letter} | {it.get('kinds') or it.get('rule') or it.get('why')}")
        rows.append(dict(kind=it['kind'], text=it['text'], options=[show(o, fr) for o in it['options']],
                         answer=show(it['answer'], fr), letter=letter,
                         note=it.get('kinds') or it.get('rule') or it.get('why')))
    out[name] = rows

json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'battery17.json'), 'w'), ensure_ascii=False, indent=1)
```

### gen17.py output

```text
--- arith
Q1 [mul] 12 × 20 | A 340 · B 32 · C 240 · D 24 | C | ['slip', 'reverse', 'answer', 'point']
Q2 [sub] 470 − 268 | A 738 · B 202 · C 201 · D 2,020 | B | ['reverse', 'answer', 'slip', 'point']
Q3 [dec] 7.6 × 5 | A 38 · B 380 · C 12.6 · D 39 | A | ['answer', 'point', 'reverse', 'slip']
Q4 [dec] 5.9 × 7 | A 4.13 · B 41.3 · C 42.3 · D 12.9 | B | ['point', 'answer', 'slip', 'reverse']
Q5 [sub] 654 − 379 | A 175 · B 275 · C 27.5 · D 1,033 | B | ['slip', 'answer', 'point', 'reverse']
Q6 [add] 885 + 728 | A 157 · B 1,613 · C 161.3 · D 1,513 | B | ['reverse', 'answer', 'point', 'slip']
Q7 [mul] 16 × 33 | A 49 · B 5,280 · C 538 · D 528 | D | ['reverse', 'point', 'slip', 'answer']
Q8 [add] 758 + 605 | A 1,363 · B 13,630 · C 153 · D 1,263 | A | ['answer', 'point', 'reverse', 'slip']
Q9 [add] 745 + 141 | A 604 · B 887 · C 88.6 · D 886 | D | ['reverse', 'slip', 'point', 'answer']
Q10 [sub] 587 − 210 | A 477 · B 377 · C 797 · D 37.7 | B | ['slip', 'answer', 'reverse', 'point']
Q11 [mul] 9 × 61 | A 70 · B 549 · C 5,490 · D 559 | B | ['reverse', 'answer', 'point', 'slip']
Q12 [pct] 45% of 240 | A 132 · B 108 · C 109 · D 10.8 | B | ['reverse', 'answer', 'slip', 'point']
Q13 [pct] 75% of 320 | A 140 · B 80 · C 24 · D 240 | D | ['slip', 'reverse', 'point', 'answer']
Q14 [div] 570 ÷ 15 | A 3.8 · B 39 · C 555 · D 38 | D | ['point', 'slip', 'reverse', 'answer']
Q15 [add] 614 + 435 | A 1,059 · B 104.9 · C 179 · D 1,049 | D | ['slip', 'point', 'reverse', 'answer']
Q16 [pct] 60% of 360 | A 144 · B 226 · C 216 · D 21.6 | C | ['reverse', 'slip', 'answer', 'point']
Q17 [div] 480 ÷ 12 | A 40 · B 468 · C 50 · D 4 | A | ['answer', 'reverse', 'slip', 'point']
Q18 [mul] 14 × 46 | A 644 · B 60 · C 64.4 · D 654 | A | ['answer', 'reverse', 'point', 'slip']
Q19 [div] 246 ÷ 6 | A 42 · B 41 · C 410 · D 240 | B | ['slip', 'answer', 'point', 'reverse']
Q20 [dec] 7.8 × 8 | A 15.8 · B 6.24 · C 72.4 · D 62.4 | D | ['reverse', 'point', 'slip', 'answer']
--- seq
Q1 [alternating] 2, 6, 5, 15, 14, 42, 41, ? | A 122 · B 123 · C 121 · D 40 | B | ×3 then −1, in turn
Q2 [squares] 17, 26, 37, 50, 65, ? | A 80 · B 82 · C 83 · D 81 | B | squares + 1
Q3 [times-plus] 4, 11, 25, 53, 109, ? | A 231 · B 218 · C 223 · D 221 | D | ×2 then +3
Q4 [geometric] 4, 12, 36, 108, 324, ? | A 648 · B 972 · C 975 · D 540 | B | ×3
Q5 [digit-sum] 21, 24, 30, 33, 39, 51, ? | A 63 · B 57 · C 58 · D 52 | B | add the digit sum
Q6 [interleaved] 3, 1, 7, 2, 11, 4, 15, ? | A 19 · B 26 · C 8 · D 12 | C | odd places +4, even places ×2
Q7 [fibonacci] 4, 3, 7, 10, 17, 27, ? | A 54 · B 44 · C 37 · D 45 | B | each term is the sum of the two before
Q8 [second-diff] 8, 12, 18, 26, 36, ? | A 47 · B 46 · C 50 · D 48 | D | gaps grow by 2
--- prob
Q1 [cards] Two cards from a 52-card deck. P(same suit)? | A 1/4 · B 13/17 · C 1/17 · D 4/17 | D | ['with replacement', 'the complement', 'one named suit', 'answer']
Q2 [dice-sum] Two fair dice. P(the total is 5)? | A 2/9 · B 1/9 · C 1/11 · D 8/9 | B | ['counted ordered pairs twice', 'answer', 'each total equally likely', 'the complement']
Q3 [coins] Flip a fair coin 5 times. P(exactly 3 heads)? | A 3/5 · B 11/16 · C 1/32 · D 5/16 | D | ['k over n', 'the complement', 'one order only', 'answer']
Q4 [ev] Roll a fair 4-sided die; on a 4, roll once more and add. Expected total? | A 2.75 · B 3.125 · C 2.5 · D 5 | B | ['added 1 not the mean', 'answer', 'ignored the reroll', 'always added']
Q5 [bayes] 10% of traders have an edge. A screen flags 90% of them and 10% of the rest. P(edge | flagged)? | A 9/10 · B 9/100 · C 1/2 · D 1/10 | C | ['the hit rate', 'true positives over everyone', 'answer', 'the base rate']
Q6 [at-least-one] Roll a fair die twice. P(at least one six)? | A 11/36 · B 25/36 · C 1/3 · D 1/36 | A | ['answer', 'the complement', 'n × p', 'every roll a six']
```

### gen18.py (the sample candidate) and its output

```python
"""l17 review: a sample candidate's marked battery, seeded with random.Random(18).
With chance 0.2 any question stalls at 2 to 3.5 times the pace.
Arithmetic: 3 to 8.5 s a question, right 85%, forward only, time runs out at 120 s (the rest blank).
Sequences: 50 to 150 s, right 80%, 800 s section. Probability: rushed, 25 to 60 s, right 55%, 720 s section.
Scoring: arithmetic +1 / -1 / 0; sequences and probability +1 / 0 / 0.
Error types: slip = wrong within the section pace; method gap = wrong over the pace;
time loss = right but over twice the pace."""
import random, json, os
here = os.path.dirname(os.path.abspath(__file__))
B = json.load(open(os.path.join(here, 'battery17.json')))
rng = random.Random(18)
SPEC = {'arith': (3.0, 8.5, 0.85, 120, 6), 'seq': (50, 150, 0.80, 800, 100), 'prob': (25, 60, 0.55, 720, 120)}
# a stall: with chance STALL a question takes 2 to 3.5 times the section pace instead
STALL = 0.2
SCORE = {'arith': (1, -1), 'seq': (1, 0), 'prob': (1, 0)}
out = {}
for sec, items in B.items():
    lo, hi, acc, limit, pace = SPEC[sec]
    t, rows = 0.0, []
    for i, it in enumerate(items):
        s = round(rng.uniform(lo, hi), 1)
        if rng.random() < STALL:
            s = round(rng.uniform(2 * pace, 3.5 * pace), 1)
        ok = rng.random() < acc
        if t + s > limit:
            rows.append(dict(q=i + 1, secs=None, mark='blank', text=it['text']))
            continue
        t = round(t + s, 1)
        kind = None
        if not ok:
            kind = 'S' if s <= pace else 'M'
        elif s > 2 * pace:
            kind = 'T'
        rows.append(dict(q=i + 1, secs=s, mark='right' if ok else 'wrong', type=kind, text=it['text']))
    R = sum(r['mark'] == 'right' for r in rows)
    W = sum(r['mark'] == 'wrong' for r in rows)
    Bk = sum(r['mark'] == 'blank' for r in rows)
    net = SCORE[sec][0] * R + SCORE[sec][1] * W
    out[sec] = dict(rows=rows, right=R, wrong=W, blank=Bk, net=net, time=t)
    print(f'--- {sec}: {R} right, {W} wrong, {Bk} blank, net {net}, time {t} s of {limit}')
    for r in rows:
        print(f"  Q{r['q']} {r['secs']} {r['mark']} {r.get('type') or ''}  {r['text']}")
print('total net', sum(v['net'] for v in out.values()))
json.dump(out, open(os.path.join(here, 'candidate18.json'), 'w'), ensure_ascii=False, indent=1)
```

```text
--- arith: 18 right, 2 wrong, 0 blank, net 16, time 119.2 s of 120
  Q1 4.0 right   12 × 20
  Q2 4.1 right   470 − 268
  Q3 5.6 right   7.6 × 5
  Q4 4.4 right   5.9 × 7
  Q5 6.7 wrong M  654 − 379
  Q6 8.2 right   885 + 728
  Q7 7.0 right   16 × 33
  Q8 6.7 right   758 + 605
  Q9 4.2 right   745 + 141
  Q10 8.4 right   587 − 210
  Q11 6.0 right   9 × 61
  Q12 7.5 right   45% of 240
  Q13 3.6 wrong S  75% of 320
  Q14 3.8 right   570 ÷ 15
  Q15 3.9 right   614 + 435
  Q16 5.4 right   60% of 360
  Q17 3.6 right   480 ÷ 12
  Q18 5.9 right   14 × 46
  Q19 7.5 right   246 ÷ 6
  Q20 12.7 right T  7.8 × 8
--- seq: 2 right, 4 wrong, 2 blank, net 2, time 588.2 s of 800
  Q1 104.3 wrong M  2, 6, 5, 15, 14, 42, 41, ?
  Q2 113.0 wrong M  17, 26, 37, 50, 65, ?
  Q3 118.2 wrong M  4, 11, 25, 53, 109, ?
  Q4 63.3 wrong S  4, 12, 36, 108, 324, ?
  Q5 97.8 right   21, 24, 30, 33, 39, 51, ?
  Q6 91.6 right   3, 1, 7, 2, 11, 4, 15, ?
  Q7 None blank   4, 3, 7, 10, 17, 27, ?
  Q8 None blank   8, 12, 18, 26, 36, ?
--- prob: 1 right, 5 wrong, 0 blank, net 1, time 555.9 s of 720
  Q1 25.6 right   Two cards from a 52-card deck. P(same suit)?
  Q2 30.7 wrong S  Two fair dice. P(the total is 5)?
  Q3 39.9 wrong S  Flip a fair coin 5 times. P(exactly 3 heads)?
  Q4 378.4 wrong M  Roll a fair 4-sided die; on a 4, roll once more and add. Expected total?
  Q5 39.8 wrong S  10% of traders have an edge. A screen flags 90% of them and 10% of the rest. P(edge | flagged)?
  Q6 41.5 wrong S  Roll a fair die twice. P(at least one six)?
total net 19
```

## Items that could seed the exams (for exam authors; no exam file written)

- `mock-oa-arith`: the 20 arithmetic items of l17 section A (seed 17) as fixed items, or the engine's `generator: "arith"` in a paper with `scoring: { right: 1, wrong: -1, blank: 0 }`, `navigation: "forward"`, `skip: false`, 80 items in 8 minutes and `passNet` about 50 (reported band 50 to 60). `gen17.py` also makes decimal and percentage items with the same three near misses, for the wider 80-in-8 mix.
- `mock-oa-trader`: l17 sections B (8 sequences) and C (6 probability), the l16 and homework sequence drills (12 sequences with one clear rule), the l15 drill and homework four-option probability rows (six with labelled slips), and the l14 drill and homework ranking pairs (12 pairs, as order or A/B/S items) for a ranking paper of about 10 in 10 minutes.
- Topic 3.3 exam: review-4 items `r-trade-twenty-four`, `r-rank-three`, `r-screen-ten-percent`, `r-digit-sum`, `r-rushed-section`; l13 quiz `q-half-penalty`; and a timed 80-in-8 part, as level 3 proposed.

## Proposed course.json change

None.

## Backlog

Five bullets under `Raised later (mental-pressure level 4):` in `docs/BACKLOG-INBOX.md`: lesson net scoring (another vote), timed lesson sections, the `table` cell `wrong[]` key (another vote), sequence and probability generators, and a legend for population grids.
