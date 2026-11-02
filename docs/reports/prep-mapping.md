# Prep paths: the full mapping in `app/content/prep.json`

Brief: `docs/briefs/prep-tags.md`, sections "Mapping" and "Data". Schema: `docs/AUTHORING.md` section 10. Departures in the engine pass (`docs/reports/engine-prep-tags.md`) need nothing different here. I edited only `app/content/prep.json`. The validator regenerated `app/content/manifest.json` as usual. The two engine sample paths are gone. The file is built by a scratch generator (`scratchpad/prep-map/build.py`). It checks why lengths, copy rules, overlaps within a path, ref resolution and study order before it writes.

## Paths (23), in file order

Top-level `asOf`: 2026-11-02. Steps are in study order. Within a path, courses follow the curriculum topic order (0.x, then 1.1 to 3.5), and a course's levels go in order. `recruiting` steps come where they are used: level 1 early in `general`, l9 and l10 at the end of OA paths, l8 and l12 at the end of interview paths, level 3 at the end of superday paths.

| Path | Steps | Lessons covered | Must | Mocks |
| --- | --- | --- | --- | --- |
| general | 13 | 79 | 12 | mock-oa-arith, mock-video |
| oa-trader | 17 | 77 | 12 | mock-oa-arith, mock-oa-trader, mock-oa-sig |
| oa-research | 23 | 192 | 13 | mock-oa-code, mock-oa-quant-data, mock-video |
| oa-strats | 17 | 141 | 10 | mock-oa-strats, mock-oa-code, mock-video |
| oa-developer | 14 | 116 | 11 | mock-oa-code, mock-oa-code-hard |
| interview-trader | 21 | 155 | 13 | none |
| interview-research | 20 | 245 | 15 | none |
| interview-strats | 19 | 136 | 10 | none |
| interview-developer | 15 | 114 | 10 | none |
| superday-trader | 15 | 106 | 10 | mock-superday-trader |
| superday-research | 15 | 110 | 7 | mock-superday-research |
| superday-strats | 12 | 61 | 7 | mock-superday-strats |
| superday-developer | 13 | 61 | 7 | mock-superday-developer |
| firm-optiver (trader) | 16 | 58 | 8 | mock-oa-arith, mock-oa-trader, mock-superday-trader |
| firm-jane-street (trader) | 12 | 59 | 7 | mock-superday-trader |
| firm-sig (trader) | 9 | 39 | 6 | mock-oa-sig, mock-superday-trader |
| firm-imc (trader) | 9 | 34 | 6 | mock-oa-trader, mock-video, mock-superday-trader |
| firm-citadel-securities (trader) | 8 | 39 | 6 | mock-oa-trader, mock-superday-trader |
| firm-two-sigma (research) | 11 | 86 | 6 | mock-oa-quant-data, mock-superday-research |
| firm-citadel (research) | 8 | 54 | 4 | mock-oa-code, mock-superday-research |
| firm-jp-morgan (research) | 14 | 71 | 6 | mock-oa-code, mock-video, mock-superday-research, mock-superday-strats |
| firm-goldman-sachs (strats) | 16 | 88 | 6 | mock-oa-strats, mock-oa-code, mock-video, mock-superday-strats |
| firm-morgan-stanley (strats) | 13 | 55 | 6 | mock-oa-quant-data, mock-video, mock-superday-strats |

Total 346 steps. No mock file exists yet apart from `mock-sample`, which no real path uses, so every mock shows "Not yet written".

## Sources per firm path

Every firm path has `asOf: "2026-10"`, `source: "recruiting/l4-firm-by-firm"` and `reported: true`. The role is l4's row. Each step's why only repeats what l4's table and screens, or the firm's row in `docs/briefs/interview-gaps.md` section 1, report. Mocks come from the "Models" column of the table in `docs/briefs/interview-plan.md` (d).

- **Optiver**: l4 rows and screen 3 (80 in 8, sequences, attention games, recruiter call, live games, final round, the official 8-month retake rule); gaps row (2026 Likelihood, Intervals and Orderbooks variants, Fermi estimates, brainteasers). The description says the attention games are not trained here (the plan leaves Zap-N out).
- **Jane Street**: l4 row (no online test, phone rounds, final day); gaps row (mental maths with no paper, dice games, card drawing, the frog recursion, the coin-and-box game, markets on cards or a die with parallel bets, harder game theory, confidence levels, reasoning aloud, light fit questions).
- **SIG**: l4 row; gaps row (official stage list, the 17 in 60 test with calculator and its multi-stage Bayes and ruin items, two heads in a row, dice rerolls, pot odds, dominoes market, poker round, the decision-you-changed question).
- **IMC**: l4 row (games or numerical test by office, recorded video, market-making game, superday); gaps row (Fermi, flips-until-a-head market, the Alice-and-Bob coin game, bankroll and card-guessing bets, why IMC).
- **Citadel Securities**: l4 row (official OA and up to five 45-minute interviews); gaps row (about 15 in 30, probability, combinatorics, mental maths, estimation, brainteasers then harder probability).
- **Two Sigma**: l4 row and screen 4; gaps QR row (data and regression tasks, statistics phone screen, open case, the interpolator and per-town regression, model choice and validation, optimisation).
- **Citadel**: l4 row and screen 7 (coding test reported both ways, "prepare for one anyway"); gaps row (the drunkard's walk, the three-correlation question, regression, PCA, regularisation, brainteasers, LeetCode medium).
- **JP Morgan**: l4 row; gaps row (official coding challenge and HireVue, string and array problems, first-round regression and puzzles, superday DP, brainteasers, regression assumptions, a case study, the $W_t^3$ martingale question, Markov chains, Itô, C++ inheritance, Black-Scholes in practice).
- **Goldman Sachs**: l4 row; gaps row (30-minute Software Fundamentals, 22-minute maths test on calculus, linear algebra and probability, older binomial theorem, combinatorics and differential equations, a recorded video, probability tree, Buffon's needle, regression rapid-fire, fair coin from biased, dice, bits).
- **Morgan Stanley**: l4 row; gaps row (official OA, video and superday; Hong Kong IED test with regularisation, z-scores, Poisson and conditional probability, two Python tasks; older written test with bonds, options and stochastic calculus; Asian against vanilla; Greeks; C++ and Python). The description says the detailed reports come from Hong Kong.

## Judgement calls

- **Every stage path starts from foundations.** OA and interview paths open with Stage 0 and 1 courses (`number-sense`, `ratio`, `series`, `mental`, `first-python`, `py-found`, the 1.3 to 1.8 courses), then go up to their stage's topics. Superday paths open with a short refresher, mostly marked Should, then the final-round material as Must.
- **Firm paths are single-role.** Each follows its l4 row's role. `interview-gaps.md` also reports software roles at Jane Street, Two Sigma and Optiver. I left these to the developer stage paths rather than mix roles on a firm path. A later pass can add `track`-tagged developer steps.
- **Lesson refs where one lesson carries a reported item**, each checked against its name and objective in `course.json`. Examples: `mental-pressure/l9`, `l10`, `l13`, `l14`, `l16` for Optiver's battery; `mm-games/l14` and `l15` for the Intervals and Orderbooks variants; `graphs-dp/l13-climbing-stairs` for the frog; `research-int/l2-correlation-limits` for Citadel's correlation question; `ito/l13-martingale-or-not`, `cpp/l21-virtual-dispatch` and `regression/l11-assumptions-fail` for JP Morgan; `conditional/l5-trees`, `puzzles/l17-buffon`, `l25-fair-from-biased`, `coding-int/l5-bit-tricks` for Goldman Sachs; `trees/l17-which-is-cheaper`, `limits-thm/l3-rare-events` and `l7-bell-curve` for Morgan Stanley.
- **JP Morgan's "do practitioners use Black-Scholes"** maps to `trees/l16-the-smile` (reading the smile), not to `l10-black-scholes`. The smile is the honest answer to the question.
- **Departures from the seeds.** `superday-trader` uses `mental-pressure/l15-probability-at-speed` instead of mental-pressure L3 to L4. Those levels are test formats (80 in 8, batteries) and belong to `oa-trader`. `oa-trader` adds `random-vars` L2 and `mm-games` l14 and l15. `oa-research` adds `first-python`, `conditional` L1, `stat-learning` L2 and `research-int` L4. `oa-strats` adds `series` L3 and `odes` L1 (a quant-strand course). Every addition is for a reported test item. `interview-trader` keeps `puzzles` L1 to L3 and leaves L4 to L5 to the superday path. `interview-research` and `interview-strats` add the recruiting reasoning-aloud lesson.
- **Mocks.** `mock-video` (models "HireVue rounds") is on the general path, the research and strats OA paths, and the firms with a recorded video stage (IMC, JP Morgan, Goldman Sachs, Morgan Stanley). IMC's video is not reported as HireVue; it is the same format. Citadel gets `mock-oa-code` because l4 advises preparing for a coding test anyway, although that mock's Models column does not name Citadel. Interview paths have no mocks; the plan's mocks are OA and superday papers.
- **Optiver's order** puts the arithmetic battery steps before the `mm-games` steps, against the 3.3 course order. The test comes first in the process, and neither set depends on the other.
- **Wording.** Firm whys say "reported" or "official" as their source says. Stage whys name no firm: firm facts stay in firm paths, l4 and mock descriptions.

## Verification

- `node tools/validate.mjs`: 0 errors, 386 warnings. That is the same count as before the mapping (all "not yet written" notes). prep.json raises no warnings: no two steps of one path overlap, and no firm date is stale.
- `node tools/playthrough.mjs --routes-only --local-cdn <pkgs>`: all passed, with and without `--mobile`.
- A scratch Playwright script (`scratchpad/prep-map/shots.mjs`) opened all 23 `#prepare/<id>` routes at 1280 px and 390 px. On every one, the steps and mocks drawn matched the file, the page was no wider than the window, and there were no console errors. I checked the 390 px screenshots of `general`, `oa-trader` and `firm-optiver` by eye: titles, Must and Should badges, Not yet written states, why lines and mocks all fit. The only overlap was the fixed bottom navigation bar, which a full-page capture draws mid-page. `prepDetail` for a busy lesson reads: "General, OA, interview, superday. Jane Street, SIG, Citadel Securities, JP Morgan, Goldman Sachs (reported, October 2026)."
