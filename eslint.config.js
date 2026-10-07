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
    'tools/py/.venv/',
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
    // CLAUDE.md: no eval or new Function anywhere.
    rules: { 'no-eval': 'error', 'no-new-func': 'error', 'no-implied-eval': 'error' },
  },
]);
