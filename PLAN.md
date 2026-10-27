# PLAN

Goal: a single-user, Brilliant-style interactive teaching app (vanilla JS, static, `app/`) that takes a learner from zero to quant-interview ready across Stages 0 to 3 of `docs/curriculum.md`. Every lesson is JSON content played by the engine, validated by `app/tools/validate.mjs` and played end to end by `app/tools/playthrough.mjs`. Done means: every course map level written, every topic and stage exam written, every topic second-read and fixed, the engine backlog inbox integrated, `validate.mjs` at 0 errors and `playthrough.mjs --all` green, and `docs/PLAN.md` section 13 satisfied.

Design documents live in `docs/` (`PLAN.md` there is the product design, not this checklist). Briefs for every unwritten level are in `docs/briefs/`. Conventions are in `CLAUDE.md`.

## Tasks (one per session; tick when committed)

### 0. Triage
- [x] Triage work left in flight on 27 Oct: arma L3 and opt-dash L4 lessons green with reports; garch l5, l9, coint l1, contests l1 kept (`docs/reports/triage-27oct.md`); nothing removed. Pass 7 left no status block; its edits sit in WIP commits; full playthrough 663 of ~1,050 ok, 0 failures, before a container restart stopped it.
- [x] Triage 2 (27 Oct): coint L3, contests L2, L3, L4 green with reports (`docs/reports/coint-3.md`, `contests-2.md` to `contests-4.md`); nothing removed.
- [x] Triage 3 (27 Oct): exams topic-2.1 to topic-2.4 written, green and reported (`docs/reports/exam-2.1.md` to `exam-2.4.md`).
- [x] Full playthrough green with `--local-cdn` (27 Oct): all 739 lessons and 354 sets in the first run; all 19 exams and every route in split re-runs (`--exams`, `--routes-only`); topic-1.3 no longer closes the browser when exams run alone.

### 1. Stage 2 content (brief: `docs/briefs/<course>.md`, section `## Level n`)
- [x] garch L2
- [x] garch L3
- [x] coint L1
- [x] coint L2
- [x] coint L3 (triage 2)
- [x] opt-dash L4
- [x] contests L1
- [x] contests L2 (triage 2)
- [x] contests L3 (triage 2)
- [x] contests L4 (triage 2)

### 2. Stage 1 gap levels (briefs: `docs/briefs/gap-<course>.md`; plan in `docs/briefs/gaps-plan.md`)
- [x] limits L5
- [x] integrals L4
- [x] multivar L5 (brief's 10% target under a 50% cap was infeasible, max 9.5%; transfer uses long-only at 10% and a 45% cap at 9%)
- [x] eigen L4
- [x] random-vars L5
- [x] limits-thm L4
- [x] markov L4
- [x] Extend exams topic-1.3, topic-1.4, topic-1.5 with items for the new levels (each now 30 items, the validator cap; reports `docs/reports/exam-1.3-gap.md`, `exam-1.4-gap.md`, `exam-1.5-gap.md`)

### 3. Stage 3 content (briefs in `docs/briefs/`)
- [ ] momentum-rep L1
- [ ] momentum-rep L2
- [ ] momentum-rep L3
- [ ] pairs-rep L1
- [ ] pairs-rep L2
- [ ] pairs-rep L3
- [ ] ito L1
- [ ] ito L2
- [ ] ito L3
- [ ] puzzles L1
- [ ] puzzles L2
- [ ] puzzles L3
- [ ] puzzles L4
- [ ] mm-games L1
- [ ] mm-games L2
- [ ] mm-games L3
- [ ] mental-pressure L1
- [ ] mental-pressure L2
- [ ] mental-pressure L3

### 4. Exams (pattern: `app/content/exams/topic-1.7.json`; brief pattern in `docs/reports/exam-1.8.md`)
- [x] topic-0.1 to topic-0.5 (Stage 0 topic exams; never written, the Learn screen shows them as unwritten; pattern topic-1.1.json, items from the Stage 0 courses of each topic)
- [x] topic-1.9 (cpp, cpp-pricing; the 1.9 review proposes coverage)
- [x] topic-2.1 (stat-learning, validation, ensembles, fin-ml)
- [x] topic-2.2 (arma, garch, coint)
- [x] topic-2.3 (backtest, alpha, opt-dash)
- [x] topic-2.4 (contests)
- [ ] topic-3.1 (momentum-rep, pairs-rep)
- [ ] topic-3.2 (ito)
- [ ] topic-3.3 (puzzles, mm-games, mental-pressure)
- [ ] stage-1, stage-2, stage-3 exams (pattern: `app/content/exams/stage-0.json`)

### 5. Second readers and fix passes (reader pattern: `docs/reviews/review-1.5.md`; fix pattern: its `## Fix pass` section)
- [ ] Second reader 1.8 (was in flight; no file yet) then fix pass 1.8
- [ ] Fix pass 1.9 (second reader 1.9 is complete in `docs/reviews/review-1.9.md`)
- [ ] Second reader 2.1 then fix pass
- [ ] Second reader 2.2 then fix pass
- [ ] Second reader 2.3 and 2.4 then fix pass
- [ ] Second reader 3.1 to 3.3 then fix pass
- [ ] Fix the seven homework items with both prose and a hidden longform prompt (list in `docs/ENGINE-BACKLOG.md`, pass 6 content note)

### 6. Engine
- [ ] Engine pass 7: backlog items 340 to 422 plus `docs/BACKLOG-INBOX.md` (was in flight; status block "Seventh pass" may be partial). Number inbox bullets from 424, clear the inbox, document in AUTHORING.md and canvas READMEs
- [ ] Engine pass 8: whatever the inbox holds after Stage 2 and 3 content lands
- [ ] Full `playthrough.mjs --all --local-cdn <pkgs>` green; `validate.mjs` 0 errors; System gallery renders in both themes

### 7. Finalise
- [ ] Getting started: `app/README.md` and `README.md` describe clone, `app/run.sh`, first load (jsDelivr for Pyodide, MathLive, Compute Engine, YoWASP clang), the self-host fallback in `app/vendor/`
- [ ] Check `docs/PLAN.md` section 13 (definition of done) item by item; record gaps in KNOWN_ISSUES.md
- [ ] Final report to the user; create `DONE`

## Completed
- [x] Stage 0 content (163 lessons, 76 sets, stage exam)
- [x] Stage 1 original content: all 426 lessons and 204 sets of topics 1.1 to 1.9
- [x] Exams topic-1.1 to topic-1.8
- [x] Second readers and fix passes for topics 1.3, 1.4, 1.5, 1.6, 1.7
- [x] Gap-pass plan: seven new levels added to course maps, briefs written
- [x] Stage 2: stat-learning, validation, ensembles, fin-ml, backtest complete; arma L1, alpha L1, L2, opt-dash L1, garch L1
- [x] Briefs for every remaining course and level
- [x] Engine passes 1 to 6; C++ runtime (clang in WebAssembly); Python via Pyodide with scikit-learn and statsmodels
