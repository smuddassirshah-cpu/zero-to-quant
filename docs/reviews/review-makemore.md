# makemore (First language models), levels 1 to 3: second-reader findings

Scope: every file in `app/content/courses/makemore/` (12 lessons, 3 reviews, 3 homeworks, 3 problem sets, `course.json`) and `app/content/data/ai/makemore-mlp.json`, at `f9616b05`.
Method: no browser. Ran `docs/reports/makemore-L1-numbers.py`, `-L2-`, `-L3-` with the venv Python, plain and with `ZQ_NUMBERS_STRICT=1`; ran `node tools/grade-all.mjs --file <path> --code --local-cdn <pkgs>` on each of the 21 files alone; timed every graded case of the 21 code widgets through `tools/code-runner.mjs` (the page's harness and limits); graded 83 wrong solutions of my own (appendix). Recomputed with my own code, not the authors' (`Counter` counts, an own NumPy MLP with hand gradients, own sampler): every count, chance, loss, sweep, seed spread, the 40,000-step run, the overfitting run, both 2D runs, the block-4 run, the seeded samples and the temperature table; checked the two 2D embeddings for "a turn and a flip" by orthogonal Procrustes; re-derived every distractor from its `why`. Style: `docs/reviews/voice-scan.py 35 --summary`, plus greps for em-dashes, exclamation marks and American spellings.
Format: `path | screen/item | severity | what is wrong | fix`. Severity: error = wrong number, false claim or wrong grading; warning = weak explanation, teaching issue or a test gap; note = style or small.

Counts: 2 errors, 7 warnings, 18 notes.

## Checks that passed

- Number scripts: L1 375 of 375, L2 207 of 207, L3 162 of 162, exit 0 (11 s, 37 s, 39 s). They read every stated value at its JSON path (`lv.expect`), check each `wrong[]` value outside its answer's tolerance, and run solution, starter and mutants. With `ZQ_NUMBERS_STRICT=1` each exits 1 on its coverage line only: uncovered on-screen numbers L1 168, L2 213, L3 205 (586 in all; warn only for this course). A sample of the uncovered numbers is repeats of checked figures (2.1609, 2.4514, 22,807) and given inputs (0.62, 0.01, 500).
- `makemore-mlp.json` is what the L2 script writes: my own 40,000-step run (own init, own gradients, batches from `default_rng(1)`) agrees with the file to 5.0e-7 everywhere, and rounding it to 6 places reproduces every one of the 6,097 entries exactly. The file gives train 2.1356, dev 2.1609, test 2.1742.
- `autograd.py`: the three shipped copies (l4 s9, l8 s8, homework-2 item 0) and l8's trainer by reference are byte-identical to `app/content/data/ai/autograd.py` and to backprop `l16-a-small-array-autograd` (SHA-256 `5917d4ec91f7...`).
- `grade-all.mjs --code`, each file alone: 21 files, 21 Python code widgets, 0 failures (3 to 16 s a file).
- Timing (table below): every graded case is at least 13 times inside its limit (slowest: homework-2 item 0, 3.4 s against 47 s; l8 s8, 1.4 s against 45 s). No case is under the 3x margin.
- Every training widget (l4 s9, l8 s8, l11 s7, homework-2 item 0) carries an exact seeded short-run test, and every one of my four no-zeroing variants fails it. Every code widget has at least two `mutants` with the taught bug among them.
- Recomputed and matching: 32,033 names, 196,113 letters, 228,146 pairs; last letters n 6,763, a 6,640, e 3,983, y 2,007; 102 zero cells; the slice; a then n third commonest pair; rows a 33,885, q 272, n 18,327, v 2,573, x 697, y 9,776; Row A and Row B log-likelihoods −260.49 and −237.43; dev sweep 2.4520, 2.4514, 2.4514, 2.4606, 2.5507; the 7 unseen dev pairs; bigram train, dev, test 2.4536, 2.4514, 2.4702; all-names 2.4546 nats, 3.5412 bits, 11.64; emma and jo costs; seeds 5 and 7 sweeps; ma 1,453; 29,494 distinct names, 390 and 417 repeats; the 500-name network (3.7441, 2.6236, 2.4387, 2.4122, 2.3830, gap 0.7687, counts 2.3820 and 2.4554, step 0.1 gives 3.7007); 182,531 rows, 5,440 contexts; after em i 160, a 140, end 128, m 100, e 80; z in 1 context in 35; initial dev 3.3010; the run's marks (200: 2.5816 and 2.5876; 1,000: 2.4249; 30,000: 2.2198); batch losses 196 to 200; the sweep and step 5 (3.28, 7.93, 7.93, 13.65, 13.67, dev 44.33); five seeds 2.4249, 2.4160, 2.4226, 2.4321, 2.4314; block 4 3.2937 and 2.5619; overfitting run (every tabled point, least dev 2.4568 at step 2,000); short run 2.423 and 2.655; 2D dev 2.32 and 2.33; first-letter chances and their shares; temperatures (a 0.3342, 0.1502, 0.0831; dev 2.5456 to 3.2674; least at 1.01, 7.4e-5 lower); seed 3 lists, seed 7 lists at 1.5, 0.5 and 1; 19.4% and 9.8%; 2 capped; argmax alee; every hand computation in the problems and homework.
- Voice: 0 sentences over 35 words, 0 explanations over three sentences, 0 lesson ids in code spans, 0 doubled words, no em-dashes, no exclamation marks in text, no American spellings found.

## Level 1 (Bigrams)

- app/content/courses/makemore/l3-one-loss-two-units.json and every later file that says "nats a letter" | l3 s0 onward | warning | The loss is averaged over every next symbol, the end mark included (228,146 pairs, 22,807 on dev), but the course calls it "nats a letter" from l3 s0 and never says so; l3 s3 and review-1 say "a pair" for the same average. A learner (and `sequence` L3, whose causal model is scored against the bigram's 2.4514) can divide by letters instead: that gives a different number (2.4514 becomes 2.85 on dev). | In l3 s2 add: "Here "a letter" means each next symbol, the end mark included: 22,807 of them on the dev names." Keep the phrase elsewhere.
- app/content/courses/makemore/l2-the-counts-are-best.json | s3 derive | note | The six lines restate info l8 almost line for line (log-likelihood as $-N H(\hat p, q)$, the split into $H + D$, Jensen), re-teaching a prerequisite rather than applying it. | Shorten to three lines that cite info l8 for the split and apply it per row: "each row is its own coin, so the info l8 argument runs row by row".
- app/content/courses/makemore/l3-one-loss-two-units.json | s4 canvas | note | The number line shows "bigram" at 2.4546 with the caption "add-one counts from all 32,033 names", but the screen is about the training counts scored on dev (2.4514) against $\ln 27$. | Points at 2.4514 (dev) and 3.2958 (equal chances); caption "Add-one counts from the training names, scored on the dev names."
- app/content/courses/makemore/l3-one-loss-two-units.json | s8 widget.how | note | Rounding the nats first and converting the rounded value fails test 1 (4.7548 against 4.7549) with only the generic line. The prose "each rounded to 4 places" allows that reading. | Add to `how`: "Convert before rounding: bits and perplexity come from the unrounded nats."
- app/content/courses/makemore/l1-counting-pairs.json | s9 widget | note | A `dtype=float` table passes every test (the tests cast with `int`), though the prose asks for whole-number counts. | Add `{ "call": "bigram_counts(['ab']).dtype.kind", "expect": "'i'" }` or drop "whole-number" from the prose.
- app/content/courses/makemore/homework-1.json | h-mle-proof line h5 | note | "Gibbs: $D \ge 0$" names an inequality the strand never introduces; info l6 and makemore l2 call the same step Jensen. | "By Jensen (info l6): $D \ge 0$ ..."

## Level 2 (A network with embeddings)

- app/content/courses/makemore/l6-letters-as-points.json | s1 explain | error | "The two runs differ by a turn and a flip" is false. Aligning run 2 to run 1 by the best rotation and reflection (orthogonal Procrustes on the 27 plotted points) leaves a residual of 0.94 of run 1's spread (0.79 with a free scale), and the two runs' pairwise distances correlate only 0.44. The vowels gather in both, but the layouts are not mirror images. `representations` L1's trap ("rotate the table and the model can undo it") would then rest on a false picture. | "The two runs place the letters differently, yet in both the vowels gather, closer to each other (about 1.1 and 1.2 apart on average) than the consonants (1.8 and 2.1)."
- app/content/courses/makemore/l7-the-mlp-model.json | s6 explain; summary.ideas[2]; review-2 r-tanh explain | error | "The tanh is what lets the hidden layer combine letters, for example to treat em differently from m" is false as an example: the linear model $E(W_1W_2)$ already sees the e in position 2 and treats em differently from .m. What a linear map cannot do is make one letter's effect depend on another's; it only adds a separate vote from each position. | "The tanh lets letters interact: without it each position adds its own fixed vote, so what m predicts could not depend on the letter before it."
- app/content/courses/makemore/l7-the-mlp-model.json | s0 prose; s2 prose; summary.ideas[0]; homework-2 h-perf prose | warning | The sizes are attributed to Bengio et al.: "Bengio and colleagues' network (2003) instead embeds each symbol in 10 numbers ... 100 tanh units to 27 outputs". Bengio, Ducharme, Vincent and Jauvin (JMLR 2003) modelled words (a vocabulary near 18,000) with 30 to 100 features, up to 100 hidden units and optional direct input-to-output weights; the 10, 100 and 27 are this course's. | s0: "A network in the style of Bengio and colleagues (2003), who did this for words, instead embeds each symbol in 10 numbers ..."; s2: "the MLP language model of Bengio et al. (2003), here without their direct input-to-output weights".
- app/content/courses/makemore/l5-three-letters-of-context.json | s3 wrong `pads` (233,783) | warning | 233,783 is $156{,}905 + 3 \times 25{,}626$, three extra rows a name with no end row. The why "You gave the padding marks rows too" gives the three pads, the letters and the end, $156{,}905 + 4 \times 25{,}626 = 259{,}409$. | Value 259,409 with the current why, or why "You counted the symbols of `...emma`, the pads and the letters, $L + 3$ a name."
- app/content/courses/makemore/l7-the-mlp-model.json | s11 wrong `product` (132) | warning | 132 is $11 \times 4 \times 3$: one row of 4 for every sector and exchange pair. The why says "You multiplied the tables together", which is $44 \times 6 = 264$. | Keep 132 with why "You gave every sector and exchange pair its own row of 4: $33 \times 4$. The two tables are separate and add."
- app/content/courses/makemore/l8-minibatches-and-rates.json | s6 options[0] text, byKey.ok; review-2 r-batch-noise option `yes` why | warning | "One batch of 32 swings by 0.4 nats from step to step" and "Neighbouring batches differ by 0.4 nats": the five batch losses (2.6831, 2.5913, 2.3616, 2.5334, 2.2918) differ from neighbour to neighbour by 0.09 to 0.24; 0.39 is their range. review-2's argument "0.24 is within that" rests on the 0.4. | "Five batches in a row range over 0.39 nats; compare dev losses"; review-2: "Five neighbouring batches of one run range from 2.29 to 2.68; a gap of 0.24 is well inside that."
- app/content/courses/makemore/l7-the-mlp-model.json | s10 widget; homework-2 item 6 (h-perf) | warning | A loss with no maximum taken out (`np.log(np.exp(Z).sum(axis=1))`) passes every test of both widgets, though the prose asks for log-sum-exp and the hint says to subtract the maximum. The supplied and planted logits are small. | Add a test with large logits, e.g. the planted model with `b2` shifted by 1,000 (loss unchanged, 0.595828), as l12's test 3 does for softmax.
- app/content/courses/makemore/l5-three-letters-of-context.json | s7 explain | note | "the rows are the 228,146-style bigram pairs" reads oddly. | "the rows are level 1's bigram pairs: 182,531 of them on the training names."
- app/content/courses/makemore/l6-letters-as-points.json | s5 options[0] text | note | "Fancy `+=` writes each index once" is not what happens: it writes a repeated index more than once and the last write wins (as the explain says). | "Fancy `+=` reads every repeat before writing, so the last write wins."
- app/content/courses/makemore/l8-minibatches-and-rates.json | quiz[2] options[0] text | note | "past 1 the steps overshoot", but in the sweep shown 1 already overshoots (2.47 against 2.42). | "0.1 to 0.3 is the useful range; by 1 the steps overshoot."
- `representations` L1 (downstream) | l6 s1 canvas | note | `representations` L1's hook reuses "a 27 by 2 table of character embeddings from makemore L2 if shipped". The 2D tables exist only inside the l6 canvas frames, not as a data file. | Have `makemore-L2-numbers.py` write `app/content/data/ai/makemore-emb2d.json` (both runs, the seeds and dev losses), or tell the `representations` author to read the canvas frames.

## Level 3 (Sampling and held-out loss)

- app/content/courses/makemore/homework-3.json | items[6] (h-perf) `dev_loss` | warning | A `dev_loss` that never resets the context between names passes every test. `toy` reads only the last symbol, which is the end mark 0 after every name, and test 7 is only a threshold on the MLP (below 2.4514). The same bug fails homework-3 item 0 test 3, which checks the MLP to 4 places. | Add `round(dev_loss(mlp, dev500[:50]), 4)` compared exactly (value from the script).
- app/content/courses/makemore/l11-overfitting.json | s1 feedback.correct, option `s250` why | note | "after that it only rises" and "It falls for the first 2,000 steps": the dev curve rises at 1,250 and 1,500 (2.4628, 2.4915) and falls again at 1,750 and 2,000, and after 2,000 it dips several times (2.4733 at 2,750, 2.5825 at 4,250). | "after that it trends upward"; s250 why: "It falls at first; its lowest point is at step 2,000."
- app/content/courses/makemore/l11-overfitting.json | s6 feedback.correct | note | "train and dev stay within 0.002": the gap is 0.0022. | "about 0.002 apart".
- app/content/courses/makemore/l11-overfitting.json | quiz[2] explain; review-3 r-cure explain | note | "With all the names, the same network cannot memorise them; the course MLP keeps train and dev 0.025 apart" mixes two models: the hidden-300 network was never trained on all the names, and 0.025 is the hidden-100 MLP's gap. | "With all the names a network has far more data for its size: the course MLP, trained on all of them, keeps train and dev 0.025 apart."
- app/content/courses/makemore/l10-train-dev-test.json | s2 prose, s4 | note | "test is used once, at the end, to report", but the course itself reports the bigram's test loss in l3 s8, s9 and quiz[0], review-1 r-test-pp, and the MLP's in l7 s10, before any choice is finished. No choice was made on test, so the figures stay honest, but the learner sees test numbers quoted from level 1. | One sentence in l10 s2: "We have quoted test losses before as figures only; no choice was ever made on them."
- app/content/courses/makemore/l10-train-dev-test.json | s3 explain | note | "The topic's exit is this:" is internal planning language. | "This is what the whole course set out to show:".
- app/content/courses/makemore/l9-sampling-names.json | s4 canvas | note | The screen discusses 500 draws with seed 11 while the canvas, titled "two samplers, seed 3", shows the six seed-3 names. | Caption "The seed-3 lists of the first screen; the 500 draws use seed 11."
- app/content/courses/makemore/l9-sampling-names.json | quiz[2] options[2] why | note | "It only catches a $u$ above the last total": the case is $u$ at or above it, as quiz[2]'s explain says. | "at or above the last total".
- app/content/courses/makemore/l12-temperature.json | s8 hints[1] | note | "a 1% move becomes about 0.01%" reads as a 1% price move. | "a move with chance 1% gets about 0.01% before rescaling".

## Whole course

- docs/reports/makemore-L1/L2/L3-numbers.py | strict coverage | note | 586 on-screen numbers have no check against them under `ZQ_NUMBERS_STRICT=1` (L1 168, L2 213, L3 205). Warn only: the course predates the rule, and the sample read is repeats and givens. | Before the next level of this course, add `lv.stated(...)` or `expect` lines until strict passes.
Wrong solutions (not a finding; the four survivors are counted above): 83 tried, 12 survive. Eight of the 12 are correct alternatives and should pass (one-hot product for `W[xs]`, `np.add.at` on flattened indices, `rng.choice(len(X), 32)`, which draws the same stream as `integers`, `rng.shuffle` of positions, `np.argmin`, the maximum taken out before dividing by $T$, chances to the power $1/T$, `exp(log p / T)`). Four are wrong and survive: the float table (l1 s9), no maximum in the log-sum-exp (l7 s10, homework-2 item 6), and the unreset context in homework-3's `dev_loss`; each has a finding above. The prompt's taught bugs all fail: counts without the marks, smoothing after normalising, log base 2 for nats, the wrong averaging axis, the reversed context, sampling that never stops, held-out loss on training names, no gradient zeroing. The course has no code widget for a learning-rate sweep; the test-split analogue (choosing on test, homework-3 item 0) fails test 4.

## Timing of graded cases

Measured with `tools/code-runner.mjs` in node (Pyodide 0.27.7 from the pkgs folder, one worker); a browser may be two or three times slower, still far inside every limit.

| Widget | Cases | Slowest case (ms) | Limit per case (ms) | Margin |
|---|---|---|---|---|
| l1-counting-pairs.json screens.9.widget | 6 | 184 | 39000 | 211x |
| l2-the-counts-are-best.json screens.10.widget | 6 | 15 | 39000 | 2630x |
| l3-one-loss-two-units.json screens.8.widget | 5 | 94 | 39000 | 413x |
| l4-bigram-as-network.json screens.9.widget | 5 | 256 | 41000 | 160x |
| l5-three-letters-of-context.json screens.8.widget | 5 | 209 | 39000 | 186x |
| l6-letters-as-points.json screens.8.widget | 5 | 1 | 35000 | 35000x |
| l7-the-mlp-model.json screens.9.widget | 4 | 1 | 35000 | 35000x |
| l7-the-mlp-model.json screens.10.widget | 4 | 218 | 39000 | 179x |
| l8-minibatches-and-rates.json screens.8.widget | 4 | 1382 | 45000 | 32x |
| l9-sampling-names.json screens.8.widget | 5 | 1 | 39000 | 39000x |
| l10-train-dev-test.json screens.8.widget | 5 | 24 | 35000 | 1456x |
| l11-overfitting.json screens.7.widget | 6 | 303 | 43000 | 141x |
| l12-temperature.json screens.7.widget | 6 | 0 | 35000 | 35000x |
| homework-1.json items.0.widget | 5 | 445 | 43000 | 96x |
| homework-1.json items.1.widget | 4 | 13 | 35000 | 2692x |
| homework-1.json items.6.widget | 7 | 200 | 43000 | 215x |
| homework-2.json items.0.widget | 7 | 3403 | 47000 | 13x |
| homework-2.json items.6.widget | 6 | 148 | 39000 | 263x |
| homework-3.json items.0.widget | 5 | 183 | 43000 | 234x |
| homework-3.json items.1.widget | 4 | 167 | 39000 | 234x |
| homework-3.json items.6.widget | 7 | 100 | 43000 | 430x |

## Appendix: wrong solutions

Each source was graded against the widget's hidden tests with the page's harness (`tools/code-runner.mjs`). "fails test N" is the first hidden test it fails; SURVIVES means it passes every hidden test.

### l1-counting-pairs.json screens.9.widget

**l1-a: no start or end mark at all.** Result: fails test 1.

```python
import numpy as np


def bigram_counts(words):
    index = {c: i + 1 for i, c in enumerate("abcdefghijklmnopqrstuvwxyz")}
    index["."] = 0
    N = np.zeros((27, 27), dtype=int)
    for w in words:
        cs = w
        for a, b in zip(cs, cs[1:]):
            N[index[a], index[b]] += 1
    return N
```

**l1-b: vectorised fancy-index += per name (repeats in a name dropped).** Result: fails test 2.

```python
import numpy as np


def bigram_counts(words):
    index = {c: i + 1 for i, c in enumerate("abcdefghijklmnopqrstuvwxyz")}
    index["."] = 0
    N = np.zeros((27, 27), dtype=int)
    for w in words:
        cs = "." + w + "."
        N[[index[a] for a in cs[:-1]], [index[b] for b in cs[1:]]] += 1
    return N
```

**l1-c: float table instead of whole-number counts.** Result: SURVIVES.

```python
import numpy as np


def bigram_counts(words):
    index = {c: i + 1 for i, c in enumerate("abcdefghijklmnopqrstuvwxyz")}
    index["."] = 0
    N = np.zeros((27, 27), dtype=float)
    for w in words:
        cs = "." + w + "."
        for a, b in zip(cs, cs[1:]):
            N[index[a], index[b]] += 1
    return N
```

### l2-the-counts-are-best.json screens.10.widget

**l2-a: smoothing added after normalising.** Result: fails test 2.

```python
import math
import numpy as np


def bigram_probs(N, alpha):
    M = N / N.sum(axis=1, keepdims=True) + alpha
    return M / M.sum(axis=1, keepdims=True)


def nll(P, words):
    total, n = 0.0, 0
    for w in words:
        cs = "." + w + "."
        for a, b in zip(cs, cs[1:]):
            p = P[index[a], index[b]]
            if p == 0:
                return math.inf
            total -= math.log(p)
            n += 1
    return total / n
```

**l2-b: nll without the end mark.** Result: fails test 4.

```python
import math
import numpy as np


def bigram_probs(N, alpha):
    M = N + alpha
    return M / M.sum(axis=1, keepdims=True)


def nll(P, words):
    total, n = 0.0, 0
    for w in words:
        cs = "." + w
        for a, b in zip(cs, cs[1:]):
            p = P[index[a], index[b]]
            if p == 0:
                return math.inf
            total -= math.log(p)
            n += 1
    return total / n
```

**l2-c: log base 10.** Result: fails test 4.

```python
import math
import numpy as np


def bigram_probs(N, alpha):
    M = N + alpha
    return M / M.sum(axis=1, keepdims=True)


def nll(P, words):
    total, n = 0.0, 0
    for w in words:
        cs = "." + w + "."
        for a, b in zip(cs, cs[1:]):
            p = P[index[a], index[b]]
            if p == 0:
                return math.inf
            total -= math.log10(p)
            n += 1
    return total / n
```

**l2-d: average over letters, not pairs.** Result: fails test 4.

```python
import math
import numpy as np


def bigram_probs(N, alpha):
    M = N + alpha
    return M / M.sum(axis=1, keepdims=True)


def nll(P, words):
    total, n = 0.0, 0
    for w in words:
        cs = "." + w + "."
        for a, b in zip(cs, cs[1:]):
            p = P[index[a], index[b]]
            if p == 0:
                return math.inf
            total -= math.log(p)
            n += 1
    return total / sum(len(w) for w in words)
```

**l2-e: alpha added only to the zero cells.** Result: fails test 2.

```python
import math
import numpy as np


def bigram_probs(N, alpha):
    M = N + alpha * (N == 0)
    return M / M.sum(axis=1, keepdims=True)


def nll(P, words):
    total, n = 0.0, 0
    for w in words:
        cs = "." + w + "."
        for a, b in zip(cs, cs[1:]):
            p = P[index[a], index[b]]
            if p == 0:
                return math.inf
            total -= math.log(p)
            n += 1
    return total / n
```

**l2-f: nll averaged per name (mean of name means).** Result: fails test 4.

```python
import math
import numpy as np


def bigram_probs(N, alpha):
    M = N + alpha
    return M / M.sum(axis=1, keepdims=True)


def nll(P, words):
    means = []
    for w in words:
        cs = "." + w + "."
        t = 0.0
        for a, b in zip(cs, cs[1:]):
            p = P[index[a], index[b]]
            if p == 0:
                return math.inf
            t -= math.log(p)
        means.append(t / (len(cs) - 1))
    return sum(means) / len(means)
```

### l3-one-loss-two-units.json screens.8.widget

**l3-a: rounds the nats first, then converts (bits and perplexity from the rounded nats).** Result: fails test 1.

```python
import math


def loss_report(P, words):
    total, n = 0.0, 0
    for w in words:
        cs = "." + w + "."
        for a, b in zip(cs, cs[1:]):
            total -= math.log(P[index[a], index[b]])
            n += 1
    nats = total / n
    nats = round(nats, 4)
    bits = nats / math.log(2)
    perplexity = math.exp(nats)
    return (round(nats, 4), round(bits, 4), round(perplexity, 4))
```

**l3-b: divides by letters (end pairs not counted in n).** Result: fails test 1.

```python
import math


def loss_report(P, words):
    total, n = 0.0, 0
    for w in words:
        cs = "." + w + "."
        for a, b in zip(cs, cs[1:]):
            total -= math.log(P[index[a], index[b]])
            n += 1
    nats = total / sum(len(w) for w in words)
    bits = nats / math.log(2)
    perplexity = math.exp(nats)
    return (round(nats, 4), round(bits, 4), round(perplexity, 4))
```

**l3-c: perplexity as e to the bits.** Result: fails test 1.

```python
import math


def loss_report(P, words):
    total, n = 0.0, 0
    for w in words:
        cs = "." + w + "."
        for a, b in zip(cs, cs[1:]):
            total -= math.log(P[index[a], index[b]])
            n += 1
    nats = total / n
    bits = nats / math.log(2)
    perplexity = math.exp(bits)
    return (round(nats, 4), round(bits, 4), round(perplexity, 4))
```

**l3-d: no end mark.** Result: fails test 2.

```python
import math


def loss_report(P, words):
    total, n = 0.0, 0
    for w in words:
        cs = "." + w
        for a, b in zip(cs, cs[1:]):
            total -= math.log(P[index[a], index[b]])
            n += 1
    nats = total / n
    bits = nats / math.log(2)
    perplexity = math.exp(nats)
    return (round(nats, 4), round(bits, 4), round(perplexity, 4))
```

**l3-e: log base 2 where nats are asked, bits then divided again.** Result: fails test 1.

```python
import math


def loss_report(P, words):
    total, n = 0.0, 0
    for w in words:
        cs = "." + w + "."
        for a, b in zip(cs, cs[1:]):
            total -= math.log2(P[index[a], index[b]])
            n += 1
    nats = total / n
    bits = nats / math.log(2)
    perplexity = math.exp(nats)
    return (round(nats, 4), round(bits, 4), round(perplexity, 4))
```

### l4-bigram-as-network.json screens.9.widget

**l4-a: zero_grad after backward (gradient wiped before the step).** Result: fails test 1.

```python
import numpy as np
from autograd import Tensor, cross_entropy, sgd_step


def train_bigram_net(xs, ys, steps, lr, seed):
    W = Tensor(np.random.default_rng(seed).standard_normal((27, 27)))
    losses = []
    for k in range(steps + 1):
        loss = cross_entropy(W[xs], ys)
        losses.append(loss.item())
        if k == steps:
            break
        loss.backward()
        W.zero_grad()
        sgd_step([W], lr)
    return losses
```

**l4-b: no gradient zeroing in the loop (zeroed once before it).** Result: fails test 1.

```python
import numpy as np
from autograd import Tensor, cross_entropy, sgd_step


def train_bigram_net(xs, ys, steps, lr, seed):
    W = Tensor(np.random.default_rng(seed).standard_normal((27, 27)))
    losses = []
    W.zero_grad()
    for k in range(steps + 1):
        loss = cross_entropy(W[xs], ys)
        losses.append(loss.item())
        if k == steps:
            break
        loss.backward()
        sgd_step([W], lr)
    return losses
```

**l4-c: legacy RandomState seeding.** Result: fails test 1.

```python
import numpy as np
from autograd import Tensor, cross_entropy, sgd_step


def train_bigram_net(xs, ys, steps, lr, seed):
    W = Tensor(np.random.RandomState(seed).standard_normal((27, 27)))
    losses = []
    for k in range(steps + 1):
        loss = cross_entropy(W[xs], ys)
        losses.append(loss.item())
        if k == steps:
            break
        W.zero_grad()
        loss.backward()
        sgd_step([W], lr)
    return losses
```

**l4-d: one-hot product instead of W[xs] (correct alternative).** Result: SURVIVES.

```python
import numpy as np
from autograd import Tensor, cross_entropy, sgd_step


def train_bigram_net(xs, ys, steps, lr, seed):
    W = Tensor(np.random.default_rng(seed).standard_normal((27, 27)))
    losses = []
    for k in range(steps + 1):
        loss = cross_entropy(Tensor(np.eye(27)[xs]) @ W, ys)
        losses.append(loss.item())
        if k == steps:
            break
        W.zero_grad()
        loss.backward()
        sgd_step([W], lr)
    return losses
```

**l4-e: loss recorded after the step, so the first loss is lost and one extra step runs.** Result: fails test 1.

```python
import numpy as np
from autograd import Tensor, cross_entropy, sgd_step


def train_bigram_net(xs, ys, steps, lr, seed):
    W = Tensor(np.random.default_rng(seed).standard_normal((27, 27)))
    losses = []
    for k in range(steps + 1):
        loss = cross_entropy(W[xs], ys)
        W.zero_grad()
        loss.backward()
        sgd_step([W], lr)
        losses.append(cross_entropy(W[xs], ys).item())
    return losses
```

### l5-three-letters-of-context.json screens.8.widget

**l5-a: slides the context in place (every row aliases one list).** Result: fails test 1.

```python
import numpy as np

INDEX = {c: i for i, c in enumerate(".abcdefghijklmnopqrstuvwxyz")}


def build_dataset(words, block):
    X, Y = [], []
    for w in words:
        context = [0] * block
        for ch in w + ".":
            ix = INDEX[ch]
            X.append(context)
            Y.append(ix)
            context.pop(0)
            context.append(ix)
    return np.array(X), np.array(Y)
```

**l5-b: pads with block - 1 marks.** Result: fails test 1.

```python
import numpy as np

INDEX = {c: i for i, c in enumerate(".abcdefghijklmnopqrstuvwxyz")}


def build_dataset(words, block):
    X, Y = [], []
    for w in words:
        context = [0] * (block - 1)
        for ch in w + ".":
            ix = INDEX[ch]
            X.append(context)
            Y.append(ix)
            context = context[1:] + [ix]
    return np.array(X), np.array(Y)
```

**l5-c: letters from 0, mark at 26.** Result: fails test 1.

```python
import numpy as np

INDEX = {c: i for i, c in enumerate("abcdefghijklmnopqrstuvwxyz.")}


def build_dataset(words, block):
    X, Y = [], []
    for w in words:
        context = [0] * block
        for ch in w + ".":
            ix = INDEX[ch]
            X.append(context)
            Y.append(ix)
            context = context[1:] + [ix]
    return np.array(X), np.array(Y)
```

**l5-d: window over the joined string of all names.** Result: fails test 4.

```python
import numpy as np

INDEX = {c: i for i, c in enumerate(".abcdefghijklmnopqrstuvwxyz")}


def build_dataset(words, block):
    s = "." * block + ".".join(words) + "."
    X, Y = [], []
    for i in range(block, len(s)):
        X.append([INDEX[c] for c in s[i - block:i]])
        Y.append(INDEX[s[i]])
    return np.array(X), np.array(Y)
```

### l6-letters-as-points.json screens.8.widget

**l6-a: joins interleaved (embedding number first, then position).** Result: fails test 1.

```python
import numpy as np


def embed(C, X):
    return C[X].transpose(0, 2, 1).reshape(X.shape[0], -1)


def embed_backward(dE, X, shape):
    dC = np.zeros(shape)
    np.add.at(dC, X, dE.reshape(X.shape[0], X.shape[1], -1))
    return dC
```

**l6-b: backward loops over contexts with fancy +=, dropping repeats inside a context.** Result: fails test 3.

```python
import numpy as np


def embed(C, X):
    return C[X].reshape(X.shape[0], -1)


def embed_backward(dE, X, shape):
    dC = np.zeros(shape)
    for i in range(X.shape[0]):
        dC[X[i]] += dE[i].reshape(X.shape[1], -1)
    return dC
```

**l6-c: np.add.at on flattened indices (correct alternative).** Result: SURVIVES.

```python
import numpy as np


def embed(C, X):
    return C[X].reshape(X.shape[0], -1)


def embed_backward(dE, X, shape):
    dC = np.zeros(shape)
    np.add.at(dC, X.ravel(), dE.reshape(-1, shape[1]))
    return dC
```

**l6-d: contexts indexed in reverse order.** Result: fails test 2.

```python
import numpy as np


def embed(C, X):
    return C[X[:, ::-1]].reshape(X.shape[0], -1)


def embed_backward(dE, X, shape):
    dC = np.zeros(shape)
    np.add.at(dC, X, dE.reshape(X.shape[0], X.shape[1], -1))
    return dC
```

### l7-the-mlp-model.json screens.9.widget

**l7a-a: embeddings indexed by the reversed context.** Result: fails test 1.

```python
import numpy as np


def mlp_forward(params, X):
    E = params["C"][X[:, ::-1]].reshape(X.shape[0], -1)
    h = np.tanh(E @ params["W1"] + params["b1"])
    return h @ params["W2"] + params["b2"]
```

**l7a-b: returns softmax chances, not logits.** Result: fails test 1.

```python
import numpy as np


def mlp_forward(params, X):
    E = params["C"][X].reshape(X.shape[0], -1)
    h = np.tanh(E @ params["W1"] + params["b1"])
    z = h @ params["W2"] + params["b2"]
    e = np.exp(z - z.max(axis=1, keepdims=True))
    return e / e.sum(axis=1, keepdims=True)
```

**l7a-c: hidden bias added after the tanh.** Result: fails test 1.

```python
import numpy as np


def mlp_forward(params, X):
    E = params["C"][X].reshape(X.shape[0], -1)
    h = np.tanh(E @ params["W1"]) + params["b1"]
    return h @ params["W2"] + params["b2"]
```

### l7-the-mlp-model.json screens.10.widget

**l7b-a: softmax normalised over the batch axis.** Result: fails test 1.

```python
import numpy as np


def mlp_dev_loss(params, X, Y):
    Z = mlp_forward(params, X)
    P = np.exp(Z - Z.max(axis=0, keepdims=True))
    P = P / P.sum(axis=0, keepdims=True)
    return float(-np.log(P[np.arange(len(Y)), Y]).mean())
```

**l7b-b: no maximum taken out of the log-sum-exp.** Result: SURVIVES.

```python
import numpy as np


def mlp_dev_loss(params, X, Y):
    Z = mlp_forward(params, X)
    m = Z.max(axis=1, keepdims=True)
    lse = np.log(np.exp(Z).sum(axis=1))
    return float((lse - Z[np.arange(len(Y)), Y]).mean())
```

**l7b-c: log-softmax averaged over every class, not the true one.** Result: fails test 1.

```python
import numpy as np


def mlp_dev_loss(params, X, Y):
    Z = mlp_forward(params, X)
    m = Z.max(axis=1, keepdims=True)
    lse = np.log(np.exp(Z - m).sum(axis=1)) + m[:, 0]
    return float((lse[:, None] - Z).mean())
```

### l8-minibatches-and-rates.json screens.8.widget

**l8-a: gradients zeroed once, before the loop.** Result: fails test 1.

```python
import numpy as np
from autograd import Tensor, cross_entropy, sgd_step


def train_mlp(params, X, Y, steps, lr, seed):
    P = {k: Tensor(np.array(v, dtype=float)) for k, v in params.items()}
    rng = np.random.default_rng(seed)
    losses = []
    for t in P.values():
        t.zero_grad()
    for _ in range(steps):
        ix = rng.integers(0, len(X), 32)
        E = P["C"][X[ix]].reshape(32, -1)
        h = (E @ P["W1"] + P["b1"]).tanh()
        loss = cross_entropy(h @ P["W2"] + P["b2"], Y[ix])
        loss.backward()
        sgd_step(list(P.values()), lr)
        losses.append(loss.item())
    return {k: t.data for k, t in P.items()}, losses
```

**l8-b: batches drawn with rng.choice.** Result: SURVIVES.

```python
import numpy as np
from autograd import Tensor, cross_entropy, sgd_step


def train_mlp(params, X, Y, steps, lr, seed):
    P = {k: Tensor(np.array(v, dtype=float)) for k, v in params.items()}
    rng = np.random.default_rng(seed)
    losses = []
    for _ in range(steps):
        ix = rng.choice(len(X), 32)
        E = P["C"][X[ix]].reshape(32, -1)
        h = (E @ P["W1"] + P["b1"]).tanh()
        loss = cross_entropy(h @ P["W2"] + P["b2"], Y[ix])
        for t in P.values():
            t.zero_grad()
        loss.backward()
        sgd_step(list(P.values()), lr)
        losses.append(loss.item())
    return {k: t.data for k, t in P.items()}, losses
```

**l8-c: zero_grad on W only, not every parameter.** Result: fails test 1.

```python
import numpy as np
from autograd import Tensor, cross_entropy, sgd_step


def train_mlp(params, X, Y, steps, lr, seed):
    P = {k: Tensor(np.array(v, dtype=float)) for k, v in params.items()}
    rng = np.random.default_rng(seed)
    losses = []
    for _ in range(steps):
        ix = rng.integers(0, len(X), 32)
        E = P["C"][X[ix]].reshape(32, -1)
        h = (E @ P["W1"] + P["b1"]).tanh()
        loss = cross_entropy(h @ P["W2"] + P["b2"], Y[ix])
        P['W1'].zero_grad()
        loss.backward()
        sgd_step(list(P.values()), lr)
        losses.append(loss.item())
    return {k: t.data for k, t in P.items()}, losses
```

**l8-d: one fixed batch for the whole run.** Result: fails test 1.

```python
import numpy as np
from autograd import Tensor, cross_entropy, sgd_step


def train_mlp(params, X, Y, steps, lr, seed):
    P = {k: Tensor(np.array(v, dtype=float)) for k, v in params.items()}
    rng = np.random.default_rng(seed)
    losses = []
    ix = rng.integers(0, len(X), 32)
    for _ in range(steps):
        E = P["C"][X[ix]].reshape(32, -1)
        h = (E @ P["W1"] + P["b1"]).tanh()
        loss = cross_entropy(h @ P["W2"] + P["b2"], Y[ix])
        for t in P.values():
            t.zero_grad()
        loss.backward()
        sgd_step(list(P.values()), lr)
        losses.append(loss.item())
    return {k: t.data for k, t in P.items()}, losses
```

### l9-sampling-names.json screens.8.widget

**l9-a: argmax of cumsum > u (no total above u gives the end mark).** Result: fails test 4.

```python
import numpy as np

SYMBOLS = ".abcdefghijklmnopqrstuvwxyz"


def sample_name(prob_fn, rng, max_len=20):
    context = [0, 0, 0]
    name = ""
    while len(name) < max_len:
        p = prob_fn(context)
        u = rng.random()
        ix = int(np.argmax(np.cumsum(p) > u))
        if ix == 0:
            break
        name += SYMBOLS[ix]
        context = context[1:] + [ix]
    return name
```

**l9-b: one u drawn per name.** Result: fails test 1.

```python
import numpy as np

SYMBOLS = ".abcdefghijklmnopqrstuvwxyz"


def sample_name(prob_fn, rng, max_len=20):
    context = [0, 0, 0]
    name = ""
    u = rng.random()
    while len(name) < max_len:
        p = prob_fn(context)
        ix = min(int(np.searchsorted(np.cumsum(p), u, side="right")), 26)
        if ix == 0:
            break
        name += SYMBOLS[ix]
        context = context[1:] + [ix]
    return name
```

**l9-c: length cap off by one (<=).** Result: fails test 3.

```python
import numpy as np

SYMBOLS = ".abcdefghijklmnopqrstuvwxyz"


def sample_name(prob_fn, rng, max_len=20):
    context = [0, 0, 0]
    name = ""
    while len(name) <= max_len:
        p = prob_fn(context)
        u = rng.random()
        ix = min(int(np.searchsorted(np.cumsum(p), u, side="right")), 26)
        if ix == 0:
            break
        name += SYMBOLS[ix]
        context = context[1:] + [ix]
    return name
```

**l9-d: never stops at the end mark (redraws instead).** Result: fails test 1 [IndexError: pop from empty list].

```python
import numpy as np

SYMBOLS = ".abcdefghijklmnopqrstuvwxyz"


def sample_name(prob_fn, rng, max_len=20):
    context = [0, 0, 0]
    name = ""
    while len(name) < max_len:
        p = prob_fn(context)
        u = rng.random()
        ix = min(int(np.searchsorted(np.cumsum(p), u, side="right")), 26)
        if ix == 0:
            continue
        name += SYMBOLS[ix]
        context = context[1:] + [ix]
    return name
```

**l9-e: caps the index at 25.** Result: fails test 4.

```python
import numpy as np

SYMBOLS = ".abcdefghijklmnopqrstuvwxyz"


def sample_name(prob_fn, rng, max_len=20):
    context = [0, 0, 0]
    name = ""
    while len(name) < max_len:
        p = prob_fn(context)
        u = rng.random()
        ix = min(int(np.searchsorted(np.cumsum(p), u, side="right")), 25)
        if ix == 0:
            break
        name += SYMBOLS[ix]
        context = context[1:] + [ix]
    return name
```

**l9-f: rng.choice with p= instead of the course rule.** Result: fails test 1 [AttributeError: 'FixedU' object has no attribute 'choice'].

```python
import numpy as np

SYMBOLS = ".abcdefghijklmnopqrstuvwxyz"


def sample_name(prob_fn, rng, max_len=20):
    context = [0, 0, 0]
    name = ""
    while len(name) < max_len:
        p = prob_fn(context)
        ix = int(rng.choice(27, p=p / p.sum()))
        if ix == 0:
            break
        name += SYMBOLS[ix]
        context = context[1:] + [ix]
    return name
```

### l10-train-dev-test.json screens.8.widget

**l10-a: legacy RandomState permutation.** Result: fails test 2.

```python
import numpy as np


def split_names(words, seed):
    n = len(words)
    perm = np.random.RandomState(seed).permutation(n)
    n1, n2 = int(0.8 * n), int(0.9 * n)
    train = [words[i] for i in perm[:n1]]
    dev = [words[i] for i in perm[n1:n2]]
    test = [words[i] for i in perm[n2:]]
    return train, dev, test
```

**l10-b: shuffles a list of positions with rng.shuffle (equivalent).** Result: SURVIVES.

```python
import numpy as np


def split_names(words, seed):
    n = len(words)
    perm = list(range(n))
    np.random.default_rng(seed).shuffle(perm)
    n1, n2 = int(0.8 * n), int(0.9 * n)
    train = [words[i] for i in perm[:n1]]
    dev = [words[i] for i in perm[n1:n2]]
    test = [words[i] for i in perm[n2:]]
    return train, dev, test
```

**l10-c: shuffles the caller's word list in place.** Result: fails test 2.

```python
import numpy as np


def split_names(words, seed):
    n = len(words)
    np.random.default_rng(seed).shuffle(words)
    n1, n2 = int(0.8 * n), int(0.9 * n)
    train, dev, test = words[:n1], words[n1:n2], words[n2:]
    return train, dev, test
```

**l10-d: dev and test swapped.** Result: fails test 1.

```python
import numpy as np


def split_names(words, seed):
    n = len(words)
    perm = np.random.default_rng(seed).permutation(n)
    n1, n2 = int(0.8 * n), int(0.9 * n)
    train = [words[i] for i in perm[:n1]]
    dev = [words[i] for i in perm[n1:n2]]
    test = [words[i] for i in perm[n2:]]
    return train, test, dev
```

### l11-overfitting.json screens.7.widget

**l11-a: returns (dev, train) in the wrong order.** Result: fails test 4.

```python
import numpy as np


def best_checkpoint(dev_losses, steps):
    best = 0
    for i in range(1, len(dev_losses)):
        if dev_losses[i] < dev_losses[best]:
            best = i
    return steps[best]


def fit_and_gap(train_words, dev_words, steps, seed):
    Xt, Yt = build_dataset(train_words)
    Xd, Yd = build_dataset(dev_words)
    p = train_mlp(course_init(), Xt, Yt, steps, 0.1, seed)
    return full_loss(p, Xd, Yd), full_loss(p, Xt, Yt)
```

**l11-b: np.argmin (correct alternative).** Result: SURVIVES.

```python
import numpy as np


def best_checkpoint(dev_losses, steps):
    return steps[int(np.argmin(dev_losses))]


def fit_and_gap(train_words, dev_words, steps, seed):
    Xt, Yt = build_dataset(train_words)
    Xd, Yd = build_dataset(dev_words)
    p = train_mlp(course_init(), Xt, Yt, steps, 0.1, seed)
    return full_loss(p, Xt, Yt), full_loss(p, Xd, Yd)
```

**l11-c: ignores the seed argument.** Result: fails test 6.

```python
import numpy as np


def best_checkpoint(dev_losses, steps):
    best = 0
    for i in range(1, len(dev_losses)):
        if dev_losses[i] < dev_losses[best]:
            best = i
    return steps[best]


def fit_and_gap(train_words, dev_words, steps, seed):
    Xt, Yt = build_dataset(train_words)
    Xd, Yd = build_dataset(dev_words)
    p = train_mlp(course_init(), Xt, Yt, steps, 0.1, 1)
    return full_loss(p, Xt, Yt), full_loss(p, Xd, Yd)
```

**l11-d: held-out loss on the training names (dev rows built from train_words).** Result: fails test 5.

```python
import numpy as np


def best_checkpoint(dev_losses, steps):
    best = 0
    for i in range(1, len(dev_losses)):
        if dev_losses[i] < dev_losses[best]:
            best = i
    return steps[best]


def fit_and_gap(train_words, dev_words, steps, seed):
    Xt, Yt = build_dataset(train_words)
    Xd, Yd = build_dataset(train_words)
    p = train_mlp(course_init(), Xt, Yt, steps, 0.1, seed)
    return full_loss(p, Xt, Yt), full_loss(p, Xd, Yd)
```

### l12-temperature.json screens.7.widget

**l12-a: maximum over the whole array, not each row.** Result: fails test 3.

```python
import numpy as np


def softmax_t(logits, T):
    z = np.asarray(logits, dtype=float) / T
    z = z - z.max()
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)
```

**l12-b: normalises along axis 0.** Result: fails test 3.

```python
import numpy as np


def softmax_t(logits, T):
    z = np.asarray(logits, dtype=float) / T
    z = z - z.max(axis=-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=0, keepdims=True)
```

**l12-c: maximum taken out before dividing by T (equivalent).** Result: SURVIVES.

```python
import numpy as np


def softmax_t(logits, T):
    z = np.asarray(logits, dtype=float)
    z = (z - z.max(axis=-1, keepdims=True)) / T
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)
```

**l12-d: softmax at T = 1, then chances to the power 1/T (equivalent).** Result: SURVIVES.

```python
import numpy as np


def softmax_t(logits, T):
    z = np.asarray(logits, dtype=float)
    z = z - z.max(axis=-1, keepdims=True)
    e = np.exp(z)
    e = (e / e.sum(axis=-1, keepdims=True)) ** (1 / T)
    return e / e.sum(axis=-1, keepdims=True)
```

### homework-1.json items.0.widget

**hw1a-a: smoothing added after normalising.** Result: fails test 2.

```python
import math
import numpy as np

INDEX = {c: i + 1 for i, c in enumerate("abcdefghijklmnopqrstuvwxyz")}
INDEX["."] = 0


def pairs(ws):
    for w in ws:
        cs = "." + w + "."
        for a, b in zip(cs, cs[1:]):
            yield INDEX[a], INDEX[b]


def best_alpha(train_words, dev_words, alphas):
    N = np.zeros((27, 27))
    for a, b in pairs(train_words):
        N[a, b] += 1
    best = None
    for alpha in alphas:
        R = N.sum(axis=1, keepdims=True)
        M = np.divide(N, R, out=np.zeros_like(N), where=R > 0) + alpha
        rows = M.sum(axis=1, keepdims=True)
        P = np.divide(M, rows, out=np.zeros_like(M), where=rows > 0)
        total, n = 0.0, 0
        for a, b in pairs(dev_words):
            if P[a, b] == 0:
                total = math.inf
                break
            total -= math.log(P[a, b])
            n += 1
        loss = total / n if n and total < math.inf else math.inf
        if best is None or loss < best[1]:
            best = (alpha, loss)
    return (best[0], round(best[1], 4))
```

**hw1a-b: counts without the end mark.** Result: fails test 2.

```python
import math
import numpy as np

INDEX = {c: i + 1 for i, c in enumerate("abcdefghijklmnopqrstuvwxyz")}
INDEX["."] = 0


def pairs(ws):
    for w in ws:
        cs = "." + w
        for a, b in zip(cs, cs[1:]):
            yield INDEX[a], INDEX[b]


def best_alpha(train_words, dev_words, alphas):
    N = np.zeros((27, 27))
    for a, b in pairs(train_words):
        N[a, b] += 1
    best = None
    for alpha in alphas:
        M = N + alpha
        rows = M.sum(axis=1, keepdims=True)
        P = np.divide(M, rows, out=np.zeros_like(M), where=rows > 0)
        total, n = 0.0, 0
        for a, b in pairs(dev_words):
            if P[a, b] == 0:
                total = math.inf
                break
            total -= math.log(P[a, b])
            n += 1
        loss = total / n if n and total < math.inf else math.inf
        if best is None or loss < best[1]:
            best = (alpha, loss)
    return (best[0], round(best[1], 4))
```

**hw1a-c: skips an unseen dev pair.** Result: fails test 2.

```python
import math
import numpy as np

INDEX = {c: i + 1 for i, c in enumerate("abcdefghijklmnopqrstuvwxyz")}
INDEX["."] = 0


def pairs(ws):
    for w in ws:
        cs = "." + w + "."
        for a, b in zip(cs, cs[1:]):
            yield INDEX[a], INDEX[b]


def best_alpha(train_words, dev_words, alphas):
    N = np.zeros((27, 27))
    for a, b in pairs(train_words):
        N[a, b] += 1
    best = None
    for alpha in alphas:
        M = N + alpha
        rows = M.sum(axis=1, keepdims=True)
        P = np.divide(M, rows, out=np.zeros_like(M), where=rows > 0)
        total, n = 0.0, 0
        for a, b in pairs(dev_words):
            if P[a, b] == 0:
                continue
            total -= math.log(P[a, b])
            n += 1
        loss = total / n if n and total < math.inf else math.inf
        if best is None or loss < best[1]:
            best = (alpha, loss)
    return (best[0], round(best[1], 4))
```

**hw1a-d: counts without the start mark.** Result: fails test 2.

```python
import math
import numpy as np

INDEX = {c: i + 1 for i, c in enumerate("abcdefghijklmnopqrstuvwxyz")}
INDEX["."] = 0


def pairs(ws):
    for w in ws:
        cs = w + "."
        for a, b in zip(cs, cs[1:]):
            yield INDEX[a], INDEX[b]


def best_alpha(train_words, dev_words, alphas):
    N = np.zeros((27, 27))
    for a, b in pairs(train_words):
        N[a, b] += 1
    best = None
    for alpha in alphas:
        M = N + alpha
        rows = M.sum(axis=1, keepdims=True)
        P = np.divide(M, rows, out=np.zeros_like(M), where=rows > 0)
        total, n = 0.0, 0
        for a, b in pairs(dev_words):
            if P[a, b] == 0:
                total = math.inf
                break
            total -= math.log(P[a, b])
            n += 1
        loss = total / n if n and total < math.inf else math.inf
        if best is None or loss < best[1]:
            best = (alpha, loss)
    return (best[0], round(best[1], 4))
```

### homework-1.json items.1.widget

**hw1b-a: Counter.most_common (ties by first seen).** Result: fails test 2.

```python
from collections import Counter


def top_start(words):
    c = Counter(w[:2] for w in words if len(w) >= 2)
    return c.most_common(1)[0]
```

**hw1b-b: counts distinct names only.** Result: fails test 3.

```python
def top_start(words):
    counts = {}
    for w in set(words):
        if len(w) >= 2:
            counts[w[:2]] = counts.get(w[:2], 0) + 1
    best = min(counts, key=lambda s: (-counts[s], s))
    return (best, counts[best])
```

### homework-1.json items.6.widget

**hw1p-a: smoothing added after normalising.** Result: fails test 2.

```python
import math
import numpy as np

SYMBOLS = ".abcdefghijklmnopqrstuvwxyz"


def bigram_model(words, alpha):
    N = np.zeros((27, 27))
    for w in words:
        cs = "." + w + "."
        for a, b in zip(cs, cs[1:]):
            N[SYMBOLS.index(a), SYMBOLS.index(b)] += 1
    M = N / N.sum(axis=1, keepdims=True) + alpha
    return M / M.sum(axis=1, keepdims=True)


def avg_nll(P, words):
    total, n = 0.0, 0
    for w in words:
        cs = "." + w + "."
        for a, b in zip(cs, cs[1:]):
            p = P[SYMBOLS.index(a), SYMBOLS.index(b)]
            if p == 0:
                return math.inf
            total -= math.log(p)
            n += 1
    return total / n
```

**hw1p-b: no start mark (both functions).** Result: fails test 2.

```python
import math
import numpy as np

SYMBOLS = ".abcdefghijklmnopqrstuvwxyz"


def bigram_model(words, alpha):
    N = np.zeros((27, 27))
    for w in words:
        cs = w + "."
        for a, b in zip(cs, cs[1:]):
            N[SYMBOLS.index(a), SYMBOLS.index(b)] += 1
    M = N + alpha
    return M / M.sum(axis=1, keepdims=True)


def avg_nll(P, words):
    total, n = 0.0, 0
    for w in words:
        cs = w + "."
        for a, b in zip(cs, cs[1:]):
            p = P[SYMBOLS.index(a), SYMBOLS.index(b)]
            if p == 0:
                return math.inf
            total -= math.log(p)
            n += 1
    return total / n
```

**hw1p-c: average over letters.** Result: fails test 4.

```python
import math
import numpy as np

SYMBOLS = ".abcdefghijklmnopqrstuvwxyz"


def bigram_model(words, alpha):
    N = np.zeros((27, 27))
    for w in words:
        cs = "." + w + "."
        for a, b in zip(cs, cs[1:]):
            N[SYMBOLS.index(a), SYMBOLS.index(b)] += 1
    M = N + alpha
    return M / M.sum(axis=1, keepdims=True)


def avg_nll(P, words):
    total, n = 0.0, 0
    for w in words:
        cs = "." + w + "."
        for a, b in zip(cs, cs[1:]):
            p = P[SYMBOLS.index(a), SYMBOLS.index(b)]
            if p == 0:
                return math.inf
            total -= math.log(p)
            n += 1
    return total / sum(len(w) for w in words)
```

### homework-2.json items.0.widget

**hw2a-a: gradients zeroed once, before the loop.** Result: fails test 5.

```python
import numpy as np
from autograd import Tensor, cross_entropy, sgd_step

INDEX = {c: i for i, c in enumerate(".abcdefghijklmnopqrstuvwxyz")}


def contexts(words, block):
    X, Y = [], []
    for w in words:
        ctx = [0] * block
        for ch in w + ".":
            X.append(ctx)
            Y.append(INDEX[ch])
            ctx = ctx[1:] + [INDEX[ch]]
    return np.array(X), np.array(Y)


def forward(P, X):
    E = P["C"][X].reshape(len(X), -1)
    return (E @ P["W1"] + P["b1"]).tanh() @ P["W2"] + P["b2"]


def block4_run(X, Y, steps, lr, seed):
    g = np.random.default_rng(0)
    P = {"C": Tensor(g.standard_normal((27, 10))),
         "W1": Tensor(g.standard_normal((40, 100)) * (5 / 3) / np.sqrt(40)),
         "b1": Tensor(np.zeros(100)),
         "W2": Tensor(g.standard_normal((100, 27)) * 0.01),
         "b2": Tensor(np.zeros(27))}
    rng = np.random.default_rng(seed)
    for t in P.values():
        t.zero_grad()
    for _ in range(steps):
        ix = rng.integers(0, len(X), 32)
        loss = cross_entropy(forward(P, X[ix]), Y[ix])
        loss.backward()
        sgd_step(list(P.values()), lr)
    return cross_entropy(forward(P, X), Y).item()
```

**hw2a-b: W1 scaled by sqrt(30) as for block 3.** Result: fails test 4.

```python
import numpy as np
from autograd import Tensor, cross_entropy, sgd_step

INDEX = {c: i for i, c in enumerate(".abcdefghijklmnopqrstuvwxyz")}


def contexts(words, block):
    X, Y = [], []
    for w in words:
        ctx = [0] * block
        for ch in w + ".":
            X.append(ctx)
            Y.append(INDEX[ch])
            ctx = ctx[1:] + [INDEX[ch]]
    return np.array(X), np.array(Y)


def forward(P, X):
    E = P["C"][X].reshape(len(X), -1)
    return (E @ P["W1"] + P["b1"]).tanh() @ P["W2"] + P["b2"]


def block4_run(X, Y, steps, lr, seed):
    g = np.random.default_rng(0)
    P = {"C": Tensor(g.standard_normal((27, 10))),
         "W1": Tensor(g.standard_normal((40, 100)) * (5 / 3) / np.sqrt(30)),
         "b1": Tensor(np.zeros(100)),
         "W2": Tensor(g.standard_normal((100, 27)) * 0.01),
         "b2": Tensor(np.zeros(27))}
    rng = np.random.default_rng(seed)
    for _ in range(steps):
        ix = rng.integers(0, len(X), 32)
        loss = cross_entropy(forward(P, X[ix]), Y[ix])
        for t in P.values():
            t.zero_grad()
        loss.backward()
        sgd_step(list(P.values()), lr)
    return cross_entropy(forward(P, X), Y).item()
```

**hw2a-c: embeddings indexed by the reversed context.** Result: fails test 4.

```python
import numpy as np
from autograd import Tensor, cross_entropy, sgd_step

INDEX = {c: i for i, c in enumerate(".abcdefghijklmnopqrstuvwxyz")}


def contexts(words, block):
    X, Y = [], []
    for w in words:
        ctx = [0] * block
        for ch in w + ".":
            X.append(ctx)
            Y.append(INDEX[ch])
            ctx = ctx[1:] + [INDEX[ch]]
    return np.array(X), np.array(Y)


def forward(P, X):
    E = P["C"][X[:, ::-1]].reshape(len(X), -1)
    return (E @ P["W1"] + P["b1"]).tanh() @ P["W2"] + P["b2"]


def block4_run(X, Y, steps, lr, seed):
    g = np.random.default_rng(0)
    P = {"C": Tensor(g.standard_normal((27, 10))),
         "W1": Tensor(g.standard_normal((40, 100)) * (5 / 3) / np.sqrt(40)),
         "b1": Tensor(np.zeros(100)),
         "W2": Tensor(g.standard_normal((100, 27)) * 0.01),
         "b2": Tensor(np.zeros(27))}
    rng = np.random.default_rng(seed)
    for _ in range(steps):
        ix = rng.integers(0, len(X), 32)
        loss = cross_entropy(forward(P, X[ix]), Y[ix])
        for t in P.values():
            t.zero_grad()
        loss.backward()
        sgd_step(list(P.values()), lr)
    return cross_entropy(forward(P, X), Y).item()
```

**hw2a-d: init from the batch seed.** Result: fails test 4.

```python
import numpy as np
from autograd import Tensor, cross_entropy, sgd_step

INDEX = {c: i for i, c in enumerate(".abcdefghijklmnopqrstuvwxyz")}


def contexts(words, block):
    X, Y = [], []
    for w in words:
        ctx = [0] * block
        for ch in w + ".":
            X.append(ctx)
            Y.append(INDEX[ch])
            ctx = ctx[1:] + [INDEX[ch]]
    return np.array(X), np.array(Y)


def forward(P, X):
    E = P["C"][X].reshape(len(X), -1)
    return (E @ P["W1"] + P["b1"]).tanh() @ P["W2"] + P["b2"]


def block4_run(X, Y, steps, lr, seed):
    g = np.random.default_rng(seed)
    P = {"C": Tensor(g.standard_normal((27, 10))),
         "W1": Tensor(g.standard_normal((40, 100)) * (5 / 3) / np.sqrt(40)),
         "b1": Tensor(np.zeros(100)),
         "W2": Tensor(g.standard_normal((100, 27)) * 0.01),
         "b2": Tensor(np.zeros(27))}
    rng = np.random.default_rng(seed)
    for _ in range(steps):
        ix = rng.integers(0, len(X), 32)
        loss = cross_entropy(forward(P, X[ix]), Y[ix])
        for t in P.values():
            t.zero_grad()
        loss.backward()
        sgd_step(list(P.values()), lr)
    return cross_entropy(forward(P, X), Y).item()
```

### homework-2.json items.6.widget

**hw2p-a: softmax normalised over the batch axis.** Result: fails test 4.

```python
import numpy as np


def mlp_forward(params, X):
    E = params["C"][X].reshape(X.shape[0], -1)
    h = np.tanh(E @ params["W1"] + params["b1"])
    return h @ params["W2"] + params["b2"]


def mlp_loss(params, X, Y):
    Z = mlp_forward(params, X)
    P = np.exp(Z - Z.max(axis=0, keepdims=True))
    P = P / P.sum(axis=0, keepdims=True)
    return float(-np.log(P[np.arange(len(Y)), Y]).mean())


def n_params(block, emb, hidden, vocab):
    return vocab * emb + block * emb * hidden + hidden + hidden * vocab + vocab
```

**hw2p-b: n_params leaves out the embedding table.** Result: fails test 1.

```python
import numpy as np


def mlp_forward(params, X):
    E = params["C"][X].reshape(X.shape[0], -1)
    h = np.tanh(E @ params["W1"] + params["b1"])
    return h @ params["W2"] + params["b2"]


def mlp_loss(params, X, Y):
    Z = mlp_forward(params, X)
    m = Z.max(axis=1, keepdims=True)
    lse = np.log(np.exp(Z - m).sum(axis=1)) + m[:, 0]
    return float((lse - Z[np.arange(len(Y)), Y]).mean())


def n_params(block, emb, hidden, vocab):
    return block * emb * hidden + hidden + hidden * vocab + vocab
```

**hw2p-c: no maximum taken out of the log-sum-exp.** Result: SURVIVES.

```python
import numpy as np


def mlp_forward(params, X):
    E = params["C"][X].reshape(X.shape[0], -1)
    h = np.tanh(E @ params["W1"] + params["b1"])
    return h @ params["W2"] + params["b2"]


def mlp_loss(params, X, Y):
    Z = mlp_forward(params, X)
    m = Z.max(axis=1, keepdims=True)
    lse = np.log(np.exp(Z).sum(axis=1))
    return float((lse - Z[np.arange(len(Y)), Y]).mean())


def n_params(block, emb, hidden, vocab):
    return vocab * emb + block * emb * hidden + hidden + hidden * vocab + vocab
```

**hw2p-d: embeddings indexed by the reversed context.** Result: fails test 4.

```python
import numpy as np


def mlp_forward(params, X):
    E = params["C"][X[:, ::-1]].reshape(X.shape[0], -1)
    h = np.tanh(E @ params["W1"] + params["b1"])
    return h @ params["W2"] + params["b2"]


def mlp_loss(params, X, Y):
    Z = mlp_forward(params, X)
    m = Z.max(axis=1, keepdims=True)
    lse = np.log(np.exp(Z - m).sum(axis=1)) + m[:, 0]
    return float((lse - Z[np.arange(len(Y)), Y]).mean())


def n_params(block, emb, hidden, vocab):
    return vocab * emb + block * emb * hidden + hidden + hidden * vocab + vocab
```

### homework-3.json items.0.widget

**hw3a-a: context not reset at each name.** Result: fails test 3.

```python
import math
import numpy as np

INDEX = {c: i for i, c in enumerate(".abcdefghijklmnopqrstuvwxyz")}


def avg_loss(prob_fn, words):
    total, n = 0.0, 0
    context = [0, 0, 0]
    for w in words:
        for ch in w + ".":
            ix = INDEX[ch]
            total -= math.log(prob_fn(context)[ix])
            n += 1
            context = context[1:] + [ix]
    return total / n


def evaluate_and_choose(models, dev, test):
    best = min(models, key=lambda name: avg_loss(models[name], dev))
    if not test:
        return (best, None)
    return (best, round(avg_loss(models[best], test), 4))
```

**hw3a-b: avg_loss without the end mark.** Result: fails test 1.

```python
import math
import numpy as np

INDEX = {c: i for i, c in enumerate(".abcdefghijklmnopqrstuvwxyz")}


def avg_loss(prob_fn, words):
    total, n = 0.0, 0
    for w in words:
        context = [0, 0, 0]
        for ch in w:
            ix = INDEX[ch]
            total -= math.log(prob_fn(context)[ix])
            n += 1
            context = context[1:] + [ix]
    return total / n


def evaluate_and_choose(models, dev, test):
    best = min(models, key=lambda name: avg_loss(models[name], dev))
    if not test:
        return (best, None)
    return (best, round(avg_loss(models[best], test), 4))
```

**hw3a-c: chooses on dev plus test averaged.** Result: fails test 4.

```python
import math
import numpy as np

INDEX = {c: i for i, c in enumerate(".abcdefghijklmnopqrstuvwxyz")}


def avg_loss(prob_fn, words):
    total, n = 0.0, 0
    for w in words:
        context = [0, 0, 0]
        for ch in w + ".":
            ix = INDEX[ch]
            total -= math.log(prob_fn(context)[ix])
            n += 1
            context = context[1:] + [ix]
    return total / n


def evaluate_and_choose(models, dev, test):
    if not test:
        return (min(models, key=lambda name: avg_loss(models[name], dev)), None)
    best = min(models, key=lambda name: avg_loss(models[name], dev) + avg_loss(models[name], test))
    return (best, round(avg_loss(models[best], test), 4))
```

**hw3a-d: learning-rate-sweep analogue: chooses on test, scores dev.** Result: fails test 4.

```python
import math
import numpy as np

INDEX = {c: i for i, c in enumerate(".abcdefghijklmnopqrstuvwxyz")}


def avg_loss(prob_fn, words):
    total, n = 0.0, 0
    for w in words:
        context = [0, 0, 0]
        for ch in w + ".":
            ix = INDEX[ch]
            total -= math.log(prob_fn(context)[ix])
            n += 1
            context = context[1:] + [ix]
    return total / n


def evaluate_and_choose(models, dev, test):
    if not test:
        return (min(models, key=lambda name: avg_loss(models[name], dev)), None)
    best = min(models, key=lambda name: avg_loss(models[name], test))
    return (best, round(avg_loss(models[best], test), 4))
```

### homework-3.json items.1.widget

**hw3b-a: divides the loss by T instead of the logits.** Result: fails test 2.

```python
import numpy as np


def dev_losses_at(temps):
    Z = batch_logits(Xdev)
    out = []
    for T in temps:
        z = Z
        m = z.max(axis=1, keepdims=True)
        lse = np.log(np.exp(z - m).sum(axis=1)) + m[:, 0]
        out.append(round(float((lse - z[np.arange(len(Ydev)), Ydev]).mean() / T), 4))
    return out
```

**hw3b-b: loss averaged over every class.** Result: fails test 1.

```python
import numpy as np


def dev_losses_at(temps):
    Z = batch_logits(Xdev)
    out = []
    for T in temps:
        z = Z / T
        m = z.max(axis=1, keepdims=True)
        lse = np.log(np.exp(z - m).sum(axis=1)) + m[:, 0]
        out.append(round(float((lse[:, None] - z).mean()), 4))
    return out
```

**hw3b-c: log base 2.** Result: fails test 1.

```python
import numpy as np


def dev_losses_at(temps):
    Z = batch_logits(Xdev)
    out = []
    for T in temps:
        z = Z / T
        m = z.max(axis=1, keepdims=True)
        lse = np.log(np.exp(z - m).sum(axis=1)) + m[:, 0]
        out.append(round(float((lse - z[np.arange(len(Ydev)), Ydev]).mean()) / np.log(2), 4))
    return out
```

### homework-3.json items.6.widget

**hw3p-a: temperature as exp(log p / T) (equivalent).** Result: SURVIVES.

```python
import math
import numpy as np

SYMBOLS = ".abcdefghijklmnopqrstuvwxyz"


def sample_names(prob_fn, n, seed, T):
    rng = np.random.default_rng(seed)
    names = []
    for _ in range(n):
        context, name = [0, 0, 0], ""
        while len(name) < 20:
            with np.errstate(divide='ignore'):
                p = np.exp(np.log(np.asarray(prob_fn(context), dtype=float)) / T)
            p = p / p.sum()
            u = rng.random()
            ix = min(int(np.searchsorted(np.cumsum(p), u, side="right")), 26)
            if ix == 0:
                break
            name += SYMBOLS[ix]
            context = context[1:] + [ix]
        names.append(name)
    return names


def dev_loss(prob_fn, words):
    total, count = 0.0, 0
    for w in words:
        context = [0, 0, 0]
        for ch in w + ".":
            ix = SYMBOLS.index(ch)
            total -= math.log(prob_fn(context)[ix])
            count += 1
            context = context[1:] + [ix]
    return total / count
```

**hw3p-b: no rescaling after the power.** Result: fails test 2 [KeyError: 26].

```python
import math
import numpy as np

SYMBOLS = ".abcdefghijklmnopqrstuvwxyz"


def sample_names(prob_fn, n, seed, T):
    rng = np.random.default_rng(seed)
    names = []
    for _ in range(n):
        context, name = [0, 0, 0], ""
        while len(name) < 20:
            p = np.asarray(prob_fn(context), dtype=float) ** (1 / T)
            u = rng.random()
            ix = min(int(np.searchsorted(np.cumsum(p), u, side="right")), 26)
            if ix == 0:
                break
            name += SYMBOLS[ix]
            context = context[1:] + [ix]
        names.append(name)
    return names


def dev_loss(prob_fn, words):
    total, count = 0.0, 0
    for w in words:
        context = [0, 0, 0]
        for ch in w + ".":
            ix = SYMBOLS.index(ch)
            total -= math.log(prob_fn(context)[ix])
            count += 1
            context = context[1:] + [ix]
    return total / count
```

**hw3p-c: dev_loss context not reset at each name.** Result: SURVIVES.

```python
import math
import numpy as np

SYMBOLS = ".abcdefghijklmnopqrstuvwxyz"


def sample_names(prob_fn, n, seed, T):
    rng = np.random.default_rng(seed)
    names = []
    for _ in range(n):
        context, name = [0, 0, 0], ""
        while len(name) < 20:
            p = np.asarray(prob_fn(context), dtype=float) ** (1 / T)
            p = p / p.sum()
            u = rng.random()
            ix = min(int(np.searchsorted(np.cumsum(p), u, side="right")), 26)
            if ix == 0:
                break
            name += SYMBOLS[ix]
            context = context[1:] + [ix]
        names.append(name)
    return names


def dev_loss(prob_fn, words):
    total, count = 0.0, 0
    context = [0, 0, 0]
    for w in words:
        for ch in w + ".":
            ix = SYMBOLS.index(ch)
            total -= math.log(prob_fn(context)[ix])
            count += 1
            context = context[1:] + [ix]
    return total / count
```

**hw3p-d: sampling that never stops at the end mark (redraws).** Result: fails test 1.

```python
import math
import numpy as np

SYMBOLS = ".abcdefghijklmnopqrstuvwxyz"


def sample_names(prob_fn, n, seed, T):
    rng = np.random.default_rng(seed)
    names = []
    for _ in range(n):
        context, name = [0, 0, 0], ""
        while len(name) < 20:
            p = np.asarray(prob_fn(context), dtype=float) ** (1 / T)
            p = p / p.sum()
            u = rng.random()
            ix = min(int(np.searchsorted(np.cumsum(p), u, side="right")), 26)
            if ix == 0:
                continue
            name += SYMBOLS[ix]
            context = context[1:] + [ix]
        names.append(name)
    return names


def dev_loss(prob_fn, words):
    total, count = 0.0, 0
    for w in words:
        context = [0, 0, 0]
        for ch in w + ".":
            ix = SYMBOLS.index(ch)
            total -= math.log(prob_fn(context)[ix])
            count += 1
            context = context[1:] + [ix]
    return total / count
```

## Fix pass

Edits are targeted, by script, to `app/content/courses/makemore/` only; `makemore-mlp.json` and `autograd.py` untouched. Number scripts: L1 376, L2 212, L3 163 checks, all pass.

- l3 "nats a letter" (warning): fixed, with a deviation. The definition is in l3 s0 (first use), not s2: "each next symbol, the end mark included ... all 228,146 pairs"; l3 s4 adds the 22,807 dev symbols. Later uses unchanged.
- l2 s3 derive (note): declined. It is an ordering exercise that applies the info l8 split row by row; cutting lines would change the graded order and remove steps the exercise tests.
- l3 s4 canvas (note): fixed. Point at 2.4514, a second point at 3.2958 (equal chances), caption names training counts scored on dev.
- l3 s8 widget.how (note): fixed, added "Convert before rounding".
- l1 s9 float table (note, real gap): fixed. Test 7 `bigram_counts(['ab']).dtype.kind` equals `'i'`; float table added as a mutant failing test 7; `how` updated.
- homework-1 h5 Gibbs (note): fixed, "By Jensen (info l6)".
- l6 s1 turn and a flip (error): fixed. Now "place the letters differently, yet in both the vowels gather", with mean distances 1.1 and 1.2 (vowels), 1.8 and 2.1 (consonants), recomputed in `makemore-L2-numbers.py`, which also checks that the best rotation or reflection leaves 0.94 of the spread. Run 2 caption "The picture turns" changed to "The layout differs". The 0.44 correlation is not stated: my recompute over the 27 plotted points gave 0.36.
- l7 s6 tanh example, summary.ideas[2], review-2 r-tanh (error): fixed. The tanh lets letters interact; without it each position adds its own fixed vote.
- Bengio sizes (warning): fixed in l7 s0, s2 (here without direct input-to-output weights), both captions, summary.ideas[0] and homework-2 h-perf as "in the style of". The 10, 100 and 27 are now this course's version.
- l5 s3 wrong `pads` (warning): fixed by keeping 233,783 and changing the why to $L + 3$ a name (the pads and letters). No number changed.
- l7 s11 wrong `product` (warning): fixed by keeping 132 and changing the why to "every sector and exchange pair its own row of 4: 33 x 4".
- l8 s6 and review-2 r-batch-noise (warning): fixed. "Five batches in a row range over 0.39 nats" (2.6831 to 2.2918); review-2 "range from 2.29 to 2.68; a gap of 0.24 is well inside that".
- l7 s10 and homework-2 h-perf no-maximum log-sum-exp (warning, real gap): fixed. New test with every logit raised by 1,000 (loss must not change); the no-maximum loss added as a mutant failing it in each widget (test 5 and test 7); `how` updated. Correct alternatives are unaffected: the test only adds overflow.
- l5 s7 explain (note): fixed, "level 1's bigram pairs".
- l6 s5 options[0] (note): fixed, "reads repeats before writing; the last write wins" (kept under the key-length ratio).
- l8 quiz[2] (note): fixed, "by 1 the steps overshoot".
- `representations` L1 2D table (note): declined. A new data file lies outside the course files; the 2D tables remain in the l6 canvas frames, which the `representations` author can read.
- homework-3 h-perf `dev_loss` context (warning, real gap): fixed. Test 8 `round(dev_loss(mlp, dev500[:50]), 4)` equals 2.2016 (the unreset version gives 2.3568); that variant added as a mutant failing test 8; `how` updated.
- l11 s1 feedback and s250 why (note): fixed, "trends upward" and "falls at first; its lowest point is at step 2,000".
- l11 s6 (note): fixed, "about 0.002 apart".
- l11 quiz[2] explain, review-3 r-cure (note): fixed. r-cure's text did not contain the quoted wording; changed to "all 25,626 training names, far more data for its size".
- l10 s2 (note): fixed, one sentence that test losses were quoted as figures only.
- l10 s3 (note): fixed, "This is what the whole course set out to show".
- l9 s4 canvas (note): fixed, caption added to the console state.
- l9 quiz[2] options[2] why (note): fixed, "at or above".
- l12 s8 hints[1] (note): fixed, "a chance of 1% becomes about 0.01%".
- Whole course strict coverage (note): deferred. Predates the rule; to be done before the next level.
