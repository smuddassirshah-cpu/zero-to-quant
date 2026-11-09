# micro level 3: performance task (PLAN 2a Phase 3 retrofit)

- File: `app/content/courses/micro/homework-3.json`, item `h-derive-tilted-quotes`, index 8 (item 9 of 9; nothing converted).
- Kind `derivation` (longform, empty box), difficulty 5, skills `ms-mm`, `ms-costs`.
- Matched objective: l11 "Derive the zero-profit half-spread $s = \alpha\delta$." The only objective of the level the verb rule matches (micro is Stage 1, so l10 and l11 "Explain" do not count).
- Task: uninformed flow tilted to buying with chance $\beta$; (a) derive the zero-profit ask $V + a$ and bid $V - b$; (b) reduce to $s = \alpha\delta$ at $\beta = \tfrac12$; (c) $\alpha = 0.2$, $\delta = 21$p, $\beta = 0.75$ give $a = 3$p, $b = 7$p, and why the bid is further; optional (d) symmetric quotes break even on average but lose 2.8p a sell. Assumptions stated: two-point value, type independent of value, one share, always trades, quotes leave $\alpha, \beta, \delta$ fixed, zero profit per side.
- Rubric 3, 2, 2, 2, 1; rows 1 to 4 `required`, row 5 is the prompt's "Optional, one more point". `rubric-passes.mjs`: only minimal pass rows 1 to 4; only row 5 can be left out.
- Overlapping screens: l11 screens 3 and 4 ($P(\text{high} \mid \text{buy})$, $E[V \mid \text{buy}]$), 7 (the formula stated) and 8 (the $s = \alpha\delta$ derivation put in order, coin-toss noise). New: noise with $\beta \ne \tfrac12$, asymmetric quotes, the bid from a written derivation, and per-side against average zero profit.
- Freshness grep (course folder, every hit read): `rebalanc`, `\beta`, `lean`, `21p`, `asymmetr`, `E[V \mid \text{sell}]`, `noise`, `competit`, `index`; `fresh-check.mjs --file content/courses/micro/homework-3.json`: 0 hits.

## Gates

1. Validator: `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; expected warning "micro/L3: has a performance task, remove from perf-pending". Manifest restored before commit.
2. Voice: `VOICE_BASE=app/content/courses/micro python3 docs/reviews/voice-scan.py 35`: 0 explanations over three sentences; 1 sentence over 35, pre-existing in `l6-impact.json` screens[4].prose (level 2, not mine to edit). The new item has 0.
3. Numbers script: `python3 -I docs/reports/micro-3-perf-numbers.py`: exit 0, 510 checks. Closed forms against exact tree enumeration (Fractions, 19 x 19 grid), the weighting route, a seeded 400,000-arrival simulation, (d) both ways, tick sets.
4. Playthrough: `node tools/playthrough.mjs --set micro/homework-3 --local-cdn <pkgs>`, with and without `--mobile`: All passed, 2 longform marked by the button, no display wider than its column. No older item flagged.

One backlog bullet. No course.json change.
