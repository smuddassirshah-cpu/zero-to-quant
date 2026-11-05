# Engine pass O1: merge-wave.sh

Files: `app/tools/merge-wave.sh`, `app/tools/test-merge-wave.sh`, backlog item 522. No content or engine files touched; usage is in the script's head comment (AUTHORING.md has no tools section).

Behaviour: per branch, `git merge --no-ff --no-commit`, then per conflicted file: drills index union by id (ours first); `BACKLOG-INBOX.md`, `PROGRESS.md`, `docs/reports/*.md`, `docs/reviews/*.md` via `git merge-file --union`; review JSON takes the side with the newer `%ct` of its last commit on that path (tie keeps ours); other files abort the merge and print `UNRESOLVED <branch>: <files>`. Conflict markers are scanned on the lines the merge adds (so legitimate `=======` rules in existing markdown do not trip it). The validator runs from `app/`; errors above 0 abort; otherwise `manifest.json` is staged and the merge is committed as `Merge <branch> (merge-wave)`. Verbose log: `${TMPDIR:-/tmp}/merge-wave.log`. Exit non-zero if any branch is not merged. The tree must be clean at start.

Test: clones the repo, copies the script in, builds `wave-a` and `wave-b` (conflicting edits to the three files, review commit dates 1 and 2 January 2026), merges both. Asserts exit 0, no markers, each drill id present exactly once (including one added by both sides), both inbox lines, newer review side kept, validator 0 errors, clean tree. Result: PASS. Note the drill index validator needs each listed id to have a drill file, so the test uses unlisted existing drills.

Not covered: delete/modify conflicts on the rule files are reported UNRESOLVED; no test for the UNRESOLVED path.
