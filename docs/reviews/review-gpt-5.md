# gpt level 5 (Hardware and precision): second-reader findings

Scope: `app/content/courses/gpt/` l17-waiting-for-memory, l18-fewer-bits, l19-what-fits, l20-the-kv-cache, review-5, homework-5 (performance task `memory_plan`), problems-5; `app/content/data/ai/gpt_ops_l5.py`; `docs/reports/gpt-L5-numbers.py`; at `e5184138`. Context read: `docs/briefs/gpt.md` Level 5, `docs/reports/gpt-L5.md`, `docs/reports/gpt-L4.md`, `numerics` l1 (float32 near 20,000, epsilon), `docs/AUTHORING.md` section 9, `CLAUDE.md` Conventions.
Method, no browser: (1) precision: an independent exact rounder (`fractions.Fraction`, IEEE round to nearest even with subnormals and overflow, any width) against `to_bf16` on the stated values, on edge cases (ties at 1 + 2^-8 and 1 + 3 x 2^-8, 255 to 259, the bf16 maximum 3.3895e38 and the values between it and the overflow threshold, float32's maximum, normals 2^-126, subnormals down to 2^-133 and below, 0, -0, ±inf, NaN and NaN payloads) and on 200,000 random float32 bit patterns; NumPy's `float16` and `round_bits(x, 11, 15)` against the same rounder on 200,000 values in four ranges; `round_bits(x, 8, 127)` against `to_bf16` on 100,000 normal float32 values; stalled totals, the float32 master copy, the 9p notional, loss scaling, all recomputed; (2) hardware: every roofline, memory, cache and decode figure recomputed by hand, every claim read for care, a grep for vendors, products and prices; `decode_step` against `gpt_ops_l2.forward_logits` on the one- and two-block weights, `generate_cached` against `sample_text` on 1,080 cases (60 seeds, temperatures 1, 0.7 and 0, three prompts, 45 characters past the window), the l20 widget's solution against `sample_text` on 600; (3) the number script through `run-number-scripts.mjs --only gpt-L5` (1 of 1 passed, 5 s) and directly with `ZQ_NUMBERS_STRICT=1` (273 of 273, 0 uncovered, 14 literals), read for fiat and dead branches; (4) `grade-all.mjs --file <f> --code --strict-feedback --local-cdn <pkgs>` on each of the 7 files alone (0 failures each); 44 own wrong solutions graded by the app's Pyodide runner through `tools/code-runner.mjs` (appendix); `same-course-reuse.mjs --all` (no error lines; nothing for level 5); (5) every stated number recomputed, every distractor read against its `why`, tolerances checked for overlap, `voice-scan.py 35` on the seven files (0 over 35 words, 0 explanations over three sentences), and a spelling, em-dash and exclamation scan (nothing).
Format: `path | screen/item | severity | what is wrong | fix`. Severity: error = wrong number, false claim or wrong grading; warning = weak explanation, teaching gap or a test gap that lets a taught bug pass; note = style, script or minor wording.

Counts: 2 errors, 7 warnings, 15 notes. No module error.

## Module `gpt_ops_l5.py` (v1.0)

Verdict: correct on every value any widget, lesson or script uses; nothing to change in a frozen file. Three notes for whoever imports it next.

- Rounding: `to_bf16` equals the exact rounder of `float32(x)` on every edge case and on all 200,000 random float32 bit patterns except NaN payloads (below). Ties go to even (1 + 2^-8 to 1, 1 + 3 x 2^-8 to 1.015625, 257 to 256, 259 to 260); 3.39e38 and 3.3961e38 go to the maximum 3.3895e38; 3.4e38, float32's maximum and 1e39 go to inf; subnormals round correctly (1.5 x 2^-134 to 2^-133, 2^-134 to 0); ±0 and ±inf keep their sign. `round_bits(x, 8, 127)` equals `to_bf16` on all 100,000 normal float32 values. `to_fp16` (NumPy) equals the exact rounder on all 200,000 values, subnormals included; `round_bits(x, 11, 15)` equals it on every normal value, overflow included (65,519 to 65,504; ±65,520 to ±inf).
- Format facts confirmed: bf16 epsilon 2^-7, largest 3.3895e38, smallest normal 1.1755e-38, smallest subnormal 9.18e-41; fp16 epsilon 2^-10, largest 65,504, smallest normal 6.1035e-5, smallest subnormal 5.96e-8; 2e-8 rounds to 0 in fp16 (below half of 5.96e-8) and 8.192e-5 is normal.
- KV cache: `decode_step` agrees with `forward_logits` to 1.4e-14 (one block) and 1.8e-14 (two blocks, so "any number of blocks" holds); `generate_cached` equals `sample_text` in all 1,080 cases, temperature 0 included.

- app/content/data/ai/gpt_ops_l5.py | `to_bf16` | note | The docstring says "the bf16 value nearest to x". It is the nearest bf16 to `float32(x)`: a float64 input that is not a float32 is rounded twice. `to_bf16(1 + 2**-8 + 2**-30)` is 1.0; the nearest bf16 is 1.0078125, which `round_bits(x, 8, 127)` returns, so the "two methods" disagree off float32 values. No stated value is affected (every one is float32-exact or far from a tie). | In a later version: "nearest bf16 to float32(x), as hardware converts". Callers that need float64 inputs rounded once use `round_bits(x, 8, 127)`.
- app/content/data/ai/gpt_ops_l5.py | `to_bf16` | note | NaN payloads are not special-cased: the carry from adding 0x7FFF turns 0x7F800001 into inf, 0xFF800001 into -inf and 0x7FFFFFFF into -0.0. Python's `float('nan')`, `np.nan` and arithmetic NaNs are canonical (0x7FC00000) and survive, so no widget reaches it. | A later version starts with `if x != x: return x`.
- app/content/data/ai/gpt_ops_l5.py | `round_bits` | note | Subnormals are not modelled (documented), so `round_bits(2e-8, 11, 15)` is 2.0e-8 where fp16 gives 0: the very underflow l18's loss-scaling screen teaches. The script rightly uses `to_fp16` for that claim. | One line in the next brief that imports the module: fp16 underflow goes through `to_fp16`, never `round_bits`.

## Lessons

- app/content/courses/gpt/l17-waiting-for-memory.json | screens[9] explain | error | "Storing the returns as float32 nearly halves it." Each return is multiplied by its own float64 weight (16 bytes a pair), so float32 returns alone make 12 bytes a pair: 0.24 s, a quarter saved. Halving needs both arrays in float32 (8 bytes, 0.16 s, the screen's own 'half' distractor). | "Storing returns and weights in float32 halves it, to 0.16 s; a faster core does nothing."
- app/content/courses/gpt/l17-waiting-for-memory.json | screens[9] explain | warning | "A Python loop over a list is slower still: ... a 24-byte object behind an 8-byte pointer, 32 bytes against an array's 8." The sentence implies the loop is slow for want of bandwidth (4 times the bytes, about 1.3 s). A CPython loop is bound by per-element interpreter overhead: 50 to 200 ns an element (over 200 ns measured here for a multiply-add over two lists of NumPy scalars), about 100 times the byte cost. It is screen 7's fixed cost, paid once per element. | "A Python loop is slower still, but not for want of bandwidth: each element pays tens of nanoseconds of interpreter overhead, screen 7's fixed cost, a billion times."
- app/content/courses/gpt/l17-waiting-for-memory.json | screens[3] explain | note | "Large matmuls, the bulk of training, reach the peak." The roof is an upper bound; real kernels reach a fraction of it. | "...can approach the peak."
- app/content/courses/gpt/l18-fewer-bits.json | screens[8] (loss scaling) | warning | Only the underflow half of loss scaling is taught. The brief and the level's own range screen make overflow the other fp16 hazard: too large an $S$ pushes gradients past 65,504 to infinity, which is why trainers pick $S$ dynamically. Nothing in l18, the review, homework or problems says so. | Add to the explain: "Too large an $S$ overflows past 65,504, so trainers check for infinities, skip that step and halve $S$."
- app/content/courses/gpt/l18-fewer-bits.json | screens[4] tests | warning | `fp32_sum_to_bf16` that never rounds to bf16 at the end passes all 9 tests, because 1,000 is a bf16 number. The taught step "rounded once at the end" is untested. | Add `fp32_sum_to_bf16([1.0] * 1001)` expecting 1000.0 (1,001 rounds to 1,000 in bf16, where the gap is 4).
- app/content/courses/gpt/l18-fewer-bits.json | screens[4] tests | note | A float64 accumulator also passes (appendix); it is a defensible fix, but the function is named for float32. | If wanted: `fp32_sum_to_bf16([1.0, 2**-8] + [2**-25] * 4)` expects 1.0 (float32 loses the four 2^-25; float64 keeps them and lands above the tie at 1.0078125).
- app/content/courses/gpt/l19-what-fits.json | screens[1] option 'six' why | warning | "That counts the bf16 weights, gradients and one float32 copy": 2 + 2 + 4 = 8, not 6. The number script "covers" 6 as 2 + 2 + 2, which matches no stated slip. | "That counts the bf16 weights and the float32 master copy, 2 + 4. Gradients and Adam's two moments add 10."
- app/content/courses/gpt/l19-what-fits.json | screens[11] feedback.correct, explain | note | "152 GB fits on two 80 GB chips" holds only if the state is split across the two (sharded); a full copy on each chip, as plain data parallelism keeps, does not fit. problems-5 says "split evenly"; this screen does not. | "...two 80 GB chips if the state is split between them, with 8 GB to spare."
- app/content/courses/gpt/l20-the-kv-cache.json | screens[11] prose | warning | The 7B-like model was introduced at screen 7 as serving sequences of 4,096 tokens, and screen 5 has just taught that a model has a hard position limit. Screen 11 runs the same model to 32,768 tokens with no word on its context. | "An analyst keeps one long conversation with a 7B-like model whose context runs to 32,768 tokens."
- app/content/courses/gpt/l20-the-kv-cache.json | screens[8] option 'quad' why | note | "the $T^2$ is the attention scores, never stored": l19 screen 5 stores exactly those weights (`att`, 128 floats a token) for the backward pass. | "...the attention scores, which decoding never caches."
- app/content/courses/gpt/l20-the-kv-cache.json | screens[2] feedback.correct | note | "caching them changes no number" sits beside "agree to about $10^{-14}$" in the explain and the 'approx' line. | "...changes no number in exact arithmetic."
- app/content/courses/gpt/l20-the-kv-cache.json | screens[8], screens[10] | note | Two careful-claim gaps on attention. (a) $2LdTb$ assumes every head keeps its own keys and values; many large models share them across groups of heads, with caches several times smaller. (b) Batching amortises the weight read but not the cache read: each sequence reads its own cache, so attention over the cache stays at an intensity of about 1 at any batch. Neither is false as written; both are what a reader will meet next. | (a) One sentence on screen 8: "Models that share keys and values across heads divide this by the sharing." (b) One clause on screen 10 or review-5 items[2]: "Batching shares the weight read, not the cache read."

## Review, homework and problems

- app/content/courses/gpt/homework-5.json | items[3] model answer, Precision | error | "In 8 bits the weights are 70 GB: twice the room for the cache." The machine holds 160 GB: 160 - 70 = 90 GB for the cache against 20 GB in bf16, 4.5 times the room (about 34,000 tokens at 2,621,440 bytes each, against 7,600). The speed claim (about 94 tokens a second) is right. | "In 8 bits the weights are 70 GB: 90 GB for the cache, about 34,000 tokens, and about twice the speed, near 94 tokens a second."
- app/content/courses/gpt/homework-5.json | items[3] model answer, Bandwidth | note | "Split over two chips ... 140 GB take about 21 ms" assumes each chip holds half of every layer and both read at once. Split by layers, a batch-1 token reads one chip after the other: about 42 ms, 24 tokens a second. | "Split so that both chips read their half of every layer at once, 140 GB take about 21 ms."
- app/content/courses/gpt/homework-5.json | items[0] prose | warning | The prose lists `master` as a config key and asks for `weights`, `grads`, `optimizer`, `kv_cache`, but never says which key holds the master copy. Filing it under `weights` (the copy is a copy of the weights) fails test 3 with no hint before the feedback. The report says "the prose says which bytes go where"; only the test-3 feedback does. | Add to the question: "`optimizer` counts Adam's two moments and the master copy."
- app/content/courses/gpt/homework-5.json | items[0] tests | warning | `context` equals `T` in all three configurations, so a cache sized with `config["T"]` passes all 8 tests (appendix). The brief's "more tests than examples" is met, but the one key that separates the cache from the model's limit is never varied. | Add `memory_plan({**SEVEN, 'context': 1000}, 'infer')['kv_cache']` expecting 524288000.
- app/content/courses/gpt/homework-5.json | items[0] question | note | Activations are left out of the plan without a word, after l19 taught "activations come on top" as the trap's twin. | "...(activations are left out: they depend on the batch, not the parameters)."
- app/content/courses/gpt/homework-5.json | items[1] widget.how | note | "Six test ties": 65,519 is not a tie (the midpoint between 65,504 and 65,536 is 65,520). Five of the first six are ties. | "Five test ties ... and the largest fp16."
- app/content/courses/gpt/homework-5.json | items[1] tests | note | No negative overflow: a solution that rounds `frexp(x)` without `abs` and returns `y` unsigned rounds every negative correctly (floor plus the tie rule is symmetric) but never overflows one, and passes (appendix). | Add `to_fp16(-65520) == -math.inf`.
- app/content/courses/gpt/review-5.json, problems-5.json | all items | (no finding) | Every number recomputed (170.7, ridge 300 and 240, 2.71875, 65,520 to infinity, 0.5, 208, 3 GiB, 82.5; 26, 2.46, 14.23, 70.3; 16, 48, 2 chips, 7; 0.03125, 6.03125, 56.25%, 6.03125); every distractor matches its `why`; no tolerance overlaps. | None.

## Number script (`docs/reports/gpt-L5-numbers.py`)

- docs/reports/gpt-L5-numbers.py | review block, `for name, cfg in [...]: pass` | note | A dead loop. | Delete it.
- docs/reports/gpt-L5-numbers.py | throughout | note | (a) Many `two(...)` calls compare one computation with the stated literal (7B 14, 112, 1,120, 544, 35, 152, 24, 48, 208, 300, 82.5, 0.03125), so those figures are computed once, not twice. The arithmetic is trivial and right, so this is form, not substance. (b) Three claims are fiat: `0.125 / 4 < 0.05` ("a few per cent", covers nothing); `4.24 / 4 < 1.1` "covers" 0.25; `2 + 2 + 2 == 6` "covers" l19's option 6, whose why says 2 + 2 + 4. (c) The two errors above and the l19 why are prose claims the script never checks. | (a) Give the second route as the product written out, or the module function. (b) Replace with a real computation (a 4-bit scale of 16 bits per 128 weights: 16 / (4 x 128) = 3.1%). (c) Add checks for "twice the room" (90 / 20), "nearly halves" (12 / 16) and the option-6 sums.

## Hardware claims (no finding beyond those above)

Every hardware figure is round and labelled hypothetical (the 1,000 TFLOP/s and 3.3 TB/s chip, a second chip of 2,000, chips of 400 and 2, 600 and 2, 2 TB/s, 80 GB and 40 GB chips, a 5 µs start-up cost, a 50 GB/s and 100 GFLOP/s laptop). No vendor, product or price is named; £ appears only for the notional and the tick price. The one real measurement is the learner's browser, never graded on speed. Every roofline, memory and cache figure was recomputed: 10.2 µs against 0.034; ridge 303; $n/3$ at 128, 512, 1,024, 2,048, 4,096; 0.9995; 140.8; 62.1 and a batch of 356; 4.24 ms and 236 a second; the 4 by 4 matmul's 0.000128 and 0.029 ns; 165; 0.32 and 0.02 s; 14, 112, 140, 1,120 GB; 576,544 and 2,887,680 bytes (705 floats a token, row by row); 68, 544 GB and 7 chips; 35 GB; 152 GB; 528 positions; 16,384, 37,748,736 (36 MiB), 2 GiB and 32 GiB; 4.89 ms and 204 a second; 16 GiB and 2.23 times; 36,864 bytes a token; the longform's 2,621,440 bytes a token, 7,600 tokens, 21 ms, 47 and 94 a second, 28 s for 1,300 tokens.

## Every file, `grade-all --strict-feedback`

l17 (10 widgets, 1 code), l18 (12, 1), l19 (14, 1), l20 (13, 2), review-5 (10, 0), homework-5 (2 plus 2 code), problems-5 (12 parts): 0 failures each.

## Appendix: reviewer wrong solutions

Each source is the widget's own solution with the edit named, graded by `tools/code-runner.mjs` (the page's harness, the local Pyodide, the page's time limits) through a scratch harness, `scratchpad/rvg5/runmut.mjs`. The result is the first hidden test it fails, or SURVIVES. 44 sources: 36 fail a test and 8 survive. Of the survivors, 5 are correct alternatives or probes (marked) and 3 are real bugs: l18 screens[4] item 7 (no final rounding), homework-5 items[0] item 5 (cache at `T`), homework-5 items[1] item 5 (negative overflow). The brief's list maps as follows. bf16 by truncation is l18 item 1; ties rounded up are l18 item 2 and homework items[1] item 1; fp16 overflow not detected is homework items[1] items 2 and 3; Adam's bytes wrong are l19 items 2 and 3 and homework items[0] item 3; the KV cache without the factor 2 or the layer count is l20 screens[9] items 1 and 2 and homework items[0] item 4; `memory_plan` without gradients is homework items[0] item 1. The task has no activation term by design, so a plan "forgetting activations" is what it asks for; adding one fails test 1 (item 9).

### l17-waiting-for-memory.json screens[5] `matmul_intensity` / `bound` / `measure_gflops`
1. bytes not multiplied by bytes_per (numbers, not bytes): fails test 1
```python
import time

import numpy as np


def matmul_intensity(m, n, k, bytes_per):
    flops = 2 * m * n * k
    moved = m * k + k * n + m * n
    return flops / moved


def bound(intensity, peak_flops, bandwidth):
    return "memory" if intensity < peak_flops / bandwidth else "compute"


def measure_gflops(n):
    rng = np.random.default_rng(0)
    a, b = rng.random((n, n)), rng.random((n, n))
    reps, t0 = 0, time.perf_counter()
    while True:
        a @ b
        reps += 1
        t = time.perf_counter() - t0
        if t >= 0.05:
            return 2 * n ** 3 * reps / t / 1e9
```
2. only the weight matrix counted as moved: fails test 1
```python
import time

import numpy as np


def matmul_intensity(m, n, k, bytes_per):
    flops = 2 * m * n * k
    moved = k * n * bytes_per
    return flops / moved


def bound(intensity, peak_flops, bandwidth):
    return "memory" if intensity < peak_flops / bandwidth else "compute"


def measure_gflops(n):
    rng = np.random.default_rng(0)
    a, b = rng.random((n, n)), rng.random((n, n))
    reps, t0 = 0, time.perf_counter()
    while True:
        a @ b
        reps += 1
        t = time.perf_counter() - t0
        if t >= 0.05:
            return 2 * n ** 3 * reps / t / 1e9
```
3. ridge as peak times bandwidth: fails test 6
```python
import time

import numpy as np


def matmul_intensity(m, n, k, bytes_per):
    flops = 2 * m * n * k
    moved = (m * k + k * n + m * n) * bytes_per
    return flops / moved


def bound(intensity, peak_flops, bandwidth):
    return "memory" if intensity < peak_flops * bandwidth else "compute"


def measure_gflops(n):
    rng = np.random.default_rng(0)
    a, b = rng.random((n, n)), rng.random((n, n))
    reps, t0 = 0, time.perf_counter()
    while True:
        a @ b
        reps += 1
        t = time.perf_counter() - t0
        if t >= 0.05:
            return 2 * n ** 3 * reps / t / 1e9
```
4. measure_gflops returns an int: fails test 9
```python
import time

import numpy as np


def matmul_intensity(m, n, k, bytes_per):
    flops = 2 * m * n * k
    moved = (m * k + k * n + m * n) * bytes_per
    return flops / moved


def bound(intensity, peak_flops, bandwidth):
    return "memory" if intensity < peak_flops / bandwidth else "compute"


def measure_gflops(n):
    rng = np.random.default_rng(0)
    a, b = rng.random((n, n)), rng.random((n, n))
    reps, t0 = 0, time.perf_counter()
    while True:
        a @ b
        reps += 1
        t = time.perf_counter() - t0
        if t >= 0.05:
            return int(2 * n ** 3 * reps / t / 1e9) + 1
```
5. measure_gflops returns a constant 2.1 (probe: speed is never graded): SURVIVES (probe: speed is never graded, by design)
```python
import time

import numpy as np


def matmul_intensity(m, n, k, bytes_per):
    flops = 2 * m * n * k
    moved = (m * k + k * n + m * n) * bytes_per
    return flops / moved


def bound(intensity, peak_flops, bandwidth):
    return "memory" if intensity < peak_flops / bandwidth else "compute"


def measure_gflops(n):
    return 2.1
    rng = np.random.default_rng(0)
    a, b = rng.random((n, n)), rng.random((n, n))
    reps, t0 = 0, time.perf_counter()
    while True:
        a @ b
        reps += 1
        t = time.perf_counter() - t0
        if t >= 0.05:
            return 2 * n ** 3 * reps / t / 1e9
```

### l18-fewer-bits.json screens[4] `to_bf16` / `bf16_sum` / `fp32_sum_to_bf16`
1. bf16 by truncation: fails test 3
```python
import numpy as np


def to_bf16(x):
    bits = int(np.array(x, dtype=np.float32).view(np.uint32))
    bits = bits & 0xFFFF0000
    return float(np.array(bits, dtype=np.uint32).view(np.float32))


def bf16_sum(xs):
    total = 0.0
    for x in xs:
        total = to_bf16(total + x)
    return total


def fp32_sum_to_bf16(xs):
    total = np.float32(0.0)
    for x in xs:
        total = np.float32(total + np.float32(x))
    return to_bf16(float(total))
```
2. tie bit read from bit 15 (ties always up): fails test 2
```python
import numpy as np


def to_bf16(x):
    bits = int(np.array(x, dtype=np.float32).view(np.uint32))
    bits = (bits + 0x7FFF + ((bits >> 15) & 1)) & 0xFFFF0000
    return float(np.array(bits, dtype=np.uint32).view(np.float32))


def bf16_sum(xs):
    total = 0.0
    for x in xs:
        total = to_bf16(total + x)
    return total


def fp32_sum_to_bf16(xs):
    total = np.float32(0.0)
    for x in xs:
        total = np.float32(total + np.float32(x))
    return to_bf16(float(total))
```
3. tie bit read from bit 0 (ties always down): fails test 3
```python
import numpy as np


def to_bf16(x):
    bits = int(np.array(x, dtype=np.float32).view(np.uint32))
    bits = (bits + 0x7FFF + (bits & 1)) & 0xFFFF0000
    return float(np.array(bits, dtype=np.uint32).view(np.float32))


def bf16_sum(xs):
    total = 0.0
    for x in xs:
        total = to_bf16(total + x)
    return total


def fp32_sum_to_bf16(xs):
    total = np.float32(0.0)
    for x in xs:
        total = np.float32(total + np.float32(x))
    return to_bf16(float(total))
```
4. rounds through np.float16 instead of bf16: fails test 2
```python
import numpy as np


def to_bf16(x):
    return float(np.float16(x))


def bf16_sum(xs):
    total = 0.0
    for x in xs:
        total = to_bf16(total + x)
    return total


def fp32_sum_to_bf16(xs):
    total = np.float32(0.0)
    for x in xs:
        total = np.float32(total + np.float32(x))
    return to_bf16(float(total))
```
5. sign dropped (abs before the bits): fails test 5
```python
import numpy as np


def to_bf16(x):
    bits = int(np.array(abs(x), dtype=np.float32).view(np.uint32))
    bits = (bits + 0x7FFF + ((bits >> 16) & 1)) & 0xFFFF0000
    return float(np.array(bits, dtype=np.uint32).view(np.float32))


def bf16_sum(xs):
    total = 0.0
    for x in xs:
        total = to_bf16(total + x)
    return total


def fp32_sum_to_bf16(xs):
    total = np.float32(0.0)
    for x in xs:
        total = np.float32(total + np.float32(x))
    return to_bf16(float(total))
```
6. bf16_sum rounds each addend, not the total: fails test 6
```python
import numpy as np


def to_bf16(x):
    bits = int(np.array(x, dtype=np.float32).view(np.uint32))
    bits = (bits + 0x7FFF + ((bits >> 16) & 1)) & 0xFFFF0000
    return float(np.array(bits, dtype=np.uint32).view(np.float32))


def bf16_sum(xs):
    total = 0.0
    for x in xs:
        total = total + to_bf16(x)
    return total


def fp32_sum_to_bf16(xs):
    total = np.float32(0.0)
    for x in xs:
        total = np.float32(total + np.float32(x))
    return to_bf16(float(total))
```
7. fp32_sum_to_bf16 never rounds to bf16 at the end: SURVIVES
```python
import numpy as np


def to_bf16(x):
    bits = int(np.array(x, dtype=np.float32).view(np.uint32))
    bits = (bits + 0x7FFF + ((bits >> 16) & 1)) & 0xFFFF0000
    return float(np.array(bits, dtype=np.uint32).view(np.float32))


def bf16_sum(xs):
    total = 0.0
    for x in xs:
        total = to_bf16(total + x)
    return total


def fp32_sum_to_bf16(xs):
    total = np.float32(0.0)
    for x in xs:
        total = np.float32(total + np.float32(x))
    return float(total)
```
8. fp32_sum_to_bf16 accumulates in float64: SURVIVES (a float64 accumulator: a defensible fix, but not the float32 one the name says)
```python
import numpy as np


def to_bf16(x):
    bits = int(np.array(x, dtype=np.float32).view(np.uint32))
    bits = (bits + 0x7FFF + ((bits >> 16) & 1)) & 0xFFFF0000
    return float(np.array(bits, dtype=np.uint32).view(np.float32))


def bf16_sum(xs):
    total = 0.0
    for x in xs:
        total = to_bf16(total + x)
    return total


def fp32_sum_to_bf16(xs):
    total = 0.0
    for x in xs:
        total = total + x
    return to_bf16(float(total))
```

### l19-what-fits.json screens[6] `training_bytes` / `inference_bytes`
1. training_bytes leaves out gradients: fails test 1
```python
def training_bytes(N, bytes_weights, bytes_grads, bytes_optimizer, master):
    return N * (bytes_weights + bytes_optimizer + master)


def inference_bytes(N, bytes_per, kv_bytes):
    return N * bytes_per + kv_bytes
```
2. Adam state counted per moment (bytes_optimizer doubled): fails test 1
```python
def training_bytes(N, bytes_weights, bytes_grads, bytes_optimizer, master):
    return N * (bytes_weights + bytes_grads + 2 * bytes_optimizer + master)


def inference_bytes(N, bytes_per, kv_bytes):
    return N * bytes_per + kv_bytes
```
3. the 16-bytes rule hard-coded: fails test 1
```python
def training_bytes(N, bytes_weights, bytes_grads, bytes_optimizer, master):
    return N * 16


def inference_bytes(N, bytes_per, kv_bytes):
    return N * bytes_per + kv_bytes
```
4. inference_bytes truncates bytes_per to a whole byte: fails test 6
```python
def training_bytes(N, bytes_weights, bytes_grads, bytes_optimizer, master):
    return N * (bytes_weights + bytes_grads + bytes_optimizer + master)


def inference_bytes(N, bytes_per, kv_bytes):
    return N * int(bytes_per) + kv_bytes
```

### l20-the-kv-cache.json screens[3] `decode_step` / `generate_cached`
1. scores scaled by sqrt(32) (width) not sqrt(8) (head): fails test 1
```python
import numpy as np


def new_cache():
    return {"k": np.zeros((4, 0, 8)), "v": np.zeros((4, 0, 8)), "pos": 0}


def decode_step(W, cache, token):
    x = W["wte"][token] + W["wpe"][cache["pos"]]
    qkv = ln(x, W["h0.ln1_g"], W["h0.ln1_b"]) @ W["h0.qkv_w"] + W["h0.qkv_b"]
    q, k, v = (qkv[j * 32:(j + 1) * 32].reshape(4, 1, 8) for j in range(3))
    cache["k"] = np.concatenate([cache["k"], k], axis=1)
    cache["v"] = np.concatenate([cache["v"], v], axis=1)
    s = q @ cache["k"].transpose(0, 2, 1) / np.sqrt(32)
    a = np.exp(s - s.max(-1, keepdims=True))
    a = a / a.sum(-1, keepdims=True)
    x = x + (a @ cache["v"]).reshape(32) @ W["h0.proj_w"] + W["h0.proj_b"]
    h = np.maximum(ln(x, W["h0.ln2_g"], W["h0.ln2_b"]) @ W["h0.fc_w"] + W["h0.fc_b"], 0)
    x = x + h @ W["h0.out_w"] + W["h0.out_b"]
    cache["pos"] += 1
    return ln(x, W["lnf_g"], W["lnf_b"]) @ W["head_w"] + W["head_b"]


def generate_cached(W, prompt, n, seed):
    rng = np.random.default_rng(seed)
    ids = encode(prompt)
    cache = new_cache()
    for t in ids[-32:]:
        z = decode_step(W, cache, t)
    for _ in range(n):
        p = np.exp(z - z.max())
        ids.append(int(rng.choice(65, p=p / p.sum())))
        if cache["pos"] == 32:
            cache = new_cache()
            for t in ids[-32:]:
                z = decode_step(W, cache, t)
        else:
            z = decode_step(W, cache, ids[-1])
    return decode(ids)
```
2. attends over the old cache before appending its own key and value: fails test 1
```python
import numpy as np


def new_cache():
    return {"k": np.zeros((4, 0, 8)), "v": np.zeros((4, 0, 8)), "pos": 0}


def decode_step(W, cache, token):
    x = W["wte"][token] + W["wpe"][cache["pos"]]
    qkv = ln(x, W["h0.ln1_g"], W["h0.ln1_b"]) @ W["h0.qkv_w"] + W["h0.qkv_b"]
    q, k, v = (qkv[j * 32:(j + 1) * 32].reshape(4, 1, 8) for j in range(3))
    K, V = (cache["k"], cache["v"]) if cache["pos"] else (k, v)
    s = q @ K.transpose(0, 2, 1) / np.sqrt(8)
    a = np.exp(s - s.max(-1, keepdims=True))
    a = a / a.sum(-1, keepdims=True)
    x = x + (a @ V).reshape(32) @ W["h0.proj_w"] + W["h0.proj_b"]
    cache["k"] = np.concatenate([cache["k"], k], axis=1)
    cache["v"] = np.concatenate([cache["v"], v], axis=1)
    h = np.maximum(ln(x, W["h0.ln2_g"], W["h0.ln2_b"]) @ W["h0.fc_w"] + W["h0.fc_b"], 0)
    x = x + h @ W["h0.out_w"] + W["h0.out_b"]
    cache["pos"] += 1
    return ln(x, W["lnf_g"], W["lnf_b"]) @ W["head_w"] + W["head_b"]


def generate_cached(W, prompt, n, seed):
    rng = np.random.default_rng(seed)
    ids = encode(prompt)
    cache = new_cache()
    for t in ids[-32:]:
        z = decode_step(W, cache, t)
    for _ in range(n):
        p = np.exp(z - z.max())
        ids.append(int(rng.choice(65, p=p / p.sum())))
        if cache["pos"] == 32:
            cache = new_cache()
            for t in ids[-32:]:
                z = decode_step(W, cache, t)
        else:
            z = decode_step(W, cache, ids[-1])
    return decode(ids)
```
3. sliding cache: drops the oldest row and reuses position 31: fails test 5
```python
import numpy as np


def new_cache():
    return {"k": np.zeros((4, 0, 8)), "v": np.zeros((4, 0, 8)), "pos": 0}


def decode_step(W, cache, token):
    x = W["wte"][token] + W["wpe"][cache["pos"]]
    qkv = ln(x, W["h0.ln1_g"], W["h0.ln1_b"]) @ W["h0.qkv_w"] + W["h0.qkv_b"]
    q, k, v = (qkv[j * 32:(j + 1) * 32].reshape(4, 1, 8) for j in range(3))
    cache["k"] = np.concatenate([cache["k"], k], axis=1)
    cache["v"] = np.concatenate([cache["v"], v], axis=1)
    s = q @ cache["k"].transpose(0, 2, 1) / np.sqrt(8)
    a = np.exp(s - s.max(-1, keepdims=True))
    a = a / a.sum(-1, keepdims=True)
    x = x + (a @ cache["v"]).reshape(32) @ W["h0.proj_w"] + W["h0.proj_b"]
    h = np.maximum(ln(x, W["h0.ln2_g"], W["h0.ln2_b"]) @ W["h0.fc_w"] + W["h0.fc_b"], 0)
    x = x + h @ W["h0.out_w"] + W["h0.out_b"]
    cache["pos"] += 1
    return ln(x, W["lnf_g"], W["lnf_b"]) @ W["head_w"] + W["head_b"]


def generate_cached(W, prompt, n, seed):
    rng = np.random.default_rng(seed)
    ids = encode(prompt)
    cache = new_cache()
    for t in ids[-32:]:
        z = decode_step(W, cache, t)
    for _ in range(n):
        p = np.exp(z - z.max())
        ids.append(int(rng.choice(65, p=p / p.sum())))
        if cache["pos"] == 32:
            cache["k"], cache["v"], cache["pos"] = cache["k"][:, 1:], cache["v"][:, 1:], 31
            z = decode_step(W, cache, ids[-1])
        else:
            z = decode_step(W, cache, ids[-1])
    return decode(ids)
```
4. refills one step early (at 31): fails test 5
```python
import numpy as np


def new_cache():
    return {"k": np.zeros((4, 0, 8)), "v": np.zeros((4, 0, 8)), "pos": 0}


def decode_step(W, cache, token):
    x = W["wte"][token] + W["wpe"][cache["pos"]]
    qkv = ln(x, W["h0.ln1_g"], W["h0.ln1_b"]) @ W["h0.qkv_w"] + W["h0.qkv_b"]
    q, k, v = (qkv[j * 32:(j + 1) * 32].reshape(4, 1, 8) for j in range(3))
    cache["k"] = np.concatenate([cache["k"], k], axis=1)
    cache["v"] = np.concatenate([cache["v"], v], axis=1)
    s = q @ cache["k"].transpose(0, 2, 1) / np.sqrt(8)
    a = np.exp(s - s.max(-1, keepdims=True))
    a = a / a.sum(-1, keepdims=True)
    x = x + (a @ cache["v"]).reshape(32) @ W["h0.proj_w"] + W["h0.proj_b"]
    h = np.maximum(ln(x, W["h0.ln2_g"], W["h0.ln2_b"]) @ W["h0.fc_w"] + W["h0.fc_b"], 0)
    x = x + h @ W["h0.out_w"] + W["h0.out_b"]
    cache["pos"] += 1
    return ln(x, W["lnf_g"], W["lnf_b"]) @ W["head_w"] + W["head_b"]


def generate_cached(W, prompt, n, seed):
    rng = np.random.default_rng(seed)
    ids = encode(prompt)
    cache = new_cache()
    for t in ids[-32:]:
        z = decode_step(W, cache, t)
    for _ in range(n):
        p = np.exp(z - z.max())
        ids.append(int(rng.choice(65, p=p / p.sum())))
        if cache["pos"] == 31:
            cache = new_cache()
            for t in ids[-32:]:
                z = decode_step(W, cache, t)
        else:
            z = decode_step(W, cache, ids[-1])
    return decode(ids)
```
5. heads split the wrong way (interleaved): fails test 1
```python
import numpy as np


def new_cache():
    return {"k": np.zeros((4, 0, 8)), "v": np.zeros((4, 0, 8)), "pos": 0}


def decode_step(W, cache, token):
    x = W["wte"][token] + W["wpe"][cache["pos"]]
    qkv = ln(x, W["h0.ln1_g"], W["h0.ln1_b"]) @ W["h0.qkv_w"] + W["h0.qkv_b"]
    q, k, v = (qkv[j * 32:(j + 1) * 32].reshape(8, 4).T.reshape(4, 1, 8) for j in range(3))
    cache["k"] = np.concatenate([cache["k"], k], axis=1)
    cache["v"] = np.concatenate([cache["v"], v], axis=1)
    s = q @ cache["k"].transpose(0, 2, 1) / np.sqrt(8)
    a = np.exp(s - s.max(-1, keepdims=True))
    a = a / a.sum(-1, keepdims=True)
    x = x + (a @ cache["v"]).reshape(32) @ W["h0.proj_w"] + W["h0.proj_b"]
    h = np.maximum(ln(x, W["h0.ln2_g"], W["h0.ln2_b"]) @ W["h0.fc_w"] + W["h0.fc_b"], 0)
    x = x + h @ W["h0.out_w"] + W["h0.out_b"]
    cache["pos"] += 1
    return ln(x, W["lnf_g"], W["lnf_b"]) @ W["head_w"] + W["head_b"]


def generate_cached(W, prompt, n, seed):
    rng = np.random.default_rng(seed)
    ids = encode(prompt)
    cache = new_cache()
    for t in ids[-32:]:
        z = decode_step(W, cache, t)
    for _ in range(n):
        p = np.exp(z - z.max())
        ids.append(int(rng.choice(65, p=p / p.sum())))
        if cache["pos"] == 32:
            cache = new_cache()
            for t in ids[-32:]:
                z = decode_step(W, cache, t)
        else:
            z = decode_step(W, cache, ids[-1])
    return decode(ids)
```
6. greedy decoding instead of sampling: fails test 3
```python
import numpy as np


def new_cache():
    return {"k": np.zeros((4, 0, 8)), "v": np.zeros((4, 0, 8)), "pos": 0}


def decode_step(W, cache, token):
    x = W["wte"][token] + W["wpe"][cache["pos"]]
    qkv = ln(x, W["h0.ln1_g"], W["h0.ln1_b"]) @ W["h0.qkv_w"] + W["h0.qkv_b"]
    q, k, v = (qkv[j * 32:(j + 1) * 32].reshape(4, 1, 8) for j in range(3))
    cache["k"] = np.concatenate([cache["k"], k], axis=1)
    cache["v"] = np.concatenate([cache["v"], v], axis=1)
    s = q @ cache["k"].transpose(0, 2, 1) / np.sqrt(8)
    a = np.exp(s - s.max(-1, keepdims=True))
    a = a / a.sum(-1, keepdims=True)
    x = x + (a @ cache["v"]).reshape(32) @ W["h0.proj_w"] + W["h0.proj_b"]
    h = np.maximum(ln(x, W["h0.ln2_g"], W["h0.ln2_b"]) @ W["h0.fc_w"] + W["h0.fc_b"], 0)
    x = x + h @ W["h0.out_w"] + W["h0.out_b"]
    cache["pos"] += 1
    return ln(x, W["lnf_g"], W["lnf_b"]) @ W["head_w"] + W["head_b"]


def generate_cached(W, prompt, n, seed):
    rng = np.random.default_rng(seed)
    ids = encode(prompt)
    cache = new_cache()
    for t in ids[-32:]:
        z = decode_step(W, cache, t)
    for _ in range(n):
        p = np.exp(z - z.max())
        ids.append(int(np.argmax(z)))
        if cache["pos"] == 32:
            cache = new_cache()
            for t in ids[-32:]:
                z = decode_step(W, cache, t)
        else:
            z = decode_step(W, cache, ids[-1])
    return decode(ids)
```
7. caches the queries too (harmless): SURVIVES (equivalent: a correct alternative)
```python
import numpy as np


def new_cache():
    return {"k": np.zeros((4, 0, 8)), "v": np.zeros((4, 0, 8)), "pos": 0}


def decode_step(W, cache, token):
    x = W["wte"][token] + W["wpe"][cache["pos"]]
    qkv = ln(x, W["h0.ln1_g"], W["h0.ln1_b"]) @ W["h0.qkv_w"] + W["h0.qkv_b"]
    q, k, v = (qkv[j * 32:(j + 1) * 32].reshape(4, 1, 8) for j in range(3))
    cache["k"] = np.concatenate([cache["k"], k], axis=1)
    cache["v"] = np.concatenate([cache["v"], v], axis=1)
    s = q @ cache["k"].transpose(0, 2, 1) / np.sqrt(8)
    a = np.exp(s - s.max(-1, keepdims=True))
    a = a / a.sum(-1, keepdims=True)
    x = x + (a @ cache["v"]).reshape(32) @ W["h0.proj_w"] + W["h0.proj_b"]
    h = np.maximum(ln(x, W["h0.ln2_g"], W["h0.ln2_b"]) @ W["h0.fc_w"] + W["h0.fc_b"], 0)
    x = x + h @ W["h0.out_w"] + W["h0.out_b"]
    cache.setdefault("q", []).append(q)
    cache["pos"] += 1
    return ln(x, W["lnf_g"], W["lnf_b"]) @ W["head_w"] + W["head_b"]


def generate_cached(W, prompt, n, seed):
    rng = np.random.default_rng(seed)
    ids = encode(prompt)
    cache = new_cache()
    for t in ids[-32:]:
        z = decode_step(W, cache, t)
    for _ in range(n):
        p = np.exp(z - z.max())
        ids.append(int(rng.choice(65, p=p / p.sum())))
        if cache["pos"] == 32:
            cache = new_cache()
            for t in ids[-32:]:
                z = decode_step(W, cache, t)
        else:
            z = decode_step(W, cache, ids[-1])
    return decode(ids)
```
8. refill crops to 31 ids then decodes the new one (equivalent): SURVIVES (equivalent: a correct alternative)
```python
import numpy as np


def new_cache():
    return {"k": np.zeros((4, 0, 8)), "v": np.zeros((4, 0, 8)), "pos": 0}


def decode_step(W, cache, token):
    x = W["wte"][token] + W["wpe"][cache["pos"]]
    qkv = ln(x, W["h0.ln1_g"], W["h0.ln1_b"]) @ W["h0.qkv_w"] + W["h0.qkv_b"]
    q, k, v = (qkv[j * 32:(j + 1) * 32].reshape(4, 1, 8) for j in range(3))
    cache["k"] = np.concatenate([cache["k"], k], axis=1)
    cache["v"] = np.concatenate([cache["v"], v], axis=1)
    s = q @ cache["k"].transpose(0, 2, 1) / np.sqrt(8)
    a = np.exp(s - s.max(-1, keepdims=True))
    a = a / a.sum(-1, keepdims=True)
    x = x + (a @ cache["v"]).reshape(32) @ W["h0.proj_w"] + W["h0.proj_b"]
    h = np.maximum(ln(x, W["h0.ln2_g"], W["h0.ln2_b"]) @ W["h0.fc_w"] + W["h0.fc_b"], 0)
    x = x + h @ W["h0.out_w"] + W["h0.out_b"]
    cache["pos"] += 1
    return ln(x, W["lnf_g"], W["lnf_b"]) @ W["head_w"] + W["head_b"]


def generate_cached(W, prompt, n, seed):
    rng = np.random.default_rng(seed)
    ids = encode(prompt)
    cache = new_cache()
    for t in ids[-32:]:
        z = decode_step(W, cache, t)
    for _ in range(n):
        p = np.exp(z - z.max())
        ids.append(int(rng.choice(65, p=p / p.sum())))
        if cache["pos"] == 32:
            cache = new_cache()
            for t in ids[-32:-1]:
                decode_step(W, cache, t)
            z = decode_step(W, cache, ids[-1])
        else:
            z = decode_step(W, cache, ids[-1])
    return decode(ids)
```

### l20-the-kv-cache.json screens[9] `kv_cache_bytes`
1. missing the factor of 2 (keys only): fails test 1
```python
def kv_cache_bytes(layers, d, T, bytes_per, batch):
    return layers * d * T * bytes_per * batch
```
2. missing the layer count: fails test 2
```python
def kv_cache_bytes(layers, d, T, bytes_per, batch):
    return 2 * d * T * bytes_per * batch
```
3. d by d per layer instead of T by d: fails test 2
```python
def kv_cache_bytes(layers, d, T, bytes_per, batch):
    return 2 * layers * d * d * bytes_per * batch
```
4. bytes_per read as bits: fails test 1
```python
def kv_cache_bytes(layers, d, T, bytes_per, batch):
    return 2 * layers * d * T * bytes_per * batch // 8
```

### homework-5.json items[0] `memory_plan` (performance task)
1. no gradients in training: fails test 1
```python
def n_params(c):
    V, T, d, L, m = c["V"], c["T"], c["d"], c["n_layer"], c["mlp"]
    n = V * d + T * d + L * (4 * d * d + 2 * d * m + 9 * d + m) + 2 * d
    return n if c["tied"] else n + d * V + V


def memory_plan(config, mode):
    N, b = n_params(config), config["bytes"]
    if mode == "train":
        opt = N * (2 * config["adam_bytes"] + config["master"])
        return {"weights": N * b, "grads": 0, "optimizer": opt, "kv_cache": 0}
    L, d = config["n_layer"], config["d"]
    kv = 2 * L * d * config["context"] * b * config["batch"]
    return {"weights": N * b, "grads": 0, "optimizer": 0, "kv_cache": kv}
```
2. master copy filed under weights: fails test 3
```python
def n_params(c):
    V, T, d, L, m = c["V"], c["T"], c["d"], c["n_layer"], c["mlp"]
    n = V * d + T * d + L * (4 * d * d + 2 * d * m + 9 * d + m) + 2 * d
    return n if c["tied"] else n + d * V + V


def memory_plan(config, mode):
    N, b = n_params(config), config["bytes"]
    if mode == "train":
        opt = N * 2 * config["adam_bytes"]
        return {"weights": N * (b + config["master"]), "grads": N * b, "optimizer": opt, "kv_cache": 0}
    L, d = config["n_layer"], config["d"]
    kv = 2 * L * d * config["context"] * b * config["batch"]
    return {"weights": N * b, "grads": 0, "optimizer": 0, "kv_cache": kv}
```
3. one Adam moment: fails test 1
```python
def n_params(c):
    V, T, d, L, m = c["V"], c["T"], c["d"], c["n_layer"], c["mlp"]
    n = V * d + T * d + L * (4 * d * d + 2 * d * m + 9 * d + m) + 2 * d
    return n if c["tied"] else n + d * V + V


def memory_plan(config, mode):
    N, b = n_params(config), config["bytes"]
    if mode == "train":
        opt = N * (config["adam_bytes"] + config["master"])
        return {"weights": N * b, "grads": N * b, "optimizer": opt, "kv_cache": 0}
    L, d = config["n_layer"], config["d"]
    kv = 2 * L * d * config["context"] * b * config["batch"]
    return {"weights": N * b, "grads": 0, "optimizer": 0, "kv_cache": kv}
```
4. cache without the layer count: fails test 4
```python
def n_params(c):
    V, T, d, L, m = c["V"], c["T"], c["d"], c["n_layer"], c["mlp"]
    n = V * d + T * d + L * (4 * d * d + 2 * d * m + 9 * d + m) + 2 * d
    return n if c["tied"] else n + d * V + V


def memory_plan(config, mode):
    N, b = n_params(config), config["bytes"]
    if mode == "train":
        opt = N * (2 * config["adam_bytes"] + config["master"])
        return {"weights": N * b, "grads": N * b, "optimizer": opt, "kv_cache": 0}
    L, d = config["n_layer"], config["d"]
    kv = 2 * d * config["context"] * b * config["batch"]
    return {"weights": N * b, "grads": 0, "optimizer": 0, "kv_cache": kv}
```
5. cache sized at T, not context: SURVIVES
```python
def n_params(c):
    V, T, d, L, m = c["V"], c["T"], c["d"], c["n_layer"], c["mlp"]
    n = V * d + T * d + L * (4 * d * d + 2 * d * m + 9 * d + m) + 2 * d
    return n if c["tied"] else n + d * V + V


def memory_plan(config, mode):
    N, b = n_params(config), config["bytes"]
    if mode == "train":
        opt = N * (2 * config["adam_bytes"] + config["master"])
        return {"weights": N * b, "grads": N * b, "optimizer": opt, "kv_cache": 0}
    L, d = config["n_layer"], config["d"]
    kv = 2 * L * d * config["T"] * b * config["batch"]
    return {"weights": N * b, "grads": 0, "optimizer": 0, "kv_cache": kv}
```
6. untied head without its bias: fails test 1
```python
def n_params(c):
    V, T, d, L, m = c["V"], c["T"], c["d"], c["n_layer"], c["mlp"]
    n = V * d + T * d + L * (4 * d * d + 2 * d * m + 9 * d + m) + 2 * d
    return n if c["tied"] else n + d * V


def memory_plan(config, mode):
    N, b = n_params(config), config["bytes"]
    if mode == "train":
        opt = N * (2 * config["adam_bytes"] + config["master"])
        return {"weights": N * b, "grads": N * b, "optimizer": opt, "kv_cache": 0}
    L, d = config["n_layer"], config["d"]
    kv = 2 * L * d * config["context"] * b * config["batch"]
    return {"weights": N * b, "grads": 0, "optimizer": 0, "kv_cache": kv}
```
7. block norms and biases left out (5d, not 9d): fails test 1
```python
def n_params(c):
    V, T, d, L, m = c["V"], c["T"], c["d"], c["n_layer"], c["mlp"]
    n = V * d + T * d + L * (4 * d * d + 2 * d * m + 5 * d + m) + 2 * d
    return n if c["tied"] else n + d * V + V


def memory_plan(config, mode):
    N, b = n_params(config), config["bytes"]
    if mode == "train":
        opt = N * (2 * config["adam_bytes"] + config["master"])
        return {"weights": N * b, "grads": N * b, "optimizer": opt, "kv_cache": 0}
    L, d = config["n_layer"], config["d"]
    kv = 2 * L * d * config["context"] * b * config["batch"]
    return {"weights": N * b, "grads": 0, "optimizer": 0, "kv_cache": kv}
```
8. inference also keeps gradients: fails test 2
```python
def n_params(c):
    V, T, d, L, m = c["V"], c["T"], c["d"], c["n_layer"], c["mlp"]
    n = V * d + T * d + L * (4 * d * d + 2 * d * m + 9 * d + m) + 2 * d
    return n if c["tied"] else n + d * V + V


def memory_plan(config, mode):
    N, b = n_params(config), config["bytes"]
    if mode == "train":
        opt = N * (2 * config["adam_bytes"] + config["master"])
        return {"weights": N * b, "grads": N * b, "optimizer": opt, "kv_cache": 0}
    L, d = config["n_layer"], config["d"]
    kv = 2 * L * d * config["context"] * b * config["batch"]
    return {"weights": N * b, "grads": N * b, "optimizer": 0, "kv_cache": kv}
```
9. training adds an activation term (batch x context x d x bytes) to the optimiser bytes; the task leaves activations out: fails test 1
```python
def n_params(c):
    V, T, d, L, m = c["V"], c["T"], c["d"], c["n_layer"], c["mlp"]
    n = V * d + T * d + L * (4 * d * d + 2 * d * m + 9 * d + m) + 2 * d
    return n if c["tied"] else n + d * V + V


def memory_plan(config, mode):
    N, b = n_params(config), config["bytes"]
    if mode == "train":
        opt = N * (2 * config["adam_bytes"] + config["master"]) + 2 * L * config["batch"] * config["context"] * config["d"] * b if False else N * (2 * config["adam_bytes"] + config["master"]) + config["batch"] * config["context"] * config["d"] * b
        return {"weights": N * b, "grads": N * b, "optimizer": opt, "kv_cache": 0}
    L, d = config["n_layer"], config["d"]
    kv = 2 * L * d * config["context"] * b * config["batch"]
    return {"weights": N * b, "grads": 0, "optimizer": 0, "kv_cache": kv}
```

### homework-5.json items[1] `round_float`
1. ties rounded up (floor(q + 0.5)): fails test 1
```python
import math


def round_float(x, bits, emax):
    if x == 0 or not math.isfinite(x):
        return float(x)
    m, e = math.frexp(abs(x))
    q = m * 2 ** bits
    r = math.floor(q + 0.5)
    y = math.ldexp(r, e - bits)
    if y >= 2.0 ** (emax + 1):
        y = math.inf
    return math.copysign(y, x)


def to_bf16(x):
    return round_float(x, 8, 127)


def to_fp16(x):
    return round_float(x, 11, 15)
```
2. overflow judged on x against the largest finite value, before rounding: fails test 5
```python
import math


def round_float(x, bits, emax):
    if x == 0 or not math.isfinite(x):
        return float(x)
    if abs(x) > (2 - 2.0 ** (1 - bits)) * 2.0 ** emax:
        return math.copysign(math.inf, x)
    m, e = math.frexp(abs(x))
    q = m * 2 ** bits
    r = math.floor(q)
    f = q - r
    if f > 0.5 or (f == 0.5 and r % 2 == 1):
        r += 1
    y = math.ldexp(r, e - bits)
    if y >= 2.0 ** (emax + 1):
        y = math.inf
    return math.copysign(y, x)


def to_bf16(x):
    return round_float(x, 8, 127)


def to_fp16(x):
    return round_float(x, 11, 15)
```
3. overflow only strictly past 2**(emax+1): fails test 6
```python
import math


def round_float(x, bits, emax):
    if x == 0 or not math.isfinite(x):
        return float(x)
    m, e = math.frexp(abs(x))
    q = m * 2 ** bits
    r = math.floor(q)
    f = q - r
    if f > 0.5 or (f == 0.5 and r % 2 == 1):
        r += 1
    y = math.ldexp(r, e - bits)
    if y > 2.0 ** (emax + 1):
        y = math.inf
    return math.copysign(y, x)


def to_bf16(x):
    return round_float(x, 8, 127)


def to_fp16(x):
    return round_float(x, 11, 15)
```
4. stored mantissa bits used as significant bits (one bit short): fails test 5
```python
import math


def round_float(x, bits, emax):
    if x == 0 or not math.isfinite(x):
        return float(x)
    m, e = math.frexp(abs(x))
    q = m * 2 ** (bits - 1)
    r = math.floor(q)
    f = q - r
    if f > 0.5 or (f == 0.5 and r % 2 == 1):
        r += 1
    y = math.ldexp(r, e - bits + 1)
    if y >= 2.0 ** (emax + 1):
        y = math.inf
    return math.copysign(y, x)


def to_bf16(x):
    return round_float(x, 8, 127)


def to_fp16(x):
    return round_float(x, 11, 15)
```
5. frexp of x, not abs(x), and no copysign (rounds negatives correctly, but -65,520 gives -65,536, not -inf): SURVIVES
```python
import math


def round_float(x, bits, emax):
    if x == 0 or not math.isfinite(x):
        return float(x)
    m, e = math.frexp(x)
    q = m * 2 ** bits
    r = math.floor(q)
    f = q - r
    if f > 0.5 or (f == 0.5 and r % 2 == 1):
        r += 1
    y = math.ldexp(r, e - bits)
    if y >= 2.0 ** (emax + 1):
        y = math.inf
    return y


def to_bf16(x):
    return round_float(x, 8, 127)


def to_fp16(x):
    return round_float(x, 11, 15)
```
6. Python's round() for the tie (equivalent): SURVIVES (equivalent: a correct alternative)
```python
import math


def round_float(x, bits, emax):
    if x == 0 or not math.isfinite(x):
        return float(x)
    m, e = math.frexp(abs(x))
    q = m * 2 ** bits
    r = round(q)
    y = math.ldexp(r, e - bits)
    if y >= 2.0 ** (emax + 1):
        y = math.inf
    return math.copysign(y, x)


def to_bf16(x):
    return round_float(x, 8, 127)


def to_fp16(x):
    return round_float(x, 11, 15)
```
