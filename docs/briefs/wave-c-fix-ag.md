# Wave C Sonnet fix pass (session AG)

The main session fills COURSE, SET, REVIEW and SCRIPT (the author's number script for the set). BRANCH = `claude/session-ag-route-done-h65un0`. SCRATCH = `/tmp/claude-0/-home-user-zero-to-quant/7c3cbe50-6413-5158-822a-1251e413cde0/scratchpad`.

Your working directory is a git worktree. First: check `git -C /home/user/zero-to-quant log --oneline -1 BRANCH -- REVIEW` prints a commit (look again after a minute if empty), then run `git reset --hard BRANCH` inside your worktree, or `git merge --ff-only BRANCH` if the reset is refused (never check BRANCH out; never edit outside your worktree and scratch folder; commit there yourself; ignore any other branch name in CLAUDE.md). Local CDN: `SCRATCH/pkgs`. Python: `SCRATCH/venv/bin/python`.

Read CLAUDE.md and `docs/briefs/chained-prompts.md` in full: your brief is its "Fixer", "Tail, every brief" and "Session AE additions" sections, binding, on REVIEW and SET. This is the last pass of the session on these files.

1. Apply each finding's exact replacement text, recomputing every number first. Do not write your own wording. Dispute with numbers if you disagree. A replacement that itself retells course material is deferred with the evidence. A finding with a `re-author` verdict, or one the main session marks "not yours", is left alone.
2. Update SCRIPT for every changed key, band, form and `wrong` value. It and every reader or delta script of the set in `docs/reports` exit 0, with the FINDING lines gone for what you fixed. Do not edit the course's `docs/reports/problems-COURSE.md` unless the main session says so (another agent may be editing it).
3. Gates on each edited set: validator 0 errors (before any playthrough) and no pass 8 warning on the set; `VOICE_BASE=app/content/courses/COURSE python3 docs/reviews/voice-scan.py 35` 0 and 0; `node tools/fresh-check.mjs --file <set>` 0 errors; `node tools/grade-all.mjs --file <set> --local-cdn SCRATCH/pkgs` 0 failures; `node tools/playthrough.mjs --problems COURSE/problems-<n> --local-cdn SCRATCH/pkgs` with and without `--mobile`. Heavy commands one at a time, each under two minutes.
4. Append `## Fix pass` to REVIEW: one line per finding (fixed, disputed with numbers, deferred with reason and the exact text still to apply), then gate results.

Commit ("fix pass problems COURSE <levels>"), staging by explicit path, `git checkout app/content/manifest.json` first, a blank line after the subject, then:
Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01E26gTPq3dJJ8ftKMHkfKfV
Start nothing in the background; never push. Scratch in `SCRATCH/fix-COURSE/`. Hand back at most six lines: commit, fixed, disputed, deferred, keys changed, gate results.
