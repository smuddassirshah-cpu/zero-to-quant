# Engine pass 9b (rule tightening)

Base b6974c12 on `claude/session-ah-engine-pass-1nzn58`, from the reader's verdicts in `docs/reviews/review-pass9-hits.md`. All rules are warnings; the validator ends at 0 errors. Tests: `test-validate-pass8`, `-pass9` (34), new `-pass9b` (15), `-pkg2` (37), `-band-rules`, `test-voice-scan`, `test-playthrough-text-overflow`, all green. The new `-pass9b` is not in `acceptance.yml` (outside my file list).

## Counts, before to after
| tag | before | after |
|---|---|---|
| `[rounding-tie]` | 72 | 9 (slip branch withdrawn, 63 gone) |
| `[working-band]` | 4 | 1 (whole-number ceilings skipped) |
| `[key-in-question]` | 28 | 5 (3+ significant digits, sign, two table values) |
| `[carry-band]` | 128 | 13 (12 on slips, 1 new carried-value hit) |
| `[no-chain]`, `[slip-in-key-band]`, `[shown-arithmetic]` new shapes | 7, 2, 2 | unchanged |
| `[band-edge]` (1203), `[later-key]` (1205) | new | 10, 10 |
| doubled word (1209, voice scan) | new | 10 |

`p-grid-budget` was a stale hit: its question was reworded after the list was made; the rule is deterministic (two runs identical).

## Item 1182
Today's `[carry-band]` did not catch it (it compares wrong bands only). I extended it to hold "0.2200 from part 3" against part 3's printed working; tested on the old text (commit 9a5a0937). One hit on content: `validation/problems-1` `p-rent-seeds` part 2.

## `[carry-band]` sample
Of 20 of the first 128 hits, 0 were faults. Cause: the carry was exact (integer, formula, given, or the stored key) or the slip too small to move. The rule now needs a rounded carry within 1% of the source key and warns only when the slip's band is under |slip| x that relative error; exact whole-number slips are skipped.

## Other
Mobile overflow now names the widest maths span (`the maths span $...$ (N px wide)`). Backlog: 1154, 1190, 1210 post-completion; 1158 with the gallery fix pass; 1182, 1203, 1205, 1209 done. Remaining unjudged hits: `docs/reports/engine-pass-9b-hits.md` (54).
