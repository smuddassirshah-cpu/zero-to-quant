# Report: mental-pressure level 2 (Fractions and estimates)

Status: complete. Course `mental-pressure`, topic 3.3; brief `docs/briefs/mental-pressure.md` `## Level 2`, with the orchestrator's additions: a follow-up screen in every lesson, a stated pace on every drill, `tags` on every drill, review and homework item, `shuffle: true` on choices, `longform` in homework only, and timed sets where they fit. No firm is named. Generator scripts and screenshots are in the scratchpad folder `mp2`.

## Files

| File | Screens or items | Canvases and widgets | Code |
|---|---|---|---|
| `l5-which-fraction.json` | 12 screens, 4 quiz | table; a `pair` of two `area` squares re-cut by two `stops` controls (explore); number-line (order four); place in order mode; order with a distractor | `bigger(a, b, c, d)`, `order_fractions(pairs)`, 10 tests |
| `l6-percent-of-percent.json` | 12 screens, 4 quiz | table; `bars` driven by two controls and `derive` (explore); tables with `unit: "%"` cells | `combine(changes)`, `reverse_change(p)`, 11 tests |
| `l7-estimating-products.json` | 12 screens, 4 quiz | area (hook); number-line with a 5% band and a derived estimate from two `stops` controls (explore); tables with `tol: { "rel": 0.05 }` cells | `within_pct`, `round_sig`, 12 tests |
| `l8-square-roots.json` | 12 screens, 4 quiz | table of squares; `plane` with $\sqrt x$, its tangent at 49 and two derived points on a slider (explore); tables | `newton_sqrt`, `nearest_square_root`, 14 tests |
| `review-2.json` | 10 items, difficulty 2 to 4, `timed: { "seconds": 300, "lockAtZero": false }` | choice, numeric | |
| `homework-2.json` | 8 items, difficulty 3 to 5 (two at 5) | 20-row drill table, 2 code items, an `order` derivation, 3 numeric, a 10-point `longform` | `estimate_checker` + `quick_product` (9 tests, difficulty 5); `combine` + `rate_change` (10 tests) |

Every lesson follows hook, explore, name, two ladders, a follow-up ladder titled "The follow-up", trap, generalise, derive, code, drill, transfer. Skills: `mp-fractions` on l5 and l6, `mp-estimate` on l7 and l8. Edge cases: equal fractions in disguise (l5 quiz), −100% (l6 quiz), "ask whether the exact figure is wanted" (l7 follow-up and quiz), a perfect square (l8 drill and quiz).

Follow-ups: l5 "by how much is 7/12 bigger?" ($\tfrac{1}{36}$ from the cross products); l6 "what fall undoes a 20% rise?" (16.67%); l7 "now the exact figure" for $0.49 \times 812$ (397.88); l8 "is 8.375 high or low, and by how much?" ($8.375^2$ overshoots 70 by $0.375^2$).

Pace: l5 drill 12 at 4 s (48 s); l6 12 at 6 s (72 s); l7 12 at 5 s (60 s); l8 10 at 8 s (80 s); homework 20 at 6 s (120 s); review-2 a 300 s guide clock. Every lesson drill says the screen has no clock.

Tags (family names, unchecked by the validator): `drill-fraction-compare`, `drill-percent-chain`, `drill-estimate-product`, `drill-sqrt` on the lesson drills; review `fraction-compare`, `percent-chain`, `estimate-product`, `sqrt-newton`, `fraction-gap`, `percent-points`, `estimate-exact`, `percent-reverse`, `fraction-odds`; homework `drill-mixed`, `code-estimate-checker`, `code-percent`, `sqrt-newton`, `fraction-gap`, `percent-reverse`, `sqrt-vol`, `spoken-estimate`.

Generated items and timed sets: `timed` is used on review-2. Generated `arith` items were not used: they make whole-number four-operation items only and belong in mock and stage exams, while this level's drills are fractions, percentages, estimates and roots (backlog bullet 1).

## Validator

`node tools/validate.mjs`: 0 errors overall. Four warnings on my files, all "a point hint usually highlights the canvas" where the canvas has no fitting id (the l5 pair of areas, the empty l5 number-line before its explanation, the two code screens).

## Playthrough

With `--local-cdn <pkgs>` and `--mobile`: l5 16 checks, quiz 4/4; l6 16 checks, quiz 4/4; l7 16 checks, quiz 4/4; l8 16 checks, quiz 4/4; review-2 10 of 10 recorded; homework-2 8 of 8 right, 38 of 38 marks. All passed. Screenshots (540 and 390 px, with Why? sheets) were read for every explore, drill, code, transfer and set screen. Fixes made from them: the l8 tangent lengthened to reach $x = 70$ and the $\sqrt x$ label moved below the curve; the l7 band label removed so it no longer stacks with the "exact" label.

Code: a CPython harness (`mp2/codecheck.py`) runs every solution and starter against every hidden test and example. All solutions pass all tests and examples. Every untouched starter fails every hidden test (the l6 and l8 starters were changed so that none passes).

## Numbers, each computed twice

Every number was written by hand in the generator scripts and asserted against `fractions.Fraction`, `decimal.Decimal` or `math.sqrt` in the same script (`mp2/l5.py` to `l8.py`, `sets.py`); a failing assert stops the file being written.

- l5: $7 \times 9 = 63$, $5 \times 12 = 60$; $13 \times 21 = 273$, $16 \times 17 = 272$ (0.7647 against 0.7619); $\tfrac37 < \tfrac12 < \tfrac59$; gaps $\tfrac29 = 0.2222 < \tfrac{3}{13} = 0.2308$, check $91 > 90$; $\tfrac57 = 0.714 > 0.7$; $\tfrac{11}{20} = 0.55 > \tfrac{6}{13} = 0.4615$; order $\tfrac35 < \tfrac58 < \tfrac{7}{11} < \tfrac23$ (55 against 56 for the close pair); $\tfrac{7}{12} - \tfrac59 = \tfrac{3}{108} = \tfrac{1}{36}$; trap $9 \times 16 = 144 > 13 \times 11 = 143$; $11 \times 11 = 121 > 8 \times 15 = 120$ (gap $\tfrac{1}{165}$); odds on £36: £21 against £20, implied 63.2% against 64.3%; quiz $6 \times 21 = 9 \times 14 = 126$, $64 < 65$, $\tfrac47 - \tfrac59 = \tfrac{1}{63}$. Drill answers R L L R R L L R R L R L, checked by cross products and by decimals; ten of twelve have products 1 apart.
- l6: $1.1 \times 0.9 = 0.99$; $1.2 \times 0.8 = 0.96$; $1.2 \times 1.3 = 1.56$; $0.8 \times 0.75 = 0.6$; $0.9^2 = 0.81$; $0.15 \times 0.4 = 0.06$; $1.5^2 = 2.25$; points 1 and 25%, −0.5 and −25%, 1.5 and 30%; undo +20% by $\tfrac16 = 16.67\%$; 50% loss needs 100%; $1.5 \times 0.5 = 0.75$; $1.05 \times 0.9 \times 1.2 = 1.134$; £80,000 to £100,000 to £80,000 ($1.25 \times 0.8 = 1$), the client's +5% overstates by £4,000; quiz 5% to 4% is −20%, $0.3 \times 0.4 = 0.12$. Drill: 21, −4, 0, 6, −40, 20, 25, −25, 33.33, 8.9, 1, 150 (%).
- l7: $48 \times 52 = 2496$, 2,500 is 0.16% off, $52^2 = 2704$ (+8.3%), $48^2 = 2304$ (−7.7%); band 2,371.2 to 2,620.8; $3.14 \times 2.7 = 8.478$ ($3 \times 3$ is 6.2% high); $0.49 \times 812 = 406 - 8.12 = 397.88$; $19 \times 21 = 399$; $6.9 \times 4.1 = 28.29$; $4.2 \times 10^6 \times 3100 = 1.302 \times 10^{10}$; $46 \times 47 = 2162$, 2,500 is +15.6%, 2,025 is −6.3%, $45 \times 48 = 2160$; $2.5 \times 8 = 20$ against $2.3 \times 7.8 = 17.94$, +11.5% (rule's sum 11.3%); cross term for 48 × 52 is −0.16%; notional $4800 \times 51.90 = 249{,}120$; quiz $6.2 \times 49 = 303.8$, $31 \times 49 = 1519$, $0.98^2 = 0.9604$ (+4.1%), $3.6 \times 10^5 \times 2.5 \times 10^3 = 9 \times 10^8$. Drill exacts: 1,599; 4,964; 17.69; 193.8; 46,906; 3.61; 624; 1,312; 14.5; 693,000; 8,091; 97.96.
- l8: $\sqrt{50}$: $7 + \tfrac1{14} = 7.0714$ (true 7.0711); $\sqrt{130}$: $11 + \tfrac9{22} = 11.409$ (true 11.402); $\sqrt{200} = 14.142$, $\sqrt{0.5} = 0.7071$, $\sqrt{27}$: 5.2 (5.196), $\sqrt{85}$: 9.222 (9.2195); $\sqrt{70}$: 8.375 (8.3666), $\sqrt{40}$: 6.333 (6.3246), $\sqrt{150}$: 12.25 (12.2474); $8.375^2 = 70.140625$, overshoot $0.375^2$, second step 8.36660; $\sqrt{36 + 64} = 10$; $\sqrt{105}$: 10.25 (10.247); $\sqrt{252}$: $16 - \tfrac4{32} = 15.875$ (true 15.8745), $20\% \div 15.8745 = 1.2599\%$; quiz $\sqrt{80} = 8.944$, $\sqrt{0.09} = 0.3$, $\sqrt{25} = 5$, $\sqrt{1000} = 31.623$ (steps 31.629 and 31.625). Drill (one place): 4.5, 7.7, 9.5, 11.0, 12, 17.3, 0.89, 1.41, 13.2, 22.4, each step within 0.05 of `math.sqrt`. Newton test values: 99/14, 251/22, 8.375, 8.36660447761194, 15.875, $\sqrt2$ after 5 steps 1.414213562373095.
- review-2: $11 \times 13 = 143 < 9 \times 16 = 144$; $1.3 \times 0.7 = 0.91$; $6.8 \times 410 = 2788$ (band 2,649 to 2,927; $7 \times 420 = 2940$ outside); $\sqrt{120}$: $11 - \tfrac1{22} = 10.9545$; $\tfrac56 - \tfrac45 = \tfrac1{30}$; 2.5% to 3% is +20%; $0.51 \times 640 = 326.4$; $\sqrt{0.3} = \sqrt{30} \div 10 = 0.5477$; undo −25% by +33.33%; odds on £63: £36 against £35.
- homework-2: drill of 20 (L/R by cross products; −16%, 9%, 33.33%, −25%, +72.8%; 2,499, 218.4, 48.98, 79,950, 4,410; 6.32, 10.49, 0.447, 15.81, 14); $\tfrac{13}{17} - \tfrac{16}{21} = \tfrac1{357} = 0.0028$; 40% loss needs 66.67%; $\sqrt{12} \approx 3.5 - \tfrac{0.25}{7} = 3.4643$ (true 3.4641), $20\% \div 3.4641 = 5.77\%$; Newton order $\tfrac{99}{14} = 7.0714$, $(\tfrac{99}{14})^2 = 50.0051$; longform: 4.2% of £7.85m = £329,700 (4% £314,000 + 0.2% £15,700), after 3% fall £319,809 (fall £9,891; quick £9,900 gives £319,800), £8m shortcut £336,000 (+1.91%), 4% shortcut −4.76%, $0.042 \times 0.97 = 0.04074$.

## Seeds and conventions

- Homework `quick_product` harness: 20 pairs from `random.Random(7)`, each `randint(1000, 99999)`, passed as `Full(int)` values that refuse `Full * Full`. Three significant figures each lands within 0.42% on all 20; two significant figures misses one pair (5.07%), so the test tells the two strategies apart.
- Percent answers use `unit: "%"` with the answer as a fraction (−0.04 for −4%) and `tol: { "abs": 0.0005 }` unless stated. Estimates use `tol: { "rel": 0.05 }` with the exact value in `accept`. Roots use `tol: { "abs": 0.05 }` (one decimal place). Fraction comparisons are text cells "L" or "R" with "left" or "right" accepted.
- Money in £ throughout; British spelling; curly apostrophes in prose.

## For exam authors

A timed paper of mixed fraction comparisons, chained percentages, estimates and roots (for example 20 items in 2 minutes, as homework's drill) suits the topic 3.3 or Stage 3 exam. No exam file was written.

## course.json

No change proposed.

## Backlog

Five bullets under "Raised later (mental-pressure level 2)" in `docs/BACKLOG-INBOX.md`: generators limited to whole-number arithmetic in exams; no clock on a single drill table; number-line labels and coincident points with a stacked interval; no way to forbid an operation in learner code; no follow-up parts or per-item pace (E11, E9).
