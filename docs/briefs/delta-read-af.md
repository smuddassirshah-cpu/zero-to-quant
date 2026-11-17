# Delta read after a re-author and fix pass (session AF)

The main session fills COURSE, SETS, REVIEWS (the second read or reads with their `## Fix pass`), NAME (the review file's name) and the commit range.

Your working directory is a git worktree. First: if `git merge-base --is-ancestor claude/session-ag-route-done-h65un0 HEAD` fails, run `git reset --hard claude/session-ag-route-done-h65un0` inside your worktree (allowed and expected; never edit files outside your worktree path and your scratch folder, and commit there yourself; that branch is BRANCH, this session's development branch; never check it out; ignore any other branch name in CLAUDE.md). SCRATCH = `/tmp/claude-0/-home-user-zero-to-quant/7c3cbe50-6413-5158-822a-1251e413cde0/scratchpad`. Local CDN: `SCRATCH/pkgs`. Python: `SCRATCH/venv/bin/python`. Scratch: `SCRATCH/delta-NAME/`.

You are the delta reader. You read and report; you edit no content and no engine file. No browser.

Read first: CLAUDE.md; `docs/briefs/chained-prompts.md` ("Author" rules, "Reader", "Tail, every brief", "Session AE additions": binding); REVIEWS in full, with their fix passes; `docs/reports/problems-COURSE.md`; a pattern, `docs/reviews/review-delta-ae-4.md`.

Scope: every problem that was re-authored and every part a fix pass changed (find them from the fix pass lines and `git diff` over the commit range on SETS). Unchanged parts are not re-read, except as reuse sources.

Method:
- Run the author's number script and every reader script of the course. Recompute every key, every `wrong` value and every printed number of the parts in scope yourself, by another method where one exists, in `docs/reports/delta-NAME-numbers.py` (resolves paths from `__file__`, exits 0, prints a `FINDING` line per failing check).
- Check claims: definitions, inequalities, "always" and "never", stem statistics that must agree with each other, a band that must take the value the part's printed working gives and refuse each `wrong` value, no key on a rounding tie, unit "%" on percentage parts, the source of any table value.
- Reuse: for each problem in scope, name the closest lesson screen, quiz, review, homework item, other set problem and exam item (topic, stage and mock exams with the course's items are in scope; the checker reads none of them and catches only close retellings), and rule `clean` or `reuse` with both texts. Check that each fix was applied as the review gave it and that no replacement retells course material.
- Classes: wrong, misleading, reuse, re-author, continuity, voice, other. Every finding carries exact fix text, recomputed, tested on a scratch copy (`fresh-check`, `grade-all.mjs --file`, voice scan) and restored; except a second `re-author` verdict, which carries only the screens not to walk. Be strict on wrong and misleading; on reuse, flag only what a learner who has done the course would recognise, since this is the last read and what stays open goes to KNOWN_ISSUES.
- Tools on each set: validator, voice scan 35, `fresh-check --file`, `grade-all.mjs --file <set> --local-cdn SCRATCH/pkgs`. Heavy commands one at a time.

Write `docs/reviews/NAME.md` (verdict per item, findings, verified with no finding, engine bullets also appended to `docs/BACKLOG-INBOX.md`). Commit review and script ("delta read NAME"), staging by explicit path, blank line, then:
Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01E26gTPq3dJJ8ftKMHkfKfV
Start nothing in the background; never push; hand back once, at most six lines: branch and commit, findings by class, items ruled reuse or re-author, script result.
