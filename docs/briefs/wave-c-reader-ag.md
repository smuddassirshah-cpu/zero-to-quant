# Wave C second reader (session AG)

The main session fills COURSE and LEVELS. BRANCH = `claude/session-ag-route-done-h65un0`. SCRATCH = `/tmp/claude-0/-home-user-zero-to-quant/7c3cbe50-6413-5158-822a-1251e413cde0/scratchpad`.

Your working directory is a git worktree. First: check `git -C /home/user/zero-to-quant log --oneline -1 BRANCH -- docs/reports/problems-COURSE.md` prints a commit (look again after a minute if empty), then run `git reset --hard BRANCH` inside your worktree, or `git merge --ff-only BRANCH` if the reset is refused (never check BRANCH out; never edit outside your worktree path and your scratch folder; commit there yourself; ignore any other branch name in CLAUDE.md). Local CDN: `SCRATCH/pkgs`. Python: `SCRATCH/venv/bin/python`.

Your brief is `docs/briefs/chained-prompts.md`: "Reader", the Author rules, "Tail, every brief" and "Session AE additions", all binding, with `docs/briefs/chained.md` and `docs/briefs/wave-c-author-ag.md` (the author's added rules 1 to 6, which you check). Added for this read:

1. Exams are in the reuse scope: read every exam item that carries one of the course's skills (skill ids from `course.json`, searched in `app/content/exams/*.json`). Per problem, name the closest lesson screen, quiz item, review item, homework item, other set problem and exam item, and rule `clean`, `reuse` or `re-author` with both texts. `re-author` is for a problem that walks several quiz, review or exam items in a row, or retells a lesson screen with other nouns or numbers; it carries the screens and items not to walk, no replacement text. Expect about a quarter of problems to be ruled re-author; do not force the number.
2. Bands: each takes the value the part's printed working gives and every accepted rounding of the stated form, and refuses each `wrong` value; no key or slip on a rounding tie; a tail or table value names its source; a percentage part carries unit "%"; a slip band is no wider than its value warrants.
3. Proof-heavy levels: flag any part passable by working backwards from a printed target, and any claim ("always", "never", a theorem's hypothesis, a counterexample) that is false or needs a missing condition. Check each definition against the course's own lesson wording.
4. Your script `docs/reports/problems-COURSE-numbers-read.py` resolves paths from `__file__`, exits 0, prints a `FINDING` line per failing check, and must not fail where a numerical solver does not converge on another SciPy build.
5. Tools per set: validator; voice scan 35; `node tools/fresh-check.mjs --files <sets> --pairs`; `node tools/grade-all.mjs --file <set> --local-cdn SCRATCH/pkgs`. Heavy commands one at a time, each under two minutes. No browser.

Output `docs/reviews/review-problems-COURSE-LEVELS.md` in the format of `docs/reviews/review-problems-analysis-1-3.md`, with the per-problem verdict table first. Commit review and script ("second read problems COURSE LEVELS"), staging by explicit path, a blank line after the subject, then:
Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01E26gTPq3dJJ8ftKMHkfKfV
Scratch in `SCRATCH/read-COURSE/`. Hand back at most six lines: commit, findings by severity, problems ruled re-author (ids), script exit codes, validator, grade-all.
