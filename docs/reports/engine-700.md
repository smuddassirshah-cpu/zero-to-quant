# Engine 700: NaN-aware compare

`app/js/engine/widgets/code.js` (`__zq_cmp`, the shared Python judge used by the widget and the playthrough): NaN in the actual matches NaN in the expected at the same position, for scalars, lists, arrays, Series, in `isclose` and `equal`; NaN against a number fails both ways. A DataFrame compares by `to_numpy().tolist()`; a DataFrame `expect` also checks index and columns. Tolerances, complex, `fraction`, `stdout`, `raises` unchanged. `screens/drill*.js` use their own scalar comparison and were left alone (not the code widget).

Dicts: compared by exact key set, then value by value (same rules).

Tests: 25 cases in `app/tools/test-engine-runtime.mjs` (unit part, local Python with NumPy and pandas). Docs: AUTHORING section 3, backlog 700 Done.

Checks: validation/homework-2 and fin-ml/homework-2 playthroughs pass.
