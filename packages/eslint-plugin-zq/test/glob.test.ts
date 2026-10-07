import { describe, expect, it } from 'vitest';
import { glob, globPrefix } from '../src/util/glob.ts';

describe('glob', () => {
  it('substitutes tokens as literals', () => {
    expect(glob('src/screens/$1/**', { cap: 'a.b' }).test('src/screens/aXb/x')).toBe(false);
    expect(glob('$dir/**', { dir: 'src/w' }).test('src/w/x')).toBe(true);
  });
});

describe('globPrefix', () => {
  it.each([
    ['src/widgets/**/schema', 'src/widgets/a/b/', true],
    ['src/widgets/**/schema', 'src/wid', true],
    ['src/widgets/**/schema', 'src/engine/', false],
    ['src/engine/**', 'src/engine', true],
    ['src/engine/**', 'src/engine/x/', true],
    ['src/engine/**', 'src/engineX', false],
    ['**/*.css', 'src/anything/', true],
    ['src/*/logic', 'src/abc', true],
    ['src/*/logic', 'src/abc/lo', true],
    ['src/*/logic', 'src/a/b/', false],
    ['npm:zod', 'npm:zo', true],
    ['npm:zod', 'npm:zod/', false],
    ['$dir/x', 'src/w/', true],
    ['src/screens/$1/**', 'src/screens/other/', false],
  ])('%s overlaps a path beginning %s: %s', (pattern, prefix, overlaps) => {
    expect(globPrefix(pattern, { dir: 'src/w', cap: 'today' }).test(prefix)).toBe(overlaps);
  });
});
