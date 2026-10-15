import { readFileSync } from 'node:fs';
import { cos, log } from '@zq/mathcore/dmath';
import { hash32, philox4x32, seedSource } from '@zq/mathcore/rng';
import type { Rng } from '@zq/contracts/base';
import fc from 'fast-check';
import { describe, expect, it } from 'vitest';
import {
  fromHex,
  mismatches,
  nearNormal,
  parseGoldens,
  renderNormalBits,
  stream,
  toBits,
} from './rng-goldens.ts';

const read = (name: string): string => readFileSync(new URL(name, import.meta.url), 'utf8');
const goldens = parseGoldens(read('./rng.golden.jsonl'));
const TWO_32 = 2 ** 32;
const TWO_53 = 2 ** 53;
const word = fc.integer({ min: 0, max: TWO_32 - 1 });
const index = fc.integer({ min: 0, max: TWO_53 - 1 });
const name = fc.string({ unit: 'binary', maxLength: 12 });
const BAD_NUMBERS = [NaN, Infinity, -Infinity, 0.5, -1.5, 2 ** 53, -(2 ** 53), 1e21, 5e-324];

/** Spec items 3 and 4 from the block function: draw j's words and at(j). */
function spec(key: readonly [number, number], j: number): { u: number; v: number; at: number } {
  const h = j % 2;
  const b = (j - h) / 2;
  const w = philox4x32([b % TWO_32, Math.floor(b / TWO_32), 0, 0], key);
  const [u = 0, v = 0] = w.slice(2 * h);
  return { u, v, at: (Math.floor(u / 32) * 2 ** 26 + Math.floor(v / 64)) / TWO_53 };
}

describe('philox4x32 against Random123', () => {
  // Every non-comment line: name, rounds, counter c0 to c3, key k0 k1, expected w0 to w3, in hexadecimal.
  const kats = read('./philox4x32-10.kat.txt')
    .split('\n')
    .filter((line) => line.trim() !== '' && !line.startsWith('#'))
    .map((line) => line.trim().split(/\s+/));

  it('passes all 55 known-answer vectors of philox4x32 10', () => {
    expect(kats).toHaveLength(55);
    for (const [label, rounds, ...hex] of kats) {
      expect([label, rounds, hex.length]).toEqual(['philox4x32', '10', 10]);
      const [c0 = 0, c1 = 0, c2 = 0, c3 = 0, k0 = 0, k1 = 0, ...want] = hex.map((x) => parseInt(x, 16));
      expect(philox4x32([c0, c1, c2, c3], [k0, k1])).toEqual(want);
    }
  });

  it('agrees with a BigInt reference of the paper round on random blocks', () => {
    const MASK = 0xffffffffn;
    const reference = (c: bigint[], k: bigint[]): number[] => {
      let [c0 = 0n, c1 = 0n, c2 = 0n, c3 = 0n] = c;
      let [k0 = 0n, k1 = 0n] = k;
      for (let r = 0; r < 10; r++) {
        if (r > 0) [k0, k1] = [(k0 + 0x9e3779b9n) & MASK, (k1 + 0xbb67ae85n) & MASK];
        const p0 = 0xd2511f53n * c0;
        const p1 = 0xcd9e8d57n * c2;
        [c0, c1, c2, c3] = [(p1 >> 32n) ^ c1 ^ k0, p1 & MASK, (p0 >> 32n) ^ c3 ^ k1, p0 & MASK];
      }
      return [c0, c1, c2, c3].map(Number);
    };
    fc.assert(
      fc.property(fc.tuple(word, word, word, word), fc.tuple(word, word), (c, k) => {
        expect(philox4x32(c, k)).toEqual(reference(c.map(BigInt), k.map(BigInt)));
      }),
    );
  });

  it('refuses a word outside [0, 2^32)', () => {
    for (const bad of [-1, TWO_32, 0.5, NaN]) {
      expect(() => philox4x32([0, 0, bad, 0], [0, 0])).toThrow(RangeError);
      expect(() => philox4x32([0, 0, 0, 0], [0, bad])).toThrow(RangeError);
    }
  });
});

describe('hash32', () => {
  const bytes = new TextEncoder();
  /** The spec's FNV-1a in BigInt, over TextEncoder's UTF-8 of well-formed parts. */
  const fnv = (parts: (string | number)[]): number => {
    let h = 2166136261n;
    for (const byte of bytes.encode(parts.map(String).join('\u001f')))
      h = ((h ^ BigInt(byte)) * 16777619n) % 2n ** 32n;
    return Number(h);
  };
  const LONE = /[\ud800-\udfff]/u;

  it('meets every hash32 golden, refusals included', () => {
    const lines = goldens.filter((g) => g.kind === 'hash32');
    expect(lines).toHaveLength(56);
    expect(lines.flatMap(mismatches)).toEqual([]);
  });

  it('is FNV-1a over UTF-8 for strings and safe integers', () => {
    const part = fc.oneof(name, fc.maxSafeInteger(), fc.constant(-0));
    fc.assert(
      fc.property(fc.array(part, { maxLength: 5 }), (parts) => {
        expect(hash32(...parts)).toBe(fnv(parts));
      }),
    );
  });

  it('throws RangeError exactly for a lone surrogate', () => {
    const unit = fc.oneof(fc.integer({ min: 0, max: 0xffff }), fc.integer({ min: 0xd7f0, max: 0xe00f }));
    const text = fc.array(unit, { maxLength: 8 }).map((units) => String.fromCharCode(...units));
    fc.assert(
      fc.property(text, (s) => {
        if (LONE.test(s)) expect(() => hash32('a', s)).toThrow(RangeError);
        else expect(hash32('a', s)).toBe(fnv(['a', s]));
      }),
    );
  });

  it('throws RangeError for a number that is not a safe integer and a part of another type', () => {
    for (const bad of BAD_NUMBERS) expect(() => hash32('gen', bad)).toThrow(RangeError);
    const notSafe = fc.double().filter((x) => !Number.isSafeInteger(x));
    fc.assert(
      fc.property(notSafe, (x) => {
        expect(() => hash32(x)).toThrow(RangeError);
      }),
    );
    const others: unknown[] = [true, null, undefined, 1n, {}];
    for (const other of others) expect(() => hash32(other as string)).toThrow(RangeError);
  });
});

describe('seedSource', () => {
  it('keeps a seed in [0, 2^32) and refuses any other', () => {
    expect(seedSource(0).seed).toBe(0);
    expect(Object.is(seedSource(-0).seed, 0)).toBe(true);
    expect(seedSource(TWO_32 - 1).seed).toBe(TWO_32 - 1);
    for (const bad of [-1, TWO_32, 0.5, NaN, Infinity]) expect(() => seedSource(bad)).toThrow(RangeError);
  });
});

describe('draws', () => {
  it('meets every draw golden: key, words and at(j) bit for bit', () => {
    const lines = goldens.filter((g) => g.kind === 'draw');
    expect(lines).toHaveLength(220);
    expect(lines.flatMap(mismatches)).toEqual([]);
  });

  it('follows spec items 2 to 4 from the block function, for streams and forks', () => {
    fc.assert(
      fc.property(word, name, name, index, (seed, s, f, j) => {
        expect(seedSource(seed).rng(s).at(j)).toBe(spec([seed, hash32(s)], j).at);
        expect(seedSource(seed).rng(s).fork(f).at(j)).toBe(spec([seed, hash32(hash32(s), f)], j).at);
      }),
    );
  });

  it('gives multiples of 2^-53 in [0, 1)', () => {
    fc.assert(
      fc.property(word, name, index, (seed, s, j) => {
        const x = seedSource(seed).rng(s).at(j);
        expect(x >= 0 && x < 1 && Number.isInteger(x * TWO_53)).toBe(true);
      }),
    );
  });

  it('keeps at() pure whatever was drawn before', () => {
    fc.assert(
      fc.property(word, fc.array(index, { minLength: 1, maxLength: 8 }), (seed, js) => {
        const rng = seedSource(seed).rng('pure');
        for (const j of js) expect(rng.at(j)).toBe(seedSource(seed).rng('pure').at(j));
      }),
    );
  });

  it('refuses an index outside [0, 2^53)', () => {
    const rng = seedSource(1).rng('s');
    expect(rng.at(TWO_53 - 1)).toBe(spec([1, hash32('s')], TWO_53 - 1).at);
    for (const bad of [-1, TWO_53, 0.5, NaN, Infinity]) expect(() => rng.at(bad)).toThrow(RangeError);
  });

  it('moves the position by next(), int() and normal() only (spec items 5 to 7)', () => {
    const op = fc.oneof(
      fc.constant({ op: 'next' as const }),
      fc.record({ op: fc.constant('at' as const), j: fc.nat(40) }),
      fc.constant({ op: 'normal' as const }),
      fc.constant({ op: 'fork' as const }),
    );
    fc.assert(
      fc.property(word, fc.array(op, { maxLength: 12 }), (seed, ops) => {
        const rng = seedSource(seed).rng('position');
        let p = 0;
        for (const o of ops) {
          if (o.op === 'next') expect(rng.next()).toBe(rng.at(p++));
          else if (o.op === 'at') expect(rng.at(o.j)).toBe(stream(seed, ['position']).at(o.j));
          else if (o.op === 'normal') {
            rng.normal();
            p += 2;
          } else expect(rng.fork('child').next()).toBe(stream(seed, ['position', 'child']).at(0));
        }
        expect(rng.next()).toBe(rng.at(p));
      }),
    );
  });

  it('gives distinct forks independent streams, none moved by its parent', () => {
    fc.assert(
      fc.property(word, name, name, fc.nat(5), (seed, a, b, skip) => {
        fc.pre(a !== b);
        const parent = seedSource(seed).rng('parent');
        for (let k = 0; k < skip; k++) parent.next();
        const [x, y] = [parent.fork(a), parent.fork(b)];
        const draws = (rng: Rng): number[] => [0, 1, 2, 3].map((j) => rng.at(j));
        expect(draws(x)).toEqual(draws(seedSource(seed).rng('parent').fork(a)));
        expect(draws(x)).not.toEqual(draws(y));
        expect(draws(x)).not.toEqual(draws(parent));
        expect(parent.next()).toBe(parent.at(skip));
      }),
    );
  });
});

describe('int', () => {
  it('meets every int golden, values and positions', () => {
    const lines = goldens.filter((g) => g.kind === 'int');
    expect(lines).toHaveLength(32);
    expect(lines.flatMap(mismatches)).toEqual([]);
  });

  it('is spec item 6: rejection on word u below 2^32 - (2^32 mod n), then lo + u mod n', () => {
    const size = fc.oneof(
      fc.integer({ min: 1, max: 12 }),
      fc.constantFrom(2 ** 31 + 1, 3 * 2 ** 30, TWO_32),
      word.filter(Boolean),
    );
    fc.assert(
      fc.property(
        word,
        size,
        fc.integer({ min: -(2 ** 31), max: 2 ** 31 }),
        fc.nat(3),
        (seed, n, lo, skip) => {
          const key = [seed, hash32('int')] as const;
          const rng = seedSource(seed).rng('int');
          for (let k = 0; k < skip; k++) rng.next();
          const limit = TWO_32 - (TWO_32 % n);
          let p = skip;
          while (spec(key, p).u >= limit) p++;
          const got = rng.int(lo, lo + n - 1);
          expect(got).toBe(lo + (spec(key, p).u % n));
          expect(got >= lo && got <= lo + n - 1 && Number.isSafeInteger(got)).toBe(true);
          expect(rng.next()).toBe(rng.at(p + 1));
        },
      ),
    );
  });

  it('reaches both ends of the safe range and refuses anything else', () => {
    const rng = seedSource(3).rng('ends');
    const MAX = Number.MAX_SAFE_INTEGER;
    expect(rng.int(MAX, MAX)).toBe(MAX);
    expect(rng.int(-MAX, -MAX)).toBe(-MAX);
    expect(rng.int(-MAX, -MAX + TWO_32 - 1)).toBeLessThanOrEqual(-MAX + TWO_32 - 1);
    const refused: [number, number][] = [
      [1, 0],
      [0, TWO_32],
      [-MAX, MAX],
      [0.5, 2],
      [0, NaN],
      [NaN, 0],
      [MAX + 1, MAX + 1],
    ];
    for (const [lo, hi] of refused) expect(() => rng.int(lo, hi)).toThrow(RangeError);
  });
});

describe('normal', () => {
  it('meets every normal and sequence golden within 1e-14 max(1, r), positions exact', () => {
    const lines = goldens.filter((g) => g.kind === 'normal' || g.kind === 'sequence');
    expect(lines).toHaveLength(8);
    expect(lines.flatMap(mismatches)).toEqual([]);
  });

  it('is sqrt(-2 log(1 - u1)) cos(tau u2) in dmath, from the next two draws', () => {
    fc.assert(
      fc.property(word, name, fc.nat(4), (seed, s, skip) => {
        const rng = seedSource(seed).rng(s);
        for (let k = 0; k < skip; k++) rng.next();
        const [u1, u2] = [rng.at(skip), rng.at(skip + 1)];
        const x = rng.normal();
        expect(x).toBe(Math.sqrt(-2 * log(1 - u1)) * cos(6.283185307179586 * u2));
        expect(Math.abs(x)).toBeLessThan(Math.sqrt(-2 * log(2 ** -53)) + 1e-12);
        expect(rng.next()).toBe(rng.at(skip + 2));
      }),
    );
  });

  it('records its own bits for the browser engines', async () => {
    await expect(renderNormalBits(goldens)).toMatchFileSnapshot('./rng.normal-bits.txt');
  });
});

describe('the golden readers', () => {
  it('read float.hex exactly and refuse other text', () => {
    expect(fromHex('0x1.0000000000000p+0')).toBe(1);
    expect(fromHex('-0x1.8000000000000p-1')).toBe(-0.75);
    expect(fromHex('0x1.fffffffffffffp+1023')).toBe(Number.MAX_VALUE);
    expect(fromHex('0x0.0000000000001p-1022')).toBe(5e-324);
    expect(Object.is(fromHex('-0x0.0p+0'), -0)).toBe(true);
    expect(toBits(fromHex('0x1.c79246bc37e00p-5'))).toBe('3fac79246bc37e00');
    for (const bad of ['1.5', '0x1.0p+1024', '0x0.1p+0', '0x2.0p+0']) expect(() => fromHex(bad)).toThrow();
    expect(nearNormal(1 + 1e-14, '0x1.0000000000000p+0', '0x1.0000000000000p+0')).toBe(true);
    expect(nearNormal(1 + 3e-14, '0x1.0000000000000p+0', '0x1.0000000000000p+1')).toBe(false);
  });
});
