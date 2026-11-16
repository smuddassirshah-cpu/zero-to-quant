# Engine pass AF part 1

Items 1060 to 1081 numbered (inbox cleared); 1075, 1076, 1080 done, 1078 partly (status lines in `ENGINE-BACKLOG.md`).

Built: `tools/retold-reuse.mjs` (kinds `retold` and `rate`, errors, waivable), `fbOf` in `same-course-reuse.mjs` (feedback, explain, why read), per cents read as fractions in the numbers kind and the pair shape, `tools/retold-model.json` (stock sentences and word frequencies learned over `app/content`, `--learn`), `tools/reuse-hits-report.mjs`.

True positives: 8 of about 31 reuse findings in the seven reviews fire as fixtures built from git (`test-fresh-check-retold-af.mjs`, 10 positive and 13 negative cases, plus a chain case, a pair-with-per-cent case and waiver and exit-code cases): ensembles 3; validation 5, 8, 13, 14; fin-ml 1 (rate); delta AE-2 3; AE-4 1.

Not reached: paraphrases with several words changed per sentence (ensembles 1 and 4, validation 6, 7, AE-3 1, 2, 4, 5, AE-4 2, 5, 8 to 10, AE-2 1, 2), a story told in another course (stat-learning 4), shared numbers (stat-learning 8, an existing kind), the fin-ml Kelly story (no shared sentence), the topic exam (not a course file).

Hits over the 128 sets: 94 new (retold 90, rate 4), below 150, so no loosening needed; thresholds were tuned to keep every positive above. `same-course-reuse.mjs --all` takes about 40 seconds.

CI: the `static` job step "Same-course reuse" fails until the 94 hits are fixed or waived.
