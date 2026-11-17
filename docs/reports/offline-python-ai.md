# Offline Python (ENGINE-BACKLOG 1214 to 1216)

**1214.** A Python or C++ load failure is no longer an answer. The lesson player shows a neutral "Python could not load" (or "C++ could not load"): no XP, attempt, Redo entry or wrong-answer styling, and Try again retries the load. Drill pages say the same; a package that cannot download stops the run likewise. The 5 minutes were stacked budgets (60 s load, 2 minutes per package, 60 s restart; C++ a flat 5). Now the CDN probe stops at 8 s and a load stops after 30 s with no bytes (C++ 90 s), at 5 minutes in all.

**1215.** `test-vendor-fallback.mjs` plays a NumPy lesson from vendor; `--absent` times the failure (0.1 s refused, 8.4 s held open) and checks the heading. It fails on the old code.

**1216.** The `python` leg caches the vendor folders (`docs/CI.md`).

## Fix (run 39)

CI run 39 failed `test-planted-check.mjs` (python leg): a planted solution that loops forever never reached its 5 s limit and the drill showed no result. Cause: engine 1214 reworked `prepare()` in `app/js/screens/drill-worker.js` and dropped the `pk('end')` on the success path (it stayed only in the catch). The page therefore never saw the package phase end, kept the 30 s stall timer from `pkgs start`, and when the loop starved the worker it gave up as "a package could not load" (`loading: true`), clearing the run instead of reporting "Stopped at 5 seconds". Fix: `pk('end')` restored after the try/catch, so the 5 s limit is armed as before. The test was not changed. Tests run with the local CDN: test-planted-check, test-drill-page, test-drill-recursion, test-bank-code, all passed; test-vendor-fallback `--absent` and `--vendor` (populated folder, since deleted) passed; validator 0 errors.
