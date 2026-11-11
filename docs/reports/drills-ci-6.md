# Drills pack `ci`, pack 6 (one-dimensional dynamic programming)

Brief: `docs/briefs/drills-ci-packs-5-8.md`, row "Pack 6", on top of `docs/briefs/drills-ci-packs.md` and `docs/briefs/drills-1.8.md`. 15 Python drills, `"pack": "ci"`, `"course": "coding-int"`, `"pattern": "dp"` (the vocabulary has no `dp-1d` slug, so the sub-pattern is the tag `dp-1d`), skills `ci-patterns` and `ci-timed`, tags `["pack-6", ("stdin",) "dp-1d", <slug>]`, rows appended to `app/content/drills/index.json`. Every drill carries `constraints` objects (ENGINE-BACKLOG 866) beside the prose.

| id | idea | difficulty | pace (s) | stdin | hidden tests | planted |
| --- | --- | --- | --- | --- | --- | --- |
| `ci-broken-steps` | climbing count, strides 1 to 3, cracked steps | 2 | 900 | no | 12 | 3 |
| `ci-best-session` | maximum subarray with its bounds and a tie rule | 2 | 960 | no | 12 | 3 |
| `ci-shift-picks` | non-adjacent best sum on a line, fewest days on a tie | 2 | 1020 | no | 12 | 3 |
| `ci-ring-stalls` | non-adjacent best sum on a ring, two empty between | 3 | 1500 | no | 13 | 3 |
| `ci-change-ways` | coin change ways, many fares from one table | 3 | 1380 | yes | 12 | 3 |
| `ci-product-stretch` | maximum product subarray of length two or more | 3 | 1440 | no | 13 | 3 |
| `ci-paving-ways` | 3 by `n` domino tiling round drains, column masks | 4 | 2100 | no | 15 | 5 |
| `ci-cooldown-trades` | trading with a `k`-day rest after each sale | 3 | 1500 | no | 12 | 3 |
| `ci-word-split` | word break, fewest words | 4 | 2100 | no | 13 | 2 + slow |
| `ci-longest-rising` | patience sorting: length and smallest end | 3 | 1500 | no | 14 | 5 |
| `ci-tape-decodes` | decoding counts, a smudge is 0 to 9 | 4 | 2160 | yes | 13 | 2 + slow |
| `ci-fewest-tokens` | coin change fewest coins, the payment with a tie rule | 4 | 2040 | no | 15 | 2 + slow |
| `ci-long-stairwell` | climbing count for $n$ up to $10^{18}$, matrix power | 4 | 2040 | no | 12 | 2 + slow |
| `ci-nested-crates` | patience sorting in two dimensions, heights non-decreasing | 5 | 2520 | no | 14 | 2 + slow |
| `ci-capped-trips` | at most `k` trades with a fee | 5 | 2700 | no | 13 | 2 + slow |

Mix: three at 2, five at 3, five at 4, two at 5; two stdin drills. Every idea of the row is covered: climbing and tiling counts (broken steps, long stairwell, paving ways), non-adjacent sums on a line and a ring (shift picks, ring stalls), coin change fewest and ways (fewest tokens, change ways), longest increasing by patience sorting (longest rising, nested crates), decoding counts (tape decodes), word break (word split), trading with a cooldown or a fee (cooldown trades, capped trips), maximum subarray and maximum product (best session, product stretch).

## Pyodide timings, difficulty 4 and 5

Measured by `drills-ci-6-check.py --pyodide <pkgs>`: Pyodide 0.27.7 under node (V8, Chromium's engine), all hidden tests in one run, as the drill page runs them against its 5 s limit. "Stopped" means the run was cut off at the 12 s cap, so the true time is longer.

| id | target (model) | obvious method | obvious method is |
| --- | --- | --- | --- |
| `ci-word-split` | 0.09 s | over 12 s (stopped) | plain recursion over every split |
| `ci-tape-decodes` | 0.22 s | over 12 s (stopped) | plain recursion over each reading of one or two characters |
| `ci-fewest-tokens` | 0.04 s | over 12 s (stopped) | plain recursion over the first token |
| `ci-long-stairwell` | 0.02 s | over 12 s (stopped) | the last `m` counts stepped forward one stair at a time |
| `ci-nested-crates` | 0.91 s | over 12 s (stopped) | $O(n^2)$ table after sorting |
| `ci-capped-trips` | 0.13 s | over 12 s (stopped) | plain recursion over (day, trips left, holding) |
| `ci-paving-ways` | 0.11 s | over 12 s (stopped) | cell-by-cell backtracking (new test: 3 by 30, 299,303,201 pavings) |

Every target is under 1 s, a factor of five inside the limit; every obvious method passes 5 s. The four recursions are defeated on time, not depth: each drill has a hidden test only 30 to 200 levels deep that branches exponentially (`'q' * 200` with codes of 1 to 5 letters and `'t' * 60 + 'u'`; 30 smudges and 40 ones; an amount of 60 with tokens 1, 2, 3; 40 days), before the long tests where the recursion would also hit the depth limit. Every model is iterative (the paving model recurses at most four levels to list its column moves), and the Pyodide run reports no recursion error. The obvious method is the last `planted` entry of each of these seven drills, and `how` names it and the step to the target.

## Checks

1. `docs/reports/drills-ci-6-check.py` (scratchpad venv Python): exit 0, "15 drills, 0 errors". Per drill it runs the model and an independent method on every example and test (brute force on small inputs: every subset, every stride sequence, every tiling by backtracking, every fill of the smudges, every multiset of tokens, every stretch, every pair; on large inputs a different algorithm: prefix minima, a state machine over (first stall, gap), numpy sums by residue, a cell-by-cell profile, a rest-counter state machine, a breadth-first search over positions, Fenwick trees, Kitamasa, a backward table). It reads every call's actual arguments and checks them against the `constraints` objects and the prose limits, so the generated tests the validator skips are checked too. It checks the starter fails, each wrong plant fails a test inside 2.5 s, each slow plant runs past 5 s in CPython, the mix, tags, paces and `how`.
2. `node tools/validate.mjs`: 0 errors; no `[no-constraints]` warning on these files. The only warnings on them are "pace over 30 minutes" on the seven drills paced 1,800 s or more, which the brief allows.
3. `node tools/playthrough.mjs --drill <15 ids> --local-cdn <pkgs>`: All passed; with `--mobile`: 15 of 15 ok. Shots at 440 px (tape decodes, paving ways) read cleanly.
4. Voice: `voice-scan.py 35` on the 15 files: 560 sentences, 0 over 35 words, 0 explanations over three sentences; no em-dashes and no `!` outside code.
5. This report and the inbox bullets.
6. `node tools/planted-check.mjs --drill <ids> --require --local-cdn <pkgs>`, in three runs of five: 15 drills, 45 planted solutions, 0 failures.

## What the independent methods caught while drafting

- `ci-nested-crates`: the first model used the usual sort (width up, height down) with `bisect_right`. It counted two crates of the same size as a row of two; the brute force caught it on `[[2, 2], [2, 2], [3, 2]]`. The model now places each width as one group against the tails from narrower crates, and the usual trick is planted as planted[0] (its slip names the same-size case). Example 2 shows two equal crates.
- `ci-fewest-tokens` planted[1] (record the smallest token reaching each amount) passed at first. A random search found `[6, 3, 7, 4]` for 15 (answer `[7, 4, 4]`, the plant `[6, 6, 3]`) and `[2, 7, 1, 5]` for 11; both are hidden tests now.
- `ci-best-session` example note said four runs make £2; there are five, now stated.

## Freshness

`node tools/fresh-check.mjs --drill <id>`: 0 hits for all 15. Taught setups avoided by design: `stairs` and `min_coins` (graphs-dp l13), so the climbing drills add cracked steps or reach $10^{18}$ and the coin drill returns the payment with a tie rule; `word_break` and `trade_with_fee` (graphs-dp homework-3), so the word drill asks for the fewest words and the fee drill caps the trips; `max_subarray` (ds homework-2), so the session drill returns the bounds with a tie rule; `max_profit_k` (contests homework-4) has no fee; `oa-decodings` (plain decoding count), so the tape drill adds smudges that may be 0; `oa-rising-run` (plain length), so the rising drill also returns the smallest end; `dsa-footpath-slabs` (2 by `n`, closed recurrence), so the paving drill is 3 by `n` with drains; `dsa-shift-pay` (no three days running), so the shift drill rests a day and breaks ties on days; `dsa-stamp-gaps` (unpayable totals), so the ways drill answers many fares. Every example and test input was written for these drills; no site sample is used. Each `how` of a drill grown from a known problem ends with a sentence saying what changed and why it changes the code.

Worked numbers in the briefs (5, `[6, 2, 4]`, `[8, 3]`, 11, `'2\n2\n1'`, 8, 2, 5, 2, `[3, 5]`, `'19\n2'`, `[6, 5, 4]`, 5, 3, 12) are the `expect` of each drill's first example, computed by the model and recomputed by the independent method in the check script.

`app/content/manifest.json` was rewritten by the validator and is not committed.

## Fix pass (second read)

Pyodide timings re-measured after the fix pass (the table above is updated): every target under 1 s (`ci-nested-crates` 0.91 s is the tightest, with the new 100,000-crate test), every obvious method cut off at 12 s. `ci-longest-rising` moved to difficulty 3 and left the table. The new slow plant of `ci-word-split` (every code tried at every position) runs 12.5 s in Pyodide on the 5,000-code test. `ci-capped-trips` is now difficulty 4 (pace 2,100), `ci-long-stairwell` 5 (2,520), `ci-paving-ways` 4 (2,100), `ci-longest-rising` 3 (1,500); mix still 3 / 5 / 5 / 2.
