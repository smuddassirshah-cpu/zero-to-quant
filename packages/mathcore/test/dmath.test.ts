import { readFileSync } from 'node:fs';
import { exp, expm1, log, log1p, tanh } from '@zq/mathcore/dmath';
import fc from 'fast-check';
import { describe, expect, it } from 'vitest';
import { type Case, evaluate, parseGoldens, renderBits, withinTolerance } from './dmath-goldens.ts';

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

// e_exp.c's reduction rounds e^1 one ulp high; dmath returns Math.E's double, as V8 does.
it('exp(1) is e correctly rounded', () => {
  expect(exp(1)).toBe(2.718281828459045);
});

describe('the tolerance rule', () => {
  const at = (reference: number, rem = 0): Case => ({ fn: 'exp', index: 0, args: [0], reference, rem });

  it.each([
    [at(-5e-324), 0, false],
    [at(5e-324), -0, false],
    [at(-0), 0, false],
    [at(-5e-324), -0, true],
    [at(5e-324), 0, true],
    [at(0), 0, true],
    [at(1e-310), 1e-310 + 5e-324, true],
    [at(1e-310), 1e-310 + 1e-323, false],
    [at(1), 1 + 2 ** -52, true],
    [at(1, 500), 1 + 2 ** -50 + 2 ** -51, false],
    [at(NaN), NaN, true],
    [at(Infinity), 1.7976931348623157e308, false],
  ])('case %#', (c, y, want) => {
    expect(withinTolerance(c, y)).toBe(want);
  });
});

// fdlibm's working range of each function, drawn like tools/zqverify/dmath.py's `span`: the binary exponent
// uniform, the significand's 52 bits random. A draw from fc.double() is uniform over the bit patterns, so it
// lands mostly where these functions overflow, underflow or return x [measured, adversarial review of
// 8 October 2026]; it is kept for the special-value sweep only.
const bitsView = new DataView(new ArrayBuffer(8));

function span(eMin: number, eMax: number, signs: readonly boolean[] = [false, true]): fc.Arbitrary<number> {
  const significand = fc.bigInt({ min: 0n, max: (1n << 52n) - 1n });
  return fc
    .tuple(fc.constantFrom(...signs), fc.integer({ min: eMin, max: eMax }), significand)
    .map(([neg, e, m]) => {
      bitsView.setBigUint64(0, (BigInt(e + 1023) << 52n) | m);
      const x = bitsView.getFloat64(0);
      return neg ? -x : x;
    });
}

const within = (lo: number, hi: number) => (x: number) => x >= lo && x <= hi;
const working: Readonly<Record<keyof typeof functions, fc.Arbitrary<number>>> = {
  exp: span(-60, 9).filter(within(-746, 710)),
  expm1: span(-60, 9).filter(within(-746, 710)),
  log: fc.oneof(
    span(-1022, 1023, [false]),
    span(-52, -1).map((d) => 1 + d),
  ),
  log1p: fc.oneof(
    span(-30, 60, [false]),
    span(-30, -1, [true]),
    span(-53, -1, [false]).map((d) => -1 + d),
  ),
  tanh: span(-30, 4).filter(within(-22, 22)),
};
const RUNS = { numRuns: 1000 };

// V8's Math functions are fdlibm ports too [sourced: V8 12.4.254, src/base/ieee754.cc]; both are within about
// 1 ulp of the true value, so they agree within 1e-15 relative for a normal result, and within 2^-1073 below.
function agrees(name: string, got: number, x: number): void {
  const want = (Math as unknown as Record<string, (v: number) => number>)[name]?.(x) ?? NaN;
  if (Number.isNaN(want) || !Number.isFinite(want) || Math.abs(want) < 2.2250738585072014e-308) {
    expect(Object.is(got, want) || Math.abs(got - want) <= 1e-323).toBe(true);
  } else expect(Math.abs(got - want) / Math.abs(want)).toBeLessThanOrEqual(1e-15);
}

describe('properties over each working range', () => {
  it('tanh is odd to the bit and stays in [-1, 1]', () => {
    fc.assert(
      fc.property(working.tanh, (x) => {
        expect(Object.is(tanh(-x), -tanh(x))).toBe(true);
        expect(Math.abs(tanh(x))).toBeLessThanOrEqual(1);
      }),
      RUNS,
    );
  });

  it.each(names)('%s agrees with the engine within 1e-15 relative', (name) => {
    const f = functions[name as keyof typeof functions];
    fc.assert(
      fc.property(working[name as keyof typeof functions], (x) => {
        agrees(name, f(x), x);
      }),
      RUNS,
    );
  });

  // exp's relative error becomes an absolute error of at most 2^-52 in log, beside log's own 1 ulp.
  it('log inverts exp within 1e-15 relative to max(1, |x|)', () => {
    fc.assert(
      fc.property(span(-40, 9).filter(within(-700, 700)), (x) => {
        expect(Math.abs(log(exp(x)) - x)).toBeLessThanOrEqual(1e-15 * Math.max(1, Math.abs(x)));
      }),
      RUNS,
    );
  });
});

describe('the special-value sweep over every double', () => {
  // NaN, the infinities, signed zeros and subnormals included.
  const anyDouble = fc.double();

  it('tanh stays odd to the bit and every function agrees with the engine', () => {
    fc.assert(
      fc.property(fc.constantFrom(...names), anyDouble, (name, x) => {
        expect(Object.is(tanh(-x), -tanh(x))).toBe(true);
        agrees(name, functions[name as keyof typeof functions](x), x);
      }),
      RUNS,
    );
  });
});
