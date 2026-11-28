# gpt level 5: Hardware and precision (report)

Author: content agent, wave 8, branch `ai-w8-gpt` (from `71ca01d0`). Brief: `docs/briefs/gpt.md` Level 5. Skill `gpt-hardware` throughout; ids, names and objectives from `course.json`. Builds on `numerics` L1 (the double's layout, epsilon, the float32 gap near 20,000) and gpt L2 to L4 (the tiny GPT's forward pass and sampler, the memory and FLOP counts). The L2 to L4 files were not edited.

## Files

| File | Screens or items | Quiz | Code widgets (mutants) |
|---|---|---|---|
| `l17-waiting-for-memory.json` | 10 | 3 | `matmul_intensity` + `bound` + `measure_gflops` (4) |
| `l18-fewer-bits.json` | 11 | 3 | `to_bf16` by float32 bits + `bf16_sum` + `fp32_sum_to_bf16` (4) |
| `l19-what-fits.json` | 12 | 3 | `training_bytes` + `inference_bytes` (4) |
| `l20-the-kv-cache.json` | 12 | 3 | `decode_step` + `generate_cached` on the tiny GPT (5); `kv_cache_bytes` (3) |
| `review-5.json` | 10 items, `pass` 0.8 | | difficulty 2 to 4, every lesson at least twice |
| `homework-5.json` | 6 items | | `h-memory-plan` performance task (6 mutants), `h-round-fp16` rounding by `math.frexp` with six ties (4), an order item with a distractor (a matmul's intensity), a longform (10-point rubric, 70B on one machine), a numeric, a choice |
| `problems-5.json` | 3 problems, 12 parts | | serving a 13B model: weights, cache, ms per token, tokens a second (d5); fine-tuning a 3B model (d3); a bf16 weight whose updates are inflated then erased (d4) |
| `app/content/data/ai/gpt_ops_l5.py` | new module, v1.0, SHA-256 starting `71bf6fff15ca` | | signatures at the end |

Canvases: `plane` with log axes (the roofline, a draggable point, tappable operations), `number-line` (bf16 numbers near 1 and from 248 to 266), `table`, `bars` with frames (bytes per parameter: inference, float32, mixed), `array` with frames (a KV cache filling) and a stale window, `console`. Performance report: `docs/reports/gpt-5-perf.md`.

## Self-check (SESSION PROTOCOL 4)

1. Validator: 0 errors. No `[source-ban]` or `[ai-mutants]` warning on these files.
2. Voice: `voice-scan.py 35` on the course folder: 0 over 35 words, 0 explanations over three sentences, 0 lesson ids in code spans, 0 doubled words.
3. Numbers: `node tools/run-number-scripts.mjs --python <venv> --only gpt-L5`: passed, 6 s; strict coverage, 0 uncovered, 14 literals with reasons; 273 checks; 7 code widgets and 30 mutants run in CPython.
4. Playthrough, `--local-cdn`, `--why`, desktop and `--mobile`, all seven files: all passed (lessons 13 to 15 checks each, quiz 3 of 3; review 10 of 10; homework 6 of 6, the performance starter failing and the longform marked; problems-5 3 problems, 12 parts, 21 typed slips routed). After the layout fixes the three changed lessons were replayed with `--mobile`: passed. Screenshots read at 440 px and desktop; two faults fixed (a roofline label beside the wrong point, number-line ticks off the bf16 dots) and the array's index row hidden where it misled.

Also `grade-all.mjs --file <each> --code --strict-feedback --local-cdn`: 0 failures (7 Python widgets in Pyodide; every mutant fails its named test and every reached test has its `byKey` line). `same-course-reuse.mjs --all`: nothing for the level after rewording one problem stem that shared 13 words with a review item. `fresh-check.mjs --file problems-5.json`: 0 hits, 1 advisory (two parameters, 0.02 and 0.01, shared with l10).

Timing: the whole of `l20-the-kv-cache` (2 code widgets, solution, starter and 8 mutants each against every test) grades in 5.3 s in Pyodide, so each case of the cached decoder is far under a third of its 5 s limit. Generations past the window cost one 32-position refill per character, so those tests are kept to 20 and 4 characters.

## Numbers and sources (two ways each, in the script)

- Rounding: bf16 by float32 bits (`to_bf16`) and by `math.frexp` (`round_bits(x, 8, 127)`), fp16 by `np.float16` and by `round_bits(x, 11, 15)`; all agree on every stated value. Known values: $1 + 2^{-7} \to 1.0078125$ (the next bf16 after 1), ties $1 + 2^{-8} \to 1$ and $1 + 3 \cdot 2^{-8} \to 1.015625$, $257 \to 256$, $0.1 \to 0.10009765625$, $3.14159 \to 3.140625$, $1000.3 \to 1000$, $2.718 \to 2.71875$, $70{,}000 \to 70{,}144$ (0.2%), £101.37 to £101.50; fp16 $2049 \to 2048$, $2051 \to 2052$, $65{,}519 \to 65{,}504$ (the largest, $= \texttt{finfo(float16).max}$), $65{,}520 \to \infty$, $0.1 \to 0.0999755859375$, $1000.3 \to 1000.5$. Epsilons $2^{-7} = 0.0078125$ and $2^{-10}$; limits $3.40 \times 10^{38}$, $3.39 \times 10^{38}$, smallest normals $1.18 \times 10^{-38}$ and $6.10 \times 10^{-5}$, fp16's smallest positive $5.96 \times 10^{-8}$; $2 \times 10^{-8}$ underflows in fp16 and $\times 4{,}096$ gives $8.192 \times 10^{-5}$, a normal number.
- Stalls: a bf16 total of 1s stops at 256, fp16 at 2,048; a float32 total reaches 1,000. A bf16 weight of 1 with a thousand updates of 0.001 stays 1 (float32 reaches about 2.0). A notional of £12,345,678.91 in float32 is £12,345,679 (9p).
- Roofline (the hypothetical chip, 1,000 TFLOP/s and 3.3 TB/s): ridge 303; intensity $n/3$: 42.7, 341.3, 682.7, 1,365.3, 170.7 at 128, 1,024, 2,048, 4,096, 512 (closed form and $2mnk/((mk+kn+mn)b)$); matrix-vector 0.9995; batch 64 intensity 62.1, the ridge at a batch of about 356; reading a 4,096 bf16 matrix 10.2 µs against 0.034 µs of arithmetic; 7B decode 4.24 ms (236 tokens a second) on both chips; 128 matmul at 2.1 GFLOP/s about 2.0 ms; a laptop pass over $10^9$ returns 0.32 s.
- Memory: 7B 14 GB, training 112 GB; 70B 140 GB and 1,120 GB; the tiny GPT 576,544 bytes with Adam in float64 (18,017 parameters by formula and by `gpt_ops_l2.shapes`), activations for 16 windows of 32: 705 floats a token, 2,887,680 bytes (counted and by summing the arrays `forward_cache` keeps); a 34B model 68 GB and 544 GB (7 chips of 80 GB); 70B at 4 bits 35 GB; fine-tuning 7B 152 GB.
- KV cache: 528 positions run without a cache for 32 characters; tiny GPT 16,384 bytes; GPT-2 small 37,748,736 bytes = 36 MiB; 7B-like 2 GiB per sequence, 32 GiB at 16; 4.89 ms (204 tokens a second) with a 2 GiB cache; 2.23 times as long per token at 32,768 tokens. The cached decoder's logits match `gpt_ops_l2.forward_logits` to $1.3 \times 10^{-14}$, and `generate_cached` equals `sample_text` on 50 seeds past the window.
- Sets: review, homework, longform (80 layers of width 8,192: 2,621,440 bytes a token, about 7,600 tokens in 20 GB, 21 ms and 47 tokens a second, 94 at 8 bits) and problems (2.46 GB, 14.23 ms, 70.3 tokens a second; 48 GB, 2 chips; gap 0.03125, 6.03125, 56.25%).

## Brief deviations and notes

- Hardware is described only with round, hypothetical figures, stated as such; no vendor, product or price is named. The brief's l19 transfer "in gigabytes and pounds" is in gigabytes and chips only, because the orchestrator's instruction for this level is to name no prices.
- The roofline is drawn in TFLOP/s against FLOPs per byte, both log axes.
- l20's edge case is stronger than "crop or slide": the tiny GPT's learned absolute positions make every cached row stale when the window slides, so the cached generator re-runs the last 32 ids, and its tests run past the window to check this.
- `homework-5` `h-round-fp16` uses `math.frexp` (one function for both formats), the brief's second method, so it does not repeat l18's bit trick; it models no subnormals and says so.
- `memory_plan` counts the optimiser state as Adam's two moments plus the master copy, the convention of the ZeRO paper; the prose says which bytes go where.

## gpt_ops_l5.py (v1.0, frozen once merged)

```
VOCAB, encode, decode                                   re-exported from gpt_ops_l2
to_bf16(x) -> float                                     nearest bf16, ties to even, via float32 bits
round_bits(x, p, emax=None) -> float                    nearest p-significant-bit number (math.frexp); inf past emax
to_fp16(x) -> float                                     float(np.float16(x))
bf16_sum(xs), fp32_then_bf16(xs) -> float               stalled bf16 total; float32 total rounded once
matmul_flops(m, n, k), matmul_bytes(m, n, k, bytes_per), matmul_intensity(m, n, k, bytes_per)
bound(intensity, peak_flops, bandwidth) -> "memory" | "compute"
n_params(V, T, d, n_layer, mlp, tied=False) -> int      level 4's count; a tied head has no bias
training_bytes(N, bytes_weights, bytes_grads, bytes_optimizer, master), inference_bytes(N, bytes_per, kv_bytes)
kv_cache_bytes(layers, d, T, bytes_per, batch=1) -> int
activation_floats(V, T, d, n_head, mlp, n_layer, B) -> int    floats gpt_ops_l2.forward_cache keeps
new_cache(weights, n_head=4) -> {"k": [...], "v": [...], "pos": 0}
decode_step(weights, cache, token, n_head=4) -> logits (V,)   any number of blocks
generate_cached(weights, prompt, n, seed=0, temperature=1.0, n_head=4) -> str   equals gpt_ops_l2.sample_text
```

## Proposed course.json change

None.

## Backlog

Two bullets under "Raised later (gpt level 5)": `drag-point` tolerance on a log axis, and point labels beside a reference line on a log plane.
