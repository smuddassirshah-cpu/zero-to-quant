# markov level 2: performance task

- File `app/content/courses/markov/homework-2.json`, item `hw-absorb-code`, index 8 (item 9 of 9, appended; cap 12, nothing converted). Kind `code` (Python, NumPy allowed), difficulty 5, skill `mc-firststep`, pace 1200 s.
- Objective matched (l8): "Write the absorption probabilities as $(I - Q)^{-1}R$ and check one numerically." The only verb-rule objective in the level.
- Product, from three stubs: `absorb_chances(P)` (full $H$), `steps_to_absorb(P)` ($t = (I - Q)^{-1}\mathbf{1}$), `simulate_absorb(P, start, runs, seed)` (the numerical check). Hypothesis in the prose: every other state can reach an absorbing state.
- Tests: 12 hidden, 2 examples, on six chains (tennis at deuce with ends in the middle, a lazy six-state chain with three ends, a cycle, all-absorbing). Simulation bands are at least 7 standard errors. Nine planted bugs each fail a test (ends taken as the last states, any self-loop read as absorbing, $R$ alone, $I + Q$, no $+1$, absorbing rows 0, counts, a coin per entry, a step cap).
- Overlapping screens: l8 screens 5 and 8 and l7 screen 8 lay out $H = (I - Q)^{-1}R$ and $t = 1 + Qt$ by hand; `hw-matrix-derive` and `hw-loan-book` derive and use them. New: code from a blank start, ends found from the diagonal anywhere in the order, three ends, no moving states, the simulation check, the tennis chain.

## Gates

1. Validator, `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; expected warning "markov/L2: has a performance task, remove from perf-pending".
2. Voice, `VOICE_BASE=app/content/courses/markov python3 docs/reviews/voice-scan.py 35`: 0 sentences over 35 words; 3 explanations over three sentences, all in `l19-optional-stopping.json` and present before this change (untouched); 0 in this item.
3. Numbers script, `<venv>/bin/python docs/reports/markov-2-perf-numbers.py`: exit 0. Fractions Gauss-Jordan, SymPy inverse, tennis closed forms $p^2/(p^2 + q^2) = 9/13$ and $2/(p^2 + q^2) = 50/13$, a seeded 100,000-run simulation per chain; solution passes 12 of 12, starter fails 12 of 12, every bug fails.
4. Playthrough, `node tools/playthrough.mjs --set markov/homework-2 --local-cdn <pkgs>`, with and without `--mobile`: All passed (performance starter fails). Shots at 1280 and 440 px read: no sideways scroll.

Freshness: `fresh-check.mjs --file` gives no hit on this item (one older hit, items[4] against review-2). Grep terms: `tennis`, `deuce`, `absorb_chances`, `steps_to_absorb`, `simulate_absorb`, `(I - Q)^{-1}`, `np.linalg`. Backlog: 0 bullets. No course.json change.
