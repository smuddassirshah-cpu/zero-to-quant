# Engine pass AD part 1: backlog numbering, number-script triage, CI runner

## A. Backlog (items 971 to 1027)

83 inbox bullets (every one after "Raised later (problems elimination)") were numbered by script-assisted reading: 82 became 52 items (974 to 1025, 30 merged, each with a count and sources), 1 merged into 970. Two items (1026, 1027) come from KNOWN_ISSUES session AC. 971 (runner, done), 972 and 973 (in flight, `engine-pass-ad-2.md`) are the reserved items. Last number used: **1027**. The inbox is now its header plus one line naming commit 619c0dd.

## B. Triage of the 28 older failures (3 + 6 + 15 + 3 + 1) plus `bank-2-s2`

| class | n | scripts | what was done |
| --- | --- | --- | --- |
| load only (pass alone) | 3 | `coding-int-3-perf` 28 s, `coint-1-perf`, `coint-L1` | AC ran 4 at once with threaded BLAS; the runner sets `OMP/OPENBLAS/MKL_NUM_THREADS=1`. |
| slow | 6 | `bank-2-s3` (more than 160 s alone), `fluency-exp-log` (more than 110 s), `-integrals`, `-odes`, `-quadratics`, `problems-limits` (69 s) | `bank-2-s3`: the brute-force twin built a `Counter` of 1,000,000 values per call, 3,000 calls (finding 9 test); cached, now 26 s. Fluency: 60 seeded draws (`FLUENCY_N`, was 200): 35 to 69 s with 4 running. `problems-limits` 69 s alone, no cheap change; passes inside the 150 s limit. |
| script rot | 15 (+1) | `exam-0.1`, `0.2`, `1.1`, `1.2`, `exam-mock-oa-sig` read, `number-sense-4`, `quadratics-4`, `stat-learning-4`, `testing-4` readers, `py-found-L1..L4`, `exam-stage-2` (3 of 4 failures), `numerics-L3`; the 29th, `bank-2-s2`; `problems-limits` is also rot (the `sign` slip helper) | Content had been fixed or rebuilt after the script (items replaced, exam grown to 28 or 29 items, paces, 35 m/s, 87,000) or the script asserted a fault by construction; the checks now assert the fixed state. `py-found`: nested `isclose`, `prelude` and `compare: "raises"` (item 1010). `numerics-L3`: float noise at 2.5e-13 needs an absolute band. `bank-2-s2`: DECISIONS keeps 11 tests for `ds-pointers-merge-ticks`. `quadratics-4` read a cwd-relative path. |
| not number scripts | 3 | `number-sense-4 dump.py`, `review-problems-number-sense-1-3 show.py`, `taught.py` | Name has no `number`; not run. |
| passes now | 1 | `coding-int numbers_fix.py` | Not reproduced. |
| content finding | 2 | `garch-L2-numbers.py` (not on the AC list), and the one failure left in `exam-stage-2 check_numbers.py` | Left failing, in `tools/number-scripts-known-failing.txt`; `docs/reports/number-scripts-ad.md`. |

Also repaired: `garch-L3` (fit-sensitive last digits, relative 1e-6). Scripts timing out only under load in my batches: `arma` x4, `exam-2.2`.

## C. Runner (item 971)

`app/tools/run-number-scripts.mjs`: finds 358 scripts, runs 4 at a time with a 150 s limit (process group killed), prints failures with their last lines and one count line, exits 1 on a new failure, a listed script that passes, or a listed path gone; `--only`, `--changed [ref]`, `--list`, `--python`, `--timeout`, `--jobs`. Test `app/tools/test-run-number-scripts.mjs` (13 checks pass). `acceptance.yml`: one new job `number-scripts` and its name in the `acceptance` needs; `ci-coverage.mjs` 0 problems. Docs: `docs/CI.md`, `docs/AUTHORING.md` (after "Recompute script"). Full run in batches of at most 110 s: 358 scripts, 356 passed, 2 known failing, 0 new, about 485 s of wall clock in 20 batches (4 jobs).

Not run: `validate.mjs`, `playthrough.mjs` (no engine or content file changed; only tools, scripts and docs).
