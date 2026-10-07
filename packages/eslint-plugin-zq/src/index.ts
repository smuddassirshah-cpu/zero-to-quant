// Zero to Quant's own lint rules (docs/ARCHITECTURE.md 10.4), loaded by eslint.config.js as `zq`.
import type { ESLint } from 'eslint';
import noColourLiterals from './rules/no-colour-literals.ts';
import noEmptyCatch from './rules/no-empty-catch.ts';
import noForbiddenApis from './rules/no-forbidden-apis.ts';
import noInnerHtml from './rules/no-inner-html.ts';

const plugin = {
  meta: { name: 'eslint-plugin-zq', version: '0.1.0' },
  rules: {
    'no-colour-literals': noColourLiterals,
    'no-empty-catch': noEmptyCatch,
    'no-forbidden-apis': noForbiddenApis,
    'no-inner-html': noInnerHtml,
  },
} satisfies ESLint.Plugin;

export default plugin;
