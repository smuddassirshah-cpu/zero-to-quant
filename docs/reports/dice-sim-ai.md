# dice-sim canvas (ENGINE-BACKLOG 1217, session AI)

New canvas kind `dice-sim` (a kind of its own: bars is a distribution chart, this is one yes-or-no rule on a roll). Params `dice`, `sides`, `keep` (sim expression over `d1..dn`, `dice`, `total`), `trials`, `seed`, `exact`, `exactLabel`, `max`, `labels`; state `ran`. Draws the latest dice (kept: orange outline and "Kept"; filtered: faded and "Filtered out"), counters Rolled / Kept / Filtered out, a share bar and a running-share trace with the exact line. Run and Reset sit in `.cvb-extra`, so `controlsAfter` holds them with no player change. Reduced motion shows the final state at once; an `aria-live` region speaks the totals after each batch. Seed 4226 with two dice reproduces the prototype's rolls exactly (1,000 rolls, 308 kept, last roll 3 and 6).

Third counter: the prototype's "Total 10" counted kept rolls with total 10 (its share bar was about that). The brief wants the kept share, so the third counter is "Filtered out" (rename with `labels.out`).

Files: `app/js/engine/canvas/dice-sim.js`, `css/canvases.css`, `index.html`, `js/screens/system.js` (two gallery entries), `tools/validate.mjs` (known kind, param rules, counts as a movable canvas), README and AUTHORING, backlog 1217.
Tests: `tools/test-dice-sim.mjs` (desktop, `--mobile`; fixture `tools/fixtures/dice-sim/l1-dice.json`): gating, counters add up, last trace point at Kept/Rolled, seed determinism, Reset repeats, reduced motion; `tools/test-validate-dice-sim.mjs`. Both in `acceptance.yml`. Shots in `scratchpad/dice-sim/`.

Widget fit: 1,000 rolls at seed 4226 keep 308; the numeric widget (answer 305, tol 25, range 280 to 330) accepts it.

Content change for `l3-shrinking` simulate screen: replace `canvas` with

```json
"canvas": {
  "kind": "dice-sim",
  "params": { "dice": 2, "keep": "d1 == 5 || d2 == 5", "trials": [10, 100, 1000], "seed": 4226, "exact": "11/36" },
  "controlsAfter": "check",
  "state": { "caption": "Filter: keep a roll when at least one die shows a 5" }
}
```

`explain.canvas: { "ran": 1000 }` works unchanged.
