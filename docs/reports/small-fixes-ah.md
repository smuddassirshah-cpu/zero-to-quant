## Session AH small fixes

1. `app/content/exams/topic-2.3.json`, item `e-honest-bar`: `pace` 150 to 90. Item paces now sum to 5,400 s against `minutes` 90. `docs/reviews/exam-2.3-scripts/numbers.py` asserted the old 5,460 s; it now asserts sum <= minutes x 60 and passes.
2. `app/content/courses/regression/problems-2.json`, `p-grocer-beta` prose.
   Before: "A supermarket chain's monthly excess returns are regressed on the market's over 50 months."
   After: "Over 50 months, the supermarket chain regresses its monthly excess returns against those of the market."
   The `[exam-reuse]` warning against topic-1.6 `s-alpha-beta-table` cleared on the first rewording; no waiver added.
3. `app/content/courses/testing/homework-3.json`, `items.8.widget.prompt`.
   Before: "Assess the claim. Check the vendor's $t$ and $p$; explain what the 200 variants change; compute what noise alone would give and the Bonferroni bar; say how long a record or what other evidence would convince you; list what you would ask the vendor for; give a verdict."
   After: "Assess the claim. Check the vendor's $t$ and $p$, then explain what the 200 variants change. Compute what noise alone would give, and the Bonferroni bar. Say how long a record, or what other evidence, would convince you. List what you would ask the vendor for, and give a verdict."
   voice-scan 35 on the testing folder: 0.
