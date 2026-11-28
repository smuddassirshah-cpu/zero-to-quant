# representations level 3 (Variational autoencoders): report

Branch `ai-w5-representations`, after level 2. Brief: `docs/briefs/representations.md` Level 3. Generators and helpers: scratchpad `representations-3/` (`common3.py`, `train12.py`, `gen_l9.py` to `gen_l12.py`, `gen_sets3.py`, `timing3.mjs`), sharing `representations-2/lib2.py`.

## Files

| File | Screens or items | Quiz |
|---|---|---|
| `l9-a-hidden-cause.json` | 12: problem guess the hidden angle of three points (`scatter`, `table` widget), explore the noise level (frames), name the latent variable model and $\ln p(\mathbf x \mid z) \approx 3.97$, ladder a five-draw Monte Carlo $p(\mathbf x)$, ladder 20-draw estimates swing (exact 2.77 by integration; `bars`), ladder the posterior on a grid peaks at 0.5, trap decoder against posterior, ladder edge a straight decoder (1.25, probabilistic PCA), generalise, code `sample_model` and `posterior_grid`, code `mc_marginal` (against the closed form), transfer today's market factor ($-1.15$). 15 min | 3 |
| `l10-the-elbo.json` | 11: problem close the gap with sliders on $m$ and $v$ (`plane`, live gap; $\ln p(\mathbf x) \approx -2.014$), name the two terms (KL 0.915 at the posterior), derive the bound by Jensen (`order`, a convex-way distractor), ladder edge $q$ equal to the prior (gap 4.22), ladder the two terms for three guesses (`bars`), trap the rebuild term alone, ladder one encoder for every point, generalise the identity with the KL to the posterior, code `elbo_mc` and `two_terms`, code `elbo_gap` (grid against the closed form), transfer hidden-regime models. 15 min | 3 |
| `l11-gaussian-kl.json` | 12: problem match the prior with sliders (live KL), name the closed form (0.818 for $\mathcal N(1, 0.5^2)$), ladder three guesses (2, 0.807, 0.168), derive it (`order`, a squared-mean distractor), ladder a Monte Carlo check (seed 7), ladder not symmetric (2.807), trap dropping $-\ln\sigma^2$ ($-0.495$), ladder edge $\sigma = 0.001$ (6.41), generalise coordinates add (0.818), code `kl_normal_std` and `kl_vector`, code `kl_numeric`, transfer a desk forecast against a benchmark (0.163). 15 min | 3 |
| `l12-reparameterisation.json` | 12: problem no path back (`console`), name the trick ($\partial z/\partial\sigma = \epsilon$; `graph` with $\epsilon$ entering beside $\mu$ and $\sigma$), ladder one point's loss ($-2.03$), ladder the recorded training curves (`series`; KL settles near 2.4), ladder prior samples against data (distances 0.038 and 0.011), trap one draw reused, ladder edge four codes, two collapse (`bars`), generalise the loss, code `reparam_sample` and `vae_loss`, code `train_vae` from the shipped start, code `sample_vae`, transfer synthetic stress scenarios. 15 min | 3 |
| `review-3.json` | 9 items, difficulty 2 to 4, `pass: 0.8`, all four lessons | |
| `homework-3.json` | 8 items, difficulty 3 to 5: performance code `vae_step` (5), code `kl_two_normals` (4), order the identity without Jensen with two distractors (4), longform good rebuilds and bad samples (5, rubric 10, two required rows), numeric $\partial z/\partial\ell$ (3), numeric the ELBO from two terms (3), choice spare code coordinates (4), numeric a three-coordinate KL (3) | |
| `problems-3.json` | 3 chained problems, 12 parts: one point's KL, sample, rebuild term and loss (l11, l12, l9; 4); a straight decoder's posterior variance and mean, the gap and the ELBO of the prior guess (l9, l10, l11; 5); a wide guess both ways, three coordinates, growth (l11, l10; 4) | |

New data files: `representations_ops_l3.py` (v1.0, 2.5 KB) and `representations-l12-vae.json` (11,838 bytes: starting and trained weights of the 2-32-1 VAE, and the recorded ELBO, rebuild and KL curves every 20 steps). Reused byte-identical: `autograd.py`, `nt_ops_l1.py`. 11 Python code widgets, 38 mutants (the taught bug among each: prior left out of the posterior, log densities averaged, the variance for the sd, $\ln q$ without its variance, the rebuild term alone, $-\ln\sigma^2$ dropped, the log of an underflowed variance, one $\epsilon$ reused). Every training widget has an exact seeded test (`train_vae` 3 and 2 steps to 6 places; `vae_step` one step to 9 places); every Monte Carlo widget has short seeded runs compared exactly and long runs against a closed form.

## Self-check (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors; level warnings are only `O2-long-sentence` advisories and ladder canvas-kind changes.
2. `voice-scan.py 35 --summary`: 0 over 35 words, 0 lesson ids in code spans, 0 doubled words, 0 explanations over three sentences.
3. `node tools/run-number-scripts.mjs --only representations-L3` (strict): 250 of 250 checks, 0 uncovered, 42 literals (givens and how-line settings), exit 0, about 8 s.
4. `grade-all.mjs --code` on all seven files: 71 widgets and 11 code widgets, 0 failures. Playthrough with `--local-cdn`, desktop and `--mobile`: all passed (end of this file). `fresh-check.mjs --file` on review, homework and problems: 0 hits after rewording one homework stem; `same-course-reuse.mjs`: no error for this course after removing `eigen` l11's matrix from a problem's explanation (only advisories remain: a taught formula restated in problems-3).

## Timing (Pyodide 0.27.7 under node, desktop, per hidden test)

`train_vae` 200 steps 835 ms (budget 8,000, limit 13 s); `kl_numeric` 200,000 draws 159 ms; `elbo_mc` 100,000 draws 91 ms; `mc_marginal` 100,000 draws 50 ms; `vae_step` under 15 ms; every other case under 90 ms.

## Numbers and their sources (route A generator, route B number script)

- l9: guesses 0.52, $-1.19$, 1.97 (atan2); $\ln p = 3.97$ (math); five draws and their mean (loops); 2.77 by SciPy `quad`; ten 20- and 2,000-draw estimates (loops); posterior peak 0.5 (loop); 1.25; $-1.15$ from $-15.28/13.32$ (Fractions); 7 in 100 draws within 0.1 (erf).
- l10: $\ln p(\mathbf x) = -2.014$ (2 by 2 inverse by hand); posterior $\mathcal N(14/15, 1/6)$ (Fractions); the ELBO never above the line on the slider grid; KL 0.915 (closed form and `quad`); gap 4.22 equals the KL to the posterior; the three guesses' terms.
- l11: every quoted KL by the closed form and by `quad`; the Monte Carlo table by chunked sums; 2.807 by `quad`; $-0.495$ and 1.808; 6.41; 0.818; 0.163 by `quad`.
- l12: 0.5839, 2.677, 0.648, $-2.03$ (math); the VAE retrained by a hand-written backward pass and Adam: starting weights to $10^{-5}$, trained weights to about $10^{-3}$ (3,700 steps), curves within 0.01 nats; KL settles at 2.40; distances 0.038 and 0.011 (loops); four-code KLs 0.0, 1.0, 0.0, 1.6 to 1 place by hand backprop.
- Sets: every key by closed form, Fractions or `quad`; thresholds of the sampling and training widgets checked on four or five seeds each with margin (`train_vae` loss at most 0.45 against the 0.8 test; samples within 0.012 of the circle against 0.025; `mc_marginal` within 1.2% against 2%).

## Conventions

- Rows are points; codes have one coordinate unless stated; the encoder outputs $\mu$ and the log-variance $\ell = \ln\sigma^2$; KL in nats.
- Decoder noise fixed at $s = 0.1$ for the VAE (`S_DEC`), $s = 0.05$ for l9's story; $\ln p(\mathbf x \mid z)$ keeps its constant $-\tfrac d2\ln(2\pi s^2)$, so losses are true negative ELBOs.
- Data: `circle_model(n, 0.05, seed)` ($z \sim \mathcal N(0, 1)$, points $(\sin z, \cos z)$ plus noise); the VAE trains on seed 0 with 500 points.

## Deviations from the brief

- The latent model's decoder is the circle map $(\sin z, \cos z)$ rather than a learned net in l9 and l10; l10's interactive bound uses the straight decoder $g(z) = z(1, 0.5)$, where every quantity has a closed form.
- `elbo_mc` and `two_terms` take the decoder noise `s` explicitly; `elbo_gap` takes the grid `zs`; `kl_numeric` draws from $q$ by `mu + sigma * eps`.
- `train_vae` returns the trained parameters; its threshold is on the loss at fixed noise. `vae_step` uses a plain gradient step of size `lr`.
- No autograd op was missing: `exp` and `log` are in v1.0.

## `representations_ops_l3.py` (v1.0): public names

- `S_DEC = 0.1`.
- `g_circle(z) -> (n, 2)`; `circle_model(n, s=0.05, seed=0) -> (X, z)`.
- `init_vae(d=2, hidden=32, k=1, seed=0) -> [We, be, Wm, bm, Wv, bv, Wd, bd, Wo, bo]`.
- `vae_encode(params, X) -> (mu, logvar)`; `vae_decode(params, Z) -> X_hat` (arrays or `Tensor`s; gradient-checked to relative $10^{-6}$).
- `circle_distance(X) -> float`.

## Proposed course.json change

None.

## Playthrough with and without --mobile

See the end of this file.

All seven files with `--local-cdn <pkgs>`, desktop and `--mobile` (440 px): all passed. l9 15 checks, l10 14, l11 15, l12 15, quizzes 3/3 each; review-3 9 of 9; homework-3 8 of 8, 36 of 36 marks, performance starter fails, longform marked by the button; problems-3 12 parts with `--why`, 21 typed slips routed. l9, l12, homework-3 and problems-3 were replayed at both sizes after their last edits. Screens read: the interactive ELBO plane with its live gap, the KL sliders, the reparameterisation graph and the four-code bars fit at 440 px.

No engine or canvas limit bent a teaching idea in this level, so no backlog bullet was added.
