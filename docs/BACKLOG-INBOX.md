# Engine backlog inbox

Content agents append their engine and canvas limitations here, under `Raised later (<course> level <n>):`, as bullets. An integration pass numbers them into `ENGINE-BACKLOG.md` and clears this file.


Cleared by engine pass 9 (items up to 1210 in `ENGINE-BACKLOG.md`); the previous text is in the commit before it.
Raised later (problems author pass AH, topology and pdes):
- Reader number scripts key on an item's old text and numbers, so an author re-authoring a problem must edit another agent's script to keep CI green (`delta-review-delta-ag-topology-numbers.py`, `delta-review-delta-ag-pdes-numbers.py`, `problems-pdes-numbers-read.py` were guarded by hand here). A helper in `numbers_lib` that skips a reader's block when the item's hash differs from the one it read, printing "stale: re-authored", would make this mechanical.
Raised later (problems validation, p-spread-blocks re-author):
- The `slip` grammar has no `ceil` or `floor`, so a packing or count slip such as $\lceil 200/7 \rceil = 29$ must be written as an equivalent sum (`1 + 196/7`). Adding `ceil` and `floor` to `slip_eval` and the validator would let the slip name the mistake directly.
- (session AH, from `docs/reviews/review-pass9b-hits.md` rule verdicts; post-completion) Tighten `[later-key]` (skip the entry's own value, stem figures, the part's own `feedback.correct`, matches under four significant digits: 0 faults in 10), `[no-chain]` (normalise expression keys, cue words for whole-number keys: 0 in 7), `[slip-in-key-band]` (skip the key's own unrounded form: 0 in 2), `[carry-band]` (judge by the `slip` expression, skip whole-number slips: 1 in 12); `[band-edge]` drops "by a float margin" and stays silent when `accept` names the neighbour (7 faults in 10: keep); doubled word allows "million" and takes waivers.
