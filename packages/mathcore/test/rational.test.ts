import { readFileSync } from 'node:fs';
import fc from 'fast-check';
import { describe, expect, it } from 'vitest';
import * as Q from '@zq/mathcore/rational';

interface Pair {
  kind: 'pair';
  a: string;
  b: string;
  canonical: string;
  neg: string;
  add: string;
  sub: string;
  mul: string;
  div: string | null;
  cmp: number;
  eq: boolean;
  terminatesA: boolean;
  terminatesB: boolean;
}
interface Refused {
  kind: 'refused';
  text: string;
  error: string;
}

const golden = readFileSync(new URL('rational.golden.jsonl', import.meta.url), 'utf8')
  .split('\n')
  .filter(Boolean)
  .map((line) => JSON.parse(line) as Pair | Refused);
const pairs = golden.filter((g): g is Pair => g.kind === 'pair');
const refused = golden.filter((g): g is Refused => g.kind === 'refused');
const big = fc.bigInt({ min: -(10n ** 30n), max: 10n ** 30n });
const nonzero = big.filter((d) => d !== 0n);
const rational = fc.tuple(big, nonzero).map(([n, d]) => Q.rat(n, d));
const ZERO = Q.rat(0);
const ONE = Q.rat(1);
// Objects built by hand, as a structured clone, a db document or an import may give them: unreduced, with a
// negative denominator, and with a zero one.
const HAND_BUILT: Q.Rational[] = [
  { n: 2n, d: 4n },
  { n: 1n, d: -2n },
  { n: 1n, d: 0n },
];
const MESSAGES = new Set([
  'not a decimal',
  'not a fraction',
  'sign on the denominator',
  'division by zero',
  `exponent beyond ${Q.EXPONENT_LIMIT}`,
]);

// Written here rather than imported, so the lowest-terms check does not rest on the module's own gcd.
const gcd = (a: bigint, b: bigint): bigint => (b === 0n ? a : gcd(b, a % b));
const abs = (x: bigint): bigint => (x < 0n ? -x : x);

/** The message of the RangeError `parse` throws for text, or null when it reads the text. */
function refusal(text: string): string | null {
  try {
    Q.parse(text);
  } catch (error) {
    if (error instanceof RangeError) return error.message;
    throw error;
  }
  return null;
}

describe('rat', () => {
  it('keeps a positive denominator in lowest terms', () => {
    expect(Q.rat(6, -4)).toEqual({ n: -3n, d: 2n });
    expect(Q.rat(-0, -5)).toEqual({ n: 0n, d: 1n });
    expect(Q.rat(7n)).toEqual({ n: 7n, d: 1n });
  });

  it('refuses a zero denominator and numbers that are not safe integers', () => {
    expect(() => Q.rat(1, 0)).toThrow(RangeError);
    expect(() => Q.div(ONE, ZERO)).toThrow('division by zero');
    expect(() => Q.rat(0.5)).toThrow(RangeError);
    expect(() => Q.rat(2 ** 53)).toThrow(/^not a safe integer$/);
  });

  it('is canonical for any numerator and denominator', () => {
    fc.assert(
      fc.property(big, nonzero, (n, d) => {
        const r = Q.rat(n, d);
        expect(r.d > 0n).toBe(true);
        expect(gcd(abs(r.n), r.d)).toBe(1n);
        expect(r.n * d).toBe(n * r.d);
        expect(Q.isRational(r)).toBe(true);
      }),
    );
  });
});

describe('isRational', () => {
  it('accepts canonical values, before and after structured clone', () => {
    fc.assert(
      fc.property(rational, (a) => {
        expect(Q.isRational(a)).toBe(true);
        expect(Q.isRational(structuredClone(a))).toBe(true);
      }),
    );
  });

  it('refuses values that are not canonical and anything that is not a rational', () => {
    const bad = [
      ...HAND_BUILT,
      { n: 0n, d: 5n },
      { n: -2n, d: 6n },
      { n: 1, d: 2n },
      { n: 1n, d: 2 },
      { n: 1n },
      null,
      '1/2',
    ];
    for (const [i, x] of bad.entries()) expect(Q.isRational(x), `case ${i}`).toBe(false);
  });

  it('guards terminates, which would loop on a zero denominator', () => {
    for (const x of HAND_BUILT) expect(() => Q.terminates(x)).toThrow(/^not a canonical rational$/);
  });
});

describe('the field laws', () => {
  it('hold for addition and multiplication', () => {
    fc.assert(
      fc.property(rational, rational, rational, (a, b, c) => {
        expect(Q.add(a, b)).toEqual(Q.add(b, a));
        expect(Q.mul(a, b)).toEqual(Q.mul(b, a));
        expect(Q.add(Q.add(a, b), c)).toEqual(Q.add(a, Q.add(b, c)));
        expect(Q.mul(Q.mul(a, b), c)).toEqual(Q.mul(a, Q.mul(b, c)));
        expect(Q.mul(a, Q.add(b, c))).toEqual(Q.add(Q.mul(a, b), Q.mul(a, c)));
        expect(Q.add(a, ZERO)).toEqual(a);
        expect(Q.mul(a, ONE)).toEqual(a);
      }),
    );
  });

  it('give inverses, and order and equality agree with subtraction', () => {
    fc.assert(
      fc.property(rational, rational, nonzero, (a, b, k) => {
        expect(Q.sub(a, a)).toEqual(ZERO);
        expect(Q.add(a, Q.neg(a))).toEqual(ZERO);
        if (a.n !== 0n) expect(Q.div(a, a)).toEqual(ONE);
        if (b.n !== 0n) expect(Q.mul(Q.div(a, b), b)).toEqual(a);
        const sign = Q.sub(a, b).n;
        expect(Q.cmp(a, b)).toBe(sign < 0n ? -1 : sign > 0n ? 1 : 0);
        expect(Q.eq(a, b)).toBe(Q.cmp(a, b) === 0);
        expect(Q.eq(a, Q.rat(a.n * k, a.d * k))).toBe(true);
      }),
    );
  });

  it('make eq compare both fields', () => {
    expect(Q.eq(Q.rat(1, 2), Q.rat(1, 3))).toBe(false);
    expect(Q.eq(Q.rat(2, 4), Q.rat(1, 2))).toBe(true);
    expect(Q.eq(Q.rat(1, 2), Q.rat(-1, 2))).toBe(false);
  });
});

describe('spellings', () => {
  it('read decimals, exponents and fractions', () => {
    expect(Q.fromDecimal('-12.5')).toEqual(Q.rat(-25, 2));
    expect(Q.fromDecimal('.25')).toEqual(Q.rat(1, 4));
    expect(Q.fromDecimal('305.')).toEqual(Q.rat(305));
    expect(Q.fromDecimal('3.2e-3')).toEqual(Q.rat(2, 625));
    expect(Q.fromDecimal('1E+3')).toEqual(Q.rat(1000));
    expect(Q.fromDecimal('-0.0')).toEqual(ZERO);
    expect(Q.parse('10/109')).toEqual(Q.rat(10, 109));
    expect(Q.parse('-6/4')).toEqual(Q.rat(-3, 2));
  });

  it('refuse anything else with a fixed message, and exponents beyond the limit', () => {
    const cases: [string, string][] = [
      ['', 'not a decimal'],
      ['.', 'not a decimal'],
      ['-', 'not a decimal'],
      ['e5', 'not a decimal'],
      ['1,000', 'not a decimal'],
      [' 1', 'not a decimal'],
      ['0x10', 'not a decimal'],
      ['+1', 'not a decimal'],
      ['+1/2', 'not a fraction'],
      ['1/+2', 'sign on the denominator'],
      ['1/-2', 'sign on the denominator'],
      ['1/0', 'division by zero'],
      ['1e1001', 'exponent beyond 1000'],
    ];
    for (const [text, error] of cases) expect(refusal(text), text).toBe(error);
    expect(Q.fromDecimal(`1e-${Q.EXPONENT_LIMIT}`).d).toBe(10n ** BigInt(Q.EXPONENT_LIMIT));
  });

  it('never echo the text in a message', () => {
    fc.assert(
      fc.property(fc.string(), (text) => {
        const error = refusal(text);
        if (error !== null) expect(MESSAGES.has(error), error).toBe(true);
      }),
    );
  });

  it('round-trip through the canonical spelling', () => {
    fc.assert(
      fc.property(rational, (a) => {
        expect(Q.parse(Q.spell(a))).toEqual(a);
      }),
    );
  });

  it('know which values terminate', () => {
    expect(Q.terminates(Q.rat(3, 40))).toBe(true);
    expect(Q.terminates(Q.rat(1, 3))).toBe(false);
    expect(Q.terminates(Q.rat(-7))).toBe(true);
  });
});

describe('parity with Fraction (tools/zqverify/rational.py)', () => {
  it(`agrees on all ${pairs.length} golden pairs`, () => {
    for (const g of pairs) {
      const [a, b] = [Q.parse(g.a), Q.parse(g.b)];
      const got: Pair = {
        kind: 'pair',
        a: g.a,
        b: g.b,
        canonical: Q.spell(a),
        neg: Q.spell(Q.neg(a)),
        add: Q.spell(Q.add(a, b)),
        sub: Q.spell(Q.sub(a, b)),
        mul: Q.spell(Q.mul(a, b)),
        div: b.n === 0n ? null : Q.spell(Q.div(a, b)),
        cmp: Q.cmp(a, b),
        eq: Q.eq(a, b),
        terminatesA: Q.terminates(a),
        terminatesB: Q.terminates(b),
      };
      expect(got).toEqual(g);
    }
  });

  it(`refuses all ${refused.length} golden refusals with the same message`, () => {
    for (const g of refused) expect(refusal(g.text), JSON.stringify(g.text)).toBe(g.error);
  });
});
