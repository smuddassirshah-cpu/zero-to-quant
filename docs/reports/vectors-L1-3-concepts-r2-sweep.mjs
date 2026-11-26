// Audit vectors-1-3-r2: sweep of the Python widgets of l12-numpy-matrices and homework-3 under the page's Pyodide 0.27.7
// (app/tools/code-runner.mjs, the page's own grader in a node worker). For each byKey test-N line it submits natural codings
// of the named mistake and records the first failing test; it re-runs every `mutants` entry; it probes the floating-point
// values the content quotes. Exit 0 when every program lands where the audit recorded and no wrong program passes every
// test; exit 1 while finding 1 or 6 is open (rows marked FAILS expected, PASSES ALL got).
// usage: node docs/reports/vectors-L1-3-concepts-r2-sweep.mjs <repo-root> <pkgs>
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
const [ROOT, PKGS] = process.argv.slice(2);
const APP = path.join(ROOT, 'app');
const { makeRunner } = await import(pathToFileURL(path.join(APP, 'tools/code-runner.mjs')).href);
const runner = makeRunner({ pkgs: PKGS, root: APP, jobs: 2 });
const H = JSON.parse(fs.readFileSync(path.join(APP, 'content/courses/vectors/homework-3.json'), 'utf8'));
const L = JSON.parse(fs.readFileSync(path.join(APP, 'content/courses/vectors/l12-numpy-matrices.json'), 'utf8'));
const hd = 'import numpy as np\n\n';
const f = (name, args, pre, body) => `${hd}def ${name}(${args}):\n${pre}${body.split('\n').map((l) => '    ' + l).join('\n')}\n`;
const preAx = '    A = np.array(A, dtype=float)\n    x = np.array(x, dtype=float)\n';
const preAB = '    A = np.array(A, dtype=float)\n    B = np.array(B, dtype=float)\n    n = len(A)\n';
const preAb = '    A = np.array(A, dtype=float)\n    b = np.array(b, dtype=float)\n';
const preG = '    A = np.array(greeks, dtype=float)\n    b = np.array(target, dtype=float)\n';
const cands = {
  0: [
    ['A * x', f('hedge_greeks', 'A, x', preAx, 'return A * x'), 'test-1'],
    ['x @ A', f('hedge_greeks', 'A, x', preAx, 'return x @ A'), 'test-1'],
    ['A.T @ x', f('hedge_greeks', 'A, x', preAx, 'return A.T @ x'), 'test-1'],
    ['(A*x).sum(axis=0)', f('hedge_greeks', 'A, x', preAx, 'return (A * x).sum(axis=0)'), 'test-1'],
    ['np.dot (right)', f('hedge_greeks', 'A, x', preAx, 'return np.dot(A, x)'), null],
    ['syntax error', hd + 'def hedge_greeks(A, x):\n    return A @@ x\n', 'error'],
    ['starter', L.screens[0].widget.starter, '?'],
  ],
  2: [
    ['return True', f('is_inverse', 'A, B', preAB, 'return True'), 'test-2'],
    ['off-diagonal only', f('is_inverse', 'A, B', preAB, 'P = B @ A\nreturn np.allclose(P - np.diag(np.diag(P)), 0)'), 'test-2'],
    ['det(BA) close to 1', f('is_inverse', 'A, B', preAB, 'return bool(np.isclose(np.linalg.det(B @ A), 1))'), '?'],
    ['B == hand formula 2x2', f('is_inverse', 'A, B', preAB, 'd = A[0,0]*A[1,1]-A[0,1]*A[1,0]\nreturn bool((B == np.array([[A[1,1], -A[0,1]], [-A[1,0], A[0,0]]]) / d).all())'), '?'],
    ['FINDING 1: (B == np.linalg.inv(A)).all()', f('is_inverse', 'A, B', preAB, 'return bool((B == np.linalg.inv(A)).all())'), 'FAILS'],
    ['FINDING 1: np.array_equal(B, np.linalg.inv(A))', f('is_inverse', 'A, B', preAB, 'return np.array_equal(B, np.linalg.inv(A))'), 'FAILS'],
    ['allclose(B, inv(A))', f('is_inverse', 'A, B', preAB, 'return np.allclose(B, np.linalg.inv(A))'), null],
    ['allclose(A@B, I)', f('is_inverse', 'A, B', preAB, 'return np.allclose(A @ B, np.eye(n))'), null],
    ['allclose atol=0 rtol=0', f('is_inverse', 'A, B', preAB, 'return np.allclose(B @ A, np.eye(n), rtol=0, atol=0)'), 'test-6'],
    ['abs diff sum == 0', f('is_inverse', 'A, B', preAB, 'return bool(np.abs(B @ A - np.eye(n)).sum() == 0)'), 'test-6'],
    ['np.eye(2) hard-coded', f('is_inverse', 'A, B', preAB, 'return np.allclose(B @ A, np.eye(2))'), '?'],
    ['allclose atol=0.1 (loose)', f('is_inverse', 'A, B', preAB, 'return np.allclose(B @ A, np.eye(n), atol=0.1)'), '?'],
    ['round 6 == I', f('is_inverse', 'A, B', preAB, 'return bool((np.round(B @ A, 6) == np.eye(n)).all())'), null],
    ['starter', L.screens[2].widget.starter, '?'],
  ],
  3: [
    ['solve(b, A)', f('solve_system', 'A, b', preAb, 'return np.linalg.solve(b, A)'), 'test-1'],
    ['inv(A) @ b', f('solve_system', 'A, b', preAb, 'return np.linalg.inv(A) @ b'), null],
    ['A @ b', f('solve_system', 'A, b', preAb, 'return A @ b'), 'test-1'],
    ['b / A', f('solve_system', 'A, b', preAb, 'return b / A'), 'test-1'],
    ['inv(A) * b', f('solve_system', 'A, b', preAb, 'return np.linalg.inv(A) * b'), 'test-1'],
    ['b @ inv(A)', f('solve_system', 'A, b', preAb, 'return b @ np.linalg.inv(A)'), 'test-1'],
    ['2x2 hand formula', f('solve_system', 'A, b', preAb, 'd = A[0,0]*A[1,1]-A[0,1]*A[1,0]\nreturn np.array([A[1,1]*b[0]-A[0,1]*b[1], -A[1,0]*b[0]+A[0,0]*b[1]])/d'), 'test-5'],
    ['starter', L.screens[3].widget.starter, '?'],
  ],
  8: [
    ['inv(A) @ b', f('three_way_hedge', 'greeks, target', preG, 'return np.linalg.inv(A) @ b'), null],
    ['A @ b', f('three_way_hedge', 'greeks, target', preG, 'return A @ b'), 'test-1'],
    ['solve(A.T, b)', f('three_way_hedge', 'greeks, target', preG, 'return np.linalg.solve(A.T, b)'), 'test-1'],
    ['b @ inv(A)', f('three_way_hedge', 'greeks, target', preG, 'return b @ np.linalg.inv(A)'), 'test-1'],
    ['clip negatives to 0', f('three_way_hedge', 'greeks, target', preG, 'return np.maximum(np.linalg.solve(A, b), 0)'), 'test-2'],
    ['abs()', f('three_way_hedge', 'greeks, target', preG, 'return np.abs(np.linalg.solve(A, b))'), 'test-2'],
    ['round to whole options', f('three_way_hedge', 'greeks, target', preG, 'return np.round(np.linalg.solve(A, b))'), null],
    ['cap at 1000', f('three_way_hedge', 'greeks, target', preG, 'return np.clip(np.linalg.solve(A, b), -1000, 1000)'), 'test-3'],
    ['3x3 only (reshape)', f('three_way_hedge', 'greeks, target', preG, 'return np.linalg.solve(A.reshape(3, 3), b)'), 'test-5'],
    ['starter', L.screens[8].widget.starter, '?'],
  ],
  9: [
    ['starter', L.screens[9].widget.starter, 'test-1'],
    ['no check (solve only)', f('safe_hedge', 'greeks, target', preG, 'return np.linalg.solve(A, b)'), 'test-1'],
    ['rank < len(A) but return not raise', f('safe_hedge', 'greeks, target', preG, 'if np.linalg.matrix_rank(A) < len(A):\n    return None\nreturn np.linalg.solve(A, b)'), 'test-1'],
    ['rank < 3 hard-coded', f('safe_hedge', 'greeks, target', preG, 'if np.linalg.matrix_rank(A) < 3:\n    raise np.linalg.LinAlgError("s")\nreturn np.linalg.solve(A, b)'), '?'],
    ['rank < 2 hard-coded', f('safe_hedge', 'greeks, target', preG, 'if np.linalg.matrix_rank(A) < 2:\n    raise np.linalg.LinAlgError("s")\nreturn np.linalg.solve(A, b)'), '?'],
    ['always raise', f('safe_hedge', 'greeks, target', preG, 'raise np.linalg.LinAlgError("s")'), 'test-4'],
    ['rank <= len(A)', f('safe_hedge', 'greeks, target', preG, 'if np.linalg.matrix_rank(A) <= len(A):\n    raise np.linalg.LinAlgError("s")\nreturn np.linalg.solve(A, b)'), 'test-4'],
    ['abs(det) < 1e-10', f('safe_hedge', 'greeks, target', preG, 'if abs(np.linalg.det(A)) < 1e-10:\n    raise np.linalg.LinAlgError("s")\nreturn np.linalg.solve(A, b)'), 'test-6'],
    ['np.isclose(det, 0)', f('safe_hedge', 'greeks, target', preG, 'if np.isclose(np.linalg.det(A), 0):\n    raise np.linalg.LinAlgError("s")\nreturn np.linalg.solve(A, b)'), 'test-6'],
    ['abs(det) < 1e-12', f('safe_hedge', 'greeks, target', preG, 'if abs(np.linalg.det(A)) < 1e-12:\n    raise np.linalg.LinAlgError("s")\nreturn np.linalg.solve(A, b)'), 'test-6'],
    ['round(det, 10) == 0', f('safe_hedge', 'greeks, target', preG, 'if round(np.linalg.det(A), 10) == 0:\n    raise np.linalg.LinAlgError("s")\nreturn np.linalg.solve(A, b)'), 'test-6'],
    ['det == 0', f('safe_hedge', 'greeks, target', preG, 'if np.linalg.det(A) == 0:\n    raise np.linalg.LinAlgError("s")\nreturn np.linalg.solve(A, b)'), 'test-7'],
    ['FINDING 6 (same gap): hand ad - bc == 0 for 2 by 2, np det otherwise', f('safe_hedge', 'greeks, target', preG, 'd = A[0,0]*A[1,1]-A[0,1]*A[1,0] if len(A) == 2 else np.linalg.det(A)\nif d == 0:\n    raise np.linalg.LinAlgError("s")\nreturn np.linalg.solve(A, b)'), '?'],
    ['isnan after solve', f('safe_hedge', 'greeks, target', preG, 'x = np.linalg.solve(A, b)\nif np.isnan(x).any():\n    raise np.linalg.LinAlgError("s")\nreturn x'), 'test-7'],
    ['cond > 1e12', f('safe_hedge', 'greeks, target', preG, 'if np.linalg.cond(A) > 1e12:\n    raise np.linalg.LinAlgError("s")\nreturn np.linalg.solve(A, b)'), null],
    ['rank < A.shape[1]', f('safe_hedge', 'greeks, target', preG, 'if np.linalg.matrix_rank(A) < A.shape[1]:\n    raise np.linalg.LinAlgError("s")\nreturn np.linalg.solve(A, b)'), null],
    ['raise ValueError', f('safe_hedge', 'greeks, target', preG, 'if np.linalg.matrix_rank(A) < len(A):\n    raise ValueError("s")\nreturn np.linalg.solve(A, b)'), 'test-1'],
    ['try/except around solve', f('safe_hedge', 'greeks, target', preG, 'try:\n    x = np.linalg.solve(A, b)\nexcept Exception:\n    raise np.linalg.LinAlgError("s")\nreturn x'), 'test-1'],
  ],
};
let bad = 0; const out = [];
for (const [si, list] of Object.entries(cands)) {
  const spec = L.screens[si].widget;
  for (const [label, src, expect] of list) {
    const r = await runner.grade(spec, src, 'tests');
    const got = r.ok ? null : r.key;
    const fl = expect === '?' ? 'probe' : expect === 'FAILS' ? (got ? 'as expected' : 'DIFFERS: PASSES ALL') : (got === expect ? 'as expected' : 'DIFFERS');
    if (fl.startsWith('DIFFERS')) bad++;
    const firstRow = r.rows.find((x) => !x.ok);
    out.push(`s${si} | ${label} | first key ${got} | expected ${expect} | ${fl}${firstRow ? ' | ' + String(firstRow.error || firstRow.actual || '').split('\n').pop().slice(0, 90) : ''}${r.error ? ' | ERR ' + String(r.error).split('\n').pop().slice(0, 80) : ''}`);
  }
  for (const [i, m] of (spec.mutants || []).entries()) {
    const r = await runner.grade(spec, m.source, 'tests');
    const got = r.ok ? null : r.key;
    if (got !== `test-${m.test}`) bad++;
    out.push(`s${si} | mutants[${i}] | first key ${got} | named test-${m.test} | ${got === `test-${m.test}` ? 'as expected' : 'DIFFERS'}`);
  }
}

// homework-3 h-min-var and h-bond-curve
const ind = (b) => b.split('\n').map((l) => '    ' + l).join('\n') + '\n';
const mv = H.items.find((x) => x.id === 'h-min-var').widget;
const pm = hd + 'def min_var_weights(cov):\n    S = np.array(cov, dtype=float)\n    ones = np.ones(len(S))\n';
const chk = 'if np.linalg.matrix_rank(S) < len(S):\n    raise np.linalg.LinAlgError("s")\n';
const mvs = [
  ['no normalise', chk + 'return np.linalg.solve(S, ones)', 'test-1'],
  ['inverse-vol weights', 'z = 1 / np.sqrt(np.diag(S))\nreturn z / z.sum()', 'test-1'],
  ['equal weights', 'return ones / len(S)', 'test-1'],
  ['S @ ones (no inverse)', chk + 'z = S @ ones\nreturn z / z.sum()', 'test-1'],
  ['inverse-variance (diagonal only)', 'z = 1 / np.diag(S)\nreturn z / z.sum()', 'test-2'],
  ['no singular check', 'z = np.linalg.solve(S, ones)\nreturn z / z.sum()', 'test-6'],
  ['raise ValueError', 'if np.linalg.matrix_rank(S) < len(S):\n    raise ValueError("s")\nz = np.linalg.solve(S, ones)\nreturn z / z.sum()', 'test-6'],
  ['np.linalg.det(S) == 0', 'if np.linalg.det(S) == 0:\n    raise np.linalg.LinAlgError("s")\nz = np.linalg.solve(S, ones)\nreturn z / z.sum()', 'test-7'],
  ['isnan after solve', 'z = np.linalg.solve(S, ones)\nif np.isnan(z).any():\n    raise np.linalg.LinAlgError("s")\nreturn z / z.sum()', 'test-7'],
  ['abs(det) < 1e-12', 'if abs(np.linalg.det(S)) < 1e-12:\n    raise np.linalg.LinAlgError("s")\nz = np.linalg.solve(S, ones)\nreturn z / z.sum()', 'test-8'],
  ['np.isclose(det, 0)', 'if np.isclose(np.linalg.det(S), 0):\n    raise np.linalg.LinAlgError("s")\nz = np.linalg.solve(S, ones)\nreturn z / z.sum()', 'test-8'],
  ['inv(S) @ ones with the rank check (sound)', chk + 'z = np.linalg.inv(S) @ ones\nreturn z / z.sum()', null],
  ['FINDING 6: hand ad - bc == 0', 'if S[0,0]*S[1,1] - S[0,1]*S[1,0] == 0:\n    raise np.linalg.LinAlgError("s")\nz = np.linalg.solve(S, ones)\nreturn z / z.sum()', 'FAILS'],
];
for (const [label, body, expect] of mvs) {
  const r = await runner.grade(mv, pm + ind(body), 'tests'); const got = r.ok ? null : r.key;
  const fl = expect === 'FAILS' ? (got ? 'as expected' : 'DIFFERS: PASSES ALL') : (got === expect ? 'as expected' : 'DIFFERS');
  if (fl !== 'as expected') bad++;
  out.push(`hw3 h-min-var | ${label} | first key ${got} | expected ${expect} | ${fl}`);
}
const bc = H.items.find((x) => x.id === 'h-bond-curve').widget;
const rows = 'def rows(bonds, years):\n    C = np.zeros((len(bonds), years))\n    for i, (c, m) in enumerate(bonds):\n        if m > years:\n            raise ValueError("late")\n        C[i, :m] = c\n        C[i, m - 1] += 100\n    return C\n\n';
const head = 'def curve_from_bonds(bonds, prices, targets):\n    years = max(m for c, m in bonds)\n    C = rows(bonds, years)\n';
const boot = (order) => hd + 'def curve_from_bonds(bonds, prices, targets):\n    years = max(m for c, m in bonds)\n    if len(bonds) != years:\n        raise ValueError("n")\n    d = np.zeros(years)\n    for (c, m), p in ' + order + ':\n        d[m - 1] = (p - c * d[:m - 1].sum()) / (100 + c)\n    vals = []\n    for c, m in targets:\n        if m > years:\n            raise ValueError("late")\n        vals.append(c * d[:m].sum() + 100 * d[m - 1])\n    return d, np.array(vals)\n';
const bcs = [
  ['count check only, then solve', hd + rows + head + ind('if len(bonds) != years:\n    raise ValueError("n")\nd = np.linalg.solve(C, np.array(prices, dtype=float))\nreturn d, rows(targets, years) @ d'), 'test-8'],
  ['try/except LinAlgError', hd + rows + head + ind('if len(bonds) != years:\n    raise ValueError("n")\ntry:\n    d = np.linalg.solve(C, np.array(prices, dtype=float))\nexcept np.linalg.LinAlgError:\n    raise ValueError("n")\nreturn d, rows(targets, years) @ d'), 'test-8'],
  ['np.linalg.det(C) == 0', hd + rows + head + ind('if len(bonds) != years or np.linalg.det(C) == 0:\n    raise ValueError("n")\nd = np.linalg.solve(C, np.array(prices, dtype=float))\nreturn d, rows(targets, years) @ d'), 'test-9'],
  ['isnan after solve', hd + rows + head + ind('if len(bonds) != years:\n    raise ValueError("n")\nd = np.linalg.solve(C, np.array(prices, dtype=float))\nif np.isnan(d).any():\n    raise ValueError("n")\nreturn d, rows(targets, years) @ d'), 'test-9'],
  ['inv(C) @ p', hd + rows + head + ind('if len(bonds) != years or np.linalg.matrix_rank(C) < years:\n    raise ValueError("n")\nd = np.linalg.inv(C) @ np.array(prices, dtype=float)\nreturn d, rows(targets, years) @ d'), 'test-12'],
  ['bootstrap in maturity order', boot('sorted(zip(bonds, prices), key=lambda t: t[0][1])'), 'test-3'],
  ['bootstrap in list order', boot('zip(bonds, prices)'), 'test-3'],
  ['targets priced without padding', hd + rows + head + ind('if len(bonds) != years or np.linalg.matrix_rank(C) < years:\n    raise ValueError("n")\nd = np.linalg.solve(C, np.array(prices, dtype=float))\nreturn d, np.array([c * d[:m].sum() + 100 * d[m - 1] for c, m in targets])'), 'test-10'],
  ['lstsq with its rank (sound)', hd + rows + head + ind('d, res, rk, sv = np.linalg.lstsq(C, np.array(prices, dtype=float), rcond=None)\nif len(bonds) != years or rk < years:\n    raise ValueError("n")\nreturn d, rows(targets, years) @ d'), null],
];
for (const [label, src, expect] of bcs) {
  const r = await runner.grade(bc, src, 'tests'); const got = r.ok ? null : r.key;
  if (got !== expect) bad++;
  out.push(`hw3 h-bond-curve | ${label} | first key ${got} | expected ${expect} | ${got === expect ? 'as expected' : 'DIFFERS'}`);
}
// numeric probes under Pyodide
const probe = { tests: [
  { call: 'repr(np.linalg.det(np.array([[2, 3], [1, 4]])))', expect: "'x'" },
  { call: 'repr(np.linalg.det(np.array([[0.04, 0.06], [0.06, 0.09]])))', expect: "'x'" },
  { call: 'repr(np.linalg.solve(np.array([[0.04, 0.06], [0.06, 0.09]]), np.array([1.0, 1.0])).tolist())', expect: "'x'" },
  { call: 'repr(np.linalg.det(np.array([[0.50, 0.25, 0.75], [0.20, 0.30, 0.50], [0.04, 0.02, 0.06]])))', expect: "'x'" },
  { call: 'repr(np.linalg.solve(np.array([[0.50, 0.25, 0.75], [0.20, 0.30, 0.50], [0.04, 0.02, 0.06]]), np.array([235.0, 140.0, 19.0])).tolist())', expect: "'x'" },
  { call: 'repr(np.linalg.solve(np.array([[1, 2], [2, 4]]), np.array([1, 2])).tolist())', expect: "'x'" },
  { call: 'repr(np.linalg.solve(np.array([[1.0, 2], [2, 4]]), np.array([3.0, 6])).tolist())', expect: "'x'" },
  { call: 'repr(np.linalg.solve(np.array([[0.50, 0.60], [0.20, 0.24]]), np.array([200.0, 150])).tolist())', expect: "'x'" },
  { call: 'repr(np.linalg.det(np.array([[0.50, 0.25, 0.60], [0.20, 0.30, 0.10], [0.04, 0.02, 0.05]]) * 1e-4))', expect: "'x'" },
  { call: 'repr(hil())', expect: "'x'" },
  { call: 'repr((np.linalg.inv(np.array([[2.0, 3], [1, 4]])) @ np.array([[2.0, 3], [1, 4]])).tolist())', expect: "'x'" },
  { call: 'repr((np.linalg.inv(G3) @ G3).tolist())', expect: "'x'" },
  { call: 'repr(np.__version__)', expect: "'x'" },
  { call: 'repr([np.linalg.matrix_rank(np.array([[0.04, 0.06], [0.06, 0.09]])), np.linalg.matrix_rank(G3 * 1e-4), np.linalg.cond(np.array([[0.04, 0.06], [0.06, 0.09]]))])', expect: "'x'" },
] };
const psrc = hd + 'G3 = np.array([[0.50, 0.25, 0.60], [0.20, 0.30, 0.10], [0.04, 0.02, 0.05]])\ndef hil():\n    n = 10\n    H = np.array([[1 / (i + j + 1) for j in range(n)] for i in range(n)])\n    b = H @ np.ones(n)\n    x1 = np.linalg.solve(H, b)\n    x2 = np.linalg.inv(H) @ b\n    return [float(np.abs(H @ x1 - b).max()), float(np.abs(H @ x2 - b).max()), float(np.abs(x1 - 1).max()), float(np.abs(x2 - 1).max())]\n';
const pr = await runner.grade(probe, psrc, 'tests');
pr.rows.forEach((r, i) => out.push(`probe ${i} | ${probe.tests[i].call.slice(0, 70)} | ${r.actual || r.error}`));
console.log(out.join('\n'));
console.log(`sweep: ${bad} differ from expectation`);
await runner.close();
process.exit(bad ? 1 : 0);
