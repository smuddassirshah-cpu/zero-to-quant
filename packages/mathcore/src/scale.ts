// Linear and log scales with nice ticks (docs/PLAN.md 11.3 row 3; ARCHITECTURE.md 5.11 names the module). Decision notes:
// - In @zq/mathcore, not src/engine/render: the stage 3 row puts scales here, and a scene's derive or a widget's
//   logic.ts may not import engine/render (ARCHITECTURE.md 4.5) [our choice: PLAN.md wins over 4.2 and 5.11].
// - Maps interpolate with stats' `lerp`, so each end of the domain maps exactly to its end of the range and back.
//   A degenerate domain maps every value to the middle of the range; a degenerate range inverts to the middle
//   of the domain, the geometric middle on a log scale [our choice].
// - The log scale takes `{ log, exp }` typed to dmath's signatures, so given @zq/mathcore/dmath it is
//   deterministic; a follow-up makes dmath the default once it merges. Its map is base-free; its ticks are
//   decimal.
// - Ticks use no transcendental function. A value's decade and mantissa come from toExponential, and each
//   tick is Number(`${k}e${p}`), the double nearest k × 10^p, so it prints as that decimal with no noise.
//   ECMA-262 fixes that rounding up to 20 significant digits (RoundMVResult), which every tick has unless a
//   count above about 280 meets the doubles' resolution [inferred]; toExponential's last digit is not unique,
//   which matters only where a mantissa ties a threshold to 17 digits [inferred; both clauses sourced at
//   tc39/ecma262 6db9135, 8 October 2026].
// - Linear steps are 1, 2 or 5 times a power of ten, chosen by the mantissa of span / count against √2, √10
//   and √50 (d3-array's tickSpec [recalled]), so a step is at least 2/√10 of span / count and there are at
//   most ⌊1.59 max(count, 2)⌋ + 1 ticks (one tick that finds none retries with two, as d3 does). Where the
//   step comes within 5 ulps of the doubles' spacing, a multiple just outside each end can round onto it, for
//   at most two more [measured: fast-check, 100,000 domains a few ulps wide].
// - Log ticks are the finest of {1..9}, {1, 2, 5} and {1} times each power of ten that gives at most
//   `count`, the linear ticks when that is fewer than half of `count` (d3-scale's rule [recalled]), and past
//   one a decade every s-th power for the least s in 2, 5, 10, 20, ... that fits max(count, 2).
// - Ticks rise whatever the domain's orientation, each inside it by double comparison; ticks finer than the
//   doubles there collapse, so the list stays strictly increasing. A call makes O(count) string conversions,
//   since each mantissa set stops once it passes `count` [measured: under 0.5 ms a call, counts up to 200].
// - Errors are RangeErrors: a non-finite end or span, a log domain or argument that is not positive, and a
//   count that is not a positive integer.
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

const SQRT2 = 1.4142135623730951;
const SQRT10 = 3.1622776601683795;
const SQRT50 = 7.0710678118654755;
const MANTISSAS = [[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 5], [1]] as const;

/** x's decimal mantissa, in [1, 10) unless x is 0, and exponent, from its shortest round-trip spelling. */
function decimal(x: number): [number, number] {
  const [m = '', e = ''] = x.toExponential().split('e');
  return [Number(m), Number(e)];
}

const tick = (k: bigint | number, p: number): number => Number(`${k}e${p}`);

function finite(name: string, [a, b]: Pair): Pair {
  if (!Number.isFinite(b - a)) throw new RangeError(`the ${name} must be finite, with a finite span`);
  return [a, b];
}

function counted(count: number): number {
  if (!Number.isInteger(count) || count < 1) throw new RangeError('a tick count is a positive integer');
  return count;
}

function linearTicks(lo: number, hi: number, count: number): number[] {
  if (lo === hi) return [lo];
  const [m, e] = decimal(Math.max((hi - lo) / count, Number.MIN_VALUE));
  const [f, p] = m >= SQRT50 ? [1n, e + 1] : m >= SQRT10 ? [5n, e] : m >= SQRT2 ? [2n, e] : [1n, e];
  const at = (k: bigint): number => tick(k * f, p);
  const [lm, le] = decimal(lo);
  // lo / step from the decimal spellings, which neither overflow nor underflow, then corrected exactly.
  let k = BigInt(Math.ceil(tick(lm, le - p) / Number(f)));
  while (at(k - 1n) >= lo) k--;
  while (at(k) < lo) k++;
  const out: number[] = [];
  for (let t = at(k); t <= hi; t = at(++k)) if (t !== out.at(-1)) out.push(t);
  return out.length === 0 && count < 2 ? linearTicks(lo, hi, 2) : out;
}

function logTicks(lo: number, hi: number, count: number): number[] {
  if (lo === hi) return [lo];
  const [lm, p0] = decimal(lo);
  const p1 = decimal(hi)[1];
  for (const ms of MANTISSAS) {
    const out: number[] = [];
    for (let p = p0; p <= p1 && out.length <= count; p++)
      for (const m of ms) {
        const t = tick(m, p);
        if (t >= lo && t <= hi && t !== out.at(-1)) out.push(t);
      }
    if (out.length <= count) return 2 * out.length < count ? linearTicks(lo, hi, count) : out;
  }
  // More powers of ten than `count`: those from 10^pa to 10^p1 whose exponent is a multiple of s.
  const pa = lm === 1 ? p0 : p0 + 1;
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
    map: (x) => lerp(r0, r1, d1 === d0 ? 0.5 : (x - d0) / (d1 - d0)),
    invert: (y) => lerp(d0, d1, r1 === r0 ? 0.5 : (y - r0) / (r1 - r0)),
    ticks: (count) => linearTicks(Math.min(d0, d1), Math.max(d0, d1), counted(count)),
  };
}

/** The map affine in log x from a positive domain to the range, with `log` and `exp` supplied. */
export function logScale(domain: Pair, range: Pair, math: LogExp): Scale {
  const [d0, d1] = finite('domain', domain);
  if (!(d0 > 0 && d1 > 0)) throw new RangeError('a log domain must be positive');
  const [r0, r1] = finite('range', range);
  const l0 = math.log(d0);
  const span = math.log(d1) - l0;
  return {
    domain: [d0, d1],
    range: [r0, r1],
    map(x) {
      if (!(x > 0)) throw new RangeError('a log scale maps positive values only');
      return lerp(r0, r1, span === 0 ? 0.5 : (math.log(x) - l0) / span);
    },
    invert(y) {
      const t = r1 === r0 ? 0.5 : (y - r0) / (r1 - r0);
      return t < 0.5 ? d0 * math.exp(t * span) : d1 * math.exp((t - 1) * span);
    },
    ticks: (count) => logTicks(Math.min(d0, d1), Math.max(d0, d1), counted(count)),
  };
}
