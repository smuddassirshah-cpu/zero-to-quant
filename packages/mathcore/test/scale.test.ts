import { readFileSync } from 'node:fs';
import fc from 'fast-check';
import { describe, expect, it } from 'vitest';
import { linearScale, logScale, type Scale } from '@zq/mathcore/scale';

/** A golden value: a non-finite one as the string Number reads back; null where the twin refuses it. */
type Value = number | string;
interface Golden {
  kind: 'linear' | 'log';
  domain: [number, number];
  range: [number, number];
  count: number;
  ticks: number[];
  x: Value[];
  map: (Value | null)[];
  y: Value[];
  invert: (Value | null)[];
}

const golden = readFileSync(new URL('scale.golden.jsonl', import.meta.url), 'utf8')
  .split('\n')
  .filter(Boolean)
  .map((line) => JSON.parse(line) as Golden);
// The engine's own functions stand in for dmath until it merges; tests are not graded paths.
const M = { log: Math.log, exp: Math.exp };
const U = 2 ** -53;
const MAX = Number.MAX_VALUE;
const REFUSED = [NaN, Infinity, -Infinity];
const most = (count: number): number => Math.floor(1.59 * Math.max(count, 2)) + 1;
const word = new DataView(new ArrayBuffer(8));
/** x moved n doubles up (n > 0) or down, for x > 0. */
function nudge(x: number, n: number): number {
  word.setFloat64(0, x);
  word.setBigUint64(0, word.getBigUint64(0) + BigInt(n));
  return word.getFloat64(0);
}

/** Increasing, inside [lo, hi] and within the stated slack; away from the doubles' resolution (no `extra`),
 *  each tick also prints as a short decimal. */
function wellFormed(ticks: number[], lo: number, hi: number, count: number, extra = 0): void {
  expect(ticks.length).toBeGreaterThanOrEqual(1);
  expect(ticks.length).toBeLessThanOrEqual(most(count) + extra);
  ticks.forEach((t, i) => {
    expect(t >= lo && t <= hi && (i === 0 || t > (ticks[i - 1] ?? -Infinity))).toBe(true);
    if (extra === 0) expect(Number(t.toPrecision(14))).toBe(t);
  });
}

describe('linearScale', () => {
  const y = linearScale([0, 10], [300, 0]);

  it('maps and inverts, reversed ranges and extrapolation included, exactly at the ends', () => {
    expect([y.map(0), y.map(10), y.map(5), y.map(20)]).toEqual([300, 0, 150, -300]);
    expect([y.invert(300), y.invert(0), y.invert(150)]).toEqual([0, 10, 5]);
    expect(y.domain).toEqual([0, 10]);
    expect(y.range).toEqual([300, 0]);
  });

  it('gives 1, 2 or 5 times a power of ten, in order whatever the orientation', () => {
    expect(linearScale([0, 1], [0, 1]).ticks(5)).toEqual([0, 0.2, 0.4, 0.6, 0.8, 1]);
    expect(linearScale([0, 1], [0, 1]).ticks(10)).toEqual([
      0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1,
    ]);
    expect(linearScale([1, -1], [0, 1]).ticks(4)).toEqual([-1, -0.5, 0, 0.5, 1]);
    expect(linearScale([0, 365], [0, 1]).ticks(7)).toEqual([0, 50, 100, 150, 200, 250, 300, 350]);
    expect(linearScale([0.1, 0.9], [0, 1]).ticks(1)).toEqual([0.5]);
    expect(linearScale([1e16, 1e16 + 4], [0, 1]).ticks(10)).toEqual([1e16, 1e16 + 2, 1e16 + 4]);
  });

  it('chooses the step from the exact span, at the thresholds and on subnormal spans', () => {
    // The span over the count lies just below √2 × 10^-13 and √50 × 10^-21 [the twin's values].
    expect(linearScale([0, 1.414213562373095e-13], [0, 1]).ticks(1)).toEqual([0]);
    expect(linearScale([1e-20, 5.242640687119285e-20], [0, 1]).ticks(3)).toEqual([2e-20, 4e-20]);
    const subnormal = linearScale([-6e-323, 1.6e-322], [0, 1]).ticks(30);
    expect([subnormal.length, subnormal[0], subnormal.at(-1)]).toEqual([23, -6e-323, 1.6e-322]);
    expect(linearScale([-1e308, 7e307], [0, 1]).ticks(3)).toEqual([-1e308, -5e307, 0, 5e307]);
  });

  it('defines degenerate domains and ranges', () => {
    const point = linearScale([3, 3], [0, 100]);
    expect([point.map(3), point.map(-7), point.invert(20)]).toEqual([50, 50, 3]);
    expect(point.ticks(5)).toEqual([3]);
    const flat = linearScale([0, 8], [7, 7]);
    expect([flat.map(1), flat.invert(7), flat.invert(0)]).toEqual([7, 4, 4]);
    expect(linearScale([-1e308, 0], [0, 1]).map(1e308)).toBe(2);
  });

  it('refuses non-finite ends or spans and counts that are not positive integers', () => {
    expect(() => linearScale([0, NaN], [0, 1])).toThrow(RangeError);
    expect(() => linearScale([-1.7e308, 1.7e308], [0, 1])).toThrow(RangeError);
    expect(() => linearScale([0, 1], [0, Infinity])).toThrow(RangeError);
    for (const count of [0, 1.5, NaN, 1001, 1e300]) expect(() => y.ticks(count)).toThrow(RangeError);
    expect(linearScale([0, 1], [0, 1]).ticks(1000)).toHaveLength(1001);
  });

  it('keeps every tick property, and round-trips map through invert', () => {
    const end = fc.double({ min: -1e6, max: 1e6, noNaN: true });
    const span = fc.double({ min: 1e-3, max: 1e6, noNaN: true });
    fc.assert(
      fc.property(end, span, fc.integer({ min: 1, max: 50 }), fc.boolean(), (lo, w, count, flip) => {
        const hi = lo + w;
        const s = linearScale(flip ? [hi, lo] : [lo, hi], [0, 1000]);
        wellFormed(s.ticks(count), lo, hi, count);
        for (const t of s.ticks(count))
          expect(Math.abs(s.invert(s.map(t)) - t)).toBeLessThanOrEqual(8 * U * (Math.abs(lo) + Math.abs(hi)));
      }),
    );
  });
});

describe('ticks at the resolution of the doubles', () => {
  it('stay increasing and inside, with at most two more', () => {
    const end = fc.double({ min: -1e300, max: 1e300, noNaN: true });
    fc.assert(
      fc.property(end, fc.integer({ min: 1, max: 6 }), fc.integer({ min: 1, max: 60 }), (a, ulps, count) => {
        let b = a;
        for (let i = 0; i < ulps; i++) b += Math.max(Math.abs(b) * 2 ** -52, Number.MIN_VALUE);
        wellFormed(linearScale([a, b], [0, 1]).ticks(count), a, b, count, 2);
        const [lo, hi] = [Math.abs(a) || 1, Math.abs(b) || 1].sort((x, y) => x - y) as [number, number];
        wellFormed(logScale([lo, hi], [0, 1], M).ticks(count), lo, hi, count, 2);
      }),
    );
  });
});

describe('logScale', () => {
  const s = logScale([1, 1000], [0, 300], M);

  it('maps in log x with the functions supplied, exactly at the ends', () => {
    expect([s.map(1), s.map(1000), s.invert(0), s.invert(300)]).toEqual([0, 300, 1, 1000]);
    expect(s.map(10)).toBeCloseTo(100, 12);
    expect(s.invert(200)).toBeCloseTo(100, 10);
    const base2 = logScale([1, 1000], [0, 300], { log: (x) => Math.log2(x), exp: (v) => 2 ** v });
    expect(base2.map(10)).toBeCloseTo(100, 12);
  });

  it('picks the finest mantissa set that fits, then every s-th power, else linear ticks', () => {
    const decades = [1, 10, 100, 1000];
    expect(s.ticks(10)).toEqual([1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]);
    expect(s.ticks(4)).toEqual(decades);
    expect(s.ticks(3)).toEqual([1, 100]);
    expect(logScale([1e-300, 1e300], [0, 1], M).ticks(10)).toEqual(
      [-300, -200, -100, 0, 100, 200, 300].map((p) => Number(`1e${p}`)),
    );
    expect(logScale([3, 2], [0, 1], M).ticks(5)).toEqual([2, 2.2, 2.4, 2.6, 2.8, 3]);
    expect(logScale([20, 60], [0, 1], M).ticks(2)).toEqual([20, 50]);
    // A coarser set stays on the decades however sparse; only {1..9}, or a domain narrower than a decade,
    // goes linear.
    expect([s.ticks(9), s.ticks(21)]).toEqual([decades, [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]]);
    expect(logScale([0.1, 1000], [0, 1], M).ticks(11)).toEqual([0.1, ...decades]);
    expect(logScale([1, 1e6], [0, 1], M).ticks(15)).toEqual([...decades, 1e4, 1e5, 1e6]);
    expect(s.ticks(100)).toEqual(Array.from({ length: 100 }, (_, i) => 10 * (i + 1)));
    expect([logScale([3, 4], [0, 1], M).ticks(1), logScale([3, 9], [0, 1], M).ticks(3)]).toEqual([
      [3, 4],
      [4, 6, 8],
    ]);
    // A lower end one double above a power of ten leaves that power out.
    expect(logScale([1000000.0000000001, 1e14], [0, 1], M).ticks(5)).toEqual([1e8, 1e10, 1e12, 1e14]);
  });

  it('keeps a narrow domain far from 1 apart, ends exact', () => {
    const [d0, d1] = [1e300, 1.0000000000000002e300];
    const adjacent = logScale([d0, d1], [0, 400], M);
    expect([adjacent.map(d0), adjacent.map(d1), adjacent.invert(0), adjacent.invert(400)]).toEqual([
      0,
      400,
      d0,
      d1,
    ]);
    const narrow = logScale([1e300, 1e300 * (1 + 1e-12)], [0, 400], M);
    const x = 1e300 * (1 + 0.5e-12);
    expect(narrow.map(x)).toBeCloseTo((400 * (x - 1e300)) / (narrow.domain[1] - 1e300), 6);
    // Across k doubles, log x is affine in x to within k·2^-52 / 8 of the span, so the map is the linear one.
    fc.assert(
      fc.property(
        fc.double({ min: -300, max: 300, noNaN: true }),
        fc.integer({ min: 1, max: 1e6 }),
        fc.double({ min: 0, max: 1, noNaN: true }),
        (e, k, v) => {
          const [lo, hi] = [10 ** e, nudge(10 ** e, k)];
          const scale = logScale([lo, hi], [0, 400], M);
          const x = Math.min(lo + (hi - lo) * v, hi);
          expect([scale.map(lo), scale.map(hi)]).toEqual([0, 400]);
          expect(Math.abs(scale.map(x) - (400 * (x - lo)) / (hi - lo))).toBeLessThanOrEqual(1e-7);
        },
      ),
    );
  });

  it('defines a degenerate domain and range, and refuses values that are not positive', () => {
    const point = logScale([5, 5], [0, 1], M);
    expect([point.map(5), point.invert(1), ...point.ticks(3)]).toEqual([0.5, 5, 5]);
    expect(logScale([1, 100], [2, 2], M).invert(2)).toBeCloseTo(10, 12);
    for (const bad of [
      [0, 10],
      [-1, 10],
      [1, NaN],
    ] as const)
      expect(() => logScale(bad, [0, 1], M)).toThrow(RangeError);
    for (const x of [0, -1, NaN]) expect(() => s.map(x)).toThrow(RangeError);
  });

  // Ends at 10^e, or one double either side of the power of ten nearest it.
  const end = (e: number, snap: boolean, n: number): number =>
    snap ? nudge(Number(`1e${Math.round(e)}`), n) : 10 ** e;
  const ends = fc.tuple(
    fc.boolean(),
    fc.integer({ min: -1, max: 1 }),
    fc.boolean(),
    fc.integer({ min: -1, max: 1 }),
  );

  it('keeps every tick property, ends next to powers of ten included', () => {
    fc.assert(
      fc.property(
        fc.double({ min: -300, max: 300, noNaN: true }),
        fc.double({ min: 0.005, max: 300, noNaN: true }),
        fc.integer({ min: 1, max: 30 }),
        ends,
        (e, w, count, [sa, na, sb, nb]) => {
          const [a, b] = [end(e, sa, na), end(Math.min(e + w, 307), sb, nb)];
          const [lo, hi] = a < b ? [a, b] : [b, a];
          // Two ends snapped to one power of ten meet the doubles' resolution.
          wellFormed(logScale([hi, lo], [0, 1], M).ticks(count), lo, hi, count, hi - lo < 1e-11 * hi ? 2 : 0);
        },
      ),
    );
  });

  // Such a domain holds at least 18 ticks of {1..9}, so counts below 36 never take the half rule.
  it('starts within a decade of a domain a hundredfold wide whose powers of ten fit the count', () => {
    fc.assert(
      fc.property(
        fc.double({ min: -300, max: 280, noNaN: true }),
        fc.double({ min: 2, max: 27, noNaN: true }),
        fc.integer({ min: 1, max: 30 }),
        ends,
        (e, w, count, [sa, na, sb, nb]) => {
          const [lo, hi] = [end(e, sa, na), end(e + w, sb, nb)];
          let powers = 0;
          for (let p = Math.floor(e) - 1; p <= Math.ceil(e + w) + 1; p++) {
            const v = Number(`1e${p}`);
            if (v >= lo && v <= hi) powers++;
          }
          fc.pre(hi >= 100 * lo && powers <= count);
          expect(logScale([lo, hi], [0, 1], M).ticks(count)[0]).toBeLessThanOrEqual(10 * lo);
        },
      ),
    );
  });
});

describe('the value contract', () => {
  /** Ends a few doubles apart anywhere, subnormal ones included, or far apart, in either order. */
  const side = fc
    .tuple(
      fc.double({ noNaN: true, noDefaultInfinity: true }),
      fc.oneof(fc.integer({ min: 0, max: 4 }), fc.double({ min: -1e300, max: 1e300, noNaN: true })),
      fc.boolean(),
    )
    .map(([a, w, flip]): [number, number] => {
      let b = a;
      if (Number.isInteger(w) && Math.abs(w) <= 4)
        for (let i = 0; i < w; i++) b += Math.max(Math.abs(b) * 2 ** -52, Number.MIN_VALUE);
      else b = a + w;
      return flip ? [b, a] : [a, b];
    })
    .filter(([a, b]) => Number.isFinite(b - a));
  const values = fc.array(fc.double({ noNaN: true, noDefaultInfinity: true }), {
    minLength: 2,
    maxLength: 8,
  });
  const sign = ([a, b]: readonly [number, number]): number => Math.sign(b - a);

  /** Never NaN, and monotone in the direction the two sides give (constant where one is degenerate). */
  function monotone(f: (v: number) => number, vs: number[], dir: number): void {
    const out = [...vs].sort((p, q) => p - q).map(f);
    out.forEach((v, i) => {
      expect(Number.isNaN(v)).toBe(false);
      const prev = out[i - 1] ?? v;
      expect(v === prev || dir * (v - prev) > 0).toBe(true);
    });
  }

  it('refuses a value that is not finite with its own error', () => {
    const point = linearScale([3, 3], [0, 1]);
    const log = logScale([1, 1000], [0, 300], M);
    for (const s of [linearScale([0, 10], [300, 0]), point, log, logScale([5, 5], [2, 2], M)])
      for (const v of REFUSED) {
        expect(() => s.map(v)).toThrow(new RangeError('a scale maps finite values only'));
        expect(() => s.invert(v)).toThrow(new RangeError('a scale inverts finite values only'));
      }
    expect(() => log.map(-1)).toThrow(new RangeError('a log scale maps positive values only'));
  });

  it('maps every finite value to a number, monotone, ends exact, on narrow and wide sides', () => {
    fc.assert(
      fc.property(side, side, values, values, (d, r, xs, ys) => {
        const s = linearScale(d, r);
        const dir = sign(d) * sign(r);
        monotone((x) => s.map(x), xs, dir);
        monotone((y) => s.invert(y), ys, dir);
        // Exact up to the sign of a zero: lerp(-0, b, 0) is 0.
        if (d[0] !== d[1] && r[0] !== r[1])
          for (const [got, want] of [
            [s.map(d[0]), r[0]],
            [s.map(d[1]), r[1]],
            [s.invert(r[0]), d[0]],
            [s.invert(r[1]), d[1]],
          ])
            expect(got === want).toBe(true);
      }),
      { numRuns: 2000 },
    );
  });

  it('meets lerp without a step where the fraction overflows', () => {
    // On [0, w], t reaches the largest double at x = w·MAX_VALUE; x walks the doubles across it.
    fc.assert(
      fc.property(fc.double({ min: Number.MIN_VALUE, max: 0.5, noNaN: true }), side, (w, r) => {
        const s = linearScale([0, w], r);
        const seam = w * MAX;
        const xs = Array.from({ length: 41 }, (_, i) => nudge(seam, i - 20));
        monotone((x) => s.map(x), xs, sign(r));
      }),
    );
  });

  it('maps a narrow domain onto itself as the identity, the fraction overflowing or not', () => {
    fc.assert(
      fc.property(side, fc.double({ noNaN: true, noDefaultInfinity: true }), ([a, b], x) => {
        fc.pre(a !== b);
        const got = linearScale([a, b], [a, b]).map(x);
        // Within its error of MAX_VALUE a rounding may overflow: [0, 1.5e-323] takes -MAX_VALUE to -Infinity.
        if (!Number.isFinite(got))
          expect(got === Math.sign(x) * Infinity && Math.abs(x) > MAX * (1 - 4 * U)).toBe(true);
        else expect(Math.abs(got - x)).toBeLessThanOrEqual(4 * U * (Math.abs(x) + Math.abs(a) + Math.abs(b)));
      }),
      { numRuns: 1000 },
    );
    const tiny = linearScale([0, Number.MIN_VALUE], [0, Number.MIN_VALUE]);
    expect([1, -MAX, MAX].map((x) => tiny.map(x))).toEqual([1, -MAX, MAX]);
    expect(linearScale([0, 1e-300], [0, 1e-300]).map(1e10)).toBe(1e10);
  });

  it('gives a signed infinity only beyond the doubles, and finite values past an overflowing fraction', () => {
    const up1 = nudge(1, 1);
    const narrow = linearScale([1, up1], [0, 400]);
    expect([narrow.map(1e300), narrow.map(-1e300), narrow.map(2)]).toEqual([
      Infinity,
      -Infinity,
      400 * 2 ** 52,
    ]);
    const reversed = linearScale([up1, 1], [300, 0]);
    expect([reversed.map(1e300), reversed.map(-1e300)]).toEqual([Infinity, -Infinity]);
    // Fraction 1e310, range one ulp of 5 wide (2^-50): 2^-50·1e310 is finite.
    const both = linearScale([0, 1e-300], [5, nudge(5, 1)]);
    expect(both.map(1e10) / (2 ** -50 * 1e300 * 1e10)).toBeCloseTo(1, 14);
    expect(linearScale([0, 1e-323], [5, 5]).map(1e10)).toBe(5);
    const flat = linearScale([0, 10], [0, Number.MIN_VALUE]);
    expect([flat.invert(1), flat.invert(-1), flat.invert(1e-320)]).toEqual([Infinity, -Infinity, 20240]);
  });

  it('inverts a log scale across the whole doubles, by thirds where e^a alone leaves them', () => {
    const wide = logScale([Number.MIN_VALUE, MAX], [0, 400], M);
    for (const s of [wide, logScale([MAX, Number.MIN_VALUE], [400, 0], M)]) {
      expect(s.invert(196) / 1.4409230854397906e-14).toBeCloseTo(1, 10);
      expect(s.invert(204) / 0.06163954403083494).toBeCloseTo(1, 10);
    }
    expect([wide.invert(600), wide.invert(-200), wide.map(MAX), wide.map(Number.MIN_VALUE)]).toEqual([
      Infinity,
      0,
      400,
      0,
    ]);
    const flat = logScale([1, 1000], [0, Number.MIN_VALUE], M);
    expect([flat.invert(1), flat.invert(-1)]).toEqual([Infinity, 0]);
    expect(logScale([5, 5], [0, 1e-323], M).invert(1e10)).toBe(5);
    fc.assert(
      fc.property(side, side, values, ([a, b], r, ys) => {
        const [d0, d1] = [Math.abs(a) || 1, Math.abs(b) || 1];
        const s = logScale([d0, d1], r, M);
        for (const y of ys) expect(Number.isNaN(s.invert(y)) || s.invert(y) < 0).toBe(false);
        for (const x of ys.map(Math.abs).filter((v) => v > 0)) expect(Number.isNaN(s.map(x))).toBe(false);
        // Monotone across the middle, where the invert changes the end it starts from; ends exact.
        const mid = r[0] / 2 + r[1] / 2;
        const walk = Array.from({ length: 21 }, (_, i) => mid + (i - 10) * U * Math.abs(mid));
        monotone((y) => s.invert(y), [...ys, ...walk.filter(Number.isFinite)], sign([d0, d1]) * sign(r));
        if (d0 !== d1 && r[0] !== r[1]) expect([s.invert(r[0]), s.invert(r[1])]).toEqual([d0, d1]);
      }),
      { numRuns: 1000 },
    );
  });
});

// Tolerances [measured, 9 October 2026]: ticks exactly the Fraction twin's; refusals and infinities exactly;
// other maps and inverts within 4 units (measured at most 2.6), a unit being u(|a| + |b|)max(1, |t|) for an
// affine map onto [a, b] at t, u = 2^-53, the log map's included, and the log invert's relative error
// u(1 + S max(1, |t|)), S = |ln(d1 / d0)|, which exp(tS) cannot beat.
describe('parity with the Fraction and mpmath twin (tools/zqverify/scale.py)', () => {
  /** (v - a) / (b - a) without overflow; 0.5 where a = b. */
  const at = (v: number, a: number, b: number): number =>
    a === b ? 0.5 : Number.isFinite(v - a) ? (v - a) / (b - a) : (v / 2 - a / 2) / ((b - a) / 2);
  /** u(|a| + |b|)max(1, |t|) for the affine value v onto [a, b], computed without overflow. */
  const unit = (v: number, a: number, b: number): number => {
    const half = Math.abs(a) / 2 + Math.abs(b) / 2;
    if (a === b) return 2 * U * half;
    const gap = Number.isFinite(v - a) ? Math.abs(v - a) : 2 * Math.abs(v / 2 - a / 2);
    return 2 * U * Math.max(half, (half / Math.abs(b - a)) * gap);
  };
  function agrees(got: () => number, want: Value | null, bound: (want: number) => number, why: string): void {
    if (want === null) {
      expect(got, why).toThrow(/^a scale (maps|inverts) finite values only$|^a log scale maps positive/);
      return;
    }
    const [g, w] = [got(), Number(want)];
    // Infinities and zeros exactly, up to the sign of a zero.
    if (!Number.isFinite(w) || w === 0 || !Number.isFinite(g))
      expect(g === w, `${why}: ${g}, ${w}`).toBe(true);
    else expect(Math.abs(g - w), why).toBeLessThanOrEqual(bound(w));
  }

  it(`agrees on all ${golden.length} golden scales`, () => {
    for (const g of golden) {
      const scale: Scale =
        g.kind === 'linear' ? linearScale(g.domain, g.range) : logScale(g.domain, g.range, M);
      const why = JSON.stringify([g.domain, g.range]);
      expect(scale.ticks(g.count), why).toEqual(g.ticks);
      const [[d0, d1], [r0, r1]] = [g.domain, g.range];
      // Where d1 / d0 leaves the doubles, |ln d0| + |ln d1| bounds S from above.
      const ln = Math.log(d1 / d0);
      const S = Number.isFinite(ln) ? Math.abs(ln) : Math.abs(Math.log(d0)) + Math.abs(Math.log(d1));
      g.x.forEach((x, i) => {
        agrees(
          () => scale.map(Number(x)),
          g.map[i] ?? null,
          (w) => 4 * unit(w, r0, r1),
          why,
        );
      });
      g.y.forEach((y, i) => {
        const v = Number(y);
        const bound =
          g.kind === 'linear'
            ? (w: number) => 4 * unit(w, d0, d1)
            : (w: number) => 4 * U * Math.abs(w) * (1 + (S && S * Math.max(1, Math.abs(at(v, r0, r1)))));
        agrees(() => scale.invert(v), g.invert[i] ?? null, bound, why);
      });
    }
  });
});
