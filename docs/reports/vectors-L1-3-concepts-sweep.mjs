// Sweep of code-widget feedback lines for vectors L3 (audit vectors-1-3, round 1), under the page's Pyodide.
// Run from the repository root: node docs/reports/vectors-L1-3-concepts-sweep.mjs app <pkgs>   (<pkgs> holds pyodide-0.27.7)
// Each row: widget | coding of a mistake | first failing test (got) against the test whose feedback line names that mistake (want; 'any' = no line claims it).
// After the fix pass (docs/reviews/audit-vectors-1-3.md, `## Fix pass`) one DIFF row remains: `solve(b, A)` reaches the test-1 line, which fits it.
// Rows re-pointed by the fix pass: the three `==` codings of s2 now want test-6, the s2 diagonal and rounding codings test-7 and test-8,
// the lax s9 checks test-7 (finding 3), and the i9 padding coding test-1 (finding 14). The fix-pass rows below the main list became main rows.
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
const [app, pkgs] = process.argv.slice(2).map((p) => path.resolve(p));
const { makeRunner } = await import(pathToFileURL(path.join(app, 'tools/code-runner.mjs')).href);
const runner = makeRunner({ pkgs, root: app, jobs: 3 });
const J = (f) => JSON.parse(fs.readFileSync(path.join(app, 'content/courses/vectors', f), 'utf8'));
const l12 = J('l12-numpy-matrices.json'), hw3 = J('homework-3.json');
const W = { s0: l12.screens[0].widget, s2: l12.screens[2].widget, s3: l12.screens[3].widget, s8: l12.screens[8].widget, s9: l12.screens[9].widget, i7: hw3.items[7].widget, i9: hw3.items[9].widget };
const H = 'import numpy as np\n\n';
const body = (sig, lines) => H + sig + '\n' + lines.map((l) => '    ' + l).join('\n') + '\n';
const hg = (e) => body('def hedge_greeks(A, x):', ['A = np.array(A, dtype=float)', 'x = np.array(x, dtype=float)', `total = ${e}`, 'return total']);
const ii = (e) => body('def is_inverse(A, B):', ['A = np.array(A, dtype=float)', 'B = np.array(B, dtype=float)', 'n = len(A)', `return ${e}`]);
const ss = (e) => body('def solve_system(A, b):', ['A = np.array(A, dtype=float)', 'b = np.array(b, dtype=float)', `x = ${e}`, 'return x']);
const th = (e) => body('def three_way_hedge(greeks, target):', ['A = np.array(greeks, dtype=float)', 'b = np.array(target, dtype=float)', `quantities = ${e}`, 'return quantities']);
const sh = (ls) => body('def safe_hedge(greeks, target):', ['A = np.array(greeks, dtype=float)', 'b = np.array(target, dtype=float)', ...ls]);
const mv = (ls) => body('def min_var_weights(cov):', ['S = np.array(cov, dtype=float)', 'ones = np.ones(len(S))', ...ls]);
const rows = `def cash_flow_rows(bonds, years):
    C = np.zeros((len(bonds), years))
    for i, (coupon, maturity) in enumerate(bonds):
        if maturity > years:
            raise ValueError("late")
        C[i, :maturity] = coupon
        C[i, maturity - 1] += 100
    return C
`;
const rowsNoCheck = rows.replace('        if maturity > years:\n            raise ValueError("late")\n', '');
const cb = (pre, ls) => H + pre + '\ndef curve_from_bonds(bonds, prices, targets):\n' + ls.map((l) => '    ' + l).join('\n') + '\n';
const M = [
  ['s0', 'A * x', hg('A * x'), 'test-1'], ['s0', 'x @ A', hg('x @ A'), 'test-1'], ['s0', 'A.T @ x', hg('A.T @ x'), 'test-1'], ['s0', 'np.dot(A, x)', hg('np.dot(A, x)'), null],
  ['s0', 'A.sum(axis=1)', hg('A.sum(axis=1)'), 'test-1'],
  ['s2', 'return True', ii('True'), 'test-2'],
  ['s2', '(B @ A == eye).all()', ii('bool((B @ A == np.eye(n)).all())'), 'test-6'],
  ['s2', 'np.array_equal', ii('np.array_equal(B @ A, np.eye(n))'), 'test-6'],
  ['s2', '(A @ B == eye).all()', ii('bool((A @ B == np.eye(n)).all())'), 'test-6'],
  ['s2', 'np.all(np.round(B@A)==eye)', ii('bool(np.all(np.round(B @ A) == np.eye(n)))'), 'test-8'],
  ['s2', 'allclose(A @ B)', ii('np.allclose(A @ B, np.eye(n))'), null],
  ['s2', 'allclose(B, inv(A))', ii('np.allclose(B, np.linalg.inv(A))'), null],
  ['s2', 'allclose(B * A) elementwise', ii('np.allclose(B * A, np.eye(n))'), 'any'],
  ['s2', 'diag only allclose(np.diag(B@A),1)', ii('np.allclose(np.diag(B @ A), 1)'), 'test-7'],
  ['s2', 'trace check isclose(trace(B@A), n)', ii('bool(np.isclose(np.trace(B @ A), n))'), 'test-7'],
  ['s2', 'diagonal allclose(np.diagonal(B@A), ones)', ii('np.allclose(np.diagonal(B @ A), np.ones(n))'), 'test-7'],
  ['s2', 'array_equal(np.round(B@A), eye)', ii('np.array_equal(np.round(B @ A), np.eye(n))'), 'test-8'],
  ['s2', 'loose tolerance allclose(atol=0.5)', ii('np.allclose(B @ A, np.eye(n), atol=0.5)'), 'test-8'],
  ['s3', 'A @ b', ss('A @ b'), 'test-1'], ['s3', 'inv(A) @ b', ss('np.linalg.inv(A) @ b'), null], ['s3', 'solve(A.T, b)', ss('np.linalg.solve(A.T, b)'), 'test-1'], ['s3', 'b / A', ss('b / A'), 'test-1'],
  ['s3', 'solve(b, A)', ss('np.linalg.solve(b, A)'), 'error'],
  ['s8', 'A @ b', th('A @ b'), 'test-1'], ['s8', 'inv(A) @ b', th('np.linalg.inv(A) @ b'), null], ['s8', 'solve(A.T, b)', th('np.linalg.solve(A.T, b)'), 'test-1'],
  ['s8', 'abs(solve)', th('np.abs(np.linalg.solve(A, b))'), 'any'], ['s8', 'clip to +-1000', th('np.clip(np.linalg.solve(A, b), -1000, 1000)'), 'test-3'],
  ['s8', 'hard-coded 3x3 first matrix', th('np.linalg.solve(np.array([[0.50, 0.25, 0.60], [0.20, 0.30, 0.10], [0.04, 0.02, 0.05]]), b)'), 'any'],
  ['s9', 'starter (no check)', W.s9.starter, 'test-1'],
  ['s9', 'det == 0', sh(['if np.linalg.det(A) == 0:', '    raise np.linalg.LinAlgError("s")', 'return np.linalg.solve(A, b)']), 'test-7'],
  ['s9', 'not det (falsy zero)', sh(['if not np.linalg.det(A):', '    raise np.linalg.LinAlgError("s")', 'return np.linalg.solve(A, b)']), 'test-7'],
  ['s9', 'abs(det) < 1e-10', sh(['if abs(np.linalg.det(A)) < 1e-10:', '    raise np.linalg.LinAlgError("s")', 'return np.linalg.solve(A, b)']), 'test-6'],
  ['s9', 'abs(det) < 1e-12', sh(['if abs(np.linalg.det(A)) < 1e-12:', '    raise np.linalg.LinAlgError("s")', 'return np.linalg.solve(A, b)']), 'test-6'],
  ['s9', 'np.isclose(det, 0)', sh(['if np.isclose(np.linalg.det(A), 0):', '    raise np.linalg.LinAlgError("s")', 'return np.linalg.solve(A, b)']), 'test-6'],
  ['s9', 'always raise', sh(['raise np.linalg.LinAlgError("s")']), 'test-4'],
  ['s9', 'rank < 3 (hard-coded 3)', sh(['if np.linalg.matrix_rank(A) < 3:', '    raise np.linalg.LinAlgError("s")', 'return np.linalg.solve(A, b)']), 'any'],
  ['s9', 'nan check after solve', sh(['x = np.linalg.solve(A, b)', 'if np.isnan(x).any():', '    raise np.linalg.LinAlgError("s")', 'return x']), 'test-7'],
  ['s9', 'isfinite check after solve', sh(['x = np.linalg.solve(A, b)', 'if not np.all(np.isfinite(x)):', '    raise np.linalg.LinAlgError("s")', 'return x']), 'test-7'],
  ['s9', 'raise ValueError on rank', sh(['if np.linalg.matrix_rank(A) < len(A):', '    raise ValueError("s")', 'return np.linalg.solve(A, b)']), 'test-1'],
  ['s9', 'cond > 1e12', sh(['if np.linalg.cond(A) > 1e12:', '    raise np.linalg.LinAlgError("s")', 'return np.linalg.solve(A, b)']), 'any'],
  ['s9', 'residual check allclose(A@x,b)', sh(['x = np.linalg.solve(A, b)', 'if not np.allclose(A @ x, b):', '    raise np.linalg.LinAlgError("s")', 'return x']), 'test-7'],
  ['i7', 'no normalise', mv(['if np.linalg.matrix_rank(S) < len(S):', '    raise np.linalg.LinAlgError("s")', 'return np.linalg.solve(S, ones)']), 'test-1'],
  ['i7', 'no rank check', mv(['z = np.linalg.solve(S, ones)', 'return z / z.sum()']), 'test-6'],
  ['i7', 'det == 0', mv(['if np.linalg.det(S) == 0:', '    raise np.linalg.LinAlgError("s")', 'z = np.linalg.solve(S, ones)', 'return z / z.sum()']), 'test-7'],
  ['i7', 'abs(det) < 1e-10', mv(['if abs(np.linalg.det(S)) < 1e-10:', '    raise np.linalg.LinAlgError("s")', 'z = np.linalg.solve(S, ones)', 'return z / z.sum()']), 'test-8'],
  ['i7', 'abs(det) < 1e-12', mv(['if abs(np.linalg.det(S)) < 1e-12:', '    raise np.linalg.LinAlgError("s")', 'z = np.linalg.solve(S, ones)', 'return z / z.sum()']), 'test-8'],
  ['i7', 'np.isclose(det,0)', mv(['if np.isclose(np.linalg.det(S), 0):', '    raise np.linalg.LinAlgError("s")', 'z = np.linalg.solve(S, ones)', 'return z / z.sum()']), 'test-8'],
  ['i7', 'nan check', mv(['z = np.linalg.solve(S, ones)', 'if not np.all(np.isfinite(z)):', '    raise np.linalg.LinAlgError("s")', 'return z / z.sum()']), 'any'],
  ['i7', 'inv with rank check', mv(['if np.linalg.matrix_rank(S) < len(S):', '    raise np.linalg.LinAlgError("s")', 'z = np.linalg.inv(S) @ ones', 'return z / z.sum()']), null],
  ['i7', 'inverse-variance weights', mv(['if np.linalg.matrix_rank(S) < len(S):', '    raise np.linalg.LinAlgError("s")', 'z = 1 / np.diag(S)', 'return z / z.sum()']), 'test-2'],
  ['i9', 'sequential bootstrap in listed order', cb('', ['d = []', 'for (c, m), p in zip(bonds, prices):', '    d.append((p - c * sum(d[:m - 1])) / (100 + c))', 'd = np.array(d)', 'vals = np.array([c * d[:m].sum() + 100 * d[m - 1] for c, m in targets])', 'return d, vals']), 'test-3'],
  ['i9', 'sort bonds, not prices', cb(rows, ['years = max(m for c, m in bonds)', 'C = cash_flow_rows(sorted(bonds, key=lambda b: b[1]), years)', 'if len(bonds) != years or np.linalg.matrix_rank(C) < years:', '    raise ValueError("x")', 'd = np.linalg.solve(C, np.array(prices, dtype=float))', 'return d, cash_flow_rows(targets, years) @ d']), 'test-5'],
  ['i9', 'no checks at all', cb(rowsNoCheck, ['years = max(m for c, m in bonds)', 'C = cash_flow_rows(bonds, years)', 'd = np.linalg.solve(C, np.array(prices, dtype=float))', 'return d, cash_flow_rows(targets, years) @ d']), 'test-8'],
  ['i9', 'len check + det == 0', cb(rows, ['years = max(m for c, m in bonds)', 'C = cash_flow_rows(bonds, years)', 'if len(bonds) != years or np.linalg.det(C) == 0:', '    raise ValueError("x")', 'd = np.linalg.solve(C, np.array(prices, dtype=float))', 'return d, cash_flow_rows(targets, years) @ d']), 'test-9'],
  ['i9', 'len check + nan check', cb(rows, ['years = max(m for c, m in bonds)', 'C = cash_flow_rows(bonds, years)', 'if len(bonds) != years:', '    raise ValueError("x")', 'd = np.linalg.solve(C, np.array(prices, dtype=float))', 'if not np.all(np.isfinite(d)):', '    raise ValueError("x")', 'return d, cash_flow_rows(targets, years) @ d']), 'test-9'],
  ['i9', 'len check + try/except LinAlgError', cb(rows, ['years = max(m for c, m in bonds)', 'C = cash_flow_rows(bonds, years)', 'if len(bonds) != years:', '    raise ValueError("x")', 'try:', '    d = np.linalg.solve(C, np.array(prices, dtype=float))', 'except np.linalg.LinAlgError:', '    raise ValueError("x")', 'return d, cash_flow_rows(targets, years) @ d']), 'test-8'],
  ['i9', 'rank check, no target-maturity check', cb(rowsNoCheck, ['years = max(m for c, m in bonds)', 'C = cash_flow_rows(bonds, years)', 'if len(bonds) != years or np.linalg.matrix_rank(C) < years:', '    raise ValueError("x")', 'd = np.linalg.solve(C, np.array(prices, dtype=float))', 'return d, cash_flow_rows(targets, years) @ d']), 'test-10'],
  ['i9', 'rank check, no len check, lstsq', cb(rows, ['years = max(m for c, m in bonds)', 'C = cash_flow_rows(bonds, years)', 'if np.linalg.matrix_rank(C) < years:', '    raise ValueError("x")', 'd = np.linalg.lstsq(C, np.array(prices, dtype=float), rcond=None)[0]', 'return d, cash_flow_rows(targets, years) @ d']), 'any'],
  ['i9', 'square check only (years from len), rank', cb(rows, ['years = len(bonds)', 'C = cash_flow_rows(bonds, years)', 'if np.linalg.matrix_rank(C) < years:', '    raise ValueError("x")', 'd = np.linalg.solve(C, np.array(prices, dtype=float))', 'return d, cash_flow_rows(targets, years) @ d']), 'any'],
  ['i9', 'uses inv', cb(rows, ['years = max(m for c, m in bonds)', 'C = cash_flow_rows(bonds, years)', 'if len(bonds) != years or np.linalg.matrix_rank(C) < years:', '    raise ValueError("x")', 'd = np.linalg.inv(C) @ np.array(prices, dtype=float)', 'return d, cash_flow_rows(targets, years) @ d']), 'test-12'],
  ['i9', 'coupon only at maturity', cb('', ['years = max(m for c, m in bonds)', 'C = np.zeros((len(bonds), years))', 'for i, (c, m) in enumerate(bonds):', '    C[i, m - 1] = 100 + c', 'if len(bonds) != years or np.linalg.matrix_rank(C) < years:', '    raise ValueError("x")', 'd = np.linalg.solve(C, np.array(prices, dtype=float))', 'return d, np.array([(100 + c) * d[m - 1] for c, m in targets])']), 'test-1'],
  ['i9', 'targets must be full length (no padding)', cb(rows, ['years = max(m for c, m in bonds)', 'C = cash_flow_rows(bonds, years)', 'if len(bonds) != years or np.linalg.matrix_rank(C) < years:', '    raise ValueError("x")', 'd = np.linalg.solve(C, np.array(prices, dtype=float))', 'return d, np.array([np.array([c] * (m - 1) + [100 + c]) @ d for c, m in targets])']), 'test-1'],
  ['i9', 'returns list for d only (no values)', cb(rows, ['years = max(m for c, m in bonds)', 'C = cash_flow_rows(bonds, years)', 'd = np.linalg.solve(C, np.array(prices, dtype=float))', 'return d, d']), 'test-2'],
];
// probes: expressions evaluated under the page's Pyodide
const probes = [
  'np.__version__', 'str(np.linalg.det(np.array([[2, 3], [1, 4]])))', 'repr(np.array([[0.50, 0.25], [0.20, 0.30]]) * np.array([225, 350]))', 'repr(np.array([[0.50, 0.25], [0.20, 0.30]]) @ np.array([225, 350]))',
  '(lambda H: "%.1e %.1e" % (np.abs(H @ np.linalg.solve(H, H @ np.ones(10)) - H @ np.ones(10)).max(), np.abs(H @ (np.linalg.inv(H) @ (H @ np.ones(10))) - H @ np.ones(10)).max()))(np.array([[1 / (i + j + 1) for j in range(10)] for i in range(10)]))',
  'repr(np.linalg.solve(np.array([[1., 2], [2, 4]]), np.array([1., 2])))', 'repr(np.linalg.solve(np.array([[1., 2], [2, 4]]), np.array([3., 6])))',
  'repr(np.linalg.solve(np.array([[0.50, 0.25, 0.75], [0.20, 0.30, 0.50], [0.04, 0.02, 0.06]]), np.array([235., 140, 19])))',
  'repr(np.linalg.solve(np.array([[0.50, 0.60], [0.20, 0.24]]), np.array([200., 150])))',
  'repr(np.linalg.solve(np.array([[0.0625, 0.0625], [0.0625, 0.0625]]), np.ones(2)))', 'repr(np.linalg.solve(np.array([[0.04, 0.06], [0.06, 0.09]]), np.ones(2)))',
  'repr([np.linalg.det(np.array(m)) for m in ([[0.50, 0.25, 0.75], [0.20, 0.30, 0.50], [0.04, 0.02, 0.06]], [[0.50, 0.60], [0.20, 0.24]], [[0.04, 0.06], [0.06, 0.09]], [[1., 2], [2, 4]], [[2.1, 2.1, 102.1], [3.3, 3.3, 103.3], [4.7, 4.7, 104.7]], [[102., 0, 0], [105, 0, 0], [4, 4, 104]])])',
  'repr([int(np.linalg.matrix_rank(np.array(m))) for m in ([[0.50, 0.25, 0.75], [0.20, 0.30, 0.50], [0.04, 0.02, 0.06]], [[0.50, 0.60], [0.20, 0.24]], [[12., 8], [3, 2]], [[0.50, 0.25], [0.20, 0.30]], [[2.1, 2.1, 102.1], [3.3, 3.3, 103.3], [4.7, 4.7, 104.7]])])',
  'repr(np.linalg.solve(np.array([[2.1, 2.1, 102.1], [3.3, 3.3, 103.3], [4.7, 4.7, 104.7]]), np.array([94.859, 98.207, 102.113])))',
  'repr(np.linalg.solve(np.array([[102., 0, 0], [105, 0, 0], [4, 4, 104]]), np.array([98.94, 101.85, 100.16])))',
  'repr((np.linalg.inv(np.array([[2., 3], [1, 4]])) @ np.array([[2., 3], [1, 4]])).tolist())',
  'repr(float(np.linalg.det(np.array([[0.50, 0.25, 0.60], [0.20, 0.30, 0.10], [0.04, 0.02, 0.05]]) * 1e-4)))',
  '(lambda v, C: repr(float(np.linalg.det(np.outer(v, v) * C))))(np.array([0.01, 0.012, 0.015, 0.02]), np.full((4, 4), 0.3) + 0.7 * np.eye(4))',
  'repr(np.linalg.inv(np.array([[1., 2], [2, 4]])))',
];
const out = [];
const pspec = { language: 'python', tests: probes.map((p) => ({ call: p, expect: '"zz"' })) };
const pr = await runner.grade(pspec, 'import numpy as np\n', 'tests');
out.push('== probes under Pyodide (error: ' + pr.error + ')');
pr.rows.forEach((r, i) => out.push(`P${i}: ${probes[i].slice(0, 70)} -> ${r.actual} ${r.error ? '[' + String(r.error).split('\n').pop() + ']' : ''}`));
for (const k of Object.keys(W)) { const r = await runner.grade(W[k], W[k].solution, 'tests'); const s = await runner.grade(W[k], W[k].starter, 'tests'); out.push(`== ${k}: solution ${r.ok ? 'passes' : 'FAILS ' + r.key}; starter key ${s.key}`); }
let bad = 0;
const res = await Promise.all(M.map(([k, name, src]) => runner.grade(W[k], src, 'tests')));
M.forEach(([k, name, src, want], i) => {
  const r = res[i], got = r.ok ? null : r.key;
  const first = r.rows.find((x) => !x.ok);
  const okk = want === 'any' ? true : got === want;
  if (!okk) bad++;
  out.push(`${okk ? 'ok ' : 'DIFF'} ${k} | ${name} | got ${got} want ${want} | ${first ? 'actual=' + String(first.actual).slice(0, 80) + ' err=' + String(first.error || r.error || '').split('\n').pop().slice(0, 90) : (r.error ? String(r.error).split('\n').pop().slice(0, 100) : '')}`);
});
out.push('differences from the expectation: ' + bad);
// the fixes proposed in findings 3 and 4 are now hidden tests 7 and 8 of s2 and test 7 of s9 (fix pass); the rows above cover them
console.log(out.join('\n'));
await runner.close();
