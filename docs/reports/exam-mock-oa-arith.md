# Report: mock exam `mock-oa-arith`

Brief: `docs/briefs/mocks.md`, preamble and section `## mock-oa-arith`. Generator and helpers: `/tmp/claude-0/-home-user-zero-to-quant/821a2fc9-d022-56ef-9082-6619f873e50b/scratchpad/mock-oa-arith/` (the orchestrator named this folder, in place of the brief's `exam-<id>/`).

## Files

- `app/content/exams/mock-oa-arith.json` (written by `fixed_arith.py`, seed `random.Random(80)`). One file, no versions, as the brief says.
- Shape: `id`, `name` "Arithmetic sprint: 80 in 8", `style` trader, `models`, `description`, `skills` (`mp-speed`, `mp-fractions`), then `parts`: paper `sprint` "80 in 8" (`minutes: 8`, `scoring` +1 / −1 / 0, `passNet: 55`, `navigation: "forward"`, `skip: false`) and check `no-calculator` "I used no calculator".
- The paper's `items` hold 32 entries: 16 generator entries (`n: 4`, `options: 4`, `skills: ["mp-speed"]`) each followed by one authored item, so 80 questions with authored items at Q5, Q10, ..., Q80.

## Item counts

| Block | Questions | Generator mix | Difficulty | Generated | Authored (in order) |
| --- | --- | --- | --- | --- | --- |
| A | Q1 to Q20 | add a, b [10, 99]; mul a [2, 9], b [2, 30]; sub, div 1 | 2 | 16 | Q5 percent, Q10 decimal, Q15 fraction, Q20 decimal |
| B | Q21 to Q40 | add, sub, mul, div 1 (warm-up defaults) | 3 | 16 | Q25 percent, Q30 decimal, Q35 fraction, Q40 percent |
| C | Q41 to Q60 | add a [100, 999], b [10, 99]; mul a [3, 12], b [12, 99] | 3 | 16 | Q45 decimal, Q50 fraction, Q55 percent, Q60 decimal |
| D | Q61 to Q80 | add a, b [100, 999]; mul a [11, 19], b [11, 49] | 4 | 16 | Q65 fraction, Q70 percent, Q75 decimal, Q80 fraction |

By family: generated 64 (count under `mental-arithmetic` per AUTHORING; see the backlog bullet), `arith-decimal` 6, `arith-fraction` 5, `arith-percent` 5. By difficulty: 20 at 2, 40 at 3, 20 at 4. Every authored item: four-option `choice`, `layout: "grid"`, `"shuffle": true`, `pace: 6`, skills `mp-speed` (decimals) or `mp-fractions` (fractions, percentages).

## Validator, voice and playthrough

- `node tools/validate.mjs 2>&1 | tail -5`: 0 errors (394 warnings, none on this file; all are other courses' unwritten lessons).
- `voice-scan.py` cannot target one file in `app/content/exams/` (it globs a folder), so a copy of the file went into `<scratch>/mock-oa-arith/voice/` and `VOICE_BASE` pointed there: 271 sentences, 0 over 20 words, 0 explanations over three sentences. `grep` finds no `!` and no em-dash.
- `node tools/playthrough.mjs --exam mock-oa-arith --local-cdn <pkgs>`: `ok 80 items, scored 80 of 80, passed`; `ok (mock checks) seed, clock at zero, attempts kept`. All passed.
- Same with `--mobile` (and once with `--why --shots`): all passed. The forward probe (no back, no jump, no step without an answer) runs during play and raised nothing. `ZQ.test.current()` on Q1 reads `forward: true, noSkip: true`.
- `startshot.mjs` (scratch folder) takes the start card at 1280 and 390 px and Q2, Q5, Q10, Q15, Q61, Q63, Q65, Q70, Q75, Q80 for seed 1, with no page errors and no sideways scroll at 390 px.

Start card text (from `startshot.mjs`): "80 questions · 8 minutes · pass 55 net · forward only, no skipping, negative marking", "Questions are generated afresh for each attempt", "No going back ... You must answer a question before the next one opens", "80 in 8: 55 net". That covers the acceptance line.

Screenshots looked at: start card (both widths), a generated item, each authored family, the check card, the results page and its explanations. Two faults were fixed in content:

1. `\tfrac` in the question and options drew the fractions at about 70% of the option text (numerators near 9 px at 390 px), hard to read at speed. Questions and options now use `\dfrac`; explanations and `why` lines keep `\tfrac`. This departs from the brief's "`\tfrac{a}{b}`" for display only; the fractions are still in lowest terms.
2. "25% of 280" mixed KaTeX and the bold sans prompt font. The percentage question is now one formula, `$25\% \text{ of } 280$`, as generated items are.

One fault is the engine's: at 390 px the start card's parts list (`.exm-parts`) squeezes its text into a column about 60 px wide ("80 / questions / · 8 / minutes ..."). Backlog bullet below.

## Generated items, seed 1 (engine's own `ZQ.arith.expand`, run in node by `gencheck.mjs`)

- Q2: $175 - 97$, key 78; options 88, 7.8, 272, 78. Check: $97 + 78 = 175$, and $175 - 100 + 3 = 78$.
- Q61: $11 \times 38$, key 418; options 318, 418, 4180, 49. Check: $380 + 38 = 418$, and $440 - 22 = 418$.
- Q63: $663 \div 17$, key 39; options 3.9, 39, 646, 38. Check: $17 \times 39 = 680 - 17 = 663$.

These match the brief. The Q63 screenshot in the browser shows the same options. `gencheck.mjs` also checks every generated key by its inverse operation and that the four options are distinct, for seeds 1, 2 and 12345: 64 generated, 0 bad each time.

## Authored items: keys and the two computations

The script holds every value as a `Fraction`. Method 1 is the closed form in `Fraction`s. Method 2 avoids `Fraction` arithmetic: `decimal.Decimal` on the shown strings for decimals and percentages (plus the ten-per-cent build), integer cross-multiplication reduced by `gcd` for fractions. Each distractor is recomputed from its named slip and asserted positive, not the key (as a `Fraction` and again as a `Decimal` or a cross-product), distinct as a value and as shown text, and within a factor of ten of the key.

| Q | Item | Key | Method 1 | Method 2 | Distractors (slip) |
| --- | --- | --- | --- | --- | --- |
| 5 | 25% of 280 | 70 | $\tfrac{25}{100} \cdot 280$ | $2 \times 28 + 14$; Decimal 0.25 × 280 | 210 (complement 75%), 56 (dropped the 5%: 20%), 7 (over 1000) |
| 10 | 0.4 × 35 | 14 | $\tfrac{4}{10} \cdot 35$ | $140 \div 10$; $12 + 2$ | 15 (slipped units), 140 (point), 87.5 (divided 35 by 0.4) |
| 15 | 3/4 + 7/12 | 4/3 | $\tfrac{9}{12} + \tfrac{7}{12}$ | $\tfrac{36 + 28}{48} = \tfrac{64}{48}$ | 5/8 (tops and bottoms, 10 over 16), 1/6 (subtracted), 5/6 (left the top of 3/4 as 3 over 12) |
| 20 | 6.3 × 3 | 18.9 | $\tfrac{63 \cdot 3}{10}$ | $18 + 0.9$; Decimal | 1.89 (point), 2.1 (divided), 18.8 (slipped tenths) |
| 25 | 15% of 160 | 24 | $\tfrac{15}{100} \cdot 160$ | $16 + 8$; Decimal | 136 (complement 85%), 16 (dropped the 5%), 2.4 (over 1000) |
| 30 | 9.2 × 0.2 | 1.84 | $\tfrac{92 \cdot 2}{100}$ | $1.8 + 0.04$; Decimal | 18.4 (point), 1.94 (slipped tenths), 2.84 (slipped units) |
| 35 | 1/2 + 1/3 | 5/6 | $\tfrac36 + \tfrac26$ | $\tfrac{3 + 2}{6}$ | 2/5 (tops and bottoms), 1/6 (subtracted), 2/3 (scaled 1/2 by 2, not 3) |
| 40 | 60% of 240 | 144 | $\tfrac{60}{100} \cdot 240$ | $6 \times 24$; Decimal | 96 (complement 40%), 120 (dropped the 10%: 50%), 14.4 (over 1000) |
| 45 | 2.8 ÷ 0.7 | 4 | $\tfrac{28/10}{7/10}$ | $28 \div 7$; $0.7 \times 4 = 2.8$ | 40 (point), 1.96 (multiplied), 5 (slipped units) |
| 50 | 2/9 − 1/6 | 1/18 | $\tfrac{4}{18} - \tfrac{3}{18}$ | $\tfrac{12 - 9}{54} = \tfrac{3}{54}$ | 1/3 (tops and bottoms, 1 over 3), 7/18 (added), 1/6 (scaled 2/9 by 3, not 2) |
| 55 | 65% of 280 | 182 | $\tfrac{65}{100} \cdot 280$ | $6 \times 28 + 14$; Decimal | 98 (complement 35%), 168 (dropped the 5%), 18.2 (over 1000) |
| 60 | 1.8 × 2.4 | 4.32 | $\tfrac{18 \cdot 24}{100}$ | $2.4 + 1.92$; Decimal | 43.2 (point), 0.75 (divided), 5.32 (slipped units) |
| 65 | 5/6 + 3/8 | 29/24 | $\tfrac{20}{24} + \tfrac{9}{24}$ | $\tfrac{40 + 18}{48} = \tfrac{58}{48}$ | 4/7 (tops and bottoms), 11/24 (subtracted), 1 (scaled 5/6 by 3, not 4) |
| 70 | 35% of 260 | 91 | $\tfrac{35}{100} \cdot 260$ | $3 \times 26 + 13$; Decimal | 169 (complement 65%), 78 (dropped the 5%), 9.1 (over 1000) |
| 75 | 3.6 ÷ 0.12 | 30 | $\tfrac{36/10}{12/100}$ | $360 \div 12$; $0.12 \times 30 = 3.6$ | 31 (slipped units), 300 (point), 0.432 (multiplied) |
| 80 | 3/4 + 3/10 | 21/20 | $\tfrac{15}{20} + \tfrac{6}{20}$ | $\tfrac{30 + 12}{40} = \tfrac{42}{40}$ | 3/7 (tops and bottoms), 9/20 (subtracted), 3/2 (scaled 3/10 by 5, not 2) |

I also checked every row by hand a third time.

Q65 and Q70 are the brief's worked items, as written. Q10 and Q75 are the brief's items with one change each (below); the script asserts all four option sets. The other twelve are drawn. Ranges: A decimals are one-place decimals times a digit, A fractions have one denominator dividing the other, A percentages are 20% or 25%. B: one-place times a tenth below 1, coprime denominators (common multiple up to 12), 15% or 60%. C: division by a one-place decimal with a whole answer, then a product of two one-place decimals above 1 (no squares, and a reverse distractor required), subtraction with a common multiple up to 20, 65% or 85%. D: a sum whose denominators have a common multiple from 12 to 24, neither dividing the other.

Distractor kinds: decimals take one misplaced point (times or over ten), the reverse operation when it is a terminating near miss, and slipped digits otherwise. Fractions take the tops and bottoms, the wrong operation and one fraction scaled by the wrong factor (the other fraction's factor, or 1 when one denominator divides the other). Percentages take the complement, the dropped part and a misplaced point. The drawn items are also asserted free of two giveaways: the key flanked by its own times-ten and over-ten, and the key flanked by two equal slips (7.12, 8.12, 9.12 was the first draw for Q60).

### Departures from the brief, for the orchestrator

- **Q75 breaks the factor-of-ten rule as written.** 0.432 is about 69 times below 30. The brief says to use the worked item as written, so the script exempts that one distractor (`NEAR_EXEMPT`) and asserts the rule everywhere else. Proposal: replace 0.432 with a slipped digit such as 31, or keep it as a real "multiplied instead" slip.
- **Q10 and Q75 changed (coordinator's instruction, after the first hand-back).** As written, their options 1.4, 14, 140 and 3, 30, 300 put the key in the middle of a times-ten triple. Each over-ten distractor is now a slipped units digit: Q10 is 14, 15, 140, 87.5 and Q75 is 30, 31, 300, 0.432. Twice: $15 \ne 14 = 0.4 \times 35 = 140 \div 10$; $31 \ne 30 = 3.6 \div 0.12 = 360 \div 12$, with $0.12 \times 30 = 3.6$. The script asserts that no item, worked or drawn, has the triple or two equal slips around the key. Validate (0 errors) and both playthroughs were rerun and passed.
- **10% and 50% are not drawn in block A.** 50% equals its own complement, and 10% has no part to drop, so neither can carry the three named slips. Block A draws 20% or 25%.
- **`models` is two sentences.** The brief's line is one 24-word sentence. It now reads "Reported, as of Nov 2026: Optiver's 80 in 8. Eighty four-option arithmetic questions in 8 minutes; +1 right, −1 wrong, no skipping, no calculator." The content is the same and it is 147 characters.
- **`\dfrac` in the question and options** (see above), and the percentage question as one formula.
- Q10's `feedback.correct` is "$4 \times 35 = 140$, and one decimal place gives 14." in the pattern of the others, not the brief's sample clause "Four tenths of 35 is 14."

## Firm names

"Optiver" appears only in `models` and `description`, each time with "reported" and "Nov 2026". It is not in `name`, items, feedback or explanations (checked with `grep`).

## Prerequisites (cited; nothing is gated)

mental-pressure `l1-towards-fifty`, `l2-two-by-two`, `l3-big-division`, `l4-decimals-fast`, `l5-which-fraction`, `l6-percent-of-percent`, `l9-eighty-in-eight`, `l12-mock-test`, `l13-negative-marking`.

## Proposed changes

- No `course.json` change. No `prep.json` change.
- The brief's worked Q10 and Q75 rows could be updated to match the file (15 for 1.4, 31 for 3).
- AUTHORING section 5 could say that fraction options in a `choice` read better as `\dfrac` (see the backlog bullet).

## Script: `fixed_arith.py` (seed 80) and its output

Run: `python3 fixed_arith.py [out.json]` (default output is the exam file). It needs only the standard library (`fractions`, `decimal`, `math`, `random`, `json`).

Output:

```text
wrote /home/user/zero-to-quant/app/content/exams/mock-oa-arith.json: 32 entries, 80 questions, seed 80
Q5  A q05-percent    25% of 280     key 70               210 (complement); 56 (dropped); 7 (point-down)
Q10 A q10-decimal    0.4 × 35       key 14               15 (slip-0); 140 (point-up); 87.5 (reverse-yx)
Q15 A q15-fraction   3/4 + 7/12     key \dfrac{4}{3}     \dfrac{5}{8} (tops); \dfrac{1}{6} (wrongop); \dfrac{5}{6} (scale-0-1)
Q20 A q20-decimal    6.3 × 3        key 18.9             1.89 (point-down); 2.1 (reverse); 18.8 (slip--1)
Q25 B q25-percent    15% of 160     key 24               136 (complement); 16 (dropped); 2.4 (point-down)
Q30 B q30-decimal    9.2 × 0.2      key 1.84             18.4 (point-up); 1.94 (slip--1); 2.84 (slip-0)
Q35 B q35-fraction   1/2 + 1/3      key \dfrac{5}{6}     \dfrac{2}{5} (tops); \dfrac{1}{6} (wrongop); \dfrac{2}{3} (scale-0-2)
Q40 B q40-percent    60% of 240     key 144              96 (complement); 120 (dropped); 14.4 (point-down)
Q45 C q45-decimal    2.8 ÷ 0.7      key 4                40 (point-up); 1.96 (reverse); 5 (slip-0)
Q50 C q50-fraction   2/9 − 1/6      key \dfrac{1}{18}    \dfrac{1}{3} (tops); \dfrac{7}{18} (wrongop); \dfrac{1}{6} (scale-0-3)
Q55 C q55-percent    65% of 280     key 182              98 (complement); 168 (dropped); 18.2 (point-down)
Q60 C q60-decimal    1.8 × 2.4      key 4.32             43.2 (point-up); 0.75 (reverse); 5.32 (slip-0)
Q65 D q65-fraction   5/6 + 3/8      key \dfrac{29}{24}   \dfrac{4}{7} (tops); \dfrac{11}{24} (wrongop); 1 (scale-0-3)
Q70 D q70-percent    35% of 260     key 91               169 (complement); 78 (dropped); 9.1 (point-down)
Q75 D q75-decimal    3.6 ÷ 0.12     key 30               31 (slip-0); 300 (point-up); 0.432 (reverse)
Q80 D q80-fraction   3/4 + 3/10     key \dfrac{21}{20}   \dfrac{3}{7} (tops); \dfrac{9}{20} (wrongop); \dfrac{3}{2} (scale-1-5)
```

```python
#!/usr/bin/env python3
"""fixed_arith.py: writes app/content/exams/mock-oa-arith.json (brief: docs/briefs/mocks.md, section mock-oa-arith).

The paper is 16 groups. Each group is one engine generator entry (n: 4, whole numbers, drawn afresh per sitting)
followed by one authored item at Q5, Q10, ..., Q80. This script makes the 16 authored items: the four worked ones
from the brief as written (Q10, Q65, Q70, Q75) and twelve drawn with random.Random(80).

Every number is a Fraction. Each key is computed twice: the Fraction closed form, and a second method that does not
use Fraction arithmetic (decimal.Decimal for decimals and percentages, integer cross-multiplication with gcd for
fractions). Each distractor is computed from its own named slip and asserted positive, wrong, distinct (as a value
and as displayed text) and within a factor of ten of the key (Q75's worked 0.432 is the one recorded exception).
Usage: python3 fixed_arith.py [out.json]
"""
import json
import random
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as F
from math import gcd

getcontext().prec = 40
SEED = 80
OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/user/zero-to-quant/app/content/exams/mock-oa-arith.json'
rng = random.Random(SEED)
WORD = {0: 'no', 1: 'one', 2: 'two', 3: 'three', 4: 'four'}
NEAR_EXEMPT = {('q75-decimal', 'reverse')}  # the brief's worked Q75 keeps 0.432 (multiplied), 69 times below 30


# ---------- text ----------
def places(x):
    """decimal places of a terminating Fraction"""
    x = F(x)
    for k in range(0, 9):
        if (x * 10 ** k).denominator == 1:
            return k
    raise AssertionError(('not terminating', x))


def num(x):
    """a terminating Fraction as a decimal string, checked against Decimal"""
    x = F(x)
    k = places(x)
    n = x * 10 ** k
    assert n.denominator == 1
    s = str(Decimal(n.numerator).scaleb(-k))
    if 'E' in s:
        s = format(Decimal(n.numerator).scaleb(-k), 'f')
    assert F(s) == x, (s, x)
    return s


def ftex(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f"\\tfrac{{{x.numerator}}}{{{x.denominator}}}"


def dtex(x):
    """a fraction at full size, for the question line and the options (tfrac draws at about 70% size)"""
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f"\\dfrac{{{x.numerator}}}{{{x.denominator}}}"


def fplain(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def pct_tex(p):
    return f"{num(p)}\\%"


def near(d, key):
    return key / 10 <= d <= key * 10


def place_name(power):
    return {2: 'hundreds', 1: 'tens', 0: 'units', -1: 'tenths', -2: 'hundredths', -3: 'thousandths'}[power]


def slip(key, avoid):
    """a slipped digit: one digit of the key off by one; returns (value, place power) or None"""
    s = num(key)
    digits = [i for i, c in enumerate(s) if c.isdigit()]
    point = s.index('.') if '.' in s else len(s)
    order = digits[:]
    rng.shuffle(order)
    for i in order:
        if i == digits[0] and s[i] == '0':
            continue  # the leading 0 of 0.42 is not a digit a solver slips
        for step in rng.sample([1, -1], 2):
            d = int(s[i]) + step
            if d < 0 or d > 9 or (i == digits[0] and d == 0) or (i == len(s) - 1 and '.' in s and d == 0):
                continue  # no wrap from 0 to 9, no new leading zero, no trailing zero that hides the point
            t = s[:i] + str(d) + s[i + 1:]
            v = F(t)
            power = point - i - 1 if i < point else point - i
            if v > 0 and v != key and near(v, key) and v not in avoid and abs(power) <= 3:
                return v, power
    return None


# ---------- items ----------
def decimal_mul(qid, x, y):
    x, y = F(x), F(y)
    key = x * y
    px, py = places(x), places(y)
    P = px + py
    ix, iy = int(x * 10 ** px), int(y * 10 ** py)
    I = ix * iy
    # second method: Decimal on the shown strings
    assert F(str(Decimal(num(x)) * Decimal(num(y)))) == key
    assert F(I, 10 ** P) == key
    return dict(qid=qid, kind='dec', op='mul', x=x, y=y, key=key, P=P, ix=ix, iy=iy, I=I,
                q=f"{num(x)} \\times {num(y)}", plain=f"{num(x)} × {num(y)}")


def decimal_div(qid, x, y):
    x, y = F(x), F(y)
    key = x / y
    py = max(places(y), places(x))
    X, Y = x * 10 ** py, y * 10 ** py
    assert X.denominator == 1 and Y.denominator == 1
    assert F(str(Decimal(num(x)) / Decimal(num(y)))) == key
    assert key * y == x
    return dict(qid=qid, kind='dec', op='div', x=x, y=y, key=key, py=py, X=int(X), Y=int(Y),
                q=f"{num(x)} \\div {num(y)}", plain=f"{num(x)} ÷ {num(y)}")


def dec_options(it, plan=None):
    """distractors for a decimal item: a misplaced point, the reverse operation (if a near miss), slipped digits"""
    key, x, y = it['key'], it['x'], it['y']
    out = []
    want = plan or ['point', 'reverse', 'slip']
    used = set()
    for k in want:
        if k == 'point' or k in ('point-up', 'point-down'):
            up = (k == 'point-up') if k != 'point' else rng.random() < 0.5
            v = key * 10 if up else key / 10
            out.append((v, 'point-up' if up else 'point-down'))
        elif k == 'reverse':
            v = x / y if it['op'] == 'mul' else x * y
            ok = v > 0 and v != key and v not in [o[0] for o in out]
            ok = ok and ((v * 10 ** 4).denominator == 1) and (near(v, key) or (it['qid'], 'reverse') in NEAR_EXEMPT)
            if ok:
                out.append((v, 'reverse'))
            else:
                s = slip(key, {key} | {o[0] for o in out})
                out.append((s[0], ('slip', s[1])))
        elif k == 'slip':
            s = slip(key, {key} | {o[0] for o in out})
            out.append((s[0], ('slip', s[1])))
        used.add(k)
    return out


def dec_why(it, kind):
    x, y = num(it['x']), num(it['y'])
    if it['op'] == 'mul':
        P = it['P']
        if kind == 'point-up':
            if P == 1:
                return f"You worked out ${it['ix']} \\times {it['iy']} = {it['I']}$ and left out the point."
            return f"You put back {WORD[P - 1]} decimal place{'s' if P - 1 > 1 else ''}, but the two numbers have {WORD[P]} between them."
        if kind == 'point-down':
            return f"You put back {WORD[P + 1]} decimal places, but the two numbers have only {WORD[P]} between them."
        if kind == 'reverse':
            return f"You divided {x} by {y} instead of multiplying."
        if kind == 'reverse-yx':
            return f"You divided {y} by {x} instead of multiplying."
    else:
        if kind == 'point-up':
            return f"You moved the point in {x} one place more than in {y}."
        if kind == 'point-down':
            return f"You moved the point in {y} one place more than in {x}."
        if kind == 'reverse':
            return f"You multiplied {x} by {y} instead of dividing."
    if isinstance(kind, tuple) and kind[0] == 'slip':
        return f"You slipped the {place_name(kind[1])} digit by one."
    raise ValueError(kind)


def dec_split_check(it):
    """the explain's check line for a product: split one factor into easy parts"""
    x, y, key = it['x'], it['y'], it['key']
    for a, b in ((x, y), (y, x)):
        whole, frac = F(int(a)), a - int(a)
        if whole >= 1 and frac > 0:
            assert whole * b + frac * b == key
            return f"${num(whole)} \\times {num(b)} + {num(frac)} \\times {num(b)} = {num(whole * b)} + {num(frac * b)} = {num(key)}$"
    for a, b in ((y, x), (x, y)):
        if a.denominator == 1 and a >= 10 and a % 10:
            t, u = F(a - a % 10), F(a % 10)
            assert b * t + b * u == key
            return f"${num(b)} \\times {num(t)} + {num(b)} \\times {num(u)} = {num(b * t)} + {num(b * u)} = {num(key)}$"
    assert key / y == x
    return f"${num(key)} \\div {num(y)} = {num(x)}$"


def dec_text(it):
    x, y, key = num(it['x']), num(it['y']), num(it['key'])
    if it['op'] == 'mul':
        P = it['P']
        pl = f"{WORD[P]} decimal place{'s' if P > 1 else ''}"
        correct = f"${it['ix']} \\times {it['iy']} = {it['I']}$, and {pl} gives {key}."
        generic = f"Multiply {it['ix']} by {it['iy']}, then put back {pl}."
        explain = f"${x} \\times {y} = {it['I']} \\div {10 ** P} = {key}$. Check: {dec_split_check(it)}."
    else:
        py = it['py']
        correct = f"${it['X']} \\div {it['Y']} = {key}$."
        generic = f"Move both points {WORD[py]} place{'s' if py > 1 else ''} right, then divide {it['X']} by {it['Y']}."
        assert F(it['X'], it['Y']) == it['key']
        explain = f"${x} \\div {y} = {it['X']} \\div {it['Y']} = {key}$. Check: ${y} \\times {key} = {x}$."
    return correct, generic, explain


def fraction_item(qid, p, q, r, s, op, slip_frac=None):
    """p/q op r/s. slip_frac: which fraction (0 or 1) the wrong-factor slip scales"""
    a, b = F(p, q), F(r, s)
    assert a.numerator == p and a.denominator == q and b.numerator == r and b.denominator == s, 'lowest terms'
    L = q * s // gcd(q, s)
    fq, fs = L // q, L // s
    key = a + b if op == '+' else a - b
    # second method: cross-multiply with integers, reduce by gcd
    n2 = p * s + r * q if op == '+' else p * s - r * q
    d2 = q * s
    g = gcd(n2, d2)
    assert (n2 // g, d2 // g) == (key.numerator, key.denominator), (n2, d2, key)
    assert key > 0
    return dict(qid=qid, kind='frac', p=p, q=q, r=r, s=s, op=op, L=L, fq=fq, fs=fs, key=key, slip_frac=slip_frac,
                q_tex=f"\\tfrac{{{p}}}{{{q}}} {'+' if op == '+' else '-'} \\tfrac{{{r}}}{{{s}}}",
                q_show=f"\\dfrac{{{p}}}{{{q}}} {'+' if op == '+' else '-'} \\dfrac{{{r}}}{{{s}}}",
                plain=f"{p}/{q} {'+' if op == '+' else '−'} {r}/{s}")


def frac_options(it):
    p, q, r, s, op, L, fq, fs = (it[k] for k in ('p', 'q', 'r', 's', 'op', 'L', 'fq', 'fs'))
    sign = 1 if op == '+' else -1
    out = []
    # added (or subtracted) the tops and the bottoms
    if op == '+':
        out.append((F(p + r, q + s), 'tops'))
    else:
        assert p - r > 0 and q - s > 0
        out.append((F(p - r, q - s), 'tops'))
    # the wrong operation
    out.append((F(p, q) - F(r, s) if op == '+' else F(p, q) + F(r, s), 'wrongop'))
    # one fraction scaled by the wrong factor: its bottom goes to L, its top by the other factor (or by 1)
    which = it['slip_frac']
    if which == 0:
        wrong = fs if fs != fq else 1
        top = p * wrong + sign * r * fs
        out.append((F(top, L), ('scale', 0, wrong)))
    else:
        wrong = fq if fq != fs else 1
        top = p * fq + sign * r * wrong
        out.append((F(top, L), ('scale', 1, wrong)))
    return out


def frac_why(it, kind):
    p, q, r, s, L, fq, fs = (it[k] for k in ('p', 'q', 'r', 's', 'L', 'fq', 'fs'))
    if kind == 'tops':
        if it['op'] == '+':
            return f"You added the tops and the bottoms, {p + r} over {q + s}."
        return f"You subtracted the tops and the bottoms, {p - r} over {q - s}."
    if kind == 'wrongop':
        return "You subtracted instead of adding." if it['op'] == '+' else "You added instead of subtracting."
    _, which, wrong = kind
    t, b, right = (p, q, fq) if which == 0 else (r, s, fs)
    if wrong == 1:
        return f"You rewrote $\\tfrac{{{t}}}{{{b}}}$ over {L} but left its top as {t}."
    return f"You scaled $\\tfrac{{{t}}}{{{b}}}$ by {wrong}, not {right}, so its top became {t * wrong} over {L}."


def frac_text(it):
    p, q, r, s, L, fq, fs, key = (it[k] for k in ('p', 'q', 'r', 's', 'L', 'fq', 'fs', 'key'))
    sym = '+' if it['op'] == '+' else '-'
    A, B = p * fq, r * fs
    top = A + B if it['op'] == '+' else A - B
    word = 'add' if it['op'] == '+' else 'subtract'
    chain = f"\\tfrac{{{A}}}{{{L}}} {sym} \\tfrac{{{B}}}{{{L}}} = \\tfrac{{{top}}}{{{L}}}"
    if (top, L) != (key.numerator, key.denominator):
        chain += f" = {ftex(key)}"
    n2 = p * s + r * q if it['op'] == '+' else p * s - r * q
    d2 = q * s
    chk = f"\\tfrac{{{p} \\cdot {s} {sym} {r} \\cdot {q}}}{{{d2}}} = \\tfrac{{{n2}}}{{{d2}}}"
    if (n2, d2) != (key.numerator, key.denominator):
        chk += f" = {ftex(key)}"
    if (top, L) != (key.numerator, key.denominator):
        correct = f"Over {L} the tops are {A} and {B}, and $\\tfrac{{{top}}}{{{L}}} = {ftex(key)}$."
    else:
        correct = f"Over {L} the tops are {A} and {B}, so ${ftex(key)}$."
    generic = f"Write both over {L}, then {word} the tops."
    explain = f"${it['q_tex']} = {chain}$. Check: ${chk}$."
    return correct, generic, explain


DROP = {F(20): F(10), F(25): F(20), F(15): F(10), F(60): F(50), F(65): F(60), F(85): F(80),
        F(35): F(30), F(45): F(40), F(25, 2): F(10), F(75): F(50)}


def pct_item(qid, p, n):
    p, n = F(p), F(n)
    key = p * n / 100
    # second method: Decimal on the shown numbers, and the ten-per-cent build the explain shows
    assert F(str(Decimal(num(p)) / Decimal(100) * Decimal(num(n)))) == key
    m, rem = divmod(p, 10)
    t = n / 10
    assert m * t + rem * n / 100 == key
    return dict(qid=qid, kind='pct', p=p, n=n, key=key, m=int(m), rem=rem, t=t,
                q=f"{pct_tex(p)}", plain=f"{num(p)}% of {num(n)}")


def pct_options(it, point=None):
    p, n, key = it['p'], it['n'], it['key']
    up = (rng.random() < 0.5 or key < 10) if point is None else point == 'up'
    return [((100 - p) * n / 100, 'complement'), (DROP[p] * n / 100, 'dropped'),
            (key * 10 if up else key / 10, 'point-up' if up else 'point-down')]


def pct_why(it, kind):
    p, n = it['p'], it['n']
    if kind == 'complement':
        return f"You found the ${pct_tex(100 - p)}$ left over, not ${pct_tex(p)}$."
    if kind == 'dropped':
        k = DROP[p]
        if p - k == k:
            return f"You found ${pct_tex(k)}$ and did not double it."
        return f"You found ${pct_tex(k)}$ and dropped the ${pct_tex(p - k)}$."
    if kind == 'point-up':
        return f"You divided by 10, not 100, when you took the per cent."
    if kind == 'point-down':
        return f"You divided by 1000, not 100, when you took the per cent."
    raise ValueError(kind)


def pct_text(it):
    p, n, key, m, rem, t = (it[k] for k in ('p', 'n', 'key', 'm', 'rem', 't'))
    u = rem * n / 100
    if rem and m == 1:
        build = f"$10\\%$ of {num(n)} is {num(t)} and ${pct_tex(rem)}$ is {num(u)}, so ${pct_tex(p)}$ is ${num(t)} + {num(u)} = {num(key)}$."
    elif rem:
        build = f"$10\\%$ of {num(n)} is {num(t)} and ${pct_tex(rem)}$ is {num(u)}, so ${pct_tex(p)}$ is ${m} \\times {num(t)} + {num(u)} = {num(key)}$."
    else:
        build = f"$10\\%$ of {num(n)} is {num(t)}, so ${pct_tex(p)}$ is ${m} \\times {num(t)} = {num(key)}$."
    explain = f"{build} Check: ${num(p / 100)} \\times {num(n)} = {num(key)}$."
    correct = f"Ten per cent of {num(n)} is {num(t)}, so ${pct_tex(p)}$ is {num(key)}."
    generic = f"Find $10\\%$ of {num(n)}, then build ${pct_tex(p)}$ from it."
    return correct, generic, explain


# ---------- assembling one item ----------
def finish(it, opts):
    key = it['key']
    vals = [v for v, _ in opts]
    assert len(opts) == 3
    texts = {}
    for v, k in opts:
        assert v > 0, (it['qid'], v)
        assert v != key, (it['qid'], 'distractor equals key', v)
        assert (it['qid'], k if isinstance(k, str) else k[0]) in NEAR_EXEMPT or near(v, key), (it['qid'], k, v, key)
    assert len(set(vals)) == 3, (it['qid'], vals)
    show = dtex if it['kind'] == 'frac' else num
    texts = [show(key)] + [show(v) for v in vals]
    assert len(set(texts)) == 4, (it['qid'], texts)
    # each distractor recomputed from its named slip, a second time
    for v, k in opts:
        if it['kind'] == 'dec':
            x, y = it['x'], it['y']
            want = {'point-up': key * 10, 'point-down': key / 10, 'reverse': x / y if it['op'] == 'mul' else x * y,
                    'reverse-yx': y / x}.get(k)
            if want is not None:
                assert v == want, (it['qid'], k, v, want)
            else:
                a, b = num(v), num(key)
                assert k[0] == 'slip' and len(a) == len(b) and sum(c != d for c, d in zip(a, b)) == 1, (it['qid'], a, b)
                assert all(abs(int(c) - int(d)) == 1 for c, d in zip(a, b) if c != d)
        elif it['kind'] == 'pct':
            want = {'complement': (100 - it['p']) * it['n'] / 100, 'dropped': DROP[it['p']] * it['n'] / 100,
                    'point-up': it['p'] * it['n'] / 10, 'point-down': it['p'] * it['n'] / 1000}[k]
            assert v == want, (it['qid'], k)
        else:
            p, q, r, s_, L = it['p'], it['q'], it['r'], it['s'], it['L']
            sg = 1 if it['op'] == '+' else -1
            if k == 'tops':
                assert v == F(p + sg * r, q + sg * s_)
            elif k == 'wrongop':
                assert v == F(p, q) - sg * F(r, s_)
            else:
                _, which, wrong = k
                tops = [p * L // q, r * L // s_]
                tops[which] = (p, r)[which] * wrong
                assert wrong * (q, s_)[which] != L  # the factor really is wrong
                assert v == F(tops[0] + sg * tops[1], L)
    # second check that each distractor is wrong: compare as Decimal (or as reduced integer pairs) to the key
    for v in vals:
        if it['kind'] == 'frac':
            assert (v.numerator * key.denominator) != (key.numerator * v.denominator)
        else:
            assert Decimal(num(v)) != Decimal(num(key))
    if it['kind'] == 'dec':
        whys = [dec_why(it, k) for _, k in opts]
        correct, generic, explain = dec_text(it)
        question = f"${it['q']}$"
        tags, skills = ['arith-decimal'], ['mp-speed']
    elif it['kind'] == 'frac':
        whys = [frac_why(it, k) for _, k in opts]
        correct, generic, explain = frac_text(it)
        question = f"${it['q_show']}$"
        tags, skills = ['arith-fraction'], ['mp-fractions']
    else:
        whys = [pct_why(it, k) for _, k in opts]
        correct, generic, explain = pct_text(it)
        question = f"${it['q']} \\text{{ of }} {num(it['n'])}$"
        tags, skills = ['arith-percent'], ['mp-fractions']
    options = [{"id": "a", "text": f"${show(key)}$", "correct": True}]
    for letter, (v, k), w in zip('bcd', opts, whys):
        options.append({"id": letter, "text": f"${show(v)}$", "why": w})
    item = {
        "id": it['qid'], "difficulty": it['difficulty'], "skills": skills, "tags": tags, "pace": 6,
        "title": it['plain'], "question": question,
        "widget": {"kind": "choice", "layout": "grid", "shuffle": True, "label": "Answer options", "options": options},
        "feedback": {"correct": correct, "generic": generic},
        "explain": {"text": explain},
    }
    row = (it['qid'], it['plain'], show(key), [(show(v), k if isinstance(k, str) else '-'.join(map(str, k))) for v, k in opts])
    return item, row


# ---------- the paper ----------
GEN = {
    'A': {"add": {"weight": 1, "a": [10, 99], "b": [10, 99]}, "sub": 1, "mul": {"weight": 1, "a": [2, 9], "b": [2, 30]}, "div": 1},
    'B': {"add": 1, "sub": 1, "mul": 1, "div": 1},
    'C': {"add": {"weight": 1, "a": [100, 999], "b": [10, 99]}, "sub": 1, "mul": {"weight": 1, "a": [3, 12], "b": [12, 99]}, "div": 1},
    'D': {"add": {"weight": 1, "a": [100, 999], "b": [100, 999]}, "sub": 1, "mul": {"weight": 1, "a": [11, 19], "b": [11, 49]}, "div": 1},
}
DIFF = {'A': 2, 'B': 3, 'C': 3, 'D': 4}
KINDS = {'A': ['pct', 'dec', 'frac', 'dec'], 'B': ['pct', 'dec', 'frac', 'pct'],
         'C': ['dec', 'frac', 'pct', 'dec'], 'D': ['frac', 'pct', 'dec', 'frac']}
NAME = {'dec': 'decimal', 'frac': 'fraction', 'pct': 'percent'}


def coprime_frac(den):
    while True:
        t = rng.randint(1, den - 1)
        if gcd(t, den) == 1:
            return t


def draw(block, slot, kind, qid):
    """the twelve drawn items; each loop redraws until every distractor rule holds"""
    for _ in range(500):
        try:
            if kind == 'dec':
                if block == 'A':  # one-place decimal times a digit
                    a = rng.choice([v for v in range(11, 100) if v % 10])
                    it = decimal_mul(qid, F(a, 10), rng.randint(3, 9))
                elif block == 'B':  # one-place decimal times a tenth-place decimal below 1
                    a = rng.choice([v for v in range(12, 100) if v % 10])
                    it = decimal_mul(qid, F(a, 10), F(rng.randint(2, 9), 10))
                elif slot == 0:  # C: division by a one-place decimal, whole answer
                    y = F(rng.randint(3, 9), 10)
                    k = rng.randint(4, 19)
                    if (k * y).denominator == 1:
                        continue
                    it = decimal_div(qid, k * y, y)
                else:  # C: two one-place decimals above 1
                    a = rng.choice([v for v in range(11, 50) if v % 10])
                    b = rng.choice([v for v in range(11, 30) if v % 10 and v != a])  # no square, so the reverse is not 1
                    it = decimal_mul(qid, F(a, 10), F(b, 10))
                opts = dec_options(it)
                if block == 'C' and slot == 1:
                    assert any(k == 'reverse' for _, k in opts)  # C's product keeps a reverse-operation distractor
            elif kind == 'frac':
                if block == 'A':  # unlike denominators, one divides the other
                    q, s = rng.choice([(2, 4), (2, 6), (3, 6), (4, 8), (2, 8), (3, 9), (4, 12), (3, 12), (5, 10), (6, 12)])
                    op, which = '+', 0
                elif block == 'B':  # coprime denominators, common multiple up to 12
                    q, s = rng.choice([(2, 3), (3, 2), (2, 5), (5, 2), (3, 4), (4, 3)])
                    op, which = '+', rng.randint(0, 1)
                elif block == 'C':  # subtraction, common multiple up to 20
                    q, s = rng.choice([(4, 6), (6, 4), (3, 5), (5, 3), (4, 5), (5, 4), (6, 9), (9, 6), (4, 10), (10, 4)])
                    op, which = '-', rng.randint(0, 1)
                else:  # D: neither divides the other, common multiple 12 to 24
                    q, s = rng.choice([(4, 6), (6, 4), (6, 8), (8, 6), (3, 8), (8, 3), (4, 10), (10, 4), (6, 9), (9, 6), (4, 6)])
                    op, which = '+', rng.randint(0, 1)
                p, r = coprime_frac(q), coprime_frac(s)
                if op == '-' and F(p, q) <= F(r, s):
                    continue
                it = fraction_item(qid, p, q, r, s, op, which)
                opts = frac_options(it)
            else:
                if block == 'A':
                    p, n = rng.choice([F(20), F(25)]), 20 * rng.randint(2, 24)
                elif block == 'B':
                    p, n = rng.choice([F(15), F(60)]), 20 * rng.randint(3, 30)
                else:
                    p, n = rng.choice([F(65), F(85)]), 20 * rng.randint(5, 45)
                it = pct_item(qid, p, n)
                if it['key'].denominator != 1:
                    continue
                opts = pct_options(it)
            it['difficulty'] = DIFF[block]
            item, row = finish(it, opts)
            # no drawn decimal shows the key between its own times-ten and over-ten (a giveaway)
            vals = {v for v, _ in opts}
            assert not (it['key'] * 10 in vals and it['key'] / 10 in vals)
            # nor between two slips of the same size either side of it (7.12, 8.12, 9.12)
            assert not any(u != v and it['key'] - u == v - it['key'] for u in vals for v in vals)
            return item, row
        except (AssertionError, TypeError):
            continue
    raise SystemExit(f'no valid draw for {qid}')


def worked(qid):
    """the brief's four worked items, as written"""
    if qid == 'q10-decimal':
        it = decimal_mul(qid, F(4, 10), 35)
        # the brief's 1.4 (point moved down) is replaced by a slipped digit, so 14 is not the middle of 1.4, 14, 140
        opts = [(F(15), ('slip', 0)), (F(140), 'point-up'), (F(35) / F(4, 10), 'reverse-yx')]
        assert [num(v) for v, _ in opts] == ['15', '140', '87.5'] and it['key'] == 14
        assert F(4, 10) * 30 + F(4, 10) * 5 == 12 + 2 == 14
    elif qid == 'q65-fraction':
        it = fraction_item(qid, 5, 6, 3, 8, '+', 0)
        opts = frac_options(it)
        assert [ftex(v) for v, _ in opts] == ['\\tfrac{4}{7}', '\\tfrac{11}{24}', '1'] and it['key'] == F(29, 24)
        assert F(20, 24) + F(9, 24) == F(5 * 8 + 3 * 6, 48) == F(29, 24)
    elif qid == 'q70-percent':
        it = pct_item(qid, 35, 260)
        opts = pct_options(it, point='down')
        assert [num(v) for v, _ in opts] == ['169', '78', '9.1'] and it['key'] == 91
        assert 26 * 3 + 13 == 91
    elif qid == 'q75-decimal':
        it = decimal_div(qid, F(36, 10), F(12, 100))
        # the brief's 3 (point moved down) is replaced by a slipped digit, so 30 is not the middle of 3, 30, 300
        opts = [(F(31), ('slip', 0)), (F(300), 'point-up'), (F(36, 10) * F(12, 100), 'reverse')]
        assert [num(v) for v, _ in opts] == ['31', '300', '0.432'] and it['key'] == 30
        assert F(12, 100) * 30 == F(36, 10) and F(360, 12) == 30
    it['difficulty'] = 4 if qid != 'q10-decimal' else 2
    vals = {v for v, _ in opts}
    assert not (it['key'] * 10 in vals and it['key'] / 10 in vals)  # no times-ten triple around the key
    assert not any(u != v and it['key'] - u == v - it['key'] for u in vals for v in vals)
    return finish(it, opts)


WORKED = {10: 'q10-decimal', 65: 'q65-fraction', 70: 'q70-percent', 75: 'q75-decimal'}
items, table = [], []
for g in range(16):
    block = 'ABCD'[g // 4]
    slot = g % 4
    items.append({"generator": "arith", "mix": GEN[block], "n": 4, "options": 4, "difficulty": DIFF[block], "skills": ["mp-speed"]})
    Q = 5 * (g + 1)
    kind = KINDS[block][slot]
    qid = f"q{Q:02d}-{NAME[kind]}"
    if Q in WORKED:
        assert WORKED[Q] == qid, (Q, qid)
        item, row = worked(qid)
    else:
        same_kind_slot = [i for i, k in enumerate(KINDS[block][:slot + 1]) if k == kind]
        item, row = draw(block, len(same_kind_slot) - 1, kind, qid)
    assert item['difficulty'] == DIFF[block]
    items.append(item)
    table.append((Q, block) + row)

assert len(items) == 32 and sum(4 if 'generator' in i else 1 for i in items) == 80
counts = {}
for i in items:
    if 'tags' in i:
        counts[i['tags'][0]] = counts.get(i['tags'][0], 0) + 1
assert counts == {'arith-decimal': 6, 'arith-fraction': 5, 'arith-percent': 5}, counts

exam = {
    "id": "mock-oa-arith",
    "name": "Arithmetic sprint: 80 in 8",
    "style": "trader",
    "models": ("Reported, as of Nov 2026: Optiver's 80 in 8. "
               "Eighty four-option arithmetic questions in 8 minutes; +1 right, −1 wrong, no skipping, no calculator."),
    "description": ("This is the reported format of Optiver's 80 in 8 test, as candidates described it by Nov 2026. "
                    "You have 80 arithmetic questions in 8 minutes, each with four options. "
                    "A right answer scores +1 and a wrong one −1. You cannot skip or go back. "
                    "Use no calculator; reports differ on scrap paper, so use none if you can. "
                    "Most questions are generated afresh each time you sit. "
                    "The pass mark here is 55 net, inside the reported band of 50 to 60."),
    "skills": {"mp-speed": "Speed arithmetic", "mp-fractions": "Fractions and percentages at speed"},
    "parts": [
        {"kind": "paper", "id": "sprint", "name": "80 in 8", "minutes": 8,
         "scoring": {"right": 1, "wrong": -1, "blank": 0}, "passNet": 55, "navigation": "forward", "skip": False,
         "items": items},
        {"kind": "check", "id": "no-calculator", "name": "I used no calculator",
         "detail": "Tick this only if you sat the whole paper without one."},
    ],
}
assert len(exam['models']) <= 200
with open(OUT, 'w') as fh:
    json.dump(exam, fh, ensure_ascii=False, indent=2)
    fh.write('\n')

print(f"wrote {OUT}: {len(items)} entries, 80 questions, seed {SEED}")
for Q, block, qid, plain, key, ds in table:
    print(f"Q{Q:<3}{block} {qid:<14} {plain:<14} key {key:<16} " + '; '.join(f"{t} ({k})" for t, k in ds))
```

## Helper: `gencheck.mjs`

```javascript
// Expands mock-oa-arith with the engine's own arith.js for a seed and checks every generated key a second way.
import fs from 'fs'; import vm from 'vm';
const APP = '/home/user/zero-to-quant/app';
const ctx = { window: {}, fetch: () => Promise.reject(new Error('no fetch')), console };
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(APP + '/js/engine/arith.js', 'utf8'), ctx);
const A = ctx.window.ZQ.arith;
await A.ready;
const exam = JSON.parse(fs.readFileSync(APP + '/content/exams/mock-oa-arith.json', 'utf8'));
const seed = process.argv[2] || '1';
const items = A.expand(exam.parts[0].items, seed, 0);
let bad = 0;
items.forEach((it, i) => {
  const q = i + 1;
  if (!it.generated) return;
  const m = it.title.match(/^(\d+) (\+|-|×|÷) (\d+)$/);
  const [a, op, b] = [+m[1], m[2], +m[3]];
  const key = it.widget.options.find(o => o.correct).text.replace(/\$/g, '');
  // second method: the inverse operation must give back the first number
  const k = +key;
  const ok = op === '+' ? k - b === a : op === '-' ? k + b === a : op === '×' ? k / b === a : k * b === a;
  const opts = it.widget.options.map(o => o.text.replace(/\$/g, ''));
  if (!ok || new Set(opts).size !== 4 || opts.filter(o => o === key).length !== 1) { bad++; console.log('BAD', q, it.title, opts); }
  if ([2, 61, 63].includes(q)) console.log(`Q${q}: ${it.title} = ${key}; options ${opts.join(', ')}`);
});
console.log(`seed ${seed}: ${items.length} items, ${items.filter(i => i.generated).length} generated, ${bad} bad`);
```
