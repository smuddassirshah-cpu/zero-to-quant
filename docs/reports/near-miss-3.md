# Near-miss pass, part 3 (62 drills)

Outcome: 2 existing plants marked, 60 near-misses written, 0 tests added (every near-miss already fails a hidden test). `planted-check --near-miss` in the real runtime: 0 failures in every batch. Validator: 0 errors, no `[near-miss]` warning on any drill in this list.

Native-run note: a time-based near-miss was checked with a 6 s per-test alarm in CPython; the page is slower, so each also fails there.

## Per drill (existing = marked an existing plant; new = wrote new)

- ci-word-split: existing, DP trying every code at each position, not each code length.
- ci-zero-quads: existing, fix three lists and look up the fourth, cubic.
- dsa-bracket-partners: new, scan back from each closer, quadratic on deep nesting.
- dsa-budget-stretch: new, extend from every start, quadratic.
- dsa-cheap-pairs: new, sorted early break but visits every pair, quadratic.
- dsa-climb-limit: new, BFS limiting drops too (abs), blocks legal descents.
- dsa-closest-hedge: new, bisect partner but lets a size pair with itself.
- dsa-closest-level: new, flatten tree and scan all levels per query.
- dsa-common-manager: new, re-searches both subtrees at each level, size times depth.
- dsa-cover-opening: new, rescans all shifts after each pick, quadratic.
- dsa-depth-block: new, running minimum from every start, quadratic.
- dsa-double-booked: new, compare every pair, quadratic when no clash.
- dsa-empty-orders-back: new, remove(0) per zero then append, quadratic.
- dsa-feed-passes: new, table walked over every calendar day to 10^9.
- dsa-fills-in-order: new, slices tape for every plan id, quadratic.
- dsa-first-overdrawn: new, slice sum from day 0 each day, quadratic.
- dsa-flattest-stretch: new, prefix sums but all pairs compared, quadratic.
- dsa-footpath-slabs: new, right recurrence recursed 500,000 deep (RecursionError).
- dsa-forced-order: new, rescans all jobs each step to find ready ones.
- dsa-free-desk-square: new, tests every square at every corner cell by cell.
- dsa-kiosk-change: new, greedy paying a 20 with three 5s first, no exchange case.
- dsa-kiosk-spacing: new, raises the gap one metre at a time, up to 10^9 steps.
- dsa-kth-repeat: new, slice-count of earlier ids at each position, quadratic.
- dsa-lift-buttons: new, BFS with a visited list and `in`, quadratic.
- dsa-loop-depots: new, drive the loop from every depot, quadratic.
- dsa-looping-route: new, walks every one of 10^15 steps.
- dsa-majority-reading: new, Boyer-Moore candidate without confirming pass.
- dsa-missing-seq: new, linear scan, too slow for 2,000 calls on a million.
- dsa-near-trades: new, early-break inner scan but counts every pair, quadratic.
- dsa-nearest-strikes: new, pick nearest remaining k times, quadratic.
- dsa-net-tape: new, rebuilds the resting list by slice per sell, quadratic.
- dsa-oncall-rota: new, extend a run from every start, quadratic.
- dsa-peak-calls: new, processes ties event by event, splits one busy stretch.
- dsa-price-peak: new, linear scan for first drop, too slow for 2,000 calls.
- dsa-print-queue: new, min over a plain waiting list each time, quadratic.
- dsa-range-volumes: new, recount rises in each range, quadratic.
- dsa-rotate-rota: new, k mod n single moves with insert(0), quadratic.
- dsa-route-order: new, linear search of legs per stop, quadratic.
- dsa-sensor-alarm: new, resums each window of k, quadratic for large k.
- dsa-server-loads: new, prunes on best but no equal-load skip, 12 identical servers blow up.
- dsa-shallowest-leaf: new, min of children without the one-child case.
- dsa-shared-tail: new, tests B's nodes against a list of A's, quadratic.
- dsa-shift-pay: new, right recurrence recursed one day per call, too deep.
- dsa-short-codes: new, `startswith` against every name per prefix, quadratic.
- dsa-shortest-cover: new, every window checked per parcel, quadratic.
- dsa-silent-sensors: new, `in` on the log list per sensor, quadratic.
- dsa-spare-cables: new, groups minus one without the n - 1 cables check.
- dsa-split-prices: new, length pruning only, no reachability table, tens of millions of cuts.
- dsa-staff-per-hour: new, adds one to every slot of every shift, quadratic.
- dsa-stamp-gaps: new, table run downwards, so each stamp used at most once.
- dsa-stock-ledger: new, list of items searched per line, quadratic.
- dsa-swapped-levels: new, swaps only around the first drop, misses far-apart swaps.
- dsa-ticker-batches: new, batch ends at first ticker's last trade only.
- dsa-ticket-desk: new, recounts waiting tickets at each arrival, quadratic.
- dsa-total-booked: new, merge takes new end not the max, nested booking shrinks run.
- dsa-trace-shapes: new, `list.count` of each shape key, quadratic.
- dsa-traders-by-ticker: new, `trader in list` before append, quadratic.
- dsa-trailing-stop: new, max of all earlier prices per tick, quadratic.
- dsa-upstream-stations: new, one search per reached station to r, quadratic.
- dsa-varied-windows: new, builds a set per window, quadratic for large k.
- dsa-window-every-venue: new, each start bisects every venue, N times k.
- dsa-winning-stretch: new, running score from every start, quadratic.

## Tests added

None.

## Not done

None.

## Statement or model faults seen

None. Notes only: dsa-footpath-slabs and dsa-shift-pay near-misses rely on RecursionError at 500,000 and 200,000 calls deep (the existing large tests); dsa-feed-passes fails on the 10^9-day tests by time, not on the small ones.
