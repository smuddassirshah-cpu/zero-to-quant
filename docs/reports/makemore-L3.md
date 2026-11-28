# makemore level 3 (Sampling and held-out loss): report

## Files

| File | Screens or items | Quiz |
|---|---|---|
| `l9-sampling-names.json` | 10: problem which list is the MLP's (`console`, bigram and MLP samples, seed 3), explore $u$ on the running totals (`number-line` with intervals and a draggable $u$), name the sampling rule and draw baa by hand (`table` widget, one $u$ equal to a running total), ladder seeds, ladder 19.4% of 500 MLP draws are training names (bigram 9.8%), trap argmax writes alee for ever, ladder the 20-letter cap, ladder edge the last total `0.9999999999999999` and the cap at 26, code `sample_name`, transfer synthetic price paths. 15 min | 3 |
| `l10-train-dev-test.json` | 10: problem a loss on what (`table` of both models on three sets), explore splitting by names against by rows (`array` with bands and a `frames` control), name the three jobs, ladder the honest test gap (0.2960), ladder what goes in the report, trap choosing on test ("no longer held out"), ladder 390 dev names repeat training names, ladder edge the bigram's dev below its train, code `split_names`, transfer a fund's live period. 14 min | 3 |
| `l11-overfitting.json` | 9: problem predict the 1,000-name run, explore the recorded run (`series`, reveal control, least-dev line at step 2,000, bigram line), name overfitting (gap 1.5447 at 20,000), ladder reading the gap, ladder the full-data MLP, trap a falling training loss, ladder edge the bigram cannot overfit, code `best_checkpoint` and `fit_and_gap` (a graded 200-step run on 200 names), transfer fifty stocks. 15 min | 3 |
| `l12-temperature.json` | 9: problem which list is the safest (`console` at $T$ = 1.5, 0.5, 1), explore the first-letter chances at three temperatures (`bars` with a `frames` control), name temperature as a power (the ai-basics link), ladder the two limits ($T = 100$ gives 3.2674), ladder dev loss against $T$ (least at 1 of those listed, 1.01 on a fine grid), trap a different model?, ladder edge $T = 1$, code `softmax_t`, transfer risk scenarios. 14 min | 3 |
| `review-3.json` | 10 items, difficulty 2 to 4, `pass: 0.8`; mk-eval 6, mk-train 4 | |
| `homework-3.json` | 7 items, difficulty 3 to 5: code `avg_loss` and `evaluate_and_choose` (5), code `dev_losses_at` (4), order an honest comparison with a distractor (4), numeric temperature 2 (3), choice which checkpoint (4), longform forty settings on the test set (5, rubric 10), performance code `sample_names` and `dev_loss` (4) | |
| `problems-3.json` | 3 chained problems, 11 parts: a planted four-way distribution sampled at $T = 1$ and $T = \tfrac12$ (5; l9, l12), checkpoints (4; l10, l11), a small split (3; l10) | |

7 Python code widgets, 29 mutants, the taught bug among each widget's (side left, no cap at 26, no length cap, argmax, choosing on test, scoring every model on test, power $T$, multiplying by $T$, no maximum taken out, keeping the later tie, training on dev). The no-length-cap mutant is marked `"timeout": true`.

## Self-check (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors; level 3 warnings: two problem screens without a canvas and `O2-long-sentence` advisories under 35 words. No `[ai-mutants]` warning.
2. `voice-scan.py 35 --summary`: 0 over 35 words, 0 lesson ids in code spans, 0 doubled words, 0 explanations over three sentences.
3. `docs/reports/makemore-L3-numbers.py` (venv): exit 0, 162 of 162 checks; it prints the topic exit. The 10 "check by hand" lines were read; each states the working of its slip.
4. `grade-all.mjs --code` on the seven files: 69 widgets and 7 code widgets, 0 failures after three fixes (a mutant test number, a no-maximum mutant that passed at logits of 1,000, now 2,000, and the timeout mark). Playthrough with `--local-cdn --mobile --why`: all passed (l9 13 checks, l10 13, l11 12, l12 12, quizzes 3/3; review 10 of 10; homework 7 of 7 with the performance starter failing and the longform marked; problems 11 parts, 7 slips routed); l9 and l11 replayed after their last edits. Screenshots at 440 px: two fixes (the l11 gap ladder showed a gap column that gave the answer; the l9 number-line's interval label sat on $u$'s label). `fresh-check.mjs --file problems-3.json`: 0 hits after rewording one feedback line.

## Topic exit (stated by the number script)

Bigram (add-one counts from the training names): dev 2.4514, test 2.4702. MLP (supplied weights): dev 2.1609, test 2.1742. The MLP beats the bigram on both held-out sets, by 0.2905 nats on dev and 0.2960 on test.

## Numbers (route A: searchsorted sampling, vectorised losses, softmax of $z/T$; route B: a running-total walk, chances to the power $1/T$, the autograd for the short run)

- Samples from the supplied weights with the course rule reproduce the brief's recorded lists at $T$ = 0.5, 1 and 1.5 (seed 7) exactly. Seed 3: bigram acli, ja, n, ilemiyanic, zahonar, na; MLP aitlane, naleightende, zakynel, naelynn, ordonan, prayel. Of 500 draws at seed 11, 19.4% are training names (the brief's 19.6% used `rng.choice`), the bigram's 9.8%; 2 of the MLP's 500 hit the 20-letter cap; argmax writes alee.
- Split: 25,626, 3,203, 3,204; 29,494 different names in 32,033 lines; 390 dev and 417 test names repeat a training name.
- Overfitting run (hidden 300, 7,226 rows, 17,697 weights): the brief's five points; least dev 2.4568 at step 2,000 of the 250-step checkpoints, never below the bigram. Graded short run (200 names, 200 steps): train 2.4230, dev 2.6550; thresholds 2.54 and 0.1. Exact 5-step test on 30 names: 3.057203 and 3.167851.
- Temperature: first-letter chances of a at $T$ = 0.5, 1, 2: 0.3342, 0.1502, 0.0831. Dev loss at 0.5, 0.9, 1, 1.1, 1.5, 2, 100: 2.5456, 2.1694, 2.1609, 2.1650, 2.2392, 2.3630, 3.2674; least at 1.01 on a 0.01 grid, 0.00007 below $T = 1$.
- Sets: toy loss 1.206043; MLP on 500 dev names below 2.4514; homework temperatures 2.5456, 2.1609, 2.2392; problems: 0.55 picks b at $T = 1$ and a at $T = \tfrac12$.

## Conventions

The sampling rule, the split and the supplied weights are levels 1 and 2's. Every graded sample comes from a planted model or the supplied weights with the course rule, never from `rng.choice`. Level 3 ships no `autograd.py`: l11's graded run uses a NumPy training loop given in the prelude, and the learner composes it (with an exact 5-step test and two thresholds).

## Brief notes

- The brief's overfitting text says dev rises "from about step 1,000"; with checkpoints every 250 steps the least dev loss is at step 2,000 (2.4568 against 2.4586 at 1,000), so the lesson marks step 2,000.
- The 500-sample share is 19.4% with the course rule (19.6% in the brief with `rng.choice`); the lesson states 19.4%.

## Proposed course.json change

None.
