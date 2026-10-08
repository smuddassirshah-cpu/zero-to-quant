import { readFileSync } from 'node:fs';
import fc from 'fast-check';
import { describe, expect, it } from 'vitest';
import {
  INPUT_LIMIT,
  formatNumber,
  normalise,
  parseNumber,
  type NumForm,
  type ParseFailure,
  type ParsedNumber,
} from '@zq/mathcore/num-parse';
import { rat, toString, type Rational } from '@zq/mathcore/rational';

interface Golden {
  in: string;
  units: string[];
  out: Record<string, unknown>;
}

const golden = readFileSync(new URL('num-parse.golden.jsonl', import.meta.url), 'utf8')
  .split('\n')
  .filter(Boolean)
  .map((line) => JSON.parse(line) as Golden);

/** The parse as plain data, with the value in its canonical spelling, as the golden file holds it. */
function plain(input: string, units: readonly string[] = []): Record<string, unknown> {
  const r = parseNumber(input, units);
  return r.ok ? spelled(r) : r;
}
const spelled = (r: ParsedNumber): Record<string, unknown> => ({ ...r, value: toString(r.value) });

describe('parseNumber', () => {
  it("reads CONTENT-FORMAT.md 7.2's examples", () => {
    const cases: [string, NumForm, string][] = [
      ['11', 'integer', '11'],
      ['\u22123', 'integer', '-3'],
      ['1,000', 'integer', '1000'],
      ['.25', 'decimal', '1/4'],
      ['305.', 'decimal', '305'],
      ['-10 / 109', 'fraction', '-10/109'],
      ['2 1/3', 'mixed', '7/3'],
      ['66.7 %', 'percent', '667/10'],
      ['3.2 x 10^5', 'standard-form', '320000'],
      ['3.2\u00D710^-3', 'standard-form', '2/625'],
    ];
    for (const [input, form, value] of cases)
      expect(plain(input), input).toMatchObject({ ok: true, form, value });
  });

  it('records places, figures and the unit typed', () => {
    expect(plain('0.0350')).toMatchObject({ places: 4, figures: 3, unit: null });
    expect(plain('\u00A312.50', ['\u00A3'])).toMatchObject({
      form: 'decimal',
      value: '25/2',
      unit: '\u00A3',
    });
    expect(plain('11 Outcomes', ['outcomes'])).toMatchObject({ value: '11', unit: 'outcomes' });
    expect(plain('250bp', ['%', 'bp'])).toMatchObject({ form: 'integer', unit: 'bp' });
  });

  it('fails with the reason a grader nudges on', () => {
    const cases: [string, ParseFailure][] = [
      ['', 'empty'],
      [' \u00A0 ', 'empty'],
      ['1'.repeat(INPUT_LIMIT + 1), 'too-long'],
      ['0,5', 'decimal-comma'],
      ['0,500', 'decimal-comma'],
      ['1/0', 'zero-denominator'],
      ['1e1001', 'out-of-range'],
      ['+5', 'syntax'],
      ['2 4/3', 'syntax'],
      ['1/2%', 'syntax'],
      ['\u00A35', 'syntax'],
      ['\uFF15', 'syntax'],
    ];
    for (const [input, reason] of cases) expect(parseNumber(input), input).toEqual({ ok: false, reason });
  });

  it('never throws, whatever is typed', () => {
    fc.assert(
      fc.property(fc.string({ unit: 'binary', maxLength: 40 }), (s) => {
        expect(() => parseNumber(s, ['\u00A3'])).not.toThrow();
      }),
    );
    fc.assert(
      fc.property(fc.stringMatching(/^[-\d,. /e%x^*]{1,24}$/), (s) => {
        expect(() => parseNumber(s, ['x'])).not.toThrow();
      }),
    );
  });
});

describe('formatNumber', () => {
  const whole = fc.bigInt({ min: -(10n ** 15n), max: 10n ** 15n });
  const terminating = fc
    .tuple(whole, fc.nat({ max: 12 }), fc.nat({ max: 12 }))
    .map(([n, a, b]) => rat(n, 2n ** BigInt(a) * 5n ** BigInt(b)));
  const any = fc.tuple(whole, fc.bigInt({ min: 1n, max: 10n ** 12n })).map(([n, d]) => rat(n, d));
  const roundTrips =
    (form: NumForm) =>
    (a: Rational): void => {
      const text = formatNumber(a, form);
      expect(plain(text), text).toMatchObject({ ok: true, form, value: toString(a) });
    };

  it('writes en-GB: grouping commas and a true minus', () => {
    expect(formatNumber(rat(-1234567), 'integer')).toBe('\u22121,234,567');
    expect(formatNumber(rat(12), 'decimal')).toBe('12.0');
    expect(formatNumber(rat(-1, 8), 'decimal')).toBe('\u22120.125');
    expect(formatNumber(rat(7, 3), 'mixed')).toBe('2 1/3');
    expect(formatNumber(rat(2, 625), 'standard-form')).toBe('3.2 \u00D7 10^\u22123');
    expect(formatNumber(rat(0), 'standard-form')).toBe('0 \u00D7 10^0');
    expect(formatNumber(rat(667, 10), 'percent')).toBe('66.7%');
  });

  it('refuses a value the form cannot hold', () => {
    expect(() => formatNumber(rat(1, 2), 'integer')).toThrow(RangeError);
    expect(() => formatNumber(rat(1, 3), 'decimal')).toThrow(RangeError);
    expect(() => formatNumber(rat(3), 'mixed')).toThrow(RangeError);
  });

  it('round-trips through parseNumber in every form', () => {
    fc.assert(
      fc.property(
        whole.map((n) => rat(n)),
        roundTrips('integer'),
      ),
    );
    fc.assert(fc.property(any, roundTrips('fraction')));
    fc.assert(
      fc.property(
        any.filter((a) => a.d !== 1n),
        roundTrips('mixed'),
      ),
    );
    for (const form of ['decimal', 'percent', 'standard-form'] as const)
      fc.assert(fc.property(terminating, roundTrips(form)));
  });
});

describe('parity with tools/zqverify/num_parse.py', () => {
  it(`agrees on all ${golden.length} golden inputs`, () => {
    for (const g of golden) expect(plain(g.in, g.units), JSON.stringify(g.in)).toEqual(g.out);
  });

  it('normalises as 7.2 says', () => {
    expect(normalise(' \u2212 1\u202F000 \t\u00B7  2 ')).toBe('- 1000 * 2');
  });
});
