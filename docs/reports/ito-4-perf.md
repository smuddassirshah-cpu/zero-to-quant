# ito level 4: performance task (perf retrofit)

- File `app/content/courses/ito/homework-4.json`, item `h-aloud-unknown-drift`, index 7 (8 of 8), appended; nothing else changed.
- Kind `aloud`: `seconds` 300, `think` 30, `lockAtZero`, three `followUps`. Difficulty 5, skills `it-pricing`, `it-calculus`, no tags.
- Objective: l17 "Derive the Black-Scholes equation aloud inside five minutes, justifying each step." Fresh against `h-derivation` (both homeworks) and `h-replicate`: the drift $\mu_t$ is any adapted process, even path-dependent, and the book is a zero-cost self-financing one with cash. Follow-ups probe self-financing (no $S\,d\Delta$), which risk is hedged, and why the drift drops out.
- Rubric: assumptions 2, lemma and book 2, hedge with $\mu_t$ cancelling 2 (`required`), no arbitrage and equation in time 2, follow-ups 2.
- Gates: (1) `cd app && node tools/validate.mjs`: 0 errors. (2) `VOICE_BASE=app/content/courses/ito python3 docs/reviews/voice-scan.py 35`: 0 and 0. (3) `python3 docs/reports/ito-4-perf-numbers.py`: exit 0, 48 checks in the venv (sympy; seeded self-financing hedge under three drifts). (4) `node tools/playthrough.mjs --set ito/homework-4 --local-cdn <pkgs>`, with and without `--mobile`: All passed. Scratch model shot: no maths overflow at 440 px.
- Freshness grep: mu_t, adapted, whole past, self-financ, S d Delta, unhedged, pays £1. `fresh-check.mjs --file`, also loose: no hit on item 7.
- Backlog: 2 bullets.
