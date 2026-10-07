import rule from '../src/rules/layering.ts';
import { at, tester } from './tester.ts';

const NOTE = 'add a layer row';
const options = [
  {
    packages: { '@zq/mathcore': 'packages/mathcore', '@zq/contracts': 'packages/contracts' },
    layers: [
      { name: 'a test', files: ['**/*.test.ts', 'packages/**/test/**'], allow: ['**'] },
      {
        name: 'widgets/**/logic.ts',
        files: ['src/widgets/**/logic.ts'],
        allow: ['packages/mathcore/**', '$dir/**'],
        deny: ['**/*.css', 'npm:**'],
      },
      {
        name: 'widgets/**/schema.ts',
        files: ['src/widgets/**/schema.ts'],
        allow: ['$dir/**'],
        deny: ['npm:**', '!npm:zod'],
      },
      { name: 'screens/', files: ['src/screens/*/**'], allow: ['src/screens/$1/**'] },
      {
        name: 'widgets/',
        files: ['src/widgets/**'],
        allow: ['src/widgets/**', 'src/engine/render/**'],
        deny: ['src/widgets/**/schema.ts'],
      },
      {
        name: 'engine/',
        files: ['src/engine/**'],
        allow: ['src/engine/**', 'packages/contracts/**', 'src/platform/types.ts'],
        deny: ['npm:zod'],
      },
      {
        name: 'platform/web',
        files: ['src/platform/web/**'],
        allow: ['src/platform/web/**'],
        allowTypes: ['src/engine/**'],
      },
      { name: 'an unlisted src/ folder', files: ['src/*/**', 'src/*'], allow: ['src/$1/**'], note: NOTE },
      { name: 'tests/', files: ['tests/**'], allow: ['**'] },
    ],
  },
];

const ENGINE = at('src/engine/a.ts');
const LOGIC = at('src/widgets/primitives/slider/logic.ts');
const SCHEMA = at('src/widgets/primitives/slider/schema.ts');
const DOTTED = at('src/widgets/a.b/logic.ts');
const SCREEN = at('src/screens/today/View.tsx');
const WEB = at('src/platform/web/index.ts');
const ELSEWHERE = at('src/elsewhere/a.ts');
const VIEW = at('src/widgets/primitives/slider/View.tsx');
const dynamic = (layer: string) => [{ messageId: 'dynamic', data: { layer } }];
const refused = (layer: string, target: string) => [
  { messageId: 'layer', data: { layer, target, note: '' } },
];
const problem = (messageId: string, specifier: string) => [{ messageId, data: { specifier } }];
const from = (filename: string) => (code: string) => ({ code, filename, options });
const engine = from(ENGINE);
const web = from(WEB);
const engineRefuses = (code: string, target: string) => ({
  ...engine(code),
  errors: refused('engine/', target),
});
const webRefuses = (code: string) => ({ ...web(code), errors: refused('platform/web', 'src/engine/t.ts') });
const logicRefuses = (code: string, target: string, filename = LOGIC) => ({
  code,
  filename,
  options,
  errors: refused('widgets/**/logic.ts', target),
});

tester.run('layering', rule, {
  valid: [
    engine('import { x } from "./b.ts"'),
    engine('import x from "@/engine/c"'),
    engine('import type { T } from "@zq/contracts"'),
    engine('import { h } from "preact"'),
    engine('import { z } from "zod/mini"'),
    engine('import "../platform/types.ts"'),
    engine('import "../platform/types.mts"'),
    engine('export * from "./d/index.ts"'),
    engine('export const local = 1'),
    engine('void import("./lazy.ts")'),
    engine('void import(`./lazy.ts`)'),
    engine('void import(`./lazy/${name}.ts`)'),
    engine('void import("./lazy-" + name)'),
    engine('import icon from "./icon.svg?raw"'),
    { code: 'import { a } from "./fixtures.ts"', filename: LOGIC, options },
    { code: 'import { r } from "@zq/mathcore/rng"', filename: LOGIC, options },
    { code: 'import { c } from "./c.ts"', filename: DOTTED, options },
    { code: 'import { z } from "zod"', filename: SCHEMA, options },
    from(SCREEN)('import { x } from "./load.ts"; import { y } from "../today/copy.ts"'),
    from(VIEW)('void import(`../../../engine/render/${name}.ts`)'),
    from(at('tests/e2e/a.ts'))('void import(name)'),
    from(at('src/app/a.test.ts'))('void import(`${name}.ts`)'),
    web('import type { T } from "../../engine/t.ts"'),
    web('import { type T, type U } from "../../engine/t.ts"'),
    web('export type { T } from "../../engine/t.ts"'),
    web('export type * from "../../engine/t.ts"'),
    web('type M = import("../../engine/t.ts").M'),
    from(ELSEWHERE)('import { b } from "./b.ts"'),
    from(at('src/engine/a.test.ts'))('import "../screens/x.ts"'),
    from(at('packages/x/test/helper.ts'))('import "../../../src/app/x.ts"'),
    from(at('tests/e2e/a.ts'))('import "../../src/screens/x.ts"'),
    from(at('docs/a.ts'))('import "../src/app/x.ts"'),
  ],
  invalid: [
    engineRefuses('import x from "../screens/x.ts"', 'src/screens/x.ts'),
    engineRefuses('export { y } from "../tutor/y.ts"', 'src/tutor/y.ts'),
    engineRefuses('export * from "@/app/z"', 'src/app/z'),
    engineRefuses('import x from "@/engine/../screens/x.ts"', 'src/screens/x.ts'),
    engineRefuses('void import("../screens/lazy.ts")', 'src/screens/lazy.ts'),
    engineRefuses('void import(`../screens/${name}.ts`)', 'src/screens/**'),
    engineRefuses('void import("../screens/" + name)', 'src/screens/**'),
    engineRefuses('import type { T } from "../tutor/t.ts"', 'src/tutor/t.ts'),
    engineRefuses('type M = typeof import("../screens/m.ts")', 'src/screens/m.ts'),
    engineRefuses('import { z } from "zod"', 'npm:zod'),
    engineRefuses('import { m } from "@zq/mathcore"', 'packages/mathcore'),
    { ...engine('void import(name)'), errors: dynamic('engine/') },
    { ...engine('void import(`${name}.ts`)'), errors: dynamic('engine/') },
    { ...from(SCREEN)('void import(name)'), errors: dynamic('screens/') },
    { ...from(WEB)('void import(`${name}`)'), errors: dynamic('platform/web') },
    {
      ...from(VIEW)('void import(`./${name}/schema.ts`)'),
      errors: refused('widgets/', 'src/widgets/primitives/slider/**'),
    },
    {
      ...from(VIEW)('void import("../" + name + "/schema.ts")'),
      errors: refused('widgets/', 'src/widgets/primitives/**'),
    },
    {
      ...from(LOGIC)('void import(`./${name}.ts`)'),
      errors: refused('widgets/**/logic.ts', 'src/widgets/primitives/slider/**'),
    },
    {
      ...from(SCHEMA)('void import(`zod/${name}`)'),
      errors: refused('widgets/**/schema.ts', 'npm:zod/**'),
    },
    { ...engine('import "../../../x.ts"'), errors: problem('outside', '../../../x.ts') },
    { ...engine('import "@/../../x.ts"'), errors: problem('outside', '@/../../x.ts') },
    { ...engine('import "/abs/x.ts"'), errors: problem('outside', '/abs/x.ts') },
    {
      ...engine('import "@zq/mathcore/../../src/app/x.ts"'),
      errors: problem('escape', '@zq/mathcore/../../src/app/x.ts'),
    },
    { ...engine('import "@zq/unknown"'), errors: problem('unmapped', '@zq/unknown') },
    webRefuses('import { T } from "../../engine/t.ts"'),
    webRefuses('import { type T, U } from "../../engine/t.ts"'),
    webRefuses('import "../../engine/t.ts"'),
    webRefuses('void import("../../engine/t.ts")'),
    logicRefuses('import { h } from "preact"', 'npm:preact'),
    logicRefuses('import "node:fs"', 'npm:node:fs'),
    logicRefuses('import s from "./view.module.css"', 'src/widgets/primitives/slider/view.module.css'),
    logicRefuses('import { o } from "../other/logic.ts"', 'src/widgets/primitives/other/logic.ts'),
    logicRefuses('import { c } from "../aXb/c.ts"', 'src/widgets/aXb/c.ts', DOTTED),
    {
      code: 'import "zod/mini"',
      filename: SCHEMA,
      options,
      errors: refused('widgets/**/schema.ts', 'npm:zod/mini'),
    },
    {
      code: 'import { v } from "../learn/View.tsx"',
      filename: SCREEN,
      options,
      errors: refused('screens/', 'src/screens/learn/View.tsx'),
    },
    {
      code: 'import { v } from "./today/View.tsx"',
      filename: at('src/screens/index.ts'),
      options,
      errors: refused('screens/', 'src/screens/today/View.tsx'),
    },
    {
      code: 'import "../app/x.ts"',
      filename: ELSEWHERE,
      options,
      errors: [
        {
          messageId: 'layerNote',
          data: { layer: 'an unlisted src/ folder', target: 'src/app/x.ts', note: NOTE },
        },
      ],
    },
  ],
});
