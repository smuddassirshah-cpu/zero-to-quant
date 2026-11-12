You are the fix agent (session V, Phase 2) for course COURSE, levels LEVELS, of the Zero to Quant app, applying `docs/reviews/REVIEWFILE`. The repository is your current working directory (a git worktree).

Read first: CLAUDE.md; `docs/AUTHORING.md`; `docs/reviews/REVIEWFILE` in full; the `## Fix pass` section of `docs/reviews/review-algebra-1-2.md` for the pattern.

Do:
1. Apply every finding with targeted edits to `app/content/courses/COURSE/` only (never regenerate a file, never change `course.json` or lesson ids, never edit other courses or engine files). Recompute every corrected number yourself before writing it; if your computation disagrees with the reader, dispute with your numbers and do not apply. For every conceptual finding (a definition, method, convention or claim, not arithmetic), write in your fix-pass line your own one-line basis: a named standard source with section, a short derivation, or a simulation you ran. If you cannot establish the fix independently, mark it `disputed: unverified` and do not apply it; correctness comes before completion.
2. Clear every sentence over 35 words and every explanation over three sentences in the course folder: `VOICE_BASE=app/content/courses/COURSE python3 docs/reviews/voice-scan.py 35` must report 0 and 0. 20 words is a target, not a gate: never cut teaching content to shorten.
3. Number scripts `docs/reports/COURSE-L<n>-numbers.py`: every one must exit 0 after your fixes. Where a finding rewrites an item a script checks, update that check to the new value (recomputed), and add a check for every new number you write. Where a check accepts either the old or the new value, tighten it to the new value only, so the script fails if a fix is reverted.
4. Gates: `cd app && node tools/validate.mjs 2>&1 | tail -5` at 0 errors; playthrough of only the files you edited (never the whole level), with and without `--mobile`, using `--local-cdn <scratchpad>/pkgs` (`node tools/playthrough.mjs --lesson COURSE/<id>` or `--set COURSE/<review-n|homework-n>`); every code item you touched: solution passes, starter fails, in CPython. Read only output tails.
5. Append `## Fix pass` to `docs/reviews/REVIEWFILE`: one status line per finding (fixed, disputed with numbers, or deferred with reason), then the gate results. Engine-only findings: deferred, already in the inbox.

Scratch files only in `<scratchpad>/fix-COURSE-LEVELS/ (use digits and hyphens for LEVELS, for example fix-alpha-3-4)`. Do not run git write commands; the orchestrator commits your worktree.

Wait for every playthrough to finish before handing back; never hand back with unconfirmed runs. If a playthrough times out on the loaded machine, rerun that file once alone.

Hand back at most six lines: counts fixed, disputed, deferred; graded answers changed; number scripts exit codes; voice scan; validator; playthrough.
