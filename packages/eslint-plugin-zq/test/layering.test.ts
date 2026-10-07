import rule from '../src/rules/layering.ts';
import { at, tester } from './tester.ts';

const options = [
  {
    packages: { '@zq/mathcore': 'packages/mathcore', '@zq/contracts': 'packages/contracts' },
    layers: [
      {
        name: 'widgets/**/logic.ts',
        files: ['src/widgets/**/logic.ts'],
        allow: ['packages/mathcore/**', '$dir/**'],
        deny: ['npm:preact', 'npm:preact/**', '**/*.css'],
      },
      { name: 'screens/', files: ['src/screens/*/**'], allow: ['src/screens/$1/**'] },
      {
        name: 'engine/',
        files: ['src/engine/**'],
        allow: ['src/engine/**', 'packages/contracts/**', 'src/platform/types.ts'],
        deny: ['npm:zod'],
      },
      { name: 'tests/', files: ['tests/**'], allow: ['**'] },
    ],
  },
];

const ENGINE = at('src/engine/a.ts');
const LOGIC = at('src/widgets/primitives/slider/logic.ts');
const DOTTED = at('src/widgets/a.b/logic.ts');
const SCREEN = at('src/screens/today/View.tsx');
const refused = (layer: string, target: string) => [{ messageId: 'layer', data: { layer, target } }];
const engine = (code: string) => ({ code, filename: ENGINE, options });
const engineRefuses = (code: string, target: string) => ({
  ...engine(code),
  errors: refused('engine/', target),
});

tester.run('layering', rule, {
  valid: [
    engine('import { x } from "./b.ts"'),
    engine('import x from "@/engine/c"'),
    engine('import type { T } from "@zq/contracts"'),
    engine('import { h } from "preact"'),
    engine('import { z } from "zod/mini"'),
    engine('import "../platform/types.ts"'),
    engine('export * from "./d/index.ts"'),
    engine('export const local = 1'),
    engine('void import("./lazy.ts")'),
    engine('void import(name)'),
    engine('void import(`../screens/${name}.ts`)'),
    engine('void import(`./lazy.ts`)'),
    engine('import icon from "./icon.svg?raw"'),
    { code: 'import { a } from "./fixtures.ts"', filename: LOGIC, options },
    { code: 'import { r } from "@zq/mathcore/rng"', filename: LOGIC, options },
    { code: 'import { c } from "./c.ts"', filename: DOTTED, options },
    {
      code: 'import { x } from "./load.ts"; import { y } from "../today/copy.ts"',
      filename: SCREEN,
      options,
    },
    { code: 'import "../../src/screens/x.ts"', filename: at('tests/e2e/a.ts'), options },
    { code: 'import "../app/x.ts"', filename: at('src/elsewhere/a.ts'), options },
  ],
  invalid: [
    engineRefuses('import x from "../screens/x.ts"', 'src/screens/x.ts'),
    engineRefuses('export { y } from "../tutor/y.ts"', 'src/tutor/y.ts'),
    engineRefuses('export * from "@/app/z"', 'src/app/z'),
    engineRefuses('void import("../screens/lazy.ts")', 'src/screens/lazy.ts'),
    engineRefuses('import type { T } from "../tutor/t.ts"', 'src/tutor/t.ts'),
    engineRefuses('type M = typeof import("../screens/m.ts")', 'src/screens/m.ts'),
    engineRefuses('import { z } from "zod"', 'npm:zod'),
    engineRefuses('import { m } from "@zq/mathcore"', 'packages/mathcore'),
    {
      code: 'import { h } from "preact"; import "preact/hooks"; import s from "./view.module.css"',
      filename: LOGIC,
      options,
      errors: [
        ...refused('widgets/**/logic.ts', 'npm:preact'),
        ...refused('widgets/**/logic.ts', 'npm:preact/hooks'),
        ...refused('widgets/**/logic.ts', 'src/widgets/primitives/slider/view.module.css'),
      ],
    },
    {
      code: 'import { o } from "../other/logic.ts"',
      filename: LOGIC,
      options,
      errors: refused('widgets/**/logic.ts', 'src/widgets/primitives/other/logic.ts'),
    },
    {
      code: 'import { c } from "../aXb/c.ts"',
      filename: DOTTED,
      options,
      errors: refused('widgets/**/logic.ts', 'src/widgets/aXb/c.ts'),
    },
    {
      code: 'import { v } from "../learn/View.tsx"',
      filename: SCREEN,
      options,
      errors: refused('screens/', 'src/screens/learn/View.tsx'),
    },
  ],
});
