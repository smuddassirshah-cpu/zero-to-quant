// Exact rationals over BigInt (docs/ARCHITECTURE.md 4.3; CONTENT-FORMAT.md 5.3 and 7.2). Decision notes:
// - Canonical form always: the denominator is positive and gcd(|n|, d) = 1, so equality is a field compare
//   and a value has one spelling, `spell`'s "n/d" (or "n"), the authored `NumValue` form.
// - Immutable plain objects, with no class and no brand, so values cross a worker boundary by structured
//   clone [our choice]. Every function here takes canonical values. One that comes back from structured
//   clone, a `db` document or an import is untrusted (PLAN.md 7.2), so that boundary checks it with
//   `isRational` before use. `terminates` checks too, because a zero denominator would loop forever and an
//   unreduced one can give the wrong answer [our choice, review of #26].
// - The grammar of `parse` is CONTENT-FORMAT.md 7.2's integer, fraction and decimal spellings and its
//   standard form in e-notation, with nothing around them: callers such as num-parse.ts remove grouping,
//   spaces and units first. Text with a "/" is a fraction, `-?\d+/\d+`; anything else is a decimal,
//   `-?\d*(\.\d*)?([eE][+-]?\d+)?` with a digit in the mantissa and an exponent of at most EXPONENT_LIMIT
//   in size. ASCII digits only, an optional `-` on n, never `+`, and no sign on d.
// - Errors are RangeErrors with fixed messages that never echo the text, which may be a learner's answer
//   (PLAN.md 8.4): a zero denominator, a non-integer or unsafe number, a malformed string, an exponent beyond
//   EXPONENT_LIMIT, and a value that is not canonical given to `terminates`.
// - Time grows with the square of the text's length, because gcd is a Euclid loop over BigInt: `fromDecimal`
//   of "0." and 5,000 digits takes 30 ms, 20,000 digits 0.76 s and 50,000 digits 6.0 s, and `parse` of "n/d"
//   with 20,000 digits each 0.76 s [measured: review of #26]. Callers bound the length: num-parse.ts's
//   INPUT_LIMIT of 200 for typed answers and NumValue's 200 characters for authored ones (CONTENT-FORMAT.md
//   3.2). EXPONENT_LIMIT bounds the size of the result (the text's length plus 1,000 digits), not the time.
//   `terminates` takes one BigInt division per factor of 2 or 5 in d, 3.8 s for 1/2^200000 [measured:
//   review of #26]; a value parsed from 200 characters has at most about 1,200 digits in d [inferred]. A
//   length cap inside `parse` was rejected: `spell(fromDecimal('1e1000'))` is 1,001 characters, and the
//   round trip through `spell` must hold.
export interface Rational {
  readonly n: bigint;
  readonly d: bigint;
}

export const EXPONENT_LIMIT = 1000;

const DECIMAL = /^(-?)(\d*)(?:\.(\d*))?(?:[eE]([+-]?\d+))?$/;
const FRACTION = /^-?\d+\/\d+$/;
const SIGNED_DENOMINATOR = /^-?\d+\/[-+]\d+$/;

function gcd(a: bigint, b: bigint): bigint {
  while (b !== 0n) [a, b] = [b, a % b];
  return a;
}

function big(x: bigint | number): bigint {
  if (typeof x === 'bigint') return x;
  if (!Number.isSafeInteger(x)) throw new RangeError('not a safe integer');
  return BigInt(x);
}

/** n/d in lowest terms with a positive denominator. Throws on a zero denominator. */
export function rat(n: bigint | number, d: bigint | number = 1n): Rational {
  let [p, q] = [big(n), big(d)];
  if (q === 0n) throw new RangeError('division by zero');
  if (q < 0n) [p, q] = [-p, -q];
  const g = gcd(p < 0n ? -p : p, q);
  return { n: p / g, d: q / g };
}

/** True for a canonical value: bigint n and d, d > 0 and gcd(|n|, d) = 1. For values crossing a boundary. */
export function isRational(x: unknown): x is Rational {
  if (typeof x !== 'object' || x === null || !('n' in x && 'd' in x)) return false;
  const { n, d } = x;
  return typeof n === 'bigint' && typeof d === 'bigint' && d > 0n && gcd(n < 0n ? -n : n, d) === 1n;
}

export const add = (a: Rational, b: Rational): Rational => rat(a.n * b.d + b.n * a.d, a.d * b.d);
export const sub = (a: Rational, b: Rational): Rational => rat(a.n * b.d - b.n * a.d, a.d * b.d);
export const mul = (a: Rational, b: Rational): Rational => rat(a.n * b.n, a.d * b.d);
export const div = (a: Rational, b: Rational): Rational => rat(a.n * b.d, a.d * b.n);
export const neg = (a: Rational): Rational => ({ n: -a.n, d: a.d });

/** -1, 0 or 1 as a is below, equal to or above b. */
export function cmp(a: Rational, b: Rational): -1 | 0 | 1 {
  const l = a.n * b.d;
  const r = b.n * a.d;
  return l < r ? -1 : l > r ? 1 : 0;
}

export const eq = (a: Rational, b: Rational): boolean => a.n === b.n && a.d === b.d;

/** The canonical spelling: "n" for an integer, otherwise "n/d", with an ASCII minus. */
export const spell = (a: Rational): string => (a.d === 1n ? `${a.n}` : `${a.n}/${a.d}`);

/** True when the decimal expansion terminates: d has no prime factor but 2 and 5. Throws if not canonical. */
export function terminates(a: Rational): boolean {
  if (!isRational(a)) throw new RangeError('not a canonical rational');
  let d = a.d;
  while (d % 2n === 0n) d /= 2n;
  while (d % 5n === 0n) d /= 5n;
  return d === 1n;
}

/**
 * A terminating decimal in ASCII: "-12.5", ".25", "305.", "3.2e-4", "1E+3". An optional `-`, never `+`, on
 * the mantissa; no grouping and no other characters.
 */
export function fromDecimal(text: string): Rational {
  const m = DECIMAL.exec(text);
  const [, sign = '', whole = '', frac = '', exp = '0'] = m ?? [];
  if (!m || whole + frac === '') throw new RangeError('not a decimal');
  if (Math.abs(Number(exp)) > EXPONENT_LIMIT) throw new RangeError(`exponent beyond ${EXPONENT_LIMIT}`);
  const e = Number(exp) - frac.length;
  const digits = BigInt(sign + whole + frac);
  return e >= 0 ? rat(digits * 10n ** BigInt(e)) : rat(digits, 10n ** BigInt(-e));
}

/**
 * Any of these spellings to a value: "n", "n/d" with an optional `-` on n, never `+`, or a terminating
 * decimal as `fromDecimal` reads it. Non-canonical spellings ("6/4", "007", "-0") are read too.
 */
export function parse(text: string): Rational {
  if (!text.includes('/')) return fromDecimal(text);
  if (!FRACTION.test(text)) {
    throw new RangeError(SIGNED_DENOMINATOR.test(text) ? 'sign on the denominator' : 'not a fraction');
  }
  const [n, d] = text.split('/').map(BigInt) as [bigint, bigint];
  return rat(n, d);
}
