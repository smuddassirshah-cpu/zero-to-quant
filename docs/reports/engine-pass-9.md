# Engine pass 9 (session AH)

Base 90bd03bc. Step 1 numbered the 57 inbox bullets as items 1154 to 1210 in `docs/ENGINE-BACKLOG.md` (status block at its end) and cleared the inbox. Step 2 built six items; the rules are warnings only, the validator reports 0 errors.

## Built
- **a. `[rounding-tie]`** widened: a `wrong` stored one place past the asked places with a half-unit band and a fraction of 0.2 to 0.8 of a step (the 0.054688 for 7/128 case); a key within 7% of a step of a tie with a band that takes only one rounding (`p-touch-note`); a printed product or quotient of two figures on a tie (`p-twin-shares`).
- **b. `[working-band]`** widened: each printed span whose bare result follows it is re-evaluated from its own printed figures (products, quotients, powers, `e^x`, roots, logs); a result outside the band is reported (`p-boom-bust`). The sd-beside-its-square path of `p-bridge-closes` is a choice of path and is not read; I took "carry forward through the next part" as "carry through the next step".
- **c. `[key-in-question]`**: the key, rounded as asked, printed in its own question after `=`, `\approx`, "is" or "equals", or anywhere for a key of three or more significant digits. Exponents and subscripts are not read. A given that equals the key by coincidence is also reported.
- **d. Mobile text overflow**: `WIDE_PROBE` in `playthrough.mjs` fails an item at 600 px or less when text ends past the window or a box that clips holds wider text. It runs per part in problem sets and in the existing sideways-scroll checks.
- **e. `voice-scan.py`** lists a lesson id in a code span (`l4`, `l12-name`).
- **f.** `--problems` and `--set` stop with "Run the validator first" when the manifest lacks the set.

## Tests
`test-validate-pass9.mjs` (26 cases), `test-voice-scan.mjs`, `test-playthrough-text-overflow.mjs` (a wide span fails at 440 px, passes without `--mobile`, the clean set stays green), `test-playthrough-manifest.mjs`; all in `acceptance.yml`. Still green: `test-validate-pass8`, `-band-rules`, `-problems`, `-shown-arithmetic`, `-near-miss`.

## Counts and hits
`docs/reports/engine-pass-9-hits.md` (every hit with file, item, part). All content: `[rounding-tie]` 72 new (63 slip, 9 key; 0 product), `[working-band]` 4 new, `[key-in-question]` 29, voice scan 3 (`coding-int` homework-2 and review-2). The earlier cases are silent after their fixes except the `p-boom-bust` slips. Mobile run on ten problem sets: `measure-prob/problems-2` fails (item 3, parts 4 and 5: prose with a long maths span ends at 487 px); nine pass.

## Not built
The slip-in-band check (1175), carried values (1182), the long-maths validator warning, shared helpers, and all `fresh-check` items (not in scope). The slip-past-places rule is noisy (63); tighten it if the list is judged too long.
