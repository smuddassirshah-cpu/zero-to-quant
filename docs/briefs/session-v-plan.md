# Session V plan (written at the close of session U, 6 Nov 2026)

Scope is ordered by value. Do the phases in order; within a phase, run waves of three or four agents (SESSION PROTOCOL 3). Quality gates never move: an item that cannot meet them carries to session W rather than landing weaker. Stop starting new work when under half the usage window is left, and finish what is in flight.

## Rules learnt in session U (binding)

- A fix agent starts only after its review merges. One reader covers at most three levels of one course, or one exam.
- Never merge while a playthrough shard runs: the validator rewrites `content/manifest.json` and a shard can read it half-written.
- Never `git checkout -- app/content/manifest.json` in the main session before a commit: run the validator and commit the regenerated manifest.
- Readers check claims, not only numbers: every author script this session passed while its level held wrong inequalities, coverage claims and code-behaviour prose. Readers recompute every key and every wrong value and run every code item in CPython.
- Freshness: every new exam reused lesson setups. Grep `app/content` for each new item's key nouns and function names, and run `fresh-check.mjs --min-run 10`.
- Sentences: 20 words is a target; the gate is 35 (DECISIONS 6 Nov).

## Phase 1: engine pass (before any content wave; protocol 6)

Two engine agents in parallel, disjoint files. Each numbers its items from the tail of `docs/ENGINE-BACKLOG.md` (590 was the last), documents author-facing changes in AUTHORING.md, adds tests, and runs `--all --shard i/4 --local-cdn` where the change touches rendering or grading.

Agent A (runtime and exams):
1. Shuffle by default for `choice` and `multi`, seeded per attempt; `shuffle: false` opts out; the validator warns on `shuffle: false` unless the options are ordered numbers or intervals (as O2 detects) or refer to each other. The playthrough must answer by option id, not position.
2. `required: true` on a paper item: the paper fails if that item is wrong. Then set it on the code exits named in `review-exam-stage-1`, `-stage-2`, `-stage-3`, `-mock-oa-code-hard` and `-mock-superday-strats` (content edits done by a Sonnet fixer after the engine merges).
3. Per-paper `tracks` on mock papers; draws seen in any exam or mock count as seen; `importHint` reads a test's `setup`; `expression` `form` (`rectangular`, `simplified`) for constant answers; a test for the 589 Skip marking path; a longform part scores ticks over points.
4. libc++ hardening: a mode that keeps bounds messages without the tree walk on every erase, or document the cost in the C++ addendum.

Agent B (validator and tools):
1. `fresh-check.mjs`: count word tokens only in a run (drop LaTeX commands, braces and number placeholders); compare code function and class names across starters, tests and solutions. Recalibrate on the session U cases and set a gate that the six session U topic exams pass without false hits.
2. 584 refinement (warn only when no `wrong[]` id has its own line); 585 false-positive exclusions (the eight in `docs/reports/scan-positional-options.md`); float `example` without `compare` warning; numeric wrong band narrower than the asked rounding; float artefacts in shown text; thousands comma inside `$...$`.
3. `merge-wave.sh`: union rules for `docs/briefs/*.md` and `docs/readiness.md` rows, and regenerate `content/readiness.json` with `readiness-sums.mjs --write` after a merge, as the session U mock merges needed by hand.

Then, while Phase 2 runs, a third engine agent takes the rest of engine pass 7 (PLAN section 6) and the inbox, numbering bullets.

## Phase 2: second reads and Sonnet fix passes (the main work)

The 90 unread levels in `docs/reports/unread-levels-session-u.txt`, in its order. One Opus reader per course (up to three levels; split a four-level course into two readers), pattern `docs/reviews/review-algebra-1-2.md` (findings with file, path, evidence, exact fix, severity). One Sonnet fixer per review after it merges, pattern its `## Fix pass`. Each fix pass also clears that course's sentences over 35 words and explanations over three sentences, adds missing checks to the course's number scripts, and replays changed files desktop and mobile.

Also read the topic exams with no second-read file (the list file's last line) after their courses' levels are fixed, one reader per exam.

## Phase 2b: concept audit (user, 6 Nov: correctness first)

Deferred by the user (6 Nov): the blind concept audit (`docs/briefs/concept-audit.md`) runs on Fable once all content is finished, after Phases 2 to 4. Phases 3 and 4 do not wait for it. Meanwhile every fixer gives its own basis for each conceptual fix or disputes it.

## Phase 3: performance-task retrofit (only with over half the window left)

`app/tools/perf-pending.json` lists 108 grandfathered levels. Retrofit order from DECISIONS "Performance tasks": interview courses and Stages 2 and 3 first. One item per level, not a level rewrite; one content agent per course, up to three levels; each task second-read with its level's next read or by a dedicated reader. Prune with `perf-pending.mjs --prune`.

Conflict rule (6 Nov): before retrofitting a course, `git fetch origin claude/fable-audit` and skip any course that branch has touched or lists as open in `docs/reports/concept-audit-log.md`; retrofit it after that course closes and the branch merges.

## Phase 4: drills and bank (only with over half the window left)

Drill packs 1 to 8 and bank part 2 (PLAN 2a), with the new freshness gate.

## Also

- The seven homework items with both prose and a hidden longform prompt (PLAN section 5, list in `docs/ENGINE-BACKLOG.md` pass 6 content note): one Sonnet fixer.
- Close: four staggered `--all --shard i/4 --local-cdn` runs green with no merge during a shard; `--routes-only --local-cdn` desktop and mobile; all `tools/test-*.mjs`; validator 0 errors; readiness-sums OK. State files, then NEXT_PROMPT for session W, under 300 words.
