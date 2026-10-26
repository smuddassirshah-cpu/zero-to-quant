# Engine backlog inbox

Content agents append their engine and canvas limitations here, under `Raised later (<course> level <n>):`, as bullets. An integration pass numbers them into `ENGINE-BACKLOG.md` and clears this file.


Raised later (cpp-pricing level 1):

- C++ runtime (libc++): a range-for over a braced list (`for (double x : {1.0, 2.0})`) fails to compile unless `<initializer_list>` is included directly or by another header; worth a line in AUTHORING section 3's C++ addendum.
- code widget (C++ and Python): `isclose` accepts any two numbers within 1e-12 of each other, so tiny values such as Φ(−10) = 7.6e-24 or 1 − cos(1e-8) cannot be tested directly. A per-case `rel` or `abs` tolerance on code tests is needed; authors currently write `f(x) / exact - 1` with expect 0, or scale the value up.
- `grade.js` `fmtNum`: rounds the test hook's and Show solution's numeric answer to 6 decimal places, so an answer like 9.5e-7 is filled in as 0.000001 and fails its own tolerance. Format with significant figures instead.
- plane canvas derive: a single `area` object cannot be targeted by its id (`A.to`); only `area.to` works. Either support it or document it in README-B.
- bars `sim`: it draws from the app's JavaScript generator, so a histogram cannot show C++ (libc++) draws live. Allowing `data` per control stop, or a seeded C++ source, would avoid precomputed derive tables.
