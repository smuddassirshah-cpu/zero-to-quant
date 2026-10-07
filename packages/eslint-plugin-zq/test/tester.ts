// RuleTester on Vitest with the TypeScript parser and JSX, as the repository's config parses code.
// `typed` adds the type checker: its cases are virtual files `typed.ts` and `typed.tsx` at the
// repository root, in typescript-eslint's default project, which has the DOM library.
import path from 'node:path';
import { RuleTester } from 'eslint';
import tseslint from 'typescript-eslint';
import { describe, it } from 'vitest';
import { REPO_ROOT } from '../src/util/paths.ts';

RuleTester.describe = describe;
RuleTester.it = it;
RuleTester.itOnly = it.only;

export const tester = new RuleTester({
  languageOptions: { parser: tseslint.parser, parserOptions: { ecmaFeatures: { jsx: true } } },
});

export const typed = new RuleTester({
  languageOptions: {
    parser: tseslint.parser,
    parserOptions: {
      projectService: { allowDefaultProject: ['typed.ts', 'typed.tsx'] },
      tsconfigRootDir: REPO_ROOT,
    },
  },
});

/** The absolute file name of a repository path, for the scoped rules. */
export const at = (file: string): string => path.join(REPO_ROOT, file);

/** The file name of a typed case. */
export const TYPED = at('typed.ts');
