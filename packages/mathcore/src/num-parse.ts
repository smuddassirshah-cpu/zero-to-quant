// en-GB number parsing for numeric answers, shared with the graders (docs/CONTENT-FORMAT.md 7.2; WIDGETS.md
// 4.2.2 `numeric-input`). Decision notes:
// - The parser reads and classifies; it does not grade. It returns the form the learner typed and its exact
//   value, and the grader applies the check's `forms`, `integer`, `probability`, `sf`, `dp` and unit rules
//   (stage 20), so the grader and every widget's parse preview read a typed number the same way.
// - Normalisation is 7.2's: U+2212 and the dashes become "-", thin and no-break spaces are removed, "×" and
//   "·" (and the dot operator U+22C5) become "*". Runs of spaces and tabs collapse to one space and ASCII
//   whitespace is trimmed [our choice]. Lengths are UTF-16 code units, JavaScript's own.
// - Grouping commas: a first group of 1 to 3 digits not starting with 0, then groups of exactly 3 (7.2's "a
//   comma between digit groups of three"); "0,500" is therefore a decimal comma, not five hundred [our choice].
//   A string that fails but parses with its one comma read as a point fails as `decimal-comma`, 7.2's nudge.
// - Accepted: a leading "-" only (no "+"), 7.2's six forms, and one listed unit, compared without case and
//   typed before or after the number (a listed "%" is read as that unit, not as the percent form). A
//   percent's value is the number before its sign ("25%" is 25); the grader divides by 100 where the answer
//   is a proportion (7.2). A mixed number's fraction is proper and non-zero. Anything else fails.
// - Inputs longer than INPUT_LIMIT characters fail, and exponents are bounded by rational.ts, so a typed
//   string cannot make a large BigInt [our choice: 200 is NumValue's own limit, CONTENT-FORMAT.md 3.2].
// - `formatNumber` writes each form in en-GB (grouping commas, U+2212 minus) so that it parses back.
import { EXPONENT_LIMIT, add, fromDecimal, neg, rat, terminates, type Rational } from './rational.ts';

export type NumForm = 'integer' | 'decimal' | 'fraction' | 'mixed' | 'percent' | 'standard-form';
export type ParseFailure =
  'empty' | 'too-long' | 'decimal-comma' | 'zero-denominator' | 'out-of-range' | 'syntax';

export interface ParsedNumber {
  readonly ok: true;
  readonly form: NumForm;
  /** Exact. For a percent, the number before the sign. */
  readonly value: Rational;
  /** The listed unit the learner typed, spelled as listed, or null. */
  readonly unit: string | null;
  /** Digits after the decimal point, as typed (0 without a point, and for fractions). */
  readonly places: number;
  /** Significant figures as typed: digits from the first non-zero one to the last, so "1200" has 4. */
  readonly figures: number;
}
export type NumParse = ParsedNumber | { readonly ok: false; readonly reason: ParseFailure };

export const INPUT_LIMIT = 200;
const MINUS = '\u2212';

const INT = String.raw`(?:[1-9]\d{0,2}(?:,\d{3})+|\d+)`;
const MIXED = new RegExp(String.raw`^(${INT}) (${INT}) ?/ ?(${INT})$`);
const FRACTION = new RegExp(String.raw`^(${INT}) ?/ ?(${INT})$`);
const DECIMAL = new RegExp(String.raw`^(${INT})?(?:\.(\d*))?(?:[eE]([+-]?\d+)| ?[*xX] ?10\^([+-]?\d+))?$`);

/** CONTENT-FORMAT.md 7.2's normalisation; runs of spaces collapsed, ASCII whitespace trimmed. */
export const normalise = (text: string): string =>
  text
    .replace(/[\u2010-\u2015\u2212\uFE58\uFE63\uFF0D]/g, '-')
    .replace(/[\u00A0\u2007\u2009\u200A\u202F]/g, '')
    .replace(/[\u00D7\u00B7\u22C5]/g, '*')
    .replace(/[ \t]+/g, ' ')
    .replace(/^[ \t\n\v\f\r]+|[ \t\n\v\f\r]+$/g, '');

type Body = Omit<ParsedNumber, 'ok' | 'unit'> | ParseFailure;

const integer = (digits: string): bigint => BigInt(digits.replaceAll(',', ''));

function body(text: string, percent: boolean): Body {
  const mixed = MIXED.exec(text);
  const parts = mixed ? mixed.slice(1) : FRACTION.exec(text)?.slice(1);
  if (parts) {
    if (percent) return 'syntax';
    const [whole, n, d] = (mixed ? parts : ['0', ...parts]).map(integer) as [bigint, bigint, bigint];
    if (d === 0n) return 'zero-denominator';
    if (mixed && (n === 0n || n >= d)) return 'syntax';
    return { form: mixed ? 'mixed' : 'fraction', value: add(rat(whole), rat(n, d)), places: 0, figures: 0 };
  }
  const m = DECIMAL.exec(text);
  if (!m) return 'syntax';
  const [, whole = '', frac, e1, e2] = m;
  const exp = e1 ?? e2;
  if (whole + (frac ?? '') === '' || (percent && exp !== undefined)) return 'syntax';
  if (exp !== undefined && Math.abs(Number(exp)) > EXPONENT_LIMIT) return 'out-of-range';
  const digits = whole.replaceAll(',', '') + (frac ?? '');
  return {
    form: percent
      ? 'percent'
      : exp !== undefined
        ? 'standard-form'
        : frac === undefined
          ? 'integer'
          : 'decimal',
    value: fromDecimal(`${whole.replaceAll(',', '')}.${frac ?? ''}e${exp ?? '0'}`),
    places: frac?.length ?? 0,
    figures: digits.replace(/^0+/, '').length,
  };
}

/** Reads a typed number. `units` lists the unit spellings the field accepts ("£", "bp", "outcomes"). */
export function parseNumber(input: string, units: readonly string[] = []): NumParse {
  if (input.length > INPUT_LIMIT) return { ok: false, reason: 'too-long' };
  const text = normalise(input);
  if (text === '') return { ok: false, reason: 'empty' };
  const negative = text.startsWith('-');
  let rest = negative ? text.slice(1) : text;
  let unit: string | null = null;
  for (const u of [...units].sort((a, b) => b.length - a.length)) {
    const key = u.toLowerCase();
    if (u !== '' && rest.slice(0, u.length).toLowerCase() === key)
      rest = rest.slice(u.length).replace(/^ /, '');
    else if (u !== '' && rest.slice(-u.length).toLowerCase() === key)
      rest = rest.slice(0, -u.length).replace(/ $/, '');
    else continue;
    unit = u;
    break;
  }
  const percent = unit === null && rest.endsWith('%');
  if (percent) rest = rest.slice(0, -1).replace(/ $/, '');
  let read = body(rest, percent);
  if (
    read === 'syntax' &&
    rest.split(',').length === 2 &&
    typeof body(rest.replace(',', '.'), percent) !== 'string'
  )
    read = 'decimal-comma';
  if (typeof read === 'string') return { ok: false, reason: read };
  return { ok: true, ...read, value: negative ? neg(read.value) : read.value, unit };
}

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

/** Writes an exact value in a form, en-GB, so that `parseNumber` reads back the same form and value. */
export function formatNumber(a: Rational, form: NumForm): string {
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
      if (a.d === 1n) throw new RangeError('an integer has no mixed form');
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
