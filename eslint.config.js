// ESLint flat config (ARCHITECTURE.md 10.4). Type-aware rules everywhere TypeScript is checked.
import js from '@eslint/js';
import { defineConfig, globalIgnores } from 'eslint/config';
import reactHooks from 'eslint-plugin-react-hooks';
import tseslint from 'typescript-eslint';
import zq from 'eslint-plugin-zq';

// Workspace package name -> repository directory, for zq/layering's resolver.
const packages = {
  '@zq/contracts': 'packages/contracts',
  '@zq/mathcore': 'packages/mathcore',
  '@zq/models': 'packages/models',
  '@zq/content-schema': 'packages/content-schema',
  '@zq/compiler': 'packages/content-compiler',
  '@zq/graders': 'packages/graders',
  '@zq/gen': 'packages/gen-kit',
  'eslint-plugin-zq': 'packages/eslint-plugin-zq',
};

// The table of docs/ARCHITECTURE.md 4.5. zq/layering takes the first layer whose `files` glob
// matches, so the most specific layer comes first. Globs: `**`, `*`, `$1` (the importer's first
// `*` capture) and `$dir` (the importer's directory); extensions and a target's `/index` are
// ignored. `deny` reads in order, last match wins, and `!` re-allows. Every file the rule runs on
// matches a row: an unlisted src/ folder reaches a catch-all, while packages/, tools/ and proxy/
// end in rows that cover their whole trees.
const pure = ['packages/contracts/**', 'packages/mathcore/**', 'packages/models/**'];
const runtime = [...pure, 'packages/content-schema/**', 'packages/graders/**', 'packages/gen-kit/**'];
const schemas = 'src/widgets/**/schema.ts';
// Classic zod and widget schemas (classic zod too) never reach a main-thread bundle; zod/mini may.
const mainThread = [
  'npm:zod',
  'npm:zod/v3',
  'npm:zod/v4',
  'npm:zod/v4/classic',
  'npm:zod/v4/classic/**',
  schemas,
];
const views = ['npm:preact', 'npm:preact/**', 'npm:@preact/**', '**/*.css', '**/View.tsx'];
const widgetEngine = [
  'src/engine/widgets/api.ts',
  'src/engine/interaction/**',
  'src/engine/render/**',
  'src/engine/motion/**',
  'src/ui/**',
  ...pure,
];
const shell = [
  'src/engine/**',
  'src/widgets/registry.gen.ts',
  'src/tutor/**',
  'src/ui/**',
  'src/platform/types.ts',
];
const platform = (name) => ({
  name: `platform/${name}`,
  files: [`src/platform/${name}/**`],
  allow: [`src/platform/${name}/**`, 'src/platform/shared/**', 'src/platform/types.ts', ...runtime],
  allowTypes: ['src/engine/**'],
  deny: mainThread,
});
const unlisted = 'add a layer row for it in eslint.config.js';
// npm packages @zq/contracts may import, and only as types (ARCHITECTURE.md 5.3).
const contractTypes = ['preact', 'preact/**', '@preact/signals-core', 'zod', 'zod/**'];
// What the packages that run in both Node and the browser (ARCHITECTURE.md 4.3) may not read: Node's own
// globals, and the browser's that Node lacks or that differ there. tsc does not catch them, since every
// packages/* project carries Node's types (tsconfig.node.base.json), nor does tools/ci/plain-node.ts, which
// imports in Node and sees only what a module reads at import time [measured, adversarial review of
// 8 October 2026]. Type names such as HTMLElement stay usable in type positions.
const isomorphic = ['packages/contracts/src/**/*.ts', 'packages/mathcore/src/**/*.ts'];
const hostGlobals = [
  'process Buffer global require module exports __dirname __filename setImmediate clearImmediate',
  'window self document navigator location history localStorage sessionStorage indexedDB',
  'customElements requestAnimationFrame cancelAnimationFrame getComputedStyle',
].flatMap((line) => line.split(' '));
const hostMessage =
  'This package runs in Node and the browser alike (ARCHITECTURE.md 4.3): receive it as a parameter';
const layers = [
  {
    name: 'a test',
    files: ['**/*.test.ts', '**/*.test.tsx', 'packages/**/test/**'],
    allow: ['**'],
  },
  { name: 'entries/', files: ['src/entries/**'], allow: ['**'], deny: mainThread },
  {
    name: 'widgets/**/logic.ts',
    files: ['src/widgets/**/logic.ts'],
    allow: [...pure, '$dir/**'],
    deny: [...views, 'npm:**', schemas],
  },
  {
    name: 'widgets/scenes/**/scene.ts',
    files: ['src/widgets/scenes/**/scene.ts'],
    allow: [...pure, '$dir/**', 'src/widgets/scene/define.ts', 'src/widgets/primitives/*/logic.ts'],
    deny: [...views, 'npm:**', schemas],
  },
  {
    name: 'widgets/**/schema.ts',
    files: ['src/widgets/**/schema.ts'],
    allow: [...pure, '$dir/**'],
    deny: [...views, 'npm:**', '!npm:zod'],
  },
  {
    name: 'widgets/registry.node.gen.ts',
    files: ['src/widgets/registry.node.gen.ts'],
    allow: ['src/widgets/**', ...pure],
    deny: views,
  },
  {
    name: 'widgets/scene/',
    files: ['src/widgets/scene/**'],
    allow: [
      ...widgetEngine,
      'src/widgets/scene/**',
      'src/widgets/primitives/**',
      'src/widgets/inputs/**',
      'src/widgets/composites/*/*/View.tsx',
    ],
    deny: mainThread,
  },
  {
    name: 'widgets/',
    files: ['src/widgets/**'],
    allow: [...widgetEngine, 'src/widgets/**'],
    deny: mainThread,
  },
  {
    name: 'app/',
    files: ['src/app/**'],
    allow: ['src/app/**', 'src/screens/**', ...shell, ...runtime],
    deny: mainThread,
  },
  {
    name: 'screens/',
    files: ['src/screens/*/**'],
    allow: ['src/screens/$1/**', 'src/app/**', ...shell, ...runtime],
    deny: mainThread,
  },
  {
    name: 'tutor/',
    files: ['src/tutor/**'],
    allow: ['src/tutor/**', 'src/engine/**', 'src/ui/**', 'src/platform/types.ts', ...runtime],
    deny: mainThread,
  },
  {
    name: 'engine/',
    files: ['src/engine/**'],
    allow: ['src/engine/**', 'src/ui/**', 'src/platform/types.ts', ...runtime],
    deny: mainThread,
  },
  {
    name: 'ui/',
    files: ['src/ui/**'],
    allow: ['src/ui/**', 'src/engine/motion/**', 'packages/contracts/**'],
    deny: mainThread,
  },
  platform('web'),
  platform('artifact'),
  {
    name: 'platform/',
    files: ['src/platform/**'],
    allow: ['src/platform/types.ts', 'src/platform/shared/**', 'src/platform/fake/**', ...runtime],
    deny: mainThread,
  },
  {
    name: 'workers/',
    files: ['src/workers/**'],
    allow: ['src/workers/**', 'src/engine/progress/fold/**', 'src/engine/rpc.ts', ...runtime],
  },
  { name: 'sw/', files: ['src/sw/**'], allow: ['src/sw/**', ...runtime] },
  {
    name: 'an unlisted src/ folder',
    files: ['src/*/**', 'src/*'],
    allow: ['src/$1/**'],
    deny: ['npm:**'],
    note: unlisted,
  },
  // ARCHITECTURE.md 4.5 and 5.3: contracts import no other workspace package, and of npm only the types of
  // preact, @preact/signals-core and zod (the type-only rule is no-restricted-imports below); mathcore
  // imports only contracts, and no npm package or Node builtin, so both run unchanged in Node and the
  // browser (4.3) [our choice: the deny lists].
  {
    name: 'packages/contracts',
    files: ['packages/contracts/**'],
    allow: ['packages/contracts/**'],
    deny: ['npm:**', ...contractTypes.map((name) => `!npm:${name}`)],
  },
  {
    name: 'packages/mathcore',
    files: ['packages/mathcore/**'],
    allow: ['packages/mathcore/**', 'packages/contracts/**'],
    deny: ['npm:**'],
  },
  { name: 'packages/*', files: ['packages/*/**'], allow: ['packages/**'], deny: ['src/**', 'tools/**'] },
  {
    name: 'tools/zq',
    files: ['tools/zq/**'],
    allow: [
      'packages/*/**',
      'tools/**',
      'src/widgets/registry.node.gen.ts',
      'src/widgets/**/logic.ts',
      'src/widgets/**/schema.ts',
      'src/widgets/presets/**',
    ],
    deny: ['**/View.tsx', '**/*.css'],
  },
  { name: 'tools/', files: ['tools/**'], allow: ['**'], deny: ['src/**'] },
  {
    name: 'proxy/',
    files: ['proxy/**'],
    allow: ['proxy/**', 'packages/*/**', 'src/tutor/context/schema.ts', 'src/tutor/render/anthropic.ts'],
  },
  { name: 'tests/', files: ['tests/**'], allow: ['**'] },
  { name: 'a root config file', files: ['*.config.ts', '*.config.js'], allow: ['packages/*/**', 'tools/**'] },
];

export default defineConfig([
  globalIgnores([
    'dist/',
    '.zq/',
    'coverage/',
    'prototype/',
    'spikes/',
    'docs/',
    'node_modules/',
    'test-results/',
    '.workflows/',
    '.claude/',
    'tools/py/.venv/',
  ]),
  {
    // No inline disables or inline configuration of any rule: an exception belongs in this file,
    // where review sees it. An inline directive is reported and has no effect.
    linterOptions: { noInlineConfig: true, reportUnusedDisableDirectives: 'error' },
  },
  js.configs.recommended,
  {
    files: ['**/*.{ts,tsx}'],
    extends: [tseslint.configs.strictTypeChecked, tseslint.configs.stylisticTypeChecked],
    languageOptions: {
      parserOptions: { projectService: true, tsconfigRootDir: import.meta.dirname },
    },
    rules: {
      '@typescript-eslint/restrict-template-expressions': ['error', { allowNumber: true }],
    },
  },
  {
    files: ['src/**/*.{ts,tsx}'],
    plugins: { 'react-hooks': reactHooks },
    rules: reactHooks.configs.recommended.rules,
  },
  {
    files: ['**/*.js'],
    languageOptions: { globals: { console: 'readonly', process: 'readonly' } },
  },
  {
    plugins: { zq },
  },
  {
    files: ['**/*.{ts,tsx,js,mjs}'],
    rules: { 'zq/no-empty-catch': 'error', 'zq/no-inner-html': 'error' },
  },
  {
    // ARCHITECTURE.md 10.4 scopes no-colour-literals to `.tsx`; widened to every script under src/
    // because widget logic and scene files produce render data, and `.js` must not be a way round.
    files: ['src/**/*.{ts,tsx,js,mjs}'],
    rules: { 'zq/no-forbidden-apis': 'error', 'zq/no-colour-literals': 'error' },
  },
  {
    files: ['{src,packages,tools,proxy,tests}/**/*.{ts,tsx,js,mjs}', '*.config.{ts,js}'],
    rules: { 'zq/layering': ['error', { layers, packages }] },
  },
  {
    files: isomorphic,
    ignores: ['**/*.test.ts'],
    rules: {
      'no-restricted-globals': ['error', ...hostGlobals.map((name) => ({ name, message: hostMessage }))],
      'no-restricted-properties': [
        'error',
        ...hostGlobals.map((property) => ({ object: 'globalThis', property, message: hostMessage })),
      ],
    },
  },
  {
    // zq/layering lets contracts reach these packages; this rule keeps the imports type-only, since a
    // value import would put a runtime dependency under the shared types (ARCHITECTURE.md 5.3). No other
    // entry sets this rule, so none replaces it per file (the flat-config problem of 4.5).
    files: ['packages/contracts/src/**/*.ts'],
    ignores: ['**/*.test.ts'],
    rules: {
      '@typescript-eslint/no-restricted-imports': [
        'error',
        {
          patterns: [
            {
              group: contractTypes,
              allowTypeImports: true,
              message: '@zq/contracts imports npm packages as types only (ARCHITECTURE.md 5.3)',
            },
          ],
        },
      ],
    },
  },
  {
    // CLAUDE.md: no eval or new Function anywhere.
    rules: { 'no-eval': 'error', 'no-new-func': 'error', 'no-implied-eval': 'error' },
  },
]);
