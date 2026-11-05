# Exam topic-1.7 extension (trees level 4)

Edited `app/content/exams/topic-1.7.json` only (plus `docs/briefs/trees-scripts/check_exam_1_7.py`).

## Items changed
- Item 20: `e-crr-q` replaced by `e-atm-rule` (d3, 3 numeric parts, skills `tp-bs`, `op-greeks`, tag `option-estimate`).
- Item 21: `e-greek-signs` folded to 3 parts (existing question verbatim as part 1; gamma peak choice; short-gamma P&L numeric). Tags `greek-signs`, `gamma-pnl`.
- Item 24: `e-bs-hedge` folded to 3 parts (table verbatim as part 1; digital call numeric; skew choice). Tags `digital-option`, `vol-smile`; skill `tp-riskneutral` added.
- Item 26: `e-american-put` folded to 2 parts (numeric 5.87 verbatim, with its canvas highlight, as part 1; ranking choice with Asian put 4.57). Tag `exotic-ranking`; skill `tp-riskneutral` added.

Items stay at 30; ramp 6/15/6/3 unchanged (positions and difficulties kept). `minutes` 60 to 70. Seven parts added, so 37 playable parts.

## Numbers
`docs/briefs/trees-scripts/check_exam_1_7.py`: 33 checks, each by two methods (math.erf against Simpson integration; enumeration against a price-and-running-sum recursion). Covers 15.00 (exact 14.95), gain 1.00 (0.9944), 8.66 (8.6347), gamma peak 94.18 and gamma 0.0198, P&L -316.80 and all four slips, digital 0.6316 (table route 0.6317) and slips 0.6412, 0.6943, 0.3535, call-spread limit, Asian 4.5669, American 5.87, European 5.25. No per cent keys changed; the old `e-crr-q` value 0.5052 appears nowhere else in the exam (the id is gone; redo entries resolve to nothing).

## Checks
- `node tools/validate.mjs`: 0 errors (manifest regenerated, not committed).
- `playthrough --exam topic-1.7` default, `--mobile`, `--tablet`, local CDN: all passed, 37 items played, 30 of 30, no crash.
- Screenshots not inspected individually; the part-1 explanation of `e-american-put` carries `canvas.highlight` of node `d`, and the item-level canvas stays on the item.
