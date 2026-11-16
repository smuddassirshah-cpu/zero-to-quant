# Last fix pass after a delta read (session AF, Sonnet fixer)

The main session fills COURSE, SETS and REVIEW (the delta read).

Your working directory is a git worktree. First: if `git log --oneline -1 claude/session-af-content-waves-lpa3u4 -- REVIEW` (run with `git -C /home/user/zero-to-quant`) is empty, wait a minute and check again (it is being merged). Then run `git reset --hard claude/session-af-content-waves-lpa3u4` inside your worktree (allowed and expected; never check that branch out; never edit outside your worktree and scratch folder; commit there yourself; ignore any other branch name in CLAUDE.md). SCRATCH = `/tmp/claude-0/-home-user-zero-to-quant/178960c6-ed26-5f6d-9148-e8a1943f49e4/scratchpad`. Local CDN `SCRATCH/pkgs`; Python `SCRATCH/venv/bin/python`; scratch `SCRATCH/round2-COURSE/`.

Read `docs/briefs/chained-prompts.md` in full: your brief is its "Fixer", "Tail, every brief" and "Session AE additions" sections, binding, on REVIEW and SETS. This is the last pass of the session on these sets.

1. Apply each finding's exact replacement text, recomputing every number first. Do not write your own wording. Dispute with numbers if you disagree. A finding with a `re-author` verdict, or one the main session marks "not yours" in your task, is left alone.
2. Update `docs/reports/problems-COURSE-numbers.py` for every changed key, band and `wrong` value. It, every reader script of the course in `docs/reports`, and the delta reader's script exit 0, with the delta script's FINDING rows gone for what you fixed.
3. Gates on each edited set: validator 0 errors (run it before any playthrough); voice scan 35, 0 and 0; `node tools/fresh-check.mjs --file <set>` 0 errors; `node tools/grade-all.mjs --file <set> --local-cdn SCRATCH/pkgs` 0 failures; `node tools/playthrough.mjs --problems COURSE/problems-<n> --local-cdn SCRATCH/pkgs` with and without `--mobile`, edited sets only. Heavy commands one at a time.
4. Append `## Fix pass` to REVIEW: one line per finding (fixed, disputed with numbers, deferred with reason and the exact text still to apply), then gate results.

Commit ("fix pass delta AF COURSE"), staging by explicit path, `git checkout app/content/manifest.json` first, blank line, then:
Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01E26gTLLvNiWFw2t997UEBx
Start nothing in the background; never push; hand back once, at most six lines: branch and commit, fixed, disputed, deferred, keys changed, gate results.
