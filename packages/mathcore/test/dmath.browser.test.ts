// dmath's bit-identity across engines (docs/PLAN.md stage 3): each browser instance (Chromium, Firefox and
// WebKit in CI's Playwright image) evaluates all 10,000 goldens and must reproduce the bits Node recorded.
import { describe, expect, it } from 'vitest';
import { parseGoldens, renderBits } from './dmath-goldens.ts';

// Vite rewrites `new URL('./file', import.meta.url)` to the file's URL on the test server [measured]; a
// computed name would not be rewritten.
const text = async (url: URL): Promise<string> => (await fetch(url)).text();

describe('dmath in this engine', () => {
  it('reproduces the bits Node recorded for every golden', async () => {
    const goldens = parseGoldens(await text(new URL('./dmath.goldens.txt', import.meta.url)));
    expect(goldens).toHaveLength(10_000);
    expect(renderBits(goldens)).toBe(await text(new URL('./dmath.bits.txt', import.meta.url)));
  });
});
