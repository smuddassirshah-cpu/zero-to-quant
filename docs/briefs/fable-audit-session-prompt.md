Read CLAUDE.md, then `docs/briefs/concept-audit.md` (binding), DECISIONS "Correctness first" and KNOWN_ISSUES. You are the concept-audit session for Zero to Quant. Your one job is to make sure existing content teaches only what is correct. You do not write new content or change the engine.

Git: `git fetch origin claude/amazing-wright-d4mx7i`, then `git checkout -B claude/fable-audit origin/claude/amazing-wright-d4mx7i` (if `origin/claude/fable-audit` exists, check that out instead and rebase it onto `origin/claude/amazing-wright-d4mx7i`; never reset). Work and push only on `claude/fable-audit` (`git push -u origin claude/fable-audit`). Never push to `claude/amazing-wright-d4mx7i`: the content session merges your branch. Build the local CDN in the background first: `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`.

Resume: if `docs/reports/concept-audit-next.md` exists on the branch, read it and `docs/reports/concept-audit-log.md` first and continue from them: finish open courses (fix passes, re-audits) before starting new ones. The same prompt is pasted for every audit session.

Scope: a content session is second-reading and fixing other courses in parallel. To avoid conflicting edits, audit only courses with no entry in `docs/reports/unread-levels-session-u.txt`, and no course a commit on `origin/claude/amazing-wright-d4mx7i` touched in the last day. Order: interview courses and Stage 3, then Stage 2, Stage 1, Stage 0. Exams come after their courses close.

Per course, as `concept-audit.md` says:
1. One auditor (Agent tool, `model: "fable"`, own worktree) per course, up to three levels, blind to earlier reviews until its ledger is written. Output: `docs/reviews/audit-<course>-<levels>.md`, a ledger and a concepts script.
2. Merge with `app/tools/merge-wave.sh`, then start one Opus fixer (`model: "opus"`, own worktree). For each finding it gives its own basis or marks it `disputed: unverified`. Send disputed findings to a fresh Fable reader.
3. Gates per course: validator 0 errors; number and concepts scripts exit 0; `voice-scan.py 35` 0 and 0; playthrough of changed files with and without `--mobile`, with `--local-cdn`.
4. Record the round in `docs/reports/concept-audit-log.md`. Re-audit with a fresh Fable reader until the convergence rule closes the course.

Waves of three or four agents. Start a wave only with more than half the usage window left. Never merge during a playthrough. Do not edit PLAN.md, PROGRESS.md, NEXT_PROMPT.md, DECISIONS.md or course.json. Put state in `docs/reports/concept-audit-log.md`, and put new decisions or issues in `docs/reports/concept-audit-notes.md`. Engine limits go to `docs/BACKLOG-INBOX.md` under `Raised later (audit <course>):`.

Report the miss rate after the first three courses: audit-only conceptual findings per three levels, against the earlier read.

Before ending: commit, push `claude/fable-audit`, and write `docs/reports/concept-audit-next.md`. Under 250 words: courses closed, open, next, and the miss rate so far. Print it.
