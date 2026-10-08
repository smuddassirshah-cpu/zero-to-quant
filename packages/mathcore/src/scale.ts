// Linear and log scales with nice ticks (docs/PLAN.md 11.3 row 3; ARCHITECTURE.md 5.11 names the module). Decision notes:
// - In @zq/mathcore, not src/engine/render: the stage 3 row puts scales here, and a scene's derive or a
//   widget's logic.ts may not import engine/render (ARCHITECTURE.md 4.5) [our choice: PLAN.md wins over 4.2
//   and 5.11].
// - Maps interpolate with stats' `lerp`, so each end of the domain maps exactly to its end of the range and
//   back. A degenerate domain maps every value to the middle of the range; a degenerate range inverts to the
//   middle of the domain, the geometric middle on a log scale [our choice]. The log map is log(x / d0) /
//   log(d1 / d0), each log of a ratio taken without cancellation, so a narrow domain far from 1 keeps its
//   resolution: within a factor of 2, Kahan's z·log(w) / (w - 1) with z = (x - d0) / d0 and w = 1 + z, x - d0
//   being exact [recalled: Goldberg 1991, theorem 4]; elsewhere the log of the ratio; and where the ratio
//   leaves the normal doubles, a difference of logs, which then exceeds 708 against logs of at most 745
//   [inferred].
// - The log scale takes `{ log, exp }` typed to dmath's signatures, so given @zq/mathcore/dmath it is
//   deterministic; a follow-up makes dmath the default once it merges. Its map is base-free; its ticks are
//   decimal.
// - Ticks use no transcendental function. A value's decade and mantissa come from toExponential, and each
//   tick is Number(`${k}e${p}`), the double nearest k × 10^p, so it prints as that decimal with no noise.
//   ECMA-262 fixes that rounding up to 20 significant digits (RoundMVResult) [sourced: tc39/ecma262 6db9135,
//   8 October 2026]. Every k here is below about √50 · 2^53 · count, under 10^20 for counts up to the cap of
//   1,000 [inferred: max(|lo|, |hi|) / (hi - lo) is at most 2^53 + 1 for distinct doubles; measured: at most
//   20 significant digits over domains one to three ulps wide at every binary exponent].
// - Linear steps are 1, 2 or 5 times a power of ten, chosen by the exact rational r = (hi - lo) / count: for
//   10^p <= r < 10^(p+1), the step is 10^(p+1), 5 × 10^p, 2 × 10^p or 10^p as (r / 10^p)^2 reaches 50, 10, 2
//   or none (d3-array 3.2.4's tickSpec makes the same test on the rounded double step [sourced:
//   src/ticks.js]). BigInt decides it, so the steps match the twin's at the thresholds and on subnormal
//   spans. A step is at least 2/√10 of r, so there are at most ⌊1.59 max(count, 2)⌋ + 1 ticks (one tick that
//   finds none retries with two, as d3 does). Where the step comes within 5 ulps of the doubles' spacing, a
//   multiple just outside each end can round onto it, for at most two more [measured: fast-check, 100,000
//   domains a few ulps wide].
// - Log ticks are the finest of {1..9}, {1, 2, 5} and {1} times each power of ten that gives at most `count`.
//   The linear ticks replace it when it gives fewer than half of `count` and is {1..9} (d3-scale 4.0.2's
//   rule, which it applies to that set only [sourced: src/log.js line 102]) or the domain is narrower than a
//   decade, hi < 10 lo exactly, where a coarser set can be empty [our choice]. Past one a decade, ticks are
//   every s-th power for the least s in 2, 5, 10, 20, ... that fits max(count, 2).
// - Ticks rise whatever the domain's orientation, each inside it by double comparison; ticks finer than the
//   doubles there collapse, so the list stays strictly increasing. A count is an integer from 1 to 1,000, so
//   a call makes O(count) string conversions and BigInt operations on numbers of a few thousand bits
//   [measured: under 1 ms a call at 1,000, Node 22.22.0].
// - Errors are RangeErrors: a non-finite end or span, a log domain or argument that is not positive, and a
//   count outside 1 to 1,000.
import { lerp } from './stats.ts';

export interface LogExp {
  readonly log: (x: number) => number;
  readonly exp: (x: number) => number;
}

export interface Scale {
  readonly domain: readonly [number, number];
  readonly range: readonly [number, number];
  map(x: number): number;
  invert(y: number): number;
  /** About `count` nice values inside the domain, increasing (the decision notes above). */
  ticks(count: number): number[];
}

type Pair = readonly [number, number];

const MOST_TICKS = 1000;
const MIN_NORMAL = 2.2250738585072014e-308;
const MANTISSAS = [[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 5], [1]] as const;
const bits = new DataView(new ArrayBuffer(8));

/** x's decimal mantissa, in [1, 10) unless x is 0, and exponent, from its shortest round-trip spelling. */
function decimal(x: number): [number, number] {
  const [m = '', e = ''] = x.toExponential().split('e');
  return [Number(m), Number(e)];
}

const tick = (k: bigint | number, p: number): number => Number(`${k}e${p}`);

/** x as n × 2^e exactly, n an integer. */
function dyadic(x: number): [bigint, number] {
  bits.setFloat64(0, x);
  const word = bits.getBigUint64(0);
  const biased = Number((word >> 52n) & 0x7ffn);
  const n = (word & 0xfffffffffffffn) | (biased === 0 ? 0n : 0x10000000000000n);
  return [word >> 63n === 0n ? n : -n, Math.max(biased, 1) - 1075];
}

/** k·a - b exactly, as n × 2^e. */
function scaledDifference(a: number, b: number, k: bigint): [bigint, number] {
  const [[na, ea], [nb, eb]] = [dyadic(a), dyadic(b)];
  const e = Math.min(ea, eb);
  return [k * (na << BigInt(ea - e)) - (nb << BigInt(eb - e)), e];
}

/** Whether x / y >= 10^q, for positive x and y. */
const atLeast = (x: bigint, y: bigint, q: number): boolean =>
  q < 0 ? x * 10n ** BigInt(-q) >= y : x >= y * 10n ** BigInt(q);

/** (x - a) / (b - a), halving first where x - a overflows. */
const fraction = (x: number, a: number, b: number): number =>
  Number.isFinite(x - a) ? (x - a) / (b - a) : (x / 2 - a / 2) / ((b - a) / 2);

function finite(name: string, [a, b]: Pair): Pair {
  if (!Number.isFinite(b - a)) throw new RangeError(`the ${name} must be finite, with a finite span`);
  return [a, b];
}

function counted(count: number): number {
  if (!(Number.isInteger(count) && count >= 1 && count <= MOST_TICKS))
    throw new RangeError('a tick count is an integer from 1 to 1,000');
  return count;
}

function linearTicks(lo: number, hi: number, count: number): number[] {
  if (lo === hi) return [lo];
  // r = a / b exactly; p is its decade, from the digit counts and one exact comparison.
  const [n, e] = scaledDifference(hi, lo, 1n);
  const [a, b] = e < 0 ? [n, BigInt(count) << BigInt(-e)] : [n << BigInt(e), BigInt(count)];
  let p = String(a).length - String(b).length;
  if (!atLeast(a, b, p)) p--;
  const reaches = (t: bigint): boolean => atLeast(a * a, t * b * b, 2 * p);
  const [f, q] = reaches(50n) ? [1n, p + 1] : reaches(10n) ? [5n, p] : reaches(2n) ? [2n, p] : [1n, p];
  const at = (k: bigint): number => tick(k * f, q);
  const [lm, le] = decimal(lo);
  // lo / step from the decimal spellings, which neither overflow nor underflow, then corrected exactly.
  let k = BigInt(Math.ceil(tick(lm, le - q) / Number(f)));
  while (at(k - 1n) >= lo) k--;
  while (at(k) < lo) k++;
  const out: number[] = [];
  for (let t = at(k); t <= hi; t = at(++k)) if (t !== out.at(-1)) out.push(t);
  return out.length === 0 && count < 2 ? linearTicks(lo, hi, 2) : out;
}

function logTicks(lo: number, hi: number, count: number): number[] {
  if (lo === hi) return [lo];
  const [p0, p1] = [decimal(lo)[1], decimal(hi)[1]];
  for (const ms of MANTISSAS) {
    const out: number[] = [];
    for (let p = p0; p <= p1 && out.length <= count; p++)
      for (const m of ms) {
        const t = tick(m, p);
        if (t >= lo && t <= hi && t !== out.at(-1)) out.push(t);
      }
    if (out.length > count) continue;
    const sparse = 2 * out.length < count && (ms === MANTISSAS[0] || scaledDifference(lo, hi, 10n)[0] > 0n);
    return sparse ? linearTicks(lo, hi, count) : out;
  }
  // More powers of ten than `count`: those from 10^pa to 10^p1 whose exponent is a multiple of s.
  const pa = tick(1, p0) >= lo ? p0 : p0 + 1;
  const most = Math.max(count, 2);
  for (let s = 2; ; s *= String(s).startsWith('2') ? 2.5 : 2) {
    const [q0, q1] = [Math.ceil(pa / s), Math.floor(p1 / s)];
    if (q1 - q0 < most) return Array.from({ length: q1 - q0 + 1 }, (_, j) => tick(1, (q0 + j) * s));
  }
}

/** The affine map from domain to range. */
export function linearScale(domain: Pair, range: Pair): Scale {
  const [d0, d1] = finite('domain', domain);
  const [r0, r1] = finite('range', range);
  return {
    domain: [d0, d1],
    range: [r0, r1],
    map: (x) => lerp(r0, r1, d1 === d0 ? 0.5 : fraction(x, d0, d1)),
    invert: (y) => lerp(d0, d1, r1 === r0 ? 0.5 : (y - r0) / (r1 - r0)),
    ticks: (count) => linearTicks(Math.min(d0, d1), Math.max(d0, d1), counted(count)),
  };
}

/** The map affine in log x from a positive domain to the range, with `log` and `exp` supplied. */
export function logScale(domain: Pair, range: Pair, math: LogExp): Scale {
  const [d0, d1] = finite('domain', domain);
  if (!(d0 > 0 && d1 > 0)) throw new RangeError('a log domain must be positive');
  const [r0, r1] = finite('range', range);
  const logRatio = (x: number, y: number): number => {
    if (x <= 2 * y && y <= 2 * x) {
      const z = (x - y) / y;
      const w = 1 + z;
      return w === 1 ? z : (math.log(w) * z) / (w - 1);
    }
    const q = x / y;
    return q >= MIN_NORMAL && q < Infinity ? math.log(q) : math.log(x) - math.log(y);
  };
  const span = logRatio(d1, d0);
  return {
    domain: [d0, d1],
    range: [r0, r1],
    map(x) {
      if (!(x > 0)) throw new RangeError('a log scale maps positive values only');
      return lerp(r0, r1, d0 === d1 ? 0.5 : logRatio(x, d0) / span);
    },
    invert(y) {
      const t = r1 === r0 ? 0.5 : (y - r0) / (r1 - r0);
      return t < 0.5 ? d0 * math.exp(t * span) : d1 * math.exp((t - 1) * span);
    },
    ticks: (count) => logTicks(Math.min(d0, d1), Math.max(d0, d1), counted(count)),
  };
}
