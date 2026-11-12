# Near-miss pass, part 2

List: `nm-part-01` (64 `ci-` drills, `ci-merged-tape` to `ci-widest-banner`).

Outcome: 61 existing (marked an existing plant), 3 wrote new, 0 wrote new and added test.

Every marked plant fails at least one hidden test natively and in the real runtime (`planted-check --near-miss`, 13 batches, 0 failures). Validator 0 errors; 0 `[near-miss]` warnings for this list.

## Existing plants marked (drill, plant index)

ci-merged-tape 1; ci-mirror-pieces 3; ci-nearest-depot 0; ci-nested-crates 0; ci-no-repeat-rota 0; ci-one-bit-apart 0; ci-others-product 1; ci-paired-signals 3; ci-paving-ways 3; ci-peak-stretch 0; ci-pillar-queens 1; ci-price-ramp 1; ci-priced-edits 0; ci-product-stretch 1; ci-read-preorder 2; ci-ready-blocks 1; ci-rebuild-from-orders 1; ci-reclaimed-land 0; ci-reference-split 1; ci-relay-masts 0; ci-rest-days 0; ci-right-edge-view 0; ci-ring-bonuses 2; ci-ring-lookup 1; ci-ring-stalls 1; ci-ring-turns 1; ci-ring-waits 1; ci-robot-floor 1; ci-room-numbers 0; ci-rota-swaps 3; ci-row-column-matches 0; ci-safest-walk 1; ci-serial-runs 0; ci-shift-picks 3; ci-smooth-orderings 1; ci-spaced-picks 0; ci-spiral-cells 2; ci-steady-climbs 0; ci-stock-by-prefix 0; ci-stone-hops 0; ci-stop-cascade 0; ci-stuck-jobs 1; ci-switch-panel 4; ci-tape-decodes 1; ci-target-blocks 0 (time-based, confirmed in runtime); ci-three-feed-common 2; ci-three-leg-nets 3; ci-tick-ranges 1; ci-tolerant-common 0; ci-trace-count 0; ci-tray-queue 0; ci-trim-to-multiple 1; ci-two-desk-matches 0; ci-two-shift-rota 0; ci-unique-counts 0; ci-van-convoys 0; ci-van-pairs 2; ci-visible-masts 0; ci-wall-break-route 0; ci-wide-bars 1; ci-widest-banner 3.

## Wrote new (no plants existed)

- ci-pair-gaps: matches both x - k and x + k with no k = 0 case, so equal pairs count twice (fails 3 tests natively).
- ci-same-total-pairs: remembers the latest, not the largest, number per digit sum (fails 2).
- ci-split-points: loops over every number, so the cut after the last item counts when the total is 0 (fails 5).

## Tests added

None.

## Drills not done

None.

## Statement or model faults

None seen.

## Note

The worktree branch started from an unrelated history, so `claude/amazing-wright-d4mx7i` was merged with `--allow-unrelated-histories` (conflicts in `.gitignore`, `README.md`, `docs/curriculum.md` resolved to the claude side).
