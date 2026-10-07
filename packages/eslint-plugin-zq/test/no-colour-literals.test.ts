import rule from '../src/rules/no-colour-literals.ts';
import { tester } from './tester.ts';

const colour = (literal: string) => [{ messageId: 'colour', data: { colour: literal } }];

tester.run('no-colour-literals', rule, {
  valid: [
    'const route = "#/system"',
    'const root = "#app"',
    'const five = "#abcde"',
    'const glued = "a#fff"',
    'const id = "#fff-x"',
    'const word = "#fffx"',
    'const named = "red"',
    'const call = "toRgb(x)"',
    'const spelt = "colour(1)"',
    'const room = "the lab (west)"',
    'const token = "var(--zq-ink)"',
    'const n = 1',
    'const built = `#${hex}`',
  ],
  invalid: [
    { code: 'const c = "#abc"', errors: colour('#abc') },
    { code: 'const c = "#ABCD"', errors: colour('#ABCD') },
    { code: 'const c = "#aabbcc"', errors: colour('#aabbcc') },
    { code: 'const c = "#aabbccdd"', errors: colour('#aabbccdd') },
    { code: 'const c = "border: 1px solid #FFF"', errors: colour('#FFF') },
    { code: 'const c = "0 0 1px,#fff"', errors: colour('#fff') },
    { code: 'const c = "rgb(0, 0, 0)"', errors: colour('rgb(0, 0, 0)') },
    { code: 'const c = "RGBA(0,0,0,.5)"', errors: colour('RGBA(0,0,0,.5)') },
    { code: 'const c = "hsl(0 0% 0%)"', errors: colour('hsl(0 0% 0%)') },
    { code: 'const c = "oklch(70% 0.1 200)"', errors: colour('oklch(70% 0.1 200)') },
    { code: 'const c = "lab(50% 0 0)"', errors: colour('lab(50% 0 0)') },
    { code: 'const c = "color-mix(in srgb, red, blue)"', errors: colour('color-mix(in srgb, red, blue)') },
    { code: 'const c = "color(display-p3 1 0 0)"', errors: colour('color(display-p3 1 0 0)') },
    { code: 'const c = `rgb(${r}, 0, 0)`', errors: colour('rgb(') },
    { code: 'const c = String.raw`\\xz #fff`', errors: colour('#fff') },
    { code: '<div style="color: #fff" />', errors: colour('#fff') },
    { code: 'type Ink = "#000"', errors: colour('#000') },
  ],
});
