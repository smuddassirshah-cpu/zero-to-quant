# markov level 4: performance task

- File `app/content/courses/markov/homework-4.json`, item `h-mh-network`, index 9 (item 10 of 10, appended; cap 12, nothing converted). Kind `code` (Python, standard library), difficulty 5, skills `mc-longrun`, `mc-chains`, pace 1200 s.
- Objective matched (l15): "Build a Metropolis chain whose long-run shares are a chosen target". The only verb-rule objective in the level.
- Product, from two stubs: `mh_network_matrix(n, edges, w)`, the exact Metropolis-Hastings matrix for a neighbour proposal with chance $1/\deg(i)$, and `mh_network_shares(...)`, a seeded run returning visit shares. Hypotheses in the prose: a connected network, positive weights; the explain says why the law is unique and the shares converge.
- Tests: 11 hidden, 1 example: exact matrices (path, star, kite, two venues), $\pi P = \pi$ through a prelude `stationary_gap`, rows, link order and weight scale, two 100,000-step runs (band 0.04, at least 7 standard deviations of a correct run). Nine planted bugs each fail a test: plain Metropolis, ratio upside down, no min, no diagonal, links one way, proposal over every venue, shares dropping rejections, shares without the ratio, counts.
- Overlapping screens: l15 screens 4, 8 and 9 lay out detailed balance for Metropolis, the Hastings rule and a $\pm 1$ sampler with visit shares; l14 screens 2 to 4 the degree law; `h-metropolis-continuous` a symmetric sampler. New: a proposal that is not symmetric because degrees differ, the exact matrix with rejections on the diagonal, any connected network.

## Gates

1. Validator, `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; expected warning "markov/L4: has a performance task, remove from perf-pending".
2. Voice, `VOICE_BASE=app/content/courses/markov python3 docs/reviews/voice-scan.py 35`: 0 over 35 words; 3 explanations over three sentences, all in `l19-optional-stopping.json`, there before this change; 0 in this item.
3. Numbers script, `<venv>/bin/python docs/reports/markov-4-perf-numbers.py`: exit 0. Fractions build with exact balance and $\pi P = \pi$; SymPy null space of $P^T - I$ one-dimensional and spanned by the weights; plain Metropolis off target (star law 1/3, 1/9, 2/9, 1/3); an independent seeded NumPy run; solution 11 of 11, starter 0 of 11, every bug fails, share bugs miss by over 0.18 on every seed.
4. Playthrough, `node tools/playthrough.mjs --set markov/homework-4 --local-cdn <pkgs>`, with and without `--mobile`: All passed. Shots read at 1280 and 440 px; only the known coach toast.

Freshness: `fresh-check.mjs --file` gives no hit on this item (one older hit, items[6] against l16). Grep terms: `Hastings`, `deg(`, `hub`, `mh_network`, `KITE`, `stationary_gap`, `1/9`. Backlog: 0 bullets. No course.json change.
