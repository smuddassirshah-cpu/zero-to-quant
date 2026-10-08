import { readFileSync } from 'node:fs';
import { exp, expm1, log, log1p, tanh } from '@zq/mathcore/dmath';
import fc from 'fast-check';
import { describe, expect, it } from 'vitest';
import { evaluate, parseGoldens, renderBits, withinTolerance } from './dmath-goldens.ts';

const goldens = parseGoldens(readFileSync(new URL('./dmath.goldens.txt', import.meta.url), 'utf8'));
const functions = { exp, log, log1p, expm1, tanh };
const names = Object.keys(functions);

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
  ])('special value %#', (got, want) => {
    expect(Object.is(got, want)).toBe(true);
  });
});

// Any double, NaN, infinities, signed zeros and subnormals included.
const anyDouble = fc.double();

describe('properties', () => {
  it('tanh is odd to the bit and stays in [-1, 1]', () => {
    fc.assert(
      fc.property(anyDouble, (x) => {
        expect(Object.is(tanh(-x), -tanh(x))).toBe(true);
        if (!Number.isNaN(x)) expect(Math.abs(tanh(x))).toBeLessThanOrEqual(1);
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
});
