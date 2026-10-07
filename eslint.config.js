// ESLint flat config (ARCHITECTURE.md 10.4). Type-aware rules everywhere TypeScript is checked.
import js from '@eslint/js';
import { defineConfig, globalIgnores } from 'eslint/config';
import reactHooks from 'eslint-plugin-react-hooks';
import tseslint from 'typescript-eslint';
import zq from 'eslint-plugin-zq';

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
  ]),
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
    // ARCHITECTURE.md 10.4 scopes no-colour-literals to `.tsx`; widened to `src/**/*.ts` because
    // widget logic and scene files produce render data.
    files: ['src/**/*.{ts,tsx}'],
    rules: { 'zq/no-forbidden-apis': 'error', 'zq/no-colour-literals': 'error' },
  },
  {
    // CLAUDE.md: no eval or new Function anywhere.
    rules: { 'no-eval': 'error', 'no-new-func': 'error', 'no-implied-eval': 'error' },
  },
]);
