import { readFileSync } from 'node:fs';
import fc from 'fast-check';
import { describe, expect, it } from 'vitest';
import * as Q from '@zq/mathcore/rational';

interface Golden {
  a: string;
  b: string;
  canonical: string;
  add: string;
  sub: string;
  mul: string;
  div: string | null;
  cmp: number;
  terminates: boolean;
}

const golden = readFileSync(new URL('rational.golden.jsonl', import.meta.url), 'utf8')
  .split('\n')
  .filter(Boolean)
  .map((line) => JSON.parse(line) as Golden);
const big = fc.bigInt({ min: -(10n ** 30n), max: 10n ** 30n });
const rational = fc
  .tuple(
    big,
    big.filter((d) => d !== 0n),
  )
  .map(([n, d]) => Q.rat(n, d));
const ZERO = Q.rat(0);
const ONE = Q.rat(1);

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
    expect(() => Q.rat(2 ** 53)).toThrow(RangeError);
  });

  it('is canonical for any numerator and denominator', () => {
    fc.assert(
      fc.property(
        big,
        big.filter((d) => d !== 0n),
        (n, d) => {
          const r = Q.rat(n, d);
          expect(r.d > 0n).toBe(true);
          expect(r.n * d).toBe(n * r.d);
          expect(Q.eq(Q.rat(r.n, r.d), r)).toBe(true);
        },
      ),
    );
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

  it('give inverses, and order agrees with subtraction', () => {
    fc.assert(
      fc.property(rational, rational, (a, b) => {
        expect(Q.sub(a, a)).toEqual(ZERO);
        expect(Q.add(a, Q.neg(a))).toEqual(ZERO);
        if (a.n !== 0n) expect(Q.div(a, a)).toEqual(ONE);
        if (b.n !== 0n) expect(Q.mul(Q.div(a, b), b)).toEqual(a);
        const sign = Q.sub(a, b).n;
        expect(Q.cmp(a, b)).toBe(sign < 0n ? -1 : sign > 0n ? 1 : 0);
        expect(Q.eq(a, b)).toBe(Q.cmp(a, b) === 0);
      }),
    );
  });
});

describe('spellings', () => {
  it('read decimals, exponents and fractions', () => {
    expect(Q.fromDecimal('-12.5')).toEqual(Q.rat(-25, 2));
    expect(Q.fromDecimal('.25')).toEqual(Q.rat(1, 4));
    expect(Q.fromDecimal('305.')).toEqual(Q.rat(305));
    expect(Q.fromDecimal('3.2e-3')).toEqual(Q.rat(2, 625));
    expect(Q.fromDecimal('1E3')).toEqual(Q.rat(1000));
    expect(Q.parse('10/109')).toEqual(Q.rat(10, 109));
    expect(Q.parse('-6/4')).toEqual(Q.rat(-3, 2));
  });

  it('refuse anything else, and exponents beyond the limit', () => {
    for (const bad of ['', '.', '-', 'e5', '1,000', '1/-2', '1/0', ' 1', '0x10', '1e1001'])
      expect(() => Q.parse(bad), bad).toThrow(RangeError);
    expect(Q.fromDecimal(`1e-${Q.EXPONENT_LIMIT}`).d).toBe(10n ** BigInt(Q.EXPONENT_LIMIT));
  });

  it('round-trip through the canonical spelling', () => {
    fc.assert(
      fc.property(rational, (a) => {
        expect(Q.parse(Q.toString(a))).toEqual(a);
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
  it(`agrees on all ${golden.length} golden pairs`, () => {
    for (const g of golden) {
      const [a, b] = [Q.parse(g.a), Q.parse(g.b)];
      const got = {
        canonical: Q.toString(a),
        add: Q.toString(Q.add(a, b)),
        sub: Q.toString(Q.sub(a, b)),
        mul: Q.toString(Q.mul(a, b)),
        div: b.n === 0n ? null : Q.toString(Q.div(a, b)),
        cmp: Q.cmp(a, b),
        terminates: Q.terminates(a),
      };
      expect({ a: g.a, b: g.b, ...got }).toEqual(g);
    }
  });
});
