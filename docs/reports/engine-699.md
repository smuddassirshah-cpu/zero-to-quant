# Engine 699: perf-reports checker

`app/tools/perf-reports.mjs` reads `content/manifest.json` `perf` and checks `docs/reports/<course>-<n>-perf.md` for the item id, kind, matched-objective line, "Overlapping screens" line and the four gates; one `<report>: missing <part>` line per gap, no-report levels listed apart, exit 1 unless `--warn`. Test `tools/test-perf-reports.mjs` (fixtures in `tools/fixtures/perf-reports/`) passes. Documented in AUTHORING section 5.

Real repository, `--warn`: 67 levels with a task, 43 reports, 24 without a report, 39 missing parts in 38 reports (Overlapping screens line 38, matched objective 1). Validator 0 errors; manifest restored.
