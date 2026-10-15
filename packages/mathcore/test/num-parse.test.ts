import { readFileSync } from 'node:fs';
import fc from 'fast-check';
import { describe, expect, it } from 'vitest';
import {
  INPUT_LIMIT,
  normalise,
  parseNumber,
  type NumForm,
  type ParseFailure,
  type ParsedNumber,
} from '@zq/mathcore/num-parse';
import { add, neg, rat, spell, terminates, type Rational } from '@zq/mathcore/rational';

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
const spelled = ({ typed, ...r }: ParsedNumber): Record<string, unknown> => ({
  ...r,
  value: spell(r.value),
  typed: typed && { whole: String(typed.whole), n: String(typed.n), d: String(typed.d) },
});

// The parser's inverse, for the round-trip property only. Learner-facing numbers are formatted by
// engine/render's format.ts through Intl.NumberFormat('en-GB') (ARCHITECTURE.md 5.11), never by this.
const MINUS = '\u2212';
const group = (digits: string): string => digits.replace(/\B(?=(?:\d{3})+$)/g, ',');

/** |a| as a decimal digit string with `places` digits after an implied point; a must terminate. */
function scaled(a: Rational): { digits: string; places: number } {
  if (!terminates(a)) throw new RangeError('the decimal does not terminate');
  let places = 0;
  let p = 1n;
  while (p % a.d !== 0n) [p, places] = [p * 10n, places + 1];
  return { digits: ((a.n < 0n ? -a.n : a.n) * (p / a.d)).toString().padStart(places + 1, '0'), places };
}

function decimal(a: Rational, point: boolean): string {
  const { digits, places } = scaled(a);
  const whole = group(digits.slice(0, digits.length - places));
  return whole + (places > 0 ? `.${digits.slice(-places)}` : point ? '.0' : '');
}

/** Writes an exact value in a form so that `parseNumber` reads back the same form and value. */
function formatNumber(a: Rational, form: NumForm): string {
  const sign = a.n < 0n ? MINUS : '';
  const n = a.n < 0n ? -a.n : a.n;
  switch (form) {
    case 'integer':
      if (a.d !== 1n) throw new RangeError('not an integer');
      return sign + group(n.toString());
    case 'decimal':
      return sign + decimal(a, true);
    case 'percent':
      return `${sign}${decimal(a, false)}%`;
    case 'fraction':
      return `${sign}${group(n.toString())}/${group(a.d.toString())}`;
    case 'mixed':
      if (a.d === 1n || n < a.d) throw new RangeError('a mixed number has a whole part and a fraction');
      return `${sign}${group((n / a.d).toString())} ${group((n % a.d).toString())}/${group(a.d.toString())}`;
    case 'standard-form': {
      const { digits, places } = scaled(a);
      const lead = digits.replace(/^0+(?=\d)/, '');
      const mantissa = lead.replace(/0+$/, '') || '0';
      const exp = lead === '0' ? 0 : lead.length - 1 - places;
      const tail = mantissa.length > 1 ? `.${mantissa.slice(1)}` : '';
      return `${sign}${mantissa.charAt(0)}${tail} \u00D7 10^${exp < 0 ? MINUS + String(-exp) : String(exp)}`;
    }
  }
}

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

  it('accepts one leading sign, with or without a space after it', () => {
    expect(plain('+33.1%')).toMatchObject({ ok: true, form: 'percent', value: '331/10' });
    expect(plain('+5')).toMatchObject({ ok: true, form: 'integer', value: '5' });
    expect(plain('\u2212 5')).toMatchObject({ ok: true, form: 'integer', value: '-5' });
    expect(plain('+ \u00A35', ['\u00A3'])).toMatchObject({ ok: true, value: '5', unit: '\u00A3' });
    expect(plain('- 2 1/3')).toMatchObject({ ok: true, form: 'mixed', value: '-7/3' });
  });

  it('keeps the parts of a fraction or mixed number as typed', () => {
    expect(plain('4/6')).toMatchObject({
      form: 'fraction',
      value: '2/3',
      typed: { whole: '0', n: '4', d: '6' },
    });
    expect(plain('2/3')).toMatchObject({
      form: 'fraction',
      value: '2/3',
      typed: { whole: '0', n: '2', d: '3' },
    });
    expect(plain('2 2/4')).toMatchObject({
      form: 'mixed',
      value: '5/2',
      typed: { whole: '2', n: '2', d: '4' },
    });
    expect(plain('-1,000 / 3')).toMatchObject({ value: '-1000/3', typed: { whole: '0', n: '1000', d: '3' } });
    expect(plain('0.5')).toMatchObject({ typed: null });
    const part = fc.bigInt({ min: 0n, max: 10n ** 9n });
    fc.assert(
      fc.property(
        part,
        part,
        part.map((d) => d + 1n),
        fc.boolean(),
        (whole, n, d, negative) => {
          const text = `${negative ? '-' : ''}${whole > 0n ? `${whole} ` : ''}${n}/${d}`;
          const r = parseNumber(text);
          const improper = whole > 0n && (n === 0n || n >= d);
          expect(r.ok, text).toBe(!improper);
          if (!r.ok) return;
          expect(r.typed, text).toEqual({ whole, n, d });
          const unsigned = add(rat(whole), rat(n, d));
          expect(r.value, text).toEqual(negative ? neg(unsigned) : unsigned);
        },
      ),
    );
  });

  it('reads a narrow space as a grouping separator only where a comma would be one', () => {
    const cases: [string, Record<string, unknown>][] = [
      ['1\u2009000', { form: 'integer', value: '1000' }],
      ['1\u00A0234\u00A0567', { form: 'integer', value: '1234567' }],
      ['12\u202F345.5', { form: 'decimal', value: '24691/2' }],
      ['2\u00A01/3', { form: 'mixed', value: '7/3' }],
      ['1\u202F1/2', { form: 'mixed', value: '3/2' }],
      ['3.2\u2009\u00D7\u200910^5', { form: 'standard-form', value: '320000' }],
      ['0\u00A0500', { ok: false, reason: 'syntax' }],
      ['1\u00A02345', { ok: false, reason: 'syntax' }],
      ['0.123\u2009456', { ok: false, reason: 'syntax' }],
      ['1\u00A0000,5', { ok: false, reason: 'decimal-comma' }],
    ];
    for (const [input, out] of cases) expect(plain(input), input).toMatchObject(out);
  });

  const narrow = fc.constantFrom('\u00A0', '\u2007', '\u2009', '\u200A', '\u202F');
  const syntax = { ok: false, reason: 'syntax' };

  it('refuses a narrow-space grouping before "/", where it also reads as a mixed number', () => {
    const cases: [string, Record<string, unknown>][] = [
      ['2\u00A0125/250', syntax],
      ['1\u202F125/250', syntax],
      ['3\u2009100/200', syntax],
      ['97\u00A0291/882674', syntax],
      ['12\u00A0345/7', syntax],
      ['1\u00A0000 / 3', syntax],
      ['1\u00A0000\u00A0/3', syntax],
      ['1\u00A0000/0', syntax],
      ['\u22121\u00A0000\u00A0000/7', syntax],
      ['2 125/250', { form: 'mixed', value: '5/2' }],
      ['2\u00A01/3', { form: 'mixed', value: '7/3' }],
      ['1\u00A0000', { form: 'integer', value: '1000' }],
      ['1,000/3', { form: 'fraction', value: '1000/3' }],
      ['3/1\u00A0000', { form: 'fraction', value: '3/1000' }],
      ['1\u00A0000\u00A01/2', { form: 'mixed', value: '2001/2' }],
    ];
    for (const [input, out] of cases) expect(plain(input), input).toMatchObject(out);
    fc.assert(
      fc.property(
        fc.bigInt({ min: 1000n, max: 10n ** 12n }),
        narrow,
        fc.constantFrom('', '-', '\u2212', '+ '),
        fc.constantFrom('', ' ', '\u00A0', ' \t'),
        fc.bigInt({ min: 0n, max: 10n ** 9n }),
        (whole, space, sign, gap, d) => {
          const text = (sep: string): string =>
            `${sign}${group(whole.toString()).replaceAll(',', sep)}${gap}/${d}`;
          expect(parseNumber(text(space)), text(space)).toEqual(syntax);
          expect(plain(text(',')), text(',')).toMatchObject(
            d === 0n ? { reason: 'zero-denominator' } : { form: 'fraction', typed: { n: String(whole) } },
          );
        },
      ),
    );
    fc.assert(
      fc.property(
        fc.bigInt({ min: 1n, max: 10n ** 6n }),
        narrow,
        fc.integer({ min: 1, max: 99 }),
        (w, space, n) => {
          const d = BigInt(n) + 1n;
          expect(plain(`${w}${space}${n}/${d}`)).toMatchObject({
            form: 'mixed',
            value: spell(add(rat(w), rat(BigInt(n), d))),
          });
        },
      ),
    );
  });

  it('never groups by a narrow space inside an exponent', () => {
    for (const input of ['3.2e1\u00A0000', '3.2E1\u00A0000', '1e\u22121\u00A0000', '3.2 x 10^1\u00A0000'])
      expect(parseNumber(input), input).toEqual(syntax);
    expect(plain('3.2e1000')).toMatchObject({ form: 'standard-form' });
    fc.assert(
      fc.property(
        fc.nat({ max: 999_999 }),
        fc.option(fc.nat({ max: 999 })),
        fc.constantFrom('e', 'E', ' x 10^', '\u00D710^', '*10^'),
        fc.constantFrom('', '-', '+', '\u2212'),
        fc.integer({ min: 1, max: 999 }),
        narrow,
        fc.nat({ max: 999 }),
        (a, b, mark, sign, k, space, r) => {
          const text = (sep: string): string =>
            `${a}${b === null ? '' : `.${b}`}${mark}${sign}${k}${sep}${String(r).padStart(3, '0')}`;
          expect(parseNumber(text(space)), text(space)).toEqual(syntax);
          expect(plain(text('')), text('')).not.toEqual(syntax);
        },
      ),
    );
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
      ['+-5', 'syntax'],
      ['++5', 'syntax'],
      ['+', 'syntax'],
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

describe("the parser's inverse", () => {
  const whole = fc.bigInt({ min: -(10n ** 15n), max: 10n ** 15n });
  const terminating = fc
    .tuple(whole, fc.nat({ max: 12 }), fc.nat({ max: 12 }))
    .map(([n, a, b]) => rat(n, 2n ** BigInt(a) * 5n ** BigInt(b)));
  const any = fc.tuple(whole, fc.bigInt({ min: 1n, max: 10n ** 12n })).map(([n, d]) => rat(n, d));
  const roundTrips =
    (form: NumForm) =>
    (a: Rational): void => {
      const text = formatNumber(a, form);
      expect(plain(text), text).toMatchObject({ ok: true, form, value: spell(a) });
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
    expect(() => formatNumber(rat(1, 2), 'mixed')).toThrow(RangeError);
    expect(() => formatNumber(rat(-1, 3), 'mixed')).toThrow(RangeError);
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
        any.filter((a) => a.d !== 1n && (a.n < 0n ? -a.n : a.n) > a.d),
        roundTrips('mixed'),
      ),
    );
    for (const form of ['decimal', 'percent', 'standard-form'] as const)
      fc.assert(fc.property(terminating, roundTrips(form)));
  });
});

describe('parity with tools/zqverify/num_parse.py', () => {
  it(`agrees on all ${golden.length} golden inputs`, () => {
    expect(golden.length).toBeGreaterThanOrEqual(1500);
    for (const g of golden) expect(plain(g.in, g.units), JSON.stringify(g.in)).toEqual(g.out);
  });

  it('never matches a unit longer than the text', () => {
    expect(parseNumber('5\u0130', ['5i\u0307', '\u0130'])).toMatchObject({ ok: true, unit: '\u0130' });
    expect(parseNumber('\u01305', ['i\u03075', '\u0130'])).toMatchObject({ ok: true, unit: '\u0130' });
    expect(parseNumber('5', ['55'])).toMatchObject({ ok: true, unit: null });
  });

  it('normalises as 7.2 says', () => {
    expect(normalise(' \u2212 1\u202F000 \t\u00B7  2 ')).toBe('- 1000 * 2');
    expect(normalise('2\u00A01/3\u2009')).toBe('2 1/3');
  });
});
