# Engine 842 and 843: Fluency state key and Today practice rows

## Evidence
- A four-shard `--all` run passed everything except 13 of 47 Fluency sets, each reporting "Today does not list the set" and "Today dropped the set after a failing attempt". Each passes alone.
- Reproduced: `--fluency-all --shard 1/12` (four sets, one profile) before the change would put the third and fourth set outside Today's rows. The rule is in `app/js/screens/today.js`: `flu.slice(0, 2)`.

## 842 State key (tool fault, no product fault)
- `ZQ.state.fluency` keys `<course>/<set id>` (`fluencyKey` in `app/js/state.js`). The weekly review writes and reads through the same `fluency.result` and `fluency.get` with the course and set id (`app/js/engine/select.js`), so it uses the same key. There was never a bare set-id key, so there is nothing to migrate and no old key to keep readable: a learner's attempts are untouched.
- The apparent collision: the fixture `app/tools/fixtures/fluency/fluency-l3-opening-brackets.json` declares `"course": "equations"` and the same id as the real equations set, so both are one record by design. The fixture run began at `"attempts":4` because the real set had just been played in that profile. Fix in the tool: `playthrough.mjs` clears the set's record before it plays each set.
- Test: `tools/test-fluency.mjs` (browser part) saves one set id under two courses and checks separate attempts, best, pass and families, and that no bare-id key appears.

## 843 Today's practice rows (product gap plus tool fault)
- Cause: Today shows at most two Fluency rows by design, newest lesson first, then only a caption "N more fluency sets on the course maps". With many lessons done the set under test was beyond the two rows, and the playthrough probe looked only at those rows.
- Product change: the cap stays (a learner should not see 40 rows). The caption is now a row "More Fluency sets" leading to the new route `#fluency-list` (`app/js/screens/fluency.js`): every set grouped by course, each with lesson done or not and passed or not, each opening the set. Documented in `docs/AUTHORING.md` section 16.
- Tool change: the playthrough accepts the set as a Today row or as an open item in the full list. New flag `--fluency-all` plays every set and the fixtures in one profile (lessons marked done as it goes), with `--mobile` available.

## Results
See the hand-back; counts are at the foot of this file.

All checks: validator 0 errors, readiness-sums OK, every tools/test-* green, 48 Fluency items green in four shards on desktop and --mobile, --routes-only on both.
