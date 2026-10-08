import { readFileSync } from 'node:fs';
import fc from 'fast-check';
import { describe, expect, it } from 'vitest';
import { linearScale, logScale, type Scale } from '@zq/mathcore/scale';

interface Golden {
  kind: 'linear' | 'log';
  domain: [number, number];
  range: [number, number];
  count: number;
  ticks: number[];
  x: number[];
  map: number[];
  y: number[];
  invert: number[];
}

const golden = readFileSync(new URL('scale.golden.jsonl', import.meta.url), 'utf8')
  .split('\n')
  .filter(Boolean)
  .map((line) => JSON.parse(line) as Golden);
// The engine's own functions stand in for dmath until it merges; tests are not graded paths.
const M = { log: Math.log, exp: Math.exp };
const U = 2 ** -53;
const most = (count: number): number => Math.floor(1.59 * Math.max(count, 2)) + 1;

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

  it('defines degenerate domains and ranges', () => {
    const point = linearScale([3, 3], [0, 100]);
    expect([point.map(3), point.map(-7), point.invert(20)]).toEqual([50, 50, 3]);
    expect(point.ticks(5)).toEqual([3]);
    const flat = linearScale([0, 8], [7, 7]);
    expect([flat.map(1), flat.invert(7), flat.invert(0)]).toEqual([7, 4, 4]);
  });

  it('refuses non-finite ends or spans and counts that are not positive integers', () => {
    expect(() => linearScale([0, NaN], [0, 1])).toThrow(RangeError);
    expect(() => linearScale([-1.7e308, 1.7e308], [0, 1])).toThrow(RangeError);
    expect(() => linearScale([0, 1], [0, Infinity])).toThrow(RangeError);
    for (const count of [0, 1.5, NaN]) expect(() => y.ticks(count)).toThrow(RangeError);
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
    expect(s.ticks(10)).toEqual([1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]);
    expect(s.ticks(4)).toEqual([1, 10, 100, 1000]);
    expect(s.ticks(3)).toEqual([1, 100]);
    expect(logScale([1e-300, 1e300], [0, 1], M).ticks(10)).toEqual(
      [-300, -200, -100, 0, 100, 200, 300].map((p) => Number(`1e${p}`)),
    );
    expect(logScale([3, 2], [0, 1], M).ticks(5)).toEqual([2, 2.2, 2.4, 2.6, 2.8, 3]);
    expect(logScale([20, 60], [0, 1], M).ticks(2)).toEqual([20, 50]);
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

  it('keeps every tick property', () => {
    fc.assert(
      fc.property(
        fc.double({ min: -300, max: 300, noNaN: true }),
        fc.double({ min: 0.005, max: 300, noNaN: true }),
        fc.integer({ min: 1, max: 30 }),
        (e, w, count) => {
          const [lo, hi] = [10 ** e, 10 ** Math.min(e + w, 307)];
          wellFormed(logScale([hi, lo], [0, 1], M).ticks(count), lo, hi, count);
        },
      ),
    );
  });
});

// Tolerances [measured, 8 October 2026]: ticks exactly the Fraction twin's; maps and inverts within 4 units
// (measured at most 2.6), a unit being u(|a| + |b|)max(1, |t|) for an affine map onto [a, b] at t, u = 2^-53,
// times 1 + (|ln x| + |ln d0| + |ln d1|) / |ln d1 - ln d0| for the log map, and the log invert's relative
// error u(1 + (|ln d0| + |ln d1|)max(1, |t|)), each set by the rounding of its steps.
describe('parity with the Fraction and mpmath twin (tools/zqverify/scale.py)', () => {
  it(`agrees on all ${golden.length} golden scales`, () => {
    for (const g of golden) {
      const scale: Scale =
        g.kind === 'linear' ? linearScale(g.domain, g.range) : logScale(g.domain, g.range, M);
      expect(scale.ticks(g.count), JSON.stringify(g.domain)).toEqual(g.ticks);
      const [[d0, d1], [r0, r1]] = [g.domain, g.range];
      const [l0, l1] = [Math.log(d0), Math.log(d1)];
      const at = (v: number, a: number, b: number): number => (a === b ? 0.5 : (v - a) / (b - a));
      g.x.forEach((x, i) => {
        const t = g.kind === 'linear' ? at(x, d0, d1) : at(Math.log(x), l0, l1);
        const k =
          g.kind === 'linear' || l0 === l1
            ? 1
            : 1 + (Math.abs(Math.log(x)) + Math.abs(l0) + Math.abs(l1)) / Math.abs(l1 - l0);
        expect(Math.abs(scale.map(x) - (g.map[i] ?? NaN))).toBeLessThanOrEqual(
          4 * U * (Math.abs(r0) + Math.abs(r1)) * Math.max(1, Math.abs(t)) * k,
        );
      });
      g.y.forEach((y, i) => {
        const [got, want, t] = [scale.invert(y), g.invert[i] ?? NaN, at(y, r0, r1)];
        const bound =
          g.kind === 'linear'
            ? 4 * U * (Math.abs(d0) + Math.abs(d1)) * Math.max(1, Math.abs(t))
            : 4 * U * Math.abs(want) * (1 + (Math.abs(l0) + Math.abs(l1)) * Math.max(1, Math.abs(t)));
        expect(Math.abs(got - want)).toBeLessThanOrEqual(bound);
      });
    }
  });
});
