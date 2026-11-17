# dice-sim canvas (ENGINE-BACKLOG 1217, session AI)

New canvas kind `dice-sim` (a kind of its own: bars is a distribution chart, this is one yes-or-no rule on a roll). Params `dice`, `sides`, `keep` (sim expression over `d1..dn`, `dice`, `total`), `trials`, `seed`, `exact`, `exactLabel`, `max`, `labels`; state `ran`. Draws the latest dice (kept: orange outline and "Kept"; filtered: faded and "Filtered out"), counters Rolled / Kept / Filtered out, a share bar and a running-share trace with the exact line. Run and Reset sit in `.cvb-extra`, so `controlsAfter` holds them with no player change. Reduced motion shows the final state at once; an `aria-live` region speaks the totals after each batch. Seed 4226 with two dice reproduces the prototype's rolls exactly (1,000 rolls, 308 kept, last roll 3 and 6).

Prototype match (coordinator review): optional `event: { rule, label, exact, exactLabel }`. With it the third counter counts kept rolls where the event holds, and the share bar and trace show event / kept (trace axis in kept rolls), as the prototype did with "Total 10". Seed 4226, 1,000 rolls: 308 kept, 28 with total 10, share 0.091 (1/11 = 0.0909), identical to the prototype's figures. Without `event` the canvas shows the kept share against `exact`, as before.

Files: `app/js/engine/canvas/dice-sim.js`, `css/canvases.css`, `index.html`, `js/screens/system.js` (two gallery entries), `tools/validate.mjs` (known kind, param rules, counts as a movable canvas), README and AUTHORING, backlog 1217.
Tests: `tools/test-dice-sim.mjs` (desktop, `--mobile`; fixture `tools/fixtures/dice-sim/l1-dice.json`): gating, counters add up, last trace point at Kept/Rolled, seed determinism, Reset repeats, reduced motion; `tools/test-validate-dice-sim.mjs`. Both in `acceptance.yml`. Shots in `scratchpad/dice-sim/`.

Widget fit: 308 kept of 1,000 at seed 4226; the numeric widget (answer 305, tol 25, range 280 to 330) accepts it.

Content change for the `l3-shrinking` simulate screen: replace `canvas` with

```json
"canvas": {
  "kind": "dice-sim",
  "params": {
    "dice": 2, "keep": "d1 == 5 || d2 == 5", "trials": [10, 100, 1000], "seed": 4226,
    "event": { "rule": "total == 10", "label": "Total 10", "exact": "1/11", "exactLabel": "1/11" }
  },
  "controlsAfter": "check",
  "state": { "caption": "Filter: keep a roll when at least one die shows a 5" }
}
```

The prototype counted a kept roll as a hit when the two dice sum to 10 (`a + b === 10`), which is `total == 10` here. `explain.canvas: { "ran": 1000 }` works unchanged. The screen's question (rolls surviving the filter) reads the Kept counter, which stays visible.
