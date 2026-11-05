# Zero-to-Quant: session operating model

Scope: how sessions are run, not what is built. Read with `review-course-correction.md`. Nothing here lowers a quality gate; each change moves a check earlier, makes it mechanical, or stops paying for it twice.

## 1. What actually limits throughput

Evidence from the repo at `f9a4545`:

- The binding constraint is the usage cap, not wall-clock. The 5-hour window stopped session H mid-task (`KNOWN_ISSUES.md:109`); the weekly cap stopped eight agents at once on 29 Oct (`:52`). Parallel agents do not make the cap go further; they reach it sooner with more unfinished work in flight.
- Fixed overhead per agent is large. Every content-author reads `docs/AUTHORING.md` (742 lines) and `LEVEL-BRIEF.md` in full before writing one level of 4 to 6 lessons. One level per agent means the 742 lines are paid per level.
- Rework is the largest variable cost. Topic 3.3's second reads produced 221 findings, 213 fixed; topic 2.1 carried about 580 long sentences a voice scan later caught. Each level passes through: author, validate, playthrough, report, answer check, fix, recheck, second read, fix pass, voice scan, playthrough again. Several of these find the same classes of defect.
- The orchestrator does hand merges of parallel worktrees and resolves conflicts itself (`DECISIONS.md:71,79`), which spends main-session context on mechanical work.
- Stale state files cost the first ten minutes of every session and have already caused wrong decisions (dates, hours, exam list).

## 2. Changes, in order of payoff

### 2.1 Author to the corrected standard, once

Do course-correction items 1 to 5 before writing any of the 160 unwritten lessons. A lesson written now has no performance task and no per-level `pass`; it will be retrofitted later at a second full cost. Writing it after item 5 costs once. This is the single largest saving available and it is free.

### 2.2 Make recurring findings mechanical

Rule: any finding class that appears three or more times across `docs/reviews/` becomes a validator rule or a script before the next content wave. Candidates already visible: long sentences (voice scan exists; make the validator run it), per cent keys (item 515, done), unshuffled interval choices, distractor values that do not match slips, prose and prompt both present, numbers in `explain` that disagree with `answer`. The validator costs nothing per run; an Opus second reader costs the most of anything in the pipeline. Every class moved to the validator is a class the reader never has to find again.

### 2.3 One agent per course, not per level

Amortise the 742-line read across a course's levels. The agent writes level n, commits, validates and plays through that level, then starts level n+1 in the same worktree. Checkpoint commit per level stays (the cap can stop it at any point). Cap: one agent carries at most three levels, because quality degrades as context fills; a six-level course gets two agents in sequence, not one.

### 2.4 Collapse the check chain to three passes

Now: answer check, recheck, second read, fix pass, voice scan, recheck. Replace with:

1. Author self-check before handoff: validator at 0 errors, voice scan at 0 and 0, every stated number recomputed by a script committed beside the report (`docs/reports/<course>-<level>-numbers.py` or similar), playthrough with and without `--mobile`. A level that arrives without these is sent back, not read.
2. Second read (Opus) that recomputes by running the author's script, not by hand, and reads for meaning, generalisation and whether the quiz measures the objective. One file of findings.
3. One fix pass (Sonnet, targeted edits) and one playthrough of the changed files only. Recheck is limited to changed keys, as now.

The answer check as a separate session-level pass goes; it is step 1 and step 2's script run.

### 2.5 Model routing

- `content-author`: Opus, keep.
- Second reader: Opus, keep.
- `test-fixer`: Sonnet. Applying a findings file with targeted edits does not need Opus; the judgement was already made by the reader.
- `engine-dev`: Sonnet, keep.
- Answer recompute, census, voice scan, merges: scripts, no model.
- `explorer`, `file-finder`: Haiku, keep.

### 2.6 Script the merge

The merge rules in `DECISIONS.md:79` are mechanical (union `drills/index.json` by id, keep both sides of `BACKLOG-INBOX.md`, newer side of a review file, re-validate). Put them in `app/tools/merge-wave.sh`. The orchestrator runs it and reads only its last five lines.

### 2.7 Wave sizing against the cap

- Start a parallel wave only with more than half the 5-hour window left. A wave is three to four agents, never eight.
- Use the last hour of a window for Haiku and script work: census, state files, NEXT_PROMPT, merges, triage.
- Every agent commits per level with a message that names the level; a stopped agent is then resumed from its branch, not restarted.
- When the weekly cap is near, finish and merge what is open rather than start anything.

### 2.8 State files from source, not memory

`app/tools/census.mjs` (course-correction item 1) is the only source of counts in PLAN, PROGRESS and KNOWN_ISSUES. Dates come from `git log`. NEXT_PROMPT.md names the census output it expects at the next session's start, so drift is caught in the first minute.

### 2.9 Topic closing stays, with the gate moved

The rule "a topic closes when every level, its exam, mocks, second read and fix pass, and a green playthrough are done" is right and stays. What changes is that the author's self-check (2.4 step 1) is the gate for handing a level to the reader, so the reader reads finished work and finds fewer, better findings.

## 3. Drop-in replacement for CLAUDE.md "SESSION PROTOCOL"

Replace the existing block with this once course-correction item 1 is committed.

```
## SESSION PROTOCOL
1. Start: run `node app/tools/census.mjs | tail -20`, then read NEXT_PROMPT.md, PLAN.md, DECISIONS.md, KNOWN_ISSUES.md. If the census disagrees with PLAN or PROGRESS, fix the state files first and record the drift in KNOWN_ISSUES.
2. Work the next unchecked task in PLAN.md. Course-correction (2c) tasks run before any content expansion until 2c items 1 to 5 are ticked.
3. Waves: three or four agents, each in its own worktree, each owning one course for up to three levels, committing per level with the level in the message. Start a wave only with more than half the usage window left. Merge with `app/tools/merge-wave.sh`; read its tail only.
4. A level is handed to a second reader only with: validator 0 errors, voice scan 0 and 0, a committed number-recompute script that passes, playthrough green with and without `--mobile`. Otherwise it goes back to its author.
5. Check chain per level: author self-check, one second read that runs the author's script, one fix pass on Sonnet, playthrough of changed files. No separate answer-check pass.
6. Any finding class seen three times in docs/reviews becomes a validator rule or script before the next wave; raise it as an engine item.
7. Stay thin: never read large files, logs or full output. Reports under 200 words; detail to files.
8. Before ending: commit, tick PLAN, one PROGRESS line dated from `git log`, record decisions and issues.
9. Last: write NEXT_PROMPT.md (exact next task, context not in state files, files to touch, acceptance check, expected census figures; under 300 words) and print it in full.
```

## 4. What not to change

- Brief before level, second read before close, playthrough at phone and tablet widths, every number computed twice (now: once by the author's script, once by the reader running it).
- Never rename or remove a lesson id.
- Strict prerequisites on by default; closures as recorded in DECISIONS.
- British English, no exclamation marks, no em-dashes, sentences under 20 words.

## 5. Expected effect

Rough, from the numbers above: 2.1 avoids a second pass over about 160 lessons and every performance task; 2.2 and 2.4 remove the duplicated checks and most of the reader's mechanical findings, which in topic 3.3 were the majority of 221; 2.3 cuts the fixed read per level by two thirds; 2.5 moves the fix passes off Opus. Together, the same cap buys roughly twice the accepted content per week. The pilot and capstone review (course-correction items 8 and 12) are unchanged: they are human time and no session model shortens them.
