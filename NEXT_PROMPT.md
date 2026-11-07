Read CLAUDE.md and follow its SESSION PROTOCOL. Branch `claude/amazing-wright-d4mx7i` only; work detached at `origin/claude/amazing-wright-d4mx7i`, push `HEAD:claude/amazing-wright-d4mx7i`, rebase on divergence, never reset. Build the local CDN in the background first: `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`. Launch long runs with `setsid nohup` (container restarts killed three runs in session V).

Expected census: lessons 1,214 of 1,214; levels 279 of 279; reviews 279, own pass 279; exams 29 topic, 4 stage, 16 mock; drills 35 (oa 8); bank 200; hours 3,695, gap 0; readiness-sums OK; validator 0 errors.

First, carried from session V: `--all --shard 3/4` and `4/4 --local-cdn`, then `--routes-only --local-cdn` desktop and mobile, at HEAD (shards 1 and 2 green at ca8e737; all `tools/test-*` green). Run them one at a time, never during a merge.

Second, a user bug: Today still shows a half-finished 0.1 lesson after topic-0.1 was passed. ENGINE-BACKLOG 461 skips a tested-out course unless the resume position was saved after the pass (`content.resumeStands`). Reproduce with Playwright (pass topic-0.1 with a lesson part-open, then reopen Today), find why it stands, and fix it so a pass always moves Today on unless the learner reopened that lesson from Learn. One engine agent; test both routes.

Then Phase 2 of `docs/briefs/session-v-plan.md`: second reads and fix passes for the 61 levels in `docs/reports/unread-levels-session-v.txt`, in its order, then the nine unread topic exams. Briefs: `docs/briefs/second-read-reader-brief.md` (Opus, one course, up to three levels) and `second-read-fixer-brief.md` (Sonnet; basis or dispute per conceptual fix; tighten checks to new values). Pipeline, four slots: a fixer starts as soon as its review merges; split a four-level course into L1 to L2 and L3 to L4 with disjoint files.

Then Phase 3 (108 performance tasks), Phase 4 (drill packs 1 to 8, bank part 2).

The Fable audit is paused (user, usage): trigger `trig_01FJuNVhosR68kSj3RhYkXrp` stays disabled; do not restart it. Its branch is fully merged.

Acceptance: validator 0 errors; readiness-sums OK; all `tools/test-*` pass; four shards and routes green; state files; NEXT_PROMPT for session X.
