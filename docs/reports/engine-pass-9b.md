# Engine pass 9b (rule tightening)

From the reader's verdicts in `docs/reviews/review-pass9-hits.md`. All rules are warnings; the validator ends at 0 errors. Green: `test-validate-pass8`, `-pass9`, new `-pass9b` (not in `acceptance.yml`, outside my file list), `-pkg2`, `-band-rules`, `test-voice-scan`, `test-playthrough-text-overflow`.

## Counts, before to after
- `[rounding-tie]` 72 to 9 (slip-past-places branch withdrawn)
- `[working-band]` 4 to 1 (whole-number ceilings skipped)
- `[key-in-question]` 28 to 5 (three or more significant digits, sign, two table values)
- `[carry-band]` 128 to 13
- `[no-chain]` 7, `[slip-in-key-band]` 2, `[shown-arithmetic]` new shapes 2: unchanged
- New: `[band-edge]` (1203) 10, `[later-key]` (1205) 10, doubled word (1209, voice scan) 10

`p-grid-budget` was a stale hit (its question was reworded after the list); the rule is deterministic.

## Item 1182
Today's `[carry-band]` did not catch it (it compared wrong bands only). It now holds "0.2200 from part 3" against part 3's printed working; tested on the old text (9a5a0937). One content hit: `validation/problems-1` `p-rent-seeds` part 2.

## `[carry-band]` sample
Of 20 of the first 128 hits, 0 were faults: the carry was exact (integer, formula, given, stored key) or the slip too small to move. Now a rounded carry within 1% of the source key is needed, and a slip is reported only when its band is under |slip| times the carry's relative error. Exact whole-number slips are skipped.

## Other
The mobile overflow message names the widest maths span. Backlog: 1154, 1190, 1210 post-completion; 1158 with the gallery fix pass; 1182, 1203, 1205, 1209 done. Unjudged hits: `docs/reports/engine-pass-9b-hits.md` (54).
