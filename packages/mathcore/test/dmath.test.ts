import { readFileSync } from 'node:fs';
import { cos, exp, expm1, log, log1p, pow, sin, tanh } from '@zq/mathcore/dmath';
import fc from 'fast-check';
import { describe, expect, it } from 'vitest';
import { evaluate, parseGoldens, renderBits, withinTolerance } from './dmath-goldens.ts';

const goldens = parseGoldens(readFileSync(new URL('./dmath.goldens.txt', import.meta.url), 'utf8'));
const functions = { exp, log, log1p, expm1, tanh, sin, cos };
const names = [...Object.keys(functions), 'pow'];

describe('dmath against 50-digit mpmath references', () => {
  it('reads 10,000 goldens over every function', () => {
    expect(goldens).toHaveLength(10_000);
    expect(new Set(goldens.map((c) => c.fn))).toEqual(new Set(names));
  });

  it.each(names)('%s is within tolerance on every golden', (name) => {
    const misses = goldens
      .filter((c) => c.fn === name && !withinTolerance(c, evaluate(c)))
      .map((c) => `${name} #${c.index} (${c.args.join(', ')}): ${evaluate(c)} against ${c.reference}`);
    expect(misses).toEqual([]);
  });

  it('reproduces the recorded bits of every result', async () => {
    await expect(renderBits(goldens)).toMatchFileSnapshot('./dmath.bits.txt');
  });
});

describe('special values (C99 Annex F)', () => {
  it.each([
    [exp(-Infinity), 0],
    [exp(-0), 1],
    [log(-0), -Infinity],
    [log(-1), NaN],
    [log(1), 0],
    [log1p(-1), -Infinity],
    [log1p(-0), -0],
    [expm1(-Infinity), -1],
    [expm1(-0), -0],
    [tanh(-Infinity), -1],
    [tanh(-0), -0],
    [sin(-0), -0],
    [sin(Infinity), NaN],
    [cos(-Infinity), NaN],
    [cos(-0), 1],
    [pow(1, NaN), 1],
    [pow(NaN, -0), 1],
    [pow(-1, Infinity), 1],
    [pow(-1, -Infinity), 1],
    [pow(-0, -3), -Infinity],
    [pow(-0, 3), -0],
    [pow(-0, 0.5), 0],
    [pow(-Infinity, -3), -0],
    [pow(-8, 1 / 3), NaN],
  ])('special value %#', (got, want) => {
    expect(Object.is(got, want)).toBe(true);
  });
});

// Any double, NaN, infinities, signed zeros and subnormals included.
const anyDouble = fc.double();

describe('properties', () => {
  it('sin and tanh are odd and cos is even, to the bit, and all three stay in [-1, 1]', () => {
    fc.assert(
      fc.property(anyDouble, (x) => {
        expect(Object.is(sin(-x), -sin(x))).toBe(true);
        expect(Object.is(tanh(-x), -tanh(x))).toBe(true);
        expect(Object.is(cos(-x), cos(x))).toBe(true);
        if (Number.isFinite(x))
          for (const v of [sin(x), cos(x), tanh(x)]) expect(Math.abs(v)).toBeLessThanOrEqual(1);
      }),
    );
  });

  // V8's Math functions are fdlibm ports too [recalled]; both are within 1 ulp of the true value, so they agree
  // within 2 ulps: 1e-15 relative for a normal result, 2^-1073 below.
  it('agrees with the engine within 1e-15 relative wherever the result is a normal double', () => {
    fc.assert(
      fc.property(fc.constantFrom(...Object.entries(functions)), anyDouble, ([name, f], x) => {
        const want = (Math as unknown as Record<string, (v: number) => number>)[name]?.(x) ?? NaN;
        const got = f(x);
        if (Number.isNaN(want) || !Number.isFinite(want) || Math.abs(want) < 2.2250738585072014e-308) {
          expect(Object.is(got, want) || Math.abs(got - want) <= 1e-323).toBe(true);
        } else expect(Math.abs(got - want) / Math.abs(want)).toBeLessThanOrEqual(1e-15);
      }),
      { numRuns: 2000 },
    );
  });

  // exp's relative error becomes an absolute error of at most 2^-52 in log, beside log's own 1 ulp.
  it('log inverts exp within 1e-15 relative to max(1, |x|)', () => {
    fc.assert(
      fc.property(fc.double({ min: -700, max: 700, noNaN: true }), (x) => {
        expect(Math.abs(log(exp(x)) - x)).toBeLessThanOrEqual(1e-15 * Math.max(1, Math.abs(x)));
      }),
    );
  });

  it('pow returns x, x * x and 1 / x for y = 1, 2 and -1, and 1 for y = 0', () => {
    fc.assert(
      fc.property(anyDouble, (x) => {
        expect(Object.is(pow(x, 1), x)).toBe(true);
        expect(Object.is(pow(x, 2), x * x)).toBe(true);
        expect(Object.is(pow(x, -1), 1 / x)).toBe(true);
        expect(pow(x, 0)).toBe(1);
      }),
    );
  });

  // fdlibm: "pow(integer, integer) always returns the correct integer provided it is representable" [sourced].
  it('pow of integers is exact while the result stays below 2^53', () => {
    const small = fc.tuple(fc.integer({ min: -3000, max: 3000 }), fc.integer({ min: 0, max: 4 }));
    const deep = fc.tuple(fc.integer({ min: -10, max: 10 }), fc.integer({ min: 5, max: 15 }));
    fc.assert(
      fc.property(fc.oneof(small, deep), ([a, n]) => {
        expect(pow(a, n)).toBe(Number(BigInt(a) ** BigInt(n)));
      }),
    );
  });

  it('pow agrees with the engine within 1e-15 relative for positive bases and normal results', () => {
    fc.assert(
      fc.property(
        fc.double({ min: 1e-300, max: 1e300, noNaN: true }),
        fc.double({ min: -64, max: 64 }),
        (x, y) => {
          const want = Math.pow(x, y);
          fc.pre(Number.isFinite(want) && want >= 2.2250738585072014e-308);
          expect(Math.abs(pow(x, y) - want) / want).toBeLessThanOrEqual(1e-15);
        },
      ),
      { numRuns: 2000 },
    );
  });
});
