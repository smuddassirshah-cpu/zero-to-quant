# representations level 4 (Diffusion): report

Branch `ai-w5-representations`, after level 3. Brief: `docs/briefs/representations.md` Level 4. Generators and helpers: scratchpad `representations-4/` (`common4.py`, `train16.py`, `gen_l13.py` to `gen_l16.py`, `gen_sets4.py`, `timing4.mjs`), sharing `representations-2/lib2.py`.

## Files

| File | Screens or items | Quiz |
|---|---|---|
| `l13-adding-noise.json` | 11: problem blur the rings (`scatter` with step frames; the gap closes between steps 10 and 20), name the forward step by hand (`table` widget), ladder $\bar\alpha_3 = 0.504$, derive two steps in one (`order`, a standard-deviation distractor), ladder Ho et al.'s schedule ($\bar\alpha_{500} \approx 0.0786$, $\bar\alpha_{1000} \approx 4.0 \times 10^{-5}$), ladder this level's schedule ($\bar\alpha_{50} \approx 0.0045$; `series`), ladder why shrink first (variance 0.91 at step 20), trap noise without shrinking (5.825), ladder edge an end that is not noise ($0.99^{50} \approx 0.605$), code `alpha_bar` and `noise_step`, code `noise_to` (against 50 single steps in distribution), transfer an AR(1) towards 0. 15 min | 3 |
| `l14-predict-the-noise.json` | 12: problem which start (about twice as likely), name the noise predictor and one loss (0.13), ladder one training example, ladder the recorded training curve (settles near 0.64), ladder edge loss by step (1.72 at step 1, 0.01 at step 50; `bars`), trap without the clock (0.81 against 0.64), generalise, code `make_batch`, code `noise_loss` (shipped weights), code `train_denoiser`, transfer a learned denoiser against a moving average. 15 min | 3 |
| `l15-sampling-backwards.json` | 11: problem rings out of noise (`scatter` frames; ring share about 0.24 until step 10, 0.70 at step 0), name the reverse step by hand, ladder the ring share against the data and a round normal (0.70, 1, 0.21), trap no fresh noise (the outer ring empties: 0% against 50%), ladder the steps run forwards (0.22), ladder edge a start far in the tail, generalise, code `reverse_step`, code `sample`, code `ring_share`, transfer synthetic scenarios checked on held-out data. 15 min | 3 |
| `l16-the-schedule.json` | 12: problem 10, 50 or 200 steps (frames of recorded samples), name the signal-to-noise ratio (0.0045), ladder three schedules' ends ($0.9^{10} \approx 0.349$), ladder the ratio curves (`plane`), ladder ring share by $T$ (0.01, 0.55, 0.70, 0.81 for 1, 10, 50, 200), trap more steps always better, ladder edge $T = 1$ (a blurred average), ladder an end that is too clean (sd 0.778), generalise, code `linear_betas` and `snr`, code `end_gap`, transfer steps as a cost, like a pricing grid. 15 min | 3 |
| `review-4.json` | 9 items, difficulty 2 to 4, `pass: 0.8`, all four lessons | |
| `homework-4.json` | 8 items, difficulty 3 to 5: performance code `ddpm_sampler` (5), code `steps_to_noise` (4), order the closed form by induction with two distractors (4), longform synthetic market data for backtests (5, rubric 10, two required rows), numeric a late signal-to-noise ratio (3), numeric a reverse mean (4), choice the last step (3), numeric the price of steps (3) | |
| `problems-4.json` | 3 chained problems, 12 parts: a schedule, a noised point, one reverse step with a perfect predictor (l13, l15; 4); normal data, the mean and variance of $x_t$, the optimal noise guess (l13, l14; 5); a constant schedule's end, its ratio, the steps needed, the cost (l13, l16; 4) | |

New data files: `representations_ops_l4.py` (v1.0, 2.6 KB) and `representations-l15-denoiser.json` (96,769 bytes: starting and trained weights of the $2 + t/T \to 64 \to 64 \to 2$ ReLU noise predictor and the training loss every 100 steps). The $T = 1$, 10 and 200 nets of l16 are not shipped; their samples are embedded in the lesson and the number script retrains them. Reused byte-identical: `autograd.py`, `nt_ops_l1.py`. 12 Python code widgets, 38 mutants (the taught bug among each: summed betas, no shrink, no square roots, steps drawn from 0, no step input, noise at the last step, no fresh noise, steps run forwards, a jump to $\mathbf x_0$ each step). Every training widget has an exact seeded test (`train_denoiser` 3 and 2 steps to 6 places).

## Self-check (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors; level warnings are only `O2-long-sentence` advisories and ladder canvas-kind changes.
2. `voice-scan.py 35 --summary`: 0 over 35 words, 0 lesson ids in code spans, 0 doubled words, 0 explanations over three sentences.
3. `node tools/run-number-scripts.mjs --only representations-L4` (strict): 248 of 248 checks, 0 uncovered, 33 literals (givens and how-line settings), exit 0, about 40 s (it retrains five nets by hand backprop).
4. `grade-all.mjs --code` on all seven files: 72 widgets and 12 code widgets, 0 failures. Playthrough with `--local-cdn`, desktop and `--mobile`: all passed (end of this file). `fresh-check.mjs --file` on review, homework and problems: 0 hits; `same-course-reuse.mjs`: no error for this course.

## Timing (Pyodide 0.27.7 under node, desktop, per hidden test)

`train_denoiser` 120 steps about 0.7 s (budget 6,000; 300 steps took 1.8 s, so the threshold run was cut to 120); `ddpm_sampler` 20,000 samples over 100 to 150 steps 153 to 247 ms; `sample` 1,000 samples over 50 steps about 160 ms (the sampling loop); `noise_to` on 20,000 points 122 ms; every other case under 40 ms.

## Numbers and their sources (route A generator, route B number script)

- l13: every $\bar\alpha$ by a sum of logs against the running product; 0.504 and the sum of betas 5.025 (Fractions); the hand step and frames (closed form); 0.0786 and $4.0 \times 10^{-5}$, 0.0045 as the brief quotes; 0.91; 0.605.
- l14: likelihood ratio about 2 (math); 0.13; the example (math); the shipped net retrained by hand backprop (start to $10^{-5}$, trained within $10^{-2}$ after 11,700 steps) and the loss curve within 0.02; loss by step by an independent forward pass; the no-time net retrained by hand backprop (loss within 0.02 of the stated 0.81).
- l15: ring shares by an independent sampler (within 0.002 to 0.003); the hand reverse step; the round-normal baseline 0.214 by the Rayleigh distribution; 0% and 50% on the outer ring; 0.22 upwards; tail runs ending at radii 1.68 and 1.67.
- l16: matched schedules by root finding (`brentq`); the $T = 1$, 10 and 200 nets retrained by hand backprop, shares within 0.01 of the stated 0.006, 0.547, 0.814; 0.0045; 0.349; 0.778.
- Sets: every key by Fractions, logs or closed forms; thresholds checked with margin on four seeds each (`train_denoiser` at most 0.77 against 0.8; ring share above 0.62 against 0.55; outer-ring share 38% to 62% against 30% to 70%; the planted normal checks within 0.03 and 0.05 against 0.05 and 0.08).

## Conventions

- Data: `two_rings(n, seed)`, radii 0.8 and 1.6 with noise 0.03, variance about 0.8 per coordinate (close to 1, as the brief asks for scaled data).
- Schedule: $T = 50$, $\beta_t$ linear from $10^{-3}$ to 0.2; for l16, $\beta_t$ linear from $10^{-3} \cdot 50/T$ to the end that matches $\bar\alpha_{50}$, so only the step count differs.
- Network: `eps_model` with the scaled time feature $t/T$, two ReLU layers of 64; Adam 0.002, batch 256, 12,000 steps; the reverse step uses $\sigma_t^2 = \beta_t$ with no noise at $t = 1$.
- Ring share: the fraction of points within 0.1 of radius 0.8 or 1.6.

## Deviations from the brief

- `noise_loss` and the sampler take the step count from `len(betas)`; `noise_loss` has an optional `T` argument.
- `train_denoiser` returns the trained parameters and draws batches of 256 inside a supplied loop; its threshold run starts from `init_denoiser(64, 0)` (loss about 2.3), because from the shipped checkpoint the loss is already near its floor.
- l16's recorded sample sets come from nets the number script retrains rather than from shipped weights; in this toy 200 steps still beat 50 (0.81 against 0.70), so the lesson says the gains shrink rather than stop.
- No autograd op was missing: `relu` is in v1.0.

## `representations_ops_l4.py` (v1.0): public names

- `two_rings(n, seed=0, radii=(0.8, 1.6), noise=0.03) -> X`.
- `linear_schedule(T=50, b1=1e-3, bT=0.2) -> betas`.
- `init_denoiser(hidden=64, seed=0) -> [W1, w1t, b1, W2, b2, W3, b3]`.
- `eps_model(params, X, t, T) -> predicted noise` (arrays or `Tensor`s; gradient-checked to relative $10^{-6}$).

## Proposed course.json change

None.

## Playthrough with and without --mobile

See the end of this file.

All seven files with `--local-cdn <pkgs>`, desktop and `--mobile` (440 px): all passed. l13 15 checks, l14 14, l15 14, l16 15, quizzes 3/3 each; review-4 9 of 9; homework-4 8 of 8, 36 of 36 marks, performance starter fails, longform marked by the button; problems-4 12 parts with `--why`, 17 typed slips routed. One mobile homework run stopped with "threw" while other Pyodide jobs ran beside it; rerun alone, with and without `--shots`, it passed in 6 to 18 s. l14, l16 and homework-4 were replayed at both sizes after their last edits. Screens read: the noising and sampling frames, the no-noise trap scatter and the labelled ratio curves fit at 440 px.
