import { readFileSync } from 'node:fs';
import fc from 'fast-check';
import { describe, expect, it } from 'vitest';
import * as S from '@zq/mathcore/stats';

interface Golden {
  xs: number[];
  sum: number | null;
  mean: number | null;
  variance: [number | null, number | null];
  sd: [number | null, number | null];
  median: number;
  linear: number[];
  inclusive: number[];
  gcse: number[];
  quartiles: [number[] | null, number[] | null];
}

const golden = readFileSync(new URL('stats.golden.jsonl', import.meta.url), 'utf8')
  .split('\n')
  .filter(Boolean)
  .map((line) => JSON.parse(line) as Golden);
const PS = [0, 0.1, 0.25, 0.37, 0.5, 0.75, 0.9, 1];
const U = 2 ** -53;
const KINDS = ['sample', 'population'] as const;

/** Distance in units in the last place: adjacent doubles are 1 apart, and -0 and 0 are 0 apart. */
function ulps(a: number, b: number): number {
  const ordinal = (x: number): bigint => {
    const view = new DataView(new ArrayBuffer(8));
    view.setFloat64(0, x);
    const i = view.getBigInt64(0);
    return i < 0n ? -(i & 0x7fffffffffffffffn) : i;
  };
  const d = ordinal(a) - ordinal(b);
  return Number(d < 0n ? -d : d);
}

const data = fc.array(fc.double({ min: -1e6, max: 1e6, noNaN: true }), { minLength: 1, maxLength: 30 });
const gcseSet = [3, 7, 8, 12, 15, 18, 21, 22, 30, 41];

describe('sum and mean', () => {
  it('round the exact sum once, ties to even across partials', () => {
    expect(S.sum([])).toBe(0);
    expect(S.sum(Array<number>(10).fill(0.1))).toBe(1);
    expect(S.sum([1e-16, 1, 1e16])).toBe(10000000000000002);
    expect(S.sum([1e100, 1, -1e100, 1e-100])).toBe(1);
    expect(S.sum(new Float64Array([0.5, 0.25]))).toBe(0.75);
    expect([S.mean([0.1, 0.1, 0.1]), S.mean([-0.1, -0.1, -0.1])]).toEqual([0.1, -0.1]);
    expect(S.sum([0.1, 0.1, 0.1]) / 3).toBe(0.10000000000000002);
  });

  it('refuse missing, NaN and infinite values, and an overflowing sum', () => {
    expect(() => S.mean([])).toThrow(RangeError);
    for (const bad of [NaN, Infinity, -Infinity]) expect(() => S.sum([1, bad])).toThrow(RangeError);
    expect(() => S.sum([1.7e308, 1.7e308, -1.7e308])).toThrow('the sum overflows');
  });

  it('do not depend on order, and the mean lies between the extremes', () => {
    const shuffled = data.chain((xs) =>
      fc.tuple(fc.constant(xs), fc.shuffledSubarray(xs, { minLength: xs.length, maxLength: xs.length })),
    );
    fc.assert(
      fc.property(shuffled, ([xs, ys]) => {
        expect(S.sum(ys)).toBe(S.sum(xs));
        expect(S.sum([...xs, ...xs.map((x) => -x)])).toBe(0);
        const m = S.mean(xs);
        expect(m >= Math.min(...xs) && m <= Math.max(...xs)).toBe(true);
      }),
    );
  });
});

describe('variance and sd', () => {
  it('divide by n - 1 or n, and need two values for a sample', () => {
    expect(S.variance([1, 2, 3, 4], 'sample')).toBe(5 / 3);
    expect(S.variance([1, 2, 3, 4], 'population')).toBe(1.25);
    expect(S.variance([7], 'population')).toBe(0);
    expect(() => S.variance([7], 'sample')).toThrow(RangeError);
    expect(S.sd([2, 4, 4, 4, 5, 5, 7, 9], 'population')).toBe(2);
  });

  it('scale by powers of two at both ends of the doubles', () => {
    expect(S.sd([1e300, -1e300], 'population')).toBe(1e300);
    expect(() => S.variance([1e300, -1e300], 'population')).toThrow('the variance overflows');
    expect(S.sd([0, 1e-320], 'population')).toBe(1e-320 / 2);
  });

  it('are non-negative, sd is the root, and integer data shifted exactly keeps them within 2 ulp', () => {
    const ints = fc.array(fc.integer({ min: -(2 ** 20), max: 2 ** 20 }), { minLength: 2, maxLength: 30 });
    fc.assert(
      fc.property(ints, fc.integer({ min: -(2 ** 30), max: 2 ** 30 }), (xs, c) => {
        const shifted = xs.map((x) => x + c);
        for (const kind of KINDS) {
          const v = S.variance(xs, kind);
          expect(v).toBeGreaterThanOrEqual(0);
          expect(S.sd(xs, kind)).toBe(Math.sqrt(v));
          expect(ulps(S.variance(shifted, kind), v)).toBeLessThanOrEqual(2);
        }
      }),
    );
  });
});

describe('lerp', () => {
  it('is exact at the ends, monotone in t, and survives a span beyond the doubles', () => {
    expect(S.lerp(-1.7e308, 1.7e308, 0.5)).toBe(0);
    fc.assert(
      fc.property(
        fc.double({ noNaN: true, noDefaultInfinity: true }),
        fc.double({ noNaN: true, noDefaultInfinity: true }),
        fc.double({ min: 0, max: 1, noNaN: true }),
        fc.double({ min: 0, max: 1, noNaN: true }),
        (a, b, s, t) => {
          expect(S.lerp(a, b, 0) === a && S.lerp(a, b, 1) === b).toBe(true);
          const [lo, hi] = s <= t ? [s, t] : [t, s];
          const step = Math.sign(b - a) * (S.lerp(a, b, hi) - S.lerp(a, b, lo));
          expect(step).toBeGreaterThanOrEqual(0);
        },
      ),
    );
  });
});

describe('quantiles', () => {
  it('follow both conventions of drl.pre.summary-stats: the same median, different quartiles', () => {
    expect(S.quartiles(gcseSet, 'inclusive')).toEqual([9, 16.5, 21.75]);
    expect(S.quartiles(gcseSet, 'gcse')).toEqual([7.75, 16.5, 24]);
    expect(S.median(gcseSet)).toBe(16.5);
    expect(S.median([5, 1, 3])).toBe(3);
  });

  it('take the end value where the GCSE position leaves the data', () => {
    expect(S.quartiles([1, 2], 'gcse')).toEqual([1, 1.5, 2]);
    expect(S.quantile([4], 0.9, 'gcse')).toBe(4);
  });

  it('refuse p outside [0, 1], NaN, and no data', () => {
    for (const p of [-0.01, 1.01, NaN]) expect(() => S.quantile([1, 2], p, 'inclusive')).toThrow(RangeError);
    expect(() => S.quartiles([], 'gcse')).toThrow(RangeError);
  });

  it('are monotone in p, inside the data, and the extremes at 0 and 1', () => {
    const p = fc.double({ min: 0, max: 1, noNaN: true });
    fc.assert(
      fc.property(data, p, p, fc.constantFrom('inclusive', 'gcse'), (xs, s, t, method: S.QuantileMethod) => {
        const [lo, hi] = s <= t ? [s, t] : [t, s];
        expect(S.quantile(xs, lo, method)).toBeLessThanOrEqual(S.quantile(xs, hi, method));
        expect(S.quantile(xs, 0, method)).toBe(Math.min(...xs));
        expect(S.quantile(xs, 1, method)).toBe(Math.max(...xs));
        expect(S.quartiles(xs, method)).toEqual([0.25, 0.5, 0.75].map((q) => S.quantile(xs, q, method)));
      }),
    );
  });
});

// Tolerances [measured on these goldens, 8 October 2026]: sum, mean and 'inclusive' against NumPy exact;
// variance and sd within 2 ulp of statistics (measured 2 and 1); against exact Fractions within u·M at quartile
// positions and n·u·M elsewhere (measured 1 and 0.58n), with u = 2^-53 and M the largest |x|; the median and
// statistics.quantiles within u·M and 2u·M (measured 1 and 1.88).
describe('parity with statistics, NumPy and Fraction (tools/zqverify/stats.py)', () => {
  const attempt = (f: () => number): number | null => {
    try {
      return f();
    } catch (error) {
      if (error instanceof RangeError) return null;
      throw error;
    }
  };

  it(`agrees on all ${golden.length} golden data sets`, () => {
    for (const g of golden) {
      const n = g.xs.length;
      const unit = Math.max(U * Math.max(...g.xs.map(Math.abs)), Number.MIN_VALUE);
      const near = (got: number, want: number, units: number): void => {
        expect(
          Math.abs(got - want),
          `${got} against ${want} for ${JSON.stringify(g.xs)}`,
        ).toBeLessThanOrEqual(units * unit);
      };
      expect([attempt(() => S.sum(g.xs)), attempt(() => S.mean(g.xs))]).toEqual([g.sum, g.mean]);
      KINDS.forEach((kind, i) => {
        for (const [f, want] of [
          [S.variance, g.variance[i] ?? null],
          [S.sd, g.sd[i] ?? null],
        ] as const) {
          const got = attempt(() => f(g.xs, kind));
          if (got === null || want === null) expect(got).toBe(want);
          else expect(ulps(got, want)).toBeLessThanOrEqual(2);
        }
      });
      near(S.median(g.xs), g.median, 1);
      PS.forEach((p, i) => {
        const units = Number.isInteger(4 * p) ? 1 : n;
        expect(S.quantile(g.xs, p, 'inclusive')).toBe(g.linear[i]);
        near(S.quantile(g.xs, p, 'inclusive'), g.inclusive[i] ?? NaN, units);
        near(S.quantile(g.xs, p, 'gcse'), g.gcse[i] ?? NaN, units);
      });
      (['inclusive', 'gcse'] as const).forEach((method, i) => {
        const want = g.quartiles[i];
        if (want)
          S.quartiles(g.xs, method).forEach((q, j) => {
            near(q, want[j] ?? NaN, 2);
          });
      });
    }
  });
});
