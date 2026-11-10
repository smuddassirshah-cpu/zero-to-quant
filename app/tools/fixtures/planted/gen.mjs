// Writes the four fixture drills (planted-py-caught, planted-py-missed, planted-cpp-caught, planted-cpp-missed) beside this file.
// They are generated once and committed; run `node tools/fixtures/planted/gen.mjs` from app/ only to change them.
import fs from 'node:fs';
const py = (id, planted) => ({
  id, sample: true, name: 'Planted fixture (Python)', course: 'py-found', skills: ['pf-functions'], difficulty: 2,
  brief: 'Write `clamp(x, lo, hi)`. It returns `lo` if `x` is below it, `hi` if `x` is above it, and `x` otherwise.',
  starter: 'def clamp(x, lo, hi):\n    return x\n',
  examples: [{ call: 'clamp(5, 0, 3)', expect: '3', compare: 'isclose' }],
  tests: [['clamp(5, 0, 3)', 3], ['clamp(-1, 0, 3)', 0], ['clamp(2, 0, 3)', 2], ['clamp(3, 0, 3)', 3]].map(([c, e]) => ({ call: c, expect: String(e), compare: 'isclose' })),
  how: 'Submit runs 4 hidden tests. Each answer is accepted when it is close to the expected value.',
  solution: 'def clamp(x, lo, hi):\n    return max(lo, min(x, hi))\n', planted });
const cpp = (id, planted) => ({
  id, sample: true, name: 'Planted fixture (C++)', course: 'cpp', skills: ['cp-stl'], difficulty: 2, language: 'cpp', pattern: 'simulation',
  brief: 'Write `clamp_int(x, lo, hi)`. It returns `lo` if `x` is below it, `hi` if `x` is above it, and `x` otherwise.',
  starter: '// Return x limited to the range lo to hi.\nint clamp_int(int x, int lo, int hi) {\n    return x;\n}\n',
  examples: [{ name: 'Above', call: 'clamp_int', args: [5, 0, 3], expect: 3, compare: 'equal' }],
  tests: [[5, 0, 3, 3], [-1, 0, 3, 0], [2, 0, 3, 2], [3, 0, 3, 3]].map(([x, l, h, e]) => ({ name: `clamp ${x}`, call: 'clamp_int', args: [x, l, h], expect: e, compare: 'equal' })),
  how: 'Submit runs 4 hidden tests.',
  solution: 'int clamp_int(int x, int lo, int hi) {\n    return x < lo ? lo : (x > hi ? hi : x);\n}\n', planted });
const w = (d) => fs.writeFileSync(new URL(`./${d.id}.json`, import.meta.url), JSON.stringify(d, null, 2) + '\n');
w(py('planted-py-caught', [{ code: 'def clamp(x, lo, hi):\n    return min(x, hi)\n', slip: 'Ignores the lower bound.' }]));
w(py('planted-py-missed', [{ code: 'def clamp(x, lo, hi):\n    return min(hi, max(lo, x))\n', slip: 'Applies the bounds in the other order, which differs only when lo is above hi.' }]));
w(cpp('planted-cpp-caught', [{ code: 'int clamp_int(int x, int lo, int hi) {\n    return x > hi ? hi : x;\n}\n', slip: 'Ignores the lower bound.' }]));
w(cpp('planted-cpp-missed', [{ code: 'int clamp_int(int x, int lo, int hi) {\n    return x > hi ? hi : (x < lo ? lo : x);\n}\n', slip: 'Tests the upper bound first, which differs only when lo is above hi.' }]));
