// Basic statistics for shown and graded numbers (docs/PLAN.md 11.3 row 3; ARCHITECTURE.md 4.3). Decision notes:
// - Sums are exactly rounded: Shewchuk's partials with the half-even correction of CPython's math.fsum, so
//   `mean` is fsum(xs) / n, as statistics.fmean, kept inside [min, max]: the two roundings can leave it
//   (fmean gives 0.10000000000000002 for three 0.1s [measured, CPython 3.12.15]). The partials sit in a
//   Float64Array that grows as math.fsum's list does: they never overlap, but a low one can exceed half an ulp
//   of the next (8897893.239287795 under 29892972380160 [measured]), so only the 2,098 bit positions of a
//   double bound their count [inferred]; random adversarial sums reached 28 [measured]. A sum is O(n) in
//   index loops. Against for-of over a pushed array it is about 6 times faster on uniform(-100, 100) data, 4
//   times on 10^9 + uniform(0, 10^-3) and 2 times on ±10^uniform(-20, 20) [measured: Node 22.22.0, 10,000
//   values, idle machine; 5.9 to 6.6, 3.8 to 4.0 and 2.1 on three runs].
//   An empty sum is 0; every other statistic needs data. `mean` throws where the sum overflows, as fmean
//   raises [our choice]: summing the data scaled by 2^-600 would drop its smallest terms, and under
//   cancellation they are the mean ([1.7e308, 1.7e308, -1.7e308, -1.7e308, 1e-320] has mean 2e-321, the
//   scaled sum 0) [measured].
// - Variance is two-pass: the mean m, then the sums of d = x - m and of d², corrected to Σd² - (Σd)²/n, the
//   corrected two-pass algorithm [recalled: Chan, Golub and LeVeque, The American Statistician 37(3), 1983],
//   which removes the error the rounded mean leaves. Its three sums are Sum2 [recalled: Ogita, Rump and Oishi,
//   SIAM J. Sci. Comput. 26(6), 2005, proposition 4.5], within u|S| + γ²Σ|x| of the exact S, with u = 2^-53
//   and γ = (n - 1)u/(1 - (n - 1)u): as good as exactly rounded to first order. To that order the variance
//   errs by at most 6u·V + 7u·n·e²/D, with e the mean's error (|e| ≤ 2u·max|x|) and D the divisor;
//   test/stats.test.ts derives the bound and takes its tolerances from it [inferred]. Rejected: the exact
//   partials, 1.1 ms at 10,000 values against Sum2's 0.05 ms [measured: Node 22.22.0], when derive has 2 ms
//   at 4x throttling (ARCHITECTURE.md 5.14); Welford's update, which rounds at every step; Σx² - (Σx)²/n,
//   which cancels catastrophically. Data beyond 2^±400 is first scaled by 2^∓600, so no square or sum
//   overflows and the squares of subnormal data stay normal. Scaling up is exact. Scaling down is exact except
//   for members below 2^-422, which become subnormal or 0: each moves by at most 2^-475 while the spread
//   exceeds 2^399, so the variance moves by less than 2^-800 of itself, far below its bound [inferred]. A
//   variance or deviation throws where it overflows, and may also throw within its error bound (a few ulp) of
//   Number.MAX_VALUE, where statistics can still give MAX_VALUE [measured: variance([a, -a, a], 'sample') with
//   a = 1.1611502276392735e154; CPython 3.12.15]. `sd` keeps the deviation of subnormal data, as
//   statistics.stdev does. ECMA-262 makes Math.sqrt correctly rounded (sec-math.sqrt) [sourced].
// - Quantiles sort a copy, O(n log n) (selection would save little at these sizes), and interpolate between
//   neighbours at a 0-based position h: 'inclusive' h = (n - 1)p, NumPy's default 'linear' and
//   statistics.quantiles(method="inclusive"); 'gcse' h = (n + 1)p - 1, the GCSE convention of
//   docs/curriculum/stage0-precalc-computing.md C5 (drill drl.pre.summary-stats). Where h falls outside
//   [0, n - 1] the result is the end value [our choice]; statistics.quantiles(method="exclusive") extrapolates
//   there [measured: CPython 3.12.15 gives 0.75 as the lower quartile of [1, 2]].
// - `lerp` is NumPy's _lerp: a + t(b - a) below t = 0.5 and b - (1 - t)(b - a) from it, exact at both ends
//   [sourced: NumPy 2.4.6 numpy/lib/_function_base_impl.py, _lerp], so 'inclusive' is bit-identical to
//   numpy.quantile wherever NumPy's b - a stays finite, up to the sign of a zero: the sort puts -0 before 0
//   [recalled: ECMA-262 CompareTypedArrayElements; measured: Node 22.22.0] and an end value is returned as
//   it is, where NumPy's lerp makes the lowest quantile of [-0, 0] a 0 [measured: NumPy 2.4.6]. Any finite t
//   extrapolates, as the scales need. Where b - a, its product with t or the sum leaves the doubles, lerp
//   interpolates the halved ends and doubles the result, which scales each step by a power of two, so the
//   result is ±Infinity only where the rounded interpolant lies beyond Number.MAX_VALUE, as IEEE-754
//   arithmetic gives [our choice].
// - Errors are RangeErrors, for invalid inputs (too little data, a NaN or infinite value, lerp end or t, and p
//   outside [0, 1]) and for a sum, variance or deviation that overflows. A lerp with valid inputs never
//   throws: its overflow is the ±Infinity above.
export type VarianceKind = 'sample' | 'population';
export type QuantileMethod = 'inclusive' | 'gcse';
/** An array or a typed array of values. */
export type Data = ArrayLike<number> & Iterable<number>;

/** Shewchuk's partials: non-overlapping, increasing in magnitude, summing exactly to every value added. */
class Partials {
  #ps = new Float64Array(32);
  #n = 0;

  /** The k-th partial; 0 below the first. */
  #at(k: number): number {
    return this.#ps[k] ?? 0;
  }

  add(value: number): void {
    const ps = this.#ps;
    let x = value;
    let i = 0;
    for (let k = 0; k < this.#n; k++) {
      let y = this.#at(k);
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
    if (x !== 0) {
      if (i === ps.length) {
        this.#ps = new Float64Array(2 * i);
        this.#ps.set(ps);
      }
      this.#ps[i++] = x;
    }
    this.#n = i;
  }

  /** The partials' exact total rounded to the nearest double, ties to even across partials (math.fsum). */
  round(): number {
    let n = this.#n;
    let hi = 0;
    let lo = 0;
    // From the top while the running sum stays exact; n ends as the index of the last partial added.
    while (n > 0) {
      const x = hi;
      const y = this.#at(--n);
      hi = x + y;
      lo = y - (hi - x);
      if (lo !== 0) break;
    }
    const below = this.#at(n - 1);
    if ((lo < 0 && below < 0) || (lo > 0 && below > 0)) {
      const y = lo * 2;
      const x = hi + y;
      if (y === x - hi) hi = x;
    }
    return hi;
  }
}

/** xs[j], with a hole read as NaN, which `range` refuses. Index loops over the data run about twice as fast
 * as for-of in V8 [measured: Node 22.22.0, 10,000 values]. */
const value = (xs: Data, j: number): number => xs[j] ?? NaN;

/** [min, max] of at least `least` values, all finite. */
function range(xs: Data, least: number): [number, number] {
  if (xs.length < least) throw new RangeError(`needs at least ${least} value${least === 1 ? '' : 's'}`);
  let lo = Infinity;
  let hi = -Infinity;
  for (let j = 0; j < xs.length; j++) {
    const x = value(xs, j);
    if (!Number.isFinite(x)) throw new RangeError('every value must be finite');
    lo = Math.min(lo, x);
    hi = Math.max(hi, x);
  }
  return [lo, hi];
}

/** The exactly rounded sum. */
function fsum(xs: Data): number {
  const total = new Partials();
  for (let j = 0; j < xs.length; j++) total.add(value(xs, j));
  return total.round();
}

/** Sum2 of Ogita, Rump and Oishi: Knuth's TwoSum carries each rounding error into a second sum. */
class Sum2 {
  #s = 0;
  #e = 0;

  add(x: number): void {
    const s = this.#s;
    const t = s + x;
    const z = t - s;
    this.#e += s - (t - z) + (x - z);
    this.#s = t;
  }

  get total(): number {
    return this.#s + this.#e;
  }
}

/** The exactly rounded sum; 0 for no values. */
export function sum(xs: Data): number {
  range(xs, 0);
  return fsum(xs);
}

/** The exactly rounded sum divided by n (statistics.fmean), kept inside the data's range. */
export function mean(xs: Data): number {
  const [lo, hi] = range(xs, 1);
  const m = fsum(xs) / xs.length;
  return m < lo ? lo : m > hi ? hi : m;
}

// 2^400, 2^-400 and 2^600 as literals: ECMA-262 lets `**` approximate (sec-numeric-types-number-exponentiate).
const HUGE = 2.5822498780869086e120;
const TINY = 3.8725919148493183e-121;
const SCALE = 4.149515568880993e180;

/** [the variance of c·xs, c], with c a power of two that keeps the squares inside the normal doubles. */
function scaledVariance(xs: Data, kind: VarianceKind): [number, number] {
  const [lo, hi] = range(xs, kind === 'sample' ? 2 : 1);
  const big = Math.max(-lo, hi);
  const c = big > HUGE ? 1 / SCALE : big < TINY ? SCALE : 1;
  const n = xs.length;
  const total = new Sum2();
  for (let j = 0; j < n; j++) total.add(value(xs, j) * c);
  const m = total.total / n;
  const s1 = new Sum2();
  const s2 = new Sum2();
  for (let j = 0; j < n; j++) {
    const d = value(xs, j) * c - m;
    s1.add(d);
    s2.add(d * d);
  }
  const ss = s2.total - (s1.total * s1.total) / n;
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
  const unscaled = Math.sqrt(v) / c;
  if (unscaled === Infinity) throw new RangeError('the deviation overflows');
  return unscaled;
}

/** NumPy's _lerp: a + t(b - a) below t = 0.5 and b - (1 - t)(b - a) from it. */
const interpolate = (a: number, b: number, t: number): number =>
  t < 0.5 ? a + (b - a) * t : b - (b - a) * (1 - t);

/** a + t(b - a), exact at t = 0 and t = 1, for finite ends and a finite t; ±Infinity where the result leaves
 * the doubles, and computed on the halved ends where only a step does. */
export function lerp(a: number, b: number, t: number): number {
  if (!Number.isFinite(a) || !Number.isFinite(b)) throw new RangeError('lerp needs finite ends');
  if (!Number.isFinite(t)) throw new RangeError('lerp needs a finite t');
  const r = interpolate(a, b, t);
  return Number.isFinite(r) ? r : 2 * interpolate(a / 2, b / 2, t);
}

function sorted(xs: Data): Float64Array {
  range(xs, 1);
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
