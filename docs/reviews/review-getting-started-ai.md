# Review: Getting started (session AI)

A follower with no project knowledge walked `README.md` then `app/README.md` on a fresh HTTPS clone of `claude/session-ai-route-done-426vot` at 42cc5215. Screenshots: scratchpad `readme-follow/` (not kept).

Worked: clone, `app/run.sh`, first load, `#setup` then `#today`. jsDelivr is blocked in this sandbox, so the CDN path was not tested. After `app/tools/fetch-vendor.sh` (about 45 s), a Python and a C++ code item passed with the CDN blocked, and the expression widget showed the maths field; without `vendor/` it fell back to the text box, as the README says.

Findings:
1. Self-hosting needs bash, curl, openssl, bzip2 and Node; the README said Node is only for the checking tools.
2. The root README did not name `fetch-vendor.sh`.
3. MathLive and Compute Engine sizes were wrong (about 1.4 MB and 0.6 MB on disk, not 5 MB and 4 MB).
4. With the CDN unreachable and no `vendor/` copy, a Python check took about 5 minutes to fail and showed the heading "Not quite right." (engine; KNOWN_ISSUES).
5. The 404s of the vendor probes with an empty `vendor/` were not mentioned.
6. The `--core` argument order of `fetch-vendor.sh` was not shown.
7. Setup also asks for a starting stage.
8. `run.sh` listens on all interfaces, not only localhost.
9. No example route to check Python and C++ (`#lesson/first-python/l1-calculator` works).

## Fix pass

See the commit "Getting started: fix pass" (findings 1 to 3 and 5 to 9 in the READMEs; 4 described there and left to KNOWN_ISSUES).
