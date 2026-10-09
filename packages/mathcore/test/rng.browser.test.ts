// The draws across engines (docs/ARCHITECTURE.md 13, E1: golden draws identical in Node, Chromium, WebKit
// and Firefox): each browser instance replays every line of rng.golden.jsonl and must reproduce the bits of
// normal() that Node recorded in rng.normal-bits.txt.
import { describe, expect, it } from 'vitest';
import { mismatches, parseGoldens, renderNormalBits } from './rng-goldens.ts';

// Vite rewrites `new URL('./file', import.meta.url)` to the file's URL on the test server, as in
// dmath.browser.test.ts.
const text = async (url: URL): Promise<string> => (await fetch(url)).text();

describe('rng in this engine', () => {
  it('meets every golden line and reproduces the bits of normal()', async () => {
    const goldens = parseGoldens(await text(new URL('./rng.golden.jsonl', import.meta.url)));
    expect(goldens).toHaveLength(316);
    expect(goldens.flatMap(mismatches)).toEqual([]);
    expect(renderNormalBits(goldens)).toBe(await text(new URL('./rng.normal-bits.txt', import.meta.url)));
  });
});
