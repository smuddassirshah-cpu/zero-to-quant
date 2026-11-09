# options level 3: performance task

`homework-3.json`, `h-derive-box`, item 9 of 9 (appended; nothing converted). Kind `derivation`.

Objective: l9 "Derive put-call parity from two portfolios with equal payoffs." The box and a loan are two portfolios with equal payoffs.

Task: payoff of a $K_1/K_2$ box, its no-arbitrage price $(K_2 - K_1)/(1+r)^T$ with both trades, a parity check, a dealer's cheap box (£18.70 against £19.23: £0.53 today, £0.00 at expiry), optional American part.

Rubric: 2 (payoff, three cases), 3 (both trades), 2 (parity), 2 (dealer), 1 (optional part). Rows 1 to 4 required. `rubric-passes.mjs --item ...#h-derive-box`: only row 5 can be left out.

Overlapping screens: l9 screens 0, 4 and 7 (equal payoffs, arbitrage cash flows, parity order), l10 screens 1 and 8, `h-derive-spread`, `h-long-stale-quote`. New: the box's fixed payoff, an equality proved both ways, parity at two strikes with $S_0$ cancelling, a trade with no share, early assignment.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/options python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `<venv>/bin/python -I docs/reports/options-3-perf-numbers.py`: exit 0.
4. `node tools/playthrough.mjs --set options/homework-3 --local-cdn <pkgs>`, with and without `--mobile`: All passed.

Freshness: `fresh-check --file` 0 hits; grep `box`, `16.20`, `10.90`, `19.23`, `assign`.
