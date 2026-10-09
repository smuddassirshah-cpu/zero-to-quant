// en-GB number parsing for numeric answers, shared with the graders (docs/CONTENT-FORMAT.md 7.2; WIDGETS.md
// 4.2.2 `numeric-input`). Decision notes:
// - The parser reads and classifies; it does not grade. It returns the form the learner typed, its exact
//   value and, for a fraction or a mixed number, the parts as typed, so the grader (stage 20) can apply the
//   check's `forms`, `integer`, `probability`, `sf`, `dp`, unit and `requireForm` rules, lowest terms
//   included, and every widget's parse preview reads a typed number the same way.
// - Normalisation is 7.2's: U+2212 and the dashes become "-", "×" and "·" (and the dot operator U+22C5)
//   become "*". A thin or no-break space is removed only where a comma would group digits (a first group of
//   1 to 3 digits, then groups of exactly 3, as in 1,000), and never inside another number or an exponent
//   (after "e", "E" or "^" and an optional sign, so "3.2e1 000" fails); anywhere else it is an ordinary
//   space, so 2 1/3 typed with a no-break space stays a mixed number [our choice, adversarial review of 8
//   October 2026]. Runs of spaces and tabs collapse to one space and ASCII whitespace is trimmed [our
//   choice]. Lengths are UTF-16 code units, JavaScript's own.
// - A run grouped by narrow spaces and then "/" (after an optional space) fails as `syntax`: "2 125/250"
//   typed with a no-break space reads as the grouped 2125/250 and as the mixed 2 125/250, both valid and
//   different, and a nudge costs no attempt where a wrong value does (B47) [our choice, review of 9 October
//   2026]. The test is the shape alone, so "12 345/7" fails too, though its mixed reading is improper, and
//   so does "1 000/0", which is `syntax`, not `zero-denominator`.
// - Grouping commas: a first group of 1 to 3 digits not starting with 0, then groups of exactly 3 (7.2's "a
//   comma between digit groups of three"); "0,500" is therefore a decimal comma, not five hundred [our
//   choice]. A string that fails but parses with its one comma read as a point fails as `decimal-comma`,
//   7.2's nudge.
// - Accepted: one leading "-" or "+", then an optional space ("+33.1%", "− 5"), 7.2's six forms, and one
//   listed unit, compared without case and typed before or after the number (a listed "%" is read as that
//   unit, not as the percent form) [our choice]. A percent's value is the number before its sign ("25%" is
//   25); the grader divides by 100 where the answer is a proportion (7.2). A mixed number's fraction is
//   proper and non-zero. Anything else fails.
// - Inputs longer than INPUT_LIMIT characters fail, and exponents are bounded by rational.ts, so a typed
//   string cannot make a large BigInt [our choice: 200 is NumValue's own limit, CONTENT-FORMAT.md 3.2].
import { EXPONENT_LIMIT, add, fromDecimal, neg, rat, type Rational } from './rational.ts';

export type NumForm = 'integer' | 'decimal' | 'fraction' | 'mixed' | 'percent' | 'standard-form';
export type ParseFailure =
  'empty' | 'too-long' | 'decimal-comma' | 'zero-denominator' | 'out-of-range' | 'syntax';

/**
 * A fraction or mixed number as typed, unsigned and unreduced: "4/6" keeps 4 and 6, and a fraction's whole
 * is 0. The sign is on the value. `requireForm: 'simplest-fraction'` checks gcd(n, d) = 1 on these parts.
 */
interface TypedFraction {
  readonly whole: bigint;
  readonly n: bigint;
  readonly d: bigint;
}

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
  /** The parts typed, for the fraction and mixed forms; null otherwise. */
  readonly typed: TypedFraction | null;
}
export type NumParse = ParsedNumber | { readonly ok: false; readonly reason: ParseFailure };

export const INPUT_LIMIT = 200;

const INT = String.raw`(?:[1-9]\d{0,2}(?:,\d{3})+|\d+)`;
const MIXED = new RegExp(String.raw`^(${INT}) (${INT}) ?/ ?(${INT})$`);
const FRACTION = new RegExp(String.raw`^(${INT}) ?/ ?(${INT})$`);
const DECIMAL = new RegExp(String.raw`^(${INT})?(?:\.(\d*))?(?:[eE]([+-]?\d+)| ?[*xX] ?10\^([+-]?\d+))?$`);
const DASHES = String.raw`\u2010-\u2015\u2212\uFE58\uFE63\uFF0D`;
const NARROWS = String.raw`\u00A0\u2007\u2009\u200A\u202F`;
const DASH = new RegExp(`[${DASHES}]`, 'g');
const NARROW = new RegExp(`[${NARROWS}]`, 'g');
// A digit grouping spelled with narrow spaces: the shape of a grouped INT, not inside another number or an
// exponent. The sign class takes the raw dashes too, so the slash test below can run before normalising.
const RUN = String.raw`(?<![\d.,]|[eE^][-+${DASHES}]?)[1-9]\d{0,2}(?:[${NARROWS}]\d{3})+(?!\d)`;
const NARROW_GROUPED = new RegExp(RUN, 'g');
const GROUPED_SLASH = new RegExp(String.raw`${RUN}[ \t${NARROWS}]*/`);

/** CONTENT-FORMAT.md 7.2's normalisation; runs of spaces collapsed, ASCII whitespace trimmed. */
export const normalise = (text: string): string =>
  text
    .replace(DASH, '-')
    .replace(NARROW_GROUPED, (run) => run.replace(NARROW, ''))
    .replace(NARROW, ' ')
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
    const value = add(rat(whole), rat(n, d));
    return { form: mixed ? 'mixed' : 'fraction', value, places: 0, figures: 0, typed: { whole, n, d } };
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
    typed: null,
  };
}

/** Reads a typed number. `units` lists the unit spellings the field accepts ("£", "bp", "outcomes"). */
export function parseNumber(input: string, units: readonly string[] = []): NumParse {
  if (input.length > INPUT_LIMIT) return { ok: false, reason: 'too-long' };
  const text = normalise(input);
  if (text === '') return { ok: false, reason: 'empty' };
  if (GROUPED_SLASH.test(input)) return { ok: false, reason: 'syntax' };
  const sign = /^[-+] ?/.exec(text)?.[0] ?? '';
  let rest = text.slice(sign.length);
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
  return { ok: true, ...read, value: sign.startsWith('-') ? neg(read.value) : read.value, unit };
}
