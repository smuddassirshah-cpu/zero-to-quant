// Shared by rng.test.ts (Node) and rng.browser.test.ts: reads the goldens tools/zqverify/rng.py writes
// (doubles as Python float.hex strings), replays every line against @zq/mathcore/rng, and renders the bits
// golden of normal(). Each line starts from a fresh Rng: `path` is the stream name, then the fork names in
// order. Positions are checked by replaying a prefix on a fresh Rng: after it, next() must equal at(p).
import { hash32, philox4x32, seedSource } from '@zq/mathcore/rng';
import type { Rng } from '@zq/contracts/base';

type Path = [string, ...string[]];
type Op =
  | ['next', string, number]
  | ['at', number, string, number]
  | ['int', number, number, number, number]
  | ['normal', string, string, number];
export type Golden =
  | { kind: 'hash32'; parts: (string | number)[]; hash?: number; error?: string }
  | {
      kind: 'draw';
      seed: number;
      path: Path;
      key: [number, number];
      j: number;
      words: [number, number];
      at: string;
    }
  | { kind: 'int'; seed: number; path: Path; n: number; calls: [number, number, number, number][] }
  | { kind: 'normal'; seed: number; path: Path; values: [string, string][] }
  | { kind: 'sequence'; seed: number; path: Path; ops: Op[] };

export function parseGoldens(text: string): Golden[] {
  return text
    .split('\n')
    .filter((line) => line !== '')
    .map((line) => JSON.parse(line) as Golden);
}

const view = new DataView(new ArrayBuffer(8));
const HEX_FLOAT = /^(-?)0x([01])\.([0-9a-f]{1,13})p([+-]\d+)$/;

/** Python's float.hex form to the exact double: 0x1.<13 digits>p<e>, or 0x0.<digits>p-1022 and 0x0.0p+0. */
export function fromHex(text: string): number {
  const [, sign = '', lead = '', digits = '', exponent = ''] = HEX_FLOAT.exec(text) ?? [];
  const fraction = BigInt(`0x${digits.padEnd(13, '0')}`);
  const e = Number(exponent);
  const biased = lead === '1' ? e + 1023 : 0;
  const valid = lead === '1' ? biased > 0 && biased < 2047 : fraction === 0n || e === -1022;
  if (digits === '' || !valid) throw new Error(`not a float.hex double: ${text}`);
  view.setBigUint64(0, (sign === '-' ? 1n << 63n : 0n) | (BigInt(biased) << 52n) | fraction);
  return view.getFloat64(0);
}

/** A double's 64 bits as 16 hexadecimal digits. */
export function toBits(x: number): string {
  view.setFloat64(0, x);
  return view.getBigUint64(0).toString(16).padStart(16, '0');
}

export function stream(seed: number, path: Path): Rng {
  const [name, ...forks] = path;
  return forks.reduce((rng, fork) => rng.fork(fork), seedSource(seed).rng(name));
}

/** The spec's normal tolerance: within 1e-14 max(1, r) of the twin's value, r = sqrt(-2 ln(1 - u1)). */
export const nearNormal = (got: number, value: string, r: string): boolean =>
  Math.abs(got - fromHex(value)) <= 1e-14 * Math.max(1, fromHex(r));

function run(rng: Rng, op: Op): number {
  switch (op[0]) {
    case 'next':
      return rng.next();
    case 'at':
      return rng.at(op[1]);
    case 'int':
      return rng.int(op[1], op[2]);
    case 'normal':
      return rng.normal();
  }
}

function agrees(op: Op, got: number): boolean {
  switch (op[0]) {
    case 'next':
      return Object.is(got, fromHex(op[1]));
    case 'at':
      return Object.is(got, fromHex(op[2]));
    case 'int':
      return Object.is(got, op[3]);
    case 'normal':
      return nearNormal(got, op[1], op[2]);
  }
}

const positionAfter = (op: Op): number => op[op.length - 1] as number;

function replay(seed: number, path: Path, ops: readonly Op[]): string[] {
  const misses: string[] = [];
  const rng = stream(seed, path);
  ops.forEach((op, k) => {
    const got = run(rng, op);
    if (!agrees(op, got)) misses.push(`op ${k} ${JSON.stringify(op)} gave ${got}`);
    const probe = stream(seed, path);
    for (const earlier of ops.slice(0, k + 1)) run(probe, earlier);
    const p = positionAfter(op);
    if (!Object.is(probe.next(), probe.at(p))) misses.push(`op ${k}: the position is not ${p}`);
  });
  return misses;
}

/** The ops a line replays: int calls and normal values become ops, a normal taking two draws (spec 7). */
function opsOf(g: Exclude<Golden, { kind: 'hash32' | 'draw' }>): Op[] {
  if (g.kind === 'sequence') return g.ops;
  if (g.kind === 'int') return g.calls.map(([lo, hi, result, p]) => ['int', lo, hi, result, p]);
  return g.values.map(([value, r], k) => ['normal', value, r, 2 * (k + 1)]);
}

function hashMisses(g: Extract<Golden, { kind: 'hash32' }>): string[] {
  let got: number | string;
  try {
    got = hash32(...g.parts);
  } catch (error) {
    got = error instanceof RangeError ? 'RangeError' : String(error);
  }
  return Object.is(got, g.hash ?? g.error) ? [] : [`hash32 ${JSON.stringify(g.parts)} gave ${got}`];
}

function drawMisses(g: Extract<Golden, { kind: 'draw' }>): string[] {
  const misses: string[] = [];
  const [name, ...forks] = g.path;
  const k1 = forks.reduce((s, fork) => hash32(s, fork), hash32(name));
  if (g.key[0] !== g.seed || g.key[1] !== k1) misses.push(`key ${g.key.join(' ')}, not ${g.seed} ${k1}`);
  const h = g.j % 2;
  const b = (g.j - h) / 2;
  const words = philox4x32([b % 2 ** 32, Math.floor(b / 2 ** 32), 0, 0], g.key).slice(2 * h, 2 * h + 2);
  if (words.join(' ') !== g.words.join(' ')) misses.push(`words ${words.join(' ')}`);
  const at = stream(g.seed, g.path).at(g.j);
  if (!Object.is(at, fromHex(g.at))) misses.push(`at ${toBits(at)}`);
  return misses.map((miss) => `draw ${g.seed} ${JSON.stringify(g.path)} ${g.j}: ${miss}`);
}

/** Every disagreement between @zq/mathcore/rng and one golden line. */
export function mismatches(g: Golden): string[] {
  if (g.kind === 'hash32') return hashMisses(g);
  if (g.kind === 'draw') return drawMisses(g);
  return replay(g.seed, g.path, opsOf(g)).map(
    (miss) => `${g.kind} ${g.seed} ${JSON.stringify(g.path)}: ${miss}`,
  );
}

/** normal()'s own bits for each golden normal line, each normal op of a sequence, and one long stream. */
export function renderNormalBits(goldens: readonly Golden[]): string {
  const lines = [
    '# The bits of @zq/mathcore/rng\'s normal(), as "<golden line> <op> <bits>" for every normal value and',
    '# sequence op of rng.golden.jsonl (line numbers from 1), then "stream <k> <bits>" for 1,000 calls on',
    '# seedSource(20261009).rng("normal-bits"). Written by Node through `vitest run -u`; the browser project',
    '# must reproduce it in every engine.',
  ];
  goldens.forEach((g, i) => {
    if (g.kind !== 'normal' && g.kind !== 'sequence') return;
    const rng = stream(g.seed, g.path);
    opsOf(g).forEach((op, k) => {
      const got = run(rng, op);
      if (op[0] === 'normal') lines.push(`${i + 1} ${k} ${toBits(got)}`);
    });
  });
  const rng = seedSource(20261009).rng('normal-bits');
  for (let k = 0; k < 1000; k++) lines.push(`stream ${k} ${toBits(rng.normal())}`);
  return `${lines.join('\n')}\n`;
}
