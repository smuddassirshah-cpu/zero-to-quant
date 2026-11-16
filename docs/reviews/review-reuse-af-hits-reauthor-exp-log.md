# Re-author, exp-log (session AF reuse hits)

Brief `docs/briefs/reauthor-af.md`; ruling `docs/reviews/review-reuse-af-hits.md` lines 201 and 205.

- `exp-log/problems-1.json` `p-rare-coin` (id kept; it names no old number). Old task: £640 two years ago to £1,000 today, 2-year factor 1.5625, $g = \sqrt{1.5625} = 1.25$, 25% a year, value 18 months ahead $1000 \times 1.25^{1.5} \approx 1397.54$. New task: £1,600 three years ago to £3,936.60 today; part 1 factor 2.460375 (wrong `inverted` 0.406442, `rise` 1.460375); part 2 $g = \sqrt[3]{2.460375} = 1.35$ (wrong `thirded-factor` 0.820125, `thirded-rise` 1.486792, `square-root` 1.568558); part 3 rate 35% (wrong `factor` 1.35, `thirded-rise` 0.486792, `decimal` 0.0035); part 4 value 18 months ago, halfway in time, $1600 \times 1.35^{1.5} \approx 2509.69$, £2,510 (tol 1; wrong `mid-value` 2768.30, `simple` 2440, `two-years-ago` 2160, `one-year-ago` 2916, `forward` 6174.79, `carried` 2900.65). Chain changed as well as numbers: a cube root over three years, then a fractional power to a past date, against `p-drawdown-recovery`'s falls, gain back and $1.11^n = 1.25^2$ solve. No 1.5625, 0.64, 1.25, 0.5625 or 56.25 in the item.
- `exp-log/problems-2.json` `p-drawdown-recovery`: not edited, as ruled.

Closest course material and verdicts are in `docs/reports/problems-exp-log.md`, "Re-author, session AF" (all clean: `l3` backtest and cube-root screens, `review-1` `r-years-ago`, `homework-1` `h-monthly-rate`, `topic-0.3` `e-fraction-powers`).

## Gates (problems-1)

- Validator: 0 errors; no warning on `exp-log/problems-1`.
- Voice scan 35 on `app/content/courses/exp-log`: 0 and 0.
- `fresh-check --file content/courses/exp-log/problems-1.json`: 0 hits (one waived line, `p-laptop-value`, as before).
- `same-course-reuse --all | grep exp-log`: no hit on `p-rare-coin`. One error remains: `problems-2` `p-drawdown-recovery` part 3 against `problems-1` `p-laptop-value` (rate, 56.25% and 0.5625 with 1.25). It is the reverse direction of the laptop hit already ruled **stands** (line 200, a chance match) and waived only from `problems-1`; the tool showed one pair per item, so the rare-coin hit hid it. Needs the mirror waiver from the main session (this brief adds none).
- `grade-all --file`: 16 widgets, 0 failures. `docs/reports/problems-exp-log-grade.mjs`: 709 checks, 0 failures (rare-coin rows retargeted).
- `docs/reports/problems-exp-log-numbers.py`: 1240 checks, 0 failures. No reader script for exp-log problems exists in `docs/reports`.
- Playthrough `--problems exp-log/problems-1 --local-cdn`: green, 16 parts; with `--mobile`: green; 440 px shots of the coin read, no layout fault.
