# systems level 3: performance task (PLAN 2a Phase 3)

- File: `app/content/courses/systems/homework-3.json`, item `h3-process-aloud`, index 7 (item 8 of 8; was 7, nothing converted).
- Kind `aloud` (120 s, 30 s think, 3 follow-ups). Objective: l11 "Explain a process, a system call and a context switch, and what each costs." The only rule-matched objective in L3 (systems is an interview course, so "explain" matches).
- Task: strategy and order sender as two processes joined by a pipe, 20,000 orders a second. Explain the three terms on this setup, cost each per order, and cut the cost. New against l11 (file reads, a wake per message, `fork`) and l12 (polling `recv`).
- Model: 0.4 µs of calls plus a 5 µs wake (2 + 1 + 2), so 5.4 µs an order, 108 ms a second, about 11% of a core, 93% of it the wake; the TLB cost of a process switch; the fix is a shared-memory ring with a spinning sender.
- Rubric: 2 (process) + 2 (system call) + 3 (context switch and the 5.4 µs, 108 ms figure, required) + 3 (fix, busy core, measure).
- Gates: (1) `cd app && node tools/validate.mjs`: 0 errors (expected perf-pending warning). (2) `VOICE_BASE=app/content/courses/systems python3 docs/reviews/voice-scan.py 35`: 0 and 0. (3) `python3 -I docs/reports/systems-3-perf-numbers.py`: exit 0 (per order against an event count of one busy second). (4) `node tools/playthrough.mjs --set systems/homework-3 --local-cdn <pkgs>`, with and without `--mobile`: All passed; 440 px shots checked.
- Freshness grep: pipe, order sender, shared memory, spin, non-blocking, 20,000, 108, 5.4, address space, scheduler. `fresh-check --file`: one hit, on the older item `h3-feed-summary` (`summarise`), not this item.
