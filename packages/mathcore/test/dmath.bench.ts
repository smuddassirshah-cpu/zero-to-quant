// dmath's speed against the engine's own Math, for docs/WIDGETS.md 9.2 item 5. A plain script rather than a
// vitest bench, which fails under the projects config of vitest.config.ts [measured]. It reads only the
// `performance` and `console` globals, so Node runs it as it stands and a browser page can import it (run so
// in Chromium 1194 through a scratch browser test [measured]):
//
//     node packages/mathcore/test/dmath.bench.ts
//
// Each row is the median, over 31 rounds, of the mean time a call takes over 4,096 inputs spread across the
// function's working range, run 20 times a round after a warm-up of the same size.
import { cos, exp, expm1, log, log1p, pow, sin, tanh } from '@zq/mathcore/dmath';

type Unary = (x: number) => number;

const N = 4096;
const spread = (lo: number, hi: number): Float64Array =>
  Float64Array.from({ length: N }, (_, i) => lo + ((hi - lo) * i) / N);

const index = Float64Array.from({ length: N }, (_, i) => i);
const exponents = spread(-30, 30);

const rows: readonly (readonly [string, Float64Array, Unary, Unary])[] = [
  ['exp', spread(-700, 700), exp, Math.exp],
  ['log', spread(1e-3, 1e6), log, Math.log],
  ['log1p', spread(-0.999, 100), log1p, Math.log1p],
  ['expm1', spread(-40, 40), expm1, Math.expm1],
  ['tanh', spread(-25, 25), tanh, Math.tanh],
  ['sin', spread(-1e6, 1e6), sin, Math.sin],
  ['cos', spread(-1e6, 1e6), cos, Math.cos],
  ['sin, |x| >= 1e10', spread(1e10, 1e300), sin, Math.sin],
  // pow over bases in [1.5, 8.5) and exponents in [-30, 30), both read from the input's index.
  [
    'pow',
    index,
    (i) => pow(1.5 + (i % 7), exponents[(i * 97) % N] ?? 0),
    (i) => Math.pow(1.5 + (i % 7), exponents[(i * 97) % N] ?? 0),
  ],
];

let sink = 0;

function nsPerCall(f: Unary, xs: Float64Array): number {
  const samples: number[] = [];
  for (let round = 0; round < 31; round++) {
    const t0 = performance.now();
    for (let rep = 0; rep < 20; rep++) for (const x of xs) sink += f(x);
    samples.push(((performance.now() - t0) * 1e6) / (20 * xs.length));
  }
  return samples.sort((a, b) => a - b)[15] ?? NaN;
}

for (const [, xs, f, g] of rows) {
  nsPerCall(f, xs);
  nsPerCall(g, xs);
}
for (const [name, xs, f, g] of rows) {
  const ours = nsPerCall(f, xs);
  const engine = nsPerCall(g, xs);
  console.log(
    `${name.padEnd(17)} dmath ${ours.toFixed(1).padStart(6)} ns   Math ${engine.toFixed(1).padStart(6)} ns   ` +
      `ratio ${(ours / engine).toFixed(2)}`,
  );
}
// Printing the sum keeps every call live.
console.log(`checksum ${String(sink)}`);
