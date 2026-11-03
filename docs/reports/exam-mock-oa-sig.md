# Report: mock exam `mock-oa-sig` (versions 1, 2 and 3)

Brief: `docs/briefs/mocks.md`, preamble and section `## mock-oa-sig`. Script and screenshots: `/tmp/claude-0/-home-user-zero-to-quant/99d9b168-d1f8-545f-868f-7528f8ba6677/scratchpad/mock-oa-sig/` (the orchestrator named this folder in place of the brief's `exam-<id>/`).

## Files

- `app/content/exams/mock-oa-sig.json` (id `mock-oa-sig`, name "Quantitative evaluation"), `mock-oa-sig-2.json` ("Quantitative evaluation, version 2") and `mock-oa-sig-3.json` ("..., version 3"). All three written by `gen_sig.py`.
- Shape (each): `id`, `name`, `style: trader`, `models` (174 characters), `description` (the brief's text, ending "version n of 3"), `skills` (the five from the brief), then one paper `quant` "Quantitative evaluation": `minutes: 60`, `scoring` +1 / 0 / 0, `passNet: 11`, free navigation (no `navigation` or `skip` key). No check part.
- Every item: `id` `qNN-<family>`, `difficulty`, `skills` (one), `tags` (the family), `pace`, `title`, `question`, `widget`, `feedback` (`correct`, `generic`, `byKey` on numerics), `explain.text`. Choices have four options, `layout: grid`, `shuffle: true`, a `why` on every distractor. Numerics ask for three decimal places, `tol: { abs: 0.005 }`, with named `wrong` values (each `tol` 0.005).
- `content/prep.json` already names `mock-oa-sig` (lines 33 and 418); it was not edited, and versions 2 and 3 are not in it.

## Item counts (identical in the three versions)

| Pos | Diff | Family | Skill | Widget | Pace |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | dice-ev | pz-expectation | choice | 90 |
| 2 | 2 | linearity | pz-expectation | choice | 90 |
| 3 | 2 | ev-fee | pz-expectation | choice | 90 |
| 4 | 2 | indicator | pz-expectation | choice | 90 |
| 5 | 3 | at-least-one | pz-conditioning | numeric | 180 |
| 6 | 3 | cards-conditional | pz-conditioning | choice | 180 |
| 7 | 3 | binomial | pz-conditioning | choice | 180 |
| 8 | 3 | weighing | bz-search | choice | 180 |
| 9 | 3 | bayes | pz-conditioning | numeric | 180 |
| 10 | 4 | waiting-time | pz-recursion | choice | 240 |
| 11 | 4 | stopping | pz-recursion | choice | 240 |
| 12 | 4 | max-of-draws | pz-expectation | numeric | 240 |
| 13 | 4 | bayes-multi | pz-conditioning | choice | 240 |
| 14 | 4 | bayes-multi | pz-conditioning | numeric | 240 |
| 15 | 4 | ruin-fair | pz-games | choice | 240 |
| 16 | 5 | ruin-biased | pz-games | numeric | 360 |
| 17 | 5 | bayes-ruin | pz-games | numeric | 360 |

Difficulty 4 at 2, 5 at 3, 6 at 4, 2 at 5 (asserted per version). Pace sums to 3420 s, 57 minutes (asserted). Widgets: 11 choice, 6 numeric. Skills: pz-expectation 5, pz-conditioning 6, pz-recursion 2, pz-games 3, bz-search 1 (the results page's by-skill chart shows the same counts).

## Validator, voice and playthrough

- `node tools/validate.mjs 2>&1 | tail -5`: `0 errors, 434 warnings`; no warning names a `mock-oa-sig` file (the warnings are other courses' unwritten lessons).
- `VOICE_BASE=/home/user/zero-to-quant/app/content/exams/ python3 docs/reviews/voice-scan.py`: no line names a `mock-oa-sig` file, so 0 sentences over 20 words and 0 explanations over three sentences. The brief's `models` line is one 26-word sentence, so it now reads "Reported, as of Nov 2026: SIG's Quantitative Evaluation. Seventeen questions in 60 minutes with a calculator, rising from quick expected values to multi-stage Bayes and ruin." `grep` finds no `!` and no em-dash.
- `node tools/playthrough.mjs --exam <id> --local-cdn <pkgs>`: for each of `mock-oa-sig`, `mock-oa-sig-2`, `mock-oa-sig-3`: `ok 17 items, scored 17 of 17, passed` and `ok (mock checks) seed, clock at zero, attempts kept`. All passed.
- The same with `--mobile` (and once with `--why --shots`): all passed for the three files.
- Firm name: "SIG" appears only in `models` and `description`, each with "reported" and "Nov 2026" (a JSON check confirms it is absent from `parts`).

Screenshots looked at (1280 and 390 px): the start card, a fraction choice (Q2, Q6), a money choice (Q11), a whole-number choice (Q8), numerics (Q9, Q16, Q17), the results page and its worked explanations. The start card shows the description, "Models ...", "60 minutes", "17 questions" and the engine's rule "Pass mark 11 net". Options fit in a two-by-two grid at 390 px with nothing overlapping. One content fault was fixed: Q17's question first held `$\tfrac34$` inline, which drew at about 70% of the prose size; Q16 and Q17 questions now say "three in four" and "two in three" (0.55 and 0.6 stay decimals). Engine faults are in the backlog bullets: on the 390 px results page the PASS stamp overlaps "of 17", and at 1280 px the long description pushes the rules list under the card's sticky footer.

## Keys and the two computations

Method 1 is the closed form in `Fraction`s. Method 2 is independent: enumeration over dice, cards or coin sequences, a dynamic programme, a linear solve, a policy search, a recursive search or natural frequencies. `note()` raises unless both equal the key.

| Pos | Method 1 | Method 2 |
| --- | --- | --- |
| 1 | $\frac{(n+1)(2n+1)}{6}$ | sum of the squares over $n$; also asserts $Var + \text{mean}^2$ |
| 2 | $k \cdot \frac{c}{52}$ | hypergeometric sum $\sum j \binom{c}{j}\binom{52-c}{k-j} / \binom{52}{k}$ |
| 3 | $\frac{\text{sum of paying faces}}{6} - c$ | enumeration over the six faces; also $\frac12 \times$ mean paying face $- c$ |
| 4 | $\frac{n-1}{4}$ | exact distribution of the count by a DP over (last toss, count) |
| 5 | $1 - (5/6)^n$ | enumeration of all $6^n$ rolls |
| 6 | $\binom{c}{2} / (\binom{52}{2} - \binom{52-c}{2})$ | enumeration of all ordered pairs of distinct cards |
| 7 | $\binom{n}{k} / 2^n$ | enumeration of all $2^n$ sequences |
| 8 | least $k$ with $3^k \ge N$ | recursive minimax over every first split $(a, a, N - 2a)$ |
| 9 | $\frac{bs}{bs + (1-b)f}$ | integer counts in 10,000 people |
| 10 | overlap sum $\sum 2^j$ over self-overlaps | linear solve over prefix states |
| 11 | backward induction | brute force over every keep-set per stage (and a joint search for two rerolls) |
| 12 | $\sum k(2k-1)/n^2$ or $\sum (n-k+1)^2/n^2$ | enumeration of all $n^2$ pairs; also $E[\max] + E[\min] = n + 1$ |
| 13 | $\frac{\text{prior}}{\text{prior} + (1-\text{prior})2^{-k}}$ | enumeration over coins and every toss sequence; also odds form |
| 14 | odds $\frac{b}{1-b}(s/f)^2$ | integer counts in 1,000,000 people; also the direct formula |
| 15 | $i(N - i)$ | linear solve of $D_k = 1 + \frac12(D_{k-1} + D_{k+1})$ |
| 16 | $\frac{1 - r^i}{1 - r^N}$ | shooting from $P_0 = 0$, scaled to $P_N = 1$; also a linear solve |
| 17 | closed-form ruin values, then Bayes | ruin values by linear solve, then Bayes |

Version 1 matches every key in the brief: $\frac{91}{6}$, $\frac54$, $-1$, $\frac94$, $\frac{671}{1296}$, $\frac{1}{33}$, $\frac{5}{16}$, 3, $\frac{19}{118}$, 6, 4.25, $\frac{161}{36}$, $\frac{8}{11}$, $\frac{361}{460}$, 21, $\frac{135}{211}$, $\frac{27}{40}$. Every row of the key table below (all three versions) is the script's output after both methods agreed.

## Option rules (asserted for every choice in every version)

Four distinct values and distinct display strings; no two values within 0.01; the key never between a times-ten pair; the key never between two equally spaced slips. Numeric `wrong` values sit more than 0.01 from the key (twice the tolerance) and more than 0.01 from each other. A draw for versions 2 and 3 that breaks a rule is rejected and the next candidate taken. Two draws were rejected: version 3 pos 3 ($c = 2$, even: −£2 and +£2 around a key of £0) and version 3 pos 9 (5%, 90%, 10%: its two-test key $\frac{81}{100}$ equals the hit rate squared, 0.81).

## Departures from the brief, for the orchestrator

- **Pos 3 distractors (all versions).** The brief's version 1 set (+£1.00, +£0.50, −£3.00 around −£1.00) puts the key between two equal slips, −£3 and +£1. The "paying faces only" slip (+£1.00) is replaced by +£2.00, "you found the expected payout and forgot the fee". Version 1 is now −£1.00, −£3.00, +£0.50, +£2.00.
- **Pos 11, version 1.** £3.50 and £5.00 sit 75p either side of £4.25. £5.00 is replaced by £4.47, "you took the larger of the two rolls" ($\frac{161}{36}$). The set is £4.25, £3.50, £4.17, £4.47. With two rerolls the threshold slip becomes "you valued the game with one reroll".
- **Pos 9, all versions: the "true positives over everyone" wrong value is not listed.** It is $b \cdot s$, which at three decimal places reads as the base rate $b$ (0.0095 against 0.01 in version 1), so the two wrong ranges overlap. Only the base rate is listed; the `why` text for the joint slip is dropped with it.
- **Pos 6 pool.** King gives the same item and key as ace ($\frac{1}{33}$), so the pool is ace, heart and picture card (jack, queen or king), key $\frac{11}{91}$.
- **Pos 7 pool.** $(5, 2)$ has key $\frac{10}{32} = \frac{5}{16}$, version 1's key, so the pool is $(6, 3)$, $(7, 2)$, $(8, 4)$.
- **Pos 13, $k = 4$.** "One minus a fair coin's chance" ($\frac{15}{16}$) is within 0.01 of the equal-priors slip ($\frac{16}{17}$). For $k = 4$ the third distractor is "you found the chance of 4 heads, not of the coin" (the marginal $P(\text{4 heads})$). Version 1 ($k = 3$) keeps the brief's $\frac78$.
- **Distractors the brief left open,** each with its slip: pos 2 one card, the complement, suit and rank mixed up; pos 4 $n$ places, chance $\frac12$, separate pairs; pos 6 the first card given, the unconditional chance, one card; pos 7 one order, the share $k/n$, at least $k$; pos 8 halving, one pair at a time ($N/2$), one coin against each other ($N - 2$); pos 10 one over the chance, the previous wait plus one, and per pattern the shortest wait (HH), every prefix an overlap (HTH), $2^{k+1}$ without the $-2$ (HHH); pos 12 one die, the other extreme, doubles left out.
- **Seeds.** Each position of version $v$ draws with `random.Random(SEED_v * 100 + pos)` (SEED 1702 and 1703), so the draw at one position does not shift the others when a rule rejects a candidate. Version 1 is the brief's `FIXED` set.
- **Pos 14** takes pos 9's parameters in the same version, as the brief says. A draw at pos 9 must suit both items.
- **`models`** split into two sentences (above).

## Version 2 and 3 parameters (no repeat of an earlier version at any position)

| Pos | Version 1 | Version 2 | Version 3 |
| --- | --- | --- | --- |
| 1 | $n = 6$ | $n = 4$ | $n = 8$ |
| 2 | 5 cards, hearts | 13 cards, aces | 5 cards, aces |
| 3 | £3, even | £3, 4 or more | £4, even |
| 4 | 10 tosses | 21 tosses | 13 tosses |
| 5 | 4 rolls | 3 rolls | 5 rolls |
| 6 | aces | picture cards | hearts |
| 7 | (6, 3) | (7, 2) | (8, 4) |
| 8 | 10 coins | 28 coins | 80 coins |
| 9, 14 | 1%, 95%, 5% | 1%, 90%, 10% | 2%, 95%, 5% |
| 10 | HH | HTH | HHH |
| 11 | 1 reroll, 6 faces | 2 rerolls, 6 faces | 1 reroll, 8 faces |
| 12 | max, 6 faces | min, 6 faces | max, 8 faces |
| 13 | 3 fair, 3 heads | 3 fair, 4 heads | 4 fair, 4 heads |
| 15 | £3 to £10 | £2 to £8 | £4 to £9 |
| 16 | 0.6, £2 to £5 | 0.55, £3 to £6 | $\frac23$, £2 to £5 |
| 17 | $\frac34$ | $\frac23$ | 0.6 |

The script asserts that the three parameter sets differ at every position. Two keys repeat across versions without a repeated item: pos 8 is 4 for both 28 and 80 coins, and pos 9's $s$ or $b$ recurs with a different set.

## Prerequisites (cited; nothing is gated)

puzzles `l1-dice-games`, `l3-waiting-for-hh`, `l4-indicator-tricks`, `l6-when-to-stop`, `l7-cards-and-colours`, `l9-bayes-in-a-minute`, `l10-ruin-in-interviews`, `l11-largest-of-several`, `l24-mixed-set`; brainteasers `l4-weighing-coins`; mental-pressure `l15-probability-at-speed`.

## Proposed changes

- No `course.json` change. No `prep.json` change made: it already names `mock-oa-sig`. The brief proposes adding versions 2 and 3 to the firm path; the orchestrator's instruction keeps them out, so they are reached only from Review's "Mock assessments" list.
- The brief's pos 3 and pos 11 worked distractors, the pos 6 and pos 7 pools and the pos 9 `wrong` list could be updated to match the files (above).

## Script: `gen_sig.py` and its output

Run: `python3 gen_sig.py [outdir]` (default `app/content/exams`). Standard library only (`fractions`, `itertools`, `math`, `random`, `json`).

Output:

```text
wrote app/content/exams/mock-oa-sig.json: 17 items
wrote app/content/exams/mock-oa-sig-2.json: 17 items
wrote app/content/exams/mock-oa-sig-3.json: 17 items
v1 Q1  n=6                    key 91/6      = 15.1667   £12.25 mean squared; £3.50 face; £91.00 no divide
v1 Q2  k=5, hearts            key 5/4       = 1.2500   1/4 one card; 15/4 complement; 5/13 suit-rank mix-up
v1 Q3  c=3, even              key -1        = -1.0000   -3 fee only; 1/2 every roll; 2 no fee
v1 Q4  n=10                   key 9/4       = 2.2500   5/2 n places; 9/2 chance 1/2; 5/4 separate pairs
v1 Q5  n=4                    key 671/1296  = 0.5177   0.667 n/6; 0.482 complement; 0.167 one roll
v1 Q6  aces                   key 1/33      = 0.0303   1/17 first card given; 1/221 unconditional; 1/13 one card
v1 Q7  n=6, k=3               key 5/16      = 0.3125   1/64 one order; 1/2 share; 21/32 at least k
v1 Q8  N=10                   key 3         = 3.0000   4 halving; 5 pairs; 8 one against each
v1 Q9  b=1%, s=95%, f=5%      key 19/118    = 0.1610   0.950 hit rate; 0.009 TP over all; 0.010 base
v1 Q14 b=1%, s=95%, f=5%      key 361/460   = 0.7848   0.161 one test; 0.902 hit rate squared
v1 Q10 HH                     key 6         = 6.0000   4 one over chance; 3 previous wait plus one; 2 HH-specific
v1 Q11 r=1, 6 faces           key 17/4      = 4.2500   £3.50 never reroll; £4.17 slip; £4.47 max of rolls
v1 Q12 max, 6 faces           key 161/36    = 4.4722   3.500 one die; 2.528 other extreme; 4.667 no doubles
v1 Q13 m=3, k=3               key 8/11      = 0.7273   1/4 prior; 8/9 equal priors; 7/8 third
v1 Q15 i=3, N=10              key 21        = 21.0000   7 N-i; 30 iN; 49 squared distance
v1 Q16 p=3/5, i=2, N=5        key 135/211   = 0.6398   0.400 fair i/N; 0.216 streak; 0.600 one bet
v1 Q17 p=3/4                  key 27/40     = 0.6750   0.513 P(reach); 0.692 biased P(reach); 0.500 prior
v2 Q1  n=4                    key 15/2      = 7.5000   £6.25 mean squared; £2.50 face; £30.00 no divide
v2 Q2  k=13, aces             key 1         = 1.0000   1/13 one card; 12 complement; 13/4 suit-rank mix-up
v2 Q3  c=3, 4 or more         key -1/2      = -0.5000   -3 fee only; 1/2 every roll; 5/2 no fee
v2 Q4  n=21                   key 5         = 5.0000   21/4 n places; 10 chance 1/2; 5/2 separate pairs
v2 Q5  n=3                    key 91/216    = 0.4213   0.500 n/6; 0.579 complement; 0.167 one roll
v2 Q6  picture cards          key 11/91     = 0.1209   11/51 first card given; 11/221 unconditional; 3/13 one card
v2 Q7  n=7, k=2               key 21/128    = 0.1641   1/128 one order; 2/7 share; 15/16 at least k
v2 Q8  N=28                   key 4         = 4.0000   5 halving; 14 pairs; 26 one against each
v2 Q9  b=1%, s=90%, f=10%     key 1/12      = 0.0833   0.900 hit rate; 0.009 TP over all; 0.010 base
v2 Q14 b=1%, s=90%, f=10%     key 9/20      = 0.4500   0.083 one test; 0.810 hit rate squared
v2 Q10 HTH                    key 10        = 10.0000   8 one over chance; 5 previous wait plus one; 14 HTH-specific
v2 Q11 r=2, 6 faces           key 14/3      = 4.6667   £3.50 never reroll; £4.25 slip; £4.96 max of rolls
v2 Q12 min, 6 faces           key 91/36     = 2.5278   3.500 one die; 4.472 other extreme; 2.333 no doubles
v2 Q13 m=3, k=4               key 16/19     = 0.8421   1/4 prior; 16/17 equal priors; 19/64 third
v2 Q15 i=2, N=8               key 12        = 12.0000   6 N-i; 16 iN; 36 squared distance
v2 Q16 p=11/20, i=3, N=6      key 1331/2060 = 0.6461   0.500 fair i/N; 0.166 streak; 0.550 one bet
v2 Q17 p=2/3                  key 12/19     = 0.6316   0.452 P(reach); 0.571 biased P(reach); 0.500 prior
v3 Q1  n=8                    key 51/2      = 25.5000   £20.25 mean squared; £4.50 face; £204.00 no divide
v3 Q2  k=5, aces              key 5/13      = 0.3846   1/13 one card; 60/13 complement; 5/4 suit-rank mix-up
v3 Q3  c=4, even              key -2        = -2.0000   -4 fee only; -1/2 every roll; 2 no fee
v3 Q4  n=13                   key 3         = 3.0000   13/4 n places; 6 chance 1/2; 3/2 separate pairs
v3 Q5  n=5                    key 4651/7776 = 0.5981   0.833 n/6; 0.402 complement; 0.167 one roll
v3 Q6  hearts                 key 2/15      = 0.1333   4/17 first card given; 1/17 unconditional; 1/4 one card
v3 Q7  n=8, k=4               key 35/128    = 0.2734   1/256 one order; 1/2 share; 163/256 at least k
v3 Q8  N=80                   key 4         = 4.0000   7 halving; 40 pairs; 78 one against each
v3 Q9  b=2%, s=95%, f=5%      key 19/68     = 0.2794   0.950 hit rate; 0.019 TP over all; 0.020 base
v3 Q14 b=2%, s=95%, f=5%      key 361/410   = 0.8805   0.279 one test; 0.902 hit rate squared
v3 Q10 HHH                    key 14        = 14.0000   8 one over chance; 7 previous wait plus one; 16 HHH-specific
v3 Q11 r=1, 8 faces           key 11/2      = 5.5000   £4.50 never reroll; £5.44 slip; £5.81 max of rolls
v3 Q12 max, 8 faces           key 93/16     = 5.8125   4.500 one die; 3.188 other extreme; 6.000 no doubles
v3 Q13 m=4, k=4               key 4/5       = 0.8000   1/5 prior; 16/17 equal priors; 1/4 third
v3 Q15 i=4, N=9               key 20        = 20.0000   5 N-i; 36 iN; 25 squared distance
v3 Q16 p=2/3, i=2, N=5        key 24/31     = 0.7742   0.400 fair i/N; 0.296 streak; 0.667 one bet
v3 Q17 p=3/5                  key 27/46     = 0.5870   0.404 P(reach); 0.474 biased P(reach); 0.500 prior
dropped wrong (reads as another slip at 3 dp) (1, 9, 'joint', Fraction(19, 2000))
dropped wrong (reads as another slip at 3 dp) (2, 9, 'joint', Fraction(9, 1000))
dropped wrong (reads as another slip at 3 dp) (3, 9, 'joint', Fraction(19, 1000))
rejected (3, 3, (2, 'even'), "('equal slips', Fraction(-2, 1), Fraction(0, 1), Fraction(2, 1))")
rejected (3, 9, (5, 90, 10), "('wrong near key', Fraction(81, 100), Fraction(81, 100))")
```

```python
#!/usr/bin/env python3
"""gen_sig.py: writes app/content/exams/mock-oa-sig.json, mock-oa-sig-2.json and mock-oa-sig-3.json.

Brief: docs/briefs/mocks.md, section mock-oa-sig. Seventeen positions, the same family, skill, widget and
difficulty in every version. Version 1 uses the brief's worked parameters (FIXED). Versions 2 and 3 draw from each
position's pool with random.Random(1702) and random.Random(1703), never repeating an earlier version's parameters,
and reject a draw whose options break the option rules (rejection is deterministic, so the files are reproducible).

Every number is a Fraction. Each key is computed by a closed form and by a second method (enumeration over dice,
cards and coin sequences, a linear solve, a policy search, a recursive search or natural frequencies) with assert.
Option rules asserted on every choice: four distinct values and display strings, no two within 0.01, the key not
between a times-ten pair, the key not between two equally spaced slips. Numeric wrong values sit more than 0.01
from the key (twice the tolerance), so a wrong range never touches the key's range.
Usage: python3 gen_sig.py [outdir]
"""
import json
import math
import random
import sys
from fractions import Fraction as F
from itertools import combinations, permutations, product

OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/user/zero-to-quant/app/content/exams'
SEEDS = {1: 1701, 2: 1702, 3: 1703}
PACE = {2: 90, 3: 180, 4: 240, 5: 360}
TOL = 0.005

# ---------- helpers ----------

def solve(A, b):
    """Gaussian elimination over Fractions."""
    n = len(A)
    M = [list(map(F, A[i])) + [F(b[i])] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def dfrac(x):
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    s = '-' if x < 0 else ''
    return f'{s}\\dfrac{{{abs(x.numerator)}}}{{{x.denominator}}}'


def tfrac(x):
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    s = '-' if x < 0 else ''
    return f'{s}\\tfrac{{{abs(x.numerator)}}}{{{x.denominator}}}'


def money(x, sign=False):
    v = float(x)
    r = round(abs(v) + 1e-12, 2)
    if v < -1e-12:
        return f'−£{r:.2f}'
    return (f'+£{r:.2f}' if sign and v > 1e-12 else f'£{r:.2f}')


def dec(x, places=None):
    v = float(x)
    if places is not None:
        return f'{v:.{places}f}'
    s = f'{v:.4f}'.rstrip('0').rstrip('.')
    assert F(s) == F(x), (s, x)  # only exact short decimals use this
    return s


def sfrac(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f'{x.numerator}/{x.denominator}'


def eq(a, b):
    """'a = b' unless the two strings are the same."""
    return a if a == b else f'{a} = {b}'


def mnum(n):
    """A whole number inside KaTeX, with a thin-space-free thousands comma."""
    return f'{n:,}'.replace(',', '{,}')


def d3(x):
    return f'{float(x):.3f}'


def check_choice(key, slips, shown):
    """key: Fraction; slips: list of Fractions; shown: list of display strings, key first."""
    vals = [F(key)] + [F(s) for s in slips]
    assert len(vals) == 4 and len(set(vals)) == 4, vals
    assert len(set(shown)) == 4, shown
    for a, b in combinations(vals, 2):
        assert abs(float(a) - float(b)) > 0.01 + 1e-12, ('too close', a, b)
    for a in slips:
        for b in slips:
            if a != b and a > 0 and b == 10 * a and a < key < b:
                raise AssertionError(('times-ten pair', a, key, b))
            if a < key < b and key - a == b - key:
                raise AssertionError(('equal slips', a, key, b))


def check_numeric(key, wrongs):
    for w in wrongs:
        assert abs(float(w) - float(key)) > 2 * TOL + 1e-12, ('wrong near key', w, key)
    for a, b in combinations(wrongs, 2):
        assert abs(float(a) - float(b)) > 2 * TOL, ('wrongs overlap', a, b)


def choice(options):
    """options: list of (id, text, why or None for the key)."""
    out = []
    for oid, text, why in options:
        o = {'id': oid, 'text': text}
        if why is None:
            o['correct'] = True
        else:
            o['why'] = why
        out.append(o)
    return {'kind': 'choice', 'layout': 'grid', 'shuffle': True, 'label': 'Answer options', 'options': out}


def numeric(key, wrongs, accept, label):
    return {'kind': 'numeric', 'answer': round(float(key), 6), 'tol': {'abs': TOL},
            'placeholder': 'three decimal places', 'label': label, 'accept': accept,
            'wrong': [{'id': wid, 'value': round(float(v), 6), 'tol': {'abs': TOL}} for wid, v in wrongs]}


KEYS = []  # rows for the report
DROPPED = []


def note(v, pos, params, key, m1, m2, slips):
    if not (m1 == m2 == key):
        raise RuntimeError((pos, params, key, m1, m2))
    KEYS.append((v, pos, params, key, slips))

# ---------- positions ----------
# Each builder takes the parameters and returns (item without id, option-rule check passes or raises).


def p1(n):
    faces = range(1, n + 1)
    m1 = F((n + 1) * (2 * n + 1), 6)
    m2 = sum(F(k * k) for k in faces) / n
    var, mean = F(n * n - 1, 12), F(n + 1, 2)
    assert var + mean ** 2 == m2
    key = m1
    sq_mean, mean_only, no_div = mean ** 2, mean, sum(F(k * k) for k in faces)
    check_choice(key, [sq_mean, mean_only, no_div], [money(x) for x in (key, sq_mean, mean_only, no_div)])
    top = n * n
    item = {
        'question': f'A fair {n}-sided die, faces 1 to {n}, pays £ the square of the face shown. What is a fair price to play once?',
        'widget': choice([
            ('a', money(key), None),
            ('b', money(sq_mean), f'You squared the average face, ${dec(mean)}^2$, instead of averaging the squares.'),
            ('c', money(mean_only), 'You priced the face itself, not its square.'),
            ('d', money(no_div), f'You added the squares but did not divide by {n}.')]),
        'feedback': {'correct': f'The mean of the squares is ${tfrac(key)}$, about {money(key)}.',
                     'generic': 'Average the squares of the faces, not the square of the average face.'},
        'explain': {'text': f'$E[X^2] = \\tfrac{{1 + 4 + \\dots + {top}}}{{{n}}} = {tfrac(key)} \\approx {float(key):.2f}$. '
                            f'Check: $Var(X) + E[X]^2 = {tfrac(var)} + {tfrac(mean ** 2)} = {tfrac(key)}$.'}}
    note(V, 1, f'n={n}', key, m1, m2, f'{money(sq_mean)} mean squared; {money(mean_only)} face; {money(no_div)} no divide')
    return item


def p2(k, kind):
    c = 13 if kind == 'heart' else 4
    word, words = ('heart', 'hearts') if kind == 'heart' else ('ace', 'aces')
    m1 = F(k * c, 52)
    m2 = sum(F(j * math.comb(c, j) * math.comb(52 - c, k - j), math.comb(52, k)) for j in range(0, min(c, k) + 1))
    key = m1
    one, comp = F(c, 52), k - key
    mix = F(k, 13) if kind == 'heart' else F(k, 4)
    check_choice(key, [one, comp, mix], [dfrac(x) for x in (key, one, comp, mix)])
    mixwhy = ('You used the share of one rank, 1 in 13, instead of one suit, 1 in 4.' if kind == 'heart'
              else 'You used the share of one suit, 1 in 4, instead of one rank, 1 in 13.')
    item = {
        'question': f'You deal {k} cards from a well-shuffled 52-card deck. What is the expected number of {words} among them?',
        'widget': choice([
            ('a', f'${dfrac(key)}$', None),
            ('b', f'${dfrac(one)}$', f'You gave the chance for one card, not the count over all {k}.'),
            ('c', f'${dfrac(comp)}$', f'You counted the cards that are not {words}.'),
            ('d', f'${dfrac(mix)}$', mixwhy)]),
        'feedback': {'correct': f'Each card is {"a" if kind == "heart" else "an"} {word} with chance ${tfrac(F(c, 52))}$, so ${k} \\times {tfrac(F(c, 52))} = {tfrac(key)}$.',
                     'generic': f'Give each card an indicator for being {"a" if kind == "heart" else "an"} {word}, then add the chances.'},
        'explain': {'text': f'Card $j$ is {"a" if kind == "heart" else "an"} {word} with chance $\\tfrac{{{c}}}{{52}} = {tfrac(F(c, 52))}$, whatever the other cards are. '
                            f'Linearity adds the {k} chances: ${tfrac(key)}$. '
                            'The cards are dependent, but an expectation does not care.'}}
    note(V, 2, f'k={k}, {words}', key, m1, m2, f'{one} one card; {comp} complement; {mix} suit-rank mix-up')
    return item


def p3(c, rule):
    pays = [2, 4, 6] if rule == 'even' else [4, 5, 6]
    m1 = F(sum(pays), 6) - c
    m2 = sum(F(x) if x in pays else F(0) for x in range(1, 7)) / 6 - c
    alt = F(1, 2) * F(sum(pays), 3) - c
    assert alt == m1
    key = m1
    # the brief's "averaged over the paying faces only" slip (+£1 in version 1) sits with -£3 as two equal slips
    # around the key, so the set is: fee only, paid on every roll, forgot the fee
    feeonly, every, nofee = F(-c), F(7, 2) - c, F(sum(pays), 6)
    check_choice(key, [feeonly, every, nofee], [money(x, True) for x in (key, feeonly, every, nofee)])
    cond = 'even' if rule == 'even' else '4 or more'
    item = {
        'question': f'You pay £{c} to roll a fair six-sided die. You receive £ the face if it is {cond}, and nothing otherwise. What is your expected profit per game?',
        'widget': choice([
            ('a', money(key, True), None),
            ('b', money(feeonly, True), 'You counted only the fee and left out the payout.'),
            ('c', money(every, True), f'You paid out the face on every roll: $3.5 - {c}$.'),
            ('d', money(nofee, True), f'You found the expected payout and forgot the £{c} fee.')]),
        'feedback': {'correct': f'The payout averages {money(nofee)}, so the profit is {money(key, True)} a game.',
                     'generic': 'Average the payout over all six faces, then take off the fee.'},
        'explain': {'text': f'$E[\\text{{payout}}] = \\tfrac{{{pays[0]} + {pays[1]} + {pays[2]}}}{{6}} = {dec(nofee)}$, so the profit is ${dec(nofee)} - {c} = {dec(key)}$. '
                            f'Check: half the rolls pay, averaging {dec(F(sum(pays), 3))}, so $\\tfrac12 \\times {dec(F(sum(pays), 3))} - {c} = {dec(key)}$.'}}
    note(V, 3, f'c={c}, {cond}', key, m1, m2, f'{feeonly} fee only; {every} every roll; {nofee} no fee')
    return item


def p4(n):
    m1 = F(n - 1, 4)
    # second method: exact distribution of the count by dynamic programming over (last toss, count)
    dist = {('H', 0): F(1, 2), ('T', 0): F(1, 2)}
    for _ in range(n - 1):
        nd = {}
        for (last, cnt), pr in dist.items():
            for t in 'HT':
                c2 = cnt + (1 if last == 'H' and t == 'H' else 0)
                nd[(t, c2)] = nd.get((t, c2), 0) + pr / 2
        dist = nd
    m2 = sum(c * p for (_, c), p in dist.items())
    key = m1
    nplaces, half, blocks = F(n, 4), F(n - 1, 2), F(n // 2, 4)
    check_choice(key, [nplaces, half, blocks], [dec(x) for x in (key, nplaces, half, blocks)])
    item = {
        'question': f'You toss a fair coin {n} times. Count each place where two heads stand side by side, overlaps included: HHH holds two. What is the expected count?',
        'widget': choice([
            ('a', f'${dec(key)}$', None),
            ('b', f'${dec(nplaces)}$', f'You counted {n} places for a pair, but {n} tosses have only {n - 1}.'),
            ('c', f'${dec(half)}$', 'You gave each place chance $\\tfrac12$, but both tosses must be heads.'),
            ('d', f'${dec(blocks)}$', 'You split the tosses into separate pairs and missed the overlapping ones.')]),
        'feedback': {'correct': f'There are {n - 1} places, each with chance $\\tfrac14$: ${n - 1} \\times \\tfrac14 = {eq(tfrac(key), dec(key))}$.',
                     'generic': 'Give each neighbouring pair of tosses an indicator, then add the chances.'},
        'explain': {'text': f'Indicator $I_j$ marks heads at tosses $j$ and $j + 1$, for $j = 1$ to ${n - 1}$. '
                            f'Each has $E[I_j] = \\tfrac14$, so the count averages ${eq(tfrac(key), dec(key))}$. '
                            'Overlapping pairs are dependent, but linearity does not care.'}}
    note(V, 4, f'n={n}', key, m1, m2, f'{nplaces} n places; {half} chance 1/2; {blocks} separate pairs')
    return item


def p5(n):
    m1 = 1 - F(5, 6) ** n
    m2 = F(sum(1 for r in product(range(1, 7), repeat=n) if 6 in r), 6 ** n)
    key = m1
    times, none, one = F(n, 6), F(5, 6) ** n, F(1, 6)
    check_numeric(key, [times, none, one])
    tot, no6 = 6 ** n, 5 ** n
    item = {
        'question': f'You roll a fair six-sided die {n} times. What is the chance of at least one six? Give three decimal places.',
        'widget': numeric(key, [('times', times), ('none', none), ('one', one)],
                          f'{key.numerator}/{key.denominator}, about {d3(key)} (within 0.005)', 'Chance of at least one six'),
        'feedback': {'correct': f'$1 - (\\tfrac56)^{n} = \\tfrac{{{key.numerator}}}{{{key.denominator}}} \\approx {d3(key)}$.',
                     'generic': 'Find the chance of no six at all, then take it from 1.',
                     'byKey': {'times': f'You added $\\tfrac16$ {n} times, which counts rolls with two sixes twice.',
                               'none': 'That is the chance of no six. Take it from 1.',
                               'one': 'That is the chance for a single roll.'}},
        'explain': {'text': f'No six in {n} rolls has chance $(\\tfrac56)^{n} = \\tfrac{{{no6}}}{{{tot}}}$. '
                            f'So at least one six has chance $\\tfrac{{{tot - no6}}}{{{tot}}} \\approx {d3(key)}$. '
                            f'Check: of the {tot:,} equally likely outcomes, {tot - no6:,} hold a six.'}}
    note(V, 5, f'n={n}', key, m1, m2, f'{d3(times)} n/6; {d3(none)} complement; {d3(one)} one roll')
    return item


DECK = [(r, s) for r in range(1, 14) for s in 'SHDC']


def p6(kind):
    if kind == 'ace':
        pred, c, word, a = (lambda cd: cd[0] == 1), 4, 'an ace', 'aces'
    elif kind == 'heart':
        pred, c, word, a = (lambda cd: cd[1] == 'H'), 13, 'a heart', 'hearts'
    else:
        pred, c, word, a = (lambda cd: cd[0] >= 11), 12, 'a picture card (jack, queen or king)', 'picture cards'
    both, none_ = math.comb(c, 2), math.comb(52 - c, 2)
    total = math.comb(52, 2)
    m1 = F(both, total - none_)
    pairs = [(x, y) for x, y in permutations(DECK, 2)]
    atl = [p for p in pairs if pred(p[0]) or pred(p[1])]
    m2 = F(sum(1 for p in atl if pred(p[0]) and pred(p[1])), len(atl))
    key = m1
    first, uncond, one = F(c - 1, 51), F(both, total), F(c, 52)
    check_choice(key, [first, uncond, one], [dfrac(x) for x in (key, first, uncond, one)])
    short = {'ace': 'an ace', 'heart': 'a heart', 'face': 'a picture card'}[kind]
    item = {
        'question': f'You draw two cards from a well-shuffled 52-card deck, without replacement. At least one is {word}. What is the chance that both are {a}?',
        'widget': choice([
            ('a', f'${dfrac(key)}$', None),
            ('b', f'${dfrac(first)}$', f'You took the first card as {short}, but "at least one" could be either card.'),
            ('c', f'${dfrac(uncond)}$', f'You found the chance of two {a} before using the condition.'),
            ('d', f'${dfrac(one)}$', f'You gave the chance that a single card is {short}.')]),
        'feedback': {'correct': f'{both} pairs of {a} out of {total - none_} pairs that hold one: ${tfrac(key)}$.',
                     'generic': f'Count unordered pairs: two {a}, over pairs with at least one.'},
        'explain': {'text': f'There are $\\binom{{52}}{{2}} = {mnum(total)}$ pairs, and $\\binom{{{52 - c}}}{{2}} = {mnum(none_)}$ hold no {a[:-1]}. '
                            f'So {total - none_} pairs hold at least one, and $\\binom{{{c}}}{{2}} = {both}$ hold two. '
                            f'The chance is $\\tfrac{{{both}}}{{{total - none_}}} = {tfrac(key)}$.'}}
    note(V, 6, a, key, m1, m2, f'{first} first card given; {uncond} unconditional; {one} one card')
    return item


def p7(n, k):
    m1 = F(math.comb(n, k), 2 ** n)
    m2 = F(sum(1 for s in product('HT', repeat=n) if s.count('H') == k), 2 ** n)
    key = m1
    order, share = F(1, 2 ** n), F(k, n)
    atleast = F(sum(math.comb(n, j) for j in range(k, n + 1)), 2 ** n)
    check_choice(key, [order, share, atleast], [dfrac(x) for x in (key, order, share, atleast)])
    seq = 'H' * k + 'T' * (n - k)
    item = {
        'question': f'You toss a fair coin {n} times. What is the chance of exactly {k} heads?',
        'widget': choice([
            ('a', f'${dfrac(key)}$', None),
            ('b', f'${dfrac(order)}$', f'You priced one order, such as {seq}, but there are $\\binom{{{n}}}{{{k}}} = {math.comb(n, k)}$ of them.'),
            ('c', f'${dfrac(share)}$', f'You gave the share of heads, ${k}$ in ${n}$, as a chance.'),
            ('d', f'${dfrac(atleast)}$', f'You found the chance of at least {k} heads.')]),
        'feedback': {'correct': f'$\\binom{{{n}}}{{{k}}} = {math.comb(n, k)}$ orders, each with chance $\\tfrac{{1}}{{{2 ** n}}}$: ${tfrac(key)}$.',
                     'generic': f'Count the orders with {k} heads, then multiply by the chance of one order.'},
        'explain': {'text': f'Each sequence of {n} tosses has chance $\\tfrac{{1}}{{{2 ** n}}}$. '
                            f'Exactly {k} heads happens in $\\binom{{{n}}}{{{k}}} = {math.comb(n, k)}$ of them, so the chance is ${eq(f'\\tfrac{{{math.comb(n, k)}}}{{{2 ** n}}}', tfrac(key))}$.'}}
    note(V, 7, f'n={n}, k={k}', key, m1, m2, f'{order} one order; {share} share; {atleast} at least k')
    return item


def weigh_rec(n, memo={}):
    """Fewest weighings that always find one heavy coin among n, by search over the first split."""
    if n <= 1:
        return 0
    if n in memo:
        return memo[n]
    best = min(1 + max(weigh_rec(a), weigh_rec(n - 2 * a)) for a in range(1, n // 2 + 1))
    memo[n] = best
    return best


def p8(N):
    k = 0
    while 3 ** k < N:
        k += 1
    m1, m2 = F(k), F(weigh_rec(N))
    key = m1
    halving, pairs, linear = F(math.ceil(math.log2(N))), F(N // 2), F(N - 2)
    assert 2 ** (halving - 1) < N <= 2 ** halving
    check_choice(key, [halving, pairs, linear], [str(x) for x in (key, halving, pairs, linear)])
    g = 3 ** (k - 1)
    item = {
        'question': f'You have {N} coins that look the same. One is heavier and the rest weigh the same. Using a balance scale, what is the fewest weighings that always finds the heavy coin?',
        'widget': choice([
            ('a', str(key), None),
            ('b', str(halving), 'You split the coins in two each time, which wastes the balanced outcome.'),
            ('c', str(pairs), 'You weighed the coins one pair at a time.'),
            ('d', str(linear), 'You set one coin against each other coin in turn.')]),
        'feedback': {'correct': f'Each weighing splits the suspects three ways, and $3^{{{k - 1}}} < {N} \\le 3^{{{k}}}$.',
                     'generic': 'A weighing has three outcomes, so split the coins into three groups.'},
        'explain': {'text': f'Each weighing has three outcomes: left heavy, right heavy or balanced. '
                            f'So $k$ weighings can single out one coin among at most $3^k$, and $3^{{{k - 1}}} = {g} < {N} \\le {3 ** k}$. '
                            f'Put equal groups in the pans and the rest aside, none above {g} coins, then repeat on the suspects.'}}
    note(V, 8, f'N={N}', key, m1, m2, f'{halving} halving; {pairs} pairs; {linear} one against each')
    return item


def bayes_counts(b, s, f):
    """Natural frequencies in 10,000 people (b, s, f in per cent): integers."""
    tp = b * s           # (100 b people) x s/100
    fp = (100 - b) * f   # (10000 - 100 b) x f/100
    return tp, fp


def p9(b, s, f):
    B, S, Fp = F(b, 100), F(s, 100), F(f, 100)
    m1 = B * S / (B * S + (1 - B) * Fp)
    tp, fp = bayes_counts(b, s, f)
    m2 = F(tp, tp + fp)
    key = m1
    hit, joint, base = S, B * S, B
    wl = [('hit', hit), ('joint', joint), ('base', base)]
    if abs(float(joint) - float(base)) <= 2 * TOL:
        # at three decimal places the two slips read the same; keep the base rate, which is the commoner slip
        wl = [('hit', hit), ('base', base)]
        DROPPED.append((V, 9, 'joint', joint))
    check_numeric(key, [w for _, w in wl])
    item = {
        'question': f'A condition affects {b}% of people. A test catches {s}% of true cases and flags {f}% of healthy people by mistake. A person tests positive. What is the chance they have the condition? Give three decimal places.',
        'widget': numeric(key, wl,
                          f'{tp}/{tp + fp} = {key.numerator}/{key.denominator}, about {d3(key)} (within 0.005)', 'Chance of the condition'),
        'feedback': {'correct': f'{tp} true positives among {tp + fp:,}: ${tfrac(key)} \\approx {d3(key)}$.',
                     'generic': 'Picture 10,000 people and count the true and the false positives.',
                     'byKey': {'hit': 'That is the chance of a positive given the condition, the wrong way round.',
                               'joint': 'You divided the true positives by everyone, not by all the positives.',
                               'base': 'You kept the base rate and ignored the test.'}},
        '_bykeep': [w for w, _ in wl],
        'explain': {'text': f'In 10,000 people, {100 * b} have it and {tp} of them test positive. '
                            f'Of the {10000 - 100 * b:,} without it, {fp} test positive. '
                            f'So $P = \\tfrac{{{tp}}}{{{tp} + {fp}}} = {tfrac(key)} \\approx {d3(key)}$.'}}
    note(V, 9, f'b={b}%, s={s}%, f={f}%', key, m1, m2, f'{d3(hit)} hit rate; {d3(joint)} TP over all; {d3(base)} base')
    return item, key


def p14(b, s, f, once):
    B, S, Fp = F(b, 100), F(s, 100), F(f, 100)
    prior_odds, lr = B / (1 - B), S / Fp
    post = prior_odds * lr ** 2
    m1 = post / (1 + post)
    # second method: natural frequencies in 1,000,000 people, integer counts
    pop = 1_000_000
    sick = pop * b // 100
    tp2 = sick * s * s // 10000
    fp2 = (pop - sick) * f * f // 10000
    assert sick * s * s % 10000 == 0 and (pop - sick) * f * f % 10000 == 0
    m2 = F(tp2, tp2 + fp2)
    m3 = B * S ** 2 / (B * S ** 2 + (1 - B) * Fp ** 2)
    assert m3 == m1
    key = m1
    sq = S ** 2
    check_numeric(key, [once, sq])
    lrs = tfrac(lr) if lr.denominator == 1 else dec(lr)
    item = {
        'question': f'A condition affects {b}% of people. A test catches {s}% of true cases and flags {f}% of healthy people. One person takes it twice, with independent results, and is positive both times. What is the chance they have the condition? Give three decimal places.',
        'widget': numeric(key, [('once', once), ('square', sq)],
                          f'{key.numerator}/{key.denominator}, about {d3(key)} (within 0.005)', 'Chance of the condition'),
        'feedback': {'correct': f'Odds ${tfrac(prior_odds)} \\times {lrs}^2 = {tfrac(post)}$, so $P = {tfrac(key)} \\approx {d3(key)}$.',
                     'generic': f'Each positive multiplies the odds by $\\tfrac{{{s}}}{{{f}}}$.',
                     'byKey': {'once': 'That uses one positive only. Update the odds again for the second.',
                               'square': 'You squared the hit rate and ignored the false positives.'}},
        'explain': {'text': f'Prior odds are ${tfrac(prior_odds)}$, and each positive multiplies them by $\\tfrac{{{s}}}{{{f}}} = {lrs}$. '
                            f'Two positives give odds ${tfrac(post)}$, so $P = {tfrac(key)} \\approx {d3(key)}$. '
                            f'Check: $\\tfrac{{{dec(B)} \\times {dec(S)}^2}}{{{dec(B)} \\times {dec(S)}^2 + {dec(1 - B)} \\times {dec(Fp)}^2}}$ gives the same.'}}
    note(V, 14, f'b={b}%, s={s}%, f={f}%', key, m1, m2, f'{d3(once)} one test; {d3(sq)} hit rate squared')
    return item


PAT = {'HH': (F(4), F(3), F(2)), 'HTH': (F(8), F(5), F(14)), 'HHH': (F(8), F(7), F(16))}


def wait_solve(pat):
    """Expected tosses to see pat, by a linear solve over prefix states."""
    k = len(pat)

    def nxt(state, t):
        s = pat[:state] + t
        while s and not pat.startswith(s):
            s = s[1:]
        return len(s)
    A, b = [], []
    for st in range(k):
        row = [F(0)] * k
        row[st] += 1
        for t in 'HT':
            ns = nxt(st, t)
            if ns < k:
                row[ns] -= F(1, 2)
        A.append(row)
        b.append(F(1))
    return solve(A, b)[0]


def p10(pat):
    m1 = sum(F(2) ** j for j in range(1, len(pat) + 1) if pat[:j] == pat[-j:])  # overlap sum
    m2 = wait_solve(pat)
    key = m1
    inv, plus1, third = PAT[pat]
    check_choice(key, [inv, plus1, third], [str(x) for x in (key, inv, plus1, third)])
    prev = {'HH': ('one head', 'H', 2), 'HTH': ('HT', 'HT', 4), 'HHH': ('HH', 'HH', 6)}[pat]
    thirdwhy = {'HH': 'You gave the shortest possible wait, not the average.',
                'HTH': 'You counted every prefix as an overlap, as for HHH, but HT does not end in H.',
                'HHH': 'You used $2^{k+1}$ for a run of heads and forgot to subtract 2.'}[pat]
    expl = {'HH': ('Let $a$ be the wait from scratch and $b$ the wait after one head. '
                   'Then $a = 1 + \\tfrac12 b + \\tfrac12 a$ and $b = 1 + \\tfrac12 a$, since a tail restarts. '
                   'So $a = 2 + b = 3 + \\tfrac12 a$, giving $a = 6$.'),
            'HTH': ('From scratch a tail changes nothing, so $E_0 = 2 + E_H$; from H a head keeps H, so $E_H = 2 + E_{HT}$. '
                    'From HT a head ends it and a tail restarts: $E_{HT} = 1 + \\tfrac12 E_0$. '
                    'So $E_0 = 5 + \\tfrac12 E_0$, giving $E_0 = 10$.'),
            'HHH': ('Let $E_j$ be the wait after $j$ heads; a tail always restarts. '
                    'Then $E_2 = 1 + \\tfrac12 E_0$, $E_1 = 1 + \\tfrac12 E_2 + \\tfrac12 E_0$ and $E_0 = 2 + E_1$. '
                    'Substituting gives $E_0 = \\tfrac72 + \\tfrac34 E_0$, so $E_0 = 14$.')}[pat]
    item = {
        'question': f'You toss a fair coin until {pat} first appears in consecutive tosses. What is the expected number of tosses?',
        'widget': choice([
            ('a', str(key), None),
            ('b', str(inv), f'You took one over the chance of {pat}, which is the gap between repeats, not the first wait.'),
            ('c', str(plus1), f'You waited for {prev[1]}, {prev[2]} tosses, and assumed the next toss obliges.'),
            ('d', str(third), thirdwhy)]),
        'feedback': {'correct': f'Solving the state equations gives {key} tosses.',
                     'generic': 'Write one equation per state of progress, from scratch to one short of the pattern.'},
        'explain': {'text': expl}}
    note(V, 10, pat, key, m1, m2, f'{inv} one over chance; {plus1} previous wait plus one; {third} {pat}-specific')
    return item


def stop_value(n, r):
    v = F(n + 1, 2)
    vals = [v]
    for _ in range(r):
        v = sum(max(F(x), v) for x in range(1, n + 1)) / n
        vals.append(v)
    return vals


def policy_search(n, r):
    """Best value over every keep-set at every stage (brute force)."""
    faces = list(range(1, n + 1))
    subsets = [set(c) for m in range(n + 1) for c in combinations(faces, m)]
    best_next = F(n + 1, 2)
    for _ in range(r):  # stages from the last reroll back; a set is optimal stage by stage
        best_next = max(sum(F(x) if x in S else best_next for x in faces) / n for S in subsets)
    return best_next


def emax(n, m):
    return sum(1 - F(k - 1, n) ** m for k in range(1, n + 1))


def p11(r, n):
    vals = stop_value(n, r)
    m1 = vals[r]
    m2 = policy_search(n, r)
    # an independent joint search over the first and second keep-sets for two rerolls
    if r == 2:
        faces = list(range(1, n + 1))
        subsets = [set(c) for m in range(n + 1) for c in combinations(faces, m)]
        mean = F(n + 1, 2)
        second = [sum(F(x) if x in S else mean for x in faces) / n for S in subsets]
        joint = max(sum(F(x) if x in S1 else v2 for x in faces) / n for S1 in subsets for v2 in second)
        assert joint == m2
    key = m1
    mean = F(n + 1, 2)
    mx = emax(n, r + 1)
    if r == 1:
        thr = min(x for x in range(1, n + 1) if x > mean)
        hi = F(sum(range(thr + 1, n + 1)), n) + F(thr, n) * mean
        slip2, why2 = hi, f'You kept only {thr + 1} or more, but {thr} beats the {money(mean)} a reroll is worth.'
    else:
        slip2, why2 = vals[1], 'You valued the game with one reroll, not two.'
    slips = [mean, slip2, mx]
    check_choice(key, slips, [money(x) for x in [key] + slips])
    rr = 'once' if r == 1 else 'up to twice'
    lines = []
    for st in range(1, r + 1):
        cont = vals[st - 1]
        keep = [x for x in range(1, n + 1) if x > cont]
        lines.append((cont, keep, vals[st]))
    if r == 1:
        cont, keep, v = lines[0]
        expl = (f'A reroll is worth {money(cont)}, so keep any face above {dec(cont)}. '
                f'The value is $\\tfrac{{{" + ".join(map(str, keep))}}}{{{n}}} + \\tfrac{{{n - len(keep)}}}{{{n}}} \\times {dec(cont)} = {dec(v)}$.')
        corr = f'Keep {", ".join(map(str, keep[:-1]))} or {keep[-1]}, because a reroll is worth only {money(cont)}.'
    else:
        (c1, k1, v1), (c2, k2, v2) = lines
        expl = (f'With one reroll left the game is worth {money(v1)}, as the last roll is worth {money(c1)}. '
                f'So on the first roll keep only a face above {dec(v1)}: {", ".join(map(str, k2[:-1]))} or {k2[-1]}. '
                f'The value is $\\tfrac{{{" + ".join(map(str, k2))}}}{{{n}}} + \\tfrac{{{n - len(k2)}}}{{{n}}} \\times {dec(v1)} = {tfrac(v2)}$, about {money(v2)}.')
        corr = f'Keep {", ".join(map(str, k2[:-1]))} or {k2[-1]} first, as the rest of the game is worth {money(v1)}.'
    item = {
        'question': f'A fair {n}-sided die, faces 1 to {n}, pays £ the face. After the first roll you may reroll {rr}, and you must keep the last face rolled. Under the best rule, what is the game worth?',
        'widget': choice([
            ('a', money(key), None),
            ('b', money(mean), 'You never rerolled, so you took the plain average.'),
            ('c', money(slip2), why2),
            ('d', money(mx), 'You took the largest face rolled, but a reroll throws the old face away.')]),
        'feedback': {'correct': corr,
                     'generic': 'Work backwards: keep a face only if it beats the value of rolling again.'},
        'explain': {'text': expl}}
    note(V, 11, f'r={r}, {n} faces', key, m1, m2, f'{money(mean)} never reroll; {money(slip2)} slip; {money(mx)} max of rolls')
    return item


def p12(which, n):
    pairs = list(product(range(1, n + 1), repeat=2))
    if which == 'max':
        m1 = sum(F(k * (2 * k - 1), n * n) for k in range(1, n + 1))
        m2 = F(sum(max(p) for p in pairs), n * n)
        other = sum(F((n - k + 1) ** 2, n * n) for k in range(1, n + 1))
        distinct = F(sum(b * (b - 1) for b in range(1, n + 1)), math.comb(n, 2))
    else:
        m1 = sum(F((n - k + 1) ** 2, n * n) for k in range(1, n + 1))
        m2 = F(sum(min(p) for p in pairs), n * n)
        other = sum(F(k * (2 * k - 1), n * n) for k in range(1, n + 1))
        distinct = F(sum(a * (n - a) for a in range(1, n + 1)), math.comb(n, 2))
    # distinct-pair means checked by enumeration too
    dp = [p for p in pairs if p[0] != p[1]]
    assert distinct == F(sum((max if which == 'max' else min)(p) for p in dp), len(dp))
    assert m1 + other == n + 1
    key = m1
    mean = F(n + 1, 2)
    check_numeric(key, [mean, other, distinct])
    word, oword = ('larger', 'smaller') if which == 'max' else ('smaller', 'larger')
    if which == 'max':
        terms = ' + '.join(f'{k} \\cdot {2 * k - 1}' for k in (1, 2)) + f' + \\dots + {n} \\cdot {2 * n - 1}'
        expl = (f'Both dice must be at most $k$, so $P(\\max \\le k) = (\\tfrac{{k}}{{{n}}})^2$ and $P(\\max = k) = \\tfrac{{2k - 1}}{{{n * n}}}$. '
                f'Then $E = \\tfrac{{{terms}}}{{{n * n}}} = {tfrac(key)} \\approx {d3(key)}$. '
                f'Check: $E[\\max] + E[\\min] = {n + 1}$, and $E[\\min] = {tfrac(other)}$.')
    else:
        sq = ' + '.join(str(j * j) for j in range(n, n - 3, -1)) + ' + \\dots + 1'
        expl = (f'Both dice must be at least $k$, so $P(\\min \\ge k) = (\\tfrac{{{n + 1} - k}}{{{n}}})^2$. '
                f'Then $E[\\min] = \\sum_k P(\\min \\ge k) = \\tfrac{{{sq}}}{{{n * n}}} = {tfrac(key)} \\approx {d3(key)}$. '
                f'Check: $E[\\max] + E[\\min] = {n + 1}$, and $E[\\max] = {tfrac(other)}$.')
    item = {
        'question': f'You roll two fair {n}-sided dice, faces 1 to {n}. What is the expected value of the {word} face? If they tie, that face counts. Give three decimal places.',
        'widget': numeric(key, [('one', mean), ('other', other), ('distinct', distinct)],
                          f'{key.numerator}/{key.denominator}, about {d3(key)} (within 0.005)', f'Expected {word} face'),
        'feedback': {'correct': f'$E = {tfrac(key)} \\approx {d3(key)}$.',
                     'generic': (f'Find $P(\\max \\le k)$ first: both dice must be at most $k$.' if which == 'max'
                                 else f'Find $P(\\min \\ge k)$ first: both dice must be at least $k$.'),
                     'byKey': {'one': f'That is the mean of one die; the {word} of two is pulled {"up" if which == "max" else "down"}.',
                               'other': f'That is the expected {oword} face.',
                               'distinct': 'You left out the doubles, which are as likely as any other ordered pair.'}},
        'explain': {'text': expl}}
    note(V, 12, f'{which}, {n} faces', key, m1, m2, f'{d3(mean)} one die; {d3(other)} other extreme; {d3(distinct)} no doubles')
    return item


def p13(m, k):
    prior = F(1, m + 1)
    m1 = prior / (prior + (1 - prior) * F(1, 2 ** k))
    # second method: enumerate coins and every toss sequence of length k
    num = den = F(0)
    for coin in range(m + 1):
        ph = F(1) if coin == m else F(1, 2)
        for seq in product('HT', repeat=k):
            pr = F(1, m + 1)
            for t in seq:
                pr *= ph if t == 'H' else 1 - ph
            if all(t == 'H' for t in seq):
                den += pr
                if coin == m:
                    num += pr
    m2 = num / den
    odds = F(1, m) * 2 ** k
    assert odds / (1 + odds) == m1
    key = m1
    equal = F(2 ** k, 2 ** k + 1)
    onem = 1 - F(1, 2 ** k)
    pk = den
    third, thirdwhy = onem, f"You took one minus a fair coin's chance of {k} heads."
    try:
        check_choice(key, [prior, equal, onem], [dfrac(x) for x in (key, prior, equal, onem)])
    except AssertionError:
        third, thirdwhy = pk, f'You found the chance of {k} heads, not the chance of the coin.'
        check_choice(key, [prior, equal, pk], [dfrac(x) for x in (key, prior, equal, pk)])
    words = {3: 'three', 4: 'four'}
    item = {
        'question': f'A bag holds {m} fair coins and one coin with two heads. You draw a coin at random and toss it {k} times. It shows {k} heads. What is the chance it is the two-headed coin?',
        'widget': choice([
            ('a', f'${dfrac(key)}$', None),
            ('b', f'${dfrac(prior)}$', f'You kept the prior ${tfrac(prior)}$ and ignored the {k} heads.'),
            ('c', f'${dfrac(equal)}$', f'You gave the two kinds of coin equal priors, but fair coins outnumber it {m} to 1.'),
            ('d', f'${dfrac(third)}$', thirdwhy)]),
        'feedback': {'correct': f'Odds $\\tfrac{{1}}{{{m}}} \\times {2 ** k} = {tfrac(odds)}$, so $P = {tfrac(key)}$.',
                     'generic': f'Weigh each kind of coin by its prior times its chance of {k} heads.'},
        'explain': {'text': f'Prior odds are $1 : {m}$, and {k} heads are $2^{k} = {2 ** k}$ times likelier with the two-headed coin. '
                            f'Posterior odds are ${odds.numerator} : {odds.denominator}$, so $P = {tfrac(key)}$. '
                            f'Check: $\\tfrac{{{sfrac(prior)}}}{{{sfrac(prior)} + {sfrac(1 - prior)} \\times {sfrac(F(1, 2 ** k))}}} = {tfrac(key)}$.'}}
    note(V, 13, f'm={m}, k={k}', key, m1, m2, f'{prior} prior; {equal} equal priors; {third} third')
    return item


def ruin_duration_solve(i, N):
    n = N - 1
    A = [[F(0)] * n for _ in range(n)]
    b = [F(1)] * n
    for k in range(1, N):
        A[k - 1][k - 1] = F(1)
        if k - 1 >= 1:
            A[k - 1][k - 2] = F(-1, 2)
        if k + 1 <= N - 1:
            A[k - 1][k] = F(-1, 2)
    return solve(A, b)[i - 1]


def p15(i, N):
    m1 = F(i * (N - i))
    m2 = ruin_duration_solve(i, N)
    key = m1
    dist, prod_, sq = F(N - i), F(i * N), F((N - i) ** 2)
    check_choice(key, [dist, prod_, sq], [str(x) for x in (key, dist, prod_, sq)])
    item = {
        'question': f'You start with £{i} and bet £1 at a time on a fair coin. You stop when you reach £0 or £{N}. What is the expected number of bets?',
        'widget': choice([
            ('a', str(key), None),
            ('b', str(dist), f'You counted the steps to £{N} as if every bet were a win.'),
            ('c', str(prod_), f'You multiplied {i} by {N}; the formula uses the distances to both ends.'),
            ('d', str(sq), f'You squared the distance to £{N} and ignored the floor at £0.')]),
        'feedback': {'correct': f'$i(N - i) = {i} \\times {N - i} = {key}$.',
                     'generic': 'First-step analysis: $D_k = 1 + \\tfrac12 (D_{k-1} + D_{k+1})$, with $D_0 = D_N = 0$.'},
        'explain': {'text': f'The duration $D_k$ satisfies $D_k = 1 + \\tfrac12(D_{{k-1}} + D_{{k+1}})$, with $D_0 = D_{{{N}}} = 0$. '
                            f'Its solution is $D_k = k({N} - k)$, so $D_{i} = {key}$. '
                            f'Check: $1 + \\tfrac12(D_{i - 1} + D_{i + 1}) = 1 + \\tfrac12({(i - 1) * (N - i + 1)} + {(i + 1) * (N - i - 1)}) = {key}$.'}}
    assert 1 + F((i - 1) * (N - i + 1) + (i + 1) * (N - i - 1), 2) == key
    note(V, 15, f'i={i}, N={N}', key, m1, m2, f'{dist} N-i; {prod_} iN; {sq} squared distance')
    return item


def ruin_prob_closed(p, i, N):
    p = F(p)
    q = 1 - p
    if p == F(1, 2):
        return F(i, N)
    r = q / p
    return (1 - r ** i) / (1 - r ** N)


def ruin_prob_shoot(p, i, N):
    p = F(p)
    q = 1 - p
    P = [F(0), F(1)]
    for k in range(1, N):
        P.append((P[k] - q * P[k - 1]) / p)
    return P[i] / P[N]


def ruin_prob_solve(p, i, N):
    p = F(p)
    q = 1 - p
    n = N - 1
    A = [[F(0)] * n for _ in range(n)]
    b = [F(0)] * n
    for k in range(1, N):
        A[k - 1][k - 1] = F(1)
        if k + 1 == N:
            b[k - 1] += p
        else:
            A[k - 1][k] = -p
        if k - 1 >= 1:
            A[k - 1][k - 2] = -q
    return solve(A, b)[i - 1]


def ptext(p):
    # words, not \\tfrac, in question text: an inline \\tfrac draws at about 70% of the prose size
    return {F(11, 20): '0.55', F(3, 5): '0.6', F(2, 3): 'two in three', F(3, 4): 'three in four'}[F(p)]


def p16(p, i, N):
    p = F(p)
    q = 1 - p
    m1 = ruin_prob_closed(p, i, N)
    m2 = ruin_prob_shoot(p, i, N)
    assert ruin_prob_solve(p, i, N) == m1
    key = m1
    fair, streak, one = F(i, N), p ** (N - i), p
    check_numeric(key, [fair, streak, one])
    r = q / p
    item = {
        'question': f'You start with £{i}. Each £1 bet wins with chance {ptext(p)}, independently. You stop when you reach £0 or £{N}. What is the chance you reach £{N}? Give three decimal places.',
        'widget': numeric(key, [('fair', fair), ('streak', streak), ('one', one)],
                          f'{key.numerator}/{key.denominator}, about {d3(key)} (within 0.005)', f'Chance of reaching £{N}'),
        'feedback': {'correct': f'$\\tfrac{{1 - r^{i}}}{{1 - r^{{{N}}}}}$ with $r = {tfrac(r)}$ gives ${tfrac(key)} \\approx {d3(key)}$.',
                     'generic': 'Use $P_i = \\tfrac{1 - r^i}{1 - r^N}$, where $r = \\tfrac{q}{p}$ is the losing odds.',
                     'byKey': {'fair': f'That is the fair-coin answer $\\tfrac{{{i}}}{{{N}}}$, but the edge is on your side.',
                               'streak': f'You needed {N - i} wins in a row, but losses can be won back.',
                               'one': 'That is the chance of winning a single bet.'}},
        'explain': {'text': f'$P_k$ solves $P_k = pP_{{k+1}} + qP_{{k-1}}$ with $P_0 = 0$ and $P_{{{N}}} = 1$, so $P_k = \\tfrac{{1 - r^k}}{{1 - r^{{{N}}}}}$ with $r = \\tfrac{{q}}{{p}} = {tfrac(r)}$. '
                            f'So $P_{i} = \\tfrac{{1 - ({sfrac(r)})^{i}}}{{1 - ({sfrac(r)})^{{{N}}}}} = {tfrac(key)} \\approx {d3(key)}$. '
                            'Check: shooting $P_{k+1} = (P_k - qP_{k-1})/p$ from $P_0 = 0$ gives the same.'}}
    note(V, 16, f'p={p}, i={i}, N={N}', key, m1, m2, f'{d3(fair)} fair i/N; {d3(streak)} streak; {d3(one)} one bet')
    return item


def p17(p):
    p = F(p)
    fair1 = ruin_prob_closed(F(1, 2), 1, 3)
    bias1 = ruin_prob_closed(p, 1, 3)
    m1 = F(1, 2) * bias1 / (F(1, 2) * (fair1 + bias1))
    fs, bs = ruin_prob_solve(F(1, 2), 1, 3), ruin_prob_solve(p, 1, 3)
    m2 = bs / (fs + bs)
    key = m1
    stage, prior = F(1, 2) * (fair1 + bias1), F(1, 2)
    check_numeric(key, [stage, bias1, prior])
    r = (1 - p) / p
    item = {
        'question': f'A coin is either fair or lands heads with chance {ptext(p)}, each equally likely. You start with £1 and bet £1 on heads at each toss. You stop at £0 or £3. You reach £3. What is the chance the coin is the biased one? Give three decimal places.',
        'widget': numeric(key, [('stage', stage), ('biased', bias1), ('prior', prior)],
                          f'{key.numerator}/{key.denominator}, about {d3(key)} (within 0.005)', 'Chance the coin is biased'),
        'feedback': {'correct': f'$\\tfrac{{{sfrac(bias1)}}}{{{sfrac(fair1)} + {sfrac(bias1)}}} = {tfrac(key)} \\approx {d3(key)}$.',
                     'generic': "Find each coin's chance of reaching £3, then use Bayes with equal priors.",
                     'byKey': {'stage': 'That is the chance of reaching £3. Now condition on having reached it.',
                               'biased': "That is the biased coin's chance of reaching £3, not the posterior.",
                               'prior': 'You kept the prior and ignored that you reached £3.'}},
        'explain': {'text': f'From £1 a fair coin reaches £3 with chance $\\tfrac13$, and the biased one with $\\tfrac{{1 - r}}{{1 - r^3}} = {tfrac(bias1)}$, where $r = {tfrac(r)}$. '
                            f'The equal priors cancel, so $P = \\tfrac{{{sfrac(bias1)}}}{{1/3 + {sfrac(bias1)}}} = {tfrac(key)} \\approx {d3(key)}$.'}}
    note(V, 17, f'p={p}', key, m1, m2, f'{d3(stage)} P(reach); {d3(bias1)} biased P(reach); {d3(prior)} prior')
    return item

# ---------- positions table ----------

POS = [  # (pos, diff, tag, skill, title, builder, pool, fixed v1)
    (1, 2, 'dice-ev', 'pz-expectation', 'A die that pays squares', p1, [(4,), (6,), (8,)], (6,)),
    (2, 2, 'linearity', 'pz-expectation', 'Cards of one kind', p2, [(k, t) for k in (5, 8, 13) for t in ('heart', 'ace')], (5, 'heart')),
    (3, 2, 'ev-fee', 'pz-expectation', 'A game with a fee', p3, [(c, t) for c in (2, 3, 4) for t in ('even', 'ge4')], (3, 'even')),
    (4, 2, 'indicator', 'pz-expectation', 'Pairs of heads', p4, [(10,), (13,), (21,)], (10,)),
    (5, 3, 'at-least-one', 'pz-conditioning', 'At least one six', p5, [(3,), (4,), (5,)], (4,)),
    (6, 3, 'cards-conditional', 'pz-conditioning', 'Two cards, at least one', p6, [('ace',), ('heart',), ('face',)], ('ace',)),
    (7, 3, 'binomial', 'pz-conditioning', 'Exactly so many heads', p7, [(6, 3), (7, 2), (8, 4)], (6, 3)),
    (8, 3, 'weighing', 'bz-search', 'The heavy coin', p8, [(10,), (28,), (80,)], (10,)),
    (9, 3, 'bayes', 'pz-conditioning', 'A positive test', None, [(b, s, f) for b in (1, 2, 5) for s in (90, 95) for f in (5, 10)], (1, 95, 5)),
    (10, 4, 'waiting-time', 'pz-recursion', 'Waiting for a pattern', p10, [('HH',), ('HTH',), ('HHH',)], ('HH',)),
    (11, 4, 'stopping', 'pz-recursion', 'Roll again or keep', p11, [(r, n) for r in (1, 2) for n in (6, 8)], (1, 6)),
    (12, 4, 'max-of-draws', 'pz-expectation', 'One face of two dice', p12, [(w, n) for w in ('max', 'min') for n in (6, 8)], ('max', 6)),
    (13, 4, 'bayes-multi', 'pz-conditioning', 'The two-headed coin', p13, [(m, k) for m in (3, 4) for k in (3, 4)], (3, 3)),
    (14, 4, 'bayes-multi', 'pz-conditioning', 'Two positive tests', None, None, None),
    (15, 4, 'ruin-fair', 'pz-games', 'How long a fair game lasts', p15, [(3, 10), (2, 8), (4, 9)], (3, 10)),
    (16, 5, 'ruin-biased', 'pz-games', 'Ruin with an edge', p16, [(p, i, N) for p in (F(11, 20), F(3, 5), F(2, 3)) for (i, N) in ((2, 5), (3, 6))], (F(3, 5), 2, 5)),
    (17, 5, 'bayes-ruin', 'pz-games', 'Which coin got you there', p17, [(F(2, 3),), (F(3, 4),), (F(3, 5),)], (F(3, 4),)),
]

NAMES = {1: 'Quantitative evaluation', 2: 'Quantitative evaluation, version 2', 3: 'Quantitative evaluation, version 3'}
MODELS = ("Reported, as of Nov 2026: SIG's Quantitative Evaluation. Seventeen questions in 60 minutes with a calculator, "
          "rising from quick expected values to multi-stage Bayes and ruin.")
DESC = ("This is the reported format of SIG's Quantitative Evaluation, as candidates described it by Nov 2026. "
        "You have 17 questions in 60 minutes. A calculator is allowed, but the app has none, so have a basic one ready. "
        "The questions start with quick expected values and end with multi-stage Bayes and gambler's ruin. "
        "Some take a choice, others a number to three decimal places. "
        "A wrong answer scores 0, and you may change answers until you submit. "
        "Other reports give 16 questions in 20 minutes; this mock follows the longer one. This is version {v} of 3.")
SKILLS = {'pz-expectation': 'Expected value puzzles', 'pz-conditioning': 'Conditioning puzzles',
          'pz-recursion': 'First-step analysis', 'pz-games': 'Games and betting', 'bz-search': 'Weighing and search'}
assert len(MODELS) <= 200

used = {pos: [] for pos, *_ in POS}
REJECT = []


def draw(pos, pool, fixed, v, build):
    if v == 1:
        return fixed, build(*fixed)
    rng = random.Random(SEEDS[v] * 100 + pos)
    cands = [c for c in pool if c not in used[pos]]
    rng.shuffle(cands)
    for c in cands:
        try:
            return c, build(*c)
        except AssertionError as e:
            REJECT.append((v, pos, c, str(e)[:80]))
            KEYS[:] = [k for k in KEYS if not (k[0] == v and k[1] in (pos, 14 if pos == 9 else pos))]
            DROPPED[:] = [d for d in DROPPED if not (d[0] == v and d[1] == pos)]
    raise SystemExit(f'no valid draw for pos {pos} v{v}')


for V in (1, 2, 3):
    items = []
    p9key = None
    p9params = None
    for pos, diff, tag, skill, title, build, pool, fixed in POS:
        if pos == 9:
            def b9(b, s, f):
                it9, k9 = p9(b, s, f)
                return it9, p14(b, s, f, k9)  # a draw must suit both item 9 and item 14
            params, (item, item14) = draw(9, pool, fixed, V, b9)
            p9params = params
        elif pos == 14:
            params, item = p9params, item14
        else:
            params, item = draw(pos, pool, fixed, V, build)
        used[pos].append(params)
        full = {'id': f'q{pos:02d}-{tag}', 'difficulty': diff, 'skills': [skill], 'tags': [tag], 'pace': PACE[diff],
                'title': title}
        keep = item.pop('_bykeep', None)
        if keep is not None:
            item['feedback']['byKey'] = {k: v for k, v in item['feedback']['byKey'].items() if k in keep}
        full.update(item)
        items.append(full)
    assert [it['difficulty'] for it in items].count(2) == 4
    assert [it['difficulty'] for it in items].count(3) == 5
    assert [it['difficulty'] for it in items].count(4) == 6
    assert [it['difficulty'] for it in items].count(5) == 2
    assert sum(it['pace'] for it in items) == 3420
    eid = 'mock-oa-sig' if V == 1 else f'mock-oa-sig-{V}'
    exam = {'id': eid, 'name': NAMES[V], 'style': 'trader', 'models': MODELS, 'description': DESC.format(v=V),
            'skills': SKILLS,
            'parts': [{'kind': 'paper', 'id': 'quant', 'name': 'Quantitative evaluation', 'minutes': 60,
                       'scoring': {'right': 1, 'wrong': 0, 'blank': 0}, 'passNet': 11, 'items': items}]}
    path = f'{OUT}/{eid}.json'
    with open(path, 'w') as fh:
        json.dump(exam, fh, ensure_ascii=False, indent=2)
        fh.write('\n')
    print(f'wrote {path}: {len(items)} items')

# no parameter set repeats across versions at any position
for pos, lst in used.items():
    assert len(set(lst)) == 3, (pos, lst)

for row in KEYS:
    v, pos, params, key, slips = row
    print(f'v{v} Q{pos:<2} {params:<22} key {str(key):<9} = {float(key):.4f}   {slips}')
for d in DROPPED:
    print('dropped wrong (reads as another slip at 3 dp)', d)
for r in REJECT:
    print('rejected', r)
```
