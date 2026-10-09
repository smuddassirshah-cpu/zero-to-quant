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
  median: number | null;
  linear: (number | null)[];
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
// The bounds below are first order in u; the 1% margin covers the dropped u² terms and Sum2's γ² ≈ (nu)² for
// n < 10^6.
const MARGIN = 1.01;

// The derived bounds on |variance - reference| and |sd - reference| for a correctly rounded reference, given
// E, the bound on the mean's error (the parity suite's notes). The products are ordered so that no step
// overflows where the bound is a double.
function varianceSlack(want: number, meanBound: number, n: number, divisor: number): number {
  const shift = meanBound * (meanBound * ((7 * U * n) / divisor));
  return MARGIN * (7 * U * Math.abs(want) + shift) + Number.MIN_VALUE;
}

function sdSlack(want: number, meanBound: number, n: number, divisor: number): number {
  const root = meanBound * Math.sqrt((7 * U * n) / divisor);
  return (
    MARGIN * (5 * U * want + (want > 0 ? Math.min(root, root * (root / want)) : root)) + Number.MIN_VALUE
  );
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

  it('keep every partial: 38 values 54 bits apart outgrow the buffer of 32 and still sum exactly', () => {
    const spaced = Array.from({ length: 38 }, (_, k) => 2 ** (1023 - 54 * k));
    expect(S.sum(spaced)).toBe(2 ** 1023);
    expect(S.sum([...spaced].reverse())).toBe(2 ** 1023);
    expect(S.sum([...spaced, ...spaced.map((x) => -x), 2 ** -1074])).toBe(2 ** -1074);
  });

  it('refuse missing, NaN and infinite values, holes, and an overflowing sum', () => {
    expect(() => S.mean([])).toThrow(RangeError);
    for (const bad of [NaN, Infinity, -Infinity]) expect(() => S.sum([1, bad])).toThrow(RangeError);
    expect(() => S.mean(Array<number>(2))).toThrow('every value must be finite');
    expect(() => S.sum([1.7e308, 1.7e308, -1.7e308])).toThrow('the sum overflows');
    // The decision notes' choice: the mean of these is 2e-321, but the sum overflows on the way, as in fmean.
    expect(() => S.mean([1.7e308, 1.7e308, -1.7e308, -1.7e308, 1e-320])).toThrow('the sum overflows');
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

  it('scale by powers of two at both ends of the doubles, and throw where the result overflows', () => {
    expect(S.sd([1e300, -1e300], 'population')).toBe(1e300);
    expect(() => S.variance([1e300, -1e300], 'population')).toThrow('the variance overflows');
    expect(S.sd([0, 1e-320], 'population')).toBe(1e-320 / 2);
    expect(S.sd([-1.7e308, 1.7e308], 'population')).toBe(1.7e308);
    expect(() => S.sd([-1.7e308, 1.7e308], 'sample')).toThrow('the deviation overflows');
  });

  it('are non-negative, sd is the root, and both stay within the derived bound of the exact variance', () => {
    // k·step + offset is exact (at most 52 significant bits), as is the integer arithmetic below 2^53, so
    // `exact` is the exact variance rounded once. Dyadic data at 2^40 puts a spread of at most 2^11 nine orders
    // of magnitude below the offset, where only the correction keeps the variance.
    const ks = fc.array(fc.integer({ min: -(2 ** 20), max: 2 ** 20 }), { minLength: 2, maxLength: 30 });
    const offset = (lo: number, hi: number): fc.Arbitrary<number> =>
      fc.tuple(fc.integer({ min: lo, max: hi }), fc.constantFrom(1, -1)).map(([o, sign]) => sign * o);
    const frame = fc.oneof(
      fc.record({ step: fc.constant(1), offset: offset(0, 2 ** 30) }),
      fc.record({ step: fc.constant(2 ** -10), offset: offset(2 ** 39, 2 ** 40) }),
    );
    fc.assert(
      fc.property(ks, frame, (ks, { step, offset }) => {
        const xs = ks.map((k) => k * step + offset);
        const n = ks.length;
        const s = ks.reduce((a, k) => a + k, 0);
        const q = ks.reduce((a, k) => a + k * k, 0);
        const m = Math.max(...xs.map(Math.abs));
        for (const kind of KINDS) {
          const divisor = kind === 'sample' ? n - 1 : n;
          const exact = ((n * q - s * s) / (n * divisor)) * step * step;
          const v = S.variance(xs, kind);
          expect(v).toBeGreaterThanOrEqual(0);
          expect(S.sd(xs, kind)).toBe(Math.sqrt(v));
          expect(Math.abs(v - exact)).toBeLessThanOrEqual(varianceSlack(exact, 2 * U * m, n, divisor));
        }
      }),
    );
  });
});

describe('lerp', () => {
  it('refuses infinite and NaN ends and t, and extrapolates for any finite t', () => {
    for (const [a, b] of [
      [Infinity, 0],
      [0, -Infinity],
      [NaN, 1],
      [1, NaN],
      [1.7e308, Infinity],
    ] as const)
      expect(() => S.lerp(a, b, 0.5)).toThrow('lerp needs finite ends');
    for (const t of [Infinity, -Infinity, NaN])
      expect(() => S.lerp(1, 1, t)).toThrow('lerp needs a finite t');
    expect([S.lerp(1, 3, 2), S.lerp(1, 3, -1)]).toEqual([5, -1]);
  });

  it('gives ±Infinity where the result leaves the doubles, and halves the ends where only a step does', () => {
    expect([S.lerp(0, 1e308, 10), S.lerp(0, 1e308, -10), S.lerp(0, 1e308, 1.8)]).toEqual([
      Infinity,
      -Infinity,
      Infinity,
    ]);
    expect(S.lerp(-1e308, 1e308, 2)).toBe(Infinity);
    // (b - a)t = -2^1024 overflows; the result, -3·2^1022, does not.
    expect(S.lerp(2 ** 1022, 1.5 * 2 ** 1022, -8)).toBe(-3 * 2 ** 1022);
  });

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

// Tolerances, derived to first order in u = 2^-53 [inferred]; each reference is the exact value rounded once
// unless named. M is the largest |x|, unit = max(u·M, MIN_VALUE), n the count and D the divisor.
// - lerp rounds b - a (|b - a| ≤ 2M), the product with t and the sum, so for an exact t it errs by at most
//   (1 + 4·min(t, 1 - t))·u·M ≤ 3u·M. At a quartile position h is exact; with the reference's rounding that is
//   4 units. Elsewhere the rounded h moves the interpolant by up to 2M·|Δh|, with |Δh| ≤ (n - 1)u for
//   'inclusive' and (2n + 1)u for 'gcse' (two roundings): 2n + 2 and 4n + 6 units.
// - statistics.median rounds (a + b)/2 once (u·M) and lerp at 0.5 errs by 2u·M: 3 units. statistics.quantiles
//   rounds (a·(4 - δ) + b·δ)/4 to within 1.75u·M: with lerp, 4 units.
// - The corrected two-pass variance: with m = x̄ + e, Σ(x - m)² - (Σ(x - m))²/n is SS exactly. Rounding x - m
//   adds 2Σδ(x - m)(x - x̄) with |δ| ≤ u, at most u·(2·SS + n·e²) by Cauchy-Schwarz; the squares, the sums
//   (Sum2, exactly rounded to first order), the correction, the difference and the division bring it to
//   u·(6·SS + 7n·e²)/D. With |e| ≤ E = 2u·M and a correctly rounded reference, the variance is within
//   7u·V + 7u·n·E²/D (varianceSlack). Its root errs by 3u·σ, Math.sqrt and the reference add u·σ each, and
//   the e term moves it by at most min(√s, s/σ) with s = 7u·n·E²/D (sdSlack).
// - The slacks take E·(E·(7u·n/D)) and √s = E·√(7u·n/D), which never overflow where the bound is a double:
//   data that is not constant spreads over at least u·M/2 (a spread below M/2 keeps every member above M/2,
//   where doubles lie more than u·M/2 apart), so V ≥ u²M²/(8D) and the e term is at most 224u·n·V. For constant data the mean lies within two
//   roundings of the value x, so every x - m is the same small multiple of the spacing at x, exact by
//   Sterbenz's lemma, and for n < 10^7 every square and sum after it is exact: the variance is 0 and E = 0.
// - Within the slack of MAX_VALUE either side may overflow where the other rounds to MAX_VALUE (the decision
//   notes): a throw against a number, or a number against a reference that overflows, passes there only.
// - A subnormal result adds MIN_VALUE. On 20,000 fresh sets (stats.case on new seeds and seven adversarial
//   families, not committed) the largest error was 0.56 of its bound [measured, 8 October 2026]; the review's
//   cases that broke the earlier fitted tolerances (1.26·n units for 'gcse' at p = 0.37, 1.23 units at a
//   quartile, 3 ulp for a variance) are in the goldens.
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
      const m = Math.max(...g.xs.map(Math.abs));
      const meanBound = g.xs.every((x) => x === g.xs[0]) ? 0 : 2 * U * m;
      const unit = Math.max(U * m, Number.MIN_VALUE);
      const within = (got: number, want: number, slack: number): void => {
        expect(
          Math.abs(got - want),
          `${got} against ${want} for ${JSON.stringify(g.xs)}`,
        ).toBeLessThanOrEqual(slack);
      };
      const near = (got: number, want: number, units: number): void => {
        within(got, want, MARGIN * units * unit);
      };
      expect([attempt(() => S.sum(g.xs)), attempt(() => S.mean(g.xs))]).toEqual([g.sum, g.mean]);
      KINDS.forEach((kind, i) => {
        const divisor = kind === 'sample' ? n - 1 : n;
        for (const [f, want, slack] of [
          [S.variance, g.variance[i] ?? null, varianceSlack],
          [S.sd, g.sd[i] ?? null, sdSlack],
        ] as const) {
          const got = attempt(() => f(g.xs, kind));
          const edge = got ?? want;
          if (got !== null && want !== null) within(got, want, slack(want, meanBound, n, divisor));
          else if (edge !== null) within(Number.MAX_VALUE, edge, slack(edge, meanBound, n, divisor));
        }
      });
      if (g.median !== null) near(S.median(g.xs), g.median, 3);
      PS.forEach((p, i) => {
        const quartile = Number.isInteger(4 * p);
        const numpy = g.linear[i];
        // + 0 maps -0 to 0: a zero's sign follows NumPy's partition and lerp, not a convention.
        if (numpy !== null) expect(S.quantile(g.xs, p, 'inclusive') + 0).toBe((numpy ?? NaN) + 0);
        near(S.quantile(g.xs, p, 'inclusive'), g.inclusive[i] ?? NaN, quartile ? 4 : 2 * n + 2);
        near(S.quantile(g.xs, p, 'gcse'), g.gcse[i] ?? NaN, quartile ? 4 : 4 * n + 6);
      });
      (['inclusive', 'gcse'] as const).forEach((method, i) => {
        const want = g.quartiles[i];
        if (want)
          S.quartiles(g.xs, method).forEach((q, j) => {
            near(q, want[j] ?? NaN, 4);
          });
      });
    }
  });
});
