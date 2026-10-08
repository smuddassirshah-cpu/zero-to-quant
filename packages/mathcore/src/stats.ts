// Basic statistics for shown and graded numbers (docs/PLAN.md 11.3 row 3; ARCHITECTURE.md 4.3). Decision notes:
// - Sums are exactly rounded: Shewchuk's partials with the half-even correction of CPython's math.fsum, so
//   `mean` is fsum(xs) / n, as statistics.fmean, kept inside [min, max]: the two roundings can leave it
//   (fmean gives 0.10000000000000002 for three 0.1s [measured, CPython 3.12.15]). Partials never
//   overlap, so there are at most about 40 of them [inferred: 2,098 exponent bits over 53-bit windows], and a
//   sum is O(n). An empty sum is 0; every other statistic needs data.
// - Variance is two-pass: the mean m, then the exactly rounded sums of d = x - m and of d², corrected to
//   Σd² - (Σd)²/n, the corrected two-pass algorithm [recalled: Chan, Golub and LeVeque, The American
//   Statistician 37(3), 1983]. The correction removes the error the rounded mean leaves: on 2,000 random sets
//   offset by up to 1e15 the plain two passes erred by up to 100% and the corrected ones by at most 1 ulp
//   [measured, 8 October 2026]; on the goldens the variance is within 2 ulp of statistics.variance and `sd`
//   within 1 of statistics.stdev [measured]. Rejected: Welford's update, which rounds at every step; Σx² -
//   (Σx)²/n, which cancels catastrophically. Data beyond 2^±400 is first scaled by 2^∓600, exact both ways, so
//   no square overflows or underflows: a variance throws only when it overflows itself, and `sd` keeps the
//   deviation of subnormal data, as statistics.stdev does. ECMA-262 makes Math.sqrt correctly rounded
//   (sec-math.sqrt) [sourced].
// - Quantiles sort a copy, O(n log n) (selection would save little at these sizes), and interpolate between
//   neighbours at a 0-based position h: 'inclusive' h = (n - 1)p, NumPy's default 'linear' and
//   statistics.quantiles(method="inclusive"); 'gcse' h = (n + 1)p - 1, the GCSE convention of
//   docs/curriculum/stage0-precalc-computing.md C5 (drill drl.pre.summary-stats). Where h falls outside
//   [0, n - 1] the result is the end value [our choice]; statistics.quantiles(method="exclusive") extrapolates
//   there [measured: CPython 3.12.15 gives 0.75 as the lower quartile of [1, 2]].
// - `lerp` is NumPy's _lerp: a + t(b - a) below t = 0.5 and b - (1 - t)(b - a) from it, exact at both ends
//   [measured: NumPy 2.4.6 source], so 'inclusive' is bit-identical to numpy.quantile on the goldens.
// - Errors are RangeErrors: too little data, a NaN or infinite value, p outside [0, 1], an overflowing sum.
export type VarianceKind = 'sample' | 'population';
export type QuantileMethod = 'inclusive' | 'gcse';
/** An array or a typed array of values. */
export type Data = ArrayLike<number> & Iterable<number>;

/** Adds x to Shewchuk's partials: non-overlapping, increasing in magnitude, summing exactly to every x added. */
function addPartial(ps: number[], value: number): void {
  let x = value;
  let i = 0;
  for (let y of ps) {
    if (Math.abs(x) < Math.abs(y)) {
      const t = x;
      x = y;
      y = t;
    }
    const hi = x + y;
    const lo = y - (hi - x);
    if (lo !== 0) ps[i++] = lo;
    x = hi;
  }
  if (!Number.isFinite(x)) throw new RangeError('the sum overflows');
  ps.length = i;
  if (x !== 0) ps.push(x);
}

/** The partials' exact total rounded to the nearest double, ties to even across partials (math.fsum). */
function roundPartials(ps: readonly number[]): number {
  let [hi, lo, n] = [0, 0, ps.length];
  // From the top while the running sum stays exact; n ends as the index of the last partial added.
  for (const y of [...ps].reverse()) {
    const x = hi;
    hi = x + y;
    lo = y - (hi - x);
    n--;
    if (lo !== 0) break;
  }
  const below = ps[n - 1] ?? 0;
  if ((lo < 0 && below < 0) || (lo > 0 && below > 0)) {
    const y = lo * 2;
    const x = hi + y;
    if (y === x - hi) hi = x;
  }
  return hi;
}

function fsum(xs: Data, map: (x: number) => number = (x) => x): number {
  const ps: number[] = [];
  for (const x of xs) addPartial(ps, map(x));
  return roundPartials(ps);
}

function check(xs: Data, least: number): void {
  if (xs.length < least) throw new RangeError(`needs at least ${least} value${least === 1 ? '' : 's'}`);
  for (const x of xs) if (!Number.isFinite(x)) throw new RangeError('every value must be finite');
}

/** The exactly rounded sum; 0 for no values. */
export function sum(xs: Data): number {
  check(xs, 0);
  return fsum(xs);
}

/** The exactly rounded sum divided by n (statistics.fmean), kept inside the data's range. */
export function mean(xs: Data): number {
  check(xs, 1);
  let [lo, hi] = [Infinity, -Infinity];
  for (const x of xs) [lo, hi] = [Math.min(lo, x), Math.max(hi, x)];
  const m = fsum(xs) / xs.length;
  return m < lo ? lo : m > hi ? hi : m;
}

// 2^400, 2^-400 and 2^600 as literals: ECMA-262 lets `**` approximate (sec-numeric-types-number-exponentiate).
const HUGE = 2.5822498780869086e120;
const TINY = 3.8725919148493183e-121;
const SCALE = 4.149515568880993e180;

/** [the variance of c·xs, c], with c a power of two that keeps the squares inside the normal doubles. */
function scaledVariance(xs: Data, kind: VarianceKind): [number, number] {
  check(xs, kind === 'sample' ? 2 : 1);
  let big = 0;
  for (const x of xs) big = Math.max(big, Math.abs(x));
  const c = big > HUGE ? 1 / SCALE : big < TINY ? SCALE : 1;
  const n = xs.length;
  const m = fsum(xs, (x) => x * c) / n;
  const s1 = fsum(xs, (x) => x * c - m);
  const s2 = fsum(xs, (x) => (x * c - m) * (x * c - m));
  const ss = s2 - (s1 * s1) / n;
  return [(ss > 0 ? ss : 0) / (kind === 'sample' ? n - 1 : n), c];
}

/** Sample (divisor n - 1, at least two values) or population (divisor n) variance. */
export function variance(xs: Data, kind: VarianceKind): number {
  const [v, c] = scaledVariance(xs, kind);
  const unscaled = v / c / c;
  if (unscaled === Infinity) throw new RangeError('the variance overflows');
  return unscaled;
}

/** The square root of the variance, finite wherever the deviation is; Math.sqrt is correctly rounded. */
export function sd(xs: Data, kind: VarianceKind): number {
  const [v, c] = scaledVariance(xs, kind);
  return Math.sqrt(v) / c;
}

/** a + t(b - a), NumPy's form: exact at t = 0 and t = 1, and halved first where b - a overflows. */
export function lerp(a: number, b: number, t: number): number {
  const d = b - a;
  if (!Number.isFinite(d)) return 2 * lerp(a / 2, b / 2, t);
  return t < 0.5 ? a + d * t : b - d * (1 - t);
}

function sorted(xs: Data): Float64Array {
  check(xs, 1);
  return Float64Array.from(xs).sort();
}

function at(s: Float64Array, p: number, method: QuantileMethod): number {
  if (!(p >= 0 && p <= 1)) throw new RangeError('p must lie in [0, 1]');
  const last = s.length - 1;
  const h = method === 'inclusive' ? last * p : (last + 2) * p - 1;
  const outside = h <= 0 || h >= last;
  const j = outside ? (h <= 0 ? 0 : last) : Math.floor(h);
  const [a = NaN, b = a] = s.subarray(j, j + 2);
  return outside ? a : lerp(a, b, h - j);
}

/** The p-quantile by the named convention (the decision notes above). */
export const quantile = (xs: Data, p: number, method: QuantileMethod): number => at(sorted(xs), p, method);

/** The lower quartile, median and upper quartile, from one sort. */
export function quartiles(xs: Data, method: QuantileMethod): [number, number, number] {
  const s = sorted(xs);
  return [at(s, 0.25, method), at(s, 0.5, method), at(s, 0.75, method)];
}

/** The 0.5 quantile, where both conventions agree. */
export const median = (xs: Data): number => quantile(xs, 0.5, 'inclusive');
