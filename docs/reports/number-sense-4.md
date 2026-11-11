# number-sense level 4: Factors, measures and averages

Author report for the gap level from `docs/briefs/gap-number-sense.md` (section `## Level 4`). Written in a worktree; commits `number-sense L4: l15` to `l19`, review and homework, script, report.

## Files written

| File | Screens / items | Quiz | Canvases | Notes |
|---|---|---|---|---|
| `l15-building-blocks.json` | 10 screens | 4 | grid (row lengths, hundred square), table, pair of graph factor trees, grid of 36's factors | explore 36 tiles, 37 tiles, sieve (multiples of 7 left: 49, 77, 91), the root test on 97, two trees of 360, trap (1, 2, 51, 53, 57, 59, 91), factor count generalise, order derive (root test, with one distractor line), 252 trading days transfer |
| `l16-shared-factors.json` | 11 screens | 4 | number-line (two rows of prints), venn (84 and 120; 12 and 18; 150 and 240), number-line for Euclid | LCM 36 and HCF 6 named after use, LCM of 4 and 6, HCF 12, LCM 840, 84/120, 5/12 + 7/18, Euclid table 252 and 198, trap 8 and 12, order derive of HCF × LCM, clip-size transfer (30 shares) |
| `l17-around-and-inside.json` | 9 screens | 4 | plane (24 m fence, corner on x + y = 12), area, plane figures | 20 and 36 m² at perimeter 24, 8 by 3, triangle 20, parallelogram 28, trapezium 32, L-shape 48, trap L perimeter 32, generalise k and k² with 1 m² = 10,000 cm², transfer 1.21 as an area model |
| `l18-circles-and-units.json` | 10 screens | 4 | plane circles, pair of area circle and plane sector wedges with a frames slider (4, 8, 16 wedges), tables, area | ratio table 3.14, wheel 157.1 cm, wedges give πr × r, radius 5 with π ≈ 3 first, semicircle 20.57, 72 km/h = 20 m/s, 25,000 cm² and 24 m³, trap 78.54 not 314.16, exact 25π, £5,000 a day and £667 an hour |
| `l19-one-number-for-many.json` | 12 screens | 4 | bars: histogram with a draggable pivot, day bars, sorted bars, frequency bars, truncated bars | pivot balances at 60 (live caption shows the two distance sums), sort, median 40, range 380, 3,100 day (mean 460, median 40), 6.5, frequency table (37, 1.85, 2, 2), missing day 180, traps (£65,000; cut-off axis 1.1), order derive of the balance point, transfer (median £40 against the quoted mean £460) |
| `review-4.json` | 10 items, difficulty 2 to 4, `pass` 0.8 | | venn, plane, table | every lesson twice |
| `homework-4.json` | 8 items, difficulty 3 to 5 (two at 5) | | plane, table | product of primes with HCF 18 and LCM 630 (3 parts), lawn with a semicircle (area 74.14, perimeter 35.42), 25 m/s = 90 km/h, frequency mean 2.6 and median 3, a mean after one bonus leaves (£38,000), Euclid on 1,071 and 462 as an `order` item (HCF 21, one distractor), longform leaflet (mean £35,000, median £20,000, cut axis; 10-point rubric, full model), factors of 2,520 (48) |

Skills as briefed: l15 `ns-powers`; l16 `ns-fractions`, `ns-powers`; l17 `ns-powers`, `ns-estimate`; l18 `ns-decimals`, `ns-powers`; l19 `ns-decimals`, `ns-negatives`. `course.json` had no `ns-measures`, so it was not used. No algebra is asked for: formulas are in words first with letters only as a label (`A = lw`, `C = 2πr`), nothing is rearranged, and money stays in pounds with no per cent sign. l19 has two `trap` screens (averaging averages; the cut-off axis), both named in the brief. Edge cases: square numbers (odd factor counts, l15 quiz), 8 and 15, 6 and 18 (l16 quiz), 1 m² = 10,000 cm² (l17), exact 25π against 78.54 (l18), two modes and a mean that is not a possible value (l19).

## Self-check (SESSION PROTOCOL 4)

1. Validator: `node tools/validate.mjs` 0 errors; no warning on any level 4 file (whole-repo total 4,364 warnings, none in these seven files).
2. Voice scan: `VOICE_BASE=app/content/courses/number-sense/ python3 docs/reviews/voice-scan.py 35` reports 0 explanations over three sentences and 0 sentences over 35 words (8,655 scanned). No `!`, no em or en dashes.
3. Numbers: `docs/reports/number-sense-L4-numbers.py` exits 0, 452 of 452 checks. Each value is computed by two routes (brute-force factor lists, `math.gcd`/`math.lcm`, Euclid, shoelace areas, `statistics`, exact `Fraction`s against the taught route) and tied to its JSON path; `check_wrongs` passes and its 88 "check by hand" byKey lines were read: each states working numbers, not a different result.
4. Playthrough: every lesson, the review and the homework pass with no flag, with `--mobile` and with `--tablet` (`--local-cdn` the scratchpad `pkgs`). Screenshots at 440 px and the Why? sheets were read for each lesson; fixes made: factor-tree leaves spread, area `shade` patches, L-shape label, value-axis bars replaced by a histogram, homework display equation broken with `aligned`.

## Numbers stated, with source

All in the script, by lesson. The planner's list is covered: 9 factors of 36; 360 = 2³ × 3² × 5 and 24 factors; 10, 15, 25 primes below 30, 50, 100; 91, 51, 57, 97; 252 = 2² × 3² × 7, 18 factors, 12 × 21; HCF 6, LCM 36; HCF 12, LCM 840, 10,080; 7/10, 29/36; remainders 54, 36, 18 and LCM 2,772; 8 and 15, 6 and 18; 12 months, 30 shares; 20 and 36; 22, 24, 20, 28, 32, 48, perimeter 32; 10,000; 1.21 (£6,050); 31.42, 78.54, 18.85, 28.27, 20.57, 314.16; 20 m/s, 25,000, 24, £5,000; mean 60, median 40, mode 40, range 380, 460; 6.5; 37, 1.85, 2, 2; 180; £65,000; 300 and 300. Computed and reported: £666.67, about £667 a trading hour. Added by this author and checked: 157.1 cm (wheel), 49/77/91, 1,200 (LCM 150, 240), review (18 factors of 180, LCM 180, 5/7, 34, 42, 153.94, 15 m/s, 1.1, 38) and homework (18, 630, 11,340, 74.14, 35.42, 90, 2.6, 3, 38,000, 21, 23,562, 420, 35, 20, 48).

Conventions: rounding half up; π to the calculator's value, answers to 2 decimal places where asked, with tolerances that also accept π ≈ 3.14 where a learner would use it (wheel ±0.15, radius-5 table ±0.05 and ±0.1).

## course.json

No change proposed. If the topic exam gains measures items, a sixth skill `ns-measures` for l17 to l19 (as the brief anticipates) would fit.

## For later passes

Fluency families worth adding (`docs/briefs/fluency.md`): product of primes; HCF and LCM of two numbers; area of a triangle or trapezium; circumference and area from a radius or diameter; mean and median of five to seven values. Problem set `problems-4.json` is not written.

## Backlog

Four bullets under `Raised later (number-sense L4):` in `docs/BACKLOG-INBOX.md`.
