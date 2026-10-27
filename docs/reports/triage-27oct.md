# Triage of four orphan lessons (27 Oct 2026)

Each lesson's author was stopped before finishing their level. Checks: validator, playthrough with the local CDN, brief coverage, every number recomputed in CPython (NumPy 2.5.3, SciPy 1.18.1, statsmodels 0.15.0), and every code solution and starter run against its hidden tests in CPython and Pyodide. All four are kept. The next level author builds on them and does not rewrite them.

## garch/l5-recent-days-more (level 2)
- Keep and build on it. It has 11 screens and 4 quiz items. Validator: 0 errors. Playthrough passed (15 checks). Both code solutions pass and both starters fail.
- It covers the whole brief entry: the crash hook, the weights explore, the five-day table, the λ sweep, the look-ahead trap, λ = 0 and 1, the flat forecast and the margin-desk transfer. One change from the brief: the starter supplies `ewma_vs_pandas` and the learner writes `pandas_ewma`.
- I recomputed every number and all agree: day 1,520; 71.0%; 0.8857% against a true 0.9649%; the correlations 0.9705, 0.9997, 0.9863, 0.9321 and 0.7531; MSE 3.85 against 4.35; 2.2566%.
- Fixed: the transfer explanation now has three sentences, not four. Quiz 2's `vol` feedback was misleading, because 1.47 is also the volatility of the right answer. Two long sentences are shorter. Still to write: l6, l7, l8, review-2 and homework-2.

## garch/l9-forecasting-vol (level 3)
- Keep and build on it. It has 12 screens and 4 quiz items. Validator: 0 errors. Playthrough passed (16 checks). Both code solutions pass and both starters fail.
- It covers the whole brief entry: the peak-storm hook, the h-step forecast, both ladders, the 5-day term structure, the √h trap, EWMA against GARCH, the edge cases, the derivation, all four code functions and the options-desk transfer. The brief gives the peak as 2.6154% on day 1,404. The correct figure is 2.6159%, forecast on the evening of day 1,403, and the lesson uses it.
- I recomputed every number. Two were wrong and are now fixed: on screen 2, 0.64% is now 0.63%. On screen 7 the calm-day figures were for 252 days, not 250, so 14.57% and 14.85% are now 14.52% and 14.79%. Everything else agrees, including the fit (0.0121, 0.0629, 0.9235) and the 25.42%, 35.17% and £7.60 figures.
- Also fixed: a claim that level 2 "distrusted such fits", which level 2 does not yet contain, and two `how` lines of about 50 words each. Level 2's l7 and l8 must deliver the persistence 0.9864, a long-run sd of 0.9426% and the 50.62-day half-life that this lesson quotes.

## coint/l1-two-walks (level 1)
- Keep and build on it. It has 12 screens and 4 quiz items. Validator: 0 errors. Playthrough passed (16 checks). All three code solutions pass and all three starters fail. statsmodels 0.14.4 in Pyodide and 0.15.0 in CPython give the same answers.
- It covers the whole brief entry: seed 103, the reseed explore, the R² and |t| histograms, the three code screens, the residual memory, the n = 2,000 rate, the normal-null trap, the AR(1) edge case and the interview transfer.
- I recomputed every number and all agree: −1.9236, −34.5924 and 0.7061; 44 of 1,000 pairs with R² of at least 0.70; a median of 0.1707; 90.0%, 4.4%, 72.8%, 82.0% and 95.2%; 43 pairs at least as extreme; a t sd of 16.3; DW 0.07; 74.3% for the AR(1) pairs.
- Fixed: the trap credited the 10⁻¹³⁴ p-value to N(0, 1), which actually gives about 3·10⁻²⁶²; the figure is statsmodels' t(498) value, and the prose now says so. Two long sentences are shorter. Still to write: l2 to l4, review-1 and homework-1.

## contests/l1-reading-statements (level 1)
- Keep and build on it. It has 12 screens and 4 quiz items. Validator: 0 errors. Playthrough passed (15 checks). Both code solutions pass and both starters fail. The 200,000-value cases finish quickly with the O(n) solution.
- It covers the whole brief entry: the statement anatomy, the many-test sum bound, the 64-bit total, the tie and n = 1 edge cases, the negative-values trap, `parse` and `new_highs`, and the online-assessment transfer.
- I rechecked every count and bound and all agree: 4; 200,000; 2·10¹⁴; 1; 2; 290,001; 10¹²; 3; 10¹¹.
- Fixed: one long sentence in the `parse` prose. The title screen describes a 5 s limit per test case. That matches `app/js/engine/widgets/code.js`, but KNOWN_ISSUES still describes a pooled budget and should be updated. Still to write: l2 to l4, review-1 and homework-1.
