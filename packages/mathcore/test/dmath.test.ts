import { readFileSync } from 'node:fs';
import { cos, exp, expm1, log, log1p, pow, sin, tanh } from '@zq/mathcore/dmath';
import fc from 'fast-check';
import { describe, expect, it } from 'vitest';
import { type Case, evaluate, parseGoldens, renderBits, withinTolerance } from './dmath-goldens.ts';

const goldens = parseGoldens(readFileSync(new URL('./dmath.goldens.txt', import.meta.url), 'utf8'));
const functions = { exp, log, log1p, expm1, tanh, sin, cos };
type Unary = keyof typeof functions;
const unary = Object.keys(functions) as Unary[];
const names = [...unary, 'pow'];

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
// sin and cos: the medium reduction below 2^20 pi/2, about 1.6e6, and Payne-Hanek above it.
const trig = fc.oneof(span(-30, 21), span(21, 1023));
const working: Readonly<Record<Unary, fc.Arbitrary<number>>> = {
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
  sin: trig,
  cos: trig,
};
const RUNS = { numRuns: 1000 };

// V8's Math functions are fdlibm ports too [sourced: V8 12.4.254, src/base/ieee754.cc]; both are within about
// 1 ulp of the true value, so they agree within 1e-15 relative for a normal result, and within 2^-1073 below.
function agrees(got: number, want: number): void {
  if (Number.isNaN(want) || !Number.isFinite(want) || Math.abs(want) < 2.2250738585072014e-308) {
    expect(Object.is(got, want) || Math.abs(got - want) <= 1e-323).toBe(true);
  } else expect(Math.abs(got - want) / Math.abs(want)).toBeLessThanOrEqual(1e-15);
}

const engine = (name: Unary, x: number): number =>
  (Math as unknown as Record<Unary, (v: number) => number>)[name](x);

describe('properties over each working range', () => {
  it('sin and tanh are odd and cos is even, to the bit, and all three stay in [-1, 1]', () => {
    fc.assert(
      fc.property(fc.oneof(working.tanh, trig), (x) => {
        expect(Object.is(sin(-x), -sin(x))).toBe(true);
        expect(Object.is(tanh(-x), -tanh(x))).toBe(true);
        expect(Object.is(cos(-x), cos(x))).toBe(true);
        for (const v of [sin(x), cos(x), tanh(x)]) expect(Math.abs(v)).toBeLessThanOrEqual(1);
      }),
      RUNS,
    );
  });

  it.each(unary)('%s agrees with the engine within 1e-15 relative', (name) => {
    fc.assert(
      fc.property(working[name], (x) => {
        agrees(functions[name](x), engine(name, x));
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

  // Positive bases over the normal doubles and near 1, exponents up to 2^10 in size, normal results. Larger
  // |y| near x = 1 is left to the goldens: there V8's Math.pow is off by up to hundreds of ulps.
  const base = fc.oneof(
    span(-1022, 1023, [false]),
    span(-60, -1).map((d) => 1 + d),
  );
  it('pow agrees with the engine within 1e-15 relative for positive bases and normal results', () => {
    fc.assert(
      fc.property(base, span(-30, 9), (x, y) => {
        const want = Math.pow(x, y);
        fc.pre(Number.isFinite(want) && want >= 2.2250738585072014e-308);
        agrees(pow(x, y), want);
      }),
      RUNS,
    );
  });

  it('pow(-x, n) is pow(x, n) for even n and -pow(x, n) for odd n, to the bit', () => {
    fc.assert(
      fc.property(base, fc.integer({ min: -1100, max: 1100 }), (x, n) => {
        expect(Object.is(pow(-x, n), n % 2 === 0 ? pow(x, n) : -pow(x, n))).toBe(true);
      }),
      RUNS,
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
      RUNS,
    );
  });
});

describe('the special-value sweep over every double', () => {
  // NaN, the infinities, signed zeros and subnormals included.
  const anyDouble = fc.double();

  it('sin and tanh stay odd and cos even, to the bit, and every function agrees with the engine', () => {
    fc.assert(
      fc.property(fc.constantFrom(...unary), anyDouble, (name, x) => {
        expect(Object.is(sin(-x), -sin(x))).toBe(true);
        expect(Object.is(tanh(-x), -tanh(x))).toBe(true);
        expect(Object.is(cos(-x), cos(x))).toBe(true);
        agrees(functions[name](x), engine(name, x));
      }),
      RUNS,
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
      RUNS,
    );
  });
});
