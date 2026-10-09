// Counter-based random draws and the one seed hash (docs/ARCHITECTURE.md 5.1; CONTENT-FORMAT.md 5.3): every
// seeded number a widget shows or a generator builds is a pure function of (seed, stream, index). Written
// from the stage 3 specification of `@zq/mathcore/rng`, items 1 to 8; tools/zqverify/rng.py is its blind
// Python twin, and test/rng.golden.jsonl holds that twin's output. Decision notes:
// - Philox4x32-10 (Salmon, Moraes, Dror and Shaw, SC11, 2011) as Random123 implements `philox4x32_R` with
//   R = 10: multipliers 0xD2511F53 and 0xCD9E8D57, Weyl key increments 0x9E3779B9 and 0xBB67AE85, the round
//   (hi1 ^ c1 ^ k0, lo1, hi0 ^ c3 ^ k1, lo0) and ten rounds with the key bumped before each after the first
//   [sourced: Random123 include/Random123/philox.h at commit 9545ff6, lines 241, 244, 255, 258, 295 to 305,
//   307 to 312 and 323 to 334, read in a clone on 9 October 2026]. All 55 of Random123's `philox4x32 10`
//   known-answer lines pass (test/philox4x32-10.kat.txt).
// - No BigInt: the 32 x 32 multiply is exact in doubles. Math.imul gives the low word. For the high word
//   each factor splits into 16-bit halves, so each of the four partial products is below 2^32 and exact;
//   the high word is the top product plus the top halves of the two cross products plus the carry out of
//   the low 32 bits, (ll >>> 16) + the low halves of the cross products, which is below 3 * 2^16. Every sum
//   stays below 2^33, so no step rounds [inferred from IEEE-754 binary64's 53-bit significand].
// - Draw j uses block floor(j / 2), so a draw costs one block whatever j is. An Rng keeps its last block,
//   which halves the work of a run of next() calls without changing any value.
// - at(j) is 27 bits of u above 26 bits of v over 2^53, the construction of MT19937's genrand_res53
//   [recalled]: an exact multiple of 2^-53 in [0, 1). normal() is the cosine half of Box-Muller,
//   sqrt(-2 ln(1 - u1)) * cos(tau * u2), with dmath's log and cos, so its bits are the same on every engine;
//   Math.sqrt is correctly rounded by ECMA-262 [sourced: tc39/ecma262 spec.html at 6db9135, sec-math.sqrt].
// - hash32 is 32-bit FNV-1a over the UTF-8 bytes of the parts joined by U+001F, encoded here in one pass
//   with no TextEncoder, which would write U+FFFD for a lone surrogate. A lone surrogate, a number part that
//   is not a safe integer and a part of any other type throw RangeError: above 2^53 ECMA-262 fixes a
//   number's last decimal digit only in a non-normative note [sourced: tc39/ecma262 spec.html at 6db9135,
//   sec-numeric-types-number-tostring, as cited by the specification's item 8].
// - Errors are RangeErrors with fixed messages that never echo a part, which may be learner text (PLAN.md
//   8.4). Every function is O(1) but hash32, O(total length of the parts), and int, whose rejection keeps a
//   word with probability above 1/2 (the limit exceeds 2^31), so it takes fewer than two draws on average.
import type { Rng, SeedSource } from '@zq/contracts/base';
import { cos, log } from './dmath.ts';

const TWO_32 = 4294967296;
const TWO_53 = 9007199254740992;
const TWO_26 = 67108864;
/** The double nearest 2 pi. */
const TAU = 6.283185307179586;

const M0 = 0xd2511f53;
const M1 = 0xcd9e8d57;
const M0_LO = M0 & 0xffff;
const M0_HI = M0 >>> 16;
const M1_LO = M1 & 0xffff;
const M1_HI = M1 >>> 16;
const W0 = 0x9e3779b9;
const W1 = 0xbb67ae85;

const FNV_OFFSET = 0x811c9dc5;
const FNV_PRIME = 0x01000193;
const SEPARATOR = 0x1f;

/** The high 32 bits of the 64-bit product of the word a and a multiplier given as 16-bit halves. */
function mulhi(a: number, mLo: number, mHi: number): number {
  const aLo = a & 0xffff;
  const aHi = a >>> 16;
  const cross1 = aLo * mHi;
  const cross2 = aHi * mLo;
  const carry = ((aLo * mLo) >>> 16) + (cross1 & 0xffff) + (cross2 & 0xffff);
  return aHi * mHi + (cross1 >>> 16) + (cross2 >>> 16) + (carry >>> 16);
}

type Block = [number, number, number, number];

/** Ten Philox rounds on words held as int32 or uint32; the output words are unsigned. */
function block(c0: number, c1: number, c2: number, c3: number, k0: number, k1: number): Block {
  for (let round = 0; round < 10; round++) {
    if (round > 0) {
      k0 = (k0 + W0) | 0;
      k1 = (k1 + W1) | 0;
    }
    const hi0 = mulhi(c0, M0_LO, M0_HI);
    const lo0 = Math.imul(M0, c0);
    const hi1 = mulhi(c2, M1_LO, M1_HI);
    const lo1 = Math.imul(M1, c2);
    c0 = hi1 ^ c1 ^ k0;
    c1 = lo1;
    c2 = hi0 ^ c3 ^ k1;
    c3 = lo0;
  }
  return [c0 >>> 0, c1 >>> 0, c2 >>> 0, c3 >>> 0];
}

const isWord = (x: number): boolean => Number.isInteger(x) && x >= 0 && x < TWO_32;

/** The Philox4x32-10 block function: four unsigned 32-bit counter words and two key words to four words. */
export function philox4x32(
  counter: readonly [number, number, number, number],
  key: readonly [number, number],
): Block {
  if (!counter.every(isWord) || !key.every(isWord)) {
    throw new RangeError('philox4x32: every counter and key word must be an integer in [0, 2^32)');
  }
  return block(counter[0], counter[1], counter[2], counter[3], key[0], key[1]);
}

/** FNV-1a's step for one byte. */
const step = (h: number, byte: number): number => Math.imul(h ^ byte, FNV_PRIME);

function hashText(h: number, text: string): number {
  for (let i = 0; i < text.length; i++) {
    const c = text.charCodeAt(i);
    if (c < 0x80) {
      h = step(h, c);
    } else if (c < 0x800) {
      h = step(step(h, 0xc0 | (c >> 6)), 0x80 | (c & 0x3f));
    } else if (c < 0xd800 || c > 0xdfff) {
      h = step(step(step(h, 0xe0 | (c >> 12)), 0x80 | ((c >> 6) & 0x3f)), 0x80 | (c & 0x3f));
    } else {
      // charCodeAt past the end is NaN, which fails the range test.
      const d = text.charCodeAt(i + 1);
      if (c > 0xdbff || !(d >= 0xdc00 && d <= 0xdfff)) {
        throw new RangeError('hash32: a string part holds a lone surrogate, which has no UTF-8 form');
      }
      const p = 0x10000 + ((c - 0xd800) << 10) + (d - 0xdc00);
      h = step(step(h, 0xf0 | (p >> 18)), 0x80 | ((p >> 12) & 0x3f));
      h = step(step(h, 0x80 | ((p >> 6) & 0x3f)), 0x80 | (p & 0x3f));
      i++;
    }
  }
  return h;
}

/**
 * 32-bit FNV-1a over the UTF-8 bytes of the parts joined by U+001F, a number part written as String(n);
 * unsigned. Throws RangeError for a number part that is not a safe integer, a lone surrogate in a string
 * part, or a part that is neither.
 */
export function hash32(...parts: readonly (string | number)[]): number {
  let h = FNV_OFFSET | 0;
  let first = true;
  for (const part of parts) {
    if (!first) h = step(h, SEPARATOR);
    first = false;
    if (typeof part === 'string') h = hashText(h, part);
    else if (Number.isSafeInteger(part)) h = hashText(h, String(part));
    else throw new RangeError('hash32: a part must be a string or a safe integer');
  }
  return h >>> 0;
}

class Philox implements Rng {
  readonly #seed: number;
  readonly #stream: number;
  #position = 0;
  // The last block computed, by block index, and its four words.
  #block = -1;
  #words: Block = [0, 0, 0, 0];

  constructor(seed: number, stream: number) {
    this.#seed = seed;
    this.#stream = stream;
  }

  /** Draw j's two words (u, v), from block floor(j / 2). */
  #draw(index: number): readonly [number, number] {
    if (!Number.isSafeInteger(index) || index < 0) {
      throw new RangeError('rng: a draw index must be an integer in [0, 2^53)');
    }
    const odd = index % 2;
    const b = (index - odd) / 2;
    if (b !== this.#block) {
      const lo = b % TWO_32;
      this.#words = block(lo, (b - lo) / TWO_32, 0, 0, this.#seed, this.#stream);
      this.#block = b;
    }
    const [w0, w1, w2, w3] = this.#words;
    return odd === 0 ? [w0, w1] : [w2, w3];
  }

  at(index: number): number {
    const [u, v] = this.#draw(index);
    return ((u >>> 5) * TWO_26 + (v >>> 6)) / TWO_53;
  }

  next(): number {
    const x = this.at(this.#position);
    this.#position += 1;
    return x;
  }

  int(lo: number, hi: number): number {
    const n = hi - lo + 1;
    if (!Number.isSafeInteger(lo) || !Number.isSafeInteger(hi) || lo > hi || n > TWO_32) {
      throw new RangeError('rng: int takes safe integers lo <= hi with at most 2^32 values');
    }
    const limit = TWO_32 - (TWO_32 % n);
    for (;;) {
      const [u] = this.#draw(this.#position);
      this.#position += 1;
      if (u < limit) return lo + (u % n);
    }
  }

  normal(): number {
    const u1 = this.next();
    const u2 = this.next();
    return Math.sqrt(-2 * log(1 - u1)) * cos(TAU * u2);
  }

  fork(stream: string): Rng {
    return new Philox(this.#seed, hash32(this.#stream, stream));
  }
}

/** The seed source for a seed in [0, 2^32): `rng(name)` has the key (seed, hash32(name)) and starts at 0. */
export function seedSource(seed: number): SeedSource {
  if (!isWord(seed)) throw new RangeError('rng: a seed must be an integer in [0, 2^32)');
  const s = seed >>> 0;
  return { seed: s, rng: (stream: string): Rng => new Philox(s, hash32(stream)) };
}
