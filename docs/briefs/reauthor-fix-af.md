# Re-author and fix pass after a second read (session AF)

The main session fills COURSE, SETS and REVIEW and names the items ruled `re-author`.

Your working directory is a git worktree. First: if `git merge-base --is-ancestor claude/session-af-content-waves-lpa3u4 HEAD` fails, run `git reset --hard claude/session-af-content-waves-lpa3u4` inside your worktree (allowed and expected; never edit files outside your worktree path and your scratch folder, and commit there yourself; that branch is BRANCH, this session's development branch; never check it out; ignore any other branch name in CLAUDE.md). SCRATCH = `/tmp/claude-0/-home-user-zero-to-quant/178960c6-ed26-5f6d-9148-e8a1943f49e4/scratchpad`. Local CDN: `SCRATCH/pkgs`. Python: `SCRATCH/venv/bin/python`. Scratch: `SCRATCH/reauthor-COURSE/`.

You are the author agent for the second read REVIEW of SETS. You do both jobs on these files, since they cannot be split between agents: re-author and fix pass.

Read first: CLAUDE.md; the review in full; `docs/briefs/chained-prompts.md` in full ("Author", "Fixer", "Tail, every brief", "Session AE additions": all binding); `docs/briefs/chained.md`; `docs/reports/problems-COURSE.md`; the topic and stage exams that cover the course (`grep -l COURSE app/content/exams/*.json`), which are in the reuse scope.

A. Re-author each item ruled `re-author`: replace it by a new problem on the same level's skills, with its own setting, data and chain of steps. Where the review says part of the chain is new and may be kept, you may keep it on new data. The review names the lesson screens, quiz, review, homework and exam items each one must not walk; the new problem walks none of them and no other screen or item of the course or its exams, and shares nothing with the course's other set problems. These sets are new this session, so ids may change. A new problem follows every Author rule, with the per-problem list of closest lesson screen, quiz, review, homework and exam item in the report.
B. Fix pass on the other problems: apply each remaining finding's exact replacement text as the reader wrote it, recomputing every number first (Fixer rules: dispute with numbers if you disagree; a replacement that itself retells course material is deferred with the evidence). Misleading and wrong findings are fixed whichever problem they sit in, unless that problem is re-authored. A part that needs a tail or table value says where the learner gets it; a part that asks for a percentage carries unit "%".
C. Update `docs/reports/problems-COURSE-numbers.py` for every changed or new key and `wrong` value; it and the reader's `-numbers-read.py` exit 0 (remove or retarget reader checks of problems that no longer exist, saying so; tighten either-value checks to the new value). Update `docs/reports/problems-COURSE.md`.
D. Gates on each edited set: validator 0 errors (run it before any playthrough, since the manifest checkout hides new sets); voice scan 35, 0 and 0; `fresh-check --file` 0 errors; `grade-all.mjs --file ... --local-cdn SCRATCH/pkgs` 0 failures; playthrough `--problems COURSE/problems-<n> --local-cdn SCRATCH/pkgs` with and without `--mobile`. Run heavy commands one at a time; other agents share this machine.
E. Append `## Fix pass` to the review: one line per finding (fixed, re-authored as <id>, disputed with numbers, deferred with reason), then gate results. A delta reader reads your new and changed parts next.

Commit per set as it passes ("problems COURSE level n: re-author and fix pass"), staging by explicit path, `git checkout app/content/manifest.json` before each commit, with a blank line and then:
Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01E26gTLLvNiWFw2t997UEBx
Edit no set outside SETS. Hand back at most six lines: branch and commit hashes, new problem ids, findings fixed, disputed, deferred, keys changed, gate results.
